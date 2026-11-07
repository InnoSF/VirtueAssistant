def _module_worldmap():
    KEY = "worldmap"; TITLE = "World Map"; ATLAS_PREFIX = "VA "; ATLAS_PLACED_KEY = "WorldMap_atlas_placed"
    ATLAS_ON_KEY = "WorldMap_atlas"
    ATLAS_OWNERS = (("corpse", "your corpse"), ("maps", "your dig spots"),
                    ("dry", "the spots that ran dry"), ("traps", "the traps you have seen"))
    ATLAS_CHECK = 1.0; ATLAS_CLOSED_CHECK = 2.5; GUMP_EVERY = 0.5; ATLAS_SETTLE = 2.0; ATLAS_OPS = 3; ATLAS_CAP = 60
    GUMPS = {"at": -1.0, "ok": False, "map": False, "arrow": False}; GUMP_TYPE = []
    def gump_flags(fresh=False):
        memo = GUMPS; now = time.time()
        if not fresh and 0.0 <= now - memo["at"] < GUMP_EVERY: return memo
        memo["at"] = now; mp = ar = False
        try:
            if not GUMP_TYPE: GUMP_TYPE.append(Tz.T("ClassicUO.Game.Managers.UIManager"))
            for w in list(Tz.get(None, "Gumps", GUMP_TYPE[0])):
                n = str(w.GetType().Name)
                if n == "WorldMapGump":
                    mp = True
                    if ar: break
                elif n == "QuestArrowGump":
                    ar = True
                    if mp: break
            memo["ok"] = True
        except Exception: memo["ok"] = False
        memo["map"], memo["arrow"] = mp, ar; return memo
    class Atlas(object):
        def __init__(self):
            self.items, self.on, self.placed, self.want, self.loose = {}, {}, {}, {}, set(); self.synced = True
            self.open_since = self.saved = None; self.next_check = 0.0; self.loaded = self.strip_pending = False
        def load(self):
            if self.loaded: return
            self.loaded = True
            for k, v in Kit.codec_load(Kit.get_var(ATLAS_ON_KEY)).items(): self.on[k] = v != "0"
            try: text = str(API.GetPersistentVar(ATLAS_PLACED_KEY, "", API.PersistentVar.Global) or "")
            except Exception: text = ""
            for line in text.split("\n"):
                p = line.split("|")
                if len(p) == 5 and p[0].startswith(ATLAS_PREFIX):
                    try: self.placed[p[0]] = (int(p[1]), int(p[2]), int(p[3]), p[4])
                    except ValueError: pass
            self.saved = text; self.strip_pending = bool(self.placed) and not self.map_open(True); self._rebuild()
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
            for owner, items in self.items.items():
                if self.on.get(owner, True):
                    for name, v in items.items():
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
                    safe(lambda: API.RemoveMapMarker(name)); del self.placed[name]; ops += 1
            for name, v in self.want.items():
                if ops >= ATLAS_OPS: break
                if name not in self.placed:
                    safe(lambda: API.AddMapMarker(name, v[0], v[1], v[2], v[3])); self.placed[name] = v; ops += 1
            self.synced = self.want == self.placed; self._save()
        def thread_work(self):
            if not self.strip_pending and not self.loose: return
            is_open = Kit.on_client(lambda: self.map_open(True))
            if self.strip_pending:
                if not is_open and self._strip_file(): self.placed.clear(); self._save()
                self.strip_pending = False; self.synced = self.want == self.placed
            if self.loose:
                if is_open:
                    for name in list(self.loose): safe(lambda: API.RemoveMapMarker(name))
                else: self._strip_file()
                self.loose.clear()
        def _save(self):
            text = "\n".join("%s|%d|%d|%d|%s" % (n, v[0], v[1], v[2], v[3]) for n, v in sorted(self.placed.items()))
            if text != self.saved:
                self.saved = text; safe(lambda: API.SavePersistentVar(ATLAS_PLACED_KEY, text, API.PersistentVar.Global))
        def shutdown(self):
            self.items.clear(); self.want = {}; self.strip_pending = False
            if not self.placed and not self.loose: self.synced = True; return
            if self.map_open(True):
                for name in list(self.placed) + list(self.loose): safe(lambda: API.RemoveMapMarker(name))
                self.placed.clear()
            elif self._strip_file(): self.placed.clear()
            self.loose.clear(); self.synced = not self.placed; self._save()
        def _strip_file(self):
            try: exe = str(Tz.get(None, "ExecutablePath", Tz.T("ClassicUO.CUOEnviroment")))
            except Exception:
                try: exe = os.path.dirname(str(API.GetType().Assembly.Location))
                except Exception: return False
            folder = os.path.join(exe, "Data", "Client")
            if not os.path.isdir(folder): return False
            path = os.path.join(folder, "userMarkers.usr")
            if not os.path.exists(path): return True
            try:
                import io
                with io.open(path, "r", encoding="utf-8-sig") as f: lines = f.read().splitlines()
                keep = []
                for line in lines:
                    p = line.split(",")
                    if len(p) > 3 and (p[3] in self.placed or p[3] in self.loose): continue
                    keep.append(line)
                if len(keep) != len(lines):
                    with io.open(path, "w", encoding="utf-8") as f: f.write(u"".join(l + u"\n" for l in keep))
                return True
            except Exception: return False
    ATLAS = Atlas()
    def atlas_name(text): return ATLAS_PREFIX + str(text).replace(",", " ")
    def arrow_open(fresh=False): f = gump_flags(fresh); return f["arrow"] if f["ok"] else True
    ATLAS_BOX = {}
    def atlas_page(owner):
        def draw(f, x, y):
            ATLAS_BOX[owner] = Kit.add_check(f.g, "Show %s on TazUO's World Map" % dict(ATLAS_OWNERS).get(owner, owner),
                                             x + 12, y, ATLAS.is_on(owner), "Puts markers named \"%s...\" on TazUO's "
                                             "World Map while it is open; they come off when this is unticked or the "
                                             "part stops" % ATLAS_PREFIX)
        return "TAZUO'S WORLD MAP  (while it is open)", (("custom", 26, draw),), {"sh": 66}
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
    JOURNAL_NAMES = ("TazUO", "World Map", "Map Pings", "Enhanced Map", "Virtue Assistant",
                     "Settings", "Inventory", "Need help", "Look here", "Go here", "Danger!")
    def journal_case(text):
        text = str(text or "")
        if not text or text[0] in "[(\"'" or text.startswith(JOURNAL_NAMES): return text
        return text[0].lower() + text[1:]
    def read_checks(c, d, keys):
        hit = []
        for k in keys:
            try: on = bool(c[k].IsChecked)
            except Exception: continue
            if on != d[k]: d[k] = on; hit.append(k)
        return hit
    def list_h(rows, row_h): return 2 * Kit.MARGIN + 30 + 2 * Kit.GAP + 36 + 30 + rows * row_h + 8
    def open_window(st, win, pos_key, mini, full, at, title, key, queue, close_tip=None):
        w, h = mini if st["minimized"] else full; x, y = Kit.load_pos(pos_key, at, (w, h))
        if Kit.is_open(win["g"]): x, y = win["g"].GetX(), win["g"].GetY()
        old, win["g"] = win["g"], None; store, c, g = ({}, {}), {}, G.CreateGump(True, True)
        if st["minimized"]:
            c["status"] = Kit.mini_bar(g, store, w, h, title, key, queue("toggle_min"), close_tip=close_tip)
        else:
            Kit.add_window_frame(g, w, h)
            Kit.title_bar(g, store, w, title, key, queue("toggle_min"), queue("to_bar"), queue("settings"),
                          close_tip=close_tip)
        return g, store, c, w, h, x, y, old
    def show_window(g, x, y, w, h, st, win, disposed, pos_key, **parts):
        Kit.show_window(g, x, y, w, h, None, st["minimized"] and st["docked"], disposed(g),
                        lambda: Kit.save_pos(pos_key, win["g"]), win, dict(parts, g=g))
    def row_clicker(rows_of, k, field, act, queue, lo=-1e9):
        def handler(*args):
            rows = rows_of()
            if k < len(rows):
                r = rows[k]; key = r[field]; prev, at = r["prev"]
                if prev and lo <= time.time() - at < 0.15: key = prev
                if key: queue((act, key))()
        return handler
    def _part_pings():
        TITLE = "Map Pings"; DEFAULT_PORT = 8887
        HOTKEYS = {"look": "CTRL+1", "danger": "CTRL+2", "go": "CTRL+3", "help": "CTRL+4",}
        HOTKEY_ORDER = ("look", "danger", "go", "help"); MARKERS_CAP = 60; PING_RATE_SECS = 0.75; SEND_TIMEOUT = 5
        PING_SOUNDS = (0x1EA, 0x307, 0x1FC, 0x202); HISTORY_MAX = 200; HISTORY_ROWS = 10
        try: import socket; import select; _HAVE_PY_SOCKET = True
        except Exception: _HAVE_PY_SOCKET = False
        import collections; VAR_PREFIX = "EMPings."; say = Kit.sayer(TITLE); LOOK, DANGER, GO, HELP = 0, 1, 2, 3
        TYPE_KEYS = {"look": LOOK, "danger": DANGER, "go": GO, "help": HELP}
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
                self.s = socket.create_connection((host, port), timeout); self.s.settimeout(SEND_TIMEOUT)
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
            if _HAVE_PY_SOCKET:
                try: return PySocketTransport(host, port, timeout)
                except (socket.timeout, socket.gaierror, ConnectionError, OSError): raise
                except Exception: pass
            return DotNetTransport(host, port, timeout)
        class Sender(object):
            def __init__(self, transport):
                self.t = transport; self.error = self.cond = None; self.stopped = False; self.q = collections.deque()
                try:
                    import threading; self.cond = threading.Condition(); th = threading.Thread(target=self._run)
                    th.daemon = True; th.start()
                except Exception: self.cond = None
            def send(self, data):
                if self.error is not None or self.stopped: raise self.error or IOError("sender stopped")
                if self.cond is None: self.t.send(data); return
                with self.cond: self.q.append(data); self.cond.notify()
            def _run(self):
                while not self.stopped:
                    with self.cond:
                        while not self.q and not self.stopped: self.cond.wait(0.5)
                        if self.stopped: return
                        data = self.q.popleft()
                    try: self.t.send(data)
                    except Exception as ex: self.error = ex; return
            def stop(self):
                self.stopped = True
                if self.cond is not None:
                    with self.cond: self.q.clear(); self.cond.notify()
        class MapConnection(object):
            kind = "own"; owns_position = True; server_relays_ping = True; OFF, HANDSHAKE, LOGIN, READY = range(4)
            STATE_NAMES = ["OFF", "HANDSHAKE", "LOGIN", "READY"]
            def __init__(self, host, port, user, password):
                self.host, self.port, self.user, self.password = host, port, user, password
                self.t = self.gave_up = self.connecting = self.sender = None; self.state = self.OFF
                self.buf = bytearray()
                self.next_try = self.login_failures = self.last_sent = self.state_since = self.ready_since = 0
                self.backoff = 3; self.kicks = []; self.name = user; self.unreachable_reported = False
            def close(self):
                if self.connecting is not None:
                    pend, self.connecting = self.connecting, None; pend["abandon"] = True
                    if pend["done"] and pend["t"] is not None: safe(lambda: pend["t"].close())
                if self.sender is not None: safe(self.sender.stop); self.sender = None
                if self.t: self.t.close()
                self.t = None; self.state = self.OFF; self.buf = bytearray()
            def _drop(self, events, kind, detail, retry_in):
                was = self.state; self.close(); now = time.time()
                self._debug(events, "dropped in state %s: %s %s" % (self.STATE_NAMES[was], kind, detail))
                if was == self.LOGIN and kind == "eof":
                    self.login_failures += 1
                    if self.login_failures >= 3:
                        self.gave_up = ("The map server closed the connection during login 3 "
                                        "times. Check the map username and password (World Map "
                                        "settings page). If they are right, tick Print debug lines on the Modules tab.")
                        events.append(("status", self.gave_up, True)); return
                    events.append(("status", "The server closed the connection during login "
                                             "(usually a wrong username or password). Retrying in "
                                             "%d seconds." % retry_in, True))
                elif was == self.LOGIN:
                    events.append(("status", "Problem while logging in (%s). Retrying in %d "
                                             "seconds." % (detail, retry_in), True))
                elif was == self.READY:
                    if kind == "eof" and now - self.ready_since < 6:
                        why = ("Logged in, but the server dropped the connection right away. Is "
                               "this map account also logged in somewhere else (Enhanced Map, for example)?")
                    elif kind == "eof": why = "Lost connection to the map server."
                    else: why = "Connection problem (%s)." % detail
                    self.kicks = [k for k in self.kicks if now - k < 300] + [now]
                    if len(self.kicks) >= 4:
                        self.gave_up = ("Kept getting disconnected. Is this map account also "
                                        "logged in somewhere else (Enhanced Map, for example)? "
                                        "Use a separate account, then click Reconnect.")
                        events.append(("status", self.gave_up, True)); return
                    events.append(("status", "%s Reconnecting in %d seconds." % (why, retry_in), True))
                else:
                    what = {"eof": "The server closed the connection",
                            "timeout": "The server didn't answer"}.get(kind, "Connection problem")
                    events.append(("status", "%s (%s). Retrying in %d seconds."
                                   % (what, detail or "handshake", retry_in), False))
                self.next_try = now + retry_in
            def _debug(self, events, text):
                if HOST.debug: events.append(("status", "[debug] " + text, True))
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
                        pend = self.connecting = {"done": False, "t": None, "err": None, "abandon": False}
                        def run(p=pend, host=self.host, port=self.port):
                            try: p["t"] = open_transport(host, port)
                            except Exception as ex: p["err"] = ex
                            if p["abandon"] and p["t"] is not None: p["t"].close()
                            p["done"] = True
                        try: import threading; th = threading.Thread(target=run); th.daemon = True; th.start()
                        except Exception: run()
                    if not pend["done"]: return events
                    self.connecting = None; now = time.time()
                    try:
                        if pend["err"] is not None: raise pend["err"]
                        if pend["t"] is None: raise IOError("no connection")
                        self.t = pend["t"]
                    except Exception as e:
                        self.backoff = min(self.backoff * 2, 60)
                        events.append(("status", "Can't reach the map server at %s:%d (%s). " "Retrying in %d seconds."
                                       % (self.host, self.port, short_error(e), self.backoff),
                                       not self.unreachable_reported))
                        self.unreachable_reported = True; self.next_try = now + self.backoff; return events
                    self.state = self.HANDSHAKE; self.state_since = now; self.buf = bytearray()
                    try: self.sender = Sender(self.t)
                    except Exception: self.sender = None
                    self.send(packet(0x2B, b"\x00")); events.append(("status", "Connecting...", False))
                closed = None; snd = self.sender
                if snd is not None and snd.error is not None:
                    e = snd.error; closed = ("error", "%s: %s" % (e.__class__.__name__, short_error(e)))
                try:
                    chunk = self.t.recv() if self.t else b""
                    if chunk:
                        if HOST.debug: self._debug(events, "received %d bytes" % len(chunk))
                        self.buf.extend(chunk)
                        if len(self.buf) > 1 << 20: raise IOError("too much data")
                except EOFError: closed = ("eof", "")
                except Exception as e: closed = ("error", "%s: %s" % (e.__class__.__name__, short_error(e)))
                while len(self.buf) >= 3 and self.t is not None:
                    pid = self.buf[0]; size = self.buf[1] | (self.buf[2] << 8)
                    if size < 3: self._drop(events, "garbled", "bad packet size", 10); return events
                    if len(self.buf) < size: break
                    data = bytes(self.buf[:size]); del self.buf[:size]
                    if HOST.debug:
                        self._debug(events, "packet 0x%02X (%d bytes) in state %s"
                                    % (pid, size, self.STATE_NAMES[self.state]))
                    try: self._handle(pid, data, events)
                    except ValueError as e: self._debug(events, "skipped malformed packet 0x%02X: %s" % (pid, e))
                if closed and self.t is not None:
                    self._drop(events, closed[0], closed[1], 30 if self.state == self.LOGIN else 10); return events
                if (self.t is not None and self.state in (self.HANDSHAKE, self.LOGIN) and now - self.state_since > 15):
                    self._drop(events, "timeout", "no reply in 15 s", 15)
                return events
            def _handle(self, pid, data, events):
                r = Reader(data)
                if pid == 0x2B and self.state == self.HANDSHAKE:
                    self.state = self.LOGIN; self.state_since = time.time()
                    self._debug(events, "handshake ok (server protocol "
                                        "%d), sending login for '%s'" % (r.u8(), self.user))
                    self.send(pk_login(self.user, self.password))
                elif pid == 0x1F and self.state == self.LOGIN:
                    if r.u8() == 1:
                        r.u8(); self.name = r.ascii(r.u8()) or self.user; self.state = self.READY
                        self.ready_since = time.time(); self.login_failures = 0; self.backoff = 3
                        self.unreachable_reported = False
                        events.append(("status", "Connected as %s." % self.name, True))
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
                import clr; from System import Array, Byte, Action, Delegate, AppDomain
                from System.Reflection import BindingFlags; from System.Collections.Concurrent import ConcurrentQueue
                self._Array, self._Byte, self._Delegate, self._AppDomain = (Array, Byte, Delegate, AppDomain)
                inst = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance
                stat = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static
                mtype = API.GetType().Assembly.GetType("ClassicUO.Game.Managers.EnhancedMap.EnhancedMapManager")
                if mtype is None: raise LookupError("this TazUO has no built-in Enhanced Map")
                p_instance = mtype.GetProperty("Instance", stat)
                self._p_connected = mtype.GetProperty("IsConnected", inst)
                self._p_config = mtype.GetProperty("Config", stat)
                self._m_reconnect = mtype.GetMethod("Reconnect", inst); f_client = mtype.GetField("_client", inst)
                if None in (p_instance, self._p_connected, self._p_config, f_client):
                    raise LookupError("TazUO's Enhanced Map internals have changed")
                self._asm = API.GetType().Assembly; self._manager = p_instance.GetValue(None)
                self._client = f_client.GetValue(self._manager); ctype = self._client.GetType()
                self._f_connection = ctype.GetField("_connection", inst)
                self._m_send = ctype.GetMethod("SendRaw", inst); self._f_onframe = ctype.GetField("OnFrame", inst)
                if None in (self._f_connection, self._m_send, self._f_onframe):
                    raise LookupError("TazUO's Enhanced Map internals have changed")
                try: self._handler, self._queue = self._make_handler()
                except Exception:
                    self._queue = ConcurrentQueue[object](); queue = self._queue
                    def on_frame(pid, payload):
                        try:
                            if pid in (0x33, 0x27) and queue.Count < 200: queue.Enqueue((int(pid), payload))
                        except Exception: pass
                    self._handler = Action[Byte, Array[Byte]](on_frame)
                self._hooked = False
            @staticmethod
            def _make_handler():
                import clr; from System import Array, Byte, Int32, Action, Tuple, Type
                from System.Collections.Concurrent import ConcurrentQueue
                from System.Linq.Expressions import Expression, ParameterExpression
                t_byte, t_bytes, t_int = (clr.GetClrType(Byte), clr.GetClrType(Array[Byte]), clr.GetClrType(Int32))
                ftype = Tuple[Byte, Array[Byte]]; queue = ConcurrentQueue[ftype]()
                p_id = Expression.Parameter(t_byte, "id"); p_payload = Expression.Parameter(t_bytes, "payload")
                q = Expression.Constant(queue); as_int = Expression.Convert(p_id, t_int)
                wanted = Expression.OrElse(Expression.Equal(as_int, Expression.Constant(0x33, t_int)),
                                           Expression.Equal(as_int, Expression.Constant(0x27, t_int)))
                room = Expression.LessThan(Expression.Property(q, "Count"), Expression.Constant(200, t_int))
                ctor = clr.GetClrType(ftype).GetConstructor(Array[Type]([t_byte, t_bytes]))
                enqueue = Expression.Call(q, queue.GetType().GetMethod("Enqueue"),
                                          Array[Expression]([Expression.New(ctor,
                                                  Array[Expression]([p_id, p_payload]))]))
                body = Expression.IfThen(Expression.AndAlso(wanted, room), enqueue)
                lam = Expression.Lambda[Action[Byte, Array[Byte]]](body, Array[ParameterExpression]([p_id, p_payload]))
                return lam.Compile(), queue
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
            def reconnect(self):
                if self._m_reconnect is not None: self._m_reconnect.Invoke(self._manager, None)
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
                if None in (mouse, selected, ui): raise LookupError("TazUO's mouse internals have changed")
                self._pos = mouse.GetField("Position", stat); self._mclick = mouse.GetField("MClickPosition", stat)
                self._mdown = mouse.GetProperty("MButtonPressed", stat); self._mdown_get = None
                self._over_world = ui.GetProperty("IsMouseOverWorld", stat)
                self._object = selected.GetField("Object", stat)
                if None in (self._pos, self._mclick, self._mdown, self._over_world, self._object):
                    raise LookupError("TazUO's mouse internals have changed")
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
            def ready(self):
                try: return self.bridge.is_connected()
                except Exception: return False
            @property
            def name(self):
                try: return (self.bridge.config() or {}).get("user", "")
                except Exception: return ""
            def poll(self):
                events = []; connected = self.ready
                if connected != self.was_connected:
                    if connected:
                        events.append(("status", "Using TazUO's Enhanced Map login (%s)."
                                       % (self.name or "connected"), True))
                    elif self.was_connected:
                        now = time.time(); self.drops = [d for d in self.drops if now - d < self.DROP_WINDOW] + [now]
                        if len(self.drops) >= self.DROP_LIMIT and not self.unhooked_for_drops:
                            safe(self.bridge.unhook); self.unhooked_for_drops = True
                            events.append(("status", "TazUO's Enhanced Map keeps dropping, so Map "
                                           "Pings stopped listening on it (your pings still go "
                                           "out; others' don't show). If it still drops, the "
                                           "cause is elsewhere. Click Reconnect to listen again.", True))
                        else:
                            events.append(("status", "TazUO's Enhanced Map connection dropped; "
                                                     "TazUO will reconnect.", True))
                    else: events.append(("status", "Waiting for TazUO's Enhanced Map to connect...", False))
                    self.was_connected = connected
                try: frames = self.bridge.frames()
                except Exception: frames = []
                for pid, payload in frames:
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
        def short_error(e): s = str(e) or e.__class__.__name__; return s if len(s) < 60 else s[:57] + "..."
        _xy = {}
        def xy_fields(t):
            got = _xy.get(t)
            if got is None: got = _xy[t] = (t.GetField("X"), t.GetField("Y"))
            return got
        def spot_of(obj):
            if obj is None: return None
            try: return int(obj.X), int(obj.Y)
            except Exception: pass
            try:
                t = obj.GetType(); fx, fy = xy_fields(t)
                if fx is not None and fy is not None: return int(fx.GetValue(obj)), int(fy.GetValue(obj))
                px, py = t.GetProperty("X"), t.GetProperty("Y")
                if px is not None and py is not None: return int(px.GetValue(obj, None)), int(py.GetValue(obj, None))
            except Exception: pass
            return None
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
                if pm == m and px > 0:
                    dist = max(abs(x - px), abs(y - py))
                    where = ("on you" if dist == 0 else "%d tiles %s" % (dist, Kit.compass(x - px, y - py)))
                else: where = "on %s" % facet_name(m)
                who = (who or "You") if local else sender
                say("%s pinged %s %s (%d, %d, %s)." % ("you" if who == "You" else who, label, where, x, y,
                                                       facet_name(m)), hue)
                self.hist_seq += 1; p.entry = HistEntry(self.hist_seq, now, t, str(who), x, y, m, bool(local))
                self.history.append(p.entry)
                if len(self.history) > HISTORY_MAX: del self.history[:len(self.history) - HISTORY_MAX]
                self.hist_ver += 1
                if not local and serial: API.HeadMsg("%s: %s %s" % (sender, label, where), serial, hue)
                if pm == m:
                    key = (x, y, m); self.marked[key] = self.marked.get(key, 0) + 1; p.marked = True
                    safe(lambda: API.MarkTile(x, y, hue, m))
                    if (not auto and px > 0 and x > 0 and y > 0 and max(abs(x - px), abs(y - py)) > 2):
                        try: API.TrackingArrow(x, y, ARROW_ID); self.arrow_for = p
                        except Exception: pass
                name = ("%s: %s %s" % (who, label, time.strftime("%H:%M:%S"))).replace(",", " ")
                if ATLAS.map_open(True):
                    try: API.AddMapMarker(name, x, y, m, mapcolor); self.markers.append((now + 60, name))
                    except Exception: pass
                    if len(self.markers) > MARKERS_CAP:
                        ATLAS.loose.update([n for _, n in self.markers[:-MARKERS_CAP]]); del self.markers[:-MARKERS_CAP]
                self._play_sound(t, now)
            def _play_sound(self, t, now):
                if not OPT["sounds"] or now - self.last_sound < 0.3: return
                self.last_sound = now; safe(lambda: API.PlaySound(PING_SOUNDS[t]))
            def update(self):
                if not self.pings and not self.markers: return
                now = time.time(); pm = None; stay = OPT["ping_secs"]
                for p in list(self.pings):
                    if now - p.created >= stay: self._expire(p); continue
                    if now < p.next_pulse: continue
                    if pm is None: pm = self.player()[2]
                    if p.map == pm:
                        p.next_pulse = now + self.PULSE; _, hue, gfx, _ = TYPE_INFO[p.type]
                        try:
                            API.CreateEffect(gfx, type=API.EffectType.FixedXYZ, hue=hue,
                                                  sourceX=p.x, sourceY=p.y, duration=self.PULSE)
                        except Exception: pass
                if self.markers and now >= self.markers[0][0] and self._map_ready(now) and ATLAS.map_open(True):
                    while self.markers and now >= self.markers[0][0]:
                        name = self.markers.pop(0)[1]; safe(lambda: API.RemoveMapMarker(name))
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
                    if left <= 0: self.marked.pop(key, None); safe(lambda: API.RemoveMarkedTile(p.x, p.y, p.map))
                    else: self.marked[key] = left
                    p.marked = False
                if self.arrow_for is p: self.arrow_off()
            def arrow_entry(self):
                a = self.arrow_for
                if a is None or isinstance(a, HistEntry): return a
                return a.entry
            def arrow_to(self, e): API.TrackingArrow(e.x, e.y, ARROW_ID); self.arrow_for = e
            def arrow_off(self):
                if self.arrow_for is not None: safe(lambda: API.TrackingArrow(-1, -1, ARROW_ID)); self.arrow_for = None
            def clear(self):
                for p in list(self.pings):
                    try: self._expire(p)
                    except Exception:
                        if p in self.pings: self.pings.remove(p)
                if self.markers:
                    names = [n for _, n in self.markers]
                    if ATLAS.map_open(True):
                        for name in names: safe(lambda: API.RemoveMapMarker(name))
                    else: ATLAS.loose.update(names)
                self.markers = []; safe(lambda: API.TrackingArrow(-1, -1, ARROW_ID))
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
                self.app = app
                self.st = {"g": None, "shutting": False, "minimized": False, "docked": False, "queue": []}
                self.queue = Kit.queuer(self.st); self.c, self.store, self.rows = {}, ({}, {}), []
                self.page, self.next_draw = 0, 0.0; self.drawn = self.drawn_pos = None
            def start(self):
                st = self.st; st["shutting"] = False
                st["minimized"] = Kit.load_min(HIST_MIN_KEY) or bool(safe(lambda: HOST.dock_wanted(HIST_DOCK), False))
                safe(lambda: HOST.dock_add(HIST_DOCK, Kit.dock_hooks(
                    HIST_TITLE, 0x14EB, st, st, self.queue("redraw"), scale=True)))
                if Kit.get_var(HIST_OPEN_KEY, "0") == "1": self.build()
            def toggle_open(self):
                st = self.st
                if st["g"] is not None and not (st["minimized"] or st["docked"]): self.close(); return
                st["minimized"] = st["docked"] = False; safe(lambda: HOST.dock_forget(HIST_DOCK))
                Kit.save_min(HIST_MIN_KEY, False); Kit.put_var(HIST_OPEN_KEY, "1"); self.build()
            def close(self):
                st = self.st; g = st["g"]
                if g is None: return
                Kit.save_pos(HIST_POS_KEY, g); st["g"], st["docked"] = None, False
                safe(lambda: HOST.dock_forget(HIST_DOCK)); Kit.put_var(HIST_OPEN_KEY, "0"); self.c, self.rows = {}, []
                Kit.dispose(g)
            def shutdown(self):
                st = self.st; st["shutting"] = True; safe(lambda: HOST.dock_remove(HIST_DOCK)); g = st["g"]
                if g is not None:
                    Kit.save_pos(HIST_POS_KEY, g); Kit.save_min(HIST_MIN_KEY, st["minimized"] and not st["docked"])
                    st["g"] = None; self.c, self.rows = {}, []; Kit.dispose(g)
            def _disposed(self, g):
                def handler(*args):
                    if self.st["g"] is g and not self.st["shutting"]: self.st["g"] = None; self.c, self.rows = {}, []
                return handler
            def build(self):
                st = self.st
                g, store, c, w, h, x, y, old = open_window(st, st, HIST_POS_KEY, (HIST_MINI_W, HIST_MINI_H),
                    (560, list_h(HISTORY_ROWS, HIST_ROW_H)), (260, 160), HIST_TITLE, HIST_DOCK, self.queue, "Close")
                rows = []
                if not st["minimized"]:
                    M = Kit.MARGIN; IW = w - 2 * M; yt = M + 30 + Kit.GAP; Kit.add_section(g, M, yt, IW, 36)
                    bx = M + 12
                    Kit.art_button(g, store, "clear", Kit.ART_CLOSE, bx, yt + 7, "Clear",
                                   "Empty the history (the pings on screen stay)", on_click=self.queue("clear"))
                    bx += 35 + Kit.text_w("Clear") + 16
                    Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, bx, yt + 7, "Arrow off",
                                   "Take the tracking arrow down", on_click=self.queue("arrow_off"))
                    right = M + IW - 8; c["pg"] = Kit.add_label(g, "", right - 100, yt + 10, Kit.HUE_INFO)
                    Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 56, yt + 8, None,
                                   "Previous page (newer pings)", on_click=self.queue(("page", -1)))
                    Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 34, yt + 8, None,
                                   "Next page (older pings)", on_click=self.queue(("page", 1)))
                    yl = yt + 36 + Kit.GAP; Kit.add_section(g, M, yl, IW, 30 + HISTORY_ROWS * HIST_ROW_H + 8)
                    cx = M + 12; xs = []
                    for head, cw in HIST_COLS:
                        Kit.add_label(g, head, cx, yl + 6, Kit.HUE_TITLE); xs.append((cx, cw)); cx += cw + 8
                    Kit.add_label(g, "Where", cx, yl + 6, Kit.HUE_TITLE); c["where_w"] = M + IW - 12 - cx
                    for k in range(HISTORY_ROWS):
                        ry = yl + 30 + k * HIST_ROW_H
                        r = {"val": None, "prev": None, "changed": 0.0, "tip": None, "vis": True, "sig": None}
                        r["labels"] = [Kit.add_label(g, "", xx, ry + 3, Kit.HUE_TEXT) for xx, _ in xs]
                        r["where"] = Kit.add_label(g, "", cx, ry + 3, Kit.HUE_INFO); r["widths"] = [cw for _, cw in xs]
                        r["catch"] = Kit.catcher(g, M + 6, ry, IW - 12, HIST_ROW_H,
                                                 Kit.row_clicker(r, self.queue, "arrow"), HIST_TIP)
                        rows.append(r)
                self.c, self.store, self.rows = c, store, rows
                show_window(g, x, y, w, h, st, st, self._disposed, HIST_POS_KEY); self.drawn = None; self.refresh()
                Kit.dispose(old)
            def tick(self):
                st = self.st
                if st["g"] is not None and Kit.was_clicked(self.store, "close"): self.close(); return
                q = st["queue"]
                while q:
                    a = q.pop(0); kind = a[0] if isinstance(a, tuple) else a
                    if kind == "toggle_min":
                        st["minimized"] = not st["minimized"]; st["docked"] = False
                        safe(lambda: HOST.dock_forget(HIST_DOCK)); Kit.save_min(HIST_MIN_KEY, st["minimized"])
                        if st["g"] is not None: self.build()
                    elif kind == "to_bar": safe(lambda: HOST.dock_to_bar(HIST_DOCK, HIST_TITLE))
                    elif kind == "redraw":
                        if st["g"] is not None: self.build()
                    elif kind == "settings": HOST.show_settings("pings")
                    elif kind == "page": self.page = max(0, self.page + a[1]); self.next_draw = 0.0
                    elif kind == "clear":
                        disp = self.app.display; del disp.history[:]; disp.hist_ver += 1; self.page = 0
                    elif kind == "arrow_off": self.app.display.arrow_off()
                    elif kind == "arrow": self.arrow(a[1])
                    elif kind == "follow": self.follow(a[1])
                if st["g"] is None or (st["minimized"] and st["docked"]): return
                self.refresh()
            def entry(self, seq): return next((e for e in self.app.display.history if e.seq == seq), None)
            def arrow(self, seq):
                disp = self.app.display; e = self.entry(seq)
                if e is None: return
                if disp.arrow_entry() is e: disp.arrow_off(); return
                pm = disp.player()[2]
                if pm != e.map: say("that ping is on %s; you are on %s." % (facet_name(e.map), facet_name(pm))); return
                try: disp.arrow_to(e)
                except Exception as ex:
                    say("couldn't show the tracking arrow (%s)." % short_error(ex), Kit.HUE_BAD); return
                say("tracking arrow on %s's %s (%d, %d)." % (e.who, label_of(e.type), e.x, e.y))
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
                try: mobs = list(API.GetAllMobiles() or [])
                except Exception: mobs = []
                for m in mobs:
                    try:
                        if str(m.Name or "").strip().lower() != low: continue
                        d = int(m.Distance)
                        if bd is None or d < bd: best, bd = int(m.Serial), d
                    except Exception: continue
                return best
            def where_text(self, e, px, py, pm):
                spot = "(%d, %d)" % (e.x, e.y)
                if pm == e.map and px > 0:
                    dist = max(abs(e.x - px), abs(e.y - py))
                    if dist == 0: return "here " + spot
                    return "%d tile%s %s  %s" % (dist, "" if dist == 1 else "s", Kit.compass(e.x - px, e.y - py), spot)
                return "%s %s" % (facet_name(e.map), spot)
            def refresh(self):
                st = self.st; disp = self.app.display; hist = disp.history; c = self.c
                if st["minimized"]:
                    if self.drawn == disp.hist_ver: return
                    self.drawn = disp.hist_ver
                    if hist:
                        e = hist[-1]
                        txt = "%s: %d ping%s, last %s %s" % (HIST_TITLE, len(hist), "" if len(hist) == 1 else "s",
                                                            label_of(e.type), e.who)
                    else: txt = "%s: no pings yet" % HIST_TITLE
                    if c.get("status") is not None: Kit.set_text(c["status"], Kit.fit(txt, HIST_MINI_W - 90))
                    return
                now = time.time(); arrow = disp.arrow_entry(); sig = (disp.hist_ver, self.page, arrow)
                if sig == self.drawn and now < self.next_draw: return
                pos = disp.player()[:3] if hist else (0, 0, -1)
                if sig == self.drawn and pos == self.drawn_pos: self.next_draw = now + 1.0; return
                self.drawn, self.next_draw, self.drawn_pos = sig, now + 1.0, pos; n = len(hist)
                per = max(1, len(self.rows)); pages = max(1, (n + per - 1) // per)
                self.page = max(0, min(pages - 1, self.page))
                if c.get("pg") is not None:
                    Kit.set_text(c["pg"], ("%d/%d" % (self.page + 1, pages)) if pages > 1 else "")
                px, py, pm = pos; first = n - 1 - self.page * per; where_w = c.get("where_w", 200)
                for k, r in enumerate(self.rows):
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
                        texts = (time.strftime("%H:%M:%S", time.localtime(e.at)), label_of(e.type), e.who)
                        hues = (Kit.HUE_INFO, hue, Kit.HUE_TEXT if not e.local else Kit.HUE_INFO)
                        for j, lbl in enumerate(r["labels"]):
                            Kit.set_text(lbl, Kit.fit(texts[j], r["widths"][j]), hues[j])
                        Kit.set_text(r["where"], Kit.fit(("> " if on else "") + where, where_w),
                                     Kit.HUE_TITLE if on else Kit.HUE_INFO)
                        tip = ("Take the tracking arrow down" if on else HIST_TIP) + ("" if e.local else HIST_ALT)
                        if tip != r["tip"]: r["tip"] = tip; Kit.with_tip(r["catch"], tip)
                    self._show(r, True)
            def _show(self, r, on, only_first=False):
                want = ("first" if only_first else on)
                if r["vis"] == want: return
                r["vis"] = want; parts = r["labels"] + [r["where"], r["catch"]]
                for j, ctl in enumerate(parts):
                    v = on and (not only_first or j == 0)
                    try: ctl.IsVisible = v
                    except Exception: pass
        class PingApp(object):
            def __init__(self):
                self.mouse = self.gesture = self.guide = self.bridge = self.bridge_error = self.conn = None
                self.aim = self.status_label = self.last_pos = None; self.guide_labels, self.recent_pings = {}, {}
                self.bridge_tried = self._shut = False
                self.next_link_check = self.last_pos_sent = self.next_pos_read = 0
                self.last_ping_sent = self.last_auto_sent = 0; self.recent_order = collections.deque()
                self.settings = Settings(); self.display = PingDisplay()
                self.pending, self.jobs, self.outbox, self.inbox, self.hooked = [], [], [], [], []
                self.status_text, self.status_w = "", 300; self.history = HistoryWindow(self)
            def set_status(self, text, also_journal=True):
                self.status_text = text
                if self.status_label is not None: Kit.set_text(self.status_label, Kit.fit(text, self.status_w))
                if also_journal: say(journal_case(text))
            def _queue_ping(self, t):
                def fn(*args):
                    if bool(safe(lambda: HOST.typing(), False)): return
                    self.pending.append(("target", t))
                return fn
            def save_setup(self):
                if self.conn and self.conn.kind == "tazuo":
                    self.set_status("Saved. TazUO's Enhanced Map login is on, so Map Pings keeps using that."); return
                if self.conn: self.conn.close(); self.conn = None
                self.choose_link()
            def apply_options(self):
                if OPT["gesture"] and self.mouse is None: self.init_mouse()
                elif not OPT["gesture"]: self.mouse = self.gesture = None; self.close_guide()
                self.jobs.append(("link",))
            def connect(self):
                if self.conn: self.conn.close()
                s = self.settings; self.conn = MapConnection(s.host, s.port, s.user, s.password)
                self.set_status("Connecting to %s:%d..." % (s.host, s.port), also_journal=False)
            def get_bridge(self):
                if not self.bridge_tried:
                    self.bridge_tried = True
                    try: self.bridge = TazUOBridge()
                    except Exception as e: self.bridge = None; self.bridge_error = short_error(e)
                return self.bridge
            def tazuo_available(self):
                b = self.get_bridge()
                if b is None: return False
                try: cfg = b.config()
                except Exception: return False
                return bool(cfg and cfg["configured"])
            def choose_link(self, announce=True):
                mode = (OPT["connection"] or "auto").lower(); current = self.conn.kind if self.conn else None
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
                        self.set_status("Turn on Enhanced Map in TazUO, or enter a separate map "
                                        "login (World Map settings page).")
                    else: self.set_status("Enter your map server details to start."); self.inbox.append(("open_setup",))
            def send_ping(self, x, y, m, t):
                now = time.time()
                if now - self.last_ping_sent < PING_RATE_SECS: return
                self.last_ping_sent = now; self._send(x, y, m, t)
            def send_auto(self, x, y, m, t, who=None):
                now = time.time()
                if now - self.last_auto_sent < PING_RATE_SECS: return False
                self.last_auto_sent = now; self._send(x, y, m, t, who=who, auto=True); return True
            def _send(self, x, y, m, t, who=None, auto=False):
                self.display.show("You", x, y, m, t, local=True, who=who, auto=auto)
                if self.conn and self.conn.ready:
                    if self.conn.server_relays_ping:
                        self.outbox.append(packet(0x33, struct.pack("<HHBB", x & 0xFFFF, y & 0xFFFF, m & 0xFF,
                                                                    t & 0xFF)))
                    typed = pk_typed_alert(x, y, m, t)
                    if typed: self.outbox.append(typed)
                    self.outbox.append(pk_alert(x, y))
                else:
                    note = "Not connected: only you can see that ping."
                    self.set_status(note, also_journal=not auto or self.status_text != note)
            AIM_SECONDS = 10
            def target_ping(self, t):
                say("target a spot for %s (target yourself for where you stand)." % label_of(t)); self.aim = None
                tm = safe(Picker._tm)
                if tm is not None:
                    aim = {"t": t, "fired": False, "spot": None, "d": None, "tm": tm,
                           "until": time.time() + self.AIM_SECONDS}
                    def got(obj, aim=aim): aim["spot"] = spot_of(obj); aim["fired"] = True
                    try:
                        from System import Action; aim["d"] = Action[object](got)
                        tm.SetTargeting(aim["d"], Picker.CURSOR_TARGET, Picker.neutral); self.aim = aim
                        safe(lambda: HOST.claim_cursor("pings", self.AIM_SECONDS)); return
                    except Exception: pass
                self.jobs.append(("aim", t))
            def poll_aim(self):
                aim = self.aim
                if aim is None: return
                if not aim["fired"]:
                    tm = aim["tm"]; ours = False
                    if tm is not None:
                        try: ours = bool(tm.IsCurrentTargetingAction(aim["d"]))
                        except Exception: ours = False
                    if ours and time.time() < aim["until"]: return
                    self.aim = None; HOST.release_cursor("pings")
                    if ours: safe(lambda: tm.CancelTarget())
                    return
                self.aim = None; HOST.release_cursor("pings"); self.aimed(aim["t"], aim["spot"])
            def aimed(self, t, spot):
                if spot is None: return
                x, y = spot
                if x <= 0 or y <= 0: return
                self.send_ping(x, y, int(API.GetMap()), t)
            def drop_aim(self):
                aim, self.aim = self.aim, None; safe(lambda: HOST.release_cursor("pings"))
                tm = safe(Picker._tm) if aim is not None else None
                if tm is None or aim["fired"]: return
                def cancel():
                    if tm.IsCurrentTargetingAction(aim["d"]): tm.CancelTarget()
                safe(lambda: Kit.on_client(cancel, fallback=False))
            def target_ping_blocking(self, t):
                target = API.RequestAnyTarget(10)
                if target is None: return
                try: x, y = int(target.X), int(target.Y)
                except Exception: return
                self.inbox.append(("aimed", t, (x, y)))
            def share_position(self):
                if not self.conn or not self.conn.ready or not self.conn.owns_position: return
                now = time.time()
                if now < self.next_pos_read: return
                self.next_pos_read = now + 0.5; pos = None
                if OPT["share"]:
                    p = API.Player
                    try: pos = (int(p.X), int(p.Y), int(API.GetMap()))
                    except Exception: pass
                if pos is None or pos[0] <= 0:
                    if now - self.conn.last_sent > 20: self.outbox.append(packet(0xFE))
                    return
                if ((pos != self.last_pos and now - self.last_pos_sent >= 1.0) or now - self.last_pos_sent >= 10):
                    flag = 0
                    try:
                        if p.IsDead: flag = 4
                        elif p.IsPoisoned: flag = 1
                        elif p.IsYellowHits: flag = 2
                        elif p.IsParalyzed: flag = 3
                        elif p.IsHidden: flag = 5
                        stats = (int(p.Hits), int(p.Stamina), int(p.Mana), int(p.HitsMax),
                                 int(p.StaminaMax), int(p.ManaMax))
                    except Exception: stats = (0, 0, 0, 0, 0, 0)
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
                inbox = self.inbox
                if inbox: self.inbox = []
                for ev in inbox:
                    if ev[0] == "open_setup": HOST.show_settings("pings")
                    elif ev[0] == "aimed": self.aimed(ev[1], ev[2])
                    else: self.handle(ev)
                self.poll_aim()
                if self.conn: self.share_position()
                self.poll_gesture(); self.display.update(); self.history.tick()
            def thread_step(self):
                while self.jobs:
                    action = self.jobs.pop(0)
                    if action[0] == "save_setup": self.save_setup()
                    elif action[0] == "link": self.choose_link(announce=False)
                    elif action[0] == "aim": self.target_ping_blocking(action[1])
                    elif action[0] == "reconnect":
                        if self.conn and self.conn.kind == "tazuo":
                            self.conn.reset(); self.set_status("Asked TazUO's Enhanced Map to reconnect.")
                        elif self.settings.complete and (OPT["connection"] or "auto").lower() != "tazuo":
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
                if not OPT["gesture"]: self.mouse = None; return
                try: self.mouse = TazUOMouse()
                except Exception as e:
                    self.mouse = None
                    say("mouse-wheel pings aren't available (%s): use the ping buttons or the hotkeys."
                        % short_error(e))
            @staticmethod
            def drag_direction(dx, dy):
                if max(abs(dx), abs(dy)) < OPT["drag"]: return None
                if abs(dx) > abs(dy): return "right" if dx > 0 else "left"
                return "down" if dy > 0 else "up"
            def poll_gesture(self):
                m = self.mouse
                if m is None: return
                try: down = m.middle_down()
                except Exception: return
                if down and self.gesture is None:
                    try: tile = m.tile_under_mouse(); start = m.position(m._mclick)
                    except Exception: tile, start = None, (0, 0)
                    self.gesture = {"tile": tile, "start": start, "dir": None, "map": int(API.GetMap())}
                    if tile is not None: self.show_guide(start)
                elif down and self.gesture is not None:
                    if self.gesture["tile"] is None: return
                    try: x, y = m.position()
                    except Exception: return
                    d = self.drag_direction(x - self.gesture["start"][0], y - self.gesture["start"][1])
                    if d != self.gesture["dir"]: self.gesture["dir"] = d; self.update_guide(d)
                elif not down and self.gesture is not None:
                    g, self.gesture = self.gesture, None; self.close_guide(); t = GESTURE.get(g["dir"])
                    if g["tile"] is not None and t is not None: self.send_ping(g["tile"][0], g["tile"][1], g["map"], t)
            def show_guide(self, center):
                self.close_guide()
                try:
                    G = API.Gumps; w, h = 180, 104; gump = G.CreateGump(False, False); scale = Kit.render_scale() or 1.0
                    cx, cy = int(round(center[0] / scale)), int(round(center[1] / scale))
                    Kit.place(gump, cx - w // 2, cy - h // 2, w, h); Kit.add_window_frame(gump, w, h, corners=False)
                    Kit.add_section(gump, 6, 6, w - 12, h - 12)
                    spots = {"up": (58, 9), "right": (110, 43), "down": (58, 77), "left": (11, 43)}
                    self.guide_labels = {}
                    for d, (lx, ly) in spots.items():
                        t = GESTURE[d]; lab = G.CreateGumpLabel(label_of(t), 946); lab.SetRect(lx, ly, 70, 18)
                        gump.Add(lab); self.guide_labels[d] = (lab, t)
                    plus = G.CreateGumpLabel("+", 53); plus.SetRect(w // 2 - 3, h // 2 - 9, 10, 18); gump.Add(plus)
                    G.AddGump(gump); safe(lambda: SNAP.skip_gump(gump)); self.guide = gump
                except Exception: self.guide = None
            def update_guide(self, chosen):
                for d, (lab, t) in self.guide_labels.items():
                    try:
                        lab.Text = "[" + label_of(t) + "]" if d == chosen else label_of(t)
                        lab.Hue = TYPE_INFO[t][1] if d == chosen else 946
                    except Exception: pass
            def close_guide(self):
                if self.guide is not None: safe(lambda: self.guide.Dispose())
                self.guide, self.guide_labels = None, {}
            def register_hotkeys(self):
                self.unregister_hotkeys()
                for key, combo in HOTKEYS.items():
                    if combo:
                        try: API.OnHotKey(combo, self._queue_ping(TYPE_KEYS[key]))
                        except Exception:
                            say("can't use '%s' as the %s hotkey." % (combo, label_of(TYPE_KEYS[key])), Kit.HUE_BAD)
                            continue
                        self.hooked.append(combo); HOST.hotkeys_owned[combo] = TITLE
                        safe(lambda: HOST.hotkey_note(combo, TITLE, "%s ping" % label_of(TYPE_KEYS[key])))
            def unregister_hotkeys(self):
                for combo in self.hooked:
                    safe(lambda: API.OnHotKey(combo)); HOST.hotkeys_owned.pop(combo, None)
                    safe(lambda: HOST.hotkey_drop(combo, TITLE))
                self.hooked = []
            def shutdown(self):
                if self._shut: return
                self._shut = True; self.unregister_hotkeys(); self.drop_aim(); self.close_guide()
                safe(self.history.shutdown); safe(self.display.clear)
                if self.conn: self.conn.close()
            def start(self):
                self.init_mouse(); self.register_hotkeys(); self.history.start()
                say("on; its ping buttons are on the World Map settings page.", Kit.HUE_GOOD); self.choose_link()
                self.next_link_check = time.time() + 5
        OPT_KEY = VAR_PREFIX + "options"
        CONNECTIONS = [("auto", "TazUO's map if on, else my login"), ("tazuo", "Only TazUO's Enhanced Map"),
                       ("own", "Only my own login")]
        CONN_CODES = [c[0] for c in CONNECTIONS]
        OPT = {"sounds": True, "share": True, "gesture": True, "connection": "auto", "ping_secs": 8, "drag": 25}
        OPT_LIMITS = {"ping_secs": (2, 60), "drag": (5, 200)}
        def load_options():
            for k, v in Kit.codec_load(Kit.get_var(OPT_KEY)).items():
                if k in ("sounds", "share", "gesture"): OPT[k] = v == "1"
                elif k == "connection" and v in CONN_CODES: OPT[k] = v
                elif k in OPT_LIMITS:
                    try: lo, hi = OPT_LIMITS[k]; OPT[k] = max(lo, min(hi, int(v)))
                    except ValueError: pass
                elif k.startswith("hk_") and k[3:] in HOTKEYS: HOTKEYS[k[3:]] = _norm_key(v)
        def save_options():
            data = "sounds=%d;share=%d;gesture=%d;connection=%s" % (
                OPT["sounds"], OPT["share"], OPT["gesture"], OPT["connection"])
            data += "".join(";hk_%s=%s" % (k, HOTKEYS[k].replace(";", "")) for k in HOTKEY_ORDER)
            data += ";ping_secs=%d;drag=%d" % (int(OPT["ping_secs"]), int(OPT["drag"])); Kit.put_var(OPT_KEY, data)
        def _queue_app(action):
            if APP["app"] is not None: APP["app"].pending.append(action)
        page = {"fields": None}; H_SEND, H_LOGIN, H_OPT, H_KEYS = 116, 160, 124, 70
        PING_TIP = "Send a %s ping where you next target: a spot, an item or a person"
        KEY_TIP = "The key for a %s ping, for example CTRL+1, F9 or SHIFT+F2 (blank = none)"
        LOGIN_TIPS = {"host": "The map server's address (a host name or an IP address)",
                      "port": "The map server's port (a number; %d by default)" % DEFAULT_PORT,
                      "user": "Your login name on the map server",
                      "pass": "Your map server password; kept in plain text in the client's saved "
                              "variables on this PC, like Enhanced Map's own"}
        def _page_action(action):
            def fn(*args): _queue_app(action)
            return fn
        def config_height(w): return H_SEND + Kit.GAP + H_LOGIN + Kit.GAP + H_OPT + Kit.GAP + H_KEYS
        def build_send(g, x, y, w, store):
            Kit.add_section(g, x, y, w, H_SEND, "SEND A PING  (or a hotkey, or the mouse-wheel drag)"); bx = x + 12
            for t in (LOOK, DANGER, GO, HELP):
                label, hue = TYPE_INFO[t][:2]; cap = label + "..."
                Kit.art_button(g, store, "ping%d" % t, Kit.ART_PLAY, bx, y + 28, cap, PING_TIP % label,
                               hue=hue, on_click=_page_action(("target", t)))
                bx += 35 + Kit.text_w(cap) + 16
            Kit.art_button(g, store, "recon", Kit.ART_PLAY, x + 12, y + 58, "Reconnect",
                           "Connect to the map server again (TazUO's Enhanced Map or the separate login)",
                           on_click=_page_action(("reconnect",)))
            hx = x + 12 + 35 + Kit.text_w("Reconnect") + 16
            Kit.art_button(g, store, "history", Kit.ART_PAGE, hx, y + 58, "History",
                           "Open the ping history window: recent pings, yours and other people's "
                           "(click again to close it)", on_click=_page_action(("history",)))
            gx = hx + 35 + Kit.text_w("History") + 16; app = APP["app"]
            if app is not None:
                Kit.add_label(g, Kit.fit("Wheel drag: up Look, right Danger, down Go, left Help", x + w - 12 - gx),
                              gx, y + 61, Kit.HUE_INFO)
            lbl = Kit.add_label(g, "", x + 12, y + 90, Kit.HUE_INFO); page["status"] = lbl
            if app is not None:
                app.status_label, app.status_w = lbl, w - 24
                Kit.set_text(lbl, Kit.fit(app.status_text or "Starting...", w - 24))
        def build_config(g, x, y, w):
            store = ({}, {}); build_send(g, x, y, w, store); y = y + H_SEND + Kit.GAP; st = Settings()
            Kit.add_section(g, x, y, w, H_LOGIN, "SEPARATE MAP LOGIN  (when TazUO's Enhanced Map is off)"); fields = {}
            col = (w - 36) // 2
            for i, (key, caption, value) in enumerate((
                    ("host", "Server address:", st.host), ("port", "Port:", str(st.port)),
                    ("user", "Map username:", st.user), ("pass", "Map password:", st.password))):
                fx = x + 12 + (i % 2) * (col + 12); fy = y + 30 + (i // 2) * 48; Kit.add_label(g, caption, fx, fy)
                fields[key] = Kit.with_tip(Kit.add_textbox(g, value, fx + 2, fy + 20, col - 8, numbers=key == "port"),
                                           LOGIN_TIPS[key])
            Kit.art_button(g, store, "save", Kit.ART_OK, x + 12, y + 128, "Save and connect",
                           "Save the four fields on this PC and connect with them")
            page["login"] = Kit.add_label(g, Kit.fit("Saved on this PC in plain text (the "
                                                      "password shows while typing).", w - 236),
                                           x + 220, y + 131, Kit.HUE_INFO)
            yo = y + H_LOGIN + Kit.GAP; Kit.add_section(g, x, yo, w, H_OPT, "OPTIONS")
            checks = {"sounds": Kit.add_check(g, "Play a sound for each ping", x + 12, yo + 32, OPT["sounds"],
                                        "Play the ping's sound when a ping shows, yours and other people's"),
                "gesture": Kit.add_check(g, "Ping with a mouse-wheel drag", x + 312, yo + 32, OPT["gesture"],
                                         "Hold the mouse wheel over a spot and drag: up Look "
                                         "here, right Danger!, down Go here, left Need help"),
                "share": Kit.add_check(g, "Show me on guildmates' maps", x + 12, yo + 58, OPT["share"],
                                       "Send your position to the map server (separate login "
                                       "only; TazUO's Enhanced Map does this itself)"),}
            nums = {}; ny = yo + 86
            for k, cap, nx, unit, tip in (("ping_secs", "Ping stays:", x + 12, "s",
                     "Seconds a ping's marker and pulse stay on screen (%d-%d)"),
                    ("drag", "Drag distance:", x + 312, "px",
                     "Pixels the mouse-wheel drag must go before a direction counts (%d-%d)")):
                Kit.add_label(g, cap, nx, ny + 3); bx = nx + Kit.text_w(cap) + 8
                nums[k] = Kit.with_tip(Kit.add_textbox(g, str(OPT[k]), bx, ny, 44), tip % OPT_LIMITS[k])
                Kit.add_label(g, unit, bx + 50, ny + 3, Kit.HUE_INFO)
            yk = yo + H_OPT + Kit.GAP; Kit.add_section(g, x, yk, w, H_KEYS, "HOTKEYS  (blank = none)"); keys = {}
            kx = x + 12
            for k in HOTKEY_ORDER:
                cap = k.capitalize() + ":"; Kit.add_label(g, cap, kx, yk + 36)
                keys[k] = Kit.with_tip(Kit.add_textbox(g, HOTKEYS[k], kx + Kit.text_w(cap) + 8, yk + 33, 84,
                                                       numbers=False), KEY_TIP % label_of(TYPE_KEYS[k]))
                kx += Kit.text_w(cap) + 8 + 84 + 16
            Kit.add_label(g, "Connection:", x + 312, yo + 60)
            idx = CONN_CODES.index(OPT["connection"]) if OPT["connection"] in CONN_CODES else 0
            dd = G.CreateDropDown(190, [c[1] for c in CONNECTIONS], idx); dd.SetPos(x + 414, yo + 56); g.Add(dd)
            Kit.with_tip(dd, "Which map connection to use: TazUO's Enhanced Map while it is on, or the separate login "
                             "above")
            page.update({"fields": fields, "checks": checks, "dd": dd, "store": store,
                         "seen": dict(OPT), "keys": keys, "seen_keys": dict(HOTKEYS), "nums": nums, "next_read": 0.0})
        def poll_config(force=False):
            if page["fields"] is None: return
            if Kit.was_clicked(page["store"], "save"): _save_login()
            now = time.time()
            if not force and now < page.get("next_read", 0.0): return
            page["next_read"] = now + 0.2
            for k, cb in page["checks"].items():
                try: OPT[k] = bool(cb.IsChecked)
                except Exception: pass
            try: i = int(page["dd"].GetSelectedIndex())
            except Exception: i = None
            if i is not None and 0 <= i < len(CONNECTIONS): OPT["connection"] = CONNECTIONS[i][0]
            for k, tb in (page.get("nums") or {}).items():
                try: txt = str(tb.Text or "").strip()
                except Exception: continue
                if txt.isdigit(): lo, hi = OPT_LIMITS[k]; OPT[k] = max(lo, min(hi, int(txt)))
            if OPT != page["seen"]: page["seen"] = dict(OPT); save_options(); _queue_app(("options",))
            new = {}
            for k, tb in page["keys"].items():
                try: new[k] = _norm_key(tb.Text)
                except Exception: new[k] = _norm_key(HOTKEYS[k])
            if force and new != page["seen_keys"]:
                page["typed"] = page["seen_keys"] = new; HOTKEYS.update(new); save_options(); _queue_app(("rehook",))
            elif new != page.get("typed"): page["typed"], page["stable"] = new, 0
            elif new != page["seen_keys"]:
                page["stable"] = page.get("stable", 0) + 1
                if force or page["stable"] >= 5:
                    page["seen_keys"] = new; HOTKEYS.update(new); save_options(); _queue_app(("rehook",))
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
            st = Settings(); st.host, st.port, st.user, st.password = host, port, user, password; st.save()
            Kit.set_text(page["login"], "Saved", Kit.HUE_GOOD); app = APP["app"]
            if app is not None:
                s = app.settings; s.host, s.port, s.user, s.password = host, port, user, password
                app.pending.append(("save_setup",))
        def config_closed():
            poll_config(True); app = APP["app"]
            if app is not None and app.status_label is page.get("status"): app.status_label = None
            page.update({"fields": None, "checks": None, "dd": None, "status": None, "keys": None,
                         "nums": None, "login": None})
        APP = {"app": None}
        def _offer_ping(x, y, m=None, kind="danger", who=None):
            app = APP["app"]
            if app is None or app._shut: return False
            if m is None:
                try: m = int(API.GetMap())
                except Exception: return False
            return app.send_auto(int(x), int(y), int(m), TYPE_KEYS.get(kind, DANGER), who)
        def _start(): APP["app"] = PingApp(); APP["app"].start(); HOST.services["pings.send"] = _offer_ping
        def _tick():
            if APP["app"] is not None: APP["app"].step()
        def _thread_tick():
            if APP["app"] is not None: APP["app"].thread_step()
        def _stop():
            HOST.services.pop("pings.send", None); app, APP["app"] = APP["app"], None
            if app is not None: app.shutdown()
        def _interval():
            app = APP["app"]
            if app is None: return 0.05
            if app.gesture is not None: return 0.02
            if app.aim is not None or app.pending or app.inbox or app.jobs or app.outbox: return 0.05
            return 0.1
        load_options()
        MODULE = {"start": _start, "tick": _tick, "stop": _stop, "interval": _interval,
                  "client_tick": True, "thread_tick": _thread_tick,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE
    def _part_corpse():
        KEY = "corpserun"; TITLE = "Corpse"; SETTINGS_KEY = "CorpseRun_settings"; CORPSE_KEY = "CorpseRun_corpse"
        POS_KEY = "CorpseRun_pos"; MIN_KEY = "CorpseRun_min"; ARROW_ID = 0x434F5250; CORPSE_GRAPHIC = 0x2006
        BONES_FIRST, BONES_LAST = 0x0ECA, 0x0ED2; DEFAULT_DECAY_MIN = 15; DEFAULT_BONES_MIN = 45
        MIN_LO, MIN_HI = 1, 120; RED_SECS = 60; DECAYED_GRACE = 120.0; ALERT_DECAY = "corpserun.decay"; FIND_SECS = 20.0
        HUMAN_BODIES = (0x190, 0x191, 0x25D, 0x25E, 0x29A, 0x29B); SEEK_RANGE = 24; ITEM_EVERY = 1.0; REACH = 2
        MOVE_GAP = 0.7; MOVE_RECHECK = 2; PLAN_CAP = 250; J_WAIT = ("must wait to perform another action",)
        HAIR_FIRST, HAIR_LAST = 0x203B, 0x204D; PING_TRY = 15.0; W = 420; MINI_W, MINI_H = 280, 46; BODY_H = 128
        H = Kit.MARGIN + 30 + Kit.GAP + BODY_H + Kit.MARGIN
        settings = {"arrow": True, "restore": True, "ping": False, "decay": DEFAULT_DECAY_MIN,
                    "bones": DEFAULT_BONES_MIN, "say": False}
        st = {"body": 0, "body_at": 0.0, "note_until": 0.0, "name": "", "drawn": None, "drawn_c": None}
        win = {"g": None, "c": {}, "store": ({}, {})}; page = {"c": None, "typed": {}}
        NUMS = {"decay": (MIN_LO, MIN_HI), "bones": (MIN_LO, MIN_HI)}
        def load_settings():
            Kit.kv_load(SETTINGS_KEY, ";", settings, NUMS)
            if (settings["decay"], settings["bones"]) == (7, 7):
                settings["decay"], settings["bones"] = DEFAULT_DECAY_MIN, DEFAULT_BONES_MIN
        def save_settings():
            Kit.kv_save(SETTINGS_KEY, ";", settings, ("arrow", "restore", "ping", "decay", "bones", "say"), NUMS)
        def load_rec():
            p = Kit.get_var(CORPSE_KEY).split("|")
            if len(p) < 8 or p[0] != "1": return None
            try:
                return {"serial": int(p[1]), "x": int(p[2]), "y": int(p[3]), "facet": int(p[4]),
                        "died": float(p[5]), "body": int(p[6]), "spot": p[7] == "1", "exact": len(p) < 9 or p[8] != "0"}
            except ValueError: return None
        def save_rec():
            r = st["rec"]
            if r is None: Kit.put_var(CORPSE_KEY, ""); return
            Kit.put_var(CORPSE_KEY, "1|%d|%d|%d|%d|%.0f|%d|%d|%d" % (
                r["serial"], r["x"], r["y"], r["facet"], r["died"], r["body"], 1 if r["spot"] else 0,
                1 if r["exact"] else 0))
        say = Kit.sayer(TITLE)
        def note(text, secs=6.0):
            st["note"], st["note_until"] = text, time.time() + secs; st["lbl_at"] = 0.0; say(journal_case(text))
        def remaining(now):
            r = st["rec"]
            if r is None: return 0.0
            if r["died"] > now: r["died"] = now
            return 60.0 * (settings["decay"] + settings["bones"]) - (now - r["died"])
        def clock(secs): secs = max(0, int(secs)); return "%d:%02d" % (secs // 60, secs % 60)
        item_of = Kit.find_item; held_item = Kit.held_item
        def cursor_up():
            try:
                if HOST.cursor_busy(KEY): return True
            except Exception: pass
            try: return bool(API.HasTarget())
            except Exception: return False
        def is_hair(it):
            try: g = int(it.Graphic)
            except Exception: return False
            if HAIR_FIRST <= g <= HAIR_LAST: return True
            try: d = it.GetItemData(); return d is not None and int(d.Layer) in (11, 16)
            except Exception: return False
        def weight_of(it):
            try: d = it.GetItemData(); w = int(d.Weight) if d is not None else 0
            except Exception: w = 0
            if w >= 255: w = 0
            try: n = int(it.Amount or 1)
            except Exception: n = 1
            total = w * max(1, n)
            try:
                if it.IsContainer:
                    for x in (API.ItemsInContainer(int(it.Serial), True) or []):
                        try:
                            d = x.GetItemData(); xw = int(d.Weight) if d is not None else 0
                            if xw < 255: total += xw * max(1, int(x.Amount or 1))
                        except Exception: continue
            except Exception: pass
            return total
        queue = Kit.queuer(st); on_disposed = Kit.disposer(KEY, st, win)
        def build_window():
            g, store, c, w, h, x, y, old = open_window(st, win, POS_KEY, (MINI_W, MINI_H), (W, H), (220, 220), TITLE,
                                                       KEY, queue)
            if not st["minimized"]:
                M = Kit.MARGIN; IW = w - 2 * M; yb = M + 30 + Kit.GAP
                Kit.add_section(g, M, yb, IW, BODY_H, "YOUR CORPSE  (where, and how long it lasts)")
                c["where"] = Kit.add_label(g, "", M + 12, yb + 28, Kit.HUE_TEXT)
                c["decay"] = Kit.add_label(g, "", M + 12, yb + 48, Kit.HUE_INFO)
                c["info"] = Kit.add_label(g, "", M + 12, yb + 68, Kit.HUE_INFO); by = yb + 92; xb = M + 10
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
            show_window(g, x, y, w, h, st, win, on_disposed, POS_KEY, c=c, store=store); st["lbl_at"] = 0.0
            Kit.dispose(old)
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
            left = remaining(now)
            try: mx, my = int(me.X), int(me.Y)
            except Exception: mx, my, mm = r["x"], r["y"], r["facet"]
            if not r["spot"]: where, mini = "Looking for your corpse round you...", "looking"
            elif mm != r["facet"]:
                where = "On %s, at %d, %d" % (Kit.facet_name(r["facet"]), r["x"], r["y"])
                mini = Kit.facet_name(r["facet"])
            else:
                wt = Kit.where_text(r["x"] - mx, r["y"] - my)
                where = "%s%s, at %d, %d" % (wt[0].upper(), wt[1:], r["x"], r["y"]); mini = wt
            bones_at = 60.0 * settings["bones"]; most = "" if r["exact"] else "at most "
            if left > bones_at:
                decay = "Bones in %s%s, gone in %s%s" % (most, clock(left - bones_at), most, clock(left))
            elif left > 0: decay = ("Bones %s; gone in %s%s" % ("now" if r["exact"] else "soon", most, clock(left)))
            else: decay = "Should have decayed by now"
            dhue = Kit.HUE_BAD if left <= RED_SECS else Kit.HUE_INFO
            if st["note"] and now < st["note_until"]: info = st["note"]
            elif j is not None:
                if j["phase"] == "open": info = "Opening your corpse..."
                else: info = "Moving %d / %d" % (min(j["i"], len(j["plan"])), len(j["plan"]))
            else:
                died = (("Died %s ago." % Kit.ago(now - r["died"])) if r["exact"] else "Found as a ghost.")
                mb = st["maybe"]
                if not r["serial"] and mb is not None:
                    info = "A corpse at %d, %d may be yours: click Get my things." % (mb[1], mb[2])
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
                try: d = max(abs(int(me.X) - r["x"]), abs(int(me.Y) - r["y"]))
                except Exception: d = REACH + 1
                if d > REACH: want = (r["x"], r["y"])
            if want == st["arrow"]: return
            if want is None: clear_arrow()
            else:
                try: API.TrackingArrow(want[0], want[1], ARROW_ID); st["arrow"] = want
                except Exception: st["arrow"] = None
        def clear_arrow():
            if st["arrow"] is not None: st["arrow"] = None; safe(lambda: API.TrackingArrow(-1, -1, ARROW_ID))
        def on_death(me, now, at_start=False):
            if st["job"] is not None: stop_job("you died")
            try: x, y, m = int(me.X), int(me.Y), int(API.GetMap())
            except Exception: return
            st["name"] = str(safe(lambda: me.Name, "") or "")
            st["rec"] = {"serial": 0, "x": x, "y": y, "facet": m, "died": now, "body": st["body"],
                         "spot": not at_start, "exact": not at_start}
            st["seek_until"], st["seek_at"] = now + FIND_SECS, now
            st["gone_since"], st["warned"], st["maybe"] = None, False, None; st["refused"] = set(); save_rec()
            if at_start: say("you are a ghost: looking for your corpse round you.")
            else:
                say("you died at %d, %d (%s). Your corpse turns to bones in %d minute%s and is "
                    "gone %d minute%s later." % (x, y, Kit.facet_name(m), settings["decay"],
                                                 "" if settings["decay"] == 1 else "s", settings["bones"],
                                                 "" if settings["bones"] == 1 else "s"), Kit.HUE_BAD)
                if settings["ping"]: st["ping"] = (x, y, m, now + PING_TRY)
            if settings["restore"]: show_full()
        CORPSE_PREFIXES = ("a corpse of ", "corpse of ", "the remains of ", "remains of "); NAME_LOW = ["", ""]
        def mine(it, strict=False, graphic=CORPSE_GRAPHIC):
            r = st["rec"]; body = r["body"] if r is not None else 0
            try: amt = int(it.Amount or 0)
            except Exception: amt = 0
            if body and amt and amt != body: return 0
            bones = BONES_FIRST <= graphic <= BONES_LAST
            if bones and (not amt or (not body and amt not in HUMAN_BODIES)): return 0
            loose = 1 if (not strict or (body and amt == body) or amt in HUMAN_BODIES) else 0; nm = st["name"]
            if nm != NAME_LOW[0]: NAME_LOW[0], NAME_LOW[1] = nm, nm.strip().lower()
            me_name = NAME_LOW[1]
            if not me_name: return loose
            try: n = str(it.Name or "")
            except Exception: n = ""
            if not n:
                try: n = str(it.NameAndProps(False) or "")
                except Exception: n = ""
            n = n.strip().lower(); owner = None
            for p in CORPSE_PREFIXES:
                if n.startswith(p): owner = n[len(p):].strip(); break
            if owner is None:
                if not n or n in ("corpse", "a corpse") or bones: return loose
                owner = n
            return 2 if owner == me_name else 0
        def scan_corpses(items, gr, strict, cx, cy, lim, acc):
            need = 2 if strict else 1
            for it in items:
                try: s, ix, iy = int(it.Serial), int(it.X), int(it.Y)
                except Exception: continue
                d = max(abs(ix - cx), abs(iy - cy))
                if d > lim: continue
                m = mine(it, strict, gr)
                if not m: continue
                e = (d, s, ix, iy); i = 0 if m >= need else 1; b = acc[i]
                if b is None or d < b[0] or (d == b[0] and s > b[1]): acc[i] = e
        def find_corpse(me):
            r = st["rec"]; strict = not r["spot"]
            if r["spot"]: cx, cy, lim = r["x"], r["y"], 3
            else:
                try: cx, cy, lim = int(me.X), int(me.Y), SEEK_RANGE
                except Exception: return None, None
            try: items = API.GetItemsOnGround(SEEK_RANGE, CORPSE_GRAPHIC) or ()
            except Exception: items = ()
            acc = [None, None]; scan_corpses(items, CORPSE_GRAPHIC, strict, cx, cy, lim, acc); best, maybe = acc
            if best is None:
                acc = [None, None]
                for gr in range(BONES_FIRST, BONES_LAST + 1):
                    try: items = API.GetItemsOnGround(SEEK_RANGE, gr)
                    except Exception: continue
                    if items: scan_corpses(items, gr, strict, cx, cy, lim, acc)
                best, m2 = acc
                if m2 is not None and (maybe is None or m2[0] < maybe[0]): maybe = m2
            return (None if best is None else best[1:]), (None if maybe is None else maybe[1:])
        def forget(why=None):
            if st["job"] is not None: stop_job(None)
            st["rec"] = st["maybe"] = st["ping"] = st["gone_since"] = None; st["refused"] = set(); clear_arrow()
            save_rec()
            if why: say(why)
            st["lbl_at"] = 0.0
        def take_maybe():
            r, mb = st["rec"], st["maybe"]
            if item_of(mb[0]) is None: note("That corpse isn't in view any more."); return
            st["maybe"] = None; r["serial"], r["x"], r["y"], r["spot"] = mb[0], mb[1], mb[2], True; save_rec()
            note("The corpse at %d, %d is taken as yours." % (mb[1], mb[2]))
        def corpse_tick(me, now, mm):
            r = st["rec"]; left = remaining(now)
            try: dist = max(abs(int(me.X) - r["x"]), abs(int(me.Y) - r["y"]))
            except Exception: dist = 1 << 20
            if not r["serial"]:
                near = r["spot"] and mm == r["facet"] and dist <= 12
                offered = not r["spot"] and st["maybe"] is not None; seeking = now < st["seek_until"]
                if (seeking and now >= st["seek_at"]) or (not seeking and (near or offered) and now >= st["look_at"]):
                    st["seek_at"] = now + 0.5; st["look_at"] = now + 1.0; hit, maybe = find_corpse(me)
                    if hit is not None:
                        r["serial"], r["x"], r["y"] = hit; st["maybe"] = None
                        if not r["spot"]: r["spot"] = True; say("found your corpse at %d, %d." % (r["x"], r["y"]))
                        save_rec(); st["lbl_at"] = 0.0
                    elif not r["spot"] and maybe != st["maybe"]: st["maybe"] = maybe; st["lbl_at"] = 0.0
                if (not r["serial"] and not r["spot"] and now >= st["seek_until"] and st["maybe"] is None):
                    forget("your corpse isn't in view (it was left before %s started)." % TITLE); return
            elif now >= st["item_at"] or st["item_at"] - now > ITEM_EVERY:
                st["item_at"] = now + ITEM_EVERY; it = item_of(r["serial"])
                if it is not None:
                    st["gone_since"] = None
                    try:
                        ix, iy = int(it.X), int(it.Y)
                        if ((ix or iy) and (ix, iy) != (r["x"], r["y"]) and not int(it.Container or 0)):
                            r["x"], r["y"] = ix, iy; save_rec()
                    except Exception: pass
                elif mm == r["facet"] and st["job"] is None and dist <= 12:
                    if st["gone_since"] is None: st["gone_since"] = now
                    elif now - st["gone_since"] >= 6.0:
                        forget("your corpse isn't at %d, %d any more (decayed or looted)." % (r["x"], r["y"])); return
                else: st["gone_since"] = None
            if left <= 60 and not st["warned"] and left > 0:
                st["warned"] = True
                try:
                    dist = Kit.where_text(r["x"] - int(me.X), r["y"] - int(me.Y)) \
                        if mm == r["facet"] else "on " + Kit.facet_name(r["facet"])
                except Exception: dist = "at %d, %d" % (r["x"], r["y"])
                HOST.alert(ALERT_DECAY, "Your corpse decays in under a minute (%s)" % dist, "warn")
            if left <= -DECAYED_GRACE and item_of(r["serial"]) is None: forget("your corpse has decayed.")
        def ping_tick(now):
            p = st["ping"]
            if p is None: return
            x, y, m, until = p; fn = HOST.services.get("pings.send")
            if fn is None or now > until:
                st["ping"] = None
                if fn is None: say("World Map > Map Pings is off, so no Need help ping was sent.")
                return
            try:
                if fn(x, y, m=m, kind="help"): st["ping"] = None; say("Need help ping sent on your corpse.")
            except Exception: st["ping"] = None
        def start_job(me, now):
            r = st["rec"]
            if st["job"] is not None: return
            if r is None: note("No corpse remembered."); return
            if bool(st["was_dead"]): note("You are still a ghost: get resurrected first."); return
            if not r["serial"]: note("Your corpse hasn't been seen yet: go to %d, %d." % (r["x"], r["y"])); return
            it = item_of(r["serial"])
            if it is None: note("Your corpse isn't in view yet (%d, %d)." % (r["x"], r["y"])); return
            try: d = max(abs(int(it.X) - int(me.X)), abs(int(it.Y) - int(me.Y)))
            except Exception: d = REACH + 1
            if d > REACH:
                note("Walk up to your corpse first (%s)."
                     % Kit.where_text(int(it.X) - int(me.X), int(it.Y) - int(me.Y)))
                return
            pack = safe(lambda: int(API.Backpack), 0) or 0
            if not pack: note("No backpack to put things in."); return
            if cursor_up(): note("A target cursor is up: finish or cancel it first."); return
            if held_item(): note("You are holding an item: put it down first."); return
            st["job"] = {"phase": "open", "corpse": r["serial"], "pack": pack, "at": now + 1.0,
                         "until": now + 3.0, "plan": [], "i": 0, "tried": set(), "waits": {},
                         "move": None, "check": None, "sent_at": 0.0, "last": 0, "rechecks": 0,
                         "hold": 0.0, "moved": 0, "refused": 0, "streak": 0, "why": None,
                         "replans": 0, "jr": Journal.reader() if settings["say"] else None}
            API.UseObject(r["serial"]); st["note"] = ""; st["lbl_at"] = 0.0
        def make_plan(j):
            try: items = API.ItemsInContainer(j["corpse"], False) or []
            except Exception: items = []
            plan = []
            for it in items:
                if len(plan) >= PLAN_CAP: break
                try: s = int(it.Serial)
                except Exception: continue
                if s in j["tried"] or s in st["refused"] or is_hair(it): continue
                plan.append(s)
            return plan
        def job_tick(me, now):
            j = st["job"]
            if j["jr"] is not None:
                for ln in j["jr"].new():
                    if ln.text and not ln.text.startswith(TITLE + ":"): say("reply: " + ln.text.strip())
            if j["why"]: stop_job(j["why"]); return
            if j["move"] is not None: return
            if st["was_dead"]: stop_job("you died"); return
            it = item_of(j["corpse"])
            if it is None: stop_job("your corpse is gone from view"); return
            try: d = max(abs(int(it.X) - int(me.X)), abs(int(it.Y) - int(me.Y)))
            except Exception: d = 0
            if d > REACH: stop_job("you walked away from your corpse"); return
            if j["check"] is not None and (now < j["at"] or not check_move(j, now)): return
            if j["phase"] == "open":
                if now < j["at"]: return
                plan = make_plan(j)
                if not plan and now < j["until"]: return
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
                try:
                    if x is None or int(x.Container or 0) != j["corpse"]: continue
                except Exception: continue
                try: wmax = int(me.WeightMax or 0); wnow = int(me.Weight or 0)
                except Exception: wmax = wnow = 0
                if wmax > 0 and (wnow >= wmax or wnow + weight_of(x) > wmax):
                    stop_job("the next item would put you over your weight limit (%d / %d stones)" % (wnow, wmax))
                    return
                j["tried"].add(s); j["move"] = s; return
            if j["replans"] < 2:
                j["replans"] += 1; more = make_plan(j)
                if more: j["plan"], j["i"] = more, 0; return
            finish_job()
        def check_move(j, now):
            s = j["check"]; it = item_of(s)
            try: where = int(it.Container or 0) if it is not None else None
            except Exception: where = None
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
            mv = j["move"]
            def run():
                if st["job"] is not j or j["move"] != mv or st["shutting"]: return "gone"
                if cursor_up(): return "a target cursor is up"
                h = held_item()
                if h and h != j["last"]: return "you picked something up"
                API.MoveItem(mv, j["pack"]); return "sent"
            try: res = Kit.on_client(run)
            except Exception as ex: res = "a move failed (%s)" % ex
            if st["job"] is not j: return
            j["move"] = None
            if res == "sent":
                j["check"] = mv; j["last"] = mv; j["sent_at"] = time.time(); j["at"] = j["sent_at"] + MOVE_GAP
            elif res != "gone": j["why"] = res
        def finish_job():
            j, st["job"] = st["job"], None
            if j is None: return
            left = []
            if item_of(j["corpse"]) is not None: left = make_plan({"corpse": j["corpse"], "tried": set()})
            n_ref = len(st["refused"])
            if j["moved"] == 0 and not j["refused"] and not left:
                forget("nothing left in your corpse%s." % ((" but %d item%s the server refused (take %s by hand)"
                     % (n_ref, "" if n_ref == 1 else "s", "it" if n_ref == 1 else "them")) if n_ref else ""))
                return
            msg = "%d item%s back in your backpack" % (j["moved"], "" if j["moved"] == 1 else "s")
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
        MOVE_HINT = ("Moves one item every %.1f s and stops when you click Stop, raise a target "
                     "cursor, pick something up, walk away or would go over your weight limit." % MOVE_GAP)
        def page_table(w):
            t1 = "Corpse to bones:"
            return (("WHEN YOU DIE  (the arrow, this window, a ping)", (
                        ("check", "arrow", "Point the tracking arrow at your corpse", "Shows a tracking arrow of its "
                         "own to the corpse (other arrows are left alone); it hides when you stand beside it"),
                        ("check", "restore", "Open the Corpse window when you die, even minimized or folded",
                         "The window comes back full size when you die"),
                        ("check", "ping", "Send a Need help map ping on your corpse when you die",
                         "Your guild sees a Need help ping where you died (needs World Map > Map Pings on). Off at "
                         "first: it tells them where you are")), {"pad": 4}), ("DECAY  (minutes; the shard's times)", (
                        ("num", "decay", t1, "Minutes from your death until the corpse turns to bones", None, MIN_LO,
                         MIN_HI, {"stay": True}),
                        ("num", "bones", "Bones gone after:", "Minutes the bones (your things still in them) last "
                         "before they decay", None, MIN_LO, MIN_HI, {"dx": Kit.text_w(t1) + 86})),
                     {"ldy": 4, "fw": 40, "pad": 8}),
                    ("GET MY THINGS  (one item at a time)", [("note", ln) for ln in Kit.wrap(MOVE_HINT, w - 28)]),
                    atlas_page("corpse"),
                    ("DEBUG  (for checking the shard's texts)", (("check", "say", "Print the shard's replies in the "
                     "journal", "While Get my things runs, every journal line is repeated as \"%s: reply: ...\", for "
                     "checking the shard's texts" % TITLE),)))
        def config_height(w): return Kit.Form.height(page_table(w), w)
        def build_config(g, x, y, w): page["c"] = Kit.Form(g, x, y, w, settings, page_table(w)).c
        def poll_config(force=False):
            c = page["c"]
            if c is None: return
            changed = False; now = time.time()
            try:
                for k in ("arrow", "restore", "ping", "say"):
                    v = bool(c[k].IsChecked)
                    if v != settings[k]: settings[k], changed = v, True
                for k in ("decay", "bones"):
                    txt = str(c[k].Text or "").strip(); t = page["typed"].get(k)
                    if t is None or t[0] != txt:
                        page["typed"][k] = (txt, now)
                        if not force: continue
                    elif not force and now - t[1] < 1.0: continue
                    if txt.isdigit():
                        v = max(MIN_LO, min(MIN_HI, int(txt)))
                        if v != settings[k]: settings[k], changed = v, True; st["warned"] = False
            except Exception: page["c"] = None; return
            if changed:
                save_settings(); st["lbl_at"] = 0.0
                if not settings["arrow"]: clear_arrow()
        def config_closed(): poll_config(True); page["c"] = None; page["typed"] = {}
        def rebase(d):
            for k in ("body_at", "seek_until", "seek_at", "look_at", "item_at", "lbl_at", "note_until"):
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
                       "last_now": None, "atlas": False, "maybe": None, "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            load_settings(); st["rec"] = load_rec(); st["warned"] = False
            if st["rec"] is not None and remaining(time.time()) <= -DECAYED_GRACE: st["rec"] = None; save_rec()
            if st["rec"] is not None and not st["rec"]["spot"]: st["seek_until"] = time.time() + FIND_SECS
            safe(lambda: HOST.alert_kind(ALERT_DECAY, "Corpse about to decay", 0x1EA)); build_window()
            HOST.dock_add(KEY, Kit.dock_hooks(TITLE, 0x0ECA, st, win, queue("redraw"), scale=True))
        def _tick():
            if win["g"] is None: return
            if Kit.was_clicked(win["store"], "close"): Kit.dispose(win["g"]); return
            now = time.time(); last, st["last_now"] = st["last_now"], now
            if last is not None and now < last - 2.0: rebase(now - last)
            me = HOST.me()
            while st["queue"]:
                action = st["queue"].pop(0)
                if action == "go":
                    if st["job"] is not None: stop_job(None, user=True)
                    elif (st["rec"] is not None and not st["rec"]["serial"] and st["maybe"] is not None): take_maybe()
                    elif me is not None: start_job(me, now)
                elif action == "help":
                    r = st["rec"]
                    if r is None or not r["spot"]: note("No corpse to ping.")
                    elif HOST.services.get("pings.send") is None:
                        note("World Map > Map Pings is off: turn it on to send pings.")
                    else: st["ping"] = (r["x"], r["y"], r["facet"], now + PING_TRY)
                elif action == "forget":
                    if st["rec"] is None: note("No corpse remembered.")
                    else: forget("forgot your corpse.")
                else: Kit.win_action(action, st, KEY, TITLE, build_window, MIN_KEY)
            if me is None: return
            try: dead = bool(me.IsDead)
            except Exception: return
            was = st["was_dead"]; st["was_dead"] = dead
            if was is None:
                if dead and st["rec"] is None: on_death(me, now, at_start=True)
            elif dead and not was: on_death(me, now)
            elif was and not dead and st["rec"] is not None:
                r = st["rec"]
                if r["spot"]:
                    try: wt = Kit.where_text(r["x"] - int(me.X), r["y"] - int(me.Y))
                    except Exception: wt = "at %d, %d" % (r["x"], r["y"])
                    say("you are alive. Your corpse is %s: click Get my things beside it." % wt, Kit.HUE_GOOD)
                st["lbl_at"] = 0.0
            if not dead and now >= st["body_at"]:
                st["body_at"] = now + 2.0
                try: st["body"] = int(me.Graphic); st["name"] = str(me.Name or "") or st["name"]
                except Exception: pass
            mm = None
            if st["rec"] is not None or st["arrow"] is not None:
                try: mm = int(API.GetMap())
                except Exception: mm = -1
            if st["rec"] is not None: corpse_tick(me, now, mm)
            if st["job"] is not None: job_tick(me, now)
            if st["ping"] is not None: ping_tick(now)
            if st["rec"] is not None or st["arrow"] is not None: arrow_tick(me, mm)
            r = st["rec"]; sig = (r["x"], r["y"], r["facet"]) if r is not None and r["spot"] else None
            if sig != st["atlas"]:
                st["atlas"] = sig
                ATLAS.set("corpse", {} if sig is None else
                          {atlas_name("Your corpse"): (sig[0], sig[1], sig[2], "white")})
            refresh(me, now, mm)
        def _thread_tick():
            j = st["job"]
            if j is not None and j["move"] is not None and not st["shutting"]: send_move()
        def _interval(): return 0.1 if st["job"] is not None else 0.25
        def _thread_wanted(): j = st["job"]; return j is not None and j["move"] is not None
        def _stop():
            st["shutting"] = True; st["job"] = st["ping"] = None; HOST.dock_remove(KEY); clear_arrow()
            Kit.save_pos(POS_KEY, win["g"]); Kit.save_min(MIN_KEY, st["minimized"]); save_settings()
            g, win["g"] = win["g"], None; win["c"] = {}; Kit.dispose(g)
        MODULE = {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "thread_tick": _thread_tick,
                  "thread_wanted": _thread_wanted, "interval": _interval,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE
    def _part_maps():
        KEY = "treasure"; TITLE = "Treasure Maps"; SETTINGS_KEY = "TreasureHunter_settings"
        MAPS_KEY = "TreasureHunter_maps"; POS_KEY = "TreasureHunter_pos"; MIN_KEY = "TreasureHunter_min"
        MINI_W, MINI_H = 320, 46; ROWS = 8; ROW_H = 24; ARROW_ID = 0x54524541; MAP_GRAPHICS = (0x14EB, 0x14EC)
        LEVELS = ("youthful", "plainly", "expertly", "adeptly", "cleverly", "deviously", "ingeniously")
        LEVEL_NAMES = ["Youthful"] + [v.capitalize() + " drawn" for v in LEVELS[1:]]
        PROP_FACETS = ["somewhere in " + n.lower() for n in Kit.FACETS]
        J_DECODED = "you successfully decode a treasure map"; J_SHOWN = "the treasure is marked by the red pin"
        J_DONE = "this treasure hunt has already been completed"
        J_ESTIMATE = re.compile(r"believe this is somewhere near (\d+) and (\d+)"); TAZ_SCALE = 300.0; SCAN_EVERY = 1.0
        LOOK_FOR = 6.0; LOOK_EVERY = 0.25; USED_KEEP = 8.0; SAVE_EVERY = 5.0; MAX_MAPS = 60; PING_TRY_FOR = 6.0
        PING_RETRY = 0.5
        LOOK_TIP = ("Point the tracking arrow at this map's spot (click again: back to the nearest map)")
        LOOK_TIP_ON = "Send the tracking arrow back to the nearest map's spot"
        LOOK_TIP_MAN = ("Point the tracking arrow at this map's spot (click again: take the tracking arrow down)")
        PING_TIP = "Send a Go here map ping on this map's spot (needs World Map > Map Pings on)"
        EMPTY_TEXT = "No treasure maps in your pack. Put one in it and double-click it once."
        settings = {"auto": True, "undecoded": True, "done": False, "say": False}
        st = {"next_look": 0.0, "dirty": False, "next_save": 0.0, "list_ver": 0, "me": (0, 0, -1), "hooked": False,
              "tm_at": 0.0, "tm_serial": 0, "hidden": 0, "in_pack": frozenset()}
        spots = {}; parsed = {}; TEXT_EVERY = 5.0; TEXT_ALL = [False]; asked = set(); read_gumps = {}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}; page = {"c": None}; JR = {"rd": None}
        bank_st = {"at": 0.0, "items": []}
        def say(text, hue=None):
            safe(lambda: API.SysMsg("%s: %s" % (TITLE, text), Kit.HUE_INFO if hue is None else hue))
        def level_name(lvl): return LEVEL_NAMES[lvl] if 0 <= lvl < len(LEVEL_NAMES) else "Treasure map"
        def save_settings(): Kit.kv_save(SETTINGS_KEY, ";", settings, ("auto", "undecoded", "done", "say"))
        def load_maps():
            spots.clear(); cut = time.time() - 60 * 86400
            for part in Kit.get_var(MAPS_KEY).split(";"):
                b = part.strip().split(",")
                if len(b) < 7: continue
                try:
                    s = int(b[0], 16)
                    rec = {"x": int(b[1]), "y": int(b[2]), "f": int(b[3]), "lvl": int(b[4]),
                           "done": b[5] == "1", "t": int(b[6]), "approx": len(b) > 7 and b[7] == "1"}
                except ValueError: continue
                if s <= 0 or rec["x"] <= 0 or rec["y"] <= 0 or rec["t"] < cut: continue
                spots[s] = rec
            cap_spots()
        def cap_spots():
            if len(spots) > MAX_MAPS:
                old = sorted(spots, key=lambda s: spots[s]["t"])
                for s in old[:len(spots) - MAX_MAPS]: del spots[s]
        def save_maps():
            st["dirty"] = False
            Kit.put_var(MAPS_KEY, ";".join("%X,%d,%d,%d,%d,%d,%d,%d" % (s, r["x"], r["y"], r["f"], r["lvl"],
                        1 if r["done"] else 0, r["t"], 1 if r.get("approx") else 0) for s, r in sorted(spots.items())))
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
            try: text = str(API.ItemNameAndProps(serial, False) or "")
            except Exception: text = ""
            again = now + TEXT_EVERY
            if not text.strip():
                again = 0.0
                try: text = str(it.Name or "")
                except Exception: text = ""
                if serial not in asked:
                    asked.add(serial)
                    if len(asked) > 500: asked.clear()
                    safe(lambda: API.RequestOPLData([serial]))
            if hit is not None and hit[0] == text: parsed[serial] = (text, hit[1], again); return hit[1]
            info = parse(text)
            if len(parsed) > 300: parsed.clear()
            parsed[serial] = (text, info, again); return info
        def solve(est, end, p, size):
            try: est = int(est)
            except Exception: return None, None
            try: end, p, size = int(end), float(p), float(size)
            except Exception: return est, None
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
            if spot is None and scale:
                try: return int(int(end) - (float(size) - float(p) - 0.5) * scale), False
                except Exception: pass
            if spot is None:
                try: return int(est), True
                except Exception: return None, True
            return spot, False
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
                    try:
                        if str(g.GetType().Name) != "MapGump": continue
                    except Exception: continue
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
            if settings["say"]:
                say("map window %X: pin %s,%s on %sx%s, far edge %s,%s, TazUO's estimate %d,%d, "
                    "facet field %s -> %s,%s" % (serial, px, py, size_w, size_h, end_x, end_y, est_x, est_y, mf, x, y))
            if x is None or y is None or x <= 0 or y <= 0: return 0
            record(serial, x, y, mf if mf is not None and mf > 0 else -1, ax or ay); return 1
        def record(serial, x, y, mf, approx=False):
            info = {}
            try:
                it = API.FindItem(serial)
                if it is not None: info = info_of(serial, it)
            except Exception: info = {}
            now = time.time()
            hinted = 0 <= now - st["tm_at"] <= LOOK_FOR and (st["tm_serial"] == serial
                or (not st["tm_serial"] and now - st["tm_at"] <= 1.5))
            if not (info.get("tm") or serial in spots or hinted):
                if settings["say"]: say("map %X has a pin but isn't a treasure map: left out." % serial)
                return False
            f = mf if mf >= 0 else info.get("f", -1)
            if f < 0:
                try: f = int(API.GetMap())
                except Exception: f = st["me"][2] if st["me"][2] >= 0 else 0
            old = spots.get(serial); lvl = info.get("lvl", -1)
            if lvl < 0 and old is not None: lvl = old["lvl"]
            rec = {"x": int(x), "y": int(y), "f": int(f), "lvl": lvl,
                   "done": bool(info.get("done") or (old is not None and old["done"])),
                   "t": int(time.time()), "approx": bool(approx)}
            same = (old is not None and (old["x"], old["y"], old["f"]) == (rec["x"], rec["y"], rec["f"]))
            spots[serial] = rec; cap_spots(); st["dirty"] = True; st["next_scan"] = 0.0
            if not same:
                st["arrow_off"] = False; mx, my, mf2 = st["me"]; where = ""
                if mf2 == rec["f"] and mx > 0:
                    d = max(abs(rec["x"] - mx), abs(rec["y"] - my))
                    where = ", %d tile%s %s" % (d, "" if d == 1 else "s",
                                                Kit.compass(rec["x"] - mx, rec["y"] - my) or "here")
                say("%s map%s: dig at %s%d, %d in %s%s." % (
                    level_name(lvl).lower(), (" (level %d)" % lvl) if lvl >= 0 else "",
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
        def hook_events():
            if st["hooked"]: return
            st["hooked"] = True; safe(lambda: API.Events.ObjectUsed(on_used))
        def handle_used(now):
            used, st["used"] = st["used"], []
            for s in used:
                try: it = API.FindItem(s); g = int(it.Graphic) if it is not None else 0
                except Exception: g = 0
                if g in MAP_GRAPHICS: st["last_map"] = (s, now); arm_look(now)
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
                    if m:
                        st["est"] = (int(m.group(1)), int(m.group(2)), now); arm_look(now)
                        if settings["say"]: say("TazUO's estimate line: %s, %s" % (m.group(1), m.group(2)))
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
            try: bps = int(API.Backpack or 0)
            except Exception: bps = 0
            if not bps: st["in_pack"] = None; return
            found = []
            try: deep = HOST.pack_items(True, 0.5)
            except Exception: deep = []
            for it in deep or ():
                try:
                    if int(it.Graphic) in MAP_GRAPHICS: found.append(it)
                except Exception: continue
            bank = bank_maps(now); banked = set()
            for it in bank:
                try: banked.add(int(it.Serial))
                except Exception: continue
            found.extend(bank); out, seen = [], set(); hidden = 0; day = int(time.time())
            tnow = None if TEXT_ALL[0] else time.time(); TEXT_ALL[0] = False
            for it in found:
                try: s = int(it.Serial)
                except Exception: continue
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
            bank_st["at"] = now; bank_st["items"] = []
            try:
                b = int(API.Bank or 0)
                if not b or not bank_open(b): return []
                items = API.ItemsInContainer(b, True) or []
                for it in list(items)[:2000]:
                    if int(it.Graphic) in MAP_GRAPHICS: bank_st["items"].append(it)
            except Exception: pass
            return bank_st["items"]
        def bank_open(bank):
            try:
                for g in Tz.windows(("ContainerGump", "GridContainer")):
                    if int(g.LocalSerial) == bank: return True
            except Exception: pass
            return False
        def dig_tiles(keep):
            want = set((int(e["x"]), int(e["y"]), int(e["f"])) for e in keep)
            for t in st["dig_tiles"] - want: safe(lambda: API.RemoveMarkedTile(t[0], t[1], t[2]))
            for t in want - st["dig_tiles"]: safe(lambda: API.MarkTile(t[0], t[1], 0x0035, t[2]))
            st["dig_tiles"] = want
        def sort_key(e): return (e["group"], e["dist"] if e["dist"] is not None else 0, e["lvl"], e["serial"])
        def atlas_publish():
            keep = [e for e in st["list"] if not (e["x"] is None or e["done"] or e["f"] < 0)]
            sig = tuple((e["serial"], e["x"], e["y"], e["f"], e["lvl"]) for e in keep)
            if sig == st["atlas_sig"]: return
            st["atlas_sig"] = sig; dig_tiles(keep); items = {}
            for e in keep:
                name = atlas_name(("Dig L%d #%04X" % (e["lvl"], e["serial"] & 0xFFFF)) if e["lvl"] >= 0
                                  else ("Dig #%04X" % (e["serial"] & 0xFFFF)))
                items[name] = (int(e["x"]), int(e["y"]), int(e["f"]), "yellow")
            ATLAS.set("maps", items)
        def where_of(e, fac):
            if e["x"] is not None:
                spot = ("about (%d, %d)" if e.get("approx") else "(%d, %d)") % (e["x"], e["y"])
                if e["done"]: return "dug up  " + spot, Kit.HUE_INFO, "This treasure has been dug up"
                if e["f"] == fac:
                    d = e["dist"]
                    if d == 0: return "here  " + spot, Kit.HUE_GOOD, LOOK_TIP
                    return ("%d tile%s %s  %s" % (d, "" if d == 1 else "s", e["dir"], spot), Kit.HUE_TEXT, LOOK_TIP)
                return ("in %s  %s" % (Kit.facet_name(e["f"]), spot), Kit.HUE_INFO,
                        "This map's spot is in %s; you are in %s" % (Kit.facet_name(e["f"]), Kit.facet_name(fac)))
            if e["done"]: return "dug up", Kit.HUE_INFO, "This treasure has been dug up"
            if e["dec"]:
                return ("open the map once to read its spot", Kit.HUE_INFO,
                        "Double-click the map once: its dig spot is read from it")
            if e["dec"] is None:
                return ("open the map to read it", Kit.HUE_INFO,
                        "Double-click the map: a decoded map's spot is read from it")
            return ("not decoded yet", Kit.HUE_INFO, "Not decoded yet: double-click the map to decode it (Cartography)")
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
            try:
                if want is None: API.TrackingArrow(-1, -1, ARROW_ID)
                else: API.TrackingArrow(want[0], want[1], ARROW_ID); st["arrow_at"] = time.time()
            except Exception: pass
            st["arrow"] = want
        def arrow_closed(now):
            if st["arrow"] is None: return
            age = now - st.get("arrow_at", 0.0)
            if age < 0: st["arrow_at"] = now; return
            if age < 1.5 or arrow_open(): return
            st["arrow"], st["arrow_off"], st["pin"] = None, True, 0
        queue = Kit.queuer(st); on_disposed = Kit.disposer(KEY, st, win)
        def build_window():
            g, store, c, w, h, x, y, old = open_window(st, win, POS_KEY, (MINI_W, MINI_H), (560, list_h(ROWS, ROW_H)),
                                                       (240, 180), TITLE, KEY, queue)
            rows = []
            if not st["minimized"]:
                M = Kit.MARGIN; IW = w - 2 * M; yt = M + 30 + Kit.GAP; Kit.add_section(g, M, yt, IW, 36)
                right = M + IW - 8
                Kit.art_button(g, store, "pg_dn", Kit.ART_MIN, right - 22, yt + 8, None,
                               "Next page", on_click=queue(("page", 1)))
                Kit.art_button(g, store, "pg_up", Kit.ART_RESTORE, right - 46, yt + 8, None,
                               "Previous page", on_click=queue(("page", -1)))
                xpg = right - 52 - Kit.text_w("9/9"); c["pg"] = Kit.add_label(g, "", xpg, yt + 10, Kit.HUE_INFO)
                x_off = xpg - 12 - (35 + Kit.text_w("Arrow off"))
                Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, x_off, yt + 7, "Arrow off",
                               "Take the tracking arrow down (a row click or Nearest brings it back)",
                               on_click=queue("arrow_off"))
                x_near = x_off - 12 - (35 + Kit.text_w("Nearest"))
                Kit.art_button(g, store, "nearest", Kit.ART_PLAY, x_near, yt + 7, "Nearest",
                               "Point the tracking arrow at the nearest dig spot on your facet",
                               on_click=queue("nearest"))
                c["status"] = Kit.add_label(g, "", M + 12, yt + 10, Kit.HUE_INFO); c["status_w"] = x_near - 8 - (M + 12)
                yl = yt + 36 + Kit.GAP; Kit.add_section(g, M, yl, IW, 30 + ROWS * ROW_H + 8); x_lvl = M + 12
                x_name = x_lvl + max(34, Kit.text_w("Level")) + 8; x_where = x_name + 150 + 8; x_ping = M + IW - 12 - 22
                Kit.add_label(g, "Level", x_lvl, yl + 6, Kit.HUE_TITLE)
                Kit.add_label(g, "Map", x_name, yl + 6, Kit.HUE_TITLE)
                Kit.add_label(g, "Dig spot", x_where, yl + 6, Kit.HUE_TITLE); c["where_w"] = x_ping - 8 - x_where
                c["empty_w"] = x_ping - 8 - x_lvl
                for k in range(ROWS):
                    ry = yl + 30 + k * ROW_H
                    r = {"serial": 0, "prev": (0, 0.0), "sig": None, "tip": None, "pvis": True}
                    r["lvl"] = Kit.add_label(g, "", x_lvl, ry + 3, Kit.HUE_TITLE)
                    r["name"] = Kit.add_label(g, "", x_name, ry + 3, Kit.HUE_TEXT)
                    r["where"] = Kit.add_label(g, "", x_where, ry + 3, Kit.HUE_INFO)
                    r["catch"] = Kit.catcher(g, M + 6, ry, x_ping - 4 - (M + 6), ROW_H,
                                             row_clicker(lambda: win["rows"], k, "serial", "row", queue, 0), LOOK_TIP)
                    r["ping"] = Kit.art_button(g, store, "ping%d" % k, Kit.ART_PLAY, x_ping, ry + 1, None, PING_TIP,
                                               on_click=row_clicker(lambda: win["rows"], k, "serial", "ping", queue, 0))
                    rows.append(r)
            show_window(g, x, y, w, h, st, win, on_disposed, POS_KEY, c=c, store=store, rows=rows); st["drawn"] = None
            refresh(); Kit.dispose(old)
        def show(ctl, r, key, on):
            if r[key] != on:
                r[key] = on
                try: ctl.IsVisible = on
                except Exception: pass
        def refresh():
            g = win["g"]
            if g is None or (st["minimized"] and st["docked"]): return
            arrow = st["arrow"][2] if st["arrow"] else 0
            sig = (st["list_ver"], st["page"], arrow, st["pin"], st["minimized"])
            if sig == st["drawn"]: return
            st["drawn"] = sig; c = win["c"]; lst = st["list"]; near = next((e for e in lst if e["group"] == 0), None)
            n = len(lst); maps = "%d map%s" % (n, "" if n == 1 else "s")
            if near is not None:
                d = near["dist"]
                part = ("here" if d == 0 else "%d tile%s %s" % (d, "" if d == 1 else "s", near["dir"]))
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
                    if r["serial"]: r["prev"] = (r["serial"], now); r["serial"] = 0
                    if k == 0 and n == 0: es = ("empty", EMPTY_TEXT if not st["hidden"] else (status + "."))
                    else: es = ("empty", "")
                    if r["sig"] != es:
                        r["sig"] = es; Kit.set_text(r["lvl"], Kit.fit(es[1], c.get("empty_w", 400)), Kit.HUE_INFO)
                        Kit.set_text(r["name"], ""); Kit.set_text(r["where"], "")
                    show(r["ping"], r, "pvis", False); continue
                e = lst[i]
                if r["serial"] != e["serial"]: r["prev"] = (r["serial"], now); r["serial"] = e["serial"]
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
                say("tracking arrow on the %s map's spot (%d, %d)." % (level_name(e["lvl"]).lower(), e["x"], e["y"]))
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
            gone = [s for s in spots if s not in here]
            for s in gone: del spots[s]
            st["dirty"] = True
            say("forgot %d spot%s of maps not in your pack." % (len(gone), "" if len(gone) == 1 else "s"))
        def draw_spots(f, x, y):
            Kit.add_label(f.g, "%d spot%s remembered" % (len(spots), "" if len(spots) == 1 else "s"), x + 12, y + 4,
                          Kit.HUE_INFO)
            Kit.art_button(f.g, f.store, "forget", Kit.ART_CLOSE, x + f.w - 12 - (35 + Kit.text_w("Forget lost maps")),
                           y, "Forget lost maps", "Forget the dig spots of every map that isn't in your backpack now",
                           on_click=queue("forget"))
        PAGE = (("WINDOW  (open a decoded map once to read its spot)", (
                    ("check", "auto", "Point the tracking arrow at the nearest map's spot",
                     "With no map picked, the tracking arrow points at the nearest dig spot on your facet"),
                    ("check", "undecoded", "List maps not decoded yet",
                     "Shows the maps still to be decoded (Cartography) in the window's list"),
                    ("check", "done", "List maps already dug up",
                     "Shows the maps whose treasure has been dug up in the window's list"))),
                ("SAVED SPOTS", (("custom", 24, draw_spots),), {"sh": 64}), atlas_page("maps"),
                ("DEBUG  (for checking the shard's texts)", (("check", "say", "Print what is read from each map in the "
                 "journal", "Prints the map window's pin, size and bounds and TazUO's estimate line, for checking the "
                 "spots against the shard"),)))
        def config_height(w): return Kit.Form.height(PAGE, w)
        def build_config(g, x, y, w): page["c"] = Kit.Form(g, x, y, w, settings, PAGE).c
        def poll_config():
            c = page["c"]
            if c is None: return
            if read_checks(c, settings, ("auto", "undecoded", "done", "say")):
                save_settings(); st["next_scan"] = 0.0; st["drawn"] = None
        def config_closed(): page["c"] = None
        def _start():
            st.update({"shutting": False, "active": True, "docked": False, "queue": [], "used": [],
                       "minimized": Kit.load_min(MIN_KEY) or bool(safe(lambda: HOST.dock_wanted(KEY), False)),
                       "list": [], "list_sig": None, "next_scan": 0.0, "arrow": None, "pin": 0, "arrow_at": 0.0,
                       "arrow_off": False, "ping": None, "est": None, "look_until": 0.0,
                       "last_map": (0, 0.0), "drawn": None, "page": 0, "atlas_ver": None,
                       "atlas_sig": None, "dig_tiles": set()})
            Kit.kv_load(SETTINGS_KEY, ";", settings); load_maps(); read_gumps.clear(); JR["rd"] = Journal.reader()
            hook_events(); scan(time.time()); build_window()
            HOST.dock_add(KEY, Kit.dock_hooks(TITLE, 0x14EB, st, win, queue("redraw"), scale=True)); update_arrow()
        def _tick():
            if win["g"] is None: return
            if Kit.was_clicked(win["store"], "close"): Kit.dispose(win["g"]); return
            now = time.time()
            if st["used"]: handle_used(now)
            handle_journal(now); look_step(now); q = st["queue"]
            while q:
                a = q.pop(0); kind = a[0] if isinstance(a, tuple) else a
                if kind == "page": st["page"] = max(0, st["page"] + a[1])
                elif kind == "row": do_row(a[1])
                elif kind == "ping": do_ping(a[1], now)
                elif kind == "nearest":
                    st["arrow_off"] = False
                    if settings["auto"]: st["pin"] = 0
                    else:
                        near = next((e for e in st["list"] if e["group"] == 0), None)
                        st["pin"] = near["serial"] if near is not None else 0
                    update_arrow(force=True)
                    if st["arrow"] is None: say("no decoded map with a spot on this facet.")
                elif kind == "arrow_off": st["pin"], st["arrow_off"] = 0, True; update_arrow()
                elif kind == "forget": forget_others(); safe(lambda: HOST.refresh_settings(KEY))
                else: Kit.win_action(kind, st, KEY, TITLE, build_window, MIN_KEY)
                if win["g"] is None: return
            if not (now < st["next_scan"] <= now + SCAN_EVERY):
                st["next_scan"] = now + SCAN_EVERY; scan(now); arrow_closed(now); update_arrow()
                if st["list_ver"] != st["atlas_ver"]: st["atlas_ver"] = st["list_ver"]; atlas_publish()
            if st["ping"] is not None: ping_step(now)
            if st["dirty"] and not (now < st["next_save"] <= now + SAVE_EVERY):
                st["next_save"] = now + SAVE_EVERY; save_maps()
            refresh()
        def _stop():
            st["shutting"] = True; st["active"] = False; HOST.dock_remove(KEY)
            if st["arrow"] is not None: update_arrow(force_off=True)
            Kit.save_pos(POS_KEY, win["g"]); Kit.save_min(MIN_KEY, st["minimized"] and not st["docked"])
            save_settings()
            if st["dirty"]: save_maps()
            JR["rd"] = None; dig_tiles(()); st["used"], st["queue"], st["ping"] = [], [], None
            g, win["g"] = win["g"], None; win["rows"] = []; Kit.dispose(g)
        def _interval(): return 0.1 if st["look_until"] > time.time() else 0.2
        MODULE = {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "interval": _interval,
                  "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE
    def _part_dry():
        KEY = "harvest"; TITLE = "Ore Tracker"; KINDS = ("ore", "wood", "fish", "sand")
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
        WEIGHT_HUE_OK, WEIGHT_HUE_WARN = 0, 0x0035; WEIGHT_ALERT = "harvest.weight"; DRAW_EVERY = 1.0
        EXPIRE_EVERY = 1.0; ARROW_ID = 0x48525654; PING_TRY = 6.0; SAVE_EVERY = 5.0; SETTINGS_KEY = "Harvest_settings"
        SPOTS_KEY = "Harvest_spots"; POS_KEY = "Harvest_pos"; MIN_KEY = "Harvest_min"; W = 440; MINI_W, MINI_H = 340, 46
        ROW_H = 24
        FACING = {"north": (0, -1), "northeast": (1, -1), "east": (1, 0), "southeast": (1, 1),
                  "south": (0, 1), "southwest": (-1, 1), "west": (-1, 0), "northwest": (-1, -1)}
        ROW_TIP = "Click: put the tracking arrow on it (click again to take it down)"
        PING_TIP = ("Send a Look here map ping on this spot, so others know it is dry (needs World Map > Map Pings on)")
        EMPTY_TEXT = "No dry spots yet. When the shard says a spot has run out, it goes here."
        SECS_MAX = 60.0 * GUARDED_RESPAWN_X * max(hi for _, hi in RESPAWN.values())
        settings = {"ore": True, "wood": True, "fish": True, "sand": True, "alert": True, "keep": True, "say": False}
        st = {"rd": None, "ver": 0, "mini_key": None, "w_key": None, "arrow_at": 0.0}; spots = {}; first = {}
        win = {"g": None, "c": {}, "store": ({}, {}), "rows": []}; page = {"c": None}; jobs = []; say = Kit.sayer(TITLE)
        def save_settings(): Kit.kv_save(SETTINGS_KEY, ";", settings, KINDS + ("alert", "keep", "say"))
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
                if hi <= now or hi - now > SECS_MAX + 60: continue
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
                try: API.TrackingArrow(x, y, ARROW_ID); st["arrow_at"] = now
                except Exception: pass
            if len(spots) > 60:
                drop = None
                for k, e in spots.items():
                    if k != key and (drop is None or e["hi"] < spots[drop]["hi"]): drop = k
                if drop is not None:
                    del spots[drop]
                    if st["arrow"] == drop: arrow_off()
            return key
        def respawn_x(): return GUARDED_RESPAWN_X if safe(lambda: HOST.guarded(), None) is True else 1
        def note_dry(kind, x, y, m, about, now):
            key = bank_of(kind, m, x, y); lo_m, hi_m = RESPAWN[kind]; x3 = respawn_x()
            lo_m, hi_m = lo_m * x3, hi_m * x3; f = first.pop(key, None)
            if f is not None and 0 <= now - f < hi_m * 60.0: lo, hi = f + lo_m * 60.0, f + hi_m * 60.0
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
            if a is not None and 1.5 <= now - st["arrow_at"] and not arrow_open():
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
        def clear_spots():
            if st["arrow"] is not None: arrow_off()
            spots.clear(); spots_changed()
        def read_me():
            try:
                p = API.Player
                if p is None: return None
                me = (int(p.X), int(p.Y), int(API.GetMap()))
            except Exception: return None
            if me[0] <= 0 and me[1] <= 0: return None
            st["me"] = me; return me
        def target_tile(kind, me):
            px, py = me[0], me[1]
            try: p = API.LastTargetPos; x, y = int(p.X), int(p.Y)
            except Exception: x = y = -1
            if 0 < x < 0xFFFF and 0 < y < 0xFFFF and max(abs(x - px), abs(y - py)) <= REACH[kind]: return x, y, False
            try: d = str(API.Player.Direction or "").strip().lower()
            except Exception: d = ""
            dx, dy = FACING.get(d, (0, 0)); return px + dx, py + dy, True
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
                low = ln.low.strip(); hit = line_kind(low)
                if hit is None: continue
                what, kind = hit; spk = (ln.name or "").strip()
                if spk.lower() not in SHARD_SPEAKERS:
                    if settings["say"]: say("not the shard's line: %s said \"%s\"." % (spk, ln.text))
                    continue
                if what == "dry" and not settings[kind]: continue
                me = read_me()
                if me is None: continue
                x, y, about = target_tile(kind, me)
                if settings["say"]:
                    say("%s line from \"%s\" (\"%s\"): %s spot %d, %d%s." % (what, spk or "no speaker", ln.text,
                        KIND_NAME[kind].lower(), x, y, " (about: the tile in front of you)" if about else ""))
                if what == "dry": note_dry(kind, x, y, me[2], about, now)
                else: note_back(kind, x, y, me[2], what == "got", now)
        def character_alerts():
            try: s = HOST.by_key.get("character"); return s is not None and bool(s.running)
            except Exception: return False
        def read_weight(now):
            if now < st["w_at"] and st["w_at"] - now <= WEIGHT_EVERY: return
            st["w_at"] = now + WEIGHT_EVERY
            if not settings["alert"] and (win["g"] is None or (st["minimized"] and st["docked"])): return
            try:
                p = API.Player; wt, wmax = int(p.Weight), int(p.WeightMax)
                strength = int(p.Strength) if wmax <= 0 else 0
            except Exception: return
            if wmax <= 0 and strength > 0: wmax = int(WEIGHT_MAX_BASE + WEIGHT_MAX_PER_STR * strength)
            frac = (float(wt) / wmax) if wmax > 0 else -1.0; st["weight"] = (wt, wmax, frac)
            if frac >= WEIGHT_RED:
                if st["w_armed"]:
                    raised = True
                    if settings["alert"] and not character_alerts():
                        try:
                            raised = HOST.alert(WEIGHT_ALERT, "Weight %d/%d (%d%%): nearly "
                                                "overloaded. Unload before you harvest more."
                                                % (wt, wmax, int(frac * 100)), level="warn", who="weight") is not False
                        except Exception: raised = True
                    if raised: st["w_armed"] = False
            elif 0 <= frac < 0.92: st["w_armed"] = True
        def arrow_off():
            if st["arrow"] is None: return
            st["arrow"] = None; st["ver"] += 1; safe(lambda: API.TrackingArrow(-1, -1, ARROW_ID))
        def arrow_to(key):
            e = spots.get(key)
            if e is None: return
            if st["arrow"] == key and arrow_open(True): arrow_off(); return
            me = read_me() or st["me"]
            if me is not None and me[2] != e["m"]:
                say("that spot is in %s; you are in %s." % (Kit.facet_name(e["m"]), Kit.facet_name(me[2]))); return
            try: API.TrackingArrow(e["x"], e["y"], ARROW_ID)
            except Exception as ex: say("couldn't show the tracking arrow (%s)." % ex, Kit.HUE_BAD); return
            st["arrow"], st["arrow_at"] = key, time.time(); st["ver"] += 1
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
            else: say("the ping on %s failed." % p[4], Kit.HUE_BAD)
        def mins(secs):
            secs = max(0, int(secs))
            if secs < 60: return "%ds" % secs
            return "%dm" % ((secs + 59) // 60)
        def dist_of(e, me):
            if me is None: return 0
            if me[2] != e["m"]: return 1 << 30
            if bank_of(e["kind"], me[2], me[0], me[1]) == e["key"]: return 0
            return max(abs(e["x"] - me[0]), abs(e["y"] - me[1]))
        def where_text(e, me):
            if me is None: return "(%d, %d)" % (e["x"], e["y"])
            if me[2] != e["m"]: return "in %s" % Kit.facet_name(e["m"])
            if bank_of(e["kind"], me[2], me[0], me[1]) == e["key"]: return "here"
            dx, dy = e["x"] - me[0], e["y"] - me[1]; dist = max(abs(dx), abs(dy))
            return "%s%d tile%s %s" % ("about " if e["about"] else "", dist, "" if dist == 1 else "s",
                                       Kit.compass(dx, dy))
        def back_text(e, now):
            if now < e["lo"]: return "back in %s-%s" % (mins(e["lo"] - now), mins(e["hi"] - now)), Kit.HUE_BAD
            return "back within %s" % mins(e["hi"] - now), Kit.HUE_TITLE
        def row_tip(e, on):
            bw, bh = BANK[e["kind"]]; x0, y0 = (e["x"] // bw) * bw, (e["y"] // bh) * bh
            when = time.strftime("%H:%M", time.localtime(e["hi"]))
            if e["lo"] > e["at"]:
                back = "back between %s and %s" % (time.strftime("%H:%M", time.localtime(e["lo"])), when)
            else: back = "back by %s at the latest" % when
            return "%s ran dry at %d, %d%s: the %dx%d block from %d, %d, %s.  %s" % (
                KIND_NAME[e["kind"]], e["x"], e["y"], " (about: the tile in front of you)" if e["about"] else "",
                bw, bh, x0, y0, back, "Click: take the tracking arrow down" if on else ROW_TIP)
        def shown_spots(): return [e for e in spots.values() if settings[e["kind"]]]
        def _by_place(t): return (t[0], t[1])
        def atlas_publish():
            items = {}
            for e in sorted(shown_spots(), key=lambda e: -e["at"])[:15]:
                name = atlas_name("%s dry %d %d" % (KIND_NAME[e["kind"]], e["x"], e["y"]))
                items[name] = (int(e["x"]), int(e["y"]), int(e["m"]), "blue")
            ATLAS.set("dry", items)
        queue = Kit.queuer(st); on_disposed = Kit.disposer(KEY, st, win); LIST_H = 74 + ROWS * ROW_H + 22
        def build_window():
            M = Kit.MARGIN
            g, store, c, w, h, x, y, old = open_window(st, win, POS_KEY, (MINI_W, MINI_H),
                (W, M + 30 + Kit.GAP + 46 + Kit.GAP + 36 + Kit.GAP + LIST_H + M), (260, 220), TITLE, KEY, queue)
            rows = []
            if not st["minimized"]:
                IW = w - 2 * M; yw = M + 30 + Kit.GAP; Kit.add_section(g, M, yw, IW, 46, "WEIGHT")
                c["wtext"] = Kit.add_label(g, "", M + 20 + Kit.text_w("WEIGHT"), yw + 6, Kit.HUE_TEXT)
                build_weight_bar(g, c, M + 12, yw + 28, IW - 24); yt = yw + 46 + Kit.GAP
                Kit.add_section(g, M, yt, IW, 36); bx = M + 12
                Kit.art_button(g, store, "clear", Kit.ART_CLOSE, bx, yt + 7, "Clear",
                               "Empty the list of dry spots", on_click=queue("clear"))
                bx += 35 + Kit.text_w("Clear") + 16
                Kit.art_button(g, store, "arrow_off", Kit.ART_CLOSE, bx, yt + 7, "Arrow off",
                               "Take the tracking arrow down", on_click=queue("arrow_off"))
                yl = yt + 36 + Kit.GAP; Kit.add_section(g, M, yl, IW, LIST_H, "DRY SPOTS  (nearest first)")
                c["here"] = Kit.add_label(g, "", M + 12, yl + 28, Kit.HUE_INFO); ping_w = 35 + Kit.text_w("Ping")
                xk, xw, xb = M + 12, M + 12 + 52, M + 12 + 52 + 130; xp = M + IW - 6 - ping_w; c["back_w"] = xp - 8 - xb
                yh = yl + 52; Kit.add_label(g, "What", xk, yh, Kit.HUE_TITLE)
                Kit.add_label(g, "Where", xw, yh, Kit.HUE_TITLE); Kit.add_label(g, "When", xb, yh, Kit.HUE_TITLE)
                for k in range(ROWS):
                    ry = yh + 22 + k * ROW_H
                    r = {"key": None, "prev": (None, 0.0), "sig": None, "vis": True, "tip": None,
                         "kind": Kit.add_label(g, "", xk, ry + 3, Kit.HUE_TEXT),
                         "where": Kit.add_label(g, "", xw, ry + 3, Kit.HUE_TEXT),
                         "back": Kit.add_label(g, "", xb, ry + 3, Kit.HUE_INFO)}
                    r["catch"] = Kit.catcher(g, M + 6, ry, xp - 4 - (M + 6), ROW_H,
                                             row_clicker(lambda: win["rows"], k, "key", "arrow", queue), ROW_TIP)
                    r["plbl"] = Kit.art_button(g, store, "ping%d" % k, Kit.ART_PLAY, xp, ry, "Ping", PING_TIP,
                                               on_click=row_clicker(lambda: win["rows"], k, "key", "ping", queue))
                    r["pbtn"] = store[0].get("ping%d" % k); rows.append(r)
                c["more"] = Kit.add_label(g, "", M + 12, yh + 22 + ROWS * ROW_H + 2, Kit.HUE_INFO)
            show_window(g, x, y, w, h, st, win, on_disposed, POS_KEY, c=c, store=store, rows=rows)
            st["drawn"] = st["mini_drawn"] = st["wdrawn"] = None; st["draw_at"] = 0.0; refresh(time.time())
            Kit.dispose(old)
        def build_weight_bar(g, c, bx, by, bw):
            lw, lh = Kit.pic_size(Kit.LINE_RED); fh = max(4, min(11, Kit.pic_size(Kit.LINE_BLUE)[1] or lh or 9))
            if lw > 0: Kit.add_tiled(g, Kit.LINE_RED, bx, by, bw, fh, hue=946)
            else: Kit.add_tiled(g, Kit.SECTION_TILE, bx, by, bw, fh, 1.0)
            fills = {}
            for kind, art, hue in (("ok", Kit.LINE_POISON, WEIGHT_HUE_OK), ("warn", Kit.LINE_BLUE, WEIGHT_HUE_WARN),
                                   ("red", Kit.LINE_RED, 0)):
                f = Kit.add_tiled(g, art, bx, by, 1, fh, hue=hue)
                if f is not None: safe(lambda f=f: setattr(f, "IsVisible", False)); fills[kind] = f
            c["wfills"] = fills; c["wbar_w"] = bw
        def show_row(r, on):
            if r["vis"] == on: return
            r["vis"] = on
            for n in ("where", "back", "catch", "pbtn", "plbl"):
                ctl = r.get(n)
                if ctl is not None:
                    try: ctl.IsVisible = on
                    except Exception: pass
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
                txt = "%s: %s, %d dry spot%s" % (
                    TITLE, ("weight %d%%" % int(wt[2] * 100)) if wt and wt[2] >= 0 else "weight ?",
                    n, "" if n == 1 else "s")
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
                    KIND_NAME[here["kind"]].lower(), back_text(here, now)[0]), W - 2 * Kit.MARGIN - 24), Kit.HUE_BAD)
            elif listed: Kit.set_text(c["here"], "Here: nothing known dry", Kit.HUE_GOOD)
            else: Kit.set_text(c["here"], Kit.fit(EMPTY_TEXT, W - 2 * Kit.MARGIN - 24), Kit.HUE_INFO)
            back_w = c.get("back_w", 160)
            for k, r in enumerate(win["rows"]):
                if k >= len(listed):
                    if r["key"] is not None: r["prev"] = (r["key"], now); r["key"] = None
                    r["sig"] = None; show_row(r, False); continue
                e = listed[k][2]; where = where_text(e, me); key = e["key"]
                if r["key"] != key: r["prev"] = (r["key"], now); r["key"] = key
                on = st["arrow"] == key; back, bhue = back_text(e, now)
                rsig = (key, where, back, bhue, on, e["lo"], e["hi"]); show_row(r, True)
                if rsig == r["sig"]: continue
                r["sig"] = rsig; Kit.set_text(r["kind"], KIND_NAME[e["kind"]], KIND_HUE.get(e["kind"], Kit.HUE_TEXT))
                Kit.set_text(r["where"], Kit.fit(("> " if on else "") + where, 124),
                             Kit.HUE_TITLE if on else Kit.HUE_TEXT)
                Kit.set_text(r["back"], Kit.fit(back, back_w), bhue); tip = (key, on, e["lo"], e["hi"])
                if tip != r["tip"]:
                    r["tip"] = tip
                    try: r["catch"].SetTooltip(row_tip(e, on))
                    except Exception: pass
            more = len(listed) - len(win["rows"])
            Kit.set_text(c["more"], ("+%d farther" % more) if more > 0 else "", Kit.HUE_INFO)
        def draw_weight():
            c = win["c"]; wt = st["weight"]
            if st["wdrawn"] is not None and wt == st["w_key"]: return
            st["w_key"] = wt; fills = c.get("wfills")
            if wt is None or wt[2] < 0: text, kind, width = "not known yet", None, 0
            else:
                frac = wt[2]; text = "%d / %d stones (%d%%)" % (wt[0], wt[1], int(frac * 100))
                kind = "red" if frac >= WEIGHT_RED else ("warn" if frac >= WEIGHT_WARN else "ok")
                bw = c.get("wbar_w", 100); width = max(1, min(bw, int(round(bw * min(1.0, frac)))))
            sig = (text, kind, width)
            if sig == st["wdrawn"]: return
            st["wdrawn"] = sig; hue = {"red": Kit.HUE_BAD, "warn": Kit.HUE_TITLE}.get(kind, Kit.HUE_TEXT)
            if c.get("wtext") is not None: Kit.set_text(c["wtext"], text, hue)
            for k, f in (fills or {}).items():
                try:
                    if k == kind: Kit.ui_w(f, width)
                    f.IsVisible = k == kind
                except Exception: pass
        RESPAWN_NOTE = ("Back in: ore and sand 10-20 min, wood 20-30, fish 10-20, counted from "
                        "the block's first harvest (3x as long in guarded towns).")
        def kind_caption(kind): return "%s (%s)" % (KIND_NAME[kind], KIND_SKILL[kind])
        def kind_cols(w):
            widest = max(Kit.text_w(kind_caption(k)) for k in KINDS); return 2 if widest + 30 <= (w - 24) // 2 else 1
        def page_table(w):
            cols, half = kind_cols(w), (w - 24) // 2
            return (("WHAT TO WATCH", [("check", k, kind_caption(k), "List the spots where the shard says the %s has "
                                        "run out" % KIND_NAME[k].lower(), {"dx": 12 + (i % cols) * half,
                                        "stay": i % cols < cols - 1}) for i, k in enumerate(KINDS)] + [("gap", 6),
                        ("check", "keep", "Keep the list when Virtue Assistant stops (per character)",
                         "Unticked: the list starts empty at every start"), ("gap", 2)] + [("note", ln) for ln in
                        ["Unticked kinds are hidden, not forgotten."] + Kit.wrap(RESPAWN_NOTE, w - 28)], {"top": 32}),
                    ("WEIGHT  (yellow at %d%%, red at %d%%)" % (int(WEIGHT_WARN * 100), int(WEIGHT_RED * 100)), (
                        ("check", "alert", "Alert as you cross the red line", "One alert each time you cross %d%% of "
                         "your maximum weight (sound: Settings > Alerts); quiet while Inventory > Paperdoll is on, "
                         "which has its own" % int(WEIGHT_RED * 100)),), {"top": 32, "pad": 4}), atlas_page("dry"),
                    ("DEBUG  (for checking the shard's texts)", (("check", "say", "Print each harvest line read in the "
                     "journal", "Prints every harvest line this part reads, with its speaker and the spot it took, for "
                     "checking the shard's wording"),)))
        def config_height(w): return Kit.Form.height(page_table(w), w)
        def build_config(g, x, y, w): page["c"] = Kit.Form(g, x, y, w, settings, page_table(w)).c
        def poll_config():
            c = page["c"]
            if c is None: return
            hit = read_checks(c, settings, ("ore", "wood", "fish", "sand", "keep", "alert", "say"))
            if "keep" in hit: st["save_due"] = True
            if "alert" in hit and settings["alert"]: st["w_armed"] = True
            if hit: save_settings(); st["drawn"] = st["mini_drawn"] = None
        def config_closed(): page["c"] = None
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "drawn": None,
                       "mini_drawn": None, "wdrawn": None, "arrow": None, "ping": None,
                       "w_armed": True, "weight": None, "w_at": 0.0, "draw_at": 0.0,
                       "expire_at": 0.0, "save_due": False, "save_at": 0.0, "me": None,
                       "count": (None, 0), "last_now": None, "atlas": None, "minimized": Kit.load_min(MIN_KEY)
                       or bool(safe(lambda: HOST.dock_wanted(KEY), False))})
            del jobs[:]; first.clear(); Kit.kv_load(SETTINGS_KEY, ";", settings); load_spots()
            st["rd"] = Journal.reader(); safe(lambda: HOST.alert_kind(WEIGHT_ALERT, "Weight near the limit", 0x04A))
            read_me(); build_window(); HOST.dock_add(KEY, Kit.dock_hooks(TITLE, 0x0E86, st, win, queue("redraw")))
        def _tick():
            if win["g"] is None: return
            if Kit.was_clicked(win["store"], "close"): Kit.dispose(win["g"]); return
            now = time.time(); last, st["last_now"] = st["last_now"], now
            if last is not None and now < last - 2.0: rebase(now - last)
            q = st["queue"]
            while q:
                action = q.pop(0); kind = action[0] if isinstance(action, tuple) else action
                if action == "clear": clear_spots()
                elif action == "arrow_off": arrow_off()
                elif kind == "arrow": arrow_to(action[1])
                elif kind == "ping": ping_spot(action[1])
                else: Kit.win_action(action, st, KEY, TITLE, build_window, MIN_KEY)
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
            st["shutting"] = True; HOST.dock_remove(KEY)
            if st["arrow"] is not None: arrow_off()
            st["ping"] = st["rd"] = None; del jobs[:]; Kit.save_pos(POS_KEY, win["g"])
            Kit.save_min(MIN_KEY, st["minimized"] and not st["docked"]); save_settings()
            Kit.put_var(SPOTS_KEY, spots_text() if settings["keep"] else ""); st["save_due"] = False
            g, win["g"], win["rows"], win["c"] = win["g"], None, [], {}; Kit.dispose(g)
        MODULE = {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "thread_tick": _thread_tick,
                  "thread_wanted": _thread_wanted, "config_height": config_height, "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE
    def _part_traps():
        KEY = "traphl"; TITLE = "Traps & Fields"; SETTINGS_KEY = "TrapHL_settings"; POS_KEY = "TrapHL_pos"
        VIEW_KEY = "TrapHL_view"; H = Kit.MARGIN + 30 + Kit.GAP + 40 + Kit.MARGIN; MINI_W, MINI_H = 320, 46
        HUE_GREEN = 68; HUE_RED = 33; HUE_MAX = 3000
        DEFAULT_GRAPHICS = [0x1103, 0x1116, 0x11AC, 0x11B1, 0x11A0, 0x11A8, 0x11B8, 0x113C, 0x1147, 0x10F5, 0x10FC,
            0x1125, 0x1B71, 0x1B72, 0x1B73, 0x1B74, 0x0E70,]
        FIELDS_KEY = "TrapHL_fields"
        FIELD_RANGES = (("fire", 0x398C, 0x399F), ("poison", 0x3914, 0x3929),
                        ("paralyze", 0x3967, 0x398A), ("energy", 0x3946, 0x3964))
        FIELD_LOOKUP = (0x398C, 0x3996, 0x3915, 0x3922, 0x3967, 0x3979, 0x3946, 0x3956); FIELD_HUE = 0x0035
        PARALYZE_HUE = 0x0481
        FIELD_WORDS = {"fire": ("Fire field", Kit.HUE_TITLE), "poison": ("Poison field", Kit.HUE_TITLE),
                       "energy": ("Energy field", Kit.HUE_TITLE), "paralyze": ("Paralyze field!", Kit.HUE_BAD)}
        FIELD_SAY_NEAR = 3; ALERT_TRAP = "traphl.trap"
        FIELD_GFX = {g: k for k, a, b in FIELD_RANGES for g in range(a, b + 1)}; NO_FIELDS = {}
        settings = {"range": 14, "cycle": 2.0, "pulse": True,
                    "green": HUE_GREEN, "red": HUE_RED, "by_name": True, "graphics": list(DEFAULT_GRAPHICS),
                    "ping": True, "fields": True, "field_hue": FIELD_HUE, "para_hue": PARALYZE_HUE, "field_say": False}
        st = {}; win = {"g": None, "c": {}, "store": ({}, {})}; page = {"c": None, "gfx_typed": None, "gfx_since": 0.0}
        say = Kit.sayer(TITLE)
        def load_settings():
            p = Kit.get_var(SETTINGS_KEY).split("|")
            if len(p) < 7: return
            try:
                settings["range"] = max(1, min(30, int(p[0]))); settings["cycle"] = max(0.5, min(10.0, float(p[1])))
                settings["pulse"] = p[2] == "1"; settings["green"] = int(p[3]); settings["red"] = int(p[4])
                settings["by_name"] = p[5] == "1"; gl = parse_graphics(p[6])
                if gl: settings["graphics"] = gl
                if len(p) >= 8: settings["ping"] = p[7] != "0"
            except Exception: pass
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
            raw = Kit.get_var(VIEW_KEY); v = dict(p.split("=", 1) for p in raw.split(";") if "=" in p)
            st["minimized"] = v.get("min") == "1"; st["paused"] = v.get("paused") == "1"
            st["say_graphics"] = v.get("say") == "1"; st["view_saved"] = raw
        def save_view():
            data = "min=%d;paused=%d;say=%d" % (int(bool(st["minimized"])), int(bool(st["paused"])),
                                                int(bool(st["say_graphics"])))
            if data != st.get("view_saved"): st["view_saved"] = data; Kit.put_var(VIEW_KEY, data)
        _hue_setters = {}; _ent_member = {}
        def _member_value(m, item):
            return m.GetValue(item, None) if hasattr(m, "GetIndexParameters") else m.GetValue(item)
        def _clr_entity(item):
            m = _ent_member.get(type(item))
            if m is not None:
                try:
                    v = _member_value(m, item)
                    if v is not None and v is not item: return v
                except Exception: pass
            try:
                import clr; from System.Reflection import BindingFlags
                flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic
                t = clr.GetClrType(type(item))
                while t is not None:
                    for m in list(t.GetProperties(flags)) + list(t.GetFields(flags)):
                        try: v = _member_value(m, item)
                        except Exception: continue
                        if v is None or v is item: continue
                        vt = v.GetType()
                        if (vt.GetProperty("Hue") is not None and vt.GetProperty("Serial") is not None):
                            _ent_member[type(item)] = m; return v
                    t = t.BaseType
            except Exception: pass
            return None
        def set_hue(item, hue):
            hue = int(hue) & 0xFFFF; tn = type(item).__name__; way = _hue_setters.get(tn)
            if way == "none": return False
            for w in ((way,) if way is not None else _HUE_WAYS):
                if _HUE_SET[w](item, hue): _hue_setters[tn] = w; return True
            if way is None: _hue_setters[tn] = "none"
            return False
        def _hue_by_method(item, hue):
            fn = getattr(item, "SetHue", None)
            if fn is None: return False
            try: fn(hue); return True
            except Exception: return False
        def _hue_by_attr(item, hue):
            try: item.Hue = hue; return int(item.Hue) == hue
            except Exception: return False
        def _hue_by_clr(item, hue):
            ent = _clr_entity(item)
            if ent is None: return False
            try: ent.Hue = hue; return True
            except Exception: return False
        _HUE_WAYS = ("method", "attr", "clr")
        _HUE_SET = {"method": _hue_by_method, "attr": _hue_by_attr, "clr": _hue_by_clr}
        def int_of(item, name):
            try: return int(getattr(item, name) or 0)
            except Exception: return 0
        def get_hue(item):
            try: return int(item.Hue or 0)
            except Exception: return 0
        def xy_of(item): return int_of(item, "X"), int_of(item, "Y")
        scan_how = {"ground": None, "form": None}; ANY_CONTAINER = 0xFFFFFFFF
        FTA_FORMS = (lambda g, r: API.FindTypeAll(g, ANY_CONTAINER, r, 0xFFFF),
                     lambda g, r: API.FindTypeAll(g, 0, r, 0xFFFF), lambda g, r: API.FindTypeAll(g, ANY_CONTAINER, r),
                     lambda g, r: API.FindTypeAll(g, 0, r))
        verdicts = {}; VERDICT_SIG = {"gfx": None, "wanted": frozenset(), "by_name": None, "fields": None}
        SKIP_SCAN = False
        def ground_all(rng):
            if scan_how["ground"] is False: return None
            try: res = API.GetItemsOnGround(rng)
            except Exception:
                if scan_how["ground"] is None: scan_how["ground"] = False; return None
                return SKIP_SCAN
            scan_how["ground"] = True; return res if res is not None else ()
        def ground_items_of(graphic, rng):
            form = scan_how["form"]
            for k in ((form,) if form is not None else range(len(FTA_FORMS))):
                try: res = FTA_FORMS[k](graphic, rng)
                except Exception: continue
                scan_how["form"] = k; return [i for i in (res or []) if is_on_ground(i)]
            return []
        def is_on_ground(item):
            try: cont = int(item.Container or 0)
            except Exception: cont = 0
            if cont and cont not in (0, 0xFFFFFFFF, -1): return False
            try: rp = int(item.RootContainer or 0); return not rp or rp == int(item.Serial)
            except Exception: return True
        def named_trap(it):
            try: name = str(it.Name or "").lower()
            except Exception: name = ""
            if not name: return None
            return "trap" in name and "scroll" not in name and "kit" not in name
        def verdict_sig():
            sig = VERDICT_SIG; gl = settings["graphics"]
            if sig["gfx"] is not gl or sig["by_name"] != settings["by_name"] or sig["fields"] != settings["fields"]:
                sig["gfx"], sig["wanted"] = gl, frozenset(gl)
                sig["by_name"], sig["fields"] = settings["by_name"], settings["fields"]; verdicts.clear()
            return sig["wanted"]
        def scan():
            rng = int(settings["range"]); st["atlas_map"] = None; found = {}; ffound = {}; items = ground_all(rng)
            if items is SKIP_SCAN: return
            st["scans"] += 1; check_hues = st["scans"] % 3 == 0
            field_gfx = FIELD_GFX if settings["fields"] else NO_FIELDS
            if items is None:
                for gfx in settings["graphics"]:
                    for it in ground_items_of(gfx, rng):
                        try: found[int(it.Serial)] = it
                        except Exception: pass
                if field_gfx:
                    for gfx in FIELD_LOOKUP:
                        if gfx in settings["graphics"]: continue
                        for it in ground_items_of(gfx, rng):
                            try:
                                s_ = int(it.Serial)
                                if s_ not in found: ffound[s_] = it
                            except Exception: pass
            else:
                wanted = verdict_sig(); by_name = settings["by_name"]; scans = st["scans"]; old = verdicts; seen = {}
                for it in items:
                    try:
                        serial = int(it.Serial); g = int(it.Graphic); v = old.get(serial)
                        if v is not None and v[0] == g and (not v[2] or scans < v[2]): kind = v[1]; seen[serial] = v
                        else:
                            retry = 0
                            if g in wanted: kind = 1
                            elif by_name and g not in field_gfx:
                                named = named_trap(it)
                                if named is None: kind, retry = 0, scans + 5
                                else: kind = 1 if named else 0
                            else: kind = 2 if g in field_gfx else 0
                            seen[serial] = (g, kind, retry)
                        if kind == 1: found[serial] = it
                        elif kind == 2: ffound[serial] = it
                    except Exception: continue
                verdicts.clear(); verdicts.update(seen)
            tracked = st["tracked"]; new_traps = []
            for serial, it in found.items():
                rec = tracked.get(serial)
                if rec is None:
                    orig = get_hue(it)
                    if orig in (settings["green"], settings["red"]): orig = 0
                    tracked[serial] = {"item": it, "orig": orig, "set": settings["green"]}
                    set_hue(it, settings["green"]); atlas_seen(it)
                    if settings["ping"] and serial not in st["pinged"]: st["ping_wait"].append(serial)
                    if serial not in st["alerted"]: new_traps.append(it)
                    if st["say_graphics"]:
                        say("trap 0x%04X (serial 0x%X) at %d, %d." % (int_of(it, "Graphic"), serial, int_of(it, "X"),
                                                                    int_of(it, "Y")))
                else:
                    rec["item"] = it
                    if check_hues and get_hue(it) != rec["set"]: set_hue(it, rec["set"])
            gone = [s for s in tracked if s not in found]
            for serial in gone: restore(serial)
            if gone and st["ping_wait"]: st["ping_wait"] = [s for s in st["ping_wait"] if s in tracked]
            if new_traps: alert_new_traps(new_traps)
            if ffound or st["fields"]: scan_fields(ffound, check_hues)
        def atlas_seen(it):
            x, y = xy_of(it)
            if x <= 0 or y <= 0: return
            if st["atlas_map"] is None:
                try: st["atlas_map"] = int(API.GetMap())
                except Exception: return
            spot = (x, y, st["atlas_map"]); seen = st["atlas_traps"]
            if spot in seen: return
            seen.append(spot)
            if len(seen) > 20: del seen[0]
            st["atlas_ver"] += 1
        def atlas_publish():
            items = {}
            for x, y, m in st["atlas_traps"]: items[atlas_name("Trap %d %d" % (x, y))] = (x, y, m, "red")
            ATLAS.set("traps", items)
        DIRS = ("north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west")
        def where(dx, dy):
            d = max(abs(dx), abs(dy))
            if d == 0: return "under you"
            a = math.degrees(math.atan2(dx, -dy)) % 360.0
            return "%d tile%s %s" % (d, "" if d == 1 else "s", DIRS[int((a + 22.5) // 45.0) % 8])
        def alert_new_traps(its):
            alerted = st["alerted"]
            if len(alerted) + len(its) > 5000: alerted.clear()
            for it in its: safe(lambda: alerted.add(int(it.Serial)))
            p = API.Player
            try: px, py = int(p.X), int(p.Y)
            except Exception: px = py = None
            best, best_d, bdx, bdy = None, None, 0, 0
            if px is not None:
                for it in its:
                    try: dx, dy = int(it.X) - px, int(it.Y) - py
                    except Exception: continue
                    d = max(abs(dx), abs(dy))
                    if best_d is None or d < best_d: best, best_d, bdx, bdy = it, d, dx, dy
            w = where(bdx, bdy) if best is not None else ""
            if len(its) == 1: text = "A trap %s" % w if w else "A trap in range"
            else: text = "%d new traps in range%s" % (len(its), " (nearest %s)" % w if w else "")
            safe(lambda: HOST.alert(ALERT_TRAP, text, who=int((best if best is not None else its[0]).Serial)))
        def field_hue(kind): return settings["para_hue"] if kind == "paralyze" else settings["field_hue"]
        def scan_fields(ffound, check_hues):
            fields = st["fields"]; said_now = []
            for serial, it in ffound.items():
                rec = fields.get(serial)
                if rec is None:
                    kind = FIELD_GFX.get(int_of(it, "Graphic"))
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
            now = time.time(); said = [e for e in st["field_said"] if now - e[3] < 10.0]; spots = []
            for rec in recs: it = rec["item"]; x, y = xy_of(it); spots.append((x, y, rec["kind"], it))
            spots.sort(key=lambda e: (e[0], e[1]))
            for x, y, kind, it in spots:
                dup = False
                for k, sx, sy, t in said:
                    if (k == kind and abs(sx - x) <= FIELD_SAY_NEAR and abs(sy - y) <= FIELD_SAY_NEAR):
                        dup = True; break
                said.append((kind, x, y, now))
                if dup: continue
                text, hue = FIELD_WORDS.get(kind, ("Field", Kit.HUE_TITLE))
                safe(lambda: API.HeadMsg(text, int(it.Serial), hue))
            st["field_said"] = said[-20:]
        def restore_field(serial):
            rec = st["fields"].pop(serial, None)
            if rec is not None and rec["set"]: put_back(serial, rec)
        def restore(serial):
            rec = st["tracked"].pop(serial, None)
            if rec is not None: put_back(serial, rec)
        def put_back(serial, rec):
            try: it = API.FindItem(serial) or rec["item"]
            except Exception: it = rec["item"]
            if it is not None: set_hue(it, rec["orig"])
        def restore_all():
            for serial in list(st["tracked"]): restore(serial)
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
                if m is None:
                    try: m = int(API.GetMap())
                    except Exception: return
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
            if st["paused"]:
                msg = ("paused: untick Pause highlighting on the World Map settings page to find and ping traps.")
            elif n == 0: msg = "no traps in range to ping; each trap will be pinged when next found."
            elif ping_service() is None:
                msg = ("%d trap%s to ping once World Map > Map Pings is on." % (n, "" if n == 1 else "s"))
            else: msg = "pinging %d trap%s." % (n, "" if n == 1 else "s")
            say(msg); st["ping_noted"] = False; refresh()
        def ping_status():
            n = len(st["ping_wait"])
            if n and st["ping_svc"] is not None: return "sending %d" % n, Kit.HUE_INFO
            if not settings["ping"]: return "auto-ping off", Kit.HUE_INFO
            if st["ping_svc"] is None: return "World Map > Map Pings is off", Kit.HUE_BAD
            return "%d sent" % st["ping_sent"], Kit.HUE_GOOD
        queue = Kit.queuer(st); on_disposed = Kit.disposer(KEY, st, win)
        SAY_TIP = ("Prints each new trap's graphic id and where it is, for checking and extending "
                   "the graphics list; untick to stop")
        PING_TIP = ("Send a Danger! map ping on every highlighted trap now, and let each be "
                    "pinged once more when next found (needs World Map > Map Pings on)")
        PING_CAP = "Ping traps on screen"
        def build_window():
            g, store, c, w, h, x, y, old = open_window(st, win, POS_KEY, (MINI_W, MINI_H), (320, H), (200, 200), TITLE,
                                                       KEY, queue)
            if not st["minimized"]:
                M = Kit.MARGIN; yb = M + 30 + Kit.GAP; Kit.add_section(g, M, yb, w - 2 * M, h - yb - M)
                Kit.art_button(g, store, "ping", Kit.ART_CIRCLE, M + 12, yb + 12, PING_CAP,
                               PING_TIP, on_click=queue("ping_again"))
            show_window(g, x, y, w, h, st, win, on_disposed, POS_KEY, c=c, store=store); refresh(); save_view()
            Kit.dispose(old)
        def refresh():
            c = win["c"]; n = len(st["tracked"]); nf = len(st["fields"])
            if st["paused"]: text, hue = "Paused", Kit.HUE_INFO
            elif n == 0 and nf == 0: text, hue = "No traps in range", Kit.HUE_INFO
            elif nf == 0: text, hue = "Highlighting %d trap%s" % (n, "" if n == 1 else "s"), Kit.HUE_GOOD
            elif n == 0: text, hue = "Highlighting %d field%s" % (nf, "" if nf == 1 else "s"), Kit.HUE_GOOD
            else:
                text, hue = "Highlighting %d trap%s, %d field%s" % (
                    n, "" if n == 1 else "s", nf, "" if nf == 1 else "s"), Kit.HUE_GOOD
            if c.get("status") is not None:
                Kit.set_text(c["status"], Kit.fit("%s: %s" % (TITLE, journal_case(text)), MINI_W - 90), hue)
            sc = page["c"]
            if sc is not None and sc.get("say") is not None:
                try:
                    if bool(sc["say"].IsChecked) != bool(st["say_graphics"]):
                        sc["say"].SetIsChecked(bool(st["say_graphics"]))
                except Exception: pass
            if sc is not None and sc.get("now") is not None:
                Kit.set_text(sc["now"], text, hue); ptext, phue = ping_status()
                Kit.set_text(sc["now_ping"], "Pings: " + ptext, phue)
                if st["pause_want"] is None:
                    try:
                        if bool(sc["paused"].IsChecked) != bool(st["paused"]):
                            sc["paused"].SetIsChecked(bool(st["paused"]))
                    except Exception: pass
        def draw_status(f, x, y):
            f.c["now"] = Kit.add_label(f.g, "", x + 12, y, Kit.HUE_GOOD)
            f.c["now_ping"] = Kit.add_label(f.g, "", x + 12 + f.w // 2, y, Kit.HUE_INFO)
        def draw_cycle(f, x, y):
            Kit.add_label(f.g, "Pulse cycle:", x + 12, y + 4); cyc = int(round(settings["cycle"] * 10))
            f.c["cycle"] = Kit.with_tip(Kit.add_slider(f.g, x + 120, y + 2, 160, 5, 100, cyc),
                                        "Seconds between red flashes (0.5-10)")
            f.c["cycle_v"] = Kit.add_label(f.g, "%.1f s" % settings["cycle"], x + 290, y + 4, Kit.HUE_INFO)
        def draw_graphics(f, x, y):
            f.c["graphics"] = Kit.with_tip(Kit.add_textbox(f.g, graphics_text(), x + 12, y, f.w - 28, numbers=False),
                                           "Item graphics counted as traps, in hex (0x1103, 1103 and 0x11AC all do), "
                                           "separated by commas. Applied once you stop typing.")
        LEFT = {"lw": 98, "fw": 60, "stay": True}
        PAGE = (("STATUS  (the window has %s)" % PING_CAP, (("custom", 24, draw_status),
                    ("check", "paused", "Pause highlighting (the hues are put back)", "Stops the scan and gives every "
                     "trap and field its own hue back; untick to highlight again")), {"pad": 4}),
                ("TRAPS  (hues are client hue numbers)", (
                    ("slider", "range", "Scan range:", "Tiles round you looked at for traps, once a second (1-30)",
                     1, 30, {"lw": 98, "ldy": 4, "sw": 160, "ugap": 10, "vfmt": "%d tiles"}),
                    ("custom", 29, draw_cycle),
                    ("num", "green", "Green hue:", "The hue traps are held at (client hue 1-%d; %d is the default "
                     "green)" % (HUE_MAX, HUE_GREEN), None, 1, HUE_MAX, LEFT),
                    ("num", "red", "Red hue:", "The hue of the pulse (client hue 1-%d; %d is the default red)"
                     % (HUE_MAX, HUE_RED), None, 1, HUE_MAX, {"dx": 200, "lw": 70, "fw": 60, "h": 29}),
                    ("check", "pulse", "Pulse red once per cycle (unticked: steady green)",
                     "Flashes every highlighted trap red for a beat once per cycle")), {"top": 32, "pad": 2}),
                ("TRAP GRAPHICS  (hex ids, comma separated)", (("custom", 30, draw_graphics),
                    ("check", "by_name", "Also highlight ground items the client names 'trap'", "Catches traps whose "
                     "art id isn't in the list (the client knows a name only after a tooltip or a single click)")),
                 {"top": 32, "pad": 8}),
                ("TRAP PINGS  (needs World Map > Map Pings)", (("check", "ping", "Send a Danger! map ping on each "
                  "new trap, once per trap", "A Danger! map ping on each new trap's tile, for you and your guildmates. "
                  "Once per trap: \"%s\" on the window pings them all again." % PING_CAP),), {"top": 32, "pad": 4}),
                ("MAGIC FIELDS  (client hue numbers, 0 = leave as is)", (
                    ("check", "fields", "Highlight magic fields: fire, poison, energy, paralyze", "Recolour field "
                     "items on the ground (client-side only, like the traps); paralyze fields get a hue of their own",
                     {"h": 29}),
                    ("num", "field_hue", "Field hue:", "The hue of fire, poison and energy fields (client hue 0-%d; 0 "
                     "leaves them as they are; %d by default)" % (HUE_MAX, FIELD_HUE), None, 0, HUE_MAX, LEFT),
                    ("num", "para_hue", "Paralyze hue:", "The hue of paralyze fields, the ones that matter most in a "
                     "fight (client hue 0-%d; 0 leaves them as they are; %d by default)" % (HUE_MAX, PARALYZE_HUE),
                     None, 0, HUE_MAX, {"dx": 200, "lgap": 12, "fw": 60, "h": 29}),
                    ("check", "field_say", "Show an overhead text when a field appears",
                     "Names each new field above it once (\"Fire field\", \"Paralyze field!\")")),
                 {"top": 32, "pad": 2}), atlas_page("traps"),
                ("DEBUG  (for checking the shard's traps)", (("check", "say", "Print each new trap's graphic id in the "
                 "journal", SAY_TIP),)))
        def build_config(g, x, y, w):
            page["c"] = Kit.Form(g, x, y, w, dict(settings, paused=st["paused"], say=st["say_graphics"]), PAGE).c
            page["gfx_typed"], page["gfx_applied"] = None, graphics_text()
            page["fhues"] = (str(settings["field_hue"]), str(settings["para_hue"])); refresh()
        def _slider_value(s, default):
            try: v = s.Value
            except Exception: v = None
            if v is None:
                try: v = s.GetValue()
                except Exception: v = default
            try: return int(v)
            except Exception: return default
        def poll_config():
            c = page["c"]
            if c is None: return
            changed = False; rng = max(1, min(30, _slider_value(c["range"], settings["range"])))
            if rng != settings["range"]:
                settings["range"] = rng; Kit.set_text(c["range_lbl"], "%d tiles" % rng); changed = True
            cyc = max(5, min(100, _slider_value(c["cycle"], int(settings["cycle"] * 10)))) / 10.0
            if abs(cyc - settings["cycle"]) > 0.01:
                settings["cycle"] = cyc; Kit.set_text(c["cycle_v"], "%.1f s" % cyc); changed = True
            for key in ("green", "red"):
                v = Kit.read_int(c[key], settings[key])
                if 1 <= v <= HUE_MAX and v != settings[key]: settings[key] = v; changed = True
            hit = read_checks(c, settings, ("pulse", "by_name", "ping"))
            if "ping" in hit:
                st["ping_wait"] = [sr for sr in st["tracked"] if sr not in st["pinged"]] if settings["ping"] else []
            if hit: changed = True
            cur = st["paused"] if st["pause_want"] is None else st["pause_want"]
            try: pz = bool(c["paused"].IsChecked)
            except Exception: pz = cur
            if pz != cur: st["pause_want"] = pz
            try: say = bool(c["say"].IsChecked)
            except Exception: say = bool(st["say_graphics"])
            if say != st["say_graphics"]: st["say_graphics"] = say; save_view(); refresh()
            try: typed = str(c["graphics"].Text or "")
            except Exception: typed = str(graphics_text() or "")
            now = time.time()
            if typed != page["gfx_typed"]: page["gfx_typed"], page["gfx_since"] = typed, now
            elif now - page["gfx_since"] >= 0.7 and typed != page.get("gfx_applied"):
                page["gfx_applied"] = typed; gl = parse_graphics(typed)
                if gl and gl != settings["graphics"]: settings["graphics"] = gl; changed = True
            if changed: save_settings(); st["last_scan"] = 0.0; refresh()
            if poll_fields(c): save_fields(); st["last_scan"] = 0.0
        def poll_fields(c):
            changed = bool(read_checks(c, settings, ("fields", "field_say")))
            try: texts = (str(c["field_hue"].Text).strip(), str(c["para_hue"].Text).strip())
            except Exception: return changed
            if texts != page.get("fhues"):
                page["fhues"] = texts
                for key, t in zip(("field_hue", "para_hue"), texts):
                    if t.isdigit() and 0 <= int(t) <= HUE_MAX and int(t) != settings[key]:
                        settings[key] = int(t); changed = True
            return changed
        def config_closed(): page["c"] = None; page["gfx_typed"] = None
        def _start():
            st.update({"shutting": False, "docked": False, "queue": [], "last_scan": 0.0,
                       "scans": 0, "tracked": {}, "pinged": set(), "pinged_spots": set(),
                       "ping_wait": [], "ping_sent": 0, "ping_noted": False,
                       "ping_svc": ping_service(), "ping_next": 0.0, "fields": {}, "field_said": [], "alerted": set(),
                       "atlas_traps": [], "atlas_ver": 0, "atlas_done": -1, "atlas_map": None, "pause_want": None})
            verdicts.clear(); load_settings(); load_fields()
            safe(lambda: HOST.alert_kind(ALERT_TRAP, "New trap in range", 0x1EF)); load_view()
            if HOST.dock_wanted(KEY): st["minimized"] = True
            build_window(); HOST.dock_add(KEY, Kit.dock_hooks(TITLE, 0x113C, st, win, queue("redraw"), scale=True))
        def _tick():
            if win["g"] is None: return
            if Kit.was_clicked(win["store"], "close"): Kit.dispose(win["g"]); return
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
                if action == "ping_again": ping_again()
                else: Kit.win_action(action, st, KEY, TITLE, build_window)
            if st["paused"]: return
            now = time.time()
            if now - st["last_scan"] >= 1.0:
                st["last_scan"] = now; before = (len(st["tracked"]), len(st["fields"])); scan(); svc = ping_service()
                if (len(st["tracked"]), len(st["fields"])) != before or (svc is None) != (st["ping_svc"] is None):
                    st["ping_svc"] = svc
                    if svc is not None: st["ping_noted"] = False
                    refresh()
                if st["atlas_ver"] != st["atlas_done"]: st["atlas_done"] = st["atlas_ver"]; atlas_publish()
            send_pings(); pulse()
        def _stop():
            st["shutting"] = True; HOST.dock_remove(KEY); restore_all(); Kit.save_pos(POS_KEY, win["g"])
            save_settings(); g, win["g"] = win["g"], None; Kit.dispose(g)
        MODULE = {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True,
                  "config_height": lambda w: Kit.Form.height(PAGE, w), "build_config": build_config,
                  "poll_config": poll_config, "config_closed": config_closed}
        return MODULE
    PARTS = (("pings", _part_pings, 0.05, "pings"),
        ("corpse", lambda: with_atlas(_part_corpse(), "corpse"), 0.25, "corpserun"),
        ("maps", lambda: with_atlas(_part_maps(), "maps"), 0.2, "treasure"),
        ("dry", lambda: with_atlas(_part_dry(), "dry"), 0.2, "harvest"),
        ("traps", lambda: with_atlas(_part_traps(), "traps"), 0.1, "traphl"),)
    MODULE = PartSet(KEY, TITLE, PARTS).hooks(); _parts_tick, _parts_stop = MODULE["tick"], MODULE["stop"]
    _parts_thread, _parts_wanted = MODULE["thread_tick"], MODULE["thread_wanted"]; atlas_err = {"said": False}
    def _tick():
        _parts_tick()
        try: ATLAS.tick()
        except Exception as ex:
            if not atlas_err["said"]:
                atlas_err["said"] = True
                API.SysMsg("%s: couldn't update TazUO's World Map (%s)." % (TITLE, ex), Kit.HUE_BAD)
    def _stop():
        try: _parts_stop()
        finally: ATLAS.shutdown()
    def _thread():
        _parts_thread()
        try: ATLAS.thread_work()
        except Exception: ATLAS.strip_pending = False
    def _thread_wanted(): return bool(ATLAS.strip_pending or ATLAS.loose) or _parts_wanted()
    MODULE.update({"tick": _tick, "stop": _stop, "thread_tick": _thread, "thread_wanted": _thread_wanted})
    return MODULE


if "HOST" in globals() and hasattr(globals()["HOST"], "add"):
    HOST.add("worldmap", "World Map", "Guild pings, your corpse, dig spots, dry spots and traps",
             _module_worldmap, 0.05, category="The world", parts=(("pings", "Map Pings",
                  "Send and receive guild pings on your Enhanced Map", False, ("pings",)), ("corpse", "Corpse",
                  "An arrow to your corpse, its decay time, Get my things", False, ("corpserun",)),
                 ("maps", "Treasure Maps", "The dig spots of your decoded treasure maps", False, ("treasure",)),
                 ("dry", "Ore Tracker", "Your weight, and the ore, wood, fish and sand that ran dry", False,
                  ("harvest",)), ("traps", "Traps & Fields",
                  "Traps and magic fields recoloured so you see them", False, ("traphl",)),),
             aliases=('Map Pings', 'Corpse Run', 'Treasure Hunter', 'Harvest Helper', 'Dry spots',
                      'Ore Tracker', 'Trap Highlight', 'Enhanced Map', 'tracking arrow', 'ping',
                      'corpse', 'dig spot', 'weight bar', 'TazUO World Map'))
else:
    import API
    API.SysMsg("World Map is a Virtue Assistant module and can't run on its own. "
               "Run Virtue Assistant instead; it loads this file.", 33)
