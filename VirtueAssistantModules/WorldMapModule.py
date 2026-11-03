# =============================================================================
#  World Map  -  a Virtue Assistant module (TazUO Legion Script, Python)
#  Shard: In Mani Ylem
#
#  This file is NOT a script to run on its own. It is one module of Virtue
#  Assistant, loaded by Virtue Assistant from LegionScripts/VirtueAssistantModules.
#  Virtue Assistant provides everything this file uses (API, G, safe, Client,
#  Kit, Follow, HOST, Journal, the main loop and the settings window), so run
#  that instead and tick World Map on its Modules tab.
#
#  To leave this module out, take this file out of the folder.
#  Module key: "worldmap"
#
#  A module made of PARTS (2.6.5): each part below was a module of its own in
#  2.6.06 and keeps every saved key, window place, list and file it had. A
#  part has its own box under the module's row on the Modules tab (click the
#  arrow on the row to see them) and runs only while it is ticked; the mother
#  script's PartSet runs the ticked parts side by side. The old module keys
#  still answer (the Action Bar's mod: cells, HOST.enable, HOST.by_key).
#
#     Map Pings        (was MapPings)         Send and receive guild pings on your Enhanced Map
#     Corpse           (was CorpseRun)        An arrow to your corpse, how long it lasts, and Get my things
#     Treasure Maps    (was TreasureHunter)   The dig spots of your decoded treasure maps
#     Ore Tracker      (was HarvestHelper)    Your weight, and the ore, wood, fish and sand spots that ran dry
#                      (called "Dry spots" in 2.6.5; renamed in 2.6.51, same key "dry" / "harvest")
#     Traps & Fields   (was TrapHighlight)    Traps and magic fields recoloured so you see them
#
#  Map Pings starts first: the other parts send their pings through its
#  pings.send service, as they did in 2.6.06.
#
#  2.6.82: speed pass: one open-window walk per 0.5 s for every part; Traps &
#  Fields keeps each ground item's verdict; Corpse looks for bones by graphic.
# =============================================================================


