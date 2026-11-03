# =============================================================================
#  Grimoire  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by Virtue Assistant from LegionScripts/VirtueAssistantModules.
#  Virtue Assistant provides everything this file uses (API, G, safe, Client,
#  Kit, HOST, the main loop and the settings window), so run that instead and
#  tick Grimoire on its Modules tab.
#
#  To leave this module out, take this file out of the folder.
#  Module key: "grimoire"   (saved settings carry over unchanged)
# =============================================================================


def _module_grimoire():
    """Builds the module in its own namespace and returns its hooks."""
    # ==============================================================================
    #  MODULE: Grimoire  (from Grimoire v2.3)  -  Unified Spell & Rune Book
    #
    #  Tabs:
    #    * Spellbook  - one page per circle. Each row: icon, name, description.
    #                   Double-click a row to cast the spell.
    #    * Runebooks  - one tab per runebook in your backpack (or in a bag inside
    #                   it that you have opened) or in either hand. Finding them
    #                   only looks at what you carry; no item is ever used.
    #                   Destinations are a table: names down the page (a second
    #                   column when the window is wide), the travel methods as
    #                   column headings with an arrow button per row. Double-click
    #                   a name to travel there. Each page shows its charges.
    #                   The star left of a name adds it to Favourites. A book
    #                   under LOW_CHARGES charges shows its tab in red.
    #    * Favourites - first of the runebook tabs: a "Last" row (the last trip,
    #                   by the same method) and the starred destinations. Type
    #                   in its search box to list every destination of every
    #                   runebook you carry whose rune or book name matches.
    #                   Double-click a row to travel there.
    #    Every tab's page is drawn once and kept, so switching tabs is instant.
    #    * Supplies   - panel on the right with your reagent, Recall scroll and
    #                   Gate Travel scroll totals (always visible, kept live).
    #                   A spell you lack a reagent or the mana for is dimmed.
    #
    #  Other modules (the Action Bar's Travel cells) travel through
    #  HOST.services["grimoire.travel"] and list the destinations with
    #  HOST.services["grimoire.destinations"] while Grimoire is on.
    #
    #  Runebook lists (and your known spells) are saved per character, so they
    #  show instantly next time. "Refresh" re-reads everything; "Re-read" on a
    #  book's page re-reads just that book.
    #
    #  Drag a corner to resize; the small arrow minimizes, "Settings" opens the
    #  background opacity and window scale on the Virtue Assistant Settings tab,
    #  X (or right-click) turns Grimoire off.
    # ==============================================================================

    # ------------------------------------------------------------------------------
    #  Settings - tweak these if your shard does things differently
    # ------------------------------------------------------------------------------

    BUILD = "2.5"                          # printed in the journal when the module starts
    SPELLBOOK_GRAPHICS = [0x0EFA]          # Magery spellbook
    RUNEBOOK_GRAPHICS  = [0x22C5]          # Runebook (add custom graphics if needed)

    # Server gump ID of the runebook gump. 0x554B87F3 is the RunUO/ServUO default.
    # If your shard uses a custom one, the script detects it automatically and
    # prints it in your system messages so you can paste it here.
    RUNEBOOK_GUMP_ID = 0x554B87F3

    # Runebook button layout (RunUO/ServUO standard): button = 2 + slot*6 + type
    TRAVEL_TYPES = {
        "charge": 0,   # Recall using one of the book's charges
        "recall": 3,   # Cast Recall (uses your reagents/mana)
        "gate":   4,   # Cast Gate Travel
        "sacred": 5,   # Cast Sacred Journey (RunUO's AoS layout; UNCHECKED IN GAME - only
                       # other modules ask for it, through HOST.services["grimoire.travel"])
    }
    DEFAULT_TRAVEL = "recall"              # What a double-click on a destination does
    SET_DEFAULT_TYPE = 2                   # runebook button type that makes a rune the book's default
    # Every way to travel other modules may ask for (HOST.services["grimoire.travel"])
    TRAVEL_METHODS = ("recall", "gate", "charge", "recall_scroll", "gate_scroll", "sacred")
    TRAVEL_SPELL = {"recall": "Recall", "gate": "Gate Travel", "sacred": "Sacred Journey"}
    LOW_CHARGES = 3                        # a runebook with fewer charges shows its tab in red
    #                                        and raises one alert each time it drops under this
    SEARCH_MAX = 40                        # most destinations the Favourites page lists at once
    FAVS_MAX = SEARCH_MAX                  # most starred destinations per character (all listed)
    SEARCH_EVERY = 0.15                    # seconds between looks at the search box (page shown)
    TRIP_GAP = 2.0                         # the travel service takes no new trip this soon after
    #                                        one started (a double key press is one trip)
    MANA_EVERY = 0.5                       # seconds between looks at your mana (spell page shown)
    STAR_ON, STAR_OFF = "#F0C040", "#6A6A6A"   # a starred / plain destination's star
    # The star (no star among the client's gump art): (x, y, w, h) boxes in a 14 x 14 square
    STAR_RECTS = ((6, 0, 2, 4), (0, 4, 14, 2), (3, 6, 8, 3), (2, 9, 3, 3), (9, 9, 3, 3))
    TAB_FAVS = 1                           # the Favourites tab, as saved in Grimoire_Tab
    #                                        (a runebook tab saves its serial, the spellbook 0)

    # Scrolls used by the "Recall scroll" / "Gate scroll" columns
    RECALL_SCROLL = 0x1F4C
    GATE_SCROLL   = 0x1F60
    SCROLL_CAST_TIMEOUT = 12               # seconds to wait for a scroll's cast to finish
    RUNE_CAST_CLAIM = 5                    # seconds the cursor is kept for a pre-targeted Recall/Gate cast
    # 2.6.81: the server's lines that mean a cast failed (lower case; matched only in
    # the server's lines and your own): a double-click cast's cursor claim and a
    # trip's pre-target end at once on one (check the shard's exact words in game)
    # ("already casting" is left out here: it is about an earlier spell, whose own
    # cursor is still to come and stays spoken for; a trip counts it, below)
    CAST_FAIL_TEXTS = ("fizzles", "not yet recovered", "more reagents",
                       "insufficient mana", "concentration is disturbed")
    PEARL_SPELLS = ("Recall", "Gate Travel")   # use Black Pearl (a rune-bag trip watches it)

    # Finding runebooks never uses (double-clicks) anything: the scan only LOOKS at
    # what the client already knows is in your pack and hands, and keeps the items
    # that are runebooks. Nothing else - keys, boards, pouches, bags - is touched.
    # Runebooks inside a bag show up once you have opened that bag yourself.
    OPEN_BAGS          = False
    # Only if OPEN_BAGS is turned on: the ONLY containers the scan may open, by
    # graphic (plain backpacks and bags). Anything not listed is never used.
    BAG_GRAPHICS       = [0x0E75, 0x0E76, 0x0E77, 0x0E78, 0x09B2]
    USE_DELAY          = 0.55              # server's delay between double-clicks

    HIDE_RUNEBOOK_GUMP = True              # Read/use runebooks without showing their gump
    PREBUILD_EVERY     = 0.4               # seconds between pages drawn quietly in the background
    CAST_CLAIM         = 5.0               # seconds the cursor is spoken for after a double-click cast
    # 2.6.81: spells that raise no target cursor (pre-AoS RunUO): their cast speaks
    # for no cursor. Blade Spirits and Energy Vortex take a place, so they aren't here.
    NO_TARGET_SPELLS = frozenset(["Reactive Armor", "Protection", "Magic Reflection", "Incognito",
                                  "Create Food", "Earthquake", "Summon Creature", "Air Elemental",
                                  "Earth Elemental", "Fire Elemental", "Water Elemental",
                                  "Summon Daemon"])
    TRAVEL_DEFER       = 3.0               # (2.6.84) a trip pressed while a runebook job ran is dropped after this
    CAST_DEFER         = 1.5               # a cast waits this long for another module's cursor, then is dropped
    #                                        (2.6.81: also the longest a press may wait behind a runebook job)
    CAST_HOLD          = 4.0               # no background runebook reads this long after a cast
    TRAVEL_HOLD        = 6.0               # ... and after a recall / gate (let it finish first)
    COUNT_EVERY        = 1.5               # seconds between supply recounts / looks at your hands
    RESIZE_SETTLE      = 0.3               # redraw (and save the size) this long after the last resize step
    SCALE_SETTLE       = 0.4               # apply the scale slider this long after it stopped moving
    SPELL_ICON_BASE    = 0x08C0            # Classic small magery icons (Clumsy = 0x08C0)

    # Look & feel
    DEFAULT_W, DEFAULT_H = 920, 950        # fits a whole circle (8 spells) without scrolling
    MIN_W, MIN_H         = 700, 220
    SIDE_W               = 160             # supplies panel on the right
    SCALE_MIN, SCALE_MAX = 60, 150         # window scale range in percent (set on the Settings tab)
    TITLE_H              = 54              # height of the title bar (all that shows when minimized)

    # Action Bar link: its Grimoire button shows this window and folds it
    # back "into the bar" (minimized and hidden), as does the gold arrow
    # beside Minimize. Minimize itself only folds the window to its title
    # strip, which stays on screen. Two shared vars, so it works whether
    # the Action Bar is merged or runs as its own script. If the bar stops
    # (or is minimized) the title strip is back once its heartbeat goes
    # stale (HOST.bar_alive), and folds in again when the bar returns (the
    # wish is kept by Virtue Assistant under DOCK_KEY until the window is
    # shown again).
    LINK_CMD = "Grimoire_cmd"          # Action Bar -> here: "show" / "dock"
    LINK_STATE = "Grimoire_state"      # here -> Action Bar: open / minimized / docked / off
    DOCK_KEY = "grimoire"              # the fold-into-the-bar wish, kept by the host
    DEFAULT_OPACITY      = 95              # background opacity, 0-100 (set on the Settings tab)
    SPELL_ICON           = 66              # spell icon size (44 x 1.5)

    # Native look: the shared stone frame with black sections (see Kit in
    # Virtue Assistant), the standard gump buttons and the spellbook's circle tabs.
    # If the art can't be loaded it falls back to flat colours.
    USE_GUMP_ART = True
    USE_UO_FONT  = True                    # client font for short text (descriptions stay smooth)
    ART_FRAME    = Kit.WINDOW_BG           # stone frame of the crafting gump
    GEM          = Kit.ART_PLAY[0]         # arrow button (tabs, row buttons)
    GEM_ON       = Kit.ART_PLAY[1]         # arrow button, pressed (the open tab)
    CIRCLE_ART   = 0x08B1                  # spellbook circle tabs (1st circle = 0x08B1)

    # Text colours. Each maps to a client hue for text drawn in the UO font.
    STONE_TEXT  = "#ECECEC"
    STONE_GOLD  = "#E8C84A"
    STONE_DIM   = "#9C9C9C"
    COL_HEAD    = STONE_GOLD  # headings
    COL_TEXT    = STONE_TEXT
    COL_DIM     = STONE_DIM
    COL_MUTED   = "#6E6E6E"
    COL_EMPTY   = "#E04848"   # count of zero / unavailable
    COL_ROW     = "#C8B070"   # row highlight
    ROW_A, ROW_SEL = 0.05, 0.20
    TEXT_HUES = {STONE_TEXT: Kit.HUE_TEXT, STONE_GOLD: Kit.HUE_TITLE, STONE_DIM: Kit.HUE_INFO,
                 COL_MUTED: Kit.HUE_INFO, COL_EMPTY: Kit.HUE_BAD}
    # Flat fallbacks (if the gump art isn't available)
    COL_BG      = "#17110C"
    COL_BORDER  = "#6A6A6A"
    COL_PARCH   = "#101010"
    COL_GOLD    = STONE_GOLD

    gump = None                 # the window (made in _start)

    # ------------------------------------------------------------------------------
    #  Spell data (T2A-era Magery). Order = spellbook order, which also sets the icon.
    # ------------------------------------------------------------------------------

    CIRCLES = [
        ("First Circle", [
            ("Clumsy",          "Lowers the target's Dexterity for a time.",                  "BM NS"),
            ("Create Food",     "Conjures a random piece of food into your pack.",            "GA GI MR"),
            ("Feeblemind",      "Lowers the target's Intelligence for a time.",               "NS GI"),
            ("Heal",            "Restores a small amount of the target's health.",            "GA GI SS"),
            ("Magic Arrow",     "Strikes the target with a minor bolt of magic.",             "SA"),
            ("Night Sight",     "Lets the target see clearly in darkness.",                   "SS SA"),
            ("Reactive Armor",  "Wards you with armor that soaks up melee damage.",           "GA SS SA"),
            ("Weaken",          "Lowers the target's Strength for a time.",                   "GA NS"),
        ]),
        ("Second Circle", [
            ("Agility",         "Raises the target's Dexterity for a time.",                  "BM MR"),
            ("Cunning",         "Raises the target's Intelligence for a time.",               "NS MR"),
            ("Cure",            "Attempts to neutralize poison in the target.",               "GA GI"),
            ("Harm",            "Damages the target; strongest at close range.",              "NS SS"),
            ("Magic Trap",      "Traps a container to explode when opened.",                  "GA SS SA"),
            ("Magic Untrap",    "Disarms a magical trap on a container.",                     "BM SA"),
            ("Protection",      "Temporarily raises your armor rating.",                      "GA GI SA"),
            ("Strength",        "Raises the target's Strength for a time.",                   "MR NS"),
        ]),
        ("Third Circle", [
            ("Bless",           "Raises the target's Strength, Dexterity and Intelligence.",  "GA MR"),
            ("Fireball",        "Hurls a ball of fire at the target.",                        "BP"),
            ("Magic Lock",      "Magically seals a container shut.",                          "BM GA SA"),
            ("Poison",          "Poisons the target.",                                        "NS"),
            ("Telekinesis",     "Uses or opens an object from a distance.",                   "BM MR"),
            ("Teleport",        "Instantly moves you to a visible location.",                 "BM MR"),
            ("Unlock",          "Opens a magically locked container.",                        "BM SA"),
            ("Wall of Stone",   "Raises a temporary wall of stone.",                          "BM GA"),
        ]),
        ("Fourth Circle", [
            ("Arch Cure",       "Cures poison in the target and those nearby.",               "GA GI MR"),
            ("Arch Protection", "Raises the armor rating of everyone around you.",            "GA GI MR SA"),
            ("Curse",           "Lowers the target's Strength, Dexterity and Intelligence.",  "GA NS SA"),
            ("Fire Field",      "Creates a wall of flame that burns those who cross it.",     "BP SS SA"),
            ("Greater Heal",    "Restores a large amount of the target's health.",            "GA GI MR SS"),
            ("Lightning",       "Calls a bolt of lightning down on the target.",              "MR SA"),
            ("Mana Drain",      "Drains mana from the target.",                               "BP MR SS"),
            ("Recall",          "Teleports you to the location marked on a rune.",            "BP BM MR"),
        ]),
        ("Fifth Circle", [
            ("Blade Spirits",   "Summons whirling blades that attack nearby creatures.",      "BP MR NS"),
            ("Dispel Field",    "Destroys a magical field.",                                  "BP GA SS SA"),
            ("Incognito",       "Disguises your appearance and name for a time.",             "BM GA NS"),
            ("Magic Reflection","Turns harmful spells back upon their caster.",               "GA MR SS"),
            ("Mind Blast",      "Damages the target based on your superior intellect.",       "BP MR NS SA"),
            ("Paralyze",        "Freezes the target in place for a time.",                    "GA MR SS"),
            ("Poison Field",    "Creates a wall of poisonous gas.",                           "BP NS SS"),
            ("Summon Creature", "Summons a random creature to fight for you.",                "BM MR SS"),
        ]),
        ("Sixth Circle", [
            ("Dispel",          "Banishes a summoned creature.",                              "GA MR SA"),
            ("Energy Bolt",     "Strikes the target with a powerful bolt of energy.",         "BP NS"),
            ("Explosion",       "Engulfs the target in a fiery explosion.",                   "BM MR"),
            ("Invisibility",    "Makes the target invisible for a time.",                     "BM NS"),
            ("Mark",            "Marks a recall rune with your current location.",            "BP BM MR"),
            ("Mass Curse",      "Curses everyone in an area.",                                "GA MR NS SA"),
            ("Paralyze Field",  "Creates a wall that paralyzes those who touch it.",          "BP GI SS"),
            ("Reveal",          "Reveals hidden creatures and players nearby.",               "BM SA"),
        ]),
        ("Seventh Circle", [
            ("Chain Lightning", "Lightning strikes everyone around the target.",              "BP BM MR SA"),
            ("Energy Field",    "Creates an impassable wall of energy.",                      "BP MR SS SA"),
            ("Flamestrike",     "Engulfs the target in a column of fire.",                    "SS SA"),
            ("Gate Travel",     "Opens a moongate to a rune's location that others can use.", "BP MR SA"),
            ("Mana Vampire",    "Steals the target's mana and gives it to you.",              "BP BM MR SS"),
            ("Mass Dispel",     "Banishes all summoned creatures in an area.",                "BP GA MR SA"),
            ("Meteor Swarm",    "Rains fire on everyone around the target.",                  "BM MR SS SA"),
            ("Polymorph",       "Transforms you into another creature.",                      "BM MR SS"),
        ]),
        ("Eighth Circle", [
            ("Earthquake",      "Shakes the ground, damaging everyone around you.",           "BM GI MR SA"),
            ("Energy Vortex",   "Summons a vortex of energy that attacks your foes.",         "BP BM MR NS"),
            ("Resurrection",    "Brings a ghost back to life.",                               "BM GI GA"),
            ("Air Elemental",   "Summons an air elemental to serve you.",                     "BM MR SS"),
            ("Summon Daemon",   "Summons a daemon to serve you.",                             "BM MR SS SA"),
            ("Earth Elemental", "Summons an earth elemental to serve you.",                   "BM MR SS"),
            ("Fire Elemental",  "Summons a fire elemental to serve you.",                     "BM MR SS SA"),
            ("Water Elemental", "Summons a water elemental to serve you.",                    "BM MR SS"),
        ]),
    ]
    # Reagent abbreviation -> (full name, item graphic)
    REAGENTS = {
        "BP": ("Black Pearl",   0x0F7A),
        "BM": ("Blood Moss",    0x0F7B),
        "GA": ("Garlic",        0x0F84),
        "GI": ("Ginseng",       0x0F85),
        "MR": ("Mandrake Root", 0x0F86),
        "NS": ("Nightshade",    0x0F88),
        "SA": ("Sulfurous Ash", 0x0F8C),
        "SS": ("Spider's Silk", 0x0F8D),
    }
    REAGENT_ORDER = ["BP", "BM", "GA", "GI", "MR", "NS", "SA", "SS"]
    # Runebook pages: a table. Destinations fill the page top to bottom (then a
    # second column if the window is wide enough); the travel methods are column
    # headings once, with just the arrow button in each row. Smooth font throughout.
    RUNE_NAME_FILL  = 0.72        # destination name text height as a share of the row height
    RUNE_NAME_MIN_SZ = 16         # ...but never smaller than this
    RUNE_HEAD_SIZE  = 16          # column headings, the "N destinations" line
    RUNE_TITLE_SIZE = 24          # the book's name at the top of its page
    RUNE_ROW_MIN    = 36          # rows stretch between these to fill the page...
    RUNE_ROW_MAX    = 54          # ...and scroll once they can't
    RUNE_NAME_MIN   = 200         # least room for a name before a second column is used
    RUNE_METHODS = [              # (method, heading, tooltip)
        ("charge",        "Charge",        "Recall using one of the book's charges"),
        ("recall",        "Recall",        "Cast Recall on this rune"),
        ("gate",          "Gate",          "Cast Gate Travel to this rune"),
        ("recall_scroll", "Recall scroll", "Read a Recall scroll on this rune"),
        ("gate_scroll",   "Gate scroll",   "Read a Gate Travel scroll on this rune"),
    ]
    REG_SLOT = 86        # width of each reagent column
    REG_PIC  = 60        # reagent picture size (2x)
    SPELL_ROW_H = 100    # height of one spell row

    ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]

    # ------------------------------------------------------------------------------
    #  State
    # ------------------------------------------------------------------------------

    state = {
        "tab": "spells",        # "spells" or a runebook serial
        "circle": 0,
        "dirty": True,          # content needs rebuilding
        "closed": False,
        "queue": [],            # actions to run from the main loop
        "status": "",
        "minimized": False,
        "switch": None,         # tab or ("spells", circle) clicked, waiting to be shown
        "content_top": 0,       # y where the tab pages start
    }
    spellbook_serial = 0
    known_spells = None         # set of normalized names, or None if unknown (show all)
    runebooks = []              # [{"serial", "title"}]
    rune_cache = {}             # serial -> list of (name, slot) or None if unreadable
    book_charges = {}           # serial -> (charges, max charges); either may be None
    bg_reads = []               # runebook serials to (re)read quietly when nothing else is going on
    bg = {"hold": 0.0}          # no background reads before this time (after casting / travelling)
    gump_id = RUNEBOOK_GUMP_ID
    # The runebook lists' version: bumped whenever a list, a charge count, the
    # books carried, the favourites or the last trip change, so the Favourites
    # page and the destinations service redo their work only then.
    lists = {"ver": 0, "dest_ver": -1, "dests": []}
    # Favourites (stars) and the last trip, per character, in the saved file:
    # "favs_<player>" = "v1;book|index|name;..." and "last_<player>" =
    # "v1;book|index|name|method". index = the rune's place in the book's list
    # as Grimoire shows it; the name moves the star when a re-read moves runes.
    favs = {"list": [],         # [[book serial, index, name], ...]
            "keys": set(),      # (book serial, index) of each, for the stars
            "last": None,       # (book serial, index, name, method) of the last trip
            "owner": None,      # the player serial they were loaded for
            "save": False,      # the favourites changed: written by the next thread tick
            "save_last": False}
    # The Favourites page: its search box, an info line and a pool of rows,
    # reassigned in place as you type (see fav_render).
    fav_ui = {"layer": None, "tb": None, "info": None, "sa": None, "pool": [], "text": "",
              "seen": None, "ver": -1, "next": 0.0, "row_w": 0, "name_w": 0}
    # Low charges (GR3): the charge count each book had when last looked at,
    # and the books whose count came in since (handled on the client tick).
    charge_seen = {}
    charge_news = []

    # The window is drawn in layers, each a list of its controls:
    #   frame   - background, title bar, tabs, supplies panel, status line
    #   pages   - one per tab (and one per spell circle); built once and then just
    #             shown/hidden when you switch tabs or circles
    def new_layer(hidden=False):
        return {"ctrls": [],     # every control (for disposing)
                "tops": [],      # the ones placed straight on the window (for showing/hiding)
                "counts": [],    # [graphic, label, last_text] for live supply counts
                "spells": [],    # a spell page's rows, dimmed in place (see refresh_castable)
                "stars": {},     # a runebook page's stars by rune index (recolor_star)
                "hidden": hidden}


    frame = new_layer()
    pages = {}                  # page key (see page_key) -> layer
    tgt = frame                 # the layer being built
    row_bgs = {}
    tab_marks = {}              # tab key -> its highlight box
    tab_parts = {}              # runebook tab key -> (its label, its click boxes), recoloured in place
    click_state = {"key": None, "t": 0.0, "selected": None}


    def norm(s):
        s = re.sub(r"[^a-z]", "", (s or "").lower())
        return s.replace("summon", "") if "elemental" in s else s


    # ------------------------------------------------------------------------------
    #  Finding books
    # ------------------------------------------------------------------------------

    _pack = {"t": 0.0, "items": []}


    def items_in_pack(fresh=False):
        """Everything in the backpack (sub-bags too). Reuses one scan for half a second,
        since a single redraw asks for it several times."""
        now = time.time()
        fn = _pack_fn[0]
        if fn is not None:
            # 2.6.82: speed pass: the host's shared listing (one per pass for every
            # module; a list up to half a second old is reused, as before)
            try:
                return fn(deep=True, max_age=0.0 if fresh else 0.5) or []
            except Exception:
                return []
        if fresh or now - _pack["t"] > 0.5:
            _pack["items"] = safe(lambda: list(API.ItemsInContainer(API.Backpack, True) or []), [])
            _pack["t"] = now
        return _pack["items"]


    _pack_fn = [getattr(HOST, "pack_items", None)]


    HAND_LAYERS = (("OneHanded", "TwoHanded"), ("onehanded", "twohanded"))   # spellings clients answer
    _hands = {"layers": None}      # the spelling pair this client answered, remembered the first time


    def held_items():
        """Whatever you have equipped, hands first. Asks by hand layer and also lists
        the items worn on your character, in case the client answers only one way.
        The layer spelling that answered once is the only one asked from then on
        (before: four spellings on every look, every COUNT_EVERY seconds)."""
        out = []
        pairs = (_hands["layers"],) if _hands["layers"] else HAND_LAYERS
        for pair in pairs:
            for layer in pair:
                try:
                    it = API.FindLayer(layer)
                except Exception:
                    it = None
                if it:
                    out.append(it)
                    _hands["layers"] = pair
        try:
            out += list(API.ItemsInContainer(API.Player.Serial, False) or [])
        except Exception:
            pass
        seen, items = set(), []
        try:
            pack = API.Backpack
        except Exception:
            pack = None
        for it in out:
            if not it:
                continue
            s = it.Serial                       # 2.6.82: read once
            if s not in seen and s != pack:
                seen.add(s)
                items.append(it)
        return items


    # ---- Runebook types you've taught the script by targeting one ("Add runebook...") ----
    # Stored per character as "graphic:hue,graphic:hue". Needed on shards where
    # runebooks use the same art as spellbooks (just hued) or custom art.

    def load_rb_types():
        raw = API.GetPersistentVar("Grimoire_RunebookTypes", "", API.PersistentVar.Char) or ""
        types = set()
        for part in raw.split(","):
            try:
                g, h = part.split(":")
                types.add((int(g, 16), int(h, 16)))
            except ValueError:
                pass
        return types


    def save_rb_types(types):
        API.SavePersistentVar("Grimoire_RunebookTypes",
                              ",".join("%X:%X" % t for t in sorted(types)), API.PersistentVar.Char)


    rb_types = load_rb_types()     # reloaded by reset_state: a character switch keeps nothing stale


    # Runebooks seen by name this session, as (graphic, hue): an equipped book often
    # has no name yet, so one that looks like these counts as a runebook too.
    rb_seen = set()
    RUNEBOOK_HUE = 0x0461                  # default runebook hue (older runebooks share the spellbook art)


    def is_runebook(it):
        g, h = it.Graphic, it.Hue
        if (g, h) in rb_types:
            return True
        return is_runebook_v(g, h, it.Name)


    def is_runebook_v(g, h, name):
        """is_runebook from values already read (2.6.82: each read once)."""
        if (g, h) in rb_types:
            return True
        name = (name or "").lower()
        if "rune" in name and "book" in name:
            return True
        if "spellbook" in name:
            return False
        if g in SPELLBOOK_GRAPHICS and h == RUNEBOOK_HUE:
            return True
        return g in RUNEBOOK_GRAPHICS and g not in SPELLBOOK_GRAPHICS


    def is_spellbook(it):
        return it.Graphic in SPELLBOOK_GRAPHICS and not is_runebook(it)


    def find_spellbook():
        books = [it for it in held_items() + items_in_pack() if is_spellbook(it)]
        # Prefer a book the client knows has spells in it
        if hasattr(API, "GetSpellsInSpellbook"):
            for b in books:
                if safe(lambda: len(list(API.GetSpellsInSpellbook(b.Serial) or [])) > 0, False):
                    return b.Serial
        return books[0].Serial if books else 0


    _uim = {"looked": False, "prop": None}     # the client's UIManager.Gumps, found once


    def close_spellbook_window(serial):
        """The spellbook window is drawn by the client itself (not a server gump), so
        CloseGump can't reach it: find it in the client's gump list and close it.
        Called on the client thread (Kit.on_client), where its windows live."""
        closed = False
        try:
            if not _uim["looked"]:
                _uim["looked"] = True
                import System
                from System.Reflection import BindingFlags
                flags = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
                # the client's own assembly (the one API lives in) first; every
                # loaded assembly only if that fails
                t = safe(lambda: API.GetType().Assembly.GetType("ClassicUO.Game.Managers.UIManager"))
                if t is None:
                    for asm in System.AppDomain.CurrentDomain.GetAssemblies():
                        t = safe(lambda: asm.GetType("ClassicUO.Game.Managers.UIManager"))
                        if t is not None:
                            break
                if t is not None:
                    _uim["prop"] = t.GetProperty("Gumps", flags)
            if _uim["prop"] is None:
                return False
            gumps = _uim["prop"].GetValue(None, None)
            for g in list(gumps):
                try:
                    if g.LocalSerial == serial and "Spellbook" in g.GetType().Name and not g.IsDisposed:
                        g.Dispose()
                        closed = True
                except Exception:
                    pass
        except Exception:
            pass
        return closed


    def spells_key():
        try:
            return "spells_%08X" % int(API.Player.Serial)
        except Exception:
            return "spells"


    def load_known_spells(force=False):
        """Returns a set of normalized spell names in the book, or None if unknown.
        Uses what the client already knows, then the saved list; only opens the book
        (and closes it again) when neither is available or on a forced refresh.
        Waits: only ever run from the thread job (scan_all), never from the tick."""
        if not spellbook_serial or not hasattr(API, "GetSpellsInSpellbook"):
            return None
        names = list(API.GetSpellsInSpellbook(spellbook_serial) or [])
        if not names and not force:
            cached = set(n for n in load_value(spells_key()).split(",") if n)   # the saved list
            if cached:
                return cached
        if not names:
            # The client only knows a book's contents after it has been opened once.
            API.UseObject(spellbook_serial)
            deadline = time.time() + 2.0
            while time.time() < deadline and HOST.idle(0.05):
                names = list(API.GetSpellsInSpellbook(spellbook_serial) or [])
                if names:
                    break
            # The window can show up a moment after the contents; keep trying briefly.
            deadline = time.time() + 1.0
            while time.time() < deadline and not HOST.aborting():
                if Kit.on_client(lambda: close_spellbook_window(spellbook_serial)):
                    break
                HOST.idle(0.05)
        if not names:
            return None
        known = set(norm(n) for n in names)
        save_value(spells_key(), ",".join(sorted(known)))
        return known


    SUPPLY_GRAPHICS = set([g for _, g in REAGENTS.values()] + [RECALL_SCROLL, GATE_SCROLL])


    def supply_counts():
        """Total of each reagent and travel scroll carried in your backpack (including sub-bags)."""
        items = items_in_pack()
        # 2.6.82: speed pass: Graphic read once per item; within one client pass
        # the same listing is counted once (page builds of one rebuild share it)
        memo = None
        if getattr(HOST, "in_hop", False):
            # (2.6.83) keyed on the pass and the count: the pack list is a new
            # copy on every call, so the list itself never matched
            memo = (HOST.pass_id, len(items))
            if _supply["key"] == memo:
                return dict(_supply["totals"])
        totals = dict((g, 0) for g in SUPPLY_GRAPHICS)
        for it in items:
            g = it.Graphic
            if g in totals:
                totals[g] += max(1, it.Amount or 0)
        if memo is not None:
            _supply.update({"key": memo, "totals": dict(totals)})
        return totals


    _supply = {"key": None, "totals": None}


    def count_text(n):
        return "{:,}".format(n)


    def count_entry(graphic, lbl, n, owned=True):
        """A live supply count: [graphic, label, text shown, hue with some, hue
        with none]. The hues are None when the label isn't in the UO font (its
        colour can't be changed in place; running out redraws instead)."""
        if not USE_UO_FONT:
            return [graphic, lbl, count_text(n), None, None]
        if not owned:
            return [graphic, lbl, count_text(n), TEXT_HUES[COL_MUTED], TEXT_HUES[COL_MUTED]]
        return [graphic, lbl, count_text(n), TEXT_HUES[COL_TEXT], TEXT_HUES[COL_EMPTY]]


    def set_label_hue(lbl, hue):
        try:
            lbl.Hue = hue
            return True
        except Exception:
            return False


    def scroll_flags(totals):
        """What a runebook page shows of your travel scrolls: some or none of each."""
        return (totals.get(RECALL_SCROLL, 0) > 0, totals.get(GATE_SCROLL, 0) > 0)


    def refresh_counts():
        if not frame["counts"]:
            for pg in pages.values():            # 2.6.82: plain loop, no generator
                if pg["counts"]:
                    break
            else:
                return
        # 2.6.82: the host's shared listing, up to half a second old (every
        # COUNT_EVERY anyway; the amounts are read live), so the Action Bar's
        # count and this one list the pack once between them
        if _pack_fn[0] is None:
            items_in_pack(fresh=True)             # an older mother: as before
        totals = supply_counts()
        changed = totals != loop["totals"]   # nothing cast, looted or restocked: labels stand
        loop["totals"] = totals
        entries = (frame["counts"] + [e for pg in pages.values() for e in pg["counts"]]) \
            if changed else []
        for entry in entries:
            graphic, lbl, last = entry[0], entry[1], entry[2]
            n = totals.get(graphic, 0)
            text = count_text(n)
            if text == last:
                continue
            if (n == 0) != (last == "0"):
                # ran out / restocked: the count turns red / back. Only the label
                # changes colour (before: the whole window and every page were
                # redrawn, a long frame right as the last reagent was cast)
                if entry[3] is None or not set_label_hue(lbl, entry[3] if n else entry[4]):
                    state["dirty"] = True         # can't recolour it here: redraw
            set_label_text(lbl, text)
            entry[2] = text
        if changed:
            refresh_castable()                    # a reagent ran out / came back: dim rows follow
        # A runebook page shades its scroll buttons and headings by whether you
        # carry any scrolls: a page drawn with other ones is drawn again (the open
        # one now, the hidden ones by prebuild_next).
        flags = scroll_flags(totals)
        shown = page_key(state["tab"])            # 2.6.82: once, not per page
        for key, pg in list(pages.items()):
            if pg.get("scrolls") is not None and pg["scrolls"] != flags and not state["dirty"]:
                if key == shown:
                    build_page(key, False)
                else:
                    clear(pages.pop(key)["ctrls"])


    def open_unopened_bags():
        """Only when OPEN_BAGS is on: open the plain bags (BAG_GRAPHICS) in the backpack
        that the client hasn't seen inside yet, then close them again. Nothing that is
        not a plain bag is ever used."""
        tried = set()
        last_use = 0.0

        def unopened():
            return [it.Serial for it in items_in_pack(fresh=True)
                    if it.Graphic in BAG_GRAPHICS                # strict whitelist: bags only
                    and it.IsContainer and not it.Opened and it.Serial not in tried]

        def bag_open(serial):
            bag = API.FindItem(serial)
            return bool(bag and bag.Opened)

        def close_bag(serial):
            try:
                it = API.FindItem(serial)
                g = it.GetContainerGump() if it else None
                if g:
                    g.Dispose()
            except Exception:
                pass

        for _ in range(6):                                   # bags inside bags inside bags...
            todo = Kit.on_client(unopened)                   # one hop for the whole look
            if not todo:
                break
            for serial in todo:
                tried.add(serial)
                wait = last_use + USE_DELAY - time.time()    # respect the server's use delay
                if wait > 0 and not HOST.idle(wait):
                    return
                API.UseObject(serial)
                last_use = time.time()
                deadline = last_use + 1.5
                while time.time() < deadline and HOST.idle(0.05):
                    if Kit.on_client(lambda: bag_open(serial)):
                        break
                Kit.on_client(lambda: close_bag(serial))


    BOOKISH = set([0x0EFA, 0x22C5, 0x0FEF, 0x0FF0, 0x0FF1, 0x0FF2, 0x0FF3, 0x0FF4,
                   0x0FBD, 0x0FBE, 0x1C11, 0x1C13, 0x2252, 0x2253, 0x238C, 0x23A0, 0x2D50])


    def report_books():
        """Print every book-like item you carry so a mis-detected runebook can be spotted."""
        books = [it for it in held_items() + items_in_pack() if it.Graphic in BOOKISH or "book" in (it.Name or "").lower()]
        if not books:
            API.SysMsg("Grimoire: no books found in your backpack or hands.", Kit.HUE_BAD)
            return
        API.SysMsg("Grimoire: books you carry (graphic / hue / name / kind):", Kit.HUE_INFO)
        for it in books:
            kind = "runebook" if is_runebook(it) else ("spellbook" if is_spellbook(it) else "?")
            API.SysMsg("Grimoire: 0x%04X / 0x%04X / %s (%s)."
                       % (it.Graphic, it.Hue, it.Name or "no name", kind), Kit.HUE_INFO)


    def register_runebook():
        """Ask the player to target a runebook. The cursor doesn't hold anything up:
        the answer comes back as a ("registered", serial) action, handled first."""
        API.SysMsg("Grimoire: target one of your runebooks.", Kit.HUE_INFO)
        token = object()
        state["pick"] = token                    # no quiet book reads while the cursor is up

        def done(serial):
            if state["pick"] is not token:       # a newer "Add runebook..." (or a restart) took over
                return
            state["pick"] = None
            state["queue"].insert(0, ("registered", serial))
        HOST.pick_target(15, done)


    def registered(serial):
        """The runebook the player targeted: remember its graphic + hue."""
        if not serial:
            API.SysMsg("Grimoire: cancelled.", Kit.HUE_INFO)
            return False
        it = API.FindItem(serial)
        if not it:
            API.SysMsg("Grimoire: that isn't an item.", Kit.HUE_BAD)
            return False
        rb_types.add((it.Graphic, it.Hue))
        save_rb_types(rb_types)
        API.SysMsg("Grimoire: runebooks are graphic 0x%04X, hue 0x%04X; saved." % (it.Graphic, it.Hue),
                   Kit.HUE_GOOD)
        return True


    def _book_vals(items):
        """[(serial, graphic, hue, name, is_runebook)] of items, each read once
        (2.6.82: speed pass; before, up to 15 reads per item per scan)."""
        out = []
        for it in items:
            try:
                g, h, n = it.Graphic, it.Hue, it.Name
            except Exception:
                continue
            out.append((it.Serial, g, h, n, is_runebook_v(g, h, n)))
        return out


    def find_runebooks():
        found, seen_titles = [], {}
        pack = _book_vals(items_in_pack(fresh=True))
        for s, g, h, n, rb in pack:
            if rb and n:
                rb_seen.add((g, h))
        got = set()                               # 2.6.82: the serials found (was a scan)
        for s, g, h, n, rb in _book_vals(held_items()) + pack:
            book = rb or (not n and (g, h) in rb_seen)
            if not book or int(s) in got:
                continue
            got.add(int(s))
            title = (n or "").strip() or "Runebook"
            title = title[:1].upper() + title[1:]
            seen_titles[title] = seen_titles.get(title, 0) + 1
            if seen_titles[title] > 1:
                title = "%s %d" % (title, seen_titles[title])
            # a plain int: the same key whether it came from the client (a .NET
            # number), the saved favourites or another module's service call
            found.append({"serial": int(s), "title": title})
        return found


    # ------------------------------------------------------------------------------
    #  Reading runebook gumps
    # ------------------------------------------------------------------------------

    # The PacketGumpText parser lives in the mother (Kit.gump_parse, Kit.gump_is_cmd,
    # Kit.gump_is_int, Kit.strip_html; shared with the Social module), so a fix lands
    # once. Only what builds on it stays here.
    def file_lines(raw):
        """Lines of a text, dropping carriage returns / NULs (the saved file, dumps)."""
        return str(raw or "").replace("\r", "").replace("\x00", "").split("\n")


    def parser_selftest():
        """Tiny checks recorded in the dump so a failure says exactly which step broke.
        Only run when a dump is written (it used to run on every read)."""
        out = {}
        try:
            out["is_cmd"] = Kit.gump_is_cmd("croppedtext 305 60 115 17 81 17")
            out["text_is_text"] = not Kit.gump_is_cmd("Page 2 Boss")
            lines, cmds = Kit.gump_parse("Shame Bankpage 0")
            out["split_merged"] = (lines, cmds)
            out["lines"] = len(Kit.gump_parse("a\nb\nc\npage 0")[0])
        except Exception as ex:
            out["error"] = str(ex)
        return out


    JUNK_TEXT = re.compile(
        r"^(empty|\(indescript\)|charges?:?|max charges:?|rename( book)?|drop rune|set default|"
        r"recall.*|gate travel.*|sacred journey.*|use charge.*|next|prev(ious)?|okay|cancel|"
        r"felucca|trammel|ilshenar|malas|tokuno)$", re.I)
    COORDS = re.compile(r"\d+\s*[o\u00b0]\s*\d+'?\s*[NSEW]", re.I)


    TEXT_ARG = {"croppedtext": (7, 6), "text": (5, 4), "htmlgump": (6, 5)}   # cmd -> (min tokens, text index)


    def gump_elements(raw):
        """Pull labels and reply buttons (with their page and position) out of PacketGumpText."""
        lines, cmds = Kit.gump_parse(raw)
        page, buttons, labels = 0, [], []
        for t in cmds:
            try:
                k = t[0].lower()
                if k == "page":
                    page = int(t[1])
                elif k == "button" and len(t) >= 8:
                    if int(t[5]) == 1:                       # reply buttons only (not page flips)
                        buttons.append((page, int(t[1]), int(t[2]), int(t[7])))
                elif k in TEXT_ARG and len(t) >= TEXT_ARG[k][0]:
                    labels.append((page, int(t[1]), int(t[2]), Kit.strip_html(lines[int(t[TEXT_ARG[k][1]])])))
            except (ValueError, IndexError):
                continue
        return lines, buttons, labels


    def looks_like_destination(text):
        t = text.strip()
        if not t or JUNK_TEXT.match(t) or COORDS.search(t):
            return False
        return not re.match(r"^[\d\s/:.,-]+$", t)       # plain numbers (charges etc.)


    parse_stats = {}            # what the parser saw last time (written into the dump file)


    def extract_destinations(raw):
        """Returns [{"name", "slot", "button"}] sorted by name.

        1) Standard RunUO/ServUO layout: the index page has a 'use' button 2 + slot*6
           beside each rune name.
        2) Anything else: pair every label with the reply button next to it and take
           the page that has the most such pairs (that's the index page).
        """
        lines, cmds = Kit.gump_parse(raw)
        parse_stats.clear()
        parse_stats.update({"text_lines": len(lines), "commands": len(cmds)})
        if cmds:
            parse_stats["last_command"] = " ".join(cmds[-1])
        else:
            tail = file_lines(raw)
            parse_stats["last_line_repr"] = repr(tail[-2] if len(tail) > 1 else tail[-1])

        # 0) Standard layout, read in order: each 'use' button (2 + slot*6) is
        #    immediately followed by its rune's label. No geometry, no regex.
        seen, pending = {}, None
        for t in cmds:
            try:
                k = t[0].lower()
                if k == "button" and len(t) >= 8 and t[5] == "1":
                    bid = int(t[7])
                    pending = bid if bid >= 2 and (bid - 2) % 6 == 0 else None
                elif k in ("croppedtext", "text") and pending is not None:
                    name = Kit.strip_html(lines[int(t[-1])])
                    slot = (pending - 2) // 6
                    if slot not in seen:
                        seen[slot] = (name, pending)
                    pending = None
                else:
                    pending = None
            except Exception as ex:
                parse_stats["error"] = str(ex)
                pending = None
        parse_stats["sequential_pairs"] = len(seen)
        dests = [{"name": n, "slot": sl, "button": bid} for sl, (n, bid) in seen.items()
                 if n and n.lower() != "empty"]
        if dests:
            return sorted(dests, key=lambda d: d["name"].lower())

        lines, buttons, labels = gump_elements(raw)
        parse_stats.update({"buttons": len(buttons), "labels": len(labels)})

        def pair(btns):
            """button id -> (label text, page) for the label sitting right beside each button.
            The nearest label wins even if it's junk (e.g. "Empty"), so an empty slot never
            borrows a name from the next column."""
            out = {}
            for (bp, bx, by, bid) in sorted(btns):
                if bid in out:
                    continue
                best = None
                for (lp, lx, ly, text) in labels:
                    dx, dy = lx - bx, abs(ly - by)
                    if lp != bp or dy > 12 or dx == 0:
                        continue
                    if 0 < dx <= 60:
                        score = dx
                    elif -150 <= dx < 0:
                        score = 100 - dx          # left side only if nothing on the right
                    else:
                        continue
                    if best is None or score < best[0]:
                        best = (score, text, bp)
                if best and looks_like_destination(best[1]):
                    out[bid] = (best[1], best[2])
            return out

        # 1) standard layout
        std = pair([b for b in buttons if b[3] >= 2 and (b[3] - 2) % 6 == 0])
        dests = []
        for bid, (name, _) in std.items():
            slot = (bid - 2) // 6
            if not any(d["slot"] == slot for d in dests):
                dests.append({"name": name, "slot": slot, "button": bid})

        # 2) generic fallback
        if not dests:
            paired = pair(buttons)
            by_page = {}
            for bid, (name, pg) in paired.items():
                by_page.setdefault(pg, []).append((name, bid))
            if by_page:
                best_page = max(sorted(by_page), key=lambda pg: len(by_page[pg]))
                for name, bid in by_page[best_page]:
                    dests.append({"name": name, "slot": None, "button": bid})

        return sorted(dests, key=lambda d: d["name"].lower())


    CLILOC_CHARGES, CLILOC_MAX_CHARGES = 1011296, 1011297     # "Charges:", "Max Charges:"
    CHARGES_TEXT = re.compile(r"^(max(imum)?\s*)?charges?\s*:?\s*(\d+)?\s*(/\s*(\d+))?$", re.I)


    def extract_charges(raw):
        """(charges, max charges) from the runebook gump; either is None if not shown.
        Standard books print a localized "Charges:" / "Max Charges:" label, each followed
        by its number. Plain-text labels ("Charges: 5", "Charges: 5/10") work too."""
        lines, cmds = Kit.gump_parse(raw)
        found, want, nums = {}, None, []
        page = 0
        for t in cmds:
            try:
                k = t[0].lower()
                if k == "page":
                    page = int(t[1])
                    continue
                if k in ("xmfhtmlgump", "xmfhtmlgumpcolor", "xmfhtmltok") and len(t) >= 6:
                    cl = int(t[5])
                    if cl == CLILOC_CHARGES:
                        want = "cur"
                    elif cl == CLILOC_MAX_CHARGES:
                        want = "max"
                    continue
                if k not in TEXT_ARG or len(t) < TEXT_ARG[k][0]:
                    continue
                x, y, text = int(t[1]), int(t[2]), lines[int(t[TEXT_ARG[k][1]])]
            except (ValueError, IndexError):
                continue
            text = Kit.strip_html(text)
            if Kit.gump_is_int(text):
                if want and want not in found:
                    found[want] = int(text)
                    want = None
                else:
                    nums.append((page, x, y, int(text)))
                continue
            m = CHARGES_TEXT.match(text)
            if m:
                key = "max" if m.group(1) else "cur"
                if m.group(3):
                    found.setdefault(key, int(m.group(3)))
                    if m.group(5):
                        found.setdefault("max", int(m.group(5)))
                else:
                    want = key
        if not found and len(nums) >= 2:
            # Unlabelled: two numbers side by side on the same line (charges, then max).
            (p1, x1, y1, a), (p2, x2, y2, b) = nums[0], nums[1]
            if p1 == p2 and abs(y1 - y2) <= 4 and x2 > x1 and a <= b:
                found = {"cur": a, "max": b}
        return found.get("cur"), found.get("max")


    # ---- Saved runebook lists ----
    # Kept in LegionScripts/Grimoire_saved.txt (one "key<TAB>value" line each), with a
    # hex-encoded copy in a persistent var as a backup. Book values look like
    # "v1;charges;max;name|slot|button|rune;..." with | ; % tab and newline escaped in names.

    def esc(s):
        return (str(s).replace("%", "%25").replace("|", "%7C").replace(";", "%3B")
                .replace("\t", "%09").replace("\n", "%0A").replace("\r", ""))


    def unesc(s):
        return (s.replace("%0A", "\n").replace("%09", "\t").replace("%3B", ";")
                .replace("%7C", "|").replace("%25", "%"))


    def hex_encode(s):
        return "".join(["%04X" % ord(ch) for ch in s])


    def hex_decode(h):
        try:
            return "".join([chr(int(h[i:i + 4], 16)) for i in range(0, len(h) - 3, 4)])
        except ValueError:
            return ""


    def opt_int(s):
        return int(s) if Kit.gump_is_int(s) else None


    _folder = {"path": None}     # LegionScripts, found once


    def data_path(filename):
        """A file in LegionScripts next to TazUO, via .NET so it works under IronPython.
        The folder is found once (it was looked up again on every save)."""
        try:
            import System
            folder = _folder["path"]
            if folder is None:
                base = System.AppDomain.CurrentDomain.BaseDirectory
                folder = System.IO.Path.Combine(base, "LegionScripts")
                if not System.IO.Directory.Exists(folder):
                    folder = base
                _folder["path"] = folder
            return System.IO.Path.Combine(folder, filename)
        except Exception:
            return filename


    def write_file(path, text):
        """.NET first (IronPython), plain open() as the fallback; raises the fallback's error."""
        try:
            import System
            System.IO.File.WriteAllText(path, text)
        except Exception:
            f = open(path, "w")
            f.write(text)
            f.close()


    SAVE_FILE = "Grimoire_saved.txt"
    saved = {"data": None, "warned": False,
             "dirty": set()}     # 2.6.82: keys changed since the file was last written


    def saved_data():
        if saved["data"] is None:
            saved["data"] = {}
            text = ""
            path = data_path(SAVE_FILE)
            try:
                import System
                if System.IO.File.Exists(path):
                    text = System.IO.File.ReadAllText(path)
            except Exception:
                try:
                    f = open(path, "r")
                    text = f.read()
                    f.close()
                except Exception:
                    text = ""
            for line in file_lines(text):
                if "\t" in line:
                    k, v = line.split("\t", 1)
                    saved["data"][k] = v
        return saved["data"]


    def save_value(key, value):
        """2.6.82: speed pass: kept here and written once at the end of the
        thread tick (flush_saved; a Refresh of N books was N whole-file writes)."""
        data = saved_data()
        if data.get(key) == value:
            return
        data[key] = value
        saved["dirty"].add(key)


    def flush_saved():
        """Write the file once for every value saved since the last write."""
        if not saved["dirty"]:
            return
        keys, saved["dirty"] = saved["dirty"], set()
        data = saved_data()
        text = "\n".join([k + "\t" + data[k] for k in sorted(data)]) + "\n"
        path = data_path(SAVE_FILE)
        ok = False
        try:
            write_file(path, text)
            ok = True
        except Exception as ex:
            if not saved["warned"]:
                API.SysMsg("Grimoire: couldn't save to %s (%s)." % (path, ex), Kit.HUE_BAD)
                saved["warned"] = True
        if ok:
            return                # the file holds it; the hex copy is only the fallback
        # The file couldn't be written: keep a hex-encoded copy in a persistent var
        # (4x the size of the text, so it is no longer rewritten on every save).
        for key in sorted(keys):
            try:
                API.SavePersistentVar("Grimoire_H_" + key, hex_encode(data[key]),
                                      API.PersistentVar.Char)
            except Exception:
                if not saved["warned"]:
                    API.SysMsg("Grimoire: couldn't save the runebook lists; they are read "
                               "again next time.", Kit.HUE_BAD)
                    saved["warned"] = True


    def load_value(key):
        v = saved_data().get(key)
        if v:
            return v
        h = Kit.get_var("Grimoire_H_" + key)
        return hex_decode(h) if h else ""


    def book_key(serial):
        return "book_%08X" % int(serial)


    def opt_str(v):
        return "" if v is None else str(v)


    def save_book(serial):
        dests = rune_cache.get(serial)
        if dests is None:
            return
        cur, mx = book_charges.get(serial, (None, None))
        parts = ["v1", opt_str(cur), opt_str(mx)]
        parts += ["|".join([esc(d["name"]), opt_str(d["slot"]), opt_str(d["button"]),
                            str(d.get("rune") or "")]) for d in dests]
        save_value(book_key(serial), ";".join(parts))


    def load_book(serial):
        """Put a saved list into rune_cache. Returns True if there was one."""
        parts = load_value(book_key(serial)).split(";")
        if len(parts) < 3 or parts[0] != "v1":
            return False
        dests = []
        for p in parts[3:]:
            f = p.split("|")
            if len(f) != 4:
                continue
            d = {"name": unesc(f[0]), "slot": opt_int(f[1]), "button": opt_int(f[2])}
            if opt_int(f[3]):
                d["rune"] = opt_int(f[3])
            dests.append(d)
        rune_cache[serial] = dests
        book_charges[serial] = (opt_int(parts[1]), opt_int(parts[2]))
        return True


    def store_book(serial, dests, charges):
        """Record a fresh read. Returns True if anything changed."""
        old = (rune_cache.get(serial, "none"), book_charges.get(serial))
        if rune_cache.get(serial) and (dests is None or (not dests and serial in rune_errors)):
            return False            # a failed re-read never hides a list we already have
        rune_cache[serial] = dests
        if charges is not None:
            book_charges[serial] = charges
            charge_news.append(serial)           # low charges: looked at on the client tick
        if dests is not None:
            save_book(serial)
        changed = old != (rune_cache.get(serial), book_charges.get(serial))
        if changed:
            rekey_favs(serial)                   # a star stays on its rune's name
            lists["ver"] += 1
        return changed


    # ---- Favourites and the last trip (GR2), per character, in the saved file ----
    def player_key():
        try:
            return "%08X" % int(API.Player.Serial)
        except Exception:
            return None


    def resolve(serial, index, name=None, taken=None):
        """The place in a book's list of the rune at `index`, or of the rune
        named `name` when the one at `index` is named otherwise (the book was
        re-read and its runes moved; index -1: a rune that had left the book).
        Places in `taken` are skipped (two runes of one name). None if the
        book or the rune is unknown."""
        lst = rune_cache.get(serial)
        if not lst:
            return None
        n = len(lst)
        if 0 <= index < n and (name is None or lst[index]["name"] == name) \
                and (taken is None or index not in taken):
            return index
        if name is None:
            return None
        best = None
        for i in range(n):                       # the same name nearest to where it was
            if lst[i]["name"] == name and (taken is None or i not in taken) \
                    and (best is None or abs(i - index) < abs(best - index)):
                best = i
        return best


    def fav_keys_now():
        """The stars' keys again ((book, index) of each favourite whose rune is
        in its book), and no destination starred twice."""
        keys, seen, lst = set(), set(), []
        for f in favs["list"]:
            k = (f[0], f[1]) if f[1] >= 0 else (f[0], -1, f[2])
            if k in seen:
                continue
            seen.add(k)
            lst.append(f)
            if f[1] >= 0:
                keys.add(k)
        if len(lst) != len(favs["list"]):
            favs["list"] = lst
            favs["save"] = True
        favs["keys"] = keys


    def rekey_favs(serial):
        """A book's list changed: each favourite (and the last trip) in it
        follows its rune's name to the rune's new place. A rune no longer in
        the book keeps its star for when it comes back (it isn't listed)."""
        moved = False
        taken = set()                            # each favourite claims its own rune
        mine = sorted([f for f in favs["list"] if f[0] == serial],
                      key=lambda f: (f[1] < 0, f[1]))
        for f in mine:
            i = resolve(serial, f[1], f[2], taken)
            if i is None:                        # gone from the book: -1 marks no row, and
                if f[1] != -1:                   # the name finds it if it comes back
                    f[1] = -1
                    moved = True
                continue
            taken.add(i)
            if i != f[1]:
                f[1] = i
                moved = True
        if moved:
            fav_keys_now()
            favs["save"] = True
        last = favs["last"]
        if last is not None and last[0] == serial:
            i = resolve(serial, last[1], last[2])
            if i is not None and i != last[1]:
                favs["last"] = (serial, i, last[2], last[3])
                favs["save_last"] = True


    def load_favs():
        """The favourites and last trip of the character playing (thread job:
        reads the player serial). Loaded once per character."""
        who = player_key()
        if who is None or who == favs["owner"]:
            return
        if favs["save"] or favs["save_last"]:
            save_favs()                      # the last character's change, written first
        lst = []
        parts = load_value("favs_" + who).split(";")
        if parts and parts[0] == "v1":
            for p in parts[1:]:
                f = p.split("|")
                if len(f) != 3:
                    continue
                try:
                    lst.append([int(f[0], 16), int(f[1]), unesc(f[2])])
                except ValueError:
                    continue
        last = None
        parts = load_value("last_" + who).split(";")
        if len(parts) == 2 and parts[0] == "v1":
            f = parts[1].split("|")
            try:
                if len(f) == 4 and f[3] in TRAVEL_METHODS:
                    last = (int(f[0], 16), int(f[1]), unesc(f[2]), f[3])
            except ValueError:
                last = None
        favs.update({"list": lst[:FAVS_MAX], "last": last, "owner": who,
                     "save": False, "save_last": False})
        fav_keys_now()
        lists["ver"] += 1


    def save_favs():
        """Write what changed (a thread job, and at stop): a disk write never
        happens on the client tick."""
        who = favs["owner"]
        if who is None:
            favs["save"] = favs["save_last"] = False
            return
        if favs["save"]:
            favs["save"] = False
            save_value("favs_" + who, ";".join(["v1"] + ["%08X|%d|%s" % (f[0], f[1], esc(f[2]))
                                                         for f in list(favs["list"])]))
        if favs["save_last"]:
            favs["save_last"] = False
            last = favs["last"]
            if last is not None:
                save_value("last_" + who, "v1;%08X|%d|%s|%s" % (last[0], last[1], esc(last[2]),
                                                                 last[3]))


    def toggle_fav(serial, index, name):
        """The star of a destination: on (added to Favourites) or off again."""
        key = (serial, index)
        if key in favs["keys"]:
            favs["list"] = [f for f in favs["list"] if (f[0], f[1]) != key]
            on = False
        else:
            if len(favs["list"]) >= FAVS_MAX:
                API.SysMsg("Grimoire: Favourites is full (%d); take a star off first." % FAVS_MAX,
                           Kit.HUE_BAD)
                return
            favs["list"].append([serial, index, name])
            on = True
        fav_keys_now()
        favs["save"] = True
        lists["ver"] += 1
        return on


    def note_trip(serial, dest, method):
        """The trip that is starting becomes the "Last" row (thread job)."""
        lst = rune_cache.get(serial) or []
        idx = None
        for i in range(len(lst)):
            if lst[i] is dest:
                idx = i
                break
        if idx is None:
            idx = resolve(serial, 0, dest.get("name"))
        if idx is None:
            return
        favs["last"] = (serial, idx, dest.get("name") or "", method)
        favs["save_last"] = True
        lists["ver"] += 1


    rune_errors = {}           # runebook serial -> why it couldn't be read (shown in its tab)


    DUMP_FILE = "Grimoire_runebook_dump.txt"
    dump = {"written": False, "armed": False,   # one dump per session, or per Refresh / Re-read
            "books": set()}     # 2.6.81 (GR-8): the book the dump file holds (only the last one)


    def dump_due():
        """Would write_dump write now? (skips gathering the details when not)"""
        return not dump["written"] or dump["armed"]


    def write_dump(text):
        """The details of a book that couldn't be read, for the dump file. Written
        once per session (and again after Refresh or a book's Re-read): before,
        every failed read of every book rewrote the file and printed the line,
        once per book per scan. The per-tab error text is kept either way."""
        if not dump_due():
            return None
        dump["written"], dump["armed"] = True, False
        path = data_path(DUMP_FILE)
        try:
            write_file(path, text)
        except Exception as ex:
            API.SysMsg("Grimoire: couldn't save the runebook details (%s)." % ex, Kit.HUE_BAD)
            return None
        API.SysMsg("Grimoire: saved the runebook details to %s." % path, Kit.HUE_INFO)
        return path


    def dumped(serial, path):
        """2.6.81 (GR-8): the dump file now holds this book (it holds one: replaced)."""
        if path:
            old, dump["books"] = dump["books"], set([serial])
            for s in old:                # a page drawn for the book it held says so no more
                if s != serial:
                    Kit.on_client(lambda s=s: drop_page(s) if s in pages else None)


    def describe_items(container):
        return Kit.on_client(lambda: [
            "  0x%08X  graphic 0x%04X  hue 0x%04X  amount %d  name '%s'"
            % (it.Serial, it.Graphic, it.Hue, it.Amount or 0, it.Name or "")
            for it in list(API.ItemsInContainer(container) or [])])


    def open_book(serial):
        """Double-click a runebook and see what the server does.
        Returns ("gump", gump_id), ("container", None) or (None, reason).
        Waits: only ever run from the thread job. Each look is one client hop."""
        nonlocal gump_id
        if gump_id and API.HasGump(gump_id):
            API.CloseGump(gump_id)
            HOST.idle(0.1)
        before = API.HasGump()
        if HIDE_RUNEBOOK_GUMP:
            API.ConfigNextGump(serial=gump_id, isVisible=False)
        API.UseObject(serial)

        def look():
            gid = API.HasGump()
            if gid and (gid == gump_id or gid != before):
                return ("gump", gid)
            book = API.FindItem(serial)
            try:
                if book and book.GetContainerGump():
                    return ("container", None)
            except Exception:
                pass
            return None

        result = (None, "double-clicking the book opened nothing within 3 seconds")
        deadline = time.time() + 3.0
        while time.time() < deadline and HOST.idle(0.05):
            seen = Kit.on_client(look)
            if seen is not None:
                result = seen
                break
        API.ConfigNextGump()   # clear any pending config
        if result[0] is None and Kit.on_client(lambda: len(list(API.ItemsInContainer(serial) or []))):
            result = ("container", None)
        if result[0] == "gump" and result[1] != gump_id:
            API.SysMsg("Grimoire: the runebook gump ID is 0x%08X (set RUNEBOOK_GUMP_ID to this)."
                       % result[1], Kit.HUE_INFO)
            gump_id = result[1]
        return result


    def rune_label(rune_serial):
        """A rune's name. Uses its item name, or single-clicks it and reads the label."""
        def item_name():
            it = API.FindItem(rune_serial)
            return ((it.Name if it else "") or "").strip()
        name = Kit.on_client(item_name)
        if not name or name.lower() in ("recall rune", "a recall rune", "rune"):
            try:
                # The journal is shared by every module, so instead of clearing it
                # only lines that arrived after the click are looked at (the
                # shared Journal, read once per pass for every module).
                # 2.6.81 (GR-7): only an item label counts (no speaker, or the rune's
                # own name), never speech or a Virtue Assistant "<Title>:" line; one
                # that says "rune" wins, any other is taken after a short wait for one.
                rd = journal_from_now()
                clicked = time.time()
                API.ClickObject(rune_serial)
                deadline = clicked + 1.0
                own = name.lower()
                plain, plain_by = None, 0.0
                while time.time() < deadline and HOST.idle(0.1):
                    best = None
                    for ln in rd.new():
                        who = (ln.name or "").lower()
                        txt = (ln.text or "").strip()
                        if not txt or (who and who != own) or va_line(txt):
                            continue
                        if "rune" in ln.low:
                            best = txt
                            break
                        if plain is None:
                            plain, plain_by = txt, time.time() + 0.3
                    if best is not None:
                        name = best
                        break
                    if plain is not None and time.time() >= plain_by:
                        name = plain
                        break
                else:
                    if plain is not None:
                        name = plain
            except Exception:
                pass
        return re.sub(r"^(a |an )?(marked )?recall rune( for| to)?\s*", "", name, flags=re.I).strip()


    def read_container_book(serial):
        dests = []
        runes = Kit.on_client(lambda: [it.Serial for it in list(API.ItemsInContainer(serial) or [])])
        for rune in runes or []:
            name = rune_label(rune)
            if not name or "unmarked" in name.lower():
                continue
            dests.append({"name": name, "slot": None, "button": None, "rune": rune})

        def close():
            try:
                book = API.FindItem(serial)
                g = book.GetContainerGump() if book else None
                if g:
                    g.Dispose()
            except Exception:
                pass
        Kit.on_client(close)
        return sorted(dests, key=lambda d: d["name"].lower())


    def gump_text(gid):
        """(PacketGumpText, error) of a server gump, read in one client hop."""
        def read():
            g = API.GetGump(gid)
            try:
                return ((g.PacketGumpText or "") if g else ""), None
            except Exception as ex:
                return "", ex
        return Kit.on_client(read)


    def read_runebook(serial):
        """Returns (destinations or None, (charges, max) or None)."""
        rune_errors.pop(serial, None)
        kind, gid = open_book(serial)

        if kind == "container":
            dests = read_container_book(serial)
            if not dests:
                rune_errors[serial] = "The book opened like a bag, but no named runes were inside."
                if dump_due():
                    dumped(serial, write_dump("Runebook 0x%08X opened as a CONTAINER\n\n" % serial +
                                              "\n".join(describe_items(serial))))
            return dests, None

        if kind is None:
            rune_errors[serial] = "Couldn't open it: " + gid + "."
            if dump_due():
                dumped(serial, write_dump("Runebook 0x%08X: %s\nLast server gump: 0x%08X\nItems inside:\n%s"
                                          % (serial, gid, API.HasGump(),
                                             "\n".join(describe_items(serial)) or "  (none known)")))
            return None, None

        raw, ex = gump_text(gid)
        if not raw:
            HOST.idle(0.1)                       # text not in yet - one more try
            raw, ex = gump_text(gid)
        if ex is not None:
            rune_errors[serial] = "Couldn't read the book's window (%s)." % ex
        API.CloseGump(gid)
        dests = extract_destinations(raw) if raw else []
        if not dests:
            rune_errors.setdefault(serial, "The book's window didn't match any known layout.")
            if dump_due():                                     # only when the dump is written
                lines, buttons, _ = gump_elements(raw) if raw else ([], [], [])
                parse_stats["selftest"] = parser_selftest()
                dumped(serial, write_dump("Runebook 0x%08X  gump 0x%08X  (%d texts, %d buttons)\nparser: %r\n\n%s"
                                          % (serial, gid, len(lines), len(buttons), parse_stats,
                                             raw or "(empty PacketGumpText)")))
            return dests, None
        return dests, extract_charges(raw)


    def note_open_gump(book_serial, gid):
        """The book's gump is open anyway (we're travelling): refresh its saved list and charges."""
        raw, _ = gump_text(gid)
        if not raw:
            return
        dests = extract_destinations(raw)
        if dests and store_book(book_serial, dests, extract_charges(raw)):
            Kit.on_client(lambda: drop_page(book_serial))     # redraw in one hop


    def fresh_dest(serial, dest):
        """(2.6.84) The rune the press meant, in the list just read off the open
        gump (note_open_gump): its name decides, its old slot only breaks a tie.
        A rune dropped from the book by hand shifts the later slots down: the
        old slot would recall to the next rune. None when it is gone."""
        same = [d for d in (rune_cache.get(serial) or ())
                if d.get("name") == dest.get("name") and d.get("slot") is not None]
        for d in same:
            if d["slot"] == dest["slot"]:
                return d
        return same[0] if same else None


    # 2.6.81 (GR-6): the lines that mean a travel spell failed, matched (lower case)
    # only in the server's lines and your own (never another player's speech, never
    # a Virtue Assistant "<Title>:" line). The spell failures, then the travel
    # refusals of RunUO (check the shard's exact words in game). The loose "You
    # cannot" / "must wait" are gone: they matched other players and other actions.
    TRAVEL_FAIL_TEXTS = CAST_FAIL_TEXTS + ("already casting", "not allowed to travel",
                                           "recall from this", "gate from this", "travel from this",
                                           "location is blocked", "too encumbered",
                                           "heat of battle", "doth not appear to work",
                                           "is not marked", "not yet marked")


    def item_amount(it):
        """A stack's amount (a single item counts 1, whatever the client says)."""
        try:
            return max(1, int(it.Amount or 0))
        except Exception:
            return 1


    def trip_look(serials):
        """Thread job only, one hop: (a cursor is up, the total amount of the items
        `serials` still in your pack, (x, y) of you)."""
        def look():
            up, n, xy = False, 0, None
            try:
                up = bool(API.HasTarget("any"))
            except Exception:
                pass
            for s in serials:
                it = API.FindItem(s)
                if it:
                    n += item_amount(it)
            try:
                xy = (int(API.Player.X), int(API.Player.Y))
            except Exception:
                pass
            return up, n, xy
        return Kit.on_client(look)


    def cursor_up_refused():
        """2.6.81 (GR-X1): a target cursor is up that Grimoire didn't raise (a spell
        cast from a TazUO icon, a skill): the armed pre-target can't take it and
        an answer would go to it, so the trip is refused. Thread job only (one hop)."""
        if safe(lambda: API.HasTarget("any"), False):
            API.SysMsg("Grimoire: a target cursor is up; finish it or press Esc first.",
                       Kit.HUE_INFO)
            return True
        return False


    def travel_by_scroll(book_serial, dest, method):
        """Read a Recall or Gate Travel scroll at the chosen rune.

        A scroll can't pick a rune inside a runebook - targeting the book uses its
        *default* rune. So the rune is made the book's default first, then the
        scroll is read on the book. (Rune-bag books: the rune is targeted directly.)"""
        graphic = GATE_SCROLL if method == "gate_scroll" else RECALL_SCROLL
        spell = "Gate Travel" if method == "gate_scroll" else "Recall"
        # Only failures from now on count. The journal is shared by every module
        # (Unified Bag, Meters, ... read "fizzles", "must wait" too), so instead of
        # clearing those lines only the ones that arrive after this moment are read.
        since = journal_from_now()
        me = player_name()                   # 2.6.81 (GR-6): your own lines count, not others'
        # 2.6.81 (GR-3): the stack's amount too, in the same hop: the server uses the
        # scroll up once its cursor was answered, which ends the wait below
        found = Kit.on_client(lambda: next(((it.Serial, item_amount(it)) for it in items_in_pack()
                                            if it.Graphic == graphic), None))
        if not found:
            API.SysMsg("Grimoire: you have no %s scrolls." % spell, Kit.HUE_BAD)
            return
        scroll, before = found

        target = dest.get("rune")
        if not target:
            if dest["slot"] is None:
                API.SysMsg("Grimoire: scrolls need a standard runebook layout.", Kit.HUE_BAD)
                return
            kind, gid = open_book(book_serial)
            if kind != "gump":
                API.SysMsg("Grimoire: the runebook did not open.", Kit.HUE_BAD)
                return
            note_open_gump(book_serial, gid)
            HOST.idle(0.1)
            dest = fresh_dest(book_serial, dest)      # (2.6.84) the slot as the book has it now
            if dest is None:
                API.CloseGump(gid)
                API.SysMsg("Grimoire: that rune isn't in the book any more; nothing was used.",
                           Kit.HUE_BAD)
                return
            if HIDE_RUNEBOOK_GUMP:
                API.ConfigNextGump(serial=gid, isVisible=False)   # the server reopens the book
            API.ReplyGump(2 + dest["slot"] * 6 + SET_DEFAULT_TYPE, gid)
            deadline = time.time() + 2.0
            while time.time() < deadline and HOST.idle(0.1):
                if API.HasGump(gid):
                    break
            API.ConfigNextGump()
            API.CloseGump(gid)
            if not HOST.idle(0.3):
                return
            target = book_serial

        # The armed pre-target answers the NEXT cursor, whoever raised it, so first
        # let another module's cursor (a bandage, a heal) finish, then speak for the
        # cursor until the scroll's own has been answered (see HOST.claim_cursor).
        if not wait_cursor_free():
            return
        if cursor_up_refused():              # 2.6.81 (GR-X1): one came up while the default was set
            return
        claim_cursor(SCROLL_CAST_TIMEOUT + 1.0)
        try:
            start = player_xy()
            # Pre-target so the client answers the cursor the moment the cast finishes,
            # however long the cast takes on this shard.
            API.CancelPreTarget()
            API.PreTarget(target, "neutral")
            API.UseObject(scroll)

            # Fallback: if a cursor shows up and the pre-target didn't take it, answer it ourselves.
            # (2.6.81: one hop per look for the cursor, the scroll and your place.)
            deadline = time.time() + SCROLL_CAST_TIMEOUT
            while time.time() < deadline and HOST.idle(0.1):
                up, left, now_xy = trip_look((scroll,))
                if up:
                    HOST.idle(0.15)                  # give the pre-target a moment to fire first
                    if API.HasTarget("any") and not cursor_taken():
                        API.Target(target)
                    return
                if left < before:
                    break                            # 2.6.81 (GR-3): the scroll was used: cast done
                if failed_since(since, me):
                    break
                if moved_far(start, now_xy):
                    break                            # you've arrived: the pre-target was used
        finally:
            API.CancelPreTarget()                    # never leave it armed for the next cursor
            release_cursor()


    # ---- sharing the one target cursor with the other modules (HOST.claim_cursor) ----
    CURSOR_KEY = "grimoire"
    CURSOR_WAIT = 3.0              # longest wait for another module's cursor before going ahead


    def cursor_taken():
        """Another module (or a HOST.pick_target) has the cursor spoken for.
        (Plain try/except: asked on every tick while a cast or a read is pending.)"""
        try:
            return HOST.cursor_busy(CURSOR_KEY) is not None
        except Exception:
            return False


    def claim_cursor(seconds):
        safe(lambda: HOST.claim_cursor(CURSOR_KEY, seconds))


    def release_cursor():
        safe(lambda: HOST.release_cursor(CURSOR_KEY))


    def wait_cursor_free():
        """Thread job only: wait (at most CURSOR_WAIT s) while someone else's cursor
        is spoken for. False if Grimoire was switched off meanwhile."""
        until = time.time() + CURSOR_WAIT
        while cursor_taken() and time.time() < until:
            if not HOST.idle(0.1):
                return False
        return True


    def player_xy():
        return Kit.on_client(lambda: safe(lambda: (int(API.Player.X), int(API.Player.Y)), None))


    def player_name():
        """Your character's name (in place on the client thread, else one hop)."""
        return Kit.on_client(lambda: safe(lambda: API.Player.Name or "", "")) or ""


    def moved_far(start, now):
        """True when now is far from where the cast began (the recall took you)."""
        return start is not None and now is not None and \
            max(abs(now[0] - start[0]), abs(now[1] - start[1])) > 30


    def journal_from_now():
        """A reader of the shared journal (Journal) that starts now: the client's
        journal is read up to this moment first, so the reader's new() hands
        over only the lines that arrive after it. Thread jobs only."""
        try:
            Journal.update(True)
        except Exception:
            pass
        return Journal.Reader()


    _va = {"titles": None}       # every module's and part's title (journal prefixes)


    def va_line(text):
        """2.6.81: a Virtue Assistant journal line ("Bandages: ...", "Character HUD >
        Frames: ..."): it starts with a loaded module's or part's title and ": ".
        The titles are gathered once (a plain "Word: " a server line might start
        with is not taken for one)."""
        i = text.find(": ")
        if i <= 0 or i > 60:
            return False
        titles = _va["titles"]
        if titles is None:
            titles = set(["Virtue Assistant", "Grimoire"])
            try:
                for sl in HOST.slots:
                    titles.add(sl.title)
                    for p in sl.parts:
                        titles.add(p[1])
                        titles.add("%s > %s" % (sl.title, p[1]))
            except Exception:
                pass
            _va["titles"] = titles
        return text[:i] in titles


    def failure_in(lines, texts, me):
        """2.6.81 (GR-2, GR-6): one of `texts` (lower case) in a line from the server
        or from you (`me`: the fizzle comes with your own name), never in another
        player's speech nor in a Virtue Assistant "<Title>:" line."""
        for ln in lines:
            name = ln.name or ""
            if name and name != "System" and name != me:
                continue
            low = ln.low
            for f in texts:
                if f in low:
                    if not va_line(ln.text or ""):
                        return True
                    break
        return False


    def failed_since(rd, me=""):
        """A travel failure line (TRAVEL_FAIL_TEXTS) among the journal lines that
        came in since the reader rd was started (journal_from_now). Each look
        hands over only the newer lines; the older ones were checked already."""
        try:
            return failure_in(rd.new(), TRAVEL_FAIL_TEXTS, me)
        except Exception:
            return False


    def travel(book_serial, dest, method):
        if cursor_up_refused():                    # 2.6.81 (GR-X1): someone else's cursor is up
            return
        if method in ("recall_scroll", "gate_scroll"):
            travel_by_scroll(book_serial, dest, method)
            return
        if dest.get("rune"):                       # rune-bag style book: cast at the rune itself
            spell = TRAVEL_SPELL.get(method, "Recall")
            if not wait_cursor_free():             # the pre-target would answer their cursor
                return
            if cursor_up_refused():                # 2.6.81 (GR-X1): one came up while waiting
                return
            claim_cursor(RUNE_CAST_CLAIM)          # ours until the spell's cursor is answered
            try:
                since, start, me = journal_from_now(), player_xy(), player_name()
                # 2.6.81 (GR-3): the server uses up the reagents once the cursor was
                # answered (a Gate doesn't move you): your Black Pearl, counted now
                pearl = REAGENTS["BP"][1]
                stacks = Kit.on_client(lambda: [(it.Serial, item_amount(it))
                                                for it in items_in_pack(True)
                                                if it.Graphic == pearl]) \
                    if spell in PEARL_SPELLS else None
                serials = tuple(s for s, _n in stacks or ())
                before = sum(n for _s, n in stacks or ())
                API.CancelPreTarget()
                API.PreTarget(dest["rune"], "neutral")
                API.CastSpell(spell)
                # A fizzle, missing reagents or an interrupted cast never asks for
                # the target: the armed pre-target would then answer the next
                # cursor anyone raises (a bandage). Watch the cast, then disarm it.
                deadline = time.time() + RUNE_CAST_CLAIM
                while time.time() < deadline and HOST.idle(0.1):
                    up, left, now_xy = trip_look(serials)
                    if up:
                        HOST.idle(0.15)              # the pre-target answers it
                        break
                    if before and left < before:
                        break                        # 2.6.81 (GR-3): reagents used: cast done
                    if failed_since(since, me) or moved_far(start, now_xy):
                        break
                API.CancelPreTarget()
            finally:
                release_cursor()
            return
        kind, gid = open_book(book_serial)
        if kind != "gump":
            API.SysMsg("Grimoire: the runebook did not open.", Kit.HUE_BAD)
            return
        note_open_gump(book_serial, gid)
        HOST.idle(0.1)
        if dest["slot"] is not None:
            dest = fresh_dest(book_serial, dest)
            if dest is None:
                API.CloseGump(gid)
                API.SysMsg("Grimoire: that rune isn't in the book any more; nothing was used.",
                           Kit.HUE_BAD)
                return
            API.ReplyGump(2 + dest["slot"] * 6 + TRAVEL_TYPES[method], gid)
        else:
            API.ReplyGump(dest["button"], gid)     # custom book: press the rune's own button
        if (method == "charge" or dest["slot"] is None) and book_serial not in bg_reads:
            bg_reads.append(book_serial)           # re-read the charge count once the recall is done


    # ------------------------------------------------------------------------------
    #  UI helpers
    # ------------------------------------------------------------------------------

    # Layout is written at 100% scale; these turn it into real pixels.
    view = {"scale": 1.0}


    def sc(v):
        return int(round(v * view["scale"]))


    _props = {}


    def clr_prop(obj, name):
        """A .NET property of obj (searching base classes), or None."""
        from System.Reflection import BindingFlags
        t = obj.GetType()
        key = (t.FullName, name)
        if key not in _props:
            flags = (BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic |
                     BindingFlags.DeclaredOnly)
            p = None
            while t is not None and p is None:
                p = t.GetProperty(name, flags)
                t = t.BaseType
            _props[key] = p
        return _props[key]


    _vis = {"ok": None, "way": None}


    def _shown_attr(ctrl, shown):
        ctrl.IsVisible = shown           # the script control's own IsVisible (public API)


    def _shown_clr(ctrl, shown):
        p = clr_prop(ctrl, "Control")    # older builds: the client control, by reflection
        inner = p.GetValue(ctrl, None) if p is not None else ctrl
        clr_prop(inner, "IsVisible").SetValue(inner, shown, None)


    def set_shown(ctrl, shown):
        """Show or hide a control instantly (no rebuild). Returns False if the client
        doesn't allow it, in which case tab switches fall back to redrawing. The
        way that works is found once: the control's public IsVisible, else the
        client control behind it by reflection (before: reflection for every
        control on every tab switch)."""
        if _vis["ok"] is False:
            return False
        shown = bool(shown)
        way = _vis["way"]
        for fn in ((way,) if way is not None else (_shown_attr, _shown_clr)):
            try:
                fn(ctrl, shown)
                _vis["ok"], _vis["way"] = True, fn
                return True
            except Exception:
                pass
        if way is not None and fn is _shown_attr:
            try:                             # this control only: the other way
                _shown_clr(ctrl, shown)
                return True
            except Exception:
                pass
        _vis["ok"] = False
        return False


    def on_window(parent, ctrl):
        """Note a control placed straight on the window, hiding it first if its layer is hidden."""
        if parent is gump:
            tgt["tops"].append(ctrl)
            if tgt["hidden"]:
                set_shown(ctrl, False)


    def show_layer(layer, shown):
        for ctrl in layer["tops"]:
            if not set_shown(ctrl, shown):
                return False
        layer["hidden"] = not shown
        return True


    def put(parent, ctrl, track):
        """Add ctrl to parent (noting it if it sits straight on the window) and to track."""
        on_window(parent, ctrl)
        parent.Add(ctrl)
        track.append(ctrl)
        return ctrl


    def box(parent, x, y, w, h, color, alpha, track):
        b = G.CreateGumpColorBox(alpha, color)
        b.SetRect(sc(x), sc(y), max(1, sc(w)), max(1, sc(h)))
        return put(parent, b, track)


    def label(parent, text, x, y, size, color, track, width=0, align="left", smooth=False):
        """Short text uses the client's UO font in a client hue, like every other
        window; wrapped text (a width with left alignment) keeps the smooth font.
        smooth=True asks for the smooth font outright (the runebook pages use it)."""
        hue = TEXT_HUES.get(color)
        if USE_UO_FONT and hue is not None and not smooth and not (width and align == "left"):
            l = G.CreateGumpLabel(text, hue)
            l.SetAcceptMouseInput(False)
            place_uo(l, x, y, size, width, align)
            return put(parent, l, track)
        size = max(6, sc(size))
        if width:
            l = G.CreateGumpTTFLabel(text, size, color, aligned=align, maxWidth=sc(width))
        else:
            l = G.CreateGumpTTFLabel(text, size, color)
        l.SetPos(sc(x), sc(y))
        l.SetAcceptMouseInput(False)
        return put(parent, l, track)


    _uo_meta = {}               # label -> (x, y, size, width, align); keyed by the control itself
    #                             (id() of a client object is a slow lookup in IronPython)


    def place_uo(l, x, y, size, width, align):
        """Position a UO font label on the line a smooth label of `size` would use,
        centred or right-aligned inside `width` (layout units)."""
        try:                                 # 2.6.82: plain try, no lambdas (every count change)
            lw = int(l.GetWidth())
        except Exception:
            lw = 0
        if not lw:
            try:
                lw = 7 * len(l.Text or "")
            except Exception:
                lw = 0
        try:
            lh = int(l.GetHeight()) or 16
        except Exception:
            lh = 16
        X = sc(x)
        if width and align == "center":
            X += max(0, (sc(width) - lw) // 2)
        elif width and align == "right":
            X += max(0, sc(width) - lw)
        Y = sc(y) + max(0, (int(sc(size) * 1.3) - lh) // 2)
        l.SetPos(X, Y)
        if width and align != "left":
            if len(_uo_meta) > 3000:
                for k in list(_uo_meta):
                    try:
                        gone = k.IsDisposed
                    except Exception:
                        gone = True
                    if gone:
                        del _uo_meta[k]
            try:
                _uo_meta[l] = (x, y, size, width, align)
            except TypeError:                # an unhashable stand-in: not re-placed on change
                pass


    def set_label_text(l, text):
        try:
            l.Text = text
        except Exception:
            safe(lambda: l.SetText(text))
        try:
            m = _uo_meta.get(l)
        except TypeError:
            m = None
        if m is not None:
            place_uo(l, m[0], m[1], m[2], m[3], m[4])


    def item_pic(parent, graphic, x, y, size, track):
        p = G.CreateGumpItemPic(graphic, sc(size), sc(size))
        p.SetPos(sc(x), sc(y))
        p.SetAcceptMouseInput(False)
        return put(parent, p, track)


    def star(parent, x, y, on, track):
        """A destination's 14 x 14 star at (x, y) (layout units): gold when it
        is in Favourites, grey when not. Returns its boxes (recolor_star)."""
        color = STAR_ON if on else STAR_OFF
        parts = []
        for rx, ry, rw, rh in STAR_RECTS:
            b = box(parent, x + rx, y + ry, rw, rh, color, 1.0, track)
            b.SetAcceptMouseInput(False)
            parts.append(b)
        return parts


    _star_rgb = {True: tuple(int(STAR_ON[i:i + 2], 16) for i in (1, 3, 5)),
                 False: tuple(int(STAR_OFF[i:i + 2], 16) for i in (1, 3, 5))}


    def recolor_star(parts, on):
        """A star turned on / off in place (the colour box's SetBaseColor).
        False if this client build can't: the caller draws the page again."""
        r, g_, b_ = _star_rgb[bool(on)]
        try:
            for p in parts:
                p.SetBaseColor(r, g_, b_, 255)
            return True
        except Exception:
            return False


    def on_click(ctrl, fn):
        G.AddControlOnClick(ctrl, fn)


    # TazUO swallows the second click of a real double-click (it never reaches
    # AddControlOnClick), so rows also hook the control's own double-click event.
    _dbl = {"ok": None}


    def hook_double_click(api_ctrl, fn):
        """Kit.hook_double, with a one-time note if the client won't allow it."""
        if _dbl["ok"] is False:
            return False
        _dbl["ok"] = Kit.hook_double(api_ctrl, fn, queue=False)
        if not _dbl["ok"]:
            API.SysMsg("Grimoire: double-clicks can't be caught on this client; "
                       "click a row, then click it again to use it.", Kit.HUE_BAD)
        return _dbl["ok"]


    def make_row_click(key, action):
        """Single click selects the row. If the double-click hook failed, clicking the
        already-selected row again triggers the action instead."""
        def cb():
            now = time.time()
            prev = click_state["selected"]
            try:                           # a row of a page redrawn since may be gone
                if prev is not None and prev != key and prev in row_bgs:
                    row_bgs[prev].SetAlpha(ROW_A)
                if key in row_bgs:
                    row_bgs[key].SetAlpha(ROW_SEL)
            except Exception:
                pass
            click_state["selected"] = key
            if _dbl["ok"] is False and click_state["key"] == key and now - click_state["t"] <= 3.0:
                click_state["key"], click_state["t"] = None, 0.0
                state["queue"].append(stamped(action, now))
            else:
                click_state["key"], click_state["t"] = key, now
        return cb


    def stamped(action, now=None):
        """2.6.81 (GR-4): a cast carries its press time (a press older than
        CAST_DEFER when the tick gets to it is dropped, not cast late); every other
        action keeps its shape (a trip's act[1..3])."""
        if action[0] == "cast":
            return action + (now or time.time(),)
        if action[0] in ("travel", "favgo"):     # (2.6.84) a trip carries its press time too
            return ("pressed", now or time.time(), action)
        return action


    def bind_row(bg, key, action):
        on_click(bg, make_row_click(key, action))
        hook_double_click(bg, lambda: state["queue"].append(stamped(action)))


    def pick_circle(i):
        """Click on a circle tab: only queued; the tick swaps the page in (see
        run_ui_action) - the tick is the one place the window changes."""
        return queue_ui(("circle", i))


    def go_circle(i):
        if i != state["circle"] or state["tab"] != "spells":
            switch_page("spells", lambda: state.update({"circle": i}))


    def queue_action(action):
        def cb():
            state["queue"].append(action)
        return cb


    def queue_stamped(action):
        """(2.6.84) A press that carries its time (stamped): a trip."""
        def cb():
            state["queue"].append(stamped(action))
        return cb


    def queue_ui(action):
        """A window action (minimize, a circle, Settings, Close): its own queue,
        drained on every tick before the job queue. (2.6.81) It is handled on the
        next tick, which comes once any runebook job running now has finished
        (the host skips this module's tick while its thread job runs)."""
        def cb():
            if action not in state["ui_queue"]:
                state["ui_queue"].append(action)
        return cb


    # ------------------------------------------------------------------------------
    #  Window: persistence
    # ------------------------------------------------------------------------------

    def load_int(name, default):
        try:
            return int(Kit.get_var("Grimoire_" + name, str(default)))
        except Exception:
            return default


    def save_int(name, value):
        Kit.put_var("Grimoire_" + name, str(int(value)))


    win = {"w": DEFAULT_W, "h": DEFAULT_H, "opacity": DEFAULT_OPACITY}
    pending_scale = {"value": None, "t": 0.0}   # applied once the slider stops moving


    def load_window_prefs():
        view["scale"] = min(SCALE_MAX, max(SCALE_MIN, load_int("Scale", 100))) / 100.0
        win["w"] = max(sc(MIN_W), load_int("W", sc(DEFAULT_W)))      # real pixels
        win["h"] = max(sc(MIN_H), load_int("H", sc(DEFAULT_H)))
        win["opacity"] = min(100, max(0, load_int("Opacity", DEFAULT_OPACITY)))
        fit_screen()


    def fit_screen():
        """2.6.81 (GR-5): never taller (or wider) than the screen: the window is cut
        to it, and its spell, rune, Favourites and supplies lists scroll, as they
        do in any shorter window. Not while the layout fits it to a zone slot
        (the slot's size is the layout's). Only the size in use is cut: your
        saved size changes only when you resize the window yourself."""
        if fitst["own"] is not None:
            return
        try:
            W, H = Kit.screen()
        except Exception:
            return
        if H > 0:
            win["h"] = max(MIN_H * SCALE_MIN // 100, min(win["h"], H))
        if W > 0:
            win["w"] = max(MIN_W * SCALE_MIN // 100, min(win["w"], W))


    def LW():
        """Window width / height in layout units (100% scale)."""
        return max(MIN_W, int(win["w"] / view["scale"]))


    def LH():
        return max(MIN_H, int(win["h"] / view["scale"]))


    bg_box = {"parts": []}       # the backdrop pieces - the only things the % slider changes


    # ------------------------------------------------------------------------------
    #  Window: creation
    # ------------------------------------------------------------------------------

    def on_resized():
        if state["minimized"]:
            return
        win["w"], win["h"] = gump.GetWidth(), gump.GetHeight()
        loop["size_dirty"] = True             # saved with the settled redraw (not twice per drag step)
        state["dirty"] = True
        loop["settle"] = time.time() + RESIZE_SETTLE    # redraw once the drag has settled, not per event


    def save_size():
        """The window's size, saved once a resize has settled (see _tick). While
        the layout fits the window to a zone, the size is kept at your own
        scale (the one that comes back when the window is freed)."""
        loop["size_dirty"] = False
        if fitst["own"] is not None:
            return                       # (2.6.56) the slot's size is the layout's, not yours
        save_int("W", win["w"])
        save_int("H", win["h"])


    def create_window():
        """The resizable window; its own panel art is hidden and drawn over."""
        nonlocal gump
        fit_screen()                          # 2.6.81 (GR-5): the screen of today
        px, py = load_int("X", -1), load_int("Y", -1)
        if px >= 0:                           # a saved place: on the screen of today, wholly
            px, py = Kit.adapt(px, max(0, py), win["w"], win["h"])
            px, py = Kit.clamp(px, py, win["w"], win["h"])   # (window rule 1, for a modern gump)
            px, py = max(0, px), max(0, py)                  # (a saved place is never negative)
        # The minimum size allows the smallest scale; layout never goes below MIN_W x MIN_H units.
        gump = G.CreateModernGump(px if px >= 0 else 100, py if py >= 0 else 60, win["w"], win["h"],
                                  True, MIN_W * SCALE_MIN // 100, MIN_H * SCALE_MIN // 100, on_resized)
        gump.SetAlpha(0)
        if px < 0:
            gump.CenterXInViewPort()
            gump.CenterYInViewPort()


    def clear(track):
        meta = _uo_meta
        for c in track:
            if meta:
                try:
                    meta.pop(c, None)     # its placement note goes with it (no dead labels kept)
                except TypeError:
                    pass
            try:
                c.Dispose()
            except Exception:
                pass
        del track[:]


    # ---- Gump art ----

    _art_sizes = {}
    _art = {"ok": None}


    def art_size(graphic):
        """Natural (width, height) of a gump graphic, or (0, 0) if it can't be loaded."""
        if graphic not in _art_sizes:
            w = h = 0
            try:
                p = G.CreateGumpPic(graphic, 0, 0, 0)
                try:
                    w, h = int(p.GetWidth()), int(p.GetHeight())
                except Exception:
                    prop = clr_prop(p, "Control")
                    inner = prop.GetValue(p, None) if prop is not None else p
                    w = int(clr_prop(inner, "Width").GetValue(inner, None))
                    h = int(clr_prop(inner, "Height").GetValue(inner, None))
                p.Dispose()
            except Exception:
                pass
            _art_sizes[graphic] = (w, h)
        return _art_sizes[graphic]


    def art_ok():
        if _art["ok"] is None:
            _art["ok"] = bool(USE_GUMP_ART and art_size(ART_FRAME)[0] > 0 and
                              art_size(Kit.SECTION_TILE)[0] > 0 and art_size(GEM)[0] > 0)
        return _art["ok"]


    def pic_px(parent, graphic, X, Y, W, H, track, mouse=False):
        """A gump picture at real pixel coordinates, stretched to W x H."""
        p = G.CreateGumpPic(graphic, X, Y, 0)
        p.SetWidth(max(1, W))
        p.SetHeight(max(1, H))
        if not mouse:
            p.SetAcceptMouseInput(False)
        return put(parent, p, track)


    def tiled_px(parent, graphic, X, Y, W, H, track):
        """Gump art repeated over W x H real pixels (falls back to stretching)."""
        try:
            t = G.CreateTiledGumpPic(graphic, max(1, W), max(1, H))
        except Exception:
            return pic_px(parent, graphic, X, Y, W, H, track)
        t.SetRect(X, Y, max(1, W), max(1, H))
        t.SetAcceptMouseInput(False)
        return put(parent, t, track)


    def stone(parent, x, y, w, h, track, alpha=1.0):
        """The stone frame of the crafting gump, drawn from its nine
        pieces. Returns [(piece, alpha factor)] for the opacity slider."""
        if not art_ok():
            parts = [(box(parent, x, y, w, h, COL_BG, alpha, track), 1.0)]
            for (bx, by, bw, bh) in ((x, y, w, 2), (x, y + h - 2, w, 2), (x, y, 2, h), (x + w - 2, y, 2, h)):
                box(parent, bx, by, bw, bh, COL_BORDER, 1.0, track)
            return parts
        X0, Y0, X3, Y3 = sc(x), sc(y), sc(x + w), sc(y + h)
        lw, th = art_size(ART_FRAME)
        rw, bh = art_size(ART_FRAME + 8)
        lw, rw = min(lw, (X3 - X0) // 2), min(rw, (X3 - X0) // 2)
        th, bh = min(th, (Y3 - Y0) // 2), min(bh, (Y3 - Y0) // 2)
        xs = [X0, X0 + lw, X3 - rw, X3]
        ys = [Y0, Y0 + th, Y3 - bh, Y3]
        parts = []
        for i in [4, 0, 1, 2, 3, 5, 6, 7, 8]:            # centre first, edges over it
            cx, cy = i % 3, i // 3
            W, H = xs[cx + 1] - xs[cx], ys[cy + 1] - ys[cy]
            if W <= 0 or H <= 0:
                continue
            if i in (0, 2, 6, 8):
                parts.append(pic_px(parent, ART_FRAME + i, xs[cx], ys[cy], W, H, track))
            else:
                parts.append(tiled_px(parent, ART_FRAME + i, xs[cx], ys[cy], W, H, track))
        for p in parts:
            p.SetAlpha(alpha)
        return [(p, 1.0) for p in parts]


    def parchment(parent, x, y, w, h, track, alpha=1.0):
        """A black section, like each part of the crafting gump. Returns
        [(backdrop, alpha factor)] for the opacity slider."""
        if art_ok():
            p = tiled_px(parent, Kit.SECTION_TILE, sc(x), sc(y), sc(w), sc(h), track)
        else:
            p = box(parent, x, y, w, h, COL_PARCH, 1.0, track)
        p.SetAlpha(alpha * Kit.SECTION_ALPHA)
        return [(p, Kit.SECTION_ALPHA)]


    def corner_knots(w, h, track):
        """The knots on the frame's corners."""
        if not art_ok() or not Kit.CORNER_ART:
            return
        cw, ch = art_size(Kit.CORNER_ART)
        if not cw or not ch:
            return
        W, H = sc(w), sc(h)
        out = []
        for X, Y in ((0, 0), (W - cw, 0), (0, H - ch), (W - cw, H - ch)):
            out.append(pic_px(gump, Kit.CORNER_ART, X, Y, cw, ch, track))
        return out


    _ttf_widths = {}             # (text, size) -> smooth-font width in real pixels


    MEASURE_MAX = 4000           # widths kept in the cache (window sizes and scales come and go)


    def measure(cache, key, make, guess):
        """Pixel width of a label make() builds (measured once, `guess` if it can't
        be), in layout units."""
        if key not in cache:
            if len(cache) >= MEASURE_MAX:
                cache.clear()             # measured again as needed: never grows without end
            px = 0
            try:
                l = make()
                px = int(l.GetWidth() or 0)
                safe(lambda: l.Dispose())
            except Exception:
                pass
            cache[key] = px or guess
        return int(round(cache[key] / view["scale"]))


    def text_w(text):
        """Width of text in the client's label font, in layout units. The UO font
        is not scaled, so the mother's shared measure (Kit.text_px: letter sums,
        one cache for every module) is divided by the layout scale. Before: an
        own label-per-text cache beside Kit's."""
        return int(round(Kit.text_px(text) / view["scale"]))


    def fit(text, room, size=None):
        """Text cut short with ".." if it's wider than `room` (layout units), in
        the label font (Kit.fit: letter sums, no label per try) or, with a size,
        the smooth font (halving: a few labels, never one per letter)."""
        if size is None:
            return Kit.fit(text, sc(room))
        if ttf_w(text, size) <= room:
            return text
        # The longest start of text that fits with ".." after it (at least two
        # characters), found by halving.
        lo, hi = 2, len(text) - 1             # text[:lo] is kept even if it doesn't fit
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if ttf_w(text[:mid] + "..", size) <= room:
                lo = mid
            else:
                hi = mid - 1
        return text[:lo].rstrip() + ".."


    def ttf_w(text, size):
        """Width of text in the smooth font at `size` (the scale is part of the key:
        a label's real size depends on it, so a scale change never reads stale widths)."""
        return measure(_ttf_widths, (text, size, view["scale"]),
                       lambda: G.CreateGumpTTFLabel(text, max(6, sc(size)), STONE_TEXT),
                       int(0.55 * size * len(text)))


    def art_w(art):
        """Width of a button's art, in layout units."""
        gw = art_size(art[0])[0] if art_ok() else 0
        return int(round((gw or 30) / view["scale"]))


    def button(x, y, w, h, text, tooltip, fn, active=False, size=14, parent=None, color=None,
               art=None):
        """A standard gump button with its caption beside it.
        The caption is clickable too."""
        parent = parent or gump
        if color is None:
            color = STONE_TEXT
        c = tgt["ctrls"]
        if art_ok():
            if art is None:
                art = (GEM_ON, GEM_ON, GEM_ON) if active else Kit.ART_PLAY
            gw, gh = art_size(art[0])
            b = G.CreateGumpButton("", 0, art[0], art[1], art[2])
            b.SetPos(sc(x), sc(y) + max(0, (sc(h) - gh) // 2))
            put(parent, b, c)
            on_click(b, fn)
            if tooltip:
                safe(lambda: b.SetTooltip(tooltip))
            if text:
                lx = x + int(round(gw / view["scale"])) + 4
                label(parent, text, lx, y + (h - size) // 2 - 1, size, color, c)
                hit = box(parent, lx, y, max(4, x + w - lx), h, COL_ROW, 0.0, c)
                on_click(hit, fn)
                if tooltip:
                    hit.SetTooltip(tooltip)
            return b
        b = box(parent, x, y, w, h, COL_GOLD if active else COL_ROW, 0.85 if active else 0.4, c)
        label(parent, text, x, y + (h - size) // 2 - 1, size, COL_BG if active else color, c,
              width=w, align="center")
        on_click(b, fn)
        if tooltip:
            b.SetTooltip(tooltip)
        return b


    def dock_wish():
        """Folded into the Action Bar by the player's choice (kept per character)."""
        return bool(safe(lambda: HOST.dock_wanted(DOCK_KEY), False))


    def set_dock_wish(on):
        safe(lambda: HOST.dock_want_set(DOCK_KEY, on))


    def bar_alive():
        return bool(safe(HOST.bar_alive, False))


    def min_click():
        """Minimize / Restore from the window itself: the title strip, never
        the Action Bar (the gold arrow is for that). Runs on the tick (the
        buttons and the title strip queue ("min_click",), see run_ui_action)."""
        set_dock_wish(False)
        toggle_min()


    def fold_to_bar():
        """The gold arrow / the bar's Grimoire button: minimized and hidden in
        the bar, or (no bar up) minimized until the bar comes."""
        set_dock_wish(True)
        if not state["minimized"]:
            toggle_min()
        if bar_alive():
            set_docked(True)
        else:
            HOST.dock_note("Grimoire")


    def toggle_min():
        state["minimized"] = not state["minimized"]
        if state["minimized"]:
            gump.SetResizable(False)
            gump.SetHeight(sc(TITLE_H))
        else:
            gump.SetHeight(win["h"])
            gump.SetResizable(True)
        set_docked(False)              # a click on the strip unfolds it
        save_int("Min", 1 if state["minimized"] else 0)   # kept for the next start
        state["dirty"] = True


    def save_window_pos():
        """Where the window is, saved the moment you let go of it."""
        try:
            x, y = int(gump.GetX()), int(gump.GetY())
        except Exception:
            return
        loop["last_pos"] = (x, y)
        save_int("X", x)
        save_int("Y", y)


    def set_docked(on):
        """Folded into the Action Bar: the whole window is hidden (not saved)."""
        on = bool(on)
        if on == state["docked"]:
            return
        state["docked"] = on
        try:
            gump.IsVisible = not on
        except Exception:
            try:
                clr_prop(gump, "IsVisible").SetValue(gump, not on, None)
            except Exception:
                state["docked"] = False       # can't hide it: stay minimized


    def link_tick():
        """Commands from the Action Bar, and this window's state for it
        (shared variables, read every 0.1 s)."""
        now = time.time()
        if now < state.get("link_next", 0.0):
            return
        state["link_next"] = now + 0.1
        if state.pop("to_bar", False):            # the gold arrow was clicked
            fold_to_bar()
        try:                                      # (every 0.1 s: plain try/except, no lambda)
            cmd = API.GetSharedVar(LINK_CMD)
        except Exception:
            cmd = None
        if cmd:
            safe(lambda: API.RemoveSharedVar(LINK_CMD))
            cmd = str(cmd)
            if cmd == "show" and (state["minimized"] or state["docked"]):
                set_dock_wish(False)
                if state["minimized"]:
                    toggle_min()                  # also undocks
                set_docked(False)
            elif cmd == "dock" and not state["docked"]:
                fold_to_bar()
        if state["docked"]:
            if not bar_alive():
                set_docked(False)                 # bar gone: show the title strip (wish kept)
        elif state["minimized"] and now >= state.get("wish_next", 0.0):
            state["wish_next"] = now + 0.25       # folded in by choice: back into the bar
            if dock_wish() and bar_alive():
                set_docked(True)
        elif not state["minimized"] and now >= state.get("wish_next", 0.0):
            state["wish_next"] = now + 1.0
            if dock_wish():
                set_dock_wish(False)              # shown again: no longer folded
        ls = "docked" if state["docked"] else ("minimized" if state["minimized"] else "open")
        if ls != state["link_state"]:
            state["link_state"] = ls
            safe(lambda: API.SetSharedVar(LINK_STATE, ls))


    def on_opacity(value):
        win["opacity"] = int(value)
        for p, factor in bg_box["parts"]:
            safe(lambda: p.SetAlpha(win["opacity"] / 100.0 * factor))
        save_int("Opacity", win["opacity"])


    def on_scale(value):
        pending_scale["value"] = int(value)
        pending_scale["t"] = time.time()


    def rescale(new, save):
        """The window drawn at scale `new` (0.6 .. 1.5), its size scaled with it
        so everything keeps its proportions; `save` keeps it as your setting
        (never while the layout fits the window to a zone: see layout_fit)."""
        if abs(new - view["scale"]) < 0.001:
            return
        ratio = new / view["scale"]
        view["scale"] = new
        win["w"], win["h"] = int(round(win["w"] * ratio)), int(round(win["h"] * ratio))
        own_w, own_h = win["w"], win["h"]     # your size at this scale (saved below)
        fit_screen()                          # 2.6.81 (GR-5): a big scale stays on the screen
        try:
            gump.SetWidth(win["w"])
            gump.SetHeight(sc(TITLE_H) if state["minimized"] else win["h"])
        except Exception:
            pass
        if save:
            save_int("Scale", int(round(new * 100)))
            save_int("W", own_w)
            save_int("H", own_h)
        state["dirty"] = True


    def apply_scale():
        """The Scale slider settled: your scale. While the window is fitted to a
        zone the fit stays on screen; your choice is kept for when it is freed
        (and a shrink-only zone is told, since it caps at your scale)."""
        value = pending_scale["value"]
        pending_scale["value"] = None
        new = min(SCALE_MAX, max(SCALE_MIN, value)) / 100.0
        if fitst["own"] is None:
            rescale(new, True)
            return
        if abs(new - fitst["own"][0]) < 0.001:
            return
        own_w = int(round(fitst["own"][1] * new / fitst["own"][0]))
        own_h = int(round(fitst["own"][2] * new / fitst["own"][0]))
        rescale(new, False)              # (2.6.56) your scale, in the slot's size (run_fit)
        fitst["own"] = (new, own_w, own_h)
        save_int("Scale", int(round(new * 100)))
        save_int("W", own_w)
        save_int("H", own_h)
        if fitst["told"] is not None:
            state["ui_queue"].append(("fit",) + fitst["told"])


    # ---------- the layout's zone fit (2.6.55) ----------
    #  Told by the mother's layout (hooks "fit") when the window sits in a zone:
    #  (2.6.56) the window is made exactly its slot's size, at your own scale (the
    #  spells lay out for the size, as after a drag of its corner); your size is
    #  kept (fitst["own"]) and comes back when it is freed.
    #  The call comes on the client thread in the keeper's pass: it only queues.
    fitst = {"own": None,        # (scale, w, h) of your own setting while fitted
             "told": None}       # the (w, h, mode) last told, for a repeat after a slider move


    def layout_fit(w, h, mode):
        fitst["told"] = (w, h, mode) if w else None
        state["ui_queue"].append(("fit", w, h, mode))


    def run_fit(w, h, mode):
        """On the tick: the window made its slot's size, or your own size again."""
        if not w:
            own, fitst["own"] = fitst["own"], None
            if own is not None:
                view["scale"] = own[0]
                win["w"], win["h"] = own[1], own[2]
                fit_screen()                     # 2.6.81 (GR-5): freed on today's screen
                try:
                    gump.SetWidth(win["w"])
                    gump.SetHeight(sc(TITLE_H) if state["minimized"] else win["h"])
                except Exception:
                    pass
                state["dirty"] = True
            return
        if fitst["own"] is None:
            fitst["own"] = (view["scale"], win["w"], win["h"])
        # (2.6.56) exactly the slot's size, at your own scale: the spells lay out for it
        w, h = int(w), int(h)
        if state["minimized"]:
            h = win["h"]                 # its bar: the slot's width; the height comes back
        if (win["w"], win["h"]) != (w, h):
            win["w"], win["h"] = w, h
            try:
                gump.SetWidth(w)
                gump.SetHeight(sc(TITLE_H) if state["minimized"] else h)
            except Exception:
                pass
            state["dirty"] = True


    CONTENT_Y = 50               # below the title section (12 + 30 + 8)
    BOTTOM_H = 48                # status section and the frame under the content


    def build_chrome():
        """Stone frame, title section and its buttons. Returns the y below it."""
        w = LW()
        h = TITLE_H if state["minimized"] else LH()
        c = tgt["ctrls"]
        op = win["opacity"] / 100.0

        bg_box["parts"] = stone(gump, 0, 0, w, h, c, op)
        frame = [p for p, _f in bg_box["parts"]]
        bg_box["parts"] += parchment(gump, 12, 12, w - 24, 30, c, op)
        if not state["minimized"]:
            frame += corner_knots(w, h, c) or []
            bg_box["parts"] += parchment(gump, 12, h - 40, w - 24, 28, c, op)    # status
        # (2.6.72) its stone frame and knots are the window's frame: "Join zone windows
        # in one frame" hides them like any Kit window's; the title row is the standard one
        try:
            Kit._frame_parts[gump] = frame
            Kit.note_title(gump, sc(12))
            if safe(lambda: HOST.layout_unified(DOCK_KEY), False):
                Kit.hide_zone_frame(gump)
        except Exception:
            pass
        label(gump, "GRIMOIRE", 42, 18, 14, STONE_GOLD, c)
        left = w - 12 - 44 - 20 - (0 if state["minimized"] else Kit.DOCK_DX + 106 + 98)
        # (every handler only queues: the tick is the one place the window changes)
        c.append(Kit.title_catcher(gump, sc(12), sc(12), sc(left - 16), sc(30),
                                   queue_ui(("min_click",)),
                                   key="grimoire:mini" if state["minimized"] else "grimoire"))

        # Title-bar buttons, right to left: close, minimize, fold, settings, refresh
        x = w - 12 - 44
        zoned = Kit.zone_up(DOCK_KEY)              # (2.6.85) a window in a zone is always up
        if not zoned:
            button(x, 15, 30, 24, "", "Close Grimoire (turns it off; the Modules tab turns it back on)",
                   queue_ui(("close",)), art=Kit.ART_CLOSE)
            x -= 20
            button(x, 15, 16, 24, "",
                   "Restore" if state["minimized"] else "Minimize (double-click the title does too)",
                   queue_ui(("min_click",)), art=Kit.ART_RESTORE if state["minimized"] else Kit.ART_MIN)
        if not state["minimized"]:
            if not zoned:
                x -= Kit.DOCK_DX                   # gold arrow: fold into the Action Bar
                button(x, 15, 16, 24, "", Kit.DOCK_TIP,
                       lambda: state.__setitem__("to_bar", True), art=Kit.ART_DOCK)
            x -= 106
            button(x, 15, 100, 24, "Settings", "Open the Grimoire settings page",
                   queue_ui(("settings",)), art=Kit.ART_PAGE)
            x -= 98
            button(x, 15, 92, 24, "Refresh",
                   "Find your spellbook and runebooks again and read every runebook afresh",
                   queue_action(("refresh",)), art=Kit.ART_OK)
        return CONTENT_Y


    def content_right():
        """Right edge of the main content; the supplies panel sits beyond it."""
        return LW() - SIDE_W - 20


    def tab_on():
        """Alpha of the active tab's highlight."""
        return 1.0 if art_ok() else 0.6


    def is_book_key(key):
        """A tab / page key that is a runebook (its serial), not "spells", "favs"
        or a spell circle's ("spells", n)."""
        return key not in ("spells", "favs", "+add") and not isinstance(key, tuple)


    def book_low(serial):
        """A runebook with fewer than LOW_CHARGES charges (known charges only)."""
        cur = book_charges.get(serial, (None, None))[0]
        return cur is not None and cur < LOW_CHARGES


    def tab_tip(key, title, short):
        """A tab's tooltip: its full name when cut short, and a low book's charges."""
        tip = title if short != title else None
        if is_book_key(key) and book_low(key):
            cur = book_charges[key][0]
            tip = "%s: %d charge%s left (low)" % (title, cur, "" if cur == 1 else "s")
        return tip


    def tab_button(key, x, y, w, h, text, tooltip, title=None):
        """A tab whose highlight (a pressed gem, or a gold fill) turns on/off without redrawing.
        A runebook's tab is red while the book is low on charges (recolor_tab)."""
        c = tgt["ctrls"]
        on = state["tab"] == key
        color = COL_EMPTY if is_book_key(key) and book_low(key) else STONE_TEXT
        if art_ok():
            gw, gh = art_size(GEM)
            gx, gy = sc(x), sc(y) + max(0, (sc(h) - gh) // 2)
            pic_px(gump, GEM, gx, gy, gw, gh, c)
            mark = pic_px(gump, GEM_ON, gx, gy, gw, gh, c)
            mark.SetAlpha(tab_on() if on else 0.0)
            lbl = label(gump, text, x + int(round(gw / view["scale"])) + 4, y + (h - 14) // 2 - 1,
                        14, color, c)
            b = box(gump, x, y, w, h, COL_ROW, 0.0, c)
        else:
            b = box(gump, x, y, w, h, COL_ROW, 0.4, c)
            mark = box(gump, x, y, w, h, COL_GOLD, tab_on() if on else 0.0, c)
            lbl = label(gump, text, x, y + (h - 14) // 2 - 1, 14, color, c, width=w,
                        align="center")
        fn = queue_switch(key)
        on_click(b, fn)
        on_click(mark, fn)
        if tooltip:
            b.SetTooltip(tooltip)
            mark.SetTooltip(tooltip)
        tab_marks[key] = mark
        if is_book_key(key):
            tab_parts[key] = (lbl, b, mark, title or text, text, color == COL_EMPTY)


    def recolor_tab(serial):
        """A runebook's tab turns red (or back) when its charges cross LOW_CHARGES:
        in place, or with a redraw when the label can't be recoloured."""
        parts = tab_parts.get(serial)
        low = book_low(serial)
        if parts is None or parts[5] == low:
            return
        lbl, b, mark, title, short, _ = parts
        if not set_label_hue(lbl, TEXT_HUES[COL_EMPTY if low else STONE_TEXT]):
            state["dirty"] = True
            return
        tab_parts[serial] = (lbl, b, mark, title, short, low)
        tip = tab_tip(serial, title, short) or title
        try:
            b.SetTooltip(tip)
            mark.SetTooltip(tip)
        except Exception:
            pass


    def queue_switch(key):
        def cb():
            state["switch"] = key
        return cb


    def build_tabs(top):
        """Tab strip in its own section; wraps to more rows if you carry many
        runebooks. Returns content top y."""
        tabs = [("spells", "Spellbook")] + ([("favs", "Favourites")] if runebooks else []) + \
            [(b["serial"], b["title"]) for b in runebooks]
        right = content_right()
        row_h = 28
        # where every tab goes (the section behind them is drawn first)
        places, x, y = [], 20, top + 4
        aw = art_w(Kit.ART_OK)
        for key, title in tabs:
            short = title if len(title) < 18 else title[:16] + ".."
            w = max(90, aw + 4 + text_w(short) + 14)
            if x + w > right - 4:
                x, y = 20, y + row_h
            places.append((key, title, short, x, y, w))
            x += w + 6
        # "Add runebook..." is pinned to the right end of the strip, never where a tab
        # will be, and only once the first scan is done (before that the strip is
        # still filling in, and a click meant for a tab could land on it).
        if state["scanned"]:
            title = "Add runebook..."
            w = max(90, aw + 4 + text_w(title) + 14)
            ax = right - 4 - w
            if x > ax:                       # no room left on this row: its own row
                y += row_h
            places.append(("+add", title, title, ax, y, w))
        tabs_bottom = y + row_h + 2
        op = win["opacity"] / 100.0
        bg_box["parts"] += parchment(gump, 12, top, right - 12, tabs_bottom - top, tgt["ctrls"], op)
        for key, title, short, x, y, w in places:
            if key == "+add":
                button(x, y, w, 24, short,
                       "Target a runebook that isn't listed; books of its kind are found from then on",
                       queue_action(("register",)), art=Kit.ART_OK)
            elif key == "favs":
                tab_button(key, x, y, w, 24, short, "Your starred destinations, your last trip "
                           "and a search of every runebook you carry")
            else:
                tab_button(key, x, y, w, 24, short, tab_tip(key, title, short), title)
        top = tabs_bottom + Kit.GAP
        # the section behind the tab pages
        bg_box["parts"] += parchment(gump, 12, top, right - 12, LH() - BOTTOM_H - top,
                                     tgt["ctrls"], op)
        state["content_top"] = top + 4
        return top + 4


    def scroll_area(x, y, w, h):
        """A scroll area that isn't on the window yet: fill it, then attach() it, so its
        rows appear all at once instead of one by one from the top."""
        sa = G.CreateGumpScrollArea(sc(x), sc(y), sc(w), sc(max(40, h)))
        tgt["ctrls"].append(sa)
        return sa


    def attach(ctrl):
        on_window(gump, ctrl)
        gump.Add(ctrl)


    def build_supplies(top):
        """Right-hand panel: total reagents and travel scrolls carried."""
        c = tgt["ctrls"]
        x0 = LW() - SIDE_W - 12
        bottom = LH() - BOTTOM_H
        bg_box["parts"] += parchment(gump, x0, top, SIDE_W, bottom - top, c, win["opacity"] / 100.0)
        label(gump, "Supplies", x0, top + 8, 15, COL_HEAD, c, width=SIDE_W, align="center")

        rows = [REAGENTS[a] for a in REAGENT_ORDER]
        rows += [None, ("Recall scroll", RECALL_SCROLL), ("Gate scroll", GATE_SCROLL)]
        rh, pic = 40, 34
        need = sum(10 if r is None else rh for r in rows)
        y0 = top + 32
        if y0 + need <= bottom:
            parent, ox, oy, sa = gump, x0, y0, None
        else:                                        # short window: let the panel scroll
            sa = scroll_area(x0 + 2, y0, SIDE_W - 2, bottom - y0 - 4)
            parent, ox, oy = sa, 0, 0

        totals = supply_counts()
        y = oy
        for r in rows:
            if r is None:
                box(parent, ox + 10, y + 4, SIDE_W - 20 - (16 if sa else 0), 1, COL_DIM, 0.6, c)
                y += 10
                continue
            name, graphic = r
            item_pic(parent, graphic, ox + 8, y + (rh - pic) // 2, pic, c)
            n = totals.get(graphic, 0)
            cnt = label(parent, count_text(n), ox + 48, y + 3, 15, COL_TEXT if n else COL_EMPTY, c)
            tgt["counts"].append(count_entry(graphic, cnt, n))
            room = SIDE_W - 52 - (16 if sa else 0)
            label(parent, fit(name, room), ox + 48, y + 21, 12, COL_TEXT, c)
            y += rh
        if sa is not None:
            attach(sa)


    def build_spell_page(top, circle):
        c = tgt["ctrls"]
        right = content_right()
        # Circle selector, with the circle's name to the right of it
        x = 22
        cw, ch = art_size(CIRCLE_ART) if art_ok() else (0, 0)
        for i, r in enumerate(ROMAN):
            if cw and ch:
                # The spellbook's own circle tabs, scaled to a 30px-high row
                h = 30
                w = max(1, cw * h // ch)
                p = pic_px(gump, CIRCLE_ART + i, sc(x), sc(top + 2), sc(w), sc(h), c, mouse=True)
                if circle != i:
                    p.SetAlpha(0.45)
                on_click(p, pick_circle(i))
                safe(lambda: p.SetTooltip(CIRCLES[i][0]))
                x += w + 6
            else:
                button(x, top + 4, 48, 26, r, CIRCLES[i][0], pick_circle(i),
                       active=circle == i)
                x += 52
        title, spells = CIRCLES[circle]
        label(gump, title, x + 10, top + 6, 18, COL_HEAD, c)
        top += 38

        if not spellbook_serial:
            label(gump, "No spellbook in your pack or hands. Carry one, then click Refresh.",
                  22, top + 4, 14, COL_DIM, c)
            return

        sa = scroll_area(16, top, right - 20, LH() - top - BOTTOM_H - 4)
        rh = SPELL_ROW_H
        totals = supply_counts()
        base = circle * 8
        row_w = right - 34
        text_x = SPELL_ICON + 18
        reg_x0 = row_w - 4 * REG_SLOT - 6          # reagent block, right-aligned (max 4 reagents)
        mana = loop["mana"]
        for i, (name, desc, regs) in enumerate(spells):
            y = i * rh
            owned = known_spells is None or norm(name) in known_spells
            key = ("spell", name)
            bg = box(sa, 0, y, row_w, rh - 4, COL_ROW, ROW_A, c)
            row_bgs[key] = bg
            # a spell you can't cast right now (a reagent at 0, too little mana)
            # is dimmed; refresh_castable follows your counts and mana in place
            entry = [name, [REAGENTS[a][1] for a in regs.split()], SPELL_MANA[circle], None,
                     None, bg, None]
            if owned:
                entry[6] = cast_state(entry, totals, mana)
            dim = owned and entry[6][0]

            icon = G.CreateGumpPic(SPELL_ICON_BASE + base + i, sc(8), sc(y + (rh - 4 - SPELL_ICON) // 2),
                                   0 if owned else 0x3B2)
            icon.SetWidth(sc(SPELL_ICON))      # GumpPic stretches its art to its size
            icon.SetHeight(sc(SPELL_ICON))
            icon.SetAcceptMouseInput(False)
            if dim:
                icon.SetAlpha(DIM_ICON)
            sa.Add(icon)
            c.append(icon)

            entry[3] = label(sa, name, text_x, y + 14, 17,
                             (STONE_DIM if dim else COL_TEXT) if owned else COL_MUTED, c)
            entry[4] = icon
            label(sa, desc if owned else desc + "  (not in your book)", text_x, y + 38, 13,
                  COL_DIM if owned else COL_MUTED, c, width=max(120, reg_x0 - text_x - 8))

            # Reagents: picture, carried count, full name - side by side
            reg_list = regs.split()
            sx = row_w - len(reg_list) * REG_SLOT - 6
            for abbr in reg_list:
                full, graphic = REAGENTS[abbr]
                pic = item_pic(sa, graphic, sx + (REG_SLOT - REG_PIC) // 2, y + 2, REG_PIC, c)
                if not owned:
                    pic.SetAlpha(0.4)
                n = totals.get(graphic, 0)
                cnt = label(sa, count_text(n), sx, y + REG_PIC + 3, 13,
                            (COL_TEXT if n else COL_EMPTY) if owned else COL_MUTED, c,
                            width=REG_SLOT, align="center")
                tgt["counts"].append(count_entry(graphic, cnt, n, owned))
                label(sa, full, sx, y + REG_PIC + 20, 11, COL_DIM if owned else COL_MUTED, c,
                      width=REG_SLOT, align="center")
                sx += REG_SLOT
            if owned:
                bind_row(bg, key, ("cast", name))
                bg.SetTooltip(cast_tip(entry))
                tgt["spells"].append(entry)
        attach(sa)


    DIM_ICON = 0.45                     # a dimmed spell's icon (can't cast it right now)
    REG_NAMES = dict((g_, n) for n, g_ in REAGENTS.values())    # graphic -> reagent name
    SPELL_MANA = tuple(getattr(Kit, "SPELL_MANA", None) or (4, 6, 9, 11, 14, 20, 40, 50))


    def cast_state(entry, totals, mana):
        """(dim, why) of a spell row: a reagent it needs at 0 in the supplies
        counts, or less mana than its circle takes (Kit.SPELL_MANA)."""
        for g_ in entry[1]:
            if totals.get(g_, 0) <= 0:
                return (True, "Out of " + REG_NAMES.get(g_, "a reagent"))
        if mana is not None and mana < entry[2]:
            return (True, "Not enough mana (it takes %d)" % entry[2])
        return (False, "")


    def cast_tip(entry):
        tip = "Double-click to cast " + entry[0]
        if entry[6] is not None and entry[6][0]:
            tip += "\n" + entry[6][1]
        return tip


    def refresh_castable():
        """Dim / undim the spell rows of every built page whose state changed
        (called when the supplies counts change and when your mana crosses a
        circle's cost): only those rows are touched, in place."""
        totals = loop["totals"]
        if totals is None:
            return
        mana = loop["mana"]
        for pg in list(pages.values()):
            for e in pg["spells"]:
                now = cast_state(e, totals, mana)
                if now == e[6]:
                    continue
                e[6] = now
                dim = now[0]
                set_label_hue(e[3], TEXT_HUES[STONE_DIM if dim else COL_TEXT])
                try:
                    e[4].SetAlpha(DIM_ICON if dim else 1.0)
                    e[5].SetTooltip(cast_tip(e))
                except Exception:
                    pass


    def mana_tick(now):
        """Your mana, every MANA_EVERY while a spell page shows (one read, in
        place on the client thread): the rows follow only when it crosses a
        circle's cost."""
        if (now < loop["next_mana"] and loop["next_mana"] - now <= MANA_EVERY) \
                or state["tab"] != "spells" or state["minimized"] \
                or state["docked"]:
            return
        loop["next_mana"] = now + MANA_EVERY
        try:
            mana = int(API.Player.Mana)
        except Exception:
            mana = None
        tier = None
        if mana is not None:
            tier = 0
            for m in SPELL_MANA:
                if m <= mana:
                    tier += 1
        loop["mana"] = mana
        if tier != loop["tier"]:
            loop["tier"] = tier
            refresh_castable()


    def charges_text(serial):
        cur, mx = book_charges.get(serial, (None, None))
        if cur is None:
            return None, 1
        if mx is None:
            return "Charges: %d" % cur, cur
        return "Charges: %d / %d" % (cur, mx), cur


    def build_rune_page(top, serial):
        c = tgt["ctrls"]
        right = content_right()
        book = next((b for b in runebooks if b["serial"] == serial), None)
        if book is None:
            if serial == state["tab"]:
                state["switch"] = "spells"
            return
        label(gump, book["title"], 22, top + 2, RUNE_TITLE_SIZE, COL_HEAD, c, smooth=True)
        button(right - 104, top + 4, 96, 26, "Re-read", "Read this runebook again",
               queue_ui(("reread", serial)), size=15, art=Kit.ART_PAGE)

        if serial not in rune_cache:
            label(gump, "Reading this runebook", 22, top + 36, 14, COL_DIM, c)
            if serial in bg_reads:
                bg_reads.remove(serial)
            if ("read", serial) not in state["queue"]:
                state["queue"].append(("read", serial))
            return

        text, charges = charges_text(serial)
        if text:                                       # red at 0 and while low (LOW_CHARGES)
            label(gump, text, right - 340, top + 6, 20,
                  COL_HEAD if charges and not book_low(serial) else COL_EMPTY, c,
                  width=226, align="right", smooth=True)

        dests = rune_cache[serial]
        if dests is None or (not dests and serial in rune_errors):
            msg = rune_errors.get(serial, "Couldn't read this runebook.")
            label(gump, msg, 22, top + 36, 14, COL_EMPTY, c, width=right - 26)
            # 2.6.81 (GR-8): "saved" only when the dump file really holds this book
            label(gump, "Details were saved to Grimoire_runebook_dump.txt in your LegionScripts "
                        "folder; send that file over, then click Refresh to try again."
                  if serial in dump["books"] else
                  "Click Re-read to save this book's details to Grimoire_runebook_dump.txt in "
                  "your LegionScripts folder.",
                  22, top + 62, 12, COL_DIM, c, width=right - 26)
            return
        if not dests:
            label(gump, "No runes in this runebook. Add some, then click Re-read.", 22, top + 36,
                  14, COL_DIM, c)
            return

        totals = supply_counts()
        tgt["scrolls"] = scroll_flags(totals)          # redrawn when these change (refresh_counts)
        have_of = {"recall_scroll": totals.get(RECALL_SCROLL, 0),
                   "gate_scroll": totals.get(GATE_SCROLL, 0), "charge": charges}
        charges_known = book_charges.get(serial, (None, None))[0] is not None
        n = len(dests)
        any_std = any(d["slot"] is not None for d in dests)
        any_btn = any_std or any(d.get("rune") for d in dests)
        label(gump, "%d destination%s; double-click a name to %s there" %
              (n, "" if n == 1 else "s", DEFAULT_TRAVEL), 22, top + 36, RUNE_HEAD_SIZE,
              COL_DIM, c, smooth=True)

        # ---- columns: the travel methods, each as wide as its heading or the arrow ----
        aw = art_w(Kit.ART_PLAY)
        methods = []
        if any_btn:
            for m, head, tip in RUNE_METHODS:
                if m == "charge" and not any_std:
                    continue
                methods.append((m, head, tip, max(aw + 12, ttf_w(head, RUNE_HEAD_SIZE) + 12)))
        block_w = sum(m[3] for m in methods)

        # ---- how many destination columns fit, and how tall a row is ----
        head_y = top + 62                                  # column-heading row
        list_y = head_y + 26                               # the destinations start here
        row_w = right - 34                                 # inside the scroll area
        unit_min = RUNE_NAME_MIN + block_w + 16
        ncols = max(1, min(n, row_w // unit_min))
        unit_w = row_w // ncols
        name_w = unit_w - block_w - 20
        rows = (n + ncols - 1) // ncols
        avail_h = LH() - list_y - BOTTOM_H - 4
        rh = max(RUNE_ROW_MIN, min(RUNE_ROW_MAX, avail_h // max(1, rows)))
        # name text fills the row: its size follows the row height
        name_size = max(RUNE_NAME_MIN_SZ, int((rh - 4) * RUNE_NAME_FILL))
        line_h = int(name_size * 1.3)

        # ---- column headings, once, above the list (aligned with every destination column) ----
        for col in range(ncols):
            hx = 16 + col * unit_w + name_w + 16
            label(gump, "Destination", 16 + col * unit_w + 30, head_y, RUNE_HEAD_SIZE, COL_HEAD, c,
                  smooth=True)
            for m, head, tip, cw in methods:
                col_color = COL_HEAD if have_of.get(m, 1) else COL_EMPTY
                label(gump, head, hx, head_y, RUNE_HEAD_SIZE, col_color, c, width=cw, align="center",
                      smooth=True)
                hx += cw
        box(gump, 18, head_y + 23, row_w - 4, 1, COL_DIM, 0.5, c)

        # ---- the destinations: down each column, then the next column ----
        sa = scroll_area(16, list_y, right - 20, avail_h)
        stars = tgt["stars"]
        for i, dest in enumerate(dests):
            col, r = divmod(i, rows)
            x0, y = col * unit_w, r * rh
            key = ("rune", serial, dest["button"], dest["name"])
            bg = box(sa, x0, y, unit_w - 6, rh - 4, COL_ROW, ROW_A, c)
            row_bgs[key] = bg
            standard = dest["slot"] is not None
            rune_bag = bool(dest.get("rune"))
            bind_row(bg, key, ("travel", serial, dest, default_method(dest)))
            bg.SetTooltip("Double-click to %s to %s" % (DEFAULT_TRAVEL, dest["name"]))
            # the star: click to list the destination in Favourites (again: off)
            stars[i] = star(sa, x0 + 8, y + max(0, (rh - 4 - 14) // 2),
                            (serial, i) in favs["keys"], c)
            hit = box(sa, x0 + 2, y, 26, rh - 4, COL_ROW, 0.0, c)
            on_click(hit, queue_ui(("star", serial, i, dest["name"])))
            hit.SetTooltip(STAR_TIP)
            ty = y + max(0, (rh - 4 - line_h) // 2)
            if not (standard or rune_bag):
                # custom book layout: double-click presses the rune's own button
                label(sa, fit(dest["name"], unit_w - 46, name_size), x0 + 30, ty,
                      name_size, COL_TEXT, c, smooth=True)
                continue
            label(sa, fit(dest["name"], name_w - 24, name_size), x0 + 30, ty,
                  name_size, COL_TEXT, c, smooth=True)
            bx = x0 + name_w + 16
            for m, head, tip, cw in methods:
                if m == "charge" and not standard:
                    bx += cw
                    continue
                have = have_of.get(m, 1)
                full_tip = tip
                if m in ("recall_scroll", "gate_scroll"):
                    full_tip += " (%d carried)" % have
                elif m == "charge" and charges_known:   # 2.6.81 (GR-9): not the placeholder 1
                    full_tip += " (%d left)" % have
                b = button(bx + (cw - aw) // 2, y + 2, aw, rh - 8, "", full_tip,
                           queue_stamped(("travel", serial, dest, m)), parent=sa)
                if not have:
                    safe(lambda b=b: b.SetAlpha(0.35))        # nothing to use it with
                bx += cw
        attach(sa)


    def default_method(dest):
        """What a double-click on a destination does: DEFAULT_TRAVEL, or the
        rune's own button (a charge) in a book of an unknown layout."""
        return DEFAULT_TRAVEL if dest["slot"] is not None or dest.get("rune") else "charge"


    # ---- the Favourites page (GR1 search, GR2 favourites and the last trip) ----
    FAV_ROW_H = 30               # a row of the Favourites page (layout units)
    STAR_TIP = "Put this destination in Favourites (click again to take it off)"   # every star
    METHOD_VERB = {"recall": "recall", "gate": "gate", "charge": "recall (a charge)",
                   "recall_scroll": "recall (a scroll)", "gate_scroll": "gate (a scroll)",
                   "sacred": "travel (Sacred Journey)"}


    def build_fav_page(top):
        """The page's title, its search box and info line, and its rows (a pool
        of FAV_ROW_H rows in a scroll area, filled by fav_render and from then
        on reassigned in place as you type or as the lists change)."""
        c = tgt["ctrls"]
        right = content_right()
        label(gump, "Favourites", 22, top + 2, RUNE_TITLE_SIZE, COL_HEAD, c, smooth=True)
        sw = 220
        sx = right - 8 - sw
        cap = "Search:"
        label(gump, cap, sx - 10 - text_w(cap), top + 8, 14, COL_TEXT, c)
        tiled_px(gump, Kit.FIELD_TILE, sc(sx) - 2, sc(top + 4) - 1, sc(sw) + 4, 24, c)
        tb = G.CreateGumpTextBox(fav_ui["text"], sc(sw), 22, False, 16)
        tb.SetPos(sc(sx), sc(top + 4))
        try:
            tb.SetTooltip("Type part of a rune's or runebook's name to search every runebook "
                          "you carry (empty: your Favourites)")
        except Exception:
            pass
        put(gump, tb, c)
        info = label(gump, "", 22, top + 38, 14, COL_DIM, c)
        list_y = top + 62
        row_w = right - 34
        sa = scroll_area(16, list_y, right - 20, LH() - list_y - BOTTOM_H - 4)
        fav_ui.update({"layer": tgt, "tb": tb, "info": info, "sa": sa, "pool": [],
                       "seen": None, "ver": -1, "row_w": row_w,
                       "name_w": max(120, int(row_w * 0.55)), "info_w": right - 30})
        fav_render(building=True)             # (build_page files the layer once it is drawn)
        attach(sa)


    def fav_rows():
        """What the Favourites page lists: (rows, info line), rows being
        (book serial, index, name, book title, method or None, last trip?).
        A search (the box's text, every word in the rune's or the book's
        name) lists every carried runebook's destinations; an empty box the
        last trip and the starred destinations, in tab order. From the saved
        lists only: no book is read."""
        titles, order = {}, []
        for b in runebooks:
            titles[b["serial"]] = b["title"]
            order.append(b["serial"])
        if not order:
            return [], "No runebooks found in your pack or hands."
        q = fav_ui["text"].strip().lower()
        rows = []
        if q:
            words = q.split()
            more = False
            for s in order:
                lst = rune_cache.get(s) or ()
                tl = titles[s].lower()
                for i in range(len(lst)):
                    hay = lst[i]["name"].lower() + "  " + tl
                    for wd in words:
                        if wd not in hay:
                            break
                    else:
                        if len(rows) >= SEARCH_MAX:
                            more = True
                            break
                        rows.append((s, i, lst[i]["name"], titles[s], None, False))
                if more:
                    break
            if more:
                return rows, "More than %d found; type more letters." % SEARCH_MAX
            if rows:
                return rows, "%d destination%s found; double-click one to %s there" % (
                    len(rows), "" if len(rows) == 1 else "s", DEFAULT_TRAVEL)
            return rows, "No rune or runebook name has '%s' in it." % fav_ui["text"].strip()
        last = favs["last"]
        if last is not None and last[0] in titles:
            i = resolve(last[0], last[1], last[2])
            if i is not None:
                rows.append((last[0], i, last[2], titles[last[0]], last[3], True))
        by_book = {}
        for f in favs["list"]:
            by_book.setdefault(f[0], []).append(f)
        away = 0
        for s in list(by_book):
            if s not in titles:
                away += len(by_book.pop(s))
        n = 0
        for s in order:
            for f in sorted(by_book.get(s, ()), key=lambda f: f[1]):
                i = resolve(s, f[1], f[2])
                if i is None:
                    away += 1
                    continue
                rows.append((s, i, f[2], titles[s], None, False))
                n += 1
        if n:
            info = "%d favourite%s; double-click one to %s there, or type above to search" % (
                n, "" if n == 1 else "s", DEFAULT_TRAVEL)
        else:
            info = "Click the star by a destination on a runebook's page to list it here."
        if away:
            info += "  (%d not in the books you carry)" % away
        return rows[:SEARCH_MAX + 1], info


    def fav_render(building=False):
        """Fill the Favourites page's rows from fav_rows, in place: a row gets a
        new destination by having its texts, star and tooltip set (only what
        changed is written); rows beyond the list are hidden. New rows are made
        only when the list is longer than any before (at most SEARCH_MAX + 1)."""
        ui = fav_ui
        layer = ui["layer"]
        if layer is None or (pages.get("favs") is not layer and not building):
            ui["layer"] = None                    # the page went (a redraw): nothing to fill
            return
        rows, info = fav_rows()
        ui["ver"], ui["seen"] = lists["ver"], ui["text"]
        Kit.set_text(ui["info"], fit(info, ui["info_w"]), TEXT_HUES[COL_DIM])
        pool = ui["pool"]
        for i in range(len(rows)):
            if i >= len(pool):
                pool.append(new_fav_slot(i, rows[i]))
            if not fav_assign(pool[i], rows[i]):
                state["fav_redraw"] = True        # a star couldn't be recoloured: redraw
        for i in range(len(rows), len(pool)):
            fav_assign(pool[i], None)


    def new_fav_slot(i, row):
        """Row i of the Favourites page (made once, then reassigned)."""
        ui = fav_ui
        sa, track, rh = ui["sa"], ui["layer"]["ctrls"], FAV_ROW_H
        y = i * rh
        slot = {"i": i, "a": None, "prev": None, "at": 0.0, "tip": None, "shown": True}
        slot["bg"] = box(sa, 0, y, ui["row_w"], rh - 4, COL_ROW, ROW_A, track)
        row_bgs[("fav", i)] = slot["bg"]
        slot["on"] = (row[0], row[1]) in favs["keys"]
        slot["star"] = star(sa, 8, y + (rh - 4 - 14) // 2, slot["on"], track)
        slot["hit"] = box(sa, 2, y, 26, rh - 4, COL_ROW, 0.0, track)
        slot["hit"].SetTooltip(STAR_TIP)
        slot["name"] = label(sa, "", 32, y + (rh - 4 - 14) // 2 - 2, 14, COL_TEXT, track)
        slot["book"] = label(sa, "", 32 + ui["name_w"] + 10, y + (rh - 4 - 14) // 2 - 2, 14,
                             COL_DIM, track)
        on_click(slot["hit"], fav_star_click(slot))
        on_click(slot["bg"], fav_row_click(slot))
        hook_double_click(slot["bg"], fav_row_double(slot))
        return slot


    def fav_show(slot, shown):
        """Show / hide a pooled row (hidden: not in the list now). Without
        hiding (an old client) the row is blanked instead."""
        slot["shown"] = shown
        ctrls = [slot["bg"], slot["hit"], slot["name"], slot["book"]] + slot["star"]
        for ctl in ctrls:
            if not set_shown(ctl, shown):
                break
        else:
            return
        try:
            slot["bg"].SetAlpha(ROW_A if shown else 0.0)
            for p in slot["star"]:
                p.SetAlpha(1.0 if shown else 0.0)
        except Exception:
            pass
        if not shown:
            Kit.set_text(slot["name"], "")
            Kit.set_text(slot["book"], "")


    def fav_assign(slot, row):
        """Give a pooled row its destination (None: hide it). False if its star
        had to change colour and couldn't."""
        if row is None:
            if slot["a"] is not None:
                slot["prev"], slot["at"], slot["a"] = slot["a"], time.time(), None
            if slot["shown"]:
                fav_show(slot, False)
            return True
        a = (row[0], row[1], row[2], row[4], row[5])
        if slot["a"] != a:
            slot["prev"], slot["at"], slot["a"] = slot["a"], time.time(), a
        if not slot["shown"]:
            fav_show(slot, True)
        ui = fav_ui
        Kit.set_text(slot["name"], fit(("Last: " if row[5] else "") + row[2], ui["name_w"] - 4),
                     TEXT_HUES[COL_TEXT])
        book = row[3] + ((", " + METHOD_VERB.get(row[4], row[4])) if row[4] else "")
        Kit.set_text(slot["book"], fit(book, ui["row_w"] - ui["name_w"] - 46), TEXT_HUES[COL_DIM])
        ok = True
        on = (row[0], row[1]) in favs["keys"]
        if on != slot["on"]:
            ok = recolor_star(slot["star"], on)
            slot["on"] = on
        lst = rune_cache.get(row[0]) or ()
        m = row[4] or (default_method(lst[row[1]]) if row[1] < len(lst) else DEFAULT_TRAVEL)
        tip = "Double-click to %s to %s (%s)" % (METHOD_VERB.get(m, m), row[2], row[3])
        if tip != slot["tip"]:
            slot["tip"] = tip
            try:
                slot["bg"].SetTooltip(tip)
            except Exception:
                pass
        return ok


    def fav_pick(slot):
        """The destination a click on a pooled row means: the one it shows, or
        the one it showed a moment ago when the list changed under the click."""
        if slot["prev"] is not None and time.time() - slot["at"] < 0.15:
            return slot["prev"]
        return slot["a"]


    def fav_row_click(slot):
        def cb():
            a = fav_pick(slot)
            if a is not None:
                make_row_click(("fav", slot["i"]), ("favgo",) + a)()
        return cb


    def fav_row_double(slot):
        def cb():
            a = fav_pick(slot)
            if a is not None:
                state["queue"].append(stamped(("favgo",) + a))
        return cb


    def fav_star_click(slot):
        def cb():
            a = fav_pick(slot)
            if a is not None:
                queue_ui(("star", a[0], a[1], a[2]))()
        return cb


    def fav_tick(now):
        """While the Favourites page shows: the search box, every SEARCH_EVERY
        (one read, in place), and the rows again when the text or the lists
        changed. A hidden page is filled when it is shown."""
        ui = fav_ui
        if ui["layer"] is None:
            return
        if pages.get("favs") is not ui["layer"]:
            ui["layer"] = None
            return
        if state["tab"] != "favs" or state["minimized"] or state["docked"]:
            return
        if now >= ui["next"] or ui["next"] - now > SEARCH_EVERY:   # (or the clock went back)
            ui["next"] = now + SEARCH_EVERY
            try:
                t = str(ui["tb"].Text or "")
            except Exception:
                t = ui["text"]
            ui["text"] = t
        if ui["text"] != ui["seen"] or ui["ver"] != lists["ver"]:
            fav_render()


    def fav_travel(act):
        """A Favourites row's double-click ("favgo", book, index, name, method,
        last?) as a travel job, or None (the rune left the book)."""
        serial, index, name, method = act[1], act[2], act[3], act[4]
        i = resolve(serial, index, name)
        if i is None:
            API.SysMsg("Grimoire: %s isn't in that runebook any more." % name, Kit.HUE_BAD)
            return None
        dest = rune_cache[serial][i]
        return ("travel", serial, dest, method or default_method(dest))


    def page_key(tab):
        """The spellbook tab has a page per circle; every other tab has one page."""
        return ("spells", state["circle"]) if tab == "spells" else tab


    def build_page(key, hidden):
        """Draw one page into its own layer."""
        nonlocal tgt
        old = pages.pop(key, None)
        pg = tgt = new_layer(hidden)
        try:
            if isinstance(key, tuple):
                build_spell_page(state["content_top"], key[1])
            elif key == "favs":
                build_fav_page(state["content_top"])
            else:
                build_rune_page(state["content_top"], key)
        finally:
            tgt = frame
        pages[key] = pg
        if old is not None:
            clear(old["ctrls"])
        return pg


    def drop_page(key):
        """A page's contents changed: draw it again right away, shown if it is the
        open tab and hidden otherwise, so every tab stays ready to show."""
        if state["minimized"] or state["dirty"]:
            if key in pages:
                clear(pages.pop(key)["ctrls"])
            return
        build_page(key, key != page_key(state["tab"]))


    def all_page_keys():
        """Every page the window can show: one per spell circle and one per runebook
        whose list is known (a book still being read gets its page once it is)."""
        keys = [("spells", i) for i in range(len(CIRCLES))]
        if runebooks:
            keys.append("favs")
        keys += [b["serial"] for b in runebooks if b["serial"] in rune_cache]
        return keys


    def switch_page(tab, change=None):
        """Hide the open page, apply change (a new circle), then show the page for
        tab. Pages already built just swap visibility, so it's instant."""
        prev = page_key(state["tab"])
        if change:
            change()
        state["tab"] = tab
        save_int("Tab", 0 if tab == "spells" else (TAB_FAVS if tab == "favs" else tab))
        save_int("Circle", state["circle"])               # open tab and circle, for next start
        if tab == "spells":
            loop["next_mana"] = 0.0                       # your mana, at once (dimmed spells)
        key = page_key(tab)
        if key == prev and key in pages and not pages[key]["hidden"]:
            return
        click_state["selected"] = None
        if prev in pages and not show_layer(pages[prev], False):
            state["dirty"] = True              # client can't hide controls: redraw instead
            return
        if key in pages:
            if not show_layer(pages[key], True):
                state["dirty"] = True
            return
        build_page(key, False)


    def switch_tab(key):
        for k, mark in tab_marks.items():
            safe(lambda: mark.SetAlpha(tab_on() if k == key else 0.0))
        switch_page(key)


    def prebuild_next():
        """Any page still missing (the hidden ones after a redraw, a runebook read
        after the last rebuild) is drawn hidden now: one page per call, with a short
        rest between, so the work is spread over many frames instead of one long
        one. Returns True if it built one."""
        if _vis["ok"] is not True or state["minimized"]:
            return False
        missing = [k for k in all_page_keys() if k not in pages]
        if not missing:
            loop["next_prebuild"] = time.time() + PREBUILD_EVERY   # look again after a rest
            return False
        build_page(missing[0], missing[0] != page_key(state["tab"]))
        loop["next_prebuild"] = time.time() + PREBUILD_EVERY
        return True


    def rebuild():
        """Redraw everything: the frame, then every page at once (only the open tab's
        page is shown), so tabs and circles switch instantly from then on."""
        # Build the new window over the old one, then remove the old one, so it never
        # sits empty while it redraws.
        old = frame["ctrls"][:]
        for k in ("ctrls", "tops", "counts"):
            del frame[k][:]
        old_pages = list(pages.values())
        pages.clear()
        row_bgs.clear()
        tab_marks.clear()
        click_state["selected"] = None
        state["dirty"] = False

        top = build_chrome()
        if _vis["ok"] is None and bg_box["parts"]:
            set_shown(bg_box["parts"][0][0], True)    # find out if pages can be shown/hidden instantly
        if not state["minimized"]:
            build_supplies(top)
            build_tabs(top)
            label(gump, state["status"], 30, LH() - 35, 12, STONE_DIM, frame["ctrls"])
            build_page(page_key(state["tab"]), False)
            # the rest are drawn hidden by prebuild_next, one per short rest
            loop["next_prebuild"] = time.time() + PREBUILD_EVERY
        clear(old)
        for pg in old_pages:
            clear(pg["ctrls"])


    def scan_all(full=False, bags=True):
        """Find your books. Saved runebook lists show straight away; books with no saved
        list (or every book, on a full refresh) are read in the background. bags=False
        skips opening bags (a quick look after you pick up or put away a book).
        Runs as a thread job (it may wait for the spellbook to open); the looks at
        your items are each made in one client hop."""
        nonlocal spellbook_serial, known_spells
        saved_data()                          # the saved file is read here, off the client thread
        load_favs()                           # this character's stars and last trip (once)
        spellbook_serial = Kit.on_client(find_spellbook)
        known_spells = load_known_spells(force=full)
        if OPEN_BAGS and bags:
            open_unopened_bags()
        Kit.on_client(lambda: scan_books(full, bags))


    def scan_books(full, bags):
        """The rest of scan_all, on the client thread: no waits in here."""
        nonlocal runebooks
        runebooks = find_runebooks()          # looks only; never uses an item
        del bg_reads[:]
        for b in runebooks:
            s = b["serial"]
            have = s in rune_cache or load_book(s)
            if full or not have:
                bg_reads.append(s)      # the saved list keeps showing until the fresh read is in
            if have and s not in charge_seen:     # charges as saved: no alert for those (GR3)
                charge_seen[s] = book_charges.get(s, (None, None))[0]
            if have and rune_cache.get(s):
                rekey_favs(s)           # stars saved against another list (a 2.6.04 re-read
                #                         moved the runes) find their runes' names again
        lists["ver"] += 1                             # the books carried may have changed
        want = state.pop("want_tab", None)            # the tab open when you left
        if want and (any(b["serial"] == want for b in runebooks) or
                     (want == TAB_FAVS and runebooks)):
            state["tab"] = "favs" if want == TAB_FAVS else want
        if state["tab"] in bg_reads:                  # the open tab goes first
            bg_reads.remove(state["tab"])
            bg_reads.insert(0, state["tab"])
        if state["tab"] == "favs":
            if not runebooks:
                state["tab"] = "spells"
        elif state["tab"] != "spells" and not any(b["serial"] == state["tab"] for b in runebooks):
            state["tab"] = "spells"
        count = "All spells shown" if known_spells is None else "%d spells known" % len(known_spells)
        state["status"] = "%s, %d runebook%s" % (count if spellbook_serial else "No spellbook",
                                                 len(runebooks), "" if len(runebooks) == 1 else "s")
        if not runebooks and bags and (full or not state["reported"]):
            report_books()                    # once per session, and on Refresh (not on every rescan)
            state["reported"] = True
        state["scanned"] = True
        state["dirty"] = True


    def read_and_store(serial):
        """A thread job: read one runebook (waits for its gump), save it, redraw its page."""
        dests, charges = read_runebook(serial)
        if store_book(serial, dests, charges):
            Kit.on_client(lambda: drop_page(serial))       # redraw in one hop


    def on_close():
        state["closed"] = True


    # ------------------------------------------------------------------------------
    #  Module: start / one pass / stop
    # ------------------------------------------------------------------------------
    loop = {"next_count": 0.0, "next_prebuild": 0.0, "last_pos": (None, None), "held": None,
            "totals": None, "settle": 0.0, "size_dirty": False,
            "mana": None, "tier": None, "next_mana": 0.0}     # your mana (dimmed spells)
    trip = {"busy": False,      # a travel job is running (the travel service waits its turn)
            "at": 0.0}          # when the last one started
    jobs = []                   # waiting work handed from _tick to _thread_tick (one at a time)
    # A double-clicked spell: the cast waits (briefly) for a free cursor, then the
    # cursor is spoken for (HOST.claim_cursor) until the player has answered it.
    cast = {"wait": None,       # (spell name, give-up time) while another module has the cursor
            "claim": 0.0,       # time the claim for the player's answer runs out (0: none)
            "seen": False,      # the spell's cursor has come up (release when it goes down)
            "next": 0.0,        # next look at API.HasTarget
            "rd": None,         # 2.6.81: journal reader from the cast on (a failure frees the claim)
            "me": ""}           # your name then (only your own and the server's lines count)


    def reset_state():
        nonlocal tgt
        state.update({"tab": "spells", "circle": 0, "dirty": True, "closed": False,
                      "queue": [("scan",)], "ui_queue": [], "status": "Reading your books",
                      "minimized": False, "switch": None, "content_top": 0, "shutting": False,
                      "scanned": False, "reported": False, "docked": False, "link_state": None,
                      "pick": None})
        del jobs[:]
        for k in ("ctrls", "tops", "counts"):
            del frame[k][:]
        pages.clear()
        row_bgs.clear()
        tab_marks.clear()
        tab_parts.clear()
        tgt = frame
        bg_box["parts"] = []
        _uo_meta.clear()                 # the last run's labels went with its window
        del bg_reads[:]
        loop["next_count"] = loop["next_prebuild"] = loop["settle"] = 0.0
        loop["held"] = loop["totals"] = None
        loop["last_pos"] = (None, None)
        loop["size_dirty"] = False
        loop["mana"] = loop["tier"] = None
        loop["next_mana"] = 0.0
        trip["busy"], trip["at"] = False, 0.0
        state["fav_redraw"] = False
        fav_ui.update({"layer": None, "tb": None, "info": None, "sa": None, "pool": [],
                       "text": "", "seen": None, "ver": -1, "next": 0.0})
        charge_seen.clear()              # (a start learns every book's charges afresh)
        del charge_news[:]
        lists["ver"] += 1
        lists["dest_ver"] = -1
        cast.update({"wait": None, "claim": 0.0, "seen": False, "next": 0.0})
        dump.update({"written": False, "armed": False})
        # the runebook types this CHARACTER taught (a character switch without a
        # script restart used to keep the previous character's, and save them over)
        rb_types.clear()
        rb_types.update(load_rb_types())
        rb_seen.clear()
        _hands["layers"] = None


    def layout_state():
        """For the layout: the window's state (None when it is closed)."""
        if state["closed"] or state["shutting"] or not Kit.is_open(gump):
            return None
        return "docked" if state["docked"] else ("minimized" if state["minimized"] else "open")


    def _start():
        API.SysMsg("Grimoire: build %s loaded." % BUILD, Kit.HUE_INFO)
        reset_state()
        _pack_fn[0] = getattr(HOST, "pack_items", None)   # 2.6.82: the host's shared pack list
        fitst["own"] = None              # 2.6.81 (GR-5): not fitted yet (fit_screen caps the size)
        load_window_prefs()
        # the circle and tab you had open (a runebook tab once the books are found)
        state["circle"] = max(0, min(len(CIRCLES) - 1, load_int("Circle", 0)))
        tab = load_int("Tab", 0)
        state.pop("want_tab", None)
        if tab:
            state["want_tab"] = tab
        create_window()
        G.AddControlOnDisposed(gump, on_close)
        G.AddGump(gump)
        safe(lambda: Kit.on_moved(gump, save_window_pos))
        add_layout = getattr(HOST, "layout_add", None)   # the layout can slot the window
        if add_layout is not None:
            hooks = {"fit": layout_fit, "state": layout_state,   # and fit it to its zone:
                     "exact": True}      # (2.6.56) made exactly its slot's size
            try:
                add_layout(DOCK_KEY, lambda: gump, "Grimoire", hooks)
            except TypeError:                              # a mother before 2.6.55
                safe(lambda: add_layout(DOCK_KEY, lambda: gump, "Grimoire"))
            except Exception:
                pass
        fitst["own"], fitst["told"] = None, None
        if load_int("Min", 0) == 1 or dock_wish():        # minimized when you left
            toggle_min()
        safe(lambda: API.RemoveSharedVar(LINK_CMD))       # ignore a stale command
        link_tick()                                       # tell the Action Bar right away
        safe(lambda: HOST.alert_kind("grimoire.charges", "Runebook low on charges", 0x1EA))
        HOST.services["grimoire.travel"] = svc_travel     # for the Action Bar's Travel cells
        HOST.services["grimoire.destinations"] = svc_destinations
        HOST.services["grimoire.book_charges"] = svc_book_charges   # 2.6.82: Travel cells' counters


    def run_ui_action(act):
        """A window action a click queued (queue_ui): run on the tick, never in the
        handler, so the tick is the one place the window changes."""
        kind = act[0]
        if kind == "min_click":
            min_click()
        elif kind == "circle":
            i = act[1]
            if ("spells", i) in pages and not state["dirty"]:
                go_circle(i)                    # already drawn: swap it in on the spot
            else:
                state["switch"] = ("spells", i)
        elif kind == "settings":
            HOST.show_settings("grimoire")
        elif kind == "fit":                     # the layout's zone fit (layout_fit)
            run_fit(act[1], act[2], act[3])
        elif kind == "close":
            Kit.dispose(gump)                   # on_close turns the module off
        elif kind == "reread":                  # the page's Re-read button: a dump may be written again
            dump["armed"] = True
            state["queue"].append(("read", act[1]))
        elif kind == "star":                    # a destination's star: Favourites on / off
            serial, i = act[1], act[2]
            on = toggle_fav(serial, i, act[3])
            if on is None:
                return
            pg = pages.get(serial)
            parts = pg["stars"].get(i) if pg is not None else None
            if parts is not None and not recolor_star(parts, on):
                drop_page(serial)               # can't recolour in place: draw the page again


    def start_cast(name):
        """Cast a double-clicked spell and speak for its target cursor (the player
        answers it): another module's automatic Target (a bandage between its
        UseObject and its Target) must not answer it (see HOST.claim_cursor).
        The claim is released once the cursor has been up and gone (watch_cast)."""
        now = time.time()
        if name in NO_TARGET_SPELLS:
            # 2.6.81 (GR-2): no cursor will come, so none is spoken for (a claim
            # would turn Bandages and Action Bar presses away for 5 s for nothing)
            API.CastSpell(name)
            bg["hold"] = now + CAST_HOLD
            return
        claim_cursor(CAST_CLAIM)
        # 2.6.81 (GR-2): a reader from now on (client thread: free), so a fizzle,
        # missing reagents or mana end the claim at once (watch_cast)
        try:
            rd = Journal.reader()
        except Exception:
            rd = None
        cast.update({"claim": now + CAST_CLAIM, "seen": False, "next": now + 0.1, "rd": rd,
                     "me": player_name()})
        API.CastSpell(name)
        bg["hold"] = now + CAST_HOLD


    def watch_cast(now):
        """While the cast's claim runs: release it once the spell's cursor has
        come and been answered (API.HasTarget back to False), or when it runs out.
        One look every 0.1 s, in place on the client thread; never a wait."""
        if now >= cast["claim"]:
            cast["claim"], cast["rd"] = 0.0, None
            release_cursor()
            return
        if now < cast["next"]:
            return
        cast["next"] = now + 0.1
        try:
            up = bool(API.HasTarget())
        except Exception:
            up = False
        if up:
            cast["seen"] = True
        elif cast["seen"]:                      # answered (or cancelled): the cursor is free again
            cast["claim"], cast["rd"] = 0.0, None
            release_cursor()
        elif cast["rd"] is not None:
            # 2.6.81 (GR-2): no cursor yet: the cast failed (fizzle, reagents, mana,
            # disturbed)? Then none will come: free the cursor now, not in 5 s
            try:
                lines = cast["rd"].new()
            except Exception:
                lines = ()
            if lines and failure_in(lines, CAST_FAIL_TEXTS, cast["me"]):
                cast["claim"], cast["rd"] = 0.0, None
                release_cursor()


    def cursor_up_now(now):
        """API.HasTarget("any") for the quiet reads. 2.6.82: speed pass: while a
        cursor stays up it is asked again only every 0.25 s (the read itself
        asks once more on the script's thread before opening a book)."""
        if API.HasTarget("any"):
            bg["cursor_next"] = now + 0.25
            return True
        return False


    def _tick():
        if state["closed"]:
            if not state["shutting"]:
                HOST.disable("grimoire")
            return
        now = time.time()
        if pending_scale["value"] is not None and now - pending_scale["t"] >= SCALE_SETTLE:
            apply_scale()
        link_tick()
        while state["ui_queue"]:                    # window actions: first, before any new job
            run_ui_action(state["ui_queue"].pop(0))
            if state["closed"]:
                return

        if now >= loop["settle"]:
            if loop["size_dirty"]:
                save_size()                         # the resize has settled: save it once
            if state["dirty"]:                      # (the size is saved even when another
                rebuild()                           # path already redrew the window)
        if state["switch"] is not None:
            key, state["switch"] = state["switch"], None
            if isinstance(key, tuple):
                go_circle(key[1])
            else:
                switch_tab(key)
            if state["dirty"]:
                rebuild()
        if state["fav_redraw"]:                     # a pooled row's star couldn't be recoloured
            state["fav_redraw"] = False
            if "favs" in pages:
                drop_page("favs")
        if charge_news:
            charges_tick()                          # a book's charges came in: low? (GR3)

        if cast["claim"]:
            watch_cast(now)
        if cast["wait"] is not None:                # a cast waiting for another module's cursor
            name, until = cast["wait"]
            if not cursor_taken():
                cast["wait"] = None
                start_cast(name)
            elif now >= until:
                cast["wait"] = None
                API.SysMsg("Grimoire: %s was not cast; the target cursor stayed in use." % name,
                           Kit.HUE_BAD)

        # This tick runs on the client thread and must never wait: anything that
        # waits for the server (reading a runebook's gump, travelling, opening the
        # spellbook) is handed to _thread_tick as a job, one at a time, in order.
        if jobs:
            pass                                    # the last job hasn't run yet
        elif state["queue"]:
            act = state["queue"].pop(0)
            if act[0] == "pressed":                 # (2.6.84) a trip, with its press time
                if 0 <= now - act[1] <= TRAVEL_DEFER:
                    act = act[2]
                else:
                    # pressed while a runebook job held this tick: never a trip
                    # seconds later, at a moment you didn't choose
                    API.SysMsg("Grimoire: that trip was not made; Grimoire was busy with a "
                               "runebook. Press it again.", Kit.HUE_INFO)
                    act = ("dropped",)
            kind = act[0]
            if kind == "cast":
                if len(act) > 2 and now - act[2] > CAST_DEFER:
                    # 2.6.81 (GR-4): pressed while a runebook job held this tick:
                    # never cast seconds later, at a moment you didn't choose
                    API.SysMsg("Grimoire: %s was not cast; Grimoire was busy with a runebook."
                               % act[1], Kit.HUE_INFO)
                elif cast["wait"] is not None:
                    pass                            # one cast is already waiting: this one is dropped
                elif cursor_taken():                # someone else's cursor: wait for it, briefly
                    cast["wait"] = (act[1], now + CAST_DEFER)
                    API.SysMsg("Grimoire: the target cursor is in use; %s is cast once it is free."
                               % act[1], Kit.HUE_INFO)
                else:
                    start_cast(act[1])
            elif kind == "read":
                if act[1] in bg_reads:
                    bg_reads.remove(act[1])
                if now < bg["hold"] or state["pick"] is not None or cast["claim"] \
                        or cast["wait"] is not None or cursor_taken() or API.HasTarget("any"):
                    # 2.6.81 (GR-1): a cursor is up or spoken for (opening a book would
                    # cancel a spell's cursor): the quiet reads take it, first in line,
                    # once everything is free (not held here: a cast behind it would wait)
                    bg_reads.insert(0, act[1])
                else:
                    jobs.append(act)
            elif kind in ("travel", "scan", "rescan", "refresh"):
                if kind == "refresh":
                    dump["armed"] = True            # a Refresh may write the dump again
                jobs.append(act)
            elif kind == "favgo":                   # a Favourites row: its rune, found again
                job = fav_travel(act)
                if job is not None:
                    jobs.append(job)
            elif kind == "register":
                register_runebook()                 # the answer comes back as "registered"
            elif kind == "registered":
                if registered(act[1]):
                    state["queue"].insert(0, ("scan",))
        elif bg_reads and now >= bg["hold"] and state["pick"] is None \
                and cast["claim"] == 0.0 and cast["wait"] is None and not cursor_taken() \
                and now >= bg.get("cursor_next", 0.0) and not cursor_up_now(now):
            # quietly update one book per pass - never while a target cursor is up
            # (opening a book would take the cursor down), never inside the shard's
            # use delay after the last read (see _thread_tick). 2.6.81 (GR-1): any
            # cursor, also one nobody spoke for (a spell cast from a TazUO icon)
            jobs.append(("read", bg_reads.pop(0)))
        if not jobs and not state["dirty"] and state["switch"] is None \
                and now >= loop["next_prebuild"]:
            prebuild_next()                         # one hidden page, then a short rest

        if state["closed"]:
            return
        if now >= loop["next_count"]:
            refresh_counts()          # keep counts live as you cast, loot or restock
            watch_hands()
            loop["next_count"] = time.time() + COUNT_EVERY
        mana_tick(now)                # your mana, while a spell page shows (dimmed spells)
        fav_tick(now)                 # the search box and rows, while Favourites shows
        # (the window's place is saved by save_window_pos the moment it is let go
        # and read once more in _stop: no per-tick GetX / GetY any more)


    def charges_tick():
        """Books whose charge count just came in (store_book): a book that drops
        under LOW_CHARGES turns its tab red and raises one alert (once per drop:
        it must come back up to LOW_CHARGES before it alerts again); one that is
        recharged turns back. A book's first count this session (no saved list)
        alerts if it is low; the counts loaded from the saved lists don't."""
        while charge_news:
            serial = charge_news.pop(0)
            cur = book_charges.get(serial, (None, None))[0]
            prev = charge_seen.get(serial)
            charge_seen[serial] = cur
            low = cur is not None and cur < LOW_CHARGES
            was_low = prev is not None and prev < LOW_CHARGES
            if low and not was_low:
                title = next((b["title"] for b in runebooks if b["serial"] == serial), "A runebook")
                try:
                    HOST.alert("grimoire.charges", "%s: %d charge%s left" %
                               (title, cur, "" if cur == 1 else "s"), who=serial)
                except Exception:
                    API.SysMsg("Grimoire: %s has %d charge%s left." %
                               (title, cur, "" if cur == 1 else "s"), Kit.HUE_BAD)
            recolor_tab(serial)


    def travel_pending():
        """A trip queued, handed over or on its way (the travel service takes
        one at a time: one key press, one trip)."""
        if trip["busy"] or time.time() - trip["at"] < TRIP_GAP:
            return True
        for a in jobs:
            if a[0] == "travel":
                return True
        for a in state["queue"]:
            if a[0] in ("travel", "favgo") or (a[0] == "pressed" and a[2][0] in ("travel", "favgo")):
                return True
        return False


    def svc_travel(book_serial, rune_index, method, name=None):
        """HOST.services["grimoire.travel"]: travel to a destination of a carried
        runebook (index = its place in the book's list, as grimoire.destinations
        gives it; name, when given, finds the rune again if a re-read moved it).
        The trip is queued for Grimoire's own tick and thread tick, never made
        inside the caller. True when it was accepted; otherwise False, with a
        journal line saying why (the call is always a player's action)."""
        if state["shutting"] or state["closed"]:
            return False
        if method not in TRAVEL_METHODS:
            API.SysMsg("Grimoire: no way to travel called '%s'." % method, Kit.HUE_BAD)
            return False
        try:
            serial, index = int(book_serial), int(rune_index)
        except (TypeError, ValueError):
            return False
        if not state["scanned"]:
            API.SysMsg("Grimoire: still looking for your runebooks; try again in a moment.",
                       Kit.HUE_INFO)
            return False
        title = None
        for b in runebooks:
            if b["serial"] == serial:
                title = b["title"]
                break
        if title is None:
            API.SysMsg("Grimoire: that runebook isn't in your pack or hands.", Kit.HUE_BAD)
            return False
        i = resolve(serial, index, name)
        if i is None:
            API.SysMsg("Grimoire: %s isn't in %s any more." % (name or "that rune", title),
                       Kit.HUE_BAD)
            return False
        try:
            dest = rune_cache[serial][i]           # read once: a re-read may replace the list
        except (KeyError, IndexError, TypeError):
            dest = None
        if dest is None:
            API.SysMsg("Grimoire: %s isn't in %s any more." % (name or "that rune", title),
                       Kit.HUE_BAD)
            return False
        if method == "charge" and dest.get("rune"):
            # (2.6.84) a rune-bag book holds no charges: the trip would cast Recall
            API.SysMsg("Grimoire: %s has no charges to use; pick Recall instead." % title,
                       Kit.HUE_BAD)
            return False
        if method in ("gate", "sacred") and dest.get("slot") is None and not dest.get("rune"):
            # a book of an unknown layout has one button per rune (its own way of travel)
            API.SysMsg("Grimoire: %s has its own runebook layout; only its rune's own button "
                       "works there, not %s." % (title, "Gate Travel" if method == "gate"
                                                 else "Sacred Journey"), Kit.HUE_BAD)
            return False
        if travel_pending():
            API.SysMsg("Grimoire: a trip is already on its way.", Kit.HUE_INFO)
            return False
        state["queue"].append(("travel", serial, dest, method))
        return True


    def svc_destinations():
        """HOST.services["grimoire.destinations"]: every destination of every
        runebook you carry, from the saved lists (no book is read): a list of
        {"book", "book_name", "index", "name", "charges"} (charges None when the
        book doesn't show them). Worked out again only when a list changed;
        the dicts are shared, so read them, don't change them."""
        if lists["dest_ver"] != lists["ver"]:
            out = []
            for b in runebooks:
                s = b["serial"]
                lst = rune_cache.get(s)
                if not lst:
                    continue
                cur = book_charges.get(s, (None, None))[0]
                for i in range(len(lst)):
                    out.append({"book": s, "book_name": b["title"], "index": i,
                                "name": lst[i]["name"], "charges": cur})
            lists["dests"], lists["dest_ver"] = out, lists["ver"]
        return list(lists["dests"])


    def svc_book_charges():
        """HOST.services["grimoire.book_charges"] (2.6.82): {book serial: charges
        or None} of every carried runebook with a saved list (the books
        grimoire.destinations lists), made again only when a list changed. The
        dict is shared: read it, don't change it."""
        if lists.get("chg_ver") != lists["ver"]:
            out = {}
            for b in runebooks:
                s = b["serial"]
                if rune_cache.get(s):
                    out[s] = book_charges.get(s, (None, None))[0]
            lists["charges"], lists["chg_ver"] = out, lists["ver"]
        return lists["charges"]


    def _thread_tick():
        """_thread_work, then the saved lists written once if any changed (2.6.82)."""
        try:
            _thread_work()
        finally:
            flush_saved()


    def thread_wanted():
        """2.6.82: the script-thread pass only when there is work for it."""
        return bool(jobs or favs["save"] or favs["save_last"] or saved["dirty"])


    def _thread_work():
        """On the script's own thread, right after a tick: the job the tick handed
        over, run exactly as before (same steps, same waits and timeouts). Its
        HOST.idle waits keep every other module and window running; Grimoire's own
        tick waits until the job is done, as it always did."""
        if state["closed"]:
            return
        if favs["save"] or favs["save_last"]:
            save_favs()                                # a star or the last trip changed
        if not jobs:
            return
        act = jobs[0]
        kind = act[0]
        if kind == "travel":
            # on its way before it leaves the list: an Action Bar hotkey runs on
            # the client thread at any moment of this job (the save below too)
            # and must find the trip taken (travel_pending)
            trip["busy"], trip["at"] = True, time.time()
        jobs.pop(0)
        if kind == "travel":
            try:
                note_trip(act[1], act[2], act[3])      # the Favourites page's "Last" row
                save_favs()
                travel(act[1], act[2], act[3])
            finally:
                trip["busy"] = False
            bg["hold"] = time.time() + TRAVEL_HOLD     # let the recall / gate finish first
        elif kind == "read":
            # 2.6.81 (GR-1): a cursor that came up since the tick handed this over
            # (a spell cast another way): opening a book would cancel it. The read
            # goes back to the front of the quiet reads, which wait for a free cursor.
            if safe(lambda: API.HasTarget("any"), False):
                if act[1] in bg_reads:
                    bg_reads.remove(act[1])
                bg_reads.insert(0, act[1])
                return
            read_and_store(act[1])
            # the shard's use delay: a second book opened right after the first
            # never opens (its gump never comes, the read fails, a dump is written)
            bg["hold"] = max(bg["hold"], time.time() + USE_DELAY)
        elif kind == "scan":
            scan_all()
        elif kind == "rescan":
            scan_all(bags=False)
        elif kind == "refresh":
            scan_all(full=True)


    _hand_names = {}        # 2.6.82: (serial, graphic, hue) -> named "rune book"? (worn, named items)


    def _held_book(it, look_names):
        """watch_hands' test, each property read once: a bookish graphic, else
        is_runebook (graphic + hue taught, then the name). A worn item's name is
        read again only when it had none yet, or every HAND_NAMES_EVERY looks."""
        g = it.Graphic
        if g in BOOKISH:
            return True
        h = it.Hue
        if (g, h) in rb_types:
            return True
        key = (it.Serial, g, h)
        hit = None if look_names else _hand_names.get(key)
        if hit is None:
            n = it.Name
            hit = is_runebook_v(g, h, n)
            if n:                                 # an item still without a name: asked again
                if len(_hand_names) > 200:
                    _hand_names.clear()
                _hand_names[key] = hit
        return hit


    HAND_NAMES_EVERY = 10   # looks (COUNT_EVERY apart) between fresh reads of worn items' names


    def watch_hands():
        """Look for your books again when you pick one up or put it away."""
        loop["hand_looks"] = n = loop.get("hand_looks", 0) + 1
        look_names = n % HAND_NAMES_EVERY == 0
        held = sorted(it.Serial for it in held_items() if _held_book(it, look_names))
        if loop["held"] is not None and held != loop["held"] and ("rescan",) not in state["queue"]:
            state["queue"].append(("rescan",))
        loop["held"] = held


    def _stop():
        state["shutting"] = True
        for k, fn in (("grimoire.travel", svc_travel), ("grimoire.destinations", svc_destinations),
                      ("grimoire.book_charges", svc_book_charges)):
            if HOST.services.get(k) is fn:
                HOST.services.pop(k, None)
        drop_layout = getattr(HOST, "layout_remove", None)
        if drop_layout is not None:
            safe(lambda: drop_layout(DOCK_KEY))
        save_favs()                            # a star changed since the last thread tick
        flush_saved()                          # 2.6.82: values saved since the last write
        state["docked"], state["link_state"] = False, None
        safe(lambda: API.SetSharedVar(LINK_STATE, "off"))
        release_cursor()                       # a cast's claim never outlives the module
        cast.update({"wait": None, "claim": 0.0, "seen": False, "rd": None})
        def keep_place():                      # 2.6.82: the window's reads in one client hop
            if Kit.is_open(gump):
                save_window_pos()              # where it is now (one read, at stop only)
                return True
            return False
        try:
            placed = Kit.on_client(keep_place)
        except Exception:
            placed = safe(keep_place, False)
        if placed:
            pass
        elif loop["last_pos"][0] is not None:
            save_int("X", loop["last_pos"][0])
            save_int("Y", loop["last_pos"][1])
        if loop["size_dirty"]:
            save_size()
        if Kit.is_open(gump):
            Kit.dispose(gump)


    # ------------------------------------------------------------------------------
    #  Grimoire's page of the Virtue Assistant Settings tab
    # ------------------------------------------------------------------------------
    CONFIG_H = 124               # height of Grimoire's settings page
    cfg = {"opacity": None, "scale": None, "op_v": None, "sc_v": None, "seen": None,
           "loaded": False}


    def build_config(g, x, y, w):
        if not cfg["loaded"] and not Kit.is_open(gump):
            cfg["loaded"] = True
            load_window_prefs()
        scale = int(round(view["scale"] * 100))
        Kit.add_section(g, x, y, w, CONFIG_H, "WINDOW")
        Kit.add_label(g, "Background opacity:", x + 12, y + 34)
        cfg["opacity"] = Kit.add_slider(g, x + 200, y + 38, 200, 0, 100, win["opacity"])
        safe(lambda: cfg["opacity"].SetTooltip("How solid the window's stone and black "
                                               "backdrop are (0-100, 0 = see-through)"))
        cfg["op_v"] = Kit.add_label(g, "%d%%" % win["opacity"], x + 412, y + 34, Kit.HUE_INFO)
        Kit.add_label(g, "Scale:", x + 12, y + 64)
        cfg["scale"] = Kit.add_slider(g, x + 200, y + 68, 200, SCALE_MIN, SCALE_MAX, scale)
        safe(lambda: cfg["scale"].SetTooltip("Size of everything in the window (%d-%d%%, "
                                             "applied once the slider stops moving)"
                                             % (SCALE_MIN, SCALE_MAX)))
        cfg["sc_v"] = Kit.add_label(g, "%d%%" % scale, x + 412, y + 64, Kit.HUE_INFO)
        Kit.add_label(g, "Drag a corner of the Grimoire window to resize it.", x + 12, y + 96,
                      Kit.HUE_INFO)
        cfg["seen"] = (win["opacity"], scale)


    def poll_config():
        if cfg["opacity"] is None:
            return
        try:                                       # 2.6.82: plain try, no lambdas
            op = int(cfg["opacity"].Value)
        except Exception:
            op = cfg["seen"][0]
        try:
            scale = int(cfg["scale"].Value)
        except Exception:
            scale = cfg["seen"][1]
        if op != cfg["seen"][0]:
            on_opacity(max(0, min(100, op)))
            Kit.set_text(cfg["op_v"], "%d%%" % op)
        if scale != cfg["seen"][1]:
            on_scale(scale)
            Kit.set_text(cfg["sc_v"], "%d%%" % scale)
            if not Kit.is_open(gump):
                apply_scale()                      # nothing on screen to wait for
        cfg["seen"] = (op, scale)


    def config_closed():
        cfg["opacity"] = cfg["scale"] = cfg["op_v"] = cfg["sc_v"] = None


    return {"start": _start, "tick": _tick, "stop": _stop,
            "client_tick": True, "thread_tick": _thread_tick, "thread_wanted": thread_wanted,
            "config_height": lambda w: CONFIG_H, "build_config": build_config,
            "poll_config": poll_config, "config_closed": config_closed}


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("grimoire", "Grimoire", "Spellbook, runebooks and reagents in one window",
             _module_grimoire, 0.05,
             category="Your things")
else:
    import API
    API.SysMsg("Grimoire is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
