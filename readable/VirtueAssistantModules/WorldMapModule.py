# =============================================================================
# World Map - a Virtue Assistant module (TazUO Legion script, IronPython 3.4)
# Shard: In Mani Ylem. Module key: "worldmap". Category: "The world".
#
# This file is not a script to run on its own. It is one module of Virtue Assistant, loaded by the
# mother script from the modules folder beside it. The mother provides everything used here (API,
# G, safe, Client, Kit, Follow, HOST, Journal, the main loop and the settings window), so run the
# mother and tick World Map on its Modules tab. Taking this file out of the folder leaves the
# module out.
#
# The module is made of PARTS. Each part has its own box under the module's row on the Modules tab
# and runs only while it is ticked; the mother's PartSet runs the ticked parts side by side. Each
# part keeps its own saved keys, window places, lists and files.
#
#     Map Pings        Send and receive guild pings on your Enhanced Map
#     Corpse           An arrow to your corpse, how long it lasts, and Get my things
#     Treasure Maps    The dig spots of your decoded treasure maps
#     Ore Tracker      Your weight, and the ore, wood, fish and sand spots that ran dry
#     Traps & Fields   Traps and magic fields recoloured so you see them
#
# Map Pings starts first: the other parts send their pings through its pings.send service.
#
# The parts also share the Atlas (below), which puts their places on TazUO's own World Map as
# named user markers.
def _module_worldmap():
    """Builds the World Map module from its parts and returns its hooks.

    The shared Atlas and helpers come first, then the parts: Map Pings, Corpse, Treasure Maps, Ore
    Tracker and Traps & Fields. Every coordinate pair the parts show goes through xy, so streamer
    mode can hide where things are.
    """
    # Module identity: the key the mother, the Action Bar and HOST.by_key know this module by.
    KEY = "worldmap"
    TITLE = "World Map"
    # Everything the Atlas writes into TazUO's marker file carries this prefix, so our markers can be
    # told from the player's own and removed by exact name.
    ATLAS_PREFIX = "VA "
    # Global persistent var: one line per marker we have placed in TazUO's marker file, so markers
    # left behind by a stopped script can be taken out later.
    ATLAS_PLACED_KEY = "WorldMap_atlas_placed"
    # Per-character persistent var: "corpse=1;maps=1;dry=1;traps=1", which owners show on the map.
    ATLAS_ON_KEY = "WorldMap_atlas"
    # Owner key and the wording used in the "Show ... on TazUO's World Map" tick box.
    ATLAS_OWNERS = (("corpse", "your corpse"), ("maps", "your dig spots"),
                    ("dry", "the spots that ran dry"), ("traps", "the traps you have seen"))
    # Seconds between looks for the World Map while markers wait to be written.
    ATLAS_CHECK = 1.0
    # The same look while the map is closed; slower, as the settle wait is 2 s anyway.
    ATLAS_CLOSED_CHECK = 2.5
    # Seconds one walk over the open windows is reused by every caller.
    GUMP_EVERY = 0.5
    # Seconds the map must have been open before markers are written: TazUO reads its marker file as
    # the map opens, and a write before that would be lost or doubled.
    ATLAS_SETTLE = 2.0
    # Marker adds or removes per pass at most: each one is a write to TazUO's file.
    ATLAS_OPS = 3
    # Markers of ours on the map at most.
    ATLAS_CAP = 60
    # Shared result of the open-window walk: time of the walk, whether it could read the windows, and
    # whether the World Map and a tracking arrow are open.
    GUMPS = {"at": -1.0, "ok": False, "map": False, "arrow": False}

    def gump_flags(fresh=False):
        """Which TazUO windows are open: {"ok", "map", "arrow"}.

        "map" is TazUO's World Map, "arrow" a tracking arrow (QuestArrowGump). The answer comes from a
        walk over the client's open windows at most GUMP_EVERY seconds old (fresh=True walks now). "ok"
        is False when the windows could not be read. Client thread.
        """
        memo = GUMPS
        # One walk serves every caller for a moment: the Atlas, Map Pings' markers and the arrow checks
        # of Treasure Maps and Ore Tracker would each ask several times a second otherwise, and a walk
        # over the open windows is not free.
        now = time.time()
        if not fresh and 0.0 <= now - memo["at"] < GUMP_EVERY:
            return memo
        memo["at"] = now
        mp = ar = False
        try:
            # Only the two window types we care about are asked for, so the walk can stop early.
            names = [str(w.GetType().Name) for w in Tz.windows(("WorldMapGump", "QuestArrowGump"))]
            mp, ar = "WorldMapGump" in names, "QuestArrowGump" in names
            memo["ok"] = True
        except Exception:
            memo["ok"] = False
        memo["map"], memo["arrow"] = mp, ar
        return memo

    class Atlas(object):
        """The Atlas: puts the parts' places on TazUO's World Map as named user markers.

        Each part says what it wants shown with set(owner, {name: (x, y, facet, color)}). Nothing
        touches the client while that matches what is on the map. Otherwise tick looks whether the map
        is open and, after it has been open ATLAS_SETTLE seconds, adds and removes ATLAS_OPS markers a
        pass. A Legion script can only use API.AddMapMarker and API.RemoveMapMarker, and only while the
        World Map is open; both go through TazUO's marker file (Data/Client/userMarkers.usr), so a
        marker added stays after the map is closed. Placed names are kept in a Global persistent var so
        markers left when the script stopped with the map closed are stripped from the file next time
        (by exact name: the player's own markers are never touched).
        """
        def __init__(self):
            """Starts empty and in sync; load fills it from the saved keys on first use."""
            # items: owner -> {name: (x, y, facet, color)} the owner wants. on: owner -> shown (the part's
            # page). placed: name -> value written to TazUO's file. want: what should be on the map now.
            # loose: other names to take out of the file (Map Pings' markers).
            self.items, self.on, self.placed, self.want, self.loose = {}, {}, {}, {}, set()
            # want == placed: nothing to do.
            self.synced = True
            self.open_since = self.saved = None
            self.next_check = 0.0
            # strip_pending: markers left in the file by the last run; the script thread strips them.
            self.loaded = self.strip_pending = False
            # chg: name -> new saved line, or None for a removal; applied by _save.
            self.chg = {}

        def load(self):
            """Read the saved owner switches and placed markers, once. Client thread.

            Marker lines are "name|x|y|facet|color"; a damaged line is skipped.
            """
            if self.loaded:
                return
            self.loaded = True
            for k, v in Kit.codec_load(Kit.get_var(ATLAS_ON_KEY)).items():
                self.on[k] = v != "0"
            text = str(API.GetPersistentVar(ATLAS_PLACED_KEY, "", API.PersistentVar.Global) or "")
            for line in text.split("\n"):
                p = line.split("|")
                if len(p) == 5 and p[0].startswith(ATLAS_PREFIX):
                    try:
                        self.placed[p[0]] = (int(p[1]), int(p[2]), int(p[3]), p[4])
                    except ValueError:
                        pass
            self.saved = text
            # Markers left from the last run with the map closed are taken out of TazUO's file by thread_work
            # on the script thread: load runs on the client thread, where a file read and write would be a
            # frame hitch.
            self.strip_pending = bool(self.placed) and not self.map_open(True)
            self._rebuild()

        def is_on(self, owner):
            """Is the owner's part shown on the map (on unless the player unticked it)?"""
            self.load()
            return self.on.get(owner, True)

        def set_on(self, owner, on):
            """Switch an owner on or off, save the choice and rebuild the wanted set."""
            self.load()
            if self.on.get(owner, True) != bool(on):
                self.on[owner] = bool(on)
                Kit.put_var(ATLAS_ON_KEY, ";".join(
                    "%s=%d" % (k, 1 if self.on.get(k, True) else 0) for k, _w in ATLAS_OWNERS))
                self._rebuild()

        def set(self, owner, items):
            """The markers the owner wants shown now: {name: (x, y, facet, color)}.

            Names start with ATLAS_PREFIX and hold no comma (TazUO's file is CSV).
            """
            self.load()
            if self.items.get(owner) != items:
                self.items[owner] = dict(items)
                self._rebuild()

        def clear(self, owner):
            """The owner wants nothing shown any more."""
            if self.items.pop(owner, None):
                self._rebuild()

        def _rebuild(self):
            """Work out what should be on the map: every owner that is switched on, capped at ATLAS_CAP."""
            want = {}
            for owner, items in self.items.items():
                if self.on.get(owner, True):
                    for name, v in items.items():
                        if len(want) >= ATLAS_CAP:
                            break
                        want[name] = v
            self.want = want
            # Compared as whole dicts, so a pass that finds them equal costs nothing afterwards.
            self.synced = want == self.placed

        def map_open(self, fresh=False):
            """Is TazUO's World Map open? False when it can't be told.

            Uses the shared walk; fresh=True for callers that act on the answer at once (stop, the file
            strip, a new marker).
            """
            f = gump_flags(fresh)
            return f["ok"] and f["map"]

        def tick(self):
            """The module's tick (client thread): bring the markers on the map in line with the wanted ones.

            Does nothing unless the map has been open long enough, and then at most ATLAS_OPS changes.
            """
            # The strip is under way or pending: placed must not change meanwhile.
            if self.synced or self.strip_pending:
                return
            now = time.time()
            # Not time to look yet; a wait longer than the settle plus a check means the clock went back, so
            # look anyway.
            if now < self.next_check and self.next_check - now <= ATLAS_SETTLE + ATLAS_CHECK:
                return
            if not self.map_open():
                self.open_since = None
                # Closed: a slower look next time.
                self.next_check = now + ATLAS_CLOSED_CHECK
                return
            if self.open_since is None or self.open_since > now:
                self.open_since = now
            if now - self.open_since < ATLAS_SETTLE:
                self.next_check = self.open_since + ATLAS_SETTLE
                return
            # The shared walk can be 0.5 s old and every operation below needs the map, so look again now.
            if not self.map_open(True):
                self.open_since = None
                self.next_check = now + ATLAS_CLOSED_CHECK
                return
            # The next few operations follow a quarter second apart.
            self.next_check = now + 0.25
            ops = 0
            for name in list(self.placed):
                if ops >= ATLAS_OPS:
                    break
                # A name that is placed but wanted differently (or not at all) comes off first.
                if self.want.get(name) != self.placed[name]:
                    API.RemoveMapMarker(name)
                    self._drop(name)
                    ops += 1
            for name, v in self.want.items():
                if ops >= ATLAS_OPS:
                    break
                if name not in self.placed:
                    API.AddMapMarker(name, v[0], v[1], v[2], v[3])
                    self._put(name, v)
                    ops += 1
            self.synced = self.want == self.placed
            self._save()

        def thread_work(self):
            """The module's thread_tick (script thread): take leftover markers out of TazUO's file.

            Strips what the last run left behind while the map is closed, and Map Pings' leftovers. One try
            only, so a failing file never makes a loop.
            """
            if not self.strip_pending and not self.loose:
                return
            # The open windows are read on the client thread (one hop; this thread may wait).
            is_open = Kit.on_client(lambda: self.map_open(True))
            if self.strip_pending:
                if not is_open and self._strip_file():
                    self._drop_all()
                    self._save()
                # Map open (tick removes them itself) or the strip failed: either way stop trying.
                self.strip_pending = False
                self.synced = self.want == self.placed
            if self.loose:
                if is_open:
                    for name in list(self.loose):
                        API.RemoveMapMarker(name)
                else:
                    # Map closed: the names go from the file instead.
                    self._strip_file()
                self.loose.clear()

        def _put(self, name, v):
            """Record a marker as placed and queue its line for saving."""
            self.placed[name] = v
            self.chg[name] = "%s|%d|%d|%d|%s" % (name, v[0], v[1], v[2], v[3])

        def _drop(self, name):
            """Record a marker as gone and queue the removal for saving."""
            self.placed.pop(name, None)
            self.chg[name] = None

        def _drop_all(self):
            """Forget every placed marker."""
            for name in list(self.placed):
                self._drop(name)

        def _save(self):
            """Save queued changes to the Global var. Client thread."""
            if not self.chg:
                return
            try:
                # Read the stored text again and merge only our changes into it, because the var is shared by
                # every character on this install.
                raw = str(API.GetPersistentVar(ATLAS_PLACED_KEY, "", API.PersistentVar.Global) or "")
            except Exception:
                return
            text = Kit.merge_text(raw, self.chg, lambda l: l.split("|", 1)[0])[0]
            self.chg = {}
            self.saved = text
            safe(lambda: API.SavePersistentVar(ATLAS_PLACED_KEY, text, API.PersistentVar.Global))

        def shutdown(self):
            """The module stops: our markers come off TazUO's map.

            With the map open this goes through the API; with it closed, out of TazUO's marker file (read
            again when the map opens), by exact name.
            """
            self.items.clear()
            self.want = {}
            self.strip_pending = False
            if not self.placed and not self.loose:
                self.synced = True
                return
            if self.map_open(True):
                for name in list(self.placed) + list(self.loose):
                    API.RemoveMapMarker(name)
                self._drop_all()
            elif self._strip_file():
                self._drop_all()
            self.loose.clear()
            self.synced = not self.placed
            self._save()

        def _strip_file(self):
            """Take our lines out of TazUO's userMarkers.usr (map closed).

            Returns True when the file holds none of our names now (or there is no file).
            """
            try:
                # TazUO's own folder, where its dll is.
                exe = str(Tz.get(None, "ExecutablePath", Tz.T("ClassicUO.CUOEnviroment")))
                folder = os.path.join(exe, "Data", "Client")
                if not os.path.isdir(folder):
                    # Not TazUO's folder after all: leave it.
                    return False
                path = os.path.join(folder, "userMarkers.usr")
                if not os.path.exists(path):
                    return True
                import io
                with io.open(path, "r", encoding="utf-8-sig") as f:
                    lines = f.read().splitlines()
                gone = set(self.placed) | self.loose
                # Name is the fourth CSV column; only exact names of ours are dropped.
                keep = [ln for ln in lines if len(ln.split(",")) < 4 or ln.split(",")[3] not in gone]
                if len(keep) != len(lines):
                    # Written through Kit.write_safe rather than a plain write, since the file is TazUO's.
                    Kit.write_safe(path, u"".join(l + u"\n" for l in keep))
                return True
            except Exception:
                return False

    # The one Atlas, shared by all parts.
    ATLAS = Atlas()

    def atlas_name(text):
        """A marker name: our prefix, no commas (TazUO's file is CSV)."""
        return ATLAS_PREFIX + str(text).replace(",", " ")

    def arrow_open(fresh=False):
        """Is a tracking arrow still on screen?

        TazUO's arrow closes with a right-click and nothing tells the script. True when it can't be
        told, so a working arrow is never taken for a closed one. Uses the shared walk.
        """
        f = gump_flags(fresh)
        return f["arrow"] if f["ok"] else True

    # owner -> its "Show ... on TazUO's World Map" box while its page is open.
    ATLAS_BOX = {}

    def atlas_page(owner):
        """Settings page section for one owner's World Map tick box.

        Returns (title, rows, options) as the settings page builder expects.
        """
        def draw(f, x, y):
            """Draw the tick box for the owner at (x, y) on the page."""
            ATLAS_BOX[owner] = Kit.add_check(f.g, "Show %s on TazUO's World Map" % dict(ATLAS_OWNERS).get(owner, owner),
                                             x + 12, y, ATLAS.is_on(owner), "Markers named \"%s...\" while the map is "
                                             "open; removed when unticked or the part stops" % ATLAS_PREFIX)

        return "TAZUO'S WORLD MAP  (while open)", (("custom", 26, draw),), {"sh": 66}

    def with_atlas(api, owner):
        """Wrap a part's hooks: poll its World Map tick box and clear its markers when it stops.

        api is the part's hook dict; owner is its Atlas owner key. Returns a new dict.
        """
        old_poll, old_closed, old_stop = api["poll_config"], api["config_closed"], api["stop"]

        def poll():
            """Settings window poll: pass on to the part, then apply a changed World Map tick box."""
            old_poll()
            cb = ATLAS_BOX.get(owner)
            if cb is not None:
                try:
                    on = bool(cb.IsChecked)
                except Exception:
                    return
                if on != ATLAS.is_on(owner):
                    ATLAS.set_on(owner, on)

        def closed():
            """Settings window closed: forget the box."""
            old_closed()
            ATLAS_BOX.pop(owner, None)

        def stop():
            """The part stops: its markers leave the map even if its own stop fails."""
            try:
                old_stop()
            finally:
                ATLAS_BOX.pop(owner, None)
                ATLAS.clear(owner)

        out = dict(api)
        out.update({"poll_config": poll, "config_closed": closed, "stop": stop})
        return out

    atlas_err = {"said": False}

    def atlas_tick():
        """The module's tick: run the Atlas, tell the player once if it throws."""
        try:
            ATLAS.tick()
        except Exception as ex:
            if not atlas_err["said"]:
                atlas_err["said"] = True
                API.SysMsg("%s: couldn't update TazUO's World Map (%s)." % (TITLE, ex), Kit.HUE_BAD)

    def atlas_thread():
        """The module's thread_tick: run the Atlas file work; never raises."""
        try:
            ATLAS.thread_work()
        except Exception:
            ATLAS.strip_pending = False

    # Hooks shared by the whole module (the parts add their own).
    SHARED = {"tick": atlas_tick, "stop": ATLAS.shutdown, "thread_tick": atlas_thread,
              # Run the script thread step only while there is something to strip.
              "thread_wanted": lambda: ATLAS.strip_pending or ATLAS.loose}
    # Names a journal line may start with in capitals.
    JOURNAL_NAMES = ("TazUO", "World Map", "Map Pings", "Enhanced Map", "Virtue Assistant",
                     "Settings", "Inventory", "Need help", "Look here", "Go here", "Danger!")

    def journal_case(text):
        """A status or window line as a journal message: first letter lower case.

        Left as is when it starts with a name from JOURNAL_NAMES or a bracketed tag or quote.
        """
        text = str(text or "")
        if not text or text[0] in "[(\"'" or text.startswith(JOURNAL_NAMES):
            return text
        return text[0].lower() + text[1:]

    def xy(x, y, fmt="%d, %d"):
        """Format a map position for display, hidden in streamer mode.

        fmt is the pattern for the two numbers (x then y); the result goes through Kit.veil("xy"), which
        returns it unchanged unless streamer mode is on.
        """
        return Kit.veil("xy", fmt % (x, y))

    def list_h(rows, row_h):
        """Height of a list window with the given rows of row_h pixels each."""
        return 2 * Kit.MARGIN + 30 + 2 * Kit.GAP + 36 + 30 + rows * row_h + 8

    def told(wnd, st, mw, mh):
        """The slot the layout gives window wnd, or None when it has none, is minimised, is not in a
        layout that holds, or is smaller than mw by mh.
        """
        z = wnd.slot
        if z is None or st["minimized"] or not HOST.layout_holds(wnd.key) or z[0] < mw or z[1] < mh:
            return None
        return z

    def _part_pings():
        """Builds the Map Pings part and returns its hooks.

        Send and receive guild pings on your Enhanced Map. Pings travel through TazUO's own Enhanced
        Map connection when it is on (Options > Enhanced Map), or through a separate map login entered
        on the settings page. Send with the mouse wheel held down over a spot and dragged (up Look
        here, right Danger!, down Go here, left Need help; let go without dragging to cancel), with a
        button on the settings page or with a hotkey then a click on the target cursor. Pings from
        Enhanced Map users show here and ours show on their maps. Other parts send pings through the
        HOST service "pings.send". The History window lists recent pings; a row puts the tracking arrow
        on that spot again. Runs on the client thread (tick) and the script thread (thread_tick).
        """
        # Part key, and the title used in journal lines and the window.
        KEY = "pings"
        TITLE = "Map Pings"
        # Default port of the Enhanced Map server for a separate login.
        DEFAULT_PORT = 8887
        # Hotkey defaults; the player rebinds them on the settings page ("" means none).
        HOTKEYS = {"look": "CTRL+1", "danger": "CTRL+2", "go": "CTRL+3", "help": "CTRL+4",}
        HOTKEY_ORDER = ("look", "danger", "go", "help")
        # Ping markers kept on the World Map at most, so they can be taken off again.
        MARKERS_CAP = 60
        # Your own pings go out at most this often.
        PING_RATE_SECS = 0.75
        # Seconds one socket write may take, on the sender thread only.
        SEND_TIMEOUT = 5
        # UO sound ids per ping type (look, danger, go, help): Bless, Explosion, Recall, Greater Heal.
        PING_SOUNDS = (0x1EA, 0x307, 0x1FC, 0x202)
        # Pings kept in the History window's list; the oldest is dropped.
        HISTORY_MAX = 200
        HISTORY_ROWS = 10
        # The socket module may be missing or broken in the runtime: the .NET transport then does the
        # same job.
        try:
            import socket
            import select
            _HAVE_PY_SOCKET = True
        except Exception:
            _HAVE_PY_SOCKET = False
        import collections
        # Saved keys of this part start with this prefix (the part's earlier name, kept so saved settings
        # carry over).
        VAR_PREFIX = "EMPings."
        OPT_KEY = VAR_PREFIX + "options"
        # Ping type numbers, the same as on the wire and in TYPE_INFO.
        LOOK, DANGER, GO, HELP = 0, 1, 2, 3
        CONNECTIONS = [("auto", "TazUO's map if on, else my login"), ("tazuo", "Only TazUO's Enhanced Map"),
                       ("own", "Only my own login")]
        CONN_CODES = [c[0] for c in CONNECTIONS]
        # Allowed range of the two number fields: seconds a ping stays, and the drag distance in pixels.
        OPT_LIMITS = {"ping_secs": (2, 60), "drag": (5, 200)}
        # Current settings; DEFAULTS keeps what a fresh character gets.
        settings = {"sounds": True, "share": True, "gesture": True, "connection": "auto", "ping_secs": 8, "drag": 25}
        DEFAULTS = dict(settings)
        # Window state shared by the part's callbacks (minimised, shutting down, docked, queued work).
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "app": None}
        # The settings window: its gump, its controls, and the last drawn contents.
        win = {"g": None, "c": {}, "store": ({}, {})}
        cleanup, queue, say = Kit.basics(st, TITLE)

        def load_settings():
            """Read the saved options into settings and HOTKEYS, clamping numbers to their limits.

            Saved format: key=value pairs joined by semicolons under OPT_KEY; hotkeys are hk_<type>.
            """
            for k, v in Kit.codec_load(Kit.get_var(OPT_KEY)).items():
                if k in ("sounds", "share", "gesture"):
                    settings[k] = v == "1"
                elif k == "connection" and v in CONN_CODES:
                    settings[k] = v
                elif k in OPT_LIMITS:
                    try:
                        lo, hi = OPT_LIMITS[k]
                        settings[k] = max(lo, min(hi, int(v)))
                    except ValueError:
                        pass
                elif k.startswith("hk_") and k[3:] in HOTKEYS:
                    HOTKEYS[k[3:]] = _norm_key(v)

        def save_settings():
            """Save settings and hotkeys to the per-character var in the same key=value format."""
            data = "sounds=%d;share=%d;gesture=%d;connection=%s" % (
                settings["sounds"], settings["share"], settings["gesture"], settings["connection"])
            data += "".join(";hk_%s=%s" % (k, HOTKEYS[k].replace(";", "")) for k in HOTKEY_ORDER)
            data += ";ping_secs=%d;drag=%d" % (int(settings["ping_secs"]), int(settings["drag"]))
            Kit.put_var(OPT_KEY, data)

        def build_window():
            """Placeholder: the settings page code below draws everything, so there is no window of its own
            to build.
            """
            pass

        wnd = None

        def refresh():
            """Placeholder: no window of its own to refresh; the settings page code does it."""
            pass

        # Button actions of the settings page, filled in by the page code.
        ACTIONS = {}
        TYPE_KEYS = {"look": LOOK, "danger": DANGER, "go": GO, "help": HELP}
        # Drag direction of the mouse gesture to ping type.
        GESTURE = {"up": LOOK, "right": DANGER, "down": GO, "left": HELP}
        # Per type: label, UO hue for the text, effect graphic, World Map colour name.
        TYPE_INFO = {LOOK:   ("Look here", 53,     0x373A,     "yellow"),
            DANGER: ("Danger!",   33,     0x3709,     "red"), GO:     ("Go here",   68,     0x376A,     "green"),
            HELP:   ("Need help", 88,     0x375A,     "blue"),}
        # Tracking arrow id (the ASCII of PING): one arrow, for the newest ping.
        ARROW_ID = 0x50494E47

        def label_of(t):
            """The player-facing label of a ping type."""
            return TYPE_INFO[t][0]

        def facet_name(m):
            """Name of a facet number, or "map N" for one we don't know."""
            return Kit.FACETS[m] if 0 <= m < len(Kit.FACETS) else "map %d" % m

        def packet(pid, payload=b""):
            """One Enhanced Map packet: id (1 byte), total length (2 bytes, little endian), then the payload."""
            return struct.pack("<BH", pid, 3 + len(payload)) + payload

        def pk_login(user, password):
            """Login packet: user name and password, Latin-1, each length-prefixed."""
            u, p = user.encode("latin-1", "replace"), password.encode("latin-1", "replace")
            return packet(0x1F, struct.pack("<BB", len(u), len(p)) + u + p)

        def pk_alert(x, y):
            """Alert packet (0x27) holding an x and y of 16 bits each."""
            return packet(0x27, struct.pack("<HH", x & 0xFFFF, y & 0xFFFF))

        # Old map servers only relay alerts, which carry nothing but x and y. UO coordinates never need
        # the top bits (maps are at most 7168 x 4096), so ping type and facet ride in the spare bits:
        # x has bit 15 as the marker, bits 13-14 the type and bits 0-12 the x; y has bit 15 as the
        # marker, bits 12-14 the facet and bits 0-11 the y. Plain alerts from anyone else never have
        # bit 15 set.
        TYPED_ALERT_FLAG = 0x8000

        def decode_typed_alert(ax, ay):
            """Unpack a ping tucked into an alert.

            Returns (x, y, facet, type), or None when the alert is a plain one.
            """
            if not (ax & TYPED_ALERT_FLAG and ay & TYPED_ALERT_FLAG):
                return None
            return ax & 0x1FFF, ay & 0x0FFF, (ay >> 12) & 0x7, (ax >> 13) & 0x3

        def pk_typed_alert(x, y, m, t):
            """Build an alert that carries a ping type and facet, or None when a value doesn't fit the bits."""
            if 0 <= x < 0x2000 and 0 <= y < 0x1000 and 0 <= m < 8 and 0 <= t < 4:
                return pk_alert(TYPED_ALERT_FLAG | (t << 13) | x, TYPED_ALERT_FLAG | (m << 12) | y)

        def pk_player_data(pos, stats, flag, color):
            """Player data packet (0x25) that shows you on guildmates' Enhanced Maps.

            pos is (x, y, z); stats are hp, stam, mana, maxhp, maxstam, maxmana, each clamped to 16 bits;
            flag and the name colour (ARGB) follow. The font is Arial, size 12, bold.
            """
            return packet(0x25, struct.pack("<HHB6HBBBIB", pos[0] & 0xFFFF, pos[1] & 0xFFFF, pos[2] & 0xFF,
                          *([max(0, min(v, 0xFFFF)) for v in stats] + [flag, 0, 0, color & 0xFFFFFFFF, 5]))
                          + b"Arial" + struct.pack("<fB", 12.0, 1))

        class Reader(object):
            """Reads fields from one packet's bytes, after the 3 byte header."""
            def __init__(self, data, offset=3):
                """Wrap data and start at offset (past the packet id and length)."""
                self.d, self.p = data, offset

            def take(self, n):
                """The next n bytes. Raises ValueError("short packet") instead of reading past the end."""
                if self.p + n > len(self.d):
                    raise ValueError("short packet")
                self.p += n
                return self.d[self.p - n:self.p]

            def u8(self):
                """One unsigned byte."""
                return bytearray(self.take(1))[0]

            def u16(self):
                """One little endian unsigned 16 bit number."""
                return struct.unpack("<H", self.take(2))[0]

            def ascii(self, n):
                """n bytes read as Latin-1 text."""
                return bytes(self.take(n)).decode("latin-1")

        class PySocketTransport(object):
            """Map server transport over Python sockets, used when the socket module works. Same send, recv
            and close interface as DotNetTransport.
            """
            def __init__(self, host, port, timeout):
                """Connect (timeout in seconds), then use SEND_TIMEOUT for writes."""
                self.s = socket.create_connection((host, port), timeout)
                self.s.settimeout(SEND_TIMEOUT)

            def send(self, data):
                """Write all the bytes."""
                self.s.sendall(data)

            def recv(self):
                """Bytes waiting, or b"" if none. Raises EOFError when the server closed."""
                # A zero timeout select: never blocks the thread.
                r, _, _ = select.select([self.s], [], [], 0)
                if not r:
                    return b""
                data = self.s.recv(8192)
                if not data:
                    raise EOFError()
                return data

            def close(self):
                """Close the socket; errors ignored."""
                safe(lambda: self.s.close())

        class DotNetTransport(object):
            """Map server transport over .NET's TcpClient, for runtimes where Python sockets don't work."""
            def __init__(self, host, port, timeout):
                """Connect without waiting forever: the connect runs as a task and is waited on for timeout."""
                # Only importable under IronPython.
                import clr
                from System.Net.Sockets import TcpClient, SelectMode
                self._select_read = SelectMode.SelectRead
                # The .NET types are looked up once here, not on every call.
                from System import Array, Byte
                self._Array, self._Byte = Array, Byte
                self.c = TcpClient()
                task = self.c.ConnectAsync(host, port)
                if not task.Wait(int(timeout * 1000)) or not self.c.Connected:
                    self.c.Close()
                    raise IOError("timed out")
                self.st = self.c.GetStream()
                self.st.WriteTimeout = int(SEND_TIMEOUT * 1000)

            def send(self, data):
                """Write the bytes to the network stream."""
                buf = self._Array[self._Byte](bytearray(data))
                self.st.Write(buf, 0, len(buf))

            def recv(self):
                """Bytes waiting, or b"" if none. Raises EOFError when the server closed."""
                if not self.c.Connected:
                    raise EOFError()
                n = self.c.Available
                # Readable with nothing to read means the peer closed.
                if n <= 0:
                    if self.c.Client.Poll(0, self._select_read):
                        raise EOFError()
                    return b""
                buf = self._Array.CreateInstance(self._Byte, n)
                got = self.st.Read(buf, 0, n)
                if got <= 0:
                    raise EOFError()
                return bytes(bytearray(buf)[:got])

            def close(self):
                """Close the connection; errors ignored."""
                safe(lambda: self.c.Close())

        def open_transport(host, port, timeout=5):
            """Open a transport to host:port, Python sockets first, then .NET.

            Network errors from Python sockets are real answers and are raised as they are. Any other
            failure means the socket module is broken in this runtime, so .NET is tried.
            """
            if _HAVE_PY_SOCKET:
                try:
                    return PySocketTransport(host, port, timeout)
                except (socket.timeout, socket.gaierror, ConnectionError, OSError):
                    raise
                except Exception:
                    pass
            return DotNetTransport(host, port, timeout)

        class Sender(object):
            """Writes to a transport on a thread of its own.

            send only queues the bytes; the worker writes them. A stalled map server would otherwise stall
            every module's thread work for up to the 5 s write timeout per packet. The first write error
            is kept in error and picked up by MapConnection.poll, which drops the connection. Without
            threads the writes happen in place.
            """
            def __init__(self, transport):
                """Start the worker thread on transport."""
                self.t = transport
                self.error = self.cond = None
                self.stopped = False
                self.q = collections.deque()
                try:
                    import threading
                    self.cond = threading.Condition()
                    th = threading.Thread(target=self._run)
                    th.daemon = True
                    th.start()
                except Exception:
                    # No threads available: send in place.
                    self.cond = None

            def send(self, data):
                """Queue data for the worker; raises the stored error when the sender has failed or stopped."""
                if self.error is not None or self.stopped:
                    raise self.error or IOError("sender stopped")
                if self.cond is None:
                    self.t.send(data)
                    return
                with self.cond:
                    self.q.append(data)
                    self.cond.notify()

            def _run(self):
                """Worker thread: take queued packets and write them, one at a time, until stopped or a write fails."""
                # The client refuses scripts that hold the always-true loop, so the loop tests the stop flag.
                while not self.stopped:
                    with self.cond:
                        while not self.q and not self.stopped:
                            # Wakes on a notify, or every half second to look at the stop flag.
                            self.cond.wait(0.5)
                        if self.stopped:
                            return
                        data = self.q.popleft()
                    try:
                        self.t.send(data)
                    except Exception as ex:
                        self.error = ex
                        return

            def stop(self):
                """Stop the worker and drop whatever is still queued."""
                self.stopped = True
                if self.cond is not None:
                    with self.cond:
                        self.q.clear()
                        self.cond.notify()

        class MapConnection(object):
            """Talks to EnhancedMapServer with a separate login.

            poll returns a list of events: ("status", text, loud), ("ping", name, x, y, map, type),
            ("alert", name, x, y) and ("message", text). loud means worth a journal line; quiet ones only
            update the panel. Runs on the script thread; nothing here blocks it (connects and writes have
            threads of their own).
            """
            # Which kind of connection this is, for the status text and the choice of link.
            kind = "own"
            # This login shares the player's position; TazUO's connection already does that itself.
            owns_position = True
            # A server with its own login always relays the ping packet.
            server_relays_ping = True
            OFF, HANDSHAKE, LOGIN, READY = range(4)

            def __init__(self, host, port, user, password):
                """Remember the server and login. Starts off, nothing connected, backoff at 3 s."""
                self.host, self.port, self.user, self.password = host, port, user, password
                # connecting: a connect running on its own thread. sender: the writer of the open transport.
                self.t = self.gave_up = self.connecting = self.sender = None
                self.state = self.OFF
                self.buf = bytearray()
                self.next_try = self.login_failures = self.last_sent = self.state_since = self.ready_since = 0
                # Seconds to wait before the next try; doubles on failure up to 60.
                self.backoff = 3
                # Times the server dropped us after login, to notice a loop of drops.
                self.kicks = []
                self.name = user
                self.unreachable_reported = False

            def close(self):
                """Close everything: a connect still running (it closes what it opens when it ends), the sender
                and the transport. Safe to call at any time.
                """
                # A connect is still running on its thread: tell it to drop whatever it opens.
                if self.connecting is not None:
                    pend, self.connecting = self.connecting, None
                    with pend["lock"]:
                        pend["abandon"] = True
                        done = pend["done"]
                    # It had just finished: close what it opened.
                    if done and pend["t"] is not None:
                        pend["t"].close()
                if self.sender is not None:
                    self.sender.stop()
                    self.sender = None
                if self.t:
                    self.t.close()
                self.t = None
                self.state = self.OFF
                self.buf = bytearray()

            def _drop(self, events, kind, detail, retry_in):
                """The connection ended: close it, tell the panel why and schedule the next try.

                events gets the status tuples. kind is "eof" (server closed), "error", "timeout" or "garbled";
                detail is text for the panel; retry_in is seconds. Gives up (gave_up set) after 3 refused
                logins or 4 drops inside 5 minutes.
                """
                was = self.state
                self.close()
                now = time.time()
                # The server says nothing when it rejects a login; it just closes the connection.
                if was == self.LOGIN and kind == "eof":
                    self.login_failures += 1
                    if self.login_failures >= 3:
                        self.gave_up = "Login refused 3 times. Check the map username and password."
                        events.append(("status", self.gave_up, True))
                        return
                    events.append(("status", "Login refused (wrong username or password?). Retrying in %d s."
                                   % retry_in, True))
                elif was == self.LOGIN:
                    events.append(("status", "Login problem (%s). Retrying in %d s." % (detail, retry_in), True))
                elif was == self.READY:
                    # Dropped within seconds of a good login usually means the same account is logged in elsewhere.
                    if kind == "eof" and now - self.ready_since < 6:
                        why = "Dropped right after login. Is this map account logged in elsewhere (Enhanced Map)?"
                    elif kind == "eof":
                        why = "Lost the map server."
                    else:
                        why = "Connection problem (%s)." % detail
                    self.kicks = [k for k in self.kicks if now - k < 300] + [now]
                    if len(self.kicks) >= 4:
                        self.gave_up = ("Kept getting dropped. Is this map account logged in elsewhere (Enhanced "
                                        "Map)? Use a separate account, then click Reconnect.")
                        events.append(("status", self.gave_up, True))
                        return
                    events.append(("status", "%s Reconnecting in %d s." % (why, retry_in), True))
                else:
                    what = {"eof": "Server closed the connection",
                            "timeout": "Server didn't answer"}.get(kind, "Connection problem")
                    events.append(("status", "%s (%s). Retrying in %d s."
                                   % (what, detail or "handshake", retry_in), False))
                self.next_try = now + retry_in

            def reset(self):
                """Forget a give-up and every failure count, and close; the player clicked Reconnect."""
                self.close()
                self.gave_up = None
                self.login_failures = self.next_try = 0
                self.kicks = []
                self.backoff = 3

            @property
            def ready(self):
                """Logged in and ready to send and receive."""
                return self.state == self.READY

            def send(self, data):
                """Queue data for the sender thread (never blocks the script's thread). A failed send closes the
                connection and retries in 3 s.
                """
                if not self.t:
                    return
                try:
                    if self.sender is not None:
                        self.sender.send(data)
                    else:
                        self.t.send(data)
                    self.last_sent = time.time()
                except Exception:
                    self.close()
                    self.next_try = time.time() + 3

            def poll(self):
                """Main pump, called every step on the script thread. Connects, reads, handles every complete
                packet and returns the events found.
                """
                events = []
                now = time.time()
                if self.gave_up:
                    return events
                if self.t is None:
                    if now < self.next_try:
                        # A connect runs on a thread of its own: it can take up to its 5 s timeout (an unreachable
                        # server, slow DNS), and on the script's thread that would stop every module.
                        return events
                    pend = self.connecting
                    if pend is None:
                        import threading
                        pend = self.connecting = {"done": False, "t": None, "err": None, "abandon": False,
                                                  "lock": threading.Lock()}

                        def run(p=pend, host=self.host, port=self.port):
                            """The connect thread: open the transport, record the result, and close it here if the
                            connection was abandoned meanwhile.
                            """
                            try:
                                p["t"] = open_transport(host, port)
                            except Exception as ex:
                                p["err"] = ex
                            with p["lock"]:
                                p["done"] = True
                                gone = p["abandon"]
                            if gone and p["t"] is not None:
                                p["t"].close()

                        try:
                            th = threading.Thread(target=run)
                            th.daemon = True
                            th.start()
                        except Exception:
                            # No threads here: connect in place.
                            run()
                    if not pend["done"]:
                        return events
                    self.connecting = None
                    now = time.time()
                    try:
                        if pend["err"] is not None:
                            raise pend["err"]
                        if pend["t"] is None:
                            raise IOError("no connection")
                        self.t = pend["t"]
                    except Exception as e:
                        self.backoff = min(self.backoff * 2, 60)
                        events.append(("status", "Can't reach the map server at %s:%d (%s). Retrying in %d s."
                                       % (self.host, self.port, short_error(e), self.backoff),
                                       not self.unreachable_reported))
                        self.unreachable_reported = True
                        self.next_try = now + self.backoff
                        return events
                    self.state = self.HANDSHAKE
                    self.state_since = now
                    self.buf = bytearray()
                    # Writes go on a thread of their own.
                    self.sender = Sender(self.t)
                    # The protocol request that starts the handshake.
                    self.send(packet(0x2B, b"\x00"))
                    events.append(("status", "Connecting", False))
                # (kind, detail) if the connection ended during this read.
                closed = None
                snd = self.sender
                if snd is not None and snd.error is not None:
                    # A write failed on the sender thread.
                    e = snd.error
                    closed = ("error", "%s: %s" % (e.__class__.__name__, short_error(e)))
                try:
                    # One read per step is plenty, and it avoids relying on select staying accurate across
                    # back-to-back reads in IronPython.
                    chunk = self.t.recv() if self.t else b""
                    if chunk:
                        self.buf.extend(chunk)
                        if len(self.buf) > 1 << 20:
                            raise IOError("too much data")
                except EOFError:
                    closed = ("eof", "")
                except Exception as e:
                    closed = ("error", "%s: %s" % (e.__class__.__name__, short_error(e)))
                # Handle every complete packet first: the server may have sent its reply just before closing,
                # and that reply says what happened.
                while len(self.buf) >= 3 and self.t is not None:
                    pid = self.buf[0]
                    size = self.buf[1] | (self.buf[2] << 8)
                    if size < 3:
                        self._drop(events, "garbled", "bad packet size", 10)
                        return events
                    if len(self.buf) < size:
                        break
                    data = bytes(self.buf[:size])
                    del self.buf[:size]
                    try:
                        self._handle(pid, data, events)
                    except ValueError:
                        pass
                if closed and self.t is not None:
                    self._drop(events, closed[0], closed[1], 30 if self.state == self.LOGIN else 10)
                    return events
                # Handshake or login taking too long.
                if (self.t is not None and self.state in (self.HANDSHAKE, self.LOGIN) and now - self.state_since > 15):
                    self._drop(events, "timeout", "no reply in 15 s", 15)
                return events

            def _handle(self, pid, data, events):
                """React to one packet: the handshake reply, the login result, or a ping, alert or message to pass
                on as an event.
                """
                r = Reader(data)
                if pid == 0x2B and self.state == self.HANDSHAKE:
                    self.state = self.LOGIN
                    self.state_since = time.time()
                    self.send(pk_login(self.user, self.password))
                elif pid == 0x1F and self.state == self.LOGIN:
                    # Login result: 1 means accepted.
                    if r.u8() == 1:
                        r.u8()
                        self.name = r.ascii(r.u8()) or self.user
                        self.state = self.READY
                        self.ready_since = time.time()
                        self.login_failures = 0
                        self.backoff = 3
                        self.unreachable_reported = False
                        events.append(("status", "Connected as %s." % self.name, True))
                    else:
                        self._drop(events, "eof", "login rejected", 30)
                elif pid in (0x33, 0x27) and self.state == self.READY:
                    events.append(parse_ping(pid, r))
                elif pid == 0x2F and self.state == self.READY:
                    events.append(("message", r.ascii(r.u16())))

        def parse_ping(pid, r):
            """Turn a ping (0x33) or alert (0x27) the server relayed into an event tuple.

            An unknown ping type counts as Look here. Everything else the server sends (positions, chat,
            labels) is for Enhanced Map and ignored.
            """
            if pid == 0x33:
                x, y, m, t = r.u16(), r.u16(), r.u8(), r.u8()
                return ("ping", r.ascii(r.u8()), x, y, m, t if t in TYPE_INFO else LOOK)
            x, y = r.u16(), r.u16()
            return ("alert", r.ascii(r.u8()), x, y)

        class TazUOBridge(object):
            """Rides on TazUO's built-in Enhanced Map connection through .NET reflection.

            TazUO has its own Enhanced Map client but doesn't expose it to scripts. Sends go through its
            SendRaw (thread-safe, uses its socket lock). For receiving, a handler is added next to
            TazUO's own OnFrame handler and removed when the script stops. TazUO runs OnFrame on its
            Enhanced Map network thread, inside the loop that reads the socket: if a handler throws,
            TazUO treats it as a broken connection, drops it and reconnects 10 s later. A Python handler
            throws once its script has stopped (Legion shuts the Python runtime down), so one left behind
            would drop the connection on every packet after each reconnect. The handler is therefore plain
            .NET (built with System.Linq.Expressions): it only queues ping and alert frames, never runs
            Python and can't throw. Hooking also clears any handler on OnFrame that isn't TazUO's own. If
            TazUO changes these internals, the script says so and falls back to a separate login.
            """
            # AppDomain slot holding our handler, so a later run can find and remove one left by a run that
            # did not clean up.
            HOOK_KEY = "EMPings.OnFrameHook"

            def __init__(self):
                """Find TazUO's Enhanced Map manager, client and the members used, and make the frame handler.

                Raises when anything is missing, which is how Map Pings learns the internals have changed.
                """
                import clr
                clr.AddReference("System.Collections.Concurrent")
                from System import Array, Byte, Action, Delegate, AppDomain
                from System.Reflection import BindingFlags
                from System.Collections.Concurrent import ConcurrentQueue
                self._Array, self._Byte, self._Delegate, self._AppDomain = (Array, Byte, Delegate, AppDomain)
                inst = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance
                stat = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static
                # Private TazUO types and members, found by name.
                mtype = API.GetType().Assembly.GetType("ClassicUO.Game.Managers.EnhancedMap.EnhancedMapManager")
                p_instance = mtype.GetProperty("Instance", stat)
                self._p_connected = mtype.GetProperty("IsConnected", inst)
                self._p_config = mtype.GetProperty("Config", stat)
                self._m_reconnect = mtype.GetMethod("Reconnect", inst)
                f_client = mtype.GetField("_client", inst)
                # TazUO's own code, to tell its handlers from ours (see _own_handlers_only).
                self._asm = API.GetType().Assembly
                self._manager = p_instance.GetValue(None)
                self._client = f_client.GetValue(self._manager)
                ctype = self._client.GetType()
                self._f_connection = ctype.GetField("_connection", inst)
                self._m_send = ctype.GetMethod("SendRaw", inst)
                self._f_onframe = ctype.GetField("OnFrame", inst)
                try:
                    # The pure .NET handler. If this machine can't compile expressions, a Python handler does the
                    # same job: fine while the script runs, and a stopped run's copy is cleared on the next hook.
                    self._handler, self._queue = self._make_handler()
                except Exception:
                    self._queue = ConcurrentQueue[object]()
                    fq = self._queue

                    def on_frame(pid, payload):
                        """Python fallback handler: queue ping and alert frames, at most 200; never raises."""
                        try:
                            if pid in (0x33, 0x27) and fq.Count < 200:
                                fq.Enqueue((int(pid), payload))
                        except Exception:
                            pass

                    self._handler = Action[Byte, Array[Byte]](on_frame)
                self._hooked = False

            @staticmethod
            def _make_handler():
                """Build a pure .NET Action<byte, byte[]> that queues ping (0x33) and alert (0x27) frames.

                Returns (handler, queue). At most 200 frames wait in the queue. It runs on TazUO's network
                thread and never calls back into Python, so it keeps working (harmlessly) after the script
                stops.
                """
                import clr
                clr.AddReference("System.Collections.Concurrent")
                clr.AddReference("System.Linq.Expressions")
                from System import Array, Byte, Int32, Action, Tuple, Type
                from System.Collections.Concurrent import ConcurrentQueue
                from System.Linq.Expressions import Expression, ParameterExpression
                t_byte, t_bytes, t_int = (clr.GetClrType(Byte), clr.GetClrType(Array[Byte]), clr.GetClrType(Int32))
                ftype = Tuple[Byte, Array[Byte]]
                fq = ConcurrentQueue[ftype]()
                p_id = Expression.Parameter(t_byte, "id")
                p_payload = Expression.Parameter(t_bytes, "payload")
                q = Expression.Constant(fq)
                as_int = Expression.Convert(p_id, t_int)
                wanted = Expression.OrElse(Expression.Equal(as_int, Expression.Constant(0x33, t_int)),
                                           Expression.Equal(as_int, Expression.Constant(0x27, t_int)))
                room = Expression.LessThan(Expression.Property(q, "Count"), Expression.Constant(200, t_int))
                ctor = clr.GetClrType(ftype).GetConstructor(Array[Type]([t_byte, t_bytes]))
                enqueue = Expression.Call(q, fq.GetType().GetMethod("Enqueue"), Array[Expression]([Expression.New(ctor,
                                                  Array[Expression]([p_id, p_payload]))]))
                body = Expression.IfThen(Expression.AndAlso(wanted, room), enqueue)
                lam = Expression.Lambda[Action[Byte, Array[Byte]]](body, Array[ParameterExpression]([p_id, p_payload]))
                return lam.Compile(), fq

            def hook(self):
                """Add our handler to TazUO's OnFrame, first removing a leftover of ours and any handler that
                isn't TazUO's own. No-op when already hooked.
                """
                if self._hooked:
                    return
                domain = self._AppDomain.CurrentDomain
                current = self._f_onframe.GetValue(self._client)
                # A leftover from a run that did not clean up.
                leftover = domain.GetData(self.HOOK_KEY)
                if leftover is not None:
                    current = self._Delegate.Remove(current, leftover)
                current = self._own_handlers_only(current)
                self._f_onframe.SetValue(self._client, self._Delegate.Combine(current, self._handler))
                domain.SetData(self.HOOK_KEY, self._handler)
                self._hooked = True

            def _own_handlers_only(self, current):
                """TazUO's own OnFrame handlers, without any a stopped script left behind (those would throw and
                drop the connection).

                TazUO's own are the ones on its EnhancedMapManager, and any other handler whose code is
                compiled into TazUO itself. Only handlers made at run time (IronPython, or the .NET one built
                in _make_handler) are cleared. When the list can't be read it is returned as it is.
                """
                if current is None:
                    return None
                try:
                    keep = None
                    for d in current.GetInvocationList():
                        if ((d.Target is not None and d.Target.Equals(self._manager)) or self._tazuo_code(d)):
                            keep = self._Delegate.Combine(keep, d)
                    return keep
                except Exception:
                    return current

            def _tazuo_code(self, d):
                """Does delegate d run a method compiled into TazUO's assembly?"""
                try:
                    return bool(d.Method.Module.Assembly.Equals(self._asm))
                except Exception:
                    return False

            def unhook(self):
                """Take our handler off OnFrame and clear the AppDomain slot."""
                if not self._hooked:
                    return
                try:
                    current = self._f_onframe.GetValue(self._client)
                    self._f_onframe.SetValue(self._client, self._Delegate.Remove(current, self._handler))
                    self._AppDomain.CurrentDomain.SetData(self.HOOK_KEY, None)
                finally:
                    self._hooked = False

            def config(self):
                """TazUO's Enhanced Map settings (enabled, configured, user, address, port, send location) as a
                dict, or None when it has none.
                """
                c = self._p_config.GetValue(None)
                if c is None:
                    return None
                return {"enabled": bool(c.Enabled), "configured": bool(c.IsConfigured), "user": str(c.Username or ""),
                        "address": str(c.Address or ""), "port": int(c.Port), "send_location": bool(c.SendLocation)}

            def is_connected(self):
                """Is TazUO's Enhanced Map connected right now?"""
                return bool(self._p_connected.GetValue(self._manager))

            def send(self, data):
                """Send raw bytes on TazUO's connection; nothing happens when there is no connection."""
                conn = self._f_connection.GetValue(self._client)
                if conn is None:
                    return
                buf = self._Array[self._Byte]([int(b) for b in bytearray(data)])
                self._m_send.Invoke(self._client, self._Array[object]([conn, buf]))

            def reconnect(self):
                """Ask TazUO to reconnect its Enhanced Map."""
                self._m_reconnect.Invoke(self._manager, None)

            def frames(self):
                """Take the queued ping and alert frames as (packet id, payload bytes) pairs."""
                out = []
                # The queue never holds more than 200.
                for _ in range(200):
                    ok, item = self._queue.TryDequeue()
                    if not ok:
                        break
                    # The Python fallback handler queues plain tuples.
                    if isinstance(item, tuple):
                        pid, payload = item
                    # The .NET handler's queue holds Tuple<byte, byte[]>.
                    else:
                        pid, payload = item.Item1, item.Item2
                    out.append((int(pid), bytes(bytearray([int(b) for b in payload]))))
                return out

        class TazUOMouse(object):
            """Reads TazUO's mouse state through reflection (not exposed to scripts): the middle button, the
            cursor position and the world object under the cursor.
            """
            def __init__(self):
                """Find the mouse fields and properties in TazUO's assembly."""
                import clr
                from System.Reflection import BindingFlags
                stat = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static
                asm = API.GetType().Assembly
                mouse = asm.GetType("ClassicUO.Input.Mouse")
                selected = asm.GetType("ClassicUO.Game.SelectedObject")
                ui = asm.GetType("ClassicUO.Game.Managers.UIManager")
                self._pos = mouse.GetField("Position", stat)
                self._mclick = mouse.GetField("MClickPosition", stat)
                self._mdown = mouse.GetProperty("MButtonPressed", stat)
                self._mdown_get = None
                self._over_world = ui.GetProperty("IsMouseOverWorld", stat)
                self._object = selected.GetField("Object", stat)

            def middle_down(self):
                """Is the middle (wheel) button held down?"""
                get = self._mdown_get
                # The bound property reader, made once.
                if get is None:
                    get = self._mdown_get = self._mdown.GetValue
                return bool(get(None))

            def position(self, f=None):
                """Cursor position (x, y) in the client window's pixels; f picks another field, such as the
                position of the last middle click.
                """
                p = (self._pos if f is None else f).GetValue(None)
                return int(p.X), int(p.Y)

            def tile_under_mouse(self):
                """World (x, y) of the ground, item or mobile under the cursor, or None (for example over a gump)."""
                if not bool(self._over_world.GetValue(None)):
                    return None
                obj = self._object.GetValue(None)
                if obj is None:
                    return None
                fx, fy = xy_fields(obj.GetType())
                if fx is None or fy is None:
                    return None
                x, y = int(fx.GetValue(obj)), int(fy.GetValue(obj))
                return (x, y) if x > 0 and y > 0 else None

        class TazUOLink(object):
            """Same interface as MapConnection, but rides on TazUO's own login.

            Watches the connection state, reports drops, and lets go of TazUO's connection if it keeps
            dropping, since the cause is then not us.
            """
            kind = "tazuo"
            # TazUO already shares the player's position itself.
            owns_position = False
            # Seconds in which drops are counted.
            DROP_WINDOW = 120
            # Drops inside DROP_WINDOW before Map Pings stops listening.
            DROP_LIMIT = 3

            def __init__(self, bridge):
                """Hook TazUO's connection through bridge."""
                self.bridge = bridge
                self.bridge.hook()
                self.was_connected = None
                self.drops = []
                # Set once a ping packet (0x33) has come in through TazUO's connection.
                self.unhooked_for_drops = self.server_relays_ping = False

            @property
            def ready(self):
                """TazUO's Enhanced Map is connected."""
                return self.bridge.is_connected()

            @property
            def name(self):
                """The Enhanced Map user name set in TazUO, or ""."""
                return (self.bridge.config() or {}).get("user", "")

            def poll(self):
                """Report connection changes and return the pings and alerts that arrived."""
                events = []
                connected = self.ready
                if connected != self.was_connected:
                    if connected:
                        events.append(("status", "Using TazUO's Enhanced Map login (%s)."
                                       % (self.name or "connected"), True))
                    elif self.was_connected:
                        now = time.time()
                        # Drops are counted in a sliding window.
                        self.drops = [d for d in self.drops if now - d < self.DROP_WINDOW] + [now]
                        if len(self.drops) >= self.DROP_LIMIT and not self.unhooked_for_drops:
                            # Let go of TazUO's connection: if it still keeps dropping, it isn't us.
                            safe(self.bridge.unhook)
                            self.unhooked_for_drops = True
                            events.append(("status", "TazUO's Enhanced Map keeps dropping, so Map "
                                           "Pings stopped listening on it (your pings still go "
                                           "out; others' don't show). If it still drops, the "
                                           "cause is elsewhere. Click Reconnect to listen again.", True))
                        else:
                            events.append(("status", "TazUO's Enhanced Map connection dropped; "
                                                     "TazUO will reconnect.", True))
                    else:
                        events.append(("status", "Waiting for TazUO's Enhanced Map to connect", False))
                    self.was_connected = connected
                for pid, payload in self.bridge.frames():
                    if pid == 0x33:
                        self.server_relays_ping = True
                    try:
                        events.append(parse_ping(pid, Reader(payload, 0)))
                    except ValueError:
                        pass
                return events

            def send(self, data):
                """Send raw bytes on TazUO's connection; errors ignored."""
                safe(lambda: self.bridge.send(data))

            def reset(self):
                """Reconnect: forget the drops, listen again if we had let go, and ask TazUO to reconnect."""
                self.drops = []
                if self.unhooked_for_drops:
                    self.unhooked_for_drops = False
                    safe(self.bridge.hook)
                safe(self.bridge.reconnect)

            def close(self):
                """Take our handler off TazUO's connection."""
                safe(self.bridge.unhook)

        def short_error(e):
            """Error text shortened to fit a status line."""
            s = str(e) or e.__class__.__name__
            return s if len(s) < 60 else s[:59]

        _xy = {}

        def xy_fields(t):
            """The public X and Y fields of a client game object type, looked up once per type (the ground, a
            static, an item, a mobile).
            """
            got = _xy.get(t)
            # Looked up by the type itself, with no name read.
            if got is None:
                got = _xy[t] = (t.GetField("X"), t.GetField("Y"))
            return got

        def spot_of(obj):
            """World (x, y) of what a target cursor got (land, static, item or mobile: the client's own game
            object), or None when cancelled.
            """
            if obj is None:
                return None
            # The direct attribute read is tried first, then reflection, then properties: the client's
            # object types differ in what Python can see.
            with Kit.quiet:
                return int(obj.X), int(obj.Y)
            with Kit.quiet:
                t = obj.GetType()
                fx, fy = xy_fields(t)
                if fx is not None and fy is not None:
                    return int(fx.GetValue(obj)), int(fy.GetValue(obj))
                px, py = t.GetProperty("X"), t.GetProperty("Y")
                if px is not None and py is not None:
                    return int(px.GetValue(obj, None)), int(py.GetValue(obj, None))
            return None

        class Ping(object):
            """One ping on screen: where, which type, when made, and its history entry."""
            def __init__(self, x, y, m, t, now, auto=False):
                """Remember the spot, facet, type and creation time; auto marks a ping made by the script itself."""
                self.x, self.y, self.map, self.type, self.auto = x, y, m, t, auto
                self.created = self.next_pulse = now
                # entry: the ping's line in the history window.
                self.marked, self.entry = False, None

        class HistEntry(object):
            """One line of the ping history: a ping shown, yours or not."""
            def __init__(self, seq, at, t, who, x, y, m, local):
                """Remember the line's sequence number, time, type, sender, spot, facet and whether it is yours."""
                self.seq, self.at, self.type, self.who = seq, at, t, who
                self.x, self.y, self.map, self.local = x, y, m, local

        class PingDisplay(object):
            """Shows pings in the world: a tile mark, a pulsing effect, a head message, a World Map marker
            and a sound. Also keeps the history list and the tracking arrow. Client thread.
            """
            # Seconds between pulses of a ping's effect.
            PULSE = 1.4

            def __init__(self):
                """Start with nothing on screen, no markers and an empty history."""
                # pings: on screen. markers: World Map markers to take off again. history: HistEntry, oldest
                # first. marked: (x, y, facet) -> count, so overlapping pings don't unmark a tile early.
                self.pings, self.markers, self.history, self.marked = [], [], [], {}
                # map_at: next look whether TazUO's World Map is open. last_sound: time of the last ping sound.
                self.map_at, self.last_sound = 0.0, -1.0
                # map_since: when the map was seen open (None while closed). arrow_for: the Ping or HistEntry
                # the tracking arrow is on.
                self.map_since = self.arrow_for = None
                # hist_ver changes whenever the history changes, so the window redraws only then; hist_seq
                # numbers the history lines.
                self.hist_ver = self.hist_seq = 0

            def player(self):
                """Your position as (x, y, facet, serial), or (0, 0, -1, 0) when it can't be read."""
                p = API.Player
                try:
                    return int(p.X), int(p.Y), int(API.GetMap()), int(p.Serial)
                except Exception:
                    return 0, 0, -1, 0

            def show(self, sender, x, y, m, t, local=False, who=None, auto=False):
                """Show one ping: journal line, tile mark, effect, head message, World Map marker and sound.

                sender is the name on the ping; local marks one of your own and who then names it (default
                "You"; a ping another module sent for you says so). auto marks a ping another module sent for
                you: it never takes the tracking arrow (a guildmate's ping keeps it), and when too many pings
                are up the oldest such ping goes first, so a burst of trap pings never pushes a guildmate's
                ping off the screen. The arrow is set only for a ping more than 2 tiles away on your facet.
                """
                now = time.time()
                p = Ping(x, y, m, t, now, auto)
                self.pings.append(p)
                # Pings on screen at most 12.
                if len(self.pings) > 12:
                    # Make room: an auto ping goes first, else the oldest. Never the new one itself.
                    self._expire(next((q for q in self.pings[:-1] if q.auto), self.pings[0]))
                label, hue, _, mapcolor = TYPE_INFO[t]
                px, py, pm, serial = self.player()
                where = Kit.where_text(x - px, y - py, "on you") if pm == m and px > 0 else "on %s" % facet_name(m)
                who = (who or "You") if local else sender
                # The journal line keeps the ping's own hue (red for Danger!, like its tile).
                say("%s pinged %s %s (%d, %d, %s)." % ("you" if who == "You" else who, label, where, x, y,
                                                       facet_name(m)), hue)
                # The history window's list.
                self.hist_seq += 1
                p.entry = HistEntry(self.hist_seq, now, t, str(who), x, y, m, bool(local))
                self.history.append(p.entry)
                if len(self.history) > HISTORY_MAX:
                    del self.history[:len(self.history) - HISTORY_MAX]
                self.hist_ver += 1
                if not local and serial:
                    # Others' pings also show above the sender's head when they are in view.
                    API.HeadMsg("%s: %s %s" % (sender, label, where), serial, hue)
                # Tile marks, effects and the arrow only make sense on the facet you are on.
                if pm == m:
                    key = (x, y, m)
                    self.marked[key] = self.marked.get(key, 0) + 1
                    p.marked = True
                    API.MarkTile(x, y, hue, m)
                    if (not auto and px > 0 and x > 0 and y > 0 and max(abs(x - px), abs(y - py)) > 2):
                        API.TrackingArrow(x, y, ARROW_ID)
                        self.arrow_for = p
                # The marker name is CSV-safe: TazUO keeps its markers in a comma separated file.
                name = ("%s: %s %s" % (who, label, time.strftime("%H:%M:%S"))).replace(",", " ")
                # Kept (to take off again) only when TazUO's World Map is open: with it closed TazUO does
                # nothing with the marker call.
                if ATLAS.map_open(True):
                    API.AddMapMarker(name, x, y, m, mapcolor)
                    # Markers stay 60 s.
                    self.markers.append((now + 60, name))
                    if len(self.markers) > MARKERS_CAP:
                        # The oldest markers beyond the cap are left to the Atlas to take out of the file later.
                        ATLAS.loose.update([n for _, n in self.markers[:-MARKERS_CAP]])
                        del self.markers[:-MARKERS_CAP]
                self._play_sound(t, now)

            def _play_sound(self, t, now):
                """Play the ping's sound, but never more often than every 0.3 s so a burst of pings stays
                bearable.
                """
                if not settings["sounds"] or now - self.last_sound < 0.3:
                    return
                self.last_sound = now
                API.PlaySound(PING_SOUNDS[t])

            def update(self):
                """Per tick (client thread): expire old pings, pulse the effects and take expired markers off."""
                if not self.pings and not self.markers:
                    # Nothing on screen: nothing to read.
                    return
                now = time.time()
                # Your facet, read only when a ping pulses.
                pm = None
                stay = settings["ping_secs"]
                for p in list(self.pings):
                    if now - p.created >= stay:
                        self._expire(p)
                        continue
                    if now < p.next_pulse:
                        continue
                    if pm is None:
                        pm = self.player()[2]
                    if p.map == pm:
                        p.next_pulse = now + self.PULSE
                        _, hue, gfx, _ = TYPE_INFO[p.type]
                        API.CreateEffect(gfx, type=API.EffectType.FixedXYZ, hue=hue, sourceX=p.x, sourceY=p.y,
                                         duration=self.PULSE)
                # An expired marker comes off only while the map has been open long enough and is open now
                # (fresh look): a removal does nothing with the map closed, and the marker would stay in
                # TazUO's file. With the map closed it waits for the map to open.
                if self.markers and now >= self.markers[0][0] and self._map_ready(now) and ATLAS.map_open(True):
                    while self.markers and now >= self.markers[0][0]:
                        API.RemoveMapMarker(self.markers.pop(0)[1])

            def _map_ready(self, now):
                """Has TazUO's World Map been open for ATLAS_SETTLE seconds? (It reads its marker files as it
                opens.) Looks at most once a second.
                """
                # Or the clock went back.
                if now >= self.map_at or self.map_at - now > 2.0:
                    self.map_at = now + 1.0
                    if ATLAS.map_open():
                        if self.map_since is None or self.map_since > now:
                            self.map_since = now
                    else:
                        self.map_since = None
                return self.map_since is not None and now - self.map_since >= ATLAS_SETTLE

            def _expire(self, p):
                """Take a ping off the screen: its tile mark (only when no other ping shares the spot) and the
                tracking arrow if it is on this ping.
                """
                if p in self.pings:
                    self.pings.remove(p)
                if p.marked:
                    key = (p.x, p.y, p.map)
                    left = self.marked.get(key, 1) - 1
                    if left <= 0:
                        self.marked.pop(key, None)
                        API.RemoveMarkedTile(p.x, p.y, p.map)
                    else:
                        self.marked[key] = left
                    p.marked = False
                if self.arrow_for is p:
                    self.arrow_off()

            def arrow_entry(self):
                """The history line the tracking arrow points at (a live ping's own line, or one put back from the
                history window), or None.
                """
                a = self.arrow_for
                if a is None or isinstance(a, HistEntry):
                    return a
                return a.entry

            def arrow_to(self, e):
                """Put the tracking arrow on history line e again."""
                API.TrackingArrow(e.x, e.y, ARROW_ID)
                self.arrow_for = e

            def arrow_off(self):
                """Take the tracking arrow down if it is up."""
                if self.arrow_for is not None:
                    API.TrackingArrow(-1, -1, ARROW_ID)
                    self.arrow_for = None

            def clear(self):
                """Stop showing everything: pings, markers and the arrow."""
                # Each step is guarded elsewhere: while TazUO is stopping the script, API calls may be cancelled.
                for p in list(self.pings):
                    self._expire(p)
                if self.markers:
                    names = [n for _, n in self.markers]
                    if ATLAS.map_open(True):
                        for name in names:
                            API.RemoveMapMarker(name)
                    # Map closed: the names come out of TazUO's file instead, through the Atlas.
                    else:
                        ATLAS.loose.update(names)
                self.markers = []
                API.TrackingArrow(-1, -1, ARROW_ID)

        class Settings(object):
            """The separate Enhanced Map login (host, port, user, password), kept as Server-wide persistent
            vars.
            """
            def __init__(self):
                """Read the saved login; a bad port falls back to the default."""
                scope = API.PersistentVar.Server
                self.host = API.GetPersistentVar(VAR_PREFIX + "host", "", scope).strip()
                try:
                    self.port = int(API.GetPersistentVar(VAR_PREFIX + "port", str(DEFAULT_PORT), scope))
                except ValueError:
                    self.port = DEFAULT_PORT
                self.user = API.GetPersistentVar(VAR_PREFIX + "user", "", scope).strip()
                self.password = API.GetPersistentVar(VAR_PREFIX + "pass", "", scope)

            @property
            def complete(self):
                """All four fields are filled and the port is valid."""
                return bool(self.host and self.user and self.password and 0 < self.port < 65536)

            def save(self):
                """Save the login. The password is kept in plain text in the client's saved variables on this PC."""
                scope = API.PersistentVar.Server
                for k, v in (("host", self.host), ("port", str(self.port)), ("user", self.user),
                             ("pass", self.password)):
                    API.SavePersistentVar(VAR_PREFIX + k, v, scope)

        HIST_TITLE = "Ping History"
        # Key of the History window in the host's fold-into-the-bar registry.
        HIST_DOCK = "pings_history"
        HIST_POS_KEY = VAR_PREFIX + "history_pos"
        HIST_MIN_KEY = VAR_PREFIX + "history_min"
        HIST_OPEN_KEY = VAR_PREFIX + "history_open"
        # Size of the History window's one-line minimised bar.
        HIST_MINI_W, HIST_MINI_H = 320, 46
        HIST_ROW_H = 24
        # Column heads and widths; Where takes the rest.
        HIST_COLS = (("When", 70), ("Ping", 80), ("From", 140))
        HIST_TIP = "Put the tracking arrow on this spot (click again to take it down)"
        HIST_ALT = ". Alt+click: auto-follow (again to stop)"
        HIST_EMPTY = "No pings yet. Send one with a ping button, a hotkey or the wheel drag."

        class HistoryWindow(object):
            """The recent pings, newest first, a page of HISTORY_ROWS pooled rows.

            Drawn on the client tick (PingApp.step). Nothing is drawn while it is folded into the bar, only
            the status line while minimised, and the rows only when the history, the page or the arrow
            changed (and once a second for the distances, which change as you walk).
            """
            def __init__(self, app):
                """Create the window object (not shown yet)."""
                self.app = app
                self.page, self.next_draw = 0, 0.0
                # drawn: what the rows were drawn from. drawn_pos: where you stood at the time.
                self.drawn = self.drawn_pos = None
                # st doubles as the dock hooks' window state (its "g" is the gump).
                self.st = {"g": None, "shutting": False, "minimized": False, "docked": False, "queue": [], "c": {},
                           "store": ({}, {}), "rows": []}
                self.wnd = Kit.Window(HIST_DOCK, HIST_TITLE, self.st, self.st, self.build, HIST_POS_KEY,
                                      default=(260, 160), mini=(HIST_MINI_W, HIST_MINI_H), icon=0x14EB, lock=True,
                                      owner=False, close_tip="Close Ping History", clear={"c": {}, "rows": []})
                self.queue = self.wnd.queue

            def start(self):
                """Start with the part: restore minimised state and open the window if it was open last time."""
                hs = self.st
                hs["shutting"] = False
                hs["minimized"] = Kit.load_min(HIST_MIN_KEY) or HOST.dock_wanted(HIST_DOCK)
                self.wnd.dock(fit=True, min=(560, list_h(1, HIST_ROW_H)), show=self.zone_show)
                # Open when Map Pings last stopped.
                if Kit.get_var(HIST_OPEN_KEY, "0") == "1":
                    self.build()

            def zone_show(self):
                """The layout asks the window to show: open it unfolded."""
                self.st["minimized"] = self.st["docked"] = False
                self.queue.add("open")

            def toggle_open(self):
                """The History button: open the window, show it when it is only minimised or folded into the bar,
                close it when it is shown.
                """
                hs = self.st
                if hs["g"] is not None and not (hs["minimized"] or hs["docked"]):
                    if not HOST.layout_holds(HIST_DOCK):
                        self.close()
                    return
                hs["minimized"] = hs["docked"] = False
                HOST.dock_forget(HIST_DOCK)
                Kit.save_min(HIST_MIN_KEY, False)
                Kit.put_var(HIST_OPEN_KEY, "1")
                self.build()

            def close(self):
                """Close the window and remember it as closed."""
                hs = self.st
                if hs["g"] is None:
                    return
                self.wnd.close()
                hs["docked"] = False
                HOST.dock_forget(HIST_DOCK)
                Kit.put_var(HIST_OPEN_KEY, "0")

            def shutdown(self):
                """Part stopping: close the window without forgetting whether it was open."""
                hs = self.st
                hs["shutting"] = True
                HOST.dock_remove(HIST_DOCK)
                if hs["g"] is not None:
                    # Folded into the bar is the host's wish (dock_wanted), not "minimised".
                    Kit.save_min(HIST_MIN_KEY, hs["minimized"] and not hs["docked"])
                    self.wnd.close()

            def build(self):
                """Build the window: toolbar (Clear, Arrow off, pager) and the pooled list rows.

                When the layout gave the window a slot, its size and row count follow the slot.
                """
                hs = self.st
                z = told(self.wnd, hs, 560, list_h(1, HIST_ROW_H))
                w, h = z if z else (560, list_h(HISTORY_ROWS, HIST_ROW_H))
                n = self.wnd.rows(HIST_ROW_H, list_h(0, HIST_ROW_H), HISTORY_ROWS) if z else HISTORY_ROWS
                # Rows are made once and re-used on redraw; only their text changes.
                g, store, c = self.wnd.begin(w, h)
                rows = []
                if not hs["minimized"]:
                    self.wnd.frame(g)
                    M = Kit.MARGIN
                    IW = w - 2 * M
                    # Toolbar: Clear, Arrow off and the pager.
                    yt = M + 30 + Kit.GAP
                    Kit.add_section(g, M, yt, IW, 36)
                    bx = M + 12
                    Kit.art_button(g, store, "clear", Kit.ART_CLOSE, bx, yt + 7, "Clear",
                                   "Empty the history (pings on screen stay)", on_click=self.queue("clear"))
                    bx += 35 + Kit.text_w("Clear") + 16
                    Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, bx, yt + 7, "Arrow off",
                                   "Take the tracking arrow down", on_click=self.queue("arrow_off"))
                    right = M + IW - 8
                    c["pg"] = Kit.add_label(g, "", right - 100, yt + 10, Kit.HUE_INFO)
                    Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 56, yt + 8, None,
                                   "Previous page (newer pings)", on_click=self.queue(("page", -1)))
                    Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 34, yt + 8, None,
                                   "Next page (older pings)", on_click=self.queue(("page", 1)))
                    # The list: column heads, then the pooled rows.
                    yl = yt + 36 + Kit.GAP
                    Kit.add_section(g, M, yl, IW, h - yl - M)
                    cx = M + 12
                    xs = []
                    for head, cw in HIST_COLS:
                        Kit.add_label(g, head, cx, yl + 6, Kit.HUE_TITLE)
                        xs.append((cx, cw))
                        cx += cw + 8
                    Kit.add_label(g, "Where", cx, yl + 6, Kit.HUE_TITLE)
                    c["where_w"] = M + IW - 12 - cx
                    for k in range(n):
                        ry = yl + 30 + k * HIST_ROW_H
                        r = {"val": None, "prev": None, "changed": 0.0, "tip": None, "vis": True, "sig": None,
                             "labels": [Kit.add_label(g, "", xx, ry + 3, Kit.HUE_TEXT) for xx, _ in xs],
                             "where": Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO), "widths": [cw for _, cw in xs]}
                        # A transparent click catcher over each row.
                        r["catch"] = Kit.catcher(g, M + 6, ry, IW - 12, HIST_ROW_H,
                                                 Kit.row_clicker(r, self.queue, "arrow"), HIST_TIP)
                        rows.append(r)
                self.wnd.end(g, {"rows": rows})
                self.drawn = None
                self.refresh()

            def tick(self):
                """Per tick (client thread): run queued clicks, then redraw if needed."""
                hs = self.st
                # The close button.
                if hs["g"] is not None and Kit.was_clicked(hs["store"], "close"):
                    self.close()
                    return
                q = hs["queue"]
                while q:
                    a = q.pop(0)
                    kind = a[0] if isinstance(a, tuple) else a
                    if kind == "toggle_min":
                        hs["minimized"] = not hs["minimized"]
                        hs["docked"] = False
                        HOST.dock_forget(HIST_DOCK)
                        Kit.save_min(HIST_MIN_KEY, hs["minimized"])
                    elif kind == "to_bar":
                        HOST.dock_to_bar(HIST_DOCK, HIST_TITLE)
                    elif kind == "settings":
                        HOST.show_settings("pings")
                    elif kind == "page":
                        self.page = max(0, self.page + a[1])
                        self.next_draw = 0.0
                    elif kind == "clear":
                        disp = self.app.display
                        del disp.history[:]
                        disp.hist_ver += 1
                        self.page = 0
                    elif kind == "arrow_off":
                        self.app.display.arrow_off()
                    elif kind == "arrow":
                        self.arrow(a[1])
                    elif kind == "follow":
                        self.follow(a[1])
                    if kind == "open" or kind in ("toggle_min", "redraw") and hs["g"] is not None:
                        self.build()
                # Closed, or folded into the bar: nothing to draw.
                if hs["g"] is None or (hs["minimized"] and hs["docked"]):
                    return
                self.refresh()

            def entry(self, seq):
                """The history line with this sequence number, or None when it has dropped off."""
                return next((e for e in self.app.display.history if e.seq == seq), None)

            def arrow(self, seq):
                """A row was clicked: the tracking arrow on that ping's spot, or off when it is already there."""
                disp = self.app.display
                e = self.entry(seq)
                if e is None:
                    return
                if disp.arrow_entry() is e:
                    disp.arrow_off()
                    return
                pm = disp.player()[2]
                # The arrow only works on your own facet.
                if pm != e.map:
                    say("that ping is on %s; you are on %s." % (facet_name(e.map), facet_name(pm)))
                    return
                disp.arrow_to(e)
                say("tracking arrow on %s's %s (%d, %d)." % (e.who, label_of(e.type), e.x, e.y))

            def follow(self, seq):
                """Alt+click on a row: auto-follow whoever sent that ping, when a player of that name is in range
                (Follow toggles it off again).
                """
                e = self.entry(seq)
                if e is None:
                    return
                if e.local:
                    say("that ping is your own.")
                    return
                serial = self.mobile_named(e.who)
                if not serial:
                    say("%s isn't in range." % e.who)
                    return
                Follow.toggle(serial, TITLE)

            def mobile_named(self, name):
                """Serial of the nearest mobile in view called name (any case), or 0."""
                low = str(name or "").strip().lower()
                if not low:
                    return 0
                best, bd = 0, None
                for m in API.GetAllMobiles() or ():
                    if str(m.Name or "").strip().lower() != low:
                        continue
                    d = int(m.Distance)
                    if bd is None or d < bd:
                        best, bd = int(m.Serial), d
                return best

            def where_text(self, e, px, py, pm):
                """The Where column text: facet and spot, or direction and distance when on your facet.

                The spot is the coordinates through xy, so it is hidden in streamer mode.
                """
                spot = xy(e.x, e.y, "(%d, %d)")
                if pm != e.map or px <= 0:
                    return "%s %s" % (facet_name(e.map), spot)
                return "%s  %s" % (Kit.where_text(e.x - px, e.y - py, "here"), spot)

            def refresh(self):
                """Redraw the list as little as possible.

                Minimised: only the status line, when the history changed. Otherwise rows are rewritten only
                when the history, page or arrow changed, or you moved (checked once a second): the texts would
                come out the same otherwise. Row controls are pooled and only their text and visibility change.
                Senders are shown through sender, so streamer mode veils other players' names.
                """
                hs = self.st
                disp = self.app.display
                hist = disp.history
                c = hs["c"]
                if hs["minimized"]:
                    if self.drawn == disp.hist_ver:
                        return
                    self.drawn = disp.hist_ver
                    if hist:
                        e = hist[-1]
                        txt = "%s: %s, last %s %s" % (HIST_TITLE, Kit.count(len(hist), "ping"), label_of(e.type),
                                                       self.sender(e))
                    else:
                        txt = "%s: no pings yet" % HIST_TITLE
                    if c.get("status") is not None:
                        Kit.set_text(c["status"], Kit.fit(txt, HIST_MINI_W - 90))
                    return
                now = time.time()
                arrow = disp.arrow_entry()
                sig = (disp.hist_ver, self.page, arrow)
                if sig == self.drawn and now < self.next_draw:
                    return
                # Position read once a second for the distances; nothing is redrawn when you haven't moved.
                pos = disp.player()[:3] if hist else (0, 0, -1)
                if sig == self.drawn and pos == self.drawn_pos:
                    self.next_draw = now + 1.0
                    return
                self.drawn, self.next_draw, self.drawn_pos = sig, now + 1.0, pos
                n = len(hist)
                per = max(1, len(hs["rows"]))
                pages = max(1, (n + per - 1) // per)
                self.page = max(0, min(pages - 1, self.page))
                if c.get("pg") is not None:
                    Kit.set_text(c["pg"], ("%d/%d" % (self.page + 1, pages)) if pages > 1 else "")
                px, py, pm = pos
                # Newest first.
                first = n - 1 - self.page * per
                where_w = c.get("where_w", 200)
                for k, r in enumerate(hs["rows"]):
                    i = first - k
                    if i < 0:
                        Kit.row_set(r, None, now)
                        r["sig"] = None
                        # An empty list says so in the first row.
                        if k == 0 and n == 0:
                            Kit.set_text(r["labels"][0], HIST_EMPTY, Kit.HUE_INFO)
                            self._show(r, True, only_first=True)
                        else:
                            self._show(r, False)
                        continue
                    e = hist[i]
                    # Row identity is the sequence number, so a click always hits the same ping.
                    Kit.row_set(r, (e.seq,), now)
                    hue = TYPE_INFO[e.type][1]
                    on = arrow is e
                    where = self.where_text(e, px, py, pm)
                    rsig = (e.seq, where, on)
                    if rsig != r["sig"]:
                        r["sig"] = rsig
                        texts = (time.strftime("%H:%M:%S", time.localtime(e.at)), label_of(e.type), self.sender(e))
                        hues = (Kit.HUE_INFO, hue, Kit.HUE_TEXT if not e.local else Kit.HUE_INFO)
                        for j, lbl in enumerate(r["labels"]):
                            Kit.set_text(lbl, Kit.fit(texts[j], r["widths"][j]), hues[j])
                        Kit.set_text(r["where"], Kit.fit(("> " if on else "") + where, where_w),
                                     Kit.HUE_TITLE if on else Kit.HUE_INFO)
                        tip = ("Take the tracking arrow down" if on else HIST_TIP) + ("" if e.local else HIST_ALT)
                        if tip != r["tip"]:
                            r["tip"] = tip
                            Kit.with_tip(r["catch"], tip)
                    self._show(r, True)

            def sender(self, e):
                """The sender name of a ping entry as it should be shown.

                Your own pings read "You" and are never veiled. In streamer mode another player's name becomes
                a veiled label derived from a checksum of the lower-cased name, so one sender always looks the
                same.
                """
                if e.who == "You" or not Kit.streamer:
                    return e.who
                return Kit.veil("name", e.who, Kit.checksum(e.who.lower().encode("utf-8")))

            def _show(self, r, on, only_first=False):
                """Show or hide a pooled row's controls; only_first leaves just the first label (the empty note)."""
                want = ("first" if only_first else on)
                if r["vis"] == want:
                    return
                r["vis"] = want
                parts = r["labels"] + [r["where"], r["catch"]]
                for j, ctl in enumerate(parts):
                    Kit.set(ctl, "IsVisible", on and (not only_first or j == 0))

        class PingApp(object):
            """Map Pings itself: the link to the map server, the target cursor, the mouse wheel gesture, the
            hotkeys and the main loop split into step (client thread) and thread_step (script thread).

            The two steps hand work to each other through lists: the client thread never touches the
            network (a connect or a send can block), so clicks and hotkeys queue actions in pending; step
            moves the network ones to jobs; thread_step sends the outbox and posts what the server said to
            the inbox for the next step.
            """
            def __init__(self):
                """Start idle: no link yet, empty queues, the saved login, the display and the History window."""
                # mouse: TazUOMouse for the wheel gesture. gesture: dict while the wheel is held. guide: the
                # on-screen direction guide. bridge: TazUO's connection helper (bridge_error says why not). conn:
                # the live link.
                self.mouse = self.gesture = self.guide = self.bridge = self.bridge_error = self.conn = None
                # aim: the target-a-spot cursor while it is up.
                self.aim = self.status_label = self.last_pos = None
                # recent_pings: (name, x, y, type) -> time first seen, to drop the copies of a ping.
                self.guide_labels, self.recent_pings = {}, {}
                self.bridge_tried = self._shut = False
                self.next_link_check = self.last_pos_sent = self.next_pos_read = 0
                self.last_ping_sent = self.last_auto_sent = 0
                # Oldest first, so pruning the dedupe list is O(1).
                self.recent_order = collections.deque()
                self.settings = Settings()
                self.display = PingDisplay()
                # pending: actions queued by clicks and hotkeys. jobs: network actions for thread_step. outbox:
                # packets for thread_step to send. inbox: what thread_step got back. hooked: hotkey combos
                # registered right now.
                self.pending, self.jobs, self.outbox, self.inbox, self.hooked = [], [], [], [], []
                # status_w: pixels the status label may take (set when the settings page is built).
                self.status_text, self.status_w = "", 300
                # The History window.
                self.history = HistoryWindow(self)

            def set_status(self, text, also_journal=True):
                """Show a status line on the settings page and, unless also_journal is False, in the journal."""
                self.status_text = text
                if self.status_label is not None:
                    Kit.set_text(self.status_label, Kit.fit(text, self.status_w))
                if also_journal:
                    say(journal_case(text))

            def _queue_ping(self, t):
                """Make the hotkey callback for ping type t.

                The callback queues a target request for the main loop and wakes the host. A key typed into a
                text field (a chat line, any text box) is not a ping.
                """
                def fn(*args):
                    """Hotkey callback: queue the target request unless the player is typing."""
                    if HOST.typing():
                        return
                    self.pending.append(("target", t))
                    HOST.poke()

                return fn

            def save_setup(self):
                """The login on the settings page was saved: connect with it (script thread).

                TazUO's own connection, when in use, stays in use.
                """
                if self.conn and self.conn.kind == "tazuo":
                    self.set_status("Saved; TazUO's Enhanced Map login is on, so that stays in use.")
                    return
                if self.conn:
                    self.conn.close()
                    self.conn = None
                self.choose_link()

            def apply_options(self):
                """Options changed on the settings page: start or stop the mouse gesture and choose the link again."""
                if settings["gesture"] and self.mouse is None:
                    self.init_mouse()
                elif not settings["gesture"]:
                    self.mouse = self.gesture = None
                    self.close_guide()
                # choose_link runs on the script thread, which is where network work belongs.
                self.jobs.append(("link",))

            def connect(self):
                """Start a separate login of our own."""
                if self.conn:
                    self.conn.close()
                s = self.settings
                self.conn = MapConnection(s.host, s.port, s.user, s.password)
                self.set_status("Connecting to %s:%d" % (s.host, s.port), also_journal=False)

            def get_bridge(self):
                """The TazUO bridge, made once. None when TazUO's internals are not as expected (bridge_error has
                the reason).
                """
                if not self.bridge_tried:
                    self.bridge_tried = True
                    try:
                        self.bridge = TazUOBridge()
                    except Exception as e:
                        self.bridge = None
                        self.bridge_error = short_error(e)
                return self.bridge

            def tazuo_available(self):
                """Is TazUO's Enhanced Map set up (configured)?"""
                b = self.get_bridge()
                return b is not None and bool((b.config() or {}).get("configured"))

            def choose_link(self, announce=True):
                """Pick TazUO's connection or our own login, per the Connection option. Safe to call repeatedly.

                auto: TazUO's when it is configured, else our own login. tazuo: only TazUO's. own: only our
                login. announce says whether to put the reason in the status when nothing can be used.
                """
                mode = (settings["connection"] or "auto").lower()
                current = self.conn.kind if self.conn else None
                if mode in ("auto", "tazuo") and self.tazuo_available():
                    if current != "tazuo":
                        # Never hold a second login on the same account.
                        if self.conn:
                            self.conn.close()
                        self.conn = TazUOLink(self.bridge)
                    # Keep waiting on it.
                    return
                if mode == "tazuo":
                    if current == "tazuo":
                        return
                    if current == "own":
                        self.conn.close()
                        self.conn = None
                        # The status says why it went quiet.
                        announce = True
                    if announce:
                        if self.get_bridge() is None:
                            self.set_status("Can't use TazUO's Enhanced Map connection (%s)." % self.bridge_error)
                        else:
                            self.set_status("Turn on Enhanced Map in TazUO's Options (server, port, login).")
                    return
                # TazUO's Enhanced Map was switched off: let go of it.
                if current == "tazuo":
                    self.conn.close()
                    self.conn = None
                    current = None
                # Our own login is already the link.
                if current == "own":
                    return
                if self.settings.complete:
                    self.connect()
                elif announce:
                    if mode == "auto" and self.get_bridge() is not None:
                        self.set_status("Turn on Enhanced Map in TazUO, or enter a map login (World Map settings).")
                    else:
                        self.set_status("Enter your map server details to start.")
                        self.inbox.append(("open_setup",))

            def send_ping(self, x, y, m, t):
                """Send one of your own pings, at most one every PING_RATE_SECS. Client thread."""
                now = time.time()
                if now - self.last_ping_sent < PING_RATE_SECS:
                    return
                self.last_ping_sent = now
                self._send(x, y, m, t)

            def send_auto(self, x, y, m, t, who=None):
                """A ping another module asks for (HOST service "pings.send", for example Traps & Fields' Danger!
                on a trap).

                Paced like your own, but on its own clock, so it never swallows a ping you send yourself.
                Returns False when too soon: ask again later.
                """
                now = time.time()
                if now - self.last_auto_sent < PING_RATE_SECS:
                    return False
                self.last_auto_sent = now
                self._send(x, y, m, t, who=who, auto=True)
                return True

            def _send(self, x, y, m, t, who=None, auto=False):
                """Show a ping of yours and queue it for the map server.

                auto marks a ping another module asked for: no tracking arrow, first off a full screen, and the
                "not connected" note goes to the journal only when it is new (a run of trap pings doesn't
                repeat it once per ping).
                """
                self.display.show("You", x, y, m, t, local=True, who=who, auto=auto)
                if self.conn and self.conn.ready:
                    # The ping packet (0x33) isn't part of the standard Enhanced Map protocol; a server without the
                    # ping update may drop whoever sends it. On TazUO's connection it is only sent once the server
                    # has shown it relays them; until then the typed alert below carries the type and facet.
                    if self.conn.server_relays_ping:
                        self.outbox.append(packet(0x33, struct.pack("<HHBB", x & 0xFFFF, y & 0xFFFF, m & 0xFF,
                                                                    t & 0xFF)))
                    # Old servers: scripts decode the type and facet from this alert.
                    typed = pk_typed_alert(x, y, m, t)
                    if typed:
                        self.outbox.append(typed)
                    # Sent last, so TazUO's overlay and Enhanced Map show the real spot. The packets go out in this
                    # order from thread_step.
                    self.outbox.append(pk_alert(x, y))
                else:
                    note = "Not connected: only you can see that ping."
                    self.set_status(note, also_journal=not auto or self.status_text != note)

            # Seconds the target cursor may stay up.
            AIM_SECONDS = 10

            def target_ping(self, t):
                """Put up the client's own target cursor to pick a spot for a ping (client thread).

                The cursor is watched every tick instead of blocking the script, which would hold every module
                until the player clicked. Like HOST.pick_target, but it hands back the spot (ground, static,
                item or mobile), not a serial. Without client access the old blocking cursor is queued for the
                script thread.
                """
                say("target a spot for %s (yourself: where you stand)." % label_of(t))
                # A newer cursor replaces ours.
                self.aim = None
                tm = Picker._tm()
                if tm is not None:
                    aim = {"t": t, "fired": False, "spot": None, "d": None, "tm": tm,
                           "until": time.time() + self.AIM_SECONDS}

                    # The client calls this when you target.
                    def got(obj, aim=aim):
                        """The client's callback when the player targets something: remember the spot."""
                        aim["spot"] = spot_of(obj)
                        aim["fired"] = True

                    with Kit.quiet:
                        from System import Action
                        aim["d"] = Action[object](got)
                        tm.SetTargeting(aim["d"], Picker.CURSOR_TARGET, Picker.neutral)
                        self.aim = aim
                        # Spoken for: Bandages and Ultima Tracker don't aim this cursor at anyone.
                        HOST.claim_cursor("pings", self.AIM_SECONDS)
                        return
                # No client access: the blocking cursor on the script thread.
                self.jobs.append(("aim", t))

            def poll_aim(self):
                """Each tick: look at the cursor and act on its outcome, once there is one."""
                aim = self.aim
                if aim is None:
                    return
                if not aim["fired"]:
                    ours = bool(aim["tm"].IsCurrentTargetingAction(aim["d"]))
                    if ours and time.time() < aim["until"]:
                        return
                    # Cancelled, replaced by another cursor, or timed out.
                    self.aim = None
                    HOST.release_cursor("pings")
                    if ours:
                        # Ours and timed out: take it down.
                        aim["tm"].CancelTarget()
                    return
                self.aim = None
                HOST.release_cursor("pings")
                self.aimed(aim["t"], aim["spot"])

            def aimed(self, t, spot):
                """A spot was targeted: send the ping there on your facet."""
                if spot is None:
                    return
                x, y = spot
                if x <= 0 or y <= 0:
                    return
                self.send_ping(x, y, int(API.GetMap()), t)

            def drop_aim(self):
                """Take our cursor down when stopping, only if it is still ours."""
                aim, self.aim = self.aim, None
                HOST.release_cursor("pings")
                if aim is None or aim["fired"]:
                    return
                tm = aim["tm"]

                def cancel():
                    """Cancel the cursor if it is still ours (runs on the client thread)."""
                    if tm.IsCurrentTargetingAction(aim["d"]):
                        tm.CancelTarget()

                safe(lambda: Kit.on_client(cancel, fallback=False))

            def target_ping_blocking(self, t):
                """Blocking cursor for builds without client access (script thread): wait for a target for up to
                10 s and hand the spot to the main loop.
                """
                target = API.RequestAnyTarget(10)
                if target is None:
                    return
                try:
                    x, y = int(target.X), int(target.Y)
                except Exception:
                    return
                self.inbox.append(("aimed", t, (x, y)))

            def share_position(self):
                """Separate login only: send your position so guildmates see you on their maps.

                The position goes out at most once a second (or every 10 s when unchanged), so it is read
                every 0.5 s rather than every tick. With sharing off, or no position, a keep-alive packet goes
                out after 20 s of silence. Status flag: dead 4, poisoned 1, yellow hits 2, paralysed 3, hidden
                5.
                """
                if not self.conn or not self.conn.ready or not self.conn.owns_position:
                    return
                now = time.time()
                if now < self.next_pos_read:
                    return
                self.next_pos_read = now + 0.5
                pos = None
                if settings["share"]:
                    p = API.Player
                    try:
                        pos = (int(p.X), int(p.Y), int(API.GetMap()))
                    except Exception:
                        pass
                if pos is None or pos[0] <= 0:
                    if now - self.conn.last_sent > 20:
                        self.outbox.append(packet(0xFE))
                    return
                if ((pos != self.last_pos and now - self.last_pos_sent >= 1.0) or now - self.last_pos_sent >= 10):
                    flag = (4 if p.IsDead else 1 if p.IsPoisoned else 2 if p.IsYellowHits else 3 if p.IsParalyzed
                            else 5 if p.IsHidden else 0)
                    stats = (int(p.Hits), int(p.Stamina), int(p.Mana), int(p.HitsMax), int(p.StaminaMax),
                             int(p.ManaMax))
                    self.outbox.append(pk_player_data(pos, stats, flag, 0xFFFFD700))
                    self.last_pos, self.last_pos_sent = pos, now

            def handle(self, ev):
                """Act on one event from the link: status, ping, alert (typed or plain) or server message."""
                kind = ev[0]
                if kind == "status":
                    self.set_status(ev[1], also_journal=ev[2])
                elif kind == "ping":
                    self.show_once(*ev[1:])
                elif kind == "alert":
                    _, name, x, y = ev
                    decoded = decode_typed_alert(x, y)
                    if decoded:
                        self.show_once(name, *decoded)
                    elif not self.seen_recently(name, x, y):
                        # A plain alert from someone without the script; the plain copy of a ping is dropped above.
                        self.show_once(name, x, y, int(API.GetMap()), LOOK)
                elif kind == "message":
                    say("map server: " + ev[1])

            DEDUPE_SECONDS = 3

            def seen_recently(self, name, x, y, t=None):
                """Was this ping seen in the last DEDUPE_SECONDS?

                Each ping can arrive up to three times (ping message, typed alert, plain alert); the first is
                shown and the others dropped. t=None (a plain alert, type unknown) matches a recent ping of
                any type.
                """
                now = time.time()
                order, recent = self.recent_order, self.recent_pings
                # Oldest first, so each prune is O(1).
                while order and now - order[0][0] > self.DEDUPE_SECONDS:
                    at, key = order.popleft()
                    if recent.get(key) == at:
                        del recent[key]
                if t is not None:
                    return (name, x, y, t) in recent
                for k in recent:
                    if k[0] == name and k[1] == x and k[2] == y:
                        return True
                return False

            def show_once(self, name, x, y, m, t):
                """Show a ping from the link unless it is a copy of one just shown."""
                if self.seen_recently(name, x, y, t):
                    return
                now = time.time()
                key = (name, x, y, t)
                self.recent_pings[key] = now
                self.recent_order.append((now, key))
                self.display.show(name, x, y, m, t)

            def step(self):
                """One pass of the main loop, on the client thread: queued actions, events from the link, the
                target cursor, position sharing, the wheel gesture, pings on screen and the History window.
                Never waits: no network here (see thread_step).
                """
                while self.pending:
                    action = self.pending.pop(0)
                    if action[0] == "target":
                        self.target_ping(action[1])
                    elif action[0] == "options":
                        self.apply_options()
                    elif action[0] == "rehook":
                        self.register_hotkeys()
                    elif action[0] == "history":
                        self.history.toggle_open()
                    # Anything else (save_setup, reconnect) is network work for the script thread.
                    else:
                        self.jobs.append(action)
                # What thread_step got from the map server and window requests.
                inbox = self.inbox
                # No new list on an idle tick.
                if inbox:
                    self.inbox = []
                for ev in inbox:
                    if ev[0] == "open_setup":
                        HOST.show_settings("pings")
                    elif ev[0] == "aimed":
                        self.aimed(ev[1], ev[2])
                    else:
                        self.handle(ev)
                self.poll_aim()
                if self.conn:
                    self.share_position()
                self.poll_gesture()
                self.display.update()
                self.history.tick()

            def thread_step(self):
                """The network side of a pass, on the script thread right after step: queued jobs, picking the
                link, sending packets and reading the server. Returns at once when idle.
                """
                while self.jobs:
                    action = self.jobs.pop(0)
                    if action[0] == "save_setup":
                        self.save_setup()
                    elif action[0] == "link":
                        self.choose_link(announce=False)
                    elif action[0] == "aim":
                        self.target_ping_blocking(action[1])
                    elif action[0] == "reconnect":
                        if self.conn and self.conn.kind == "tazuo":
                            self.conn.reset()
                            self.set_status("Asked TazUO's Enhanced Map to reconnect.")
                        elif self.settings.complete and (settings["connection"] or "auto").lower() != "tazuo":
                            self.connect()
                            self.conn.reset()
                        else:
                            self.choose_link()
                # In auto mode, follow TazUO's Enhanced Map being switched on and off.
                if time.time() >= self.next_link_check:
                    self.next_link_check = time.time() + 5
                    self.choose_link(announce=False)
                out = self.outbox
                # No new list on an idle pass.
                if out:
                    self.outbox = []
                if self.conn:
                    for data in out:
                        self.conn.send(data)
                    self.inbox.extend(self.conn.poll())

            def init_mouse(self):
                """Make the mouse reader for the wheel gesture, unless the gesture is off or TazUO's mouse
                internals aren't found.
                """
                if not settings["gesture"]:
                    self.mouse = None
                    return
                try:
                    self.mouse = TazUOMouse()
                except Exception as e:
                    self.mouse = None
                    say("mouse-wheel pings unavailable (%s): use the ping buttons or hotkeys." % short_error(e))

            @staticmethod
            def drag_direction(dx, dy):
                """Direction of a drag ("up", "down", "left", "right"), or None when it is shorter than the Drag
                distance option.
                """
                if max(abs(dx), abs(dy)) < settings["drag"]:
                    return None
                if abs(dx) > abs(dy):
                    return "right" if dx > 0 else "left"
                return "down" if dy > 0 else "up"

            def poll_gesture(self):
                """Each tick: watch the mouse wheel. Press over the world starts a gesture and the guide; drag
                picks a direction; release sends the ping for that direction.
                """
                m = self.mouse
                if m is None:
                    return
                down = m.middle_down()
                if down and self.gesture is None:
                    tile = m.tile_under_mouse()
                    start = m.position(m._mclick)
                    self.gesture = {"tile": tile, "start": start, "dir": None, "map": int(API.GetMap())}
                    if tile is not None:
                        self.show_guide(start)
                elif down and self.gesture is not None:
                    # Pressed over a gump or panel (or nothing): ignore this press entirely.
                    if self.gesture["tile"] is None:
                        return
                    x, y = m.position()
                    d = self.drag_direction(x - self.gesture["start"][0], y - self.gesture["start"][1])
                    if d != self.gesture["dir"]:
                        self.gesture["dir"] = d
                        self.update_guide(d)
                elif not down and self.gesture is not None:
                    g, self.gesture = self.gesture, None
                    self.close_guide()
                    t = GESTURE.get(g["dir"])
                    if g["tile"] is not None and t is not None:
                        self.send_ping(g["tile"][0], g["tile"][1], g["map"], t)

            def show_guide(self, center):
                """Show the direction guide round the cursor: four labels and a plus sign."""
                self.close_guide()
                w, h = 180, 104
                gump = G.CreateGump(False, False)
                # The press position is in the client window's real pixels; gumps are placed in UI-scaled
                # pixels (Kit.screen), so with a UI scale other than 1 the guide would open away from the
                # cursor.
                scale = Kit.render_scale() or 1.0
                cx, cy = int(round(center[0] / scale)), int(round(center[1] / scale))
                # Kept on screen.
                Kit.place(gump, cx - w // 2, cy - h // 2, w, h)
                Kit.add_window_frame(gump, w, h, corners=False)
                Kit.add_section(gump, 6, 6, w - 12, h - 12)
                for d, (lx, ly) in (("up", (58, 9)), ("right", (110, 43)), ("down", (58, 77)), ("left", (11, 43))):
                    t = GESTURE[d]
                    lab = G.CreateGumpLabel(label_of(t), Kit.HUE_INFO)
                    lab.SetRect(lx, ly, 70, 18)
                    gump.Add(lab)
                    self.guide_labels[d] = (lab, t)
                plus = G.CreateGumpLabel("+", Kit.HUE_TITLE)
                plus.SetRect(w // 2 - 3, h // 2 - 9, 10, 18)
                gump.Add(plus)
                G.AddGump(gump)
                # A guide under the held wheel is no window to snap to or move: keep it out of the mother's
                # snapping and keeper.
                SNAP.skip_gump(gump)
                self.guide = gump

            def update_guide(self, chosen):
                """Bracket the chosen direction's label and colour it; the others go back to plain."""
                for d, (lab, t) in self.guide_labels.items():
                    lab.Text = "[" + label_of(t) + "]" if d == chosen else label_of(t)
                    lab.Hue = TYPE_INFO[t][1] if d == chosen else 946

            def close_guide(self):
                """Close the direction guide."""
                Kit.dispose(self.guide)
                self.guide, self.guide_labels = None, {}

            def register_hotkeys(self):
                """Register the four ping hotkeys with the host (replacing earlier ones).

                A hotkey the host says is not a key is reported once and not kept.
                """
                self.unregister_hotkeys()
                for key, combo in HOTKEYS.items():
                    if combo:
                        t = TYPE_KEYS[key]
                        what = "%s ping" % label_of(t)
                        got = HOST.hotkey_on(combo, TITLE, self._queue_ping(t), what)
                        if got is False:
                            say("couldn't set the %s hotkey (%s isn't a key)." % (label_of(t), combo),
                                Kit.HUE_BAD)
                        if got is not False:
                            self.hooked.append(combo)

            def unregister_hotkeys(self):
                """Release the hotkeys this part holds."""
                for combo in self.hooked:
                    HOST.hotkey_off(combo, TITLE)
                self.hooked = []

            def shutdown(self):
                """Stop everything this part started: hotkeys, cursor, guide, History window, pings on screen and
                the link. Safe to call twice.
                """
                if self._shut:
                    return
                self._shut = True
                self.unregister_hotkeys()
                self.drop_aim()
                self.close_guide()
                safe(self.history.shutdown)
                safe(self.display.clear)
                if self.conn:
                    self.conn.close()

            def start(self):
                """Start the part: mouse, hotkeys, History window and the link."""
                self.init_mouse()
                self.register_hotkeys()
                self.history.start()
                say("on; ping buttons are on the World Map settings page.", Kit.HUE_GOOD)
                self.choose_link()
                self.next_link_check = time.time() + 5

        def _queue_app(action):
            """Queue an action for Map Pings' main loop, if it is running."""
            if st["app"] is not None:
                st["app"].pending.append(action)

        # State of the settings page while it is open: its form, drop down, status label and fields.
        page = {"f": None}
        # Heights of the three custom sections of the page.
        H_SEND, H_LOGIN, H_KEYS = 116, 160, 70
        PING_TIP = "Send a %s ping on the spot, item or person you target"
        KEY_TIP = "Key for a %s ping, like CTRL+1, F9 or SHIFT+F2 (blank = none)"
        LOGIN_TIPS = {"host": "Map server address (host name or IP)", "port": "Map server port (default %d)"
                      % DEFAULT_PORT, "user": "Your map server login name",
                      "pass": "Map server password; saved in plain text on this PC, like Enhanced Map's"}

        def _page_action(action):
            """Make a settings page button callback that queues action for Map Pings' main loop."""
            def fn(*args):
                """Button callback: queue the action."""
                _queue_app(action)

            return fn

        def draw_send(f, x, y):
            """Draw the SEND A PING section: the four ping buttons, Reconnect, History, the wheel drag hint
            and the status line.
            """
            g, store, w = f.g, f.store, f.w
            bx = x + 12
            for t in (LOOK, DANGER, GO, HELP):
                label, hue = TYPE_INFO[t][:2]
                cap = label + "..."
                Kit.art_button(g, store, "ping%d" % t, Kit.ART_PLAY, bx, y + 28, cap, PING_TIP % label,
                               hue=hue, on_click=_page_action(("target", t)))
                bx += 35 + Kit.text_w(cap) + 16
            Kit.art_button(g, store, "recon", Kit.ART_PLAY, x + 12, y + 58, "Reconnect", "Reconnect to the map server",
                           on_click=_page_action(("reconnect",)))
            hx = x + 12 + 35 + Kit.text_w("Reconnect") + 16
            Kit.art_button(g, store, "history", Kit.ART_PAGE, hx, y + 58, "History",
                           "Open or close the window of recent pings, yours and others'",
                           on_click=_page_action(("history",)))
            gx = hx + 35 + Kit.text_w("History") + 16
            app = st["app"]
            if app is not None:
                Kit.add_label(g, Kit.fit("Wheel drag: up Look, right Danger, down Go, left Help", x + w - 12 - gx),
                              gx, y + 61, Kit.HUE_INFO)
            lbl = Kit.add_label(g, "", x + 12, y + 90, Kit.HUE_INFO)
            page["status"] = lbl
            if app is not None:
                # The status line is shared with the app, so status changes show here at once.
                app.status_label, app.status_w = lbl, w - 24
                Kit.set_text(lbl, Kit.fit(app.status_text or "Starting", w - 24))

        def draw_login(f, x, y):
            """Draw the MAP LOGIN section: server, port, user and password boxes and the Save button.

            The boxes start from the saved login, not from what the app holds.
            """
            g, w = f.g, f.w
            saved = Settings()
            col = (w - 36) // 2
            page["fields"] = fields = {}
            for i, (key, caption, value) in enumerate((
                    ("host", "Server address:", saved.host), ("port", "Port:", str(saved.port)),
                    ("user", "Map username:", saved.user), ("pass", "Map password:", saved.password))):
                fx = x + 12 + (i % 2) * (col + 12)
                fy = y + 30 + (i // 2) * 48
                Kit.add_label(g, caption, fx, fy)
                fields[key] = Kit.with_tip(Kit.add_textbox(g, value, fx + 2, fy + 20, col - 8, numbers=key == "port"),
                                           LOGIN_TIPS[key])
            Kit.art_button(g, f.store, "save", Kit.ART_OK, x + 12, y + 128, "Save and connect",
                           "Save the four fields on this PC and connect")
            page["login"] = Kit.add_label(g, Kit.fit("Saved on this PC in plain text (password shows while typing).",
                                                     w - 236), x + 220, y + 131, Kit.HUE_INFO)

        def draw_keys(f, x, y):
            """Draw the HOTKEYS section: one box per ping type."""
            kx = x + 12
            page["keys"] = keys = {}
            for k in HOTKEY_ORDER:
                cap = k.capitalize() + ":"
                Kit.add_label(f.g, cap, kx, y + 36)
                keys[k] = Kit.with_tip(Kit.add_textbox(f.g, HOTKEYS[k], kx + Kit.text_w(cap) + 8, y + 33, 84,
                                                       numbers=False), KEY_TIP % label_of(TYPE_KEYS[k]))
                kx += Kit.text_w(cap) + 8 + 84 + 16

        # Option layout numbers: label gap, field width, unit gap.
        NUM = {"lgap": 8, "fw": 44, "ugap": 6}
        # The settings page: sections in order, each a list of rows the form builder draws.
        PAGE = (("SEND A PING  (or a hotkey or wheel drag)", (("custom", 0, draw_send),), {"sh": H_SEND, "top": 0}),
                ("MAP LOGIN  (when TazUO's Enhanced Map is off)", (("custom", 0, draw_login),),
                 {"sh": H_LOGIN, "top": 0}), ("OPTIONS", (
                    ("check", "sounds", "Play a sound for each ping", "For your pings and others'", {"stay": True}),
                    ("check", "gesture", "Ping with a mouse-wheel drag", "Hold the wheel on a spot and drag: up Look "
                     "here, right Danger!, down Go here, left Need help", {"dx": 312}),
                    ("check", "share", "Show me on guildmates' maps", "Sends your position (map login only; TazUO's "
                     "Enhanced Map does its own)", {"stay": True}), ("gap", 28),
                    ("num", "ping_secs", "Ping stays:", "How long a ping's marker and pulse stay", "s",
                     OPT_LIMITS["ping_secs"][0], OPT_LIMITS["ping_secs"][1], dict(NUM, stay=True)),
                    ("num", "drag", "Drag distance:", "Pixels the wheel drag must move to count", "px",
                     OPT_LIMITS["drag"][0], OPT_LIMITS["drag"][1], dict(NUM, dx=312))), {"top": 32}),
                ("HOTKEYS  (blank = none)", (("custom", 0, draw_keys),), {"sh": H_KEYS, "top": 0}))

        def page_table(w):
            """The page layout for a given width (it is the same at every width)."""
            return PAGE

        # The page helper: reads and saves the options and reports the page height.
        cfg = Kit.Page(settings, page_table, save_settings)

        def build_config(g, x, y, w):
            """Build the settings page: the form and the Connection drop down beside its options."""
            f = Kit.Form(g, x, y, w, settings, PAGE)
            yo = y + H_SEND + H_LOGIN + 2 * Kit.GAP
            Kit.add_label(g, "Connection:", x + 312, yo + 60)
            idx = CONN_CODES.index(settings["connection"]) if settings["connection"] in CONN_CODES else 0
            dd = G.CreateDropDown(190, [c[1] for c in CONNECTIONS], idx)
            dd.SetPos(x + 414, yo + 56)
            g.Add(dd)
            Kit.with_tip(dd, "TazUO's Enhanced Map while it is on, or the login above")
            page.update({"f": f, "dd": dd, "seen_keys": dict(HOTKEYS), "next_read": 0.0})

        def poll_config(force=False):
            """Read the settings page and apply changes (the settings window's poll, client thread).

            Runs about five times a second while the page is open; force reads at once (the page is
            closing). A Save click saves the login. Option changes are saved and queued for the main loop.
            Hotkey boxes are applied only after the text has stood unchanged for about a second (or when
            the page closes), so half-typed keys are never registered.
            """
            f = page["f"]
            if f is None:
                return
            if Kit.was_clicked(f.store, "save"):
                _save_login()
            now = time.time()
            # Read at most every 0.2 s.
            if not force and now < page["next_read"]:
                return
            page["next_read"] = now + 0.2
            new = f.read()
            i = Kit.dd_index(page["dd"], -1)
            if 0 <= i < len(CONNECTIONS):
                new["connection"] = CONNECTIONS[i][0]
            if new != settings:
                settings.update(new)
                save_settings()
                _queue_app(("options",))
            new = {}
            for k, tb in page["keys"].items():
                try:
                    new[k] = _norm_key(tb.Text)
                except Exception:
                    new[k] = _norm_key(HOTKEYS[k])
            # The page closing takes what is typed.
            if force and new != page["seen_keys"]:
                page["typed"] = page["seen_keys"] = new
                HOTKEYS.update(new)
                save_settings()
                _queue_app(("rehook",))
            # Still being typed: wait for it to settle.
            elif new != page.get("typed"):
                page["typed"], page["stable"] = new, 0
            elif new != page["seen_keys"]:
                page["stable"] = page.get("stable", 0) + 1
                # Unchanged for about a second (five reads), or the page closing.
                if force or page["stable"] >= 5:
                    page["seen_keys"] = new
                    HOTKEYS.update(new)
                    save_settings()
                    _queue_app(("rehook",))

        def _save_login():
            """Check and save the login fields, hand them to the app and ask it to connect.

            All four fields must be filled and the port a number from 1 to 65535.
            """
            f = page["fields"]
            try:
                host = f["host"].Text.strip()
                port_text = f["port"].Text.strip()
                user = f["user"].Text.strip()
                password = f["pass"].Text
            except Exception:
                return
            try:
                port = int(port_text)
            except ValueError:
                port = 0
            if not host or not user or not password or not (0 < port < 65536):
                Kit.set_text(page["login"], "Fill in all four fields (the port is a number)", Kit.HUE_BAD)
                return
            saved = Settings()
            saved.host, saved.port, saved.user, saved.password = host, port, user, password
            saved.save()
            Kit.set_text(page["login"], "Saved", Kit.HUE_GOOD)
            app = st["app"]
            if app is not None:
                s = app.settings
                s.host, s.port, s.user, s.password = host, port, user, password
                app.pending.append(("save_setup",))

        def config_closed():
            """Settings page closed: take the last typed values, then drop the page state."""
            poll_config(True)
            app = st["app"]
            if app is not None and app.status_label is page.get("status"):
                app.status_label = None
            page.update({"f": None, "dd": None, "status": None, "keys": None, "fields": None, "login": None})

        def _offer_ping(x, y, m=None, kind="danger", who=None):
            """HOST service "pings.send": another module sends a ping of yours.

            kind is "look", "danger", "go" or "help"; m is the facet (None means yours); who names the
            sender. Call it from a tick (client thread). True means shown and sent (or shown only when not
            connected); False means not now (Map Pings stopping, or the last one too recent): ask again on a
            later tick.
            """
            app = st["app"]
            if app is None or app._shut:
                return False
            if m is None:
                m = API.GetMap()
            return app.send_auto(int(x), int(y), int(m), TYPE_KEYS.get(kind, DANGER), who)

        # Saved options are read once, when the part is built.
        load_settings()

        def _start():
            """Start the app and publish the pings.send service."""
            st["app"] = PingApp()
            st["app"].start()
            cleanup.service("pings.send", _offer_ping)

        def _tick():
            """Client tick: run one pass of the main loop."""
            if st["app"] is not None:
                st["app"].step()

        def _thread_tick():
            """Script thread tick: network work."""
            if st["app"] is not None:
                st["app"].thread_step()

        def _interval():
            """Seconds until the next tick.

            0.02 while the wheel is held, 0.05 while something is under way (our cursor up, clicks or
            map-server lines waiting), else 0.1: a wheel gesture needs a drag, so a 0.1 s first look still
            catches it.
            """
            app = st["app"]
            if app is None:
                return 0.05
            if app.gesture is not None:
                return 0.02
            if app.aim is not None or app.pending or app.inbox or app.jobs or app.outbox:
                return 0.05
            return 0.1

        def _stop():
            """Stop: release the service and shut the app down."""
            cleanup.close()
            app, st["app"] = st["app"], None
            if app is not None:
                app.shutdown()

        # Hooks of the part: both ticks (the client one runs the screen side, the thread one the network)
        # and the settings page callbacks.
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": build_config, "poll_config": poll_config, "config_closed": config_closed,
                "thread_tick": _thread_tick, "interval": _interval}

    def _part_corpse():
        """Builds the Corpse part and returns its hooks: back to your corpse, and your things back from it.

        When you die it remembers where (x, y, facet) and when, finds your corpse there (the corpse item
        that turns up beside where you died, with your body and, when the client knows it, your name)
        and points a tracking arrow of its own at it. The window shows how far and which way, and counts
        down until the corpse turns to bones and then decays (red in the last minute, with one alert).
        After you are resurrected, Get my things (only when you press it) opens the corpse and moves your
        items into your backpack one at a time. It stops when you press Stop, when a target cursor is up,
        when you pick something up, when you walk away, before you would go over your weight limit and
        after FAIL_STOP refused moves in a row. Optionally (off at first) a Need help ping on your corpse
        goes to your guild through Map Pings. A second death replaces the first; the corpse is kept per
        character, so logging out and back in keeps it. Only this part's own arrow is ever touched.
        Nothing here acts on its own: the only actions are the ones the player clicks.
        """
        # Part key; the saved keys below keep the part's earlier name so saved data carries over.
        KEY = "corpserun"
        TITLE = "Corpse"
        # Per character: "arrow=1;restore=1;ping=0;decay=15;bones=45".
        SETTINGS_KEY = "CorpseRun_settings"
        # Where the window sits, saved the moment it is let go.
        POS_KEY = "CorpseRun_pos"
        # Minimised when you left, kept for the next start.
        MIN_KEY = "CorpseRun_min"
        # Per character: the corpse remembered (see save_rec).
        CORPSE_KEY = "CorpseRun_corpse"
        # The ASCII of CORP: this part's own tracking arrow; Map Pings uses another, and each clears only
        # its own.
        ARROW_ID = 0x434F5250
        # Graphic of a corpse.
        CORPSE_GRAPHIC = 0x2006
        # A player corpse turned to bones is the same item with another graphic in this range.
        BONES_FIRST, BONES_LAST = 0x0ECA, 0x0ED2
        # On In Mani Ylem a player corpse turns to bones after 15 minutes and the bones (your items still
        # in them) are gone 45 minutes later, an hour in all. These are the default minutes of the two
        # settings.
        DEFAULT_DECAY_MIN = 15
        DEFAULT_BONES_MIN = 45
        # What the two minute fields accept.
        MIN_LO, MIN_HI = 1, 120
        # The countdown turns red this many seconds before it ends, and one alert says so.
        RED_SECS = 60
        # Seconds past the end before a corpse still not seen is forgotten (the shard may be slower than
        # the numbers).
        DECAYED_GRACE = 120.0
        # Alert kind for the decay warning: sound, on or off on Settings > Alerts.
        ALERT_DECAY = "corpserun.decay"
        # Look for the corpse this long after the death.
        FIND_SECS = 20.0
        # Body graphics of a player's corpse: its amount is the dead body's graphic.
        HUMAN_BODIES = (0x190, 0x191, 0x25D, 0x25E, 0x29A, 0x29B)
        # Tiles round you that are searched (one client call).
        SEEK_RANGE = 24
        # Seconds between looks at a known corpse.
        ITEM_EVERY = 1.0
        # Tiles: how close you must stand to use or loot it.
        REACH = 2
        # Least gap after the client reports a new corpse before the search runs again.
        POKE_GAP = 0.25
        DIED_HOLD = 10.0
        # Seconds between two moves (the shard's drag delay).
        MOVE_GAP = 0.7
        # Extra looks at a move the server hasn't answered yet.
        MOVE_RECHECK = 2
        # Items taken by one press at most.
        PLAN_CAP = 250
        # Journal text of the server's "You must wait..." answer (cliloc 500119).
        J_WAIT = ("must wait to perform another action",)
        # Hair and beard graphics: they ride on a corpse and are never taken.
        HAIR_FIRST, HAIR_LAST = 0x203B, 0x204D
        # Seconds a Need help ping waits for Map Pings' pace.
        PING_TRY = 15.0
        # Full window width.
        W = 420
        # Size of the minimised bar.
        MINI_W, MINI_H = 280, 46
        # Height of the YOUR CORPSE section.
        BODY_H = 128
        H = Kit.MARGIN + 30 + Kit.GAP + BODY_H + Kit.MARGIN
        settings = {"arrow": True, "restore": True, "ping": False, "decay": DEFAULT_DECAY_MIN,
                    "bones": DEFAULT_BONES_MIN}
        # What a fresh character gets.
        DEFAULTS = dict(settings)
        # Part state. rec is the corpse remembered; job is a Get my things run; body is the graphic of
        # your own body, read while alive and kept as the corpse's amount; note is a message shown for a
        # few seconds.
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "body": 0, "body_at": 0.0,
              "note_until": 0.0, "name": "", "drawn": None, "drawn_c": None, "unnamed": False, "hooked": False,
              "find_at": 0.0}
        win = {"g": None, "c": {}, "store": ({}, {})}
        # Text boxes of the settings page that are being typed in.
        typed = {}
        cleanup, queue, say = Kit.basics(st, TITLE)
        # Allowed range of the two minute settings.
        NUMS = {"decay": (MIN_LO, MIN_HI), "bones": (MIN_LO, MIN_HI)}

        def load_settings():
            """Read the saved settings. A save still holding the old 7 and 7 minutes (never right on this
            shard) is moved to the current defaults.
            """
            Kit.kv_load(SETTINGS_KEY, ";", settings, NUMS)
            if (settings["decay"], settings["bones"]) == (7, 7):
                settings["decay"], settings["bones"] = DEFAULT_DECAY_MIN, DEFAULT_BONES_MIN

        def save_settings():
            """Save the settings."""
            Kit.kv_save(SETTINGS_KEY, ";", settings, ("arrow", "restore", "ping", "decay", "bones"), NUMS)

        def load_rec():
            """Read the corpse remembered, or None.

            Format: "1|serial|x|y|facet|died|body|spot|exact|name". spot 0 means the place isn't known yet
            and the corpse is being looked for round you; exact 0 means you were found dead at the start,
            so the time of death is a guess and the countdown an upper bound.
            """
            p = Kit.get_var(CORPSE_KEY).split("|")
            if len(p) < 8 or p[0] != "1":
                return None
            try:
                return {"serial": int(p[1]), "x": int(p[2]), "y": int(p[3]), "facet": int(p[4]),
                        "died": float(p[5]), "body": int(p[6]), "spot": p[7] == "1", "exact": len(p) < 9 or p[8] != "0",
                        "name": p[9] if len(p) > 9 else ""}
            except ValueError:
                return None

        def save_rec():
            """Save the corpse remembered (the same format), or clear the saved value when there is none. The
            name loses any bar so it can't break the format.
            """
            r = st["rec"]
            if r is None:
                Kit.put_var(CORPSE_KEY, "")
                return
            Kit.put_var(CORPSE_KEY, "1|%d|%d|%d|%d|%.0f|%d|%d|%d|%s" % (
                r["serial"], r["x"], r["y"], r["facet"], r["died"], r["body"], 1 if r["spot"] else 0,
                1 if r["exact"] else 0, r["name"].replace("|", "")))

        def note(text, secs=6.0, spot=None):
            """Show a note in the window for secs seconds and in the journal.

            spot is an (x, y) pair that appears in text as "x, y"; the window copy has it replaced by xy's
            veiled form, while the journal line keeps the text as given.
            """
            st["note"] = text if spot is None else text.replace("%d, %d" % spot, xy(*spot))
            st["note_until"] = time.time() + secs
            st["lbl_at"] = 0.0
            say(journal_case(text))

        def remaining(now):
            """Seconds until the corpse is gone, from the time of death and the two minute settings. A time of
            death in the future (the clock was set back) is pulled back to now.
            """
            r = st["rec"]
            if r is None:
                return 0.0
            if r["died"] > now:
                r["died"] = now
            return 60.0 * (settings["decay"] + settings["bones"]) - (now - r["died"])

        def clock(secs):
            """Seconds as minutes:seconds."""
            secs = max(0, int(secs))
            return "%d:%02d" % (secs // 60, secs % 60)

        # Shared helpers of the mother: an item by serial, and the item held on the cursor.
        item_of = Kit.find_item
        held_item = Kit.held_item

        def cursor_up():
            """Is a target cursor up (ours, another module's or the client's)?"""
            return bool(HOST.cursor_busy(KEY)) or bool(API.HasTarget())

        def is_hair(it):
            """Is the item hair or a beard? Judged by graphic, or by layer when the item data has one."""
            if HAIR_FIRST <= int(it.Graphic) <= HAIR_LAST:
                return True
            d = it.GetItemData()
            return d is not None and int(d.Layer) in (11, 16)

        def weight_of(it):
            """Weight of an item and what is in it, in stones as the item data states. 255 means no weight set
            and counts as 0.
            """
            d = it.GetItemData()
            w = int(d.Weight) if d is not None else 0
            total = (0 if w >= 255 else w) * max(1, int(it.Amount or 1))
            if it.IsContainer:
                for x in API.ItemsInContainer(int(it.Serial), True) or ():
                    d = x.GetItemData()
                    xw = int(d.Weight) if d is not None else 0
                    if xw < 255:
                        total += xw * max(1, int(x.Amount or 1))
            return total

        def build_window():
            """Build the window: where the corpse is, how long it lasts, and the Get my things, Ping for help
            and Forget buttons. Follows the layout slot when it has one.
            """
            z = told(wnd, st, W, H)
            w, h = z if z else (W, H)
            g, store, c = wnd.begin(w, h)
            if not st["minimized"]:
                wnd.frame(g)
                M = Kit.MARGIN
                IW = w - 2 * M
                yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, h - yb - M, "YOUR CORPSE  (where, how long it lasts)")
                c["where"] = Kit.add_label(g, "", M + 12, yb + 28, Kit.HUE_TEXT)
                c["decay"] = Kit.add_label(g, "", M + 12, yb + 48, Kit.HUE_INFO)
                c["info"] = Kit.add_label(g, "", M + 12, yb + 68, Kit.HUE_INFO)
                by = yb + 92
                xb = M + 10
                c["go"] = Kit.art_button(g, store, "go", Kit.ART_PLAY, xb, by, "Get my things",
                                         "Move your things from your corpse to your backpack one by one (stand "
                                         "beside it; click again to stop)", on_click=queue("go"))
                xb += 35 + max(Kit.text_w("Get my things"), Kit.text_w("Stop")) + 14
                Kit.art_button(g, store, "help", Kit.ART_PLAY, xb, by, "Ping for help",
                               "Send your guild a Need help ping on your corpse (needs World Map > Map Pings)",
                               on_click=queue("help"))
                xb += 35 + Kit.text_w("Ping for help") + 14
                Kit.art_button(g, store, "forget", Kit.ART_CLOSE, xb, by, "Forget",
                               "Forget this corpse and take its arrow down", on_click=queue("forget"))
            wnd.end(g)
            st["lbl_at"] = 0.0

        # The window: key, title, state, controls, builder, saved place and minimised flag, default
        # place, mini size, tray icon (bones) and cleanup; locked in place by the layout.
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (220, 220), (MINI_W, MINI_H), 0x0ECA,
                         cleanup, lock=True, clear={"c": {}})

        def show_full():
            """Show the full window again if it was minimised or folded into the bar."""
            if not st["minimized"] and not st["docked"]:
                return
            st["minimized"], st["docked"] = False, False
            HOST.dock_forget(KEY)
            Kit.save_min(MIN_KEY, False)
            build_window()

        def texts(me, now, mm):
            """Work out the window's texts.

            Returns (where text, its hue, decay text, its hue, info text, minimised bar text). me is the
            player and mm the facet. Counting times are marked "at most" when the death was not seen.
            Coordinates in the texts go through xy.
            """
            r = st["rec"]
            j = st["job"]
            if r is None:
                dead = bool(st["was_dead"])
                info = st["note"] if st["note"] and now < st["note_until"] else \
                    ("Find a healer or a resurrection." if dead else "When you die, this window shows the way back.")
                return ("No corpse to find.", Kit.HUE_TEXT, "", Kit.HUE_INFO, info, TITLE + ": none")
            left = remaining(now)
            mx, my = int(me.X), int(me.Y)
            if not r["spot"]:
                where, mini = "Looking for your corpse round you", "looking"
            elif mm != r["facet"]:
                where = "On %s, at %s" % (Kit.facet_name(r["facet"]), xy(r["x"], r["y"]))
                mini = Kit.facet_name(r["facet"])
            else:
                wt = Kit.where_text(r["x"] - mx, r["y"] - my)
                where = "%s%s, at %s" % (wt[0].upper(), wt[1:], xy(r["x"], r["y"]))
                mini = wt
            bones_at = 60.0 * settings["bones"]
            most = "" if r["exact"] else "at most "
            if left > bones_at:
                decay = "Bones in %s%s, gone in %s%s" % (most, clock(left - bones_at), most, clock(left))
            elif left > 0:
                decay = ("Bones %s; gone in %s%s" % ("now" if r["exact"] else "soon", most, clock(left)))
            else:
                decay = "Should have decayed by now"
            dhue = Kit.HUE_BAD if left <= RED_SECS else Kit.HUE_INFO
            if st["note"] and now < st["note_until"]:
                info = st["note"]
            elif j is not None:
                if j["phase"] == "open":
                    info = "Opening your corpse"
                else:
                    info = "Moving %d / %d" % (min(j["i"], len(j["plan"])), len(j["plan"]))
            else:
                died = (("Died %s ago." % Kit.ago(now - r["died"])) if r["exact"] else "Found as a ghost.")
                if not r["serial"] and st["unnamed"]:
                    info = "Waiting for the corpse's name: click it once."
                elif st["was_dead"]:
                    info = died + " Be resurrected, then click Get my things."
                elif r["serial"] and r["spot"]:
                    info = died + " Stand by it and click Get my things."
                else:
                    info = died + " Not seen there yet."
            mini = "%s  %s" % (mini, clock(left)) if left > 0 else mini
            return where, Kit.HUE_TEXT, decay, dhue, info, "%s: %s" % (TITLE, mini)

        def refresh(me, now, mm, force=False):
            """Update the window's labels, at most twice a second (force skips that), and only when the texts
            changed since the last draw. The minimised bar shows one line. Client thread.
            """
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return
            if not force and now < st["lbl_at"]:
                return
            st["lbl_at"] = now + 0.5
            where, whue, decay, dhue, info, mini = texts(me, now, mm)
            c = win["c"]
            if st["minimized"]:
                hue = Kit.HUE_BAD if st["rec"] is not None and remaining(now) <= RED_SECS else Kit.HUE_INFO
                sig = (mini, hue)
            else:
                sig = (where, whue, decay, dhue, info, st["job"] is not None)
            # Same texts and same controls: nothing to write.
            if sig == st["drawn"] and c is st["drawn_c"]:
                return
            st["drawn"], st["drawn_c"] = sig, c
            if st["minimized"]:
                lbl = c.get("status")
                if lbl is not None:
                    Kit.set_text(lbl, Kit.fit(mini, MINI_W - 90), hue)
                return
            for k, text, tone in (("where", where, whue), ("decay", decay, dhue), ("info", info, Kit.HUE_INFO)):
                Kit.set_text(c[k], Kit.fit(text, W - 2 * Kit.MARGIN - 24), tone)
            Kit.set_text(c["go"], "Stop" if st["job"] is not None else "Get my things",
                         Kit.HUE_TITLE if st["job"] is not None else Kit.HUE_TEXT)

        def arrow_tick(me, mm):
            """Keep the tracking arrow on the corpse while it is known, on your facet and more than REACH tiles
            away; take it down otherwise.
            """
            r = st["rec"]
            want = None
            if settings["arrow"] and r is not None and r["spot"] and mm == r["facet"]:
                if max(abs(int(me.X) - r["x"]), abs(int(me.Y) - r["y"])) > REACH:
                    want = (r["x"], r["y"])
            if want == st["arrow"]:
                return
            if want is None:
                Kit.drop_arrow(st, ARROW_ID)
            else:
                API.TrackingArrow(want[0], want[1], ARROW_ID)
                st["arrow"] = want

        def on_death(me, now, at_start=False):
            """You died (or were found dead when the part started, at_start): remember the spot and time, start
            looking for the corpse, optionally queue the Need help ping and show the window.
            """
            if st["job"] is not None:
                stop_job("you died")
            x, y, m = int(me.X), int(me.Y), int(API.GetMap())
            st["name"] = str(me.Name or "")
            st["rec"] = {"serial": 0, "x": x, "y": y, "facet": m, "died": now, "body": st["body"],
                         "spot": not at_start, "exact": not at_start, "name": st["name"]}
            # The corpse turns up beside where you died; look for FIND_SECS seconds.
            st["seek_until"], st["seek_at"] = now + FIND_SECS, now
            st["gone_since"], st["warned"], st["unnamed"] = None, False, False
            st["refused"] = set()
            save_rec()
            # Found dead at the start: the place and time are guesses, so the corpse is looked for round you.
            if at_start:
                say("you are a ghost: looking for your corpse round you.")
            else:
                say("you died at %d, %d (%s). Bones in %s, gone %s later." % (
                    x, y, Kit.facet_name(m), Kit.count(settings["decay"], "minute"),
                    Kit.count(settings["bones"], "minute")), Kit.HUE_BAD)
                if settings["ping"]:
                    st["ping"] = (x, y, m, now + PING_TRY)
            if settings["restore"]:
                show_full()

        # Name prefixes a corpse item may carry in front of the owner's name.
        CORPSE_PREFIXES = ("a corpse of ", "corpse of ", "the remains of ", "remains of ")

        def owner_name():
            """Your name as the corpse would carry it, lower case: from the record, else the last name seen."""
            r = st["rec"]
            return ((r["name"] if r is not None and r["name"] else st["name"]) or "").strip().lower()

        def mine(it, graphic, me_name):
            """Is this item your corpse? 2 yes (the name matches), 1 maybe (no name to compare, or unnamed),
            0 no.

            The amount of a corpse is its body graphic, so a different amount is someone else's. Bones with
            no amount can't be a player's.
            """
            r = st["rec"]
            body = r["body"] if r is not None else 0
            amt = int(it.Amount or 0)
            if body and amt and amt != body:
                return 0
            bones = BONES_FIRST <= graphic <= BONES_LAST
            if bones and (not amt or (not body and amt not in HUMAN_BODIES)):
                return 0
            n = (str(it.Name or "") or str(it.NameAndProps(False) or "")).strip().lower()
            owner = None
            for p in CORPSE_PREFIXES:
                if n.startswith(p):
                    owner = n[len(p):].strip()
                    break
            if owner is None:
                if not n or n in ("corpse", "a corpse", "bones", "remains") or bones:
                    return 1
                owner = n
            if not me_name:
                return 1
            return 2 if owner == me_name else 0

        def scan_corpses(items, cx, cy, lim, acc, me_name):
            """Look through (item, graphic) pairs for the best match to your corpse.

            acc[0] gets the nearest (distance, serial, x, y), the higher serial winning a tie; acc[1] is set
            when an unnamed possible corpse was seen. Only items within lim tiles of (cx, cy) count.
            """
            for it, gr in items:
                s, ix, iy = int(it.Serial), int(it.X), int(it.Y)
                d = max(abs(ix - cx), abs(iy - cy))
                if d > lim:
                    continue
                m = mine(it, gr, me_name)
                if m == 1:
                    acc[1] = True
                if m != 2:
                    continue
                e = (d, s, ix, iy)
                b = acc[0]
                if b is None or d < b[0] or (d == b[0] and s > b[1]):
                    acc[0] = e

        def find_corpse(me):
            """Find your corpse. Returns ((serial, x, y) or None, whether an unnamed candidate was seen).

            Searches round the death spot, or round you when the spot isn't known. One read of the ground
            items in SEEK_RANGE is split into corpses and bones by graphic; corpses first, bones only when
            no corpse was found.
            """
            r = st["rec"]
            me_name = owner_name()
            cx, cy, lim = (r["x"], r["y"], 3) if r["spot"] else (int(me.X), int(me.Y), SEEK_RANGE)
            acc = [None, False]
            corpses, bones = [], []
            # One walk of the ground items instead of one per corpse and bones graphic: the client walks every
            # item for each call.
            for it in API.GetItemsOnGround(SEEK_RANGE) or ():
                g = int(it.Graphic)
                if g == CORPSE_GRAPHIC:
                    corpses.append((it, g))
                elif BONES_FIRST <= g <= BONES_LAST:
                    bones.append((it, g))
            scan_corpses(corpses, cx, cy, lim, acc, me_name)
            if acc[0] is None:
                scan_corpses(bones, cx, cy, lim, acc, me_name)
            return (None if acc[0] is None else acc[0][1:]), acc[1]

        def forget(why=None):
            """Drop the corpse remembered: stop a running job, clear the arrow and the saved value; why goes to
            the journal.
            """
            if st["job"] is not None:
                stop_job(None)
            st["rec"] = st["ping"] = st["gone_since"] = None
            st["unnamed"] = False
            st["refused"] = set()
            Kit.drop_arrow(st, ARROW_ID)
            save_rec()
            if why:
                say(why)
            st["lbl_at"] = 0.0

        def corpse_tick(me, now, mm):
            """Per tick while a corpse is remembered: find it, follow where it lies, forget it when it is gone
            or decayed, and give the one alert in its last minute.
            """
            r = st["rec"]
            left = remaining(now)
            dist = max(abs(int(me.X) - r["x"]), abs(int(me.Y) - r["y"]))
            if not r["serial"]:
                # Within 12 tiles on its facet: worth a look.
                near = r["spot"] and mm == r["facet"] and dist <= 12
                # A corpse of unknown spot that was seen without a name: the player may click it.
                offered = not r["spot"] and st["unnamed"]
                seeking = now < st["seek_until"]
                if (seeking and now >= st["seek_at"]) or (not seeking and (near or offered) and now >= st["look_at"]):
                    st["seek_at"] = now + 0.5
                    st["look_at"] = now + 1.0
                    st["find_at"] = now
                    hit, unnamed = find_corpse(me)
                    if hit is not None:
                        r["serial"], r["x"], r["y"] = hit
                        st["unnamed"] = False
                        if not r["name"]:
                            r["name"] = owner_name()
                        if not r["spot"]:
                            r["spot"] = True
                            say("found your corpse at %d, %d." % (r["x"], r["y"]))
                        save_rec()
                        st["lbl_at"] = 0.0
                    elif unnamed != st["unnamed"]:
                        st["unnamed"] = unnamed
                        st["lbl_at"] = 0.0
                # The search window is over and nothing was seen: it was left before this part started.
                if (not r["serial"] and not r["spot"] and now >= st["seek_until"] and not st["unnamed"]):
                    forget("your corpse isn't in view (it was left before %s started)." % TITLE)
                    return
            # Known corpse: look at it once a second (or when the clock went back).
            elif now >= st["item_at"] or st["item_at"] - now > ITEM_EVERY:
                st["item_at"] = now + ITEM_EVERY
                it = item_of(r["serial"])
                if it is not None:
                    st["gone_since"] = None
                    ix, iy = int(it.X), int(it.Y)
                    # It moved (dragged, or picked up and dropped): follow it, unless it is in a container.
                    if (ix or iy) and (ix, iy) != (r["x"], r["y"]) and not int(it.Container or 0):
                        r["x"], r["y"] = ix, iy
                        save_rec()
                # Near it, in view of nothing, with no job: it may be gone.
                elif mm == r["facet"] and st["job"] is None and dist <= 12:
                    if st["gone_since"] is None:
                        st["gone_since"] = now
                    # Six seconds of absence close to it: looted or decayed.
                    elif now - st["gone_since"] >= 6.0:
                        forget("your corpse isn't at %d, %d any more (decayed or looted)." % (r["x"], r["y"]))
                        return
                else:
                    st["gone_since"] = None
            # The one alert, in the last minute.
            if left <= 60 and not st["warned"] and left > 0:
                st["warned"] = True
                where = Kit.where_text(r["x"] - int(me.X), r["y"] - int(me.Y)) if mm == r["facet"] else \
                    "on " + Kit.facet_name(r["facet"])
                HOST.alert(ALERT_DECAY, "Corpse decays in under a minute (%s)" % where, "warn")
            if left <= -DECAYED_GRACE and item_of(r["serial"]) is None:
                forget("your corpse has decayed.")

        def ping_tick(now):
            """Send the queued Need help ping through Map Pings' pings.send service, retrying on later ticks
            until PING_TRY seconds pass. Says so when Map Pings is off.
            """
            p = st["ping"]
            if p is None:
                return
            x, y, m, until = p
            fn = HOST.services.get("pings.send")
            if fn is None or now > until:
                st["ping"] = None
                if fn is None:
                    say("World Map > Map Pings is off, so no Need help ping was sent.")
                return
            try:
                if fn(x, y, m=m, kind="help"):
                    st["ping"] = None
                    say("Need help ping sent on your corpse.")
            except Exception:
                st["ping"] = None

        def start_job(me, now):
            """Start the Get my things job on your own corpse, if every precondition holds.

            Runs on the client tick when the Get my things button is pressed. Each failed check says why in the
            part's note line and returns; nothing is sent to the server until all of them pass. On success it
            double-clicks the corpse (so the client learns what is inside) and sets up the job record that
            job_tick and send_move work through. Notes that name a spot pass it as spot= so the window copy
            is veiled in streamer mode.
            """
            r = st["rec"]
            if st["job"] is not None:
                return
            if r is None:
                note("No corpse remembered.")
                return
            # A ghost cannot loot its own corpse, so there is nothing to start until the player is resurrected.
            if bool(st["was_dead"]):
                note("You are still a ghost: get resurrected first.")
                return
            spot = (r["x"], r["y"])
            if not r["serial"]:
                note("Your corpse hasn't been seen yet: go to %d, %d." % spot, spot=spot)
                return
            it = item_of(r["serial"])
            if it is None:
                note("Your corpse isn't in view yet (%d, %d)." % spot, spot=spot)
                return
            # mine() answers 2 for the player's corpse, 1 while the owner's name has not arrived yet (the client
            # only learns a corpse's name once it is clicked), anything else for someone else's body (R2: only
            # your own things are ever moved).
            whose = mine(it, int(it.Graphic), owner_name())
            if whose == 1:
                note("Waiting for the corpse's name: click it once.")
                return
            if whose != 2:
                note("That corpse isn't yours.")
                return
            # Items can only be lifted from a container within reach, so the player has to stand beside it.
            dx, dy = int(it.X) - int(me.X), int(it.Y) - int(me.Y)
            if max(abs(dx), abs(dy)) > REACH:
                note("Walk up to your corpse first (%s)." % Kit.where_text(dx, dy))
                return
            pack = int(API.Backpack or 0)
            if not pack:
                note("No backpack to put things in.")
                return
            # A pending target cursor or an item held on the cursor would be hit by the lift, so both block a start.
            if cursor_up():
                note("A target cursor is up: finish or cancel it first.")
                return
            if held_item():
                note("You are holding an item: put it down first.")
                return
            # The job is a small state machine: phase open (wait for the corpse's contents to arrive), then move
            # (one item at a time). at is the next time the job may act, until is the end of the opening wait,
            # tried holds serials already attempted, waits counts too-soon replies per item, move is the item the
            # client tick picked and check the one whose answer is awaited. The other counters feed the final
            # report and the stop rules.
            st["job"] = {"phase": "open", "corpse": r["serial"], "pack": pack, "at": now + 1.0,
                         "until": now + 3.0, "plan": [], "i": 0, "tried": set(), "waits": {},
                         "move": None, "check": None, "sent_at": 0.0, "last": 0, "rechecks": 0,
                         "hold": 0.0, "moved": 0, "refused": 0, "streak": 0, "why": None, "replans": 0}
            # Opens the corpse so that the client is sent its contents.
            API.UseObject(r["serial"])
            st["note"] = ""
            st["lbl_at"] = 0.0

        def make_plan(j):
            """List the items still lying in the corpse that are worth moving.

            j holds the corpse serial and the set of serials already tried. Items tried in this job, items the
            server refused on an earlier press and hair are left out; the list is capped at PLAN_CAP so one pass
            stays small. Returns a list of serials.
            """
            plan = []
            for it in API.ItemsInContainer(j["corpse"], False) or ():
                if len(plan) >= PLAN_CAP:
                    break
                s = int(it.Serial)
                if s not in j["tried"] and s not in st["refused"] and not is_hair(it):
                    plan.append(s)
            return plan

        def job_tick(me, now):
            """One client tick of the running job: decide whether to stop, wait, or pick the next item to move.

            Stops (with a reason shown to the player) when the player died, the corpse left view, the player
            walked away, a target cursor appeared or something other than our last item is held. It never sends
            anything itself: it only sets j["move"], and send_move sends it afterwards in the same tick.
            """
            j = st["job"]
            if j["why"]:
                stop_job(j["why"])
                return
            # A move is picked and not yet sent (send_move runs right after this in the same tick).
            if j["move"] is not None:
                return
            if st["was_dead"]:
                stop_job("you died")
                return
            it = item_of(j["corpse"])
            if it is None:
                stop_job("your corpse is gone from view")
                return
            if max(abs(int(it.X) - int(me.X)), abs(int(it.Y) - int(me.Y))) > REACH:
                stop_job("you walked away from your corpse")
                return
            # Wait for the answer to the previous move before choosing another: one item at a time keeps to the
            # server's own pace and makes a refusal attributable to one item.
            if j["check"] is not None and (now < j["at"] or not check_move(j, now)):
                return
            # The corpse's items arrive some time after it is opened: wait for a non-empty plan, but only until
            # the opening wait has run out, so an empty corpse still finishes.
            if j["phase"] == "open":
                if now < j["at"]:
                    return
                plan = make_plan(j)
                if not plan and now < j["until"]:
                    return
                j["plan"], j["i"], j["phase"] = plan, 0, "move"
                if not plan:
                    finish_job()
                    return
            # Pause after a too-soon reply from the server.
            if now < j["hold"]:
                return
            if cursor_up():
                stop_job("a target cursor is up")
                return
            h = held_item()
            # The last moved item may still show as held while the server's answer is on its way, so it is not
            # counted as the player picking something up.
            if h and h != j["last"]:
                stop_job("you picked something up")
                return
            plan = j["plan"]
            while j["i"] < len(plan):
                s = plan[j["i"]]
                j["i"] += 1
                if s in j["tried"]:
                    continue
                x = item_of(s)
                # Gone, or taken by hand or by the server meanwhile: skip it.
                if x is None or int(x.Container or 0) != j["corpse"]:
                    continue
                # Over the weight limit the server would refuse every further item, so stop with a clear reason
                # instead of collecting refusals. A zero maximum means the weight is not known yet.
                wmax, wnow = int(me.WeightMax or 0), int(me.Weight or 0)
                if wmax > 0 and (wnow >= wmax or wnow + weight_of(x) > wmax):
                    stop_job("the next item would put you over your weight limit (%d / %d stones)" % (wnow, wmax))
                    return
                j["tried"].add(s)
                j["move"] = s
                return
            # Anything that turned up in the corpse during the run gets a second look, at most twice.
            if j["replans"] < 2:
                j["replans"] += 1
                more = make_plan(j)
                if more:
                    j["plan"], j["i"] = more, 0
                    return
            finish_job()

        def check_move(j, now):
            """Read the server's answer to the last move, MOVE_GAP seconds after it went out.

            Returns True when the job may go on and False when it must wait longer or has stopped. An item no
            longer in the corpse counts as moved; a too-soon journal reply puts the same item back in the plan;
            an item still there after the rechecks is marked refused and, after three in a row, the job stops.
            """
            s = j["check"]
            it = item_of(s)
            where = int(it.Container or 0) if it is not None else None
            # The item was not found at all (lifted, not answered yet on a slow line): look again shortly.
            if where is None and j["rechecks"] < MOVE_RECHECK:
                j["rechecks"] += 1
                j["at"] = now + MOVE_GAP * 0.5
                return False
            # Anywhere but the corpse means it reached the pack, or was stacked into a pile there.
            if where != j["corpse"]:
                j["moved"] += 1
                j["streak"] = j["rechecks"] = 0
                j["check"] = None
                return True
            # The shard says to wait between moves: give the same item another go after a pause, twice at most.
            if (Journal.find(j["sent_at"], J_WAIT) is not None and j["waits"].get(s, 0) < 2):
                j["waits"][s] = j["waits"].get(s, 0) + 1
                j["tried"].discard(s)
                j["i"] = max(0, j["i"] - 1)
                j["check"] = None
                j["rechecks"] = 0
                j["hold"] = now + MOVE_GAP
                return False
            if j["rechecks"] < MOVE_RECHECK:
                j["rechecks"] += 1
                j["at"] = now + MOVE_GAP * 0.5
                return False
            j["check"] = None
            j["rechecks"] = 0
            j["refused"] += 1
            j["streak"] += 1
            # Each item gets one move per press, and the refused set is capped so it cannot grow without bound.
            if len(st["refused"]) < PLAN_CAP:
                st["refused"].add(s)
            if j["streak"] >= 3:
                stop_job("%d moves in a row were refused" % j["streak"])
                return False
            return True

        def send_move():
            """Send the move that job_tick picked, on the client tick.

            Does nothing without a pending move or while the module shuts down. A failing call becomes
            j["why"], which the next job_tick reports and stops on. Records when it was sent so the answer is
            read MOVE_GAP later.
            """
            j = st["job"]
            if j is None or j["move"] is None or st["shutting"]:
                return
            mv = j["move"]
            j["move"] = None
            try:
                API.MoveItem(mv, j["pack"])
            except Exception as ex:
                j["why"] = "a move failed (%s)" % ex
                return
            j["check"] = mv
            j["last"] = mv
            j["sent_at"] = time.time()
            j["at"] = j["sent_at"] + MOVE_GAP

        def finish_job():
            """End the job after the last item and tell the player the outcome.

            Counts what is left in the corpse. A job that moved nothing and has nothing left forgets the corpse;
            otherwise the message says how many items came back, how many were refused (those must be taken by
            hand) and how many remain so the button can be pressed again. A complete run forgets the corpse.
            """
            j, st["job"] = st["job"], None
            if j is None:
                return
            left = []
            if item_of(j["corpse"]) is not None:
                left = make_plan({"corpse": j["corpse"], "tried": set()})
            n_ref = len(st["refused"])
            if j["moved"] == 0 and not j["refused"] and not left:
                forget("nothing left in your corpse%s." % ((" but %s the server refused (take %s by hand)"
                     % (Kit.count(n_ref, "item"), "it" if n_ref == 1 else "them")) if n_ref else ""))
                return
            msg = "%s back in your backpack" % Kit.count(j["moved"], "item")
            if j["refused"]:
                msg += ", %d refused (left in your corpse: take %s by hand)" % (
                    j["refused"], "it" if j["refused"] == 1 else "them")
            if left:
                say("%s; %d still in your corpse (click Get my things again)." % (msg, len(left)),
                    Kit.HUE_BAD if j["refused"] else Kit.HUE_INFO)
                st["lbl_at"] = 0.0
                return
            forget(None)
            say("%s. Re-dress when you are ready." % msg, Kit.HUE_BAD if j["refused"] else Kit.HUE_GOOD)

        def stop_job(why=None, user=False):
            """End the job early and say why.

            why is a reason for the player; user is True when the Stop button was pressed, which gets a plain
            message. Clears the label timer so the window text redraws at once.
            """
            j, st["job"] = st["job"], None
            if j is None:
                return
            if user:
                say("stopped (%d moved)." % j["moved"])
            elif why:
                say("stopped: %s (%d moved)." % (why, j["moved"]), Kit.HUE_BAD)
            st["lbl_at"] = 0.0

        def act_go(me, now):
            """Get my things button: stop the running job, or start one."""
            if st["job"] is not None:
                stop_job(None, user=True)
            elif me is not None:
                start_job(me, now)

        def act_help(me, now):
            """Need help button: ask for a map ping on the remembered corpse spot.

            Needs Map Pings (World Map) to be on; ping_tick sends it and retries for PING_TRY seconds.
            """
            r = st["rec"]
            if r is None or not r["spot"]:
                note("No corpse to ping.")
            elif HOST.services.get("pings.send") is None:
                note("World Map > Map Pings is off: turn it on to send pings.")
            else:
                st["ping"] = (r["x"], r["y"], r["facet"], now + PING_TRY)

        def act_forget(me, now):
            """Forget button: drop the remembered corpse."""
            if st["rec"] is None:
                note("No corpse remembered.")
            else:
                forget("forgot your corpse.")

        # Queue names the window's buttons post, mapped to the functions the tick runs for them.
        ACTIONS = {"go": act_go, "help": act_help, "forget": act_forget}
        MOVE_HINT = ("One item every %.1f s; stops on Stop, a target cursor, picking something up, walking away or "
                     "going over your weight limit." % MOVE_GAP)

        def page_table(w):
            """The Corpse part's settings page: the table Kit.Page builds its controls from.

            w is the page width, used to wrap the Get my things hint. Returns the sections for when you die,
            the decay times and the hint, then the shared atlas page.
            """
            t1 = "Corpse to bones:"
            return (("WHEN YOU DIE", (
                        ("check", "arrow", "Point the tracking arrow at your corpse", "Its own arrow (others are left "
                         "alone); hidden when you stand beside it"),
                        ("check", "restore", "Open the Corpse window when you die, even minimized or folded",
                         "It comes back full size"),
                        ("check", "ping", "Send a Need help map ping on your corpse when you die",
                         "Your guild sees where you died (needs World Map > Map Pings); off at first, as it shows "
                         "where you are")), {"pad": 4}), ("DECAY  (minutes; the shard's times)", (
                        ("num", "decay", t1, "Minutes from death until bones", None, MIN_LO, MIN_HI, {"stay": True}),
                        ("num", "bones", "Bones gone after:", "Minutes the bones (with your things) last", None, MIN_LO,
                         MIN_HI, {"dx": Kit.text_w(t1) + 86})), {"ldy": 4, "fw": 40, "pad": 8}),
                    ("GET MY THINGS  (one item at a time)", [("note", ln) for ln in Kit.wrap(MOVE_HINT, w - 28)]),
                    atlas_page("corpse"))

        def settle(f, new):
            """Hold back a number that is still being typed.

            Kit.Page calls this before it applies a change. A decay or bones field is only accepted after its
            text has stood still for a second (unless the page is forced), so typing 15 never briefly applies 1.
            """
            now = time.time()
            for k in ("decay", "bones"):
                try:
                    txt = str(f.c[k].Text or "").strip()
                except Exception:
                    continue
                t = typed.get(k)
                if t is None or t[0] != txt:
                    typed[k] = (txt, now)
                if not cfg.force and (t is None or t[0] != txt or now - t[1] < 1.0):
                    new[k] = settings[k]

        def on_change(old, new):
            """Settings changed: reset the decay warning when the times changed, redraw, and drop the arrow if off."""
            if (new["decay"], new["bones"]) != (old["decay"], old["bones"]):
                st["warned"] = False
            st["lbl_at"] = 0.0
            if not new["arrow"]:
                Kit.drop_arrow(st, ARROW_ID)

        cfg = Kit.Page(settings, page_table, save_settings, on_change, adjust=settle, final=True)

        def config_closed():
            """Settings page closed: let Kit.Page finish, and forget the typed-text memory."""
            cfg.closed()
            typed.clear()

        def on_corpse(*args):
            """Client event OnCorpseCreated: bring the corpse search forward.

            Only matters while the remembered corpse has not been seen yet; the search is pulled to just after
            the next permitted poke.
            """
            r = st["rec"]
            if r is None or r["serial"] or st["shutting"]:
                return
            soon = st["find_at"] + POKE_GAP
            st["seek_at"] = min(st["seek_at"], soon)
            st["look_at"] = min(st["look_at"], soon)

        def on_died(*args):
            """Script event: you died. Only sets a flag and asks for a Corpse tick (a game event, not input).

            The tick then records the death at once, before the client shows you as a ghost.
            """
            if st["shutting"]:
                return
            st["died"] = True
            HOST.poke("worldmap.corpse", False)

        def rebase(d):
            """Shift every stored time by d after the computer's clock was set back.

            d is negative. Without it waits would last as long as the jump, and the decay countdown must keep
            the real time left, so the saved death time moves too and is written again.
            """
            for k in ("body_at", "seek_until", "seek_at", "look_at", "item_at", "lbl_at", "note_until", "find_at",
                      "died_at"):
                st[k] = st[k] + d
            if st["gone_since"] is not None:
                st["gone_since"] += d
            p = st["ping"]
            if p is not None:
                st["ping"] = (p[0], p[1], p[2], p[3] + d)
            j = st["job"]
            if j is not None:
                for k in ("at", "until", "sent_at", "hold"):
                    j[k] += d
            r = st["rec"]
            if r is not None:
                r["died"] += d
                save_rec()

        def _start():
            """Module start: reset the per-run state, load the saved settings and corpse, build and dock the window.

            Runs on the client thread when the module is switched on.
            """
            st.update({"shutting": False, "docked": False, "queue": [], "job": None, "arrow": None, "refused": set(),
                       "ping": None, "was_dead": None, "seek_until": 0.0, "seek_at": 0.0,
                       "look_at": 0.0, "gone_since": None, "item_at": 0.0, "lbl_at": 0.0, "note": "",
                       "last_now": None, "atlas": False, "unnamed": False, "died": False, "died_at": 0.0,
                       "minimized": wnd.start_min()})
            load_settings()
            st["rec"] = load_rec()
            st["warned"] = False
            # Long decayed while the player was away: forget it.
            if st["rec"] is not None and remaining(time.time()) <= -DECAYED_GRACE:
                st["rec"] = None
                save_rec()
            # A corpse position without a serial means it is still being looked for around the player.
            if st["rec"] is not None and not st["rec"]["spot"]:
                st["seek_until"] = time.time() + FIND_SECS
            HOST.alert_kind(ALERT_DECAY, "Corpse about to decay", 0x1EA)
            build_window()
            wnd.dock(fit=True, min=(W, H))
            Kit.hook_once(st, "hooked", ("OnCorpseCreated", on_corpse), ("OnPlayerDeath", on_died))

        def _tick():
            """Client tick of the Corpse part: death detection, queued buttons, the job, the ping, the arrow and
            the window.

            Runs on the client thread, so nothing in it may wait. Returns early when the window is gone.
            """
            if win["g"] is None:
                return
            # A closed window (Kit.closed) ends the module.
            if Kit.closed(win):
                return
            now = time.time()
            last, st["last_now"] = st["last_now"], now
            # The clock went back more than two seconds: move every stored time with it.
            if last is not None and now < last - 2.0:
                rebase(now - last)
            # One read of the player per pass so that X and Y are read once, not again in each helper.
            me = HOST.me()
            while st["queue"]:
                action = st["queue"].pop(0)
                if not wnd.action(action):
                    ACTIONS[action](me, now)
            if me is None:
                return
            dead = bool(me.IsDead)
            was = st["was_dead"]
            st["was_dead"] = dead
            died = st["died"]
            st["died"] = False
            # The death event starts the record at once. When you are not yet shown as dead, died_at holds
            # the time, so the dead-body check below skips this same death when it sees it (within DIED_HOLD);
            # without the event that check still records the death.
            if died and not was:
                on_death(me, now)
                st["died_at"] = 0.0 if dead else now
            elif was is None:
                if dead and st["rec"] is None:
                    on_death(me, now, at_start=True)
            elif dead and not was:
                if not 0.0 <= now - st["died_at"] <= DIED_HOLD:
                    on_death(me, now)
                st["died_at"] = 0.0
            elif was and not dead and st["rec"] is not None:
                r = st["rec"]
                if r["spot"]:
                    say("you are alive. Your corpse is %s: click Get my things beside it."
                        % Kit.where_text(r["x"] - int(me.X), r["y"] - int(me.Y)), Kit.HUE_GOOD)
                st["lbl_at"] = 0.0
            # The body graphic and name are kept every two seconds while alive: a corpse carries its owner's body
            # graphic as its amount, and mine() uses it, with the name, to recognise the player's own corpse.
            if not dead and now >= st["body_at"]:
                st["body_at"] = now + 2.0
                st["body"] = int(me.Graphic)
                st["name"] = str(me.Name or "") or st["name"]
            if not st["name"]:
                st["name"] = str(me.Name or "")
            # The facet is only read when something needs it.
            mm = int(API.GetMap()) if st["rec"] is not None or st["arrow"] is not None else None
            if st["rec"] is not None:
                corpse_tick(me, now, mm)
            if st["job"] is not None:
                job_tick(me, now)
                send_move()
            if st["ping"] is not None:
                ping_tick(now)
            if st["rec"] is not None or st["arrow"] is not None:
                arrow_tick(me, mm)
            r = st["rec"]
            sig = (r["x"], r["y"], r["facet"]) if r is not None and r["spot"] else None
            # Publish the corpse spot to TazUO's World Map only when it changed.
            if sig != st["atlas"]:
                st["atlas"] = sig
                ATLAS.set("corpse", {} if sig is None else
                          {atlas_name("Your corpse"): (sig[0], sig[1], sig[2], "white")})
            refresh(me, now, mm)

        def _interval():
            """Tick spacing: 0.1 s while a job runs (items move one at a time), 0.25 s otherwise."""
            return 0.1 if st["job"] is not None else 0.25

        def _stop():
            """Module stop: end the job and ping, take down our own arrow, save the settings, close the cleanup."""
            st["shutting"] = True
            st["job"] = st["ping"] = None
            Kit.drop_arrow(st, ARROW_ID)
            save_settings()
            cleanup.close()

        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": config_closed,
                "interval": _interval}

    def _part_maps():
        """Build the Treasure Maps part and return its module hooks.

        Lists the treasure maps in the backpack (bags inside it too, and the bank box while it is open): each
        map's level, whether it is decoded and, for a decoded map, its dig spot with distance and direction.
        The tracking arrow points at the nearest spot on the player's facet or at the row clicked, and a
        button on each row sends a Go here ping through Map Pings. Display only (R2): nothing here digs,
        decodes or moves anything. Everything runs on the client tick.

        Where the spot comes from: the player double-clicks a decoded map once. The client's map window
        holds the server's pin; it is read from there when the pin arrives (nothing is sent to the server)
        and kept by the map's serial per character, so it is known after a restart too. TazUO's own journal
        estimate takes a 300 pixel map for granted, so the spot is worked out from the pin's pixel, the
        map's bounds and its real width. When the window cannot be read, the journal line and the map just
        double-clicked are used instead.

        Saved keys: TreasureHunter_settings (options), TreasureHunter_pos and TreasureHunter_min (window),
        TreasureHunter_maps (spots as serial,x,y,facet,level,done,time,approx joined by semicolons).
        """
        # The saved key names keep their old prefix so that existing saves still load.
        KEY = "treasure"
        TITLE = "Treasure Maps"
        SETTINGS_KEY = "TreasureHunter_settings"
        POS_KEY = "TreasureHunter_pos"
        MIN_KEY = "TreasureHunter_min"
        MAPS_KEY = "TreasureHunter_maps"
        MINI_W, MINI_H = 320, 46
        ROWS = 8
        ROW_H = 24
        ARROW_ID = 0x54524541
        # Item art of maps (the map graphics in the client's tile data).
        MAP_GRAPHICS = (0x14EB, 0x14EC)
        # Words in a map's name that tell its level, in level order (a treasure map is named like a
        # tattered, adeptly drawn treasure map).
        LEVELS = ("youthful", "plainly", "expertly", "adeptly", "cleverly", "deviously", "ingeniously")
        LEVEL_NAMES = ["Youthful"] + [v.capitalize() + " drawn" for v in LEVELS[1:]]
        PROP_FACETS = ["somewhere in " + n.lower() for n in Kit.FACETS]
        # Journal texts of the shard and client that mark a map being decoded, its pin shown, or a hunt
        # already completed.
        J_DECODED = "you successfully decode a treasure map"
        J_SHOWN = "the treasure is marked by the red pin"
        J_DONE = "this treasure hunt has already been completed"
        # TazUO prints this line itself with its own estimate of the spot.
        J_ESTIMATE = re.compile(r"believe this is somewhere near (\d+) and (\d+)")
        # The map width TazUO's estimate assumes.
        TAZ_SCALE = 300.0
        SCAN_EVERY = 1.0
        LOOK_FOR = 6.0
        LOOK_EVERY = 0.25
        USED_KEEP = 8.0
        # Seconds between saves of the spots, and only when something changed.
        SAVE_EVERY = 5.0
        # Spots remembered at most; the oldest seen are dropped first.
        MAX_MAPS = 60
        PING_TRY_FOR = 6.0
        # Seconds between tries of a Go here ping while Map Pings is pacing itself.
        PING_RETRY = 0.5
        LOOK_TIP = "Point the tracking arrow at this map's spot (again: back to the nearest map)"
        LOOK_TIP_ON = "Send the tracking arrow back to the nearest map's spot"
        LOOK_TIP_MAN = "Point the tracking arrow at this map's spot (again: take it down)"
        PING_TIP = "Send a Go here ping on this map's spot (needs World Map > Map Pings)"
        EMPTY_TEXT = "No treasure maps in your pack: put one in and double-click it once."
        DUG_TIP = "This treasure has been dug up"
        settings = {"auto": True, "undecoded": True, "done": False}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "next_look": 0.0, "dirty": False,
              "next_save": 0.0, "list_ver": 0, "me": (0, 0, -1), "hooked": False, "tm_at": 0.0, "tm_serial": 0,
              "hidden": 0, "in_pack": frozenset()}
        spots = {}
        # Map serial -> (name and properties text, what they say, time it is read again).
        parsed = {}
        TEXT_EVERY = 5.0
        # A one-item list so the nested functions can set it: when True, the next scan reads every map's text
        # again.
        TEXT_ALL = [False]
        # Serials whose properties were already asked of the server once.
        asked = set()
        # Map serial -> the map window object already read, so each opening is read only once.
        read_gumps = {}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        JR = {"rd": None}
        cleanup, queue, say = Kit.basics(st, TITLE)
        # Bank box look: when it was made and the maps found, so it is only read every few seconds.
        bank_st = {"at": 0.0, "items": []}

        def level_name(lvl):
            """Name of a map level (0 upwards), or a plain name when the level is unknown."""
            return LEVEL_NAMES[lvl] if 0 <= lvl < len(LEVEL_NAMES) else "Treasure map"

        def load_settings():
            """Load the options from their saved key."""
            Kit.kv_load(SETTINGS_KEY, ";", settings)

        def save_settings():
            """Save the options."""
            Kit.kv_save(SETTINGS_KEY, ";", settings, ("auto", "undecoded", "done"))

        def load_maps():
            """Load the saved dig spots of this character.

            Each entry is a semicolon-separated record of serial (hex), x, y, facet, level, done, time and an
            optional approximate flag. Broken entries and spots not seen for 60 days are skipped.
            """
            spots.clear()
            cut = time.time() - 60 * 86400
            for part in Kit.get_var(MAPS_KEY).split(";"):
                b = part.strip().split(",")
                if len(b) < 7:
                    continue
                try:
                    s = int(b[0], 16)
                    rec = {"x": int(b[1]), "y": int(b[2]), "f": int(b[3]), "lvl": int(b[4]),
                           "done": b[5] == "1", "t": int(b[6]), "approx": len(b) > 7 and b[7] == "1"}
                except ValueError:
                    continue
                if s <= 0 or rec["x"] <= 0 or rec["y"] <= 0 or rec["t"] < cut:
                    continue
                spots[s] = rec
            cap_spots()

        def cap_spots():
            """Keep at most MAX_MAPS spots by dropping the least recently seen."""
            if len(spots) > MAX_MAPS:
                old = sorted(spots, key=lambda s: spots[s]["t"])
                for s in old[:len(spots) - MAX_MAPS]:
                    del spots[s]

        def save_maps():
            """Save the dig spots in the format load_maps reads and clear the dirty flag."""
            st["dirty"] = False
            Kit.put_var(MAPS_KEY, ";".join("%X,%d,%d,%d,%d,%d,%d,%d" % (s, r["x"], r["y"], r["f"], r["lvl"],
                        1 if r["done"] else 0, r["t"], 1 if r.get("approx") else 0) for s, r in sorted(spots.items())))

        def parse(text):
            """Read a map's name and properties text: is it a treasure map, its level, whether it is decoded, the
            facet it names and whether it is completed.

            Returns a dict with keys tm, lvl, dec (None when not a treasure map), f and done. A treasure map
            whose name says tattered is not decoded yet.
            """
            low = text.lower()
            name = low.split("\n", 1)[0]
            info = {"tm": "treasure map" in low, "lvl": -1, "dec": None, "f": -1, "done": "completed by" in low}
            for lvl, word in enumerate(LEVELS):
                if word in name:
                    info["lvl"] = lvl
                    break
            if info["tm"]:
                info["dec"] = "tattered" not in name
            for f, t in enumerate(PROP_FACETS):
                if t in low:
                    info["f"] = f
                    break
            return info

        def info_of(serial, it, now=None):
            """What the client knows of map serial, cached by its text.

            it is the item object, used for its name when no properties have arrived. now is the scan's time:
            the cached reading is reused until TEXT_EVERY has passed; None reads it now. Never waits (client
            tick). When the properties are empty the server is asked for them once per serial and the read is
            repeated at the next scan.
            """
            hit = parsed.get(serial)
            # The upper bound also discards a stored time that lies far ahead, as after the clock was set back.
            if now is not None and hit is not None and now < hit[2] <= now + TEXT_EVERY:
                return hit[1]
            if now is None:
                now = time.time()
            text = str(API.ItemNameAndProps(serial, False) or "")
            again = now + TEXT_EVERY
            if not text.strip():
                again = 0.0
                text = str(it.Name or "")
                if serial not in asked:
                    asked.add(serial)
                    # The set is only a once-per-serial memory, so it is simply emptied when it grows large.
                    if len(asked) > 500:
                        asked.clear()
                    # Asks the server for the item's properties; the answer shows up in a later scan.
                    API.RequestOPLData([serial])
            if hit is not None and hit[0] == text:
                parsed[serial] = (text, hit[1], again)
                return hit[1]
            info = parse(text)
            if len(parsed) > 300:
                parsed.clear()
            parsed[serial] = (text, info, again)
            return info

        def solve(est, end, p, size):
            """Work out the dig spot and the map's tiles per pixel on one axis of an opened map.

            est is TazUO's estimate of the spot, made as start + p * (end - start) / 300 with the map's start no
            longer kept once the pin has arrived. end is the far edge of the map, p the pin's pixel on this axis
            and size the map's width (or height) in pixels. On a 300 pixel map the estimate is exact; on any
            other the start is solved back out of it and the spot taken at the middle of the pin's cell.
            Returns (spot, scale): spot is None when it cannot be told that way (a pin near pixel 300 of a bigger
            map) and scale is None when it is not known well enough to lend to the other axis.
            """
            # No pin pixel or no size: TazUO's own estimate has to do.
            if None in (end, p, size):
                return est, None
            p, size = float(p), float(size)
            if size <= 0 or p < 0 or p > size:
                return est, None
            # k is how much of the estimate's error survives in the formula; near zero the start cannot be
            # recovered.
            k = 1.0 - p / TAZ_SCALE
            start = None
            if abs(k) >= 0.001:
                base = p * end / TAZ_SCALE
                # The estimate is an integer, so the true value lies between est and est + 1: take the middle.
                lo, hi = (est - base) / k, (est + 1 - base) / k
                start = int(math.floor((lo + hi) / 2.0))
                if not 0 < end - start <= 8192:
                    start = None
            # A map is drawn at the same scale both ways, so a well known scale is lent to the other axis.
            scale = float(end - start) / size if start is not None and abs(k) >= 0.25 else None
            if abs(size - TAZ_SCALE) < 0.5:
                # TazUO's own figure is exact on a 300 pixel map.
                return est, scale
            # The start is too uncertain for the spot.
            if start is None or abs(1.0 - (p + 0.5) / size) / abs(k) > 2.0:
                return None, scale
            return int(start + (p + 0.5) * (end - start) / size), scale

        def axis(est, end, p, size, scale=None):
            """Dig spot coordinate on one axis as (coordinate, approximate).

            scale is the other axis's tiles per pixel, used when this axis cannot be solved. With neither, TazUO's
            own estimate is returned and marked approximate.
            """
            spot = solve(est, end, p, size)[0]
            if spot is not None:
                return spot, False
            if scale and None not in (end, p, size):
                return int(end - (float(size) - float(p) - 0.5) * scale), False
            return est, True

        def num(obj, name):
            """An int member of a client object (public or not), or None."""
            # Typing._get reads a field or property of a client object by name, private ones too.
            v = Typing._get(obj, name)
            if v is None:
                return None
            try:
                return int(v)
            except Exception:
                return None

        def look_gumps():
            """Read every open map window whose pin has arrived, once per opening.

            Returns None when the client's windows cannot be read, else how many windows were read.
            """
            Typing._find()
            uim = Typing.uim
            if uim is None:
                return None
            # The client's list of open windows.
            gumps = Typing._get(None, "Gumps", uim)
            if gumps is None:
                return None
            n = 0
            try:
                for g in gumps:
                    # Only map windows are of interest.
                    if str(g.GetType().Name) != "MapGump":
                        continue
                    r = read_gump(g)
                    if r is None:
                        # A map window this build lays out differently: give up so the journal fallback can take over.
                        return None
                    n += r
            except Exception:
                return None
            return n

        def read_gump(g):
            """Read one map window.

            Returns 1 when it was read now, 0 when it was read before, has no pin yet or is not a map of the
            player's, and None when its fields cannot be read.
            """
            serial = num(g, "LocalSerial")
            if not serial:
                return 0
            if Typing._get(g, "IsDisposed", default=False):
                return 0
            # This opening was read already.
            if read_gumps.get(serial) is g:
                return 0
            found = Typing._get(g, "foundMapLoc")
            if found is None:
                return None
            # The pin has not arrived yet.
            if not found:
                return 0
            est_x, est_y = num(g, "mapX"), num(g, "mapY")
            if est_x is None or est_y is None:
                return None
            end_x, end_y, mf = num(g, "mapEndX"), num(g, "mapEndY"), num(g, "mapFacet")
            hit = Typing._get(g, "_hit")
            size_w = num(hit, "Width") if hit is not None else None
            size_h = num(hit, "Height") if hit is not None else None
            px = py = None
            # The window's pin list: the pin's pixel is worked back out of where the client drew it.
            pins = Typing._get(g, "_container")
            try:
                if pins is not None and int(pins.Count) > 0:
                    pin = pins[0]
                    pw, ph = num(pin, "Width"), num(pin, "Height")
                    x0, y0 = num(pin, "X"), num(pin, "Y")
                    if None not in (pw, ph, x0, y0):
                        # The client placed the pin at (x + width + 5, y + height), so this undoes that.
                        px, py = x0 - pw - 5, y0 - ph
            except Exception:
                px = py = None
            # Bounded memory of windows already read.
            if len(read_gumps) > 50:
                read_gumps.clear()
            read_gumps[serial] = g
            sx = solve(est_x, end_x, px, size_w)[1]
            sy = solve(est_y, end_y, py, size_h)[1]
            x, ax = axis(est_x, end_x, px, size_w, sy)
            y, ay = axis(est_y, end_y, py, size_h, sx)
            if x is None or y is None or x <= 0 or y <= 0:
                return 0
            # The facet of the window itself when it has one (above zero), else record works it out.
            record(serial, x, y, mf if mf is not None and mf > 0 else -1, ax or ay)
            return 1

        def record(serial, x, y, mf, approx=False):
            """Store a map's dig spot, read just now.

            The facet comes from the map window when it has one, else from the map's properties, else the facet
            the player is on. Only a treasure map's spot is kept: its name says so, it was recorded before or
            the shard has just said it showed one (a plain map with a plotted course has pins too). Says the
            spot in the journal line when it is new. Returns True when kept.
            """
            it = API.FindItem(serial)
            info = info_of(serial, it) if it is not None else {}
            now = time.time()
            # The map just double-clicked, or the only one opening right now, counts as a treasure map when the
            # shard has just said so.
            hinted = 0 <= now - st["tm_at"] <= LOOK_FOR and (st["tm_serial"] == serial
                or (not st["tm_serial"] and now - st["tm_at"] <= 1.5))
            if not (info.get("tm") or serial in spots or hinted):
                return False
            f = mf if mf >= 0 else info.get("f", -1)
            if f < 0:
                f = int(API.GetMap())
            old = spots.get(serial)
            lvl = info.get("lvl", -1)
            if lvl < 0 and old is not None:
                lvl = old["lvl"]
            rec = {"x": int(x), "y": int(y), "f": int(f), "lvl": lvl,
                   "done": bool(info.get("done") or (old is not None and old["done"])),
                   "t": int(time.time()), "approx": bool(approx)}
            same = (old is not None and (old["x"], old["y"], old["f"]) == (rec["x"], rec["y"], rec["f"]))
            spots[serial] = rec
            cap_spots()
            st["dirty"] = True
            # List the map at the next client tick.
            st["next_scan"] = 0.0
            if not same:
                # A new spot: the arrow may come back.
                st["arrow_off"] = False
                mx, my, mf2 = st["me"]
                where = (", " + Kit.where_text(rec["x"] - mx, rec["y"] - my, "here")) if mf2 == rec["f"] and mx > 0 \
                    else ""
                say("%s map%s: dig at %s%d, %d in %s%s." % (
                    level_name(lvl).lower(), (" (level %d)" % lvl) if lvl >= 0 else "",
                    "about " if rec["approx"] else "", rec["x"], rec["y"], Kit.facet_name(rec["f"]), where),
                    Kit.HUE_GOOD)
            return True

        def arm_look(now):
            """Start watching for an opened map window for LOOK_FOR seconds, beginning now."""
            st["look_until"] = now + LOOK_FOR
            st["next_look"] = 0.0

        def on_used(*args):
            """Event ObjectUsed (a double-click the client sends): only noted here.

            The serial goes into a short queue and handle_used looks at it on the tick. Ignored when the module
            is off.
            """
            if not st["active"]:
                return
            for a in args:
                try:
                    s = int(a)
                except Exception:
                    continue
                if s > 0 and len(st["used"]) < 20:
                    st["used"].append(s)
                return

        def hook_events():
            """Hook the ObjectUsed event once per run (Kit.hook_once); on_used checks active."""
            Kit.hook_once(st, "hooked", ("ObjectUsed", on_used))

        def handle_used(now):
            """Look at the double-clicked items noted by on_used; a map's serial is remembered with its time and a
            look for its window is armed.
            """
            used, st["used"] = st["used"], []
            for s in used:
                it = API.FindItem(s)
                if it is not None and int(it.Graphic) in MAP_GRAPHICS:
                    st["last_map"] = (s, now)
                    arm_look(now)

        def handle_journal(now):
            """Read the new journal lines for the three map texts: TazUO's estimate, the shard showing or decoding
            a map, and the shard saying a hunt is completed.
            """
            rd = JR["rd"]
            if rd is None:
                return
            own = TITLE.lower() + ":"
            for ln in rd.new():
                low = ln.low
                # The three texts first: most lines are none of them.
                if "somewhere near" in low:
                    kind = 1
                elif J_SHOWN in low or J_DECODED in low:
                    kind = 2
                elif J_DONE in low:
                    kind = 3
                else:
                    continue
                # Our own say() lines come back through the journal: skip them.
                if low.startswith(own):
                    continue
                name = (ln.name or "").strip().lower()
                # Only lines from the system or the client, not a player saying the text.
                if name and name != "system":
                    continue
                if kind == 1:
                    m = J_ESTIMATE.search(low)
                    if m:
                        st["est"] = (int(m.group(1)), int(m.group(2)), now)
                        arm_look(now)
                elif kind == 2:
                    # The map window coming is a treasure map's: the one just double-clicked when known, else only one
                    # that opens right now.
                    s, t = st["last_map"]
                    st["tm_at"] = now
                    st["tm_serial"] = s if s and 0 <= now - t <= USED_KEEP else 0
                    # A decoded map's name changes, so every map's text is read again.
                    TEXT_ALL[0] = True
                    arm_look(now)
                else:
                    s, t = st["last_map"]
                    # Its properties say completed now.
                    TEXT_ALL[0] = True
                    if s and 0 <= now - t <= USED_KEEP and s in spots and not spots[s]["done"]:
                        spots[s]["done"] = True
                        st["dirty"] = True
                        st["next_scan"] = 0.0

        def look_step(now):
            """One step of the search for an opened map window (client tick).

            While a look is active it reads the windows every LOOK_EVERY seconds. When the look ends it falls
            back to TazUO's journal estimate if one is waiting, and drops the windows held.
            """
            # Guard against a clock set back: a look that ends far in the future is cut to the normal length.
            if not (now < st["look_until"] <= now + LOOK_FOR + 1.0):
                if st["look_until"] > now + LOOK_FOR + 1.0:
                    st["look_until"] = now + LOOK_FOR
                    return
                if st["est"] is not None:
                    fallback()
                # Do not hold on to closed map windows.
                if read_gumps:
                    read_gumps.clear()
                return
            # Not time for the next look yet.
            if now < st["next_look"] <= now + LOOK_EVERY:
                return
            st["next_look"] = now + LOOK_EVERY
            n = look_gumps()
            if n is None:
                # The client's windows cannot be read: use TazUO's journal line as soon as the map that was
                # double-clicked is known.
                est, used = st["est"], st["last_map"]
                if est is not None and used[0] and -2.0 <= est[2] - used[1] <= USED_KEEP:
                    fallback()
            elif n > 0:
                # The estimate belonged to this window.
                st["est"] = None
                # A map was read: stop looking after a second.
                st["look_until"] = min(st["look_until"], now + 1.0)

        def fallback():
            """No map window could be read: use TazUO's estimate line and the map just double-clicked.

            The estimate assumes a 300 pixel map, which is right for the shard's treasure maps. Only used when
            the two happened within a few seconds of each other.
            """
            x, y, te = st["est"]
            st["est"] = None
            s, tu = st["last_map"]
            if not s or not (-2.0 <= te - tu <= USED_KEEP) or x <= 0 or y <= 0:
                return
            st["last_map"] = (0, 0.0)
            record(s, x, y, -1)

        def scan(now):
            """Scan the maps in the backpack and the open bank box and rebuild the list (client tick, once a
            second).

            Sets st["list"] (sorted nearest first), the set of serials seen and a version that changes only when
            the visible content does. Maps without a known spot are listed by whether they are decoded;
            completed and undecoded maps are hidden or shown by the options and counted.
            """
            try:
                # The player's place and facet are read once for the whole scan.
                me = API.Player
                mx, my = int(me.X), int(me.Y)
                fac = int(API.GetMap())
            except Exception:
                return
            st["me"] = (mx, my, fac)
            # No backpack known now: the list stays as it was and Forget waits until it is.
            if not int(API.Backpack or 0):
                st["in_pack"] = None
                return
            # Every depth of the backpack comes from the shared pass list, then the bank box when it is open.
            found = [it for it in HOST.pack_items(True, 0.5) if int(it.Graphic) in MAP_GRAPHICS]
            bank = bank_maps(now)
            banked = set([int(it.Serial) for it in bank])
            found.extend(bank)
            out, seen = [], set()
            hidden = 0
            day = int(time.time())
            # None means every map's text is read now; otherwise the cache decides.
            tnow = None if TEXT_ALL[0] else time.time()
            TEXT_ALL[0] = False
            for it in found:
                s = int(it.Serial)
                if s in seen:
                    continue
                seen.add(s)
                # Listed at most 100 maps.
                if len(out) >= 100:
                    continue
                info = info_of(s, it, tnow)
                rec = spots.get(s)
                # A plain map, not a treasure map and nothing remembered for it.
                if not info["tm"] and rec is None:
                    continue
                lvl = info["lvl"] if info["lvl"] >= 0 else (rec["lvl"] if rec else -1)
                done = bool(info["done"] or (rec is not None and rec["done"]))
                if rec is not None:
                    # The map's own word on its facet.
                    if info["f"] >= 0 and rec["f"] != info["f"]:
                        rec["f"] = info["f"]
                        st["dirty"] = True
                    if lvl != rec["lvl"] or done != rec["done"]:
                        rec["lvl"], rec["done"] = lvl, done
                        st["dirty"] = True
                    # Seen in your pack: kept from aging out of the saved spots, written at most once a day.
                    if day - rec["t"] > 86400:
                        rec["t"] = day
                        st["dirty"] = True
                dec = True if rec is not None else info["dec"]
                e = {"serial": s, "lvl": lvl, "dec": dec, "done": done, "x": None, "y": None,
                     # Group orders the list: 0 spot on this facet, 1 spot on another facet, 2 decoded without a spot,
                     # 3 not decoded, 4 dug up.
                     "f": -1, "dist": None, "group": 3, "bank": s in banked}
                if rec is not None:
                    e["x"], e["y"], e["f"] = rec["x"], rec["y"], rec["f"]
                    e["approx"] = rec.get("approx", False)
                    if e["f"] == fac:
                        e["dist"] = max(abs(rec["x"] - mx), abs(rec["y"] - my))
                        e["dir"] = Kit.compass(rec["x"] - mx, rec["y"] - my)
                        e["group"] = 0
                    else:
                        e["group"] = 1
                elif dec:
                    e["group"] = 2
                if done:
                    e["group"] = 4
                    if not settings["done"]:
                        hidden += 1
                        continue
                elif not dec and not settings["undecoded"]:
                    hidden += 1
                    continue
                e["where"], e["hue"], e["tip"] = where_of(e, fac)
                # Clearly marked as lying in the bank.
                if e["bank"]:
                    e["where"] = "in the bank: " + e["where"]
                out.append(e)
            out.sort(key=sort_key)
            st["list"] = out
            # Every map in the pack, listed or not: Forget keeps the ones in it.
            st["in_pack"] = seen
            if st["pin"] and st["pin"] not in seen:
                # The pinned map left your pack.
                st["pin"] = 0
            # The signature covers only what is drawn, so a step that changes nothing visible does not redraw.
            sig = (tuple((e["serial"], e["lvl"], e["dec"], e["done"], e["where"]) for e in out) + (hidden,))
            st["hidden"] = hidden
            if sig != st["list_sig"]:
                st["list_sig"] = sig
                st["list_ver"] += 1

        def bank_maps(now):
            """The treasure maps in the bank box while its window is open; an empty list otherwise.

            Looked at most every 5 seconds and reads at most 2000 items.
            """
            if now - bank_st["at"] < 5.0 and now >= bank_st["at"]:
                return bank_st["items"]
            b = int(API.Bank or 0)
            bank_st["at"] = now
            bank_st["items"] = []
            if b and bank_open(b):
                bank_st["items"] = [it for it in list(API.ItemsInContainer(b, True) or [])[:2000]
                                    if int(it.Graphic) in MAP_GRAPHICS]
            return bank_st["items"]

        def bank_open(bank):
            """True when one of the client's own container windows is showing the bank box."""
            with Kit.quiet:
                for g in Tz.windows(("ContainerGump", "GridContainer")):
                    if int(g.LocalSerial) == bank:
                        return True
            return False

        def dig_tiles(keep):
            """Highlight the spot of each decoded map not yet dug up in the game world, so the player can walk to
            it and dig on the exact tile.

            Display only (R2). keep is the list entries to show; only the changes are sent and a spot gone from
            it loses its highlight.
            """
            want = set((int(e["x"]), int(e["y"]), int(e["f"])) for e in keep)
            for t in st["dig_tiles"] - want:
                API.RemoveMarkedTile(t[0], t[1], t[2])
            for t in want - st["dig_tiles"]:
                # Gold tile highlight.
                API.MarkTile(t[0], t[1], 0x0035, t[2])
            st["dig_tiles"] = want

        def sort_key(e):
            """Sort key of a list entry: group, then distance, level and serial."""
            return (e["group"], e["dist"] if e["dist"] is not None else 0, e["lvl"], e["serial"])

        def atlas_publish():
            """Publish the dig spots of the maps in the pack, not dug up yet, as markers on TazUO's World Map.

            Only made again when the spots change, not with every step's where text. Also refreshes the tile
            highlights.
            """
            keep = [e for e in st["list"] if not (e["x"] is None or e["done"] or e["f"] < 0)]
            sig = tuple((e["serial"], e["x"], e["y"], e["f"], e["lvl"]) for e in keep)
            if sig == st["atlas_sig"]:
                return
            st["atlas_sig"] = sig
            dig_tiles(keep)
            ATLAS.set("maps", {atlas_name(("Dig L%d #%04X" % (e["lvl"], e["serial"] & 0xFFFF)) if e["lvl"] >= 0
                                          else ("Dig #%04X" % (e["serial"] & 0xFFFF))):
                               (int(e["x"]), int(e["y"]), int(e["f"]), "yellow") for e in keep})

        def where_of(e, fac):
            """Where text, hue and row tooltip of one list entry; fac is the facet the player is on.

            The coordinates are shown through xy (veiled in streamer mode); an approximate spot is prefixed
            with "about".
            """
            if e["x"] is not None:
                spot = ("about " if e.get("approx") else "") + xy(e["x"], e["y"], "(%d, %d)")
                if e["done"]:
                    return "dug up  " + spot, Kit.HUE_INFO, DUG_TIP
                if e["f"] == fac:
                    d = e["dist"]
                    if d == 0:
                        return "here  " + spot, Kit.HUE_GOOD, LOOK_TIP
                    return ("%s %s  %s" % (Kit.count(d, "tile"), e["dir"], spot), Kit.HUE_TEXT, LOOK_TIP)
                return ("in %s  %s" % (Kit.facet_name(e["f"]), spot), Kit.HUE_INFO,
                        "This map's spot is in %s; you are in %s" % (Kit.facet_name(e["f"]), Kit.facet_name(fac)))
            if e["done"]:
                return "dug up", Kit.HUE_INFO, DUG_TIP
            if e["dec"]:
                return "open the map once to read its spot", Kit.HUE_INFO, "Double-click the map once to read it"
            if e["dec"] is None:
                return "open the map to read it", Kit.HUE_INFO, "Double-click the map to read it"
            return "not decoded yet", Kit.HUE_INFO, "Double-click the map to decode it (Cartography)"

        def entry(serial):
            """The list entry for a map serial, or None."""
            return next((e for e in st["list"] if e["serial"] == serial), None)

        def arrow_target():
            """The spot the tracking arrow should show as (x, y, serial), or None.

            The row picked wins when its spot is on the player's facet and not dug up; else the nearest spot when
            the nearest option is on.
            """
            if st["arrow_off"]:
                return None
            fac = st["me"][2]
            if st["pin"]:
                e = entry(st["pin"])
                if e is not None and e["x"] is not None and e["f"] == fac and not e["done"]:
                    return (e["x"], e["y"], e["serial"])
            if settings["auto"]:
                # The list is sorted nearest first, so the first spot on this facet is the nearest.
                for e in st["list"]:
                    if e["group"] == 0:
                        return (e["x"], e["y"], e["serial"])
            return None

        def update_arrow(force_off=False, force=False):
            """Show, move or take down our own tracking arrow.

            force_off takes it down whatever the options say. force shows it again even when it should already
            be up, in case the player closed it.
            """
            want = None if force_off else arrow_target()
            cur = st["arrow"]
            # Same place as before: no call to the client.
            if not force and (want[:2] if want else None) == (cur[:2] if cur else None):
                st["arrow"] = want
                return
            if want is None:
                # Negative coordinates take the arrow down.
                API.TrackingArrow(-1, -1, ARROW_ID)
            else:
                API.TrackingArrow(want[0], want[1], ARROW_ID)
                st["arrow_at"] = time.time()
            st["arrow"] = want

        def arrow_closed(now):
            """Notice that the player closed our arrow with a right-click (TazUO allows it).

            That counts as Arrow off, so the row mark goes and only a press shows it again, never the one second
            scan.
            """
            if st["arrow"] is None:
                return
            age = now - st.get("arrow_at", 0.0)
            # The clock went back.
            if age < 0:
                st["arrow_at"] = now
                return
            # Give a new arrow a moment to appear before it is looked for.
            if age < 1.5 or arrow_open():
                return
            st["arrow"], st["arrow_off"], st["pin"] = None, True, 0

        def build_window():
            """Build the window: toolbar, column heads and the pooled rows (client tick).

            The rows are created once and refilled by refresh; their number follows the window's height. Folded
            into the Action Bar there is no body.
            """
            z = told(wnd, st, 560, list_h(1, ROW_H))
            w, h = z if z else (560, list_h(ROWS, ROW_H))
            n = wnd.rows(ROW_H, list_h(0, ROW_H), ROWS) if z else ROWS
            g, store, c = wnd.begin(w, h)
            rows = []
            if not st["minimized"]:
                wnd.frame(g)
                M = Kit.MARGIN
                IW = w - 2 * M
                # The toolbar: what is in the pack, Nearest, Arrow off and the pager.
                yt = M + 30 + Kit.GAP
                Kit.add_section(g, M, yt, IW, 36)
                right = M + IW - 8
                Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 22, yt + 8, None,
                               "Next page", on_click=queue(("page", 1)))
                Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 46, yt + 8, None,
                               "Previous page", on_click=queue(("page", -1)))
                xpg = right - 52 - Kit.text_w("9/9")
                c["pg"] = Kit.add_label(g, "", xpg, yt + 10, Kit.HUE_INFO)
                x_off = xpg - 12 - (35 + Kit.text_w("Arrow off"))
                Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, x_off, yt + 7, "Arrow off",
                               "Take the tracking arrow down (a row click or Nearest brings it back)",
                               on_click=queue("arrow_off"))
                x_near = x_off - 12 - (35 + Kit.text_w("Nearest"))
                Kit.art_button(g, store, "nearest", Kit.ART_PLAY, x_near, yt + 7, "Nearest",
                               "Point the tracking arrow at the nearest dig spot on your facet",
                               on_click=queue("nearest"))
                c["status"] = Kit.add_label(g, "", M + 12, yt + 10, Kit.HUE_INFO)
                c["status_w"] = x_near - 8 - (M + 12)
                # The list: column heads, then the pooled rows.
                yl = yt + 36 + Kit.GAP
                Kit.add_section(g, M, yl, IW, h - yl - M)
                x_lvl = M + 12
                x_name = x_lvl + max(34, Kit.text_w("Level")) + 8
                x_where = x_name + 150 + 8
                x_ping = M + IW - 12 - 22
                Kit.add_label(g, "Level", x_lvl, yl + 6, Kit.HUE_TITLE)
                Kit.add_label(g, "Map", x_name, yl + 6, Kit.HUE_TITLE)
                Kit.add_label(g, "Dig spot", x_where, yl + 6, Kit.HUE_TITLE)
                c["where_w"] = x_ping - 8 - x_where
                # The empty-list line is drawn on the first row.
                c["empty_w"] = x_ping - 8 - x_lvl
                for k in range(n):
                    ry = yl + 30 + k * ROW_H
                    r = {"val": None, "prev": None, "changed": 0.0, "sig": None, "tip": None, "pvis": True,
                         "lvl": Kit.add_label(g, "", x_lvl, ry + 3, Kit.HUE_TITLE),
                         "name": Kit.add_label(g, "", x_name, ry + 3, Kit.HUE_TEXT),
                         "where": Kit.add_label(g, "", x_where, ry + 3, Kit.HUE_INFO)}
                    r["catch"] = Kit.catcher(g, M + 6, ry, x_ping - 4 - (M + 6), ROW_H,
                                             Kit.row_clicker(r, queue, "row", follow=False), LOOK_TIP)
                    r["ping"] = Kit.art_button(g, store, "ping%d" % k, Kit.ART_PLAY, x_ping, ry + 1, None, PING_TIP,
                                               on_click=Kit.row_clicker(r, queue, "ping", follow=False))
                    rows.append(r)
            wnd.end(g, {"rows": rows})
            st["drawn"] = None
            refresh()

        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (240, 180), (MINI_W, MINI_H), 0x14EB,
                         cleanup, lock=True, clear={"rows": []}, docked_min=True)

        def show(ctl, r, key, on):
            """Show or hide a control, only when its state differs from the last one set."""
            if r[key] != on:
                r[key] = on
                Kit.set(ctl, "IsVisible", on)

        def refresh():
            """Draw what changed (client tick).

            Folded into the bar: nothing; minimized: the status line only; open: the rows of this page. Skipped
            entirely when the signature of the list, page, arrow and pick did not change.
            """
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return
            arrow = st["arrow"][2] if st["arrow"] else 0
            sig = (st["list_ver"], st["page"], arrow, st["pin"], st["minimized"])
            # Nothing changed since the last draw.
            if sig == st["drawn"]:
                return
            st["drawn"] = sig
            c = win["c"]
            lst = st["list"]
            near = next((e for e in lst if e["group"] == 0), None)
            n = len(lst)
            maps = Kit.count(n, "map")
            # The nearest spot on this facet gives the status text: here, or the tiles and direction.
            if near is not None:
                d = near["dist"]
                part = ("here" if d == 0 else "%s %s" % (Kit.count(d, "tile"), near["dir"]))
                status = "%s, nearest %s" % (maps, part)
                mini = "%s, %s" % (maps, part)
            elif n:
                status = mini = "%s, no spot on this facet" % maps
            elif st["hidden"]:
                status = "No maps listed (%d hidden on the settings page)" % st["hidden"]
                mini = "%d hidden" % st["hidden"]
            else:
                status = "No treasure maps in your pack"
                mini = "no maps"
            if st["minimized"]:
                if c.get("status") is not None:
                    Kit.set_text(c["status"], Kit.fit("%s: %s" % (TITLE, mini), MINI_W - 90))
                return
            rows = win["rows"]
            per = max(1, len(rows))
            pages = max(1, (n + per - 1) // per)
            # The list shrank under the page shown: clamp the page and mark it drawn.
            if not 0 <= st["page"] < pages:
                st["page"] = max(0, min(pages - 1, st["page"]))
                st["drawn"] = sig[:1] + (st["page"],) + sig[2:]
            Kit.set_text(c["status"], Kit.fit(status, c.get("status_w", 200)))
            Kit.set_text(c["pg"], ("%d/%d" % (st["page"] + 1, pages)) if pages > 1 else "")
            first = st["page"] * per
            where_w = c.get("where_w", 200)
            now = time.time()
            for k, r in enumerate(rows):
                i = first + k
                if i >= n:
                    Kit.row_set(r, None, now)
                    # An empty list says so on its first row.
                    if k == 0 and n == 0:
                        es = ("empty", EMPTY_TEXT if not st["hidden"] else (status + "."))
                    else:
                        es = ("empty", "")
                    if r["sig"] != es:
                        r["sig"] = es
                        Kit.set_text(r["lvl"], Kit.fit(es[1], c.get("empty_w", 400)), Kit.HUE_INFO)
                        Kit.set_text(r["name"], "")
                        Kit.set_text(r["where"], "")
                    show(r["ping"], r, "pvis", False)
                    continue
                e = lst[i]
                Kit.row_set(r, (e["serial"],), now)
                on = arrow == e["serial"]
                rsig = (e["serial"], e["lvl"], e["dec"], e["done"], e["where"], on,
                        st["pin"] == e["serial"], settings["auto"])
                if rsig != r["sig"]:
                    r["sig"] = rsig
                    Kit.set_text(r["lvl"], ("L%d" % e["lvl"]) if e["lvl"] >= 0 else "?",
                                 Kit.HUE_TITLE if not e["done"] else Kit.HUE_INFO)
                    Kit.set_text(r["name"], Kit.fit(level_name(e["lvl"]), 150),
                                 Kit.HUE_TEXT if e["dec"] and not e["done"] else Kit.HUE_INFO)
                    Kit.set_text(r["where"], Kit.fit(("> " if on else "") + e["where"], where_w),
                                 Kit.HUE_TITLE if on else e["hue"])
                    tip = e["tip"]
                    # The tooltip tells what the second click does, which depends on the options.
                    if tip == LOOK_TIP:
                        pinned = st["pin"] == e["serial"]
                        if settings["auto"]:
                            tip = LOOK_TIP_ON if pinned else LOOK_TIP
                        else:
                            tip = "Take the tracking arrow down" if pinned else LOOK_TIP_MAN
                    if tip != r["tip"]:
                        r["tip"] = tip
                        Kit.with_tip(r["catch"], tip)
                show(r["ping"], r, "pvis", e["x"] is not None and not e["done"])

        def do_row(serial):
            """A click on a row: show the arrow on that map's spot, or take it back to the nearest.

            Maps with no spot or already dug up only say why. A map on another facet only says where it is.
            """
            e = entry(serial)
            if e is None:
                return
            if e["x"] is None or e["done"]:
                say(journal_case(e["tip"]) + ".")
                return
            if e["f"] != st["me"][2]:
                say("that map's spot is in %s; you are in %s." % (Kit.facet_name(e["f"]), Kit.facet_name(st["me"][2])))
                return
            st["arrow_off"] = False
            # Clicking the pinned row again: back to the nearest map, or, with that option off, down.
            if st["pin"] == serial:
                st["pin"] = 0
                if settings["auto"]:
                    say("tracking arrow back on the nearest map.")
                else:
                    st["arrow_off"] = True
                    say("tracking arrow down.")
            else:
                st["pin"] = serial
                say("tracking arrow on the %s map's spot (%d, %d)." % (level_name(e["lvl"]).lower(), e["x"], e["y"]))
            # Shown again even if the player closed it.
            update_arrow(force=True)

        def do_ping(serial, now):
            """Button on a row: arm a Go here ping on the map's spot, retried until Map Pings accepts it.

            Needs Map Pings (World Map) to be on.
            """
            e = entry(serial)
            if e is None or e["x"] is None:
                return
            if HOST.services.get("pings.send") is None:
                say("World Map > Map Pings is off; turn it on to send map pings.")
                return
            st["ping"] = [e["x"], e["y"], e["f"], now + PING_TRY_FOR, 0.0]

        def ping_step(now):
            """Try the armed ping, at most every PING_RETRY seconds and for PING_TRY_FOR seconds in all."""
            p = st["ping"]
            # Not time for the next try yet (the upper bound guards a clock set back).
            if p is None or (now < p[4] <= now + PING_RETRY):
                return
            fn = HOST.services.get("pings.send")
            if fn is None:
                st["ping"] = None
                say("World Map > Map Pings is off; turn it on to send map pings.")
                return
            try:
                ok = bool(fn(p[0], p[1], m=p[2], kind="go"))
            except Exception:
                # Failed outright: not retried.
                ok = True
            if ok:
                st["ping"] = None
            elif not (now < p[3] <= now + PING_TRY_FOR):
                st["ping"] = None
                say("Map Pings didn't take the ping (too soon after the last one); try again.")
            else:
                p[4] = now + PING_RETRY

        def forget_others():
            """Forget the spots of maps that are not in the backpack.

            Waits until the backpack has been seen at least once, so nothing is lost by mistake.
            """
            here = st["in_pack"]
            if here is None:
                say("your backpack isn't known yet; nothing was forgotten.")
                return
            # Bank maps count as present: they are in the seen set.
            gone = [s for s in spots if s not in here]
            for s in gone:
                del spots[s]
            st["dirty"] = True
            say("forgot %s of maps not in your pack." % Kit.count(len(gone), "spot"))

        def draw_spots(f, x, y):
            """Custom row of the settings page: how many spots are remembered and the Forget lost maps button."""
            Kit.add_label(f.g, "%s remembered" % Kit.count(len(spots), "spot"), x + 12, y + 4, Kit.HUE_INFO)
            Kit.art_button(f.g, f.store, "forget", Kit.ART_CLOSE, x + f.w - 12 - (35 + Kit.text_w("Forget lost maps")),
                           y, "Forget lost maps", "Forget the spots of maps not in your backpack",
                           on_click=queue("forget"))

        def act_page(a, now):
            """Page buttons: move the page by the step in the action."""
            st["page"] = max(0, st["page"] + a[1])

        def act_nearest(a, now):
            """Nearest button: point the arrow at the nearest spot, or pin it when the nearest option is off."""
            st["arrow_off"] = False
            if settings["auto"]:
                st["pin"] = 0
            else:
                near = next((e for e in st["list"] if e["group"] == 0), None)
                st["pin"] = near["serial"] if near is not None else 0
            update_arrow(force=True)
            if st["arrow"] is None:
                say("no decoded map with a spot on this facet.")

        def act_arrow_off(a, now):
            """Arrow off button: take the arrow down until a row click or Nearest brings it back."""
            st["pin"], st["arrow_off"] = 0, True
            update_arrow()

        def act_forget(a, now):
            """Forget lost maps button."""
            forget_others()
            HOST.refresh_settings(KEY)

        # Queued actions by name; queue entries are tuples with arguments or plain names.
        ACTIONS = {"page": act_page, "row": lambda a, now: do_row(a[1]), "ping": lambda a, now: do_ping(a[1], now),
                   "nearest": act_nearest, "arrow_off": act_arrow_off, "forget": act_forget}
        MAPS_PAGE = (("WINDOW  (open a decoded map once to read it)", (
                    ("check", "auto", "Point the tracking arrow at the nearest map's spot",
                     "With no map picked, the arrow points at the nearest spot on your facet"),
                    ("check", "undecoded", "List maps not decoded yet", "Maps still to decode (Cartography)"),
                    ("check", "done", "List maps already dug up", "Maps whose treasure is dug up"))),
                ("SAVED SPOTS", (("custom", 24, draw_spots),), {"sh": 64}), atlas_page("maps"))

        def page_table(w):
            """The settings page table of the part (the same for any width)."""
            return MAPS_PAGE

        def on_change(old, new):
            """Settings changed: rescan at the next tick and redraw."""
            st["next_scan"] = 0.0
            st["drawn"] = None

        cfg = Kit.Page(settings, page_table, save_settings, on_change)

        def _start():
            """Module start: reset state, load the saved settings and spots, open the journal reader and build the
            window.

            Runs on the client thread when the module is switched on.
            """
            st.update({"shutting": False, "active": True, "docked": False, "queue": [], "used": [],
                       "minimized": wnd.start_min(), "list": [], "list_sig": None, "next_scan": 0.0, "arrow": None,
                       "pin": 0, "arrow_at": 0.0, "arrow_off": False, "ping": None, "est": None, "look_until": 0.0,
                       "last_map": (0, 0.0), "drawn": None, "page": 0, "atlas_ver": None,
                       "atlas_sig": None, "dig_tiles": set()})
            load_settings()
            load_maps()
            read_gumps.clear()
            JR["rd"] = Journal.reader()
            hook_events()
            scan(time.time())
            build_window()
            wnd.dock(fit=True, min=(560, list_h(1, ROW_H)))
            update_arrow()

        def _tick():
            """Client tick of the Treasure Maps part.

            Handles double-clicks, the journal, the search for a map window, queued buttons, the one second scan
            (with the arrow and the World Map markers), the ping and the saves. Runs on the client thread, so
            nothing in it may wait.
            """
            if win["g"] is None:
                return
            # A closed window ends the module.
            if Kit.closed(win):
                return
            now = time.time()
            if st["used"]:
                handle_used(now)
            handle_journal(now)
            look_step(now)
            q = st["queue"]
            while q:
                a = q.pop(0)
                kind = a[0] if isinstance(a, tuple) else a
                if not wnd.action(kind):
                    ACTIONS[kind](a, now)
                if win["g"] is None:
                    return
            # Guard against a clock set back as well as the normal one second interval.
            if not (now < st["next_scan"] <= now + SCAN_EVERY):
                st["next_scan"] = now + SCAN_EVERY
                scan(now)
                arrow_closed(now)
                update_arrow()
                # The World Map markers are only made again when the list changed.
                if st["list_ver"] != st["atlas_ver"]:
                    st["atlas_ver"] = st["list_ver"]
                    atlas_publish()
            if st["ping"] is not None:
                ping_step(now)
            # Spots are written at most every SAVE_EVERY seconds, and only when changed.
            if st["dirty"] and not (now < st["next_save"] <= now + SAVE_EVERY):
                st["next_save"] = now + SAVE_EVERY
                save_maps()
            refresh()

        def _interval():
            """Tick spacing: 0.1 s while a map window is being looked for, else 0.2 s (the real work is a one
            second scan).
            """
            return 0.1 if st["look_until"] > time.time() else 0.2

        def _stop():
            """Module stop: take down our own arrow and the tile highlights, save, drop the journal reader."""
            st["shutting"] = True
            st["active"] = False
            update_arrow(force_off=True)
            save_settings()
            if st["dirty"]:
                save_maps()
            JR["rd"] = None
            dig_tiles(())
            st["used"], st["queue"], st["ping"] = [], [], None
            cleanup.close()

        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed, "interval": _interval}

    def _part_dry():
        """Build the Ore Tracker part and return its module hooks.

        For mining, lumberjacking, fishing and digging sand by hand. It never harvests, moves or targets
        anything itself (R2): it only shows things. It has a weight bar (the player's weight against the
        maximum, yellow from WEIGHT_WARN, red from WEIGHT_RED, with one alert as the red line is crossed;
        while Inventory > Paperdoll runs, its own weight alert speaks and this one stays quiet) and a list
        of dry spots.

        A spot goes on the list when the shard says it has run out. The shard keeps its resources in blocks
        of tiles (the harvest banks, see BANK), so a dry spot is that whole block. Each row shows a countdown
        until the block can be back, the distance and the direction. A spot leaves the list when its time is
        up, or at once when a harvest there works again (a failed skill check counts too: it means something
        is left). A click on a row points the tracking arrow at it; Ping sends a Look here map ping.

        The spot is the tile of the player's last target when it is within reach, else the tile in front of
        the player (marked about). Only the shard's own lines count, not a player saying the words.

        Saved keys: Harvest_settings, Harvest_pos, Harvest_min and Harvest_spots (kind,facet,x,y,earliest,
        latest,about joined by semicolons).
        """
        KEY = "harvest"
        TITLE = "Ore Tracker"
        SETTINGS_KEY = "Harvest_settings"
        POS_KEY = "Harvest_pos"
        MIN_KEY = "Harvest_min"
        # The four harvest kinds, in the order the settings page lists them.
        KINDS = ("ore", "wood", "fish", "sand")
        KIND_NAME = {"ore": "Ore", "wood": "Wood", "fish": "Fish", "sand": "Sand"}
        KIND_SKILL = {"ore": "mining", "wood": "lumberjacking", "fish": "fishing", "sand": "sand for glassblowing"}
        KIND_HUE = {"ore": 1153, "wood": 68, "fish": 88, "sand": 53}
        # The shard's lines for a spot that ran out, lower case and whole. Taken from the standard server
        # texts.
        DRY_TEXTS = {"there is no metal here to mine.": "ore", "there's not enough wood here to harvest.": "wood",
            "the fish don't seem to be biting here.": "fish", "there is no sand here to mine.": "sand",}
        # A failed skill check: the bank still has something in it.
        FAIL_TEXTS = {"you loosen some rocks but fail to find any useable ore.": "ore",
            "you hack at the tree for a while, but fail to produce any useable wood.": "wood",
            "you fish a while, but fail to catch anything.": "fish",
            "you dig for a while but fail to find any of sufficient quality for glassblowing.": "sand",}
        # A harvest that worked: the line starts with one of these.
        GOT_PREFIXES = (("you dig some ", "ore"), ("you put some logs", "wood"), ("you chop some ", "wood"),
            ("you pull out ", "fish"), ("you carefully dig up sand", "sand"),
            ("your backpack can't hold the sand", "sand"),)
        # Who the shard's lines come from; a player's name never counts.
        SHARD_SPEAKERS = ("", "system")
        # The harvest banks: the width and height of the tile block that shares one stock of the resource
        # (standard server values).
        BANK = {"ore": (8, 8), "wood": (4, 3), "fish": (8, 8), "sand": (8, 8)}
        # Minutes a bank takes to fill again (shortest, longest), counted from the first harvest of a full
        # bank (standard server values).
        RESPAWN = {"ore": (10, 20), "wood": (20, 30), "fish": (10, 20), "sand": (10, 20)}
        # Resources in guarded regions come back this many times slower.
        GUARDED_RESPAWN_X = 3
        # Tiles from the player at which the last target still counts as the harvest spot (the server's reach
        # plus one for a step).
        REACH = {"ore": 3, "wood": 3, "fish": 5, "sand": 3}
        # Banks whose first harvest time is remembered, at most.
        FIRST_MAX = 300
        ROWS = 8
        WEIGHT_WARN = 0.85
        WEIGHT_RED = 0.95
        # Maximum weight when the client does not report one: base plus a share per point of strength.
        WEIGHT_MAX_BASE, WEIGHT_MAX_PER_STR = 40, 3.5
        WEIGHT_EVERY = 0.5
        WEIGHT_ALERT = "harvest.weight"
        DRAW_EVERY = 1.0
        EXPIRE_EVERY = 1.0
        # Our own tracking arrow id (HRVT), so it does not touch another module's arrow.
        ARROW_ID = 0x48525654
        PING_TRY = 6.0
        SAVE_EVERY = 5.0
        SPOTS_KEY = "Harvest_spots"
        W = 440
        MINI_W, MINI_H = 340, 46
        ROW_H = 24
        FACING = {"north": (0, -1), "northeast": (1, -1), "east": (1, 0), "southeast": (1, 1),
                  "south": (0, 1), "southwest": (-1, 1), "west": (-1, 0), "northwest": (-1, -1)}
        ROW_TIP = "Put the tracking arrow on it (again: take it down)"
        PING_TIP = "Send a Look here ping on this spot so others know it is dry (needs World Map > Map Pings)"
        EMPTY_TEXT = "No dry spots yet: spots the shard says ran out show here."
        # The longest time a spot can stay dry, used to throw away saved spots that make no sense.
        SECS_MAX = 60.0 * GUARDED_RESPAWN_X * max(hi for _, hi in RESPAWN.values())
        settings = {"ore": True, "wood": True, "fish": True, "sand": True, "alert": True, "keep": True}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "rd": None, "ver": 0,
              # The remaining state keys are added by _start.
              "mini_key": None, "w_key": None, "arrow_at": 0.0}
        spots = {}
        first = {}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        # Work for the script thread (saving the list), queued by the client tick.
        jobs = []
        cleanup, queue, say = Kit.basics(st, TITLE)

        def load_settings():
            """Load the options from their saved key."""
            Kit.kv_load(SETTINGS_KEY, ";", settings)

        def save_settings():
            """Save the options."""
            Kit.kv_save(SETTINGS_KEY, ";", settings, KINDS + ("alert", "keep"))

        def spots_text():
            """The dry spot list as saved text: kind, facet, x, y, earliest, latest and the about flag, joined by
            semicolons.
            """
            return ";".join("%s,%d,%d,%d,%d,%d,%d" % (e["kind"], e["m"], e["x"], e["y"], int(e["lo"]), int(e["hi"]),
                                                      1 if e["about"] else 0) for e in spots.values())

        def load_spots():
            """Load the dry spots kept from the last run.

            Skipped when keeping the list is off. Spots whose time is up, or that a clock set far back would keep
            for ever, are dropped.
            """
            spots.clear()
            if not settings["keep"]:
                return
            now = time.time()
            for part in Kit.get_var(SPOTS_KEY).split(";"):
                b = part.split(",")
                if len(b) < 7 or b[0] not in KINDS:
                    continue
                try:
                    m, x, y, lo, hi = int(b[1]), int(b[2]), int(b[3]), float(b[4]), float(b[5])
                except ValueError:
                    continue
                if hi <= now or hi - now > SECS_MAX + 60:
                    continue
                add_spot(b[0], m, x, y, lo, hi, b[6] == "1", now)
            st["ver"] += 1

        def spots_changed():
            """The list changed: bump its version for the redraw and queue a save when keeping is on."""
            st["ver"] += 1
            if settings["keep"]:
                st["save_due"] = True

        def save_spots_job():
            """Save the list to its saved key (script thread, run from _thread_tick)."""
            st["save_due"] = False
            st["save_at"] = time.time() + SAVE_EVERY
            Kit.put_var(SPOTS_KEY, spots_text() if settings["keep"] else "")

        def bank_of(kind, m, x, y):
            """The key of the harvest bank a tile belongs to: kind, facet and the bank's block coordinates."""
            bw, bh = BANK[kind]
            return (kind, m, x // bw, y // bh)

        def add_spot(kind, m, x, y, lo, hi, about, now):
            """Add or replace the dry spot of a bank and return its key.

            lo and hi are the earliest and latest times it can be back, about says the tile was guessed. The
            list holds at most 60 spots.
            """
            key = bank_of(kind, m, x, y)
            old = spots.get(key)
            spots[key] = {"kind": kind, "m": m, "x": x, "y": y, "lo": lo, "hi": hi, "at": now,
                          "about": about, "key": key}
            # The block ran dry again at another tile: the arrow follows the new spot.
            if st["arrow"] == key and old is not None and (old["x"], old["y"]) != (x, y):
                API.TrackingArrow(x, y, ARROW_ID)
                st["arrow_at"] = now
            # A cap: the spot back soonest goes first.
            if len(spots) > 60:
                drop = None
                for k, e in spots.items():
                    if k != key and (drop is None or e["hi"] < spots[drop]["hi"]):
                        drop = k
                if drop is not None:
                    del spots[drop]
                    if st["arrow"] == drop:
                        arrow_off()
            return key

        def respawn_x():
            """How many times slower resources come back here: 3 inside a guard zone, else 1.

            This is the player's place, not the spot's; HOST.guarded() is a cached lookup and never waits.
            """
            return GUARDED_RESPAWN_X if HOST.guarded() is True else 1

        def note_dry(kind, x, y, m, about, now):
            """The shard said the spot ran out.

            When the bank's first harvest was seen this session, it is back between first plus the shortest and
            first plus the longest time; otherwise at any time up to the longest from now.
            """
            key = bank_of(kind, m, x, y)
            lo_m, hi_m = RESPAWN[kind]
            # Guard zones make the wait longer.
            x3 = respawn_x()
            lo_m, hi_m = lo_m * x3, hi_m * x3
            f = first.pop(key, None)
            if f is not None and 0 <= now - f < hi_m * 60.0:
                lo, hi = f + lo_m * 60.0, f + hi_m * 60.0
            else:
                lo, hi = now, now + hi_m * 60.0
            add_spot(kind, m, x, y, lo, hi, about, now)
            spots_changed()

        def note_back(kind, x, y, m, got, now):
            """A harvest there worked (got) or failed a skill check: the bank is not empty.

            The spot leaves the list. A success starts the bank's clock, that is its first harvest.
            """
            key = bank_of(kind, m, x, y)
            if spots.pop(key, None) is not None:
                if st["arrow"] == key:
                    arrow_off()
                spots_changed()
            if got:
                f = first.get(key)
                if f is None or not 0 <= now - f < RESPAWN[kind][1] * 60.0 * respawn_x():
                    # The memory of first harvests is bounded: old entries go first, then everything.
                    if len(first) >= FIRST_MAX:
                        for k in [k for k, t in first.items() if not 0 <= now - t < SECS_MAX]:
                            del first[k]
                        if len(first) >= FIRST_MAX:
                            first.clear()
                    first[key] = now

        def expire(now):
            """Drop spots whose time is up and take care of the arrow (client tick, once a second).

            Also forgets spots made in the future, which happens when the clock is set back, takes the arrow off
            when the player changed facet and notices an arrow the player closed.
            """
            # A spot noted in the future means the clock was set back.
            gone = [k for k, e in spots.items() if e["hi"] <= now or e["at"] - now > 60.0]
            for k in gone:
                del spots[k]
                if st["arrow"] == k:
                    arrow_off()
            if gone:
                spots_changed()
            a = st["arrow"]
            # The player closed the arrow with a right-click: its mark in the row goes (nothing to take down).
            if a is not None and 1.5 <= now - st["arrow_at"] and not arrow_open():
                st["arrow"] = None
                st["ver"] += 1
                a = None
            if a is not None:
                me = read_me()
                # After a facet change the arrow would point at that x, y in the wrong world.
                if me is not None and me[2] != a[1]:
                    arrow_off()

        def rebase(d):
            """The clock went back (d is negative): every time kept moves with it, so the list is not thrown away as
            made in the future and each countdown keeps the real time left.
            """
            for e in spots.values():
                e["lo"] += d
                e["hi"] += d
                e["at"] += d
            for k in list(first):
                first[k] += d
            for k in ("w_at", "draw_at", "expire_at", "save_at", "arrow_at"):
                st[k] = st[k] + d
            p = st["ping"]
            if p is not None:
                p[3] += d
            if spots:
                spots_changed()

        def read_me():
            """The player's (x, y, facet), remembered in st["me"], or None before the player is in the world.

            Runs on the client thread, so every call is answered in place.
            """
            p = API.Player
            if p is None:
                return None
            me = (int(p.X), int(p.Y), int(API.GetMap()))
            # Not in the world yet.
            if me[0] <= 0 and me[1] <= 0:
                return None
            st["me"] = me
            return me

        def target_tile(kind, me):
            """The spot a harvest line is about: (x, y, about).

            The last target's tile when it is within reach of the player, else the tile in front of the player,
            for which about is True.
            """
            px, py = me[0], me[1]
            p = API.LastTargetPos
            x, y = int(p.X), int(p.Y)
            # The client reports an unset target as a huge or zero coordinate.
            if 0 < x < 0xFFFF and 0 < y < 0xFFFF and max(abs(x - px), abs(y - py)) <= REACH[kind]:
                return x, y, False
            dx, dy = FACING.get(str(API.Player.Direction or "").strip().lower(), (0, 0))
            return px + dx, py + dy, True

        def line_kind(low):
            """Classify a lower case harvest line as (dry, kind), (fail, kind) or (got, kind), else None."""
            k = DRY_TEXTS.get(low)
            if k is not None:
                return "dry", k
            k = FAIL_TEXTS.get(low)
            if k is not None:
                return "fail", k
            if low.startswith("you"):
                for pre, k in GOT_PREFIXES:
                    if low.startswith(pre):
                        return "got", k
            return None

        def read_journal(now):
            """Read the new journal lines and note the harvest results (client tick).

            Only lines from the shard count. A line about a kind that is switched off is ignored when it says a
            spot ran dry; a line that says a harvest worked or failed still counts, so a spot is taken off the
            list even when its kind is hidden.
            """
            rd = st["rd"]
            if rd is None:
                return
            for ln in rd.new():
                hit = line_kind(ln.low.strip())
                if hit is None or (ln.name or "").strip().lower() not in SHARD_SPEAKERS:
                    continue
                what, kind = hit
                if what == "dry" and not settings[kind]:
                    continue
                me = read_me()
                if me is None:
                    continue
                x, y, about = target_tile(kind, me)
                if what == "dry":
                    note_dry(kind, x, y, me[2], about, now)
                else:
                    note_back(kind, x, y, me[2], what == "got", now)

        def character_alerts():
            """True while Inventory > Paperdoll (module key character) runs: it raises the same weight alert."""
            s = HOST.by_key.get("character")
            return s is not None and bool(s.running)

        def read_weight(now):
            """Read the player's weight twice a second, keep it for the bar and raise the red line alert once.

            The alert is armed again when the weight falls below 92 percent, so it comes once per crossing.
            When another module's alert would say the same thing, nothing is raised here. Skipped when nothing
            shows the weight.
            """
            # The second condition catches a clock set back.
            if now < st["w_at"] and st["w_at"] - now <= WEIGHT_EVERY:
                return
            st["w_at"] = now + WEIGHT_EVERY
            # Folded away and no alert wanted: nothing needs the reading.
            if not settings["alert"] and (win["g"] is None or (st["minimized"] and st["docked"])):
                return
            p = API.Player
            if p is None:
                return
            wt, wmax = int(p.Weight), int(p.WeightMax)
            # Strength is read only when it is needed.
            strength = int(p.Strength) if wmax <= 0 else 0
            # The client does not report the maximum weight: work it out from strength.
            if wmax <= 0 and strength > 0:
                wmax = int(WEIGHT_MAX_BASE + WEIGHT_MAX_PER_STR * strength)
            frac = (float(wt) / wmax) if wmax > 0 else -1.0
            st["weight"] = (wt, wmax, frac)
            if frac >= WEIGHT_RED:
                if st["w_armed"]:
                    raised = True
                    if settings["alert"] and not character_alerts():
                        # A refused alert (the alerts' rate limit, or its kind turned off) keeps it armed, so it comes
                        # when it can.
                        raised = HOST.alert(WEIGHT_ALERT, "Weight %d/%d (%d%%): nearly overloaded"
                                            % (wt, wmax, int(frac * 100)), level="warn", who="weight") is not False
                    if raised:
                        st["w_armed"] = False
            elif 0 <= frac < 0.92:
                st["w_armed"] = True

        def arrow_off():
            """Take our tracking arrow down, if it is up."""
            if st["arrow"] is None:
                return
            st["arrow"] = None
            st["ver"] += 1
            API.TrackingArrow(-1, -1, ARROW_ID)

        def arrow_to(key):
            """Row click: point the arrow at the spot, or take it down when it is already there.

            Says so when the spot is on another facet and does nothing else then.
            """
            e = spots.get(key)
            if e is None:
                return
            # Looked at at once, as it is a click: the arrow was closed by the player if it is not open now.
            if st["arrow"] == key and arrow_open(True):
                arrow_off()
                return
            # When the player's place is unknown, the last one read is used.
            me = read_me() or st["me"]
            if me is not None and me[2] != e["m"]:
                say("that spot is in %s; you are in %s." % (Kit.facet_name(e["m"]), Kit.facet_name(me[2])))
                return
            API.TrackingArrow(e["x"], e["y"], ARROW_ID)
            st["arrow"], st["arrow_at"] = key, time.time()
            st["ver"] += 1

        def ping_spot(key):
            """Ping button on a row: arm a Look here ping on the spot.

            Needs Map Pings (World Map) to be on; send_ping then tries until Map Pings has its turn.
            """
            e = spots.get(key)
            if e is None:
                return
            if HOST.services.get("pings.send") is None:
                say("turn World Map > Map Pings on to ping a spot.")
                return
            st["ping"] = [e["x"], e["y"], e["m"], time.time() + PING_TRY, "the dry %s spot (%d, %d)"
                          % (KIND_NAME[e["kind"]].lower(), e["x"], e["y"])]

        def send_ping(now):
            """Send the armed ping, retrying each tick until PING_TRY seconds have passed."""
            p = st["ping"]
            if p is None:
                return
            fn = HOST.services.get("pings.send")
            # Also gives up when the time lies too far ahead, as after the clock was set back.
            if fn is None or now > p[3] or p[3] - now > PING_TRY + 1.0:
                st["ping"] = None
                say("the ping on %s wasn't sent (%s)."
                    % (p[4], "Map Pings is off" if fn is None else "Map Pings stayed busy"))
                return
            try:
                ok = fn(p[0], p[1], p[2], "look")
            except Exception:
                # Failed outright: not tried again every tick.
                ok = None
            if ok is False:
                # Map Pings' own pace has not allowed another ping yet: try again next tick.
                return
            st["ping"] = None
            if ok:
                say("Look here ping on %s." % p[4], Kit.HUE_GOOD)
            else:
                say("couldn't send the ping on %s (Map Pings refused it)." % p[4], Kit.HUE_BAD)

        def mins(secs):
            """Seconds as a short text: seconds under a minute, else whole minutes rounded up."""
            secs = max(0, int(secs))
            if secs < 60:
                return "%ds" % secs
            return "%dm" % ((secs + 59) // 60)

        def dist_of(e, me):
            """Distance of a spot from the player, for the sort only (no text made).

            Zero when the player stands in the same bank, a huge number on another facet.
            """
            if me is None:
                return 0
            if me[2] != e["m"]:
                return 1 << 30
            if bank_of(e["kind"], me[2], me[0], me[1]) == e["key"]:
                return 0
            return max(abs(e["x"] - me[0]), abs(e["y"] - me[1]))

        def where_text(e, me):
            """The where text of a spot: here, the direction and distance, the facet, or the bare coordinates.

            The bare coordinates (no position known) go through xy, so streamer mode hides them.
            """
            if me is None:
                return xy(e["x"], e["y"], "(%d, %d)")
            if me[2] != e["m"]:
                return "in %s" % Kit.facet_name(e["m"])
            if bank_of(e["kind"], me[2], me[0], me[1]) == e["key"]:
                return "here"
            return ("about " if e["about"] else "") + Kit.where_text(e["x"] - me[0], e["y"] - me[1])

        def back_text(e, now):
            """The when text and hue of a spot: back in a range while it cannot be back yet, back within a time once
            it may.
            """
            if now < e["lo"]:
                return "back in %s-%s" % (mins(e["lo"] - now), mins(e["hi"] - now)), Kit.HUE_BAD
            return "back within %s" % mins(e["hi"] - now), Kit.HUE_TITLE

        def row_tip(e, on):
            """Tooltip of a row: the spot, the block it belongs to, when it is back and what a click does.

            Both the spot and the corner of its block are shown through xy.
            """
            bw, bh = BANK[e["kind"]]
            x0, y0 = (e["x"] // bw) * bw, (e["y"] // bh) * bh
            when = time.strftime("%H:%M", time.localtime(e["hi"]))
            if e["lo"] > e["at"]:
                back = "back between %s and %s" % (time.strftime("%H:%M", time.localtime(e["lo"])), when)
            else:
                back = "back by %s at the latest" % when
            return "%s ran dry at %s%s: the %dx%d block from %s, %s.  %s" % (
                KIND_NAME[e["kind"]], xy(e["x"], e["y"]), " (about: the tile in front of you)" if e["about"] else "",
                bw, bh, xy(x0, y0), back, "Take the tracking arrow down" if on else ROW_TIP)

        def shown_spots():
            """The spots of the kinds that are ticked."""
            return [e for e in spots.values() if settings[e["kind"]]]

        def _by_place(t):
            """Sort key of a listed row: distance, then the soonest back."""
            return (t[0], t[1])

        def atlas_publish():
            """Publish the spots that ran dry (ticked kinds, the most recent first, at most 15) as markers on
            TazUO's World Map.
            """
            ATLAS.set("dry", {atlas_name("%s dry %d %d" % (KIND_NAME[e["kind"]], e["x"], e["y"])):
                              (int(e["x"]), int(e["y"]), int(e["m"]), "blue")
                              for e in sorted(shown_spots(), key=lambda e: -e["at"])[:15]})

        def full_h(n):
            """Full window height for n rows."""
            return 2 * Kit.MARGIN + 30 + 3 * Kit.GAP + 46 + 36 + 74 + n * ROW_H + 22

        def build_window():
            """Build the window: weight bar, toolbar, the Here line, column heads and the pooled rows (client tick).

            The rows are made once and refilled by refresh; their number follows the window's height. When it is
            folded there is no body.
            """
            M = Kit.MARGIN
            z = told(wnd, st, W, full_h(1))
            w, h = z if z else (W, full_h(ROWS))
            n = wnd.rows(ROW_H, full_h(0), ROWS) if z else ROWS
            g, store, c = wnd.begin(w, h)
            rows = []
            if not st["minimized"]:
                wnd.frame(g)
                IW = w - 2 * M
                # Weight: a figure and the bar.
                yw = M + 30 + Kit.GAP
                Kit.add_section(g, M, yw, IW, 46, "WEIGHT")
                c["wtext"] = Kit.add_label(g, "", M + 20 + Kit.text_w("WEIGHT"), yw + 6, Kit.HUE_TEXT)
                Kit.weight_bar(g, c, M + 12, yw + 28, IW - 24)
                # Toolbar.
                yt = yw + 46 + Kit.GAP
                Kit.add_section(g, M, yt, IW, 36)
                bx = M + 12
                Kit.art_button(g, store, "clear", Kit.ART_CLOSE, bx, yt + 7, "Clear",
                               "Empty the list of dry spots", on_click=queue("clear"))
                bx += 35 + Kit.text_w("Clear") + 16
                Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, bx, yt + 7, "Arrow off",
                               "Take the tracking arrow down", on_click=queue("arrow_off"))
                # The list: the Here line, column heads, the pooled rows and the count.
                yl = yt + 36 + Kit.GAP
                Kit.add_section(g, M, yl, IW, h - yl - M, "DRY SPOTS  (nearest first)")
                c["here"] = Kit.add_label(g, "", M + 12, yl + 28, Kit.HUE_INFO)
                ping_w = 35 + Kit.text_w("Ping")
                xk, xw, xb = M + 12, M + 12 + 52, M + 12 + 52 + 130
                xp = M + IW - 6 - ping_w
                c["back_w"] = xp - 8 - xb
                yh = yl + 52
                Kit.add_label(g, "What", xk, yh, Kit.HUE_TITLE)
                Kit.add_label(g, "Where", xw, yh, Kit.HUE_TITLE)
                Kit.add_label(g, "When", xb, yh, Kit.HUE_TITLE)
                c["here_w"] = IW - 24
                for k in range(n):
                    ry = yh + 22 + k * ROW_H
                    r = {"val": None, "prev": None, "changed": 0.0, "sig": None, "vis": True, "tip": None,
                         "kind": Kit.add_label(g, "", xk, ry + 3, Kit.HUE_TEXT),
                         "where": Kit.add_label(g, "", xw, ry + 3, Kit.HUE_TEXT),
                         "back": Kit.add_label(g, "", xb, ry + 3, Kit.HUE_INFO)}
                    r["catch"] = Kit.catcher(g, M + 6, ry, xp - 4 - (M + 6), ROW_H,
                                             Kit.row_clicker(r, queue, "arrow", follow=False), ROW_TIP)
                    r["plbl"] = Kit.art_button(g, store, "ping%d" % k, Kit.ART_PLAY, xp, ry, "Ping", PING_TIP,
                                               on_click=Kit.row_clicker(r, queue, "ping", follow=False))
                    r["pbtn"] = store[0].get("ping%d" % k)
                    rows.append(r)
                c["more"] = Kit.add_label(g, "", M + 12, yh + 22 + n * ROW_H + 2, Kit.HUE_INFO)
            wnd.end(g, {"rows": rows})
            st["drawn"] = st["mini_drawn"] = st["wdrawn"] = None
            st["draw_at"] = 0.0
            refresh(time.time())

        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (260, 220), (MINI_W, MINI_H), 0x0E86,
                         cleanup, lock=True, clear={"rows": [], "c": {}}, docked_min=True)

        def show_row(r, on):
            """Show or hide all controls of a row, only when its state changes."""
            if r["vis"] == on:
                return
            r["vis"] = on
            for n in ("where", "back", "catch", "pbtn", "plbl"):
                Kit.set(r.get(n), "IsVisible", on)
            if not on:
                Kit.set_text(r["kind"], "")

        def refresh(now):
            """Draw what changed (client tick): nothing when folded, the status line when minimized, else the
            weight bar, the Here line and the rows.

            Skipped when the list, arrow and options did not change and a second has not passed since the last
            draw (countdowns and distances move every second).
            """
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return
            c = win["c"]
            if st["minimized"]:
                wt = st["weight"]
                sig = (st["ver"], settings["ore"], settings["wood"], settings["fish"], settings["sand"])
                # Counted only when the list changed.
                if st["count"][0] != sig:
                    st["count"] = (sig, len(shown_spots()))
                n = st["count"][1]
                # The text is only made on a change.
                mkey = (n, wt)
                if st["mini_drawn"] is not None and mkey == st["mini_key"]:
                    return
                st["mini_key"] = mkey
                txt = "%s: %s, %s" % (TITLE, ("weight %d%%" % int(wt[2] * 100)) if wt and wt[2] >= 0 else "weight ?",
                    Kit.count(n, "dry spot"))
                if txt != st["mini_drawn"]:
                    st["mini_drawn"] = txt
                    lbl = c.get("status")
                    if lbl is not None:
                        hue = Kit.HUE_INFO
                        if wt and wt[2] >= WEIGHT_RED:
                            hue = Kit.HUE_BAD
                        elif wt and wt[2] >= WEIGHT_WARN:
                            hue = Kit.HUE_TITLE
                        Kit.set_text(lbl, Kit.fit(txt, MINI_W - 90), hue)
                return
            draw_weight()
            sig = (st["ver"], st["arrow"], settings["ore"], settings["wood"], settings["fish"], settings["sand"])
            # The second condition keeps a redraw going once a second and survives a clock set back.
            if sig == st["drawn"] and now < st["draw_at"] and st["draw_at"] - now <= DRAW_EVERY:
                return
            st["drawn"], st["draw_at"] = sig, now + DRAW_EVERY
            me = read_me() or st["me"]
            # Only the distance is worked out for the whole list; texts are made just for the rows shown.
            listed = [(dist_of(e, me), e["hi"], e) for e in shown_spots()]
            listed.sort(key=_by_place)
            # The Here line: the dry block the player stands in, if any.
            here = None
            if me is not None:
                for kind in KINDS:
                    if settings[kind]:
                        e = spots.get(bank_of(kind, me[2], me[0], me[1]))
                        if e is not None:
                            here = e
                            break
            if here is not None:
                Kit.set_text(c["here"], Kit.fit("Here: %s is dry, %s" % (
                    KIND_NAME[here["kind"]].lower(), back_text(here, now)[0]), c["here_w"]), Kit.HUE_BAD)
            elif listed:
                Kit.set_text(c["here"], "Here: nothing known dry", Kit.HUE_GOOD)
            else:
                Kit.set_text(c["here"], Kit.fit(EMPTY_TEXT, c["here_w"]), Kit.HUE_INFO)
            back_w = c.get("back_w", 160)
            for k, r in enumerate(win["rows"]):
                if k >= len(listed):
                    Kit.row_set(r, None, now)
                    r["sig"] = None
                    show_row(r, False)
                    continue
                e = listed[k][2]
                where = where_text(e, me)
                key = e["key"]
                Kit.row_set(r, (key,), now)
                on = st["arrow"] == key
                back, bhue = back_text(e, now)
                rsig = (key, where, back, bhue, on, e["lo"], e["hi"])
                show_row(r, True)
                if rsig == r["sig"]:
                    continue
                r["sig"] = rsig
                Kit.set_text(r["kind"], KIND_NAME[e["kind"]], KIND_HUE.get(e["kind"], Kit.HUE_TEXT))
                Kit.set_text(r["where"], Kit.fit(("> " if on else "") + where, 124),
                             Kit.HUE_TITLE if on else Kit.HUE_TEXT)
                Kit.set_text(r["back"], Kit.fit(back, back_w), bhue)
                tip = (key, on, e["lo"], e["hi"])
                if tip != r["tip"]:
                    r["tip"] = tip
                    Kit.with_tip(r["catch"], row_tip(e, on))
            more = len(listed) - len(win["rows"])
            Kit.set_text(c["more"], ("+%d farther" % more) if more > 0 else "", Kit.HUE_INFO)

        def draw_weight():
            """Draw the weight figure and bar when the reading changed."""
            c = win["c"]
            wt = st["weight"]
            if st["wdrawn"] is not None and wt == st["w_key"]:
                return
            st["w_key"] = wt
            fills = c.get("wfills")
            if wt is None or wt[2] < 0:
                text, kind, width = "not known yet", None, 0
            else:
                text = "%d / %d stones (%d%%)" % (wt[0], wt[1], int(wt[2] * 100))
                kind, width = Kit.weight_level(wt[2], c.get("wbar_w", 100))
            sig = (text, kind, width)
            if sig == st["wdrawn"]:
                return
            st["wdrawn"] = sig
            hue = {"red": Kit.HUE_BAD, "warn": Kit.HUE_TITLE}.get(kind, Kit.HUE_TEXT)
            if c.get("wtext") is not None:
                Kit.set_text(c["wtext"], text, hue)
            Kit.weight_show(fills or {}, kind, width)

        RESPAWN_NOTE = ("Back in: ore and sand 10-20 min, wood 20-30, fish 10-20, from the block's first harvest (3x "
                        "as long in guarded towns).")

        def act_clear(action):
            """Clear button: empty the list."""
            arrow_off()
            spots.clear()
            spots_changed()

        # Queued actions by name; arrow and ping come as tuples with the spot key.
        ACTIONS = {"clear": act_clear, "arrow_off": lambda action: arrow_off(),
                   "arrow": lambda action: arrow_to(action[1]), "ping": lambda action: ping_spot(action[1])}

        def kind_caption(kind):
            """Caption of a kind's tick box: its name and skill."""
            return "%s (%s)" % (KIND_NAME[kind], KIND_SKILL[kind])

        def kind_cols(w):
            """2 when the four kinds fit two to a row on a page of width w, else 1."""
            widest = max(Kit.text_w(kind_caption(k)) for k in KINDS)
            return 2 if widest + 30 <= (w - 24) // 2 else 1

        def page_table(w):
            """The settings page table of the part for page width w."""
            cols, half = kind_cols(w), (w - 24) // 2
            return (("WHAT TO WATCH", [("check", k, kind_caption(k), "List spots where the %s ran out"
                                        % KIND_NAME[k].lower(), {"dx": 12 + (i % cols) * half,
                                        "stay": i % cols < cols - 1}) for i, k in enumerate(KINDS)] + [("gap", 6),
                        ("check", "keep", "Keep the list when Virtue Assistant stops (per character)",
                         "Unticked: it starts empty each time"), ("gap", 2)] + [("note", ln) for ln in
                        ["Unticked kinds are hidden, not forgotten."] + Kit.wrap(RESPAWN_NOTE, w - 28)], {"top": 32}),
                    ("WEIGHT  (yellow at %d%%, red at %d%%)" % (int(WEIGHT_WARN * 100), int(WEIGHT_RED * 100)), (
                        ("check", "alert", "Alert as you cross the red line", "Once each time you pass %d%% of your "
                         "maximum weight; quiet while Inventory > Paperdoll is on (it has its own)"
                         % int(WEIGHT_RED * 100)),), {"top": 32, "pad": 4}), atlas_page("dry"))

        def on_change(old, new):
            """Settings changed: queue a save when keeping changed, re-arm the weight alert when it was just turned
            on and redraw.
            """
            if new["keep"] != old["keep"]:
                st["save_due"] = True
            if new["alert"] and not old["alert"]:
                st["w_armed"] = True
            st["drawn"] = st["mini_drawn"] = None

        cfg = Kit.Page(settings, page_table, save_settings, on_change)

        def _start():
            """Module start: reset state, load the saved settings and list, open the journal reader and build the
            window.

            Runs on the client thread when the module is switched on. Registers the weight alert kind.
            """
            st.update({"shutting": False, "docked": False, "queue": [], "drawn": None,
                       "mini_drawn": None, "wdrawn": None, "arrow": None, "ping": None,
                       "w_armed": True, "weight": None, "w_at": 0.0, "draw_at": 0.0,
                       "expire_at": 0.0, "save_due": False, "save_at": 0.0, "me": None,
                       "count": (None, 0), "last_now": None, "atlas": None, "minimized": wnd.start_min()})
            # Left over work of an earlier run is dropped.
            del jobs[:]
            first.clear()
            load_settings()
            load_spots()
            # Only the lines from now on.
            st["rd"] = Journal.reader()
            HOST.alert_kind(WEIGHT_ALERT, "Weight near the limit", 0x04A)
            read_me()
            build_window()
            wnd.dock(fit=True, min=(W, full_h(1)))

        def _tick():
            """Client tick of the Ore Tracker part.

            Handles clock changes, queued buttons, the journal, expiry, the World Map markers, the weight, the
            ping and the drawing, and queues a save when one is due. Runs on the client thread, so nothing in it
            may wait.
            """
            if win["g"] is None:
                return
            # A closed window ends the module.
            if Kit.closed(win):
                return
            now = time.time()
            last, st["last_now"] = st["last_now"], now
            # The clock was set back.
            if last is not None and now < last - 2.0:
                rebase(now - last)
            q = st["queue"]
            while q:
                action = q.pop(0)
                kind = action[0] if isinstance(action, tuple) else action
                if not wnd.action(action):
                    ACTIONS[kind](action)
                if win["g"] is None:
                    return
            read_journal(now)
            # Once a second; the second condition catches a clock set back.
            if now >= st["expire_at"] or st["expire_at"] - now > EXPIRE_EVERY:
                st["expire_at"] = now + EXPIRE_EVERY
                expire(now)
            av = (st["ver"], settings["ore"], settings["wood"], settings["fish"], settings["sand"])
            if av != st["atlas"]:
                st["atlas"] = av
                atlas_publish()
            read_weight(now)
            send_ping(now)
            refresh(now)
            # The save runs on the script thread: it is queued and not done here.
            if st["save_due"] and (now >= st["save_at"] or st["save_at"] - now > SAVE_EVERY) and not jobs:
                jobs.append(save_spots_job)

        def _thread_tick():
            """Script thread, right after the client tick: run the queued saves."""
            while jobs and not st["shutting"]:
                jobs.pop(0)()

        def _thread_wanted():
            """True when a save is queued, so the thread tick runs only then."""
            return bool(jobs)

        def _stop():
            """Module stop: take down the arrow, drop the ping and the reader, save the settings and the list."""
            st["shutting"] = True
            arrow_off()
            st["ping"] = st["rd"] = None
            del jobs[:]
            save_settings()
            Kit.put_var(SPOTS_KEY, spots_text() if settings["keep"] else "")
            st["save_due"] = False
            cleanup.close()

        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed,
                "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}

    def _part_traps():
        """Build the Traps & Fields part and return its module hooks.

        The client cannot draw an outline round a world item, so a trap on the ground is recoloured instead:
        it is held at the green hue and, once per cycle, flashes to the red hue for a short beat (the pulse).
        The original hues are put back when a trap leaves range, vanishes, or the module stops. The recolour
        is client side only: nothing is sent to the server, so the shard never sees it (R2).

        With Map Pings on, each trap found gets one Danger! ping on its tile, once per serial and once per
        spot, at Map Pings' own pace. Magic fields (fire, poison, energy, paralyze) are a second group with
        their own hues, no pulse and no pings, and an optional overhead text. The first time a trap comes
        into range an alert says where.

        Saved keys: TrapHL_settings (range, cycle, pulse, hues, by-name, graphics and ping, joined by bars),
        TrapHL_fields (on, hue, para, say), TrapHL_view (min, paused) and TrapHL_pos.
        """
        KEY = "traphl"
        TITLE = "Traps & Fields"
        SETTINGS_KEY = "TrapHL_settings"
        POS_KEY = "TrapHL_pos"
        VIEW_KEY = "TrapHL_view"
        # Window height: one section holding the Ping button.
        H = Kit.MARGIN + 30 + Kit.GAP + 40 + Kit.MARGIN
        MINI_W, MINI_H = 320, 46
        HUE_GREEN = 68
        HUE_RED = 33
        # Client hue numbers run from 1 to 3000.
        HUE_MAX = 3000
        # Shortest time between two scans when a ground item event asks for an early one.
        POKE_GAP = 0.15
        SCAN_MOVE = 1.0
        SCAN_IDLE = 3.0
        HUE_EVERY = 3.0
        NAME_RETRY = 5.0
        # Item graphics of ground traps: saw, spike, gas, stone face, mushroom, fire column, flame spurt and
        # giant spike, and a trap door. These are the classic server art ids and may differ on this shard, so
        # the list can be edited on the settings page; any hue of these graphics counts.
        DEFAULT_GRAPHICS = [0x1103, 0x1116, 0x11AC, 0x11B1, 0x11A0, 0x11A8, 0x11B8, 0x113C, 0x1147, 0x10F5, 0x10FC,
            0x1125, 0x1B71, 0x1B72, 0x1B73, 0x1B74, 0x0E70,]
        FIELDS_KEY = "TrapHL_fields"
        # Graphic ranges of the field spells' art (the client animates the frames of one field): the first
        # id of each is what the spell places.
        FIELD_RANGES = (("fire", 0x398C, 0x399F), ("poison", 0x3914, 0x3929),
                        ("paralyze", 0x3967, 0x398A), ("energy", 0x3946, 0x3964))
        FIELD_HUE = 0x0035
        PARALYZE_HUE = 0x0481
        FIELD_WORDS = {"fire": ("Fire field", Kit.HUE_TITLE), "poison": ("Poison field", Kit.HUE_TITLE),
                       "energy": ("Energy field", Kit.HUE_TITLE), "paralyze": ("Paralyze field!", Kit.HUE_BAD)}
        FIELD_SAY_NEAR = 3
        ALERT_TRAP = "traphl.trap"
        # Graphic -> field kind, made once for all four ranges.
        FIELD_GFX = {g: k for k, a, b in FIELD_RANGES for g in range(a, b + 1)}
        # Used in place of FIELD_GFX when field highlighting is off.
        NO_FIELDS = {}
        # Defaults; the pipe separated save string keeps the older order of fields, new ones sit at the end.
        settings = {"range": 14, "cycle": 2.0, "pulse": True,
                    "green": HUE_GREEN, "red": HUE_RED, "by_name": True, "graphics": list(DEFAULT_GRAPHICS),
                    "ping": True, "fields": True, "field_hue": FIELD_HUE, "para_hue": PARALYZE_HUE, "field_say": False}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "hooked": False, "poke": False}
        win = {"g": None, "c": {}, "store": ({}, {})}
        page = {"f": None, "gfx_typed": None, "gfx_since": 0.0}
        cleanup, queue, say = Kit.basics(st, TITLE)

        def load_settings():
            """Load the main settings: range, cycle, pulse, hues, by-name, graphics and the ping flag.

            The saved string has bar separated fields; a short or broken one leaves the defaults. Values are
            clamped.
            """
            p = Kit.get_var(SETTINGS_KEY).split("|")
            if len(p) < 7:
                return
            with Kit.quiet:
                settings["range"] = max(1, min(30, int(p[0])))
                settings["cycle"] = max(0.5, min(10.0, float(p[1])))
                settings["pulse"] = p[2] == "1"
                settings["green"] = int(p[3])
                settings["red"] = int(p[4])
                settings["by_name"] = p[5] == "1"
                gl = parse_graphics(p[6])
                if gl or not p[6].strip():
                    settings["graphics"] = gl
                # A field added later: it is on when absent.
                if len(p) >= 8:
                    settings["ping"] = p[7] != "0"

        def load_fields():
            """Load the magic field settings from their own key.

            Their own key means older saves load with the defaults.
            """
            v = Kit.codec_load(Kit.get_var(FIELDS_KEY))
            settings["fields"] = v.get("on") != "0"
            settings["field_say"] = v.get("say") == "1"
            for k, key, default in (("hue", "field_hue", FIELD_HUE), ("para", "para_hue", PARALYZE_HUE)):
                try:
                    settings[key] = max(0, min(HUE_MAX, int(v[k])))
                except (KeyError, ValueError):
                    settings[key] = default

        def save_fields():
            """Save the magic field settings."""
            Kit.put_var(FIELDS_KEY, "on=%d;hue=%d;para=%d;say=%d" % (
                int(settings["fields"]), settings["field_hue"], settings["para_hue"], int(settings["field_say"])))

        def save_settings():
            """Save the main settings in the bar separated format load_settings reads."""
            Kit.put_var(SETTINGS_KEY, "|".join([str(settings["range"]), "%.2f" % settings["cycle"],
                        "1" if settings["pulse"] else "0", str(settings["green"]), str(settings["red"]),
                        "1" if settings["by_name"] else "0", graphics_text(), "1" if settings["ping"] else "0"]))

        def parse_graphics(text):
            """Parse a typed list of graphic ids into a list of ints.

            Separators are commas, semicolons or spaces; ids are always read as hex, with or without 0x. Zero,
            out of range and duplicate ids are dropped.
            """
            out = []
            for tok in str(text).replace(";", ",").replace(" ", ",").split(","):
                tok = tok.strip()
                if not tok:
                    continue
                try:
                    # Always hex.
                    v = int(tok, 16)
                except Exception:
                    continue
                if 0 < v < 0x10000 and v not in out:
                    out.append(v)
            return out

        def graphics_text():
            """The trap graphics as editable text, 0x1103 style, comma separated."""
            return ", ".join("0x%04X" % g for g in settings["graphics"])

        def load_view():
            """Load whether the window was minimized and highlighting paused."""
            raw = Kit.get_var(VIEW_KEY)
            v = Kit.codec_load(raw)
            st["minimized"] = v.get("min") == "1"
            st["paused"] = v.get("paused") == "1"
            st["view_saved"] = raw

        def save_view():
            """Save the view (minimized, paused) the moment it changes."""
            data = "min=%d;paused=%d" % (int(bool(st["minimized"])), int(bool(st["paused"])))
            if data != st.get("view_saved"):
                st["view_saved"] = data
                Kit.put_var(VIEW_KEY, data)

        def set_hue(item, hue):
            """Recolour an item in the client by setting its hue (masked to 16 bits)."""
            item.Hue = int(hue) & 0xFFFF

        def get_hue(item):
            """The item's hue, 0 when it has none."""
            return int(item.Hue or 0)

        def xy_of(item):
            """(x, y) of an item."""
            return int(item.X), int(item.Y)

        # The verdict per ground serial: serial -> (graphic, kind, retry), kind 1 trap, 2 field, 0 neither.
        # retry is 0 when final, else the scan number from which an unnamed item's name is read again.
        verdicts = {}
        # What the verdicts were made under, so the cache starts over when a setting changes.
        VERDICT_SIG = {"gfx": None, "wanted": frozenset(), "by_name": None, "fields": None}

        def named_trap(it):
            """Does the client call this ground item a trap (its name has trap in it but not scroll or kit)?

            True or False, or None while the client has no name for it yet (it is asked again later). A magic
            trap scroll or a tinker's trap kit on the floor is named after a trap but is not one.
            """
            # Names are only known to the client after a tooltip or a click.
            name = str(it.Name or "").lower()
            if not name:
                return None
            return "trap" in name and "scroll" not in name and "kit" not in name

        def verdict_sig():
            """The set of trap graphics wanted, remade (and the verdict cache emptied) when a setting that the
            verdicts depend on changed.
            """
            sig = VERDICT_SIG
            gl = settings["graphics"]
            if sig["gfx"] is not gl or sig["by_name"] != settings["by_name"] or sig["fields"] != settings["fields"]:
                sig["gfx"], sig["wanted"] = gl, frozenset(gl)
                sig["by_name"], sig["fields"] = settings["by_name"], settings["fields"]
                verdicts.clear()
            return sig["wanted"]

        def scan():
            """Scan the ground once and recolour what it finds, on the client tick.

            Runs when you move (at most every SCAN_MOVE s), every SCAN_IDLE s while you stand still, and
            soon after a trap or field graphic appears. Reads every ground item in range with one call, gives
            each a verdict (cached by serial), and then: newly seen traps get their original hue remembered
            and the green hue, joined to the ping queue and the new trap alert; known ones are looked at
            again; traps that left have their hue put back. Fields go through scan_fields.
            """
            rng = int(settings["range"])
            # Our facet is read once, and only if a trap is new.
            st["atlas_map"] = None
            found = {}
            ffound = {}
            now = st["last_scan"]
            # Timed in seconds, so the hue check (every HUE_EVERY s) and the name retry
            # (NAME_RETRY s) keep their pace however often the scan runs.
            check_hues = now >= st["hue_at"]
            field_gfx = FIELD_GFX if settings["fields"] else NO_FIELDS
            if check_hues:
                st["hue_at"] = now + HUE_EVERY
            wanted = verdict_sig()
            by_name = settings["by_name"]
            old = verdicts
            seen = {}
            # One call hands back every ground item within range.
            for it in API.GetItemsOnGround(rng) or ():
                serial = int(it.Serial)
                g = int(it.Graphic)
                v = old.get(serial)
                if v is not None and v[0] == g and (not v[2] or now < v[2]):
                    kind = v[1]
                    seen[serial] = v
                else:
                    retry = 0
                    if g in wanted:
                        kind = 1
                    elif by_name and g not in field_gfx:
                        named = named_trap(it)
                        if named is None:
                            kind, retry = 0, now + NAME_RETRY
                        else:
                            kind = 1 if named else 0
                    else:
                        kind = 2 if g in field_gfx else 0
                    seen[serial] = (g, kind, retry)
                if kind == 1:
                    found[serial] = it
                elif kind == 2:
                    ffound[serial] = it
            # Only what is still on the ground is kept.
            verdicts.clear()
            verdicts.update(seen)
            tracked = st["tracked"]
            new_traps = []
            for serial, it in found.items():
                rec = tracked.get(serial)
                if rec is None:
                    orig = get_hue(it)
                    # A trap already wearing our hue (left painted by an earlier run) has no hue of its own to restore.
                    if orig in (settings["green"], settings["red"]):
                        orig = 0
                    tracked[serial] = {"item": it, "orig": orig, "set": settings["green"]}
                    set_hue(it, settings["green"])
                    atlas_seen(it)
                    if settings["ping"] and serial not in st["pinged"]:
                        st["ping_wait"].append(serial)
                    if serial not in st["alerted"]:
                        new_traps.append(it)
                else:
                    rec["item"] = it
                    if check_hues and get_hue(it) != rec["set"]:
                        set_hue(it, rec["set"])
            gone = [s for s in tracked if s not in found]
            for serial in gone:
                put_back(serial, tracked.pop(serial))
            # A trap that left before its ping went out stops waiting; it is queued again if it returns, so it is
            # never in the list twice.
            if gone and st["ping_wait"]:
                st["ping_wait"] = [s for s in st["ping_wait"] if s in tracked]
            if new_traps:
                alert_new_traps(new_traps)
            if ffound or st["fields"]:
                scan_fields(ffound, check_hues)

        def atlas_seen(it):
            """A trap newly in range goes on the World Map list (each spot once; the oldest leave past 20)."""
            x, y = xy_of(it)
            if x <= 0 or y <= 0:
                return
            if st["atlas_map"] is None:
                st["atlas_map"] = int(API.GetMap())
            spot = (x, y, st["atlas_map"])
            seen = st["atlas_traps"]
            if spot in seen:
                return
            seen.append(spot)
            if len(seen) > 20:
                del seen[0]
            st["atlas_ver"] += 1

        def atlas_publish():
            """Publish the remembered traps as markers on TazUO's World Map."""
            ATLAS.set("traps", {atlas_name("Trap %d %d" % (x, y)): (x, y, m, "red") for x, y, m in st["atlas_traps"]})

        # Compass names for the new trap text.
        DIRS = ("east", "south-east", "south", "south-west", "west", "north-west", "north", "north-east")

        def alert_new_traps(its):
            """Raise one alert for the traps seen for the first time in this scan.

            Each trap is only alerted once: its serial is remembered (the memory starts over at 5000). The text
            names the nearest one and how far and which way it is.
            """
            alerted = st["alerted"]
            if len(alerted) + len(its) > 5000:
                alerted.clear()
            p = API.Player
            px, py = int(p.X), int(p.Y)
            best, best_d, bdx, bdy = None, None, 0, 0
            for it in its:
                alerted.add(int(it.Serial))
                dx, dy = int(it.X) - px, int(it.Y) - py
                d = max(abs(dx), abs(dy))
                if best_d is None or d < best_d:
                    best, best_d, bdx, bdy = it, d, dx, dy
            w = Kit.where_text(bdx, bdy, names=DIRS)
            text = "A trap %s" % w if len(its) == 1 else "%d new traps in range (nearest %s)" % (len(its), w)
            # Rate limited per trap, not per text: two traps that come into range at the same distance and way are
            # still two alerts.
            HOST.alert(ALERT_TRAP, text, who=int(best.Serial))

        def field_hue(kind):
            """The hue a field of this kind gets: its own for paralyze, the shared one for the rest."""
            return settings["para_hue"] if kind == "paralyze" else settings["field_hue"]

        def scan_fields(ffound, check_hues):
            """Handle the fields on the ground: new ones are painted, known ones repainted and gone ones restored.

            A hue of 0 leaves a kind as it is. A field painted by a run that never stopped keeps no original hue.
            Known fields are repainted when the hue was changed on the settings page or, every third scan, when
            the server put theirs back. New fields are named overhead when asked.
            """
            fields = st["fields"]
            said_now = []
            for serial, it in ffound.items():
                rec = fields.get(serial)
                if rec is None:
                    kind = FIELD_GFX.get(int(it.Graphic))
                    if kind is None:
                        continue
                    want = field_hue(kind)
                    orig = get_hue(it)
                    # Left painted by a run that never stopped: no real hue to put back.
                    if orig and orig in (settings["field_hue"], settings["para_hue"]):
                        orig = 0
                    fields[serial] = rec = {"item": it, "orig": orig, "set": want, "kind": kind}
                    if want:
                        set_hue(it, want)
                    if settings["field_say"]:
                        said_now.append(rec)
                    continue
                rec["item"] = it
                want = field_hue(rec["kind"])
                # The hue was changed on the settings page.
                if want != rec["set"]:
                    set_hue(it, want if want else rec["orig"])
                    rec["set"] = want
                elif want and check_hues and get_hue(it) != want:
                    set_hue(it, want)
            for serial in [s_ for s_ in fields if s_ not in ffound]:
                restore_field(serial)
            if said_now:
                say_fields(said_now)

        def say_fields(recs):
            """Name each new field overhead once, not once per tile of it.

            A tile within FIELD_SAY_NEAR of a tile of the same kind seen in the last ten seconds belongs to that
            field, so a wall, taken tile by tile along its line, is one field however long. The memory of seen
            tiles is cut to the last 20.
            """
            now = time.time()
            said = [e for e in st["field_said"] if now - e[3] < 10.0]
            # Sorted along the wall's line so neighbouring tiles come together.
            spots = sorted([xy_of(rec["item"]) + (rec["kind"], rec["item"]) for rec in recs], key=_by_place)
            for x, y, kind, it in spots:
                dup = False
                for k, sx, sy, t in said:
                    if (k == kind and abs(sx - x) <= FIELD_SAY_NEAR and abs(sy - y) <= FIELD_SAY_NEAR):
                        dup = True
                        break
                # The tile counts for the field whether it was said or not.
                said.append((kind, x, y, now))
                if dup:
                    continue
                text, hue = FIELD_WORDS.get(kind, ("Field", Kit.HUE_TITLE))
                API.HeadMsg(text, int(it.Serial), hue)
            st["field_said"] = said[-20:]

        def _by_place(e):
            """Sort key of a field tile: x then y."""
            return (e[0], e[1])

        def restore_field(serial):
            """Forget a field and give its original hue back, when it was painted."""
            rec = st["fields"].pop(serial, None)
            if rec is not None and rec["set"]:
                put_back(serial, rec)

        def put_back(serial, rec):
            """Put an item's original hue back, looking the item up again first.

            The item may have been re-created by the client, so the stored object is only the fallback.
            """
            set_hue(API.FindItem(serial) or rec["item"], rec["orig"])

        def restore_all():
            """Put back every hue this part has changed, traps and fields (module stop and Pause)."""
            for serial in list(st["tracked"]):
                put_back(serial, st["tracked"].pop(serial))
            for serial in list(st["fields"]):
                restore_field(serial)

        def pulse():
            """Hold the traps green and flash them red for a beat once per cycle.

            A hue is only set when it changes, twice a cycle; nothing is read back here, the scan repaints a hue
            the server put back.
            """
            if not st["tracked"]:
                return
            want_red = settings["pulse"] and (time.time() % max(0.5, settings["cycle"])
                                              # The beat is at most 0.35 s and never more than half the cycle.
                                              < min(0.35, settings["cycle"] / 2.0))
            hue = settings["red"] if want_red else settings["green"]
            for rec in st["tracked"].values():
                if rec["set"] != hue:
                    set_hue(rec["item"], hue)
                    rec["set"] = hue

        def ping_service():
            """Map Pings' send function, or None while Map Pings is off."""
            return HOST.services.get("pings.send")

        def send_pings():
            """Send the next waiting trap ping, redrawing the status when the queue changed."""
            n0 = len(st["ping_wait"])
            if n0:
                _send_one_ping()
                if len(st["ping_wait"]) != n0:
                    refresh()

        def _send_one_ping():
            """Send at most one Danger! ping per tick, for the first trap still waiting.

            A trap is pinged once: its serial and its spot are remembered, so a trap put back on the same tile
            with a new serial is not pinged again. Pings go out 0.75 s apart, Map Pings' own pace; should it
            still answer False (too soon), the trap waits for the next tick. While Map Pings is off they wait
            and go out once it is on, for the traps still in range.
            """
            wait = st["ping_wait"]
            svc = ping_service()
            if svc is None:
                # Said once, not every tick.
                if not st["ping_noted"]:
                    st["ping_noted"] = True
                    say("turn World Map > Map Pings on to ping traps (they wait until then).")
                return
            # Map Pings' pace: not yet.
            if time.time() < st["ping_next"]:
                return
            tracked = st["tracked"]
            m = None
            while wait:
                serial = wait[0]
                rec = tracked.get(serial)
                # Gone, or already pinged.
                if rec is None or serial in st["pinged"]:
                    wait.pop(0)
                    continue
                x, y = xy_of(rec["item"])
                # No place to ping.
                if x <= 0 or y <= 0:
                    wait.pop(0)
                    continue
                if m is None:
                    m = int(API.GetMap())
                spot = (m, x, y)
                if spot in st["pinged_spots"]:
                    mark_pinged(serial, None)
                    wait.pop(0)
                    continue
                try:
                    ok = svc(x, y, m, "danger", "You (trap)")
                except Exception:
                    # A ping that fails outright is not asked for again every tick (it may have been half shown
                    # already): this trap is done.
                    mark_pinged(serial, spot)
                    wait.pop(0)
                    return
                if ok:
                    wait.pop(0)
                    mark_pinged(serial, spot)
                    st["ping_sent"] += 1
                    # Read after the call: Map Pings' clock is later than ours.
                    st["ping_next"] = time.time() + 0.75
                return

        def mark_pinged(serial, spot):
            """Remember that a trap (and its spot) was pinged; the memory starts over at 5000 entries."""
            if len(st["pinged"]) >= 5000:
                st["pinged"].clear()
                st["pinged_spots"].clear()
            st["pinged"].add(serial)
            if spot is not None:
                st["pinged_spots"].add(spot)

        def ping_again():
            """Ping traps on screen button: every trap in range gets its ping now, and each may be pinged once more
            when next found.
            """
            st["pinged"].clear()
            st["pinged_spots"].clear()
            st["ping_sent"] = 0
            st["ping_wait"] = list(st["tracked"])
            n = len(st["ping_wait"])
            if st["paused"]:
                msg = "paused: untick Pause highlighting (World Map settings) to ping traps."
            elif n == 0:
                msg = "no traps in range; each is pinged when next found."
            elif ping_service() is None:
                msg = ("%s to ping once World Map > Map Pings is on." % Kit.count(n, "trap"))
            else:
                msg = "pinging %s." % Kit.count(n, "trap")
            say(msg)
            st["ping_noted"] = False
            refresh()

        def ping_status():
            """The ping part of the status: (text, hue)."""
            n = len(st["ping_wait"])
            # Also covers the button with automatic pinging off.
            if n and st["ping_svc"] is not None:
                return "sending %d" % n, Kit.HUE_INFO
            if not settings["ping"]:
                return "auto-ping off", Kit.HUE_INFO
            if st["ping_svc"] is None:
                return "World Map > Map Pings is off", Kit.HUE_BAD
            return "%d sent" % st["ping_sent"], Kit.HUE_GOOD

        PING_TIP = "Ping danger on each highlighted trap, and again when next found (needs World Map > Map Pings)"
        PING_CAP = "Ping traps on screen"

        def build_window():
            """Build the floating window: one circle button, or the minimized bar (client tick).

            The status, Pause and the graphic id printing are on the settings page.
            """
            z = told(wnd, st, 320, H)
            w, h = z if z else (320, H)
            g, store, c = wnd.begin(w, h)
            if not st["minimized"]:
                wnd.frame(g)
                M = Kit.MARGIN
                yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, w - 2 * M, h - yb - M)
                Kit.art_button(g, store, "ping", Kit.ART_CIRCLE, M + 12, yb + 12, PING_CAP,
                               PING_TIP, on_click=queue("ping_again"))
            wnd.end(g)
            refresh()
            save_view()

        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, None, (200, 200), (MINI_W, MINI_H), 0x113C,
                         cleanup, lock=True)

        def refresh():
            """Update the status texts: the minimized bar and the settings page's status lines.

            Also keeps the page's Paused box in step with the real state.
            """
            c = win["c"]
            n = len(st["tracked"])
            nf = len(st["fields"])
            if st["paused"]:
                text, hue = "Paused", Kit.HUE_INFO
            elif n == 0 and nf == 0:
                text, hue = "No traps in range", Kit.HUE_INFO
            elif nf == 0:
                text, hue = "Highlighting %s" % Kit.count(n, "trap"), Kit.HUE_GOOD
            elif n == 0:
                text, hue = "Highlighting %s" % Kit.count(nf, "field"), Kit.HUE_GOOD
            else:
                text, hue = "Highlighting %s, %s" % (Kit.count(n, "trap"), Kit.count(nf, "field")), Kit.HUE_GOOD
            # The minimized bar.
            if c.get("status") is not None:
                Kit.set_text(c["status"], Kit.fit("%s: %s" % (TITLE, journal_case(text)), MINI_W - 90), hue)
            f = page["f"]
            if f is None:
                return
            Kit.set_text(f.c["now"], text, hue)
            ptext, phue = ping_status()
            Kit.set_text(f.c["now_ping"], "Pings: " + ptext, phue)
            # Skipped while a change from the page is waiting for the next tick.
            if st["pause_want"] is None and bool(f.c["paused"].IsChecked) != bool(st["paused"]):
                f.c["paused"].SetIsChecked(bool(st["paused"]))

        def draw_status(f, x, y):
            """Settings page row: the status labels (what is highlighted, and the pings)."""
            f.c["now"] = Kit.add_label(f.g, "", x + 12, y, Kit.HUE_GOOD)
            f.c["now_ping"] = Kit.add_label(f.g, "", x + 12 + f.w // 2, y, Kit.HUE_INFO)

        def draw_paused(f, x, y):
            """Settings page row: the Pause highlighting tick box."""
            f.c["paused"] = Kit.add_check(f.g, "Pause highlighting (the hues are put back)", x + 12, y, st["paused"],
                                          "Stops the scan and puts every hue back")

        ACTIONS = {"ping_again": ping_again}

        def draw_cycle(f, x, y):
            """Settings page row: the pulse cycle slider and its value text."""
            Kit.add_label(f.g, "Pulse cycle:", x + 12, y + 4)
            cyc = int(round(settings["cycle"] * 10))
            f.c["cycle"] = Kit.with_tip(Kit.add_slider(f.g, x + 120, y + 2, 160, 5, 100, cyc),
                                        "Seconds between red flashes (0.5-10)")
            f.c["cycle_v"] = Kit.add_label(f.g, "%.1f s" % settings["cycle"], x + 290, y + 4, Kit.HUE_INFO)

        def draw_graphics(f, x, y):
            """Settings page row: the text box of trap graphics (hex)."""
            f.c["graphics"] = Kit.with_tip(Kit.add_textbox(f.g, graphics_text(), x + 12, y, f.w - 28, numbers=False),
                                           "Trap item graphics in hex (0x1103 or 1103), comma separated; applied "
                                           "when you stop typing")

        LEFT = {"lw": 98, "fw": 60, "stay": True, "clamp": False}
        PAGE = (("STATUS  (the window has %s)" % PING_CAP, (("custom", 24, draw_status), ("custom", 26, draw_paused)),
                 {"pad": 4}), ("TRAPS  (hues are client hue numbers)", (
                    ("slider", "range", "Scan range:", "Tiles round you scanned as you move (1-30)",
                     1, 30, {"lw": 98, "ldy": 4, "sw": 160, "ugap": 10, "vfmt": "%d tiles"}),
                    ("custom", 29, draw_cycle),
                    ("num", "green", "Green hue:", "Hue traps are held at (1-%d; default %d)" % (HUE_MAX, HUE_GREEN),
                     None, 1, HUE_MAX, LEFT),
                    ("num", "red", "Red hue:", "Hue of the pulse (1-%d; default %d)" % (HUE_MAX, HUE_RED), None, 1,
                     HUE_MAX, {"dx": 200, "lw": 70, "fw": 60, "h": 29, "clamp": False}),
                    ("check", "pulse", "Pulse red once per cycle (unticked: steady green)",
                     "Flashes each highlighted trap red for a beat")), {"top": 32, "pad": 2}),
                ("TRAP GRAPHICS  (hex ids, comma separated)", (("custom", 30, draw_graphics),
                    ("check", "by_name", "Also highlight ground items the client names 'trap'", "For traps not in the "
                     "list (the client knows a name only after a tooltip or click)")), {"top": 32, "pad": 8}),
                ("TRAP PINGS  (needs World Map > Map Pings)", (("check", "ping", "Send a Danger! map ping on each "
                  "new trap, once per trap", "For you and your guildmates; \"%s\" on the window pings them all again"
                  % PING_CAP),), {"top": 32, "pad": 4}), ("MAGIC FIELDS  (client hue numbers, 0 = leave as is)", (
                    ("check", "fields", "Highlight magic fields: fire, poison, energy, paralyze",
                     "Client-side recolour, like the traps; paralyze fields get their own hue", {"h": 29}),
                    ("num", "field_hue", "Field hue:", "Hue of fire, poison and energy fields (0-%d, 0 = as is; "
                     "default %d)" % (HUE_MAX, FIELD_HUE), None, 0, HUE_MAX, LEFT),
                    ("num", "para_hue", "Paralyze hue:", "Hue of paralyze fields (0-%d, 0 = as is; default %d)"
                     % (HUE_MAX, PARALYZE_HUE), None, 0, HUE_MAX, {"dx": 200, "lgap": 12, "fw": 60, "h": 29,
                                                                    "clamp": False}),
                    ("check", "field_say", "Show an overhead text when a field appears",
                     "Names each new field above it once (\"Fire field\", \"Paralyze field!\")")),
                 {"top": 32, "pad": 2}), atlas_page("traps"))

        def page_table(w):
            """The settings page table (the same for any width)."""
            return PAGE

        cfg = Kit.Page(settings, page_table, save_settings)

        def build_config(g, x, y, w):
            """Build the settings page: the form from PAGE, and its remembered typing state."""
            page["f"] = Kit.Form(g, x, y, w, settings, PAGE)
            page["gfx_typed"], page["gfx_applied"] = None, graphics_text()
            refresh()

        def poll_config():
            """Poll the settings page and apply what changed (client tick).

            Reads the form, the cycle slider, the Paused box and the graphics text. The graphics list is applied
            only once the text has stood unchanged for 0.7 s, so typing 0x11 on the way to 0x11AC does not
            highlight graphic 0x0011 half way. Pause is applied by the tick. Turning pings on queues the traps
            in range not yet pinged; off clears the queue.
            """
            f = page["f"]
            if f is None:
                return
            new = f.read()
            c = f.c
            now = time.time()
            try:
                typed = str(c["graphics"].Text or "")
                cyc = int(c["cycle"].Value)
                pz = bool(c["paused"].IsChecked)
            except Exception:
                return
            # The slider counts tenths of a second.
            cyc = max(5, min(100, cyc)) / 10.0
            if abs(cyc - settings["cycle"]) > 0.01:
                new["cycle"] = cyc
                Kit.set_text(c["cycle_v"], "%.1f s" % cyc)
            if typed != page["gfx_typed"]:
                page["gfx_typed"], page["gfx_since"] = typed, now
            # Applied once the text has settled and differs from what was applied last.
            elif now - page["gfx_since"] >= 0.7 and typed != page["gfx_applied"]:
                page["gfx_applied"] = typed
                # Empty text clears the list; unparsable text keeps the old one.
                new["graphics"] = (parse_graphics(typed) or settings["graphics"]) if typed.strip() else []
            if pz != (st["paused"] if st["pause_want"] is None else st["pause_want"]):
                st["pause_want"] = pz
            if new["ping"] != settings["ping"]:
                st["ping_wait"] = [sr for sr in st["tracked"] if sr not in st["pinged"]] if new["ping"] else []
            if new == settings:
                return
            settings.update(new)
            # Rescan at once with the new list, range or hues.
            st["last_scan"] = 0.0
            save_settings()
            save_fields()
            refresh()

        def config_closed():
            """Settings page closed: forget its form."""
            page["f"] = None
            page["gfx_typed"] = None

        def _start():
            """Module start: reset state, load settings, fields and view, hook the ground item and position
            events and build the window.

            Runs on the client thread when the module is switched on.
            """
            st.update({"shutting": False, "docked": False, "queue": [], "last_scan": 0.0,
                       "hue_at": 0.0, "moved": False, "tracked": {}, "pinged": set(), "pinged_spots": set(),
                       "ping_wait": [], "ping_sent": 0, "ping_noted": False,
                       "ping_svc": ping_service(), "ping_next": 0.0, "fields": {}, "field_said": [], "alerted": set(),
                       "atlas_traps": [], "atlas_ver": 0, "atlas_done": -1, "atlas_map": None, "pause_want": None})
            # No verdict survives a restart.
            verdicts.clear()
            load_settings()
            load_fields()
            # Listed on Settings > Alerts.
            HOST.alert_kind(ALERT_TRAP, "New trap in range", 0x1EF)
            load_view()
            Kit.hook_once(st, "hooked", ("OnItemCreated", on_ground_item), ("OnPositionChanged", on_moved))
            # Folded into the Action Bar when the module was left.
            if HOST.dock_wanted(KEY):
                st["minimized"] = True
            build_window()
            wnd.dock(fit=True, min=(320, H))

        def _tick():
            """Client tick of the Traps & Fields part: apply Pause, queued buttons, the scan, pings and the pulse.

            Runs on the client thread, so nothing in it may wait; the scan's reads and recolours all run in
            place. Does nothing while paused.
            """
            if win["g"] is None:
                return
            if Kit.closed(win):
                return
            # The settings page's Paused box, handed over to the tick.
            want = st["pause_want"]
            if want is not None:
                st["pause_want"] = None
                if want != st["paused"]:
                    st["paused"] = want
                    if want:
                        restore_all()
                        # Traps found again after Resume are queued again.
                        st["ping_wait"] = []
                    else:
                        st["last_scan"] = 0.0
                    save_view()
                    refresh()
            while st["queue"]:
                action = st["queue"].pop(0)
                if not wnd.action(action):
                    ACTIONS[action]()
            if st["paused"]:
                return
            now = time.time()
            gap = now - st["last_scan"]
            # Scan when you moved, when the slow timer is due, or soon after a poke. A burst of steps only
            # sets one flag, so it gives one scan.
            if gap >= SCAN_IDLE or (st["moved"] and gap >= SCAN_MOVE) or (st["poke"] and gap >= POKE_GAP):
                st["last_scan"] = now
                st["poke"] = st["moved"] = False
                before = (len(st["tracked"]), len(st["fields"]))
                scan()
                svc = ping_service()
                # Redraw when the counts changed or Map Pings was switched on or off.
                if (len(st["tracked"]), len(st["fields"])) != before or (svc is None) != (st["ping_svc"] is None):
                    st["ping_svc"] = svc
                    if svc is not None:
                        st["ping_noted"] = False
                    refresh()
                # The World Map markers are only made again when a trap was added.
                if st["atlas_ver"] != st["atlas_done"]:
                    st["atlas_done"] = st["atlas_ver"]
                    atlas_publish()
            send_pings()
            pulse()

        def on_ground_item(*args):
            """Client event OnItemCreated: ask for an early scan when the new item is a trap or field graphic.

            Cheap on purpose: it only sets a flag, and does nothing while paused, shutting down or already
            poked.
            """
            if st["poke"] or st["paused"] or st["shutting"]:
                return
            for a in args:
                try:
                    g = int(a.Graphic)
                except Exception:
                    continue
                if g in VERDICT_SIG["wanted"] or (settings["fields"] and g in FIELD_GFX):
                    st["poke"] = True
                return

        def on_moved(*args):
            """Script event: your position changed. Only sets a flag; the next tick scans."""
            st["moved"] = True

        def _stop():
            """Module stop: put every hue back, save the settings and close the cleanup."""
            st["shutting"] = True
            restore_all()
            save_settings()
            cleanup.close()

        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": build_config, "poll_config": poll_config, "config_closed": config_closed}

    # The five parts in order, each with its builder, tick interval and the old key it replaces. The
    # parts that draw on TazUO's World Map are wrapped with it (with_atlas).
    PARTS = (("pings", _part_pings, 0.05, "pings"),
        ("corpse", lambda: with_atlas(_part_corpse(), "corpse"), 0.25, "corpserun"),
        ("maps", lambda: with_atlas(_part_maps(), "maps"), 0.2, "treasure"),
        ("dry", lambda: with_atlas(_part_dry(), "dry"), 0.2, "harvest"),
        ("traps", lambda: with_atlas(_part_traps(), "traps"), 0.1, "traphl"),)
    return PartSet(KEY, TITLE, PARTS, shared=SHARED).hooks()


# Run on its own (no mother script): load the stand-alone host, which stands in for the mother.
if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
# Registers the module with the mother: key, caption, one-line summary, builder, interval, category,
# and the five parts that can be switched on one by one, with the old names the module answers to.
HOST.add("worldmap", "World Map", "Pings, corpse, dig and dry spots, traps",
         _module_worldmap, 0.05, category="The world", parts=(
             ("pings", "Map Pings", "Guild pings on your Enhanced Map", False, ("pings",)),
             ("corpse", "Corpse", "Arrow, decay time and Get my things", False, ("corpserun",)),
             ("maps", "Treasure Maps", "Dig spots of your decoded maps", False, ("treasure",)),
             ("dry", "Ore Tracker", "Your weight and spots that ran dry", False, ("harvest",)),
             ("traps", "Traps & Fields", "Traps and magic fields recoloured", False, ("traphl",)),),
         aliases=('Map Pings', 'Corpse Run', 'Treasure Hunter', 'Harvest Helper', 'Dry spots',
                  'Ore Tracker', 'Trap Highlight', 'Enhanced Map', 'tracking arrow', 'ping',
                  'corpse', 'dig spot', 'weight bar', 'TazUO World Map'))