def _module_worldmap():
    """Builds the module from its parts and returns its hooks."""
    KEY = "worldmap"
    TITLE = "World Map"

    # =========================================================================
    #  The Atlas (2.6.51): the parts' places on TazUO's own World Map.
    #
    #  What a Legion script can do there (TazUO-main, LegionAPI.cs and
    #  WorldMapGump.cs): API.AddMapMarker(name, x, y, map, color) and
    #  API.RemoveMapMarker(name). Both work only while TazUO's World Map is
    #  open (otherwise they do nothing), and both go through TazUO's own user
    #  markers file (Data/Client/userMarkers.usr): an added marker is written
    #  there and so is still on the map after it is closed and opened again,
    #  and a removal rewrites the file. There is no other way in for a script
    #  (no layer, icon or line of our own, no click on a marker), so each part
    #  shows as named, coloured user markers:
    #     Corpse         "VA Your corpse" (white)
    #     Treasure Maps  "VA Dig L<level> #<map>" (yellow), each decoded map not dug up
    #     Ore Tracker    "VA <Ore|Wood|Fish|Sand> dry <x> <y>" (blue), the most recent
    #     Traps          "VA Trap <x> <y>" (red), the most recent traps seen this session
    #  Map Pings already put each ping on the World Map (since 2.4), unchanged.
    #  Magic fields are left off: a field lasts seconds and every marker change
    #  is a write to TazUO's file.
    #
    #  How it keeps the map right: each part says what it wants shown
    #  (ATLAS.set(owner, {name: (x, y, facet, color)})); nothing touches the
    #  client while that matches what is on the map. Otherwise, about every
    #  second it looks whether the World Map is open (one walk over the open
    #  windows) and, once it has been open ATLAS_SETTLE seconds (TazUO reads
    #  its marker files as the map opens), removes and adds ATLAS_OPS markers
    #  a pass. The names it put there are kept (Global persistent var), so
    #  markers left behind when the script stopped with the map closed are
    #  taken out of TazUO's file the next time (by exact name: the player's
    #  own markers are never touched). Each part has "Show on TazUO's World
    #  Map" in a TAZUO'S WORLD MAP section of its settings page, drawn by the
    #  part itself (atlas_section) just before its DEBUG section (on at first).
    # =========================================================================
    ATLAS_PREFIX = "VA "
    ATLAS_PLACED_KEY = "WorldMap_atlas_placed"   # Global: names in TazUO's user markers file
    ATLAS_ON_KEY = "WorldMap_atlas"              # per character: "corpse=1;maps=1;dry=1;traps=1"
    ATLAS_OWNERS = (("corpse", "your corpse"), ("maps", "your dig spots"),
                    ("dry", "the spots that ran dry"), ("traps", "the traps you have seen"))
    ATLAS_CHECK = 1.0          # seconds between looks for the World Map while something waits
    ATLAS_CLOSED_CHECK = 2.5   # the same while the map is closed (2.6.82; ATLAS_SETTLE waits 2 s anyway)
    GUMP_EVERY = 0.5           # seconds an open-window walk is reused by the parts (2.6.82)
    ATLAS_SETTLE = 2.0         # seconds the map has been open before markers are written
    ATLAS_OPS = 3              # marker adds / removes per pass at most (each one is a file write)
    ATLAS_CAP = 60             # markers of ours on the map at most
    ATLAS_COLORS = ("red", "green", "blue", "purple", "black", "yellow", "white")
    ATLAS_H = 66               # the "TAZUO'S WORLD MAP" section of a part's page (one check row)

    # One walk over the client's open windows serves every caller for GUMP_EVERY
    # (2.6.82): the Atlas, Map Pings' markers and the tracking-arrow checks of
    # Treasure Maps and Ore Tracker each walked them on their own before, up to
    # four times a second. A walk stops once both windows are found.
    GUMPS = {"at": -1.0, "ok": False, "map": False, "arrow": False}
    GUMP_TYPE = []             # UIManager's type, looked up once

    def gump_flags(fresh=False):
        """{"ok", "map", "arrow"}: TazUO's World Map / a tracking arrow open, as
        of a walk at most GUMP_EVERY old (fresh: walk now); ok False when the
        windows could not be read."""
        memo = GUMPS
        now = time.time()
        if not fresh and 0.0 <= now - memo["at"] < GUMP_EVERY:
            return memo
        memo["at"] = now
        mp = ar = False
        try:
            if not GUMP_TYPE:
                GUMP_TYPE.append(Tz.T("ClassicUO.Game.Managers.UIManager"))
            for w in list(Tz.get(None, "Gumps", GUMP_TYPE[0])):
                n = str(w.GetType().Name)
                if n == "WorldMapGump":
                    mp = True
                    if ar:
                        break
                elif n == "QuestArrowGump":
                    ar = True
                    if mp:
                        break
            memo["ok"] = True
        except Exception:
            memo["ok"] = False
        memo["map"], memo["arrow"] = mp, ar
        return memo

    class Atlas(object):
        def __init__(self):
            self.items = {}        # owner -> {name: (x, y, facet, color)}
            self.on = {}           # owner -> shown on the map (the part's page)
            self.placed = {}       # name -> (x, y, facet, color) written to TazUO's file
            self.want = {}         # what should be on the map now (the owners that are on)
            self.synced = True     # want == placed: nothing to do
            self.open_since = None
            self.next_check = 0.0
            self.saved = None      # the placed text last saved
            self.loaded = False
            self.strip_pending = False   # markers left in TazUO's file: thread_work strips them
            self.loose = set()           # other names to take out of that file: Map Pings' markers
            #                              still on the map when it stopped with the map closed (2.6.81)

        # ---- what the parts call ----
        def load(self):
            if self.loaded:
                return
            self.loaded = True
            for part in Kit.get_var(ATLAS_ON_KEY).split(";"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    self.on[k.strip()] = v.strip() != "0"
            try:
                text = str(API.GetPersistentVar(ATLAS_PLACED_KEY, "", API.PersistentVar.Global) or "")
            except Exception:
                text = ""
            for line in text.split("\n"):
                p = line.split("|")
                if len(p) == 5 and p[0].startswith(ATLAS_PREFIX):
                    try:
                        self.placed[p[0]] = (int(p[1]), int(p[2]), int(p[3]), p[4])
                    except ValueError:
                        pass
            self.saved = text
            # left behind when the script last stopped: taken out of TazUO's file by
            # thread_work on the script's thread (2.6.81: load runs on the client
            # thread, where a file read and write is a frame hitch)
            self.strip_pending = bool(self.placed) and not self.map_open(True)
            self._rebuild()

        def is_on(self, owner):
            self.load()
            return self.on.get(owner, True)

        def set_on(self, owner, on):
            self.load()
            if self.on.get(owner, True) != bool(on):
                self.on[owner] = bool(on)
                Kit.put_var(ATLAS_ON_KEY, ";".join(
                    "%s=%d" % (k, 1 if self.on.get(k, True) else 0) for k, _w in ATLAS_OWNERS))
                self._rebuild()

        def set(self, owner, items):
            """The markers owner wants shown now: {name: (x, y, facet, color)}.
            Names start with ATLAS_PREFIX and hold no comma (TazUO's file is CSV)."""
            self.load()
            if self.items.get(owner) != items:
                self.items[owner] = dict(items)
                self._rebuild()

        def clear(self, owner):
            if self.items.pop(owner, None):
                self._rebuild()

        def _rebuild(self):
            want = {}
            for owner, items in self.items.items():
                if self.on.get(owner, True):
                    for name, v in items.items():
                        if len(want) >= ATLAS_CAP:
                            break
                        want[name] = v
            self.want = want
            self.synced = want == self.placed

        # ---- the module's tick (client thread) ----
        def map_open(self, fresh=False):
            """TazUO's World Map is open (False when it can't be told); from the
            shared walk (gump_flags, 2.6.82), fresh for the rare callers that act
            on the answer at once (stop, the file strip, a new marker)."""
            f = gump_flags(fresh)
            return f["ok"] and f["map"]

        def tick(self):
            if self.synced or self.strip_pending:    # (placed is not touched mid-strip)
                return
            now = time.time()
            if now < self.next_check and self.next_check - now <= ATLAS_SETTLE + ATLAS_CHECK:
                return                               # (a wait longer than that: the clock went back)
            if not self.map_open():
                self.open_since = None
                self.next_check = now + ATLAS_CLOSED_CHECK   # (closed: a slower look, 2.6.82)
                return
            if self.open_since is None or self.open_since > now:
                self.open_since = now
            if now - self.open_since < ATLAS_SETTLE:
                self.next_check = self.open_since + ATLAS_SETTLE
                return
            if not self.map_open(True):              # (2.6.83) every op below needs the map
                self.open_since = None               # open now: the shared walk can be 0.5 s old
                self.next_check = now + ATLAS_CLOSED_CHECK
                return
            self.next_check = now + 0.25             # the next few, a quarter second apart
            ops = 0
            for name in list(self.placed):
                if ops >= ATLAS_OPS:
                    break
                if self.want.get(name) != self.placed[name]:
                    try:
                        API.RemoveMapMarker(name)
                    except Exception:
                        pass
                    del self.placed[name]
                    ops += 1
            for name, v in self.want.items():
                if ops >= ATLAS_OPS:
                    break
                if name not in self.placed:
                    try:
                        API.AddMapMarker(name, v[0], v[1], v[2], v[3])
                    except Exception:
                        pass
                    self.placed[name] = v
                    ops += 1
            self.synced = self.want == self.placed
            self._save()

        def strip_names(self, names):
            """Map Pings stopped with its markers still in TazUO's file and the map
            closed: thread_work (or shutdown, when the whole module stops first)
            takes them out, by exact name (2.6.81)."""
            self.loose.update(names)

        def thread_work(self):
            """Script thread (the module's thread_tick): strip the markers left in
            TazUO's file by the last run, while the map is still closed, and Map
            Pings' leftovers (2.6.81)."""
            if not self.strip_pending and not self.loose:
                return
            # the open windows are read on the client thread (one hop; this thread may wait)
            is_open = Kit.on_client(self._map_open_now)
            if self.strip_pending:
                if not is_open and self._strip_file():
                    self.placed.clear()
                    self._save()
                self.strip_pending = False       # map open (tick removes them) or the strip failed
                self.synced = self.want == self.placed
            if self.loose:
                if is_open:
                    for name in list(self.loose):
                        try:
                            API.RemoveMapMarker(name)
                        except Exception:
                            pass
                else:
                    self._strip_file()           # (placed is empty or already gone from the file)
                self.loose.clear()               # one try: never a loop on a failing file

        def _map_open_now(self):
            return self.map_open(True)

        def _save(self):
            text = "\n".join("%s|%d|%d|%d|%s" % (n, v[0], v[1], v[2], v[3])
                             for n, v in sorted(self.placed.items()))
            if text != self.saved:
                self.saved = text
                try:
                    API.SavePersistentVar(ATLAS_PLACED_KEY, text, API.PersistentVar.Global)
                except Exception:
                    pass

        def shutdown(self):
            """The module stops: our markers come off TazUO's map. With the map
            open through its API; with it closed, out of TazUO's user markers
            file (it is read again when the map opens), by exact name."""
            self.items.clear()
            self.want = {}
            self.strip_pending = False           # (done here now, if still to do)
            if not self.placed and not self.loose:
                self.synced = True
                return
            if self.map_open(True):
                for name in list(self.placed) + list(self.loose):
                    try:
                        API.RemoveMapMarker(name)
                    except Exception:
                        pass
                self.placed.clear()
            elif self._strip_file():
                self.placed.clear()
            self.loose.clear()
            self.synced = not self.placed
            self._save()

        def _strip_file(self):
            """Take our lines out of TazUO's userMarkers.usr (map closed). True when
            the file has none of them now (or there is no file)."""
            try:
                exe = str(Tz.get(None, "ExecutablePath", Tz.T("ClassicUO.CUOEnviroment")))
            except Exception:
                try:                                 # TazUO's own folder, where its dll is
                    exe = os.path.dirname(str(API.GetType().Assembly.Location))
                except Exception:
                    return False
            folder = os.path.join(exe, "Data", "Client")
            if not os.path.isdir(folder):
                return False                         # not TazUO's folder after all: leave it
            path = os.path.join(folder, "userMarkers.usr")
            if not os.path.exists(path):
                return True
            try:
                import io
                with io.open(path, "r", encoding="utf-8-sig") as f:
                    lines = f.read().splitlines()
                keep = []
                for line in lines:
                    p = line.split(",")
                    if len(p) > 3 and (p[3] in self.placed or p[3] in self.loose):
                        continue
                    keep.append(line)
                if len(keep) != len(lines):
                    with io.open(path, "w", encoding="utf-8") as f:
                        f.write(u"".join(l + u"\n" for l in keep))
                return True
            except Exception:
                return False

    ATLAS = Atlas()

    def atlas_name(text):
        """A marker name: our prefix, no commas (TazUO's file is CSV)."""
        return ATLAS_PREFIX + str(text).replace(",", " ")

    def arrow_open(ident, fresh=False):
        """Is our tracking arrow `ident` still on screen? TazUO's arrow
        (QuestArrowGump, its LocalSerial the id) closes with a right-click and
        nothing tells the script. True when it can't be told (2.6.81). Closed
        only when no arrow at all is up: if arrows are up but none carries our
        id (a build that numbers them its own way) it counts as open, so a
        working arrow is never taken for a closed one. From the shared walk
        (gump_flags, 2.6.82)."""
        f = gump_flags(fresh)
        return f["arrow"] if f["ok"] else True

    ATLAS_BOX = {}             # owner -> its "Show ... on TazUO's World Map" box while its page is open

    def atlas_section(g, x, y, w, owner):
        """The TAZUO'S WORLD MAP section (ATLAS_H high) of a part's settings
        page: the part draws it just before its DEBUG section and counts
        ATLAS_H + Kit.GAP in its config_height; with_atlas polls the box."""
        what = dict(ATLAS_OWNERS).get(owner, owner)
        Kit.add_section(g, x, y, w, ATLAS_H, "TAZUO'S WORLD MAP  (while it is open)")
        ATLAS_BOX[owner] = Kit.add_check(g, "Show %s on TazUO's World Map" % what, x + 12, y + 30,
                                         ATLAS.is_on(owner),
                                         "Puts markers named \"%s...\" on TazUO's World Map while "
                                         "it is open; they come off when this is unticked or the "
                                         "part stops" % ATLAS_PREFIX)

    def with_atlas(api, owner):
        """A part's hooks with the TAZUO'S WORLD MAP box of its settings page
        polled (the part draws the section itself with atlas_section) and its
        markers cleared when it stops."""
        old_poll = api.get("poll_config")
        old_closed = api.get("config_closed")
        old_stop = api.get("stop")

        def poll():
            if old_poll:
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
            if old_closed:
                old_closed()
            ATLAS_BOX.pop(owner, None)

        def stop():
            try:
                if old_stop:
                    old_stop()
            finally:
                ATLAS_BOX.pop(owner, None)
                ATLAS.clear(owner)

        out = dict(api)
        out.update({"poll_config": poll, "config_closed": closed, "stop": stop})
        return out

    JOURNAL_NAMES = ("TazUO", "World Map", "Map Pings", "Enhanced Map", "Virtue Assistant",
                     "Settings", "Inventory", "Need help", "Look here", "Go here", "Danger!")

    def journal_case(text):
        """A status or window line as a journal message: its first letter lower
        case, unless it starts with a name (JOURNAL_NAMES) or a tag in brackets."""
        text = str(text or "")
        if not text or text[0] in "[(\"'" or text.startswith(JOURNAL_NAMES):
            return text
        return text[0].lower() + text[1:]


    def _dock_hooks(*args, **kw):
        """Kit.dock_hooks with the 2.6.55 zone-fit keywords (scale=True: the
        layout may scale the window, which is rebuilt whole and never moves a
        control after building), or without them on an older mother."""
        try:
            return Kit.dock_hooks(*args, **kw)
        except TypeError:
            return Kit.dock_hooks(*args)


    def _part_pings():
        """Builds the module in its own namespace and returns its hooks."""
        # =============================================================================
        #  MODULE: Map Pings  (from Enhanced Map Pings v1.6)
        #  Shared pings between guildmates, through your Enhanced Map server.
        #
        #  Login: uses TazUO's own Enhanced Map connection (Options > Enhanced Map),
        #  so there is nothing extra to log in to. If that's turned off, enter a
        #  separate map login on the World Map settings page (SEPARATE MAP LOGIN).
        #
        #  Send a ping:  hold the MOUSE WHEEL down over a spot, drag in a direction,
        #                and let go:   up = Look here   right = Danger!
        #                              down = Go here   left = Need help
        #                (let go without dragging to cancel)
        #             or click a ping button on the settings page (SEND A PING) or
        #                press a hotkey, then click a spot, item or person with the
        #                target cursor.
        #  Hotkeys:      CTRL+1 Look here   CTRL+2 Danger!   CTRL+3 Go here   CTRL+4 Need help
        #
        #  Works with Enhanced Map users too: their pings show here, yours show on
        #  their maps.
        #
        #  Other modules can send a ping of yours through HOST.services["pings.send"]
        #  (2.6.02): Traps & Fields uses it to put a Danger! ping on each trap it finds.
        #
        #  Ping history (2.6.05): the History button on the settings page opens a
        #  window listing the recent pings, yours and other people's (kind, who,
        #  when, where). Click a row to put the tracking arrow on that spot again
        #  (click it again to take the arrow off); Alt+click a row of someone in
        #  range to auto-follow them.
        # =============================================================================
        TITLE = "Map Pings"

        # ---- Only used for a separate login (when TazUO's Enhanced Map is off) ----------
        DEFAULT_SERVER = ""          # e.g. "mymapserver.example.com" or "203.0.113.7"
        DEFAULT_PORT = 8887

        # ---- Options --------------------------------------------------------------------
        HOTKEYS = {                  # defaults; rebind them on the settings page ("" = none)
            "look": "CTRL+1",
            "danger": "CTRL+2",
            "go": "CTRL+3",
            "help": "CTRL+4",
        }
        HOTKEY_ORDER = ("look", "danger", "go", "help")
        MOUSE_GESTURE = True         # hold the mouse wheel and drag to ping (see top of file)
        GESTURE_DIRECTIONS = {       # which ping each drag direction sends
            "up": "look",
            "right": "danger",
            "down": "go",
            "left": "help",
        }
        GESTURE_MIN_DRAG = 25        # pixels you must drag before a direction counts (default;
                                     #   "Drag distance" on the settings page)
        PING_SECONDS = 8             # how long a ping stays on screen (default; "Ping stays" on
                                     #   the settings page)
        DRAG_MIN, DRAG_MAX = 5, 200          # limits of the drag distance field
        PING_SECS_MIN, PING_SECS_MAX = 2, 60  # limits of the ping seconds field
        MAP_MARKER_SECONDS = 60      # how long a ping stays on the world map (if open)
        MARKERS_CAP = 60             # ping markers kept to take off again at most (2.6.81)
        MAX_PINGS_SHOWN = 12         # pings kept on screen at once (the oldest goes first)
        PING_RATE_SECS = 0.75        # your own pings are sent at most this often
        SOUND_GAP_SECS = 0.3         # never more than one ping sound this often
        POSITION_READ_EVERY = 0.5    # separate login: how often your position is read for sharing
        SEND_TIMEOUT = 5             # seconds a socket write may take (on the sender thread)
        CONNECTION = "auto"          # "auto":  use TazUO's Enhanced Map connection when it's on,
                                     #          otherwise a separate login (Settings tab)
                                     # "tazuo": only ever use TazUO's connection
                                     # "own":   always use a separate login
        SHARE_POSITION = True        # separate login only: show you on guildmates' Enhanced Maps
                                     #   (TazUO's connection already does this itself)
        SEND_LEGACY_ALERT = True     # also send each ping as "alerts", so it works on map servers
                                     #   without the ping update (type and facet are tucked into the
                                     #   alert, other copies of this script decode them), and so it
                                     #   shows in TazUO's own map overlay. Duplicates are dropped.
        SEND_PING_PACKET = "auto"    # "auto": on TazUO's connection, send the ping packet (0x33) only
                                     #   once the server has relayed one (servers without the ping
                                     #   update may drop you for it); "always": send it every time
        PLAY_SOUNDS = True           # play a sound for each ping (yours and other people's)
        PING_SOUNDS = {              # UO sound ids (same numbers a UO server uses); 0 = silent
            "look": 0x1EA,           #   Bless spell: bright chime
            "danger": 0x307,         #   Explosion spell: sharp boom
            "go": 0x1FC,             #   Recall spell: travel whoosh
            "help": 0x202,           #   Greater Heal spell: healing tone
        }
        NAME_COLOR = 0xFFFFD700      # your name colour on Enhanced Maps (ARGB)
        HISTORY_MAX = 200            # pings kept in the history window's list (oldest dropped)
        HISTORY_ROWS = 10            # rows per page of the history window
        HISTORY_ICON = 0x14EB        # item art (a map) on the Action Bar's tray button when the
                                     #   history window is folded into the bar
        DEBUG = False                # True = print connection details to the journal (for troubleshooting)

        # =============================================================================
        #  Nothing below needs changing.
        # =============================================================================

        try:
            import socket
            import select
            _HAVE_PY_SOCKET = True
        except Exception:
            _HAVE_PY_SOCKET = False
        import collections

        VAR_PREFIX = "EMPings."
        JPFX = TITLE + ": "             # every journal line of this part starts with this

        LOOK, DANGER, GO, HELP = 0, 1, 2, 3
        TYPE_KEYS = {"look": LOOK, "danger": DANGER, "go": GO, "help": HELP}

        TYPE_INFO = {
            #        label        UO hue  effect gfx  world-map colour
            LOOK:   ("Look here", 53,     0x373A,     "yellow"),
            DANGER: ("Danger!",   33,     0x3709,     "red"),
            GO:     ("Go here",   68,     0x376A,     "green"),
            HELP:   ("Need help", 88,     0x375A,     "blue"),
        }

        FACETS = ["Felucca", "Trammel", "Ilshenar", "Malas", "Tokuno", "Ter Mur"]

        ARROW_ID = 0x50494E47        # "PING"; one tracking arrow for the newest ping


        def label_of(t):
            return TYPE_INFO.get(t, TYPE_INFO[LOOK])[0]


        def facet_name(m):
            return FACETS[m] if 0 <= m < len(FACETS) else "map %d" % m


        def direction(dx, dy):
            """Compass direction in UO terms (+x east, +y south)."""
            if dx == 0 and dy == 0:
                return "here"
            deg = math.degrees(math.atan2(-dy, dx))
            if deg < 0:
                deg += 360
            return ["E", "NE", "N", "NW", "W", "SW", "S", "SE"][int(round(deg / 45.0)) % 8]


        # =============================================================================
        #  Enhanced Map server protocol
        #  Every packet: id (1 byte), total length (2 bytes, little endian), payload.
        # =============================================================================

        def packet(pid, payload=b""):
            return struct.pack("<BH", pid, 3 + len(payload)) + payload


        def pk_login(user, password):
            u, p = user.encode("latin-1", "replace"), password.encode("latin-1", "replace")
            return packet(0x1F, struct.pack("<BB", len(u), len(p)) + u + p)


        def pk_ping(x, y, m, t):
            return packet(0x33, struct.pack("<HHBB", x & 0xFFFF, y & 0xFFFF, m & 0xFF, t & 0xFF))


        def pk_alert(x, y):
            return packet(0x27, struct.pack("<HH", x & 0xFFFF, y & 0xFFFF))


        # Old map servers only relay "alerts", which carry nothing but x and y (16 bits each).
        # UO coordinates never need the top bits (maps are at most 7168 x 4096), so the ping
        # type and facet ride in those spare bits:
        #   x: bit 15 = marker, bits 13-14 = ping type, bits 0-12 = x (< 8192)
        #   y: bit 15 = marker, bits 12-14 = facet,     bits 0-11 = y (< 4096)
        # Plain alerts from anyone else never have bit 15 set.
        TYPED_ALERT_FLAG = 0x8000


        def encode_typed_alert(x, y, m, t):
            if not (0 <= x < 0x2000 and 0 <= y < 0x1000 and 0 <= m < 8 and 0 <= t < 4):
                return None
            return (TYPED_ALERT_FLAG | (t << 13) | x, TYPED_ALERT_FLAG | (m << 12) | y)


        def decode_typed_alert(ax, ay):
            """(x, y, map, type) if this alert carries a tucked-in ping, else None."""
            if not (ax & TYPED_ALERT_FLAG and ay & TYPED_ALERT_FLAG):
                return None
            return ax & 0x1FFF, ay & 0x0FFF, (ay >> 12) & 0x7, (ax >> 13) & 0x3


        def pk_typed_alert(x, y, m, t):
            enc = encode_typed_alert(x, y, m, t)
            return pk_alert(enc[0], enc[1]) if enc else None


        def pk_keepalive():
            return packet(0xFE)   # unknown to the server: ignored, but resets its idle timer


        def pk_player_data(pos, stats, flag, color):
            """pos (x, y, map); stats (hp, stam, mana, maxhp, maxstam, maxmana)."""
            body = struct.pack("<HHB", pos[0] & 0xFFFF, pos[1] & 0xFFFF, pos[2] & 0xFF)
            body += struct.pack("<HHHHHH", *[max(0, min(v, 0xFFFF)) for v in stats])
            body += struct.pack("<BBBI", flag, 0, 0, color & 0xFFFFFFFF)   # flag, 0, panic (off), name colour
            body += struct.pack("<B", 5) + b"Arial"                          # font
            body += struct.pack("<fB", 12.0, 1)                              # size, bold
            return packet(0x25, body)


        class Reader(object):
            def __init__(self, data, offset=3):
                self.d = data
                self.p = offset

            def need(self, n):
                if self.p + n > len(self.d):
                    raise ValueError("short packet")

            def u8(self):
                self.need(1)
                v = self.d[self.p]
                self.p += 1
                return v

            def u16(self):
                self.need(2)
                v = struct.unpack_from("<H", self.d, self.p)[0]
                self.p += 2
                return v

            def ascii(self, n):
                self.need(n)
                v = bytes(self.d[self.p:self.p + n]).decode("latin-1")
                self.p += n
                return v


        # ---- transports: Python sockets, or .NET if the socket module isn't available ----

        class PySocketTransport(object):
            def __init__(self, host, port, timeout):
                self.s = socket.create_connection((host, port), timeout)
                self.s.settimeout(SEND_TIMEOUT)

            def send(self, data):
                self.s.sendall(data)

            def recv(self):
                """Bytes waiting (b"" if none). Raises EOFError when the server closes."""
                r, _, _ = select.select([self.s], [], [], 0)
                if not r:
                    return b""
                data = self.s.recv(8192)
                if not data:
                    raise EOFError()
                return data

            def close(self):
                try:
                    self.s.close()
                except Exception:
                    pass


        class DotNetTransport(object):
            def __init__(self, host, port, timeout):
                import clr  # noqa: F401  (IronPython only)
                from System.Net.Sockets import TcpClient, SelectMode
                self._select_read = SelectMode.SelectRead
                from System import Array, Byte
                self._Array, self._Byte = Array, Byte    # imported once, not per call (2.6.82)
                self.c = TcpClient()
                task = self.c.ConnectAsync(host, port)
                if not task.Wait(int(timeout * 1000)) or not self.c.Connected:
                    self.c.Close()
                    raise IOError("timed out")
                self.st = self.c.GetStream()
                self.st.WriteTimeout = int(SEND_TIMEOUT * 1000)

            def send(self, data):
                buf = self._Array[self._Byte](bytearray(data))
                self.st.Write(buf, 0, len(buf))

            def recv(self):
                if not self.c.Connected:
                    raise EOFError()
                n = self.c.Available
                if n <= 0:
                    if self.c.Client.Poll(0, self._select_read):
                        raise EOFError()  # readable with nothing to read = closed
                    return b""
                buf = self._Array.CreateInstance(self._Byte, n)
                got = self.st.Read(buf, 0, n)
                if got <= 0:
                    raise EOFError()
                return bytes(bytearray(buf)[:got])

            def close(self):
                try:
                    self.c.Close()
                except Exception:
                    pass


        def open_transport(host, port, timeout=5):
            if _HAVE_PY_SOCKET:
                try:
                    return PySocketTransport(host, port, timeout)
                except (socket.timeout, socket.gaierror, ConnectionError, OSError):
                    raise
                except Exception:
                    pass  # socket module broken in this runtime: try .NET
            return DotNetTransport(host, port, timeout)


        class Sender(object):
            """Writes to a transport on a thread of its own. A send used to run on
            the script's thread (thread_step) with a 5 s socket timeout, so a
            stalled map server stalled every module's thread work for up to 5 s
            per packet. Now send() only queues the bytes; the worker writes them
            and the first error is picked up by MapConnection.poll (which drops
            the connection). Without threads the writes happen in place."""

            def __init__(self, transport):
                self.t = transport
                self.error = None
                self.stopped = False
                self.q = collections.deque()
                self.cond = None
                self.thread = None
                try:
                    import threading
                    self.cond = threading.Condition()
                    th = threading.Thread(target=self._run)
                    th.daemon = True
                    th.start()
                    self.thread = th
                except Exception:
                    self.cond = None            # no threads here: send in place

            def send(self, data):
                if self.error is not None or self.stopped:
                    raise self.error or IOError("sender stopped")
                if self.cond is None:
                    self.t.send(data)
                    return
                with self.cond:
                    self.q.append(data)
                    self.cond.notify()

            def _run(self):
                while not self.stopped:         # (never "while True": the client refuses it)
                    with self.cond:
                        while not self.q and not self.stopped:
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
                self.stopped = True
                if self.cond is not None:
                    with self.cond:
                        self.q.clear()
                        self.cond.notify()


        class MapConnection(object):
            """Talks to EnhancedMapServer. poll() returns a list of events:
               ("status", text, loud), ("ping", name, x, y, map, type), ("alert", name, x, y), ("message", text)
               loud=True means worth a journal line; quiet ones only update the panel."""

            kind = "own"
            owns_position = True
            server_relays_ping = True    # own login: unchanged (a drop here only costs our own login)
            OFF, HANDSHAKE, LOGIN, READY = range(4)
            STATE_NAMES = ["OFF", "HANDSHAKE", "LOGIN", "READY"]

            def __init__(self, host, port, user, password):
                self.host, self.port, self.user, self.password = host, port, user, password
                self.clock = time.time
                self.t = None
                self.state = self.OFF
                self.buf = bytearray()
                self.next_try = 0
                self.backoff = 3
                self.login_failures = 0
                self.kicks = []
                self.gave_up = None
                self.last_sent = 0
                self.state_since = 0
                self.name = user
                self.unreachable_reported = False
                self.ready_since = 0
                self.connecting = None    # a connect running on its own thread (see poll)
                self.sender = None        # the writer thread of the open transport (see Sender)

            # -- lifecycle ---------------------------------------------------------------
            def close(self):
                if self.connecting is not None:   # a connect still running: drop what it opens
                    pend, self.connecting = self.connecting, None
                    pend["abandon"] = True
                    if pend["done"] and pend["t"] is not None:   # it had just finished: close it
                        try:
                            pend["t"].close()
                        except Exception:
                            pass
                if self.sender is not None:
                    try:
                        self.sender.stop()
                    except Exception:
                        pass
                    self.sender = None
                if self.t:
                    self.t.close()
                self.t = None
                self.state = self.OFF
                self.buf = bytearray()

            def _drop(self, events, kind, detail, retry_in):
                """kind: "eof" (server closed), "error", "timeout" or "garbled"."""
                was = self.state
                self.close()
                now = self.clock()
                self._debug(events, "dropped in state %s: %s %s" % (self.STATE_NAMES[was], kind, detail))

                if was == self.LOGIN and kind == "eof":
                    # The server says nothing when it rejects a login; it just closes the connection.
                    self.login_failures += 1
                    if self.login_failures >= 3:
                        self.gave_up = ("The map server closed the connection during login 3 times. Check the "
                                        "map username and password (World Map settings page). If they are "
                                        "right, tick Print debug lines on the Modules tab.")
                        events.append(("status", self.gave_up, True))
                        return
                    events.append(("status", "The server closed the connection during login (usually a wrong "
                                             "username or password). Retrying in %d seconds." % retry_in, True))
                elif was == self.LOGIN:
                    events.append(("status", "Problem while logging in (%s). Retrying in %d seconds." % (detail, retry_in), True))
                elif was == self.READY:
                    if kind == "eof" and now - self.ready_since < 6:
                        why = ("Logged in, but the server dropped the connection right away. Is this map account "
                               "also logged in somewhere else (Enhanced Map, for example)?")
                    elif kind == "eof":
                        why = "Lost connection to the map server."
                    else:
                        why = "Connection problem (%s)." % detail
                    self.kicks = [k for k in self.kicks if now - k < 300] + [now]
                    if len(self.kicks) >= 4:
                        self.gave_up = ("Kept getting disconnected. Is this map account also logged in somewhere else "
                                        "(Enhanced Map, for example)? Use a separate account, then click Reconnect.")
                        events.append(("status", self.gave_up, True))
                        return
                    events.append(("status", "%s Reconnecting in %d seconds." % (why, retry_in), True))
                else:
                    what = {"eof": "The server closed the connection", "timeout": "The server didn't answer"}.get(kind, "Connection problem")
                    events.append(("status", "%s (%s). Retrying in %d seconds." % (what, detail or "handshake", retry_in), False))
                self.next_try = now + retry_in

            def _debug(self, events, text):
                if DEBUG or getattr(HOST, "debug", False):
                    events.append(("status", "[debug] " + text, True))

            def reset(self):
                self.close()
                self.gave_up = None
                self.login_failures = 0
                self.kicks = []
                self.backoff = 3
                self.next_try = 0

            @property
            def ready(self):
                return self.state == self.READY

            # -- sending -----------------------------------------------------------------
            def send(self, data):
                """Queues data for the sender thread (never blocks the script's thread)."""
                if not self.t:
                    return False
                try:
                    if self.sender is not None:
                        self.sender.send(data)
                    else:
                        self.t.send(data)
                    self.last_sent = self.clock()
                    return True
                except Exception:
                    self.close()
                    self.next_try = self.clock() + 3
                    return False

            # -- main pump ---------------------------------------------------------------
            def poll(self):
                events = []
                now = self.clock()

                if self.gave_up:
                    return events

                if self.t is None:
                    if now < self.next_try:
                        return events
                    # Connecting can take up to its 5 s timeout (an unreachable server,
                    # slow DNS); on the script's thread that would stop every module, so
                    # it runs on a thread of its own and is picked up on a later pass.
                    pend = self.connecting
                    if pend is None:
                        pend = self.connecting = {"done": False, "t": None, "err": None, "abandon": False}

                        def run(p=pend, host=self.host, port=self.port):
                            try:
                                p["t"] = open_transport(host, port)
                            except Exception as ex:
                                p["err"] = ex
                            if p["abandon"] and p["t"] is not None:
                                p["t"].close()
                            p["done"] = True
                        try:
                            import threading
                            th = threading.Thread(target=run)
                            th.daemon = True
                            th.start()
                        except Exception:
                            run()                       # no threads here: connect in place
                    if not pend["done"]:
                        return events
                    self.connecting = None
                    now = self.clock()
                    try:
                        if pend["err"] is not None:
                            raise pend["err"]
                        if pend["t"] is None:
                            raise IOError("no connection")
                        self.t = pend["t"]
                    except Exception as e:
                        self.backoff = min(self.backoff * 2, 60)
                        events.append(("status", "Can't reach the map server at %s:%d (%s). Retrying in %d seconds."
                                       % (self.host, self.port, short_error(e), self.backoff), not self.unreachable_reported))
                        self.unreachable_reported = True
                        self.next_try = now + self.backoff
                        return events
                    self.state = self.HANDSHAKE
                    self.state_since = now
                    self.buf = bytearray()
                    try:
                        self.sender = Sender(self.t)       # writes on a thread of their own
                    except Exception:
                        self.sender = None
                    self.send(packet(0x2B, b"\x00"))   # protocol request
                    events.append(("status", "Connecting...", False))

                # read what's waiting
                closed = None   # (kind, detail) if the connection ended during this read
                snd = self.sender
                if snd is not None and snd.error is not None:   # a write failed on the sender thread
                    e = snd.error
                    closed = ("error", "%s: %s" % (e.__class__.__name__, short_error(e)))
                try:
                    # one read per loop (every 50 ms) is plenty, and avoids relying on
                    # select() staying accurate across back-to-back reads in IronPython
                    chunk = self.t.recv() if self.t else b""
                    if chunk:
                        if DEBUG or getattr(HOST, "debug", False):   # (text made only when shown, 2.6.82)
                            self._debug(events, "received %d bytes" % len(chunk))
                        self.buf.extend(chunk)
                        if len(self.buf) > 1 << 20:
                            raise IOError("too much data")
                except EOFError:
                    closed = ("eof", "")
                except Exception as e:
                    closed = ("error", "%s: %s" % (e.__class__.__name__, short_error(e)))

                # handle every complete packet first: the server may have sent its reply
                # just before closing, and that reply says what happened
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
                    if DEBUG or getattr(HOST, "debug", False):
                        self._debug(events, "packet 0x%02X (%d bytes) in state %s" % (pid, size, self.STATE_NAMES[self.state]))
                    try:
                        self._handle(pid, data, events)
                    except ValueError as e:
                        self._debug(events, "skipped malformed packet 0x%02X: %s" % (pid, e))

                if closed and self.t is not None:
                    self._drop(events, closed[0], closed[1], 30 if self.state == self.LOGIN else 10)
                    return events

                # handshake taking too long
                if self.t is not None and self.state in (self.HANDSHAKE, self.LOGIN) and now - self.state_since > 15:
                    self._drop(events, "timeout", "no reply in 15 s", 15)

                return events

            def _handle(self, pid, data, events):
                r = Reader(data)
                if pid == 0x2B and self.state == self.HANDSHAKE:
                    self.state = self.LOGIN
                    self.state_since = self.clock()
                    self._debug(events, "handshake ok (server protocol %d), sending login for '%s'" % (r.u8(), self.user))
                    self.send(pk_login(self.user, self.password))
                elif pid == 0x1F and self.state == self.LOGIN:
                    if r.u8() == 1:
                        r.u8()  # access level
                        self.name = r.ascii(r.u8()) or self.user
                        self.state = self.READY
                        self.ready_since = self.clock()
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
                # everything else (positions, chat, labels...) is for Enhanced Map; ignore


        def parse_ping(pid, r):
            """0x33 ping or 0x27 alert as relayed by the server -> event tuple."""
            if pid == 0x33:
                x, y, m, t = r.u16(), r.u16(), r.u8(), r.u8()
                return ("ping", r.ascii(r.u8()), x, y, m, t if t in TYPE_INFO else LOOK)
            x, y = r.u16(), r.u16()
            return ("alert", r.ascii(r.u8()), x, y)


        # =============================================================================
        #  Riding on TazUO's built-in Enhanced Map connection
        #  TazUO has its own Enhanced Map client (Options > Enhanced Map) but doesn't
        #  expose it to scripts, so this reaches it through .NET reflection:
        #    - sends go through its SendRaw (thread-safe, uses its socket lock)
        #    - receives: a handler is added next to TazUO's own OnFrame handler,
        #      and removed again when the script stops
        #  TazUO runs OnFrame on its Enhanced Map network thread, inside the loop
        #  that reads the socket: if a handler throws, TazUO treats it as a broken
        #  connection, drops it and reconnects 10 s later. A Python handler throws
        #  as soon as its script has stopped (Legion shuts the Python runtime
        #  down), so a handler left behind by a stopped run made the connection
        #  drop on the first packet after every reconnect, over and over. Since
        #  2.5.13 the handler is plain .NET (built with System.Linq.Expressions):
        #  it only puts ping/alert frames in a queue, never runs Python and can't
        #  throw, so even one left behind is harmless. Hooking also clears out
        #  any handler on OnFrame that isn't TazUO's own (left by older runs).
        #  If TazUO changes these internals, the script says so and falls back to a
        #  separate login.
        # =============================================================================

        class TazUOBridge(object):
            HOOK_KEY = "EMPings.OnFrameHook"

            def __init__(self, api):
                import clr  # noqa: F401  (IronPython only)
                from System import Array, Byte, Action, Delegate, AppDomain
                from System.Reflection import BindingFlags
                from System.Collections.Concurrent import ConcurrentQueue

                self._Array, self._Byte, self._Delegate, self._AppDomain = Array, Byte, Delegate, AppDomain
                inst = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance
                stat = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static

                mtype = api.GetType().Assembly.GetType("ClassicUO.Game.Managers.EnhancedMap.EnhancedMapManager")
                if mtype is None:
                    raise LookupError("this TazUO has no built-in Enhanced Map")

                p_instance = mtype.GetProperty("Instance", stat)
                self._p_connected = mtype.GetProperty("IsConnected", inst)
                self._p_config = mtype.GetProperty("Config", stat)
                self._m_reconnect = mtype.GetMethod("Reconnect", inst)
                f_client = mtype.GetField("_client", inst)
                if None in (p_instance, self._p_connected, self._p_config, f_client):
                    raise LookupError("TazUO's Enhanced Map internals have changed")

                self._asm = api.GetType().Assembly          # TazUO's own code (see _own_handlers_only)
                self._manager = p_instance.GetValue(None)
                self._client = f_client.GetValue(self._manager)
                ctype = self._client.GetType()
                self._f_connection = ctype.GetField("_connection", inst)
                self._m_send = ctype.GetMethod("SendRaw", inst)
                self._f_onframe = ctype.GetField("OnFrame", inst)
                if None in (self._f_connection, self._m_send, self._f_onframe):
                    raise LookupError("TazUO's Enhanced Map internals have changed")

                try:
                    self._handler, self._queue = self._make_handler()
                    self.handler_kind = ".NET"
                except Exception as e:
                    # Fallback (older .NET without expression compiling): a Python handler.
                    # Fine while the script runs; a stopped run's copy is cleared on the next hook.
                    self.handler_kind = "Python (%s)" % short_error(e)
                    self._queue = ConcurrentQueue[object]()
                    queue = self._queue

                    def on_frame(pid, payload):
                        try:
                            if (pid == 0x33 or pid == 0x27) and queue.Count < 200:
                                queue.Enqueue((int(pid), payload))
                        except Exception:
                            pass

                    self._handler = Action[Byte, Array[Byte]](on_frame)
                self._hooked = False

            @staticmethod
            def _make_handler():
                """A pure .NET Action<byte, byte[]> that queues ping (0x33) and alert (0x27)
                frames, at most 200. It runs on TazUO's network thread and never calls back
                into Python, so it keeps working (harmlessly) after this script stops."""
                import clr
                from System import Array, Byte, Int32, Action, Tuple, Type
                from System.Collections.Concurrent import ConcurrentQueue
                from System.Linq.Expressions import Expression, ParameterExpression
                t_byte, t_bytes, t_int = clr.GetClrType(Byte), clr.GetClrType(Array[Byte]), clr.GetClrType(Int32)
                ftype = Tuple[Byte, Array[Byte]]
                queue = ConcurrentQueue[ftype]()
                p_id = Expression.Parameter(t_byte, "id")
                p_payload = Expression.Parameter(t_bytes, "payload")
                q = Expression.Constant(queue)
                as_int = Expression.Convert(p_id, t_int)
                wanted = Expression.OrElse(Expression.Equal(as_int, Expression.Constant(0x33, t_int)),
                                           Expression.Equal(as_int, Expression.Constant(0x27, t_int)))
                room = Expression.LessThan(Expression.Property(q, "Count"), Expression.Constant(200, t_int))
                ctor = clr.GetClrType(ftype).GetConstructor(Array[Type]([t_byte, t_bytes]))
                enqueue = Expression.Call(q, queue.GetType().GetMethod("Enqueue"),
                                          Array[Expression]([Expression.New(ctor, Array[Expression]([p_id, p_payload]))]))
                body = Expression.IfThen(Expression.AndAlso(wanted, room), enqueue)
                lam = Expression.Lambda[Action[Byte, Array[Byte]]](
                    body, Array[ParameterExpression]([p_id, p_payload]))
                return lam.Compile(), queue

            def hook(self):
                if self._hooked:
                    return
                domain = self._AppDomain.CurrentDomain
                current = self._f_onframe.GetValue(self._client)
                leftover = domain.GetData(self.HOOK_KEY)          # from a run that didn't clean up
                if leftover is not None:
                    current = self._Delegate.Remove(current, leftover)
                current = self._own_handlers_only(current)
                self._f_onframe.SetValue(self._client, self._Delegate.Combine(current, self._handler))
                domain.SetData(self.HOOK_KEY, self._handler)
                self._hooked = True

            def _own_handlers_only(self, current):
                """TazUO's own OnFrame handlers, without any a stopped script left
                behind: those would throw and drop the connection. TazUO's own are
                the ones on its EnhancedMapManager, and (2.5.22) any other handler
                whose code is compiled into TazUO itself (a lambda or a helper class
                of TazUO's): only script-made handlers (IronPython, or the .NET one
                built in _make_handler, both generated at run time) are cleared."""
                if current is None:
                    return None
                try:
                    keep = None
                    for d in current.GetInvocationList():
                        if (d.Target is not None and d.Target.Equals(self._manager)) or self._tazuo_code(d):
                            keep = self._Delegate.Combine(keep, d)
                    return keep
                except Exception:
                    return current

            def _tazuo_code(self, d):
                """True when delegate d runs a method compiled into TazUO's assembly."""
                try:
                    return bool(d.Method.Module.Assembly.Equals(self._asm))
                except Exception:
                    return False

            def unhook(self):
                if not self._hooked:
                    return
                try:
                    current = self._f_onframe.GetValue(self._client)
                    self._f_onframe.SetValue(self._client, self._Delegate.Remove(current, self._handler))
                    self._AppDomain.CurrentDomain.SetData(self.HOOK_KEY, None)
                finally:
                    self._hooked = False

            def config(self):
                c = self._p_config.GetValue(None)
                if c is None:
                    return None
                return {"enabled": bool(c.Enabled), "configured": bool(c.IsConfigured), "user": str(c.Username or ""),
                        "address": str(c.Address or ""), "port": int(c.Port), "send_location": bool(c.SendLocation)}

            def is_connected(self):
                return bool(self._p_connected.GetValue(self._manager))

            def send(self, data):
                conn = self._f_connection.GetValue(self._client)
                if conn is None:
                    return False
                buf = self._Array[self._Byte]([int(b) for b in bytearray(data)])
                self._m_send.Invoke(self._client, self._Array[object]([conn, buf]))
                return True

            def reconnect(self):
                if self._m_reconnect is not None:
                    self._m_reconnect.Invoke(self._manager, None)

            def frames(self):
                out = []
                for _ in range(200):          # the queue never holds more than 200
                    ok, item = self._queue.TryDequeue()
                    if not ok:
                        break
                    if isinstance(item, tuple):          # the Python fallback handler
                        pid, payload = item
                    else:                                # the .NET handler's Tuple<byte, byte[]>
                        pid, payload = item.Item1, item.Item2
                    out.append((int(pid), bytes(bytearray([int(b) for b in payload]))))
                return out


        class TazUOMouse(object):
            """Reads TazUO's mouse state (not exposed to scripts) through reflection:
            middle button, cursor position, and the world object under the cursor."""

            def __init__(self, api):
                import clr  # noqa: F401  (IronPython only)
                from System.Reflection import BindingFlags
                stat = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static
                asm = api.GetType().Assembly
                mouse = asm.GetType("ClassicUO.Input.Mouse")
                selected = asm.GetType("ClassicUO.Game.SelectedObject")
                ui = asm.GetType("ClassicUO.Game.Managers.UIManager")
                if None in (mouse, selected, ui):
                    raise LookupError("TazUO's mouse internals have changed")
                self._pos = mouse.GetField("Position", stat)
                self._mclick = mouse.GetField("MClickPosition", stat)
                self._mdown = mouse.GetProperty("MButtonPressed", stat)
                self._mdown_get = None
                self._over_world = ui.GetProperty("IsMouseOverWorld", stat)
                self._object = selected.GetField("Object", stat)
                if None in (self._pos, self._mclick, self._mdown, self._over_world, self._object):
                    raise LookupError("TazUO's mouse internals have changed")

            def middle_down(self):
                get = self._mdown_get
                if get is None:                          # the bound reader, made once (2.6.82)
                    get = self._mdown_get = self._mdown.GetValue
                return bool(get(None))

            def position(self):
                p = self._pos.GetValue(None)
                return int(p.X), int(p.Y)

            def press_position(self):
                p = self._mclick.GetValue(None)
                return int(p.X), int(p.Y)

            def tile_under_mouse(self):
                """World (x, y) of the ground/item/mobile under the cursor, or None (e.g. over a gump)."""
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
            """Same interface as MapConnection, but rides on TazUO's own login."""
            kind = "tazuo"
            owns_position = False

            DROP_WINDOW = 120            # seconds
            DROP_LIMIT = 3               # drops inside DROP_WINDOW before Map Pings lets go

            def __init__(self, bridge):
                self.bridge = bridge
                self.bridge.hook()
                self.was_connected = None
                self.last_sent = 0
                self.gave_up = None
                self.drops = []
                self.unhooked_for_drops = False
                self.server_relays_ping = False     # set once a 0x33 has come in through it

            @property
            def ready(self):
                try:
                    return self.bridge.is_connected()
                except Exception:
                    return False

            @property
            def name(self):
                try:
                    return (self.bridge.config() or {}).get("user", "")
                except Exception:
                    return ""

            def poll(self):
                events = []
                connected = self.ready
                if connected != self.was_connected:
                    if connected:
                        events.append(("status", "Using TazUO's Enhanced Map login (%s)." % (self.name or "connected"), True))
                    elif self.was_connected:
                        now = time.time()
                        self.drops = [d for d in self.drops if now - d < self.DROP_WINDOW] + [now]
                        if len(self.drops) >= self.DROP_LIMIT and not self.unhooked_for_drops:
                            # Let go of TazUO's connection: if it still keeps dropping, it isn't us.
                            try:
                                self.bridge.unhook()
                            except Exception:
                                pass
                            self.unhooked_for_drops = True
                            events.append(("status", "TazUO's Enhanced Map keeps dropping, so Map Pings stopped "
                                           "listening on it (your pings still go out; others' don't show). If it "
                                           "still drops, the cause is elsewhere. Click Reconnect to listen again.", True))
                        else:
                            events.append(("status", "TazUO's Enhanced Map connection dropped; TazUO will reconnect.", True))
                    else:
                        events.append(("status", "Waiting for TazUO's Enhanced Map to connect...", False))
                    self.was_connected = connected
                try:
                    frames = self.bridge.frames()
                except Exception:
                    frames = []
                for pid, payload in frames:
                    if pid == 0x33:
                        self.server_relays_ping = True
                    try:
                        events.append(parse_ping(pid, Reader(payload, 0)))
                    except ValueError:
                        pass
                return events

            def send(self, data):
                try:
                    ok = self.bridge.send(data)
                except Exception:
                    ok = False
                if ok:
                    self.last_sent = time.time()
                return ok

            def reset(self):
                self.drops = []
                if self.unhooked_for_drops:
                    self.unhooked_for_drops = False
                    try:
                        self.bridge.hook()
                    except Exception:
                        pass
                try:
                    self.bridge.reconnect()
                except Exception:
                    pass

            def close(self):
                try:
                    self.bridge.unhook()
                except Exception:
                    pass


        def short_error(e):
            s = str(e) or e.__class__.__name__
            return s if len(s) < 60 else s[:57] + "..."


        _xy = {}                                     # .NET type -> (X field, Y field), found once


        def xy_fields(t):
            """The public X / Y fields of a client game object type (looked up once
            per type: the ground, a static, an item, a mobile)."""
            got = _xy.get(t)                         # by the type itself (2.6.82: no FullName read)
            if got is None:
                got = _xy[t] = (t.GetField("X"), t.GetField("Y"))
            return got


        def spot_of(obj):
            """World (x, y) of what a target cursor got (land, static, item or
            mobile: the client's own game object), or None (cancelled)."""
            if obj is None:
                return None
            try:
                return int(obj.X), int(obj.Y)
            except Exception:
                pass
            try:                                     # not visible to Python: by reflection
                t = obj.GetType()
                fx, fy = xy_fields(t)
                if fx is not None and fy is not None:
                    return int(fx.GetValue(obj)), int(fy.GetValue(obj))
                px, py = t.GetProperty("X"), t.GetProperty("Y")
                if px is not None and py is not None:
                    return int(px.GetValue(obj, None)), int(py.GetValue(obj, None))
            except Exception:
                pass
            return None


        # =============================================================================
        #  TazUO side
        # =============================================================================

        class Ping(object):
            def __init__(self, sender, x, y, m, t, now, auto=False):
                self.sender, self.x, self.y, self.map, self.type = sender, x, y, m, t
                self.created = now
                self.next_pulse = now
                self.marked = False
                self.auto = auto           # sent for you by another module (a trap ping)
                self.entry = None          # its line in the history (2.6.05)


        class HistEntry(object):
            """One line of the ping history (2.6.05): a ping shown, yours or not."""
            def __init__(self, seq, at, t, who, x, y, m, local):
                self.seq, self.at, self.type, self.who = seq, at, t, who
                self.x, self.y, self.map, self.local = x, y, m, local


        class PingDisplay(object):
            PULSE = 1.4

            def __init__(self, api):
                self.api = api
                self.clock = time.time
                self.pings = []
                self.markers = []          # (expires, name), oldest first
                self.map_at = 0.0          # next look whether TazUO's World Map is open (2.6.81)
                self.map_since = None      # ...open since then (None: closed)
                self.marked = {}           # (x, y, map) -> count, so overlapping pings don't unmark early
                self.arrow_for = None      # the Ping (or HistEntry, 2.6.05) the tracking arrow is on
                self.last_sound = -1.0
                self.history = []          # HistEntry, oldest first, at most HISTORY_MAX (2.6.05)
                self.hist_ver = 0          # bumped when the history changes
                self.hist_seq = 0

            def player(self):
                p = self.api.Player
                try:
                    return int(p.X), int(p.Y), int(self.api.GetMap()), int(p.Serial)
                except Exception:
                    return 0, 0, -1, 0

            def show(self, sender, x, y, m, t, local=False, who=None, auto=False):
                """who: the name shown for a ping of your own (default "You"; a ping
                another module sent for you, Traps & Fields' for example, says so).
                auto: a ping another module sent for you: it never takes the
                tracking arrow (a guildmate's ping keeps it), and when too many
                pings are up the oldest such ping goes first, so a burst of trap
                pings never pushes a guildmate's ping off the screen."""
                now = self.clock()
                p = Ping(sender, x, y, m, t, now, auto)
                self.pings.append(p)
                if len(self.pings) > MAX_PINGS_SHOWN:
                    victim = self.pings[0]
                    for i in range(len(self.pings) - 1):     # never the new one itself
                        if self.pings[i].auto:
                            victim = self.pings[i]
                            break
                    self._expire(victim)

                label, hue, _, mapcolor = TYPE_INFO.get(t, TYPE_INFO[LOOK])
                px, py, pm, serial = self.player()

                if pm == m and px > 0:
                    dist = max(abs(x - px), abs(y - py))
                    where = "on you" if dist == 0 else "%d tiles %s" % (dist, direction(x - px, y - py))
                else:
                    where = "on %s" % facet_name(m)

                who = (who or "You") if local else sender
                # the line keeps the ping's own hue (red for Danger!, like its tile)
                self.api.SysMsg(JPFX + "%s pinged %s %s (%d, %d, %s)." % (
                    "you" if who == "You" else who, label, where, x, y, facet_name(m)), hue)
                self.hist_seq += 1                # the history window's list (2.6.05)
                p.entry = HistEntry(self.hist_seq, now, t, str(who), x, y, m, bool(local))
                self.history.append(p.entry)
                if len(self.history) > HISTORY_MAX:
                    del self.history[:len(self.history) - HISTORY_MAX]
                self.hist_ver += 1
                if not local and serial:
                    self.api.HeadMsg("%s: %s %s" % (sender, label, where), serial, hue)

                if pm == m:
                    key = (x, y, m)
                    self.marked[key] = self.marked.get(key, 0) + 1
                    p.marked = True
                    try:
                        self.api.MarkTile(x, y, hue, m)
                    except Exception:
                        pass
                    if not auto and px > 0 and x > 0 and y > 0 and max(abs(x - px), abs(y - py)) > 2:
                        try:
                            self.api.TrackingArrow(x, y, ARROW_ID)
                            self.arrow_for = p
                        except Exception:
                            pass

                name = ("%s: %s %s" % (who, label, time.strftime("%H:%M:%S"))).replace(",", " ")   # (2.6.84) CSV-safe
                # 2.6.81: kept (to take off again) only when TazUO's World Map is open;
                # with it closed TazUO does nothing with the marker
                if ATLAS.map_open(True):
                    try:
                        self.api.AddMapMarker(name, x, y, m, mapcolor)
                        self.markers.append((now + MAP_MARKER_SECONDS, name))
                    except Exception:
                        pass
                    if len(self.markers) > MARKERS_CAP:   # (the oldest: out of the file later)
                        ATLAS.strip_names([n for _, n in self.markers[:-MARKERS_CAP]])
                        del self.markers[:-MARKERS_CAP]

                self._play_sound(t, now)

            def _play_sound(self, t, now):
                """One sound per ping, but never more than one every SOUND_GAP_SECS (a burst of pings stays bearable)."""
                if not OPT["sounds"] or now - self.last_sound < SOUND_GAP_SECS:
                    return
                sound = 0
                for k, v in TYPE_KEYS.items():
                    if v == t:
                        sound = PING_SOUNDS.get(k, 0)
                        break
                if not sound:
                    return
                self.last_sound = now
                try:
                    self.api.PlaySound(int(sound))
                except Exception:
                    pass

            def update(self):
                if not self.pings and not self.markers:
                    return                     # nothing on screen: nothing to read
                now = self.clock()
                pm = None                      # your facet, read only when a ping pulses
                stay = OPT["ping_secs"]

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
                        try:
                            self.api.CreateEffect(gfx, type=self.api.EffectType.FixedXYZ, hue=hue,
                                                  sourceX=p.x, sourceY=p.y, duration=self.PULSE)
                        except Exception:
                            pass

                # 2.6.81: an expired marker comes off only while the map is open (a
                # removal does nothing with it closed, and the marker stays in TazUO's
                # file); with the map closed it waits for the map to open
                if self.markers and now >= self.markers[0][0] and self._map_ready(now) \
                        and ATLAS.map_open(True):     # (2.6.83) fresh: a removal needs it open
                    while self.markers and now >= self.markers[0][0]:
                        name = self.markers.pop(0)[1]
                        try:
                            self.api.RemoveMapMarker(name)
                        except Exception:
                            pass

            def _map_ready(self, now):
                """TazUO's World Map open for ATLAS_SETTLE s (it reads its marker files
                as it opens); looked at once a second at most (2.6.81)."""
                if now >= self.map_at or self.map_at - now > 2.0:   # (or the clock went back)
                    self.map_at = now + 1.0
                    if ATLAS.map_open():
                        if self.map_since is None or self.map_since > now:
                            self.map_since = now
                    else:
                        self.map_since = None
                return self.map_since is not None and now - self.map_since >= ATLAS_SETTLE

            def _expire(self, p):
                if p in self.pings:
                    self.pings.remove(p)
                if p.marked:
                    key = (p.x, p.y, p.map)
                    left = self.marked.get(key, 1) - 1
                    if left <= 0:
                        self.marked.pop(key, None)
                        try:
                            self.api.RemoveMarkedTile(p.x, p.y, p.map)
                        except Exception:
                            pass
                    else:
                        self.marked[key] = left
                    p.marked = False
                if self.arrow_for is p:
                    try:
                        self.api.TrackingArrow(-1, -1, ARROW_ID)
                    except Exception:
                        pass
                    self.arrow_for = None

            def arrow_entry(self):
                """The history line the tracking arrow points at (a live ping's own
                line, or one put back from the history window), or None."""
                a = self.arrow_for
                if a is None or isinstance(a, HistEntry):
                    return a
                return a.entry

            def arrow_to(self, e):
                """Put the tracking arrow on history line e again (2.6.05)."""
                self.api.TrackingArrow(e.x, e.y, ARROW_ID)
                self.arrow_for = e

            def arrow_off(self):
                if self.arrow_for is not None:
                    try:
                        self.api.TrackingArrow(-1, -1, ARROW_ID)
                    except Exception:
                        pass
                    self.arrow_for = None

            def clear(self):
                # each step guarded: while TazUO is stopping the script, API calls may be cancelled
                for p in list(self.pings):
                    try:
                        self._expire(p)
                    except Exception:
                        if p in self.pings:
                            self.pings.remove(p)
                if self.markers:
                    names = [n for _, n in self.markers]
                    if ATLAS.map_open(True):
                        for name in names:
                            try:
                                self.api.RemoveMapMarker(name)
                            except Exception:
                                pass
                    else:                      # 2.6.81: out of TazUO's file instead
                        ATLAS.strip_names(names)
                self.markers = []
                try:
                    self.api.TrackingArrow(-1, -1, ARROW_ID)
                except Exception:
                    pass


        class Settings(object):
            def __init__(self, api):
                self.api = api
                scope = api.PersistentVar.Server
                self.host = api.GetPersistentVar(VAR_PREFIX + "host", DEFAULT_SERVER, scope).strip()
                try:
                    self.port = int(api.GetPersistentVar(VAR_PREFIX + "port", str(DEFAULT_PORT), scope))
                except ValueError:
                    self.port = DEFAULT_PORT
                self.user = api.GetPersistentVar(VAR_PREFIX + "user", "", scope).strip()
                self.password = api.GetPersistentVar(VAR_PREFIX + "pass", "", scope)

            @property
            def complete(self):
                return bool(self.host and self.user and self.password and 0 < self.port < 65536)

            def save(self):
                scope = self.api.PersistentVar.Server
                for k, v in (("host", self.host), ("port", str(self.port)), ("user", self.user),
                             ("pass", self.password)):
                    self.api.SavePersistentVar(VAR_PREFIX + k, v, scope)


        # =============================================================================
        #  Ping history window (2.6.05)
        # =============================================================================
        HIST_TITLE = "Ping History"
        HIST_DOCK = "pings_history"      # its key in the host's fold-into-the-bar registry
        HIST_POS_KEY = VAR_PREFIX + "history_pos"
        HIST_MIN_KEY = VAR_PREFIX + "history_min"
        HIST_OPEN_KEY = VAR_PREFIX + "history_open"
        HIST_W = 560
        HIST_MINI_W, HIST_MINI_H = 320, 46
        HIST_ROW_H = 24
        HIST_COLS = (("When", 70), ("Ping", 80), ("From", 140))     # then Where: the rest
        HIST_CLOSE_TIP = "Close"                                     # Map Pings stays on
        HIST_TIP = "Put the tracking arrow on this spot (click again to take it down)"
        HIST_TIP_ON = "Take the tracking arrow down"
        HIST_ALT = ". Alt+click: auto-follow (again to stop)"      # on other people's rows
        HIST_TIPS = {(False, True): HIST_TIP, (True, True): HIST_TIP_ON,
                     (False, False): HIST_TIP + HIST_ALT, (True, False): HIST_TIP_ON + HIST_ALT}
        HIST_EMPTY = "No pings yet. Send one with a ping button, a hotkey or the wheel drag."


        class HistoryWindow(object):
            """The recent pings, newest first, a page of HISTORY_ROWS pooled rows.
            Drawn on the client tick (PingApp.step); nothing is drawn while it is
            folded, only the status line while minimized, and the rows only when
            the history, the page or the arrow changed (and once a second for the
            distances, which move as you walk)."""

            def __init__(self, app):
                self.app = app
                # st doubles as the dock hooks' "win" (its "g")
                self.st = {"g": None, "shutting": False, "minimized": False, "docked": False,
                           "queue": []}
                self.queue = Kit.queuer(self.st)
                self.c = {}
                self.store = ({}, {})
                self.rows = []
                self.page = 0
                self.drawn = None          # what the rows were drawn from (see refresh)
                self.next_draw = 0.0
                self.drawn_pos = None      # where you stood when they were (2.6.82)

            # ---- open / close ----
            def start(self):
                st = self.st
                st["shutting"] = False
                st["minimized"] = Kit.load_min(HIST_MIN_KEY) or \
                    bool(safe(lambda: HOST.dock_wanted(HIST_DOCK), False))
                safe(lambda: HOST.dock_add(HIST_DOCK, _dock_hooks(
                    HIST_TITLE, HISTORY_ICON, st, st, self.queue("redraw"), scale=True)))
                if Kit.get_var(HIST_OPEN_KEY, "0") == "1":   # open when Map Pings last stopped
                    self.build()

            def is_open(self):
                return self.st["g"] is not None

            def toggle_open(self):
                """The History button: opens the window, shows it when it is only
                minimized or folded into the bar, closes it when it is shown."""
                st = self.st
                if self.is_open() and not (st["minimized"] or st["docked"]):
                    self.close()
                    return
                st["minimized"] = st["docked"] = False
                safe(lambda: HOST.dock_forget(HIST_DOCK))
                Kit.save_min(HIST_MIN_KEY, False)
                Kit.put_var(HIST_OPEN_KEY, "1")
                self.build()

            def close(self):
                st = self.st
                g = st["g"]
                if g is None:
                    return
                self.save_pos()
                st["g"] = None
                st["docked"] = False
                safe(lambda: HOST.dock_forget(HIST_DOCK))
                Kit.put_var(HIST_OPEN_KEY, "0")
                self.c, self.rows = {}, []
                Kit.dispose(g)

            def shutdown(self):
                st = self.st
                st["shutting"] = True
                safe(lambda: HOST.dock_remove(HIST_DOCK))
                g = st["g"]
                if g is not None:
                    self.save_pos()
                    # folded into the bar is the host's wish (dock_wanted), not "minimized"
                    Kit.save_min(HIST_MIN_KEY, st["minimized"] and not st["docked"])
                    st["g"] = None
                    self.c, self.rows = {}, []
                    Kit.dispose(g)

            def save_pos(self):
                Kit.save_pos(HIST_POS_KEY, self.st["g"])

            def _disposed(self, g):
                def handler(*args):
                    if self.st["g"] is g and not self.st["shutting"]:
                        self.st["g"] = None        # gone some other way: drawn again when asked
                        self.c, self.rows = {}, []
                return handler

            # ---- the window ----
            def full_h(self):
                M = Kit.MARGIN
                return M + 30 + Kit.GAP + 36 + Kit.GAP + 30 + HISTORY_ROWS * HIST_ROW_H + 8 + M

            def build(self):
                st = self.st
                if st["minimized"]:
                    w, h = HIST_MINI_W, HIST_MINI_H
                else:
                    w, h = HIST_W, self.full_h()
                x, y = Kit.load_pos(HIST_POS_KEY, (260, 160), (w, h))
                if Kit.is_open(st["g"]):
                    x, y = st["g"].GetX(), st["g"].GetY()
                old, st["g"] = st["g"], None
                M = Kit.MARGIN
                store, c, rows = ({}, {}), {}, []
                g = G.CreateGump(True, True)
                if st["minimized"]:
                    c["status"] = Kit.mini_bar(g, store, w, h, HIST_TITLE, HIST_DOCK,
                                               self.queue("toggle_min"), close_tip=HIST_CLOSE_TIP)
                else:
                    IW = w - 2 * M
                    Kit.add_window_frame(g, w, h)
                    Kit.title_bar(g, store, w, HIST_TITLE, HIST_DOCK, self.queue("toggle_min"),
                                  self.queue("to_bar"), self.queue("settings"),
                                  close_tip=HIST_CLOSE_TIP)
                    # toolbar: Clear, Arrow off, the pager
                    yt = M + 30 + Kit.GAP
                    Kit.add_section(g, M, yt, IW, 36)
                    bx = M + 12
                    Kit.art_button(g, store, "clear", Kit.ART_CLOSE, bx, yt + 7, "Clear",
                                   "Empty the history (the pings on screen stay)",
                                   on_click=self.queue("clear"))
                    bx += 35 + Kit.text_w("Clear") + 16
                    Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, bx, yt + 7, "Arrow off",
                                   "Take the tracking arrow down", on_click=self.queue("arrow_off"))
                    right = M + IW - 8
                    c["pg"] = Kit.add_label(g, "", right - 100, yt + 10, Kit.HUE_INFO)
                    Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 56, yt + 8, None,
                                   "Previous page (newer pings)", on_click=self.queue(("page", -1)))
                    Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 34, yt + 8, None,
                                   "Next page (older pings)", on_click=self.queue(("page", 1)))
                    # the list: column heads, then the pooled rows
                    yl = yt + 36 + Kit.GAP
                    Kit.add_section(g, M, yl, IW, 30 + HISTORY_ROWS * HIST_ROW_H + 8)
                    cx = M + 12
                    xs = []
                    for head, cw in HIST_COLS:
                        Kit.add_label(g, head, cx, yl + 6, Kit.HUE_TITLE)
                        xs.append((cx, cw))
                        cx += cw + 8
                    Kit.add_label(g, "Where", cx, yl + 6, Kit.HUE_TITLE)
                    where_w = M + IW - 12 - cx
                    c["where_w"] = where_w
                    for k in range(HISTORY_ROWS):
                        ry = yl + 30 + k * HIST_ROW_H
                        r = {"seq": 0, "prev": (0, 0.0), "tip": None, "vis": True, "sig": None}
                        r["labels"] = [Kit.add_label(g, "", xx, ry + 3, Kit.HUE_TEXT)
                                       for xx, _ in xs]
                        r["where"] = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO)
                        r["widths"] = [cw for _, cw in xs]
                        r["catch"] = Kit.catcher(g, M + 6, ry, IW - 12, HIST_ROW_H,
                                                 self.row_click(k), HIST_TIP)
                        rows.append(r)
                Kit.place(g, x, y, w, h)                     # wholly on screen
                self.c, self.store, self.rows = c, store, rows
                st["g"] = g
                G.AddControlOnDisposed(g, self._disposed(g))
                G.AddGump(g)
                safe(lambda: Kit.on_moved(g, self.save_pos))   # saved the moment it is let go
                if st["minimized"] and st["docked"]:         # folded into the Action Bar
                    safe(lambda: setattr(g, "IsVisible", False))
                self.drawn = None
                self.refresh()
                Kit.dispose(old)

            def row_click(self, k):
                def handler(*args):
                    r = self.rows[k] if k < len(self.rows) else None
                    if r is None:
                        return
                    seq = r["seq"]
                    prev, at = r["prev"]
                    if prev and time.time() - at < 0.15:   # the row just changed: what was seen
                        seq = prev
                    if not seq:
                        return
                    if Follow.alt_held():
                        self.queue(("follow", seq))()
                    else:
                        self.queue(("arrow", seq))()
                return handler

            # ---- the tick (client thread) ----
            def tick(self):
                st = self.st
                if st["g"] is not None and Kit.was_clicked(self.store, "close"):
                    self.close()
                    return
                q = st["queue"]
                while q:
                    a = q.pop(0)
                    kind = a[0] if isinstance(a, tuple) else a
                    if kind == "toggle_min":
                        st["minimized"] = not st["minimized"]
                        st["docked"] = False
                        safe(lambda: HOST.dock_forget(HIST_DOCK))
                        Kit.save_min(HIST_MIN_KEY, st["minimized"])
                        if st["g"] is not None:
                            self.build()
                    elif kind == "to_bar":
                        safe(lambda: HOST.dock_to_bar(HIST_DOCK, HIST_TITLE))
                    elif kind == "redraw":
                        if st["g"] is not None:
                            self.build()
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
                if st["g"] is None or (st["minimized"] and st["docked"]):
                    return                                   # closed, or folded: nothing to draw
                self.refresh()

            def entry(self, seq):
                for e in self.app.display.history:
                    if e.seq == seq:
                        return e
                return None

            def arrow(self, seq):
                """A row clicked: the tracking arrow on that ping's spot, or off when
                it is already there."""
                disp = self.app.display
                e = self.entry(seq)
                if e is None:
                    return
                if disp.arrow_entry() is e:
                    disp.arrow_off()
                    return
                pm = disp.player()[2]
                if pm != e.map:
                    self.app.api.SysMsg(JPFX + "that ping is on %s; you are on %s." % (
                        facet_name(e.map), facet_name(pm)), Kit.HUE_INFO)
                    return
                try:
                    disp.arrow_to(e)
                except Exception as ex:
                    self.app.api.SysMsg(JPFX + "couldn't show the tracking arrow (%s)." %
                                        short_error(ex), Kit.HUE_BAD)
                    return
                self.app.api.SysMsg(JPFX + "tracking arrow on %s's %s (%d, %d)." % (
                    e.who, label_of(e.type), e.x, e.y), Kit.HUE_INFO)

            def follow(self, seq):
                """Alt+click on a row: auto-follow whoever sent that ping, when a
                player of that name is in range (Follow toggles it off again)."""
                e = self.entry(seq)
                if e is None:
                    return
                if e.local:
                    self.app.api.SysMsg(JPFX + "that ping is your own.", Kit.HUE_INFO)
                    return
                serial = self.mobile_named(e.who)
                if not serial:
                    self.app.api.SysMsg(JPFX + "%s isn't in range." % e.who, Kit.HUE_INFO)
                    return
                Follow.toggle(serial, TITLE)

            def mobile_named(self, name):
                """Serial of the nearest mobile in view called `name` (any case), or 0."""
                low = str(name or "").strip().lower()
                if not low:
                    return 0
                best, bd = 0, None
                try:
                    mobs = list(self.app.api.GetAllMobiles() or [])
                except Exception:
                    mobs = []
                for m in mobs:
                    try:
                        if str(m.Name or "").strip().lower() != low:
                            continue
                        d = int(m.Distance)
                        if bd is None or d < bd:
                            best, bd = int(m.Serial), d
                    except Exception:
                        continue
                return best

            # ---- drawing ----
            def where_text(self, e, px, py, pm):
                spot = "(%d, %d)" % (e.x, e.y)
                if pm == e.map and px > 0:
                    dist = max(abs(e.x - px), abs(e.y - py))
                    if dist == 0:
                        return "here " + spot
                    return "%d tile%s %s  %s" % (dist, "" if dist == 1 else "s",
                                                 direction(e.x - px, e.y - py), spot)
                return "%s %s" % (facet_name(e.map), spot)

            def refresh(self):
                st = self.st
                disp = self.app.display
                hist = disp.history
                c = self.c
                if st["minimized"]:
                    if self.drawn == disp.hist_ver:
                        return
                    self.drawn = disp.hist_ver
                    if hist:
                        e = hist[-1]
                        txt = "%s: %d ping%s, last %s %s" % (HIST_TITLE, len(hist),
                                                            "" if len(hist) == 1 else "s",
                                                            label_of(e.type), e.who)
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
                # once a second for the distances; 2.6.82: nothing is redrawn when
                # you haven't moved (the rows' texts would come out the same)
                pos = disp.player()[:3] if hist else (0, 0, -1)
                if sig == self.drawn and pos == self.drawn_pos:
                    self.next_draw = now + 1.0
                    return
                self.drawn, self.next_draw, self.drawn_pos = sig, now + 1.0, pos
                n = len(hist)
                per = max(1, len(self.rows))
                pages = max(1, (n + per - 1) // per)
                self.page = max(0, min(pages - 1, self.page))
                if c.get("pg") is not None:
                    Kit.set_text(c["pg"], ("%d/%d" % (self.page + 1, pages)) if pages > 1 else "")
                px, py, pm = pos
                first = n - 1 - self.page * per                 # newest first
                where_w = c.get("where_w", 200)
                for k, r in enumerate(self.rows):
                    i = first - k
                    if i < 0:
                        if r["seq"]:
                            r["prev"] = (r["seq"], now)
                            r["seq"] = 0
                        r["sig"] = None
                        if k == 0 and n == 0:                    # an empty list says so
                            Kit.set_text(r["labels"][0], HIST_EMPTY, Kit.HUE_INFO)
                            self._show(r, True, only_first=True)
                        else:
                            self._show(r, False)
                        continue
                    e = hist[i]
                    if r["seq"] != e.seq:
                        r["prev"] = (r["seq"], now)
                        r["seq"] = e.seq
                    hue = TYPE_INFO.get(e.type, TYPE_INFO[LOOK])[1]
                    on = arrow is e
                    where = self.where_text(e, px, py, pm)
                    rsig = (e.seq, where, on)
                    if rsig != r["sig"]:
                        r["sig"] = rsig
                        texts = (time.strftime("%H:%M:%S", time.localtime(e.at)),
                                 label_of(e.type), e.who)
                        hues = (Kit.HUE_INFO, hue, Kit.HUE_TEXT if not e.local else Kit.HUE_INFO)
                        for j, lbl in enumerate(r["labels"]):
                            Kit.set_text(lbl, Kit.fit(texts[j], r["widths"][j]), hues[j])
                        Kit.set_text(r["where"], Kit.fit(("> " if on else "") + where, where_w),
                                     Kit.HUE_TITLE if on else Kit.HUE_INFO)
                        tip = HIST_TIPS[(on, e.local)]
                        if tip != r["tip"]:
                            r["tip"] = tip
                            try:
                                r["catch"].SetTooltip(tip)
                            except Exception:
                                pass
                    self._show(r, True)

            def _show(self, r, on, only_first=False):
                want = ("first" if only_first else on)
                if r["vis"] == want:
                    return
                r["vis"] = want
                parts = r["labels"] + [r["where"], r["catch"]]
                for j, ctl in enumerate(parts):
                    v = on and (not only_first or j == 0)
                    try:
                        ctl.IsVisible = v
                    except Exception:
                        pass


        class PingApp(object):
            def __init__(self, api):
                self.api = api
                self.mouse = None
                self.gesture = None         # dict while the wheel is held
                self.guide = None           # on-screen direction guide
                self.guide_labels = {}
                self.clock = time.time
                self.bridge = None
                self.bridge_error = None
                self.bridge_tried = False
                self.next_link_check = 0
                # (name, x, y, type) -> time first seen, to drop the copies of a ping (the
                # legacy alerts); recent_order keeps them oldest first so pruning is O(1)
                self.recent_pings = {}
                self.recent_order = collections.deque()
                self.settings = Settings(api)
                self.display = PingDisplay(api)
                self.conn = None
                self.pending = []           # actions queued by clicks/hotkeys, run in the main loop
                # The tick runs on the client thread and never touches the network
                # (a connect or a send can block); that is thread_step's, on the
                # script's own thread right after. They hand work to each other here:
                self.jobs = []              # network actions for thread_step
                self.outbox = []            # packets for thread_step to send
                self.inbox = []             # what thread_step got back, for the tick
                self.aim = None             # the "target a spot" cursor while it is up
                self.status_label = None
                self.hooked = []            # hotkey combos registered right now
                self.last_pos = None
                self.last_pos_sent = 0
                self.next_pos_read = 0      # share_position reads your position this often (0.5 s)
                self.last_ping_sent = 0
                self.last_auto_sent = 0     # pings other modules ask for (pings.send), own pace
                self.status_text = ""
                self.status_w = 300         # px the status label may take (set by build_send)
                self._shut = False
                self.history = HistoryWindow(self)   # the ping history window (2.6.05)

            # ---- UI ------------------------------------------------------------------
            def set_status(self, text, also_journal=True):
                self.status_text = text
                if self.status_label is not None:
                    Kit.set_text(self.status_label, Kit.fit(text, self.status_w))
                if also_journal:
                    self.api.SysMsg(JPFX + journal_case(text), Kit.HUE_INFO)

            # ---- the floating Guild Pings section of the shared window is gone
            #      (2.6.51): the settings page's SEND A PING section has its
            #      buttons and its status (build_send) ----
            def _gesture_summary(self):
                short = {LOOK: "Look", DANGER: "Danger", GO: "Go", HELP: "Help"}
                ts = [(d, TYPE_KEYS.get(GESTURE_DIRECTIONS.get(d, ""))) for d in ("up", "right", "down", "left")]
                return ", ".join("%s %s" % (d, short[t]) for d, t in ts if t is not None)

            def _queue_ping(self, t):
                def fn(*args):
                    # a key typed into a field (chat line, any text box): not a ping
                    if bool(safe(lambda: HOST.typing(), False)):
                        return
                    self.pending.append(("target", t))
                return fn

            def open_setup(self):
                self.inbox.append(("open_setup",))   # a window: drawn by the tick

            def save_setup(self):
                """The login on the settings page was saved: connect with it."""
                if self.conn and self.conn.kind == "tazuo":
                    self.set_status("Saved. TazUO's Enhanced Map login is on, so Map Pings keeps using that.")
                    return
                if self.conn:
                    self.conn.close()
                    self.conn = None
                self.choose_link()

            def apply_options(self):
                """Options changed on the settings page."""
                if OPT["gesture"] and self.mouse is None:
                    self.init_mouse()
                elif not OPT["gesture"]:
                    self.mouse = None
                    self.gesture = None
                    self.close_guide()
                self.jobs.append(("link",))  # choose_link(announce=False), on the script's thread

            # ---- network ---------------------------------------------------------------
            def connect(self):
                """Start a separate login of our own."""
                if self.conn:
                    self.conn.close()
                s = self.settings
                self.conn = MapConnection(s.host, s.port, s.user, s.password)
                self.set_status("Connecting to %s:%d..." % (s.host, s.port), also_journal=False)

            def get_bridge(self):
                if not self.bridge_tried:
                    self.bridge_tried = True
                    try:
                        self.bridge = TazUOBridge(self.api)
                    except Exception as e:
                        self.bridge = None
                        self.bridge_error = short_error(e)
                return self.bridge

            def tazuo_available(self):
                b = self.get_bridge()
                if b is None:
                    return False
                try:
                    cfg = b.config()
                except Exception:
                    return False
                return bool(cfg and cfg["configured"])

            def choose_link(self, announce=True):
                """Pick TazUO's connection or our own login, per CONNECTION. Safe to call repeatedly."""
                mode = (OPT["connection"] or "auto").lower()
                current = self.conn.kind if self.conn else None

                if mode in ("auto", "tazuo") and self.tazuo_available():
                    if current != "tazuo":
                        if self.conn:
                            self.conn.close()       # never hold a second login on the same account
                        self.conn = TazUOLink(self.bridge)
                    return

                if mode == "tazuo":
                    if current == "tazuo":
                        return  # keep waiting on it
                    if current == "own":              # 2.6.81: never our own login in this mode
                        self.conn.close()
                        self.conn = None
                        announce = True               # the status says why it went quiet
                    if announce:
                        if self.get_bridge() is None:
                            self.set_status("Can't use TazUO's Enhanced Map connection (%s)." % self.bridge_error)
                        else:
                            self.set_status("Turn on Enhanced Map in TazUO's Options (server, port, login).")
                    return

                if current == "tazuo":                # TazUO's Enhanced Map was switched off
                    self.conn.close()
                    self.conn = None
                    current = None

                if current == "own":
                    return
                if self.settings.complete:
                    self.connect()
                elif announce:
                    if mode == "auto" and self.get_bridge() is not None:
                        self.set_status("Turn on Enhanced Map in TazUO, or enter a separate map login "
                                        "(World Map settings page).")
                    else:
                        self.set_status("Enter your map server details to start.")
                        self.open_setup()

            def send_ping(self, x, y, m, t):
                now = self.clock()
                if now - self.last_ping_sent < PING_RATE_SECS:
                    return
                self.last_ping_sent = now
                self._send(x, y, m, t)

            def send_auto(self, x, y, m, t, who=None):
                """A ping another module asks for (HOST.services["pings.send"], for
                example Traps & Fields' Danger! on a trap). Paced like your own, one every
                PING_RATE_SECS, but on its own clock, so it never swallows a ping
                you send yourself. False = not now (too soon): ask again later."""
                now = self.clock()
                if now - self.last_auto_sent < PING_RATE_SECS:
                    return False
                self.last_auto_sent = now
                self._send(x, y, m, t, who=who, auto=True)
                return True

            def _send(self, x, y, m, t, who=None, auto=False):
                """Show a ping of yours and send it to the map server. auto (a ping
                another module asked for): no tracking arrow, first off a full
                screen, and the "not connected" note goes to the journal only when
                it is new (a run of trap pings doesn't repeat it once per ping)."""
                self.display.show("You", x, y, m, t, local=True, who=who, auto=auto)
                if self.conn and self.conn.ready:
                    # The ping packet (0x33) isn't part of the standard Enhanced Map protocol; a
                    # server without the ping update may drop whoever sends it. On TazUO's
                    # connection it is only sent once the server has shown it relays them;
                    # until then the typed alert below carries the type and facet.
                    # (sent in this order by thread_step, right after this tick)
                    relays = self.conn.server_relays_ping
                    if relays or SEND_PING_PACKET == "always":
                        self.outbox.append(pk_ping(x, y, m, t))
                    if SEND_LEGACY_ALERT or not relays:
                        typed = pk_typed_alert(x, y, m, t)
                        if typed:
                            self.outbox.append(typed)        # old servers: scripts decode type + facet from this
                        self.outbox.append(pk_alert(x, y))   # last, so TazUO's overlay / Enhanced Map show the real spot
                else:
                    note = "Not connected: only you can see that ping."
                    self.set_status(note, also_journal=not auto or self.status_text != note)

            # ---- "target a spot": the client's own target cursor, watched every tick ----
            # API.RequestAnyTarget held the whole script (every module) until the
            # player clicked; this cursor holds nothing up. Like HOST.pick_target,
            # but it hands back the spot (ground, static, item or mobile), not a serial.
            AIM_SECONDS = 10

            def _target_manager(self):
                P = globals().get("Picker")             # Virtue Assistant's cursor helper
                return safe(P._tm) if P is not None else None

            def target_ping(self, t):
                self.api.SysMsg(JPFX + "target a spot for %s (target yourself for where you stand)."
                                % label_of(t), Kit.HUE_INFO)
                self.aim = None                         # a newer cursor replaces ours
                tm = self._target_manager()
                if tm is not None:
                    aim = {"t": t, "fired": False, "spot": None, "d": None, "tm": tm,
                           "until": self.clock() + self.AIM_SECONDS}

                    def got(obj, aim=aim):              # the client calls this when you target
                        aim["spot"] = spot_of(obj)
                        aim["fired"] = True
                    try:
                        from System import Action
                        aim["d"] = Action[object](got)
                        tm.SetTargeting(aim["d"], Picker.CURSOR_TARGET, Picker.neutral)
                        self.aim = aim
                        # spoken for: Bandages / Ultima Tracker don't aim it at anyone
                        safe(lambda: HOST.claim_cursor("pings", self.AIM_SECONDS))
                        return
                    except Exception:
                        pass
                self.jobs.append(("aim", t))            # no client access: the old blocking cursor

            def poll_aim(self):
                """On the tick: the cursor's outcome, once there is one."""
                aim = self.aim
                if aim is None:
                    return
                if not aim["fired"]:
                    tm = aim["tm"]                      # the one it went up on (2.6.82: not looked up per tick)
                    ours = False
                    if tm is not None:                  # every tick while the cursor is up: no lambdas
                        try:
                            ours = bool(tm.IsCurrentTargetingAction(aim["d"]))
                        except Exception:
                            ours = False
                    if ours and self.clock() < aim["until"]:
                        return                          # still up
                    self.aim = None                     # cancelled, replaced by another cursor, or timed out
                    HOST.release_cursor("pings")
                    if ours:
                        try:
                            tm.CancelTarget()           # ours, timed out: take it down
                        except Exception:
                            pass
                    return
                self.aim = None
                HOST.release_cursor("pings")
                self.aimed(aim["t"], aim["spot"])

            def aimed(self, t, spot):
                if spot is None:
                    return
                x, y = spot
                if x <= 0 or y <= 0:
                    return
                self.send_ping(x, y, int(self.api.GetMap()), t)

            def drop_aim(self):
                """Take our cursor down (stopping): only if it is still ours."""
                aim, self.aim = self.aim, None
                safe(lambda: HOST.release_cursor("pings"))
                tm = self._target_manager() if aim is not None else None
                if tm is None or aim["fired"]:
                    return

                def cancel():
                    if tm.IsCurrentTargetingAction(aim["d"]):
                        tm.CancelTarget()
                safe(lambda: Kit.on_client(cancel, fallback=False))

            def target_ping_blocking(self, t):
                """Builds without client access: the old blocking cursor (script's thread)."""
                target = self.api.RequestAnyTarget(10)
                if target is None:
                    return
                try:
                    x, y = int(target.X), int(target.Y)
                except Exception:
                    return
                self.inbox.append(("aimed", t, (x, y)))

            def share_position(self):
                """Separate login only: your position for guildmates' maps. The
                position is sent at most once a second, so it is read every 0.5 s
                (it used to be read every tick: API.Player, X, Y and GetMap each time)."""
                if not self.conn or not self.conn.ready or not self.conn.owns_position:
                    return
                now = self.clock()
                if now < self.next_pos_read:
                    return
                self.next_pos_read = now + POSITION_READ_EVERY
                pos = None
                if OPT["share"]:
                    p = self.api.Player
                    try:
                        pos = (int(p.X), int(p.Y), int(self.api.GetMap()))
                    except Exception:
                        pass
                if pos is None or pos[0] <= 0:
                    if now - self.conn.last_sent > 20:
                        self.outbox.append(pk_keepalive())
                    return

                if (pos != self.last_pos and now - self.last_pos_sent >= 1.0) or now - self.last_pos_sent >= 10:
                    flag = 0
                    try:                                # (2.6.82: direct reads, same order)
                        if p.IsDead:
                            flag = 4
                        elif p.IsPoisoned:
                            flag = 1
                        elif p.IsYellowHits:
                            flag = 2
                        elif p.IsParalyzed:
                            flag = 3
                        elif p.IsHidden:
                            flag = 5
                        stats = (int(p.Hits), int(p.Stamina), int(p.Mana), int(p.HitsMax), int(p.StaminaMax), int(p.ManaMax))
                    except Exception:
                        stats = (0, 0, 0, 0, 0, 0)
                    self.outbox.append(pk_player_data(pos, stats, flag, NAME_COLOR))
                    self.last_pos, self.last_pos_sent = pos, now

            # ---- loop -------------------------------------------------------------------
            def handle(self, ev):
                kind = ev[0]
                if kind == "status":
                    self.set_status(ev[1], also_journal=ev[2])
                elif kind == "ping":
                    _, name, x, y, m, t = ev
                    self.show_once(name, x, y, m, t)
                elif kind == "alert":
                    _, name, x, y = ev
                    decoded = decode_typed_alert(x, y)
                    if decoded:
                        dx, dy, dm, dt = decoded
                        self.show_once(name, dx, dy, dm, dt)
                    elif not self.seen_recently(name, x, y):
                        # a plain alert from someone without the script (the plain copy of a ping is dropped above)
                        self.show_once(name, x, y, int(self.api.GetMap()), LOOK)
                elif kind == "message":
                    self.api.SysMsg(JPFX + "map server: " + ev[1], Kit.HUE_INFO)

            # Each ping can arrive up to three times (ping message, typed alert, plain alert).
            # The first copy is shown; the others are dropped.
            DEDUPE_SECONDS = 3

            def seen_recently(self, name, x, y, t=None):
                """t=None (a plain alert, type unknown) matches a recent ping of any type."""
                now = self.clock()
                order, recent = self.recent_order, self.recent_pings
                while order and now - order[0][0] > self.DEDUPE_SECONDS:   # oldest first: O(1) a prune
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
                if self.seen_recently(name, x, y, t):
                    return
                now = self.clock()
                key = (name, x, y, t)
                self.recent_pings[key] = now
                self.recent_order.append((now, key))
                self.display.show(name, x, y, m, t)

            def step(self):
                """One pass of the main loop, on the client thread (never waits:
                no network here, see thread_step)."""
                while self.pending:
                    action = self.pending.pop(0)
                    if action[0] == "target":
                        self.target_ping(action[1])
                    elif action[0] == "options":
                        self.apply_options()
                    elif action[0] == "rehook":
                        self.register_hotkeys()
                    elif action[0] == "history":        # the History button (2.6.05)
                        self.history.toggle_open()
                    else:                               # save_setup, reconnect: network
                        self.jobs.append(action)

                # what thread_step got from the map server (and its window requests)
                inbox = self.inbox
                if inbox:                               # (2.6.82: no new list per idle tick)
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
                """The network side of a pass, on the script's own thread right after
                step(): connecting, sending, reading. Returns at once when idle."""
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
                        elif self.settings.complete and \
                                (OPT["connection"] or "auto").lower() != "tazuo":
                            self.connect()            # (2.6.81: not when only TazUO's is wanted)
                            self.conn.reset()
                        else:
                            self.choose_link()

                # in auto mode, follow TazUO's Enhanced Map being switched on/off
                if self.clock() >= self.next_link_check:
                    self.next_link_check = self.clock() + 5
                    self.choose_link(announce=False)

                out = self.outbox
                if out:                                 # (2.6.82: no new list per idle pass)
                    self.outbox = []
                if self.conn:
                    for data in out:
                        self.conn.send(data)
                    self.inbox.extend(self.conn.poll())

            # ---- mouse-wheel gesture ----------------------------------------------------
            def init_mouse(self):
                if not OPT["gesture"]:
                    self.mouse = None
                    return
                try:
                    self.mouse = TazUOMouse(self.api)
                except Exception as e:
                    self.mouse = None
                    self.api.SysMsg(JPFX + "mouse-wheel pings aren't available (%s): use the ping buttons "
                                    "or the hotkeys." % short_error(e), Kit.HUE_INFO)

            @staticmethod
            def drag_direction(dx, dy):
                if max(abs(dx), abs(dy)) < OPT["drag"]:
                    return None
                if abs(dx) > abs(dy):
                    return "right" if dx > 0 else "left"
                return "down" if dy > 0 else "up"

            def poll_gesture(self):
                m = self.mouse
                if m is None:
                    return
                try:
                    down = m.middle_down()
                except Exception:
                    return

                if down and self.gesture is None:
                    try:
                        tile = m.tile_under_mouse()
                        start = m.press_position()
                    except Exception:
                        tile, start = None, (0, 0)
                    # pressed over a gump/panel (or nothing): ignore this press entirely
                    self.gesture = {"tile": tile, "start": start, "dir": None, "map": int(self.api.GetMap())}
                    if tile is not None:
                        self.show_guide(start)
                elif down and self.gesture is not None:
                    if self.gesture["tile"] is None:
                        return
                    try:
                        x, y = m.position()
                    except Exception:
                        return
                    d = self.drag_direction(x - self.gesture["start"][0], y - self.gesture["start"][1])
                    if d != self.gesture["dir"]:
                        self.gesture["dir"] = d
                        self.update_guide(d)
                elif not down and self.gesture is not None:
                    g, self.gesture = self.gesture, None
                    self.close_guide()
                    t = TYPE_KEYS.get(GESTURE_DIRECTIONS.get(g["dir"] or "", ""))
                    if g["tile"] is not None and t is not None:
                        self.send_ping(g["tile"][0], g["tile"][1], g["map"], t)

            def show_guide(self, center):
                self.close_guide()
                try:
                    G = self.api.Gumps
                    w, h = 180, 104
                    gump = G.CreateGump(False, False)
                    # the press position is in the client window's real pixels; gumps are
                    # placed in UI-scaled pixels (Kit.screen), so with a UI scale other
                    # than 1 the guide opened away from the cursor
                    scale = Kit.render_scale() or 1.0
                    cx, cy = int(round(center[0] / scale)), int(round(center[1] / scale))
                    Kit.place(gump, cx - w // 2, cy - h // 2, w, h)   # on screen
                    Kit.add_window_frame(gump, w, h, corners=False)
                    Kit.add_section(gump, 6, 6, w - 12, h - 12)
                    spots = {"up": (58, 9), "right": (110, 43), "down": (58, 77), "left": (11, 43)}
                    self.guide_labels = {}
                    for d, (lx, ly) in spots.items():
                        t = TYPE_KEYS.get(GESTURE_DIRECTIONS.get(d, ""))
                        if t is None:
                            continue
                        lab = G.CreateGumpLabel(label_of(t), 946)
                        lab.SetRect(lx, ly, 70, 18)
                        gump.Add(lab)
                        self.guide_labels[d] = (lab, t)
                    plus = G.CreateGumpLabel("+", 53)
                    plus.SetRect(w // 2 - 3, h // 2 - 9, 10, 18)
                    gump.Add(plus)
                    G.AddGump(gump)
                    try:
                        # a guide under the held wheel is no window to snap to or move:
                        # keep it out of the mother's snapping and keeper
                        SNAP.skip_gump(gump)
                    except Exception:
                        pass
                    self.guide = gump
                except Exception:
                    self.guide = None

            def update_guide(self, chosen):
                for d, (lab, t) in self.guide_labels.items():
                    try:
                        lab.Text = "[" + label_of(t) + "]" if d == chosen else label_of(t)
                        lab.Hue = TYPE_INFO[t][1] if d == chosen else 946
                    except Exception:
                        pass

            def close_guide(self):
                if self.guide is not None:
                    try:
                        self.guide.Dispose()
                    except Exception:
                        pass
                self.guide = None
                self.guide_labels = {}

            def register_hotkeys(self):
                self.unregister_hotkeys()
                owned = getattr(HOST, "hotkeys_owned", None)
                for key, combo in HOTKEYS.items():
                    if combo and key in TYPE_KEYS:
                        try:
                            self.api.OnHotKey(combo, self._queue_ping(TYPE_KEYS[key]))
                        except Exception:
                            self.api.SysMsg(JPFX + "can't use '%s' as the %s hotkey." % (
                                combo, label_of(TYPE_KEYS[key])), Kit.HUE_BAD)
                            continue
                        self.hooked.append(combo)
                        if owned is not None:
                            owned[combo] = TITLE            # the Action Bar keeps off it
                        note = getattr(HOST, "hotkey_note", None)
                        if note is not None:                # listed on Settings > Hotkeys (2.6.05)
                            try:
                                note(combo, TITLE, "%s ping" % label_of(TYPE_KEYS[key]))
                            except Exception:
                                pass

            def unregister_hotkeys(self):
                owned = getattr(HOST, "hotkeys_owned", None)
                drop = getattr(HOST, "hotkey_drop", None)
                for combo in self.hooked:
                    try:
                        self.api.OnHotKey(combo)
                    except Exception:
                        pass
                    if owned is not None:
                        owned.pop(combo, None)
                    if drop is not None:                    # off Settings > Hotkeys (2.6.05)
                        try:
                            drop(combo, TITLE)
                        except Exception:
                            pass
                self.hooked = []

            def shutdown(self):
                if self._shut:
                    return
                self._shut = True
                self.unregister_hotkeys()
                self.drop_aim()
                self.close_guide()
                try:
                    self.history.shutdown()
                except Exception:
                    pass
                try:
                    self.display.clear()
                except Exception:
                    pass
                if self.conn:
                    self.conn.close()

            def start(self):
                # 2.6.51: no floating window any more (its section of the shared
                # window is gone): the ping buttons, Reconnect, History and the
                # status are on the settings page (SEND A PING), with the hotkeys
                # and the mouse-wheel drag as before
                self.init_mouse()
                self.register_hotkeys()
                self.history.start()
                self.api.SysMsg(JPFX + "on; its ping buttons are on the World Map settings page.", Kit.HUE_GOOD)
                self.choose_link()
                self.next_link_check = self.clock() + 5


        # =============================================================================
        #  Module
        # =============================================================================
        APP = {"app": None}


        def _offer_ping(x, y, m=None, kind="danger", who=None):
            """HOST.services["pings.send"]: another module sends a ping of yours.
            kind: "look", "danger", "go" or "help"; m: the facet (None = yours).
            Call it from a tick (the client thread). True = shown and sent (or
            shown only, when not connected); False = not now (Map Pings stopping
            or the last one was too recent): ask again on a later tick."""
            app = APP["app"]
            if app is None or app._shut:
                return False
            if m is None:
                try:
                    m = int(API.GetMap())
                except Exception:
                    return False
            return app.send_auto(int(x), int(y), int(m), TYPE_KEYS.get(kind, DANGER), who)


        def _start():
            APP["app"] = PingApp(API)
            APP["app"].start()
            if hasattr(HOST, "services"):
                HOST.services["pings.send"] = _offer_ping     # Traps & Fields' trap pings, for one


        def _tick():
            if APP["app"] is not None:
                APP["app"].step()


        def _thread_tick():
            if APP["app"] is not None:
                APP["app"].thread_step()


        def _stop():
            if hasattr(HOST, "services"):
                HOST.services.pop("pings.send", None)
            app, APP["app"] = APP["app"], None
            if app is not None:
                app.shutdown()


        def _interval():
            """0.02 s while the wheel is held, 0.05 s while something is under way
            (our cursor up, clicks or map-server lines waiting), else 0.1 s (2.6.82:
            a wheel gesture needs a drag, so a 0.1 s first look still catches it)."""
            app = APP["app"]
            if app is None:
                return 0.05
            if app.gesture is not None:
                return 0.02
            if app.aim is not None or app.pending or app.inbox or app.jobs or app.outbox:
                return 0.05
            return 0.1


        # =============================================================================
        #  Map Pings' page of the Virtue Assistant Settings tab
        # =============================================================================
        OPT_KEY = VAR_PREFIX + "options"
        CONNECTIONS = [("auto", "TazUO's map if on, else my login"),
                       ("tazuo", "Only TazUO's Enhanced Map"),
                       ("own", "Only my own login")]
        CONN_CODES = [c[0] for c in CONNECTIONS]
        OPT = {"sounds": PLAY_SOUNDS, "share": SHARE_POSITION, "gesture": MOUSE_GESTURE,
               "connection": CONNECTION,
               "ping_secs": PING_SECONDS,       # how long a ping stays on screen (settings page)
               "drag": GESTURE_MIN_DRAG}        # pixels to drag before a direction counts
        OPT_LIMITS = {"ping_secs": (PING_SECS_MIN, PING_SECS_MAX), "drag": (DRAG_MIN, DRAG_MAX)}


        def load_options():
            for part in Kit.get_var(OPT_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                if k in ("sounds", "share", "gesture"):
                    OPT[k] = v == "1"
                elif k == "connection" and v in CONN_CODES:
                    OPT[k] = v
                elif k in OPT_LIMITS:                    # new trailing fields (2.6.01)
                    try:
                        lo, hi = OPT_LIMITS[k]
                        OPT[k] = max(lo, min(hi, int(v)))
                    except ValueError:
                        pass
                elif k.startswith("hk_") and k[3:] in HOTKEYS:
                    HOTKEYS[k[3:]] = norm_hotkey(v)


        def norm_hotkey(v):
            return str(v or "").strip().upper().replace(" ", "")


        def save_options():
            data = "sounds=%d;share=%d;gesture=%d;connection=%s" % (
                OPT["sounds"], OPT["share"], OPT["gesture"], OPT["connection"])
            data += "".join(";hk_%s=%s" % (k, HOTKEYS[k].replace(";", "")) for k in HOTKEY_ORDER)
            data += ";ping_secs=%d;drag=%d" % (int(OPT["ping_secs"]), int(OPT["drag"]))
            Kit.put_var(OPT_KEY, data)


        def _queue_app(action):
            if APP["app"] is not None:
                APP["app"].pending.append(action)


        page = {"fields": None, "checks": None, "dd": None, "store": ({}, {}), "seen": None,
                "status": None, "keys": None, "seen_keys": None, "nums": None}
        H_SEND, H_LOGIN, H_OPT, H_KEYS = 116, 160, 124, 70
        PING_TIP = "Send a %s ping where you next target: a spot, an item or a person"
        KEY_SHORT = {"look": "Look", "danger": "Danger", "go": "Go", "help": "Help"}   # the hotkey labels
        KEY_TIP = "The key for a %s ping, for example CTRL+1, F9 or SHIFT+F2 (blank = none)"
        LOGIN_TIPS = {"host": "The map server's address (a host name or an IP address)",
                      "port": "The map server's port (a number; %d by default)" % DEFAULT_PORT,
                      "user": "Your login name on the map server",
                      "pass": "Your map server password; kept in plain text in the client's saved "
                              "variables on this PC, like Enhanced Map's own"}


        def _page_ping(t):
            """A ping button on the settings page: only queued (the tick raises
            the cursor), as the floating window's buttons did."""
            def fn(*args):
                if APP["app"] is not None:
                    APP["app"].pending.append(("target", t))
            return fn


        def _page_action(action):
            def fn(*args):
                _queue_app(action)
            return fn


        def config_height(w):
            return H_SEND + Kit.GAP + H_LOGIN + Kit.GAP + H_OPT + Kit.GAP + H_KEYS


        def build_send(g, x, y, w, store):
            """SEND A PING (2.6.51): what the floating Guild Pings section had (the
            four ping buttons, Reconnect, History and the connection's status)."""
            Kit.add_section(g, x, y, w, H_SEND, "SEND A PING  (or a hotkey, or the mouse-wheel drag)")
            bx = x + 12
            for t in (LOOK, DANGER, GO, HELP):
                label, hue = TYPE_INFO[t][:2]
                cap = label + "..."                  # a target cursor follows
                Kit.art_button(g, store, "ping%d" % t, Kit.ART_PLAY, bx, y + 28, cap, PING_TIP % label,
                               hue=hue, on_click=_page_ping(t))
                bx += 35 + Kit.text_w(cap) + 16
            Kit.art_button(g, store, "recon", Kit.ART_PLAY, x + 12, y + 58, "Reconnect",
                           "Connect to the map server again (TazUO's Enhanced Map or the separate login)",
                           on_click=_page_action(("reconnect",)))
            hx = x + 12 + 35 + Kit.text_w("Reconnect") + 16
            Kit.art_button(g, store, "history", Kit.ART_PAGE, hx, y + 58, "History",
                           "Open the ping history window: recent pings, yours and other people's "
                           "(click again to close it)", on_click=_page_action(("history",)))
            gx = hx + 35 + Kit.text_w("History") + 16
            app = APP["app"]
            if app is not None:                  # the same line whether the drag is on or not
                hint = "Wheel drag: " + app._gesture_summary()
                Kit.add_label(g, Kit.fit(hint, x + w - 12 - gx), gx, y + 61, Kit.HUE_INFO)
            lbl = Kit.add_label(g, "", x + 12, y + 90, Kit.HUE_INFO)
            page["status"] = lbl
            if app is not None:                  # the connection's status lines land here now
                app.status_label, app.status_w = lbl, w - 24
                Kit.set_text(lbl, Kit.fit(app.status_text or "Starting...", w - 24))


        def build_config(g, x, y, w):
            store = ({}, {})
            build_send(g, x, y, w, store)
            y = y + H_SEND + Kit.GAP
            st = Settings(API)
            h_login, h_opt = H_LOGIN, H_OPT
            Kit.add_section(g, x, y, w, h_login, "SEPARATE MAP LOGIN  (when TazUO's Enhanced Map is off)")
            fields = {}
            col = (w - 36) // 2
            for i, (key, caption, value) in enumerate((
                    ("host", "Server address:", st.host), ("port", "Port:", str(st.port)),
                    ("user", "Map username:", st.user), ("pass", "Map password:", st.password))):
                fx = x + 12 + (i % 2) * (col + 12)
                fy = y + 30 + (i // 2) * 48
                Kit.add_label(g, caption, fx, fy)
                fields[key] = Kit.add_textbox(g, value, fx + 2, fy + 20, col - 8,
                                              numbers=key == "port")
                safe(lambda key=key: fields[key].SetTooltip(LOGIN_TIPS[key]))
            Kit.art_button(g, store, "save", Kit.ART_OK, x + 12, y + 128, "Save and connect",
                           "Save the four fields on this PC and connect with them")
            # the login is kept in plain text in the client's saved variables on this PC
            page["login"] = Kit.add_label(g, Kit.fit("Saved on this PC in plain text (the password "
                                                      "shows while typing).", w - 236),
                                           x + 220, y + 131, Kit.HUE_INFO)

            yo = y + h_login + Kit.GAP
            Kit.add_section(g, x, yo, w, h_opt, "OPTIONS")
            checks = {
                "sounds": Kit.add_check(g, "Play a sound for each ping", x + 12, yo + 32,
                                        OPT["sounds"],
                                        "Play the ping's sound when a ping shows, yours and other people's"),
                "gesture": Kit.add_check(g, "Ping with a mouse-wheel drag", x + 312, yo + 32,
                                         OPT["gesture"],
                                         "Hold the mouse wheel over a spot and drag: up Look here, "
                                         "right Danger!, down Go here, left Need help"),
                "share": Kit.add_check(g, "Show me on guildmates' maps", x + 12, yo + 58,
                                       OPT["share"],
                                       "Send your position to the map server (separate login only; "
                                       "TazUO's Enhanced Map does this itself)"),
            }
            # ping seconds and drag distance (2.6.01): were constants in the file
            nums = {}
            ny = yo + 86
            Kit.add_label(g, "Ping stays:", x + 12, ny + 3)
            nx = x + 12 + Kit.text_w("Ping stays:") + 8
            nums["ping_secs"] = Kit.add_textbox(g, str(OPT["ping_secs"]), nx, ny, 44)
            Kit.add_label(g, "s", nx + 50, ny + 3, Kit.HUE_INFO)
            safe(lambda: nums["ping_secs"].SetTooltip(
                "Seconds a ping's marker and pulse stay on screen (%d-%d)" % OPT_LIMITS["ping_secs"]))
            Kit.add_label(g, "Drag distance:", x + 312, ny + 3)
            dx_ = x + 312 + Kit.text_w("Drag distance:") + 8
            nums["drag"] = Kit.add_textbox(g, str(OPT["drag"]), dx_, ny, 44)
            Kit.add_label(g, "px", dx_ + 50, ny + 3, Kit.HUE_INFO)
            safe(lambda: nums["drag"].SetTooltip(
                "Pixels the mouse-wheel drag must go before a direction counts (%d-%d)" % OPT_LIMITS["drag"]))
            yk = yo + h_opt + Kit.GAP
            Kit.add_section(g, x, yk, w, H_KEYS, "HOTKEYS  (blank = none)")
            keys = {}
            kx = x + 12
            for k in HOTKEY_ORDER:
                cap = KEY_SHORT[k] + ":"
                Kit.add_label(g, cap, kx, yk + 36)
                keys[k] = Kit.add_textbox(g, HOTKEYS[k], kx + Kit.text_w(cap) + 8, yk + 33, 84,
                                          numbers=False)
                safe(lambda k=k: keys[k].SetTooltip(KEY_TIP % label_of(TYPE_KEYS[k])))
                kx += Kit.text_w(cap) + 8 + 84 + 16
            Kit.add_label(g, "Connection:", x + 312, yo + 60)
            idx = CONN_CODES.index(OPT["connection"]) if OPT["connection"] in CONN_CODES else 0
            dd = G.CreateDropDown(190, [c[1] for c in CONNECTIONS], idx)
            dd.SetPos(x + 414, yo + 56)
            g.Add(dd)
            safe(lambda: dd.SetTooltip("Which map connection to use: TazUO's Enhanced Map while it "
                                       "is on, or the separate login above"))
            page.update({"fields": fields, "checks": checks, "dd": dd, "store": store,
                         "seen": dict(OPT), "keys": keys, "seen_keys": dict(HOTKEYS),
                         "nums": nums, "unread": False, "next_read": 0.0})


        CONFIG_READ_EVERY = 0.2      # seconds between reads of the boxes, list and hotkey fields


        def poll_config(force=False):
            if page["fields"] is None:
                return
            if Kit.was_clicked(page["store"], "save"):
                _save_login()
            now = time.time()
            if not force and now < page.get("next_read", 0.0):
                page["unread"] = True            # read on the next poll, or as the page closes
                return
            page["next_read"], page["unread"] = now + CONFIG_READ_EVERY, False
            # plain loops and try blocks: this runs five times a second while the
            # page is open, on the client thread
            for k, cb in page["checks"].items():
                try:
                    OPT[k] = bool(cb.IsChecked)
                except Exception:
                    pass
            try:
                i = int(page["dd"].GetSelectedIndex())
            except Exception:
                i = None
            if i is not None and 0 <= i < len(CONNECTIONS):
                OPT["connection"] = CONNECTIONS[i][0]
            for k, tb in (page.get("nums") or {}).items():
                try:
                    txt = str(tb.Text or "").strip()
                except Exception:
                    continue
                if txt.isdigit():                       # a half-typed or empty field: keep the old value
                    lo, hi = OPT_LIMITS[k]
                    OPT[k] = max(lo, min(hi, int(txt)))
            if OPT != page["seen"]:
                page["seen"] = dict(OPT)
                save_options()
                _queue_app(("options",))
            new = {}
            for k, tb in page["keys"].items():
                try:
                    new[k] = norm_hotkey(tb.Text)
                except Exception:
                    new[k] = norm_hotkey(HOTKEYS[k])
            if force and new != page["seen_keys"]:   # 2.6.81: the page closing takes what is typed
                page["typed"] = page["seen_keys"] = new
                HOTKEYS.update(new)
                save_options()
                _queue_app(("rehook",))
            elif new != page.get("typed"):           # still being typed: wait for it to settle
                page["typed"], page["stable"] = new, 0
            elif new != page["seen_keys"]:
                page["stable"] = page.get("stable", 0) + 1
                if force or page["stable"] >= 5:     # unchanged for ~1 s (or the page closing)
                    page["seen_keys"] = new
                    HOTKEYS.update(new)
                    save_options()
                    _queue_app(("rehook",))


        def _save_login():
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
            st = Settings(API)
            st.host, st.port, st.user, st.password = host, port, user, password
            st.save()
            Kit.set_text(page["login"], "Saved", Kit.HUE_GOOD)
            app = APP["app"]
            if app is not None:
                s = app.settings
                s.host, s.port, s.user, s.password = host, port, user, password
                app.pending.append(("save_setup",))


        def config_closed():
            poll_config(True)                   # the page's last values, however recent (2.6.81:
            #                                     always: a key typed after the last read counts too)
            app = APP["app"]
            if app is not None and app.status_label is page.get("status"):
                app.status_label = None          # the page's status label goes with the page
            page.update({"fields": None, "checks": None, "dd": None, "status": None, "keys": None,
                         "nums": None, "login": None})


        load_options()
        # tick: the client side (cursor, gesture, pings on screen), on the client
        # thread; thread_tick: the map server connection, which may block.
        MODULE = {"start": _start, "tick": _tick, "stop": _stop, "interval": _interval,
                  "client_tick": True, "thread_tick": _thread_tick,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE

    def _part_corpse():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Kit, Journal, HOST, the main loop and the settings window), so run that
        # =============================================================================
        #  MODULE: Corpse (Corpse Run before 2.6.52)  -  back to your corpse, and your
        #  things back from it
        #
        #  - When you die it remembers where (x, y, facet) and when, finds your
        #    corpse there (the corpse item that turns up beside where you died, with
        #    your body and, when the client knows it, your name) and points a
        #    tracking arrow of its own at it. The window shows how far and which
        #    way, and counts down until the corpse turns to bones and then decays
        #    (red in the last minute, with one alert).
        #  - After you are resurrected, "Get my things" (only when you press it)
        #    opens the corpse and moves your items back into your backpack one at
        #    a time, one move every MOVE_GAP seconds. It stops when you press Stop,
        #    when a target cursor is up, when you pick something up, when you walk
        #    away from the corpse, before you would go over your weight limit, and
        #    after FAIL_STOP refused moves in a row. Each item is moved once (an
        #    item the server answers "You must wait..." for is tried again).
        #    Re-dressing afterwards is yours (an Action Bar "Dress outfit" cell
        #    does it in one key).
        #  - Optional (off at first): a Need help map ping on your corpse for your
        #    guild when you die, through Map Pings when it is on. The window's
        #    "Ping for help" button sends one by hand.
        #  - A second death replaces the first. The corpse is remembered per
        #    character, so logging out and back in keeps it. The arrow is cleared
        #    when your things are back, when the corpse is gone or forgotten, and
        #    when the module stops; only this module's own arrow is ever touched.
        #  - Nothing here acts on its own: the only actions are the ones you click
        #    (Get my things, Ping for help).
        # =============================================================================
        KEY = "corpserun"
        TITLE = "Corpse"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "CorpseRun_settings"   # per character: "arrow=1;restore=1;ping=0;decay=7;bones=7;say=0"
        CORPSE_KEY = "CorpseRun_corpse"       # per character: the corpse remembered (see save_rec)
        POS_KEY = "CorpseRun_pos"             # where the window sits (saved the moment it is let go)
        MIN_KEY = "CorpseRun_min"             # minimized when you left (kept for the next start)
        TRAY_ICON = 0x0ECA                    # bones: item art on the Action Bar's tray button
        ARROW_ID = 0x434F5250                 # "CORP": this module's own tracking arrow (Map Pings
        #                                       uses 0x50494E47; each clears only its own)
        CORPSE_GRAPHIC = 0x2006               # a corpse
        BONES_FIRST, BONES_LAST = 0x0ECA, 0x0ED2   # a player corpse turned to bones (same item)
        BONES_GFX = tuple(range(BONES_FIRST, BONES_LAST + 1))
        #  Decay (minutes; the settings page): on In Mani Ylem a player corpse turns
        #  to bones after 15 minutes and the bones (your items still in them) are
        #  gone 45 minutes later (an hour in all). A save from 2.6.06 still holding
        #  its old 7 / 7 (RunUO's stock times, never right here) is moved to these.
        DEFAULT_DECAY_MIN = 15
        DEFAULT_BONES_MIN = 45
        OLD_DEFAULTS = (7, 7)                 # 2.6.06's defaults: a save with them loads as the new ones
        MIN_LO, MIN_HI = 1, 120               # what the two minute fields accept
        TYPE_SETTLE = 1.0                     # seconds a minute field's text stands before it applies
        RED_SECS = 60                         # the countdown turns red this long before it ends
        WARN_SECS = 60                        # ...and one alert says so (Settings > Alerts)
        DECAYED_GRACE = 120.0                 # seconds past the end before a corpse still not seen
        #                                       gone is forgotten (the shard may be slower)
        ALERT_DECAY = "corpserun.decay"       # its alert kind: sound, on / off on Settings > Alerts
        ALERT_DECAY_SOUND = 0x1EA             # chime
        #  Finding the corpse after a death
        FIND_SECS = 20.0                      # look for it this long after the death...
        FIND_EVERY = 0.5                      # ...this often
        CORPSE_NEAR = 3                       # tiles from where you died
        HUMAN_BODIES = (0x190, 0x191, 0x25D, 0x25E, 0x29A, 0x29B)   # a player's corpse (its amount
        #                                       is the body), when found without knowing the spot
        SEEK_RANGE = 24                       # tiles round you that are searched (one client call)
        LOOK_NEAR = 12                        # not found yet: looked for again whenever you are this
        LOOK_EVERY = 1.0                      # close to the spot, this often
        GONE_RANGE = 12                       # tiles: this close to it and not in view...
        GONE_SECS = 6.0                       # ...this long: the corpse is gone (looted or decayed)
        ITEM_EVERY = 1.0                      # seconds between looks at a known corpse (2.6.82)
        #  Get my things
        REACH = 2                             # tiles: how close you must stand to use / loot it
        #                                       (RunUO's container range; unchecked in game)
        OPEN_WAIT = 1.0                       # seconds after opening it before its items are read
        OPEN_MAX = 3.0                        # ...and at most this long for them to arrive
        MOVE_GAP = 0.7                        # seconds between two moves (the shard's drag delay;
        #                                       unchecked in game)
        MOVE_RECHECK = 2                      # extra looks at a move the server hasn't answered yet
        FAIL_STOP = 3                         # refused moves in a row before it gives up
        WAIT_RETRY = 2                        # "You must wait..." answers allowed per item
        PLAN_CAP = 250                        # items taken by one press
        REPLAN = 2                            # looks for items that turned up meanwhile (per press)
        J_WAIT = ("must wait to perform another action",)   # cliloc 500119
        HAIR_LAYERS = (11, 16)                # hair and beard ride on a corpse: never taken
        HAIR_FIRST, HAIR_LAST = 0x203B, 0x204D    # (by graphic too, when the layer can't be read)
        #  Need help ping (Map Pings' HOST.services["pings.send"])
        PING_TRY = 15.0                       # seconds a ping waits for Map Pings' pace
        #  Pace
        TICK_IDLE = 0.25                      # seconds between ticks
        TICK_BUSY = 0.1                       # ...while your things are being moved
        BODY_EVERY = 2.0                      # your body graphic is read this often while alive
        LABEL_EVERY = 0.5                     # the window's texts are worked out this often
        CLOCK_JUMP = 2.0                      # seconds: the computer's clock going back more than
        #                                       this between two ticks moves every time kept with it
        FACETS = ("Felucca", "Trammel", "Ilshenar", "Malas", "Tokuno", "Ter Mur")
        COMPASS = ("E", "SE", "S", "SW", "W", "NW", "N", "NE")   # clockwise from east (y grows south)
        W = 420                               # full window
        MINI_W, MINI_H = 280, 46              # minimized bar
        BODY_H = 128                          # the YOUR CORPSE section
        CFG_H1, CFG_H2, CFG_H4 = 112, 66, 66  # the settings page's sections (GET MY THINGS: cfg_h3)
        # -----------------------------------------------------------------------------

        H = Kit.MARGIN + 30 + Kit.GAP + BODY_H + Kit.MARGIN
        settings = {"arrow": True, "restore": True, "ping": False, "decay": DEFAULT_DECAY_MIN,
                    "bones": DEFAULT_BONES_MIN, "say": False}
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
              "rec": None,            # the corpse: {"serial", "x", "y", "facet", "died", "body", "spot",
              #                         "exact"} (exact: the death was seen, so is its time)
              "was_dead": None,       # IsDead on the last tick (None: not read yet)
              "body": 0, "body_at": 0.0,
              "seek_until": 0.0, "seek_at": 0.0, "look_at": 0.0, "gone_since": None, "item_at": 0.0,
              "warned": False, "arrow": None, "ping": None, "job": None,
              "lbl_at": 0.0, "note": "", "note_until": 0.0, "name": "", "drawn": None, "drawn_c": None,
              "last_now": None,       # time.time() of the last tick (to see the clock set back)
              "refused": set(),       # items of this corpse the server refused: never tried again
              "maybe": None}          # (serial, x, y): a corpse that may be yours, offered while the
        #                               spot isn't known; Get my things takes it (2.6.81)
        win = {"g": None, "c": {}, "store": ({}, {})}
        page = {"c": None, "typed": {}}


        # ---------- saved settings ----------
        def load_settings():
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = [s.strip() for s in part.split("=", 1)]
                if k in ("arrow", "restore", "ping", "say"):
                    settings[k] = v == "1"
                elif k in ("decay", "bones"):
                    try:
                        settings[k] = max(MIN_LO, min(MIN_HI, int(v)))
                    except ValueError:
                        pass
            if (settings["decay"], settings["bones"]) == OLD_DEFAULTS:
                settings["decay"], settings["bones"] = DEFAULT_DECAY_MIN, DEFAULT_BONES_MIN


        def save_settings():
            Kit.put_var(SETTINGS_KEY, "arrow=%d;restore=%d;ping=%d;decay=%d;bones=%d;say=%d" % (
                1 if settings["arrow"] else 0, 1 if settings["restore"] else 0,
                1 if settings["ping"] else 0, settings["decay"], settings["bones"],
                1 if settings["say"] else 0))


        def load_rec():
            """The corpse remembered: "1|serial|x|y|facet|died|body|spot|exact" (spot 0:
            the place isn't known yet, the corpse is being looked for round you;
            exact 0: you were found dead at the start, so the time of death is a
            guess and the countdown an upper bound)."""
            p = Kit.get_var(CORPSE_KEY).split("|")
            if len(p) < 8 or p[0] != "1":
                return None
            try:
                return {"serial": int(p[1]), "x": int(p[2]), "y": int(p[3]), "facet": int(p[4]),
                        "died": float(p[5]), "body": int(p[6]), "spot": p[7] == "1",
                        "exact": len(p) < 9 or p[8] != "0"}
            except ValueError:
                return None


        def save_rec():
            r = st["rec"]
            if r is None:
                Kit.put_var(CORPSE_KEY, "")
                return
            Kit.put_var(CORPSE_KEY, "1|%d|%d|%d|%d|%.0f|%d|%d|%d" % (
                r["serial"], r["x"], r["y"], r["facet"], r["died"], r["body"], 1 if r["spot"] else 0,
                1 if r["exact"] else 0))


        # ---------- small helpers ----------
        def say(text, hue=None):
            API.SysMsg("%s: %s" % (TITLE, text), Kit.HUE_INFO if hue is None else hue)


        def note(text, secs=6.0):
            """A line in the window (and the journal) for a few seconds."""
            st["note"], st["note_until"] = text, time.time() + secs
            st["lbl_at"] = 0.0
            say(journal_case(text))


        def compass(dx, dy):
            if not dx and not dy:
                return ""
            return COMPASS[int(round(math.atan2(dy, dx) / (math.pi / 4))) % 8]


        def facet_name(m):
            return FACETS[m] if 0 <= m < len(FACETS) else "facet %d" % m


        def total_secs():
            return 60.0 * (settings["decay"] + settings["bones"])


        def remaining(now):
            r = st["rec"]
            if r is None:
                return 0.0
            if r["died"] > now:                    # the clock was set back: count from now
                r["died"] = now
            return total_secs() - (now - r["died"])


        def clock(secs):
            secs = max(0, int(secs))
            return "%d:%02d" % (secs // 60, secs % 60)


        def where_text(dx, dy):
            d = max(abs(dx), abs(dy))
            if d == 0:
                return "under you"
            return "%d tile%s %s" % (d, "" if d == 1 else "s", compass(dx, dy))


        def item_of(serial):
            if not serial:
                return None
            try:
                return API.FindItem(serial)
            except Exception:
                return None


        def held_item():
            try:
                return int(API.GetHeldItem() or 0)
            except Exception:
                return 0


        def cursor_up():
            """Another module's cursor or pick, or any target cursor up (a spell of
            yours being aimed): never moved over."""
            try:                                    # (plain tries: this runs on every tick of a run)
                if HOST.cursor_busy(KEY):
                    return True
            except Exception:
                pass
            try:
                return bool(API.HasTarget())
            except Exception:
                return False


        def is_hair(it):
            try:
                g = int(it.Graphic)
            except Exception:
                return False
            if HAIR_FIRST <= g <= HAIR_LAST:
                return True
            try:
                d = it.GetItemData()
                return d is not None and int(d.Layer) in HAIR_LAYERS
            except Exception:
                return False


        def weight_of(it):
            """Stones the item adds (tiledata weight x amount, a bag with what the
            client knows is in it); 0 when it can't be told."""
            try:
                d = it.GetItemData()
                w = int(d.Weight) if d is not None else 0
            except Exception:
                w = 0
            if w >= 255:                            # tiledata's "can't be moved"
                w = 0
            try:
                n = int(it.Amount or 1)
            except Exception:
                n = 1
            total = w * max(1, n)
            try:
                if it.IsContainer:
                    for x in (API.ItemsInContainer(int(it.Serial), True) or []):
                        try:
                            d = x.GetItemData()
                            xw = int(d.Weight) if d is not None else 0
                            if xw < 255:
                                total += xw * max(1, int(x.Amount or 1))
                        except Exception:
                            continue
            except Exception:
                pass
            return total


        # ---------- the window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)


        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])


        def build_window():
            w, h = (MINI_W, MINI_H) if st["minimized"] else (W, H)
            x, y = Kit.load_pos(POS_KEY, (220, 220), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            M = Kit.MARGIN
            store = ({}, {})
            c = {}
            g = G.CreateGump(True, True)
            if st["minimized"]:
                c["mini"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
            else:
                IW = w - 2 * M
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, BODY_H, "YOUR CORPSE  (where, and how long it lasts)")
                c["where"] = Kit.add_label(g, "", M + 12, yb + 28, Kit.HUE_TEXT)
                c["decay"] = Kit.add_label(g, "", M + 12, yb + 48, Kit.HUE_INFO)
                c["info"] = Kit.add_label(g, "", M + 12, yb + 68, Kit.HUE_INFO)
                by = yb + 92
                xb = M + 10
                c["go"] = Kit.art_button(g, store, "go", Kit.ART_PLAY, xb, by, "Get my things",
                                         "Open your corpse and move your things back into your "
                                         "backpack one at a time (stand next to it). Click again "
                                         "to stop.", on_click=queue("go"))
                xb += 35 + max(Kit.text_w("Get my things"), Kit.text_w("Stop")) + 14
                Kit.art_button(g, store, "help", Kit.ART_PLAY, xb, by, "Ping for help",
                               "Send a Need help map ping on your corpse to your guild (needs "
                               "World Map > Map Pings on)", on_click=queue("help"))
                xb += 35 + Kit.text_w("Ping for help") + 14
                Kit.art_button(g, store, "forget", Kit.ART_CLOSE, xb, by, "Forget",
                               "Forget this corpse and take its arrow down", on_click=queue("forget"))
            Kit.place(g, x, y, w, h)                     # wholly on screen (the window rules)
            win.update({"g": g, "c": c, "store": store})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))      # saved the moment you let go of it
            if st["minimized"] and st["docked"]:         # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            st["lbl_at"] = 0.0
            Kit.dispose(old)


        def show_full():
            """Back to the full window (a death, with "Open the Corpse window when
            you die" on)."""
            if not st["minimized"] and not st["docked"]:
                return
            st["minimized"], st["docked"] = False, False
            HOST.dock_forget(KEY)
            Kit.save_min(MIN_KEY, False)
            build_window()


        def texts(me, now, mm):
            """(where, where hue, decay, decay hue, info, mini) for the window."""
            r = st["rec"]
            j = st["job"]
            if r is None:
                dead = bool(st["was_dead"])
                info = st["note"] if st["note"] and now < st["note_until"] else \
                    ("Find a healer or a resurrection." if dead else
                     "When you die, this window shows the way back.")
                return ("No corpse to find.", Kit.HUE_TEXT, "", Kit.HUE_INFO, info, TITLE + ": none")
            left = remaining(now)
            try:
                mx, my = int(me.X), int(me.Y)
            except Exception:
                mx, my, mm = r["x"], r["y"], r["facet"]
            if not r["spot"]:
                where, mini = "Looking for your corpse round you...", "looking"
            elif mm != r["facet"]:
                where = "On %s, at %d, %d" % (facet_name(r["facet"]), r["x"], r["y"])
                mini = facet_name(r["facet"])
            else:
                wt = where_text(r["x"] - mx, r["y"] - my)
                where = "%s%s, at %d, %d" % (wt[0].upper(), wt[1:], r["x"], r["y"])
                mini = wt
            bones_at = 60.0 * settings["bones"]
            most = "" if r["exact"] else "at most "
            if left > bones_at:
                decay = "Bones in %s%s, gone in %s%s" % (most, clock(left - bones_at), most,
                                                         clock(left))
            elif left > 0:
                decay = "Bones %s; gone in %s%s" % ("now" if r["exact"] else "soon", most, clock(left))
            else:
                decay = "Should have decayed by now"
            dhue = Kit.HUE_BAD if left <= RED_SECS else Kit.HUE_INFO
            if st["note"] and now < st["note_until"]:
                info = st["note"]
            elif j is not None:
                if j["phase"] == "open":
                    info = "Opening your corpse..."
                else:
                    info = "Moving %d / %d" % (min(j["i"], len(j["plan"])), len(j["plan"]))
            else:
                died = ("Died %s ago." % ago(now - r["died"])) if r["exact"] else "Found as a ghost."
                mb = st["maybe"]
                if not r["serial"] and mb is not None:        # 2.6.81: taken only on your press
                    info = "A corpse at %d, %d may be yours: click Get my things." % (mb[1], mb[2])
                elif st["was_dead"]:
                    info = died + " Be resurrected, then click Get my things."
                elif r["serial"] and r["spot"]:
                    info = died + " Stand by it and click Get my things."
                else:
                    info = died + " Not seen there yet."
            mini = "%s  %s" % (mini, clock(left)) if left > 0 else mini
            return where, Kit.HUE_TEXT, decay, dhue, info, "%s: %s" % (TITLE, mini)


        def ago(secs):
            secs = max(0, int(secs))
            if secs < 60:
                return "%ds" % secs
            if secs < 3600:
                return "%dm" % (secs // 60)
            return "%dh %dm" % (secs // 3600, (secs % 3600) // 60)


        def refresh(me, now, mm, force=False):
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return                                       # folded: nothing is drawn
            if not force and now < st["lbl_at"]:
                return
            st["lbl_at"] = now + LABEL_EVERY
            where, whue, decay, dhue, info, mini = texts(me, now, mm)
            c = win["c"]
            if st["minimized"]:
                hue = Kit.HUE_BAD if st["rec"] is not None and remaining(now) <= RED_SECS \
                    else Kit.HUE_INFO
                sig = (mini, hue)
            else:
                sig = (where, whue, decay, dhue, info, st["job"] is not None)
            # 2.6.82: the same texts on the same controls: nothing to fit or set
            if sig == st["drawn"] and c is st["drawn_c"]:
                return
            st["drawn"], st["drawn_c"] = sig, c
            if st["minimized"]:
                lbl = c.get("mini")
                if lbl is not None:
                    Kit.set_text(lbl, Kit.fit(mini, MINI_W - 90), hue)
                return
            IW = W - 2 * Kit.MARGIN - 24
            Kit.set_text(c["where"], Kit.fit(where, IW), whue)
            Kit.set_text(c["decay"], Kit.fit(decay, IW), dhue)
            Kit.set_text(c["info"], Kit.fit(info, IW), Kit.HUE_INFO)
            Kit.set_text(c["go"], "Stop" if st["job"] is not None else "Get my things",
                         Kit.HUE_TITLE if st["job"] is not None else Kit.HUE_TEXT)


        # ---------- the arrow ----------
        def arrow_tick(me, mm):
            r = st["rec"]
            want = None
            if settings["arrow"] and r is not None and r["spot"] and mm == r["facet"]:
                try:
                    d = max(abs(int(me.X) - r["x"]), abs(int(me.Y) - r["y"]))
                except Exception:
                    d = REACH + 1
                if d > REACH:
                    want = (r["x"], r["y"])
            if want == st["arrow"]:
                return
            if want is None:
                clear_arrow()
            else:
                try:
                    API.TrackingArrow(want[0], want[1], ARROW_ID)
                    st["arrow"] = want
                except Exception:
                    st["arrow"] = None


        def clear_arrow():
            if st["arrow"] is not None:
                st["arrow"] = None
                safe(lambda: API.TrackingArrow(-1, -1, ARROW_ID))   # ours only (its id)


        # ---------- death, the corpse ----------
        def on_death(me, now, at_start=False):
            """You died (or were found dead when the module started)."""
            if st["job"] is not None:
                stop_job("you died")
            try:
                x, y, m = int(me.X), int(me.Y), int(API.GetMap())
            except Exception:
                return
            st["name"] = str(safe(lambda: me.Name, "") or "")
            # found dead at start: the ghost may have wandered off, so the corpse is
            # looked for round you, and the place is known only once it is seen
            st["rec"] = {"serial": 0, "x": x, "y": y, "facet": m, "died": now, "body": st["body"],
                         "spot": not at_start, "exact": not at_start}
            st["seek_until"], st["seek_at"] = now + FIND_SECS, now
            st["gone_since"], st["warned"], st["maybe"] = None, False, None
            st["refused"] = set()
            save_rec()
            if at_start:
                say("you are a ghost: looking for your corpse round you.")
            else:
                say("you died at %d, %d (%s). Your corpse turns to bones in %d minute%s and is "
                    "gone %d minute%s later." % (x, y, facet_name(m), settings["decay"],
                                                 "" if settings["decay"] == 1 else "s",
                                                 settings["bones"],
                                                 "" if settings["bones"] == 1 else "s"), Kit.HUE_BAD)
                if settings["ping"]:
                    st["ping"] = (x, y, m, now + PING_TRY)
            if settings["restore"]:
                show_full()


        CORPSE_PREFIXES = ("a corpse of ", "corpse of ", "the remains of ", "remains of ")
        NAME_LOW = ["", ""]                          # st["name"], and it stripped and lower case


        def mine(it, strict=False, graphic=CORPSE_GRAPHIC):
            """Is this corpse yours? Its body (the corpse's amount) and, when the
            client knows a name for it, your name. 2: yours by name; 1: could be
            (a body that fits and nothing to tell by); 0: not yours. strict (the
            spot isn't known): only 2 counts; a 1 is only offered (find_corpse).
            2.6.81: the name must equal yours once "a corpse of " and the like are
            cut off (it was a substring test, so "al" matched "alice"), and a body
            alone is never enough while the spot isn't known."""
            r = st["rec"]
            body = r["body"] if r is not None else 0
            try:
                amt = int(it.Amount or 0)
            except Exception:
                amt = 0
            if body and amt and amt != body:
                return 0
            bones = BONES_FIRST <= graphic <= BONES_LAST
            if bones and (not amt or (not body and amt not in HUMAN_BODIES)):
                return 0                                          # decorative bones (amount 1)
            loose = 1 if (not strict or (body and amt == body) or amt in HUMAN_BODIES) else 0
            nm = st["name"]
            if nm != NAME_LOW[0]:                    # lowered once per name (2.6.82)
                NAME_LOW[0], NAME_LOW[1] = nm, nm.strip().lower()
            me_name = NAME_LOW[1]
            if not me_name:
                return loose
            try:
                n = str(it.Name or "")
            except Exception:
                n = ""
            if not n:
                try:
                    n = str(it.NameAndProps(False) or "")        # what the client holds; no wait
                except Exception:
                    n = ""
            n = n.strip().lower()
            owner = None
            for p in CORPSE_PREFIXES:
                if n.startswith(p):
                    owner = n[len(p):].strip()
                    break
            if owner is None:
                # nothing to tell by (a bones item may carry only its tiledata name)
                if not n or n in ("corpse", "a corpse") or bones:
                    return loose
                owner = n
            return 2 if owner == me_name else 0


        def scan_corpses(items, gr, strict, cx, cy, lim, acc):
            """Into acc = [best, maybe] from items, all of graphic gr (the client
            call filtered them: 2.6.82, the graphic isn't read per item): each
            (d, serial, x, y) or None. best is yours (by name, or by body when the
            spot is known); maybe a corpse that only could be yours (strict). The
            pick doesn't depend on the order the items come in."""
            need = 2 if strict else 1
            for it in items:
                try:
                    s, ix, iy = int(it.Serial), int(it.X), int(it.Y)
                except Exception:
                    continue
                d = max(abs(ix - cx), abs(iy - cy))
                if d > lim:
                    continue
                m = mine(it, strict, gr)
                if not m:
                    continue
                # the nearest; the newest (highest serial) of two as near
                e = (d, s, ix, iy)
                if m >= need:
                    best = acc[0]
                    if best is None or d < best[0] or (d == best[0] and s > best[1]):
                        acc[0] = e
                else:
                    maybe = acc[1]
                    if maybe is None or d < maybe[0] or (d == maybe[0] and s > maybe[1]):
                        acc[1] = e


        def find_corpse(me):
            """(hit, maybe): serial, x, y of your corpse in view, and of a corpse
            that may be yours (spot unknown, nothing to tell by); each or None.
            2.6.81: a corpse past its bones time is the same item with a bones
            graphic: looked for only when no corpse fits (2.6.82: one call per
            bones graphic, filtered by the client, not one over every item)."""
            r = st["rec"]
            strict = not r["spot"]
            if r["spot"]:
                cx, cy, lim = r["x"], r["y"], CORPSE_NEAR
            else:
                try:
                    cx, cy, lim = int(me.X), int(me.Y), SEEK_RANGE
                except Exception:
                    return None, None
            try:
                items = API.GetItemsOnGround(SEEK_RANGE, CORPSE_GRAPHIC) or ()
            except Exception:
                items = ()
            acc = [None, None]
            scan_corpses(items, CORPSE_GRAPHIC, strict, cx, cy, lim, acc)
            best, maybe = acc
            if best is None:
                acc = [None, None]
                for gr in BONES_GFX:
                    try:
                        items = API.GetItemsOnGround(SEEK_RANGE, gr)
                    except Exception:
                        continue
                    if items:
                        scan_corpses(items, gr, strict, cx, cy, lim, acc)
                best, m2 = acc
                if m2 is not None and (maybe is None or m2[0] < maybe[0]):
                    maybe = m2
            return (None if best is None else best[1:]), (None if maybe is None else maybe[1:])


        def forget(why=None):
            if st["job"] is not None:
                stop_job(None)
            st["rec"] = None
            st["maybe"] = None
            st["ping"] = None
            st["gone_since"] = None
            st["refused"] = set()
            clear_arrow()
            save_rec()
            if why:
                say(why)
            st["lbl_at"] = 0.0


        def take_maybe():
            """Get my things on a corpse that only may be yours (found as a ghost,
            nothing to tell it by): the press takes it as yours and moves nothing;
            the next press, beside it, does (2.6.81)."""
            r, mb = st["rec"], st["maybe"]
            if item_of(mb[0]) is None:
                note("That corpse isn't in view any more.")   # the next look drops it
                return
            st["maybe"] = None
            r["serial"], r["x"], r["y"], r["spot"] = mb[0], mb[1], mb[2], True
            save_rec()
            note("The corpse at %d, %d is taken as yours." % (mb[1], mb[2]))


        def corpse_tick(me, now, mm):
            r = st["rec"]
            left = remaining(now)
            try:
                dist = max(abs(int(me.X) - r["x"]), abs(int(me.Y) - r["y"]))
            except Exception:
                dist = 1 << 20
            if not r["serial"]:
                near = r["spot"] and mm == r["facet"] and dist <= LOOK_NEAR
                # 2.6.81: a corpse that may be yours stays offered (looked at once a second)
                offered = not r["spot"] and st["maybe"] is not None
                seeking = now < st["seek_until"]
                if (seeking and now >= st["seek_at"]) or \
                        (not seeking and (near or offered) and now >= st["look_at"]):
                    st["seek_at"] = now + FIND_EVERY
                    st["look_at"] = now + LOOK_EVERY
                    hit, maybe = find_corpse(me)
                    if hit is not None:
                        r["serial"], r["x"], r["y"] = hit
                        st["maybe"] = None
                        if not r["spot"]:
                            r["spot"] = True
                            say("found your corpse at %d, %d." % (r["x"], r["y"]))
                        save_rec()
                        st["lbl_at"] = 0.0
                    elif not r["spot"] and maybe != st["maybe"]:
                        st["maybe"] = maybe                   # never taken without your press
                        st["lbl_at"] = 0.0
                if not r["serial"] and not r["spot"] and now >= st["seek_until"] and st["maybe"] is None:
                    forget("your corpse isn't in view (it was left before %s started)." % TITLE)
                    return
            elif now >= st["item_at"] or st["item_at"] - now > ITEM_EVERY:
                # 2.6.82: looked up once a second, not every tick (a corpse doesn't
                # move; GONE_SECS waits 6 s anyway)
                st["item_at"] = now + ITEM_EVERY
                it = item_of(r["serial"])
                if it is not None:
                    st["gone_since"] = None
                    try:
                        ix, iy = int(it.X), int(it.Y)
                        if (ix or iy) and (ix, iy) != (r["x"], r["y"]) and not int(it.Container or 0):
                            r["x"], r["y"] = ix, iy
                            save_rec()
                    except Exception:
                        pass
                elif mm == r["facet"] and st["job"] is None and dist <= GONE_RANGE:
                    if st["gone_since"] is None:
                        st["gone_since"] = now
                    elif now - st["gone_since"] >= GONE_SECS:
                        forget("your corpse isn't at %d, %d any more (decayed or looted)."
                               % (r["x"], r["y"]))
                        return
                else:
                    st["gone_since"] = None
            if left <= WARN_SECS and not st["warned"] and left > 0:
                st["warned"] = True
                try:
                    dist = where_text(r["x"] - int(me.X), r["y"] - int(me.Y)) \
                        if mm == r["facet"] else "on " + facet_name(r["facet"])
                except Exception:
                    dist = "at %d, %d" % (r["x"], r["y"])
                HOST.alert(ALERT_DECAY, "Your corpse decays in under a minute (%s)" % dist, "warn")
            if left <= -DECAYED_GRACE and item_of(r["serial"]) is None:
                forget("your corpse has decayed.")


        def ping_tick(now):
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


        # ---------- Get my things ----------
        def start_job(me, now):
            r = st["rec"]
            if st["job"] is not None:
                return
            if r is None:
                note("No corpse remembered.")
                return
            if bool(st["was_dead"]):
                note("You are still a ghost: get resurrected first.")
                return
            if not r["serial"]:
                note("Your corpse hasn't been seen yet: go to %d, %d." % (r["x"], r["y"]))
                return
            it = item_of(r["serial"])
            if it is None:
                note("Your corpse isn't in view yet (%d, %d)." % (r["x"], r["y"]))
                return
            try:
                d = max(abs(int(it.X) - int(me.X)), abs(int(it.Y) - int(me.Y)))
            except Exception:
                d = REACH + 1
            if d > REACH:
                note("Walk up to your corpse first (%s)." % where_text(int(it.X) - int(me.X),
                                                                   int(it.Y) - int(me.Y)))
                return
            pack = safe(lambda: int(API.Backpack), 0) or 0
            if not pack:
                note("No backpack to put things in.")
                return
            if cursor_up():
                note("A target cursor is up: finish or cancel it first.")
                return
            if held_item():
                note("You are holding an item: put it down first.")
                return
            st["job"] = {"phase": "open", "corpse": r["serial"], "pack": pack, "at": now + OPEN_WAIT,
                         "until": now + OPEN_MAX, "plan": [], "i": 0, "tried": set(), "waits": {},
                         "move": None, "check": None, "sent_at": 0.0, "last": 0, "rechecks": 0,
                         "hold": 0.0, "moved": 0, "refused": 0, "streak": 0, "why": None,
                         "replans": 0, "jr": Journal.reader() if settings["say"] else None}
            API.UseObject(r["serial"])                     # opens it (the client learns what's in it)
            st["note"] = ""
            st["lbl_at"] = 0.0


        def make_plan(j):
            """Every item lying in the corpse that hasn't been tried (nor refused on an
            earlier press), hair aside."""
            try:
                items = API.ItemsInContainer(j["corpse"], False) or []
            except Exception:
                items = []
            plan = []
            for it in items:
                if len(plan) >= PLAN_CAP:
                    break
                try:
                    s = int(it.Serial)
                except Exception:
                    continue
                if s in j["tried"] or s in st["refused"] or is_hair(it):
                    continue
                plan.append(s)
            return plan


        def job_tick(me, now):
            j = st["job"]
            if j["jr"] is not None:                           # debug: the shard's replies
                for ln in j["jr"].new():
                    if ln.text and not ln.text.startswith(TITLE + ":"):
                        say("reply: " + ln.text.strip())
            if j["why"]:
                stop_job(j["why"])
                return
            if j["move"] is not None:
                return                                        # thread_tick sends it
            if st["was_dead"]:
                stop_job("you died")
                return
            it = item_of(j["corpse"])
            if it is None:
                stop_job("your corpse is gone from view")
                return
            try:
                d = max(abs(int(it.X) - int(me.X)), abs(int(it.Y) - int(me.Y)))
            except Exception:
                d = 0
            if d > REACH:
                stop_job("you walked away from your corpse")
                return
            if j["check"] is not None:
                if now < j["at"] or not check_move(j, now):
                    return
            if j["phase"] == "open":
                if now < j["at"]:
                    return
                plan = make_plan(j)
                if not plan and now < j["until"]:
                    return                                    # its items haven't arrived yet
                j["plan"], j["i"], j["phase"] = plan, 0, "move"
                if not plan:
                    finish_job()
                    return
            if now < j["hold"]:
                return
            if cursor_up():
                stop_job("a target cursor is up")
                return
            h = held_item()
            if h and h != j["last"]:                          # (the last move's item: the server's
                stop_job("you picked something up")           # answer to it is still on its way)
                return
            plan = j["plan"]
            while j["i"] < len(plan):
                s = plan[j["i"]]
                j["i"] += 1
                if s in j["tried"]:
                    continue
                x = item_of(s)
                try:
                    if x is None or int(x.Container or 0) != j["corpse"]:
                        continue                              # gone, or taken by hand meanwhile
                except Exception:
                    continue
                try:
                    wmax = int(me.WeightMax or 0)
                    wnow = int(me.Weight or 0)
                except Exception:
                    wmax = wnow = 0
                if wmax > 0 and (wnow >= wmax or wnow + weight_of(x) > wmax):
                    stop_job("the next item would put you over your weight limit (%d / %d stones)"
                             % (wnow, wmax))
                    return
                j["tried"].add(s)
                j["move"] = s
                return
            if j["replans"] < REPLAN:                         # anything that turned up meanwhile
                j["replans"] += 1
                more = make_plan(j)
                if more:
                    j["plan"], j["i"] = more, 0
                    return
            finish_job()


        def check_move(j, now):
            """The last move's answer, MOVE_GAP after it went out: True to go on,
            False when it waits a little longer (or stopped)."""
            s = j["check"]
            it = item_of(s)
            try:
                where = int(it.Container or 0) if it is not None else None
            except Exception:
                where = None
            if where is None and j["rechecks"] < MOVE_RECHECK:
                j["rechecks"] += 1                           # lifted, not answered yet (slow line)
                j["at"] = now + MOVE_GAP * 0.5
                return False
            if where != j["corpse"]:                         # in your pack (or stacked into a pile)
                j["moved"] += 1
                j["streak"] = j["rechecks"] = 0
                j["check"] = None
                return True
            if Journal.find(j["sent_at"], J_WAIT) is not None and j["waits"].get(s, 0) < WAIT_RETRY:
                j["waits"][s] = j["waits"].get(s, 0) + 1     # too soon for the server: the same item
                j["tried"].discard(s)
                j["i"] = max(0, j["i"] - 1)
                j["check"] = None
                j["rechecks"] = 0
                j["hold"] = now + MOVE_GAP
                return False
            if j["rechecks"] < MOVE_RECHECK:                 # no answer yet: a little later
                j["rechecks"] += 1
                j["at"] = now + MOVE_GAP * 0.5
                return False
            j["check"] = None
            j["rechecks"] = 0
            j["refused"] += 1
            j["streak"] += 1
            if len(st["refused"]) < PLAN_CAP:
                st["refused"].add(s)                         # each item gets one move, press or not
            if j["streak"] >= FAIL_STOP:
                stop_job("%d moves in a row were refused" % j["streak"])
                return False
            return True


        def send_move():
            """thread_tick: the move the client tick picked goes out, in one hop
            that looks at the cursor and your hand first."""
            j = st["job"]
            if j is None or j["move"] is None or st["shutting"]:
                return
            mv = j["move"]

            def run():
                if st["job"] is not j or j["move"] != mv or st["shutting"]:
                    return "gone"
                if cursor_up():
                    return "a target cursor is up"
                h = held_item()
                if h and h != j["last"]:
                    return "you picked something up"
                API.MoveItem(mv, j["pack"])
                return "sent"
            try:
                res = Kit.on_client(run)
            except Exception as ex:
                res = "a move failed (%s)" % ex
            if st["job"] is not j:
                return
            j["move"] = None
            if res == "sent":
                j["check"] = mv
                j["last"] = mv
                j["sent_at"] = time.time()
                j["at"] = j["sent_at"] + MOVE_GAP
            elif res != "gone":
                j["why"] = res                               # the next tick stops it and says why


        def finish_job():
            j, st["job"] = st["job"], None
            if j is None:
                return
            left = []
            if item_of(j["corpse"]) is not None:
                left = make_plan({"corpse": j["corpse"], "tried": set()})
            n_ref = len(st["refused"])
            if j["moved"] == 0 and not j["refused"] and not left:
                forget("nothing left in your corpse%s." % (
                    (" but %d item%s the server refused (take %s by hand)"
                     % (n_ref, "" if n_ref == 1 else "s", "it" if n_ref == 1 else "them"))
                    if n_ref else ""))
                return
            msg = "%d item%s back in your backpack" % (j["moved"], "" if j["moved"] == 1 else "s")
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
            j, st["job"] = st["job"], None
            if j is None:
                return
            if user:
                say("stopped (%d moved)." % j["moved"])
            elif why:
                say("stopped: %s (%d moved)." % (why, j["moved"]), Kit.HUE_BAD)
            st["lbl_at"] = 0.0


        # ---------- settings page ----------
        def config_height(w):
            return (CFG_H1 + Kit.GAP + CFG_H2 + Kit.GAP + cfg_h3(w) + Kit.GAP + ATLAS_H + Kit.GAP
                    + CFG_H4)


        def cfg_h3(w):
            return 30 + 20 * len(Kit.wrap(MOVE_HINT, w - 28)) + 10


        MOVE_HINT = ("Moves one item every %.1f s and stops when you click Stop, raise a target "
                     "cursor, pick something up, walk away or would go over your weight limit."
                     % MOVE_GAP)


        def build_config(g, x, y, w):
            c = {}
            Kit.add_section(g, x, y, w, CFG_H1, "WHEN YOU DIE  (the arrow, this window, a ping)")
            c["arrow"] = Kit.add_check(g, "Point the tracking arrow at your corpse", x + 12, y + 30,
                                       settings["arrow"], "Shows a tracking arrow of its own to the "
                                       "corpse (other arrows are left alone); it hides when you "
                                       "stand beside it")
            c["restore"] = Kit.add_check(g, "Open the Corpse window when you die, even minimized or folded",
                                         x + 12, y + 56, settings["restore"],
                                         "The window comes back full size when you die")
            c["ping"] = Kit.add_check(g, "Send a Need help map ping on your corpse when you die",
                                      x + 12, y + 82, settings["ping"],
                                      "Your guild sees a Need help ping where you died (needs World "
                                      "Map > Map Pings on). Off at first: it tells them where you are")
            y2 = y + CFG_H1 + Kit.GAP
            Kit.add_section(g, x, y2, w, CFG_H2, "DECAY  (minutes; the shard's times)")
            t1, t2 = "Corpse to bones:", "Bones gone after:"
            Kit.add_label(g, t1, x + 12, y2 + 34)
            x1 = x + 12 + Kit.text_w(t1) + 10
            c["decay"] = Kit.add_textbox(g, str(settings["decay"]), x1, y2 + 30, 40)
            safe(lambda: c["decay"].SetTooltip("Minutes from your death until the corpse turns to "
                                               "bones (%d-%d)" % (MIN_LO, MIN_HI)))
            x2 = x1 + 40 + 24
            Kit.add_label(g, t2, x2, y2 + 34)
            c["bones"] = Kit.add_textbox(g, str(settings["bones"]), x2 + Kit.text_w(t2) + 10,
                                         y2 + 30, 40)
            safe(lambda: c["bones"].SetTooltip("Minutes the bones (your things still in them) last "
                                               "before they decay (%d-%d)" % (MIN_LO, MIN_HI)))
            y3 = y2 + CFG_H2 + Kit.GAP
            h3 = cfg_h3(w)
            Kit.add_section(g, x, y3, w, h3, "GET MY THINGS  (one item at a time)")
            for i, line in enumerate(Kit.wrap(MOVE_HINT, w - 28)):
                Kit.add_label(g, line, x + 12, y3 + 30 + i * 20, Kit.HUE_INFO)
            y4 = y3 + h3 + Kit.GAP
            atlas_section(g, x, y4, w, "corpse")
            y5 = y4 + ATLAS_H + Kit.GAP
            Kit.add_section(g, x, y5, w, CFG_H4, "DEBUG  (for checking the shard's texts)")
            c["say"] = Kit.add_check(g, "Print the shard's replies in the journal",
                                     x + 12, y5 + 30, settings["say"],
                                     "While Get my things runs, every journal line is repeated as "
                                     "\"%s: reply: ...\", for checking the shard's texts" % TITLE)
            page["c"] = c


        def poll_config(force=False):
            c = page["c"]
            if c is None:
                return
            changed = False
            now = time.time()
            try:
                for k in ("arrow", "restore", "ping", "say"):
                    v = bool(c[k].IsChecked)
                    if v != settings[k]:
                        settings[k], changed = v, True
                for k in ("decay", "bones"):
                    txt = str(c[k].Text or "").strip()
                    # 2.6.81: a minute field applies once its text has stood TYPE_SETTLE s (or
                    # the page closes), so a half-typed value ("4" on the way from 45 to 40)
                    # never moves the countdown, fires its alert or forgets the corpse
                    t = page["typed"].get(k)
                    if t is None or t[0] != txt:
                        page["typed"][k] = (txt, now)
                        if not force:
                            continue
                    elif not force and now - t[1] < TYPE_SETTLE:
                        continue
                    if txt.isdigit():
                        v = max(MIN_LO, min(MIN_HI, int(txt)))
                        if v != settings[k]:
                            settings[k], changed = v, True
                            st["warned"] = False              # the countdown changed
            except Exception:
                page["c"] = None
                return
            if changed:
                save_settings()
                st["lbl_at"] = 0.0
                if not settings["arrow"]:
                    clear_arrow()


        def config_closed():
            poll_config(True)                     # 2.6.81: what was typed last still applies
            page["c"] = None
            page["typed"] = {}


        # ---------- the computer's clock set back ----------
        def rebase(d):
            """The clock went back (d < 0 seconds since the last tick): every time
            kept moves with it, so no wait lasts as long as the jump (the window's
            texts, the search for the corpse, a run half way) and the countdown
            keeps the real time left."""
            for k in ("body_at", "seek_until", "seek_at", "look_at", "item_at", "lbl_at", "note_until"):
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


        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "job": None, "arrow": None,
                       "refused": set(),
                       "ping": None, "was_dead": None, "seek_until": 0.0, "seek_at": 0.0,
                       "look_at": 0.0, "gone_since": None, "item_at": 0.0, "lbl_at": 0.0, "note": "",
                       "last_now": None, "atlas": False, "maybe": None,
                       "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            load_settings()
            st["rec"] = load_rec()
            st["warned"] = False
            if st["rec"] is not None and remaining(time.time()) <= -DECAYED_GRACE:
                st["rec"] = None                              # long decayed while you were away
                save_rec()
            if st["rec"] is not None and not st["rec"]["spot"]:
                st["seek_until"] = time.time() + FIND_SECS    # still being looked for round you
            safe(lambda: HOST.alert_kind(ALERT_DECAY, "Corpse about to decay", ALERT_DECAY_SOUND))
            build_window()
            HOST.dock_add(KEY, _dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"), scale=True))


        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])                         # on_disposed turns the module off
                return
            now = time.time()
            last, st["last_now"] = st["last_now"], now
            if last is not None and now < last - CLOCK_JUMP:
                rebase(now - last)                            # the clock was set back
            # the pass's memo of the player (2.6.82): its X / Y are read once, not in
            # corpse_tick, arrow_tick and texts each
            me = HOST.me()
            while st["queue"]:
                action = st["queue"].pop(0)
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
                elif action == "go":
                    if st["job"] is not None:
                        stop_job(None, user=True)
                    elif st["rec"] is not None and not st["rec"]["serial"] and st["maybe"] is not None:
                        take_maybe()                          # 2.6.81: this press only confirms
                    elif me is not None:
                        start_job(me, now)
                elif action == "help":
                    r = st["rec"]
                    if r is None or not r["spot"]:
                        note("No corpse to ping.")
                    elif HOST.services.get("pings.send") is None:
                        note("World Map > Map Pings is off: turn it on to send pings.")
                    else:
                        st["ping"] = (r["x"], r["y"], r["facet"], now + PING_TRY)
                elif action == "forget":
                    if st["rec"] is None:
                        note("No corpse remembered.")
                    else:
                        forget("forgot your corpse.")
            if me is None:
                return
            try:
                dead = bool(me.IsDead)
            except Exception:
                return
            was = st["was_dead"]
            st["was_dead"] = dead
            if was is None:                                   # the first look since the start
                if dead and st["rec"] is None:
                    on_death(me, now, at_start=True)
            elif dead and not was:
                on_death(me, now)
            elif was and not dead and st["rec"] is not None:
                r = st["rec"]
                if r["spot"]:
                    try:
                        wt = where_text(r["x"] - int(me.X), r["y"] - int(me.Y))
                    except Exception:
                        wt = "at %d, %d" % (r["x"], r["y"])
                    say("you are alive. Your corpse is %s: click Get my things beside it." % wt,
                        Kit.HUE_GOOD)
                st["lbl_at"] = 0.0
            if not dead and now >= st["body_at"]:
                st["body_at"] = now + BODY_EVERY
                try:
                    st["body"] = int(me.Graphic)
                    st["name"] = str(me.Name or "") or st["name"]
                except Exception:
                    pass
            mm = None
            if st["rec"] is not None:
                try:
                    mm = int(API.GetMap())
                except Exception:
                    mm = -1
                corpse_tick(me, now, mm)
            if st["job"] is not None:
                job_tick(me, now)
            if st["ping"] is not None:
                ping_tick(now)
            if st["rec"] is not None or st["arrow"] is not None:
                if mm is None:
                    try:                                      # plain try (2.6.82)
                        mm = int(API.GetMap())
                    except Exception:
                        mm = -1
                arrow_tick(me, mm)
            r = st["rec"]                                     # on TazUO's World Map (2.6.51)
            sig = (r["x"], r["y"], r["facet"]) if r is not None and r["spot"] else None
            if sig != st["atlas"]:
                st["atlas"] = sig
                ATLAS.set("corpse", {} if sig is None else
                          {atlas_name("Your corpse"): (sig[0], sig[1], sig[2], "white")})
            refresh(me, now, mm)


        def _thread_tick():
            """Script thread, right after the client tick: a move waiting to go out."""
            j = st["job"]
            if j is not None and j["move"] is not None and not st["shutting"]:
                send_move()


        def _interval():
            return TICK_BUSY if st["job"] is not None else TICK_IDLE


        def _thread_wanted():
            """(2.6.82) A script-thread pass only with a move to send."""
            j = st["job"]
            return j is not None and j["move"] is not None


        def _stop():
            st["shutting"] = True
            st["job"] = None
            st["ping"] = None
            HOST.dock_remove(KEY)
            clear_arrow()                                     # ours only; back at the next start
            save_pos()
            Kit.save_min(MIN_KEY, st["minimized"])
            save_settings()
            g, win["g"] = win["g"], None
            win["c"] = {}
            Kit.dispose(g)


        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,          # tick on the client thread: no waits in it
                  "thread_tick": _thread_tick,  # the moves go out from the script's thread
                  "thread_wanted": _thread_wanted,
                  "interval": _interval,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    def _part_maps():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the Virtue Assistant script from
        #  this file uses (API, G, safe, Client, Kit, Follow, HOST, Journal, the main
        #  on its Modules tab.
        # ============================ MODULE START ===================================
        #  MODULE: Treasure Maps (Treasure Hunter before 2.6.52)  -  your treasure
        #  maps and where to dig
        #
        #  Lists the treasure maps in your backpack (bags inside it too): each map's
        #  level, whether it is decoded, and for a decoded map its dig spot with the
        #  distance and direction from you. The client's tracking arrow points at
        #  the nearest spot on your facet (or at the map you click), and a button on
        #  each row sends a Go here map ping on its spot through Map Pings.
        #
        #  Where the spot comes from: open (double-click) a decoded map once. The
        #  server draws the map and puts its pin on it; TazUO keeps both in its map
        #  window, and this module reads them from there the moment the pin arrives
        #  (once per opening, nothing sent to the server) and remembers the spot by
        #  the map's serial, per character, so it is known from then on, also after
        #  a restart. TazUO also prints its own estimate of the spot in the journal
        #  ("I can't be certain but I believe this is somewhere near X and Y."); it
        #  takes a 300-pixel map for granted, so the spot is worked out here from
        #  the pin's pixel, the map's bounds and its real width. When the client's
        #  map window can't be read, that journal line and the map you just
        #  double-clicked are used instead.
        #
        #  Level, decoded or not, the facet and "completed" come from the map's name
        #  and properties as the client has them ("a tattered, adeptly drawn
        #  treasure map", "for somewhere in Felucca", "completed by ..."). Rows are
        #  about items, not mobiles: nothing to follow.
        #
        #  Display only: nothing here digs, decodes or moves anything.
        # =============================================================================
        KEY = "treasure"
        TITLE = "Treasure Maps"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "TreasureHunter_settings"   # per character: the options (the old name stays)
        MAPS_KEY = "TreasureHunter_maps"           # per character: the dig spots read
        POS_KEY = "TreasureHunter_pos"
        MIN_KEY = "TreasureHunter_min"
        W = 560                               # full window width
        MINI_W, MINI_H = 320, 46              # minimized bar
        ROWS = 8                              # rows per page of the list
        ROW_H = 24
        TRAY_ICON = 0x14EB                    # a map, on the Action Bar's tray button
        ARROW_ID = 0x54524541                 # "TREA": our own tracking arrow (Map Pings: "PING")
        MAP_GRAPHICS = (0x14EB, 0x14EC)       # item art of maps (Tiledata "map")
        TREASURE_TEXT = "treasure map"        # in the name of every treasure map (cliloc 1041510-1041521)
        UNDECODED_TEXT = "tattered"           # "a tattered, plainly drawn treasure map": not decoded
        LEVELS = (("youthful", 0), ("plainly", 1), ("expertly", 2), ("adeptly", 3),
                  ("cleverly", 4), ("deviously", 5), ("ingeniously", 6))   # cliloc 1041510-1063453
        LEVEL_NAMES = ("Youthful", "Plainly drawn", "Expertly drawn", "Adeptly drawn",
                       "Cleverly drawn", "Deviously drawn", "Ingeniously drawn")
        FACETS = ("Felucca", "Trammel", "Ilshenar", "Malas", "Tokuno", "Ter Mur")
        PROP_FACETS = (("somewhere in felucca", 0), ("somewhere in trammel", 1),   # 1041502 / 03
                       ("somewhere in ilshenar", 2), ("somewhere in malas", 3),    # 1060850 / 51
                       ("somewhere in tokuno", 4), ("somewhere in ter mur", 5))
        DONE_TEXT = "completed by"            # cliloc 1041507 "completed by ~1_val~"
        J_DECODED = "you successfully decode a treasure map"     # cliloc 503019
        J_SHOWN = "the treasure is marked by the red pin"        # cliloc 503017
        J_DONE = "this treasure hunt has already been completed"  # cliloc 503014
        J_ESTIMATE = re.compile(r"believe this is somewhere near (\d+) and (\d+)")  # TazUO's own line
        TAZ_SCALE = 300.0                     # the map width TazUO's estimate takes for granted
        SCAN_EVERY = 1.0                      # seconds between looks at the maps in your pack
        LOOK_FOR = 6.0                        # seconds to watch for an opened map window after a
        #                                       map is double-clicked or the shard shows one
        LOOK_EVERY = 0.25                     # seconds between those looks
        TM_HINT = 1.5                         # seconds: with no double-click seen, a map window read
        #                                       this soon after the shard's "marked by the red pin"
        #                                       counts as a treasure map's
        USED_KEEP = 8.0                       # seconds a double-clicked map stays "the map just
        #                                       opened" (for the journal fallback)
        SAVE_EVERY = 5.0                      # seconds between saves of the spots (when changed)
        MAX_MAPS = 60                         # spots remembered at most (oldest seen dropped)
        FORGET_DAYS = 60                      # a spot of a map not seen in your pack this long goes
        MAX_PACK_MAPS = 100                   # maps listed at most
        PING_TRY_FOR = 6.0                    # seconds a Go here ping waits for Map Pings' pace
        PING_RETRY = 0.5
        LOOK_TIP = "Point the tracking arrow at this map's spot (click again: back to the nearest map)"
        LOOK_TIP_ON = "Send the tracking arrow back to the nearest map's spot"
        # 2.6.81: with "Point the tracking arrow at the nearest map's spot" unticked
        # a second click takes the arrow down (there is no nearest map to go back to)
        LOOK_TIP_MAN = "Point the tracking arrow at this map's spot (click again: take the tracking arrow down)"
        LOOK_TIP_MAN_ON = "Take the tracking arrow down"
        ARROW_LOOK = 1.5                      # seconds after showing the arrow before it is looked for
        PING_TIP = "Send a Go here map ping on this map's spot (needs World Map > Map Pings on)"
        EMPTY_TEXT = "No treasure maps in your pack. Put one in it and double-click it once."
        # -----------------------------------------------------------------------------

        settings = {"auto": True, "undecoded": True, "done": False, "say": False}
        st = {"shutting": False, "active": False, "minimized": False, "docked": False,
              "queue": [], "used": [], "last_map": (0, 0.0), "look_until": 0.0,
              "next_look": 0.0, "est": None, "next_scan": 0.0, "dirty": False,
              "next_save": 0.0, "list": [], "list_ver": 0, "list_sig": None, "atlas_sig": None,
              "me": (0, 0, -1), "pin": 0, "arrow_off": False, "arrow": None, "ping": None,
              "page": 0, "hooked": False, "drawn": None, "tm_at": 0.0,
              "tm_serial": 0, "hidden": 0, "in_pack": frozenset()}
        spots = {}        # map serial -> {"x", "y", "f", "lvl", "done", "t"}: the dig spots read
        parsed = {}       # map serial -> (its name and properties text, what they say, read again at)
        TEXT_EVERY = 5.0  # seconds a map's name and properties are kept before they are read again
        #                   (2.6.82; read every scan before; "completed" and a map window shown
        #                   read them all again at once, and a map still without them every scan)
        TEXT_ALL = [False]  # the next scan reads every map's text again
        asked = set()     # serials whose properties were asked of the server once
        read_gumps = {}   # map serial -> the map window already read (one read per opening)
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        page = {"c": None, "store": ({}, {})}
        JR = {"rd": None}

        # ---------- small helpers ----------
        BANK_EVERY = 5.0                 # (2.6.85) seconds between looks in the open bank box
        BANK_CAP = 2000                  # ...and how many of its items one look reads
        DIG_HUE = 0x0035                 # (2.6.85) the dig spot's tile highlight (gold)
        bank_st = {"at": 0.0, "items": []}

        def facet_name(f):
            return FACETS[f] if 0 <= f < len(FACETS) else "facet %d" % f

        def direction(dx, dy):
            """Compass direction in UO terms (+x east, +y south)."""
            if dx == 0 and dy == 0:
                return "here"
            deg = math.degrees(math.atan2(-dy, dx))
            if deg < 0:
                deg += 360
            return ("E", "NE", "N", "NW", "W", "SW", "S", "SE")[int(round(deg / 45.0)) % 8]

        def say(text, hue=None):
            try:
                API.SysMsg("%s: %s" % (TITLE, text), Kit.HUE_INFO if hue is None else hue)
            except Exception:
                pass

        def level_name(lvl):
            return LEVEL_NAMES[lvl] if 0 <= lvl < len(LEVEL_NAMES) else "Treasure map"

        # ---------- saved settings and spots ----------
        def load_settings():
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k = k.strip()
                if k in settings:
                    settings[k] = v.strip() == "1"

        def save_settings():
            Kit.put_var(SETTINGS_KEY, ";".join("%s=%d" % (k, 1 if settings[k] else 0)
                                               for k in ("auto", "undecoded", "done", "say")))

        def load_maps():
            spots.clear()
            cut = time.time() - FORGET_DAYS * 86400
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
            if len(spots) > MAX_MAPS:
                old = sorted(spots, key=lambda s: spots[s]["t"])
                for s in old[:len(spots) - MAX_MAPS]:
                    del spots[s]

        def save_maps():
            st["dirty"] = False
            parts = []
            for s in sorted(spots):
                r = spots[s]
                parts.append("%X,%d,%d,%d,%d,%d,%d,%d" % (s, r["x"], r["y"], r["f"], r["lvl"],
                                                         1 if r["done"] else 0, r["t"],
                                                         1 if r.get("approx") else 0))
            Kit.put_var(MAPS_KEY, ";".join(parts))

        # ---------- what a map's name and properties say ----------
        def parse(text):
            low = text.lower()
            name = low.split("\n", 1)[0]
            info = {"tm": TREASURE_TEXT in low, "lvl": -1, "dec": None, "f": -1,
                    "done": DONE_TEXT in low}
            for word, lvl in LEVELS:
                if word in name:
                    info["lvl"] = lvl
                    break
            if info["tm"]:
                info["dec"] = UNDECODED_TEXT not in name
            for t, f in PROP_FACETS:
                if t in low:
                    info["f"] = f
                    break
            return info

        def info_of(serial, it, now=None):
            """What the client knows of map `serial` (cached by its text; no waits:
            the client tick runs on the client thread). now: the scan's time, and
            the text is read again only TEXT_EVERY after the last read (2.6.82);
            None: read now."""
            hit = parsed.get(serial)
            if now is not None and hit is not None and now < hit[2] <= now + TEXT_EVERY:
                return hit[1]
            if now is None:
                now = time.time()
            text = ""
            try:
                text = str(API.ItemNameAndProps(serial, False) or "")
            except Exception:
                text = ""
            again = now + TEXT_EVERY                 # (its properties are known)
            if not text.strip():
                again = 0.0                          # not yet: read again next scan
                try:
                    text = str(it.Name or "")
                except Exception:
                    text = ""
                if serial not in asked:              # once: ask the server for its properties
                    asked.add(serial)
                    if len(asked) > 500:
                        asked.clear()
                    try:
                        API.RequestOPLData([serial])
                    except Exception:
                        pass
            if hit is not None and hit[0] == text:
                parsed[serial] = (text, hit[1], again)
                return hit[1]
            info = parse(text)
            if len(parsed) > 300:
                parsed.clear()
            parsed[serial] = (text, info, again)
            return info

        # ---------- the spot of an opened map (client thread) ----------
        def solve(est, end, p, size):
            """(spot, tiles per pixel) on one axis of an opened map. est: TazUO's
            estimate, made as start + p * (end - start) / 300 (the map's start is
            no longer kept once the pin has arrived); end: the map's far edge; p:
            the pin's pixel on that axis; size: the map's width (or height) in
            pixels. On a 300-pixel map (RunUO's treasure maps) the estimate is
            exact; on any other the start is solved back out of it and the spot
            taken at the middle of the pin's cell. The spot is None when it can't
            be told that way (a pin near pixel 300 of a bigger map); the scale is
            None when it isn't known well enough to lend to the other axis."""
            try:
                est = int(est)
            except Exception:
                return None, None
            try:
                end, p, size = int(end), float(p), float(size)
            except Exception:
                return est, None                     # no pin pixel or size: TazUO's estimate
            if size <= 0 or p < 0 or p > size:
                return est, None
            k = 1.0 - p / TAZ_SCALE
            start = None
            if abs(k) >= 0.001:
                base = p * end / TAZ_SCALE
                lo, hi = (est - base) / k, (est + 1 - base) / k
                start = int(math.floor((lo + hi) / 2.0))
                if not 0 < end - start <= 8192:
                    start = None
            scale = float(end - start) / size if start is not None and abs(k) >= 0.25 else None
            if abs(size - TAZ_SCALE) < 0.5:
                return est, scale                    # TazUO's own figure is exact
            if start is None or abs(1.0 - (p + 0.5) / size) / abs(k) > 2.0:
                return None, scale                   # the start is too uncertain for the spot
            return int(start + (p + 0.5) * (end - start) / size), scale

        def axis(est, end, p, size, scale=None):
            """(coordinate, approximate) of the dig spot on one axis (see solve).
            scale: the other axis's tiles per pixel, used when this one can't be
            solved (a map is drawn at the same scale both ways); with neither,
            TazUO's own estimate, marked approximate."""
            spot = solve(est, end, p, size)[0]
            if spot is None and scale:
                try:
                    return int(int(end) - (float(size) - float(p) - 0.5) * scale), False
                except Exception:
                    pass
            if spot is None:
                try:
                    return int(est), True
                except Exception:
                    return None, True
            return spot, False

        def num(obj, name):
            """An int member of a client object (public or not), or None."""
            v = Typing._get(obj, name)
            if v is None:
                return None
            try:
                return int(v)
            except Exception:
                return None

        def look_gumps():
            """Read every open map window whose pin has arrived (once per opening).
            None when the client's windows can't be read; else how many were read."""
            Typing._find()
            uim = Typing.uim
            if uim is None:
                return None
            gumps = Typing._get(None, "Gumps", uim)
            if gumps is None:
                return None
            n = 0
            try:
                for g in gumps:
                    try:
                        if str(g.GetType().Name) != "MapGump":
                            continue
                    except Exception:
                        continue
                    r = read_gump(g)
                    if r is None:
                        return None                  # a map window this build lays out otherwise
                    n += r
            except Exception:
                return None
            return n

        def read_gump(g):
            """1 if map window g was read now, 0 if not (read before, no pin yet,
            not a map of yours), None if its fields can't be read."""
            serial = num(g, "LocalSerial")
            if not serial:
                return 0
            if Typing._get(g, "IsDisposed", default=False):
                return 0
            if read_gumps.get(serial) is g:
                return 0                             # this opening was read already
            found = Typing._get(g, "foundMapLoc")
            if found is None:
                return None
            if not found:
                return 0                             # the pin hasn't arrived yet
            est_x, est_y = num(g, "mapX"), num(g, "mapY")
            if est_x is None or est_y is None:
                return None
            end_x, end_y, mf = num(g, "mapEndX"), num(g, "mapEndY"), num(g, "mapFacet")
            hit = Typing._get(g, "_hit")
            size_w = num(hit, "Width") if hit is not None else None
            size_h = num(hit, "Height") if hit is not None else None
            px = py = None
            pins = Typing._get(g, "_container")
            try:
                if pins is not None and int(pins.Count) > 0:
                    pin = pins[0]
                    pw, ph = num(pin, "Width"), num(pin, "Height")
                    x0, y0 = num(pin, "X"), num(pin, "Y")
                    if None not in (pw, ph, x0, y0):
                        px, py = x0 - pw - 5, y0 - ph      # AddPin placed it at (x + w + 5, y + h)
            except Exception:
                px = py = None
            if len(read_gumps) > 50:
                read_gumps.clear()
            read_gumps[serial] = g
            sx = solve(est_x, end_x, px, size_w)[1]
            sy = solve(est_y, end_y, py, size_h)[1]
            x, ax = axis(est_x, end_x, px, size_w, sy)
            y, ay = axis(est_y, end_y, py, size_h, sx)
            if settings["say"]:
                say("map window %X: pin %s,%s on %sx%s, far edge %s,%s, TazUO's estimate %d,%d, "
                    "facet field %s -> %s,%s" % (serial, px, py, size_w, size_h, end_x, end_y,
                                                est_x, est_y, mf, x, y))
            if x is None or y is None or x <= 0 or y <= 0:
                return 0
            record(serial, x, y, mf if mf is not None and mf > 0 else -1, ax or ay)
            return 1                                 # (read, treasure map or not: not read again)

        def record(serial, x, y, mf, approx=False):
            """A map's dig spot, read now. The facet: the map window's own when it
            has one (> 0), else the map's properties, else the one you are on.
            Only a treasure map's: its name says so, it was read before, or the
            shard has just said it showed one (a plain map with a plotted course
            has pins too)."""
            info = {}
            try:
                it = API.FindItem(serial)
                if it is not None:
                    info = info_of(serial, it)
            except Exception:
                info = {}
            now = time.time()
            hinted = 0 <= now - st["tm_at"] <= LOOK_FOR and (
                st["tm_serial"] == serial or (not st["tm_serial"] and now - st["tm_at"] <= TM_HINT))
            if not (info.get("tm") or serial in spots or hinted):
                if settings["say"]:
                    say("map %X has a pin but isn't a treasure map: left out." % serial)
                return False
            f = mf if mf >= 0 else info.get("f", -1)
            if f < 0:
                try:
                    f = int(API.GetMap())
                except Exception:
                    f = st["me"][2] if st["me"][2] >= 0 else 0
            old = spots.get(serial)
            lvl = info.get("lvl", -1)
            if lvl < 0 and old is not None:
                lvl = old["lvl"]
            rec = {"x": int(x), "y": int(y), "f": int(f), "lvl": lvl,
                   "done": bool(info.get("done") or (old is not None and old["done"])),
                   "t": int(time.time()), "approx": bool(approx)}
            same = old is not None and (old["x"], old["y"], old["f"]) == (rec["x"], rec["y"], rec["f"])
            spots[serial] = rec
            cap_spots()
            st["dirty"] = True
            st["next_scan"] = 0.0                    # list it now
            if not same:
                st["arrow_off"] = False              # a new spot: the arrow may come back
                mx, my, mf2 = st["me"]
                where = ""
                if mf2 == rec["f"] and mx > 0:
                    d = max(abs(rec["x"] - mx), abs(rec["y"] - my))
                    where = ", %d tile%s %s" % (d, "" if d == 1 else "s",
                                                direction(rec["x"] - mx, rec["y"] - my))
                say("%s map%s: dig at %s%d, %d in %s%s." % (
                    level_name(lvl).lower(), (" (level %d)" % lvl) if lvl >= 0 else "",
                    "about " if rec["approx"] else "", rec["x"], rec["y"],
                    facet_name(rec["f"]), where), Kit.HUE_GOOD)
            return True

        def arm_look(now):
            st["look_until"] = now + LOOK_FOR
            st["next_look"] = 0.0

        # ---------- events and the journal (client tick) ----------
        def on_used(*args):
            """API.Events.ObjectUsed (a double-click the client sends): only noted."""
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
            if st["hooked"]:
                return
            st["hooked"] = True                      # once per run: the handler checks "active"
            try:
                API.Events.ObjectUsed(on_used)
            except Exception:
                pass

        def handle_used(now):
            used, st["used"] = st["used"], []
            for s in used:
                try:
                    it = API.FindItem(s)
                    g = int(it.Graphic) if it is not None else 0
                except Exception:
                    g = 0
                if g in MAP_GRAPHICS:
                    st["last_map"] = (s, now)
                    arm_look(now)

        def handle_journal(now):
            rd = JR["rd"]
            if rd is None:
                return
            own = TITLE.lower() + ":"
            for ln in rd.new():
                low = ln.low
                # (2.6.82) the three texts first: most lines are none of them
                if "somewhere near" in low:
                    kind = 1
                elif J_SHOWN in low or J_DECODED in low:
                    kind = 2
                elif J_DONE in low:
                    kind = 3
                else:
                    continue
                if low.startswith(own):
                    continue
                name = (ln.name or "").strip().lower()
                if name and name != "system":
                    continue                         # a player saying it, not the shard / client
                if kind == 1:
                    m = J_ESTIMATE.search(low)
                    if m:
                        st["est"] = (int(m.group(1)), int(m.group(2)), now)
                        arm_look(now)
                        if settings["say"]:
                            say("TazUO's estimate line: %s, %s" % (m.group(1), m.group(2)))
                elif kind == 2:
                    # the map window coming is a treasure map's: the one just
                    # double-clicked when known, else only one opening right now
                    s, t = st["last_map"]
                    st["tm_at"] = now
                    st["tm_serial"] = s if s and 0 <= now - t <= USED_KEEP else 0
                    TEXT_ALL[0] = True               # (a decoded map's name changes)
                    arm_look(now)
                else:
                    s, t = st["last_map"]
                    TEXT_ALL[0] = True               # (its properties say "completed" now)
                    if s and 0 <= now - t <= USED_KEEP and s in spots and not spots[s]["done"]:
                        spots[s]["done"] = True
                        st["dirty"] = True
                        st["next_scan"] = 0.0

        def look_step(now):
            if not (now < st["look_until"] <= now + LOOK_FOR + 1.0):
                if st["look_until"] > now + LOOK_FOR + 1.0:   # the clock was set back
                    st["look_until"] = now + LOOK_FOR
                    return
                if st["est"] is not None:
                    fallback(now)                    # the look is over: the journal line, if any
                if read_gumps:
                    read_gumps.clear()               # hold no closed map window
                return
            if now < st["next_look"] <= now + LOOK_EVERY:
                return
            st["next_look"] = now + LOOK_EVERY
            n = look_gumps()
            if n is None:
                # the client's map windows can't be read: TazUO's journal line, as soon
                # as the map that was double-clicked is known (else when the look ends)
                est, used = st["est"], st["last_map"]
                if est is not None and used[0] and -2.0 <= est[2] - used[1] <= USED_KEEP:
                    fallback(now)
            elif n > 0:
                st["est"] = None                     # that line was this map window's own
                st["look_until"] = min(st["look_until"], now + 1.0)

        def fallback(now):
            """No map window could be read: TazUO's estimate line and the map you
            just double-clicked (an estimate that takes a 300-pixel map for granted,
            as RunUO's treasure maps are)."""
            x, y, te = st["est"]
            st["est"] = None
            s, tu = st["last_map"]
            if not s or not (-2.0 <= te - tu <= USED_KEEP) or x <= 0 or y <= 0:
                return
            st["last_map"] = (0, 0.0)                # one line per double-click
            record(s, x, y, -1)                      # (exact for RunUO's 300-pixel maps)

        # ---------- the maps in your pack (client tick) ----------
        def scan(now):
            try:
                me = API.Player
                mx, my = int(me.X), int(me.Y)
                fac = int(API.GetMap())
            except Exception:
                return
            st["me"] = (mx, my, fac)
            # 2.6.85: API.Backpack is the serial itself (reading .Serial off it raised, so
            # no scan ever got past here and the window stayed empty)
            try:
                bps = int(API.Backpack or 0)
            except Exception:
                bps = 0
            if not bps:
                st["in_pack"] = None                 # (Forget waits until the pack is known)
                return                               # no backpack known now: the list stays as it was
            # 2.6.85: every depth of the backpack (the pass's shared list), and the bank box
            # while it is open (read at most every BANK_EVERY, at most BANK_CAP items)
            found = []
            try:
                fn = getattr(HOST, "pack_items", None)
                deep = fn(True, 0.5) if fn is not None else API.ItemsInContainer(bps, True)
            except Exception:
                deep = []
            for it in deep or ():
                try:
                    if int(it.Graphic) in MAP_GRAPHICS:
                        found.append(it)
                except Exception:
                    continue
            bank = bank_maps(now)
            banked = set()
            for it in bank:
                try:
                    banked.add(int(it.Serial))
                except Exception:
                    continue
            found.extend(bank)
            out, seen = [], set()
            hidden = 0
            day = int(time.time())
            tnow = None if TEXT_ALL[0] else time.time()   # None: every map's text read now
            TEXT_ALL[0] = False
            for it in found:
                try:
                    s = int(it.Serial)
                except Exception:
                    continue
                if s in seen:
                    continue
                seen.add(s)                          # every map in the pack, listed or not
                if len(out) >= MAX_PACK_MAPS:
                    continue                         # (listed at most MAX_PACK_MAPS)
                info = info_of(s, it, tnow)
                rec = spots.get(s)
                if not info["tm"] and rec is None:
                    continue                         # a plain map, not a treasure map
                lvl = info["lvl"] if info["lvl"] >= 0 else (rec["lvl"] if rec else -1)
                done = bool(info["done"] or (rec is not None and rec["done"]))
                if rec is not None:
                    if info["f"] >= 0 and rec["f"] != info["f"]:
                        rec["f"] = info["f"]         # the map's own word on its facet
                        st["dirty"] = True
                    if lvl != rec["lvl"] or done != rec["done"]:
                        rec["lvl"], rec["done"] = lvl, done
                        st["dirty"] = True
                    if day - rec["t"] > 86400:       # seen in your pack: kept from aging out
                        rec["t"] = day
                        st["dirty"] = True
                dec = True if rec is not None else info["dec"]
                e = {"serial": s, "lvl": lvl, "dec": dec, "done": done, "x": None, "y": None,
                     "f": -1, "dist": None, "group": 3, "bank": s in banked}
                if rec is not None:
                    e["x"], e["y"], e["f"] = rec["x"], rec["y"], rec["f"]
                    e["approx"] = rec.get("approx", False)
                    if e["f"] == fac:
                        e["dist"] = max(abs(rec["x"] - mx), abs(rec["y"] - my))
                        e["dir"] = direction(rec["x"] - mx, rec["y"] - my)
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
                if e["bank"]:                        # 2.6.85: clearly marked as in the bank
                    e["where"] = "in the bank: " + e["where"]
                out.append(e)
            out.sort(key=sort_key)
            st["list"] = out
            st["in_pack"] = seen
            if st["pin"] and st["pin"] not in seen:
                st["pin"] = 0                        # that map left your pack
            sig = tuple((e["serial"], e["lvl"], e["dec"], e["done"], e["where"]) for e in out) + (hidden,)
            st["hidden"] = hidden
            if sig != st["list_sig"]:
                st["list_sig"] = sig
                st["list_ver"] += 1

        def bank_maps(now):
            """(2.6.85) The treasure maps in the bank box, while its window is open; [] else."""
            if now - bank_st["at"] < BANK_EVERY and now >= bank_st["at"]:
                return bank_st["items"]
            bank_st["at"] = now
            bank_st["items"] = []
            try:
                b = int(API.Bank or 0)
                if not b or not bank_open(b):
                    return []
                items = API.ItemsInContainer(b, True) or []
                for it in list(items)[:BANK_CAP]:
                    if int(it.Graphic) in MAP_GRAPHICS:
                        bank_st["items"].append(it)
            except Exception:
                pass
            return bank_st["items"]

        def bank_open(bank):
            """A container window of the client's own is showing the bank box."""
            try:
                for g in Tz.windows(("ContainerGump", "GridContainer")):
                    if int(g.LocalSerial) == bank:
                        return True
            except Exception:
                pass
            return False

        def dig_tiles(keep):
            """(2.6.85) The spot of each decoded map not dug up, highlighted in the game world
            so you can walk to it and dig on the exact tile. Display only: nothing walks or
            digs (R2). Only the changes are sent; gone from `keep`, the highlight goes."""
            want = set((int(e["x"]), int(e["y"]), int(e["f"])) for e in keep)
            for t in st["dig_tiles"] - want:
                try:
                    API.RemoveMarkedTile(t[0], t[1], t[2])
                except Exception:
                    pass
            for t in want - st["dig_tiles"]:
                try:
                    API.MarkTile(t[0], t[1], DIG_HUE, t[2])
                except Exception:
                    pass
            st["dig_tiles"] = want

        def sort_key(e):
            return (e["group"], e["dist"] if e["dist"] is not None else 0, e["lvl"], e["serial"])

        def atlas_publish():
            """The dig spots of the decoded maps in your pack, not dug up yet, as
            markers on TazUO's World Map (the Atlas, 2.6.51). 2.6.82: made again
            only when the spots change, not with every step's "where" text."""
            keep = [e for e in st["list"] if not (e["x"] is None or e["done"] or e["f"] < 0)]
            sig = tuple((e["serial"], e["x"], e["y"], e["f"], e["lvl"]) for e in keep)
            if sig == st["atlas_sig"]:
                return
            st["atlas_sig"] = sig
            dig_tiles(keep)
            items = {}
            for e in keep:
                name = atlas_name(("Dig L%d #%04X" % (e["lvl"], e["serial"] & 0xFFFF)) if e["lvl"] >= 0
                                  else ("Dig #%04X" % (e["serial"] & 0xFFFF)))
                items[name] = (int(e["x"]), int(e["y"]), int(e["f"]), "yellow")
            ATLAS.set("maps", items)

        def where_of(e, fac):
            """(where text, hue, row tooltip) of a list entry."""
            if e["x"] is not None:
                spot = ("about (%d, %d)" if e.get("approx") else "(%d, %d)") % (e["x"], e["y"])
                if e["done"]:
                    return "dug up  " + spot, Kit.HUE_INFO, "This treasure has been dug up"
                if e["f"] == fac:
                    d = e["dist"]
                    if d == 0:
                        return "here  " + spot, Kit.HUE_GOOD, LOOK_TIP
                    return ("%d tile%s %s  %s" % (d, "" if d == 1 else "s", e["dir"], spot),
                            Kit.HUE_TEXT, LOOK_TIP)
                return ("in %s  %s" % (facet_name(e["f"]), spot), Kit.HUE_INFO,
                        "This map's spot is in %s; you are in %s" % (facet_name(e["f"]),
                                                                    facet_name(fac)))
            if e["done"]:
                return "dug up", Kit.HUE_INFO, "This treasure has been dug up"
            if e["dec"]:
                return ("open the map once to read its spot", Kit.HUE_INFO,
                        "Double-click the map once: its dig spot is read from it")
            if e["dec"] is None:
                return ("open the map to read it", Kit.HUE_INFO,
                        "Double-click the map: a decoded map's spot is read from it")
            return ("not decoded yet", Kit.HUE_INFO,
                    "Not decoded yet: double-click the map to decode it (Cartography)")

        def entry(serial):
            for e in st["list"]:
                if e["serial"] == serial:
                    return e
            return None

        # ---------- the tracking arrow ----------
        def arrow_target():
            if st["arrow_off"]:
                return None
            fac = st["me"][2]
            if st["pin"]:
                e = entry(st["pin"])
                if e is not None and e["x"] is not None and e["f"] == fac and not e["done"]:
                    return (e["x"], e["y"], e["serial"])
            if settings["auto"]:
                for e in st["list"]:                 # nearest first
                    if e["group"] == 0:
                        return (e["x"], e["y"], e["serial"])
            return None

        def update_arrow(force_off=False, force=False):
            """force (a press: Nearest, a row click): the arrow is shown again even
            when it should already be up, in case the player closed it (2.6.81)."""
            want = None if force_off else arrow_target()
            cur = st["arrow"]
            if not force and (want[:2] if want else None) == (cur[:2] if cur else None):
                st["arrow"] = want
                return
            try:
                if want is None:
                    API.TrackingArrow(-1, -1, ARROW_ID)
                else:
                    API.TrackingArrow(want[0], want[1], ARROW_ID)
                    st["arrow_at"] = time.time()
            except Exception:
                pass
            st["arrow"] = want

        def arrow_closed(now):
            """The player closed our arrow with a right-click (TazUO lets them):
            taken as Arrow off, so the row's "> " goes and a press shows it again;
            never shown again by itself (2.6.81; the 1 s scan only)."""
            if st["arrow"] is None:
                return
            age = now - st.get("arrow_at", 0.0)
            if age < 0:                              # the clock went back
                st["arrow_at"] = now
                return
            if age < ARROW_LOOK or arrow_open(ARROW_ID):
                return
            st["arrow"], st["arrow_off"], st["pin"] = None, True, 0

        # ---------- window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)

        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])

        def full_h():
            M = Kit.MARGIN
            return M + 30 + Kit.GAP + 36 + Kit.GAP + 30 + ROWS * ROW_H + 8 + M

        def build_window():
            if st["minimized"]:
                w, h = MINI_W, MINI_H
            else:
                w, h = W, full_h()
            x, y = Kit.load_pos(POS_KEY, (240, 180), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            M = Kit.MARGIN
            store = ({}, {})
            c, rows = {}, []
            g = G.CreateGump(True, True)
            if st["minimized"]:
                c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
            else:
                IW = w - 2 * M
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                # toolbar: what's in your pack, Nearest, Arrow off, the pager
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
                # the list: column heads, then the pooled rows
                yl = yt + 36 + Kit.GAP
                Kit.add_section(g, M, yl, IW, 30 + ROWS * ROW_H + 8)
                x_lvl = M + 12
                x_name = x_lvl + max(34, Kit.text_w("Level")) + 8
                x_where = x_name + 150 + 8
                x_ping = M + IW - 12 - 22
                Kit.add_label(g, "Level", x_lvl, yl + 6, Kit.HUE_TITLE)
                Kit.add_label(g, "Map", x_name, yl + 6, Kit.HUE_TITLE)
                Kit.add_label(g, "Dig spot", x_where, yl + 6, Kit.HUE_TITLE)
                c["where_w"] = x_ping - 8 - x_where
                c["empty_w"] = x_ping - 8 - x_lvl           # the empty-list line, on the first row
                for k in range(ROWS):
                    ry = yl + 30 + k * ROW_H
                    r = {"serial": 0, "prev": (0, 0.0), "sig": None, "tip": None, "pvis": True}
                    r["lvl"] = Kit.add_label(g, "", x_lvl, ry + 3, Kit.HUE_TITLE)
                    r["name"] = Kit.add_label(g, "", x_name, ry + 3, Kit.HUE_TEXT)
                    r["where"] = Kit.add_label(g, "", x_where, ry + 3, Kit.HUE_INFO)
                    r["catch"] = Kit.catcher(g, M + 6, ry, x_ping - 4 - (M + 6), ROW_H,
                                             row_click(k), LOOK_TIP)
                    r["ping"] = Kit.art_button(g, store, "ping%d" % k, Kit.ART_PLAY, x_ping, ry + 1,
                                               None, PING_TIP, on_click=ping_click(k))
                    rows.append(r)
            Kit.place(g, x, y, w, h)
            win.update({"g": g, "c": c, "store": store, "rows": rows})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))
            if st["minimized"] and st["docked"]:     # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            st["drawn"] = None
            refresh()
            Kit.dispose(old)

        def row_serial(k):
            rows = win["rows"]
            r = rows[k] if k < len(rows) else None
            if r is None:
                return 0
            s = r["serial"]
            prev, at = r["prev"]
            if prev and 0 <= time.time() - at < 0.15:   # the row just changed: what was seen
                s = prev
            return s

        def row_click(k):
            def handler(*args):
                s = row_serial(k)
                if s:
                    queue(("row", s))()
            return handler

        def ping_click(k):
            def handler(*args):
                s = row_serial(k)
                if s:
                    queue(("ping", s))()
            return handler

        def show(ctl, r, key, on):
            if r[key] != on:
                r[key] = on
                try:
                    ctl.IsVisible = on
                except Exception:
                    pass

        def refresh():
            """Draw what changed (client thread). Folded: nothing; minimized: the
            status line only; open: the rows of this page."""
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return
            arrow = st["arrow"][2] if st["arrow"] else 0
            sig = (st["list_ver"], st["page"], arrow, st["pin"], st["minimized"])
            if sig == st["drawn"]:
                return                               # nothing changed since the last draw
            st["drawn"] = sig
            c = win["c"]
            lst = st["list"]
            near = None
            for e in lst:
                if e["group"] == 0:
                    near = e
                    break
            n = len(lst)
            maps = "%d map%s" % (n, "" if n == 1 else "s")
            if near is not None:                     # 2.6.81: "here", "1 tile"
                d = near["dist"]
                part = "here" if d == 0 else "%d tile%s %s" % (d, "" if d == 1 else "s", near["dir"])
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
                    if r["serial"]:
                        r["prev"] = (r["serial"], now)
                        r["serial"] = 0
                    if k == 0 and n == 0:             # an empty list says so on its first row
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
                if r["serial"] != e["serial"]:
                    r["prev"] = (r["serial"], now)
                    r["serial"] = e["serial"]
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
                    if tip == LOOK_TIP:                  # the second click's meaning (2.6.81)
                        pinned = st["pin"] == e["serial"]
                        if settings["auto"]:
                            tip = LOOK_TIP_ON if pinned else LOOK_TIP
                        else:
                            tip = LOOK_TIP_MAN_ON if pinned else LOOK_TIP_MAN
                    if tip != r["tip"]:
                        r["tip"] = tip
                        try:
                            r["catch"].SetTooltip(tip)
                        except Exception:
                            pass
                show(r["ping"], r, "pvis", e["x"] is not None and not e["done"])

        # ---------- the queue (client tick) ----------
        def do_row(serial):
            e = entry(serial)
            if e is None:
                return
            if e["x"] is None or e["done"]:
                say(journal_case(e["tip"]) + ".")
                return
            if e["f"] != st["me"][2]:
                say("that map's spot is in %s; you are in %s." % (facet_name(e["f"]),
                                                                 facet_name(st["me"][2])))
                return
            st["arrow_off"] = False
            if st["pin"] == serial:
                st["pin"] = 0                        # again: back to the nearest map...
                if settings["auto"]:
                    say("tracking arrow back on the nearest map.")
                else:                                # ...or, with that unticked, down (2.6.81)
                    st["arrow_off"] = True
                    say("tracking arrow down.")
            else:
                st["pin"] = serial
                say("tracking arrow on the %s map's spot (%d, %d)." % (
                    level_name(e["lvl"]).lower(), e["x"], e["y"]))
            update_arrow(force=True)                 # shown again even if the player closed it

        def do_ping(serial, now):
            e = entry(serial)
            if e is None or e["x"] is None:
                return
            if HOST.services.get("pings.send") is None:
                say("World Map > Map Pings is off; turn it on to send map pings.")
                return
            st["ping"] = [e["x"], e["y"], e["f"], now + PING_TRY_FOR, 0.0]

        def ping_step(now):
            p = st["ping"]
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
                ok = True                            # it failed outright: not retried
            if ok:
                st["ping"] = None
            elif not (now < p[3] <= now + PING_TRY_FOR):
                st["ping"] = None
                say("Map Pings didn't take the ping (too soon after the last one); try again.")
            else:
                p[4] = now + PING_RETRY

        def forget_others():
            here = st["in_pack"]                     # every map in the pack, hidden ones too
            if here is None:
                say("your backpack isn't known yet; nothing was forgotten.")
                return
            gone = [s for s in spots if s not in here]
            for s in gone:
                del spots[s]
            st["dirty"] = True
            say("forgot %d spot%s of maps not in your pack." % (len(gone),
                                                                 "" if len(gone) == 1 else "s"))

        # ---------- settings page ----------
        PAGE_CHECKS = (("auto", "Point the tracking arrow at the nearest map's spot",
                        "With no map picked, the tracking arrow points at the nearest dig spot "
                        "on your facet"),
                       ("undecoded", "List maps not decoded yet",
                        "Shows the maps still to be decoded (Cartography) in the window's list"),
                       ("done", "List maps already dug up",
                        "Shows the maps whose treasure has been dug up in the window's list"))
        DEBUG_CHECK = ("say", "Print what is read from each map in the journal",
                       "Prints the map window's pin, size and bounds and TazUO's estimate line, "
                       "for checking the spots against the shard")
        H_WINDOW = 30 + 26 * len(PAGE_CHECKS) + 10
        H_SPOTS, H_DEBUG = 64, 66

        def config_height(w):
            return H_WINDOW + Kit.GAP + H_SPOTS + Kit.GAP + ATLAS_H + Kit.GAP + H_DEBUG

        def build_config(g, x, y, w):
            Kit.add_section(g, x, y, w, H_WINDOW, "WINDOW  (open a decoded map once to read its spot)")
            c = {}
            for i, (k, text, tip) in enumerate(PAGE_CHECKS):
                c[k] = Kit.add_check(g, text, x + 12, y + 30 + i * 26, settings[k], tip)
            y2 = y + H_WINDOW + Kit.GAP
            Kit.add_section(g, x, y2, w, H_SPOTS, "SAVED SPOTS")
            store = ({}, {})
            c["count"] = Kit.add_label(g, "%d spot%s remembered" % (len(spots),
                                       "" if len(spots) == 1 else "s"), x + 12, y2 + 34, Kit.HUE_INFO)
            bx = x + w - 12 - (35 + Kit.text_w("Forget lost maps"))
            Kit.art_button(g, store, "forget", Kit.ART_CLOSE, bx, y2 + 30, "Forget lost maps",
                           "Forget the dig spots of every map that isn't in your backpack now",
                           on_click=queue("forget"))
            y3 = y2 + H_SPOTS + Kit.GAP
            atlas_section(g, x, y3, w, "maps")
            y4 = y3 + ATLAS_H + Kit.GAP
            Kit.add_section(g, x, y4, w, H_DEBUG, "DEBUG  (for checking the shard's texts)")
            k, text, tip = DEBUG_CHECK
            c[k] = Kit.add_check(g, text, x + 12, y4 + 30, settings[k], tip)
            page.update({"c": c, "store": store})

        def poll_config():
            c = page["c"]
            if c is None:
                return
            changed = False
            for k, _, _ in PAGE_CHECKS + (DEBUG_CHECK,):
                ctl = c.get(k)
                if ctl is None:
                    continue
                try:
                    v = bool(ctl.IsChecked)
                except Exception:
                    continue
                if v != settings[k]:
                    settings[k] = v
                    changed = True
            if changed:
                save_settings()
                st["next_scan"] = 0.0
                st["drawn"] = None

        def config_closed():
            page["c"] = None

        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "active": True, "docked": False, "queue": [], "used": [],
                       "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False)),
                       "list": [], "list_sig": None, "next_scan": 0.0, "arrow": None, "pin": 0,
                       "arrow_at": 0.0,
                       "arrow_off": False, "ping": None, "est": None, "look_until": 0.0,
                       "last_map": (0, 0.0), "drawn": None, "page": 0, "atlas_ver": None,
                       "atlas_sig": None, "dig_tiles": set()})
            load_settings()
            load_maps()
            read_gumps.clear()
            JR["rd"] = Journal.reader()
            hook_events()
            scan(time.time())
            build_window()
            HOST.dock_add(KEY, _dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"), scale=True))
            update_arrow()

        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])                # on_disposed turns the module off
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
                if kind == "settings":
                    HOST.show_settings(KEY)
                elif kind == "toggle_min":
                    st["minimized"] = not st["minimized"]
                    st["docked"] = False
                    HOST.dock_forget(KEY)
                    Kit.save_min(MIN_KEY, st["minimized"])
                    build_window()
                elif kind == "to_bar":
                    HOST.dock_to_bar(KEY, TITLE)
                elif kind == "redraw":
                    build_window()
                elif kind == "page":
                    st["page"] = max(0, st["page"] + a[1])
                elif kind == "row":
                    do_row(a[1])
                elif kind == "ping":
                    do_ping(a[1], now)
                elif kind == "nearest":
                    st["arrow_off"] = False
                    if settings["auto"]:
                        st["pin"] = 0                # follows the nearest map as you walk
                    else:                            # 2.6.81: pinned, since nothing follows it
                        near = None
                        for e in st["list"]:         # nearest first
                            if e["group"] == 0:
                                near = e
                                break
                        st["pin"] = near["serial"] if near is not None else 0
                    update_arrow(force=True)         # shown again even if the player closed it
                    if st["arrow"] is None:
                        say("no decoded map with a spot on this facet.")
                elif kind == "arrow_off":
                    st["pin"], st["arrow_off"] = 0, True
                    update_arrow()
                elif kind == "forget":
                    forget_others()
                    safe(lambda: HOST.refresh_settings(KEY))
                if win["g"] is None:
                    return
            if not (now < st["next_scan"] <= now + SCAN_EVERY):
                st["next_scan"] = now + SCAN_EVERY
                scan(now)
                arrow_closed(now)
                update_arrow()
                if st["list_ver"] != st["atlas_ver"]:        # on TazUO's World Map (2.6.51)
                    st["atlas_ver"] = st["list_ver"]
                    atlas_publish()
            if st["ping"] is not None:
                ping_step(now)
            if st["dirty"] and not (now < st["next_save"] <= now + SAVE_EVERY):
                st["next_save"] = now + SAVE_EVERY
                save_maps()
            refresh()

        def _stop():
            st["shutting"] = True
            st["active"] = False
            HOST.dock_remove(KEY)
            if st["arrow"] is not None:
                update_arrow(force_off=True)         # only our own arrow comes down
            save_pos()
            Kit.save_min(MIN_KEY, st["minimized"] and not st["docked"])
            save_settings()
            if st["dirty"]:
                save_maps()
            JR["rd"] = None
            dig_tiles(())                            # (2.6.85) the highlights go with the part
            st["used"], st["queue"], st["ping"] = [], [], None
            g, win["g"] = win["g"], None
            win["rows"] = []
            Kit.dispose(g)

        def _interval():
            """(2.6.82) 0.1 s while an opened map window is looked for (its looks
            are LOOK_EVERY apart), else 0.2 s: the work is a 1 s scan."""
            return 0.1 if st["look_until"] > time.time() else 0.2

        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,          # tick on the client thread: no waits in it
                  "interval": _interval,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    def _part_dry():
        """Builds the module in its own namespace and returns its hooks."""
        # ---- notes carried over from the 2.6.06 module file ----
        #  Assistant, loaded by the Virtue Assistant script from
        #  this file uses (API, G, safe, Client, Kit, Follow, HOST, Journal, the main
        #  on its Modules tab.
        #
        #  For mining, lumberjacking, fishing and digging sand BY HAND. It never
        #  harvests, moves or targets anything itself: it only shows things.
        #
        #    - A weight bar: your weight against your maximum, yellow from WEIGHT_WARN,
        #      red from WEIGHT_RED, with one alert as you cross the red line ("Weight
        #      near the limit (harvesting)" on Settings > Alerts; while Inventory >
        #      Paperdoll is on, its own weight alert says it and this one stays quiet).
        #    - Dry spots: when the shard says a spot has run out ("There is no metal
        #      here to mine.", "There's not enough wood here to harvest.", "The fish
        #      don't seem to be biting here.", "There is no sand here to mine."), the
        #      spot you aimed at goes on a list, nearest first, with a countdown until
        #      it can be back, how far and which way it is. The shard keeps its
        #      resources in blocks of tiles (RunUO's harvest banks: BANK below), so a
        #      dry spot is that whole block: the "Here:" line says when you stand in a
        #      dry one. A spot leaves the list when its time is up, or at once when a
        #      harvest there works again (or fails a skill check, which also means
        #      there is something left).
        #      Click a row: the tracking arrow points at that spot (click again: off).
        #      Ping: a Look here map ping on the spot (needs Map Pings), so a friend
        #      knows it's dry.
        #    The spot is the tile of your last target (the client's last-target
        #    place, API.LastTargetPos) when it is within reach of you, else the tile
        #    in front of you ("about" in the list).
        #
        #  Only the shard's own lines count (a player saying the words doesn't).
        #  "Print each harvest line read in the journal" (DEBUG on the settings
        #  page) prints each line this part reads, with its speaker, to check the
        #  shard's wording.
        # ============================ MODULE START ===================================
        #  MODULE: Ore Tracker (Harvest Helper before 2.6.5, "Dry spots" in 2.6.5)  -  weight
        #  bar and dry harvest spots (display only). Every saved key keeps its old name.
        # =============================================================================
        KEY = "harvest"
        TITLE = "Ore Tracker"

        # ------------------------------- CONFIG --------------------------------------
        KINDS = ("ore", "wood", "fish", "sand")
        KIND_NAME = {"ore": "Ore", "wood": "Wood", "fish": "Fish", "sand": "Sand"}
        KIND_SKILL = {"ore": "mining", "wood": "lumberjacking", "fish": "fishing",
                      "sand": "sand for glassblowing"}
        KIND_HUE = {"ore": 1153, "wood": 68, "fish": 88, "sand": 53}
        #  The shard's lines, lower case, whole line (cliloc numbers from Cliloc.enu;
        #  the texts are RunUO's: UNCHECKED IN GAME on In Mani Ylem).
        DRY_TEXTS = {                    # the spot has run out
            "there is no metal here to mine.": "ore",                 # 503040, 501866
            "there's not enough wood here to harvest.": "wood",       # 500488, 500493
            "the fish don't seem to be biting here.": "fish",         # 503168, 503172, 503173
            "there is no sand here to mine.": "sand",                 # 1044629
        }
        FAIL_TEXTS = {                   # a skill check failed: there is something left
            "you loosen some rocks but fail to find any useable ore.": "ore",      # 503043, 501869
            "you hack at the tree for a while, but fail to produce any useable wood.": "wood",
            "you fish a while, but fail to catch anything.": "fish",               # 503171
            "you dig for a while but fail to find any of sufficient quality for glassblowing.":
                "sand",                                                            # 1044630
        }
        GOT_PREFIXES = (                 # a harvest worked (the line starts with this)
            ("you dig some ", "ore"),                    # 503044, 503045, 1007072-1007080
            ("you put some logs", "wood"),               # 500498
            ("you chop some ", "wood"),                  # 1072540-1072546
            ("you pull out ", "fish"),                   # 1043297, 1008124, 1008125
            ("you carefully dig up sand", "sand"),       # 1044631
            ("your backpack can't hold the sand", "sand"),   # 1044632 (taken, then lost)
        )
        SHARD_SPEAKERS = ("", "system")  # who the shard's lines come from (a player's name doesn't count)
        #  The shard's harvest banks: each holds the resource of a block of tiles
        #  (width, height); RunUO: ore and sand 8x8, wood 4x3, fish 8x8. UNCHECKED IN GAME.
        BANK = {"ore": (8, 8), "wood": (4, 3), "fish": (8, 8), "sand": (8, 8)}
        #  Minutes a bank takes to fill again (min, max), counted by the shard from the
        #  first harvest of a full bank (RunUO's HarvestBank): ore and sand 10-20, wood
        #  20-30, fish 10-20. UNCHECKED IN GAME.
        RESPAWN = {"ore": (10, 20), "wood": (20, 30), "fish": (10, 20), "sand": (10, 20)}
        GUARDED_RESPAWN_X = 3            # resources in guarded regions respawn 3x slower (shard value,
        #                                  In Mani Ylem rules section 6; 2.6.81)
        #  Tiles from you the last target may be and still be the harvest spot (RunUO's
        #  reach is 2 for mining / wood, 4 for fishing; one more for a step). UNCHECKED.
        REACH = {"ore": 3, "wood": 3, "fish": 5, "sand": 3}
        MAX_SPOTS = 60                   # dry spots kept at most (the soonest back go first)
        FIRST_MAX = 300                  # banks whose first harvest time is remembered, at most
        ROWS = 8                         # dry spots shown (nearest first; the rest are counted)
        WEIGHT_WARN = 0.85               # the weight bar turns yellow at this share of your maximum
        WEIGHT_RED = 0.95                # ...and red here, with one alert as you cross it
        WEIGHT_REARM = 0.92              # ...armed again once you are back under this share
        WEIGHT_MAX_BASE, WEIGHT_MAX_PER_STR = 40, 3.5   # max weight when the client doesn't say it
        WEIGHT_EVERY = 0.5               # seconds between weight readings
        WEIGHT_HUE_OK, WEIGHT_HUE_WARN = 0, 0x0035      # hues on the green / yellow line art
        WEIGHT_BG_HUE = 946              # grey hue on the red line under the bar
        WEIGHT_ALERT = "harvest.weight"  # its kind on Settings > Alerts
        WEIGHT_ALERT_SOUND = 0x04A       # lever (the player picks on Settings > Alerts)
        DRAW_EVERY = 1.0                 # seconds between redraws of the distances / countdowns
        EXPIRE_EVERY = 1.0               # seconds between looks for spots whose time is up
        ARROW_ID = 0x48525654            # "HRVT": this module's own tracking arrow
        ARROW_LOOK = 1.5                 # seconds after showing it before it is looked for (2.6.81)
        PING_KIND = "look"               # Map Pings' Look here
        PING_SERVICE = "pings.send"
        PING_TRY = 6.0                   # seconds a ping waits for Map Pings' pace before giving up
        SAVE_EVERY = 5.0                 # seconds between saves of the list (off the client thread)
        CLOCK_JUMP = 2.0                 # seconds: the computer's clock going back more than this
        #                                  between two ticks moves every time kept with it
        SETTINGS_KEY = "Harvest_settings"     # per character
        SPOTS_KEY = "Harvest_spots"           # per character: the dry spots, when kept
        POS_KEY = "Harvest_pos"
        MIN_KEY = "Harvest_min"
        W = 440                          # full window width
        MINI_W, MINI_H = 340, 46         # minimized bar
        ROW_H = 24
        TRAY_ICON = 0x0E86               # a pickaxe on the Action Bar's tray button
        #  Facing (API.Player.Direction) -> the tile in front of you
        FACING = {"north": (0, -1), "northeast": (1, -1), "east": (1, 0), "southeast": (1, 1),
                  "south": (0, 1), "southwest": (-1, 1), "west": (-1, 0), "northwest": (-1, -1)}
        FACETS = ("Felucca", "Trammel", "Ilshenar", "Malas", "Tokuno", "Ter Mur")
        ROW_TIP = "Click: put the tracking arrow on it (click again to take it down)"
        ROW_TIP_ON = "Click: take the tracking arrow down"
        PING_TIP = ("Send a Look here map ping on this spot, so others know it is dry "
                    "(needs World Map > Map Pings on)")
        EMPTY_TEXT = "No dry spots yet. When the shard says a spot has run out, it goes here."
        # -----------------------------------------------------------------------------

        SECS_MAX = 60.0 * GUARDED_RESPAWN_X * max(hi for _, hi in RESPAWN.values())   # longest a
        #                                  spot can be dry (a guarded one: 2.6.81)
        settings = {"ore": True, "wood": True, "fish": True, "sand": True,
                    "alert": True, "keep": True, "say": False}
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
              "rd": None,            # our reader of the shared Journal
              "ver": 0,              # bumped whenever the list changes
              "drawn": None,         # what the rows were last drawn from
              "draw_at": 0.0,        # next redraw of the distances / countdowns
              "mini_drawn": None,    # what the minimized status last showed
              "mini_key": None, "w_key": None,   # what those were made from (2.6.82)
              "expire_at": 0.0,
              "w_at": 0.0,           # next weight reading
              "w_armed": True,       # the weight alert is raised when you next cross the red line
              "weight": None,        # (weight, max, share) last read
              "wdrawn": None,        # (text, kind, width) of the weight section as last set
              "me": None,            # (x, y, facet) last read
              "arrow": None,         # key of the spot the tracking arrow points at
              "arrow_at": 0.0,       # when it was last shown (looked for ARROW_LOOK s later, 2.6.81)
              "ping": None,          # [x, y, facet, give up at, text]: a ping waiting for its turn
              "save_due": False,
              "save_at": 0.0,
              "count": (None, 0),    # (what it was counted from, dry spots shown) for the minimized form
              "last_now": None}      # time.time() of the last tick (to see the clock set back)
        spots = {}                   # (kind, facet, bank x, bank y) -> spot dict (see note_dry)
        first = {}                   # (kind, facet, bank x, bank y) -> time of its first harvest seen
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}
        page = {"c": None}           # this module's page of the Settings tab
        jobs = []                    # work for _thread_tick (saving the list)


        # ---------- saved settings ----------
        def load_settings():
            for part in Kit.get_var(SETTINGS_KEY).split(";"):
                if "=" not in part:
                    continue
                k, v = part.split("=", 1)
                k = k.strip()
                if k in settings:                    # unknown keys (a newer version's) are skipped
                    settings[k] = v.strip() == "1"

        def save_settings():
            Kit.put_var(SETTINGS_KEY, ";".join("%s=%d" % (k, 1 if settings[k] else 0)
                                               for k in ("ore", "wood", "fish", "sand", "alert",
                                                         "keep", "say")))

        def spots_text():
            out = []
            for e in spots.values():
                out.append("%s,%d,%d,%d,%d,%d,%d" % (e["kind"], e["m"], e["x"], e["y"], int(e["lo"]),
                                                     int(e["hi"]), 1 if e["about"] else 0))
            return ";".join(out)

        def load_spots():
            """The list kept from the last session (spots whose time is up, or that
            a clock set far back would keep for ever, are dropped)."""
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

        def want_save():
            if settings["keep"]:
                st["save_due"] = True

        def save_spots_job():
            """Script thread (_thread_tick): the list to its saved var."""
            st["save_due"] = False
            st["save_at"] = time.time() + SAVE_EVERY
            Kit.put_var(SPOTS_KEY, spots_text() if settings["keep"] else "")


        # ---------- the list ----------
        def bank_of(kind, m, x, y):
            bw, bh = BANK[kind]
            return (kind, m, x // bw, y // bh)

        def add_spot(kind, m, x, y, lo, hi, about, now):
            key = bank_of(kind, m, x, y)
            old = spots.get(key)
            spots[key] = {"kind": kind, "m": m, "x": x, "y": y, "lo": lo, "hi": hi, "at": now,
                          "about": about, "key": key}
            if st["arrow"] == key and old is not None and (old["x"], old["y"]) != (x, y):
                try:                                 # the block ran dry again at another tile:
                    API.TrackingArrow(x, y, ARROW_ID)    # the arrow follows the new spot
                    st["arrow_at"] = now
                except Exception:
                    pass
            if len(spots) > MAX_SPOTS:               # a cap: the one back soonest goes
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
            """GUARDED_RESPAWN_X inside a guard zone, else 1 (your place, not the
            spot's; HOST.guarded() is a cached lookup, no wait)."""
            return GUARDED_RESPAWN_X if safe(lambda: HOST.guarded(), None) is True else 1

        def note_dry(kind, x, y, m, about, now):
            """The shard said the spot (x, y) ran out. When the bank's first harvest
            was seen this session, it is back between first + min and first + max;
            otherwise at any time up to max from now."""
            key = bank_of(kind, m, x, y)
            lo_m, hi_m = RESPAWN[kind]
            x3 = respawn_x()                         # 2.6.81: 3x as long in a guard zone
            lo_m, hi_m = lo_m * x3, hi_m * x3
            f = first.pop(key, None)
            if f is not None and 0 <= now - f < hi_m * 60.0:
                lo, hi = f + lo_m * 60.0, f + hi_m * 60.0
            else:
                lo, hi = now, now + hi_m * 60.0
            add_spot(kind, m, x, y, lo, hi, about, now)
            st["ver"] += 1
            want_save()

        def note_back(kind, x, y, m, got, now):
            """A harvest there worked (got) or failed a skill check: the bank isn't
            empty. Off the list; a success starts the bank's clock (its first harvest)."""
            key = bank_of(kind, m, x, y)
            if spots.pop(key, None) is not None:
                if st["arrow"] == key:
                    arrow_off()
                st["ver"] += 1
                want_save()
            if got:
                f = first.get(key)
                if f is None or not 0 <= now - f < RESPAWN[kind][1] * 60.0 * respawn_x():
                    if len(first) >= FIRST_MAX:
                        for k in [k for k, t in first.items() if not 0 <= now - t < SECS_MAX]:
                            del first[k]
                        if len(first) >= FIRST_MAX:
                            first.clear()
                    first[key] = now

        def expire(now):
            gone = [k for k, e in spots.items() if e["hi"] <= now or e["at"] - now > 60.0]
            for k in gone:                           # (made in the future: the clock was set back)
                del spots[k]
                if st["arrow"] == k:
                    arrow_off()
            if gone:
                st["ver"] += 1
                want_save()
            a = st["arrow"]
            if a is not None and ARROW_LOOK <= now - st["arrow_at"] and not arrow_open(ARROW_ID):
                st["arrow"] = None                   # 2.6.81: closed with a right-click: its
                st["ver"] += 1                       # row's "> " goes (nothing to take down)
                a = None
            if a is not None:                        # you changed facet: the arrow would point
                me = read_me()                       # at that x, y here
                if me is not None and me[2] != a[1]:
                    arrow_off()

        def rebase(d):
            """The clock went back (d < 0 seconds since the last tick): every time
            kept moves with it, so the list isn't thrown away as "made in the
            future" and each countdown keeps the real time left."""
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
                st["ver"] += 1
                want_save()

        def clear_spots():
            if st["arrow"] is not None:
                arrow_off()
            spots.clear()
            st["ver"] += 1
            want_save()


        # ---------- reading the game (client thread: every call runs in place) ----------
        def read_me():
            try:
                p = API.Player
                if p is None:
                    return None
                me = (int(p.X), int(p.Y), int(API.GetMap()))
            except Exception:
                return None
            if me[0] <= 0 and me[1] <= 0:            # not in the world yet
                return None
            st["me"] = me
            return me

        def target_tile(kind, me):
            """(x, y, about): the last target's tile when it is within reach (the
            harvest spot), else the tile in front of you (about = True)."""
            px, py = me[0], me[1]
            try:
                p = API.LastTargetPos
                x, y = int(p.X), int(p.Y)
            except Exception:
                x = y = -1
            if 0 < x < 0xFFFF and 0 < y < 0xFFFF and max(abs(x - px), abs(y - py)) <= REACH[kind]:
                return x, y, False
            try:
                d = str(API.Player.Direction or "").strip().lower()
            except Exception:
                d = ""
            dx, dy = FACING.get(d, (0, 0))
            return px + dx, py + dy, True

        def line_kind(low):
            """("dry" / "fail" / "got", kind) for a harvest line, else None."""
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
            rd = st["rd"]
            if rd is None:
                return
            for ln in rd.new():
                low = ln.low.strip()
                hit = line_kind(low)
                if hit is None:
                    continue
                what, kind = hit
                spk = (ln.name or "").strip()
                if spk.lower() not in SHARD_SPEAKERS:
                    if settings["say"]:
                        API.SysMsg("%s: not the shard's line: %s said \"%s\"." % (TITLE, spk, ln.text),
                                   Kit.HUE_INFO)
                    continue                         # a player saying it doesn't count
                if what == "dry" and not settings[kind]:
                    continue                         # (a line saying it is back still counts)
                me = read_me()
                if me is None:
                    continue
                x, y, about = target_tile(kind, me)
                if settings["say"]:
                    API.SysMsg("%s: %s line from \"%s\" (\"%s\"): %s spot %d, %d%s." % (
                        TITLE, what, spk or "no speaker", ln.text, KIND_NAME[kind].lower(), x, y,
                        " (about: the tile in front of you)" if about else ""), Kit.HUE_INFO)
                if what == "dry":
                    note_dry(kind, x, y, me[2], about, now)
                else:
                    note_back(kind, x, y, me[2], what == "got", now)

        def character_alerts():
            """Inventory > Paperdoll (module key "character") raises the same
            weight alert while it runs."""
            try:
                s = HOST.by_key.get("character")
                return s is not None and bool(s.running)
            except Exception:
                return False

        def read_weight(now):
            if now < st["w_at"] and st["w_at"] - now <= WEIGHT_EVERY:   # (further: clock set back)
                return
            st["w_at"] = now + WEIGHT_EVERY
            if not settings["alert"] and (win["g"] is None or (st["minimized"] and st["docked"])):
                return                               # folded and no alert: nothing needs it
            try:
                p = API.Player
                wt, wmax = int(p.Weight), int(p.WeightMax)
                # (2.6.82) Strength read only when it is needed
                strength = int(p.Strength) if wmax <= 0 else 0
            except Exception:
                return
            if wmax <= 0 and strength > 0:           # the client doesn't know your max
                wmax = int(WEIGHT_MAX_BASE + WEIGHT_MAX_PER_STR * strength)
            frac = (float(wt) / wmax) if wmax > 0 else -1.0
            st["weight"] = (wt, wmax, frac)
            if frac >= WEIGHT_RED:
                if st["w_armed"]:
                    raised = True
                    if settings["alert"] and not character_alerts():
                        try:
                            # "not now" (the alerts' rate limit, or the kind turned off)
                            # keeps it armed, so it comes when it can
                            raised = HOST.alert(WEIGHT_ALERT, "Weight %d/%d (%d%%): nearly "
                                                "overloaded. Unload before you harvest more."
                                                % (wt, wmax, int(frac * 100)),
                                                level="warn", who="weight") is not False
                        except Exception:
                            raised = True
                    if raised:
                        st["w_armed"] = False
            elif 0 <= frac < WEIGHT_REARM:
                st["w_armed"] = True


        # ---------- the tracking arrow and the ping ----------
        def arrow_off():
            if st["arrow"] is None:
                return
            st["arrow"] = None
            st["ver"] += 1
            try:
                API.TrackingArrow(-1, -1, ARROW_ID)
            except Exception:
                pass

        def arrow_to(key):
            e = spots.get(key)
            if e is None:
                return
            if st["arrow"] == key:
                if arrow_open(ARROW_ID, True):           # (a click: looked at now)
                    arrow_off()
                    return
                # 2.6.81: the player closed it with a right-click: this click shows it again
            me = read_me() or st["me"]
            if me is not None and me[2] != e["m"]:
                API.SysMsg("%s: that spot is in %s; you are in %s." % (
                    TITLE, facet_name(e["m"]), facet_name(me[2])), Kit.HUE_INFO)
                return
            try:
                API.TrackingArrow(e["x"], e["y"], ARROW_ID)
            except Exception as ex:
                API.SysMsg("%s: couldn't show the tracking arrow (%s)." % (TITLE, ex), Kit.HUE_BAD)
                return
            st["arrow"], st["arrow_at"] = key, time.time()
            st["ver"] += 1

        def ping_spot(key):
            e = spots.get(key)
            if e is None:
                return
            if HOST.services.get(PING_SERVICE) is None:
                API.SysMsg("%s: turn World Map > Map Pings on to ping a spot." % TITLE, Kit.HUE_INFO)
                return
            st["ping"] = [e["x"], e["y"], e["m"], time.time() + PING_TRY,
                          "the dry %s spot (%d, %d)" % (KIND_NAME[e["kind"]].lower(), e["x"], e["y"])]

        def send_ping(now):
            p = st["ping"]
            if p is None:
                return
            fn = HOST.services.get(PING_SERVICE)
            if fn is None or now > p[3] or p[3] - now > PING_TRY + 1.0:   # (clock set back: give up)
                st["ping"] = None
                API.SysMsg("%s: the ping on %s wasn't sent (%s)." % (
                    TITLE, p[4], "Map Pings is off" if fn is None else "Map Pings stayed busy"),
                    Kit.HUE_INFO)
                return
            try:
                ok = fn(p[0], p[1], p[2], PING_KIND)
            except Exception:
                ok = None                            # failed outright: not tried again every tick
            if ok is False:
                return                               # Map Pings' pace: next tick
            st["ping"] = None
            if ok:
                API.SysMsg("%s: Look here ping on %s." % (TITLE, p[4]), Kit.HUE_GOOD)
            else:
                API.SysMsg("%s: the ping on %s failed." % (TITLE, p[4]), Kit.HUE_BAD)


        # ---------- text helpers ----------
        def facet_name(m):
            return FACETS[m] if 0 <= m < len(FACETS) else "facet %d" % m

        def compass(dx, dy):
            """Compass direction in UO terms (+x east, +y south)."""
            if dx == 0 and dy == 0:
                return "here"
            deg = math.degrees(math.atan2(-dy, dx))
            if deg < 0:
                deg += 360
            return ("E", "NE", "N", "NW", "W", "SW", "S", "SE")[int(round(deg / 45.0)) % 8]

        def mins(secs):
            secs = max(0, int(secs))
            if secs < 60:
                return "%ds" % secs
            return "%dm" % ((secs + 59) // 60)

        def dist_of(e, me):
            """where_text's distance alone (2.6.82: for the sort, no text made)."""
            if me is None:
                return 0
            if me[2] != e["m"]:
                return 1 << 30
            if bank_of(e["kind"], me[2], me[0], me[1]) == e["key"]:
                return 0
            return max(abs(e["x"] - me[0]), abs(e["y"] - me[1]))

        def where_text(e, me):
            if me is None:
                return "(%d, %d)" % (e["x"], e["y"]), 0
            if me[2] != e["m"]:
                return "in %s" % facet_name(e["m"]), 1 << 30
            if bank_of(e["kind"], me[2], me[0], me[1]) == e["key"]:
                return "here", 0
            dx, dy = e["x"] - me[0], e["y"] - me[1]
            dist = max(abs(dx), abs(dy))
            return "%s%d tile%s %s" % ("about " if e["about"] else "", dist,
                                       "" if dist == 1 else "s", compass(dx, dy)), dist

        def back_text(e, now):
            """(text, hue): 'in 6m-14m' while it can't be back yet, 'within 14m' once it may."""
            if now < e["lo"]:
                return "back in %s-%s" % (mins(e["lo"] - now), mins(e["hi"] - now)), Kit.HUE_BAD
            return "back within %s" % mins(e["hi"] - now), Kit.HUE_TITLE

        def row_tip(e, on):
            bw, bh = BANK[e["kind"]]
            x0, y0 = (e["x"] // bw) * bw, (e["y"] // bh) * bh
            when = time.strftime("%H:%M", time.localtime(e["hi"]))
            if e["lo"] > e["at"]:
                back = "back between %s and %s" % (time.strftime("%H:%M", time.localtime(e["lo"])),
                                                   when)
            else:
                back = "back by %s at the latest" % when
            return "%s ran dry at %d, %d%s: the %dx%d block from %d, %d, %s.  %s" % (
                KIND_NAME[e["kind"]], e["x"], e["y"],
                " (about: the tile in front of you)" if e["about"] else "",
                bw, bh, x0, y0, back, ROW_TIP_ON if on else ROW_TIP)

        def shown_spots():
            return [e for e in spots.values() if settings[e["kind"]]]

        def _by_place(t):
            return (t[0], t[1])

        ATLAS_SPOTS = 15                 # spots on TazUO's World Map at most (the most recent)

        def _by_time(e):
            return -e["at"]

        def atlas_publish():
            """The spots that ran dry (the kinds ticked, the most recent first) as
            markers on TazUO's World Map (the Atlas, 2.6.51)."""
            items = {}
            for e in sorted(shown_spots(), key=_by_time)[:ATLAS_SPOTS]:
                name = atlas_name("%s dry %d %d" % (KIND_NAME[e["kind"]], e["x"], e["y"]))
                items[name] = (int(e["x"]), int(e["y"]), int(e["m"]), "blue")
            ATLAS.set("dry", items)


        # ---------- window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)

        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])

        LIST_H = 74 + ROWS * ROW_H + 22          # the list section: "Here:", heads, rows, count

        def full_h():
            M = Kit.MARGIN
            return M + 30 + Kit.GAP + 46 + Kit.GAP + 36 + Kit.GAP + LIST_H + M

        def build_window():
            if st["minimized"]:
                w, h = MINI_W, MINI_H
            else:
                w, h = W, full_h()
            x, y = Kit.load_pos(POS_KEY, (260, 220), (w, h))
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
                # weight: a figure and the bar
                yw = M + 30 + Kit.GAP
                Kit.add_section(g, M, yw, IW, 46, "WEIGHT")
                c["wtext"] = Kit.add_label(g, "", M + 20 + Kit.text_w("WEIGHT"), yw + 6, Kit.HUE_TEXT)
                build_weight_bar(g, c, M + 12, yw + 28, IW - 24)
                # toolbar
                yt = yw + 46 + Kit.GAP
                Kit.add_section(g, M, yt, IW, 36)
                bx = M + 12
                Kit.art_button(g, store, "clear", Kit.ART_CLOSE, bx, yt + 7, "Clear",
                               "Empty the list of dry spots", on_click=queue("clear"))
                bx += 35 + Kit.text_w("Clear") + 16
                Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, bx, yt + 7, "Arrow off",
                               "Take the tracking arrow down", on_click=queue("arrow_off"))
                # the list: the "Here:" line, column heads, the pooled rows, the count
                yl = yt + 36 + Kit.GAP
                Kit.add_section(g, M, yl, IW, LIST_H, "DRY SPOTS  (nearest first)")
                c["here"] = Kit.add_label(g, "", M + 12, yl + 28, Kit.HUE_INFO)
                ping_w = 35 + Kit.text_w("Ping")
                xk, xw, xb = M + 12, M + 12 + 52, M + 12 + 52 + 130
                xp = M + IW - 6 - ping_w
                c["back_w"] = xp - 8 - xb
                yh = yl + 52
                Kit.add_label(g, "What", xk, yh, Kit.HUE_TITLE)
                Kit.add_label(g, "Where", xw, yh, Kit.HUE_TITLE)
                Kit.add_label(g, "When", xb, yh, Kit.HUE_TITLE)
                for k in range(ROWS):
                    ry = yh + 22 + k * ROW_H
                    r = {"key": None, "prev": (None, 0.0), "sig": None, "vis": True, "tip": None,
                         "kind": Kit.add_label(g, "", xk, ry + 3, Kit.HUE_TEXT),
                         "where": Kit.add_label(g, "", xw, ry + 3, Kit.HUE_TEXT),
                         "back": Kit.add_label(g, "", xb, ry + 3, Kit.HUE_INFO)}
                    r["catch"] = Kit.catcher(g, M + 6, ry, xp - 4 - (M + 6), ROW_H, row_click(k),
                                             ROW_TIP)
                    r["plbl"] = Kit.art_button(g, store, "ping%d" % k, Kit.ART_PLAY, xp, ry, "Ping",
                                               PING_TIP, on_click=ping_click(k))
                    r["pbtn"] = store[0].get("ping%d" % k)
                    rows.append(r)
                c["more"] = Kit.add_label(g, "", M + 12, yh + 22 + ROWS * ROW_H + 2, Kit.HUE_INFO)
            Kit.place(g, x, y, w, h)                     # wholly on screen
            win.update({"g": g, "c": c, "store": store, "rows": rows})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))      # saved the moment it is let go
            if st["minimized"] and st["docked"]:         # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            st["drawn"] = st["mini_drawn"] = st["wdrawn"] = None
            st["draw_at"] = 0.0
            refresh(time.time())
            Kit.dispose(old)

        def build_weight_bar(g, c, bx, by, bw):
            """The client's red status line hued grey under one fill per colour
            (only one shows), like Character's weight bar."""
            lw, lh = Kit.pic_size(Kit.LINE_RED)
            fh = max(4, min(11, Kit.pic_size(Kit.LINE_BLUE)[1] or lh or 9))
            if lw > 0:
                Kit.add_tiled(g, Kit.LINE_RED, bx, by, bw, fh, hue=WEIGHT_BG_HUE)
            else:
                Kit.add_tiled(g, Kit.SECTION_TILE, bx, by, bw, fh, 1.0)
            fills = {}
            for kind, art, hue in (("ok", Kit.LINE_POISON, WEIGHT_HUE_OK),
                                   ("warn", Kit.LINE_BLUE, WEIGHT_HUE_WARN),
                                   ("red", Kit.LINE_RED, 0)):
                f = Kit.add_tiled(g, art, bx, by, 1, fh, hue=hue)
                if f is not None:
                    safe(lambda f=f: setattr(f, "IsVisible", False))
                    fills[kind] = f
            c["wfills"] = fills
            c["wbar_w"] = bw

        def row_click(k):
            def handler(*args):
                rows = win["rows"]
                if k >= len(rows):
                    return
                r = rows[k]
                key = r["key"]
                prev, at = r["prev"]
                if prev is not None and time.time() - at < 0.15:   # the row just changed: what was seen
                    key = prev
                if key is not None:
                    queue(("arrow", key))()
            return handler

        def ping_click(k):
            def handler(*args):
                rows = win["rows"]
                if k >= len(rows):
                    return
                r = rows[k]
                key = r["key"]
                prev, at = r["prev"]
                if prev is not None and time.time() - at < 0.15:
                    key = prev
                if key is not None:
                    queue(("ping", key))()
            return handler

        def show_row(r, on):
            if r["vis"] == on:
                return
            r["vis"] = on
            for n in ("where", "back", "catch", "pbtn", "plbl"):
                ctl = r.get(n)
                if ctl is not None:
                    try:
                        ctl.IsVisible = on
                    except Exception:
                        pass
            if not on:
                Kit.set_text(r["kind"], "")

        # ---------- drawing (client thread; only what changed) ----------
        def refresh(now):
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]):
                return                                   # closed or folded: nothing to draw
            c = win["c"]
            if st["minimized"]:
                wt = st["weight"]
                sig = (st["ver"], settings["ore"], settings["wood"], settings["fish"], settings["sand"])
                if st["count"][0] != sig:                # counted only when the list changed
                    st["count"] = (sig, len(shown_spots()))
                n = st["count"][1]
                mkey = (n, wt)                           # (2.6.82) the text made only on a change
                if st["mini_drawn"] is not None and mkey == st["mini_key"]:
                    return
                st["mini_key"] = mkey
                txt = "%s: %s, %d dry spot%s" % (
                    TITLE, ("weight %d%%" % int(wt[2] * 100)) if wt and wt[2] >= 0 else "weight ?",
                    n, "" if n == 1 else "s")
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
            sig = (st["ver"], st["arrow"], settings["ore"], settings["wood"], settings["fish"],
                   settings["sand"])
            if sig == st["drawn"] and now < st["draw_at"] and st["draw_at"] - now <= DRAW_EVERY:
                return
            st["drawn"], st["draw_at"] = sig, now + DRAW_EVERY
            me = read_me() or st["me"]
            listed = []
            for e in shown_spots():                      # (2.6.82: the distance only; the text
                listed.append((dist_of(e, me), e["hi"], e))   # just for the rows shown)
            listed.sort(key=_by_place)                   # nearest first, then the soonest back
            # the "Here:" line: the dry block you stand in, if any
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
                    KIND_NAME[here["kind"]].lower(), back_text(here, now)[0]), W - 2 * Kit.MARGIN - 24),
                    Kit.HUE_BAD)
            elif listed:
                Kit.set_text(c["here"], "Here: nothing known dry", Kit.HUE_GOOD)
            else:
                Kit.set_text(c["here"], Kit.fit(EMPTY_TEXT, W - 2 * Kit.MARGIN - 24), Kit.HUE_INFO)
            back_w = c.get("back_w", 160)
            for k, r in enumerate(win["rows"]):
                if k >= len(listed):
                    if r["key"] is not None:
                        r["prev"] = (r["key"], now)
                        r["key"] = None
                    r["sig"] = None
                    show_row(r, False)
                    continue
                e = listed[k][2]
                where = where_text(e, me)[0]
                key = e["key"]
                if r["key"] != key:
                    r["prev"] = (r["key"], now)
                    r["key"] = key
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
                    try:
                        r["catch"].SetTooltip(row_tip(e, on))
                    except Exception:
                        pass
            more = len(listed) - len(win["rows"])
            Kit.set_text(c["more"], ("+%d farther" % more) if more > 0 else "", Kit.HUE_INFO)

        def draw_weight():
            c = win["c"]
            wt = st["weight"]
            if st["wdrawn"] is not None and wt == st["w_key"]:
                return                                   # (2.6.82) unchanged: no text made
            st["w_key"] = wt
            fills = c.get("wfills")
            if wt is None or wt[2] < 0:
                text, kind, width = "not known yet", None, 0
            else:
                frac = wt[2]
                text = "%d / %d stones (%d%%)" % (wt[0], wt[1], int(frac * 100))
                kind = "red" if frac >= WEIGHT_RED else ("warn" if frac >= WEIGHT_WARN else "ok")
                bw = c.get("wbar_w", 100)
                width = max(1, min(bw, int(round(bw * min(1.0, frac)))))
            sig = (text, kind, width)
            if sig == st["wdrawn"]:
                return
            st["wdrawn"] = sig
            hue = {"red": Kit.HUE_BAD, "warn": Kit.HUE_TITLE}.get(kind, Kit.HUE_TEXT)
            if c.get("wtext") is not None:
                Kit.set_text(c["wtext"], text, hue)
            for k, f in (fills or {}).items():
                try:
                    if k == kind:
                        Kit.ui_w(f, width)
                    f.IsVisible = k == kind
                except Exception:
                    pass


        # ---------- settings page (drawn inside the Virtue Assistant window) ----------
        SEC2_H, SEC3_H = 62, 66
        RESPAWN_NOTE = ("Back in: ore and sand 10-20 min, wood 20-30, fish 10-20, counted from the "
                        "block's first harvest (3x as long in guarded towns).")

        def kind_caption(kind):
            return "%s (%s)" % (KIND_NAME[kind], KIND_SKILL[kind])

        def kind_cols(w):
            """2 when the four kinds fit two to a row, else 1."""
            widest = max(Kit.text_w(kind_caption(k)) for k in KINDS)
            return 2 if widest + 30 <= (w - 24) // 2 else 1

        def note_lines(w):
            """The two grey lines under the kinds: the unticked note, the respawn times."""
            return ["Unticked kinds are hidden, not forgotten."] + Kit.wrap(RESPAWN_NOTE, w - 28)

        def sec1_h(w):
            rows = (len(KINDS) + kind_cols(w) - 1) // kind_cols(w)
            return 32 + rows * 26 + 6 + 26 + 2 + 20 * len(note_lines(w)) + 10

        def config_height(w):
            return sec1_h(w) + Kit.GAP + SEC2_H + Kit.GAP + ATLAS_H + Kit.GAP + SEC3_H

        def build_config(g, x, y, w):
            c = {}
            h1 = sec1_h(w)
            Kit.add_section(g, x, y, w, h1, "WHAT TO WATCH")
            cols = kind_cols(w)
            half = (w - 24) // 2
            for i, kind in enumerate(KINDS):
                cx = x + 12 + (i % cols) * half
                cy = y + 32 + (i // cols) * 26
                c[kind] = Kit.add_check(g, kind_caption(kind), cx, cy, settings[kind],
                                        "List the spots where the shard says the %s has run out"
                                        % KIND_NAME[kind].lower())
            yk = y + 32 + ((len(KINDS) + cols - 1) // cols) * 26 + 6
            c["keep"] = Kit.add_check(g, "Keep the list when Virtue Assistant stops (per character)",
                                      x + 12, yk, settings["keep"],
                                      "Unticked: the list starts empty at every start")
            for i, ln in enumerate(note_lines(w)):
                Kit.add_label(g, ln, x + 12, yk + 28 + 20 * i, Kit.HUE_INFO)
            y2 = y + h1 + Kit.GAP
            Kit.add_section(g, x, y2, w, SEC2_H, "WEIGHT  (yellow at %d%%, red at %d%%)"
                            % (int(WEIGHT_WARN * 100), int(WEIGHT_RED * 100)))
            c["alert"] = Kit.add_check(g, "Alert as you cross the red line", x + 12, y2 + 32,
                                       settings["alert"],
                                       "One alert each time you cross %d%% of your maximum weight "
                                       "(sound: Settings > Alerts); quiet while Inventory > Paperdoll "
                                       "is on, which has its own" % int(WEIGHT_RED * 100))
            y3 = y2 + SEC2_H + Kit.GAP
            atlas_section(g, x, y3, w, "dry")
            y4 = y3 + ATLAS_H + Kit.GAP
            Kit.add_section(g, x, y4, w, SEC3_H, "DEBUG  (for checking the shard's texts)")
            c["say"] = Kit.add_check(g, "Print each harvest line read in the journal", x + 12, y4 + 30,
                                     settings["say"],
                                     "Prints every harvest line this part reads, with its speaker "
                                     "and the spot it took, for checking the shard's wording")
            page["c"] = c

        def poll_config():
            c = page["c"]
            if c is None:
                return
            changed = False
            for k in ("ore", "wood", "fish", "sand", "keep", "alert", "say"):
                ctl = c.get(k)
                if ctl is None:
                    continue
                try:                                     # a plain try: this runs every poll
                    on = bool(ctl.IsChecked)
                except Exception:
                    continue
                if on != settings[k]:
                    settings[k] = on
                    changed = True
                    if k == "keep":
                        st["save_due"] = True            # kept: written now; not kept: emptied
                    elif k == "alert" and on:
                        st["w_armed"] = True
            if changed:
                save_settings()
                st["drawn"] = st["mini_drawn"] = None

        def config_closed():
            page["c"] = None


        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "drawn": None,
                       "mini_drawn": None, "wdrawn": None, "arrow": None, "ping": None,
                       "w_armed": True, "weight": None, "w_at": 0.0, "draw_at": 0.0,
                       "expire_at": 0.0, "save_due": False, "save_at": 0.0, "me": None,
                       "count": (None, 0), "last_now": None, "atlas": None,
                       "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            del jobs[:]
            first.clear()
            load_settings()
            load_spots()
            st["rd"] = Journal.reader()                  # the lines from now on
            if hasattr(HOST, "alert_kind"):
                safe(lambda: HOST.alert_kind(WEIGHT_ALERT, "Weight near the limit",
                                             WEIGHT_ALERT_SOUND))
            read_me()
            build_window()
            HOST.dock_add(KEY, Kit.dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw")))

        def _tick():
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])                    # on_disposed turns the module off
                return
            now = time.time()
            last, st["last_now"] = st["last_now"], now
            if last is not None and now < last - CLOCK_JUMP:
                rebase(now - last)                       # the clock was set back
            q = st["queue"]
            while q:
                action = q.pop(0)
                kind = action[0] if isinstance(action, tuple) else action
                if action == "settings":
                    HOST.show_settings(KEY)
                elif action == "toggle_min":
                    st["minimized"] = not st["minimized"]
                    st["docked"] = False
                    HOST.dock_forget(KEY)                # its own minimized form, not the bar
                    Kit.save_min(MIN_KEY, st["minimized"])
                    build_window()
                elif action == "to_bar":
                    HOST.dock_to_bar(KEY, TITLE)         # folds in now, or once the bar is up
                elif action == "redraw":
                    build_window()
                elif action == "clear":
                    clear_spots()
                elif action == "arrow_off":
                    arrow_off()
                elif kind == "arrow":
                    arrow_to(action[1])
                elif kind == "ping":
                    ping_spot(action[1])
                if win["g"] is None:
                    return
            read_journal(now)
            if now >= st["expire_at"] or st["expire_at"] - now > EXPIRE_EVERY:
                st["expire_at"] = now + EXPIRE_EVERY
                expire(now)
            av = (st["ver"], settings["ore"], settings["wood"], settings["fish"], settings["sand"])
            if av != st["atlas"]:                        # on TazUO's World Map (2.6.51)
                st["atlas"] = av
                atlas_publish()
            read_weight(now)
            send_ping(now)
            refresh(now)
            if st["save_due"] and (now >= st["save_at"] or st["save_at"] - now > SAVE_EVERY) \
                    and not jobs:
                jobs.append(save_spots_job)

        def _thread_tick():
            """Script thread, right after the client tick: the list's save."""
            while jobs and not st["shutting"]:
                jobs.pop(0)()

        def _thread_wanted():
            return bool(jobs)                    # (2.6.82) only with a save queued

        def _stop():
            st["shutting"] = True
            HOST.dock_remove(KEY)
            if st["arrow"] is not None:
                arrow_off()
            st["ping"] = None
            st["rd"] = None
            del jobs[:]
            save_pos()
            # folded into the bar is the host's wish (dock_wanted), not "minimized"
            Kit.save_min(MIN_KEY, st["minimized"] and not st["docked"])
            save_settings()
            Kit.put_var(SPOTS_KEY, spots_text() if settings["keep"] else "")
            st["save_due"] = False
            g, win["g"] = win["g"], None
            win["rows"] = []
            win["c"] = {}
            Kit.dispose(g)

        load_settings()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop,
                  "client_tick": True,          # tick on the client thread: no waits in it
                  "thread_tick": _thread_tick,  # the list's save, on the script's thread
                  "thread_wanted": _thread_wanted,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        # ============================= MODULE END ====================================
        return MODULE

    def _part_traps():
        """Builds the module in its own namespace and returns its hooks."""
        # =============================================================================
        #  MODULE: Traps & Fields (Trap Highlight before 2.6.52)  -  recolours traps
        #  on the ground bright green and pulses them red on a slow cycle so they
        #  stand out at a glance
        #
        #  How it works: the client cannot draw an outline round a world item, so
        #  the trap itself is recoloured. The item is held at the green hue and,
        #  once per cycle, flashes to the red hue for a short beat (the "pulse").
        #  Original hues are put back when a trap leaves range, vanishes, or the
        #  module is turned off. Nothing is sent to the server: the recolour is
        #  client-side only, so the shard never sees it.
        #
        #  Trap pings (2.6.02): with Map Pings on, each trap found gets one Danger!
        #  map ping on its tile, for you and your guildmates. Each trap is pinged
        #  once only (by serial and by spot), even if it leaves range and comes
        #  back; "Ping traps on screen" on the window pings every trap in range now
        #  and lets each trap be pinged once more when next found. Pings go out one
        #  at a time at Map Pings' own pace. On / off on the settings page.
        #
        #  Magic fields (2.6.05): fire, poison, energy and paralyze fields on the
        #  ground are a second group, recoloured with their own hues (paralyze
        #  fields get one of their own, so they stand out most), client-side only
        #  like the traps; no pulse and no pings. An optional overhead text names a
        #  field when it appears. On / off and the hues on the settings page.
        #
        #  New trap alert (2.6.05): the first time a trap comes into range (once
        #  per trap), an alert (sound, banner, journal line) says where. Its sound,
        #  or off, is set on Settings > Alerts.
        # =============================================================================
        KEY = "traphl"
        TITLE = "Traps & Fields"

        # ------------------------------- CONFIG --------------------------------------
        SETTINGS_KEY = "TrapHL_settings"     # per character (the old name stays)
        POS_KEY = "TrapHL_pos"
        VIEW_KEY = "TrapHL_view"             # minimized / paused, kept for the next start
        W = 320                              # full window (room for Minimize and Fold into the bar)
        BTN_H = 40                           # its one section: the Ping traps on screen button (2.6.51)
        H = Kit.MARGIN + 30 + Kit.GAP + BTN_H + Kit.MARGIN
        MINI_W, MINI_H = 320, 46             # minimized bar
        TRAY_ICON = 0x113C                   # the Action Bar's tray button (gas trap)

        HUE_GREEN = 68        # bright green (same hue Kit uses for "good")
        HUE_RED = 33          # red for the pulse
        DEFAULT_RANGE = 14    # tiles scanned round the player
        DEFAULT_CYCLE = 2.0   # seconds per pulse (green -> red beat -> green)
        PULSE_BEAT = 0.35     # how long the red beat lasts inside each cycle, seconds
        SCAN_EVERY = 1.0      # seconds between ground scans (the pulse runs every tick)
        HUE_CHECK_EVERY = 3   # every N-th scan reads the hues back (a hue the server put back)
        HUE_MAX = 3000        # client hue numbers run 1-3000
        FIELD_SETTLE = 0.7    # seconds the graphics text stands unchanged before it is applied
        PING_SERVICE = "pings.send"   # Map Pings' service (HOST.services) that sends a ping
        PING_KIND = "danger"          # the ping put on a trap: Danger!
        PING_WHO = "You (trap)"       # how Map Pings names the ping in the journal / world map
        PINGED_CAP = 5000             # traps remembered as pinged before the memory starts over
        PING_GAP = 0.75               # Map Pings sends one automatic ping this often at most (its
                                      #   PING_RATE_SECS): waiting here saves asking it in between

        # Item graphics of ground traps. These are the classic RunUO trap art ids;
        # In Mani Ylem may use others, so VERIFY IN GAME (single-click a trap with
        # the DEBUG box "Print each new trap's graphic id in the journal" on, or
        # check the shard's trap list) and edit the list on the settings page. Any
        # hue of these graphics counts.
        DEFAULT_GRAPHICS = [
            0x1103, 0x1116, 0x11AC, 0x11B1,          # saw traps (wall / floor)
            0x11A0, 0x11A8, 0x11B8,                  # spike traps
            0x113C, 0x1147,                          # gas traps
            0x10F5, 0x10FC,                          # stone face traps
            0x1125,                                  # mushroom trap
            0x1B71, 0x1B72, 0x1B73, 0x1B74,          # fire column / flame spurt / giant spike
            0x0E70,                                  # trap door (shard-specific, unverified)
        ]
        # Also treat any ground item whose name (once the client knows it) contains
        # one of these words as a trap. Names are only known after a tooltip/single
        # click, so this is a backup to the graphics list.
        NAME_WORDS = ("trap",)
        # ...but not things that are only named after a trap: a Magic Trap / Remove
        # Trap scroll or a tinker's trap kit lying on the floor isn't one.
        NAME_SKIP = ("scroll", "kit")

        # Magic fields (2.6.05). Item ids from Tiledata.mul ("Field of fire",
        # "Field of Poison", "field of paralysis", "field of energy"); RunUO's field
        # spells place the first id of each pair, east-west / north-south: fire
        # 0x398C / 0x3996, poison 0x3915 / 0x3922, paralyze 0x3967 / 0x3979, energy
        # 0x3946 / 0x3956 (the client animates the rest). Unchecked in game.
        FIELDS_KEY = "TrapHL_fields"           # per character (new in 2.6.05): "on=1;hue=53;para=1153;say=0"
        FIELD_RANGES = (("fire", 0x398C, 0x399F), ("poison", 0x3914, 0x3929),
                        ("paralyze", 0x3967, 0x398A), ("energy", 0x3946, 0x3964))
        FIELD_LOOKUP = (0x398C, 0x3996, 0x3915, 0x3922, 0x3967, 0x3979, 0x3946, 0x3956)
        #               ^ looked up one by one only on a TazUO build without GetItemsOnGround
        FIELD_HUE = 0x0035        # fire, poison and energy fields (53: gold); 0 = leave as they are
        PARALYZE_HUE = 0x0481     # paralyze fields (1153: white); 0 = leave as they are
        FIELD_WORDS = {"fire": ("Fire field", Kit.HUE_TITLE), "poison": ("Poison field", Kit.HUE_TITLE),
                       "energy": ("Energy field", Kit.HUE_TITLE),
                       "paralyze": ("Paralyze field!", Kit.HUE_BAD)}   # the overhead text, its hue
        FIELD_SAY_NEAR = 3        # tiles: one overhead text per field, not one per tile of it...
        FIELD_SAY_GAP = 10.0      # ...for this long
        FIELD_SAY_CAP = 20        # fields remembered for that

        # New trap alert (2.6.05): Settings > Alerts lists it (sound, on / off)
        ALERT_TRAP = "traphl.trap"
        ALERT_TRAP_SOUND = 0x1EF  # trap snap
        ALERTED_CAP = 5000        # traps remembered as alerted before the memory starts over
        # -----------------------------------------------------------------------------
        FIELD_GFX = {}                                   # graphic -> kind
        for _kind, _lo, _hi in FIELD_RANGES:
            for _g in range(_lo, _hi + 1):
                FIELD_GFX[_g] = _kind
        NO_FIELDS = {}

        settings = {"range": DEFAULT_RANGE, "cycle": DEFAULT_CYCLE, "pulse": True,
                    "green": HUE_GREEN, "red": HUE_RED, "by_name": True,
                    "graphics": list(DEFAULT_GRAPHICS),
                    "ping": True,       # Danger! map ping on each trap, once (2.6.02)
                    # magic fields (2.6.05; saved in FIELDS_KEY)
                    "fields": True, "field_hue": FIELD_HUE, "para_hue": PARALYZE_HUE,
                    "field_say": False}
        st = {"shutting": False, "minimized": False, "docked": False, "queue": [],
              "last_scan": 0.0, "scans": 0,
              "tracked": {},        # serial -> {"item": PyItem, "orig": hue, "set": hue painted}
              "say_graphics": False, "paused": False,
              # trap pings: serials / (facet, x, y) spots already pinged, and the
              # serials waiting for their ping (sent one at a time, Map Pings' pace)
              "pinged": set(), "pinged_spots": set(), "ping_wait": [],
              "ping_sent": 0, "ping_noted": False, "ping_svc": None,
              "ping_next": 0.0,     # no ping is asked for before this time (PING_GAP)
              "fields": {},         # serial -> {"item", "orig", "set" (hue painted or 0), "kind"}
              "field_said": [],     # (kind, x, y, time) of the fields named overhead lately
              "alerted": set(),     # trap serials the new-trap alert was raised for
              "atlas_traps": [],    # (x, y, facet) of the traps seen lately, for the Atlas (2.6.51)
              "atlas_ver": 0, "atlas_done": -1, "atlas_map": None,
              "pause_want": None}   # the settings page's Paused box, for the next tick (2.6.51)
        win = {"g": None, "c": {}, "store": ({}, {})}
        page = {"c": None, "store": ({}, {}), "gfx_typed": None, "gfx_since": 0.0}


        # ---------- saved settings ----------
        def load_settings():
            p = Kit.get_var(SETTINGS_KEY).split("|")
            if len(p) < 7:
                return
            try:
                settings["range"] = max(1, min(30, int(p[0])))
                settings["cycle"] = max(0.5, min(10.0, float(p[1])))
                settings["pulse"] = p[2] == "1"
                settings["green"] = int(p[3])
                settings["red"] = int(p[4])
                settings["by_name"] = p[5] == "1"
                gl = parse_graphics(p[6])
                if gl:
                    settings["graphics"] = gl
                if len(p) >= 8:                          # new trailing field (2.6.02); on when absent
                    settings["ping"] = p[7] != "0"
            except Exception:
                pass


        def load_fields():
            """The magic-field settings: their own key (2.6.05), so older saves load
            with the defaults and the older version never sees them."""
            v = {}
            for part in Kit.get_var(FIELDS_KEY).split(";"):
                if "=" in part:
                    k, val = part.split("=", 1)
                    v[k.strip()] = val.strip()
            settings["fields"] = v.get("on") != "0"
            settings["field_say"] = v.get("say") == "1"
            for k, key, default in (("hue", "field_hue", FIELD_HUE), ("para", "para_hue", PARALYZE_HUE)):
                try:
                    settings[key] = max(0, min(HUE_MAX, int(v[k])))
                except (KeyError, ValueError):
                    settings[key] = default


        def save_fields():
            Kit.put_var(FIELDS_KEY, "on=%d;hue=%d;para=%d;say=%d" % (
                int(settings["fields"]), settings["field_hue"], settings["para_hue"],
                int(settings["field_say"])))


        def save_settings():
            data = "|".join([str(settings["range"]), "%.2f" % settings["cycle"],
                             "1" if settings["pulse"] else "0", str(settings["green"]),
                             str(settings["red"]), "1" if settings["by_name"] else "0",
                             graphics_text(), "1" if settings["ping"] else "0"])
            Kit.put_var(SETTINGS_KEY, data)


        def parse_graphics(text):
            out = []
            for tok in str(text).replace(";", ",").replace(" ", ",").split(","):
                tok = tok.strip()
                if not tok:
                    continue
                try:
                    v = int(tok, 16)                     # with or without 0x: always hex
                except Exception:
                    continue
                if 0 < v < 0x10000 and v not in out:
                    out.append(v)
            return out


        def graphics_text():
            return ", ".join("0x%04X" % g for g in settings["graphics"])


        def save_pos():
            Kit.save_pos(POS_KEY, win["g"])


        def load_view():
            raw = Kit.get_var(VIEW_KEY)
            v = dict(p.split("=", 1) for p in raw.split(";") if "=" in p)
            st["minimized"] = v.get("min") == "1"
            st["paused"] = v.get("paused") == "1"
            st["say_graphics"] = v.get("say") == "1"       # new field (2.6.01); off when absent
            st["view_saved"] = raw


        def save_view():
            """Minimized, paused and the DEBUG "print graphic ids" box are saved the
            moment they change."""
            data = "min=%d;paused=%d;say=%d" % (int(bool(st["minimized"])), int(bool(st["paused"])),
                                                int(bool(st["say_graphics"])))
            if data != st.get("view_saved"):
                st["view_saved"] = data
                Kit.put_var(VIEW_KEY, data)


        # ---------- item hue (client-side recolour) ----------
        _hue_setters = {}       # type name -> way that worked ("attr", "api", "clr", "none")
        _ent_member = {}        # wrapper type -> the field/property that holds the client entity


        def _member_value(m, item):
            return m.GetValue(item, None) if hasattr(m, "GetIndexParameters") else m.GetValue(item)


        def _clr_entity(item):
            """The ClassicUO entity behind a Legion item wrapper, found by looking for
            a field/property that holds an object with Hue and Serial. The member
            that held it is remembered per wrapper type, so the reflection search
            runs once, not on every recolour (the pulse recolours every cycle)."""
            m = _ent_member.get(type(item))
            if m is not None:
                try:
                    v = _member_value(m, item)
                    if v is not None and v is not item:
                        return v
                except Exception:
                    pass
            try:
                import clr
                from System.Reflection import BindingFlags
                flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                t = clr.GetClrType(type(item))
                while t is not None:
                    for m in list(t.GetProperties(flags)) + list(t.GetFields(flags)):
                        try:
                            v = _member_value(m, item)
                        except Exception:
                            continue
                        if v is None or v is item:
                            continue
                        vt = v.GetType()
                        if vt.GetProperty("Hue") is not None and vt.GetProperty("Serial") is not None:
                            _ent_member[type(item)] = m
                            return v
                    t = t.BaseType
            except Exception:
                pass
            return None


        def set_hue(item, hue):
            """Recolour an item in the client. Tries the item's own SetHue (the
            documented way on current TazUO builds), then the wrapper's Hue, then an
            API call if this TazUO build has one, then the client entity directly.
            The way that worked is remembered per wrapper type."""
            hue = int(hue) & 0xFFFF
            tn = type(item).__name__
            way = _hue_setters.get(tn)
            if way == "none":
                return False
            for w in ((way,) if way is not None else _HUE_WAYS):
                if _HUE_SET[w](item, hue):
                    _hue_setters[tn] = w
                    return True
            # Only a type on which no way ever worked is given up on. A way that
            # worked before and fails now means this one item is gone (it left
            # range a moment ago); the next trap still gets recoloured. (Before,
            # one such miss switched recolouring off for the rest of the session.)
            if way is None:
                _hue_setters[tn] = "none"
            return False


        def _hue_by_method(item, hue):
            fn = getattr(item, "SetHue", None)
            if fn is None:
                return False
            try:
                fn(hue)
                return True
            except Exception:
                return False


        def _hue_by_attr(item, hue):
            try:
                item.Hue = hue
                return int(item.Hue) == hue
            except Exception:
                return False


        def _hue_by_api(item, hue):
            for name in ("SetHue", "SetItemHue"):
                fn = getattr(API, name, None)
                if fn is not None:
                    try:
                        fn(item.Serial, hue)
                        return True
                    except Exception:
                        pass
            return False


        def _hue_by_clr(item, hue):
            ent = _clr_entity(item)
            if ent is None:
                return False
            try:
                ent.Hue = hue
                return True
            except Exception:
                return False


        _HUE_WAYS = ("method", "attr", "api", "clr")
        _HUE_SET = {"method": _hue_by_method, "attr": _hue_by_attr, "api": _hue_by_api,
                    "clr": _hue_by_clr}


        def int_of(item, name):
            try:
                return int(getattr(item, name) or 0)
            except Exception:
                return 0


        def get_hue(item):
            try:                                 # 2.6.82: a direct read, not getattr by name
                return int(item.Hue or 0)
            except Exception:
                return 0


        def xy_of(item):
            """(x, y) of an item, 0 for one that can't be read (as int_of)."""
            try:
                x = int(item.X or 0)
            except Exception:
                x = 0
            try:
                y = int(item.Y or 0)
            except Exception:
                y = 0
            return x, y


        # ---------- finding traps ----------
        #  The ground is read once per scan (once a second). API.GetItemsOnGround
        #  hands back every ground item within range in one call; on a build
        #  without it, each trap graphic is looked up with API.FindTypeAll in the
        #  first call form the build accepts (found on the first scan, then reused).
        #  Before 2.5.22 the one-call path looked for API.NearestEntities /
        #  API.GetAllItems, which TazUO doesn't have, so every scan made up to four
        #  FindTypeAll attempts for each of the 17 graphics (each failed attempt an
        #  exception), and "Also highlight ground items the client names 'trap'"
        #  never looked at a single name.
        scan_how = {"ground": None,     # None: not tried yet; True: GetItemsOnGround works; False: not here
                    "form": None}       # index into FTA_FORMS that this build accepts
        ANY_CONTAINER = 0xFFFFFFFF      # FindTypeAll's own default: any container, so ground too
        FTA_FORMS = (lambda g, r: API.FindTypeAll(g, ANY_CONTAINER, r, 0xFFFF),
                     lambda g, r: API.FindTypeAll(g, 0, r, 0xFFFF),    # the forms tried before
                     lambda g, r: API.FindTypeAll(g, ANY_CONTAINER, r),
                     lambda g, r: API.FindTypeAll(g, 0, r))
        # 2.6.82: the verdict per ground serial, not the name: serial -> (graphic,
        # kind, retry): kind 1 trap, 2 field, 0 neither; retry 0 = final, else the
        # scan number from which an unnamed item's name is read again (names only
        # come after a hover or a click; before 2.6.82 it was read every scan).
        # Remade under new settings (VERDICT_SIG) and kept to what is on the ground.
        verdicts = {}
        NAME_RETRY = 5                  # scans between looks at an unnamed item's name
        VERDICT_SIG = {"gfx": None, "wanted": frozenset(), "by_name": None, "fields": None}


        SKIP_SCAN = False                   # ground_all's "the call failed this once: skip this scan"


        def ground_all(rng):
            """Every item on the ground within rng (one call); None when this
            build can't do that (then it's FindTypeAll per graphic); SKIP_SCAN when
            the call worked before and raised this once (a transient error: the
            tracked traps are kept as they are instead of being read as gone and
            restored, then tracked again a second later)."""
            if scan_how["ground"] is False:
                return None
            fn = scan_how.get("fn")                 # looked up once (2.6.82)
            if fn is None:
                fn = getattr(API, "GetItemsOnGround", None)
                if fn is None:
                    scan_how["ground"] = False
                    return None
                scan_how["fn"] = fn
            try:
                res = fn(rng)
            except Exception:
                if scan_how["ground"] is None:      # never worked: this build's call is different
                    scan_how["ground"] = False
                    return None
                return SKIP_SCAN                    # worked before: try again next scan
            scan_how["ground"] = True
            return res if res is not None else ()   # None = nothing on the ground (2.6.82: no copy)


        def ground_items_of(graphic, rng):
            """Ground items of one graphic within range, any hue."""
            form = scan_how["form"]
            for k in ((form,) if form is not None else range(len(FTA_FORMS))):
                try:
                    res = FTA_FORMS[k](graphic, rng)
                except Exception:
                    continue
                scan_how["form"] = k
                return [i for i in (res or []) if is_on_ground(i)]
            return []


        def is_on_ground(item):
            try:
                cont = int(item.Container or 0)
            except Exception:
                cont = 0
            if cont and cont not in (0, 0xFFFFFFFF, -1):
                return False
            try:
                rp = int(item.RootContainer or 0)
                return not rp or rp == int(item.Serial)
            except Exception:
                return True


        def named_trap(it):
            """The client calls this ground item a trap (NAME_WORDS): True / False,
            or None while the client has no name for it yet (asked again later).
            The verdict is kept per serial by scan (2.6.82), so a named item's name
            is read once."""
            try:
                name = str(it.Name or "").lower()
            except Exception:
                name = ""
            if not name:
                return None
            for w in NAME_SKIP:
                if w in name:
                    return False
            for w in NAME_WORDS:
                if w in name:
                    return True
            return False


        def verdict_sig():
            """The settings the verdicts were made under: the cache starts over
            when one of them changes (2.6.82)."""
            sig = VERDICT_SIG
            gl = settings["graphics"]
            if sig["gfx"] is not gl or sig["by_name"] != settings["by_name"] or \
                    sig["fields"] != settings["fields"]:
                sig["gfx"], sig["wanted"] = gl, frozenset(gl)
                sig["by_name"], sig["fields"] = settings["by_name"], settings["fields"]
                verdicts.clear()
            return sig["wanted"]


        def scan():
            rng = int(settings["range"])
            st["atlas_map"] = None                       # your facet, read once if a trap is new
            found = {}
            ffound = {}                                  # magic fields (2.6.05)
            items = ground_all(rng)
            if items is SKIP_SCAN:                       # a transient error: nothing changes
                return
            st["scans"] += 1
            check_hues = st["scans"] % HUE_CHECK_EVERY == 0
            field_gfx = FIELD_GFX if settings["fields"] else NO_FIELDS
            if items is None:                            # one look per trap graphic
                for gfx in settings["graphics"]:
                    for it in ground_items_of(gfx, rng):
                        try:
                            found[int(it.Serial)] = it
                        except Exception:
                            pass
                if field_gfx:                            # and per field id RunUO places
                    for gfx in FIELD_LOOKUP:
                        if gfx in settings["graphics"]:     # looked up as a trap already
                            continue
                        for it in ground_items_of(gfx, rng):
                            try:
                                s_ = int(it.Serial)
                                if s_ not in found:
                                    ffound[s_] = it
                            except Exception:
                                pass
            else:                                        # one look at the ground: graphic first
                wanted = verdict_sig()
                by_name = settings["by_name"]
                scans = st["scans"]
                old = verdicts
                seen = {}
                for it in items:
                    try:
                        serial = int(it.Serial)
                        g = int(it.Graphic)
                        v = old.get(serial)
                        if v is not None and v[0] == g and (not v[2] or scans < v[2]):
                            kind = v[1]                  # known: no name read (2.6.82)
                            seen[serial] = v
                        else:
                            retry = 0
                            if g in wanted:
                                kind = 1
                            elif by_name and g not in field_gfx:
                                named = named_trap(it)
                                if named is None:        # no name yet: asked again later
                                    kind, retry = 0, scans + NAME_RETRY
                                else:
                                    kind = 1 if named else 0
                            else:
                                kind = 2 if g in field_gfx else 0
                            seen[serial] = (g, kind, retry)
                        if kind == 1:
                            found[serial] = it
                        elif kind == 2:
                            ffound[serial] = it
                    except Exception:
                        continue
                verdicts.clear()                         # only what is still on the ground
                verdicts.update(seen)
            tracked = st["tracked"]
            new_traps = []                               # for the new-trap alert
            # newly seen: remember the original hue, paint green
            for serial, it in found.items():
                rec = tracked.get(serial)
                if rec is None:
                    orig = get_hue(it)
                    if orig in (settings["green"], settings["red"]):
                        orig = 0
                    tracked[serial] = {"item": it, "orig": orig, "set": settings["green"]}
                    set_hue(it, settings["green"])
                    atlas_seen(it)
                    if settings["ping"] and serial not in st["pinged"]:
                        st["ping_wait"].append(serial)   # its Danger! ping, sent by send_pings
                    if serial not in st["alerted"]:
                        new_traps.append(it)
                    if st["say_graphics"]:
                        API.SysMsg("%s: trap 0x%04X (serial 0x%X) at %d, %d." %
                                   (TITLE, int_of(it, "Graphic"), serial, int_of(it, "X"),
                                    int_of(it, "Y")), Kit.HUE_INFO)
                else:
                    rec["item"] = it
                    # the pulse only sets a hue when it changes; every HUE_CHECK_EVERY-th
                    # scan, with the item freshly looked up, a hue the server or client
                    # put back is painted over again (one wrapper read per trap, so not
                    # every scan: the pulse repaints within a cycle anyway)
                    if check_hues and get_hue(it) != rec["set"]:
                        set_hue(it, rec["set"])
            # gone: put the hue back
            gone = [s for s in tracked if s not in found]
            for serial in gone:
                restore(serial)
            # a trap that left before its ping went out stops waiting (it is queued
            # again if it comes back, so it is never in the list twice)
            if gone and st["ping_wait"]:
                st["ping_wait"] = [s for s in st["ping_wait"] if s in tracked]
            if new_traps:
                alert_new_traps(new_traps)
            if ffound or st["fields"]:
                scan_fields(ffound, check_hues)


        # ---------- traps on TazUO's World Map (the Atlas, 2.6.51) ----------
        ATLAS_TRAPS = 20          # the most recent traps seen this session, shown at most

        def atlas_seen(it):
            """A trap newly in range: it goes on the Atlas list (newest last; each
            spot once; the oldest leaves past ATLAS_TRAPS)."""
            x, y = xy_of(it)
            if x <= 0 or y <= 0:
                return
            if st["atlas_map"] is None:
                try:
                    st["atlas_map"] = int(API.GetMap())
                except Exception:
                    return
            spot = (x, y, st["atlas_map"])
            seen = st["atlas_traps"]
            if spot in seen:
                return
            seen.append(spot)
            if len(seen) > ATLAS_TRAPS:
                del seen[0]
            st["atlas_ver"] += 1

        def atlas_publish():
            items = {}
            for x, y, m in st["atlas_traps"]:
                items[atlas_name("Trap %d %d" % (x, y))] = (x, y, m, "red")
            ATLAS.set("traps", items)


        # ---------- the new-trap alert (2.6.05) ----------
        DIRS = ("north", "north-east", "east", "south-east", "south", "south-west", "west",
                "north-west")


        def where(dx, dy):
            """'3 tiles north-east' for an offset from you (2.6.82: the offset the
            caller already has, not read again)."""
            d = max(abs(dx), abs(dy))
            if d == 0:
                return "under you"
            # eight ways round, north up (y grows to the south)
            a = math.degrees(math.atan2(dx, -dy)) % 360.0
            return "%d tile%s %s" % (d, "" if d == 1 else "s", DIRS[int((a + 22.5) // 45.0) % 8])


        def alert_new_traps(its):
            """One alert per scan for the traps seen for the first time (each trap
            once: its serial is remembered)."""
            alerted = st["alerted"]
            if len(alerted) + len(its) > ALERTED_CAP:    # a long session: start over
                alerted.clear()
            for it in its:
                try:
                    alerted.add(int(it.Serial))
                except Exception:
                    pass
            fn = getattr(HOST, "alert", None)
            if fn is None:
                return
            p = API.Player
            try:                                         # read once, not per trap (2.6.82)
                px, py = int(p.X), int(p.Y)
            except Exception:
                px = py = None
            best, best_d, bdx, bdy = None, None, 0, 0
            if px is not None:
                for it in its:
                    try:
                        dx, dy = int(it.X) - px, int(it.Y) - py
                    except Exception:
                        continue
                    d = max(abs(dx), abs(dy))
                    if best_d is None or d < best_d:
                        best, best_d, bdx, bdy = it, d, dx, dy
            w = where(bdx, bdy) if best is not None else ""
            if len(its) == 1:
                text = "A trap %s" % w if w else "A trap in range"
            else:
                text = "%d new traps in range%s" % (len(its), " (nearest %s)" % w if w else "")
            try:
                # rate-limited per trap (who), not per text: two traps that come into
                # range at the same distance and way are two alerts
                fn(ALERT_TRAP, text, who=int((best if best is not None else its[0]).Serial))
            except Exception:
                pass


        # ---------- magic fields (2.6.05) ----------
        def field_hue(kind):
            return settings["para_hue"] if kind == "paralyze" else settings["field_hue"]


        def scan_fields(ffound, check_hues):
            """Fields on the ground: new ones painted their hue (and named overhead
            if asked), known ones repainted when the hue changed on the settings page
            or the server put theirs back, gone ones given their own hue back."""
            fields = st["fields"]
            said_now = []
            for serial, it in ffound.items():
                rec = fields.get(serial)
                if rec is None:
                    kind = FIELD_GFX.get(int_of(it, "Graphic"))
                    if kind is None:
                        continue
                    want = field_hue(kind)
                    orig = get_hue(it)
                    if orig and orig in (settings["field_hue"], settings["para_hue"]):
                        orig = 0                         # left painted by a run that never stopped
                    fields[serial] = rec = {"item": it, "orig": orig, "set": want, "kind": kind}
                    if want:
                        set_hue(it, want)
                    if settings["field_say"]:
                        said_now.append(rec)
                    continue
                rec["item"] = it
                want = field_hue(rec["kind"])
                if want != rec["set"]:                   # the hue changed on the settings page
                    set_hue(it, want if want else rec["orig"])
                    rec["set"] = want
                elif want and check_hues and get_hue(it) != want:
                    set_hue(it, want)
            for serial in [s_ for s_ in fields if s_ not in ffound]:
                restore_field(serial)
            if said_now:
                say_fields(said_now)


        def say_fields(recs):
            """An overhead text on each new field: once per field, not once per tile
            of it. A tile within FIELD_SAY_NEAR of a field tile of the same kind seen
            in the last FIELD_SAY_GAP seconds belongs to that field (so a wall, taken
            tile by tile along its line, is one field however long)."""
            now = time.time()
            said = [e for e in st["field_said"] if now - e[3] < FIELD_SAY_GAP]
            spots = []
            for rec in recs:
                it = rec["item"]
                x, y = xy_of(it)
                spots.append((x, y, rec["kind"], it))
            spots.sort(key=_spot_key)                    # along the wall's line
            for x, y, kind, it in spots:
                dup = False
                for k, sx, sy, t in said:
                    if k == kind and abs(sx - x) <= FIELD_SAY_NEAR and abs(sy - y) <= FIELD_SAY_NEAR:
                        dup = True
                        break
                said.append((kind, x, y, now))           # the field's tiles, said or not
                if dup:
                    continue
                text, hue = FIELD_WORDS.get(kind, ("Field", Kit.HUE_TITLE))
                try:
                    API.HeadMsg(text, int(it.Serial), hue)
                except Exception:
                    pass
            st["field_said"] = said[-FIELD_SAY_CAP:]


        def _spot_key(e):
            return (e[0], e[1])


        def restore_field(serial):
            rec = st["fields"].pop(serial, None)
            if rec is None or not rec["set"]:
                return
            try:                                         # plain try (2.6.82)
                it = API.FindItem(serial) or rec["item"]
            except Exception:
                it = rec["item"]
            if it is not None:
                set_hue(it, rec["orig"])


        def restore(serial):
            rec = st["tracked"].pop(serial, None)
            if rec is None:
                return
            try:                                         # plain try (2.6.82)
                it = API.FindItem(serial) or rec["item"]
            except Exception:
                it = rec["item"]
            if it is not None:
                set_hue(it, rec["orig"])


        def restore_all():
            for serial in list(st["tracked"]):
                restore(serial)
            for serial in list(st["fields"]):
                restore_field(serial)


        def pulse():
            """Hold green; flash red for PULSE_BEAT seconds once per cycle. A hue is
            only set when it changes (twice a cycle); nothing is read back here (the
            scan repaints a hue the server put back, see scan)."""
            if not st["tracked"]:
                return
            want_red = settings["pulse"] and (time.time() % max(0.5, settings["cycle"])
                                              < min(PULSE_BEAT, settings["cycle"] / 2.0))
            hue = settings["red"] if want_red else settings["green"]
            for rec in st["tracked"].values():
                if rec["set"] != hue:              # also a hue changed on the settings page
                    set_hue(rec["item"], hue)
                    rec["set"] = hue


        # ---------- trap pings (through Map Pings) ----------
        def ping_service():
            """Map Pings' send function, or None while Map Pings is off."""
            try:
                return HOST.services.get(PING_SERVICE)
            except Exception:
                return None


        def send_pings():
            n0 = len(st["ping_wait"])
            if n0:
                _send_one_ping()
                if len(st["ping_wait"]) != n0:
                    refresh()                            # "Sending N..." / "N pinged"


        def _send_one_ping():
            """One Danger! ping per tick at most, for the first trap still waiting.
            A trap is pinged once: its serial and its spot are remembered (a trap
            put back on the same tile with a new serial isn't pinged again). They
            go out PING_GAP apart, Map Pings' own pace (should it still answer
            False, too soon, the trap waits for the next tick).
            While Map Pings is off they wait, and go out once it is on, for the
            traps still in range."""
            wait = st["ping_wait"]
            if not wait:
                return
            svc = ping_service()
            if svc is None:
                if not st["ping_noted"]:
                    st["ping_noted"] = True
                    API.SysMsg("%s: turn World Map > Map Pings on to ping traps (they wait until then)."
                               % TITLE, Kit.HUE_INFO)
                return
            if time.time() < st["ping_next"]:                   # Map Pings' pace: not yet
                return
            tracked = st["tracked"]
            m = None
            while wait:
                serial = wait[0]
                rec = tracked.get(serial)
                if rec is None or serial in st["pinged"]:       # gone, or pinged already
                    wait.pop(0)
                    continue
                x, y = xy_of(rec["item"])
                if x <= 0 or y <= 0:                             # no place to ping
                    wait.pop(0)
                    continue
                if m is None:
                    try:
                        m = int(API.GetMap())
                    except Exception:
                        return
                spot = (m, x, y)
                if spot in st["pinged_spots"]:
                    mark_pinged(serial, None)
                    wait.pop(0)
                    continue
                try:
                    ok = svc(x, y, m, PING_KIND, PING_WHO)
                except Exception:
                    # a ping that fails outright isn't asked for again every tick
                    # (it may have been half shown already): this trap is done
                    mark_pinged(serial, spot)
                    wait.pop(0)
                    return
                if ok:
                    wait.pop(0)
                    mark_pinged(serial, spot)
                    st["ping_sent"] += 1
                    st["ping_next"] = time.time() + PING_GAP     # read after: Map Pings' clock is later
                return                                           # one per tick


        def mark_pinged(serial, spot):
            if len(st["pinged"]) >= PINGED_CAP:                  # a long session: start over
                st["pinged"].clear()
                st["pinged_spots"].clear()
            st["pinged"].add(serial)
            if spot is not None:
                st["pinged_spots"].add(spot)


        def ping_again():
            """The window's "Ping traps on screen": every trap in range gets its
            ping now, and each trap may be pinged once more when it is next found."""
            st["pinged"].clear()
            st["pinged_spots"].clear()
            st["ping_sent"] = 0
            st["ping_wait"] = list(st["tracked"])
            n = len(st["ping_wait"])
            if st["paused"]:
                msg = "paused: untick Pause highlighting on the World Map settings page to find and ping traps."
            elif n == 0:
                msg = "no traps in range to ping; each trap will be pinged when next found."
            elif ping_service() is None:
                msg = "%d trap%s to ping once World Map > Map Pings is on." % (n, "" if n == 1 else "s")
            else:
                msg = "pinging %d trap%s." % (n, "" if n == 1 else "s")
            API.SysMsg("%s: %s" % (TITLE, msg), Kit.HUE_INFO)
            st["ping_noted"] = False
            refresh()


        def ping_status():
            n = len(st["ping_wait"])
            if n and st["ping_svc"] is not None:         # also "Ping traps on screen" with auto-ping off
                return "sending %d" % n, Kit.HUE_INFO
            if not settings["ping"]:
                return "auto-ping off", Kit.HUE_INFO
            if st["ping_svc"] is None:
                return "World Map > Map Pings is off", Kit.HUE_BAD
            return "%d sent" % st["ping_sent"], Kit.HUE_GOOD


        # ---------- window ----------
        queue = Kit.queuer(st)
        on_disposed = Kit.disposer(KEY, st, win)
        SAY_TIP = ("Prints each new trap's graphic id and where it is, for checking and extending "
                   "the graphics list; untick to stop")
        PING_TIP = ("Send a Danger! map ping on every highlighted trap now, and let each be pinged "
                    "once more when next found (needs World Map > Map Pings on)")
        PING_CAP = "Ping traps on screen"


        def build_window():
            w, h = (MINI_W, MINI_H) if st["minimized"] else (W, H)
            x, y = Kit.load_pos(POS_KEY, (200, 200), (w, h))
            if Kit.is_open(win["g"]):
                x, y = win["g"].GetX(), win["g"].GetY()
            old, win["g"] = win["g"], None
            M = Kit.MARGIN
            store = ({}, {})
            c = {}
            g = G.CreateGump(True, True)
            if st["minimized"]:
                c["status"] = Kit.mini_bar(g, store, w, h, TITLE, KEY, queue("toggle_min"))
            else:
                # 2.6.51: one simple circle button; the status, Pause highlighting
                # and the graphic-id printing are on the settings page (STATUS, DEBUG)
                Kit.add_window_frame(g, w, h)
                Kit.title_bar(g, store, w, TITLE, KEY, queue("toggle_min"), queue("to_bar"),
                              queue("settings"))
                yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, w - 2 * M, h - yb - M)
                Kit.art_button(g, store, "ping", Kit.ART_CIRCLE, M + 12, yb + 12, PING_CAP,
                               PING_TIP, on_click=queue("ping_again"))
            Kit.place(g, x, y, w, h)                     # wholly on screen
            win.update({"g": g, "c": c, "store": store})
            G.AddControlOnDisposed(g, on_disposed(g))
            G.AddGump(g)
            safe(lambda: Kit.on_moved(g, save_pos))      # saved the moment you let go of it
            if st["minimized"] and st["docked"]:         # folded into the Action Bar
                safe(lambda: setattr(g, "IsVisible", False))
            refresh()
            save_view()
            Kit.dispose(old)


        def refresh():
            c = win["c"]
            n = len(st["tracked"])
            nf = len(st["fields"])
            if st["paused"]:
                text, hue = "Paused", Kit.HUE_INFO
            elif n == 0 and nf == 0:
                text, hue = "No traps in range", Kit.HUE_INFO
            elif nf == 0:
                text, hue = "Highlighting %d trap%s" % (n, "" if n == 1 else "s"), Kit.HUE_GOOD
            elif n == 0:
                text, hue = "Highlighting %d field%s" % (nf, "" if nf == 1 else "s"), Kit.HUE_GOOD
            else:
                text, hue = "Highlighting %d trap%s, %d field%s" % (
                    n, "" if n == 1 else "s", nf, "" if nf == 1 else "s"), Kit.HUE_GOOD
            if c.get("status") is not None:              # the minimized bar
                Kit.set_text(c["status"], Kit.fit("%s: %s" % (TITLE, journal_case(text)), MINI_W - 90),
                             hue)
            sc = page["c"]                               # the settings page's copy of the toggle
            if sc is not None and sc.get("say") is not None:
                try:
                    if bool(sc["say"].IsChecked) != bool(st["say_graphics"]):
                        sc["say"].SetIsChecked(bool(st["say_graphics"]))
                except Exception:
                    pass
            if sc is not None and sc.get("now") is not None:   # STATUS on the settings page (2.6.51)
                Kit.set_text(sc["now"], text, hue)
                ptext, phue = ping_status()
                Kit.set_text(sc["now_ping"], "Pings: " + ptext, phue)
                if st["pause_want"] is None:
                    try:
                        if bool(sc["paused"].IsChecked) != bool(st["paused"]):
                            sc["paused"].SetIsChecked(bool(st["paused"]))
                    except Exception:
                        pass


        # ---------- settings page ----------
        SEC0_H, SEC1_H, SEC2_H, SEC3_H, SEC4_H, SEC5_H = 84, 146, 96, 62, 118, 66
        PAUSE_TIP = ("Stops the scan and gives every trap and field its own hue back; untick to "
                     "highlight again")


        def with_tip(ctrl, text):
            safe(lambda: ctrl.SetTooltip(text))
            return ctrl


        def build_config(g, x, y, w):
            c = {}
            # STATUS (2.6.51): what the floating window showed, and its Pause / Resume
            Kit.add_section(g, x, y, w, SEC0_H, "STATUS  (the window has %s)" % PING_CAP)
            c["now"] = Kit.add_label(g, "", x + 12, y + 30, Kit.HUE_GOOD)
            c["now_ping"] = Kit.add_label(g, "", x + 12 + w // 2, y + 30, Kit.HUE_INFO)
            c["paused"] = Kit.add_check(g, "Pause highlighting (the hues are put back)", x + 12, y + 54,
                                        st["paused"], PAUSE_TIP)
            y = y + SEC0_H + Kit.GAP
            Kit.add_section(g, x, y, w, SEC1_H, "TRAPS  (hues are client hue numbers)")
            Kit.add_label(g, "Scan range:", x + 12, y + 36)
            c["range"] = with_tip(Kit.add_slider(g, x + 120, y + 34, 160, 1, 30, settings["range"]),
                                  "Tiles round you looked at for traps, once a second (1-30)")
            c["range_v"] = Kit.add_label(g, "%d tiles" % settings["range"], x + 290, y + 36,
                                         Kit.HUE_INFO)
            Kit.add_label(g, "Pulse cycle:", x + 12, y + 64)
            c["cycle"] = with_tip(Kit.add_slider(g, x + 120, y + 62, 160, 5, 100,
                                                 int(round(settings["cycle"] * 10))),
                                  "Seconds between red flashes (0.5-10)")
            c["cycle_v"] = Kit.add_label(g, "%.1f s" % settings["cycle"], x + 290, y + 64,
                                         Kit.HUE_INFO)
            Kit.add_label(g, "Green hue:", x + 12, y + 92)
            c["green"] = with_tip(Kit.add_textbox(g, str(settings["green"]), x + 120, y + 89, 60),
                                  "The hue traps are held at (client hue 1-%d; %d is the default "
                                  "green)" % (HUE_MAX, HUE_GREEN))
            Kit.add_label(g, "Red hue:", x + 200, y + 92)
            c["red"] = with_tip(Kit.add_textbox(g, str(settings["red"]), x + 280, y + 89, 60),
                                "The hue of the pulse (client hue 1-%d; %d is the default red)"
                                % (HUE_MAX, HUE_RED))
            c["pulse"] = Kit.add_check(g, "Pulse red once per cycle (unticked: steady green)",
                                       x + 12, y + 118, settings["pulse"],
                                       "Flashes every highlighted trap red for a beat once per cycle")
            y2 = y + SEC1_H + Kit.GAP
            Kit.add_section(g, x, y2, w, SEC2_H, "TRAP GRAPHICS  (hex ids, comma separated)")
            c["graphics"] = with_tip(Kit.add_textbox(g, graphics_text(), x + 12, y2 + 32, w - 28,
                                                     numbers=False),
                                     "Item graphics counted as traps, in hex (0x1103, 1103 and 0x11AC "
                                     "all do), separated by commas. Applied once you stop typing.")
            c["by_name"] = Kit.add_check(g, "Also highlight ground items the client names 'trap'",
                                         x + 12, y2 + 62, settings["by_name"],
                                         "Catches traps whose art id isn't in the list (the client "
                                         "knows a name only after a tooltip or a single click)")
            y3 = y2 + SEC2_H + Kit.GAP
            Kit.add_section(g, x, y3, w, SEC3_H, "TRAP PINGS  (needs World Map > Map Pings)")
            c["ping"] = Kit.add_check(g, "Send a Danger! map ping on each new trap, once per trap",
                                      x + 12, y3 + 32, settings["ping"],
                                      "A Danger! map ping on each new trap's tile, for you and your "
                                      "guildmates. Once per trap: \"%s\" on the window "
                                      "pings them all again." % PING_CAP)
            # magic fields (2.6.05)
            y4 = y3 + SEC3_H + Kit.GAP
            Kit.add_section(g, x, y4, w, SEC4_H, "MAGIC FIELDS  (client hue numbers, 0 = leave as is)")
            c["fields"] = Kit.add_check(g, "Highlight magic fields: fire, poison, energy, paralyze",
                                        x + 12, y4 + 32, settings["fields"],
                                        "Recolour field items on the ground (client-side only, like "
                                        "the traps); paralyze fields get a hue of their own")
            Kit.add_label(g, "Field hue:", x + 12, y4 + 64)
            c["field_hue"] = with_tip(Kit.add_textbox(g, str(settings["field_hue"]), x + 120, y4 + 61,
                                                      60),
                                      "The hue of fire, poison and energy fields (client hue 0-%d; "
                                      "0 leaves them as they are; %d by default)" % (HUE_MAX, FIELD_HUE))
            Kit.add_label(g, "Paralyze hue:", x + 200, y4 + 64)
            px_ = x + 212 + Kit.text_w("Paralyze hue:")
            c["para_hue"] = with_tip(Kit.add_textbox(g, str(settings["para_hue"]), px_, y4 + 61, 60),
                                     "The hue of paralyze fields, the ones that matter most in a "
                                     "fight (client hue 0-%d; 0 leaves them as they are; %d by "
                                     "default)" % (HUE_MAX, PARALYZE_HUE))
            c["field_say"] = Kit.add_check(g, "Show an overhead text when a field appears",
                                           x + 12, y4 + 90, settings["field_say"],
                                           "Names each new field above it once (\"Fire field\", "
                                           "\"Paralyze field!\")")
            y5 = y4 + SEC4_H + Kit.GAP
            atlas_section(g, x, y5, w, "traps")
            y6 = y5 + ATLAS_H + Kit.GAP
            Kit.add_section(g, x, y6, w, SEC5_H, "DEBUG  (for checking the shard's traps)")
            # the "print graphic ids" toggle (saved in VIEW_KEY, like the old window button's)
            c["say"] = Kit.add_check(g, "Print each new trap's graphic id in the journal",
                                     x + 12, y6 + 30, st["say_graphics"], SAY_TIP)
            page["c"] = c
            page["gfx_typed"], page["gfx_applied"] = None, graphics_text()
            page["fhues"] = (str(settings["field_hue"]), str(settings["para_hue"]))
            refresh()                                    # the STATUS labels


        def _slider_value(s, default):
            try:                                         # plain try, no lambdas (2.6.82)
                v = s.Value
            except Exception:
                v = None
            if v is None:
                try:
                    v = s.GetValue()
                except Exception:
                    v = default
            try:
                return int(v)
            except Exception:
                return default


        def poll_config():
            c = page["c"]
            if c is None:
                return
            changed = False
            rng = max(1, min(30, _slider_value(c["range"], settings["range"])))
            if rng != settings["range"]:
                settings["range"] = rng
                Kit.set_text(c["range_v"], "%d tiles" % rng)
                changed = True
            cyc = max(5, min(100, _slider_value(c["cycle"], int(settings["cycle"] * 10)))) / 10.0
            if abs(cyc - settings["cycle"]) > 0.01:
                settings["cycle"] = cyc
                Kit.set_text(c["cycle_v"], "%.1f s" % cyc)
                changed = True
            for key in ("green", "red"):
                try:
                    v = int(str(c[key].Text).strip())
                except Exception:
                    v = settings[key]
                if 1 <= v <= HUE_MAX and v != settings[key]:
                    settings[key] = v
                    changed = True
            for key in ("pulse", "by_name", "ping"):            # plain try: runs every poll
                try:
                    on = bool(c[key].IsChecked)
                except Exception:
                    on = settings[key]
                if on != settings[key]:
                    settings[key] = on
                    changed = True
                    if key == "ping" and not on:
                        st["ping_wait"] = []             # traps not yet pinged stay unpinged
                    elif key == "ping":                  # on again: the traps in range not yet pinged
                        st["ping_wait"] = [sr for sr in st["tracked"] if sr not in st["pinged"]]
            try:                                         # Paused (2.6.51): applied by the tick
                pz = bool(c["paused"].IsChecked)
            except Exception:
                pz = st["paused"] if st["pause_want"] is None else st["pause_want"]
            if pz != (st["paused"] if st["pause_want"] is None else st["pause_want"]):
                st["pause_want"] = pz
            try:
                say = bool(c["say"].IsChecked)
            except Exception:
                say = bool(st["say_graphics"])
            if say != st["say_graphics"]:
                st["say_graphics"] = say                 # the same flag as the window's button
                save_view()
                refresh()
            # the graphics list is applied once the text has stood unchanged for
            # FIELD_SETTLE (typing "0x11" on the way to "0x11AC" no longer saves and
            # highlights graphic 0x0011 mid-edit)
            try:
                typed = str(c["graphics"].Text or "")
            except Exception:
                typed = str(graphics_text() or "")
            now = time.time()
            if typed != page["gfx_typed"]:
                page["gfx_typed"], page["gfx_since"] = typed, now
            elif now - page["gfx_since"] >= FIELD_SETTLE and typed != page.get("gfx_applied"):
                page["gfx_applied"] = typed              # compared against the last applied text
                gl = parse_graphics(typed)
                if gl and gl != settings["graphics"]:
                    settings["graphics"] = gl
                    changed = True
            if changed:
                save_settings()
                st["last_scan"] = 0.0      # rescan with the new list / range at once
                refresh()
            if poll_fields(c):
                save_fields()
                st["last_scan"] = 0.0      # fields painted / put back with the new choice at once


        def poll_fields(c):
            """The magic-field settings (2.6.05); True when one changed. The hue
            boxes are parsed only when their text changed."""
            changed = False
            for key in ("fields", "field_say"):
                try:
                    on = bool(c[key].IsChecked)
                except Exception:
                    on = settings[key]
                if on != settings[key]:
                    settings[key] = on
                    changed = True
            try:
                texts = (str(c["field_hue"].Text).strip(), str(c["para_hue"].Text).strip())
            except Exception:
                return changed
            if texts != page.get("fhues"):
                page["fhues"] = texts
                for key, t in zip(("field_hue", "para_hue"), texts):
                    if t.isdigit() and 0 <= int(t) <= HUE_MAX and int(t) != settings[key]:
                        settings[key] = int(t)
                        changed = True
            return changed


        def config_closed():
            page["c"] = None
            page["gfx_typed"] = None


        # ---------- module hooks ----------
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "last_scan": 0.0,
                       "scans": 0, "tracked": {}, "pinged": set(), "pinged_spots": set(),
                       "ping_wait": [], "ping_sent": 0, "ping_noted": False,
                       "ping_svc": ping_service(), "ping_next": 0.0,
                       "fields": {}, "field_said": [], "alerted": set(),
                       "atlas_traps": [], "atlas_ver": 0, "atlas_done": -1, "atlas_map": None,
                       "pause_want": None})
            verdicts.clear()
            load_settings()
            load_fields()
            fn = getattr(HOST, "alert_kind", None)       # listed on Settings > Alerts
            if fn is not None:
                safe(lambda: fn(ALERT_TRAP, "New trap in range", ALERT_TRAP_SOUND))
            load_view()                                  # minimized / paused as you left them
            if HOST.dock_wanted(KEY):                    # folded into the Action Bar when you left
                st["minimized"] = True
            build_window()
            # folding into the Action Bar (the host's dock registry)
            HOST.dock_add(KEY, _dock_hooks(TITLE, TRAY_ICON, st, win, queue("redraw"), scale=True))


        def _tick():
            # Runs on the client thread (client_tick): nothing here waits, and the
            # scan's and the pulse's reads and recolours all run in place.
            if win["g"] is None:
                return
            if Kit.was_clicked(win["store"], "close"):
                Kit.dispose(win["g"])
                return
            want = st["pause_want"]                      # the settings page's Paused box (2.6.51)
            if want is not None:
                st["pause_want"] = None
                if want != st["paused"]:
                    st["paused"] = want
                    if want:
                        restore_all()
                        st["ping_wait"] = []             # found again (and queued) after Resume
                    else:
                        st["last_scan"] = 0.0
                    save_view()
                    refresh()
            while st["queue"]:
                action = st["queue"].pop(0)
                if action == "settings":
                    HOST.show_settings(KEY)
                elif action == "toggle_min":
                    st["minimized"] = not st["minimized"]
                    st["docked"] = False
                    HOST.dock_forget(KEY)                # its own minimized form, not the bar
                    build_window()
                elif action == "to_bar":
                    HOST.dock_to_bar(KEY, TITLE)         # folds in now, or once the bar is up
                elif action == "redraw":
                    build_window()
                elif action == "ping_again":
                    ping_again()
            if st["paused"]:
                return
            now = time.time()
            if now - st["last_scan"] >= SCAN_EVERY:
                st["last_scan"] = now
                before = (len(st["tracked"]), len(st["fields"]))
                scan()
                svc = ping_service()                     # Map Pings switched on / off
                if (len(st["tracked"]), len(st["fields"])) != before or \
                        (svc is None) != (st["ping_svc"] is None):
                    st["ping_svc"] = svc
                    if svc is not None:
                        st["ping_noted"] = False
                    refresh()
                if st["atlas_ver"] != st["atlas_done"]:   # on TazUO's World Map (2.6.51)
                    st["atlas_done"] = st["atlas_ver"]
                    atlas_publish()
            send_pings()
            pulse()


        def _stop():
            st["shutting"] = True
            HOST.dock_remove(KEY)
            restore_all()
            save_pos()
            save_settings()
            g, win["g"] = win["g"], None
            Kit.dispose(g)


        load_settings()
        load_fields()
        load_view()          # the settings page's DEBUG box saves the view string too
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True,
                "config_height": lambda w: SEC0_H + Kit.GAP + SEC1_H + Kit.GAP + SEC2_H + Kit.GAP +
                SEC3_H + Kit.GAP + SEC4_H + Kit.GAP + ATLAS_H + Kit.GAP + SEC5_H,
                "build_config": build_config,
                "poll_config": poll_config, "config_closed": config_closed}

    # ---------- the parts, run side by side by the mother's PartSet ----------
    #  (part key, builder, tick interval, the 2.6.06 module key it keeps)
    #  (the Corpse, Treasure Maps, Ore Tracker and Traps & Fields parts also
    #  have the Atlas's "TAZUO'S WORLD MAP" section on their settings page, 2.6.51)
    def _atlas_corpse():
        return with_atlas(_part_corpse(), "corpse")

    def _atlas_maps():
        return with_atlas(_part_maps(), "maps")

    def _atlas_dry():
        return with_atlas(_part_dry(), "dry")

    def _atlas_traps():
        return with_atlas(_part_traps(), "traps")

    PARTS = (
        ("pings", _part_pings, 0.05, "pings"),
        ("corpse", _atlas_corpse, 0.25, "corpserun"),
        ("maps", _atlas_maps, 0.2, "treasure"),
        ("dry", _atlas_dry, 0.2, "harvest"),
        ("traps", _atlas_traps, 0.1, "traphl"),
    )
    MODULE = PartSet(KEY, TITLE, PARTS).hooks()
    _parts_tick, _parts_stop = MODULE["tick"], MODULE["stop"]
    _parts_thread = MODULE.get("thread_tick")
    _parts_wanted = MODULE.get("thread_wanted")
    atlas_err = {"said": False}

    def _tick():
        _parts_tick()
        try:
            ATLAS.tick()                     # the parts' markers onto TazUO's World Map
        except Exception as ex:
            if not atlas_err["said"]:        # said once; the parts keep running
                atlas_err["said"] = True
                API.SysMsg("%s: couldn't update TazUO's World Map (%s)." % (TITLE, ex), Kit.HUE_BAD)

    def _stop():
        try:
            _parts_stop()
        finally:
            ATLAS.shutdown()                 # our markers come off TazUO's World Map

    def _thread():
        """Script thread: the parts' waiting work, then the Atlas's file strip
        (2.6.81: never on the client thread)."""
        if _parts_thread:
            _parts_thread()
        try:
            ATLAS.thread_work()
        except Exception:
            ATLAS.strip_pending = False

    def _thread_wanted():
        """(2.6.82) The parts' thread work, or the Atlas's file strip owed (the
        PartSet's own check knows nothing of the Atlas)."""
        if ATLAS.strip_pending or ATLAS.loose:
            return True
        return _parts_wanted() if _parts_wanted is not None else True

    MODULE["tick"], MODULE["stop"], MODULE["thread_tick"] = _tick, _stop, _thread
    MODULE["thread_wanted"] = _thread_wanted
    return MODULE


# ------------------------- registration with Virtue Assistant ----------------
if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("worldmap", "World Map",
             "Guild pings, your corpse, dig spots, dry spots and traps",
             _module_worldmap, 0.05,
             category="The world",
             parts=(
                 ("pings", "Map Pings",
                  "Send and receive guild pings on your Enhanced Map", False, ("pings",)),
                 ("corpse", "Corpse",
                  "An arrow to your corpse, its decay time, Get my things", False, ("corpserun",)),
                 ("maps", "Treasure Maps",
                  "The dig spots of your decoded treasure maps", False, ("treasure",)),
                 ("dry", "Ore Tracker",
                  "Your weight, and the ore, wood, fish and sand that ran dry", False, ("harvest",)),
                 ("traps", "Traps & Fields",
                  "Traps and magic fields recoloured so you see them", False, ("traphl",)),
             ),
             aliases=('Map Pings', 'Corpse Run', 'Treasure Hunter', 'Harvest Helper', 'Dry spots', 'Ore Tracker', 'Trap Highlight', 'Enhanced Map', 'tracking arrow', 'ping', 'corpse', 'dig spot', 'weight bar', 'TazUO World Map'))
else:
    import API
    API.SysMsg("World Map is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
