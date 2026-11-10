# Action Bar: a Virtue Assistant module (module key "actionbar", category "On screen").
# This file is not a script to run on its own. The mother script (VirtueAssistant.py) loads it
# from the modules folder beside it and runs it in the mother's namespace, so API, G, safe, Kit,
# HOST, Journal and the main loop are all provided by the host. Delete the file to leave the
# module out; the rest of Virtue Assistant carries on without it.
#
# The module is one function, _module_actionbar, that builds everything in its own namespace and
# returns its hooks to the host. It draws the bar (action cells with counters, window buttons,
# bag slots, twelve pages, keybind mode and a tray for windows folded into the bar) and links to
# the Bags module, Grimoire and the Virtue Assistant window through shared vars and HOST.
def _module_actionbar():
    """Build the Action Bar module and return its hooks for the host.

    Holds all the module state (settings, cells, st, win, menu, tray, page), its saved-var keys and
    every helper below, so nothing leaks into the mother's namespace. Called once by the host's
    module loader on the script thread.
    """
    KEY = "actionbar"
    TITLE = "Action Bar"
    SETTINGS_KEY = "ActionBar_settings"
    POS_KEY = "ActionBar_pos"
    MIN_KEY = "ActionBar_min"
    # Slot counts: the top row is plain squares, the bottom row has pages, the buttons are the
    # window-button strip. Extra rows sit above the top row.
    TOP_SLOTS = 24
    BOTTOM_SLOTS = 12
    UI_SLOTS = 11
    BAG_SLOTS = 5
    ACTION_SLOTS = TOP_SLOTS + BOTTOM_SLOTS
    PAGES = 12
    PAGE_W = 22
    SLOT_MIN, SLOT_MAX = 36, 64
    SCALE_MIN, SCALE_MAX = 50, 150
    BAR_M = 8
    CTRL_W = 44
    UI_SHARE = 0.65
    UI_GAP = 4
    BAG_GAP = 3
    TRAY_BTN = 30
    TRAY_GAP = 4
    # Graphic id of the stone tile drawn behind a slot.
    SLOT_TILE = 2624
    SLOT_ALPHA = 0.92
    COUNT_EVERY = 0.75
    HELD_KEY_STALE = 2.0
    LOW_DEFAULT = 5
    COUNT_SOON = 0.1
    # Spell names treated as harmful (they ask for a target on someone else).
    HARMFUL_SPELLS = set(("clumsy|feeblemind|magic arrow|weaken|harm|fireball|poison|curse|lightning|mana drain|"
                          "mind blast|paralyze|dispel|energy bolt|explosion|mass curse|chain lightning|flamestrike|"
                          "mana vampire|meteor swarm|earthquake|mass dispel|paralyze field").split("|"))
    TRAVEL_WAYS = [("recall", "Recall (spell)"), ("gate", "Gate Travel (spell)"),
                   ("charge", "Recall (a book charge)"), ("recall_scroll", "Recall scroll"),
                   ("gate_scroll", "Gate Travel scroll"), ("sacred", "Sacred Journey (spell)")]
    TRAVEL_VERB = {"recall": "Recall", "gate": "Gate", "charge": "Recall (charge)",
                   "recall_scroll": "Recall scroll", "gate_scroll": "Gate scroll", "sacred": "Sacred Journey"}
    TRAVEL_SCROLL = {"recall_scroll": 0x1F4C, "gate_scroll": 0x1F60}
    TRAVEL_ITEM = {"charge": 0x22C5, "recall_scroll": 0x1F4C, "gate_scroll": 0x1F60}
    TRAVEL_SPELL = {"recall": "Recall", "gate": "Gate Travel", "sacred": "Sacred Journey"}
    # Shared vars and keys that link this bar to the Bags module, Grimoire and the host window.
    UB_MODULE_KEY = "bag"
    UB_LINK_ALIVE = "ActionBar_alive"
    GRIM_MODULE_KEY = "grimoire"
    GRIM_LINK_CMD = "Grimoire_cmd"
    VA_LINK_CMD = "VirtueAssistant_cmd"
    CELLS_KEY = "ActionBar_cells"
    PAGES_KEY = "ActionBar_pages"
    EXTRA_KEY = "ActionBar_extra"
    EXTRA_ROWS = 4
    EXTRA_SLOTS = EXTRA_ROWS * TOP_SLOTS
    MINI_W, MINI_H = 240, 46
    UI_ACTIONS = [("paperdoll",   "Paperdoll",         0x1F03, "paperdoll"),
        ("status",      "Status",            0x0F0C, "ga:OpenStatusBar"),
        ("journal",     "Journal",           0x0FF0, "ga:OpenJournal:ResizableJournal"),
        ("skills",      "Skills",            0x13E3, "ga:OpenSkills"),
        ("spellbook",   "Grimoire",          0x0EFA, "grimoire"),
        ("worldmap",    "World map",         0x14EB, "ga:OpenWorldMap"),
        ("minimap",     "Mini map",          0x14F5, "ga:OpenMiniMap"),
        ("quests",      "Quest log",         0x0E34, "quests"),
        ("guild",       "Guild",             0x1B76, "ga:OpenGuildGump"),
        ("party",       "Party",             0x1F14, "macro:PartyManifest"),
        ("chat",        "Chat",              0x0E37, "ga:OpenChat"),
        ("options",     "Options",           0x1EB8, "ga:OpenSettings"),
        ("help",        "Help",              0x0FEF, "help"), ("war",         "War / peace",       0x13FF, "war"),
        ("barsettings", "Bar settings",      0x0FBF, "barsettings"),
        ("virtue",      "Virtue Assistant",  0x1053, "virtue"),
        ("lock",        "Lock / unlock bar", 0x100F, "lock"), ("minimize",    "Minimize bar",      0,      "minimize"),]
    SPELLBOOKS = (0x0EFA, 0x2253, 0x2252, 0x238C, 0x23A0, 0x2D50, 0x2D9D)
    UI_TIPS = {"paperdoll": "Open your paperdoll", "status": "Open the status bar", "journal": "Open the journal",
               "skills": "Open the skills window", "worldmap": "Open TazUO's World Map", "minimap": "Open the mini map",
               "quests": "Open the quest log", "guild": "Open the guild window", "party": "Open the party window",
               "chat": "Open the chat window", "options": "Open the client's options", "help": "Open the help menu",
               "war": "Switch war and peace mode", "barsettings": "Open the Action Bar settings page",
               "lock": "Lock or unlock the bar", "minimize": "Minimize the bar"}
    DEFAULT_UI = "paperdoll status skills spellbook guild chat minimap worldmap options barsettings virtue".split()
    OLD_DEFAULT_UI = ["paperdoll", "status", "journal", "skills", "spellbook", "worldmap",
                      "minimap", "quests", "options", "barsettings", "virtue"]
    CTRL_ROW_MIN = 16
    CTRL_PAD = 2
    SKILLS = ("Anatomy|Animal Lore|Animal Taming|Arms Lore|Begging|Cartography|Detect Hidden|Discordance|"
              "Evaluate Intelligence|Forensic Evaluation|Hiding|Inscription|Item Identification|Meditation|"
              "Peacemaking|Poisoning|Provocation|Remove Trap|Spirit Speak|Stealing|Stealth|Taste Identification|"
              "Tracking").split("|")
    SCHOOL_NAMES = ["Magery", "Necromancy", "Chivalry", "Bushido", "Ninjitsu", "Spellweaving", "Mysticism"]
    MENU_ROWS = 16
    MENU_COLS = 4
    MENU_ROW_H = 20
    TYPES = [("", "Empty"), ("item", "Item + counter"), ("spell", "Spell"),
             ("skill", "Skill"), ("macro", "TazUO macro"), ("ability", "Weapon ability"),
             ("script", "Legion script"), ("dress", "Dress outfit"),
             ("undress", "Undress outfit"), ("say", "Say text"), ("ui", "Client window"),
             ("travel", "Travel (runebook)")]
    TRAVEL_KEYS = ("rb", "ri", "rm")
    TARGETS = [("", "None"), ("self", "Self"), ("last", "Last target")]
    BAG_MODES = ["Bags' slots", "Bags I pick", "Backpack + sub-bags"]
    # Icon bases per spell school: each spell's icon is its school's base plus its index in the list.
    SPELL_SCHOOLS = ((0x08C0, "|".join(n for n, _ in Kit.MAGERY)),
        (0x5000, "Animate Dead|Blood Oath|Corpse Skin|Curse Weapon|Evil Omen|Horrific Beast|"
                 "Lich Form|Mind Rot|Pain Spike|Poison Strike|Strangle|Summon Familiar|"
                 "Vampiric Embrace|Vengeful Spirit|Wither|Wraith Form|Exorcism"),
        (0x5100, "Cleanse by Fire|Close Wounds|Consecrate Weapon|Dispel Evil|Divine Fury|"
                 "Enemy of One|Holy Light|Noble Sacrifice|Remove Curse|Sacred Journey"),
        (0x5420, "Honorable Execution|Confidence|Evasion|Counter Attack|Lightning Strike|Momentum Strike"),
        (0x5320, "Focus Attack|Death Strike|Animal Form|Ki Attack|Surprise Attack|Backstab|Shadowjump|Mirror Image"),
        (0x59D8, "Arcane Circle|Gift of Renewal|Immolating Weapon|Attune Weapon|Thunderstorm|"
                 "Nature's Fury|Summon Fey|Summon Fiend|Reaper Form|Wildfire|Essence of Wind|"
                 "Dryad Allure|Ethereal Voyage|Word of Death|Gift of Life|Arcane Empowerment"),
        (0x5DC0, "Nether Bolt|Healing Stone|Purge Magic|Enchant|Sleep|Eagle Strike|"
                 "Animated Weapon|Stone Form|Spell Trigger|Mass Sleep|Cleansing Winds|Bombard|"
                 "Spell Plague|Hail Storm|Nether Cyclone|Rising Colossus"),)
    HELP = ["Click a cell to use it; right-click it (Shift+click when right-clicks don't reach the bar) to choose "
            "what it holds: an item (counted in your pack), spell, skill, weapon ability, TazUO macro, Legion script, "
            "outfit, text to say, window or runebook destination, plus its hotkey and target.",
            "Click an empty cell to target an item for it.",
            "The 12 bottom-left cells have 12 pages, each with its own cells and hotkeys: the tiny arrows and the "
            "number switch pages.",
            "Keys (far right) starts keybind mode: hover a cell, window button or bag slot and press a key; Esc ends "
            "it, Backspace clears a key. Lock locks the bar (with zones, toggles Arrange mode); Grid shows the snap "
            "grid.",
            "Drag the bar by its stone edge; drop it near a corner, edge middle or the centre to anchor it there "
            "(upright on the left or right edge).",
            "Bag slots show the bags of Inventory > Bags: click to show the Bags window, again to fold it into the "
            "bar; right-click for its settings. With Bags I pick, click an empty slot to target a bag.",
            "The Grimoire and Virtue Assistant buttons show their window (turning Grimoire on); click again to fold "
            "it into the bar.",
            "A Module windows button (page 2 of the Client window list) turns that module on and shows its window; "
            "click again to fold it into the tray beside the bar. The bar's numbered button hides or shows the tray.",
            "A Travel (runebook) cell goes to a runebook destination by Recall, Gate Travel, a book charge, a scroll "
            "or Sacred Journey, through Grimoire (must be on); its counter shows charges or scrolls.",
            "A used skill or spell darkens the cells of that kind while they count down; a spell cell greys out while "
            "a reagent it needs is at 0. Red at: when an item's counter turns red."]
    # Defaults of the saved settings; load_settings overwrites them from the saved var.
    settings = {"slot": 44, "top": True, "keys": True, "lock": False,
                "short": True, "hue": False, "bagmode": 0, "bags": "", "page": 0,
                "scale": 100, "tray_open": True, "bagkeys": "", "extra": 0, "anchor": "", "vertical": False}
    DEFAULTS = dict(settings)
    # Cell store: "a" action cells (top row plus bottom pages), "u" window buttons, "x" extra rows.
    cells = {"a": [], "u": [], "x": [], "pages": []}

    def fresh():
        """Return the per-run state keys that a restart of the module resets (queues, timers, flags)."""
        return {"shutting": False, "queue": [], "want_target": None, "next_count": 0.0, "next_scan": 0.0,
                "rebuild_at": 0.0, "bag_sig": None, "ability_sig": None, "bind": None, "jobs": [], "redraw": set(),
                "ub_job": False, "cool": {"skill": 0.0, "spell": 0.0}, "cool_next": 0.0}

    st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "em": False, "ub_pending": False,
          "cnt": {}, "cnt_g": {}, "first": {}, "first_g": {}, "bags": [None] * BAG_SLOTS, "ub_found": None,
          "ub_cache": None, "ub_state": None, "grim_state": None, "va_state": None, "pending_on": None,
          "right_ok": None, "dock_sig": None, "watch_next": 0.0, "script_check": None, "ub_last": None}
    st.update(fresh())
    win = {"g": None, "c": {}, "store": ({}, {}), "cells": {}, "bags": {}}
    cleanup, queue, say = Kit.basics(st, TITLE)
    tray = {"g": None, "at": None}
    menu = {"g": None, "ref": None, "level": "cats", "cat": None, "page": 0, "c": {}, "bag": None, "items": [],
            "anchor": None, "moved": None, "placed": None}
    page = {"sel": ACTION_SLOTS - BOTTOM_SLOTS, "dds": []}
    # Lower-case spell name to icon graphic, built once from SPELL_SCHOOLS.
    SPELL_ICON = dict((n.lower(), base + i) for base, names in SPELL_SCHOOLS for i, n in enumerate(names.split("|")))

    def later(fn):
        """Queue fn to run later on the main loop (the host drains st["jobs"])."""
        st["jobs"].append(fn)

    def spell_icon(name):
        """Return the graphic id of a spell's icon by name (exact, then prefix), or 0 when there is none."""
        n = (name or "").strip().lower()
        if not n:
            return 0
        icon = SPELL_ICON.get(n)
        if icon is None:
            icon = next((v for k, v in SPELL_ICON.items() if k.startswith(n)), None)
        return icon if icon and Kit.pic_size(icon)[0] > 0 else 0

    def ability_info(which):
        """Return (icon graphic, name) of the player's current primary or secondary weapon ability.

        which is "primary" or "secondary". The icon is 0 when the ability is not known or has no art.
        """
        names = [str(n) for n in (API.CurrentAbilityNames() or [])]
        i = 1 if which == "secondary" else 0
        if len(names) <= i:
            return 0, ""
        name = names[i]
        known = [str(n) for n in (API.KnownAbilityNames() or [])]
        if name not in known:
            return 0, name
        idx = known.index(name)
        # The known-abilities list may start with a placeholder entry, which shifts the icon index.
        if known and known[0].lower() in ("none", "invalid"):
            idx -= 1
        icon = 0x5200 + idx
        return (icon if idx >= 0 and Kit.pic_size(icon)[0] > 0 else 0), name

    def ui_def(uid):
        """Return the UI_ACTIONS row for a window-button id, or the module row for a "mod:" id."""
        if uid.startswith("mod:"):
            return mod_def(uid[4:])
        return next((d for d in UI_ACTIONS if d[0] == uid), None)

    def mod_def(key, docks=None):
        """Return the (id, title, icon, action) row of the module with this key, or None.

        None for an unknown module and for this module itself. docks is an optional snapshot of
        HOST.docks so a caller looping over modules copies it only once.
        """
        s = HOST.by_key.get(key)
        if s is None or key == KEY:
            return None
        d = (docks if docks is not None else dict(HOST.docks)).get(key)
        icon = int(d.get("icon") or 0) if d else 0
        return ("mod:" + key, s.title, icon, "mod:" + key)

    def mod_actions():
        """Return the button rows of every module window the host knows, in the host's slot order."""
        out = []
        docks = dict(HOST.docks)
        for slot in HOST.slots:
            keys = [p[4][0] if len(p) > 4 and p[4] else "%s.%s" % (slot.key, p[0]) for p in slot.parts]
            for key in keys or [slot.key]:
                d = mod_def(key, docks)
                if d is not None:
                    out.append(d)
        return out

    def ui_all():
        """Return every window button the bar can offer: the fixed ones, then the modules'."""
        return UI_ACTIONS + mod_actions()

    def mod_tip(key):
        """Return the tooltip text for a module's window button, by that module's current state."""
        s = HOST.by_key.get(key)
        if s is None:
            return "Module '%s' (not loaded)" % key
        d = dict(HOST.docks).get(key)
        if not s.running:
            return "Turn %s on" % s.title
        if d is None:
            return "Turn %s off" % s.title
        if safe(d.get("state")) == "open":
            return "Fold %s into the bar" % s.title
        return "Show %s" % s.title

    def toggle_module(key):
        """Click action of a module button: turn it on, fold it, show it or turn it off.

        Returns True when the key was handled. A stopped module is turned on from a queued job (the
        host starts it on the main loop).
        """
        s = HOST.by_key.get(key)
        if s is None:
            say("no module '%s'." % key, Kit.HUE_BAD)
            return False
        d = dict(HOST.docks).get(key)
        if not s.running:
            HOST.dock_forget(key)

            def turn(k=key, title=s.title):
                """Turn the module on and say so when it does not start."""
                HOST.enable(k)
                if not HOST.by_key[k].running:
                    say("%s couldn't be turned on." % title, Kit.HUE_BAD)

            later(turn)
            return True
        if d is None:
            HOST.disable(key)
            return True
        if safe(d.get("state")) == "open":
            HOST.dock_to_bar(key, s.title)
        else:
            safe(d.get("show"))
            HOST.dock_forget(key)
        return True

    def key_owner(k):
        """Return the owner the host recorded for a hotkey, or None when nobody holds it."""
        return HOST.hotkeys_owned.get(_norm_key(k))

    def bar_keys():
        """Return the set of normalised keys bound on the bar (cells and bag slots)."""
        return set(_norm_key(c["k"]) for _, c in all_cells() if c["k"] and c["t"]) | set(k for k in bag_keys() if k)

    def fit(text, width):
        """Shorten text to width characters, ending in a full stop when cut."""
        return Kit.fit(str(text), width, ".")

    def short_key(k):
        """Return a key name in the short form the cell shows (CTRL+ becomes C and so on)."""
        return (k.upper().replace("CTRL+", "C").replace("SHIFT+", "S")
                .replace("ALT+", "A").replace("NUMPAD", "N").replace("KP_", "N"))

    def fmt_count(n):
        """Format a counter for a cell: 12400 as 12k and 1500 as 1.5k when "short" is on, else as is."""
        if settings["short"]:
            if n >= 10000:
                return "%dk" % (n // 1000)
            if n >= 1000:
                return "%.1fk" % (n / 1000.0)
        return str(n)

    def parse_graphic(text):
        """Parse "graphic" or "graphic,hue" (decimal or 0x hex) into (graphic, hue), or None if invalid."""
        t = (text or "").strip()
        if not t:
            return None
        a, b = [s.strip() for s in (t.split(",", 1) + [""])[:2]]
        try:
            return (int(a, 16) if a.lower().startswith("0x") else int(a),
                    (int(b, 16) if b.lower().startswith("0x") else int(b)) if b else 0)
        except Exception:
            return None

    def blank():
        """Return a new empty cell record.

        Keys: t type, v value, g graphic, h hue, tg target, k hotkey, lo red-at count, n name.
        """
        return {"t": "", "v": "", "g": 0, "h": 0, "tg": "", "k": "", "lo": LOW_DEFAULT, "n": ""}

    def cell(ref):
        """Return the cell record a (kind, index) reference points to."""
        return cells[ref[0]][ref[1]]

    def bag_keys():
        """Return the five bag-slot hotkeys from the saved list, padded with empty strings."""
        ks = [_norm_key(k) for k in settings["bagkeys"].split(",")]
        return (ks + [""] * BAG_SLOTS)[:BAG_SLOTS]

    def set_key_of(ref, k):
        """Store hotkey k on the cell or bag slot ref and save it."""
        if ref[0] == "b":
            ks = bag_keys()
            ks[ref[1]] = k
            settings["bagkeys"] = ",".join(ks)
            save_settings()
        else:
            cell(ref)["k"] = k
            save_cells()

    def ref_name(ref):
        """Return a short name for a reference, used in messages ("page 2 cell 3")."""
        kind, i = ref
        if kind == "b":
            return "bag slot %d" % (i + 1)
        if kind == "u":
            return "button %d" % (i + 1)
        if kind == "x":
            return "row %d cell %d" % (i // TOP_SLOTS + 2, i % TOP_SLOTS + 1)
        if i < TOP_SLOTS:
            return "top cell %d" % (i + 1)
        return "page %d cell %d" % (settings["page"] + 1, i - TOP_SLOTS + 1)

    def sel_ref(idx):
        """Map a settings-page selector index to a (kind, index) reference.

        Order: action cells, then window buttons, then extra rows.
        """
        if idx < ACTION_SLOTS:
            return ("a", idx)
        if idx < ACTION_SLOTS + UI_SLOTS:
            return ("u", idx - ACTION_SLOTS)
        return ("x", idx - ACTION_SLOTS - UI_SLOTS)

    def ref_sel(ref):
        """Map a (kind, index) reference back to its settings-page selector index."""
        if ref[0] == "a":
            return ref[1]
        if ref[0] == "u":
            return ACTION_SLOTS + ref[1]
        return ACTION_SLOTS + UI_SLOTS + ref[1]

    def sel_names():
        """Return the selector names for every cell, in the same order as sel_ref."""
        return (["Top %d" % (i + 1) for i in range(TOP_SLOTS)] + ["Bottom %d" % (i + 1) for i in range(BOTTOM_SLOTS)] +
                ["Button %d" % (i + 1) for i in range(UI_SLOTS)] +
                ["Row %d-%d" % (i // TOP_SLOTS + 2, i % TOP_SLOTS + 1) for i in range(EXTRA_SLOTS)])

    def shown(ref):
        """Return whether the cell is currently drawn (extra rows and the top row can be switched off)."""
        kind, i = ref
        if kind == "x":
            return i < settings["extra"] * TOP_SLOTS
        if kind == "a":
            return settings["top"] or i >= TOP_SLOTS
        return True

    def all_cells():
        """Return every cell as ((kind, index), record) pairs."""
        return [((k, i), c) for k in "aux" for i, c in enumerate(cells[k])]

    def default_cells():
        """Return the starting cells for a fresh install: action cells and window buttons.

        Seeds the first page with bandages and three potions, and the buttons with DEFAULT_UI.
        """
        a = [blank() for _ in range(ACTION_SLOTS)]
        seeds = [(0x0E21, "Bandages", "self"), (0x0F0C, "Heal potion", ""),
                 (0x0F07, "Cure potion", ""), (0x0F0B, "Refresh potion", "")]
        for i, (gr, n, tg) in enumerate(seeds):
            a[TOP_SLOTS + i].update({"t": "item", "g": gr, "n": n, "tg": tg})
        u = [blank() for _ in range(UI_SLOTS)]
        for i, uid in enumerate(DEFAULT_UI[:UI_SLOTS]):
            u[i].update({"t": "ui", "v": uid})
        return a, u

    def cell_text(c):
        """Return the label a cell shows: item name, window name, ability or script file name, or value."""
        t, v = c["t"], c["v"]
        if t == "item":
            return c["n"] or ("0x%04X" % c["g"])
        if t == "ui":
            d = ui_def(v)
            return d[1] if d else v
        if t == "ability":
            return "Secondary" if v == "secondary" else "Primary"
        if t == "script":
            return v.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0]
        return v

    def travel_what(c):
        """Return the tooltip phrase for a travel cell ("Recall to <destination> (<book>)")."""
        return "%s to %s%s" % (TRAVEL_VERB.get(c.get("rm"), "Travel"), c["v"] or "?",
                               (" (%s)" % c["n"]) if c["n"] else "")

    def describe(ref):
        """Return the tooltip text of a cell: what a click does, its key, and a hint to right-click.

        Reads st for the Grimoire and Virtue Assistant states and warns when a spell's reagent is out.
        """
        c = cell(ref)
        t = c["t"]
        if not t:
            if ref[0] in ("a", "x"):
                return "Empty: click to target an item; right-click for a spell, skill or more"
            return "Empty: right-click to choose what it does"
        if t == "travel":
            tip = travel_what(c)
            if HOST.services.get("grimoire.travel") is None:
                tip = "Grimoire is off: turn it on to use this cell\n" + tip
            if c["k"]:
                tip += "  [%s]" % c["k"]
            return tip + "\nRight-click to change"
        name = cell_text(c)
        if t == "ui" and c["v"] == "spellbook":
            name = {"open": "Fold Grimoire into the bar", "minimized": "Show Grimoire",
                    "docked": "Show Grimoire"}.get(st["grim_state"], "Open Grimoire (turns it on)")
        elif t == "ui" and c["v"] == "virtue":
            name = {"open": "Fold Virtue Assistant into the bar", "gear": "Open the Virtue Assistant window",
                    "docked": "Open the Virtue Assistant window"}.get(st["va_state"], "Virtue Assistant (not running)")
        elif t == "ui" and c["v"].startswith("mod:"):
            name = mod_tip(c["v"][4:])
        elif t == "ui":
            name = UI_TIPS.get(c["v"], name)
        tip = {"item": "Use %s", "spell": "Cast %s", "skill": "Use %s", "macro": "Run macro %s",
               "ability": "Use the %s ability", "script": "Start or stop script %s",
               "dress": "Dress %s", "undress": "Undress %s", "say": "Say \"%s\"", "ui": "%s"}.get(t, "%s") % name
        if c["tg"]:
            tip += ", then target %s" % ("yourself" if c["tg"] == "self" else "last target")
        if c["k"]:
            tip += "  [%s]" % c["k"]
        if t == "spell":
            miss = missing_reg(c["v"])
            if miss is not None:
                tip += "\nOut of %s" % miss[1]
        return tip + "\nRight-click to change"

    def _esc(s):
        """Escape the separator characters of a saved value so it survives the var encoding."""
        return (str(s).replace("%", "%25").replace("&", "%26").replace("=", "%3D")
                .replace(";", "%3B").replace("|", "%7C"))

    def _unesc(s):
        """Undo _esc."""
        return (s.replace("%7C", "|").replace("%3B", ";").replace("%3D", "=") .replace("%26", "&").replace("%25", "%"))

    def _enc(d):
        """Encode a dict as key=value pairs joined by "&", values escaped."""
        return "&".join("%s=%s" % (k, _esc(v)) for k, v in d.items())

    def _dec(s):
        """Decode what _enc produced; pairs without "=" are dropped."""
        return dict((k, _unesc(v)) for k, v in (p.split("=", 1) for p in s.split("&") if "=" in p))

    def load_settings():
        """Load the saved settings var into settings, clamping each number to its range.

        Settings are kept in the character var ActionBar_settings (see save_settings). Missing or
        bad entries keep their defaults.
        """
        d = _dec(Kit.get_var(SETTINGS_KEY))
        for k in ("top", "keys", "lock", "short", "hue", "tray_open", "vertical"):
            if k in d:
                settings[k] = d[k] == "1"
        for k, lo, hi in (("slot", SLOT_MIN, SLOT_MAX), ("bagmode", 0, len(BAG_MODES) - 1),
                          ("page", 0, PAGES - 1), ("scale", SCALE_MIN, SCALE_MAX), ("extra", 0, EXTRA_ROWS)):
            with Kit.quiet:
                settings[k] = int(d[k])
            settings[k] = max(lo, min(hi, settings[k]))
        a = d.get("anchor", "")
        settings["anchor"] = a if a in Kit.ANCHORS else ""
        for k in ("bags", "bagkeys"):
            settings[k] = d.get(k, settings[k])

    def save_settings():
        """Save settings to the ActionBar_settings var (booleans as 1 and 0)."""
        Kit.put_var(SETTINGS_KEY, _enc(dict(
            (k, ("1" if v else "0") if isinstance(v, bool) else v) for k, v in settings.items())))

    def _norm(d):
        """Return a clean cell record from a loaded dict, keeping only known keys and numeric fields."""
        c = blank()
        for k in ("t", "v", "tg", "k", "n"):
            c[k] = d.get(k, c[k])
        for k in ("g", "h", "lo"):
            with Kit.quiet:
                c[k] = int(d.get(k, c[k]))
        if c["t"] == "travel":
            for k in TRAVEL_KEYS:
                c[k] = d.get(k, "")
        return c

    def _cells_of(raw, n, skip_empty=True):
        """Return n cell records decoded from a ";"-joined saved string, padded with empty cells.

        With skip_empty the blank entries between separators are dropped first; saved cell lists keep
        them so empty cells stay in place.
        """
        lst = [_norm(_dec(s)) for s in raw.split(";") if s or not skip_empty]
        return (lst + [blank() for _ in range(n)])[:n]

    def load_cells():
        """Load the cells, window buttons, pages and extra rows from their saved vars.

        Starts from the default cells, repairs window buttons whose window no longer exists, and moves
        an untouched old default strip to the current defaults. The bottom row shows the current page.
        """
        # _saved_cells (below) remembers the last text written per var; clear it so the next save writes.
        _saved_cells.clear()
        a, u = default_cells()
        raw = Kit.get_var(CELLS_KEY)
        if "|" in raw:
            ra, ru = raw.split("|", 1)
            a = _cells_of(ra, ACTION_SLOTS, False)
            u = _cells_of(ru, UI_SLOTS, False)
            used = set(c["v"] for c in u if c["t"] == "ui")
            spare = [d for d in DEFAULT_UI if d not in used]
            for c in u:
                if c["t"] == "ui" and ui_def(c["v"]) is None and not c["v"].startswith("mod:"):
                    c.update(blank())
                    if spare:
                        c.update({"t": "ui", "v": spare.pop(0)})
            # An untouched strip from an earlier default layout is moved to the current default strip.
            if [c["v"] if c["t"] == "ui" else None for c in u] == OLD_DEFAULT_UI[:UI_SLOTS]:
                for i, uid in enumerate(DEFAULT_UI[:UI_SLOTS]):
                    u[i].update({"t": "ui", "v": uid})
        pages = [[blank() for _ in range(BOTTOM_SLOTS)] for _ in range(PAGES)]
        rawp = Kit.get_var(PAGES_KEY)
        if rawp:
            for pi, ps in enumerate(rawp.split("|")[:PAGES]):
                pages[pi] = _cells_of(ps, BOTTOM_SLOTS)
        else:
            pages[0] = a[TOP_SLOTS:]
            settings["page"] = 0
        a[TOP_SLOTS:] = pages[settings["page"]]
        cells["x"] = _cells_of(Kit.get_var(EXTRA_KEY), EXTRA_SLOTS)
        cells["a"], cells["u"], cells["pages"] = a, u, pages
        cells_touched()

    def sync_page():
        """Copy the bottom row back into its page, so the current page keeps what was edited."""
        if cells["pages"]:
            cells["pages"][settings["page"]] = list(cells["a"][TOP_SLOTS:])

    # Last text written per saved var, so save_cells skips unchanged vars.
    _saved_cells = {}

    def save_cells():
        """Save cells, pages and extra rows to their vars, writing only the vars whose text changed."""
        sync_page()
        cells_touched()

        def enc(lst):
            """Join the encoded cells of one list with ";"."""
            return ";".join(_enc(c) for c in lst)

        for key, text in ((CELLS_KEY, enc(cells["a"]) + "|" + enc(cells["u"])),
                          (PAGES_KEY, "|".join(enc(pg) for pg in cells["pages"])), (EXTRA_KEY, enc(cells["x"]))):
            if _saved_cells.get(key) != text:
                Kit.put_var(key, text)
                _saved_cells[key] = text

    def set_page(p):
        """Switch the bottom row to page p (wrapping round) and update everything that shows it.

        Saves the old page, re-registers the hotkeys, redraws the bottom cells and closes the cell
        menu if it was open on a bottom cell.
        """
        p = p % PAGES
        if p == settings["page"]:
            return
        sync_page()
        settings["page"] = p
        cells["a"][TOP_SLOTS:] = cells["pages"][p]
        cells_touched()
        save_settings()
        register_hotkeys()
        st["next_count"] = 0.0
        want_redraw([("a", TOP_SLOTS + i) for i in range(BOTTOM_SLOTS)])
        refresh_page_column()
        HOST.refresh_settings(KEY)
        r = menu.get("ref")
        if menu.get("g") is not None and r and r[0] == "a" and r[1] >= TOP_SLOTS:
            close_menu()

    def picked_bags():
        """Return the five picked-bag serials from the settings (0 for an empty slot)."""
        out = [0] * BAG_SLOTS
        for i, p in enumerate(settings["bags"].split(",")[:BAG_SLOTS]):
            try:
                out[i] = int(p, 16) if p.strip() else 0
            except Exception:
                out[i] = 0
        return out

    def set_picked_bag(i, serial):
        """Store a picked bag serial in slot i and save the settings."""
        lst = picked_bags()
        lst[i] = serial
        settings["bags"] = ",".join(("%X" % s) if s else "" for s in lst)
        save_settings()

    def save_pos():
        """Save the bar's position when it moved; skipped while a zone owns the window."""
        # In a zone the host owns the position.
        if Kit.zone_up(KEY):
            return
        p = Kit.pos(win["g"]) if Kit.is_open(win["g"]) else None
        if p is not None and p != st.get("pos_saved"):
            st["pos_saved"] = p
            Kit.put_var(POS_KEY, "%d,%d" % p)

    class ClientUI(object):
        """Reflection bridge to the client's own windows and macros (GameActions, UIManager, Macros).

        All members are static. Calls that touch client objects run on the client thread through
        Client.on_main_ex; the last failure text is kept in ClientUI.error.
        """
        looked = False
        error = ""
        world = None
        GA = None
        UIM = None
        _methods = {}
        _get = staticmethod(Typing._get)

        @staticmethod
        def _method(t, name, ptypes, static):
            """Return the cached reflection method of a type by name, parameter type names and static flag."""
            key = (t, name, tuple(ptypes), static)
            if key not in ClientUI._methods:
                ClientUI._methods[key] = ClientUI._find_method(t, name, ptypes, static)
            return ClientUI._methods[key]

        @staticmethod
        def _find_method(t, name, ptypes, static):
            """Find a non-generic method by name whose first parameters match the given type names.

            A None entry in ptypes matches any type. Parameters left over must be optional. Returns None
            when there is no match.
            """
            # Client.flags gives the binding flags for static or instance members.
            for m in t.GetMethods(Client.flags(static)):
                if m.Name != name or m.IsGenericMethodDefinition:
                    continue
                ps = m.GetParameters()
                if len(ps) < len(ptypes):
                    continue
                if any(want is not None and ps[i].ParameterType.Name != want for i, want in enumerate(ptypes)):
                    continue
                if all(p.IsOptional for p in ps[len(ptypes):]):
                    return m
            return None

        @staticmethod
        def _invoke(m, target, args):
            """Invoke method m on target, filling any missing optional arguments with their defaults."""
            import System
            ps = m.GetParameters()
            full = list(args) + [p.DefaultValue for p in ps[len(args):]]
            return m.Invoke(target, System.Array[object](full))

        @staticmethod
        def find():
            """Look up the client's World, GameActions and UIManager once; set error if they are missing."""
            if ClientUI.looked:
                return
            ClientUI.looked = True
            world = ClientUI.world = safe(lambda: ClientUI._get(API, "World"))
            ClientUI.GA = Client._type("ClassicUO.Game.GameActions")
            ClientUI.UIM = Client._type("ClassicUO.Game.Managers.UIManager")
            if world is None:
                ClientUI.error = "client World not found"
            elif ClientUI.GA is None:
                ClientUI.error = "GameActions not found"

        @staticmethod
        def on_main(fn):
            """Run fn on the client thread and return its result, or None with ClientUI.error set."""
            how, value = Client.on_main_ex(fn)
            if how == "ok":
                return value
            if how == "err":
                ex = Client.exc
                # The real error sits in the inner exception of the IronPython wrapper.
                inner = getattr(ex, "InnerException", None) or \
                    getattr(getattr(ex, "clsException", None), "InnerException", None)
                ClientUI.error = str(inner) if inner else Client.error
            else:
                ClientUI.error = Client.error or "can't run on the client thread"
            return None

        @staticmethod
        def _bring_to_front(type_name):
            """Bring an open gump of the given type name to the front; True when one was found."""
            gumps = (ClientUI._get(None, "Gumps", ClientUI.UIM) if ClientUI.UIM is not None else None)
            node = gumps.First if gumps is not None else None
            while node is not None:
                g = node.Value
                if g is not None and g.GetType().Name == type_name and not g.IsDisposed:
                    m = ClientUI._method(g.GetType(), "BringOnTop", [], False)
                    if m is not None:
                        m.Invoke(g, None)
                    return True
                node = node.Next
            return False

        @staticmethod
        def game_action(name, extra=(), reuse=None):
            """Call a GameActions method on the client thread, or just raise an open window named by reuse.

            extra holds the arguments after World. Returns True when the call was made.
            """
            ClientUI.find()
            if ClientUI.world is None or ClientUI.GA is None:
                return False
            world = ClientUI.world

            def run():
                """Client thread body: front an existing window, else call the GameActions method."""
                if reuse and ClientUI._bring_to_front(reuse):
                    return True
                m = ClientUI._method(ClientUI.GA, name, ["World"] + [None] * len(extra), True)
                if m is None:
                    raise Exception("GameActions.%s not found" % name)
                ClientUI._invoke(m, None, [world] + list(extra))
                return True

            return bool(ClientUI.on_main(run))

        @staticmethod
        def open_macro(sub):
            """Run an Open macro action for the client window named sub; True when it was started."""
            ClientUI.find()
            world = ClientUI.world
            if world is None:
                return False

            def run():
                """Client thread body: build a MacroObject by reflection and run it.

                MacroObject lives in ClassicUO.Game.Managers; its MacroType and MacroSubType enums live in
                ClassicUO.Common.Enums.
                """
                import System
                mgr = ClientUI._get(world, "Macros")
                mo_t, mt_t, ms_t = [mgr.GetType().Assembly.GetType("ClassicUO." + n) for n in (
                    "Game.Managers.MacroObject", "Common.Enums.MacroType", "Common.Enums.MacroSubType")]
                mo = System.Activator.CreateInstance(mo_t, System.Array[object](
                    [System.Enum.Parse(mt_t, "Open", True), System.Enum.Parse(ms_t, sub, True)]))
                ClientUI._run_macro_object(mgr, mo)
                return True

            return bool(ClientUI.on_main(run))

        @staticmethod
        def macro_names():
            """Return the names of the client's TazUO macros, or an empty list."""
            ClientUI.find()
            world = ClientUI.world
            if world is None:
                return []

            def run():
                """Client thread body: read every macro's name."""
                mgr = ClientUI._get(world, "Macros")
                m = ClientUI._method(mgr.GetType(), "GetAllMacros", [], False)
                names = [str(ClientUI._get(mc, "Name") or "") for mc in (m.Invoke(mgr, None) or [])]
                return [n for n in names if n]

            return list(ClientUI.on_main(run) or [])

        @staticmethod
        def _run_macro_object(mgr, mo):
            """Queue the macro object on the client's macro manager and step it once."""
            t = mgr.GetType()
            ClientUI._invoke(ClientUI._method(t, "SetMacroToExecute", ["MacroObject"], False), mgr, [mo])
            ClientUI._invoke(ClientUI._method(t, "Update", [], False), mgr, [])

        @staticmethod
        def run_macro(name):
            """Run the TazUO macro called name.

            Returns True when it started, False when it could not, None when no such macro exists.
            """
            ClientUI.find()
            world = ClientUI.world
            if world is None:
                return False

            def run():
                """Client thread body: find the macro and run its first step."""
                mgr = ClientUI._get(world, "Macros")
                find = ClientUI._method(mgr.GetType(), "FindMacro", ["String"], False)
                macro = find.Invoke(mgr, __import__("System").Array[object]([name]))
                if macro is None:
                    return "missing"
                first = ClientUI._get(macro, "Items")
                if first is None:
                    return "empty"
                ClientUI._run_macro_object(mgr, first)
                return "ok"

            r = ClientUI.on_main(run)
            if r == "missing":
                return None
            return r == "ok"

    def ub_cfg_path():
        """Return the path of this character's Inventory > Bags config file."""
        return Kit.data_path("_unified_bag_%d.cfg" % int(safe(lambda: API.Player.Serial, 0) or 0))

    def unified_bags(path):
        """Read the bag serials the Bags module assigned to its slots, cached by file time.

        Returns a list of serials, or None when the file can't be read.
        """
        try:
            mtime = os.path.getmtime(path)
            cache = st["ub_cache"]
            if cache and cache[0] == path and cache[1] == mtime:
                return list(cache[2])
            with open(path, "r") as f:
                lines = f.read().splitlines()
        except Exception:
            return None
        slots, assign = 0, {}
        for line in lines:
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip()
            with Kit.quiet:
                if k == "slots":
                    slots = int(v)
                elif k.startswith("slot."):
                    assign[int(k[5:])] = int(v)
        lst = [assign[i] for i in sorted(assign) if (slots <= 0 or i < slots) and assign[i] > 0]
        st["ub_cache"] = (path, mtime, lst)
        return list(lst)

    def ub_bags():
        """Return the Bags module's bag serials, or None when unknown.

        On the client thread the file read is queued as a job so the draw is never held up; the last
        answer is returned meanwhile.
        """
        # The script thread may read files; the client thread must not wait on disk.
        if not Client.on_client_thread():
            st["ub_last"], st["ub_pending"] = unified_bags(ub_cfg_path()), False
        elif not st["ub_job"]:
            st["ub_job"] = True
            path = ub_cfg_path()

            def job():
                """Read the Bags config and ask for a bag rescan when the answer changed."""
                st["ub_job"] = False
                res = unified_bags(path)
                if res != st["ub_last"] or st["ub_pending"]:
                    st["ub_last"], st["ub_pending"] = res, False
                    st["next_scan"] = 0.0

            later(job)
        return None if st["ub_last"] is None else list(st["ub_last"])

    def link_state(var, allowed):
        """Read a shared var and return it only when it is one of the allowed state words."""
        s = API.GetSharedVar(var)
        return str(s) if s is not None and str(s) in allowed else None

    def ub_state():
        """Return the Bags window state: open, collapsed or docked, else None."""
        return link_state("UnifiedBag_state", ("open", "collapsed", "docked"))

    def grim_state():
        """Return the Grimoire window state: open, minimized or docked, else None."""
        return link_state("Grimoire_state", ("open", "minimized", "docked"))

    def va_state():
        """Return the Virtue Assistant window state: open, gear or docked, else None."""
        return link_state("VirtueAssistant_state", ("open", "gear", "docked"))

    def ub_send(cmd):
        """Send a command to the Bags module through its shared var."""
        API.SetSharedVar("UnifiedBag_cmd", cmd)

    def all_docks():
        """Return the host's registered window docks."""
        return list(HOST.docks)

    def tray_docks():
        """Return the docks that belong in the tray: always-shown ones and those folded in."""
        return [(k, d) for k, d in all_docks() if d.get("always") or safe(d.get("state")) == "docked"]

    def dock_sig():
        """Return a signature of every dock's state, to notice a change cheaply."""
        return tuple([(k, safe(d.get("state"))) for k, d in all_docks()])

    def tray_sig():
        """Return a signature of what the tray shows, to redraw it only when that changes."""
        return tuple([(k, d.get("icon"), safe(d.get("state")) if d.get("always") else None) for k, d in tray_docks()])

    def heartbeat(on=True):
        """Publish or withdraw this bar's alive stamp for the Bags module.

        The other windows read it to know whether to fold into this bar.
        """
        if on and not st["em"]:
            # Re-stamped every call; the stamp's age tells the others this bar is running.
            API.SetSharedVar(UB_LINK_ALIVE, time.time())
        else:
            API.RemoveSharedVar(UB_LINK_ALIVE)

    def watch_ub():
        """Poll the other windows' states a few times a second and update what shows them.

        Refreshes tooltips and the tray when a window state changes, redraws module buttons when a
        module appears or goes, re-registers hotkeys when another module takes or frees a key this bar
        uses, and reports a window that did not start in time. Main loop.
        """
        now = time.time()
        if now < st["watch_next"]:
            return
        # Other windows are polled only four times a second.
        st["watch_next"] = now + 0.25
        tips = False
        for k, s, tip in (("ub_state", ub_state(), settings["bagmode"] == 0),
                          ("grim_state", grim_state(), True), ("va_state", va_state(), True)):
            if s != st[k]:
                st[k] = s
                tips = tips or tip
        if tips:
            refresh_tips()
        sig = dock_sig()
        if sig != st["dock_sig"]:
            old_keys = set(k for k, _ in (st["dock_sig"] or ()))
            st["dock_sig"] = sig
            tsig = tray_sig()
            if tsig != st.get("tray_sig"):
                st["tray_sig"] = tsig
                refresh_tray()
            refs = [ref for ref, c in all_cells() if c["t"] == "ui" and c["v"].startswith("mod:")]
            if refs:
                if set(k for k, _ in sig) != old_keys:
                    want_redraw(refs)
                else:
                    refresh_tips()
        owned = frozenset(HOST.hotkeys_owned)
        if owned != st.get("owned_sig"):
            changed = owned ^ (st.get("owned_sig") or frozenset())
            st["owned_sig"] = owned
            # Only a change to a key this bar uses needs the hotkeys registered again.
            if changed & bar_keys():
                register_hotkeys()
        p = st["pending_on"]
        if p and time.time() > p[2]:
            st["pending_on"] = None
            state = ub_state() if p[0] == UB_MODULE_KEY else grim_state()
            if state is None:
                say("%s didn't start; is Virtue Assistant running?" % p[1], Kit.HUE_BAD)
                if p[3] is not None:
                    p[3]()

    def turn_on(key, title, fallback=None):
        """Turn a module on by key and wait a few seconds for its window state to show.

        fallback runs if it did not start. Uses the host when it knows the module, else asks the
        mother script through a shared var.
        """
        if key in HOST.by_key:
            later(lambda: HOST.enable(key))
        else:
            API.SetSharedVar("VirtueAssistant_enable", key)
        say("turning %s on." % title)
        st["pending_on"] = (key, title, time.time() + 4.0, fallback)

    def toggle_grimoire():
        """Button action of Grimoire: turn it on, show it or fold it into the bar. Returns True."""
        state = grim_state()
        heartbeat()
        if state in ("minimized", "docked", "open"):
            API.SetSharedVar(GRIM_LINK_CMD, "dock" if state == "open" else "show")
        else:
            turn_on(GRIM_MODULE_KEY, "Grimoire", open_spellbook)
        return True

    def toggle_va():
        """Button action of Virtue Assistant: show its window or fold it into the bar.

        Returns False when Virtue Assistant is not running.
        """
        state = va_state()
        heartbeat()
        if state not in ("open", "gear", "docked"):
            say("Virtue Assistant isn't running.", Kit.HUE_BAD)
            return False
        API.SetSharedVar(VA_LINK_CMD, "dock" if state == "open" else "show")
        return True

    def auto_bags():
        """Return the backpack and its first sub-bags (up to the slot count) as the bag list."""
        out = []
        bp = int(API.Backpack or 0)
        if bp:
            out.append(bp)
        for it in (API.ItemsInContainer(bp, False) or []):
            if len(out) >= BAG_SLOTS:
                break
            with Kit.quiet:
                if it.IsContainer:
                    out.append(int(it.Serial))
        return out

    def scan_bags():
        """Work out the five bag slots by the bag mode and redraw them when the bags changed.

        Mode 0 follows the Bags module's slots (falling back to the pack when there is no Bags
        config), mode 1 uses the bags the player picked, mode 2 the pack and its sub-bags.
        """
        mode = settings["bagmode"]
        if mode == 0:
            serials = ub_bags()
            if serials is None and st["ub_pending"]:
                serials = []
            else:
                st["ub_found"] = serials is not None
                if serials is None:
                    serials = auto_bags()
        elif mode == 1:
            serials = picked_bags()
        else:
            serials = auto_bags()
        bags, found = [], []
        for s in (list(serials) + [0] * BAG_SLOTS)[:BAG_SLOTS]:
            if not s:
                bags.append(None)
                found.append(None)
                continue
            it = Kit.find_item(s)
            found.append(it)
            if it is None:
                bags.append({"s": s, "g": 0, "h": 0, "n": "Bag (not loaded yet)"})
                continue
            try:
                gr, hu = int(it.Graphic or 0), int(it.Hue or 0)
            except Exception:
                gr = hu = 0
            bags.append({"s": s, "g": gr, "h": hu, "n": None})
        sig = tuple((b["s"], b["g"], b["h"]) if b else None for b in bags)
        if sig != st["bag_sig"]:
            for b, it in zip(bags, found):
                if b is not None and b["n"] is None:
                    try:
                        b["n"] = str(it.Name or "") or "Bag"
                    except Exception:
                        b["n"] = "Bag"
            st["bags"], st["bag_sig"] = bags, sig
            want_redraw([("b", i) for i in range(BAG_SLOTS)])

    def bag_at(i):
        """Return the bag record shown in slot i, or None."""
        return st["bags"][i] if i < len(st["bags"]) else None

    # Cached cell summary; set to None to rebuild.
    _kinds = {"types": None}

    def cells_touched():
        """Forget the cached cell kinds; call whenever the cells change."""
        _kinds["types"] = None

    def _cell_kinds():
        """Return the cached summary of the cells: types used, item graphics, spell reagents, refs.

        Lets the counting and cooldown code skip work for kinds the bar does not hold.
        """
        if _kinds["types"] is None:
            every = cells["a"] + cells["u"] + cells["x"]
            _kinds["types"] = set(c["t"] for c in every)
            _kinds["items"] = set(c["g"] for c in every if c["t"] == "item")
            regs, extra = set(), set()
            refs = {"skill": [], "spell": []}
            for ref, c in all_cells():
                if c["t"] == "spell":
                    regs.update(r[1] for r in spell_reg_list(c["v"]))
                    refs["spell"].append(ref)
                elif c["t"] == "skill":
                    refs["skill"].append(ref)
                elif c["t"] == "travel" and c.get("rm") in TRAVEL_SCROLL:
                    extra.add(TRAVEL_SCROLL[c["rm"]])
            _kinds["extra"], _kinds["refs"] = frozenset(regs | extra), refs
        return _kinds

    def scan_abilities():
        """Redraw the ability cells when the player's current abilities change."""
        if "ability" not in _cell_kinds()["types"]:
            return
        sig = tuple([str(n) for n in (API.CurrentAbilityNames() or [])])
        if sig != st["ability_sig"]:
            st["ability_sig"] = sig
            want_redraw([r for r, c in all_cells() if c["t"] == "ability"])

    def count_now(extra=(), max_age=0.0):
        """Count the bar's items in the pack and store the totals and first serials in st.

        extra adds graphics to count; max_age lets a recent host pack snapshot be reused. Items in the
        top-level pack win over those in sub-bags when a serial is chosen to use.
        """
        ver = HOST.pack_ver()
        try:
            items = HOST.pack_items(deep=True, max_age=max_age)
            bp = int(API.Backpack or 0)
        except Exception:
            return
        k = _cell_kinds()
        wanted = k["items"]
        if extra or k["extra"]:
            wanted = wanted | k["extra"] | set(extra)
        cnt, cnt_g, first, first_g, top, top_g = {}, {}, {}, {}, {}, {}
        # Local aliases of the dict getters: this loop runs over every pack item.
        cget, gget = cnt.get, cnt_g.get
        for it in items:
            try:
                gr = int(it.Graphic)
                if gr not in wanted:
                    continue
                hu, ser = int(it.Hue), int(it.Serial)
                amt = max(1, int(it.Amount or 0))
                # Items straight in the pack are preferred to those in sub-bags when picking the one to use.
                f, fg = (top, top_g) if int(it.Container) == bp else (first, first_g)
            except Exception:
                continue
            key = (gr, hu)
            cnt[key] = cget(key, 0) + amt
            cnt_g[gr] = gget(gr, 0) + amt
            f.setdefault(key, ser)
            fg.setdefault(gr, ser)
        first.update(top)
        first_g.update(top_g)
        st.update({"cnt": cnt, "cnt_g": cnt_g, "first": first, "first_g": first_g, "counted": wanted,
                   "counted_at": time.time(), "pack_v": ver})

    def _place(info, lbl, text, hue):
        """Set a counter label's text and hue, moving it to the bottom right only when the text changed."""
        if info.get("txt") != text:
            info["txt"] = text
            try:
                lbl.Text = text
                Kit.ui_pos(lbl, info["x"] + info["w"] - Kit.text_px(text) - 3, info["y"] + info["h"] - 16)
            except Exception:
                pass
        if info.get("hue") != hue:
            info["hue"] = hue
            Kit.set(lbl, "Hue", hue)

    def refresh_counts():
        """Recount the pack when item or scroll counters are shown, then update every label."""
        if st["em"]:
            return
        k = _cell_kinds()
        if "item" in k["types"] or k["extra"]:
            count_now(max_age=0.5)
        else:
            st["pack_v"] = None
        update_labels()

    # Cached list of (ref, info, label) for the cells that show a counter.
    _counters = [None]

    def update_labels():
        """Update every counter label: counts, red-at colour, cooldown time, ON marks and spell grey-out."""
        now = time.time()
        cool = st["cool"]
        charges = False
        # Built once, then reused until the cells are redrawn.
        lst = _counters[0]
        if lst is None:
            lst = [(ref, info, info["count"]) for ref, info in win["cells"].items() if info.get("count") is not None]
            _counters[0] = lst
        for ref, info, lbl in lst:
            c = cell(ref)
            t, v = c["t"], c["v"]
            text, hue = "", Kit.HUE_TEXT
            end = cool.get(t)
            if end and now < end:
                text, hue = cool_text(end - now), Kit.HUE_TITLE
            elif t == "item":
                n = st["cnt"].get((c["g"], c["h"]), 0) if settings["hue"] else st["cnt_g"].get(c["g"], 0)
                text = fmt_count(n)
                hue = Kit.HUE_BAD if n <= max(0, c["lo"]) else Kit.HUE_TEXT
            elif t in ("spell", "ability", "script"):
                try:
                    if t == "spell":
                        on = bool(API.IsSpellActive(v))
                    elif t == "ability":
                        on = bool(API.SecondaryAbilityActive() if v == "secondary" else API.PrimaryAbilityActive())
                    else:
                        on = script_running(v)
                except Exception:
                    on = False
                text, hue = ("ON" if on else ""), Kit.HUE_GOOD
            elif t == "travel":
                if charges is False:
                    charges = travel_charges()
                text, hue = travel_count(c, charges)
            if t == "spell":
                miss = missing_reg(v)
                grey_cell(ref, info, miss is not None)
                if miss is not None and not (end and now < end):
                    text, hue = miss[0], Kit.HUE_BAD
            _place(info, lbl, text, hue)
        for i, info in list(win["bags"].items()):
            lbl = info.get("count")
            b = bag_at(i)
            if lbl is None or not b:
                continue
            try:
                n = int(API.Contents(b["s"]) or 0)
            except Exception:
                n = 0
            _place(info, lbl, str(n), Kit.HUE_TEXT)

    _regs = {}

    def spell_reg_list(name):
        """Return the reagents a spell needs as (reagent, graphic, name) tuples, cached by spell name."""
        hit = _regs.get(name)
        if hit is None:
            info = Kit.spell_info(name)
            table = Kit.REAGENTS
            hit = tuple((a, table[a][1], table[a][0]) for a in (info[1] if info else ()) if a in table)
            if len(_regs) > 200:
                _regs.clear()
            _regs[name] = hit
        return hit

    def missing_reg(name):
        """Return (reagent, name) of the first reagent of a spell that is at 0 in the pack, or None.

        Only reagents the last count looked at can be missing, so an uncounted reagent never greys a cell.
        """
        cnt, counted = st["cnt_g"], st.get("counted") or ()
        for a, g, n in spell_reg_list(name):
            if cnt.get(g, 0) <= 0 and g in counted:
                return (a, n)
        return None

    def grey_cell(ref, info, grey):
        """Grey a spell cell's icon (and refresh its tooltip) when a reagent is out; only on a change."""
        if info.get("grey", False) == grey:
            return
        info["grey"] = grey
        icon = info.get("icon")
        if icon is not None:
            icon.SetAlpha(0.35 if grey else 1.0)
        set_tip(info, describe(ref))

    def travel_charges():
        """Return {runebook serial: charges} from Grimoire's services, or None when Grimoire is off."""
        fn = HOST.services.get("grimoire.book_charges")
        if fn is not None:
            return safe(fn)
        fn = HOST.services.get("grimoire.destinations")
        if fn is None:
            return None
        try:
            return dict((d["book"], d["charges"]) for d in fn() or ())
        except Exception:
            return None

    def travel_count(c, charges):
        """Return the (text, hue) a travel cell's counter shows.

        charges is the dict from travel_charges. Scroll methods show the scrolls in the pack (red at or
        below the cell's red-at value), a charge shows the book's charges, other methods show the
        charges in the info colour.
        """
        if charges is None:
            return "off", Kit.HUE_INFO
        m = c.get("rm")
        lo = max(0, c["lo"])
        if m in TRAVEL_SCROLL:
            n = st["cnt_g"].get(TRAVEL_SCROLL[m], 0)
            return fmt_count(n), Kit.HUE_BAD if n <= lo else Kit.HUE_TEXT
        try:
            n = charges.get(int(c.get("rb") or "0", 16))
        except ValueError:
            n = None
        if n is None:
            return "", Kit.HUE_TEXT
        if m == "charge":
            return str(n), Kit.HUE_BAD if n <= lo else Kit.HUE_TEXT
        return str(n), Kit.HUE_INFO

    def fire_travel(c):
        """Send a travel cell's destination to Grimoire's travel service. Returns True when it went.

        Says why when Grimoire is off or the cell has no destination.
        """
        fn = HOST.services.get("grimoire.travel")
        if fn is None:
            say("Grimoire is off; turn it on to use Travel cells.", Kit.HUE_BAD)
            return False
        try:
            book, idx = int(c.get("rb") or "", 16), int(c.get("ri") or "")
        except ValueError:
            say("this Travel cell has no destination; right-click it to pick one.", Kit.HUE_BAD)
            return False
        return bool(fn(book, idx, c.get("rm") or "recall", c["v"] or None))

    def set_travel(ref, d, method):
        """Set a cell to a travel destination picked from Grimoire's list (d) and a travel method.

        Keeps the cell's hotkey and red-at value, then saves and redraws that one cell.
        """
        cur = cell(ref)
        new = dict(blank(), t="travel", v=str(d["name"]), n=str(d["book_name"]), k=cur["k"], tg="",
                   lo=cur["lo"] if cur["t"] == "travel" else 2, rb="%X" % int(d["book"]), ri=str(int(d["index"])),
                   rm=method)
        cells[ref[0]][ref[1]] = new
        cells_changed(recount=True, refs=[ref])
        say("%s set on %s." % (travel_what(new), ref_name(ref)), Kit.HUE_GOOD)

    # Seconds of delay after a skill with a long fixed delay; others use ten.
    _skill_delay = {"arms lore": 3.0, "item identification": 3.0, "detect hidden": 3.0}

    def cool_text(rem):
        """Return the cooldown text: whole seconds from 3 up, tenths below."""
        return ("%d" % int(math.ceil(rem))) if rem >= 3.0 else ("%.1f" % max(0.0, rem))

    def start_cool(t, v):
        """Start the darkening countdown of a skill or spell kind after the player uses one.

        Skills use a fixed delay (most 10 seconds), spells use the spell's cast delay from Kit.
        """
        if t == "skill":
            secs = _skill_delay.get(str(v).strip().lower(), 10.0)
        else:
            info = Kit.spell_info(v)
            secs = info[3] if info else 0.0
        if secs and secs > 0:
            st["cool"][t] = time.time() + secs
            st["cool_next"] = 0.0

    def cool_tick(now):
        """Advance the skill and spell cooldown displays: darken the cells of that kind and count down.

        Runs every tick but does work only every tenth of a second while a cooldown is active.
        """
        cool = st["cool"]
        if not (cool["skill"] or cool["spell"]) or now < st["cool_next"]:
            return
        st["cool_next"] = now + 0.1
        refs = _cell_kinds()["refs"]
        ended = False
        for kind in ("skill", "spell"):
            end = cool[kind]
            if not end:
                continue
            done = now >= end
            if done:
                cool[kind] = 0.0
                ended = True
            text = "" if done else cool_text(end - now)
            for ref in refs[kind]:
                info = win["cells"].get(ref)
                if info is None:
                    continue
                dark = not done
                if info.get("dark", False) != dark:
                    info["dark"] = dark
                    info["catcher"].SetAlpha(0.55 if dark else 0.01)
                lbl = info.get("count")
                if lbl is not None and not done:
                    _place(info, lbl, text, Kit.HUE_TITLE)
        if ended:
            update_labels()

    def short_what(ref):
        """Return the first line of a cell's tooltip without its key, for the hotkey list."""
        c = cell(ref)
        if c["t"] == "travel":
            return travel_what(c)
        tip = describe(ref).split("\n")[0]
        return tip.replace("  [%s]" % c["k"], "") if c["k"] else tip

    def hotkeys_service():
        """Return the (key, description) pairs this module offers the host's hotkey list.

        Notes keys another module already owns as "left to" that module.
        """
        out = [(_norm_key(c["k"]), "%s: %s" % (ref_name(r), short_what(r))) for r, c in all_cells()
               if _norm_key(c["k"]) and c["t"] and shown(r)]
        out += [(k, "bag slot %d" % (i + 1)) for i, k in enumerate(bag_keys()) if k]
        return [(k, what + ((" (left to %s)" % key_owner(k)) if key_owner(k) else "")) for k, what in out]

    on_disposed = Kit.disposer(KEY, st, win)

    def want_rebuild(delay=0.0):
        """Ask the main loop to rebuild the whole bar after delay seconds."""
        st["rebuild_at"] = time.time() + delay

    def cells_changed(recount=False, refresh=True, refs=None):
        """Save and re-register after the cells changed, and redraw all of the bar or just refs.

        recount forces a fresh item count; refresh also refreshes the settings page.
        """
        save_cells()
        register_hotkeys()
        if recount:
            st["next_count"] = 0.0
        if refs is None:
            want_rebuild()
        else:
            want_redraw(refs)
        if refresh:
            HOST.refresh_settings(KEY)

    def clear_cell(ref):
        """Empty one cell and redraw it."""
        cells[ref[0]][ref[1]] = blank()
        cells_changed(refs=[ref])

    # Zone fit: scale and shape told by the zone, slot, offset and signature of the settings used.
    fitst = {"scale": None, "vertical": None, "slot": None, "off": (0, 0), "sig": None}

    def eff_scale():
        """Return the scale in use: the zone fit if there is one, else the saved percentage."""
        v = fitst["scale"]
        return int(settings["scale"]) if v is None else v

    def eff_vertical():
        """Return whether the bar stands upright: the zone's shape if there is one, else the setting."""
        v = fitst["vertical"]
        return bool(settings["vertical"]) if v is None else v

    def told_slot():
        """Return the zone slot size (w, h) the bar was told to fill, or None when not fitted."""
        return fitst["slot"] if fitst["scale"] is not None else None

    def fit_sig():
        """Return the settings that change the bar's size, to notice when a fit has gone stale."""
        return (settings["slot"], settings["top"], settings["extra"])

    def _fit_scale(along, across):
        """Return the largest scale percent whose bar fits along x across.

        Starts from a proportional guess, then steps by one percent (at most eight steps each way)
        using the real geometry. The scale in use is restored afterwards.
        """
        keep = fitst["scale"]
        try:
            fitst["scale"] = 100
            G1 = _geom_base()
            pct = max(SCALE_MIN, min(SCALE_MAX, int(min(along * 100.0 / max(1.0, G1["W"]),
                                                        across * 100.0 / max(1.0, G1["H"])))))

            def fits(p):
                """Test whether the bar at percent p fits the space."""
                fitst["scale"] = p
                G2 = _geom_base()
                return G2["W"] <= along and G2["H"] <= across

            for _ in range(8):
                if pct <= SCALE_MIN or fits(pct):
                    break
                pct -= 1
            for _ in range(8):
                if pct >= SCALE_MAX or not fits(pct + 1):
                    break
                pct += 1
            return pct
        finally:
            fitst["scale"] = keep

    def tell_need():
        """Tell the host how much space the bar needs, for the zone layout.

        With extra rows the need is measured with them off, so the host sizes the zone for a single
        row of the fitted scale.
        """
        base = HOST.layout_base(KEY)
        if not settings["extra"] or base is None:
            HOST.layout_need(KEY)
            return
        vert = base[1] > base[0]
        along, across = (base[1], base[0]) if vert else base
        keep, kept_scale, vt = settings["extra"], fitst["scale"], _ctrl.get("vtmp")
        _ctrl["vtmp"] = vert
        try:
            settings["extra"] = 0
            p = _fit_scale(int(along), int(across))
            settings["extra"] = keep
            fitst["scale"] = p
            need = _geom_base()["H"]
        finally:
            settings["extra"] = keep
            fitst["scale"] = kept_scale
            _ctrl["vtmp"] = vt
        HOST.layout_need(KEY, need if vert else None, None if vert else need)

    def layout_fit(w, h, mode):
        """Host hook: fit the bar to a zone slot of w x h (None to leave the zone).

        Works out the scale and orientation, and rebuilds the bar when they changed.
        """
        if w is None or h is None or not w or not h:
            new = (None, None)
            slot = sig = None
        else:
            slot = (int(w), int(h))
            vert = h > w
            along, across = (h, w) if vert else (w, h)
            sig = fit_sig()
            tell_need()
            _ctrl["vtmp"] = vert
            try:
                new = (_fit_scale(int(along), int(across)), vert)
            finally:
                _ctrl["vtmp"] = None
        was = (eff_scale(), eff_vertical(), fitst["slot"])
        fitst["scale"], fitst["vertical"] = new
        fitst["slot"], fitst["sig"] = slot, sig
        if (eff_scale(), eff_vertical(), fitst["slot"]) != was and not st["shutting"]:
            want_rebuild()

    def refit_if_stale():
        """Fit again when a setting that changes the bar's size changed since the last fit."""
        slot = told_slot()
        sig = fit_sig()
        if slot is None or sig == fitst["sig"]:
            return
        along, across = (slot[1], slot[0]) if fitst["vertical"] else slot
        fitst["scale"] = _fit_scale(along, across)
        fitst["sig"] = sig
        tell_need()

    def layout_state():
        """Host hook: report "open", "minimized" or None for the zone manager."""
        if win["g"] is None or st["shutting"]:
            return None
        return "minimized" if st["em"] else "open"

    def layout_min():
        """Host hook: return the smallest (w, h) the bar can be drawn at, in either orientation."""
        keep, vt = fitst["scale"], _ctrl["vtmp"]
        out = []
        try:
            fitst["scale"] = SCALE_MIN
            for v in (False, True):
                _ctrl["vtmp"] = v
                G1 = _geom_base()
                out.append((G1["H"], G1["W"]) if v else (G1["W"], G1["H"]))
        finally:
            fitst["scale"], _ctrl["vtmp"] = keep, vt
        return min(out[0][0], out[1][0]), min(out[0][1], out[1][1])

    # Hooks the host's zone manager calls for this window.
    LAYOUT_HOOKS = {"fit": layout_fit, "state": layout_state, "min": layout_min, "exact": True, "untitled": True}

    def sc(v, lo=1):
        """Scale a design size by the effective scale, never below lo."""
        k = max(SCALE_MIN, min(SCALE_MAX, eff_scale())) / 100.0
        return max(lo, int(round(v * k)))

    # Cached layout and the inputs it was built from.
    _geom = {"key": None, "L": None}

    def geom():
        """Return the bar's layout dict, rebuilt only when its inputs change.

        Stretches the base layout to fill the zone slot when there is one.
        """
        slot = told_slot()
        key = (settings["slot"], eff_scale(), settings["top"], settings["extra"], slot, eff_vertical())
        if _geom["key"] != key:
            if slot is None:
                _geom["L"] = _geom_base()
            else:
                along, across = (slot[1], slot[0]) if eff_vertical() else slot
                _geom["L"] = _stretch(_geom_base(), along, across)
            _geom["key"] = key
        return _geom["L"]

    # Cached control width and a temporary orientation used while measuring.
    _ctrl = {"capw": None, "vtmp": None}

    def ctrl_capw():
        """Return the width of the widest control caption plus padding, measured once."""
        if _ctrl["capw"] is None:
            _ctrl["capw"] = max(Kit.text_w(c) for c in ("Keys", "Lock", "Grid")) + 6
        return _ctrl["capw"]

    def ctrl_orders(vert):
        """Return the column counts to try for the four controls, widest first when upright."""
        return (4, 2, 1) if vert else (1, 2, 4)

    def ctrl_cells(c, dw, dh):
        """Return (rows, cell width, cell height) of the controls laid out in c columns in a w x h box."""
        rows = (4 + c - 1) // c
        cell_w = (dw - 2 * CTRL_PAD - (c - 1) * CTRL_PAD) // c
        cell_h = min(24, (dh - 2 * CTRL_PAD - (rows - 1) * CTRL_PAD) // rows)
        return rows, cell_w, cell_h

    def ctrl_need(col_h, vert):
        """Return the control column's length needed for col_h of free space, by the best column count."""
        capw = ctrl_capw()
        for c in ctrl_orders(vert):
            rows = (4 + c - 1) // c
            across = rows * CTRL_ROW_MIN + (rows - 1) * CTRL_PAD + 2 * CTRL_PAD
            along = c * capw + (c - 1) * CTRL_PAD + 2 * CTRL_PAD
            if vert and along <= col_h:
                return across
            if not vert and across <= col_h:
                return along
        return (4 * CTRL_ROW_MIN + 5 * CTRL_PAD) if vert else (4 * capw + 5 * CTRL_PAD)

    def _geom_base():
        """Return the unstretched layout dict (sizes, positions and totals) at the effective scale.

        Keys include S slot size, pitch, per-row and per-column positions, the widths of the window
        button and bag panels, and W and H, the bar's overall size when drawn flat.
        """
        S = sc(max(SLOT_MIN, min(SLOT_MAX, int(settings["slot"]))), 18)
        bm, sg, p4 = sc(BAR_M, 4), sc(6, 3), sc(4, 2)
        m = bm
        gap, ug, bg = sc(4, 2), sc(UI_GAP, 2), sc(BAG_GAP, 2)
        pw, cw, tb = sc(PAGE_W, 16), sc(CTRL_W, 34), sc(TRAY_BTN, 18)
        pitch = S + gap
        ph = S + 2 * p4
        inner = pw + TOP_SLOTS * pitch + p4
        left_w = BOTTOM_SLOTS * pitch + p4
        tray_w = tb + 2 * p4
        rest = inner - pw - left_w - 2 * sg - tray_w - sg
        ui_w = int(rest * UI_SHARE)
        bag_w = rest - ui_w
        bw = (ui_w - 2 * p4 - (UI_SLOTS - 1) * ug) // UI_SLOTS
        bgw = (bag_w - 2 * p4 - (BAG_SLOTS - 1) * bg) // BAG_SLOTS
        rows = (2 if settings["top"] else 1) + settings["extra"]
        # The controls column never gets smaller than its widest control needs.
        cw = max(cw, ctrl_need(rows * ph + (rows - 1) * sg, eff_vertical() if _ctrl["vtmp"] is None else _ctrl["vtmp"]))
        return {"S": S, "pitch": pitch, "ph": ph, "inner": inner, "left_w": left_w, "rows": rows,
                "ui_w": ui_w, "bag_w": bag_w, "bw": bw, "bh": ph - 3 * p4, "tray_w": tray_w, "tb": tb,
                "bgw": bgw, "bgh": ph - 2 * p4, "m": m, "sg": sg, "p4": p4, "ug": ug, "bg": bg, "pw": pw, "cw": cw,
                "tm": bm, "colx": tuple(p4 + i * pitch for i in range(TOP_SLOTS)),
                "colw": (S,) * TOP_SLOTS, "top_w": TOP_SLOTS * pitch + p4, "sgx": sg, "sgc": sg,
                "rowy": tuple(r * (ph + sg) for r in range(rows)), "rowh": (ph,) * rows,
                "celly": (p4,) * rows, "cellh": (S,) * rows, "W": m + inner + sg + cw + m,
                "H": m + rows * ph + (rows - 1) * sg + m}

    def _share(total, n):
        """Split total into n whole parts that differ by at most one and add up exactly."""
        if n <= 0:
            return []
        if total <= 0:
            return [0] * n
        return [(total * (i + 1)) // n - (total * i) // n for i in range(n)]

    def _stretch(L, along, across):
        """Stretch a layout to fill a slot of along x across.

        Spare length first widens the gaps, then the cells (up to 1.6 times as deep as wide), then the
        window button and bag panels take the rest; spare height goes the same way between rows.
        """
        L = dict(L)
        S, p4, sg, rows = L["S"], L["p4"], L["sg"], L["rows"]
        gap = L["pitch"] - S
        n = TOP_SLOTS
        # A cell may grow to 1.6 times as deep as the base slot when a zone is taller.
        deep = max(0, int(S * 1.6) - S)
        spare = along - L["W"]
        if spare > 0:
            cap1 = n * gap + sg
            s1 = min(spare, cap1)
            t = float(s1) / cap1 if cap1 > 0 else 0.0
            dc = min(s1, int(round(sg * t)))
            gaps = [gap + d for d in _share(s1 - dc, n)]
            s2 = min(spare - s1, n * deep)
            colw = [S + d for d in _share(s2, n)]
            s3 = spare - s1 - s2
            tail = 0
            if s3 > 0:
                if rows > 1:
                    gaps = [a + d for a, d in zip(gaps, _share(s3, n))]
                else:
                    tail = s3
            colx, x = [], p4
            for i in range(n):
                colx.append(x)
                x += colw[i] + gaps[i]
            sgx = sg + int(round(sg * t))
            ug = L["ug"] + int(round(L["ug"] * t))
            bg = L["bg"] + int(round(L["bg"] * t))
            pw, tray_w = L["pw"], L["tray_w"]
            inner = pw + x + tail
            left_w = colx[BOTTOM_SLOTS]
            rest = inner - pw - left_w - 3 * sgx - tray_w
            ui_w = int(rest * UI_SHARE)
            bag_w = rest - ui_w
            L.update({"colx": tuple(colx), "colw": tuple(colw), "top_w": x,
                      "sgx": sgx, "sgc": sg + dc, "ug": ug, "bg": bg,
                      "inner": inner, "left_w": left_w, "ui_w": ui_w, "bag_w": bag_w,
                      "bw": (ui_w - 2 * p4 - (UI_SLOTS - 1) * ug) // UI_SLOTS,
                      "bgw": (bag_w - 2 * p4 - (BAG_SLOTS - 1) * bg) // BAG_SLOTS})
            L["W"] = L["m"] + inner + L["sgc"] + L["cw"] + L["m"]
        spare = across - L["H"]
        if spare > 0:
            s1 = min(spare, (rows - 1) * sg)
            rgap = [sg + d for d in _share(s1, rows - 1)]
            s2 = min(spare - s1, rows * deep)
            cellh = [S + d for d in _share(s2, rows)]
            pad = _share(spare - s1 - s2, rows)
            rowy, rowh, celly, y = [], [], [], 0
            for r in range(rows):
                rowy.append(y)
                rh = cellh[r] + 2 * p4 + pad[r]
                rowh.append(rh)
                celly.append(p4 + pad[r] // 2)
                y += rh + (rgap[r] if r < rows - 1 else 0)
            L.update({"rowy": tuple(rowy), "rowh": tuple(rowh), "celly": tuple(celly),
                      "cellh": tuple(cellh), "bh": cellh[-1] - p4, "bgh": cellh[-1]})
            L["H"] = L["m"] + y + L["m"]
        return L

    def flat():
        """Return whether the bar is drawn flat (not upright)."""
        return not eff_vertical()

    def bar_size():
        """Return the bar's (width, height) on screen, swapped when upright."""
        if st["em"]:
            return MINI_W, MINI_H
        L = geom()
        return (L["W"], L["H"]) if flat() else (L["H"], L["W"])

    def R(x, y, w, h):
        """Return an (x, y, w, h) box in flat layout terms as the screen box, swapped when upright."""
        ox, oy = fitst["off"]
        return (x + ox, y + oy, w, h) if flat() else (y + ox, x + oy, h, w)

    def add_item_pic(g, graphic, hue, x, y, w, h):
        """Add an item picture of a graphic and hue at x, y that ignores the mouse; None on failure."""
        try:
            p = G.CreateGumpItemPic(int(graphic), int(w), int(h))
        except Exception:
            return None
        if hue:
            p.Hue = max(0, min(0xFFFF, int(hue)))
        p.SetPos(x, y)
        p.SetAcceptMouseInput(False)
        g.Add(p)
        return p

    def caption_words(text):
        """Put spaces between the words of a camel-case name ("OpenSkills" as "Open Skills")."""
        t = str(text).replace("_", " ")
        return "".join(" " + ch if i and ch.isupper() and t[i - 1].islower() else ch for i, ch in enumerate(t))

    def add_cell_text(g, text, x, y, w, h, hue=None):
        """Add up to three centred lines of caption text in a cell; return the labels."""
        most = max(1, min(3, (h - 2) // 14))
        lines = [Kit.fit(l, w - 4) for l in Kit.wrap(caption_words(text), w - 4)]
        if len(lines) > most:
            lines = lines[:most]
            lines[-1] = Kit.fit(lines[-1] + "..", w - 4) if not lines[-1].endswith("..") else lines[-1]
        ty = y + (h - 14 * len(lines)) // 2 - 1
        return [Kit.add_label(g, l, x + (w - Kit.text_w(l)) // 2, ty + i * 14,
                              Kit.HUE_TEXT if hue is None else hue) for i, l in enumerate(lines)]

    def click_handler(kind, menu_kind, arg):
        """Return a click callback that queues (kind, arg), or the menu kind on a Shift+click.

        Shift+click stands in for a right-click when the client does not send right-clicks to the bar.
        """
        def fn():
            """Queue the click, or the menu request when Shift is held and right-clicks do not reach the bar."""
            if st["right_ok"] is False and Client.key_held("shift"):
                queue.add((menu_kind, arg), dup=True)
            else:
                queue.add((kind, arg), dup=True)

        return Kit.once(fn, (KEY, kind, arg), Kit.TWICE)

    def hook_right(api_ctrl, fn):
        """Hook a right-button release on a control; return True when it works.

        Warns once and disables itself when the client sends no right-click events.
        """
        if api_ctrl is None or st["right_ok"] is False:
            return False
        if Kit.hook_mouse(api_ctrl, fn, event="MouseUp", button="Right"):
            st["right_ok"] = True
            return True
        if st["right_ok"] is None:
            st["right_ok"] = False
            say("no right-click events from this client; Shift+click a cell for its menu instead.")
        return False

    def add_icon(g, icon, x, y, w, h):
        """Add an icon picture centred in a cell that ignores the mouse; None on failure."""
        side = min(w, h) - 4
        p = Kit.add_pic(g, icon, x + (w - side) // 2, y + (h - side) // 2)
        if p is not None:
            p.SetWidth(side)
            p.SetHeight(side)
            p.SetAcceptMouseInput(False)
        return p

    def trims(g, xs, ws, y, h):
        """Add the gold trim lines between neighbouring panels along a row."""
        art = Kit.GOLD_V if flat() else Kit.GOLD_H
        for a, b, w in zip(xs, xs[1:], ws):
            gw = b - a - w
            s = min(gw, Kit.GOLD_T)
            Kit.add_tiled(g, art, *R(a + w + (gw - s) // 2, y, s, h))

    def draw_cell(g, ref, x, y, w, h):
        """Draw one cell's tile (an outlined empty one, or a solid one) and its contents."""
        if not cell(ref)["t"]:
            Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA * 0.3)
            # An empty cell is drawn as a faint tile with a solid one-pixel outline.
            for bx, by, bw_, bh_ in ((x, y, w, 1), (x, y + h - 1, w, 1), (x, y, 1, h), (x + w - 1, y, 1, h)):
                Kit.add_tiled(g, SLOT_TILE, bx, by, bw_, bh_, SLOT_ALPHA)
        else:
            Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        cell_content(g, ref, x, y, w, h)

    def pic_box(ref, x, y, w, h, pad):
        """Return the (x, y, w, h) a cell's picture goes in; non-square cells use a centred square."""
        if w == h or ref[0] == "u":
            return x + pad, y + pad, w - 2 * pad, h - 2 * pad
        side = min(w, h) - 2 * pad
        return x + (w - side) // 2, y + (h - side) // 2, side, side

    def cell_content(g, ref, x, y, w, h):
        """Draw what a cell holds (picture, caption, hotkey, counter) and record its controls in win.

        The info dict (position, size, count label, icon) is stored per cell ref for later updates.
        """
        c = cell(ref)
        t = c["t"]
        info = {"x": x, "y": y, "w": w, "h": h, "count": None}
        parts = []
        # Whether the cell already has something drawn on it; if not a caption is added below.
        shown = False
        # Room for the hotkey line on top when the key is shown.
        ky = 14 if (settings["keys"] and c["k"] and t) else 0
        p = None
        if t == "item" and c["g"]:
            p = add_item_pic(g, c["g"], c["h"], *pic_box(ref, x, y, w, h, 3))
        elif t == "spell":
            icon = spell_icon(c["v"])
            if icon:
                p = info["icon"] = add_icon(g, icon, x, y, w, h)
        elif t == "travel":
            m = c.get("rm")
            if m in TRAVEL_SPELL:
                icon = spell_icon(TRAVEL_SPELL[m])
                if icon:
                    p = add_icon(g, icon, x, y, w, h)
            elif m in TRAVEL_ITEM:
                p = add_item_pic(g, TRAVEL_ITEM[m], 0, *pic_box(ref, x, y, w, h, 3))
            if p is not None:
                # A travel cell's picture is dimmed so its caption and counter read clearly.
                p.SetAlpha(0.5)
            name = fit(c["v"] or "?", w - 4)
            parts.append(Kit.add_label(g, name, x + (w - Kit.text_w(name)) // 2, y + ky + (h - ky - 14) // 2 - 1))
            shown = True
        elif t == "ability":
            icon, name = ability_info(c["v"])
            if icon:
                p = add_icon(g, icon, x, y, w, h)
            elif name:
                parts.extend(add_cell_text(g, name, x, y + ky, w, h - ky))
                shown = True
        elif t == "ui":
            d = ui_def(c["v"])
            if d and d[2]:
                p = add_item_pic(g, d[2], 0, *pic_box(ref, x, y, w, h, 2))
        elif t == "script":
            nm = caption_words(cell_text(c)).strip().lower()
            # A script named like a spell shows that spell's icon.
            icon = SPELL_ICON.get(nm) if nm else None
            if icon and Kit.pic_size(icon)[0] > 0:
                p = add_icon(g, icon, x, y, w, h)
        if p is not None:
            shown = True
            parts.append(p)
        if t and not shown:
            parts.extend(add_cell_text(g, cell_text(c), x, y + ky, w, h - ky))
        win["cells"][ref] = finish_cell(g, info, parts, t in ("item", "spell", "ability", "script", "skill", "travel"),
                                        c["k"] if settings["keys"] and t else "", describe(ref), ("click", "menu", ref))
        # The counter list is rebuilt after a draw because the labels are new.
        _counters[0] = None

    def finish_cell(g, info, parts, counted, k, tip, click):
        """Add a cell's counter, hotkey label and click catcher, and return the finished info dict.

        counted says whether the cell shows a counter; k is the hotkey text (empty for none); click is
        (kind, menu kind, argument) for the left click and the right click or Shift+click.
        """
        x, y, w, h = info["x"], info["y"], info["w"], info["h"]
        if counted:
            info["count"] = Kit.add_label(g, "", x + w - 6, y + h - 16)
            info["txt"], info["hue"] = "", Kit.HUE_TEXT
            parts.append(info["count"])
        if k:
            kt = fit(short_key(k), w - 4)
            info["key"] = Kit.add_label(g, kt, x + w - 2 - Kit.text_w(kt), y + 1, Kit.HUE_INFO)
            parts.append(info["key"])
        info["tip"] = tip
        info["catcher"] = Kit.catcher(g, x, y, w, h, click_handler(*click), tip)
        parts.append(info["catcher"])
        hook_right(info["catcher"], queue(click[1:]))
        info["parts"] = parts
        return info

    def bag_tip(i):
        """Return the tooltip of bag slot i for the bag mode and the Bags window state."""
        b, mode = bag_at(i), settings["bagmode"]
        ub = (mode == 0 and st["ub_state"]) and ("Show the Bags window" if st["ub_state"] != "open"
                                                 else "Fold the Bags window into the bar")
        if mode == 1:
            tip = ("Open %s\nRight-click: pick another bag, or clear the slot" % b["n"] if b else
                   "Empty: click, then target a bag for it")
        elif ub:
            tip = ub + "\n%sRight-click: the Bags settings" % (b["n"] + "   " if b else "")
        else:
            tip = "Open %s" % b["n"] if b else "No bag here"
        bk = bag_keys()[i]
        if bk:
            tip += "  [%s]" % bk
        return tip

    def draw_bag(g, i, x, y, w, h):
        """Draw bag slot i: its tile, then what it holds."""
        Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        bag_content(g, i, x, y, w, h)

    def bag_content(g, i, x, y, w, h):
        """Draw the contents of bag slot i (picture, hotkey, counter) and store its info in win["bags"]."""
        b = bag_at(i)
        info = {"x": x, "y": y, "w": w, "h": h, "count": None}
        parts = [add_item_pic(g, b["g"], b["h"], x + 3, y + 3, w - 6, h - 6)] if b and b["g"] else []
        win["bags"][i] = finish_cell(g, info, parts, b, bag_keys()[i] if settings["keys"] else "", bag_tip(i),
                                     ("bag", "bagmenu", i))

    def want_redraw(refs):
        """Mark cells (or bag slots, kind "b") to be redrawn by the next refresh."""
        st["redraw"].update(refs)

    def refresh_key(ref):
        """Update the hotkey label and tooltip of one cell or bag slot in place, without a redraw."""
        g = win["g"]
        bag = ref[0] == "b"
        info, k = (win["bags"].get(ref[1]), bag_keys()[ref[1]]) if bag else (win["cells"].get(ref), cell(ref)["k"])
        if info is None or not Kit.is_open(g):
            return
        text = fit(short_key(k), info["w"] - 4) if (settings["keys"] and k and (bag or cell(ref)["t"])) else ""
        lbl = info.get("key")
        if text and lbl is None:
            lbl = Kit.add_label(g, text, info["x"] + info["w"] - 2 - Kit.text_w(text), info["y"] + 1, Kit.HUE_INFO)
            lbl.SetAcceptMouseInput(False)
            info["key"] = lbl
            info.setdefault("parts", []).append(lbl)
        elif lbl is not None:
            lbl.Text = text
        set_tip(info, bag_tip(ref[1]) if bag else describe(ref))

    def set_tip(info, tip):
        """Set a cell's tooltip when it differs from the one shown."""
        c = info.get("catcher")
        if c is not None and info.get("tip") != tip:
            info["tip"] = tip
            Kit.with_tip(c, tip)

    def refresh_tips():
        """Refresh the tooltips of the cells and bags whose text depends on window or module state."""
        if not Kit.is_open(win["g"]):
            return
        for ref, info in list(win["cells"].items()):
            c = cell(ref)
            if (c["t"] == "ui" and (c["v"] in ("spellbook", "virtue") or c["v"].startswith("mod:"))
                    or c["t"] == "travel"):
                set_tip(info, describe(ref))
        for i, info in list(win["bags"].items()):
            set_tip(info, bag_tip(i))

    def recolor(btn, hue, tip):
        """Change a small button's text colour and tooltip in place."""
        for lbl in btn["text"]:
            lbl.Hue = hue
        Kit.with_tip(btn.get("catcher"), tip)

    def refresh_bind_button():
        """Update the Keys button's look to match keybind mode."""
        btn = win.get("keybtn")
        if btn and Kit.is_open(win["g"]):
            recolor(btn, *bind_look())

    def refresh_tray():
        """Update the tray button's count and redraw the tray window."""
        if not Kit.is_open(win["g"]):
            return
        btn = win.get("traybtn")
        if btn:
            n = len(tray_docks())
            hue = Kit.HUE_TITLE if n else Kit.HUE_INFO
            for lbl in btn.get("text", []):
                Kit.set_text(lbl, str(n), hue)
                Kit.ui_pos(lbl, btn["x"] + (btn["w"] - Kit.text_px(str(n))) // 2, btn["ly"])
            Kit.with_tip(btn.get("catcher"), tray_tip(n))
        build_tray()

    # Fixed tooltip texts for the page column.
    PAGE_TIPS = (("up", "Next page of the bottom-left cells (page %d of %d showing)"),
                 ("dn", "Previous page of the bottom-left cells (page %d of %d showing)"),
                 ("catcher", "Page %d of %d of the bottom-left cells; click for the next page"))

    def draw_page_column(g, store, x, y0, ph, PAGE_W):
        """Draw the page column: next arrow, page number and previous arrow, with their tooltips.

        store is the art-button store of the window; the geometry comes from R so the column turns with
        an upright bar.
        """
        p = settings["page"]
        aw, ah = Kit.pic_size(Kit.ART_RESTORE[0])
        aw, ah = aw or 16, ah or 16
        cx = x + (PAGE_W - aw) // 2
        ax, ay = R(cx, y0 + 1, aw, ah)[:2]
        up = Kit.art_button(g, store, "pgup", Kit.ART_RESTORE, ax, ay, None, PAGE_TIPS[0][1] % (p + 1, PAGES),
                            on_click=queue(("page", 1)))
        ax, ay = R(cx, y0 + ph - ah - 1, aw, ah)[:2]
        dn = Kit.art_button(g, store, "pgdn", Kit.ART_MIN, ax, ay, None, PAGE_TIPS[1][1] % (p + 1, PAGES),
                            on_click=queue(("page", -1)))
        num = str(p + 1)
        nx, ny, nw, nh = R(x, y0 + ah + 1, PAGE_W, max(1, ph - 2 * ah - 2))
        lbl = Kit.add_label(g, num, nx + (nw - Kit.text_w(num)) // 2, ny + (nh - 14) // 2, Kit.HUE_TITLE)
        c = Kit.catcher(g, nx, ny, nw, nh, queue(("page", 1)), PAGE_TIPS[2][1] % (p + 1, PAGES))
        win["pagecol"] = {"up": up, "dn": dn, "num": lbl, "catcher": c, "rect": (nx, ny, nw, nh), "page": p}

    def refresh_page_column():
        """Change the page number and tooltips shown, without a redraw, when the page changed."""
        pc = win.get("pagecol")
        p = settings["page"]
        if not pc or pc["page"] == p or not Kit.is_open(win["g"]):
            return
        pc["page"] = p
        num = str(p + 1)
        nx, ny, nw, nh = pc["rect"]
        lbl = pc["num"]
        Kit.set_text(lbl, num)
        Kit.ui_pos(lbl, nx + (nw - Kit.text_w(num)) // 2, ny + (nh - 14) // 2)
        for k, tip in PAGE_TIPS:
            Kit.with_tip(pc[k], tip % (p + 1, PAGES))

    def draw_tray(g, key, d, x, y, w, h):
        """Draw one tray tile for a folded or always-shown window and its click and tooltip.

        The icon is dimmed when the window is not open; windows without an icon show three letters.
        """
        Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        state = safe(d.get("state"))
        title = d.get("title") or key
        hue = 0 if state == "open" else Kit.HUE_INFO
        icon = d.get("icon") or 0
        shown = icon and add_item_pic(g, icon, hue, x + 2, y + 2, w - 4, h - 4) is not None
        if not shown:
            add_cell_text(g, title[:3].upper(), x, y, w, h, Kit.HUE_TEXT if state == "open" else Kit.HUE_INFO)
        tip = ("%s is off; click to turn it on" if state is None else
               "Fold %s into the bar" if state == "open" else "Show %s") % title
        Kit.catcher(g, x, y, w, h, queue(("dock", key)), tip)

    def draw_small_button(g, box, caption, fn, hue, tip):
        """Draw a small captioned button on a tile; return its labels and click catcher."""
        x, y, w, h = box
        Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        return {"text": add_cell_text(g, caption, x, y, w, max(16, h), hue),
                "catcher": Kit.catcher(g, x, y, w, h, fn, tip)}

    def bind_look():
        """Return the Keys button's (hue, tooltip) for the current keybind state."""
        if st["bind"] is not None:
            return Kit.HUE_TITLE, "Keybind mode on: hover a cell, press a key; Esc or a click here ends it"
        return Kit.HUE_TEXT, "Start keybind mode: hover a cell and press a key to bind it"

    def tray_tip(n):
        """Return the tray button's tooltip for n folded windows."""
        return "%s folded into the bar; click to %s the tray" % (Kit.count(n, "window"),
                                                                         "hide" if settings["tray_open"] else "show")

    def draw_ctrl_column(g, store, L):
        """Draw the control column: minimize arrow, then the Keys, Lock and Grid buttons.

        A flat bar with enough room gets the buttons stacked in one column; otherwise the buttons are
        laid out in a grid (columns chosen by ctrl_orders) that fits the column's box.
        """
        BAR_M, CTRL_W = L["m"], L["cw"]
        x = BAR_M + L["inner"] + L["sgc"]
        col_h = L["rowy"][-1] + L["rowh"][-1]
        aw, ah = Kit.pic_size(Kit.ART_MIN[0])
        aw, ah = aw or 16, ah or 16
        ty = BAR_M + 2 + ah + 4
        avail = BAR_M + col_h - ty
        capw = ctrl_capw()
        acts = (("Keys", queue(("bind",)), bind_look()), ("Lock", queue(("lockbar",)), lock_look()),
                ("Grid", queue(("grid",)), grid_look()))
        if flat() and avail >= 66 and CTRL_W - 4 >= capw:
            mx, my = R(x + (CTRL_W - aw) // 2, BAR_M + 2, aw, ah)[:2]
            bw_, bh_ = CTRL_W - 4, min(28, (avail - 8) // 3)
            boxes = [R(x + 2, ty + i * (bh_ + 4), bw_, bh_) for i in range(3)]
        else:
            dx, dy, dw, dh = R(x, BAR_M, CTRL_W, col_h)
            opts = [(c,) + ctrl_cells(c, dw, dh) for c in ctrl_orders(not flat())]
            c, rows, cell_w, cell_h = (next((o for o in opts if o[2] >= capw and o[3] >= CTRL_ROW_MIN), None) or
                                       max(opts, key=lambda o: min(o[2] - capw, o[3] - CTRL_ROW_MIN)))
            cell_w, cell_h = max(1, cell_w), max(1, cell_h)
            block_w = c * cell_w + (c - 1) * CTRL_PAD
            block_h = rows * cell_h + (rows - 1) * CTRL_PAD
            x0 = dx + max(CTRL_PAD, (dw - block_w) // 2)
            y0 = dy + max(CTRL_PAD, (dh - block_h) // 2)
            cells = [(x0 + (n % c) * (cell_w + CTRL_PAD), y0 + (n // c) * (cell_h + CTRL_PAD),
                      cell_w, cell_h) for n in range(4)]
            mx, my = cells[0][0] + (cell_w - aw) // 2, cells[0][1] + (cell_h - ah) // 2
            # The remaining three boxes belong to Keys, Lock and Grid.
            boxes = cells[1:]
        if not Kit.zone_up(KEY):
            Kit.art_button(g, store, "min", Kit.ART_MIN, mx, my, None, "Minimize the bar",
                           on_click=queue(("toggle_min",)))
        win["keybtn"], win["lockbtn"], win["gridbtn"] = [draw_small_button(g, box, cap, fn, *look)
                                                         for (cap, fn, look), box in zip(acts, boxes)]

    def grid_look():
        """Return the Grid button's (hue, tooltip) for whether the grid is shown."""
        if HOST.grid_shown():
            return Kit.HUE_TITLE, "Hide the screen grid windows snap to"
        return Kit.HUE_INFO, "Show the screen grid; windows you let go snap to it, the corners, edge middles and centre"

    def toggle_grid():
        """Show or hide the host's snap grid and update the Grid button."""
        on = bool(HOST.grid_toggle())
        btn = win.get("gridbtn")
        if btn and Kit.is_open(win["g"]):
            recolor(btn, *grid_look())
        say("screen grid %s." % ("shown" if on else "hidden"))

    def lock_look():
        """Return the Lock button's (hue, tooltip) for the zone layout or the bar's own lock."""
        if HOST.layout_in_use():
            if HOST.layout_arranging():
                return Kit.HUE_TITLE, "Lock every window in its zone"
            return Kit.HUE_INFO, "Unlock the layout to move windows between zones"
        if settings["lock"]:
            return Kit.HUE_BAD, "Locked; click to unlock the bar"
        return Kit.HUE_INFO, "Lock the bar in place"

    def refresh_lock_button():
        """Update the Lock button and whether the bar can be dragged. Returns False when no bar is up."""
        g, btn = win["g"], win.get("lockbtn")
        if not btn or not Kit.is_open(g):
            return False
        g.CanMove = not settings["lock"] and not HOST.layout_locked(KEY)
        recolor(btn, *lock_look())
        win["arranging"] = HOST.layout_arranging()
        return True

    WIN_PARTS = ("g", "store", "cells", "bags", "keybtn", "lockbtn", "gridbtn", "traybtn", "pagecol")

    def build_window():
        """Draw a fresh bar and dispose of the old one only once the new one is up.

        If drawing fails the old bar stays and the half-built one is thrown away; the error is raised
        again for the caller to report.
        """
        keep = dict((k, win.get(k)) for k in WIN_PARTS)
        old = keep["g"]
        x, y = (old.GetX(), old.GetY()) if Kit.is_open(old) else (None, None)
        win.setdefault("stale", []).append(old)
        # Clear every per-bar entry; the old gump is kept aside in win["stale"] until the new one shows.
        win.update(dict.fromkeys(WIN_PARTS[4:]), g=None, cells={}, bags={})
        store = ({}, {})
        _counters[0] = None
        built = {"g": None}
        try:
            _draw_bar(x, y, store, built)
        except Exception:
            if win["g"] is None:
                Kit.dispose(built["g"])
                win.update(keep)
                _counters[0] = None
                win["stale"] = [s for s in win.get("stale", []) if s is not old]
            else:
                for s in win.pop("stale", []):
                    Kit.dispose(s)
            raise

    def _draw_bar(x, y, store, built):
        """Draw the whole bar (or the minimized strip) at x, y and show it.

        store is the art-button store and built receives the new gump so a failure can dispose of it.
        Lays out extra rows, the top row, the page column and bottom cells, window buttons, bag slots,
        tray button and controls from the geometry in geom(). Layout is drawn flat; R turns it upright.
        """
        held_lock = HOST.layout_locked(KEY)
        # A minimized bar shows only in the free state; a zone always draws the full bar.
        em = st["em"] = bool(st["minimized"]) and not Kit.zone_up(KEY)
        if em:
            w, h = MINI_W, MINI_H
            if x is None:
                x, y = Kit.load_pos(POS_KEY, (200, 600), (w, h))
            # Second argument is whether the gump may be dragged; a held lock or zone stops it.
            g = built["g"] = G.CreateGump(True, not held_lock)
            Kit.mini_bar(g, store, w, h, TITLE, KEY, queue(("toggle_min",)),
                         "%s: page %d" % (TITLE, settings["page"] + 1))
        else:
            refit_if_stale()
            L = geom()
            w, h = bar_size()
            # A zone slot larger than the bar centres the bar in it.
            fitst["off"] = (0, 0)
            slot = told_slot()
            if slot is not None:
                fitst["off"] = (max(0, (slot[0] - w) // 2), max(0, (slot[1] - h) // 2))
                w, h = max(w, slot[0]), max(h, slot[1])
            if x is None:
                x, y = Kit.load_pos(POS_KEY, (200, 600), (w, h))
            BAR_M, PAGE_W, p4 = L["m"], L["pw"], L["p4"]
            UI_GAP, BAG_GAP, TRAY_BTN = L["ug"], L["bg"], L["tb"]
            SGX, colx, colw = L["sgx"], L["colx"], L["colw"]
            rowy, rowh, celly, cellh = L["rowy"], L["rowh"], L["celly"], L["cellh"]
            x0 = BAR_M + PAGE_W
            g = built["g"] = G.CreateGump(True, not settings["lock"] and not held_lock)
            Kit.add_window_frame(g, w, h, corners=False)
            r = 0
            # Extra rows go above the top row, the highest row first.
            for kind, base in ([("x", k * TOP_SLOTS) for k in range(settings["extra"] - 1, -1, -1)]
                               + ([("a", 0)] if settings["top"] else [])):
                y0 = BAR_M + rowy[r]
                Kit.gold_box(g, *R(x0, y0, L["top_w"], rowh[r]))
                cy, ch = y0 + celly[r], cellh[r]
                for i in range(TOP_SLOTS):
                    draw_cell(g, (kind, base + i), *R(x0 + colx[i], cy, colw[i], ch))
                trims(g, [x0 + c for c in colx], colw, cy, ch)
                r += 1
            y0, ph = BAR_M + rowy[r], rowh[r]
            cy, ch = y0 + celly[r], cellh[r]
            draw_page_column(g, store, BAR_M, y0, ph, PAGE_W)
            Kit.gold_box(g, *R(x0, y0, L["left_w"], ph))
            for i in range(BOTTOM_SLOTS):
                draw_cell(g, ("a", TOP_SLOTS + i), *R(x0 + colx[i], cy, colw[i], ch))
            trims(g, [x0 + c for c in colx[:BOTTOM_SLOTS]], colw, cy, ch)
            ux = x0 + L["left_w"] + SGX
            Kit.gold_box(g, *R(ux, y0, L["ui_w"], ph))
            # The window button strip has a faint stone background.
            Kit.add_tiled(g, Kit.STONE_TILE, *R(ux + p4, y0 + p4, L["ui_w"] - 2 * p4, ph - 2 * p4), alpha=0.55)
            total = UI_SLOTS * L["bw"] + (UI_SLOTS - 1) * UI_GAP
            bx = ux + (L["ui_w"] - total) // 2
            for i in range(UI_SLOTS):
                draw_cell(g, ("u", i), *R(bx + i * (L["bw"] + UI_GAP), y0 + (ph - L["bh"]) // 2, L["bw"], L["bh"]))
            trims(g, [bx + i * (L["bw"] + UI_GAP) for i in range(UI_SLOTS)], (L["bw"],) * UI_SLOTS,
                  y0 + (ph - L["bh"]) // 2, L["bh"])
            gx = ux + L["ui_w"] + SGX
            Kit.gold_box(g, *R(gx, y0, L["bag_w"], ph))
            total = BAG_SLOTS * L["bgw"] + (BAG_SLOTS - 1) * BAG_GAP
            bx = gx + (L["bag_w"] - total) // 2
            for i in range(BAG_SLOTS):
                draw_bag(g, i, *R(bx + i * (L["bgw"] + BAG_GAP), cy, L["bgw"], L["bgh"]))
            trims(g, [bx + i * (L["bgw"] + BAG_GAP) for i in range(BAG_SLOTS)], (L["bgw"],) * BAG_SLOTS, cy, L["bgh"])
            tx = gx + L["bag_w"] + SGX
            Kit.gold_box(g, *R(tx, y0, L["tray_w"], ph))
            draw_tray_button(g, *R(tx + p4, cy, TRAY_BTN, L["bgh"]))
            draw_ctrl_column(g, store, L)
        if settings["anchor"] and not Kit.zone_up(KEY):
            ax, ay = Kit.anchor_pos(settings["anchor"], w, h)
            if ax is not None:
                x, y = ax, ay
        # show_window places the gump and wires save and dispose handling.
        st["last_pos"] = Kit.show_window(g, x, y, w, h, None, False, on_disposed(g), save_pos, win,
                                         {"g": g, "store": store})
        st["moved_at"] = None
        for s in win.pop("stale", []):
            Kit.dispose(s)
        # Count right away only when the last count is old.
        if not em and time.time() - st.get("counted_at", 0.0) > COUNT_EVERY:
            k = _cell_kinds()
            if "item" in k["types"] or k["extra"]:
                count_now()
        update_labels()
        build_tray()

    def draw_tray_button(g, x, y, w, h):
        """Draw the tray button showing how many windows are folded in."""
        n = len(tray_docks())
        Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        labels = add_cell_text(g, str(n), x, y, w, h, Kit.HUE_TITLE if n else Kit.HUE_INFO)
        win["traybtn"] = {"text": labels, "x": x, "w": w, "ly": y + (h - 14) // 2 - 1,
                          "catcher": Kit.catcher(g, x, y, w, h, queue(("traywin",)), tray_tip(n))}

    def tray_pos(w, h, at=None, rect=False):
        """Return where the tray goes beside the bar, on the side that stays on screen.

        at and rect override the bar's position and box. Tries right of a flat bar, then left, then
        below, then above; an upright bar tries below first.
        """
        if rect is False:
            g = win["g"]
            if not Kit.is_open(g):
                return 300, 300
            rect = Kit.rect(g)
            if at is None:
                at = Kit.pos(g) or (0, 0)
        bx, by = at
        bw, bh = (rect[2], rect[3]) if rect is not None and rect[2] > 0 else bar_size()
        W, H = Kit.screen()
        if flat():
            x, y = bx + bw + TRAY_GAP, by + bh - h
            if W and x + w > W:
                x = bx - TRAY_GAP - w
                if x < 0:
                    x, y = bx, by + bh + TRAY_GAP
                    if H and y + h > H:
                        y = by - TRAY_GAP - h
        else:
            x, y = bx, by + bh + TRAY_GAP
            if H and y + h > H:
                y = by - TRAY_GAP - h
                if y < 0:
                    x, y = bx + bw + TRAY_GAP, by
                    if W and x + w > W:
                        x = bx - TRAY_GAP - w
        return x, y

    def bar_gump():
        """Return the bar's gump (used by the host for docking)."""
        return win["g"]

    wnd = None

    def refresh():
        """Redraw the cells and bag slots marked in st["redraw"], then update the counters."""
        refs, st["redraw"] = st["redraw"], set()
        g = win["g"]
        if not refs or st["em"] or not Kit.is_open(g):
            return
        for ref in sorted(refs):
            bag = ref[0] == "b"
            info = win["bags"].get(ref[1]) if bag else win["cells"].get(ref)
            if info is None:
                continue
            for p in info.get("parts") or ():
                Kit.dispose(p)
            if bag:
                bag_content(g, ref[1], info["x"], info["y"], info["w"], info["h"])
            else:
                cell_content(g, ref, info["x"], info["y"], info["w"], info["h"])
        update_labels()

    def place_on_anchor():
        """Move the bar to its anchor spot when it is not already there."""
        g = win["g"]
        if not settings["anchor"] or not Kit.is_open(g) or Kit.zone_up(KEY):
            return
        w, h = bar_size()
        x, y = Kit.anchor_pos(settings["anchor"], w, h)
        if x is None:
            return
        if (x, y) != st.get("last_pos"):
            g.SetPos(x, y)
            Kit.note_rect(g, x, y)
            Kit.moved_by_code(g)
            st["last_pos"] = (x, y)
            follow_tray()

    def settle(x, y):
        """React to the bar being let go at x, y: snap to a corner, edge or centre and turn upright or flat.

        The anchor name comes from Kit.anchor_at. Left and right edges stand the bar upright, top and
        bottom edges lay it flat; a change of shape rebuilds the bar. Not used in a zone.
        """
        if st["em"]:
            return
        if Kit.zone_up(KEY):
            return
        w, h = bar_size()
        name = Kit.anchor_at(x, y, w, h, SNAP_ANCHOR)
        # Left and right edges stand the bar upright, top and bottom lay it flat, anything else keeps it.
        turn = True if name in ("L", "R") else False if name in ("T", "B") else None
        turning = turn is not None and turn != settings["vertical"]
        if name != settings["anchor"] or turning:
            settings["anchor"] = name
            if turning:
                settings["vertical"] = turn
                save_settings()
                want_rebuild()
                say("standing %s along the %s edge." % ("upright" if turn else "flat",
                    {"L": "left", "R": "right", "T": "top", "B": "bottom"}[name]))
                return
            save_settings()
        place_on_anchor()
        save_pos()

    def watch_position(now):
        """Watch the bar's position each tick: settle it shortly after a drag, keep the tray beside it.

        Also re-applies the anchor every couple of seconds when the screen size changes.
        """
        g = win["g"]
        if not Kit.is_open(g):
            return
        rect = Kit.rect(g)
        pos = (rect[0], rect[1]) if rect else (0, 0)
        if pos != st.get("last_pos"):
            st["last_pos"], st["moved_at"] = pos, now
        # Wait until the mouse is released and the position has held still for a moment.
        elif st.get("moved_at") is not None and now - st["moved_at"] >= 0.3 and SNAP.pressed() is not True:
            st["moved_at"] = None
            settle(pos[0], pos[1])
        follow_tray(pos, rect)
        # The screen size is checked only every couple of seconds.
        if settings["anchor"] and now >= st.get("screen_next", 0.0):
            st["screen_next"] = now + 2.0
            wh = Kit.screen()
            if wh != st.get("screen_wh"):
                st["screen_wh"] = wh
                if not Kit.zone_up(KEY):
                    place_on_anchor()

    def build_tray():
        """Draw the tray window of folded and always-shown windows beside the bar, or remove it."""
        old, tray["g"] = tray["g"], None
        docks = tray_docks()
        if st["em"] or not settings["tray_open"] or not docks:
            Kit.dispose(old)
            return
        L = geom()
        tb, bg, m = L["tb"], L["bg"], max(4, L["tm"] // 2)
        aw, ah = Kit.pic_size(Kit.ART_MIN[0])
        aw, ah = aw or 16, ah or 16
        bh = L["bgh"]
        w = m + len(docks) * (tb + bg) + aw + m
        h = m + bh + m
        g = G.CreateGump(True, False)
        Kit.add_window_frame(g, w, h, corners=False)
        for i, (key, d) in enumerate(docks):
            draw_tray(g, key, d, m + i * (tb + bg), m, tb, bh)
        store = ({}, {})
        Kit.art_button(g, store, "fold", Kit.ART_MIN, w - m - aw, m + (bh - ah) // 2, None,
                       "Hide the tray (the bar's numbered button brings it back)", on_click=queue(("traywin",)))
        x, y = tray_pos(w, h)
        Kit.place(g, x, y, w, h)
        tray.update({"g": g, "at": (x, y), "w": w, "h": h})
        G.AddGump(g)
        Kit.attach(g, win["g"])
        Kit.dispose(old)

    def follow_tray(at=None, rect=False):
        """Move the tray along with the bar."""
        g = tray["g"]
        if not Kit.is_open(g):
            return
        w, h = tray.get("w", 0), tray.get("h", 0)
        x, y = tray_pos(w, h, at, rect)
        if (x, y) != tray["at"]:
            tray["at"] = (x, y)
            g.SetPos(*Kit.clamp(x, y, w, h))
            Kit.moved_by_code(g)

    def open_spellbook():
        """Use the first spellbook found in the pack or worn. Returns True when one was used.

        Used as the fallback when Grimoire cannot be turned on.
        """
        # Count the spellbook graphics along with the items the bar holds.
        count_now(SPELLBOOKS)
        book = (next((s for s in (st["first_g"].get(gr) for gr in SPELLBOOKS) if s), None) or
                API.FindLayer("Spellbook"))
        if book:
            API.UseObject(book)
            return True
        say("no spellbook in your pack.", Kit.HUE_BAD)
        return False

    def toggle_lock():
        """Lock or unlock the bar; with zones in use it toggles Arrange mode instead."""
        if HOST.layout_in_use():
            HOST.layout_arrange()
            refresh_lock_button()
            return
        settings["lock"] = not settings["lock"]
        save_settings()
        if not refresh_lock_button():
            want_rebuild()
        # The settings page may be open: keep its checkbox in step.
        if cfg.f is not None:
            cfg.f.c["lock"].IsChecked = settings["lock"]
        else:
            HOST.refresh_settings(KEY)
        say("%s." % ("locked" if settings["lock"] else "unlocked"), Kit.HUE_GOOD)

    def hovered_ref():
        """Return the ref of the cell or bag slot under the mouse, or None."""
        g = win["g"]
        pos = Kit.mouse_pos()
        at = Kit.pos(g) if Kit.is_open(g) else None
        if pos is None or at is None:
            return None
        mx, my = pos[0] - at[0], pos[1] - at[1]
        for ref, info in (list(win["cells"].items()) + [(("b", i), info) for i, info in win["bags"].items()]):
            if info["x"] <= mx < info["x"] + info["w"] and info["y"] <= my < info["y"] + info["h"]:
                return ref
        return None

    def start_bind(ref=None):
        """Start keybind mode (optionally with a cell already selected) and tell the player."""
        HOST.release_typing()
        st["bind"] = {"sel": ref}
        refresh_bind_button()
        say("keybind mode on: %s (Esc ends it, Backspace clears a key)." % (
            "click a cell, then press a key" if Kit.mouse_pos() is None else "hover a cell and press a key"))

    def end_bind():
        """End keybind mode."""
        if st["bind"] is None:
            return
        st["bind"] = None
        refresh_bind_button()
        say("keybind mode off.")

    def assign_key(ref, k):
        """Bind hotkey k to a cell or bag slot, taking it off any other cell that held it.

        Refuses a key another module owns.
        """
        owner = key_owner(k)
        if owner:
            say("%s belongs to %s; pick another." % (k, owner), Kit.HUE_BAD)
            return
        changed = [ref]
        for r, c in all_cells():
            if r != ref and _norm_key(c["k"]) == k:
                c["k"] = ""
                changed.append(r)
                say("%s taken off %s." % (k, ref_name(r)))
        for i, bk in enumerate(bag_keys()):
            if ("b", i) != ref and bk == k:
                set_key_of(("b", i), "")
                changed.append(("b", i))
                say("%s taken off bag slot %d." % (k, i + 1))
        set_key_of(ref, k)
        if ref[0] == "b":
            save_cells()
        register_hotkeys()
        keys_changed(changed)
        empty = ref[0] != "b" and not cell(ref)["t"]
        say("%s bound to %s%s." % (k, ref_name(ref), " (empty; fill it to use it)" if empty else ""), Kit.HUE_GOOD)

    def on_bind_key(combo):
        """Handle a key pressed in keybind mode: Esc ends it, Backspace or Delete clears, else bind.

        combo is the key combination text from the client. The cell is the hovered one, or the last
        selected one.
        """
        b = st["bind"]
        if not b:
            return
        k = combo.rsplit("+", 1)[-1]
        if k == "ESCAPE":
            end_bind()
            return
        ref = hovered_ref() or b["sel"]
        if ref is None:
            say("hover a cell on the bar (or click one) first.")
            return
        b["sel"] = ref
        if k in ("BACKSPACE", "DELETE"):
            set_key_of(ref, "")
            register_hotkeys()
            keys_changed([ref])
            say("%s has no hotkey now." % ref_name(ref), Kit.HUE_GOOD)
            return
        assign_key(ref, combo)

    def keys_changed(refs):
        """Refresh the key labels of cells whose key changed and the settings page entry if shown."""
        for r in refs:
            refresh_key(r)
        shown = sel_ref(page["sel"])
        if cfg.f is not None and shown in refs:
            cfg.f.c["key"].SetText(cell(shown)["k"])

    # Window buttons that need no client call.
    UI_SIMPLE = {"barsettings": lambda: HOST.show_settings(KEY), "lock": lambda: toggle_lock(),
                 "minimize": lambda: queue(("toggle_min",))(),
                 "war": lambda: API.SetWarMode(not bool(API.Player.InWarMode)),
                 "help": lambda: API.OpenHelp(), "quests": lambda: API.OpenQuestLog()}

    def run_ui(uid):
        """Run a window button by its id: client windows, modules, Grimoire, Virtue Assistant and so on.

        Returns True when it worked; says why when it did not.
        """
        d = ui_def(uid)
        if d is None:
            say("unknown window button '%s'." % uid, Kit.HUE_BAD)
            return False
        how = d[3]
        ok = True
        if how in UI_SIMPLE:
            UI_SIMPLE[how]()
        elif how == "grimoire":
            return toggle_grimoire()
        elif how == "virtue":
            return toggle_va()
        elif how == "paperdoll":
            # Paperdoll is opened through the client's own action; the context menu is the fallback.
            import System
            if not ClientUI.game_action("OpenPaperdoll", [System.UInt32(int(API.Player.Serial))]):
                if Client.on_client_thread():
                    later(lambda: run_ui("paperdoll"))
                else:
                    ok = safe(lambda: API.ContextMenu(API.Player, "Open Paperdoll", 2), None) is not False
        elif how.startswith("mod:"):
            return toggle_module(how[4:])
        elif how.startswith("ga:"):
            parts = how.split(":")
            ok = ClientUI.game_action(parts[1], reuse=parts[2] if len(parts) > 2 else None)
        elif how.startswith("macro:"):
            ok = ClientUI.open_macro(how[6:])
        if not ok:
            say("couldn't open %s (%s)." % (d[1], ClientUI.error or "unknown"), Kit.HUE_BAD)
        return ok

    _legion = {"looked": False, "type": None}

    def loaded_scripts():
        """Return (relative path, full path) of every script the Legion script manager has loaded.

        Reads the client's list by reflection; on the client thread it only queues the first look and
        returns an empty list until then.
        """
        # Reflection runs on the script thread only; the client thread asks for it later.
        if not _legion["looked"] and Client.on_client_thread():
            if not _legion.get("asked"):
                _legion["asked"] = True
                later(loaded_scripts)
            return []
        if not _legion["looked"]:
            _legion["looked"] = True
            _legion["type"] = Client._type("ClassicUO.LegionScripting.LegionScripting")
        t = _legion["type"]
        if t is None:
            return []
        out = []

        def get(sf, n):
            """Read a field of a loaded script as text, empty when missing."""
            return str(safe(lambda: ClientUI._get(sf, n), "") or "")

        with Kit.quiet:
            for sf in (ClientUI._get(None, "LoadedScripts", t) or []):
                rel, path = get(sf, "RelativePath") or get(sf, "FileName"), get(sf, "FullPath")
                if rel or path:
                    out.append((rel, path))
        return out

    _script_names = {}
    _names_due = set()

    def script_names_for(v):
        """Return the names the script manager might know a script cell's script by.

        The result is cached for a minute. On the script thread it also walks the Legion folder for a
        file of that name; on the client thread it queues that walk and returns the cached answer.
        """
        v = str(v or "").strip().replace("\\", "/")
        hit = _script_names.get(v)
        if hit is not None and time.time() < hit[0]:
            return list(hit[1])
        base = v.split("/")[-1]
        low, blow = v.lower(), base.lower()
        out = []

        def add(c):
            """Add a candidate name once."""
            if c and c not in out:
                out.append(c)

        walk = not Client.on_client_thread()
        if not walk:
            if v not in _names_due:
                _names_due.add(v)

                def job():
                    """Redo the lookup off the client thread."""
                    _names_due.discard(v)
                    script_names_for(v)

                later(job)
            if hit is not None:
                return list(hit[1])
        if "/" in v:
            add(v)
        for rel, _ in loaded_scripts():
            r = rel.replace("\\", "/")
            rl = r.lower()
            if rl == low or rl.endswith("/" + low) or rl.split("/")[-1] == blow:
                add(r)
        if not walk:
            add(v)
            add(base)
            return list(out)
        root = legion_root()
        if root:
            with Kit.quiet:
                for d, dirs, files in os.walk(root):
                    rel = d.replace("\\", "/")[len(root):].strip("/")
                    if rel.count("/") >= 2:
                        dirs[:] = []
                    # Skips hidden folders, library folders and folders deeper than two levels.
                    dirs[:] = [x for x in dirs if not x.startswith(".") and x.lower() not in LIB_DIRS]
                    for f in files:
                        if f.lower() == blow:
                            add((rel + "/" + f) if rel else f)
        add(v)
        add(base)
        # Keep the result for a minute.
        _script_names[v] = (time.time() + 60.0, out)
        return list(out)

    _run_hint = {}

    def script_running(v):
        """Return whether the script of a script cell is running, trying each name it may go by.

        Remembers the name that worked first.
        """
        names = script_names_for(v)
        hint = _run_hint.get(v)
        if hint is not None and hint in names:
            try:
                if API.IsScriptRunning(hint):
                    return True
            except Exception:
                pass
        for c in names:
            if c == hint:
                continue
            try:
                if API.IsScriptRunning(c):
                    if len(_run_hint) > 200:
                        _run_hint.clear()
                    _run_hint[v] = c
                    return True
            except Exception:
                pass
        return False

    def run_script(v):
        """Start the script of a script cell, or stop it when it runs; return True if a call was made."""
        cands = script_names_for(v)
        was = script_running(v)
        fn = API.StopScript if was else API.PlayScript
        done = False
        for c in cands:
            if not safe(lambda c=c: (fn(c), True)[1], False):
                continue
            done = True
            # Stop trying further names once one call took effect.
            if not HOST.idle(0.1) or script_running(v) != was:
                break
        # A check half a second later reports what happened.
        st["script_check"] = (v, was, time.time() + 0.5)
        return done

    def check_script(now):
        """After a script cell was used, report whether the script started or stopped."""
        chk = st.get("script_check")
        if not chk or now < chk[2]:
            return
        st["script_check"] = None
        v, was, _ = chk
        on = script_running(v)
        name = v.replace("\\", "/").split("/")[-1]
        if was and not on:
            say("stopped %s." % name)
        elif not was and on:
            say("started %s." % name, Kit.HUE_GOOD)
        elif not was:
            say("%s didn't start; is it in the Legion Script Manager's list (refresh it)?" % name, Kit.HUE_BAD)
        update_labels()

    def use_item(c):
        """Use the cell's item from the pack; return True when one was used.

        Refreshes the count first when it is stale, and again if no serial was found, then forgets the
        cached pack so the counter updates quickly.
        """
        def first():
            """Return the first matching item serial for the cell (same hue first)."""
            return st["first"].get((c["g"], c["h"])) or (None if settings["hue"] else st["first_g"].get(c["g"]))

        stale = time.time() - st.get("counted_at", 0.0) > COUNT_EVERY
        if stale:
            count_now()
        serial = first()
        if not serial and not stale:
            count_now()
            serial = first()
        if not serial:
            say("no %s left." % cell_text(c), Kit.HUE_BAD)
            return False
        API.UseObject(serial)
        st["next_count"] = time.time() + 0.4
        HOST.pack_dirty()
        return True

    # Cell types that call one API function with the cell's value.
    CELL_CALLS = {"spell": API.CastSpell, "skill": API.UseSkill, "dress": API.Dress, "undress": API.Undress,
                  "say": API.Msg}
    HARM_SKILLS = ("stealing", "snooping", "discordance", "provocation")

    def harmful_cell(c, t, v):
        """Return whether a cell does something harmful when aimed at the last target.

        Covers harmful spells, skills such as stealing, and the explosion potion.
        """
        if t == "skill":
            n = v.lower()
            return bool(n) and any(n in s for s in HARM_SKILLS)
        if t == "spell":
            n = v.lower()
            return bool(n) and (n in HARMFUL_SPELLS or any(s.startswith(n) for s in HARMFUL_SPELLS))
        return t == "item" and int(c.get("g") or 0) == 0x0F0D

    def must_confirm(tok, c, t, v):
        """Return True when a harmful cell aimed at the last target must wait for a second press.

        R1: the confirmation goes through the host's harm check, never a bare repeat.
        """
        if c["tg"] != "last" or not harmful_cell(c, t, v):
            return False
        # The harm check gets the last target, a token for this cell, and asks for a repeat press.
        return not HOST.harm_ok(int(API.LastTargetSerial or 0), ("actionbar",) + tok, TITLE, True,
                                "press again to confirm", t == "skill")

    def run_cell(ref):
        """Do what a cell does: cast, use, run, start a script, open a window or travel.

        Sets up the automatic target for cells aimed at self or the last target, unless another target
        is pending or the cursor is in use (the player then targets by hand). Starts the cooldown
        darkening for skills and spells.
        """
        c = cell(ref)
        t, v = c["t"], c["v"].strip()
        if not t:
            say("%s is empty." % ref_name(ref))
            return
        now = time.time()
        tok = (ref, settings["page"])
        if must_confirm(tok, c, t, v):
            return
        arms = c["tg"] in ("self", "last") and t not in ("travel", "say", "ui", "dress", "undress", "ability")
        w = st["want_target"]
        if w and now > w[1]:
            w = None
        pending_same = bool(w) and w[2] == tok
        clash = False
        if w and not pending_same:
            drop_want()
            clash = arms
        ok = True
        # A cursor that was already up is not ours to answer.
        cursor_was_up = bool(API.HasTarget("any"))
        try:
            if t in CELL_CALLS:
                CELL_CALLS[t](v)
            elif t == "item":
                ok = use_item(c)
            elif t == "macro":
                r = ClientUI.run_macro(v)
                ok = bool(r)
                if r is None:
                    say("no TazUO macro named '%s'." % v, Kit.HUE_BAD)
                elif not r:
                    say("couldn't run macro '%s' (%s)." % (v, ClientUI.error or "unknown"), Kit.HUE_BAD)
            elif t == "ability":
                API.ToggleAbility(v or "primary")
            elif t == "script":
                def job():
                    """Start or stop the script off the click path."""
                    try:
                        run_script(v)
                    except Exception as ex:
                        say("couldn't use %s (%s)." % (cell_text(c), ex), Kit.HUE_BAD)

                later(job)
            elif t == "ui":
                ok = run_ui(v)
            elif t == "travel":
                ok = fire_travel(c)
        except Exception as ex:
            say("couldn't use %s (%s)." % (cell_text(c), ex), Kit.HUE_BAD)
            ok = False
        if ok and t in ("skill", "spell"):
            start_cool(t, v)
        if ok and arms and not pending_same:
            if clash:
                say("a target was still pending; target by hand.")
            elif cursor_was_up:
                say("a target cursor was already up; target by hand.")
            elif HOST.cursor_busy(KEY):
                say("another module is using the target cursor; target by hand.")
            else:
                # Wait for the cursor: the spell's cast delay is added on top.
                wait = 2.5
                if t == "spell":
                    info = Kit.spell_info(v)
                    wait += info[3] if info else 0.0
                HOST.claim_cursor(KEY, wait)
                st["want_target"] = (c["tg"], time.time() + wait, tok, harmful_cell(c, t, v),
                                     int(API.LastTargetSerial or 0))

    def handle_target(now):
        """Answer the target cursor a cell asked for: target self or the last target, once, in time."""
        w = st["want_target"]
        if not w:
            return
        mode, until = w[0], w[1]
        if now > until:
            drop_want()
            return
        if not API.HasTarget("any"):
            return
        drop_want()
        if HOST.cursor_busy(KEY):
            return
        if API.HasTarget("beneficial" if w[3] else "harmful"):
            say("that cursor isn't this cell's; target by hand.")
            return
        if mode == "self":
            API.TargetSelf()
        else:
            last = w[4] if w[3] else int(API.LastTargetSerial or 0)
            if last:
                API.Target(last)
            else:
                say("no last target yet; target by hand.")

    def drop_want():
        """Forget the pending target request and give the cursor back."""
        st["want_target"] = None
        HOST.release_cursor(KEY)

    def pick(action):
        """Ask the player to target something and queue the action with the serial that was picked."""
        drop_want()

        def done(serial):
            """Callback of the target pick: queue the action with the serial."""
            queue.add(tuple(action) + (int(serial or 0),), dup=True)

        HOST.pick_target(15, done)

    def pick_item(ref):
        """Ask the player to target an item for a cell."""
        say("target an item for %s (Esc to cancel)." % ref_name(ref))
        pick(("picked_item", ref, settings["page"]))

    def picked_item(ref, pg, serial):
        """Set a cell to the item that was targeted, on the page it was asked for.

        ref is the cell, pg the page it was asked on, serial the item. Ignored while shutting down.
        """
        if st["shutting"] or HOST.aborting():
            return
        item = Kit.find_item(serial)
        if item is None:
            say("no item picked.")
            return
        gr, hu = int(item.Graphic or 0), int(item.Hue or 0)
        name = str(item.Name or "") or ("0x%04X" % gr)
        where = ref_name(ref)
        refs = [ref]
        if ref[0] == "a" and ref[1] >= TOP_SLOTS and pg != settings["page"] and cells["pages"]:
            target = cells["pages"][pg][ref[1] - TOP_SLOTS]
            where = "page %d cell %d" % (pg + 1, ref[1] - TOP_SLOTS + 1)
            refs = []
        else:
            target = cell(ref)
        target.update({"t": "item", "v": "", "g": gr, "h": hu, "n": name})
        for k in TRAVEL_KEYS:
            target.pop(k, None)
        cells_changed(recount=True, refs=refs)
        say("%s set on %s." % (name, where), Kit.HUE_GOOD)

    def pick_bag(i):
        """Ask the player to target a bag for a bag slot."""
        say("target a bag for bag slot %d (Esc to cancel)." % (i + 1))
        pick(("picked_bag", i))

    def picked_bag(i, serial):
        """Store the bag that was targeted for a bag slot; only containers are accepted."""
        if st["shutting"] or HOST.aborting():
            return
        item = Kit.find_item(serial)
        if item is None or not item.IsContainer:
            say("that isn't a bag.", Kit.HUE_BAD)
            return
        set_picked_bag(i, serial)
        st["next_scan"] = 0.0

    def on_cell_click(ref):
        """Handle a left click on a cell: select it in keybind mode, use it, or target an item for it."""
        if st["bind"] is not None:
            st["bind"]["sel"] = ref
            say("%s; now press a key or combination for it." % ref_name(ref))
        elif cell(ref)["t"]:
            run_cell(ref)
        elif ref[0] in ("a", "x"):
            pick_item(ref)
        else:
            open_menu(ref)

    def on_bag_click(i):
        """Handle a left click on a bag slot: bind it in keybind mode, else open, show or fold its bag."""
        if st["bind"] is not None:
            st["bind"]["sel"] = ("b", i)
            say("bag slot %d; now press a key or combination for it." % (i + 1))
            return
        b = bag_at(i)
        if settings["bagmode"] == 1 and b is None:
            pick_bag(i)
            return
        if settings["bagmode"] == 0:
            state = ub_state()
            if state in ("collapsed", "docked"):
                ub_send("show")
                heartbeat()
            elif state == "open":
                heartbeat()
                ub_send("dock")
            else:
                serial = b["s"] if b else None
                turn_on(UB_MODULE_KEY, "Bags", (lambda: API.UseObject(serial)) if serial else None)
        elif b is None:
            say("no bag in that slot (see Bag slots on the Action Bar settings page).")
        else:
            API.UseObject(b["s"])

    CATS = [("item", "Item...")] + [(k, dict(TYPES)[k])
                                    # Types of the cell menu, in menu order.
                                    for k in "spell skill ability ui macro script dress undress say travel".split()]
    MENU_CAPS = dict(CATS + [("hotkey", "Hotkey"), ("lo", "Red at")])
    LIST_TITLES = {"macro": "TazUO macros", "script": "Legion scripts",
                   "dress": "Dress outfits", "undress": "Dress outfits"}

    def legion_root():
        """Return the folder that holds the Legion scripts (the parent of the folder this script is in)."""
        base = Kit.script_dir().replace("\\", "/").rstrip("/")
        parent = os.path.dirname(base)
        return parent if parent and parent != base else base

    # Folder names left out of the script walk.
    LIB_DIRS = ("iplib", "lib", "libs", "library", "site-packages", "dlls", "stubs",
                "__pycache__", "api", "docs", "examples", "virtueassistantmodules")

    def script_names():
        """Return the script names for the script picker, merged from the loaded list and the folder."""
        root_dir = legion_root()
        rl = root_dir.lower()
        out = []
        for name, path in loaded_scripts():
            p = path.replace("\\", "/")
            # A path under the Legion folder is shown relative to it.
            rel = (p[len(root_dir):].strip("/") if root_dir and p.lower().startswith(rl) else (p or name))
            parts = rel.lower().split("/")
            # Library folders and files starting with an underscore are not scripts a player picks.
            if any(d in LIB_DIRS for d in parts[:-1]) or parts[-1].startswith("_"):
                continue
            if rel and rel not in out:
                out.append(rel)
        # When the manager listed nothing, walk the Legion folder instead.
        if out or not root_dir:
            return sorted(out, key=lambda s: s.lower())
        with Kit.quiet:
            for root, dirs, files in os.walk(root_dir):
                rel = root.replace("\\", "/")[len(root_dir):].strip("/")
                # A package folder (with an init file) and anything more than two levels down is skipped.
                if rel.count("/") >= 2 or "__init__.py" in files:
                    dirs[:] = []
                    if "__init__.py" in files:
                        continue
                dirs[:] = [d for d in dirs if not d.startswith(".") and d.lower() not in LIB_DIRS]
                for f in files:
                    if f.lower().endswith(".py") and not f.startswith("_"):
                        out.append((rel + "/" + f) if rel else f)
        return sorted(out, key=lambda s: s.lower())

    def saved_list(cat):
        """Return the names for a menu list: macros, scripts or dress outfits."""
        if cat == "macro":
            return ClientUI.macro_names()
        if cat == "script":
            return script_names()
        return list(API.GetAvailableDressOutfits() or [])

    TEXT_HINT = {"macro": "The name of a macro from TazUO's macro window",
                 "script": "The script's file name (heal.py, or Spells/Bless.py)",
                 "dress": "An outfit name from TazUO's dress agent",
                 "undress": "An outfit name from TazUO's dress agent", "say": "The text to say in game",
                 "hotkey": "A key or combination (F5, CTRL+Q, SHIFT+F2; blank = none)",
                 "lo": "The counter turns red at this many or fewer (0 = only when none)"}

    def _cell_rect(info):
        """Return the screen box (x, y, w, h) of a drawn cell, or None when the bar is not up."""
        at = Kit.pos(win["g"]) if Kit.is_open(win["g"]) and info is not None else None
        return None if at is None else (at[0] + info["x"], at[1] + info["y"], info["w"], info["h"])

    def menu_place(w, h):
        """Return where the cell menu goes: where the player left it, else below the cell, kept on screen."""
        a = menu.get("anchor")
        if menu.get("moved") is not None:
            x, y = menu["moved"]
        elif a is None:
            x, y = 300, 300
        else:
            ax, ay, _, ah = a
            x, y = ax, ay + ah + 2
        W, H = Kit.screen()
        if W and H:
            if a is not None and menu.get("moved") is None and y + h > H:
                y = ay - 2 - h
            x, y = max(0, min(x, W - w)), max(0, min(y, H - h))
        return int(x), int(y)

    def close_menu():
        """Close the cell menu."""
        g, menu["g"] = menu["g"], None
        menu["c"] = {}
        Kit.dispose(g)

    def menu_disposed(g):
        """Return a dispose handler that forgets the menu when its own gump is closed."""
        def handler(*args):
            """Clear the menu state if the closed gump is still the current menu."""
            if menu["g"] is g:
                menu["g"] = None
                menu["c"] = {}

        return handler

    def open_menu(ref, bag=None):
        """Open the cell menu for a cell ref, or for a bag slot when ref is None."""
        menu.update({"ref": ref, "bag": bag, "level": "cats" if ref else "bag", "cat": None,
                     "page": 0, "moved": None, "placed": None,
                     "anchor": _cell_rect(win["cells"].get(ref) if ref else win["bags"].get(bag))})
        build_menu()

    def in_pages(rows):
        """Split menu rows into pages of one screenful."""
        return [rows[i:i + MENU_ROWS * MENU_COLS] for i in range(0, len(rows), MENU_ROWS * MENU_COLS)]

    def menu_entries():
        """Return (rows, paging) for the menu's current level.

        Each row is (caption, action) and an action of None is a divider. Levels: bag slot, category
        list, travel method, and item lists (spells by school, skills, abilities, destinations, saved
        names, windows). paging is (title, page index, page count) or None.
        """
        lvl, cat = menu["level"], menu["cat"]
        # Level "bag": menu of a bag slot.
        if lvl == "bag":
            i = menu["bag"]
            rows = []
            if settings["bagmode"] == 1:
                rows += [("Pick a bag...", ("pickbag", i)), ("Clear this slot", ("clearbag", i))]
            elif settings["bagmode"] == 0:
                s = ub_state()
                if s in ("collapsed", "docked"):
                    rows.append(("Show the Bags window", ("ub", "show")))
                elif s == "open":
                    rows.append(("Fold the Bags window into the bar", ("ub", "dock")))
                else:
                    rows.append(("Turn Bags on", ("ub", "on")))
                if UB_MODULE_KEY in HOST.by_key:
                    rows.append(("Bags settings", ("ub", "settings")))
            else:
                b = bag_at(i)
                rows.append(("Open %s" % b["n"] if b else "No bag here", ("bag", i)))
            rows.append(("Hotkey: %s" % (bag_keys()[i] or "none"), ("bagbind", i)))
            rows.append(("Bag slots: " + BAG_MODES[settings["bagmode"]], ("bagmode", None)))
            return rows, None
        # Level "cats": menu of the types a cell can hold.
        if lvl == "cats":
            c = cell(menu["ref"])
            rows = [(cap, ("cat", key)) for key, cap in CATS]
            tg = {"self": "self", "last": "last target"}.get(c["tg"], "none")
            rows += [("-", None), ("Hotkey: %s" % (c["k"] or "none"), ("cat", "hotkey")),
                     ("Press a key for it", ("bindsel", None)), ("Then target: %s" % tg, ("target", None))]
            if c["t"] in ("item", "travel"):
                rows.append(("Red at: %d or fewer" % max(0, c["lo"]), ("cat", "lo")))
            rows += [("Clear cell", ("clear", None)), ("More on the settings page", ("settings", None))]
            return rows, None
        if lvl == "method":
            return [(cap, ("tset", m)) for m, cap in TRAVEL_WAYS], None
        if lvl == "list":
            if cat == "spell":
                pages = [[(n, ("set", ("spell", n))) for n in names.split("|")] for _, names in SPELL_SCHOOLS]
                titles = SCHOOL_NAMES
            elif cat == "skill":
                pages, titles = [[(n, ("set", ("skill", n))) for n in SKILLS]], ["Skills"]
            elif cat == "ability":
                pages, titles = [[("Primary ability", ("set", ("ability", "primary"))),
                                  ("Secondary ability", ("set", ("ability", "secondary")))]], ["Weapon ability"]
            elif cat == "travel":
                if HOST.services.get("grimoire.destinations") is None:
                    rows = [("Grimoire is off: click to turn it on", ("grimon", None))]
                elif not menu["items"]:
                    rows = [("No runebook read yet: open Grimoire's runebook tabs", ("none", None))]
                else:
                    rows = [(fit("%s  (%s)" % (d["name"], d["book_name"]), 260), ("tdest", i))
                            for i, d in enumerate(menu["items"])]
                pages = in_pages(rows)
                titles = ["Runebook destinations"] * len(pages)
            elif cat in LIST_TITLES:
                rows = [(fit(n, 220), ("set", (cat, n))) for n in menu["items"]]
                if not rows:
                    rows = [("Nothing saved in TazUO yet", ("none", None))]
                rows.append(("Type a name", ("typed", cat)))
                pages = in_pages(rows)
                titles = [LIST_TITLES[cat]] * len(pages)
            else:
                pages = [[(d[1], ("set", ("ui", d[0]))) for d in UI_ACTIONS]]
                titles = ["Client windows"]
                mods = [(d[1], ("set", ("ui", d[0]))) for d in mod_actions()]
                if mods:
                    pages.append(mods)
                    titles.append("Module windows")
            p = max(0, min(len(pages) - 1, menu["page"]))
            menu["page"] = p
            return pages[p], (titles[p], p, len(pages))
        return [], None

    def build_menu():
        """Draw the cell menu on the client thread."""
        Kit.on_client(_build_menu_now)

    def _build_menu_now():
        """Draw the cell menu in one go: title, close and back buttons, the rows in columns, paging.

        Keeps the place the player dragged it to and marks the entry the cell already holds.
        """
        old = menu["g"]
        pos = Kit.pos(old) if Kit.is_open(old) else None
        if pos is not None and menu.get("placed") is not None and pos != menu["placed"]:
            menu["moved"] = pos
        menu["g"], menu["stale"] = None, old
        store, c = ({}, {}), {}
        M, GAP = Kit.MARGIN, Kit.GAP
        rows, paged = menu_entries()
        lvl, ref = menu["level"], menu["ref"]
        if lvl == "bag":
            title = "BAG SLOT %d" % (menu["bag"] + 1)
        elif lvl == "method":
            title = "TRAVEL TO %s" % str((menu.get("dest") or {}).get("name", "?")).upper()
        elif lvl in ("list", "text"):
            cap = MENU_CAPS.get(menu["cat"], "Hotkey")
            title = "%s: %s" % (ref_name(ref).upper(), cap.replace("...", "").upper())
        else:
            title = "SET " + ref_name(ref).upper()
        tw = Kit.text_w(title) + 60
        if lvl == "text":
            w = max(tw, 340)
            body_h = 92
        else:
            ncol = max(1, min(MENU_COLS, (len(rows) + MENU_ROWS - 1) // MENU_ROWS))
            nrow = (len(rows) + ncol - 1) // ncol if rows else 1
            col_w = max([Kit.text_w(r[0]) for r in rows] + [100]) + 24
            w = max(tw, 2 * M + 16 + ncol * col_w)
            body_h = 10 + nrow * MENU_ROW_H + (34 if paged else 10)
        IW = w - 2 * M
        h = M + 30 + GAP + body_h + M
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, w, h, corners=False)
        Kit.add_section(g, M, M, IW, 30)
        Kit.add_label(g, title, M + 10, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 34, M + 4, None, "Close the menu",
                       on_click=queue(("mpick", "close", None)))
        if lvl not in ("cats", "bag"):
            Kit.art_button(g, store, "back", Kit.ART_RESTORE, w - M - 54, M + 7, None, "Back to the previous menu",
                           on_click=queue(("mpick", "back", None)))
        yb = M + 30 + GAP
        Kit.add_section(g, M, yb, IW, body_h)
        if lvl == "text":
            cur = cell(ref)
            if menu["cat"] == "lo":
                val = str(max(0, cur["lo"]))
            else:
                val = cur["k"] if menu["cat"] == "hotkey" else (cur["v"] if cur["t"] == menu["cat"] else "")
            Kit.add_label(g, TEXT_HINT.get(menu["cat"], ""), M + 10, yb + 8, Kit.HUE_INFO)
            c["text"] = Kit.add_textbox(g, val, M + 10, yb + 32, IW - 20, numbers=False)
            Kit.art_button(g, store, "ok", Kit.ART_OK, M + 10, yb + 62, "Apply", "Save this value on the cell",
                           on_click=queue(("mpick", "text", None)))
            c["status"] = Kit.add_label(g, "", M + 10 + 35 + Kit.text_w("Apply") + 12, yb + 65, Kit.HUE_INFO)
        else:
            for i, (cap, action) in enumerate(rows):
                col, row = divmod(i, nrow)
                x = M + 8 + col * col_w
                y = yb + 6 + row * MENU_ROW_H
                if action is None:
                    Kit.add_tiled(g, Kit.STONE_TILE, x, y + MENU_ROW_H // 2, col_w - 16, 1)
                    continue
                # The entry the cell already holds is shown in the good colour.
                now = action[0] == "set" and (cell(ref)["t"], cell(ref)["v"]) == action[1] \
                    or action[0] in ("tdest", "tset") and travel_now(ref, action)
                Kit.add_label(g, cap, x + 4, y + 2, Kit.HUE_GOOD if now else Kit.HUE_TEXT)
                Kit.catcher(g, x, y, col_w - 8, MENU_ROW_H, queue(("mpick",) + tuple(action)), cap)
            if paged:
                name, p, n = paged
                py = yb + body_h - 28
                Kit.add_label(g, "%s  (%d of %d)" % (name, p + 1, n), M + 10, py + 4, Kit.HUE_INFO)
                if n > 1:
                    Kit.art_button(g, store, "next", Kit.ART_PAGE, w - M - 44, py, None,
                                   "Next page", on_click=queue(("mpick", "page", 1)))
                    Kit.art_button(g, store, "prev", Kit.ART_PAGE, w - M - 84, py, None,
                                   "Previous page", on_click=queue(("mpick", "page", -1)))
        x, y = menu_place(w, h)
        x, y = Kit.place(g, x, y, w, h)
        menu.update({"g": g, "c": c, "placed": (x, y)})
        G.AddControlOnDisposed(g, menu_disposed(g))
        G.AddGump(g)
        g.SetInScreen()
        Kit.dispose(menu.pop("stale", None))

    def set_cell(ref, t, v):
        """Set a cell to a type and value, keeping its key, target and red-at value."""
        cur = cell(ref)
        new = dict(blank(), t=t, v=v, k=cur["k"], tg=cur["tg"], lo=cur["lo"])
        cells[ref[0]][ref[1]] = new
        cells_changed(recount=True, refs=[ref])
        say("%s set on %s." % (cell_text(new), ref_name(ref)), Kit.HUE_GOOD)

    def travel_now(ref, action):
        """Return whether a travel menu row is the one the cell already uses."""
        c = cell(ref)
        if c["t"] != "travel":
            return False
        if action[0] == "tdest":
            items = menu["items"]
            d = items[action[1]] if 0 <= action[1] < len(items) else None
        else:
            d = menu.get("dest")
            if c.get("rm") != action[1]:
                return False
        if not d:
            return False
        try:
            return (int(c.get("rb") or "0", 16) == int(d["book"]) and c.get("ri") == str(int(d["index"])))
        except (ValueError, TypeError, KeyError):
            return False

    def menu_to(**kw):
        """Change the menu state and redraw it."""
        menu.update(kw)
        build_menu()

    def menu_pick(what, arg):
        """Act on a menu click (client tick).

        what and arg come from the clicked row's action. Actions that finish with the menu close it first;
        then the handler for what in MENU_ACTS runs with the cell the menu is open on (ref) and arg.
        """
        ref = menu["ref"]
        # Actions that finish with the menu close it first.
        if what in ("close", "bindsel", "bagbind", "set", "settings", "pickbag", "clearbag",
                    "ub", "bag", "bagmode", "tset", "grimon") or (what, arg) == ("cat", "item"):
            close_menu()
        # The state-free actions are lambdas in MENU_ACTS; the ones that read or change the menu state have
        # their own menu_* function above it.
        if what in MENU_ACTS:
            MENU_ACTS[what](ref, arg)

    def menu_back(ref, arg):
        """Back one level: from the travel method choice to the destination list, otherwise to the categories."""
        if menu["level"] == "method":
            menu_to(level="list", cat="travel")
        else:
            menu_to(level="cats", cat=None, page=0)

    def menu_cat(ref, arg):
        """A category was picked: open its list, a typed-value page, or the item picker.

        Lists kept in saved data are fetched on the script thread (when called from the client thread) so
        the tick never waits for them.
        """
        if arg == "travel":
            fn = HOST.services.get("grimoire.destinations")
            menu_to(items=list(safe(fn, []) or []) if fn is not None else [], level="list", cat="travel", page=0)
            return
        if arg == "item":
            pick_item(ref)
            return
        if arg in LIST_TITLES and Client.on_client_thread():
            def job():
                """Fetch the saved list on the script thread and then show it, if the menu is still wanted."""
                items = saved_list(arg)
                if menu["ref"] == ref and menu["level"] == "cats" and Kit.is_open(menu["g"]):
                    menu_to(items=items, level="list", cat=arg, page=0)

            later(job)
            return
        if arg in ("spell", "skill", "ability", "ui", "macro", "script", "dress", "undress"):
            menu_to(items=saved_list(arg) if arg in LIST_TITLES else [], level="list", cat=arg, page=0)
            return
        menu_to(level="text", cat=arg)

    def menu_tdest(ref, arg):
        """A travel destination was picked from the list: go on to choosing how to travel there."""
        if menu["level"] == "list" and menu["cat"] == "travel" and 0 <= arg < len(menu["items"]):
            menu_to(level="method", dest=menu["items"][arg])

    def menu_tset(ref, arg):
        """A travel method was picked: save it, with the destination chosen before, on the cell."""
        if menu.get("dest") and ref is not None:
            set_travel(ref, menu["dest"], arg)

    def menu_text(ref, arg):
        """The Set button of a typed page: apply the text as a hotkey, a red-at value or the cell's value.

        A bad entry (a key another cell owns, not a number, empty) says why in the menu's status line and
        keeps the menu open.
        """
        v = str(menu["c"]["text"].Text or "").strip()
        if menu["cat"] == "hotkey":
            k = _norm_key(v)
            owner = key_owner(k)
            if owner:
                Kit.set_text(menu["c"]["status"], "%s belongs to %s" % (k, owner), Kit.HUE_BAD)
                return
            if k:
                assign_key(ref, k)
            else:
                cell(ref)["k"] = ""
                cells_changed(refs=[ref])
            close_menu()
            return
        if menu["cat"] == "lo":
            try:
                lo = int(v)
            except ValueError:
                Kit.set_text(menu["c"]["status"], "Type a number", Kit.HUE_BAD)
                return
            cell(ref)["lo"] = max(0, lo)
            cells_changed(refs=[ref])
            close_menu()
            return
        if not v:
            Kit.set_text(menu["c"]["status"], "Type a value first", Kit.HUE_BAD)
        else:
            close_menu()
            set_cell(ref, menu["cat"], v)

    def menu_target(ref, arg):
        """Cycle who the cell's action is aimed at (nobody, self, last target) and redraw the menu."""
        c = cell(ref)
        c["tg"] = {"": "self", "self": "last", "last": ""}.get(c["tg"], "")
        save_cells()
        want_redraw([ref])
        HOST.refresh_settings(KEY)
        build_menu()

    def menu_clear(ref, arg):
        """Empty the cell and close the menu."""
        clear_cell(ref)
        close_menu()

    def menu_settings(ref, arg):
        """Show this module's settings page with the cell selected."""
        page["sel"] = ref_sel(ref)
        HOST.show_settings(KEY)
        HOST.refresh_settings(KEY)

    def menu_clearbag(ref, arg):
        """Forget the bag picked for a slot and ask for a new bag scan at once."""
        set_picked_bag(arg, 0)
        st["next_scan"] = 0.0

    def menu_ub(ref, arg):
        """A Bags module button of the menu: open its settings, turn it on, or send it the command in arg."""
        if arg == "settings":
            if UB_MODULE_KEY in HOST.by_key:
                HOST.show_settings(UB_MODULE_KEY)
        elif arg == "on":
            turn_on(UB_MODULE_KEY, "Bags")
        else:
            heartbeat()
            ub_send(arg)

    # Menu actions that need no extra state.
    # The table maps a menu action name to its handler, called as handler(ref, arg).
    MENU_ACTS = {"bindsel": lambda ref, arg: start_bind(ref), "bagbind": lambda ref, arg: start_bind(("b", arg)),
                 "set": lambda ref, arg: set_cell(ref, arg[0], arg[1]), "pickbag": lambda ref, arg: pick_bag(arg),
                 "bag": lambda ref, arg: on_bag_click(arg), "bagmode": lambda ref, arg: HOST.show_settings(KEY),
                 "grimon": lambda ref, arg: turn_on(GRIM_MODULE_KEY, "Grimoire"),
                 "page": lambda ref, arg: menu_to(page=menu["page"] + arg), "back": menu_back, "cat": menu_cat,
                 "tdest": menu_tdest, "tset": menu_tset, "typed": lambda ref, arg: menu_to(level="text", cat=arg),
                 "text": menu_text, "target": menu_target, "clear": menu_clear, "settings": menu_settings,
                 "clearbag": menu_clearbag, "ub": menu_ub}

    def use(ref):
        """Use a cell or a bag slot as if it was clicked."""
        if ref[0] == "b":
            on_bag_click(ref[1])
        else:
            run_cell(ref)

    def use_now(ref):
        """Use a cell or bag slot, reporting a failure instead of raising."""
        try:
            use(ref)
        except Exception as ex:
            say("couldn't use %s (%s)." % (ref_name(ref), ex), Kit.HUE_BAD)

    # Direct hotkey state: whether the key event works, keys held, key map and hooks.
    _hk = {"ok": None, "held": {}, "map": {}, "hooks": None}

    def sdl_combo(k):
        """Turn a key name into the SDL key combination text the client's key event uses."""
        parts, key = _norm_key(k).split("+"), None
        for p in parts:
            if p and p not in ("CTRL", "SHIFT", "ALT"):
                key = p if p.startswith("SDLK_") else "SDLK_" + p
        mods = [m for m in ("CTRL", "SHIFT", "ALT") if m in parts]
        return "+".join(mods + ([key] if key else []))

    def legion_combo(sdl):
        """Turn an SDL combination text back into the key names used elsewhere."""
        return "+".join(p[5:] if p.startswith("SDLK_") else p for p in str(sdl).upper().split("+"))

    def direct_ok(ref):
        """Return whether a cell is safe to use straight from the key event on the client thread.

        Cells that need the script thread (scripts, window buttons that wait) are left to the queue.
        """
        if ref[0] == "b":
            return (st["bind"] is None and bag_at(ref[1]) is not None and
                    (settings["bagmode"] != 0 or st["ub_state"] is not None))
        c = cell(ref)
        if c["t"] == "ui":
            d = ui_def(c["v"])
            how = d[3] if d else ""
            return (how in ("war", "help", "quests", "paperdoll", "lock", "minimize") or
                    how.startswith(("ga:", "macro:")))
        return c["t"] in ("item", "spell", "skill", "ability", "macro", "say", "dress", "undress", "travel")

    def _hk_down(combo):
        """Client key event handler: act on the hotkey the moment it is pressed.

        Ignores key repeat (a key held down is not pressed again for a while). In keybind mode the key
        is queued for the binding; otherwise a bound cell is used directly when direct_ok allows.
        """
        try:
            if not _hk["ok"]:
                return
            combo = str(combo)
            base = combo.rsplit("+", 1)[-1]
            now, held = time.time(), _hk["held"]
            at = held.get(base)
            held[base] = now
            # Held keys are ignored until they have been up for a moment.
            if at is not None and now - at < HELD_KEY_STALE:
                return
            # Forget stale held keys now and then so the table stays small.
            if len(held) > 32:
                for k in [k for k, t in held.items() if now - t >= HELD_KEY_STALE]:
                    del held[k]
            if st["shutting"] or win["g"] is None:
                return
            if st["bind"] is not None:
                if not HOST.typing():
                    queue.add(("bindkey", legion_combo(combo)), dup=True)
                    HOST.poke()
                return
            ref = _hk["map"].get(combo)
            if ref is None or HOST.typing():
                return
            if direct_ok(ref):
                use_now(ref)
            else:
                queue.add(("use", ref), dup=True)
                HOST.poke()
        except Exception:
            pass

    def _hk_up(combo):
        """Client key-up handler: forget the key as held."""
        try:
            _hk["held"].pop(str(combo).rsplit("+", 1)[-1], None)
        except Exception:
            pass

    def _hk_install():
        """Hook the client's key down and key up events once; hotkeys are off when this fails.

        Reads the client's Keyboard events by reflection and says so when it cannot, so the failure is
        never silent.
        """
        if _hk["ok"] is not None:
            return
        _hk["ok"] = False
        try:
            # Both events are hooked or neither is; a half hook is removed again.
            import clr
            import System
            from System.Reflection import BindingFlags
            flags = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
            kb = Client._type("ClassicUO.Input.Keyboard")
            evd, evu = kb.GetEvent("KeyDownEvent", flags), kb.GetEvent("KeyUpEvent", flags)
            dd = clr.GetPythonType(evd.EventHandlerType)(_hk_down)
            du = clr.GetPythonType(evu.EventHandlerType)(_hk_up)
            evd.GetAddMethod(True).Invoke(None, System.Array[object]([dd]))
            try:
                evu.GetAddMethod(True).Invoke(None, System.Array[object]([du]))
            except Exception:
                evd.GetRemoveMethod(True).Invoke(None, System.Array[object]([dd]))
                raise
            _hk.update({"hooks": (evd, dd, evu, du), "ok": True, "held": {}})
        except Exception as ex:
            say("couldn't read the keyboard, so cell hotkeys are off (%s)." % ex, Kit.HUE_BAD)

    def _hk_remove():
        """Remove the key event hooks and clear the key map."""
        hooks, _hk["hooks"] = _hk["hooks"], None
        _hk["ok"] = None if hooks else _hk["ok"]
        _hk["map"] = {}
        if not hooks:
            return
        import System
        evd, dd, evu, du = hooks
        safe(lambda: evd.GetRemoveMethod(True).Invoke(None, System.Array[object]([dd])))
        safe(lambda: evu.GetRemoveMethod(True).Invoke(None, System.Array[object]([du])))

    _told = set()

    def tell_once(what, text):
        """Say a problem once per kind (a key conflict is not repeated every time the keys register)."""
        if what not in _told:
            _told.add(what)
            say(text, Kit.HUE_BAD)

    def register_hotkeys():
        """Rebuild the key map from the cells and bag slots that have a hotkey.

        Skips keys another module owns and empty or hidden cells; when two cells share a key the later
        one gets it. The map is keyed by the client's own combination text.
        """
        seen = {}
        for r, c in all_cells():
            k = _norm_key(c["k"])
            if not k or not c["t"] or not shown(r):
                continue
            owner = key_owner(k)
            if owner:
                tell_once((k, owner), "%s belongs to %s; %s has no hotkey." % (k, owner, ref_name(r)))
                continue
            if k in seen:
                tell_once((k, "two cells"), "%s is on two cells; %s gets it." % (k, ref_name(r)))
            seen[k] = r
        for i, k in enumerate(bag_keys()):
            if k and not key_owner(k):
                seen[k] = ("b", i)
        # The map holds nothing until the key hook works.
        _hk["map"] = dict((sdl_combo(k), ref) for k, ref in seen.items()) if _hk["ok"] else {}

    # Queued action kinds and their handlers.
    ACTIONS = {"click": on_cell_click, "use": use, "bag": on_bag_click, "ui": run_ui,
               "pick": pick_item, "menu": open_menu, "mpick": menu_pick,
               "picked_item": picked_item, "picked_bag": picked_bag,
               "bindkey": on_bind_key, "lockbar": toggle_lock, "grid": toggle_grid,
               "bagmenu": lambda i: open_menu(None, i), "page": lambda step: set_page(settings["page"] + step),
               "bind": lambda: start_bind() if st["bind"] is None else end_bind()}

    def page_table(w):
        """Return the settings page layout for width w: the BAR options, EDIT A CELL and HOW TO USE."""
        col = (w - 24) // 3
        hint = Kit.wrap("Value: a spell, skill, macro or outfit name, primary or secondary, a script file, text to "
                        "say, or an item graphic (0x0E21, or 0x0E21,1153 with a hue).", w - 24)[:3]
        return (("BAR", (("check", "lock", "Lock in place", "Keep the bar where it is (unlocked: drag its stone edge)",
                     {"stay": True}), ("check", "top", "Show the top row", "Show the 24-cell row above the bottom row",
                     {"stay": True, "dx": 12 + col}),
                    ("check", "keys", "Show hotkeys", "Show each cell's hotkey in its corner", {"dx": 12 + 2 * col}),
                    ("check", "short", "Short counts", "Show 1200 as 1.2k on the counters", {"stay": True}),
                    ("check", "hue", "Count same hue only", "Count only items of the cell's hue",
                     {"stay": True, "dx": 12 + col}), ("custom", 28, draw_ub_state),
                    ("slider", "slot", "Cell size:", "Cell side in pixels (%d-%d)" % (SLOT_MIN, SLOT_MAX), SLOT_MIN,
                     SLOT_MAX, {"sw": 120, "vfmt": "%d px", "stay": True}),
                    ("custom", 26, draw_bag_mode), ("custom", 26, draw_page_buttons),
                    ("slider", "scale", "Scale:", "Size of the whole bar (%d-%d%%); text keeps its size"
                     % (SCALE_MIN, SCALE_MAX), SCALE_MIN, SCALE_MAX, {"sw": 160, "vfmt": "%d%%"}),
                    ("slider", "extra", "Extra rows:", "Rows of %d cells above the top row (0-%d); hidden rows' "
                     "hotkeys are off" % (TOP_SLOTS, EXTRA_ROWS), 0, EXTRA_ROWS,
                     {"sw": 100, "vfmt": "%d", "stay": True}), ("custom", 26, draw_anchor)),
                 {"ldy": 2, "sdy": 6, "lgap": 8, "ugap": 10, "fh": 26, "pad": 6}),
                ("EDIT A CELL", [("custom", 128, draw_edit)] + [("note", line) for line in hint]),
                ("HOW TO USE", [("note", line) for para in HELP for line in Kit.wrap(para, w - 24)]))

    def buttons(f, by, specs):
        """Draw a row of art buttons at y inside the settings page; return the x after the last one."""
        return Kit.buttons(f.g, f.store, f.x + 12, by, specs, 16)

    def drop_down(f, lx, ry, label, key, dw, pairs, value, tooltip):
        """Queue a drop-down to be added after the page is drawn; return the x for the next control."""
        Kit.add_label(f.g, label, lx, ry + 2)
        codes = [p[0] for p in pairs]
        page["dds"].append((key, lx + Kit.text_w(label) + 8, ry, dw, [p[1] for p in pairs],
                            codes.index(value) if value in codes else 0, tooltip))
        return lx + Kit.text_w(label) + 8 + dw + 16

    def draw_ub_state(f, x, y):
        """Settings page: show the Bags window state beside the options."""
        found = st["ub_found"]
        state = ub_state()
        ub = ({"open": "Bags: shown", "collapsed": "Bags: folded",
               "docked": "Bags: in the bar"}.get(state) if state else "Bags: off" if found else
              "Bags: not found" if found is False else "Bags: not in use")
        found = found or state is not None
        col = (f.w - 24) // 3
        Kit.add_label(f.g, fit(ub, col - 6), x + 12 + 2 * col, y + 2, Kit.HUE_GOOD if found else Kit.HUE_INFO)

    def draw_bag_mode(f, x, y):
        """Settings page: the Bag slots drop-down."""
        drop_down(f, x + f.w - 12 - 170 - 8 - Kit.text_w("Bag slots:"), y, "Bag slots:", "bagmode", 170,
                  list(enumerate(BAG_MODES)), settings["bagmode"],
                  "Where the bag slots get bags: Inventory > Bags, bags you target, or your backpack and its bags")

    def draw_page_buttons(f, x, y):
        """Settings page: the Prev, Next and Keybind mode buttons and the page number."""
        bx = buttons(f, y, (("pgprev", Kit.ART_PAGE, "Prev", "Show the previous bottom-left page"),
                            ("pgnext", Kit.ART_PAGE, "Next", "Show the next bottom-left page"),
                            ("bind", Kit.ART_PLAY, "Keybind mode", "Start keybind mode: hover a cell and press a key")))
        Kit.add_label(f.g, fit("Bar page %d of %d" % (settings["page"] + 1, PAGES), x + f.w - 16 - bx), bx, y + 3,
                      Kit.HUE_INFO)

    def draw_anchor(f, x, y):
        """Settings page: say where the bar is anchored."""
        sx = x + 12 + Kit.text_w("Extra rows:") + 8
        anch = settings["anchor"]
        where = {"": "none (drop near a corner or edge middle)", "L": "left edge, upright", "R": "right edge, upright",
                 "T": "top edge", "B": "bottom edge", "C": "screen centre"}.get(
            anch, {"TL": "top-left", "TR": "top-right", "BL": "bottom-left",
                   "BR": "bottom-right"}.get(anch, anch) + " corner")
        Kit.add_label(f.g, fit("Anchor: %s" % where, x + f.w - 16 - (sx + 130)), sx + 130, y + 2, Kit.HUE_INFO)

    def draw_edit(f, x, y):
        """Settings page: the cell editor (cell, type, target, value, window, hotkey, red-at, buttons)."""
        g, c, w = f.g, f.c, f.w
        sel = page["sel"]
        cur = cell(sel_ref(sel))
        lx = drop_down(f, x + 12, y, "Cell:", "sel", 120, list(enumerate(sel_names())), sel,
                       "The cell to edit (right-clicking a cell on the bar does the same)")
        lx = drop_down(f, lx, y, "Does:", "does", 150, TYPES, cur["t"], "What a click or the hotkey does")
        drop_down(f, lx, y, "Target:", "target", 100, TARGETS, cur["tg"],
                  "Answer the cell's target cursor with yourself or your last target (when no other module holds it)")
        Kit.add_label(g, "Value:", x + 12, y + 34)
        if cur["t"] == "item":
            val = ("0x%04X" % cur["g"]) + ((",%d" % cur["h"]) if cur["h"] else "")
        elif cur["t"] == "ui":
            val = ""
        elif cur["t"] == "travel":
            val = travel_what(cur)
        else:
            val = cur["v"]
        vx = x + 12 + max(Kit.text_w("Value:"), Kit.text_w("Window:")) + 8
        c["value"] = Kit.with_tip(Kit.add_textbox(g, val, vx, y + 32, x + w - 16 - vx, numbers=False),
                                  "The cell's value (see below; a Client window cell uses Window)")
        Kit.add_label(g, "Window:", x + 12, y + 66)
        ua = ui_all()
        uids = [d[0] for d in ua]
        page["dds"].append(("window", vx, y + 64, 140, [d[1] for d in ua],
                            uids.index(cur["v"]) if cur["t"] == "ui" and cur["v"] in uids else 0,
                            "The client or module window a Client window cell opens"))
        lx = vx + 140 + 16
        for key, label, text, fw, numbers, tip in (
                ("key", "Hotkey:", cur["k"], 100, False, TEXT_HINT["hotkey"] + "; or use Keybind mode"),
                ("lo", "Red at:", str(cur["lo"]), 40, True, TEXT_HINT["lo"])):
            Kit.add_label(g, label, lx, y + 66)
            c[key] = Kit.with_tip(Kit.add_textbox(g, text, lx + Kit.text_w(label) + 8, y + 64, fw, numbers=numbers),
                                  tip)
            lx += Kit.text_w(label) + 8 + fw + 16
        bx = buttons(f, y + 96, (("apply", Kit.ART_OK, "Apply", "Save this cell"),
                                 ("pick", Kit.ART_PLAY, "Pick item...", "Target an item for this cell"),
                                 ("clear", Kit.ART_CLOSE, "Clear", "Empty this cell")))
        c["status"] = Kit.add_label(g, "", bx, y + 99, Kit.HUE_INFO)

    def build_config(g, x, y, w):
        """Build the settings page and place its drop-downs on top of the other controls.

        Drop-downs are added last, from the lowest on the page up, so open lists overlap what is below.
        """
        if not cells["a"]:
            load_cells()
        page["dds"] = []
        f = cfg.build(g, x, y, w)
        for key, dx, dy, dw, items, idx, tooltip in sorted(page["dds"], key=lambda d: -d[2]):
            dd = G.CreateDropDown(dw, items, idx)
            dd.SetPos(dx, dy)
            g.Add(dd)
            f.c[key] = Kit.with_tip(dd, tooltip)
        page.update({"seen_sel": page["sel"], "seen_bag": settings["bagmode"]})

    def set_status(text, hue=None):
        """Show a line of status text on the settings page when it is open."""
        if cfg.f is not None:
            Kit.set_text(cfg.f.c["status"], text, Kit.HUE_INFO if hue is None else hue)

    def apply_edit():
        """Apply the cell editor's values to the selected cell after checking them.

        Item cells need a graphic, travel cells keep their destination (it is only picked from the
        menu), and a hotkey held by another module is refused.
        """
        c = cfg.f.c
        ref = sel_ref(page["sel"])
        cur = cell(ref)

        def chosen(lst, dd):
            """Return the code of the entry a drop-down shows."""
            return lst[max(0, min(len(lst) - 1, Kit.dd_index(dd, 0)))][0]

        t = chosen(TYPES, c["does"])
        v = str(c["value"].Text or "").strip()
        tg = chosen(TARGETS, c["target"])
        k = _norm_key(c["key"].Text)
        owner = key_owner(k)
        if owner:
            set_status("%s belongs to %s" % (k, owner), Kit.HUE_BAD)
            return
        try:
            lo = int(str(c["lo"].Text or "0"))
        except Exception:
            lo = LOW_DEFAULT
        new = dict(blank(), t=t, tg=tg, k=k, lo=lo)
        if t == "item":
            gh = parse_graphic(v)
            if gh is None and cur["t"] == "item" and cur["g"]:
                gh = (cur["g"], cur["h"])
            if gh is None:
                set_status("Pick an item, or type its graphic", Kit.HUE_BAD)
                return
            new.update({"g": gh[0], "h": gh[1], "n": cur["n"] if (cur["g"], cur["h"]) == gh else "0x%04X" % gh[0]})
        elif t == "ui":
            new["v"] = chosen(ui_all(), c["window"])
        elif t == "ability":
            new["v"] = "secondary" if v.lower().startswith("s") else "primary"
        elif t == "travel":
            if cur["t"] != "travel":
                set_status("Pick its destination: right-click the cell, then Travel (runebook)", Kit.HUE_BAD)
                return
            new["tg"] = ""
            for k in ("v", "n") + TRAVEL_KEYS:
                new[k] = cur.get(k, "")
        elif t:
            if not v:
                set_status("Type a value first", Kit.HUE_BAD)
                return
            new["v"] = v
        cells[ref[0]][ref[1]] = new
        if new["k"] and new["k"] != _norm_key(cur["k"]):
            assign_key(ref, new["k"])
        cells_changed(recount=True, refresh=False, refs=[ref])
        set_status("Saved %s" % ref_name(ref), Kit.HUE_GOOD)

    def page_clicks(f):
        """Act on the settings page's button clicks."""
        for key, action in (("pgprev", ("page", -1)), ("pgnext", ("page", 1)), ("bind", ("bind",))):
            if Kit.was_clicked(f.store, key):
                queue(action)()
        if Kit.was_clicked(f.store, "apply"):
            apply_edit()
        if Kit.was_clicked(f.store, "pick"):
            queue(("pick", sel_ref(page["sel"])))()
            set_status("Target the item")
        if Kit.was_clicked(f.store, "clear"):
            clear_cell(sel_ref(page["sel"]))

    def read_dropdowns(f, new):
        """Read the Bag slots and Cell drop-downs, which the page does not read by itself."""
        bm = Kit.dd_index(f.c["bagmode"], settings["bagmode"])
        if bm != page["seen_bag"] and 0 <= bm < len(BAG_MODES):
            page["seen_bag"] = new["bagmode"] = bm
        sel = Kit.dd_index(f.c["sel"], page["sel"])
        if sel != page["seen_sel"] and 0 <= sel < ACTION_SLOTS + UI_SLOTS + EXTRA_SLOTS:
            page["sel"] = sel
            HOST.refresh_settings(KEY)

    def settings_changed(old, new):
        """Settings changed on the page: rescan the bags when the mode changed and rebuild the bar."""
        if new["bagmode"] != old["bagmode"]:
            st["bag_sig"], st["next_scan"] = None, 0.0
        register_hotkeys()
        want_rebuild(0.4)

    # Settings page: the page definition, the hooks it calls and the poll interval.
    cfg = Kit.Page(settings, page_table, save_settings, settings_changed, adjust=read_dropdowns, clicks=page_clicks,
                   every=0.2)
    load_settings()

    def _start():
        """Start the module: load settings and cells, link to the other windows and draw the bar.

        Called by the host on the client thread (the script thread only if the client queue is out of reach).
        """
        st.update(fresh(), minimized=Kit.load_min(MIN_KEY), em=False, ub_last=None, ub_pending=True, counted_at=0.0)
        _told.clear()
        _hk["held"] = {}
        fitst.update(scale=None, vertical=None, slot=None, sig=None)
        load_settings()
        load_cells()
        scan_bags()
        st["ub_state"], st["grim_state"], st["va_state"] = ub_state(), grim_state(), va_state()
        heartbeat()
        HOST.layout_add(KEY, bar_gump, TITLE, LAYOUT_HOOKS)
        cleanup.add(HOST.layout_remove, KEY)
        st.update(dock_sig=dock_sig(), tray_sig=tray_sig(), watch_next=0.0, owned_sig=frozenset(HOST.hotkeys_owned))
        build_window()
        st.update(rebuild_at=0.0, redraw=set())
        _hk_install()
        register_hotkeys()
        cleanup.service("actionbar.hotkeys", hotkeys_service)
        cleanup.service("look.actionbar", want_rebuild)

    def _tick():
        """Host tick on the client thread: watch the other windows, run queued actions, rebuild, count.

        Order: pending target, script check, window watch, queued clicks, bag and ability scan every
        two seconds, rebuild or redraw, counters, cooldowns, and the bar's position.
        """
        if st["shutting"] or win["g"] is None:
            return
        if Kit.closed(win):
            return
        now = time.time()
        handle_target(now)
        check_script(now)
        watch_ub()
        # A minimized bar redraws when a zone starts or stops, so it takes the right shape.
        if st["minimized"] and st["em"] == Kit.zone_up(KEY) and not st["rebuild_at"]:
            want_rebuild()
        arr = HOST.layout_arranging()
        if arr != win.get("arranging", False):
            win["arranging"] = arr
            if win.get("lockbtn"):
                recolor(win["lockbtn"], *lock_look())
        # Run every queued action, stopping at once if the module was shut down by one.
        while st["queue"]:
            action = st["queue"].pop(0)
            kind = action[0]
            if kind in ACTIONS:
                ACTIONS[kind](*action[1:])
            elif kind == "dock":
                d = dict(all_docks()).get(action[1])
                if d is not None:
                    s = safe(d.get("state"))
                    if s is None:
                        if d.get("on"):
                            safe(d["on"])
                        else:
                            later(lambda k=action[1]: safe(lambda: HOST.enable(k)))
                    elif s == "open":
                        HOST.dock_to_bar(action[1])
                    else:
                        safe(d.get("show"))
                    st["dock_sig"], st["watch_next"] = None, 0.0
            elif kind == "traywin":
                settings["tray_open"] = not settings["tray_open"]
                save_settings()
                refresh_tray()
            elif kind == "toggle_min":
                if Kit.zone_up(KEY) and not st["minimized"]:
                    continue
                save_pos()
                st["minimized"] = not st["minimized"]
                Kit.save_min(MIN_KEY, st["minimized"])
                heartbeat()
                want_rebuild()
            if st["shutting"] or win["g"] is None:
                return
        now = time.time()
        # Bag, ability and heartbeat work is done every two seconds.
        if now >= st["next_scan"]:
            st["next_scan"] = now + 2.0
            scan_bags()
            scan_abilities()
            heartbeat()
            if st.get("last_pos") != st.get("pos_saved"):
                save_pos()
        if st["rebuild_at"] and now >= st["rebuild_at"]:
            st["rebuild_at"] = 0.0
            st["redraw"] = set()
            build_window()
        elif st["redraw"]:
            refresh()
        # Count on a timer, and sooner when the pack changed.
        if now >= st["next_count"] or (st.get("pack_v") is not None and now - st.get("counted_at", 0.0) >= COUNT_SOON
                                       and HOST.pack_ver() != st["pack_v"]):
            st["next_count"] = now + COUNT_EVERY
            refresh_counts()
        cool_tick(now)
        if now >= st.get("tray_next", 0.0):
            st["tray_next"] = now + 0.1
            watch_position(now)

    def _thread_tick():
        """Host script-thread tick: run the queued jobs (they may block, unlike the client tick)."""
        while st["jobs"] and not st["shutting"]:
            st["jobs"].pop(0)()

    def _stop():
        """Stop the module: close everything it opened and save its settings, cells and position."""
        st["shutting"] = True
        cleanup.close()
        drop_want()
        g, tray["g"] = tray["g"], None
        Kit.dispose(g)
        st["bind"] = None
        close_menu()
        heartbeat(False)
        _hk_remove()
        with Kit.quiet:
            Kit.on_client(save_pos)
        Kit.save_min(MIN_KEY, st["minimized"])
        save_settings()
        save_cells()
        g, win["g"] = win["g"], None
        Kit.dispose(g)
        for s in win.pop("stale", []):
            Kit.dispose(s)

    # The hooks the host calls: start, ticks, stop and the settings page.
    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": build_config, "poll_config": cfg.poll, "config_closed": cfg.closed,
            "thread_tick": _thread_tick, "thread_wanted": lambda: bool(st["jobs"])}


# Run alone, load the stand-in host first.
if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("actionbar", "Action Bar", "Cells for items, spells, skills and windows",
         _module_actionbar, 0.05, category="On screen")
