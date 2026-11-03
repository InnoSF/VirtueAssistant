# =============================================================================
#  Skills  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by Virtue Assistant from LegionScripts/VirtueAssistantModules.
#  Virtue Assistant provides everything this file uses (API, G, safe, Client,
#  Kit, Follow, HOST, Journal, the main loop and the settings window), so run
#  that instead and tick Skills on its Modules tab.
#
#  To leave this module out, take this file out of the folder.
#  Module key: "skills"
#
#  A module made of PARTS (2.6.5): each part below was a module of its own in
#  2.6.06 and keeps every saved key, window place, list and file it had. A
#  part has its own box under the module's row on the Modules tab (click the
#  arrow on the row to see them) and runs only while it is ticked; the mother
#  script's PartSet runs the ticked parts side by side. The old module keys
#  still answer (the Action Bar's mod: cells, HOST.enable, HOST.by_key).
#
#     Skills Window    (was Skills)           A skills window with locks, groups, session gains and targets
#     Training Alarm   (was Attention)        An alarm when staff or a gump need you; skill loops pause
#     Skill Bags       (was SkillBags)        Uses a skill on every item in a bag, once each
#
#  The Training Alarm starts before Skill Bags, which pauses while the alarm's
#  attention.up service says an alarm waits for you.
#
#  2.6.82: speed pass: fewer client reads per tick in all three parts (same
#  actions, messages, saved values and windows).
# =============================================================================


