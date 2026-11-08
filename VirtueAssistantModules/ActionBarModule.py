def _module_actionbar():
    KEY = "actionbar"; TITLE = "Action Bar"; say = Kit.sayer(TITLE); TOP_SLOTS = 24; BOTTOM_SLOTS = 12; UI_SLOTS = 11
    BAG_SLOTS = 5; ACTION_SLOTS = TOP_SLOTS + BOTTOM_SLOTS; PAGES = 12; PAGE_W = 22; SLOT_MIN, SLOT_MAX = 36, 64
    SCALE_MIN, SCALE_MAX = 50, 150; BAR_M = 8; CTRL_W = 44; UI_SHARE = 0.65; UI_GAP = 4; BAG_GAP = 3; TRAY_BTN = 30
    TRAY_GAP = 4; SLOT_TILE = 2624; SLOT_ALPHA = 0.92; SLOT_FRAME = 2620; COUNT_EVERY = 0.75; HELD_KEY_STALE = 2.0
    LOW_DEFAULT = 5
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
    TRAVEL_SPELL = {"recall": "Recall", "gate": "Gate Travel", "sacred": "Sacred Journey"}; UB_MODULE_KEY = "bag"
    UB_LINK_ALIVE = "ActionBar_alive"; GRIM_MODULE_KEY = "grimoire"; GRIM_LINK_CMD = "Grimoire_cmd"
    VA_LINK_CMD = "VirtueAssistant_cmd"; SETTINGS_KEY = "ActionBar_settings"; CELLS_KEY = "ActionBar_cells"
    PAGES_KEY = "ActionBar_pages"; EXTRA_KEY = "ActionBar_extra"; EXTRA_ROWS = 4; EXTRA_SLOTS = EXTRA_ROWS * TOP_SLOTS
    POS_KEY = "ActionBar_pos"; MIN_KEY = "ActionBar_min"; MINI_W, MINI_H = 240, 46
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
    CTRL_ROW_MIN = 16; CTRL_PAD = 2
    SKILLS = ("Anatomy|Animal Lore|Animal Taming|Arms Lore|Begging|Cartography|Detect Hidden|Discordance|"
              "Evaluate Intelligence|Forensic Evaluation|Hiding|Inscription|Item Identification|Meditation|"
              "Peacemaking|Poisoning|Provocation|Remove Trap|Spirit Speak|Stealing|Stealth|Taste Identification|"
              "Tracking").split("|")
    SCHOOL_NAMES = ["Magery", "Necromancy", "Chivalry", "Bushido", "Ninjitsu", "Spellweaving", "Mysticism"]
    MENU_ROWS = 16; MENU_COLS = 4; MENU_ROW_H = 20
    TYPES = [("", "Empty"), ("item", "Item + counter"), ("spell", "Spell"),
             ("skill", "Skill"), ("macro", "TazUO macro"), ("ability", "Weapon ability"),
             ("script", "Legion script"), ("dress", "Dress outfit"),
             ("undress", "Undress outfit"), ("say", "Say text"), ("ui", "Client window"),
             ("travel", "Travel (runebook)")]
    TRAVEL_KEYS = ("rb", "ri", "rm"); TARGETS = [("", "None"), ("self", "Self"), ("last", "Last target")]
    BAG_MODES = ["Bags' slots", "Bags I pick", "Backpack + sub-bags"]
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
    settings = {"slot": 44, "top": True, "keys": True, "lock": False,
                "short": True, "hue": False, "bagmode": 0, "bags": "", "page": 0,
                "scale": 100, "tray_open": True, "bagkeys": "", "extra": 0, "anchor": "", "vertical": False}
    cells = {"a": [], "u": [], "x": [], "pages": []}
    def fresh():
        return {"shutting": False, "queue": [], "want_target": None, "next_count": 0.0, "next_scan": 0.0,
                "rebuild_at": 0.0, "bag_sig": None, "ability_sig": None, "bind": None, "jobs": [], "redraw": set(),
                "ub_job": False, "confirm": None, "cool": {"skill": 0.0, "spell": 0.0}, "cool_next": 0.0}
    st = fresh()
    st.update({"minimized": False, "ub_pending": False, "cnt": {}, "cnt_g": {}, "first": {},
               "first_g": {}, "bags": [None] * BAG_SLOTS, "ub_found": None, "ub_cache": None, "ub_state": None,
               "grim_state": None, "va_state": None, "pending_on": None, "right_ok": None, "dock_sig": None,
               "watch_next": 0.0, "script_check": None, "ub_last": None})
    win = {"g": None, "store": ({}, {}), "cells": {}, "bags": {}}; tray = {"g": None, "at": None}
    menu = {"g": None, "ref": None, "level": "cats", "cat": None, "page": 0, "c": {}, "bag": None, "items": [],
            "anchor": None, "moved": None, "placed": None}
    page = {"sel": ACTION_SLOTS - BOTTOM_SLOTS, "dds": []}
    SPELL_ICON = dict((n.lower(), base + i) for base, names in SPELL_SCHOOLS for i, n in enumerate(names.split("|")))
    def later(fn): st["jobs"].append(fn)
    def spell_icon(name):
        n = (name or "").strip().lower()
        if not n: return 0
        icon = SPELL_ICON.get(n)
        if icon is None: icon = next((v for k, v in SPELL_ICON.items() if k.startswith(n)), None)
        return icon if icon and Kit.pic_size(icon)[0] > 0 else 0
    def ability_info(which):
        names = [str(n) for n in (API.CurrentAbilityNames() or [])]; i = 1 if which == "secondary" else 0
        if len(names) <= i: return 0, ""
        name = names[i]; known = [str(n) for n in (API.KnownAbilityNames() or [])]
        if name not in known: return 0, name
        idx = known.index(name)
        if known and known[0].lower() in ("none", "invalid"): idx -= 1
        icon = 0x5200 + idx; return (icon if idx >= 0 and Kit.pic_size(icon)[0] > 0 else 0), name
    def ui_def(uid):
        if uid.startswith("mod:"): return mod_def(uid[4:])
        return next((d for d in UI_ACTIONS if d[0] == uid), None)
    def mod_def(key, docks=None):
        s = HOST.by_key.get(key)
        if s is None or key == KEY: return None
        d = (docks if docks is not None else dict(HOST.docks)).get(key)
        icon = int(d.get("icon") or 0) if d else 0; return ("mod:" + key, s.title, icon, "mod:" + key)
    def mod_actions():
        out = []; docks = dict(HOST.docks)
        for slot in HOST.slots:
            keys = [p[4][0] if len(p) > 4 and p[4] else "%s.%s" % (slot.key, p[0]) for p in slot.parts]
            for key in keys or [slot.key]:
                d = mod_def(key, docks)
                if d is not None: out.append(d)
        return out
    def ui_all(): return UI_ACTIONS + mod_actions()
    def mod_tip(key):
        s = HOST.by_key.get(key)
        if s is None: return "Module '%s' (not loaded)" % key
        d = dict(HOST.docks).get(key)
        if not s.running: return "Turn %s on" % s.title
        if d is None: return "Turn %s off" % s.title
        if safe(d.get("state")) == "open": return "Fold %s into the bar" % s.title
        return "Show %s" % s.title
    def toggle_module(key):
        s = HOST.by_key.get(key)
        if s is None: say("no module '%s'." % key, Kit.HUE_BAD); return False
        d = dict(HOST.docks).get(key)
        if not s.running:
            HOST.dock_forget(key)
            def turn(k=key, title=s.title):
                HOST.enable(k)
                if not HOST.by_key[k].running: say("%s couldn't be turned on." % title, Kit.HUE_BAD)
            later(turn); return True
        if d is None: HOST.disable(key); return True
        if safe(d.get("state")) == "open": HOST.dock_to_bar(key, s.title)
        else: safe(d.get("show")); HOST.dock_forget(key)
        return True
    def norm_key(k): return str(k or "").strip().upper().replace(" ", "")
    def key_owner(k): return HOST.hotkeys_owned.get(k)
    def bar_keys():
        return set(norm_key(c["k"]) for _, c in all_cells() if c["k"] and c["t"]) | set(k for k in bag_keys() if k)
    def fit(text, width): return Kit.fit(str(text), width, ".")
    def short_key(k):
        return (k.upper().replace("CTRL+", "C").replace("SHIFT+", "S")
                .replace("ALT+", "A").replace("NUMPAD", "N").replace("KP_", "N"))
    def fmt_count(n):
        if settings["short"]:
            if n >= 10000: return "%dk" % (n // 1000)
            if n >= 1000: return "%.1fk" % (n / 1000.0)
        return str(n)
    def parse_graphic(text):
        t = (text or "").strip()
        if not t: return None
        a, b = [s.strip() for s in (t.split(",", 1) + [""])[:2]]
        try:
            return (int(a, 16) if a.lower().startswith("0x") else int(a),
                    (int(b, 16) if b.lower().startswith("0x") else int(b)) if b else 0)
        except Exception: return None
    def blank(): return {"t": "", "v": "", "g": 0, "h": 0, "tg": "", "k": "", "lo": LOW_DEFAULT, "n": ""}
    def cell(ref): return cells[ref[0]][ref[1]]
    def bag_keys():
        ks = [norm_key(k) for k in settings["bagkeys"].split(",")]; return (ks + [""] * BAG_SLOTS)[:BAG_SLOTS]
    def set_key_of(ref, k):
        if ref[0] == "b": ks = bag_keys(); ks[ref[1]] = k; settings["bagkeys"] = ",".join(ks); save_settings()
        else: cell(ref)["k"] = k; save_cells()
    def ref_name(ref):
        kind, i = ref
        if kind == "b": return "bag slot %d" % (i + 1)
        if kind == "u": return "button %d" % (i + 1)
        if kind == "x": return "row %d cell %d" % (i // TOP_SLOTS + 2, i % TOP_SLOTS + 1)
        if i < TOP_SLOTS: return "top cell %d" % (i + 1)
        return "page %d cell %d" % (settings["page"] + 1, i - TOP_SLOTS + 1)
    def sel_ref(idx):
        if idx < ACTION_SLOTS: return ("a", idx)
        if idx < ACTION_SLOTS + UI_SLOTS: return ("u", idx - ACTION_SLOTS)
        return ("x", idx - ACTION_SLOTS - UI_SLOTS)
    def ref_sel(ref):
        if ref[0] == "a": return ref[1]
        if ref[0] == "u": return ACTION_SLOTS + ref[1]
        return ACTION_SLOTS + UI_SLOTS + ref[1]
    def sel_names():
        return (["Top %d" % (i + 1) for i in range(TOP_SLOTS)] + ["Bottom %d" % (i + 1) for i in range(BOTTOM_SLOTS)] +
                ["Button %d" % (i + 1) for i in range(UI_SLOTS)] +
                ["Row %d-%d" % (i // TOP_SLOTS + 2, i % TOP_SLOTS + 1) for i in range(EXTRA_SLOTS)])
    def shown(ref):
        kind, i = ref
        if kind == "x": return i < settings["extra"] * TOP_SLOTS
        if kind == "a": return settings["top"] or i >= TOP_SLOTS
        return True
    def all_cells(): return [((k, i), c) for k in "aux" for i, c in enumerate(cells[k])]
    def default_cells():
        a = [blank() for _ in range(ACTION_SLOTS)]
        seeds = [(0x0E21, "Bandages", "self"), (0x0F0C, "Heal potion", ""),
                 (0x0F07, "Cure potion", ""), (0x0F0B, "Refresh potion", "")]
        for i, (gr, n, tg) in enumerate(seeds): a[TOP_SLOTS + i].update({"t": "item", "g": gr, "n": n, "tg": tg})
        u = [blank() for _ in range(UI_SLOTS)]
        for i, uid in enumerate(DEFAULT_UI[:UI_SLOTS]): u[i].update({"t": "ui", "v": uid})
        return a, u
    def cell_text(c):
        t, v = c["t"], c["v"]
        if t == "item": return c["n"] or ("0x%04X" % c["g"])
        if t == "ui": d = ui_def(v); return d[1] if d else v
        if t == "ability": return "Secondary" if v == "secondary" else "Primary"
        if t == "script": return v.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0]
        return v
    def travel_what(c):
        return "%s to %s%s" % (TRAVEL_VERB.get(c.get("rm"), "Travel"), c["v"] or "?",
                               (" (%s)" % c["n"]) if c["n"] else "")
    def describe(ref):
        c = cell(ref); t = c["t"]
        if not t:
            if ref[0] in ("a", "x"): return "Empty: click to target an item; right-click for a spell, skill or more"
            return "Empty: right-click to choose what it does"
        if t == "travel":
            tip = travel_what(c)
            if HOST.services.get("grimoire.travel") is None:
                tip = "Grimoire is off: turn it on to use this cell\n" + tip
            if c["k"]: tip += "  [%s]" % c["k"]
            return tip + "\nRight-click to change"
        name = cell_text(c)
        if t == "ui" and c["v"] == "spellbook":
            name = {"open": "Fold Grimoire into the bar", "minimized": "Show Grimoire",
                    "docked": "Show Grimoire"}.get(st["grim_state"], "Open Grimoire (turns it on)")
        elif t == "ui" and c["v"] == "virtue":
            name = {"open": "Fold Virtue Assistant into the bar", "gear": "Open the Virtue Assistant window",
                    "docked": "Open the Virtue Assistant window"}.get(st["va_state"], "Virtue Assistant (not running)")
        elif t == "ui" and c["v"].startswith("mod:"): name = mod_tip(c["v"][4:])
        elif t == "ui": name = UI_TIPS.get(c["v"], name)
        tip = {"item": "Use %s", "spell": "Cast %s", "skill": "Use %s", "macro": "Run macro %s",
               "ability": "Use the %s ability", "script": "Start or stop script %s",
               "dress": "Dress %s", "undress": "Undress %s", "say": "Say \"%s\"", "ui": "%s"}.get(t, "%s") % name
        if c["tg"]: tip += ", then target %s" % ("yourself" if c["tg"] == "self" else "last target")
        if c["k"]: tip += "  [%s]" % c["k"]
        if t == "spell":
            miss = missing_reg(c["v"])
            if miss is not None: tip += "\nOut of %s" % miss[1]
        return tip + "\nRight-click to change"
    def _esc(s):
        return (str(s).replace("%", "%25").replace("&", "%26").replace("=", "%3D")
                .replace(";", "%3B").replace("|", "%7C"))
    def _unesc(s):
        return (s.replace("%7C", "|").replace("%3B", ";").replace("%3D", "=") .replace("%26", "&").replace("%25", "%"))
    def _enc(d): return "&".join("%s=%s" % (k, _esc(v)) for k, v in d.items())
    def _dec(s): return dict((k, _unesc(v)) for k, v in (p.split("=", 1) for p in s.split("&") if "=" in p))
    def load_settings():
        d = _dec(Kit.get_var(SETTINGS_KEY))
        for k in ("top", "keys", "lock", "short", "hue", "tray_open", "vertical"):
            if k in d: settings[k] = d[k] == "1"
        for k, lo, hi in (("slot", SLOT_MIN, SLOT_MAX), ("bagmode", 0, len(BAG_MODES) - 1),
                          ("page", 0, PAGES - 1), ("scale", SCALE_MIN, SCALE_MAX), ("extra", 0, EXTRA_ROWS)):
            try: settings[k] = int(d[k])
            except Exception: pass
            settings[k] = max(lo, min(hi, settings[k]))
        a = d.get("anchor", ""); settings["anchor"] = a if a in Kit.ANCHORS else ""
        for k in ("bags", "bagkeys"): settings[k] = d.get(k, settings[k])
    def save_settings():
        Kit.put_var(SETTINGS_KEY, _enc(dict(
            (k, ("1" if v else "0") if isinstance(v, bool) else v) for k, v in settings.items())))
    def _norm(d):
        c = blank()
        for k in ("t", "v", "tg", "k", "n"): c[k] = d.get(k, c[k])
        for k in ("g", "h", "lo"):
            try: c[k] = int(d.get(k, c[k]))
            except Exception: pass
        if c["t"] == "travel":
            for k in TRAVEL_KEYS: c[k] = d.get(k, "")
        return c
    def _cells_of(raw, n, skip_empty=True):
        lst = [_norm(_dec(s)) for s in raw.split(";") if s or not skip_empty]
        return (lst + [blank() for _ in range(n)])[:n]
    def load_cells():
        _saved_cells.clear(); a, u = default_cells(); raw = Kit.get_var(CELLS_KEY)
        if "|" in raw:
            ra, ru = raw.split("|", 1); a = _cells_of(ra, ACTION_SLOTS, False); u = _cells_of(ru, UI_SLOTS, False)
            used = set(c["v"] for c in u if c["t"] == "ui"); spare = [d for d in DEFAULT_UI if d not in used]
            for c in u:
                if c["t"] == "ui" and ui_def(c["v"]) is None and not c["v"].startswith("mod:"):
                    c.update(blank())
                    if spare: c.update({"t": "ui", "v": spare.pop(0)})
            if [c["v"] if c["t"] == "ui" else None for c in u] == OLD_DEFAULT_UI[:UI_SLOTS]:
                for i, uid in enumerate(DEFAULT_UI[:UI_SLOTS]): u[i].update({"t": "ui", "v": uid})
        pages = [[blank() for _ in range(BOTTOM_SLOTS)] for _ in range(PAGES)]; rawp = Kit.get_var(PAGES_KEY)
        if rawp:
            for pi, ps in enumerate(rawp.split("|")[:PAGES]): pages[pi] = _cells_of(ps, BOTTOM_SLOTS)
        else: pages[0] = a[TOP_SLOTS:]; settings["page"] = 0
        a[TOP_SLOTS:] = pages[settings["page"]]; cells["x"] = _cells_of(Kit.get_var(EXTRA_KEY), EXTRA_SLOTS)
        cells["a"], cells["u"], cells["pages"] = a, u, pages; cells_touched()
    def sync_page():
        if cells["pages"]: cells["pages"][settings["page"]] = list(cells["a"][TOP_SLOTS:])
    _saved_cells = {}
    def save_cells():
        sync_page(); cells_touched()
        def enc(lst): return ";".join(_enc(c) for c in lst)
        for key, text in ((CELLS_KEY, enc(cells["a"]) + "|" + enc(cells["u"])),
                          (PAGES_KEY, "|".join(enc(pg) for pg in cells["pages"])), (EXTRA_KEY, enc(cells["x"]))):
            if _saved_cells.get(key) != text: Kit.put_var(key, text); _saved_cells[key] = text
    def set_page(p):
        p = p % PAGES
        if p == settings["page"]: return
        sync_page(); settings["page"] = p; cells["a"][TOP_SLOTS:] = cells["pages"][p]; cells_touched(); save_settings()
        register_hotkeys(); st["next_count"] = 0.0; want_redraw([("a", TOP_SLOTS + i) for i in range(BOTTOM_SLOTS)])
        refresh_page_column(); HOST.refresh_settings(KEY); r = menu.get("ref")
        if menu.get("g") is not None and r and r[0] == "a" and r[1] >= TOP_SLOTS: close_menu()
    def picked_bags():
        out = [0] * BAG_SLOTS
        for i, p in enumerate(settings["bags"].split(",")[:BAG_SLOTS]):
            try: out[i] = int(p, 16) if p.strip() else 0
            except Exception: out[i] = 0
        return out
    def set_picked_bag(i, serial):
        lst = picked_bags(); lst[i] = serial; settings["bags"] = ",".join(("%X" % s) if s else "" for s in lst)
        save_settings()
    def save_pos():
        p = Kit.pos(win["g"]) if Kit.is_open(win["g"]) else None
        if p is not None and p != st.get("pos_saved"): st["pos_saved"] = p; Kit.put_var(POS_KEY, "%d,%d" % p)
    class ClientUI(object):
        looked = False; error = ""; world = None; GA = None; UIM = None; _acc = {}; _methods = {}
        @staticmethod
        def _flags(static):
            from System.Reflection import BindingFlags
            return (BindingFlags.Public | BindingFlags.NonPublic |
                    (BindingFlags.Static if static else BindingFlags.Instance))
        @staticmethod
        def _get(obj, name, t=None):
            static = obj is None; t = t if t is not None else obj.GetType(); key = (t, name, static)
            acc = ClientUI._acc.get(key, False)
            if acc is False:
                acc = None; flags = ClientUI._flags(static); tt = t
                while tt is not None:
                    try: p = tt.GetProperty(name, flags)
                    except Exception: p = None
                    if p is not None: acc = (p, True); break
                    f = tt.GetField(name, flags)
                    if f is not None: acc = (f, False); break
                    tt = tt.BaseType
                ClientUI._acc[key] = acc
            if acc is None: return None
            return acc[0].GetValue(obj, None) if acc[1] else acc[0].GetValue(obj)
        @staticmethod
        def _method(t, name, ptypes, static):
            key = (t, name, tuple(ptypes), static)
            if key not in ClientUI._methods: ClientUI._methods[key] = ClientUI._find_method(t, name, ptypes, static)
            return ClientUI._methods[key]
        @staticmethod
        def _find_method(t, name, ptypes, static):
            for m in t.GetMethods(ClientUI._flags(static)):
                if m.Name != name or m.IsGenericMethodDefinition: continue
                ps = m.GetParameters()
                if len(ps) < len(ptypes): continue
                if any(want is not None and ps[i].ParameterType.Name != want for i, want in enumerate(ptypes)): continue
                if all(p.IsOptional for p in ps[len(ptypes):]): return m
            return None
        @staticmethod
        def _invoke(m, target, args):
            import System; ps = m.GetParameters(); full = list(args) + [p.DefaultValue for p in ps[len(args):]]
            return m.Invoke(target, System.Array[object](full))
        @staticmethod
        def find():
            if ClientUI.looked: return
            ClientUI.looked = True; world = ClientUI.world = safe(lambda: ClientUI._get(API, "World"))
            ClientUI.GA = Client._type("ClassicUO.Game.GameActions")
            ClientUI.UIM = Client._type("ClassicUO.Game.Managers.UIManager")
            if world is None: ClientUI.error = "client World not found"
            elif ClientUI.GA is None: ClientUI.error = "GameActions not found"
        @staticmethod
        def on_main(fn):
            how, value = Client.on_main_ex(fn)
            if how == "ok": return value
            if how == "err":
                ex = Client.exc
                inner = getattr(ex, "InnerException", None) or \
                    getattr(getattr(ex, "clsException", None), "InnerException", None)
                ClientUI.error = str(inner) if inner else Client.error
            else: ClientUI.error = Client.error or "can't run on the client thread"
            return None
        @staticmethod
        def _bring_to_front(type_name):
            gumps = (ClientUI._get(None, "Gumps", ClientUI.UIM) if ClientUI.UIM is not None else None)
            node = gumps.First if gumps is not None else None
            while node is not None:
                g = node.Value
                if g is not None and g.GetType().Name == type_name and not g.IsDisposed:
                    m = ClientUI._method(g.GetType(), "BringOnTop", [], False)
                    if m is not None: m.Invoke(g, None)
                    return True
                node = node.Next
            return False
        @staticmethod
        def game_action(name, extra=(), reuse=None):
            ClientUI.find()
            if ClientUI.world is None or ClientUI.GA is None: return False
            world = ClientUI.world
            def run():
                if reuse and ClientUI._bring_to_front(reuse): return True
                m = ClientUI._method(ClientUI.GA, name, ["World"] + [None] * len(extra), True)
                if m is None: raise Exception("GameActions.%s not found" % name)
                ClientUI._invoke(m, None, [world] + list(extra)); return True
            return bool(ClientUI.on_main(run))
        @staticmethod
        def open_macro(sub):
            ClientUI.find(); world = ClientUI.world
            if world is None: return False
            def run():
                import System; mgr = ClientUI._get(world, "Macros")
                mo_t, mt_t, ms_t = [mgr.GetType().Assembly.GetType("ClassicUO.Game.Managers." + n)
                                    for n in ("MacroObject", "MacroType", "MacroSubType")]
                mo = System.Activator.CreateInstance(mo_t, System.Array[object](
                    [System.Enum.Parse(mt_t, "Open", True), System.Enum.Parse(ms_t, sub, True)]))
                ClientUI._run_macro_object(mgr, mo); return True
            return bool(ClientUI.on_main(run))
        @staticmethod
        def macro_names():
            ClientUI.find(); world = ClientUI.world
            if world is None: return []
            def run():
                mgr = ClientUI._get(world, "Macros"); m = ClientUI._method(mgr.GetType(), "GetAllMacros", [], False)
                names = [str(ClientUI._get(mc, "Name") or "") for mc in (m.Invoke(mgr, None) or [])]
                return [n for n in names if n]
            return list(ClientUI.on_main(run) or [])
        @staticmethod
        def _run_macro_object(mgr, mo):
            t = mgr.GetType()
            ClientUI._invoke(ClientUI._method(t, "SetMacroToExecute", ["MacroObject"], False), mgr, [mo])
            ClientUI._invoke(ClientUI._method(t, "Update", [], False), mgr, [])
        @staticmethod
        def run_macro(name):
            ClientUI.find(); world = ClientUI.world
            if world is None: return False
            def run():
                mgr = ClientUI._get(world, "Macros")
                find = ClientUI._method(mgr.GetType(), "FindMacro", ["String"], False)
                macro = find.Invoke(mgr, __import__("System").Array[object]([name]))
                if macro is None: return "missing"
                first = ClientUI._get(macro, "Items")
                if first is None: return "empty"
                ClientUI._run_macro_object(mgr, first); return "ok"
            r = ClientUI.on_main(run)
            if r == "missing": return None
            return r == "ok"
    def ub_cfg_path(): return Kit.data_path("_unified_bag_%d.cfg" % int(safe(lambda: API.Player.Serial, 0) or 0))
    def unified_bags(path):
        try:
            mtime = os.path.getmtime(path); cache = st["ub_cache"]
            if cache and cache[0] == path and cache[1] == mtime: return list(cache[2])
            with open(path, "r") as f: lines = f.read().splitlines()
        except Exception: return None
        slots, assign = 0, {}
        for line in lines:
            if "=" not in line: continue
            k, v = line.split("=", 1); k, v = k.strip(), v.strip()
            try:
                if k == "slots": slots = int(v)
                elif k.startswith("slot."): assign[int(k[5:])] = int(v)
            except Exception: pass
        lst = [assign[i] for i in sorted(assign) if (slots <= 0 or i < slots) and assign[i] > 0]
        st["ub_cache"] = (path, mtime, lst); return list(lst)
    def ub_bags():
        if not Client.on_client_thread(): st["ub_last"], st["ub_pending"] = unified_bags(ub_cfg_path()), False
        elif not st["ub_job"]:
            st["ub_job"] = True; path = ub_cfg_path()
            def job():
                st["ub_job"] = False; res = unified_bags(path)
                if res != st["ub_last"] or st["ub_pending"]:
                    st["ub_last"], st["ub_pending"] = res, False; st["next_scan"] = 0.0
            later(job)
        return None if st["ub_last"] is None else list(st["ub_last"])
    def link_state(var, allowed):
        s = API.GetSharedVar(var); return str(s) if s is not None and str(s) in allowed else None
    def ub_state(): return link_state("UnifiedBag_state", ("open", "collapsed", "docked"))
    def grim_state(): return link_state("Grimoire_state", ("open", "minimized", "docked"))
    def va_state(): return link_state("VirtueAssistant_state", ("open", "gear", "docked"))
    def ub_send(cmd): API.SetSharedVar("UnifiedBag_cmd", cmd)
    def all_docks(): return list(HOST.docks)
    def tray_docks(): return [(k, d) for k, d in all_docks() if d.get("always") or safe(d.get("state")) == "docked"]
    def dock_sig(): return tuple([(k, safe(d.get("state"))) for k, d in all_docks()])
    def tray_sig():
        return tuple([(k, d.get("icon"), safe(d.get("state")) if d.get("always") else None) for k, d in tray_docks()])
    def heartbeat(on=True):
        if on and not st["minimized"]: API.SetSharedVar(UB_LINK_ALIVE, time.time())
        else: API.RemoveSharedVar(UB_LINK_ALIVE)
    def watch_ub():
        now = time.time()
        if now < st["watch_next"]: return
        st["watch_next"] = now + 0.25; tips = False
        for k, s, tip in (("ub_state", ub_state(), settings["bagmode"] == 0),
                          ("grim_state", grim_state(), True), ("va_state", va_state(), True)):
            if s != st[k]: st[k] = s; tips = tips or tip
        if tips: refresh_tips()
        sig = dock_sig()
        if sig != st["dock_sig"]:
            old_keys = set(k for k, _ in (st["dock_sig"] or ())); st["dock_sig"] = sig; tsig = tray_sig()
            if tsig != st.get("tray_sig"): st["tray_sig"] = tsig; refresh_tray()
            refs = [ref for ref, c in all_cells() if c["t"] == "ui" and c["v"].startswith("mod:")]
            if refs:
                if set(k for k, _ in sig) != old_keys: want_redraw(refs)
                else: refresh_tips()
        owned = frozenset(HOST.hotkeys_owned)
        if owned != st.get("owned_sig"):
            changed = owned ^ (st.get("owned_sig") or frozenset()); st["owned_sig"] = owned
            if changed & bar_keys(): register_hotkeys()
        p = st["pending_on"]
        if p and time.time() > p[2]:
            st["pending_on"] = None; state = ub_state() if p[0] == UB_MODULE_KEY else grim_state()
            if state is None:
                say("%s didn't start; is Virtue Assistant running?" % p[1], Kit.HUE_BAD)
                if p[3] is not None: p[3]()
    def turn_on(key, title, fallback=None):
        if key in HOST.by_key: later(lambda: HOST.enable(key))
        else: API.SetSharedVar("VirtueAssistant_enable", key)
        say("turning %s on." % title); st["pending_on"] = (key, title, time.time() + 4.0, fallback)
    def toggle_grimoire():
        state = grim_state(); heartbeat()
        if state in ("minimized", "docked", "open"):
            API.SetSharedVar(GRIM_LINK_CMD, "dock" if state == "open" else "show")
        else: turn_on(GRIM_MODULE_KEY, "Grimoire", open_spellbook)
        return True
    def toggle_va():
        state = va_state(); heartbeat()
        if state not in ("open", "gear", "docked"): say("Virtue Assistant isn't running.", Kit.HUE_BAD); return False
        API.SetSharedVar(VA_LINK_CMD, "dock" if state == "open" else "show"); return True
    def auto_bags():
        out = []; bp = int(API.Backpack or 0)
        if bp: out.append(bp)
        for it in (API.ItemsInContainer(bp, False) or []):
            if len(out) >= BAG_SLOTS: break
            try:
                if it.IsContainer: out.append(int(it.Serial))
            except Exception: pass
        return out
    def scan_bags():
        mode = settings["bagmode"]
        if mode == 0:
            serials = ub_bags()
            if serials is None and st["ub_pending"]: serials = []
            else:
                st["ub_found"] = serials is not None
                if serials is None: serials = auto_bags()
        elif mode == 1: serials = picked_bags()
        else: serials = auto_bags()
        bags, found = [], []
        for s in (list(serials) + [0] * BAG_SLOTS)[:BAG_SLOTS]:
            if not s: bags.append(None); found.append(None); continue
            it = Kit.find_item(s); found.append(it)
            if it is None: bags.append({"s": s, "g": 0, "h": 0, "n": "Bag (not loaded yet)"}); continue
            try: gr, hu = int(it.Graphic or 0), int(it.Hue or 0)
            except Exception: gr = hu = 0
            bags.append({"s": s, "g": gr, "h": hu, "n": None})
        sig = tuple((b["s"], b["g"], b["h"]) if b else None for b in bags)
        if sig != st["bag_sig"]:
            for b, it in zip(bags, found):
                if b is not None and b["n"] is None:
                    try: b["n"] = str(it.Name or "") or "Bag"
                    except Exception: b["n"] = "Bag"
            st["bags"], st["bag_sig"] = bags, sig; want_redraw([("b", i) for i in range(BAG_SLOTS)])
    def bag_at(i): return st["bags"][i] if i < len(st["bags"]) else None
    _kinds = {"types": None}
    def cells_touched(): _kinds["types"] = None
    def _cell_kinds():
        if _kinds["types"] is None:
            every = cells["a"] + cells["u"] + cells["x"]; _kinds["types"] = set(c["t"] for c in every)
            _kinds["items"] = set(c["g"] for c in every if c["t"] == "item"); regs, extra = set(), set()
            refs = {"skill": [], "spell": []}
            for ref, c in all_cells():
                if c["t"] == "spell": regs.update(r[1] for r in spell_reg_list(c["v"])); refs["spell"].append(ref)
                elif c["t"] == "skill": refs["skill"].append(ref)
                elif c["t"] == "travel" and c.get("rm") in TRAVEL_SCROLL: extra.add(TRAVEL_SCROLL[c["rm"]])
            _kinds["extra"], _kinds["refs"] = frozenset(regs | extra), refs
        return _kinds
    def scan_abilities():
        if "ability" not in _cell_kinds()["types"]: return
        sig = tuple([str(n) for n in (API.CurrentAbilityNames() or [])])
        if sig != st["ability_sig"]:
            st["ability_sig"] = sig; want_redraw([r for r, c in all_cells() if c["t"] == "ability"])
    def count_now(extra=(), max_age=0.0):
        try: items = HOST.pack_items(deep=True, max_age=max_age)
        except Exception: return
        k = _cell_kinds(); wanted = k["items"]
        if extra or k["extra"]: wanted = wanted | k["extra"] | set(extra)
        cnt, cnt_g, first, first_g = {}, {}, {}, {}
        cget, gget, fset, fgset = cnt.get, cnt_g.get, first.setdefault, first_g.setdefault
        for it in items:
            try:
                gr = int(it.Graphic)
                if gr not in wanted: continue
                hu, ser = int(it.Hue), int(it.Serial); amt = max(1, int(it.Amount or 0))
            except Exception: continue
            key = (gr, hu); cnt[key] = cget(key, 0) + amt; cnt_g[gr] = gget(gr, 0) + amt; fset(key, ser); fgset(gr, ser)
        st.update({"cnt": cnt, "cnt_g": cnt_g, "first": first, "first_g": first_g, "counted": wanted,
                   "counted_at": time.time()})
    def _place(info, lbl, text, hue):
        if info.get("txt") != text:
            info["txt"] = text
            try:
                lbl.Text = text
                Kit.ui_pos(lbl, info["x"] + info["w"] - Kit.text_px(text) - 3, info["y"] + info["h"] - 16)
            except Exception: pass
        if info.get("hue") != hue: info["hue"] = hue; Kit.set(lbl, "Hue", hue)
    def refresh_counts():
        if st["minimized"]: return
        k = _cell_kinds()
        if "item" in k["types"] or k["extra"]: count_now(max_age=0.5)
        update_labels()
    _counters = [None]
    def update_labels():
        now = time.time(); cool = st["cool"]; charges = False; lst = _counters[0]
        if lst is None:
            lst = [(ref, info, info["count"]) for ref, info in win["cells"].items() if info.get("count") is not None]
            _counters[0] = lst
        for ref, info, lbl in lst:
            c = cell(ref); t, v = c["t"], c["v"]; text, hue = "", Kit.HUE_TEXT; end = cool.get(t)
            if end and now < end: text, hue = cool_text(end - now), Kit.HUE_TITLE
            elif t == "item":
                n = st["cnt"].get((c["g"], c["h"]), 0) if settings["hue"] else st["cnt_g"].get(c["g"], 0)
                text = fmt_count(n); hue = Kit.HUE_BAD if n <= max(0, c["lo"]) else Kit.HUE_TEXT
            elif t in ("spell", "ability", "script"):
                try:
                    if t == "spell": on = bool(API.IsSpellActive(v))
                    elif t == "ability":
                        on = bool(API.SecondaryAbilityActive() if v == "secondary" else API.PrimaryAbilityActive())
                    else: on = script_running(v)
                except Exception: on = False
                text, hue = ("ON" if on else ""), Kit.HUE_GOOD
            elif t == "travel":
                if charges is False: charges = travel_charges()
                text, hue = travel_count(c, charges)
            if t == "spell":
                miss = missing_reg(v); grey_cell(ref, info, miss is not None)
                if miss is not None and not (end and now < end): text, hue = miss[0], Kit.HUE_BAD
            _place(info, lbl, text, hue)
        for i, info in list(win["bags"].items()):
            lbl = info.get("count"); b = bag_at(i)
            if lbl is None or not b: continue
            try: n = int(API.Contents(b["s"]) or 0)
            except Exception: n = 0
            _place(info, lbl, str(n), Kit.HUE_TEXT)
    _regs = {}
    def spell_reg_list(name):
        hit = _regs.get(name)
        if hit is None:
            info = Kit.spell_info(name); table = Kit.REAGENTS
            hit = tuple((a, table[a][1], table[a][0]) for a in (info[1] if info else ()) if a in table)
            if len(_regs) > 200: _regs.clear()
            _regs[name] = hit
        return hit
    def missing_reg(name):
        cnt, counted = st["cnt_g"], st.get("counted") or ()
        for a, g, n in spell_reg_list(name):
            if cnt.get(g, 0) <= 0 and g in counted: return (a, n)
        return None
    def grey_cell(ref, info, grey):
        if info.get("grey", False) == grey: return
        info["grey"] = grey; icon = info.get("icon")
        if icon is not None: icon.SetAlpha(0.35 if grey else 1.0)
        set_tip(info, describe(ref))
    def travel_charges():
        fn = HOST.services.get("grimoire.book_charges")
        if fn is not None: return safe(fn)
        fn = HOST.services.get("grimoire.destinations")
        if fn is None: return None
        try: return dict((d["book"], d["charges"]) for d in fn() or ())
        except Exception: return None
    def travel_count(c, charges):
        if charges is None: return "off", Kit.HUE_INFO
        m = c.get("rm"); lo = max(0, c["lo"])
        if m in TRAVEL_SCROLL:
            n = st["cnt_g"].get(TRAVEL_SCROLL[m], 0); return fmt_count(n), Kit.HUE_BAD if n <= lo else Kit.HUE_TEXT
        try: n = charges.get(int(c.get("rb") or "0", 16))
        except ValueError: n = None
        if n is None: return "", Kit.HUE_TEXT
        if m == "charge": return str(n), Kit.HUE_BAD if n <= lo else Kit.HUE_TEXT
        return str(n), Kit.HUE_INFO
    def fire_travel(c):
        fn = HOST.services.get("grimoire.travel")
        if fn is None: say("Grimoire is off; turn it on to use Travel cells.", Kit.HUE_BAD); return False
        try: book, idx = int(c.get("rb") or "", 16), int(c.get("ri") or "")
        except ValueError:
            say("this Travel cell has no destination; right-click it to pick one.", Kit.HUE_BAD); return False
        return bool(fn(book, idx, c.get("rm") or "recall", c["v"] or None))
    def set_travel(ref, d, method):
        cur = cell(ref)
        new = dict(blank(), t="travel", v=str(d["name"]), n=str(d["book_name"]), k=cur["k"], tg="",
                   lo=cur["lo"] if cur["t"] == "travel" else 2, rb="%X" % int(d["book"]), ri=str(int(d["index"])),
                   rm=method)
        cells[ref[0]][ref[1]] = new; cells_changed(recount=True, refs=[ref])
        say("%s set on %s." % (travel_what(new), ref_name(ref)), Kit.HUE_GOOD)
    _skill_delay = {"arms lore": 3.0, "item identification": 3.0, "detect hidden": 3.0}
    def cool_text(rem): return ("%d" % int(math.ceil(rem))) if rem >= 3.0 else ("%.1f" % max(0.0, rem))
    def start_cool(t, v):
        if t == "skill": secs = _skill_delay.get(str(v).strip().lower(), 10.0)
        else: info = Kit.spell_info(v); secs = info[3] if info else 0.0
        if secs and secs > 0: st["cool"][t] = time.time() + secs; st["cool_next"] = 0.0
    def cool_tick(now):
        cool = st["cool"]
        if not (cool["skill"] or cool["spell"]) or now < st["cool_next"]: return
        st["cool_next"] = now + 0.1; refs = _cell_kinds()["refs"]; ended = False
        for kind in ("skill", "spell"):
            end = cool[kind]
            if not end: continue
            done = now >= end
            if done: cool[kind] = 0.0; ended = True
            text = "" if done else cool_text(end - now)
            for ref in refs[kind]:
                info = win["cells"].get(ref)
                if info is None: continue
                dark = not done
                if info.get("dark", False) != dark:
                    info["dark"] = dark; info["catcher"].SetAlpha(0.55 if dark else 0.01)
                lbl = info.get("count")
                if lbl is not None and not done: _place(info, lbl, text, Kit.HUE_TITLE)
        if ended: update_labels()
    def short_what(ref):
        c = cell(ref)
        if c["t"] == "travel": return travel_what(c)
        tip = describe(ref).split("\n")[0]; return tip.replace("  [%s]" % c["k"], "") if c["k"] else tip
    def hotkeys_service():
        out = [(norm_key(c["k"]), "%s: %s" % (ref_name(r), short_what(r))) for r, c in all_cells()
               if norm_key(c["k"]) and c["t"] and shown(r)]
        out += [(k, "bag slot %d" % (i + 1)) for i, k in enumerate(bag_keys()) if k]
        return [(k, what + ((" (left to %s)" % key_owner(k)) if key_owner(k) else "")) for k, what in out]
    queue = Kit.queuer(st); on_disposed = Kit.disposer(KEY, st, win)
    def want_rebuild(delay=0.0): st["rebuild_at"] = time.time() + delay
    def cells_changed(recount=False, refresh=True, refs=None):
        save_cells(); register_hotkeys()
        if recount: st["next_count"] = 0.0
        if refs is None: want_rebuild()
        else: want_redraw(refs)
        if refresh: HOST.refresh_settings(KEY)
    def clear_cell(ref): cells[ref[0]][ref[1]] = blank(); cells_changed(refs=[ref])
    fitst = {"scale": None, "vertical": None, "slot": None, "off": (0, 0), "sig": None}
    def eff_scale(): v = fitst["scale"]; return int(settings["scale"]) if v is None else v
    def eff_vertical(): v = fitst["vertical"]; return bool(settings["vertical"]) if v is None else v
    def told_slot(): return fitst["slot"] if fitst["scale"] is not None else None
    def fit_sig(): return (settings["slot"], settings["top"], settings["extra"])
    def _fit_scale(along, across):
        keep = fitst["scale"]
        try:
            fitst["scale"] = 100; G1 = _geom_base()
            pct = max(SCALE_MIN, min(SCALE_MAX, int(min(along * 100.0 / max(1.0, G1["W"]),
                                                        across * 100.0 / max(1.0, G1["H"])))))
            def fits(p): fitst["scale"] = p; G2 = _geom_base(); return G2["W"] <= along and G2["H"] <= across
            for _ in range(8):
                if pct <= SCALE_MIN or fits(pct): break
                pct -= 1
            for _ in range(8):
                if pct >= SCALE_MAX or not fits(pct + 1): break
                pct += 1
            return pct
        finally: fitst["scale"] = keep
    def tell_need():
        base = HOST.layout_base(KEY)
        if not settings["extra"] or base is None: HOST.layout_need(KEY); return
        vert = base[1] > base[0]; along, across = (base[1], base[0]) if vert else base
        keep, kept_scale, vt = settings["extra"], fitst["scale"], _ctrl.get("vtmp"); _ctrl["vtmp"] = vert
        try:
            settings["extra"] = 0; p = _fit_scale(int(along), int(across)); settings["extra"] = keep
            fitst["scale"] = p; need = _geom_base()["H"]
        finally: settings["extra"] = keep; fitst["scale"] = kept_scale; _ctrl["vtmp"] = vt
        HOST.layout_need(KEY, need if vert else None, None if vert else need)
    def layout_fit(w, h, mode):
        if w is None or h is None or not w or not h: new = (None, None); slot = sig = None
        else:
            slot = (int(w), int(h)); vert = h > w; along, across = (h, w) if vert else (w, h)
            sig = fit_sig(); tell_need(); _ctrl["vtmp"] = vert
            try: new = (_fit_scale(int(along), int(across)), vert)
            finally: _ctrl["vtmp"] = None
        was = (eff_scale(), eff_vertical(), fitst["slot"]); fitst["scale"], fitst["vertical"] = new
        fitst["slot"], fitst["sig"] = slot, sig
        if (eff_scale(), eff_vertical(), fitst["slot"]) != was and not st["shutting"]: want_rebuild()
    def refit_if_stale():
        slot = told_slot(); sig = fit_sig()
        if slot is None or sig == fitst["sig"]: return
        along, across = (slot[1], slot[0]) if fitst["vertical"] else slot
        fitst["scale"] = _fit_scale(along, across); fitst["sig"] = sig; tell_need()
    def layout_state():
        if win["g"] is None or st["shutting"]: return None
        return "minimized" if st["minimized"] else "open"
    LAYOUT_HOOKS = {"fit": layout_fit, "state": layout_state, "exact": True, "untitled": True}
    def sc(v, lo=1): k = max(SCALE_MIN, min(SCALE_MAX, eff_scale())) / 100.0; return max(lo, int(round(v * k)))
    _geom = {"key": None, "L": None}
    def geom():
        slot = told_slot()
        key = (settings["slot"], eff_scale(), settings["top"], settings["extra"], slot, eff_vertical())
        if _geom["key"] != key:
            if slot is None: _geom["L"] = _geom_base()
            else:
                along, across = (slot[1], slot[0]) if eff_vertical() else slot
                _geom["L"] = _stretch(_geom_base(), along, across)
            _geom["key"] = key
        return _geom["L"]
    _ctrl = {"capw": None, "vtmp": None}
    def ctrl_capw():
        if _ctrl["capw"] is None: _ctrl["capw"] = max(Kit.text_w(c) for c in ("Keys", "Lock", "Grid")) + 6
        return _ctrl["capw"]
    def ctrl_orders(vert): return (4, 2, 1) if vert else (1, 2, 4)
    def ctrl_cells(c, dw, dh):
        rows = (4 + c - 1) // c; cell_w = (dw - 2 * CTRL_PAD - (c - 1) * CTRL_PAD) // c
        cell_h = min(24, (dh - 2 * CTRL_PAD - (rows - 1) * CTRL_PAD) // rows); return rows, cell_w, cell_h
    def ctrl_need(col_h, vert):
        capw = ctrl_capw()
        for c in ctrl_orders(vert):
            rows = (4 + c - 1) // c; across = rows * CTRL_ROW_MIN + (rows - 1) * CTRL_PAD + 2 * CTRL_PAD
            along = c * capw + (c - 1) * CTRL_PAD + 2 * CTRL_PAD
            if vert and along <= col_h: return across
            if not vert and across <= col_h: return along
        return (4 * CTRL_ROW_MIN + 5 * CTRL_PAD) if vert else (4 * capw + 5 * CTRL_PAD)
    def _geom_base():
        S = sc(max(SLOT_MIN, min(SLOT_MAX, int(settings["slot"]))), 18); bm, sg, p4 = sc(BAR_M, 4), sc(6, 3), sc(4, 2)
        m = bm; gap, ug, bg = sc(4, 2), sc(UI_GAP, 2), sc(BAG_GAP, 2)
        pw, cw, tb = sc(PAGE_W, 16), sc(CTRL_W, 34), sc(TRAY_BTN, 18); pitch = S + gap; ph = S + 2 * p4
        inner = pw + TOP_SLOTS * pitch + p4; left_w = BOTTOM_SLOTS * pitch + p4; tray_w = tb + 2 * p4
        rest = inner - pw - left_w - 2 * sg - tray_w - sg; ui_w = int(rest * UI_SHARE); bag_w = rest - ui_w
        bw = (ui_w - 2 * p4 - (UI_SLOTS - 1) * ug) // UI_SLOTS
        bgw = (bag_w - 2 * p4 - (BAG_SLOTS - 1) * bg) // BAG_SLOTS
        rows = (2 if settings["top"] else 1) + settings["extra"]
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
        if n <= 0: return []
        if total <= 0: return [0] * n
        return [(total * (i + 1)) // n - (total * i) // n for i in range(n)]
    def _stretch(L, along, across):
        L = dict(L); S, p4, sg, rows = L["S"], L["p4"], L["sg"], L["rows"]; gap = L["pitch"] - S; n = TOP_SLOTS
        deep = max(0, int(S * 1.6) - S); spare = along - L["W"]
        if spare > 0:
            cap1 = n * gap + sg; s1 = min(spare, cap1); t = float(s1) / cap1 if cap1 > 0 else 0.0
            dc = min(s1, int(round(sg * t))); gaps = [gap + d for d in _share(s1 - dc, n)]
            s2 = min(spare - s1, n * deep); colw = [S + d for d in _share(s2, n)]; s3 = spare - s1 - s2; tail = 0
            if s3 > 0:
                if rows > 1: gaps = [a + d for a, d in zip(gaps, _share(s3, n))]
                else: tail = s3
            colx, x = [], p4
            for i in range(n): colx.append(x); x += colw[i] + gaps[i]
            sgx = sg + int(round(sg * t)); ug = L["ug"] + int(round(L["ug"] * t))
            bg = L["bg"] + int(round(L["bg"] * t)); pw, tray_w = L["pw"], L["tray_w"]; inner = pw + x + tail
            left_w = colx[BOTTOM_SLOTS]; rest = inner - pw - left_w - 3 * sgx - tray_w; ui_w = int(rest * UI_SHARE)
            bag_w = rest - ui_w
            L.update({"colx": tuple(colx), "colw": tuple(colw), "top_w": x,
                      "sgx": sgx, "sgc": sg + dc, "ug": ug, "bg": bg,
                      "inner": inner, "left_w": left_w, "ui_w": ui_w, "bag_w": bag_w,
                      "bw": (ui_w - 2 * p4 - (UI_SLOTS - 1) * ug) // UI_SLOTS,
                      "bgw": (bag_w - 2 * p4 - (BAG_SLOTS - 1) * bg) // BAG_SLOTS})
            L["W"] = L["m"] + inner + L["sgc"] + L["cw"] + L["m"]
        spare = across - L["H"]
        if spare > 0:
            s1 = min(spare, (rows - 1) * sg); rgap = [sg + d for d in _share(s1, rows - 1)]
            s2 = min(spare - s1, rows * deep); cellh = [S + d for d in _share(s2, rows)]
            pad = _share(spare - s1 - s2, rows); rowy, rowh, celly, y = [], [], [], 0
            for r in range(rows):
                rowy.append(y); rh = cellh[r] + 2 * p4 + pad[r]; rowh.append(rh); celly.append(p4 + pad[r] // 2)
                y += rh + (rgap[r] if r < rows - 1 else 0)
            L.update({"rowy": tuple(rowy), "rowh": tuple(rowh), "celly": tuple(celly),
                      "cellh": tuple(cellh), "bh": cellh[-1] - p4, "bgh": cellh[-1]})
            L["H"] = L["m"] + y + L["m"]
        return L
    def flat(): return not eff_vertical()
    def bar_size():
        if st["minimized"]: return MINI_W, MINI_H
        L = geom(); return (L["W"], L["H"]) if flat() else (L["H"], L["W"])
    def R(x, y, w, h): ox, oy = fitst["off"]; return (x + ox, y + oy, w, h) if flat() else (y + ox, x + oy, h, w)
    def add_item_pic(g, graphic, hue, x, y, w, h):
        try: p = G.CreateGumpItemPic(int(graphic), int(w), int(h))
        except Exception: return None
        if hue: p.Hue = max(0, min(0xFFFF, int(hue)))
        p.SetPos(x, y); p.SetAcceptMouseInput(False); g.Add(p); return p
    def caption_words(text):
        t = str(text).replace("_", " ")
        return "".join(" " + ch if i and ch.isupper() and t[i - 1].islower() else ch for i, ch in enumerate(t))
    def add_cell_text(g, text, x, y, w, h, hue=None):
        most = max(1, min(3, (h - 2) // 14)); lines = [Kit.fit(l, w - 4) for l in Kit.wrap(caption_words(text), w - 4)]
        if len(lines) > most:
            lines = lines[:most]
            lines[-1] = Kit.fit(lines[-1] + "..", w - 4) if not lines[-1].endswith("..") else lines[-1]
        ty = y + (h - 14 * len(lines)) // 2 - 1
        return [Kit.add_label(g, l, x + (w - Kit.text_w(l)) // 2, ty + i * 14,
                              Kit.HUE_TEXT if hue is None else hue) for i, l in enumerate(lines)]
    def click_handler(kind, menu_kind, arg):
        def fn():
            if st["right_ok"] is False and Client.key_held("shift"): st["queue"].append((menu_kind, arg))
            else: st["queue"].append((kind, arg))
        return fn
    _right = {"add": {}, "mods": None}
    def hook_right(api_ctrl, fn):
        if api_ctrl is None or st["right_ok"] is False: return False
        try:
            mods = _right["mods"]
            if mods is None:
                import clr; import System; from System.Reflection import BindingFlags
                mods = _right["mods"] = (clr, System, BindingFlags.Instance |
                                         BindingFlags.Public | BindingFlags.NonPublic)
            clr, System, flags = mods; ctrl = Kit.client_control(api_ctrl); key = str(ctrl.GetType().FullName)
            add = _right["add"].get(key)
            if add is None:
                t, ev = ctrl.GetType(), None
                while t is not None and ev is None: ev = t.GetEvent("MouseUp", flags); t = t.BaseType
                add = _right["add"][key] = (clr.GetPythonType(ev.EventHandlerType), ev.GetAddMethod(True))
            def handler(sender, e):
                try:
                    if str(e.Button) == "Right": Kit.pending.append(fn); e.Result = True; HOST.poke()
                except Exception: pass
            add[1].Invoke(ctrl, System.Array[object]([add[0](handler)])); st["right_ok"] = True; return True
        except Exception:
            if st["right_ok"] is None:
                st["right_ok"] = False
                say("no right-click events from this client; Shift+click a cell for its menu instead.")
            return False
    def add_icon(g, icon, x, y, w, h):
        side = min(w, h) - 4; p = Kit.add_pic(g, icon, x + (w - side) // 2, y + (h - side) // 2)
        if p is not None: p.SetWidth(side); p.SetHeight(side); p.SetAcceptMouseInput(False)
        return p
    def draw_cell(g, ref, x, y, w, h):
        if not cell(ref)["t"]:
            Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA * 0.3)
            for bx, by, bw_, bh_ in ((x, y, w, 1), (x, y + h - 1, w, 1), (x, y, 1, h), (x + w - 1, y, 1, h)):
                Kit.add_tiled(g, SLOT_TILE, bx, by, bw_, bh_, SLOT_ALPHA)
        else: Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        cell_content(g, ref, x, y, w, h)
    def pic_box(ref, x, y, w, h, pad):
        if w == h or ref[0] == "u": return x + pad, y + pad, w - 2 * pad, h - 2 * pad
        side = min(w, h) - 2 * pad; return x + (w - side) // 2, y + (h - side) // 2, side, side
    def cell_content(g, ref, x, y, w, h):
        c = cell(ref); t = c["t"]; info = {"x": x, "y": y, "w": w, "h": h, "count": None}; parts = []; shown = False
        ky = 14 if (settings["keys"] and c["k"] and t) else 0; p = None
        if t == "item" and c["g"]: p = add_item_pic(g, c["g"], c["h"], *pic_box(ref, x, y, w, h, 3))
        elif t == "spell":
            icon = spell_icon(c["v"])
            if icon: p = info["icon"] = add_icon(g, icon, x, y, w, h)
        elif t == "travel":
            m = c.get("rm")
            if m in TRAVEL_SPELL:
                icon = spell_icon(TRAVEL_SPELL[m])
                if icon: p = add_icon(g, icon, x, y, w, h)
            elif m in TRAVEL_ITEM: p = add_item_pic(g, TRAVEL_ITEM[m], 0, *pic_box(ref, x, y, w, h, 3))
            if p is not None: p.SetAlpha(0.5)
            name = fit(c["v"] or "?", w - 4)
            parts.append(Kit.add_label(g, name, x + (w - Kit.text_w(name)) // 2, y + ky + (h - ky - 14) // 2 - 1))
            shown = True
        elif t == "ability":
            icon, name = ability_info(c["v"])
            if icon: p = add_icon(g, icon, x, y, w, h)
            elif name: parts.extend(add_cell_text(g, name, x, y + ky, w, h - ky)); shown = True
        elif t == "ui":
            d = ui_def(c["v"])
            if d and d[2]: p = add_item_pic(g, d[2], 0, *pic_box(ref, x, y, w, h, 2))
        elif t == "script":
            nm = caption_words(cell_text(c)).strip().lower(); icon = SPELL_ICON.get(nm) if nm else None
            if icon and Kit.pic_size(icon)[0] > 0: p = add_icon(g, icon, x, y, w, h)
        if p is not None: shown = True; parts.append(p)
        if t and not shown: parts.extend(add_cell_text(g, cell_text(c), x, y + ky, w, h - ky))
        win["cells"][ref] = finish_cell(g, info, parts, t in ("item", "spell", "ability", "script", "skill", "travel"),
                                        c["k"] if settings["keys"] and t else "", describe(ref), ("click", "menu", ref))
        _counters[0] = None
    def finish_cell(g, info, parts, counted, k, tip, click):
        x, y, w, h = info["x"], info["y"], info["w"], info["h"]
        if counted:
            info["count"] = Kit.add_label(g, "", x + w - 6, y + h - 16); info["txt"], info["hue"] = "", Kit.HUE_TEXT
            parts.append(info["count"])
        if k:
            kt = fit(short_key(k), w - 4)
            info["key"] = Kit.add_label(g, kt, x + w - 2 - Kit.text_w(kt), y + 1, Kit.HUE_INFO)
            parts.append(info["key"])
        info["tip"] = tip; info["catcher"] = Kit.catcher(g, x, y, w, h, click_handler(*click), tip)
        parts.append(info["catcher"]); hook_right(info["catcher"], queue(click[1:])); info["parts"] = parts; return info
    def bag_tip(i):
        b, mode = bag_at(i), settings["bagmode"]
        ub = (mode == 0 and st["ub_state"]) and ("Show the Bags window" if st["ub_state"] != "open"
                                                 else "Fold the Bags window into the bar")
        if mode == 1:
            tip = ("Open %s\nRight-click: pick another bag, or clear the slot" % b["n"] if b else
                   "Empty: click, then target a bag for it")
        elif ub: tip = ub + "\n%sRight-click: the Bags settings" % (b["n"] + "   " if b else "")
        else: tip = "Open %s" % b["n"] if b else "No bag here"
        bk = bag_keys()[i]
        if bk: tip += "  [%s]" % bk
        return tip
    def draw_bag(g, i, x, y, w, h): Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA); bag_content(g, i, x, y, w, h)
    def bag_content(g, i, x, y, w, h):
        b = bag_at(i); info = {"x": x, "y": y, "w": w, "h": h, "count": None}
        parts = [add_item_pic(g, b["g"], b["h"], x + 3, y + 3, w - 6, h - 6)] if b and b["g"] else []
        win["bags"][i] = finish_cell(g, info, parts, b, bag_keys()[i] if settings["keys"] else "", bag_tip(i),
                                     ("bag", "bagmenu", i))
    def want_redraw(refs): st["redraw"].update(refs)
    def redraw_now():
        refs, st["redraw"] = st["redraw"], set(); g = win["g"]
        if not refs or st["minimized"] or not Kit.is_open(g): return
        for ref in sorted(refs):
            bag = ref[0] == "b"; info = win["bags"].get(ref[1]) if bag else win["cells"].get(ref)
            if info is None: continue
            for p in info.get("parts") or (): Kit.dispose(p)
            if bag: bag_content(g, ref[1], info["x"], info["y"], info["w"], info["h"])
            else: cell_content(g, ref, info["x"], info["y"], info["w"], info["h"])
        update_labels()
    def refresh_key(ref):
        g = win["g"]; bag = ref[0] == "b"
        info, k = (win["bags"].get(ref[1]), bag_keys()[ref[1]]) if bag else (win["cells"].get(ref), cell(ref)["k"])
        if info is None or not Kit.is_open(g): return
        text = fit(short_key(k), info["w"] - 4) if (settings["keys"] and k and (bag or cell(ref)["t"])) else ""
        lbl = info.get("key")
        if text and lbl is None:
            lbl = Kit.add_label(g, text, info["x"] + info["w"] - 2 - Kit.text_w(text), info["y"] + 1, Kit.HUE_INFO)
            lbl.SetAcceptMouseInput(False); info["key"] = lbl; info.setdefault("parts", []).append(lbl)
        elif lbl is not None: lbl.Text = text
        set_tip(info, bag_tip(ref[1]) if bag else describe(ref))
    def set_tip(info, tip):
        c = info.get("catcher")
        if c is not None and info.get("tip") != tip: info["tip"] = tip; Kit.with_tip(c, tip)
    def refresh_tips():
        if not Kit.is_open(win["g"]): return
        for ref, info in list(win["cells"].items()):
            c = cell(ref)
            if (c["t"] == "ui" and (c["v"] in ("spellbook", "virtue") or c["v"].startswith("mod:"))
                    or c["t"] == "travel"):
                set_tip(info, describe(ref))
        for i, info in list(win["bags"].items()): set_tip(info, bag_tip(i))
    def recolor(btn, hue, tip):
        for lbl in btn["text"]: lbl.Hue = hue
        Kit.with_tip(btn.get("catcher"), tip)
    def refresh_bind_button():
        btn = win.get("keybtn")
        if btn and Kit.is_open(win["g"]): recolor(btn, *bind_look())
    def refresh_tray():
        if not Kit.is_open(win["g"]): return
        btn = win.get("traybtn")
        if btn:
            n = len(tray_docks()); hue = Kit.HUE_TITLE if n else Kit.HUE_INFO
            for lbl in btn.get("text", []):
                Kit.set_text(lbl, str(n), hue)
                Kit.ui_pos(lbl, btn["x"] + (btn["w"] - Kit.text_px(str(n))) // 2, btn["ly"])
            Kit.with_tip(btn.get("catcher"), tray_tip(n))
        build_tray()
    PAGE_TIPS = (("up", "Next page of the bottom-left cells (page %d of %d showing)"),
                 ("dn", "Previous page of the bottom-left cells (page %d of %d showing)"),
                 ("catcher", "Page %d of %d of the bottom-left cells; click for the next page"))
    def draw_page_column(g, store, x, y0, ph, PAGE_W):
        p = settings["page"]; aw, ah = Kit.pic_size(Kit.ART_RESTORE[0]); aw, ah = aw or 16, ah or 16
        cx = x + (PAGE_W - aw) // 2; ax, ay = R(cx, y0 + 1, aw, ah)[:2]
        up = Kit.art_button(g, store, "pgup", Kit.ART_RESTORE, ax, ay, None, PAGE_TIPS[0][1] % (p + 1, PAGES),
                            on_click=queue(("page", 1)))
        ax, ay = R(cx, y0 + ph - ah - 1, aw, ah)[:2]
        dn = Kit.art_button(g, store, "pgdn", Kit.ART_MIN, ax, ay, None, PAGE_TIPS[1][1] % (p + 1, PAGES),
                            on_click=queue(("page", -1)))
        num = str(p + 1); nx, ny, nw, nh = R(x, y0 + ah + 1, PAGE_W, max(1, ph - 2 * ah - 2))
        lbl = Kit.add_label(g, num, nx + (nw - Kit.text_w(num)) // 2, ny + (nh - 14) // 2, Kit.HUE_TITLE)
        c = Kit.catcher(g, nx, ny, nw, nh, queue(("page", 1)), PAGE_TIPS[2][1] % (p + 1, PAGES))
        win["pagecol"] = {"up": up, "dn": dn, "num": lbl, "catcher": c, "rect": (nx, ny, nw, nh), "page": p}
    def refresh_page_column():
        pc = win.get("pagecol"); p = settings["page"]
        if not pc or pc["page"] == p or not Kit.is_open(win["g"]): return
        pc["page"] = p; num = str(p + 1); nx, ny, nw, nh = pc["rect"]; lbl = pc["num"]; Kit.set_text(lbl, num)
        Kit.ui_pos(lbl, nx + (nw - Kit.text_w(num)) // 2, ny + (nh - 14) // 2)
        for k, tip in PAGE_TIPS: Kit.with_tip(pc[k], tip % (p + 1, PAGES))
    def draw_tray(g, key, d, x, y, w, h):
        Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA); state = safe(d.get("state")); title = d.get("title") or key
        hue = 0 if state == "open" else Kit.HUE_INFO; icon = d.get("icon") or 0
        shown = icon and add_item_pic(g, icon, hue, x + 2, y + 2, w - 4, h - 4) is not None
        if not shown: add_cell_text(g, title[:3].upper(), x, y, w, h, Kit.HUE_TEXT if state == "open" else Kit.HUE_INFO)
        tip = ("%s is off; click to turn it on" if state is None else
               "Fold %s into the bar" if state == "open" else "Show %s") % title
        Kit.catcher(g, x, y, w, h, queue(("dock", key)), tip)
    def draw_small_button(g, box, caption, fn, hue, tip):
        x, y, w, h = box; Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        return {"text": add_cell_text(g, caption, x, y, w, max(16, h), hue),
                "catcher": Kit.catcher(g, x, y, w, h, fn, tip)}
    def bind_look():
        if st["bind"] is not None:
            return Kit.HUE_TITLE, "Keybind mode on: hover a cell, press a key; Esc or a click here ends it"
        return Kit.HUE_TEXT, "Start keybind mode: hover a cell and press a key to bind it"
    def tray_tip(n):
        return "%s folded into the bar; click to %s the tray" % (Kit.count(n, "window"),
                                                                         "hide" if settings["tray_open"] else "show")
    def draw_ctrl_column(g, store, L):
        BAR_M, CTRL_W = L["m"], L["cw"]; x = BAR_M + L["inner"] + L["sgc"]; col_h = L["rowy"][-1] + L["rowh"][-1]
        aw, ah = Kit.pic_size(Kit.ART_MIN[0]); aw, ah = aw or 16, ah or 16; ty = BAR_M + 2 + ah + 4
        avail = BAR_M + col_h - ty; capw = ctrl_capw()
        acts = (("Keys", queue(("bind",)), bind_look()), ("Lock", queue(("lockbar",)), lock_look()),
                ("Grid", queue(("grid",)), grid_look()))
        if flat() and avail >= 66 and CTRL_W - 4 >= capw:
            mx, my = R(x + (CTRL_W - aw) // 2, BAR_M + 2, aw, ah)[:2]; bw_, bh_ = CTRL_W - 4, min(28, (avail - 8) // 3)
            boxes = [R(x + 2, ty + i * (bh_ + 4), bw_, bh_) for i in range(3)]
        else:
            dx, dy, dw, dh = R(x, BAR_M, CTRL_W, col_h)
            opts = [(c,) + ctrl_cells(c, dw, dh) for c in ctrl_orders(not flat())]
            c, rows, cell_w, cell_h = (next((o for o in opts if o[2] >= capw and o[3] >= CTRL_ROW_MIN), None) or
                                       max(opts, key=lambda o: min(o[2] - capw, o[3] - CTRL_ROW_MIN)))
            cell_w, cell_h = max(1, cell_w), max(1, cell_h); block_w = c * cell_w + (c - 1) * CTRL_PAD
            block_h = rows * cell_h + (rows - 1) * CTRL_PAD; x0 = dx + max(CTRL_PAD, (dw - block_w) // 2)
            y0 = dy + max(CTRL_PAD, (dh - block_h) // 2)
            cells = [(x0 + (n % c) * (cell_w + CTRL_PAD), y0 + (n // c) * (cell_h + CTRL_PAD),
                      cell_w, cell_h) for n in range(4)]
            mx, my = cells[0][0] + (cell_w - aw) // 2, cells[0][1] + (cell_h - ah) // 2; boxes = cells[1:]
        if not Kit.zone_up(KEY):
            Kit.art_button(g, store, "min", Kit.ART_MIN, mx, my, None, "Minimize the bar",
                           on_click=queue(("toggle_min",)))
        win["keybtn"], win["lockbtn"], win["gridbtn"] = [draw_small_button(g, box, cap, fn, *look)
                                                         for (cap, fn, look), box in zip(acts, boxes)]
    def grid_look():
        if HOST.grid_shown(): return Kit.HUE_TITLE, "Hide the screen grid windows snap to"
        return Kit.HUE_INFO, "Show the screen grid; windows you let go snap to it, the corners, edge middles and centre"
    def toggle_grid():
        on = bool(HOST.grid_toggle()); btn = win.get("gridbtn")
        if btn and Kit.is_open(win["g"]): recolor(btn, *grid_look())
        say("screen grid %s." % ("shown" if on else "hidden"))
    def lock_look():
        if HOST.layout_in_use():
            if HOST.layout_arranging(): return Kit.HUE_TITLE, "Lock every window in its zone"
            return Kit.HUE_INFO, "Unlock the layout to move windows between zones"
        if settings["lock"]: return Kit.HUE_BAD, "Locked; click to unlock the bar"
        return Kit.HUE_INFO, "Lock the bar in place"
    def refresh_lock_button():
        g, btn = win["g"], win.get("lockbtn")
        if not btn or not Kit.is_open(g): return False
        g.CanMove = not settings["lock"] and not HOST.layout_locked(KEY)
        recolor(btn, *lock_look()); win["arranging"] = HOST.layout_arranging(); return True
    WIN_PARTS = ("g", "store", "cells", "bags", "keybtn", "lockbtn", "gridbtn", "traybtn", "pagecol")
    def build_window():
        keep = dict((k, win.get(k)) for k in WIN_PARTS); old = keep["g"]
        x, y = (old.GetX(), old.GetY()) if Kit.is_open(old) else (None, None); win.setdefault("stale", []).append(old)
        win.update(dict.fromkeys(WIN_PARTS[4:]), g=None, cells={}, bags={}); store = ({}, {}); _counters[0] = None
        built = {"g": None}
        try: _draw_bar(x, y, store, built)
        except Exception:
            if win["g"] is None:
                Kit.dispose(built["g"]); win.update(keep); _counters[0] = None
                win["stale"] = [s for s in win.get("stale", []) if s is not old]
            else:
                for s in win.pop("stale", []): Kit.dispose(s)
            raise
    def _draw_bar(x, y, store, built):
        held_lock = HOST.layout_locked(KEY)
        if st["minimized"]:
            w, h = MINI_W, MINI_H
            if x is None: x, y = Kit.load_pos(POS_KEY, (200, 600), (w, h))
            g = built["g"] = G.CreateGump(True, not held_lock)
            Kit.mini_bar(g, store, w, h, TITLE, KEY, queue(("toggle_min",)), TITLE)
        else:
            refit_if_stale(); L = geom()
            w, h = bar_size(); fitst["off"] = (0, 0); slot = told_slot()
            if slot is not None:
                fitst["off"] = (max(0, (slot[0] - w) // 2), max(0, (slot[1] - h) // 2))
                w, h = max(w, slot[0]), max(h, slot[1])
            if x is None: x, y = Kit.load_pos(POS_KEY, (200, 600), (w, h))
            BAR_M, PAGE_W, p4 = L["m"], L["pw"], L["p4"]; UI_GAP, BAG_GAP, TRAY_BTN = L["ug"], L["bg"], L["tb"]
            SGX, colx, colw = L["sgx"], L["colx"], L["colw"]
            rowy, rowh, celly, cellh = L["rowy"], L["rowh"], L["celly"], L["cellh"]; x0 = BAR_M + PAGE_W
            g = built["g"] = G.CreateGump(True, not settings["lock"] and not held_lock)
            Kit.add_window_frame(g, w, h, corners=False); r = 0
            for kind, base in ([("x", k * TOP_SLOTS) for k in range(settings["extra"] - 1, -1, -1)]
                               + ([("a", 0)] if settings["top"] else [])):
                y0 = BAR_M + rowy[r]; Kit.add_resizepic(g, SLOT_FRAME, *R(x0, y0, L["top_w"], rowh[r]))
                cy, ch = y0 + celly[r], cellh[r]
                for i in range(TOP_SLOTS): draw_cell(g, (kind, base + i), *R(x0 + colx[i], cy, colw[i], ch))
                r += 1
            y0, ph = BAR_M + rowy[r], rowh[r]; cy, ch = y0 + celly[r], cellh[r]
            draw_page_column(g, store, BAR_M, y0, ph, PAGE_W)
            Kit.add_resizepic(g, SLOT_FRAME, *R(x0, y0, L["left_w"], ph))
            for i in range(BOTTOM_SLOTS): draw_cell(g, ("a", TOP_SLOTS + i), *R(x0 + colx[i], cy, colw[i], ch))
            ux = x0 + L["left_w"] + SGX; Kit.add_resizepic(g, SLOT_FRAME, *R(ux, y0, L["ui_w"], ph))
            Kit.add_tiled(g, Kit.STONE_TILE, *R(ux + p4, y0 + p4, L["ui_w"] - 2 * p4, ph - 2 * p4), alpha=0.55)
            total = UI_SLOTS * L["bw"] + (UI_SLOTS - 1) * UI_GAP; bx = ux + (L["ui_w"] - total) // 2
            for i in range(UI_SLOTS):
                draw_cell(g, ("u", i), *R(bx + i * (L["bw"] + UI_GAP), y0 + (ph - L["bh"]) // 2, L["bw"], L["bh"]))
            gx = ux + L["ui_w"] + SGX; Kit.add_resizepic(g, SLOT_FRAME, *R(gx, y0, L["bag_w"], ph))
            total = BAG_SLOTS * L["bgw"] + (BAG_SLOTS - 1) * BAG_GAP; bx = gx + (L["bag_w"] - total) // 2
            for i in range(BAG_SLOTS): draw_bag(g, i, *R(bx + i * (L["bgw"] + BAG_GAP), cy, L["bgw"], L["bgh"]))
            tx = gx + L["bag_w"] + SGX; Kit.add_resizepic(g, SLOT_FRAME, *R(tx, y0, L["tray_w"], ph))
            draw_tray_button(g, *R(tx + p4, cy, TRAY_BTN, L["bgh"])); draw_ctrl_column(g, store, L)
        if settings["anchor"] and not Kit.zone_up(KEY):
            ax, ay = Kit.anchor_pos(settings["anchor"], w, h)
            if ax is not None: x, y = ax, ay
        st["last_pos"] = Kit.show_window(g, x, y, w, h, None, False, on_disposed(g), save_pos, win,
                                         {"g": g, "store": store})
        st["moved_at"] = None
        for s in win.pop("stale", []): Kit.dispose(s)
        if not st["minimized"] and time.time() - st.get("counted_at", 0.0) > COUNT_EVERY:
            k = _cell_kinds()
            if "item" in k["types"] or k["extra"]: count_now()
        update_labels(); build_tray()
    def draw_tray_button(g, x, y, w, h):
        n = len(tray_docks()); Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        labels = add_cell_text(g, str(n), x, y, w, h, Kit.HUE_TITLE if n else Kit.HUE_INFO)
        win["traybtn"] = {"text": labels, "x": x, "w": w, "ly": y + (h - 14) // 2 - 1,
                          "catcher": Kit.catcher(g, x, y, w, h, queue(("traywin",)), tray_tip(n))}
    def tray_pos(w, h, at=None, rect=False):
        if rect is False:
            g = win["g"]
            if not Kit.is_open(g): return 300, 300
            rect = Kit.rect(g)
            if at is None: at = Kit.pos(g) or (0, 0)
        bx, by = at; bw, bh = (rect[2], rect[3]) if rect is not None and rect[2] > 0 else bar_size()
        W, H = Kit.screen()
        if flat():
            x, y = bx + bw + TRAY_GAP, by + bh - h
            if W and x + w > W:
                x = bx - TRAY_GAP - w
                if x < 0:
                    x, y = bx, by + bh + TRAY_GAP
                    if H and y + h > H: y = by - TRAY_GAP - h
        else:
            x, y = bx, by + bh + TRAY_GAP
            if H and y + h > H:
                y = by - TRAY_GAP - h
                if y < 0:
                    x, y = bx + bw + TRAY_GAP, by
                    if W and x + w > W: x = bx - TRAY_GAP - w
        return x, y
    def bar_gump(): return win["g"]
    def place_on_anchor():
        g = win["g"]
        if not settings["anchor"] or not Kit.is_open(g) or Kit.zone_up(KEY): return
        w, h = bar_size(); x, y = Kit.anchor_pos(settings["anchor"], w, h)
        if x is None: return
        if (x, y) != st.get("last_pos"):
            g.SetPos(x, y); Kit.note_rect(g, x, y); Kit.moved_by_code(g)
            st["last_pos"] = (x, y); follow_tray()
    def settle(x, y):
        if st["minimized"]: return
        if Kit.zone_up(KEY): save_pos(); return
        w, h = bar_size(); name = Kit.anchor_at(x, y, w, h, SNAP_ANCHOR)
        turn = True if name in ("L", "R") else False if name in ("T", "B") else None
        turning = turn is not None and turn != settings["vertical"]
        if name != settings["anchor"] or turning:
            settings["anchor"] = name
            if turning:
                settings["vertical"] = turn; save_settings(); want_rebuild()
                say("standing %s along the %s edge." % ("upright" if turn else "flat",
                    {"L": "left", "R": "right", "T": "top", "B": "bottom"}[name]))
                return
            save_settings()
        place_on_anchor(); save_pos()
    def watch_position(now):
        g = win["g"]
        if not Kit.is_open(g): return
        rect = Kit.rect(g); pos = (rect[0], rect[1]) if rect else (0, 0)
        if pos != st.get("last_pos"): st["last_pos"], st["moved_at"] = pos, now
        elif st.get("moved_at") is not None and now - st["moved_at"] >= 0.3 and SNAP.pressed() is not True:
            st["moved_at"] = None; settle(pos[0], pos[1])
        follow_tray(pos, rect)
        if settings["anchor"] and now >= st.get("screen_next", 0.0):
            st["screen_next"] = now + 2.0; wh = Kit.screen()
            if wh != st.get("screen_wh"):
                st["screen_wh"] = wh
                if not Kit.zone_up(KEY): place_on_anchor()
    def build_tray():
        old, tray["g"] = tray["g"], None; docks = tray_docks()
        if st["minimized"] or not settings["tray_open"] or not docks: Kit.dispose(old); return
        L = geom(); tb, bg, m = L["tb"], L["bg"], max(4, L["tm"] // 2); aw, ah = Kit.pic_size(Kit.ART_MIN[0])
        aw, ah = aw or 16, ah or 16; bh = L["bgh"]; w = m + len(docks) * (tb + bg) + aw + m; h = m + bh + m
        g = G.CreateGump(True, False); Kit.add_window_frame(g, w, h, corners=False)
        for i, (key, d) in enumerate(docks): draw_tray(g, key, d, m + i * (tb + bg), m, tb, bh)
        store = ({}, {})
        Kit.art_button(g, store, "fold", Kit.ART_MIN, w - m - aw, m + (bh - ah) // 2, None,
                       "Hide the tray (the bar's numbered button brings it back)", on_click=queue(("traywin",)))
        x, y = tray_pos(w, h); Kit.place(g, x, y, w, h); tray.update({"g": g, "at": (x, y), "w": w, "h": h})
        G.AddGump(g); Kit.attach(g, win["g"]); Kit.dispose(old)
    def follow_tray(at=None, rect=False):
        g = tray["g"]
        if not Kit.is_open(g): return
        w, h = tray.get("w", 0), tray.get("h", 0); x, y = tray_pos(w, h, at, rect)
        if (x, y) != tray["at"]: tray["at"] = (x, y); g.SetPos(*Kit.clamp(x, y, w, h)); Kit.moved_by_code(g)
    def open_spellbook():
        count_now(SPELLBOOKS)
        book = (next((s for s in (st["first_g"].get(gr) for gr in SPELLBOOKS) if s), None) or
                API.FindLayer("Spellbook"))
        if book: API.UseObject(book); return True
        say("no spellbook in your pack.", Kit.HUE_BAD); return False
    def toggle_lock():
        if HOST.layout_in_use(): HOST.layout_arrange(); refresh_lock_button(); return
        settings["lock"] = not settings["lock"]; save_settings()
        if not refresh_lock_button(): want_rebuild()
        if cfg.f is not None: cfg.f.c["lock"].IsChecked = settings["lock"]
        else: HOST.refresh_settings(KEY)
        say("%s." % ("locked" if settings["lock"] else "unlocked"), Kit.HUE_GOOD)
    def hovered_ref():
        g = win["g"]; pos = Kit.mouse_pos(); at = Kit.pos(g) if Kit.is_open(g) else None
        if pos is None or at is None: return None
        mx, my = pos[0] - at[0], pos[1] - at[1]
        for ref, info in (list(win["cells"].items()) + [(("b", i), info) for i, info in win["bags"].items()]):
            if info["x"] <= mx < info["x"] + info["w"] and info["y"] <= my < info["y"] + info["h"]: return ref
        return None
    def start_bind(ref=None):
        HOST.release_typing(); st["bind"] = {"sel": ref}; refresh_bind_button()
        say("keybind mode on: %s (Esc ends it, Backspace clears a key)." % (
            "click a cell, then press a key" if Kit.mouse_pos() is None else "hover a cell and press a key"))
    def end_bind():
        if st["bind"] is None: return
        st["bind"] = None; refresh_bind_button(); say("keybind mode off.")
    def assign_key(ref, k):
        owner = key_owner(k)
        if owner: say("%s belongs to %s; pick another." % (k, owner), Kit.HUE_BAD); return
        changed = [ref]
        for r, c in all_cells():
            if r != ref and norm_key(c["k"]) == k:
                c["k"] = ""; changed.append(r); say("%s taken off %s." % (k, ref_name(r)))
        for i, bk in enumerate(bag_keys()):
            if ("b", i) != ref and bk == k:
                set_key_of(("b", i), ""); changed.append(("b", i)); say("%s taken off bag slot %d." % (k, i + 1))
        set_key_of(ref, k)
        if ref[0] == "b": save_cells()
        register_hotkeys(); keys_changed(changed); empty = ref[0] != "b" and not cell(ref)["t"]
        say("%s bound to %s%s." % (k, ref_name(ref), " (empty; fill it to use it)" if empty else ""), Kit.HUE_GOOD)
    def on_bind_key(combo):
        b = st["bind"]
        if not b: return
        k = combo.rsplit("+", 1)[-1]
        if k == "ESCAPE": end_bind(); return
        ref = hovered_ref() or b["sel"]
        if ref is None: say("hover a cell on the bar (or click one) first."); return
        b["sel"] = ref
        if k in ("BACKSPACE", "DELETE"):
            set_key_of(ref, ""); register_hotkeys(); keys_changed([ref])
            say("%s has no hotkey now." % ref_name(ref), Kit.HUE_GOOD); return
        assign_key(ref, combo)
    def keys_changed(refs):
        for r in refs: refresh_key(r)
        shown = sel_ref(page["sel"])
        if cfg.f is not None and shown in refs: cfg.f.c["key"].SetText(cell(shown)["k"])
    def run_ui(uid):
        d = ui_def(uid)
        if d is None: say("unknown window button '%s'." % uid, Kit.HUE_BAD); return False
        how = d[3]; ok = True
        if how == "barsettings": HOST.show_settings(KEY)
        elif how == "lock": toggle_lock()
        elif how == "minimize": queue(("toggle_min",))()
        elif how == "war": API.SetWarMode(not bool(API.Player.InWarMode))
        elif how == "help": API.OpenHelp()
        elif how == "grimoire": return toggle_grimoire()
        elif how == "virtue": return toggle_va()
        elif how == "quests": API.OpenQuestLog()
        elif how == "paperdoll":
            import System
            if not ClientUI.game_action("OpenPaperdoll", [System.UInt32(int(API.Player.Serial))]):
                if Client.on_client_thread(): later(lambda: run_ui("paperdoll"))
                else: ok = safe(lambda: API.ContextMenu(API.Player, "Open Paperdoll", 2), None) is not False
        elif how.startswith("mod:"): return toggle_module(how[4:])
        elif how.startswith("ga:"):
            parts = how.split(":"); ok = ClientUI.game_action(parts[1], reuse=parts[2] if len(parts) > 2 else None)
        elif how.startswith("macro:"): ok = ClientUI.open_macro(how[6:])
        if not ok: say("couldn't open %s (%s)." % (d[1], ClientUI.error or "unknown"), Kit.HUE_BAD)
        return ok
    _legion = {"looked": False, "type": None}
    def loaded_scripts():
        if not _legion["looked"] and Client.on_client_thread():
            if not _legion.get("asked"): _legion["asked"] = True; later(loaded_scripts)
            return []
        if not _legion["looked"]:
            _legion["looked"] = True; _legion["type"] = Client._type("ClassicUO.LegionScripting.LegionScripting")
        t = _legion["type"]
        if t is None: return []
        out = []
        def get(sf, n): return str(safe(lambda: ClientUI._get(sf, n), "") or "")
        try:
            for sf in (ClientUI._get(None, "LoadedScripts", t) or []):
                rel, path = get(sf, "RelativePath") or get(sf, "FileName"), get(sf, "FullPath")
                if rel or path: out.append((rel, path))
        except Exception: pass
        return out
    _script_names = {}; _names_due = set()
    def script_names_for(v):
        v = str(v or "").strip().replace("\\", "/"); hit = _script_names.get(v)
        if hit is not None and time.time() < hit[0]: return list(hit[1])
        base = v.split("/")[-1]; low, blow = v.lower(), base.lower(); out = []
        def add(c):
            if c and c not in out: out.append(c)
        walk = not Client.on_client_thread()
        if not walk:
            if v not in _names_due:
                _names_due.add(v)
                def job(): _names_due.discard(v); script_names_for(v)
                later(job)
            if hit is not None: return list(hit[1])
        if "/" in v: add(v)
        for rel, _ in loaded_scripts():
            r = rel.replace("\\", "/"); rl = r.lower()
            if rl == low or rl.endswith("/" + low) or rl.split("/")[-1] == blow: add(r)
        if not walk: add(v); add(base); return list(out)
        root = legion_root()
        if root:
            try:
                for d, dirs, files in os.walk(root):
                    rel = d.replace("\\", "/")[len(root):].strip("/")
                    if rel.count("/") >= 2: dirs[:] = []
                    dirs[:] = [x for x in dirs if not x.startswith(".") and x.lower() not in LIB_DIRS]
                    for f in files:
                        if f.lower() == blow: add((rel + "/" + f) if rel else f)
            except Exception: pass
        add(v); add(base); _script_names[v] = (time.time() + 60.0, out); return list(out)
    _run_hint = {}
    def script_running(v):
        names = script_names_for(v); hint = _run_hint.get(v)
        if hint is not None and hint in names:
            try:
                if API.IsScriptRunning(hint): return True
            except Exception: pass
        for c in names:
            if c == hint: continue
            try:
                if API.IsScriptRunning(c):
                    if len(_run_hint) > 200: _run_hint.clear()
                    _run_hint[v] = c; return True
            except Exception: pass
        return False
    def run_script(v):
        cands = script_names_for(v); was = script_running(v); fn = API.StopScript if was else API.PlayScript
        done = False
        for c in cands:
            if not safe(lambda c=c: (fn(c), True)[1], False): continue
            done = True
            if not HOST.idle(0.1) or script_running(v) != was: break
        st["script_check"] = (v, was, time.time() + 0.5); return done
    def check_script(now):
        chk = st.get("script_check")
        if not chk or now < chk[2]: return
        st["script_check"] = None; v, was, _ = chk; on = script_running(v); name = v.replace("\\", "/").split("/")[-1]
        if was and not on: say("stopped %s." % name)
        elif not was and on: say("started %s." % name, Kit.HUE_GOOD)
        elif not was:
            say("%s didn't start; is it in the Legion Script Manager's list (refresh it)?" % name, Kit.HUE_BAD)
        update_labels()
    def use_item(c):
        def first():
            return st["first"].get((c["g"], c["h"])) or (None if settings["hue"] else st["first_g"].get(c["g"]))
        stale = time.time() - st.get("counted_at", 0.0) > COUNT_EVERY
        if stale: count_now()
        serial = first()
        if not serial and not stale: count_now(); serial = first()
        if not serial: say("no %s left." % cell_text(c), Kit.HUE_BAD); return False
        API.UseObject(serial); st["next_count"] = time.time() + 0.4; HOST.pack_dirty(); return True
    CELL_CALLS = {"spell": API.CastSpell, "skill": API.UseSkill, "dress": API.Dress, "undress": API.Undress,
                  "say": API.Msg}
    HARM_SKILLS = ("stealing", "snooping", "discordance", "provocation")
    def harmful_cell(c, t, v):
        if t == "skill":
            n = v.lower(); return bool(n) and any(n in s for s in HARM_SKILLS)
        if t == "spell":
            n = v.lower(); return bool(n) and (n in HARMFUL_SPELLS or any(s.startswith(n) for s in HARMFUL_SPELLS))
        return t == "item" and int(c.get("g") or 0) == 0x0F0D
    def must_confirm(tok, c, t, v, now):
        if c["tg"] != "last" or not harmful_cell(c, t, v): return False
        conf, st["confirm"] = st["confirm"], None
        if conf and conf[0] == tok and now <= conf[1]:
            if 0 <= now - conf[2] < 0.3: st["confirm"] = conf; return True
            return False
        gz = HOST.guarded()
        if gz is False: return False
        last = int(API.LastTargetSerial or 0); m = API.FindMobile(last) if last else None
        noto = int(safe(lambda: int(m.Notoriety), 0) or 0) if m is not None else 0
        if noto not in (1, 2) and not (m is None and last and t == "skill"): return False
        st["confirm"] = (tok, now + 3.0, now)
        say("your last target is %s and you %s a guard zone; "
                   "press again to confirm, or target by hand." % ("blue" if noto == 1 else "green" if noto == 2 else
                                                                   "not a mobile",
                    "are in" if gz is True else "may be in"), Kit.HUE_BAD)
        return True
    def run_cell(ref):
        c = cell(ref); t, v = c["t"], c["v"].strip()
        if not t: say("%s is empty." % ref_name(ref)); return
        now = time.time(); tok = (ref, settings["page"])
        if must_confirm(tok, c, t, v, now): return
        arms = c["tg"] in ("self", "last") and t not in ("travel", "say", "ui", "dress", "undress", "ability")
        w = st["want_target"]
        if w and now > w[1]: w = None
        pending_same = bool(w) and w[2] == tok; clash = False
        if w and not pending_same: drop_want(); clash = arms
        ok = True; cursor_was_up = bool(API.HasTarget("any"))
        try:
            if t in CELL_CALLS: CELL_CALLS[t](v)
            elif t == "item": ok = use_item(c)
            elif t == "macro":
                r = ClientUI.run_macro(v); ok = bool(r)
                if r is None: say("no TazUO macro named '%s'." % v, Kit.HUE_BAD)
                elif not r: say("couldn't run macro '%s' (%s)." % (v, ClientUI.error or "unknown"), Kit.HUE_BAD)
            elif t == "ability": API.ToggleAbility(v or "primary")
            elif t == "script":
                def job():
                    try: run_script(v)
                    except Exception as ex: say("%s failed (%s)." % (cell_text(c), ex), Kit.HUE_BAD)
                later(job)
            elif t == "ui": ok = run_ui(v)
            elif t == "travel": ok = fire_travel(c)
        except Exception as ex: say("%s failed (%s)." % (cell_text(c), ex), Kit.HUE_BAD); ok = False
        if ok and t in ("skill", "spell"): start_cool(t, v)
        if ok and arms and not pending_same:
            if clash: say("a target was still pending; target by hand.")
            elif cursor_was_up: say("a target cursor was already up; target by hand.")
            elif HOST.cursor_busy(KEY): say("another module is using the target cursor; target by hand.")
            else:
                wait = 2.5
                if t == "spell": info = Kit.spell_info(v); wait += info[3] if info else 0.0
                HOST.claim_cursor(KEY, wait)
                st["want_target"] = (c["tg"], time.time() + wait, tok, harmful_cell(c, t, v),
                                     int(API.LastTargetSerial or 0))
    def handle_target(now):
        w = st["want_target"]
        if not w: return
        mode, until = w[0], w[1]
        if now > until: drop_want(); return
        if not API.HasTarget("any"): return
        drop_want()
        if HOST.cursor_busy(KEY): return
        if API.HasTarget("beneficial" if w[3] else "harmful"):
            say("that cursor isn't this cell's; target by hand."); return
        if mode == "self": API.TargetSelf()
        else:
            last = w[4] if w[3] else int(API.LastTargetSerial or 0)
            if last: API.Target(last)
            else: say("no last target yet; target by hand.")
    def drop_want(): st["want_target"] = None; HOST.release_cursor(KEY)
    def pick(action):
        drop_want()
        def done(serial): st["queue"].append(tuple(action) + (int(serial or 0),))
        HOST.pick_target(15, done)
    def pick_item(ref):
        say("target an item for %s (Esc to cancel)." % ref_name(ref)); pick(("picked_item", ref, settings["page"]))
    def picked_item(ref, pg, serial):
        if st["shutting"] or HOST.aborting(): return
        item = Kit.find_item(serial)
        if item is None: say("no item picked."); return
        gr, hu = int(item.Graphic or 0), int(item.Hue or 0)
        name = str(item.Name or "") or ("0x%04X" % gr); where = ref_name(ref); refs = [ref]
        if ref[0] == "a" and ref[1] >= TOP_SLOTS and pg != settings["page"] and cells["pages"]:
            target = cells["pages"][pg][ref[1] - TOP_SLOTS]
            where = "page %d cell %d" % (pg + 1, ref[1] - TOP_SLOTS + 1); refs = []
        else: target = cell(ref)
        target.update({"t": "item", "v": "", "g": gr, "h": hu, "n": name})
        for k in TRAVEL_KEYS: target.pop(k, None)
        cells_changed(recount=True, refs=refs); say("%s set on %s." % (name, where), Kit.HUE_GOOD)
    def pick_bag(i): say("target a bag for bag slot %d (Esc to cancel)." % (i + 1)); pick(("picked_bag", i))
    def picked_bag(i, serial):
        if st["shutting"] or HOST.aborting(): return
        item = Kit.find_item(serial)
        if item is None or not item.IsContainer:
            say("that isn't a bag.", Kit.HUE_BAD); return
        set_picked_bag(i, serial); st["next_scan"] = 0.0
    def on_cell_click(ref):
        if st["bind"] is not None:
            st["bind"]["sel"] = ref; say("%s; now press a key or combination for it." % ref_name(ref))
        elif cell(ref)["t"]: run_cell(ref)
        elif ref[0] in ("a", "x"): pick_item(ref)
        else: open_menu(ref)
    def on_bag_click(i):
        if st["bind"] is not None:
            st["bind"]["sel"] = ("b", i); say("bag slot %d; now press a key or combination for it." % (i + 1)); return
        b = bag_at(i)
        if settings["bagmode"] == 1 and b is None: pick_bag(i); return
        if settings["bagmode"] == 0:
            state = ub_state()
            if state in ("collapsed", "docked"): ub_send("show"); heartbeat()
            elif state == "open": heartbeat(); ub_send("dock")
            else:
                serial = b["s"] if b else None
                turn_on(UB_MODULE_KEY, "Bags", (lambda: API.UseObject(serial)) if serial else None)
        elif b is None: say("no bag in that slot (see Bag slots on the Action Bar settings page).")
        else: API.UseObject(b["s"])
    CATS = [("item", "Item...")] + [(k, dict(TYPES)[k])
                                    for k in "spell skill ability ui macro script dress undress say travel".split()]
    MENU_CAPS = dict(CATS + [("hotkey", "Hotkey"), ("lo", "Red at")])
    LIST_TITLES = {"macro": "TazUO macros", "script": "Legion scripts",
                   "dress": "Dress outfits", "undress": "Dress outfits"}
    def legion_root():
        base = Kit.script_dir().replace("\\", "/").rstrip("/"); parent = os.path.dirname(base)
        return parent if parent and parent != base else base
    LIB_DIRS = ("iplib", "lib", "libs", "library", "site-packages", "dlls", "stubs",
                "__pycache__", "api", "docs", "examples", "virtueassistantmodules")
    def script_names():
        root_dir = legion_root(); rl = root_dir.lower(); out = []
        for name, path in loaded_scripts():
            p = path.replace("\\", "/")
            rel = (p[len(root_dir):].strip("/") if root_dir and p.lower().startswith(rl) else (p or name))
            parts = rel.lower().split("/")
            if any(d in LIB_DIRS for d in parts[:-1]) or parts[-1].startswith("_"): continue
            if rel and rel not in out: out.append(rel)
        if out or not root_dir: return sorted(out, key=lambda s: s.lower())
        try:
            for root, dirs, files in os.walk(root_dir):
                rel = root.replace("\\", "/")[len(root_dir):].strip("/")
                if rel.count("/") >= 2 or "__init__.py" in files:
                    dirs[:] = []
                    if "__init__.py" in files: continue
                dirs[:] = [d for d in dirs if not d.startswith(".") and d.lower() not in LIB_DIRS]
                for f in files:
                    if f.lower().endswith(".py") and not f.startswith("_"): out.append((rel + "/" + f) if rel else f)
        except Exception: pass
        return sorted(out, key=lambda s: s.lower())
    def saved_list(cat):
        if cat == "macro": return ClientUI.macro_names()
        if cat == "script": return script_names()
        return list(API.GetAvailableDressOutfits() or [])
    TEXT_HINT = {"macro": "The name of a macro from TazUO's macro window",
                 "script": "The script's file name (heal.py, or Spells/Bless.py)",
                 "dress": "An outfit name from TazUO's dress agent",
                 "undress": "An outfit name from TazUO's dress agent", "say": "The text to say in game",
                 "hotkey": "A key or combination (F5, CTRL+Q, SHIFT+F2; blank = none)",
                 "lo": "The counter turns red at this many or fewer (0 = only when none)"}
    def _cell_rect(info):
        at = Kit.pos(win["g"]) if Kit.is_open(win["g"]) and info is not None else None
        return None if at is None else (at[0] + info["x"], at[1] + info["y"], info["w"], info["h"])
    def menu_place(w, h):
        a = menu.get("anchor")
        if menu.get("moved") is not None: x, y = menu["moved"]
        elif a is None: x, y = 300, 300
        else: ax, ay, _, ah = a; x, y = ax, ay + ah + 2
        W, H = Kit.screen()
        if W and H:
            if a is not None and menu.get("moved") is None and y + h > H: y = ay - 2 - h
            x, y = max(0, min(x, W - w)), max(0, min(y, H - h))
        return int(x), int(y)
    def close_menu(): g, menu["g"] = menu["g"], None; menu["c"] = {}; Kit.dispose(g)
    def menu_disposed(g):
        def handler(*args):
            if menu["g"] is g: menu["g"] = None; menu["c"] = {}
        return handler
    def open_menu(ref, bag=None):
        menu.update({"ref": ref, "bag": bag, "level": "cats" if ref else "bag", "cat": None,
                     "page": 0, "moved": None, "placed": None,
                     "anchor": _cell_rect(win["cells"].get(ref) if ref else win["bags"].get(bag))})
        build_menu()
    def in_pages(rows): return [rows[i:i + MENU_ROWS * MENU_COLS] for i in range(0, len(rows), MENU_ROWS * MENU_COLS)]
    def menu_entries():
        lvl, cat = menu["level"], menu["cat"]
        if lvl == "bag":
            i = menu["bag"]; rows = []
            if settings["bagmode"] == 1:
                rows += [("Pick a bag...", ("pickbag", i)), ("Clear this slot", ("clearbag", i))]
            elif settings["bagmode"] == 0:
                s = ub_state()
                if s in ("collapsed", "docked"): rows.append(("Show the Bags window", ("ub", "show")))
                elif s == "open": rows.append(("Fold the Bags window into the bar", ("ub", "dock")))
                else: rows.append(("Turn Bags on", ("ub", "on")))
                if UB_MODULE_KEY in HOST.by_key: rows.append(("Bags settings", ("ub", "settings")))
            else: b = bag_at(i); rows.append(("Open %s" % b["n"] if b else "No bag here", ("bag", i)))
            rows.append(("Hotkey: %s" % (bag_keys()[i] or "none"), ("bagbind", i)))
            rows.append(("Bag slots: " + BAG_MODES[settings["bagmode"]], ("bagmode", None))); return rows, None
        if lvl == "cats":
            c = cell(menu["ref"]); rows = [(cap, ("cat", key)) for key, cap in CATS]
            tg = {"self": "self", "last": "last target"}.get(c["tg"], "none")
            rows += [("-", None), ("Hotkey: %s" % (c["k"] or "none"), ("cat", "hotkey")),
                     ("Press a key for it", ("bindsel", None)), ("Then target: %s" % tg, ("target", None))]
            if c["t"] in ("item", "travel"): rows.append(("Red at: %d or fewer" % max(0, c["lo"]), ("cat", "lo")))
            rows += [("Clear cell", ("clear", None)), ("More on the settings page", ("settings", None))]
            return rows, None
        if lvl == "method": return [(cap, ("tset", m)) for m, cap in TRAVEL_WAYS], None
        if lvl == "list":
            if cat == "spell":
                pages = [[(n, ("set", ("spell", n))) for n in names.split("|")] for _, names in SPELL_SCHOOLS]
                titles = SCHOOL_NAMES
            elif cat == "skill": pages, titles = [[(n, ("set", ("skill", n))) for n in SKILLS]], ["Skills"]
            elif cat == "ability":
                pages, titles = [[("Primary ability", ("set", ("ability", "primary"))),
                                  ("Secondary ability", ("set", ("ability", "secondary")))]], ["Weapon ability"]
            elif cat == "travel":
                if HOST.services.get("grimoire.destinations") is None:
                    rows = [("Grimoire is off: click to turn it on", ("grimon", None))]
                elif not menu["items"]: rows = [("No runebook read yet: open Grimoire's runebook tabs", ("none", None))]
                else:
                    rows = [(fit("%s  (%s)" % (d["name"], d["book_name"]), 260), ("tdest", i))
                            for i, d in enumerate(menu["items"])]
                pages = in_pages(rows); titles = ["Runebook destinations"] * len(pages)
            elif cat in LIST_TITLES:
                rows = [(fit(n, 220), ("set", (cat, n))) for n in menu["items"]]
                if not rows: rows = [("Nothing saved in TazUO yet", ("none", None))]
                rows.append(("Type a name", ("typed", cat))); pages = in_pages(rows)
                titles = [LIST_TITLES[cat]] * len(pages)
            else:
                pages = [[(d[1], ("set", ("ui", d[0]))) for d in UI_ACTIONS]]; titles = ["Client windows"]
                mods = [(d[1], ("set", ("ui", d[0]))) for d in mod_actions()]
                if mods: pages.append(mods); titles.append("Module windows")
            p = max(0, min(len(pages) - 1, menu["page"])); menu["page"] = p; return pages[p], (titles[p], p, len(pages))
        return [], None
    def build_menu(): Kit.on_client(_build_menu_now)
    def _build_menu_now():
        old = menu["g"]; pos = Kit.pos(old) if Kit.is_open(old) else None
        if pos is not None and menu.get("placed") is not None and pos != menu["placed"]: menu["moved"] = pos
        menu["g"], menu["stale"] = None, old; store, c = ({}, {}), {}; M, GAP = Kit.MARGIN, Kit.GAP
        rows, paged = menu_entries(); lvl, ref = menu["level"], menu["ref"]
        if lvl == "bag": title = "BAG SLOT %d" % (menu["bag"] + 1)
        elif lvl == "method": title = "TRAVEL TO %s" % str((menu.get("dest") or {}).get("name", "?")).upper()
        elif lvl in ("list", "text"):
            cap = MENU_CAPS.get(menu["cat"], "Hotkey")
            title = "%s: %s" % (ref_name(ref).upper(), cap.replace("...", "").upper())
        else: title = "SET " + ref_name(ref).upper()
        tw = Kit.text_w(title) + 60
        if lvl == "text": w = max(tw, 340); body_h = 92
        else:
            ncol = max(1, min(MENU_COLS, (len(rows) + MENU_ROWS - 1) // MENU_ROWS))
            nrow = (len(rows) + ncol - 1) // ncol if rows else 1
            col_w = max([Kit.text_w(r[0]) for r in rows] + [100]) + 24; w = max(tw, 2 * M + 16 + ncol * col_w)
            body_h = 10 + nrow * MENU_ROW_H + (34 if paged else 10)
        IW = w - 2 * M; h = M + 30 + GAP + body_h + M; g = G.CreateGump(True, True)
        Kit.add_window_frame(g, w, h, corners=False); Kit.add_section(g, M, M, IW, 30)
        Kit.add_label(g, title, M + 10, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 34, M + 4, None, "Close",
                       on_click=queue(("mpick", "close", None)))
        if lvl not in ("cats", "bag"):
            Kit.art_button(g, store, "back", Kit.ART_RESTORE, w - M - 54, M + 7, None, "Back to the previous menu",
                           on_click=queue(("mpick", "back", None)))
        yb = M + 30 + GAP; Kit.add_section(g, M, yb, IW, body_h)
        if lvl == "text":
            cur = cell(ref)
            if menu["cat"] == "lo": val = str(max(0, cur["lo"]))
            else: val = cur["k"] if menu["cat"] == "hotkey" else (cur["v"] if cur["t"] == menu["cat"] else "")
            Kit.add_label(g, TEXT_HINT.get(menu["cat"], ""), M + 10, yb + 8, Kit.HUE_INFO)
            c["text"] = Kit.add_textbox(g, val, M + 10, yb + 32, IW - 20, numbers=False)
            Kit.art_button(g, store, "ok", Kit.ART_OK, M + 10, yb + 62, "Apply", "Save this value on the cell",
                           on_click=queue(("mpick", "text", None)))
            c["status"] = Kit.add_label(g, "", M + 10 + 35 + Kit.text_w("Apply") + 12, yb + 65, Kit.HUE_INFO)
        else:
            for i, (cap, action) in enumerate(rows):
                col, row = divmod(i, nrow); x = M + 8 + col * col_w; y = yb + 6 + row * MENU_ROW_H
                if action is None: Kit.add_tiled(g, Kit.STONE_TILE, x, y + MENU_ROW_H // 2, col_w - 16, 1); continue
                now = action[0] == "set" and (cell(ref)["t"], cell(ref)["v"]) == action[1] \
                    or action[0] in ("tdest", "tset") and travel_now(ref, action)
                Kit.add_label(g, cap, x + 4, y + 2, Kit.HUE_GOOD if now else Kit.HUE_TEXT)
                Kit.catcher(g, x, y, col_w - 8, MENU_ROW_H, queue(("mpick",) + tuple(action)), cap)
            if paged:
                name, p, n = paged; py = yb + body_h - 28
                Kit.add_label(g, "%s  (%d of %d)" % (name, p + 1, n), M + 10, py + 4, Kit.HUE_INFO)
                if n > 1:
                    Kit.art_button(g, store, "next", Kit.ART_PAGE, w - M - 44, py, None,
                                   "Next page", on_click=queue(("mpick", "page", 1)))
                    Kit.art_button(g, store, "prev", Kit.ART_PAGE, w - M - 84, py, None,
                                   "Previous page", on_click=queue(("mpick", "page", -1)))
        x, y = menu_place(w, h); x, y = Kit.place(g, x, y, w, h)
        menu.update({"g": g, "c": c, "placed": (x, y)}); G.AddControlOnDisposed(g, menu_disposed(g)); G.AddGump(g)
        g.SetInScreen(); Kit.dispose(menu.pop("stale", None))
    def set_cell(ref, t, v):
        cur = cell(ref); new = dict(blank(), t=t, v=v, k=cur["k"], tg=cur["tg"], lo=cur["lo"])
        cells[ref[0]][ref[1]] = new; cells_changed(recount=True, refs=[ref])
        say("%s set on %s." % (cell_text(new), ref_name(ref)), Kit.HUE_GOOD)
    def travel_now(ref, action):
        c = cell(ref)
        if c["t"] != "travel": return False
        if action[0] == "tdest": items = menu["items"]; d = items[action[1]] if 0 <= action[1] < len(items) else None
        else:
            d = menu.get("dest")
            if c.get("rm") != action[1]: return False
        if not d: return False
        try: return (int(c.get("rb") or "0", 16) == int(d["book"]) and c.get("ri") == str(int(d["index"])))
        except (ValueError, TypeError, KeyError): return False
    def menu_to(**kw): menu.update(kw); build_menu()
    def menu_pick(what, arg):
        ref = menu["ref"]
        if what in ("close", "bindsel", "bagbind", "set", "settings", "pickbag", "clearbag",
                    "ub", "bag", "bagmode", "tset", "grimon") or (what, arg) == ("cat", "item"):
            close_menu()
        if what in MENU_ACTS: MENU_ACTS[what](ref, arg)
        elif what == "back":
            if menu["level"] == "method": menu_to(level="list", cat="travel")
            else: menu_to(level="cats", cat=None, page=0)
        elif what == "cat" and arg == "travel":
            fn = HOST.services.get("grimoire.destinations")
            menu_to(items=list(safe(fn, []) or []) if fn is not None else [], level="list", cat="travel", page=0)
        elif what == "tdest" and menu["level"] == "list" and menu["cat"] == "travel" and 0 <= arg < len(menu["items"]):
            menu_to(level="method", dest=menu["items"][arg])
        elif what == "tset" and menu.get("dest") and ref is not None: set_travel(ref, menu["dest"], arg)
        elif what == "cat" and arg == "item": pick_item(ref)
        elif what == "cat" and arg in LIST_TITLES and Client.on_client_thread():
            def job():
                items = saved_list(arg)
                if menu["ref"] == ref and menu["level"] == "cats" and Kit.is_open(menu["g"]):
                    menu_to(items=items, level="list", cat=arg, page=0)
            later(job)
        elif what == "cat" and arg in ("spell", "skill", "ability", "ui", "macro", "script", "dress", "undress"):
            menu_to(items=saved_list(arg) if arg in LIST_TITLES else [], level="list", cat=arg, page=0)
        elif what in ("cat", "typed"): menu_to(level="text", cat=arg)
        elif what == "text":
            v = str(menu["c"]["text"].Text or "").strip()
            if menu["cat"] == "hotkey":
                k = norm_key(v); owner = key_owner(k)
                if owner: Kit.set_text(menu["c"]["status"], "%s belongs to %s" % (k, owner), Kit.HUE_BAD); return
                if k: assign_key(ref, k)
                else: cell(ref)["k"] = ""; cells_changed(refs=[ref])
                close_menu()
            elif menu["cat"] == "lo":
                try: lo = int(v)
                except ValueError: Kit.set_text(menu["c"]["status"], "Type a number", Kit.HUE_BAD); return
                cell(ref)["lo"] = max(0, lo); cells_changed(refs=[ref]); close_menu()
            elif not v: Kit.set_text(menu["c"]["status"], "Type a value first", Kit.HUE_BAD)
            else: close_menu(); set_cell(ref, menu["cat"], v)
        elif what == "target":
            c = cell(ref); c["tg"] = {"": "self", "self": "last", "last": ""}.get(c["tg"], ""); save_cells()
            want_redraw([ref]); HOST.refresh_settings(KEY); build_menu()
        elif what == "clear": clear_cell(ref); close_menu()
        elif what == "settings": page["sel"] = ref_sel(ref); HOST.show_settings(KEY); HOST.refresh_settings(KEY)
        elif what == "clearbag": set_picked_bag(arg, 0); st["next_scan"] = 0.0
        elif what == "ub":
            if arg == "settings":
                if UB_MODULE_KEY in HOST.by_key: HOST.show_settings(UB_MODULE_KEY)
            elif arg == "on": turn_on(UB_MODULE_KEY, "Bags")
            else: heartbeat(); ub_send(arg)
    MENU_ACTS = {"bindsel": lambda ref, arg: start_bind(ref), "bagbind": lambda ref, arg: start_bind(("b", arg)),
                 "set": lambda ref, arg: set_cell(ref, arg[0], arg[1]), "pickbag": lambda ref, arg: pick_bag(arg),
                 "bag": lambda ref, arg: on_bag_click(arg), "bagmode": lambda ref, arg: HOST.show_settings(KEY),
                 "grimon": lambda ref, arg: turn_on(GRIM_MODULE_KEY, "Grimoire"),
                 "page": lambda ref, arg: menu_to(page=menu["page"] + arg)}
    def use(ref):
        if ref[0] == "b": on_bag_click(ref[1])
        else: run_cell(ref)
    def use_now(ref):
        try: use(ref)
        except Exception as ex: say("%s failed (%s)." % (ref_name(ref), ex), Kit.HUE_BAD)
    _hk = {"ok": None, "held": {}, "map": {}, "hooks": None}
    def sdl_combo(k):
        parts, key = norm_key(k).split("+"), None
        for p in parts:
            if p and p not in ("CTRL", "SHIFT", "ALT"): key = p if p.startswith("SDLK_") else "SDLK_" + p
        mods = [m for m in ("CTRL", "SHIFT", "ALT") if m in parts]; return "+".join(mods + ([key] if key else []))
    def legion_combo(sdl): return "+".join(p[5:] if p.startswith("SDLK_") else p for p in str(sdl).upper().split("+"))
    def direct_ok(ref):
        if ref[0] == "b":
            return (st["bind"] is None and bag_at(ref[1]) is not None and
                    (settings["bagmode"] != 0 or st["ub_state"] is not None))
        c = cell(ref)
        if c["t"] == "ui":
            d = ui_def(c["v"]); how = d[3] if d else ""
            return (how in ("war", "help", "quests", "paperdoll", "lock", "minimize") or
                    how.startswith(("ga:", "macro:")))
        return c["t"] in ("item", "spell", "skill", "ability", "macro", "say", "dress", "undress", "travel")
    def _hk_down(combo):
        try:
            if not _hk["ok"]: return
            combo = str(combo); base = combo.rsplit("+", 1)[-1]; now, held = time.time(), _hk["held"]
            at = held.get(base); held[base] = now
            if at is not None and now - at < HELD_KEY_STALE: return
            if len(held) > 32:
                for k in [k for k, t in held.items() if now - t >= HELD_KEY_STALE]: del held[k]
            if st["shutting"] or win["g"] is None: return
            if st["bind"] is not None:
                if not HOST.typing(): st["queue"].append(("bindkey", legion_combo(combo))); HOST.poke()
                return
            ref = _hk["map"].get(combo)
            if ref is None or HOST.typing(): return
            if direct_ok(ref): use_now(ref)
            else: st["queue"].append(("use", ref)); HOST.poke()
        except Exception: pass
    def _hk_up(combo):
        try: _hk["held"].pop(str(combo).rsplit("+", 1)[-1], None)
        except Exception: pass
    def _hk_install():
        if _hk["ok"] is not None: return
        _hk["ok"] = False
        try:
            import clr; import System; from System.Reflection import BindingFlags
            flags = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
            kb = Client._type("ClassicUO.Input.Keyboard")
            evd, evu = kb.GetEvent("KeyDownEvent", flags), kb.GetEvent("KeyUpEvent", flags)
            dd = clr.GetPythonType(evd.EventHandlerType)(_hk_down); du = clr.GetPythonType(evu.EventHandlerType)(_hk_up)
            evd.GetAddMethod(True).Invoke(None, System.Array[object]([dd]))
            try: evu.GetAddMethod(True).Invoke(None, System.Array[object]([du]))
            except Exception: evd.GetRemoveMethod(True).Invoke(None, System.Array[object]([dd])); raise
            _hk.update({"hooks": (evd, dd, evu, du), "ok": True, "held": {}})
        except Exception as ex: say("couldn't read the keyboard, so cell hotkeys are off (%s)." % ex, Kit.HUE_BAD)
    def _hk_remove():
        hooks, _hk["hooks"] = _hk["hooks"], None; _hk["ok"] = None if hooks else _hk["ok"]; _hk["map"] = {}
        if not hooks: return
        import System; evd, dd, evu, du = hooks
        safe(lambda: evd.GetRemoveMethod(True).Invoke(None, System.Array[object]([dd])))
        safe(lambda: evu.GetRemoveMethod(True).Invoke(None, System.Array[object]([du])))
    _told = set()
    def tell_once(what, text):
        if what not in _told: _told.add(what); say(text, Kit.HUE_BAD)
    def register_hotkeys():
        seen = {}
        for r, c in all_cells():
            k = norm_key(c["k"])
            if not k or not c["t"] or not shown(r): continue
            owner = key_owner(k)
            if owner: tell_once((k, owner), "%s belongs to %s; %s has no hotkey." % (k, owner, ref_name(r))); continue
            if k in seen: tell_once((k, "two cells"), "%s is on two cells; %s gets it." % (k, ref_name(r)))
            seen[k] = r
        for i, k in enumerate(bag_keys()):
            if k and not key_owner(k): seen[k] = ("b", i)
        _hk["map"] = dict((sdl_combo(k), ref) for k, ref in seen.items()) if _hk["ok"] else {}
    def page_table(w):
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
                ("HOW TO USE IT", [("note", line) for para in HELP for line in Kit.wrap(para, w - 24)]))
    def dd_index(dd, default):
        try: return int(dd.GetSelectedIndex())
        except Exception: return default
    def buttons(f, by, specs): return Kit.buttons(f.g, f.store, f.x + 12, by, specs, 16)
    def drop_down(f, lx, ry, label, key, dw, pairs, value, tooltip):
        Kit.add_label(f.g, label, lx, ry + 2); codes = [p[0] for p in pairs]
        page["dds"].append((key, lx + Kit.text_w(label) + 8, ry, dw, [p[1] for p in pairs],
                            codes.index(value) if value in codes else 0, tooltip))
        return lx + Kit.text_w(label) + 8 + dw + 16
    def draw_ub_state(f, x, y):
        found = st["ub_found"]; state = ub_state()
        ub = ({"open": "Bags: shown", "collapsed": "Bags: folded",
               "docked": "Bags: in the bar"}.get(state) if state else "Bags: off" if found else
              "Bags: not found" if found is False else "Bags: not in use")
        found = found or state is not None; col = (f.w - 24) // 3
        Kit.add_label(f.g, fit(ub, col - 6), x + 12 + 2 * col, y + 2, Kit.HUE_GOOD if found else Kit.HUE_INFO)
    def draw_bag_mode(f, x, y):
        drop_down(f, x + f.w - 12 - 170 - 8 - Kit.text_w("Bag slots:"), y, "Bag slots:", "bagmode", 170,
                  list(enumerate(BAG_MODES)), settings["bagmode"],
                  "Where the bag slots get bags: Inventory > Bags, bags you target, or your backpack and its bags")
    def draw_page_buttons(f, x, y):
        bx = buttons(f, y, (("pgprev", Kit.ART_PAGE, "Prev", "Show the previous bottom-left page"),
                            ("pgnext", Kit.ART_PAGE, "Next", "Show the next bottom-left page"),
                            ("bind", Kit.ART_PLAY, "Keybind mode", "Start keybind mode: hover a cell and press a key")))
        Kit.add_label(f.g, fit("Bar page %d of %d" % (settings["page"] + 1, PAGES), x + f.w - 16 - bx), bx, y + 3,
                      Kit.HUE_INFO)
    def draw_anchor(f, x, y):
        sx = x + 12 + Kit.text_w("Extra rows:") + 8; anch = settings["anchor"]
        where = {"": "none (drop near a corner or edge middle)", "L": "left edge, upright", "R": "right edge, upright",
                 "T": "top edge", "B": "bottom edge", "C": "screen centre"}.get(
            anch, {"TL": "top-left", "TR": "top-right", "BL": "bottom-left",
                   "BR": "bottom-right"}.get(anch, anch) + " corner")
        Kit.add_label(f.g, fit("Anchor: %s" % where, x + f.w - 16 - (sx + 130)), sx + 130, y + 2, Kit.HUE_INFO)
    def draw_edit(f, x, y):
        g, c, w = f.g, f.c, f.w; sel = page["sel"]; cur = cell(sel_ref(sel))
        lx = drop_down(f, x + 12, y, "Cell:", "sel", 120, list(enumerate(sel_names())), sel,
                       "The cell to edit (right-clicking a cell on the bar does the same)")
        lx = drop_down(f, lx, y, "Does:", "does", 150, TYPES, cur["t"], "What a click or the hotkey does")
        drop_down(f, lx, y, "Target:", "target", 100, TARGETS, cur["tg"],
                  "Answer the cell's target cursor with yourself or your last target (when no other module holds it)")
        Kit.add_label(g, "Value:", x + 12, y + 34)
        if cur["t"] == "item": val = ("0x%04X" % cur["g"]) + ((",%d" % cur["h"]) if cur["h"] else "")
        elif cur["t"] == "ui": val = ""
        elif cur["t"] == "travel": val = travel_what(cur)
        else: val = cur["v"]
        vx = x + 12 + max(Kit.text_w("Value:"), Kit.text_w("Window:")) + 8
        c["value"] = Kit.with_tip(Kit.add_textbox(g, val, vx, y + 32, x + w - 16 - vx, numbers=False),
                                  "The cell's value (see below; a Client window cell uses Window)")
        Kit.add_label(g, "Window:", x + 12, y + 66); ua = ui_all(); uids = [d[0] for d in ua]
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
        if not cells["a"]: load_cells()
        page["dds"] = []; f = cfg.build(g, x, y, w)
        for key, dx, dy, dw, items, idx, tooltip in sorted(page["dds"], key=lambda d: -d[2]):
            dd = G.CreateDropDown(dw, items, idx); dd.SetPos(dx, dy); g.Add(dd); f.c[key] = Kit.with_tip(dd, tooltip)
        page.update({"seen_sel": page["sel"], "seen_bag": settings["bagmode"]})
    def set_status(text, hue=None):
        if cfg.f is not None: Kit.set_text(cfg.f.c["status"], text, Kit.HUE_INFO if hue is None else hue)
    def apply_edit():
        c = cfg.f.c; ref = sel_ref(page["sel"]); cur = cell(ref)
        def chosen(lst, dd): return lst[max(0, min(len(lst) - 1, dd_index(dd, 0)))][0]
        t = chosen(TYPES, c["does"]); v = str(c["value"].Text or "").strip()
        tg = chosen(TARGETS, c["target"]); k = norm_key(c["key"].Text); owner = key_owner(k)
        if owner: set_status("%s belongs to %s" % (k, owner), Kit.HUE_BAD); return
        try: lo = int(str(c["lo"].Text or "0"))
        except Exception: lo = LOW_DEFAULT
        new = dict(blank(), t=t, tg=tg, k=k, lo=lo)
        if t == "item":
            gh = parse_graphic(v)
            if gh is None and cur["t"] == "item" and cur["g"]: gh = (cur["g"], cur["h"])
            if gh is None: set_status("Pick an item, or type its graphic", Kit.HUE_BAD); return
            new.update({"g": gh[0], "h": gh[1], "n": cur["n"] if (cur["g"], cur["h"]) == gh else "0x%04X" % gh[0]})
        elif t == "ui": new["v"] = chosen(ui_all(), c["window"])
        elif t == "ability": new["v"] = "secondary" if v.lower().startswith("s") else "primary"
        elif t == "travel":
            if cur["t"] != "travel":
                set_status("Pick its destination: right-click the cell, then Travel (runebook)", Kit.HUE_BAD); return
            new["tg"] = ""
            for k in ("v", "n") + TRAVEL_KEYS: new[k] = cur.get(k, "")
        elif t:
            if not v: set_status("Type a value first", Kit.HUE_BAD); return
            new["v"] = v
        cells[ref[0]][ref[1]] = new
        if new["k"] and new["k"] != norm_key(cur["k"]): assign_key(ref, new["k"])
        cells_changed(recount=True, refresh=False, refs=[ref]); set_status("Saved %s" % ref_name(ref), Kit.HUE_GOOD)
    def page_clicks(f):
        for key, action in (("pgprev", ("page", -1)), ("pgnext", ("page", 1)), ("bind", ("bind",))):
            if Kit.was_clicked(f.store, key): queue(action)()
        if Kit.was_clicked(f.store, "apply"): apply_edit()
        if Kit.was_clicked(f.store, "pick"): queue(("pick", sel_ref(page["sel"])))(); set_status("Target the item")
        if Kit.was_clicked(f.store, "clear"): clear_cell(sel_ref(page["sel"]))
    def read_dropdowns(f, new):
        bm = dd_index(f.c["bagmode"], settings["bagmode"])
        if bm != page["seen_bag"] and 0 <= bm < len(BAG_MODES): page["seen_bag"] = new["bagmode"] = bm
        sel = dd_index(f.c["sel"], page["sel"])
        if sel != page["seen_sel"] and 0 <= sel < ACTION_SLOTS + UI_SLOTS + EXTRA_SLOTS:
            page["sel"] = sel; HOST.refresh_settings(KEY)
    def settings_changed(old, new):
        if new["bagmode"] != old["bagmode"]: st["bag_sig"], st["next_scan"] = None, 0.0
        register_hotkeys(); want_rebuild(0.4)
    cfg = Kit.Page(settings, page_table, save_settings, settings_changed, adjust=read_dropdowns, clicks=page_clicks,
                   every=0.2)
    cleanup = Kit.Cleanup()
    def _start():
        st.update(fresh(), minimized=Kit.load_min(MIN_KEY), ub_last=None, ub_pending=True, counted_at=0.0)
        _told.clear(); _hk["held"] = {}; fitst.update(scale=None, vertical=None, slot=None, sig=None)
        load_settings(); load_cells(); scan_bags()
        st["ub_state"], st["grim_state"], st["va_state"] = ub_state(), grim_state(), va_state(); heartbeat()
        HOST.layout_add(KEY, bar_gump, TITLE, LAYOUT_HOOKS); cleanup.add(HOST.layout_remove, KEY)
        st.update(dock_sig=dock_sig(), tray_sig=tray_sig(), watch_next=0.0, owned_sig=frozenset(HOST.hotkeys_owned))
        build_window(); st.update(rebuild_at=0.0, redraw=set()); _hk_install(); register_hotkeys()
        cleanup.service("actionbar.hotkeys", hotkeys_service)
    ON_ACTION = {"click": on_cell_click, "use": use, "bag": on_bag_click, "ui": run_ui,
                 "pick": pick_item, "menu": open_menu, "mpick": menu_pick,
                 "picked_item": picked_item, "picked_bag": picked_bag,
                 "bindkey": on_bind_key, "lockbar": toggle_lock, "grid": toggle_grid,
                 "bagmenu": lambda i: open_menu(None, i), "page": lambda step: set_page(settings["page"] + step),
                 "bind": lambda: start_bind() if st["bind"] is None else end_bind()}
    def _tick():
        if st["shutting"] or win["g"] is None: return
        if Kit.closed(win): return
        now = time.time(); handle_target(now); check_script(now); watch_ub()
        arr = HOST.layout_arranging()
        if arr != win.get("arranging", False):
            win["arranging"] = arr
            if win.get("lockbtn"): recolor(win["lockbtn"], *lock_look())
        while st["queue"]:
            action = st["queue"].pop(0); kind = action[0]
            if kind in ON_ACTION: ON_ACTION[kind](*action[1:])
            elif kind == "dock":
                d = dict(all_docks()).get(action[1])
                if d is not None:
                    s = safe(d.get("state"))
                    if s is None:
                        if d.get("on"): safe(d["on"])
                        else: later(lambda k=action[1]: safe(lambda: HOST.enable(k)))
                    elif s == "open": HOST.dock_to_bar(action[1])
                    else: safe(d.get("show"))
                    st["dock_sig"], st["watch_next"] = None, 0.0
            elif kind == "traywin": settings["tray_open"] = not settings["tray_open"]; save_settings(); refresh_tray()
            elif kind == "toggle_min":
                if Kit.zone_up(KEY) and not st["minimized"]: continue
                save_pos(); st["minimized"] = not st["minimized"]; Kit.save_min(MIN_KEY, st["minimized"]); heartbeat()
                want_rebuild()
            if st["shutting"] or win["g"] is None: return
        now = time.time()
        if now >= st["next_scan"]:
            st["next_scan"] = now + 2.0; scan_bags(); scan_abilities(); heartbeat()
            if st.get("last_pos") != st.get("pos_saved"): save_pos()
        if st["rebuild_at"] and now >= st["rebuild_at"]: st["rebuild_at"] = 0.0; st["redraw"] = set(); build_window()
        elif st["redraw"]: redraw_now()
        if now >= st["next_count"]: st["next_count"] = now + COUNT_EVERY; refresh_counts()
        cool_tick(now)
        if now >= st.get("tray_next", 0.0): st["tray_next"] = now + 0.1; watch_position(now)
    def _thread_tick():
        while st["jobs"] and not st["shutting"]: st["jobs"].pop(0)()
    def _stop():
        st["shutting"] = True; cleanup.close(); drop_want(); g, tray["g"] = tray["g"], None; Kit.dispose(g)
        st["bind"] = None; close_menu(); heartbeat(False); _hk_remove()
        with Kit.quiet: Kit.on_client(save_pos)
        Kit.save_min(MIN_KEY, st["minimized"]); save_settings(); save_cells(); g, win["g"] = win["g"], None
        Kit.dispose(g)
        for s in win.pop("stale", []): Kit.dispose(s)
    load_settings()
    return {"start": _start, "tick": _tick, "stop": _stop, "thread_wanted": lambda: bool(st["jobs"]),
              "client_tick": True, "thread_tick": _thread_tick, "config_height": cfg.height,
              "build_config": build_config, "poll_config": cfg.poll, "config_closed": cfg.closed}


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("actionbar", "Action Bar", "Cells for items, spells, skills and windows",
         _module_actionbar, 0.05, category="On screen")
