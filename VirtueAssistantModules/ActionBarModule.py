# =============================================================================
#  Action Bar  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by Virtue Assistant from LegionScripts/VirtueAssistantModules.
#  Virtue Assistant provides everything this file uses (API, G, safe, Client,
#  Kit, HOST, the main loop and the settings window), so run that instead and
#  tick Action Bar on its Modules tab.
#
#  To leave this module out, take this file out of the folder.
#  Module key: "actionbar"   (saved settings carry over unchanged)
#
#  Layout. The bar anchors to the screen's corners, edge midpoints and centre
#  (let it go near one); on the left or right edge it stands upright. Up to 4
#  extra rows of cells go above the top row (settings). GRID (under LOCK)
#  shows the host's screen grid, which every Virtue Assistant window snaps to.
#
#  Response time. Hotkeys are taken from the client's own key event and used
#  on the spot (DIRECT_KEYS); the bar, its menu and its settings page are
#  drawn in one hop on the client thread (BUILD_ON_CLIENT); binding a key,
#  locking, keybind mode and tooltips change the bar in place instead of
#  redrawing it; counters are written, never read back. Each of these falls
#  back to the plain script API when the client doesn't allow it.
# =============================================================================


def _module_actionbar():
    """Builds the module in its own namespace and returns its hooks."""
    # ============================ MODULE START ===================================
    #  MODULE: Action Bar  -  action cells with counters, window buttons, bag
    #  slots, 12 pages, keybind mode and a tray for the windows that fold in
    #
    #  Grimoire, Inventory > Bags and the Virtue Assistant window fold into this bar
    #  through shared vars (see the LINK constants); the other windows use the
    #  host's dock registry (HOST.docks).
    #
    #  A window folds in only when asked: its gold "Fold into the Action Bar"
    #  arrow, or this bar's button / tray icon for it while it is open. A
    #  window that is merely minimized keeps its own minimized form on screen
    #  and gets no tray icon.
    # =============================================================================
    KEY = "actionbar"
    TITLE = "Action Bar"

    # ------------------------------- CONFIG --------------------------------------
    TOP_SLOTS = 24                # top row (plain squares)
    BOTTOM_SLOTS = 12             # first half of the bottom row (one page of them)
    UI_SLOTS = 11                 # rectangle window buttons
    BAG_SLOTS = 5                 # bag slots at the right end
    ACTION_SLOTS = TOP_SLOTS + BOTTOM_SLOTS
    PAGES = 12                    # saved sets of the 12 bottom-left cells
    PAGE_W = 22                   # column left of them: page arrows and number

    SLOT_MIN, SLOT_MAX = 36, 64   # cell size range (icons stretch to fit)
    SCALE_MIN, SCALE_MAX = 50, 150   # whole-bar scale, percent
    SLOT_DEFAULT = 44
    SLOT_GAP = 4                  # stone between cells
    BAR_M = 8                     # stone round the bar
    SEC_GAP = 6                   # stone between the bottom-row panels
    CTRL_W = 44                   # column at the right: minimize, KEY (keybind mode), LOCK
    UI_SHARE = 0.65               # share of the bottom-right space for buttons (image: ~65%)
    UI_GAP = 4
    BAG_GAP = 3
    TRAY_BTN = 30                 # width of each icon in the tray (windows folded into the bar)
    TRAY_GAP = 4                  # stone between the bar and its tray window
    # (2.6.74) In a zone the bar fills its slot both ways (_stretch): the spare
    # length first widens the gaps (up to FIT_GAP_MAX x their size), then the cells
    # (up to FIT_CELL_MAX x as wide as deep, the icon square in the middle), then
    # the window buttons' and bag panels take the rest
    FIT_GAP_MAX = 2.0
    FIT_CELL_MAX = 1.6

    SLOT_TILE = 2624              # dark tile of a cell
    SLOT_ALPHA = 0.92
    SLOT_FRAME = 2620             # dark 9-piece frame: group panels (one frame off)
    UI_PANEL_ALPHA = 0.55         # stone inside the button panel (lighter grey)

    COUNT_EVERY = 0.75            # seconds between counter refreshes
    SCAN_EVERY = 2.0              # seconds between bag / ability re-checks
    TRAY_EVERY = 0.1              # seconds between looks at where the bar is (tray follows it)
    PAGE_EVERY = 0.2              # seconds between reads of the settings page's controls
    WATCH_EVERY = 0.25            # seconds between looks at the other windows' states (shared vars)
    SCREEN_EVERY = 2.0            # seconds between screen-size checks of an anchored bar
    SLIDER_SETTLE = 0.4           # seconds a settings slider rests before the bar is rebuilt
    RECOUNT_AFTER_USE = 0.4       # seconds after using an item before its counter is read again
    SCRIPT_CHECK_AFTER = 0.5      # seconds after a script cell is used before its state is checked
    SCRIPT_NAMES_LIFE = 60.0      # seconds a script cell's list of names to try is kept (folder walk)
    FALLBACK_REPEAT = 0.6         # (2.6.84) key events closer than this on the OnHotKey fallback: a held key
    HELD_KEY_STALE = 2.0          # seconds without a key event after which a "held" key is let go
    # Speed. Every script call that returns a value waits for the client's next
    # update pass (a round trip), so a window of ~400 controls built one call at
    # a time takes a second or more, and a key pressed while the bar's tick is
    # busy waits for it. These do the work where it is free:
    DIRECT_KEYS = True            # act on a hotkey inside the client's own key event
    #                               (no wait for the script's next pass or any slow tick)
    BUILD_ON_CLIENT = True        # draw windows in one hop on the client thread
    #                               (one round trip instead of one per control)
    TARGET_WAIT = 2.5             # seconds to wait for a target cursor after use
    #                               (a spell cell adds its cast time, Kit.spell_info)
    NO_CURSOR_KINDS = ("travel", "say", "ui", "dress", "undress", "ability")   # never raise one
    PICK_TIMEOUT = 15             # seconds to target an item / bag
    LOW_DEFAULT = 5               # counter turns red at this many or fewer
    # Cooldown sweep: after a skill cell is used every skill cell darkens and
    # counts down the skill delay (the server keeps one skill timer for all
    # skills); after a spell cell, every spell cell counts down that spell's
    # cast time (Kit.spell_info). Seconds per skill: the shard's values (In Mani
    # Ylem rules, section 6; anything not listed gets SKILL_DELAY_DEFAULT):
    SKILL_DELAY_DEFAULT = 10.0
    SKILL_DELAY = {"Arms Lore": 3.0, "Item Identification": 3.0, "Detect Hidden": 3.0}
    # Guard-zone warning (shard rule R6): a harmful cell aimed at the last target
    # while that target is blue (or green) and you are under the town guards
    # does nothing on the first press; a second press of the same cell within
    # CONFIRM_SECS goes through.
    HARMFUL_SPELLS = set(n.lower() for n in (
        "Clumsy", "Feeblemind", "Magic Arrow", "Weaken", "Harm", "Fireball", "Poison",
        "Curse", "Lightning", "Mana Drain", "Mind Blast", "Paralyze", "Dispel",
        "Energy Bolt", "Explosion", "Mass Curse", "Chain Lightning", "Flamestrike",
        "Mana Vampire", "Meteor Swarm", "Earthquake", "Mass Dispel", "Paralyze Field"))
    HARMFUL_ITEMS = set([0x0F0D])  # item graphics that harm their target (explosion potion)
    WARN_NOTO = (1, 2)            # notoriety that flags you when harmed: innocent (blue), ally (green)
    CONFIRM_SECS = 3.0            # seconds the confirming second press stays open
    CONFIRM_MIN = 0.3             # (2.6.84) a press this soon after is the same click (a double-click)
    COOL_EVERY = 0.1              # seconds between countdown redraws while one runs
    COOL_DARK = 0.55              # how dark a cooling cell gets (its click catcher's alpha)
    CATCHER_ALPHA = 0.01          # a click catcher's alpha otherwise (Kit.catcher)
    GREY_ICON = 0.35              # a spell cell's icon while a reagent it needs is at 0
    # Travel cells (Grimoire's runebook destinations): how each way is shown
    # and offered. The counter shows the book's charges, or the scrolls carried.
    TRAVEL_WAYS = [("recall", "Recall (spell)"), ("gate", "Gate Travel (spell)"),
                   ("charge", "Recall (a book charge)"), ("recall_scroll", "Recall scroll"),
                   ("gate_scroll", "Gate Travel scroll"), ("sacred", "Sacred Journey (spell)")]
    TRAVEL_VERB = {"recall": "Recall", "gate": "Gate", "charge": "Recall (charge)",
                   "recall_scroll": "Recall scroll", "gate_scroll": "Gate scroll",
                   "sacred": "Sacred Journey"}
    TRAVEL_SCROLL = {"recall_scroll": 0x1F4C, "gate_scroll": 0x1F60}
    TRAVEL_ITEM = {"charge": 0x22C5, "recall_scroll": 0x1F4C, "gate_scroll": 0x1F60}
    TRAVEL_SPELL = {"recall": "Recall", "gate": "Gate Travel", "sacred": "Sacred Journey"}
    TRAVEL_ICON = 0.5             # the way's icon under a Travel cell's rune name

    # Weapon ability icons (gump art): first ability after "None"
    ABILITY_ICON_BASE = 0x5200

    # Unified Bag (Virtue Assistant 1.8) saves its bags per character in
    # "_unified_bag_<serial>.cfg" next to Virtue Assistant, as "slot.N=<serial>"
    # lines. The bar reads that file (never writes it). Blank folder = the folder
    # this script runs from; set it if this script lives somewhere else.
    UB_CFG_NAME = "_unified_bag_%d.cfg"
    UB_CFG_DIR = ""
    UB_MODULE_KEY = "bag"         # Bags' key inside Virtue Assistant (its old module key)

    # Link to Inventory > Bags (shared vars; the var names keep the window's old
    # name): the bar sends "show" / "dock"; Bags reports "open", "collapsed",
    # "docked" (folded into this bar, title strip hidden) or "off". While the
    # bar's bag slots are on screen it keeps a heartbeat; without one Bags
    # brings its title strip back by itself.
    UB_LINK_CMD = "UnifiedBag_cmd"
    UB_LINK_STATE = "UnifiedBag_state"
    UB_LINK_ALIVE = "ActionBar_alive"
    # Grimoire (Virtue Assistant's spellbook / runebook module) - same kind of link:
    # states "open", "minimized", "docked" (folded into this bar, window hidden).
    GRIM_MODULE_KEY = "grimoire"
    GRIM_LINK_CMD = "Grimoire_cmd"
    GRIM_LINK_STATE = "Grimoire_state"
    # Asks Virtue Assistant to turn Grimoire / Bags on when they're off
    VA_LINK_ENABLE = "VirtueAssistant_enable"
    # The Virtue Assistant window itself - states "open", "gear" (minimized)
    # and "docked" (its gear hidden while this bar is open; the bar's Virtue
    # Assistant button stands in for it).
    VA_LINK_CMD = "VirtueAssistant_cmd"
    VA_LINK_STATE = "VirtueAssistant_state"
    VA_GEAR_ITEM = 0x1053          # the gear Virtue Assistant folds into
    ENABLE_WAIT = 4.0             # seconds before saying Virtue Assistant didn't answer

    # Hotkeys other Virtue Assistant modules own (Swing Bar, Map Pings, ...)
    # are read from HOST.hotkeys_owned, which each of them fills while it is
    # on. All modules share one script, so a bar cell on one of them would
    # steal it; when a module comes on and takes a key, the bar lets go of it.

    SETTINGS_KEY = "ActionBar_settings"   # per character
    CELLS_KEY = "ActionBar_cells"
    PAGES_KEY = "ActionBar_pages"         # the 12 pages of bottom-left cells
    EXTRA_KEY = "ActionBar_extra"         # the extra rows' cells (settings: Extra rows)
    EXTRA_ROWS = 4                        # most extra rows of TOP_SLOTS cells, above the top row
    EXTRA_SLOTS = EXTRA_ROWS * TOP_SLOTS
    # Screen anchors (the bar snaps to them when let go; see Snap in the host):
    # corners TL TR BL BR, edge midpoints T B L R, the centre C. On L or R the
    # bar stands upright (its rows become columns); on T or B it lies flat.
    ANCHORS_VERTICAL = ("L", "R")
    ANCHORS_HORIZONTAL = ("T", "B")
    SETTLE_AFTER = 0.3                    # seconds at rest after a drag before the anchor is read
    POS_KEY = "ActionBar_pos"
    MIN_KEY = "ActionBar_min"     # minimized when you left (kept for the next start)
    MINI_W, MINI_H = 240, 46

    # Window buttons: (id, caption, icon item graphic, how it opens).
    # "ga:Name" calls the client's GameActions.Name(world) - what TazUO's own top
    # bar and macros call; "ga:Name:Gump" brings an open Gump of that type forward
    # instead of opening another. Icons are item art scaled into the rectangle;
    # set one to 0 for a text caption.
    UI_ACTIONS = [
        ("paperdoll",   "Paperdoll",         0x1F03, "paperdoll"),
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
        ("help",        "Help",              0x0FEF, "help"),
        ("war",         "War / peace",       0x13FF, "war"),
        ("barsettings", "Bar settings",      0x0FBF, "barsettings"),
        ("virtue",      "Virtue Assistant",  VA_GEAR_ITEM, "virtue"),
        ("lock",        "Lock / unlock bar", 0x100F, "lock"),
        ("minimize",    "Minimize bar",      0,      "minimize"),
    ]
    # Spellbooks the Spellbook button looks for, in this order
    SPELLBOOKS = (0x0EFA, 0x2253, 0x2252, 0x238C, 0x23A0, 0x2D50, 0x2D9D)
    # What each window button's tooltip says (the caption alone would repeat itself)
    UI_TIPS = {"paperdoll": "Open the client's paperdoll", "status": "Open the client's status bar",
               "journal": "Open the client's journal", "skills": "Open the client's skills window",
               "worldmap": "Open TazUO's World Map", "minimap": "Open the client's mini map",
               "quests": "Open the quest log", "guild": "Open the guild window",
               "party": "Open the party window", "chat": "Open the chat window",
               "options": "Open the client's options", "help": "Open the help menu",
               "war": "Switch between war and peace mode",
               "barsettings": "Open the Action Bar settings page",
               "lock": "Lock the bar in place, or unlock it", "minimize": "Minimize the bar"}
    DEFAULT_UI = ["paperdoll", "status", "skills", "spellbook", "guild", "chat",
                  "minimap", "worldmap", "options", "barsettings", "virtue"]
    # What the buttons were before pages were added: a bar still holding exactly these is
    # moved to DEFAULT_UI (a bar you changed yourself is left alone)
    OLD_DEFAULT_UI = ["paperdoll", "status", "journal", "skills", "spellbook", "worldmap",
                      "minimap", "quests", "options", "barsettings", "virtue"]

    # Keybind mode: every key / modifier combination below is hooked as a
    # hotkey while it's on, so a tap is reported by the client itself. BIND_EVERY
    # and POLL_KEYS are the polling fallback if hotkeys can't be hooked.
    BIND_MODS = ("", "CTRL+", "SHIFT+", "ALT+", "CTRL+SHIFT+", "CTRL+ALT+", "SHIFT+ALT+")
    BIND_EVERY = 0.05
    POLL_KEYS = (["F%d" % i for i in range(1, 13)] + [chr(c) for c in range(65, 91)] +
                 [str(d) for d in range(10)] + ["NUMPAD%d" % d for d in range(10)] +
                 ["SPACE", "TAB", "HOME", "END", "INSERT", "DELETE", "PAGEUP", "PAGEDOWN",
                  "UP", "DOWN", "LEFT", "RIGHT", "ESCAPE", "BACKSPACE", "ENTER"])
    # XNA key names that aren't just upper-cased for a Legion hotkey
    XNA_NAMES = {"Back": "BACKSPACE", "OemMinus": "MINUS", "OemPlus": "PLUS",
                 "OemTilde": "TILDE", "OemComma": "COMMA", "OemPeriod": "PERIOD",
                 "OemQuestion": "SLASH", "OemSemicolon": "SEMICOLON", "OemQuotes": "QUOTE",
                 "OemOpenBrackets": "LEFTBRACKET", "OemCloseBrackets": "RIGHTBRACKET",
                 "OemPipe": "BACKSLASH", "Add": "NUMPADPLUS", "Subtract": "NUMPADMINUS",
                 "Multiply": "NUMPADMULTIPLY", "Divide": "NUMPADDIVIDE", "Decimal": "NUMPADPERIOD"}
    #  (2.6.75) the Keys / Lock / Grid buttons are always short text buttons (2.6.74
    #  drew item icons when a zone made the column too small): the column is made
    #  wide enough for their captions in the arrangement its height allows
    CTRL_CAPS = ("Keys", "Lock", "Grid")
    CTRL_ROW_MIN = 16             # px: the least height of a button (one line of text)
    CTRL_ROW_MAX = 24             # px: the most, in the compact arrangements
    CTRL_PAD = 2                  # px between the buttons and round them

    # Skills the Skill category lists (the usable ones), in TazUO's order
    SKILLS = ["Anatomy", "Animal Lore", "Animal Taming", "Arms Lore", "Begging",
              "Cartography", "Detect Hidden", "Discordance", "Evaluate Intelligence",
              "Forensic Evaluation", "Hiding", "Inscription", "Item Identification",
              "Meditation", "Peacemaking", "Poisoning", "Provocation", "Remove Trap",
              "Spirit Speak", "Stealing", "Stealth", "Taste Identification", "Tracking"]
    SCHOOL_NAMES = ["Magery", "Necromancy", "Chivalry", "Bushido", "Ninjitsu",
                    "Spellweaving", "Mysticism"]
    MENU_ROWS = 16                # list rows per column in the right-click menu
    MENU_COLS = 4                 # columns per page
    MENU_ROW_H = 20

    # Cell kinds, as in TazUO's action bar cells (plus Say and Window)
    TYPES = [("", "Empty"), ("item", "Item + counter"), ("spell", "Spell"),
             ("skill", "Skill"), ("macro", "TazUO macro"), ("ability", "Weapon ability"),
             ("script", "Legion script"), ("dress", "Dress outfit"),
             ("undress", "Undress outfit"), ("say", "Say text"), ("ui", "Client window"),
             ("travel", "Travel (runebook)")]
    # A Travel cell keeps its destination in keys of its own (the 2.6.04 bar
    # loads such a cell without them): "rb" the runebook's serial (hex), "ri"
    # the rune's index in Grimoire's list, "rm" the way to travel; "v" is the
    # rune's name, "n" the book's.
    TRAVEL_KEYS = ("rb", "ri", "rm")
    TARGETS = [("", "None"), ("self", "Self"), ("last", "Last target")]
    BAG_MODES = ["Bags' slots", "Bags I pick", "Backpack + sub-bags"]

    # Spell icons (gump art), in each school's spell order
    SPELL_SCHOOLS = (
        (0x08C0, "Clumsy|Create Food|Feeblemind|Heal|Magic Arrow|Night Sight|Reactive Armor|"
                 "Weaken|Agility|Cunning|Cure|Harm|Magic Trap|Magic Untrap|Protection|Strength|"
                 "Bless|Fireball|Magic Lock|Poison|Telekinesis|Teleport|Unlock|Wall of Stone|"
                 "Arch Cure|Arch Protection|Curse|Fire Field|Greater Heal|Lightning|Mana Drain|"
                 "Recall|Blade Spirits|Dispel Field|Incognito|Magic Reflection|Mind Blast|"
                 "Paralyze|Poison Field|Summon Creature|Dispel|Energy Bolt|Explosion|"
                 "Invisibility|Mark|Mass Curse|Paralyze Field|Reveal|Chain Lightning|"
                 "Energy Field|Flamestrike|Gate Travel|Mana Vampire|Mass Dispel|Meteor Swarm|"
                 "Polymorph|Earthquake|Energy Vortex|Resurrection|Air Elemental|Summon Daemon|"
                 "Earth Elemental|Fire Elemental|Water Elemental"),
        (0x5000, "Animate Dead|Blood Oath|Corpse Skin|Curse Weapon|Evil Omen|Horrific Beast|"
                 "Lich Form|Mind Rot|Pain Spike|Poison Strike|Strangle|Summon Familiar|"
                 "Vampiric Embrace|Vengeful Spirit|Wither|Wraith Form|Exorcism"),
        (0x5100, "Cleanse by Fire|Close Wounds|Consecrate Weapon|Dispel Evil|Divine Fury|"
                 "Enemy of One|Holy Light|Noble Sacrifice|Remove Curse|Sacred Journey"),
        (0x5420, "Honorable Execution|Confidence|Evasion|Counter Attack|Lightning Strike|"
                 "Momentum Strike"),
        (0x5320, "Focus Attack|Death Strike|Animal Form|Ki Attack|Surprise Attack|Backstab|"
                 "Shadowjump|Mirror Image"),
        (0x59D8, "Arcane Circle|Gift of Renewal|Immolating Weapon|Attune Weapon|Thunderstorm|"
                 "Nature's Fury|Summon Fey|Summon Fiend|Reaper Form|Wildfire|Essence of Wind|"
                 "Dryad Allure|Ethereal Voyage|Word of Death|Gift of Life|Arcane Empowerment"),
        (0x5DC0, "Nether Bolt|Healing Stone|Purge Magic|Enchant|Sleep|Eagle Strike|"
                 "Animated Weapon|Stone Form|Spell Trigger|Mass Sleep|Cleansing Winds|Bombard|"
                 "Spell Plague|Hail Storm|Nether Cyclone|Rising Colossus"),
    )

    HELP = [
        "Click a cell to use it; right-click it (Shift+click when right-clicks don't reach "
        "the bar) for a menu of what to put there: an item (target it; the cell counts how "
        "many you carry), a spell, skill, weapon ability, TazUO macro, Legion script, outfit, "
        "text to say, a window or a runebook destination, plus its hotkey and target.",
        "Click an empty cell to target an item for it straight away.",
        "The 12 cells at the bottom left have 12 pages: the tiny arrows and the number "
        "beside them switch pages, and each page keeps its own cells and hotkeys.",
        "Keys, at the far right, starts keybind mode: hover a cell, window button or bag slot "
        "and press a key or combination to bind it; Esc ends it and Backspace clears a key. "
        "Lock locks the bar in place (with windows in zones it turns Arrange mode on and off); "
        "Grid shows the screen grid every window snaps to.",
        "Drag the bar by its stone edge; let it go near a screen corner, the middle of an "
        "edge or the centre and it anchors there (on the left or right edge it stands upright).",
        "The bag slots show the bags of Inventory > Bags: click one to show the Bags window, "
        "click again to fold it into the bar, right-click one for its settings. With Bags I "
        "pick, click an empty slot to target a bag for it.",
        "The Grimoire and Virtue Assistant buttons show their window (turning Grimoire on "
        "when it is off); click again to fold that window into the bar.",
        "A Module windows button (page 2 of the Client window list) turns that module on and "
        "shows its window; click again to fold the window into the tray, the small window of "
        "icons beside the bar (Ultima Tracker always has one). The bar's numbered button "
        "folds the tray itself away and brings it back.",
        "A Travel (runebook) cell goes to one of your runebook destinations by Recall, Gate "
        "Travel, a book charge, a scroll or Sacred Journey, through Grimoire (it must be on); "
        "its counter shows the book's charges or the scrolls you carry.",
        "After a skill or spell cell is used, the cells of that kind darken and count down; "
        "a spell cell greys out while a reagent it needs is at 0. Red at sets when an item's "
        "counter turns red.",
    ]
    # -----------------------------------------------------------------------------

    settings = {"slot": SLOT_DEFAULT, "top": True, "keys": True, "lock": False,
                "short": True, "hue": False, "bagmode": 0, "bags": "", "page": 0,
                "scale": 100, "tray_open": True, "bagkeys": "",
                "extra": 0,                  # extra rows of cells above the top row (0-4)
                "anchor": "",                # screen anchor the bar sits on ("" = free)
                "vertical": False}           # upright (anchored to the left or right edge)
    # "a" action cells (top row, then the bottom-left cells of the current page),
    # "u" window buttons, "pages" the 12 saved bottom-left sets (page = settings["page"])
    cells = {"a": [], "u": [], "x": [], "pages": []}   # "x": the extra rows' cells
    st = {"shutting": False, "minimized": False, "queue": [], "hotkeys": [],
          "want_target": None, "next_count": 0.0, "next_scan": 0.0, "rebuild_at": 0.0,
          "confirm": None,           # ((ref, page), until): a harmful press awaiting its second
          "ub_pending": False,       # Bags' file not looked at yet since start: slots blank
          "cnt": {}, "cnt_g": {}, "first": {}, "first_g": {},
          "bags": [None] * BAG_SLOTS, "bag_sig": None, "ub_found": None,
          "ability_sig": None, "ub_cache": None, "ub_state": None, "grim_state": None,
          "va_state": None,
          "pending_on": None, "right_ok": None, "bind": None, "dock_sig": None,
          "watch_next": 0.0, "script_check": None,
          "jobs": [],                # work that waits / reads the disk: run by _thread_tick
          "redraw": set(),           # cells / bag slots to draw again in place (redraw_now)
          "ub_job": False, "ub_last": None,   # Unified Bag's file: a read is queued / last result
          "cool": {"skill": 0.0, "spell": 0.0},   # countdowns: when each kind's ends (0: none)
          "cool_next": 0.0}
    win = {"g": None, "store": ({}, {}), "cells": {}, "bags": {}}
    tray = {"g": None, "at": None}             # the tray window (folded windows' icons)
    menu = {"g": None, "ref": None, "level": "cats", "cat": None, "page": 0,
            "c": {}, "bag": None, "items": [],
            "anchor": None, "moved": None, "placed": None}
    page = {"c": None, "store": ({}, {}), "sel": ACTION_SLOTS - BOTTOM_SLOTS}
    SPELL_ICON = dict((n.lower(), base + i) for base, names in SPELL_SCHOOLS
                      for i, n in enumerate(names.split("|")))


    # ---------- small helpers ----------
    def later(fn):
        """fn() on the script's own thread, right after the bar's next tick
        (_thread_tick): for work that waits (HOST.idle, a server reply) or
        reads the disk. The tick itself runs on the client thread, where a
        wait would freeze the game."""
        st["jobs"].append(fn)


    def on_client_thread():
        return bool(safe(Client.on_client_thread, False))


    def spell_icon(name):
        n = (name or "").strip().lower()
        if not n:
            return 0
        icon = SPELL_ICON.get(n)
        if icon is None:                       # partial, like API.CastSpell
            icon = next((v for k, v in SPELL_ICON.items() if k.startswith(n)), None)
        return icon if icon and Kit.pic_size(icon)[0] > 0 else 0


    def ability_info(which):
        """(icon, name) of the current primary / secondary weapon ability."""
        names = [str(n) for n in (safe(lambda: list(API.CurrentAbilityNames()), []) or [])]
        i = 1 if which == "secondary" else 0
        if len(names) <= i:
            return 0, ""
        name = names[i]
        known = [str(n) for n in (safe(lambda: list(API.KnownAbilityNames()), []) or [])]
        if name not in known:
            return 0, name
        idx = known.index(name)
        if known and known[0].lower() in ("none", "invalid"):
            idx -= 1
        icon = ABILITY_ICON_BASE + idx
        return (icon if idx >= 0 and Kit.pic_size(icon)[0] > 0 else 0), name


    def ui_def(uid):
        if uid.startswith("mod:"):
            return mod_def(uid[4:])
        return next((d for d in UI_ACTIONS if d[0] == uid), None)


    def mod_def(key, docks=None):
        """Another Virtue Assistant module as a window button ("Module
        windows"): (uid, title, icon, how). The icon is the one its window
        folds into the tray with, once the module has registered it.
        `docks` (2.6.82): dict(HOST.docks) when the caller already made it."""
        s = HOST.by_key.get(key)
        if s is None or key == KEY:
            return None
        d = (docks if docks is not None else dict(HOST.docks)).get(key)
        icon = int(safe(lambda: d.get("icon"), 0) or 0) if d else 0
        return ("mod:" + key, s.title, icon, "mod:" + key)


    def mod_actions():
        """Every other module as a window button, in the Modules tab's order; a
        module made of parts (2.6.5) gives one button per part ("Character HUD:
        Pets"), under the part's own key (its 2.6.06 module key when it has
        one, so cells made before 2.6.5 still match)."""
        out = []
        docks = dict(HOST.docks)                 # 2.6.82: once, not per slot
        for slot in HOST.slots:
            parts = getattr(slot, "parts", ())
            if parts:
                for p in parts:
                    olds = p[4] if len(p) > 4 else ()
                    d = mod_def(olds[0] if olds else "%s.%s" % (slot.key, p[0]), docks)
                    if d is not None:
                        out.append(d)
                continue
            d = mod_def(slot.key, docks)
            if d is not None:
                out.append(d)
        return out


    def ui_all():
        """The client's windows, then the modules' windows."""
        return UI_ACTIONS + mod_actions()


    def mod_tip(key):
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
        """A module's window button: turns the module on, shows its window
        or folds it into the bar; a module without a foldable window is
        simply turned on or off."""
        s = HOST.by_key.get(key)
        if s is None:
            API.SysMsg("Action Bar: no module '%s'." % key, Kit.HUE_BAD)
            return False
        d = dict(HOST.docks).get(key)
        if not s.running:
            HOST.dock_forget(key)                # it should come up on screen

            def turn(k=key, title=s.title):      # may compile its file: the script's thread
                HOST.enable(k)
                if not HOST.by_key[k].running:
                    API.SysMsg("Action Bar: %s couldn't be turned on." % title, Kit.HUE_BAD)
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


    MOD_NAMES = {"ALT": ["ALT", "LALT", "RALT", "LEFTALT", "RIGHTALT", "MENU"],
                 "SHIFT": ["SHIFT", "LSHIFT", "RSHIFT", "LEFTSHIFT", "RIGHTSHIFT"],
                 "CTRL": ["CTRL", "LCTRL", "RCTRL", "LEFTCTRL", "RIGHTCTRL", "CONTROL"]}


    _keyboard = [None]      # ClassicUO.Input.Keyboard (False: not there)


    def key_down(name):
        """Alt / Shift / Ctrl held? API.IsKeyPressed wants a combination ("CTRL+F1"),
        so ask the client first, as Ultima Tracker does."""
        v = Client.key_held(name.lower()) if name != "CTRL" else None
        if v is not None:
            return bool(v)
        kb = _keyboard[0]                       # 2.6.82: the Keyboard type looked up once
        if kb is None:
            try:
                from ClassicUO.Input import Keyboard
                kb = Keyboard
            except Exception:
                kb = False
            _keyboard[0] = kb
        if kb is not False:
            try:
                return bool(getattr(kb, {"ALT": "Alt", "SHIFT": "Shift", "CTRL": "Ctrl"}[name]))
            except Exception:
                pass
        for k in MOD_NAMES.get(name, [name]):
            if safe(lambda k=k: API.IsKeyPressed(k), False):
                return True
        return False


    def norm_key(k):
        return str(k or "").strip().upper().replace(" ", "")


    MOD_BASES = set(n for names in MOD_NAMES.values() for n in names)   # a modifier on its own


    def key_owner(k):
        """Which module holds this hotkey right now (None = free): what Swing
        Timer, Map Pings and the like register with the host while they are on."""
        owned = getattr(HOST, "hotkeys_owned", None)
        return owned.get(k) if owned else None


    def owned_keys():
        """The hotkeys other modules hold, as a set (empty when none)."""
        owned = getattr(HOST, "hotkeys_owned", None)
        return frozenset(owned) if owned else frozenset()


    def bar_keys():
        """Every hotkey on a filled cell or a bag slot, normalised."""
        ks = set(norm_key(c["k"]) for _, c in all_cells() if c["k"] and c["t"])
        ks.update(k for k in bag_keys() if k)
        return ks


    _input = {"looked": False, "mouse": None, "keys": None}


    def _find_input():
        """The client's mouse position and keyboard state, by reflection (the
        script API has neither). Mouse: ClassicUO.Input.Mouse.Position. Keys:
        the XNA/FNA Keyboard.GetState() the client itself reads."""
        if _input["looked"]:
            return
        _input["looked"] = True
        mt = Client._type("ClassicUO.Input.Mouse")
        if mt is not None:
            try:
                m = Client._member(mt, "Position")
                p = m[0]()
                int(p.X), int(p.Y)
                _input["mouse"] = m[0]
            except Exception:
                _input["mouse"] = None
        kt = Client._type("Microsoft.Xna.Framework.Input.Keyboard")
        if kt is not None:
            try:
                import System
                from System.Reflection import BindingFlags
                gs = kt.GetMethod("GetState", BindingFlags.Static | BindingFlags.Public, None,
                                  System.Type.EmptyTypes, None)

                def read():
                    return [str(k) for k in gs.Invoke(None, None).GetPressedKeys()]
                read()
                _input["keys"] = read
            except Exception:
                _input["keys"] = None


    def mouse_pos():
        """(x, y) of the mouse on screen, or None if the client won't say."""
        _find_input()
        fn = _input["mouse"]
        if fn is None:
            return None
        p = safe(fn)
        try:
            return int(p.X), int(p.Y)
        except Exception:
            return None


    def xna_key_name(n):
        """An XNA key name as a Legion hotkey name: D5 -> 5, NumPad3 -> NUMPAD3, F5 -> F5."""
        if len(n) == 2 and n[0] == "D" and n[1].isdigit():
            return n[1]
        if n.startswith("NumPad"):
            return "NUMPAD" + n[6:]
        return XNA_NAMES.get(n, n.upper())


    def keys_now():
        """(ctrl, shift, alt, [other keys held]) right now."""
        _find_input()
        fn = _input["keys"]
        names = safe(fn) if fn is not None else None
        if names is None:                      # poll the likely keys instead
            main = []                          # 2.6.82: plain loop, no lambda per key
            for k in POLL_KEYS:
                try:
                    if API.IsKeyPressed(k):
                        main.append(k)
                except Exception:
                    pass
            return key_down("CTRL"), key_down("SHIFT"), key_down("ALT"), main
        ctrl = shift = alt = False
        main = []
        for n in names:
            if n in ("LeftControl", "RightControl"):
                ctrl = True
            elif n in ("LeftShift", "RightShift"):
                shift = True
            elif n in ("LeftAlt", "RightAlt"):
                alt = True
            elif n not in ("None", "LeftWindows", "RightWindows", "CapsLock", "NumLock"):
                main.append(xna_key_name(n))
        return ctrl, shift, alt, main


    def fit(text, width):
        """text cut to fit width (pixels): the mother's Kit.fit (letter widths,
        no label made per letter), with this module's one-dot tail."""
        return Kit.fit(str(text), width, ".")


    def short_key(k):
        return (k.upper().replace("CTRL+", "C").replace("SHIFT+", "S")
                .replace("ALT+", "A").replace("NUMPAD", "N").replace("KP_", "N"))


    def fmt_count(n):
        if settings["short"]:
            if n >= 10000:
                return "%dk" % (n // 1000)
            if n >= 1000:
                return "%.1fk" % (n / 1000.0)
        return str(n)


    def parse_graphic(text):
        """'0x0E21' or '0x0E21,1153' -> (graphic, hue), or None."""
        t = (text or "").strip()
        if not t:
            return None
        a, b = [s.strip() for s in (t.split(",", 1) + [""])[:2]]
        try:
            return (int(a, 16) if a.lower().startswith("0x") else int(a),
                    (int(b, 16) if b.lower().startswith("0x") else int(b)) if b else 0)
        except Exception:
            return None


    # ---------- cells ----------
    def blank():
        return {"t": "", "v": "", "g": 0, "h": 0, "tg": "", "k": "", "lo": LOW_DEFAULT, "n": ""}


    def cell(ref):
        return cells[ref[0]][ref[1]]


    def bag_keys():
        """Hotkey of each bag slot ("" = none)."""
        ks = [norm_key(k) for k in settings["bagkeys"].split(",")]
        return (ks + [""] * BAG_SLOTS)[:BAG_SLOTS]


    def set_key_of(ref, k):
        """Put hotkey k on a cell, a window button or a bag slot, and save."""
        if ref[0] == "b":
            ks = bag_keys()
            ks[ref[1]] = k
            settings["bagkeys"] = ",".join(ks)
            save_settings()
        else:
            cell(ref)["k"] = k
            save_cells()


    def ref_name(ref):
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


    SEL_TOTAL = ACTION_SLOTS + UI_SLOTS + EXTRA_SLOTS   # entries of the Cell drop-down


    def sel_ref(idx):
        if idx < ACTION_SLOTS:
            return ("a", idx)
        if idx < ACTION_SLOTS + UI_SLOTS:
            return ("u", idx - ACTION_SLOTS)
        return ("x", idx - ACTION_SLOTS - UI_SLOTS)


    def ref_sel(ref):
        if ref[0] == "a":
            return ref[1]
        if ref[0] == "u":
            return ACTION_SLOTS + ref[1]
        return ACTION_SLOTS + UI_SLOTS + ref[1]


    def sel_names():
        return (["Top %d" % (i + 1) for i in range(TOP_SLOTS)] +
                ["Bottom %d" % (i + 1) for i in range(BOTTOM_SLOTS)] +
                ["Button %d" % (i + 1) for i in range(UI_SLOTS)] +
                ["Row %d-%d" % (i // TOP_SLOTS + 2, i % TOP_SLOTS + 1) for i in range(EXTRA_SLOTS)])


    def shown(ref):
        """Is this cell on the bar right now? (hidden rows' hotkeys stay quiet)"""
        kind, i = ref
        if kind == "x":
            return i < settings["extra"] * TOP_SLOTS
        if kind == "a":
            return settings["top"] or i >= TOP_SLOTS
        return True


    def all_cells():
        """Every action cell and window button, with its ref: [(ref, cell)]."""
        return ([(("a", i), c) for i, c in enumerate(cells["a"])] +
                [(("u", i), c) for i, c in enumerate(cells["u"])] +
                [(("x", i), c) for i, c in enumerate(cells["x"])])


    def default_cells():
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
        """What a Travel cell does, in words."""
        return "%s to %s%s" % (TRAVEL_VERB.get(c.get("rm"), "Travel"), c["v"] or "?",
                               (" (%s)" % c["n"]) if c["n"] else "")


    def describe(ref):
        c = cell(ref)
        t = c["t"]
        if not t:
            if ref[0] in ("a", "x"):
                return "Empty: click, then target an item for it. Right-click for a spell, skill or more."
            return "Empty: right-click to choose what this button does"
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
            name = {"open": "Fold Virtue Assistant into the bar",
                    "gear": "Open the Virtue Assistant window",
                    "docked": "Open the Virtue Assistant window"
                    }.get(st["va_state"], "Virtue Assistant (not running)")
        elif t == "ui" and c["v"].startswith("mod:"):
            name = mod_tip(c["v"][4:])
        elif t == "ui":
            name = UI_TIPS.get(c["v"], name)
        tip = {"item": "Use %s", "spell": "Cast %s", "skill": "Use %s", "macro": "Run macro %s",
               "ability": "Use the %s ability", "script": "Start or stop script %s",
               "dress": "Dress %s", "undress": "Undress %s", "say": "Say \"%s\"",
               "ui": "%s"}.get(t, "%s") % name
        if c["tg"]:
            tip += ", then target %s" % ("yourself" if c["tg"] == "self" else "last target")
        if c["k"]:
            tip += "  [%s]" % c["k"]
        if t == "spell":
            miss = missing_reg(c["v"])
            if miss is not None:
                tip += "\nOut of %s" % miss[1]
        return tip + "\nRight-click to change"


    # ---------- saved settings ----------
    def _esc(s):
        return (str(s).replace("%", "%25").replace("&", "%26").replace("=", "%3D")
                .replace(";", "%3B").replace("|", "%7C"))


    def _unesc(s):
        return (s.replace("%7C", "|").replace("%3B", ";").replace("%3D", "=")
                .replace("%26", "&").replace("%25", "%"))


    def _enc(d):
        return "&".join("%s=%s" % (k, _esc(v)) for k, v in d.items())


    def _dec(s):
        d = {}
        for part in s.split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                d[k] = _unesc(v)
        return d


    def load_settings():
        d = _dec(Kit.get_var(SETTINGS_KEY))
        for k in ("top", "keys", "lock", "short", "hue", "tray_open", "vertical"):
            if k in d:
                settings[k] = d[k] == "1"
        for k, lo, hi in (("slot", SLOT_MIN, SLOT_MAX), ("bagmode", 0, len(BAG_MODES) - 1),
                          ("page", 0, PAGES - 1), ("scale", SCALE_MIN, SCALE_MAX),
                          ("extra", 0, EXTRA_ROWS)):
            try:
                settings[k] = int(d[k])
            except Exception:
                pass
            settings[k] = max(lo, min(hi, settings[k]))
        a = d.get("anchor", "")
        settings["anchor"] = a if a in ("TL", "T", "TR", "L", "C", "R", "BL", "B", "BR") else ""
        for k in ("bags", "bagkeys"):
            settings[k] = d.get(k, settings[k])


    def save_settings():
        Kit.put_var(SETTINGS_KEY, _enc(dict(
            (k, ("1" if v else "0") if isinstance(v, bool) else v) for k, v in settings.items())))


    def _norm(d):
        c = blank()
        for k in ("t", "v", "tg", "k", "n"):
            c[k] = d.get(k, c[k])
        for k in ("g", "h", "lo"):
            try:
                c[k] = int(d.get(k, c[k]))
            except Exception:
                pass
        if c["t"] == "travel":                   # a Travel cell's destination (only its own)
            for k in TRAVEL_KEYS:
                c[k] = d.get(k, "")
        return c


    def _cells_of(raw, n, skip_empty=True):
        """n cells from saved text (padded with blanks)."""
        lst = [_norm(_dec(s)) for s in raw.split(";") if s or not skip_empty]
        return (lst + [blank() for _ in range(n)])[:n]


    def load_cells():
        _saved_cells.clear()                    # 2.6.82: the first save writes every var
        a, u = default_cells()
        raw = Kit.get_var(CELLS_KEY)
        if "|" in raw:
            ra, ru = raw.split("|", 1)
            a = _cells_of(ra, ACTION_SLOTS, False)
            u = _cells_of(ru, UI_SLOTS, False)
            used = set(c["v"] for c in u if c["t"] == "ui")
            spare = [d for d in DEFAULT_UI if d not in used]
            for c in u:
                # an unknown stock button is replaced by a spare one; a module
                # button whose file is missing today is kept (it draws its key
                # as text and says so when clicked) so it is back when the file is
                if c["t"] == "ui" and ui_def(c["v"]) is None and not c["v"].startswith("mod:"):
                    c.update(blank())
                    if spare:
                        c.update({"t": "ui", "v": spare.pop(0)})
            # the old stock buttons, never changed: move to the new stock set
            if [c["v"] if c["t"] == "ui" else None for c in u] == OLD_DEFAULT_UI[:UI_SLOTS]:
                for i, uid in enumerate(DEFAULT_UI[:UI_SLOTS]):
                    u[i].update({"t": "ui", "v": uid})
        # the 12 pages of bottom-left cells; the bar shows settings["page"]
        pages = [[blank() for _ in range(BOTTOM_SLOTS)] for _ in range(PAGES)]
        rawp = Kit.get_var(PAGES_KEY)
        if rawp:
            for pi, ps in enumerate(rawp.split("|")[:PAGES]):
                pages[pi] = _cells_of(ps, BOTTOM_SLOTS)
        else:                                   # first run with pages: page 1 = the old cells
            pages[0] = a[TOP_SLOTS:]
            settings["page"] = 0
        a[TOP_SLOTS:] = pages[settings["page"]]
        cells["x"] = _cells_of(Kit.get_var(EXTRA_KEY), EXTRA_SLOTS)
        cells["a"], cells["u"], cells["pages"] = a, u, pages
        cells_touched()


    def sync_page():
        """The bar's bottom-left cells are the current page's cells."""
        if cells["pages"]:
            cells["pages"][settings["page"]] = list(cells["a"][TOP_SLOTS:])


    _saved_cells = {}       # 2.6.82: var -> the text last written this session


    def save_cells():
        sync_page()
        cells_touched()

        def enc(lst):
            return ";".join(_enc(c) for c in lst)
        # 2.6.82: speed pass: a var is written only when its text changed
        for key, text in ((CELLS_KEY, enc(cells["a"]) + "|" + enc(cells["u"])),
                          (PAGES_KEY, "|".join(enc(pg) for pg in cells["pages"])),
                          (EXTRA_KEY, enc(cells["x"]))):
            if _saved_cells.get(key) != text:
                Kit.put_var(key, text)
                _saved_cells[key] = text


    def set_page(p):
        """Show page p (wraps round) of the bottom-left cells."""
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
        want_redraw([("a", TOP_SLOTS + i) for i in range(BOTTOM_SLOTS)])   # only that page's cells
        refresh_page_column()
        HOST.refresh_settings(KEY)
        # 2.6.81: a menu opened on a bottom-left cell belongs to the page it was
        # opened on; it closes so it can't change the new page's cell
        r = menu.get("ref")
        if menu.get("g") is not None and r and r[0] == "a" and r[1] >= TOP_SLOTS:
            close_menu()


    def picked_bags():
        out = [0] * BAG_SLOTS
        for i, p in enumerate(settings["bags"].split(",")[:BAG_SLOTS]):
            try:
                out[i] = int(p, 16) if p.strip() else 0
            except Exception:
                out[i] = 0
        return out


    def set_picked_bag(i, serial):
        lst = picked_bags()
        lst[i] = serial
        settings["bags"] = ",".join(("%X" % s) if s else "" for s in lst)
        save_settings()


    def save_pos():
        """Save where the bar is, but only when it moved (a save is a disk write)."""
        g = win["g"]
        if not Kit.is_open(g):
            return
        try:                                     # 2.6.82: plain try, no lambdas
            x = int(g.GetX())
        except Exception:
            x = 0
        try:
            y = int(g.GetY())
        except Exception:
            y = 0
        p = (x, y)
        if p != st.get("pos_saved"):
            st["pos_saved"] = p
            Kit.put_var(POS_KEY, "%d,%d" % p)


    # ---------- client windows and macros (client reflection) ----------
    class ClientUI(object):
        """Opens client windows the way TazUO's own top bar does - by calling the
        client's GameActions (OpenJournal, OpenSkills, OpenSettings...) with the
        World that the API object holds - and runs TazUO macros by name. Scripts
        have no API for these, so this uses .NET reflection, and every call runs
        on the client thread through the host's own hop (Client.on_main_ex).
        Each property / method is looked up once per type and kept (_acc,
        _methods): a hotkey on a macro or window cell is one Invoke, not a
        scan of the type's methods."""
        looked = False
        error = ""
        world = None
        GA = None                 # ClassicUO.Game.GameActions (internal static class)
        UIM = None                # ClassicUO.Game.Managers.UIManager
        MTQ = None                # found: the client thread can be reached
        _acc = {}                 # (type, name, static) -> (PropertyInfo / FieldInfo, is property) or None
        _methods = {}             # (type, name, parameter types, static) -> MethodInfo or None

        @staticmethod
        def _flags(static):
            from System.Reflection import BindingFlags
            return (BindingFlags.Public | BindingFlags.NonPublic |
                    (BindingFlags.Static if static else BindingFlags.Instance))

        @staticmethod
        def _get(obj, name, t=None):
            static = obj is None
            t = t if t is not None else obj.GetType()
            key = (t, name, static)
            acc = ClientUI._acc.get(key, False)
            if acc is False:
                acc = None
                flags = ClientUI._flags(static)
                tt = t
                while tt is not None:
                    try:
                        p = tt.GetProperty(name, flags)
                    except Exception:
                        p = None
                    if p is not None:
                        acc = (p, True)
                        break
                    f = tt.GetField(name, flags)
                    if f is not None:
                        acc = (f, False)
                        break
                    tt = tt.BaseType
                ClientUI._acc[key] = acc
            if acc is None:
                return None
            return acc[0].GetValue(obj, None) if acc[1] else acc[0].GetValue(obj)

        @staticmethod
        def _method(t, name, ptypes, static):
            """Method `name` whose parameters start with the given type names
            (None = any type), and whose other parameters are optional."""
            key = (t, name, tuple(ptypes), static)
            if key not in ClientUI._methods:
                ClientUI._methods[key] = ClientUI._find_method(t, name, ptypes, static)
            return ClientUI._methods[key]

        @staticmethod
        def _find_method(t, name, ptypes, static):
            for m in t.GetMethods(ClientUI._flags(static)):
                if m.Name != name or m.IsGenericMethodDefinition:
                    continue
                ps = m.GetParameters()
                if len(ps) < len(ptypes):
                    continue
                if any(want is not None and ps[i].ParameterType.Name != want
                       for i, want in enumerate(ptypes)):
                    continue
                if all(p.IsOptional for p in ps[len(ptypes):]):
                    return m
            return None

        @staticmethod
        def _invoke(m, target, args):
            import System
            ps = m.GetParameters()
            full = list(args) + [p.DefaultValue for p in ps[len(args):]]
            return m.Invoke(target, System.Array[object](full))

        @staticmethod
        def _type(asm, name):
            t = safe(lambda: asm.GetType(name)) if asm is not None else None
            return t if t is not None else Client._type(name)

        @staticmethod
        def find():
            if ClientUI.looked:
                return
            ClientUI.looked = True
            asm = None
            try:
                import clr
                asm = API.GetType().Assembly
                clr.AddReference(asm)
                from ClassicUO.Game.Managers import MainThreadQueue
                ClientUI.MTQ = MainThreadQueue
            except Exception as ex:
                ClientUI.error = "no client thread (%s)" % ex
                return
            # The API object (LegionAPI) keeps the client's World in a field
            world = safe(lambda: ClientUI._get(API, "World"))
            if world is None:                      # else Client.Game.UO.World
                ct = ClientUI._type(asm, "ClassicUO.Client")
                game = safe(lambda: ClientUI._get(None, "Game", ct)) if ct is not None else None
                uo = safe(lambda: ClientUI._get(game, "UO")) if game is not None else None
                world = safe(lambda: ClientUI._get(uo, "World")) if uo is not None else None
            ClientUI.world = world
            ClientUI.GA = ClientUI._type(asm, "ClassicUO.Game.GameActions")
            ClientUI.UIM = ClientUI._type(asm, "ClassicUO.Game.Managers.UIManager")
            if world is None:
                ClientUI.error = "client World not found"
            elif ClientUI.GA is None:
                ClientUI.error = "GameActions not found"

        @staticmethod
        def on_main(fn):
            """fn() on the client thread (in place when already there, as in a
            key event or a client tick): the host's Client.on_main_ex. Returns
            fn's result; on failure returns None and leaves the reason in
            ClientUI.error."""
            if ClientUI.MTQ is None:
                return None
            how, value = Client.on_main_ex(fn)
            if how == "ok":
                return value
            if how == "err":
                ex = Client.exc
                inner = getattr(ex, "InnerException", None) or \
                    getattr(getattr(ex, "clsException", None), "InnerException", None)
                ClientUI.error = str(inner) if inner else Client.error
            else:
                ClientUI.error = Client.error or "can't run on the client thread"
            return None

        @staticmethod
        def _bring_to_front(type_name):
            """An open gump of this type brought on top; False if none is open."""
            gumps = ClientUI._get(None, "Gumps", ClientUI.UIM) if ClientUI.UIM is not None else None
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
            """GameActions.<name>(world, *extra) on the client thread, as the top
            bar calls it. `reuse`: gump type to bring forward instead, if open."""
            ClientUI.find()
            if ClientUI.world is None or ClientUI.GA is None:
                return False
            world = ClientUI.world

            def run():
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
            """The client's built-in 'Open <sub>' macro (used for the party window)."""
            ClientUI.find()
            world = ClientUI.world
            if world is None:
                return False

            def run():
                import System
                mgr = ClientUI._get(world, "Macros")
                mo_t, mt_t, ms_t = [mgr.GetType().Assembly.GetType("ClassicUO.Game.Managers." + n)
                                    for n in ("MacroObject", "MacroType", "MacroSubType")]
                mo = System.Activator.CreateInstance(mo_t, System.Array[object](
                    [System.Enum.Parse(mt_t, "Open", True), System.Enum.Parse(ms_t, sub, True)]))
                ClientUI._run_macro_object(mgr, mo)
                return True
            return bool(ClientUI.on_main(run))

        @staticmethod
        def macro_names():
            """Names of the player's TazUO macros, in the client's order."""
            ClientUI.find()
            world = ClientUI.world
            if world is None:
                return []

            def run():
                mgr = ClientUI._get(world, "Macros")
                out = []
                m = ClientUI._method(mgr.GetType(), "GetAllMacros", [], False)
                if m is not None:
                    for mc in (m.Invoke(mgr, None) or []):
                        out.append(str(ClientUI._get(mc, "Name") or ""))
                else:                                  # walk the linked list
                    node = ClientUI._get(mgr, "Items")
                    while node is not None:
                        out.append(str(ClientUI._get(node, "Name") or ""))
                        node = ClientUI._get(node, "Next")
                return [n for n in out if n]
            return list(ClientUI.on_main(run) or [])

        @staticmethod
        def _names_of(v):
            """Names found in a list of things with a Name (or Key)."""
            out = []
            if v is None or isinstance(v, str):
                return out
            try:
                for e in v:
                    n = e if isinstance(e, str) else (
                        safe(lambda: ClientUI._get(e, "Name")) or safe(lambda: ClientUI._get(e, "Key")))
                    if n:
                        out.append(str(n))
            except Exception:
                return []
            return out

        @staticmethod
        def _type_like(part):
            import System
            for asm in System.AppDomain.CurrentDomain.GetAssemblies():
                try:
                    types = asm.GetTypes()
                except Exception:
                    continue
                for tt in types:
                    if part in tt.Name and "Manager" in tt.Name:
                        return tt
            return None

        @staticmethod
        def outfit_names():
            """Names of the dress agent's saved outfits: the API's own list if
            it has one, else the client's DressAgentManager (best effort)."""
            for attr in ("DressConfigNames", "GetDressConfigNames", "DressConfigs",
                         "GetDressConfigs", "ListDressConfigs", "DressNames"):
                fn = getattr(API, attr, None)
                if fn is None:
                    continue
                names = ClientUI._names_of(safe(fn) if callable(fn) else fn)
                if names:
                    return names
            ClientUI.find()
            t = Client._type("ClassicUO.Game.Managers.DressAgentManager") or \
                safe(lambda: ClientUI._type_like("DressAgent"))
            if t is None:
                return []
            inst = safe(lambda: ClientUI._get(None, "Instance", t))
            for obj, tt in ((inst, safe(lambda: inst.GetType())), (None, t)):
                if tt is None:
                    continue
                flags = ClientUI._flags(obj is None)
                members = list(safe(lambda: tt.GetProperties(flags), []) or []) + \
                    list(safe(lambda: tt.GetFields(flags), []) or [])
                for m in members:
                    try:
                        v = m.GetValue(obj, None) if hasattr(m, "GetGetMethod") else m.GetValue(obj)
                    except Exception:
                        continue
                    names = ClientUI._names_of(v)
                    if names:
                        return names
            return []

        @staticmethod
        def _run_macro_object(mgr, mo):
            t = mgr.GetType()
            ClientUI._invoke(ClientUI._method(t, "SetMacroToExecute", ["MacroObject"], False), mgr, [mo])
            ClientUI._invoke(ClientUI._method(t, "Update", [], False), mgr, [])

        @staticmethod
        def run_macro(name):
            """Run one of the player's TazUO macros by name. None = no such macro."""
            ClientUI.find()
            world = ClientUI.world
            if world is None:
                return False

            def run():
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


    def on_client(fn, fallback=True):
        """fn() in ONE hop on the client thread (the host's Kit.on_client):
        every script call inside runs in place instead of each waiting a
        client update pass. Without BUILD_ON_CLIENT, fn runs here (if
        `fallback`, else None)."""
        if BUILD_ON_CLIENT:
            return Kit.on_client(fn, fallback)
        return fn() if fallback else None


    # ---------- Inventory > Bags' slots (its file) ----------
    def ub_cfg_paths():
        # 2.6.82: speed pass: worked out once per start (the character and the
        # script folder don't change while it runs), once the character is known
        hit = st.get("ub_paths")
        if hit is not None:
            return list(hit)
        serial = int(safe(lambda: API.Player.Serial, 0) or 0)
        name = UB_CFG_NAME % serial
        if UB_CFG_DIR:
            out = [UB_CFG_DIR.rstrip("/\\") + "/" + name]
        else:
            base = str(safe(lambda: API.ScriptPath, "") or "").rstrip("/\\")
            if not base:
                return [name]
            parent = base.replace("\\", "/").rsplit("/", 1)[0]
            out = [base + "/" + name, parent + "/" + name]    # same folder, then one up
        if serial:
            st["ub_paths"] = out
        return list(out)


    def unified_bags(paths=None):
        """Bags' bags in slot order, or None when its file isn't found.
        Re-read only when the file changes. Disk work: see ub_bags."""
        for path in (paths if paths is not None else ub_cfg_paths()):
            mtime = safe(lambda path=path: os.path.getmtime(path))
            if mtime is None:
                continue
            cache = st["ub_cache"]
            if cache and cache[0] == path and cache[1] == mtime:
                return list(cache[2])
            slots, assign = 0, {}
            try:
                with open(path, "r") as f:
                    lines = f.read().splitlines()
            except Exception:
                continue
            for line in lines:
                if "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip()
                try:
                    if k == "slots":
                        slots = int(v)
                    elif k.startswith("slot."):
                        assign[int(k[5:])] = int(v)
                except Exception:
                    pass
            lst = [assign[i] for i in sorted(assign) if (slots <= 0 or i < slots) and assign[i] > 0]
            st["ub_cache"] = (path, mtime, lst)
            return list(lst)
        return None


    def ub_bags():
        """unified_bags() for scan_bags. On the client thread the file is looked
        at on the script's own thread (a disk read there would be a frame
        hitch) and the last reading is used; a change found there rescans the
        bag slots at once."""
        if not on_client_thread():
            st["ub_last"], st["ub_pending"] = unified_bags(), False
            return None if st["ub_last"] is None else list(st["ub_last"])
        if not st["ub_job"]:
            st["ub_job"] = True
            paths = ub_cfg_paths()            # read here: free on the client thread

            def job():
                st["ub_job"] = False
                res = unified_bags(paths)
                if res != st["ub_last"] or st["ub_pending"]:
                    st["ub_last"], st["ub_pending"] = res, False
                    st["next_scan"] = 0.0     # the slots follow on the next tick
            later(job)
        return None if st["ub_last"] is None else list(st["ub_last"])


    def link_state(var, allowed):
        try:                                     # 2.6.82: plain try (every WATCH_EVERY)
            s = API.GetSharedVar(var)
        except Exception:
            s = None
        return str(s) if s is not None and str(s) in allowed else None


    def ub_state():
        """'open', 'collapsed', 'docked', or None when Bags isn't running."""
        return link_state(UB_LINK_STATE, ("open", "collapsed", "docked"))


    def grim_state():
        """'open', 'minimized', 'docked', or None when Grimoire isn't running."""
        return link_state(GRIM_LINK_STATE, ("open", "minimized", "docked"))


    def va_state():
        """'open', 'gear', 'docked', or None when Virtue Assistant isn't running."""
        return link_state(VA_LINK_STATE, ("open", "gear", "docked"))


    def ub_send(cmd):
        safe(lambda: API.SetSharedVar(UB_LINK_CMD, cmd))


    def all_docks():
        """Every window that can fold into the bar, from the host: [(key, hooks)]."""
        return list(HOST.docks)


    def tray_docks():
        """The tray's buttons: windows folded into the bar, plus the ones that
        always have a button (Ultima Tracker). A window that is only
        minimized shows its own minimized form instead."""
        return [(k, d) for k, d in all_docks()
                if d.get("always") or safe(d.get("state")) == "docked"]


    def dock_sig():
        return tuple((k, safe(d.get("state"))) for k, d in all_docks())


    def tray_sig():
        """What the tray is drawn from: the folded / always-there windows, their
        icons, and the state of the always-there ones (their hue and tooltip).
        A window merely minimizing or restoring doesn't change it."""
        return tuple((k, d.get("icon"), safe(d.get("state")) if d.get("always") else None)
                     for k, d in tray_docks())


    def heartbeat(on=True):
        """While the bar is on screen, Grimoire, Bags and the Virtue
        Assistant gear may fold into it: the ones the player folded in (the
        gold arrow) come back into it by themselves once they see the
        heartbeat. Merely minimized windows are never folded in."""
        if on and not st["minimized"]:
            safe(lambda: API.SetSharedVar(UB_LINK_ALIVE, time.time()))
        else:
            safe(lambda: API.RemoveSharedVar(UB_LINK_ALIVE))


    def watch_ub():
        """Other windows' states (shared variables, the dock registry) and the
        hotkeys other modules hold, every WATCH_EVERY seconds."""
        now = time.time()
        if now < st["watch_next"]:
            return
        st["watch_next"] = now + WATCH_EVERY
        tips = False
        for k, s, tip in (("ub_state", ub_state(), settings["bagmode"] == 0),
                          ("grim_state", grim_state(), True), ("va_state", va_state(), True)):
            if s != st[k]:
                st[k] = s
                tips = tips or tip
        if tips:
            refresh_tips()                        # in place: no rebuild
        sig = dock_sig()
        if sig != st["dock_sig"]:              # the module buttons follow their windows
            old_keys = set(k for k, _ in (st["dock_sig"] or ()))
            st["dock_sig"] = sig
            tsig = tray_sig()
            if tsig != st.get("tray_sig"):     # the tray only when its buttons change
                st["tray_sig"] = tsig
                refresh_tray()
            refs = [ref for ref, c in cells_with("ui") if c["v"].startswith("mod:")]
            if refs:
                if set(k for k, _ in sig) != old_keys:     # a window came or went: its icon
                    want_redraw(refs)
                else:                                      # its state: the tooltip
                    refresh_tips()
        owned = owned_keys()                   # a module came on / went off with hotkeys
        if owned != st.get("owned_sig"):
            changed = owned ^ (st.get("owned_sig") or frozenset())
            st["owned_sig"] = owned
            if changed & bar_keys():           # one of the bar's keys: let go of / take back
                register_hotkeys()
        p = st["pending_on"]
        if p and time.time() > p[2]:
            st["pending_on"] = None
            state = ub_state() if p[0] == UB_MODULE_KEY else grim_state()
            if state is None:
                API.SysMsg("Action Bar: %s didn't start; is Virtue Assistant running?" % p[1],
                           Kit.HUE_BAD)
                if p[3] is not None:
                    p[3]()


    def turn_on(key, title, fallback=None):
        """Turn a Virtue Assistant module on: directly when merged, else by asking
        Virtue Assistant. fallback() runs if nothing answers."""
        if key in HOST.by_key:
            # turning a module on may load its file (disk): on the script's thread
            later(lambda: HOST.enable(key))
        else:
            safe(lambda: API.SetSharedVar(VA_LINK_ENABLE, key))
        API.SysMsg("Action Bar: turning %s on." % title, Kit.HUE_INFO)
        st["pending_on"] = (key, title, time.time() + ENABLE_WAIT, fallback)


    def toggle_grimoire():
        """Show Grimoire, fold it into the bar, or turn it on."""
        state = grim_state()
        heartbeat()
        if state in ("minimized", "docked"):
            safe(lambda: API.SetSharedVar(GRIM_LINK_CMD, "show"))
        elif state == "open":
            safe(lambda: API.SetSharedVar(GRIM_LINK_CMD, "dock"))
        else:
            turn_on(GRIM_MODULE_KEY, "Grimoire", open_spellbook)
        return True


    def toggle_va():
        """Open the Virtue Assistant window, or fold it into the bar."""
        state = va_state()
        heartbeat()
        if state == "open":
            safe(lambda: API.SetSharedVar(VA_LINK_CMD, "dock"))
        elif state in ("gear", "docked"):
            safe(lambda: API.SetSharedVar(VA_LINK_CMD, "show"))
        else:
            API.SysMsg("Action Bar: Virtue Assistant isn't running.", Kit.HUE_BAD)
            return False
        return True


    def auto_bags():
        out = []
        bp = int(safe(lambda: API.Backpack, 0) or 0)
        if bp:
            out.append(bp)
        for it in (safe(lambda: list(API.ItemsInContainer(bp, False)), []) or []):
            if len(out) >= BAG_SLOTS:
                break
            try:                                  # 2.6.82: plain try, no lambda per item
                if it.IsContainer:
                    out.append(int(it.Serial))
            except Exception:
                pass
        return out


    def scan_bags():
        mode = settings["bagmode"]
        if mode == 0:
            serials = ub_bags()
            if serials is None and st["ub_pending"]:
                serials = []                  # 2.6.81: Bags' file not looked at yet: blank
            else:
                st["ub_found"] = serials is not None
                if serials is None:
                    serials = auto_bags()
        elif mode == 1:
            serials = picked_bags()
        else:
            serials = auto_bags()
        # 2.6.82: speed pass: plain try, no lambdas; a bag's name (a string read)
        # only when the slots changed (it was only ever kept then)
        bags, found = [], []
        for s in (list(serials) + [0] * BAG_SLOTS)[:BAG_SLOTS]:
            if not s:
                bags.append(None)
                found.append(None)
                continue
            try:
                it = API.FindItem(s)
            except Exception:
                it = None
            found.append(it)
            if it is None:
                bags.append({"s": s, "g": 0, "h": 0, "n": "Bag (not loaded yet)"})
                continue
            try:
                gr = int(it.Graphic or 0)
            except Exception:
                gr = 0
            try:
                hu = int(it.Hue or 0)
            except Exception:
                hu = 0
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
            want_redraw([("b", i) for i in range(BAG_SLOTS)])   # only the bag slots


    def bag_at(i):
        return st["bags"][i] if i < len(st["bags"]) else None


    _kinds = {"types": None, "items": None,   # what the cells hold (see cells_touched)
              "regs": None,                    # reagent graphics the spell cells need
              "extra": None,                   # other graphics to count (Travel cells' scrolls)
              "refs": None}                    # kind -> [refs] of the skill / spell cells


    def cells_touched():
        """The cells changed (saved, a page switched, loaded): what they hold
        is worked out again on the next look."""
        _kinds["types"] = _kinds["items"] = _kinds["regs"] = _kinds["extra"] = None
        _kinds["refs"] = None


    def spell_regs(name):
        """The reagent graphics a spell needs (Kit's Magery table), or ()."""
        info = safe(lambda: Kit.spell_info(name)) if hasattr(Kit, "spell_info") else None
        if not info:
            return ()
        regs = getattr(Kit, "REAGENTS", {})
        return tuple(regs[a][1] for a in info[1] if a in regs)


    def _cell_kinds():
        if _kinds["types"] is None:
            every = cells["a"] + cells["u"] + cells["x"]
            _kinds["types"] = set(c["t"] for c in every)
            _kinds["items"] = set(c["g"] for c in every if c["t"] == "item")
            regs, extra = set(), set()
            refs = {"skill": [], "spell": []}
            for ref, c in all_cells():
                if c["t"] == "spell":
                    regs.update(spell_regs(c["v"]))
                    refs["spell"].append(ref)
                elif c["t"] == "skill":
                    refs["skill"].append(ref)
                elif c["t"] == "travel" and c.get("rm") in TRAVEL_SCROLL:
                    extra.add(TRAVEL_SCROLL[c["rm"]])
            _kinds["regs"], _kinds["extra"] = frozenset(regs), frozenset(regs | extra)
            _kinds["refs"] = refs
        return _kinds


    def has_type(t):
        """Does any cell hold this kind? (asked every count and scan)"""
        return t in _cell_kinds()["types"]


    def scan_abilities():
        if not has_type("ability"):
            return
        sig = tuple(safe(lambda: [str(n) for n in API.CurrentAbilityNames()], []) or [])
        if sig != st["ability_sig"]:
            st["ability_sig"] = sig
            # a weapon swap: only the ability cells change their icon
            want_redraw([r for r, c in all_cells() if c["t"] == "ability"])


    # ---------- counters ----------
    def pack_list(max_age=0.0):
        """Every item in the pack, sub-bags included, or None when it can't be
        read. 2.6.82: speed pass: the host's shared list (HOST.pack_items: one
        listing per pass for every module; `max_age` lets a slow look reuse
        one up to that old), the old private listing on an older mother."""
        try:
            if _pack_fn[0] is not None:
                return _pack_fn[0](deep=True, max_age=max_age)
            return list(API.ItemsInContainer(API.Backpack, True))
        except Exception:
            return None


    _pack_fn = [getattr(HOST, "pack_items", None)]


    def count_now(extra=(), max_age=0.0):
        """Count the pack for the item cells' graphics (plus `extra`): only
        those items' hue, serial and amount are read."""
        items = pack_list(max_age)
        if items is None:
            return
        k = _cell_kinds()
        wanted = k["items"]
        if extra or k["extra"]:                 # + the spell cells' reagents, Travel scrolls
            wanted = wanted | k["extra"] | set(extra)
        cnt, cnt_g, first, first_g = {}, {}, {}, {}
        cget, gget, fset, fgset = cnt.get, cnt_g.get, first.setdefault, first_g.setdefault
        for it in items:
            try:
                gr = int(it.Graphic)
                if gr not in wanted:
                    continue
                hu, ser = int(it.Hue), int(it.Serial)
                amt = max(1, int(it.Amount or 0))
            except Exception:
                continue
            key = (gr, hu)
            cnt[key] = cget(key, 0) + amt
            cnt_g[gr] = gget(gr, 0) + amt
            fset(key, ser)
            fgset(gr, ser)
        st.update({"cnt": cnt, "cnt_g": cnt_g, "first": first, "first_g": first_g,
                   "counted": wanted,           # what was looked for (missing_reg)
                   "counted_at": time.time()})


    def count_if_stale():
        """2.6.82: speed pass: the pack is counted only while the bar shows its
        counters; a press or a restore counts first when the last count is
        older than COUNT_EVERY (minimized: no count at all until then)."""
        if time.time() - st.get("counted_at", 0.0) > COUNT_EVERY:
            k = _cell_kinds()
            if "item" in k["types"] or k["extra"]:
                count_now()


    def count_of(c):
        if settings["hue"]:
            return st["cnt"].get((c["g"], c["h"]), 0)
        return st["cnt_g"].get(c["g"], 0)


    def _place(info, lbl, text, hue):
        """Set a counter label's text and hue. What the label shows is kept
        here (info["txt"], info["hue"]) so nothing is read back from the
        client: a read waits for the client, a write doesn't."""
        if info.get("txt") != text:             # every COUNT_EVERY for every counter: no lambdas
            info["txt"] = text
            try:
                lbl.Text = text
                Kit.ui_pos(lbl, info["x"] + info["w"] - Kit.text_px(text) - 3,
                           info["y"] + info["h"] - 16)
            except Exception:
                pass
        if info.get("hue") != hue:
            info["hue"] = hue
            try:
                lbl.Hue = hue
            except Exception:
                pass


    def refresh_counts():
        """Recount the pack (item cells only) and redraw every counter, in one
        hop on the client thread (the spell / ability / bag reads run there)."""
        def work():
            if st["minimized"]:                  # 2.6.82: no counters on screen: no count
                return                           # (a press counts itself: use_item)
            k = _cell_kinds()
            if "item" in k["types"] or k["extra"]:
                count_now(max_age=0.5)           # (+ the spell cells' reagents, the scrolls)
            update_labels()
        on_client(work)


    _counters = [None]      # 2.6.82: [(ref, info, label)] of the cells with a counter


    def update_labels():
        now = time.time()
        cool = st["cool"]
        charges = False                            # Travel cells' book charges, read once
        lst = _counters[0]
        if lst is None:                            # 2.6.82: only the cells with a counter
            lst = [(ref, info, info["count"]) for ref, info in win["cells"].items()
                   if info.get("count") is not None]
            _counters[0] = lst
        for ref, info, lbl in lst:
            c = cell(ref)
            t, v = c["t"], c["v"]
            text, hue = "", Kit.HUE_TEXT
            end = cool.get(t)
            if end and now < end:                  # counting down (see cool_tick)
                text, hue = cool_text(end - now), Kit.HUE_TITLE
            elif t == "item":
                n = count_of(c)
                text = fmt_count(n)
                hue = Kit.HUE_BAD if n == 0 or n <= max(0, c["lo"]) else Kit.HUE_TEXT
            elif t in ("spell", "ability", "script"):
                try:                                   # every COUNT_EVERY: no lambdas
                    if t == "spell":
                        on = bool(API.IsSpellActive(v))
                    elif t == "ability":
                        on = bool(API.SecondaryAbilityActive() if v == "secondary"
                                  else API.PrimaryAbilityActive())
                    else:
                        on = script_running(v)
                except Exception:
                    on = False
                text, hue = ("ON" if on else ""), Kit.HUE_GOOD
            elif t == "travel":
                if charges is False:
                    charges = travel_charges()
                text, hue = travel_count(c, charges)
            if t == "spell":                       # a reagent at 0: greyed, the counter names it
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


    # ---------- spell cells' reagents (greyed at 0) ----------
    _regs = {}              # spell name -> ((abbreviation, graphic, name), ...) from Kit's table


    def spell_reg_list(name):
        hit = _regs.get(name)
        if hit is None:
            info = safe(lambda: Kit.spell_info(name)) if hasattr(Kit, "spell_info") else None
            table = getattr(Kit, "REAGENTS", {})
            hit = tuple((a, table[a][1], table[a][0]) for a in (info[1] if info else ())
                        if a in table)
            if len(_regs) > 200:
                _regs.clear()
            _regs[name] = hit
        return hit


    def missing_reg(name):
        """(abbreviation, reagent name) of the first reagent the spell needs that
        the last count found none of, or None (from count_now's counts)."""
        cnt, counted = st["cnt_g"], st.get("counted") or ()
        for a, g, n in spell_reg_list(name):
            if cnt.get(g, 0) <= 0 and g in counted:    # (not counted yet: not known missing)
                return (a, n)
        return None


    def grey_cell(ref, info, grey):
        """A spell cell's icon greyed / back, and its tooltip, when that changes."""
        if info.get("grey", False) == grey:
            return
        info["grey"] = grey
        icon = info.get("icon")
        if icon is not None:
            try:
                icon.SetAlpha(GREY_ICON if grey else 1.0)
            except Exception:
                pass
        set_tip(info, describe(ref))


    # ---------- Travel cells (Grimoire's runebook destinations) ----------
    TRAVEL_LOW = 2          # a new Travel cell's "Red at" (book charges / scrolls)


    def travel_charges():
        """Each carried runebook's charges ({serial: charges or None}) from
        Grimoire's saved lists, or None while Grimoire is off. 2.6.82: Grimoire's
        own dict, made again only when a list changed (the destinations list
        copied and turned into a dict every count, on an older Grimoire)."""
        fn = HOST.services.get("grimoire.book_charges")
        if fn is not None:
            try:
                return fn()
            except Exception:
                return None
        fn = HOST.services.get("grimoire.destinations")
        if fn is None:
            return None
        out = {}
        try:
            for d in fn() or ():
                out[d["book"]] = d["charges"]
        except Exception:
            return None
        return out


    def travel_count(c, charges):
        """(text, hue) of a Travel cell's counter: the scrolls carried for a
        scroll, else the book's charges (red at the cell's Red at for a charge,
        grey for a spell); "off" while Grimoire is off."""
        if charges is None:
            return "off", Kit.HUE_INFO
        m = c.get("rm")
        lo = max(0, c["lo"])
        if m in TRAVEL_SCROLL:
            n = st["cnt_g"].get(TRAVEL_SCROLL[m], 0)
            return fmt_count(n), Kit.HUE_BAD if n == 0 or n <= lo else Kit.HUE_TEXT
        try:
            n = charges.get(int(c.get("rb") or "0", 16))
        except ValueError:
            n = None
        if n is None:
            return "", Kit.HUE_TEXT
        if m == "charge":
            return str(n), Kit.HUE_BAD if n == 0 or n <= lo else Kit.HUE_TEXT
        return str(n), Kit.HUE_INFO


    def fire_travel(c):
        """A Travel cell used: one trip, made by Grimoire (its service only
        queues it, and says in the journal why when it can't)."""
        fn = HOST.services.get("grimoire.travel")
        if fn is None:
            API.SysMsg("Action Bar: Grimoire is off; turn it on to use Travel cells.", Kit.HUE_BAD)
            return False
        try:
            book, idx = int(c.get("rb") or "", 16), int(c.get("ri") or "")
        except ValueError:
            API.SysMsg("Action Bar: this Travel cell has no destination; right-click it to "
                       "pick one.", Kit.HUE_BAD)
            return False
        return bool(fn(book, idx, c.get("rm") or "recall", c["v"] or None))


    def set_travel(ref, d, method):
        """Put a Grimoire destination d (a grimoire.destinations entry) and a way
        to travel on the cell, keeping its hotkey."""
        cur = cell(ref)
        new = blank()
        new.update({"t": "travel", "v": str(d["name"]), "n": str(d["book_name"]),
                    "k": cur["k"], "tg": "", "lo": cur["lo"] if cur["t"] == "travel" else TRAVEL_LOW,
                    "rb": "%X" % int(d["book"]), "ri": str(int(d["index"])), "rm": method})
        cells[ref[0]][ref[1]] = new
        cells_changed(recount=True, refs=[ref])
        API.SysMsg("Action Bar: %s set on %s." % (travel_what(new), ref_name(ref)), Kit.HUE_GOOD)


    # ---------- cooldown sweep (skill delay, spell cast) ----------
    _skill_delay = dict((k.lower(), v) for k, v in SKILL_DELAY.items())


    def cool_text(rem):
        return ("%d" % int(math.ceil(rem))) if rem >= 3.0 else ("%.1f" % max(0.0, rem))


    def start_cool(t, v):
        """A skill / spell cell was used: every cell of that kind counts down
        (the skill delay, or this spell's cast time)."""
        if t == "skill":
            secs = _skill_delay.get(str(v).strip().lower(), SKILL_DELAY_DEFAULT)
        else:
            info = safe(lambda: Kit.spell_info(v)) if hasattr(Kit, "spell_info") else None
            secs = info[3] if info else 0.0
        if secs and secs > 0:
            st["cool"][t] = time.time() + secs
            st["cool_next"] = 0.0


    def cool_tick(now):
        """While a countdown runs, every COOL_EVERY: the cells of its kind are
        darkened (their click catcher, made more opaque) and their counter
        shows the seconds left; at the end they are lit again and the counters
        show what they did before. Only existing controls change."""
        cool = st["cool"]
        if not (cool["skill"] or cool["spell"]) or now < st["cool_next"]:
            return
        st["cool_next"] = now + COOL_EVERY
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
                    try:
                        info["catcher"].SetAlpha(COOL_DARK if dark else CATCHER_ALPHA)
                    except Exception:
                        pass
                lbl = info.get("count")
                if lbl is not None and not done:
                    _place(info, lbl, text, Kit.HUE_TITLE)
        if ended:
            update_labels()                     # the counters' own texts come back


    # ---------- the Hotkeys page (Settings > Hotkeys) ----------
    def short_what(ref):
        c = cell(ref)
        if c["t"] == "travel":
            return travel_what(c)
        tip = describe(ref).split("\n")[0]
        return tip.replace("  [%s]" % c["k"], "") if c["k"] else tip


    def hotkeys_service():
        """HOST.services["actionbar.hotkeys"]: [(combo, what it does)] for every
        key the bar listens to (filled cells on rows that show, bag slots); a
        key another module holds is listed as left to it."""
        out = []
        for r, c in all_cells():
            k = norm_key(c["k"])
            if not k or not c["t"] or not shown(r):
                continue
            what = "%s: %s" % (ref_name(r), short_what(r))
            owner = key_owner(k)
            out.append((k, what + ((" (left to %s)" % owner) if owner else "")))
        for i, k in enumerate(bag_keys()):
            if k:
                owner = key_owner(k)
                out.append((k, "bag slot %d" % (i + 1) + ((" (left to %s)" % owner) if owner
                                                          else "")))
        return out


    # ---------- the bar ----------
    queue = Kit.queuer(st)
    on_disposed = Kit.disposer(KEY, st, win)


    def want_rebuild(delay=0.0):
        st["rebuild_at"] = time.time() + delay


    def cells_changed(recount=False, refresh=True, refs=None):
        """A cell changed: save, re-hook the hotkeys, redraw the changed cells
        (refs; None = the whole bar) and the settings page."""
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
        cells[ref[0]][ref[1]] = blank()
        cells_changed(refs=[ref])


    # ---------- the zone fit (2.6.55) ----------
    #  Slotted in a zone of the layout, the bar is told the zone's size
    #  (layout_fit, through HOST.layout_add's hooks) and fits it: upright when
    #  the zone is taller than wide, flat otherwise, and scaled so its length
    #  fills the zone's long side. The fit is an override held here, never
    #  written to the player's Scale % or orientation: freed, the bar is as
    #  the player set it. The layout tells it again after every start.
    #  (2.6.74) It then fills the zone both ways: the spare length (or depth)
    #  is shared out over its gaps, cells and right-hand panels (_stretch).
    fitst = {"scale": None, "vertical": None,
             "slot": None,      # (2.6.57) the slot (w, h) the bar is drawn exactly, or None
             "off": (0, 0),     # (2.6.57) where the bar's cells start inside that slot
             "m": None,         # (2.6.74) the margin round the panels in the slot (None: its own)
             "sig": None}       # (2.6.74) the settings the fit's scale was worked out for


    def eff_scale():
        """The scale in use: the zone fit's, else the player's Scale %."""
        v = fitst["scale"]
        return int(settings["scale"]) if v is None else v


    def eff_vertical():
        """Upright in use: the zone fit's, else the player's orientation."""
        v = fitst["vertical"]
        return bool(settings["vertical"]) if v is None else v


    def told_slot():
        """(2.6.74) The (w, h) the layout told the bar, which it is drawn exactly
        (stretched to it, _stretch), or None: free, or not told since the start."""
        return fitst["slot"] if fitst["scale"] is not None else None


    def fit_margin(unified=None):
        """(2.6.74) The margin round the bar's panels in a zone: with one frame on
        Kit.MARGIN (the layout makes the window that much bigger than the panels'
        rect, Layout._grow, so the panels sit Kit.ZONE_INSET in from the zone like
        every window's), else None (the bar's own, scaled)."""
        if unified is None:
            unified = bool(safe(lambda: HOST.layout_unified(KEY), False))
        return int(getattr(Kit, "MARGIN", 12)) if unified else None


    def fit_sig(mz):
        """(2.6.74) What the zone fit's scale depends on besides the slot."""
        return (settings["slot"], settings["top"], settings["extra"], mz)


    def _fit_scale(along, across, mz):
        """(2.6.74) The biggest Scale % at which the bar's own geometry (margin mz)
        fits along x across px; the bar is then stretched over the rest (_stretch).
        Worked out from the bar at 100%, then stepped (every size on the bar is
        rounded on its own, sc) to the biggest that fits."""
        keep = fitst["scale"]
        try:
            fitst["scale"] = 100
            G1 = _geom_base(mz)
            fx = 2 * mz if mz is not None else 0     # a margin that doesn't scale with the bar
            pct = int(min((along - fx) * 100.0 / max(1.0, G1["W"] - fx),
                          (across - fx) * 100.0 / max(1.0, G1["H"] - fx)))
            pct = max(SCALE_MIN, min(SCALE_MAX, pct))

            def fits(p):
                fitst["scale"] = p
                G2 = _geom_base(mz)
                return G2["W"] <= along and G2["H"] <= across
            n = 0
            while n < 8 and pct > SCALE_MIN and not fits(pct):
                pct -= 1
                n += 1
            n = 0
            while n < 8 and pct < SCALE_MAX and fits(pct + 1):
                pct += 1
                n += 1
            return pct
        finally:
            fitst["scale"] = keep


    def tell_need(mz):
        """(2.6.85) Extra rows: the zone is asked for the room they take at the size the
        bar has without them, so the rows don't shrink the whole bar (the layout grows
        the zone; the game view gives way first). No extra rows: nothing asked."""
        fn = getattr(HOST, "layout_need", None)
        base = safe(lambda: HOST.layout_base(KEY))
        if fn is None:
            return
        if not settings["extra"] or base is None:
            safe(lambda: fn(KEY))
            return
        vert = base[1] > base[0]
        along, across = (base[1], base[0]) if vert else base
        keep, kept_scale, vt = settings["extra"], fitst["scale"], _ctrl.get("vtmp")
        _ctrl["vtmp"] = vert
        try:
            settings["extra"] = 0
            p = _fit_scale(int(along), int(across), mz)
            settings["extra"] = keep
            fitst["scale"] = p
            need = _geom_base(mz)["H"]
        finally:
            settings["extra"] = keep
            fitst["scale"] = kept_scale
            _ctrl["vtmp"] = vt
        safe(lambda: fn(KEY, need if vert else None, None if vert else need))


    def layout_fit(w, h, mode):
        """The layout: the bar's slot in a zone is w x h px, or it is freed
        (None). Upright in a slot taller than wide; (2.6.74) scaled as big as fits
        the slot both ways, then stretched to fill it exactly both ways (_stretch:
        the 2.6.57 bar was centred in a frame the slot's size, which left a short
        wide zone's ends empty). Client thread, in the keeper's pass: record and
        queue the rebuild."""
        if w is None or h is None or not w or not h:
            new = (None, None)
            slot = mz = sig = None
        else:
            slot = (int(w), int(h))
            vert = h > w
            along, across = (h, w) if vert else (w, h)
            mz = fit_margin()
            sig = fit_sig(mz)
            tell_need(mz)
            _ctrl["vtmp"] = vert                 # (2.6.75) the column's sums for this orientation
            try:
                new = (_fit_scale(int(along), int(across), mz), vert)
            finally:
                _ctrl["vtmp"] = None
        was = (eff_scale(), eff_vertical(), fitst["slot"], fitst["m"])
        fitst["scale"], fitst["vertical"] = new
        fitst["slot"], fitst["m"], fitst["sig"] = slot, mz, sig
        now = (eff_scale(), eff_vertical(), fitst["slot"], fitst["m"])
        if now != was and not st["shutting"]:
            want_rebuild()
            if HOST.debug:
                API.SysMsg("Action Bar: %s." % (
                    "fitted to a zone %d x %d (%s, %d%%)" % (w, h, "upright" if now[1] else "flat", now[0])
                    if new[0] is not None else "freed from its zone"), Kit.HUE_INFO)


    def refit_if_stale(unified):
        """(2.6.74) Before a build in a zone: the fit's scale again when one frame
        was turned on or off, or Cell size / Top row / Extra rows changed, since
        the slot was told (the layout tells the bar only a new slot size, and
        the old scale overfilled or underfilled it)."""
        slot = told_slot()
        if slot is None:
            return
        mz = fit_margin(unified)
        sig = fit_sig(mz)
        if sig == fitst["sig"]:
            return
        along, across = (slot[1], slot[0]) if fitst["vertical"] else slot
        fitst["scale"] = _fit_scale(along, across, mz)
        fitst["m"], fitst["sig"] = mz, sig
        tell_need(mz)                            # (2.6.85) rows added or taken away


    def layout_state():
        if win["g"] is None or st["shutting"]:
            return None
        return "minimized" if st["minimized"] else "open"


    # (2.6.57) the bar is drawn exactly its slot's size: the whole bar (both rows,
    # the bag and tray sections, the KEY / LOCK / GRID column) scaled as one, as
    # big as fits, (2.6.74) then stretched to the slot both ways (_stretch).
    # (2.6.74) "untitled": the bar has no title row by design (Layout.look_problems)
    LAYOUT_HOOKS = {"fit": layout_fit, "state": layout_state, "exact": True, "untitled": True}


    def sc(v, lo=1):
        """v scaled by the bar's Scale % setting (or the zone fit's)."""
        k = max(SCALE_MIN, min(SCALE_MAX, eff_scale())) / 100.0
        return max(lo, int(round(v * k)))


    _geom = {"key": None, "L": None}


    def geom():
        """Every size on the bar, scaled by Scale % (cells by Cell size too).
        Worked out once per size setting (the tray follows the bar ten times
        a second and asks for the bar's size each time); never changed by
        its callers."""
        # (2.6.74) and per slot told by the layout (the stretch fills it)
        key = (settings["slot"], eff_scale(), settings["top"], settings["extra"],
               told_slot(), fitst["m"], eff_vertical())
        if _geom["key"] != key:
            _geom["L"] = _geom_now()
            _geom["key"] = key
        return _geom["L"]


    def _geom_now():
        """(2.6.74) The geometry in use: the bar's own (_geom_base), and in a slot
        told by the layout stretched to fill it both ways (_stretch)."""
        slot = told_slot()
        if slot is None:
            return _geom_base()
        along, across = (slot[1], slot[0]) if eff_vertical() else slot
        return _stretch(_geom_base(fitst["m"]), along, across)


    _ctrl = {"capw": None, "vtmp": None}


    def ctrl_vertical():
        """(2.6.75) Upright for the control column's sums: the orientation being
        fitted (layout_fit works the scale out before it records it), else the
        one in use."""
        v = _ctrl["vtmp"]
        return eff_vertical() if v is None else v


    def ctrl_capw():
        """(2.6.75) The width a Keys / Lock / Grid button needs for its caption
        (draw_small_button's own test: the caption plus 4 px), measured once."""
        if _ctrl["capw"] is None:
            _ctrl["capw"] = max(Kit.text_w(c) for c in CTRL_CAPS) + 6
        return _ctrl["capw"]


    def ctrl_orders(vert):
        """(2.6.75) Columns of the control grid to try, best first: stacked on a
        flat bar (its column is tall), one row on an upright bar (it is wide)."""
        return (4, 2, 1) if vert else (1, 2, 4)


    def ctrl_cells(c, dw, dh):
        """(2.6.75) (rows, cell w, cell h) of the minimize arrow and the three
        buttons in c columns inside dw x dh (drawn px)."""
        rows = (4 + c - 1) // c
        cell_w = (dw - 2 * CTRL_PAD - (c - 1) * CTRL_PAD) // c
        cell_h = min(CTRL_ROW_MAX, (dh - 2 * CTRL_PAD - (rows - 1) * CTRL_PAD) // rows)
        return rows, cell_w, cell_h


    def ctrl_need(col_h, vert):
        """(2.6.75) The least width (flat sums) of the control column so the three
        buttons show their captions, for a column col_h long: the fewest columns
        whose rows fit its height on a flat bar, the most whose width fits on an
        upright one (the column lies across the bar's foot there)."""
        capw = ctrl_capw()
        for c in ctrl_orders(vert):
            rows = (4 + c - 1) // c
            across = rows * CTRL_ROW_MIN + (rows - 1) * CTRL_PAD + 2 * CTRL_PAD
            along = c * capw + (c - 1) * CTRL_PAD + 2 * CTRL_PAD
            if vert and along <= col_h:
                return across
            if not vert and across <= col_h:
                return along
        # nothing fits that way: the arrangement that needs only the column's width
        return (4 * CTRL_ROW_MIN + 5 * CTRL_PAD) if vert else (4 * capw + 5 * CTRL_PAD)


    def _geom_base(m=None):
        """The bar's own geometry, worked out flat (R turns it upright). m: the
        margin round the panels (2.6.74: the zone fit's), else the bar's own."""
        S = sc(max(SLOT_MIN, min(SLOT_MAX, int(settings["slot"]))), 18)
        bm, sg, p4 = sc(BAR_M, 4), sc(SEC_GAP, 3), sc(4, 2)
        m = bm if m is None else m
        gap, ug, bg = sc(SLOT_GAP, 2), sc(UI_GAP, 2), sc(BAG_GAP, 2)
        pw, cw, tb = sc(PAGE_W, 16), sc(CTRL_W, 34), sc(TRAY_BTN, 18)
        pitch = S + gap
        ph = S + 2 * p4                             # height of a row
        # (2.6.72) the top rows are indented by the page column's width, as the bottom
        # row is, so the rows line up cell for cell (the bottom row sat shifted right)
        inner = pw + TOP_SLOTS * pitch + p4         # width of the cell area
        left_w = BOTTOM_SLOTS * pitch + p4
        tray_w = tb + 2 * p4                        # one fixed button: the tray
        rest = inner - pw - left_w - 2 * sg - tray_w - sg
        ui_w = int(rest * UI_SHARE)
        bag_w = rest - ui_w
        bw = (ui_w - 2 * p4 - (UI_SLOTS - 1) * ug) // UI_SLOTS
        bgw = (bag_w - 2 * p4 - (BAG_SLOTS - 1) * bg) // BAG_SLOTS
        rows = (2 if settings["top"] else 1) + settings["extra"]
        # (2.6.75) wide enough for the Keys / Lock / Grid captions (ctrl_need)
        cw = max(cw, ctrl_need(rows * ph + (rows - 1) * sg, ctrl_vertical()))
        return {"S": S, "pitch": pitch, "ph": ph, "inner": inner, "left_w": left_w,
                "rows": rows,
                "ui_w": ui_w, "bag_w": bag_w, "bw": bw, "bh": ph - 3 * p4,
                "tray_w": tray_w, "tb": tb,
                "bgw": bgw, "bgh": ph - 2 * p4,
                "m": m, "sg": sg, "p4": p4, "ug": ug, "bg": bg, "pw": pw, "cw": cw,
                "tm": bm,                           # (2.6.74) the tray window's margin: the bar's own
                # (2.6.74) where each cell sits along a row (from its panel's left edge)
                # and each row down the bar (from the margin), so the zone fit can
                # stretch them (_stretch); the bar's own: evenly by pitch
                "colx": tuple(p4 + i * pitch for i in range(TOP_SLOTS)),
                "colw": (S,) * TOP_SLOTS, "top_w": TOP_SLOTS * pitch + p4,
                "sgx": sg, "sgc": sg,               # bottom-row panels' gaps; before the column
                "rowy": tuple(r * (ph + sg) for r in range(rows)), "rowh": (ph,) * rows,
                "celly": (p4,) * rows, "cellh": (S,) * rows,
                "W": m + inner + sg + cw + m,
                "H": m + rows * ph + (rows - 1) * sg + m}


    def _share(total, n):
        """(2.6.74) total px shared over n places as evenly as whole px allow (the
        odd px spread along, never bunched at one end)."""
        if n <= 0:
            return []
        if total <= 0:
            return [0] * n
        return [(total * (i + 1)) // n - (total * i) // n for i in range(n)]


    def _stretch(L, along, across):
        """(2.6.74) The bar's own geometry L stretched to exactly along x across px
        (flat layout; the told slot, turned for an upright bar). Along: the gaps
        between cells and between groups grow first (up to FIT_GAP_MAX x), then
        the cells widen (up to FIT_CELL_MAX x, the icon square in the middle),
        then the window buttons' and bag panels take the rest (with rows above,
        the gaps take it too, so they still end level with the bottom row).
        Across, the same: the gaps between rows, then the cells deepen, then the
        rows' panels. Where the bar is bigger than its slot (Scale % at its
        least) it stays as it is that way."""
        L = dict(L)
        S, p4, sg, rows = L["S"], L["p4"], L["sg"], L["rows"]
        gap = L["pitch"] - S
        n = TOP_SLOTS
        grow = FIT_GAP_MAX - 1.0
        deep = max(0, int(S * FIT_CELL_MAX) - S)    # most px a cell may widen (or deepen)
        spare = along - L["W"]
        if spare > 0:
            cap1 = n * gap + sg
            s1 = min(spare, int(cap1 * grow))
            t = float(s1) / cap1 if cap1 > 0 else 0.0
            dc = min(s1, int(round(sg * t)))        # the gap before the KEY / LOCK / GRID column
            gaps = [gap + d for d in _share(s1 - dc, n)]
            s2 = min(spare - s1, n * deep)
            colw = [S + d for d in _share(s2, n)]
            s3 = spare - s1 - s2
            tail = 0
            if s3 > 0:
                if rows > 1:
                    gaps = [a + d for a, d in zip(gaps, _share(s3, n))]
                else:                               # the bottom row alone: its right panels
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
            s1 = min(spare, int((rows - 1) * sg * grow))
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
        """Horizontal (True) or upright (False): the layout below is worked out
        as rows and transposed when the bar stands upright."""
        return not eff_vertical()


    def bar_size():
        """(w, h) of the bar as drawn right now."""
        if st["minimized"]:
            return MINI_W, MINI_H
        L = geom()
        return (L["W"], L["H"]) if flat() else (L["H"], L["W"])


    def R(x, y, w, h):
        """A rect of the flat layout, as drawn: the same, or transposed (and, in
        a zone, moved by where the bar sits in its slot)."""
        ox, oy = fitst["off"]
        return (x + ox, y + oy, w, h) if flat() else (y + ox, x + oy, h, w)


    def add_item_pic(g, graphic, hue, x, y, w, h):
        try:
            p = G.CreateGumpItemPic(int(graphic), int(w), int(h))
        except Exception:
            return None
        if hue:
            try:                                 # 2.6.82: plain try, no lambdas
                p.Hue = int(hue)
            except Exception:
                pass
        p.SetPos(x, y)
        try:
            p.SetAcceptMouseInput(False)
        except Exception:
            pass
        g.Add(p)
        return p


    def caption_words(text):
        """(2.6.72) A name as words to wrap: CamelCase and underscores split
        ("ClearHands" -> "Clear Hands", "pre_bless" -> "pre bless")."""
        t = str(text).replace("_", " ")
        out = []
        for i, ch in enumerate(t):
            if i and ch.isupper() and t[i - 1].islower():
                out.append(" ")
            out.append(ch)
        return "".join(out)


    KEY_LINE = 14                 # (2.6.85) px a cell's hotkey keeps at its top

    def add_cell_text(g, text, x, y, w, h, hue=None):
        # (2.6.72) words split first, up to 3 lines when the cell is tall enough, and a
        # cut keeps the standard ".." tail (the one-dot cut read as "Clear.", "Bands.")
        most = max(1, min(3, (h - 2) // 14))
        lines = [Kit.fit(l, w - 4) for l in Kit.wrap(caption_words(text), w - 4)]
        if len(lines) > most:
            lines = lines[:most]
            lines[-1] = Kit.fit(lines[-1] + "..", w - 4) if not lines[-1].endswith("..") \
                else lines[-1]
        ty = y + (h - 14 * len(lines)) // 2 - 1
        return [Kit.add_label(g, l, x + (w - Kit.text_w(l)) // 2, ty + i * 14,
                              Kit.HUE_TEXT if hue is None else hue) for i, l in enumerate(lines)]


    def click_handler(kind, menu_kind, arg):
        """A cell's / bag slot's click handler. Without a right-click hook,
        Shift+click stands in for it."""
        def fn():
            if st["right_ok"] is False and key_down("SHIFT"):
                st["queue"].append((menu_kind, arg))
            else:
                st["queue"].append((kind, arg))
        return fn


    _right = {"ev": {}, "prop": {}, "add": {}, "mods": None}


    def hook_right(api_ctrl, fn):
        """Run fn (queued, on the module's next tick) when the control is
        right-clicked: the client's own MouseUp event, found the way
        Kit.hook_double finds MouseDoubleClick. The first failure turns the
        Shift+click fallback on."""
        if api_ctrl is None or st["right_ok"] is False:
            return False
        try:
            mods = _right["mods"]                # 2.6.82: imported once, not per cell
            if mods is None:
                import clr
                import System
                from System.Reflection import BindingFlags
                mods = _right["mods"] = (clr, System, BindingFlags.Instance |
                                         BindingFlags.Public | BindingFlags.NonPublic)
            clr, System, flags = mods
            prop = _right["prop"].get(type(api_ctrl))    # looked up once per control type
            if prop is None:
                t = clr.GetClrType(type(api_ctrl))
                while t is not None and prop is None:
                    prop = t.GetProperty("Control", flags)
                    t = t.BaseType
                _right["prop"][type(api_ctrl)] = prop
            ctrl = prop.GetValue(api_ctrl, None)
            key = str(ctrl.GetType().FullName)
            ev = _right["ev"].get(key)
            if ev is None:
                t = ctrl.GetType()
                while t is not None and ev is None:
                    ev = t.GetEvent("MouseUp", flags)
                    t = t.BaseType
                _right["ev"][key] = ev

            def handler(sender, e):
                try:
                    if str(e.Button) == "Right":
                        Kit.pending.append(fn)
                        e.Result = True
                except Exception:
                    pass
            add = _right["add"].get(key)         # 2.6.82: delegate type, add method once
            if add is None:
                add = _right["add"][key] = (clr.GetPythonType(ev.EventHandlerType),
                                            ev.GetAddMethod(True))
            add[1].Invoke(ctrl, System.Array[object]([add[0](handler)]))
            st["right_ok"] = True
            return True
        except Exception:
            if st["right_ok"] is None:
                st["right_ok"] = False
                API.SysMsg("Action Bar: no right-click events from this client; "
                           "Shift+click a cell for its menu instead.", Kit.HUE_INFO)
            return False


    def add_icon(g, icon, x, y, w, h):
        """Gump-art icon stretched to the cell (GumpPic scales to its size)."""
        side = min(w, h) - 4
        p = Kit.add_pic(g, icon, x + (w - side) // 2, y + (h - side) // 2)
        if p is not None:                        # 2.6.82: plain try, no lambdas
            try:
                p.SetWidth(side)
            except Exception:
                pass
            try:
                p.SetHeight(side)
            except Exception:
                pass
            try:
                p.SetAcceptMouseInput(False)
            except Exception:
                pass
        return p


    def group_panel(g, rect, unified):
        """(2.6.72) A group's panel: the dark framed panel, or with one frame on a
        black section like every other window's panels."""
        if unified:
            Kit.add_section(g, *rect)
        else:
            Kit.add_resizepic(g, SLOT_FRAME, *rect)


    def draw_cell(g, ref, x, y, w, h, framed):
        """A cell: its background, which stays for the life of the bar, then
        what it holds (cell_content), which can be drawn again on its own.
        (2.6.72) An empty cell is a faint outline, not a solid dark square."""
        if framed:
            Kit.add_resizepic(g, SLOT_FRAME, x, y, w, h)
        elif not cell(ref)["t"]:
            Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA * 0.3)
            for bx, by, bw_, bh_ in ((x, y, w, 1), (x, y + h - 1, w, 1), (x, y, 1, h),
                                     (x + w - 1, y, 1, h)):
                Kit.add_tiled(g, SLOT_TILE, bx, by, bw_, bh_, SLOT_ALPHA)
        else:
            Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        cell_content(g, ref, x, y, w, h)


    def pic_box(ref, x, y, w, h, pad):
        """(2.6.74) Where an item picture goes in a cell, pad px in: in a cell the
        zone fit made wider (or deeper) than square it stays square, in the
        middle; a window button (the "u" row) is a rectangle by design."""
        if w == h or ref[0] == "u":
            return x + pad, y + pad, w - 2 * pad, h - 2 * pad
        side = min(w, h) - 2 * pad
        return x + (w - side) // 2, y + (h - side) // 2, side, side


    def cell_content(g, ref, x, y, w, h):
        """What a cell holds: icon or caption, counter, hotkey and the click
        catcher on top. Its controls are kept in info["parts"], so a page
        switch, a weapon swap or a changed cell redraws just those cells in
        place (redraw_now) instead of rebuilding the whole bar."""
        c = cell(ref)
        t = c["t"]
        info = {"x": x, "y": y, "w": w, "h": h, "count": None}
        parts = []
        shown = False
        # (2.6.85) the hotkey sits in the top right corner on a line of its own; a caption
        # gets the cell under it, so the two never touch
        ky = KEY_LINE if (settings["keys"] and c["k"] and t) else 0
        if t == "item" and c["g"]:
            p = add_item_pic(g, c["g"], c["h"], *pic_box(ref, x, y, w, h, 3))   # (2.6.74)
            shown = p is not None
            parts.append(p)
        elif t == "spell":
            icon = spell_icon(c["v"])
            if icon:
                p = add_icon(g, icon, x, y, w, h)
                shown = p is not None
                parts.append(p)
                info["icon"] = p                 # greyed while a reagent is at 0 (grey_cell)
        elif t == "travel":
            # the way's icon, faded, under the rune's name (one line)
            m = c.get("rm")
            p = None
            if m in TRAVEL_SPELL:
                icon = spell_icon(TRAVEL_SPELL[m])
                if icon:
                    p = add_icon(g, icon, x, y, w, h)
            elif m in TRAVEL_ITEM:
                p = add_item_pic(g, TRAVEL_ITEM[m], 0, *pic_box(ref, x, y, w, h, 3))   # (2.6.74)
            if p is not None:
                safe(lambda: p.SetAlpha(TRAVEL_ICON))
                parts.append(p)
            name = fit(c["v"] or "?", w - 4)
            parts.append(Kit.add_label(g, name, x + (w - Kit.text_w(name)) // 2,
                                       y + ky + (h - ky - 14) // 2 - 1))
            shown = True
        elif t == "ability":
            icon, name = ability_info(c["v"])
            if icon:
                p = add_icon(g, icon, x, y, w, h)
                shown = p is not None
                parts.append(p)
            elif name:
                parts.extend(add_cell_text(g, name, x, y + ky, w, h - ky))
                shown = True
        elif t == "ui":
            d = ui_def(c["v"])
            if d and d[2]:
                p = add_item_pic(g, d[2], 0, *pic_box(ref, x, y, w, h, 2))   # (2.6.74)
                shown = p is not None
                parts.append(p)
        elif t == "script":
            # (2.6.72) a script named after a spell ("GreaterHeal.py") shows that spell's icon
            nm = caption_words(cell_text(c)).strip().lower()
            icon = SPELL_ICON.get(nm) if nm else None
            if icon and Kit.pic_size(icon)[0] > 0:
                p = add_icon(g, icon, x, y, w, h)
                shown = p is not None
                parts.append(p)
        if t and not shown:
            parts.extend(add_cell_text(g, cell_text(c), x, y + ky, w, h - ky))
        if t in ("item", "spell", "ability", "script", "skill", "travel"):
            info["count"] = Kit.add_label(g, "", x + w - 6, y + h - 16)
            info["txt"], info["hue"] = "", Kit.HUE_TEXT
            parts.append(info["count"])
        if settings["keys"] and c["k"] and t:
            kt = fit(short_key(c["k"]), w - 4)
            info["key"] = Kit.add_label(g, kt, x + w - 2 - Kit.text_w(kt), y + 1, Kit.HUE_INFO)
            parts.append(info["key"])
        info["tip"] = describe(ref)
        info["catcher"] = Kit.catcher(g, x, y, w, h, click_handler("click", "menu", ref),
                                      info["tip"])
        parts.append(info["catcher"])
        hook_right(info["catcher"], queue(("menu", ref)))
        info["parts"] = parts
        win["cells"][ref] = info
        _counters[0] = None                     # 2.6.82: the counter list is made again


    def bag_tip(i):
        """Tooltip of bag slot i for the bar's current state."""
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
        Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        bag_content(g, i, x, y, w, h)


    def bag_content(g, i, x, y, w, h):
        """What bag slot i shows (kept in info["parts"], like cell_content)."""
        b = bag_at(i)
        info = {"x": x, "y": y, "w": w, "h": h, "count": None}
        parts = []
        if b:
            if b["g"]:
                parts.append(add_item_pic(g, b["g"], b["h"], x + 3, y + 3, w - 6, h - 6))
            info["count"] = Kit.add_label(g, "", x + w - 6, y + h - 16)
            info["txt"], info["hue"] = "", Kit.HUE_TEXT
            parts.append(info["count"])
        bk = bag_keys()[i]
        if bk and settings["keys"]:
            kt = fit(short_key(bk), w - 4)
            info["key"] = Kit.add_label(g, kt, x + w - 2 - Kit.text_w(kt), y + 1, Kit.HUE_INFO)
            parts.append(info["key"])
        info["tip"] = bag_tip(i)
        info["catcher"] = Kit.catcher(g, x, y, w, h, click_handler("bag", "bagmenu", i),
                                      info["tip"])
        parts.append(info["catcher"])
        hook_right(info["catcher"], queue(("bagmenu", i)))
        info["parts"] = parts
        win["bags"][i] = info


    def want_redraw(refs):
        """These cells (and ("b", i) bag slots) are drawn again, in place, on
        the bar's next tick."""
        st["redraw"].update(refs)


    def redraw_now():
        """Draw the cells / bag slots in st["redraw"] again where they are: their
        old content controls go, new ones are added on top of the cell's
        background (the catcher last, so it still takes the clicks). One hop;
        a page switch is ~50 controls instead of the whole bar's ~400."""
        refs, st["redraw"] = st["redraw"], set()
        g = win["g"]
        if not refs or st["minimized"] or not Kit.is_open(g):
            return                                # a later build draws them anyway

        def work():
            for ref in sorted(refs):
                bag = ref[0] == "b"
                info = win["bags"].get(ref[1]) if bag else win["cells"].get(ref)
                if info is None:                  # not on the bar (hidden row)
                    continue
                for p in info.get("parts") or ():
                    Kit.dispose(p)
                if bag:
                    bag_content(g, ref[1], info["x"], info["y"], info["w"], info["h"])
                else:
                    cell_content(g, ref, info["x"], info["y"], info["w"], info["h"])
            update_labels()
        on_client(work)


    # ---------- small changes drawn in place (no rebuild of the bar) ----------
    def refresh_key(ref):
        """One cell's / bag slot's hotkey corner label and tooltip, in place."""
        g = win["g"]
        if ref[0] == "b":
            info, k = win["bags"].get(ref[1]), bag_keys()[ref[1]]
            tip = bag_tip(ref[1]) if info else ""
        else:
            info, k = win["cells"].get(ref), cell(ref)["k"]
            tip = describe(ref) if info else ""
        if info is None or not Kit.is_open(g):
            return
        text = fit(short_key(k), info["w"] - 4) if (settings["keys"] and k and
                                                   (ref[0] == "b" or cell(ref)["t"])) else ""
        lbl = info.get("key")
        if text and lbl is None:
            lbl = Kit.add_label(g, text, info["x"] + info["w"] - 2 - Kit.text_w(text), info["y"] + 1,
                                Kit.HUE_INFO)
            safe(lambda: lbl.SetAcceptMouseInput(False))
            info["key"] = lbl
            info.setdefault("parts", []).append(lbl)     # goes with the cell's next redraw
        elif lbl is not None:
            safe(lambda: setattr(lbl, "Text", text))
        set_tip(info, tip)


    def set_tip(info, tip):
        """A cell's / bag slot's tooltip, set only when it changes."""
        c = info.get("catcher")
        if c is not None and info.get("tip") != tip:
            info["tip"] = tip
            safe(lambda: c.SetTooltip(tip))


    def cells_with(t):
        """[(ref, cell)] of every cell of kind t on the bar."""
        out = []
        for kind in ("a", "x", "u"):
            for i, c in enumerate(cells[kind]):
                if c["t"] == t:
                    out.append(((kind, i), c))
        return out


    def refresh_tips():
        """The tooltips that name Bags', Grimoire's and Virtue
        Assistant's state, in place: the bag slots and the Grimoire and
        Virtue Assistant buttons (no other cell's tooltip depends on them)."""
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
        """A small button's (draw_small_button) colour and tooltip, in place."""
        for lbl in btn.get("text", []):
            safe(lambda lbl=lbl: setattr(lbl, "Hue", hue))
        if btn.get("pic") is not None:
            safe(lambda: setattr(btn["pic"], "Hue", 0 if hue == Kit.HUE_TEXT else hue))
        if btn.get("catcher") is not None:
            safe(lambda: btn["catcher"].SetTooltip(tip))


    def refresh_bind_button():
        """The KEY button shows keybind mode (gold) or not, in place."""
        btn = win.get("keybtn")
        if btn and Kit.is_open(win["g"]):
            recolor(btn, *bind_look())


    def refresh_tray():
        """The tray button's count and the tray window follow the folded
        windows; the bar itself stays as it is."""
        if not Kit.is_open(win["g"]):
            return
        btn = win.get("traybtn")
        if btn:
            n = len(tray_docks())
            hue = Kit.HUE_TITLE if n else Kit.HUE_INFO
            for lbl in btn.get("text", []):
                safe(lambda lbl=lbl: setattr(lbl, "Text", str(n)))
                safe(lambda lbl=lbl: setattr(lbl, "Hue", hue))
                safe(lambda lbl=lbl: Kit.ui_pos(lbl, btn["x"] + (btn["w"] - Kit.text_px(str(n))) // 2,
                                                btn["ly"]))
            if btn.get("catcher") is not None:
                safe(lambda: btn["catcher"].SetTooltip(tray_tip(n)))
        on_client(build_tray)


    def draw_page_column(g, store, x, y0, ph, PAGE_W):
        """Tiny up / down arrows and the page number, left of the bottom-left
        cells (flat layout coordinates; drawn through R)."""
        p = settings["page"]
        aw, ah = Kit.pic_size(Kit.ART_RESTORE[0])
        aw, ah = aw or 16, ah or 16
        cx = x + (PAGE_W - aw) // 2
        ax, ay = R(cx, y0 + 1, aw, ah)[:2]
        up = Kit.art_button(g, store, "pgup", Kit.ART_RESTORE, ax, ay, None,
                            "Next page of the bottom-left cells (page %d of %d showing)" % (p + 1, PAGES),
                            on_click=queue(("page", 1)))
        ax, ay = R(cx, y0 + ph - ah - 1, aw, ah)[:2]
        dn = Kit.art_button(g, store, "pgdn", Kit.ART_MIN, ax, ay, None,
                            "Previous page of the bottom-left cells (page %d of %d showing)" % (p + 1, PAGES),
                            on_click=queue(("page", -1)))
        num = str(p + 1)
        nx, ny, nw, nh = R(x, y0 + ah + 1, PAGE_W, max(1, ph - 2 * ah - 2))
        lbl = Kit.add_label(g, num, nx + (nw - Kit.text_w(num)) // 2, ny + (nh - 14) // 2,
                            Kit.HUE_TITLE)
        c = Kit.catcher(g, nx, ny, nw, nh, queue(("page", 1)),
                        "Page %d of %d of the bottom-left cells; click for the next page" % (p + 1, PAGES))
        win["pagecol"] = {"up": up, "dn": dn, "num": lbl, "catcher": c, "rect": (nx, ny, nw, nh),
                          "page": p}


    def refresh_page_column():
        """The page number and the page arrows' tooltips, in place (set_page)."""
        pc = win.get("pagecol")
        p = settings["page"]
        if not pc or pc["page"] == p or not Kit.is_open(win["g"]):
            return
        pc["page"] = p
        num = str(p + 1)
        nx, ny, nw, nh = pc["rect"]
        lbl = pc["num"]
        Kit.set_text(lbl, num)
        safe(lambda: Kit.ui_pos(lbl, nx + (nw - Kit.text_w(num)) // 2, ny + (nh - 14) // 2))
        for k, tip in (("up", "Next page of the bottom-left cells (page %d of %d showing)"),
                       ("dn", "Previous page of the bottom-left cells (page %d of %d showing)"),
                       ("catcher", "Page %d of %d of the bottom-left cells; click for the next page")):
            ctl = pc[k]
            safe(lambda: ctl.SetTooltip(tip % (p + 1, PAGES)))


    def draw_tray(g, key, d, x, y, w, h):
        """One tray button: a window that folds into the bar."""
        Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        state = safe(d.get("state"))
        title = d.get("title") or key
        hue = 0 if state == "open" else Kit.HUE_INFO
        icon = d.get("icon") or 0
        shown = icon and add_item_pic(g, icon, hue, x + 2, y + 2, w - 4, h - 4) is not None
        if not shown:
            add_cell_text(g, title[:3].upper(), x, y, w, h, Kit.HUE_TEXT if state == "open"
                          else Kit.HUE_INFO)
        tip = ("%s is off; click to turn it on" if state is None else
               "Fold %s into the bar" if state == "open" else "Show %s") % title
        Kit.catcher(g, x, y, w, h, queue(("dock", key)), tip)


    def draw_small_button(g, box, caption, fn, hue, tip):
        """A dark little button with its caption (2.6.75: always the caption; the
        column is made room for it, ctrl_need). Returns its parts, so it can be
        recoloured in place later."""
        x, y, w, h = box
        Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        parts = {"text": add_cell_text(g, caption, x, y, w, max(16, h), hue), "pic": None}
        parts["catcher"] = Kit.catcher(g, x, y, w, h, fn, tip)
        return parts


    def bind_look():
        """(hue, tooltip) of the KEY button."""
        if st["bind"] is not None:
            return Kit.HUE_TITLE, ("Keybind mode is on: hover a cell and press a key or combination. "
                                   "Esc or a click here ends it; Backspace clears a key.")
        return Kit.HUE_TEXT, ("Start keybind mode: hover a cell on the bar and press the key or "
                              "combination to bind to it")


    def tray_tip(n):
        return "%d window%s folded into the bar; click to %s" % (
            n, "" if n == 1 else "s",
            "fold the tray away" if settings["tray_open"] else "show the tray")


    def draw_ctrl_column(g, store, L):
        """Far right (flat layout): minimize arrow, then the Keys (keybind mode),
        Lock and Grid buttons, stacked when the bar is tall enough. (2.6.75) Else
        a compact grid of short text buttons (arrow and Keys, then Lock and Grid;
        or one row), never item icons: the column is made wide enough for it
        (ctrl_need). Drawn through R."""
        BAR_M, CTRL_W = L["m"], L["cw"]
        x = BAR_M + L["inner"] + L["sgc"]               # (2.6.74) the gaps from the geometry
        col_h = L["rowy"][-1] + L["rowh"][-1]           # (stretched in a zone)
        aw, ah = Kit.pic_size(Kit.ART_MIN[0])
        aw, ah = aw or 16, ah or 16
        ty = BAR_M + 2 + ah + 4
        avail = BAR_M + col_h - ty
        capw = ctrl_capw()
        acts = (("Keys", queue(("bind",)), bind_look()), ("Lock", queue(("lockbar",)), lock_look()),
                ("Grid", queue(("grid",)), grid_look()))
        if flat() and avail >= 66 and CTRL_W - 4 >= capw:   # stacked (as before 2.6.74)
            mx, my = R(x + (CTRL_W - aw) // 2, BAR_M + 2, aw, ah)[:2]
            bw_, bh_ = CTRL_W - 4, min(28, (avail - 8) // 3)
            boxes = [R(x + 2, ty + i * (bh_ + 4), bw_, bh_) for i in range(3)]
        else:
            # (2.6.75) in drawn px: the column's rect as it shows (upright: across the foot)
            dx, dy, dw, dh = R(x, BAR_M, CTRL_W, col_h)
            vert = not flat()
            pick = None
            for c in ctrl_orders(vert):
                rows, cell_w, cell_h = ctrl_cells(c, dw, dh)
                if cell_w >= capw and cell_h >= CTRL_ROW_MIN:
                    pick = (c, rows, cell_w, cell_h)
                    break
            if pick is None:                              # the roomiest cells, text cut to fit
                best = None
                for c in ctrl_orders(vert):
                    rows, cell_w, cell_h = ctrl_cells(c, dw, dh)
                    room = min(cell_w - capw, cell_h - CTRL_ROW_MIN)
                    if best is None or room > best[0]:
                        best = (room, c, rows, cell_w, cell_h)
                pick = best[1:]
            c, rows, cell_w, cell_h = pick
            cell_w, cell_h = max(1, cell_w), max(1, cell_h)
            block_w = c * cell_w + (c - 1) * CTRL_PAD
            block_h = rows * cell_h + (rows - 1) * CTRL_PAD
            x0 = dx + max(CTRL_PAD, (dw - block_w) // 2)
            y0 = dy + max(CTRL_PAD, (dh - block_h) // 2)
            cells = [(x0 + (n % c) * (cell_w + CTRL_PAD), y0 + (n // c) * (cell_h + CTRL_PAD),
                      cell_w, cell_h) for n in range(4)]
            ax, ay = cells[0][0], cells[0][1]
            mx, my = ax + (cell_w - aw) // 2, ay + (cell_h - ah) // 2
            boxes = cells[1:]
        if not layout_held():                    # (2.6.85) a window in a zone is always up
            Kit.art_button(g, store, "min", Kit.ART_MIN, mx, my, None, "Minimize the bar",
                           on_click=queue(("toggle_min",)))
        # (2.6.72) captions in sentence case (UI rules 3.2)
        btns = []
        for (cap, fn, look), box in zip(acts, boxes):
            btns.append(draw_small_button(g, box, cap, fn, *look))
        win["keybtn"], win["lockbtn"], win["gridbtn"] = btns


    # ---------- the screen grid (lives in the host; any window snaps to it) ----------
    def grid_look():
        """(hue, tooltip) of the GRID button."""
        if safe(HOST.grid_shown, False):
            return Kit.HUE_TITLE, ("The screen grid is on; click to hide it. While it shows, "
                                   "every Virtue Assistant window you let go snaps to its lines.")
        return Kit.HUE_INFO, ("Show a grid over the whole screen; windows you let go snap to "
                              "its lines, the screen's corners, edge midpoints and centre")


    def toggle_grid():
        on = bool(safe(HOST.grid_toggle, False))
        btn = win.get("gridbtn")
        if btn and Kit.is_open(win["g"]):
            recolor(btn, *grid_look())
        API.SysMsg("Action Bar: screen grid %s." % ("shown" if on else "hidden"), Kit.HUE_INFO)


    def zones_in_use():
        return bool(safe(lambda: HOST.layout_in_use(), False))


    def lock_look():
        """(hue, tooltip) of the Lock button. (2.6.72) While windows sit in zones
        it is the layout's lock: it turns Arrange mode on and off."""
        if zones_in_use():
            if safe(lambda: HOST.layout_arranging(), False):
                return Kit.HUE_TITLE, "Lock every window in its zone"
            return Kit.HUE_INFO, "Unlock the layout so windows can be moved between zones"
        if settings["lock"]:
            return Kit.HUE_BAD, "The bar is locked; click to unlock it"
        return Kit.HUE_INFO, "The bar can be dragged; click to lock it in place"


    def refresh_lock_button():
        """The LOCK button and the bar's draggability, in place. False if the
        bar can't be changed in place (then it is rebuilt)."""
        g, btn = win["g"], win.get("lockbtn")
        if not btn or not Kit.is_open(g):
            return False
        # (2.6.72) a bar held in its zone stays put (the layout's lock; Arrange moves it)
        can = not settings["lock"] and not safe(lambda: HOST.layout_locked(KEY), False)
        try:
            g.Gump.CanMove = can                    # the client's own gump object
        except Exception:
            try:
                setattr(g, "CanMove", can)
            except Exception:
                return False
        recolor(btn, *lock_look())
        win["arranging"] = safe(lambda: HOST.layout_arranging(), False)
        return True


    def build_window():
        """Draw the bar (and its tray). Done in one hop on the client thread,
        where creating ~400 controls costs a few milliseconds instead of one
        client update pass each; built here the slow way if that can't be."""
        if BUILD_ON_CLIENT and on_client(_build_window_now, fallback=False) is True:
            return
        for g in win.pop("stale", []):           # a build that failed half-way
            Kit.dispose(g)
        _build_window_now()


    WIN_PARTS = ("g", "store", "cells", "bags", "keybtn", "lockbtn", "gridbtn", "traybtn", "pagecol")


    def _build_window_now():
        """Builds the new bar beside the old one, then swaps. If a gump call
        fails half-way (a client build that throws), the old bar is put back
        exactly as it was (its controls, counters and hotkeys keep working) and
        the half-built one is disposed before the error goes up to the host,
        so an error report never leaves the module without a bar."""
        keep = dict((k, win.get(k)) for k in WIN_PARTS)    # the bar as it is now
        old = keep["g"]
        if Kit.is_open(old):
            x, y = old.GetX(), old.GetY()
        else:
            x, y = None, None
        win["g"] = None
        win.setdefault("stale", []).append(old)   # disposed once the new bar is up
        win["keybtn"], win["lockbtn"], win["gridbtn"], win["traybtn"] = None, None, None, None
        win["pagecol"] = None
        store = ({}, {})
        win["cells"], win["bags"] = {}, {}
        _counters[0] = None
        built = {"g": None}
        try:
            _draw_bar(x, y, store, built)
        except Exception:
            if win["g"] is None:                  # failed before the swap: the old bar
                Kit.dispose(built["g"])           # stays, as it was; the half-built one goes
                win.update(keep)
                _counters[0] = None
                win["stale"] = [s for s in win.get("stale", []) if s is not old]
            else:                                 # failed after it: the new bar is up
                for s in win.pop("stale", []):    # and the old one goes
                    Kit.dispose(s)
            raise
        return True


    def _draw_bar(x, y, store, built):
        """The body of _build_window_now: draws the bar at (x, y) (None, None =
        its saved place), puts it up and disposes the old one."""
        # 2.6.81: a bar the layout holds in a zone is made unmovable at once
        # (window rules: ask layout_locked before making a draggable window)
        held_lock = bool(safe(lambda: HOST.layout_locked(KEY), False))
        if st["minimized"]:
            w, h = MINI_W, MINI_H
            if x is None:
                x, y = Kit.load_pos(POS_KEY, (200, 600), (w, h))   # saved place (a database read)
            g = built["g"] = G.CreateGump(True, not held_lock)
            Kit.mini_bar(g, store, w, h, TITLE, KEY, queue(("toggle_min",)), TITLE)
        else:
            # The layout is worked out flat (rows); upright, every rect goes
            # through R, which transposes it, so the rows stand as columns.
            unified = bool(safe(lambda: HOST.layout_unified(KEY), False))
            refit_if_stale(unified)              # (2.6.74) a zone fit for other settings
            L = geom()
            w, h = bar_size()
            fitst["off"] = (0, 0)
            slot = told_slot()
            if slot is not None:                 # (2.6.57) exactly its slot ((2.6.74) the stretch
                #                                  fills it; centred only if it can't shrink to it)
                fitst["off"] = (max(0, (slot[0] - w) // 2), max(0, (slot[1] - h) // 2))
                w, h = max(w, slot[0]), max(h, slot[1])
            if x is None:
                x, y = Kit.load_pos(POS_KEY, (200, 600), (w, h))   # saved place (a database read)
            BAR_M, PAGE_W, p4 = L["m"], L["pw"], L["p4"]
            UI_GAP, BAG_GAP, TRAY_BTN = L["ug"], L["bg"], L["tb"]
            # (2.6.74) cells, gaps and rows from the geometry's lists (stretched in a zone)
            SGX, colx, colw = L["sgx"], L["colx"], L["colw"]
            rowy, rowh, celly, cellh = L["rowy"], L["rowh"], L["celly"], L["cellh"]
            x0 = BAR_M + PAGE_W                  # the rows' panels start here
            g = built["g"] = G.CreateGump(True, not settings["lock"] and not held_lock)
            Kit.add_window_frame(g, w, h, corners=False)
            # extra rows (highest first), then the top row: squares on a group panel the
            # height of the bottom row's (2.6.72: indented by the page column, so the
            # rows line up cell for cell; they were bare cells, the bottom row framed)
            r = 0
            for kind, base in ([("x", k * TOP_SLOTS) for k in range(settings["extra"] - 1, -1, -1)]
                               + ([("a", 0)] if settings["top"] else [])):
                y0 = BAR_M + rowy[r]
                group_panel(g, R(x0, y0, L["top_w"], rowh[r]), unified)
                cy, ch = y0 + celly[r], cellh[r]
                for i in range(TOP_SLOTS):
                    draw_cell(g, (kind, base + i), *R(x0 + colx[i], cy, colw[i], ch), framed=False)
                r += 1
            y0, ph = BAR_M + rowy[r], rowh[r]    # the bottom row
            cy, ch = y0 + celly[r], cellh[r]
            draw_page_column(g, store, BAR_M, y0, ph, PAGE_W)  # page arrows and number
            # bottom left (one page): (2.6.73) the same squares on the same group panel as
            # the rows above, no gold-rimmed frame round each cell
            group_panel(g, R(x0, y0, L["left_w"], ph), unified)
            for i in range(BOTTOM_SLOTS):
                draw_cell(g, ("a", TOP_SLOTS + i), *R(x0 + colx[i], cy, colw[i], ch), framed=False)
            ux = x0 + L["left_w"] + SGX              # window buttons on a lighter panel
            group_panel(g, R(ux, y0, L["ui_w"], ph), unified)
            if not unified:                          # (2.6.72) one frame: panels only, no stone
                Kit.add_tiled(g, Kit.STONE_TILE, *R(ux + p4, y0 + p4, L["ui_w"] - 2 * p4,
                                                    ph - 2 * p4), alpha=UI_PANEL_ALPHA)
            total = UI_SLOTS * L["bw"] + (UI_SLOTS - 1) * UI_GAP
            bx = ux + (L["ui_w"] - total) // 2
            for i in range(UI_SLOTS):
                draw_cell(g, ("u", i), *R(bx + i * (L["bw"] + UI_GAP), y0 + (ph - L["bh"]) // 2,
                                          L["bw"], L["bh"]), framed=False)
            gx = ux + L["ui_w"] + SGX                # bag slots
            group_panel(g, R(gx, y0, L["bag_w"], ph), unified)
            total = BAG_SLOTS * L["bgw"] + (BAG_SLOTS - 1) * BAG_GAP
            bx = gx + (L["bag_w"] - total) // 2
            for i in range(BAG_SLOTS):
                draw_bag(g, i, *R(bx + i * (L["bgw"] + BAG_GAP), cy, L["bgw"], L["bgh"]))
            tx = gx + L["bag_w"] + SGX                # the tray button
            group_panel(g, R(tx, y0, L["tray_w"], ph), unified)
            draw_tray_button(g, *R(tx + p4, cy, TRAY_BTN, L["bgh"]))
            draw_ctrl_column(g, store, L)            # minimize, KEY, LOCK, GRID
            safe(lambda: setattr(g, "CanCloseWithRightClick", False))
        if settings["anchor"] and not layout_held():   # anchored: the screen says where
            #                                  (2.6.81: a bar held in a zone keeps its slot)
            ax, ay = anchor_pos(settings["anchor"], w, h)
            if ax is not None:
                x, y = ax, ay
        x, y = Kit.place(g, x, y, w, h)             # wholly on screen
        st["last_pos"], st["moved_at"] = (x, y), None
        win.update({"g": g, "store": store})        # the swap: from here the new bar is the bar
        G.AddControlOnDisposed(g, on_disposed(g))
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, save_pos))  # saved the moment you let go of it
        for s in win.pop("stale", []):
            Kit.dispose(s)
        if not st["minimized"]:
            count_if_stale()                     # 2.6.82: restored / started: fresh counters
        update_labels()
        build_tray()
        return True


    def draw_tray_button(g, x, y, w, h):
        """The bar's one tray button: how many windows are folded in; click to
        show the tray window beside the bar or fold it back into the bar."""
        n = len(tray_docks())
        Kit.add_tiled(g, SLOT_TILE, x, y, w, h, SLOT_ALPHA)
        labels = add_cell_text(g, str(n), x, y, w, h, Kit.HUE_TITLE if n else Kit.HUE_INFO)
        win["traybtn"] = {"text": labels, "x": x, "w": w, "ly": y + (h - 14) // 2 - 1,
                          "catcher": Kit.catcher(g, x, y, w, h, queue(("traywin",)), tray_tip(n))}


    _rect_fn = getattr(Kit, "rect", None)


    def bar_at():
        """(x, y) of the bar now ((0, 0) when it can't be read). Asked every
        TRAY_EVERY on the client thread: plain try, no lambdas."""
        g = win["g"]
        rect = getattr(Kit, "rect", None)       # (2.6.70) as placed, until the client applies it
        try:
            if rect is not None:
                r = rect(g)
                if r is not None:
                    return int(r[0]), int(r[1])
            return int(g.GetX() or 0), int(g.GetY() or 0)
        except Exception:
            return 0, 0


    def tray_pos(w, h, at=None, rect=False):
        """Where the tray window goes: beside a flat bar (right, bottom edges
        level) or under an upright one (left edges level); on the other side
        when that would leave the screen, and across (under / beside) when
        neither side has room. `at`: the bar's position, if known; `rect`
        (2.6.82): the bar's Kit.rect already read this look (the bar is open)."""
        if rect is False:
            g = win["g"]
            if not Kit.is_open(g):
                return 300, 300
            if at is None:
                at = bar_at()
            try:
                rect = Kit.rect(g) if hasattr(Kit, "rect") else None
            except Exception:
                rect = None
        bx, by = at
        # 2.6.81: always the bar as it is on screen (a zone's fit, or a bar taller
        # or wider than the screen cut to it with a scrollbar: Kit.rect's size
        # includes the scroll band); its drawn size only when that can't be read
        bw, bh = 0, 0
        try:
            r = rect
            if r is not None and r[2] > 0:
                bw, bh = int(r[2]), int(r[3])
        except Exception:
            pass
        if bw <= 0:
            bw, bh = bar_size()
        W, H = Kit.screen()
        if flat():
            x, y = bx + bw + TRAY_GAP, by + bh - h
            if W and x + w > W:
                x = bx - TRAY_GAP - w
                if x < 0:                        # no room either side: under (or over) it
                    x, y = bx, by + bh + TRAY_GAP
                    if H and y + h > H:
                        y = by - TRAY_GAP - h
        else:
            x, y = bx, by + bh + TRAY_GAP
            if H and y + h > H:
                y = by - TRAY_GAP - h
                if y < 0:                        # no room above or below: beside it
                    x, y = bx + bw + TRAY_GAP, by
                    if W and x + w > W:
                        x = bx - TRAY_GAP - w
        return x, y


    def bar_gump():
        """The bar's window, for the layout's registry (HOST.layout_add)."""
        return win["g"]


    def layout_held():
        """Is the bar slotted in a zone of the layout (2.6.54): then the layout
        places it and the anchor rule above stands down."""
        fn = getattr(HOST, "layout_holds", None)
        if fn is None:
            return False
        try:
            return bool(fn(KEY))
        except Exception:
            return False


    # ---------- screen anchors (the host's: the same nine for every window) ----------
    def anchor_pos(name, w, h):
        """(x, y) of a w x h bar sitting on anchor `name`, or (None, None)."""
        return Kit.anchor_pos(name, w, h)


    def anchor_at(x, y, w, h, slack=2):
        """The anchor a w x h bar at (x, y) sits on ("" = free)."""
        return Kit.anchor_at(x, y, w, h, slack)


    def place_on_anchor():
        """Move the bar on to its anchor (after a rebuild, a resolution change)."""
        g = win["g"]
        if not settings["anchor"] or not Kit.is_open(g) or layout_held():
            return
        w, h = bar_size()
        x, y = anchor_pos(settings["anchor"], w, h)
        if x is None:
            return
        if (x, y) != st.get("last_pos"):
            safe(lambda: g.SetPos(x, y))
            safe(lambda: Kit.note_rect(g, x, y))    # (2.6.71) the tray reads the new place
            safe(lambda: Kit.moved_by_code(g))      # a code move, not a drag
            st["last_pos"] = (x, y)
            follow_tray()


    def settle(x, y):
        """The bar came to rest after a drag. Within SNAP_ANCHOR (the host's own
        distance) of a screen anchor it is that anchor's: remembered, and the
        bar is put exactly on it (the host does that too while snapping is on;
        this way it also works with snapping turned off). On a side midpoint
        the bar turns to stand along that side."""
        if st["minimized"]:
            return
        if layout_held():                         # slotted in a zone: the layout places it
            save_pos()
            return
        w, h = bar_size()
        name = anchor_at(x, y, w, h, SNAP_ANCHOR)
        turn = True if name in ANCHORS_VERTICAL else False if name in ANCHORS_HORIZONTAL else None
        turning = turn is not None and turn != settings["vertical"]
        if name != settings["anchor"] or turning:
            settings["anchor"] = name
            if turning:
                settings["vertical"] = turn
                save_settings()
                want_rebuild()                    # rebuilt on the anchor, turned
                API.SysMsg("Action Bar: standing %s along the %s edge." % (
                    "upright" if turn else "flat",
                    {"L": "left", "R": "right", "T": "top", "B": "bottom"}[name]), Kit.HUE_INFO)
                return
            save_settings()
            if name and HOST.debug:
                API.SysMsg("Action Bar: anchored at %s." % name, Kit.HUE_INFO)
        place_on_anchor()                         # exactly on it (no-op when free or there)
        save_pos()


    def watch_position(now):
        """Every TRAY_EVERY: where is the bar? The tray follows it; once it has
        rested for SETTLE_AFTER after moving, its anchor is read (settle)."""
        g = win["g"]
        if not Kit.is_open(g):
            return
        # 2.6.82: speed pass: the bar's rect read once for the look and the tray
        rect = False
        if _rect_fn is not None:
            try:
                rect = _rect_fn(g)
            except Exception:
                rect = None
        if rect:
            try:
                pos = int(rect[0]), int(rect[1])
            except Exception:
                pos = (0, 0)
        else:
            pos = bar_at()
        if pos != st.get("last_pos"):
            st["last_pos"], st["moved_at"] = pos, now
        elif st.get("moved_at") is not None and now - st["moved_at"] >= SETTLE_AFTER:
            if safe(SNAP.pressed) is not True:
                st["moved_at"] = None
                settle(pos[0], pos[1])
        follow_tray(pos, rect)
        if settings["anchor"] and now >= st.get("screen_next", 0.0):
            st["screen_next"] = now + SCREEN_EVERY
            wh = Kit.screen()
            if wh != st.get("screen_wh"):          # resolution changed: stay on the anchor
                st["screen_wh"] = wh
                if not layout_held():              # (slotted in a zone: the layout moves it)
                    place_on_anchor()


    def build_tray():
        """The tray window: one icon per folded window, plus a small arrow
        that folds the tray itself into the bar."""
        old, tray["g"] = tray["g"], None
        docks = tray_docks()
        if st["minimized"] or not settings["tray_open"] or not docks:
            Kit.dispose(old)
            return
        L = geom()
        tb, bg, m = L["tb"], L["bg"], max(4, L["tm"] // 2)   # (2.6.74) the bar's own margin
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
                       "Fold the tray away (the bar's numbered tray button brings it back)",
                       on_click=queue(("traywin",)))
        x, y = tray_pos(w, h)
        Kit.place(g, x, y, w, h)                     # wholly on screen (tray_pos has already
        #                                              picked the side of the bar with room)
        safe(lambda: setattr(g, "CanMove", False))
        safe(lambda: setattr(g, "CanCloseWithRightClick", False))
        tray.update({"g": g, "at": (x, y), "w": w, "h": h})   # "at": the place asked for
        G.AddGump(g)
        safe(lambda: Kit.attach(g, win["g"]))        # it follows the bar by itself
        Kit.dispose(old)


    def follow_tray(at=None, rect=False):
        """Keep the tray beside the bar when the bar is dragged. Every
        TRAY_EVERY on the client thread: no lambdas."""
        g = tray["g"]
        if not Kit.is_open(g):
            return
        w, h = tray.get("w", 0), tray.get("h", 0)
        x, y = tray_pos(w, h, at, rect)
        if (x, y) != tray["at"]:
            tray["at"] = (x, y)
            try:
                cx, cy = Kit.clamp(x, y, w, h)
                g.SetPos(cx, cy)
                Kit.moved_by_code(g)                 # a code move, not a drag
            except Exception:
                pass


    # ---------- doing things ----------
    def open_spellbook():
        count_now(SPELLBOOKS)
        for gr in SPELLBOOKS:
            serial = st["first_g"].get(gr)
            if serial:
                API.UseObject(serial)
                return True
        book = safe(lambda: API.FindLayer("Spellbook"))
        if book:
            API.UseObject(book)
            return True
        API.SysMsg("Action Bar: no spellbook in your pack.", Kit.HUE_BAD)
        return False


    def toggle_lock():
        if zones_in_use():                           # (2.6.72) the layout's lock: Arrange mode
            safe(lambda: HOST.layout_arrange())
            refresh_lock_button()
            return
        settings["lock"] = not settings["lock"]
        save_settings()
        if not refresh_lock_button():
            want_rebuild()
        c = page["c"]
        if c is not None and c.get("chk_lock") is not None:   # the page's box follows
            safe(lambda: setattr(c["chk_lock"], "IsChecked", settings["lock"]))
        else:
            HOST.refresh_settings(KEY)
        API.SysMsg("Action Bar: %s." % ("locked" if settings["lock"] else "unlocked"),
                   Kit.HUE_GOOD)


    # ---------- keybind mode ----------
    def hovered_ref():
        """The cell under the mouse, or None."""
        g = win["g"]
        pos = mouse_pos()
        if pos is None or not Kit.is_open(g):
            return None
        mx = pos[0] - int(safe(lambda: g.GetX(), 0) or 0)
        my = pos[1] - int(safe(lambda: g.GetY(), 0) or 0)
        for ref, info in (list(win["cells"].items()) +
                          [(("b", i), info) for i, info in win["bags"].items()]):
            if info["x"] <= mx < info["x"] + info["w"] and info["y"] <= my < info["y"] + info["h"]:
                return ref
        return None


    def bind_hook(combo):
        def fn(*args):
            if not typing_in_chat():
                st["queue"].append(("bindkey", combo))
        return fn


    def hook_bind_keys():
        """Hook every key combination as a hotkey for the duration of keybind
        mode. Returns the ones that took (other modules' hotkeys are left alone)."""
        hooked = []
        for mod in BIND_MODS:
            for k in POLL_KEYS:
                combo = mod + k
                if key_owner(combo):
                    continue
                try:
                    API.OnHotKey(combo, bind_hook(combo))
                    hooked.append(combo)
                except Exception:
                    pass
        return hooked


    def start_bind(ref=None):
        safe(HOST.release_typing)            # leave any text field, so keys bind
        hooked = []
        if not _hk["ok"]:                    # no client key event: every key as a hotkey
            unregister_hotkeys()             # so a pressed key doesn't fire a cell
            hooked = hook_bind_keys()
        st["bind"] = {"sel": ref, "armed": False, "next": 0.0, "hooks": hooked,
                      "poll": not _hk["ok"] and len(hooked) < len(POLL_KEYS)}
        refresh_bind_button()
        API.SysMsg("Action Bar: keybind mode on: %s (Esc ends it, Backspace clears a key)." % (
            "click a cell, then press a key" if mouse_pos() is None else
            "hover a cell and press a key or combination"), Kit.HUE_INFO)


    def drop_bind():
        """Keybind mode off, its key hooks gone; returns what it was (or None)."""
        b, st["bind"] = st["bind"], None
        for combo in (b or {}).get("hooks", []):
            if not key_owner(combo):             # (2.6.84) never another module's key
                safe(lambda combo=combo: API.OnHotKey(combo))
        return b


    def end_bind():
        b = drop_bind()
        if b is None:
            return
        if b.get("hooks"):
            register_hotkeys()               # the cells' own hotkeys come back
        refresh_bind_button()
        API.SysMsg("Action Bar: keybind mode off.", Kit.HUE_INFO)


    def assign_key(ref, k):
        owner = key_owner(k)
        if owner:
            API.SysMsg("Action Bar: %s belongs to %s; pick another." % (k, owner), Kit.HUE_BAD)
            return
        changed = [ref]
        for r, c in all_cells():
            if r != ref and norm_key(c["k"]) == k:
                c["k"] = ""
                changed.append(r)
                API.SysMsg("Action Bar: %s taken off %s." % (k, ref_name(r)), Kit.HUE_INFO)
        for i, bk in enumerate(bag_keys()):
            if ("b", i) != ref and bk == k:
                set_key_of(("b", i), "")
                changed.append(("b", i))
                API.SysMsg("Action Bar: %s taken off bag slot %d." % (k, i + 1), Kit.HUE_INFO)
        set_key_of(ref, k)
        if ref[0] == "b":
            save_cells()                       # the cells may have lost the key
        register_hotkeys()
        keys_changed(changed)
        empty = ref[0] != "b" and not cell(ref)["t"]
        API.SysMsg("Action Bar: %s bound to %s%s." %
                   (k, ref_name(ref), " (empty; fill it to use it)" if empty else ""),
                   Kit.HUE_GOOD)


    def on_bind_key(combo):
        """A key (combination) pressed in keybind mode."""
        b = st["bind"]
        if not b:
            return
        k = combo.rsplit("+", 1)[-1]
        if k == "ESCAPE":
            end_bind()
            return
        ref = hovered_ref() or b["sel"]
        if ref is None:
            API.SysMsg("Action Bar: hover a cell on the bar (or click one) first.", Kit.HUE_INFO)
            return
        b["sel"] = ref
        if k in ("BACKSPACE", "DELETE"):
            set_key_of(ref, "")
            register_hotkeys()
            keys_changed([ref])
            API.SysMsg("Action Bar: %s has no hotkey now." % ref_name(ref), Kit.HUE_GOOD)
            return
        assign_key(ref, combo)


    def keys_changed(refs):
        """Hotkeys of these cells changed: their corner labels and tooltips are
        redrawn in place (one hop), and the settings page's Hotkey box follows
        if it shows one of them. No rebuild of the bar or the page."""
        def work():
            for r in refs:
                refresh_key(r)
        on_client(work)
        c = page["c"]
        if c is not None and c.get("key") is not None:
            shown = sel_ref(page["sel"])
            if shown in refs:
                safe(lambda: c["key"].SetText(cell(shown)["k"]))


    def bind_tick(now):
        """Polling fallback, only when the keys couldn't be hooked."""
        b = st["bind"]
        if not b or not b.get("poll") or now < b["next"]:
            return
        b["next"] = now + BIND_EVERY
        ctrl, shift, alt, main = keys_now()
        if not main:
            b["armed"] = True                # everything released: ready for the next key
            return
        if not b["armed"]:
            return
        b["armed"] = False
        if typing_in_chat():                 # a key typed into a field: not a binding
            return
        on_bind_key("+".join([m for m, on in (("CTRL", ctrl), ("SHIFT", shift), ("ALT", alt)) if on]
                             + [main[0]]))


    def run_ui(uid):
        d = ui_def(uid)
        if d is None:
            API.SysMsg("Action Bar: unknown window button '%s'." % uid, Kit.HUE_BAD)
            return False
        how = d[3]
        ok = True
        if how == "barsettings":
            HOST.show_settings(KEY)
        elif how == "lock":
            toggle_lock()
        elif how == "minimize":
            queue(("toggle_min",))()
        elif how == "war":
            API.SetWarMode(not bool(safe(lambda: API.Player.InWarMode, False)))
        elif how == "help":
            API.OpenHelp()
        elif how == "grimoire":
            return toggle_grimoire()
        elif how == "virtue":
            return toggle_va()
        elif how == "quests":
            if not safe(lambda: (API.OpenQuestLog(), True)[1], False):
                ok = ClientUI.game_action("RequestQuestMenu")
        elif how == "paperdoll":
            serial = int(safe(lambda: API.Player.Serial, 0) or 0)
            arg = safe(lambda: __import__("System").UInt32(serial))
            if arg is None or not ClientUI.game_action("OpenPaperdoll", [arg]):
                if on_client_thread():               # ContextMenu waits for the server:
                    later(lambda: run_ui("paperdoll"))   # on the script's thread
                else:
                    ok = safe(lambda: API.ContextMenu(API.Player, "Open Paperdoll", 2),
                              None) is not False
        elif how.startswith("mod:"):
            return toggle_module(how[4:])
        elif how.startswith("ga:"):
            parts = how.split(":")
            ok = ClientUI.game_action(parts[1], reuse=parts[2] if len(parts) > 2 else None)
        elif how.startswith("macro:"):
            ok = ClientUI.open_macro(how[6:])
        if not ok:
            API.SysMsg("Action Bar: couldn't open %s (%s)." % (d[1], ClientUI.error or "unknown"),
                       Kit.HUE_BAD)
        return ok


    # ---------- Legion scripts ----------
    _legion = {"looked": False, "type": None}


    def loaded_scripts():
        """[(name, full path)] of the scripts the client's Legion Script Manager
        has loaded, read from LegionScripting.LoadedScripts by reflection; []
        when that can't be read. The first look for the manager's type (it may
        walk every loaded assembly) is done on the script's own thread."""
        if not _legion["looked"] and on_client_thread():
            if not _legion.get("asked"):
                _legion["asked"] = True
                later(loaded_scripts)
            return []
        if not _legion["looked"]:
            _legion["looked"] = True
            names = ("LegionScripting.LegionScripting", "ClassicUO.LegionScripting.LegionScripting",
                     "ClassicUO.LegionScripting", "TazUO.LegionScripting.LegionScripting")
            _legion["type"] = next((t for t in map(Client._type, names) if t is not None), None)
            if _legion["type"] is None:
                try:
                    import System
                    _legion["type"] = next((
                        tt for asm in System.AppDomain.CurrentDomain.GetAssemblies()
                        for tt in (safe(lambda asm=asm: list(asm.GetTypes()), []) or [])
                        if tt.Name == "LegionScripting"), None)
                except Exception:
                    pass
        t = _legion["type"]
        if t is None:
            return []
        out = []

        def get(sf, n):
            return str(safe(lambda: ClientUI._get(sf, n), "") or "")
        try:
            for sf in (ClientUI._get(None, "LoadedScripts", t) or []):
                rel, path = get(sf, "RelativePath"), get(sf, "FullPath")
                rel = rel or get(sf, "FileName")
                if rel or path:
                    out.append((rel, path))      # rel is what PlayScript / ToggleScript want
        except Exception:
            pass
        return out


    _script_names = {}      # script name as typed -> (good until, the names to try)
    _names_due = set()      # names being worked out on the script's thread


    def script_names_for(v):
        """The names to try for a script. TazUO's PlayScript / ToggleScript /
        IsScriptRunning match ScriptFile.RelativePath: the path under the
        LegionScripts folder with forward slashes ("Spells/Bless.py"). So:
        the manager's own RelativePath for any loaded script with this file
        name, the relative paths of files with this name under LegionScripts
        (for cells saved as a bare "Bless.py"), then the name as typed and
        the bare file name. Worked out once every SCRIPT_NAMES_LIFE per script, since it
        walks the folder - on the script's own thread: on the client thread
        the last list is used (or, the first time, the name as typed and
        what the manager holds) while a fresh one is worked out there."""
        v = str(v or "").strip().replace("\\", "/")
        hit = _script_names.get(v)
        if hit is not None and time.time() < hit[0]:
            return list(hit[1])
        base = v.split("/")[-1]
        low, blow = v.lower(), base.lower()
        out = []

        def add(c):
            if c and c not in out:
                out.append(c)
        walk = not on_client_thread()
        if not walk:
            if v not in _names_due:
                _names_due.add(v)

                def job():
                    _names_due.discard(v)
                    script_names_for(v)
                later(job)
            if hit is not None:
                return list(hit[1])
        if "/" in v:
            add(v)
        for rel, _ in loaded_scripts():              # what the Script Manager holds
            r = rel.replace("\\", "/")
            rl = r.lower()
            if rl == low or rl.endswith("/" + low) or rl.split("/")[-1] == blow:
                add(r)
        if not walk:                                 # for now; not kept
            add(v)
            add(base)
            return list(out)
        root = legion_root()
        if root:                                     # files of that name under LegionScripts
            try:
                for d, dirs, files in os.walk(root):
                    rel = d.replace("\\", "/")[len(root):].strip("/")
                    if rel.count("/") >= 2:
                        dirs[:] = []
                    dirs[:] = [x for x in dirs if not x.startswith(".") and x.lower() not in LIB_DIRS]
                    for f in files:
                        if f.lower() == blow:
                            add((rel + "/" + f) if rel else f)
            except Exception:
                pass
        add(v)
        add(base)
        _script_names[v] = (time.time() + SCRIPT_NAMES_LIFE, out)
        return list(out)


    _run_hint = {}          # 2.6.82: script cell value -> the name that last answered running


    def script_running(v):
        """Is the script running under any of its names? 2.6.82: speed pass: the
        name that answered last time is asked first; plain try, no lambdas."""
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
        """Start a Legion script (stop it if it's running): PlayScript / StopScript
        when the API has them, else ToggleScript, under each name TazUO might
        use; the result is checked half a second later."""
        cands = script_names_for(v)
        was = script_running(v)
        fns = [getattr(API, n, None) for n in
               (("StopScript",) if was else ("PlayScript", "RunScript", "StartScript"))]
        fn = next((f for f in fns if f is not None), None) or API.ToggleScript
        done = False
        for c in cands:                       # a wrong name is ignored silently, so
            if not safe(lambda c=c: (fn(c), True)[1], False):   # try each until one takes
                continue
            done = True
            if not HOST.idle(0.1) or script_running(v) != was:
                break
        st["script_check"] = (v, was, time.time() + SCRIPT_CHECK_AFTER)
        return done


    def check_script(now):
        """SCRIPT_CHECK_AFTER after a script cell was used: did it start (or stop)?"""
        chk = st.get("script_check")
        if not chk or now < chk[2]:
            return
        st["script_check"] = None
        v, was, _ = chk
        on = script_running(v)
        name = v.replace("\\", "/").split("/")[-1]
        if was and not on:
            API.SysMsg("Action Bar: stopped %s." % name, Kit.HUE_INFO)
        elif not was and on:
            API.SysMsg("Action Bar: started %s." % name, Kit.HUE_GOOD)
        elif not was:
            API.SysMsg("Action Bar: %s didn't start; is it in the Legion Script Manager's "
                       "list (refresh it)?" % name, Kit.HUE_BAD)
            if HOST.debug:
                known = [r or p for r, p in loaded_scripts()]
                API.SysMsg("Action Bar: tried %s; the manager lists %s." %
                           (", ".join(script_names_for(v)),
                            ", ".join(known[:12]) if known else "nothing readable"), Kit.HUE_INFO)
        update_labels()


    def use_item(c):
        def first():
            return st["first"].get((c["g"], c["h"])) or (
                None if settings["hue"] else st["first_g"].get(c["g"]))
        if time.time() - st.get("counted_at", 0.0) > COUNT_EVERY:
            count_now()                          # 2.6.82: minimized (no count running) or old
            serial = first()
        else:
            serial = first()
            if not serial:
                count_now()
                serial = first()
        if not serial:
            API.SysMsg("Action Bar: no %s left." % cell_text(c), Kit.HUE_BAD)
            return False
        API.UseObject(serial)
        st["next_count"] = time.time() + RECOUNT_AFTER_USE   # recount soon
        try:
            HOST.pack_dirty()                    # 2.6.82: that recount lists the pack afresh
        except Exception:
            pass
        return True


    def harmful_cell(c, t, v):
        """A spell or item cell that harms what it is aimed at (HARMFUL_SPELLS,
        HARMFUL_ITEMS)."""
        if t == "spell":
            n = v.lower()
            # (2.6.84) a partial name too, as API.CastSpell takes one ("explo")
            return bool(n) and (n in HARMFUL_SPELLS or
                                any(s.startswith(n) for s in HARMFUL_SPELLS))
        return t == "item" and int(c.get("g") or 0) in HARMFUL_ITEMS


    def must_confirm(tok, c, t, v, now):
        """2.6.81 (shard rule R6): a harmful cell aimed at the last target, while
        that target is blue or green and you are (or may be) under the town guards, only
        warns on its first press; a second press of the same cell within
        CONFIRM_SECS goes through. True: do nothing on this press."""
        if c["tg"] != "last" or not harmful_cell(c, t, v):
            return False
        conf, st["confirm"] = st["confirm"], None
        if conf and conf[0] == tok and now <= conf[1]:
            if len(conf) > 2 and 0 <= now - conf[2] < CONFIRM_MIN:
                st["confirm"] = conf             # (2.6.84) the same click (a double-click):
                return True                      # not a confirm
            return False                         # the confirming second press
        gz = safe(lambda: HOST.guarded())          # True / False / None (not known yet)
        if gz is False:                            # an unknown zone warns too (the strict reading)
            return False
        last = int(safe(lambda: API.LastTargetSerial, 0) or 0)
        m = safe(lambda: API.FindMobile(last)) if last else None
        noto = int(safe(lambda: int(m.Notoriety), 0) or 0) if m is not None else 0
        if noto not in WARN_NOTO:
            return False
        st["confirm"] = (tok, now + CONFIRM_SECS, now)
        API.SysMsg("Action Bar: your last target is %s and you %s a guard zone; "
                   "press again to confirm, or target by hand." %
                   ("blue" if noto == 1 else "green",
                    "are in" if gz is True else "may be in"), Kit.HUE_BAD)
        return True


    def run_cell(ref):
        c = cell(ref)
        t, v = c["t"], c["v"].strip()
        if not t:
            API.SysMsg("Action Bar: %s is empty." % ref_name(ref), Kit.HUE_INFO)
            return
        now = time.time()
        tok = (ref, settings["page"])            # this cell (a page switch makes it another)
        if must_confirm(tok, c, t, v, now):      # 2.6.81: R6 guard-zone warning
            return
        # 2.6.81: a "then target" wait belongs to the cell that armed it. A press
        # of another cell drops a pending one (a stale wait must never answer
        # this cell's cursor); kinds that never raise a cursor don't arm one.
        arms = c["tg"] in ("self", "last") and t not in NO_CURSOR_KINDS
        w = st["want_target"]
        if w and now > w[1]:
            w = None
        pending_same = bool(w) and w[2] == tok
        clash = False
        if w and not pending_same:
            st["want_target"] = None
            safe(lambda: HOST.release_cursor(KEY))
            clash = arms
        ok = True
        cursor_was_up = bool(safe(lambda: API.HasTarget("any"), False))
        try:
            if t == "item":
                ok = use_item(c)
            elif t == "spell":
                API.CastSpell(v)
            elif t == "skill":
                API.UseSkill(v)
            elif t == "macro":
                r = ClientUI.run_macro(v)
                ok = bool(r)
                if r is None:
                    API.SysMsg("Action Bar: no TazUO macro named '%s'." % v, Kit.HUE_BAD)
                elif not r:
                    API.SysMsg("Action Bar: couldn't run macro '%s' (%s)." %
                               (v, ClientUI.error or "unknown"), Kit.HUE_BAD)
            elif t == "ability":
                API.ToggleAbility(v or "primary")
            elif t == "script":                 # it waits to see the script start:
                def job():                       # on the script's thread
                    try:
                        run_script(v)
                    except Exception as ex:
                        API.SysMsg("Action Bar: %s failed (%s)." % (cell_text(c), ex), Kit.HUE_BAD)
                later(job)
            elif t == "dress":
                API.Dress(v)
            elif t == "undress":
                API.Undress(v)
            elif t == "say":
                API.Msg(v)
            elif t == "ui":
                ok = run_ui(v)
            elif t == "travel":
                ok = fire_travel(c)
        except Exception as ex:
            API.SysMsg("Action Bar: %s failed (%s)." % (cell_text(c), ex), Kit.HUE_BAD)
            ok = False
        if ok and t in ("skill", "spell"):
            start_cool(t, v)                     # the cells of its kind count down
        if ok and arms and not pending_same:     # a double press keeps the first wait
            if clash:                  # another cell's wait was pending: answer neither
                API.SysMsg("Action Bar: a target was still pending; target by hand.",
                           Kit.HUE_INFO)
            elif cursor_was_up:        # someone else's cursor (Bandages, say): leave it
                API.SysMsg("Action Bar: a target cursor was already up; target by hand.",
                           Kit.HUE_INFO)
            elif safe(lambda: HOST.cursor_busy(KEY)):   # another module's flow has it
                API.SysMsg("Action Bar: another module is using the target cursor; "
                           "target by hand.", Kit.HUE_INFO)
            else:                      # ours for the wait: the others leave it alone
                # 2.6.81: a spell's cursor comes after its cast time (Kit.spell_info
                # holds the shard's, +0.5 s included), so the wait covers it
                wait = TARGET_WAIT
                if t == "spell":
                    info = safe(lambda: Kit.spell_info(v))
                    wait += info[3] if info else 0.0
                safe(lambda: HOST.claim_cursor(KEY, wait))
                st["want_target"] = (c["tg"], time.time() + wait, tok, harmful_cell(c, t, v))


    def handle_target(now):
        w = st["want_target"]
        if not w:
            return
        mode, until = w[0], w[1]                 # (mode, deadline, cell) from 2.6.81
        if now > until:
            st["want_target"] = None
            safe(lambda: HOST.release_cursor(KEY))
            return
        try:                                     # 2.6.82: plain try (every tick while waiting)
            up = API.HasTarget("any")
        except Exception:
            up = False
        if not up:
            return
        st["want_target"] = None
        safe(lambda: HOST.release_cursor(KEY))
        if safe(lambda: HOST.cursor_busy(KEY)):     # a pick took the cursor meanwhile
            return
        # (2.6.84) only a cursor of the cell's own kind: a harmful spell the player
        # casts by hand meanwhile (after a fizzle) is never aimed, nor the reverse
        # (area spells and a thrown potion raise a neutral cursor: that one is aimed)
        harm = len(w) > 3 and bool(w[3])
        if (not harm and safe(lambda: API.HasTarget("harmful"), False)) or \
                (harm and safe(lambda: API.HasTarget("beneficial"), False)):
            API.SysMsg("Action Bar: that cursor isn't this cell's; target by hand.", Kit.HUE_INFO)
            return
        if mode == "self":
            API.TargetSelf()
        else:
            last = int(safe(lambda: API.LastTargetSerial, 0) or 0)
            if last:
                API.Target(last)
            else:
                API.SysMsg("Action Bar: no last target yet; target by hand.", Kit.HUE_INFO)


    def pick(action):
        """A target cursor that holds nothing up (HOST.pick_target): the
        answer comes back as `action` + (serial,) on the bar's queue. The
        cell's own "then target" wait is dropped, so it can't answer it."""
        st["want_target"] = None
        safe(lambda: HOST.release_cursor(KEY))

        def done(serial):
            st["queue"].append(tuple(action) + (int(serial or 0),))
        HOST.pick_target(PICK_TIMEOUT, done)


    def pick_item(ref):
        API.SysMsg("Action Bar: target an item for %s (Esc to cancel)." % ref_name(ref),
                   Kit.HUE_INFO)
        pick(("picked_item", ref, settings["page"]))


    def picked_item(ref, pg, serial):
        """The item targeted for cell ref (picked while page pg showed)."""
        if st["shutting"] or HOST.aborting():
            return
        item = safe(lambda: API.FindItem(serial)) if serial else None
        if item is None:
            API.SysMsg("Action Bar: no item picked.", Kit.HUE_INFO)
            return
        gr = int(safe(lambda: item.Graphic, 0) or 0)
        hu = int(safe(lambda: item.Hue, 0) or 0)
        name = str(safe(lambda: item.Name, "") or "") or ("0x%04X" % gr)
        where = ref_name(ref)
        refs = [ref]
        if ref[0] == "a" and ref[1] >= TOP_SLOTS and pg != settings["page"] and cells["pages"]:
            # the page was switched while the cursor was up: the cell of that page
            target = cells["pages"][pg][ref[1] - TOP_SLOTS]
            where = "page %d cell %d" % (pg + 1, ref[1] - TOP_SLOTS + 1)
            refs = []                              # not on the bar now: nothing to redraw
        else:
            target = cell(ref)
        target.update({"t": "item", "v": "", "g": gr, "h": hu, "n": name})
        for k in TRAVEL_KEYS:                      # (it may have been a Travel cell)
            target.pop(k, None)
        cells_changed(recount=True, refs=refs)
        API.SysMsg("Action Bar: %s set on %s." % (name, where), Kit.HUE_GOOD)


    def pick_bag(i):
        API.SysMsg("Action Bar: target a bag for bag slot %d (Esc to cancel)." % (i + 1),
                   Kit.HUE_INFO)
        pick(("picked_bag", i))


    def picked_bag(i, serial):
        if st["shutting"] or HOST.aborting():
            return
        item = safe(lambda: API.FindItem(serial)) if serial else None
        if item is None or not safe(lambda: bool(item.IsContainer), False):
            API.SysMsg("Action Bar: that isn't a bag.", Kit.HUE_BAD)
            return
        set_picked_bag(i, serial)
        st["next_scan"] = 0.0


    def edit_in_settings(ref):
        page["sel"] = ref_sel(ref)
        HOST.show_settings(KEY)
        HOST.refresh_settings(KEY)


    def on_cell_click(ref):
        if st["bind"] is not None:           # keybind mode: clicking picks the cell
            st["bind"]["sel"] = ref
            API.SysMsg("Action Bar: %s; now press a key or combination for it." % ref_name(ref),
                       Kit.HUE_INFO)
        elif cell(ref)["t"]:
            run_cell(ref)
        elif ref[0] in ("a", "x"):
            pick_item(ref)
        else:
            open_menu(ref)


    def on_bag_click(i):
        if st["bind"] is not None:           # keybind mode: clicking picks the slot
            st["bind"]["sel"] = ("b", i)
            API.SysMsg("Action Bar: bag slot %d; now press a key or combination for it." % (i + 1),
                       Kit.HUE_INFO)
            return
        b = bag_at(i)
        if settings["bagmode"] == 1 and b is None:
            pick_bag(i)
            return
        if settings["bagmode"] == 0:
            state = ub_state()
            if state in ("collapsed", "docked"):
                ub_send("show")                   # unfold the Bags window
                heartbeat()
            elif state == "open":
                heartbeat()
                ub_send("dock")                   # fold it back into the bar
            else:                                 # Bags off: turn it on
                serial = b["s"] if b else None
                turn_on(UB_MODULE_KEY, "Bags",
                        (lambda: API.UseObject(serial)) if serial else None)
        elif b is None:
            API.SysMsg("Action Bar: no bag in that slot (see Bag slots on the Action Bar "
                       "settings page).", Kit.HUE_INFO)
        else:
            API.UseObject(b["s"])      # Bags pins it into its own slot when it opens


    # ---------- right-click menu (TazUO-style: categories, then a list) ----------
    CATS = [("item", "Item..."), ("spell", "Spell"), ("skill", "Skill"),
            ("ability", "Weapon ability"), ("ui", "Client window"), ("macro", "TazUO macro"),
            ("script", "Legion script"), ("dress", "Dress outfit"),
            ("undress", "Undress outfit"), ("say", "Say text"),
            ("travel", "Travel (runebook)")]
    MENU_CAPS = dict(CATS + [("hotkey", "Hotkey"), ("lo", "Red at")])   # the menu's titles
    LIST_CATS = ("spell", "skill", "ability", "ui", "macro", "script", "dress", "undress")
    LIST_TITLES = {"macro": "TazUO macros", "script": "Legion scripts",
                   "dress": "Dress outfits", "undress": "Dress outfits"}


    def legion_root():
        """The LegionScripts folder: the folder above this script's own folder
        (this script lives in LegionScripts/VirtueAssistant), else its folder."""
        base = str(safe(lambda: API.ScriptPath, "") or "").replace("\\", "/").rstrip("/")
        if not base:
            return ""
        if safe(lambda: os.path.isfile(base), False):
            base = os.path.dirname(base)
        parent = os.path.dirname(base)
        return parent if parent and parent != base else base


    # Folders under LegionScripts that hold Python libraries, not scripts to run
    LIB_DIRS = ("iplib", "lib", "libs", "library", "site-packages", "dlls", "stubs",
                "__pycache__", "api", "docs", "examples",
                "virtueassistantmodules")      # Virtue Assistant's own module files


    def script_names():
        """The scripts you can run, as paths under LegionScripts ("Spells/Bless.py"):
        the Legion Script Manager's own list when it can be read, else the .py
        files in the folder (three levels deep), skipping library folders such
        as iplib, packages (folders with __init__.py) and _private files."""
        root_dir = legion_root()
        rl = root_dir.lower()
        out = []
        for name, path in loaded_scripts():               # what the manager shows
            p = path.replace("\\", "/")
            rel = p[len(root_dir):].strip("/") if root_dir and p.lower().startswith(rl) else (p or name)
            parts = rel.lower().split("/")
            if any(d in LIB_DIRS for d in parts[:-1]) or parts[-1].startswith("_"):
                continue
            if rel and rel not in out:
                out.append(rel)
        if out or not root_dir:
            return sorted(out, key=lambda s: s.lower())
        try:
            for root, dirs, files in os.walk(root_dir):   # pruned as it goes
                rel = root.replace("\\", "/")[len(root_dir):].strip("/")
                if rel.count("/") >= 2 or "__init__.py" in files:
                    dirs[:] = []
                    if "__init__.py" in files:
                        continue
                dirs[:] = [d for d in dirs if not d.startswith(".") and d.lower() not in LIB_DIRS]
                for f in files:
                    if f.lower().endswith(".py") and not f.startswith("_"):
                        out.append((rel + "/" + f) if rel else f)
        except Exception:
            pass
        return sorted(out, key=lambda s: s.lower())


    def saved_list(cat):
        """What TazUO has saved for a list category."""
        if cat == "macro":
            return ClientUI.macro_names()
        if cat == "script":
            return script_names()
        return safe(ClientUI.outfit_names, []) or []          # dress / undress
    TEXT_HINT = {"macro": "The name of a macro from TazUO's macro window",
                 "script": "The script's file name (heal.py, or Spells/Bless.py)",
                 "dress": "An outfit name from TazUO's dress agent",
                 "undress": "An outfit name from TazUO's dress agent",
                 "say": "The text to say in game",
                 "hotkey": "A key or combination (F5, CTRL+Q, SHIFT+F2; blank = none)",
                 "lo": "The counter turns red at this many or fewer (0 = only when none)"}


    def _cell_rect(info):
        """Screen rect (x, y, w, h) of a cell / bag slot on the bar, or None."""
        g = win["g"]
        if not Kit.is_open(g) or info is None:
            return None
        return (int(safe(lambda: g.GetX(), 0) or 0) + info["x"],
                int(safe(lambda: g.GetY(), 0) or 0) + info["y"], info["w"], info["h"])


    def menu_place(w, h):
        """Where a w x h menu goes so all of it is on screen: just under its
        cell, or just above it when there's no room below (a bar at the bottom
        of the screen), then pushed in from any edge. A menu the player dragged
        stays where it was put, only pushed back on screen."""
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
                y = ay - 2 - h                   # no room under the cell: open above it
            x = max(0, min(x, W - w))
            y = max(0, min(y, H - h))
        return int(x), int(y)


    def close_menu():
        g, menu["g"] = menu["g"], None
        menu["c"] = {}
        Kit.dispose(g)


    def menu_disposed(g):
        def handler(*args):
            if menu["g"] is g:
                menu["g"] = None
                menu["c"] = {}
        return handler


    def open_menu(ref, bag=None):
        """The menu of a cell, or (ref None) of bag slot `bag`, opened next to it."""
        menu.update({"ref": ref, "bag": bag, "level": "cats" if ref else "bag", "cat": None,
                     "page": 0, "moved": None, "placed": None,
                     "anchor": _cell_rect(win["cells"].get(ref) if ref else win["bags"].get(bag))})
        build_menu()


    def menu_entries():
        """(caption, action) rows for the level the menu is on. Lists are paged."""
        lvl, cat = menu["level"], menu["cat"]
        if lvl == "bag":
            i = menu["bag"]
            rows = []
            if settings["bagmode"] == 1:
                rows += [("Pick a bag...", ("pickbag", i)),
                         ("Clear this slot", ("clearbag", i))]
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
        if lvl == "cats":
            c = cell(menu["ref"])
            rows = [(cap, ("cat", key)) for key, cap in CATS]
            tg = {"self": "self", "last": "last target"}.get(c["tg"], "none")
            rows += [("-", None),
                     ("Hotkey: %s" % (c["k"] or "none"), ("cat", "hotkey")),
                     ("Press a key for it", ("bindsel", None)),
                     ("Then target: %s" % tg, ("target", None))]
            if c["t"] in ("item", "travel"):         # a counter that can turn red
                rows.append(("Red at: %d or fewer" % max(0, c["lo"]), ("cat", "lo")))
            rows += [("Clear cell", ("clear", None)),
                     ("More on the settings page", ("settings", None))]
            return rows, None
        if lvl == "method":                          # a Travel cell: the way to go there
            return [(cap, ("tset", m)) for m, cap in TRAVEL_WAYS], None
        if lvl == "list":
            if cat == "spell":
                pages = [[(n, ("set", ("spell", n))) for n in names.split("|")]
                         for _, names in SPELL_SCHOOLS]
                titles = SCHOOL_NAMES
            elif cat == "skill":
                pages = [[(n, ("set", ("skill", n))) for n in SKILLS]]
                titles = ["Skills"]
            elif cat == "ability":
                pages = [[("Primary ability", ("set", ("ability", "primary"))),
                          ("Secondary ability", ("set", ("ability", "secondary")))]]
                titles = ["Weapon ability"]
            elif cat == "travel":                    # Grimoire's runebook destinations
                if HOST.services.get("grimoire.destinations") is None:
                    rows = [("Grimoire is off: click to turn it on", ("grimon", None))]
                elif not menu["items"]:
                    rows = [("No runebook read yet: open Grimoire's runebook tabs",
                             ("none", None))]
                else:
                    rows = [(fit("%s  (%s)" % (d["name"], d["book_name"]), 260), ("tdest", i))
                            for i, d in enumerate(menu["items"])]
                per = MENU_ROWS * MENU_COLS
                pages = [rows[i:i + per] for i in range(0, len(rows), per)]
                titles = ["Runebook destinations"] * len(pages)
            elif cat in LIST_TITLES:                 # saved macros / scripts / outfits
                rows = [(fit(n, 220), ("set", (cat, n))) for n in menu["items"]]
                if not rows:
                    rows = [("Nothing saved in TazUO yet", ("none", None))]
                rows.append(("Type a name", ("typed", cat)))
                per = MENU_ROWS * MENU_COLS
                pages = [rows[i:i + per] for i in range(0, len(rows), per)]
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
        """The right-click menu, drawn in one hop on the client thread."""
        if BUILD_ON_CLIENT and on_client(_build_menu_now, fallback=False) is True:
            return
        Kit.dispose(menu.pop("stale", None))
        _build_menu_now()


    def _build_menu_now():
        old = menu["g"]
        if Kit.is_open(old):                     # dragged since it was placed? keep it there
            pos = (int(safe(lambda: old.GetX(), 0) or 0), int(safe(lambda: old.GetY(), 0) or 0))
            if menu.get("placed") is not None and pos != menu["placed"]:
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
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 34, M + 4, None, "Close",
                       on_click=queue(("mpick", "close", None)))
        if lvl not in ("cats", "bag"):
            Kit.art_button(g, store, "back", Kit.ART_RESTORE, w - M - 54, M + 7, None,
                           "Back to the previous menu",
                           on_click=queue(("mpick", "back", None)))
        yb = M + 30 + GAP
        Kit.add_section(g, M, yb, IW, body_h)
        if lvl == "text":
            cur = cell(ref)
            if menu["cat"] == "lo":
                val = str(max(0, cur["lo"]))
            else:
                val = cur["k"] if menu["cat"] == "hotkey" else (cur["v"] if cur["t"] == menu["cat"]
                                                                else "")
            Kit.add_label(g, TEXT_HINT.get(menu["cat"], ""), M + 10, yb + 8, Kit.HUE_INFO)
            c["text"] = Kit.add_textbox(g, val, M + 10, yb + 32, IW - 20, numbers=False)
            Kit.art_button(g, store, "ok", Kit.ART_OK, M + 10, yb + 62, "Apply",
                           "Save this value on the cell",
                           on_click=queue(("mpick", "text", None)))
            c["status"] = Kit.add_label(g, "", M + 10 + 35 + Kit.text_w("Apply") + 12, yb + 65,
                                        Kit.HUE_INFO)
        else:
            for i, (cap, action) in enumerate(rows):
                col, row = divmod(i, nrow)
                x = M + 8 + col * col_w
                y = yb + 6 + row * MENU_ROW_H
                if action is None:                      # separator
                    Kit.add_tiled(g, Kit.STONE_TILE, x, y + MENU_ROW_H // 2, col_w - 16, 1)
                    continue
                now = action[0] == "set" and (cell(ref)["t"], cell(ref)["v"]) == action[1] \
                    or action[0] in ("tdest", "tset") and travel_now(ref, action)
                Kit.add_label(g, cap, x + 4, y + 2,     # green: what the cell holds now
                              Kit.HUE_GOOD if now else Kit.HUE_TEXT)
                Kit.catcher(g, x, y, col_w - 8, MENU_ROW_H, queue(("mpick",) + tuple(action)),
                            cap)
            if paged:
                name, p, n = paged
                py = yb + body_h - 28
                Kit.add_label(g, "%s  (%d of %d)" % (name, p + 1, n), M + 10, py + 4, Kit.HUE_INFO)
                if n > 1:
                    Kit.art_button(g, store, "next", Kit.ART_PAGE, w - M - 44, py, None,
                                   "Next page", on_click=queue(("mpick", "page", 1)))
                    Kit.art_button(g, store, "prev", Kit.ART_PAGE, w - M - 84, py, None,
                                   "Previous page", on_click=queue(("mpick", "page", -1)))
        x, y = menu_place(w, h)                  # always wholly on screen
        x, y = Kit.place(g, x, y, w, h)
        safe(lambda: setattr(g, "CanCloseWithRightClick", False))
        menu.update({"g": g, "c": c, "placed": (x, y)})
        G.AddControlOnDisposed(g, menu_disposed(g))
        G.AddGump(g)
        safe(lambda: g.SetInScreen())
        Kit.dispose(menu.pop("stale", None))
        return True


    def set_cell(ref, t, v):
        """Put t/v in the cell, keeping its hotkey, target and red-at values."""
        cur = cell(ref)
        new = blank()
        new.update({"t": t, "v": v, "k": cur["k"], "tg": cur["tg"], "lo": cur["lo"]})
        cells[ref[0]][ref[1]] = new
        cells_changed(recount=True, refs=[ref])
        API.SysMsg("Action Bar: %s set on %s." % (cell_text(new), ref_name(ref)), Kit.HUE_GOOD)


    def travel_now(ref, action):
        """Does the cell already go there (a destination row) / that way (a way row)?"""
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
            return int(c.get("rb") or "0", 16) == int(d["book"]) and c.get("ri") == str(int(d["index"]))
        except (ValueError, TypeError, KeyError):
            return False


    def menu_pick(what, arg):
        ref = menu["ref"]
        if what in ("close", "bindsel", "bagbind", "set", "settings", "pickbag", "clearbag",
                    "ub", "bag", "bagmode", "tset", "grimon") or (what, arg) == ("cat", "item"):
            close_menu()                                 # these close the menu first
        if what == "back":
            if menu["level"] == "method":                # back to the destinations
                menu.update({"level": "list", "cat": "travel"})
            else:
                menu.update({"level": "cats", "cat": None, "page": 0})
            build_menu()
        elif what == "cat" and arg == "travel":
            fn = HOST.services.get("grimoire.destinations")
            menu["items"] = list(safe(fn, []) or []) if fn is not None else []
            menu.update({"level": "list", "cat": "travel", "page": 0})
            build_menu()
        elif what == "tdest":
            items = menu["items"]
            if menu["level"] == "list" and menu["cat"] == "travel" and 0 <= arg < len(items):
                menu.update({"level": "method", "dest": items[arg]})
                build_menu()
        elif what == "tset":
            if menu.get("dest") and ref is not None:
                set_travel(ref, menu["dest"], arg)
        elif what == "grimon":
            turn_on(GRIM_MODULE_KEY, "Grimoire")
        elif what == "page":
            menu["page"] += arg
            build_menu()
        elif what == "cat" and arg == "item":
            pick_item(ref)
        elif what == "cat" and arg in LIST_TITLES and on_client_thread():
            # the saved macros / scripts / outfits are looked up on the script's
            # thread (a folder walk, a search of the client's types)
            def job():
                items = saved_list(arg)
                if menu["ref"] == ref and menu["level"] == "cats" and Kit.is_open(menu["g"]):
                    menu["items"] = items
                    menu.update({"level": "list", "cat": arg, "page": 0})
                    build_menu()
            later(job)
        elif what == "cat" and arg in LIST_CATS:
            menu["items"] = saved_list(arg) if arg in LIST_TITLES else []
            menu.update({"level": "list", "cat": arg, "page": 0})
            build_menu()
        elif what in ("cat", "typed"):                   # typed values, and the hotkey
            menu.update({"level": "text", "cat": arg})
            build_menu()
        elif what == "bindsel":
            start_bind(ref)
        elif what == "bagbind":
            start_bind(("b", arg))
        elif what == "set":
            set_cell(ref, arg[0], arg[1])
        elif what == "text":
            tb = menu["c"].get("text")
            v = str(safe(lambda: tb.Text, "") or "").strip()
            if menu["cat"] == "hotkey":
                k = norm_key(v)
                owner = key_owner(k)
                if owner:
                    Kit.set_text(menu["c"]["status"], "%s belongs to %s" % (k, owner), Kit.HUE_BAD)
                    return
                if k:
                    assign_key(ref, k)          # (2.6.84) off any other cell or bag slot too
                else:
                    cell(ref)["k"] = ""
                    cells_changed(refs=[ref])
                close_menu()
            elif menu["cat"] == "lo":                    # Red at: the counter's threshold
                try:
                    lo = int(v)
                except ValueError:
                    Kit.set_text(menu["c"]["status"], "Type a number", Kit.HUE_BAD)
                    return
                cell(ref)["lo"] = max(0, lo)
                cells_changed(refs=[ref])
                close_menu()
            elif not v:
                Kit.set_text(menu["c"]["status"], "Type a value first", Kit.HUE_BAD)
            else:
                close_menu()
                set_cell(ref, menu["cat"], v)
        elif what == "target":
            c = cell(ref)
            c["tg"] = {"": "self", "self": "last", "last": ""}.get(c["tg"], "")
            save_cells()
            want_redraw([ref])                       # its tooltip names the target
            HOST.refresh_settings(KEY)
            build_menu()
        elif what == "clear":
            clear_cell(ref)
            close_menu()
        elif what == "settings":
            edit_in_settings(ref)
        # ---- bag slots ----
        elif what == "pickbag":
            pick_bag(arg)
        elif what == "clearbag":
            set_picked_bag(arg, 0)
            st["next_scan"] = 0.0
        elif what == "ub":
            if arg == "settings":
                if UB_MODULE_KEY in HOST.by_key:         # its page of the Settings tab
                    HOST.show_settings(UB_MODULE_KEY)
            elif arg == "on":
                turn_on(UB_MODULE_KEY, "Bags")
            else:
                heartbeat()
                ub_send(arg)
        elif what == "bag":
            on_bag_click(arg)
        elif what == "bagmode":
            HOST.show_settings(KEY)


    # ---------- hotkeys ----------
    def typing_in_chat():
        """True while keys go into a text field anywhere on screen (the chat
        line, any window's text box; the host's HOST.typing), so a key pressed
        then is text, not a bar hotkey."""
        return bool(safe(HOST.typing, False))


    def hotkey_fn(ref, key=None):
        """The hotkey's callback. TazUO runs it on this script's own thread
        (from API.ProcessCallbacks), so the cell is used right here, not on
        the bar's next tick: no added delay. It is used in one hop on the
        client thread (every read in it is free there; whatever has to wait
        is handed to _thread_tick)."""
        def fn(*args):
            if typing_in_chat() or st["shutting"] or win["g"] is None:   # typing: not a hotkey
                return
            if key is not None:
                # (2.6.84) this path has no key-up: a key held down repeats, and each
                # event comes within FALLBACK_REPEAT of the last: one press, one use
                now, held = time.time(), _hk["fb"]
                at = held.get(key)
                held[key] = now
                if len(held) > 64:
                    held.clear()
                if at is not None and 0 <= now - at < FALLBACK_REPEAT:
                    return
            on_client(lambda: use_now(ref))
        return fn


    def use(ref):
        """Use a cell, or a bag slot (ref ("b", i))."""
        if ref[0] == "b":
            on_bag_click(ref[1])
        else:
            run_cell(ref)


    def use_now(ref):
        try:
            use(ref)
        except Exception as ex:
            API.SysMsg("Action Bar: %s failed (%s)." % (ref_name(ref), ex), Kit.HUE_BAD)


    # ---------- hotkeys straight from the client's key event ----------
    # TazUO's OnHotKey callbacks run on the script's thread, on its next
    # ProcessCallbacks: after the current pass of the main loop and whatever
    # tick is busy. Hooking the client's own Keyboard.KeyDownEvent instead
    # (the same event TazUO's hotkeys come from) runs the cell the moment the
    # key goes down, on the client thread, where every game call is free.
    # Anything that must not run there (scripts, turning modules on, the
    # settings window) is queued for the bar's tick as before.
    _hk = {"ok": None, "held": {}, "map": {}, "hooks": None, "fb": {}}   # held: base key -> last event time
    DIRECT_TYPES = ("item", "spell", "skill", "ability", "macro", "say", "dress", "undress",
                    "travel")
    DIRECT_UI = ("war", "help", "quests", "paperdoll", "lock", "minimize")


    def sdl_combo(k):
        """A hotkey as the client's key event spells it: "CTRL+F1" -> "CTRL+SDLK_F1"
        (the same normalising TazUO's OnHotKey does)."""
        parts, key = norm_key(k).split("+"), None
        for p in parts:
            if p and p not in ("CTRL", "SHIFT", "ALT"):
                key = p if p.startswith("SDLK_") else "SDLK_" + p
        mods = [m for m in ("CTRL", "SHIFT", "ALT") if m in parts]
        return "+".join(mods + ([key] if key else []))


    def legion_combo(sdl):
        """The client's key string as the hotkey name the bar saves: "CTRL+SDLK_F1" -> "CTRL+F1"."""
        return "+".join(p[5:] if p.startswith("SDLK_") else p for p in str(sdl).upper().split("+"))


    def direct_ok(ref):
        """Can this cell be used right inside the key event?"""
        if ref[0] == "b":
            return (st["bind"] is None and bag_at(ref[1]) is not None and
                    (settings["bagmode"] != 0 or st["ub_state"] is not None))
        c = cell(ref)
        if c["t"] == "ui":
            d = ui_def(c["v"])
            how = d[3] if d else ""
            return how in DIRECT_UI or how.startswith(("ga:", "macro:"))
        return c["t"] in DIRECT_TYPES


    def fire(ref):
        """Use a cell for its hotkey: here and now when that is safe, else on
        the bar's next tick."""
        if direct_ok(ref):
            use_now(ref)
        else:
            st["queue"].append(("use", ref))


    def _hk_down(combo):
        """Keyboard.KeyDownEvent: on the client thread, for every key."""
        try:
            if not _hk["ok"]:
                return
            combo = str(combo)
            base = combo.rsplit("+", 1)[-1]
            now, held = time.time(), _hk["held"]
            at = held.get(base)
            held[base] = now
            # auto-repeat while held. A KeyUp the client never delivered (focus
            # lost with the key down) would otherwise hold the key for ever:
            # one HELD_KEY_STALE without a repeat and the key counts as let go.
            if at is not None and now - at < HELD_KEY_STALE:
                return
            if len(held) > 32:                   # keys whose KeyUp never came
                for k in [k for k, t in held.items() if now - t >= HELD_KEY_STALE]:
                    del held[k]
            if st["shutting"] or win["g"] is None:
                return
            if st["bind"] is not None:           # keybind mode: the key is the answer
                if typing_in_chat():             # ... unless it's typed into a field
                    return
                name = base[5:] if base.startswith("SDLK_") else base
                if name in MOD_BASES:            # a modifier on its own is not a binding
                    return                       # (the combination comes with its key)
                k = legion_combo(combo)
                st["queue"].append(("bindkey", k))   # assign_key says whose key it is
                return
            ref = _hk["map"].get(combo)
            if ref is None or typing_in_chat():
                return
            fire(ref)
        except Exception:
            pass


    def _hk_up(combo):
        try:
            _hk["held"].pop(str(combo).rsplit("+", 1)[-1], None)
        except Exception:
            pass


    def _hk_install():
        """Hook the client's key events (once). False if this client won't let us."""
        if _hk["ok"] is not None:
            return _hk["ok"]
        _hk["ok"] = False
        if not DIRECT_KEYS:
            return False
        try:
            import clr
            import System
            from System.Reflection import BindingFlags
            kb = Client._type("ClassicUO.Input.Keyboard")
            if kb is None:
                raise Exception("no ClassicUO.Input.Keyboard")
            flags = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
            evd, evu = kb.GetEvent("KeyDownEvent", flags), kb.GetEvent("KeyUpEvent", flags)
            if evd is None or evu is None:
                raise Exception("no KeyDownEvent / KeyUpEvent")
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
            _hk["ok"] = False
            if HOST.debug:
                API.SysMsg("Action Bar: hotkeys go through TazUO's OnHotKey (no direct key "
                           "event: %s)." % ex, Kit.HUE_INFO)
        return _hk["ok"]


    def _hk_remove():
        hooks, _hk["hooks"] = _hk["hooks"], None
        _hk["ok"] = None if hooks else _hk["ok"]
        _hk["map"] = {}
        if not hooks:
            return
        import System
        evd, dd, evu, du = hooks
        safe(lambda: evd.GetRemoveMethod(True).Invoke(None, System.Array[object]([dd])))
        safe(lambda: evu.GetRemoveMethod(True).Invoke(None, System.Array[object]([du])))


    def unregister_hotkeys():
        for k in st["hotkeys"]:
            if not key_owner(k):                 # (2.6.84) a key another module took since: its own
                safe(lambda k=k: API.OnHotKey(k))
        st["hotkeys"] = []
        _hk["map"] = {}


    _told = set()           # (key, owner) conflicts already said this start (see _start)


    def tell_once(what, text):
        """A conflict line, once per start per key (register_hotkeys runs on every
        page switch, cell edit and settings change: it would otherwise repeat)."""
        if what not in _told:
            _told.add(what)
            API.SysMsg(text, Kit.HUE_BAD)


    def register_hotkeys():
        unregister_hotkeys()
        seen = {}
        for r, c in all_cells():
            k = norm_key(c["k"])
            if not k or not c["t"] or not shown(r):      # hidden rows stay quiet
                continue
            owner = key_owner(k)
            if owner:
                tell_once((k, owner), "Action Bar: %s belongs to %s; %s has no hotkey." %
                          (k, owner, ref_name(r)))
                continue
            if k in seen:
                tell_once((k, "two cells"), "Action Bar: %s is on two cells; %s gets it." %
                          (k, ref_name(r)))
            seen[k] = r
        for i, k in enumerate(bag_keys()):
            if k and not key_owner(k):
                seen[k] = ("b", i)
        if _hk["ok"]:                            # the client's key event does the rest
            _hk["map"] = dict((sdl_combo(k), ref) for k, ref in seen.items())
            return
        if st["bind"] is not None:               # keybind mode holds every key; end_bind
            return                               # registers the cells' hotkeys again
        for k, ref in seen.items():
            try:
                API.OnHotKey(k, hotkey_fn(ref, k))
                st["hotkeys"].append(k)
            except Exception:
                API.SysMsg("Action Bar: can't use '%s' as a hotkey." % k, Kit.HUE_BAD)


    # ---------- settings page (drawn inside the Virtue Assistant window) ----------
    def page_layout(w):
        hint = Kit.wrap("Value: a spell, skill, macro or outfit name, primary or secondary, "
                        "a script file, text to say, or an item graphic like 0x0E21 "
                        "(or 0x0E21,1153 with a hue).", w - 24)[:3]
        help_lines = [line for para in HELP for line in Kit.wrap(para, w - 24)]
        h1 = 194
        h2 = 158 + 20 * len(hint) + 10
        h3 = 30 + 20 * len(help_lines) + 10
        return {"h1": h1, "h2": h2, "h3": h3, "hint": hint, "help": help_lines,
                "total": h1 + Kit.GAP + h2 + Kit.GAP + h3}


    def config_height(w):
        return page_layout(w)["total"]


    def _int_v(v):
        """int(v), or None when v is None or no number."""
        if v is None:
            return None
        try:
            return int(v)
        except Exception:
            return None


    def dd_index(dd, default):
        # 2.6.82: speed pass: plain try, no lambdas (the method, then the field, as before)
        try:
            v = _int_v(dd.GetSelectedIndex())
        except Exception:
            v = None
        if v is None:
            try:
                v = _int_v(dd.SelectedIndex)
            except Exception:
                v = None
        return default if v is None else v


    def slider_value(s, default):
        try:
            v = _int_v(s.GetValue())
        except Exception:
            v = None
        if v is None:
            try:
                v = _int_v(s.Value)
            except Exception:
                v = None
        return default if v is None else v


    def build_config(g, x, y, w):
        """The settings page, drawn in one hop on the client thread."""
        if BUILD_ON_CLIENT and on_client(lambda: _build_config_now(g, x, y, w),
                                         fallback=False) is True:
            return
        _build_config_now(g, x, y, w)


    def _build_config_now(g, x, y, w):
        if not cells["a"]:                    # the page shown while the module is off:
            load_cells()                      # its cells are only read when it starts
        L = page_layout(w)
        c = {}
        dds = []                       # (key, x, y, w, items, index) - added last
        store = ({}, {})

        def tooltip_on(ctrl, text):
            """A tooltip on a control (built once: a lambda is fine here)."""
            safe(lambda: ctrl.SetTooltip(text))

        def slider(label, ry, sw, lo, hi, key, text, tooltip):
            """Label, slider c[key] and its value label c[key + "_lbl"]; returns the slider's x."""
            Kit.add_label(g, label, x + 12, ry + 2)
            sx = x + 12 + Kit.text_w(label) + 8
            c[key] = Kit.add_slider(g, sx, ry + 6, sw, lo, hi, settings[key])
            tooltip_on(c[key], tooltip)
            c[key + "_lbl"] = Kit.add_label(g, text, sx + sw + 10, ry + 2, Kit.HUE_INFO)
            return sx

        def buttons(by, specs):
            """A row of art buttons from the left; returns the x after them."""
            bx = x + 12
            for key, art, cap, tip in specs:
                Kit.art_button(g, store, key, art, bx, by, cap, tip)
                bx += 35 + Kit.text_w(cap) + 16
            return bx

        def drop_down(lx, ry, label, key, dw, pairs, value, tooltip):
            """Label and drop-down of pairs' captions (on value's entry); returns the next x."""
            Kit.add_label(g, label, lx, ry + 2)
            codes = [p[0] for p in pairs]
            dds.append((key, lx + Kit.text_w(label) + 8, ry, dw, [p[1] for p in pairs],
                        codes.index(value) if value in codes else 0, tooltip))
            return lx + Kit.text_w(label) + 8 + dw + 16
        # ---- bar ----
        Kit.add_section(g, x, y, w, L["h1"], "BAR")
        col = (w - 24) // 3
        checks = [("lock", "Lock in place", "Lock the bar where it is (unlocked, drag it by its stone edge)"),
                  ("top", "Show the top row", "Show the 24-cell top row above the bottom row"),
                  ("keys", "Show hotkeys", "Show each cell's hotkey in its corner"),
                  ("short", "Short counts", "Show 1200 as 1.2k on the counters"),
                  ("hue", "Count same hue only", "Count only items of the cell's own colour (hue)")]
        for i, (k, text, tip) in enumerate(checks):
            c["chk_" + k] = Kit.add_check(g, text, x + 12 + (i % 3) * col, y + 30 + (i // 3) * 26,
                                          settings[k], tip)
        found = st["ub_found"]
        state = ub_state()
        ub = ({"open": "Bags: shown", "collapsed": "Bags: folded",
               "docked": "Bags: in the bar"}.get(state) if state else
              "Bags: off" if found else
              "Bags: not found" if found is False else "Bags: not in use")
        found = found or state is not None
        c["ub"] = Kit.add_label(g, fit(ub, col - 6), x + 12 + 2 * col, y + 58,
                                Kit.HUE_GOOD if found else Kit.HUE_INFO)
        ry = y + 84
        slider("Cell size:", ry, 120, SLOT_MIN, SLOT_MAX, "slot", "%d px" % settings["slot"],
               "Side of each cell in pixels (%d-%d); icons stretch to fit" % (SLOT_MIN, SLOT_MAX))
        ddw = 170
        Kit.add_label(g, "Bag slots:", x + w - 12 - ddw - 8 - Kit.text_w("Bag slots:"), ry + 2)
        dds.append(("bagmode", x + w - 12 - ddw, ry, ddw, BAG_MODES, settings["bagmode"],
                    "Where the five bag slots get their bags: Inventory > Bags' slots, bags you "
                    "target yourself, or your backpack and the first bags in it"))
        ry2 = y + 110
        bx = buttons(ry2, (("pgprev", Kit.ART_PAGE, "Prev", "Show the previous page of the bottom-left cells"),
                           ("pgnext", Kit.ART_PAGE, "Next", "Show the next page of the bottom-left cells"),
                           ("bind", Kit.ART_PLAY, "Keybind mode",
                            "Start keybind mode: hover a cell on the bar and press the key to bind to it")))
        c["page_lbl"] = Kit.add_label(g, fit("Bar page %d of %d" %
                                             (settings["page"] + 1, PAGES), x + w - 16 - bx),
                                      bx, ry2 + 3, Kit.HUE_INFO)
        ry3 = y + 136
        slider("Scale:", ry3, 160, SCALE_MIN, SCALE_MAX, "scale", "%d%%" % settings["scale"],
               "Size of the whole bar (%d-%d%%); its text stays the client's size" %
               (SCALE_MIN, SCALE_MAX))
        ry4 = y + 162
        sx = slider("Extra rows:", ry4, 100, 0, EXTRA_ROWS, "extra", str(settings["extra"]),
                    "More rows of %d cells above the top row (0-%d); hidden rows' hotkeys "
                    "stay quiet" % (TOP_SLOTS, EXTRA_ROWS))
        anch = settings["anchor"]
        where = {"": "none (drop it near a corner or edge middle)",
                 "L": "left edge, upright", "R": "right edge, upright",
                 "T": "top edge", "B": "bottom edge", "C": "screen centre"}.get(
            anch, {"TL": "top-left", "TR": "top-right", "BL": "bottom-left",
                   "BR": "bottom-right"}.get(anch, anch) + " corner")
        Kit.add_label(g, fit("Anchor: %s" % where, x + w - 16 - (sx + 130)), sx + 130, ry4 + 2,
                      Kit.HUE_INFO)
        # ---- edit a cell ----
        y2 = y + L["h1"] + Kit.GAP
        Kit.add_section(g, x, y2, w, L["h2"], "EDIT A CELL")
        sel = page["sel"]
        ref = sel_ref(sel)
        cur = cell(ref)
        r1 = y2 + 30
        Kit.add_label(g, "Cell:", x + 12, r1 + 2)
        lx = x + 12 + Kit.text_w("Cell:") + 8
        dds.append(("sel", lx, r1, 120, sel_names(), sel,
                    "The cell to edit: top row, bottom-left cells of the page showing, "
                    "window buttons, extra rows (right-clicking a cell on the bar does the same)"))
        lx = drop_down(lx + 120 + 16, r1, "Does:", "does", 150, TYPES, cur["t"],
                       "What the cell does when clicked or its hotkey is pressed")
        drop_down(lx, r1, "Target:", "target", 100, TARGETS, cur["tg"],
                  "After using the cell, answer the target cursor with yourself or your "
                  "last target (only when no other module holds the cursor)")
        r2 = y2 + 62
        Kit.add_label(g, "Value:", x + 12, r2 + 2)
        if cur["t"] == "item":
            val = ("0x%04X" % cur["g"]) + ((",%d" % cur["h"]) if cur["h"] else "")
        elif cur["t"] == "ui":
            val = ""
        elif cur["t"] == "travel":                # (its destination is picked from its menu)
            val = travel_what(cur)
        else:
            val = cur["v"]
        vx = x + 12 + max(Kit.text_w("Value:"), Kit.text_w("Window:")) + 8
        c["value"] = Kit.add_textbox(g, val, vx, r2, x + w - 16 - vx, numbers=False)
        tooltip_on(c["value"], "The cell's value: see the hint below (a Client window cell "
                               "uses the Window list instead)")
        r3 = y2 + 94
        Kit.add_label(g, "Window:", x + 12, r3 + 2)
        ua = ui_all()
        uids = [d[0] for d in ua]
        wix = uids.index(cur["v"]) if cur["t"] == "ui" and cur["v"] in uids else 0
        dds.append(("window", vx, r3, 140, [d[1] for d in ua], wix,
                    "For a Client window cell: the client window or module window it opens"))
        lx = vx + 140 + 16
        Kit.add_label(g, "Hotkey:", lx, r3 + 2)
        c["key"] = Kit.add_textbox(g, cur["k"], lx + Kit.text_w("Hotkey:") + 8, r3, 100,
                                   numbers=False)
        tooltip_on(c["key"], TEXT_HINT["hotkey"] + "; or use Keybind mode above")
        lx = lx + Kit.text_w("Hotkey:") + 8 + 100 + 16
        Kit.add_label(g, "Red at:", lx, r3 + 2)
        c["lo"] = Kit.add_textbox(g, str(cur["lo"]), lx + Kit.text_w("Red at:") + 8, r3, 40)
        tooltip_on(c["lo"], "An item cell's counter turns red at this many or fewer (0 = only when none)")
        r4 = y2 + 126
        bx = buttons(r4, (("apply", Kit.ART_OK, "Apply", "Save this cell"),
                          ("pick", Kit.ART_PLAY, "Pick item...", "Target an item for this cell"),
                          ("clear", Kit.ART_CLOSE, "Clear", "Empty this cell")))
        c["status"] = Kit.add_label(g, "", bx, r4 + 3, Kit.HUE_INFO)
        for i, line in enumerate(L["hint"]):
            Kit.add_label(g, line, x + 12, y2 + 158 + i * 20, Kit.HUE_INFO)
        # ---- how to ----
        y3 = y2 + L["h2"] + Kit.GAP
        Kit.add_section(g, x, y3, w, L["h3"], "HOW TO USE IT")
        for i, line in enumerate(L["help"]):
            Kit.add_label(g, line, x + 12, y3 + 30 + i * 20, Kit.HUE_INFO)
        # ---- drop-downs last, lowest first so upper lists open over lower ones ----
        for key, dx, dy, dw, items, idx, tooltip in sorted(dds, key=lambda d: -d[2]):
            dd = G.CreateDropDown(dw, items, idx)
            dd.SetPos(dx, dy)
            g.Add(dd)
            tooltip_on(dd, tooltip)
            c[key] = dd
        page.update({"c": c, "store": store, "seen_sel": sel,
                     "seen_bag": settings["bagmode"], "next_read": 0.0})
        return True


    def set_status(text, hue=None):
        c = page["c"]
        if c is not None and c.get("status") is not None:
            Kit.set_text(c["status"], text, Kit.HUE_INFO if hue is None else hue)


    def apply_edit():
        c = page["c"]
        ref = sel_ref(page["sel"])
        cur = cell(ref)

        def chosen(lst, dd):
            return lst[max(0, min(len(lst) - 1, dd_index(dd, 0)))][0]
        t = chosen(TYPES, c["does"])
        v = str(safe(lambda: c["value"].Text, "") or "").strip()
        tg = chosen(TARGETS, c["target"])
        k = norm_key(safe(lambda: c["key"].Text, ""))
        owner = key_owner(k)
        if owner:
            set_status("%s belongs to %s" % (k, owner), Kit.HUE_BAD)
            return
        try:
            lo = int(str(safe(lambda: c["lo"].Text, "0") or "0"))
        except Exception:
            lo = LOW_DEFAULT
        new = blank()
        new.update({"t": t, "tg": tg, "k": k, "lo": lo})
        if t == "item":
            gh = parse_graphic(v)
            if gh is None and cur["t"] == "item" and cur["g"]:
                gh = (cur["g"], cur["h"])
            if gh is None:
                set_status("Pick an item, or type its graphic", Kit.HUE_BAD)
                return
            new.update({"g": gh[0], "h": gh[1],
                        "n": cur["n"] if (cur["g"], cur["h"]) == gh else "0x%04X" % gh[0]})
        elif t == "ui":
            new["v"] = chosen(ui_all(), c["window"])
        elif t == "ability":
            new["v"] = "secondary" if v.lower().startswith("s") else "primary"
        elif t == "travel":
            if cur["t"] != "travel":
                set_status("Pick its destination: right-click the cell, then Travel (runebook)",
                           Kit.HUE_BAD)
                return
            new["tg"] = ""                         # Grimoire answers its own cursor
            for k in ("v", "n") + TRAVEL_KEYS:
                new[k] = cur.get(k, "")
        elif t:
            if not v:
                set_status("Type a value first", Kit.HUE_BAD)
                return
            new["v"] = v
        cells[ref[0]][ref[1]] = new
        cells_changed(recount=True, refresh=False, refs=[ref])
        set_status("Saved %s" % ref_name(ref), Kit.HUE_GOOD)


    def poll_config():
        """Every pass: the page's buttons (their click handlers leave a flag,
        so this costs nothing). Every PAGE_EVERY seconds: the checkboxes,
        sliders and drop-downs, whose values have to be read from the client
        (each read waits for it), all in one hop."""
        c = page["c"]
        if c is None:
            return
        now = time.time()
        if now >= page.get("next_read", 0.0):
            page["next_read"] = now + PAGE_EVERY
            on_client(read_config)
            return
        poll_buttons(quick=True)


    def poll_buttons(quick):
        """quick: only the click handlers' flags (no client reads)."""
        c, st_ = page["c"], page["store"]
        if c is None:
            return
        def quick_clicked(key):
            hit = bool(st_[1].get(key, False))
            st_[1][key] = False
            return hit
        clicked = quick_clicked if quick else (lambda key: Kit.was_clicked(st_, key))
        for key, action in (("pgprev", ("page", -1)), ("pgnext", ("page", 1)), ("bind", ("bind",))):
            if clicked(key):
                queue(action)()
        if clicked("apply"):
            apply_edit()
        if clicked("pick"):
            queue(("pick", sel_ref(page["sel"])))()
            set_status("Target the item in game")
        if clicked("clear"):
            clear_cell(sel_ref(page["sel"]))


    def read_config():
        c = page["c"]
        if c is None:
            return
        changed = False
        for k in ("lock", "top", "keys", "short", "hue"):
            try:                                  # 2.6.82: plain try, no lambda
                v = bool(c["chk_" + k].IsChecked)
            except Exception:
                v = bool(settings[k])
            if v != settings[k]:
                settings[k] = v
                changed = True
        for k, lo, hi, fmt in (("slot", SLOT_MIN, SLOT_MAX, "%d px"),
                               ("scale", SCALE_MIN, SCALE_MAX, "%d%%"),
                               ("extra", 0, EXTRA_ROWS, "%d")):
            v = max(lo, min(hi, slider_value(c[k], settings[k])))
            if v != settings[k]:
                settings[k] = v
                Kit.set_text(c[k + "_lbl"], fmt % v)
                changed = True
        bm = dd_index(c["bagmode"], settings["bagmode"])
        if bm != page["seen_bag"] and 0 <= bm < len(BAG_MODES):
            page["seen_bag"] = bm
            settings["bagmode"] = bm
            st["bag_sig"], st["next_scan"] = None, 0.0
            changed = True
        if changed:
            save_settings()
            register_hotkeys()                    # rows shown or hidden: their hotkeys follow
            want_rebuild(SLIDER_SETTLE)           # wait for the slider to settle
        sel = dd_index(c["sel"], page["sel"])
        if sel != page["seen_sel"] and 0 <= sel < SEL_TOTAL:
            page["sel"] = sel
            HOST.refresh_settings(KEY)            # show the chosen cell's values
            return
        poll_buttons(quick=False)                 # the client's own clicked flags too


    def config_closed():
        page["c"] = None


    # ---------- module hooks ----------
    def _start():
        st.update({"shutting": False, "queue": [], "want_target": None,
                   "next_count": 0.0, "next_scan": 0.0, "rebuild_at": 0.0,
                   "bag_sig": None, "ability_sig": None, "bind": None, "jobs": [],
                   "redraw": set(),
                   "ub_job": False, "confirm": None, "ub_paths": None,
                   "cool": {"skill": 0.0, "spell": 0.0}, "cool_next": 0.0,
                   "minimized": Kit.load_min(MIN_KEY)})                  # as you left it
        _told.clear()
        _hk["held"] = {}
        fitst["scale"], fitst["vertical"] = None, None   # the layout tells the fit again
        fitst["slot"], fitst["m"], fitst["sig"] = None, None, None   # (2.6.74)
        load_settings()
        load_cells()
        # Bags' file: 2.6.81: looked at on the script's thread (ub_bags), not
        # here on the client thread; the bag slots stay blank until that first
        # look is in (one tick), then show its bags
        st["ub_last"], st["ub_pending"] = None, True
        st["counted_at"] = 0.0                # 2.6.82: counted by build_window when shown
        _pack_fn[0] = getattr(HOST, "pack_items", None)
        scan_bags()
        st["ub_state"], st["grim_state"], st["va_state"] = ub_state(), grim_state(), va_state()
        heartbeat()
        add_layout = getattr(HOST, "layout_add", None)   # the layout can slot the bar in a zone
        if add_layout is not None:
            def list_bar():
                try:
                    add_layout(KEY, bar_gump, TITLE, LAYOUT_HOOKS)   # 2.6.55: with the zone fit
                except TypeError:
                    add_layout(KEY, bar_gump, TITLE)                 # an older mother
            safe(list_bar)
        st["dock_sig"], st["tray_sig"], st["watch_next"] = dock_sig(), tray_sig(), 0.0
        st["owned_sig"] = owned_keys()        # other modules' hotkeys, as they are now
        build_window()
        st["rebuild_at"] = 0.0
        st["redraw"] = set()
        _hk_install()
        register_hotkeys()
        HOST.services["actionbar.hotkeys"] = hotkeys_service     # for Settings > Hotkeys


    # queued actions run by _tick: kind -> fn(the action's other values)
    ON_ACTION = {"click": on_cell_click, "use": use, "bag": on_bag_click, "ui": run_ui,
                 "pick": pick_item, "menu": open_menu, "mpick": menu_pick,
                 "picked_item": picked_item, "picked_bag": picked_bag,
                 "bindkey": on_bind_key, "lockbar": toggle_lock, "grid": toggle_grid}


    def _tick():
        if st["shutting"] or win["g"] is None:
            return
        if Kit.was_clicked(win["store"], "close"):
            Kit.dispose(win["g"])                    # on_disposed turns the module off
            return
        now = time.time()
        handle_target(now)
        check_script(now)
        bind_tick(now)
        watch_ub()
        arr = HOST.layout_arranging() if hasattr(HOST, "layout_arranging") else False
        if arr != win.get("arranging", False):         # (2.6.72) Arrange turned on / off elsewhere
            win["arranging"] = arr
            if win.get("lockbtn"):
                recolor(win["lockbtn"], *lock_look())
        while st["queue"]:
            action = st["queue"].pop(0)
            kind = action[0]
            if kind in ON_ACTION:
                ON_ACTION[kind](*action[1:])
            elif kind == "bagmenu":
                open_menu(None, action[1])
            elif kind == "page":
                set_page(settings["page"] + action[1])
            elif kind == "bind":
                if st["bind"] is None:
                    start_bind()
                else:
                    end_bind()
            elif kind == "dock":
                d = dict(all_docks()).get(action[1])
                if d is not None:
                    s = safe(d.get("state"))
                    if s is None:
                        if d.get("on"):
                            safe(d["on"])
                        else:                         # may load its file: script's thread
                            later(lambda k=action[1]: safe(lambda: HOST.enable(k)))
                    elif s == "open":
                        HOST.dock_to_bar(action[1])   # kept folded until shown again
                    else:
                        safe(d.get("show"))
                    st["dock_sig"], st["watch_next"] = None, 0.0
            elif kind == "traywin":
                settings["tray_open"] = not settings["tray_open"]
                save_settings()
                refresh_tray()                    # its button's tooltip and the tray window
            elif kind == "toggle_min":
                save_pos()
                st["minimized"] = not st["minimized"]
                Kit.save_min(MIN_KEY, st["minimized"])
                heartbeat()                       # bag slots hidden: no heartbeat
                want_rebuild()
            if st["shutting"] or win["g"] is None:
                return
        now = time.time()
        if now >= st["next_scan"]:
            st["next_scan"] = now + SCAN_EVERY
            scan_bags()
            scan_abilities()
            heartbeat()
            if st.get("last_pos") != st.get("pos_saved"):
                save_pos()                    # 2.6.82: only when the bar's look saw it move
        if st["rebuild_at"] and now >= st["rebuild_at"]:
            st["rebuild_at"] = 0.0
            st["redraw"] = set()                  # the new bar draws every cell
            build_window()
        elif st["redraw"]:
            redraw_now()                          # a few cells, in place
        if now >= st["next_count"]:
            st["next_count"] = now + COUNT_EVERY
            refresh_counts()                  # one hop; the pack is only read for item cells
        cool_tick(now)                        # a skill / spell countdown, while one runs
        if now >= st.get("tray_next", 0.0):
            st["tray_next"] = now + TRAY_EVERY
            watch_position(now)               # tray follows; anchors are read when let go


    def _thread_tick():
        """On the script's own thread, right after each tick: the jobs the
        tick (or a click, a hotkey, a target cursor) handed over - work that
        waits or reads the disk. Nothing to do: returns at once."""
        while st["jobs"] and not st["shutting"]:
            st["jobs"].pop(0)()


    def _stop():
        st["shutting"] = True
        if HOST.services.get("actionbar.hotkeys") is hotkeys_service:
            HOST.services.pop("actionbar.hotkeys", None)
        drop_layout = getattr(HOST, "layout_remove", None)
        if drop_layout is not None:
            safe(lambda: drop_layout(KEY))
        st["want_target"] = None
        safe(lambda: HOST.release_cursor(KEY))
        g, tray["g"] = tray["g"], None
        Kit.dispose(g)
        drop_bind()
        close_menu()
        heartbeat(False)                  # Bags, Grimoire and the gear come back
        unregister_hotkeys()
        _hk_remove()
        try:                                  # 2.6.82: the place read in one client hop
            on_client(save_pos)
        except Exception:
            safe(save_pos)
        Kit.save_min(MIN_KEY, st["minimized"])
        save_settings()
        save_cells()
        g, win["g"] = win["g"], None
        Kit.dispose(g)
        for s in win.pop("stale", []):
            Kit.dispose(s)


    load_settings()
    MODULE = {"start": _start, "tick": _tick, "stop": _stop,
              "interval": lambda: 0.05,
              # 2.6.82: the script-thread pass only when a job is queued (later())
              "thread_wanted": lambda: bool(st["jobs"]),
              # the tick runs on the client thread, batched with the other
              # modules' (it never waits); waits and disk reads go to thread_tick
              "client_tick": True, "thread_tick": _thread_tick,
              "config_height": config_height, "build_config": build_config,
              "poll_config": poll_config, "config_closed": config_closed}
    # ============================= MODULE END ====================================
    return MODULE


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("actionbar", "Action Bar",
             "A bar of cells for items, spells, skills, macros and windows",
             _module_actionbar, 0.05,
             category="On screen")
else:
    import API
    API.SysMsg("Action Bar is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