def _module_skills():
    """Builds the module from its parts and returns its hooks."""
    KEY = "skills"
    TITLE = "Skills"


    def _scaled_hooks(title, icon, st, win, redraw):
        """Kit.dock_hooks with scale=True (2.6.55: the layout may scale the
        window whole to fit its zone; these windows are rebuilt whole and never
        move a control after building); the plain hooks on an older mother."""
        try:
            return Kit.dock_hooks(title, icon, st, win, redraw, scale=True)
        except TypeError:
            return Kit.dock_hooks(title, icon, st, win, redraw)

    def _part_window():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Replaces the client's skills window (both the standard scroll and the
        #  advanced list) with one in the Virtue Assistant look. Everything the
        #  client's window does, it does:
        #      every skill with its real value, value with bonuses and cap
        #      the lock arrow per skill (click: up -> down -> locked -> up)
        #      the small gem beside a usable skill uses it
        #      double-click a skill: a floating skill button (the client's own,
        #      the same one you get by dragging a skill out of the client's window)
        #      sort by name, real, value, cap or lock, either way round
        #      the client's skill groups: shown, folded, renamed, added, deleted,
        #      skills moved between them, reset to the default groups
        #      totals of the real and the modified values
        #  and on top of that:
        #      opens instead of the client's window: the paperdoll's Skills button,
        #      the Skills macro and the Action Bar's Skills button all bring this up
        #      search box and filters (trained, gaining now, gained this session,
        #      up / down / locked, below cap, pinned)
        #      session gains: per skill and in total, gains per hour (overall and
        #      over the last half hour), time to cap at the current pace; the
        #      session survives a Virtue Assistant restart and starts anew after a
        #      long break (or when you press Reset)
        #      a progress bar per skill (value / cap)
        #      total skill points against the shard's total cap, with a warning when
        #      you are at the cap and no skill is set to go down
        #      Str / Dex / Int with their lock arrows and the stat cap
        #      a target per skill: the skill locks itself when it gets there; or lock
        #      every skill the moment it reaches its cap
        #      Str / Dex / Int targets too (the stat locks when it gets there) and
        #      the session's stat gains per hour (2.6.05)
        #      a training tip for the range each skill is in, in its tooltip and in
        #      the picked skill's details, from the TIPS table in CONFIG (general
        #      classic-era advice: edit it for the shard) (2.6.05)
        #      pinned skills on top (and in their own group)
        #      lock every shown skill up / down / locked at once, or lock every
        #      capped skill; named lock sets to save and put back whole lock layouts
        #      recent gains list, a journal line per gain (off by default: the
        #      client prints one already), green names for skills that just rose
        #      export a skill sheet (text file next to Virtue Assistant)
        #      ask the server for fresh skill values
        #      Minimize gives the small minimized bar; the gold arrow beside it
        #      folds the window into the Action Bar's tray instead
        #      drag any corner of the window to resize it: its height sets how many
        #      rows the list shows, its width spreads the columns (the name column
        #      and the progress bars grow); the size is remembered with the position
        #
        #  Assistant, loaded by the Virtue Assistant script from
        KEY = "skills"
        TITLE = "Skills"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "Skills_settings"      # per character; every key starts with Skills_
        POS_KEY = "Skills_pos"
        MARKS_KEY = "Skills_marks"            # pinned skills and targets
        LOCKSETS_KEY = "Skills_locksets"      # saved lock layouts
        SESSION_KEY = "Skills_session"        # the running session (survives a restart)
        SESSION_STALE_H = 6                   # no Virtue Assistant for this many hours: new session
        TOTAL_CAP_DEFAULT = 7000              # In Mani Ylem total skill cap in tenths (700.0);
        #                                       not known for sure - set it on the settings page
        VANILLA = ("StandardSkillsGump", "SkillGumpAdvanced")   # the client's skills windows
        DOCK_ICON = 0x13E3                    # Action Bar tray art (as its own Skills button)
        ROW_H = 22                            # one row of the skill list
        SEARCH_W = 110                        # search box width
        BAR_W = 56                            # progress bar width (at the window's natural width)
        BAR_GROW = 120                        # ... and at most this much wider in a wide window
        RESIZE_SETTLE = 0.35                  # seconds without a corner-drag step before relaying out
        MIN_IW = 380                          # the window's narrowest inside width
        ZONE_NAME_MIN = 60                    # (2.6.78) in a zone: the skill name column at least
        ZONE_DROPS = ("bar", "gain", "cap", "real")   # ...and the columns given up, in order
        ZONE_FIELD_MIN = 80                   # (2.6.78) in a zone: the search field at least
        ZONE_MIN_ROWS = 2                     # ...the list rows below which it is drawn smaller
        ZONE_LOG_MIN = 2                      # ...and the log lines it keeps
        TOTAL_TIP = "Real values added up, against the total cap (set it on the settings page)"
        LOCK_BTNS = (("all_up", "All up", "Set every skill in the list to go up"),
                     ("all_down", "All down", "Set every skill in the list to go down "
                                              "(click twice: it can lower many skills)"),
                     ("all_locked", "All locked", "Lock every skill in the list"),
                     ("lock_capped", "Lock capped", "Lock every skill that is at its cap"))
        MINI_W, MINI_H = 280, 46              # minimized bar
        LOG_KEEP = 200                        # gains remembered for rates and the list
        MAX_LOCKSETS = 10
        # client gump art
        GEM = (0x0837, 0x0838, 0x0838)        # the small "use skill" gem (client skills window)
        LOCK_ART = (0x0983, 0x0985, 0x082C)   # up, down, locked arrows (client skills window)
        GROUP_OPEN, GROUP_SHUT = 0x0826, 0x0827   # group arrows (client skills window)
        LINE_GREEN = 0x0808                   # status line art, green (bar of a capped skill)
        BAR_BG_HUE = 946                      # hue on the red line under each bar (grey)
        DIM_HUE = 946                         # the two lock arrows that are not the current one
        SEL_COLOR, SEL_ALPHA = "#D8B048", 0.16    # picked row
        GROUP_COLOR, GROUP_ALPHA = "#FFFFFF", 0.07  # group header rows
        ARM_SECS = 4.0                        # a second click within this confirms (All down, reset)
        REDRAW_EVERY = 1.0                    # the window's texts follow the clock this often
        FALLBACK_NAMES = [                    # only if the client's skill list can't be read
            "Alchemy", "Anatomy", "Animal Lore", "Item Identification", "Arms Lore", "Parrying",
            "Begging", "Blacksmithy", "Bowcraft/Fletching", "Peacemaking", "Camping",
            "Carpentry", "Cartography", "Cooking", "Detecting Hidden", "Discordance",
            "Evaluating Intelligence", "Healing", "Fishing", "Forensic Evaluation", "Herding",
            "Hiding", "Provocation", "Inscription", "Lockpicking", "Magery", "Resisting Spells",
            "Tactics", "Snooping", "Musicianship", "Poisoning", "Archery", "Spirit Speak",
            "Stealing", "Tailoring", "Animal Taming", "Taste Identification", "Tinkering",
            "Tracking", "Veterinary", "Swordsmanship", "Mace Fighting", "Fencing", "Wrestling",
            "Lumberjacking", "Mining", "Meditation", "Stealth", "Remove Trap", "Necromancy",
            "Focus", "Chivalry", "Bushido", "Ninjitsu", "Spellweaving", "Mysticism", "Imbuing",
            "Throwing"]
        # Training tips (2.6.05): one line per skill for the range its real value
        # is in, shown in the picked skill's details and in each row's tooltip
        # (settings: "Training tips"). General classic-era (pre-AoS) advice from
        # the usual training guides - NOT checked against In Mani Ylem: edit it
        # freely for what the shard does differently. Each skill lists
        # (up to, tip) pairs: a tip covers the range from the previous "up to"
        # (or 0) to its own; past the last one there is no tip. Names are spelled
        # as the client's skills window spells them; a skill left out (or with an
        # empty list) shows no tip.
        TIPS = {
            "Alchemy": [(30, "NPC alchemists teach the first points for gold"),
                        (50, "Heal and Agility potions"),
                        (70, "Cure and Greater Agility potions"),
                        (90, "Greater Strength and Greater Heal potions"),
                        (100, "Greater Cure and Greater Explosion potions")],
            "Anatomy": [(100, "Use it on any creature or player; bandaging checks it too")],
            "Animal Lore": [(100, "Use it on tamed or tameable animals")],
            "Item Identification": [(100, "Use it on any item")],
            "Arms Lore": [(100, "Use it on weapons and armour")],
            "Parrying": [(100, "Fight with a shield on (only shields parry pre-AoS)")],
            "Begging": [(100, "Beg from town NPCs")],
            "Blacksmithy": [(30, "NPC blacksmiths teach the first points for gold"),
                            (50, "Maces, then cutlasses"),
                            (65, "Scimitars, then broadswords and kryss"),
                            (80, "Katanas, then short spears and spears"),
                            (100, "Plate gorgets and gloves, then plate legs and tunics")],
            "Bowcraft/Fletching": [(40, "Shafts and arrows"),
                                   (65, "Bows"),
                                   (85, "Crossbows"),
                                   (100, "Heavy crossbows")],
            "Peacemaking": [(100, "Use it near creatures; tougher ones as it rises")],
            "Camping": [(100, "Light kindling over and over (a blade on a tree gives some)")],
            "Carpentry": [(30, "NPC carpenters teach the first points for gold"),
                          (50, "Medium crates"),
                          (65, "Large crates, then wooden shields"),
                          (85, "Fishing poles and quarter staves"),
                          (100, "Gnarled and black staves")],
            "Cartography": [(30, "NPC mapmakers teach the first points for gold"),
                            (50, "Local maps"),
                            (65, "City maps"),
                            (100, "Sea charts, then world maps")],
            "Cooking": [(30, "NPC cooks teach the first points for gold"),
                        (100, "Cook over and over (fish steaks and ribs are cheap)")],
            "Detecting Hidden": [(100, "Use it often, best near someone hidden")],
            "Discordance": [(100, "Use it on creatures; tougher ones as it rises")],
            "Evaluating Intelligence": [(100, "Use it on any player or creature")],
            "Healing": [(30, "NPC healers teach the first points; bandage yourself when hurt"),
                        (60, "Bandage yourself or friends while hurt"),
                        (80, "Keep bandaging; curing poison needs 60 Healing and 60 Anatomy"),
                        (100, "Keep bandaging; resurrecting needs 80 Healing and 80 Anatomy")],
            "Fishing": [(100, "Fish over and over, in any water")],
            "Forensic Evaluation": [(100, "Use it on corpses")],
            "Herding": [(100, "Herd animals with a shepherd's crook")],
            "Hiding": [(100, "Use it over and over")],
            "Provocation": [(100, "Make creatures fight each other; tougher ones as it rises")],
            "Inscription": [(30, "NPC scribes teach the first points for gold"),
                            (100, "Scribe scrolls of a circle you sometimes fail (spell in your book)")],
            "Lockpicking": [(30, "NPC thieves and tinkers teach the first points"),
                            (100, "Pick locked boxes just above your level")],
            "Magery": [(30, "NPC mages teach the first points; then 2nd circle spells"),
                       (45, "3rd circle: Bless, Teleport"),
                       (55, "4th circle: Greater Heal, Mana Drain"),
                       (65, "5th circle: Paralyze, Mind Blast"),
                       (75, "6th circle: Invisibility, Mark"),
                       (90, "7th circle: Flamestrike, Mana Vampire"),
                       (100, "8th circle: Earthquake, summons")],
            "Resisting Spells": [(100, "Rises when spells hit you: a friend's low curses work")],
            "Tactics": [(100, "Rises as you fight with any weapon")],
            "Snooping": [(100, "Look into others' packs (a friend's pack animal is safe)")],
            "Musicianship": [(100, "Play an instrument; the other bard skills train it too")],
            "Poisoning": [(30, "Lesser poison on a weapon or food"),
                          (60, "Regular poison"),
                          (100, "Greater, then deadly poison")],
            "Archery": [(30, "An archery butte or an NPC trainer for the first points"),
                        (100, "Shoot creatures a little tougher than you as it rises")],
            "Spirit Speak": [(100, "Use it over and over")],
            "Stealing": [(100, "Steal light items from a friend's pack; heavier is harder")],
            "Tailoring": [(30, "NPC tailors teach the first points for gold"),
                          (45, "Short pants and fancy shirts"),
                          (55, "Cloaks"),
                          (70, "Robes, then leather gorgets and sleeves"),
                          (85, "Leather leggings and tunics"),
                          (100, "Studded gloves, then studded sleeves and leggings")],
            "Animal Taming": [(30, "NPC animal trainers teach the first points for gold"),
                              (50, "Horses, ostards, llamas, black and polar bears"),
                              (70, "Panthers, grey wolves, grizzly bears, great harts"),
                              (85, "White wolves, bulls, frenzied ostards"),
                              (100, "Drakes and hell hounds, then dragons")],
            "Taste Identification": [(100, "Use it on food and potions")],
            "Tinkering": [(30, "NPC tinkers teach the first points for gold"),
                          (60, "Tools and clock parts"),
                          (80, "Lockpicks"),
                          (100, "Spyglasses or jewellery")],
            "Tracking": [(100, "Use it over and over")],
            "Veterinary": [(30, "NPC veterinarians teach the first points"),
                           (60, "Bandage hurt animals and pets"),
                           (80, "Keep bandaging; curing needs 60 Veterinary, 60 Animal Lore"),
                           (100, "Keep bandaging; resurrecting needs 80 and 80")],
            "Swordsmanship": [(30, "NPC trainers or a training dummy for the first points"),
                              (100, "Fight creatures a little tougher than you as it rises")],
            "Mace Fighting": [(30, "NPC trainers or a training dummy for the first points"),
                              (100, "Fight creatures a little tougher than you as it rises")],
            "Fencing": [(30, "NPC trainers or a training dummy for the first points"),
                        (100, "Fight creatures a little tougher than you as it rises")],
            "Wrestling": [(30, "NPC trainers or a training dummy, empty-handed"),
                          (100, "Fight empty-handed; tougher creatures as it rises")],
            "Lumberjacking": [(100, "Chop trees with an axe over and over")],
            "Mining": [(30, "NPC miners teach the first points for gold"),
                       (65, "Mine iron ore in mountains and caves"),
                       (100, "Keep mining: the coloured ores come from 65 up")],
            "Meditation": [(100, "Spend mana, then meditate; metal armour blocks it")],
            "Stealth": [(100, "Needs 80 Hiding: hide, then move with Stealth (light armour)")],
            "Remove Trap": [(100, "Use it on trapped boxes (tinkers can trap some to practise on)")],
        }
        STAT_TARGETS_KEY = "Skills_stat_targets"   # Str,Dex,Int targets (0 = none), 2.6.05
        STAT_TARGET_MAX = 250                 # the targets' upper bound
        # -----------------------------------------------------------------------------

        LOCK_WORD = ("up", "down", "locked")
        LOCK_TEXT = ("Going up", "Going down", "Locked")
        LOCK_SET = ("Set it to go up", "Set it to go down", "Lock it")   # the details' arrows
        FILTERS = [("all", "All skills"), ("trained", "Trained (above 0)"),
                   ("gaining", "Gaining now"), ("session", "Gained this session"),
                   ("up", "Set to go up"), ("down", "Set to go down"), ("locked", "Locked"),
                   ("below", "Below cap"), ("pinned", "Pinned")]
        SORTS = ("name", "real", "value", "cap", "gain", "lock")

        DEFAULTS = {"replace": True, "x_hides": True, "bars": True, "col_cap": True,
                    "col_gain": True, "journal": False, "lock_at_cap": False,
                    "lock_at_target": True, "cap_warn": True,
                    "rows": 12, "total_cap": TOTAL_CAP_DEFAULT, "hl_secs": 30, "rate_min": 30,
                    "sec_summary": True, "sec_stats": True, "sec_locks": True,
                    "sec_detail": True, "sec_log": False, "log_lines": 5,
                    "sort": "name", "asc": True, "filter": 0, "groups": False,
                    "minimized": False,
                    "width": 0,                   # window width dragged to (0: its natural width)
                    # 2.6.05 (keys 2.6.04 skips when it loads these settings):
                    "tips": True,                 # training tips (details line, row tooltips)
                    "lock_stat_target": True}     # a stat locks when it reaches its target
        LIMITS = {"rows": (4, 40), "total_cap": (100, 72000), "hl_secs": (0, 600),
                  "rate_min": (5, 240), "log_lines": (2, 15), "filter": (0, len(FILTERS) - 1),
                  "width": (0, 4000)}
        LAYOUT_KEYS = ("bars", "col_cap", "col_gain", "rows", "sec_summary", "sec_stats",
                       "sec_locks", "sec_detail", "sec_log", "log_lines", "tips",
                       "x_hides", "replace")      # 2.6.81: the Close tooltip follows these two
        GRP_SETTLE = 1.0                      # 2.6.81: seconds a renamed group's name rests before it is saved
        STAT_NAMES = ("Strength", "Dexterity", "Intelligence")

        def tip_table():
            """TIPS by lower-case skill name: [(up to in tenths, "lo-hi", tip)]."""
            out = {}
            for name, rows in TIPS.items():
                lst, lo = [], 0
                for hi, text in rows or []:
                    try:
                        hi10 = int(round(float(hi) * 10))
                    except (TypeError, ValueError):
                        continue
                    if hi10 <= lo or not text:
                        continue
                    lst.append((hi10, "%g-%g" % (lo / 10.0, hi10 / 10.0), str(text)))
                    lo = hi10
                if lst:
                    out[str(name).lower()] = lst
            return out
        TIP_TABLE = tip_table()

        settings = dict(DEFAULTS)
        marks = {"pins": set(), "targets": {}}          # targets: index -> tenths
        locksets = []                                   # [(name, "udl..."), ...]
        stat_tgt = [0, 0, 0]                            # Str / Dex / Int targets (0: none)
        st = {"shutting": False, "minimized": False, "docked": False, "hidden": False,
              "queue": [], "rebuild": None, "sel": None, "desc": None, "m": None,
              "last_click": (None, 0.0), "arm": {}, "search": "", "tgt_shown": None,
              "ready": False, "asked": 0.0, "swallow_until": 0.0,
              "warned_cap": False, "hl": {}, "log": [], "gains": {}, "pc": {},
              "ref_at": 0.0, "grp_at": 0.0, "save_at": 0.0, "slow_at": 0.0,
              "stat_pending": {}, "started": 0.0, "to_write": [],
              "dirty": True, "redraw_at": 0.0, "ver": 0, "desc_key": None, "cap_at": 0.0,
              "resize_at": 0.0,                     # last step of a corner drag (0: none going on)
              "grp_dirty_at": 0.0,                  # 2.6.81: a group renamed then (0: none waiting)
              "no_resize_told": False,              # the "no resizable windows" note was printed
              "preview": False}                     # the window's own panel shows (a corner drag)
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "rowmap": {}}
        page = {"c": None, "store": ({}, {}), "sync": False}
        UIC = {}                                        # (control, what) -> last value set (see setp)
        REF = {"world": None, "player": None, "how": ""}
        SK = {"objs": [], "names": [], "click": [], "collide": [], "n": 0, "cur": [],
              "low": [], "full": True, "rr": 0}     # 2.6.82: lower-case names; read_skills' turn
        STATS = {"cur": [0, 0, 0], "locks": [0, 0, 0], "cap": 0, "prev": [0, 0, 0]}
        GR = {"list": [], "ok": False, "ver": 0, "sig": None, "of": {}}
        VG = {"gumps": None, "sig": None, "full_at": 0.0}   # the client's window list (vanilla_check)

        def touch():
            """Something the window shows changed: redraw on this tick, and work
            the list's rows out again (st["ver"] is part of rebuild_rows' key)."""
            st["ver"] += 1
            st["dirty"] = True

        HIDDEN_READ = 0.5                     # 2.6.82: s between skill reads while the list is off screen
        STATS_EVERY = 1.0                     # 2.6.82: s between stat reads (stats move a point at a time)
        CAP_EVERY = 5.0                       # 2.6.82: the cap warning's fallback look (changes check at once)

        def list_moved():
            """2.6.82: a skill's values changed. Its texts are redrawn; the list's
            order and members are worked out again only when they can follow the
            values (sorted by a value, or a filter on values: by name with All or
            Pinned they can't)."""
            st["dirty"] = True
            if settings["sort"] != "name" or FILTERS[settings["filter"]][0] not in ("all", "pinned"):
                st["ver"] += 1

        # ---------- the layout's zone fit (2.6.55; 2.6.78) ----------
        #  Told by the mother's layout (hooks "fit") when the window sits in a
        #  zone. (2.6.78) The window then lays itself out for its slot exactly
        #  (hooks "exact" and "verify"): every row flows at the slot's width, the
        #  list takes the height the other sections leave, and a slot narrower
        #  than ZONE_MIN_W is laid out at that width and drawn smaller (see
        #  zone_plan). Your dragged width and rows (settings "width", "rows") are
        #  untouched and come back when the window is freed. The call comes on
        #  the client thread in the keeper's pass: it records and asks for a
        #  rebuild; mode "again" draws it again even at a size it was told.
        fitst = {"width": None, "rows": None, "slot": None, "k": 1.0, "full": None}

        def eff_width():
            """The width the layout wants, else your own (0: the natural width)."""
            return fitst["width"] if fitst["width"] is not None else settings["width"]

        def layout_fit(w, h, mode):
            """(2.6.78) The layout: the window's slot in a zone is w x h px (None:
            freed). Client thread, the keeper's pass: record, rebuild."""
            new = (int(w), int(h)) if (w and h) else None
            if new == fitst["slot"] and not (mode == "again" and new is not None):
                return
            fitst["slot"] = new
            fitst["width"] = new[0] if new is not None else None
            fitst["rows"] = None
            st["m"] = None
            st["rebuild"] = "window"
            touch()

        def drawn_at():
            """(2.6.78) For Check fit: the scale the window is drawn at, and the
            slot size that shows it at 100% (None when it is)."""
            return fitst["k"], fitst["full"]
        sess = {"start": 0.0, "base": {}, "stats": None, "seen": 0.0}

        # =========================================================================
        #  saved settings
        # =========================================================================
        def load_settings():
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                if k not in DEFAULTS:
                    continue
                d = DEFAULTS[k]
                if isinstance(d, bool):
                    settings[k] = v == "1"
                elif isinstance(d, int):
                    try:
                        lo, hi = LIMITS.get(k, (-10 ** 9, 10 ** 9))
                        settings[k] = max(lo, min(hi, int(v)))
                    except ValueError:
                        pass
                else:
                    settings[k] = v
            if settings["sort"] not in SORTS:
                settings["sort"] = "name"

        def save_settings():
            parts = []
            for k in DEFAULTS:
                v = settings[k]
                if isinstance(v, bool):
                    v = "1" if v else "0"
                parts.append("%s=%s" % (k, v))
            Kit.put_var(SETTINGS_KEY, ";".join(parts))

        def load_marks():
            marks["pins"], marks["targets"] = set(), {}
            for part in Kit.get_var(MARKS_KEY).split(";"):
                p = part.split(":")
                if len(p) != 3:
                    continue
                try:
                    i, pin, tgt = int(p[0]), p[1] == "1", int(p[2])
                except ValueError:
                    continue
                if pin:
                    marks["pins"].add(i)
                if tgt > 0:
                    marks["targets"][i] = tgt

        def save_marks():
            idx = sorted(marks["pins"] | set(marks["targets"]))
            Kit.put_var(MARKS_KEY, ";".join("%d:%s:%d" % (i, "1" if i in marks["pins"] else "0",
                                                          marks["targets"].get(i, 0)) for i in idx))

        def load_locksets():
            del locksets[:]
            for part in Kit.get_var(LOCKSETS_KEY).split("|"):
                if "=" in part:
                    name, code = part.split("=", 1)
                    if name and code:
                        locksets.append((name, code))

        def save_locksets():
            Kit.put_var(LOCKSETS_KEY, "|".join("%s=%s" % (n, c) for n, c in locksets))

        def load_stat_targets():
            """Str / Dex / Int targets (2.6.05: a key of its own, which 2.6.04 never reads)."""
            p = Kit.get_var(STAT_TARGETS_KEY).split(",")
            for k in range(3):
                try:
                    stat_tgt[k] = max(0, min(STAT_TARGET_MAX, int(p[k])))
                except (IndexError, ValueError):
                    stat_tgt[k] = 0

        def save_stat_targets():
            Kit.put_var(STAT_TARGETS_KEY, ",".join(str(v) for v in stat_tgt))

        def load_session():
            p = Kit.get_var(SESSION_KEY).split("|")
            now = time.time()
            sess.update({"start": now, "base": {}, "stats": None, "seen": now})
            if len(p) < 4:
                return
            try:
                start, seen = float(p[0]), float(p[3])
            except ValueError:
                return
            if now - seen > SESSION_STALE_H * 3600 or start > now:
                return                                  # a long break: a new session
            base = {}
            for kv in p[1].split(","):
                if ":" in kv:
                    try:
                        k, v = kv.split(":")
                        base[int(k)] = int(v)
                    except ValueError:
                        pass
            stats = None
            try:
                s = [int(x) for x in p[2].split(",")]
                stats = s if len(s) == 3 else None
            except ValueError:
                pass
            sess.update({"start": start, "base": base, "stats": stats, "seen": now})

        def save_session():
            sess["seen"] = time.time()
            b = ",".join("%d:%d" % (k, v) for k, v in sorted(sess["base"].items()))
            s = ",".join(str(x) for x in sess["stats"]) if sess["stats"] else ""
            Kit.put_var(SESSION_KEY, "%d|%s|%s|%d" % (sess["start"], b, s, sess["seen"]))

        def new_session():
            sess.update({"start": time.time(), "base": {}, "stats": None})
            for i in range(SK["n"]):
                sess["base"][i] = SK["cur"][i][0]
            if any(STATS["cur"]):
                sess["stats"] = list(STATS["cur"])
            st["gains"], st["log"] = {}, []
            save_session()

        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])

        # =========================================================================
        #  the client's skills (read straight from the client: no waiting)
        # =========================================================================
        def find_world():
            w = safe(lambda: Tz.get(None, "Instance", Tz.T("ClassicUO.Game.World")))
            if w is None:
                w = safe(lambda: Typing._get(None, "World",
                                             Tz.T("ClassicUO.Game.Managers.UIManager")))
            if w is None:
                w = safe(lambda: Typing._get(API, "World"))
            return w

        LOCK_BY_NAME = {"Up": 0, "Down": 1, "Locked": 2}
        LKC = {"int": True}           # 2.6.82: int() takes the client's Lock enum (decided once)

        def lock_int(v):
            """A lock (the client's Lock enum, or a number) as 0 up, 1 down, 2
            locked. 2.6.82: when int() refuses the enum (a name comes back from
            str()), the name is used from then on: no exception per skill per tick."""
            if LKC["int"]:
                try:
                    return max(0, min(2, int(v)))
                except Exception:
                    n = LOCK_BY_NAME.get(str(v))
                    if n is not None:
                        LKC["int"] = False
                        return n
                    return 0
            n = LOCK_BY_NAME.get(str(v))
            if n is not None:
                return n
            try:
                return max(0, min(2, int(v)))
            except Exception:
                return 0

        def load_skill_objects(objs, how):
            names, click = [], []
            for s in objs:
                names.append(str(safe(lambda s=s: s.Name, "") or "?"))
                click.append(bool(safe(lambda s=s: s.IsClickable, False)))
            # API.UseSkill / SetSkillLock take the FIRST skill whose name contains
            # the text: a name inside an earlier skill's name needs the index way
            low = [n.lower() for n in names]
            collide = [any(low[i] in low[j] for j in range(i)) for i in range(len(low))]
            SK.update({"objs": objs, "names": names, "click": click, "collide": collide,
                       "n": len(objs), "low": low, "full": True})   # 2.6.82: low, full (read_skills)
            if len(SK["cur"]) != len(objs):
                SK["cur"] = [[0, 0, 0, 0] for _ in objs]
            REF["how"] = how
            st["m"] = None                               # column widths follow the names

        def refresh_refs(force=False):
            """The client's Skill objects (kept: the client updates them in place).
            Looked up again every few seconds in case you relogged."""
            now = time.time()
            if not force and now < st["ref_at"]:
                return SK["n"] > 0
            st["ref_at"] = now + 3.0
            world = find_world()
            player = safe(lambda: Typing._get(world, "Player")) if world is not None else None
            if player is not None:
                arr = safe(lambda: Typing._get(player, "Skills"))
                objs = safe(lambda: [s for s in arr], None) if arr is not None else None
                if objs:
                    # 2.6.82: `is` (the client's object itself, as ReferenceEquals)
                    same = REF["player"] is not None and REF["player"] is player \
                        and len(objs) == SK["n"]
                    relog = REF["player"] is not None and not same
                    REF.update({"world": world, "player": player})
                    if not same:
                        if relog:                         # another character: start over
                            SK["cur"] = []
                            st["ready"] = False
                            st["rebuild"] = "window"
                        load_skill_objects(objs, "client")
                    return True
            REF.update({"world": world, "player": None})
            if SK["n"] == 0 or REF["how"] != "api":
                objs = []
                for name in FALLBACK_NAMES:            # by name through the API
                    s = safe(lambda name=name: API.GetSkill(name))
                    if s is not None and str(safe(lambda: s.Name, "")) == name:
                        objs.append(s)
                if objs:
                    load_skill_objects(objs, "api")
            return SK["n"] > 0

        RR_N = 15                     # 2.6.82: skills whose cap and lock are read per tick

        def read_skills(full=False):
            """Fresh values of every skill. Returns {index: values before} of the
            ones that changed. Runs every tick, so it makes nothing new unless a
            value really changed (a changed skill gets a new list: the old one is
            what note_gains compares with). 2.6.82: Base and Value of every skill
            each tick; Cap and Lock of RR_N skills a tick in turn (each about once
            a second), and at once of a skill whose Base or Value moved (so the
            lock at its cap or target sees fresh ones). full: all four of all
            (the first read, new skill objects, skills not in yet)."""
            changed = {}
            cur = SK["cur"]
            objs = SK["objs"]
            n = len(objs)
            if n == 0 or len(cur) != n:
                return changed
            if SK["full"]:
                SK["full"] = False
                full = True
            rr = SK["rr"] % n
            SK["rr"] = rr + RR_N
            _int = int
            for i in range(n):
                s = objs[i]
                try:
                    b, v = _int(s.BaseFixed), _int(s.ValueFixed)
                except Exception:
                    continue
                c = cur[i]
                if full or b != c[0] or v != c[1] or (i - rr) % n < RR_N:
                    try:
                        cp = _int(s.CapFixed)
                        lk = lock_int(s.Lock)
                    except Exception:
                        continue
                    if b != c[0] or v != c[1] or cp != c[2] or lk != c[3]:
                        changed[i] = c
                        cur[i] = [b, v, cp, lk]
            return changed

        def read_stats():
            """Str / Dex / Int, their locks and the stat cap; True if any changed."""
            cur = STATS["cur"]
            locks = STATS["locks"]
            cap = STATS["cap"]
            p = REF["player"]
            done = False
            if p is not None:
                try:
                    cur = [int(p.Strength), int(p.Dexterity), int(p.Intelligence)]
                    locks = [lock_int(p.StrLock), lock_int(p.DexLock), lock_int(p.IntLock)]
                    cap = int(p.StatsCap)
                    done = True
                except Exception:
                    pass
            if not done:
                pl = safe(lambda: API.Player)
                if pl is not None:
                    cur = [int(safe(lambda a=a: getattr(pl, a), 0) or 0)
                           for a in ("Strength", "Dexterity", "Intelligence")]
                    locks = [lock_int(safe(lambda a=a: getattr(pl, a), 0))
                             for a in ("StrLock", "DexLock", "IntLock")]
                    cap = int(safe(lambda: pl.StatsCap, 0) or 0)
            if st["stat_pending"]:
                now = time.time()
                locks = list(locks)
                for k, (lk, until) in list(st["stat_pending"].items()):
                    if now < until:
                        locks[k] = lk                   # just clicked: show it until the server says
                    else:
                        st["stat_pending"].pop(k, None)
            if cur == STATS["cur"] and locks == STATS["locks"] and cap == STATS["cap"]:
                return False
            STATS["prev"] = STATS["cur"]                # (note_stats: a step onto a target)
            STATS["cur"], STATS["locks"], STATS["cap"] = cur, locks, cap
            return True

        def skills_loaded():
            return any(c[2] > 0 for c in SK["cur"])

        # ---------- groups: the client's own (shared with its skills window) ----------
        def group_mgr():
            w = REF["world"] or find_world()
            return safe(lambda: Typing._get(w, "SkillsGroupManager")) if w is not None else None

        def groups_wanted():
            """The groups are on show somewhere: the list shows them, the picked
            skill's details name its group, or the settings page is open."""
            if page["c"] is not None:
                return True
            if win["g"] is None or not win["c"] or st["minimized"] or st["docked"]:
                return False
            return settings["groups"] or (st["sel"] is not None and settings["sec_detail"])

        def read_groups(force=False):
            """The client's skill groups (re-read once a second while they are on
            show - they can be changed in the client's own skills window too)."""
            now = time.time()
            if not force and (now < st["grp_at"] or not groups_wanted()):
                return
            # 2.6.82: once a second while the list or the settings page shows the
            # groups; every GRP_DETAIL_EVERY s while only the details name one
            st["grp_at"] = now + (1.0 if page["c"] is not None or settings["groups"]
                                  else GRP_DETAIL_EVERY)
            mgr = group_mgr()
            lst = safe(lambda: Typing._get(mgr, "Groups")) if mgr is not None else None
            out = []
            if lst is not None:
                for g in safe(lambda: list(lst), []) or []:
                    try:
                        n = int(g.Count)
                        members = [int(g.GetSkill(k)) for k in range(n)]
                        out.append({"obj": g, "name": str(g.Name or ""),
                                    "members": [m for m in members if m < SK["n"]],
                                    "max": bool(g.IsMaximized)})
                    except Exception:
                        continue
            sig = (lst is not None, tuple((g["name"], tuple(g["members"]), g["max"]) for g in out))
            if sig != GR["sig"]:
                GR["sig"] = sig
                GR["ver"] += 1                            # the list's rows are worked out again
            of = {}                                       # 2.6.82: skill -> its (first) group
            for gi in range(len(out) - 1, -1, -1):
                for k in out[gi]["members"]:
                    of[k] = gi
            GR["list"], GR["ok"], GR["of"] = out, lst is not None, of

        GRP_DETAIL_EVERY = 3.0                # 2.6.82: s between group reads for the details alone

        def group_of(i):
            return GR["of"].get(i)

        def groups_save():
            mgr = group_mgr()
            if mgr is not None:
                safe(lambda: mgr.Save())
            read_groups(True)

        # ---------- sending to the client / server ----------
        def as_byte(v):
            try:
                import System
                return System.Byte(v)
            except Exception:
                return v

        def ga_call(name, args):
            return Tz.call(None, name, args, Tz.T("ClassicUO.Game.GameActions"))

        def set_lock(i, v):
            if i is None or i >= SK["n"] or SK["cur"][i][3] == v:
                return
            name = SK["names"][i]
            done = False
            if not SK["collide"][i]:
                done = safe(lambda: (API.SetSkillLock(name, LOCK_WORD[v]), True)[1], False)
            if not done:
                try:
                    import System
                    ga_call("ChangeSkillLockStatus", [System.UInt16(i), System.Byte(v)])
                    lt = Tz.T("ClassicUO.Game.Data.Lock")
                    Tz.put(SK["objs"][i], "Lock", System.Enum.ToObject(lt, v))
                except Exception:
                    pass
            SK["cur"][i][3] = v

        def use_skill(i):
            if i is None or i >= SK["n"]:
                return
            if not SK["click"][i]:
                API.SysMsg("%s: %s can't be used directly." % (TITLE, SK["names"][i]), Kit.HUE_INFO)
                return
            if not SK["collide"][i] and safe(lambda: (API.UseSkill(SK["names"][i]), True)[1], False):
                return
            try:
                ga_call("UseSkill", [i])
            except Exception as ex:
                API.SysMsg("%s: couldn't use %s (%s)." % (TITLE, SK["names"][i], Tz.why(ex)),
                           Kit.HUE_BAD)

        def make_button(i):
            """The client's own floating skill button, as dragging a skill out of
            its skills window makes it (one per skill)."""
            if i is None or i >= SK["n"] or not SK["click"][i]:
                API.SysMsg("%s: only a usable skill gets a button." % TITLE, Kit.HUE_INFO)
                return
            try:
                import System
                for b in Tz.windows(["SkillButtonGump"]):
                    if int(safe(lambda b=b: Tz.get(b, "SkillID"), -1)) == i:
                        safe(lambda b=b: b.Dispose())
                t = Tz.T("ClassicUO.Game.UI.Gumps.SkillButtonGump")
                world = REF["world"] or find_world()
                g = win["g"]
                x = (safe(lambda: g.GetX(), 200) + safe(lambda: g.GetWidth(), 300) + 10) \
                    if Kit.is_open(g) else 200
                y = safe(lambda: g.GetY(), 200) if Kit.is_open(g) else 200
                btn = System.Activator.CreateInstance(t, System.Array[object](
                    [world, SK["objs"][i], x, y]))
                Tz.call(None, "Add", [btn, True], Tz.T("ClassicUO.Game.Managers.UIManager"))
                API.SysMsg("%s: %s button placed beside the window; drag it where you like."
                           % (TITLE, SK["names"][i]), Kit.HUE_GOOD)
            except Exception as ex:
                API.SysMsg("%s: couldn't make the button (%s)." % (TITLE, Tz.why(ex)), Kit.HUE_BAD)

        def ask_server():
            """Fresh skill values: the client's own request (it opens the client's
            skills window, which is closed again at once)."""
            world = REF["world"] or find_world()
            st["swallow_until"] = time.time() + 6.0
            st["asked"] = time.time()
            try:
                ga_call("OpenSkills", [world])
                return True
            except Exception:
                return False

        def set_stat_lock(k, v):
            """Str / Dex / Int (k 0-2) set to go up / down / locked (v 0-2)."""
            try:
                API.SetStatLock(("str", "dex", "int")[k], LOCK_WORD[v])
            except Exception:
                return False
            STATS["locks"][k] = v
            st["stat_pending"][k] = (v, time.time() + 2.5)
            return True

        def stat_lock(k):
            set_stat_lock(k, (STATS["locks"][k] + 1) % 3)

        # =========================================================================
        #  session numbers
        # =========================================================================
        def f1(tenths):
            return "%.1f" % (tenths / 10.0)

        def sgain(i):
            b = sess["base"].get(i)
            return 0 if b is None else SK["cur"][i][0] - b

        def total_gain():
            return sum(sgain(i) for i in range(SK["n"]))

        MIN_RATE_SPAN = 600.0                 # rates are never worked out over less than this

        def hours_running():
            return max(MIN_RATE_SPAN, time.time() - sess["start"]) / 3600.0

        def recent_gain(i, now):
            win_s = settings["rate_min"] * 60
            return sum(d for t, d in st["gains"].get(i, []) if now - t <= win_s)

        def rates(i, now):
            """(session average per hour, recent per hour), in tenths."""
            avg = sgain(i) / hours_running()
            span = max(MIN_RATE_SPAN, min(settings["rate_min"] * 60.0,
                                          now - max(sess["start"], st["started"])))
            recent = recent_gain(i, now) / (span / 3600.0)
            return avg, recent

        def dur(secs):
            secs = int(max(0, secs))
            if secs >= 3600:
                return "%dh %02dm" % (secs // 3600, (secs % 3600) // 60)
            if secs >= 60:
                return "%dm" % (secs // 60)
            return "%ds" % secs

        def eta(i, now, rt=None):
            base, _, cap, _ = SK["cur"][i]
            if base >= cap:
                return "at cap"
            avg, recent = rt if rt is not None else rates(i, now)
            r = recent if recent > 0 else avg
            if r <= 0:
                return "--"
            return "~" + dur((cap - base) / r * 3600)

        def gaining_now(i, now):
            return recent_gain(i, now) > 0

        def note_gains(changed, now):
            """Gains and losses of the real value, the rates, journal lines and the
            auto locks that ride on them. changed: {index: values before}."""
            dirty = False
            for i in changed:
                old = changed.get(i)
                if old is None:
                    continue
                new = SK["cur"][i]
                d = new[0] - old[0]
                if d == 0:
                    continue
                dirty = True
                name = SK["names"][i]
                if i not in sess["base"]:
                    sess["base"][i] = old[0]
                if d > 0:
                    st["gains"].setdefault(i, []).append((now, d))
                    if len(st["gains"][i]) > LOG_KEEP:
                        st["gains"][i] = st["gains"][i][-LOG_KEEP:]
                    if settings["hl_secs"] > 0:
                        st["hl"][i] = now + settings["hl_secs"]
                st["log"].append((now, name, d, new[0]))
                if len(st["log"]) > LOG_KEEP:
                    st["log"] = st["log"][-LOG_KEEP:]
                if settings["journal"]:
                    API.SysMsg("%s: %s %s%s (%s, session %+.1f)." % (
                        TITLE, name, "+" if d > 0 else "-", f1(abs(d)), f1(new[0]),
                        sgain(i) / 10.0), Kit.HUE_GOOD if d > 0 else Kit.HUE_BAD)
                # its cap, then its target (new is SK["cur"][i] itself, so the target
                # sees a lock set at the cap)
                for mark, opt, what in ((new[2], "lock_at_cap", "its cap (%s)"),
                                        (marks["targets"].get(i), "lock_at_target", "its target %s")):
                    if d > 0 and mark is not None and old[0] < mark <= new[0]:
                        what = what % f1(mark)
                        if settings[opt] and new[3] == 0:
                            set_lock(i, 2)
                            API.SysMsg("%s: %s reached %s and was locked." % (TITLE, name, what),
                                       Kit.HUE_GOOD)
                        else:
                            API.SysMsg("%s: %s reached %s." % (TITLE, name, what), Kit.HUE_GOOD)
            if dirty and time.time() >= st["save_at"]:
                st["save_at"] = time.time() + 15.0
                save_session()

        def total_real():
            return sum(c[0] for c in SK["cur"])

        def at_total_cap():
            """At the total cap with skills set to go up but none set to go down:
            nothing can rise any more."""
            if total_real() < settings["total_cap"]:
                return False
            up = any(c[3] == 0 and c[0] < c[2] for c in SK["cur"])
            down = any(c[3] == 1 and c[0] > 0 for c in SK["cur"])
            return up and not down

        def cap_warning():
            if not settings["cap_warn"]:
                st["warned_cap"] = False
                return
            stuck = at_total_cap()
            if stuck and not st["warned_cap"]:
                API.SysMsg("%s: you are at the total skill cap (%s) and no skill is set to go "
                           "down, so nothing can rise. Set one to go down." % (
                               TITLE, f1(settings["total_cap"])), Kit.HUE_BAD)
            st["warned_cap"] = stuck

        # ---------- stat targets and gains (2.6.05) ----------
        def stat_gain(k):
            base = sess["stats"]
            return STATS["cur"][k] - base[k] if base else 0

        def note_stats():
            """A stat that stepped by one point (as a gain or a loss does; the
            jump of a spell or a potion doesn't count) onto its target, the way
            its lock sends it, has reached it: locked there when the option is
            on, as a skill is at its target. Runs when the stats changed."""
            prev, cur = STATS["prev"], STATS["cur"]
            for k in range(3):
                t = stat_tgt[k]
                if not t or not prev[k] or cur[k] != t:
                    continue
                step = cur[k] - prev[k]
                if step == 1:
                    way = 0                             # rose to it: set to go up
                elif step == -1:
                    way = 1                             # fell to it: set to go down
                else:
                    continue
                if settings["lock_stat_target"] and STATS["locks"][k] == way:
                    set_stat_lock(k, 2)
                    API.SysMsg("%s: %s reached its target %d and was locked." % (
                        TITLE, STAT_NAMES[k], t), Kit.HUE_GOOD)
                else:
                    API.SysMsg("%s: %s reached its target %d." % (TITLE, STAT_NAMES[k], t),
                               Kit.HUE_GOOD)

        def stat_at_target(k):
            """A target just set to where the stat is now: locked at once (with
            the option on), or the next gain would carry it past."""
            t, v = stat_tgt[k], STATS["cur"][k]
            if t and v == t and settings["lock_stat_target"] and STATS["locks"][k] != 2:
                set_stat_lock(k, 2)
                API.SysMsg("%s: %s is at its target %d and was locked." % (
                    TITLE, STAT_NAMES[k], t), Kit.HUE_GOOD)

        def stat_tip(k, hrs):
            """The tooltip of Str / Dex / Int in the window: the session's gain,
            the rate and the target."""
            v = STATS["cur"][k]
            lines = ["%s %d" % (STAT_NAMES[k], v)]
            if sess["stats"]:
                d = stat_gain(k)
                lines[0] += ": %+d this session (%.1f / hour)" % (d, d / hrs)
            t = stat_tgt[k]
            if not t:
                lines.append("No target (click: set one on the settings page)")
            elif v == t:
                lines.append("Target %d: reached" % t)
            else:
                lines.append("Target %d: %d to go %s%s" % (
                    t, abs(t - v), "up" if t > v else "down",
                    ", then it locks" if settings["lock_stat_target"] else ""))
            return "\n".join(lines)

        # ---------- training tips (2.6.05) ----------
        def tip_for(i):
            """(range "lo-hi", tip) for skill i at its real value now, or None."""
            if i is None or i >= SK["n"]:
                return None
            rows = TIP_TABLE.get(SK["names"][i].lower())
            if rows:
                base = SK["cur"][i][0]
                for hi, rng, text in rows:
                    if base < hi:
                        return rng, text
            return None

        # =========================================================================
        #  what the list shows
        # =========================================================================
        def passes(i, now):
            f = FILTERS[settings["filter"]][0]
            base, _, cap, lock = SK["cur"][i]
            q = st["search"]
            if q and q not in SK["low"][i]:
                return False
            if f == "trained":
                return base > 0
            if f == "gaining":
                return gaining_now(i, now)
            if f == "session":
                return sgain(i) > 0
            if f in LOCK_WORD:                          # up / down / locked
                return lock == LOCK_WORD.index(f)
            if f == "below":
                return base < cap
            if f == "pinned":
                return i in marks["pins"]
            return True

        def sort_list(idx):
            s = settings["sort"]
            name = SK["low"].__getitem__                  # 2.6.82: lower-case once per load
            if s == "name":
                out = sorted(idx, key=name)
            else:
                col = {"real": 0, "value": 1, "cap": 2, "lock": 3}.get(s)
                kf = sgain if col is None else (lambda i: SK["cur"][i][col])
                out = sorted(sorted(idx, key=name), key=kf)   # stable: names break ties
            if not settings["asc"]:
                out.reverse()
            return out

        def descriptors(now):
            vis = [i for i in range(SK["n"]) if passes(i, now)]
            vset = set(vis)                               # 2.6.82: membership tests (vis keeps the order)
            pins = [i for i in vis if i in marks["pins"]]
            filt = bool(st["search"]) or settings["filter"] != 0
            out = []
            if not settings["groups"] or not GR["ok"]:
                if FILTERS[settings["filter"]][0] == "pinned":
                    return [("s", i) for i in sort_list(vis)]
                rest = [i for i in vis if i not in marks["pins"]]
                return [("s", i) for i in sort_list(pins) + sort_list(rest)]
            if pins and FILTERS[settings["filter"]][0] != "pinned":
                shut = st["pc"].get("pin", False)
                out.append(("g", "pin", shut))
                if not shut:
                    out += [("s", i) for i in sort_list(pins)]
            seen = set()
            for gi, g in enumerate(GR["list"]):
                mem = [i for i in g["members"] if i in vset]
                seen.update(g["members"])
                if not mem and filt:
                    continue
                out.append(("g", gi, not g["max"]))
                if g["max"]:
                    out += [("s", i) for i in sort_list(mem)]
            other = [i for i in vis if i not in seen]
            if other:
                shut = st["pc"].get("other", False)
                out.append(("g", "other", shut))
                if not shut:
                    out += [("s", i) for i in sort_list(other)]
            return out

        # =========================================================================
        #  window
        # =========================================================================
        def queue(action):
            """Click handler: the action runs on the module's next tick."""
            def handler(*args):
                if isinstance(action, tuple) or action not in st["queue"]:
                    st["queue"].append(action)
            return handler

        def row_click(i):
            """A click on a skill row picks it; a second click on the same row
            within 0.6 s (a double-click) makes its floating button."""
            def handler(*args):
                now = time.time()
                last, t = st["last_click"]
                if last == i and now - t <= 0.6:
                    st["last_click"] = (None, 0.0)
                    st["queue"].append(("button", i))
                else:
                    st["last_click"] = (i, now)
                    st["queue"].append(("pick", i))
            return handler

        on_disposed = Kit.disposer(KEY, st, win)

        def redraw():
            st["rebuild"] = "window"

        def setp(ctrl, attr, value):
            """Set a control's property only when it changes. The cache is keyed by
            the control itself (as Kit._texts is): id() of a client object is a slow
            lookup in IronPython, and this runs for every row part on every refresh."""
            if ctrl is None:
                return
            k = (ctrl, attr)
            try:
                if UIC.get(k) == value:
                    return
                UIC[k] = value
            except TypeError:                             # an unhashable stand-in: always set
                pass
            try:                                          # (no safe(lambda): this runs a lot)
                zk = fitst["k"]                           # (2.6.78) a window drawn smaller
                if attr == "Width":
                    Kit.ui_w(ctrl, value if zk == 1.0 else int(round(value * zk)))
                elif attr == "Pos":
                    if zk == 1.0:
                        Kit.ui_pos(ctrl, value[0], value[1])
                    else:
                        ctrl.SetPos(int(round(value[0] * zk)), int(round(value[1] * zk)))
                else:
                    setattr(ctrl, attr, value)
            except Exception:
                pass

        def remember(ctrl, attr, value):
            """Note the value a control was made with, so setp skips the first set."""
            try:
                UIC[(ctrl, attr)] = value
            except TypeError:
                pass

        # ---------- text widths ----------
        #  Texts that change all the time (rates, the session clock, totals, times
        #  to cap) are trimmed with Kit.fit: the letter-sum measure this module
        #  carried (each letter measured once, a text's width their sum) moved into
        #  the mother as Kit.text_px / Kit.fit in 2.6.01, one cache for every module.
        def cap_w(caption):
            return 35 + Kit.text_w(caption)

        def metrics(IW=None, zone=False):
            """Column places of the skill list (measured from the real font). With
            IW, the inside width of the window, the columns spread into it: what
            is left over past the natural width goes to the name column and (up
            to BAR_GROW) to the progress bars. Without IW, the places last worked
            out (or the natural ones). (2.6.78) zone: the list fits IW whatever it
            is: the progress bar, Gain, Cap and Real are given up in that order
            (your column settings untouched) and the name column takes the rest,
            its names cut (m["cut"])."""
            m = st["m"]
            if m is not None and (IW is None or (m["IW"] == IW and m.get("zone", False) == zone)):
                return m
            m = natural_metrics()
            if zone and IW:
                drop = []
                for key in ZONE_DROPS:
                    if m["sa_w"] + 16 <= IW:
                        break
                    drop.append(key)
                    m = natural_metrics(drop)
                short = (m["sa_w"] + 16) - IW
                if short > 0:                         # still too wide: the names give way
                    cut = min(short, m["name_w"] - ZONE_NAME_MIN)
                    if cut > 0:
                        m["name_w"] -= cut
                        for key in ("real_x", "val_x", "cap_x", "bar_x", "gain_x", "lock_x"):
                            if m[key] is not None:
                                m[key] -= cut
                        m["row_w"] = m["lock_x"] + m["lock_w"] + 6
                        m["sa_w"] = m["row_w"] + 16
                        m["cut"] = True
                m["drop"] = tuple(drop)
            m["zone"] = zone
            extra = max(0, IW - (m["sa_w"] + 16)) if IW else 0
            if extra:
                bar_extra = min(BAR_GROW, extra * 2 // 5) if m["bar_x"] is not None else 0
                name_extra = extra - bar_extra
                m["name_w"] += name_extra
                for key in ("real_x", "val_x", "cap_x", "bar_x", "gain_x", "lock_x"):
                    if m[key] is not None:
                        m[key] += name_extra
                if bar_extra:
                    m["bar_w"] += bar_extra
                    for key in ("gain_x", "lock_x"):
                        if m[key] is not None and m[key] > m["bar_x"]:
                            m[key] += bar_extra
                m["row_w"] = m["lock_x"] + m["lock_w"] + 6
                m["sa_w"] = m["row_w"] + 16
            m["IW"] = IW
            st["m"] = m
            return m

        def natural_metrics(drop=()):
            """The column places at the window's natural width (nothing spread).
            (2.6.78) drop: columns left out in a zone ("bar", "gain", "cap", "real")."""
            m = {"cut": False, "drop": ()}
            names = SK["names"] or FALLBACK_NAMES
            arrow_w = Kit.pic_size(LOCK_ART[0])[0] or 10
            m["arrow_w"] = arrow_w
            m["lock_w"] = max(arrow_w, Kit.pic_size(LOCK_ART[2])[0] or 12)
            gem_w = Kit.pic_size(GEM[0])[0] or 11
            m["name_x"] = 4 + gem_w + 6
            m["name_w"] = max([Kit.text_w(n) for n in names] + [Kit.text_w("Skill") + arrow_w + 4]) + 10
            num_w = max(Kit.text_w("120.0"), Kit.text_w("Value") + arrow_w + 3) + 10
            gain_w = max(Kit.text_w("+120.0"), Kit.text_w("Gain") + arrow_w + 3) + 8
            if "real" in drop:
                m["real_x"] = None
                m["val_x"] = x = m["name_x"] + m["name_w"]
            else:
                m["real_x"] = m["name_x"] + m["name_w"]
                m["val_x"] = x = m["real_x"] + num_w
            x += num_w
            m["bar_h"] = max(4, min(11, Kit.pic_size(Kit.LINE_BLUE)[1] or 9))
            m["bar_w"] = BAR_W
            for key, on, cw in (("cap_x", settings["col_cap"] and "cap" not in drop, num_w),
                                ("bar_x", settings["bars"] and "bar" not in drop, BAR_W + 10),
                                ("gain_x", settings["col_gain"] and "gain" not in drop, gain_w)):
                m[key] = x if on else None              # None: column turned off
                if on:
                    x += cw
            m["lock_x"] = x
            m["row_w"] = x + m["lock_w"] + 6
            m["sa_w"] = m["row_w"] + 16                  # the scrollbar's gutter
            return m

        def detail_rows():
            """Rows of the picked skill's details: five, and the training tip."""
            return 6 if settings["tips"] else 5

        def layout():
            """Sizes and places of every section of the full window: at its
            natural size, or at the size it was dragged to (settings "width" and
            "rows"), kept within the screen. L["min_w"] / L["min_h"] are the
            smallest size a corner drag may give; L["fixed_h"] is the height of
            everything but the list's rows (apply_resize turns a height back into
            rows with it)."""
            M, GAP = Kit.MARGIN, Kit.GAP
            m = natural_metrics()
            sw, sh = Kit.screen()
            tool_need = 12 + Kit.text_w("Find:") + 6 + SEARCH_W + 14 + \
                cap_w(max((f[1] for f in FILTERS), key=Kit.text_w)) + 12 + \
                24 + Kit.text_w("Groups") + 12
            lock_caps = ["All up", "All down", "All locked", "Lock capped"]
            locks_need = 12 + sum(cap_w(c) for c in lock_caps) + 3 * 10 + 12
            detail_need = 12 + cap_w("Use") + 12 + cap_w("Make button") + 12 + \
                cap_w("Next group") + 12
            aw = Kit.pic_size(LOCK_ART[2])[0] or 12
            stats_need = 12 + 3 * (Kit.text_w("Int 125 (+25)") + 8 + aw + 14) + \
                Kit.text_w("Stats 225 / 225") + 12 if settings["sec_stats"] else 0
            IW = max(m["sa_w"] + 16, tool_need, locks_need, detail_need, stats_need, MIN_IW)
            min_w = IW + 2 * M
            if eff_width() > min_w:
                IW = eff_width() - 2 * M
            if sw:                                        # never wider than the screen
                IW = max(min_w - 2 * M, min(IW, sw - 2 * M - 10))
            m = metrics(IW)
            L = {"IW": IW, "W": IW + 2 * M, "min_w": min_w}
            y = M + 30 + GAP
            n_sum = (2 if settings["sec_summary"] else 0) + (1 if settings["sec_stats"] else 0)
            if n_sum:
                L["sum"] = (y, 6 + 24 * n_sum + 4)
                y += L["sum"][1] + GAP
            L["tool"] = (y, 36)
            y += 36 + GAP
            rows = settings["rows"] if fitst["rows"] is None else fitst["rows"]
            L["list"] = (y, 26 + rows * ROW_H + 6)
            y += L["list"][1] + GAP
            if settings["sec_locks"]:
                L["locks"] = (y, 36)
                y += 36 + GAP
            if settings["sec_detail"]:
                L["detail"] = (y, 6 + 24 * detail_rows() + 4)
                y += L["detail"][1] + GAP
            if settings["sec_log"]:
                L["log"] = (y, 26 + 20 * settings["log_lines"] + 4)
                y += L["log"][1] + GAP
            L["H"] = y - GAP + M
            L["fixed_h"] = L["H"] - rows * ROW_H
            lo = LIMITS["rows"][0]
            L["min_h"] = L["fixed_h"] + lo * ROW_H
            if sh and L["H"] > sh - 10 and rows > lo:     # taller than the screen: fewer rows
                fit_rows = max(lo, (sh - 10 - L["fixed_h"]) // ROW_H)
                if fit_rows < rows:
                    shrink = (rows - fit_rows) * ROW_H
                    L["list"] = (L["list"][0], L["list"][1] - shrink)
                    for key in ("locks", "detail", "log"):
                        if key in L:
                            L[key] = (L[key][0] - shrink, L[key][1])
                    L["H"] -= shrink
                    L["rows"] = fit_rows
                    return L
            L["rows"] = rows
            return L

        # ---------- the window in a zone (2.6.78) ----------
        #  In a zone the window is exactly its slot ("exact"): each row flows left
        #  to right at the slot's width, measured with Kit.text_w, and what doesn't
        #  fit goes on the next line; the list's columns give way (metrics, zone
        #  True) and the list takes the height the other sections leave. A slot
        #  narrower than zone_min_w() is laid out at that width and the whole
        #  window drawn smaller (Kit.scale_window); one too short for
        #  ZONE_MIN_ROWS rows is drawn smaller too, laid out wider. Never
        #  converted to a scrolling window: the list has its own scroll area.
        ZLOCKS = tuple(b[1] for b in LOCK_BTNS)

        def zflow(widths, gap, IW):
            """Places (x, line) of items `widths` wide in a section IW wide, from
            12 px in, `gap` px apart, wrapping at 12 px from the right edge; and
            the number of lines used."""
            out, x, line = [], 12, 0
            for cw in widths:
                if x > 12 and x + cw > IW - 12:
                    x, line = 12, line + 1
                out.append((x, line))
                x += cw + gap
            return out, line + 1

        def zone_min_w():
            """The narrowest width every row's flow fits (the window's MIN_W in
            a zone): the list with its columns given up and its names cut, the
            search row wrapped, one button a line."""
            nm = natural_metrics(ZONE_DROPS)
            need = [nm["sa_w"] - max(0, nm["name_w"] - ZONE_NAME_MIN) + 16,
                    12 + Kit.text_w("Find:") + 6 + ZONE_FIELD_MIN + 2 + 12,
                    12 + cap_w(max((f[1] for f in FILTERS), key=Kit.text_w)) + 12,
                    12 + 24 + Kit.text_w("Groups") + 12]
            if settings["sec_summary"]:
                need += [12 + Kit.text_w("Session +99.9") + 12, 12 + cap_w("Reset") + 12]
            if settings["sec_stats"]:
                need.append(12 + Kit.text_w("Int 125 (+25)") + 8 +
                            (Kit.pic_size(LOCK_ART[2])[0] or 12) + 4)
            if settings["sec_locks"]:
                need.append(12 + max(cap_w(t) for t in ZLOCKS) + 12)
            if settings["sec_detail"]:
                aw = max(Kit.pic_size(a)[0] for a in LOCK_ART) or 12
                need += [12 + ZONE_NAME_MIN + 8 + 3 * (aw + 10) + 12,
                         12 + Kit.text_w("Target:") + 8 + 56 + 12 + Kit.text_w("none set") + 4,
                         12 + max(cap_w("Make button"), cap_w("Next group")) + 12]
            return max(need) + 2 * Kit.MARGIN

        def zone_plan(w, h):
            """Every section's place for a window laid out w x h px in a zone
            (layout pixels). "rows" are the list's whole rows (the pixels left
            over go to its section); "need" is the height with ZONE_MIN_ROWS
            rows and ZONE_LOG_MIN log lines; "short": fewer rows than that fit."""
            M, GAP = Kit.MARGIN, Kit.GAP
            IW = w - 2 * M
            Z = {"IW": IW, "W": w, "H": h}
            secs = []                                 # (key, height) top to bottom
            # ---- totals, session and stats ----
            n_sum = 0
            if settings["sec_summary"]:
                cap = f1(settings["total_cap"])
                one = "Total %s / %s   (%s free)   with bonuses %s" % (cap, cap, cap, cap)
                Z["total2"] = Kit.text_w(one) > IW - 24
                rx = IW - 12 - cap_w("Reset")
                Z["sess_own"] = rx - 12 - 6 < Kit.text_w("Session +99.9")
                n_sum += (2 if Z["total2"] else 1) + (2 if Z["sess_own"] else 1)
            if settings["sec_stats"]:
                slot = Kit.text_w("Int 125 (+25)") + 8
                aws = Kit.pic_size(LOCK_ART[2])[0] or 12
                places, sx, line = [], 12, 0
                for j in range(3):
                    if sx > 12 and sx + slot + aws > IW - 4:
                        sx, line = 12, line + 1
                    places.append((sx, line))
                    sx += slot + aws + 14
                if sx > 12 and sx + Kit.text_w("Stats 225 / 225") > IW - 4:
                    sx, line = 12, line + 1
                Z["stats"] = (places, (sx, line))
                n_sum += line + 1
            if n_sum:
                secs.append(("sum", 6 + 24 * n_sum + 4))
            # ---- search row ----
            fcap = cap_w(max((f[1] for f in FILTERS), key=Kit.text_w))
            grp_w = 24 + Kit.text_w("Groups")
            tx = 12 + Kit.text_w("Find:") + 6
            field = IW - tx - 14 - fcap - 12 - grp_w - 12
            if field >= ZONE_FIELD_MIN:
                T = {"field": field, "filter": (tx + field + 14, 0), "groups": (IW - 12 - grp_w, 0)}
                n = 1
            else:
                T = {"field": max(20, IW - tx - 2 - 12), "filter": (12, 1)}
                if 12 + fcap + 12 + grp_w + 12 <= IW:
                    T["groups"], n = (IW - 12 - grp_w, 1), 2
                else:
                    T["groups"], n = (12, 2), 3
            T["tx"] = tx
            Z["T"] = T
            secs.append(("tool", 36 + 28 * (n - 1)))
            secs.append(("list", None))
            # ---- the lock buttons ----
            if settings["sec_locks"]:
                Z["locks_p"], n = zflow([cap_w(t) for t in ZLOCKS], 10, IW)
                secs.append(("locks", 36 + 26 * (n - 1)))
            # ---- the picked skill ----
            if settings["sec_detail"]:
                tx = 12 + Kit.text_w("Target:") + 8
                tgt_x = tx + 56 + 12
                pin_x = IW - 12 - cap_w("Unpin")
                pin_here = pin_x - tgt_x - 6 >= Kit.text_w("none set")
                keys = ["use", "button"] + ([] if pin_here else ["pin"]) + ["nextgrp"]
                caps = {"use": "Use", "button": "Make button", "pin": "Unpin",
                        "nextgrp": "Next group"}
                places, nb = zflow([cap_w(caps[kk]) for kk in keys], 12, IW)
                if nb == 1:                           # one line: Next group at the right, as ever
                    places[-1] = (IW - 12 - cap_w("Next group"), 0)
                Z["D"] = {"tx": tx, "tgt_x": tgt_x, "pin_here": pin_here, "pin_x": pin_x,
                          "tgt_w": (pin_x - 6 if pin_here else IW - 4) - tgt_x,
                          "btns": list(zip(keys, places))}
                secs.append(("detail", 6 + 24 * (detail_rows() + nb) + 4))
            # ---- the log ----
            n_log = settings["log_lines"] if settings["sec_log"] else 0
            if settings["sec_log"]:
                secs.append(("log", None))

            def height(rows, logn):
                y = M + 30 + GAP
                for key, hh in secs:
                    if key == "list":
                        hh = 26 + rows * ROW_H + 6
                    elif key == "log":
                        hh = 26 + 20 * logn + 4
                    y += hh + GAP
                return y - GAP + M
            lo = LIMITS["rows"][0]
            rows = (h - height(0, n_log)) // ROW_H
            while rows < lo and n_log > ZONE_LOG_MIN:     # the log gives way first
                n_log -= 1
                rows = (h - height(0, n_log)) // ROW_H
            Z["need"] = height(ZONE_MIN_ROWS, min(n_log, ZONE_LOG_MIN) if settings["sec_log"] else 0)
            Z["short"] = rows < ZONE_MIN_ROWS
            rows = max(1, rows)
            Z["rows"], Z["log_n"] = rows, n_log
            list_h = max(26 + rows * ROW_H + 6, h - height(0, n_log) + 32)
            y = M + 30 + GAP
            for key, hh in secs:
                if key == "list":
                    hh = list_h
                elif key == "log":
                    hh = 26 + 20 * n_log + 4
                Z[key] = (y, hh)
                y += hh + GAP
            Z["H"] = y - GAP + M
            return Z

        def zone_geom(w, h):
            """(lw, lh, k, Z): the size the window is laid out at for a w x h
            slot, the scale it is drawn at (lw * k = w), and its plan."""
            mw = zone_min_w()
            k = 1.0 if w >= mw else w / float(mw)
            lw, lh, Z = w, h, None
            for _ in range(4):
                lw = w if k == 1.0 else max(mw, int(round(w / k)))
                lh = h if k == 1.0 else int(round(h / k))
                Z = zone_plan(lw, lh)
                if not Z["short"]:
                    break
                k = min(k, h / float(Z["need"]) * 0.999)
            return lw, lh, k, Z

        def fit_set(c, key, txt, room, hue=None, base=None, lbl=None):
            """Label c[key] (or lbl) shows txt cut to room px. (2.6.78) With a
            catcher c[key + "_cat"] (in a zone) the whole text is its tooltip
            while it is cut (with `base`, the area's own tooltip, if any)."""
            if lbl is None:
                lbl = c.get(key)
            if lbl is None:
                return
            src = (txt, room, hue, base)                  # 2.6.82: nothing new: no fit, no set
            sk = key + "_src"
            if c.get(sk) == src:
                return
            c[sk] = src
            shown = Kit.fit(txt, room)
            Kit.set_text(lbl, shown, hue)
            cat = c.get(key + "_cat")
            if cat is None:
                return
            if shown == txt:
                tip = base or ""
            else:
                tip = ("%s. %s." % (txt, base)) if base else txt
            if tip != c.get(key + "_tip"):
                c[key + "_tip"] = tip
                try:
                    cat.SetTooltip(tip)
                except Exception:
                    pass

        def zcut(g, c, key, x, y, w, h=22):
            """(2.6.78) The tooltip area of label c[key] (see fit_set)."""
            c[key + "_cat"] = Kit.catcher(g, x - 2, y - 3, max(8, w + 4), h, lambda: None)
            c[key + "_tip"] = ""

        def build_zone(g, store, c, Z, k):
            """The sections of the window in a zone, from its plan (zone_plan),
            at scale k (only the text field needs it: the client never scales a
            field's text)."""
            M = Kit.MARGIN
            IW = Z["IW"]
            x0 = M
            metrics(IW, zone=True)                    # the list's columns for this width
            if "sum" in Z:
                y0, hh = Z["sum"]
                Kit.add_section(g, x0, y0, IW, hh)
                ry = y0 + 6
                if settings["sec_summary"]:
                    nl = 2 if Z["total2"] else 1
                    c["total"] = Kit.add_label(g, "", x0 + 12, ry + 3)
                    c["total_cat"] = Kit.catcher(g, x0 + 8, ry, IW - 16, 24 * nl - 2, lambda: None,
                                                 TOTAL_TIP)
                    c["total_tip"] = TOTAL_TIP
                    ry += 24
                    if Z["total2"]:
                        c["total2"] = Kit.add_label(g, "", x0 + 12, ry + 3)
                        ry += 24
                    rx = x0 + IW - 12 - cap_w("Reset")
                    c["session"] = Kit.add_label(g, "", x0 + 12, ry + 3)
                    if Z["sess_own"]:
                        c["session_w"] = IW - 28
                        zcut(g, c, "session", x0 + 12, ry + 3, c["session_w"])
                        ry += 24
                    else:
                        c["session_w"] = rx - x0 - 12 - 6
                        zcut(g, c, "session", x0 + 12, ry + 3, c["session_w"])
                    Kit.art_button(g, store, "newsess", Kit.ART_CLOSE, rx, ry - 1, "Reset",
                                   "Start a new session: gains count from now",
                                   on_click=queue("newsess"))
                    ry += 24
                if settings["sec_stats"]:
                    slot = Kit.text_w("Int 125 (+25)") + 8
                    places, (tx, tl) = Z["stats"]
                    c["stats"] = []
                    c["stat_cats"], c["stat_tips"] = [], [None, None, None]
                    for j, nm in enumerate(("Str", "Dex", "Int")):
                        sx, ln = places[j]
                        yy = ry + 24 * ln
                        lbl = Kit.add_label(g, "", x0 + sx, yy + 3)
                        c["stat_cats"].append(Kit.catcher(g, x0 + sx - 2, yy, slot - 4, 22,
                                                          queue("settings"), STAT_NAMES[j]))
                        pic = Kit.add_pic(g, LOCK_ART[0], x0 + sx + slot, yy + 5)
                        if pic is not None:
                            Kit.on_click(pic, queue(("stat", j)))
                            safe(lambda pic=pic, nm=nm: pic.SetTooltip(
                                "Set " + nm + " to go up, down or locked (click for the next)"))
                        c["stats"].append((lbl, pic))
                    c["stat_total"] = Kit.add_label(g, "", x0 + tx, ry + 24 * tl + 3, Kit.HUE_INFO)
                    c["stat_total_w"] = IW - 4 - tx
                    zcut(g, c, "stat_total", x0 + tx, ry + 24 * tl + 3, c["stat_total_w"])
            # ---- search row ----
            y0, hh = Z["tool"]
            T = Z["T"]
            Kit.add_section(g, x0, y0, IW, hh)
            Kit.add_label(g, "Find:", x0 + 12, y0 + 10)
            c["search"] = Kit.add_textbox(g, st["search"], x0 + T["tx"], y0 + 7, T["field"],
                                          numbers=False, font=max(8, int(round(16 * k))))
            safe(lambda: c["search"].SetTooltip("Type part of a skill name"))
            safe(lambda: c["search"].SetPlaceholder("search"))
            fx, fl = T["filter"]
            c["filter"] = Kit.art_button(g, store, "filter", Kit.ART_PAGE, x0 + fx, y0 + 7 + 28 * fl,
                                         FILTERS[settings["filter"]][1],
                                         "Which skills the list shows (click for the next choice)",
                                         on_click=queue("filter"))
            gx, gl = T["groups"]
            c["groups"] = Kit.add_check(g, "Groups", x0 + gx, y0 + 9 + 28 * gl, settings["groups"],
                                        "Show the client's skill groups (click a group to fold it)")
            # ---- the list ----
            build_list(g, c, x0, Z["list"][0], IW, Z["list"][1], Z["rows"])
            # ---- the lock buttons ----
            if "locks" in Z:
                y0, hh = Z["locks"]
                Kit.add_section(g, x0, y0, IW, hh)
                for (key, cap, tip), (bx, ln) in zip(LOCK_BTNS, Z["locks_p"]):
                    Kit.art_button(g, store, key, Kit.ART_OK, x0 + bx, y0 + 7 + 26 * ln, cap, tip,
                                   on_click=queue(key))
            # ---- the picked skill ----
            if "detail" in Z:
                y0, hh = Z["detail"]
                D = Z["D"]
                Kit.add_section(g, x0, y0, IW, hh)
                ry = y0 + 6
                aw = max(Kit.pic_size(a)[0] for a in LOCK_ART) or 12
                lx = x0 + IW - 12 - 3 * (aw + 10)
                c["d_name"] = Kit.add_label(g, "", x0 + 12, ry + 3, Kit.HUE_TITLE)
                c["d_name_w"] = lx - x0 - 12 - 8
                zcut(g, c, "d_name", x0 + 12, ry + 3, c["d_name_w"])
                c["d_locks"] = []
                for v in range(3):
                    p = Kit.add_pic(g, LOCK_ART[v], lx + v * (aw + 10), ry + 5)
                    if p is not None:
                        Kit.on_click(p, queue(("dlock", v)))
                        safe(lambda p=p, v=v: p.SetTooltip(LOCK_SET[v]))
                    c["d_locks"].append(p)
                ry += 24
                c["d_lw"] = IW - 28
                c["d_l1"] = Kit.add_label(g, "", x0 + 12, ry + 3)
                zcut(g, c, "d_l1", x0 + 12, ry + 3, c["d_lw"])
                ry += 24
                c["d_l2"] = Kit.add_label(g, "", x0 + 12, ry + 3, Kit.HUE_INFO)
                zcut(g, c, "d_l2", x0 + 12, ry + 3, c["d_lw"])
                ry += 24
                if settings["tips"]:                      # the training tip (2.6.05)
                    c["d_tip"] = Kit.add_label(g, "", x0 + 12, ry + 3, Kit.HUE_TEXT)
                    c["d_tip_cat"] = Kit.catcher(g, x0 + 8, ry, IW - 16, 22, lambda: None,
                                                 "Training tip for this skill's range")
                    c["d_tip_full"] = None
                    ry += 24
                Kit.add_label(g, "Target:", x0 + 12, ry + 3)
                c["target"] = Kit.add_textbox(g, "", x0 + D["tx"], ry, 56, numbers=False,
                                              font=max(8, int(round(16 * k))))
                safe(lambda: c["target"].SetTooltip("Real value this skill stops at (empty = none)"))
                safe(lambda: c["target"].SetPlaceholder("none"))
                c["d_tgt"] = Kit.add_label(g, "", x0 + D["tgt_x"], ry + 3, Kit.HUE_INFO)
                c["d_tgt_w"] = D["tgt_w"]
                zcut(g, c, "d_tgt", x0 + D["tgt_x"], ry + 3, c["d_tgt_w"])
                pin_tip = "Keep this skill at the top of the list (again to let it go)"
                if D["pin_here"]:
                    c["pin"] = Kit.art_button(g, store, "pin", Kit.ART_OK, x0 + D["pin_x"], ry - 1,
                                              "Pin", pin_tip, on_click=queue("pin"))
                ry += 24
                for key, (bx, ln) in D["btns"]:
                    by = ry - 1 + 24 * ln
                    if key == "use":
                        Kit.art_button(g, store, "use", Kit.ART_PLAY, x0 + bx, by, "Use",
                                       "Use this skill now", on_click=queue("use"))
                    elif key == "button":
                        Kit.art_button(g, store, "button", Kit.ART_PAGE, x0 + bx, by, "Make button",
                                       "Make the client's floating button for this skill "
                                       "(double-clicking it in the list does the same)",
                                       on_click=queue("mkbutton"))
                    elif key == "pin":
                        c["pin"] = Kit.art_button(g, store, "pin", Kit.ART_OK, x0 + bx, by, "Pin",
                                                  pin_tip, on_click=queue("pin"))
                    else:
                        Kit.art_button(g, store, "nextgrp", Kit.ART_PAGE, x0 + bx, by, "Next group",
                                       "Move this skill into the next skill group",
                                       on_click=queue("nextgrp"))
            # ---- the log ----
            if "log" in Z:
                y0, hh = Z["log"]
                Kit.add_section(g, x0, y0, IW, hh, "RECENT GAINS")
                c["log"] = []
                c["log_w"] = IW - 28
                for j in range(Z["log_n"]):
                    c["log"].append(Kit.add_label(g, "", x0 + 12, y0 + 26 + 20 * j, Kit.HUE_TEXT))
                    zcut(g, c, "log%d" % j, x0 + 12, y0 + 26 + 20 * j + 1, c["log_w"], 20)

        def brings_back():
            """What brings the window back once its Close hid it."""
            if settings["replace"]:
                return "the client's Skills button"
            return "the Action Bar's Skills button"

        def close_tip():
            """The Close button's tooltip: with "x_hides" on it only hides the window."""
            if settings["x_hides"]:
                return "Close %s (hides it; %s brings it back)" % (TITLE, brings_back())
            return "Close %s (turns it off; the Modules tab turns it back on)" % TITLE

        def _build_window():
            old, win["g"] = win["g"], None
            UIC.clear()
            st["desc"] = None
            st["rebuild"] = None
            if st["hidden"]:
                win.update({"c": {}, "rows": [], "rowmap": {}, "store": ({}, {})})
                Kit.dispose(old)
                return
            M = Kit.MARGIN
            store = ({}, {})
            c = {}
            st["resize_at"], st["preview"] = 0.0, False
            win["L"] = None
            L, Z = None, None
            fitst["k"], fitst["full"] = 1.0, None
            if st["minimized"] or st["docked"]:
                w, h = MINI_W, MINI_H
            elif fitst["slot"] is not None:               # (2.6.78) in a zone: exactly its slot
                w, h = fitst["slot"]
                lw, lh, k, Z = zone_geom(w, h)
            else:
                L = layout()
                w, h, IW = L["W"], L["H"], L["IW"]
                win["L"] = L
            x, y = Kit.load_pos(POS_KEY, (160, 120), (w, h))   # saved place, wholly on today's screen
            if Kit.is_open(old):
                x, y = old.GetX(), old.GetY()
            if Z is not None:
                g = G.CreateGump(True, True)              # no corner drags: the zone sizes it
                Kit.add_window_frame(g, lw, lh)
                Kit.title_bar(g, store, lw, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"), close_tip=close_tip())
                build_zone(g, store, c, Z, k)
                if k != 1.0:                              # too small: drawn smaller
                    wf = max(zone_min_w(), w)
                    fitst["k"], fitst["full"] = k, (int(wf), int(zone_plan(wf, 0)["need"]))
                    Kit.scale_window(g, k)
            elif L is None:
                g = G.CreateGump(True, True)
                c["mini"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"),
                                         close_tip=close_tip())
            else:
                x, y = Kit.clamp(x, y, w, h)              # (window rule 1, for a modern gump)
                try:                                      # resizable by its corners
                    g = G.CreateModernGump(x, y, w, h, True, L["min_w"], L["min_h"], on_resized)
                    safe(lambda: g.SetAlpha(0))           # its own panel hides under the stone
                except Exception:
                    g = G.CreateGump(True, True)          # a build without resizable windows
                    if not st["no_resize_told"]:          # said once: corner drags do nothing here
                        st["no_resize_told"] = True
                        API.SysMsg("%s: this client has no resizable windows: set the rows and "
                                   "the width on the settings page instead of dragging a corner."
                                   % TITLE, Kit.HUE_INFO)
                Kit.add_window_frame(g, w, h, mouse=False)    # corners free for the drag
                # ---- title (the standard title row, drawn here: a resizable window) ----
                Kit.add_section(g, M, M, IW, 30)
                Kit.add_label(g, TITLE.upper(), M + 30, M + 7, Kit.HUE_TITLE)
                Kit.note_title(g, M)                      # (2.6.78) for Check look
                zoned = Kit.zone_up(KEY)                  # (2.6.85) a window in a zone is always up
                x_set = w - M - (10 if zoned else 84 + Kit.DOCK_DX) - cap_w("Settings")
                if zoned:
                    Kit.catcher(g, M, M, x_set - M - 6, 30, lambda *a: None, None, movable=True)
                else:
                    Kit.title_catcher(g, M, M, x_set - M - 6, 30, queue("toggle_min"), key=KEY)
                Kit.art_button(g, store, "settings", Kit.ART_PAGE, x_set, M + 4, "Settings",
                               "Open the " + TITLE + " settings page",
                               on_click=queue("settings"))
                if not zoned:
                    Kit.dock_button(g, store, w - M - 74, M + 7, on_click=queue("to_bar"))
                    Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 74, M + 7, None,
                                   "Minimize (double-click the title does too)",
                                   on_click=queue("toggle_min"))
                    Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None,
                                   close_tip())
                if "sum" in L:
                    build_summary(g, store, c, M, L["sum"][0], IW)
                build_toolbar(g, store, c, M, L["tool"][0], IW)
                build_list(g, c, M, L["list"][0], IW, L["list"][1], L["rows"])
                if "locks" in L:
                    build_locks(g, store, M, L["locks"][0], IW)
                if "detail" in L:
                    build_detail(g, store, c, M, L["detail"][0], IW)
                if "log" in L:
                    build_log(g, c, M, L["log"][0], IW)
            Kit.place(g, x, y, w, h)                     # wholly on screen (at its new size too)
            if Z is not None and safe(lambda: HOST.layout_locked(KEY), False):
                safe(lambda: setattr(g, "CanMove", False))    # held in its zone
            win.update({"g": g, "c": c, "store": store, "rows": [], "rowmap": {},
                        "w": lw if Z is not None else w})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))
            if st["docked"]:
                safe(lambda: setattr(g, "IsVisible", False))    # the Action Bar stands in for it
            if settings["minimized"] != st["minimized"]:
                settings["minimized"] = st["minimized"]
                save_settings()
            show_target_text()
            read_groups()                                 # (not read while they weren't on show)
            rebuild_rows(time.time())
            refresh(time.time())
            Kit.dispose(old)

        # ---------- resizing (a corner drag) ----------
        def on_resized(*args):
            """A step of a corner drag (from the client, about every 75 ms). The
            window's own panel shows meanwhile, as a preview of the new size; the
            layout follows once the drag has settled (see apply_resize)."""
            st["resize_at"] = time.time()
            g = win["g"]
            L = win.get("L")
            if st["preview"] or L is None or not Kit.is_open(g) or st["minimized"] or st["docked"]:
                return
            if fitst["width"] is not None:                # (2.6.56) in a zone: the layout sizes it
                return
            try:                                          # only a real change of size shows the
                same = (int(g.GetWidth()), int(g.GetHeight())) == (L["W"], L["H"])
            except Exception:                             # preview (a client that reports the
                same = False                              # initial SetRect too would flash it)
            if not same:
                st["preview"] = True
                safe(lambda: g.SetAlpha(0.55))

        def apply_resize():
            """The corner drag was let go: the height dragged to sets the rows of
            the list, the width spreads the columns; both are saved with the
            settings (and shown on the settings page), and the window is drawn
            again at that size."""
            g = win["g"]
            L = win.get("L")
            st["preview"] = False
            if L is None or not Kit.is_open(g) or st["minimized"] or st["docked"]:
                return
            if fitst["width"] is not None:                # (2.6.56) in a zone: its size is the slot's
                safe(lambda: g.SetAlpha(0))
                return
            try:
                w, h = int(g.GetWidth()), int(g.GetHeight())
            except Exception:
                return
            lo, hi = LIMITS["rows"]
            rows = max(lo, min(hi, (h - L["fixed_h"] + ROW_H // 2) // ROW_H))
            width = w if w > L["min_w"] else 0            # at its narrowest: the natural width
            if fitst["width"] is not None:                # fitted to a zone: the zone has the width
                width = settings["width"]
            if rows == L["rows"] and width == settings["width"] and (w, h) == (L["W"], L["H"]):
                safe(lambda: g.SetAlpha(0))               # a drag that changed nothing
                return
            if rows != settings["rows"] or width != settings["width"]:
                settings["rows"], settings["width"] = rows, width
                save_settings()
                page["sync"] = True                       # the settings page's Rows field follows
            st["m"] = None
            st["rebuild"] = "window"
            touch()

        # ---------- sections ----------
        def build_summary(g, store, c, x0, y0, IW):
            Kit.add_section(g, x0, y0, IW, 6 + 24 * ((2 if settings["sec_summary"] else 0) +
                                                      (1 if settings["sec_stats"] else 0)) + 4)
            ry = y0 + 6
            if settings["sec_summary"]:
                c["total"] = Kit.add_label(g, "", x0 + 12, ry + 3)
                Kit.catcher(g, x0 + 8, ry, IW - 16, 22, lambda: None, TOTAL_TIP)
                ry += 24
                rx = x0 + IW - 12 - cap_w("Reset")
                c["session"] = Kit.add_label(g, "", x0 + 12, ry + 3)
                c["session_w"] = rx - x0 - 12 - 6
                Kit.art_button(g, store, "newsess", Kit.ART_CLOSE, rx, ry - 1, "Reset",
                               "Start a new session: gains count from now",
                               on_click=queue("newsess"))
                ry += 24
            if settings["sec_stats"]:
                slot = Kit.text_w("Int 125 (+25)") + 8
                c["stats"] = []
                c["stat_cats"], c["stat_tips"] = [], [None, None, None]
                sx = x0 + 12
                aw = Kit.pic_size(LOCK_ART[2])[0]
                for k, nm in enumerate(("Str", "Dex", "Int")):
                    lbl = Kit.add_label(g, "", sx, ry + 3)
                    # the session's gain per hour and the target (2.6.05), in its tooltip;
                    # a click opens the settings page, where the targets are set
                    c["stat_cats"].append(Kit.catcher(g, sx - 2, ry, slot - 4, 22,
                                                      queue("settings"), STAT_NAMES[k]))
                    pic = Kit.add_pic(g, LOCK_ART[0], sx + slot, ry + 5)
                    if pic is not None:
                        Kit.on_click(pic, queue(("stat", k)))
                        safe(lambda pic=pic, nm=nm: pic.SetTooltip(
                            "Set " + nm + " to go up, down or locked (click for the next)"))
                    c["stats"].append((lbl, pic))
                    sx += slot + (aw or 12) + 14
                c["stat_total"] = Kit.add_label(g, "", sx, ry + 3, Kit.HUE_INFO)
                c["stat_total_w"] = x0 + IW - 4 - sx

        def build_toolbar(g, store, c, x0, y0, IW):
            Kit.add_section(g, x0, y0, IW, 36)
            fx = x0 + 12
            Kit.add_label(g, "Find:", fx, y0 + 10)
            tx = fx + Kit.text_w("Find:") + 6
            c["search"] = Kit.add_textbox(g, st["search"], tx, y0 + 7, SEARCH_W, numbers=False)
            safe(lambda: c["search"].SetTooltip("Type part of a skill name"))
            safe(lambda: c["search"].SetPlaceholder("search"))
            bx = tx + SEARCH_W + 14
            c["filter"] = Kit.art_button(g, store, "filter", Kit.ART_PAGE, bx, y0 + 7,
                                         FILTERS[settings["filter"]][1],
                                         "Which skills the list shows (click for the next choice)",
                                         on_click=queue("filter"))
            cx = x0 + IW - 12 - 24 - Kit.text_w("Groups")
            c["groups"] = Kit.add_check(g, "Groups", cx, y0 + 9, settings["groups"],
                                        "Show the client's skill groups (click a group to fold it)")

        def build_list(g, c, x0, y0, IW, h, rows):
            m = metrics()
            Kit.add_section(g, x0, y0, IW, h)
            sx = x0 + 8
            c["hdr"] = {}
            heads = [("name", "Skill", m["name_x"]), ("real", "Real", m["real_x"]),
                     ("value", "Value", m["val_x"]), ("cap", "Cap", m["cap_x"]),
                     ("gain", "Gain", m["gain_x"])]
            tips = {"name": "Sort by name", "real": "Sort by real value, without item bonuses",
                    "value": "Sort by value with bonuses", "cap": "Sort by cap",
                    "gain": "Sort by gain this session"}
            nxt = {"name": m["real_x"] or m["val_x"], "real": m["val_x"], "value": m["cap_x"] or m["bar_x"]
                   or m["gain_x"] or m["lock_x"], "cap": m["bar_x"] or m["gain_x"] or m["lock_x"],
                   "gain": m["lock_x"]}
            for key, text, cx in heads:
                if cx is None:
                    continue
                lbl = Kit.add_label(g, text, sx + cx, y0 + 6, Kit.HUE_INFO)
                Kit.catcher(g, sx + cx - 2, y0 + 3, (nxt[key] or cx + 40) - cx - 2, 20,
                            queue(("sort", key)), tips[key] + " (click again to reverse)")
                c["hdr"][key] = lbl
            lp = Kit.add_pic(g, LOCK_ART[2], sx + m["lock_x"], y0 + 7)
            if lp is not None:
                Kit.on_click(lp, queue(("sort", "lock")))
                safe(lambda: lp.SetTooltip("Sort by lock (click again to reverse)"))
            c["hdr"]["lock_pic"] = lp
            c["arrow"] = Kit.add_pic(g, LOCK_ART[1], sx, y0 + 8, mouse=False)
            try:
                sa = G.CreateGumpScrollArea(sx, y0 + 26, m["sa_w"], rows * ROW_H)
                g.Add(sa)
            except Exception:
                sa = None
            c["sa"] = sa
            c["sa_g"] = g                                 # no scroll area: rows go on the window
            c["sa_xy"] = (sx, y0 + 26)
            c["list_rows"] = rows

        def build_locks(g, store, x0, y0, IW):
            Kit.add_section(g, x0, y0, IW, 36)
            bx = x0 + 12
            for key, cap, tip in LOCK_BTNS:
                Kit.art_button(g, store, key, Kit.ART_OK, bx, y0 + 7, cap, tip,
                               on_click=queue(key))
                bx += cap_w(cap) + 10

        def build_detail(g, store, c, x0, y0, IW):
            Kit.add_section(g, x0, y0, IW, 6 + 24 * detail_rows() + 4)
            ry = y0 + 6
            aw = max(Kit.pic_size(a)[0] for a in LOCK_ART) or 12
            lx = x0 + IW - 12 - 3 * (aw + 10)
            c["d_name"] = Kit.add_label(g, "", x0 + 12, ry + 3, Kit.HUE_TITLE)
            c["d_name_w"] = lx - x0 - 12 - 8
            c["d_locks"] = []
            for v in range(3):
                p = Kit.add_pic(g, LOCK_ART[v], lx + v * (aw + 10), ry + 5)
                if p is not None:
                    Kit.on_click(p, queue(("dlock", v)))
                    safe(lambda p=p, v=v: p.SetTooltip(LOCK_SET[v]))
                c["d_locks"].append(p)
            ry += 24
            c["d_l1"] = Kit.add_label(g, "", x0 + 12, ry + 3)
            ry += 24
            c["d_l2"] = Kit.add_label(g, "", x0 + 12, ry + 3, Kit.HUE_INFO)
            c["d_lw"] = IW - 28
            ry += 24
            if settings["tips"]:                          # the training tip (2.6.05)
                c["d_tip"] = Kit.add_label(g, "", x0 + 12, ry + 3, Kit.HUE_TEXT)
                c["d_tip_cat"] = Kit.catcher(g, x0 + 8, ry, IW - 16, 22, lambda: None,
                                             "Training tip for this skill's range")
                c["d_tip_full"] = None                    # the catcher's tooltip, as last set
                ry += 24
            Kit.add_label(g, "Target:", x0 + 12, ry + 3)
            tx = x0 + 12 + Kit.text_w("Target:") + 8
            c["target"] = Kit.add_textbox(g, "", tx, ry, 56, numbers=False)
            safe(lambda: c["target"].SetTooltip("Real value this skill stops at (empty = none)"))
            safe(lambda: c["target"].SetPlaceholder("none"))
            px = x0 + IW - 12 - cap_w("Unpin")
            c["d_tgt"] = Kit.add_label(g, "", tx + 56 + 12, ry + 3, Kit.HUE_INFO)
            c["d_tgt_w"] = px - (tx + 56 + 12) - 6
            c["pin"] = Kit.art_button(g, store, "pin", Kit.ART_OK, px, ry - 1, "Pin",
                                      "Keep this skill at the top of the list (again to let it go)",
                                      on_click=queue("pin"))
            ry += 24
            bx = x0 + 12
            Kit.art_button(g, store, "use", Kit.ART_PLAY, bx, ry - 1, "Use", "Use this skill now",
                           on_click=queue("use"))
            bx += cap_w("Use") + 12
            Kit.art_button(g, store, "button", Kit.ART_PAGE, bx, ry - 1, "Make button",
                           "Make the client's floating button for this skill (double-clicking "
                           "it in the list does the same)",
                           on_click=queue("mkbutton"))
            Kit.art_button(g, store, "nextgrp", Kit.ART_PAGE, x0 + IW - 12 - cap_w("Next group"),
                           ry - 1, "Next group", "Move this skill into the next skill group",
                           on_click=queue("nextgrp"))

        def build_log(g, c, x0, y0, IW):
            Kit.add_section(g, x0, y0, IW, 26 + 20 * settings["log_lines"] + 4, "RECENT GAINS")
            c["log"] = [Kit.add_label(g, "", x0 + 12, y0 + 26 + 20 * k, Kit.HUE_TEXT)
                        for k in range(settings["log_lines"])]
            c["log_w"] = IW - 28

        # ---------- the rows ----------
        #  Every skill (and group header) has ONE row of controls, made the first
        #  time it is shown and kept while the window lives: a new order (sorting
        #  by gain while training, a filter, typing in the search box, folding a
        #  group) only moves rows to their new place and hides the ones left out.
        #  It used to clear the list and make every row again (about 10 controls a
        #  skill, ~580 for the whole list) on each of those - a frame hitch each
        #  time. A row's click handlers belong to its skill, as before. Hidden rows
        #  are parked at the top of the list so they never stretch its scrolling.
        def _row_origin():
            c = win["c"]
            if c.get("sa") is not None:
                return c["sa"], 0, 0
            return c["sa_g"], c["sa_xy"][0], c["sa_xy"][1]

        def move_row(r, y):
            if r["y"] == y:
                return
            r["y"] = y
            zk = fitst["k"]                               # (2.6.78) a window drawn smaller
            for ctl, x, dy in r["parts"]:
                try:
                    if zk == 1.0:
                        Kit.ui_pos(ctl, x, y + dy)
                    else:
                        ctl.SetPos(int(round(x * zk)), int(round((y + dy) * zk)))
                except Exception:
                    pass

        def show_row(r, on):
            if r["hidden"] == (not on):
                return
            r["hidden"] = not on
            for ctl, _, _ in r["parts"]:
                if ctl is r.get("bar"):
                    if not on:                              # (shown again by refresh_rows)
                        setp(ctl, "IsVisible", False)
                else:
                    setp(ctl, "IsVisible", on)
            if on:
                r["sig"] = None                             # values may have moved meanwhile

        def rebuild_rows(now):
            """Put the rows in the order (and selection) the list shows now. The
            list is worked out again only when something it depends on changed
            (see touch) or, with the "gaining now" filter, once a second."""
            c = win["c"]
            if "sa_xy" not in c:
                return
            key = (st["ver"], GR["ver"],
                   int(now) if FILTERS[settings["filter"]][0] == "gaining" else 0)
            if st["desc"] is not None and key == st["desc_key"]:
                return
            st["desc_key"] = key
            desc = descriptors(now)
            if desc == st["desc"]:
                return
            st["desc"] = desc
            m = metrics()
            tgt, ox, oy = _row_origin()
            made = len(win["rowmap"]) + (0 if "selbox" in c else 1) + (0 if c.get("empty") else 1)
            limit = len(desc) if c.get("sa") is not None else c.get("list_rows", settings["rows"])
            if "selbox" not in c:                         # first: drawn under the rows
                c["selbox"] = Kit.add_box(tgt, ox, oy, m["row_w"], ROW_H - 1, SEL_ALPHA, SEL_COLOR)
                setp(c["selbox"], "IsVisible", False)
            empty = "" if desc else ("No skill matches; change the search or the filter."
                                     if SK["n"] else "Waiting for the server to send your skills.")
            if c.get("empty") is None and empty:          # made the first time it's needed
                c["empty"] = Kit.add_label(tgt, empty, ox + m["name_x"], oy + 3, Kit.HUE_INFO)
            if c.get("empty") is not None:
                Kit.set_text(c["empty"], empty)
                setp(c["empty"], "IsVisible", bool(empty))
            rowmap = win["rowmap"]
            rows, want, nth = [], set(), {}
            for n, d in enumerate(desc[:limit]):
                ry = oy + n * ROW_H
                k = (d[0], d[1])
                nth[k] = c_k = nth.get(k, -1) + 1         # a pinned skill is listed twice with groups on
                k = (d[0], d[1], c_k)                     # (under "Pinned" and in its own group)
                r = rowmap.get(k)
                if r is None:
                    if d[0] == "g":
                        r = build_group_row(tgt, ox, ry, d, m)
                    else:
                        r = build_skill_row(tgt, ox, ry, d[1], m)
                    rowmap[k] = r
                else:
                    move_row(r, ry)
                    show_row(r, True)
                if d[0] == "g":
                    setp(r["arrow"], "Graphic", GROUP_SHUT if d[2] else GROUP_OPEN)
                want.add(k)
                rows.append(r)
            for k, r in rowmap.items():
                if k not in want and not r["hidden"]:
                    show_row(r, False)
                    move_row(r, oy)
            win["rows"] = rows
            if fitst["k"] != 1.0 and made != len(rowmap) + (0 if "selbox" in c else 1) + \
                    (0 if c.get("empty") else 1):         # (2.6.78) new controls: drawn smaller too
                Kit.scale_window(win["g"], fitst["k"])
            place_selbox()

        def build_group_row(tgt, ox, ry, d, m):
            key, shut = d[1], d[2]
            r = {"kind": "g", "key": key, "y": ry, "hidden": False, "parts": [], "sig": None}

            def put(ctl, x, dy):
                if ctl is not None:
                    r["parts"].append((ctl, x, dy))
                return ctl
            put(Kit.add_box(tgt, ox, ry + 1, m["row_w"], ROW_H - 2, GROUP_ALPHA, GROUP_COLOR), ox, 1)
            r["arrow"] = put(Kit.add_pic(tgt, GROUP_SHUT if shut else GROUP_OPEN, ox + 4, ry + 5,
                                         mouse=False), ox + 4, 5)
            remember(r["arrow"], "Graphic", GROUP_SHUT if shut else GROUP_OPEN)
            r["lbl"] = put(Kit.add_label(tgt, "", ox + m["name_x"], ry + 3, Kit.HUE_TITLE),
                           ox + m["name_x"], 3)
            r["real"] = put(Kit.add_label(tgt, "", ox + m["real_x"], ry + 3, Kit.HUE_INFO),
                            ox + m["real_x"], 3) if m["real_x"] is not None else None
            r["val"] = put(Kit.add_label(tgt, "", ox + m["val_x"], ry + 3, Kit.HUE_INFO),
                           ox + m["val_x"], 3)
            r["gain"] = put(Kit.add_label(tgt, "", ox + m["gain_x"], ry + 3, Kit.HUE_INFO),
                            ox + m["gain_x"], 3) if m["gain_x"] is not None else None
            put(Kit.catcher(tgt, ox, ry, m["row_w"], ROW_H - 1, queue(("fold", key)),
                            "Fold or unfold this group"), ox, 0)
            return r

        def build_skill_row(tgt, ox, ry, i, m):
            r = {"kind": "s", "i": i, "y": ry, "hidden": False, "parts": [], "sig": None}

            def put(ctl, x, dy):
                if ctl is not None:
                    r["parts"].append((ctl, x, dy))
                return ctl
            r["name"] = put(Kit.add_label(tgt, row_name(i, m),
                                          ox + m["name_x"], ry + 3), ox + m["name_x"], 3)
            r["real"] = put(Kit.add_label(tgt, "", ox + m["real_x"], ry + 3), ox + m["real_x"], 3) \
                if m["real_x"] is not None else None
            r["val"] = put(Kit.add_label(tgt, "", ox + m["val_x"], ry + 3), ox + m["val_x"], 3)
            r["cap"] = put(Kit.add_label(tgt, "", ox + m["cap_x"], ry + 3, Kit.HUE_INFO),
                           ox + m["cap_x"], 3) if m["cap_x"] is not None else None
            r["gain"] = put(Kit.add_label(tgt, "", ox + m["gain_x"], ry + 3, Kit.HUE_GOOD),
                            ox + m["gain_x"], 3) if m["gain_x"] is not None else None
            r["bar"] = None
            if m["bar_x"] is not None:
                bdy = (ROW_H - m["bar_h"]) // 2
                by = ry + bdy
                if Kit.pic_size(Kit.LINE_RED)[0] > 0:
                    put(Kit.add_tiled(tgt, Kit.LINE_RED, ox + m["bar_x"], by, m["bar_w"],
                                      m["bar_h"], hue=BAR_BG_HUE), ox + m["bar_x"], bdy)
                else:
                    put(Kit.add_tiled(tgt, Kit.SECTION_TILE, ox + m["bar_x"], by, m["bar_w"],
                                      m["bar_h"], 1.0), ox + m["bar_x"], bdy)
                r["bar"] = put(Kit.add_tiled(tgt, Kit.LINE_BLUE, ox + m["bar_x"], by, 1, m["bar_h"]),
                               ox + m["bar_x"], bdy)
            tip = "Click: pick it (details below); double-click: its floating button" \
                if SK["click"][i] else "Click: pick it (details below)"
            r["cat"] = put(Kit.catcher(tgt, ox + m["name_x"] - 2, ry, m["lock_x"] - m["name_x"] - 2,
                                       ROW_H - 1, row_click(i), tip), ox + m["name_x"] - 2, 0)
            r["tip0"] = r["cat_tip"] = tip                # its tooltip without / with the tip
            r["use"] = None
            if SK["click"][i]:
                b = G.CreateGumpButton("", Kit.HUE_TEXT, GEM[0], GEM[1], GEM[2])
                b.SetPos(ox + 4, ry + 6)
                tgt.Add(b)
                Kit.on_click(b, queue(("use", i)))
                safe(lambda: b.SetTooltip("Use " + SK["names"][i]))
                r["use"] = put(b, ox + 4, 6)
            r["lock"] = put(Kit.add_pic(tgt, LOCK_ART[0], ox + m["lock_x"], ry + 4),
                            ox + m["lock_x"], 4)
            r["tip"] = None                               # the lock arrow's tooltip, as last set
            if r["lock"] is not None:
                Kit.on_click(r["lock"], queue(("lock", i)))
                remember(r["lock"], "Graphic", LOCK_ART[0])
            return r

        def row_name(i, m=None):
            """A skill's name as its row shows it: (2.6.78) cut to the name column
            in a zone too narrow for the whole names."""
            nm = SK["names"][i] if i < SK["n"] else "?"
            m = m or metrics()
            if m.get("cut"):
                return Kit.fit(nm, m["name_w"] - 10)
            return nm

        def place_selbox():
            box = win["c"].get("selbox")
            if box is None:
                return
            y = None
            sel = st["sel"]
            if sel is not None:
                for r in win["rows"]:
                    if r["kind"] == "s" and r["i"] == sel:
                        y = r["y"]
                        break
            if y is None:
                setp(box, "IsVisible", False)
            else:
                ox = 0 if win["c"].get("sa") is not None else win["c"]["sa_xy"][0]
                setp(box, "Pos", (ox, y))
                setp(box, "IsVisible", True)

        # ---------- refreshing what is on screen ----------
        def name_hue(i, now):
            if st["hl"].get(i, 0) > now:
                return Kit.HUE_GOOD
            if i in marks["pins"]:
                return Kit.HUE_TITLE
            return Kit.HUE_TEXT

        def refresh_rows(now):
            """The shown rows' numbers. A row whose skill, gain and name colour are
            what it already shows is passed over (most rows, most seconds)."""
            cur = SK["cur"]
            n = SK["n"]
            has_gain = settings["col_gain"]
            tips_on = settings["tips"]
            bar_w = metrics()["bar_w"]
            for r in win["rows"]:
                if r["kind"] == "g":
                    refresh_group_row(r)
                    continue
                i = r["i"]
                if i >= n:
                    continue
                base, val, cap, lock = cur[i]
                hue = name_hue(i, now)
                sig = (base, val, cap, lock, sgain(i) if has_gain else 0, hue)
                if sig == r["sig"]:
                    continue
                r["sig"] = sig
                Kit.set_text(r["name"], row_name(i), hue)
                if r["real"] is not None:
                    Kit.set_text(r["real"], f1(base),
                                 Kit.HUE_GOOD if cap and base >= cap else Kit.HUE_TEXT)
                bonus = val - base
                Kit.set_text(r["val"], f1(val), Kit.HUE_GOOD if bonus > 0 else (
                    Kit.HUE_BAD if bonus < 0 else Kit.HUE_TEXT))
                if r["cap"] is not None:
                    Kit.set_text(r["cap"], f1(cap))
                if r["gain"] is not None:
                    gn = sgain(i)
                    Kit.set_text(r["gain"], ("%+.1f" % (gn / 10.0)) if gn else "",
                                 Kit.HUE_GOOD if gn > 0 else Kit.HUE_BAD)
                if r["lock"] is not None:
                    setp(r["lock"], "Graphic", LOCK_ART[lock])
                    tip = "%s (click: %s)" % (LOCK_TEXT[lock], LOCK_TEXT[(lock + 1) % 3].lower())
                    if r.get("tip") != tip:               # kept in the row, not an id()-keyed cache
                        r["tip"] = tip
                        try:
                            r["lock"].SetTooltip(tip)
                        except Exception:
                            pass
                if tips_on:                               # the training tip (2.6.05)
                    tp = tip_for(i)
                    ct = r["tip0"] if tp is None else "%s\n%s %s: %s" % (
                        r["tip0"], SK["names"][i], tp[0], tp[1])
                    if ct != r["cat_tip"]:
                        r["cat_tip"] = ct
                        try:
                            r["cat"].SetTooltip(ct)
                        except Exception:
                            pass
                if r["bar"] is not None:
                    fw = int(bar_w * min(1.0, float(val) / cap)) if cap > 0 else 0
                    setp(r["bar"], "Width", max(1, fw))
                    setp(r["bar"], "IsVisible", fw > 0)
                    setp(r["bar"], "Graphic", LINE_GREEN if cap and base >= cap else Kit.LINE_BLUE)

        GOTHER = {"list": None, "n": -1, "mem": []}   # 2.6.82: "Other"'s members, per group read

        def group_info(key):
            if key == "pin":
                return "Pinned", [i for i in range(SK["n"]) if i in marks["pins"]]
            if key == "other":
                if GOTHER["list"] is not GR["list"] or GOTHER["n"] != SK["n"]:
                    of = GR["of"]
                    GOTHER.update({"list": GR["list"], "n": SK["n"],
                                   "mem": [i for i in range(SK["n"]) if i not in of]})
                return "Other", GOTHER["mem"]
            if isinstance(key, int) and key < len(GR["list"]):
                g = GR["list"][key]
                return g["name"] or "(no name)", g["members"]
            return "?", []

        def refresh_group_row(r):
            name, mem = group_info(r["key"])
            m = metrics()
            n = SK["n"]
            cur = SK["cur"]
            tr = tv = gn = 0
            for i in mem:
                if i < n:
                    c = cur[i]
                    tr += c[0]
                    tv += c[1]
                    if r["gain"] is not None:
                        gn += sgain(i)
            room = (m["real_x"] or m["val_x"]) - m["name_x"] - 6
            sig = (name, len(mem), room, tr, tv, gn)      # 2.6.82: an unchanged row is passed over
            if r.get("gsig") == sig:
                return
            r["gsig"] = sig
            Kit.set_text(r["lbl"], Kit.fit("%s (%d)" % (name, len(mem)), room))
            if r["real"] is not None:
                Kit.set_text(r["real"], f1(tr))
            Kit.set_text(r["val"], f1(tv))
            if r["gain"] is not None:
                Kit.set_text(r["gain"], ("%+.1f" % (gn / 10.0)) if gn else "")

        def refresh_header():
            c = win["c"]
            hdr = c.get("hdr")
            if not hdr:
                return
            m = metrics()
            s = settings["sort"]
            hk = (s, settings["asc"], m)                  # 2.6.82: redone only when the sort moved
            old = c.get("hdr_k")
            if old is not None and old[0] == s and old[1] == hk[1] and old[2] is m:
                return
            c["hdr_k"] = hk
            names = {"name": ("Skill", m["name_x"]), "real": ("Real", m["real_x"]),
                     "value": ("Value", m["val_x"]), "cap": ("Cap", m["cap_x"]),
                     "gain": ("Gain", m["gain_x"])}
            for key, lbl in hdr.items():
                if key != "lock_pic":
                    Kit.set_text(lbl, names[key][0], Kit.HUE_TITLE if key == s else Kit.HUE_INFO)
            arrow = c.get("arrow")
            if arrow is None:
                return
            sx = c["sa_xy"][0]
            if s == "lock":
                ax = sx + m["lock_x"] - m["arrow_w"] - 3
            elif names.get(s, (None, None))[1] is not None:
                text, cx = names[s]
                ax = sx + cx + Kit.text_w(text) + 3
            else:
                setp(arrow, "IsVisible", False)
                return
            y0 = c["sa_xy"][1] - 26
            setp(arrow, "Pos", (ax, y0 + 8))
            setp(arrow, "Graphic", LOCK_ART[0] if settings["asc"] else LOCK_ART[1])
            setp(arrow, "IsVisible", True)

        LOGTXT = {}                           # 2.6.82: log entry -> its line (capped)

        def refresh(now):
            c = win["c"]
            if not c:
                return
            tr = total_real()
            if c.get("mini") is not None:
                if st["docked"]:                          # 2.6.82: folded: nothing on screen to set
                    return
                txt = "%s: %s / %s %+.1f" % (TITLE, f1(tr), f1(settings["total_cap"]),
                                              total_gain() / 10.0)
                if not st["ready"]:
                    txt = "%s: waiting for your skills" % TITLE
                Kit.set_text(c["mini"], Kit.fit(txt, MINI_W - 90),
                             Kit.HUE_BAD if settings["cap_warn"] and st["warned_cap"] else Kit.HUE_INFO)
                return
            refresh_header()
            refresh_rows(now)
            place_selbox()
            IWt = win.get("w", 400) - 2 * Kit.MARGIN - 24
            if c.get("total") is not None:
                tv = sum(x[1] for x in SK["cur"])
                free = settings["total_cap"] - tr
                if st["warned_cap"]:
                    a = "Total %s / %s: at the cap" % (f1(tr), f1(settings["total_cap"]))
                    b, sep = "set a skill to go down", ", "
                    hue = Kit.HUE_BAD
                else:
                    a = "Total %s / %s   (%s free)" % (f1(tr), f1(settings["total_cap"]),
                                                     f1(max(0, free)))
                    b, sep = "with bonuses %s" % f1(tv), "   "
                    hue = Kit.HUE_TEXT
                txt = a + sep + b
                if c.get("total2") is not None:           # (2.6.78) two lines in a narrow zone
                    sa, sb = Kit.fit(a, IWt), Kit.fit(b, IWt)
                    Kit.set_text(c["total"], sa, hue)
                    Kit.set_text(c["total2"], sb, hue)
                    tip = TOTAL_TIP if (sa, sb) == (a, b) else "%s. %s." % (txt, TOTAL_TIP)
                    if tip != c.get("total_tip"):
                        c["total_tip"] = tip
                        safe(lambda: c["total_cat"].SetTooltip(tip))
                else:
                    fit_set(c, "total", txt, IWt, hue, TOTAL_TIP)
            if c.get("session") is not None:
                tg = total_gain()
                hrs = hours_running()
                txt = "Session %+.1f in %s   (%.1f / hour)" % (tg / 10.0,
                                                              dur(now - sess["start"]),
                                                              tg / 10.0 / hrs)
                fit_set(c, "session", txt, c["session_w"], Kit.HUE_GOOD if tg > 0 else Kit.HUE_INFO)
            if c.get("stats"):
                base = sess["stats"] or STATS["cur"]
                hrs = hours_running()
                cats, tips = c.get("stat_cats") or (), c.get("stat_tips")
                for k, (lbl, pic) in enumerate(c["stats"]):
                    v = STATS["cur"][k]
                    d = v - base[k] if sess["stats"] else 0
                    Kit.set_text(lbl, "%s %d%s" % (("Str", "Dex", "Int")[k], v,
                                                  (" (%+d)" % d) if d else ""),
                                 Kit.HUE_GOOD if d > 0 else Kit.HUE_TEXT)
                    setp(pic, "Graphic", LOCK_ART[STATS["locks"][k]])
                    if k < len(cats):                     # gain per hour and target (2.6.05)
                        tip = stat_tip(k, hrs)
                        if tip != tips[k]:
                            tips[k] = tip
                            try:
                                cats[k].SetTooltip(tip)
                            except Exception:
                                pass
                tot = sum(STATS["cur"])
                cap = STATS["cap"]
                txt = ("Stats %d / %d" % (tot, cap)) if cap else ("Stats %d" % tot)
                tg = (stat_gain(0) + stat_gain(1) + stat_gain(2)) if sess["stats"] else 0
                if tg:                                    # the session's stat gain, when it fits
                    more = "%s   %+d (%.1f / hour)" % (txt, tg, tg / hrs)
                    if Kit.text_px(more) <= c["stat_total_w"]:
                        txt = more
                fit_set(c, "stat_total", txt, c["stat_total_w"],
                        Kit.HUE_GOOD if cap and tot >= cap else Kit.HUE_INFO)
            refresh_detail(now)
            if c.get("log") is not None:
                lines = st["log"][-len(c["log"]):][::-1]
                for k, lbl in enumerate(c["log"]):
                    if k < len(lines):
                        e = lines[k]
                        d = e[2]                            # 2.6.83: the entry's own gain, every line
                        txt = LOGTXT.get(e)                 # 2.6.82: one format per log entry
                        if txt is None:
                            t, name, _g, nb = e
                            txt = "%s  %s %s%s  (%s)" % (time.strftime("%H:%M", time.localtime(t)),
                                                         name, "+" if d > 0 else "-", f1(abs(d)),
                                                         f1(nb))
                            if len(LOGTXT) >= 2 * LOG_KEEP:
                                LOGTXT.clear()
                            LOGTXT[e] = txt
                        fit_set(c, "log%d" % k, txt, c["log_w"],
                                Kit.HUE_GOOD if d > 0 else Kit.HUE_BAD, lbl=lbl)
                    else:
                        fit_set(c, "log%d" % k, "No gains yet this session." if k == 0 and not lines
                                else "", c["log_w"], Kit.HUE_INFO, lbl=lbl)

        def refresh_detail(now):
            c = win["c"]
            if c.get("d_name") is None:
                return
            i = st["sel"]
            if i is None or i >= SK["n"]:
                fit_set(c, "d_name", "No skill picked", c["d_name_w"])
                fit_set(c, "d_l1", "Click a skill in the list to see it here.", c["d_lw"],
                        Kit.HUE_INFO)
                fit_set(c, "d_l2", "", c["d_lw"])
                fit_set(c, "d_tgt", "", c["d_tgt_w"])
                if c.get("d_tip") is not None:
                    Kit.set_text(c["d_tip"], "")
                    if c["d_tip_full"] is not None:       # (no older tip left in its tooltip)
                        c["d_tip_full"] = None
                        try:
                            c["d_tip_cat"].SetTooltip("Training tip for this skill's range")
                        except Exception:
                            pass
                for p in c["d_locks"]:
                    setp(p, "Hue", DIM_HUE)
                return
            base, val, cap, lock = SK["cur"][i]
            gi = group_of(i)
            gname = GR["list"][gi]["name"] if gi is not None else ""
            fit_set(c, "d_name", SK["names"][i] + ("   (%s)" % gname if gname else ""),
                    c["d_name_w"], Kit.HUE_TITLE)
            for v, p in enumerate(c["d_locks"]):
                setp(p, "Hue", 0 if v == lock else DIM_HUE)
            bonus = val - base
            l1 = "Real %s   Value %s%s   Cap %s   %s" % (
                f1(base), f1(val), (" (%+.1f)" % (bonus / 10.0)) if bonus else "", f1(cap),
                ("To cap %s" % f1(cap - base)) if base < cap else "At cap")
            fit_set(c, "d_l1", l1, c["d_lw"], Kit.HUE_TEXT)
            rt = rates(i, now)
            avg, recent = rt
            l2 = "Session %+.1f   %.1f / hour   last %d min %.1f / hour   cap %s" % (
                sgain(i) / 10.0, avg / 10.0, settings["rate_min"], recent / 10.0, eta(i, now, rt))
            fit_set(c, "d_l2", l2, c["d_lw"], Kit.HUE_INFO)
            if c.get("d_tip") is not None:                # the training tip (2.6.05)
                tp = tip_for(i)
                if tp is not None:
                    full, hue = "Tip %s: %s" % tp, Kit.HUE_TEXT
                else:
                    full, hue = "No tip for this range (TIPS in the Skills file)", Kit.HUE_INFO
                Kit.set_text(c["d_tip"], Kit.fit(full, c["d_lw"]), hue)
                if full != c["d_tip_full"]:
                    c["d_tip_full"] = full
                    try:
                        c["d_tip_cat"].SetTooltip(full)
                    except Exception:
                        pass
            tgt = marks["targets"].get(i)
            if tgt:
                if base >= tgt:
                    txt, hue = "reached", Kit.HUE_GOOD
                else:
                    txt = "%s to go%s" % (f1(tgt - base), ", then locks"
                                          if settings["lock_at_target"] else "")
                    hue = Kit.HUE_INFO
            else:
                txt, hue = "none set", Kit.HUE_INFO
            fit_set(c, "d_tgt", txt, c["d_tgt_w"], hue)
            if c.get("pin") is not None:
                Kit.set_text(c["pin"], "Unpin" if i in marks["pins"] else "Pin")

        def show_target_text():
            """Put the picked skill's target in the box (when the pick changed)."""
            c = win["c"]
            tb = c.get("target")
            if tb is None:
                st["tgt_shown"] = None
                return
            i = st["sel"]
            txt = f1(marks["targets"][i]) if i is not None and i in marks["targets"] else ""
            try:
                tb.SetText(txt)
            except Exception:
                safe(lambda: setattr(tb, "Text", txt))
            st["tgt_shown"] = (i, txt)

        def poll_fields(now):
            """The search box and the target box (read on the client thread).
            True when something in them changed."""
            c = win["c"]
            moved = False
            sb = c.get("search")
            if sb is not None:
                try:                                      # (every tick: no safe(lambda))
                    q = str(sb.Text or "").strip().lower()
                except Exception:
                    q = st["search"]
                if q != st["search"]:
                    st["search"], moved = q, True
            tb = c.get("target")
            if tb is not None and st["tgt_shown"] is not None:
                i, shown = st["tgt_shown"]
                try:
                    txt = str(tb.Text or "").strip()
                except Exception:
                    txt = shown
                if txt != shown and i is not None and i == st["sel"]:
                    st["tgt_shown"] = (i, txt)
                    try:
                        v = int(round(float(txt.replace(",", ".")) * 10)) if txt else 0
                    except ValueError:
                        v = None
                    if v is not None:
                        v = max(0, min(2000, v))
                        if v:
                            marks["targets"][i] = v
                        else:
                            marks["targets"].pop(i, None)
                        save_marks()
                        moved = True
            cb = c.get("groups")
            if cb is not None:
                try:
                    on = bool(cb.IsChecked)
                except Exception:
                    on = settings["groups"]
                if on != settings["groups"]:
                    settings["groups"] = on
                    save_settings()
                    if on:
                        read_groups(True)                 # (not read while they weren't on show)
                    moved = True
            return moved

        # ---------- the client's own skills window ----------
        def gumps_sig():
            """(how many windows the client has, the front one): a window that
            opens changes it. None when the client's list can't be read."""
            try:
                lst = VG["gumps"]
                if lst is None:
                    lst = VG["gumps"] = Tz.get(None, "Gumps",
                                               Tz.T("ClassicUO.Game.Managers.UIManager"))
                return (int(lst.Count), lst.First)
            except Exception:
                VG["gumps"] = None
                return None

        VANILLA_FULL_EVERY = 3.0              # 2.6.82: s between full looks with no change seen (was 1)

        def vanilla_check():
            """While "replace" is on, the client's skills window is closed the
            moment it opens and this one comes up instead. Looking through every
            window the client has (each one's type name) four times a second was
            most of this module's idle cost: now the full look runs only when the
            client's window list changed (count or front window) and once a
            second besides."""
            if not settings["replace"] and time.time() > st["swallow_until"]:
                return
            now = time.time()
            sig = gumps_sig()
            if sig is not None and sig == VG["sig"] and now < VG["full_at"]:
                return
            VG["sig"], VG["full_at"] = sig, now + VANILLA_FULL_EVERY
            VG["gumps"] = None                            # (the list itself is looked up afresh too)
            found = safe(lambda: Tz.windows(VANILLA), []) or []
            if not found:
                return
            VG["sig"] = None                              # they go away: look again next tick
            for gmp in found:
                safe(lambda gmp=gmp: gmp.Dispose())
            if time.time() <= st["swallow_until"]:
                st["swallow_until"] = 0.0                 # our own "ask the server": just close it
                return
            bring_up()

        def bring_up():
            if st["hidden"] or st["minimized"] or st["docked"] or not Kit.is_open(win["g"]):
                st["hidden"] = st["minimized"] = st["docked"] = False
                settings["minimized"] = False
                save_settings()
                _build_window()
            else:
                ctl = Kit.client_control(win["g"])
                if ctl is not None:
                    safe(lambda: Tz.call(None, "MakeTopMostGump", [ctl],
                                         Tz.T("ClassicUO.Game.Managers.UIManager")))

        # =========================================================================
        #  actions (clicks are queued; they run here, on the module's tick)
        # =========================================================================
        def armed(key, text):
            """True on the second click within ARM_SECS; the first only says so."""
            now = time.time()
            if now - st["arm"].get(key, 0.0) <= ARM_SECS:
                st["arm"].pop(key, None)
                return True
            st["arm"][key] = now
            API.SysMsg("%s: %s" % (TITLE, text), Kit.HUE_INFO)
            return False

        def shown_skills():
            return [d[1] for d in (st["desc"] or []) if d[0] == "s"]

        def bulk_lock(v, only_capped=False):
            n = 0
            for i in (range(SK["n"]) if only_capped else shown_skills()):
                base, _, cap, lock = SK["cur"][i]
                if only_capped and not (cap and base >= cap):
                    continue
                if lock != v:
                    set_lock(i, v)
                    n += 1
            API.SysMsg("%s: %d skill%s %s." % (TITLE, n, "" if n == 1 else "s",
                                               ("set to go up", "set to go down", "locked")[v]),
                       Kit.HUE_GOOD if n else Kit.HUE_INFO)

        def apply_lockset(k):
            if k >= len(locksets):
                return
            name, code = locksets[k]
            n = 0
            for i, ch in enumerate(code[:SK["n"]]):
                v = "udl".find(ch)
                if v >= 0 and SK["cur"][i][3] != v:
                    set_lock(i, v)
                    n += 1
            API.SysMsg("%s: lock set \"%s\" put on (%d change%s)." % (
                TITLE, name, n, "" if n == 1 else "s"), Kit.HUE_GOOD)

        def save_lockset(name):
            name = re.sub(r"[|=;]", "", name or "").strip()[:24]
            if not name:
                name = "Set %d" % (len(locksets) + 1)
            code = "".join("udl"[c[3]] for c in SK["cur"])
            for k, (n, _) in enumerate(locksets):
                if n.lower() == name.lower():
                    locksets[k] = (name, code)
                    break
            else:
                if len(locksets) >= MAX_LOCKSETS:
                    API.SysMsg("%s: at most %d lock sets: delete one first." % (
                        TITLE, MAX_LOCKSETS), Kit.HUE_BAD)
                    return
                locksets.append((name, code))
            save_locksets()
            API.SysMsg("%s: lock set \"%s\" saved." % (TITLE, name), Kit.HUE_GOOD)

        def move_to_next_group(i):
            read_groups(True)
            if i is None or not GR["list"]:
                API.SysMsg("%s: the client's skill groups can't be read." % TITLE, Kit.HUE_BAD)
                return
            gi = group_of(i)
            dst = 0 if gi is None else (gi + 1) % len(GR["list"])
            try:
                if gi is not None:
                    GR["list"][gi]["obj"].Remove(as_byte(i))
                GR["list"][dst]["obj"].Add(as_byte(i))
                groups_save()
                API.SysMsg("%s: %s moved to %s." % (TITLE, SK["names"][i],
                                                    GR["list"][group_of(i) or 0]["name"]),
                           Kit.HUE_GOOD)
            except Exception as ex:
                API.SysMsg("%s: couldn't move it (%s)." % (TITLE, Tz.why(ex)), Kit.HUE_BAD)

        def group_new():
            mgr = group_mgr()
            try:
                import System
                g = System.Activator.CreateInstance(Tz.T("ClassicUO.Game.Managers.SkillsGroup"))
                g.Name = "New group"
                g.IsMaximized = True
                mgr.Add(g)
                groups_save()
            except Exception as ex:
                API.SysMsg("%s: couldn't add a group (%s)." % (TITLE, Tz.why(ex)), Kit.HUE_BAD)

        def group_delete(gi):
            read_groups(True)
            if gi <= 0 or gi >= len(GR["list"]):
                return
            mgr = group_mgr()
            name = GR["list"][gi]["name"]
            if safe(lambda: mgr.Remove(GR["list"][gi]["obj"]), False):
                groups_save()
                API.SysMsg("%s: group \"%s\" deleted; its skills went to \"%s\"." % (
                    TITLE, name, GR["list"][0]["name"] if GR["list"] else "the first group"),
                    Kit.HUE_GOOD)

        def group_reset():
            mgr = group_mgr()
            try:
                mgr.MakeDefault()
                groups_save()
                API.SysMsg("%s: skill groups reset to the default ones." % TITLE, Kit.HUE_GOOD)
            except Exception as ex:
                API.SysMsg("%s: couldn't reset the groups (%s)." % (TITLE, Tz.why(ex)), Kit.HUE_BAD)

        def export_sheet():
            serial = int(safe(lambda: API.Player.Serial, 0) or 0)
            # (the character's name goes into the sheet's header: this export, a runtime
            # file the player asks for beside Virtue Assistant, is the only place one is
            # written; nothing of Virtue Assistant's own files carries a name)
            who = str(safe(lambda: API.Player.Name, "") or "")
            path = os.path.join(str(API.ScriptPath), "Skills_%08X.txt" % serial)
            now = time.time()
            lines = ["Skill sheet - %s - %s" % (who, time.strftime("%Y-%m-%d %H:%M",
                                                                     time.localtime(now))),
                     "Total %s / %s   (with bonuses %s)" % (
                         f1(total_real()), f1(settings["total_cap"]),
                         f1(sum(x[1] for x in SK["cur"]))),
                     "Str %d  Dex %d  Int %d   (stat cap %d)" % (
                         STATS["cur"][0], STATS["cur"][1], STATS["cur"][2], STATS["cap"]),
                     "Session %+.1f in %s" % (total_gain() / 10.0, dur(now - sess["start"])),
                     "",
                     "%-26s %7s %7s %7s %8s  %s" % ("Skill", "Real", "Value", "Cap", "Session",
                                                   "Lock")]
            for i in sorted(range(SK["n"]), key=lambda i: SK["names"][i].lower()):
                b, v, cp, lk = SK["cur"][i]
                gn = sgain(i)
                lines.append("%-26s %7s %7s %7s %8s  %s" % (
                    SK["names"][i], f1(b), f1(v), f1(cp), ("%+.1f" % (gn / 10.0)) if gn else "",
                    LOCK_WORD[lk]))
            # written by write_files() on the script's own thread (thread_tick): a
            # disk write on the client thread is a frame hitch
            st["to_write"].append((path, "\n".join(lines) + "\n"))

        def write_files():
            """thread_tick: write the skill sheets export_sheet() prepared (returns
            at once when there are none)."""
            while st["to_write"]:
                path, text = st["to_write"].pop(0)
                try:
                    with open(path, "w") as fh:
                        fh.write(text)
                    API.SysMsg("%s: skill sheet written to %s." % (TITLE, path), Kit.HUE_GOOD)
                except Exception as ex:
                    API.SysMsg("%s: couldn't write %s (%s)." % (TITLE, path, ex), Kit.HUE_BAD)

        def pick(i):
            if st["sel"] != i:
                st["sel"] = i
                show_target_text()
                if settings["sec_detail"]:
                    # its group is named in the details: the once-a-second read does
                    # (a click storm while sorting by gain did one reflection walk per click);
                    # only when the groups were never read is the read forced
                    read_groups(GR["sig"] is None)
            place_selbox()

        def picked(i):
            if i is None:
                API.SysMsg("%s: pick a skill first." % TITLE, Kit.HUE_INFO)
            return i is not None

        def run_action(a, now):
            kind = a[0] if isinstance(a, tuple) else a
            arg = a[1] if isinstance(a, tuple) and len(a) > 1 else None
            sel = st["sel"]
            if kind == "settings":
                HOST.show_settings(KEY)
            elif kind == "toggle_min":
                st["minimized"] = not (st["minimized"] or st["docked"])
                st["docked"] = False
                safe(lambda: HOST.dock_forget(KEY))      # its own minimized bar, not the Action Bar
                settings["minimized"] = st["minimized"]
                save_settings()
                st["rebuild"] = "window"
            elif kind == "to_bar":
                safe(lambda: HOST.dock_to_bar(KEY, TITLE))   # folds in now, or once the bar is up
            elif kind == "filter":
                settings["filter"] = (settings["filter"] + 1) % len(FILTERS)
                save_settings()
                lbl = win["c"].get("filter")
                if lbl is not None:
                    Kit.set_text(lbl, FILTERS[settings["filter"]][1])
            elif kind == "sort":
                if settings["sort"] == arg:
                    settings["asc"] = not settings["asc"]
                else:
                    settings["sort"] = arg
                    settings["asc"] = arg == "name"       # numbers: biggest first
                save_settings()
            elif kind == "pick":
                pick(arg)
            elif kind == "button":
                pick(arg)
                make_button(arg)
            elif kind == "mkbutton":
                if picked(sel):
                    make_button(sel)
            elif kind == "use":
                i = arg if arg is not None else sel
                if picked(i):
                    use_skill(i)
            elif kind == "lock":
                if arg is not None and arg < SK["n"]:
                    set_lock(arg, (SK["cur"][arg][3] + 1) % 3)
            elif kind == "dlock":
                if sel is not None:
                    set_lock(sel, arg)
            elif kind == "stat":
                stat_lock(arg)
            elif kind == "fold":
                if isinstance(arg, int):
                    g = GR["list"][arg] if arg < len(GR["list"]) else None
                    if g is not None:
                        safe(lambda: setattr(g["obj"], "IsMaximized", not g["max"]))
                        g["max"] = not g["max"]
                else:
                    st["pc"][arg] = not st["pc"].get(arg, False)
            elif kind == "pin":
                if picked(sel):
                    marks["pins"] ^= {sel}                # pin / unpin
                    save_marks()
            elif kind == "nextgrp":
                if picked(sel):
                    move_to_next_group(sel)
            elif kind == "all_up":
                bulk_lock(0)
            elif kind == "all_down":
                if armed("all_down", "click All down again to set every skill in the list to "
                                     "go down."):
                    bulk_lock(1)
            elif kind == "all_locked":
                bulk_lock(2)
            elif kind == "lock_capped":
                bulk_lock(2, only_capped=True)
            elif kind == "newsess":
                new_session()
                API.SysMsg("%s: new session; gains count from now." % TITLE, Kit.HUE_GOOD)
            elif kind == "export":
                export_sheet()
            elif kind == "ask":
                if ask_server():
                    API.SysMsg("%s: asked the server for your skills." % TITLE, Kit.HUE_INFO)
                else:
                    API.SysMsg("%s: couldn't ask the server." % TITLE, Kit.HUE_BAD)
            elif kind == "ls_save":
                save_lockset(arg)
                HOST.refresh_settings(KEY)
            elif kind == "ls_apply":
                apply_lockset(arg)
            elif kind == "ls_del":
                if arg < len(locksets):
                    n = locksets.pop(arg)[0]
                    save_locksets()
                    API.SysMsg("%s: lock set \"%s\" deleted." % (TITLE, n), Kit.HUE_INFO)
                HOST.refresh_settings(KEY)
            elif kind == "grp_new":
                group_new()
                HOST.refresh_settings(KEY)
            elif kind == "grp_del":
                group_delete(arg)
                HOST.refresh_settings(KEY)
            elif kind == "grp_reset":
                if armed("grp_reset", "click Reset groups again to put back the default "
                                      "skill groups."):
                    group_reset()
                    HOST.refresh_settings(KEY)
            elif kind == "grp_save":
                groups_save()

        # =========================================================================
        #  settings page (drawn inside the Virtue Assistant window)
        # =========================================================================
        MAIN_CHECKS = [
            ("replace", "Open this window instead of the client's skills window",
             "The paperdoll's Skills button, the Skills macro and the Action Bar bring this up"),
            ("x_hides", "Its Close only hides it (the Modules tab turns Skills off)",
             "Off: Close turns the Skills module off, as it does in other windows"),
            ("bars", "Progress bar per skill (value / cap)",
             "A bar in every row, filled to value / cap (green once the skill is at its cap)"),
            ("col_cap", "Cap column", "Show each skill's cap in its own column"),
            ("col_gain", "Session gain column", "Show what each skill gained this session"),
            ("journal", "A journal line for every gain or loss",
             "The client may print its own line too (its Options)"),
            ("lock_at_cap", "Lock a skill when it reaches its cap",
             "A skill set to go up is locked the moment it reaches its cap"),
            ("lock_at_target", "Lock a skill when it reaches its target",
             "Set a target in the window's details part"),
            ("cap_warn", "Warn at the total cap when no skill is set to go down",
             "A journal warning (and a red total) when nothing can rise any more"),
            ("tips", "Training tips in the details and in each row's tooltip",
             "A tip for the skill's range, from the TIPS table in the Skills file (classic-era "
             "advice; edit it for the shard)")]
        NUM_FIELDS = [("rows", "Rows in the list:", False,
                       "How many skills the list shows at once (or drag a corner of the window)"),
                      ("total_cap", "Total skill cap:", True,
                       "Your shard's total skill cap (In Mani Ylem: check it in game)"),
                      ("hl_secs", "Green name after a gain (s):", False,
                       "Seconds a skill's name stays green after it gained (0 = never)"),
                      ("rate_min", "Recent pace over (minutes):", False,
                       "Minutes the recent gain rate and the time to cap look back over")]
        SEC_CHECKS = [("sec_summary", "Totals and session", "Total skill points and the session line"),
                      ("sec_stats", "Str / Dex / Int", "Your stats, their lock arrows and the stat cap"),
                      ("sec_locks", "Lock buttons", "All up, All down, All locked and Lock capped"),
                      ("sec_detail", "Picked skill details", "Rates, target, pin and the Use button"),
                      ("sec_log", "Recent gains", "The last gains, newest first")]
        TOOLS_HINT = "Export writes a skill sheet to a text file next to Virtue Assistant."

        SIZE_HINT = ("Drag any corner of the Skills window to resize it: its height sets the "
                     "rows, its width spreads the columns.")
        STAT_HINT = ("A stat set to go up locks when it rises to its target; one set to go down, "
                     "when it falls to it. The window's Str / Dex / Int tooltips show the "
                     "session's gains per hour.")

        def page_heights(w):
            hs = [30 + len(MAIN_CHECKS) * 24 + len(NUM_FIELDS) * 28 +
                  len(Kit.wrap(SIZE_HINT, w - 24)) * 18 + 6,
                  30 + 3 * 24 + 28 + 6,
                  30 + 28 + 24 + len(Kit.wrap(STAT_HINT, w - 24)) * 18 + 6,
                  58 + max(1, len(locksets)) * 26 + 6]
            # (the groups are re-read once a second while the page is open - read_groups'
            # own cadence - not on every measurement of the page; only never-read ones now)
            read_groups(GR["sig"] is None)
            ng = len(GR["list"]) if GR["ok"] else 1
            hs.append(30 + max(1, ng) * 28 + 28 + 6)
            hs.append(58 + len(Kit.wrap(TOOLS_HINT, w - 24)) * 18 + 6)
            return hs

        def config_height(w):
            hs = page_heights(w)
            return sum(hs) + Kit.GAP * (len(hs) - 1)

        def build_config(g, x, y, w):
            hs = page_heights(w)
            store = ({}, {})
            c = {"store": store, "num": {}, "chk": {}, "grp": []}
            # ---- the window ----
            Kit.add_section(g, x, y, w, hs[0], "WINDOW")
            ry = y + 30
            for k, text, tip in MAIN_CHECKS:
                c["chk"][k] = Kit.add_check(g, text, x + 12, ry, settings[k], tip)
                ry += 24
            lx = x + 12 + max(Kit.text_w(t) for _, t, _, _ in NUM_FIELDS) + 10
            for k, text, dec, tip in NUM_FIELDS:
                Kit.add_label(g, text, x + 12, ry + 3)
                val = f1(settings[k]) if dec else str(settings[k])
                c["num"][k] = Kit.add_textbox(g, val, lx, ry, 70, numbers=not dec)
                safe(lambda k=k, tip=tip: c["num"][k].SetTooltip(tip))
                lo, hi = LIMITS[k]
                rng = ("(%s-%s)" % (f1(lo), f1(hi))) if dec else ("(%d-%d)" % (lo, hi))
                Kit.add_label(g, Kit.fit(rng, x + w - 4 - (lx + 84)), lx + 84, ry + 3, Kit.HUE_INFO)
                if k == "rows":
                    # the dragged width, beside Rows: read-only (a corner drag sets it)
                    wx = lx + 84 + Kit.text_w(rng) + 16
                    c["width_v"] = Kit.add_label(g, Kit.fit(width_text(), x + w - 4 - wx), wx,
                                                 ry + 3, Kit.HUE_INFO)
                    Kit.catcher(g, wx - 2, ry, x + w - 4 - wx, 22, lambda: None,
                                "The window's width, set by dragging a corner (natural: as wide "
                                "as its columns need)")
                ry += 28
            for line in Kit.wrap(SIZE_HINT, w - 24):
                Kit.add_label(g, line, x + 12, ry + 2, Kit.HUE_INFO)
                ry += 18
            y += hs[0] + Kit.GAP
            # ---- sections ----
            Kit.add_section(g, x, y, w, hs[1], "SECTIONS  (what the window shows)")
            half = (w - 24) // 2
            for n, (k, text, tip) in enumerate(SEC_CHECKS):
                c["chk"][k] = Kit.add_check(g, text, x + 12 + (n % 2) * half,
                                            y + 30 + (n // 2) * 24, settings[k], tip)
            ry = y + 30 + 3 * 24
            Kit.add_label(g, "Recent gains lines:", x + 12, ry + 3)
            c["num"]["log_lines"] = Kit.add_textbox(g, str(settings["log_lines"]),
                                                    x + 12 + Kit.text_w("Recent gains lines:") + 10,
                                                    ry, 50, numbers=True)
            safe(lambda: c["num"]["log_lines"].SetTooltip("Lines the Recent gains part shows (%d-%d)"
                                                          % LIMITS["log_lines"]))
            y += hs[1] + Kit.GAP
            # ---- stat targets (2.6.05) ----
            Kit.add_section(g, x, y, w, hs[2], "STAT TARGETS  (a stat locks when it gets there)")
            ry = y + 30
            sx = x + 12
            c["stat_tgt"] = []                            # [field, value applied, typed, since]
            for k, nm in enumerate(("Str", "Dex", "Int")):
                Kit.add_label(g, nm + ":", sx, ry + 3)
                tx = sx + Kit.text_w(nm + ":") + 8
                shown = str(stat_tgt[k]) if stat_tgt[k] else ""
                tb = Kit.add_textbox(g, shown, tx, ry, 44, numbers=True)
                safe(lambda tb=tb, k=k: tb.SetTooltip("%s target (1-%d, empty = none)" % (
                    STAT_NAMES[k], STAT_TARGET_MAX)))
                c["stat_tgt"].append([tb, shown, shown, 0.0])
                sx = tx + 44 + 24
            ry += 28
            c["chk"]["lock_stat_target"] = Kit.add_check(
                g, "Lock a stat when it reaches its target", x + 12, ry,
                settings["lock_stat_target"], "Off: only a journal line when it gets there")
            ry += 24
            for line in Kit.wrap(STAT_HINT, w - 24):
                Kit.add_label(g, line, x + 12, ry + 2, Kit.HUE_INFO)
                ry += 18
            y += hs[2] + Kit.GAP
            # ---- lock sets ----
            Kit.add_section(g, x, y, w, hs[3], "LOCK SETS  (saved up / down / locked layouts)")
            Kit.add_label(g, "Name:", x + 12, y + 33)
            nx = x + 12 + Kit.text_w("Name:") + 8
            sx = x + w - 12 - cap_w("Save current")
            c["ls_name"] = Kit.add_textbox(g, "", nx, y + 30, max(60, sx - nx - 14), numbers=False)
            safe(lambda: c["ls_name"].SetTooltip("Name for the lock set Save current makes "
                                                 "(empty = Set 1, Set 2 ...)"))
            Kit.art_button(g, store, "ls_save", Kit.ART_OK, sx, y + 29, "Save current",
                           "Save every skill's lock as a set (the same name replaces it)")
            ry = y + 58
            if not locksets:
                Kit.add_label(g, "No lock sets yet. Type a name and click Save current.",
                              x + 12, ry + 3, Kit.HUE_INFO)
            dx = x + w - 12 - cap_w("Delete")
            ax = dx - 12 - cap_w("Apply")
            for k, (name, code) in enumerate(locksets):
                ups, downs = code.count("u"), code.count("d")
                Kit.add_label(g, Kit.fit("%s  (%d up, %d down)" % (name, ups, downs), ax - x - 24),
                              x + 12, ry + 3)
                Kit.art_button(g, store, "ls_apply_%d" % k, Kit.ART_OK, ax, ry - 1, "Apply",
                               "Put this lock set on your skills")
                Kit.art_button(g, store, "ls_del_%d" % k, Kit.ART_CLOSE, dx, ry - 1, "Delete",
                               "Delete this lock set")
                ry += 26
            y += hs[3] + Kit.GAP
            # ---- groups ----
            Kit.add_section(g, x, y, w, hs[4], "GROUPS  (the client's skill groups)")
            ry = y + 30
            dx = x + w - 12 - cap_w("Delete")
            if not GR["ok"]:
                Kit.add_label(g, "The client's skill groups can't be read.", x + 12, ry + 3,
                              Kit.HUE_BAD)
                ry += 28
            for gi, gr in enumerate(GR["list"]):
                tb = Kit.add_textbox(g, gr["name"], x + 12, ry, 200, numbers=False)
                safe(lambda tb=tb: tb.SetTooltip("The group's name (type to rename it)"))
                Kit.add_label(g, "%d skill%s" % (len(gr["members"]), "" if len(gr["members"]) == 1
                                                 else "s"), x + 226, ry + 3, Kit.HUE_INFO)
                if gi > 0:
                    Kit.art_button(g, store, "grp_del_%d" % gi, Kit.ART_CLOSE, dx, ry - 1,
                                   "Delete", "Delete this group (its skills go to the first one)")
                else:
                    Kit.add_label(g, "first group", dx + 35, ry + 3, Kit.HUE_INFO)
                c["grp"].append((tb, gi, gr["name"]))
                ry += 28
            if GR["ok"] and not GR["list"]:
                ry += 28
            Kit.art_button(g, store, "grp_new", Kit.ART_OK, x + 12, ry - 1, "New group",
                           "Add an empty group (the window's Next group button moves skills in)")
            Kit.art_button(g, store, "grp_reset", Kit.ART_CLOSE, x + 12 + cap_w("New group") + 16,
                           ry - 1, "Reset groups", "Put back the client's default groups "
                                                   "(click twice)")
            y += hs[4] + Kit.GAP
            # ---- tools ----
            Kit.add_section(g, x, y, w, hs[5], "TOOLS")
            bx = x + 12
            for key, cap, tip in (("export", "Export sheet",
                                   "Write every skill's values to a text file next to Virtue Assistant"),
                                  ("ask", "Ask server", "Ask the server for fresh skill values"),
                                  ("newsess", "New session", "Start a new session: gains count from now")):
                Kit.art_button(g, store, key, Kit.ART_PLAY, bx, y + 29, cap, tip)
                bx += cap_w(cap) + 16
            for k, line in enumerate(Kit.wrap(TOOLS_HINT, w - 24)):
                Kit.add_label(g, line, x + 12, y + 58 + k * 18, Kit.HUE_INFO)
            page["c"] = c

        def width_text():
            """What the settings page says of the dragged width."""
            if settings["width"]:
                return "Width: %d px (drag a corner)" % settings["width"]
            return "Width: natural (drag a corner)"

        def read_num(ctrl, default, lo, hi, dec):
            try:                                          # 2.6.82: plain try (no lambda per read)
                txt = str(ctrl.Text or "").strip()
            except Exception:
                txt = ""
            try:
                v = int(round(float(txt.replace(",", ".")) * 10)) if dec else int(txt)
                return max(lo, min(hi, v))
            except ValueError:
                return default

        def poll_config():
            c = page["c"]
            if c is None:
                return
            if page["sync"]:                              # a corner drag changed the rows / width
                page["sync"] = False
                tb = c["num"].get("rows")
                if tb is not None:
                    try:
                        tb.SetText(str(settings["rows"]))
                    except Exception:
                        safe(lambda: setattr(tb, "Text", str(settings["rows"])))
                if c.get("width_v") is not None:
                    Kit.set_text(c["width_v"], width_text())
                return
            new = dict(settings)
            for k, ctrl in c["chk"].items():
                try:
                    new[k] = bool(ctrl.IsChecked)
                except Exception:
                    new[k] = bool(settings[k])
            for k, ctrl in c["num"].items():
                lo, hi = LIMITS[k]
                new[k] = read_num(ctrl, settings[k], lo, hi, k == "total_cap")
            if new != settings:
                relayout = any(new[k] != settings[k] for k in LAYOUT_KEYS)
                settings.update(new)
                save_settings()
                touch()
                if relayout:
                    st["m"] = None
                    st["rebuild"] = "window"
                st["warned_cap"] = False
                st["cap_at"] = 0.0                        # checked again on the next tick
            poll_stat_targets(c, False)
            for tb, gi, shown in list(c["grp"]):
                try:
                    txt = str(tb.Text or "")
                except Exception:
                    txt = str(shown or "")
                if txt != shown and gi < len(GR["list"]):
                    safe(lambda: setattr(GR["list"][gi]["obj"], "Name", txt))
                    GR["list"][gi]["name"] = txt
                    touch()
                    c["grp"] = [(t, g2, txt if g2 == gi else s) for t, g2, s in c["grp"]]
                    st["grp_dirty_at"] = time.time()      # 2.6.81: saved once the typing rests

            store = c["store"]
            for key in list(store[0].keys()):
                if not Kit.was_clicked(store, key):
                    continue
                if key == "ls_save":
                    name = str(safe(lambda: c["ls_name"].Text, "") or "")
                    st["queue"].append(("ls_save", name))
                elif key.startswith(("ls_apply_", "ls_del_", "grp_del_")):
                    kind, _, n = key.rpartition("_")
                    st["queue"].append((kind, int(n)))
                else:
                    st["queue"].append((key,))
                HOST.poke()

        STAT_SETTLE = 0.8                     # a target field unchanged this long is applied

        def poll_stat_targets(c, final):
            """The Str / Dex / Int target fields: applied once a field has stopped
            changing for STAT_SETTLE seconds (or the page closes), so the number
            typed half-way ("1" on the way to "100") never counts. final (the page
            is going): the text the last poll read is applied, the field is not
            read again - config_closed also runs after the settings window's
            measuring pass has disposed its copy of the page, and a disposed
            TazUO text box reads "" (that read wiped every target)."""
            now = time.time()
            for k, e in enumerate(c.get("stat_tgt") or ()):
                if final:
                    txt = e[2]
                else:
                    try:
                        txt = str(e[0].Text or "").strip()
                    except Exception:
                        continue
                    if txt != e[2]:
                        e[2], e[3] = txt, now
                        continue
                if txt == e[1] or (not final and now - e[3] < STAT_SETTLE):
                    continue
                e[1] = txt
                if txt and not txt.isdigit():
                    continue
                v = max(0, min(STAT_TARGET_MAX, int(txt))) if txt else 0
                if v != stat_tgt[k]:
                    stat_tgt[k] = v
                    save_stat_targets()
                    touch()
                    stat_at_target(k)

        def config_closed():
            if page["c"] is not None:
                poll_stat_targets(page["c"], True)        # a target still settling is kept
            page["c"] = None
            page["sync"] = False
            if st.get("grp_dirty_at"):                    # 2.6.81: a rename still resting
                st["grp_dirty_at"] = 0.0
                st["queue"].append(("grp_save",))

        # =========================================================================
        #  module hooks
        # =========================================================================
        def set_ready():
            """The skills have come in: the session counts from what they are."""
            st["ready"] = True
            for i in range(SK["n"]):
                sess["base"].setdefault(i, SK["cur"][i][0])
            if sess["stats"] is None and any(STATS["cur"]):
                sess["stats"] = list(STATS["cur"])

        def run_queue(now):
            while st["queue"]:
                run_action(st["queue"].pop(0), now)

        def tick_body():
            now = time.time()
            if win["g"] is not None and Kit.was_clicked(win["store"], "close"):
                if settings["x_hides"]:
                    st["hidden"] = True
                    save_pos()
                    g, win["g"] = win["g"], None          # hidden, not off
                    win.update({"c": {}, "rows": [], "rowmap": {}})
                    UIC.clear()                           # (keyed by control: no disposed keys kept)
                    Kit.dispose(g)
                    API.SysMsg("%s: hidden; %s brings it back." % (
                        TITLE, "the client's Skills button or the Action Bar's Skills button"
                        if settings["replace"] else
                        "the Action Bar's Skills button (or Skills off and on in the Modules tab)"),
                        Kit.HUE_INFO)
                else:
                    Kit.dispose(win["g"])                 # on_disposed turns the module off
                    return
            if st["resize_at"] and now - st["resize_at"] >= RESIZE_SETTLE \
                    and not safe(lambda: SNAP.pressed(), False):
                st["resize_at"] = 0.0                     # a corner drag was let go
                apply_resize()
            # 2.6.81: a renamed skill group is saved once its name has rested
            # GRP_SETTLE s (not on every key: the client writes its groups file)
            if st["grp_dirty_at"] and now - st["grp_dirty_at"] >= GRP_SETTLE:
                st["grp_dirty_at"] = 0.0
                groups_save()
            # the client's skills
            had = SK["n"]
            if not refresh_refs():
                run_queue(now)
                vanilla_check()
                if st["rebuild"] == "window":
                    _build_window()
                elif win["g"] is not None and win["c"] and st["desc"] is None:
                    rebuild_rows(now)
                return
            if SK["n"] != had:
                st["rebuild"] = "window"
            # 2.6.82: while the list isn't on screen (hidden by its X, minimized,
            # folded) the skills are read every HIDDEN_READ s, not every tick;
            # the stats once a second (every tick while a stat lock click waits)
            changed, stats_moved = {}, False
            if (st["ready"] and (win["g"] is None or not win["c"] or st["minimized"]
                                 or st["docked"])) and now < st["read_at"]:
                pass
            else:
                st["read_at"] = now + HIDDEN_READ
                changed = read_skills(not st["ready"])
                if st["stat_pending"] or now >= st["stats_at"] or not st["ready"]:
                    st["stats_at"] = now + STATS_EVERY
                    stats_moved = read_stats()
            if changed:
                list_moved()
            elif stats_moved:
                st["dirty"] = True                        # (a stat never changes the list)
            if not st["ready"]:
                if skills_loaded():
                    set_ready()
                    save_session()
                    st["rebuild"] = st["rebuild"] or "rows"
                elif now - st["started"] > 3.0 and not st["asked"]:
                    ask_server()                          # nothing yet: ask once
            elif changed:
                note_gains(changed, now)
            if stats_moved and st["ready"] and (stat_tgt[0] or stat_tgt[1] or stat_tgt[2]):
                note_stats()                              # a stat at its target (2.6.05)
            if st["ready"] and sess["stats"] is None and any(STATS["cur"]):
                sess["stats"] = list(STATS["cur"])
            read_groups()
            ran = bool(st["queue"])
            if ran:
                touch()
            run_queue(now)                                # clicks
            # the total-cap warning: when the skills or locks may have moved (a
            # change, a click, the settings page) and every CAP_EVERY s besides
            if changed or ran or now >= st["cap_at"]:
                st["cap_at"] = now + CAP_EVERY
                warned = st["warned_cap"]
                cap_warning()
                if warned != st["warned_cap"]:
                    touch()
            vanilla_check()
            if st["rebuild"] == "window":
                _build_window()
                st["dirty"], st["redraw_at"] = False, now + REDRAW_EVERY
                return
            if win["g"] is None or not win["c"]:
                return
            if not (st["minimized"] or st["docked"]) and poll_fields(now):
                touch()
            # the list and its texts are redone when something changed (a skill, a
            # stat, a click, a field) and once a second for what only time moves
            # (session clock, rates, green names, "gaining now")
            if not st["dirty"] and now < st["redraw_at"]:
                return
            st["dirty"], st["redraw_at"] = False, now + REDRAW_EVERY
            if st["minimized"] or st["docked"]:
                refresh(now)
                return
            rebuild_rows(now)
            refresh(now)

        def _tick():
            # client_tick: this already runs on the client thread, where
            # Kit.on_client(tick_body) only ran it in place after a few checks
            tick_body()

        def _start():
            st.update({"shutting": False, "docked": False, "hidden": False, "queue": [],
                       "rebuild": None, "desc": None, "m": None, "ready": False,
                       "asked": 0.0, "swallow_until": 0.0, "warned_cap": False, "hl": {},
                       "log": [], "gains": {}, "started": time.time(), "ref_at": 0.0,
                       "grp_at": 0.0, "tgt_shown": None, "stat_pending": {}, "dirty": True,
                       "redraw_at": 0.0, "desc_key": None, "cap_at": 0.0, "resize_at": 0.0,
                       "grp_dirty_at": 0.0,       # 2.6.81: when a group was last renamed (0: none)
                       "read_at": 0.0, "stats_at": 0.0})   # 2.6.82: next skill / stat read
            VG.update({"gumps": None, "sig": None, "full_at": 0.0})
            load_settings()
            load_marks()
            load_locksets()
            load_stat_targets()
            load_session()
            st["minimized"] = settings["minimized"] or bool(safe(lambda: HOST.dock_wanted(KEY), False))
            refresh_refs(True)
            read_skills()
            read_stats()
            read_groups(True)
            if skills_loaded():
                set_ready()
            fitst.update({"width": None, "rows": None, "slot": None, "k": 1.0, "full": None})
            _build_window()
            show_target_text()
            hooks = Kit.dock_hooks(TITLE, DOCK_ICON, st, win, redraw)
            hooks["on"] = bring_up               # hidden by its X: the Action Bar's button shows it again
            hooks["fit"] = layout_fit            # the layout fits it to its zone (2.6.55)
            hooks.update({"exact": True, "verify": True, "drawn_at": drawn_at})  # (2.6.78) its slot exactly
            safe(lambda: HOST.dock_add(KEY, hooks))
            if settings["replace"]:
                vanilla_check()

        def _stop():
            st["shutting"] = True
            if st.get("grp_dirty_at"):     # 2.6.81: a group rename still resting is saved
                st["grp_dirty_at"] = 0.0     # (on the client thread: mgr is a live client object)
                safe(lambda: Kit.on_client(groups_save))
            write_files()                  # a sheet still waiting: no thread_tick comes after stop
            save_pos()
            save_settings()
            if st["ready"]:
                save_session()
            safe(lambda: HOST.dock_remove(KEY))
            g, win["g"] = win["g"], None
            win.update({"c": {}, "rows": [], "rowmap": {}})
            UIC.clear()
            Kit.dispose(g)

        load_settings()
        load_stat_targets()
        # The tick runs on the client thread, batched with the other modules (it
        # never waits); a skill sheet export is written from thread_tick on the
        # script's own thread.
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True, "thread_tick": write_files,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE

    def _part_alarm():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the Virtue Assistant script from
        #  this file uses (API, G, safe, Client, Kit, Follow, HOST, Journal, the main
        #  its Modules tab.
        # ============================ MODULE START ===================================
        #  MODULE: Training Alarm (was Attention)  -  an alarm when something needs
        #  you at the keyboard
        #
        #  For attended skill training: staff may check that you are at the
        #  keyboard. When something needs you, the Training Alarm raises a loud alarm (the
        #  shared alert banner, flashing until it is clicked, its sound and a
        #  journal line), repeats the sound until you answer, and pauses every
        #  skill loop that asks it (Skill Bags, through the generic
        #  HOST.services["attention.up"], True while an alarm waits for you and,
        #  if you set it, a while after you answer).
        #
        #  What raises the alarm (each can be turned off on the settings page):
        #    - a server gump opens that nobody asked for: not within ASKED_SECS of
        #      your own mouse (a click or a move: you are there, and the gump is
        #      most likely yours), your own typing (the chat line or a text field
        #      changing; a spoken command you typed counts too, but a skill loop's
        #      spell words or its "You have hidden yourself well." don't) or a gump
        #      of yours that just closed (a button reply), not a page of a window you had open in the
        #      last SAME_GUMP_SECS, not one opened hidden (a module reading it), and
        #      not an id on the ignore list. Skill loops double-click and target all
        #      the time, so those don't count as "asked" (only when the client's
        #      mouse can't be read: then a double-click or an answered cursor does);
        #    - a mobile whose name or title holds one of the staff words (GM,
        #      Counselor, Seer, ...) comes into view;
        #    - someone else says your character's name (and, as an option, any word
        #      of it with 4 letters or more), or whispers to you;
        #    - (off by default) you take damage while not in war mode.
        #  Your character's name is read from the game while it runs; nothing about
        #  you is written in this file.
        #
        #  Answer it with a click on the alert banner, on "I'm here" in this
        #  module's window, or on the window's alarm line. Alt+click the alarm line
        #  to auto-follow the mobile that raised it (staff, or who spoke).
        #
        #  It never acts in the game: it reads, sounds and pauses. No target
        #  cursors, no speech, no moves.
        # =============================================================================
        KEY = "attention"
        TITLE = "Training Alarm"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "Attention_settings"   # per character: the triggers and the alarm options
        POS_KEY = "Attention_pos"             # where the window sits
        MIN_KEY = "Attention_min"             # minimized when last seen
        W = 400                               # full window (its height follows the rows below)
        MINI_W, MINI_H = 300, 46              # minimized bar
        TRAY_ICON = 0x1C12                    # a bell, on the Action Bar's tray button
        GUMP_EVERY = 0.25                     # seconds between looks at the server gumps
        STAFF_EVERY = 1.0                     # seconds between looks at the mobiles in view
        STAFF_RANGE = 18                      # tiles: mobiles this close are looked at
        STAFF_RECHECK = 2.0                   # seconds: a mobile's title is read again once, this
        #                                       long after it was first seen (titles come later)
        STAFF_GONE = 60.0                     # seconds out of view before the same staff mobile
        #                                       raises the alarm again
        HIT_EVERY = 0.25                      # seconds between looks at your hit points
        ASKED_SECS = 1.5                      # a gump this soon after your mouse, your typing, your
        #                                       typed speech or a closed gump was asked for
        #                                       (UNCHECKED IN GAME: lag may need more)
        TYPED_SECS = 5.0                      # a line of yours this soon after you typed is speech
        #                                       you typed (else a skill loop's words or messages:
        #                                       they come under your name too, and never count)
        SAME_GUMP_SECS = 60.0                 # a gump with the id of one you had open this
        #                                       recently is a page of a window you were using
        DEFAULT_MARKERS = "GM, Counselor, Seer, Admin, Administrator, Developer, Staff, Game Master"
        #                                       staff words (UNCHECKED IN GAME: how In Mani Ylem
        #                                       names or titles its staff); edited on the settings page
        DEFAULT_IGNORE = ""                   # gump ids never alarmed (hex or decimal, commas)
        WHISPER_TYPES = ("whisper", "8")      # the client's MessageType of a whispered line
        #                                       (UNCHECKED IN GAME: the shard sends whispers as such)
        QUIET_TYPES = ("regular", "0", "system", "1", "label", "6")   # not printed by the debug
        REPEAT_DEFAULT, REPEAT_MAX = 5, 120   # seconds between alarm sounds until answered (0 = once)
        HOLD_DEFAULT, HOLD_MAX = 0, 600       # seconds skill loops stay paused after you answer
        REASONS_MAX = 8                       # reasons kept for one alarm (the oldest dropped)
        QUOTE_MAX = 60                        # characters of a spoken line quoted in the alarm
        FLASH_SECS = 0.5                      # the alarm line's flash
        CACHE_CAP = 500                       # mobiles remembered (cleared past this)
        OPEN_IDS_CAP = 60                     # gump ids remembered as "in use"
        QUEUE_CAP = 30                        # whispered lines waiting for the tick
        NAME_EVERY = 5.0                      # seconds between reads of your character's name
        # the kinds of alarm: (trigger, alert key on Settings > Alerts, label, default sound)
        #  (the sounds are ALERT_SOUNDS ids: Boom 0x307, Yell 0x338, Harm 0x1F1)
        KINDS = (("gump", "attention.gump", "Gump nobody asked for", 0x307),
                 ("staff", "attention.staff", "Staff in view", 0x307),
                 ("name", "attention.name", "Someone says your name", 0x338),
                 ("whisper", "attention.whisper", "A whisper to you", 0x338),
                 ("hit", "attention.hit", "Hit while not fighting", 0x1F1),
                 ("test", "attention.test", "Training Alarm test", 0x307))
        ALERT_KEY = dict((k, a) for k, a, _, _ in KINDS)
        SOUND_OF = dict((k, s) for k, _, _, s in KINDS)
        TRIGGERS = ("gump", "staff", "name", "words", "whisper", "hit")
        # -----------------------------------------------------------------------------

        settings = {"gump": True, "staff": True, "name": True, "words": True, "whisper": True,
                    "hit": False, "markers": DEFAULT_MARKERS, "ignore": DEFAULT_IGNORE,
                    "repeat": REPEAT_DEFAULT, "hold": HOLD_DEFAULT, "say": False,
                    "anyalarm": True}     # 2.6.5: any module's alarm banner pauses skill loops too
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [], "active": False,
              "alarm": [],            # the reasons of the alarm waiting for you (empty: none)
              "resume_at": 0.0,       # after you answer: skill loops go on at this time
              "next_gump": 0.0, "gump_obj": None, "gump_gid": 0, "gump_vis": False, "primed": False,
              "open_ids": {}, "input": None,
              "asked_at": 0.0, "used_at": 0.0, "cursor_up": False, "last_gid": 0,
              "typing": None, "typed_at": 0.0,
              "next_staff": 0.0, "checked": {}, "staff_seen": {},
              "me": 0, "my_name": "", "name_at": 0.0, "name_re": None, "words_re": None,
              "next_hit": 0.0, "hp": None,
              "rd": None, "heard": [],
              "next_sound": 0.0, "banner_seen": False, "flash_at": 0.0, "flash_on": False,
              "drawn": None, "seq": 0, "checked_pat": None}
        win = {"g": None, "c": {}, "store": ({}, {})}
        page = {"c": None, "store": ({}, {})}
        hooks = {"done": False}       # the client events are subscribed once per script run
        mouse = {"looked": False, "get": None}     # the client's mouse, by reflection (once)
        rx = {"markers": None, "text": None, "ignore": frozenset(), "ignore_text": None}


        # ---------- saved settings ----------
        def _clean(text):
            return str(text or "").replace(";", ",").replace("=", " ").strip()


        def load_settings():
            raw = Kit.get_var(SETTINGS_KEY)
            for part in raw.split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k, v = k.strip(), v.strip()
                if k in TRIGGERS or k in ("say", "anyalarm"):
                    settings[k] = v == "1"
                elif k in ("repeat", "hold"):
                    try:
                        n = int(v)
                    except ValueError:
                        continue
                    hi = REPEAT_MAX if k == "repeat" else HOLD_MAX
                    settings[k] = max(0, min(hi, n))
                elif k in ("markers", "ignore"):
                    settings[k] = v


        def save_settings():
            parts = ["%s=%d" % (k, 1 if settings[k] else 0) for k in TRIGGERS + ("say", "anyalarm")]
            parts.append("repeat=%d" % settings["repeat"])
            parts.append("hold=%d" % settings["hold"])
            parts.append("markers=%s" % _clean(settings["markers"]))
            parts.append("ignore=%s" % _clean(settings["ignore"]))
            Kit.put_var(SETTINGS_KEY, ";".join(parts))


        def marker_re():
            """The staff words as one pattern (whole words, any case), made again
            only when the words change."""
            text = settings["markers"]
            if rx["text"] != text:
                words = [w.strip() for w in str(text or "").split(",") if w.strip()]
                words.sort(key=len, reverse=True)          # "Game Master" before "Game"
                rx["markers"] = re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"
                                           % "|".join(re.escape(w) for w in words),
                                           re.IGNORECASE) if words else None
                rx["text"] = text
            return rx["markers"]


        def ignored_ids():
            """The ignore list's gump ids (hex 0x.. or decimal), parsed again only
            when the list changes."""
            text = settings["ignore"]
            if rx["ignore_text"] != text:
                ids = set()
                for w in str(text or "").replace(" ", ",").split(","):
                    w = w.strip().lower()
                    if not w:
                        continue
                    try:
                        ids.add(int(w, 16) if w.startswith("0x") else int(w))
                    except ValueError:
                        continue
                rx["ignore"] = frozenset(ids)
                rx["ignore_text"] = text
            return rx["ignore"]


        def say(text):
            if settings["say"]:
                API.SysMsg("%s: %s" % (TITLE, text), Kit.HUE_INFO)


        # ---------- the shared alert banner (Settings > Alerts) ----------
        def alerts():
            """The mother's alert service object, or None (an older Virtue Assistant)."""
            try:
                return ALERTS
            except NameError:
                return None


        def sound_of(kind):
            """The alarm's sound as the player has it on Settings > Alerts (0 when
            that kind is silent or every alert sound is muted), else ours."""
            al = alerts()
            if al is None:
                return SOUND_OF.get(kind, 0)
            try:
                if al.mute:
                    return 0
                on, sid = al.setting(ALERT_KEY[kind])
                return int(sid) if on else 0
            except Exception:
                return SOUND_OF.get(kind, 0)


        def banner_up():
            """True while the shared banner shows an alarm (it flashes until clicked)."""
            al = alerts()
            if al is None:
                return False
            try:
                return bool(al.shown and al.alarm)
            except Exception:
                return False


        # ---------- the alarm ----------
        def is_up():
            """HOST.services["attention.up"]: True while an alarm waits for you, and
            for the seconds set after you answer it. Cheap: no client calls."""
            if st["alarm"]:
                return True
            ra = st["resume_at"]
            if ra:
                left = ra - time.time()
                if 0 < left <= HOLD_MAX + 1:            # (further: the clock was set back)
                    return True
            if settings["anyalarm"]:                    # 2.6.5: any module's alarm banner
                try:
                    return bool(HOST.alarm_up())
                except Exception:
                    return False
            return False


        def raise_alarm(kind, text, who=None, serial=0, gid=0, said=None):
            """A reason for the alarm (client thread). The same speaker and words
            twice (a whisper that also names you: the journal and the client's
            event both see it) count once."""
            fresh = not st["alarm"]
            again = False                                  # this speaker is already on the alarm
            for r in st["alarm"]:
                if r["who"] == who:
                    if r["text"] == text or (said is not None and r["said"] == said):
                        return False
                    again = True
            now = time.time()
            if fresh:
                st["seq"] += 1                             # a new alarm: never held back by the
                #                                            banner's 10 s rate limit (see below)
            st["alarm"].append({"kind": kind, "text": text, "who": who, "serial": int(serial or 0),
                                "gid": int(gid or 0), "at": now, "said": said})
            if len(st["alarm"]) > REASONS_MAX:
                del st["alarm"][:-REASONS_MAX]
            st["resume_at"] = 0.0
            if fresh:
                st["banner_seen"] = False
                rep = settings["repeat"]
                st["next_sound"] = now + rep if rep > 0 else 0.0
            if again:
                draw()                                     # (the banner already flashes for them)
                return True
            if hasattr(HOST, "alert"):
                # who: the reason, numbered per alarm: the same speaker or gump in a new
                # alarm (after you answered) is a new banner, not one the rate limit drops
                HOST.alert(ALERT_KEY[kind], text, "alarm", who="%s#%d" % (who or text, st["seq"]))
            else:                                          # an older Virtue Assistant: our own
                API.SysMsg("%s: %s." % (TITLE, text), Kit.HUE_BAD)
                sid = SOUND_OF.get(kind, 0)
                if sid:
                    API.PlaySound(sid)
            draw()
            return True


        def answer(how):
            """You answered: skill loops go on (after the hold, if one is set)."""
            if not st["alarm"]:
                return
            last = st["alarm"][-1]
            st["alarm"] = []
            hold = settings["hold"]
            st["resume_at"] = time.time() + hold if hold > 0 else 0.0
            if how != "banner" and banner_up():
                al = alerts()
                try:                                       # the banner shows ours: take it down too
                    # (the banner's line is "<module title>: <text>": matched by the text)
                    if last["text"] and str(al.line).endswith(last["text"]):
                        al.dismiss()
                except Exception:
                    pass
            API.SysMsg("%s: answered; %s" % (TITLE, ("skill loops go on in %d s." % hold) if hold
                                             else "skill loops go on."), Kit.HUE_GOOD)
            st["last_answered"] = last
            draw()


        def alarm_tick(now):
            if not st["alarm"]:
                return
            if banner_up():
                st["banner_seen"] = True
            elif st["banner_seen"]:
                answer("banner")                           # the banner was clicked away
                return
            rep = settings["repeat"]
            if rep > 0 and not st["next_sound"]:
                st["next_sound"] = now + rep               # (the repeat was set during the alarm)
            if rep > 0 and not 0 < st["next_sound"] - now <= rep:
                st["next_sound"] = now + rep
                sid = sound_of(st["alarm"][-1]["kind"])
                if sid:
                    API.PlaySound(sid)
            if not 0 < st["flash_at"] - now <= FLASH_SECS:
                st["flash_at"] = now + FLASH_SECS
                st["flash_on"] = not st["flash_on"]
                draw()


        # ---------- who you are ----------
        def read_me(now, p):
            if st["my_name"] and 0 <= now - st["name_at"] < NAME_EVERY:
                return
            st["name_at"] = now
            try:
                name = str(p.Name or "").strip()
                st["me"] = int(p.Serial)
            except Exception:
                return
            if name and name != st["my_name"]:
                st["my_name"] = name
                st["name_re"] = re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(name),
                                           re.IGNORECASE)
                parts = [w for w in re.split(r"[^A-Za-z0-9']+", name) if w]
                words = [w for w in parts if len(w) >= 4]
                if len(parts) > 1 and words:
                    st["words_re"] = re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"
                                                % "|".join(re.escape(w) for w in words),
                                                re.IGNORECASE)
                else:
                    st["words_re"] = None                  # one word: the whole name already


        # ---------- server gumps ----------
        def real_gump(g):
            """The client's Gump (a build may hand back a wrapper with a .Gump)."""
            if g is None:
                return None
            try:
                inner = g.Gump
            except Exception:
                return g
            return inner if inner is not None else g


        def gone(g):
            try:
                return bool(g.IsDisposed)
            except Exception:
                return True


        def mouse_readers():
            """Getters of the client's mouse (its place and its last left / right
            click times), found once by reflection; None when they can't be read."""
            if not mouse["looked"]:
                mouse["looked"] = True
                got = []
                t = safe(lambda: Client._type("ClassicUO.Input.Mouse"))
                if t is not None:
                    for name in ("Position", "LastLeftButtonClickTime", "LastRightButtonClickTime"):
                        m = safe(lambda: Client._member(t, name))
                        if m is not None:                  # 2.6.82: (getter, a point?)
                            got.append((m[0], name == "Position"))
                mouse["get"] = got or None
            return mouse["get"]


        def input_tick(now):
            """Has the mouse moved or clicked since the last look? (Then you are at
            the keyboard and a gump now is most likely yours.) None: the mouse
            can't be read on this build."""
            gs = mouse_readers()
            if not gs:
                return None
            cur = []
            for fn, point in gs:                           # 2.6.82: no raised try for the click times
                try:
                    v = fn()
                    if point:
                        try:
                            v = (int(v.X), int(v.Y))
                        except Exception:
                            v = int(v)
                    else:
                        v = int(v)
                except Exception:
                    v = None
                cur.append(v)
            cur = tuple(cur)
            prev, st["input"] = st["input"], cur
            if prev is not None and cur != prev:
                st["asked_at"] = now
            return True


        def typing_tick(now):
            """Did the keyboard go into or out of a text field (the chat line, a
            field) since the last look? That is you typing: you are there. Only the
            change counts: a field that simply keeps the focus while you are away
            must not make every gump 'asked for'."""
            try:
                t = bool(HOST.typing())
            except Exception:
                return
            prev, st["typing"] = st["typing"], t
            if prev is not None and t != prev:
                st["typed_at"] = st["asked_at"] = now


        def gump_tick(now):
            """One look at the server gump the client opened last (on the client
            thread these calls cost nothing)."""
            typing_tick(now)
            if input_tick(now) is None:                    # no mouse to read: the looser signs
                try:
                    up = bool(API.HasTarget("any"))
                except Exception:
                    up = False
                if st["cursor_up"] and not up:
                    st["asked_at"] = now                   # a cursor answered (you or a module)
                st["cursor_up"] = up
                if 0 <= now - st["used_at"] <= ASKED_SECS:     # a double-click (the client's event)
                    st["asked_at"] = max(st["asked_at"], st["used_at"])
            try:
                gid = int(API.HasGump() or 0)
            except Exception:
                gid = 0
            prev = st["gump_obj"]
            if gid and prev is not None and gid == st["gump_gid"] and not gone(prev):
                st["open_ids"][gid] = now                  # 2.6.82: the same window still up: no GetGump
                return
            g = None
            if gid:
                try:
                    g = real_gump(API.GetGump(gid))
                except Exception:
                    g = None
            if g is prev or (g is not None and prev is not None and gid == st["gump_gid"]
                             and not gone(prev)):
                st["gump_obj"] = g
                if gid:
                    st["open_ids"][gid] = now              # still open: a window in use
                return
            if prev is not None and st["gump_vis"] and gone(prev):
                st["asked_at"] = now                       # yours closed: the next follows from it
            st["gump_obj"], st["gump_gid"] = g, gid
            if g is None:
                st["gump_vis"] = False
                return
            visible = bool(safe(lambda: g.IsVisible, True))
            st["gump_vis"] = visible
            st["last_gid"] = gid
            opened = st["open_ids"]
            seen_at = opened.get(gid)
            opened[gid] = now
            if len(opened) > OPEN_IDS_CAP:
                for k in sorted(opened, key=opened.get)[:len(opened) - OPEN_IDS_CAP]:
                    del opened[k]
            if not st["primed"]:
                return                                     # open before we started: not news
            why = None
            if not visible:
                why = "opened hidden (a module reading it)"
            elif gid in ignored_ids():
                why = "on the ignore list"
            elif seen_at is not None and 0 <= now - seen_at <= SAME_GUMP_SECS:
                why = "a page of a window you had open"
            elif 0 <= now - st["asked_at"] <= ASKED_SECS:
                why = "asked for %.1f s before" % (now - st["asked_at"])
            if why is not None:
                say("gump 0x%X: %s." % (gid, why))
                return
            say("gump 0x%X: nobody asked for it." % gid)
            if settings["gump"]:
                raise_alarm("gump", "A gump opened by itself (id 0x%X)" % gid, "gump 0x%X" % gid,
                            gid=gid)


        # ---------- staff in view ----------
        def staff_tick(now):
            pat = marker_re()
            if pat is None:
                return
            try:
                mobs = HOST.mobiles(STAFF_RANGE)            # 2.6.82: the pass's one shared scan
            except Exception:
                return
            checked, seen, me = st["checked"], st["staff_seen"], st["me"]
            if len(checked) > CACHE_CAP or pat is not st["checked_pat"]:
                checked.clear()                            # (new staff words: look again)
                st["checked_pat"] = pat
            for m in mobs:
                try:
                    s = int(m.Serial)
                except Exception:
                    continue
                if s == me:
                    continue
                hit = checked.get(s)
                if hit is None or (not hit[0] and hit[2] < 2 and now - hit[1] >= STAFF_RECHECK):
                    try:
                        name = str(m.Name or "")
                        text = name
                        try:
                            props = m.raw.NameAndProps(False)
                            if props:
                                text = name + "\n" + str(props).split("\n")[0]
                        except Exception:
                            pass
                    except Exception:
                        continue
                    hit = (bool(pat.search(text)), now, (hit[2] if hit else 0) + 1, name)
                    checked[s] = hit
                if not hit[0]:
                    continue
                last = seen.get(s)
                seen[s] = now
                if last is None or not 0 <= now - last <= STAFF_GONE:
                    say("staff in view: %s." % hit[3])
                    raise_alarm("staff", "Staff in view: %s" % (hit[3] or "someone"), "staff %X" % s,
                                serial=s)
            if len(seen) > 50:
                for k in [k for k, t in seen.items() if not 0 <= now - t <= STAFF_GONE]:
                    del seen[k]


        # ---------- speech ----------
        def speaker_serial(name):
            """The serial of the mobile in view called `name` (0 when none)."""
            low = name.lower()
            try:
                for m in HOST.mobiles(STAFF_RANGE):         # 2.6.82: the pass's shared scan
                    if str(m.Name or "").lower() == low:
                        return int(m.Serial)
            except Exception:
                pass
            return 0


        def quote(text):
            text = " ".join(str(text).split())
            return text if len(text) <= QUOTE_MAX else text[:QUOTE_MAX - 2] + ".."


        def speech_tick(now):
            rd = st["rd"]
            if rd is None:
                return
            lines = rd.new()
            if not lines:
                return
            my_low = st["my_name"].lower()
            nre = st["name_re"]
            wre = st["words_re"] if settings["words"] else None
            for ln in lines:
                name = (ln.name or "").strip()
                text = ln.text
                if not name and ": " in text:              # "Name: text" in one string
                    name, text = [x.strip() for x in text.split(": ", 1)]
                if not name or name.lower() == "system":
                    continue
                low = name.lower()
                if my_low and low == my_low:
                    # your own line: a spoken command you typed makes the next gump
                    # yours; a skill loop's spell words and its messages ("You have
                    # hidden yourself well.") come under your name too, and don't
                    if 0 <= now - st["typed_at"] <= TYPED_SECS:
                        st["asked_at"] = now
                    continue
                if not settings["name"] or nre is None:
                    continue
                if nre.search(text) or (wre is not None and wre.search(text)):
                    say("%s said your name." % name)
                    raise_alarm("name", '%s said your name: "%s"' % (name, quote(text)), name,
                                serial=speaker_serial(name), said=text)


        def heard_tick():
            """Lines the client's journal event handed over (whispers, by their
            message type; the debug prints any other unusual type)."""
            q = st["heard"]
            if not q:
                return
            st["heard"] = []
            my_low = st["my_name"].lower()
            for text, name, mt in q:
                if not name or name.lower() == "system" or (my_low and name.lower() == my_low):
                    continue
                if mt not in QUIET_TYPES:
                    say("a %s line from %s." % (mt, name))
                if mt in WHISPER_TYPES and settings["whisper"]:
                    raise_alarm("whisper", '%s whispers to you: "%s"' % (name, quote(text)), name,
                                serial=speaker_serial(name), said=text)


        # ---------- the client's events (subscribed once; ignored while off) ----------
        def on_used(*args):
            if st["active"]:
                st["used_at"] = time.time()


        MT_LOW = {}                                        # 2.6.82: MessageType -> its lower-case name

        def on_entry(*args):
            if not st["active"]:
                return
            for a in args:
                # 2.6.82: the type first (its name cached per value); the text and
                # the name are read only for a line that is wanted
                try:
                    mt = a.MessageType
                    m = MT_LOW.get(mt)
                    if m is None:
                        m = str(mt).lower()
                        if len(MT_LOW) < 64:
                            MT_LOW[mt] = m
                except Exception:
                    continue
                if m in WHISPER_TYPES or (settings["say"] and m not in QUIET_TYPES):
                    try:
                        text = str(a.Text or "")
                        name = str(a.Name or "")
                    except Exception:
                        continue
                    q = st["heard"]                        # whispers (and, for the debug, the rest)
                    if len(q) < QUEUE_CAP:
                        q.append((text, name, m))
                return


        def hook_events():
            if hooks["done"]:
                return
            hooks["done"] = True
            ev = safe(lambda: API.Events)
            if ev is None:
                return
            safe(lambda: ev.ObjectUsed(on_used))
            safe(lambda: ev.JournalEntryAdded(on_entry))


        # ---------- hit points ----------
        def hit_tick(p):
            if not settings["hit"]:                        # 2.6.82: off: nothing read (the first
                st["hp"] = None                            # reading once on is the baseline)
                return
            try:
                hp = int(p.Hits)
                dead = bool(p.IsDead)
                war = bool(p.InWarMode)
            except Exception:
                return
            prev = st["hp"]
            st["hp"] = hp
            if prev is None or dead or war or hp >= prev:
                return
            if settings["hit"]:
                raise_alarm("hit", "You took %d damage while not fighting" % (prev - hp), "hit")


        # ---------- window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)


        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])


        def on_alarm_click():
            """The alarm line (full window or minimized bar): click answers,
            Alt+click follows who raised it. On the minimized bar, with no alarm
            up, a double-click restores the window (the bar's own strip is under
            this one)."""
            if Follow.alt_held():
                r = st["alarm"][-1] if st["alarm"] else st.get("last_answered")
                if r is not None and r.get("serial"):
                    queue(("follow", r["serial"]))()
                return
            if st["alarm"]:
                queue("answer")()
                return
            if st["minimized"]:
                now = time.time()
                if 0 <= now - st.get("mini_click", 0.0) <= 0.6:
                    st["mini_click"] = 0.0
                    queue("toggle_min")()
                else:
                    st["mini_click"] = now


        def window_h():
            return Kit.MARGIN + 30 + Kit.GAP + 96 + Kit.MARGIN


        def build_window():
            w, h = (MINI_W, MINI_H) if st["minimized"] else (W, window_h())
            x, y = Kit.load_pos(POS_KEY, (240, 160), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            M = Kit.MARGIN
            store = ({}, {})
            c = {}
            g = G.CreateGump(True, True)
            tip = ("Click: answer the alarm (skill loops go on). "
                   "Alt+click: auto-follow (again to stop)")
            if st["minimized"]:
                c["line"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
                c["line_w"] = w - 90
                c["alarm_hit"] = Kit.catcher(g, 14, 12, w - 90, h - 24, on_alarm_click,
                                             "Click: answer the alarm (skill loops go on). "
                                             "Double-click: restore. Alt+click: auto-follow "
                                             "(again to stop)", movable=True)
            else:
                IW = w - 2 * M
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, 96)
                c["line"] = Kit.add_label(g, "", M + 12, yb + 10, Kit.HUE_INFO)
                c["line2"] = Kit.add_label(g, "", M + 12, yb + 32, Kit.HUE_INFO)
                c["line_w"] = IW - 28
                c["alarm_hit"] = Kit.catcher(g, M + 6, yb + 6, IW - 12, 46, on_alarm_click, tip,
                                             movable=True)
                xb = M + 12
                Kit.art_button(g, store, "here", Kit.ART_OK, xb, yb + 62, "I'm here",
                               "Answer the alarm: skill loops go on (after the pause set on the "
                               "settings page)", on_click=queue("answer"))
                xb += 35 + Kit.text_w("I'm here") + 14
                Kit.art_button(g, store, "test", Kit.ART_PLAY, xb, yb + 62, "Test",
                               "Raise a test alarm: the banner, the sound and paused skill loops, "
                               "until you answer", on_click=queue("test"))
                xb += 35 + Kit.text_w("Test") + 14
                c["ignore"] = Kit.art_button(g, store, "ignore", Kit.ART_CLOSE, xb, yb + 62,
                                             "Ignore this gump",
                                             "Answer, and put the gump that raised this alarm on "
                                             "the ignore list (it never raises the alarm again)",
                                             on_click=queue("ignore_gump"))
            Kit.place(g, x, y, w, h)                     # wholly on screen (the window rules)
            win.update({"g": g, "c": c, "store": store})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))
            if st["minimized"] and st["docked"]:          # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            st["drawn"] = None
            draw()
            Kit.dispose(old)


        def watching_text():
            on = []
            if settings["gump"]:
                on.append("gumps")
            if settings["staff"]:
                on.append("staff")
            if settings["name"]:
                on.append("your name")
            if settings["whisper"]:
                on.append("whispers")
            if settings["hit"]:
                on.append("hits")
            if st["minimized"]:                            # the minimized bar: "<Title>: <status>"
                return "%s: %s" % (TITLE, ("watching " + ", ".join(on)) if on
                                   else "nothing ticked on the settings page")
            return ("Watching: " + ", ".join(on)) if on else "Nothing ticked on the settings page"


        def draw():
            """Only what changed; nothing while folded."""
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return
            c = win["c"]
            lw = c.get("line_w", 200)
            al = st["alarm"]
            if al:
                r = al[-1]
                line = ("%s: " % TITLE if st["minimized"] else "ALARM: ") + r["text"]
                hue = Kit.HUE_BAD if st["flash_on"] else Kit.HUE_TEXT
                line2 = ("+%d more. " % (len(al) - 1) if len(al) > 1 else "") + \
                    "Skill loops paused: click here or I'm here"
            else:
                left = st["resume_at"] - time.time() if st["resume_at"] else 0
                line, hue = watching_text(), Kit.HUE_INFO
                line2 = ("Skill loops go on in %d s" % int(left + 0.99)) if 0 < left <= HOLD_MAX + 1 \
                    else ("All quiet" if hasattr(HOST, "alert") else "All quiet (no alert banner)")
            key = (line, hue, line2, lw)                   # 2.6.82: the raw texts: cut only on a change
            if key == st["drawn"]:
                return
            st["drawn"] = key
            line = Kit.fit(line, lw)
            Kit.set_text(c["line"], line, hue)
            if "line2" in c:
                Kit.set_text(c["line2"], Kit.fit(line2, lw), Kit.HUE_INFO)
            ig = c.get("ignore")
            if ig is not None:
                want = bool(al) and al[-1]["kind"] == "gump"
                if c.get("ignore_on") != want:
                    c["ignore_on"] = want
                    safe(lambda: setattr(ig, "IsVisible", want))
                    b = win["store"][0].get("ignore")
                    if b is not None:
                        safe(lambda: setattr(b, "IsVisible", want))


        def ignore_gump(from_alarm):
            """A gump id goes on the ignore list: the one of the newest gump alarm
            (the window's button), or the last server gump seen (the settings page)."""
            gid = 0
            if from_alarm:
                for r in reversed(st["alarm"]):
                    if r["kind"] == "gump" and r["gid"]:
                        gid = r["gid"]
                        break
            if not gid:
                gid = st["last_gid"]
            if not gid:
                API.SysMsg("%s: no server gump seen yet." % TITLE, Kit.HUE_INFO)
                return
            if gid not in ignored_ids():
                cur = settings["ignore"].strip().strip(",")
                settings["ignore"] = (cur + ", " if cur else "") + "0x%X" % gid
                save_settings()
                HOST.refresh_settings(KEY)
                API.SysMsg("%s: gump 0x%X is on the ignore list now." % (TITLE, gid), Kit.HUE_INFO)


        # ---------- settings page (drawn inside the Virtue Assistant window) ----------
        SEC1_H, SEC2_H, SEC3_H, SEC4_H = 194, 126, 126, 66   # TRIGGERS, STAFF AND GUMPS, ALARM, DEBUG


        def config_height(w):
            return SEC1_H + Kit.GAP + SEC2_H + Kit.GAP + SEC3_H + Kit.GAP + SEC4_H


        def build_config(g, x, y, w):
            c = {}
            store = ({}, {})
            Kit.add_section(g, x, y, w, SEC1_H, "TRIGGERS  (each pauses skill loops too)")
            rows = (("gump", "A server gump opens that nobody asked for", 12,
                     "Not within %.1f s of your mouse, your typing or a gump of yours closing; "
                     "not a page of an open window or an ignored id" % ASKED_SECS),
                    ("staff", "Staff come into view (a staff word in the name or title)", 12,
                     "A mobile within %d tiles whose name or title holds a staff word (the list "
                     "below)" % STAFF_RANGE),
                    ("name", "Someone else says your character's name", 12,
                     "Your name is read from the game (whole words, any case)"),
                    ("words", "Or any word of it with 4 letters or more", 34,
                     "For a name of two words or more: \"Wolf\" in \"Grey Wolf\""),
                    ("whisper", "Someone whispers to you", 12,
                     "Lines the client marks as whispered (the DEBUG box below prints the kinds "
                     "the shard sends)"),
                    ("hit", "You take damage while not in war mode", 12,
                     "Training, not fighting: someone or something is hurting you (off at first)"))
            for i, (k, text, dx, tip) in enumerate(rows):
                c[k] = Kit.add_check(g, text, x + dx, y + 32 + i * 26, settings[k], tip)
            y2 = y + SEC1_H + Kit.GAP
            Kit.add_section(g, x, y2, w, SEC2_H, "STAFF AND GUMPS")
            Kit.add_label(g, "Staff words:", x + 12, y2 + 36)
            xt = x + 12 + Kit.text_w("Gump ids to ignore:") + 10
            c["markers"] = Kit.add_textbox(g, settings["markers"], xt, y2 + 32, w - (xt - x) - 16,
                                           numbers=False)
            safe(lambda: c["markers"].SetTooltip(
                "Words that mark a staff member's name or title, commas between them (whole "
                "words, any case). Empty: no staff check."))
            Kit.add_label(g, "Gump ids to ignore:", x + 12, y2 + 66)
            c["ignore"] = Kit.add_textbox(g, settings["ignore"], xt, y2 + 62, w - (xt - x) - 16,
                                          numbers=False)
            safe(lambda: c["ignore"].SetTooltip(
                "Server gump ids that never raise the alarm: hex (0x1A2B) or decimal, commas "
                "between them"))
            Kit.art_button(g, store, "ignore_last", Kit.ART_OK, x + 12, y2 + 92, "Ignore last gump",
                           "Put the last server gump seen on the ignore list",
                           on_click=queue("ignore_last"))
            xl = x + 12 + 35 + Kit.text_w("Ignore last gump") + 14
            c["last"] = Kit.add_label(g, last_gump_text(), xl, y2 + 95, Kit.HUE_INFO)
            y3 = y2 + SEC2_H + Kit.GAP
            Kit.add_section(g, x, y3, w, SEC3_H, "ALARM  (sound: Settings > Alerts)")
            t1, t2 = "Repeat the sound every:", "Loops stay paused after you answer:"
            xn = x + 12 + max(Kit.text_w(t1), Kit.text_w(t2)) + 10
            Kit.add_label(g, t1, x + 12, y3 + 36)
            c["repeat"] = Kit.add_textbox(g, str(settings["repeat"]), xn, y3 + 32, 40)
            safe(lambda: c["repeat"].SetTooltip("Seconds between alarm sounds until you answer "
                                                "(0-%d, 0 = only once)" % REPEAT_MAX))
            Kit.add_label(g, "s", xn + 52, y3 + 36, Kit.HUE_INFO)
            Kit.add_label(g, t2, x + 12, y3 + 66)
            c["hold"] = Kit.add_textbox(g, str(settings["hold"]), xn, y3 + 62, 40)
            safe(lambda: c["hold"].SetTooltip("Seconds skill loops stay paused after you answer "
                                              "(0-%d, 0 = they go on at once)" % HOLD_MAX))
            Kit.add_label(g, "s", xn + 52, y3 + 66, Kit.HUE_INFO)
            c["anyalarm"] = Kit.add_check(g, "Any alarm pauses skill loops", x + 12, y3 + 92,
                                          settings["anyalarm"],
                                          "Skill loops pause while any module's alarm banner waits "
                                          "for a click (an Ultima Tracker > Lookout alarm, a red in "
                                          "your house)")
            y4 = y3 + SEC3_H + Kit.GAP
            Kit.add_section(g, x, y4, w, SEC4_H, "DEBUG  (for checking the shard's texts)")
            c["say"] = Kit.add_check(g, "Print every gump, staff match and odd line in the journal",
                                     x + 12, y4 + 32, settings["say"],
                                     "Why each server gump did or didn't raise the alarm, each "
                                     "staff match and the kind of every unusual line (whispers)")
            page.update({"c": c, "store": store, "last_shown": st["last_gid"]})


        def last_gump_text():
            return ("Last server gump: 0x%X" % st["last_gid"]) if st["last_gid"] else \
                "No server gump seen yet"


        def _num(ctl, cur, hi):
            try:
                n = int(str(ctl.Text or "").strip())
            except Exception:
                return cur                                 # empty or half-typed: keep it
            return max(0, min(hi, n))


        def poll_config():
            c = page["c"]
            if c is None:
                return
            if "ignore_last" in st["queue"]:               # (the module may be off)
                st["queue"].remove("ignore_last")
                ignore_gump(False)
                return
            changed = False                                # (every pass while the page is up:
            for k in TRIGGERS + ("say", "anyalarm"):       # plain try, no lambda per read)
                try:
                    on = bool(c[k].IsChecked)
                except Exception:
                    continue
                if on != settings[k]:
                    settings[k] = on
                    changed = True
            for k in ("markers", "ignore"):
                try:
                    v = _clean(c[k].Text)
                except Exception:
                    continue
                if v != _clean(settings[k]):
                    settings[k] = v
                    changed = True
            for k, hi in (("repeat", REPEAT_MAX), ("hold", HOLD_MAX)):
                n = _num(c[k], settings[k], hi)
                if n != settings[k]:
                    settings[k] = n
                    changed = True
            if page.get("last_shown") != st["last_gid"]:
                page["last_shown"] = st["last_gid"]
                Kit.set_text(c["last"], last_gump_text(), Kit.HUE_INFO)
            if changed:
                save_settings()
                st["drawn"] = None                         # the "Watching:" line may change


        def config_closed():
            page["c"] = None
            page["store"] = ({}, {})


        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "docked": False, "active": True, "alarm": [],
                       "queue": [a for a in st["queue"] if a == "ignore_last"],
                       "resume_at": 0.0, "next_gump": 0.0, "gump_obj": None, "gump_gid": 0,
                       "gump_vis": False, "primed": False, "input": None,
                       "asked_at": 0.0, "used_at": 0.0, "cursor_up": False,
                       "typing": None, "typed_at": 0.0,
                       "next_staff": 0.0, "checked": {}, "staff_seen": {}, "name_at": 0.0,
                       "next_hit": 0.0, "hp": None, "heard": [], "next_sound": 0.0,
                       "banner_seen": False, "flash_at": 0.0, "flash_on": False, "drawn": None,
                       "last_answered": None, "rd": Journal.reader(), "checked_pat": None,
                       "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            load_settings()
            hook_events()
            if hasattr(HOST, "alert_kind"):
                for k, akey, label, snd in KINDS:
                    HOST.alert_kind(akey, label, snd)
            HOST.services["attention.up"] = is_up
            build_window()
            HOST.dock_add(KEY, _scaled_hooks(TITLE, TRAY_ICON, st, win, queue("redraw")))


        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])            # on_disposed turns the module off
                return
            now = time.time()
            while st["queue"]:
                action = st["queue"].pop(0)
                kind = action[0] if isinstance(action, tuple) else action
                if action == "settings":
                    HOST.show_settings(KEY)
                elif action == "toggle_min":
                    st["minimized"] = not st["minimized"]
                    st["docked"] = False
                    HOST.dock_forget(KEY)
                    Kit.save_min(MIN_KEY, st["minimized"])
                    build_window()
                elif action == "to_bar":
                    HOST.dock_to_bar(KEY, TITLE)
                elif action == "redraw":
                    build_window()
                elif kind == "follow":
                    Follow.toggle(action[1], TITLE)
                elif action == "answer":
                    answer("click")
                elif action == "test":
                    raise_alarm("test", "Test alarm: answer it to go on", "test")
                elif action == "ignore_gump":
                    ignore_gump(True)
                    answer("click")
                elif action == "ignore_last":
                    ignore_gump(False)
            p = HOST.me()                                  # 2.6.82: the pass's player (reads kept)
            if p is None:
                return
            read_me(now, p)
            if not 0 < st["next_gump"] - now <= GUMP_EVERY:
                st["next_gump"] = now + GUMP_EVERY
                gump_tick(now)
                st["primed"] = True
            if settings["staff"] and not 0 < st["next_staff"] - now <= STAFF_EVERY:
                st["next_staff"] = now + STAFF_EVERY
                staff_tick(now)
            speech_tick(now)
            heard_tick()
            if not 0 < st["next_hit"] - now <= HIT_EVERY:
                st["next_hit"] = now + HIT_EVERY
                hit_tick(p)
            alarm_tick(now)
            if not st["alarm"] and st["resume_at"]:
                if not is_up():
                    st["resume_at"] = 0.0
                draw()                                     # the countdown (only when it changes)


        def _stop():
            st["shutting"] = True
            st["active"] = False
            if HOST.services.get("attention.up") is is_up:
                HOST.services.pop("attention.up", None)
            st["alarm"] = []
            st["resume_at"] = 0.0
            HOST.dock_remove(KEY)
            save_pos()
            Kit.save_min(MIN_KEY, st["minimized"])
            save_settings()
            st["rd"] = None
            st["gump_obj"] = None
            g, win["g"] = win["g"], None
            Kit.dispose(g)


        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,          # tick on the client thread: no waits in it
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    def _part_bags():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the Virtue Assistant script from
        #  this file uses (API, G, safe, Client, Kit, Follow, HOST, Journal, the main
        #  its Modules tab.
        # ============================ MODULE START ===================================
        #  MODULE: Skill Bags  -  use a skill on everything in a bag
        #
        #  A rule pairs a bag with an action and an item filter: "Item Identification
        #  on every item in this bag", "Remove Trap on every container in that one",
        #  "Lockpicking on every chest", "decode every treasure map". With Auto on,
        #  the rule watches its bag and handles every new item that lands in it; Run
        #  does one pass by hand. Each item is handled once (the result is remembered
        #  per character) until the rule is Reset.
        #
        #  Actions come in three kinds: a skill (use it, then target the item), a tool
        #  from your backpack (lockpicks: use them, then target the item) and a plain
        #  double-click of the item itself (a treasure map decodes that way). Two
        #  custom actions take any skill name or tool graphic.
        #
        #  Everything runs on the client tick with no waits: one item at a time, the
        #  cursor is claimed while a skill's target cursor is awaited, the server's
        #  answer is read from the shared journal, and the next item follows after
        #  the rule's delay. Nothing happens while you have a cursor up yourself,
        #  while another module has the cursor, while you are hidden (option) or in
        #  war mode (always, 2.6.71), in a guard zone (always, unless unticked while
        #  Training Alarm is on, 2.6.71: macroing isn't allowed in towns), or while
        #  you are dead. 2.6.06: nor while an
        #  alarm that wants you at the keyboard is unanswered (the Training Alarm's
        #  HOST.services["attention.up"], when that module is on).
        #
        #  Results (2.6.05): the shard's answer to every item a rule handles (Item
        #  Identification: the item's label, magic or plain; Remove Trap: disarmed,
        #  failed or no trap; ...) is listed per rule in a Results window, with
        #  counts and an Export to a text file next to Virtue Assistant. Kept for
        #  the session, RES_KEEP per rule.
        # =============================================================================
        KEY = "skillbags"
        TITLE = "Skill Bags"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "SkillBags_settings"   # global options (per character)
        RULES_KEY = "SkillBags_rules"         # the rules
        DONE_KEY = "SkillBags_done"           # per rule: the items already handled
        POS_KEY = "SkillBags_pos"
        MIN_KEY = "SkillBags_min"             # minimized when last seen
        W = 740                               # full window width (height follows the rules); 2.6.05:
        #                                       80 px wider for each rule's Results button
        MINI_W, MINI_H = 240, 46              # minimized bar
        TRAY_ICON = 0x0E76                    # a bag, on the Action Bar's tray button
        ROW_H = 42                            # one rule per row in the window: the rule's line
        #                                       and, under it, the shard's last answer to it
        MAX_RULES = 8                         # rules at most. The window grows by ROW_H per rule
        #                                       (window_h, build_window) and the settings page by
        #                                       SEC_R (config_height); 8 rows fit a 1080 screen.
        #                                       Past that, the rules section needs a scroll area
        #                                       (G.CreateScrollArea holding the rows, a fixed
        #                                       height) instead of a taller window.
        MAX_DONE = 300                        # remembered items per rule (oldest dropped)
        NAME_SCANS_MAX = 6                    # scans an item's name may stay unknown before the
        #                                       item is skipped (the server never answered)
        RELIST_EVERY = 5.0                    # seconds between full listings of a bag whose item
        #                                       count didn't change (items inside inner bags)
        BAG_NAME_EVERY = 2.0                  # seconds between reads of a bag's name for the rows
        TARGET_TIMEOUT = 3.0                  # seconds to wait for the skill's target cursor
        OPEN_TIMEOUT = 2.5                    # seconds to wait for a bag to open
        OPEN_RETRY = 6.0                      # seconds before a bag that didn't open is tried again
        BUSY_RETRY = 1.5                      # seconds before an item is tried again after "must wait"
        MAX_BUSY = 4                          # "must wait" / no cursor answers before an item is given up
        # 2.6.81: the shard's skill timers (in-mani-ylem-rules section 6): a skill rule's
        # delay never goes under its skill's timer, and a "must wait" answer to a skill
        # is waited out (not counted toward MAX_BUSY)
        SKILL_TIMER = 10.0
        SKILL_TIMER_SHORT = {"item identification": 3.0, "arms lore": 3.0, "detect hidden": 3.0}
        MIN_DELAY, MAX_DELAY = 0.5, 60.0      # bounds of a rule's delay between items (s)
        DEFAULT_RETRIES = 1                   # extra attempts after a failed attempt
        CHECK_EVERY = 0.25                    # seconds between looks at the window's checkboxes
        SCAN_EVERY = 0.5                      # seconds between looks inside the bags
        LOCKPICK_GRAPHIC = 0x14FC             # lockpicks (the tool Lockpicking uses)
        # Lines the server answers with. BUSY: try the same item again shortly.
        # The rest are per action: OK / FAIL / SKIP (nothing to do on that item).
        # These are RunUO / ServUO defaults, not checked against In Mani Ylem's
        # texts: the DEBUG box on the settings page prints every journal line seen while
        # an answer is awaited, so a phrase that never matches can be spotted.
        BUSY_WORDS = ("must wait", "too far away", "cannot reach", "can't reach",
                      "can't see that", "cannot see that", "already casting", "you are busy")
        GUARD_STATUS = "Paused: guard zone"   # 2.6.05: the status while HOST.guarded() pauses the rules
        UNKNOWN_STATUS = HOLD_TEXT["unknown"]  # 2.6.81: the zone isn't known yet (the strict reading)
        # 2.6.5: anything of a fight pauses the rules too (the shard's rules: no skill
        # loop while fighting), always, not as a setting. 2.6.81: the mother's one fight
        # test, HOST.fight_hold(): dead, war mode, damage taken in the last HURT_SECS, a
        # hostile within FOE_RANGE (players and monsters; your own pets skipped), an item
        # held on the cursor, an alarm waiting for you. Status "Paused: " + HOLD_TEXT[why]
        # 2.6.05: the results list (per rule, this session)
        RES_POS_KEY = "SkillBags_results_pos"  # where the Results window sits
        RES_KEEP = 200                        # results kept per rule (the oldest dropped)
        RES_ROWS = 16                         # rows in the Results window; Prev / Next page through the rest
        RES_W = 680                           # the Results window's width
        RES_ROW_H = 18
        RES_ANSWER_MAX = 160                  # characters of the shard's answer kept per item
        EXPORT_NAME = "SkillBags_%08X_rule%d.txt"   # the Export, next to Virtue Assistant (player serial, rule)
        # Item Identification: a word in the item's label (the attribute list the client
        # shows on the item after a successful identification, "[Vanquishing/Accurate]")
        # that makes it "magic": the pre-AoS weapon / armour attribute names (Cliloc
        # 1038001-1038020, the client spells one "Indestructable") and slayer names (Cliloc
        # 1017384-1017409); a "[spell : charges]" part counts too. Unchecked on the shard:
        # the DEBUG box prints the lines it sends.
        ITEMID_MAGIC = ("durable", "substantial", "massive", "fortified", "indestructable",
                        "indestructible", "defense", "guarding", "hardening", "fortification",
                        "invulnerability", "accurate", "ruin", "might", "force", "power", "vanquishing",
                        "silver", "slaying", "slaughter", "thrashing", "repond", "terathan", "bane",
                        "reptilian death", "dismissal", "gargoyle's foe", "damnation", "exorcism",
                        "ophidian", "spider's death", "arachnid doom", "dousing", "dissipation",
                        "vacuum", "elemental health", "earth shatter", "blood drinking", "summer wind",
                        "elemental ban", "slayer", "magic")
        ITEMID_UNKNOWN = "unidentified"       # in the label (Cliloc 1038000): the identification didn't take
        # The word each answer is listed under, per action (the rest: OK / failed / skipped / done)
        RESULT_WORDS = {"itemid": {2: "not certain"},
                        "armslore": {2: "not certain", 4: "read"},
                        "tasteid": {2: "not certain", 4: "read"},
                        "removetrap": {1: "disarmed", 2: "trap, not disarmed", 3: "no trap"},
                        "lockpick": {1: "unlocked", 2: "still locked", 3: "not locked"},
                        "cartography": {1: "decoded", 2: "not decoded", 3: "can't decode"}}
        # -----------------------------------------------------------------------------
        ITEMID_MAGIC_RE = re.compile(r"\b(" + "|".join(ITEMID_MAGIC) + r")\b")
        ITEMID_CHARGES_RE = re.compile(r"\[[^\]]*:\s*\d+\s*\]")    # "[Clumsiness : 5]"
        ITEMID_MAGIC_WORD = re.compile(r"\bmagic\b")               # no attribute list: "magic wand"

        #  key, caption, kind ("skill" / "tool" / "use" / "cskill" / "ctool"), what
        #  (skill name or tool graphic), default delay, default filter, OK, FAIL, SKIP
        ACTIONS = [
            ("itemid", "Item Identification", "skill", "Item Identification", 3.2, 0,
             (), ("not certain", "no idea how much", "tell much about it"), ()),
            ("armslore", "Arms Lore", "skill", "Arms Lore", 3.2, 0,
             (), ("not certain", "tell much about it"), ()),
            ("tasteid", "Taste Identification", "skill", "Taste Identification", 10.2, 0,
             (), ("not certain", "tell much about it", "can't tell"), ()),
            ("removetrap", "Remove Trap", "skill", "Remove Trap", 10.2, 1,
             ("render the trap harmless", "successfully"), ("fail to disarm",),
             ("doesn't appear to be trapped", "isn't trapped", "not trapped")),
            ("lockpick", "Lockpicking (uses lockpicks)", "tool", LOCKPICK_GRAPHIC, 1.5, 1,
             ("lock quickly yields",), ("unable to pick the lock",),
             ("does not appear to be locked", "cannot be picked by normal means",
              "did not need to be unlocked")),
            ("cartography", "Cartography (decode maps)", "use", None, 1.0, 3,
             ("successfully decode",), ("fail to make anything of the map",),
             ("too difficult to attempt to decode", "not a map")),
            ("use", "Double-click each item", "use", None, 1.0, 0, (), (), ()),
            ("cskill", "Custom skill (name in Custom)", "cskill", None, 10.2, 0, (), (), ()),
            ("ctool", "Custom tool (graphic in Custom)", "ctool", None, 1.5, 0, (), (), ()),
        ]
        ACTION_KEYS = [a[0] for a in ACTIONS]
        ACTION_NAMES = [a[1] for a in ACTIONS]
        FILTERS = [("all", "Every item"), ("containers", "Containers only"),
                   ("graphics", "Graphics in Text (hex)"), ("name", "Name contains Text")]
        FILTER_NAMES = [f[1] for f in FILTERS]
        CODE_TEXT = {1: "OK", 2: "failed", 3: "skipped", 4: "done"}

        settings = {"hidden": True, "war": True, "open": True, "retries": DEFAULT_RETRIES,
                    "say": False,          # 2.6.01: print the journal lines seen while waiting
                    "guard": True}         # 2.6.05: pause in guard zones (on by default)
        rules = []                 # dicts: action, bag, filt, text, custom, delay, deep, auto, done
        #                            (and, unsaved: _cache (the bag's listing), _count, _last,
        #                            _gfx, _tries, _bagname, _res (the results, 2.6.05), _rescount)
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
              "paused": False, "job": None, "next_scan": 0.0, "next_check": 0.0,
              "status": "", "run": set(), "opening": {}, "later": {}, "pick": None,
              "rows": 0, "no_tool": {}, "busy_n": {}, "next_rows": 0.0,
              "rr": 0,                 # the rule looked at next (one rule per scan, round-robin)
              "guard_paused": None,    # 2.6.05: a guard zone pauses the rules now (2.6.81:
              #                          HOST.guard_hold()'s "guard" / "unknown", or None)
              "writes": []}            # 2.6.05: (path, text) exports for thread_tick to write
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        page = {"c": None, "store": ({}, {}), "rows": [], "next_read": 0.0}
        # 2.6.05: the Results window (one at a time, showing one rule's results)
        resw = {"g": None, "rule": None, "c": {}, "rows": [], "store": ({}, {}), "page": 0,
                "dirty": False}

        # ---------- small helpers ----------
        def esc(s):
            return str(s or "").replace("|", "/").replace("~", "-")

        def clamp_delay(v, default):
            try:
                v = float(v)
            except Exception:
                return default
            return max(MIN_DELAY, min(MAX_DELAY, v))

        def new_rule(action=0):
            a = ACTIONS[action]
            return {"action": action, "bag": 0, "filt": a[5], "text": "", "custom": "",
                    "delay": a[4], "deep": False, "auto": False, "done": {}, "order": []}

        def rule_action(r):
            return ACTIONS[r["action"]]

        def skill_floor(r):
            """2.6.81: the shard's timer of the rule's skill (s), 0 for tool and use rules."""
            a = ACTIONS[r["action"]]
            if a[2] == "skill":
                name = a[3]
            elif a[2] == "cskill":
                name = r["custom"].strip()
                if not name:
                    return 0.0
            else:
                return 0.0
            return SKILL_TIMER_SHORT.get(name.lower(), SKILL_TIMER)

        def parse_graphics(text):
            out = []
            for part in str(text or "").replace(";", ",").split(","):
                part = part.strip()
                if not part:
                    continue
                try:
                    out.append(int(part, 16) if part.lower().startswith("0x") else int(part, 0))
                except Exception:
                    try:
                        out.append(int(part, 16))
                    except Exception:
                        pass
            return out

        # ---------- saved settings ----------
        def load_settings():
            p = Kit.get_var(SETTINGS_KEY).split("|")
            if len(p) >= 4:
                settings["hidden"] = p[0] == "1"
                settings["war"] = p[1] == "1"
                settings["open"] = p[2] == "1"
                try:
                    settings["retries"] = max(0, min(9, int(p[3])))
                except Exception:
                    settings["retries"] = DEFAULT_RETRIES
            if len(p) >= 5:                                   # 2.6.01, after the old four
                settings["say"] = p[4] == "1"
            settings["guard"] = (p[5] == "1") if len(p) >= 6 else True   # 2.6.05 (older saves: on)
            del rules[:]
            raw = Kit.get_var(RULES_KEY)
            if raw:
                for chunk in raw.split("|"):
                    f = chunk.split("~")
                    if len(f) < 8:
                        continue
                    try:
                        r = new_rule(max(0, min(len(ACTIONS) - 1, int(f[0]))))
                        r["bag"] = int(f[1]) if f[1] else 0
                        r["filt"] = max(0, min(len(FILTERS) - 1, int(f[2])))
                        r["text"] = f[3]
                        r["custom"] = f[4]
                        r["delay"] = clamp_delay(f[5], rule_action(r)[4])
                        r["delay"] = max(r["delay"], skill_floor(r))   # 2.6.81: older saves had 1.5 s
                        r["deep"] = f[6] == "1"
                        r["auto"] = f[7] == "1"
                        rules.append(r)
                    except Exception:
                        continue
                    if len(rules) >= MAX_RULES:
                        break
            raw = Kit.get_var(DONE_KEY)
            if raw:
                lists = raw.split("|")
                for i, r in enumerate(rules):
                    if i >= len(lists):
                        break
                    for part in lists[i].split(","):
                        if ":" not in part:
                            continue
                        s, c = part.split(":", 1)
                        try:
                            s, c = int(s), int(c)
                        except Exception:
                            continue
                        r["done"][s] = c
                        r["order"].append(s)

        def save_settings():
            Kit.put_var(SETTINGS_KEY, "|".join([
                "1" if settings["hidden"] else "0", "1" if settings["war"] else "0",
                "1" if settings["open"] else "0", str(settings["retries"]),
                "1" if settings["say"] else "0",
                "1" if settings["guard"] else "0"]))           # 2.6.05: a sixth field
            Kit.put_var(RULES_KEY, "|".join(
                "~".join([str(r["action"]), str(r["bag"]), str(r["filt"]), esc(r["text"]),
                          esc(r["custom"]), "%.2f" % r["delay"], "1" if r["deep"] else "0",
                          "1" if r["auto"] else "0"]) for r in rules))
            save_done()

        def save_done():
            Kit.put_var(DONE_KEY, "|".join(
                ",".join("%d:%d" % (s, r["done"][s]) for s in r["order"] if s in r["done"])
                for r in rules))

        def mark_done(r, serial, code):
            if serial not in r["done"]:
                r["order"].append(serial)
            r["done"][serial] = code
            order = r["order"]
            if len(order) > MAX_DONE:                      # 2.6.82: the oldest dropped in one cut
                k = len(order) - MAX_DONE
                done = r["done"]
                for old in order[:k]:
                    done.pop(old, None)
                del order[:k]
            st["save_done"] = True

        # ---------- 2.6.05: the results (the shard's answer per item) ----------
        def result_tag(a, code, answer):
            """The word an item's result is listed and counted under."""
            if a[0] == "itemid" and code in (1, 4):
                low = (answer or "").lower()
                if not low:
                    return "no answer"
                if ITEMID_UNKNOWN in low:
                    return "unidentified"
                if ITEMID_CHARGES_RE.search(low):
                    return "magic"
                k = low.find("[")                    # the attribute list: the words count only there
                if k >= 0:                           # (a plain "silver ring" is not a Silver slayer)
                    return "magic" if ITEMID_MAGIC_RE.search(low, k) else "plain"
                return "magic" if ITEMID_MAGIC_WORD.search(low) else "plain"
            words = RESULT_WORDS.get(a[0])
            if words is not None and code in words:
                return words[code]
            return CODE_TEXT.get(code, "done")

        def answer_of(j):
            """The shard's answer to a job, as said: the line a phrase matched, else
            the item's own label (a line spoken by the item, naming it, or an
            attribute list "[...]"), else the last system line, else the last line
            seen ("" when none came)."""
            if j.get("match_raw"):
                return j["match_raw"]
            raw = j.get("raw")
            if not raw:
                return ""
            nm = (j.get("name") or "").lower()
            best = None
            for k in range(len(raw) - 1, -1, -1):
                text, name = raw[k]
                ln = name.lower()
                if (nm and (ln == nm or (len(nm) >= 3 and nm in text.lower()))) or text.lstrip().startswith("["):
                    return text
                if best is None and (not name or ln == "system"):
                    best = text
            return best if best is not None else raw[-1][0]

        def add_result(r, serial, code, name, answer, tag=None):
            """An item is done: its answer goes in the rule's results (newest
            last; an item handled again replaces its old line; RES_KEEP kept)."""
            res = r.get("_res")
            if res is None:
                res = r["_res"] = []
            for k in range(len(res) - 1, -1, -1):
                if res[k][1] == serial:
                    del res[k]
                    break
            answer = str(answer or "").replace("\n", " ").strip()[:RES_ANSWER_MAX]
            res.append((time.time(), serial, name or ("0x%08X" % serial), code,
                        tag or result_tag(rule_action(r), code, answer), answer))
            if len(res) > RES_KEEP:
                del res[:-RES_KEEP]
            r.pop("_rescount", None)
            if resw["rule"] is r:
                resw["dirty"] = True

        def clear_results(r):
            r.pop("_res", None)
            r.pop("_rescount", None)
            if resw["rule"] is r:
                resw["dirty"] = True

        def _by_count(kv):
            return (-kv[1], kv[0])

        def counts_text(r):
            """"24 items: 5 magic, 19 plain" (worked out when the results change)."""
            txt = r.get("_rescount")
            if txt is None:
                res = r.get("_res") or []
                if not res:
                    txt = "No results yet: each item's answer shows here once the rule handles it."
                else:
                    cnt = {}
                    for e in res:
                        cnt[e[4]] = cnt.get(e[4], 0) + 1
                    txt = "%d item%s: %s" % (len(res), "" if len(res) == 1 else "s",
                                             ", ".join(["%d %s" % (n, t) for t, n in
                                                        sorted(cnt.items(), key=_by_count)]))
                r["_rescount"] = txt
            return txt

        # ---------- the bags and their items ----------
        def get_item(serial):
            if not serial:
                return None
            try:
                return API.FindItem(serial)
            except Exception:
                return None

        def bag_name(r, short=True):
            """The bag's name (re-read every BAG_NAME_EVERY seconds: the window's
            rows ask several times a second)."""
            if not r["bag"]:
                return "no bag yet"
            now = time.time()
            cached = r.get("_bagname")
            if cached is not None and cached[0] == r["bag"] and now < cached[1]:
                name = cached[2]
            else:
                it = get_item(r["bag"])
                if it is None:
                    name = "bag not found"
                else:
                    name = ""
                    try:
                        name = str(it.Name or "")
                    except Exception:
                        pass
                    if not name:
                        name = "0x%08X" % r["bag"]
                r["_bagname"] = (r["bag"], now + BAG_NAME_EVERY, name)
            return name if short else "%s  0x%08X" % (name, r["bag"])


        def invalidate(r=None):
            """Forget the bag listings (of one rule, or all): the next look lists
            the bag again. Called when a rule or its filter changes."""
            for rule in ([r] if r is not None else rules):
                rule.pop("_cache", None)
                rule.pop("_bagname", None)

        def matches(r, it):
            """Does this item pass the rule's filter? None: not known yet (name)."""
            f = FILTERS[r["filt"]][0]
            if f == "all":
                return True
            if f == "containers":
                try:
                    return bool(it.IsContainer)
                except Exception:
                    return False
            if f == "graphics":
                try:
                    return int(it.Graphic) in r["_gfx"]
                except Exception:
                    return False
            if f == "name":
                want = r["text"].strip().lower()
                if not want:
                    return True
                name = ""
                try:
                    name = str(it.Name or "")
                except Exception:
                    pass
                if not name:
                    try:                     # asks the server for the tooltip; back later
                        name = str(API.ItemNameAndProps(it.Serial, False) or "").split("\n")[0]
                    except Exception:
                        name = ""
                if not name:
                    return None
                return want in name.lower()
            return True

        def bag_count(serial):
            """The bag's item count as the client knows it (one call)."""
            try:
                return int(API.Contents(serial) or 0)
            except Exception:
                return -1


        def bag_items(r, i, now, may_list=True):
            """The items of the rule's bag that pass its filter: ((serial, item)
            pairs, how many are still waiting for a name, listed now?). The bag is
            listed again (API.ItemsInContainer, one filter check per item) only
            when its item count changed, every RELIST_EVERY seconds, or when the
            rule changed (invalidate); between listings the cached list serves,
            and only the items whose name hasn't come yet are asked again. An item
            whose name never comes in NAME_SCANS_MAX scans is marked skipped (code
            3). With may_list False (another bag was listed this pass) a listing
            that is due waits: the cached list serves (listed None), or None comes
            back when there is none yet."""
            bag = get_item(r["bag"]) if r["bag"] else None
            if bag is None:
                r.pop("_cache", None)
                return [], 0, False
            cache = r.get("_cache")
            count = bag_count(r["bag"])
            listed = False                    # True: listed now; None: a listing is due but waits
            if (cache is None or cache["count"] != count or now >= cache["relist"]
                    or cache["bag"] != r["bag"]):
                if not may_list:
                    if cache is None:
                        return None
                    listed = None
                else:
                    listed = True
            if listed:
                try:
                    items = list(API.ItemsInContainer(r["bag"], bool(r["deep"])) or [])
                except Exception:
                    items = []
                if FILTERS[r["filt"]][0] == "graphics":
                    r["_gfx"] = set(parse_graphics(r["text"]))
                scans = cache["scans"] if cache is not None else {}
                out, pending = [], []
                for it in items:
                    try:
                        serial = int(it.Serial)
                    except Exception:
                        continue
                    if serial == r["bag"]:
                        continue
                    m = matches(r, it)
                    if m is None and serial in r["done"]:
                        m = True                           # handled already: counted, not asked again
                    if m is None:
                        pending.append((serial, it))
                    elif m:
                        out.append((serial, it))
                        scans.pop(serial, None)
                cache = {"bag": r["bag"], "count": count, "relist": now + RELIST_EVERY,
                         "items": out, "pending": pending, "scans": scans}
                r["_cache"] = cache
            elif cache["pending"]:
                # the names asked for last time may have come: check those items only
                still = []
                for serial, it in cache["pending"]:
                    m = matches(r, it)
                    if m is None:
                        still.append((serial, it))
                    elif m:
                        cache["items"].append((serial, it))
                cache["pending"] = still
            # a name that never comes: give the item up after NAME_SCANS_MAX scans
            scans = cache["scans"]
            gave_up = []
            for serial, it in cache["pending"]:
                n = scans.get(serial, 0) + 1
                scans[serial] = n
                if n >= NAME_SCANS_MAX:
                    scans.pop(serial, None)
                    gave_up.append((serial, it))
                    cache["items"].append((serial, it))
                    mark_done(r, serial, 3)
                    add_result(r, serial, 3, "", "its name never came", "skipped (no name)")
                    API.SysMsg("%s: 0x%08X skipped, its name never came (rule %d)." %
                               (TITLE, serial, i + 1), Kit.HUE_INFO)
            if gave_up:                                    # 2.6.82: the list rebuilt once (no remove per item)
                gone = set(s for s, _ in gave_up)
                cache["pending"] = [p for p in cache["pending"] if p[0] not in gone]
            if len(scans) > MAX_DONE:
                scans.clear()
            return cache["items"], len(cache["pending"]), listed

        def bag_opened(serial):
            it = get_item(serial)
            if it is None:
                return False
            try:
                if it.Opened:
                    return True
            except Exception:
                pass
            try:
                return int(API.Contents(serial) or 0) > 0
            except Exception:
                return False

        def ensure_open(r, now):
            """A bag the client hasn't looked inside shows no items. Open it once
            (double-click) and give it a moment. True when its contents are usable."""
            serial = r["bag"]
            if not serial or bag_opened(serial):
                st["opening"].pop(serial, None)
                return True
            if not settings["open"] or get_item(serial) is None:
                return False
            o = st["opening"].get(serial)
            if o is None or now > o + OPEN_TIMEOUT + OPEN_RETRY:
                st["opening"][serial] = now
                API.UseObject(serial)
            return False

        # ---------- the job: one item at a time ----------
        def blocked(now):
            """Why nothing can run right now (a short status), or None."""
            if st["paused"]:
                return "Paused"
            p = HOST.me()                                  # 2.6.82: the pass's player (reads kept)
            if p is None:
                return "No player"
            # 2.6.81: the mother's one fight test (SK-2: an item held on the cursor;
            # SK-3: hostile monsters too, your own pets and summons skipped)
            why = HOST.fight_hold(now)
            if why == "dead":
                return "Dead"
            try:
                if settings["hidden"] and p.IsHidden:
                    return "Hidden"
            except Exception:
                pass
            if why == "war":                               # (2.6.71) always: the shard's rules
                return "War mode"
            gp = st["guard_paused"]
            if gp == "unknown":                            # 2.6.81: the zone isn't known yet
                return UNKNOWN_STATUS
            if gp:                                         # 2.6.05: no macroing in guard zones
                return GUARD_STATUS
            if why:                                        # 2.6.5: nothing in a fight
                return "Paused: " + HOLD_TEXT.get(why, why)
            if HOST.cursor_busy(KEY):
                return "Cursor busy"
            if API.HasTarget("any"):
                return "Cursor up"
            return None

        def pick_next(now):
            """The next (rule, serial) to handle: the first item of a running rule
            (Auto on, or a Run pass) which isn't done and isn't waiting. The rules
            are looked at round-robin (st["rr"]) and at most ONE bag is listed per
            scan (bag_items lists only when its count changed or every
            RELIST_EVERY): several deep bags no longer all get listed every half
            second, and the rules take turns at their items."""
            n = len(rules)
            if not n:
                return None
            start = st["rr"] % n
            listed = False
            for k in range(n):
                i = (start + k) % n
                r = rules[i]
                if not (r["auto"] or i in st["run"]) or not r["bag"]:
                    continue
                if not ensure_open(r, now):
                    continue
                got = bag_items(r, i, now, not listed)
                if got is None:                            # needs a listing: another bag had this scan's
                    continue
                items, unknown, did = got
                if did:
                    listed = True
                    st["rr"] = i + 1                       # the next scan lists another bag first
                r["_count"] = (sum(1 for s, it in items if s in r["done"]), len(items))
                waiting = False                            # 2.6.81: an item waits for its retry
                for serial, it in items:
                    if serial in r["done"]:
                        continue
                    if st["later"].get((i, serial), 0.0) > now:
                        waiting = True                     # (a Run pass doesn't end before it)
                        continue
                    return i, r, serial, it
                if i in st["run"] and not unknown and not waiting and did is not None:
                    st["run"].discard(i)                   # the pass is over (on a fresh listing)
                    API.SysMsg("%s: %s on %s, %d of %d handled." % (
                        TITLE, rule_action(r)[1], bag_name(r), r["_count"][0], r["_count"][1]),
                        Kit.HUE_GOOD)
            return None

        def auto_off(i, r):
            """2.6.81: a rule that can't run: its Run pass ends and its Auto goes off,
            saved and shown (the window's and the page's ticked boxes would turn it
            back on, and the error would repeat twice a second)."""
            st["run"].discard(i)
            r["auto"] = False
            save_settings()
            if i < len(win["rows"]):
                try:
                    win["rows"][i]["auto"].IsChecked = False
                except Exception:
                    pass
            if page["c"] is not None:
                HOST.refresh_settings(KEY)

        def start_job(i, r, serial, it, now):
            a = rule_action(r)
            kind = a[2]
            j = {"rule": i, "serial": serial, "t": now, "phase": "target", "reader": None,
                 "lines": [], "retry": False,
                 "raw": [],                # 2.6.05: (text, speaker) beside each lower-case line
                 "name": ""}               # 2.6.05: the item's name, for its result
            try:
                j["name"] = str(it.Name or "")
            except Exception:
                pass
            if kind == "cskill":
                name = r["custom"].strip()
                if not name:
                    API.SysMsg("%s: rule %d needs a skill name in its Custom box on the settings "
                               "page." % (TITLE, i + 1), Kit.HUE_BAD)
                    auto_off(i, r)
                    return False
                HOST.claim_cursor(KEY, TARGET_TIMEOUT + 0.5)
                j["reader"] = Journal.reader()
                API.UseSkill(name)
            elif kind == "skill":
                HOST.claim_cursor(KEY, TARGET_TIMEOUT + 0.5)
                j["reader"] = Journal.reader()
                API.UseSkill(a[3])
            elif kind in ("tool", "ctool"):
                graphic = a[3]
                if kind == "ctool":
                    gl = parse_graphics(r["custom"])
                    graphic = gl[0] if gl else 0
                    if not graphic:
                        API.SysMsg("%s: rule %d needs a tool graphic in its Custom box on the "
                                   "settings page." % (TITLE, i + 1), Kit.HUE_BAD)
                        auto_off(i, r)
                        return False
                tool = None
                try:
                    tool = API.FindType(int(graphic), API.Backpack)
                except Exception:
                    tool = None
                if not tool:
                    if st["no_tool"].get(i, 0.0) < now:
                        st["no_tool"][i] = now + 10.0
                        API.SysMsg("%s: no tool 0x%04X in your backpack for rule %d." %
                                   (TITLE, int(graphic), i + 1), Kit.HUE_BAD)
                    st["later"][(i, serial)] = now + 10.0
                    st["run"].discard(i)                   # 2.6.81: a Run pass ends (the line says why)
                    return False
                HOST.claim_cursor(KEY, TARGET_TIMEOUT + 0.5)
                j["reader"] = Journal.reader()
                API.UseObject(tool.Serial)
            else:                                          # "use": double-click the item
                j["reader"] = Journal.reader()
                API.UseObject(serial)
                j["phase"] = "recover"
            st["job"] = j
            return True

        va_pref = {"t": None}        # 2.6.81: "<title>:" of every Virtue Assistant module and part

        def va_prefixes():
            """The lower-case journal prefixes of Virtue Assistant's own lines (the
            mother, every module and part), read once: the modules don't change."""
            t = va_pref["t"]
            if t is None:
                out = set([APP_NAME.lower() + ":"])
                try:
                    for sl in HOST.slots:
                        out.add(str(sl.title).lower() + ":")
                        for pt in (sl.parts or ()):
                            if len(pt) > 1:
                                out.add(str(pt[1]).lower() + ":")
                except Exception:
                    pass
                t = va_pref["t"] = tuple(out)
            return t

        def is_answer(j, ln):
            """2.6.81: may this journal line be the shard's answer to the job? Lines
            the client printed itself (Virtue Assistant's) and other mobiles' speech
            are not: the shard's (speaker empty or "System"), or the item's own
            overhead line (speaker = the item's name, or an Item ID label "[...")."""
            kind = (ln.kind or "").upper()
            if kind == "CLIENT" or ln.low.startswith(va_prefixes()):
                return False
            who = (ln.name or "").strip().lower()
            if not who or who == "system":
                return True
            if kind != "OBJECT":
                return False
            if not j["name"] and not j.get("named"):       # no name at the start: read it again
                j["named"] = True
                it = get_item(j["serial"])
                try:
                    j["name"] = str(it.Name or "") if it is not None else ""
                except Exception:
                    pass
            return who == j["name"].strip().lower() or ln.text.startswith("[")

        def job_result(j, a):
            """What the journal said since the attempt: "busy", "ok", "fail",
            "skip" or None."""
            rd = j["reader"]
            if rd is None:
                return None
            lines, raw = j["lines"], j["raw"]
            came = False
            for ln in rd.new():
                if ln.text and not ln.text.startswith(TITLE):
                    if settings["say"]:                    # the shard's actual texts, for the match lists
                        API.SysMsg("%s: reply: %s (from %s, %s)" % (TITLE, ln.text, ln.name or "nobody",
                                                                  ln.kind or "?"), Kit.HUE_INFO)
                    if not is_answer(j, ln):               # 2.6.81: not another's speech or line
                        continue
                    lines.append(ln.low)
                    came = True
                    raw.append((ln.text, ln.name or ""))   # as said, for the results (2.6.05)
                    if len(lines) > 40:                    # a cap: a chatty fight while we wait
                        del lines[:-40]
                        del raw[:-40]
            if not lines:
                return None
            if not came:                                   # 2.6.82: no new line: the same answer as last time
                return j.get("res")
            res = None
            for rs, words in (("busy", BUSY_WORDS), ("skip", a[8]), ("ok", a[6]), ("fail", a[7])):
                for w in words:
                    for k in range(len(lines)):
                        if w in lines[k]:
                            j["match"] = lines[k]          # the line that decided it (the window shows it)
                            j["match_raw"] = raw[k][0]
                            res = rs
                            break
                    if res is not None:
                        break
                if res is not None:
                    break
            j["res"] = res
            return res

        def finish_job(j, r, res, now):
            i, serial = j["rule"], j["serial"]
            key = (i, serial)
            nxt = None
            floor = skill_floor(r) if res == "busy" else 0.0
            if floor > 0 and "must wait" in (j.get("match") or ""):
                # 2.6.81: the skill's timer still runs: wait it out, not counted
                # (tool and use rules keep the counted retry below)
                st["later"][key] = now + floor
                nxt = now + min(r["delay"], floor)
            elif res == "busy":
                n = st["busy_n"].get(key, 0) + 1
                if n >= MAX_BUSY:
                    st["busy_n"].pop(key, None)
                    mark_done(r, serial, 2)
                    add_result(r, serial, 2, j["name"], answer_of(j) or "no answer from the shard",
                               "no answer")
                    API.SysMsg("%s: giving up on 0x%08X (no answer from %s)." %
                               (TITLE, serial, rule_action(r)[1]), Kit.HUE_BAD)
                else:
                    st["busy_n"][key] = n
                    st["later"][key] = now + BUSY_RETRY
            elif res == "fail":
                st["busy_n"].pop(key, None)
                tries = r.setdefault("_tries", {})
                n = tries.get(serial, 0) + 1
                if n <= settings["retries"]:
                    tries[serial] = n
                    st["later"][key] = now + max(r["delay"], 1.0)
                else:
                    tries.pop(serial, None)
                    mark_done(r, serial, 2)
                    add_result(r, serial, 2, j["name"], answer_of(j))
            else:
                st["busy_n"].pop(key, None)
                code = {"ok": 1, "skip": 3}.get(res, 4)
                mark_done(r, serial, code)
                add_result(r, serial, code, j["name"], answer_of(j))
            st["job"] = None
            # the rule's delay runs from the attempt (the recover wait is part of it);
            # a "busy" answer gets the whole delay again
            waited = max(0.0, now - j.get("t", now))
            st["next_scan"] = nxt if nxt is not None else now + (
                r["delay"] if res == "busy" else max(MIN_DELAY, r["delay"] - waited))
            st["status"] = "%s: %s" % (rule_action(r)[1], res or "done")
            # the shard's last answer to this rule, for the window's second line
            if j.get("match"):
                r["_last"] = "%s: %s" % (res, j["match"])
            elif j["lines"]:
                r["_last"] = "%s, no phrase matched; the shard said: %s" % (res or "no answer",
                                                                          j["lines"][-1])
            else:
                r["_last"] = "%s, no journal line in %.1f s" % (res or "no answer",
                                                              max(0.0, now - j.get("t", now)))
            if len(st["later"]) > 400:                   # a cap, like every growing dict
                for k in [k for k, t in st["later"].items() if t < now]:
                    st["later"].pop(k, None)
            if len(st["busy_n"]) > 400:
                st["busy_n"].clear()
            if len(r.get("_tries", {})) > MAX_DONE:
                r["_tries"].clear()

        def job_step(now):
            j = st["job"]
            r = rules[j["rule"]] if j["rule"] < len(rules) else None
            if r is None:
                HOST.release_cursor(KEY)
                st["job"] = None
                return
            a = rule_action(r)
            if j["phase"] == "target":
                res = job_result(j, a)
                if res:                                    # answered before any cursor
                    HOST.release_cursor(KEY)
                    finish_job(j, r, res, now)
                    return
                # (2.6.84) only the skill's own kind of cursor (neutral): a spell
                # the player casts meanwhile is never aimed at the bag item
                if HOST.cursor_ok(KEY, "neutral"):
                    API.Target(j["serial"])
                    HOST.release_cursor(KEY)
                    j["phase"], j["t"] = "recover", now
                elif HOST.cursor_busy(KEY) is None and API.HasTarget("any"):
                    HOST.release_cursor(KEY)               # someone's spell cursor: left alone
                    finish_job(j, r, "busy", now)
                elif now - j["t"] > TARGET_TIMEOUT:
                    HOST.release_cursor(KEY)
                    finish_job(j, r, "busy", now)
                return
            # recover: give the server the rule's delay to answer, then move on
            if now - j["t"] < max(r["delay"], MIN_DELAY):
                res = job_result(j, a)
                if res in ("busy", "skip", "fail"):
                    finish_job(j, r, res, now)
                return
            finish_job(j, r, job_result(j, a), now)

        def guard_check():
            """2.6.05: does a guard zone pause the rules? 2.6.81: HOST.guard_hold():
            "guard" in one, "unknown" while the zone isn't known yet (the strict
            reading: that pauses too), None out of one. Said once in the journal
            when it starts and ends while a rule is at work; with no rule at work
            nothing is asked."""
            active = bool(st["run"]) and not st["paused"]
            if not active and not st["paused"]:
                for r in rules:
                    if r["auto"] and r["bag"]:
                        active = True
                        break
            hold = None
            # (2.6.71) the town override counts only while Training Alarm is on (you
            # are answering its at-keyboard alarms): the shard's rules. 2.6.81: it
            # covers an unknown zone too (you chose to run in town with the alarm on)
            if active and (settings["guard"] or "attention.up" not in HOST.services):
                try:
                    hold = HOST.guard_hold()
                except Exception:
                    hold = None
            if hold != st["guard_paused"]:
                st["guard_paused"] = hold
                if active:
                    if hold == "guard":
                        msg = ("%s: paused in a guard zone (no skill use in towns); it goes on when "
                               "you leave." % TITLE)
                    elif hold == "unknown":
                        msg = ("%s: paused until the guard zone is known; cross a town's guard "
                               "line once." % TITLE)
                    else:
                        msg = "%s: out of the guard zone; going on." % TITLE
                    API.SysMsg(msg, Kit.HUE_INFO)

        IDLE_LOOK = 1.5                       # s between the idle status's fight tests; under
                                              # HURT_FRESH (2 s), so the shared HP watch stays fresh (2.6.83)

        def run_jobs(now):
            if st["job"] is not None:
                job_step(now)
                return
            if now < st["next_scan"]:
                return
            guard_check()
            if not st["run"] and not any(r["auto"] and r["bag"] for r in rules):
                # 2.6.82: no rule can run: nothing will be used, so the status's
                # fight test is looked at every IDLE_LOOK s (the same words), not
                # every scan; a rule that can run gets the full test every scan
                st["next_scan"] = now + SCAN_EVERY
                if now >= st["idle_at"]:
                    st["idle_at"] = now + IDLE_LOOK
                    st["status"] = blocked(now) or "Idle"
                return
            st["idle_at"] = 0.0
            why = blocked(now)
            if why:
                st["status"] = why
                st["next_scan"] = now + SCAN_EVERY
                return
            nxt = pick_next(now)
            if nxt is None:
                st["status"] = "Watching" if any(r["auto"] and r["bag"] for r in rules) else "Idle"
                st["next_scan"] = now + SCAN_EVERY
                return
            i, r, serial, it = nxt
            if start_job(i, r, serial, it, now):
                st["status"] = "%s %d/%d" % (rule_action(r)[1], r["_count"][0] + 1, r["_count"][1])
            else:
                st["next_scan"] = now + SCAN_EVERY

        # ---------- bag picking ----------
        def pick_bag(i):
            if st["pick"] is not None:
                API.SysMsg("%s: already targeting a bag." % TITLE, Kit.HUE_INFO)
                return
            st["pick"] = i
            API.SysMsg("%s: target the bag for rule %d." % (TITLE, i + 1), Kit.HUE_INFO)

            def done(serial):
                st["queue"].append(("picked", i, int(serial or 0)))
            HOST.pick_target(20, done)

        def bag_picked(i, serial):
            st["pick"] = None
            if i >= len(rules):
                return
            if not serial:
                API.SysMsg("%s: cancelled." % TITLE, Kit.HUE_INFO)
                return
            it = get_item(serial)
            ok = False
            try:
                ok = bool(it is not None and it.IsContainer)
            except Exception:
                ok = False
            if not ok:
                API.SysMsg("%s: that isn't a container." % TITLE, Kit.HUE_BAD)
                return
            r = rules[i]
            if r["bag"] != serial:
                r["bag"] = serial
                r["done"].clear()
                del r["order"][:]
                st["later"].clear()
                invalidate(r)
                clear_results(r)                   # 2.6.05: they were the old bag's
            save_settings()
            API.SysMsg("%s: rule %d uses %s." % (TITLE, i + 1, bag_name(r, False)), Kit.HUE_GOOD)
            st["redraw"] = True
            HOST.refresh_settings(KEY)

        # ---------- window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)

        def window_h():
            M = Kit.MARGIN
            return M + 30 + Kit.GAP + 40 + Kit.GAP + 30 + max(1, len(rules)) * ROW_H + 8 + M

        def build_window():
            w, h = (MINI_W, MINI_H) if st["minimized"] else (W, window_h())
            x, y = Kit.load_pos(POS_KEY, (200, 200), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            M = Kit.MARGIN
            store = ({}, {})
            c = {}
            rows = []
            g = G.CreateGump(True, True)
            if st["minimized"]:
                c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
            else:
                IW = w - 2 * M
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                # control strip: Pause / Resume, Add rule, status
                yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, 40)
                c["pause"] = Kit.art_button(g, store, "pause", Kit.ART_PLAY, M + 12, yb + 9,
                                            "Resume" if st["paused"] else "Pause",
                                            "Stop every rule for now, or start them again",
                                            on_click=queue("pause"))
                x_add = M + 12 + 35 + Kit.text_w("Resume") + 14
                Kit.art_button(g, store, "add", Kit.ART_OK, x_add, yb + 9, "Add rule",
                               "Add a rule (a bag and an action); it is set up on the settings page",
                               on_click=queue("add"))
                x_st = x_add + 35 + Kit.text_w("Add rule") + 14
                c["status"] = Kit.add_label(g, "", x_st, yb + 12, Kit.HUE_INFO)
                c["status_w"] = M + IW - 4 - x_st      # 2.6.81: a long status is cut to the strip
                st["full_txt"] = None
                # the rules
                yr = yb + 40 + Kit.GAP
                Kit.add_section(g, M, yr, IW, 30 + max(1, len(rules)) * ROW_H + 8,
                                "RULES  (a bag and an action each)")
                y0 = yr + 30
                x_reset = M + IW - 12 - 35 - Kit.text_w("Reset")
                x_run = x_reset - 35 - Kit.text_w("Run") - 6
                x_bag = x_run - 35 - Kit.text_w("Bag...") - 6       # ("..." : a target cursor follows)
                x_res = x_bag - 35 - Kit.text_w("Results") - 6      # 2.6.05
                c["last_w"] = IW - 36 - 16            # the "Last:" line runs the row's width
                if not rules:
                    Kit.add_label(g, "No rules yet. Click Add rule, then set its bag and action.",
                                  M + 12, y0 + 5, Kit.HUE_INFO)
                for i, r in enumerate(rules):
                    ry = y0 + i * ROW_H
                    row = {}
                    row["auto"] = Kit.add_check(g, "", M + 10, ry + 2, r["auto"],
                                                "Watch this bag and handle every new item that lands in it")
                    row["bag"] = Kit.add_label(g, "", M + 36, ry + 3, Kit.HUE_TEXT)
                    row["act"] = Kit.add_label(g, "", M + 172, ry + 3, Kit.HUE_TITLE)
                    row["prog"] = Kit.add_label(g, "", M + 298, ry + 3, Kit.HUE_INFO)
                    # the shard's last answer to this rule (what the OK / FAIL / SKIP words matched)
                    row["last"] = Kit.add_label(g, "", M + 36, ry + 22, Kit.HUE_INFO)
                    safe(lambda: row["last"].SetTooltip(
                        "The shard's last answer to this rule and how it was read (ok, fail, skip or "
                        "busy). The DEBUG box on the settings page prints every line the shard says."))
                    Kit.art_button(g, store, "res%d" % i, Kit.ART_PAGE, x_res, ry + 1, "Results",
                                   "Open this rule's results: the shard's answer to each item, with "
                                   "counts and an export (again: close)", on_click=queue(("results", i)))
                    Kit.art_button(g, store, "bag%d" % i, Kit.ART_PLAY, x_bag, ry + 1, "Bag...",
                                   "Target the bag this rule works on", on_click=queue(("bag", i)))
                    Kit.art_button(g, store, "run%d" % i, Kit.ART_PLAY, x_run, ry + 1, "Run",
                                   "One pass over the bag now (the items not done yet)",
                                   on_click=queue(("run", i)))
                    Kit.art_button(g, store, "reset%d" % i, Kit.ART_CLOSE, x_reset, ry + 1, "Reset",
                                   "Forget what was done in this bag, so every item is handled again",
                                   on_click=queue(("reset", i)))
                    row["text"] = (None, None, None, None)
                    rows.append(row)
            Kit.place(g, x, y, w, h)                     # wholly on screen (the window rules)
            win.update({"g": g, "c": c, "store": store, "rows": rows})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, lambda: Kit.save_pos(POS_KEY, win["g"])))
            if st["minimized"] and st["docked"]:
                safe(lambda: setattr(g, "IsVisible", False))
            st["rows"] = len(rules)
            st["redraw"] = False
            refresh()
            Kit.dispose(old)

        fit = Kit.fit                 # text cut to a width (letter sums: no label per step)

        def refresh():
            if st["minimized"] and st["docked"]:
                return
            lbl = win["c"].get("status")
            if lbl is not None:
                hue = Kit.HUE_BAD if st["paused"] else (Kit.HUE_GOOD if st["job"] else Kit.HUE_INFO)
                if st["minimized"]:                        # the minimized bar: "<Title>: <status>"
                    mt = st.get("mini_txt")                # (fitted once per status, not per tick)
                    if mt is None or mt[0] != st["status"]:
                        mt = (st["status"], fit("%s: %s" % (TITLE, st["status"]), MINI_W - 90))
                        st["mini_txt"] = mt
                    Kit.set_text(lbl, mt[1], hue)
                else:
                    ft = st.get("full_txt")                # 2.6.81: fitted once per status too
                    if ft is None or ft[0] != st["status"]:
                        ft = (st["status"], fit(st["status"], win["c"].get("status_w", 400)))
                        st["full_txt"] = ft
                    Kit.set_text(lbl, ft[1], hue)
            if st["minimized"]:
                return
            now = time.time()
            if now < st["next_rows"]:
                return
            st["next_rows"] = now + CHECK_EVERY
            for i, row in enumerate(win["rows"]):
                if i >= len(rules):
                    break
                r = rules[i]
                cnt = r.get("_count")
                prog = "%d/%d" % cnt if cnt else ""
                if st["job"] and st["job"]["rule"] == i:
                    prog += "  working"
                elif i in st["run"]:
                    prog += "  pass"
                last = r.get("_last") or ""
                t = (bag_name(r), rule_action(r)[1], prog, last)
                if t != row["text"]:
                    row["text"] = t
                    Kit.set_text(row["bag"], fit(t[0], 130))
                    Kit.set_text(row["act"], fit(t[1], 120))
                    Kit.set_text(row["prog"], fit(t[2], 96))
                    Kit.set_text(row["last"], fit("Last: " + last if last else
                                                  "Last: no answer read yet",
                                                  win["c"].get("last_w", 500)))

        def read_checks():
            """The Auto boxes of the window, a few times a second."""
            changed = False
            for i, row in enumerate(win["rows"]):
                if i >= len(rules):
                    break
                try:
                    v = bool(row["auto"].IsChecked)
                except Exception:
                    continue
                if v != rules[i]["auto"]:
                    rules[i]["auto"] = v
                    changed = True
            if changed:
                save_settings()
                HOST.refresh_settings(KEY)

        # ---------- 2.6.05: the Results window (one rule's results, newest first) ----------
        RES_NAME_W, RES_TAG_W = 230, 120      # columns: "time  item", the result word, then the answer

        def rule_index(r):
            """The rule's place in the list (by identity), or -1 once removed."""
            for k in range(len(rules)):
                if rules[k] is r:
                    return k
            return -1

        def save_res_pos():
            Kit.save_pos(RES_POS_KEY, resw["g"])

        def on_res_disposed(g):
            def handler(*args):
                if resw["g"] is g:
                    resw["g"], resw["rows"], resw["rule"] = None, [], None
            return handler

        def close_results():
            g = resw["g"]
            if g is not None:
                save_res_pos()
            resw.update({"g": None, "rows": [], "rule": None, "c": {}})
            Kit.dispose(g)

        def show_results(i):
            """The rule's Results button: opens the window on that rule, switches
            an open one to it, or closes it when it already shows that rule."""
            if i >= len(rules):
                return
            r = rules[i]
            if resw["rule"] is r and Kit.is_open(resw["g"]):
                close_results()
                return
            resw["rule"], resw["page"] = r, 0
            if Kit.is_open(resw["g"]):
                resw["dirty"] = True              # same window, another rule: rows rewritten
            else:
                build_results()

        def build_results():
            M = Kit.MARGIN
            w = RES_W
            IW = w - 2 * M
            sh = 30 + 24 + RES_ROWS * RES_ROW_H + 8
            h = M + 30 + Kit.GAP + sh + M
            x, y = Kit.load_pos(RES_POS_KEY, (260, 220), (w, h))     # saved place, on today's screen
            old = resw["g"]
            if Kit.is_open(old):
                x, y = old.GetX(), old.GetY()
            resw["g"] = None
            store = ({}, {})
            c = {}
            g = G.CreateGump(True, True)
            Kit.add_window_frame(g, w, h)
            Kit.add_section(g, M, M, IW, 30)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close",
                           on_click=queue("res_close"))
            x_exp = w - M - 54 - 12 - 35 - Kit.text_w("Export")
            Kit.art_button(g, store, "export", Kit.ART_OK, x_exp, M + 4, "Export",
                           "Write this rule's results to a text file next to Virtue Assistant",
                           on_click=queue("res_export"))
            x_clr = x_exp - 12 - 35 - Kit.text_w("Clear")
            Kit.art_button(g, store, "clear", Kit.ART_CLOSE, x_clr, M + 4, "Clear",
                           "Forget this rule's results (the items stay done; Reset in the Skill Bags "
                           "window handles them again)", on_click=queue("res_clear"))
            c["title"] = Kit.add_label(g, "", M + 30, M + 7, Kit.HUE_TITLE)
            c["title_w"] = x_clr - (M + 30) - 8
            ys = M + 30 + Kit.GAP
            Kit.add_section(g, M, ys, IW, sh, "RESULTS  (newest first)")
            x_old = M + IW - 12 - 35 - Kit.text_w("Next")
            Kit.art_button(g, store, "older", Kit.ART_PAGE, x_old, ys + 24, "Next",
                           "Next page (older results)", on_click=queue("res_older"))
            x_new = x_old - 10 - 35 - Kit.text_w("Prev")
            Kit.art_button(g, store, "newer", Kit.ART_PAGE, x_new, ys + 24, "Prev",
                           "Previous page (newer results)", on_click=queue("res_newer"))
            c["page_x"], c["page_y"] = x_new - 8, ys + 28   # "page 2 of 3", right-aligned to Prev
            c["page"] = Kit.add_label(g, "", c["page_x"], ys + 28, Kit.HUE_INFO)
            c["counts"] = Kit.add_label(g, "", M + 12, ys + 28, Kit.HUE_TEXT)
            c["counts_w"] = x_new - (M + 12) - 16 - Kit.text_w("page 99 of 99")
            c["ans_w"] = IW - 12 - RES_NAME_W - RES_TAG_W - 8
            rows = []
            y0 = ys + 30 + 24
            for k in range(RES_ROWS):
                ry = y0 + k * RES_ROW_H
                rows.append({"name": Kit.add_label(g, "", M + 12, ry, Kit.HUE_TEXT),
                             "tag": Kit.add_label(g, "", M + 12 + RES_NAME_W, ry, Kit.HUE_INFO),
                             "ans": Kit.add_label(g, "", M + 12 + RES_NAME_W + RES_TAG_W, ry, Kit.HUE_INFO),
                             "tip": None})
            Kit.place(g, x, y, w, h)                              # wholly on screen (the window rules)
            resw.update({"g": g, "c": c, "rows": rows, "store": store})
            G.AddControlOnDisposed(g, on_res_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_res_pos))           # saved the moment you let go of it
            refresh_results()
            Kit.dispose(old)

        RES_HUE = {1: Kit.HUE_GOOD, 2: Kit.HUE_BAD, 3: Kit.HUE_INFO, 4: Kit.HUE_TEXT}

        def refresh_results():
            """Rewrites the window's rows (only when the results, the rule or the
            page changed: resw["dirty"])."""
            resw["dirty"] = False
            r, rows = resw["rule"], resw["rows"]
            if not rows or r is None:
                return
            i = rule_index(r)
            if i < 0:                                             # the rule was removed
                close_results()
                return
            c = resw["c"]
            res = r.get("_res") or []
            n = len(res)
            pages = max(1, (n + RES_ROWS - 1) // RES_ROWS)
            pg = resw["page"] = max(0, min(resw["page"], pages - 1))
            Kit.set_text(c["title"], fit("RULE %d RESULTS: %s" % (i + 1, rule_action(r)[1]), c["title_w"]))
            Kit.set_text(c["counts"], fit(counts_text(r), c["counts_w"]))
            ptxt = "page %d of %d" % (pg + 1, pages) if pages > 1 else ""
            if Kit.set_text(c["page"], ptxt) and ptxt:      # right-aligned: moved when its text changes
                tw = Kit.text_w(ptxt)
                try:
                    Kit.ui_pos(c["page"], c["page_x"] - tw, c["page_y"])
                except Exception:
                    pass
            top = n - 1 - pg * RES_ROWS
            today = time.localtime()[:3]
            for k, row in enumerate(rows):
                idx = top - k
                if idx >= 0:
                    t, serial, name, code, tag, answer = res[idx]
                    lt = time.localtime(t)
                    when = time.strftime("%H:%M" if lt[:3] == today else "%b %d %H:%M", lt)
                    Kit.set_text(row["name"], fit("%s  %s" % (when, name), RES_NAME_W - 8))
                    hue = Kit.HUE_TITLE if tag == "magic" else RES_HUE.get(code, Kit.HUE_INFO)
                    Kit.set_text(row["tag"], fit(tag, RES_TAG_W - 8), hue)
                    Kit.set_text(row["ans"], fit(answer or "no answer", c["ans_w"]))
                    if row["tip"] != answer:                      # the whole answer, when it is cut
                        row["tip"] = answer
                        try:
                            row["ans"].SetTooltip(answer or "")
                        except Exception:
                            pass
                else:
                    Kit.set_text(row["name"], "")
                    Kit.set_text(row["tag"], "")
                    Kit.set_text(row["ans"], "")

        def export_results():
            """The shown rule's results as a text file next to Virtue Assistant
            (oldest first); written by thread_tick, never on the client thread."""
            r = resw["rule"]
            i = rule_index(r) if r is not None else -1
            if i < 0:
                return
            res = r.get("_res") or []
            if not res:
                API.SysMsg("%s: rule %d has no results to export yet." % (TITLE, i + 1), Kit.HUE_INFO)
                return
            serial = 0
            try:
                serial = int(API.Player.Serial)
            except Exception:
                pass
            path = os.path.join(str(API.ScriptPath), EXPORT_NAME % (serial, i + 1))
            lines = ["Skill Bags results - rule %d: %s on %s" % (i + 1, rule_action(r)[1], bag_name(r, False)),
                     "Exported %s - %s" % (time.strftime("%Y-%m-%d %H:%M"), counts_text(r)),
                     "",
                     "%-19s  %-10s  %-32s  %-18s  %s" % ("Time", "Serial", "Item", "Result",
                                                        "The shard's answer")]
            for t, s, name, code, tag, answer in res:
                lines.append("%-19s  0x%08X  %-32s  %-18s  %s" % (
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)), s, name, tag, answer))
            st["writes"].append((path, "\n".join(lines) + "\n"))

        def write_files():
            """thread_tick: write the exports export_results() prepared (returns
            at once when there are none)."""
            while st["writes"]:
                path, text = st["writes"].pop(0)
                try:
                    with open(path, "w") as fh:
                        fh.write(text)
                    API.SysMsg("%s: results written to %s." % (TITLE, path), Kit.HUE_GOOD)
                except Exception as ex:
                    API.SysMsg("%s: couldn't write %s (%s)." % (TITLE, path, ex), Kit.HUE_BAD)

        # ---------- settings page (drawn inside the Virtue Assistant window) ----------
        SEC_G0, SEC_R, SEC_D = 118, 118, 66   # the general section grows by the hint's lines; DEBUG last
        HINT = ("The OK / FAIL / SKIP phrases that read the shard's answers are RunUO defaults, not "
                "checked on this shard: the DEBUG box at the bottom prints what the shard really "
                "says, and the window's Last line shows each rule's last answer.")
        TIP_TEXT = ("For Graphics in Text: the item graphics in hex, commas between them (0x14FC, "
                    "0x0E76). For Name contains Text: part of the item's name (treasure map)")
        TIP_CUSTOM = ("Custom skill: the skill's name as the client spells it (Item Identification). "
                      "Custom tool: the tool's graphic in hex (0x14FC: lockpicks). "
                      "Nothing for the other actions.")
        TIP_DELAY = ("Seconds between two items of this rule (%g-%g; a skill rule waits at least its "
                     "skill timer, 3 or 10 s)" % (MIN_DELAY, MAX_DELAY))
        TIP_DEEP = "Also handle the items inside bags that sit in this bag"
        TIP_AUTO = "Watch the bag and handle every new item that lands in it (the window's box too)"

        def hint_lines(w):
            return Kit.wrap(HINT, w - 24) or [HINT]

        def sec_g(w):
            return SEC_G0 + 18 * len(hint_lines(w))

        def config_height(w):
            return sec_g(w) + len(rules) * (Kit.GAP + SEC_R) + Kit.GAP + SEC_D

        def tipped(ctrl, tip):
            safe(lambda: ctrl.SetTooltip(tip))
            return ctrl

        def build_config(g, x, y, w):
            store = ({}, {})
            c = {}
            prow = []
            dds = []
            hint = hint_lines(w)
            SEC_G = sec_g(w)
            Kit.add_section(g, x, y, w, SEC_G, "OPTIONS")
            c["hidden"] = Kit.add_check(g, "Pause while hidden", x + 12, y + 30, settings["hidden"],
                                        "Using a skill would reveal you")
            c["open"] = Kit.add_check(g, "Open a bag the client hasn't looked inside yet", x + 12,
                                      y + 56, settings["open"],
                                      "Double-click the bag once so its contents are known")
            Kit.art_button(g, store, "add", Kit.ART_OK, x + 400, y + 54, "Add rule",
                           "Add a rule (a bag and an action)", on_click=queue("add"))
            tip = "Times the item is tried again after a failed attempt, the FAIL phrase (0-9)"
            tipped(Kit.add_label(g, "Extra tries after a failure:", x + 12, y + 88), tip)
            c["retries"] = tipped(Kit.add_textbox(g, str(settings["retries"]), x + 290, y + 84, 40), tip)
            c["guard"] = Kit.add_check(g, "Pause in guard zones", x + 380, y + 86, settings["guard"],
                                       "No skill use in towns or before the zone is known; unticked counts "
                                       "only while Skills > Training Alarm is on")
            for k, line in enumerate(hint):
                Kit.add_label(g, line, x + 12, y + 112 + 18 * k, Kit.HUE_INFO)
            yr = y + SEC_G
            for i, r in enumerate(rules):
                yr += Kit.GAP
                Kit.add_section(g, x, yr, w, SEC_R, "RULE %d  (%s)" % (i + 1, fit(bag_name(r, False), 300)))
                row = {}
                Kit.add_label(g, "Action:", x + 12, yr + 34)
                dds.append(("action", i, x + 70, yr + 30, 210, ACTION_NAMES, r["action"]))
                tipped(Kit.add_label(g, "Custom:", x + 296, yr + 34), TIP_CUSTOM)
                row["custom"] = tipped(Kit.add_textbox(g, r["custom"], x + 356, yr + 30, 130,
                                                       numbers=False), TIP_CUSTOM)
                x_rm = x + w - 12 - 35 - Kit.text_w("Remove")
                Kit.art_button(g, store, "rm%d" % i, Kit.ART_CLOSE, x_rm, yr + 28, "Remove",
                               "Remove this rule", on_click=queue(("remove", i)))
                Kit.add_label(g, "Items:", x + 12, yr + 62)
                dds.append(("filt", i, x + 70, yr + 58, 210, FILTER_NAMES, r["filt"]))
                tipped(Kit.add_label(g, "Text:", x + 296, yr + 62), TIP_TEXT)
                row["text"] = tipped(Kit.add_textbox(g, r["text"], x + 356, yr + 58, w - 356 - 16,
                                                     numbers=False), TIP_TEXT)
                tipped(Kit.add_label(g, "Delay (s):", x + 12, yr + 90), TIP_DELAY)
                row["delay"] = tipped(Kit.add_textbox(g, "%g" % r["delay"], x + 90, yr + 86, 50,
                                                      numbers=False), TIP_DELAY)
                row["deep"] = Kit.add_check(g, "Look inside bags within the bag", x + 160, yr + 88,
                                            r["deep"], TIP_DEEP)
                row["auto"] = Kit.add_check(g, "Auto (watch the bag)", x + 420, yr + 88, r["auto"],
                                            TIP_AUTO)
                prow.append(row)
                yr += SEC_R
            yd = yr + Kit.GAP
            Kit.add_section(g, x, yd, w, SEC_D, "DEBUG  (for checking the shard's texts)")
            c["say"] = Kit.add_check(g, "Print the shard's replies in the journal", x + 12, yd + 32,
                                     settings["say"],
                                     "While an answer is awaited, every journal line seen is printed "
                                     "as \"%s: reply: ...\", to compare with the OK / FAIL / SKIP "
                                     "phrases" % TITLE)
            # drop-downs last, lowest first, so an open list draws over what is below it
            for kind, i, dx, dy, dw, items, idx in sorted(dds, key=lambda d: -d[3]):
                try:
                    dd = G.CreateDropDown(dw, list(items), int(idx))
                    dd.SetPos(dx, dy)
                    g.Add(dd)
                    prow[i][kind] = dd
                except Exception:
                    prow[i][kind] = None
                    Kit.add_label(g, items[idx], dx, dy + 4, Kit.HUE_INFO)
            page.update({"c": c, "store": store, "rows": prow, "next_read": 0.0})

        def poll_config():
            c = page["c"]
            if c is None:
                return
            now = time.time()
            if now < page["next_read"]:
                return
            page["next_read"] = now + CHECK_EVERY
            changed = False
            relist = []                          # 2.6.81: the rules whose bag must be listed again
            auto_moved = []                      # 2.6.81: the rules whose Auto changed here
            try:
                for k in ("hidden", "open", "say", "guard"):   # (2.6.71) war mode always pauses
                    v = bool(c[k].IsChecked)
                    if v != settings[k]:
                        settings[k] = v
                        changed = True
                t = str(c["retries"].Text or "").strip()
                if t.isdigit() and 0 <= int(t) <= 9 and int(t) != settings["retries"]:
                    settings["retries"] = int(t)
                    changed = True
                for i, row in enumerate(page["rows"]):
                    if i >= len(rules):
                        break
                    r = rules[i]
                    act_new = False                        # 2.6.81: the action changed this pass
                    for kind, names in (("action", ACTIONS), ("filt", FILTERS)):
                        dd = row.get(kind)
                        if dd is None:
                            continue
                        idx = safe(lambda: int(dd.GetSelectedIndex()), r[kind])
                        if 0 <= idx < len(names) and idx != r[kind]:
                            r[kind] = idx
                            changed = True
                            relist.append(r)
                            if kind == "action":           # a new action: its own defaults
                                act_new = True
                                r["filt"] = ACTIONS[idx][5]
                                r["delay"] = ACTIONS[idx][4]
                                r["done"].clear()
                                del r["order"][:]
                                clear_results(r)           # 2.6.05: they were the old action's
                                page["dirty"] = True       # the page is redrawn with them
                                break
                    for k in ("custom", "text"):
                        v = str(row[k].Text or "").strip()
                        if v != r[k]:
                            r[k] = v
                            changed = True
                            relist.append(r)
                    if not act_new:                        # 2.6.81: the box still shows the old delay
                        d = clamp_delay(str(row["delay"].Text or "").strip(), r["delay"])
                        d = max(d, skill_floor(r))         # 2.6.81: never under the skill's timer
                        if abs(d - r["delay"]) > 0.001:
                            r["delay"] = d
                            changed = True
                    for k in ("deep", "auto"):
                        v = bool(row[k].IsChecked)
                        if v != r[k]:
                            r[k] = v
                            changed = True
                            (relist if k == "deep" else auto_moved).append(r)
            except Exception as ex:
                page["c"] = None
                API.SysMsg("%s: settings page error: %s (reopen the page)." % (TITLE, ex), Kit.HUE_BAD)
                return
            if changed:
                save_settings()
                # 2.6.81: only the rules whose listing changed are listed again, and
                # the window isn't rebuilt: its rows follow in refresh(); an Auto
                # change ticks the window's box (read_checks would undo it)
                for r in relist:
                    invalidate(r)
                for r in auto_moved:
                    i = rule_index(r)
                    if 0 <= i < len(win["rows"]):
                        try:
                            win["rows"][i]["auto"].IsChecked = r["auto"]
                        except Exception:
                            st["redraw"] = True
                if page.get("dirty"):
                    page["dirty"] = False
                    HOST.refresh_settings(KEY)

        def config_closed():
            page["c"] = None
            page["rows"] = []

        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "paused": False,
                       "job": None, "next_scan": 0.0, "next_check": 0.0, "status": "Idle",
                       "run": set(), "opening": {}, "later": {}, "pick": None, "redraw": False,
                       "save_done": False, "no_tool": {}, "busy_n": {}, "next_rows": 0.0,
                       "rr": 0, "guard_paused": None, "writes": [],
                       "idle_at": 0.0, "done_at": 0.0,   # 2.6.82: idle status look; done marks saved
                       "minimized": bool(safe(lambda: HOST.dock_wanted(KEY), False))
                       or Kit.load_min(MIN_KEY)})
            resw.update({"g": None, "rule": None, "c": {}, "rows": [], "page": 0, "dirty": False})
            load_settings()
            build_window()
            HOST.dock_add(KEY, _scaled_hooks(TITLE, TRAY_ICON, st, win, queue("redraw")))
            n = sum(1 for r in rules if r["auto"] and r["bag"])
            API.SysMsg("%s: on, %d rule%s, %d watching." % (TITLE, len(rules),
                                                            "" if len(rules) == 1 else "s", n),
                       Kit.HUE_GOOD)

        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])            # on_disposed turns the module off
                return
            now = time.time()
            while st["queue"]:
                action = st["queue"].pop(0)
                kind = action[0] if isinstance(action, tuple) else action
                if action == "settings":
                    HOST.show_settings(KEY)
                elif action == "toggle_min":
                    st["minimized"] = not st["minimized"]
                    st["docked"] = False
                    Kit.save_min(MIN_KEY, st["minimized"])   # remembered per character
                    HOST.dock_forget(KEY)
                    build_window()
                elif action == "to_bar":
                    HOST.dock_to_bar(KEY, TITLE)
                elif action == "redraw":
                    build_window()
                elif action == "pause":
                    st["paused"] = not st["paused"]
                    st["idle_at"] = 0.0                      # 2.6.82: the status says so at once
                    if st["paused"] and st["job"] is not None:
                        HOST.release_cursor(KEY)
                        st["job"] = None
                    lbl = win["c"].get("pause")
                    if lbl is not None:
                        Kit.set_text(lbl, "Resume" if st["paused"] else "Pause")
                    API.SysMsg("%s: %s." % (TITLE, "paused" if st["paused"] else "resumed"),
                               Kit.HUE_INFO)
                elif action == "add":
                    if len(rules) >= MAX_RULES:
                        API.SysMsg("%s: at most %d rules." % (TITLE, MAX_RULES), Kit.HUE_INFO)
                    else:
                        rules.append(new_rule())
                        save_settings()
                        build_window()
                        HOST.refresh_settings(KEY)
                        if page["c"] is None:
                            HOST.show_settings(KEY)
                elif kind == "remove":
                    i = action[1]
                    if i < len(rules):
                        if st["job"] is not None and st["job"]["rule"] == i:
                            HOST.release_cursor(KEY)
                            st["job"] = None
                        elif st["job"] is not None and st["job"]["rule"] > i:
                            st["job"]["rule"] -= 1           # its rule moves up a place (its result with it)
                        gone = rules.pop(i)
                        if resw["rule"] is gone:             # its Results window goes with it
                            close_results()
                        elif resw["rule"] is not None:
                            resw["dirty"] = True             # another rule's: its number may change
                        st["rr"] = 0
                        st["run"] = set(k - 1 if k > i else k for k in st["run"] if k != i)
                        st["later"].clear()
                        st["busy_n"].clear()                 # keyed by rule index too
                        st["no_tool"].clear()
                        save_settings()
                        build_window()
                        HOST.refresh_settings(KEY)
                elif kind == "bag":
                    if action[1] < len(rules):
                        pick_bag(action[1])
                elif kind == "picked":
                    bag_picked(action[1], action[2])
                elif kind == "run":
                    i = action[1]
                    if i < len(rules):
                        if not rules[i]["bag"]:
                            API.SysMsg("%s: set the bag for rule %d first (Bag button)." % (TITLE, i + 1),
                                       Kit.HUE_BAD)
                        else:
                            st["run"].add(i)
                            st["later"].clear()
                            invalidate(rules[i])         # a Run pass starts from a fresh listing
                            st["next_scan"] = 0.0
                elif kind == "reset":
                    i = action[1]
                    if i < len(rules):
                        rules[i]["done"].clear()
                        del rules[i]["order"][:]
                        rules[i].pop("_tries", None)
                        rules[i].pop("_last", None)
                        invalidate(rules[i])
                        st["later"].clear()
                        save_done()
                        API.SysMsg("%s: rule %d will handle every item again (%s)." %
                                   (TITLE, i + 1, bag_name(rules[i])), Kit.HUE_INFO)
                elif kind == "results":                      # 2.6.05: the Results window
                    show_results(action[1])
                elif action == "res_close":
                    close_results()
                elif action == "res_export":
                    export_results()
                elif action == "res_clear":
                    if resw["rule"] is not None:
                        clear_results(resw["rule"])
                        resw["page"] = 0
                elif action in ("res_older", "res_newer"):
                    resw["page"] += 1 if action == "res_older" else -1
                    resw["dirty"] = True                     # refresh_results keeps it in range
            if st.get("redraw"):
                build_window()
            if resw["dirty"] and resw["g"] is not None:
                refresh_results()
            if not st["minimized"] and now >= st["next_check"]:
                st["next_check"] = now + CHECK_EVERY
                read_checks()
            run_jobs(now)
            if st.get("save_done") and now >= st["done_at"]:   # 2.6.82: one write per DONE_SAVE_EVERY s
                st["save_done"] = False
                st["done_at"] = now + DONE_SAVE_EVERY
                save_done()
            refresh()

        def _stop():
            st["shutting"] = True
            if st["job"] is not None:
                HOST.release_cursor(KEY)
                st["job"] = None
            HOST.dock_remove(KEY)
            Kit.save_pos(POS_KEY, win["g"])
            Kit.save_min(MIN_KEY, st["minimized"])
            save_settings()
            g, win["g"] = win["g"], None
            Kit.dispose(g)
            close_results()
            if st["writes"]:
                # an export asked for in the very last pass: written now, unless
                # this runs on the client thread (a disk write there is a hitch)
                if Client.on_client_thread():
                    API.SysMsg("%s: the export wasn't written (the module stopped); export again." % TITLE,
                               Kit.HUE_INFO)
                    del st["writes"][:]
                else:
                    write_files()

        DONE_SAVE_EVERY = 5.0                 # 2.6.82: s between saves of the done marks (and on stop)

        def _interval():
            # 2.6.82: fast only while the skill's cursor is awaited; the recover
            # wait (the rule's delay, seconds) reads the answer every 0.1 s
            j = st["job"]
            return 0.05 if j is not None and j["phase"] == "target" else 0.1

        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True,
                  "thread_tick": write_files,       # 2.6.05: the results Export is written here
                  "interval": _interval,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    # ---------- the parts, run side by side by the mother's PartSet ----------
    #  (part key, builder, tick interval, the 2.6.06 module key it keeps)
    PARTS = (
        ("window", _part_window, 0.25, "skills"),
        ("alarm", _part_alarm, 0.1, "attention"),
        ("bags", _part_bags, 0.1, "skillbags"),
    )
    MODULE = PartSet(KEY, TITLE, PARTS).hooks()
    return MODULE


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("skills", "Skills",
             "Your skills, training and what needs you at the keyboard",
             _module_skills, 0.1,
             category="Skills and home",
             parts=(
                 ("window", "Skills Window",
                  "A skills window with locks, groups, gains and targets", True, ("skills",)),
                 ("alarm", "Training Alarm",
                  "An alarm when staff or a gump need you; skill loops pause", False, ("attention",)),
                 ("bags", "Skill Bags",
                  "Uses a skill on every item in a bag, once each", False, ("skillbags",)),
             ),
             aliases=('Skill Bags', 'Attention', 'GM check', 'training', 'locks', 'gains', 'Item ID'))
else:
    import API
    API.SysMsg("Skills is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
