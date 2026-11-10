# Social: a Virtue Assistant module. This file is not a script to run on its own: the mother script
# loads it from the modules folder and runs it inside its own namespace, so API, G, safe, Client,
# Kit, Tz, Typing, Follow, HOST, Journal and the settings window are all provided by the mother.
# Leaving the file out of the folder leaves the module out. Key "social", category "The world".
#
# One window for everything social, on four tabs:
#   Friends: TazUO's own friends list (the one nameplates and the Legion API use), with each
#     friend's health while in view. Add by target, remove with the X, click a row to target,
#     Alt+click to auto-follow. The journal says when a friend comes into view.
#   Party: members with health, invite by target, leave, loot on or off, the client's party
#     window, accept or decline an invite, party chat.
#   Guild: what the server's guild window shows, read into this window: the My Guild page, the
#     whole Guild Roster (every page), plus your own guild line from your tooltip. The guild
#     window is opened hidden for the read and closed again. Members in view get a health bar
#     and distance. Buttons for the guild window, its Diplomacy page, guild and alliance chat.
#   Profile: your name, titles, notoriety, gold, followers and weight, plus buttons for the
#     server's profile scroll, paperdoll, status and the ignore list.
# Notes: Shift+click a row to write a note on that player. Notes are kept by name for the whole
# account, show in the row's tooltip and reach Ultima Tracker through HOST.services.
# The Guild tab's Sort button orders the roster by online, last on, rank or name.
#
# Speed: everything that draws runs on the client thread (client_tick) into a pool of rows and
# writes a label only when its text changed. The jobs that wait (guild window reads, the
# Diplomacy page) run on the script's thread (thread_tick). Mobile and player reads are shared
# per pass, the roster order and info lines are kept until they change, and each gump layout is
# parsed once.
def _module_social():
    """Build the Social module in its own namespace and return its hooks for the mother: start, tick,
    stop, the settings page and the script-thread tick.
    """
    # Module identity and the names of the saved keys. Settings, the minimized flag, the friend
    # names and the guild and roster copies are per character; notes (below) are per account.
    KEY = "social"
    TITLE = "Social"
    SETTINGS_KEY = "Social_settings"
    POS_KEY = "Social_pos"
    MIN_KEY = "Social_min"
    NAMES_KEY = "Social_names"
    GUILD_KEY = "Social_guild"
    ROSTER_KEY = "Social_roster"
    # Item art shown on the Action Bar's tray button for this module.
    TRAY_ICON = 0x1F14
    # Window widths: the Guild tab is wider because the roster has five columns.
    W = 460
    GUILD_W = 600
    # Size of the minimized bar.
    MINI_W, MINI_H = 240, 46
    ROW_H = 24
    # Limits for the rows-per-page setting.
    ROWS_MIN, ROWS_MAX = 4, 16
    DEFAULT_ROWS = 8
    # Tab id and caption pairs, in the order the tab strip shows them.
    TABS = [("friends", "Friends"), ("party", "Party"), ("guild", "Guild"), ("profile", "Profile")]
    TAB_TIPS = {"friends": "Show TazUO's friends list and their health",
                "party": "Show your party: members, invites, loot and chat",
                "guild": "Show your guild: info, roster and chat",
                "profile": "Show your character and the client's windows"}
    # Age text table for Kit.ago: seconds limit, divisor, format. The last row (limit 0) catches
    # everything older. Used for the roster's Last On column.
    SOCIAL_AGO = ((60, 1, "just now"), (3600, 60, "%d min ago"), (86400, 3600, "%d h ago"),
                  (172800, 86400, "%d day ago"), (0, 86400, "%d days ago"))
    # Polling periods in seconds. Mobiles in view are looked at often, the friends list and your own
    # tooltip rarely, since those change slowly.
    LIST_EVERY = 0.25
    FRIENDS_EVERY = 2.0
    PROFILE_EVERY = 1.0
    # Seconds the player has to target a friend or invitee.
    PICK_TIMEOUT = 15
    # Seconds to wait for the server to send the guild window.
    GUMP_WAIT = 4.0
    # Caption of the guild window's Diplomacy button, searched first; the button id is only the
    # fallback when no button carries that caption. 0 as the id means label only.
    DIPLOMACY_LABEL = "Diplomacy"
    DIPLOMACY_BUTTON = 3
    DIPLOMACY_BUTTON_MAX = 9999
    # Column widths of the list rows. The rank column is sized for the longest rank, Emissary.
    NAME_W = 150
    STATUS_W = 90
    RANK_W = 64
    # Shortest the chat entry field may get when the window is narrow.
    MSG_W_MIN = 120
    # Characters of an unrecognised gump's layout copied to the journal, so it can be reported.
    DUMP_CHARS = 200
    # Captions of the two guild window pages, matching the clilocs in the table below.
    INFO_TAB, ROSTER_TAB = "My Guild", "Guild Roster"
    # Button ids of the two tab buttons, used when the captions cannot be found.
    INFO_BUTTON, ROSTER_BUTTON = 1, 2
    # Reply button id for the roster's next page.
    FORWARD_BUTTON = 7
    # Most roster pages read in one go; this stops a gump that never ends from keeping the reader busy.
    ROSTER_PAGES_MAX = 40
    # Members kept in the saved roster copy, to bound the size of the saved value.
    ROSTER_KEEP = 300
    # Automatic guild re-read interval in minutes: default and the settings field's upper bound.
    GUILD_EVERY_MIN = 5
    GUILD_EVERY_MAX = 120
    # Seconds before another automatic guild read after a failure; the delay doubles with each
    # failure in a row up to the maximum.
    GUILD_RETRY = 60
    GUILD_RETRY_MAX = 600
    # The create-a-guild window is sent instead of the guild window when you are in no guild. These
    # clilocs and texts recognise it so the tab can say so instead of failing.
    NOT_GUILDED_CLILOCS = (1062939, 1062940, 1063035)
    NOT_GUILDED = ("not a member of any guild", "abbreviation:")
    # Cliloc texts the guild window uses, built in so captions read right even when the client's
    # cliloc lookup is unavailable; that lookup is only tried for numbers not listed here.
    CLILOCS = {1062954: "Guild Name", 1063025: "Alliance", 1063084: "Guild Faction",
               1062955: "Name", 1062956: "Rank", 1062952: "Last On",
               1062953: "Guild Title", 1063015: "Online", 1062959: "Leader",
               1062960: "Warlord", 1062961: "Emissary", 1062962: "Member",
               1062963: "Ronin", 1062974: ROSTER_TAB, 1063014: INFO_TAB,
               1062978: DIPLOMACY_LABEL, 1062992: "Invite Player", 3006115: "Resign"}
    # Tab captions as clilocs, as the same numbers written in a layout, and as lower-case text. A
    # layout holding none of them cannot be a guild window page and is not parsed.
    TAB_CLILOCS = (1063014, 1062974, 1062978)
    TAB_MARKS = ("1063014", "1062974", "1062978")
    TAB_CAPS_LOW = (INFO_TAB.lower(), ROSTER_TAB.lower(), DIPLOMACY_LABEL.lower())
    # Notoriety numbers to names: one table, not a dict built per call.
    NOTO_NAMES = ("Unknown", "Innocent", "Ally", "Gray", "Criminal", "Enemy", "Murderer", "Invulnerable")
    # Separators of the saved guild and roster copies. FS and RS are the old control characters,
    # still read from old saves. New saves use the printable PF and PR with ESC escaping all three,
    # because any store carries printable text unchanged.
    FS, RS = "\x1f", "\x1e"
    PF, PR, ESC = "|", ";", "~"
    # Notes on players are saved per account, as name|note records split by semicolons. They are
    # capped in count and length so the saved value stays small.
    NOTES_KEY = "Social_notes"
    NOTES_MAX = 500
    NOTE_CHARS = 200
    # Variable that remembers where the note window sits.
    NOTE_POS_KEY = "Social_note_pos"
    NOTE_W = 440
    # Roster sort modes: code, button caption, short name. The chosen code is remembered.
    SORTS = [("online", "Sort: online", "Online"), ("laston", "Sort: last on", "Last on"),
             ("rank", "Sort: rank", "Rank"), ("name", "Sort: name", "Name")]
    SORT_CODES = [x[0] for x in SORTS]
    # Ranks, top first, each with the other spellings it may arrive as (the leader cliloc reads
    # Guild Leader in the client's table but Leader in the table above). A rank not listed sorts
    # after these.
    RANK_ORDER = (("leader", "guild leader"), ("warlord",), ("emissary",), ("member",), ("ronin",))
    # The roster's Last On column read as a date. Year first is the form the server uses; otherwise
    # the part that cannot be a month decides day or month order; the remaining ambiguous forms are
    # month first for a slash and day first for a dot (unchecked in game).
    DATE_RE = re.compile(r"(\d{1,4})\s*([-/.])\s*(\d{1,2})\s*[-/.]\s*(\d{1,4})")
    # Defaults for every setting. The saved form is a pipe-separated list in a fixed key order, so
    # new keys are only ever added at the end.
    settings = {"tab": "friends", "rows": DEFAULT_ROWS, "bars": True, "announce": True,
                "gevery": GUILD_EVERY_MIN, "ghide": True, "dbutton": DIPLOMACY_BUTTON, "left": False, "gsort": "online"}
    DEFAULTS = dict(settings)
    # Run state shared by the whole module, none of it saved except where a key says so: minimized
    # and docked flags, queued client-thread work, lists read from the client, the party read, the
    # parsed profile, last typed chat text per tab, guild gump ids, and caches.
    st = {"shutting": False, "minimized": False, "docked": False, "queue": [], "friends": [], "names_dirty": False,
          "party": None, "profile": None, "msg": {}, "gids": {}, "me_s": 0, "fserials": []}
    # The main window: its gump, the control table and the pool store used to reuse its rows.
    win = {"g": None, "c": {}, "store": ({}, {})}
    # Kit.basics gives the standard clean-up list, the client-thread work queue and the journal
    # printer, all tied to this module's state.
    cleanup, queue, say = Kit.basics(st, TITLE)
    # Work that waits for the script thread, drained by thread_tick.
    jobs = []
    # Notes by lower-case name, each value (name as written, text).
    NOTES = {}
    # dirty: a save is pending. ver: bumped on every change so row tooltips know to refresh. chg:
    # changes not yet merged into the saved text (None marks a deletion).
    notes_st = {"dirty": False, "ver": 0, "chg": {}}
    # The note window: only one is open at a time.
    ed = {"g": None, "c": {}, "store": ({}, {}), "name": ""}
    M = Kit.MARGIN

    def load_settings():
        """Read the saved settings, names, guild copy and notes into memory. Called once at start.

        Settings are a pipe-separated list; each group of keys was added after the earlier ones, so a
        shorter older value still loads and the missing keys keep their defaults. Out-of-range numbers
        are clamped.
        """
        p = Kit.get_var(SETTINGS_KEY).split("|")

        def num(i, lo, hi, dflt):
            """Read field i of the saved list as an integer clamped to lo..hi, or dflt when it is missing
            or not a number.
            """
            try:
                return max(lo, min(hi, int(p[i])))
            except Exception:
                return dflt

        # Keys come in groups by length of the saved list, so a value saved by an older build still loads.
        if len(p) >= 4:
            if p[0] in TAB_TIPS:
                settings["tab"] = p[0]
            settings.update({"rows": num(1, ROWS_MIN, ROWS_MAX, DEFAULT_ROWS), "bars": p[2] == "1",
                             "announce": p[3] == "1"})
        if len(p) >= 6:
            settings.update({"gevery": num(4, 0, GUILD_EVERY_MAX, GUILD_EVERY_MIN), "ghide": p[5] == "1"})
        if len(p) >= 8:
            settings.update({"dbutton": num(6, 0, DIPLOMACY_BUTTON_MAX, DIPLOMACY_BUTTON), "left": p[7] == "1"})
        if len(p) >= 9 and p[8] in SORT_CODES:
            settings["gsort"] = p[8]
        # Friend serial to last seen name, kept as a fallback for friends not in view.
        names = {}
        for part in Kit.get_var(NAMES_KEY).split("|"):
            if "=" in part:
                s, n = part.split("=", 1)
                with Kit.quiet:
                    names[int(s)] = n
        st["names"] = names
        load_guild()
        load_notes()

    def save_settings():
        """Save the settings as a pipe-separated list in the fixed key order read by load_settings."""
        Kit.put_var(SETTINGS_KEY, "|".join([str(int(settings[k])) if isinstance(settings[k], bool) else str(settings[k])
                                            for k in ("tab", "rows", "bars", "announce", "gevery", "ghide", "dbutton",
                                                      "left", "gsort")]))

    def save_names():
        """Save the friend names as serial=name pairs, only when they changed. Keeps the 200 highest
        serials so the saved value stays bounded. Pipe and equals signs in a name are replaced.
        """
        if not st["names_dirty"]:
            return
        st["names_dirty"] = False
        items = sorted(st["names"].items())[-200:]
        Kit.put_var(NAMES_KEY, "|".join("%d=%s" % (s, n.replace("|", "/").replace("=", "-")) for s, n in items))

    def empty_guild():
        """Return a blank guild record: nothing read yet, assumed to be in a guild until a read says not."""
        return {"ok": False, "in_guild": True, "name": "", "alliance": "", "faction": "",
                "charter": "", "website": "", "members": [], "at": 0.0, "note": ""}

    def clean(s):
        """Make text safe to save: control separators and line breaks become spaces, and the three
        printable separators are escaped with ESC. The result holds no PF, PR or raw ESC.
        """
        s = str(s or "").replace(FS, " ").replace(RS, " ").replace("\n", " ").strip()
        return s.replace(ESC, ESC + "t").replace(PF, ESC + "p").replace(PR, ESC + "s")

    def unclean(s):
        """Undo clean: restore the escaped separators and ESC."""
        return str(s or "").replace(ESC + "p", PF).replace(ESC + "s", PR).replace(ESC + "t", ESC)

    def split_saved(raw, old_sep, new_sep):
        """Split a saved text into fields. An old save is recognised by its control separators and split
        by old_sep; a new one is split by new_sep and unescaped.
        """
        if FS in raw or RS in raw:
            return raw.split(old_sep)
        return [unclean(p) for p in raw.split(new_sep)]

    def load_guild():
        """Rebuild the guild record and roster from the saved copies. The record counts as read (ok) only
        when its timestamp is set; a missing or damaged copy gives the empty record.
        """
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
        # The old form used RS between records, the new one PR; pick by what the text holds.
        for rec in raw.split(RS if FS in raw or RS in raw else PR):
            f = split_saved(rec, FS, PF)
            # A saved member is never marked as you: that flag is set again when the roster is shown.
            if len(f) >= 5 and f[0]:
                members.append({"name": f[0], "rank": f[1], "laston": f[2], "title": f[3],
                                "online": f[4] == "1", "me": False})
        gd["members"] = members
        st["guild"] = gd

    def save_guild():
        """Save the guild record and the first ROSTER_KEEP roster members in the printable form."""
        gd = st["guild"] or empty_guild()
        Kit.put_var(GUILD_KEY, PF.join([clean(gd[k]) for k in ("name", "alliance", "faction", "charter", "website")]
                                       + ["%d" % int(gd["at"] or 0), "1" if gd["in_guild"] else "0"]))
        Kit.put_var(ROSTER_KEY, PR.join(PF.join([clean(m[k]) for k in ("name", "rank", "laston", "title")]
                                                + ["1" if m["online"] else "0"]) for m in gd["members"][:ROSTER_KEEP]))

    def load_notes():
        """Load the notes from the account-wide saved value; an unreadable value gives no notes."""
        try:
            raw = str(API.GetPersistentVar(NOTES_KEY, "", API.PersistentVar.Account) or "")
        except Exception:
            raw = ""
        notes_from(raw)

    def notes_from(raw):
        """Rebuild NOTES from the saved text, then reapply the changes not yet saved (chg) so a note typed
        while a save was pending is not lost. Bumps ver so tooltips refresh.
        """
        new = {}
        for rec in raw.split(PR):
            f = [unclean(x).strip() for x in rec.split(PF)]
            if len(f) >= 2 and f[0] and f[1] and len(new) < NOTES_MAX:
                new[f[0].lower()] = (f[0], f[1])
        for k, v in list(notes_st["chg"].items()):
            if v is None:
                new.pop(k, None)
            else:
                new[k] = v
        for k in [k for k in NOTES if k not in new]:
            del NOTES[k]
        NOTES.update(new)
        notes_st["ver"] += 1

    def save_notes():
        """Merge the pending note changes into the account-wide saved text and save it. Runs on the
        script thread as a job. Merging into what is saved now, record by record, keeps notes another
        character of the account wrote meanwhile. On failure the dirty flag is set again so the next
        change retries.
        """
        if not notes_st["dirty"]:
            return
        notes_st["dirty"] = False
        chg = dict(notes_st["chg"])
        entries = dict((k, None if v is None else PF.join([clean(v[0]), clean(v[1])])) for k, v in chg.items())
        try:
            raw = str(API.GetPersistentVar(NOTES_KEY, "", API.PersistentVar.Account) or "")
            data = Kit.merge_text(raw, entries, lambda rec: unclean(rec.split(PF)[0]).strip().lower(), PR)[0]
            API.SavePersistentVar(NOTES_KEY, data, API.PersistentVar.Account)
        except Exception as ex:
            notes_st["dirty"] = True
            say("couldn't save the notes (%s); they're saved with the next change." % ex, Kit.HUE_BAD)
            return
        # Drop each change that is now saved, unless it was changed again during the save.
        for k, v in chg.items():
            if notes_st["chg"].get(k, 0) == v:
                notes_st["chg"].pop(k, None)
        notes_from(data)

    def note_of(player_name):
        """Return the note text on a player by name, case-insensitive, or an empty string."""
        e = NOTES.get(str(player_name or "").strip().lower())
        return e[1] if e else ""

    def notes_changed():
        """Mark the notes as changed and queue a save."""
        notes_st["dirty"] = True
        notes_st["ver"] += 1
        jobs.append(save_notes)

    def set_note(name, text):
        """Set or delete the note on a player. An empty text deletes it. Returns True when the request was
        handled and False when it was refused (no name, or the note count is at its limit).
        """
        name = " ".join(str(name or "").split())
        text = " ".join(str(text or "").split())[:NOTE_CHARS]
        if not name:
            say("type a name first.")
            return False
        k = name.lower()
        if not text:
            if NOTES.pop(k, None) is not None:
                notes_st["chg"][k] = None
                say("note on %s deleted." % name)
                notes_changed()
            return True
        if k not in NOTES and len(NOTES) >= NOTES_MAX:
            say("at most %d notes; delete one first." % NOTES_MAX, Kit.HUE_BAD)
            return False
        NOTES[k] = notes_st["chg"][k] = (name, text)
        notes_changed()
        say("note on %s saved." % name, Kit.HUE_GOOD)
        return True

    # Kit.fit cuts text to a pixel width using letter sums, so no label is created per trial width.
    fit = Kit.fit

    def shift_held():
        """Return True while a Shift key is held, read from the client."""
        return bool(Client.key_held("shift"))

    def set_vis(part, on):
        """Show or hide a control part and remember it. part is [control, visible]; the client is only
        touched when the state changes.
        """
        if part[0] is not None and part[1] != on:
            part[1] = on
            Kit.set(part[0], "IsVisible", on)

    def noto_name(n):
        """Return the name of a notoriety value. Unknown numbers give the text after the last dot of
        their string form, and None gives an empty string.
        """
        if n is None:
            return ""
        try:
            i = int(n)
        except Exception:
            i = -1
        return NOTO_NAMES[i] if 0 <= i < 8 else str(n).split(".")[-1]

    def player_serial():
        """Return your own serial, read once and cached; read again while it is still 0."""
        s = st["me_s"]
        if not s:
            try:
                s = int(API.Player.Serial or 0)
            except Exception:
                s = 0
            st["me_s"] = s
        return s

    def player_name():
        """Return your own name: the one from the parsed profile when there is one, else the player's."""
        prof = st["profile"]
        if prof and prof[0]:
            return prof[0]
        try:
            return str(API.Player.Name or "")
        except Exception:
            return ""

    def ago(t):
        """Return how long ago t (epoch seconds) was, as text, or never for 0."""
        return "never" if not t else Kit.ago(time.time() - t, SOCIAL_AGO)

    class CL(object):
        """Reach into the client's own classes by reflection: the world, GameActions, UIManager and
        FriendsListManager. Everything is looked up lazily by find, and every call that touches the
        client's data runs on the client thread through on_main. Static members only; error holds the
        last reason a lookup or call failed.
        """
        looked = False
        error = ""
        world = None
        GA = None
        UIM = None
        FLM = None

        @staticmethod
        def call(obj, name, args=(), t=None):
            """Call a method on obj (or on the client class t) by name with the given arguments, through Tz."""
            return Tz.call(obj, name, args, t, True)

        @staticmethod
        def find():
            """Look up the client classes once. Sets error when the world or GameActions cannot be found; the
            world comes from the API object first and from the client's static Game otherwise.
            """
            if CL.looked:
                return
            CL.looked = True
            try:
                asm = API.GetType().Assembly
            except Exception as ex:
                CL.error = "no client access (%s)" % ex
                return
            world = Typing._get(API, "World")
            if world is None:
                game = Typing._get(None, "Game", Client._type("ClassicUO.Client"))
                world = Typing._get(Typing._get(game, "UO"), "World")
            CL.world = world
            CL.GA = Client._type("ClassicUO.Game.GameActions")
            CL.UIM = Client._type("ClassicUO.Game.Managers.UIManager")
            CL.FLM = Client._type("ClassicUO.Game.Managers.FriendsListManager")
            if world is None:
                CL.error = "client World not found"
            elif CL.GA is None:
                CL.error = "GameActions not found"

        @staticmethod
        def on_main(fn, need=True):
            """Run fn on the client thread and return its value, or None (with error set) when that fails.
            With need False nothing runs, so callers can pass a precondition inline.
            """
            if not need:
                return None
            how, value = Client.on_main_ex(fn)
            if how == "ok":
                return value
            CL.error = Client.error or "can't run on the client thread"
            return None

        @staticmethod
        def game_action(name, args=(), with_world=True):
            """Call a static GameActions method on the client thread. When with_world is set the world is
            passed as the first argument. Returns True when the call ran.
            """
            full = ([CL.world] if with_world else []) + list(args)

            def run():
                """Client-thread body of game_action."""
                CL.call(None, name, full, CL.GA)
                return True

            return bool(CL.on_main(run, CL.GA is not None))

        @staticmethod
        def friends():
            """Read TazUO's friends list as a list of (serial, name), or None when the manager is missing."""
            def run():
                """Client-thread body of friends."""
                inst = Typing._get(None, "Instance", CL.FLM)
                if inst is None:
                    return None
                out = []
                for f in (CL.call(inst, "GetFriends") or []):
                    ft = f.GetType()
                    out.append((int(Typing._get(f, "Serial", ft) or 0), str(Typing._get(f, "Name", ft) or "")))
                return out

            return CL.on_main(run, CL.FLM is not None)

        @staticmethod
        def party():
            """Read the client's party as (leader serial, inviter serial, can loot, [member serials]) or None
            when there is none. You are left out of the member list.
            """
            world = CL.world

            def run():
                """Client-thread body of party."""
                party = Typing._get(world, "Party")
                if party is None:
                    return None
                leader = int(Typing._get(party, "Leader") or 0)
                inviter = int(Typing._get(party, "Inviter") or 0)
                loot = bool(Typing._get(party, "CanLoot") or False)
                pl = Typing._get(world, "Player")
                me = int(Typing._get(pl, "Serial") or 0) if pl is not None else 0
                members = []
                for m in (Typing._get(party, "Members") or []):
                    if m is not None:
                        s = int(Typing._get(m, "Serial") or 0)
                        if s and s != me:
                            members.append(s)
                return (leader, inviter, loot, members)

            return CL.on_main(run, world is not None)

        @staticmethod
        def open_ignore_list():
            """Open the client's own ignore list window, or bring it to the front when it is already open.
            Returns True when it worked.
            """
            def run():
                """Client-thread body of open_ignore_list. The window class takes the world as its only
                constructor argument.
                """
                import System
                if CL.bring_to_front("IgnoreManagerGump"):
                    return True
                t = Client._type("ClassicUO.Game.UI.Gumps.IgnoreManagerGump")
                if t is None:
                    raise Exception("IgnoreManagerGump not found")
                g = System.Activator.CreateInstance(t, System.Array[object]([CL.world]))
                CL.call(None, "Add", [g], CL.UIM)
                return True

            return bool(CL.on_main(run, CL.world is not None and CL.UIM is not None))

        @staticmethod
        def bring_to_front(type_name):
            """Bring the client gump of the named class to the top if one is open. Returns True when found.
            Client thread only.
            """
            for g in Typing._get(None, "Gumps", CL.UIM) or ():
                if g is not None and g.GetType().Name == type_name and not g.IsDisposed:
                    CL.call(g, "BringOnTop")
                    return True
            return False

        @staticmethod
        def find_server_gump(test):
            """Find the open server gump whose layout text satisfies test. Returns (server serial, layout
            text), or (0, "") when none does. Gumps without layout text are skipped.
            """
            def run():
                """Client-thread body of find_server_gump."""
                for g in Typing._get(None, "Gumps", CL.UIM) or ():
                    if g is None or g.IsDisposed:
                        continue
                    # One odd gump must not stop the search of the rest.
                    try:
                        raw = Typing._get(g, "PacketGumpText")
                        if not raw:
                            continue
                        raw = str(raw)
                        if test(raw):
                            return int(Typing._get(g, "ServerSerial") or 0), raw
                    except Exception:
                        continue
                return 0, ""

            r = CL.on_main(run, CL.UIM is not None)
            return r if r else (0, "")

        @staticmethod
        def press_labelled(gump, label):
            """In a server gump, press the button nearest the text label. A text equal to the label
            (case-insensitive) is preferred, else the first text containing it, so a charter that mentions
            guild roster cannot steal the match. Returns False when there is no such text, no button, or
            the nearest button is further than 80 pixels. Runs on the client thread through on_main.
            """
            # A wrapper gump holds the client's real control in its Gump member; use that when it is there.
            inner = safe(lambda: gump.Gump)
            gump = inner if inner is not None else gump
            want = label.lower().strip()

            def run():
                """Client-thread body of press_labelled: collect text and button positions, then click the button
                nearest the chosen text.
                """
                import System
                exact, texts, buttons = [], [], []

                def at(ch):
                    """Screen position (x, y) of a control."""
                    x = int(Typing._get(ch, "ScreenCoordinateX") or 0)
                    return x, int(Typing._get(ch, "ScreenCoordinateY") or 0)

                def walk(ctrl):
                    """Collect every button (x, y, id) and every text containing the label, below ctrl, depth first."""
                    for ch in list(Typing._get(ctrl, "Children") or []):
                        if ch is None:
                            continue
                        tn = ch.GetType().Name
                        if tn == "Button":
                            buttons.append(at(ch) + (int(Typing._get(ch, "ButtonID") or 0),))
                        else:
                            txt = Typing._get(ch, "Text")
                            low = Kit.strip_html(txt).lower() if txt else ""
                            if low and want in low:
                                (exact if low == want else texts).append(at(ch))
                        walk(ch)

                walk(gump)
                texts = exact or texts
                if not texts or not buttons:
                    return False
                tx, ty = texts[0]

                def off(b):
                    """Distance of button b from the chosen text, as a sum of the x and y differences."""
                    return abs(b[0] - tx) + abs(b[1] - ty)

                best = min(buttons, key=off)
                if off(best) > 80:
                    return False
                # The id is passed as a real Int32 so the reflection call finds the click method's int parameter.
                CL.call(gump, "OnButtonClick", [System.Int32(best[2])])
                return True

            return bool(CL.on_main(run))

    def read_mobile(serial):
        """Row data of a mobile in view as (name, hits, hits max, distance, dead, True), or None when it
        is not in view or cannot be read. The last slot says the row data is whole.
        """
        # Mobiles come through the mother's per-pass reads: one another module or scan_view already looked
        # at in this client pass costs nothing again.
        m = HOST.mobile(serial)
        if m is None:
            return None
        try:
            return (str(m.Name or ""), int(m.Hits or 0), int(m.HitsMax or 0), int(m.Distance), bool(m.IsDead), True)
        except Exception:
            return None

    def full_mob(serial):
        """This pass's row data for serial, reading the health now when only its name and distance were
        kept by scan_view. Returns None when the mobile is not in view.
        """
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
        """Read the friends list, names included, at most every FRIENDS_EVERY seconds, into st friends
        (sorted, unnamed last), their serials and the saved names. Queues a names save when a name
        is new or changed. Client tick.
        """
        now = time.time()
        if now < st["next_friends"]:
            return
        st["next_friends"] = now + FRIENDS_EVERY
        # TazUO's own list gives names; if it cannot be read the API's serial list is used and names come
        # from the saved ones and from view.
        lst = CL.friends()
        named = lst is not None
        if lst is None:
            lst = [(int(s), st["names"].get(int(s), "")) for s in API.GetAllFriends() or ()]
        me = player_serial()
        # When the client gave every name and the list is as it was last time, nothing is rebuilt or
        # sorted again. Lists with unnamed friends are never cached, so a name is picked up once the
        # friend is in view.
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
            if not name:
                unnamed = True
                d = st["mobs"].get(serial)
                name = (d[0] if d and d[0] else "") or st["names"].get(serial, "")
            if name and st["names"].get(serial) != name:
                st["names"][serial] = name
                st["names_dirty"] = True
            # A friend with no known name shows its serial in hex.
            out.append((serial, name or ("0x%08X" % serial)))
        # Sort by name, with the unnamed (hex) ones last.
        out.sort(key=lambda e: (e[1].startswith("0x"), e[1].lower()))
        st["friends"] = out
        st["fserials"] = [s for s, _n in out]
        st["friends_raw"] = None if unnamed else raw_key
        if st["names_dirty"]:
            jobs.append(save_names)

    def read_party():
        """Read your party into st party: the client's own data, else the API's leader and member lists.
        None when you are in none.
        """
        p = CL.party()
        if p is None:
            leader = int(API.GetPartyLeader() or 0)
            p = (leader, 0, False, [int(s) for s in API.GetPartyMemberSerials() or ()]) if leader else None
        st["party"] = p

    def in_party(p):
        """True when p, a party read, is a real party. The client keeps a party object (leader 0, no
        members) when you are in none, so only a leader or listed members count.
        """
        return bool(p) and bool(p[0] or p[3])

    def read_profile(full=True):
        """Read your own name, tooltip lines and, when full, the Profile tab's values, at most every
        PROFILE_EVERY seconds. The Guild tab needs only the name and lines (full False); a profile
        read that way is read in full at once when the Profile tab asks. st profile becomes None
        when you are not in the world.

        Full form: (name, lines, notoriety, gold, followers, followers max, weight, weight max, war
        mode, hidden).
        """
        now = time.time()
        if now < st["next_profile"] and not (full and st["prof_part"]):
            return
        st["next_profile"] = now + PROFILE_EVERY
        p = HOST.me()
        if p is None:
            st["profile"] = None
            st["prof_part"] = False
            return
        try:
            name = str(p.Name or "")
            try:
                # The tooltip's text lines, which hold the guild line; a client without the call gives no lines.
                nap = p.raw.NameAndProps(False)
            except Exception:
                nap = ""
            lines = [l.strip() for l in str(nap or "").replace("\r", "").split("\n") if l.strip()]
            if not full:
                old = st["profile"]
                # A partial read keeps the old values after the name and lines.
                rest = old[2:] if old else ("", 0, 0, 0, 0, 0, False, False)
                st["profile"] = (name, lines) + tuple(rest)
                st["prof_part"] = True
                return
            prof = (name, lines, noto_name(p.Notoriety), int(p.Gold or 0), int(p.Followers or 0),
                    int(p.FollowersMax or 0), int(p.Weight or 0), int(p.WeightMax or 0), bool(p.InWarMode),
                    bool(p.IsHidden))
        except Exception:
            prof = None
        st["profile"] = prof
        st["prof_part"] = False

    def scan_view():
        """One pass over the mobiles in view: players by lower-case name (for the roster), the Ally
        (green) ones as a list, the set of every serial in view, and name and distance of each player
        kept for the rows.

        Pets and NPCs are left out so a pet or vendor sharing a member's name cannot stand in for the
        member: only humans and gargoyles count, and invulnerable ones are skipped.
        """
        me = player_serial()
        view, allies, serials, kept = {}, [], set(), {}
        for m in HOST.mobiles():
            try:
                s = int(m.Serial)
                if not s or s == me:
                    continue
                serials.add(s)
                # Human test first: most mobiles in a hunting area are not players, so they cost two reads, not
                # four.
                if not (m.IsHuman or m.IsGargoyle):
                    continue
                n = m.Notoriety
                ni = int(n) if n is not None else -1
                # Notoriety 7 is invulnerable (vendors, guards).
                if ni == 7:
                    continue
                name = str(m.Name or "")
                if name:
                    view[name.lower()] = s
                # Notoriety 2 is ally.
                if ni == 2:
                    allies.append((s, name))
                kept[s] = (name, int(m.Distance))
            except Exception:
                continue
        st["view"], st["allies"], st["view_serials"], st["kept"] = view, allies, serials, kept

    def friends_in_view(serials):
        """Return which of the friend serials are in view this pass. Uses the serials scan_view made when
        it ran, else one lookup per friend or, with many friends, one shared scan. Presence only: no
        properties are read here.
        """
        known = st["view_serials"]
        if known is None and len(serials) > FRIENDS_SCAN:
            try:
                known = {int(m.Serial) for m in HOST.mobiles()}
            except Exception:
                known = None
        if known is not None:
            return known.intersection(serials)
        return {s for s in serials if s and HOST.mobile(s) is not None}

    # Above this many friends one shared scan is cheaper than one lookup per friend.
    FRIENDS_SCAN = 10

    def last_two(fn):
        """Decorator: remember the last two inputs and results of fn. The same layout seen again, which
        is the usual case while polling a gump that has not changed, reuses its parse. Results must
        never be changed by their users. Entries are replaced whole, so a read from another thread
        sees either the old or the new one.
        """
        slots = [None, None]

        def run(raw):
            """Return the cached result for raw, else call fn and keep it as the newest of two."""
            for e in slots:
                # Identity first: the same string object is the common case and costs no comparison.
                if e is not None and (e[0] is raw or e[0] == raw):
                    return e[1]
            out = fn(raw)
            slots[1] = slots[0]
            slots[0] = (raw, out)
            return out

        return run

    @last_two
    def gump_cells(raw):
        """Parse a gump layout into text cells and buttons, with the cliloc table of this module."""
        return Kit.gump_cells(raw, CLILOCS)

    @last_two
    def classify(raw):
        """Say what a guild window layout is: roster for the Guild Roster page (it carries the column
        headers), guild for the other pages (they carry the tab captions), noguild for the
        create-a-guild window, else None.
        """
        cells = gump_cells(raw)[0]
        if not cells:
            return None
        texts = [c["text"].lower() for c in cells]
        clilocs = [c["cliloc"] for c in cells]
        if any(cl in TAB_CLILOCS for cl in clilocs) or ROSTER_TAB.lower() in texts:
            if (1062955 in clilocs and 1062956 in clilocs) or ("rank" in texts and (
                    "last on" in texts or "name" in texts)):
                return "roster"
            return "guild"
        # Joined with a character no text holds, so a phrase cannot match across two cells.
        joined = "\x00".join(texts)
        if any(cl in NOT_GUILDED_CLILOCS for cl in clilocs) or any(w in joined for w in NOT_GUILDED):
            return "noguild"

    def may_be_guild(raw):
        """Cheap test before classify: every guild window page carries a tab cliloc or the roster caption
        in its layout.
        """
        return any(t in raw for t in TAB_MARKS) or "roster" in raw.lower()

    def bands(cells, tol=6):
        """Group cells into rows by y, within tol pixels of the row's first cell, top to bottom, each row
        sorted by x.
        """
        out = []
        for c in sorted(cells, key=lambda c: (c["y"], c["x"])):
            if out and abs(c["y"] - out[-1][0]) <= tol:
                out[-1][1].append(c)
            else:
                out.append([c["y"], [c]])
        return [sorted(row, key=lambda c: c["x"]) for _, row in out]

    def parse_info(raw):
        """Read the My Guild page: name, alliance, faction, charter and website. The charter and website
        are the two wide cells with a background; a not yet set text counts as empty.
        """
        cells, _ = gump_cells(raw)
        cells = [c for c in cells if c["cliloc"] not in TAB_CLILOCS]

        def right_of(cliloc):
            """The text of the cell nearest to the right of the label with this cliloc, on the same row, or
            an empty string.
            """
            label = CLILOCS[cliloc].lower()
            lab = next((c for c in cells if c["cliloc"] == cliloc or c["text"].lower() == label), None)
            if lab is None:
                return ""
            near = [c for c in cells if abs(c["y"] - lab["y"]) <= 6 and c["x"] > lab["x"]]
            return min(near, key=lambda c: c["x"])["text"] if near else ""

        out = {"name": right_of(1062954), "alliance": right_of(1063025), "faction": right_of(1063084),
               "charter": "", "website": ""}
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
        """Read one Guild Roster page: returns ([member dicts], whether a next page exists). The header
        row (Name, Rank, Last On, Guild Title) gives the columns; each later row is a member, its
        cells assigned to the nearest header column within 30 pixels.
        """
        cells, buttons = gump_cells(raw)
        # Left out: the tab captions, which sit at the top of every page.
        cells = [c for c in cells if c["cliloc"] not in TAB_CLILOCS and c["text"].lower() not in TAB_CAPS_LOW]
        rows = bands(cells)
        header = None
        for row in rows:
            texts = [c["text"].lower() for c in row]
            if len(row) >= 3 and ("name" in texts or "rank" in texts or "last on" in texts
                                  or any(c["cliloc"] in (1062955, 1062956, 1062952, 1062953) for c in row)):
                header = row
                break
        if header is None:
            return [], False
        cols = [c["x"] for c in header]
        names = [c["text"].lower() for c in header]
        idx = {}
        # Which header column holds which field. Last On also answers to Online, the header some
        # pages use.
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
            # Trailing marks the roster adds to a name are not part of it.
            if name.endswith(" *"):
                name = name[:-2]
            name = name.strip()
            if name.endswith(" VvV"):
                name = name[:-4].strip()
            if not name:
                continue
            raw_name = nc["raw"].lower()
            col = [got[idx[k]]["text"] if k in idx and idx[k] in got else "" for k in ("rank", "laston", "title")]
            # Online is read from the text and from the name's colour in the layout; the green colour also
            # marks your own line.
            online = col[1].lower() == "online" or "#000066" in raw_name or "#006600" in raw_name
            members.append({"name": name, "rank": col[0], "laston": col[1], "title": col[2], "online": online,
                            "me": "#006600" in raw_name})
        # The Next page reply button exists only while more pages follow.
        more = any(b[2] == FORWARD_BUTTON for b in buttons)
        return members, more

    def _last_gump_run():
        """Client-thread body of last_gump: the last server gump's id and layout text in one hop."""
        gid = int(API.HasGump() or 0)
        if not gid:
            return 0, ""
        try:
            return gid, str(API.GetGump(gid).PacketGumpText or "")
        except Exception:
            return gid, ""

    def last_gump():
        """The last server gump as (id, layout), or (0, "") when there is none. One client hop instead of
        three, each of which would wait a frame on the script thread.
        """
        return safe(lambda: Kit.on_client(_last_gump_run)) or (0, "")

    def guild_test(raw):
        """True when raw is a guild window page of any kind."""
        return may_be_guild(raw) and classify(raw) in ("guild", "roster")

    def hide_next(gid=0):
        """Make the next server gump arrive invisible (TazUO's ConfigNextGump), when the setting says so,
        so the guild window never flashes on screen. gid 0 means whichever gump comes. Also announces
        the gump through the gump.expect service, when there is one, for the length of the wait.
        """
        exp = HOST.services.get("gump.expect")
        if exp is not None and gid:
            exp(gid, GUMP_WAIT + 1.0)
        if settings["ghide"] and gid:
            API.ConfigNextGump(serial=gid, isVisible=False)

    def reset_hide():
        """Cancel a pending hide-next-gump request."""
        API.ConfigNextGump()

    def unknown_gump(had):
        """After the guild window did not come: dump the gump that did come, if any, to the journal (its
        first DUMP_CHARS of layout) so an unrecognised layout can be diagnosed. Returns the failure
        note.
        """
        gid, raw = last_gump()
        if not gid or gid == had:
            return "the guild window didn't come"
        dump = " ".join(raw.split())[:DUMP_CHARS] if raw else "(empty layout)"
        say("gump 0x%08X came instead of the guild window (left open); it begins: %s." % (gid, dump))
        return "the guild window didn't come (another gump did)"

    def wait_gump(check):
        """Poll the last server gump until check(layout) gives a true result. Returns (id, layout, result),
        or (0, "", None) on timeout or script stop. Runs on the script thread.
        """
        deadline = time.time() + GUMP_WAIT
        while time.time() < deadline and not st["shutting"]:
            # One hop per look, not three waits.
            gid, raw = last_gump()
            r = gid and raw and check(raw)
            if r:
                return gid, raw, r
            # HOST.idle sleeps in short steps and says False once the script is stopping.
            if not HOST.idle(0.15):
                break
        return 0, "", None

    def press(gid, label, button):
        """Press the tab of a guild window by its caption, else by its known button id. A button id of 0
        means caption only, because replying with button 0 would close the window.
        """
        gump = safe(lambda: API.GetGump(gid))
        # Kit.client_control gives the client's own control when gump is only a wrapper.
        if gump is not None and CL.press_labelled(Kit.client_control(gump) or gump, label):
            return True
        return bool(button) and bool(API.ReplyGump(button, gid))

    def guild_job():
        """Script-thread job: open the guild window (hidden), read the My Guild page, go to Guild Roster
        and read every page, then close it. Always resets the hide request and closes a window we
        opened hidden. A failed read keeps what was known, backs the automatic retry off (1, 2, 4
        minutes up to GUILD_RETRY_MAX) and says so once until the message changes. A good read is
        saved.
        """
        st["guild_busy"] = True
        st["guild_pages"] = 0
        old = st["guild"] or empty_guild()
        gd = old
        try:
            gd = read_guild_window(old)
        except Exception as ex:
            gd = empty_guild()
            gd["note"] = "couldn't read the guild window (%s)" % ex
        # Runs whatever happened: a hidden window we opened must never be left behind.
        finally:
            with Kit.quiet:
                reset_hide()
            hid = st.get("ghid", 0)
            st["ghid"] = 0
            if hid:
                with Kit.quiet:
                    API.CloseGump(hid)
            # The failure is held here because the kept copy of an earlier good read has ok set.
            failed = not gd["ok"]
            if failed:
                # A failed read keeps the last good copy, with only the note replaced.
                note, gd = gd["note"], dict(old)
                gd["note"] = note
                st["guild_fails"] = min(st["guild_fails"] + 1, 10)
                st["guild_next"] = time.time() + min(GUILD_RETRY_MAX, GUILD_RETRY * (2 ** (st["guild_fails"] - 1)))
            else:
                st["guild_fails"] = 0
                st["guild_said"] = ""
            st["guild"] = gd
            st["guild_busy"] = False
            st["guild_dirty"] = True
            if gd["ok"] and not failed:
                save_guild()
        if gd["note"]:
            if not failed:
                say("%s." % gd["note"])
            # Say a failure once until its text changes, so a retry loop does not fill the journal.
            elif gd["note"] != st["guild_said"]:
                st["guild_said"] = gd["note"]
                again = ""
                if settings["gevery"] and settings["tab"] == "guild":
                    again = " (retry in %d min)" % max(1, int((st["guild_next"] - time.time()) / 60 + 0.5))
                say("%s%s." % (gd["note"], again), Kit.HUE_BAD)

    def read_guild_window(old):
        """Script-thread body of guild_job: read the My Guild page and every Guild Roster page into a
        guild record and return it, with ok set when it worked. A guild window the player already has
        open is read as it is and put back on My Guild afterwards; otherwise one is requested (hidden
        when set), read and closed. A roster read cut short keeps the members last read, shown offline,
        so the saved roster is never emptied by a bad read.
        """
        gd = empty_guild()
        gd["members"] = list(old["members"])
        gids = st["gids"]

        def fail(note, stamp=False):
            """Set the failure note and return the record. With stamp the read still counts as done, for a
            failure after the My Guild page was read.
            """
            gd["note"] = note
            if stamp:
                gd.update({"ok": True, "at": time.time()})
            return gd

        # The guild window may be open but not the last server gump (another came after it): look through
        # every open gump before asking for a new one, which would close the player's own window.
        had, had_raw = last_gump()
        had_kind = classify(had_raw) if had_raw else None
        had_open = had_kind in ("guild", "roster")
        if not had_open:
            og, oraw = CL.find_server_gump(guild_test)
            if og:
                had, had_raw, had_kind, had_open = og, oraw, classify(oraw), True
        if had_open:
            # Read an open window as it is: asking the server for another would close it, and a press on the
            # old one would be dropped.
            gid, raw, kind = had, had_raw, had_kind
        else:
            # Hide the next gump: the My Guild page by id once known, else whatever comes (the create-a-guild
            # window for a character in no guild).
            hide_next(gids.get("info", 0) if old.get("in_guild", True) else 0)
            if not CL.game_action("OpenGuildGump"):
                return fail("couldn't ask for the guild window (%s)" % CL.error)
            gid, raw, kind = wait_gump(classify)
            if not gid:
                return fail(unknown_gump(had))
            st["ghid"] = gid
        # Not in a guild: record that, with an empty roster, and close the create-a-guild window.
        if kind == "noguild":
            API.CloseGump(gid)
            st["ghid"] = 0
            gd.update({"ok": True, "in_guild": False, "members": [], "at": time.time()})
            return gd
        # It opened on the roster: go to My Guild first.
        if kind == "roster":
            gids["roster"] = gid
            if not had_open:
                hide_next(gids.get("info", 0))
            press(gid, INFO_TAB, INFO_BUTTON)
            gid, raw, kind = wait_gump(lambda r: classify(r) == "guild" and "guild")
            if not gid:
                return fail("the My Guild page didn't come")
            if not had_open:
                st["ghid"] = gid
        info = parse_info(raw)
        # Open on another page (Diplomacy): go to My Guild first. The page must differ from the one
        # already seen.
        if had_open and not info.get("name"):
            prev = raw
            press(gid, INFO_TAB, INFO_BUTTON)
            gid, raw, kind = wait_gump(lambda r2: classify(r2) == "guild" and r2 != prev and "guild")
            if not gid:
                return fail("the My Guild page didn't come")
            info = parse_info(raw)
        gids["info"] = gid
        gd.update(info)
        # Hide the roster page by id once it is known.
        if not had_open:
            hide_next(gids.get("roster", 0))
        if not press(gid, ROSTER_TAB, ROSTER_BUTTON):
            return fail("couldn't open the Guild Roster page", True)
        gid, raw, kind = wait_gump(lambda r: classify(r) == "roster" and "roster")
        if not gid:
            return fail("the Guild Roster page didn't come", True)
        if not had_open:
            st["ghid"] = gid
        gids["roster"] = gid
        # Roster pages, one after another; seen holds names already taken so a repeated page adds no
        # duplicates.
        members, seen, pages, whole = [], {}, 0, False
        while not st["shutting"]:
            got, more = parse_roster(raw)
            pages += 1
            st["guild_pages"] = pages
            for m in got:
                k = m["name"].lower()
                if k not in seen:
                    seen[k] = True
                    members.append(m)
            # Stop at the last page or at the page limit.
            if not more or pages >= ROSTER_PAGES_MAX:
                whole = True
                break
            if not had_open:
                hide_next(gid)
            if not API.ReplyGump(FORWARD_BUTTON, gid):
                break
            prev = raw
            # The next page must be a roster that differs from the last one read.
            gid2, raw2, _ = wait_gump(lambda r2: classify(r2) == "roster" and r2 != prev and "ok")
            if not gid2:
                break
            gid, raw = gid2, raw2
            if not had_open:
                st["ghid"] = gid
        # A read cut short, or one that found nobody: the members not read stay as last read, shown
        # offline, never dropped from the saved roster.
        if not whole or not members:
            for m in old["members"]:
                k = m["name"].lower()
                if k not in seen:
                    seen[k] = True
                    # Keys starting with an underscore are sort keys; they are made afresh.
                    c = dict((k2, v2) for k2, v2 in m.items() if not k2.startswith("_"))
                    c["online"] = False
                    members.append(c)
            if not whole and pages:
                gd["note"] = "read %s only; rest as before" % Kit.count(pages, "roster page")
        gd["members"] = members
        gd.update({"ok": True, "at": time.time()})
        # Leave a window the player had open on My Guild, as it was.
        if had_open:
            press(gid, INFO_TAB, INFO_BUTTON)
        else:
            API.CloseGump(gid)
            st["ghid"] = 0
        return gd

    def win_w(tab):
        """Window width of a tab: the Guild tab is wider."""
        return GUILD_W if tab == "guild" else W

    def layout_fit(fw, fh, mode):
        """Called by the layout when this window sits in a zone: fw and fh are the slot it was given (None
        when it is freed). A new slot queues a redraw at exactly that size, with the title row and tab
        row laid out for the width they get. In mode again the layout measured the window and it is
        not its slot's size, so it is drawn once more.
        """
        new = (int(fw), int(fh)) if (fw is not None and fh is not None) else None
        if new != st.get("fit"):
            st["fit"] = new
            queue("redraw")()
        # Once per slot and drawing: a redraw that was asked for and still measures otherwise would not
        # change by drawing the same again.
        elif mode == "again" and new is not None:
            sig = (new, settings["tab"], st["minimized"], settings["rows"], settings["bars"])
            now = time.time()
            # After 5 seconds the same slot is drawn again, so a redraw that did not land (a drag, a client
            # clamp) is not left to the layout's stretch.
            if sig != st["again_for"] or not 0 <= now - st.get("again_at", 0.0) < 5.0:
                st.update({"again_for": sig, "again_at": now, "again_build": True})
                queue("redraw")()

    def min_title_w():
        """The narrowest the window can be drawn: the title and the Fold, Minimize and Close buttons,
        without Settings.
        """
        return max(160, M + 30 + Kit.text_w(TITLE.upper()) + 6 + 94 + M)

    def min_w():
        """The width the title row needs with its Settings button too."""
        return (M + 30 + Kit.text_w(TITLE.upper()) + 16 + (0 if Kit.zone_up(KEY) else 84 + Kit.DOCK_DX) + 35
                + Kit.text_w("Settings") + M)

    def tab_lines(iw):
        """Place the tab buttons in a row iw wide, wrapping to further lines. Returns ([(tab key,
        caption, x offset, line)], number of lines).
        """
        out, tx, line = [], 10, 0
        for key, cap in TABS:
            bw = 35 + Kit.text_w(cap)
            if tx > 10 and tx + bw > iw - 4:
                tx, line = 10, line + 1
            out.append((key, cap, tx, line))
            tx += bw + 14
        return out, line + 1

    def tab_layout(tab):
        """Body shape of a tab as (info lines, toolbar rows, list rows). The Profile tab has no list."""
        # Per tab: Friends one info line and one toolbar; Party two info lines, three bars (buttons,
        # Accept and Decline, chat); Guild six info lines, two bars (buttons, chat); anything else
        # (Profile) seven info lines, two bars.
        info, bars = {"friends": (1, 1), "party": (2, 3), "guild": (6, 2)}.get(tab, (7, 2))
        return info, bars, settings["rows"] if info < 7 else 0

    def window_h(tab):
        """Height in pixels of the window for a tab at its own size."""
        info, bars, rows = tab_layout(tab)
        body = (8 + info * 22 + (8 if info else 0) + bars * 30 + rows * ROW_H + (8 if rows else 0) + 4)
        return M + 30 + Kit.GAP + 30 + Kit.GAP + body + M

    def min_size():
        """The layout's minimum size: the narrowest title row, and the tallest tab with one list row (the
        tab can change after the window is placed), plus 30 for the tab row wrapping onto a second
        line. Below that the info lines and toolbars would be drawn past the window's bottom.
        """
        return (min_title_w(), max(window_h(t) - max(0, tab_layout(t)[2] - 1) * ROW_H for t, _c in TABS) + 30)

    def build_window():
        """Draw the window for the current tab: title bar, tab row, body, then fill it with refresh. At
        its own size, or in a zone exactly the slot it was given. Minimized, only the bar is drawn.
        """
        tab = settings["tab"]
        g, store, c = wnd.begin(win_w(tab), window_h(tab))
        w, h = wnd.w, wnd.h
        rows = []
        # New labels: their tooltips and last written texts start afresh.
        win["info_tips"], win["info_in"] = {}, {}
        # A redraw asked for by layout_fit keeps its again state; any other build clears it.
        if st["again_build"]:
            st["again_build"] = False
        else:
            st["again_for"] = None
        if not st["minimized"]:
            fit = st.get("fit")
            # A slot shorter than the window can be drawn is ignored and the window keeps its own size.
            if fit is not None and fit[1] < min_size()[1]:
                fit = None
            if fit is not None:
                # Never narrower than the title row needs, or its buttons draw over one another.
                w, h = max(min_title_w(), fit[0]), fit[1]
            IW = w - 2 * M
            c["iw"] = IW
            # Too narrow for the Settings button: left out (the mother's window still opens the page), so
            # nothing overlaps in the title row.
            wnd.frame(g, w, h, settings=w >= min_w())
            # The tab row, on two lines when the width is too small for one.
            yt = M + 30 + Kit.GAP
            places, nlines = tab_lines(IW)
            Kit.add_section(g, M, yt, IW, 30 * nlines)
            for key, cap, tx, line in places:
                Kit.art_button(g, store, "tab_" + key, Kit.ART_PAGE, M + tx, yt + 4 + 30 * line, cap, TAB_TIPS[key],
                               hue=Kit.HUE_TITLE if key == tab else Kit.HUE_TEXT, on_click=queue(("tab", key)))
            # The body.
            yb = yt + 30 * nlines + Kit.GAP
            if fit is None:
                # At its own size the window grows to hold a wrapped tab row.
                h += 30 * (nlines - 1)
            bh = h - yb - M
            Kit.add_section(g, M, yb, IW, bh)
            # In a zone the list rows are counted under the toolbars as they were laid out, since a narrow
            # zone may wrap them onto more lines.
            build_tab(g, store, c, rows, tab, M, yb, IW, bh, fit is not None)
        wnd.end(g, {"rows": rows, "tab": tab, "info": {}}, w, h)
        st["rebuild"] = False
        refresh()

    # The standard module window of the mother: position and minimized state are saved under the two
    # keys and the tray icon shows on the Action Bar. docked_min means a docked, minimized window
    # is folded into the Action Bar.
    wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, mini=(MINI_W, MINI_H), icon=TRAY_ICON,
                     cleanup=cleanup, docked_min=True)

    def build_tab(g, store, c, rows, tab, x, y, w, h, fit=False):
        """Draw the body of one tab (info labels, toolbars, chat field and list rows) inside the section
        at x, y of size w by h. With fit set, the window is sized by a zone: the rows and the info
        lines are counted from the height that is there.
        """
        info, bars, nrows = tab_layout(tab)
        TOOL_RIGHT[0] = x + w - 6

        def list_rows(yy):
            """The number of list rows that fit under yy in a zone (at least one), else the setting's."""
            return max(1, (y + h - 12 - yy) // ROW_H) if fit else nrows

        # In a zone fewer info lines are shown when the height is short; the rest are stacked on the
        # last visible position and hidden.
        vis = max(1, min(info, (h - 16 - bars * 30 - (ROW_H + 12 if nrows else 4)) // 22)) if fit and info else info
        c["info"] = [Kit.add_label(g, "", x + 10, y + 8 + 22 * min(i, vis - 1), Kit.HUE_INFO) for i in range(info)]
        for lbl in c["info"][vis:]:
            lbl.IsVisible = False
        yy = y + 8 + 22 * vis + (8 if vis else 0)
        if tab == "friends":
            items = [("add", Kit.ART_PLAY, ["Add friend...", None], "Target someone to add to TazUO's friends list"),
                     ("add_last", Kit.ART_OK, ["Add last target", None],
                      "Add your last target to TazUO's friends list")]
            # Friends toolbar: the page arrows go at its end.
            yy = toolbar_paged(g, store, c, x, y, yy, w, items, None)
            add_rows(g, store, c, rows, list_rows(yy), x, yy, w,
                     ROW_TIP % "set as last target (or answer a target cursor)",
                     True, rm_tip="Remove from TazUO's friends list")
        elif tab == "party":
            # Party toolbar over the width of the window.
            yy += 30 * toolbar(g, store, c, x, yy, x + w - 6, [
                ("invite", Kit.ART_PLAY, ["Invite...", None], "Target someone to invite to your party"),
                ("leave", Kit.ART_CLOSE, ["Leave", None], "Leave the party"), ("loot", Kit.ART_OK, ["Loot", None],
                 "Allow or forbid party looting of your corpse (the line above shows which)"),
                ("pwin", Kit.ART_PAGE, ["Party window", None], "Open the client's party window")])
            # Accept and Decline have their own row, with room kept for the page arrows at its end.
            TOOL_RIGHT[0] = x + w - 6 - PAGER_W - 6
            c["accept"] = tool(g, store, x + 10, yy, "accept", Kit.ART_OK, "Accept",
                               "Join the party. Alt+click: auto-follow the inviter (again to stop)",
                               on_click=invite_click("accept"))
            c["decline"] = tool(g, store, c["accept"][1], yy, "decline", Kit.ART_CLOSE, "Decline",
                                "Turn the invitation down. Alt+click: auto-follow the inviter (again to stop)",
                                on_click=invite_click("decline"))
            TOOL_RIGHT[0] = x + w - 6
            pager(g, store, c, x + w, yy)
            yy += 30
            chat(g, store, c, x, yy, w, [("psend", "Send", "Say it in party chat")], "Message for party chat")
            yy += 30
            add_rows(g, store, c, rows, list_rows(yy), x, yy, w,
                     ROW_TIP % "set as last target (or answer a target cursor)",
                     True, rm_tip="Remove from the party (leader only)")
        elif tab == "guild":
            items = [("grefresh", Kit.ART_PLAY, ["Refresh", None], "Read the guild window again (info and roster); "
                      + ("it opens hidden" if settings["ghide"] else
                         "it shows while read; Social settings can hide it")),
                     ("gwin", Kit.ART_PAGE, ["Guild window", None], "Open the server's guild menu"),
                     ("diplo", Kit.ART_PAGE, ["Diplomacy", None], "Open the guild window's Diplomacy page"),
                     ("gsort", Kit.ART_PAGE, ["long", "short", None], None)]
            # The captions give way in this order: the Sort button's long caption shortens first, then the
            # captions drop from the last button back, then the Sort button loses its caption.
            yy = toolbar_paged(g, store, c, x, y, yy, w, items, [3, 2, 1, 0, 3])
            chat(g, store, c, x, yy, w, [("gsend", "Guild", "Say it in guild chat"),
                                         ("asend", "Alliance", "Say it in alliance chat")],
                 "Message for guild or alliance chat")
            yy += 30
            add_rows(g, store, c, rows, list_rows(yy), x, yy, w, ROW_TIP % "set as last target when in view",
                     False, before=[("rank", RANK_W)], after=[("title", 0)])
        else:
            # Profile tab: two toolbars, no list.
            yy += 30 * toolbar(g, store, c, x, yy, x + w - 6, [("edit", Kit.ART_PAGE, ["Edit profile", None],
                 "Open your profile (the server's scroll; closing saves)"),
                ("paperdoll", Kit.ART_PAGE, ["Paperdoll", None], "Open the client's paperdoll"),
                ("status", Kit.ART_PAGE, ["Status", None], "Open the client's status window")])
            toolbar(g, store, c, x, yy, x + w - 6, [
                ("ignore", Kit.ART_PAGE, ["Ignore list", None], "Open TazUO's ignore list (speech you hide)"),
                ("war", Kit.ART_PLAY, ["War / peace", None],
                 "Switch war mode and peace (the last line above shows which)")])

    # Row tooltip, filled with what a plain click does on that tab.
    ROW_TIP = "Click: %s. Shift+click: write a note. Alt+click: auto-follow (again to stop)"
    # Width kept at a toolbar's right end for the page arrows and the page number.
    PAGER_W = 100

    def sort_tip(c):
        """Tooltip of the Sort button. When the button shows no caption, the tip names the roster order."""
        tip = "Next roster order: online (in view first), last on, rank or name"
        if c.get("gsort_bare"):
            e = SORTS[SORT_CODES.index(settings["gsort"])]
            tip = "Roster order: %s. %s" % (e[2].lower(), tip)
        return tip

    def cap_w(key, cap):
        """Pixel width a caption needs. The Sort button is sized for its widest order so it does not
        change width when the order changes.
        """
        if key == "gsort":
            if cap == "long":
                return max(Kit.text_w(e[1]) for e in SORTS)
            return max(Kit.text_w(e[2]) for e in SORTS)
        return Kit.text_w(cap)

    def toolbar_plan(items, x, right, order):
        """Choose a caption level for each toolbar button so the row fits between x + 10 and right. The
        first try has every caption in full; then the levels are stepped down, one button per step,
        in the order given (item indexes; the default drops the last button's caption first). Returns
        the list of levels, or None when even the last step does not fit.
        """
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

    def toolbar(g, store, c, x, y, right, items, order=None, plan=None):
        """Draw a row of buttons from x + 10 to right. items are (key, art, [captions, then None for
        button alone], tooltip). Captions give way as toolbar_plan decides, or, when even the buttons
        alone do not fit, the row wraps onto further lines at the shortest captions. Returns the
        number of lines used.
        """
        lv = plan or toolbar_plan(items, x, right, order)
        wrap = lv is None
        if wrap:
            lv = [len(it[2]) - 1 for it in items]
        bx, line = x + 10, 0
        for i, (key, art, caps, tip) in enumerate(items):
            cap = caps[lv[i]]
            if key == "gsort":
                c["gsort_long"] = cap == "long"
                c["gsort_bare"] = cap is None
                tip = sort_tip(c)
                cap = None if cap is None else sort_caption(c)
            # A dropped caption goes into the tooltip so the button is still named.
            elif cap is None and caps[0]:
                tip = Kit.caption_tip(caps[0], tip)
            need = 30 if cap is None else 35 + Kit.text_w(cap)
            if wrap and bx > x + 10 and bx + need > right:
                bx, line = x + 10, line + 1
            ctrl = Kit.art_button(g, store, key, art, bx, y + 30 * line, cap, tip, on_click=queue(key))
            bx += 30 if cap is None else need + 12
            if key == "gsort":
                # The Sort button's caption is rewritten in place when the order changes.
                c["gsort"] = ctrl if cap is not None else None
                c["gsort_btn"] = store[0].get(key)
        return line + 1

    def toolbar_paged(g, store, c, x, y, yy, w, items, order):
        """A toolbar with the page arrows at its right end. When the buttons would lose a caption beside
        the arrows (a narrow zone), the arrows go up to the end of the first info line instead and the
        info line is cut short for them. Returns the y under the toolbar.
        """
        plan = toolbar_plan(items, x, x + w - 6 - PAGER_W - 6, order)
        full = plan is not None and all(
            it[2][l] is not None and (l == 0 or it[0] == "gsort") for it, l in zip(items, plan))
        if full:
            lines = toolbar(g, store, c, x, yy, x + w - 6 - PAGER_W - 6, items, order, plan)
            pager(g, store, c, x + w, yy)
        else:
            lines = toolbar(g, store, c, x, yy, x + w - 6, items, order)
            pager(g, store, c, x + w, y + 8 - 6)
            c["info_cut"] = PAGER_W + 6
        return yy + 30 * lines

    # Right edge of the toolbar being built, so tool knows when a caption no longer fits.
    TOOL_RIGHT = [100000]

    def tool(g, store, x, y, key, art, cap, tip, on_click=None):
        """Draw one art button with its caption at x, y. When the caption would pass TOOL_RIGHT the
        button is drawn alone and the caption goes into its tooltip. Returns (the button's part, the
        x for the next button, the control).
        """
        bare = x + 35 + Kit.text_w(cap) > TOOL_RIGHT[0]
        ctrl = Kit.art_button(g, store, key, art, x, y, None if bare else cap,
                              Kit.caption_tip(cap, tip) if bare else tip, on_click=on_click or queue(key))
        return store[0].get(key), (x + 30 if bare else x + 35 + Kit.text_w(cap) + 12), ctrl

    def invite_click(key):
        """Click handler for Accept and Decline. They act on the invitation; Alt+click follows the
        inviter instead, as everywhere in the suite. Alt is read in the click itself.
        """
        def handler(*args):
            """The click handler."""
            p = st["party"]
            inv = p[1] if p else 0
            if inv and Follow.alt_held():
                queue(("follow", inv))()
            else:
                queue(key)()

        return handler

    def pager(g, store, c, right, y):
        """The page number label and the two page arrows, ending at the x right, on the row at y."""
        c["pg"] = Kit.add_label(g, "", right - 100, y + 6, Kit.HUE_INFO)
        Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 56, y + 4, None, "Previous page",
                       on_click=queue(("page", -1)))
        Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 34, y + 4, None, "Next page",
                       on_click=queue(("page", 1)))

    def chat(g, store, c, x, y, w, buttons, field_tip):
        """A text box and its Send buttons, right-aligned. What was typed is kept per tab in st msg.
        When the field would be narrower than MSG_W_MIN the buttons lose their captions.
        """
        bw = sum(35 + Kit.text_w(cap) + 12 for _, cap, _ in buttons)
        fw = w - 20 - bw - 8
        if fw < MSG_W_MIN:
            fw = max(40, w - 20 - 30 * len(buttons) - 8)
        c["msg"] = Kit.with_tip(Kit.add_textbox(g, st["msg"].get(settings["tab"], ""), x + 10, y + 3, fw,
                                                numbers=False), field_tip)
        bx = x + 10 + fw + 12
        for key, cap, tip in buttons:
            bx = tool(g, store, bx, y, key, Kit.ART_PLAY, cap, tip)[1]

    def add_rows(g, store, c, rows, n, x, y, w, tip, removable, before=None, after=None, rm_tip="Remove"):
        """Build a pool of n list rows: name, extra columns before the bar, the health bar, status,
        extra columns after, and an X button when removable. before and after are [(key, width)]
        extra label columns, with width 0 meaning the rest of the row. Rows are reused for the life of
        the window and only their text is rewritten.

        A row too narrow for its columns drops them: the last extra columns first, then the health
        bar. What a dropped column would show goes into the row's tooltip instead.
        """
        bw, bh = Kit.pic_size(Kit.LINE_RED)
        # Bar size from the art; the numbers are used when it is not loaded yet.
        bw, bh = bw or 109, bh or 9
        fw, fh = Kit.pic_size(Kit.LINE_BLUE)
        # The X button takes 40 pixels at the right.
        right = x + w - 4 - (40 if removable else 0)
        before, after = list(before or []), list(after or [])
        dropped = []
        bars = settings["bars"]

        def fixed():
            """Width the extra columns take with their gaps, a width of 0 counted as 40."""
            return sum(wd + 8 for _k, wd in before) + sum((wd or 40) + 8 for _k, wd in after)

        # Drop columns until the row fits the name, status and bar floors.
        while right - (x + 10) < fixed() + 8 + 40 + 8 + (30 + 8 if bars else 0) + 44 and (after or before or bars):
            if after:
                dropped.append(after.pop()[0])
            elif before:
                dropped.append(before.pop()[0])
            else:
                bars = False
        # Columns share the width the row really has: at the window's own width as set; narrower (a
        # zone), the status and the bar give way to a floor and the name takes what is left, so nothing
        # runs past the X or the window's edge.
        name_w, status_w = NAME_W, STATUS_W
        room = right - (x + 10) - fixed() - 8
        need = NAME_W + 8 + (bw + 8 if bars else 0) + STATUS_W
        if room < need:
            status_w = max(44, min(STATUS_W, int(room * 0.24)))
            if bars:
                bw = max(30, min(bw, int(room * 0.30)))
            name_w = max(40, room - status_w - 8 - (bw + 8 if bars else 0))
        c["bar_w"], c["name_w"], c["status_w"] = bw, name_w, status_w
        for i in range(n):
            ry = y + i * ROW_H
            # One row: serial and who it shows now, serial and who it showed before with the time it
            # changed, the controls as [control, visible] parts, and the extra labels.
            r = {"serial": 0, "prev": (0, 0.0), "parts": [], "name": None, "status": None,
                 "fill": None, "fill_w": -1, "x": None, "red": None, "extra": {}, "who": "", "prev_who": ("", 0.0),
                 "tip0": tip, "tip": tip}
            cx = x + 10
            r["name"] = Kit.add_label(g, "", cx, ry + 3)
            # Parts are [control, visible] pairs so set_vis only touches the client when the state changes.
            r["parts"].append([r["name"], True])
            cx += name_w + 8
            for key in dropped:
                r["extra"][key] = (None, 0)
            for key, wd in before:
                lbl = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO)
                r["extra"][key] = (lbl, wd)
                r["parts"].append([lbl, True])
                cx += wd + 8
            if bars:
                # The red bar is tiled to the bar width; the blue fill on top of it is resized to the health.
                r["red"] = [Kit.add_tiled(g, Kit.LINE_RED, cx, ry + 7, bw, bh), True]
                r["parts"].append(r["red"])
                if fw and fh:
                    r["fill"] = Kit.add_tiled(g, Kit.LINE_BLUE, cx, ry + 7, 1, fh)
                    r["fill"].SetWidth(0)
                    r["parts"].append([r["fill"], True])
                cx += bw + 8
            r["status"] = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO)
            r["parts"].append([r["status"], True])
            cx += status_w + 8
            for key, wd in after:
                # A width of 0 takes what is left of the row.
                wd = wd or max(40, right - cx)
                lbl = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO)
                r["extra"][key] = (lbl, wd)
                r["parts"].append([lbl, True])
                cx += wd + 8
            # An invisible catcher over the whole row (the X excluded) takes the clicks and shows the tip.
            r["catch"] = Kit.catcher(g, x + 4, ry, w - 8 - (40 if removable else 0), ROW_H, row_click(rows, i), tip)
            r["parts"].append([r["catch"], True])
            if removable:
                r["x"] = Kit.art_button(g, store, "rm%d" % i, Kit.ART_CLOSE, x + w - 42, ry + 1,
                                        None, rm_tip + ". Alt+click: auto-follow (again to stop)",
                                        on_click=rm_click(rows, i))
                r["parts"].append([r["x"], True])
            rows.append(r)

    def recent(r, cur, prev, now):
        """Return the previous value of a row's field when it changed under 0.15 seconds ago, else the
        current one. A click lands on what the player saw, not on what the row was just rewritten to.
        """
        p, at = r[prev]
        return p if p and now - at < 0.15 else r[cur]

    def rm_click(rows, i):
        """Click handler for the X of row i: Alt+click follows the row's mobile, a plain click removes it."""
        def handler(*args):
            """The click handler. Queues the work for the client tick; the serial is the one that was shown,
            not whoever holds the row when the tick runs.
            """
            serial = recent(rows[i], "serial", "prev", time.time())
            if serial and Follow.alt_held():
                queue(("follow", serial))()
            elif serial:
                queue(("rm", serial))()

        return handler

    def row_click(rows, i):
        """Click handler for row i: Alt+click follows, Shift+click writes a note, a plain click targets."""
        def handler(*args):
            """The click handler. A row with a name but nobody in view only takes the note click; any other
            click says they are not in view.
            """
            r, now = rows[i], time.time()
            serial, who = recent(r, "serial", "prev", now), recent(r, "who", "prev_who", now)
            if not serial:
                if who and not Follow.alt_held() and shift_held():
                    queue(("note", who))()
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

    # Shared empty extra columns, never changed.
    NO_EXTRA = {}

    def shift(r, key, prev, v):
        """Set a row field and remember the old value with the time of change, for recent."""
        if r[key] != v:
            r[prev], r[key] = (r[key], time.time()), v

    def set_row(r, serial, name, status, hue, frac, extra=None, name_hue=None, bar=True, show_x=True):
        """Write a row: the name, status, health bar and extra columns, only what changed since the last
        pass. extra holds rank and title; text too long for its column goes into the row's tooltip,
        with the player's note when there is one. A pass identical to the last one writes nothing. The
        notes version is part of that comparison so a changed note refreshes its tooltip.
        """
        # The comparison key: everything the row shows.
        ex = extra or NO_EXTRA
        key = (serial, name, status, hue, frac, ex.get("rank"), ex.get("title"), name_hue, bar, show_x, notes_st["ver"])
        if key == r.get("last"):
            return
        r["last"] = key
        shift(r, "serial", "prev", serial)
        shift(r, "who", "prev_who", name)
        if name_hue is None:
            name_hue = Kit.HUE_TEXT if frac is not None else Kit.HUE_INFO
        c = win["c"]
        Kit.set_text(r["name"], fit(name, c.get("name_w", NAME_W)), name_hue)
        Kit.set_text(r["status"], fit(status, c.get("status_w", STATUS_W)), hue)
        # Columns too long for the row, listed in the tooltip.
        cut = []
        for key, (lbl, wd) in r["extra"].items():
            full = str(ex.get(key, "") or "")
            short = ""
            if lbl is not None:
                short = fit(full, wd)
                Kit.set_text(lbl, short, Kit.HUE_INFO)
            if short != full:
                cut.append("%s: %s" % (key.capitalize(), full))
        tip = "\n".join([r["tip0"]] + cut)
        if NOTES:
            e = NOTES.get(name.lower())
            if e is not None:
                tip = tip + "\nNote: " + e[1]
        if tip != r["tip"] and r.get("catch") is not None:
            r["tip"] = tip
            Kit.with_tip(r["catch"], tip)
        w = int(win["c"].get("bar_w", 109) * max(0.0, min(1.0, frac or 0.0)))
        if r["fill"] is not None and w != r["fill_w"]:
            r["fill_w"] = w
            Kit.ui_w(r["fill"], max(1, w))
        # The X is the last part.
        xp = r["parts"][-1] if r["x"] is not None else None
        for p in r["parts"]:
            if r["fill"] is not None and p[0] is r["fill"]:
                # Visibility is written once, not hidden then shown.
                set_vis(p, bar and w > 0)
            elif r["red"] is not None and p is r["red"]:
                set_vis(p, bar)
            elif p is xp:
                set_vis(p, show_x)
            else:
                set_vis(p, True)

    def hide_row(r):
        """Hide every part of a row and forget what it showed, so the next set_row writes it in full."""
        r["last"] = None
        shift(r, "serial", "prev", 0)
        shift(r, "who", "prev_who", "")
        for p in r["parts"]:
            set_vis(p, False)

    def mobile_status(serial):
        """Status of a mobile from this pass's reads: (text, hue, health fraction or None). Away when out
        of view, dead, else the distance; the hue goes green, yellow below half and red below a
        quarter.
        """
        d = full_mob(serial)
        if d is None:
            return "away", Kit.HUE_INFO, None
        name, hits, hmax, dist, dead, noto = d
        if dead:
            return "dead", Kit.HUE_BAD, 0.0
        frac = hits / float(hmax) if hmax > 0 else None
        hue = (Kit.HUE_GOOD if frac is None or frac > 0.5 else (Kit.HUE_TITLE if frac > 0.25 else Kit.HUE_BAD))
        return (Kit.count(dist, "tile")), hue, frac

    def page_of(items):
        """The items on the current page of the current tab, and the page text such as 1/3 (empty for one
        page). The page number is clamped to the pages that exist.
        """
        n = max(1, len(win["rows"]))
        pages = max(1, (len(items) + n - 1) // n)
        p = max(0, min(pages - 1, st["page"].get(settings["tab"], 0)))
        st["page"][settings["tab"]] = p
        return items[p * n:(p + 1) * n], ("%d/%d" % (p + 1, pages)) if pages > 1 else ""

    # Rank name, in lower case, to its place in the order.
    RANK_INDEX = dict((name, i) for i, names in enumerate(RANK_ORDER) for name in names)

    def laston_key(m):
        """A member's Last On as a number that sorts (newest highest, -1 when it is not a date), worked
        out once per member read and kept in the member's record.
        """
        v = m.get("_lo")
        if v is None:
            v = -1
            hit = DATE_RE.search(m["laston"] or "")
            if hit is not None:
                a, sep, b, c = hit.group(1), hit.group(2), int(hit.group(3)), hit.group(4)
                ia, ic = int(a), int(c)
                # Year first (2026-10-31), else the year is last and day or month comes first.
                if len(a) == 4 or ia > 31:
                    y, mo, d = ia, b, ic
                else:
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
        """Caption of the Sort button for the current order, long or short as the toolbar laid it out."""
        e = SORTS[SORT_CODES.index(settings["gsort"])]
        return e[1] if c.get("gsort_long") else e[2]

    # Roster order kept per read: src is the members list it was made for (replaced whole by a new
    # read), how the order. For the last on, rank and name orders it depends only on the members;
    # online keeps the members out of view in this order and only those in view are sorted each pass.
    gcache = {"src": None, "how": None, "order": [], "names": {}, "online": 0}

    def mkey(m):
        """A member's lower-case name, worked out once and kept in the record."""
        k = m.get("_k")
        if k is None:
            k = m["_k"] = m["name"].lower()
        return k

    def first(e):
        """First item of a tuple, the sort key for lists of (key, serial, member)."""
        return e[0]

    def static_key(how):
        """Return the sort key function for an order, made once per read: online (online first, then
        name), name, rank (top rank first, then name) or last on (online first, newest first, then
        name).
        """
        nranks = len(RANK_ORDER)
        if how == "online":
            return lambda m: ((0 if m["online"] else 1), m["_k"])
        if how == "name":
            return lambda m: m["_k"]
        if how == "rank":
            return lambda m: (RANK_INDEX.get((m["rank"] or "").strip().lower(), nranks), m["_k"])
        return lambda m: ((0 if m["online"] else 1), -laston_key(m), m["_k"])

    def guild_order(gd, how):
        """Return the roster order cache for how, rebuilding it only when the members list or the order
        changed. Also counts the online members.
        """
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

    def guild_items(me):
        """The roster rows as (serial in view or 0, member). Orders as the Sort button says: online first
        (members in view first, nearest first, then online, then the rest by name), last on, rank, or
        name. Allies in view that are not on the roster come last, nearest first. Returns the rows
        and how many members are in view.
        """
        gd = st["guild"] or empty_guild()
        view, mobs = st["view"], st["mobs"]
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
            # Allies already on the roster, you and nameless ones are skipped.
            if k in names or k == me or not name:
                continue
            d = mobs.get(serial)
            allies.append(((d[3] if d else 999, k), serial,
                           {"name": name, "rank": "ally", "laston": "", "title": "ally in view",
                            # Not a roster member: marked ally so it is not counted as one.
                            "online": True, "me": False, "_k": k, "ally": True}))
        if allies:
            allies.sort(key=first)
            for e in allies:
                items.append((e[1], e[2]))
        return items, inview

    def refresh():
        """Write what changed into the window: labels, rows and bars, for the tab shown, or the one status
        line when minimized. Client tick. Does nothing while the window is folded into the Action Bar
        or while its drawn form does not match the minimized flag (a rebuild is on its way).
        """
        g, c = win["g"], win["c"]
        if g is None or (st["minimized"] and st["docked"]) or ("status" in c) != bool(st["minimized"]):
            return
        if st["minimized"]:
            n, inview = len(st["friends"]), len(st["inview"])
            party = st["party"]
            txt = "%s: %s, %d in view" % (TITLE, Kit.count(n, "friend"), inview)
            if in_party(party):
                txt += ", party of %d" % (len(party[3]) + 1)
            # The mini bar's text is cut to what is left beside its buttons.
            Kit.set_text(c["status"], fit(txt, MINI_W - 18 - 66))
            return
        tab = win["tab"]
        info = c.get("info", [])
        tw = c.get("iw", win_w(tab) - 2 * Kit.MARGIN) - 20
        tw0 = tw - c.get("info_cut", 0)
        if tab == "friends":
            items = st["friends"]
            shown, pg = page_of(items)
            inview = len(st["inview"])
            # The line is formatted again only when its inputs change.
            fk = (len(items), inview, tw0)
            if win["info"].get("friends") != fk:
                win["info"]["friends"] = fk
                Kit.set_text(info[0], fit("%s, %d in view" % (Kit.count(len(items), "friend"), inview) if items else
                                          "No friends yet: Add friend... targets one", tw0))
            show_rows(c, [(s, mob_name(s, n)) for s, n in shown], pg)
        elif tab == "party":
            party = st["party"]
            me = player_serial()
            # The client keeps an empty party object when you are in none; in_party tells.
            if not in_party(party):
                Kit.set_text(info[0], fit("Not in a party: Invite... asks someone to join", tw), Kit.HUE_INFO)
                Kit.set_text(info[1], "", Kit.HUE_INFO)
                items = []
            else:
                leader, inviter, loot, members = party
                lname = "you" if leader == me else mob_name(leader)
                Kit.set_text(info[0], fit(("Party of %d, led by %s" % (len(members) + 1, lname))
                                          if leader else "Party of %d" % (len(members) + 1), tw), Kit.HUE_TEXT)
                Kit.set_text(info[1], fit("Party may loot your corpse: %s" % ("yes" if loot else "no"), tw),
                             Kit.HUE_INFO)
                items = [s for s in members if s != me]
            inviter = party[1] if party else 0
            # An invitation shows only while there is an inviter and you are in no party.
            invite = bool(inviter) and not (party and party[0])
            for k in ("accept", "decline"):
                ctrl = c.get(k)
                if ctrl is not None and win["info"].get("vis_" + k) != invite:
                    win["info"]["vis_" + k] = invite
                    for part in (ctrl[0], ctrl[2]):
                        Kit.set(part, "IsVisible", invite)
            if invite:
                nm = st["mobs"].get(inviter)
                Kit.set_text(info[0], fit("Party invite from %s: Accept or Decline" % (
                    nm[0] if nm and nm[0] else "0x%08X" % inviter), tw), Kit.HUE_TITLE)
            shown, pg = page_of(items)
            # Only the leader can remove members, so the X shows for the leader alone.
            show_rows(c, [(s, mob_name(s)) for s in shown], pg, bool(party) and party[0] == me and bool(me))
        elif tab == "guild":
            refresh_guild(info, c, tw)
        else:
            # Read on the Guild tab, the profile holds only the name and lines; read all of it now.
            if st["prof_part"]:
                read_profile(True)
            prof = st["profile"]
            if not prof:
                win["info"].pop("prof", None)
                for l in info:
                    Kit.set_text(l, "")
                Kit.set_text(info[0], fit("No character logged in", tw), Kit.HUE_INFO)
                return
            # Formatted only when the profile or the width changes.
            pk = (prof, tw)
            if win["info"].get("prof") == pk:
                return
            win["info"]["prof"] = pk
            name, lines, noto, gold, fol, fmax, wt, wmax, war, hidden = prof
            titles = [l for l in lines if l != name]
            texts = [(name, Kit.HUE_TITLE), (" / ".join(titles) if titles else
                      "No titles read yet: hover yourself once", Kit.HUE_INFO),
                     ("Notoriety: %s" % (noto or "unknown"), Kit.HUE_TEXT), ("Gold: %d" % gold, Kit.HUE_TEXT),
                     ("Followers: %d / %d" % (fol, fmax), Kit.HUE_TEXT), ("Weight: %d / %d" % (wt, wmax), Kit.HUE_TEXT),
                     ("%s%s" % ("War mode" if war else "Peace", ", hidden" if hidden else ""),
                      Kit.HUE_BAD if war else Kit.HUE_GOOD)]
            for l, (t, hue) in zip(info, texts):
                # A narrow zone cuts the lines short.
                Kit.set_text(l, fit(t, tw), hue)

    def mob_name(s, other=None):
        """Name for a serial: the one read this pass, else the saved one, else other, else the serial in
        hex.
        """
        d = st["mobs"].get(s)
        return (d[0] if d and d[0] else "") or st["names"].get(s, "") or other or "0x%08X" % s

    def show_rows(c, shown, pg, show_x=True):
        """Fill the list rows with (serial, name) pairs from the current page and hide the rest of the
        rows. pg is the page text; show_x says whether the X buttons show.
        """
        Kit.set_text(c["pg"], pg)
        rows = win["rows"]
        for r, (serial, name) in zip(rows, shown):
            status, hue, frac = mobile_status(serial)
            set_row(r, serial, name, status, hue, frac, show_x=show_x)
        for r in rows[len(shown):]:
            hide_row(r)

    def set_info(lbl, full, width, hue):
        """Write an info line cut to width, with its whole text as the tooltip when it was cut. A line
        identical to the last one written is skipped: a long charter would otherwise take the slow,
        letter by letter route through fit every pass.
        """
        done = win["info_in"]
        k = (full, width, hue)
        if done.get(lbl) == k:
            return
        shown = fit(full, width)
        Kit.set_text(lbl, shown, hue)
        tip = full if shown != full else ""
        tips = win["info_tips"]
        # The two memo tables are bounded; they only ever hold this window's few labels.
        if len(tips) > 64:
            tips.clear()
        if tips.get(lbl) != tip:
            tips[lbl] = tip
            lbl.SetAcceptMouseInput(bool(tip))
            lbl.SetTooltip(tip)
        if len(done) > 64:
            done.clear()
        done[lbl] = k

    def plain_info(lbl, text, hue=None):
        """Write an info line without set_info; set_info writes it in full the next time."""
        Kit.set_text(lbl, text, hue)
        win["info_in"].pop(lbl, None)

    def refresh_guild(info, c, tw):
        """Fill the Guild tab: the six info lines (name, your guild line, alliance and faction, charter,
        website, read status), then the roster rows with health for the members in view.
        """
        # Beside the page arrows when in a zone.
        tw0 = tw - c.get("info_cut", 0)
        gd = st["guild"] or empty_guild()
        prof = st["profile"]
        # Your tooltip lines other than your name make up your own guild line.
        lines = [l for l in prof[1][1:] if l and l != prof[0]] if prof else []
        if not gd["ok"]:
            plain_info(info[0], fit("Guild window not read yet", tw0), Kit.HUE_INFO)
        elif not gd["in_guild"]:
            plain_info(info[0], fit("Not in a guild", tw0), Kit.HUE_INFO)
        else:
            set_info(info[0], gd["name"] or "Guild name not shown", tw0, Kit.HUE_TITLE)
        # A line cut to the window's width has its whole text as its tooltip.
        set_info(info[1], ("You: " + " / ".join(lines)) if lines else
                 "Your guild line isn't read yet: hover yourself once", tw, Kit.HUE_TEXT if lines else Kit.HUE_INFO)
        if gd["ok"] and gd["in_guild"]:
            set_info(info[2], "Alliance: %s     Faction: %s" % (
                gd["alliance"] or "none", gd["faction"] or "none"), tw, Kit.HUE_TEXT)
            set_info(info[3], "Charter: %s" % (gd["charter"] or "not set"), tw, Kit.HUE_INFO)
            set_info(info[4], "Website: %s" % (gd["website"] or "not set"), tw, Kit.HUE_INFO)
        else:
            for l in info[2:5]:
                plain_info(l, "")
        me_name = str(player_name() or "").lower()
        # The in view count holds members only; allies in view that are off the roster are not counted.
        items, inview = guild_items(me_name)
        online = guild_order(gd, settings["gsort"])["online"]
        if st["guild_busy"]:
            pages = st["guild_pages"]
            status = "Reading the guild window" + (" (page %d)" % pages if pages else "")
            hue = Kit.HUE_TITLE
        elif not gd["ok"]:
            note = gd["note"]
            status = ((note[:1].upper() + note[1:]) if note else
                      ("Click Refresh to read the guild window" if not settings["gevery"]
                       else "Read when this tab shows"))
            hue = Kit.HUE_BAD if note else Kit.HUE_INFO
        elif not gd["in_guild"]:
            status, hue = "Read %s; allies in view below" % ago(gd["at"]), Kit.HUE_INFO
        else:
            n = len(gd["members"])
            status = "%s, %d online, %d in view; read %s" % (Kit.count(n, "member"), online, inview, ago(gd["at"]))
            if gd["note"]:
                status += "  (%s)" % gd["note"]
            hue = Kit.HUE_INFO
        set_info(info[5], status, tw, hue)
        shown, pg = page_of(items)
        Kit.set_text(c["pg"], pg)
        for r, (serial, m) in zip(win["rows"], shown):
            # Health is read for the rows shown only.
            d = full_mob(serial) if serial else None
            if d is not None:
                stat, hue, frac = mobile_status(serial)
            elif m["online"]:
                stat, hue, frac = "Online", Kit.HUE_GOOD, None
            else:
                stat, hue, frac = (m["laston"] or "offline"), Kit.HUE_INFO, None
            # You (also after the saved copy was loaded) get the title colour.
            if m["me"] or (me_name and mkey(m) == me_name):
                nhue = Kit.HUE_TITLE
            elif d is not None or m["online"]:
                nhue = Kit.HUE_GOOD if d is None else Kit.HUE_TEXT
            else:
                nhue = Kit.HUE_INFO
            set_row(r, serial if d is not None else 0, m["name"], stat, hue, frac,
                    extra={"rank": m["rank"], "title": m["title"]}, name_hue=nhue, bar=d is not None)
        for r in win["rows"][len(shown):]:
            hide_row(r)

    NOTE_BODY_H = 104
    NOTE_H = Kit.MARGIN + 30 + Kit.GAP + NOTE_BODY_H + Kit.MARGIN

    def open_note(name):
        """Open the note window for name; one at a time, a new name replaces the old window. It sits
        where it was last left, else beside this module's window.
        """
        notew.close()
        w, h = NOTE_W, NOTE_H
        dx, dy = 240, 180
        if Kit.is_open(win["g"]):
            dx, dy = win["g"].GetX() + 40, win["g"].GetY() + 60
        # Position given when no saved one exists.
        g, store, c = notew.begin(w, h, (dx, dy))
        Kit.add_window_frame(g, w, h)
        Kit.add_section(g, M, M, w - 2 * M, 30)
        Kit.add_label(g, "PLAYER NOTE", M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, "Close without saving",
                       on_click=queue("note_close"))
        IW = w - 2 * M
        yb = M + 30 + Kit.GAP
        Kit.add_section(g, M, yb, IW, NOTE_BODY_H)
        lx = M + 12
        fx = lx + max(Kit.text_w("Player:"), Kit.text_w("Note:")) + 10
        Kit.add_label(g, "Player:", lx, yb + 13)
        c["name"] = Kit.with_tip(Kit.add_textbox(g, name, fx, yb + 10, 200, numbers=False),
                                 "Player name as shown over their head (any case)")
        Kit.add_label(g, "Note:", lx, yb + 43)
        c["text"] = Kit.with_tip(Kit.add_textbox(g, NOTES.get(name.lower(), ("", ""))[1], fx, yb + 40,
                                                 M + IW - 12 - fx, numbers=False),
                                 "Your note (up to %d letters); saving it empty deletes it" % NOTE_CHARS)
        by = yb + 72
        Kit.art_button(g, store, "save", Kit.ART_OK, lx, by, "Save",
                       "Save the note for every character of this account", on_click=queue("note_save"))
        Kit.art_button(g, store, "delete", Kit.ART_CLOSE, lx + 35 + Kit.text_w("Save") + 16, by,
                       "Delete", "Delete this note", on_click=queue("note_delete"))
        hint = "Kept per account"
        Kit.add_label(g, hint, M + IW - 12 - Kit.text_w(hint), by + 3, Kit.HUE_INFO)
        notew.end(g, {"name": name})

    # A second window of this module for the note; it keeps its own place under the note position key.
    notew = Kit.Window(KEY, TITLE, None, ed, open_note, NOTE_POS_KEY, cleanup=cleanup, lock=False, owner=False,
                       clear={"c": {}, "store": ({}, {})})

    def note_fields():
        """The player name and note text as typed in the note window, read on the client thread. Falls
        back to the name the window was opened for.
        """
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

    def read_msg():
        """Text of the chat field (empty when there is none), read once and kept across a rebuild."""
        tb = win["c"].get("msg")
        return "" if tb is None else str(tb.Text or "").strip()

    def clear_msg():
        """Empty the chat field and forget what was kept for this tab."""
        tb = win["c"].get("msg")
        if tb is not None:
            tb.SetText("")
        st["msg"].pop(settings["tab"], None)

    SAY = {"psend": "PartyMsg", "gsend": "GuildMsg", "asend": "AllyMsg"}

    def send_chat(fn, txt):
        """Say txt through the API chat call named fn, then clear the field. An empty text says so."""
        if not txt:
            say("type something first.")
            return
        getattr(API, fn)(txt)
        clear_msg()

    def add_friend(serial):
        """Add the mobile to TazUO's friends list. Refuses with a journal line for nothing targeted, you,
        a mobile not in view or an existing friend. Asks for a fresh read of the list afterwards.
        """
        serial = int(serial or 0)
        if not serial:
            say("nothing targeted.")
            return
        if serial == player_serial():
            say("that's you.")
            return
        m = API.FindMobile(serial)
        if m is None:
            say("target a player or creature in view.", Kit.HUE_BAD)
            return
        name = str(m.Name or "")
        who = name or "0x%08X" % serial
        if serial in [int(s) for s in API.GetAllFriends() or ()] or any(s == serial for s, _ in st["friends"]):
            say("%s is already a friend." % who)
        elif API.AddFriend(serial):
            if name:
                st["names"][serial] = name
                st["names_dirty"] = True
            say("%s added to friends." % who, Kit.HUE_GOOD)
            # Already in view, so it is not announced as coming into view.
            if st["seen"] is not None:
                # A new set: seen may be the very set st inview holds.
                st["seen"] = st["seen"] | {serial}
        else:
            say("couldn't add %s to friends (the client refused)." % who, Kit.HUE_BAD)
        st["next_friends"] = 0.0

    def remove_friend(serial):
        """Remove the friend from TazUO's friends list and ask for a fresh read of it."""
        name = st["names"].get(serial, "") or "0x%08X" % serial
        if API.RemoveFriend(serial):
            say("%s removed from friends." % name)
        else:
            say("couldn't remove %s from friends (the client refused)." % name, Kit.HUE_BAD)
        if st["seen"]:
            st["seen"].discard(serial)
        st["next_friends"] = 0.0

    def row_remove(serial):
        """Remove the serial the clicked row showed: on the Friends tab from TazUO's list, on the Party tab
        through the client's party request when you lead the party.
        """
        if not serial:
            return
        if win["tab"] == "friends":
            remove_friend(serial)
        elif win["tab"] == "party":
            party = st["party"]
            if party and party[0] and party[0] == player_serial():
                if not CL.game_action("RequestPartyRemoveMember", [to_uint(serial)], False):
                    say("couldn't remove them (%s)." % CL.error, Kit.HUE_BAD)
            else:
                say("only the leader can remove members.")

    def clear_inviter():
        """Clear the party invitation after Accept or Decline was sent, on the client thread. The server's
        answer does not clear World.Party.Inviter, so the client's own party window clears it after its
        send and this does the same; otherwise the invitation would stay shown.
        """
        with Kit.quiet:
            import System
            party = Typing._get(CL.world, "Party") if CL.world is not None else None
            if party is not None:
                Tz.put(party, "Inviter", System.UInt32(0))
        # The row goes now, not at the next read.
        p = st["party"]
        if p:
            st["party"] = (p[0], 0, p[2], p[3])

    def to_uint(serial):
        """A serial as the client's unsigned 32-bit type, which its methods need through reflection; the
        number itself when that cannot be made.
        """
        try:
            import System
            return System.UInt32(int(serial))
        except Exception:
            return serial

    # What each window button calls: (GameActions method, whether it takes your serial, whether it
    # takes the world). The ignore list is opened by its own routine.
    WINS = {"paperdoll": ("OpenPaperdoll", True, True), "status": ("OpenStatusBar", False, True),
            "gwin": ("OpenGuildGump", False, True), "invite": ("RequestPartyInviteByTarget", False, False),
            "edit": ("RequestProfile", True, False), "ignore": None}

    def open_window(what):
        """Open a client window by its WINS key, the way the Action Bar does. Says why in the journal when
        it cannot. Returns True when it opened.
        """
        e = WINS[what]
        if e is None:
            ok = CL.open_ignore_list()
        else:
            ok = CL.game_action(e[0], [to_uint(player_serial())] if e[1] else (), e[2])
        if not ok:
            say("couldn't open that (%s)." % (CL.error or "no client access"), Kit.HUE_BAD)
        return ok

    def party_window():
        """Open the client's own party window by running its Open PartyManifest macro."""
        world = CL.world
        if world is None:
            say("couldn't open the party window (no client access: %s)." % CL.error, Kit.HUE_BAD)
            return

        def run():
            """Client-thread body of party_window: build the macro object and hand it to the macro manager."""
            import System
            mgr = Typing._get(world, "Macros")
            asm = mgr.GetType().Assembly
            mo_t, mt_t, ms_t = [asm.GetType("ClassicUO.Game.Managers." + n)
                                for n in ("MacroObject", "MacroType", "MacroSubType")]
            mo = System.Activator.CreateInstance(mo_t, System.Array[object]([System.Enum.Parse(mt_t, "Open", True),
                 System.Enum.Parse(ms_t, "PartyManifest", True)]))
            CL.call(mgr, "SetMacroToExecute", [mo])
            CL.call(mgr, "Update")
            return True

        if not CL.on_main(run):
            say("couldn't open the party window (%s)." % CL.error, Kit.HUE_BAD)

    def diplomacy_job():
        """Script-thread job: open the guild window if it is not open, then press its Diplomacy button.
        The button is found by its caption, else by the id in the settings. A guild window already
        open is used as it is, since asking for another would close it and a press on the old one
        would be dropped.
        """
        gid, raw = last_gump()
        # The page is recognised by classify; its captions are clilocs, not plain text.
        if not (gid and classify(raw) in ("guild", "roster")):
            gid = CL.find_server_gump(guild_test)[0]
        if not gid:
            if not CL.game_action("OpenGuildGump"):
                say("couldn't ask for the guild window (%s)." % CL.error, Kit.HUE_BAD)
                return
            gid, _raw, _kind = wait_gump(lambda r2: classify(r2) in ("guild", "roster") and "ok")
        if not gid:
            say("the guild window didn't come (are you in a guild?).", Kit.HUE_BAD)
            return
        if not press(gid, DIPLOMACY_LABEL, settings["dbutton"]):
            say("no %s button found; press it in the guild window (or set its id in Social settings)."
                 % DIPLOMACY_LABEL)

    def click_mobile(serial):
        """A row was clicked: answer a target cursor that is open, else make the mobile your last target."""
        if API.HasTarget("any") and not HOST.cursor_busy(KEY):
            # The mother's check before a target cursor is answered with this mobile.
            if HOST.harm_ok(serial, "social.row", TITLE):
                API.Target(serial)
            return
        API.SetLastTarget(to_uint(serial))
        m = API.FindMobile(serial)
        if m is None:
            say("%s isn't in view." % (st["names"].get(serial, "") or "they"))
        else:
            say("%s is your last target." % (str(m.Name or "") or "that"))

    def start_guild_read():
        """Queue a read of the guild window, one at a time. Returns False when one is running."""
        if st["guild_busy"]:
            return False
        # Shows as Reading until the job takes over, and the automatic read waits a retry period.
        st["guild_busy"] = True
        st["guild_next"] = time.time() + GUILD_RETRY
        jobs.append(guild_job)
        return True

    def announce():
        """Say in the journal when a friend comes into view and, with the option on, when one leaves.
        The friends already in view when it is first switched on are not announced.
        """
        now_in = st["inview"]
        if not (settings["announce"] or settings["left"]) or st["seen"] is None:
            st["seen"] = now_in
            return
        if settings["announce"]:
            for s in now_in - st["seen"]:
                say("%s is in view." % mob_name(s, "a friend"), Kit.HUE_GOOD)
        if settings["left"]:
            for s in st["seen"] - now_in:
                say("%s left view." % mob_name(s, "a friend"))
        st["seen"] = now_in

    def party_action(action):
        """Leave the party or switch loot on or off, through the client's party requests. Says when it
        cannot.
        """
        party = st["party"]
        if not in_party(party):
            say("not in a party.")
        elif action == "leave":
            if not CL.game_action("RequestPartyRemoveMember", [to_uint(player_serial())], False):
                say("couldn't leave (%s)." % CL.error, Kit.HUE_BAD)
        elif CL.game_action("RequestPartyLootState", [not party[2]], False):
            say("party %s loot your corpse." % ("may not" if party[2] else "may"))
        else:
            say("couldn't change looting (%s)." % CL.error, Kit.HUE_BAD)

    def answer_invite(action):
        """Answer the party invitation. Accepting sends the request and clears the invitation in one
        client hop. The client has no call for declining, so the decline packet is sent through its
        network extension, which sends it and returns nothing.
        """
        inv = to_uint(st["party"][1])
        if action == "accept":
            def accept():
                """Client-thread body of accepting."""
                if not CL.game_action("RequestPartyAccept", [inv], False):
                    return None
                clear_inviter()
                return True

            if CL.on_main(accept) is None:
                say("couldn't accept (%s)." % CL.error, Kit.HUE_BAD)
            return
        net = Client._type("ClassicUO.Network.AsyncNetClient")
        ext = Client._type("ClassicUO.Network.NetClientExt")

        def decline():
            """Client-thread body of declining."""
            CL.call(None, "Send_PartyDecline", [Typing._get(None, "Socket", net), inv], ext)
            clear_inviter()
            return True

        if net is None or ext is None or CL.on_main(decline) is None:
            say("couldn't decline (%s)." % CL.error, Kit.HUE_BAD)

    def next_sort():
        """Step the roster to the next order, save it, and update the Sort button's caption and tip in
        place. Goes back to page one and asks for a list pass at once.
        """
        i = SORT_CODES.index(settings["gsort"]) if settings["gsort"] in SORT_CODES else 0
        settings["gsort"] = SORT_CODES[(i + 1) % len(SORT_CODES)]
        save_settings()
        c = win["c"]
        lbl = c.get("gsort")
        if lbl is not None:
            Kit.set_text(lbl, sort_caption(c))
        btn = c.get("gsort_btn")
        if btn is not None and c.get("gsort_bare"):
            Kit.with_tip(btn, sort_tip(c))
        st["page"]["guild"] = 0
        st["next_list"] = 0.0

    def guild_refresh():
        """Refresh button: read the guild window again, or say that a read is already running. A read
        asked for reports its failure.
        """
        st["guild_said"] = ""
        if start_guild_read():
            refresh()
        else:
            say("already reading the guild window.")

    # Actions that carry an argument (a serial or name) and plain actions, by the name the queue
    # holds.
    WITH_ARG = {"click": click_mobile, "rm": row_remove, "follow": lambda serial: Follow.toggle(serial, TITLE),
                "noview": lambda name: say("%s isn't in view." % name),
                "picked": lambda serial: serial and add_friend(serial)}
    ACTIONS = {"pwin": party_window, "note_close": notew.close, "gsort": next_sort, "grefresh": guild_refresh,
               "leave": lambda: party_action("leave"), "loot": lambda: party_action("loot"),
               "add_last": lambda: add_friend(int(API.LastTargetSerial or 0))}
    # Layout of this module's page in the mother's Settings tab.
    PAGE_OPTS = {"ldy": 4, "fw": 40, "ltip": True, "clamp": False}

    def page_table(w):
        """Describe this module's page of the Settings tab for width w: window, friends and guild window
        groups of checks and number fields.
        """
        return (("WINDOW", (("note", fit("Shift+click a row to note that player; %d saved for this account."
                                         % len(NOTES), w - 28)),
                            ("note", fit("Action Bar cells can show this window (Client window, page 2).", w - 28)),
                            ("check", "bars", "Show health bars", "A bar for everyone in view; off, rows show name, "
                             "status and distance"),
                            ("num", "rows", "Rows per page:", "Rows on the Friends, Party and Guild tabs; the window "
                             "grows to fit", None, ROWS_MIN, ROWS_MAX))), ("FRIENDS  (journal lines)", (
                    ("check", "announce", "Say when a friend comes into view",
                     "One line when a friend comes into view (not those in view at start)"),
                    ("check", "left", "Say when a friend leaves view", "One line when a friend in view is gone"))),
                ("GUILD WINDOW  (for the Guild tab)", (("check", "ghide", "Read the guild window hidden",
                     "It opens invisible for the read; off, it shows for a few seconds", {"h": 28}),
                    ("num", "gevery", "Read it again every:", "Minutes between reads while the Guild tab shows (0-%d, "
                     "0 = only on Refresh)" % GUILD_EVERY_MAX, "min", 0, GUILD_EVERY_MAX),
                    ("num", "dbutton", "Diplomacy button id:", "Pressed when the Diplomacy caption isn't found; "
                     "ServUO uses %d (0-%d, 0 = caption only)" % (DIPLOMACY_BUTTON, DIPLOMACY_BUTTON_MAX), None, 0,
                     DIPLOMACY_BUTTON_MAX)), {"pad": 8}))

    def on_change(old, new):
        """Settings changed: rebuild the window when the bars, rows or (on the Guild tab) hiding changed,
        and forget what was seen when announcing is switched on, so nobody in view is announced at once.
        """
        if (new["bars"], new["rows"]) != (old["bars"], old["rows"]) or (new["ghide"] != old["ghide"]
                                                                        and old["tab"] == "guild"):
            st["rebuild"] = True
        if (new["announce"] or new["left"]) and not (old["announce"] or old["left"]):
            st["seen"] = None

    # The first start right after the module was built, for the same character, uses what the build
    # loaded: names, guild copy and notes were read just then and nothing can have saved them since.
    cfg = Kit.Page(settings, page_table, save_settings, on_change, PAGE_OPTS)
    LOADED_FOR = [0]
    load_settings()
    LOADED_FOR[0] = player_serial()

    def _start():
        """Module start: reset the run state, load saved data when the character changed, find the client
        classes, draw the window, register it with the zone layout and offer notes to other modules
        through the social.note service.
        """
        # Everything the pass caches starts empty; the minimized state is as it was left.
        st.update({"shutting": False, "docked": False, "queue": [], "page": {}, "mobs": {},
                   "inview": set(), "seen": None, "next_list": 0.0, "next_friends": 0.0,
                   "next_profile": 0.0, "guild_busy": False, "guild_dirty": False,
                   "guild_next": 0.0, "guild_fails": 0, "guild_said": "", "guild_pages": 0,
                   "ghid": 0, "view": {}, "view_serials": None, "allies": [], "fit": None,
                   "me_s": 0, "friends_raw": None, "kept": {}, "prof_part": False,
                   "again_for": None, "again_build": False, "minimized": wnd.start_min()})
        # Nothing queued before a stop runs now.
        del jobs[:]
        if not (LOADED_FOR[0] and LOADED_FOR[0] == player_serial()):
            load_settings()
        LOADED_FOR[0] = 0
        CL.find()
        build_window()
        # Exact means the window is drawn exactly the slot a zone gives it; verify has the layout measure
        # it every pass; min keeps a zone from going below the fixed part.
        wnd.dock(layout_fit, exact=True, verify=True, min=min_size)
        # Ultima Tracker reads notes for its row tooltips through this service.
        cleanup.service("social.note", note_of)

    def _tick():
        """Client tick: handle the queued clicks, rebuild when asked, then (at most every LIST_EVERY
        seconds) read what the shown tab needs and refresh. Folded into the Action Bar it still
        announces friends in view when that setting is on.
        """
        if win["g"] is None:
            return
        # Closing the window turns the module off.
        if Kit.closed(win):
            return
        # One lookup of the queue; the start makes a new list.
        q = st["queue"]
        while q:
            action = q.pop(0)
            kind = action[0] if isinstance(action, tuple) else action
            if action == "to_bar" or (action == "toggle_min" and not st["minimized"]):
                # Keep what was typed before the window is redrawn or folded.
                st["msg"][settings["tab"]] = read_msg()
            if action == "redraw":
                st["rebuild"] = True
            # The window's own actions (fold, minimize, close, settings) come first.
            elif wnd.action(action):
                continue
            elif kind in WITH_ARG:
                WITH_ARG[kind](action[1])
            elif action in ACTIONS:
                ACTIONS[action]()
            elif kind == "tab":
                if action[1] != settings["tab"]:
                    st["msg"][settings["tab"]] = read_msg()
                    settings["tab"] = action[1]
                    save_settings()
                    st["rebuild"] = True
            elif kind == "page":
                st["page"][settings["tab"]] = max(0, st["page"].get(settings["tab"], 0) + action[1])
                st["next_list"] = 0.0
            elif action == "add":
                say("target the friend to add.")
                # The pick answers from the shared target helper, not from this module's tick; the answer is
                # queued back to it.
                HOST.pick_target(PICK_TIMEOUT, lambda serial: queue.add(("picked", int(serial or 0)), dup=True))
            elif action in WINS:
                if open_window(action) and action == "invite":
                    say("target who to invite.")
            elif action in ("accept", "decline") and st["party"] and st["party"][1]:
                answer_invite(action)
            elif action in SAY:
                send_chat(SAY[action], read_msg())
            elif action == "diplo":
                # Waits for the server: never on this tick.
                jobs.append(diplomacy_job)
            elif action == "war":
                # Toggle war and peace.
                API.SetWarMode(not API.Player.InWarMode)
            elif kind == "note":
                if str(action[1]).startswith("0x"):
                    say("name not known yet.")
                else:
                    open_note(action[1])
            elif action in ("note_save", "note_delete"):
                if ed["g"] is not None:
                    name, text = note_fields()
                    if set_note(name, text if action == "note_save" else ""):
                        notew.close()
        if st["rebuild"]:
            if not st["minimized"]:
                st["msg"][settings["tab"]] = read_msg()
            build_window()
            return
        if st["guild_dirty"]:
            st["guild_dirty"] = False
            st["next_list"] = 0.0
        now = time.time()
        # The time test first: most ticks end here.
        if now < st["next_list"] <= now + LIST_EVERY:
            return
        # Folded into the bar nothing is drawn; with both announce options off it does nothing and the
        # first look afterwards is silent.
        folded = st["minimized"] and st["docked"]
        if folded and not (settings["announce"] or settings["left"]):
            st["seen"] = None
            return
        st["next_list"] = now + LIST_EVERY
        read_friends()
        tab = "mini" if st["minimized"] else win["tab"]
        # Only the mobiles the window shows are read in full (each costs a mobile lookup and several
        # property reads): the rows of the current page, the party's leader and inviter, and the guild
        # members and allies in view. Every friend gets a presence check only, for the in view counts
        # and the announcements.
        wanted = set()
        st["view_serials"] = None
        if tab == "mini":
            if not folded:
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
            # The automatic guild re-read, only while the Guild tab shows.
            if (settings["gevery"] and not st["guild_busy"] and now >= st["guild_next"]
                    and now - gd["at"] >= settings["gevery"] * 60):
                start_guild_read()
        if tab in ("guild", "profile"):
            read_profile(tab == "profile")
        mobs = {}
        # On the Guild tab the members and allies in view get their name and distance from the scan,
        # which is all the roster's order needs; their health is read for the rows shown only (the row
        # data's last slot is None until then).
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
        # Friends in the data are in view; the rest get the presence check.
        for s in st["fserials"]:
            if s in mobs:
                inview.add(s)
            else:
                rest.append(s)
        # The presence check runs only when something shows or announces it.
        if tab == "friends" or (tab == "mini" and not folded) or settings["announce"] or settings["left"]:
            inview |= friends_in_view(rest)
        st["inview"] = inview
        announce()
        refresh()

    def _thread_tick():
        """Script thread, right after the client tick: run the waiting jobs one by one until none are
        left or the module is stopping.
        """
        while jobs and not st["shutting"]:
            jobs.pop(0)()

    def _stop():
        """Module stop: save settings, names and any note not yet saved, then clean up."""
        st["shutting"] = True
        save_settings()
        # Forced dirty so the final save of the names always happens.
        st["names_dirty"] = True
        save_names()
        save_notes()
        cleanup.close()

    # Hooks of the module: start, stop and the client tick, the settings page, and the thread tick
    # which runs only when a job waits.
    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed,
            "thread_tick": _thread_tick, "thread_wanted": lambda: bool(jobs)}


# Without the mother's HOST, the stand-in file _Alone.py supplies one so the module can start by itself.
if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
HOST.add("social", "Social", "Friends, party, guild and profile", _module_social, 0.1, category="The world")
