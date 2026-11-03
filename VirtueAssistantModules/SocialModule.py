# =============================================================================
#  Social  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by Virtue Assistant from LegionScripts/VirtueAssistantModules.
#  Virtue Assistant provides everything this file uses (API, G, safe, Client,
#  Kit, Follow, HOST, the main loop and the settings window), so run that
#  instead and tick Social on its Modules tab.
#
#  To leave this module out, take this file out of the folder.
#  Module key: "social"
#
#  One window for everything social: TazUO's friends list, your party, your
#  guild (its info, roster and diplomacy) and your own character profile, on
#  four tabs. The Action Bar lists it under "Module windows" (right-click a
#  window button), so one bar button shows it, folds it away and brings it
#  back.
# =============================================================================


def _module_social():
    """Builds the module in its own namespace and returns its hooks."""
    # ============================ MODULE START ===================================
    #  MODULE: Social  -  friends, party, guild and profile in one window
    #
    #  FRIENDS: TazUO's own friends list (the one its nameplates, GetAllMobiles
    #    and the Legion API use), with each friend's health when in view. Add
    #    by target, remove with the X; click a row to target, Alt+click to
    #    auto-follow. Says so in the journal when a friend comes into view.
    #  PARTY: members with health, invite (target), leave, loot on/off, the
    #    client's party window, accept / decline an invite, party chat.
    #  GUILD: what the server's guild window shows, read into this window:
    #    the "My Guild" page (guild name, alliance, faction, charter, website)
    #    and the whole "Guild Roster" (every member with rank, last on / online
    #    and guild title, all its pages), plus your own guild line from your
    #    tooltip. Members in view get a health bar and distance; allies in view
    #    that aren't on the roster are listed after it. The guild window is
    #    opened hidden for the read (2.6.0) and closed again; Refresh re-reads
    #    it, and it is re-read on its own every few minutes while the tab
    #    shows (settings). Buttons for the guild window itself, its Diplomacy
    #    page, guild and alliance chat.
    #  PROFILE: your name and titles, notoriety, gold, followers, weight; edit
    #    your profile (the server's profile scroll), paperdoll, status, the
    #    ignore list.
    #  NOTES (2.6.05): Shift+click a row to write a note on that player (by
    #    name, kept for the whole account). The note shows in the row's
    #    tooltip, and in Ultima Tracker's through HOST.services["social.note"].
    #  ROSTER SORT (2.6.05): the Guild tab's Sort button orders the roster by
    #    online first (members in view first), last on, rank or name.
    #
    #  Speed: ticks on the client thread (client_tick), draws into a pool of
    #  rows and writes a label only when it changed. The jobs that wait (the
    #  guild window reads, the Diplomacy page) run on the script's thread
    #  (thread_tick).
    #  2.6.82: speed pass: the shared per-pass mobile / player reads, no unused
    #  notoriety reads, the roster's order and info lines kept until they change,
    #  one client hop per guild-window poll, each gump layout parsed once.
    # =============================================================================
    KEY = "social"
    TITLE = "Social"

    # ------------------------------- CONFIG --------------------------------------
    SETTINGS_KEY = "Social_settings"      # per character
    POS_KEY = "Social_pos"
    MIN_KEY = "Social_min"                # minimized when you left (kept for the next start)
    NAMES_KEY = "Social_names"            # friend serial -> name, as last seen (fallback)
    GUILD_KEY = "Social_guild"            # the My Guild page as last read (shown until re-read)
    ROSTER_KEY = "Social_roster"          # the roster as last read
    TRAY_ICON = 0x1F14                    # item art on the Action Bar's tray button
    W = 460                               # full window width (Friends, Party, Profile)
    GUILD_W = 600                         # the Guild tab is wider: five roster columns
    MINI_W, MINI_H = 240, 46              # minimized bar
    ROW_H = 24                            # one list row
    ROWS_MIN, ROWS_MAX = 4, 16            # rows per page (settings)
    DEFAULT_ROWS = 8
    TABS = [("friends", "Friends"), ("party", "Party"), ("guild", "Guild"),
            ("profile", "Profile")]
    TAB_TIPS = {"friends": "Show TazUO's friends list, with each friend's health when in view",
                "party": "Show your party: its members, invites, loot rights and party chat",
                "guild": "Show your guild: its info, the whole roster and guild chat",
                "profile": "Show your character: name, titles, gold, weight and the client's windows"}
    LIST_EVERY = 0.5                      # seconds between looks at the mobiles in view
    FRIENDS_EVERY = 2.0                   # seconds between reads of the friends list
    PROFILE_EVERY = 1.0                   # seconds between reads of your own tooltip
    PICK_TIMEOUT = 15                     # seconds to target a friend
    GUMP_WAIT = 4.0                       # seconds to wait for the guild window
    DIPLOMACY_LABEL = "Diplomacy"         # text of the guild window's diplomacy button
    DIPLOMACY_BUTTON = 3                  # its button id, if the label can't be found
    #                                       (ServUO's guild window: My Guild 1, Guild
    #                                       Roster 2, Diplomacy 3; 0 = label only).
    #                                       The default of the settings page's field.
    DIPLOMACY_BUTTON_MAX = 9999           # the field's upper bound
    NAME_W = 150                          # a row's name column
    STATUS_W = 90                         # a row's status column ("12 tiles", "away")
    RANK_W = 64                           # the roster's rank column ("Emissary" is ~55 px)
    MSG_W_MIN = 120                       # shortest chat field
    DUMP_CHARS = 200                      # of an unrecognised gump's layout put in the journal
    # The guild window (ServUO's "new guild system" gump, as In Mani Ylem sends it):
    INFO_TAB, ROSTER_TAB = "My Guild", "Guild Roster"    # the tab captions (clilocs below)
    INFO_BUTTON, ROSTER_BUTTON = 1, 2     # the tab buttons' ids (fallback for the captions)
    FORWARD_BUTTON = 7                    # the roster's "next page" reply button (8 a page)
    ROSTER_PAGES_MAX = 40                 # pages read at most (320 members)
    ROSTER_KEEP = 300                     # members kept in the saved copy
    GUILD_EVERY_MIN = 5                   # default: re-read every 5 minutes while the tab shows
    GUILD_EVERY_MAX = 120                 # the settings field's upper bound (minutes)
    GUILD_RETRY = 60                      # seconds before another automatic try after a failure
    GUILD_RETRY_MAX = 600                 # ... doubling with every failure in a row, up to this
    # The create-a-guild window comes instead when you're in no guild:
    NOT_GUILDED_CLILOCS = (1062939, 1062940, 1063035)   # GUILD MENU, "not a member of any
    NOT_GUILDED = ("not a member of any guild", "abbreviation:")   # guild...", Abbreviation:
    # Cliloc texts the guild window uses, so they read right even without
    # API.GetClilocString (which is tried first for any other number):
    CLILOCS = {1062954: "Guild Name", 1063025: "Alliance", 1063084: "Guild Faction",
               1062955: "Name", 1062956: "Rank", 1062952: "Last On",
               1062953: "Guild Title", 1063015: "Online", 1062959: "Leader",
               1062960: "Warlord", 1062961: "Emissary", 1062962: "Member",
               1062963: "Ronin", 1062974: ROSTER_TAB, 1063014: INFO_TAB,
               1062978: DIPLOMACY_LABEL, 1062992: "Invite Player", 3006115: "Resign"}
    TAB_CLILOCS = (1063014, 1062974, 1062978)
    # (2.6.82) a layout without one of these can't be a guild window page (the
    # tab clilocs as written in it, or the roster caption as text): not parsed
    TAB_MARKS = ("1063014", "1062974", "1062978")
    # the tab captions as roster cells read them (left out of the roster rows)
    TAB_CAPS_LOW = (INFO_TAB.lower(), ROSTER_TAB.lower(), DIPLOMACY_LABEL.lower())
    # notoriety numbers -> names (2.6.82: one table, not a dict built per call)
    NOTO_NAMES = ("Unknown", "Innocent", "Ally", "Gray", "Criminal", "Enemy", "Murderer",
                  "Invulnerable")
    # The saved copy of the guild window. 2.6.0 wrote it with the control
    # characters FS / RS between fields / records; since 2.6.01 it is written
    # with printable separators (PF / PR) and an escape (ESC), which any store
    # carries unchanged. Both forms are read.
    FS, RS = "\x1f", "\x1e"               # field / record separators of the 2.6.0 saved copy
    PF, PR, ESC = "|", ";", "~"           # the printable ones (ESC escapes all three)
    # Notes on players (2.6.05): saved per ACCOUNT (every character of it sees
    # them), in the printable form above: name|note;name|note
    NOTES_KEY = "Social_notes"
    NOTES_MAX = 500                       # notes kept at most
    NOTE_CHARS = 200                      # the longest note
    NOTE_POS_KEY = "Social_note_pos"      # where the note window sits
    NOTE_W = 440                          # the note window's width
    # Roster sorting (2.6.05): the Guild tab's Sort button, remembered.
    SORTS = [("online", "Sort: online", "Online"), ("laston", "Sort: last on", "Last on"),
             ("rank", "Sort: rank", "Rank"), ("name", "Sort: name", "Name")]
    SORT_CODES = [x[0] for x in SORTS]
    # the ranks, top first (each with the other spellings it may come as: the
    # roster's rank cliloc 1062959 reads "Guild Leader" in Cliloc.enu, "Leader"
    # through CLILOCS above); a rank not listed sorts after these
    RANK_ORDER = (("leader", "guild leader"), ("warlord",), ("emissary",), ("member",),
                  ("ronin",))
    # The roster's "Last On" is read as a date: year first (2026-10-31, the
    # ServUO form), else day / month by which part can't be a month, else
    # month first for "/" and day first for "." (unchecked in game).
    DATE_RE = re.compile(r"(\d{1,4})\s*([-/.])\s*(\d{1,2})\s*[-/.]\s*(\d{1,4})")
    # -----------------------------------------------------------------------------

    settings = {"tab": "friends", "rows": DEFAULT_ROWS, "bars": True, "announce": True,
                "gevery": GUILD_EVERY_MIN, "ghide": True,
                "dbutton": DIPLOMACY_BUTTON,     # 2.6.01: the Diplomacy button id (settings)
                "left": False,                   # 2.6.01: also say when a friend leaves view
                "gsort": "online"}               # 2.6.05: how the guild roster is sorted
    st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
          "page": {}, "rebuild": False,
          "friends": [],            # [(serial, name)] from the client
          "names": {},              # serial -> name last seen (saved)
          "names_dirty": False,
          "seen": None,             # friend serials in view (None until the first look)
          "next_list": 0.0, "next_friends": 0.0, "next_profile": 0.0,
          "mobs": {},               # serial -> row data read this pass (the rows shown only)
          "inview": set(),          # friend serials in view this pass (presence only)
          "party": None,            # (leader, inviter, canloot, [serials]) or None
          "profile": None,          # (name, lines, noto, gold, followers, fmax, weight, wmax, war, hidden)
          "msg": {},                # the last text typed in a chat field, per tab
          "guild": None,            # the guild window as last read (see empty_guild)
          "guild_busy": False,      # a read is running on the script's thread
          "guild_dirty": False,     # a read finished: redraw
          "guild_next": 0.0,        # earliest time of the next automatic read
          "guild_fails": 0,         # automatic reads failed in a row (the retry delay doubles)
          "guild_said": "",         # the last failure note printed (printed once until it changes)
          "guild_pages": 0,         # roster pages read so far by the running read
          "gids": {},               # the guild window's gump ids once seen ("info", "roster")
          "ghid": 0,                # the gump we opened hidden, if any (closed whatever happens)
          "hid_any": False,         # the next gump was hidden with no serial: whatever came is hidden
          "view": {},               # lower-case name -> serial of every mobile in view
          "view_serials": None,     # the serials in view, when scan_view ran this pass (else None)
          "allies": [],             # [(serial, name)] of Ally mobiles in view
          # (2.6.82) speed caches
          "me_s": 0,                # your serial (read once a start, again while 0)
          "fserials": [],           # the friends' serials, in st["friends"] order
          "friends_raw": None,      # the client's list as last read (unchanged: no rebuild)
          "kept": {},               # serial -> (name, distance) of the players scan_view kept
          "prof_part": False,       # st["profile"] holds only the name and lines (Guild tab)
          "again_for": None,        # the slot an "again" redraw was last done for
          "again_build": False}     # the build running is that redraw
    win = {"g": None, "c": {}, "store": ({}, {}), "rows": [], "tab": None, "info": {}}
    page = {"c": None, "store": ({}, {})}      # this module's page of the Settings tab
    jobs = []                                  # work that waits: run by _thread_tick
    NOTES = {}                                 # lower-case name -> (name as written, note)
    notes_st = {"dirty": False, "ver": 0}      # ver: bumped when NOTES change (row tooltips)
    # the note window (2.6.05): one at a time
    ed = {"g": None, "c": {}, "store": ({}, {}), "name": ""}


    # ---------- saved settings ----------
    def load_settings():
        p = Kit.get_var(SETTINGS_KEY).split("|")
        if len(p) >= 4:
            if p[0] in dict(TABS):
                settings["tab"] = p[0]
            try:
                settings["rows"] = max(ROWS_MIN, min(ROWS_MAX, int(p[1])))
            except Exception:
                settings["rows"] = DEFAULT_ROWS
            settings["bars"] = p[2] == "1"
            settings["announce"] = p[3] == "1"
        if len(p) >= 6:                                   # 2.6.0 guild keys, after the old four
            try:
                settings["gevery"] = max(0, min(GUILD_EVERY_MAX, int(p[4])))
            except Exception:
                settings["gevery"] = GUILD_EVERY_MIN
            settings["ghide"] = p[5] == "1"
        if len(p) >= 8:                                   # 2.6.01 keys, after those
            try:
                settings["dbutton"] = max(0, min(DIPLOMACY_BUTTON_MAX, int(p[6])))
            except Exception:
                settings["dbutton"] = DIPLOMACY_BUTTON
            settings["left"] = p[7] == "1"
        if len(p) >= 9 and p[8] in SORT_CODES:            # 2.6.05, after those (2.6.04 reads 8)
            settings["gsort"] = p[8]
        names = {}
        for part in Kit.get_var(NAMES_KEY).split("|"):
            if "=" in part:
                s, n = part.split("=", 1)
                try:
                    names[int(s)] = n
                except Exception:
                    pass
        st["names"] = names
        load_guild()
        load_notes()


    def save_settings():
        Kit.put_var(SETTINGS_KEY, "|".join([settings["tab"], str(settings["rows"]),
                                            "1" if settings["bars"] else "0",
                                            "1" if settings["announce"] else "0",
                                            str(settings["gevery"]),
                                            "1" if settings["ghide"] else "0",
                                            str(settings["dbutton"]),
                                            "1" if settings["left"] else "0",
                                            settings["gsort"]]))


    def save_names():
        if not st["names_dirty"]:
            return
        st["names_dirty"] = False
        items = sorted(st["names"].items())[-200:]          # a cap, oldest serials dropped
        Kit.put_var(NAMES_KEY, "|".join("%d=%s" % (s, n.replace("|", "/").replace("=", "-"))
                                        for s, n in items))


    def empty_guild():
        return {"ok": False, "in_guild": True, "name": "", "alliance": "", "faction": "",
                "charter": "", "website": "", "members": [], "at": 0.0, "note": ""}


    def clean(s):
        """A field of the saved copy: control characters out, the printable
        separators escaped (ESC+t for ESC, ESC+p for PF, ESC+s for PR)."""
        s = str(s or "").replace(FS, " ").replace(RS, " ").replace("\n", " ").strip()
        return s.replace(ESC, ESC + "t").replace(PF, ESC + "p").replace(PR, ESC + "s")


    def unclean(s):
        """The escaping of clean() undone (every ESC in an escaped text starts
        an escape, so the order of these replacements is safe)."""
        return str(s or "").replace(ESC + "p", PF).replace(ESC + "s", PR).replace(ESC + "t", ESC)


    def split_saved(raw, old_sep, new_sep):
        """The fields of a saved record: the 2.6.0 form's when it holds the
        control separators (as saved), else the printable form's, unescaped."""
        if FS in raw or RS in raw:
            return raw.split(old_sep)
        return [unclean(p) for p in raw.split(new_sep)]


    def load_guild():
        """The guild window as last read, saved per character (shown until re-read)."""
        gd = empty_guild()
        head = split_saved(Kit.get_var(GUILD_KEY), FS, PF)
        if len(head) >= 7:
            gd["name"], gd["alliance"], gd["faction"], gd["charter"], gd["website"] = head[:5]
            try:
                gd["at"] = float(head[5])
            except Exception:
                gd["at"] = 0.0
            gd["in_guild"] = head[6] != "0"
            gd["ok"] = gd["at"] > 0
        members = []
        raw = Kit.get_var(ROSTER_KEY)
        old_form = FS in raw or RS in raw
        for rec in raw.split(RS if old_form else PR):
            f = rec.split(FS) if old_form else [unclean(p) for p in rec.split(PF)]
            if len(f) >= 5 and f[0]:
                members.append({"name": f[0], "rank": f[1], "laston": f[2], "title": f[3],
                                "online": f[4] == "1", "me": False})
        gd["members"] = members
        st["guild"] = gd


    def save_guild():
        """Off the client thread (persistent vars don't touch it). Written in
        the printable form (see PF / PR above)."""
        gd = st["guild"] or empty_guild()
        Kit.put_var(GUILD_KEY, PF.join([clean(gd["name"]), clean(gd["alliance"]),
                                        clean(gd["faction"]), clean(gd["charter"]),
                                        clean(gd["website"]), "%d" % int(gd["at"] or 0),
                                        "1" if gd["in_guild"] else "0"]))
        Kit.put_var(ROSTER_KEY, PR.join(PF.join([clean(m["name"]), clean(m["rank"]),
                                                 clean(m["laston"]), clean(m["title"]),
                                                 "1" if m["online"] else "0"])
                                        for m in gd["members"][:ROSTER_KEEP]))


    # ---------- notes on players (2.6.05): per account ----------
    def load_notes():
        try:
            raw = str(API.GetPersistentVar(NOTES_KEY, "", API.PersistentVar.Account) or "")
        except Exception:
            raw = ""
        NOTES.clear()
        notes_st["ver"] += 1
        for rec in raw.split(PR):
            f = [unclean(x) for x in rec.split(PF)]
            if len(f) >= 2 and f[0].strip() and f[1].strip() and len(NOTES) < NOTES_MAX:
                NOTES[f[0].strip().lower()] = (f[0].strip(), f[1].strip())

    def save_notes():
        """Off the client thread (a job), and from stop()."""
        if not notes_st["dirty"]:
            return
        notes_st["dirty"] = False
        data = PR.join(PF.join([clean(n), clean(t)])
                       for n, t in sorted(NOTES.values(), key=lambda e: e[0].lower()))
        try:
            API.SavePersistentVar(NOTES_KEY, data, API.PersistentVar.Account)
        except Exception:
            pass

    def note_of(player_name):
        """HOST.services["social.note"]: the note on that player ("" if none);
        the name is matched without regard to case."""
        try:
            e = NOTES.get(str(player_name or "").strip().lower())
        except Exception:
            return ""
        return e[1] if e else ""

    def set_note(name, text):
        """Write (or, with an empty text, delete) the note on `name`."""
        name = " ".join(str(name or "").split())
        text = " ".join(str(text or "").split())[:NOTE_CHARS]
        if not name:
            API.SysMsg("Social: type the player's name first.", Kit.HUE_INFO)
            return False
        k = name.lower()
        if not text:
            if NOTES.pop(k, None) is not None:
                API.SysMsg("Social: note on %s deleted." % name, Kit.HUE_INFO)
                notes_st["dirty"] = True
                notes_st["ver"] += 1
                jobs.append(save_notes)           # a write: off the client thread
            return True
        if k not in NOTES and len(NOTES) >= NOTES_MAX:
            API.SysMsg("Social: at most %d notes; delete one first." % NOTES_MAX, Kit.HUE_BAD)
            return False
        NOTES[k] = (name, text)
        notes_st["dirty"] = True
        notes_st["ver"] += 1
        jobs.append(save_notes)
        API.SysMsg("Social: note on %s saved." % name, Kit.HUE_GOOD)
        return True

    # ---------- small helpers ----------
    fit = Kit.fit                         # text cut to a width (letter sums: no label per step)


    def shift_held():
        """Shift down? (read inside a click handler, as Follow.alt_held)."""
        v = Client.key_held("shift")
        if v is not None:
            return bool(v)
        try:
            from ClassicUO.Input import Keyboard
            return bool(Keyboard.Shift)
        except Exception:
            pass
        return bool(safe(lambda: API.IsKeyPressed("SHIFT"), False))


    def set_vis(part, on):
        """IsVisible written only on change (parts are [ctrl, visible] pairs)."""
        if part[0] is not None and part[1] != on:
            part[1] = on
            try:
                part[0].IsVisible = on
            except Exception:
                pass


    def noto_name(n):
        if n is None:
            return ""
        try:
            i = int(n)
        except Exception:
            return str(n).split(".")[-1]
        if 0 <= i < 8:
            return NOTO_NAMES[i]
        return str(n).split(".")[-1]       # (only for a number past the table)


    def player_serial():
        """Your serial: read once a start (2.6.82; a character switch restarts
        the modules), again while it is 0 (not logged in yet)."""
        s = st["me_s"]
        if not s:
            try:
                s = int(API.Player.Serial or 0)
            except Exception:
                s = 0
            st["me_s"] = s
        return s


    def player_name():
        prof = st["profile"]
        if prof and prof[0]:
            return prof[0]
        try:
            return str(API.Player.Name or "")
        except Exception:
            return ""


    def ago(t):
        """'just now', '3 min ago', '2 h ago', '4 days ago' for a time.time() value."""
        if not t:
            return "never"
        d = max(0, int(time.time() - t))
        if d < 60:
            return "just now"
        if d < 3600:
            return "%d min ago" % (d // 60)
        if d < 86400:
            return "%d h ago" % (d // 3600)
        return "%d day%s ago" % (d // 86400, "" if d // 86400 == 1 else "s")


    # ---------- the client (reflection; every call runs on the client thread) ----------
    class CL(object):
        """What the Legion API doesn't give a script: the client's World (its
        Party), TazUO's FriendsListManager (friends' names), GameActions
        (guild window, profile, party requests) and UIManager (ignore list).
        Each lookup is done once; a missing piece leaves `error` set."""
        looked = False
        error = ""
        world = None
        GA = None
        UIM = None
        FLM = None            # FriendsListManager type
        _acc = {}

        @staticmethod
        def _flags(static):
            from System.Reflection import BindingFlags
            return (BindingFlags.Public | BindingFlags.NonPublic |
                    (BindingFlags.Static if static else BindingFlags.Instance))

        @staticmethod
        def get(obj, name, t=None):
            """A property or field, private ones too (obj None: static on t)."""
            static = obj is None
            t = t if t is not None else obj.GetType()
            key = (t, name, static)
            acc = CL._acc.get(key, False)
            if acc is False:
                acc = None
                flags = CL._flags(static)
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
                CL._acc[key] = acc
            if acc is None:
                return None
            return acc[0].GetValue(obj, None) if acc[1] else acc[0].GetValue(obj)

        @staticmethod
        def set(obj, name, value):
            """(2.6.81) The twin of get: write a property or field, private ones too
            (same lookup, kept in the same cache). False when it can't be."""
            if obj is None:
                return False
            CL.get(obj, name)                      # finds (and caches) the accessor
            acc = CL._acc.get((obj.GetType(), name, False))
            if not acc:
                return False
            if acc[1]:
                acc[0].SetValue(obj, value, None)
            else:
                acc[0].SetValue(obj, value)
            return True

        _methods = {}

        @staticmethod
        def call(obj, name, args=(), t=None):
            """Call a method by name (obj None: static on t), private ones too;
            parameters past the given args must be optional and get their
            defaults. Raises when there is no such method."""
            t = t if t is not None else obj.GetType()
            args = list(args)
            key = (t, name, len(args), obj is None)
            e = CL._methods.get(key, False)
            if e is False:
                m = None
                flags = CL._flags(obj is None)
                tt = t
                while tt is not None and m is None:
                    for mm in tt.GetMethods(flags):
                        if mm.Name != name or mm.IsGenericMethodDefinition:
                            continue
                        ps = mm.GetParameters()
                        if len(ps) >= len(args) and all(p.IsOptional for p in ps[len(args):]):
                            m = mm
                            break
                    tt = tt.BaseType
                # (2.6.82) the method and its defaults' tail kept together: no
                # GetParameters (a reflection array) on every call
                e = None if m is None else (m, [p.DefaultValue for p in m.GetParameters()[len(args):]])
                CL._methods[key] = e
            if e is None:
                raise Exception("can't call %s.%s" % (t.Name, name))
            arr = CL._sys_array()
            return e[0].Invoke(obj, arr(args + e[1]))

        _arr = []

        @staticmethod
        def _sys_array():
            """System.Array[object], looked up once."""
            if not CL._arr:
                import System
                CL._arr.append(System.Array[object])
            return CL._arr[0]

        @staticmethod
        def find():
            if CL.looked:
                return
            CL.looked = True
            try:
                asm = API.GetType().Assembly
            except Exception as ex:
                CL.error = "no client access (%s)" % ex
                return
            world = safe(lambda: CL.get(API, "World"))
            if world is None:
                ct = Client._type("ClassicUO.Client")
                game = safe(lambda: CL.get(None, "Game", ct)) if ct is not None else None
                uo = safe(lambda: CL.get(game, "UO")) if game is not None else None
                world = safe(lambda: CL.get(uo, "World")) if uo is not None else None
            CL.world = world
            CL.GA = Client._type("ClassicUO.Game.GameActions")
            CL.UIM = Client._type("ClassicUO.Game.Managers.UIManager")
            CL.FLM = Client._type("ClassicUO.Game.Managers.FriendsListManager")
            if world is None:
                CL.error = "client World not found"
            elif CL.GA is None:
                CL.error = "GameActions not found"

        @staticmethod
        def on_main(fn):
            """fn() in one hop on the client thread (in place when already there)."""
            how, value = Client.on_main_ex(fn)
            if how == "ok":
                return value
            CL.error = Client.error or "can't run on the client thread"
            return None

        _ga_methods = {}      # (name, argument count, with_world) -> MethodInfo, looked up once

        @staticmethod
        def game_action(name, args=(), with_world=True):
            """GameActions.<name>(world, *args) - or (*args) when the method
            takes no World - on the client thread. False when it can't be."""
            CL.find()
            if CL.GA is None:
                return False
            world = CL.world

            def run():
                import System
                full = ([world] if with_world else []) + list(args)
                key = (name, len(full), with_world)
                m = CL._ga_methods.get(key, False)
                if m is False:                         # the scan of GetMethods, once per key
                    m = None
                    for mm in CL.GA.GetMethods(CL._flags(True)):
                        if mm.Name != name or mm.IsGenericMethodDefinition:
                            continue
                        ps = mm.GetParameters()
                        if len(ps) < len(full) or not all(p.IsOptional for p in ps[len(full):]):
                            continue
                        if with_world and (len(ps) == 0 or ps[0].ParameterType.Name != "World"):
                            continue
                        if not with_world and len(ps) and ps[0].ParameterType.Name == "World":
                            continue
                        m = mm
                        break
                    CL._ga_methods[key] = m
                if m is None:
                    raise Exception("GameActions.%s not found" % name)
                ps = m.GetParameters()
                m.Invoke(None, System.Array[object](full + [p.DefaultValue for p in ps[len(full):]]))
                return True
            return bool(CL.on_main(run))

        @staticmethod
        def friends():
            """[(serial, name)] from TazUO's FriendsListManager; None if it
            can't be read (the API's serial list is used instead)."""
            CL.find()
            if CL.FLM is None:
                return None

            def run():
                inst = CL.get(None, "Instance", CL.FLM)
                if inst is None:
                    return None
                out = []
                for f in (CL.call(inst, "GetFriends") or []):
                    ft = f.GetType()                 # (2.6.82) once per friend, not per field
                    out.append((int(CL.get(f, "Serial", ft) or 0), str(CL.get(f, "Name", ft) or "")))
                return out
            return CL.on_main(run)

        @staticmethod
        def party():
            """(leader, inviter, canloot, [member serials]) from World.Party, or None."""
            CL.find()
            world = CL.world
            if world is None:
                return None

            def run():
                party = CL.get(world, "Party")
                if party is None:
                    return None
                leader = int(CL.get(party, "Leader") or 0)
                inviter = int(CL.get(party, "Inviter") or 0)
                loot = bool(CL.get(party, "CanLoot") or False)
                # 2.6.81: World.Party.Members holds you too; leave yourself out, as the
                # API's list does, so "party of N" (len + 1) is right on both paths
                pl = CL.get(world, "Player")
                me = int(CL.get(pl, "Serial") or 0) if pl is not None else 0
                members = []
                for m in (CL.get(party, "Members") or []):
                    if m is not None:
                        s = int(CL.get(m, "Serial") or 0)
                        if s and s != me:
                            members.append(s)
                return (leader, inviter, loot, members)
            return CL.on_main(run)

        @staticmethod
        def open_ignore_list():
            """UIManager.Add(new IgnoreManagerGump(world)); an open one comes forward."""
            CL.find()
            if CL.world is None or CL.UIM is None:
                return False

            def run():
                import System
                if CL.bring_to_front("IgnoreManagerGump"):
                    return True
                t = Client._type("ClassicUO.Game.UI.Gumps.IgnoreManagerGump")
                if t is None:
                    raise Exception("IgnoreManagerGump not found")
                g = System.Activator.CreateInstance(t, System.Array[object]([CL.world]))
                CL.call(None, "Add", [g], CL.UIM)
                return True
            return bool(CL.on_main(run))

        @staticmethod
        def bring_to_front(type_name):
            gumps = CL.get(None, "Gumps", CL.UIM) if CL.UIM is not None else None
            node = gumps.First if gumps is not None else None
            while node is not None:
                g = node.Value
                if g is not None and g.GetType().Name == type_name and not g.IsDisposed:
                    safe(lambda: CL.call(g, "BringOnTop"))
                    return True
                node = node.Next
            return False

        @staticmethod
        def find_server_gump(test):
            """(server serial, PacketGumpText) of the open server gump whose
            layout passes test(raw), wherever it sits in UIManager.Gumps (the
            API's HasGump only knows the LAST one); (0, "") when none."""
            CL.find()
            if CL.UIM is None:
                return 0, ""

            def run():
                gumps = CL.get(None, "Gumps", CL.UIM)
                node = gumps.First if gumps is not None else None
                while node is not None:
                    g = node.Value
                    node = node.Next
                    if g is None or g.IsDisposed:
                        continue
                    try:
                        raw = CL.get(g, "PacketGumpText")
                        if not raw:
                            continue
                        raw = str(raw)
                        if test(raw):
                            return int(CL.get(g, "ServerSerial") or 0), raw
                    except Exception:
                        continue
                return 0, ""
            r = CL.on_main(run)
            return r if r else (0, "")

        @staticmethod
        def inner(gump):
            """The client's Gump behind an API gump wrapper (API.GetGump gives
            an ApiUiBaseGump whose Gump property is the real one)."""
            g = safe(lambda: gump.Gump)
            return g if g is not None else gump

        @staticmethod
        def press_labelled(gump, label):
            """In a server gump, press the Button nearest the text `label`
            (its ButtonID through the gump's OnButtonClick): a text that IS
            the label (case-insensitive) first, else the first that contains
            it (a charter mentioning "guild roster" must not steal the match).
            False if there is no such text or button."""
            gump = CL.inner(gump)
            want = label.lower().strip()

            def run():
                import System
                exact, texts, buttons = [], [], []

                def walk(ctrl):
                    try:                             # (2.6.82) try blocks, no lambda per control
                        kids = list(CL.get(ctrl, "Children") or [])
                    except Exception:
                        kids = []
                    for ch in kids:
                        if ch is None:
                            continue
                        tn = ch.GetType().Name
                        if tn == "Button":
                            buttons.append((int(CL.get(ch, "ScreenCoordinateX") or 0),
                                            int(CL.get(ch, "ScreenCoordinateY") or 0),
                                            int(CL.get(ch, "ButtonID") or 0)))
                        else:
                            try:
                                txt = CL.get(ch, "Text")
                            except Exception:
                                txt = None
                            low = Kit.strip_html(txt).lower() if txt else ""
                            if low and want in low:
                                at = (int(CL.get(ch, "ScreenCoordinateX") or 0),
                                      int(CL.get(ch, "ScreenCoordinateY") or 0))
                                (exact if low == want else texts).append(at)
                        walk(ch)
                walk(gump)
                texts = exact or texts
                if not texts or not buttons:
                    return False
                tx, ty = texts[0]
                best = min(buttons, key=lambda b: abs(b[0] - tx) + abs(b[1] - ty))
                if abs(best[0] - tx) + abs(best[1] - ty) > 80:
                    return False
                CL.call(gump, "OnButtonClick", [System.Int32(best[2])])
                return True
            return bool(CL.on_main(run))


    # ---------- reading the world (on the client thread, in place) ----------
    # (2.6.82) Mobiles and the player come through the mother's per-pass reads
    # (HOST.mobile / HOST.mobiles / HOST.me): within one client pass a mobile
    # another module (or scan_view) already looked at costs nothing again.
    def read_mobile(serial):
        """Row data of a mobile in view: (name, hits, hmax, dist, dead, True) or
        None. (2.6.82: the notoriety was read here and never used; the last
        slot now says the row data is whole, see part_mobile.)"""
        try:
            m = HOST.mobile(serial)
        except Exception:
            m = None
        if m is None:
            return None
        try:
            name = str(m.Name or "")
            hits, hmax = int(m.Hits or 0), int(m.HitsMax or 0)
            dead = bool(m.IsDead)
        except Exception:
            return None
        try:
            dist = int(m.Distance)
        except Exception:
            try:
                p = HOST.me()
                dist = max(abs(int(m.X) - int(p.X)), abs(int(m.Y) - int(p.Y)))
            except Exception:
                dist = 0
        return (name, hits, hmax, dist, dead, True)


    def full_mob(serial):
        """(2.6.82) This pass's row data of `serial`, the health read now when
        only its name and distance were (part_mobile); None when not in view."""
        mobs = st["mobs"]
        d = mobs.get(serial)
        if d is not None and d[5] is None:
            d = read_mobile(serial)
            if d is None:
                mobs.pop(serial, None)
            else:
                mobs[serial] = d
        return d


    def read_friends():
        """The friends list, names included, every FRIENDS_EVERY seconds."""
        now = time.time()
        if now < st["next_friends"]:
            return
        st["next_friends"] = now + FRIENDS_EVERY
        lst = CL.friends()
        named = lst is not None
        if lst is None:                                   # the API's serials, names from view
            try:
                serials = [int(s) for s in API.GetAllFriends()]
            except Exception:
                return
            lst = [(s, st["names"].get(s, "")) for s in serials]
        me = player_serial()
        # (2.6.82) the client's list as it was last time (every name given, so
        # nothing comes from view): the same result, no rebuild and no sort
        raw_key = (me, lst) if named else None
        if raw_key is not None and raw_key == st["friends_raw"]:
            if st["names_dirty"]:
                jobs.append(save_names)
            return
        out = []
        unnamed = False
        for serial, name in lst:
            if serial == me or not serial:
                continue
            if name:
                if st["names"].get(serial) != name:
                    st["names"][serial] = name
                    st["names_dirty"] = True
            else:
                unnamed = True
                d = st["mobs"].get(serial)
                name = (d[0] if d and d[0] else "") or st["names"].get(serial, "")
                if name and st["names"].get(serial) != name:
                    st["names"][serial] = name
                    st["names_dirty"] = True
                name = name or ("0x%08X" % serial)
            out.append((serial, name))
        out.sort(key=friend_order)                        # unnamed last
        st["friends"] = out
        st["fserials"] = [s for s, _n in out]
        st["friends_raw"] = None if unnamed else raw_key
        if st["names_dirty"]:
            jobs.append(save_names)                        # a write: off the client thread


    def friend_order(e):
        return (e[1].startswith("0x"), e[1].lower())


    def read_party():
        p = CL.party()
        if p is None:                                      # the API's view of it
            leader = int(safe(lambda: API.GetPartyLeader(), 0) or 0)
            members = safe(lambda: [int(s) for s in API.GetPartyMemberSerials()], []) or []
            p = (leader, 0, False, members) if leader else None
        st["party"] = p


    def in_party(p):
        """2.6.81: the client keeps a Party object (leader 0, no members) when you
        are in none; a leader, or anyone else listed, is a party."""
        return bool(p) and bool(p[0] or p[3])


    def read_profile(full=True):
        """Your own name, tooltip lines and (full) the Profile tab's values,
        every PROFILE_EVERY seconds. (2.6.82) The Guild tab needs only the name
        and the lines (full False); a profile read that way is read in full at
        once when the Profile tab wants it."""
        now = time.time()
        if now < st["next_profile"] and not (full and st["prof_part"]):
            return
        st["next_profile"] = now + PROFILE_EVERY
        try:
            p = HOST.me()
        except Exception:
            p = None
        if p is None:
            st["profile"] = None
            st["prof_part"] = False
            return
        try:
            name = str(p.Name or "")
            try:
                nap = p.raw.NameAndProps(False)
            except Exception:
                nap = ""
            lines = [l.strip() for l in str(nap or "").replace("\r", "").split("\n") if l.strip()]
            if not full:
                old = st["profile"]
                rest = old[2:] if old else ("", 0, 0, 0, 0, 0, False, False)
                st["profile"] = (name, lines) + tuple(rest)
                st["prof_part"] = True
                return
            try:                                           # the plain reads (they don't raise)
                vals = (noto_name(p.Notoriety), int(p.Gold or 0), int(p.Followers or 0),
                        int(p.FollowersMax or 0), int(p.Weight or 0), int(p.WeightMax or 0),
                        bool(p.InWarMode), bool(p.IsHidden))
            except Exception:                              # field by field, as before
                vals = (noto_name(safe(lambda: p.Notoriety)),
                        int(safe(lambda: p.Gold, 0) or 0),
                        int(safe(lambda: p.Followers, 0) or 0),
                        int(safe(lambda: p.FollowersMax, 0) or 0),
                        int(safe(lambda: p.Weight, 0) or 0), int(safe(lambda: p.WeightMax, 0) or 0),
                        bool(safe(lambda: p.InWarMode, False)), bool(safe(lambda: p.IsHidden, False)))
            prof = (name, lines) + vals
        except Exception:
            prof = None
        st["profile"] = prof
        st["prof_part"] = False


    def guild_lines():
        """Your tooltip's lines after the name: guild abbreviation / title."""
        prof = st["profile"]
        if not prof:
            return []
        return [l for l in prof[1][1:] if l and l != prof[0]]


    def scan_view():
        """Every player in view by name (for the roster), the Ally (green)
        ones as a list in API.GetAllMobiles order (guild_items sorts them,
        nearest first), and the set of every serial in view. One pass over
        the mobiles (2.6.82: the mother's shared scan, HOST.mobiles). Pets and
        NPCs are left out (a pet or vendor with a member's name must not stand
        in for the member): invulnerable mobiles, and non-humans when the build
        tells. (2.6.82) The human test comes first (most mobiles in a hunting
        area are not: two reads instead of four), and the name and distance of
        each player kept are remembered for the rows (st["kept"])."""
        try:
            mobs = HOST.mobiles()
        except Exception:
            mobs = []
        me = player_serial()
        view, allies, serials, kept = {}, [], set(), {}
        no_flags = CL_FLAGS[0]
        for m in mobs:
            try:
                s = int(m.Serial)
                if not s or s == me:
                    continue
                serials.add(s)
                if not no_flags:
                    try:
                        human = bool(m.IsHuman) or bool(m.IsGargoyle)
                    except AttributeError:             # a build without the flags: keep them all
                        CL_FLAGS[0] = no_flags = True
                        human = True
                    except Exception:
                        human = True
                    if not human:
                        continue
                n = None
                try:
                    n = m.Notoriety
                    ni = int(n) if n is not None else -1
                except Exception:                      # by name, as noto_name tells it
                    try:
                        nn = noto_name(n)
                    except Exception:
                        nn = ""
                    ni = 7 if nn == "Invulnerable" else (2 if nn == "Ally" else -1)
                if ni == 7:                            # Invulnerable
                    continue
                name = str(m.Name or "")
                if name:
                    view[name.lower()] = s
                if ni == 2:                            # Ally
                    allies.append((s, name))
                try:
                    kept[s] = (name, int(m.Distance))
                except Exception:
                    pass                               # (read in full by read_mobile)
            except Exception:
                pass
        st["view"], st["allies"], st["view_serials"], st["kept"] = view, allies, serials, kept


    CL_FLAGS = [False]                    # (2.6.82) True: the build has no IsHuman flag


    def friends_in_view(serials):
        """The friend serials in view this pass: from the serials scan_view
        made (the Guild tab), else (2.6.82) the mother's per-pass lookups: one
        HOST.mobile per friend, or one shared scan when there are many
        (presence only, no property reads: the rows shown get read_mobile)."""
        known = st["view_serials"]
        out = set()
        if known is None and len(serials) > FRIENDS_SCAN:
            known = set()
            try:
                for m in HOST.mobiles():
                    known.add(int(m.Serial))
            except Exception:
                known = None
        if known is not None:
            for s in serials:
                if s in known:
                    out.add(s)
            return out
        for s in serials:
            try:
                if s and HOST.mobile(s) is not None:
                    out.add(s)
            except Exception:
                pass
        return out


    FRIENDS_SCAN = 10                     # (2.6.82) more friends to look for: one scan instead


    # ---------- the guild window: reading its pages ----------
    # The PacketGumpText parser (text lines, commands, cells, cliloc texts)
    # lives in the mother since 2.6.01 (Kit.gump_parse / Kit.gump_cells /
    # Kit.cliloc_text / Kit.strip_html); it is given this module's CLILOCS
    # table so the guild window's captions read right without the client.
    # (2.6.82) the last two layouts parsed, and the last two classified: a poll
    # that sees the same layout again, and parse_info / parse_roster after the
    # poll that found the page, reuse the parse (results are never changed by
    # their users). Entries are replaced whole (one assignment each).
    _cells = [None, None]
    _kinds = [None, None]


    def gump_cells(raw):
        for e in _cells:
            if e is not None and (e[0] is raw or e[0] == raw):
                return e[1]
        out = Kit.gump_cells(raw, CLILOCS)
        _cells[1] = _cells[0]
        _cells[0] = (raw, out)
        return out


    def classify(raw):
        """'guild' for a page of the guild window (it carries the tab
        captions), 'noguild' for the create-a-guild window, 'roster' for the
        Guild Roster page (its column headers), else None."""
        for e in _kinds:
            if e is not None and (e[0] is raw or e[0] == raw):
                return e[1]
        kind = classify_now(raw)
        _kinds[1] = _kinds[0]
        _kinds[0] = (raw, kind)
        return kind


    def classify_now(raw):
        cells, buttons = gump_cells(raw)
        if not cells:
            return None
        texts = [c["text"].lower() for c in cells]
        clilocs = [c["cliloc"] for c in cells]
        kind = None
        if any(cl in TAB_CLILOCS for cl in clilocs) or ROSTER_TAB.lower() in texts:
            kind = "guild"
            if (1062955 in clilocs and 1062956 in clilocs) or ("rank" in texts and (
                    "last on" in texts or "name" in texts)):
                kind = "roster"
        elif any(cl in NOT_GUILDED_CLILOCS for cl in clilocs):
            kind = "noguild"
        else:
            joined = "\x00".join(texts)            # one text to look in (no word holds \x00)
            if any(w in joined for w in NOT_GUILDED):
                kind = "noguild"
        return kind


    def may_be_guild(raw):
        """(2.6.82) Cheap pre-test before classify: every guild window page
        carries a tab cliloc or the roster caption in its layout."""
        for t in TAB_MARKS:
            if t in raw:
                return True
        return "roster" in raw.lower()


    def bands(cells, tol=6):
        """Cells grouped into rows by y (tolerance tol), top to bottom, each
        row sorted by x."""
        out = []
        for c in sorted(cells, key=lambda c: (c["y"], c["x"])):
            if out and abs(c["y"] - out[-1][0]) <= tol:
                out[-1][1].append(c)
            else:
                out.append([c["y"], [c]])
        return [sorted(row, key=lambda c: c["x"]) for _, row in out]


    def parse_info(raw):
        """The My Guild page: name, alliance, faction, charter, website."""
        cells, _ = gump_cells(raw)
        cells = [c for c in cells if c["cliloc"] not in TAB_CLILOCS]
        out = {"name": "", "alliance": "", "faction": "", "charter": "", "website": ""}

        def right_of(label, cliloc):
            lab = None
            for c in cells:
                if c["cliloc"] == cliloc or c["text"].lower() == label.lower():
                    lab = c
                    break
            if lab is None:
                return ""
            best = None
            for c in cells:
                if c is lab or abs(c["y"] - lab["y"]) > 6 or c["x"] <= lab["x"]:
                    continue
                if best is None or c["x"] < best["x"]:
                    best = c
            return best["text"] if best is not None else ""

        out["name"] = right_of("Guild Name", 1062954)
        out["alliance"] = right_of("Alliance", 1063025)
        out["faction"] = right_of("Guild Faction", 1063084)
        wide = sorted([c for c in cells if c["w"] >= 300 and c["bg"]], key=lambda c: c["y"])
        if wide:
            out["charter"] = wide[0]["text"]
        if len(wide) > 1:
            out["website"] = wide[1]["text"]
        for k in ("charter", "website"):
            if "not yet set" in out[k].lower():
                out[k] = ""
        return out


    def parse_roster(raw):
        """One Guild Roster page: ([member dicts], more pages?). The column
        headers (Name, Rank, Last On, Guild Title) give the columns; every
        row below them is a member."""
        cells, buttons = gump_cells(raw)
        cells = [c for c in cells if c["cliloc"] not in TAB_CLILOCS
                 and c["text"].lower() not in TAB_CAPS_LOW]
        rows = bands(cells)
        header = None
        for row in rows:
            texts = [c["text"].lower() for c in row]
            if len(row) >= 3 and ("name" in texts or "rank" in texts or "last on" in texts
                                  or any(c["cliloc"] in (1062955, 1062956, 1062952, 1062953)
                                         for c in row)):
                header = row
                break
        if header is None:
            return [], False
        cols = [c["x"] for c in header]
        names = [c["text"].lower() for c in header]
        idx = {}
        for want, keys in (("name", ("name",)), ("rank", ("rank",)),
                           ("laston", ("last on", "online")), ("title", ("title",))):
            for i, n in enumerate(names):
                if any(k in n for k in keys) and i not in idx.values():
                    idx[want] = i
                    break
        if "name" not in idx:
            idx["name"] = 0
        members = []
        hy = header[0]["y"]
        for row in rows:
            if row[0]["y"] <= hy + 10:
                continue
            got = {}
            for c in row:
                best, bd = -1, 1e9
                for i, cx in enumerate(cols):
                    d = abs(c["x"] - cx)
                    if d < bd:
                        best, bd = i, d
                if bd <= 30 and best not in got:
                    got[best] = c
            if len(got) < 2 or idx["name"] not in got:
                continue
            nc = got[idx["name"]]
            name = nc["text"]
            if name.endswith(" *"):
                name = name[:-2]
            name = name.strip()
            if name.endswith(" VvV"):
                name = name[:-4].strip()
            if not name:
                continue
            raw_name = nc["raw"].lower()
            laston = got[idx["laston"]]["text"] if "laston" in idx and idx["laston"] in got else ""
            online = laston.lower() == "online" or "#000066" in raw_name or "#006600" in raw_name
            members.append({"name": name,
                            "rank": got[idx["rank"]]["text"] if "rank" in idx and idx["rank"] in got else "",
                            "laston": laston,
                            "title": got[idx["title"]]["text"] if "title" in idx and idx["title"] in got else "",
                            "online": online, "me": "#006600" in raw_name})
        more = any(b[2] == FORWARD_BUTTON for b in buttons)
        return members, more


    # ---------- the guild window: the read itself (script thread) ----------
    def _last_gump_run():
        gid = 0
        try:
            gid = int(API.HasGump() or 0)
        except Exception:
            gid = 0
        if not gid:
            return 0, ""
        try:
            g = API.GetGump(gid)
        except Exception:
            g = None
        if g is None:
            return gid, ""
        try:
            return gid, str(g.PacketGumpText or "")
        except Exception:
            return gid, ""


    def last_gump():
        """(2.6.82) (gid, layout) of the last server gump in ONE client hop
        (HasGump, GetGump and PacketGumpText each waited a frame of their own
        on the script's thread); (0, "") when there is none."""
        try:
            r = Kit.on_client(_last_gump_run)
        except Exception:
            r = None
        return r if r else (0, "")


    def guild_test(raw):
        return may_be_guild(raw) and classify(raw) in ("guild", "roster")


    def open_guild_gump():
        """(server serial, layout) of a guild window page that is open, wherever
        it sits among the open gumps (API.HasGump knows only the last one);
        (0, "") when none. One hop to the client thread. (2.6.82) A layout
        without the guild window's marks isn't parsed (may_be_guild)."""
        try:
            return CL.find_server_gump(guild_test)
        except Exception:
            return 0, ""


    def hide_next(gid=0):
        """The next server gump arrives invisible (TazUO's ConfigNextGump),
        when the setting says so; reset_hide() undoes a pending one."""
        if not settings["ghide"]:
            return
        if gid:
            safe(lambda: API.ConfigNextGump(serial=gid, isVisible=False))
        else:
            st["hid_any"] = True                 # whatever comes next is hidden
            safe(lambda: API.ConfigNextGump(isVisible=False))


    def reset_hide():
        st["hid_any"] = False
        safe(lambda: API.ConfigNextGump())


    def unknown_gump(had):
        """After the guild window didn't come: the gump that DID come in the
        meantime, if any, dumped to the journal (its first DUMP_CHARS of
        layout) so an unrecognised shard layout can be diagnosed, and closed
        when it arrived hidden through our hide_next(0). Returns a note."""
        gid, raw = last_gump()
        if not gid or gid == had:
            return "the guild window didn't come"
        dump = " ".join(raw.split())[:DUMP_CHARS] if raw else "(empty layout)"
        if st["hid_any"]:                        # hidden, so unseen: not left behind
            safe(lambda: API.CloseGump(gid))
            st["hid_any"] = False
            what = "closed again"
        else:
            what = "left open"
        API.SysMsg("Social: an unrecognised gump 0x%08X came instead of the guild window (%s); "
                   "its layout begins: %s." % (gid, what, dump), Kit.HUE_INFO)
        return "the guild window didn't come (another gump did, see above)"


    def wait_gump(check, timeout=GUMP_WAIT):
        """Polls the last server gump until check(gid, raw) returns something
        true, giving (gid, raw, result); (0, "", None) on timeout or stop."""
        deadline = time.time() + timeout
        while time.time() < deadline and not st["shutting"]:
            gid, raw = last_gump()                # (2.6.82) one hop, not three waits
            if gid:
                if raw:
                    r = check(gid, raw)
                    if r:
                        return gid, raw, r
            if not HOST.idle(0.15):
                break
        return 0, "", None


    def press(gid, label, button):
        """A tab of the guild window: its caption's button, else the known id."""
        gump = safe(lambda: API.GetGump(gid))
        if gump is not None:                     # the client's own control, if this is a wrapper
            gump = safe(lambda: Kit.client_control(gump)) or gump
        if gump is not None and CL.press_labelled(gump, label):
            return True
        if not button:                           # 0 = label only (ReplyGump(0) would close it)
            return False
        return bool(safe(lambda: API.ReplyGump(button, gid), False))


    def guild_job():
        """On the script's thread: open the guild window (hidden), read its
        My Guild page, go to Guild Roster and read every page, close it."""
        st["guild_busy"] = True
        st["guild_pages"] = 0
        old = st["guild"] or empty_guild()
        gd = old
        try:
            gd = read_guild_window(old)
        except Exception as ex:
            gd = empty_guild()
            gd["note"] = "couldn't read the guild window (%s)" % ex
        finally:
            reset_hide()
            hid = st.get("ghid", 0)
            st["ghid"] = 0
            if hid:                               # a page we opened hidden and didn't close
                safe(lambda: API.CloseGump(hid))
            # 2.6.81: the failure is remembered here, because the kept copy of a
            # good earlier read has ok True (it was taken as a success before)
            failed = not gd["ok"]
            if failed:                            # a failed read keeps what was known
                note, gd = gd["note"], dict(old)
                gd["note"] = note
                # the automatic retry backs off: 1, 2, 4... minutes, up to GUILD_RETRY_MAX
                st["guild_fails"] = min(st["guild_fails"] + 1, 10)
                st["guild_next"] = time.time() + min(GUILD_RETRY_MAX,
                                                     GUILD_RETRY * (2 ** (st["guild_fails"] - 1)))
            else:
                st["guild_fails"] = 0
                st["guild_said"] = ""
            st["guild"] = gd
            st["guild_busy"] = False
            st["guild_dirty"] = True
            if gd["ok"] and not failed:
                safe(save_guild)
        if gd["note"]:
            if not failed:
                API.SysMsg("Social: %s." % gd["note"], Kit.HUE_INFO)
            elif gd["note"] != st["guild_said"]:  # a failure is said once until it changes
                st["guild_said"] = gd["note"]
                again = ""
                if settings["gevery"] and settings["tab"] == "guild":
                    again = " (another try in %d min)" % max(
                        1, int((st["guild_next"] - time.time()) / 60 + 0.5))
                API.SysMsg("Social: %s%s." % (gd["note"], again), Kit.HUE_BAD)


    def read_guild_window(old):
        gd = empty_guild()
        gd["members"] = list(old["members"])          # kept if the roster can't be read
        # a guild window already open stays open and goes back to My Guild after
        gids = st["gids"]
        had, had_raw = last_gump()
        had_kind = classify(had_raw) if had_raw else None
        had_open = had_kind in ("guild", "roster")
        if not had_open:
            # the guild window may be open but not the LAST server gump (another
            # came after it): look through every open gump before asking for a new
            # one, which would close the user's window
            og, oraw = open_guild_gump()
            if og:
                had, had_raw, had_kind, had_open = og, oraw, classify(oraw), True
        if had_open:
            # read the window that is open as it is: asking the server for another
            # would close this one, and a press on the old one would be dropped
            gid, raw, kind = had, had_raw, had_kind
        else:
            # hide the next gump: the My Guild page by id once known, else whatever
            # comes (the create-a-guild window for a character without a guild)
            hide_next(gids.get("info", 0) if old.get("in_guild", True) else 0)
            if not CL.game_action("OpenGuildGump"):
                gd["note"] = "couldn't ask for the guild window (%s)" % CL.error
                return gd
            gid, raw, kind = wait_gump(lambda gid, raw: classify(raw))
            if not gid:
                gd["note"] = unknown_gump(had)        # what came instead, if anything
                return gd
            st["ghid"] = gid                          # ours, hidden: closed whatever happens
        if kind == "noguild":
            safe(lambda: API.CloseGump(gid))
            st["ghid"] = 0
            gd.update({"ok": True, "in_guild": False, "members": [], "at": time.time()})
            return gd
        if kind == "roster":                          # it opened on the roster: My Guild first
            gids["roster"] = gid
            if not had_open:
                hide_next(gids.get("info", 0))
            press(gid, INFO_TAB, INFO_BUTTON)
            gid, raw, kind = wait_gump(lambda gid, raw: classify(raw) == "guild" and "guild")
            if not gid:
                gd["note"] = "the My Guild page didn't come"
                return gd
            if not had_open:
                st["ghid"] = gid
        info = parse_info(raw)
        if had_open and not info.get("name"):         # open on another page (Diplomacy): My Guild first
            prev = raw
            press(gid, INFO_TAB, INFO_BUTTON)
            gid, raw, kind = wait_gump(lambda g2, r2: classify(r2) == "guild" and r2 != prev and "guild")
            if not gid:
                gd["note"] = "the My Guild page didn't come"
                return gd
            info = parse_info(raw)
        gids["info"] = gid
        gd.update(info)
        # the roster, every page
        if not had_open:
            hide_next(gids.get("roster", 0))
        if not press(gid, ROSTER_TAB, ROSTER_BUTTON):
            gd["note"] = "couldn't open the Guild Roster page"
            gd.update({"ok": True, "at": time.time()})
            return gd
        gid, raw, kind = wait_gump(lambda gid, raw: classify(raw) == "roster" and "roster")
        if not gid:
            gd["note"] = "the Guild Roster page didn't come"
            gd.update({"ok": True, "at": time.time()})
            return gd
        if not had_open:
            st["ghid"] = gid
        gids["roster"] = gid
        members, seen, pages, whole = [], {}, 0, False
        while not st["shutting"]:
            got, more = parse_roster(raw)
            pages += 1
            st["guild_pages"] = pages                 # shown as "page N" while it reads
            for m in got:
                k = m["name"].lower()
                if k not in seen:
                    seen[k] = True
                    members.append(m)
            if not more or pages >= ROSTER_PAGES_MAX:
                whole = True
                break
            if not had_open:
                hide_next(gid)
            if not safe(lambda: API.ReplyGump(FORWARD_BUTTON, gid), False):
                break
            prev = raw
            gid2, raw2, _ = wait_gump(lambda g2, r2: classify(r2) == "roster" and r2 != prev and "ok")
            if not gid2:
                break
            gid, raw = gid2, raw2
            if not had_open:
                st["ghid"] = gid
        if not whole or not members:
            # (2.6.84) a read cut short (a page that didn't come, a stop) or one that
            # found nobody: the members not read stay as last read (shown offline),
            # never dropped from the saved roster
            for m in old["members"]:
                k = m["name"].lower()
                if k not in seen:
                    seen[k] = True
                    c = dict((k2, v2) for k2, v2 in m.items() if not k2.startswith("_"))
                    c["online"] = False                # (its sort keys made afresh)
                    members.append(c)
            if not whole and pages:
                gd["note"] = "read %d roster page%s only; the rest as last read" % (
                    pages, "" if pages == 1 else "s")
        gd["members"] = members
        gd.update({"ok": True, "at": time.time()})
        if had_open:
            press(gid, INFO_TAB, INFO_BUTTON)        # leave it as it was: on My Guild
        else:
            safe(lambda: API.CloseGump(gid))
            st["ghid"] = 0
        return gd


    # ---------- window ----------
    queue = Kit.queuer(st)
    on_disposed = Kit.disposer(KEY, st, win)


    def win_w(tab):
        return GUILD_W if tab == "guild" else W


    # ---------- (2.6.57) in a zone ----------
    #  The layout tells the window its slot (layout_fit; hooks "fit" + "exact")
    #  and the window is drawn exactly that size: the title row and the tab row
    #  laid out for the width they get (the tabs go on a second line when they
    #  don't fit on one), the list rows across the whole width, as many rows as
    #  the height holds. Freed, its own size again. (2.6.56 stretched the
    #  window drawn at its own size: the title row's buttons overlapped, the tab
    #  row was cut off and the rows stopped short of the right edge.)
    def layout_fit(fw, fh, mode):
        new = (int(fw), int(fh)) if (fw is not None and fh is not None) else None
        # (2.6.69) "again": the layout measured the window and it isn't its slot's
        # size, so it is drawn again even though the slot is the one it was told
        if new != st.get("fit"):
            st["fit"] = new
            queue("redraw")()
        elif mode == "again" and new is not None:
            # (2.6.82) once per slot and drawing: when the redraw it asked for
            # still measures otherwise, drawing the same again can't change it
            # (it was rebuilt on every verify pass); any other build allows it again
            sig = (new, settings["tab"], st["minimized"], settings["rows"], settings["bars"])
            now = time.time()
            # (2.6.83) the same again too, 5 s on: a redraw that didn't land (a drag,
            # a client clamp) is drawn again instead of left to the layout's stretch
            if sig != st["again_for"] or not 0 <= now - st.get("again_at", 0.0) < 5.0:
                st["again_for"] = sig
                st["again_at"] = now
                st["again_build"] = True
                queue("redraw")()


    def min_title_w():
        """(2.6.64) The narrowest the window can be drawn: the title and the
        Fold, Minimize and Close buttons, without Settings."""
        M = Kit.MARGIN
        return max(160, M + 30 + Kit.text_w(TITLE.upper()) + 6 + 94 + M)


    def min_w():
        """The width the title row needs with its Settings button."""
        M = Kit.MARGIN
        return (M + 30 + Kit.text_w(TITLE.upper()) + 16 + 84 + Kit.DOCK_DX + 35
                + Kit.text_w("Settings") + M)


    def tab_lines(iw):
        """[(tab key, caption, x offset, line)] of the tab buttons in a row iw
        wide (wrapping to the next line), and the number of lines."""
        out, tx, line = [], 10, 0
        for key, cap in TABS:
            bw = 35 + Kit.text_w(cap)
            if tx > 10 and tx + bw > iw - 4:
                tx, line = 10, line + 1
            out.append((key, cap, tx, line))
            tx += bw + 14
        return out, line + 1


    def tab_layout(tab):
        """(info lines, toolbar rows, list rows) of a tab: how tall its body is."""
        if tab == "friends":
            return 1, 1, settings["rows"]
        if tab == "party":
            return 2, 3, settings["rows"]        # buttons, Accept / Decline, chat
        if tab == "guild":
            return 6, 2, settings["rows"]
        return 7, 2, 0


    def window_h(tab):
        info, bars, rows = tab_layout(tab)
        M = Kit.MARGIN
        body = 8 + info * 22 + (8 if info else 0) + bars * 30 + rows * ROW_H + (8 if rows else 0) + 4
        return M + 30 + Kit.GAP + 30 + Kit.GAP + body + M


    def min_size():
        """(2.6.81) The layout's "min" hook: the narrowest title row, and the
        tallest tab at one list row (the tab can change after the window is
        placed), plus 30 for the tab row wrapping onto a second line. Below
        that the info lines and toolbars were drawn past the window's bottom."""
        return (min_title_w(), max(window_h(t) - max(0, tab_layout(t)[2] - 1) * ROW_H
                                   for t, _c in TABS) + 30)


    def save_pos():
        Kit.save_pos(POS_KEY, win["g"])


    def build_window():
        tab = settings["tab"]
        size = (MINI_W, MINI_H) if st["minimized"] else (win_w(tab), window_h(tab))
        x, y = Kit.load_pos(POS_KEY, (200, 200), size)
        if Kit.is_open(win["g"]):
            x, y = win["g"].GetX(), win["g"].GetY()
        old, win["g"] = win["g"], None
        M = Kit.MARGIN
        store = ({}, {})
        c = {}
        rows = []
        win["info_tips"] = {}                       # (2.6.72) new labels: their tooltips afresh
        win["info_in"] = {}                         # (2.6.82) what set_info last wrote, per label
        if st["again_build"]:                       # (2.6.82) see layout_fit
            st["again_build"] = False
        else:
            st["again_for"] = None
        g = G.CreateGump(True, True)
        if safe(lambda: HOST.layout_locked(KEY), False):
            safe(lambda: setattr(g, "CanMove", False))   # (2.6.72) held in its zone
        if st["minimized"]:
            w, h = MINI_W, MINI_H
            c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
        else:
            w, h = win_w(tab), window_h(tab)
            fit = st.get("fit")
            if fit is not None:                      # (2.6.57) exactly its slot in a zone
                # (2.6.64) never narrower than its title row needs (the title,
                # Fold, Minimize, Close): below that they drew over one another
                w, h = max(min_title_w(), fit[0]), fit[1]
            IW = w - 2 * M
            c["iw"] = IW
            win["_build_c"] = c                      # (2.6.64) the toolbar's Sort button
            Kit.add_window_frame(g, w, h)
            # (2.6.58) too narrow for the Settings button: left out (the Virtue
            # Assistant window still opens the page), so nothing overlaps in the row
            Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                          queue("settings") if w >= min_w() else None)
            # tab row (on two lines when the window is too narrow for one)
            yt = M + 30 + Kit.GAP
            places, nlines = tab_lines(IW)
            Kit.add_section(g, M, yt, IW, 30 * nlines)
            c["tabs"] = {}
            for key, cap, tx, line in places:
                hue = Kit.HUE_TITLE if key == tab else Kit.HUE_TEXT
                c["tabs"][key] = Kit.art_button(g, store, "tab_" + key, Kit.ART_PAGE, M + tx,
                                                yt + 4 + 30 * line, cap,
                                                TAB_TIPS.get(key, "Show the %s tab" % cap),
                                                hue=hue, on_click=queue(("tab", key)))
            # body
            yb = yt + 30 * nlines + Kit.GAP
            if fit is None:
                h += 30 * (nlines - 1)               # (one line at its own width, as before)
            bh = h - yb - M
            Kit.add_section(g, M, yb, IW, bh)
            # (2.6.64) in a zone the rows are counted under the toolbars as they
            # were laid out (a narrow one may wrap onto another line)
            build_tab(g, store, c, rows, tab, M, yb, IW, bh, fit is not None)
            win.pop("_build_c", None)
        Kit.place(g, x, y, w, h)                     # wholly on screen, always
        win.update({"g": g, "c": c, "store": store, "rows": rows, "tab": tab, "info": {}})
        G.AddControlOnDisposed(g, on_disposed(g))
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, save_pos))      # its place is saved when let go
        if st["minimized"] and st["docked"]:         # folded into the Action Bar
            safe(lambda: setattr(g, "IsVisible", False))
        st["rebuild"] = False
        refresh()
        Kit.dispose(old)


    def build_tab(g, store, c, rows, tab, x, y, w, h, fit=False):
        info, bars, nrows = tab_layout(tab)
        TOOL_RIGHT[0] = x + w - 6

        def list_rows(yy):
            """(2.6.64) In a zone: as many rows as fit under yy (at least one)."""
            if fit:
                return max(1, (y + h - 12 - yy) // ROW_H)
            return nrows

        yy = y + 8
        c["info"] = []
        for i in range(info):
            c["info"].append(Kit.add_label(g, "", x + 10, yy, Kit.HUE_INFO))
            yy += 22
        if info:
            yy += 8
        if tab == "friends":
            items = [("add", Kit.ART_PLAY, ["Add friend...", None],
                      "Target someone to put them on TazUO's friends list"),
                     ("add_last", Kit.ART_OK, ["Add last target", None],
                      "Put your last target on TazUO's friends list")]
            yy = toolbar_paged(g, store, c, x, y, yy, w, items, None, bool(info))
            add_rows(g, store, c, rows, list_rows(yy), x, yy, w,
                     "Click: set them as your last target (or answer a target cursor). "
                     "Shift+click: write a note on them. Alt+click: auto-follow (again to stop)",
                     True, rm_tip="Remove them from TazUO's friends list")
        elif tab == "party":
            yy += 30 * toolbar(g, store, x, yy, x + w - 6, [
                ("invite", Kit.ART_PLAY, ["Invite...", None],
                 "Target someone to invite them to your party"),
                ("leave", Kit.ART_CLOSE, ["Leave", None], "Leave the party"),
                ("loot", Kit.ART_OK, ["Loot", None],
                 "Allow or forbid party members looting your corpse (the line above says "
                 "which it is now)"),
                ("pwin", Kit.ART_PAGE, ["Party window", None],
                 "Open the client's party window")])[0]
            # Accept / Decline on their own row (shown while an invitation waits):
            # after Party window they stood past the window's right edge
            # (2.6.81) the page arrows go at this row's end (only two buttons on it):
            # the party had none, so members past the first page were never seen;
            # a narrow zone drops the two captions before they reach the arrows
            bx = x + 10
            c["accept_x"] = bx
            TOOL_RIGHT[0] = x + w - 6 - PAGER_W - 6
            c["accept"] = tool(g, store, bx, yy, "accept", Kit.ART_OK, "Accept",
                               "Join the party you were invited to. "
                               "Alt+click: auto-follow the inviter (again to stop)", ret="ctrl",
                               on_click=invite_click("accept"))
            c["decline"] = tool(g, store, c["accept"][1], yy, "decline", Kit.ART_CLOSE, "Decline",
                                "Turn the party invitation down. "
                                "Alt+click: auto-follow the inviter (again to stop)", ret="ctrl",
                                on_click=invite_click("decline"))
            TOOL_RIGHT[0] = x + w - 6
            pager(g, store, c, x + w, yy)
            yy += 30
            chat(g, store, c, x, yy, w, [("psend", "Send", "Say the text in party chat")],
                 "Type a message for party chat, then click Send")
            yy += 30
            add_rows(g, store, c, rows, list_rows(yy), x, yy, w,
                     "Click: set them as your last target (or answer a target cursor). "
                     "Shift+click: write a note on them. Alt+click: auto-follow (again to stop)",
                     True, rm_tip="Remove them from the party (the leader only)")
        elif tab == "guild":
            # (2.6.64) Refresh, Guild window, Diplomacy, the Sort button and the
            # page arrows, laid out for the width the window has (in a zone the
            # page arrows go up beside the guild's name and the captions give way
            # last button first, instead of drawing over one another)
            items = [("grefresh", Kit.ART_PLAY, ["Refresh", None],
                      "Read the guild window again (My Guild and every roster page); "
                      + ("it is opened hidden and closed again" if settings["ghide"] else
                         "it shows while read; the Social settings page can hide it")),
                     ("gwin", Kit.ART_PAGE, ["Guild window", None],
                      "Open the guild window (the server's guild menu)"),
                     ("diplo", Kit.ART_PAGE, ["Diplomacy", None],
                      "Open the guild window on its Diplomacy page (wars and alliances)"),
                     ("gsort", Kit.ART_PAGE, ["long", "short", None], None)]
            # the roster's order (2.6.05): "Sort: ..." when it fits, else the
            # short captions, else the button alone (its tooltip names the order)
            yy = toolbar_paged(g, store, c, x, y, yy, w, items, [3, 2, 1, 0, 3], bool(info))
            chat(g, store, c, x, yy, w, [("gsend", "Guild", "Say the text in guild chat"),
                                         ("asend", "Alliance", "Say the text in alliance chat")],
                 "Type a message, then click Guild or Alliance to say it in that chat")
            yy += 30
            add_rows(g, store, c, rows, list_rows(yy), x, yy, w,
                     "Click: set them as your last target when they are in view. "
                     "Shift+click: write a note on them. Alt+click: auto-follow (again to stop)",
                     False, before=[("rank", RANK_W)], after=[("title", 0)])
        else:
            yy += 30 * toolbar(g, store, x, yy, x + w - 6, [
                ("edit", Kit.ART_PAGE, ["Edit profile", None],
                 "Open your character profile (the server's scroll; closing it saves)"),
                ("paperdoll", Kit.ART_PAGE, ["Paperdoll", None], "Open the client's paperdoll"),
                ("status", Kit.ART_PAGE, ["Status", None], "Open the client's status window")])[0]
            toolbar(g, store, x, yy, x + w - 6, [
                ("ignore", Kit.ART_PAGE, ["Ignore list", None],
                 "Open TazUO's ignore list (players whose speech is hidden)"),
                ("war", Kit.ART_PLAY, ["War / peace", None],
                 "Switch between war mode and peace (the last line above says which)")])


    PAGER_W = 100                         # (2.6.64) the page arrows and "1/3" at a row's end


    def sort_tip(c):
        """The Sort button's tooltip (the button alone names the order in it)."""
        tip = ("Click for the next roster order: online (members in view first), "
               "last on, rank or name")
        if c.get("gsort_bare"):
            e = SORTS[SORT_CODES.index(settings["gsort"])]
            tip = "Roster order: %s. %s" % (e[2].lower(), tip)
        return tip


    def cap_w(key, cap):
        """Pixel width a caption needs (the Sort button: its widest order)."""
        if key == "gsort":
            if cap == "long":
                return max(Kit.text_w(e[1]) for e in SORTS)
            return max(Kit.text_w(e[2]) for e in SORTS)
        return Kit.text_w(cap)


    def toolbar_plan(items, x, right, order):
        """(2.6.64) The caption level of each button so the row fits between
        x + 10 and right: every caption first, then the levels stepped down in
        `order` (item indexes, one step each; default: the last button's
        caption goes first). None when even the last step doesn't fit."""
        lv = [0] * len(items)
        if order is None:
            order = list(range(len(items) - 1, -1, -1))
        steps = [None] + list(order)
        for st_i in steps:
            if st_i is not None:
                lv[st_i] = min(lv[st_i] + 1, len(items[st_i][2]) - 1)
            bx, end = x + 10, x + 10
            for i, it in enumerate(items):
                cap = it[2][lv[i]]
                if cap is None:
                    end, bx = bx + 30, bx + 30
                else:
                    cw = cap_w(it[0], cap)
                    end, bx = bx + 35 + cw, bx + 35 + cw + 12
            if end <= right:
                return list(lv)
        return None


    def toolbar(g, store, x, y, right, items, order=None, plan=None):
        """(2.6.64) A row of buttons `items` [(key, art, [captions..., None],
        tooltip)] from x + 10 to `right`. Captions give way (toolbar_plan); when
        even the buttons alone don't fit, the row wraps onto the next line.
        Returns (lines used, levels used)."""
        lv = plan or toolbar_plan(items, x, right, order)
        wrap = lv is None
        if wrap:
            lv = [len(it[2]) - 1 for it in items]
        bx, line = x + 10, 0
        for i, it in enumerate(items):
            key, art, caps, tip = it
            cap = caps[lv[i]]
            if key == "gsort":
                c = win.get("_build_c")
                c["gsort_long"] = cap == "long"
                c["gsort_bare"] = cap is None
                tip = sort_tip(c)
                cap = None if cap is None else sort_caption(c)
            need = 30 if cap is None else 35 + Kit.text_w(cap)
            if wrap and bx > x + 10 and bx + need > right:
                bx, line = x + 10, line + 1
            yb = y + 30 * line
            if cap is None:
                ctrl = Kit.art_button(g, store, key, art, bx, yb,
                                      None, (caps[0] + ": " + tip[0].lower() + tip[1:])
                                      if caps[0] and key != "gsort" else tip,
                                      on_click=queue(key))
                bx += 30
            else:
                ctrl = Kit.art_button(g, store, key, art, bx, yb,
                                      cap, tip, on_click=queue(key))
                bx += 35 + Kit.text_w(cap) + 12
            if key == "gsort":
                c = win["_build_c"]
                c["gsort"] = ctrl if cap is not None else None    # its caption, updated in place
                c["gsort_btn"] = store[0].get(key)
        return line + 1, lv


    def toolbar_paged(g, store, c, x, y, yy, w, items, order, can_move):
        """(2.6.64) A toolbar with the page arrows at its right end. When the
        buttons would lose a caption beside them (a narrow zone), the arrows go
        up to the end of the first info line instead (cut short for them).
        Returns the y under the toolbar."""
        plan = toolbar_plan(items, x, x + w - 6 - PAGER_W - 6, order)
        full = plan is not None and all(
            it[2][l] is not None and (l == 0 or it[0] == "gsort") for it, l in zip(items, plan))
        if full or not can_move:
            lines, _lv = toolbar(g, store, x, yy, x + w - 6 - PAGER_W - 6, items, order, plan)
            pager(g, store, c, x + w, yy)
        else:
            lines, _lv = toolbar(g, store, x, yy, x + w - 6, items, order)
            pager(g, store, c, x + w, y + 8 - 6)
            c["info_cut"] = PAGER_W + 6
        return yy + 30 * lines


    TOOL_RIGHT = [100000]                 # (2.6.58) the toolbar's right edge in this build


    def tool(g, store, x, y, key, art, cap, tip, ret="x", on_click=None):
        on_click = on_click or queue(key)        # (2.6.81) a handler of its own (Alt+click)
        if x + 35 + Kit.text_w(cap) > TOOL_RIGHT[0]:
            # (2.6.58) no room for its caption (a narrow zone): the button alone,
            # its tooltip names it
            ctrl = Kit.art_button(g, store, key, art, x, y, None, cap + ": " + tip[0].lower() + tip[1:],
                                  on_click=on_click)
            nx = x + 30
            if ret == "ctrl":
                return (store[0].get(key), nx, ctrl)
            return nx
        ctrl = Kit.art_button(g, store, key, art, x, y, cap, tip, on_click=on_click)
        nx = x + 35 + Kit.text_w(cap) + 12
        if ret == "ctrl":
            return (store[0].get(key), nx, ctrl)
        return nx


    def invite_click(key):
        """(2.6.81) Accept / Decline act on the inviter: Alt+click follows them
        instead (standing rule); Alt is read in the click itself."""
        def handler(*args):
            p = st["party"]
            inv = p[1] if p else 0
            if inv and Follow.alt_held():
                queue(("follow", inv))()
            else:
                queue(key)()
        return handler


    def pager(g, store, c, right, y):
        """Page arrows and "1/3" at the right end of a toolbar row."""
        c["pg"] = Kit.add_label(g, "", right - 100, y + 6, Kit.HUE_INFO)
        Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 56, y + 4, None, "Previous page",
                       on_click=queue(("page", -1)))
        Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 34, y + 4, None, "Next page",
                       on_click=queue(("page", 1)))


    def chat(g, store, c, x, y, w, buttons, field_tip):
        """A text field (tooltip field_tip) and its Send buttons (right-aligned)."""
        bw = sum(35 + Kit.text_w(cap) + 12 for _, cap, _ in buttons)
        fw = w - 20 - bw - 8
        if fw < MSG_W_MIN:                       # (2.6.58) narrow: the buttons go without
            # captions, the field keeps its room ((2.6.64) down to 40 px, so
            # the buttons stay inside the window)
            fw = max(40, w - 20 - 30 * len(buttons) - 8)
        c["msg"] = Kit.add_textbox(g, st["msg"].get(settings["tab"], ""), x + 10, y + 3, fw,
                                   numbers=False)
        safe(lambda: c["msg"].SetTooltip(field_tip))
        bx = x + 10 + fw + 12
        for key, cap, tip in buttons:
            bx = tool(g, store, bx, y, key, Kit.ART_PLAY, cap, tip)


    def add_rows(g, store, c, rows, n, x, y, w, tip, removable, before=None, after=None,
                 rm_tip="Remove"):
        """A pool of n list rows: name, [extra columns], health bar, status,
        [extra columns], X (tooltip rm_tip). `before` / `after` are
        [(key, width)] extra label columns (width 0 = the rest of the row)."""
        bw, bh = Kit.pic_size(Kit.LINE_RED)
        bw, bh = bw or 109, bh or 9
        fw, fh = Kit.pic_size(Kit.LINE_BLUE)
        right = x + w - 4 - (40 if removable else 0)
        # (2.6.64) a row too narrow for every column even at their floors (a
        # narrow zone): the extra columns go, the last first, then the health
        # bar; what a column would show is in the row's tooltip instead
        before, after = list(before or []), list(after or [])
        dropped = []
        bars = settings["bars"]

        def floors():
            return (sum(wd + 8 for _k, wd in before) + sum((wd or 40) + 8 for _k, wd in after)
                    + 8 + 40 + 8 + (30 + 8 if bars else 0) + 44)

        while right - (x + 10) < floors() and (after or before or bars):
            if after:
                dropped.append(after.pop()[0])
            elif before:
                dropped.append(before.pop()[0])
            else:
                bars = False
        # (2.6.58) the columns share the width the row really has: at the window's
        # own width as before; narrower (a zone), the status and the bar give way
        # down to a floor, then the name takes what is left, so nothing runs past
        # the X or the window's edge
        name_w, status_w = NAME_W, STATUS_W
        fixed = sum(wd + 8 for _k, wd in (before or [])) + \
            sum((wd or 40) + 8 for _k, wd in (after or []))
        room = right - (x + 10) - fixed - 8
        need = NAME_W + 8 + (bw + 8 if bars else 0) + STATUS_W
        if room < need:
            status_w = max(44, min(STATUS_W, int(room * 0.24)))
            if bars:
                bw = max(30, min(bw, int(room * 0.30)))
            name_w = max(40, room - status_w - 8 - (bw + 8 if bars else 0))
        c["bar_w"], c["name_w"], c["status_w"] = bw, name_w, status_w
        for i in range(n):
            ry = y + i * ROW_H
            r = {"serial": 0, "prev": (0, 0.0), "parts": [], "name": None, "status": None,
                 "fill": None, "fill_w": -1, "x": None, "red": None, "extra": {}, "who": "",
                 "prev_who": ("", 0.0),          # the name it showed before, and when it changed
                 "tip0": tip, "tip": tip}       # the row tooltip, and what it says now
            cx = x + 10
            r["name"] = Kit.add_label(g, "", cx, ry + 3)
            r["parts"].append([r["name"], True])
            cx += name_w + 8
            for key in dropped:
                r["extra"][key] = (None, 0)      # (2.6.64) left out: shown in the tooltip
            for key, wd in before:
                lbl = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO)
                r["extra"][key] = (lbl, wd)
                r["parts"].append([lbl, True])
                cx += wd + 8
            if bars:
                # tiled to the bar's width (a narrow row draws a shorter bar)
                red = Kit.add_tiled(g, Kit.LINE_RED, cx, ry + 7, bw, bh)
                if red is not None:
                    safe(lambda: red.SetAcceptMouseInput(False))
                r["red"] = [red, True]
                r["parts"].append(r["red"])
                if fw and fh:
                    r["fill"] = Kit.add_tiled(g, Kit.LINE_BLUE, cx, ry + 7, 1, fh)
                    safe(lambda: r["fill"].SetWidth(0))
                    r["parts"].append([r["fill"], True])
                cx += bw + 8
            r["status"] = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO)
            r["parts"].append([r["status"], True])
            cx += status_w + 8
            for key, wd in after:
                wd = wd or max(40, right - cx)
                lbl = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO)
                r["extra"][key] = (lbl, wd)
                r["parts"].append([lbl, True])
                cx += wd + 8
            r["catch"] = Kit.catcher(g, x + 4, ry, w - 8 - (40 if removable else 0), ROW_H,
                                     row_click(rows, i), tip)
            r["parts"].append([r["catch"], True])
            if removable:
                r["x"] = Kit.art_button(g, store, "rm%d" % i, Kit.ART_CLOSE, x + w - 42, ry + 1,
                                        None, rm_tip + ". Alt+click: auto-follow (again to stop)",
                                        on_click=rm_click(rows, i))
                r["parts"].append([r["x"], True])
            rows.append(r)


    def rm_click(rows, i):
        """The X on a row: Alt+click follows the row's mobile (the standing
        rule), a plain click removes them."""
        def handler(*args):
            r = rows[i]
            serial = r["serial"]
            prev, at = r["prev"]
            if prev and time.time() - at < 0.15:    # the row just changed: what was seen
                serial = prev
            if serial and Follow.alt_held():
                queue(("follow", serial))()
            elif serial:                            # 2.6.81: remove the one that was shown,
                queue(("rm", serial))()             # not whoever holds the row at tick time
        return handler


    def row_click(rows, i):
        def handler(*args):
            r = rows[i]
            serial = r["serial"]
            now = time.time()
            prev, at = r["prev"]
            if prev and now - at < 0.15:            # the row just changed: what was seen
                serial = prev
            who = r["who"]
            pw, pat = r["prev_who"]
            if pw and now - pat < 0.15:
                who = pw
            if not serial:
                if who and not Follow.alt_held() and shift_held():
                    queue(("note", who))()          # Shift+click: a note on them (2.6.05)
                elif who:
                    queue(("noview", who))()
                return
            if Follow.alt_held():
                queue(("follow", serial))()
            elif who and shift_held():
                queue(("note", who))()
            else:
                queue(("click", serial))()
        return handler


    NO_EXTRA = {}


    def set_row(r, serial, name, status, hue, frac, extra=None, name_hue=None, bar=True,
                show_x=True):
        # (2.6.82) the same as the last pass (the common case): nothing to write.
        # The extra columns are rank / title (the only ones add_rows makes); the
        # notes version keeps a saved note's tooltip fresh; hide_row forgets it.
        ex = extra or NO_EXTRA
        key = (serial, name, status, hue, frac, ex.get("rank"), ex.get("title"), name_hue, bar,
               show_x, notes_st["ver"])
        if key == r.get("last"):
            return
        r["last"] = key
        if r["serial"] != serial:
            r["prev"] = (r["serial"], time.time())
            r["serial"] = serial
        if r["who"] != name:
            r["prev_who"] = (r["who"], time.time())
            r["who"] = name
        if name_hue is None:
            name_hue = Kit.HUE_TEXT if frac is not None else Kit.HUE_INFO
        c = win["c"]
        Kit.set_text(r["name"], fit(name, c.get("name_w", NAME_W)), name_hue)
        Kit.set_text(r["status"], fit(status, c.get("status_w", STATUS_W)), hue)
        cut = []                                  # columns too long for the row: the tooltip has them
        for key, (lbl, wd) in r["extra"].items():
            full = str((extra or {}).get(key, "") or "")
            if lbl is None:                       # (2.6.64) a column left out: the tooltip has it
                if full:
                    cut.append("%s: %s" % (key.capitalize(), full))
                continue
            short = fit(full, wd)
            Kit.set_text(lbl, short, Kit.HUE_INFO)
            if short != full:
                cut.append("%s: %s" % (key.capitalize(), full))
        tip = r["tip0"] if not cut else r["tip0"] + "\n" + "\n".join(cut)
        if NOTES:                                 # the note on them (2.6.05)
            e = NOTES.get(name.lower())
            if e is not None:
                tip = tip + "\nNote: " + e[1]
        if tip != r["tip"] and r.get("catch") is not None:
            r["tip"] = tip
            try:
                r["catch"].SetTooltip(tip)
            except Exception:
                pass
        w = int(win["c"].get("bar_w", 109) * max(0.0, min(1.0, frac or 0.0)))
        if r["fill"] is not None and w != r["fill_w"]:
            r["fill_w"] = w
            safe(lambda: Kit.ui_w(r["fill"], max(1, w)))
        xp = r["parts"][-1] if r["x"] is not None else None   # the X is the last part
        for p in r["parts"]:
            if r["fill"] is not None and p[0] is r["fill"]:
                set_vis(p, bar and w > 0)
            elif r["red"] is not None and p is r["red"]:
                set_vis(p, bar)
            elif p is xp:
                set_vis(p, show_x)                # 2.6.81: written once, not shown then hidden
            else:
                set_vis(p, True)


    def hide_row(r):
        r["last"] = None                          # (2.6.82) the next set_row writes in full
        if r["serial"]:
            r["prev"] = (r["serial"], time.time())
            r["serial"] = 0
        if r["who"]:
            r["prev_who"] = (r["who"], time.time())
            r["who"] = ""
        for p in r["parts"]:
            set_vis(p, False)


    def mobile_status(serial):
        """(status text, hue, health fraction or None) of a mobile from this pass's reads."""
        d = full_mob(serial)
        if d is None:
            return "away", Kit.HUE_INFO, None
        name, hits, hmax, dist, dead, noto = d
        if dead:
            return "dead", Kit.HUE_BAD, 0.0
        frac = hits / float(hmax) if hmax > 0 else None
        hue = Kit.HUE_GOOD if frac is None or frac > 0.5 else (Kit.HUE_TITLE if frac > 0.25 else Kit.HUE_BAD)
        return ("%d tile%s" % (dist, "" if dist == 1 else "s")), hue, frac


    def page_of(items):
        """The items on the current page of the current tab, and "p/n"."""
        n = max(1, len(win["rows"]))
        pages = max(1, (len(items) + n - 1) // n)
        p = max(0, min(pages - 1, st["page"].get(settings["tab"], 0)))
        st["page"][settings["tab"]] = p
        return items[p * n:(p + 1) * n], ("%d/%d" % (p + 1, pages)) if pages > 1 else ""


    RANK_INDEX = dict((name, i) for i, names in enumerate(RANK_ORDER) for name in names)


    def laston_key(m):
        """A member's "Last On" as a sortable number (newest highest; -1 when
        it isn't a date), worked out once per member read (kept in the dict)."""
        v = m.get("_lo")
        if v is None:
            v = -1
            hit = DATE_RE.search(m["laston"] or "")
            if hit is not None:
                a, sep, b, c = hit.group(1), hit.group(2), int(hit.group(3)), hit.group(4)
                ia, ic = int(a), int(c)
                if len(a) == 4 or ia > 31:          # year first: 2026-10-31
                    y, mo, d = ia, b, ic
                else:                                # year last: day / month first?
                    y = ic + (2000 if ic < 100 else 0)
                    if ia > 12:
                        d, mo = ia, b
                    elif b > 12:
                        mo, d = ia, b
                    elif sep == ".":
                        d, mo = ia, b
                    else:
                        mo, d = ia, b
                if 1 <= mo <= 12 and 1 <= d <= 31:
                    v = y * 10000 + mo * 100 + d
            m["_lo"] = v
        return v


    def sort_caption(c):
        e = SORTS[SORT_CODES.index(settings["gsort"])]
        return e[1] if c.get("gsort_long") else e[2]


    # (2.6.82) The roster's order kept per read: for the last on, rank and name
    # orders it depends only on the members (re-sorted when a read replaces
    # them or the order changes); for online, the members out of view keep the
    # same order (online first, then by name) and only those in view are sorted
    # each pass, nearest first. The same keys as before, so the same order.
    gcache = {"src": None, "how": None, "order": [], "names": {}, "online": 0}


    def mkey(m):
        """A member's lower-case name (worked out once, kept in the dict)."""
        k = m.get("_k")
        if k is None:
            k = m["_k"] = m["name"].lower()
        return k


    def first(e):
        return e[0]


    def static_key(how):
        nranks = len(RANK_ORDER)
        if how == "online":
            return lambda m: ((0 if m["online"] else 1), m["_k"])
        if how == "name":
            return lambda m: m["_k"]
        if how == "rank":
            return lambda m: (RANK_INDEX.get((m["rank"] or "").strip().lower(), nranks), m["_k"])
        return lambda m: ((0 if m["online"] else 1), -laston_key(m), m["_k"])


    def guild_order(gd, how):
        mem = gd["members"]
        gc = gcache
        if gc["src"] is not mem or gc["how"] != how:
            names, online = {}, 0
            for m in mem:
                names[mkey(m)] = True
                if m["online"]:
                    online += 1
            gc.update({"src": mem, "how": how, "order": sorted(mem, key=static_key(how)),
                       "names": names, "online": online})
        return gc


    def guild_items(me=None):
        """The roster rows: (serial in view or 0, member dict), in the order
        the Sort button says: online first (members in view first, nearest
        first, then online, then the rest by name), last on (online, then the
        newest date), rank (top rank first) or name; allies in view that
        aren't on the roster come last, nearest first. (2.6.82) Returns the
        rows and the members in view among them; me = your lower-case name."""
        gd = st["guild"] or empty_guild()
        view, mobs = st["view"], st["mobs"]
        if me is None:
            me = player_name().lower()
        how = settings["gsort"]
        gc = guild_order(gd, how)
        items = []
        inview = 0
        if how == "online":
            near = []
            for m in gd["members"]:
                serial = view.get(m["_k"], 0)
                if serial:
                    d = mobs.get(serial)
                    if d:
                        near.append(((d[3], (0 if m["online"] else 1), m["_k"]), serial, m))
            if near:
                near.sort(key=first)
                inview = len(near)
                for e in near:
                    items.append((e[1], e[2]))
                for m in gc["order"]:
                    serial = view.get(m["_k"], 0)
                    if not (serial and mobs.get(serial)):
                        items.append((serial, m))
            else:
                for m in gc["order"]:
                    items.append((view.get(m["_k"], 0), m))
        else:
            for m in gc["order"]:
                serial = view.get(m["_k"], 0)
                if serial and serial in mobs:
                    inview += 1
                items.append((serial, m))
        names = gc["names"]
        allies = []
        for serial, name in st["allies"]:
            k = name.lower()
            if k in names or k == me or not name:
                continue
            d = mobs.get(serial)
            allies.append(((d[3] if d else 999, k), serial,
                           {"name": name, "rank": "ally", "laston": "", "title": "ally in view",
                            "online": True, "me": False, "_k": k,
                            "ally": True}))   # (2.6.81) not counted as a member
        if allies:
            allies.sort(key=first)
            for e in allies:
                items.append((e[1], e[2]))
        return items, inview


    def refresh():
        """Write what changed into the window (labels, rows, bars)."""
        g, c = win["g"], win["c"]
        if g is None or (st["minimized"] and st["docked"]):
            return
        if st["minimized"]:
            n, inview = len(st["friends"]), len(st["inview"])
            party = st["party"]
            txt = "%s: %d friend%s, %d in view" % (TITLE, n, "" if n == 1 else "s", inview)
            if in_party(party):                  # 2.6.81: leader 0 and nobody is no party
                txt += ", party of %d" % (len(party[3]) + 1)
            Kit.set_text(c["status"], fit(txt, MINI_W - 18 - 66))
            return
        tab = win["tab"]
        info = c.get("info", [])
        tw = c.get("iw", win_w(tab) - 2 * Kit.MARGIN) - 20   # (2.6.58) the width it really has
        tw0 = tw - c.get("info_cut", 0)          # the first info line, beside the page arrows
        if tab == "friends":
            items = st["friends"]
            shown, pg = page_of(items)
            inview = len(st["inview"])
            fk = (len(items), inview, tw0)       # (2.6.82) formatted only when it changes
            if win["info"].get("friends") != fk:
                win["info"]["friends"] = fk
                Kit.set_text(info[0], fit("%d friend%s on TazUO's friends list, %d in view" % (
                    len(items), "" if len(items) == 1 else "s", inview) if items else
                    "No friends on the list yet: Add friend... targets one", tw0))
            Kit.set_text(c["pg"], pg)
            for i, r in enumerate(win["rows"]):
                if i < len(shown):
                    serial, name = shown[i]
                    d = st["mobs"].get(serial)
                    status, hue, frac = mobile_status(serial)
                    set_row(r, serial, (d[0] if d and d[0] else name), status, hue, frac)
                else:
                    hide_row(r)
        elif tab == "party":
            party = st["party"]
            me = player_serial()
            if not in_party(party):              # 2.6.81: the client's empty Party is none
                Kit.set_text(info[0], fit("Not in a party: Invite... asks someone to join yours", tw),
                             Kit.HUE_INFO)
                Kit.set_text(info[1], "", Kit.HUE_INFO)
                items = []
            else:
                leader, inviter, loot, members = party
                ld = st["mobs"].get(leader)
                lname = "you" if leader == me else (ld[0] if ld and ld[0] else
                                                    st["names"].get(leader, "") or "0x%08X" % leader)
                Kit.set_text(info[0], fit(("Party of %d, led by %s" % (len(members) + 1, lname))
                                          if leader else "Party of %d" % (len(members) + 1), tw),
                             Kit.HUE_TEXT)
                Kit.set_text(info[1], fit("Party members may loot your corpse: %s"
                                          % ("yes" if loot else "no"), tw), Kit.HUE_INFO)
                items = [s for s in members if s != me]
            inviter = party[1] if party else 0
            invite = bool(inviter) and not (party and party[0])
            for k in ("accept", "decline"):
                ctrl = c.get(k)
                if ctrl is not None:
                    key = "vis_" + k
                    if win["info"].get(key) != invite:
                        win["info"][key] = invite
                        for part in (ctrl[0], ctrl[2]):
                            safe(lambda part=part: setattr(part, "IsVisible", invite))
            if invite:
                nm = st["mobs"].get(inviter)
                Kit.set_text(info[0], fit("Invited to a party by %s: Accept or Decline" % (
                    nm[0] if nm and nm[0] else "0x%08X" % inviter), tw), Kit.HUE_TITLE)
            shown, pg = page_of(items)
            if c.get("pg") is not None:
                Kit.set_text(c["pg"], pg)            # 2.6.81: the party tab pages too
            lead = bool(party) and party[0] == me and bool(me)
            for i, r in enumerate(win["rows"]):
                if i < len(shown):
                    serial = shown[i]
                    d = st["mobs"].get(serial)
                    status, hue, frac = mobile_status(serial)
                    # 2.6.81: the X shows only for the leader, set once (no hide after show)
                    set_row(r, serial, (d[0] if d and d[0] else st["names"].get(serial, "") or
                                        "0x%08X" % serial), status, hue, frac, show_x=lead)
                else:
                    hide_row(r)
        elif tab == "guild":
            refresh_guild(info, c, tw)
        else:
            if st["prof_part"]:                  # (2.6.82) read on the Guild tab: all of it now
                read_profile(True)
            prof = st["profile"]
            if not prof:
                win["info"].pop("prof", None)
                for l in info:
                    Kit.set_text(l, "")
                Kit.set_text(info[0], fit("No character logged in", tw), Kit.HUE_INFO)
                return
            pk = (prof, tw)                      # (2.6.82) formatted only when it changes
            if win["info"].get("prof") == pk:
                return
            win["info"]["prof"] = pk
            name, lines, noto, gold, fol, fmax, wt, wmax, war, hidden = prof
            titles = [l for l in lines if l != name]
            texts = [(name, Kit.HUE_TITLE),
                     (" / ".join(titles) if titles else      # (cut to the width below)
                      "No titles read yet: hover yourself once", Kit.HUE_INFO),
                     ("Notoriety: %s" % (noto or "unknown"), Kit.HUE_TEXT),
                     ("Gold: %d" % gold, Kit.HUE_TEXT),
                     ("Followers: %d / %d" % (fol, fmax), Kit.HUE_TEXT),
                     ("Weight: %d / %d" % (wt, wmax), Kit.HUE_TEXT),
                     ("%s%s" % ("War mode" if war else "Peace", ", hidden" if hidden else ""),
                      Kit.HUE_BAD if war else Kit.HUE_GOOD)]
            for l, (t, hue) in zip(info, texts):
                Kit.set_text(l, fit(t, tw), hue)     # (2.6.64) a narrow zone cuts them short


    def info_tip(lbl, full, shown):
        """(2.6.72) An info line cut to its width carries its whole text as its
        tooltip (only written when that changes)."""
        tip = full if shown != full else ""
        tips = win.get("info_tips")
        if tips is None:
            tips = win["info_tips"] = {}
        if len(tips) > 64:
            tips.clear()
        # (2.6.82) keyed by the label itself, as Kit.set_text does (id() of a
        # client object is a slow lookup in IronPython and can be reused)
        if tips.get(lbl) == tip:
            return
        tips[lbl] = tip
        safe(lambda: lbl.SetAcceptMouseInput(bool(tip)))
        safe(lambda: lbl.SetTooltip(tip))

    def set_info(lbl, full, width, hue):
        # (2.6.82) the same line as last time: nothing to cut or write (a long
        # charter took the slow, letter by letter way through fit every pass)
        done = win.get("info_in")
        k = (full, width, hue)
        if done is not None and done.get(lbl) == k:
            return
        shown = fit(full, width)
        Kit.set_text(lbl, shown, hue)
        info_tip(lbl, full, shown)
        if done is not None:
            if len(done) > 64:
                done.clear()
            done[lbl] = k


    def plain_info(lbl, text, hue=None):
        """An info line written without set_info: set_info writes it in full next time."""
        Kit.set_text(lbl, text, hue)
        done = win.get("info_in")
        if done is not None:
            done.pop(lbl, None)

    def refresh_guild(info, c, tw):
        """The Guild tab: the My Guild page's lines, then the roster rows."""
        tw0 = tw - c.get("info_cut", 0)          # (2.6.64) beside the page arrows, in a zone
        gd = st["guild"] or empty_guild()
        lines = guild_lines()
        if not gd["ok"]:
            plain_info(info[0], fit("Guild window not read yet", tw0), Kit.HUE_INFO)
        elif not gd["in_guild"]:
            plain_info(info[0], fit("Not in a guild", tw0), Kit.HUE_INFO)
        else:
            set_info(info[0], gd["name"] or "Guild name not shown", tw0, Kit.HUE_TITLE)
        # (2.6.72) a line cut to the window's width has its whole text as its tooltip
        set_info(info[1], ("You: " + " / ".join(lines)) if lines else
                 "Your guild line isn't read yet: hover yourself once", tw,
                 Kit.HUE_TEXT if lines else Kit.HUE_INFO)
        if gd["ok"] and gd["in_guild"]:
            set_info(info[2], "Alliance: %s     Faction: %s" % (
                gd["alliance"] or "none", gd["faction"] or "none"), tw, Kit.HUE_TEXT)
            set_info(info[3], "Charter: %s" % (gd["charter"] or "not set"), tw, Kit.HUE_INFO)
            set_info(info[4], "Website: %s" % (gd["website"] or "not set"), tw, Kit.HUE_INFO)
        else:
            for l in info[2:5]:
                plain_info(l, "")
        me_name = str(player_name() or "").lower()
        # 2.6.81: members only in the "in view" count (allies in view off the
        # roster were counted too); (2.6.82) both counts come with the order
        items, inview = guild_items(me_name)
        online = guild_order(gd, settings["gsort"])["online"]
        if st["guild_busy"]:
            pages = st["guild_pages"]
            status = "Reading the guild window" + (" (roster page %d)" % pages if pages else "")
            hue = Kit.HUE_TITLE
        elif not gd["ok"]:
            note = gd["note"]
            status = ((note[:1].upper() + note[1:]) if note else
                      ("Click Refresh to read the guild window" if not settings["gevery"]
                       else "The guild window is read when this tab shows"))
            hue = Kit.HUE_BAD if note else Kit.HUE_INFO
        elif not gd["in_guild"]:
            status, hue = "Read %s; allies in view are listed below" % ago(gd["at"]), Kit.HUE_INFO
        else:
            n = len(gd["members"])
            status = "%d member%s, %d online, %d in view; read %s" % (
                n, "" if n == 1 else "s", online, inview, ago(gd["at"]))
            if gd["note"]:
                status += "  (%s)" % gd["note"]
            hue = Kit.HUE_INFO
        set_info(info[5], status, tw, hue)
        shown, pg = page_of(items)
        Kit.set_text(c["pg"], pg)
        for i, r in enumerate(win["rows"]):
            if i < len(shown):
                serial, m = shown[i]
                # (2.6.82) the health of the rows shown only (full_mob)
                d = full_mob(serial) if serial else None
                if d is not None:
                    stat, hue, frac = mobile_status(serial)
                elif m["online"]:
                    stat, hue, frac = "Online", Kit.HUE_GOOD, None
                else:
                    stat, hue, frac = (m["laston"] or "offline"), Kit.HUE_INFO, None
                if m["me"] or (me_name and mkey(m) == me_name):
                    nhue = Kit.HUE_TITLE                 # you (also after a reload of the saved copy)
                elif d is not None or m["online"]:
                    nhue = Kit.HUE_GOOD if d is None else Kit.HUE_TEXT
                else:
                    nhue = Kit.HUE_INFO
                set_row(r, serial if d is not None else 0, m["name"], stat, hue, frac,
                        extra={"rank": m["rank"], "title": m["title"]}, name_hue=nhue,
                        bar=d is not None)
            else:
                hide_row(r)


    # ---------- the note window (2.6.05) ----------
    NOTE_BODY_H = 104
    NOTE_H = Kit.MARGIN + 30 + Kit.GAP + NOTE_BODY_H + Kit.MARGIN


    def save_note_pos():
        Kit.save_pos(NOTE_POS_KEY, ed["g"])


    def note_disposed(g):
        def handler(*args):
            if ed["g"] is g:                     # gone some other way: forget it
                ed.update({"g": None, "c": {}, "store": ({}, {})})
        return handler


    def open_note(name):
        """The note window for `name` (one at a time: a new name replaces it).
        Placed where it was last left, else beside Social's window."""
        close_note()
        w, h = NOTE_W, NOTE_H
        M = Kit.MARGIN
        dx, dy = 240, 180
        if Kit.is_open(win["g"]):
            try:
                dx, dy = win["g"].GetX() + 40, win["g"].GetY() + 60
            except Exception:
                pass
        x, y = Kit.load_pos(NOTE_POS_KEY, (dx, dy), (w, h))
        store, c = ({}, {}), {}
        g = G.CreateGump(True, True)
        Kit.add_window_frame(g, w, h)
        Kit.add_section(g, M, M, w - 2 * M, 30)
        Kit.add_label(g, "NOTE ON A PLAYER", M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None,
                       "Close (an unsaved change is dropped)", on_click=queue("note_close"))
        IW = w - 2 * M
        yb = M + 30 + Kit.GAP
        Kit.add_section(g, M, yb, IW, NOTE_BODY_H)
        lx = M + 12
        fx = lx + max(Kit.text_w("Player:"), Kit.text_w("Note:")) + 10
        Kit.add_label(g, "Player:", lx, yb + 13)
        c["name"] = Kit.add_textbox(g, name, fx, yb + 10, 200, numbers=False)
        safe(lambda: c["name"].SetTooltip("The player's name, as it shows over their head "
                                          "(any case)"))
        Kit.add_label(g, "Note:", lx, yb + 43)
        c["text"] = Kit.add_textbox(g, NOTES.get(name.lower(), ("", ""))[1], fx, yb + 40,
                                    M + IW - 12 - fx, numbers=False)
        safe(lambda: c["text"].SetTooltip("Your note on them (up to %d letters); Save with it "
                                          "empty deletes the note" % NOTE_CHARS))
        by = yb + 72
        Kit.art_button(g, store, "save", Kit.ART_OK, lx, by, "Save",
                       "Save the note (every character of this account sees it)",
                       on_click=queue("note_save"))
        Kit.art_button(g, store, "delete", Kit.ART_CLOSE, lx + 35 + Kit.text_w("Save") + 16, by,
                       "Delete", "Delete the note on this player", on_click=queue("note_delete"))
        hint = "Kept for the whole account"
        Kit.add_label(g, hint, M + IW - 12 - Kit.text_w(hint), by + 3, Kit.HUE_INFO)
        Kit.place(g, x, y, w, h)                 # wholly on screen
        ed.update({"g": g, "c": c, "store": store, "name": name})
        G.AddControlOnDisposed(g, note_disposed(g))
        G.AddGump(g)
        safe(lambda: Kit.on_moved(g, save_note_pos))   # its place is saved when let go


    def close_note():
        g = ed["g"]
        if g is None:
            return
        save_note_pos()
        ed.update({"g": None, "c": {}, "store": ({}, {})})
        Kit.dispose(g)


    def note_fields():
        """(name, note) as typed in the note window (read on the client thread)."""
        c = ed["c"]
        try:
            name = str(c["name"].Text or "")
        except Exception:
            name = ed["name"]
        try:
            text = str(c["text"].Text or "")
        except Exception:
            text = ""
        return name, text


    # ---------- doing things ----------
    def read_msg():
        """The chat field's text (one read), kept for a rebuild."""
        tb = win["c"].get("msg")
        if tb is None:
            return ""
        txt = str(safe(lambda: tb.Text, "") or "").strip()
        return txt


    def clear_msg():
        tb = win["c"].get("msg")
        if tb is not None:
            safe(lambda: tb.SetText(""))
        st["msg"].pop(settings["tab"], None)


    def say(kind, txt):
        if not txt:
            API.SysMsg("Social: type something first.", Kit.HUE_INFO)
            return
        if kind == "party":
            API.PartyMsg(txt)
        elif kind == "guild":
            API.GuildMsg(txt)
        else:
            API.AllyMsg(txt)
        clear_msg()


    def add_friend(serial):
        serial = int(serial or 0)
        if not serial:
            API.SysMsg("Social: nothing targeted.", Kit.HUE_INFO)
            return
        if serial == player_serial():
            API.SysMsg("Social: that's you.", Kit.HUE_INFO)
            return
        m = safe(lambda: API.FindMobile(serial))
        if m is None:
            API.SysMsg("Social: target a player or creature in view.", Kit.HUE_BAD)
            return
        name = str(safe(lambda: m.Name, "") or "")
        who = name or "0x%08X" % serial
        already = safe(lambda: [int(s) for s in API.GetAllFriends()], None) or []
        if serial in already or any(s == serial for s, _ in st["friends"]):
            API.SysMsg("Social: %s is already on the friends list." % who, Kit.HUE_INFO)
        elif safe(lambda: API.AddFriend(serial), False):
            if name:
                st["names"][serial] = name
                st["names_dirty"] = True
            API.SysMsg("Social: %s added to the friends list." % who, Kit.HUE_GOOD)
            if st["seen"] is not None:            # 2.6.81: already in view, not "came into view"
                st["seen"] = st["seen"] | {serial}   # a new set: seen may be inview itself
        else:
            API.SysMsg("Social: couldn't add %s to the friends list." % who, Kit.HUE_BAD)
        st["next_friends"] = 0.0


    def remove_friend(serial):
        name = st["names"].get(serial, "") or "0x%08X" % serial
        if safe(lambda: API.RemoveFriend(serial), False):
            API.SysMsg("Social: %s removed from the friends list." % name, Kit.HUE_INFO)
        else:
            API.SysMsg("Social: couldn't remove %s." % name, Kit.HUE_BAD)
        if st["seen"]:
            st["seen"].discard(serial)
        st["next_friends"] = 0.0


    def row_remove(serial):
        """2.6.81: takes the serial the row showed when clicked (was the row index,
        read again at tick time, after a re-sort could have moved someone else in)."""
        if not serial:
            return
        if win["tab"] == "friends":
            remove_friend(serial)
        elif win["tab"] == "party":
            party = st["party"]
            if party and party[0] and party[0] == player_serial():
                if not CL.game_action("RequestPartyRemoveMember", [to_uint(serial)], False):
                    API.SysMsg("Social: couldn't remove them (%s)." % CL.error, Kit.HUE_BAD)
            else:
                API.SysMsg("Social: only the party leader can remove members.", Kit.HUE_INFO)


    def clear_inviter():
        """(2.6.81) On the client thread, after Accept / Decline was sent: World.
        Party.Inviter = 0, as the client's own party window does after its send
        (the server's answer doesn't clear it, so the invitation stayed shown)."""
        try:
            import System
            party = CL.get(CL.world, "Party") if CL.world is not None else None
            if party is not None:
                CL.set(party, "Inviter", System.UInt32(0))
        except Exception:
            pass
        p = st["party"]
        if p:                                     # the row goes now, not at the next read
            st["party"] = (p[0], 0, p[2], p[3])


    def to_uint(serial):
        try:
            import System
            return System.UInt32(int(serial))
        except Exception:
            return serial


    def open_window(what):
        """A client window, the way the Action Bar opens them."""
        ok = False
        if what == "paperdoll":
            ok = CL.game_action("OpenPaperdoll", [to_uint(player_serial())])
        elif what == "status":
            ok = CL.game_action("OpenStatusBar")
        elif what == "guild":
            ok = CL.game_action("OpenGuildGump")
        elif what == "party":
            ok = CL.game_action("RequestPartyInviteByTarget", (), False)
        elif what == "ignore":
            ok = CL.open_ignore_list()
        elif what == "profile":
            ok = CL.game_action("RequestProfile", [to_uint(player_serial())], False)
        if not ok:
            API.SysMsg("Social: couldn't open that (%s)." % (CL.error or "no client access"),
                       Kit.HUE_BAD)
        return ok


    def party_window():
        """The client's own party window: the built-in 'Open PartyManifest' macro."""
        world = (CL.find(), CL.world)[1]
        if world is None:
            API.SysMsg("Social: couldn't open the party window (no client access: %s)." % CL.error,
                       Kit.HUE_BAD)
            return

        def run():
            import System
            mgr = CL.get(world, "Macros")
            asm = mgr.GetType().Assembly
            mo_t, mt_t, ms_t = [asm.GetType("ClassicUO.Game.Managers." + n)
                                for n in ("MacroObject", "MacroType", "MacroSubType")]
            mo = System.Activator.CreateInstance(mo_t, System.Array[object](
                [System.Enum.Parse(mt_t, "Open", True), System.Enum.Parse(ms_t, "PartyManifest", True)]))
            CL.call(mgr, "SetMacroToExecute", [mo])
            CL.call(mgr, "Update")
            return True
        if not CL.on_main(run):
            API.SysMsg("Social: couldn't open the party window (%s)." % CL.error, Kit.HUE_BAD)


    def diplomacy_job():
        """On the script's thread: open the guild window and press its
        Diplomacy button once the server's gump is up."""
        # a guild window that is already open is used as it is (asking for another
        # would close it and a press on the old one would be dropped)
        gid, raw = last_gump()
        if not (gid and classify(raw) in ("guild", "roster")):
            gid = open_guild_gump()[0]               # open, but not the last gump?
        if not gid:
            if not CL.game_action("OpenGuildGump"):
                API.SysMsg("Social: couldn't ask for the guild window (%s)." % CL.error, Kit.HUE_BAD)
                return
            # the tab captions are clilocs, so the page is recognised by classify, not by text
            gid, _raw, _kind = wait_gump(lambda g2, r2: classify(r2) in ("guild", "roster") and "ok")
        if not gid:
            API.SysMsg("Social: the guild window didn't show a %s button (are you in a guild?)."
                       % DIPLOMACY_LABEL, Kit.HUE_BAD)
            return
        if not press(gid, DIPLOMACY_LABEL, settings["dbutton"]):
            API.SysMsg("Social: found the guild window but not its %s button; press it there "
                       "(or set its button id on the Social settings page)." % DIPLOMACY_LABEL,
                       Kit.HUE_INFO)


    def click_mobile(serial):
        """A row clicked: make the mobile the last target, or answer a cursor."""
        if safe(lambda: API.HasTarget("any"), False) and not HOST.cursor_busy(KEY):
            API.Target(serial)
            return
        safe(lambda: API.SetLastTarget(to_uint(serial)))
        m = safe(lambda: API.FindMobile(serial))
        name = str(safe(lambda: m.Name, "") or "") if m is not None else ""
        if m is None:
            API.SysMsg("Social: %s isn't in view." % (st["names"].get(serial, "") or "they"),
                       Kit.HUE_INFO)
        else:
            API.SysMsg("Social: %s is your last target." % (name or "that"), Kit.HUE_INFO)


    def start_guild_read():
        """Queue a read of the guild window (one at a time)."""
        if st["guild_busy"]:
            return False
        st["guild_busy"] = True             # shows "Reading..." until the job takes over
        st["guild_next"] = time.time() + GUILD_RETRY
        jobs.append(guild_job)
        return True


    def friend_name(s):
        d = st["mobs"].get(s)
        return (d[0] if d and d[0] else "") or st["names"].get(s, "") or "a friend"


    def announce():
        """A friend came into view (and, with the option, left it): one journal
        line (not for the ones already in view when the module starts)."""
        now_in = st["inview"]
        if not (settings["announce"] or settings["left"]) or st["seen"] is None:
            st["seen"] = now_in
            return
        if settings["announce"]:
            for s in now_in - st["seen"]:
                API.SysMsg("Social: %s is in view." % friend_name(s), Kit.HUE_GOOD)
        if settings["left"]:
            for s in st["seen"] - now_in:
                API.SysMsg("Social: %s left view." % friend_name(s), Kit.HUE_INFO)
        st["seen"] = now_in


    # ---------- settings page (drawn inside the Virtue Assistant window) ----------
    # WINDOW (two grey lines, a check, a field), FRIENDS (two checks),
    # GUILD WINDOW (a check, two fields): 30 title + rows (20 grey, 26 check,
    # 28 field) + 10 each, Kit.GAP between
    H1, H2, H3 = 30 + 20 + 20 + 26 + 28 + 10, 30 + 26 + 26 + 10, 30 + 26 + 28 + 28 + 10
    PAGE_H = H1 + Kit.GAP + H2 + Kit.GAP + H3


    def config_height(w):
        return PAGE_H


    def field(g, c, key, label, value, x, y, tip, unit=""):
        """A labelled number field with a tooltip on both, and a grey unit after it."""
        lbl = Kit.add_label(g, label, x, y + 4)
        fx = x + Kit.text_w(label) + 10
        tb = Kit.add_textbox(g, str(value), fx, y, 40)
        safe(lambda: lbl.SetTooltip(tip))
        safe(lambda: tb.SetTooltip(tip))
        if unit:
            Kit.add_label(g, unit, fx + 40 + 8, y + 4, Kit.HUE_INFO)
        c[key] = tb


    def build_config(g, x, y, w):
        c = {}
        Kit.add_section(g, x, y, w, H1, "WINDOW")
        Kit.add_label(g, fit("Shift+click a row to write a note on that player; %d saved for "
                             "this account." % len(NOTES), w - 28), x + 12, y + 30, Kit.HUE_INFO)
        Kit.add_label(g, fit("An Action Bar cell can show this window: right-click a cell, "
                             "Client window, page 2.", w - 28), x + 12, y + 50, Kit.HUE_INFO)
        c["bars"] = Kit.add_check(g, "Show health bars on the rows",
                                  x + 12, y + 70, settings["bars"],
                                  "A bar for each friend, party member and guildmate in view; "
                                  "off, the rows show name, status and distance only")
        field(g, c, "rows", "Rows per page:", settings["rows"], x + 12, y + 96,
              "Rows the Friends, Party and Guild tabs show per page (%d-%d); the window "
              "grows with them" % (ROWS_MIN, ROWS_MAX))
        y += H1 + Kit.GAP
        Kit.add_section(g, x, y, w, H2, "FRIENDS  (said in the journal)")
        c["announce"] = Kit.add_check(g, "Say when a friend comes into view",
                                      x + 12, y + 30, settings["announce"],
                                      "One journal line when someone on TazUO's friends list "
                                      "comes into view (not for those in view when Social starts)")
        c["left"] = Kit.add_check(g, "Say when a friend leaves view",
                                  x + 12, y + 56, settings["left"],
                                  "One journal line when a friend who was in view is gone")
        y += H2 + Kit.GAP
        Kit.add_section(g, x, y, w, H3, "GUILD WINDOW  (read into the Guild tab)")
        c["ghide"] = Kit.add_check(g, "Read the guild window hidden",
                                   x + 12, y + 30, settings["ghide"],
                                   "It opens invisible for the read and is closed again; off, it "
                                   "shows on screen for a few seconds")
        field(g, c, "gevery", "Read it again every:", settings["gevery"], x + 12, y + 58,
              "Minutes between reads of the guild window while the Guild tab shows "
              "(0-%d, 0 = only when you click Refresh)" % GUILD_EVERY_MAX, unit="min")
        field(g, c, "dbutton", "Diplomacy button id:", settings["dbutton"], x + 12, y + 86,
              "Pressed when the Diplomacy caption can't be found (0-%d, 0 = caption only; "
              "ServUO uses %d). Change it if Diplomacy opens the wrong page."
              % (DIPLOMACY_BUTTON_MAX, DIPLOMACY_BUTTON))
        page.update({"c": c})


    def num_field(c, key, lo, hi):
        """The field's number when it is one within [lo, hi], else the setting as is."""
        try:
            txt = str(c[key].Text or "").strip()
        except Exception:
            txt = ""
        if txt.isdigit() and lo <= int(txt) <= hi:
            return int(txt)
        return settings[key]


    def checked(c, key):
        """A check box of the page, else the setting as it is."""
        try:
            return bool(c[key].IsChecked)
        except Exception:
            return bool(settings[key])


    def poll_config():
        c = page["c"]
        if c is None:
            return
        # (2.6.82) plain reads (the mother polls the page at 4 Hz unless typing)
        ann = checked(c, "announce")
        left = checked(c, "left")
        bars = checked(c, "bars")
        ghide = checked(c, "ghide")
        rows = num_field(c, "rows", ROWS_MIN, ROWS_MAX)
        gevery = num_field(c, "gevery", 0, GUILD_EVERY_MAX)
        dbutton = num_field(c, "dbutton", 0, DIPLOMACY_BUTTON_MAX)
        new = (ann, left, bars, rows, gevery, ghide, dbutton)
        cur = (settings["announce"], settings["left"], settings["bars"], settings["rows"],
               settings["gevery"], settings["ghide"], settings["dbutton"])
        if new != cur:
            # the Guild tab's Refresh tooltip tells whether the read is hidden
            layout = ((bars, rows) != (settings["bars"], settings["rows"])
                      or (ghide != settings["ghide"] and settings["tab"] == "guild"))
            if (ann or left) and not (settings["announce"] or settings["left"]):
                st["seen"] = None            # announcements just turned on: a silent first look
            settings.update({"announce": ann, "left": left, "bars": bars, "rows": rows,
                             "gevery": gevery, "ghide": ghide, "dbutton": dbutton})
            save_settings()
            if layout:
                st["rebuild"] = True


    def config_closed():
        page["c"] = None


    # ---------- module hooks ----------
    def _start():
        st.update({"shutting": False, "docked": False, "queue": [], "page": {}, "mobs": {},
                   "inview": set(), "seen": None, "next_list": 0.0, "next_friends": 0.0,
                   "next_profile": 0.0, "guild_busy": False, "guild_dirty": False,
                   "guild_next": 0.0, "guild_fails": 0, "guild_said": "", "guild_pages": 0,
                   "ghid": 0, "hid_any": False, "view": {}, "view_serials": None, "allies": [],
                   "fit": None,                 # (2.6.71) the layout tells it again when slotted
                   "me_s": 0, "friends_raw": None, "kept": {}, "prof_part": False,
                   "again_for": None, "again_build": False,      # (2.6.82) speed caches
                   "minimized": bool(safe(lambda: HOST.dock_wanted(KEY), False)) or
                   Kit.load_min(MIN_KEY)})          # as you left it
        del jobs[:]                              # nothing queued before a stop runs now
        # (2.6.82) the first start right after the module was built (same
        # character) uses what the build loaded: names, guild copy and notes
        # were read just then and nothing can have saved them since
        if not (LOADED_FOR[0] and LOADED_FOR[0] == player_serial()):
            load_settings()
        LOADED_FOR[0] = 0
        CL.find()
        build_window()
        hooks = Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"))
        hooks["fit"] = layout_fit                # (2.6.57) drawn exactly its slot in a zone
        hooks["exact"] = True
        hooks["verify"] = True                   # (2.6.69) measured by the layout every pass
        hooks["min"] = min_size                  # (2.6.81) no zone lower than its fixed part
        HOST.dock_add(KEY, hooks)
        HOST.services["social.note"] = note_of   # Ultima Tracker's row tooltips (2.6.05)


    def _tick():
        if win["g"] is None:
            return
        if Kit.was_clicked(win["store"], "close"):
            Kit.dispose(win["g"])            # on_disposed turns the module off
            return
        q = st["queue"]                          # (2.6.82) one lookup (_start makes a new list)
        while q:
            action = q.pop(0)
            kind = action[0] if isinstance(action, tuple) else action
            if action == "settings":
                HOST.show_settings(KEY)
            elif action == "toggle_min":
                if not st["minimized"]:
                    st["msg"][settings["tab"]] = read_msg()
                st["minimized"] = not st["minimized"]
                st["docked"] = False
                Kit.save_min(MIN_KEY, st["minimized"])
                HOST.dock_forget(KEY)            # its own minimized form, not the bar
                build_window()
            elif action == "to_bar":
                st["msg"][settings["tab"]] = read_msg()
                HOST.dock_to_bar(KEY, TITLE)     # folds in now, or once the bar is up
            elif action == "redraw":
                st["rebuild"] = True
            elif kind == "tab":
                if action[1] != settings["tab"]:
                    st["msg"][settings["tab"]] = read_msg()
                    settings["tab"] = action[1]
                    save_settings()
                    st["rebuild"] = True
            elif kind == "page":
                st["page"][settings["tab"]] = max(0, st["page"].get(settings["tab"], 0) + action[1])
                st["next_list"] = 0.0
            elif kind == "follow":               # Alt+click on a row (standing rule)
                Follow.toggle(action[1], TITLE)
            elif kind == "click":
                click_mobile(action[1])
            elif kind == "noview":
                API.SysMsg("Social: %s isn't in view." % action[1], Kit.HUE_INFO)
            elif kind == "rm":
                row_remove(action[1])
            elif action == "add":
                API.SysMsg("Social: target the friend to add.", Kit.HUE_INFO)
                HOST.pick_target(PICK_TIMEOUT,
                                 lambda serial: st["queue"].append(("picked", int(serial or 0))))
            elif kind == "picked":
                if action[1]:
                    add_friend(action[1])
            elif action == "add_last":
                add_friend(int(safe(lambda: API.LastTargetSerial, 0) or 0))
            elif action == "invite":
                if open_window("party"):
                    API.SysMsg("Social: target who to invite.", Kit.HUE_INFO)
            elif action == "leave":
                party = st["party"]
                if not in_party(party):          # 2.6.81: not the client's empty Party
                    API.SysMsg("Social: you aren't in a party.", Kit.HUE_INFO)
                elif not CL.game_action("RequestPartyRemoveMember", [to_uint(player_serial())], False):
                    API.SysMsg("Social: couldn't leave (%s)." % CL.error, Kit.HUE_BAD)
            elif action == "loot":
                party = st["party"]
                if not in_party(party):          # 2.6.81: not the client's empty Party
                    API.SysMsg("Social: you aren't in a party.", Kit.HUE_INFO)
                elif CL.game_action("RequestPartyLootState", [not party[2]], False):
                    API.SysMsg("Social: party members %s loot your corpse." % (
                        "may not" if party[2] else "may"), Kit.HUE_INFO)
                else:
                    API.SysMsg("Social: couldn't change that (%s)." % CL.error, Kit.HUE_BAD)
            elif action == "pwin":
                party_window()
            elif action == "accept":
                party = st["party"]
                if party and party[1]:
                    inv = to_uint(party[1])

                    def accept():                # (2.6.81) one hop: the request, then the
                        if not CL.game_action("RequestPartyAccept", [inv], False):
                            return None
                        clear_inviter()          # invitation is gone, as the client's own
                        return True              # party window does it
                    if CL.on_main(accept) is None:
                        API.SysMsg("Social: couldn't accept (%s)." % CL.error, Kit.HUE_BAD)
            elif action == "decline":
                party = st["party"]
                if party and party[1]:
                    inv = to_uint(party[1])
                    net = Client._type("ClassicUO.Network.AsyncNetClient")
                    ext = Client._type("ClassicUO.Network.NetClientExt")

                    def decline():               # (the packet sender returns nothing: say True)
                        sock = CL.get(None, "Socket", net)
                        try:                     # an instance method on older clients...
                            CL.call(sock, "Send_PartyDecline", [inv])
                            clear_inviter()      # (2.6.81) the row goes, as in the client's
                            return True          # own party window
                        except Exception:
                            if ext is None:
                                raise
                        # ...a static extension method (NetClientExt) on newer ones
                        CL.call(None, "Send_PartyDecline", [sock, inv], ext)
                        clear_inviter()
                        return True
                    if net is None or CL.on_main(decline) is None:
                        API.SysMsg("Social: couldn't decline (%s)." % CL.error, Kit.HUE_BAD)
            elif action == "psend":
                say("party", read_msg())
            elif action == "gsend":
                say("guild", read_msg())
            elif action == "asend":
                say("ally", read_msg())
            elif action == "gwin":
                open_window("guild")
            elif action == "grefresh":
                st["guild_said"] = ""            # a read you asked for reports its failure
                if start_guild_read():
                    refresh()
                else:
                    API.SysMsg("Social: the guild window is being read already.", Kit.HUE_INFO)
            elif action == "diplo":
                jobs.append(diplomacy_job)       # waits for the server: never on this tick
            elif action == "edit":
                open_window("profile")
            elif action == "paperdoll":
                open_window("paperdoll")
            elif action == "status":
                open_window("status")
            elif action == "ignore":
                open_window("ignore")
            elif action == "war":
                API.SetWarMode(not bool(safe(lambda: API.Player.InWarMode, False)))
            elif kind == "note":                 # Shift+click on a row (2.6.05)
                if str(action[1]).startswith("0x"):
                    API.SysMsg("Social: that player's name isn't known yet.", Kit.HUE_INFO)
                else:
                    open_note(action[1])
            elif action == "note_save":
                if ed["g"] is not None:
                    name, text = note_fields()
                    if set_note(name, text):
                        close_note()
            elif action == "note_delete":
                if ed["g"] is not None:
                    name, _text = note_fields()
                    if set_note(name, ""):
                        close_note()
            elif action == "note_close":
                close_note()
            elif action == "gsort":              # the roster's order (2.6.05)
                i = SORT_CODES.index(settings["gsort"]) if settings["gsort"] in SORT_CODES else 0
                settings["gsort"] = SORT_CODES[(i + 1) % len(SORT_CODES)]
                save_settings()
                lbl = win["c"].get("gsort")
                if lbl is not None:
                    Kit.set_text(lbl, sort_caption(win["c"]))
                btn = win["c"].get("gsort_btn")
                if btn is not None and win["c"].get("gsort_bare"):   # (2.6.64) the button alone
                    tip = sort_tip(win["c"])
                    safe(lambda: btn.SetTooltip(tip))
                st["page"]["guild"] = 0
                st["next_list"] = 0.0
        if st["rebuild"]:
            if not st["minimized"]:
                st["msg"][settings["tab"]] = read_msg()   # keep what was typed
            build_window()
            return
        # 2.6.81: folded into the Action Bar it still says who comes into view
        # (the setting promises it; it was silent, then told all at once on
        # unfold). Nothing is drawn (refresh returns); with both options off it
        # does nothing, and the first look after that is silent.
        # (2.6.82) the time test first: four passes in five end there
        if st["guild_dirty"]:                    # a read finished on the script's thread
            st["guild_dirty"] = False
            st["next_list"] = 0.0
        now = time.time()
        if now < st["next_list"]:
            return
        folded = st["minimized"] and st["docked"]
        if folded and not (settings["announce"] or settings["left"]):
            st["seen"] = None
            return
        st["next_list"] = now + LIST_EVERY
        read_friends()
        tab = "mini" if st["minimized"] else win["tab"]
        # Only the mobiles the window shows get read in full (API.FindMobile and
        # six property reads each): the rows of the current page, the party's
        # leader and inviter (named in the info lines), the guild members and
        # allies in view (sorted by distance). Every friend gets a presence
        # check only (one FindMobile, or nothing on the Guild tab, whose scan
        # of the mobiles in view already tells), for the "in view" counts and
        # the announcements.
        wanted = set()
        st["view_serials"] = None
        if tab == "mini":
            if not folded:                       # (only the mini bar's text uses it)
                read_party()
        elif tab == "friends":
            shown, _pg = page_of(st["friends"])
            wanted.update(s for s, _ in shown)
        elif tab == "party":
            read_party()
            party = st["party"]
            if party:
                me = player_serial()
                shown, _pg = page_of([s for s in party[3] if s != me])
                wanted.update(shown)
                wanted.add(party[0])
                wanted.add(party[1])
        elif tab == "guild":
            scan_view()
            for s, _n in st["allies"]:
                wanted.add(s)
            gd = st["guild"] or empty_guild()
            view = st["view"]
            for m in gd["members"]:
                s = view.get(mkey(m), 0)
                if s:
                    wanted.add(s)
            # the automatic re-read, while the tab shows
            if (settings["gevery"] and not st["guild_busy"] and now >= st["guild_next"]
                    and now - gd["at"] >= settings["gevery"] * 60):
                start_guild_read()
        if tab in ("guild", "profile"):
            read_profile(tab == "profile")       # (2.6.82) the Guild tab: name and lines only
        mobs = {}
        # (2.6.82) on the Guild tab the members and allies in view get their name
        # and distance from the scan (all the roster's order needs); the health
        # is read for the rows shown only (full_mob, slot 5 None until then)
        kept = st["kept"] if tab == "guild" else None
        for s in wanted:
            if s:
                e = kept.get(s) if kept else None
                if e is not None:
                    mobs[s] = (e[0], 0, 0, e[1], False, None)
                    continue
                d = read_mobile(s)
                if d is not None:
                    mobs[s] = d
        st["mobs"] = mobs
        inview = set()
        rest = []
        for s in st["fserials"]:
            if s in mobs:
                inview.add(s)
            else:
                rest.append(s)
        if tab == "friends" or (tab == "mini" and not folded) or settings["announce"] \
                or settings["left"]:
            inview |= friends_in_view(rest)
        st["inview"] = inview
        announce()
        refresh()


    def _thread_tick():
        """Script thread, right after the client tick: work that waits."""
        while jobs and not st["shutting"]:
            jobs.pop(0)()


    def _stop():
        st["shutting"] = True
        HOST.dock_remove(KEY)
        save_pos()
        # folded into the bar is the host's wish (dock_wanted), not "minimized"
        Kit.save_min(MIN_KEY, st["minimized"] and not st["docked"])
        save_settings()
        st["names_dirty"] = True
        save_names()
        HOST.services.pop("social.note", None)
        close_note()
        save_notes()                             # a note still waiting for thread_tick
        g, win["g"] = win["g"], None
        Kit.dispose(g)


    LOADED_FOR = [0]                      # (2.6.82) the character the build's load was for
    load_settings()
    LOADED_FOR[0] = player_serial()
    st["me_s"] = 0                        # (read again at the start)
    MODULE = {"start": _start, "tick": _tick, "stop": _stop,
              "client_tick": True,          # tick on the client thread: no waits in it
              "thread_tick": _thread_tick,  # waiting work, on the script's thread
              # (2.6.82) the script-thread pass only when a job waits
              "thread_wanted": lambda: bool(jobs),
              "config_height": config_height, "build_config": build_config,
              "poll_config": poll_config, "config_closed": config_closed}
    # ============================= MODULE END ====================================
    return MODULE


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("social", "Social", "Friends, party, guild and your profile in one window",
             _module_social, 0.1,
             category="The world")
else:
    import API
    API.SysMsg("Social is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
