# =============================================================================
#  Meters  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by the Virtue Assistant script from
#  LegionScripts/VirtueAssistantModules. Virtue Assistant provides everything
#  this file uses (API, G, safe, Client, Kit, Follow, HOST, the main loop and
#  the settings window), so run that instead and tick Meters on its Modules
#  tab.
#
#  A damage / healing / everything meter in the spirit of WoW's Details!:
#  bar windows that rank what happened, per fight or for the whole session.
#
#   * Displays (pick one per window with the arrows, or the display button):
#       COMBAT    Damage done, Damage taken, All damage nearby, Biggest hits,
#                 Kills, Deaths
#       HEALING   Healing done, Healing received, Healing by method, Cures,
#                 Poisonings
#       MAGIC & ITEMS  Spells cast (with fizzles / interrupts), Mana spent,
#                 Consumables (bandages, potions, reagents, arrows / bolts),
#                 Buffs & debuffs
#       ECONOMY & PROGRESS  Gold (gained / spent, per hour), Items gained
#                 (loot, ore, logs, crafts), Skill gains (per hour: UO's
#                 "experience"), Stat gains, Fame & karma, Travel, and a
#                 Session summary
#   * Segments: "Current" is the fight going on (or the last one), "Overall"
#     is the whole session since you started or reset, and every finished
#     fight is kept in the segment list (how many: Settings). A fight starts
#     with the first damage you deal or take and ends after a few quiet
#     seconds (Settings).
#   * "New window" opens another meter window, each with its own display
#     and segment, so you can watch DPS, healing and gold per hour at once.
#     Every window minimizes, folds into the Action Bar and remembers where
#     it sits, its size and what it shows. Drag any corner of a free window
#     to resize it: the rows fill the height, the columns share the width.
#     In a zone of the screen layout a window is exactly the zone's size
#     (its share of it), whatever its own size. The X of an extra window closes just that
#     window; the X of the first one switches Meters off.
#   * Click a row for its details (hits, average, biggest, rate ...).
#     Alt+click a row that is a mobile to auto-follow it (again to stop).
#   * "Report" puts the display's top rows in party chat when you are in a
#     party (switch on the Settings page), otherwise in your journal.
#   * Gold by place (ECONOMY & PROGRESS): the gold you gain, by where you
#     were - the guarded town when Virtue Assistant knows its name, else a
#     spot you named on the Settings page ("Name this spot"), else
#     Elsewhere - ranked by gold per hour spent there.
#   * A graph of the last hour (one bar per minute) of a window's display,
#     under its rows: switch it on in that window's display list.
#   * Export (Settings, or a window's display list) writes every display of
#     the window's segment to Meters_<serial>.txt next to Virtue Assistant.
#   * Death recap: when you die, a window shows the last seconds of damage
#     you took (who, how much, and your hit points falling).
#
#  How things are counted (UO doesn't say who hit whom, so some is judged):
#   - Damage numbers are the client's own (the numbers over heads), read
#     from TazUO's damage event through a small .NET hook that only queues
#     them (it never runs Python, so it is harmless if the script stops).
#   - Your damage = damage on a mobile you attacked (war mode) or targeted
#     in the last few seconds (Settings), so your pets' damage on your
#     target counts as yours. Every number also goes to All damage nearby.
#   - Damage taken / healing / cures / deaths are watched for you, your
#     party, your pets and your TazUO friends list. Their hit points are only
#     sent to you as a percentage for pets and strangers, so their healing
#     shows as a "(%)" row.
#   - Healing done by you: a rise in hit points right after your bandage,
#     heal spell or heal potion. Rises smaller than the regen limit
#     (Settings) are ignored.
#   - Items gained / reagents used come from your backpack's contents (open
#     the backpack once after logging in so the client knows them).
#
#  To leave this module out, take this file out of the folder.
#  Module key: "meters"
# =============================================================================


