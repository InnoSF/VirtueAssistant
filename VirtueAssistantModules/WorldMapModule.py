def _module_worldmap():
    KEY = "worldmap"; TITLE = "World Map"; ATLAS_PREFIX = "VA "; ATLAS_PLACED_KEY = "WorldMap_atlas_placed"
    ATLAS_ON_KEY = "WorldMap_atlas"; ATLAS_ALIVE_KEY = "WorldMap_atlas_alive"; ATLAS_BEAT = 60.0; ATLAS_STALE = 180.0
    ATLAS_OWNERS = (("corpse", "your corpse"), ("maps", "your dig spots"),
                    ("dry", "the spots that ran dry"), ("traps", "the traps you have seen"))
    ATLAS_CHECK = 1.0; ATLAS_CLOSED_CHECK = 2.5; GUMP_EVERY = 0.5; ATLAS_SETTLE = 2.0; ATLAS_OPS = 3; ATLAS_CAP = 60
    GUMPS = {"at": -1.0, "ok": False, "map": False, "arrows": set()}
    def gump_flags(fresh=False):
        memo = GUMPS; now = time.time()
        if not fresh and 0.0 <= now - memo["at"] < GUMP_EVERY: return memo
        memo["at"] = now; mp = False; ar = set()
        try:
            for w in Tz.windows(("WorldMapGump", "QuestArrowGump")):
                if str(w.GetType().Name) == "WorldMapGump": mp = True
                else: ar.add(int(w.LocalSerial))
            memo["ok"] = True
        except Exception: memo["ok"] = False
        memo["map"], memo["arrows"] = mp, ar; return memo
    class Atlas(object):
        def __init__(self):
            self.items, self.on, self.placed, self.want, self.loose = {}, {}, {}, {}, set(); self.synced = True
            self.open_since = self.saved = None; self.next_check = self.retry_at = 0.0
            self.loaded = self.strip_pending = self.dirty = False; self.me = self.tag = ""; self.legacy = set()
            self.owners, self.foreign, self.beat_at = set(), set(), 0.0
        def load(self):
            if self.loaded: return
            self.loaded = True
            for k, v in Kit.codec_load(Kit.get_var(ATLAS_ON_KEY)).items(): self.on[k] = v != "0"
            try: self.me = "%d" % int(API.Player.Serial); self.tag = " %04X" % (int(self.me) & 0xFFFF)
            except Exception: self.me = self.tag = ""
            text = str(API.GetPersistentVar(ATLAS_PLACED_KEY, "", API.PersistentVar.Global) or "")
            beats = self.beats(); now = time.time(); self.owners = set([self.me])
            for line in text.split("\n"):
                p = line.split("|")
                if len(p) == 6 and not abs(now - beats.get(p[5], 0.0)) < ATLAS_STALE: self.owners.add(p[5])
            for line in text.split("\n"):
                p = line.split("|")
                if self.own(p):
                    if len(p) == 5: self.legacy.add(p[0])
                    try: self.placed[p[0]] = (int(p[1]), int(p[2]), int(p[3]), p[4])
                    except ValueError: pass
            self.note_foreign(text); self.saved = text; self.dirty = len(self.owners) > 1 or bool(self.legacy)
            self.strip_pending = bool(self.placed) and not self.map_open(True); self._rebuild()
        def own(self, p, legacy=None):
            if not p[0].startswith(ATLAS_PREFIX): return False
            if len(p) == 6: return p[5] in self.owners
            return len(p) == 5 and (legacy is None or p[0] in legacy)
        def note_foreign(self, text):
            self.foreign = set(ln.split("|")[0] for ln in text.split("\n")
                               if ln.startswith(ATLAS_PREFIX) and not self.own(ln.split("|"), self.legacy))
        def beats(self):
            out = {}
            for part in str(API.GetPersistentVar(ATLAS_ALIVE_KEY, "", API.PersistentVar.Global) or "").split(";"):
                k, _s, v = part.partition("=")
                try: out[k] = float(v)
                except ValueError: pass
            return out
        def beat_due(self):
            now = time.time(); return bool(self.placed) and (now >= self.beat_at or self.beat_at - now > ATLAS_BEAT)
        def beat(self):
            now = time.time(); self.beat_at = now + ATLAS_BEAT
            try: beats = self.beats()
            except Exception: return
            beats[self.me] = now
            text = ";".join("%s=%d" % (k, v) for k, v in sorted(beats.items()) if k and abs(now - v) < 86400)
            safe(lambda: API.SavePersistentVar(ATLAS_ALIVE_KEY, text, API.PersistentVar.Global))
        def is_on(self, owner): self.load(); return self.on.get(owner, True)
        def set_on(self, owner, on):
            self.load()
            if self.on.get(owner, True) != bool(on):
                self.on[owner] = bool(on)
                Kit.put_var(ATLAS_ON_KEY, ";".join(
                    "%s=%d" % (k, 1 if self.on.get(k, True) else 0) for k, _w in ATLAS_OWNERS))
                self._rebuild()
        def set(self, owner, items):
            self.load()
            if self.items.get(owner) != items: self.items[owner] = dict(items); self._rebuild()
        def clear(self, owner):
            if self.items.pop(owner, None): self._rebuild()
        def _rebuild(self):
            want = {}
            for owner, _w in ATLAS_OWNERS:
                if self.on.get(owner, True):
                    for name, v in self.items.get(owner, {}).items():
                        if len(want) >= ATLAS_CAP: break
                        want[name] = v
            self.want = want; self.synced = want == self.placed
        def map_open(self, fresh=False): f = gump_flags(fresh); return f["ok"] and f["map"]
        def tick(self):
            if self.synced or self.strip_pending: return
            now = time.time()
            if now < self.next_check and self.next_check - now <= ATLAS_SETTLE + ATLAS_CHECK: return
            if not self.map_open(): self.open_since = None; self.next_check = now + ATLAS_CLOSED_CHECK; return
            if self.open_since is None or self.open_since > now: self.open_since = now
            if now - self.open_since < ATLAS_SETTLE: self.next_check = self.open_since + ATLAS_SETTLE; return
            if not self.map_open(True): self.open_since = None; self.next_check = now + ATLAS_CLOSED_CHECK; return
            self.next_check = now + 0.25; ops = 0
            for name in list(self.placed):
                if ops >= ATLAS_OPS: break
                if self.want.get(name) != self.placed[name]:
                    if name not in self.foreign: API.RemoveMapMarker(name)
                    self._drop(name); ops += 1
            for name, v in self.want.items():
                if ops >= ATLAS_OPS: break
                if name not in self.placed:
                    API.AddMapMarker(name, v[0], v[1], v[2], v[3]); self._put(name, v); ops += 1
            self.synced = self.want == self.placed
        def loose_due(self): return bool(self.loose) and time.time() >= self.retry_at
        def thread_work(self):
            self._save(); loose = set(self.loose) if self.loose_due() else set()
            if self.beat_due(): self.beat()
            if not self.strip_pending and not loose: return
            is_open = Kit.on_client(lambda: self.map_open(True))
            if self.strip_pending:
                if not is_open and self._strip_file(set(self.placed) - self.foreign): self._drop_all(); self._save()
                self.strip_pending = False; self.synced = self.want == self.placed
            if loose:
                if is_open:
                    for name in loose: API.RemoveMapMarker(name)
                elif not self._strip_file(loose): self.retry_at = time.time() + 10.0; return
                self.loose.difference_update(loose)
        def _put(self, name, v): self.placed[name] = v; self.dirty = True
        def _drop(self, name): self.placed.pop(name, None); self.dirty = True
        def _drop_all(self):
            for name in list(self.placed): self._drop(name)
        def _save(self):
            if not self.dirty: return
            try: raw = str(API.GetPersistentVar(ATLAS_PLACED_KEY, "", API.PersistentVar.Global) or "")
            except Exception: return
            self.dirty = False; self.note_foreign(raw)
            keep = [ln for ln in raw.split("\n") if ln.strip() and not self.own(ln.split("|"), self.legacy)]
            text = "\n".join(keep + ["%s|%d|%d|%d|%s|%s" % (n, v[0], v[1], v[2], v[3], self.me)
                                     for n, v in sorted(dict(self.placed).items())])
            if text != raw or text != self.saved:
                try: API.SavePersistentVar(ATLAS_PLACED_KEY, text, API.PersistentVar.Global)
                except Exception: self.dirty = True; return
                self.saved = text
            self.owners, self.legacy = set([self.me]), set()
        def shutdown(self):
            self.items.clear(); self.want = {}; self.strip_pending = False
            if not self.placed and not self.loose: self.synced = True; self._save(); return
            gone = (set(self.placed) - self.foreign) | self.loose
            if self.map_open(True):
                for name in gone: API.RemoveMapMarker(name)
                self._drop_all()
            elif self._strip_file(gone): self._drop_all()
            self.loose.clear(); self.synced = not self.placed; self._save()
        def _strip_file(self, gone):
            try:
                exe = str(Tz.get(None, "ExecutablePath", Tz.T("ClassicUO.CUOEnviroment")))
                folder = os.path.join(exe, "Data", "Client")
                if not os.path.isdir(folder): return False
                path = os.path.join(folder, "userMarkers.usr")
                if not os.path.exists(path): return True
                import io
                with io.open(path, "r", encoding="utf-8-sig") as f: lines = f.read().splitlines()
                keep = [ln for ln in lines if len(ln.split(",")) < 4 or ln.split(",")[3] not in gone]
                if len(keep) != len(lines): Kit.write_safe(path, u"".join(l + u"\n" for l in keep))
                return True
            except Exception: return False
    ATLAS = Atlas()
    def atlas_name(text): ATLAS.load(); return ATLAS_PREFIX + str(text).replace(",", " ") + ATLAS.tag
    def arrow_open(ident, fresh=False): f = gump_flags(fresh); return ident in f["arrows"] if f["ok"] else True
    ATLAS_BOX = {}
    def atlas_page(owner):
        def draw(f, x, y):
            ATLAS_BOX[owner] = Kit.add_check(f.g, "Show %s on TazUO's World Map" % dict(ATLAS_OWNERS).get(owner, owner),
                                             x + 12, y, ATLAS.is_on(owner), "Markers named \"%s...\" while the map is "
                                             "open; removed when unticked or the part stops" % ATLAS_PREFIX)
        return "TAZUO'S WORLD MAP  (while open)", (("custom", 26, draw),), {"sh": 66}
    def with_atlas(api, owner):
        old_poll, old_closed, old_stop = api["poll_config"], api["config_closed"], api["stop"]
        def poll():
            old_poll(); cb = ATLAS_BOX.get(owner)
            if cb is not None:
                try: on = bool(cb.IsChecked)
                except Exception: return
                if on != ATLAS.is_on(owner): ATLAS.set_on(owner, on)
        def closed(): old_closed(); ATLAS_BOX.pop(owner, None)
        def stop():
            try: old_stop()
            finally: ATLAS_BOX.pop(owner, None); ATLAS.clear(owner)
        out = dict(api); out.update({"poll_config": poll, "config_closed": closed, "stop": stop}); return out
    atlas_err = {"said": False}
    def atlas_tick():
        try: ATLAS.load(); ATLAS.tick()
        except Exception as ex:
            if not atlas_err["said"]:
                atlas_err["said"] = True
                API.SysMsg("%s: couldn't update TazUO's World Map (%s)." % (TITLE, ex), Kit.HUE_BAD)
    def atlas_thread():
        try: ATLAS.thread_work()
        except Exception: ATLAS.strip_pending = False
    SHARED = {"tick": atlas_tick, "stop": ATLAS.shutdown, "thread_tick": atlas_thread,
              "thread_wanted": lambda: ATLAS.strip_pending or ATLAS.dirty or ATLAS.loose_due() or ATLAS.beat_due()}
    JOURNAL_NAMES = ("TazUO", "World Map", "Map Pings", "Enhanced Map", "Virtue Assistant",
                     "Settings", "Inventory", "Need help", "Look here", "Go here", "Danger!")
    def journal_case(text):
        text = str(text or "")
        if not text or text[0] in "[(\"'" or text.startswith(JOURNAL_NAMES): return text
        return text[0].lower() + text[1:]
    def xy(x, y, fmt="%d, %d"): return Kit.veil("xy", fmt % (x, y))
    def contents(serial, cap):
        out, bags = [], [int(serial)]
        while bags and len(out) < cap:
            for it in API.ItemsInContainer(bags.pop(), False) or ():
                out.append(it)
                if it.IsContainer: bags.append(int(it.Serial))
        return out[:cap]
    def list_h(rows, row_h): return 2 * Kit.MARGIN + 30 + 2 * Kit.GAP + 36 + 30 + rows * row_h + 8
    def told(wnd, st, mw, mh):
        z = wnd.slot
        if z is None or st["minimized"] or not HOST.layout_holds(wnd.key) or z[0] < mw or z[1] < mh: return None
        return z
    def _part_pings():
        KEY = "pings"; TITLE = "Map Pings"; DEFAULT_PORT = 8887
        HOTKEYS = {"look": "CTRL+1", "danger": "CTRL+2", "go": "CTRL+3", "help": "CTRL+4",}
        HOTKEY_ORDER = ("look", "danger", "go", "help"); MARKERS_CAP = 60; PING_RATE_SECS = 0.75; SEND_TIMEOUT = 5
        PING_SOUNDS = (0x1EA, 0x307, 0x1FC, 0x202); HISTORY_MAX = 200; HISTORY_ROWS = 10
        socket = select = _HAVE_PY_SOCKET = None
        def net():
            nonlocal socket, select, _HAVE_PY_SOCKET
            if _HAVE_PY_SOCKET is None:
                try: import _socket as so; import select as se; socket, select, _HAVE_PY_SOCKET = so, se, True
                except Exception: _HAVE_PY_SOCKET = False
            return _HAVE_PY_SOCKET
        import collections; VAR_PREFIX = "EMPings."; OPT_KEY = VAR_PREFIX + "options"
        LOOK, DANGER, GO, HELP = 0, 1, 2, 3
        CONNECTIONS = [("auto", "TazUO's map if on, else my login"), ("tazuo", "Only TazUO's Enhanced Map"),
                       ("own", "Only my own login")]
        CONN_CODES = [c[0] for c in CONNECTIONS]; OPT_LIMITS = {"ping_secs": (2, 60), "drag": (5, 200)}
        settings = {"sounds": True, "share": True, "gesture": True, "connection": "auto", "ping_secs": 8, "drag": 25}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "app": None}
        win = {"g": None, "c": {}, "store": ({}, {})}; cleanup, queue, say = Kit.basics(st, TITLE)
        def load_settings():
            for k, v in Kit.codec_load(Kit.get_var(OPT_KEY)).items():
                if k in ("sounds", "share", "gesture"): settings[k] = v == "1"
                elif k == "connection" and v in CONN_CODES: settings[k] = v
                elif k in OPT_LIMITS:
                    try: lo, hi = OPT_LIMITS[k]; settings[k] = max(lo, min(hi, int(v)))
                    except ValueError: pass
                elif k.startswith("hk_") and k[3:] in HOTKEYS: HOTKEYS[k[3:]] = _norm_key(v)
        def save_settings():
            data = "sounds=%d;share=%d;gesture=%d;connection=%s" % (
                settings["sounds"], settings["share"], settings["gesture"], settings["connection"])
            data += "".join(";hk_%s=%s" % (k, HOTKEYS[k].replace(";", "")) for k in HOTKEY_ORDER)
            data += ";ping_secs=%d;drag=%d" % (int(settings["ping_secs"]), int(settings["drag"]))
            Kit.put_var(OPT_KEY, data)
        def build_window(): pass
        wnd = None
        def refresh(): pass
        ACTIONS = {}; TYPE_KEYS = {"look": LOOK, "danger": DANGER, "go": GO, "help": HELP}
        GESTURE = {"up": LOOK, "right": DANGER, "down": GO, "left": HELP}
        TYPE_INFO = {LOOK:   ("Look here", 53,     0x373A,     "yellow"),
            DANGER: ("Danger!",   33,     0x3709,     "red"), GO:     ("Go here",   68,     0x376A,     "green"),
            HELP:   ("Need help", 88,     0x375A,     "blue"),}
        ARROW_ID = 0x50494E47
        def label_of(t): return TYPE_INFO[t][0]
        def facet_name(m): return Kit.FACETS[m] if 0 <= m < len(Kit.FACETS) else "map %d" % m
        def packet(pid, payload=b""): return struct.pack("<BH", pid, 3 + len(payload)) + payload
        def pk_login(user, password):
            u, p = user.encode("latin-1", "replace"), password.encode("latin-1", "replace")
            return packet(0x1F, struct.pack("<BB", len(u), len(p)) + u + p)
        def pk_alert(x, y): return packet(0x27, struct.pack("<HH", x & 0xFFFF, y & 0xFFFF))
        TYPED_ALERT_FLAG = 0x8000
        def decode_typed_alert(ax, ay):
            if not (ax & TYPED_ALERT_FLAG and ay & TYPED_ALERT_FLAG): return None
            return ax & 0x1FFF, ay & 0x0FFF, (ay >> 12) & 0x7, (ax >> 13) & 0x3
        def pk_typed_alert(x, y, m, t):
            if 0 <= x < 0x2000 and 0 <= y < 0x1000 and 0 <= m < 8 and 0 <= t < 4:
                return pk_alert(TYPED_ALERT_FLAG | (t << 13) | x, TYPED_ALERT_FLAG | (m << 12) | y)
        def pk_player_data(pos, stats, flag, color):
            return packet(0x25, struct.pack("<HHB6HBBBIB", pos[0] & 0xFFFF, pos[1] & 0xFFFF, pos[2] & 0xFF,
                          *([max(0, min(v, 0xFFFF)) for v in stats] + [flag, 0, 0, color & 0xFFFFFFFF, 5]))
                          + b"Arial" + struct.pack("<fB", 12.0, 1))
        class Reader(object):
            def __init__(self, data, offset=3): self.d, self.p = data, offset
            def take(self, n):
                if self.p + n > len(self.d): raise ValueError("short packet")
                self.p += n; return self.d[self.p - n:self.p]
            def u8(self): return bytearray(self.take(1))[0]
            def u16(self): return struct.unpack("<H", self.take(2))[0]
            def ascii(self, n): return bytes(self.take(n)).decode("latin-1")
        class PySocketTransport(object):
            def __init__(self, host, port, timeout):
                err = None
                for af, kind, proto, _, addr in socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM):
                    s = None
                    try: s = socket.socket(af, kind, proto); s.settimeout(timeout); s.connect(addr); break
                    except OSError as ex:
                        err = ex
                        if s is not None: s.close()
                else: raise err if err is not None else OSError("getaddrinfo returns an empty list")
                self.s = s; s.settimeout(SEND_TIMEOUT)
            def send(self, data): self.s.sendall(data)
            def recv(self):
                r, _, _ = select.select([self.s], [], [], 0)
                if not r: return b""
                data = self.s.recv(8192)
                if not data: raise EOFError()
                return data
            def close(self): safe(lambda: self.s.close())
        class DotNetTransport(object):
            def __init__(self, host, port, timeout):
                import clr; from System.Net.Sockets import TcpClient, SelectMode
                self._select_read = SelectMode.SelectRead; from System import Array, Byte
                self._Array, self._Byte = Array, Byte; self.c = TcpClient(); task = self.c.ConnectAsync(host, port)
                if not task.Wait(int(timeout * 1000)) or not self.c.Connected:
                    self.c.Close(); raise IOError("timed out")
                self.st = self.c.GetStream(); self.st.WriteTimeout = int(SEND_TIMEOUT * 1000)
            def send(self, data): buf = self._Array[self._Byte](bytearray(data)); self.st.Write(buf, 0, len(buf))
            def recv(self):
                if not self.c.Connected: raise EOFError()
                n = self.c.Available
                if n <= 0:
                    if self.c.Client.Poll(0, self._select_read): raise EOFError()
                    return b""
                buf = self._Array.CreateInstance(self._Byte, n); got = self.st.Read(buf, 0, n)
                if got <= 0: raise EOFError()
                return bytes(bytearray(buf)[:got])
            def close(self): safe(lambda: self.c.Close())
        def open_transport(host, port, timeout=5):
            if net():
                try: return PySocketTransport(host, port, timeout)
                except (socket.timeout, socket.gaierror, ConnectionError, OSError): raise
                except Exception: pass
            return DotNetTransport(host, port, timeout)
        class Sender(object):
            def __init__(self, transport):
                self.t = transport; self.error = self.wake = None; self.stopped = False; self.q = collections.deque()
                try:
                    import _thread; self.wake = _thread.allocate_lock(); self.wake.acquire()
                    _thread.start_new_thread(self._run, ())
                except Exception: self.wake = None
            def send(self, data):
                if self.error is not None or self.stopped: raise self.error or IOError("sender stopped")
                if self.wake is None: self.t.send(data); return
                self.q.append(data); self.poke()
            def poke(self):
                with Kit.quiet: self.wake.release()
            def _run(self):
                while not self.stopped:
                    if not self.q: self.wake.acquire(True, 0.5); continue
                    try: data = self.q.popleft()
                    except IndexError: continue
                    try: self.t.send(data)
                    except Exception as ex: self.error = ex; return
            def stop(self):
                self.stopped = True
                if self.wake is not None: self.q.clear(); self.poke()
        class MapConnection(object):
            kind = "own"; owns_position = True; server_relays_ping = True; OFF, HANDSHAKE, LOGIN, READY = range(4)
            def __init__(self, host, port, user, password):
                self.host, self.port, self.user, self.password = host, port, user, password
                self.t = self.gave_up = self.connecting = self.sender = None; self.state = self.OFF
                self.buf = bytearray()
                self.next_try = self.login_failures = self.last_sent = self.state_since = self.ready_since = 0
                self.backoff = 3; self.kicks = []; self.name = user; self.unreachable_reported = False
            def close(self):
                if self.connecting is not None:
                    pend, self.connecting = self.connecting, None
                    with pend["lock"]: pend["abandon"] = True; done = pend["done"]
                    if done and pend["t"] is not None: pend["t"].close()
                if self.sender is not None: self.sender.stop(); self.sender = None
                if self.t: self.t.close()
                self.t = None; self.state = self.OFF; self.buf = bytearray()
            def _drop(self, events, kind, detail, retry_in):
                was = self.state; self.close(); now = time.time()
                if was == self.LOGIN and kind == "eof":
                    self.login_failures += 1
                    if self.login_failures >= 3:
                        self.gave_up = "Login refused 3 times; check the map username and password."
                        events.append(("status", self.gave_up, True)); return
                    events.append(("status", "Login refused (wrong username or password?); retrying in %d s."
                                   % retry_in, True))
                elif was == self.LOGIN:
                    events.append(("status", "Login problem (%s); retrying in %d s." % (detail, retry_in), True))
                elif was == self.READY:
                    if kind == "eof" and now - self.ready_since < 6:
                        why = "Dropped right after login (is this map account logged in elsewhere, Enhanced Map?)"
                    elif kind == "eof": why = "Lost the map server"
                    else: why = "Connection problem (%s)" % detail
                    self.kicks = [k for k in self.kicks if now - k < 300] + [now]
                    if len(self.kicks) >= 4:
                        self.gave_up = ("Kept getting dropped (is this map account logged in elsewhere, Enhanced "
                                        "Map?); use a separate account, then click Reconnect.")
                        events.append(("status", self.gave_up, True)); return
                    events.append(("status", "%s; reconnecting in %d s." % (why, retry_in), True))
                else:
                    what = {"eof": "Server closed the connection",
                            "timeout": "Server didn't answer"}.get(kind, "Connection problem")
                    events.append(("status", "%s (%s); retrying in %d s."
                                   % (what, detail or "handshake", retry_in), False))
                self.next_try = now + retry_in
            def reset(self):
                self.close(); self.gave_up = None; self.login_failures = self.next_try = 0; self.kicks = []
                self.backoff = 3
            @property
            def ready(self): return self.state == self.READY
            def send(self, data):
                if not self.t: return
                try:
                    if self.sender is not None: self.sender.send(data)
                    else: self.t.send(data)
                    self.last_sent = time.time()
                except Exception: self.close(); self.next_try = time.time() + 3
            def poll(self):
                events = []; now = time.time()
                if self.gave_up: return events
                if self.t is None:
                    if now < self.next_try: return events
                    pend = self.connecting
                    if pend is None:
                        import _thread; net()
                        pend = self.connecting = {"done": False, "t": None, "err": None, "abandon": False,
                                                  "lock": _thread.allocate_lock()}
                        def run(p=pend, host=self.host, port=self.port):
                            try: p["t"] = open_transport(host, port)
                            except Exception as ex: p["err"] = ex
                            with p["lock"]: p["done"] = True; gone = p["abandon"]
                            if gone and p["t"] is not None: p["t"].close()
                        try: _thread.start_new_thread(run, ())
                        except Exception: run()
                    if not pend["done"]: return events
                    self.connecting = None; now = time.time()
                    try:
                        if pend["err"] is not None: raise pend["err"]
                        if pend["t"] is None: raise IOError("no connection")
                        self.t = pend["t"]
                    except Exception as e:
                        self.backoff = min(self.backoff * 2, 60)
                        events.append(("status", "Can't reach the map server at %s:%d (%s); retrying in %d s."
                                       % (self.host, self.port, short_error(e), self.backoff),
                                       not self.unreachable_reported))
                        self.unreachable_reported = True; self.next_try = now + self.backoff; return events
                    self.state = self.HANDSHAKE; self.state_since = now; self.buf = bytearray()
                    self.sender = Sender(self.t)
                    self.send(packet(0x2B, b"\x00")); events.append(("status", "Connecting", False))
                closed = None; snd = self.sender
                if snd is not None and snd.error is not None:
                    e = snd.error; closed = ("error", "%s: %s" % (e.__class__.__name__, short_error(e)))
                try:
                    chunk = self.t.recv() if self.t else b""
                    if chunk:
                        self.buf.extend(chunk)
                        if len(self.buf) > 1 << 20: raise IOError("too much data")
                except EOFError: closed = ("eof", "")
                except Exception as e: closed = ("error", "%s: %s" % (e.__class__.__name__, short_error(e)))
                while len(self.buf) >= 3 and self.t is not None:
                    pid = self.buf[0]; size = self.buf[1] | (self.buf[2] << 8)
                    if size < 3: self._drop(events, "garbled", "bad packet size", 10); return events
                    if len(self.buf) < size: break
                    data = bytes(self.buf[:size]); del self.buf[:size]
                    try: self._handle(pid, data, events)
                    except ValueError: pass
                if closed and self.t is not None:
                    self._drop(events, closed[0], closed[1], 30 if self.state == self.LOGIN else 10); return events
                if (self.t is not None and self.state in (self.HANDSHAKE, self.LOGIN) and now - self.state_since > 15):
                    self._drop(events, "timeout", "no reply in 15 s", 15)
                return events
            def _handle(self, pid, data, events):
                r = Reader(data)
                if pid == 0x2B and self.state == self.HANDSHAKE:
                    self.state = self.LOGIN; self.state_since = time.time()
                    self.send(pk_login(self.user, self.password))
                elif pid == 0x1F and self.state == self.LOGIN:
                    if r.u8() == 1:
                        again = bool(self.login_failures or self.kicks or self.unreachable_reported)
                        r.u8(); self.name = r.ascii(r.u8()) or self.user; self.state = self.READY
                        self.ready_since = time.time(); self.login_failures = 0; self.backoff = 3
                        self.unreachable_reported = False
                        events.append(("status", "Connected." if Kit.streamer else "Connected as %s." % self.name,
                                       again))
                    else: self._drop(events, "eof", "login rejected", 30)
                elif pid in (0x33, 0x27) and self.state == self.READY: events.append(parse_ping(pid, r))
                elif pid == 0x2F and self.state == self.READY: events.append(("message", r.ascii(r.u16())))
        def parse_ping(pid, r):
            if pid == 0x33:
                x, y, m, t = r.u16(), r.u16(), r.u8(), r.u8()
                return ("ping", r.ascii(r.u8()), x, y, m, t if t in TYPE_INFO else LOOK)
            x, y = r.u16(), r.u16(); return ("alert", r.ascii(r.u8()), x, y)
        class TazUOBridge(object):
            HOOK_KEY = "EMPings.OnFrameHook"
            def __init__(self):
                import clr; clr.AddReference("System.Collections.Concurrent")
                from System import Array, Byte, Action, Delegate, AppDomain
                from System.Reflection import BindingFlags; from System.Collections.Concurrent import ConcurrentQueue
                self._Array, self._Byte, self._Delegate, self._AppDomain = (Array, Byte, Delegate, AppDomain)
                inst = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance
                stat = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static
                mtype = API.GetType().Assembly.GetType("ClassicUO.Game.Managers.EnhancedMap.EnhancedMapManager")
                p_instance = mtype.GetProperty("Instance", stat)
                self._p_connected = mtype.GetProperty("IsConnected", inst)
                self._p_config = mtype.GetProperty("Config", stat)
                self._m_reconnect = mtype.GetMethod("Reconnect", inst); f_client = mtype.GetField("_client", inst)
                self._asm = API.GetType().Assembly; self._manager = p_instance.GetValue(None)
                self._client = f_client.GetValue(self._manager); ctype = self._client.GetType()
                self._f_connection = ctype.GetField("_connection", inst)
                self._m_send = ctype.GetMethod("SendRaw", inst); self._f_onframe = ctype.GetField("OnFrame", inst)
                try: self._handler, self._queue = self._make_handler()
                except Exception:
                    self._queue = ConcurrentQueue[object](); fq = self._queue
                    def on_frame(pid, payload):
                        try:
                            if pid in (0x33, 0x27) and fq.Count < 200: fq.Enqueue((int(pid), payload))
                        except Exception: pass
                    self._handler = Action[Byte, Array[Byte]](on_frame)
                self._hooked = False
            @staticmethod
            def _make_handler():
                import clr; clr.AddReference("System.Collections.Concurrent")
                clr.AddReference("System.Linq.Expressions"); from System import Array, Byte, Int32, Action, Tuple, Type
                from System.Collections.Concurrent import ConcurrentQueue
                from System.Linq.Expressions import Expression, ParameterExpression
                t_byte, t_bytes, t_int = (clr.GetClrType(Byte), clr.GetClrType(Array[Byte]), clr.GetClrType(Int32))
                ftype = Tuple[Byte, Array[Byte]]; fq = ConcurrentQueue[ftype]()
                p_id = Expression.Parameter(t_byte, "id"); p_payload = Expression.Parameter(t_bytes, "payload")
                q = Expression.Constant(fq); as_int = Expression.Convert(p_id, t_int)
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
                if self._hooked: return
                domain = self._AppDomain.CurrentDomain; current = self._f_onframe.GetValue(self._client)
                leftover = domain.GetData(self.HOOK_KEY)
                if leftover is not None: current = self._Delegate.Remove(current, leftover)
                current = self._own_handlers_only(current)
                self._f_onframe.SetValue(self._client, self._Delegate.Combine(current, self._handler))
                domain.SetData(self.HOOK_KEY, self._handler); self._hooked = True
            def _own_handlers_only(self, current):
                if current is None: return None
                try:
                    keep = None
                    for d in current.GetInvocationList():
                        if ((d.Target is not None and d.Target.Equals(self._manager)) or self._tazuo_code(d)):
                            keep = self._Delegate.Combine(keep, d)
                    return keep
                except Exception: return current
            def _tazuo_code(self, d):
                try: return bool(d.Method.Module.Assembly.Equals(self._asm))
                except Exception: return False
            def unhook(self):
                if not self._hooked: return
                try:
                    current = self._f_onframe.GetValue(self._client)
                    self._f_onframe.SetValue(self._client, self._Delegate.Remove(current, self._handler))
                    self._AppDomain.CurrentDomain.SetData(self.HOOK_KEY, None)
                finally: self._hooked = False
            def config(self):
                c = self._p_config.GetValue(None)
                if c is None: return None
                return {"enabled": bool(c.Enabled), "configured": bool(c.IsConfigured), "user": str(c.Username or ""),
                        "address": str(c.Address or ""), "port": int(c.Port), "send_location": bool(c.SendLocation)}
            def is_connected(self): return bool(self._p_connected.GetValue(self._manager))
            def send(self, data):
                conn = self._f_connection.GetValue(self._client)
                if conn is None: return
                buf = self._Array[self._Byte]([int(b) for b in bytearray(data)])
                self._m_send.Invoke(self._client, self._Array[object]([conn, buf]))
            def reconnect(self): self._m_reconnect.Invoke(self._manager, None)
            def frames(self):
                out = []
                for _ in range(200):
                    ok, item = self._queue.TryDequeue()
                    if not ok: break
                    if isinstance(item, tuple): pid, payload = item
                    else: pid, payload = item.Item1, item.Item2
                    out.append((int(pid), bytes(bytearray([int(b) for b in payload]))))
                return out
        class TazUOMouse(object):
            def __init__(self):
                import clr; from System.Reflection import BindingFlags
                stat = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static; asm = API.GetType().Assembly
                mouse = asm.GetType("ClassicUO.Input.Mouse"); selected = asm.GetType("ClassicUO.Game.SelectedObject")
                ui = asm.GetType("ClassicUO.Game.Managers.UIManager")
                self._pos = mouse.GetField("Position", stat); self._mclick = mouse.GetField("MClickPosition", stat)
                self._mdown = mouse.GetProperty("MButtonPressed", stat); self._mdown_get = None
                self._over_world = ui.GetProperty("IsMouseOverWorld", stat)
                self._object = selected.GetField("Object", stat)
            def middle_down(self):
                get = self._mdown_get
                if get is None: get = self._mdown_get = self._mdown.GetValue
                return bool(get(None))
            def position(self, f=None): p = (self._pos if f is None else f).GetValue(None); return int(p.X), int(p.Y)
            def tile_under_mouse(self):
                if not bool(self._over_world.GetValue(None)): return None
                obj = self._object.GetValue(None)
                if obj is None: return None
                fx, fy = xy_fields(obj.GetType())
                if fx is None or fy is None: return None
                x, y = int(fx.GetValue(obj)), int(fy.GetValue(obj)); return (x, y) if x > 0 and y > 0 else None
        class TazUOLink(object):
            kind = "tazuo"; owns_position = False; DROP_WINDOW = 120; DROP_LIMIT = 3
            def __init__(self, bridge):
                self.bridge = bridge; self.bridge.hook(); self.was_connected = None; self.drops = []
                self.unhooked_for_drops = self.server_relays_ping = False
            @property
            def ready(self): return self.bridge.is_connected()
            @property
            def name(self): return "" if Kit.streamer else (self.bridge.config() or {}).get("user", "")
            def poll(self):
                events = []; connected = self.ready
                if connected != self.was_connected:
                    if connected:
                        events.append(("status", "Using TazUO's Enhanced Map login%s." % (
                                       " (%s)" % self.name if self.name else ""), False))
                    elif self.was_connected:
                        now = time.time(); self.drops = [d for d in self.drops if now - d < self.DROP_WINDOW] + [now]
                        if len(self.drops) >= self.DROP_LIMIT and not self.unhooked_for_drops:
                            safe(self.bridge.unhook); self.unhooked_for_drops = True
                            events.append(("status", "TazUO's Enhanced Map keeps dropping, so Map "
                                           "Pings stopped listening on it (your pings still go "
                                           "out; others' don't show); click Reconnect to listen again.", True))
                        else:
                            events.append(("status", "TazUO's Enhanced Map connection dropped; "
                                                     "TazUO will reconnect.", True))
                    else: events.append(("status", "Waiting for TazUO's Enhanced Map to connect", False))
                    self.was_connected = connected
                for pid, payload in self.bridge.frames():
                    if pid == 0x33: self.server_relays_ping = True
                    try: events.append(parse_ping(pid, Reader(payload, 0)))
                    except ValueError: pass
                return events
            def send(self, data): safe(lambda: self.bridge.send(data))
            def reset(self):
                self.drops = []
                if self.unhooked_for_drops: self.unhooked_for_drops = False; safe(self.bridge.hook)
                safe(self.bridge.reconnect)
            def close(self): safe(self.bridge.unhook)
        def short_error(e): s = str(e) or e.__class__.__name__; return s if len(s) < 60 else s[:59]
        _xy = {}
        def xy_fields(t):
            got = _xy.get(t)
            if got is None: got = _xy[t] = (t.GetField("X"), t.GetField("Y"))
            return got
        def spot_of(obj):
            if obj is None: return None
            with Kit.quiet:
                if not obj.OnGround: return "root", int(obj.RootContainer)
            with Kit.quiet: return int(obj.X), int(obj.Y)
            with Kit.quiet:
                t = obj.GetType(); fx, fy = xy_fields(t)
                if fx is not None and fy is not None: return int(fx.GetValue(obj)), int(fy.GetValue(obj))
                px, py = t.GetProperty("X"), t.GetProperty("Y")
                if px is not None and py is not None: return int(px.GetValue(obj, None)), int(py.GetValue(obj, None))
            return None
        def root_spot(s):
            o = API.FindMobile(s) if 0 < s < 0x40000000 else Kit.find_item(s)
            if o is None or not (s < 0x40000000 or o.OnGround): return None
            return int(o.X), int(o.Y)
        def masked(who):
            if who == "You" or not Kit.streamer: return who
            return Kit.veil("name", who, Kit.checksum(str(who).lower().encode("utf-8")))
        class Ping(object):
            def __init__(self, x, y, m, t, now, auto=False):
                self.x, self.y, self.map, self.type, self.auto = x, y, m, t, auto; self.created = self.next_pulse = now
                self.marked, self.entry = False, None
        class HistEntry(object):
            def __init__(self, seq, at, t, who, x, y, m, local):
                self.seq, self.at, self.type, self.who = seq, at, t, who
                self.x, self.y, self.map, self.local = x, y, m, local
        class PingDisplay(object):
            PULSE = 1.4
            def __init__(self):
                self.pings, self.markers, self.history, self.marked = [], [], [], {}
                self.map_at, self.last_sound = 0.0, -1.0; self.map_since = self.arrow_for = None
                self.hist_ver = self.hist_seq = 0
            def player(self):
                p = API.Player
                try: return int(p.X), int(p.Y), int(API.GetMap()), int(p.Serial)
                except Exception: return 0, 0, -1, 0
            def show(self, sender, x, y, m, t, local=False, who=None, auto=False):
                now = time.time(); p = Ping(x, y, m, t, now, auto); self.pings.append(p)
                if len(self.pings) > 12: self._expire(next((q for q in self.pings[:-1] if q.auto), self.pings[0]))
                label, hue, _, mapcolor = TYPE_INFO[t]; px, py, pm, serial = self.player()
                where = Kit.where_text(x - px, y - py, "on you") if pm == m and px > 0 else "on %s" % facet_name(m)
                who = (who or "You") if local else sender
                say("%s pinged %s %s (%d, %d, %s)." % ("you" if who == "You" else who, label, where, x, y,
                                                       facet_name(m)), hue)
                self.hist_seq += 1; p.entry = HistEntry(self.hist_seq, now, t, str(who), x, y, m, bool(local))
                self.history.append(p.entry)
                if len(self.history) > HISTORY_MAX: del self.history[:len(self.history) - HISTORY_MAX]
                self.hist_ver += 1
                if not local and serial: API.HeadMsg("%s: %s %s" % (masked(sender), label, where), serial, hue)
                if pm == m:
                    key = (x, y, m); self.marked[key] = self.marked.get(key, 0) + 1; p.marked = True
                    API.MarkTile(x, y, hue, m)
                    if (not auto and px > 0 and x > 0 and y > 0 and max(abs(x - px), abs(y - py)) > 2):
                        API.TrackingArrow(x, y, ARROW_ID); self.arrow_for = p
                name = ("%s: %s %s" % (masked(who), label, time.strftime("%H:%M:%S"))).replace(",", " ")
                if ATLAS.map_open(True):
                    API.AddMapMarker(name, x, y, m, mapcolor); self.markers.append((now + 60, name))
                    if len(self.markers) > MARKERS_CAP:
                        ATLAS.loose.update([n for _, n in self.markers[:-MARKERS_CAP]]); del self.markers[:-MARKERS_CAP]
                self._play_sound(t, now)
            def _play_sound(self, t, now):
                if not settings["sounds"] or now - self.last_sound < 0.3: return
                self.last_sound = now; API.PlaySound(PING_SOUNDS[t])
            def update(self):
                if not self.pings and not self.markers: return
                now = time.time(); pm = None; stay = settings["ping_secs"]
                for p in list(self.pings):
                    if now - p.created >= stay: self._expire(p); continue
                    if now < p.next_pulse: continue
                    if pm is None: pm = self.player()[2]
                    if p.map == pm:
                        p.next_pulse = now + self.PULSE; _, hue, gfx, _ = TYPE_INFO[p.type]
                        API.CreateEffect(gfx, type=API.EffectType.FixedXYZ, hue=hue, sourceX=p.x, sourceY=p.y,
                                         duration=self.PULSE)
                if self.markers and now >= self.markers[0][0] and self._map_ready(now) and ATLAS.map_open(True):
                    while self.markers and now >= self.markers[0][0]: API.RemoveMapMarker(self.markers.pop(0)[1])
            def _map_ready(self, now):
                if now >= self.map_at or self.map_at - now > 2.0:
                    self.map_at = now + 1.0
                    if ATLAS.map_open():
                        if self.map_since is None or self.map_since > now: self.map_since = now
                    else: self.map_since = None
                return self.map_since is not None and now - self.map_since >= ATLAS_SETTLE
            def _expire(self, p):
                if p in self.pings: self.pings.remove(p)
                if p.marked:
                    key = (p.x, p.y, p.map); left = self.marked.get(key, 1) - 1
                    if left <= 0: self.marked.pop(key, None); API.RemoveMarkedTile(p.x, p.y, p.map)
                    else: self.marked[key] = left
                    p.marked = False
                if self.arrow_for is p: self.arrow_off()
            def arrow_entry(self):
                a = self.arrow_for
                if a is None or isinstance(a, HistEntry): return a
                return a.entry
            def arrow_to(self, e): API.TrackingArrow(e.x, e.y, ARROW_ID); self.arrow_for = e
            def arrow_off(self):
                if self.arrow_for is not None: API.TrackingArrow(-1, -1, ARROW_ID); self.arrow_for = None
            def clear(self):
                for p in list(self.pings): self._expire(p)
                if self.markers:
                    names = [n for _, n in self.markers]
                    if ATLAS.map_open(True):
                        for name in names: API.RemoveMapMarker(name)
                    else: ATLAS.loose.update(names)
                self.markers = []; API.TrackingArrow(-1, -1, ARROW_ID)
        class Settings(object):
            def __init__(self):
                scope = API.PersistentVar.Server
                self.host = API.GetPersistentVar(VAR_PREFIX + "host", "", scope).strip()
                try: self.port = int(API.GetPersistentVar(VAR_PREFIX + "port", str(DEFAULT_PORT), scope))
                except ValueError: self.port = DEFAULT_PORT
                self.user = API.GetPersistentVar(VAR_PREFIX + "user", "", scope).strip()
                self.password = API.GetPersistentVar(VAR_PREFIX + "pass", "", scope)
            @property
            def complete(self): return bool(self.host and self.user and self.password and 0 < self.port < 65536)
            def save(self):
                scope = API.PersistentVar.Server
                for k, v in (("host", self.host), ("port", str(self.port)), ("user", self.user),
                             ("pass", self.password)):
                    API.SavePersistentVar(VAR_PREFIX + k, v, scope)
        HIST_TITLE = "Ping History"; HIST_DOCK = "pings_history"; HIST_POS_KEY = VAR_PREFIX + "history_pos"
        HIST_MIN_KEY = VAR_PREFIX + "history_min"; HIST_OPEN_KEY = VAR_PREFIX + "history_open"
        HIST_MINI_W, HIST_MINI_H = 320, 46; HIST_ROW_H = 24; HIST_COLS = (("When", 70), ("Ping", 80), ("From", 140))
        HIST_TIP = "Put the tracking arrow on this spot (click again to take it down)"
        HIST_ALT = ". Alt+click: auto-follow (again to stop)"
        HIST_EMPTY = "No pings yet. Send one with a ping button, a hotkey or the wheel drag."
        class HistoryWindow(object):
            def __init__(self, app):
                self.app = app; self.page, self.next_draw = 0, 0.0; self.drawn = self.drawn_pos = None
                self.st = {"g": None, "shutting": False, "minimized": False, "docked": False, "queue": [], "c": {},
                           "store": ({}, {}), "rows": []}
                self.wnd = Kit.Window(HIST_DOCK, HIST_TITLE, self.st, self.st, self.build, HIST_POS_KEY,
                                      default=(260, 160), mini=(HIST_MINI_W, HIST_MINI_H), icon=0x14EB, lock=True,
                                      owner=False, close_tip="Close Ping History", clear={"c": {}, "rows": []})
                self.queue = self.wnd.queue
            def start(self):
                hs = self.st; hs["shutting"] = False
                hs["minimized"] = Kit.load_min(HIST_MIN_KEY) or HOST.dock_wanted(HIST_DOCK)
                self.wnd.dock(fit=True, min=(560, list_h(1, HIST_ROW_H)), show=self.zone_show)
                if Kit.get_var(HIST_OPEN_KEY, "0") == "1": self.build()
            def zone_show(self): self.st["minimized"] = self.st["docked"] = False; self.queue.add("open")
            def toggle_open(self):
                hs = self.st
                if hs["g"] is not None and not (hs["minimized"] or hs["docked"]):
                    if not HOST.layout_holds(HIST_DOCK): self.close()
                    return
                hs["minimized"] = hs["docked"] = False; HOST.dock_forget(HIST_DOCK)
                Kit.save_min(HIST_MIN_KEY, False); Kit.put_var(HIST_OPEN_KEY, "1"); self.build()
            def close(self):
                hs = self.st
                if hs["g"] is None: return
                self.wnd.close(); hs["docked"] = False; HOST.dock_forget(HIST_DOCK); Kit.put_var(HIST_OPEN_KEY, "0")
            def shutdown(self):
                hs = self.st; hs["shutting"] = True; HOST.dock_remove(HIST_DOCK)
                if hs["g"] is not None:
                    Kit.save_min(HIST_MIN_KEY, hs["minimized"] and not hs["docked"]); self.wnd.close()
            def build(self):
                hs = self.st; z = told(self.wnd, hs, 560, list_h(1, HIST_ROW_H))
                w, h = z if z else (560, list_h(HISTORY_ROWS, HIST_ROW_H))
                n = self.wnd.rows(HIST_ROW_H, list_h(0, HIST_ROW_H), HISTORY_ROWS) if z else HISTORY_ROWS
                g, store, c = self.wnd.begin(w, h); rows = []
                if not hs["minimized"]:
                    self.wnd.frame(g); M = Kit.MARGIN; IW = w - 2 * M; yt = M + 30 + Kit.GAP
                    Kit.add_section(g, M, yt, IW, 36); bx = M + 12
                    Kit.art_button(g, store, "clear", Kit.ART_CLOSE, bx, yt + 7, "Clear",
                                   "Empty the history (pings on screen stay)", on_click=self.queue("clear"))
                    bx += 35 + Kit.text_w("Clear") + 16
                    Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, bx, yt + 7, "Arrow off",
                                   "Take the tracking arrow down", on_click=self.queue("arrow_off"))
                    right = M + IW - 8; c["pg"] = Kit.add_label(g, "", right - 100, yt + 10, Kit.HUE_INFO)
                    Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 56, yt + 8, None,
                                   "Previous page (newer pings)", on_click=self.queue(("page", -1)))
                    Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 34, yt + 8, None,
                                   "Next page (older pings)", on_click=self.queue(("page", 1)))
                    yl = yt + 36 + Kit.GAP; Kit.add_section(g, M, yl, IW, h - yl - M)
                    cx = M + 12; xs = []
                    for head, cw in HIST_COLS:
                        Kit.add_label(g, head, cx, yl + 6, Kit.HUE_TITLE); xs.append((cx, cw)); cx += cw + 8
                    Kit.add_label(g, "Where", cx, yl + 6, Kit.HUE_TITLE); c["where_w"] = M + IW - 12 - cx
                    for k in range(n):
                        ry = yl + 30 + k * HIST_ROW_H
                        r = {"val": None, "prev": None, "changed": 0.0, "tip": None, "vis": True, "sig": None,
                             "labels": [Kit.add_label(g, "", xx, ry + 3, Kit.HUE_TEXT) for xx, _ in xs],
                             "where": Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO), "widths": [cw for _, cw in xs]}
                        r["catch"] = Kit.catcher(g, M + 6, ry, IW - 12, HIST_ROW_H,
                                                 Kit.row_clicker(r, self.queue, "arrow"), HIST_TIP)
                        rows.append(r)
                self.wnd.end(g, {"rows": rows}); self.drawn = None; self.refresh()
            def tick(self):
                hs = self.st
                if hs["g"] is not None and Kit.was_clicked(hs["store"], "close"): self.close(); return
                q = hs["queue"]
                while q:
                    a = q.pop(0); kind = a[0] if isinstance(a, tuple) else a
                    if kind == "toggle_min":
                        hs["minimized"] = not hs["minimized"]; hs["docked"] = False; HOST.dock_forget(HIST_DOCK)
                        Kit.save_min(HIST_MIN_KEY, hs["minimized"])
                    elif kind == "to_bar": HOST.dock_to_bar(HIST_DOCK, HIST_TITLE)
                    elif kind == "settings": HOST.show_settings("pings")
                    elif kind == "page": self.page = max(0, self.page + a[1]); self.next_draw = 0.0
                    elif kind == "clear":
                        disp = self.app.display; del disp.history[:]; disp.hist_ver += 1; self.page = 0
                    elif kind == "arrow_off": self.app.display.arrow_off()
                    elif kind == "arrow": self.arrow(a[1])
                    elif kind == "follow": self.follow(a[1])
                    if kind == "open" or kind in ("toggle_min", "redraw") and hs["g"] is not None: self.build()
                if hs["g"] is None or (hs["minimized"] and hs["docked"]): return
                self.refresh()
            def entry(self, seq): return next((e for e in self.app.display.history if e.seq == seq), None)
            def arrow(self, seq):
                disp = self.app.display; e = self.entry(seq)
                if e is None: return
                if disp.arrow_entry() is e: disp.arrow_off(); return
                pm = disp.player()[2]
                if pm != e.map: say("that ping is on %s; you are on %s." % (facet_name(e.map), facet_name(pm))); return
                disp.arrow_to(e); say("tracking arrow on %s's %s (%d, %d)." % (e.who, label_of(e.type), e.x, e.y))
            def follow(self, seq):
                e = self.entry(seq)
                if e is None: return
                if e.local: say("that ping is your own."); return
                serial = self.mobile_named(e.who)
                if not serial: say("%s isn't in range." % e.who); return
                Follow.toggle(serial, TITLE)
            def mobile_named(self, name):
                low = str(name or "").strip().lower()
                if not low: return 0
                best, bd = 0, None
                for m in API.GetAllMobiles() or ():
                    if str(m.Name or "").strip().lower() != low: continue
                    d = int(m.Distance)
                    if bd is None or d < bd: best, bd = int(m.Serial), d
                return best
            def where_text(self, e, px, py, pm):
                spot = xy(e.x, e.y, "(%d, %d)")
                if pm != e.map or px <= 0: return "%s %s" % (facet_name(e.map), spot)
                return "%s  %s" % (Kit.where_text(e.x - px, e.y - py, "here"), spot)
            def refresh(self):
                hs = self.st; disp = self.app.display; hist = disp.history; c = hs["c"]
                if hs["minimized"]:
                    if self.drawn == disp.hist_ver: return
                    self.drawn = disp.hist_ver
                    if hist:
                        e = hist[-1]
                        txt = "%s: %s, last %s %s" % (HIST_TITLE, Kit.count(len(hist), "ping"), label_of(e.type),
                                                       self.sender(e))
                    else: txt = "%s: no pings yet" % HIST_TITLE
                    if c.get("status") is not None: Kit.set_text(c["status"], Kit.fit(txt, HIST_MINI_W - 90))
                    return
                now = time.time(); arrow = disp.arrow_entry(); sig = (disp.hist_ver, self.page, arrow)
                if sig == self.drawn and now < self.next_draw: return
                pos = disp.player()[:3] if hist else (0, 0, -1)
                if sig == self.drawn and pos == self.drawn_pos: self.next_draw = now + 1.0; return
                self.drawn, self.next_draw, self.drawn_pos = sig, now + 1.0, pos; n = len(hist)
                per = max(1, len(hs["rows"])); pages = max(1, (n + per - 1) // per)
                self.page = max(0, min(pages - 1, self.page))
                if c.get("pg") is not None:
                    Kit.set_text(c["pg"], ("%d/%d" % (self.page + 1, pages)) if pages > 1 else "")
                px, py, pm = pos; first = n - 1 - self.page * per; where_w = c.get("where_w", 200)
                for k, r in enumerate(hs["rows"]):
                    i = first - k
                    if i < 0:
                        Kit.row_set(r, None, now); r["sig"] = None
                        if k == 0 and n == 0:
                            Kit.set_text(r["labels"][0], HIST_EMPTY, Kit.HUE_INFO); self._show(r, True, only_first=True)
                        else: self._show(r, False)
                        continue
                    e = hist[i]; Kit.row_set(r, (e.seq,), now); hue = TYPE_INFO[e.type][1]; on = arrow is e
                    where = self.where_text(e, px, py, pm); rsig = (e.seq, where, on)
                    if rsig != r["sig"]:
                        r["sig"] = rsig
                        texts = (time.strftime("%H:%M:%S", time.localtime(e.at)), label_of(e.type), self.sender(e))
                        hues = (Kit.HUE_INFO, hue, Kit.HUE_TEXT if not e.local else Kit.HUE_INFO)
                        for j, lbl in enumerate(r["labels"]):
                            Kit.set_text(lbl, Kit.fit(texts[j], r["widths"][j]), hues[j])
                        Kit.set_text(r["where"], Kit.fit(("> " if on else "") + where, where_w),
                                     Kit.HUE_TITLE if on else Kit.HUE_INFO)
                        tip = ("Take the tracking arrow down" if on else HIST_TIP) + ("" if e.local else HIST_ALT)
                        if tip != r["tip"]: r["tip"] = tip; Kit.with_tip(r["catch"], tip)
                    self._show(r, True)
            def sender(self, e): return masked(e.who)
            def _show(self, r, on, only_first=False):
                want = ("first" if only_first else on)
                if r["vis"] == want: return
                r["vis"] = want; parts = r["labels"] + [r["where"], r["catch"]]
                for j, ctl in enumerate(parts): Kit.set(ctl, "IsVisible", on and (not only_first or j == 0))
        class PingApp(object):
            def __init__(self):
                self.mouse = self.gesture = self.guide = self.bridge = self.bridge_error = self.conn = None
                self.aim = self.status_label = self.last_pos = None; self.guide_labels, self.recent_pings = {}, {}
                self.bridge_tried = self._shut = self.in_thread = False
                self.next_link_check = self.last_pos_sent = self.next_pos_read = 0
                self.last_ping_sent = self.last_auto_sent = 0; self.recent_order = collections.deque()
                self.settings = Settings(); self.display = PingDisplay()
                self.pending, self.jobs, self.outbox, self.inbox, self.hooked = [], [], [], [], []
                self.status_text, self.status_w = "", 300; self.history = HistoryWindow(self)
            def set_status(self, text, also_journal=True):
                self.status_text = text
                if self.in_thread: self.inbox.append(("status", text, also_journal)); return
                lbl = self.status_label
                if lbl is not None: Kit.set_text(lbl, Kit.fit(text.rstrip("."), self.status_w))
                if also_journal: say(journal_case(text))
            def _queue_ping(self, t):
                def fn(*args):
                    if HOST.typing(): return
                    self.pending.append(("target", t)); HOST.poke()
                return fn
            def save_setup(self):
                if self.conn and self.conn.kind == "tazuo":
                    self.set_status("Saved; TazUO's Enhanced Map login is on, so that stays in use."); return
                if self.conn: self.conn.close(); self.conn = None
                self.choose_link()
            def apply_options(self):
                if settings["gesture"] and self.mouse is None: self.init_mouse()
                elif not settings["gesture"]: self.mouse = self.gesture = None; self.close_guide()
                self.jobs.append(("link",))
            def connect(self):
                if self.conn: self.conn.close()
                s = self.settings; self.conn = MapConnection(s.host, s.port, s.user, s.password)
                self.set_status("Connecting to %s:%d" % (s.host, s.port), also_journal=False)
            def get_bridge(self):
                if not self.bridge_tried:
                    self.bridge_tried = True
                    try: self.bridge = TazUOBridge()
                    except Exception as e: self.bridge = None; self.bridge_error = short_error(e)
                return self.bridge
            def tazuo_available(self):
                b = self.get_bridge(); return b is not None and bool((b.config() or {}).get("configured"))
            def choose_link(self, announce=True):
                mode = (settings["connection"] or "auto").lower(); current = self.conn.kind if self.conn else None
                if mode in ("auto", "tazuo") and self.tazuo_available():
                    if current != "tazuo":
                        if self.conn: self.conn.close()
                        self.conn = TazUOLink(self.bridge)
                    return
                if mode == "tazuo":
                    if current == "tazuo": return
                    if current == "own": self.conn.close(); self.conn = None; announce = True
                    if announce:
                        if self.get_bridge() is None:
                            self.set_status("Can't use TazUO's Enhanced Map connection (%s)." % self.bridge_error)
                        else: self.set_status("Turn on Enhanced Map in TazUO's Options (server, port, login).")
                    return
                if current == "tazuo": self.conn.close(); self.conn = None; current = None
                if current == "own": return
                if self.settings.complete: self.connect()
                elif announce:
                    if mode == "auto" and self.get_bridge() is not None:
                        self.set_status("Turn on Enhanced Map in TazUO, or enter a map login (World Map settings).")
                    else: self.set_status("Enter your map server details to start."); self.inbox.append(("open_setup",))
            def send_ping(self, x, y, m, t):
                now = time.time()
                if now - self.last_ping_sent < PING_RATE_SECS: return
                self.last_ping_sent = now; self._send(x, y, m, t)
            def send_auto(self, x, y, m, t, who=None, quiet=False):
                now = time.time()
                if now - self.last_auto_sent < PING_RATE_SECS: return False
                self.last_auto_sent = now; return self._send(x, y, m, t, who=who, auto=True, quiet=quiet) or "local"
            def _send(self, x, y, m, t, who=None, auto=False, quiet=False):
                self.display.show("You", x, y, m, t, local=True, who=who, auto=auto)
                if self.conn and self.conn.ready:
                    if self.conn.server_relays_ping:
                        self.outbox.append(packet(0x33, struct.pack("<HHBB", x & 0xFFFF, y & 0xFFFF, m & 0xFF,
                                                                    t & 0xFF)))
                    typed = pk_typed_alert(x, y, m, t)
                    if typed: self.outbox.append(typed)
                    self.outbox.append(pk_alert(x, y)); return True
                note = "Not connected: only you can see that ping."
                self.set_status(note, also_journal=not quiet and (not auto or self.status_text != note)); return False
            AIM_SECONDS = 10
            def target_ping(self, t):
                say("target a spot for %s (yourself: where you stand)." % label_of(t)); self.aim = None
                tm = Picker._tm()
                if tm is not None:
                    aim = {"t": t, "fired": False, "spot": None, "d": None, "tm": tm,
                           "until": time.time() + self.AIM_SECONDS}
                    def got(obj, aim=aim): aim["spot"] = spot_of(obj); aim["fired"] = True
                    with Kit.quiet:
                        from System import Action; aim["d"] = Action[object](got)
                        tm.SetTargeting(aim["d"], Picker.CURSOR_TARGET, Picker.neutral); self.aim = aim
                        HOST.claim_cursor("pings", self.AIM_SECONDS); return
                self.jobs.append(("aim", t))
            def poll_aim(self):
                aim = self.aim
                if aim is None: return
                if not aim["fired"]:
                    ours = bool(aim["tm"].IsCurrentTargetingAction(aim["d"]))
                    if ours and time.time() < aim["until"]: return
                    self.aim = None; HOST.release_cursor("pings")
                    if ours: aim["tm"].CancelTarget()
                    return
                self.aim = None; HOST.release_cursor("pings"); self.aimed(aim["t"], aim["spot"])
            def aimed(self, t, spot):
                if spot is not None and spot[0] == "root":
                    spot = root_spot(spot[1])
                    if spot is None: say("couldn't tell where that item is: target a spot, a person or an item on "
                                         "the ground."); return
                if spot is None: return
                x, y = spot
                if x <= 0 or y <= 0: return
                self.send_ping(x, y, int(API.GetMap()), t)
            def drop_aim(self):
                aim, self.aim = self.aim, None; HOST.release_cursor("pings")
                if aim is None or aim["fired"]: return
                tm = aim["tm"]
                def cancel():
                    if tm.IsCurrentTargetingAction(aim["d"]): tm.CancelTarget()
                safe(lambda: Kit.on_client(cancel, fallback=False))
            def target_ping_blocking(self, t):
                spot = spot_of(API.RequestAnyTarget(10))
                if spot is not None: self.inbox.append(("aimed", t, spot))
            def share_position(self):
                if not self.conn or not self.conn.ready or not self.conn.owns_position: return
                now = time.time()
                if now < self.next_pos_read: return
                self.next_pos_read = now + 0.5; pos = None
                if settings["share"]:
                    p = API.Player
                    try: pos = (int(p.X), int(p.Y), int(API.GetMap()))
                    except Exception: pass
                if pos is None or pos[0] <= 0:
                    if now - self.conn.last_sent > 20: self.outbox.append(packet(0xFE))
                    return
                if ((pos != self.last_pos and now - self.last_pos_sent >= 1.0) or now - self.last_pos_sent >= 10):
                    flag = (4 if p.IsDead else 1 if p.IsPoisoned else 2 if p.IsYellowHits else 3 if p.IsParalyzed
                            else 5 if p.IsHidden else 0)
                    stats = (int(p.Hits), int(p.Stamina), int(p.Mana), int(p.HitsMax), int(p.StaminaMax),
                             int(p.ManaMax))
                    self.outbox.append(pk_player_data(pos, stats, flag, 0xFFFFD700))
                    self.last_pos, self.last_pos_sent = pos, now
            def handle(self, ev):
                kind = ev[0]
                if kind == "status": self.set_status(ev[1], also_journal=ev[2])
                elif kind == "ping": self.show_once(*ev[1:])
                elif kind == "alert":
                    _, name, x, y = ev; decoded = decode_typed_alert(x, y)
                    if decoded: self.show_once(name, *decoded)
                    elif not self.seen_recently(name, x, y): self.show_once(name, x, y, int(API.GetMap()), LOOK)
                elif kind == "message": say("map server: " + ev[1])
            DEDUPE_SECONDS = 3
            def seen_recently(self, name, x, y, t=None):
                now = time.time(); order, recent = self.recent_order, self.recent_pings
                while order and now - order[0][0] > self.DEDUPE_SECONDS:
                    at, key = order.popleft()
                    if recent.get(key) == at: del recent[key]
                if t is not None: return (name, x, y, t) in recent
                for k in recent:
                    if k[0] == name and k[1] == x and k[2] == y: return True
                return False
            def show_once(self, name, x, y, m, t):
                if self.seen_recently(name, x, y, t): return
                now = time.time(); key = (name, x, y, t); self.recent_pings[key] = now
                self.recent_order.append((now, key)); self.display.show(name, x, y, m, t)
            def step(self):
                while self.pending:
                    action = self.pending.pop(0)
                    if action[0] == "target": self.target_ping(action[1])
                    elif action[0] == "options": self.apply_options()
                    elif action[0] == "rehook": self.register_hotkeys()
                    elif action[0] == "history": self.history.toggle_open()
                    else: self.jobs.append(action)
                for _i in range(len(self.inbox)):
                    ev = self.inbox.pop(0)
                    if ev[0] == "open_setup": HOST.show_settings("pings")
                    elif ev[0] == "aimed": self.aimed(ev[1], ev[2])
                    else: self.handle(ev)
                self.poll_aim()
                if self.conn: self.share_position()
                self.poll_gesture(); self.display.update(); self.history.tick()
            def thread_step(self):
                self.in_thread = True
                try: self.thread_jobs()
                finally: self.in_thread = False
            def thread_jobs(self):
                while self.jobs:
                    action = self.jobs.pop(0)
                    if action[0] == "save_setup": self.save_setup()
                    elif action[0] == "link": self.choose_link(announce=False)
                    elif action[0] == "aim": self.target_ping_blocking(action[1])
                    elif action[0] == "reconnect":
                        if self.conn and self.conn.kind == "tazuo":
                            self.conn.reset(); self.set_status("Asked TazUO's Enhanced Map to reconnect.")
                        elif self.settings.complete and (settings["connection"] or "auto").lower() != "tazuo":
                            self.connect(); self.conn.reset()
                        else: self.choose_link()
                if time.time() >= self.next_link_check:
                    self.next_link_check = time.time() + 5; self.choose_link(announce=False)
                out = self.outbox
                if out: self.outbox = []
                if self.conn:
                    for data in out: self.conn.send(data)
                    self.inbox.extend(self.conn.poll())
            def init_mouse(self):
                if not settings["gesture"]: self.mouse = None; return
                try: self.mouse = TazUOMouse()
                except Exception as e:
                    self.mouse = None
                    say("mouse-wheel pings unavailable (%s): use the ping buttons or hotkeys." % short_error(e))
            @staticmethod
            def drag_direction(dx, dy):
                if max(abs(dx), abs(dy)) < settings["drag"]: return None
                if abs(dx) > abs(dy): return "right" if dx > 0 else "left"
                return "down" if dy > 0 else "up"
            def poll_gesture(self):
                m = self.mouse
                if m is None: return
                down = m.middle_down()
                if down and self.gesture is None:
                    tile = m.tile_under_mouse(); start = m.position(m._mclick)
                    self.gesture = {"tile": tile, "start": start, "dir": None, "map": int(API.GetMap())}
                    if tile is not None: self.show_guide(start)
                elif down and self.gesture is not None:
                    if self.gesture["tile"] is None: return
                    x, y = m.position()
                    d = self.drag_direction(x - self.gesture["start"][0], y - self.gesture["start"][1])
                    if d != self.gesture["dir"]: self.gesture["dir"] = d; self.update_guide(d)
                elif not down and self.gesture is not None:
                    g, self.gesture = self.gesture, None; self.close_guide(); t = GESTURE.get(g["dir"])
                    if g["tile"] is not None and t is not None: self.send_ping(g["tile"][0], g["tile"][1], g["map"], t)
            def show_guide(self, center):
                self.close_guide()
                w, h = 180, 104; gump = G.CreateGump(False, False); scale = Kit.render_scale() or 1.0
                cx, cy = int(round(center[0] / scale)), int(round(center[1] / scale))
                Kit.place(gump, cx - w // 2, cy - h // 2, w, h); Kit.add_window_frame(gump, w, h, corners=False)
                Kit.add_section(gump, 6, 6, w - 12, h - 12)
                for d, (lx, ly) in (("up", (58, 9)), ("right", (110, 43)), ("down", (58, 77)), ("left", (11, 43))):
                    t = GESTURE[d]; lab = G.CreateGumpLabel(label_of(t), Kit.HUE_INFO); lab.SetRect(lx, ly, 70, 18)
                    gump.Add(lab); self.guide_labels[d] = (lab, t)
                plus = G.CreateGumpLabel("+", Kit.HUE_TITLE); plus.SetRect(w // 2 - 3, h // 2 - 9, 10, 18)
                gump.Add(plus)
                Kit.add_front(gump); SNAP.skip_gump(gump); self.guide = gump
            def update_guide(self, chosen):
                for d, (lab, t) in self.guide_labels.items():
                    lab.Text = "[" + label_of(t) + "]" if d == chosen else label_of(t)
                    lab.Hue = TYPE_INFO[t][1] if d == chosen else 946
            def close_guide(self): Kit.dispose(self.guide); self.guide, self.guide_labels = None, {}
            def register_hotkeys(self):
                self.unregister_hotkeys()
                for key, combo in HOTKEYS.items():
                    if combo:
                        t = TYPE_KEYS[key]; what = "%s ping" % label_of(t)
                        got = HOST.hotkey_on(combo, TITLE, self._queue_ping(t), what)
                        if got is False: say("couldn't set the %s hotkey (%s isn't a key)." % (label_of(t), combo),
                                             Kit.HUE_BAD)
                        if got is not False: self.hooked.append(combo)
            def unregister_hotkeys(self):
                for combo in self.hooked: HOST.hotkey_off(combo, TITLE)
                self.hooked = []
            def shutdown(self):
                if self._shut: return
                self._shut = True; self.unregister_hotkeys(); self.drop_aim(); self.close_guide()
                safe(self.history.shutdown); safe(self.display.clear)
                if self.conn: self.conn.close()
            def start(self):
                self.init_mouse(); self.register_hotkeys(); self.history.start()
                self.choose_link(); self.next_link_check = time.time() + 5
        def _queue_app(action):
            if st["app"] is not None: st["app"].pending.append(action)
        page = {"f": None}; H_SEND, H_LOGIN, H_KEYS = 116, 160, 70
        PING_TIP = "Send a %s ping on the spot, item or person you target"
        KEY_TIP = "Key for a %s ping, like CTRL+1, F9 or SHIFT+F2 (blank = none)"
        LOGIN_TIPS = {"host": "Map server address (host name or IP)", "port": "Map server port (default %d)"
                      % DEFAULT_PORT, "user": "Your map server login name",
                      "pass": "Map server password; saved in plain text on this PC, like Enhanced Map's"}
        def _page_action(action):
            def fn(*args): _queue_app(action)
            return fn
        def draw_send(f, x, y):
            g, store, w = f.g, f.store, f.w; bx = x + 12
            for t in (LOOK, DANGER, GO, HELP):
                label, hue = TYPE_INFO[t][:2]; cap = label + "..."
                Kit.art_button(g, store, "ping%d" % t, Kit.ART_PLAY, bx, y + 28, cap, PING_TIP % label,
                               hue=hue, on_click=_page_action(("target", t)))
                bx += 35 + Kit.text_w(cap) + 16
            Kit.art_button(g, store, "recon", Kit.ART_PLAY, x + 12, y + 58, "Reconnect", "Reconnect to the map server",
                           on_click=_page_action(("reconnect",)))
            hx = x + 12 + 35 + Kit.text_w("Reconnect") + 16
            Kit.art_button(g, store, "history", Kit.ART_PAGE, hx, y + 58, "History",
                           "Open or close the window of recent pings, yours and others'",
                           on_click=_page_action(("history",)))
            gx = hx + 35 + Kit.text_w("History") + 16; app = st["app"]
            if app is not None:
                Kit.add_label(g, Kit.fit("Wheel drag: up Look, right Danger, down Go, left Help", x + w - 12 - gx),
                              gx, y + 61, Kit.HUE_INFO)
            lbl = Kit.add_label(g, "", x + 12, y + 90, Kit.HUE_INFO); page["status"] = lbl
            if app is not None:
                app.status_label, app.status_w = lbl, w - 24
                Kit.set_text(lbl, Kit.fit(app.status_text.rstrip(".") or "Starting", w - 24))
        def draw_login(f, x, y):
            g, w = f.g, f.w; saved = Settings(); col = (w - 36) // 2; page["fields"] = fields = {}
            for i, (key, caption, value) in enumerate((
                    ("host", "Server address:", saved.host), ("port", "Port:", str(saved.port)),
                    ("user", "Map username:", saved.user), ("pass", "Map password:", saved.password))):
                fx = x + 12 + (i % 2) * (col + 12); fy = y + 30 + (i // 2) * 48; Kit.add_label(g, caption, fx, fy)
                fields[key] = Kit.with_tip(Kit.add_textbox(g, value, fx + 2, fy + 20, col - 8, numbers=key == "port"),
                                           LOGIN_TIPS[key])
            Kit.art_button(g, f.store, "save", Kit.ART_OK, x + 12, y + 128, "Save and connect",
                           "Save the four fields on this PC and connect")
            page["login"] = Kit.add_label(g, Kit.fit("Saved on this PC in plain text (password shows while typing).",
                                                     w - 236), x + 220, y + 131, Kit.HUE_INFO)
        def draw_keys(f, x, y):
            kx = x + 12; page["keys"] = keys = {}
            for k in HOTKEY_ORDER:
                cap = k.capitalize() + ":"; Kit.add_label(f.g, cap, kx, y + 36)
                keys[k] = Kit.with_tip(Kit.add_textbox(f.g, HOTKEYS[k], kx + Kit.text_w(cap) + 8, y + 33, 84,
                                                       numbers=False), KEY_TIP % label_of(TYPE_KEYS[k]))
                kx += Kit.text_w(cap) + 8 + 84 + 16
        NUM = {"lgap": 8, "fw": 44, "ugap": 6}
        PAGE = (("SEND A PING  (or a hotkey or wheel drag)", (("custom", 0, draw_send),), {"sh": H_SEND, "top": 0}),
                ("MAP LOGIN  (when TazUO's Enhanced Map is off)", (("custom", 0, draw_login),),
                 {"sh": H_LOGIN, "top": 0}), ("OPTIONS", (
                    ("check", "sounds", "Play a sound for each ping", "For your pings and others'", {"stay": True}),
                    ("check", "gesture", "Ping with a mouse-wheel drag", "Hold the wheel on a spot and drag: up Look "
                     "here, right Danger, down Go here, left Need help", {"dx": 312}),
                    ("check", "share", "Show me on guildmates' maps", "Sends your position (map login only; TazUO's "
                     "Enhanced Map does its own)", {"stay": True}), ("gap", 28),
                    ("num", "ping_secs", "Ping stays:", "How long a ping's marker and pulse stay", "s",
                     OPT_LIMITS["ping_secs"][0], OPT_LIMITS["ping_secs"][1], dict(NUM, stay=True)),
                    ("num", "drag", "Drag distance:", "Pixels the wheel drag must move to count", "px",
                     OPT_LIMITS["drag"][0], OPT_LIMITS["drag"][1], dict(NUM, dx=312))), {"top": 32}),
                ("HOTKEYS  (blank = none)", (("custom", 0, draw_keys),), {"sh": H_KEYS, "top": 0}))
        def page_table(w): return PAGE
        cfg = Kit.Page(settings, page_table, save_settings)
        def build_config(g, x, y, w):
            f = Kit.Form(g, x, y, w, settings, PAGE)
            yo = y + H_SEND + H_LOGIN + 2 * Kit.GAP + 32 + (Kit.Form.COMPACT if Kit.compact else Kit.Form.OPTS)["ch"]
            Kit.add_label(g, "Connection:", x + 312, yo + 2)
            idx = CONN_CODES.index(settings["connection"]) if settings["connection"] in CONN_CODES else 0
            dd = G.CreateDropDown(190, [c[1] for c in CONNECTIONS], idx); dd.SetPos(x + 414, yo - 2); g.Add(dd)
            Kit.with_tip(dd, "TazUO's Enhanced Map while it is on, or the login above")
            page.update({"f": f, "dd": dd, "seen_keys": dict(HOTKEYS), "next_read": 0.0})
        def poll_config(force=False):
            f = page["f"]
            if f is None: return
            if Kit.was_clicked(f.store, "save"): _save_login()
            now = time.time()
            if not force and now < page["next_read"]: return
            page["next_read"] = now + 0.2; new = f.read()
            i = Kit.dd_index(page["dd"], -1)
            if 0 <= i < len(CONNECTIONS): new["connection"] = CONNECTIONS[i][0]
            if new != settings: settings.update(new); save_settings(); _queue_app(("options",))
            new = {}
            for k, tb in page["keys"].items():
                try: new[k] = _norm_key(tb.Text)
                except Exception: new[k] = _norm_key(HOTKEYS[k])
            if force and new != page["seen_keys"]:
                page["typed"] = page["seen_keys"] = new; HOTKEYS.update(new); save_settings(); _queue_app(("rehook",))
            elif new != page.get("typed"): page["typed"], page["stable"] = new, 0
            elif new != page["seen_keys"]:
                page["stable"] = page.get("stable", 0) + 1
                if force or page["stable"] >= 5:
                    page["seen_keys"] = new; HOTKEYS.update(new); save_settings(); _queue_app(("rehook",))
        def _save_login():
            f = page["fields"]
            try:
                host = f["host"].Text.strip(); port_text = f["port"].Text.strip(); user = f["user"].Text.strip()
                password = f["pass"].Text
            except Exception: return
            try: port = int(port_text)
            except ValueError: port = 0
            if not host or not user or not password or not (0 < port < 65536):
                Kit.set_text(page["login"], "Fill in all four fields (the port is a number)", Kit.HUE_BAD); return
            saved = Settings(); saved.host, saved.port, saved.user, saved.password = host, port, user, password
            saved.save()
            Kit.set_text(page["login"], "Saved", Kit.HUE_GOOD); app = st["app"]
            if app is not None:
                s = app.settings; s.host, s.port, s.user, s.password = host, port, user, password
                app.pending.append(("save_setup",))
        def config_closed():
            poll_config(True); app = st["app"]
            if app is not None and app.status_label is page.get("status"): app.status_label = None
            page.update({"f": None, "dd": None, "status": None, "keys": None, "fields": None, "login": None})
        def _offer_ping(x, y, m=None, kind="danger", who=None, quiet=False):
            app = st["app"]
            if app is None or app._shut: return False
            if m is None: m = API.GetMap()
            return app.send_auto(int(x), int(y), int(m), TYPE_KEYS.get(kind, DANGER), who, quiet)
        load_settings()
        def _start(): st["app"] = PingApp(); st["app"].start(); cleanup.service("pings.send", _offer_ping)
        def _tick():
            if st["app"] is not None: st["app"].step()
        def _thread_tick():
            if st["app"] is not None: st["app"].thread_step()
        def _interval():
            app = st["app"]
            if app is None: return 0.05
            if app.gesture is not None: return 0.02
            if app.aim is not None or app.pending or app.inbox or app.jobs or app.outbox: return 0.05
            return 0.1
        def _stop():
            cleanup.close(); app, st["app"] = st["app"], None
            if app is not None: app.shutdown()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": build_config, "poll_config": poll_config, "config_closed": config_closed,
                "thread_tick": _thread_tick, "interval": _interval}
    def _part_corpse():
        KEY = "corpserun"; TITLE = "Corpse"; SETTINGS_KEY = "CorpseRun_settings"; POS_KEY = "CorpseRun_pos"
        MIN_KEY = "CorpseRun_min"; CORPSE_KEY = "CorpseRun_corpse"; ARROW_ID = 0x434F5250; CORPSE_GRAPHIC = 0x2006
        BONES_FIRST, BONES_LAST = 0x0ECA, 0x0ED2; DEFAULT_DECAY_MIN = 15; DEFAULT_BONES_MIN = 45
        MIN_LO, MIN_HI = 1, 120; RED_SECS = 60; DECAYED_GRACE = 120.0; ALERT_DECAY = "corpserun.decay"; FIND_SECS = 20.0
        HUMAN_BODIES = (0x190, 0x191, 0x25D, 0x25E, 0x29A, 0x29B); SEEK_RANGE = 24; ITEM_EVERY = 1.0; REACH = 2
        POKE_GAP = 0.25; DIED_HOLD = 10.0
        MOVE_GAP = 0.7; MOVE_RECHECK = 2; PLAN_CAP = 250; J_WAIT = ("must wait to perform another action",)
        HAIR_FIRST, HAIR_LAST = 0x203B, 0x204D; PING_TRY = 15.0; W = 420; MINI_W, MINI_H = 280, 46; BODY_H = 128
        H = Kit.MARGIN + 30 + Kit.GAP + BODY_H + Kit.MARGIN
        settings = {"arrow": True, "restore": True, "ping": False, "decay": DEFAULT_DECAY_MIN,
                    "bones": DEFAULT_BONES_MIN}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "body": 0, "body_at": 0.0,
              "note_until": 0.0, "name": "", "drawn": None, "drawn_c": None, "unnamed": False, "hooked": False,
              "find_at": 0.0}
        win = {"g": None, "c": {}, "store": ({}, {})}; typed = {}
        cleanup, queue, say = Kit.basics(st, TITLE); NUMS = {"decay": (MIN_LO, MIN_HI), "bones": (MIN_LO, MIN_HI)}
        def load_settings():
            Kit.kv_load(SETTINGS_KEY, ";", settings, NUMS)
            if (settings["decay"], settings["bones"]) == (7, 7):
                settings["decay"], settings["bones"] = DEFAULT_DECAY_MIN, DEFAULT_BONES_MIN
        def save_settings():
            Kit.kv_save(SETTINGS_KEY, ";", settings, ("arrow", "restore", "ping", "decay", "bones"), NUMS)
        def load_rec():
            p = Kit.get_var(CORPSE_KEY).split("|")
            if len(p) < 8 or p[0] != "1": return None
            try:
                r = {"serial": int(p[1]), "x": int(p[2]), "y": int(p[3]), "facet": int(p[4]),
                     "died": float(p[5]), "body": int(p[6]), "spot": p[7] == "1", "exact": len(p) < 9 or p[8] != "0",
                     "name": p[9] if len(p) > 9 else ""}
            except ValueError: return None
            if not (0 <= r["serial"] < 0x80000000 and 0 <= r["x"] < 0x10000 and 0 <= r["y"] < 0x10000
                    and 0 <= r["facet"] < 0x100 and 0 <= r["body"] < 0x10000 and 0 < r["died"] < 1e11): return None
            return r
        def save_rec():
            r = st["rec"]
            if r is None: Kit.put_var(CORPSE_KEY, ""); return
            Kit.put_var(CORPSE_KEY, "1|%d|%d|%d|%d|%.0f|%d|%d|%d|%s" % (
                r["serial"], r["x"], r["y"], r["facet"], r["died"], r["body"], 1 if r["spot"] else 0,
                1 if r["exact"] else 0, r["name"].replace("|", "")))
        def note(text, secs=6.0, spot=None):
            st["note"] = text if spot is None else text.replace("%d, %d" % spot, xy(*spot))
            st["note_until"] = time.time() + secs; st["lbl_at"] = 0.0; say(journal_case(text))
        def remaining(now):
            r = st["rec"]
            if r is None: return 0.0
            if r["died"] > now: r["died"] = now
            return 60.0 * (settings["decay"] + settings["bones"]) - (now - r["died"])
        def clock(secs): secs = max(0, int(secs)); return "%d:%02d" % (secs // 60, secs % 60)
        item_of = Kit.find_item; held_item = Kit.held_item
        def cursor_up(): return bool(HOST.cursor_busy(KEY)) or bool(API.HasTarget())
        def is_hair(it):
            if HAIR_FIRST <= int(it.Graphic) <= HAIR_LAST: return True
            d = it.GetItemData(); return d is not None and int(d.Layer) in (11, 16)
        def weight_of(it):
            d = it.GetItemData(); w = int(d.Weight) if d is not None else 0
            total = (0 if w >= 255 else w) * max(1, int(it.Amount or 1))
            if it.IsContainer:
                for x in contents(int(it.Serial), PLAN_CAP):
                    d = x.GetItemData(); xw = int(d.Weight) if d is not None else 0
                    if xw < 255: total += xw * max(1, int(x.Amount or 1))
            return total
        def build_window():
            z = told(wnd, st, W, H); w, h = z if z else (W, H); g, store, c = wnd.begin(w, h)
            if not st["minimized"]:
                wnd.frame(g); M = Kit.MARGIN; IW = w - 2 * M; yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, h - yb - M, "YOUR CORPSE  (where, how long it lasts)")
                c["where"] = Kit.add_label(g, "", M + 12, yb + 28, Kit.HUE_TEXT)
                c["decay"] = Kit.add_label(g, "", M + 12, yb + 48, Kit.HUE_INFO)
                c["info"] = Kit.add_label(g, "", M + 12, yb + 68, Kit.HUE_INFO); by = yb + 92; xb = M + 10
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
            wnd.end(g); st["lbl_at"] = 0.0
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (220, 220), (MINI_W, MINI_H), 0x0ECA,
                         cleanup, lock=True, clear={"c": {}})
        def show_full():
            if not st["minimized"] and not st["docked"]: return
            st["minimized"], st["docked"] = False, False; HOST.dock_forget(KEY); Kit.save_min(MIN_KEY, False)
            build_window()
        def texts(me, now, mm):
            r = st["rec"]; j = st["job"]
            if r is None:
                dead = bool(st["was_dead"])
                info = st["note"] if st["note"] and now < st["note_until"] else \
                    ("Find a healer or a resurrection." if dead else "When you die, this window shows the way back.")
                return ("No corpse to find.", Kit.HUE_TEXT, "", Kit.HUE_INFO, info, TITLE + ": none")
            left = remaining(now); mx, my = int(me.X), int(me.Y)
            if not r["spot"]: where, mini = "Looking for your corpse round you", "looking"
            elif mm != r["facet"]:
                where = "On %s, at %s" % (Kit.facet_name(r["facet"]), xy(r["x"], r["y"]))
                mini = Kit.facet_name(r["facet"])
            else:
                wt = Kit.where_text(r["x"] - mx, r["y"] - my)
                where = "%s%s, at %s" % (wt[0].upper(), wt[1:], xy(r["x"], r["y"])); mini = wt
            bones_at = 60.0 * settings["bones"]; most = "" if r["exact"] else "at most "
            if left > bones_at:
                decay = "Bones in %s%s, gone in %s%s" % (most, clock(left - bones_at), most, clock(left))
            elif left > 0: decay = ("Bones %s; gone in %s%s" % ("now" if r["exact"] else "soon", most, clock(left)))
            else: decay = "Should have decayed by now"
            dhue = Kit.HUE_BAD if left <= RED_SECS else Kit.HUE_INFO
            if st["note"] and now < st["note_until"]: info = st["note"]
            elif j is not None:
                if j["phase"] == "open": info = "Opening your corpse"
                else: info = "Moving %d / %d" % (min(j["i"], len(j["plan"])), len(j["plan"]))
            else:
                died = (("Died %s ago." % Kit.ago(now - r["died"])) if r["exact"] else "Found as a ghost.")
                if not r["serial"] and st["unnamed"]: info = "Waiting for the corpse's name: click it once."
                elif st["was_dead"]: info = died + " Be resurrected, then click Get my things."
                elif r["serial"] and r["spot"]: info = died + " Stand by it and click Get my things."
                else: info = died + " Not seen there yet."
            mini = "%s  %s" % (mini, clock(left)) if left > 0 else mini
            return where, Kit.HUE_TEXT, decay, dhue, info, "%s: %s" % (TITLE, mini)
        def refresh(me, now, mm, force=False):
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]): return
            if not force and now < st["lbl_at"]: return
            st["lbl_at"] = now + 0.5; where, whue, decay, dhue, info, mini = texts(me, now, mm); c = win["c"]
            if st["minimized"]:
                hue = Kit.HUE_BAD if st["rec"] is not None and remaining(now) <= RED_SECS else Kit.HUE_INFO
                sig = (mini, hue)
            else: sig = (where, whue, decay, dhue, info, st["job"] is not None)
            if sig == st["drawn"] and c is st["drawn_c"]: return
            st["drawn"], st["drawn_c"] = sig, c
            if st["minimized"]:
                lbl = c.get("status")
                if lbl is not None: Kit.set_text(lbl, Kit.fit(mini, MINI_W - 90), hue)
                return
            for k, text, tone in (("where", where, whue), ("decay", decay, dhue), ("info", info, Kit.HUE_INFO)):
                Kit.set_text(c[k], Kit.fit(text, W - 2 * Kit.MARGIN - 24), tone)
            Kit.set_text(c["go"], "Stop" if st["job"] is not None else "Get my things",
                         Kit.HUE_TITLE if st["job"] is not None else Kit.HUE_TEXT)
        def arrow_tick(me, mm):
            r = st["rec"]; want = None
            if settings["arrow"] and r is not None and r["spot"] and mm == r["facet"]:
                if max(abs(int(me.X) - r["x"]), abs(int(me.Y) - r["y"])) > REACH: want = (r["x"], r["y"])
            if want == st["arrow"]: return
            if want is None: Kit.drop_arrow(st, ARROW_ID)
            else: API.TrackingArrow(want[0], want[1], ARROW_ID); st["arrow"] = want
        def on_death(me, now, at_start=False):
            if st["job"] is not None: stop_job("you died")
            x, y, m = int(me.X), int(me.Y), int(API.GetMap()); st["name"] = str(me.Name or "")
            st["rec"] = {"serial": 0, "x": x, "y": y, "facet": m, "died": now, "body": st["body"],
                         "spot": not at_start, "exact": not at_start, "name": st["name"]}
            st["seek_until"], st["seek_at"] = now + FIND_SECS, now
            st["gone_since"], st["warned"], st["unnamed"] = None, False, False; st["refused"] = set(); save_rec()
            if at_start: say("you are a ghost: looking for your corpse round you.")
            else:
                say("you died at %d, %d (%s). Bones in %s, gone %s later." % (
                    x, y, Kit.facet_name(m), Kit.count(settings["decay"], "minute"),
                    Kit.count(settings["bones"], "minute")), Kit.HUE_BAD)
                if settings["ping"]: st["ping"] = (x, y, m, now + PING_TRY)
            if settings["restore"]: show_full()
        CORPSE_PREFIXES = ("a corpse of ", "corpse of ", "the remains of ", "remains of ")
        def owner_name():
            r = st["rec"]; return ((r["name"] if r is not None and r["name"] else st["name"]) or "").strip().lower()
        def mine(it, graphic, me_name):
            r = st["rec"]; body = r["body"] if r is not None else 0; amt = int(it.Amount or 0)
            if body and amt and amt != body: return 0
            bones = BONES_FIRST <= graphic <= BONES_LAST
            if bones and (not amt or (not body and amt not in HUMAN_BODIES)): return 0
            n = (str(it.Name or "") or str(it.NameAndProps(False) or "")).strip().lower(); owner = None
            for p in CORPSE_PREFIXES:
                if n.startswith(p): owner = n[len(p):].strip(); break
            if owner is None:
                if not n or n in ("corpse", "a corpse", "bones", "remains") or bones: return 1
                owner = n
            if not me_name: return 1
            return 2 if owner == me_name else 0
        def scan_corpses(items, cx, cy, lim, acc, me_name):
            for it, gr in items:
                s, ix, iy = int(it.Serial), int(it.X), int(it.Y); d = max(abs(ix - cx), abs(iy - cy))
                if d > lim: continue
                m = mine(it, gr, me_name)
                if m == 1: acc[1] = True
                if m != 2: continue
                e = (d, s, ix, iy); b = acc[0]
                if b is None or d < b[0] or (d == b[0] and s > b[1]): acc[0] = e
        def find_corpse(me):
            r = st["rec"]; me_name = owner_name()
            cx, cy, lim = (r["x"], r["y"], 3) if r["spot"] else (int(me.X), int(me.Y), SEEK_RANGE); acc = [None, False]
            corpses, bones = [], []
            for it in API.GetItemsOnGround(SEEK_RANGE) or ():
                g = int(it.Graphic)
                if g == CORPSE_GRAPHIC: corpses.append((it, g))
                elif BONES_FIRST <= g <= BONES_LAST: bones.append((it, g))
            scan_corpses(corpses, cx, cy, lim, acc, me_name)
            if acc[0] is None: scan_corpses(bones, cx, cy, lim, acc, me_name)
            return (None if acc[0] is None else acc[0][1:]), acc[1]
        def forget(why=None):
            if st["job"] is not None: stop_job(None)
            st["rec"] = st["ping"] = st["gone_since"] = None; st["unnamed"] = False; st["refused"] = set()
            Kit.drop_arrow(st, ARROW_ID); save_rec()
            if why: say(why)
            st["lbl_at"] = 0.0
        def corpse_tick(me, now, mm):
            r = st["rec"]; left = remaining(now); dist = max(abs(int(me.X) - r["x"]), abs(int(me.Y) - r["y"]))
            if not r["serial"]:
                near = r["spot"] and mm == r["facet"] and dist <= 12
                offered = not r["spot"] and st["unnamed"]; seeking = now < st["seek_until"]
                if (seeking and now >= st["seek_at"]) or (not seeking and (near or offered) and now >= st["look_at"]):
                    st["seek_at"] = now + 0.5; st["look_at"] = now + 1.0; st["find_at"] = now
                    hit, unnamed = find_corpse(me)
                    if hit is not None:
                        r["serial"], r["x"], r["y"] = hit; st["unnamed"] = False
                        if not r["name"]: r["name"] = owner_name()
                        if not r["spot"]: r["spot"] = True; say("found your corpse at %d, %d." % (r["x"], r["y"]))
                        save_rec(); st["lbl_at"] = 0.0
                    elif unnamed != st["unnamed"]: st["unnamed"] = unnamed; st["lbl_at"] = 0.0
                if (not r["serial"] and not r["spot"] and now >= st["seek_until"] and not st["unnamed"]):
                    forget("your corpse isn't in view (it was left before %s started)." % TITLE); return
            elif now >= st["item_at"] or st["item_at"] - now > ITEM_EVERY:
                st["item_at"] = now + ITEM_EVERY; it = item_of(r["serial"])
                if it is not None:
                    st["gone_since"] = None; ix, iy = int(it.X), int(it.Y)
                    if (ix or iy) and (ix, iy) != (r["x"], r["y"]) and not int(it.Container or 0):
                        r["x"], r["y"] = ix, iy; save_rec()
                elif mm == r["facet"] and st["job"] is None and dist <= 12:
                    if st["gone_since"] is None: st["gone_since"] = now
                    elif now - st["gone_since"] >= 6.0:
                        forget("your corpse isn't at %d, %d any more (decayed or looted)." % (r["x"], r["y"])); return
                else: st["gone_since"] = None
            if left <= 60 and not st["warned"] and left > 0:
                st["warned"] = True
                where = Kit.where_text(r["x"] - int(me.X), r["y"] - int(me.Y)) if mm == r["facet"] else \
                    "on " + Kit.facet_name(r["facet"])
                HOST.alert(ALERT_DECAY, "Corpse decays in under a minute (%s)" % where, "warn")
            if left <= -DECAYED_GRACE and item_of(r["serial"]) is None: forget("your corpse has decayed.")
        def ping_tick(now):
            p = st["ping"]
            if p is None: return
            x, y, m, until = p; fn = HOST.services.get("pings.send")
            if fn is None or now > until:
                st["ping"] = None
                if fn is None: say("World Map > Map Pings is off, so no Need help ping was sent.")
                return
            try: ok = fn(x, y, m=m, kind="help", quiet=True)
            except Exception: st["ping"] = None; return
            if ok: st["ping"] = None; say("Need help ping sent on your corpse." if ok is True else
                                          "Need help ping shown only to you (Map Pings isn't connected).")
        def start_job(me, now):
            r = st["rec"]
            if st["job"] is not None: return
            if r is None: note("No corpse remembered."); return
            if bool(st["was_dead"]): note("You are still a ghost: get resurrected first."); return
            spot = (r["x"], r["y"])
            if not r["serial"]: note("Your corpse hasn't been seen yet: go to %d, %d." % spot, spot=spot); return
            it = item_of(r["serial"])
            if it is None: note("Your corpse isn't in view yet (%d, %d)." % spot, spot=spot); return
            whose = mine(it, int(it.Graphic), owner_name())
            if whose == 1: note("Waiting for the corpse's name: click it once."); return
            if whose != 2: note("That corpse isn't yours."); return
            dx, dy = int(it.X) - int(me.X), int(it.Y) - int(me.Y)
            if max(abs(dx), abs(dy)) > REACH:
                note("Walk up to your corpse first (%s)." % Kit.where_text(dx, dy)); return
            pack = int(API.Backpack or 0)
            if not pack: note("No backpack to put things in."); return
            if cursor_up(): note("A target cursor is up: finish or cancel it first."); return
            if held_item(): note("You are holding an item: put it down first."); return
            st["job"] = {"phase": "open", "corpse": r["serial"], "pack": pack, "at": now + 1.0,
                         "until": now + 3.0, "plan": [], "i": 0, "tried": set(), "waits": {},
                         "move": None, "check": None, "sent_at": 0.0, "last": 0, "rechecks": 0,
                         "hold": 0.0, "moved": 0, "refused": 0, "streak": 0, "why": None, "replans": 0, "opened": False}
            API.UseObject(r["serial"]); st["note"] = ""; st["lbl_at"] = 0.0
        def make_plan(j):
            plan = []
            for it in API.ItemsInContainer(j["corpse"], False) or ():
                if len(plan) >= PLAN_CAP: break
                s = int(it.Serial)
                if s not in j["tried"] and s not in st["refused"] and not is_hair(it): plan.append(s)
            return plan
        def job_tick(me, now):
            j = st["job"]
            if j["why"]: stop_job(j["why"]); return
            if j["move"] is not None: return
            if st["was_dead"]: stop_job("you died"); return
            it = item_of(j["corpse"])
            if it is None: stop_job("your corpse is gone from view"); return
            if max(abs(int(it.X) - int(me.X)), abs(int(it.Y) - int(me.Y))) > REACH:
                stop_job("you walked away from your corpse"); return
            if j["check"] is not None and (now < j["at"] or not check_move(j, now)): return
            if j["phase"] == "open":
                if now < j["at"]: return
                plan = make_plan(j)
                if not plan and now < j["until"]: return
                if not plan and Journal.find(j["until"] - 3.0, J_WAIT) is not None:
                    stop_job("the server said to wait; click Get my things again"); return
                if not plan and not (j["opened"] or it.Opened):
                    stop_job("your corpse didn't open; click Get my things again"); return
                j["plan"], j["i"], j["phase"] = plan, 0, "move"
                if not plan: finish_job(); return
            if now < j["hold"]: return
            if cursor_up(): stop_job("a target cursor is up"); return
            h = held_item()
            if h and h != j["last"]: stop_job("you picked something up"); return
            plan = j["plan"]
            while j["i"] < len(plan):
                s = plan[j["i"]]; j["i"] += 1
                if s in j["tried"]: continue
                x = item_of(s)
                if x is None or int(x.Container or 0) != j["corpse"]: continue
                wmax, wnow = int(me.WeightMax or 0), int(me.Weight or 0)
                if wmax > 0 and (wnow >= wmax or wnow + weight_of(x) > wmax):
                    stop_job("the next item would put you over your weight limit (%d / %d stones)" % (wnow, wmax))
                    return
                j["tried"].add(s); j["move"] = s; return
            if j["replans"] < 2:
                j["replans"] += 1; more = make_plan(j)
                if more: j["plan"], j["i"] = more, 0; return
            finish_job()
        def check_move(j, now):
            s = j["check"]; it = item_of(s); where = int(it.Container or 0) if it is not None else None
            if where is None and j["rechecks"] < MOVE_RECHECK:
                j["rechecks"] += 1; j["at"] = now + MOVE_GAP * 0.5; return False
            if where != j["corpse"]: j["moved"] += 1; j["streak"] = j["rechecks"] = 0; j["check"] = None; return True
            if (Journal.find(j["sent_at"], J_WAIT) is not None and j["waits"].get(s, 0) < 2):
                j["waits"][s] = j["waits"].get(s, 0) + 1; j["tried"].discard(s); j["i"] = max(0, j["i"] - 1)
                j["check"] = None; j["rechecks"] = 0; j["hold"] = now + MOVE_GAP; return False
            if j["rechecks"] < MOVE_RECHECK: j["rechecks"] += 1; j["at"] = now + MOVE_GAP * 0.5; return False
            j["check"] = None; j["rechecks"] = 0; j["refused"] += 1; j["streak"] += 1
            if len(st["refused"]) < PLAN_CAP: st["refused"].add(s)
            if j["streak"] >= 3: stop_job("%d moves in a row were refused" % j["streak"]); return False
            return True
        def send_move():
            j = st["job"]
            if j is None or j["move"] is None or st["shutting"]: return
            mv = j["move"]; j["move"] = None
            try: API.MoveItem(mv, j["pack"])
            except Exception as ex: j["why"] = "a move failed (%s)" % ex; return
            j["check"] = mv; j["last"] = mv; j["sent_at"] = time.time(); j["at"] = j["sent_at"] + MOVE_GAP
        def finish_job():
            j, st["job"] = st["job"], None
            if j is None: return
            left = []
            if item_of(j["corpse"]) is not None: left = make_plan({"corpse": j["corpse"], "tried": set()})
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
                st["lbl_at"] = 0.0; return
            forget(None); say("%s. Re-dress when you are ready." % msg, Kit.HUE_BAD if j["refused"] else Kit.HUE_GOOD)
        def stop_job(why=None, user=False):
            j, st["job"] = st["job"], None
            if j is None: return
            if user: say("stopped (%d moved)." % j["moved"])
            elif why: say("stopped: %s (%d moved)." % (why, j["moved"]), Kit.HUE_BAD)
            st["lbl_at"] = 0.0
        def act_go(me, now):
            if st["job"] is not None: stop_job(None, user=True)
            elif me is not None: start_job(me, now)
        def act_help(me, now):
            r = st["rec"]
            if r is None or not r["spot"]: note("No corpse to ping.")
            elif HOST.services.get("pings.send") is None:
                note("World Map > Map Pings is off: turn it on to send pings.")
            else: st["ping"] = (r["x"], r["y"], r["facet"], now + PING_TRY)
        def act_forget(me, now):
            if st["rec"] is None: note("No corpse remembered.")
            else: forget("forgot your corpse.")
        ACTIONS = {"go": act_go, "help": act_help, "forget": act_forget}
        MOVE_HINT = ("One item every %.1f s; stops on Stop, a target cursor, picking something up, walking away or "
                     "going over your weight limit." % MOVE_GAP)
        def page_table(w):
            t1 = "Corpse to bones:"
            return (("WHEN YOU DIE", (
                        ("check", "arrow", "Point the tracking arrow at your corpse", "Its own arrow (others are left "
                         "alone); hidden when you stand beside it"),
                        ("check", "restore", "Open the Corpse window on death, even minimized or folded",
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
            now = time.time()
            for k in ("decay", "bones"):
                try: txt = str(f.c[k].Text or "").strip()
                except Exception: continue
                t = typed.get(k)
                if t is None or t[0] != txt: typed[k] = (txt, now)
                if not cfg.force and (t is None or t[0] != txt or now - t[1] < 1.0): new[k] = settings[k]
        def on_change(old, new):
            if (new["decay"], new["bones"]) != (old["decay"], old["bones"]): st["warned"] = False
            st["lbl_at"] = 0.0
            if not new["arrow"]: Kit.drop_arrow(st, ARROW_ID)
        cfg = Kit.Page(settings, page_table, save_settings, on_change, adjust=settle, final=True)
        def config_closed(): cfg.closed(); typed.clear()
        def on_corpse(*args):
            r = st["rec"]
            if r is None or r["serial"] or st["shutting"]: return
            soon = st["find_at"] + POKE_GAP; st["seek_at"] = min(st["seek_at"], soon)
            st["look_at"] = min(st["look_at"], soon)
        def on_died(*args):
            if st["shutting"]: return
            st["died"] = True; HOST.poke("worldmap.corpse", False)
        def on_open(*args):
            j = st["job"]
            if j is None: return
            for a in args:
                try: s = int(a.Serial)
                except AttributeError:
                    try: s = int(a)
                    except Exception: continue
                except Exception: continue
                if s == j["corpse"]: j["opened"] = True; return
        def rebase(d):
            for k in ("body_at", "seek_until", "seek_at", "look_at", "item_at", "lbl_at", "note_until", "find_at",
                      "died_at"):
                st[k] = st[k] + d
            if st["gone_since"] is not None: st["gone_since"] += d
            p = st["ping"]
            if p is not None: st["ping"] = (p[0], p[1], p[2], p[3] + d)
            j = st["job"]
            if j is not None:
                for k in ("at", "until", "sent_at", "hold"): j[k] += d
            r = st["rec"]
            if r is not None: r["died"] += d; save_rec()
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "job": None, "arrow": None, "refused": set(),
                       "ping": None, "was_dead": None, "seek_until": 0.0, "seek_at": 0.0,
                       "look_at": 0.0, "gone_since": None, "item_at": 0.0, "lbl_at": 0.0, "note": "",
                       "last_now": None, "atlas": False, "unnamed": False, "died": False, "died_at": 0.0,
                       "minimized": wnd.start_min()})
            load_settings(); st["rec"] = load_rec(); st["warned"] = False
            if st["rec"] is not None and remaining(time.time()) <= -DECAYED_GRACE: st["rec"] = None; save_rec()
            if st["rec"] is not None and not st["rec"]["spot"]: st["seek_until"] = time.time() + FIND_SECS
            HOST.alert_kind(ALERT_DECAY, "Corpse about to decay", 0x1EA); build_window()
            wnd.dock(fit=True, min=(W, H))
            Kit.hook_once(st, "hooked", ("OnCorpseCreated", on_corpse), ("OnPlayerDeath", on_died),
                          ("OnOpenContainer", on_open))
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            now = time.time(); last, st["last_now"] = st["last_now"], now
            if last is not None and now < last - 2.0: rebase(now - last)
            me = HOST.me()
            while st["queue"]:
                action = st["queue"].pop(0)
                if not wnd.action(action): ACTIONS[action](me, now)
            if me is None: return
            dead = bool(me.IsDead); was = st["was_dead"]; st["was_dead"] = dead; died = st["died"]; st["died"] = False
            if died and not was: on_death(me, now); st["died_at"] = 0.0 if dead else now
            elif was is None:
                if dead and st["rec"] is None: on_death(me, now, at_start=True)
            elif dead and not was:
                if not 0.0 <= now - st["died_at"] <= DIED_HOLD: on_death(me, now)
                st["died_at"] = 0.0
            elif was and not dead and st["rec"] is not None:
                r = st["rec"]
                if r["spot"]:
                    say("you are alive. Your corpse is %s: click Get my things beside it."
                        % Kit.where_text(r["x"] - int(me.X), r["y"] - int(me.Y)), Kit.HUE_GOOD)
                st["lbl_at"] = 0.0
            if not dead and now >= st["body_at"]:
                st["body_at"] = now + 2.0; st["body"] = int(me.Graphic); st["name"] = str(me.Name or "") or st["name"]
            if not st["name"]: st["name"] = str(me.Name or "")
            mm = int(API.GetMap()) if st["rec"] is not None or st["arrow"] is not None else None
            if st["rec"] is not None: corpse_tick(me, now, mm)
            if st["job"] is not None: job_tick(me, now); send_move()
            if st["ping"] is not None: ping_tick(now)
            if st["rec"] is not None or st["arrow"] is not None: arrow_tick(me, mm)
            r = st["rec"]; sig = (r["x"], r["y"], r["facet"]) if r is not None and r["spot"] else None
            if sig != st["atlas"]:
                st["atlas"] = sig; cn = atlas_name("Your corpse")
                ATLAS.set("corpse", {} if sig is None else {cn: (sig[0], sig[1], sig[2], "white")})
            refresh(me, now, mm)
        def _interval(): return 0.1 if st["job"] is not None else 0.25
        def _stop():
            st["shutting"] = True; st["job"] = st["ping"] = None; Kit.drop_arrow(st, ARROW_ID); save_settings()
            cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": config_closed,
                "interval": _interval}
    def _part_maps():
        KEY = "treasure"; TITLE = "Treasure Maps"; SETTINGS_KEY = "TreasureHunter_settings"
        POS_KEY = "TreasureHunter_pos"; MIN_KEY = "TreasureHunter_min"; MAPS_KEY = "TreasureHunter_maps"
        MINI_W, MINI_H = 320, 46; ROWS = 8; ROW_H = 24; ARROW_ID = 0x54524541; MAP_GRAPHICS = (0x14EB, 0x14EC)
        LEVELS = ("youthful", "plainly", "expertly", "adeptly", "cleverly", "deviously", "ingeniously")
        LEVEL_NAMES = ["Youthful"] + [v.capitalize() + " drawn" for v in LEVELS[1:]]
        PROP_FACETS = ["somewhere in " + n.lower() for n in Kit.FACETS]
        J_DECODED = "you successfully decode a treasure map"; J_SHOWN = "the treasure is marked by the red pin"
        J_DONE = "this treasure hunt has already been completed"
        J_ESTIMATE = re.compile(r"believe this is somewhere near (\d+) and (\d+)"); TAZ_SCALE = 300.0; SCAN_EVERY = 1.0
        LOOK_FOR = 6.0; LOOK_EVERY = 0.25; USED_KEEP = 8.0; SAVE_EVERY = 5.0; MAX_MAPS = 60; PING_TRY_FOR = 6.0
        PING_RETRY = 0.5; LOOK_TIP = "Point the tracking arrow at this map's spot (again: back to the nearest map)"
        LOOK_TIP_ON = "Send the tracking arrow back to the nearest map's spot"
        LOOK_TIP_MAN = "Point the tracking arrow at this map's spot (again: take it down)"
        PING_TIP = "Send a Go here ping on this map's spot (needs World Map > Map Pings)"
        EMPTY_TEXT = "No treasure maps in your pack: put one in and double-click it once."
        DUG_TIP = "This treasure has been dug up"; settings = {"auto": True, "undecoded": True, "done": False}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "next_look": 0.0, "dirty": False,
              "next_save": 0.0, "list_ver": 0, "me": (0, 0, -1), "hooked": False, "tm_at": 0.0, "tm_serial": 0,
              "hidden": 0, "in_pack": frozenset()}
        spots = {}; parsed = {}; TEXT_EVERY = 5.0; TEXT_ALL = [False]; asked = set(); read_gumps = {}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}; JR = {"rd": None}
        cleanup, queue, say = Kit.basics(st, TITLE); bank_st = {"at": 0.0, "items": []}
        def level_name(lvl): return LEVEL_NAMES[lvl] if 0 <= lvl < len(LEVEL_NAMES) else "Treasure map"
        def map_noun(lvl): return level_name(lvl).lower() + (" map" if 0 <= lvl < len(LEVEL_NAMES) else "")
        def load_settings(): Kit.kv_load(SETTINGS_KEY, ";", settings)
        def save_settings(): Kit.kv_save(SETTINGS_KEY, ";", settings, ("auto", "undecoded", "done"))
        def load_maps():
            spots.clear(); now = int(time.time()); cut = now - 60 * 86400
            for part in Kit.get_var(MAPS_KEY).split(";"):
                b = part.strip().split(",")
                if len(b) < 7: continue
                try:
                    s = int(b[0], 16)
                    rec = {"x": int(b[1]), "y": int(b[2]), "f": int(b[3]), "lvl": int(b[4]),
                           "done": b[5] == "1", "t": int(b[6]), "approx": len(b) > 7 and b[7] == "1",
                           "bank": len(b) > 8 and b[8] == "1"}
                except ValueError: continue
                if not (0 < s < 0x80000000 and 0 < rec["x"] < 0x10000 and 0 < rec["y"] < 0x10000
                        and -1 <= rec["f"] < 0x100 and cut <= rec["t"]): continue
                rec["t"] = min(rec["t"], now)
                if not 0 <= rec["lvl"] < len(LEVELS): rec["lvl"] = -1
                spots[s] = rec
            cap_spots()
        def cap_spots():
            if len(spots) > MAX_MAPS:
                old = sorted(spots, key=lambda s: spots[s]["t"])
                for s in old[:len(spots) - MAX_MAPS]: del spots[s]
        def save_maps():
            st["dirty"] = False
            Kit.put_var(MAPS_KEY, ";".join("%X,%d,%d,%d,%d,%d,%d,%d,%d" % (s, r["x"], r["y"], r["f"], r["lvl"],
                        1 if r["done"] else 0, r["t"], 1 if r.get("approx") else 0, 1 if r.get("bank") else 0)
                        for s, r in sorted(spots.items())))
        def parse(text):
            low = text.lower(); name = low.split("\n", 1)[0]
            info = {"tm": "treasure map" in low, "lvl": -1, "dec": None, "f": -1, "done": "completed by" in low}
            for lvl, word in enumerate(LEVELS):
                if word in name: info["lvl"] = lvl; break
            if info["tm"]: info["dec"] = "tattered" not in name
            for f, t in enumerate(PROP_FACETS):
                if t in low: info["f"] = f; break
            return info
        def info_of(serial, it, now=None):
            hit = parsed.get(serial)
            if now is not None and hit is not None and now < hit[2] <= now + TEXT_EVERY: return hit[1]
            if now is None: now = time.time()
            text = str(API.ItemNameAndProps(serial, False) or ""); again = now + TEXT_EVERY
            if not text.strip():
                again = 0.0; text = str(it.Name or "")
                if serial not in asked:
                    asked.add(serial)
                    if len(asked) > 500: asked.clear()
                    API.RequestOPLData([serial])
            if hit is not None and hit[0] == text: parsed[serial] = (text, hit[1], again); return hit[1]
            info = parse(text)
            if len(parsed) > 300: parsed.clear()
            parsed[serial] = (text, info, again); return info
        def solve(est, end, p, size):
            if None in (end, p, size): return est, None
            p, size = float(p), float(size)
            if size <= 0 or p < 0 or p > size: return est, None
            k = 1.0 - p / TAZ_SCALE; start = None
            if abs(k) >= 0.001:
                base = p * end / TAZ_SCALE; lo, hi = (est - base) / k, (est + 1 - base) / k
                start = int(math.floor((lo + hi) / 2.0))
                if not 0 < end - start <= 8192: start = None
            scale = float(end - start) / size if start is not None and abs(k) >= 0.25 else None
            if abs(size - TAZ_SCALE) < 0.5: return est, scale
            if start is None or abs(1.0 - (p + 0.5) / size) / abs(k) > 2.0: return None, scale
            return int(start + (p + 0.5) * (end - start) / size), scale
        def axis(est, end, p, size, scale=None):
            spot = solve(est, end, p, size)[0]
            if spot is not None: return spot, False
            if scale and None not in (end, p, size): return int(end - (float(size) - float(p) - 0.5) * scale), False
            return est, True
        def num(obj, name):
            v = Typing._get(obj, name)
            if v is None: return None
            try: return int(v)
            except Exception: return None
        def look_gumps():
            Typing._find(); uim = Typing.uim
            if uim is None: return None
            gumps = Typing._get(None, "Gumps", uim)
            if gumps is None: return None
            n = 0
            try:
                for g in gumps:
                    if str(g.GetType().Name) != "MapGump": continue
                    r = read_gump(g)
                    if r is None: return None
                    n += r
            except Exception: return None
            return n
        def read_gump(g):
            serial = num(g, "LocalSerial")
            if not serial: return 0
            if Typing._get(g, "IsDisposed", default=False): return 0
            if read_gumps.get(serial) is g: return 0
            found = Typing._get(g, "foundMapLoc")
            if found is None: return None
            if not found: return 0
            est_x, est_y = num(g, "mapX"), num(g, "mapY")
            if est_x is None or est_y is None: return None
            end_x, end_y, mf = num(g, "mapEndX"), num(g, "mapEndY"), num(g, "mapFacet"); hit = Typing._get(g, "_hit")
            size_w = num(hit, "Width") if hit is not None else None
            size_h = num(hit, "Height") if hit is not None else None; px = py = None
            pins = Typing._get(g, "_container")
            try:
                if pins is not None and int(pins.Count) > 0:
                    pin = pins[0]; pw, ph = num(pin, "Width"), num(pin, "Height"); x0, y0 = num(pin, "X"), num(pin, "Y")
                    if None not in (pw, ph, x0, y0): px, py = x0 - pw - 5, y0 - ph
            except Exception: px = py = None
            if len(read_gumps) > 50: read_gumps.clear()
            read_gumps[serial] = g; sx = solve(est_x, end_x, px, size_w)[1]; sy = solve(est_y, end_y, py, size_h)[1]
            x, ax = axis(est_x, end_x, px, size_w, sy); y, ay = axis(est_y, end_y, py, size_h, sx)
            if x is None or y is None or x <= 0 or y <= 0: return 0
            record(serial, x, y, mf if mf is not None and mf > 0 else -1, ax or ay); return 1
        def record(serial, x, y, mf, approx=False):
            it = API.FindItem(serial); info = info_of(serial, it) if it is not None else {}; now = time.time()
            hinted = 0 <= now - st["tm_at"] <= LOOK_FOR and (st["tm_serial"] == serial
                or (not st["tm_serial"] and now - st["tm_at"] <= 1.5))
            if not (info.get("tm") or serial in spots or hinted): return False
            f = mf if mf >= 0 else info.get("f", -1)
            if f < 0: f = int(API.GetMap())
            old = spots.get(serial); lvl = info.get("lvl", -1)
            if lvl < 0 and old is not None: lvl = old["lvl"]
            rec = {"x": int(x), "y": int(y), "f": int(f), "lvl": lvl,
                   "done": bool(info.get("done") or (old is not None and old["done"])),
                   "t": int(time.time()), "approx": bool(approx)}
            same = (old is not None and (old["x"], old["y"], old["f"]) == (rec["x"], rec["y"], rec["f"]))
            spots[serial] = rec; cap_spots(); st["dirty"] = True; st["next_scan"] = 0.0
            if not same:
                st["arrow_off"] = False; mx, my, mf2 = st["me"]
                where = (", " + Kit.where_text(rec["x"] - mx, rec["y"] - my, "here")) if mf2 == rec["f"] and mx > 0 \
                    else ""
                say("%s%s: dig at %s%d, %d in %s%s." % (map_noun(lvl), (" (level %d)" % lvl) if lvl >= 0 else "",
                    "about " if rec["approx"] else "", rec["x"], rec["y"], Kit.facet_name(rec["f"]), where),
                    Kit.HUE_GOOD)
            return True
        def arm_look(now): st["look_until"] = now + LOOK_FOR; st["next_look"] = 0.0
        def on_used(*args):
            if not st["active"]: return
            for a in args:
                try: s = int(a)
                except Exception: continue
                if s > 0 and len(st["used"]) < 20: st["used"].append(s)
                return
        def hook_events(): Kit.hook_once(st, "hooked", ("ObjectUsed", on_used))
        def handle_used(now):
            used, st["used"] = st["used"], []
            for s in used:
                it = API.FindItem(s)
                if it is not None and int(it.Graphic) in MAP_GRAPHICS: st["last_map"] = (s, now); arm_look(now)
        def handle_journal(now):
            rd = JR["rd"]
            if rd is None: return
            own = TITLE.lower() + ":"
            for ln in rd.new():
                low = ln.low
                if "somewhere near" in low: kind = 1
                elif J_SHOWN in low or J_DECODED in low: kind = 2
                elif J_DONE in low: kind = 3
                else: continue
                if low.startswith(own): continue
                name = (ln.name or "").strip().lower()
                if name and name != "system": continue
                if kind == 1:
                    m = J_ESTIMATE.search(low)
                    if m: st["est"] = (int(m.group(1)), int(m.group(2)), now); arm_look(now)
                elif kind == 2:
                    s, t = st["last_map"]; st["tm_at"] = now
                    st["tm_serial"] = s if s and 0 <= now - t <= USED_KEEP else 0; TEXT_ALL[0] = True; arm_look(now)
                else:
                    s, t = st["last_map"]; TEXT_ALL[0] = True
                    if s and 0 <= now - t <= USED_KEEP and s in spots and not spots[s]["done"]:
                        spots[s]["done"] = True; st["dirty"] = True; st["next_scan"] = 0.0
        def look_step(now):
            if not (now < st["look_until"] <= now + LOOK_FOR + 1.0):
                if st["look_until"] > now + LOOK_FOR + 1.0: st["look_until"] = now + LOOK_FOR; return
                if st["est"] is not None: fallback()
                if read_gumps: read_gumps.clear()
                return
            if now < st["next_look"] <= now + LOOK_EVERY: return
            st["next_look"] = now + LOOK_EVERY; n = look_gumps()
            if n is None:
                est, used = st["est"], st["last_map"]
                if est is not None and used[0] and -2.0 <= est[2] - used[1] <= USED_KEEP: fallback()
            elif n > 0: st["est"] = None; st["look_until"] = min(st["look_until"], now + 1.0)
        def fallback():
            x, y, te = st["est"]; st["est"] = None; s, tu = st["last_map"]
            if not s or not (-2.0 <= te - tu <= USED_KEEP) or x <= 0 or y <= 0: return
            st["last_map"] = (0, 0.0); record(s, x, y, -1)
        def scan(now):
            try: me = API.Player; mx, my = int(me.X), int(me.Y); fac = int(API.GetMap())
            except Exception: return
            st["me"] = (mx, my, fac)
            if not int(API.Backpack or 0): st["in_pack"] = None; return
            found = [it for it in HOST.pack_items(True, 0.5) if int(it.Graphic) in MAP_GRAPHICS]
            bank = bank_maps(now); banked = set([int(it.Serial) for it in bank])
            found.extend(bank); out, seen = [], set(); hidden = 0; day = int(time.time())
            tnow = None if TEXT_ALL[0] else time.time(); TEXT_ALL[0] = False
            for it in found:
                s = int(it.Serial)
                if s in seen: continue
                seen.add(s)
                if len(out) >= 100: continue
                info = info_of(s, it, tnow); rec = spots.get(s)
                if not info["tm"] and rec is None: continue
                lvl = info["lvl"] if info["lvl"] >= 0 else (rec["lvl"] if rec else -1)
                done = bool(info["done"] or (rec is not None and rec["done"]))
                if rec is not None:
                    if info["f"] >= 0 and rec["f"] != info["f"]: rec["f"] = info["f"]; st["dirty"] = True
                    if lvl != rec["lvl"] or done != rec["done"]: rec["lvl"], rec["done"] = lvl, done; st["dirty"] = True
                    if day - rec["t"] > 86400: rec["t"] = day; st["dirty"] = True
                    if rec.get("bank", False) != (s in banked): rec["bank"] = s in banked; st["dirty"] = True
                dec = True if rec is not None else info["dec"]
                e = {"serial": s, "lvl": lvl, "dec": dec, "done": done, "x": None, "y": None,
                     "f": -1, "dist": None, "group": 3, "bank": s in banked}
                if rec is not None:
                    e["x"], e["y"], e["f"] = rec["x"], rec["y"], rec["f"]; e["approx"] = rec.get("approx", False)
                    if e["f"] == fac:
                        e["dist"] = max(abs(rec["x"] - mx), abs(rec["y"] - my))
                        e["dir"] = Kit.compass(rec["x"] - mx, rec["y"] - my); e["group"] = 0
                    else: e["group"] = 1
                elif dec: e["group"] = 2
                if done:
                    e["group"] = 4
                    if not settings["done"]: hidden += 1; continue
                elif not dec and not settings["undecoded"]: hidden += 1; continue
                e["where"], e["hue"], e["tip"] = where_of(e, fac)
                if e["bank"]: e["where"] = "in the bank: " + e["where"]
                out.append(e)
            out.sort(key=sort_key); st["list"] = out; st["in_pack"] = seen
            if st["pin"] and st["pin"] not in seen: st["pin"] = 0
            sig = (tuple((e["serial"], e["lvl"], e["dec"], e["done"], e["where"]) for e in out) + (hidden,))
            st["hidden"] = hidden
            if sig != st["list_sig"]: st["list_sig"] = sig; st["list_ver"] += 1
        def bank_maps(now):
            if now - bank_st["at"] < 5.0 and now >= bank_st["at"]: return bank_st["items"]
            b = int(API.Bank or 0); bank_st["at"] = now; bank_st["items"] = []
            if b and bank_open(b):
                bank_st["items"] = [it for it in contents(b, 2000) if int(it.Graphic) in MAP_GRAPHICS]
            return bank_st["items"]
        def bank_open(bank):
            with Kit.quiet:
                for g in Tz.windows(("ContainerGump", "GridContainer")):
                    if int(g.LocalSerial) == bank: return True
            return False
        def dig_tiles(keep):
            want = set((int(e["x"]), int(e["y"]), int(e["f"])) for e in keep)
            for t in (st["dig_tiles"] | st["dig_stale"]) - want: API.RemoveMarkedTile(t[0], t[1], t[2])
            for t in want - st["dig_tiles"]: API.MarkTile(t[0], t[1], 0x0035, t[2])
            st["dig_tiles"] = want; st["dig_stale"] = set()
        def sort_key(e): return (e["group"], e["dist"] if e["dist"] is not None else 0, e["lvl"], e["serial"])
        def atlas_publish():
            keep = [e for e in st["list"] if not (e["x"] is None or e["done"] or e["f"] < 0)]
            sig = tuple((e["serial"], e["x"], e["y"], e["f"], e["lvl"]) for e in keep)
            if sig == st["atlas_sig"]: return
            st["atlas_sig"] = sig; dig_tiles(keep)
            ATLAS.set("maps", {atlas_name(("Dig L%d #%X" % (e["lvl"], e["serial"])) if e["lvl"] >= 0
                                          else ("Dig #%X" % e["serial"])):
                               (int(e["x"]), int(e["y"]), int(e["f"]), "yellow") for e in keep})
        def where_of(e, fac):
            if e["x"] is not None:
                spot = ("about " if e.get("approx") else "") + xy(e["x"], e["y"], "(%d, %d)")
                if e["done"]: return "dug up  " + spot, Kit.HUE_INFO, DUG_TIP
                if e["f"] == fac:
                    d = e["dist"]
                    if d == 0: return "here  " + spot, Kit.HUE_GOOD, LOOK_TIP
                    return ("%s %s  %s" % (Kit.count(d, "tile"), e["dir"], spot), Kit.HUE_TEXT, LOOK_TIP)
                return ("in %s  %s" % (Kit.facet_name(e["f"]), spot), Kit.HUE_INFO,
                        "This map's spot is in %s; you are in %s" % (Kit.facet_name(e["f"]), Kit.facet_name(fac)))
            if e["done"]: return "dug up", Kit.HUE_INFO, DUG_TIP
            if e["dec"]:
                return "open the map once to read its spot", Kit.HUE_INFO, "Double-click the map once to read it"
            if e["dec"] is None: return "open the map to read it", Kit.HUE_INFO, "Double-click the map to read it"
            return "not decoded yet", Kit.HUE_INFO, "Double-click the map to decode it (Cartography)"
        def entry(serial): return next((e for e in st["list"] if e["serial"] == serial), None)
        def arrow_target():
            if st["arrow_off"]: return None
            fac = st["me"][2]
            if st["pin"]:
                e = entry(st["pin"])
                if e is not None and e["x"] is not None and e["f"] == fac and not e["done"]:
                    return (e["x"], e["y"], e["serial"])
            if settings["auto"]:
                for e in st["list"]:
                    if e["group"] == 0: return (e["x"], e["y"], e["serial"])
            return None
        def update_arrow(force_off=False, force=False):
            want = None if force_off else arrow_target(); cur = st["arrow"]
            if not force and (want[:2] if want else None) == (cur[:2] if cur else None): st["arrow"] = want; return
            if want is None: API.TrackingArrow(-1, -1, ARROW_ID)
            else: API.TrackingArrow(want[0], want[1], ARROW_ID); st["arrow_at"] = time.time()
            st["arrow"] = want
        def arrow_closed(now):
            if st["arrow"] is None: return
            age = now - st.get("arrow_at", 0.0)
            if age < 0: st["arrow_at"] = now; return
            if age < 1.5 or arrow_open(ARROW_ID): return
            st["arrow"], st["arrow_off"], st["pin"] = None, True, 0
        def build_window():
            z = told(wnd, st, 560, list_h(1, ROW_H)); w, h = z if z else (560, list_h(ROWS, ROW_H))
            n = wnd.rows(ROW_H, list_h(0, ROW_H), ROWS) if z else ROWS; g, store, c = wnd.begin(w, h); rows = []
            if not st["minimized"]:
                wnd.frame(g); M = Kit.MARGIN; IW = w - 2 * M; yt = M + 30 + Kit.GAP; Kit.add_section(g, M, yt, IW, 36)
                right = M + IW - 8
                Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 22, yt + 8, None,
                               "Next page", on_click=queue(("page", 1)))
                Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 46, yt + 8, None,
                               "Previous page", on_click=queue(("page", -1)))
                xpg = right - 52 - Kit.text_w("100/100"); c["pg"] = Kit.add_label(g, "", xpg, yt + 10, Kit.HUE_INFO)
                x_off = xpg - 12 - (35 + Kit.text_w("Arrow off"))
                Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, x_off, yt + 7, "Arrow off",
                               "Take the tracking arrow down (a row click or Nearest brings it back)",
                               on_click=queue("arrow_off"))
                x_near = x_off - 12 - (35 + Kit.text_w("Nearest"))
                Kit.art_button(g, store, "nearest", Kit.ART_PLAY, x_near, yt + 7, "Nearest",
                               "Point the tracking arrow at the nearest dig spot on your facet",
                               on_click=queue("nearest"))
                c["status"] = Kit.add_label(g, "", M + 12, yt + 10, Kit.HUE_INFO); c["status_w"] = x_near - 8 - (M + 12)
                yl = yt + 36 + Kit.GAP; Kit.add_section(g, M, yl, IW, h - yl - M); x_lvl = M + 12
                x_name = x_lvl + max(34, Kit.text_w("Level")) + 8; x_where = x_name + 150 + 8; x_ping = M + IW - 12 - 22
                Kit.add_label(g, "Level", x_lvl, yl + 6, Kit.HUE_TITLE)
                Kit.add_label(g, "Map", x_name, yl + 6, Kit.HUE_TITLE)
                Kit.add_label(g, "Dig spot", x_where, yl + 6, Kit.HUE_TITLE); c["where_w"] = x_ping - 8 - x_where
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
            wnd.end(g, {"rows": rows}); st["drawn"] = None; refresh()
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (240, 180), (MINI_W, MINI_H), 0x14EB,
                         cleanup, lock=True, clear={"rows": []}, docked_min=True)
        def show(ctl, r, key, on):
            if r[key] != on: r[key] = on; Kit.set(ctl, "IsVisible", on)
        def refresh():
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]): return
            arrow = st["arrow"][2] if st["arrow"] else 0
            sig = (st["list_ver"], st["page"], arrow, st["pin"], st["minimized"])
            if sig == st["drawn"]: return
            st["drawn"] = sig; c = win["c"]; lst = st["list"]; near = next((e for e in lst if e["group"] == 0), None)
            n = len(lst); maps = Kit.count(n, "map")
            if near is not None:
                d = near["dist"]; part = ("here" if d == 0 else "%s %s" % (Kit.count(d, "tile"), near["dir"]))
                status = "%s, nearest %s" % (maps, part); mini = "%s, %s" % (maps, part)
            elif n: status = mini = "%s, no spot on this facet" % maps
            elif st["hidden"]:
                status = "No maps listed (%d hidden on the settings page)" % st["hidden"]
                mini = "%d hidden" % st["hidden"]
            else: status = "No treasure maps in your pack"; mini = "no maps"
            if st["minimized"]:
                if c.get("status") is not None:
                    Kit.set_text(c["status"], Kit.fit("%s: %s" % (TITLE, mini), MINI_W - 90))
                return
            rows = win["rows"]; per = max(1, len(rows)); pages = max(1, (n + per - 1) // per)
            if not 0 <= st["page"] < pages:
                st["page"] = max(0, min(pages - 1, st["page"])); st["drawn"] = sig[:1] + (st["page"],) + sig[2:]
            Kit.set_text(c["status"], Kit.fit(status, c.get("status_w", 200)))
            Kit.set_text(c["pg"], ("%d/%d" % (st["page"] + 1, pages)) if pages > 1 else ""); first = st["page"] * per
            where_w = c.get("where_w", 200); now = time.time()
            for k, r in enumerate(rows):
                i = first + k
                if i >= n:
                    Kit.row_set(r, None, now)
                    if k == 0 and n == 0: es = ("empty", EMPTY_TEXT if not st["hidden"] else (status + "."))
                    else: es = ("empty", "")
                    if r["sig"] != es:
                        r["sig"] = es; Kit.set_text(r["lvl"], Kit.fit(es[1], c.get("empty_w", 400)), Kit.HUE_INFO)
                        Kit.set_text(r["name"], ""); Kit.set_text(r["where"], "")
                    show(r["ping"], r, "pvis", False); continue
                e = lst[i]; Kit.row_set(r, (e["serial"],), now); on = arrow == e["serial"]
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
                    if tip == LOOK_TIP:
                        pinned = st["pin"] == e["serial"]
                        if settings["auto"]: tip = LOOK_TIP_ON if pinned else LOOK_TIP
                        else: tip = "Take the tracking arrow down" if pinned else LOOK_TIP_MAN
                    if tip != r["tip"]: r["tip"] = tip; Kit.with_tip(r["catch"], tip)
                show(r["ping"], r, "pvis", e["x"] is not None and not e["done"])
        def do_row(serial):
            e = entry(serial)
            if e is None: return
            if e["x"] is None or e["done"]: say(journal_case(e["tip"]) + "."); return
            if e["f"] != st["me"][2]:
                say("that map's spot is in %s; you are in %s." % (Kit.facet_name(e["f"]), Kit.facet_name(st["me"][2])))
                return
            st["arrow_off"] = False
            if st["pin"] == serial:
                st["pin"] = 0
                if settings["auto"]: say("tracking arrow back on the nearest map.")
                else: st["arrow_off"] = True; say("tracking arrow down.")
            else:
                st["pin"] = serial
                say("tracking arrow on the %s's spot (%d, %d)." % (map_noun(e["lvl"]), e["x"], e["y"]))
            update_arrow(force=True)
        def do_ping(serial, now):
            e = entry(serial)
            if e is None or e["x"] is None: return
            if HOST.services.get("pings.send") is None:
                say("World Map > Map Pings is off; turn it on to send map pings."); return
            st["ping"] = [e["x"], e["y"], e["f"], now + PING_TRY_FOR, 0.0]
        def ping_step(now):
            p = st["ping"]
            if p is None or (now < p[4] <= now + PING_RETRY): return
            fn = HOST.services.get("pings.send")
            if fn is None: st["ping"] = None; say("World Map > Map Pings is off; turn it on to send map pings."); return
            try: ok = bool(fn(p[0], p[1], m=p[2], kind="go"))
            except Exception: ok = True
            if ok: st["ping"] = None
            elif not (now < p[3] <= now + PING_TRY_FOR):
                st["ping"] = None; say("Map Pings didn't take the ping (too soon after the last one); try again.")
            else: p[4] = now + PING_RETRY
        def forget_others():
            here = st["in_pack"]
            if here is None: say("your backpack isn't known yet; nothing was forgotten."); return
            gone = [s for s in spots if s not in here and not spots[s].get("bank")]
            for s in gone: del spots[s]
            st["dirty"] = True; say("forgot %s of maps not in your pack or bank." % Kit.count(len(gone), "spot"))
        def draw_spots(f, x, y):
            Kit.add_label(f.g, "%s remembered" % Kit.count(len(spots), "spot"), x + 12, y + 4, Kit.HUE_INFO)
            Kit.art_button(f.g, f.store, "forget", Kit.ART_CLOSE, x + f.w - 12 - (35 + Kit.text_w("Forget lost maps")),
                           y, "Forget lost maps", "Forget the spots of maps not in your backpack or bank",
                           on_click=queue("forget"))
        def act_page(a, now): st["page"] = max(0, st["page"] + a[1])
        def act_nearest(a, now):
            st["arrow_off"] = False
            if settings["auto"]: st["pin"] = 0
            else:
                near = next((e for e in st["list"] if e["group"] == 0), None)
                st["pin"] = near["serial"] if near is not None else 0
            update_arrow(force=True)
            if st["arrow"] is None: say("no decoded map with a spot on this facet.")
        def act_arrow_off(a, now): st["pin"], st["arrow_off"] = 0, True; update_arrow()
        def act_forget(a, now): forget_others(); HOST.refresh_settings(KEY)
        ACTIONS = {"page": act_page, "row": lambda a, now: do_row(a[1]), "ping": lambda a, now: do_ping(a[1], now),
                   "nearest": act_nearest, "arrow_off": act_arrow_off, "forget": act_forget}
        MAPS_PAGE = (("WINDOW  (open a decoded map once to read it)", (
                    ("check", "auto", "Point the tracking arrow at the nearest map's spot",
                     "With no map picked, the arrow points at the nearest spot on your facet"),
                    ("check", "undecoded", "List maps not decoded yet", "Maps still to decode (Cartography)"),
                    ("check", "done", "List maps already dug up", "Maps whose treasure is dug up"))),
                ("SAVED SPOTS", (("custom", 24, draw_spots),), {"sh": 64}), atlas_page("maps"))
        def page_table(w): return MAPS_PAGE
        def on_change(old, new): st["next_scan"] = 0.0; st["drawn"] = None
        cfg = Kit.Page(settings, page_table, save_settings, on_change)
        def _start():
            st.update({"shutting": False, "active": True, "docked": False, "queue": [], "used": [],
                       "minimized": wnd.start_min(), "list": [], "list_sig": None, "next_scan": 0.0, "arrow": None,
                       "pin": 0, "arrow_at": 0.0, "arrow_off": False, "ping": None, "est": None, "look_until": 0.0,
                       "last_map": (0, 0.0), "drawn": None, "page": 0, "atlas_ver": None,
                       "atlas_sig": None, "dig_tiles": set()})
            load_settings(); load_maps(); read_gumps.clear(); JR["rd"] = Journal.reader()
            st["dig_stale"] = set((r["x"], r["y"], r["f"]) for r in spots.values())
            hook_events(); scan(time.time()); build_window(); wnd.dock(fit=True, min=(560, list_h(1, ROW_H)))
            update_arrow()
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            now = time.time()
            if st["used"]: handle_used(now)
            handle_journal(now); look_step(now); q = st["queue"]
            while q:
                a = q.pop(0); kind = a[0] if isinstance(a, tuple) else a
                if not wnd.action(kind): ACTIONS[kind](a, now)
                if win["g"] is None: return
            if not (now < st["next_scan"] <= now + SCAN_EVERY):
                st["next_scan"] = now + SCAN_EVERY; scan(now); arrow_closed(now); update_arrow()
                if st["list_ver"] != st["atlas_ver"]: st["atlas_ver"] = st["list_ver"]; atlas_publish()
            if st["ping"] is not None: ping_step(now)
            if st["dirty"] and not (now < st["next_save"] <= now + SAVE_EVERY):
                st["next_save"] = now + SAVE_EVERY; save_maps()
            refresh()
        def _interval(): return 0.1 if st["look_until"] > time.time() else 0.2
        def _stop():
            st["shutting"] = True; st["active"] = False; update_arrow(force_off=True); save_settings()
            if st["dirty"]: save_maps()
            JR["rd"] = None; dig_tiles(()); st["used"], st["queue"], st["ping"] = [], [], None; cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed, "interval": _interval}
    def _part_dry():
        KEY = "harvest"; TITLE = "Ore Tracker"; SETTINGS_KEY = "Harvest_settings"; POS_KEY = "Harvest_pos"
        MIN_KEY = "Harvest_min"; KINDS = ("ore", "wood", "fish", "sand")
        KIND_NAME = {"ore": "Ore", "wood": "Wood", "fish": "Fish", "sand": "Sand"}
        KIND_SKILL = {"ore": "mining", "wood": "lumberjacking", "fish": "fishing", "sand": "sand for glassblowing"}
        KIND_HUE = {"ore": 1153, "wood": 68, "fish": 88, "sand": 53}
        DRY_TEXTS = {"there is no metal here to mine.": "ore", "there's not enough wood here to harvest.": "wood",
            "the fish don't seem to be biting here.": "fish", "there is no sand here to mine.": "sand",}
        FAIL_TEXTS = {"you loosen some rocks but fail to find any useable ore.": "ore",
            "you hack at the tree for a while, but fail to produce any useable wood.": "wood",
            "you fish a while, but fail to catch anything.": "fish",
            "you dig for a while but fail to find any of sufficient quality for glassblowing.": "sand",}
        GOT_PREFIXES = (("you dig some ", "ore"), ("you put some logs", "wood"), ("you chop some ", "wood"),
            ("you pull out ", "fish"), ("you carefully dig up sand", "sand"),
            ("your backpack can't hold the sand", "sand"),)
        SHARD_SPEAKERS = ("", "system"); BANK = {"ore": (8, 8), "wood": (4, 3), "fish": (8, 8), "sand": (8, 8)}
        RESPAWN = {"ore": (10, 20), "wood": (20, 30), "fish": (10, 20), "sand": (10, 20)}; GUARDED_RESPAWN_X = 3
        REACH = {"ore": 3, "wood": 3, "fish": 5, "sand": 3}; FIRST_MAX = 300; ROWS = 8; WEIGHT_WARN = 0.85
        WEIGHT_RED = 0.95; WEIGHT_MAX_BASE, WEIGHT_MAX_PER_STR = 40, 3.5; WEIGHT_EVERY = 0.5
        WEIGHT_ALERT = "harvest.weight"; DRAW_EVERY = 1.0
        EXPIRE_EVERY = 1.0; ARROW_ID = 0x48525654; PING_TRY = 6.0; SAVE_EVERY = 5.0
        SPOTS_KEY = "Harvest_spots"; W = 440; MINI_W, MINI_H = 340, 46
        ROW_H = 24
        FACING = {"north": (0, -1), "northeast": (1, -1), "east": (1, 0), "southeast": (1, 1),
                  "south": (0, 1), "southwest": (-1, 1), "west": (-1, 0), "northwest": (-1, -1)}
        ROW_TIP = "Put the tracking arrow on it (again: take it down)"
        PING_TIP = "Send a Look here ping on this spot so others know it is dry (needs World Map > Map Pings)"
        EMPTY_TEXT = "No dry spots yet: spots the shard says ran out show here."
        SECS_MAX = 60.0 * GUARDED_RESPAWN_X * max(hi for _, hi in RESPAWN.values())
        settings = {"ore": True, "wood": True, "fish": True, "sand": True, "alert": True, "keep": True}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "rd": None, "ver": 0,
              "mini_key": None, "w_key": None, "arrow_at": 0.0}; spots = {}; first = {}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}; jobs = []
        cleanup, queue, say = Kit.basics(st, TITLE)
        def load_settings(): Kit.kv_load(SETTINGS_KEY, ";", settings)
        def save_settings(): Kit.kv_save(SETTINGS_KEY, ";", settings, KINDS + ("alert", "keep"))
        def spots_text():
            return ";".join("%s,%d,%d,%d,%d,%d,%d" % (e["kind"], e["m"], e["x"], e["y"], int(e["lo"]), int(e["hi"]),
                                                      1 if e["about"] else 0) for e in spots.values())
        def load_spots():
            spots.clear()
            if not settings["keep"]: return
            now = time.time()
            for part in Kit.get_var(SPOTS_KEY).split(";"):
                b = part.split(",")
                if len(b) < 7 or b[0] not in KINDS: continue
                try: m, x, y, lo, hi = int(b[1]), int(b[2]), int(b[3]), float(b[4]), float(b[5])
                except ValueError: continue
                if not hi - SECS_MAX - 60 <= lo <= hi or hi <= now or hi - now > SECS_MAX + 60: continue
                if not (0 <= m < 0x100 and 0 < x < 0x10000 and 0 < y < 0x10000): continue
                add_spot(b[0], m, x, y, lo, hi, b[6] == "1", now)
            st["ver"] += 1
        def spots_changed():
            st["ver"] += 1
            if settings["keep"]: st["save_due"] = True
        def save_spots_job():
            st["save_due"] = False; st["save_at"] = time.time() + SAVE_EVERY
            Kit.put_var(SPOTS_KEY, spots_text() if settings["keep"] else "")
        def bank_of(kind, m, x, y): bw, bh = BANK[kind]; return (kind, m, x // bw, y // bh)
        def add_spot(kind, m, x, y, lo, hi, about, now):
            key = bank_of(kind, m, x, y); old = spots.get(key)
            spots[key] = {"kind": kind, "m": m, "x": x, "y": y, "lo": lo, "hi": hi, "at": now,
                          "about": about, "key": key}
            if st["arrow"] == key and old is not None and (old["x"], old["y"]) != (x, y):
                API.TrackingArrow(x, y, ARROW_ID); st["arrow_at"] = now
            if len(spots) > 60:
                drop = None
                for k, e in spots.items():
                    if k != key and (drop is None or e["hi"] < spots[drop]["hi"]): drop = k
                if drop is not None:
                    del spots[drop]
                    if st["arrow"] == drop: arrow_off()
            return key
        def respawn_x(): return GUARDED_RESPAWN_X if HOST.guarded() is True else 1
        def note_dry(kind, x, y, m, about, now):
            key = bank_of(kind, m, x, y); lo_m, hi_m = RESPAWN[kind]; x3 = respawn_x()
            lo_m, hi_m = lo_m * x3, hi_m * x3; f = first.pop(key, None); old = spots.get(key)
            if old is not None and old["lo"] > now: lo, hi = old["lo"], old["hi"]
            elif old is not None and old["hi"] > now: lo, hi = now, max(old["hi"], now + hi_m * 60.0)
            elif f is not None and 0 <= now - f < hi_m * 60.0: lo, hi = f + lo_m * 60.0, f + hi_m * 60.0
            else: lo, hi = now, now + hi_m * 60.0
            add_spot(kind, m, x, y, lo, hi, about, now); spots_changed()
        def note_back(kind, x, y, m, got, now):
            key = bank_of(kind, m, x, y)
            if spots.pop(key, None) is not None:
                if st["arrow"] == key: arrow_off()
                spots_changed()
            if got:
                f = first.get(key)
                if f is None or not 0 <= now - f < RESPAWN[kind][1] * 60.0 * respawn_x():
                    if len(first) >= FIRST_MAX:
                        for k in [k for k, t in first.items() if not 0 <= now - t < SECS_MAX]: del first[k]
                        if len(first) >= FIRST_MAX: first.clear()
                    first[key] = now
        def expire(now):
            gone = [k for k, e in spots.items() if e["hi"] <= now or e["at"] - now > 60.0]
            for k in gone:
                del spots[k]
                if st["arrow"] == k: arrow_off()
            if gone: spots_changed()
            a = st["arrow"]
            if a is not None and 1.5 <= now - st["arrow_at"] and not arrow_open(ARROW_ID):
                st["arrow"] = None; st["ver"] += 1; a = None
            if a is not None:
                me = read_me()
                if me is not None and me[2] != a[1]: arrow_off()
        def rebase(d):
            for e in spots.values(): e["lo"] += d; e["hi"] += d; e["at"] += d
            for k in list(first): first[k] += d
            for k in ("w_at", "draw_at", "expire_at", "save_at", "arrow_at"): st[k] = st[k] + d
            p = st["ping"]
            if p is not None: p[3] += d
            if spots: spots_changed()
        def read_me():
            p = API.Player
            if p is None: return None
            me = (int(p.X), int(p.Y), int(API.GetMap()))
            if me[0] <= 0 and me[1] <= 0: return None
            st["me"] = me; return me
        def target_tile(kind, me):
            px, py = me[0], me[1]; p = API.LastTargetPos; x, y = int(p.X), int(p.Y)
            if 0 < x < 0xFFFF and 0 < y < 0xFFFF and max(abs(x - px), abs(y - py)) <= REACH[kind]: return x, y, False
            dx, dy = FACING.get(str(API.Player.Direction or "").strip().lower(), (0, 0)); return px + dx, py + dy, True
        def line_kind(low):
            k = DRY_TEXTS.get(low)
            if k is not None: return "dry", k
            k = FAIL_TEXTS.get(low)
            if k is not None: return "fail", k
            if low.startswith("you"):
                for pre, k in GOT_PREFIXES:
                    if low.startswith(pre): return "got", k
            return None
        def read_journal(now):
            rd = st["rd"]
            if rd is None: return
            for ln in rd.new():
                hit = line_kind(ln.low.strip())
                if hit is None or (ln.name or "").strip().lower() not in SHARD_SPEAKERS: continue
                what, kind = hit
                if what == "dry" and not settings[kind]: continue
                me = read_me()
                if me is None: continue
                x, y, about = target_tile(kind, me)
                if what == "dry": note_dry(kind, x, y, me[2], about, now)
                else: note_back(kind, x, y, me[2], what == "got", now)
        def character_alerts(): s = HOST.by_key.get("character"); return s is not None and bool(s.running)
        def read_weight(now):
            if now < st["w_at"] and st["w_at"] - now <= WEIGHT_EVERY: return
            st["w_at"] = now + WEIGHT_EVERY
            if not settings["alert"] and (win["g"] is None or (st["minimized"] and st["docked"])): return
            p = API.Player
            if p is None: return
            wt, wmax = int(p.Weight), int(p.WeightMax); strength = int(p.Strength) if wmax <= 0 else 0
            if wmax <= 0 and strength > 0: wmax = int(WEIGHT_MAX_BASE + WEIGHT_MAX_PER_STR * strength)
            frac = (float(wt) / wmax) if wmax > 0 else -1.0; st["weight"] = (wt, wmax, frac)
            if frac >= WEIGHT_RED:
                if st["w_armed"]:
                    raised = True
                    if settings["alert"] and not character_alerts():
                        raised = HOST.alert(WEIGHT_ALERT, "Weight %d/%d (%d%%): nearly overloaded"
                                            % (wt, wmax, int(frac * 100)), level="warn", who="weight") is not False
                    if raised: st["w_armed"] = False
            elif 0 <= frac < 0.92: st["w_armed"] = True
        def arrow_off():
            if st["arrow"] is None: return
            st["arrow"] = None; st["ver"] += 1; API.TrackingArrow(-1, -1, ARROW_ID)
        def arrow_to(key):
            e = spots.get(key)
            if e is None: return
            if st["arrow"] == key and arrow_open(ARROW_ID, True): arrow_off(); return
            me = read_me() or st["me"]
            if me is not None and me[2] != e["m"]:
                say("that spot is in %s; you are in %s." % (Kit.facet_name(e["m"]), Kit.facet_name(me[2]))); return
            API.TrackingArrow(e["x"], e["y"], ARROW_ID); st["arrow"], st["arrow_at"] = key, time.time(); st["ver"] += 1
        def ping_spot(key):
            e = spots.get(key)
            if e is None: return
            if HOST.services.get("pings.send") is None: say("turn World Map > Map Pings on to ping a spot."); return
            st["ping"] = [e["x"], e["y"], e["m"], time.time() + PING_TRY, "the dry %s spot (%d, %d)"
                          % (KIND_NAME[e["kind"]].lower(), e["x"], e["y"])]
        def send_ping(now):
            p = st["ping"]
            if p is None: return
            fn = HOST.services.get("pings.send")
            if fn is None or now > p[3] or p[3] - now > PING_TRY + 1.0:
                st["ping"] = None
                say("the ping on %s wasn't sent (%s)."
                    % (p[4], "Map Pings is off" if fn is None else "Map Pings stayed busy"))
                return
            try: ok = fn(p[0], p[1], p[2], "look")
            except Exception: ok = None
            if ok is False: return
            st["ping"] = None
            if ok: say("Look here ping on %s." % p[4], Kit.HUE_GOOD)
            else: say("couldn't send the ping on %s (Map Pings refused it)." % p[4], Kit.HUE_BAD)
        def mins(secs):
            secs = max(0, int(secs))
            if secs < 60: return "%d s" % secs
            return "%d min" % ((secs + 59) // 60)
        def dist_of(e, me):
            if me is None: return 0
            if me[2] != e["m"]: return 1 << 30
            if bank_of(e["kind"], me[2], me[0], me[1]) == e["key"]: return 0
            return max(abs(e["x"] - me[0]), abs(e["y"] - me[1]))
        def where_text(e, me):
            if me is None: return xy(e["x"], e["y"], "(%d, %d)")
            if me[2] != e["m"]: return "in %s" % Kit.facet_name(e["m"])
            if bank_of(e["kind"], me[2], me[0], me[1]) == e["key"]: return "here"
            return ("about " if e["about"] else "") + Kit.where_text(e["x"] - me[0], e["y"] - me[1])
        def back_text(e, now):
            if now < e["lo"]:
                a, b = mins(e["lo"] - now), mins(e["hi"] - now)
                if a.endswith(" min") and b.endswith(" min"): a = a[:-4]
                return "back in %s-%s" % (a, b), Kit.HUE_BAD
            return "back within %s" % mins(e["hi"] - now), Kit.HUE_TITLE
        def row_tip(e, on):
            bw, bh = BANK[e["kind"]]; x0, y0 = (e["x"] // bw) * bw, (e["y"] // bh) * bh
            when = time.strftime("%H:%M", time.localtime(e["hi"]))
            if e["lo"] > e["at"]:
                back = "back between %s and %s" % (time.strftime("%H:%M", time.localtime(e["lo"])), when)
            else: back = "back by %s at the latest" % when
            return "%s ran dry at %s%s: the %dx%d block from %s, %s.  %s" % (
                KIND_NAME[e["kind"]], xy(e["x"], e["y"]), " (about: the tile in front of you)" if e["about"] else "",
                bw, bh, xy(x0, y0), back, "Take the tracking arrow down" if on else ROW_TIP)
        def shown_spots(): return [e for e in spots.values() if settings[e["kind"]]]
        def _by_place(t): return (t[0], t[1])
        def atlas_publish():
            ATLAS.set("dry", {atlas_name("%s dry %d %d" % (KIND_NAME[e["kind"]], e["x"], e["y"])):
                              (int(e["x"]), int(e["y"]), int(e["m"]), "blue")
                              for e in sorted(shown_spots(), key=lambda e: -e["at"])[:15]})
        def full_h(n): return 2 * Kit.MARGIN + 30 + 3 * Kit.GAP + 46 + 36 + 74 + n * ROW_H + 22
        def build_window():
            M = Kit.MARGIN; z = told(wnd, st, W, full_h(1)); w, h = z if z else (W, full_h(ROWS))
            n = wnd.rows(ROW_H, full_h(0), ROWS) if z else ROWS; g, store, c = wnd.begin(w, h); rows = []
            if not st["minimized"]:
                wnd.frame(g); IW = w - 2 * M; yw = M + 30 + Kit.GAP; Kit.add_section(g, M, yw, IW, 46, "WEIGHT")
                c["wtext"] = Kit.add_label(g, "", M + 20 + Kit.text_w("WEIGHT"), yw + 6, Kit.HUE_TEXT)
                Kit.weight_bar(g, c, M + 12, yw + 28, IW - 24); yt = yw + 46 + Kit.GAP
                Kit.add_section(g, M, yt, IW, 36); bx = M + 12
                Kit.art_button(g, store, "clear", Kit.ART_CLOSE, bx, yt + 7, "Clear",
                               "Empty the list of dry spots", on_click=queue("clear"))
                bx += 35 + Kit.text_w("Clear") + 16
                Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, bx, yt + 7, "Arrow off",
                               "Take the tracking arrow down", on_click=queue("arrow_off"))
                yl = yt + 36 + Kit.GAP; Kit.add_section(g, M, yl, IW, h - yl - M, "DRY SPOTS  (nearest first)")
                c["here"] = Kit.add_label(g, "", M + 12, yl + 28, Kit.HUE_INFO); ping_w = 35 + Kit.text_w("Ping")
                xk, xw, xb = M + 12, M + 12 + 52, M + 12 + 52 + 130; xp = M + IW - 6 - ping_w; c["back_w"] = xp - 8 - xb
                yh = yl + 52; Kit.add_label(g, "What", xk, yh, Kit.HUE_TITLE)
                Kit.add_label(g, "Where", xw, yh, Kit.HUE_TITLE); Kit.add_label(g, "When", xb, yh, Kit.HUE_TITLE)
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
                    r["pbtn"] = store[0].get("ping%d" % k); rows.append(r)
                c["more"] = Kit.add_label(g, "", M + 12, yh + 22 + n * ROW_H + 2, Kit.HUE_INFO)
            wnd.end(g, {"rows": rows})
            st["drawn"] = st["mini_drawn"] = st["wdrawn"] = None; st["draw_at"] = 0.0; refresh(time.time())
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, MIN_KEY, (260, 220), (MINI_W, MINI_H), 0x0E86,
                         cleanup, lock=True, clear={"rows": [], "c": {}}, docked_min=True)
        def show_row(r, on):
            if r["vis"] == on: return
            r["vis"] = on
            for n in ("where", "back", "catch", "pbtn", "plbl"): Kit.set(r.get(n), "IsVisible", on)
            if not on: Kit.set_text(r["kind"], "")
        def refresh(now):
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]): return
            c = win["c"]
            if st["minimized"]:
                wt = st["weight"]
                sig = (st["ver"], settings["ore"], settings["wood"], settings["fish"], settings["sand"])
                if st["count"][0] != sig: st["count"] = (sig, len(shown_spots()))
                n = st["count"][1]; mkey = (n, wt)
                if st["mini_drawn"] is not None and mkey == st["mini_key"]: return
                st["mini_key"] = mkey
                txt = "%s: %s, %s" % (TITLE, ("weight %d%%" % int(wt[2] * 100)) if wt and wt[2] >= 0 else "weight ?",
                    Kit.count(n, "dry spot"))
                if txt != st["mini_drawn"]:
                    st["mini_drawn"] = txt; lbl = c.get("status")
                    if lbl is not None:
                        hue = Kit.HUE_INFO
                        if wt and wt[2] >= WEIGHT_RED: hue = Kit.HUE_BAD
                        elif wt and wt[2] >= WEIGHT_WARN: hue = Kit.HUE_TITLE
                        Kit.set_text(lbl, Kit.fit(txt, MINI_W - 90), hue)
                return
            draw_weight()
            sig = (st["ver"], st["arrow"], settings["ore"], settings["wood"], settings["fish"], settings["sand"])
            if sig == st["drawn"] and now < st["draw_at"] and st["draw_at"] - now <= DRAW_EVERY: return
            st["drawn"], st["draw_at"] = sig, now + DRAW_EVERY; me = read_me() or st["me"]
            listed = [(dist_of(e, me), e["hi"], e) for e in shown_spots()]; listed.sort(key=_by_place); here = None
            if me is not None:
                for kind in KINDS:
                    if settings[kind]:
                        e = spots.get(bank_of(kind, me[2], me[0], me[1]))
                        if e is not None: here = e; break
            if here is not None:
                Kit.set_text(c["here"], Kit.fit("Here: %s is dry, %s" % (
                    KIND_NAME[here["kind"]].lower(), back_text(here, now)[0]), c["here_w"]), Kit.HUE_BAD)
            elif listed: Kit.set_text(c["here"], "Here: nothing known dry", Kit.HUE_GOOD)
            else: Kit.set_text(c["here"], Kit.fit(EMPTY_TEXT, c["here_w"]), Kit.HUE_INFO)
            back_w = c.get("back_w", 160)
            for k, r in enumerate(win["rows"]):
                if k >= len(listed):
                    Kit.row_set(r, None, now)
                    r["sig"] = None; show_row(r, False); continue
                e = listed[k][2]; where = where_text(e, me); key = e["key"]
                Kit.row_set(r, (key,), now)
                on = st["arrow"] == key; back, bhue = back_text(e, now)
                rsig = (key, where, back, bhue, on, e["lo"], e["hi"]); show_row(r, True)
                if rsig == r["sig"]: continue
                r["sig"] = rsig; Kit.set_text(r["kind"], KIND_NAME[e["kind"]], KIND_HUE.get(e["kind"], Kit.HUE_TEXT))
                Kit.set_text(r["where"], Kit.fit(("> " if on else "") + where, 124),
                             Kit.HUE_TITLE if on else Kit.HUE_TEXT)
                Kit.set_text(r["back"], Kit.fit(back, back_w), bhue); tip = (key, on, e["lo"], e["hi"])
                if tip != r["tip"]: r["tip"] = tip; Kit.with_tip(r["catch"], row_tip(e, on))
            more = len(listed) - len(win["rows"])
            Kit.set_text(c["more"], ("+%d farther" % more) if more > 0 else "", Kit.HUE_INFO)
        def draw_weight():
            c = win["c"]; wt = st["weight"]
            if st["wdrawn"] is not None and wt == st["w_key"]: return
            st["w_key"] = wt; fills = c.get("wfills")
            if wt is None or wt[2] < 0: text, kind, width = "not known yet", None, 0
            else:
                text = "%d / %d stones (%d%%)" % (wt[0], wt[1], int(wt[2] * 100))
                kind, width = Kit.weight_level(wt[2], c.get("wbar_w", 100))
            sig = (text, kind, width)
            if sig == st["wdrawn"]: return
            st["wdrawn"] = sig; hue = {"red": Kit.HUE_BAD, "warn": Kit.HUE_TITLE}.get(kind, Kit.HUE_TEXT)
            if c.get("wtext") is not None: Kit.set_text(c["wtext"], text, hue)
            Kit.weight_show(fills or {}, kind, width)
        RESPAWN_NOTE = ("Back in: ore and sand 10-20 min, wood 20-30, fish 10-20, from the block's first harvest (3x "
                        "as long in guarded towns).")
        def act_clear(action): arrow_off(); spots.clear(); spots_changed()
        ACTIONS = {"clear": act_clear, "arrow_off": lambda action: arrow_off(),
                   "arrow": lambda action: arrow_to(action[1]), "ping": lambda action: ping_spot(action[1])}
        def kind_caption(kind): return "%s (%s)" % (KIND_NAME[kind], KIND_SKILL[kind])
        def kind_cols(w):
            widest = max(Kit.text_w(kind_caption(k)) for k in KINDS); return 2 if widest + 30 <= (w - 24) // 2 else 1
        def page_table(w):
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
            if new["keep"] != old["keep"]: st["save_due"] = True
            if new["alert"] and not old["alert"]: st["w_armed"] = True
            st["drawn"] = st["mini_drawn"] = None
        cfg = Kit.Page(settings, page_table, save_settings, on_change)
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "drawn": None,
                       "mini_drawn": None, "wdrawn": None, "arrow": None, "ping": None,
                       "w_armed": True, "weight": None, "w_at": 0.0, "draw_at": 0.0,
                       "expire_at": 0.0, "save_due": False, "save_at": 0.0, "me": None,
                       "count": (None, 0), "last_now": None, "atlas": None, "minimized": wnd.start_min()})
            del jobs[:]; first.clear(); load_settings(); load_spots()
            st["rd"] = Journal.reader(); HOST.alert_kind(WEIGHT_ALERT, "Weight near the limit", 0x04A)
            read_me(); build_window(); wnd.dock(fit=True, min=(W, full_h(1)))
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            now = time.time(); last, st["last_now"] = st["last_now"], now
            if last is not None and now < last - 2.0: rebase(now - last)
            q = st["queue"]
            while q:
                action = q.pop(0); kind = action[0] if isinstance(action, tuple) else action
                if not wnd.action(action): ACTIONS[kind](action)
                if win["g"] is None: return
            read_journal(now)
            if now >= st["expire_at"] or st["expire_at"] - now > EXPIRE_EVERY:
                st["expire_at"] = now + EXPIRE_EVERY; expire(now)
            av = (st["ver"], settings["ore"], settings["wood"], settings["fish"], settings["sand"])
            if av != st["atlas"]: st["atlas"] = av; atlas_publish()
            read_weight(now); send_ping(now); refresh(now)
            if st["save_due"] and (now >= st["save_at"] or st["save_at"] - now > SAVE_EVERY) and not jobs:
                jobs.append(save_spots_job)
        def _thread_tick():
            while jobs and not st["shutting"]: jobs.pop(0)()
        def _thread_wanted(): return bool(jobs)
        def _stop():
            st["shutting"] = True; arrow_off(); st["ping"] = st["rd"] = None; del jobs[:]; save_settings()
            Kit.put_var(SPOTS_KEY, spots_text() if settings["keep"] else ""); st["save_due"] = False; cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed,
                "thread_tick": _thread_tick, "thread_wanted": _thread_wanted}
    def _part_traps():
        KEY = "traphl"; TITLE = "Traps & Fields"; SETTINGS_KEY = "TrapHL_settings"; POS_KEY = "TrapHL_pos"
        VIEW_KEY = "TrapHL_view"; H = Kit.MARGIN + 30 + Kit.GAP + 40 + Kit.MARGIN; MINI_W, MINI_H = 320, 46
        HUE_GREEN = 68; HUE_RED = 33; HUE_MAX = 3000; POKE_GAP = 0.15
        SCAN_MOVE = 1.0; SCAN_IDLE = 3.0; HUE_EVERY = 3.0; NAME_RETRY = 5.0
        DEFAULT_GRAPHICS = [0x1103, 0x1116, 0x11AC, 0x11B1, 0x11A0, 0x11A8, 0x11B8, 0x113C, 0x1147, 0x10F5, 0x10FC,
            0x1125, 0x1B71, 0x1B72, 0x1B73, 0x1B74, 0x0E70,]
        FIELDS_KEY = "TrapHL_fields"
        FIELD_RANGES = (("fire", 0x398C, 0x399F), ("poison", 0x3914, 0x3929),
                        ("paralyze", 0x3967, 0x398A), ("energy", 0x3946, 0x3964))
        FIELD_HUE = 0x0035; PARALYZE_HUE = 0x0481
        FIELD_WORDS = {"fire": ("Fire field", Kit.HUE_TITLE), "poison": ("Poison field", Kit.HUE_TITLE),
                       "energy": ("Energy field", Kit.HUE_TITLE), "paralyze": ("Paralyze field!", Kit.HUE_BAD)}
        FIELD_SAY_NEAR = 3; ALERT_TRAP = "traphl.trap"
        FIELD_GFX = {g: k for k, a, b in FIELD_RANGES for g in range(a, b + 1)}; NO_FIELDS = {}
        settings = {"range": 14, "cycle": 2.0, "pulse": True,
                    "green": HUE_GREEN, "red": HUE_RED, "by_name": True, "graphics": list(DEFAULT_GRAPHICS),
                    "ping": True, "fields": True, "field_hue": FIELD_HUE, "para_hue": PARALYZE_HUE, "field_say": False}
        DEFAULTS = dict(settings)
        st = {"minimized": False, "shutting": False, "docked": False, "queue": [], "hooked": False, "poke": False}
        win = {"g": None, "c": {}, "store": ({}, {})}; page = {"f": None, "gfx_typed": None, "gfx_since": 0.0}
        cleanup, queue, say = Kit.basics(st, TITLE)
        def load_settings():
            p = Kit.get_var(SETTINGS_KEY).split("|")
            if len(p) < 7: return
            with Kit.quiet:
                settings["range"] = max(1, min(30, int(p[0]))); settings["cycle"] = max(0.5, min(10.0, float(p[1])))
                settings["pulse"] = p[2] == "1"; settings["green"] = max(1, min(HUE_MAX, int(p[3])))
                settings["red"] = max(1, min(HUE_MAX, int(p[4])))
                settings["by_name"] = p[5] == "1"; gl = parse_graphics(p[6])
                if gl or not p[6].strip(): settings["graphics"] = gl
                if len(p) >= 8: settings["ping"] = p[7] != "0"
        def load_fields():
            v = Kit.codec_load(Kit.get_var(FIELDS_KEY)); settings["fields"] = v.get("on") != "0"
            settings["field_say"] = v.get("say") == "1"
            for k, key, default in (("hue", "field_hue", FIELD_HUE), ("para", "para_hue", PARALYZE_HUE)):
                try: settings[key] = max(0, min(HUE_MAX, int(v[k])))
                except (KeyError, ValueError): settings[key] = default
        def save_fields():
            Kit.put_var(FIELDS_KEY, "on=%d;hue=%d;para=%d;say=%d" % (
                int(settings["fields"]), settings["field_hue"], settings["para_hue"], int(settings["field_say"])))
        def save_settings():
            Kit.put_var(SETTINGS_KEY, "|".join([str(settings["range"]), "%.2f" % settings["cycle"],
                        "1" if settings["pulse"] else "0", str(settings["green"]), str(settings["red"]),
                        "1" if settings["by_name"] else "0", graphics_text(), "1" if settings["ping"] else "0"]))
        def parse_graphics(text):
            out = []
            for tok in str(text).replace(";", ",").replace(" ", ",").split(","):
                tok = tok.strip()
                if not tok: continue
                try: v = int(tok, 16)
                except Exception: continue
                if 0 < v < 0x10000 and v not in out: out.append(v)
            return out
        def graphics_text(): return ", ".join("0x%04X" % g for g in settings["graphics"])
        def load_view():
            raw = Kit.get_var(VIEW_KEY); v = Kit.codec_load(raw)
            st["minimized"] = v.get("min") == "1"; st["paused"] = v.get("paused") == "1"; st["view_saved"] = raw
        def save_view():
            data = "min=%d;paused=%d" % (int(bool(st["minimized"])), int(bool(st["paused"])))
            if data != st.get("view_saved"): st["view_saved"] = data; Kit.put_var(VIEW_KEY, data)
        def set_hue(item, hue): item.Hue = int(hue) & 0xFFFF
        def get_hue(item): return int(item.Hue or 0)
        def xy_of(item): return int(item.X), int(item.Y)
        verdicts = {}; VERDICT_SIG = {"gfx": None, "wanted": frozenset(), "by_name": None, "fields": None}
        def named_trap(it):
            name = str(it.Name or "").lower()
            if not name: return None
            return "trap" in name and "scroll" not in name and "kit" not in name
        def verdict_sig():
            sig = VERDICT_SIG; gl = settings["graphics"]
            if sig["gfx"] is not gl or sig["by_name"] != settings["by_name"] or sig["fields"] != settings["fields"]:
                sig["gfx"], sig["wanted"] = gl, frozenset(gl)
                sig["by_name"], sig["fields"] = settings["by_name"], settings["fields"]; verdicts.clear()
            return sig["wanted"]
        def scan():
            rng = int(settings["range"]); st["atlas_map"] = None; found = {}; ffound = {}; now = st["last_scan"]
            check_hues = now >= st["hue_at"]; field_gfx = FIELD_GFX if settings["fields"] else NO_FIELDS
            if check_hues: st["hue_at"] = now + HUE_EVERY
            wanted = verdict_sig(); by_name = settings["by_name"]; old = verdicts; seen = {}
            for it in API.GetItemsOnGround(rng) or ():
                serial = int(it.Serial); g = int(it.Graphic); v = old.get(serial)
                if v is not None and v[0] == g and (not v[2] or now < v[2]): kind = v[1]; seen[serial] = v
                else:
                    retry = 0
                    if g in wanted: kind = 1
                    elif by_name and g not in field_gfx:
                        named = named_trap(it)
                        if named is None: kind, retry = 0, now + NAME_RETRY
                        else: kind = 1 if named else 0
                    else: kind = 2 if g in field_gfx else 0
                    seen[serial] = (g, kind, retry)
                if kind == 1: found[serial] = it
                elif kind == 2: ffound[serial] = it
            verdicts.clear(); verdicts.update(seen); tracked = st["tracked"]; new_traps = []
            for serial, it in found.items():
                rec = tracked.get(serial)
                if rec is None:
                    orig = get_hue(it)
                    if orig in (settings["green"], settings["red"]): orig = 0
                    tracked[serial] = {"item": it, "orig": orig, "set": settings["green"]}
                    set_hue(it, settings["green"]); atlas_seen(it)
                    if settings["ping"] and serial not in st["pinged"]: st["ping_wait"].append(serial)
                    if serial not in st["alerted"]: new_traps.append(it)
                else:
                    rec["item"] = it
                    if check_hues and get_hue(it) != rec["set"]: set_hue(it, rec["set"])
            gone = [s for s in tracked if s not in found]
            for serial in gone: put_back(serial, tracked.pop(serial))
            if gone and st["ping_wait"]: st["ping_wait"] = [s for s in st["ping_wait"] if s in tracked]
            if new_traps: alert_new_traps(new_traps)
            if ffound or st["fields"]: scan_fields(ffound, check_hues)
        def atlas_seen(it):
            x, y = xy_of(it)
            if x <= 0 or y <= 0: return
            if st["atlas_map"] is None: st["atlas_map"] = int(API.GetMap())
            spot = (x, y, st["atlas_map"]); seen = st["atlas_traps"]
            if spot in seen: return
            seen.append(spot)
            if len(seen) > 20: del seen[0]
            st["atlas_ver"] += 1
        def atlas_publish():
            ATLAS.set("traps", {atlas_name("Trap %d %d" % (x, y)): (x, y, m, "red") for x, y, m in st["atlas_traps"]})
        DIRS = ("east", "south-east", "south", "south-west", "west", "north-west", "north", "north-east")
        def alert_new_traps(its):
            alerted = st["alerted"]
            if len(alerted) + len(its) > 5000: alerted.clear()
            p = API.Player; px, py = int(p.X), int(p.Y); best, best_d, bdx, bdy = None, None, 0, 0
            for it in its:
                alerted.add(int(it.Serial)); dx, dy = int(it.X) - px, int(it.Y) - py; d = max(abs(dx), abs(dy))
                if best_d is None or d < best_d: best, best_d, bdx, bdy = it, d, dx, dy
            w = Kit.where_text(bdx, bdy, names=DIRS)
            text = "A trap %s" % w if len(its) == 1 else "%d new traps in range (nearest %s)" % (len(its), w)
            HOST.alert(ALERT_TRAP, text, who=int(best.Serial))
        def field_hue(kind): return settings["para_hue"] if kind == "paralyze" else settings["field_hue"]
        def scan_fields(ffound, check_hues):
            fields = st["fields"]; said_now = []
            for serial, it in ffound.items():
                rec = fields.get(serial)
                if rec is None:
                    kind = FIELD_GFX.get(int(it.Graphic))
                    if kind is None: continue
                    want = field_hue(kind); orig = get_hue(it)
                    if orig and orig in (settings["field_hue"], settings["para_hue"]): orig = 0
                    fields[serial] = rec = {"item": it, "orig": orig, "set": want, "kind": kind}
                    if want: set_hue(it, want)
                    if settings["field_say"]: said_now.append(rec)
                    continue
                rec["item"] = it; want = field_hue(rec["kind"])
                if want != rec["set"]: set_hue(it, want if want else rec["orig"]); rec["set"] = want
                elif want and check_hues and get_hue(it) != want: set_hue(it, want)
            for serial in [s_ for s_ in fields if s_ not in ffound]: restore_field(serial)
            if said_now: say_fields(said_now)
        def say_fields(recs):
            now = time.time(); said = [e for e in st["field_said"] if now - e[3] < 10.0]
            spots = sorted([xy_of(rec["item"]) + (rec["kind"], rec["item"]) for rec in recs], key=_by_place)
            for x, y, kind, it in spots:
                dup = False
                for k, sx, sy, t in said:
                    if (k == kind and abs(sx - x) <= FIELD_SAY_NEAR and abs(sy - y) <= FIELD_SAY_NEAR):
                        dup = True; break
                said.append((kind, x, y, now))
                if dup: continue
                text, hue = FIELD_WORDS.get(kind, ("Field", Kit.HUE_TITLE)); API.HeadMsg(text, int(it.Serial), hue)
            st["field_said"] = said[-20:]
        def _by_place(e): return (e[0], e[1])
        def restore_field(serial):
            rec = st["fields"].pop(serial, None)
            if rec is not None and rec["set"]: put_back(serial, rec)
        def put_back(serial, rec): set_hue(API.FindItem(serial) or rec["item"], rec["orig"])
        def restore_all():
            for serial in list(st["tracked"]): put_back(serial, st["tracked"].pop(serial))
            for serial in list(st["fields"]): restore_field(serial)
        def pulse():
            if not st["tracked"]: return
            want_red = settings["pulse"] and (time.time() % max(0.5, settings["cycle"])
                                              < min(0.35, settings["cycle"] / 2.0))
            hue = settings["red"] if want_red else settings["green"]
            for rec in st["tracked"].values():
                if rec["set"] != hue: set_hue(rec["item"], hue); rec["set"] = hue
        def ping_service(): return HOST.services.get("pings.send")
        def send_pings():
            n0 = len(st["ping_wait"])
            if n0:
                _send_one_ping()
                if len(st["ping_wait"]) != n0: refresh()
        def _send_one_ping():
            wait = st["ping_wait"]; svc = ping_service()
            if svc is None:
                if not st["ping_noted"]:
                    st["ping_noted"] = True; say("turn World Map > Map Pings on to ping traps (they wait until then).")
                return
            if time.time() < st["ping_next"]: return
            tracked = st["tracked"]; m = None
            while wait:
                serial = wait[0]; rec = tracked.get(serial)
                if rec is None or serial in st["pinged"]: wait.pop(0); continue
                x, y = xy_of(rec["item"])
                if x <= 0 or y <= 0: wait.pop(0); continue
                if m is None: m = int(API.GetMap())
                spot = (m, x, y)
                if spot in st["pinged_spots"]: mark_pinged(serial, None); wait.pop(0); continue
                try: ok = svc(x, y, m, "danger", "You (trap)")
                except Exception: mark_pinged(serial, spot); wait.pop(0); return
                if ok:
                    wait.pop(0); mark_pinged(serial, spot); st["ping_sent"] += 1; st["ping_next"] = time.time() + 0.75
                return
        def mark_pinged(serial, spot):
            if len(st["pinged"]) >= 5000: st["pinged"].clear(); st["pinged_spots"].clear()
            st["pinged"].add(serial)
            if spot is not None: st["pinged_spots"].add(spot)
        def ping_again():
            st["pinged"].clear(); st["pinged_spots"].clear(); st["ping_sent"] = 0; st["ping_wait"] = list(st["tracked"])
            n = len(st["ping_wait"])
            if st["paused"]: msg = "paused: untick Pause highlighting (World Map settings) to ping traps."
            elif n == 0: msg = "no traps in range; each is pinged when next found."
            elif ping_service() is None: msg = ("%s to ping once World Map > Map Pings is on." % Kit.count(n, "trap"))
            else: msg = "pinging %s." % Kit.count(n, "trap")
            say(msg); st["ping_noted"] = False; refresh()
        def ping_status():
            n = len(st["ping_wait"])
            if n and st["ping_svc"] is not None: return "sending %d" % n, Kit.HUE_INFO
            if not settings["ping"]: return "auto-ping off", Kit.HUE_INFO
            if st["ping_svc"] is None: return "World Map > Map Pings is off", Kit.HUE_BAD
            return "%d sent" % st["ping_sent"], Kit.HUE_GOOD
        PING_TIP = "Ping danger on each highlighted trap, and again when next found (needs World Map > Map Pings)"
        PING_CAP = "Ping traps on screen"
        def build_window():
            z = told(wnd, st, 320, H); w, h = z if z else (320, H); g, store, c = wnd.begin(w, h)
            if not st["minimized"]:
                wnd.frame(g); M = Kit.MARGIN; yb = M + 30 + Kit.GAP; Kit.add_section(g, M, yb, w - 2 * M, h - yb - M)
                Kit.art_button(g, store, "ping", Kit.ART_CIRCLE, M + 12, yb + 12, PING_CAP,
                               PING_TIP, on_click=queue("ping_again"))
            wnd.end(g); refresh(); save_view()
        wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, None, (200, 200), (MINI_W, MINI_H), 0x113C,
                         cleanup, lock=True)
        def refresh():
            c = win["c"]; n = len(st["tracked"]); nf = len(st["fields"])
            if st["paused"]: text, hue = "Paused", Kit.HUE_INFO
            elif n == 0 and nf == 0: text, hue = "No traps in range", Kit.HUE_INFO
            elif nf == 0: text, hue = "Highlighting %s" % Kit.count(n, "trap"), Kit.HUE_GOOD
            elif n == 0: text, hue = "Highlighting %s" % Kit.count(nf, "field"), Kit.HUE_GOOD
            else: text, hue = "Highlighting %s, %s" % (Kit.count(n, "trap"), Kit.count(nf, "field")), Kit.HUE_GOOD
            if c.get("status") is not None:
                Kit.set_text(c["status"], Kit.fit("%s: %s" % (TITLE, journal_case(text)), MINI_W - 90), hue)
            f = page["f"]
            if f is None: return
            Kit.set_text(f.c["now"], text, hue); ptext, phue = ping_status()
            Kit.set_text(f.c["now_ping"], "Pings: " + ptext, phue)
            if st["pause_want"] is None and bool(f.c["paused"].IsChecked) != bool(st["paused"]):
                f.c["paused"].SetIsChecked(bool(st["paused"]))
        def draw_status(f, x, y):
            f.c["now"] = Kit.add_label(f.g, "", x + 12, y, Kit.HUE_GOOD)
            f.c["now_ping"] = Kit.add_label(f.g, "", x + 12 + f.w // 2, y, Kit.HUE_INFO)
        def draw_paused(f, x, y):
            f.c["paused"] = Kit.add_check(f.g, "Pause highlighting (the hues are put back)", x + 12, y, st["paused"],
                                          "Stops the scan and puts every hue back")
        ACTIONS = {"ping_again": ping_again}
        def draw_cycle(f, x, y):
            Kit.add_label(f.g, "Pulse cycle:", x + 12, y + 4); cyc = int(round(settings["cycle"] * 10))
            f.c["cycle"] = Kit.with_tip(Kit.add_slider(f.g, x + 120, y + 2, 160, 5, 100, cyc),
                                        "Seconds between red flashes (0.5-10)")
            f.c["cycle_v"] = Kit.add_label(f.g, "%.1f s" % settings["cycle"], x + 290, y + 4, Kit.HUE_INFO)
        def draw_graphics(f, x, y):
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
                ("TRAP PINGS  (needs World Map > Map Pings)", (("check", "ping", "Send a Danger map ping on each "
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
        def page_table(w): return PAGE
        cfg = Kit.Page(settings, page_table, save_settings)
        def build_config(g, x, y, w):
            page["f"] = Kit.Form(g, x, y, w, settings, PAGE)
            page["gfx_typed"], page["gfx_applied"] = None, graphics_text(); refresh()
        def poll_config(force=False):
            f = page["f"]
            if f is None: return
            new = f.read(); c = f.c; now = time.time()
            try: typed = str(c["graphics"].Text or ""); cyc = int(c["cycle"].Value); pz = bool(c["paused"].IsChecked)
            except Exception: return
            cyc = max(5, min(100, cyc)) / 10.0
            if abs(cyc - settings["cycle"]) > 0.01: new["cycle"] = cyc; Kit.set_text(c["cycle_v"], "%.1f s" % cyc)
            if typed != page["gfx_typed"]: page["gfx_typed"], page["gfx_since"] = typed, now
            if (force or now - page["gfx_since"] >= 0.7) and typed != page["gfx_applied"]:
                page["gfx_applied"] = typed
                new["graphics"] = (parse_graphics(typed) or settings["graphics"]) if typed.strip() else []
            if pz != (st["paused"] if st["pause_want"] is None else st["pause_want"]): st["pause_want"] = pz
            if new["ping"] != settings["ping"]:
                st["ping_wait"] = [sr for sr in st["tracked"] if sr not in st["pinged"]] if new["ping"] else []
            if new == settings: return
            settings.update(new); st["last_scan"] = 0.0; save_settings(); save_fields(); refresh()
        def config_closed():
            try: poll_config(True)
            finally: page["f"] = None; page["gfx_typed"] = None
        def _start():
            st.update({"shutting": False, "docked": HOST.dock_soon(KEY), "queue": [], "last_scan": 0.0,
                       "hue_at": 0.0, "moved": False, "tracked": {}, "pinged": set(), "pinged_spots": set(),
                       "ping_wait": [], "ping_sent": 0, "ping_noted": False,
                       "ping_svc": ping_service(), "ping_next": 0.0, "fields": {}, "field_said": [], "alerted": set(),
                       "atlas_traps": [], "atlas_ver": 0, "atlas_done": -1, "atlas_map": None, "pause_want": None})
            verdicts.clear(); load_settings(); load_fields()
            HOST.alert_kind(ALERT_TRAP, "New trap in range", 0x1EF); load_view()
            Kit.hook_once(st, "hooked", ("OnItemCreated", on_ground_item), ("OnPositionChanged", on_moved))
            if HOST.dock_wanted(KEY): st["minimized"] = True
            build_window(); wnd.dock(fit=True, min=(320, H))
        def _tick():
            if win["g"] is None: return
            if Kit.closed(win): return
            want = st["pause_want"]
            if want is not None:
                st["pause_want"] = None
                if want != st["paused"]:
                    st["paused"] = want
                    if want: restore_all(); st["ping_wait"] = []
                    else: st["last_scan"] = 0.0
                    save_view(); refresh()
            while st["queue"]:
                action = st["queue"].pop(0)
                if not wnd.action(action): ACTIONS[action]()
            if st["paused"]: return
            now = time.time(); gap = now - st["last_scan"]
            if gap < 0: st["last_scan"] = st["hue_at"] = st["ping_next"] = 0.0; gap = SCAN_IDLE
            if gap >= SCAN_IDLE or (st["moved"] and gap >= SCAN_MOVE) or (st["poke"] and gap >= POKE_GAP):
                st["last_scan"] = now; st["poke"] = st["moved"] = False
                before = (len(st["tracked"]), len(st["fields"])); scan(); svc = ping_service()
                if (len(st["tracked"]), len(st["fields"])) != before or (svc is None) != (st["ping_svc"] is None):
                    st["ping_svc"] = svc
                    if svc is not None: st["ping_noted"] = False
                    refresh()
                if st["atlas_ver"] != st["atlas_done"]: st["atlas_done"] = st["atlas_ver"]; atlas_publish()
            send_pings(); pulse()
        def on_ground_item(*args):
            if st["poke"] or st["paused"] or st["shutting"]: return
            for a in args:
                try: g = int(a.Graphic)
                except Exception: continue
                if g in VERDICT_SIG["wanted"] or (settings["fields"] and g in FIELD_GFX): st["poke"] = True
                return
        def on_moved(*args): st["moved"] = True
        def _stop(): st["shutting"] = True; restore_all(); save_settings(); cleanup.close()
        return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
                "build_config": build_config, "poll_config": poll_config, "config_closed": config_closed}
    PARTS = (("pings", _part_pings, 0.05, "pings"),
        ("corpse", lambda: with_atlas(_part_corpse(), "corpse"), 0.25, "corpserun"),
        ("maps", lambda: with_atlas(_part_maps(), "maps"), 0.2, "treasure"),
        ("dry", lambda: with_atlas(_part_dry(), "dry"), 0.2, "harvest"),
        ("traps", lambda: with_atlas(_part_traps(), "traps"), 0.1, "traphl"),)
    return PartSet(KEY, TITLE, PARTS, shared=SHARED).hooks()


if "HOST" not in globals():
    import API
    exec(open(API.ScriptPath + "/../VirtueAssistantModules/_Alone.py").read())
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
