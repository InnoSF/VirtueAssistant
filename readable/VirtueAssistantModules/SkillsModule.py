# =============================================================================
# Skills: a Virtue Assistant module (TazUO Legion script, IronPython 3.4).
# Shard: In Mani Ylem.
#
# This file is not a script to run on its own. It is one module of Virtue Assistant: the mother
# script loads it from the modules folder beside it and runs it in its own namespace, so API, G,
# safe, Client, Kit, Typing, Tz, HOST, LAYOUT and the main loop all come from the mother. Run the
# mother script and tick Skills on its Modules tab. To leave the module out, take this file out
# of the folder.
#
# Module key: skills. Category: Skills and home.
#
# The module is made of parts, each with its own box under the module's row on the Modules tab
# and its own saved keys, window place and files. The mother's PartSet runs the ticked parts side
# by side. This file holds three of them:
#
#   Skills Window    replaces the client's skills window: locks, groups, session gains, targets
#   Training Alarm   an alarm when staff or a gump need you; skill loops pause
#   Skill Bags       uses a skill on every item in a bag, once each
#
# The Training Alarm starts before Skill Bags, which pauses while the alarm's attention.up service
# says an alarm waits for the player.
#
# Layout of this file: one builder function per module (_module_skills), one builder per part
# inside it (_part_window and the others), and each part is a closure over its own state tables
# (settings, st, win, SK, STATS, GR and so on). Nothing here blocks: the tick runs on the client
# thread and only the disk write of a skill sheet runs on the script thread.
# =============================================================================
def _module_skills():
    """Builds the Skills module from its parts and returns the hooks the mother script runs.

    The module key is skills. The parts are built one after another; the mother's PartSet ticks the
    ones the player has switched on.
    """
    KEY = "skills"
    TITLE = "Skills"

    def write_queue(q, title, what):
        """Writes every queued (path, text) pair to disk and says so in the journal. Script thread.

        The queue holds files prepared on the client thread: a disk write there would be a frame hitch.
        A failed write is reported with its error and does not stop the rest of the queue.
        """
        while q:
            path, text = q.pop(0)
            try:
                with open(path, "w") as fh:
                    fh.write(text)
                API.SysMsg("%s: %s written to %s." % (title, what, path), Kit.HUE_GOOD)
            except Exception as ex:
                API.SysMsg("%s: couldn't write %s (%s)." % (title, path, ex), Kit.HUE_BAD)

    def _part_window():
        """Builds the Skills Window part and returns its hooks (start, tick, stop, thread tick, settings page).

        The part replaces the client's skills window, standard scroll and advanced list alike, with one
        in the Virtue Assistant look: every skill with its real value, value with bonuses and cap, lock
        arrows, the use gem, floating skill buttons, the client's skill groups, session gains and rates,
        per-skill targets, stat targets, pins, lock sets, a training tip per range and a sheet export.
        Saved keys: Skills_settings, Skills_pos, Skills_marks, Skills_locksets, Skills_session and
        Skills_stat_targets.
        """
        # Names and saved keys. Every saved key starts with Skills_ so the part keeps the values it had
        # when it was a module of its own.
        KEY = "skills"
        TITLE = "Skills"
        SETTINGS_KEY = "Skills_settings"
        POS_KEY = "Skills_pos"
        MARKS_KEY = "Skills_marks"
        LOCKSETS_KEY = "Skills_locksets"
        SESSION_KEY = "Skills_session"
        # A session older than this many hours with no Virtue Assistant running starts afresh.
        SESSION_STALE_H = 6
        # The shard's total skill cap in tenths (700.0 points). The settings page lets the player change it.
        TOTAL_CAP_DEFAULT = 7000
        # The type names of the client's own skills windows (standard scroll and advanced list). These are
        # the ones closed when Replace is on.
        VANILLA = ("StandardSkillsGump", "SkillGumpAdvanced")
        # Art id of the Action Bar tray icon this window folds into.
        DOCK_ICON = 0x13E3
        ROW_H = 22
        SEARCH_W = 110
        BAR_W = 56
        # The progress bar is BAR_W wide at the window's natural width and grows by at most BAR_GROW when
        # the window is dragged wider.
        BAR_GROW = 120
        # Seconds without a corner-drag step before the layout is worked out again.
        RESIZE_SETTLE = 0.35
        MIN_IW = 380
        ZONE_NAME_MIN = 60
        # In a zone the columns give way in this order: progress bar, Gain, Cap, Real. The name column
        # takes the room left and is cut last.
        ZONE_DROPS = ("bar", "gain", "cap", "real")
        ZONE_FIELD_MIN = 80
        ZONE_MIN_ROWS = 2
        ZONE_LOG_MIN = 2
        # The tooltip of the Total line, shared by the one-line and two-line forms.
        TOTAL_TIP = "Real values added up, against the total cap (settings page)"
        LOCK_BTNS = (("all_up", "All up", "Set every listed skill to go up"),
                     ("all_down", "All down", "Set every listed skill to go down (click twice)"),
                     ("all_locked", "All locked", "Lock every listed skill"),
                     ("lock_capped", "Lock capped", "Lock every skill at its cap"))
        # Size of the minimized bar.
        MINI_W, MINI_H = 280, 46
        # The picked skill's buttons: art, caption, tooltip, queued action. The order here is not the order
        # on screen; the zone plan decides that and may put Pin beside the target box.
        DETAIL_BTNS = {"use": (Kit.ART_PLAY, "Use", "Use this skill", "use"),
                       "button": (Kit.ART_PAGE, "Make button", "Make its floating client button (or double-click "
                                  "it in the list)", "mkbutton"),
                       "pin": (Kit.ART_OK, "Pin", "Keep it at the top of the list (again to unpin)", "pin"),
                       "nextgrp": (Kit.ART_PAGE, "Next group", "Move it to the next skill group", "nextgrp")}
        # Gains remembered per skill and in the log, for the rates and the Recent gains list.
        LOG_KEEP = 200
        MAX_LOCKSETS = 10
        # Client gump art: the small gem that uses a skill (normal, pressed, hover).
        GEM = (0x0837, 0x0838, 0x0838)
        # Client gump art for the lock arrows: up, down, locked.
        LOCK_ART = (0x0983, 0x0985, 0x082C)
        GROUP_OPEN, GROUP_SHUT = 0x0826, 0x0827
        LINE_GREEN = 0x0808
        BAR_BG_HUE = 946
        DIM_HUE = 946
        SEL_COLOR, SEL_ALPHA = "#D8B048", 0.16
        GROUP_COLOR, GROUP_ALPHA = "#FFFFFF", 0.07
        # A second click within this many seconds confirms a risky button (All down, Reset groups).
        ARM_SECS = 4.0
        # The window's texts follow the clock this often even when no skill moved.
        REDRAW_EVERY = 1.0
        # Used only when the client's skill list cannot be read: the names are looked up through the API
        # one by one, in the client's own order, which is the order of the skill index.
        FALLBACK_NAMES = ["Alchemy", "Anatomy", "Animal Lore", "Item Identification", "Arms Lore", "Parrying",
            "Begging", "Blacksmithy", "Bowcraft/Fletching", "Peacemaking", "Camping",
            "Carpentry", "Cartography", "Cooking", "Detecting Hidden", "Discordance",
            "Evaluating Intelligence", "Healing", "Fishing", "Forensic Evaluation", "Herding",
            "Hiding", "Provocation", "Inscription", "Lockpicking", "Magery", "Resisting Spells",
            "Tactics", "Snooping", "Musicianship", "Poisoning", "Archery", "Spirit Speak",
            "Stealing", "Tailoring", "Animal Taming", "Taste Identification", "Tinkering",
            "Tracking", "Veterinary", "Swordsmanship", "Mace Fighting", "Fencing", "Wrestling",
            "Lumberjacking", "Mining", "Meditation", "Stealth", "Remove Trap", "Necromancy",
            "Focus", "Chivalry", "Bushido", "Ninjitsu", "Spellweaving", "Mysticism", "Imbuing", "Throwing"]
        # Training tips: per skill, (up to, tip) pairs. A tip covers the range from the previous "up to"
        # (or 0) to its own, and past the last pair there is no tip. These are general classic-era hints.
        # A skill left out shows no tip. Names are spelled as the client
        # spells them. tip_table turns this into the form the lookups use.
        TIPS = {"Alchemy": [(30, "NPC alchemists teach the first points for gold"), (50, "Heal and Agility potions"),
                        (70, "Cure and Greater Agility potions"), (90, "Greater Strength and Greater Heal potions"),
                        (100, "Greater Cure and Greater Explosion potions")],
            "Anatomy": [(100, "Use it on any creature or player; bandaging checks it too")],
            "Animal Lore": [(100, "Use it on tamed or tameable animals")],
            "Item Identification": [(100, "Use it on any item")], "Arms Lore": [(100, "Use it on weapons and armour")],
            "Parrying": [(100, "Fight with a shield on (only shields parry pre-AoS)")],
            "Begging": [(100, "Beg from town NPCs")],
            "Blacksmithy": [(30, "NPC blacksmiths teach the first points for gold"), (50, "Maces, then cutlasses"),
                            (65, "Scimitars, then broadswords and kryss"),
                            (80, "Katanas, then short spears and spears"),
                            (100, "Plate gorgets and gloves, then plate legs and tunics")],
            "Bowcraft/Fletching": [(40, "Shafts and arrows"), (65, "Bows"), (85, "Crossbows"),
                                   (100, "Heavy crossbows")],
            "Peacemaking": [(100, "Use it near creatures; tougher ones as it rises")],
            "Camping": [(100, "Light kindling over and over (a blade on a tree gives some)")],
            "Carpentry": [(30, "NPC carpenters teach the first points for gold"), (50, "Medium crates"),
                          (65, "Large crates, then wooden shields"), (85, "Fishing poles and quarter staves"),
                          (100, "Gnarled and black staves")],
            "Cartography": [(30, "NPC mapmakers teach the first points for gold"), (50, "Local maps"),
                            (65, "City maps"), (100, "Sea charts, then world maps")],
            "Cooking": [(30, "NPC cooks teach the first points for gold"),
                        (100, "Cook over and over (fish steaks and ribs are cheap)")],
            "Detecting Hidden": [(100, "Use it often, best near someone hidden")],
            "Discordance": [(100, "Use it on creatures; tougher ones as it rises")],
            "Evaluating Intelligence": [(100, "Use it on any player or creature")],
            "Healing": [(30, "NPC healers teach the first points; bandage yourself when hurt"),
                        (60, "Bandage yourself or friends while hurt"),
                        (80, "Keep bandaging; curing poison needs 60 Healing and 60 Anatomy"),
                        (100, "Keep bandaging; resurrecting needs 80 Healing and 80 Anatomy")],
            "Fishing": [(100, "Fish over and over, in any water")], "Forensic Evaluation": [(100, "Use it on corpses")],
            "Herding": [(100, "Herd animals with a shepherd's crook")], "Hiding": [(100, "Use it over and over")],
            "Provocation": [(100, "Make creatures fight each other; tougher ones as it rises")],
            "Inscription": [(30, "NPC scribes teach the first points for gold"),
                            (100, "Scribe scrolls of a circle you sometimes fail (spell in your book)")],
            "Lockpicking": [(30, "NPC thieves and tinkers teach the first points"),
                            (100, "Pick locked boxes just above your level")],
            "Magery": [(30, "NPC mages teach the first points; then 2nd circle spells"),
                       (45, "3rd circle: Bless, Teleport"), (55, "4th circle: Greater Heal, Mana Drain"),
                       (65, "5th circle: Paralyze, Mind Blast"), (75, "6th circle: Invisibility, Mark"),
                       (90, "7th circle: Flamestrike, Mana Vampire"), (100, "8th circle: Earthquake, summons")],
            "Resisting Spells": [(100, "Rises when spells hit you: a friend's low curses work")],
            "Tactics": [(100, "Rises as you fight with any weapon")],
            "Snooping": [(100, "Look into others' packs (a friend's pack animal is safe)")],
            "Musicianship": [(100, "Play an instrument; the other bard skills train it too")],
            "Poisoning": [(30, "Lesser poison on a weapon or food"), (60, "Regular poison"),
                          (100, "Greater, then deadly poison")],
            "Archery": [(30, "An archery butte or an NPC trainer for the first points"),
                        (100, "Shoot creatures a little tougher than you as it rises")],
            "Spirit Speak": [(100, "Use it over and over")],
            "Stealing": [(100, "Steal light items from a friend's pack; heavier is harder")],
            "Tailoring": [(30, "NPC tailors teach the first points for gold"), (45, "Short pants and fancy shirts"),
                          (55, "Cloaks"), (70, "Robes, then leather gorgets and sleeves"),
                          (85, "Leather leggings and tunics"),
                          (100, "Studded gloves, then studded sleeves and leggings")],
            "Animal Taming": [(30, "NPC animal trainers teach the first points for gold"),
                              (50, "Horses, ostards, llamas, black and polar bears"),
                              (70, "Panthers, grey wolves, grizzly bears, great harts"),
                              (85, "White wolves, bulls, frenzied ostards"),
                              (100, "Drakes and hell hounds, then dragons")],
            "Taste Identification": [(100, "Use it on food and potions")],
            "Tinkering": [(30, "NPC tinkers teach the first points for gold"), (60, "Tools and clock parts"),
                          (80, "Lockpicks"), (100, "Spyglasses or jewellery")],
            "Tracking": [(100, "Use it over and over")],
            "Veterinary": [(30, "NPC veterinarians teach the first points"), (60, "Bandage hurt animals and pets"),
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
            "Mining": [(30, "NPC miners teach the first points for gold"), (65, "Mine iron ore in mountains and caves"),
                       (100, "Keep mining: the coloured ores come from 65 up")],
            "Meditation": [(100, "Spend mana, then meditate; metal armour blocks it")],
            "Stealth": [(100, "Needs 80 Hiding: hide, then move with Stealth (light armour)")],
            "Remove Trap": [(100, "Use it on trapped boxes (tinkers can trap some to practise on)")],}
        # The stat targets live in a key of their own, apart from the per-skill marks.
        STAT_TARGETS_KEY = "Skills_stat_targets"
        STAT_TARGET_MAX = 250
        # Lock words as the API takes them, in the order of the client's lock enum (up, down, locked).
        LOCK_WORD = ("up", "down", "locked")
        LOCK_TEXT = ("Going up", "Going down", "Locked")
        LOCK_SET = ("Set it to go up", "Set it to go down", "Lock it")
        # The filters in the order the Filter button cycles through. The first word is what passes() tests.
        FILTERS = [("all", "All skills"), ("trained", "Trained (above 0)"),
                   ("gaining", "Gaining now"), ("session", "Gained this session"),
                   ("up", "Set to go up"), ("down", "Set to go down"), ("locked", "Locked"),
                   ("below", "Below cap"), ("pinned", "Pinned")]
        SORTS = ("name", "real", "value", "cap", "gain", "lock")
        # Defaults of every setting. The saved string only holds values that differ from these, and
        # unknown keys from other versions are skipped on load.
        settings = {"replace": True, "x_hides": True, "bars": True, "col_cap": True,
                    "col_gain": True, "journal": False, "lock_at_cap": False, "lock_at_target": True, "cap_warn": True,
                    "rows": 12, "total_cap": TOTAL_CAP_DEFAULT, "hl_secs": 30, "rate_min": 30,
                    "sec_summary": True, "sec_stats": True, "sec_locks": True,
                    "sec_detail": True, "sec_log": False, "log_lines": 5,
                    "sort": "name", "asc": True, "filter": 0, "groups": False, "minimized": False, "width": 0,
                    "tips": True, "lock_stat_target": True}
        # A copy of the defaults, taken before load_settings changes anything.
        DEFAULTS = dict(settings)
        # Allowed range per numeric setting; kv_load and kv_save clamp to it.
        LIMITS ={"rows": (4, 40), "total_cap": (100, 72000), "hl_secs": (0, 600),
                  "rate_min": (5, 240), "log_lines": (2, 15), "filter": (0, len(FILTERS) - 1), "width": (0, 4000)}
        # Settings that change the window's shape: the settings page rebuilds the window when one changes.
        LAYOUT_KEYS = ("bars", "col_cap", "col_gain", "rows", "sec_summary", "sec_stats",
                       "sec_locks", "sec_detail", "sec_log", "log_lines", "tips", "x_hides", "replace")
        # Seconds a renamed group's name rests before it is saved, so typing does not save per letter.
        GRP_SETTLE = 1.0
        STAT_NAMES = ("Strength", "Dexterity", "Intelligence")

        def tip_table():
            """Turns the TIPS table into {lower-case skill name: [(up to in tenths, "lo-hi", tip)]}.

            Run once when the part is built.
            """
            out = {}
            for name, rows in TIPS.items():
                lst, lo = [], 0
                for hi, text in rows:
                    lst.append((hi * 10, "%g-%g" % (lo / 10.0, hi), text))
                    lo = hi * 10
                out[name.lower()] = lst
            return out

        TIP_TABLE = tip_table()
        marks = {"pins": set(), "targets": {}}
        locksets = []
        stat_tgt = [0, 0, 0]
        # Window state. rebuild is a request for the tick to rebuild the window; ver is part of the key
        # that decides whether the list's rows are worked out again; arm holds the times of first clicks
        # that wait for a second.
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "sel": None,
              "last_click": (None, 0.0), "arm": {}, "search": "", "pc": {}, "save_at": 0.0, "to_write": [], "ver": 0,
              "preview": False}
        # The window and what it holds: the gump, its controls by key, the button store, and the shown
        # rows with their lookup by (kind, key, nth).
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "rowmap": {}}
        page = {"sync": False, "skip": False}
        # Kit.basics gives the cleanup list, the click queue and the say helper for the journal.
        cleanup, queue, say = Kit.basics(st, TITLE)
        # (control, attribute) to the last value set; see setp.
        UIC = {}
        REF = {"world": None, "player": None, "how": ""}
        # The client's skills as read: Skill objects, their names, whether each can be used, and the last
        # values. low is lower-case names; rr is the round-robin position of read_skills.
        SK = {"objs": [], "names": [], "click": [], "collide": [], "n": 0, "cur": [], "low": [], "full": True, "rr": 0}
        STATS = {"cur": [0, 0, 0], "locks": [0, 0, 0], "cap": 0, "prev": [0, 0, 0]}
        # The client's skill groups as read: the list, whether it could be read, a change counter, a
        # signature, and skill to group.
        GR = {"list": [], "ok": False, "ver": 0, "sig": None, "of": {}}
        # The client's window list, cached for vanilla_check.
        VG = {"gumps": None, "sig": None, "full_at": 0.0}

        def touch():
            """Something the window shows changed: redraw on this tick and work the list's rows out again.

            The counter is part of rebuild_rows' key.
            """
            st["ver"] += 1
            st["dirty"] = True

        # Seconds between skill reads while the list is off screen.
        HIDDEN_READ = 0.5
        # Seconds between stat reads; stats move a point at a time.
        STATS_EVERY = 1.0
        # Seconds between looks at the total cap when nothing else asked.
        CAP_EVERY = 5.0
        ROW_SPARE = 2
        ROW_CHUNK = 8
        ROW_WAIT = 2.0

        def list_moved():
            """A skill's values changed: redraw its texts, and re-sort the list only when it can follow values.

            The order and members are worked out again only when sorted by a value or filtered on values.
            Sorted by name with All or Pinned they cannot change, so nothing is redone.
            """
            st["dirty"] = True
            if (settings["sort"] != "name" or FILTERS[settings["filter"]][0] not in ("all", "pinned")):
                st["ver"] += 1

        fitst = {"width": None, "rows": None, "slot": None, "k": 1.0, "full": None}

        def eff_width():
            """The width the layout wants, else the player's own (0 means the natural width)."""
            return fitst["width"] if fitst["width"] is not None else settings["width"]

        def layout_fit(w, h, mode):
            """Layout hook: the window's slot in a zone is w by h pixels, or None when freed. Client thread.

            Runs in the layout keeper's pass. It records the slot, clears the row count and the metrics and
            asks for a rebuild. Mode "again" redraws at a slot size it was already told.
            """
            new = (int(w), int(h)) if (w and h) else None
            # The same slot again needs no rebuild, unless the layout insists with "again".
            if new == fitst["slot"] and not (mode == "again" and new is not None):
                return
            fitst["slot"] = new
            fitst["width"] = new[0] if new is not None else None
            fitst["rows"] = None
            st["m"] = None
            st["rebuild"] = "window"
            touch()

        def drawn_at():
            """Layout hook for Check fit: the scale the window is drawn at and the slot size showing it at 100%."""
            return fitst["k"], fitst["full"]

        sess = {"start": 0.0, "base": {}, "stats": None, "seen": 0.0}

        def load_settings():
            """Loads the saved settings, keeping the defaults for anything missing, and checks the sort key."""
            Kit.kv_load(SETTINGS_KEY, ";", settings, LIMITS, ("sort",))
            if settings["sort"] not in SORTS:
                settings["sort"] = "name"

        def save_settings():
            """Saves the settings that differ from the defaults."""
            Kit.kv_save(SETTINGS_KEY, ";", settings, DEFAULTS, LIMITS, ("sort",))

        def load_marks():
            """Loads pins and per-skill targets from Skills_marks.

            Format: skill index, pin flag and target in tenths, joined by colons, entries by semicolons.
            Entries that do not parse are skipped.
            """
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
            """Saves pins and targets in the Skills_marks format (see load_marks), only for skills that have one."""
            idx = sorted(marks["pins"] | set(marks["targets"]))
            Kit.put_var(MARKS_KEY, ";".join("%d:%s:%d" % (i, "1" if i in marks["pins"] else "0",
                                                          marks["targets"].get(i, 0)) for i in idx))

        def load_locksets():
            """Loads the named lock sets from Skills_locksets.

            Format: name, equals sign, one letter per skill (u, d or l), sets joined by a bar.
            """
            del locksets[:]
            for part in Kit.get_var(LOCKSETS_KEY).split("|"):
                if "=" in part:
                    name, code = part.split("=", 1)
                    if name and code:
                        locksets.append((name, code))

        def save_locksets():
            """Saves the lock sets in the Skills_locksets format."""
            Kit.put_var(LOCKSETS_KEY, "|".join("%s=%s" % (n, c) for n, c in locksets))

        def load_stat_targets():
            """Loads the Str, Dex and Int targets (0 means none) from their own key, clamped to the stat maximum."""
            p = Kit.get_var(STAT_TARGETS_KEY).split(",")
            for k in range(3):
                try:
                    stat_tgt[k] = max(0, min(STAT_TARGET_MAX, int(p[k])))
                except (IndexError, ValueError):
                    stat_tgt[k] = 0

        def load_session():
            """Loads the running session from Skills_session, or starts a fresh one.

            Format: start time, per-skill base values, stat base values and the last time seen, joined by
            bars. A session older than SESSION_STALE_H hours, or one that claims to start in the future,
            is dropped. Entries that do not parse are skipped so a damaged value cannot stop the module.
            """
            p = Kit.get_var(SESSION_KEY).split("|")
            now = time.time()
            sess.update({"start": now, "base": {}, "stats": None, "seen": now})
            if len(p) < 4:
                return
            try:
                start, seen = float(p[0]), float(p[3])
            except ValueError:
                return
            # A long break (or a clock gone backwards) means a new session.
            if now - seen > SESSION_STALE_H * 3600 or start > now:
                return
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
            """Saves the session so it survives a restart of Virtue Assistant."""
            sess["seen"] = time.time()
            b = ",".join("%d:%d" % (k, v) for k, v in sorted(sess["base"].items()))
            s = ",".join(str(x) for x in sess["stats"]) if sess["stats"] else ""
            Kit.put_var(SESSION_KEY, "%d|%s|%s|%d" % (sess["start"], b, s, sess["seen"]))

        def new_session():
            """Starts a new session from the values now and clears the gain history and the gains log."""
            sess.update({"start": time.time(), "base": {}, "stats": None})
            for i in range(SK["n"]):
                sess["base"][i] = SK["cur"][i][0]
            if any(STATS["cur"]):
                sess["stats"] = list(STATS["cur"])
            st["gains"], st["log"] = {}, []
            save_session()

        def save_pos():
            """Saves the window's place."""
            Kit.save_pos(POS_KEY, win["g"])

        def find_world():
            """Returns the client's World object, or None when it cannot be reached."""
            # Read through reflection: the World is a singleton on the client class.
            return Typing._get(None, "Instance", Client._type("ClassicUO.Game.World"))

        def load_skill_objects(objs, how):
            """Stores the client's Skill objects and what is known of them, and flags a full read.

            objs: the Skill objects. how: "client" (read from the player) or "api" (the fallback lookup).
            """
            names = [str(safe(lambda s=s: s.Name, "") or "?") for s in objs]
            click = [bool(safe(lambda s=s: s.IsClickable, False)) for s in objs]
            low = [n.lower() for n in names]
            # API.UseSkill and API.SetSkillLock take the first skill whose name contains the text. A name that
            # sits inside an earlier skill's name must go by index instead; collide marks those skills.
            collide = [any(low[i] in low[j] for j in range(i)) for i in range(len(low))]
            SK.update({"objs": objs, "names": names, "click": click, "collide": collide,
                       "n": len(objs), "low": low, "full": True})
            # The value lists are only rebuilt when the number of skills changed.
            if len(SK["cur"]) != len(objs):
                SK["cur"] = [[0, 0, 0, 0] for _ in objs]
            REF["how"] = how
            # Column widths follow the names, so the cached metrics are dropped.
            st["m"] = None

        def refresh_refs(force=False):
            """Finds the client's Skill objects (kept: the client updates them in place). True when skills exist.

            Looked up again every few seconds in case of a relog. force skips the wait. Falls back to the
            API's skill lookup by name when the client's own list cannot be reached.
            """
            now = time.time()
            if not force and now < st["ref_at"]:
                return SK["n"] > 0
            st["ref_at"] = now + 3.0
            world = find_world()
            player = Typing._get(world, "Player") if world is not None else None
            if player is not None:
                arr = Typing._get(player, "Skills")
                objs = list(arr) if arr is not None else None
                if objs:
                    # Reference identity: the client keeps one object per skill, so an unchanged object means the same
                    # character.
                    same = REF["player"] is not None and REF["player"] is player and len(objs) == SK["n"]
                    relog = REF["player"] is not None and not same
                    REF.update({"world": world, "player": player})
                    if not same:
                        if relog:
                            # A different player object is another login: start the values and the session from scratch.
                            SK["cur"] = []
                            st["ready"] = False
                            st["rebuild"] = "window"
                        load_skill_objects(objs, "client")
                    return True
            REF.update({"world": world, "player": None})
            # The API fallback is looked up once and kept until the client's own list can be read.
            if SK["n"] == 0 or REF["how"] != "api":
                objs = []
                for name in FALLBACK_NAMES:
                    s = API.GetSkill(name)
                    if s is not None and str(s.Name) == name:
                        objs.append(s)
                if objs:
                    load_skill_objects(objs, "api")
            return SK["n"] > 0

        RR_N = 15

        def read_skills(full=False):
            """Reads fresh values of every skill and returns {index: values before} of the ones that changed.

            Runs every tick, so it allocates nothing unless a value changed (a changed skill gets a new
            list, and the old one is what note_gains compares with). Base and Value are read every tick for
            every skill; Cap and Lock only for RR_N skills a tick in turn (each about once a second) and at
            once for a skill whose Base or Value moved, so the locks at a cap or target see fresh values.
            full reads all four of every skill: the first read, new skill objects, skills not in yet.
            """
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
            # Local alias: int() is looked up for every skill on every tick.
            _int = int
            for i in range(n):
                s = objs[i]
                try:
                    b, v = _int(s.BaseFixed), _int(s.ValueFixed)
                except Exception:
                    continue
                c = cur[i]
                # Cap and Lock are read when the value moved, on a full read, or on this skill's turn.
                if full or b != c[0] or v != c[1] or (i - rr) % n < RR_N:
                    try:
                        cp = _int(s.CapFixed)
                        lk = _int(s.Lock)
                    except Exception:
                        continue
                    if b != c[0] or v != c[1] or cp != c[2] or lk != c[3]:
                        changed[i] = c
                        cur[i] = [b, v, cp, lk]
            return changed

        def read_stats():
            """Reads Str, Dex, Int, their locks and the stat cap. Returns True if any of them changed.

            Uses the player the skills came from, else the API's. A lock the player just clicked is shown
            for a moment as clicked, until the server's answer catches up.
            """
            cur, locks, cap = STATS["cur"], STATS["locks"], STATS["cap"]
            p = REF["player"]
            if p is None:
                p = API.Player
            if p is not None:
                try:
                    cur = [int(p.Strength), int(p.Dexterity), int(p.Intelligence)]
                    locks = [int(p.StrLock), int(p.DexLock), int(p.IntLock)]
                    cap = int(p.StatsCap)
                except Exception:
                    pass
            # A click on a stat lock is shown at once; the server's confirmation takes a moment.
            if st["stat_pending"]:
                now = time.time()
                locks = list(locks)
                for k, (lk, until) in list(st["stat_pending"].items()):
                    if now < until:
                        locks[k] = lk
                    else:
                        st["stat_pending"].pop(k, None)
            if cur == STATS["cur"] and locks == STATS["locks"] and cap == STATS["cap"]:
                return False
            # Kept so note_stats can tell a one-point step from a jump.
            STATS["prev"] = STATS["cur"]
            STATS["cur"], STATS["locks"], STATS["cap"] = cur, locks, cap
            return True

        def skills_loaded():
            """True once the server has sent real caps, which a skill that is not in yet lacks."""
            return any(c[2] > 0 for c in SK["cur"])

        def group_mgr():
            """Returns the client's skills group manager, or None."""
            w = REF["world"] or find_world()
            return Typing._get(w, "SkillsGroupManager") if w is not None else None

        def groups_wanted():
            """True when the groups are on show somewhere: the list shows them, the details name one, or the
            settings page is open.
            """
            if cfg.f is not None:
                return True
            if win["g"] is None or not win["c"] or st["minimized"] or st["docked"]:
                return False
            return settings["groups"] or (st["sel"] is not None and settings["sec_detail"])

        def read_groups(force=False):
            """Reads the client's skill groups into GR (they can also change in the client's own window).

            force skips the wait. Read once a second while the list or settings page shows the groups, and
            every GRP_DETAIL_EVERY seconds while only the details name one. A change of names, members or
            folding bumps GR["ver"] so the list's rows are worked out again.
            """
            now = time.time()
            if not force and (now < st["grp_at"] or not groups_wanted()):
                return
            # Once a second while the list or the settings page shows the groups, slower for the details alone.
            st["grp_at"] = now + (1.0 if cfg.f is not None or settings["groups"] else GRP_DETAIL_EVERY)
            mgr = group_mgr()
            lst = Typing._get(mgr, "Groups") if mgr is not None else None
            out = []
            if lst is not None:
                for g in list(lst):
                    try:
                        n = int(g.Count)
                        members = [int(g.GetSkill(k)) for k in range(n)]
                        # Members past the skill count are dropped: a group may name a skill this client does not have.
                        out.append({"obj": g, "name": str(g.Name or ""), "members": [m for m in members if m < SK["n"]],
                                    "max": bool(g.IsMaximized)})
                    except Exception:
                        continue
            sig = (lst is not None, tuple((g["name"], tuple(g["members"]), g["max"]) for g in out))
            if sig != GR["sig"]:
                GR["sig"] = sig
                GR["ver"] += 1
            # Skill to group. Walking backwards makes the first group win when a skill is in several.
            of = {}
            for gi in range(len(out) - 1, -1, -1):
                for k in out[gi]["members"]:
                    of[k] = gi
            GR["list"], GR["ok"], GR["of"] = out, lst is not None, of

        # Seconds between group reads for the details alone.
        GRP_DETAIL_EVERY = 3.0

        def group_of(i):
            """The index of the group a skill belongs to, or None."""
            return GR["of"].get(i)

        def groups_save():
            """Saves the client's groups to disk through its manager and reads them back."""
            mgr = group_mgr()
            if mgr is not None:
                safe(lambda: mgr.Save())
            read_groups(True)

        def ga_call(name, args):
            """Calls a static method of the client's GameActions class by name."""
            return Tz.call(None, name, args, Tz.T("ClassicUO.Game.GameActions"))

        def set_lock(i, v):
            """Sets skill i's lock to v (0 up, 1 down, 2 locked) and remembers it at once.

            Goes through the API by name where the name is unambiguous. For a name inside another skill's
            name it calls the client's own action by index and sets the object's Lock field by hand, with
            the client's own noise kept quiet.
            """
            if i is None or i >= SK["n"] or SK["cur"][i][3] == v:
                return
            if not SK["collide"][i]:
                API.SetSkillLock(SK["names"][i], LOCK_WORD[v])
            else:
                with Kit.quiet:
                    import System
                    ga_call("ChangeSkillLockStatus", [System.UInt16(i), System.Byte(v)])
                    lt = Tz.T("ClassicUO.Game.Data.Lock")
                    Tz.put(SK["objs"][i], "Lock", System.Enum.ToObject(lt, v))
            SK["cur"][i][3] = v

        def use_skill(i):
            """Uses skill i, by name through the API or by index where the name is ambiguous."""
            if i is None or i >= SK["n"]:
                return
            if not SK["click"][i]:
                say("%s can't be used directly." % SK["names"][i], Kit.HUE_INFO)
                return
            if not SK["collide"][i]:
                API.UseSkill(SK["names"][i])
                return
            try:
                ga_call("UseSkill", [i])
            except Exception as ex:
                say("couldn't use %s (%s)." % (SK["names"][i], Tz.why(ex)), Kit.HUE_BAD)

        def make_button(i):
            """Makes the client's own floating skill button for skill i (one per skill) beside the window.

            The same gump the client makes when a skill is dragged out of its window. An older button of the
            same skill is disposed first so there is only one.
            """
            if i is None or i >= SK["n"] or not SK["click"][i]:
                say("only a usable skill gets a button.", Kit.HUE_INFO)
                return
            try:
                import System
                for b in Tz.windows(["SkillButtonGump"]):
                    if int(Tz.get(b, "SkillID")) == i:
                        b.Dispose()
                t = Tz.T("ClassicUO.Game.UI.Gumps.SkillButtonGump")
                world = REF["world"] or find_world()
                g = win["g"]
                x, y = (g.GetX() + g.GetWidth() + 10, g.GetY()) if Kit.is_open(g) else (200, 200)
                # Built by reflection: the gump's constructor takes the world, the skill and the place.
                btn = System.Activator.CreateInstance(t, System.Array[object]([world, SK["objs"][i], x, y]))
                Tz.call(None, "Add", [btn, True], Tz.T("ClassicUO.Game.Managers.UIManager"))
                say("%s button placed beside the window." % SK["names"][i], Kit.HUE_GOOD)
            except Exception as ex:
                say("couldn't make the button (%s)." % Tz.why(ex), Kit.HUE_BAD)

        def ask_server():
            """Asks the server for fresh skill values through the client's own request. True if it was sent.

            The request opens the client's skills window, which vanilla_check closes again at once, because
            swallow_until tells it this one is ours.
            """
            world = REF["world"] or find_world()
            st["swallow_until"] = time.time() + 6.0
            st["asked"] = time.time()
            try:
                ga_call("OpenSkills", [world])
                return True
            except Exception:
                return False

        def set_stat_lock(k, v):
            """Sets Str, Dex or Int (k 0-2) to up, down or locked (v 0-2) and shows it until the server answers."""
            API.SetStatLock(("str", "dex", "int")[k], LOCK_WORD[v])
            STATS["locks"][k] = v
            st["stat_pending"][k] = (v, time.time() + 2.5)

        def f1(tenths):
            """Tenths as text with one decimal."""
            return "%.1f" % (tenths / 10.0)

        def sgain(i):
            """The session gain of skill i in tenths: its value now less the value when the session began."""
            b = sess["base"].get(i)
            return 0 if b is None else SK["cur"][i][0] - b

        def total_gain():
            """The total session gain in tenths."""
            return sum(sgain(i) for i in range(SK["n"]))

        # Rates are never worked out over less than this many seconds.
        MIN_RATE_SPAN = 600.0

        def hours_running():
            """Hours the session has run, never less than MIN_RATE_SPAN seconds, so a first gain is not shown
            as a huge rate per hour.
            """
            return max(MIN_RATE_SPAN, time.time() - sess["start"]) / 3600.0

        def recent_gain(i, now):
            """Gain of skill i in tenths within the recent window (settings: rate_min minutes)."""
            win_s = settings["rate_min"] * 60
            return sum(d for t, d in st["gains"].get(i, []) if now - t <= win_s)

        def rates(i, now):
            """Returns (session average per hour, recent per hour) for skill i, in tenths.

            The recent span is the window or the time since the session or the module started if shorter,
            and never under MIN_RATE_SPAN.
            """
            avg = sgain(i) / hours_running()
            span = max(MIN_RATE_SPAN, min(settings["rate_min"] * 60.0, now - max(sess["start"], st["started"])))
            recent = recent_gain(i, now) / (span / 3600.0)
            return avg, recent

        def dur(secs):
            """Formats seconds as 1h 05m, 7m or 12s."""
            secs = int(max(0, secs))
            if secs >= 3600:
                return "%dh %02dm" % (secs // 3600, (secs % 3600) // 60)
            if secs >= 60:
                return "%dm" % (secs // 60)
            return "%ds" % secs

        def eta(i, now, rt=None):
            """Time to cap of skill i at the current pace, as text.

            Returns "at cap", "--" when it is not rising, else a time with a leading tilde. The recent rate
            is used when there is one, else the session average. rt is the result of rates() if already known.
            """
            base, _, cap, _ = SK["cur"][i]
            if base >= cap:
                return "at cap"
            avg, recent = rt if rt is not None else rates(i, now)
            r = recent if recent > 0 else avg
            if r <= 0:
                return "--"
            return "~" + dur((cap - base) / r * 3600)

        def note_gains(changed, now):
            """Handles the real value of every skill that changed: gains, losses, rates, journal lines, locks.

            changed is {index: values before}. A gain is added to the history and the log, turns the name
            green for hl_secs seconds, and may lock the skill at its cap or its target. Also saves the
            session about every fifteen seconds while gains come in.
            """
            dirty = False
            for i, old in changed.items():
                new = SK["cur"][i]
                d = new[0] - old[0]
                if d == 0:
                    continue
                dirty = True
                name = SK["names"][i]
                # A skill's session base is its value before its first change.
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
                    say("%s %s%s (%s, session %+.1f)." % (name, "+" if d > 0 else "-", f1(abs(d)), f1(new[0]),
                        sgain(i) / 10.0), Kit.HUE_GOOD if d > 0 else Kit.HUE_BAD)
                # Its cap first, then its target. new is the skill's live list, so the target check sees a lock
                # set at the cap.
                for mark, opt, what in ((new[2], "lock_at_cap", "its cap (%s)"),
                                        (marks["targets"].get(i), "lock_at_target", "its target %s")):
                    # Only a rise across the mark counts, so an old value above it does not fire.
                    if d > 0 and mark is not None and old[0] < mark <= new[0]:
                        what = what % f1(mark)
                        # Locks only a skill that is still going up.
                        if settings[opt] and new[3] == 0:
                            set_lock(i, 2)
                            say("%s reached %s and was locked." % (name, what), Kit.HUE_GOOD)
                        else:
                            say("%s reached %s." % (name, what), Kit.HUE_GOOD)
            # Saved at most every fifteen seconds so a run of gains is one write.
            if dirty and time.time() >= st["save_at"]:
                st["save_at"] = time.time() + 15.0
                save_session()

        def total_real():
            """The real values of every skill added up, in tenths."""
            return sum(c[0] for c in SK["cur"])

        def at_total_cap():
            """True at the total cap with a skill set to go up that can rise but none set to go down.

            Nothing can rise any more then: the next gain would need a loss somewhere.
            """
            if total_real() < settings["total_cap"]:
                return False
            up = any(c[3] == 0 and c[0] < c[2] for c in SK["cur"])
            down = any(c[3] == 1 and c[0] > 0 for c in SK["cur"])
            return up and not down

        def cap_warning():
            """Warns once in the journal when at_total_cap becomes true; re-arms when it clears."""
            if not settings["cap_warn"]:
                st["warned_cap"] = False
                return
            stuck = at_total_cap()
            if stuck and not st["warned_cap"]:
                say("at the total skill cap (%s) and no skill set to go down: nothing can rise."
                    % f1(settings["total_cap"]), Kit.HUE_BAD)
            st["warned_cap"] = stuck

        def stat_gain(k):
            """The session gain of stat k in points (0 without a session base)."""
            base = sess["stats"]
            return STATS["cur"][k] - base[k] if base else 0

        def note_stats():
            """Locks a stat that has stepped by one point onto its target, the way its lock sends it.

            A step of one point (a gain or a loss; the jump of a spell or a potion does not count) onto the
            target, in the direction its lock allows, means the target is reached. Locked there when the
            option is on. Runs when the stats changed.
            """
            prev, cur = STATS["prev"], STATS["cur"]
            for k in range(3):
                t = stat_tgt[k]
                if not t or not prev[k] or cur[k] != t:
                    continue
                # Rose to it: the stat was set to go up. Fell to it: set to go down. Any other step is ignored.
                way = {1: 0, -1: 1}.get(cur[k] - prev[k])
                if way is None:
                    continue
                if settings["lock_stat_target"] and STATS["locks"][k] == way:
                    set_stat_lock(k, 2)
                    say("%s reached its target %d and was locked." % (STAT_NAMES[k], t), Kit.HUE_GOOD)
                else:
                    say("%s reached its target %d." % (STAT_NAMES[k], t), Kit.HUE_GOOD)

        def stat_at_target(k):
            """A target was just set where the stat already is: lock it at once if the option is on."""
            t, v = stat_tgt[k], STATS["cur"][k]
            if t and v == t and settings["lock_stat_target"] and STATS["locks"][k] != 2:
                set_stat_lock(k, 2)
                say("%s is at its target %d and was locked." % (STAT_NAMES[k], t), Kit.HUE_GOOD)

        def stat_tip(k, hrs):
            """Tooltip text of stat k: the session gain, the rate per hour and the target.

            hrs is the hours the session has run.
            """
            v = STATS["cur"][k]
            lines = ["%s %d" % (STAT_NAMES[k], v)]
            if sess["stats"]:
                d = stat_gain(k)
                lines[0] += ": %+d this session (%.1f / hour)" % (d, d / hrs)
            t = stat_tgt[k]
            if not t:
                lines.append("No target (click: set one in settings)")
            elif v == t:
                lines.append("Target %d: reached" % t)
            else:
                lines.append("Target %d: %d to go %s%s" % (t, abs(t - v), "up" if t > v else "down",
                    ", then it locks" if settings["lock_stat_target"] else ""))
            return "\n".join(lines)

        def tip_for(i):
            """Returns (range text, tip) for skill i at its real value now, or None when there is no tip."""
            if i is None or i >= SK["n"]:
                return None
            rows = TIP_TABLE.get(SK["names"][i].lower())
            if rows:
                base = SK["cur"][i][0]
                for hi, rng, text in rows:
                    if base < hi:
                        return rng, text
            return None

        def passes(i, now):
            """True when skill i passes the search text and the chosen filter."""
            f = FILTERS[settings["filter"]][0]
            base, _, cap, lock = SK["cur"][i]
            q = st["search"]
            if q and q not in SK["low"][i]:
                return False
            if f == "trained":
                return base > 0
            if f == "gaining":
                return recent_gain(i, now) > 0
            if f == "session":
                return sgain(i) > 0
            # Up, down and locked filters compare with the lock's index.
            if f in LOCK_WORD:
                return lock == LOCK_WORD.index(f)
            if f == "below":
                return base < cap
            if f == "pinned":
                return i in marks["pins"]
            return True

        def sort_list(idx):
            """Sorts skill indices by the chosen column, either way round, with names breaking ties."""
            s = settings["sort"]
            # Lower-case names are made once per load, not per sort.
            name = SK["low"].__getitem__
            if s == "name":
                out = sorted(idx, key=name)
            else:
                col = {"real": 0, "value": 1, "cap": 2, "lock": 3}.get(s)
                kf = sgain if col is None else (lambda i: SK["cur"][i][col])
                # A stable sort by the value on top of a sort by name, so equal values keep name order.
                out = sorted(sorted(idx, key=name), key=kf)
            if not settings["asc"]:
                out.reverse()
            return out

        def descriptors(now):
            """Works out the rows the list shows, in order, as ("s", skill) and ("g", group key, folded) entries.

            Without groups: pinned skills first, then the rest, each sorted. With groups: a Pinned header when
            any shown skill is pinned, then each client group with its members, then an Other group for the
            skills no group holds. Folded groups keep their header only. A group with no shown member is
            left out while a search or filter is active.
            """
            vis = [i for i in range(SK["n"]) if passes(i, now)]
            # Membership tests per group are against a set; vis keeps the order.
            vset = set(vis)
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

        def row_click(i):
            """Returns the click handler of skill row i: one click picks it, a second within 0.6 s makes its button.

            The handler only queues the action; the tick carries it out.
            """
            def handler(*args):
                """Queues pick or button for the row; runs on the client thread."""
                now = time.time()
                last, t = st["last_click"]
                if last == i and now - t <= 0.6:
                    st["last_click"] = (None, 0.0)
                    queue.add(("button", i), dup=True)
                else:
                    st["last_click"] = (i, now)
                    queue.add(("pick", i), dup=True)

            return handler

        # Clears the window state when the gump is disposed, whoever disposed it.
        on_disposed = Kit.disposer("skills.window", st, win)

        def redraw():
            """Asks for the window to be rebuilt on the next tick."""
            st["rebuild"] = "window"

        def setp(ctrl, attr, value):
            """Sets a control's property only when it differs from the last value set. Used for every row part.

            The cache is keyed by the control itself: id() of a client object is a slow lookup in
            IronPython, and this runs for every part of every row on every refresh. Width and Pos go through
            Kit helpers, and are scaled when the window is drawn smaller in a zone.
            """
            if ctrl is None:
                return
            k = (ctrl, attr)
            if UIC.get(k) == value:
                return
            UIC[k] = value
            # No safe(lambda) here: this is the hottest call of the module.
            try:
                # The scale the window is drawn at in a zone (1.0 otherwise).
                zk = fitst["k"]
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
            """Notes the value a control was made with, so setp skips the first set."""
            UIC[(ctrl, attr)] = value

        def cap_w(caption):
            """The width of a button with this caption: its art plus the text."""
            return 35 + Kit.text_w(caption)

        def metrics(IW=None, zone=False):
            """Returns the column places of the skill list for an inside width IW.

            Without IW, the places last worked out (or the natural ones). With IW, whatever is left past the
            natural width goes to the name column and (up to BAR_GROW) to the progress bars. In a zone the
            list must fit IW whatever it is: the progress bar, Gain, Cap and Real are given up in that order
            (the player's column settings are untouched), then the name column takes the cut and the names
            are cut (m["cut"]). The result is cached by width and zone flag.
            """
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
                # Still too wide after the columns were given up: the names give way.
                if short > 0:
                    cut = min(short, m["name_w"] - ZONE_NAME_MIN)
                    if cut > 0:
                        widen(m, -cut)
                        m["cut"] = True
                m["drop"] = tuple(drop)
            m["zone"] = zone
            # Room past the natural width, to be shared between the bars and the name column.
            extra = max(0, IW - (m["sa_w"] + 16)) if IW else 0
            if extra:
                # The bars take two fifths of the extra, to a maximum of BAR_GROW.
                bar_extra = min(BAR_GROW, extra * 2 // 5) if m["bar_x"] is not None else 0
                if bar_extra:
                    m["bar_w"] += bar_extra
                    for key in ("gain_x", "lock_x"):
                        if m[key] is not None and m[key] > m["bar_x"]:
                            m[key] += bar_extra
                widen(m, extra - bar_extra)
            m["IW"] = IW
            st["m"] = m
            return m

        def widen(m, d):
            """Moves the name column's right edge by d pixels and shifts every column after it."""
            m["name_w"] += d
            for key in ("real_x", "val_x", "cap_x", "bar_x", "gain_x", "lock_x"):
                if m[key] is not None:
                    m[key] += d
            m["row_w"] = m["lock_x"] + m["lock_w"] + 6
            m["sa_w"] = m["row_w"] + 16

        def natural_metrics(drop=()):
            """Returns the column places at the window's natural width, nothing spread.

            drop names the columns left out in a zone (bar, gain, cap, real). A column the player turned off
            has None for its place. Texts are measured from the real font so the columns fit it.
            """
            m = {"cut": False, "drop": ()}
            names = SK["names"] or FALLBACK_NAMES
            # The arrow and gem widths come from the client's art; the numbers are fallbacks.
            arrow_w = Kit.pic_size(LOCK_ART[0])[0] or 10
            m["arrow_w"] = arrow_w
            m["lock_w"] = max(arrow_w, Kit.pic_size(LOCK_ART[2])[0] or 12)
            gem_w = Kit.pic_size(GEM[0])[0] or 11
            m["name_x"] = 4 + gem_w + 6
            m["name_w"] = (max([Kit.text_w(n) for n in names] + [Kit.text_w("Skill") + arrow_w + 4]) + 10)
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
                # None means this column is off.
                m[key] = x if on else None
                if on:
                    x += cw
            m["lock_x"] = x
            m["row_w"] = x + m["lock_w"] + 6
            # The scroll area is a scrollbar's gutter wider than the row.
            m["sa_w"] = m["row_w"] + 16
            return m

        def row_h():
            """Return the height of one list row in pixels: ROW_H, or a little less in compact mode (Kit.pitch).

            Every row position and every row count in the window is worked out from this, never from ROW_H.
            """
            return Kit.pitch(ROW_H)

        def detail_rows():
            """The number of rows in the picked skill's details: five, six with the training tip."""
            return 6 if settings["tips"] else 5

        def layout():
            """Works out every section's place for the full window at its natural size or its dragged size.

            Returns a dict: IW, W, H, a (y, height) per section, rows, and the limits the corner drag works
            with: min_w, min_h and fixed_h (the height of everything but the list's rows, which apply_resize
            turns a height back into rows with). A window taller than the screen has fewer rows. Heights use
            row_h(), so compact mode fits more rows in the same space.
            """
            M, GAP = Kit.MARGIN, Kit.GAP
            m = natural_metrics()
            sw, sh = Kit.screen()
            # The inside width must fit every section's widest line: tool row, lock buttons, detail buttons
            # and stats.
            tool_need = 12 + Kit.text_w("Find:") + 6 + SEARCH_W + 14 + \
                cap_w(max((f[1] for f in FILTERS), key=Kit.text_w)) + 12 + 24 + Kit.text_w("Groups") + 12
            locks_need = 12 + sum(cap_w(c) for c in ZLOCKS) + 3 * 10 + 12
            detail_need = 12 + cap_w("Use") + 12 + cap_w("Make button") + 12 + cap_w("Next group") + 12
            aw = Kit.pic_size(LOCK_ART[2])[0] or 12
            stats_need = 12 + 3 * (Kit.text_w("Int 125 (+25)") + 8 + aw + 14) + \
                Kit.text_w("Stats 225 / 225") + 12 if settings["sec_stats"] else 0
            IW = max(m["sa_w"] + 16, tool_need, locks_need, detail_need, stats_need, MIN_IW)
            min_w = IW + 2 * M
            if eff_width() > min_w:
                IW = eff_width() - 2 * M
            # Never wider than the screen.
            if sw:
                IW = max(min_w - 2 * M, min(IW, sw - 2 * M - 10))
            m = metrics(IW)
            L = {"IW": IW, "W": IW + 2 * M, "min_w": min_w}
            y = M + 30 + GAP
            n_sum = (2 if settings["sec_summary"] else 0) + (1 if settings["sec_stats"] else 0)
            rows = settings["rows"] if fitst["rows"] is None else fitst["rows"]
            # (section, shown, height) from top to bottom. The list is the one whose height depends on rows.
            for key, on, hh in (("sum", n_sum, 6 + 24 * n_sum + 4), ("tool", True, 36),
                                ("list", True, 26 + rows * row_h() + 6), ("locks", settings["sec_locks"], 36),
                                ("detail", settings["sec_detail"], 6 + 24 * detail_rows() + 4),
                                ("log", settings["sec_log"], 26 + 20 * settings["log_lines"] + 4)):
                if on:
                    L[key] = (y, hh)
                    y += hh + GAP
            L["H"] = y - GAP + M
            L["fixed_h"] = L["H"] - rows * row_h()
            lo = LIMITS["rows"][0]
            L["min_h"] = L["fixed_h"] + lo * row_h()
            # Taller than the screen: fewer rows, and every section below the list moves up.
            if sh and L["H"] > sh - 10 and rows > lo:
                fit_rows = max(lo, (sh - 10 - L["fixed_h"]) // row_h())
                if fit_rows < rows:
                    shrink = (rows - fit_rows) * row_h()
                    L["list"] = (L["list"][0], L["list"][1] - shrink)
                    for key in ("locks", "detail", "log"):
                        if key in L:
                            L[key] = (L[key][0] - shrink, L[key][1])
                    L["H"] -= shrink
                    L["rows"] = fit_rows
                    return L
            L["rows"] = rows
            return L

        ZLOCKS = tuple(b[1] for b in LOCK_BTNS)

        def zflow(widths, gap, IW):
            """Places (x, line) of items `widths` wide in a section IW wide, flowing from 12 px in, `gap` apart.

            An item that would pass 12 px from the right edge starts the next line. Also returns the number
            of lines used.
            """
            out, x, line = [], 12, 0
            for cw in widths:
                if x > 12 and x + cw > IW - 12:
                    x, line = 12, line + 1
                out.append((x, line))
                x += cw + gap
            return out, line + 1

        def zone_min_w():
            """The narrowest width every row of the window in a zone can flow at.

            The list with its columns given up and names cut, the search row wrapped, the buttons one a
            line. A slot narrower than this is drawn smaller.
            """
            nm = natural_metrics(ZONE_DROPS)
            need = [nm["sa_w"] - max(0, nm["name_w"] - ZONE_NAME_MIN) + 16,
                    12 + Kit.text_w("Find:") + 6 + ZONE_FIELD_MIN + 2 + 12,
                    12 + cap_w(max((f[1] for f in FILTERS), key=Kit.text_w)) + 12, 12 + 24 + Kit.text_w("Groups") + 12]
            if settings["sec_summary"]:
                need += [12 + Kit.text_w("Session +99.9") + 12, 12 + cap_w("Reset") + 12]
            if settings["sec_stats"]:
                need.append(12 + Kit.text_w("Int 125 (+25)") + 8 + (Kit.pic_size(LOCK_ART[2])[0] or 12) + 4)
            if settings["sec_locks"]:
                need.append(12 + max(cap_w(t) for t in ZLOCKS) + 12)
            if settings["sec_detail"]:
                aw = max(Kit.pic_size(a)[0] for a in LOCK_ART) or 12
                need += [12 + ZONE_NAME_MIN + 8 + 3 * (aw + 10) + 12,
                         12 + Kit.text_w("Target:") + 8 + 56 + 12 + Kit.text_w("none set") + 4,
                         12 + max(cap_w("Make button"), cap_w("Next group")) + 12]
            return max(need) + 2 * Kit.MARGIN

        def zone_plan(w, h):
            """Works out every section's place for a window laid out w by h pixels in a zone.

            Returns a dict like layout()'s, plus: stats, T (the search row), locks_p and D (the details)
            with the places the sections use, total2 and sess_own for lines that wrapped, rows (the list's
            whole rows of row_h(); the pixels left over go to its section), log_n, need (the height with
            ZONE_MIN_ROWS rows and ZONE_LOG_MIN log lines) and short (fewer rows than that fit). Layout
            pixels, before scaling.
            """
            M, GAP = Kit.MARGIN, Kit.GAP
            IW = w - 2 * M
            Z = {"IW": IW, "W": w, "H": h}
            secs = []
            # Section heights are counted in 24 px lines; each section grows with the lines that wrapped.
            n_sum = 0
            # Totals and session: the total line may take two lines and the session line its own line when
            # they do not fit beside Reset.
            if settings["sec_summary"]:
                cap = f1(settings["total_cap"])
                one = "Total %s / %s   (%s free)   with bonuses %s" % (cap, cap, cap, cap)
                Z["total2"] = Kit.text_w(one) > IW - 24
                rx = IW - 12 - cap_w("Reset")
                Z["sess_own"] = rx - 12 - 6 < Kit.text_w("Session +99.9")
                n_sum += (2 if Z["total2"] else 1) + (2 if Z["sess_own"] else 1)
            # The stats: three entries flow like words and the total follows.
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
            # The search row is one to three lines depending on what fits.
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
            # The list takes the rest: its height is decided below.
            secs.append(("list", None))
            if settings["sec_locks"]:
                Z["locks_p"], n = zflow([cap_w(t) for t in ZLOCKS], 10, IW)
                secs.append(("locks", 36 + 26 * (n - 1)))
            # The picked skill: Pin moves beside the target box when there is room, else it joins the buttons.
            if settings["sec_detail"]:
                tx = 12 + Kit.text_w("Target:") + 8
                tgt_x = tx + 56 + 12
                pin_x = IW - 12 - cap_w("Unpin")
                pin_here = pin_x - tgt_x - 6 >= Kit.text_w("none set")
                keys = ["use", "button"] + ([] if pin_here else ["pin"]) + ["nextgrp"]
                caps = {"use": "Use", "button": "Make button", "pin": "Unpin", "nextgrp": "Next group"}
                places, nb = zflow([cap_w(caps[kk]) for kk in keys], 12, IW)
                if nb == 1:
                    places[-1] = (IW - 12 - cap_w("Next group"), 0)
                Z["D"] = {"tx": tx, "tgt_x": tgt_x, "pin_here": pin_here, "pin_x": pin_x,
                          "tgt_w": (pin_x - 6 if pin_here else IW - 4) - tgt_x, "btns": list(zip(keys, places))}
                secs.append(("detail", 6 + 24 * (detail_rows() + nb) + 4))
            n_log = settings["log_lines"] if settings["sec_log"] else 0
            if settings["sec_log"]:
                secs.append(("log", None))

            def height(rows, logn):
                """Height of the whole window with a given number of list rows (of row_h() each) and log lines."""
                y = M + 30 + GAP
                for key, hh in secs:
                    if key == "list":
                        hh = 26 + rows * row_h() + 6
                    elif key == "log":
                        hh = 26 + 20 * logn + 4
                    y += hh + GAP
                return y - GAP + M

            lo = LIMITS["rows"][0]
            rows = (h - height(0, n_log)) // row_h()
            while rows < lo and n_log > ZONE_LOG_MIN:
                n_log -= 1
                rows = (h - height(0, n_log)) // row_h()
            Z["need"] = height(ZONE_MIN_ROWS, min(n_log, ZONE_LOG_MIN) if settings["sec_log"] else 0)
            Z["short"] = rows < ZONE_MIN_ROWS
            rows = max(1, rows)
            Z["rows"], Z["log_n"] = rows, n_log
            list_h = max(26 + rows * row_h() + 6, h - height(0, n_log) + 32)
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
            """Returns (lw, lh, k, Z) for a w by h slot: the layout size, the scale drawn at, and the plan.

            A slot narrower than zone_min_w, or too short for ZONE_MIN_ROWS rows, is laid out bigger and
            drawn smaller (lw times k is w). The loop settles on a scale where the plan fits.
            """
            mw = zone_min_w()
            k = 1.0 if w >= mw else w / float(mw)
            lw, lh, Z = w, h, None
            # Shrinking the scale changes the layout width, so plan again; four passes are enough in practice.
            for _ in range(4):
                lw = w if k == 1.0 else max(mw, int(round(w / k)))
                lh = h if k == 1.0 else int(round(h / k))
                Z = zone_plan(lw, lh)
                if not Z["short"]:
                    break
                k = min(k, h / float(Z["need"]) * 0.999)
            return lw, lh, k, Z

        def fit_set(c, key, txt, room, hue=None, base=None, lbl=None):
            """Shows txt cut to room pixels in label c[key] (or lbl), and keeps the whole text as a tooltip.

            With a catcher c[key + "_cat"] (in a zone) the whole text is its tooltip while it is cut, after
            the area's own tooltip base if there is one. Nothing happens when the inputs are unchanged since
            the last call.
            """
            if lbl is None:
                lbl = c.get(key)
            if lbl is None:
                return
            # The key of what was last shown: nothing new, no fit and no set.
            src = (txt, room, hue, base)
            sk = key + "_src"
            if c.get(sk) == src:
                return
            c[sk] = src
            shown = Kit.fit(txt, room)
            Kit.set_text(lbl, shown, hue)
            cat = c.get(key + "_cat")
            if cat is None:
                return
            tip = base or "" if shown == txt else (("%s. %s" % (txt, base)) if base else txt)
            if tip != c.get(key + "_tip"):
                c[key + "_tip"] = tip
                safe(lambda: cat.SetTooltip(tip))

        def plain_plan(L):
            """Builds the plan for the plain window (not in a zone) in the same shape zone_plan returns.

            The plain window lays its sections out at fixed places, so the plan only carries the places the
            builder asks for.
            """
            IW = L["IW"]
            Z = dict(L, total2=False, sess_own=False, log_n=settings["log_lines"])
            step = Kit.text_w("Int 125 (+25)") + 8 + (Kit.pic_size(LOCK_ART[2])[0] or 12) + 14
            Z["stats"] = ([(12 + j * step, 0) for j in range(3)], (12 + 3 * step, 0))
            tx = 12 + Kit.text_w("Find:") + 6
            Z["T"] = {"tx": tx, "field": SEARCH_W, "filter": (tx + SEARCH_W + 14, 0),
                      "groups": (IW - 12 - 24 - Kit.text_w("Groups"), 0)}
            Z["locks_p"] = zflow([cap_w(t) for t in ZLOCKS], 10, IW)[0]
            tx = 12 + Kit.text_w("Target:") + 8
            pin_x = IW - 12 - cap_w("Unpin")
            Z["D"] = {"tx": tx, "tgt_x": tx + 68, "pin_here": True, "pin_x": pin_x, "tgt_w": pin_x - 6 - (tx + 68),
                      "btns": [("use", (12, 0)), ("button", (24 + cap_w("Use"), 0)),
                               ("nextgrp", (IW - 12 - cap_w("Next group"), 0))]}
            return Z

        def build_zone(g, store, c, Z, k, zone=True):
            """Builds the sections of the window from a plan, at scale k (only the text fields need it).

            zone True: the labels get tooltip catchers so cut texts can be read. False: the plain window.
            The text fields are the exception to scaling: the client never scales a field's text, so their
            font size follows k.
            """
            M = Kit.MARGIN
            IW = Z["IW"]
            x0 = M
            metrics(IW, zone=zone)

            def zlabel(key, x, y, w, hue=None, h=22, dy=0):
                """Makes a label and, in a zone, a catcher over it that carries the full text as a tooltip."""
                lbl = Kit.add_label(g, "", x, y, hue)
                if zone:
                    c[key + "_cat"] = Kit.catcher(g, x - 2, y + dy - 3, max(8, w + 4), h, lambda: None)
                    c[key + "_tip"] = ""
                return lbl

            # The totals and session section.
            if "sum" in Z:
                y0, hh = Z["sum"]
                Kit.add_section(g, x0, y0, IW, hh)
                ry = y0 + 6
                if settings["sec_summary"]:
                    nl = 2 if Z["total2"] else 1
                    c["total"] = Kit.add_label(g, "", x0 + 12, ry + 3)
                    cat = Kit.catcher(g, x0 + 8, ry, IW - 16, 24 * nl - 2, lambda: None, TOTAL_TIP)
                    if zone:
                        c["total_cat"], c["total_tip"] = cat, TOTAL_TIP
                    ry += 24
                    if Z["total2"]:
                        c["total2"] = Kit.add_label(g, "", x0 + 12, ry + 3)
                        ry += 24
                    rx = x0 + IW - 12 - cap_w("Reset")
                    c["session_w"] = IW - 28 if Z["sess_own"] else rx - x0 - 12 - 6
                    c["session"] = zlabel("session", x0 + 12, ry + 3, c["session_w"])
                    if Z["sess_own"]:
                        ry += 24
                    Kit.art_button(g, store, "newsess", Kit.ART_CLOSE, rx, ry - 1, "Reset",
                                   "New session: gains count from now", on_click=queue("newsess"))
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
                            Kit.on_click(pic, queue(("stat", j), dup=True))
                            Kit.with_tip(pic, "Click: %s up, down or locked" % nm)
                        c["stats"].append((lbl, pic))
                    c["stat_total_w"] = IW - 4 - tx
                    c["stat_total"] = zlabel("stat_total", x0 + tx, ry + 24 * tl + 3, c["stat_total_w"], Kit.HUE_INFO)
            # The search row.
            y0, hh = Z["tool"]
            T = Z["T"]
            Kit.add_section(g, x0, y0, IW, hh)
            Kit.add_label(g, "Find:", x0 + 12, y0 + 10)
            c["search"] = Kit.with_tip(Kit.add_textbox(g, st["search"], x0 + T["tx"], y0 + 7, T["field"], numbers=False,
                                                       font=max(8, int(round(16 * k)))), "Type part of a skill name")
            c["search"].SetPlaceholder("search")
            fx, fl = T["filter"]
            c["filter"] = Kit.art_button(g, store, "filter", Kit.ART_PAGE, x0 + fx, y0 + 7 + 28 * fl,
                                         FILTERS[settings["filter"]][1], "Which skills to list (click: next)",
                                         on_click=queue("filter"))
            gx, gl = T["groups"]
            c["groups"] = Kit.add_check(g, "Groups", x0 + gx, y0 + 9 + 28 * gl, settings["groups"],
                                        "Show the client's skill groups (click one to fold it)")
            # The list.
            build_list(g, c, x0, Z["list"][0], IW, Z["list"][1], Z["rows"])
            # The lock buttons.
            if "locks" in Z:
                y0, hh = Z["locks"]
                Kit.add_section(g, x0, y0, IW, hh)
                for (key, cap, tip), (bx, ln) in zip(LOCK_BTNS, Z["locks_p"]):
                    Kit.art_button(g, store, key, Kit.ART_OK, x0 + bx, y0 + 7 + 26 * ln, cap, tip, on_click=queue(key))
            # The picked skill's details.
            if "detail" in Z:
                y0, hh = Z["detail"]
                D = Z["D"]
                Kit.add_section(g, x0, y0, IW, hh)
                ry = y0 + 6
                aw = max(Kit.pic_size(a)[0] for a in LOCK_ART) or 12
                lx = x0 + IW - 12 - 3 * (aw + 10)
                c["d_name_w"] = lx - x0 - 12 - 8
                c["d_locks"] = []
                c["d_name"] = zlabel("d_name", x0 + 12, ry + 3, c["d_name_w"], Kit.HUE_TITLE)
                for v in range(3):
                    p = Kit.add_pic(g, LOCK_ART[v], lx + v * (aw + 10), ry + 5)
                    if p is not None:
                        Kit.on_click(p, queue(("dlock", v), dup=True))
                        Kit.with_tip(p, LOCK_SET[v])
                    c["d_locks"].append(p)
                ry += 24
                c["d_lw"] = IW - 28
                c["d_l1"] = zlabel("d_l1", x0 + 12, ry + 3, c["d_lw"])
                ry += 24
                c["d_l2"] = zlabel("d_l2", x0 + 12, ry + 3, c["d_lw"], Kit.HUE_INFO)
                ry += 24
                if settings["tips"]:
                    c["d_tip"] = Kit.add_label(g, "", x0 + 12, ry + 3, Kit.HUE_TEXT)
                    c["d_tip_cat"] = Kit.catcher(g, x0 + 8, ry, IW - 16, 22, lambda: None,
                                                 "Training tip for this skill's range")
                    c["d_tip_full"] = None
                    ry += 24
                Kit.add_label(g, "Target:", x0 + 12, ry + 3)
                c["target"] = Kit.with_tip(Kit.add_textbox(g, "", x0 + D["tx"], ry, 56, numbers=False,
                                                           font=max(8, int(round(16 * k)))),
                                           "Real value to stop at (empty = none)")
                c["target"].SetPlaceholder("none")
                c["d_tgt_w"] = D["tgt_w"]
                c["d_tgt"] = zlabel("d_tgt", x0 + D["tgt_x"], ry + 3, D["tgt_w"], Kit.HUE_INFO)
                ry += 24
                for key, (bx, ln) in ([("pin", (D["pin_x"], -1))] if D["pin_here"] else []) + D["btns"]:
                    art, cap, tip, act = DETAIL_BTNS[key]
                    b = Kit.art_button(g, store, key, art, x0 + bx, ry - 1 + 24 * ln, cap, tip, on_click=queue(act))
                    if key == "pin":
                        c["pin"] = b
            # The log.
            if "log" in Z:
                y0, hh = Z["log"]
                Kit.add_section(g, x0, y0, IW, hh, "RECENT GAINS")
                c["log"] = []
                c["log_w"] = IW - 28
                for j in range(Z["log_n"]):
                    c["log"].append(zlabel("log%d" % j, x0 + 12, y0 + 26 + 20 * j, c["log_w"], Kit.HUE_TEXT, 20, 1))

        def back_by():
            """Return where the player gets a hidden Skills window back from, as text for tooltips and journal lines."""
            return ("the client's or the Action Bar's Skills button" if settings["replace"]
                    else "the Action Bar's Skills button")

        def close_tip():
            """The Close button's tooltip: with x_hides on, it only hides the window."""
            if settings["x_hides"]:
                return "Hide %s (%s brings it back)" % (TITLE, back_by())
            return Kit.CLOSE_TIP % TITLE

        def build_window():
            """Builds the window from nothing and disposes the old one.

            Picks the form: the minimized bar, the zone form (its slot exactly, drawn smaller if need be) or
            the plain window, which has a corner drag. Keeps its place across rebuilds, or takes the
            layout's remembered spot (LAYOUT.spot) when the layout holds the window. Then shows the target
            text, reads the groups, works the rows out and fills the texts. Client thread, from the tick.
            """
            old, win["g"] = win["g"], None
            UIC.clear()
            st["desc"] = None
            st["rebuild"] = None
            # Hidden by its X: nothing to build; the Action Bar's button shows it again.
            if st["hidden"]:
                win.update({"c": {}, "rows": [], "rowmap": {}, "store": ({}, {})})
                Kit.dispose(old)
                return
            store = ({}, {})
            c = {}
            st["resize_at"], st["preview"] = 0.0, False
            win["L"] = None
            L, Z = None, None
            fitst["k"], fitst["full"] = 1.0, None
            if st["minimized"] or st["docked"]:
                w, h = MINI_W, MINI_H
            elif fitst["slot"] is not None:
                w, h = fitst["slot"]
                lw, lh, k, Z = zone_geom(w, h)
            else:
                L = layout()
                w, h = L["W"], L["H"]
                win["L"] = L
            x, y = Kit.load_pos(POS_KEY, (160, 120), (w, h))
            if Kit.is_open(old):
                x, y = old.GetX(), old.GetY()
            at = LAYOUT.spot(KEY) if HOST.layout_holds(KEY) else None
            if at is not None:
                x, y = int(at[0]), int(at[1])
            if Z is not None:
                g = G.CreateGump(True, True)
                Kit.add_window_frame(g, lw, lh)
                Kit.title_bar(g, store, lw, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"), close_tip=close_tip())
                build_zone(g, store, c, Z, k)
                if k != 1.0:
                    wf = max(zone_min_w(), w)
                    fitst["k"], fitst["full"] = k, (int(wf), int(zone_plan(wf, 0)["need"]))
                    Kit.scale_window(g, k)
            elif L is None:
                g = G.CreateGump(True, True)
                c["mini"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"), close_tip=close_tip())
            else:
                if at is None:
                    x, y = Kit.clamp(x, y, w, h)
                g = G.CreateModernGump(x, y, w, h, True, L["min_w"], L["min_h"], on_resized)
                # Fully transparent: the panel under the frame is the visible window and the real one is only the
                # resize handle. A corner drag shows it as a preview (see on_resized).
                g.SetAlpha(0)
                Kit.add_window_frame(g, w, h, mouse=False)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"), close_tip=close_tip())
                build_zone(g, store, c, plain_plan(L), 1.0, False)
            xy = Kit.show_window(g, x, y, w, h, KEY, st["docked"], on_disposed(g), save_pos, win,
                                 {"g": g, "c": c, "store": store, "rows": [], "rowmap": {},
                                  "w": lw if Z is not None else w})
            # The client may have moved it; put it back where the layout wants it.
            if at is not None and xy is not None and tuple(xy) != (x, y):
                g.SetPos(x, y)
                Kit.note_rect(g, x, y)
                Kit.moved_by_code(g)
            if at is not None:
                LAYOUT.fit_now(KEY, g)
            if settings["minimized"] != st["minimized"]:
                settings["minimized"] = st["minimized"]
                save_settings()
            show_target_text()
            read_groups()
            rebuild_rows(time.time())
            refresh(time.time())
            Kit.dispose(old)

        wnd = None
        hooks = Kit.dock_hooks(TITLE, DOCK_ICON, st, win, redraw)

        def on_resized(*args):
            """A step of a corner drag from the client, about every 75 ms: shows the window as a preview.

            The window's own panel shows meanwhile as a preview of the new size. The layout follows once
            the drag has settled (see apply_resize).
            """
            st["resize_at"] = time.time()
            g = win["g"]
            L = win.get("L")
            if st["preview"] or L is None or not Kit.is_open(g) or st["minimized"] or st["docked"]:
                return
            # In a zone the layout sizes the window, so a drag does nothing. Only a real change of size shows
            # the preview: a client that reports the initial size too would flash it.
            if fitst["width"] is None and (int(g.GetWidth()), int(g.GetHeight())) != (L["W"], L["H"]):
                st["preview"] = True
                g.SetAlpha(0.55)

        def apply_resize():
            """The corner drag was let go: turns the dragged size into settings and draws the window again.

            The dragged height sets the rows of the list (height over row_h(), rounded), the width spreads
            the columns; both are saved with the settings, shown on the settings page, and the window is
            rebuilt at that size.
            """
            g = win["g"]
            L = win.get("L")
            st["preview"] = False
            if L is None or not Kit.is_open(g) or st["minimized"] or st["docked"]:
                return
            # Fitted to a zone: the zone has the width.
            if fitst["width"] is not None:
                g.SetAlpha(0)
                return
            w, h = int(g.GetWidth()), int(g.GetHeight())
            lo, hi = LIMITS["rows"]
            rows = max(lo, min(hi, (h - L["fixed_h"] + row_h() // 2) // row_h()))
            # At its narrowest the width is natural (0).
            width = w if w > L["min_w"] else 0
            # A drag that changed nothing: hide the preview again.
            if rows == L["rows"] and width == settings["width"] and (w, h) == (L["W"], L["H"]):
                g.SetAlpha(0)
                return
            if rows != settings["rows"] or width != settings["width"]:
                settings["rows"], settings["width"] = rows, width
                save_settings()
                page["sync"] = True
            st["m"] = None
            st["rebuild"] = "window"
            touch()

        def build_list(g, c, x0, y0, IW, h, rows):
            """Builds the list's header and scroll area; the rows are made later by rebuild_rows.

            Each header label has a catcher over it that sorts by that column (again to reverse); the lock
            column has its own arrow. A column the player turned off has no header. The scroll area is
            rows times row_h() high. Sets the row cap: while the host is still booting only the visible rows
            plus ROW_SPARE are made, so the window appears quickly; otherwise every row is allowed.
            """
            m = metrics()
            Kit.add_section(g, x0, y0, IW, h)
            sx = x0 + 8
            c["hdr"] = {}
            heads = [("name", "Skill", m["name_x"], "Sort by name"),
                     ("real", "Real", m["real_x"], "Sort by real value without item bonuses"),
                     ("value", "Value", m["val_x"], "Sort by value with bonuses"),
                     ("cap", "Cap", m["cap_x"], "Sort by cap"),
                     ("gain", "Gain", m["gain_x"], "Sort by gain this session")]
            nxt = {"name": m["real_x"] or m["val_x"], "real": m["val_x"], "value": m["cap_x"] or m["bar_x"]
                   or m["gain_x"] or m["lock_x"], "cap": m["bar_x"] or m["gain_x"] or m["lock_x"], "gain": m["lock_x"]}
            for key, text, cx, tip in heads:
                if cx is None:
                    continue
                c["hdr"][key] = Kit.add_label(g, text, sx + cx, y0 + 6, Kit.HUE_INFO)
                Kit.catcher(g, sx + cx - 2, y0 + 3, (nxt[key] or cx + 40) - cx - 2, 20,
                            queue(("sort", key), dup=True), tip + " (again to reverse)")
            lp = Kit.add_pic(g, LOCK_ART[2], sx + m["lock_x"], y0 + 7)
            if lp is not None:
                Kit.on_click(lp, queue(("sort", "lock"), dup=True))
                Kit.with_tip(lp, "Sort by lock (again to reverse)")
            c["hdr"]["lock_pic"] = lp
            c["arrow"] = Kit.add_pic(g, LOCK_ART[1], sx, y0 + 8, mouse=False)
            c["sa"] = G.CreateGumpScrollArea(sx, y0 + 26, m["sa_w"], rows * row_h())
            g.Add(c["sa"])
            # During boot, build only the rows that show (grow_rows adds the rest a chunk at a time).
            boot = safe(HOST.booting, False)
            c["sa_xy"] = (sx, y0 + 26)
            c["more"] = False
            c["cap"] = rows + ROW_SPARE if boot else LIMITS["rows"][1] + 999
            c["grow_at"] = time.time() + ROW_WAIT

        def move_row(r, y):
            """Moves every part of row r to y, scaled when the window is drawn smaller."""
            if r["y"] == y:
                return
            r["y"] = y
            zk = fitst["k"]
            for ctl, x, dy in r["parts"]:
                try:
                    if zk == 1.0:
                        Kit.ui_pos(ctl, x, y + dy)
                    else:
                        ctl.SetPos(int(round(x * zk)), int(round((y + dy) * zk)))
                except Exception:
                    pass

        def show_row(r, on):
            """Shows or hides every part of row r. A shown row's texts are redone on the next refresh."""
            if r["hidden"] == (not on):
                return
            r["hidden"] = not on
            for ctl, _, _ in r["parts"]:
                # The progress bar is only hidden here; refresh_rows shows it when it has a width.
                if ctl is r.get("bar"):
                    if not on:
                        setp(ctl, "IsVisible", False)
                else:
                    setp(ctl, "IsVisible", on)
            if on:
                r["sig"] = None

        def rebuild_rows(now):
            """Puts the rows in the order (and selection) the list shows now.

            The list is worked out again only when something it depends on changed (see touch) or, with the
            gaining filter, once a second. Rows are made when first needed and then reused: moved, shown or
            hidden, never destroyed. Row y positions are the row's index times row_h(). Rows past the cap are
            left unmade and flagged in c["more"] for grow_rows, except the selected skill, which is always made.
            """
            c = win["c"]
            if "sa_xy" not in c:
                return
            # What the order depends on: the touch counter, the group counter and, for gaining, the second.
            key = (st["ver"], GR["ver"], int(now) if FILTERS[settings["filter"]][0] == "gaining" else 0)
            if st["desc"] is not None and key == st["desc_key"]:
                return
            st["desc_key"] = key
            desc = descriptors(now)
            if desc == st["desc"]:
                return
            st["desc"] = desc
            m = metrics()
            tgt = c["sa"]
            # How many controls exist now, to tell later whether the scaled window needs scaling again.
            made = len(win["rowmap"]) + (0 if "selbox" in c else 1) + (0 if c.get("empty") else 1)
            # Made first, so it is drawn under the rows.
            if "selbox" not in c:
                c["selbox"] = Kit.add_box(tgt, 0, 0, m["row_w"], row_h() - 1, SEL_ALPHA, SEL_COLOR)
                setp(c["selbox"], "IsVisible", False)
            empty = "" if desc else ("No skill matches; change the search or the filter."
                                     if SK["n"] else "Waiting for the server to send your skills.")
            if c.get("empty") is None and empty:
                c["empty"] = Kit.add_label(tgt, empty, m["name_x"], 3, Kit.HUE_INFO)
            if c.get("empty") is not None:
                Kit.set_text(c["empty"], empty)
                setp(c["empty"], "IsVisible", bool(empty))
            rowmap = win["rowmap"]
            rows, want, nth = [], set(), {}
            rh = row_h()
            c["more"] = False
            for n, d in enumerate(desc):
                ry = n * rh
                k = (d[0], d[1])
                # A pinned skill is listed twice with groups on (under Pinned and in its own group), so a row is
                # keyed by its kind, key and how many times that key came before.
                nth[k] = c_k = nth.get(k, -1) + 1
                k = (d[0], d[1], c_k)
                r = rowmap.get(k)
                # Past the cap: leave the row for a later pass; only the selected skill is made regardless.
                if r is None and n >= c["cap"] and (d[0] == "g" or d[1] != st["sel"]):
                    c["more"] = True
                    continue
                if r is None:
                    r = build_group_row(tgt, ry, d, m) if d[0] == "g" else build_skill_row(tgt, ry, d[1], m)
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
                    move_row(r, 0)
            win["rows"] = rows
            # New controls were made in a window that is drawn smaller: scale them too.
            if fitst["k"] != 1.0 and made != len(rowmap) + (0 if "selbox" in c else 1) + (0 if c.get("empty") else 1):
                Kit.scale_window(win["g"], fitst["k"])
            place_selbox()

        def grow_rows(now):
            """Make the next ROW_CHUNK rows of a list that still has unmade rows, then redraw and refresh them.

            Called from the tick. While booting it waits until c["grow_at"] (ROW_WAIT seconds after the list was
            built) so the first rows are not slowed; once the host has settled it goes at once.
            """
            c = win["c"]
            if not c.get("more") or (now < c["grow_at"] and safe(HOST.booting, False)):
                return
            c["cap"] += ROW_CHUNK
            st["desc"] = None
            rebuild_rows(now)
            refresh_rows(now)

        def put(r, ctl, x, dy):
            """Adds control ctl to row r's parts (with its x and y offset) and returns it."""
            if ctl is not None:
                r["parts"].append((ctl, x, dy))
            return ctl

        def build_group_row(tgt, ry, d, m):
            """Builds a group header row: arrow, name and totals, with a catcher that folds it.

            The row's boxes are row_h() tall, so they follow compact mode.
            """
            key, shut = d[1], d[2]
            r = {"kind": "g", "key": key, "y": ry, "hidden": False, "parts": [], "sig": None}
            put(r, Kit.add_box(tgt, 0, ry + 1, m["row_w"], row_h() - 2, GROUP_ALPHA, GROUP_COLOR), 0, 1)
            r["arrow"] = put(r, Kit.add_pic(tgt, GROUP_SHUT if shut else GROUP_OPEN, 4, ry + 5, mouse=False), 4, 5)
            remember(r["arrow"], "Graphic", GROUP_SHUT if shut else GROUP_OPEN)
            r["lbl"] = put(r, Kit.add_label(tgt, "", m["name_x"], ry + 3, Kit.HUE_TITLE), m["name_x"], 3)
            r["real"] = put(r, Kit.add_label(tgt, "", m["real_x"], ry + 3, Kit.HUE_INFO),
                            m["real_x"], 3) if m["real_x"] is not None else None
            r["val"] = put(r, Kit.add_label(tgt, "", m["val_x"], ry + 3, Kit.HUE_INFO), m["val_x"], 3)
            r["gain"] = put(r, Kit.add_label(tgt, "", m["gain_x"], ry + 3, Kit.HUE_INFO),
                            m["gain_x"], 3) if m["gain_x"] is not None else None
            put(r, Kit.catcher(tgt, 0, ry, m["row_w"], row_h() - 1, queue(("fold", key), dup=True),
                            "Fold or unfold this group"), 0, 0)
            return r

        def build_skill_row(tgt, ry, i, m):
            """Builds the parts of one skill row: name, columns, progress bar, use gem, lock arrow and catcher.

            The progress bar is centred in the row's height (row_h()) and the catcher covers the name area.
            """
            r = {"kind": "s", "i": i, "y": ry, "hidden": False, "parts": [], "sig": None}
            r["name"] = put(r, Kit.add_label(tgt, row_name(i, m), m["name_x"], ry + 3), m["name_x"], 3)
            r["real"] = put(r, Kit.add_label(tgt, "", m["real_x"], ry + 3), m["real_x"], 3) \
                if m["real_x"] is not None else None
            r["val"] = put(r, Kit.add_label(tgt, "", m["val_x"], ry + 3), m["val_x"], 3)
            r["cap"] = put(r, Kit.add_label(tgt, "", m["cap_x"], ry + 3, Kit.HUE_INFO),
                           m["cap_x"], 3) if m["cap_x"] is not None else None
            r["gain"] = put(r, Kit.add_label(tgt, "", m["gain_x"], ry + 3, Kit.HUE_GOOD),
                            m["gain_x"], 3) if m["gain_x"] is not None else None
            r["bar"] = None
            if m["bar_x"] is not None:
                bdy = (row_h() - m["bar_h"]) // 2
                by = ry + bdy
                # The bar's background is the client's red line art, or a plain tile when that art is missing.
                if Kit.pic_size(Kit.LINE_RED)[0] > 0:
                    put(r, Kit.add_tiled(tgt, Kit.LINE_RED, m["bar_x"], by, m["bar_w"],
                                      m["bar_h"], hue=BAR_BG_HUE), m["bar_x"], bdy)
                else:
                    put(r, Kit.add_tiled(tgt, Kit.SECTION_TILE, m["bar_x"], by, m["bar_w"],
                                      m["bar_h"], 1.0), m["bar_x"], bdy)
                r["bar"] = put(r, Kit.add_tiled(tgt, Kit.LINE_BLUE, m["bar_x"], by, 1, m["bar_h"]), m["bar_x"], bdy)
            tip = "Click: pick it (details below); double-click: its floating button" \
                if SK["click"][i] else "Click: pick it (details below)"
            r["cat"] = put(r, Kit.catcher(tgt, m["name_x"] - 2, ry, m["lock_x"] - m["name_x"] - 2,
                                       row_h() - 1, row_click(i)), m["name_x"] - 2, 0)
            r["tip0"], r["cat_tip"], r["use"] = tip, None, None
            if SK["click"][i]:
                b = G.CreateGumpButton("", Kit.HUE_TEXT, GEM[0], GEM[1], GEM[2])
                b.SetPos(4, ry + 6)
                tgt.Add(b)
                Kit.on_click(b, queue(("use", i), dup=True))
                Kit.with_tip(b, "Use " + SK["names"][i])
                r["use"] = put(r, b, 4, 6)
            r["lock"] = put(r, Kit.add_pic(tgt, LOCK_ART[0], m["lock_x"], ry + 4), m["lock_x"], 4)
            # The lock arrow's tooltip, as last set.
            r["tip"] = None
            if r["lock"] is not None:
                Kit.on_click(r["lock"], queue(("lock", i), dup=True))
                remember(r["lock"], "Graphic", LOCK_ART[0])
            return r

        def row_name(i, m=None):
            """A skill's name as its row shows it: cut to the name column when the zone is too narrow."""
            nm = SK["names"][i] if i < SK["n"] else "?"
            m = m or metrics()
            if m.get("cut"):
                return Kit.fit(nm, m["name_w"] - 10)
            return nm

        def place_selbox():
            """Places the selection box behind the picked skill's row, or hides it when that row is not shown."""
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
                setp(box, "Pos", (0, y))
                setp(box, "IsVisible", True)

        def name_hue(i, now):
            """The colour of a skill's name: green while a gain is fresh, gold when pinned, else normal."""
            if st["hl"].get(i, 0) > now:
                return Kit.HUE_GOOD
            if i in marks["pins"]:
                return Kit.HUE_TITLE
            return Kit.HUE_TEXT

        def refresh_rows(now):
            """Sets the texts of the shown rows.

            A row whose values, gain and name colour are what it already shows is passed over (most rows,
            most seconds), so a quiet window costs very little. The row tooltip is the same line as when the
            row was built plus the training tip when tips are on; it is set only when it changed.
            """
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
                # The row's signature: nothing changed means nothing is touched.
                sig = (base, val, cap, lock, sgain(i) if has_gain else 0, hue)
                if sig == r["sig"]:
                    continue
                r["sig"] = sig
                Kit.set_text(r["name"], row_name(i), hue)
                if r["real"] is not None:
                    Kit.set_text(r["real"], f1(base), Kit.HUE_GOOD if cap and base >= cap else Kit.HUE_TEXT)
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
                    # Kept in the row, not in an id()-keyed cache.
                    if r.get("tip") != tip:
                        r["tip"] = tip
                        Kit.with_tip(r["lock"], tip)
                tp = tip_for(i) if tips_on else None
                ct = r["tip0"] if tp is None else "%s\n%s %s: %s" % (r["tip0"], SK["names"][i], tp[0], tp[1])
                if ct != r["cat_tip"]:
                    r["cat_tip"] = ct
                    Kit.with_tip(r["cat"], ct)
                if r["bar"] is not None:
                    fw = int(bar_w * min(1.0, float(val) / cap)) if cap > 0 else 0
                    setp(r["bar"], "Width", max(1, fw))
                    setp(r["bar"], "IsVisible", fw > 0)
                    setp(r["bar"], "Graphic", LINE_GREEN if cap and base >= cap else Kit.LINE_BLUE)

        GOTHER = {"list": None, "n": -1, "mem": []}

        def group_info(key):
            """Returns (name, member skills) of a group row's key: pin, other or a client group index."""
            if key == "pin":
                return "Pinned", [i for i in range(SK["n"]) if i in marks["pins"]]
            if key == "other":
                # The Other group's members are worked out once per group read, not per refresh.
                if GOTHER["list"] is not GR["list"] or GOTHER["n"] != SK["n"]:
                    of = GR["of"]
                    GOTHER.update({"list": GR["list"], "n": SK["n"], "mem": [i for i in range(SK["n"]) if i not in of]})
                return "Other", GOTHER["mem"]
            if isinstance(key, int) and key < len(GR["list"]):
                g = GR["list"][key]
                return g["name"] or "(no name)", g["members"]
            return "?", []

        def refresh_group_row(r):
            """Sets a group row's name and its totals of real value, value and gain."""
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
            # An unchanged row is passed over.
            sig = (name, len(mem), room, tr, tv, gn)
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
            """Sets the list's header texts and the sort arrow, only when the sort or the columns moved."""
            c = win["c"]
            hdr = c.get("hdr")
            if not hdr:
                return
            m = metrics()
            s = settings["sort"]
            # Redone only when the sort moved or the columns were worked out again.
            hk = (s, settings["asc"], m)
            old = c.get("hdr_k")
            if old is not None and old[0] == s and old[1] == hk[1] and old[2] is m:
                return
            c["hdr_k"] = hk
            names = {"name": ("Skill", m["name_x"]), "real": ("Real", m["real_x"]),
                     "value": ("Value", m["val_x"]), "cap": ("Cap", m["cap_x"]), "gain": ("Gain", m["gain_x"])}
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

        LOGTXT = {}

        def refresh(now):
            """Refreshes everything the window shows: the list, totals, session, stats, details and log.

            Called every REDRAW_EVERY seconds and when something changed. Does nothing while folded into
            the Action Bar. The minimized bar only gets its one line. Every text goes through fit_set or
            Kit.set_text, which skip an unchanged text.
            """
            c = win["c"]
            if not c:
                return
            tr = total_real()
            if c.get("mini") is not None:
                # Folded into the tray: nothing on screen to set.
                if st["docked"]:
                    return
                txt = "%s: %s / %s %+.1f" % (TITLE, f1(tr), f1(settings["total_cap"]), total_gain() / 10.0)
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
                    a = "Total %s / %s   (%s free)" % (f1(tr), f1(settings["total_cap"]), f1(max(0, free)))
                    b, sep = "with bonuses %s" % f1(tv), "   "
                    hue = Kit.HUE_TEXT
                txt = a + sep + b
                # Two lines in a narrow zone: the total and the bonuses on their own lines.
                if c.get("total2") is not None:
                    sa, sb = Kit.fit(a, IWt), Kit.fit(b, IWt)
                    Kit.set_text(c["total"], sa, hue)
                    Kit.set_text(c["total2"], sb, hue)
                    tip = TOTAL_TIP if (sa, sb) == (a, b) else "%s. %s" % (txt, TOTAL_TIP)
                    if tip != c.get("total_tip"):
                        c["total_tip"] = tip
                        Kit.with_tip(c["total_cat"], tip)
                else:
                    fit_set(c, "total", txt, IWt, hue, TOTAL_TIP)
            if c.get("session") is not None:
                tg = total_gain()
                hrs = hours_running()
                txt = "Session %+.1f in %s   (%.1f / hour)" % (tg / 10.0, dur(now - sess["start"]), tg / 10.0 / hrs)
                fit_set(c, "session", txt, c["session_w"], Kit.HUE_GOOD if tg > 0 else Kit.HUE_INFO)
            if c.get("stats"):
                base = sess["stats"] or STATS["cur"]
                hrs = hours_running()
                cats, tips = c.get("stat_cats") or (), c.get("stat_tips")
                for k, (lbl, pic) in enumerate(c["stats"]):
                    v = STATS["cur"][k]
                    d = v - base[k] if sess["stats"] else 0
                    Kit.set_text(lbl, "%s %d%s" % (("Str", "Dex", "Int")[k], v, (" (%+d)" % d) if d else ""),
                                 Kit.HUE_GOOD if d > 0 else Kit.HUE_TEXT)
                    setp(pic, "Graphic", LOCK_ART[STATS["locks"][k]])
                    if k < len(cats):
                        tip = stat_tip(k, hrs)
                        # The stat tooltips are set only when the text changed.
                        if tip != tips[k]:
                            tips[k] = tip
                            Kit.with_tip(cats[k], tip)
                tot = sum(STATS["cur"])
                cap = STATS["cap"]
                txt = ("Stats %d / %d" % (tot, cap)) if cap else ("Stats %d" % tot)
                tg = (stat_gain(0) + stat_gain(1) + stat_gain(2)) if sess["stats"] else 0
                # The session's stat gain, when it fits beside the total.
                if tg:
                    more = "%s   %+d (%.1f / hour)" % (txt, tg, tg / hrs)
                    if Kit.text_px(more) <= c["stat_total_w"]:
                        txt = more
                fit_set(c, "stat_total", txt, c["stat_total_w"], Kit.HUE_GOOD if cap and tot >= cap else Kit.HUE_INFO)
            refresh_detail(now)
            if c.get("log") is not None:
                lines = st["log"][-len(c["log"]):][::-1]
                for k, lbl in enumerate(c["log"]):
                    if k < len(lines):
                        e = lines[k]
                        # The entry's own gain decides the colour, every line.
                        d = e[2]
                        # One format per log entry; the text is made once and remembered.
                        txt = LOGTXT.get(e)
                        if txt is None:
                            t, name, _g, nb = e
                            txt = "%s  %s %s%s  (%s)" % (time.strftime("%H:%M", time.localtime(t)),
                                                         name, "+" if d > 0 else "-", f1(abs(d)), f1(nb))
                            # Bounded: the memory is cleared when it grows past twice the log.
                            if len(LOGTXT) >= 2 * LOG_KEEP:
                                LOGTXT.clear()
                            LOGTXT[e] = txt
                        fit_set(c, "log%d" % k, txt, c["log_w"], Kit.HUE_GOOD if d > 0 else Kit.HUE_BAD, lbl=lbl)
                    else:
                        fit_set(c, "log%d" % k, "No gains yet this session." if k == 0 and not lines
                                else "", c["log_w"], Kit.HUE_INFO, lbl=lbl)

        def refresh_detail(now):
            """Sets the picked skill's details: name and group, lock arrows, values, rates, tip, target, Pin."""
            c = win["c"]
            if c.get("d_name") is None:
                return
            i = st["sel"]
            if i is None or i >= SK["n"]:
                fit_set(c, "d_name", "No skill picked", c["d_name_w"])
                fit_set(c, "d_l1", "Click a skill in the list to see it here.", c["d_lw"], Kit.HUE_INFO)
                fit_set(c, "d_l2", "", c["d_lw"])
                fit_set(c, "d_tgt", "", c["d_tgt_w"])
                if c.get("d_tip") is not None:
                    Kit.set_text(c["d_tip"], "")
                    # No older tip is left in its tooltip.
                    if c["d_tip_full"] is not None:
                        c["d_tip_full"] = None
                        Kit.with_tip(c["d_tip_cat"], "Training tip for this skill's range")
                for p in c["d_locks"]:
                    setp(p, "Hue", DIM_HUE)
                return
            base, val, cap, lock = SK["cur"][i]
            gi = group_of(i)
            gname = GR["list"][gi]["name"] if gi is not None else ""
            fit_set(c, "d_name", SK["names"][i] + ("   (%s)" % gname if gname else ""), c["d_name_w"], Kit.HUE_TITLE)
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
            # The training tip.
            if c.get("d_tip") is not None:
                tp = tip_for(i)
                if tp is not None:
                    full, hue = "Tip %s: %s" % tp, Kit.HUE_TEXT
                else:
                    full, hue = "No tip for this range", Kit.HUE_INFO
                Kit.set_text(c["d_tip"], Kit.fit(full, c["d_lw"]), hue)
                if full != c["d_tip_full"]:
                    c["d_tip_full"] = full
                    Kit.with_tip(c["d_tip_cat"], full)
            tgt = marks["targets"].get(i)
            if tgt:
                if base >= tgt:
                    txt, hue = "reached", Kit.HUE_GOOD
                else:
                    txt = "%s to go%s" % (f1(tgt - base), ", then locks" if settings["lock_at_target"] else "")
                    hue = Kit.HUE_INFO
            else:
                txt, hue = "none set", Kit.HUE_INFO
            fit_set(c, "d_tgt", txt, c["d_tgt_w"], hue)
            if c.get("pin") is not None:
                Kit.set_text(c["pin"], "Unpin" if i in marks["pins"] else "Pin")

        def show_target_text():
            """Puts the picked skill's target in the target box (when the pick changed)."""
            c = win["c"]
            tb = c.get("target")
            if tb is None:
                st["tgt_shown"] = None
                return
            i = st["sel"]
            txt = f1(marks["targets"][i]) if i is not None and i in marks["targets"] else ""
            tb.SetText(txt)
            st["tgt_shown"] = (i, txt)

        def poll_fields(now):
            """Reads the search box, the target box and the Groups tick on the client thread.

            Returns True when something changed. A typed target is saved the moment it parses. The reads
            are plain try blocks: this runs every tick.
            """
            c = win["c"]
            moved = False
            sb = c.get("search")
            if sb is not None:
                # Every tick: no safe(lambda) here.
                try:
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
                    except (ValueError, OverflowError):
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
                        # The groups were not read while they were not on show.
                        read_groups(True)
                    moved = True
            return moved

        def gumps_sig():
            """Returns (how many windows the client has, the front one), or None when the list cannot be read.

            A window that opens changes it, which is what vanilla_check looks for.
            """
            try:
                lst = VG["gumps"]
                if lst is None:
                    lst = VG["gumps"] = Tz.get(None, "Gumps", Tz.T("ClassicUO.Game.Managers.UIManager"))
                return (int(lst.Count), lst.First)
            except Exception:
                VG["gumps"] = None
                return None

        # Seconds between full looks when nothing was seen to change.
        VANILLA_FULL_EVERY = 3.0

        def vanilla_check():
            """Closes the client's own skills window the moment it opens and brings this one up instead.

            Only while Replace is on, or while an Ask server request is waiting for its own window to
            close. Looking through every window of the client (each one's type name) four times a second
            was most of this module's idle cost, so the full look runs only when the client's window list
            changed (count or front window) and once every VANILLA_FULL_EVERY seconds besides.
            """
            if not settings["replace"] and time.time() > st["swallow_until"]:
                return
            now = time.time()
            sig = gumps_sig()
            if sig is not None and sig == VG["sig"] and now < VG["full_at"]:
                return
            VG["sig"], VG["full_at"] = sig, now + VANILLA_FULL_EVERY
            # The list itself is looked up afresh too.
            VG["gumps"] = None
            found = safe(lambda: Tz.windows(VANILLA), []) or []
            if not found:
                return
            # A window was found and closed: look again next tick.
            VG["sig"] = None
            for gmp in found:
                gmp.Dispose()
            # Our own Ask server request: just close it, do not bring the window up.
            if time.time() <= st["swallow_until"]:
                st["swallow_until"] = 0.0
                return
            bring_up()

        def bring_up():
            """Shows this window: from hidden, minimized or folded it is rebuilt full size; else brought to front."""
            if st["hidden"] or st["minimized"] or st["docked"] or not Kit.is_open(win["g"]):
                st["hidden"] = st["minimized"] = st["docked"] = False
                settings["minimized"] = False
                save_settings()
                build_window()
            else:
                ctl = Kit.client_control(win["g"])
                if ctl is not None:
                    Tz.call(None, "MakeTopMostGump", [ctl], Tz.T("ClassicUO.Game.Managers.UIManager"))

        def armed(key, text):
            """True on the second click within ARM_SECS; the first only says so in the journal."""
            now = time.time()
            if now - st["arm"].get(key, 0.0) <= ARM_SECS:
                st["arm"].pop(key, None)
                return True
            st["arm"][key] = now
            say(text, Kit.HUE_INFO)
            return False

        def bulk_lock(v, only_capped=False):
            """Sets the shown skills (or every capped skill) to lock v and says how many changed."""
            n = 0
            for i in (range(SK["n"]) if only_capped else [d[1] for d in (st["desc"] or []) if d[0] == "s"]):
                base, _, cap, lock = SK["cur"][i]
                if only_capped and not (cap and base >= cap):
                    continue
                if lock != v:
                    set_lock(i, v)
                    n += 1
            say("%s %s." % (Kit.count(n, "skill"), ("set to go up", "set to go down", "locked")[v]),
                       Kit.HUE_GOOD if n else Kit.HUE_INFO)

        def apply_lockset(k):
            """Puts lock set k on the skills, one letter per skill, and says how many changed."""
            if k >= len(locksets):
                return
            name, code = locksets[k]
            n = 0
            for i, ch in enumerate(code[:SK["n"]]):
                v = "udl".find(ch)
                if v >= 0 and SK["cur"][i][3] != v:
                    set_lock(i, v)
                    n += 1
            say("lock set \"%s\" put on (%d change%s)." % (name, n, "" if n == 1 else "s"), Kit.HUE_GOOD)

        def save_lockset(name):
            """Saves every skill's lock as a lock set called name; the same name replaces it.

            The name loses the characters the save format uses and is cut to 24; an empty name becomes Set n.
            At most MAX_LOCKSETS sets: a new one past that is refused.
            """
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
                    say("at most %d lock sets: delete one first." % MAX_LOCKSETS, Kit.HUE_BAD)
                    return
                locksets.append((name, code))
            save_locksets()
            say("lock set \"%s\" saved." % name, Kit.HUE_GOOD)

        def move_to_next_group(i):
            """Moves skill i to the next client skill group, wrapping round, and saves the groups.

            A skill in no group goes to the first. The group objects are the client's own.
            """
            read_groups(True)
            if i is None or not GR["list"]:
                say("couldn't move the skill (the client's skill groups can't be read).", Kit.HUE_BAD)
                return
            gi = group_of(i)
            dst = 0 if gi is None else (gi + 1) % len(GR["list"])
            try:
                import System
                if gi is not None:
                    GR["list"][gi]["obj"].Remove(System.Byte(i))
                GR["list"][dst]["obj"].Add(System.Byte(i))
                groups_save()
                say("%s moved to %s." % (SK["names"][i], GR["list"][group_of(i) or 0]["name"]), Kit.HUE_GOOD)
            except Exception as ex:
                say("couldn't move it (%s)." % Tz.why(ex), Kit.HUE_BAD)

        def group_new():
            """Adds an empty client skill group called New group."""
            mgr = group_mgr()
            try:
                import System
                g = System.Activator.CreateInstance(Tz.T("ClassicUO.Game.Managers.SkillsGroup"))
                g.Name = "New group"
                g.IsMaximized = True
                mgr.Add(g)
                groups_save()
            except Exception as ex:
                say("couldn't add a group (%s)." % Tz.why(ex), Kit.HUE_BAD)

        def group_delete(gi):
            """Deletes group gi (never the first), whose skills go to the first group, and saves."""
            read_groups(True)
            if gi <= 0 or gi >= len(GR["list"]):
                return
            mgr = group_mgr()
            name = GR["list"][gi]["name"]
            if safe(lambda: mgr.Remove(GR["list"][gi]["obj"]), False):
                groups_save()
                say("group \"%s\" deleted; its skills went to \"%s\"." % (
                    name, GR["list"][0]["name"] if GR["list"] else "the first group"), Kit.HUE_GOOD)

        def group_reset():
            """Puts back the client's default skill groups and saves."""
            mgr = group_mgr()
            try:
                mgr.MakeDefault()
                groups_save()
                say("skill groups reset to the default ones.", Kit.HUE_GOOD)
            except Exception as ex:
                say("couldn't reset the groups (%s)." % Tz.why(ex), Kit.HUE_BAD)

        def export_sheet():
            """Prepares a text file with every skill's values for write_files to write.

            The file goes to the settings folder as Skills_ and the character's serial. The header names the
            character and the time; then the totals, the stats, the session and one line per skill sorted by
            name. Only prepared here: the write is done on the script thread.
            """
            p = API.Player
            path = Kit.data_path("Skills_%08X.txt" % int(p.Serial))
            now = time.time()
            # The character's name goes into the sheet's header: this export, a runtime file the player asks
            # for, is the only place a name is written. Nothing of Virtue Assistant's own files carries one.
            lines = ["Skill sheet - %s - %s" % (p.Name or "", time.strftime("%Y-%m-%d %H:%M", time.localtime(now))),
                     "Total %s / %s   (with bonuses %s)" % (f1(total_real()), f1(settings["total_cap"]),
                         f1(sum(x[1] for x in SK["cur"]))), "Str %d  Dex %d  Int %d   (stat cap %d)" % (
                         STATS["cur"][0], STATS["cur"][1], STATS["cur"][2], STATS["cap"]),
                     "Session %+.1f in %s" % (total_gain() / 10.0, dur(now - sess["start"])), "",
                     "%-26s %7s %7s %7s %8s  %s" % ("Skill", "Real", "Value", "Cap", "Session", "Lock")]
            for i in sorted(range(SK["n"]), key=lambda i: SK["names"][i].lower()):
                b, v, cp, lk = SK["cur"][i]
                gn = sgain(i)
                lines.append("%-26s %7s %7s %7s %8s  %s" % (
                    SK["names"][i], f1(b), f1(v), f1(cp), ("%+.1f" % (gn / 10.0)) if gn else "", LOCK_WORD[lk]))
            # Queued for write_files on the script thread: a disk write on the client thread is a frame hitch.
            st["to_write"].append((path, "\n".join(lines) + "\n"))

        def write_files():
            """Script thread: writes the skill sheets export_sheet prepared. Returns at once when there are none."""
            write_queue(st["to_write"], TITLE, "skill sheet")

        def _thread_wanted():
            """True when the script thread has work: a sheet waits to be written."""
            return bool(st["to_write"])

        def pick(i):
            """Picks skill i (shows its details and target)."""
            if st["sel"] != i:
                st["sel"] = i
                show_target_text()
                if settings["sec_detail"]:
                    # Its group is named in the details; the once-a-second read does that. A click storm while
                    # sorting by gain once did one reflection walk per click, so a read is forced only when the
                    # groups were never read.
                    read_groups(GR["sig"] is None)
            place_selbox()

        def picked(i):
            """True when a skill is picked; says so in the journal when not."""
            if i is None:
                say("pick a skill first.", Kit.HUE_INFO)
            return i is not None

        def action_parts(a):
            """Splits a queued action into its name and its argument (None when it has none)."""
            if not isinstance(a, tuple):
                return a, None
            return a[0], a[1] if len(a) > 1 else None

        def toggle_min(arg):
            """Minimized or full: a click toggles, and a folded window comes out first. Saved with the settings."""
            st["minimized"] = not (st["minimized"] or st["docked"])
            st["docked"] = False
            safe(lambda: HOST.dock_forget(KEY))
            settings["minimized"] = st["minimized"]
            save_settings()
            st["rebuild"] = "window"

        def cycle_filter(arg):
            """Moves to the next filter and shows its name on the button."""
            settings["filter"] = (settings["filter"] + 1) % len(FILTERS)
            save_settings()
            lbl = win["c"].get("filter")
            if lbl is not None:
                Kit.set_text(lbl, FILTERS[settings["filter"]][1])

        def sort_by(arg):
            """Sorts by column arg; the same column again reverses it. A new column starts ascending for names."""
            if settings["sort"] == arg:
                settings["asc"] = not settings["asc"]
            else:
                settings["sort"] = arg
                settings["asc"] = arg == "name"
            save_settings()

        def use_action(arg):
            """Uses the skill arg, or the picked one."""
            i = arg if arg is not None else st["sel"]
            if picked(i):
                use_skill(i)

        def fold_row(arg):
            """Folds or unfolds a group row: the module's own groups (Pinned, Other) or the client's."""
            if not isinstance(arg, int):
                st["pc"][arg] = not st["pc"].get(arg, False)
            elif arg < len(GR["list"]):
                g = GR["list"][arg]
                g["obj"].IsMaximized = g["max"] = not g["max"]

        def pin_skill(arg):
            """Pins or unpins the picked skill and saves the marks."""
            sel = st["sel"]
            if picked(sel):
                marks["pins"] ^= {sel}
                save_marks()

        def ask_skills(arg):
            """Asks the server for fresh skill values and says whether the request went."""
            if ask_server():
                say("asked the server for your skills.", Kit.HUE_INFO)
            else:
                say("couldn't ask the server (the client's skills call failed).", Kit.HUE_BAD)

        def lockset_delete(arg):
            """Deletes lock set arg and refreshes the settings page."""
            if arg < len(locksets):
                n = locksets.pop(arg)[0]
                save_locksets()
                say("lock set \"%s\" deleted." % n, Kit.HUE_INFO)
            HOST.refresh_settings(KEY)

        def reset_groups(arg):
            """Puts back the default groups after a second click within ARM_SECS."""
            if armed("grp_reset", "click Reset groups again for the default groups."):
                group_reset()
                HOST.refresh_settings(KEY)

        # Queued action name to handler, each taking the argument the click queued. A lambda returning a
        # tuple runs both of its parts.
        ACTIONS = {"settings": lambda arg: HOST.show_settings(KEY), "to_bar": lambda arg: HOST.dock_to_bar(KEY, TITLE),
                   "pick": pick, "stat": lambda arg: set_stat_lock(arg, (STATS["locks"][arg] + 1) % 3),
                   "all_up": lambda arg: bulk_lock(0), "all_locked": lambda arg: bulk_lock(2),
                   "lock_capped": lambda arg: bulk_lock(2, True), "export": lambda arg: export_sheet(),
                   "ls_save": lambda arg: (save_lockset(arg), HOST.refresh_settings(KEY)), "ls_apply": apply_lockset,
                   "grp_new": lambda arg: (group_new(), HOST.refresh_settings(KEY)),
                   "grp_del": lambda arg: (group_delete(arg), HOST.refresh_settings(KEY)),
                   "grp_save": lambda arg: groups_save(), "toggle_min": toggle_min, "filter": cycle_filter,
                   "sort": sort_by, "button": lambda arg: (pick(arg), make_button(arg)),
                   "mkbutton": lambda arg: picked(st["sel"]) and make_button(st["sel"]), "use": use_action,
                   "lock": lambda arg: arg is not None and arg < SK["n"] and set_lock(arg, (SK["cur"][arg][3] + 1) % 3),
                   "dlock": lambda arg: st["sel"] is not None and set_lock(st["sel"], arg), "fold": fold_row,
                   "pin": pin_skill, "nextgrp": lambda arg: picked(st["sel"]) and move_to_next_group(st["sel"]),
                   # All down needs a second click: it is the one bulk action that can undo a lot.
                   "all_down": lambda arg: armed("all_down",
                                                 "click All down again to set every listed skill to go down.")
                   and bulk_lock(1),
                   "newsess": lambda arg: (new_session(), say("new session; gains count from now.", Kit.HUE_GOOD)),
                   "ask": ask_skills, "ls_del": lockset_delete, "grp_reset": reset_groups}
        # The settings page: the checkboxes of the Window section (key, caption, tooltip).
        MAIN_CHECKS = [("replace", "Replace the client's skills window",
             "The paperdoll's Skills button, the Skills macro and the Action Bar open this one"),
            ("x_hides", "Close only hides it", "Off: Close turns Skills off"),
            ("bars", "Progress bar per skill (value / cap)", "Filled to value / cap; green at the cap"),
            ("col_cap", "Cap column", "Each skill's cap"), ("col_gain", "Session gain column",
             "What each skill gained this session"),
            ("journal", "Journal line for each gain or loss", "The client may print its own line too (its Options)"),
            ("lock_at_cap", "Lock a skill when it reaches its cap", "A rising skill locks the moment it hits its cap"),
            ("lock_at_target", "Lock a skill when it reaches its target", "Set targets in the window's details"),
            ("cap_warn", "Warn at the total cap when no skill is set to go down",
             "Journal warning and a red total when nothing can rise"),
            ("tips", "Training tips in the details and row tooltips", "Classic-era advice for the skill's range")]
        # The numeric fields: key, caption, whether it shows tenths, tooltip.
        NUM_FIELDS = [("rows", "Rows in the list:", False, "Skills shown at once (or drag a window corner)"),
                      ("total_cap", "Total skill cap:", True, "The shard's total skill cap (check it in game)"),
                      ("hl_secs", "Green name after a gain (s):", False,
                       "Seconds a name stays green after a gain (0 = never)"),
                      ("rate_min", "Recent pace over (minutes):", False,
                       "Minutes the recent rate and time to cap look back")]
        # The checkboxes of the Sections section: what the window shows.
        SEC_CHECKS = [("sec_summary", "Totals and session", "Total skill points and the session line"),
                      ("sec_stats", "Str / Dex / Int", "Stats, lock arrows and the stat cap"),
                      ("sec_locks", "Lock buttons", "All up, All down, All locked and Lock capped"),
                      ("sec_detail", "Picked skill details", "Rates, target, pin and the Use button"),
                      ("sec_log", "Recent gains", "The last gains, newest first")]
        TOOLS_HINT = "Export writes a text file to the VirtueAssistantSettings folder."
        SIZE_HINT = "Drag a window corner: height sets the rows, width spreads the columns."
        STAT_HINT = ("A stat set to go up locks when it rises to its target, one set to go down when it falls to it. "
                     "The window's stat tooltips show gains per hour.")

        def page_table(w):
            """Builds the settings page's table of sections for a page w pixels wide.

            Returns the (section name, rows, layout) tuples the mother's settings window draws: the window
            checks and numbers, the sections, the stat targets, the lock sets, the groups and the tools.
            The custom rows are drawn by the nested functions below, which keep their controls in the page's
            c table for the page's own poll to read.
            """
            read_groups(GR["sig"] is None)
            ng = len(GR["list"]) if GR["ok"] else 1
            half = (w - 24) // 2

            def hint(text, dy):
                """The wrapped lines of a hint text as note rows."""
                return [("note", line, {"ndy": dy, "h": 18}) for line in Kit.wrap(text, w - 24)]

            def num_field(k, text, dec, tip):
                """A row of a labelled number field with its range, and for Rows the dragged width.

                Returns a custom row for the table; the nested draw makes the controls.
                """
                def draw(f, x, ry):
                    """Draws the field: caption, box, range and (for Rows) the width the window was dragged to."""
                    g = f.g
                    c = f.c
                    # All captions share one column so the boxes line up.
                    lx = x + 12 + max(Kit.text_w(t) for _, t, _, _ in NUM_FIELDS) + 10
                    Kit.add_label(g, text, x + 12, ry + 3)
                    val = f1(settings[k]) if dec else str(settings[k])
                    c.setdefault("num", {})[k] = Kit.with_tip(Kit.add_textbox(g, val, lx, ry, 70, numbers=not dec), tip)
                    lo, hi = LIMITS[k]
                    rng = ("(%s-%s)" % (f1(lo), f1(hi))) if dec else ("(%d-%d)" % (lo, hi))
                    Kit.add_label(g, Kit.fit(rng, x + w - 4 - (lx + 84)), lx + 84, ry + 3, Kit.HUE_INFO)
                    if k == "rows":
                        wx = lx + 84 + Kit.text_w(rng) + 16
                        c["width_v"] = Kit.add_label(g, Kit.fit(width_text(), x + w - 4 - wx), wx, ry + 3, Kit.HUE_INFO)
                        Kit.catcher(g, wx - 2, ry, x + w - 4 - wx, 22, lambda: None,
                                    "Window width, set by dragging a corner (natural: as wide as the columns need)")

                return ("custom", 28, draw)

            def stat_targets(f, x, ry):
                """Draws the three Str, Dex and Int target boxes, each with its own tooltip."""
                sx = x + 12
                c = f.c
                c["stat_tgt"] = []
                for k, nm in enumerate(("Str", "Dex", "Int")):
                    Kit.add_label(f.g, nm + ":", sx, ry + 3)
                    tx = sx + Kit.text_w(nm + ":") + 8
                    shown = str(stat_tgt[k]) if stat_tgt[k] else ""
                    tb = Kit.with_tip(Kit.add_textbox(f.g, shown, tx, ry, 44, numbers=True),
                                      "%s target (1-%d, empty = none)" % (STAT_NAMES[k], STAT_TARGET_MAX))
                    # Each entry holds the box and its last shown, last read and settle time (see poll_stat_targets).
                    c["stat_tgt"].append([tb, shown, shown, 0.0])
                    sx = tx + 44 + 24

            def lock_sets(f, x, ry):
                """Draws the lock sets: a name box with Save current, then a line per set with Apply and Delete."""
                g, store = f.g, f.store
                Kit.add_label(g, "Name:", x + 12, ry + 3)
                nx = x + 12 + Kit.text_w("Name:") + 8
                sx = x + w - 12 - cap_w("Save current")
                f.c["ls_name"] = Kit.with_tip(Kit.add_textbox(g, "", nx, ry, max(60, sx - nx - 14), numbers=False),
                                              "Name for Save current (empty = Set 1, Set 2 and so on)")
                Kit.art_button(g, store, "ls_save", Kit.ART_OK, sx, ry - 1, "Save current",
                               "Save every skill's lock as a set (same name replaces it)")
                ry += 28
                if not locksets:
                    Kit.add_label(g, "No lock sets yet. Type a name and click Save current.", x + 12, ry + 3,
                                  Kit.HUE_INFO)
                dx = x + w - 12 - cap_w("Delete")
                ax = dx - 12 - cap_w("Apply")
                for k, (name, code) in enumerate(locksets):
                    ups, downs = code.count("u"), code.count("d")
                    Kit.add_label(g, Kit.fit("%s  (%d up, %d down)" % (name, ups, downs), ax - x - 24), x + 12, ry + 3)
                    Kit.art_button(g, store, "ls_apply_%d" % k, Kit.ART_OK, ax, ry - 1, "Apply",
                                   "Put this set's locks on your skills")
                    Kit.art_button(g, store, "ls_del_%d" % k, Kit.ART_CLOSE, dx, ry - 1, "Delete",
                                   "Delete this lock set")
                    ry += 26

            def groups(f, x, ry):
                """Draws the groups section: a name box and a Delete per group, then New group and Reset groups."""
                g, store = f.g, f.store
                dx = x + w - 12 - cap_w("Delete")
                f.c["grp"] = []
                # The groups could not be read: say so rather than showing an empty list.
                if not GR["ok"]:
                    Kit.add_label(g, "The client's skill groups can't be read.", x + 12, ry + 3, Kit.HUE_BAD)
                    ry += 28
                for gi, gr in enumerate(GR["list"]):
                    tb = Kit.with_tip(Kit.add_textbox(g, gr["name"], x + 12, ry, 200, numbers=False),
                                      "Group name (type to rename)")
                    Kit.add_label(g, Kit.count(len(gr["members"]), "skill"), x + 226, ry + 3, Kit.HUE_INFO)
                    if gi > 0:
                        # The first group cannot be deleted: it is where deleted groups' skills go.
                        Kit.art_button(g, store, "grp_del_%d" % gi, Kit.ART_CLOSE, dx, ry - 1,
                                       "Delete", "Delete this group (its skills go to the first one)")
                    else:
                        Kit.add_label(g, "first group", dx + 35, ry + 3, Kit.HUE_INFO)
                    f.c["grp"].append((tb, gi, gr["name"]))
                    ry += 28
                if GR["ok"] and not GR["list"]:
                    ry += 28
                Kit.art_button(g, store, "grp_new", Kit.ART_OK, x + 12, ry - 1, "New group",
                               "Add an empty group (Next group in the window moves skills in)")
                Kit.art_button(g, store, "grp_reset", Kit.ART_CLOSE, x + 12 + cap_w("New group") + 16,
                               ry - 1, "Reset groups", "Put back the client's default groups (click twice)")

            # The line count of Recent gains is a number field on the page's own table.
            lo, hi = LIMITS["log_lines"]
            sec = {"ch": 24, "pad": 6}
            return (("WINDOW", [("check",) + r for r in MAIN_CHECKS] + [num_field(*r) for r in NUM_FIELDS] +
                     hint(SIZE_HINT, 2), sec),
                    ("SECTIONS  (what the window shows)", [("check",) + r + ({"stay": n % 2 == 0 and n < 4,
                     "dx": 12 + (n % 2) * half},) for n, r in enumerate(SEC_CHECKS)] + [("num", "log_lines",
                     "Recent gains lines:", "Lines the Recent gains part shows (%d-%d)" % (lo, hi), None, lo, hi)],
                     sec), ("STAT TARGETS", [("custom", 28, stat_targets),
                     ("check", "lock_stat_target", "Lock a stat when it reaches its target",
                      "Off: only a journal line when it gets there")] + hint(STAT_HINT, 2), sec),
                    ("LOCK SETS  (saved locks)", (("custom", 28 + max(1, len(locksets)) * 26, lock_sets),), sec),
                    ("GROUPS  (the client's skill groups)", (("custom", max(1, ng) * 28 + 28, groups),), sec),
                    ("TOOLS", [("buttons", (("export", Kit.ART_PLAY, "Export sheet", "Write every skill's values to a "
                                             "file in the VirtueAssistantSettings folder"),
                                            ("ask", Kit.ART_PLAY, "Ask server",
                                             "Ask the server for fresh skill values"),
                                            ("newsess", Kit.ART_PLAY, "New session",
                                             "Start a new session: gains count from now")))] + hint(TOOLS_HINT, 0),
                     dict(sec, bdy=-1, bgap=16)))

        def width_text():
            """Says what the settings page shows of the dragged width."""
            if settings["width"]:
                return "Width: %d px (drag a corner)" % settings["width"]
            return "Width: natural (drag a corner)"

        def read_num(ctrl, default, lo, hi, dec):
            """Reads a number box clamped to lo and hi (tenths when dec is true); default if it does not parse."""
            try:
                # Plain try (no lambda per read): the page polls this.
                txt = str(ctrl.Text or "").strip()
            except Exception:
                txt = ""
            try:
                v = int(round(float(txt.replace(",", ".")) * 10)) if dec else int(txt)
                return max(lo, min(hi, v))
            except (ValueError, OverflowError):
                return default

        def page_clicks(f):
            """Skills Window settings page: read the typed fields and queue the buttons that were clicked.

            Runs on the client tick while the page is open. The first call after the page was rebuilt only
            refills the fields from the saved settings. Otherwise it applies the Str / Dex / Int targets once
            settled, renames groups whose text box changed, and turns each clicked button into a queued action.
            """
            c = f.c
            # The first pass after a rebuild must not read the freshly drawn fields back as edits: page_adjust
            # skips its read when this is set.
            page["skip"] = page["sync"]
            if page["sync"]:
                page["sync"] = False
                tb = c["num"].get("rows")
                if tb is not None:
                    tb.SetText(str(settings["rows"]))
                if c.get("width_v") is not None:
                    Kit.set_text(c["width_v"], width_text())
                return
            poll_stat_targets(c, False)
            # Group names are plain text boxes: a change is spotted by comparing the text with what was last
            # shown, and the group is renamed at once; the save waits until the typing has rested.
            for tb, gi, shown in list(c.get("grp", ())):
                try:
                    txt = str(tb.Text or "")
                except Exception:
                    txt = str(shown or "")
                if txt != shown and gi < len(GR["list"]):
                    GR["list"][gi]["obj"].Name = GR["list"][gi]["name"] = txt
                    touch()
                    c["grp"] = [(t, g2, txt if g2 == gi else s) for t, g2, s in c["grp"]]
                    st["grp_dirty_at"] = time.time()
            store = f.store
            for key in list(store[0].keys()):
                if not Kit.was_clicked(store, key):
                    continue
                # Buttons with a number in the key (apply, delete) are split here so the queue holds (kind, index).
                if key == "ls_save":
                    queue.add(("ls_save", str(c["ls_name"].Text or "")), dup=True)
                elif key.startswith(("ls_apply_", "ls_del_", "grp_del_")):
                    kind, _, n = key.rpartition("_")
                    queue.add((kind, int(n)), dup=True)
                else:
                    queue.add((key,), dup=True)
                # Wakes the module so the queued action runs now, not on the next slow tick.
                HOST.poke()

        def page_adjust(f, new):
            """Settings page hook: fill `new` with the numeric fields read from the page (clamped to LIMITS).

            When a rebuild is still being synced the saved settings are kept instead.
            """
            if page["skip"]:
                new.update(settings)
                return
            for k, ctrl in f.c["num"].items():
                lo, hi = LIMITS[k]
                new[k] = read_num(ctrl, settings[k], lo, hi, k == "total_cap")

        def page_changed(old, new):
            """Settings page hook: a setting changed, so the layout, the window and the cap warning are redone.

            A change to a layout key drops the measured layout and rebuilds the whole window.
            """
            touch()
            if any(new[k] != old[k] for k in LAYOUT_KEYS):
                st["m"] = None
                st["rebuild"] = "window"
            st["warned_cap"] = False
            st["cap_at"] = 0.0

        cfg = Kit.Page(settings, page_table, save_settings, page_changed, adjust=page_adjust, clicks=page_clicks)
        # Seconds a typed target must stay unchanged before it counts.
        STAT_SETTLE = 0.8

        def poll_stat_targets(c, final):
            """Apply the Str / Dex / Int target fields once each has stopped changing (or the page is closing).

            A number typed half way (the 1 on the way to 100) must never count, so a field is applied only
            after STAT_SETTLE seconds of no change. `final` is True when the page is going: the text of the
            last poll is applied and the box is not read again, because a disposed text box reads as empty
            and that would wipe every target. Saves the targets to the shared variable store.
            """
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
                # Not a number yet (a stray sign or letter): ignore it and wait for the next edit.
                if txt and not txt.isdigit():
                    continue
                v = max(0, min(STAT_TARGET_MAX, int(txt))) if txt else 0
                if v != stat_tgt[k]:
                    stat_tgt[k] = v
                    Kit.put_var(STAT_TARGETS_KEY, ",".join(str(t) for t in stat_tgt))
                    touch()
                    stat_at_target(k)

        def config_closed():
            """Settings page closed: apply targets still settling, and save a group rename still resting."""
            if cfg.f is not None:
                poll_stat_targets(cfg.f.c, True)
            cfg.closed()
            page["sync"] = False
            if st.get("grp_dirty_at"):
                st["grp_dirty_at"] = 0.0
                queue.add(("grp_save",), dup=True)

        def set_ready():
            """The skills have come in from the server: mark the window ready and take the session baseline.

            The baseline is what the gains and the session totals are counted from.
            """
            st["ready"] = True
            for i in range(SK["n"]):
                sess["base"].setdefault(i, SK["cur"][i][0])
            if sess["stats"] is None and any(STATS["cur"]):
                sess["stats"] = list(STATS["cur"])

        def drop_window():
            """Dispose the Skills window and forget every control that belonged to it."""
            g, win["g"] = win["g"], None
            win.update({"c": {}, "rows": [], "rowmap": {}})
            UIC.clear()
            Kit.dispose(g)

        load_settings()
        load_stat_targets()

        def _start():
            """Part hook: reset the run state, load the saved data, read skills and stats and draw the window.

            Registers the window with the dock so the layout can place it in its zone. The window starts
            docked (in the Action Bar tray) when the host says it is about to be folded in, so it is not drawn
            once loose and then folded.
            """
            st.update({"shutting": False, "docked": HOST.dock_soon(KEY), "hidden": False, "queue": [],
                       "rebuild": None, "desc": None, "m": None, "ready": False,
                       "asked": 0.0, "swallow_until": 0.0, "warned_cap": False, "hl": {},
                       "log": [], "gains": {}, "started": time.time(), "ref_at": 0.0,
                       "grp_at": 0.0, "tgt_shown": None, "stat_pending": {}, "dirty": True,
                       "redraw_at": 0.0, "desc_key": None, "cap_at": 0.0, "resize_at": 0.0, "grp_dirty_at": 0.0,
                       # read_at and stats_at: when the skills and the stats are next read.
                       "read_at": 0.0, "stats_at": 0.0})
            VG.update({"gumps": None, "sig": None, "full_at": 0.0})
            load_settings()
            load_marks()
            load_locksets()
            load_stat_targets()
            load_session()
            st["minimized"] = settings["minimized"] or HOST.dock_wanted(KEY)
            refresh_refs(True)
            read_skills()
            read_stats()
            read_groups(True)
            if skills_loaded():
                set_ready()
            fitst.update({"width": None, "rows": None, "slot": None, "k": 1.0, "full": None})
            build_window()
            show_target_text()
            # The layout fits the window to its zone (fit), asks for the exact slot, and can ask where it was
            # really drawn (drawn_at).
            HOST.dock_add(KEY, dict(hooks, on=bring_up, show=bring_up, fit=layout_fit, exact=True, verify=True,
                                    drawn_at=drawn_at))
            if settings["replace"]:
                vanilla_check()

        def _tick():
            """Part hook, client tick: run queued actions, read skills and stats, redraw what changed.

            Runs on the client thread, so it never waits. A hidden, docked or minimized window reads the
            skills only every HIDDEN_READ seconds; an open window reads on every tick. Also grows the list a
            chunk of rows at a time while rows are still unmade.
            """
            now = time.time()
            # The X either hides the window (the Action Bar button brings it back) or turns the module off.
            if win["g"] is not None and Kit.was_clicked(win["store"], "close"):
                if settings["x_hides"]:
                    st["hidden"] = True
                    save_pos()
                    drop_window()
                    say("hidden; %s brings it back." % back_by(), Kit.HUE_INFO)
                else:
                    Kit.dispose(win["g"])
                    return
            # A drag-resize is applied only after the mouse is released and the size has settled.
            if st["resize_at"] and now - st["resize_at"] >= RESIZE_SETTLE and not safe(lambda: SNAP.pressed(), False):
                st["resize_at"] = 0.0
                apply_resize()
            if win["g"] is not None and win["c"].get("more") and not st["rebuild"]:
                grow_rows(now)
            if st["grp_dirty_at"] and now - st["grp_dirty_at"] >= GRP_SETTLE:
                st["grp_dirty_at"] = 0.0
                groups_save()
            had = SK["n"]
            # The references (skill list, gump handles) are not ready: run what is queued and nothing else.
            if not refresh_refs():
                while st["queue"]:
                    kind, arg = action_parts(st["queue"].pop(0))
                    fn = ACTIONS.get(kind)
                    if fn is not None:
                        fn(arg)
                vanilla_check()
                if st["rebuild"] == "window":
                    build_window()
                elif win["g"] is not None and win["c"] and st["desc"] is None:
                    rebuild_rows(now)
                return
            if SK["n"] != had:
                st["rebuild"] = "window"
            changed, stats_moved = {}, False
            # Skip the read while a hidden window is not yet due; everything else reads each tick.
            if not (st["ready"] and (win["g"] is None or not win["c"] or st["minimized"] or st["docked"])
                    and now < st["read_at"]):
                st["read_at"] = now + HIDDEN_READ
                changed = read_skills(not st["ready"])
                if st["stat_pending"] or now >= st["stats_at"] or not st["ready"]:
                    st["stats_at"] = now + STATS_EVERY
                    stats_moved = read_stats()
            if changed:
                list_moved()
            elif stats_moved:
                st["dirty"] = True
            if not st["ready"]:
                if skills_loaded():
                    set_ready()
                    save_session()
                    st["rebuild"] = st["rebuild"] or "rows"
                # No skill list after 3 seconds: ask the server for it, once.
                elif now - st["started"] > 3.0 and not st["asked"]:
                    ask_server()
            elif changed:
                note_gains(changed, now)
            if stats_moved and st["ready"] and (stat_tgt[0] or stat_tgt[1] or stat_tgt[2]):
                note_stats()
            if st["ready"] and sess["stats"] is None and any(STATS["cur"]):
                sess["stats"] = list(STATS["cur"])
            read_groups()
            ran = bool(st["queue"])
            if ran:
                touch()
            while st["queue"]:
                kind, arg = action_parts(st["queue"].pop(0))
                fn = ACTIONS.get(kind)
                if fn is not None:
                    fn(arg)
            # The skill cap warning is rechecked after a change or an action, else every CAP_EVERY seconds.
            if changed or ran or now >= st["cap_at"]:
                st["cap_at"] = now + CAP_EVERY
                warned = st["warned_cap"]
                cap_warning()
                if warned != st["warned_cap"]:
                    touch()
            vanilla_check()
            if st["rebuild"] == "window":
                build_window()
                st["dirty"], st["redraw_at"] = False, now + REDRAW_EVERY
                return
            if win["g"] is None or not win["c"]:
                return
            # Typed fields are polled only while the full window is up.
            if not (st["minimized"] or st["docked"]) and poll_fields(now):
                touch()
            if not st["dirty"] and now < st["redraw_at"]:
                return
            st["dirty"], st["redraw_at"] = False, now + REDRAW_EVERY
            if st["minimized"] or st["docked"]:
                refresh(now)
                return
            rebuild_rows(now)
            refresh(now)

        def _stop():
            """Part hook: save everything (group rename, sheets, position, settings, session) and close the window.

            The group save runs on the client thread because the group manager is a live client object. A
            sheet still waiting is written now, as no thread tick comes after stop.
            """
            st["shutting"] = True
            if st.get("grp_dirty_at"):
                st["grp_dirty_at"] = 0.0
                safe(lambda: Kit.on_client(groups_save))
            write_files()
            save_pos()
            save_settings()
            if st["ready"]:
                save_session()
            HOST.dock_remove(KEY)
            drop_window()
            cleanup.close()

        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": config_closed,
                "thread_tick": write_files, "thread_wanted": _thread_wanted}

    def _part_alarm():
        """Builds the Training Alarm part and returns its hooks.

        Raises a loud alarm when something needs you at the keyboard: a server gump nobody asked for, a
        staff name in view, your name said or whispered, or (off by default) damage while not fighting.
        The alarm shows on the shared banner, plays the alert sound, repeats it until answered, and
        pauses skill loops through the service attention.up. It only reads, sounds and pauses: it never
        targets, speaks or moves. The character name is read from the game, never stored in the script.
        """
        # Saved keys: Attention_settings (triggers and options), Attention_pos (window place) and
        # Attention_min (minimized when last seen). The old module name stays in the keys so saves load.
        KEY = "attention"
        TITLE = "Training Alarm"
        SETTINGS_KEY = "Attention_settings"
        POS_KEY = "Attention_pos"
        MIN_KEY = "Attention_min"
        W = 400
        MINI_W, MINI_H = 300, 46
        TRAY_ICON = 0x1C12
        # Polling intervals: server gumps, mobiles in view (staff), and hit points, in seconds.
        GUMP_EVERY = 0.25
        STAFF_EVERY = 1.0
        STAFF_RANGE = 18
        STAFF_RECHECK = 2.0
        STAFF_GONE = 60.0
        HIT_EVERY = 0.25
        # A gump opening within this many seconds of your mouse, typing or a gump closing counts as asked
        # for (it is most likely yours). TYPED_SECS is how long a typed command makes the next gump yours.
        ASKED_SECS = 1.5
        TYPED_SECS = 5.0
        # A gump id seen open in the last minute is a page of a window you were using, not news.
        SAME_GUMP_SECS = 60.0
        DEFAULT_MARKERS = ("GM, Counselor, Seer, Admin, Administrator, Developer, Staff, Game Master")
        DEFAULT_IGNORE = ""
        # The client's MessageType of a whispered line, by name and by number.
        WHISPER_TYPES = ("whisper", "8")
        REPEAT_DEFAULT, REPEAT_MAX = 5, 120
        HOLD_DEFAULT, HOLD_MAX = 0, 600
        REASONS_MAX = 8
        QUOTE_MAX = 60
        FLASH_SECS = 0.5
        # Caps on what is remembered: mobiles checked, gump ids seen, and whispers waiting for the tick.
        CACHE_CAP = 500
        OPEN_IDS_CAP = 60
        QUEUE_CAP = 30
        NAME_EVERY = 5.0
        # Each kind of alarm: trigger, alert key on Settings > Alerts, its label, and the default sound id.
        KINDS = (("gump", "attention.gump", "Gump nobody asked for", 0x307),
                 ("staff", "attention.staff", "Staff in view", 0x307),
                 ("name", "attention.name", "Someone says your name", 0x338),
                 ("whisper", "attention.whisper", "A whisper to you", 0x338),
                 ("hit", "attention.hit", "Hit while not fighting", 0x1F1),
                 ("test", "attention.test", "Training Alarm test", 0x307))
        ALERT_KEY = dict((k, a) for k, a, _, _ in KINDS)
        TRIGGERS = ("gump", "staff", "name", "words", "whisper", "hit")
        # Defaults: every trigger on except hit; anyalarm means any module's alarm banner also pauses loops.
        settings = {"gump": True, "staff": True, "name": True, "words": True, "whisper": True,
                    "hit": False, "markers": DEFAULT_MARKERS, "ignore": DEFAULT_IGNORE,
                    "repeat": REPEAT_DEFAULT, "hold": HOLD_DEFAULT, "anyalarm": True}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "open_ids": {}, "last_gid": 0,
              "me": 0, "my_name": "", "name_re": None, "words_re": None, "seq": 0}
        win = {"g": None, "c": {}, "store": ({}, {})}
        page = {"skip": False}
        # The client events are subscribed once per script run, not once per start.
        hooks = {"done": False}
        cleanup, queue, say = Kit.basics(st, TITLE)
        # The client's mouse readers, found once by reflection.
        mouse = {"looked": False, "get": None}
        rx = {"markers": None, "text": None, "ignore": frozenset(), "ignore_text": None}

        def _clean(text):
            """Make a free-text setting safe for the saved string (no semicolons or equals signs)."""
            return str(text or "").replace(";", ",").replace("=", " ").strip()

        def load_settings():
            """Read the saved triggers, options, staff words and ignore list from the shared variable store."""
            for k, v in Kit.codec_load(Kit.get_var(SETTINGS_KEY)).items():
                if k in TRIGGERS or k == "anyalarm":
                    settings[k] = v == "1"
                elif k in ("repeat", "hold"):
                    try:
                        settings[k] = max(0, min(REPEAT_MAX if k == "repeat" else HOLD_MAX, int(v)))
                    except ValueError:
                        continue
                elif k in ("markers", "ignore"):
                    settings[k] = v

        def save_settings():
            """Write the triggers, options, staff words and ignore list as one key=value;key=value string."""
            parts = ["%s=%d" % (k, 1 if settings[k] else 0) for k in TRIGGERS + ("anyalarm",)]
            parts += ["repeat=%d" % settings["repeat"], "hold=%d" % settings["hold"],
                      "markers=%s" % _clean(settings["markers"]), "ignore=%s" % _clean(settings["ignore"])]
            Kit.put_var(SETTINGS_KEY, ";".join(parts))

        def marker_re():
            """The staff words as one whole-word, any-case pattern; built again only when the words change.

            Returns None when the list is empty (no staff check).
            """
            text = settings["markers"]
            if rx["text"] != text:
                words = [w.strip() for w in str(text or "").split(",") if w.strip()]
                # Longest first, so Game Master is tried before Game.
                words.sort(key=len, reverse=True)
                rx["markers"] = re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"
                                           % "|".join(re.escape(w) for w in words), re.IGNORECASE) if words else None
                rx["text"] = text
            return rx["markers"]

        def ignored_ids():
            """The ignore list as a set of gump ids (hex 0x.. or decimal), parsed again only when it changes."""
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

        def sound_of(kind):
            """The sound id to play for this kind of alarm, 0 when it is silent, the alerts are in quiet mode or
            all alert sounds are muted.

            Follows the player's choice on Settings > Alerts, else the default of the kind.
            """
            if ALERTS.quiet_on() or ALERTS.mute:
                return 0
            on, sid = ALERTS.setting(ALERT_KEY[kind])
            return sid if on else 0

        def banner_up():
            """True while the shared alert banner shows an alarm (it flashes until clicked)."""
            return bool(ALERTS.shown and ALERTS.alarm)

        def is_up():
            """Service attention.up: True while an alarm waits, for the hold seconds after it, or while any
            module's alarm banner is up (if that option is on).

            Called often by other modules, so it makes no client calls.
            """
            if st["alarm"]:
                return True
            ra = st["resume_at"]
            # A resume time further away than the longest hold means the clock was set back: ignore it.
            if ra and 0 < ra - time.time() <= HOLD_MAX + 1:
                return True
            return bool(settings["anyalarm"] and HOST.alarm_up())

        def raise_alarm(kind, text, who=None, serial=0, gid=0, said=None, nm=""):
            """Add a reason to the alarm (client thread). Returns True if it was new, False if a repeat.

            The same speaker with the same text or words counts once (a whisper that names you is seen both
            by the journal and by the client event). A new alarm starts the sound clock and the banner; a
            further reason on an alarm already up only refreshes the window. nm is the player's name when
            the reason is about one, passed on with the serial to the shared alert so the banner can veil
            it in streamer mode.
            """
            fresh = not st["alarm"]
            again = False
            for r in st["alarm"]:
                if r["who"] == who:
                    if r["text"] == text or (said is not None and r["said"] == said):
                        return False
                    again = True
            now = time.time()
            # A new alarm gets a new number, so its banner is never swallowed by the banner's rate limit.
            if fresh:
                st["seq"] += 1
            st["alarm"].append({"kind": kind, "text": text, "who": who, "serial": int(serial or 0),
                                "gid": int(gid or 0), "at": now, "said": said, "nm": nm})
            # Only the newest reasons are kept.
            if len(st["alarm"]) > REASONS_MAX:
                del st["alarm"][:-REASONS_MAX]
            st["resume_at"] = 0.0
            if fresh:
                st["banner_seen"] = False
                rep = settings["repeat"]
                st["next_sound"] = now + rep if rep > 0 else 0.0
            # This speaker is already on the alarm: the banner already flashes for them.
            if again:
                refresh()
                return True
            HOST.alert(ALERT_KEY[kind], text, "alarm", who="%s#%d" % (who or text, st["seq"]), name=nm, serial=serial)
            refresh()
            return True

        def answer(how):
            """The alarm was answered (button, line click or banner click): skill loops go on after the hold.

            `how` is banner when the banner itself was clicked, so it is not taken down twice.
            """
            if not st["alarm"]:
                return
            last = st["alarm"][-1]
            st["alarm"] = []
            hold = settings["hold"]
            st["resume_at"] = time.time() + hold if hold > 0 else 0.0
            # The banner line is the module title and the text: matched by the text, so a banner from another
            # module is left up.
            if how != "banner" and banner_up() and last["text"] and str(ALERTS.line).endswith(last["text"]):
                ALERTS.dismiss()
            say("answered; %s" % (("skill loops go on in %d s." % hold) if hold
                                             else "skill loops go on."), Kit.HUE_GOOD)
            st["last_answered"] = last
            refresh()

        def alarm_tick(now):
            """Keep an alarm alive: notice a clicked banner, repeat the sound and flash the window line."""
            if not st["alarm"]:
                return
            if banner_up():
                st["banner_seen"] = True
            # The banner was up and is gone: it was clicked, so that answers the alarm.
            elif st["banner_seen"]:
                answer("banner")
                return
            rep = settings["repeat"]
            if rep > 0 and not st["next_sound"]:
                st["next_sound"] = now + rep
            # Also catches a clock set back, or a repeat time changed while the alarm was up.
            if rep > 0 and not 0 < st["next_sound"] - now <= rep:
                st["next_sound"] = now + rep
                sid = sound_of(st["alarm"][-1]["kind"])
                if sid:
                    API.PlaySound(sid)
            if not 0 < st["flash_at"] - now <= FLASH_SECS:
                st["flash_at"] = now + FLASH_SECS
                st["flash_on"] = not st["flash_on"]
                refresh()

        def read_me(now, p):
            """Read your character's name from the game (every NAME_EVERY seconds) and build the name patterns.

            The whole name matches as whole words. For a name of two words or more, any word of 4 letters or
            more matches too (Wolf in Grey Wolf). Nothing of the name is stored.
            """
            if st["my_name"] and 0 <= now - st["name_at"] < NAME_EVERY:
                return
            st["name_at"] = now
            name = str(p.Name or "").strip()
            st["me"] = int(p.Serial)
            if name and name != st["my_name"]:
                st["my_name"] = name
                st["name_re"] = re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(name), re.IGNORECASE)
                parts = [w for w in re.split(r"[^A-Za-z0-9']+", name) if w]
                words = [w for w in parts if len(w) >= 4]
                if len(parts) > 1 and words:
                    st["words_re"] = re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])"
                                                % "|".join(re.escape(w) for w in words), re.IGNORECASE)
                else:
                    # A one-word name is already covered by the whole-name pattern.
                    st["words_re"] = None

        def real_gump(g):
            """The client's Gump object (a build may hand back a wrapper with a Gump property)."""
            if g is None:
                return None
            try:
                inner = g.Gump
            except Exception:
                return g
            return inner if inner is not None else g

        def gone(g):
            """True when the gump was disposed; an unreadable gump counts as gone."""
            try:
                return bool(g.IsDisposed)
            except Exception:
                return True

        def mouse_readers():
            """Getters for the client's mouse position and last click times, found once by reflection.

            Returns a list of (getter, is_point) or None when this client build does not expose them.
            """
            if not mouse["looked"]:
                mouse["looked"] = True
                got = []
                t = Client._type("ClassicUO.Input.Mouse")
                if t is not None:
                    for name in ("Position", "LastLeftButtonClickTime", "LastRightButtonClickTime"):
                        m = Client._member(t, name)
                        # Each entry is (getter, whether it returns a point).
                        if m is not None:
                            got.append((m[0], name == "Position"))
                mouse["get"] = got or None
            return mouse["get"]

        def input_tick(now):
            """Has the mouse moved or clicked since the last look? Then you are at the keyboard.

            Moving or clicking marks asked_at, so a gump opening just after is most likely yours. Returns
            None when the mouse cannot be read on this build, True otherwise.
            """
            gs = mouse_readers()
            if not gs:
                return None
            cur = []
            for fn, point in gs:
                v = fn()
                cur.append((int(v.X), int(v.Y)) if point else int(v))
            cur = tuple(cur)
            prev, st["input"] = st["input"], cur
            if prev is not None and cur != prev:
                st["asked_at"] = now
            return True

        def typing_tick(now):
            """Did the keyboard go into or out of a text field since the last look? That is you typing.

            Only the change counts: a field that simply keeps the focus while you are away must not make
            every gump asked for.
            """
            t = bool(HOST.typing())
            prev, st["typing"] = st["typing"], t
            if prev is not None and t != prev:
                st["typed_at"] = st["asked_at"] = now

        def gump_tick(now):
            """Look at the newest server gump and raise the gump alarm if nobody asked for it (client thread).

            A gump is asked for when your mouse, typing or a closing gump of yours came just before, when it
            is a page of a window you had open in the last minute, when another module said it was opening
            it (HOST.gump_expected), or when its id is on the ignore list. A gump opened hidden is ignored.
            """
            typing_tick(now)
            # No mouse to read: fall back to the looser signs, a cursor answered or a double-click event.
            if input_tick(now) is None:
                up = bool(API.HasTarget("any"))
                if st["cursor_up"] and not up:
                    st["asked_at"] = now
                st["cursor_up"] = up
                # A double-click (the client event) counts as asking.
                if 0 <= now - st["used_at"] <= ASKED_SECS:
                    st["asked_at"] = max(st["asked_at"], st["used_at"])
            gid = int(API.HasGump() or 0)
            prev = st["gump_obj"]
            # Same gump still up: refresh its in-use time and skip the costly GetGump call.
            if gid and prev is not None and gid == st["gump_gid"] and not gone(prev):
                st["open_ids"][gid] = now
                return
            g = real_gump(API.GetGump(gid)) if gid else None
            if g is prev or (g is not None and prev is not None and gid == st["gump_gid"] and not gone(prev)):
                st["gump_obj"] = g
                if gid:
                    st["open_ids"][gid] = now
                return
            # A gump of yours closed (a button reply): whatever opens next follows from it.
            if prev is not None and st["gump_vis"] and gone(prev):
                st["asked_at"] = now
            st["gump_obj"], st["gump_gid"] = g, gid
            if g is None:
                st["gump_vis"] = False
                return
            visible = bool(g.IsVisible)
            st["gump_vis"] = visible
            st["last_gid"] = gid
            opened = st["open_ids"]
            seen_at = opened.get(gid)
            opened[gid] = now
            if len(opened) > OPEN_IDS_CAP:
                for k in sorted(opened, key=opened.get)[:len(opened) - OPEN_IDS_CAP]:
                    del opened[k]
            if HOST.gump_expected(gid, now):
                return
            # The first look only learns what was already open: that is not news.
            if not st["primed"] or not visible or gid in ignored_ids():
                return
            if seen_at is not None and 0 <= now - seen_at <= SAME_GUMP_SECS:
                return
            if 0 <= now - st["asked_at"] <= ASKED_SECS:
                return
            if settings["gump"]:
                raise_alarm("gump", "A gump opened by itself (id 0x%X)" % gid, "gump 0x%X" % gid, gid=gid)

        def staff_tick(now):
            """Look at the mobiles in view for a staff word in the name or title and raise the staff alarm.

            Uses the pass's shared mobile scan. Each mobile is checked once and cached, with up to two
            rechecks because a title can arrive after the mobile does. A staff mobile alarms again only
            after STAFF_GONE seconds out of view. The alarm carries the staff name for the streamer veil.
            """
            pat = marker_re()
            if pat is None:
                return
            # The pass's one shared scan of nearby mobiles.
            mobs = HOST.mobiles(STAFF_RANGE)
            checked, seen, me = st["checked"], st["staff_seen"], st["me"]
            if len(checked) > CACHE_CAP or pat is not st["checked_pat"]:
                # New staff words: look at everyone again.
                checked.clear()
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
                            # The name plus the first property line (the title) are checked together.
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
                    raise_alarm("staff", "Staff in view: %s" % (hit[3] or "someone"), "staff %X" % s, serial=s,
                                nm=hit[3])
            if len(seen) > 50:
                for k in [k for k, t in seen.items() if not 0 <= now - t <= STAFF_GONE]:
                    del seen[k]

        def speaker_serial(name):
            """The serial of the mobile in view called `name` (0 when none), so the alarm can follow them."""
            low = name.lower()
            try:
                for m in HOST.mobiles(STAFF_RANGE):
                    if str(m.Name or "").lower() == low:
                        return int(m.Serial)
            except Exception:
                pass
            return 0

        def quote(text):
            """A spoken line squeezed to one line and cut to QUOTE_MAX characters for the alarm text."""
            text = " ".join(str(text).split())
            return text if len(text) <= QUOTE_MAX else text[:QUOTE_MAX - 2] + ".."

        def speech_tick(now):
            """Read the new journal lines and raise the alarm when another player says your name (client thread).

            Your own lines are not alarms: a line you typed just before marks you as present, while a skill
            loop's spell words and system messages are ignored. The alarm carries the speaker's name for
            the streamer veil.
            """
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
                # Some lines come as one string, Name: text.
                if not name and ": " in text:
                    name, text = [x.strip() for x in text.split(": ", 1)]
                if not name or name.lower() == "system":
                    continue
                low = name.lower()
                # Your own line. If you typed just before, it is speech and so a sign you are there; a skill
                # loop's words and messages come under your name too and must not count.
                if my_low and low == my_low:
                    if 0 <= now - st["typed_at"] <= TYPED_SECS:
                        st["asked_at"] = now
                    continue
                if not settings["name"] or nre is None:
                    continue
                if nre.search(text) or (wre is not None and wre.search(text)):
                    raise_alarm("name", '%s said your name: "%s"' % (name, quote(text)), name,
                                serial=speaker_serial(name), said=text, nm=name)

        def heard_tick():
            """Raise the whisper alarm for whispers the client event handed over since the last tick.

            The alarm carries the speaker's name and serial for the streamer veil.
            """
            q = st["heard"]
            if not q:
                return
            st["heard"] = []
            my_low = st["my_name"].lower()
            for text, name, mt in q:
                if not name or name.lower() == "system" or (my_low and name.lower() == my_low):
                    continue
                if mt in WHISPER_TYPES and settings["whisper"]:
                    raise_alarm("whisper", '%s whispers to you: "%s"' % (name, quote(text)), name,
                                serial=speaker_serial(name), said=text, nm=name)

        def on_used(*args):
            """Client event ObjectUsed: remember when you last double-clicked, while the module is on."""
            if st["active"]:
                st["used_at"] = time.time()

        MT_LOW = {}

        def on_entry(*args):
            """Client event JournalEntryAdded: queue whispered lines for heard_tick (never raises)."""
            if not st["active"]:
                return
            for a in args:
                try:
                    # Read the type first and cache its lower-case name; the text and name are read only for a line
                    # that is wanted.
                    mt = a.MessageType
                    m = MT_LOW.get(mt)
                    if m is None:
                        m = str(mt).lower()
                        if len(MT_LOW) < 64:
                            MT_LOW[mt] = m
                except Exception:
                    continue
                if m in WHISPER_TYPES:
                    try:
                        text = str(a.Text or "")
                        name = str(a.Name or "")
                    except Exception:
                        continue
                    q = st["heard"]
                    if len(q) < QUEUE_CAP:
                        q.append((text, name, m))
                return

        def on_hits(*args):
            """Client event OnPlayerHitsChanged: wake the module at once when the hit trigger is on."""
            if settings["hit"] and not st.get("hit_poke"):
                st["hit_poke"] = True
                HOST.poke("skills.alarm", False)

        def hook_events():
            """Subscribe the three client events once per script run."""
            Kit.hook_once(hooks, "done", ("ObjectUsed", on_used), ("JournalEntryAdded", on_entry),
                          ("OnPlayerHitsChanged", on_hits))

        def hit_tick(p):
            """Raise the hit alarm when your hit points fall while you are not in war mode (client thread)."""
            # Off: nothing is read, so the first reading after it is switched on is only the baseline.
            if not settings["hit"]:
                st["hp"] = None
                return
            hp = int(p.Hits)
            prev = st["hp"]
            st["hp"] = hp
            if prev is None or p.IsDead or p.InWarMode or hp >= prev:
                return
            raise_alarm("hit", "You took %d damage while not fighting" % (prev - hp), "hit")

        def on_alarm_click():
            """Click on the alarm line (full window or minimized bar).

            Alt+click toggles auto-follow of the mobile that raised the alarm. A plain click answers the
            alarm. On the minimized bar with no alarm up, a double-click restores the window (the bar's own
            drag strip lies under this catcher).
            """
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

        def build_window():
            """Draw the Training Alarm window: a status line and three buttons, or the small bar when minimized.

            Rebuilt whole whenever the layout or the minimized state changes.
            """
            g, store, c = wnd.begin(W, Kit.MARGIN + 30 + Kit.GAP + 96 + Kit.MARGIN)
            M = Kit.MARGIN
            if st["minimized"]:
                c["line_w"] = MINI_W - 90
                # An invisible click catcher over the line, so the line itself is the answer button.
                c["alarm_hit"] = Kit.catcher(g, 14, 12, MINI_W - 90, MINI_H - 24, on_alarm_click,
                                             "Click: answer the alarm. Double-click: restore. Alt+click: auto-follow "
                                             "(again to stop)", movable=True)
            else:
                IW = W - 2 * M
                wnd.frame(g)
                yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, 96)
                c["status"] = Kit.add_label(g, "", M + 12, yb + 10, Kit.HUE_INFO)
                c["line2"] = Kit.add_label(g, "", M + 12, yb + 32, Kit.HUE_INFO)
                c["line_w"] = IW - 28
                c["alarm_hit"] = Kit.catcher(g, M + 6, yb + 6, IW - 12, 46, on_alarm_click,
                                             "Click: answer the alarm. Alt+click: auto-follow (again to stop)",
                                             movable=True)
                xb = M + 12
                for key, art, cap, tip, act in (
                        ("here", Kit.ART_OK, "I'm here", "Answer the alarm: skill loops go on (after the set pause)",
                         "answer"), ("test", Kit.ART_PLAY, "Test", "Raise a test alarm until you answer", "test"),
                        ("ignore", Kit.ART_CLOSE, "Ignore this gump", "Answer and ignore this gump from now on",
                         "ignore_gump")):
                    b = Kit.art_button(g, store, key, art, xb, yb + 62, cap, tip, on_click=queue(act))
                    xb += 35 + Kit.text_w(cap) + 14
                # The last button made is Ignore this gump: refresh shows it only for a gump alarm.
                c["ignore"] = b
            wnd.end(g)
            st["drawn"] = None
            refresh()

        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (240, 160), (MINI_W, MINI_H), TRAY_ICON,
                         cleanup, lock=True)

        def watching_text():
            """The status text when nothing is raised: which triggers are ticked."""
            on = [w for k, w in (("gump", "gumps"), ("staff", "staff"), ("name", "your name"), ("whisper", "whispers"),
                                 ("hit", "hits")) if settings[k]]
            if st["minimized"]:
                return "%s: %s" % (TITLE, ("watching " + ", ".join(on)) if on else "nothing ticked in settings")
            return ("Watching: " + ", ".join(on)) if on else "Nothing ticked in settings"

        def refresh():
            """Redraw the status lines (only when the text, colour or width changed).

            While an alarm waits the line flashes between two colours and shows how many more reasons are
            there; otherwise it shows what is watched and the pause countdown after an answer. In streamer
            mode the alarm text hides the speaker's name (veiled by serial) and your own character name.
            """
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return
            c = win["c"]
            lw = c.get("line_w", 200)
            al = st["alarm"]
            if al:
                r = al[-1]
                text = r["text"]
                if Kit.streamer:
                    if r["nm"]:
                        text = text.replace(r["nm"], Kit.veil("name", r["nm"], r["serial"]))
                    if st["name_re"] is not None:
                        text = st["name_re"].sub(Kit.veil("me", ""), text)
                line = ("%s: " % TITLE if st["minimized"] else "ALARM: ") + text
                hue = Kit.HUE_BAD if st["flash_on"] else Kit.HUE_TEXT
                line2 = ("+%d more. " % (len(al) - 1) if len(al) > 1 else "") + \
                    "Skill loops paused: click here or I'm here"
            else:
                left = st["resume_at"] - time.time() if st["resume_at"] else 0
                line, hue = watching_text(), Kit.HUE_INFO
                line2 = ("Skill loops go on in %d s" % int(left + 0.99)) if 0 < left <= HOLD_MAX + 1 else "All quiet"
            # The raw texts and colour are compared first, so the cutting to width happens only on a change.
            key = (line, hue, line2, lw)
            if key == st["drawn"]:
                return
            st["drawn"] = key
            line = Kit.fit(line, lw)
            Kit.set_text(c["status"], line, hue)
            if "line2" in c:
                Kit.set_text(c["line2"], Kit.fit(line2, lw), Kit.HUE_INFO)
            ig = c.get("ignore")
            if ig is not None:
                # The Ignore button only makes sense for a gump alarm.
                want = bool(al) and al[-1]["kind"] == "gump"
                if c.get("ignore_on") != want:
                    c["ignore_on"] = want
                    ig.IsVisible = want
                    b = win["store"][0].get("ignore")
                    if b is not None:
                        b.IsVisible = want

        def ignore_gump(from_alarm):
            """Put a gump id on the ignore list: the newest gump alarm's id, or the last server gump seen.

            The first is the window button, the second the settings page button.
            """
            gid = 0
            if from_alarm:
                for r in reversed(st["alarm"]):
                    if r["kind"] == "gump" and r["gid"]:
                        gid = r["gid"]
                        break
            if not gid:
                gid = st["last_gid"]
            if not gid:
                say("no server gump seen yet.", Kit.HUE_INFO)
                return
            if gid not in ignored_ids():
                cur = settings["ignore"].strip().strip(",")
                settings["ignore"] = (cur + ", " if cur else "") + "0x%X" % gid
                save_settings()
                HOST.refresh_settings(KEY)
                say("gump 0x%X ignored." % gid, Kit.HUE_INFO)

        def ignore_and_answer(action):
            """The window's Ignore this gump button: ignore the gump, then answer the alarm."""
            ignore_gump(True)
            answer("click")

        ACTIONS = {"follow": lambda action: Follow.toggle(action[1], TITLE), "answer": lambda action: answer("click"),
                "test": lambda action: raise_alarm("test", "Test alarm: answer it to go on", "test"),
                "ignore_gump": ignore_and_answer, "ignore_last": lambda action: ignore_gump(False)}

        def page_table(w):
            """Settings page layout: the triggers, the staff words and ignore ids, and the alarm timing."""
            fields = {"top": 32, "ldy": 4, "fh": 30, "align": True, "sh": 126}
            return (("TRIGGERS  (each pauses skill loops too)", (("check", "gump", "A server gump nobody asked for",
                         "Not within %.1f s of your mouse, typing or a gump closing; not a page of an open window "
                         "or an ignored id" % ASKED_SECS),
                        ("check", "staff", "Staff in view (a staff word in name or title)",
                         "Within %d tiles, a name or title holding a staff word (list below)" % STAFF_RANGE),
                        ("check", "name", "Someone says your name", "Read from the game (whole words, any case)"),
                        ("check", "words", "Or any word of it with 4 letters or more",
                         "For a name of two words or more: \"Wolf\" in \"Grey Wolf\"", {"dx": 34}),
                        ("check", "whisper", "Someone whispers to you", "Lines the client marks as whispered"),
                        ("check", "hit", "You take damage while not in war mode",
                         "Something hurts you while you train (off at first)")),
                     {"top": 32, "sh": 194}), ("STAFF AND GUMPS", (
                        ("text", "markers", "Staff words:", "Words marking a staff name or title, commas between "
                         "(whole words, any case; empty: no check)"), ("text", "ignore", "Gump ids to ignore:",
                         "Gump ids that never raise the alarm: hex (0x1A2B) or decimal, commas between"),
                        ("buttons", (("ignore_last", Kit.ART_OK, "Ignore last gump", "Ignore the last server gump seen",
                                      queue("ignore_last")),), {"bdy": 0, "stay": True}), ("note", last_gump_text(),
                         {"dx": 12 + 35 + Kit.text_w("Ignore last gump") + 14, "ndy": 3, "key": "last"})), fields),
                    ("ALARM  (sound: Settings > Alerts)", (("num", "repeat", "Repeat the sound every:",
                         "Seconds between sounds until you answer (0-%d, 0 = once)" % REPEAT_MAX, "s", 0, REPEAT_MAX),
                        ("num", "hold", "Loops stay paused after you answer:",
                         "Seconds loops stay paused after you answer (0-%d, 0 = none)" % HOLD_MAX, "s", 0, HOLD_MAX),
                        ("check", "anyalarm", "Any alarm pauses skill loops", "While any module's alarm banner waits "
                         "for a click (Ultima Tracker > Lookout, a red in your house)")), dict(fields, fw=40, ugap=12)))

        def last_gump_text():
            """The line under the Ignore last gump button: the id of the last server gump seen."""
            return ("Last server gump: 0x%X" % st["last_gid"]) if st["last_gid"] else "No server gump seen yet"

        def page_clicks(f):
            """Settings page hook: the Ignore last gump button queues a marker; handle it here."""
            # The click is taken from the queue now, so the page does not also run it a second time.
            page["skip"] = "ignore_last" in st["queue"]
            if page["skip"]:
                st["queue"].remove("ignore_last")
                ignore_gump(False)

        def page_adjust(f, new):
            """Settings page hook: clean the staff words and ignore ids and refresh the last gump text.

            The cleaned text is kept only when it really differs, so typing does not rewrite the setting.
            """
            if page["skip"]:
                new.update(settings)
                return
            for k in ("markers", "ignore"):
                v = _clean(new[k])
                new[k] = v if v != _clean(settings[k]) else settings[k]
            Kit.set_text(f.c["last"], last_gump_text(), Kit.HUE_INFO)

        def page_changed(old, new):
            """Settings page hook: a setting changed, so the window lines are redrawn."""
            st["drawn"] = None

        cfg = Kit.Page(settings, page_table, save_settings, page_changed, adjust=page_adjust, clicks=page_clicks)
        load_settings()

        def _start():
            """Part hook: reset the state, subscribe the events, register the alert kinds and draw the window.

            Publishes the service attention.up so other modules (Skill Bags) can pause while an alarm waits.
            """
            st.update({"shutting": False, "docked": False, "active": True, "alarm": [],
                       # An Ignore last gump click made while the module was off is kept.
                       "queue": [a for a in st["queue"] if a == "ignore_last"],
                       "resume_at": 0.0, "next_gump": 0.0, "gump_obj": None, "gump_gid": 0,
                       "gump_vis": False, "primed": False, "input": None,
                       "asked_at": 0.0, "used_at": 0.0, "cursor_up": False, "typing": None, "typed_at": 0.0,
                       "next_staff": 0.0, "checked": {}, "staff_seen": {}, "name_at": 0.0,
                       "next_hit": 0.0, "hp": None, "heard": [], "next_sound": 0.0,
                       "banner_seen": False, "flash_at": 0.0, "flash_on": False, "drawn": None,
                       # rd is a journal reader that sees only lines from now on.
                       "last_answered": None, "rd": Journal.reader(), "checked_pat": None,
                       "minimized": wnd.start_min()})
            load_settings()
            hook_events()
            for k, akey, label, snd in KINDS:
                HOST.alert_kind(akey, label, snd)
            cleanup.service("attention.up", is_up)
            build_window()
            wnd.dock()

        def _tick():
            """Part hook, client tick: run actions, then poll gumps, staff, speech, whispers and hit points.

            Every poll has its own interval and costs nothing while nothing changed. Runs only while the
            window exists; closing it with the X turns the module off.
            """
            if win["g"] is None:
                return
            # on_disposed turns the module off.
            if Kit.closed(win):
                return
            now = time.time()
            while st["queue"]:
                action = st["queue"].pop(0)
                if wnd.action(action):
                    continue
                fn = ACTIONS.get(action[0] if isinstance(action, tuple) else action)
                if fn is not None:
                    fn(action)
            # The pass's one shared player object.
            p = HOST.me()
            if p is None:
                return
            read_me(now, p)
            # Interval test that also recovers from a clock set back.
            if not 0 < st["next_gump"] - now <= GUMP_EVERY:
                st["next_gump"] = now + GUMP_EVERY
                gump_tick(now)
                # After the first look every later gump is news.
                st["primed"] = True
            if settings["staff"] and not 0 < st["next_staff"] - now <= STAFF_EVERY:
                st["next_staff"] = now + STAFF_EVERY
                staff_tick(now)
            speech_tick(now)
            heard_tick()
            # A hit event pokes the module, so damage is seen without waiting for the interval.
            if st.pop("hit_poke", False) or not 0 < st["next_hit"] - now <= HIT_EVERY:
                st["next_hit"] = now + HIT_EVERY
                hit_tick(p)
            alarm_tick(now)
            if not st["alarm"] and st["resume_at"]:
                if not is_up():
                    st["resume_at"] = 0.0
                refresh()

        def _stop():
            """Part hook: clear the alarm, save the settings and drop every reference."""
            st["shutting"] = True
            st["active"] = False
            st["alarm"] = []
            st["resume_at"] = 0.0
            save_settings()
            st["rd"] = None
            st["gump_obj"] = None
            cleanup.close()

        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                  "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed}

    def _part_bags():
        """Builds the Skill Bags part and returns its hooks.

        A rule pairs a bag in your backpack with an action (a skill, a tool from the backpack, or a
        plain double-click) and an item filter. With Auto on, the rule watches its bag and handles every
        new item; Run does one pass by hand. Each item is handled once, remembered per character, until
        the rule is Reset. One item at a time runs on the client tick with no waits: the cursor is
        claimed while a skill's target is awaited and the shard's answer is read from the shared journal.
        Nothing runs while you are hidden (option), fighting, in war mode, dead, in a guard zone (an
        option), holding a cursor yourself or while a Training Alarm waits for you. Results per item
        are listed in a Results window and can be exported to a text file.
        """
        # Saved keys: SkillBags_settings (options), SkillBags_rules (the rules), SkillBags_done (handled
        # items per rule), SkillBags_pos and SkillBags_min (window), SkillBags_results_pos (Results window).
        KEY = "skillbags"
        TITLE = "Skill Bags"
        SETTINGS_KEY = "SkillBags_settings"
        POS_KEY = "SkillBags_pos"
        MIN_KEY = "SkillBags_min"
        RULES_KEY = "SkillBags_rules"
        DONE_KEY = "SkillBags_done"
        W = 740
        MINI_W, MINI_H = 240, 46
        TRAY_ICON = 0x0E76
        # One rule per row: the rule's line and, under it, the shard's last answer.
        ROW_H = 42
        # The window grows by ROW_H per rule; eight rows still fit a 1080 pixel screen.
        MAX_RULES = 8
        # Handled items remembered per rule; the oldest are dropped.
        MAX_DONE = 300
        # How many scans an item's name may stay unknown before the item is skipped (the server never
        # sent its tooltip).
        NAME_SCANS_MAX = 6
        # Seconds between full listings of a bag whose item count has not changed (items in inner bags).
        RELIST_EVERY = 5.0
        # A bag's name is re-read this often: the window rows ask for it several times a second.
        BAG_NAME_EVERY = 2.0
        # Seconds to wait for the skill's target cursor; OPEN_TIMEOUT is the same for a bag opening.
        TARGET_TIMEOUT = 3.0
        OPEN_TIMEOUT = 2.5
        OPEN_RETRY = 6.0
        BUSY_RETRY = 1.5
        # Answers of must wait or no cursor before an item is given up on.
        MAX_BUSY = 4
        # The shard's skill timers: a skill rule's delay never goes under its skill's timer, and a must
        # wait answer to a skill is waited out and not counted toward MAX_BUSY. The short ones are
        # listed by name.
        SKILL_TIMER = 10.0
        SKILL_TIMER_SHORT = {"item identification": 3.0, "arms lore": 3.0, "detect hidden": 3.0}
        MIN_DELAY, MAX_DELAY = 0.5, 60.0
        DEFAULT_RETRIES = 1
        CHECK_EVERY = 0.25
        SCAN_EVERY = 0.5
        # The tool the Lockpicking action uses.
        LOCKPICK_GRAPHIC = 0x14FC
        # Journal phrases that mean try this item again shortly. The OK, FAIL and SKIP phrases are per
        # action in RULE_ACTIONS. They are RunUO defaults, so
        # the window's Last line shows what the shard really said.
        BUSY_WORDS = ("must wait", "too far away", "cannot reach", "can't reach",
                      "can't see that", "cannot see that", "already casting", "you are busy")
        GUARD_STATUS = "Paused: guard zone"
        # The guard zone is not known yet (the strict reading pauses too).
        UNKNOWN_STATUS = HOLD_TEXT["unknown"]
        RES_POS_KEY = "SkillBags_results_pos"
        # Results kept per rule for the session; the oldest are dropped.
        RES_KEEP = 200
        RES_ROWS = 16
        RES_W = 680
        RES_ROW_H = 18
        RES_KEY = "skillbags.results"
        RES_TITLE = "Skill Bags Results"
        RES_MIN_W = 500
        # The Results window's height apart from its rows.
        RES_FIXED = 2 * Kit.MARGIN + 30 + Kit.GAP + 30 + 24 + 8
        RES_EMPTY = "No results shown. Click a rule's Results."
        RES_ANSWER_MAX = 160
        # Export file name: the player's serial and the rule number.
        EXPORT_NAME = "SkillBags_%08X_rule%d.txt"
        # Item Identification: words in the item's attribute list (the label the client shows after a
        # successful identification) that make it magic: the weapon and armour attribute names and the
        # slayer names.
        ITEMID_MAGIC = ("durable", "substantial", "massive", "fortified", "indestructable",
                        "indestructible", "defense", "guarding", "hardening", "fortification",
                        "invulnerability", "accurate", "ruin", "might", "force", "power", "vanquishing",
                        "silver", "slaying", "slaughter", "thrashing", "repond", "terathan", "bane",
                        "reptilian death", "dismissal", "gargoyle's foe", "damnation", "exorcism",
                        "ophidian", "spider's death", "arachnid doom", "dousing", "dissipation",
                        "vacuum", "elemental health", "earth shatter", "blood drinking", "summer wind",
                        "elemental ban", "slayer", "magic")
        # In the label when the identification did not take.
        ITEMID_UNKNOWN = "unidentified"
        # The word each answer code is listed under, per action; other codes use CODE_TEXT.
        RESULT_WORDS = {"itemid": {2: "not certain"}, "armslore": {2: "not certain", 4: "read"},
                        "tasteid": {2: "not certain", 4: "read"},
                        "removetrap": {1: "disarmed", 2: "trap, not disarmed", 3: "no trap"},
                        "lockpick": {1: "unlocked", 2: "still locked", 3: "not locked"},
                        "cartography": {1: "decoded", 2: "not decoded", 3: "can't decode"}}
        # Whole words only, so a plain silver ring is not a Silver slayer.
        ITEMID_MAGIC_RE = re.compile(r"\b(" + "|".join(ITEMID_MAGIC) + r")\b")
        # A charges part such as [Clumsiness : 5] counts as magic too.
        ITEMID_CHARGES_RE = re.compile(r"\[[^\]]*:\s*\d+\s*\]")
        ITEMID_MAGIC_WORD = re.compile(r"\bmagic\b")
        # Each action: key, caption, kind (skill, tool, use, cskill or ctool), what (skill name or tool
        # graphic), default delay, default filter index, then the OK, FAIL and SKIP phrases (lower case).
        RULE_ACTIONS = [("itemid", "Item Identification", "skill", "Item Identification", 3.2, 0,
             (), ("not certain", "no idea how much", "tell much about it"), ()),
            ("armslore", "Arms Lore", "skill", "Arms Lore", 3.2, 0, (), ("not certain", "tell much about it"), ()),
            ("tasteid", "Taste Identification", "skill", "Taste Identification", 10.2, 0,
             (), ("not certain", "tell much about it", "can't tell"), ()),
            ("removetrap", "Remove Trap", "skill", "Remove Trap", 10.2, 1,
             ("render the trap harmless", "successfully"), ("fail to disarm",),
             ("doesn't appear to be trapped", "isn't trapped", "not trapped")),
            ("lockpick", "Lockpicking (uses lockpicks)", "tool", LOCKPICK_GRAPHIC, 1.5, 1,
             ("lock quickly yields",), ("unable to pick the lock",),
             ("does not appear to be locked", "cannot be picked by normal means", "did not need to be unlocked")),
            ("cartography", "Cartography (decode maps)", "use", None, 1.0, 3,
             ("successfully decode",), ("fail to make anything of the map",),
             ("too difficult to attempt to decode", "not a map")),
            ("use", "Double-click each item", "use", None, 1.0, 0, (), (), ()),
            ("cskill", "Custom skill (name in Custom)", "cskill", None, 10.2, 0, (), (), ()),
            ("ctool", "Custom tool (graphic in Custom)", "ctool", None, 1.5, 0, (), (), ()),]
        ACTION_NAMES = [a[1] for a in RULE_ACTIONS]
        FILTERS = [("all", "Every item"), ("containers", "Containers only"),
                   ("graphics", "Graphics in Text (hex)"), ("name", "Name contains Text")]
        FILTER_NAMES = [f[1] for f in FILTERS]
        CODE_TEXT = {1: "OK", 2: "failed", 3: "skipped", 4: "done"}
        settings = {"hidden": True, "war": True, "open": True, "retries": DEFAULT_RETRIES, "guard": True}
        DEFAULTS = dict(settings)
        rules = []
        # The state shared with the window and the dock; the per-run keys are set again in _start.
        st = {"minimized": False, "shutting": False, "docked": False, "queue": []}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        cleanup, queue, say = Kit.basics(st, TITLE)
        # The settings page: its form, the controls of each rule row, and when it is read next.
        page = {"f": None, "rows": [], "next_read": 0.0}
        # The Results window: one at a time, showing one rule's results.
        resw = {"g": None, "rule": None, "c": {}, "rows": [], "page": 0, "dirty": False, "minimized": False,
                "shutting": False, "docked": False, "queue": []}

        def esc(s):
            """Make text safe for the saved rules string (no bar or tilde, its separators)."""
            return str(s or "").replace("|", "/").replace("~", "-")

        def clamp_delay(v, default):
            """A delay read as a number and held between MIN_DELAY and MAX_DELAY; `default` when it is not one."""
            try:
                v = float(v)
            except Exception:
                return default
            return max(MIN_DELAY, min(MAX_DELAY, v))

        def new_rule(action=0):
            """A fresh rule dict with the action's default filter and delay."""
            a = RULE_ACTIONS[action]
            return {"action": action, "bag": 0, "filt": a[5], "text": "", "custom": "",
                    "delay": a[4], "deep": False, "auto": False, "done": {}, "order": []}

        def rule_action(r):
            """The RULE_ACTIONS row of the rule's action."""
            return RULE_ACTIONS[r["action"]]

        def skill_floor(r):
            """The shard's timer in seconds for the rule's skill, 0 for tool and use rules.

            A skill rule's delay is never set below this.
            """
            a = RULE_ACTIONS[r["action"]]
            name = a[3] if a[2] == "skill" else r["custom"].strip() if a[2] == "cskill" else ""
            return SKILL_TIMER_SHORT.get(name.lower(), SKILL_TIMER) if name else 0.0

        def parse_graphics(text):
            """Graphic ids from a text of numbers split by commas or semicolons (hex with 0x, or decimal).

            A bare hex number such as 14FC is read as hex when it is not a decimal.
            """
            out = []
            for part in str(text or "").replace(";", ",").split(","):
                part = part.strip()
                if not part:
                    continue
                try:
                    out.append(int(part, 16) if part.lower().startswith("0x") else int(part, 0))
                except Exception:
                    # Not a plain number: try it as hex, quietly (a failure here is expected).
                    with Kit.quiet:
                        out.append(int(part, 16))
            return out

        def load_settings():
            """Read the saved options, rules and handled-item lists for this character.

            Settings are bar separated, rules are bar separated records of tilde separated fields, and the
            handled items are comma separated serial:code pairs, one list per rule in rule order. Bad
            records are skipped.
            """
            p = Kit.get_var(SETTINGS_KEY).split("|")
            if len(p) >= 4:
                for n, k in enumerate(("hidden", "war", "open")):
                    settings[k] = p[n] == "1"
                try:
                    settings["retries"] = max(0, min(9, int(p[3])))
                except Exception:
                    settings["retries"] = DEFAULT_RETRIES
            # Saves without the sixth field keep the guard pause on.
            settings["guard"] = (p[5] == "1") if len(p) >= 6 else True
            del rules[:]
            raw = Kit.get_var(RULES_KEY)
            if raw:
                for chunk in raw.split("|"):
                    f = chunk.split("~")
                    if len(f) < 8:
                        continue
                    try:
                        r = new_rule(max(0, min(len(RULE_ACTIONS) - 1, int(f[0]))))
                        r.update({"bag": int(f[1]) if f[1] else 0, "filt": max(0, min(len(FILTERS) - 1, int(f[2]))),
                                  "text": f[3], "custom": f[4]})
                        # Never under the skill's timer, even for a rule saved with a shorter delay.
                        r.update({"delay": max(clamp_delay(f[5], rule_action(r)[4]), skill_floor(r)),
                                  "deep": f[6] == "1", "auto": f[7] == "1"})
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
            """Write the options, the rules and the handled items to the shared variable store.

            The fifth settings field is kept (always 0) so the saved format stays the same.
            """
            Kit.put_var(SETTINGS_KEY, "|".join(["1" if settings["hidden"] else "0", "1" if settings["war"] else "0",
                "1" if settings["open"] else "0", str(settings["retries"]), "0", "1" if settings["guard"] else "0"]))
            Kit.put_var(RULES_KEY, "|".join("~".join([str(r["action"]), str(r["bag"]), str(r["filt"]), esc(r["text"]),
                          esc(r["custom"]), "%.2f" % r["delay"], "1" if r["deep"] else "0",
                          "1" if r["auto"] else "0"]) for r in rules))
            save_done()

        def save_done():
            """Write the handled items, one comma list of serial:code per rule, bar separated."""
            Kit.put_var(DONE_KEY, "|".join(",".join("%d:%d" % (s, r["done"][s]) for s in r["order"] if s in r["done"])
                for r in rules))

        def mark_done(r, serial, code):
            """Record that an item was handled with a result code (1 ok, 2 failed, 3 skipped, 4 done).

            Keeps at most MAX_DONE per rule and flags the marks to be saved on a timer, not on every item.
            """
            if serial not in r["done"]:
                r["order"].append(serial)
            r["done"][serial] = code
            order = r["order"]
            # The oldest are dropped in one cut.
            if len(order) > MAX_DONE:
                k = len(order) - MAX_DONE
                done = r["done"]
                for old in order[:k]:
                    done.pop(old, None)
                del order[:k]
            st["save_done"] = True

        def result_tag(a, code, answer):
            """The word an item's result is listed and counted under (magic, plain, disarmed, failed ...).

            Item Identification reads the answer: charges or an attribute word in the attribute list is
            magic, no label at all is no answer, and the unidentified marker is unidentified.
            """
            if a[0] == "itemid" and code in (1, 4):
                low = (answer or "").lower()
                if not low:
                    return "no answer"
                if ITEMID_UNKNOWN in low:
                    return "unidentified"
                if ITEMID_CHARGES_RE.search(low):
                    return "magic"
                # The attribute list starts at the bracket: words count only there, so a plain silver ring is not
                # a slayer.
                k = low.find("[")
                if k >= 0:
                    return "magic" if ITEMID_MAGIC_RE.search(low, k) else "plain"
                return "magic" if ITEMID_MAGIC_WORD.search(low) else "plain"
            words = RESULT_WORDS.get(a[0])
            if words is not None and code in words:
                return words[code]
            return CODE_TEXT.get(code, "done")

        def answer_of(j):
            """The shard's answer to a job as it was said, or an empty text when nothing came.

            Order: the line a phrase matched, else a line spoken by the item itself (named after it, or an
            attribute list), else the last system line, else the last line seen.
            """
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
                if ((nm and (ln == nm or (len(nm) >= 3 and nm in text.lower()))) or text.lstrip().startswith("[")):
                    return text
                if best is None and (not name or ln == "system"):
                    best = text
            return best if best is not None else raw[-1][0]

        def add_result(r, serial, code, name, answer, tag=None):
            """Add an item's result to the rule's list (newest last).

            An item handled again replaces its old line; at most RES_KEEP are kept and the answer text is
            cut. Marks the Results window for a redraw when it shows this rule.
            """
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
            """Forget the rule's listed results (the items stay marked done)."""
            r.pop("_res", None)
            r.pop("_rescount", None)
            if resw["rule"] is r:
                resw["dirty"] = True

        def counts_text(r):
            """The count line for the Results window, such as 24 items: 5 magic, 19 plain.

            Worked out when the results change and kept on the rule.
            """
            txt = r.get("_rescount")
            if txt is None:
                res = r.get("_res") or []
                if not res:
                    txt = "No results yet."
                else:
                    cnt = {}
                    for e in res:
                        cnt[e[4]] = cnt.get(e[4], 0) + 1
                    txt = "%s: %s" % (Kit.count(len(res), "item"), ", ".join(["%d %s" % (n, t) for t, n in
                                                        sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))]))
                r["_rescount"] = txt
            return txt

        # The client's item lookup by serial.
        get_item = Kit.find_item

        def bag_name(r, short=True):
            """The bag's name for the rows (with its serial when `short` is False), cached for BAG_NAME_EVERY."""
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
                    name = safe(lambda: str(it.Name or ""), "") or "0x%08X" % r["bag"]
                r["_bagname"] = (r["bag"], now + BAG_NAME_EVERY, name)
            return name if short else "%s  0x%08X" % (name, r["bag"])

        def invalidate(r=None):
            """Drop the cached bag listings (and names) of one rule or all of them, so the next look lists again.

            Called when a rule, its filter or its bag changes.
            """
            for rule in ([r] if r is not None else rules):
                rule.pop("_cache", None)
                rule.pop("_bagname", None)

        def matches(r, it):
            """Does this item pass the rule's filter? True or False, or None when its name is not known yet."""
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
                # No name yet: ask the server for the tooltip (the first line is the name) and try again later.
                if not name:
                    try:
                        name = str(API.ItemNameAndProps(it.Serial, False) or "").split("\n")[0]
                    except Exception:
                        name = ""
                if not name:
                    return None
                return want in name.lower()
            return True

        def bag_count(serial):
            """The bag's item count as the client knows it (one cheap call), -1 when it cannot be read."""
            try:
                return int(API.Contents(serial) or 0)
            except Exception:
                return -1

        def bag_items(r, i, now, may_list=True):
            """The rule's items that pass its filter, as (items, how many still wait for a name, listed now).

            The bag is listed again (one API call, one filter check per item) only when its item count
            changed, every RELIST_EVERY seconds, or after invalidate. Between listings the cached list
            serves, and only items whose name has not come yet are asked again; an item whose name never
            comes within NAME_SCANS_MAX scans is skipped (code 3). With `may_list` False (another bag was
            listed in this pass) a due listing waits: the cache serves and listed is None, or None comes
            back when there is no cache yet. Returns None in that last case.
            """
            bag = get_item(r["bag"]) if r["bag"] else None
            if bag is None:
                r.pop("_cache", None)
                return [], 0, False
            cache = r.get("_cache")
            count = bag_count(r["bag"])
            listed = False
            if (cache is None or cache["count"] != count or now >= cache["relist"] or cache["bag"] != r["bag"]):
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
                    # A name still unknown for an item already handled counts as a match, so it is not asked again.
                    if m is None and serial in r["done"]:
                        m = True
                    if m is None:
                        pending.append((serial, it))
                    elif m:
                        out.append((serial, it))
                        scans.pop(serial, None)
                cache = {"bag": r["bag"], "count": count, "relist": now + RELIST_EVERY,
                         "items": out, "pending": pending, "scans": scans}
                r["_cache"] = cache
            # The names asked for last time may have come: check only those items.
            elif cache["pending"]:
                still = []
                for serial, it in cache["pending"]:
                    m = matches(r, it)
                    if m is None:
                        still.append((serial, it))
                    elif m:
                        cache["items"].append((serial, it))
                cache["pending"] = still
            scans = cache["scans"]
            gave_up = []
            for serial, it in cache["pending"]:
                n = scans.get(serial, 0) + 1
                scans[serial] = n
                # Give the item up: it is added to the items, marked skipped and reported once.
                if n >= NAME_SCANS_MAX:
                    scans.pop(serial, None)
                    gave_up.append((serial, it))
                    cache["items"].append((serial, it))
                    mark_done(r, serial, 3)
                    add_result(r, serial, 3, "", "its name never came", "skipped (no name)")
                    say("0x%08X skipped, its name never came (rule %d)." % (serial, i + 1), Kit.HUE_INFO)
            # The pending list is rebuilt once, not with a remove per item.
            if gave_up:
                gone = set(s for s, _ in gave_up)
                cache["pending"] = [p for p in cache["pending"] if p[0] not in gone]
            if len(scans) > MAX_DONE:
                scans.clear()
            return cache["items"], len(cache["pending"]), listed

        def bag_opened(serial):
            """True when the client has seen inside the bag (opened, or it holds items it knows of)."""
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

        def due(t, now):
            """True when time `t` has come. A t further than MAX_DELAY ahead (a clock set back) counts as due."""
            return not 0 < t - now <= MAX_DELAY

        def ensure_open(r, now, on_run=True):
            """A bag the client has not looked in shows no items: open it once on Run and wait for it.

            Returns True when the contents are usable. Only a bag in your backpack is ever opened, only on a
            Run pass (never for Auto) and only if the open option is on; it is retried after OPEN_RETRY.
            """
            serial = r["bag"]
            if not serial or not Kit.in_pack(serial):
                return False
            if bag_opened(serial):
                st["opening"].pop(serial, None)
                r["_closed"] = False
                return True
            r["_closed"] = True
            if not settings["open"] or not on_run:
                return False
            o = st["opening"].get(serial)
            if o is None or due(o + OPEN_TIMEOUT + OPEN_RETRY, now):
                st["opening"][serial] = now
                API.UseObject(serial)
            return False

        def blocked(now):
            """Why no rule may run right now (a short status text), or None when one may.

            Order: paused by the player, no player, dead, hidden (option), war mode, guard zone, any fight
            hold from the mother (hurt, hostile near, item on the cursor, alarm waiting), then a cursor up.
            """
            if st["paused"]:
                return "Paused"
            p = HOST.me()
            if p is None:
                return "No player"
            # The mother's one fight test, shared by every skill loop.
            why = HOST.fight_hold(now)
            if why == "dead":
                return "Dead"
            if settings["hidden"] and p.IsHidden:
                return "Hidden"
            # War mode always pauses: the shard's rules, not a setting.
            if why == "war":
                return "War mode"
            gp = st["guard_paused"]
            # The zone is not known yet.
            if gp == "unknown":
                return UNKNOWN_STATUS
            # No macroing in a guard zone.
            if gp:
                return GUARD_STATUS
            if why:
                return "Paused: " + HOLD_TEXT.get(why, why)
            if HOST.cursor_busy(KEY):
                return "Cursor busy"
            if API.HasTarget("any"):
                return "Cursor up"
            return None

        def pick_next(now):
            """The next (rule index, rule, serial, item) to handle, or None.

            Takes the first not-done, not-waiting item of a rule that is on Auto or in a Run pass. Rules are
            looked at round robin and at most one bag is listed per scan, so several deep bags are not all
            listed twice a second and the rules take turns. Also ends a finished Run pass and reports it.
            """
            n = len(rules)
            if not n:
                return None
            start = st["rr"] % n
            listed = False
            for k in range(n):
                i = (start + k) % n
                r = rules[i]
                if not (r["auto"] or i in st["run"]) or not r["bag"]:
                    r.pop("_closed", None)
                    continue
                # A custom tool runs only on Run, never on Auto: the graphic is the player's own text.
                if rule_action(r)[2] == "ctool" and i not in st["run"]:
                    if r["auto"]:
                        auto_off(i, r)
                        say("rule %d: a custom tool runs only on Run." % (i + 1), Kit.HUE_BAD)
                    continue
                if not Kit.in_pack(r["bag"]):
                    st["run"].discard(i)
                    st["budget"].pop(i, None)
                    say("rule %d: its bag isn't in your backpack." % (i + 1), Kit.HUE_BAD)
                    if r["auto"]:
                        auto_off(i, r)
                    continue
                if not ensure_open(r, now, i in st["run"]):
                    continue
                got = bag_items(r, i, now, not listed)
                # This bag needs a listing but another bag already had this scan's.
                if got is None:
                    continue
                items, unknown, did = got
                if did:
                    listed = True
                    # The next scan starts at the following rule, so it lists another bag first.
                    st["rr"] = i + 1
                r["_count"] = (sum(1 for s, it in items if s in r["done"]), len(items))
                waiting = False
                budget = st["budget"]
                if i in st["run"] and rule_action(r)[2] == "ctool" and i not in budget:
                    # A custom tool pass stops at its count: the items left, with their retries.
                    budget[i] = (r["_count"][1] - r["_count"][0] + unknown) * (1 + settings["retries"])
                for serial, it in items:
                    if serial in r["done"]:
                        continue
                    if not due(st["later"].get((i, serial), 0.0), now):
                        # An item waits for its retry: a Run pass must not end before it.
                        waiting = True
                        continue
                    if i in budget:
                        if budget[i] <= 0:
                            st["run"].discard(i)
                            budget.pop(i, None)
                            say("rule %d stopped at its count (%s)." % (i + 1, bag_name(r)), Kit.HUE_INFO)
                            break
                        budget[i] -= 1
                    return i, r, serial, it
                # Everything is handled and the listing is fresh: the Run pass is over.
                if i in st["run"] and not unknown and not waiting and did is not None:
                    st["run"].discard(i)
                    st["budget"].pop(i, None)
                    say("%s on %s, %d of %d handled." % (
                        rule_action(r)[1], bag_name(r), r["_count"][0], r["_count"][1]), Kit.HUE_GOOD)
            return None

        def auto_off(i, r):
            """Stop a rule that cannot run: end its Run pass and turn its Auto off, saved and shown.

            The window's and the page's ticked boxes would otherwise turn it back on and the error would
            repeat twice a second.
            """
            st["run"].discard(i)
            r["auto"] = False
            save_settings()
            if i < len(win["rows"]):
                win["rows"][i]["auto"].IsChecked = False
            if page["f"] is not None:
                HOST.refresh_settings(KEY)

        def start_job(i, r, serial, it, now):
            """Start the use of the rule's action on one item. Returns False when nothing was started.

            A skill or tool use claims the target cursor and opens a journal reader before it acts. A plain
            use double-clicks the item and goes straight to the answer wait. A rule that cannot run (no
            skill name, no tool graphic) is turned off with a message; a missing tool waits 10 seconds.
            """
            a = rule_action(r)
            kind = a[2]
            # The job: phase target (waiting for the cursor) or recover (waiting for the answer); lines are
            # lower case journal lines and raw holds the same as said, with the speaker.
            j = {"rule": i, "serial": serial, "t": now, "phase": "target", "reader": None, "lines": [], "raw": [],
                 "name": safe(lambda: str(it.Name or ""), "")}
            if kind in ("skill", "cskill"):
                name = a[3] if kind == "skill" else r["custom"].strip()
                if not name:
                    say("rule %d needs a skill name in its Custom box." % (i + 1), Kit.HUE_BAD)
                    auto_off(i, r)
                    return False
                # Claim the cursor so no other module aims at it while the skill's target is awaited.
                HOST.claim_cursor(KEY, TARGET_TIMEOUT + 0.5)
                j["reader"] = Journal.reader()
                API.UseSkill(name)
            elif kind in ("tool", "ctool"):
                graphic = a[3]
                if kind == "ctool":
                    gl = parse_graphics(r["custom"])
                    graphic = gl[0] if gl else 0
                    if not graphic:
                        say("rule %d needs a tool graphic in its Custom box." % (i + 1), Kit.HUE_BAD)
                        auto_off(i, r)
                        return False
                tool = API.FindType(int(graphic), API.Backpack)
                if not tool:
                    if due(st["no_tool"].get(i, 0.0), now):
                        st["no_tool"][i] = now + 10.0
                        say("no tool 0x%04X in your backpack for rule %d." % (int(graphic), i + 1), Kit.HUE_BAD)
                    st["later"][(i, serial)] = now + 10.0
                    st["run"].discard(i)
                    return False
                HOST.claim_cursor(KEY, TARGET_TIMEOUT + 0.5)
                j["reader"] = Journal.reader()
                API.UseObject(tool.Serial)
            # A use rule: double-click the item itself; there is no cursor to wait for.
            else:
                j["reader"] = Journal.reader()
                API.UseObject(serial)
                j["phase"] = "recover"
            st["job"] = j
            return True

        # The prefixes of Virtue Assistant's own journal lines, found once.
        va_pref = {"t": None}

        def va_prefixes():
            """The lower case journal prefixes of every Virtue Assistant module and part, read once.

            Those lines are printed by the client itself and must never be read as the shard's answer.
            """
            t = va_pref["t"]
            if t is None:
                out = set([APP_NAME.lower() + ":"])
                for sl in HOST.slots:
                    out.add(str(sl.title).lower() + ":")
                    for pt in (sl.parts or ()):
                        if len(pt) > 1:
                            out.add(str(pt[1]).lower() + ":")
                t = va_pref["t"] = tuple(out)
            return t

        def is_answer(j, ln):
            """May this journal line be the shard's answer to the job?

            Not the client's own lines, not another mobile's speech. Yes for the shard's (no speaker or
            System) and for the item's own overhead line (speaker is the item's name, or a label starting
            with a bracket).
            """
            kind = (ln.kind or "").upper()
            if kind == "CLIENT" or ln.low.startswith(va_prefixes()):
                return False
            who = (ln.name or "").strip().lower()
            if not who or who == "system":
                return True
            if kind != "OBJECT":
                return False
            # The item had no name at the start: read it once more now.
            if not j["name"] and not j.get("named"):
                j["named"] = True
                it = get_item(j["serial"])
                j["name"] = safe(lambda: str(it.Name or "") if it is not None else "", "")
            return who == j["name"].strip().lower() or ln.text.startswith("[")

        def job_result(j, a):
            """What the journal said since the attempt: busy, ok, fail, skip or None.

            Collects the new answer lines (capped), then checks the phrase lists in order of priority: busy,
            skip, ok, fail. Remembers the line that decided it for the window's Last line.
            """
            rd = j["reader"]
            if rd is None:
                return None
            lines, raw = j["lines"], j["raw"]
            came = False
            for ln in rd.new():
                if ln.text and not ln.text.startswith(TITLE):
                    if not is_answer(j, ln):
                        continue
                    lines.append(ln.low)
                    came = True
                    raw.append((ln.text, ln.name or ""))
                    # A cap: a busy fight while waiting would otherwise fill it.
                    if len(lines) > 40:
                        del lines[:-40]
                        del raw[:-40]
            if not lines:
                return None
            # Nothing new since last time: the same answer as before.
            if not came:
                return j.get("res")
            # First phrase found wins; busy first so a must wait is never read as a failure.
            hit = next(((rs, k) for rs, words in (("busy", BUSY_WORDS), ("skip", a[8]), ("ok", a[6]), ("fail", a[7]))
                        for w in words for k in range(len(lines)) if w in lines[k]), None)
            if hit is not None:
                j["match"] = lines[hit[1]]
                j["match_raw"] = raw[hit[1]][0]
            res = j["res"] = hit[0] if hit is not None else None
            return res

        def finish_job(j, r, res, now):
            """Close the job with its result: mark the item, plan the retry or the next scan, set the status.

            busy: a skill still on its timer waits it out uncounted; otherwise it is retried after
            BUSY_RETRY and given up after MAX_BUSY tries. fail: retried up to the retries option, then
            marked failed. Anything else marks the item done (ok, skip, or no phrase matched).
            """
            i, serial = j["rule"], j["serial"]
            key = (i, serial)
            nxt = None
            floor = skill_floor(r) if res == "busy" else 0.0
            # The skill's timer is still running: wait it out, not counted as a busy try.
            if floor > 0 and "must wait" in (j.get("match") or ""):
                st["later"][key] = now + floor
                nxt = now + min(r["delay"], floor)
            elif res == "busy":
                n = st["busy_n"].get(key, 0) + 1
                if n >= MAX_BUSY:
                    st["busy_n"].pop(key, None)
                    mark_done(r, serial, 2)
                    add_result(r, serial, 2, j["name"], answer_of(j) or "no answer from the shard", "no answer")
                    say("giving up on 0x%08X (no answer from %s)." % (serial, rule_action(r)[1]), Kit.HUE_BAD)
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
            # The rule's delay runs from the attempt, so the recover wait is part of it; a busy answer gets the
            # whole delay again.
            waited = max(0.0, now - j.get("t", now))
            st["next_scan"] = nxt if nxt is not None else now + (
                r["delay"] if res == "busy" else max(MIN_DELAY, r["delay"] - waited))
            st["status"] = "%s: %s" % (rule_action(r)[1], res or "done")
            if j.get("match"):
                r["_last"] = "%s: %s" % (res, j["match"])
            elif j["lines"]:
                r["_last"] = "%s, no phrase matched; the shard said: %s" % (res or "no answer", j["lines"][-1])
            else:
                r["_last"] = "%s, no journal line in %.1f s" % (res or "no answer", max(0.0, now - j.get("t", now)))
            # Caps, like every growing dict.
            if len(st["later"]) > 400:
                for k in [k for k, t in st["later"].items() if due(t, now)]:
                    st["later"].pop(k, None)
            if len(st["busy_n"]) > 400:
                st["busy_n"].clear()
            if len(r.get("_tries", {})) > MAX_DONE:
                r["_tries"].clear()

        def job_step(now):
            """Advance the running job one step (client tick): wait for the cursor, target, then wait the answer.

            Phase target: finish at once if the journal already answered, else target the item when the
            cursor is the skill's own kind. Phase recover: give the server the rule's delay to answer, but
            end early on a busy, skip or fail answer.
            """
            j = st["job"]
            r = rules[j["rule"]] if j["rule"] < len(rules) else None
            if r is None:
                HOST.release_cursor(KEY)
                st["job"] = None
                return
            a = rule_action(r)
            if j["phase"] == "target":
                res = job_result(j, a)
                if res:
                    HOST.release_cursor(KEY)
                    finish_job(j, r, res, now)
                    return
                # Only the skill's own neutral cursor is targeted: a spell the player casts meanwhile is never aimed
                # at the bag item.
                if HOST.cursor_ok(KEY, "neutral"):
                    API.Target(j["serial"])
                    HOST.release_cursor(KEY)
                    j["phase"], j["t"] = "recover", now
                # A cursor nobody here claimed is up (the player's own): leave it alone and count the item as busy.
                elif HOST.cursor_busy(KEY) is None and API.HasTarget("any"):
                    HOST.release_cursor(KEY)
                    finish_job(j, r, "busy", now)
                elif now - j["t"] > TARGET_TIMEOUT:
                    HOST.release_cursor(KEY)
                    finish_job(j, r, "busy", now)
                return
            if now - j["t"] < max(r["delay"], MIN_DELAY):
                res = job_result(j, a)
                if res in ("busy", "skip", "fail"):
                    finish_job(j, r, res, now)
                return
            finish_job(j, r, job_result(j, a), now)

        def guard_check():
            """Ask whether a guard zone pauses the rules, and say once in the journal when that changes.

            HOST.guard_hold gives guard in a guard zone, unknown while the zone is not known yet (the strict
            reading pauses too) and None outside. Nothing is asked when no rule is at work.
            """
            active = not st["paused"] and (bool(st["run"]) or any(r["auto"] and r["bag"] for r in rules))
            hold = None
            # Unticking the guard option works only while the Training Alarm is on, because then you are
            # answering its at-keyboard alarms (shard rules: no macroing in towns). It covers an unknown zone too.
            if active and (settings["guard"] or "attention.up" not in HOST.services):
                hold = HOST.guard_hold()
            if hold != st["guard_paused"]:
                st["guard_paused"] = hold
                if active:
                    if hold == "guard":
                        msg = "%s: paused in a guard zone; it goes on when you leave." % TITLE
                    elif hold == "unknown":
                        msg = ("%s: paused until the guard zone is known; cross a town's guard line once." % TITLE)
                    else:
                        msg = "%s: out of the guard zone; going on." % TITLE
                    API.SysMsg(msg, Kit.HUE_INFO)

        # Seconds between the fight tests of the idle status.
        IDLE_LOOK = 1.5

        def run_jobs(now):
            """Per-tick driver: step the job, or when a scan is due check the guard, then start the next item.

            Sets the status text (Idle, Watching, or why blocked) and the time of the next scan.
            """
            if st["job"] is not None:
                job_step(now)
                return
            if not due(st["next_scan"], now):
                return
            guard_check()
            if not st["run"] and not any(r["auto"] and r["bag"] for r in rules):
                # With no rule able to run nothing will be used, so the status's fight test is looked at only every
                # IDLE_LOOK seconds; a rule that can run gets the full test every scan.
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

        def pick_bag(i):
            """The rule's Bag button: ask the player to target a bag for rule i (one pick at a time)."""
            if st["pick"] is not None:
                say("already targeting a bag.", Kit.HUE_INFO)
                return
            st["pick"] = i
            say("target the bag for rule %d." % (i + 1), Kit.HUE_INFO)

            def done(serial):
                """Target callback: queue the picked serial for the tick (0 means cancelled)."""
                queue.add(("picked", i, int(serial or 0)), dup=True)

            HOST.pick_target(20, done)

        def bag_picked(i, serial):
            """A bag was targeted for rule i: check it is a container in your backpack and give it to the rule.

            A different bag clears the rule's handled items, listings and results, as they were the old bag's.
            """
            st["pick"] = None
            if i >= len(rules):
                return
            if not serial:
                say("cancelled.", Kit.HUE_INFO)
                return
            it = get_item(serial)
            if it is None or not it.IsContainer:
                say("that isn't a container.", Kit.HUE_BAD)
                return
            if not Kit.in_pack(serial):
                say("that bag isn't in your backpack.", Kit.HUE_BAD)
                return
            r = rules[i]
            if r["bag"] != serial:
                r["bag"] = serial
                r["done"].clear()
                del r["order"][:]
                st["later"].clear()
                invalidate(r)
                # They belonged to the old bag.
                clear_results(r)
            save_settings()
            say("rule %d uses %s." % (i + 1, bag_name(r, False)), Kit.HUE_GOOD)
            st["redraw"] = True
            HOST.refresh_settings(KEY)

        def bags_min():
            """The smallest window size that shows every rule row."""
            return W, 2 * Kit.MARGIN + 30 + Kit.GAP + 40 + Kit.GAP + 30 + max(1, len(rules)) * ROW_H + 8

        def build_window():
            """Draw the Skill Bags window: a control strip (Pause, Add rule, status) and one row per rule.

            In a zone the window takes the zone's slot when it is big enough, else its own minimum size.
            Each row has the Auto box, bag, action, progress, the shard's last answer and the buttons
            Results, Bag, Run and Reset.
            """
            mw, mh = bags_min()
            w, h = wnd.zone_slot(mw, mh) or (mw, mh)
            g, store, c = wnd.begin(w, h)
            M = Kit.MARGIN
            rows = []
            if not st["minimized"]:
                IW = w - 2 * M
                wnd.frame(g)
                yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, 40)
                c["pause"] = Kit.art_button(g, store, "pause", Kit.ART_PLAY, M + 12, yb + 9,
                                            "Resume" if st["paused"] else "Pause", "Stop or restart every rule",
                                            on_click=queue("pause"))
                x_add = M + 12 + 35 + Kit.text_w("Resume") + 14
                Kit.art_button(g, store, "add", Kit.ART_OK, x_add, yb + 9, "Add rule",
                               "Add a rule (set it up on the settings page)", on_click=queue("add"))
                x_st = x_add + 35 + Kit.text_w("Add rule") + 14
                c["status"] = Kit.add_label(g, "", x_st, yb + 12, Kit.HUE_INFO)
                c["status_w"] = M + IW - 4 - x_st
                st["full_txt"] = None
                yr = yb + 40 + Kit.GAP
                Kit.add_section(g, M, yr, IW, h - yr - M, "RULES  (a bag and an action each)")
                y0 = yr + 30
                x_reset = M + IW - 12 - 35 - Kit.text_w("Reset")
                x_run = x_reset - 35 - Kit.text_w("Run") - 6
                # The three dots say a target cursor follows.
                x_bag = x_run - 35 - Kit.text_w("Bag...") - 6
                x_res = x_bag - 35 - Kit.text_w("Results") - 6
                c["last_w"] = IW - 36 - 16
                if not rules:
                    Kit.add_label(g, "No rules yet. Click Add rule, then set its bag and action.",
                                  M + 12, y0 + 5, Kit.HUE_INFO)
                for i, r in enumerate(rules):
                    ry = y0 + i * ROW_H
                    row = {}
                    row["auto"] = Kit.add_check(g, "", M + 10, ry + 2, r["auto"], "Handle every new item that lands "
                                                "in this bag")
                    row["bag"] = Kit.add_label(g, "", M + 36, ry + 3, Kit.HUE_TEXT)
                    row["act"] = Kit.add_label(g, "", M + 172, ry + 3, Kit.HUE_TITLE)
                    row["prog"] = Kit.add_label(g, "", M + 298, ry + 3, Kit.HUE_INFO)
                    row["last"] = Kit.with_tip(Kit.add_label(g, "", M + 36, ry + 22, Kit.HUE_INFO), "The shard's last "
                                               "answer to this rule and how it was read (ok, fail, skip or busy)")
                    for key, art, bx, cap, tip, act in (
                            ("res", Kit.ART_PAGE, x_res, "Results", "Show the shard's answer per item (again: close)",
                             "results"), ("bag", Kit.ART_PLAY, x_bag, "Bag...", "Target the bag this rule works on",
                             "bag"), ("run", Kit.ART_PLAY, x_run, "Run", "One pass over the items not done yet", "run"),
                            ("reset", Kit.ART_CLOSE, x_reset, "Reset", "Forget what was done, so every item is handled "
                             "again", "reset")):
                        Kit.art_button(g, store, "%s%d" % (key, i), art, bx, ry + 1, cap, tip, on_click=queue((act, i)))
                    row["text"] = (None, None, None, None)
                    rows.append(row)
            wnd.end(g, {"rows": rows})
            st["redraw"] = False
            refresh()

        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, mini=(MINI_W, MINI_H), icon=TRAY_ICON,
                         cleanup=cleanup, lock=True)
        # Text cut to a width by letter widths, with no label created per step.
        fit = Kit.fit

        def refresh():
            """Redraw the status line and the rule rows (only the rows whose text changed, every CHECK_EVERY).

            On the minimized bar the status carries the module title. The fitted text is cached per status.
            """
            if st["minimized"] and st["docked"]:
                return
            lbl = win["c"].get("status")
            if lbl is not None:
                hue = (Kit.HUE_BAD if st["paused"] else (Kit.HUE_GOOD if st["job"] else Kit.HUE_INFO))
                key = "mini_txt" if st["minimized"] else "full_txt"
                ft = st.get(key)
                if ft is None or ft[0] != st["status"]:
                    ft = st[key] = (st["status"], fit("%s: %s" % (TITLE, st["status"]), MINI_W - 90) if st["minimized"]
                                    else fit(st["status"], win["c"].get("status_w", 400)))
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
                prog = "closed" if r.get("_closed") else "%d/%d" % cnt if cnt else ""
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
                    Kit.set_text(row["last"], fit("Last: " + last if last else "Last: no answer read yet",
                                                  win["c"].get("last_w", 500)))

        def read_checks():
            """Read the Auto boxes of the window a few times a second and save a change."""
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

        # Results columns: time and item, then the result word, then the answer takes the rest.
        RES_NAME_W, RES_TAG_W = 230, 120

        def rule_index(r):
            """The rule's place in the list (by identity), or -1 once removed."""
            return next((k for k in range(len(rules)) if rules[k] is r), -1)

        def show_results(i):
            """A rule's Results button: open the window on that rule, switch an open one, or close it."""
            if i >= len(rules):
                return
            r = rules[i]
            if resw["rule"] is r and Kit.is_open(resw["g"]):
                res_close()
                return
            resw["rule"], resw["page"] = r, 0
            if Kit.is_open(resw["g"]):
                # Same window, another rule: the rows are rewritten.
                resw["dirty"] = True
            else:
                build_results()

        def res_min():
            """The smallest Results window size (a few rows)."""
            return RES_MIN_W, RES_FIXED + 4 * RES_ROW_H

        def res_close():
            """Close the Results window (or rebuild it empty when it lives in a zone)."""
            resw["rule"] = None
            if Kit.zone_up(RES_KEY):
                build_results()
            else:
                resultw.close()

        def res_redraw():
            """Rebuild or close the Results window after a zone or layout change."""
            if Kit.zone_up(RES_KEY) or resw["rule"] is not None and resw["g"] is not None:
                build_results()
            elif resw["g"] is not None:
                resultw.close()

        def build_results():
            """Draw the Results window: title, Close, Export, Clear, page buttons and the rows.

            In a zone the window takes the zone's slot and as many rows as fit; otherwise RES_ROWS rows.
            """
            M = Kit.MARGIN
            held = Kit.zone_up(RES_KEY)
            z = resultw.slot if held else None
            mw, mh = res_min()
            if z is not None and (z[0] < mw or z[1] < mh):
                z = None
            w = z[0] if z is not None else RES_W
            n = resultw.rows(RES_ROW_H, RES_FIXED, RES_ROWS) if z else RES_ROWS
            h = z[1] if z is not None else RES_FIXED + n * RES_ROW_H
            IW = w - 2 * M
            sh = h - M - 30 - Kit.GAP - M
            g, store, c = resultw.begin(w, h)
            Kit.add_window_frame(g, w, h)
            Kit.add_section(g, M, M, IW, 30)
            if not held:
                Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close the results",
                               on_click=queue("res_close"))
            x_exp = w - M - (10 if held else 66) - 35 - Kit.text_w("Export")
            Kit.art_button(g, store, "export", Kit.ART_OK, x_exp, M + 4, "Export",
                           "Write the results to a file in the VirtueAssistantSettings folder",
                           on_click=queue("res_export"))
            x_clr = x_exp - 12 - 35 - Kit.text_w("Clear")
            Kit.art_button(g, store, "clear", Kit.ART_CLOSE, x_clr, M + 4, "Clear",
                           "Forget these results (items stay done; Reset handles them again)",
                           on_click=queue("res_clear"))
            c["title"] = Kit.add_label(g, "", M + 30, M + 7, Kit.HUE_TITLE)
            c["title_w"] = x_clr - (M + 30) - 8
            ys = M + 30 + Kit.GAP
            Kit.add_section(g, M, ys, IW, sh, "RESULTS  (newest first)")
            x_old = M + IW - 12 - 35 - Kit.text_w("Next")
            Kit.art_button(g, store, "older", Kit.ART_PAGE, x_old, ys + 24, "Next", "Older results",
                           on_click=queue("res_older"))
            x_new = x_old - 10 - 35 - Kit.text_w("Prev")
            Kit.art_button(g, store, "newer", Kit.ART_PAGE, x_new, ys + 24, "Prev", "Newer results",
                           on_click=queue("res_newer"))
            # The page label is right-aligned to Prev, so it is moved when its text changes.
            c["page_x"], c["page_y"] = x_new - 8, ys + 28
            c["page"] = Kit.add_label(g, "", c["page_x"], ys + 28, Kit.HUE_INFO)
            c["counts"] = Kit.add_label(g, "", M + 12, ys + 28, Kit.HUE_TEXT)
            c["counts_w"] = x_new - (M + 12) - 16 - Kit.text_w("page 99 of 99")
            c["ans_w"] = IW - 12 - RES_NAME_W - RES_TAG_W - 8
            rows = []
            y0 = ys + 30 + 24
            for k in range(n):
                ry = y0 + k * RES_ROW_H
                rows.append({"name": Kit.add_label(g, "", M + 12, ry, Kit.HUE_TEXT),
                             "tag": Kit.add_label(g, "", M + 12 + RES_NAME_W, ry, Kit.HUE_INFO),
                             "ans": Kit.add_label(g, "", M + 12 + RES_NAME_W + RES_TAG_W, ry, Kit.HUE_INFO),
                             "tip": None})
            resultw.end(g, {"rows": rows})
            refresh_results()

        resultw = Kit.Window(RES_KEY, RES_TITLE, resw, resw, build_results, RES_POS_KEY, default=(260, 220),
                             cleanup=cleanup, lock=True, owner=False, clear={"rows": [], "rule": None, "c": {}})
        RES_HUE = {1: Kit.HUE_GOOD, 2: Kit.HUE_BAD, 3: Kit.HUE_INFO, 4: Kit.HUE_TEXT}

        def refresh_results():
            """Rewrite the Results rows (only when the results, the rule or the page changed).

            Newest first, one page of rows at a time; the whole answer is in each row's tooltip when it is
            cut. A removed rule closes the window.
            """
            resw["dirty"] = False
            r, rows, c = resw["rule"], resw["rows"], resw["c"]
            if not rows:
                return
            if r is None:
                Kit.set_text(c["title"], fit(RES_TITLE.upper(), c["title_w"]))
                Kit.set_text(c["counts"], fit(
                    RES_EMPTY, c["counts_w"]))
                return
            i = rule_index(r)
            if i < 0:
                res_close()
                return
            per = len(rows)
            res = r.get("_res") or []
            n = len(res)
            pages = max(1, (n + per - 1) // per)
            pg = resw["page"] = max(0, min(resw["page"], pages - 1))
            Kit.set_text(c["title"], fit("RULE %d RESULTS: %s" % (i + 1, rule_action(r)[1]), c["title_w"]))
            Kit.set_text(c["counts"], fit(counts_text(r), c["counts_w"]))
            ptxt = "page %d of %d" % (pg + 1, pages) if pages > 1 else ""
            if Kit.set_text(c["page"], ptxt) and ptxt:
                Kit.ui_pos(c["page"], c["page_x"] - Kit.text_w(ptxt), c["page_y"])
            top = n - 1 - pg * per
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
                    # The whole answer, when it is cut.
                    if row["tip"] != answer:
                        row["tip"] = answer
                        row["ans"].SetTooltip(answer or "")
                else:
                    for key in ("name", "tag", "ans"):
                        Kit.set_text(row[key], "")

        def export_results():
            """Prepare the shown rule's results as a text file (oldest first) for the thread to write.

            Never written on the client thread: a disk write there would be a hitch.
            """
            r = resw["rule"]
            i = rule_index(r) if r is not None else -1
            if i < 0:
                return
            res = r.get("_res") or []
            if not res:
                say("rule %d has no results to export yet." % (i + 1), Kit.HUE_INFO)
                return
            path = Kit.data_path(EXPORT_NAME % (int(API.Player.Serial), i + 1))
            lines = ["Skill Bags results - rule %d: %s on %s" % (i + 1, rule_action(r)[1], bag_name(r, False)),
                     "Exported %s - %s" % (time.strftime("%Y-%m-%d %H:%M"), counts_text(r)), "",
                     "%-19s  %-10s  %-32s  %-18s  %s" % ("Time", "Serial", "Item", "Result", "The shard's answer")]
            for t, s, name, code, tag, answer in res:
                lines.append("%-19s  0x%08X  %-32s  %-18s  %s" % (
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)), s, name, tag, answer))
            st["writes"].append((path, "\n".join(lines) + "\n"))

        def write_files():
            """Thread tick: write the exports prepared by export_results (returns at once when there are none)."""
            write_queue(st["writes"], TITLE, "results")

        def _thread_wanted():
            """Tell the host whether the script thread has an export to write."""
            return bool(st["writes"])

        def toggle_pause(action):
            """Pause or resume every rule; pausing drops a job in progress and gives the cursor back."""
            st["paused"] = not st["paused"]
            st["idle_at"] = 0.0
            if st["paused"] and st["job"] is not None:
                HOST.release_cursor(KEY)
                st["job"] = None
            lbl = win["c"].get("pause")
            if lbl is not None:
                Kit.set_text(lbl, "Resume" if st["paused"] else "Pause")
            say("%s." % ("paused" if st["paused"] else "resumed"), Kit.HUE_INFO)

        def add_rule(action):
            """Add a rule (up to MAX_RULES), save, redraw, and open the settings page to set it up."""
            if len(rules) >= MAX_RULES:
                say("at most %d rules." % MAX_RULES, Kit.HUE_INFO)
                return
            rules.append(new_rule())
            save_settings()
            build_window()
            HOST.refresh_settings(KEY)
            if page["f"] is None:
                HOST.show_settings(KEY)

        def remove_rule(action):
            """Remove rule action[1]: later rules move up a place, along with their jobs and Run passes.

            The per-rule timers are keyed by rule index, so they are all cleared.
            """
            i = action[1]
            if st["job"] is not None and st["job"]["rule"] == i:
                HOST.release_cursor(KEY)
                st["job"] = None
            elif st["job"] is not None and st["job"]["rule"] > i:
                st["job"]["rule"] -= 1
            # Its Results window goes with it.
            gone = rules.pop(i)
            if resw["rule"] is gone:
                res_close()
            elif resw["rule"] is not None:
                resw["dirty"] = True
            st["rr"] = 0
            st["run"] = set(k - 1 if k > i else k for k in st["run"] if k != i)
            # These are keyed by rule index, so they cannot survive a removal.
            st["budget"].clear()
            st["later"].clear()
            st["busy_n"].clear()
            st["no_tool"].clear()
            save_settings()
            build_window()
            HOST.refresh_settings(KEY)

        def run_rule(action):
            """The Run button: one pass over the rule's items not yet done (needs a bag)."""
            i = action[1]
            if not rules[i]["bag"]:
                say("set the bag for rule %d first (Bag button)." % (i + 1), Kit.HUE_BAD)
                return
            st["run"].add(i)
            st["budget"].pop(i, None)
            st["later"].clear()
            # A Run pass starts from a fresh listing.
            invalidate(rules[i])
            st["next_scan"] = 0.0

        def reset_rule(action):
            """The Reset button: forget what was done on this rule so every item is handled again."""
            i = action[1]
            rules[i]["done"].clear()
            del rules[i]["order"][:]
            rules[i].pop("_tries", None)
            rules[i].pop("_last", None)
            invalidate(rules[i])
            st["later"].clear()
            save_done()
            say("rule %d will handle every item again (%s)." % (i + 1, bag_name(rules[i])), Kit.HUE_INFO)

        def clear_shown(action):
            """The Results window's Clear button: forget the shown rule's results."""
            if resw["rule"] is not None:
                clear_results(resw["rule"])
                resw["page"] = 0

        def page_step(action):
            """The Results window's Prev and Next buttons: move one page."""
            resw["page"] += 1 if action == "res_older" else -1
            resw["dirty"] = True

        ACTIONS = {"pause": toggle_pause, "add": add_rule, "remove": remove_rule, "run": run_rule, "reset": reset_rule,
                "bag": lambda action: pick_bag(action[1]), "picked": lambda action: bag_picked(action[1], action[2]),
                "results": lambda action: show_results(action[1]), "res_close": lambda action: res_close(),
                "res_export": lambda action: export_results(), "res_clear": clear_shown, "res_older": page_step,
                "res_newer": page_step}
        # Seconds between saves of the handled items (and one more on stop).
        DONE_SAVE_EVERY = 5.0
        SEC_R = 118
        # Shown on the settings page under the options.
        HINT = ("The OK / FAIL / SKIP phrases that read the shard's answers are RunUO defaults, not checked on this "
                "shard; the window's Last line shows each rule's last answer.")
        TIP_TEXT = "Hex graphics with commas (0x14FC, 0x0E76), or part of a name (treasure map)"
        TIP_CUSTOM = "The skill's client name (Item Identification), or the tool's hex graphic (0x14FC: lockpicks)"
        TIP_DELAY = ("Seconds between items (%g-%g; a skill rule waits at least its 3 or 10 s timer)"
                     % (MIN_DELAY, MAX_DELAY))
        TIP_DEEP = "Also handle items in bags inside it"
        TIP_AUTO = "Handle every new item that lands in the bag (the window's box too)"

        def page_table(w, prow=None, dds=None):
            """Settings page layout: the options and one section per rule.

            `prow` collects the rule rows' controls and `dds` the drop-downs to place after the form is drawn.
            """
            def rule_sec(i, r):
                """One rule's section: a header and its own drawn controls."""
                def draw(f, x, y):
                    """Draw one rule's controls (action, custom, remove, items, text, delay, deep, auto).

                    Drop-downs are only recorded here; build_config creates them last.
                    """
                    g, yr, row = f.g, y - 30, {}
                    Kit.add_label(g, "Action:", x + 12, yr + 34)
                    dds.append(("action", i, x + 70, yr + 30, 210, ACTION_NAMES, r["action"]))
                    Kit.with_tip(Kit.add_label(g, "Custom:", x + 296, yr + 34), TIP_CUSTOM)
                    row["custom"] = Kit.with_tip(Kit.add_textbox(g, r["custom"], x + 356, yr + 30, 130, numbers=False),
                                                 TIP_CUSTOM)
                    Kit.art_button(g, f.store, "rm%d" % i, Kit.ART_CLOSE, x + f.w - 12 - 35 - Kit.text_w("Remove"),
                                   yr + 28, "Remove", "Remove this rule", on_click=queue(("remove", i)))
                    Kit.add_label(g, "Items:", x + 12, yr + 62)
                    dds.append(("filt", i, x + 70, yr + 58, 210, FILTER_NAMES, r["filt"]))
                    Kit.with_tip(Kit.add_label(g, "Text:", x + 296, yr + 62), TIP_TEXT)
                    row["text"] = Kit.with_tip(Kit.add_textbox(g, r["text"], x + 356, yr + 58, f.w - 356 - 16,
                                                               numbers=False), TIP_TEXT)
                    Kit.with_tip(Kit.add_label(g, "Delay (s):", x + 12, yr + 90), TIP_DELAY)
                    row["delay"] = Kit.with_tip(Kit.add_textbox(g, "%g" % r["delay"], x + 90, yr + 86, 50,
                                                                numbers=False), TIP_DELAY)
                    row["deep"] = Kit.add_check(g, "Look inside bags within the bag", x + 160, yr + 88, r["deep"],
                                                TIP_DEEP)
                    row["auto"] = Kit.add_check(g, "Auto (watch the bag)", x + 420, yr + 88, r["auto"], TIP_AUTO)
                    prow.append(row)

                return ("RULE %d  (%s)" % (i + 1, fit(bag_name(r, False), 300)), (("custom", 0, draw),), {"sh": SEC_R})

            return ([("OPTIONS", [("check", "hidden", "Pause while hidden", "Using a skill would reveal you"),
                        ("check", "open", "Open bags the client hasn't looked in",
                         "On Run, double-clicks the bag once so its contents are known", {"stay": True}),
                        ("buttons", (("add", Kit.ART_OK, "Add rule", "Add a rule (a bag and an action)",
                                      queue("add")),), {"dx": 400}), ("num", "retries", "Extra tries after a failure:",
                         "Retries after a FAIL phrase (0-9)", None, 0, 9,
                         {"lw": 268, "fw": 40, "ldy": 4, "ltip": True, "h": 2, "clamp": False}),
                        ("check", "guard", "Pause in guard zones", "No skill use in towns or an unknown zone; "
                         "unticked counts only while Skills > Training Alarm is on", {"dx": 380})] +
                     [("note", line, {"h": 18}) for line in Kit.wrap(HINT, w - 24) or [HINT]], {"pad": 6})] +
                    [rule_sec(i, r) for i, r in enumerate(rules)])

        cfg = Kit.Page(settings, page_table)

        def build_config(g, x, y, w):
            """Build the settings page and remember its controls for poll_config."""
            prow, dds = [], []
            f = Kit.Form(g, x, y, w, settings, page_table(w, prow, dds))
            # Drop-downs last, the lowest first, so an open list draws over what is below it.
            for kind, i, dx, dy, dw, items, idx in sorted(dds, key=lambda d: -d[3]):
                dd = G.CreateDropDown(dw, list(items), int(idx))
                dd.SetPos(dx, dy)
                g.Add(dd)
                prow[i][kind] = dd
            page.update({"f": f, "rows": prow, "next_read": 0.0})

        def poll_config():
            """Read the settings page a few times a second and apply what changed.

            Options, then each rule's action, filter, custom text, filter text, delay and the deep and auto
            boxes. A new action takes that action's defaults and forgets the old results. Only the rules
            whose listing changed are listed again, and the window rows follow in refresh. Any error closes
            the page's reading until it is reopened.
            """
            f = page["f"]
            if f is None:
                return
            now = time.time()
            if now < page["next_read"]:
                return
            page["next_read"] = now + CHECK_EVERY
            relist = []
            auto_moved = []
            try:
                new = f.read(True)
                changed = new != settings
                settings.update(new)
                for i, row in enumerate(page["rows"]):
                    if i >= len(rules):
                        break
                    r = rules[i]
                    # The action changed in this pass: its defaults replace the delay, whose box still shows the old.
                    act_new = False
                    for kind, names in (("action", RULE_ACTIONS), ("filt", FILTERS)):
                        idx = int(row[kind].GetSelectedIndex())
                        if 0 <= idx < len(names) and idx != r[kind]:
                            r[kind] = idx
                            changed = True
                            relist.append(r)
                            if kind == "action":
                                act_new = True
                                r["filt"] = RULE_ACTIONS[idx][5]
                                r["delay"] = RULE_ACTIONS[idx][4]
                                r["done"].clear()
                                del r["order"][:]
                                # They belonged to the old action.
                                clear_results(r)
                                page["dirty"] = True
                                break
                    for k in ("custom", "text"):
                        v = str(row[k].Text or "").strip()
                        if v != r[k]:
                            r[k] = v
                            changed = True
                            relist.append(r)
                    if not act_new:
                        d = clamp_delay(str(row["delay"].Text or "").strip(), r["delay"])
                        # Never under the skill's timer.
                        d = max(d, skill_floor(r))
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
                page["f"] = None
                say("settings page error: %s (reopen the page)." % ex, Kit.HUE_BAD)
                return
            if changed:
                save_settings()
                for r in relist:
                    invalidate(r)
                # An Auto change is shown on the window's box, since read_checks would otherwise undo it.
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
            """Settings page closed: forget its controls."""
            page["f"] = None
            page["rows"] = []

        load_settings()

        def _start():
            """Part hook: reset the run state and the Results window, load the saved rules and draw the window."""
            st.update({"shutting": False, "docked": False, "queue": [], "paused": False,
                       "job": None, "next_scan": 0.0, "next_check": 0.0, "status": "Idle",
                       "run": set(), "budget": {}, "opening": {}, "later": {}, "pick": None, "redraw": False,
                       "save_done": False, "no_tool": {}, "busy_n": {}, "next_rows": 0.0,
                       "rr": 0, "guard_paused": None, "writes": [], "idle_at": 0.0, "done_at": 0.0,
                       "minimized": wnd.start_min()})
            resw.update({"g": None, "rule": None, "c": {}, "rows": [], "page": 0, "dirty": False, "minimized": False,
                         "shutting": False, "docked": False, "queue": []})
            load_settings()
            build_window()
            # The layout may scale the window to its zone; bags_min is the smallest it may be.
            wnd.dock(fit=True, min=bags_min)
            resultw.dock(fit=True, min=res_min)

        def _tick():
            """Part hook, client tick: run queued actions, redraw, read the Auto boxes and run the jobs.

            Rebuilds the window when a rule list changed, saves the handled items at most every
            DONE_SAVE_EVERY seconds, and refreshes the status.
            """
            if win["g"] is None:
                return
            if Kit.closed(win):
                return
            now = time.time()
            while st["queue"]:
                action = st["queue"].pop(0)
                kind = action[0] if isinstance(action, tuple) else action
                # Window actions first; a button of a rule that has since been removed is dropped.
                if wnd.action(action) or (kind in ("remove", "bag", "run", "reset") and action[1] >= len(rules)):
                    continue
                fn = ACTIONS.get(kind)
                if fn is not None:
                    fn(action)
            if st.get("redraw"):
                build_window()
            # The Results window asked for a redraw (a zone change).
            if resw["queue"]:
                del resw["queue"][:]
                res_redraw()
            if resw["dirty"] and resw["g"] is not None:
                refresh_results()
            if not st["minimized"] and now >= st["next_check"]:
                st["next_check"] = now + CHECK_EVERY
                read_checks()
            run_jobs(now)
            # One write per DONE_SAVE_EVERY seconds.
            if st.get("save_done") and now >= st["done_at"]:
                st["save_done"] = False
                st["done_at"] = now + DONE_SAVE_EVERY
                save_done()
            refresh()

        def _interval():
            """Part hook: seconds until the next tick, fast only while a skill's target cursor is awaited.

            The recover wait, which can last seconds, reads the answer every 0.1 seconds.
            """
            j = st["job"]
            return 0.05 if j is not None and j["phase"] == "target" else 0.1

        def _stop():
            """Part hook: drop the job and its cursor, save, and write or drop a pending export."""
            st["shutting"] = resw["shutting"] = True
            if st["job"] is not None:
                HOST.release_cursor(KEY)
                st["job"] = None
            save_settings()
            cleanup.close()
            if st["writes"]:
                # An export asked for in the very last pass is written now, unless this is the client thread, where
                # a disk write would be a hitch.
                if Client.on_client_thread():
                    say("the export wasn't written (the module stopped); export again.", Kit.HUE_INFO)
                    del st["writes"][:]
                else:
                    write_files()

        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": build_config, "poll_config": poll_config, "config_closed": config_closed,
                "thread_tick": write_files, "thread_wanted": _thread_wanted, "interval": _interval}

    PARTS = (("window", _part_window, 0.25, "skills"), ("alarm", _part_alarm, 0.1, "attention"),
        ("bags", _part_bags, 0.1, "skillbags"),)
    return PartSet(KEY, TITLE, PARTS).hooks()


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("skills", "Skills", "Skills, training and AFK alarms", _module_skills, 0.1,
         category="Skills and home", parts=(("window", "Skills Window",
              "Skills with locks, groups and gains", True, ("skills",)),
             ("alarm", "Training Alarm", "Alarm when staff or a gump needs you", False,
              ("attention",)), ("bags", "Skill Bags", "A skill on each item in a bag, once", False, ("skillbags",)),),
         aliases=('Skill Bags', 'Attention', 'GM check', 'training', 'locks', 'gains', 'Item ID'))