def _module_meters():
    """Builds the module in its own namespace and returns its hooks."""
    # ============================ MODULE START ===================================
    #  MODULE: Meters  -  Details!-style meters for combat, healing and economy
    # =============================================================================
    KEY = "meters"
    TITLE = "Meters"

    # ------------------------------- CONFIG --------------------------------------
    SETTINGS_KEY = "Meters_settings"      # per character
    WINS_KEY = "Meters_windows"           # per character: the windows and what they show
    W = 360                               # meter window width (its own size)
    SIZE_MIN_W = 240                      # (2.6.64) narrowest a corner drag makes a free window
    SIZE_MAX_W = 1200                     # (2.6.64) widest
    RESIZE_SETTLE = 0.35                  # (2.6.64) seconds without a corner-drag step: let go
    ZONE_EVERY = 0.5                      # (2.6.64) seconds between looks at its zone slot
    MINI_W, MINI_H = 320, 46              # minimized bar (its text: "Meters: Damage done  Total ...")
    PICK_W = 360                          # display / segment pickers
    DETAIL_W = 300                        # row details window
    ROW_H = 20                            # one bar row
    VAL_W = 146                           # value column at the right of each row
    MAX_WINDOWS = 6
    TRAY_ICON = 0x0EEF                    # gold coins on the Action Bar's tray button
    ART_LEFT = (4014, 4016, 4015)         # left arrow (previous display)
    BAR_BG = "#17171a"
    UI_EVERY = 1.0                        # seconds between redraws of the numbers
    FRIENDS_EVERY = 3.0                   # seconds between looks for party / pets / friends
    SCAN_EVERY = 2.0                      # seconds between backpack looks
    WATCH_SECS = 30.0                     # a damaged mobile is watched this long (kills)
    KILL_CREDIT_SECS = 30.0               # your damage this recent gets you the kill
    PET_RANGE = 18                        # your pets are looked for this far away
    JUMP_TILES = 12                       # a move further than this is a recall / gate
    DEATH_BIT = 0x80000000                # TazUO marks a dying mobile's serial with this
    GOLD_GRAPHIC = 0x0EED
    HEAL_SPELL_SECS = 8.0                 # a heal spell's words, then the heal within ...
    BANDAGE_SECS = 2.0                    # bandage message <-> hit point rise
    POTION_SECS = 2.5
    CURE_SECS = 8.0
    ORPHAN_SECS = 1.5                     # a rise seen just before its message still counts
    MANA_SECS = 4.0                       # mana drop this soon after a spell's words = that spell
    BIG_KEEP = 25                         # biggest hits kept per segment
    REPORT_ROWS = 5
    HOOK_KEY = "VirtueMeters.DamageHook"  # AppDomain slot of the damage hook (cleanup)
    DAMAGE_QUEUE_MAX = 4000
    PARTY_MSG_MAX = 220                   # characters one party chat line may hold
    DYING_CHECK_SECS = WATCH_SECS / 2     # a watched mobile's death is looked for this long after its last hit
    WATCH_MAX = 40                        # mobiles watched for a kill at once
    FEED_BURST = 600                      # damage numbers taken from the hook's queue per tick
    MOBS_MAX = 800                        # names remembered (cleared past this)
    # Gold by place (2.6.05)
    SPOTS_KEY = "Meters_spots"            # per character: the spots you named
    SPOTS_MAX = 20                        # named spots kept
    SPOT_NAME_MAX = 24                    # characters of a spot's name
    SPOT_RADIUS = 20                      # tiles round a new spot (the default in the box)
    SPOT_RADIUS_LIMITS = (1, 300)
    PLACE_EVERY = 1.0                     # seconds between looks at where you are
    PLACE_ELSEWHERE = "Elsewhere"         # not in a known guarded town nor in a named spot
    PLACE_MIN_SECS = 60.0                 # a place's rate counts at least this much time there
    # the session graph (2.6.05)
    GRAPH_MINUTES = 60                    # one bar per minute, the last hour
    GRAPH_H = 40                          # bar height at the hour's peak (pixels)
    GRAPH_COL = 4                         # bar width; one pixel between bars
    GRAPH_BLOCK = 18 + GRAPH_H + 4        # caption, bars and the gap under them
    # Export (2.6.05): every display of a window's segment, to a text file
    EXPORT_FILE = "Meters_%08X.txt"       # next to Virtue Assistant (one per character)
    EXPORT_ROWS = 50                      # rows written per display (the top ones)
    # death recap (2.6.05)
    RECAP_SECS = 10.0                     # seconds of damage taken shown when you die
    RECAP_ROWS = 12                       # hits listed (the last ones)
    RECAP_COLS = 40                       # bars of the hit point line
    RECAP_W = 360
    RECAP_POS_KEY = "Meters_recap_pos"    # per character: where the recap window sits
    RECAP_HINT = ("Who: spell words heard just before the hit,",
                  "else whom you were fighting (shown with ?).")
    TAKEN_KEEP = 200                      # hits on you kept for the recap (newest)
    HP_KEEP = 300                         # hit point readings kept for the recap (newest)
    CASTS_KEEP = 20                       # others' harmful words of power kept
    CAST_CREDIT_SECS = 4.0                # a hit within this long after someone's harmful
    #                                       spell could land (its words + its cast delay) is
    #                                       credited to them (unchecked in game)
    CAST_EARLY = 0.5                      # ... or this much before its delay is over (faster
    #                                       casting; Kit.CAST_DELAY is unchecked in game too)
    HARM_SPELLS = ("Magic Arrow", "Harm", "Fireball", "Lightning", "Mind Blast",
                   "Energy Bolt", "Explosion", "Flamestrike", "Chain Lightning",
                   "Meteor Swarm", "Earthquake", "Poison", "Poison Field", "Fire Field",
                   "Holy Light", "Pain Spike", "Poison Strike", "Strangle", "Wither")

    # journal lines (lower case, matched as the start of the line)
    MSG_BANDAGE_BEGIN = "you begin applying the bandages"
    MSG_BANDAGE_HEALS = ("you finish applying the bandages", "you heal what little damage",
                         "you apply the bandages, but they barely help")
    MSG_BANDAGE_CURE = "you have cured the target of all poisons"
    MSG_FIZZLE = "the spell fizzles"
    MSG_INTERRUPT = "your concentration is disturbed"
    MSG_NO_MANA = "insufficient mana"
    RE_SKILL = re.compile(r"your skill in (.+?) has (increased|decreased) by ([0-9]+(?:\.[0-9]+)?)", re.I)
    RE_STAT = re.compile(r"your (strength|dexterity|intelligence) has (increased|decreased) by ([0-9]+)", re.I)
    RE_FAME = re.compile(r"you have (gained|lost) .*?\b(fame|karma)\b", re.I)

    # words of power -> (spell, kind); kind "heal" / "cure" / "cure+" (cures several).
    # Since 2.6.05 the table is the mother's shared copy (Kit.SPELL_WORDS, also
    # read by Unit Frames' cast bar), no longer one of Meters' own; a mother
    # without it gives an empty table (spells simply aren't counted).
    SPELLS = getattr(Kit, "SPELL_WORDS", None) or {}
    POTIONS = {0x0F0C: ("Heal", "heal"), 0x0F07: ("Cure", "cure"), 0x0F0B: ("Refresh", None),
               0x0F09: ("Strength", None), 0x0F08: ("Agility", None),
               0x0F0D: ("Explosion", None), 0x0F06: ("Night Sight", None),
               0x0F0A: ("Poison", None)}
    CONSUMABLES = {0x0F7A: "Black Pearl", 0x0F7B: "Blood Moss", 0x0F84: "Garlic",
                   0x0F85: "Ginseng", 0x0F86: "Mandrake Root", 0x0F88: "Nightshade",
                   0x0F8D: "Spiders' Silk", 0x0F8C: "Sulfurous Ash", 0x0F78: "Bat Wing",
                   0x0F8F: "Grave Dust", 0x0F7D: "Daemon Blood", 0x0F8E: "Nox Crystal",
                   0x0F8A: "Pig Iron", 0x0F3F: "Arrows", 0x1BFB: "Bolts"}

    # displays: id -> (title, rate unit, number format, bar colour, rows are mobiles)
    #   rate "s" = per second of combat, "m" = per minute, "h" = per hour, "" = none
    METRIC = {
        "dmg_done":   ("Damage done", "s", "n", "#c4562a", True),
        "dmg_taken":  ("Damage taken", "s", "n", "#b02a2a", True),
        "dmg_nearby": ("All damage nearby", "s", "n", "#9a5a3a", True),
        "big":        ("Biggest hits", "", "n", "#d07a2a", True),
        "kills":      ("Kills", "h", "n", "#8a6ab0", False),
        "deaths":     ("Deaths", "h", "n", "#6a6a78", True),
        "heal_done":  ("Healing done", "s", "n", "#2f9a3c", True),
        "heal_taken": ("Healing received", "s", "n", "#3fae5a", True),
        "heal_by":    ("Healing by method", "s", "n", "#4aa070", False),
        "cures":      ("Cures", "m", "n", "#2a9a8a", True),
        "poisoned":   ("Poisonings", "m", "n", "#5a9a2a", True),
        "spells":     ("Spells cast", "m", "n", "#2f62cc", False),
        "mana":       ("Mana spent", "m", "n", "#3a72d8", False),
        "consum":     ("Consumables", "h", "n", "#a08a2a", False),
        "buffs":      ("Buffs & debuffs", "h", "n", "#8a5ab0", False),
        "gold":       ("Gold", "h", "n", "#cfae2a", False),
        "gold_place": ("Gold by place", "h", "n", "#d8b84a", False),
        "loot":       ("Items gained", "h", "n", "#a8925a", False),
        "skills":     ("Skill gains", "h", "d1", "#5a8acc", False),
        "stats":      ("Stat gains", "h", "n", "#cc7a5a", False),
        "fame":       ("Fame & karma", "h", "n", "#b0a050", False),
        "travel":     ("Travel", "h", "n", "#6a9aaa", False),
        "session":    ("Session summary", "", "", "#4a4a58", False),
    }
    GROUPS = (("COMBAT", ("dmg_done", "dmg_taken", "dmg_nearby", "big", "kills", "deaths")),
              ("HEALING", ("heal_done", "heal_taken", "heal_by", "cures", "poisoned")),
              ("MAGIC & ITEMS", ("spells", "mana", "consum", "buffs")),
              ("ECONOMY & PROGRESS", ("gold", "gold_place", "loot", "skills", "stats", "fame",
                                      "travel", "session")))
    ORDER = [m for _, ms in GROUPS for m in ms]
    DEFAULT_METRIC = "dmg_done"
    RATE_WORD = {"s": "per sec", "m": "per min", "h": "per hour"}
    RATE_SHORT = {"s": "/s", "m": "/m", "h": "/h"}

    DEFAULTS = {"idle": 6, "engage": 12, "history": 10, "min_heal": 3, "rows": 8,
                "rank": True, "pct": True, "scan": True, "travel": True, "party": True,
                "recap": True}
    LIMITS = {"idle": (2, 60), "engage": (3, 120), "history": (1, 30), "min_heal": (1, 50),
              "rows": (3, 20)}
    # -----------------------------------------------------------------------------

    MAX_ROWS = 5000                       # rows one display keeps in one segment; past that
    FOLD_TO = 4000                        # the smallest are added into one OTHERS row (a
    #                                       safety cap for endless sessions: normal play never
    #                                       gets near it, so nothing is ever folded there)
    OTHERS = "(others)"
    HARM_SET = frozenset(HARM_SPELLS)
    OWN_PREFIX = TITLE.lower() + ":"      # this module's own journal lines

    settings = dict(DEFAULTS)
    st = {"shutting": False, "active": False, "queue": [], "last_tick": 0.0, "next_ui": 0.0,
          "next_friends": 0.0, "next_scan": 0.0, "hooked": False, "jr": None,
          "used": [], "buffq": [], "amtq": [],
          "engaged": {}, "watch": {}, "friendly": {}, "mobs": {}, "dead_seen": {},
          "prev": {}, "pack": None, "pack_sig": None, "pend": [], "orph": [], "last_spell": None,
          "cast_t": 0.0, "prev_lt": 0, "me": None, "pos": None,
          # 2.6.05: where you are (Gold by place), the death recap's memory,
          # exports waiting for the script's thread
          "place": None, "next_place": 0.0, "taken": [], "hp_log": [], "casts": [],
          "recap": None, "recap_show": False, "to_write": [],
          "redraw_wait": set(),       # (2.6.74) window ids whose redraw waits for a drag's end
          # 2.6.82: the friends the client had at the last friends look (polled every
          # tick), a backpack look spread over ticks, your name (read every NAME_EVERY)
          "present": [], "pscan": None, "pack_cand": None, "my_ser": None, "my_name": "", "next_name": 0.0,
          "fnames": None}
    spots = []                                 # named spots: [name, x, y, facet, radius]
    # minute -> {display: amount}; "ver" changes on a reset, "vb" per display (2.6.82)
    graph = {"min": None, "b": None, "hist": {}, "ver": 0, "vb": {}}
    recap = {"g": None, "store": ({}, {}), "rows": []}       # the death recap window
    data = {}
    wins = []                                  # meter windows (dicts), [0] is the main one
    page = {"c": None, "store": ({}, {})}
    feed = {"q": None, "handler": None, "event": None, "kind": "not hooked"}
    refl = {"tried": False, "tm": None, "la": None}
    jobs = []                                  # one-shot work for the script's thread (_thread_tick)
    SEGN = [0]                                 # segments made so far (each gets its own number)
    import heapq
    RE_COUNT = re.compile(r"^[0-9,]+\s+")      # (2.6.82) a stack's count before its name
    PACK_CHUNK = 60                            # (2.6.82) backpack items read per tick
    NAME_EVERY = 1.0                           # (2.6.82) seconds between reads of your name

    # 2.6.82 (speed pass): the mother's per-pass shared reads (one read of the
    # player / a mobile / the mobiles / the backpack per pass for every module),
    # or the plain API calls with a mother that hasn't them
    _SH_ME = getattr(HOST, "me", None)
    _SH_MOB = getattr(HOST, "mobile", None)
    _SH_MOBS = getattr(HOST, "mobiles", None)
    _SH_PACK = getattr(HOST, "pack_items", None)

    def player():
        return _SH_ME() if _SH_ME is not None else API.Player

    def find_mob(ser):
        return _SH_MOB(ser) if _SH_MOB is not None else API.FindMobile(ser)

    def mobiles_near(d):
        if _SH_MOBS is not None:
            return _SH_MOBS(d)
        return API.GetAllMobiles(distance=d) or []

    def pack_list(bp):
        if _SH_PACK is not None:
            return list(_SH_PACK(True))
        return list(API.ItemsInContainer(bp, True) or [])

    def pets_near():
        """Serials of your pets within PET_RANGE: Character HUD's shared list
        (HOST.services["pets.list"](distance=...)) when it is on and answers,
        else a look at the mobiles here."""
        svc = None
        try:
            svc = HOST.services.get("pets.list")
        except Exception:
            svc = None
        if svc is not None:
            try:
                got = svc(distance=PET_RANGE)
                if got is not None:
                    return [int(s) for s in got]
            except Exception:
                pass
        pets = []
        try:
            mobs = mobiles_near(PET_RANGE)
        except Exception:
            mobs = []
        for m in mobs:
            try:                                  # (no lambda per mobile)
                if m.IsRenamable:
                    pets.append(int(m.Serial))
            except Exception:
                pass
        return pets


    # ---------- small helpers ----------
    def fmt_num(v, f="n"):
        if f == "d1":
            return "%.1f" % v
        a = abs(v)
        if a >= 1e6:
            return "%.2fM" % (v / 1e6)
        if a >= 1e4:
            return "%.1fk" % (v / 1e3)
        if a >= 1000:
            return "%.2fk" % (v / 1e3)
        if abs(v - round(v)) < 0.05:
            return "%d" % int(round(v))
        return "%.1f" % v

    def fmt_rate(v, f="n"):
        if f == "d1":
            return "%.1f" % v if abs(v) < 100 else "%d" % int(round(v))
        if abs(v) < 10:
            return "%.1f" % v
        if abs(v) < 1000:
            return "%d" % int(round(v))
        return fmt_num(v)

    def fmt_signed(v, f="n"):
        s = fmt_num(v, f)
        return s if v < 0 else "+" + s

    def fmt_time(sec):
        sec = int(max(0, sec))
        h, m, s = sec // 3600, (sec // 60) % 60, sec % 60
        return "%d:%02d:%02d" % (h, m, s) if h else "%d:%02d" % (m, s)

    # ---------- text widths ----------
    #  The value texts change every second in a fight ("1.2k (45/s, 23%)", the
    #  combat clock, rates). Since 2.6.01 the mother measures a text as the sum
    #  of its letters' widths (Kit.text_px, no label made for known letters)
    #  and cuts it to fit with Kit.fit, so this module's own copy of that
    #  (text_px, trunc and its cache) is gone.
    def trunc(text, width):
        """text cut (with ..) to fit width pixels."""
        return Kit.fit(text, width)

    def is_mobile(ser):
        return 0 < int(ser or 0) < 0x40000000

    def pct_row(name):
        return name.endswith(" (%)")


    # ---------- saved settings and windows ----------
    def load_settings():
        for part in Kit.get_var(SETTINGS_KEY).split("|"):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            if k in LIMITS:
                try:
                    lo, hi = LIMITS[k]
                    settings[k] = max(lo, min(hi, int(v)))
                except ValueError:
                    pass
            elif k in DEFAULTS:
                settings[k] = v == "1"

    def save_settings():
        parts = []
        for k in sorted(DEFAULTS):
            v = settings[k]
            parts.append("%s=%s" % (k, ("1" if v else "0") if isinstance(v, bool) else int(v)))
        Kit.put_var(SETTINGS_KEY, "|".join(parts))

    def new_win(wid, metric=DEFAULT_METRIC, x=200, y=200, minimized=False):
        return {"id": wid, "metric": metric if metric in METRIC else DEFAULT_METRIC,
                "seg": "current", "x": x, "y": y, "minimized": minimized, "docked": False,
                "shutting": False, "g": None, "c": {}, "store": ({}, {}), "slots": [],
                "picker": None, "segpick": None, "detail": None, "dc": {}, "detail_row": None,
                "detail_metric": None, "graph": False, "gcols": [], "gkey": None,
                "fit": None,     # (2.6.57) its slot in a zone (w, h), or None: its own size
                "size": None,    # (2.6.64) the size a corner drag gave it (w, h), or None
                "drawn": None,   # (2.6.64) the size it was last drawn at (w, h)
                "resize_at": 0.0, "preview": False}   # (2.6.64) a corner drag going on

    def load_windows():
        out = []
        for part in Kit.get_var(WINS_KEY).split(";"):
            p = part.split(",")
            if len(p) < 6:
                continue
            try:
                wid, x, y = int(p[0]), int(p[3]), int(p[4])
            except ValueError:
                continue
            if any(w["id"] == wid for w in out):
                continue
            x, y = Kit.adapt(x, y, W, 0)              # a saved place: on the screen of today
            w = new_win(wid, p[1], x, y, p[5] == "1")
            w["seg"] = "overall" if p[2] == "overall" else "current"
            w["graph"] = len(p) > 6 and p[6] == "1"   # 2.6.05 field (2.6.04 reads 6)
            if len(p) > 8:                            # 2.6.64 fields: its own size (0: none)
                try:
                    sw, sh = int(p[7]), int(p[8])
                    if sw > 0 and sh > 0:
                        w["size"] = (max(SIZE_MIN_W, min(SIZE_MAX_W, sw)), max(60, sh))
                except ValueError:
                    pass
            out.append(w)
        out.sort(key=lambda w: w["id"])
        if not out or out[0]["id"] != 0:
            out.insert(0, new_win(0))
        del wins[:]
        wins.extend(out[:MAX_WINDOWS])

    def forget_sizes_off():
        """(2.6.81) Meters is off: forget every corner-drag size in the saved
        windows. wins is empty until Meters has been on this session, so load
        them first (dicts only, no gumps) or the save would erase every window;
        save_windows takes x/y from open gumps only, so the places stay as saved."""
        if not wins:
            load_windows()
        for w in wins:
            w["size"] = None
        save_windows()

    def save_windows():
        parts = []
        for w in wins:
            g = w["g"]
            if Kit.is_open(g):
                w["x"], w["y"] = safe(lambda: g.GetX(), w["x"]), safe(lambda: g.GetY(), w["y"])
            # the 7th field (graph on) is new in 2.6.05: 2.6.04 reads the first 6
            # of each window and ignores the rest, so it loads these as before
            # the 8th and 9th (its size from a corner drag, 0,0: its own) are new in
            # 2.6.64: older versions read the first 7 and ignore the rest
            size = w.get("size") or (0, 0)
            parts.append("%d,%s,%s,%d,%d,%s,%s,%d,%d" % (w["id"], w["metric"],
                                                         "overall" if w["seg"] == "overall"
                                                         else "current",
                                                         int(w["x"]), int(w["y"]),
                                                         "1" if w["minimized"] else "0",
                                                         "1" if w.get("graph") else "0",
                                                         int(size[0]), int(size[1])))
        Kit.put_var(WINS_KEY, ";".join(parts))

    def load_spots():
        """The named spots: "name,x,y,facet,radius;..." (a key 2.6.04 never reads)."""
        del spots[:]
        for part in Kit.get_var(SPOTS_KEY).split(";"):
            p = part.split(",")
            if len(p) < 5 or not p[0].strip():
                continue
            try:
                sp = [p[0].strip(), int(p[1]), int(p[2]), int(p[3]), int(p[4])]
            except ValueError:
                continue
            lo, hi = SPOT_RADIUS_LIMITS
            sp[4] = max(lo, min(hi, sp[4]))
            if all(o[0] != sp[0] for o in spots) and len(spots) < SPOTS_MAX:
                spots.append(sp)

    def save_spots():
        Kit.put_var(SPOTS_KEY, ";".join("%s,%d,%d,%d,%d" % tuple(sp) for sp in spots))

    def spot_name(text):
        """A spot's name as typed, made safe for the saved string."""
        for ch in ";,|":
            text = text.replace(ch, " ")
        return " ".join(text.split())[:SPOT_NAME_MAX]


    # ---------- the numbers ----------
    def new_seg(kind, n=0):
        now = time.time()
        SEGN[0] += 1
        return {"kind": kind, "n": n, "name": "Fight %d" % n if n else "Overall",
                "start": now, "end": None, "combat": 0.0, "d": {}, "serial": {}, "big": [],
                "fights": 0, "uid": SEGN[0], "ver": 0,
                "tot": {},                    # (2.6.82) each display's total, kept as recorded
                "place_t": {}}                # Gold by place: seconds spent in each place

    def reset_data():
        data.clear()
        data.update({"overall": new_seg("overall"), "cur": None, "hist": [], "n": 0,
                     "last_combat": 0.0, "c_at": None})
        st["watch"].clear()
        st["engaged"].clear()
        st["pend"], st["orph"] = [], []
        graph.update({"min": None, "b": None, "ver": graph["ver"] + 1})
        graph["hist"].clear()                     # the graph is the session's too
        graph["vb"].clear()

    def segs():
        cur = data["cur"]
        return (data["overall"], cur) if cur is not None else (data["overall"],)

    def graph_bucket(now):
        """This minute's amounts per display (for the session graph); a new
        minute starts a new bucket and drops those older than the hour."""
        m = int(now // 60)
        if m != graph["min"]:
            hist = graph["hist"]
            for k in [k for k in hist if k <= m - GRAPH_MINUTES]:
                del hist[k]
            graph["min"] = m
            b = graph["b"] = hist.get(m)
            if b is None:
                b = graph["b"] = hist[m] = {}
        return graph["b"]

    def record(mid, row, amt, ser=None):
        now = time.time()
        pct = row.endswith(" (%)")
        # the session graph: this minute's amount of the display (as its total
        # counts it: "(%)" rows aren't in it; Gold counts what was gained)
        if not pct and (mid != "gold" or row == "Gained"):
            b = graph_bucket(now)
            b[mid] = b.get(mid, 0.0) + amt
            vb = graph["vb"]
            vb[mid] = vb.get(mid, 0) + 1          # (2.6.82) per display: only its graph redraws
        for seg in segs():
            d = seg["d"].get(mid)
            if d is None:
                d = seg["d"][mid] = {}
            r = d.get(row)
            if r is None:                     # total, count, biggest, smallest, first, last
                if len(d) >= MAX_ROWS:
                    fold(seg, mid, d)
                r = d[row] = [0.0, 0, amt, amt, now, now]
            r[0] += amt
            r[1] += 1
            if amt > r[2]:
                r[2] = amt
            if amt < r[3]:
                r[3] = amt
            r[5] = now
            if ser:
                seg["serial"][(mid, row)] = ser
            if not pct:                       # (2.6.82) the total as total() summed it
                tot = seg["tot"]
                tot[mid] = tot.get(mid, 0.0) + amt
            seg["ver"] += 1

    def fold(seg, mid, d):
        """A display reached MAX_ROWS rows in one segment (in a long session
        All damage nearby gets a row for every passer-by hit near you, and the
        segment kept them all, and sorted them all every second): its smallest
        rows are added into one OTHERS row, so every total and share stays
        right and the rows stay few. Rows "(%)" never fold (they aren't in
        the total)."""
        small = sorted((abs(r[0]), k) for k, r in d.items()
                       if k != OTHERS and not k.endswith(" (%)"))
        o = d.get(OTHERS)
        sers = seg["serial"]
        for _, k in small[:max(0, len(d) - FOLD_TO)]:
            r = d.pop(k)
            sers.pop((mid, k), None)
            if o is None:
                o = d[OTHERS] = list(r)
            else:
                o[0] += r[0]
                o[1] += r[1]
                o[2], o[3] = max(o[2], r[2]), min(o[3], r[3])
                o[4], o[5] = min(o[4], r[4]), max(o[5], r[5])

    def record_big(amt, name, ser):
        b = graph_bucket(time.time())             # the graph: the minute's biggest hit
        if amt > b.get("big", 0.0):
            b["big"] = amt
            vb = graph["vb"]
            vb["big"] = vb.get("big", 0) + 1
        for seg in segs():
            big = seg["big"]
            if len(big) >= BIG_KEEP and amt <= big[-1][0]:
                continue
            # (2.6.82) put in its place (after the equal ones, as the stable sort
            # by size did) instead of a sort of the list with a lambda per hit
            i = len(big)
            while i > 0 and big[i - 1][0] < amt:
                i -= 1
            big.insert(i, (amt, name, ser))
            del big[BIG_KEEP:]

    def total(seg, mid):
        """The display's total ("(%)" rows aren't in it). 2.6.82: kept by record()
        as each amount comes (fold() moves rows into OTHERS, the sum stays), so
        no pass over thousands of rows per window per second."""
        if not seg or not seg["d"].get(mid):
            return 0
        return seg["tot"].get(mid, 0)

    def enter_combat():
        now = time.time()
        if data["cur"] is None:
            data["n"] += 1
            data["cur"] = new_seg("fight", data["n"])
            data["overall"]["fights"] += 1
        data["last_combat"] = now
        # (2.6.84) the combat times at the last hit: a fight's idle tail is cut
        # back to them on close (a sleep / clock jump mid-fight can't wipe Overall)
        data["c_at"] = (data["cur"]["combat"], data["overall"]["combat"])

    def close_fight(now):
        cur = data["cur"]
        if cur is None:
            return
        ca = data.get("c_at")
        if ca is not None:
            cur["combat"], data["overall"]["combat"] = ca
        else:
            tail = max(0.0, now - data["last_combat"])
            for seg in (cur, data["overall"]):
                seg["combat"] = max(0.0, seg["combat"] - tail)
        data["c_at"] = None
        cur["end"] = data["last_combat"]
        d = cur["d"].get("dmg_done", {})
        if d:
            top = max(d.items(), key=lambda kv: kv[1][0])[0]
            cur["name"] = top + (" +%d" % (len(d) - 1) if len(d) > 1 else "")
        data["hist"].insert(0, cur)
        del data["hist"][settings["history"]:]
        data["cur"] = None

    def combat_secs(seg):
        return max(1.0, seg["combat"])

    def wall_secs(seg):
        return max(1.0, (seg["end"] or time.time()) - seg["start"])   # "end": finished fights only

    def rate_of(seg, rate, value):
        if rate == "s":
            return value / combat_secs(seg)
        if rate == "m":
            return value / (wall_secs(seg) / 60.0)
        if rate == "h":
            return value / (max(60.0, wall_secs(seg)) / 3600.0)
        return 0.0

    def seg_for(w):
        s = w["seg"]
        if s == "overall":
            return data["overall"]
        if s != "current":
            for h in data["hist"]:
                if h["n"] == s:
                    return h
            w["seg"] = "current"
        return data["cur"] or (data["hist"][0] if data["hist"] else None)

    SEG_CAPS = {"overall": "Overall", "current": "Current"}

    def seg_caption(w):
        s = w["seg"]
        return SEG_CAPS.get(s) or "Fight %d" % s

    def seg_duration_text(seg):
        if seg is None:
            return ""
        if seg["kind"] == "overall":
            return fmt_time(time.time() - seg["start"])
        return fmt_time(combat_secs(seg))


    # ---------- what a window shows ----------
    def _row_size(kv):
        return abs(kv[1][0])

    def view(mid, seg, limit=None):
        """(header parts, rows); a row is (name, bar value, value text, serial, raw record).
        limit: only the top rows are worked out (a window shows `rows` of them,
        Report 5); every row used to be formatted every second for nothing."""
        _, rate, f, _, _ = METRIC[mid]
        if seg is None:
            return (["No fight yet. Attack something and the meters start."], [])   # (2.6.72)
        dur = seg_duration_text(seg)
        if mid == "session":
            return session_view(seg)
        if mid == "big":
            big = seg["big"] if limit is None else seg["big"][:limit]
            rows = [(name, amt, fmt_num(amt), ser, None) for amt, name, ser in big]
            head = (["Biggest %s on %s" % (fmt_num(seg["big"][0][0]), seg["big"][0][1])]
                    if seg["big"] else ["No hits yet. Hits land here as they happen."])
            return (head + [dur], rows)
        d = seg["d"].get(mid, {})
        if mid == "gold":
            gain = d.get("Gained", [0.0])[0]
            spent = d.get("Spent / banked", [0.0])[0]
            net = gain - spent
            rows = [("Gained", gain, "%s (%s/h)" % (fmt_num(gain), fmt_rate(rate_of(seg, "h", gain))),
                     None, d.get("Gained")),
                    ("Spent / banked", spent, fmt_num(spent), None, d.get("Spent / banked")),
                    ("Net", abs(net), "%s (%s/h)" % (fmt_signed(net), fmt_rate(rate_of(seg, "h", net))),
                     None, None)]
            return (["Net %s" % fmt_signed(net), "%s per hour" % fmt_rate(rate_of(seg, "h", net)),
                     dur], rows)
        if mid == "gold_place":
            return place_view(seg, d, limit, dur)
        tot = total(seg, mid)
        if limit is None:
            items = sorted(d.items(), key=_row_size, reverse=True)
        elif limit <= 0:
            items = []
        else:                                 # only the top rows: O(n), not a sort of them all
            items = heapq.nlargest(limit, d.items(), key=_row_size)
        rows = []
        for name, r in items:
            v = r[0]
            bits = []
            if rate:
                bits.append(fmt_rate(rate_of(seg, rate, v), f) + ("" if rate == "s" else RATE_SHORT[rate]))
            if settings["pct"] and tot and not pct_row(name) and v > 0:
                bits.append("%d%%" % int(round(100.0 * v / tot)))
            vt = (fmt_signed(v, f) if mid in ("skills", "stats") else fmt_num(v, f))
            text = vt + (" (%s)" % ", ".join(bits) if bits else "")
            rows.append((name, abs(v), text, seg["serial"].get((mid, name)), r))
        if mid in ("skills", "stats"):
            head = ["Total %s" % fmt_signed(tot, f)]
        elif mid == "cures":
            mine = total(seg, "cures_mine")
            head = ["Cures %s" % fmt_num(tot), "by you %s" % fmt_num(mine)]
        else:
            head = ["Total %s" % fmt_num(tot, f)]
        if rate:
            head.append("%s %s" % (fmt_rate(rate_of(seg, rate, tot), f), RATE_WORD[rate]))
        head.append("in combat " + fmt_time(seg["combat"]) if rate == "s" else dur)
        return (head, rows)

    def place_rate(seg, name, gold):
        """Gold per hour spent in place `name` in this segment (at least
        PLACE_MIN_SECS counted, so a minute's lucky pick-up isn't millions)."""
        secs = seg["place_t"].get(name, 0.0)
        return gold / (max(PLACE_MIN_SECS, secs) / 3600.0), secs

    def _rate_size(row):
        return row[1]

    def place_view(seg, d, limit, dur):
        """Gold by place: every place you gained gold in, or spent at least
        PLACE_MIN_SECS in, ranked by gold per hour spent there."""
        pt = seg["place_t"]
        names = list(d)
        for k, secs in pt.items():
            if secs >= PLACE_MIN_SECS and k not in d:
                names.append(k)
        tot = sum(r[0] for r in d.values())
        rows = []
        for name in names:
            r = d.get(name)
            gold = r[0] if r is not None else 0.0
            rate, _secs = place_rate(seg, name, gold)
            bits = [fmt_num(gold)]
            if settings["pct"] and tot and gold > 0:
                bits.append("%d%%" % int(round(100.0 * gold / tot)))
            rows.append((name, rate, "%s/h (%s)" % (fmt_rate(rate), ", ".join(bits)), None, r))
        rows.sort(key=_rate_size, reverse=True)
        if limit is not None:
            del rows[max(0, limit):]
        n = len(names)
        return (["Gained %s" % fmt_num(tot), "%d place%s" % (n, "" if n == 1 else "s"), dur],
                rows)

    def session_view(seg):
        wall = wall_secs(seg)
        cs = seg["combat"]
        dd, dt, hd = total(seg, "dmg_done"), total(seg, "dmg_taken"), total(seg, "heal_done")
        kills, deaths = total(seg, "kills"), total(seg, "deaths")
        gd = seg["d"].get("gold", {})
        net = gd.get("Gained", [0.0])[0] - gd.get("Spent / banked", [0.0])[0]
        sk = total(seg, "skills")
        lines = [("Time", fmt_time(wall)),
                 ("In combat", "%s (%d%%)" % (fmt_time(cs), int(100 * cs / wall)))]
        if seg["kind"] == "overall":
            lines.append(("Fights", "%d" % seg["fights"]))
        lines += [("Damage done", "%s (%s/s)" % (fmt_num(dd), fmt_rate(rate_of(seg, "s", dd)))),
                  ("Damage taken", "%s (%s/s)" % (fmt_num(dt), fmt_rate(rate_of(seg, "s", dt)))),
                  ("Healing done", "%s (%s/s)" % (fmt_num(hd), fmt_rate(rate_of(seg, "s", hd)))),
                  ("Kills", "%s (%s/h)" % (fmt_num(kills), fmt_rate(rate_of(seg, "h", kills)))),
                  ("Deaths", fmt_num(deaths)),
                  ("Gold", "%s (%s/h)" % (fmt_signed(net), fmt_rate(rate_of(seg, "h", net)))),
                  ("Skill gain", "%s (%s/h)" % (fmt_signed(sk, "d1"),
                                                fmt_rate(rate_of(seg, "h", sk), "d1"))),
                  ("Items gained", fmt_num(total(seg, "loot"))),
                  ("Spells cast", fmt_num(sum(r[1] for k, r in seg["d"].get("spells", {}).items()
                                              if k not in ("Fizzled", "Interrupted", "Out of mana"))))]
        rows = [(name, 0.0, text, None, None) for name, text in lines]
        return ([seg["name"] if seg["kind"] == "fight" else "Session", fmt_time(wall)], rows)


    # ---------- the damage feed: a .NET hook on TazUO's damage event ----------
    def hook_damage():
        """TazUO raises EventSink.OnEntityDamage(entity, amount) for every damage
        number, but the script event hands Python only the amount. A tiny .NET
        handler (System.Linq.Expressions) puts (serial, amount) in a queue; it
        never runs Python, so a copy left behind by a stopped run can't throw
        inside the client's packet handling. Falls back to amounts only."""
        try:
            import clr
            from System import Array, Int32, UInt32, Object, EventHandler, Tuple, Type, AppDomain
            from System.Reflection import BindingFlags
            from System.Collections.Concurrent import ConcurrentQueue
            from System.Linq.Expressions import Expression, ParameterExpression
            stat = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static
            asm = API.GetType().Assembly
            sink = asm.GetType("ClassicUO.Game.Managers.EventSink")
            ent = asm.GetType("ClassicUO.Game.GameObjects.Entity")
            if sink is None or ent is None:
                raise LookupError("TazUO's EventSink / Entity not found")
            ev = sink.GetEvent("OnEntityDamage", stat)
            if ev is None:
                raise LookupError("no OnEntityDamage event")
            t_obj, t_int, t_uint = clr.GetClrType(Object), clr.GetClrType(Int32), clr.GetClrType(UInt32)
            ftype = Tuple[UInt32, Int32]
            q = ConcurrentQueue[ftype]()
            p_s = Expression.Parameter(t_obj, "sender")
            p_e = Expression.Parameter(t_int, "amount")
            qc = Expression.Constant(q)
            serial = Expression.Convert(Expression.PropertyOrField(Expression.Convert(p_s, ent), "Serial"),
                                        t_uint)
            ctor = clr.GetClrType(ftype).GetConstructor(Array[Type]([t_uint, t_int]))
            enqueue = Expression.Call(qc, q.GetType().GetMethod("Enqueue"),
                                      Array[Expression]([Expression.New(ctor, Array[Expression]([serial, p_e]))]))
            room = Expression.LessThan(Expression.Property(qc, "Count"),
                                       Expression.Constant(DAMAGE_QUEUE_MAX, t_int))
            body = Expression.IfThen(Expression.AndAlso(Expression.TypeIs(p_s, ent), room), enqueue)
            handler = Expression.Lambda[EventHandler[Int32]](
                body, Array[ParameterExpression]([p_s, p_e])).Compile()
            dom = AppDomain.CurrentDomain
            left = dom.GetData(HOOK_KEY)                   # a run that didn't clean up
            if left is not None:
                safe(lambda: ev.GetRemoveMethod(True).Invoke(None, Array[Object]([left])))
            ev.GetAddMethod(True).Invoke(None, Array[Object]([handler]))
            dom.SetData(HOOK_KEY, handler)
            feed.update({"q": q, "handler": handler, "event": ev,
                         "kind": "exact (damage numbers per mobile)"})
            return True
        except Exception as ex:
            feed.update({"q": None, "handler": None, "event": None})
            try:
                if not feed.get("fallback"):
                    API.Events.OnEntityDamage(on_damage_amount)
                    feed["fallback"] = True
                feed["kind"] = "amounts only (%s)" % (str(ex)[:50] or "no hook")
            except Exception:
                feed["kind"] = "off (%s)" % (str(ex)[:50] or "no hook")
            return False

    def unhook_damage():
        h, ev = feed.get("handler"), feed.get("event")
        if h is None or ev is None:
            return
        try:
            from System import Array, Object, AppDomain
            ev.GetRemoveMethod(True).Invoke(None, Array[Object]([h]))
            AppDomain.CurrentDomain.SetData(HOOK_KEY, None)
        except Exception:
            pass
        feed.update({"q": None, "handler": None, "event": None, "kind": "not hooked"})

    def on_damage_amount(*args):                       # fallback feed (amounts only)
        if not st["active"]:
            return
        for a in args:
            try:
                st["amtq"].append(int(a))
            except Exception:
                continue
            del st["amtq"][:-200]
            return

    def last_attack():
        """TargetManager.LastAttack (who you attack in war mode), by reflection."""
        if not refl["tried"]:
            refl["tried"] = True
            try:
                from System.Reflection import BindingFlags
                fl = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                world = None
                f = API.GetType().GetField("World", fl)
                if f is not None:
                    world = f.GetValue(API)
                if world is None:                      # ClassicUO.Client.Game.UO.World
                    sf = BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic
                    ct = API.GetType().Assembly.GetType("ClassicUO.Client")
                    game = ct.GetProperty("Game", sf).GetValue(None, None)
                    uo = game.GetType().GetProperty("UO", fl).GetValue(game, None)
                    world = uo.GetType().GetProperty("World", fl).GetValue(uo, None)
                p = world.GetType().GetProperty("TargetManager", fl)
                tm = p.GetValue(world, None) if p is not None else \
                    world.GetType().GetField("TargetManager", fl).GetValue(world)
                refl["tm"], refl["la"] = tm, tm.GetType().GetProperty("LastAttack", fl)
            except Exception:
                refl["tm"] = refl["la"] = None
        if refl["la"] is None:
            return 0
        try:                                       # every tick: no lambda
            return int(refl["la"].GetValue(refl["tm"], None) or 0)
        except Exception:
            return 0


    # ---------- script events (items used, buffs) ----------
    #  The journal is not an event here any more: it comes from Virtue
    #  Assistant's shared Journal (read once per pass for every module). Before,
    #  Meters took either TazUO's JournalEntryAdded event (a Python call per
    #  line) or, on builds without it, its own scan of 3-30 s of journal every
    #  tick with its own "seen" dict; now there is one source on every build,
    #  each line handed over exactly once (Journal de-duplicates by the line's
    #  time and text, as the scan did).
    def on_used(*args):
        if not st["active"]:
            return
        for a in args:
            try:
                st["used"].append(int(a))
                del st["used"][:-30]
                return
            except Exception:
                continue

    def on_buff(*args):
        if not st["active"]:
            return
        for a in args:
            t = safe(lambda: a.Title)
            if t:
                st["buffq"].append(str(t))
                del st["buffq"][:-50]
                return

    def hook_events():
        if st["hooked"]:
            return
        st["hooked"] = True
        ev = safe(lambda: API.Events)
        if ev is not None:
            safe(lambda: ev.ObjectUsed(on_used))
            safe(lambda: ev.OnBuffAdded(on_buff))


    # ---------- one look at the client (on the client thread) ----------
    def _opt(fn, default):
        """fn() or default: a plain try for the reads that may be missing on a build."""
        try:
            v = fn()
            return default if v is None else v
        except Exception:
            return default

    def _map():
        return API.GetMap()

    def _last_target():
        return API.LastTargetSerial

    def _backpack():
        return API.Backpack

    def sample():
        now = time.time()
        out = {"me": None, "dmg": [], "info": {}, "fhp": {}, "wst": {}, "used": [],
               "pack": None, "friends": None}
        p = player()
        if p is None:
            return out
        # (every tick on the client thread: named helpers, no lambdas built per tick)
        try:
            gold = int(p.Gold or 0)
        except Exception:
            gold = 0
        try:
            war = bool(p.InWarMode)
        except Exception:
            war = False
        ser = int(p.Serial)
        # (2.6.82) your name is read every NAME_EVERY (and at once for another
        # character), not every tick; the rest still every tick (HitsMax too:
        # the heal check compares it, Map: a gate between facets)
        if ser != st["my_ser"] or now >= st["next_name"]:
            st["my_name"] = str(p.Name or "")
            st["my_ser"], st["next_name"] = ser, now + NAME_EVERY
        me = {"ser": ser, "name": st["my_name"], "hits": int(p.Hits),
              "hmax": int(p.HitsMax), "mana": int(p.Mana), "x": int(p.X), "y": int(p.Y),
              "gold": gold, "dead": bool(p.IsDead), "war": war, "poison": bool(p.IsPoisoned),
              "map": int(_opt(_map, 0) or 0)}
        out["me"] = me
        q = feed["q"]
        if q is not None:
            for _ in range(FEED_BURST):
                ok, item = q.TryDequeue()
                if not ok:
                    break
                out["dmg"].append((int(item.Item1), int(item.Item2)))
        mobs = st["mobs"]
        info = out["info"]
        for ser, _ in out["dmg"]:
            if ser not in mobs and ser not in info and ser != me["ser"]:
                m = find_mob(ser)
                info[ser] = str(m.Name or "") if m is not None else ""
        out["lt"] = int(_opt(_last_target, 0) or 0)
        out["la"] = last_attack()
        for ser in st["engaged"]:                 # (2.6.82) then the two below: no list built
            if is_mobile(ser) and ser not in mobs and ser not in info and ser != me["ser"]:
                m = find_mob(ser)
                if m is not None:
                    info[ser] = str(m.Name or "")
        for ser in (out["lt"], out["la"]):
            if is_mobile(ser) and ser not in mobs and ser not in info and ser != me["ser"]:
                m = find_mob(ser)
                if m is not None:
                    info[ser] = str(m.Name or "")
        if now >= st["next_friends"]:
            st["next_friends"] = now + FRIENDS_EVERY
            party = [int(s) for s in (safe(lambda: API.GetPartyMemberSerials(), []) or [])]
            pets = pets_near()
            friends = [int(s) for s in (safe(lambda: API.GetAllFriends(), []) or [])]
            out["friends"] = (party, pets, friends)
            # (2.6.82) which of them the client has now: only those are read every
            # tick (the whole friends list was looked up 4 times a second). In the
            # order of the friendly set (friends, pets, party), you left out; used
            # from the next tick on, as the friendly set made from this look is
            pres, seen = [], set()
            for sers in (friends, pets, party):
                for fs in sers:
                    if fs != me["ser"] and fs not in seen:
                        seen.add(fs)
                        if find_mob(fs) is not None:
                            pres.append(fs)
        else:
            pres = None
        names_due = out["friends"] is not None    # known names: re-read with the friends look
        fhp = out["fhp"]
        for ser in st["present"]:
            m = find_mob(ser)
            if m is not None:
                known = None if names_due else mobs.get(ser)
                fhp[ser] = (int(m.Hits), int(m.HitsMax), bool(m.IsPoisoned),
                            bool(m.IsDead), known or str(m.Name or ""))
        if pres is not None:
            st["present"] = pres
        # A mobile you damaged dies right after its last hit (the killing blow is
        # a hit too), so its death is only looked for within DYING_CHECK_SECS of
        # that hit: two FindMobile calls per watched mobile per tick used to run
        # for every one of up to 40 for the whole WATCH_SECS.
        wst = out["wst"]
        for ser, w in st["watch"].items():
            if now - w["t"] > DYING_CHECK_SECS:
                continue                        # expires in process() without a look
            if find_mob(ser) is not None:
                wst[ser] = "alive"
            elif API.FindMobile(ser | DEATH_BIT) is not None:
                wst[ser] = "dying"
            else:
                wst[ser] = "gone"
        if st["used"]:
            used, st["used"] = st["used"], []
            for ser in used:
                it = API.FindItem(ser)
                if it is not None:
                    out["used"].append((int(it.Graphic), str(it.Name or "")))
        if not settings["scan"]:
            st["pscan"] = None
        elif st["pscan"] is None and now >= st["next_scan"]:
            st["next_scan"] = now + SCAN_EVERY
            bp = _opt(_backpack, 0)
            if bp:
                # [items, next index, (item, amount) pairs, serial sum, amount sum,
                #  when the list was taken]
                st["pscan"] = [pack_list(bp), 0, [], 0, 0, now]
        ps = st["pscan"]
        if ps is not None:
            out["pack"] = pack_step(ps, now)
        return out

    def pack_step(ps, now):
        """(2.6.82) A part of the backpack look: PACK_CHUNK items a tick (a full
        pack is hundreds of items, all read in one frame every 2 s before).
        Cheap first look: the item count, the sum of the serials and the sum of
        the amounts. When all three are as last time nothing was gained, used or
        moved, and the Graphic / Hue / Name work of every item is skipped.
        Returns the pack's totals when the look is done and something changed,
        else None."""
        items, i, pairs, ssum, asum, taken = ps
        n = len(items)
        end = min(n, i + PACK_CHUNK)
        try:
            while i < end:
                it = items[i]
                a = int(it.Amount or 1) or 1
                ssum += int(it.Serial or 0)
                asum += a
                pairs.append((it, a))
                i += 1
        except Exception:
            st["pscan"] = None
            if taken == now:                      # a list taken this tick: as before
                raise
            st["next_scan"] = 0.0                 # an item gone meanwhile: a new look next tick
            return None
        if i < n:
            ps[1], ps[3], ps[4] = i, ssum, asum
            return None
        st["pscan"] = None
        sig = (len(pairs), ssum, asum)
        if sig == st["pack_sig"] and st["pack"] is not None:
            st["pack_cand"] = None
            return None
        if taken != now and st.get("pack_cand") != sig:
            # (2.6.83) a look spread over ticks can catch a stack split or merged
            # halfway (phantom loot or use): it counts once the next look agrees
            st["pack_cand"] = sig
            st["next_scan"] = 0.0
            return None
        st["pack_cand"] = None
        st["pack_sig"] = sig
        tot = {}
        for it, a in pairs:
            k = (int(it.Graphic), int(it.Hue))
            if k in tot:
                tot[k][0] += a
            else:
                tot[k] = [a, None, it]
        prev = st["pack"] or {}
        for k, v in tot.items():          # names only for what's new or grew
            old = prev.get(k)
            if old is None or v[0] > old[0]:
                try:
                    v[1] = str(v[2].Name or "")
                except Exception:
                    v[1] = ""
            else:
                v[1] = old[1]
            v[2] = None
        return tot


    # ---------- turning a look into numbers ----------
    def is_friend(ser):
        me = st["me"]
        return (me is not None and ser == me["ser"]) or ser in st["friendly"]

    def mob_name(ser):
        me = st["me"]
        if me is not None and ser == me["ser"]:
            return me["name"] or "You"
        return st["mobs"].get(ser) or "Unknown"

    def engaged(ser, now):
        t = st["engaged"].get(ser)
        return t is not None and now - t <= settings["engage"]

    def add_pending(now, kind, method, secs, ser=None):
        """Your heal / cure action: claims a rise just seen, or the next one."""
        multi = kind == "cure+"
        kind = "cure" if multi else kind
        for o in list(st["orph"]):
            if o[1] == kind and now - o[0] <= ORPHAN_SECS:
                st["orph"].remove(o)
                credit(kind, method, o[2], o[3], o[4])
                if not multi:
                    return
        st["pend"].append([now + secs, kind, method, multi])

    def credit(kind, method, ser, name, amt):
        if kind == "heal":
            record("heal_done", name, amt, ser)
            if not pct_row(name):
                record("heal_by", method, amt)
        else:
            record("cures_mine", method, 1)

    def claim(kind, now, ser, name, amt):
        """A heal / cure happened: yours if one of your actions waits for it."""
        for p in st["pend"]:
            if p[1] == kind and now <= p[0]:
                if not p[3]:
                    st["pend"].remove(p)
                credit(kind, p[2], ser, name, amt)
                return
        st["orph"].append((now, kind, ser, name, amt))

    def process(s, now):
        me = s["me"]
        if me is None:
            return
        old_me, st["me"] = st["me"], me
        mobs = st["mobs"]
        if len(mobs) > MOBS_MAX:
            mobs.clear()
        for ser, name in s["info"].items():
            if name:
                mobs[ser] = name
        if st["pend"]:                    # (2.6.82) no list made per tick when empty
            st["pend"] = [p for p in st["pend"] if p[0] >= now]
        if st["orph"]:
            st["orph"] = [o for o in st["orph"] if now - o[0] <= ORPHAN_SECS]

        # friendly set: party, your pets, friends list
        if s["friends"] is not None:
            party, pets, friends = s["friends"]
            fr = {}
            for kind, sers in (("friend", friends), ("pet", pets), ("party", party)):
                for ser in sers:
                    fr[ser] = kind
            fr.pop(me["ser"], None)
            st["friendly"] = fr

        # who you are fighting
        lt, la = s.get("lt", 0), s.get("la", 0)
        if la and me["war"] and is_mobile(la) and not is_friend(la):
            st["engaged"][la] = now
        if is_mobile(lt) and not is_friend(lt) and (lt != st["prev_lt"] or now - st["cast_t"] <= 2.0):
            st["engaged"][lt] = now
        st["prev_lt"] = lt
        if st["engaged"]:
            for ser in [k for k, t in st["engaged"].items() if now - t > settings["engage"]]:
                st["engaged"].pop(ser, None)

        # damage
        budget = 0
        if old_me is not None and me["hits"] < old_me["hits"]:
            budget = old_me["hits"] - me["hits"]
        for ser, dmg in s["dmg"]:
            hit(ser, dmg, now)
        if st["amtq"]:
            tgt = None                                   # (2.6.82) looked for once a tick:
            for amt in st["amtq"]:                       # fallback feed: amounts only
                if budget >= amt:
                    budget -= amt
                    hit(me["ser"], amt, now)
                else:
                    # the newest engaged mobile; a hit on it keeps it the newest
                    if tgt is None:
                        tgt = max(st["engaged"].items(), key=lambda kv: kv[1])[0] \
                            if st["engaged"] else 0
                    hit(tgt, amt, now) if tgt else record("dmg_nearby", "Unknown", amt)
            st["amtq"] = []

        # hit points, poison and death of you and your friends
        hp = s["fhp"]                     # (2.6.82) this tick's own dict: no copy
        hp[me["ser"]] = (me["hits"], me["hmax"], me["poison"], me["dead"], me["name"] or "You")
        for ser, (hits, hmax, poison, dead, name) in hp.items():
            if name:
                mobs[ser] = name
            name = mob_name(ser)
            prev = st["prev"].get(ser)
            st["prev"][ser] = (hits, hmax, poison, dead)
            if prev is None:
                continue
            if dead and not prev[3]:
                if now - st["dead_seen"].get(ser, 0) > 10:
                    record("deaths", name, 1, ser)
                    st["dead_seen"][ser] = now
                    if ser == me["ser"] and settings["recap"]:
                        make_recap(now)               # you died: the death recap
                continue
            if dead or prev[3]:
                continue
            real = ser == me["ser"] or st["friendly"].get(ser) == "party" or hmax not in (25, 100)
            dh = hits - prev[0]
            if dh >= (settings["min_heal"] if real else 1) and hmax == prev[1]:
                row = name if real else name + " (%)"
                amt = dh if real else dh * 100.0 / max(1, hmax)
                record("heal_taken", row, amt, ser)
                claim("heal", now, ser, row, amt)
            if poison and not prev[2]:
                record("poisoned", name, 1, ser)
            elif prev[2] and not poison:
                record("cures", name, 1, ser)
                claim("cure", now, ser, name, 1)
        if len(st["prev"]) != len(hp):    # (every key of hp is in prev by now)
            for ser in [k for k in st["prev"] if k not in hp]:
                st["prev"].pop(ser, None)

        # mobiles you damaged: dying means a kill (or a friend's death)
        for ser, state in s["wst"].items():
            w = st["watch"].get(ser)
            if w is None:
                continue
            if state == "dying":
                st["watch"].pop(ser, None)
                if w["friend"]:
                    if now - st["dead_seen"].get(ser, 0) > 10:
                        record("deaths", w["name"], 1, ser)
                        st["dead_seen"][ser] = now
                elif w["mine"] and now - w["mine"] <= KILL_CREDIT_SECS:
                    record("kills", w["name"], 1)
        # (the ones not looked at any more, see sample(), still expire)
        if st["watch"]:
            for ser in [k for k, w in st["watch"].items() if now - w["t"] > WATCH_SECS]:
                st["watch"].pop(ser, None)
        if st["dead_seen"]:
            for ser in [k for k, t in st["dead_seen"].items() if now - t > 30]:
                st["dead_seen"].pop(ser, None)

        # your hit points, for the death recap (each change, the newest HP_KEEP)
        hl = st["hp_log"]
        if not hl or hl[-1][1] != me["hits"] or hl[-1][2] != me["hmax"]:
            hl.append((now, me["hits"], me["hmax"]))
            if len(hl) > HP_KEEP:
                del hl[:len(hl) - HP_KEEP]

        # mana
        if old_me is not None and me["mana"] < old_me["mana"] and not me["dead"]:
            ls = st["last_spell"]
            row = ls[1] if ls is not None and now - ls[0] <= MANA_SECS else "Other"
            record("mana", row, old_me["mana"] - me["mana"])

        # gold
        if old_me is not None and old_me["ser"] == me["ser"]:
            dg = me["gold"] - old_me["gold"]
            if dg > 0:
                record("gold", "Gained", dg)
                record("gold_place", st["place"] or PLACE_ELSEWHERE, dg)
            elif dg < 0:
                record("gold", "Spent / banked", -dg)

        # travel
        pos = (me["x"], me["y"], me["map"])
        if settings["travel"] and st["pos"] is not None and (me["x"] or me["y"]):
            ox, oy, om = st["pos"]
            dist = max(abs(me["x"] - ox), abs(me["y"] - oy))
            if om != me["map"] or dist > JUMP_TILES:
                record("travel", "Recalls, gates & teleports", 1)
            elif dist > 0:
                record("travel", "Tiles walked", dist)
        st["pos"] = pos

        # items used (potions). One row per potion kind, named from POTIONS: the
        # server names the same potion "Greater Heal Potion" or "heal potion" by
        # turns, which used to give it two rows.
        for graphic, name in s["used"]:
            pot = POTIONS.get(graphic)
            if pot is None:
                continue
            label = pot[0] + " potion"
            record("consum", label, 1)
            if pot[1]:                                    # "Heal potion" / "Cure potion"
                add_pending(now, pot[1], pot[0] + " potion", POTION_SECS)

        # backpack: items gained, reagents / ammo used
        pack = s["pack"]
        if pack is not None:
            old = st["pack"]
            # only the first fill is skipped (the client learning the pack's contents
            # when it is first opened); a real haul of many new kinds (a chest
            # emptied into the pack) is counted, as it used to be dropped past 30 kinds
            fresh = old is not None and len(old) == 0 and len(pack) > 0
            if old is not None and not fresh:
                for k, v in pack.items():
                    o = old.get(k)
                    diff = v[0] - (o[0] if o else 0)
                    if diff > 0 and k[0] != GOLD_GRAPHIC:
                        nm = RE_COUNT.sub("", (v[1] or "").strip()) or "Item 0x%04X" % k[0]
                        record("loot", nm.title(), diff)
                    elif diff < 0 and k[0] in CONSUMABLES:
                        record("consum", CONSUMABLES[k[0]], -diff)
                for k, o in old.items():
                    if k not in pack and k[0] in CONSUMABLES:
                        record("consum", CONSUMABLES[k[0]], o[0])
            st["pack"] = pack

        # buffs
        if st["buffq"]:
            for title in st["buffq"]:
                record("buffs", title, 1)
            st["buffq"] = []

    def hit(ser, dmg, now):
        me = st["me"]
        name = mob_name(ser)
        record("dmg_nearby", name, dmg, ser)
        w = st["watch"].get(ser)
        if w is None:
            if len(st["watch"]) >= WATCH_MAX:
                oldest = min(st["watch"].items(), key=lambda kv: kv[1]["t"])[0]
                st["watch"].pop(oldest, None)
            w = st["watch"][ser] = {"name": name, "t": now, "mine": 0.0, "friend": False}
        w["t"], w["name"] = now, name
        if is_friend(ser):
            w["friend"] = ser != me["ser"]
            record("dmg_taken", name, dmg, ser)
            enter_combat()
            if ser == me["ser"]:
                note_taken(dmg, now)            # for the death recap
        elif engaged(ser, now):
            st["engaged"][ser] = now
            w["mine"] = now
            record("dmg_done", name, dmg, ser)
            record_big(dmg, name, ser)
            enter_combat()

    def read_journal(now):
        """The journal lines since the last tick (Journal: each line once).
        Most lines match nothing; each regex now runs only on lines holding the
        words it needs (it used to run all three on every such line). The
        regexes ignore case and every name they give is .title()d, so they run
        on the lower-case line Journal already made."""
        jr = st["jr"]
        if jr is None:
            return
        try:
            lines = jr.new()
        except Exception:
            return
        if not lines:
            return
        me = st["me"]
        my_name = me["name"] if me else None
        for ln in lines:
            name = ln.name
            low = ln.low.strip()
            if my_name and name == my_name:
                sp = SPELLS.get(low)
                if sp is not None:
                    record("spells", sp[0], 1)
                    st["last_spell"] = (now, sp[0])
                    st["cast_t"] = now
                    if sp[1] == "heal":
                        add_pending(now, "heal", sp[0], HEAL_SPELL_SECS)
                    elif sp[1] in ("cure", "cure+"):
                        add_pending(now, sp[1], sp[0], CURE_SECS)
                continue
            if low.startswith(OWN_PREFIX):
                continue
            if low.startswith(MSG_FIZZLE):
                record("spells", "Fizzled", 1)
            elif low.startswith(MSG_INTERRUPT):
                record("spells", "Interrupted", 1)
            elif low.startswith(MSG_NO_MANA):
                record("spells", "Out of mana", 1)
            elif low.startswith(MSG_BANDAGE_BEGIN):
                record("consum", "Bandages", 1)
            elif low.startswith(MSG_BANDAGE_CURE):
                add_pending(now, "cure", "Bandage", BANDAGE_SECS)
            elif low.startswith(MSG_BANDAGE_HEALS):          # (a tuple: any of them)
                add_pending(now, "heal", "Bandage", BANDAGE_SECS)
            else:
                if name and my_name:           # someone else's words of power (death recap)
                    sp = SPELLS.get(low)
                    if sp is not None:
                        if sp[0] in HARM_SET:
                            note_cast(now, name, sp[0])
                        continue
                if "your skill in" in low:
                    m = RE_SKILL.search(low)
                    if m:
                        try:
                            v = float(m.group(3))
                        except ValueError:
                            continue
                        record("skills", m.group(1).strip().title(),
                               v if m.group(2).lower() == "increased" else -v)
                        continue
                if "your " in low and " has " in low:
                    m = RE_STAT.search(low)
                    if m:
                        v = int(m.group(3))
                        record("stats", m.group(1).title(),
                               v if m.group(2).lower() == "increased" else -v)
                        continue
                if "you have " in low and ("fame" in low or "karma" in low):
                    m = RE_FAME.search(low)
                    if m:
                        record("fame", "%s %s" % (m.group(2).title(), m.group(1).lower()), 1)


    # ---------- where you are (Gold by place) ----------
    def find_place(me):
        """Where you are, for Gold by place: the guarded town Virtue Assistant
        knows the name of (HOST.guard_area), else the nearest spot you named
        that you stand in, else Elsewhere."""
        area = None
        ga = getattr(HOST, "guard_area", None)
        if ga is not None:
            try:
                area = ga()
            except Exception:
                area = None
        if area:
            return str(area)
        best = None
        x, y, m = me["x"], me["y"], me["map"]
        for sp in spots:
            if sp[3] == m:
                d = max(abs(x - sp[1]), abs(y - sp[2]))
                if d <= sp[4] and (best is None or d < best[0]):
                    best = (d, sp[0])
        return best[1] if best is not None else PLACE_ELSEWHERE

    def track_place(now, dt):
        """Every tick: the time spent where you are, per segment."""
        me = st["me"]
        if me is None:
            return
        if st["place"] is None or now >= st["next_place"]:
            st["next_place"] = now + PLACE_EVERY
            st["place"] = find_place(me)
        place = st["place"]
        for seg in segs():
            pt = seg["place_t"]
            pt[place] = pt.get(place, 0.0) + dt

    def add_spot(name, radius):
        """Settings' "Name this spot": you, here, with that name and radius
        (a spot of that name already named moves here)."""
        me = st["me"]
        if me is None or not (me["x"] or me["y"]):
            API.SysMsg("%s: your position isn't known yet; try again in a moment." % TITLE,
                       Kit.HUE_BAD)
            return
        name = spot_name(name) or "Spot %d" % (len(spots) + 1)
        lo, hi = SPOT_RADIUS_LIMITS
        radius = max(lo, min(hi, int(radius)))
        old = [sp for sp in spots if sp[0].lower() == name.lower()]
        if not old and len(spots) >= SPOTS_MAX:
            API.SysMsg("%s: %d named spots is the most; remove one first." % (TITLE, SPOTS_MAX),
                       Kit.HUE_BAD)
            return
        for sp in old:
            spots.remove(sp)
        spots.append([name, me["x"], me["y"], me["map"], radius])
        save_spots()
        st["place"] = None                        # looked at again on the next tick
        API.SysMsg("%s: spot \"%s\" named here (%d, %d), %d tiles round." % (
            TITLE, name, me["x"], me["y"], radius), Kit.HUE_GOOD)
        HOST.refresh_settings(KEY)

    def remove_spot(name):
        n = len(spots)
        spots[:] = [sp for sp in spots if sp[0] != name]
        if len(spots) != n:
            save_spots()
            st["place"] = None
            HOST.refresh_settings(KEY)


    # ---------- the death recap's memory ----------
    def friendly_names(now):
        """(2.6.82) Made once a tick at most (the journal is read before the
        names change this tick), not once per harmful spell heard."""
        fn = st["fnames"]
        if fn is not None and fn[0] == now:
            return fn[1]
        mobs = st["mobs"]
        names = set(mobs.get(ser) for ser in st["friendly"] if mobs.get(ser))
        st["fnames"] = (now, names)
        return names

    def note_cast(now, name, spell):
        """Someone else said a harmful spell's words: a hit on you right after
        is credited to them (a party member's or pet's words are not)."""
        if name in friendly_names(now):
            return
        try:
            info = Kit.spell_info(spell)
        except Exception:
            info = None
        delay = float(info[3]) if info else 0.0      # it can't land before its cast delay
        cs = st["casts"]
        cs.append([now, name, spell, False, delay])
        while cs and (len(cs) > CASTS_KEEP or now - cs[0][0] > cs[0][4] + CAST_CREDIT_SECS):
            cs.pop(0)

    def credit_hit(now):
        """(what to show, the mobile's name or None, its serial or 0) for a hit
        on you now. UO doesn't say who hit whom, so: someone whose harmful
        spell could have landed by now (its words, then its cast delay, then
        up to CAST_CREDIT_SECS to aim; each cast credits one hit), else the
        mobile you were fighting (shown with a "?"), else Poison while you
        are poisoned, else Unknown."""
        for c in st["casts"]:                     # oldest first
            el = now - c[0]
            if not c[3] and c[4] - CAST_EARLY <= el <= c[4] + CAST_CREDIT_SECS:
                c[3] = True
                return "%s: %s" % (c[1], c[2]), c[1], 0
        best = None
        for ser, t in st["engaged"].items():
            if best is None or t > best[1]:
                best = (ser, t)
        if best is not None and engaged(best[0], now):
            nm = mob_name(best[0])
            return nm + "?", nm, best[0]
        me = st["me"]
        if me is not None and me["poison"]:
            return "Poison", None, 0
        return "Unknown", None, 0

    def note_taken(dmg, now):
        """A hit on you, kept (the newest TAKEN_KEEP) for the death recap:
        (time, amount, who, who's name, serial, your hits, your max hits)."""
        me = st["me"]
        who, nm, ser = credit_hit(now)
        tk = st["taken"]
        tk.append((now, dmg, who, nm, ser, me["hits"], me["hmax"]))
        if len(tk) > TAKEN_KEEP:
            del tk[:len(tk) - TAKEN_KEEP]

    def make_recap(now):
        """You died: the hits on you and your hit points of the last
        RECAP_SECS, kept as st["recap"] and shown on this tick."""
        t0 = now - RECAP_SECS
        hits = [e for e in st["taken"] if e[0] >= t0]
        hp, before = [], None
        for h in st["hp_log"]:
            if h[0] < t0:
                before = h
            else:
                hp.append(h)
        if before is not None:
            hp.insert(0, (t0, before[1], before[2]))
        me = st["me"]
        if me is not None:                        # this tick's reading (logged after this)
            hp.append((now, me["hits"], me["hmax"]))
        # names of casters -> serials, for Alt+click (one look at the
        # mobiles, only when you die)
        want = set(e[3] for e in hits if e[3] and not e[4])
        sers = {}
        if want:
            for ser, nm in st["mobs"].items():
                if nm in want:
                    sers[nm] = ser
            for m in (safe(lambda: API.GetAllMobiles(), []) or []):
                try:
                    nm = str(m.Name or "")
                    if nm in want:
                        sers[nm] = int(m.Serial)
                except Exception:
                    continue
        rows = [(e[0], e[1], e[2], e[4] or sers.get(e[3], 0), e[5], e[6]) for e in hits]
        st["recap"] = {"t": now, "rows": rows, "hp": hp, "total": sum(e[1] for e in hits)}
        st["recap_show"] = True


    # ---------- Export: every display of a segment, to a text file ----------
    def export(w):
        """Write every display of window w's segment to EXPORT_FILE next to
        Virtue Assistant. The text is made here; the file is written on the
        script's thread (_thread_tick): a disk write here is a frame hitch."""
        seg = seg_for(w)
        cap = seg_caption(w)
        if seg is None:                           # "Current" before the first fight
            seg, cap = data["overall"], "Overall"
        me = st["me"]
        serial = me["ser"] if me else int(safe(lambda: API.Player.Serial, 0) or 0)
        path = os.path.join(str(API.ScriptPath), EXPORT_FILE % serial)
        what = seg["name"] if cap != seg["name"] else ""
        lines = ["Meters export: %s%s, %s" % (cap, " (%s)" % what if what else "",
                                               time.strftime("%Y-%m-%d %H:%M:%S",
                                                             time.localtime(time.time()))),
                 ("Session time %s, in combat %s" % (fmt_time(wall_secs(seg)), fmt_time(seg["combat"]))
                  if seg["kind"] == "overall" else "Fight time %s" % fmt_time(combat_secs(seg))),
                 ""]
        for mid in ORDER:
            head, rows = view(mid, seg, EXPORT_ROWS)
            lines.append("== %s ==" % METRIC[mid][0])
            lines.append("   " + "   ".join(h for h in head if h))
            for i, r in enumerate(rows):
                lines.append("   %2d. %-30s %s" % (i + 1, r[0], r[2]))
            if not rows:
                lines.append("   (nothing)")
            lines.append("")
        st["to_write"].append((path, "\n".join(lines) + "\n", cap))

    def write_files():
        """thread_tick: write the exports export() made (returns at once when none)."""
        while st["to_write"] and not st["shutting"]:
            path, text, cap = st["to_write"].pop(0)
            try:
                with open(path, "w") as fh:
                    fh.write(text)
                API.SysMsg("%s: %s exported to %s." % (TITLE, cap, path), Kit.HUE_GOOD)
            except Exception as ex:
                API.SysMsg("%s: couldn't write %s (%s)." % (TITLE, path, ex), Kit.HUE_BAD)


    # ---------- windows ----------
    queue = Kit.queuer(st)

    def win_by_id(wid):
        return next((w for w in wins if w["id"] == wid), None)

    def dock_key(w):
        return KEY if w["id"] == 0 else "%s_%d" % (KEY, w["id"])

    def win_title(w):
        return TITLE if w["id"] == 0 else "%s %d" % (TITLE, w["id"] + 1)

    def on_disposed(w, g):
        def handler(*args):
            if w["g"] is g and not st["shutting"]:
                w["g"] = None
                if w["id"] == 0:
                    HOST.disable(KEY)
                else:
                    st["queue"].append(("closed", w["id"]))
        return handler

    def on_sub_disposed(w, slot, g):
        def handler(*args):
            if w.get(slot) is g:
                w[slot] = None
        return handler

    def row_click(w, i):
        def handler(*args):
            slots = w["slots"]
            if i >= len(slots):
                return
            ser = slots[i].get("ser")
            if Follow.alt_held():
                if ser:
                    queue(("follow", ser))()
                return
            queue(("detail", w["id"], i))()
        return handler

    def build_window(w):
        x, y = w["x"], w["y"]
        old = w["g"]
        if Kit.is_open(old):
            x, y = old.GetX(), old.GetY()
        w["g"] = None
        M = Kit.MARGIN
        store = ({}, {})
        c = {}
        slots = []
        mid = w["metric"]
        gcols = []
        close_tip = ("Close " + win_title(w) +
                     (" (this window only)" if w["id"]
                      else " (turns it off; the Modules tab turns it back on)"))
        w["resize_at"], w["preview"] = 0.0, False
        if w["minimized"]:
            g = G.CreateGump(True, True)
            ww, hh = MINI_W, MINI_H
            c["status"] = Kit.mini_bar(g, store, ww, hh, win_title(w), dock_key(w),
                                       queue(("toggle_min", w["id"])), close_tip=close_tip)
        else:
            rows = settings["rows"]
            yb = M + 30 + Kit.GAP
            yr = yb + 30 + Kit.GAP
            extra_h = 56 + (GRAPH_BLOCK if w.get("graph") else 0)
            # (2.6.72) the footer never drops its captions: New, Report and Reset in one
            # row when they fit, else Reset (the main window's) wraps on to a second row
            foot_w = 8 + 35 + Kit.text_w("New") + 14 + 35 + Kit.text_w("Report") + 8
            if w["id"] == 0:
                foot_w += 14 + 35 + Kit.text_w("Reset")
            want0 = w.get("fit") or w.get("size")
            fw_room = (max(120, want0[0]) if want0 else W) - 2 * M
            two_rows = foot_w > fw_room
            if two_rows:
                extra_h += 26
            body_h = extra_h + rows * ROW_H
            ww, hh = W, yr + body_h + M
            fit = w.get("fit")
            want = fit if fit is not None else w.get("size")
            if want is not None:
                # in a zone (2.6.57): exactly its slot; free with a size of its own
                # (2.6.64, a corner drag): that size. As many rows as the height
                # holds (at least one; a slot too short for one scrolls, Kit.place),
                # the body section to the bottom edge
                ww, hh = max(120, want[0]), want[1]  # (2.6.58) never wider than its share
                rows = max(1, (hh - yr - M - extra_h) // ROW_H)
                body_h = max(extra_h + rows * ROW_H, hh - yr - M)
                if fit is not None:
                    # (2.6.72) a slot shorter than one row: the body ends at the slot's
                    # bottom and the window scrolls (it ran past its zone)
                    body_h = max(30, min(body_h, hh - yr - M))
                    rows = max(0, (body_h - extra_h) // ROW_H)
                hh = yr + body_h + M
            IW = ww - 2 * M
            g = None
            if fit is None:                      # (2.6.64) free: resizable by its corners
                x, y = Kit.clamp(x, y, ww, hh)       # (window rule 1, for a modern gump)
                min_h = yr + extra_h + ROW_H + M     # one row
                try:
                    g = G.CreateModernGump(x, y, ww, hh, True, min(SIZE_MIN_W, ww),
                                           min(min_h, hh), on_resized(w))
                    safe(lambda: g.SetAlpha(0))      # its own panel hides under the stone
                except Exception:
                    g = None                         # a build without resizable windows
            if g is None:                        # in a zone: the zone gives its size
                g = G.CreateGump(True, True)
            Kit.add_window_frame(g, ww, hh, mouse=False)   # corners free for the drag
            # title: this window's name, Settings, Fold, Minimize, Close (the
            # mother's standard title row; it takes the per-window title and
            # close tip since 2.6.01)
            # (2.6.58) a window too narrow for the Settings button (a narrow zone) leaves
            # it out (the Virtue Assistant window still opens the page)
            title_room = (Kit.MARGIN + 30 + Kit.text_w(win_title(w).upper()) + 16 + 84 + Kit.DOCK_DX
                          + 35 + Kit.text_w("Settings") + Kit.MARGIN)
            Kit.title_bar(g, store, ww, win_title(w), dock_key(w), queue(("toggle_min", w["id"])),
                          queue(("to_bar", w["id"])),
                          queue(("settings",)) if ww >= title_room else None, close_tip=close_tip)
            # toolbar: previous / next display, display list, segment list
            Kit.add_section(g, M, yb, IW, 30)
            bx = M + 8
            Kit.art_button(g, store, "prev", ART_LEFT, bx, yb + 4, None,
                           "Show the previous display", on_click=queue(("step", w["id"], -1)))
            Kit.art_button(g, store, "next", Kit.ART_PLAY, bx + 32, yb + 4, None,
                           "Show the next display", on_click=queue(("step", w["id"], 1)))
            mt, _, _, color, mobrows = METRIC[mid]
            mx = bx + 68
            # (2.6.69) a narrow zone: the display list button loses its caption (the
            # summary line names the display) before the segment button runs past the
            # window's edge, which made the window wider than its zone
            pick_cap = mt if mx + 35 + Kit.text_w(mt) + 10 + 35 + 40 <= M + IW - 6 else None
            Kit.art_button(g, store, "pick", Kit.ART_PAGE, mx, yb + 4, pick_cap,
                           "Open the display list to pick what this window shows"
                           + ("" if pick_cap else " (now: %s)" % mt),
                           on_click=queue(("picker", w["id"])))
            sx = mx + (35 + Kit.text_w(mt) if pick_cap else 30) + 10
            c["seg_room"], c["iw"] = max(20, M + IW - 6 - sx - 35), IW         # (2.6.58) in its row
            seg_cap = Kit.fit(seg_caption(w), c["seg_room"])
            c["seg"] = Kit.art_button(g, store, "segs", Kit.ART_PAGE, sx, yb + 4, seg_cap,
                                      "Open the segment list: the current fight, the whole "
                                      "session (Overall) or an earlier fight",
                                      on_click=queue(("segpick", w["id"])))
            # body: summary line, bars, footer buttons
            Kit.add_section(g, M, yr, IW, body_h)
            c["head"] = Kit.add_label(g, "", M + 8, yr + 5, Kit.HUE_INFO)
            follow = "Alt+click: auto-follow (again to stop)"
            if mid in ("session", "big", "gold"):     # rows with no details window
                tip = follow if mobrows else None
            else:
                tip = "Open this row's details" + (". " + follow if mobrows else "")
            val_w = min(VAL_W, int(IW * 0.45))      # (2.6.58) a narrow window: shared
            name_w = IW - 12 - val_w - 10
            for i in range(rows):
                ry = yr + 26 + i * ROW_H
                pb = G.CreateGumpSimpleProgressBar(IW - 12, ROW_H - 2, BAR_BG, color, 0, 100)
                pb.SetPos(M + 6, ry)
                safe(lambda: pb.SetAcceptMouseInput(False))
                g.Add(pb)
                ln = Kit.add_label(g, "", M + 10, ry + 1, Kit.HUE_TEXT)
                lv = Kit.add_label(g, "", M + IW - 6 - val_w, ry + 1, Kit.HUE_TEXT)
                slots.append({"bar": pb, "name": ln, "val": lv, "ser": None, "key": None,
                              "prog": None, "nw": name_w, "vw": val_w})
            for i in range(rows):
                ry = yr + 26 + i * ROW_H
                Kit.catcher(g, M + 6, ry, IW - 12, ROW_H - 2, row_click(w, i), tip)
            fy = yr + 26 + rows * ROW_H + 4
            if w.get("graph"):                    # the last hour, one bar per minute
                gy = fy - 2
                c["gcap"] = Kit.add_label(g, "", M + 10, gy, Kit.HUE_INFO)
                base = gy + 18 + GRAPH_H
                # (2.6.64) a narrow window shows the most recent minutes that fit
                ncol = max(1, min(GRAPH_MINUTES, (IW - 12) // (GRAPH_COL + 1)))
                gx = M + 6 + (IW - 12 - ncol * (GRAPH_COL + 1)) // 2
                for i in range(ncol):
                    box = G.CreateGumpColorBox(0.9, color)
                    box.SetRect(gx + i * (GRAPH_COL + 1), base - 1, GRAPH_COL, 1)
                    safe(lambda: setattr(box, "IsVisible", False))
                    safe(lambda: box.SetAcceptMouseInput(False))
                    g.Add(box)
                    gcols.append({"box": box, "x": gx + i * (GRAPH_COL + 1), "h": 0})
                c["gbase"] = base
                fy += GRAPH_BLOCK
            # (2.6.72) captions always (short, verb first); a narrow window puts Reset
            # on a second row instead of dropping every caption
            Kit.art_button(g, store, "new", Kit.ART_PAGE, M + 8, fy, "New",
                           "Open another meter window (up to %d)" % MAX_WINDOWS,
                           on_click=queue(("new",)))
            rx = M + 8 + 35 + Kit.text_w("New") + 14
            Kit.art_button(g, store, "report", Kit.ART_PAGE, rx, fy, "Report",
                           "Put this display's top %d rows in party chat (in a party, if the "
                           "Meters settings page says so), else in your journal" % REPORT_ROWS,
                           on_click=queue(("report", w["id"])))
            if w["id"] == 0:
                ry2 = fy + 26 if two_rows else fy
                Kit.art_button(g, store, "reset", Kit.ART_CLOSE,
                               ww - M - 8 - 35 - Kit.text_w("Reset"),
                               ry2, "Reset", "Clear every meter and start a new session",
                               on_click=queue(("reset",)))
        x, y = Kit.place(g, x, y, ww, hh)            # wholly on screen
        if safe(lambda: HOST.layout_locked(dock_key(w)), False):
            safe(lambda: setattr(g, "CanMove", False))   # (2.6.72) held in its zone
        w.update({"g": g, "c": c, "store": store, "slots": slots, "x": x, "y": y,
                  "vkey": None, "gcols": gcols, "gkey": None,   # new controls: drawn in full
                  "drawn": (ww, hh)})
        G.AddControlOnDisposed(g, on_disposed(w, g))
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, moved(w, g)))
        if w["minimized"] and w["docked"]:
            safe(lambda: setattr(g, "IsVisible", False))
        for k in ("picker", "segpick", "detail"):   # (2.6.64) its side windows: on the new one
            sub = w.get(k)
            if Kit.is_open(sub) and not w["minimized"]:
                # (2.6.71) placed at its own size: a side window that scrolls reads
                # back wider (its bar) and cut, and was made wider at each redraw
                info = Kit.scroll_info(sub)
                if info is not None:
                    sw, sh = int(info["w"]), int(info["h"])
                else:
                    sw = int(safe(lambda: sub.GetWidth(), PICK_W) or PICK_W)
                    sh = int(safe(lambda: sub.GetHeight(), 200) or 200)
                sx, sy = side_pos(w, sw, sh)
                Kit.place(sub, sx, sy, sw, sh)
                safe(lambda: Kit.attach(sub, g))
        refresh_window(w)
        Kit.dispose(old)

    def moved(w, g):
        """(2.6.64) The window was let go (or moved with a window it is snapped
        to): its place is saved, and the layout is asked to slot it in the zone
        under it (or free it outside every zone) when it isn't on its slot
        already. The layout's own drop does the same for a drag; this makes
        sure a meter window let go on a zone always takes it."""
        # (2.6.72) only saves now: the layout itself hears every drag let go
        # (Snap.on_drop), and this ran for moves made by code too (a window towed
        # by another, the keeper's shifts), each one taken for a drop
        def fn():
            save_windows()
        return fn

    def on_resized(w):
        """(2.6.64) A step of a corner drag (the client, about every 75 ms): the
        window's own panel shows meanwhile as a preview of the new size; the
        rows follow once the drag has settled (apply_resize, from the tick)."""
        def fn(*args):
            w["resize_at"] = time.time()
            g = w["g"]
            if w["preview"] or w["fit"] is not None or w["minimized"] or not Kit.is_open(g):
                return
            try:                                     # only a real change of size shows the
                same = (int(g.GetWidth()), int(g.GetHeight())) == w["drawn"]
            except Exception:                        # preview (a client that reports the
                same = False                         # first SetRect too would flash it)
            if not same:
                w["preview"] = True
                safe(lambda: g.SetAlpha(0.55))
        return fn

    def apply_resize(w):
        """(2.6.64) A corner drag was let go: that size is the window's own from
        now on (saved), drawn again with as many rows as it holds. In a zone the
        zone keeps its size (the window is drawn at its slot again)."""
        g = w["g"]
        w["preview"] = False
        if not Kit.is_open(g) or w["minimized"]:
            return
        try:
            gw, gh = int(g.GetWidth()), int(g.GetHeight())
        except Exception:
            return
        if w["fit"] is not None:
            safe(lambda: g.SetAlpha(0))
            if (gw, gh) != w["drawn"]:
                build_window(w)
            return
        drawn = w["drawn"] or (0, 0)
        if abs(gw - drawn[0]) <= 2 and abs(gh - drawn[1]) <= 2:
            safe(lambda: g.SetAlpha(0))              # a drag that changed nothing
            return
        sh = (Kit.screen() or (0, 0))[1]
        if sh > 0:
            gh = min(gh, sh)                         # never taller than the screen
        w["size"] = (max(SIZE_MIN_W, min(SIZE_MAX_W, gw)), max(60, gh))
        build_window(w)
        save_windows()

    def side_pos(w, width, height):
        g = w["g"]
        x, y = (g.GetX(), g.GetY()) if Kit.is_open(g) else (w["x"], w["y"])
        r = safe(lambda: Kit.rect(g)) if Kit.is_open(g) else None
        if r is not None:                    # (2.6.70) a window just rebuilt reads 0, 0 for a frame
            x, y = r[0], r[1]
        sw = (Kit.screen() or (0, 0))[0]
        nx = x + ((w.get("drawn") or (W, 0))[0]) + 4       # (2.6.64) its width as drawn
        if sw and nx + width > sw:
            nx = max(0, x - width - 4)
        return nx, y

    def sub_window(w, slot, width, hh, title, close_key, close_tip):
        """A side window (picker / segments / details): frame, title and Close."""
        M = Kit.MARGIN
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, width, hh)
        Kit.add_section(g, M, M, width - 2 * M, 30)
        Kit.add_label(g, title, M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, ({}, {}), close_key, Kit.ART_CLOSE, width - M - 54, M + 4, None,
                       close_tip, on_click=queue(("close_sub", w["id"], slot)))
        return g

    def show_sub(w, slot, g, width, hh):
        """Put a side window up next to its meter window."""
        x0, y0 = side_pos(w, width, hh)
        Kit.place(g, x0, y0, width, hh)              # wholly on screen
        w[slot] = g
        G.AddControlOnDisposed(g, on_sub_disposed(w, slot, g))
        G.AddGump(g)
        safe(lambda: Kit.attach(g, w["g"]))          # placed by its meter window: kept as a pair

    def build_picker(w):
        Kit.dispose(w["picker"])
        w["picker"] = None
        M = Kit.MARGIN
        IW = PICK_W - 2 * M
        col = (IW - 24) // 2
        hs = [28 + ((len(ms) + 1) // 2) * 22 + 6 for _, ms in GROUPS]
        h_win = 28 + 2 * 22 + 6                    # THIS WINDOW: graph, export
        hh = M + 30 + sum(h + Kit.GAP for h in hs) + h_win + Kit.GAP + M
        g = sub_window(w, "picker", PICK_W, hh, "DISPLAYS", "pclose", "Close")
        y = M + 30 + Kit.GAP
        for (gname, ms), h in zip(GROUPS, hs):
            Kit.add_section(g, M, y, IW, h, gname)
            for i, mid in enumerate(ms):
                cx = M + 12 + (i % 2) * (col + 12)
                cy = y + 28 + (i // 2) * 22
                hue = Kit.HUE_TITLE if mid == w["metric"] else Kit.HUE_TEXT
                Kit.add_label(g, trunc(METRIC[mid][0], col - 4), cx, cy, hue)
                Kit.catcher(g, cx - 2, cy - 2, col, 20, queue(("metric", w["id"], mid)),
                            "Show %s in this window" % METRIC[mid][0])
            y += h + Kit.GAP
        # this window's own switches (2.6.05): the graph under its rows, Export
        Kit.add_section(g, M, y, IW, h_win, "THIS WINDOW")
        on = bool(w.get("graph"))
        state = "on" if on else "off"
        Kit.add_label(g, trunc("Graph of the last hour under the rows", IW - 36 - Kit.text_w(state)),
                      M + 12, y + 28)
        Kit.add_label(g, state, M + IW - 12 - Kit.text_w(state), y + 28,
                      Kit.HUE_GOOD if on else Kit.HUE_INFO)
        Kit.catcher(g, M + 8, y + 26, IW - 16, 20, queue(("graph", w["id"])),
                    "Show or hide a graph of this display's last hour under the rows "
                    "(one bar per minute)")
        Kit.add_label(g, trunc("Export this segment to a text file", IW - 24), M + 12, y + 50)
        Kit.catcher(g, M + 8, y + 48, IW - 16, 20, queue(("export", w["id"])),
                    "Write every display of this segment to %s next to Virtue Assistant"
                    % (EXPORT_FILE.replace("%08X", "<serial>")))
        show_sub(w, "picker", g, PICK_W, hh)

    def build_segpick(w):
        Kit.dispose(w["segpick"])
        w["segpick"] = None
        M = Kit.MARGIN
        IW = PICK_W - 2 * M
        items = [("current", "Current fight" + (" (going on)" if data["cur"] else " (or the last)"), ""),
                 ("overall", "Overall (the whole session)", fmt_time(time.time() - data["overall"]["start"]))]
        for h in data["hist"]:
            items.append((h["n"], "#%d  %s" % (h["n"], h["name"]),
                          "%s  %s" % (fmt_time(combat_secs(h)), fmt_num(total(h, "dmg_done")))))
        sh = 28 + len(items) * 22 + 6
        hh = M + 30 + Kit.GAP + sh + M
        g = sub_window(w, "segpick", PICK_W, hh, "SEGMENTS", "sclose", "Close")
        y = M + 30 + Kit.GAP
        Kit.add_section(g, M, y, IW, sh, "WHAT TO SHOW  (fight time, damage done)")
        rw = 110
        for i, (val, text, right) in enumerate(items):
            cy = y + 28 + i * 22
            hue = Kit.HUE_TITLE if val == w["seg"] else Kit.HUE_TEXT
            Kit.add_label(g, trunc(text, IW - 24 - rw - 6), M + 12, cy, hue)
            if right:
                Kit.add_label(g, right, M + IW - 12 - rw, cy, Kit.HUE_INFO)
            Kit.catcher(g, M + 8, cy - 2, IW - 16, 20, queue(("seg", w["id"], val)),
                        "Show this segment in the meter window")
        show_sub(w, "segpick", g, PICK_W, hh)

    DETAIL_LINES = ("Total", "Share", "Rate", "Times", "Average", "Biggest", "Smallest",
                    "First", "Last")

    def build_detail(w):
        Kit.dispose(w["detail"])
        w["detail"] = None
        M = Kit.MARGIN
        IW = DETAIL_W - 2 * M
        sh = 30 + len(DETAIL_LINES) * 20 + 6
        hh = M + 30 + Kit.GAP + sh + M
        g = sub_window(w, "detail", DETAIL_W, hh, "DETAILS", "dclose", "Close")
        c = {}
        y = M + 30 + Kit.GAP
        Kit.add_section(g, M, y, IW, sh)
        c["name"] = Kit.add_label(g, "", M + 10, y + 6, Kit.HUE_TITLE)
        lw = max(Kit.text_w(t) for t in DETAIL_LINES) + 14
        for i, t in enumerate(DETAIL_LINES):
            ly = y + 30 + i * 20
            Kit.add_label(g, t, M + 10, ly, Kit.HUE_INFO)
            c[t] = Kit.add_label(g, "", M + 10 + lw, ly, Kit.HUE_TEXT)
        c["vw"] = IW - 20 - lw
        w["dc"] = c
        show_sub(w, "detail", g, DETAIL_W, hh)
        refresh_detail(w)

    def refresh_graph(w):
        """The last hour's bars (the graph is wall-clock time, whatever the
        segment): worked out again only when a minute passes or something
        was recorded, and each bar is touched only when its height changes."""
        mid = w["metric"]
        m = int(time.time() // 60)
        key = (mid, m, graph["ver"], graph["vb"].get(mid, 0))   # (2.6.82) its display's own
        if key == w["gkey"]:
            return
        w["gkey"] = key
        hist = graph["hist"]
        vals = []
        top = 0.0
        if mid != "session":
            first = m - GRAPH_MINUTES + 1
            for i in range(GRAPH_MINUTES):
                b = hist.get(first + i)
                v = b.get(mid, 0.0) if b is not None else 0.0
                if v > top:
                    top = v
                vals.append(v)
        base = w["c"]["gbase"]
        skip = len(vals) - len(w["gcols"])       # (2.6.64) fewer bars: the latest minutes
        for i, col in enumerate(w["gcols"]):
            v = vals[i + skip] if vals else 0.0
            h = int(round(GRAPH_H * v / top)) if top > 0 and v > 0 else 0
            if v > 0 and h < 1:
                h = 1
            if h != col["h"]:
                box = col["box"]
                try:                              # up to 60 bars: no lambda per bar
                    if h:
                        Kit.ui_rect(box, col["x"], base - h, GRAPH_COL, h)
                    if (h > 0) != (col["h"] > 0):
                        box.IsVisible = h > 0
                except Exception:
                    pass
                col["h"] = h
        if mid == "session":
            cap = "No graph for the summary: pick another display"
        elif top <= 0:
            cap = "Last hour, per minute: nothing yet"
        else:
            cap = "Last hour, %s per minute: peak %s" % (
                "biggest hit" if mid == "big" else "gained" if mid in ("gold", "gold_place")
                else "total", fmt_num(top, METRIC[mid][2] or "n"))
        Kit.set_text(w["c"]["gcap"], trunc(cap, w["c"].get("iw", W - 2 * Kit.MARGIN) - 20))

    def fit_once(holder, k, text, width):
        """(2.6.82) Kit.fit(text, width), worked out again only when the text or
        the room changed (holder: a slot's or window's dict, rebuilt with it)."""
        f = holder.get(k)
        if f is not None and f[0] == text and f[1] == width:
            return f[2]
        cut = Kit.fit(text, width)
        holder[k] = (text, width, cut)
        return cut

    def refresh_window(w):
        g = w["g"]
        if not Kit.is_open(g):
            return
        mid = w["metric"]
        if w.get("gcols") and not w["minimized"]:
            refresh_graph(w)                  # before the finished-fight shortcut below
        seg = seg_for(w)
        me = st["me"]
        my_name = me["name"] if me else None
        # A finished fight never changes (its rates use its own end time), and
        # out of combat "Current" shows the last finished fight: nothing to do
        # once it is drawn, as long as the window shows the same thing the
        # same way. (The details beside it show "ago" times: still refreshed.)
        # 2.6.82: the same for a segment going on when the display depends on
        # nothing but its numbers and the combat clock (the per-second displays:
        # out of combat Overall's damage and healing can't change); a display
        # with a wall-clock rate or duration (per minute / hour, Gold, the
        # summary, Biggest hits) is still worked out every time
        key = None
        if seg is not None:
            if seg["end"] is not None:
                key = (mid, w["seg"], seg["uid"], seg["ver"], w["minimized"], settings["rank"],
                       settings["pct"], my_name)
            elif METRIC[mid][1] == "s":
                key = (mid, w["seg"], seg["uid"], seg["ver"], seg["combat"], w["minimized"],
                       settings["rank"], settings["pct"], my_name)
            if key is not None and key == w.get("vkey"):
                refresh_detail(w)
                return
        w["vkey"] = key
        head, rows = view(mid, seg, 0 if w["minimized"] else len(w["slots"]))
        c = w["c"]
        if w["minimized"]:
            lbl = c.get("status")
            if lbl is not None:
                Kit.set_text(lbl, fit_once(c, "_fst", "%s: %s  %s" % (win_title(w), METRIC[mid][0],
                                                                      "  ".join(head[:2])),
                                           MINI_W - 90))
            return
        Kit.set_text(c["head"], fit_once(c, "_fhd", "   ".join(h for h in head if h),
                                         c.get("iw", W - 2 * Kit.MARGIN) - 16))
        Kit.set_text(c["seg"], fit_once(c, "_fsg", seg_caption(w), c.get("seg_room", 400)))
        top = max([r[1] for r in rows] + [0.0])
        for i, slot in enumerate(w["slots"]):
            if i < len(rows):
                name, val, text, ser, _ = rows[i]
                label = ("%d. %s" % (i + 1, name)) if settings["rank"] else name
                hue = Kit.HUE_TITLE if (my_name and name == my_name) else Kit.HUE_TEXT
                Kit.set_text(slot["name"], fit_once(slot, "_fn", label, slot["nw"]), hue)
                Kit.set_text(slot["val"], fit_once(slot, "_fv", text, slot.get("vw", VAL_W)))
                prog = (float(val), float(top or 1.0))
                slot["ser"], slot["key"] = (ser if is_mobile(ser) else None), name
            else:
                Kit.set_text(slot["name"], "")
                Kit.set_text(slot["val"], "")
                prog = (0.0, 1.0)
                slot["ser"], slot["key"] = None, None
            if prog != slot["prog"]:
                slot["prog"] = prog
                try:                              # every second per row: no lambda
                    slot["bar"].SetProgress(prog[0], prog[1])
                except Exception:
                    pass
        refresh_detail(w)

    def refresh_detail(w):
        if not Kit.is_open(w["detail"]):
            return
        c = w["dc"]
        mid, key = w["detail_metric"], w["detail_row"]
        seg = seg_for(w)
        r = seg["d"].get(mid, {}).get(key) if (seg is not None and mid) else None
        Kit.set_text(c["name"], trunc("%s (%s)" % (key or "", METRIC.get(mid, ("",))[0]),
                                      DETAIL_W - 2 * Kit.MARGIN - 20))
        vals = dict((t, "") for t in DETAIL_LINES)
        if r is not None:
            _, rate, f, _, _ = METRIC[mid]
            now = time.time()
            tot = total(seg, mid)
            if mid == "gold_place":               # per hour spent in that place
                pr, secs = place_rate(seg, key, r[0])
                rate_txt = "%s/h (%s there)" % (fmt_rate(pr), fmt_time(secs))
            elif rate:
                rate_txt = "%s %s" % (fmt_rate(rate_of(seg, rate, r[0]), f), RATE_WORD[rate])
            else:
                rate_txt = "-"
            vals.update({
                "Total": fmt_num(r[0], f),
                "Share": ("%d%% of %s" % (int(round(100.0 * r[0] / tot)), fmt_num(tot, f))
                          if tot and not pct_row(key) else "-"),
                "Rate": rate_txt,
                "Times": "%d" % r[1],
                "Average": fmt_num(r[0] / max(1, r[1]), f),
                "Biggest": fmt_num(r[2], f),
                "Smallest": fmt_num(r[3], f),
                "First": "%s ago" % fmt_time(now - r[4]),
                "Last": "%s ago" % fmt_time(now - r[5])})
        elif key:
            vals["Total"] = "nothing in this segment"
        for t in DETAIL_LINES:
            Kit.set_text(c[t], trunc(vals[t], c["vw"]))

    def refresh_all():
        for w in wins:
            if not w["docked"]:              # folded into the Action Bar: hidden, and
                refresh_window(w)            # redrawn (with its numbers) when shown

    def _dock_hooks(*args, **kw):
        """Kit.dock_hooks with the 2.6.55 zone-fit keywords (scale=True: the
        layout may scale the window, which is rebuilt whole and never moves a
        control after building), or without them on an older mother."""
        try:
            return Kit.dock_hooks(*args, **kw)
        except TypeError:
            return Kit.dock_hooks(*args)


    def drag_busy():
        """(2.6.74) A window is being dragged (the host's list) or the left
        button is held: no meter window is rebuilt or put on a new place now.
        Asked only when work waits (SNAP.pressed() asks the client)."""
        try:
            if SNAP.drag:
                return True
        except Exception:
            pass
        try:
            return SNAP.pressed() is True
        except Exception:
            return False

    def layout_fit(w):
        """(2.6.57) The layout's "fit" hook for meter window w: its slot is
        fw x fh (None: freed); the window is then drawn exactly that size
        (exact). Client thread, the keeper's pass: records and queues a redraw."""
        def fit(fw, fh, mode):
            new = (int(fw), int(fh)) if (fw is not None and fh is not None) else None
            # (2.6.69) "again": the layout measured the window and it isn't its slot's
            # size, so it is drawn again even though the slot is the one it was told
            if new != w.get("fit") or (mode == "again" and new is not None):
                w["fit"] = new
                queue(("redraw", w["id"]))()
        return fit

    def check_zones():
        """(2.6.64) Every half second: each meter window is the size its zone
        wants (HOST.layout_slot) or, free, its own size again. The layout tells
        a window its slot once (layout_fit); this puts right a fit that went
        astray (a slot told while the window was being rebuilt, a rebuild that
        failed), so a window in a zone always conforms to it."""
        slot_of = getattr(HOST, "layout_slot", None)
        if slot_of is None:                      # an older mother: layout_fit alone
            return
        # (2.6.72) never while a window is being dragged: a rebuild under the mouse
        # made the client lose the drag (the jump), then the keeper put the new
        # window back on its slot (the spring-back)
        if drag_busy():                          # (2.6.74) the shared check
            return
        for w in wins:
            g = w["g"]
            if w["minimized"] or w["docked"] or w["resize_at"] or not Kit.is_open(g):
                continue
            try:
                want = slot_of(dock_key(w))
            except Exception:
                continue
            if want is not None:
                want = (int(want[0]), int(want[1]))
                fit = w["fit"]
                if fit is None or abs(fit[0] - want[0]) > 4 or abs(fit[1] - want[1]) > 4:
                    w["fit"] = want
                    build_window(w)
                    continue
                if w["drawn"] is None or w["drawn"][0] != max(120, fit[0]):
                    build_window(w)              # drawn at another width than its slot's
                    continue
                try:                             # (2.6.69) and the window as it really is
                    real = (int(g.GetWidth()), int(g.GetHeight()))
                except Exception:
                    real = None
                if real is not None and (abs(real[0] - w["drawn"][0]) > 2
                                         or abs(real[1] - w["drawn"][1]) > 2):
                    w["misfit"] = w.get("misfit", 0) + 1
                    if w["misfit"] in (2, 6, 20):    # a few tries, never a rebuild every look
                        build_window(w)
                else:
                    w["misfit"] = 0
            elif w["fit"] is not None and not safe(lambda: HOST.layout_holds(dock_key(w)), False):
                w["fit"] = None                  # freed: its own size again
                build_window(w)

    def dock_win(w):
        # (2.6.57) in a zone the window lays itself out for its slot (fit + exact):
        # 2.6.56 left it to the layout's stretch, which left it at its drawn size
        hooks = _dock_hooks(win_title(w), TRAY_ICON, w, w, queue(("redraw", w["id"])))
        hooks["fit"] = layout_fit(w)
        hooks["exact"] = True
        hooks["verify"] = True        # (2.6.69) measured by the layout every pass
        # (2.6.69) its side windows (display list, segments, details) ride beside it,
        # outside its slot: they never take room from it (they took it from the
        # meter window, which was drawn that much narrower than its zone)
        hooks["pieces_out"] = True
        HOST.dock_add(dock_key(w), hooks)

    def open_all():
        for w in wins:
            build_window(w)
            dock_win(w)

    def close_window(w, remove):
        w["shutting"] = True
        HOST.dock_remove(dock_key(w))
        if remove:
            HOST.dock_forget(dock_key(w))
        for k in ("picker", "segpick", "detail", "g"):
            g, w[k] = w[k], None
            Kit.dispose(g)
        if remove and w in wins:
            wins.remove(w)

    # ---------- the death recap window ----------
    def recap_click(i):
        """A recap row: Alt+click auto-follows the mobile it names (if known)."""
        def handler(*args):
            sers = recap["rows"]
            if i < len(sers) and sers[i] and Follow.alt_held():
                queue(("follow", sers[i]))()
        return handler

    def recap_disposed(g):
        def handler(*args):
            if recap["g"] is g:
                recap["g"] = None
        return handler

    def save_recap_pos():
        Kit.save_pos(RECAP_POS_KEY, recap["g"])

    def close_recap():
        g, recap["g"] = recap["g"], None
        if Kit.is_open(g):
            Kit.save_pos(RECAP_POS_KEY, g)
        Kit.dispose(g)
        recap["rows"] = []

    def recap_hp_at(hp, t):
        """(hits, max hits) at time t from the readings (oldest first)."""
        cur = hp[0] if hp else (t, 0, 0)
        for h in hp:
            if h[0] > t:
                break
            cur = h
        return cur[1], cur[2]

    def build_recap():
        """The death recap: the last RECAP_SECS of hits on you, your hit point
        line falling, who hit you. Made when you die (rare), so it is simply
        built again each time rather than pooled."""
        rc = st["recap"]
        if rc is None:
            return
        old = recap["g"]
        recap["g"] = None
        M = Kit.MARGIN
        IW = RECAP_W - 2 * M
        rows = rc["rows"][-RECAP_ROWS:]
        strip_h = 30
        sh = 30 + 20 + strip_h + 8 + max(1, len(rows)) * 20 + 2 * 18 + 6
        hh = M + 30 + Kit.GAP + sh + M
        if Kit.is_open(old):
            x, y = old.GetX(), old.GetY()
        else:
            dx, dy = side_pos(wins[0], RECAP_W, hh) if wins else (200, 200)
            x, y = Kit.load_pos(RECAP_POS_KEY, (dx, dy), (RECAP_W, hh))
        store = ({}, {})
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, RECAP_W, hh)
        Kit.add_section(g, M, M, IW, 30)
        Kit.add_label(g, "DEATH RECAP", M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, RECAP_W - M - 54, M + 4, None,
                       "Close", on_click=queue(("recap_close",)))
        y0 = M + 30 + Kit.GAP
        Kit.add_section(g, M, y0, IW, sh, "LAST %d SECONDS  (damage you took)" % int(RECAP_SECS))
        n = len(rc["rows"])
        head = "Died %s:  %s damage in %d hit%s" % (
            time.strftime("%H:%M:%S", time.localtime(rc["t"])), fmt_num(rc["total"]), n,
            "" if n == 1 else "s")
        Kit.add_label(g, trunc(head, IW - 20), M + 10, y0 + 26, Kit.HUE_TEXT)
        # the hit point line: one bar per slice of the seconds, its height your HP
        ys = y0 + 26 + 20
        Kit.add_label(g, "HP", M + 10, ys + (strip_h - 16) // 2, Kit.HUE_INFO)
        sx0 = M + 10 + Kit.text_w("HP") + 8
        cw = max(2, (M + IW - 10 - sx0) // RECAP_COLS)
        t0 = rc["t"] - RECAP_SECS
        for i in range(RECAP_COLS):
            hits, hmax = recap_hp_at(rc["hp"], t0 + (i + 1) * RECAP_SECS / RECAP_COLS)
            bh = int(round(strip_h * max(0, hits) / float(hmax))) if hmax > 0 else 0
            if bh > 0:
                box = G.CreateGumpColorBox(0.9, "#c22d2d")
                box.SetRect(sx0 + i * cw, ys + strip_h - bh, max(1, cw - 1), bh)
                g.Add(box)
        # the hits, oldest first, the killing blow last
        yr = ys + strip_h + 8
        sers = []
        if not rows:
            Kit.add_label(g, "No damage numbers were seen in that time.", M + 10, yr, Kit.HUE_INFO)
        who_x, who_w = M + 60, IW - 166
        for i, (t, dmg, who, ser, hits, hmax) in enumerate(rows):
            ry = yr + i * 20
            Kit.add_label(g, "-%.1fs" % max(0.0, rc["t"] - t), M + 10, ry, Kit.HUE_INFO)
            Kit.add_label(g, trunc(who, who_w), who_x, ry, Kit.HUE_TEXT)
            amt = "-%s" % fmt_num(dmg)
            Kit.add_label(g, amt, M + IW - 64 - Kit.text_w(amt), ry, Kit.HUE_BAD)
            Kit.add_label(g, "HP %d" % hits, M + IW - 58, ry, Kit.HUE_INFO)
            sers.append(ser if is_mobile(ser) else 0)
            if sers[-1]:
                Kit.catcher(g, who_x - 2, ry - 2, who_w + 4, 20, recap_click(i),
                            "Alt+click: auto-follow (again to stop)")
        for i, line in enumerate(RECAP_HINT):
            Kit.add_label(g, trunc(line, IW - 20), M + 10, y0 + sh - 40 + i * 18, Kit.HUE_INFO)
        Kit.place(g, x, y, RECAP_W, hh)              # wholly on screen
        recap.update({"g": g, "store": store, "rows": sers})
        G.AddControlOnDisposed(g, recap_disposed(g))
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, save_recap_pos))   # saved the moment you let go of it
        Kit.dispose(old)

    def report(w):
        mid = w["metric"]
        seg = seg_for(w)
        head, rows = view(mid, seg, REPORT_ROWS)
        title = "%s (%s)" % (METRIC[mid][0], seg_caption(w))
        parts = ["%d. %s %s" % (i + 1, r[0], r[2]) for i, r in enumerate(rows[:REPORT_ROWS])]
        in_party = bool(safe(lambda: API.GetPartyMemberSerials(), []) or [])
        if settings["party"] and in_party:
            body = "; ".join(parts) or "nothing yet"
            msg = "%s: %s - %s" % (title, "  ".join(head[:2]), body)
            if len(msg) <= PARTY_MSG_MAX:
                lines = [msg]
            else:                                 # too long for one line: the rows on a second
                lines = ["%s: %s" % (title, "  ".join(head[:2])), body]
            for line in lines:
                if len(line) > PARTY_MSG_MAX:     # still too long: cut, and say so
                    line = line[:PARTY_MSG_MAX - 2] + ".."
                safe(lambda: API.PartyMsg(line))
        else:
            API.SysMsg("%s: %s: %s." % (TITLE, title, "  ".join(head)), Kit.HUE_INFO)
            for p in parts or ["nothing yet"]:
                API.SysMsg("%s:    %s." % (TITLE, p), Kit.HUE_TEXT)


    # ---------- settings page (drawn inside the Virtue Assistant window) ----------
    # (key, label, tooltip without its range, unit shown after the box)
    FIELDS = (("idle", "A fight ends after this much quiet:",
               "No damage dealt or taken for this long ends the current fight", "s"),
              ("engage", "Count damage on what you attacked or targeted within:",
               "Damage on a mobile you attacked or targeted this recently counts as yours", "s"),
              ("history", "Earlier fights kept in the segment list:",
               "How many finished fights the segment list remembers", "fights"),
              ("min_heal", "Ignore HP rises smaller than:",
               "HP rises below this count as regeneration, not healing", "HP"),
              ("rows", "Rows in each meter window:",
               "Bar rows in a meter window of its own size; changing it undoes corner drags",
               "rows"))
    CHECKS = (("rank", "Number the rows (1. 2. 3. ...)",
               "Put a rank number before each row's name"),
              ("pct", "Show each row's share of the total (%)",
               "Add the row's percentage of the display's total after its value"),
              ("party", "Report to party chat when you are in a party",
               "Unticked, Report always goes to your journal"),
              ("scan", "Watch the backpack: items gained, reagents and ammo used",
               "Open your backpack once after logging in so the client knows what is in it"),
              ("travel", "Count tiles walked and recalls / gates",
               "Fill the Travel display: tiles walked, and recalls, gates and teleports"),
              ("recap", "Show a death recap when you die",
               "A window with the last %d seconds of damage you took: who, how much, and "
               "your HP falling" % int(RECAP_SECS)))
    PCT_HINT = ("Pets' and strangers' HP come as a percentage, so their healing is a "
                "\"(%)\" row outside the total.")
    H_FIELDS = 30 + len(FIELDS) * 28 + 4
    H_CHECKS = 30 + len(CHECKS) * 26 + 18 + 4      # + the "(%)" rows hint
    H_TOOLS = 30 + 2 * 28 + 26 + 4                # two rows of buttons, the feed line
    SPOT_ROW = 24

    def spots_height():
        return 30 + 28 + max(1, len(spots)) * SPOT_ROW + 4

    def config_height(w):
        return H_FIELDS + Kit.GAP + H_CHECKS + Kit.GAP + spots_height() + Kit.GAP + H_TOOLS

    def build_config(g, x, y, w):
        store = ({}, {})
        c = {}
        Kit.add_section(g, x, y, w, H_FIELDS, "COUNTING  (fights, healing, rows)")
        lx = x + 12 + max(Kit.text_w(t) for _, t, _, _ in FIELDS) + 10
        for i, (k, text, tip, unit) in enumerate(FIELDS):
            ry = y + 30 + i * 28
            Kit.add_label(g, text, x + 12, ry + 3)
            tb = c[k] = Kit.add_textbox(g, str(settings[k]), lx, ry, 50, numbers=True)
            safe(lambda: tb.SetTooltip("%s (%d-%d)" % ((tip,) + LIMITS[k])))
            Kit.add_label(g, unit, lx + 58, ry + 3, Kit.HUE_INFO)
        y2 = y + H_FIELDS + Kit.GAP
        Kit.add_section(g, x, y2, w, H_CHECKS, "SHOW AND TRACK")
        for i, (k, text, tip) in enumerate(CHECKS):
            c[k] = Kit.add_check(g, text, x + 12, y2 + 30 + i * 26, settings[k], tip)
        Kit.add_label(g, Kit.fit(PCT_HINT, w - 28), x + 12, y2 + 30 + len(CHECKS) * 26 + 2,
                      Kit.HUE_INFO)
        # Gold by place: the spots you named (2.6.05)
        ys = y2 + H_CHECKS + Kit.GAP
        hs = spots_height()
        Kit.add_section(g, x, ys, w, hs, "GOLD BY PLACE  (named spots, per character)")
        Kit.add_label(g, "Name:", x + 12, ys + 33)
        nx = x + 12 + Kit.text_w("Name:") + 8
        c["spot_name"] = Kit.add_textbox(g, "", nx, ys + 30, 140, numbers=False)
        safe(lambda: c["spot_name"].SetTooltip("The new spot's name (up to %d letters)"
                                               % SPOT_NAME_MAX))
        rx = nx + 140 + 12
        Kit.add_label(g, "Radius:", rx, ys + 33)
        rx += Kit.text_w("Radius:") + 8
        c["spot_radius"] = Kit.add_textbox(g, str(page.get("radius", SPOT_RADIUS)), rx,
                                           ys + 30, 44)
        safe(lambda: c["spot_radius"].SetTooltip("Tiles round you that belong to the spot "
                                                 "(%d-%d)" % SPOT_RADIUS_LIMITS))
        rx += 44 + 10
        Kit.add_label(g, "tiles", rx, ys + 33, Kit.HUE_INFO)
        Kit.art_button(g, store, "spot_add", Kit.ART_OK, rx + Kit.text_w("tiles") + 12, ys + 28,
                       "Name this spot", "Name where you stand: gold gained within the radius "
                       "counts for this spot (a known guarded town comes first)")
        if not spots:
            Kit.add_label(g, trunc("No spots yet. Stand where you farm, type a name, then click "
                                   "Name this spot.", w - 28), x + 12, ys + 30 + 28 + 3, Kit.HUE_INFO)
        rm_w = Kit.pic_size(Kit.ART_CLOSE[0])[0] or 30
        c["spot_rm"] = [("spot_rm%d" % i, sp[0]) for i, sp in enumerate(spots)]
        for i, sp in enumerate(spots):
            ry = ys + 30 + 28 + i * SPOT_ROW
            where = "facet %d at %d, %d, %d tiles round" % (sp[3], sp[1], sp[2], sp[4])
            ww_ = Kit.text_w(where)
            Kit.add_label(g, trunc(sp[0], w - 24 - rm_w - 18 - ww_ - 12), x + 12, ry + 3)
            Kit.add_label(g, where, x + w - 12 - rm_w - 12 - ww_, ry + 3, Kit.HUE_INFO)
            Kit.art_button(g, store, "spot_rm%d" % i, Kit.ART_CLOSE, x + w - 12 - rm_w, ry,
                           None, "Remove the spot " + sp[0])
        y3 = ys + hs + Kit.GAP
        Kit.add_section(g, x, y3, w, H_TOOLS, "TOOLS")
        Kit.art_button(g, store, "new", Kit.ART_PAGE, x + 12, y3 + 28, "New meter window",
                       "Open another meter window (up to %d)" % MAX_WINDOWS)
        nx = x + 12 + 35 + Kit.text_w("New meter window") + 20
        Kit.art_button(g, store, "recap", Kit.ART_PAGE, nx, y3 + 28, "Last death recap",
                       "Show the recap of your last death this session again")
        nx += 35 + Kit.text_w("Last death recap") + 20
        Kit.art_button(g, store, "own_size", Kit.ART_CLOSE, nx, y3 + 28, "Reset sizes",
                       "Give every meter window out of a zone its own size again (Rows above, "
                       "%d px wide)" % W)
        Kit.art_button(g, store, "export", Kit.ART_OK, x + 12, y3 + 56, "Export",
                       "Write every display of the first meter window's segment to %s next to "
                       "Virtue Assistant" % EXPORT_FILE.replace("%08X", "<serial>"))
        nx = x + 12 + 35 + Kit.text_w("Export") + 20
        Kit.art_button(g, store, "reset", Kit.ART_CLOSE, nx, y3 + 56, "Reset all meters",
                       "Clear every meter and start a new session")
        c["feed"] = Kit.add_label(g, trunc("Damage numbers: " + feed["kind"], w - 28), x + 12,
                                  y3 + 86, Kit.HUE_INFO)
        page.update({"c": c, "store": store, "unread": False, "next_read": 0.0, "w": w})

    def read_int(ctrl, default, lo, hi):
        txt = str(safe(lambda: ctrl.Text, "") or "").strip()
        try:
            return max(lo, min(hi, int(txt)))
        except ValueError:
            return default

    CONFIG_READ_EVERY = 0.2                  # seconds between reads of the fields and boxes

    def poll_config(force=False):
        c = page["c"]
        if c is None:
            return
        store = page["store"]
        if Kit.was_clicked(store, "reset"):
            queue(("reset",))()
        if Kit.was_clicked(store, "new"):
            queue(("new",))()
        if Kit.was_clicked(store, "own_size"):
            if st["active"]:
                queue(("own_size",))()
            else:                                 # Meters is off: forget the sizes now
                forget_sizes_off()
        off = not st["active"]                    # Meters is off: no tick to do the work
        for key, action in (("export", ("export", 0)), ("recap", ("recap",))):
            if Kit.was_clicked(store, key):
                if off:
                    API.SysMsg("%s: turn Meters on first (the Modules tab)." % TITLE, Kit.HUE_INFO)
                else:
                    queue(action)()
        if Kit.was_clicked(store, "spot_add"):    # the boxes are read only now, at the click
            name = str(safe(lambda: c["spot_name"].Text, "") or "")
            radius = read_int(c["spot_radius"], SPOT_RADIUS, *SPOT_RADIUS_LIMITS)
            page["radius"] = radius               # the box keeps it when the page is redrawn
            if off:                               # where you stand comes from Meters' tick
                API.SysMsg("%s: turn Meters on first to name a spot (the Modules tab)." % TITLE,
                           Kit.HUE_INFO)
            else:
                queue(("spot_add", name, radius))()
        for key, name in c["spot_rm"]:
            if Kit.was_clicked(store, key):
                if off:
                    remove_spot(name)             # needs no tick (saves and redraws the page)
                else:
                    queue(("spot_rm", name))()
        now = time.time()
        if not force and now < page.get("next_read", 0.0):
            page["unread"] = True            # read on the next poll, or as the page closes
            return
        page["next_read"], page["unread"] = now + CONFIG_READ_EVERY, False
        # the damage hook is made on the script's thread after start: show its outcome
        Kit.set_text(c["feed"], trunc("Damage numbers: " + feed["kind"], page.get("w", 600) - 28))
        new = dict(settings)
        for k, _, _, _ in FIELDS:
            new[k] = read_int(c[k], settings[k], *LIMITS[k])
        for k, _, _ in CHECKS:
            new[k] = bool(safe(lambda: c[k].IsChecked, settings[k]))
        if new != settings:
            rebuild = new["rows"] != settings["rows"]
            settings.update(new)
            save_settings()
            del data["hist"][settings["history"]:]
            if rebuild:
                if st["active"]:
                    for w in wins:
                        w["size"] = None          # (2.6.64) the rows set the size again
                        queue(("redraw", w["id"]))()
                else:                             # 2.6.81: Meters off: saved now, or _start
                    forget_sizes_off()            # would load the dragged sizes back
            st["next_ui"] = 0.0

    def config_closed():
        if page.get("unread"):              # the page's last values, however recent
            poll_config(True)
        page["c"] = None


    # ---------- module hooks ----------
    def _start():
        st.update({"shutting": False, "active": True, "queue": [], "last_tick": time.time(),
                   "next_ui": 0.0, "next_friends": 0.0, "next_scan": 0.0, "me": None,
                   "pos": None, "pack": None, "prev": {}, "used": [], "buffq": [],
                   "amtq": [], "place": None, "next_place": 0.0, "taken": [], "hp_log": [],
                   "casts": [], "recap": None, "recap_show": False, "to_write": [],
                   "redraw_wait": set(), "present": [], "pscan": None, "pack_cand": None, "my_ser": None,
                   "my_name": "", "next_name": 0.0, "fnames": None})
        try:
            st["jr"] = Journal.reader()           # the lines from now on, each once
        except Exception:
            st["jr"] = None
        load_settings()
        reset_data()
        load_windows()
        load_spots()
        for w in wins:
            w["shutting"] = False
            w["docked"] = False
            if safe(lambda: HOST.dock_wanted(dock_key(w)), False):
                w["minimized"] = True
        hook_events()
        if feed["handler"] is None:
            # reflection + Expression.Compile take some tens of ms: not on the
            # client thread (_start runs there), but on the script's thread right
            # after this pass; the hook hands its queue over through `feed`
            del jobs[:]
            jobs.append(hook_damage)
        open_all()

    def _thread_tick():
        """Script thread, right after the client tick: one-shot jobs (the damage
        hook) and the files Export made."""
        while jobs and not st["shutting"]:
            job = jobs.pop(0)
            try:
                job()
            except Exception:
                pass
        if st["to_write"]:
            write_files()

    def _thread_wanted():
        """(2.6.82) The script thread's pass is wanted only for a job or an export."""
        return bool(jobs) or bool(st["to_write"])

    def _tick():
        if not wins or wins[0]["g"] is None:
            return
        now = time.time()
        dt = max(0.0, min(1.0, now - st["last_tick"]))
        st["last_tick"] = now
        # buttons and clicks
        for w in list(wins):
            if Kit.was_clicked(w["store"], "close"):
                if w["id"] == 0:
                    Kit.dispose(w["g"])            # on_disposed switches the module off
                    return
                st["queue"].append(("closed", w["id"]))
        while st["queue"]:
            action = st["queue"].pop(0)
            if not do_action(action):
                return
        if st["redraw_wait"] and not drag_busy():   # (2.6.74) the drag is over: drawn now
            ids, st["redraw_wait"] = st["redraw_wait"], set()
            for w in list(wins):
                if w["id"] in ids:
                    build_window(w)
            save_windows()
        # (2.6.64) a corner drag let go, and the window's zone slot
        for w in wins:
            if w["resize_at"] and now - w["resize_at"] >= RESIZE_SETTLE \
                    and not safe(lambda: SNAP.pressed(), False) and not drag_busy():
                w["resize_at"] = 0.0              # (2.6.74) and no window in a drag
                apply_resize(w)
        if now >= st.get("next_zone", 0.0):
            st["next_zone"] = now + ZONE_EVERY
            check_zones()
        # the numbers (client_tick: this runs on the client thread already, so
        # sample() and refresh_all() are called in place - Kit.on_client only
        # ran them in place after a few checks)
        try:
            s = sample()
        except Exception as ex:
            s = None
            msg = str(ex)[:120]
            if msg != st.get("err"):                 # say it once, keep going
                st["err"] = msg
                API.SysMsg("%s: couldn't read the client this time (%s)." % (TITLE, msg), Kit.HUE_BAD)
        read_journal(now)
        if s:
            process(s, now)
        track_place(now, dt)                         # Gold by place: time spent where you are
        if st["recap_show"]:                         # you died: the death recap
            st["recap_show"] = False
            build_recap()
        if data["cur"] is not None:
            data["cur"]["combat"] += dt
            data["overall"]["combat"] += dt
            if not 0.0 <= now - data["last_combat"] <= settings["idle"]:   # (or the clock went back)
                close_fight(now)
                st["next_ui"] = 0.0
        if now >= st["next_ui"]:
            st["next_ui"] = now + UI_EVERY
            refresh_all()

    def do_action(action):
        """One queued click. False when the module must stop this pass."""
        kind = action[0]
        w = win_by_id(action[1]) if len(action) > 1 and isinstance(action[1], int) and \
            kind != "follow" else None
        if kind == "settings":
            HOST.show_settings(KEY)
        elif kind == "follow":
            Follow.toggle(action[1], TITLE)
        elif kind == "new":
            if len(wins) >= MAX_WINDOWS:
                API.SysMsg("%s: %d windows is the most." % (TITLE, MAX_WINDOWS), Kit.HUE_INFO)
                return True
            base = wins[-1]
            g = base["g"]
            bx, by = (g.GetX(), g.GetY()) if Kit.is_open(g) else (base["x"], base["y"])
            nid = max(x["id"] for x in wins) + 1
            used = set(x["metric"] for x in wins)
            metric = next((m for m in ORDER if m not in used), DEFAULT_METRIC)
            nw = new_win(nid, metric, bx + 30, by + 30)
            wins.append(nw)
            build_window(nw)
            dock_win(nw)
            save_windows()
        elif kind == "own_size":                  # (2.6.64) every window its own size again
            for ow in wins:
                had = ow["size"] is not None
                ow["size"] = None
                if had and ow["fit"] is None and Kit.is_open(ow["g"]):
                    build_window(ow)
            save_windows()
        elif kind == "reset":
            reset_data()
            st["next_ui"] = 0.0
            API.SysMsg("%s: every meter cleared; a new session starts now." % TITLE, Kit.HUE_GOOD)
        elif kind == "spot_add":
            add_spot(action[1], action[2])
        elif kind == "spot_rm":
            remove_spot(action[1])
        elif kind == "recap":                     # Settings: show the last recap again
            if st["recap"] is None:
                API.SysMsg("%s: no death this session." % TITLE, Kit.HUE_INFO)
            else:
                build_recap()
        elif kind == "recap_close":
            close_recap()
        elif w is None:
            return True
        elif kind == "graph":                     # the display list: graph on / off
            w["graph"] = not w.get("graph")
            build_window(w)
            dock_win(w)                           # its hooks follow the graph (scale or not)
            if Kit.is_open(w["picker"]):
                build_picker(w)
            save_windows()
        elif kind == "export":
            export(w)
        elif kind == "closed":
            st["redraw_wait"].discard(w["id"])    # (2.6.74) gone: no redraw waits for it
            close_window(w, True)
            save_windows()
        elif kind == "toggle_min":
            w["minimized"] = not w["minimized"]
            w["docked"] = False
            HOST.dock_forget(dock_key(w))
            build_window(w)
            save_windows()
        elif kind == "to_bar":
            HOST.dock_to_bar(dock_key(w), win_title(w))
        elif kind == "redraw":
            if drag_busy():
                # (2.6.74) a zone's fit ("again" too) or a fold under a drag: a window
                # made anew under the mouse is a new gump, so the drop of the old one
                # was lost; drawn once the drag is over (see _tick)
                st["redraw_wait"].add(w["id"])
                return True
            st["redraw_wait"].discard(w["id"])
            build_window(w)
            save_windows()
        elif kind == "step":
            i = ORDER.index(w["metric"]) if w["metric"] in ORDER else 0
            w["metric"] = ORDER[(i + action[2]) % len(ORDER)]
            build_window(w)
            if Kit.is_open(w["picker"]):
                build_picker(w)
            save_windows()
        elif kind in ("picker", "segpick"):
            if Kit.is_open(w[kind]):
                Kit.dispose(w[kind])
            else:
                (build_picker if kind == "picker" else build_segpick)(w)
        elif kind == "metric":
            w["metric"] = action[2]
            Kit.dispose(w["picker"])
            build_window(w)
            save_windows()
        elif kind == "seg":
            w["seg"] = action[2]
            Kit.dispose(w["segpick"])
            refresh_window(w)
            save_windows()
        elif kind == "close_sub":
            Kit.dispose(w.get(action[2]))
        elif kind == "detail":
            slots = w["slots"]
            i = action[2]
            key = slots[i].get("key") if i < len(slots) else None
            if key is None or w["metric"] in ("session", "big", "gold"):
                return True
            w["detail_row"], w["detail_metric"] = key, w["metric"]
            if Kit.is_open(w["detail"]):
                refresh_detail(w)
            else:
                build_detail(w)
        elif kind == "report":
            report(w)
        return True

    def _stop():
        st["shutting"] = True
        st["active"] = False
        st["jr"] = None
        del jobs[:]
        save_windows()
        save_settings()
        unhook_damage()
        close_recap()
        for w in list(wins):
            close_window(w, False)


    load_settings()
    load_spots()                          # the settings page lists them while Meters is off too
    reset_data()
    # The tick never waits (no pauses, cursors, server replies or file writes),
    # so it runs on the client thread with the others: every read in place.
    # 2.6.82: speed pass: friends polled only when near, the backpack look spread
    # over ticks, running totals, unchanged views not worked out again, the
    # mother's shared per-pass reads, the thread pass only when work waits.
    MODULE = {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True,
              "thread_tick": _thread_tick,  # the damage hook's one-off build (reflection)
              "thread_wanted": _thread_wanted,
              "config_height": config_height, "build_config": build_config,
              "poll_config": poll_config, "config_closed": config_closed}
    # ============================= MODULE END ====================================
    return MODULE


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("meters", "Meters", "Damage, healing, loot and gold meters, per fight or session",
             _module_meters, 0.25,
             category="Extras")
else:
    import API
    API.SysMsg("Meters is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
