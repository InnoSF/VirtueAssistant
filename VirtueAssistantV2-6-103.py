import API
import math
import os
import re
import struct
import time
APP_NAME = "Virtue Assistant"
APP_VERSION = "2.6.103"
MODULE_DIR = "VirtueAssistantModules"
SETTINGS_DIR = "VirtueAssistantSettings"
SETTINGS_KEY = "VirtueAssistant_settings"
VA_ALONE = "VA_ALONE" in globals()
ALIVE_KEY = "VirtueAssistant_alive"
ALONE_PARTS = "VirtueAssistant_alone_parts_%s"
HOST_TICK = 0.02
UI_TICK = 0.05
GRID_DEFAULT = 32
SNAP_ANCHOR = 40
KEEP_EVERY = 0.5
PROFILE_DIR = "VirtueAssistantProfiles"
PROFILE_STATE_KEY = "VirtueAssistant_profile"
PROFILE_NAME_MAX = 32
ALERT_RATE = 10.0
ALERT_HOLD = 8.0
ALERT_SOUND_GAP = 0.4
ALERT_FLASH = 0.5
ALERT_SOUNDS = (("Silent", 0), ("Chime", 0x1EA), ("Harp note", 0x3D0), ("Lever", 0x04A), ("Whistle", 0x335),
    ("Yell", 0x338), ("War drum", 0x2E7), ("Trap snap", 0x1EF), ("Boom", 0x307), ("Recall", 0x1FC),
    ("Heal tone", 0x202), ("Bird", 0x017), ("Smack", 0x3B2), ("Harm", 0x1F1), ("Cure", 0x1E0))
GUARD_IN_TEXTS = ("you are now under the protection of the town guards",)
GUARD_OUT_TEXTS = ("you have left the protection of the town guards",
                   "beware! you have left the protection of the town guards")
GUARD_AREAS = ()
GUARD_SPOT = 3
FOE_RANGE = 12
FOE_EVERY = 1.0
FOE_NOTO = (5, 6)
FOE_WAR_NOTO = (3, 4)
HURT_SECS = 10.0
HOLD_TEXT = {"dead": "you are dead", "war": "war mode", "hurt": "you took damage", "foe": "a hostile is near",
    "item": "you are moving an item", "alarm": "an alarm needs you", "guard": "guard zone",
    "unknown": "Guard zone not known yet: cross a town's guard line once",}
CATEGORY_ORDER = ("On screen", "Your things", "The world", "Skills and home", "Extras", "Other")
SEARCH_SETTLE = 0.3
WHATS_NEW_KEY = "VirtueAssistant_seen_version"


def whats_new():
    import sys; d = module_folders()
    if not d: return ()
    if d[0] not in sys.path: sys.path.insert(0, d[0])
    sys.modules.pop("_WhatsNew", None)
    try: import _WhatsNew; return tuple(_WhatsNew.WHATS_NEW)
    except Exception: return ()


class _Gumps(object):
    def __init__(self, inner): self._inner = inner
    def __getattr__(self, name): v = getattr(self._inner, name); self.__dict__[name] = v; return v
    def AddControlOnClick(self, ctrl, fn):
        def run(*args):
            try: fn(*args)
            finally: HOST.poke()
        self._inner.AddControlOnClick(ctrl, run)
    def AddGump(self, g):
        Kit.set(g, "CanCloseWithRightClick", False); Kit.set(Kit._raw_gump(g), "CanCloseWithRightClick", False)
        p = Kit._pend.get(g)
        if (p is not None and p[2] and p[3]) or g in Kit._scrolled: Kit.pin_size(g)
        r = self._inner.AddGump(g)
        try:
            SNAP.add(g)
            if LAYOUT.loaded: LAYOUT.fresh_adds.add(g)
        except Exception: pass
        return r


G = _Gumps(API.Gumps)


def safe(fn, default=None):
    try: return fn()
    except Exception: return default


class Client(object):
    looked = False; mouse = None; keys = {}; NO_CLICK_TIME = 1; _types = {}; _client_asm = False; TYPE_RETRY = 30.0
    @staticmethod
    def _type(name):
        hit = Client._types.get(name)
        if hit is not None:
            if type(hit) is not tuple: return hit
            if time.time() - hit[1] < Client.TYPE_RETRY: return None
        t = None
        try:
            if Client._client_asm is False:
                Client._client_asm = None
                try: Client._client_asm = API.GetType().Assembly
                except Exception: pass
            asm = Client._client_asm
            if asm is not None:
                try: t = asm.GetType(name, False)
                except Exception: t = None
            if t is None:
                import System
                for asm in System.AppDomain.CurrentDomain.GetAssemblies():
                    try: t = asm.GetType(name, False)
                    except Exception: t = None
                    if t is not None: break
        except Exception: t = None
        Client._types[name] = t if t is not None else (None, time.time()); return t
    @staticmethod
    def flags(static=False, public=True):
        from System.Reflection import BindingFlags
        return ((BindingFlags.Static if static else BindingFlags.Instance) | BindingFlags.NonPublic |
                (BindingFlags.Public if public else BindingFlags.Default))
    @staticmethod
    def _member(t, name):
        import System; flags = Client.flags(True); p = t.GetProperty(name, flags)
        if p is not None:
            return (lambda: p.GetValue(None, None),
                    lambda v: p.SetValue(None, System.Convert.ChangeType(v, p.PropertyType), None))
        f = t.GetField(name, flags)
        if f is not None:
            return (lambda: f.GetValue(None), lambda v: f.SetValue(None, System.Convert.ChangeType(v, f.FieldType)))
        return None
    @staticmethod
    def find():
        if Client.looked: return
        Client.looked = True; mouse = Client._type("ClassicUO.Input.Mouse")
        if mouse is not None:
            try: m = Client._member(mouse, "LastLeftButtonClickTime"); int(m[0]()); Client.mouse = m
            except Exception: Client.mouse = None
        kb = Client._type("ClassicUO.Input.Keyboard")
        if kb is not None:
            for key, name in (("alt", "Alt"), ("shift", "Shift"), ("ctrl", "Ctrl")):
                try: m = Client._member(kb, name); bool(m[0]()); Client.keys[key] = m[0]
                except Exception: pass
    @staticmethod
    def second_click_swallowed():
        Client.find()
        if Client.mouse is None: return False
        get, put = Client.mouse
        try: last = int(get()); put(Client.NO_CLICK_TIME); return last in (0, 0xFFFFFFFF)
        except Exception: return False
    @staticmethod
    def typing(): return bool(safe(Typing.now, False))
    @staticmethod
    def key_held(which):
        if not Client.looked: Client.find()
        fn = Client.keys.get(which)
        if fn is None: return None
        try: return bool(fn())
        except Exception: return False
    MTQ = None; mtq_looked = False; main_call = None
    @staticmethod
    def _find_mtq():
        if Client.mtq_looked: return Client.MTQ
        Client.mtq_looked = True
        try:
            import clr; clr.AddReference(API.GetType().Assembly); from ClassicUO.Game.Managers import MainThreadQueue
            Client.MTQ = MainThreadQueue
        except Exception: Client.MTQ = None
        return Client.MTQ
    @staticmethod
    def on_client_thread():
        MTQ = Client.MTQ if Client.mtq_looked else Client._find_mtq()
        if MTQ is None: return False
        try: return bool(MTQ.IsMainThread)
        except Exception: return False
    @staticmethod
    def _pick_main_call():
        from System import Func; MTQ = Client.MTQ; F = Func[object]
        def generic_of():
            inv = MTQ.InvokeOnMainThread[object]
            def generic(run): inv(F(run))
            return generic
        def inferred_of():
            def inferred(run): MTQ.InvokeOnMainThread(F(run))
            return inferred
        def with_event_of():
            from System import Action; from System.Threading import ManualResetEventSlim
            def with_event(run):
                done = ManualResetEventSlim(False)
                def wrapped():
                    try: run()
                    finally: done.Set()
                MTQ.EnqueueAction(Action(wrapped))
                if not done.Wait(5000): raise _HopTimeout("the client thread didn't answer in 5 s")
            return with_event
        for make in (generic_of, inferred_of, with_event_of):
            probe = {}
            def run_probe(): probe["ok"] = True
            try: candidate = make(); candidate(run_probe)
            except Exception: continue
            if probe.get("ok"): return candidate
        return None
    @staticmethod
    def on_main_ex(fn):
        Client.exc = None
        if (Client.MTQ if Client.mtq_looked else Client._find_mtq()) is None: return "no", None
        if Client.on_client_thread():
            try: return "ok", fn()
            except Exception as ex:
                Client.error = str(getattr(ex, "InnerException", None) or ex); Client.exc = ex
                return "err", Client.error
        call = Client.main_call
        if call is None:
            call = Client.main_call = Client._pick_main_call()
            if call is None: Client.error = "can't run on the client thread"; return "no", None
        hop = _Hop(fn)
        try: call(hop.run)
        except _HopTimeout as ex: Client.error = str(ex); return "err", Client.error
        except Exception as ex: Client.error = str(ex); return "no", None
        if hop.e is not None: Client.error, Client.exc = hop.e, hop.x; return "err", hop.e
        return "ok", hop.v
    error = ""; exc = None


class _HopTimeout(Exception): pass


class _Hop(object):
    __slots__ = ("fn", "v", "e", "x")
    def __init__(self, fn): self.fn, self.v, self.e, self.x = fn, None, None, None
    def run(self):
        try: self.v = self.fn()
        except Exception as ex: self.e = str(getattr(ex, "InnerException", None) or ex); self.x = ex
        except: self.e = "unknown error"


class Typing(object):
    looked = False; uim = None; prof = None; _members = {}; _flags = None; _prof_t = None; _chat_t = None
    _now_pid = -1; _now_val = False
    @staticmethod
    def _find():
        if Typing.looked: return
        Typing.looked = True; Typing.uim = Client._type("ClassicUO.Game.Managers.UIManager")
        Typing.prof = Client._type("ClassicUO.Configuration.ProfileManager")
    @staticmethod
    def _lookup(t, name, static):
        if Typing._flags is None:
            from System.Reflection import BindingFlags
            base = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly
            Typing._flags = (base | BindingFlags.Instance, base | BindingFlags.Static)
        flags = Typing._flags[1 if static else 0]; m, prop, tt = None, False, t
        while tt is not None and m is None:
            try: m = tt.GetProperty(name, flags)
            except Exception: m = None
            if m is not None: prop = True
            else: m = tt.GetField(name, flags)
            tt = tt.BaseType
        if m is None and not static:
            for it in t.GetInterfaces():
                m = it.GetProperty(name)
                if m is not None: prop = True; break
        return (m, prop) if m is not None else None
    @staticmethod
    def _get(obj, name, t=None, default=None):
        try:
            static = obj is None
            if t is None: t = obj.GetType()
            ck = (t, name, static); m = Typing._members.get(ck, False)
            if m is False: m = Typing._members[ck] = Typing._lookup(t, name, static)
            if m is None: return default
            if m[1]: return m[0].GetValue(obj, None)
            return m[0].GetValue(obj)
        except Exception: return default
    @staticmethod
    def _same(a, b): return a is not None and b is not None and bool(Kit._same()(a, b))
    @staticmethod
    def _ptype(cur):
        t = Typing._prof_t
        if t is None:
            try: t = Typing._prof_t = cur.GetType()
            except Exception: t = None
        return t
    @staticmethod
    def now():
        try: h = HOST; pid = h.pass_id if h.in_hop else None
        except Exception: pid = None
        if pid is not None and Typing._now_pid == pid: return Typing._now_val
        v = Typing._now()
        if pid is not None: Typing._now_pid = pid; Typing._now_val = v
        return v
    @staticmethod
    def _now():
        Typing._find(); uim = Typing.uim
        if uim is None: return False
        focus = Typing._get(None, "KeyboardFocusControl", uim); chat = Typing._get(None, "SystemChat", uim)
        chat_tb = None
        if chat is not None:
            ct = Typing._chat_t
            if ct is None:
                try: ct = Typing._chat_t = chat.GetType()
                except Exception: ct = None
            chat_tb = Typing._get(chat, "TextBoxControl", ct)
        if focus is not None and not Typing._same(focus, chat_tb) \
                and not bool(Typing._get(focus, "IsDisposed", default=False)) \
                and bool(Typing._get(focus, "IsVisible", default=True)) \
                and bool(Typing._get(focus, "AcceptKeyboardInput", default=True)):
            return True
        if chat is None: return False
        after_enter = True
        if Typing.prof is not None:
            cur = Typing._get(None, "CurrentProfile", Typing.prof)
            if cur is not None:
                v = Typing._get(cur, "ActivateChatAfterEnter", Typing._ptype(cur))
                after_enter = True if v is None else bool(v)
        if after_enter and bool(Typing._get(chat, "IsActive", Typing._chat_t, default=False)): return True
        text = Typing._get(chat_tb, "Text") if chat_tb is not None else None
        return text is not None and len(str(text)) > 0
    @staticmethod
    def release():
        Typing._now_pid = -1
        def run():
            Typing._find(); uim = Typing.uim
            if uim is None: return
            try:
                m = uim.GetMethod("RestoreSystemChatFocus", Client.flags(True))
                if m is not None: m.Invoke(None, None); return
            except Exception: pass
            chat = Typing._get(None, "SystemChat", uim)
            tb = Typing._get(chat, "TextBoxControl") if chat is not None else None
            if tb is not None: safe(lambda: tb.SetKeyboardFocus())
        if Client.on_client_thread(): safe(run)
        else: Client.on_main_ex(run)


class Follow(object):
    serial = None; readers = None; ALT_NAMES = ("ALT", "LALT", "RALT", "LEFTALT", "RIGHTALT", "MENU", "LMENU", "RMENU")
    SDL_ALT = 0x0300
    @staticmethod
    def _find():
        if Follow.readers is not None: return
        r = []
        try:
            import clr
            for asm in ("ClassicUO", "ClassicUO.Client", "TazUO", "FNA", "SDL2-CS", "SDL3-CS"):
                safe(lambda: clr.AddReference(asm))
        except Exception: pass
        Client.find()
        if "alt" in Client.keys: r.append(lambda: Client.key_held("alt"))
        try: from ClassicUO.Input import Keyboard; bool(Keyboard.Alt); r.append(lambda: bool(Keyboard.Alt))
        except Exception: pass
        for modname in ("SDL2", "SDL3"):
            try:
                sdl = __import__(modname).SDL; int(sdl.SDL_GetModState())
                r.append(lambda sdl=sdl: (int(sdl.SDL_GetModState()) & Follow.SDL_ALT) != 0)
            except Exception: pass
        Follow.readers = r
    @staticmethod
    def alt_held():
        Follow._find()
        for fn in Follow.readers:
            if safe(fn, False): return True
        if Follow.readers: return False
        for k in Follow.ALT_NAMES:
            if safe(lambda: API.IsKeyPressed(k), False): return True
        return False
    _pid = -1; _val = None
    @staticmethod
    def current():
        try: h = HOST; pid = h.pass_id if h.in_hop else None
        except Exception: pid = None
        if pid is not None and Follow._pid == pid: return Follow._val
        v = Follow._current()
        if pid is not None: Follow._pid = pid; Follow._val = v
        return v
    @staticmethod
    def _current():
        Typing._find(); cur = Typing._get(None, "CurrentProfile", Typing.prof) if Typing.prof is not None else None
        if cur is not None:
            pt = Typing._ptype(cur); mode = Typing._get(cur, "FollowingMode", pt)
            if mode is not None:
                if not bool(mode): Follow.serial = None; return None
                t = Typing._get(cur, "FollowingTarget", pt)
                if t is not None:
                    try: Follow.serial = int(t) or None
                    except Exception: pass
                return Follow.serial
        if Follow.serial is not None and API.FindMobile(Follow.serial) is None: Follow.serial = None
        return Follow.serial
    @staticmethod
    def start(serial, who=APP_NAME):
        serial = int(serial or 0)
        if not serial: return False
        me = int(safe(lambda: API.Player.Serial, 0) or 0)
        if serial == me: API.SysMsg("%s: you can't follow yourself." % who, Kit.HUE_INFO); return False
        if API.FindMobile(serial) is None:
            API.SysMsg("%s: can't follow them, they are out of sight." % who, Kit.HUE_BAD); return False
        try: API.AutoFollow(serial)
        except Exception as ex: API.SysMsg("%s: couldn't auto-follow (%s)." % (who, ex), Kit.HUE_BAD); return False
        Follow.serial = serial; Follow._pid = -1; API.HeadMsg("* following *", serial, 0x44); return True
    @staticmethod
    def stop(who=APP_NAME):
        s = Follow.serial; Follow._pid = -1; API.CancelAutoFollow(); Follow.serial = None
        if s: API.HeadMsg("* stopped following *", s, 0x35)
    @staticmethod
    def toggle(serial, who=APP_NAME):
        serial = int(serial or 0)
        if serial and Follow.current() == serial: Follow.stop(who); return False
        return Follow.start(serial, who)


class Kit(object):
    WINDOW_BG     = 5054; STONE_TILE    = 5058; SECTION_TILE  = 2624; SECTION_ALPHA = 0.8; FIELD_TILE    = 2624
    CORNER_ART    = 10460; ART_PLAY    = (4005, 4007, 4006); ART_CLOSE   = (4017, 4019, 4018)
    ART_OK      = (4023, 4025, 4024); ART_PAGE    = (4011, 4013, 4012); ART_MIN     = (253, 252, 253)
    ART_RESTORE = (251, 250, 251); ART_DOCK    = (5602, 5606, 5602); ART_CIRCLE  = (2117, 2118, 2118)
    DOCK_DX, DOCK_DY = 20, 2; DOCK_TIP = "Fold into the Action Bar's tray"
    MIN_TIP = "Minimize (or double-click the title)"; RESTORE_TIP = "Restore"
    SETTINGS_TIP = "Open %s settings"; CLOSE_TIP = "Close %s (turns it off)"
    DOUBLE_TIP = "Double-click: minimize or restore"; LINE_RED, LINE_BLUE, LINE_POISON = 0x0805, 0x0806, 0x0808
    HUE_TITLE = 53; HUE_TEXT  = 1153; HUE_GOOD  = 68; HUE_BAD   = 33; HUE_INFO  = 946; MARGIN = 12; GAP    = 8
    _sizes = {}
    @staticmethod
    def on_client(fn, fallback=True):
        how, v = Client.on_main_ex(fn)
        if how == "ok": return v
        if how == "err": raise Client.exc if isinstance(Client.exc, Exception) else Exception(Client.error)
        return fn() if fallback else None
    _screen = {"wh": (0, 0), "at": 0.0}
    @staticmethod
    def screen():
        now = time.time()
        if now - Kit._screen["at"] >= 1.0:
            Kit._screen["at"] = now
            try: b = API.GetClientBounds(); wh = (int(b.Width), int(b.Height))
            except Exception: wh = None
            if wh and wh[0] > 0 and wh[1] > 0:
                s = Kit.render_scale()
                if abs(s - 1.0) > 0.001: wh = (int(round(wh[0] / s)), int(round(wh[1] / s)))
                Kit._screen["wh"] = wh
        return Kit._screen["wh"]
    _scale = {"fn": None, "looked": False}
    @staticmethod
    def render_scale():
        st = Kit._scale
        if not st["looked"]:
            st["looked"] = True
            try:
                t = Client._type("ClassicUO.Client"); gp = t.GetProperty("Game", Client.flags(True))
                game = gp.GetValue(None, None); rp = game.GetType().GetProperty("RenderScale", Client.flags())
                float(rp.GetValue(game, None)); st["fn"] = lambda: float(rp.GetValue(gp.GetValue(None, None), None))
            except Exception: st["fn"] = None
        fn = st["fn"]
        if fn is None: return 1.0
        try: s = fn(); return s if 0.25 <= s <= 4.0 else 1.0
        except Exception: return 1.0
    ANCHORS = ("TL", "T", "TR", "L", "C", "R", "BL", "B", "BR"); SCREEN_KEY = "VirtueAssistant_screen"
    _pos_screen = None
    @staticmethod
    def clamp(x, y, w, h):
        W, H = Kit.screen(); x, y, w, h = int(x or 0), int(y or 0), int(w or 0), int(h or 0)
        if W > 0: x = max(0, min(x, W - w)) if w <= W else max(W - w, min(x, 0))
        if H > 0: y = max(0, min(y, H - h)) if h <= H else max(H - h, min(y, 0))
        return x, y
    _frame_parts = {}; _pend = {}; PEND_FOR = 1.0
    @staticmethod
    def note_rect(g, x, y, w=None, h=None):
        if g is None: return
        try:
            r = None
            if Kit._pend: r = Kit.rect(g)
            old = Kit._pend.get(g)
            if w is None and old is not None: w, h = old[2], old[3]
            if old is not None: was = old[5]
            elif r is not None: was = r
            else: was = (int(g.GetX()), int(g.GetY()), int(g.GetWidth() or 0), int(g.GetHeight() or 0))
            Kit._pend[g] = (int(x), int(y), None if w is None else int(w),
                            None if h is None else int(h), time.time(), was)
        except Exception: pass
    @staticmethod
    def rect(g):
        try: x, y = int(g.GetX()), int(g.GetY()); w, h = int(g.GetWidth() or 0), int(g.GetHeight() or 0)
        except Exception: return None
        pend = Kit._pend
        if pend:
            p = pend.get(g)
            if p is not None:
                pw = w if p[2] is None else p[2]; ph = h if p[3] is None else p[3]
                if (x, y, w, h) == (p[0], p[1], pw, ph) or (x, y, w, h) != p[5] or time.time() - p[4] > Kit.PEND_FOR:
                    del pend[g]
                else: return p[0], p[1], pw, ph
        return x, y, w, h
    @staticmethod
    def pos(g):
        if Kit._pend and g in Kit._pend: r = Kit.rect(g); return None if r is None else (r[0], r[1])
        try: return int(g.GetX()), int(g.GetY())
        except Exception: return None
    @staticmethod
    def prune_pending():
        if len(Kit._pinned) > 400: Kit._pinned = set(g for g in Kit._pinned if Kit.is_open(g))
        if not Kit._pend: return
        now = time.time()
        for g in [g for g, p in Kit._pend.items() if now - p[4] > Kit.PEND_FOR]: Kit._pend.pop(g, None)
    @staticmethod
    def place(g, x, y, w, h, head=None, max_h=None):
        rec = Fill.recs.get(g) if Fill.recs else None
        if rec is not None and rec["slot"] is not None:
            rec["nat"], rec["size"] = (int(w or 0), int(h or 0)), None; sx, sy, sw, sh = rec["slot"]
            if Kit.on_client(lambda: Fill.fit(g, sx, sy, sw, sh, rec["mode"]), fallback=False) is not None:
                return sx, sy
            Fill.recs.pop(g, None)
        return Kit._place_raw(g, x, y, w, h, head, max_h)
    @staticmethod
    def _place_raw(g, x, y, w, h, head=None, max_h=None):
        w, h = int(w or 0), int(h or 0); H = Kit.screen()[1]; limit = H if not max_h else min(H, int(max_h))
        if limit > 0 and (h > limit or g in Kit._scrolled):
            fit = Kit.scroll_fit(g, w, h, head, int(max_h) if max_h else None)
            if fit is not None: w, h = fit
        x, y = Kit.clamp(x, y, w, h); g.SetRect(x, y, w, h); Kit.note_rect(g, x, y, w, h)
        if g not in Kit._pinned: Kit.pin_size(g)
        return x, y
    _pinned = set()
    @staticmethod
    def pin_size(g, raw=None):
        try:
            raw = raw if raw is not None else Kit._raw_gump(g)
            if raw is None: return False
            if raw.WantUpdateSize: raw.WantUpdateSize = False
            Kit._pinned.add(g); return True
        except Exception: return False
    SCROLL_BAND = 15; _frames = {}; _scrolled = {}; scroll_info = _scrolled.get; _rawmode = {}
    @staticmethod
    def scroll_fit(g, w, h, head=None, limit=None):
        try:
            H = Kit.screen()[1]
            if limit: H = min(H, int(limit))
            info = Kit._scrolled.get(g)
            if info is not None and info["w"] == w and info["h"] == h and info["H"] == H: return info["w2"], info["hv"]
            if head is None: head = info["head"] if info is not None else Kit.MARGIN + 30 + Kit.GAP
            out = Kit.on_client(lambda: Kit._scroll_build(g, w, h, int(head), H), fallback=False)
            if out is not None: Kit._scrolled[g]["lim"] = int(limit) if limit else None
            return out
        except Exception: return None
    @staticmethod
    def _raw_rect(c):
        mode = Kit._rawmode
        try: loc = c.Location; x, y = int(loc.X), int(loc.Y)
        except Exception: return None
        how = mode.get("how")
        if how != "reflect":
            try: w, h = int(c.Width), int(c.Height); mode["how"] = "direct"; return x, y, w, h
            except Exception: mode["how"] = "reflect"
        try:
            t = c.GetType(); pw = t.GetProperty("Width"); ph = t.GetProperty("Height")
            return x, y, int(pw.GetValue(c, None)), int(ph.GetValue(c, None))
        except Exception: return None
    @staticmethod
    def _raw_gump(g):
        try:
            raw = g.Gump
            if raw is not None: return raw
        except Exception: pass
        return Kit.client_control(g)
    @staticmethod
    def _children(raw): kids = raw.Children; return [kids[i] for i in range(int(kids.Count))]
    @staticmethod
    def _scroll_build(g, w, h, head, H):
        M = Kit.MARGIN
        if not Kit.flush(): return None
        raw = Kit._raw_gump(g)
        if raw is None: return None
        hv = min(h, H); head = max(0, min(head, hv - M - 40)); w2 = w + Kit.SCROLL_BAND; area_w = w - M + 14
        area_h = hv - M; info = Kit._scrolled.get(g)
        if info is not None: return Kit._scroll_refit(g, info, raw, w, h, H, hv, w2, area_w, area_h, head)
        fr = Kit._frames.get(g); corners = fr["corners"] if fr else True; mouse = fr["mouse"] if fr else True
        old_frame = list(fr["pieces"]) if fr else []; kids, content, header, fixed = [], [], [], []
        skip = [pr for pr in map(Kit.client_control, old_frame) if pr is not None]; same = Kit._same()
        for c in Kit._children(raw):
            try:
                if c.IsDisposed: continue
            except Exception: continue
            if any(same(c, s) for s in skip): continue
            r = Kit._raw_rect(c)
            if r is None: return None
            kids.append(c); cy, ch = r[1], r[3]
            if cy <= 0 and ch >= h - 2: fixed.append(c)
            elif cy < head: header.append(c)
            else: content.append(c)
        Kit._frames.pop(g, None)
        for p in old_frame: Kit.dispose(p)
        frame = area = band = None
        try:
            area = G.CreateGumpScrollArea(0, 0, area_w, area_h); frame = Kit._scroll_frame(g, w2, hv, corners, mouse)
            if not Kit.flush(): raise Exception("queue")
            for c in fixed: c.Parent = raw
            g.Add(area)
            if not Kit.flush(): raise Exception("queue")
            area_raw = Kit.client_control(area)
            if area_raw is None: raise Exception("no area")
            for c in content: c.Parent = area_raw
            band = Kit._scroll_band(g, w, w2, hv, head, corners, mouse)
            if not Kit.flush(): raise Exception("queue")
            for c in header: c.Parent = raw
        except Exception: Kit._scroll_undo(g, raw, w, h, corners, mouse, kids, frame, area, band); return None
        Kit._scroll_note(g, raw, w, h, H, w2, hv, head, area, area_raw, frame, band, header, fixed, corners, mouse)
        return w2, hv
    @staticmethod
    def _scroll_refit(g, info, raw, w, h, H, hv, w2, area_w, area_h, head):
        frame = area = band = None; moved = False
        try:
            for p in info["frame"] + info["band"]: Kit.dispose(p)
            old_area, old_raw = info["area"], info["area_raw"]; header = [c for c in info["header"] if not c.IsDisposed]
            fixed = [c for c in info["fixed"] if not c.IsDisposed]; corners, mouse = info["corners"], info["mouse"]
            frame = Kit._scroll_frame(g, w2, hv, corners, mouse)
            if not Kit.flush(): raise Exception("queue")
            for c in fixed: c.Parent = raw
            area = G.CreateGumpScrollArea(0, 0, area_w, area_h); g.Add(area)
            if not Kit.flush(): raise Exception("queue")
            area_raw = Kit.client_control(area)
            if area_raw is None: raise Exception("no area")
            kids = Kit._children(old_raw)
            for c in kids[1:]:
                try:
                    if not c.IsDisposed: c.Parent = area_raw
                except Exception: pass
            Kit.dispose(old_area); moved = True; band = Kit._scroll_band(g, w, w2, hv, head, corners, mouse)
            if not Kit.flush(): raise Exception("queue")
            for c in header: c.Parent = raw
        except Exception:
            if moved: info.update(area=area, area_raw=area_raw)
            else: Kit.dispose(area)
            info.update(frame=frame or [], band=band or [], known=None, skip_raw=None); return None
        Kit._scroll_note(g, raw, w, h, H, w2, hv, head, area, area_raw, frame, band, header, fixed, corners, mouse)
        return w2, hv
    @staticmethod
    def _scroll_frame(g, w2, hv, corners, mouse):
        return Kit._add_corners(g, Kit._frame_pieces(g, w2, hv, False, mouse), w2, hv, corners, mouse)
    @staticmethod
    def _add_corners(g, out, right, hv, corners, mouse):
        cw, ch = Kit.pic_size(Kit.CORNER_ART) if corners and Kit.CORNER_ART else (0, 0)
        if cw and ch:
            for cy in (0, hv - ch):
                p = Kit.add_pic(g, Kit.CORNER_ART, 0 if right is None else right - cw, cy, mouse=mouse)
                if p is not None: out.append(p); Kit._note_frame_part(g, p)
        return out
    @staticmethod
    def _scroll_band(g, w, w2, hv, head, corners, mouse):
        M = Kit.MARGIN; band = []; bl = Kit.pic_size(Kit.WINDOW_BG + 3)[0] or M
        bt = Kit.pic_size(Kit.WINDOW_BG + 1)[1] or M
        t = Kit.add_tiled(g, Kit.STONE_TILE, bl, bt, w - M - bl, head - bt)
        if t is not None:
            t.SetAcceptMouseInput(True); t.CanMove = True; band.append(t)
        return Kit._add_corners(g, band, None, hv, corners, mouse)
    @staticmethod
    def _note_frame_part(g, p):
        parts = Kit._frame_parts.get(g)
        if parts is not None: parts.append(p)
    @staticmethod
    def _scroll_note(g, raw, w, h, H, w2, hv, head, area, area_raw, frame, band, header, fixed, corners, mouse):
        Kit._scrolled[g] = {"w": w, "h": h, "H": H, "w2": w2, "hv": hv, "head": head, "raw": raw, "area": area,
                            "area_raw": area_raw, "frame": frame, "band": band, "header": header, "fixed": fixed,
                            "n": Kit._live_count(raw), "corners": corners, "mouse": mouse}
        Kit._prune(Kit._scrolled)
    @staticmethod
    def _scroll_undo(g, raw, w, h, corners, mouse, kids, frame, area, band):
        for p in (frame or []) + (band or []): Kit.dispose(p)
        Kit.dispose(area)
        with Kit.quiet:
            pieces = Kit._frame_pieces(g, w, h, corners, mouse)
            Kit._frames[g] = {"pieces": pieces, "corners": corners, "mouse": mouse}; Kit.flush()
            for c in kids: c.Parent = raw
    @staticmethod
    def _live_count(raw):
        n = 0
        try:
            kids = raw.Children
            for i in range(int(kids.Count)):
                if not kids[i].IsDisposed: n += 1
        except Exception: return -1
        return n
    _same_fn = None
    @staticmethod
    def _same():
        fn = Kit._same_fn
        if fn is not None: return fn
        try: import System; fn = System.Object.ReferenceEquals
        except Exception: fn = lambda a, b: a is b
        Kit._same_fn = fn; return fn
    @staticmethod
    def scroll_sweep():
        if not Kit._scrolled: return
        gone, stalled = [], False; H = Kit.screen()[1]
        for g, info in list(Kit._scrolled.items()):
            if not Kit.is_open(g): gone.append(g); continue
            raw = info["raw"]; lim = info.get("lim"); want = min(H, lim) if lim else H
            if H > 0 and info["H"] != want:
                try:
                    fit = Kit._scroll_build(g, info["w"], info["h"], info["head"], want)
                    if fit is not None:
                        info = Kit._scrolled.get(g) or info; info["lim"] = lim
                        x, y = Kit.clamp(int(g.GetX()), int(g.GetY()), fit[0], fit[1]); g.SetRect(x, y, fit[0], fit[1])
                        Kit.moved_by_code(g)
                except Exception: pass
                continue
            try: cnt = int(raw.Children.Count)
            except Exception: cnt = -1
            now = time.time()
            if cnt >= 0 and cnt == info.get("cnt") and 0 <= info.get("full_at", 0.0) - now: continue
            info["cnt"] = cnt; info["full_at"] = now + Kit.SWEEP_FULL; n = Kit._live_count(raw)
            if n < 0 or n == info["n"]: continue
            if stalled or not Kit.flush(): info["cnt"], stalled = None, True; continue
            try: kids = Kit._children(raw)
            except Exception: info["cnt"] = None; continue
            known = info.get("known")
            if known is None:
                known = info["known"] = set([info["area_raw"]] + info["header"] + info["fixed"] + [
                    kr for kr in map(Kit.client_control, info["frame"] + info["band"]) if kr is not None])
            for c in kids:
                try:
                    if c.IsDisposed or c in known: continue
                except Exception: continue
                r = Kit._raw_rect(c)
                if r is None: continue
                if r[1] < info["head"]: info["header"].append(c); known.add(c)
                else:
                    try: c.Parent = info["area_raw"]
                    except Exception: pass
            info["n"] = Kit._live_count(raw)
            try: info["cnt"] = int(raw.Children.Count)
            except Exception: info["cnt"] = -1
        for g in gone: Kit._scrolled.pop(g, None); Kit._frames.pop(g, None)
    @staticmethod
    def attach(follower, leader): SNAP.attach(follower, leader)
    @staticmethod
    def detach(follower): SNAP.detach(follower)
    @staticmethod
    def no_snap(g): SNAP.exempt(g)
    @staticmethod
    def anchor_pos(name, w, h):
        W, H = Kit.screen()
        if W <= 0 or H <= 0 or not name: return None, None
        col = "L" if "L" in name else "R" if "R" in name else "C"
        row = "T" if "T" in name else "B" if "B" in name else "C"
        x = 0 if col == "L" else max(0, W - w) if col == "R" else max(0, (W - w) // 2)
        y = 0 if row == "T" else max(0, H - h) if row == "B" else max(0, (H - h) // 2); return x, y
    @staticmethod
    def anchor_at(x, y, w, h, slack=2):
        W, H = Kit.screen()
        if W <= 0 or H <= 0: return ""
        col = "L" if abs(x) <= slack else "R" if abs(x + w - W) <= slack else \
            "C" if abs(x - (W - w) // 2) <= slack else None
        row = "T" if abs(y) <= slack else "B" if abs(y + h - H) <= slack else \
            "C" if abs(y - (H - h) // 2) <= slack else None
        if col is None or row is None: return ""
        return (row + col).replace("C", "") or "C"
    @staticmethod
    def anchor_targets(w, h):
        W, H = Kit.screen()
        if W <= 0 or H <= 0: return []
        return [Kit.anchor_pos(n, w, h) for n in Kit.ANCHORS]
    @staticmethod
    def remap_axis(p, s, S, S2):
        p, s, S, S2 = int(p), int(s or 0), int(S), int(S2)
        if S <= 0 or S2 <= 0 or S == S2: return p
        if p == 0: return 0
        if p == S - s: return S2 - s
        if p == (S - s) // 2: return (S2 - s) // 2
        c = p + s / 2.0
        if c < S / 3.0: return p
        if c > 2 * S / 3.0: return S2 - (S - p)
        return p + (S2 - S) // 2
    @staticmethod
    def adapt(x, y, w=0, h=0):
        W, H = Kit.screen(); old = Kit._pos_screen; x, y = int(x), int(y)
        if old is not None and W > 0 and H > 0 and (W, H) != old:
            x = Kit.remap_axis(x, w, old[0], W); y = Kit.remap_axis(y, h, old[1], H)
        if w and h: x, y = Kit.clamp(x, y, w, h)
        return x, y
    @staticmethod
    def read_screen():
        try: w, h = Kit.get_var(Kit.SCREEN_KEY).split(","); Kit._pos_screen = (int(w), int(h))
        except Exception: Kit._pos_screen = None
    @staticmethod
    def note_screen(wh=None):
        wh = wh or Kit.screen()
        if wh and wh[0] > 0 and wh[1] > 0 and wh != Kit._pos_screen:
            Kit._pos_screen = wh; Kit.put_var(Kit.SCREEN_KEY, "%d,%d" % wh)
    @staticmethod
    def pic_size(graphic):
        wh = Kit._sizes.get(graphic)
        if wh is None:
            w = h = 0
            try: p = G.CreateGumpPic(graphic); w, h = int(p.GetWidth() or 0), int(p.GetHeight() or 0); Kit.dispose(p)
            except Exception: pass
            wh = Kit._sizes[graphic] = (w, h)
        return wh
    @staticmethod
    def add_pic(g, graphic, x, y, hue=0, mouse=True):
        try:
            p = G.CreateGumpPic(graphic, x, y, hue) if hue else G.CreateGumpPic(graphic, x, y); p.SetPos(x, y)
            if not mouse: p.SetAcceptMouseInput(False)
            g.Add(p); return p
        except Exception: return None
    @staticmethod
    def add_tiled(g, graphic, x, y, w, h, alpha=None, fallback="#101010", hue=0):
        if w <= 0 or h <= 0: return None
        try: t = (G.CreateTiledGumpPic(graphic, w, h, hue) if hue else G.CreateTiledGumpPic(graphic, w, h))
        except Exception: t = G.CreateGumpColorBox(alpha if alpha is not None else 1.0, fallback)
        t.SetRect(x, y, w, h)
        if alpha is not None: t.SetAlpha(alpha)
        t.SetAcceptMouseInput(False); g.Add(t); return t
    @staticmethod
    def add_box(g, x, y, w, h, alpha=0.5, color="#FFFFFF"):
        if w <= 0 or h <= 0: return None
        b = G.CreateGumpColorBox(alpha, color); b.SetRect(x, y, w, h); b.SetAcceptMouseInput(False); g.Add(b); return b
    @staticmethod
    def add_resizepic(g, base, x, y, w, h, mouse=True):
        s = Kit._rp_sizes.get(base)
        if s is None:
            s = [Kit.pic_size(base + i) for i in range(9)]
            if not all(p[0] > 0 and p[1] > 0 for p in s): return [Kit.add_tiled(g, base + 4, x, y, w, h)]
            Kit._rp_sizes[base] = s
        tl, t, tr, l, c, r, bl, b, br = s
        out = [Kit.add_tiled(g, base + 4, x + l[0], y + t[1], w - l[0] - r[0], h - t[1] - b[1]),
            Kit.add_tiled(g, base + 1, x + tl[0], y, w - tl[0] - tr[0], t[1]),
            Kit.add_tiled(g, base + 7, x + bl[0], y + h - b[1], w - bl[0] - br[0], b[1]),
            Kit.add_tiled(g, base + 3, x, y + tl[1], l[0], h - tl[1] - bl[1]),
            Kit.add_tiled(g, base + 5, x + w - r[0], y + tr[1], r[0], h - tr[1] - br[1]),
            Kit.add_pic(g, base + 0, x, y, mouse=mouse), Kit.add_pic(g, base + 2, x + w - tr[0], y, mouse=mouse),
            Kit.add_pic(g, base + 6, x, y + h - bl[1], mouse=mouse),
            Kit.add_pic(g, base + 8, x + w - br[0], y + h - br[1], mouse=mouse)]
        return [p for p in out if p is not None]
    @staticmethod
    def _frame_pieces(g, w, h, corners=True, mouse=True):
        out = Kit.add_resizepic(g, Kit.WINDOW_BG, 0, 0, w, h, mouse)
        if corners and Kit.CORNER_ART:
            cw, ch = Kit.pic_size(Kit.CORNER_ART)
            if cw and ch:
                for cx, cy in ((0, 0), (w - cw, 0), (0, h - ch), (w - cw, h - ch)):
                    p = Kit.add_pic(g, Kit.CORNER_ART, cx, cy, mouse=mouse)
                    if p is not None: out.append(p)
        if type(g) is not PageCanvas:
            try: Kit._prune(Kit._frame_parts); Kit._frame_parts[g] = [p for p in out if p is not None]
            except TypeError: pass
        return out
    @staticmethod
    def add_window_frame(g, w, h, corners=True, mouse=True):
        pieces = Kit._frame_pieces(g, w, h, corners, mouse)
        if type(g) is not PageCanvas:
            Kit._prune(Kit._frames, 32)
            if len(Kit._frames) > 48: Kit._frames.clear()
            Kit._frames[g] = {"pieces": pieces, "corners": corners, "mouse": mouse}
    @staticmethod
    def add_section(g, x, y, w, h, title=None, alpha=None):
        if type(g) is PageCanvas: g.sections.append((x, y, w, h))
        t = Kit.add_tiled(g, Kit.SECTION_TILE, x, y, w, h, Kit.SECTION_ALPHA if alpha is None else alpha)
        if title: Kit.add_label(g, title, x + 8, y + 6, Kit.HUE_TITLE)
        return t
    @staticmethod
    def add_label(g, text, x, y, hue=None):
        lbl = G.CreateGumpLabel(text, Kit.HUE_TEXT if hue is None else hue); lbl.SetPos(x, y); g.Add(lbl); return lbl
    @staticmethod
    def add_check(g, text, x, y, checked=False, tooltip=None):
        cb = G.CreateGumpCheckbox(text, Kit.HUE_TEXT, checked); cb.SetPos(x, y); Kit.with_tip(cb, tooltip); g.Add(cb)
        return cb
    @staticmethod
    def add_textbox(g, text, x, y, w=60, numbers=True, font=16):
        Kit.add_tiled(g, Kit.FIELD_TILE, x - 2, y - 1, w + 4, 24); tb = G.CreateGumpTextBox(text, w, 22, False, font)
        tb.SetPos(x, y)
        if numbers: tb.NumbersOnly = True
        g.Add(tb); return tb
    @staticmethod
    def add_slider(g, x, y, w, lo, hi, value): s = G.CreateSlider(w, lo, hi, int(value), x, y, True); g.Add(s); return s
    clicks_seen = False
    @staticmethod
    def on_click(ctrl, fn):
        def handler(*args):
            Kit.clicks_seen = True; twice = Client.second_click_swallowed()
            try: fn()
            finally:
                try:
                    if twice: fn()
                finally: HOST.poke()
        G.AddControlOnClick(ctrl, handler)
    _dbl = {}; pending = []; _fired = {}
    @staticmethod
    def _prune(d, cap=64):
        if len(d) > cap:
            for k in [k for k in d if not Kit.is_open(k)]: d.pop(k, None)
    @staticmethod
    def _forget_old(d, now, age=5.0):
        if len(d) > 64:
            for k in [k for k, v in d.items() if now - (v[0] if type(v) is tuple else v) > age]: d.pop(k, None)
    @staticmethod
    def once(fn, key):
        def run():
            now = time.time()
            if now - Kit._fired.get(key, 0.0) < 0.6: return
            Kit._fired[key] = now; Kit._forget_old(Kit._fired, now); fn()
        return run
    @staticmethod
    def hook_mouse(api_ctrl, fn, queue=True, event="MouseDoubleClick", button="Left"):
        try:
            import clr; import System; ctrl = Kit.client_control(api_ctrl); t0 = ctrl.GetType()
            name = (str(t0.FullName), event); found = Kit._dbl_events.get(name)
            if found is None:
                flags = Client.flags(); t, ev = t0, None
                while t is not None and ev is None: ev = t.GetEvent(event, flags); t = t.BaseType
                found = (ev, clr.GetPythonType(ev.EventHandlerType), ev.GetAddMethod(True))
                if len(Kit._dbl_events) > 64: Kit._dbl_events.clear()
                Kit._dbl_events[name] = found
            ev, delegate_type, add = found
            def handler(sender, e):
                try:
                    if str(e.Button) == button:
                        if queue: Kit.pending.append(fn)
                        else: fn()
                        e.Result = True; HOST.poke()
                except Exception: pass
            add.Invoke(ctrl, System.Array[object]([delegate_type(handler)])); return True
        except Exception: return False
    hook_double = hook_mouse; _dbl_events = {}
    @staticmethod
    def on_moved(g, fn): SNAP.on_moved(g, fn)
    @staticmethod
    def moved_by_code(g): SNAP.moved_by_code(g)
    @staticmethod
    def title_catcher(g, x, y, w, h, fn, key=None):
        key = key or id(g); once = Kit.once(fn, key)
        def fn():
            if Kit.just_dragged(g): Kit._dbl.pop(key, None); return
            once()
        def clicked():
            now = time.time()
            if Kit.just_dragged(g): Kit._dbl.pop(key, None); return
            pos = (g.GetX(), g.GetY()); last = Kit._dbl.get(key)
            if last and now - last[0] <= 0.7 and abs(pos[0] - last[1][0]) <= 3 and abs(pos[1] - last[1][1]) <= 3:
                Kit._dbl.pop(key, None); fn()
            else: Kit._dbl[key] = (now, pos); Kit._forget_old(Kit._dbl, now)
        c = Kit.catcher(g, x, y, w, h, clicked, Kit.DOUBLE_TIP, movable=True)
        if Client.mouse is None: Kit.hook_double(c, fn)
        return c
    DRAG_QUIET = 0.4
    @staticmethod
    def just_dragged(g):
        try:
            if g in SNAP.drag or g in SNAP.dragged: return True
            t = SNAP.drag_end.get(g); return t is not None and time.time() - t < Kit.DRAG_QUIET
        except Exception: return False
    @staticmethod
    def catcher(g, x, y, w, h, fn, tooltip=None, movable=False):
        c = G.CreateGumpColorBox(0.01, "#000000"); c.SetRect(x, y, w, h); Kit.on_click(c, fn); Kit.with_tip(c, tooltip)
        if movable: c.CanMove = True
        g.Add(c); return c
    @staticmethod
    def art_button(g, store, key, art, x, y, label=None, tooltip=None, hue=None, on_click=None):
        bdict, cdict = store; b = G.CreateGumpButton("", Kit.HUE_TEXT, art[0], art[1], art[2]); b.SetPos(x, y); g.Add(b)
        bdict[key] = b; cdict[key] = False; bid = Binds.note(store, key, on_click, b, tooltip)
        def clicked(*args):
            cdict[key] = True
            if on_click is not None: on_click()
        click = Binds.wrap(bid, clicked); Kit.on_click(b, click); combo = Binds.saved.get(bid)
        if combo: tooltip = (tooltip + " " if tooltip else "") + "(hotkey: %s)" % combo
        Kit.with_tip(b, tooltip)
        if label:
            bw, bh = Kit.pic_size(art[0])
            lbl = Kit.add_label(g, label, x + (bw or 30) + 5, y + max(((bh or 22) - 16) // 2, 0), hue)
            lbl.SetAcceptMouseInput(True); Kit.on_click(lbl, click); return lbl
        return b
    @staticmethod
    def closed(win, key="g"):
        if not Kit.was_clicked(win["store"], "close"): return False
        Kit.dispose(win[key]); return True
    @staticmethod
    def weight_bar(g, c, bx, by, bw, centre=0):
        lw, lh = Kit.pic_size(Kit.LINE_RED); fh = max(4, min(11, Kit.pic_size(Kit.LINE_BLUE)[1] or lh or 9))
        if centre: by += max(0, (centre - fh) // 2)
        if lw > 0: Kit.add_tiled(g, Kit.LINE_RED, bx, by, bw, fh, hue=946)
        else: Kit.add_tiled(g, Kit.SECTION_TILE, bx, by, bw, fh, 1.0)
        fills = {}
        for kind, art, hue in (("ok", Kit.LINE_POISON, 0), ("warn", Kit.LINE_BLUE, 0x0035), ("red", Kit.LINE_RED, 0)):
            f = Kit.add_tiled(g, art, bx, by, 1, fh, hue=hue)
            if f is not None: f.IsVisible = False; fills[kind] = f
        c["wfills"] = fills; c["wbar_w"] = bw
    @staticmethod
    def weight_level(frac, bw):
        if frac < 0: return None, 0
        kind = "red" if frac >= 0.95 else "warn" if frac >= 0.85 else "ok"
        return kind, max(1, min(bw, int(round(bw * min(1.0, frac)))))
    @staticmethod
    def weight_show(fills, kind, width):
        for k, f in fills.items():
            try:
                if k == kind: Kit.ui_w(f, width)
                f.IsVisible = k == kind
            except Exception: pass
    @staticmethod
    def hook_once(holder, key, *pairs):
        if holder[key]: return
        holder[key] = True
        for event, fn in pairs:
            with Kit.quiet: getattr(API.Events, event)(fn)
    @staticmethod
    def was_clicked(store, key):
        cdict = store[1]; hit = cdict.get(key, False)
        if hit: cdict[key] = False
        if Kit.clicks_seen: return hit
        ctl = store[0].get(key)
        if ctl is not None:
            try: hit = ctl.HasBeenClicked() or hit
            except Exception: pass
        return hit
    _texts = {}; _texts_cap = 3000; _texts_sweep = False; _texts_list = None; _texts_at = 0; TEXTS_SLICE = 400
    @staticmethod
    def set_text(lbl, text, hue=None):
        try: e = Kit._texts.get(lbl)
        except TypeError: e = [None, None]
        if e is None:
            e = Kit._texts[lbl] = [None, None]
            if len(Kit._texts) > Kit._texts_cap: Kit._prune_texts()
        changed = e[0] != text
        if changed:
            e[0] = text
            try: lbl.Text = text
            except Exception:
                try: lbl.SetText(text)
                except Exception: pass
        if hue is not None and e[1] != hue:
            e[1] = hue
            try: lbl.Hue = hue
            except Exception: pass
        return changed
    @staticmethod
    def _prune_texts():
        if not Client.on_client_thread(): Kit._texts_cap = len(Kit._texts) + 500; Kit._texts_sweep = True; return
        lst = Kit._texts_list
        if lst is None:
            lst = Kit._texts_list = list(Kit._texts); Kit._texts_at = 0; Kit._texts_cap = len(Kit._texts) + 500
        Kit._texts_sweep = True; i = Kit._texts_at; end = min(len(lst), i + Kit.TEXTS_SLICE); texts = Kit._texts
        while i < end:
            lbl = lst[i]; i += 1
            try:
                if lbl.IsDisposed: texts.pop(lbl, None)
            except Exception: texts.pop(lbl, None)
        Kit._texts_at = i
        if i >= len(lst):
            Kit._texts_list = None; Kit._texts_sweep = False; Kit._texts_cap = max(3000, 2 * len(Kit._texts))
    _widths = {}; _ctl_prop = {}; _rp_sizes = {}; SWEEP_FULL = 5.0; WIDTHS_MAX = 4000
    @staticmethod
    def text_w(text):
        px = Kit._widths.get(text)
        if px is None:
            px = 0
            try: l = G.CreateGumpLabel(text, Kit.HUE_TEXT); px = int(l.GetWidth() or 0); Kit.dispose(l)
            except Exception: pass
            px = px or 8 * len(text)
            if len(Kit._widths) >= Kit.WIDTHS_MAX:
                wd = Kit._widths
                for k in [k for k in wd if len(k) > 12]: del wd[k]
                if len(wd) >= Kit.WIDTHS_MAX // 2: wd.clear()
            Kit._widths[text] = px
        return px
    @staticmethod
    def wrap(text, width):
        lines = []; words = text.split()
        if words and Kit._px["ok"] is None: Kit.text_px("")
        if Kit._px["ok"]:
            pad, cw = Kit._px["pad"], Kit._px_ch; sp = cw.get(" ")
            if sp is None: sp = Kit._ch_w(" ")
            cur = 0
            for word in words:
                ww = Kit.text_px(word) - pad
                if lines and cur + sp + ww <= width: lines[-1] += " " + word; cur += sp + ww
                else: lines.append(word); cur = pad + ww
            return lines or [""]
        for word in words:
            if lines and Kit.text_w(lines[-1] + " " + word) <= width: lines[-1] += " " + word
            else: lines.append(word)
        return lines or [""]
    _px = {"ok": None, "pad": 0}; _px_ch = {}; PX_REF = "Total 120.0 / 700.0 (+5.2) Session ~1h 05m: Magery, Str"
    @staticmethod
    def _ch_w(ch): w = Kit.text_w("x" + ch + "x") - Kit.text_w("xx"); Kit._px_ch[ch] = w; return w
    @staticmethod
    def text_px(text):
        px = Kit._px
        if px["ok"] is None:
            try:
                px["pad"] = 2 * Kit.text_w("x") - Kit.text_w("xx"); ref = Kit.PX_REF
                px["ok"] = Kit.text_w(ref) == px["pad"] + sum(Kit._ch_w(ch) for ch in ref)
            except Exception: px["ok"] = False
        if not px["ok"]: return Kit.text_w(text)
        w, cw = px["pad"], Kit._px_ch
        for ch in text: x = cw.get(ch); w += Kit._ch_w(ch) if x is None else x
        return w
    @staticmethod
    def fit(text, width, tail=".."):
        text = str(text or "")
        if len(text) * 9 <= width or Kit.text_px(text) <= width: return text
        if Kit._px["ok"]:
            w, cw = Kit.text_px(text + tail), Kit._px_ch
            while text and w > width: w -= cw.get(text[-1], 0); text = text[:-1]
            return text.rstrip() + tail
        lo, hi = 1, len(text) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if Kit.text_w(text[:mid] + tail) <= width: lo = mid
            else: hi = mid - 1
        return text[:lo].rstrip() + tail
    GUMP_CMDS = ("page", "button", "buttontileart", "checkertrans", "croppedtext", "gumppic", "gumppictiled",
                 "gumppichued", "gumppicphued", "htmlgump", "xmfhtmlgump", "xmfhtmlgumpcolor", "xmfhtmltok", "noclose",
                 "nodispose", "nomove", "noresize", "group", "endgroup", "radio", "checkbox", "resizepic", "text",
                 "textentry", "textentrylimited", "tilepic", "tilepichue", "tooltip", "itemproperty", "mastergump",
                 "picinpic", "picinpichued", "picinpicphued", "togglelimitgumpscale", "maparea")
    _gump_cmds = frozenset(GUMP_CMDS); _cliloc_cache = {}
    @staticmethod
    def gump_is_int(a):
        a = str(a)
        if a.startswith("-"): a = a[1:]
        return len(a) > 0 and a.isdigit()
    @staticmethod
    def _gump_arg_ok(a):
        if Kit.gump_is_int(a): return True
        if a.startswith("#"): return Kit.gump_is_int(a[1:])
        if "=" in a: return a.split("=", 1)[0].isalnum()
        return a.startswith("@") or a.endswith("@")
    @staticmethod
    def gump_is_cmd(line):
        words = str(line).strip().split()
        if not words or words[0].lower() not in Kit._gump_cmds: return False
        inside = False
        for a in words[1:]:
            if inside:
                if a.endswith("@"): inside = False
                continue
            if a.startswith("@") and not (len(a) > 1 and a.endswith("@")): inside = True; continue
            if not Kit._gump_arg_ok(a): return False
        return True
    @staticmethod
    def _gump_split_merged(merged):
        merged = str(merged); low = merged.lower(); n = len(merged)
        for p in range(n):
            for kw in Kit.GUMP_CMDS:
                end = p + len(kw)
                if low[p:end] != kw: continue
                if end < n and merged[end] != " ": continue
                if Kit.gump_is_cmd(merged[p:]): return merged[:p], merged[p:]
        return merged, None
    @staticmethod
    def gump_parse(raw):
        raw = str(raw or "").replace("\r", "").replace("\x00", ""); parts = raw.split("\n")
        while parts and parts[-1].strip() == "": parts.pop()
        j = len(parts)
        while j > 0 and Kit.gump_is_cmd(parts[j - 1]): j -= 1
        if j == 0: lines, cmds = [], parts
        else:
            tail, first = Kit._gump_split_merged(parts[j - 1])
            if first is None: lines, cmds = parts[:j] + [""], parts[j:]
            else: lines, cmds = parts[:j - 1] + [tail], [first] + parts[j:]
        return lines, [c.split() for c in cmds]
    _HTML_RE = re.compile(r"<[^>]*>")
    @staticmethod
    def strip_html(s): return Kit._HTML_RE.sub("", str(s or "")).replace("&nbsp;", " ").strip()
    @staticmethod
    def cliloc_text(n, clilocs=None):
        if clilocs:
            t = clilocs.get(n)
            if t is not None: return t
        t = Kit._cliloc_cache.get(n)
        if t is None:
            t = str(safe(lambda: API.GetClilocString(n), "") or "").strip() or ("#%d" % n)
            if len(Kit._cliloc_cache) > 500: Kit._cliloc_cache.clear()
            Kit._cliloc_cache[n] = t
        return t
    _CELLS = {"htmlgump": (8, 5, None, 6, 1), "xmfhtmlgump": (8, None, 5, 6, 1), "xmfhtmlgumpcolor": (8, None, 5, 6, 1),
              "xmfhtmltok": (9, None, 8, 5, 1), "text": (5, 4, None, None, 0), "croppedtext": (7, 6, None, None, 1)}
    @staticmethod
    def gump_cells(raw, clilocs=None):
        lines, cmds = Kit.gump_parse(raw); cells, buttons = [], []
        for t in cmds:
            try:
                k = t[0].lower()
                if k == "button" and len(t) >= 8:
                    if int(t[5]) == 1: buttons.append((int(t[1]), int(t[2]), int(t[7])))
                    continue
                r = Kit._CELLS.get(k)
                if r is None or len(t) < r[0]: continue
                li, ci, bi, sized = r[1:]; src = "" if li is None else lines[int(t[li])]
                cl = 0 if ci is None else int(str(t[ci]).replace("#", ""))
                cells.append({"x": int(t[1]), "y": int(t[2]), "w": int(t[3]) if sized else 0,
                              "h": int(t[4]) if sized else 0, "raw": src,
                              "text": Kit.strip_html(src) if ci is None else Kit.cliloc_text(cl, clilocs),
                              "cliloc": cl, "bg": bi is not None and int(t[bi]) != 0})
            except (ValueError, IndexError): continue
        return cells, buttons
    @staticmethod
    def dispose(ctrl):
        if ctrl is not None:
            try: ctrl.Dispose()
            except Exception: pass
    @staticmethod
    def is_open(g):
        if g is None: return False
        try: return not g.IsDisposed
        except Exception: return False
    @staticmethod
    def get_var(key, default=""):
        try: v = API.GetPersistentVar(key, default, API.PersistentVar.Char)
        except Exception: v = default
        return str(v or default)
    @staticmethod
    def put_var(key, value):
        with Kit.quiet: API.SavePersistentVar(key, value, API.PersistentVar.Char)
    _data_dir = [None]
    DATA_MOVE = re.compile(r"^(_ultima_tracker_data\.txt|_lookout_feed\.txt|_unified_bag_\d+\.cfg"
                           r"|_storage_index_[^\\/]+?\.txt|_swing_timer_\d+\.txt"
                           r"|Skills_[0-9A-F]{8}\.txt|SkillBags_[0-9A-F]{8}_rule\d+\.txt"
                           r"|Meters_[0-9A-F]{8}\.txt|Grimoire_saved\.txt" r"|Grimoire_runebook_dump\.txt)"
                           r"(\.\d+)?(\.tmp)?$")
    DATA_MOVE_ROOT = re.compile(r"^(Grimoire_saved\.txt|Grimoire_runebook_dump\.txt)$")
    @staticmethod
    def script_dir():
        base = str(API.ScriptPath or "").rstrip("/\\")
        if base and os.path.isfile(base): base = os.path.dirname(base)
        if base.endswith("Modules"): base = os.path.dirname(base)
        return base or safe(Kit._legion_root, "")
    @staticmethod
    def _legion_root():
        import System; return os.path.join(str(System.AppDomain.CurrentDomain.BaseDirectory), "LegionScripts")
    @staticmethod
    def data_dir():
        d = Kit._data_dir[0]
        if d is None:
            base = Kit.script_dir(); d = Kit._data_dir[0] = os.path.join(base, SETTINGS_DIR) if base else SETTINGS_DIR
        return d
    @staticmethod
    def data_path(name): return os.path.join(Kit.data_dir(), name)
    @staticmethod
    def data_setup():
        base, d = Kit.script_dir(), Kit.data_dir()
        try:
            if not os.path.isdir(d): os.makedirs(d)
        except Exception as ex:
            Kit._data_dir[0] = base or ""
            Kit.say("couldn't make the %s folder (%s); saving beside the script." % (SETTINGS_DIR, ex), Kit.HUE_BAD)
            return
        moved, failed = 0, 0; places = [(base, Kit.DATA_MOVE)] if base else []; root = safe(Kit._legion_root, "")
        norm = lambda p: os.path.normcase(os.path.abspath(p)) if p else ""
        if root and norm(root) != norm(base): places.append((root, Kit.DATA_MOVE_ROOT))
        for place, pat in places:
            try: names = os.listdir(place)
            except Exception: continue
            for n in names:
                if not pat.match(n): continue
                src, dst = os.path.join(place, n), os.path.join(d, n)
                try:
                    if not os.path.isfile(src) or os.path.exists(dst): continue
                    os.rename(src, dst); moved += 1
                except Exception: failed += 1
        if base:
            src, dst = os.path.join(base, PROFILE_DIR), os.path.join(d, PROFILE_DIR)
            try:
                if os.path.isdir(src) and not os.path.exists(dst): os.rename(src, dst); moved += 1
            except Exception: failed += 1
        if moved: Kit.say("moved %s into the %s folder." % (Kit.count(moved, "saved file"), SETTINGS_DIR), Kit.HUE_INFO)
        if failed:
            Kit.say("couldn't move %s into the %s folder (open in another client?)." % (
                Kit.count(failed, "saved file"), SETTINGS_DIR), Kit.HUE_BAD)
    @staticmethod
    def load_pos(key, default=(200, 200), size=None):
        try: x, y = Kit.get_var(key, "%d,%d" % default).split(","); x, y = int(x), int(y)
        except Exception: x, y = default
        w, h = size if size else (0, 0); return Kit.adapt(x, y, w, h)
    @staticmethod
    def load_min(key): return Kit.get_var(key, "0") == "1"
    @staticmethod
    def save_min(key, minimized): Kit.put_var(key, "1" if minimized else "0")
    @staticmethod
    def save_pos(key, g):
        if Kit.is_open(g): Kit.put_var(key, "%d,%d" % (g.GetX(), g.GetY()))
    @staticmethod
    def queuer(st):
        def queue(action):
            def handler(*args):
                if action not in st["queue"]:
                    st["queue"].append(action)
                    if not HOST.in_hop: HOST.poke()
            return handler
        return queue
    @staticmethod
    def disposer(key, st, win):
        def on_disposed(g):
            def handler(*args):
                if win["g"] is g and not st["shutting"]: win["g"] = None; HOST.disable(key)
            return handler
        return on_disposed
    TITLE_GAP = 6; CAP_GAP = 10; BARE_GAP = 4
    @staticmethod
    def caption_tip(caption, tip):
        tip = str(tip or "")
        if not tip: return caption
        return "%s: %s%s" % (caption, tip[:1].lower(), tip[1:])
    @staticmethod
    def title_plan(w, title, buttons, after=None):
        M = Kit.MARGIN; right = w - M - 84 - Kit.DOCK_DX; t0 = M + 30; caps_w = [35 + Kit.text_w(b[0]) for b in buttons]
        def xs(with_caps):
            out, x = [], right
            for cw in caps_w:
                x -= cw if with_caps else 30; out.append(x); x -= Kit.CAP_GAP if with_caps else Kit.BARE_GAP
            return out
        tw = Kit.text_w(title.upper()); aw = (8 + Kit.text_w(after)) if after else 0
        for with_caps in (True, False):
            pos = xs(with_caps); left = pos[-1] if pos else right
            if t0 + tw + aw + Kit.TITLE_GAP <= left: return with_caps, bool(after), title.upper(), pos, left
        pos = xs(False)
        while pos and pos[-1] < M + 4: pos.pop()
        left = pos[-1] if pos else right; room = left - Kit.TITLE_GAP - t0
        T = title.upper() if tw <= room else "" if room < Kit.text_w("W..") else Kit.fit(title.upper(), room)
        return False, False, T, pos, left
    @staticmethod
    def title_bar(g, store, w, title, key, on_min, on_dock, on_settings=None, close_tip=None, extra=None, after=None):
        M = Kit.MARGIN; Kit.add_section(g, M, M, w - 2 * M, 30); buttons = []
        if on_settings is not None:
            buttons.append(("Settings", "settings", Kit.ART_PAGE, Kit.SETTINGS_TIP % title, on_settings))
        for b in (extra or ()): buttons.append((b[2], b[0], b[1], b[3], b[4]))
        zoned = Kit.zone_up(key); shift = (84 + Kit.DOCK_DX - 10) if zoned else 0
        caps, show_after, shown, pos, left = Kit.title_plan(w + shift, title, buttons, after)
        Kit.add_label(g, shown, M + 30, M + 7, Kit.HUE_TITLE)
        if show_after: Kit.add_label(g, after, M + 30 + Kit.text_w(shown) + 8, M + 7, Kit.HUE_INFO)
        if zoned:
            strip = Kit.catcher(g, M, M, max(20, left - M - Kit.TITLE_GAP), 30, lambda *a: None, None, movable=True)
        else: strip = Kit.title_catcher(g, M, M, max(20, left - M - Kit.TITLE_GAP), 30, on_min, key=key)
        if shown != title.upper(): Kit.with_tip(strip, title if zoned else "%s. %s" % (title, Kit.DOUBLE_TIP))
        for (cap, bkey, art, tip, fn), x in zip(buttons, pos):
            Kit.art_button(g, store, bkey, art, x, M + 4, cap if caps else None,
                           tip if caps else Kit.caption_tip(cap, tip), on_click=fn)
        if not zoned:
            Kit.dock_button(g, store, w - M - 74, M + 7, on_click=on_dock)
            Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 74, M + 7, None, Kit.MIN_TIP, on_click=on_min)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None,
                           close_tip or Kit.CLOSE_TIP % title)
        return pos[-1] if pos else w - M - 84 - Kit.DOCK_DX + shift
    @staticmethod
    def zone_up(key): return bool(HOST.layout_holds(key))
    _mouse = [None]
    @staticmethod
    def mouse_pos():
        f = Kit._mouse[0]
        if f is None:
            Kit._mouse[0] = False; t = Client._type("ClassicUO.Input.Mouse")
            if t is not None:
                try: m = Client._member(t, "Position"); p = m[0](); int(p.X); Kit._mouse[0] = m[0]
                except Exception: pass
            f = Kit._mouse[0]
        if not f: return None
        try: p = f(); return int(p.X), int(p.Y)
        except Exception: return None
    @staticmethod
    def mini_bar(g, store, w, h, title, key, on_restore, text="", hue=None, close_tip=None):
        Kit.add_window_frame(g, w, h, corners=False); Kit.add_section(g, 8, 8, w - 16, h - 16)
        lbl = Kit.add_label(g, text, 18, 15, Kit.HUE_INFO if hue is None else hue)
        Kit.title_catcher(g, 8, 8, w - 70, h - 16, on_restore, key=str(key) + ":mini")
        Kit.art_button(g, store, "restore", Kit.ART_RESTORE, w - 60, 15, None, Kit.RESTORE_TIP, on_click=on_restore)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - 44, 12, None, close_tip or Kit.CLOSE_TIP % title)
        return lbl
    @staticmethod
    def dock_button(g, store, x_min, y_min, on_click=None, key="tobar"):
        return Kit.art_button(g, store, key, Kit.ART_DOCK, x_min - Kit.DOCK_DX,
                              y_min + Kit.DOCK_DY, None, Kit.DOCK_TIP, on_click=on_click)
    @staticmethod
    def dock_hooks(title, icon, st, win, redraw, scale=False, fit=None):
        def state():
            if win["g"] is None or st["shutting"]: return None
            return "docked" if st["docked"] else ("minimized" if st["minimized"] else "open")
        def to(docked, minimized):
            def f(): st["docked"], st["minimized"] = docked, minimized; redraw()
            return f
        def undock(): st["docked"] = False; redraw()
        hooks = {"title": title, "icon": icon, "state": state, "show": to(False, False), "dock": to(True, True),
                 "undock": undock, "minimize": to(False, True), "gump": lambda: win["g"], "redraw": redraw}
        if scale: hooks["scale"] = True
        if fit is not None: hooks["fit"] = fit
        return hooks
    @staticmethod
    def flush():
        MTQ = Client._find_mtq()
        if MTQ is None or not Client.on_client_thread(): return False
        try:
            n = 0
            while int(MTQ.Count) > 0 and n < 500: MTQ.ProcessQueue(); n += 1
            return int(MTQ.Count) == 0
        except Exception: return False
    @staticmethod
    def client_control(api_ctrl):
        try:
            pt = type(api_ctrl); cache = Kit._ctl_prop; prop = cache.get(pt, False)
            if prop is False:
                prop = None; import clr; flags = Client.flags(); t = clr.GetClrType(pt)
                while t is not None:
                    prop = t.GetProperty("Control", flags)
                    if prop is not None: break
                    t = t.BaseType
                cache[pt] = prop
            if prop is not None: return prop.GetValue(api_ctrl, None)
        except Exception: pass
        return None
    @staticmethod
    def _scroll_skip(g):
        info = Kit._scrolled.get(g)
        if info is None: return [], None
        base = info.get("skip_raw")
        if base is None:
            base = [pr for pr in map(Kit.client_control, info["frame"] + info["band"]) if pr is not None]
            info["skip_raw"] = base
        skip = list(base); area = info["area_raw"]
        try:
            kids = area.Children
            if int(kids.Count) > 0: skip.append(kids[0])
        except Exception: pass
        return skip, area
    @staticmethod
    def scale_window(g, scale):
        if abs(scale - 1.0) < 0.001: return True
        root = Kit.client_control(g)
        if root is None or not Kit.flush(): return False
        skip, area = Kit._scroll_skip(g); same = Kit._same()
        def tree(c):
            if skip and any(same(c, k) for k in skip): return
            if area is None or not same(c, area):
                if str(c.GetType().Name) == "GumpPicTiled": Kit.set(c, "ScaleTiledTexture", True)
                c.ApplyScale(scale, True, True, False)
            kids = c.Children
            for i in range(kids.Count): tree(kids[i])
        try:
            kids = root.Children
            for i in range(kids.Count): tree(kids[i])
            return True
        except Exception: return False
    @staticmethod
    def ui_pos(c, x, y):
        if c is None: return
        if not (Fill.recs and Fill.change(c, x=x, y=y)): c.SetPos(int(x), int(y))
    @staticmethod
    def ui_rect(c, x, y, w, h):
        if c is None: return
        if not (Fill.recs and Fill.change(c, x, y, w, h)): c.SetRect(int(x), int(y), int(w), int(h))
    @staticmethod
    def ui_w(c, w):
        if c is None: return
        if not (Fill.recs and Fill.change(c, w=w)): c.SetWidth(int(w))
    @staticmethod
    def ui_size(c, w, h):
        if c is None: return
        if not (Fill.recs and Fill.change(c, w=w, h=h)): c.SetWidth(int(w)); c.SetHeight(int(h))
    @staticmethod
    def ui_y(c): own = Fill.own(c) if Fill.recs else None; return own[1] if own is not None else c.GetY()
    SPELL_WORDS, MAGERY, CAST_DELAY_OTHER = {}, [], {}
    for _r in ("uus jux,Clumsy,BM NS,;in mani ylem,Create Food,GA GI MR,;rel wis,Feeblemind,GI NS,;"
               "in mani,Heal,GA GI SS,heal;in por ylem,Magic Arrow,SA,;in lor,Night Sight,SS SA,;"
               "flam sanct,Reactive Armor,GA SS SA,;des mani,Weaken,GA NS,;ex uus,Agility,BM MR,;"
               "uus wis,Cunning,MR NS,;an nox,Cure,GA GI,cure;an mani,Harm,NS SS,;in jux,Magic Trap,GA SS SA,;"
               "an jux,Magic Untrap,BM SA,;uus sanct,Protection,GA GI SA,;uus mani,Strength,MR NS,;"
               "rel sanct,Bless,GA MR,;vas flam,Fireball,BP,;an por,Magic Lock,BM GA SA,;in nox,Poison,NS,;"
               "ort por ylem,Telekinesis,BM MR,;rel por,Teleport,BM MR,;ex por,Unlock,BM SA,;"
               "in sanct ylem,Wall of Stone,BM GA,;vas an nox,Arch Cure,GA GI MR,cure+;"
               "vas uus sanct,Arch Protection,GA GI MR SA,;des sanct,Curse,GA NS SA,;in flam grav,Fire Field,BP SS SA,;"
               "in vas mani,Greater Heal,GA GI MR SS,heal;por ort grav,Lightning,MR SA,;ort rel,Mana Drain,BP MR SS,;"
               "kal ort por,Recall,BP BM MR,;in jux hur ylem,Blade Spirits,BP MR NS,;an grav,Dispel Field,BP GA SS SA,;"
               "kal in ex,Incognito,BM GA NS,;in jux sanct,Magic Reflection,GA MR SS,;"
               "por corp wis,Mind Blast,BP MR NS SA,;an ex por,Paralyze,GA MR SS,;in nox grav,Poison Field,BP NS SS,;"
               "kal xen,Summon Creature,BM MR SS,;an ort,Dispel,GA MR SA,;corp por,Energy Bolt,BP NS,;"
               "vas ort flam,Explosion,BM MR,;an lor xen,Invisibility,BM NS,;kal por ylem,Mark,BP BM MR,;"
               "vas des sanct,Mass Curse,GA MR NS SA,;in ex grav,Paralyze Field,BP GI SS,;wis quas,Reveal,BM SA,;"
               "vas ort grav,Chain Lightning,BP BM MR SA,;in sanct grav,Energy Field,BP MR SS SA,;"
               "kal vas flam,Flamestrike,SS SA,;vas rel por,Gate Travel,BP MR SA,;ort sanct,Mana Vampire,BP BM MR SS,;"
               "vas an ort,Mass Dispel,BP GA MR SA,;flam kal des ylem,Meteor Swarm,BM MR SS SA,;"
               "vas ylem rel,Polymorph,BM MR SS,;in vas por,Earthquake,BM GI MR SA,;"
               "vas corp por,Energy Vortex,BP BM MR NS,;an corp,Resurrection,BM GA GI,;"
               "kal vas xen hur,Air Elemental,BM MR SS,;kal vas xen corp,Summon Daemon,BM MR SS SA,;"
               "kal vas xen ylem,Earth Elemental,BM MR SS,;kal vas xen flam,Fire Elemental,BM MR SS SA,;"
               "kal vas xen an flam,Water Elemental,BM MR SS,;expor flamus,Cleanse by Fire,1.0,cure;"
               "obsu vulni,Close Wounds,1.5,heal;consecrus arma,Consecrate Weapon,0.5,;dispiro malas,Dispel Evil,0.25,;"
               "divinum furis,Divine Fury,1.0,;forul solum,Enemy of One,0.5,;augus luminos,Holy Light,1.75,;"
               "dium prostra,Noble Sacrifice,1.5,;extermo vomica,Remove Curse,1.5,;sanctum viatas,Sacred Journey,1.5,;"
               "uus corp,Animate Dead,1.75,;in jux mani xen,Blood Oath,1.5,;in agle corp ylem,Corpse Skin,1.5,;"
               "an sanct gra char,Curse Weapon,1.0,;pas tym an sanct,Evil Omen,1.0,;"
               "rel xen vas bal,Horrific Beast,2.0,;rel xen corp ort,Lich Form,2.0,;wis an ben,Mind Rot,1.5,;"
               "in sar,Pain Spike,1.25,;in vas nox,Poison Strike,2.0,;in bal nox,Strangle,2.0,;"
               "kal xen bal,Summon Familiar,2.0,;rel xen an sanct,Vampiric Embrace,2.0,;"
               "kal xen bal beh,Vengeful Spirit,2.0,;kal vas an flam,Wither,1.5,;rel xen um,Wraith Form,2.0,;"
               "ort corp grav,Exorcism,2.0,").split(";"):
        _w, _n, _x, _t = _r.split(","); SPELL_WORDS[_w] = (_n, _t or None)
        if _x[0] > "9": MAGERY.append((_n, _x))
        else: CAST_DELAY_OTHER[_n] = float(_x)
    MAGERY = tuple(MAGERY); del _r, _w, _n, _x, _t
    REAGENTS = {"BP": ("Black Pearl", 0x0F7A), "BM": ("Blood Moss", 0x0F7B), "GA": ("Garlic", 0x0F84),
                "GI": ("Ginseng", 0x0F85), "MR": ("Mandrake Root", 0x0F86), "NS": ("Nightshade", 0x0F88),
                "SS": ("Spiders' Silk", 0x0F8D), "SA": ("Sulfurous Ash", 0x0F8C)}
    SPELL_MANA = (4, 6, 9, 11, 14, 20, 40, 50); CAST_DELAY = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25)
    CAST_EXTRA = 0.5; _spells = {}
    @staticmethod
    def spell_info(name):
        if not Kit._spells:
            for n, secs in Kit.CAST_DELAY_OTHER.items(): Kit._spells[n.lower()] = (0, (), 0, secs)
            for i, (n, regs) in enumerate(Kit.MAGERY):
                c = i // 8 + 1
                Kit._spells[n.lower()] = (c, tuple(regs.split()), Kit.SPELL_MANA[c - 1],
                                          Kit.CAST_DELAY[c - 1] + Kit.CAST_EXTRA)
        return Kit._spells.get(str(name or "").strip().lower())
    COMPASS = ("E", "SE", "S", "SW", "W", "NW", "N", "NE")
    FACETS = ("Felucca", "Trammel", "Ilshenar", "Malas", "Tokuno", "Ter Mur")
    @staticmethod
    def compass(dx, dy, names=None):
        if not dx and not dy: return ""
        return (names or Kit.COMPASS)[int(round(math.atan2(dy, dx) / (math.pi / 4))) % 8]
    @staticmethod
    def held_item():
        pid = HOST.pass_id if HOST.in_hop else None
        if pid is not None and Kit._held[0] == pid: return Kit._held[1]
        try: v = int(API.GetHeldItem() or 0)
        except Exception: v = 0
        if pid is not None: Kit._held[0], Kit._held[1] = pid, v
        return v
    _held = [-1, 0]
    @staticmethod
    def find_item(serial):
        if not serial: return None
        try: return API.FindItem(serial)
        except Exception: return None
    @staticmethod
    def where_text(dx, dy, here="under you", names=None):
        d = max(abs(int(dx)), abs(int(dy)))
        if d == 0: return here
        return "%s %s" % (Kit.count(d, "tile"), Kit.compass(dx, dy, names))
    @staticmethod
    def count(n, word, many=None): return "%d %s" % (n, word if n == 1 else many or word + "s")
    @staticmethod
    def facet_name(m):
        try: m = int(m)
        except Exception: return "?"
        return Kit.FACETS[m] if 0 <= m < len(Kit.FACETS) else "facet %d" % m
    AGO = ((60, 1, "%ds"), (3600, 60, "%dm"), (0, 3600, "%dh %dm"))
    AGO_SHORT = ((60, 1, "%ds"), (3600, 60, "%dm"), (0, 3600, "%dh"))
    AGO_WORDS = ((60, 1, "just now"), (3600, 60, "%dm ago"), (86400, 3600, "%dh ago"), (0, 86400, "%dd ago"))
    @staticmethod
    def ago(secs, units=None):
        secs = max(0, int(secs))
        for limit, div, fmt in units or Kit.AGO:
            if not limit or secs < limit: break
        n = fmt.count("%")
        if n == 0: return fmt
        return fmt % (secs // div) if n == 1 else fmt % (secs // div, secs % div // 60)
    @staticmethod
    def read_int(ctrl, default, lo=None, hi=None):
        try: v = int(str(ctrl.Text or "").strip())
        except Exception: return default
        if lo is not None and v < lo: v = lo
        if hi is not None and v > hi: v = hi
        return v
    @staticmethod
    def codec_load(text):
        out = {}
        for part in str(text or "").split(";"):
            if "=" in part: k, v = part.split("=", 1); out[k.strip()] = v.strip()
        return out
    @staticmethod
    def kv_load(key, sep, into, nums=None, strs=()):
        nums = nums or {}
        for part in Kit.get_var(key).split(sep):
            if "=" not in part: continue
            k, v = part.split("=", 1); k, v = k.strip(), v.strip()
            if k in nums:
                try: into[k] = max(nums[k][0], min(nums[k][1], int(v)))
                except ValueError: pass
            elif k in strs: into[k] = v
            elif k in into: into[k] = v == "1"
    @staticmethod
    def kv_save(key, sep, vals, order, nums=None, strs=()):
        nums = nums or {}
        Kit.put_var(key, sep.join("%s=%s" % (k, vals[k] if k in nums or k in strs else ("1" if vals[k] else "0"))
                                  for k in order))
    @staticmethod
    def with_tip(ctrl, text):
        if text:
            try: ctrl.SetTooltip(text)
            except Exception: pass
        return ctrl
    @staticmethod
    def sayer(title, gate=None, key=None):
        def say(text, hue=None):
            if gate is None or gate[key]: API.SysMsg("%s: %s" % (title, text), Kit.HUE_INFO if hue is None else hue)
        return say
    @staticmethod
    def say(text, hue=None): API.SysMsg(APP_NAME + ": " + str(text), Kit.HUE_INFO if hue is None else hue)
    @staticmethod
    def win_action(action, st, key, title, build, min_key=None):
        if action == "settings": HOST.show_settings(key)
        elif action == "toggle_min":
            st["minimized"], st["docked"] = not st["minimized"], False; HOST.dock_forget(key)
            if min_key: Kit.save_min(min_key, st["minimized"])
            build()
        elif action == "to_bar": HOST.dock_to_bar(key, title)
        elif action == "redraw": build()
        else: return False
        return True
    @staticmethod
    def show_window(g, x, y, w, h, lock_key, hidden, on_disposed, moved, into=None, parts=None, max_h=None):
        xy = Kit.place(g, x, y, w, h, None, max_h)
        if lock_key is not None and HOST.layout_locked(lock_key): g.CanMove = False
        if into is not None: into.update(parts)
        if on_disposed is not None: G.AddControlOnDisposed(g, on_disposed)
        G.AddGump(g)
        if moved is not None: Kit.on_moved(g, moved)
        if hidden: g.IsVisible = False
        return xy
    @staticmethod
    def row_set(row, val, now):
        cur = row.get("val")
        if (cur[0] if cur else None) != (val[0] if val else None):
            row["prev"], row["val"], row["changed"] = cur or None, val, now
    @staticmethod
    def row_clicker(row, queue, kind, grace=0.15, follow=True):
        def handler(*args):
            v = row.get("prev")
            if not (v and time.time() - row.get("changed", 0.0) < grace): v = row.get("val")
            if not v or not v[0]: return
            if follow and Follow.alt_held(): queue(("follow", v[0]))()
            else: queue((kind,) + tuple(v))()
        return handler
    @staticmethod
    def buttons(g, store, x, y, rows, gap=20):
        for b in rows:
            Kit.art_button(g, store, b[0], b[1], x, y, b[2], b[3], b[5] if len(b) > 5 else None,
                           b[4] if len(b) > 4 else None)
            x += 35 + Kit.text_w(b[2]) + gap
        return x
    class Form(object):
        OPTS = {"top": 30, "pad": 10, "ch": 26, "fh": 28, "nh": 20, "bh": 28, "dx": 12, "ldy": 3, "lgap": 10,
                "ugap": 8, "fw": 50, "sw": 140, "sdy": 2, "ndy": 0, "bdy": -2, "bgap": 20, "fmt": "%d"}
        STEP = {"check": "ch", "note": "nh", "buttons": "bh", "num": "fh", "text": "fh", "slider": "fh"}
        FIELDS = ("num", "text", "slider")
        def __init__(self, g, x, y, w, vals, page=(), store=None, **opts):
            self.g, self.x, self.y, self.w, self.vals, self.opts = g, x, y, w, vals, opts
            self.top, self.c, self.store, self.specs = y, {}, store or ({}, {}), []
            for sec in page: self.section(*sec)
        @property
        def h(self): return max(0, self.y - self.top - Kit.GAP)
        @staticmethod
        def height(page, w=0, **opts): return Kit.Form(None, 0, 0, w, {}, page, **opts).h
        def _o(self, sec, r=None):
            o = dict(Kit.Form.OPTS); o.update(self.opts); o.update(sec)
            if r and type(r[-1]) is dict: o.update(r[-1])
            return o
        @staticmethod
        def _step(r, o):
            if o.get("stay"): return 0
            if r[0] in ("gap", "custom"): return r[1]
            return o["h"] if "h" in o else o[Kit.Form.STEP[r[0]]]
        def section(self, title, rows, sec=None):
            sec = sec or {}; so, opts = self._o(sec), [self._o(sec, r) for r in rows]
            sh = sec.get("sh") or so["top"] + sum(Kit.Form._step(r, o) for r, o in zip(rows, opts)) + so["pad"]
            x, ry, g = self.x, self.y + so["top"], self.g
            if g is not None: Kit.add_section(g, x, self.y, self.w, sh, title)
            self.y += sh + Kit.GAP
            if g is None: return
            lw = max([Kit.text_w(r[2]) for r in rows if r[0] in Kit.Form.FIELDS] or [0])
            for r, o in zip(rows, opts):
                self._row(g, r, o, x, ry, o.get("lw", lw if o.get("align") else None)); ry += Kit.Form._step(r, o)
        def _row(self, g, r, o, sx, y, lw):
            kind, c, x = r[0], self.c, sx + o["dx"]; k = r[1] if kind in Kit.Form.FIELDS or kind == "check" else None
            if kind == "check": c[k] = Kit.add_check(g, r[2], x, y, self.vals[k], r[3]); self.specs.append((r, o))
            elif kind == "note":
                lbl = Kit.add_label(g, r[1], x, y + o["ndy"], o.get("hue", Kit.HUE_INFO))
                if o.get("key"): c[o["key"]] = lbl
            elif kind == "buttons": Kit.buttons(g, self.store, x, y + o["bdy"], [b[:5] for b in r[1]], o["bgap"])
            elif kind == "custom": r[2](self, sx, y)
            elif kind in Kit.Form.FIELDS:
                lbl = Kit.add_label(g, r[2], x, y + o["ldy"])
                fx = x + (Kit.text_w(r[2]) if lw is None else lw) + o["lgap"]; tip = r[3]
                if kind == "num":
                    if tip and not tip.endswith(")"): tip += " (%d-%d)" % (r[5], r[6])
                    c[k] = Kit.add_textbox(g, o["fmt"] % self.vals[k], fx, y, o["fw"])
                    if r[4]: Kit.add_label(g, r[4], fx + o["fw"] + o["ugap"], y + o["ldy"], Kit.HUE_INFO)
                elif kind == "text":
                    tw = o.get("tw") or self.w - (fx - sx) - 16
                    c[k] = Kit.add_textbox(g, self.vals[k], fx, y, tw, numbers=False)
                else:
                    c[k] = Kit.add_slider(g, fx, y + o["sdy"], o["sw"], r[4], r[5], self.vals[k])
                    if o.get("vfmt") or o.get("unit"):
                        c[k + "_lbl"] = Kit.add_label(g, o["vfmt"] % self.vals[k] if o.get("vfmt") else o["unit"],
                                                      fx + o["sw"] + o["ugap"], y + o["ldy"], Kit.HUE_INFO)
                Kit.with_tip(c[k], tip)
                if o.get("ltip"): Kit.with_tip(lbl, tip)
                self.specs.append((r, o))
        def read(self, strict=False, empty=None):
            out = dict(self.vals)
            for r, o in self.specs:
                kind, k = r[0], r[1]
                try:
                    ctrl = self.c[k]
                    if kind == "check": v = bool(ctrl.IsChecked)
                    elif kind == "num":
                        v = Kit.read_int(ctrl, out[k], *((r[5], r[6]) if o.get("clamp", True) else ()))
                        v = o.get("cast", int)(v if r[5] <= v <= r[6] else out[k])
                    elif kind == "text": v = str(ctrl.Text or "").strip() or (empty or {}).get(k, "")
                    else: v = max(r[4], min(r[5], int(ctrl.Value)))
                except Exception:
                    if strict: raise
                    continue
                out[k] = v
                if kind == "slider" and o.get("vfmt"): Kit.set_text(self.c[k + "_lbl"], o["vfmt"] % v)
            return out
    class Page(object):
        def __init__(self, vals, table, save=None, on_change=None, opts=None, strict=False, empty=None, adjust=None,
                     clicks=None, every=0.0, final=False):
            self.vals, self.table, self.save, self.on_change, self.opts = vals, table, save, on_change, opts or {}
            self.strict, self.empty, self.adjust, self.clicks, self.every = strict, empty, adjust, clicks, every
            self.f, self.unread, self.at, self.final, self.force = None, False, 0.0, final, False
        def rows(self, w): return self.table(w) if callable(self.table) else self.table
        def height(self, w): return Kit.Form.height(self.rows(w), w, **self.opts)
        def build(self, g, x, y, w):
            self.unread, self.at = False, 0.0; self.f = Kit.Form(g, x, y, w, self.vals, self.rows(w), **self.opts)
            return self.f
        def poll(self, force=False):
            f = self.f
            if f is None: return
            if self.clicks is not None:
                self.clicks(f)
                if self.f is not f: return
            if self.every:
                now = time.time()
                if not force and now < self.at: self.unread = True; return
                self.at, self.unread = now + self.every, False
            try: new = f.read(self.strict, self.empty)
            except Exception: self.f = None; return
            self.force = force
            if self.adjust is not None: self.adjust(f, new)
            if new == self.vals: return
            old = dict(self.vals); self.vals.update(new)
            if self.save is not None: self.save()
            if self.on_change is not None: self.on_change(old, self.vals)
        def closed(self):
            if (self.unread or self.final) and self.f is not None: self.poll(True)
            self.f, self.unread = None, False
    class Cleanup(object):
        def __init__(self): self.jobs = []
        def add(self, fn, *args): self.jobs.append((fn, args)); return fn
        def service(self, name, fn):
            HOST.services[name] = fn; self.jobs.append((Kit.Cleanup.drop, (name, fn))); return fn
        def gump(self, holder, key="g", **clear): self.jobs.append((Kit.Cleanup.dispose, (holder, key, clear)))
        @staticmethod
        def drop(name, fn):
            if HOST.services.get(name) is fn: HOST.services.pop(name, None)
        @staticmethod
        def dispose(holder, key, clear): g, holder[key] = holder.get(key), None; holder.update(clear); Kit.dispose(g)
        def close(self):
            jobs = self.jobs
            while jobs:
                fn, args = jobs.pop()
                try: fn(*args)
                except Exception: pass
    class Window(object):
        def __init__(self, key, title, st, win, build, pos_key, min_key=None, default=(200, 200), mini=None,
                     icon=None, cleanup=None, gkey="g", names=("c", "store"), lock=True, owner=True, close_tip=None,
                     clear=None, docked_min=False):
            self.key, self.title, self.st, self.win, self.build, self.pos_key = key, title, st, win, build, pos_key
            self.min_key, self.default, self.mini, self.icon, self.cleanup = min_key, default, mini, icon, cleanup
            self.gkey, self.names, self.lock, self.owner, self.close_tip = gkey, names, lock, owner, close_tip
            self.clear, self.docked_min, self.slot, self.held, self.old = clear or {}, docked_min, None, False, None
            self.queue = Kit.queuer(st) if st is not None else None; self.x = self.y = self.w = self.h = 0
            self.c, self.store = {}, ({}, {})
        def minimized(self): return self.st is not None and bool(self.st["minimized"])
        def start_min(self): return bool(HOST.dock_wanted(self.key) or (self.min_key and Kit.load_min(self.min_key)))
        def begin(self, w, h, default=None):
            if Kit.is_open(self.old) and self.old is not self.win.get(self.gkey): Kit.dispose(self.old)
            old = self.win.get(self.gkey); mini = self.minimized()
            if mini and self.mini: w, h = self.mini
            self.w, self.h = w, h
            if Kit.is_open(old): self.x, self.y = old.GetX(), old.GetY()
            else: self.x, self.y = Kit.load_pos(self.pos_key, default or self.default, (w, h))
            self.old, self.win[self.gkey] = old, None
            if self.cleanup is not None and not self.held: self.held = True; self.cleanup.add(self.release)
            g = G.CreateGump(True, True); self.c, self.store = {}, ({}, {})
            if mini:
                self.c["status"] = Kit.mini_bar(g, self.store, w, h, self.title, self.key, self.queue("toggle_min"),
                                                close_tip=self.close_tip)
            return g, self.store, self.c
        def frame(self, g, w=None, h=None, extra=None, after=None, settings=True, mouse=True, corners=True):
            w = self.w if w is None else w; q = self.queue
            Kit.add_window_frame(g, w, self.h if h is None else h, corners, mouse)
            return Kit.title_bar(g, self.store, w, self.title, self.key, q("toggle_min"), q("to_bar"),
                                 q("settings") if settings else None, self.close_tip, extra, after)
        def end(self, g, parts=None, w=None, h=None, max_h=None):
            st, parts = self.st, dict(parts or {}); parts[self.gkey] = g
            for name, v in zip(self.names or (), (self.c, self.store)): parts[name] = v
            xy = Kit.show_window(g, self.x, self.y, self.w if w is None else w, self.h if h is None else h,
                                 self.key if self.lock else None, st is not None and st["minimized"] and st["docked"],
                                 self.disposed(g), self.save_pos, self.win, parts, max_h)
            old, self.old = self.old, None; Kit.dispose(old); return xy
        def disposed(self, g):
            def handler(*args):
                win = self.win
                if win.get(self.gkey) is not g or (self.owner and self.st["shutting"]): return
                win[self.gkey] = None; win.update(self.clear)
                if self.owner: HOST.disable(self.key)
            return handler
        def save_pos(self): Kit.save_pos(self.pos_key, self.win.get(self.gkey))
        def close(self):
            if Kit.is_open(self.old) and self.old is not self.win.get(self.gkey): Kit.dispose(self.old)
            st = self.st; self.save_pos()
            if self.min_key and st is not None:
                Kit.save_min(self.min_key, st["minimized"] and not (self.docked_min and st["docked"]))
            g, self.win[self.gkey] = self.win.get(self.gkey), None; self.win.update(self.clear); Kit.dispose(g)
        def release(self): self.held = False; self.close()
        def action(self, action): return Kit.win_action(action, self.st, self.key, self.title, self.build, self.min_key)
        def fit(self, w, h, mode):
            new = (int(w), int(h)) if (w is not None and h is not None) else None
            if new != self.slot or (mode == "again" and new is not None): self.slot = new; self.queue("redraw")()
        def dock(self, fit=False, scale=False, **extra):
            hooks = Kit.dock_hooks(self.title, self.icon, self.st, self.win, self.queue("redraw"), scale,
                                   self.fit if fit is True else (fit or None))
            hooks.update(extra); HOST.dock_add(self.key, hooks)
            if self.cleanup is not None: self.cleanup.add(HOST.dock_remove, self.key)
            return hooks
    class _Quiet(object):
        def __enter__(self): return self
        def __exit__(self, kind, value, tb): return kind is not None and issubclass(kind, Exception)
    quiet = _Quiet(); _notos = {}
    @staticmethod
    def noto_name(mob):
        try: v = mob.Notoriety
        except Exception: return "unknown"
        return Kit.noto_of(v)
    @staticmethod
    def noto_of(v):
        try: return Kit._notos[v]
        except KeyError: pass
        except Exception: return str(v).split(".")[-1].lower()
        n = Kit._notos[v] = str(v).split(".")[-1].lower(); return n
    @staticmethod
    def set(obj, attr, value):
        try: setattr(obj, attr, value)
        except Exception: pass


class Fill(object):
    ROW_H = 72; MIN_EDGE = 20; MIN_BG = 40; FILL_MIN_K = 0.6; FIELD_T = "TTFTextInputField"; recs = {}; by_raw = {}
    w2r = {}; _api_t = [None]; broken = False
    @staticmethod
    def _axis(n, N, M, ivals, mode):
        n, N = float(max(1, n)), float(max(1, N)); E = N - n
        if E < 0.5: return None
        lo, hi = float(M), n - M
        if hi - lo < 8: lo, hi = 0.0, n
        merged = []
        for a, b in sorted(ivals):
            a, b = max(lo, float(a)), min(hi, float(b))
            if b - a < 1: continue
            if merged and a <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], b)
            else: merged.append([a, b])
        if not merged or mode == "grid": merged = [[lo, hi]]
        L = sum(b - a for a, b in merged); pts = [(0.0, 0.0)]; shift = 0.0
        for a, b in merged: pts.append((a, a + shift)); shift += E * (b - a) / L; pts.append((b, b + shift))
        pts.append((n, n + shift)); return pts
    @staticmethod
    def _ev(m, v):
        if m is None or v <= m[0][0]: return float(v)
        for i in range(1, len(m)):
            a0, b0 = m[i - 1]; a1, b1 = m[i]
            if v <= a1:
                if a1 - a0 < 1e-9: return b1
                return b0 + (v - a0) * (b1 - b0) / (a1 - a0)
        a, b = m[-1]; return b + (v - a)
    @staticmethod
    def _xform(rec, e):
        kind, x, y, w, h, bg = e[:6]; role = e[8] if len(e) > 8 else None
        if role == "back":
            pe = rec["ent"].get(e[9])
            if pe is not None: fr = Fill._xform(rec, pe); return fr[0] - 2, fr[1] - 1, fr[2] + 4, fr[3] + (h - pe[4])
        k = rec.get("k", 1.0); h0 = h
        if k != 1.0:
            x, y, w = x * k, y * k, w * k
            if role == "field":
                slack = e[10] if len(e) > 10 else None
                fh = h if slack is None else max(h * k, min(h, (h + 2 * slack) * k)); y = y + h * k / 2.0 - fh / 2.0
                h = fh
            else: h = h * k
            if bg is not None: bg = (bg[0] * k, bg[1] * k, bg[2] * k, bg[3] * k)
            w = max(1, int(round(w))); h = max(1, int(round(h)))
        fx, fy = rec["fx"], rec["fy"]; N, Hn = rec["size"]; ev = Fill._ev
        if kind == "s":
            x0, x1 = ev(fx, x), ev(fx, x + w)
            if h0 >= Fill.MIN_EDGE and (h0 > Fill.ROW_H or rec["rows"]): y0, y1 = ev(fy, y), ev(fy, y + h)
            else: c = ev(fy, y + h / 2.0); y0, y1 = c - h / 2.0, c + h / 2.0
            x0 = max(0, min(N - 1, int(round(x0)))); y0 = max(0, min(Hn - 1, int(round(y0))))
            x1, y1 = min(N, int(round(x1))), min(Hn, int(round(y1))); return x0, y0, max(1, x1 - x0), max(1, y1 - y0)
        mode = rec["mode"]
        if bg is not None:
            bx, by, bw, bh = bg
            if mode == "frame":
                cbx, cby = bx + bw / 2.0, by + bh / 2.0; nx = x + ev(fx, cbx) - cbx; ny = y + ev(fy, cby) - cby
            else:
                if mode == "anchor":
                    third = bw / 3.0; cx = x + w / 2.0
                    if cx < bx + third: nx = ev(fx, bx) + (x - bx)
                    elif cx > bx + bw - third: nx = ev(fx, bx + bw) - (bx + bw - x)
                    else: nx = ev(fx, cx) - w / 2.0
                else: nx = ev(fx, x + w / 2.0) - w / 2.0
                ny = ev(fy, y + h / 2.0) - h / 2.0
        elif mode == "frame" and not e[7]:
            nx = x + (N - rec["nat"][0] * k) / 2.0; ny = y + (Hn - rec["nat"][1] * k) / 2.0
        else: nx = ev(fx, x + w / 2.0) - w / 2.0; ny = ev(fy, y + h / 2.0) - h / 2.0
        nx = max(0, min(int(round(nx)), N - w)) if w < N else 0
        ny = max(0, min(int(round(ny)), Hn - h)) if h < Hn else 0; return nx, ny, w, h
    @staticmethod
    def raw_of(c):
        r = Fill.w2r.get(c)
        if r is None:
            r = Kit.client_control(c)
            if r is None: return None
            if len(Fill.w2r) > 4000: Fill.w2r.clear()
            Fill.w2r[c] = r
        return r
    @staticmethod
    def _set(raw, r, pos_only=False):
        t = Fill._api_t[0]
        if t is None: return False
        try:
            wraps = Fill._wraps; w = wraps.get(raw)
            if w is None:
                mk = Fill._mk
                if mk is None: import System; mk = Fill._mk = System.Activator.CreateInstance
                w = mk(t, raw)
                if len(wraps) >= 6000: wraps.clear()
                wraps[raw] = w
            if pos_only: w.SetPos(int(r[0]), int(r[1]))
            else: w.SetRect(int(r[0]), int(r[1]), int(r[2]), int(r[3]))
            return True
        except Exception: Fill.broken = True; return False
    _wraps = {}; _mk = None
    @staticmethod
    def _find_api_type(g):
        if Fill._api_t[0] is not None: return True
        try:
            import clr; t = clr.GetClrType(type(g))
            while t is not None:
                if str(t.Name) == "ApiUiBaseControl": Fill._api_t[0] = t; return True
                t = t.BaseType
        except Exception: pass
        return False
    @staticmethod
    def _scan(rec, kids, skip, k_now=1.0):
        ents = rec["ent"]; same = Kit._same(); new = []
        for c in kids:
            try:
                if c.IsDisposed or c in ents: continue
            except Exception: continue
            if skip and any(same(c, s) for s in skip): continue
            r = Kit._raw_rect(c)
            if r is None: continue
            tn = str(c.GetType().Name); kind = "s" if tn in Fill.STRETCH else "p"
            if tn == "GumpPic":
                try:
                    if int(c.Graphic) in (Kit.LINE_RED, Kit.LINE_BLUE, Kit.LINE_POISON): kind = "s"
                except Exception: pass
            if kind == "s" and tn == "AlphaBlendControl" and r[2] < Fill.MIN_BG:
                try:
                    if float(c.Alpha) < 0.05: kind = "p"
                except Exception: pass
            e = [kind, r[0], r[1], r[2], r[3], None, tuple(r), c in rec["frame"],
                 "field" if tn == Fill.FIELD_T else None, None, None]
            ents[c] = e; Fill.by_raw[c] = (rec, e); new.append((c, e))
            if tn == "ScrollArea": rec["nested"] = True
            if k_now != 1.0: Fill._scale_one(rec, c, k_now)
        if new: Fill._pair_fields(rec)
        return new
    @staticmethod
    def _pair_fields(rec):
        ents = rec["ent"]; fields = [(c, e) for c, e in ents.items() if e[8] == "field"]
        if not fields: return
        for c, e in ents.items():
            if e[0] != "s" or e[8] is not None or e[7]: continue
            for fc, fe in fields:
                if abs(e[1] - (fe[1] - 2)) <= 1 and abs(e[2] - (fe[2] - 1)) <= 1 \
                        and abs(e[3] - (fe[3] + 4)) <= 1 and e[4] <= 26:
                    e[8], e[9] = "back", fc; fe[9] = c; break
        for fc, fe in fields:
            fx, fy, fw, fh = fe[1], fe[2], fe[3], fe[4]; slack = None
            for c, e in ents.items():
                if c is fc or e[8] == "back" or e[7]: continue
                x, y, w, h = e[1], e[2], e[3], e[4]
                if x >= fx + fw or x + w <= fx: continue
                if x <= fx and y <= fy and x + w >= fx + fw and y + h >= fy + fh: continue
                if y + h <= fy: gap = fy - (y + h)
                elif y >= fy + fh: gap = y - (fy + fh)
                else: continue
                slack = gap if slack is None else min(slack, gap)
            fe[10] = slack
    @staticmethod
    def _desc(c):
        out = []
        try: stack = list(Kit._children(c))
        except Exception: return out
        while stack:
            d = stack.pop(); out.append(d)
            try: stack.extend(Kit._children(d))
            except Exception: pass
        return out
    @staticmethod
    def _scale_one(rec, c, k):
        try:
            if abs(k - 1.0) > 0.001 and str(c.GetType().Name) == "GumpPicTiled": c.ScaleTiledTexture = True
            c.SetInternalScale(k)
        except Exception: pass
        desc = rec["desc"]
        for d in Fill._desc(c):
            try:
                own = desc.get(d)
                if own is None:
                    r = Kit._raw_rect(d)
                    if r is None: continue
                    own = desc[d] = tuple(r)
                if abs(k - 1.0) > 0.001 and str(d.GetType().Name) == "GumpPicTiled": d.ScaleTiledTexture = True
                Fill._set(d, (own[0] * k, own[1] * k, max(1, own[2] * k), max(1, own[3] * k))); d.SetInternalScale(k)
            except Exception: pass
    STRETCH = ("GumpPicTiled", "AlphaBlendControl", "ScrollArea", "ResizePic", "SimpleProgressBar")
    @staticmethod
    def _bgs(rec):
        nw, nh = rec["nat"]; out = []; frame = rec["frame"]
        for c, e in rec["ent"].items():
            if e[0] != "s" or c in frame or e[8] == "back": continue
            x, y, w, h = e[1], e[2], e[3], e[4]
            if w < Fill.MIN_BG or h < Fill.MIN_EDGE: continue
            if w >= nw - 8 and h >= nh - 8: continue
            if y < 2 or y + h > nh - 2: continue
            out.append((x, y, w, h))
        return out
    @staticmethod
    def _maps(rec):
        nw, nh = rec["nat"]; N, Hn = rec["size"]; k = rec.get("k", 1.0); M = Kit.MARGIN * k; bgs = Fill._bgs(rec)
        tall = [b for b in bgs if b[3] > Fill.ROW_H]; rec["rows"] = not tall
        rec["fx"] = Fill._axis(nw * k, N, M, [(b[0] * k, (b[0] + b[2]) * k) for b in bgs], rec["mode"])
        rec["fy"] = Fill._axis(nh * k, Hn, M, [(b[1] * k, (b[1] + b[3]) * k) for b in (tall or bgs)], rec["mode"])
        rec["bgs"] = bgs
        for e in rec["ent"].values(): Fill._anchor(e, bgs)
    @staticmethod
    def _anchor(e, bgs):
        if e[0] == "s": return
        cx, cy = e[1] + e[3] / 2.0, e[2] + e[4] / 2.0; best = None
        for x, y, w, h in bgs:
            if (x <= cx <= x + w and y <= cy <= y + h and (best is None or w * h < best[2] * best[3])):
                best = (x, y, w, h)
        e[5] = best
    @staticmethod
    def _apply(rec, pairs=None):
        for c, e in (list(rec["ent"].items()) if pairs is None else pairs):
            try:
                if c.IsDisposed: rec["ent"].pop(c, None); Fill.by_raw.pop(c, None); Fill._wraps.pop(c, None); continue
            except Exception: continue
            r = Fill._xform(rec, e)
            if r != e[6] and Fill._set(c, r, e[0] == "p" and rec.get("k", 1.0) == 1.0 and (r[2], r[3]) == (e[3], e[4])):
                e[6] = r
    @staticmethod
    def fit(g, x, y, W, H, mode="anchor"):
        if Fill.broken or not Fill._find_api_type(g) or not Kit.flush(): return None
        raw = Kit._raw_gump(g)
        if raw is None: return None
        rec = Fill.recs.get(g); info = Kit.scroll_info(g)
        if rec is None:
            r = Snap.rect(g)
            if r is None: return None
            nat = (info["w"], info["h"]) if info is not None else (r[2], r[3])
            rec = {"g": g, "raw": raw, "nat": nat, "size": None, "slot": None, "mode": mode,
                   "ent": {}, "fx": None, "fy": None, "rows": False, "n": -1, "an": -1,
                   "placed": None, "scroll": False, "bgs": [], "frame": set(), "k": 1.0, "desc": {}, "nested": False,
                   "head0": (info["head"] if info is not None else None) or (Kit.MARGIN + 30 + Kit.GAP)}
            fr = Kit._frames.get(g)
            rec["frame"].update(pr for pr in map(Kit.client_control, fr["pieces"] if fr else ()) if pr is not None)
            Fill.recs[g] = rec
        elif rec["placed"] is not None and info is None:
            r = Snap.rect(g)
            if r is not None and (r[2], r[3]) != rec["placed"][2:]: rec["nat"] = (r[2], r[3]); rec["size"] = None
        rec["mode"] = mode; skip, area = Kit._scroll_skip(g)
        try: cnt = (int(raw.Children.Count), int(area.Children.Count) if area is not None else 0)
        except Exception: cnt = None
        now = time.time()
        if cnt is not None and cnt == rec.get("cnt") and 0 <= rec.get("full_at", 0.0) - now:
            n, an = rec["n"], rec.get("an")
        else:
            rec["cnt"] = cnt; rec["full_at"] = now + Kit.SWEEP_FULL; n = Kit._live_count(raw)
            an = Kit._live_count(area) if area is not None else 0
        new = []
        if n != rec["n"] or an != rec.get("an"):
            kids = Kit._children(raw)
            if area is not None: kids = kids + Kit._children(area)
            new = Fill._scan(rec, kids, skip + ([area] if area is not None else []), rec["k"])
            rec["n"], rec["an"] = Kit._live_count(raw), an
        nw, nh = rec["nat"]; band = Kit.SCROLL_BAND; conv = g in Kit._scrolled
        if conv:
            Wb = W - band
            k = 1.0 if (Wb >= nw and H >= nh) else min(1.0, Wb / float(nw), max(Fill.FILL_MIN_K, H / float(nh)))
            scroll = nh * k > H + 1
        else: k, scroll = Fill.scale_for(nw, nh, W, H, rec["nested"])
        size = (W - band, int(round(nh * k)) if scroll else H) if scroll or conv else (W, H)
        if abs(k - rec["k"]) > 0.0005:
            rec["k"] = k
            for c in list(rec["ent"]): Fill._scale_one(rec, c, k)
            rec["size"] = None
        if size != rec["size"] or mode != rec.get("mode_was"):
            rec["size"], rec["mode_was"], rec["scroll"] = size, mode, scroll; Fill._maps(rec); Fill._apply(rec)
        elif new:
            for c, e in new: Fill._anchor(e, rec["bgs"])
            Fill._apply(rec, new)
        r = Snap.rect(g)
        if r is not None and (r[0], r[1], r[2], r[3]) == (x, y, W, H) and not new and rec["placed"] is not None:
            return False
        if scroll or conv: head = int(round(rec["head0"] * k)); Kit._place_raw(g, x, y, size[0], size[1], head, H)
        else: Kit._place_raw(g, x, y, W, H, None, None)
        r = Snap.rect(g); rec["placed"] = (x, y, r[2], r[3]) if r is not None else (x, y, W, H)
        rec["slot"] = (x, y, W, H); return True
    @staticmethod
    def scale_for(nw, nh, W, H, nested=False):
        nw, nh = float(max(1, nw)), float(max(1, nh))
        if W >= nw and H >= nh: return 1.0, False
        if nested: return min(1.0, W / nw, H / nh), False
        k = min(1.0, W / nw, max(Fill.FILL_MIN_K, H / nh))
        if nh * k > H + 1:
            k = min(1.0, (W - Kit.SCROLL_BAND) / nw, max(Fill.FILL_MIN_K, H / nh)); return k, nh * k > H + 1
        return k, False
    @staticmethod
    def unfit(g):
        rec = Fill.recs.pop(g, None)
        if rec is None: return False
        for d, own in list(rec.get("desc", {}).items()):
            try:
                if not d.IsDisposed: Fill._set(d, own); d.SetInternalScale(1.0)
            except Exception: pass
        for c, e in list(rec["ent"].items()):
            Fill.by_raw.pop(c, None)
            try:
                if not c.IsDisposed:
                    if rec.get("k", 1.0) != 1.0: c.SetInternalScale(1.0)
                    Fill._set(c, (e[1], e[2], e[3], e[4]), e[0] == "p" and rec.get("k", 1.0) == 1.0)
            except Exception: pass
            Fill._wraps.pop(c, None)
        if Kit.is_open(g):
            try:
                nw, nh = rec["nat"]; Kit._place_raw(g, int(g.GetX()), int(g.GetY()), nw, nh, None, None)
                Kit.moved_by_code(g)
            except Exception: pass
        return True
    @staticmethod
    def beside(rf, r, nr):
        def one(f0, f1, a0, a1, b0, b1):
            if f0 >= a1: return b1 + (f0 - a1)
            if f1 <= a0: return b0 - (a0 - f0)
            return f0 + (b0 - a0)
        return (one(rf[0], rf[0] + rf[2], r[0], r[0] + r[2], nr[0], nr[0] + nr[2]),
                one(rf[1], rf[1] + rf[3], r[1], r[1] + r[3], nr[1], nr[1] + nr[3]))
    @staticmethod
    def prune():
        if not Fill.recs: return
        for g in [g for g in Fill.recs if not Kit.is_open(g)]:
            rec = Fill.recs.pop(g)
            for c in rec["ent"]: Fill.by_raw.pop(c, None); Fill._wraps.pop(c, None)
        if len(Fill.by_raw) > 20000:
            Fill.by_raw.clear()
            for rec in Fill.recs.values():
                for c, e in rec["ent"].items(): Fill.by_raw[c] = (rec, e)
    @staticmethod
    def entry(c): return Fill.by_raw.get(Fill.raw_of(c)) if Fill.recs else None
    @staticmethod
    def change(c, x=None, y=None, w=None, h=None):
        hit = Fill.entry(c)
        if hit is None: return False
        rec, e = hit
        for i, v in ((1, x), (2, y), (3, w), (4, h)):
            if v is not None: e[i] = int(v)
        if rec["size"] is None: return False
        if e[0] == "p" and (x is not None or y is not None): Fill._anchor(e, rec["bgs"])
        r = Fill._xform(rec, e)
        try:
            if e[0] == "p" and w is None and h is None: c.SetPos(r[0], r[1])
            else: c.SetRect(r[0], r[1], r[2], r[3])
            e[6] = r
        except Exception: return False
        return True
    @staticmethod
    def own(c): hit = Fill.entry(c); return None if hit is None else tuple(hit[1][1:5])


class PageCanvas(object):
    def __init__(self, inner): self._inner = inner; self.ctrls = []; self.sections = []
    def Add(self, ctrl, *args):
        self.ctrls.append(ctrl)
        if self._inner is not None: return self._inner.Add(ctrl, *args)
        return ctrl
    def __getattr__(self, name):
        if self._inner is None: raise AttributeError(name)
        return getattr(self._inner, name)


class Alerts(object):
    KEY = "VirtueAssistant_alerts"; POS_KEY = "VirtueAssistant_alert_pos"; W, H = 420, 46
    LEVELS = {"info": Kit.HUE_INFO, "warn": Kit.HUE_TITLE, "alarm": Kit.HUE_BAD}; TEST_KEY = "va.test"
    def __init__(self):
        self.kinds = {}; self.order = []; self.choice = {}; self.banner_on = True
        self.mute = self.loaded = self.busy = self.shown = self.alarm = self.flash_on = self.clicked = False
        self.last = {}; self.pending = []; self.sounds = []; self.pings = []
        self.sound_at = self.hide_at = self.flash_at = self.moved_at = 0.0; self.g = self.pos = None; self.c = {}
        self.count = 0; self.hue = Kit.HUE_TITLE; self.line = ""; self.tw = self.W - 36
    def load(self):
        self.loaded = True; self.choice = {}; self.mute, self.banner_on = False, True
        for k, v in Kit.codec_load(Kit.get_var(self.KEY)).items():
            if k == "mute": self.mute = v == "1"
            elif k == "banner": self.banner_on = v != "0"
            elif k.startswith("kind."):
                bits = v.split(",")
                try: snd = int(bits[1]) if len(bits) > 1 and bits[1] != "" else None
                except ValueError: snd = None
                self.choice[k[5:]] = [bits[0] != "0", snd]
    def save(self):
        parts = ["mute=%d" % (1 if self.mute else 0), "banner=%d" % (1 if self.banner_on else 0)]
        for k in sorted(self.choice):
            on, snd = self.choice[k]
            parts.append("kind.%s=%d,%s" % (k, 1 if on else 0, "" if snd is None else int(snd)))
        Kit.put_var(self.KEY, ";".join(parts))
    def setting(self, key):
        if not self.loaded: self.load()
        k = self.kinds.get(key); ch = self.choice.get(key); on = ch[0] if ch is not None else True
        snd = ch[1] if ch is not None and ch[1] is not None else (k["sound"] if k else 0); return on, int(snd or 0)
    def choose(self, key, on=None, sound=None):
        cur = self.setting(key); new = [cur[0] if on is None else bool(on), cur[1] if sound is None else int(sound)]
        if new != list(cur) or key not in self.choice: self.choice[key] = new; self.save()
    def kind(self, key, label, sound=None, owner=None):
        key = str(key); k = self.kinds.get(key)
        new = {"label": str(label or key), "sound": int(sound or 0), "owner": str(owner or APP_NAME)}
        if k is None: self.order.append(key)
        if new != k:
            self.kinds[key] = new
            if key != self.TEST_KEY: HOST.refresh_settings(ALERTS_PAGE)
        return key
    def raise_(self, key, text, level="warn", sound=None, ping=None, who=None, owner=None):
        if not self.loaded: self.load()
        key = str(key); k = self.kinds.get(key)
        if k is None: self.kind(key, key, sound, owner); k = self.kinds[key]
        on, snd = self.setting(key)
        if not on: return False
        now = time.time(); rk = (key, str(who) if who is not None else str(text)); t = self.last.get(rk)
        if t is not None and 0 <= now - t < ALERT_RATE: return False
        if len(self.last) > 200:
            cut = now - ALERT_RATE
            for old in [x for x, tt in self.last.items() if tt < cut or tt > now]: del self.last[old]
        self.last[rk] = now; who_t = k["owner"]; text = str(text)
        line = text if text.startswith(who_t + ":") else "%s: %s" % (who_t, text)
        hue = self.LEVELS.get(level, Kit.HUE_TITLE); API.SysMsg(line, hue)
        sid = (int(sound) if sound else snd) if snd else 0
        if sid and not self.mute and len(self.sounds) < 4:
            if not self.sounds and not 0 <= now - self.sound_at < ALERT_SOUND_GAP: self._play(sid, now)
            else: self.sounds.append(sid)
        if self.banner_on:
            self.pending.append((line, hue, level == "alarm"))
            if len(self.pending) > 50: del self.pending[:-50]
        if ping is not None and len(self.pings) < 8:
            safe(lambda: self.pings.append([int(ping[0]), int(ping[1]), now + 10.0]))
        self.busy = True; return True
    def _play(self, sid, now): self.sound_at = now; API.PlaySound(int(sid))
    def tick(self, now):
        if not self.busy: return
        if self.sounds and not 0 <= now - self.sound_at < ALERT_SOUND_GAP: self._play(self.sounds.pop(0), now)
        if self.pings:
            x, y, until = self.pings[0]; fn = HOST.services.get("pings.send"); done = now > until or fn is None
            if not done:
                try: done = bool(fn(x, y))
                except Exception: done = True
            if done: self.pings.pop(0)
        if self.pending: items, self.pending = self.pending, []; self._show(items, now)
        if self.shown: self._watch(now)
        self.busy = bool(self.sounds or self.pings or self.pending or self.shown)
    def _show(self, items, now):
        if not self.banner_on: return
        line, hue, alarm = items[-1]
        if self.shown and Kit.is_open(self.g):
            self.count += len(items); self.alarm = self.alarm or any(a for _, _, a in items)
        else: self.count = len(items) - 1; self.alarm = any(a for _, _, a in items)
        self.line, self.hue = line, hue
        if not Kit.is_open(self.g): self._build()
        if self.g is None: return
        self._label()
        if not self.shown:
            Kit.set(self.g, "IsVisible", True); self.shown = True; self.clicked = False
            self.pos = Snap.pos(self.g)
        self.hide_at = now + ALERT_HOLD; self.flash_at = now + ALERT_FLASH; self.flash_on = True
    def _label(self):
        c = self.c; more = ("+%d more" % self.count) if self.count > 0 else ""; mw = Kit.text_px(more) if more else 0
        tw = self.W - 36 - ((mw + 8) if more else 0); self.tw = tw
        Kit.set_text(c["text"], Kit.fit(self.line, tw), self.hue); Kit.set_text(c["more"], more, Kit.HUE_INFO)
        if more: c["more"].SetPos(self.W - 18 - mw, 15)
    def _watch(self, now):
        g = self.g
        if not Kit.is_open(g): self.shown, self.g = False, None; return
        p = Snap.pos(g)
        if p != self.pos:
            if self.pos is not None: self.moved_at = now
            self.pos = p
        if self.clicked:
            self.clicked = False
            if not 0 <= now - self.moved_at <= 0.35: self.dismiss(); return
        if self.alarm:
            if not 0 < self.flash_at - now <= ALERT_FLASH:
                self.flash_at = now + ALERT_FLASH; self.flash_on = not self.flash_on
                Kit.set_text(self.c["text"], Kit.fit(self.line, self.tw), Kit.HUE_BAD
                             if self.flash_on else Kit.HUE_TEXT)
        elif not 0 < self.hide_at - now <= ALERT_HOLD: self.dismiss()
    def dismiss(self):
        self.shown, self.count, self.alarm = False, 0, False; g = self.g
        if Kit.is_open(g): Kit.set(g, "IsVisible", False)
    def _click(self): self.clicked = True; self.busy = True
    def _build(self):
        W, H = self.W, self.H; sw = Kit.screen()[0] or 1024
        x, y = Kit.load_pos(self.POS_KEY, (max(0, (sw - W) // 2), 60), (W, H)); g = G.CreateGump(True, True)
        Kit.add_window_frame(g, W, H, corners=False); Kit.add_section(g, 8, 8, W - 16, H - 16)
        c = {"text": Kit.add_label(g, "", 18, 15, Kit.HUE_TITLE),
             "more": Kit.add_label(g, "", W - 60, 15, Kit.HUE_INFO)}
        Kit.catcher(g, 0, 0, W, H, self._click, "Click to dismiss; drag to move", movable=True)
        Kit.show_window(g, x, y, W, H, None, False, None, lambda: Kit.save_pos(self.POS_KEY, self.g))
        self.g, self.c = g, c; self.shown = False
    def close(self):
        g, self.g = self.g, None
        if Kit.is_open(g): Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g); self.shown = False; self.pending, self.sounds, self.pings = [], [], []; self.busy = False


class Guard(object):
    KEY = "VirtueAssistant_guard"; EVERY = 0.25
    def __init__(self): self.state = self.rd = self.saved = None; self.next = 0.0; self.cache = (0.0, None, None)
    def tick(self, now):
        if now < self.next and self.next - now <= self.EVERY: return
        self.next = now + self.EVERY
        if self.rd is None: self.rd = Journal.reader(); self.rd.last = 0
        for ln in self.rd.new():
            low = ln.low
            if "protection of the town guards" not in low: continue
            if ln.name and ln.name.lower() != "system": continue
            new = False if low.startswith(GUARD_OUT_TEXTS) else True if low.startswith(GUARD_IN_TEXTS) else None
            if new is not None and new != self.state: self.state = new; self.cache = (0.0, None, None); self._save(new)
    @staticmethod
    def _where():
        try: p = HOST.me(); return int(p.X), int(p.Y), int(API.GetMap())
        except Exception: return None
    def _save(self, state):
        w = self._where()
        if w is None or not (w[0] or w[1]): return
        self.saved = (state, w[0], w[1], w[2])
        Kit.put_var(self.KEY, "%d,%d,%d,%d" % (1 if state else 0, w[0], w[1], w[2]))
    def store(self):
        if self.state is not None: self._save(self.state)
    def _look(self):
        now = time.time()
        if now < self.cache[0] <= now + 1.0: return self.cache[1], self.cache[2]
        w = self._where(); state, name = None, None
        if w is not None:
            x, y, m = w
            for a in GUARD_AREAS:
                try:
                    if a[0] == m and a[1] <= x <= a[3] and a[2] <= y <= a[4]: state, name = True, str(a[5]); break
                except Exception: continue
            if state is None and self.state is None:
                if self.saved is None:
                    try:
                        b = [int(v) for v in Kit.get_var(self.KEY).split(",")]
                        self.saved = (b[0] == 1, b[1], b[2], b[3])
                    except Exception: self.saved = (None, 0, 0, -1)
                s = self.saved
                if s[0] is not None and s[3] == m and abs(s[1] - x) <= GUARD_SPOT and abs(s[2] - y) <= GUARD_SPOT:
                    state = s[0]
        self.cache = (now + 1.0, state, name); return state, name
    def guarded(self):
        if self.state is not None: return self.state
        return self._look()[0]
    def area(self): return self._look()[1]


class _Page(object):
    def __init__(self): self.c = None; self.store = ({}, {})
    def closed(self): self.c = None
    def api(self):
        return {"config_height": self.height, "build_config": self.build,
                "poll_config": self.poll, "config_closed": self.closed}


class AlertsPage(_Page):
    def kinds(self): return [k for k in ALERTS.order if k != Alerts.TEST_KEY]
    def table(self, w):
        return (("ALERTS  (every module's warnings)", (("check", "mute", "Mute every alert sound",
                     "No alert sounds; banners and journal lines stay", {"stay": True}),
                    ("check", "banner", "Show the banner", "Show alerts in a banner (click to dismiss, drag to move)",
                     {"dx": 242}), ("buttons", (("test", Kit.ART_PLAY, "Test alert",
                                  "Raise a test alert"),), {"bdy": 4, "stay": True}),
                    ("note", "The same alert repeats at most every %d s." % int(ALERT_RATE), {"dx": 172, "ndy": 7})),
                 {"top": 32, "sh": 98}), (Kit.fit("ALERT KINDS  (from modules on this session)", w - 16),
                 (("custom", 0, self._kinds),), {"sh": 40 + 28 * max(1, len(self.kinds()))}))
    def height(self, w): return Kit.Form.height(self.table(w), w)
    def build(self, g, x, y, w):
        if not ALERTS.loaded: ALERTS.load()
        self.store = ({}, {})
        self.c = Kit.Form(g, x, y, w, {"mute": ALERTS.mute, "banner": ALERTS.banner_on}, self.table(w), self.store).c
    def _kinds(self, f, x, y):
        g, w, c, kinds = f.g, f.w, f.c, self.kinds(); c.update(rows=[], dd=[])
        if not kinds: Kit.add_label(g, "No alerts yet: turn on a module that has some.", x + 12, y + 6, Kit.HUE_INFO)
        dd_w = 150; x_dd = x + w - 12 - 30 - 8 - dd_w; later = []
        for i, key in enumerate(kinds):
            k = ALERTS.kinds[key]; on, snd = ALERTS.setting(key); ry = y + 4 + 28 * i; label = Kit.fit(k["label"], 196)
            cb = Kit.add_check(g, label, x + 12, ry, on, "Raise the %s alert" % k["label"])
            Kit.add_label(g, Kit.fit(k["owner"], x_dd - 8 - (x + 236)), x + 236, ry + 2, Kit.HUE_INFO)
            Kit.art_button(g, self.store, "play%d" % i, Kit.ART_PLAY, x + w - 12 - 30, ry - 2,
                           None, "Play this alert's sound")
            ids = [sid for _, sid in ALERT_SOUNDS]; names = [n for n, _ in ALERT_SOUNDS]
            if snd not in ids: ids.append(snd); names.append("Sound 0x%X" % snd)
            later.append((key, ids, names, ids.index(snd), x_dd, ry)); c["rows"].append((key, cb))
        for key, ids, names, idx, dx, dy in later:
            dd = G.CreateDropDown(dd_w, names, idx); dd.SetPos(dx, dy); g.Add(dd)
            Kit.with_tip(dd, "This alert's sound"); c["dd"].append((key, dd, ids, idx))
    def poll(self):
        c = self.c
        if c is None: return
        try: mute = bool(c["mute"].IsChecked); banner = bool(c["banner"].IsChecked)
        except Exception: mute, banner = ALERTS.mute, ALERTS.banner_on
        if mute != ALERTS.mute or banner != ALERTS.banner_on:
            ALERTS.mute, ALERTS.banner_on = mute, banner
            if not banner: ALERTS.dismiss()
            ALERTS.save()
        for key, cb in c["rows"]:
            try: v = bool(cb.IsChecked)
            except Exception: continue
            if v != ALERTS.setting(key)[0]: ALERTS.choose(key, on=v)
        if Kit.was_clicked(self.store, "test"):
            ALERTS.kind(Alerts.TEST_KEY, "Test", 0x1EA, APP_NAME); ALERTS.last.pop((Alerts.TEST_KEY, "test"), None)
            ALERTS.raise_(Alerts.TEST_KEY, "This is how an alert looks and sounds.", "warn", who="test")
        for n, row in enumerate(c["dd"]):
            key, dd, ids, idx = row
            try: i = int(dd.GetSelectedIndex())
            except Exception: i = idx
            if i != idx and 0 <= i < len(ids): idx = i; c["dd"][n] = (key, dd, ids, i); ALERTS.choose(key, sound=ids[i])
            if Kit.was_clicked(self.store, "play%d" % n) and ids[idx]: API.PlaySound(int(ids[idx]))


def _norm_key(k): return str(k or "").strip().upper().replace(" ", "")


class Binds(object):
    VAR = "VirtueAssistant_binds"; REPEAT = 0.6; ARM_SECS = 20.0; REG_CAP = 5000; armed_until = 0.0; reg = {}
    saved = {}; last = {}; hooked = set(); armed = False; picked = None; answer = None; loaded = False
    OWNER = "Button binds"
    @staticmethod
    def note(store, key, on_click, ctl, tip):
        owner = HOST.cur_owner
        if owner is None: cur = HOST.current(); owner = cur.key if cur is not None else "va"
        bid = "%s|%s" % (owner, key)
        if len(Binds.reg) >= Binds.REG_CAP: Binds.reg.clear()
        Binds.reg[bid] = (store, key, on_click); return bid
    @staticmethod
    def wrap(bid, handler):
        def click(*args):
            if Binds.armed:
                Binds.armed = False
                if time.time() <= Binds.armed_until: Binds.pick(bid); return
            handler(*args)
        return click
    @staticmethod
    def load():
        if Binds.loaded or not safe(lambda: API.Player): return
        Binds.loaded = True
        for part in str(Kit.get_var(Binds.VAR, "") or "").split(";"):
            if "=" in part:
                bid, combo = part.rsplit("=", 1)
                if bid and combo: Binds.saved[bid] = combo; Binds.hook(combo)
    @staticmethod
    def save(): Kit.put_var(Binds.VAR, ";".join("%s=%s" % kv for kv in sorted(Binds.saved.items())))
    @staticmethod
    def hook(combo):
        HOST.hotkey_note(combo, Binds.OWNER, "a button")
        if combo in Binds.hooked: return
        Binds.hooked.add(combo)
        def fired(*a): Binds.fire(combo)
        try: API.OnHotKey(combo, fired)
        except Exception: Binds.hooked.discard(combo)
    @staticmethod
    def fire(combo):
        now = time.time(); was = Binds.last.get(combo); Binds.last[combo] = now
        if was is not None and 0 <= now - was < Binds.REPEAT: return
        for bid, c in Binds.saved.items():
            if c == combo:
                r = Binds.reg.get(bid)
                if r is None: return
                store, key, on_click = r; store[1][key] = True; HOST.poke()
                if on_click is not None: on_click()
                return
    @staticmethod
    def arm(on=True):
        Binds.armed = bool(on)
        if on:
            Binds.armed_until = time.time() + Binds.ARM_SECS
            Kit.say("click a button to bind within %d s (Esc on the key window cancels)."
                       % int(Binds.ARM_SECS), Kit.HUE_INFO)
    @staticmethod
    def pick(bid):
        Binds.armed = False; Binds.picked = bid; Binds.answer = None; import System
        def ask():
            try: Binds.answer = str(API.RequestHotkey("Press the key for this button", 30) or "")
            except Exception: Binds.answer = ""
        t = System.Threading.Thread(System.Threading.ThreadStart(ask)); t.IsBackground = True; t.Start()
    @staticmethod
    def tick():
        if Binds.answer is None: return
        combo, Binds.answer = _norm_key(Binds.answer), None; bid, Binds.picked = Binds.picked, None
        if bid is None or not combo: return
        taken = next((row[1] for row in KeysPage.rows()
                      if row[0] == combo and not (row[1] == Binds.OWNER and Binds.saved.get(bid) == combo)), None)
        if taken is not None:
            Kit.say("%s is already %s's key; pick another." % (combo, taken), Kit.HUE_BAD); return
        old = Binds.saved.get(bid)
        if old: HOST.hotkey_drop(old, Binds.OWNER)
        Binds.saved[bid] = combo; Binds.hook(combo); Binds.save()
        Kit.say("%s bound." % combo, Kit.HUE_GOOD); HOST.refresh_settings(KEYS_PAGE)
    @staticmethod
    def clear():
        for combo in set(Binds.saved.values()): HOST.hotkey_drop(combo, Binds.OWNER)
        Binds.saved.clear(); Binds.save()


class KeysPage(_Page):
    ROW = 24
    @staticmethod
    def rows():
        out, seen = [], set()
        for combo, owner, what in list(HOST.hotkey_list):
            out.append((_norm_key(combo), owner, what)); seen.add((_norm_key(combo), owner))
        for combo, owner in list(HOST.hotkeys_owned.items()):
            if (_norm_key(combo), owner) not in seen: out.append((_norm_key(combo), str(owner), ""))
        for name, fn in list(HOST.services.items()):
            if not name.endswith(".hotkeys") or not callable(fn): continue
            s = HOST.by_key.get(name[:-len(".hotkeys")]); owner = s.title if s is not None else name[:-len(".hotkeys")]
            try: got = fn() or []
            except Exception: got = []
            for item in got:
                try: out.append((_norm_key(item[0]), owner, str(item[1])))
                except Exception: continue
        n = {}
        for combo, _, _ in out:
            if combo: n[combo] = n.get(combo, 0) + 1
        out = [(combo, owner, what, n.get(combo, 0) > 1) for combo, owner, what in out if combo]
        out.sort(key=lambda r: (r[0], r[1], r[2])); return out
    def height(self, w): return 64 + self.ROW * max(1, len(self.rows()))
    def build(self, g, x, y, w):
        self.store = ({}, {}); rows = self.rows(); h = 64 + self.ROW * max(1, len(rows))
        Kit.add_section(g, x, y, w, h, "HOTKEYS  (every key Virtue Assistant listens to)"); rx = x + w + 4
        for key, art, cap, dy, tip in (("refresh", Kit.ART_PAGE, "Refresh", 4, "Read the hotkeys again"),
                ("bind_clear", Kit.ART_CLOSE, "Clear binds", 28, "Unbind every button"),
                ("bind", Kit.ART_PLAY, "Bind a button", 28, "Click this, then a button in any window, then a key")):
            rx -= 16 + 35 + Kit.text_w(cap); Kit.art_button(g, self.store, key, art, rx, y + dy, cap, tip)
        clashes = len(set(r[0] for r in rows if r[3]))
        Kit.add_label(g, ("%s bound twice (shown in red)" % Kit.count(clashes, "key"))
                      if clashes else "No key is bound twice.", x + 12, y + 32,
                      Kit.HUE_BAD if clashes else Kit.HUE_INFO)
        if not rows: Kit.add_label(g, "No module that is on has a hotkey.", x + 12, y + 56, Kit.HUE_INFO)
        xo, xw = x + 12 + 160, x + 12 + 160 + 150
        for i, (combo, owner, what, clash) in enumerate(rows):
            ry = y + 56 + self.ROW * i; hue = Kit.HUE_BAD if clash else Kit.HUE_TEXT
            Kit.add_label(g, Kit.fit(combo, 150), x + 12, ry, hue)
            Kit.add_label(g, Kit.fit(owner, 140), xo, ry, hue if clash else Kit.HUE_TITLE)
            if what: Kit.add_label(g, Kit.fit(what, x + w - 16 - xw), xw, ry, Kit.HUE_INFO)
        self.c = True
    def poll(self):
        if self.c is not None and Kit.was_clicked(self.store, "refresh"): HOST.refresh_settings(KEYS_PAGE)
        if self.c is not None and Kit.was_clicked(self.store, "bind"): Binds.arm(True)
        if self.c is not None and Kit.was_clicked(self.store, "bind_clear"):
            Binds.clear(); HOST.refresh_settings(KEYS_PAGE)


ALERTS_PAGE, KEYS_PAGE = "va.alerts", "va.keys"


class WhatsNew(object):
    W = 520
    def __init__(self): self.g = None; self.store = ({}, {}); self.text = None
    def due(self):
        if self.text is None: self.text = whats_new()
        if not self.text: return False
        try: seen = API.GetPersistentVar(WHATS_NEW_KEY, "", API.PersistentVar.Account)
        except Exception: return False
        return str(seen or "") != APP_VERSION
    def open(self):
        if self.due(): Kit.on_client(self._build)
    def _build(self):
        M, W = Kit.MARGIN, self.W; lines = []
        for para in self.text: lines += Kit.wrap(para, W - 2 * M - 24) or [""]
        h_body = 16 + 20 * len(lines); H = M + 30 + Kit.GAP + h_body + M; self.store = ({}, {})
        g = G.CreateGump(True, True); Kit.add_window_frame(g, W, H); Kit.add_section(g, M, M, W - 2 * M, 30)
        Kit.add_label(g, "WHAT'S NEW IN %s %s" % (APP_NAME.upper(), APP_VERSION), M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, self.store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None, "Close (shown once per version)")
        yb = M + 30 + Kit.GAP; Kit.add_section(g, M, yb, W - 2 * M, h_body)
        for i, line in enumerate(lines): Kit.add_label(g, line, M + 12, yb + 8 + 20 * i, Kit.HUE_TEXT)
        sw, sh = Kit.screen(); Kit.place(g, max(0, ((sw or 1024) - W) // 2), max(0, ((sh or 768) - H) // 3), W, H)
        G.AddGump(g); self.g = g
    def poll(self):
        g = self.g
        if g is None: return
        if not Kit.is_open(g) or Kit.was_clicked(self.store, "close"): self.close(True)
    def close(self, seen=False):
        g, self.g = self.g, None; Kit.dispose(g)
        if seen: API.SavePersistentVar(WHATS_NEW_KEY, APP_VERSION, API.PersistentVar.Account)


class ModuleSlot(object):
    def __init__(self, key, title, desc, factory, interval):
        self.key = key; self.title = title; self.desc = desc; self.factory = factory; self.interval = interval
        self.api = self.lazy = self.broken = self.iv_fn = self.thread_want = None
        self.enabled = self.default_on = self.running = self.busy = self.pending_stop = False
        self.thread_due = self.on_client = self.has_thread = False
        self.category = "Other"; self.next_due = self.worst_ms = 0.0; self.errors = set(); self.error_count = 0
        self.parts = self.aliases = (); self.parts_on = {}; self.parts_running = set(); self.folded = True
    def part(self, key):
        for p in self.parts:
            if p[0] == key: return p
        return None
    def parts_wanted(self): return [p[0] for p in self.parts if self.parts_on.get(p[0])]
    def part_title(self, key):
        p = self.part(key); return "%s > %s" % (self.title, p[1]) if p is not None else self.title


class PartView(object):
    def __init__(self, key, slot, part):
        self.key = key; self.slot = slot; self.part = part; self.title = slot.part_title(part)
        self.category = slot.category
    @property
    def running(self): return bool(self.slot.running and self.part in self.slot.parts_running)
    @property
    def enabled(self): return bool(self.slot.enabled and self.slot.parts_on.get(self.part))
    @property
    def api(self): return self.slot.api
    @property
    def lazy(self): return self.slot.lazy
    @property
    def broken(self): return self.slot.broken


class _KeyMap(dict):
    def __init__(self, host): dict.__init__(self); self.host = host
    def view(self, key):
        slot, part = self.host.resolve(key); return PartView(key, slot, part) if part is not None else None
    def __contains__(self, key): return dict.__contains__(self, key) or self.view(key) is not None
    def get(self, key, default=None):
        if dict.__contains__(self, key): return dict.__getitem__(self, key)
        v = self.view(key); return v if v is not None else default
    def __getitem__(self, key):
        if dict.__contains__(self, key): return dict.__getitem__(self, key)
        v = self.view(key)
        if v is None: raise KeyError(key)
        return v


def _error_where():
    try:
        import sys; tb = sys.exc_info()[2]
        while tb is not None and tb.tb_next is not None: tb = tb.tb_next
        if tb is None: return ""
        where = safe(lambda: os.path.basename(str(tb.tb_frame.f_code.co_filename)), "") or ""
        if where.endswith("Module.py"): return " (%s line %d)" % (where, tb.tb_lineno)
        return " (line %d)" % tb.tb_lineno
    except Exception: return ""


class JLine(object):
    __slots__ = ("seq", "text", "low", "name", "hue", "ticks", "at", "kind")
    def __init__(self, seq, text, name, hue, ticks, at, kind):
        self.seq, self.text, self.low, self.name = seq, text, text.lower(), name
        self.hue, self.ticks, self.at, self.kind = hue, ticks, at, kind


class Journal(object):
    KEEP = 60.0; MAX_BACK = 30.0; lines = []; seen = {}; seq = 0; read_at = 0.0; pass_id = -1; zero_seen = False
    class Reader(object):
        __slots__ = ("last",)
        def __init__(self): self.last = Journal.seq
        def new(self, read=True):
            if read: Journal.update()
            last, self.last = self.last, Journal.seq
            if last >= Journal.seq: return []
            out = []
            for ln in reversed(Journal.lines):
                if ln.seq <= last: break
                out.append(ln)
            out.reverse(); return out
    @staticmethod
    def reader(): Journal.update(); return Journal.Reader()
    @staticmethod
    def update(force=False):
        pid = HOST.pass_id
        if pid == Journal.pass_id and not force: return
        Journal.pass_id = pid; now = time.time()
        back = min(Journal.MAX_BACK, max(1.0, now - Journal.read_at + 1.0)) if Journal.read_at else Journal.MAX_BACK
        Journal.read_at = now
        try: entries = list(API.GetJournalEntries(back) or [])
        except Exception: entries = []
        seen, fresh, zero, stopped, i = Journal.seen, [], [], False, len(entries) - 1
        while i >= 0:
            e = entries[i]; i -= 1; pos = i
            try:
                text = str(e.Text or "")
                if not text: continue
                try: ticks = int(e.Time.Ticks)
                except Exception: ticks = 0
                key = (ticks, text, str(e.Name or ""))
                if ticks == 0: zero.append((key, e, pos)); Journal.zero_seen = True; continue
                if stopped or key in seen:
                    if not Journal.zero_seen: break
                    stopped = True; continue
                fresh.append((key, e, pos))
            except Exception: continue
        if zero:
            total = {}
            for key, e, pos in zero: total[key] = total.get(key, 0) + 1
            kept = {}; ws = now - back
            for ln in reversed(Journal.lines):
                if ln.at < ws: break
                if ln.ticks == 0: k = (0, ln.text, ln.name); kept[k] = kept.get(k, 0) + 1
            rank = {}
            for key, e, pos in zero:
                r = rank.get(key, 0); rank[key] = r + 1
                if r < total[key] - kept.get(key, 0): fresh.append((key, e, pos))
            fresh.sort(key=lambda t: t[2])
        else: fresh.reverse()
        added = {}
        for key, e, pos in fresh:
            if key[0] != 0:
                if key in added: continue
                added[key] = 1
            try:
                Journal.seq += 1; seen[key] = Journal.seq
                Journal.lines.append(JLine(Journal.seq, key[1], key[2], int(e.Hue or 0), key[0], now,
                                           str(e.TextType or "")))
            except Exception: continue
        cut = now - Journal.KEEP; lines = Journal.lines
        if lines and lines[0].at < cut:
            i = 0
            while i < len(lines) and lines[i].at < cut:
                ln = lines[i]; seen.pop((ln.ticks, ln.text, ln.name), None); i += 1
            del lines[:i]
    @staticmethod
    def since(t):
        Journal.update(); out = []
        for ln in reversed(Journal.lines):
            if ln.at < t: break
            out.append(ln)
        out.reverse(); return out
    @staticmethod
    def recent(secs): return Journal.since(time.time() - secs)
    @staticmethod
    def find(t, texts):
        if isinstance(texts, str): texts = (texts,)
        low = [x.lower() for x in texts]
        for ln in Journal.since(t):
            for x in low:
                if x in ln.low: return ln
        return None


class Picker(object):
    jobs = []; cuo = None; neutral = None; looked = False; CURSOR_TARGET = 6983686
    @staticmethod
    def _tm():
        if not Picker.looked:
            Picker.looked = True
            try:
                import clr; clr.AddReference(API.GetType().Assembly); from ClassicUO import Client as CUO
                from ClassicUO.Game.Managers import TargetType; Picker.cuo, Picker.neutral = CUO, TargetType.Neutral
            except Exception: Picker.cuo = None
        if Picker.cuo is None: return None
        try: return Picker.cuo.Game.UO.World.TargetManager
        except Exception: return None
    @staticmethod
    def ask(timeout, fn, owner=None):
        for j in Picker.jobs: j["cancel"] = True
        if owner is None: owner = HOST.owner_key()
        Picker.jobs.append({"t": float(timeout), "fn": fn, "until": 0.0, "d": None,
                            "got": None, "block": False, "cancel": False, "owner": owner})
        HOST.poke()
    @staticmethod
    def _done(j, serial):
        if j in Picker.jobs: Picker.jobs.remove(j)
        try: j["fn"](int(serial or 0))
        except Exception as ex: Kit.say("target error: %s%s" % (ex, _error_where()), Kit.HUE_BAD)
    @staticmethod
    def tick():
        if not Picker.jobs: return
        tm = Picker._tm()
        for j in list(Picker.jobs):
            if j["block"]: continue
            if j["d"] is None:
                if j["cancel"]: Picker._done(j, 0); continue
                if tm is None: j["block"] = True; continue
                try:
                    from System import Action
                    def got(obj, j=j):
                        try: j["got"] = (int(getattr(obj, "Serial", 0) or 0) if obj is not None else 0)
                        except Exception: j["got"] = 0
                    j["d"] = Action[object](got); tm.SetTargeting(j["d"], Picker.CURSOR_TARGET, Picker.neutral)
                    j["until"] = time.time() + j["t"]
                except Exception: j["d"], j["block"] = None, True
                continue
            if j["got"] is not None: Picker._done(j, j["got"]); continue
            try: cur = bool(tm.IsCurrentTargetingAction(j["d"]))
            except Exception: cur = False
            if not cur: Picker._done(j, 0)
            elif j["cancel"] or time.time() >= j["until"]:
                try: tm.CancelTarget()
                except Exception: pass
                Picker._done(j, 0)
    @staticmethod
    def drop(owner=None):
        mine = [j for j in Picker.jobs if owner is None or j.get("owner") == owner]
        if not mine: return
        for j in mine: Picker.jobs.remove(j)
        tm = Picker._tm(); up = [j["d"] for j in mine if j["d"] is not None and j["got"] is None]
        if tm is not None and up:
            def take_down():
                for d in up:
                    if tm.IsCurrentTargetingAction(d): tm.CancelTarget()
            safe(lambda: Kit.on_client(take_down, fallback=False))
        for j in mine: Picker._done(j, 0)
    @staticmethod
    def run_blocking():
        for j in [j for j in Picker.jobs if j["block"]]:
            Picker.jobs.remove(j); serial = 0 if j["cancel"] else int(safe(lambda: API.RequestTarget(j["t"]), 0) or 0)
            Picker._done(j, serial)


def _first(e): return e[0]


class _Memo(object):
    def __init__(self, raw): self.__dict__["raw"] = raw
    def __getattr__(self, name): v = getattr(self.__dict__["raw"], name); self.__dict__[name] = v; return v
    def __setattr__(self, name, value): setattr(self.__dict__["raw"], name, value); self.__dict__.pop(name, None)
    def __int__(self): return int(self.__dict__["raw"].Serial)


class Host(object):
    def __init__(self):
        self.slots = []; self.by_key = _KeyMap(self); self.old_map = {}
        self.cur_part = self.cur_owner = self.config = self.hub = self.grid = self.profile_req = self.alone = None
        self.hurt_hp = self._me = self._want_raw = None; self.stack = []
        self.quitting = self.shut = self.ui_busy = self.poked = self.prefs_frozen = False
        self.in_hop = self.pass_poked = False; self.alive_at = 0.0
        self.ui_next = self.dock_next = self._claim_len = self.hurt_until = self.hurt_at = self.input_at = 0.0
        self.docks = []; self.services = {}; self.hotkeys_owned = {}; self.prefs = {}; self.cursor_claim = (None, 0.0)
        self.foe_seen = (0.0, None); self.client_idles = self.pass_id = 0
        self._me_pid = self._mob_pid = self._one_pid = -1; self._mob_list = (); self._one = {}; self._pack = {}
        self.active = []; self.client_run = []; self._pass_fn = self._client_pass; self._want_set = frozenset()
        self.told, self._zone_held, self._zone_was_d = set(), set(), None
        self.load_jobs = []; self.hotkey_list = []; self.pages = []
        for key, title, page in ((ALERTS_PAGE, "Alerts", AlertsPage()), (KEYS_PAGE, "Keys", KeysPage()),
                                 (LAYOUT_PAGE, "Layout", LayoutPage())):
            s = ModuleSlot(key, title, "", None, 1.0); s.api = page.api(); self.pages.append(s)
        self.whats_new = WhatsNew()
    def _tell(self, msg):
        if msg in self.told: return
        if len(self.told) > 50: self.told.clear()
        self.told.add(msg); API.SysMsg(msg, Kit.HUE_BAD)
    def _refresh_active(self):
        act = [s for s in self.slots if s.running]; self.active = act; self.client_run = [s for s in act if s.on_client]
    def poke(self): self.poked = True; self.input_at = time.time()
    INPUT_FAST = 1.0; PAGE_EVERY = 0.25
    def poll_due(self, gate, every=None):
        now = time.time()
        if every is not None and every <= UI_TICK: return True
        if not Kit.clicks_seen: return True
        fast = now - self.input_at <= self.INPUT_FAST or 0 <= gate[0] - now > 2.0
        if not fast:
            p = SNAP.pressed()
            if p is not False:
                if p: self.input_at = now
                fast = True
            else: fast = Client.typing()
        if fast or now >= gate[0]: gate[0] = now + (every if every is not None else self.PAGE_EVERY); return True
        return False
    def alert_kind(self, key, label, default_sound=None):
        s = self.current(); return ALERTS.kind(key, label, default_sound, s.title if s is not None else APP_NAME)
    def alert(self, key, text, level="warn", sound=None, ping=None, who=None):
        s = self.current()
        return ALERTS.raise_(key, text, level, sound, ping, who, s.title if s is not None else APP_NAME)
    def guarded(self): return GUARD.guarded()
    def guard_area(self): return GUARD.area()
    def hotkey_note(self, combo, owner, what=""):
        k = _norm_key(combo)
        self.hotkey_list = [e for e in self.hotkey_list if not (_norm_key(e[0]) == k and e[1] == owner)]
        self.hotkey_list.append((k, str(owner), str(what or "")))
        if k not in self.hotkeys_owned: self.hotkeys_owned[k] = str(owner)
    def hotkey_drop(self, combo, owner=None):
        k = _norm_key(combo)
        self.hotkey_list = [e for e in self.hotkey_list
                            if not (_norm_key(e[0]) == k and (owner is None or e[1] == owner))]
        left = [e[1] for e in self.hotkey_list if _norm_key(e[0]) == k]; cur = self.hotkeys_owned.get(k)
        if cur is None or owner is None or cur == str(owner):
            if left: self.hotkeys_owned[k] = left[0]
            else: self.hotkeys_owned.pop(k, None)
    def page_slot(self, key):
        s = self.resolve(key)[0]
        if s is None: return next((p for p in self.pages if p.key == key), None)
        return s
    def resolve(self, key):
        s = dict.get(self.by_key, key)
        if s is not None: return s, None
        m = self.old_map.get(key)
        if m is None and "." in str(key): m = str(key).split(".", 1)
        if m is not None:
            s = dict.get(self.by_key, m[0])
            if s is not None and s.part(m[1]) is not None: return s, m[1]
        return None, None
    def _note_parts(self, s, default_on, category, parts, aliases):
        s.default_on = bool(default_on); s.category = str(category or "Other")
        s.parts = tuple(tuple(p) for p in (parts or ())); s.aliases = tuple(str(a) for a in (aliases or ()))
        for p in s.parts:
            for old in (p[4] if len(p) > 4 else ()): self.old_map[str(old)] = (s.key, p[0])
            if p[0] not in s.parts_on: s.parts_on[p[0]] = False
    def part_on(self, part, module=None):
        if module is None: cur = self.current(); module = cur.key if cur is not None else None
        s = dict.get(self.by_key, module); return bool(s is not None and s.parts_on.get(part))
    def owner_key(self):
        cur = self.current()
        if cur is None: return None
        if self.cur_owner is not None and cur.parts: return self.cur_owner
        return cur.key
    def _parts_fill(self, s):
        if s.parts and not s.parts_wanted():
            for p in [p[0] for p in s.parts if p[3]] or [s.parts[0][0]]: s.parts_on[p] = True
    def _part_notify(self, s):
        if not s.running or s.api is None or not s.api.get("parts"): return
        was = s.busy; self._enter(s)
        try: want = set(s.parts_wanted()); Kit.on_client(lambda: s.api["parts"](want))
        except Exception as ex: self.report(s, ex)
        finally: self._leave(s); s.busy = was
    def part_set(self, module, part, on):
        s = dict.get(self.by_key, module)
        if s is None or s.part(part) is None: return
        on = bool(on)
        if s.parts_on.get(part) == on:
            if on and not s.enabled: self.enable(module)
            return
        s.parts_on[part] = on
        if on and not s.enabled: self.enable(module)
        elif not on and not s.parts_wanted(): self.disable(module)
        else: self.save_prefs(); self._part_notify(s)
        self.refresh_settings(module)
    def alarm_up(self): return bool(ALERTS.shown and ALERTS.alarm)
    def typing(self): return Client.typing()
    def release_typing(self): Typing.release()
    def grid_size(self): return max(8, min(512, self.pref_int("grid", GRID_DEFAULT)))
    def grid_shown(self): return self.grid is not None and self.grid.shown
    def grid_toggle(self):
        if self.grid is not None:
            self.grid.toggle(); self.prefs["grid_on"] = "1" if self.grid_shown() else "0"; self.save_prefs()
        return self.grid_shown()
    def dock_wanted(self, key): return key in self._dock_want()
    def _dock_want(self):
        raw = self.prefs.get("dock_want", "") or ""
        if raw != self._want_raw: self._want_raw = raw; self._want_set = frozenset(k for k in str(raw).split(",") if k)
        return self._want_set
    def dock_want_set(self, key, on):
        want = self._dock_want()
        if bool(on) == (key in want): return
        self.prefs["dock_want"] = ",".join(sorted(want | {key} if on else want - {key})); self.save_prefs()
    def dock_forget(self, key): self.dock_want_set(key, False)
    def dock_to_bar(self, key, title=None):
        if LAYOUT.holds(key): return False
        self.dock_want_set(key, True); d = dict(self.docks).get(key); alive = self.bar_alive()
        if d is not None:
            fn = d.get("dock") if alive else (d.get("minimize") or d.get("dock"))
            if fn: safe(fn)
            title = title or d.get("title")
        if not alive: self.dock_note(title or key)
        self.dock_next = 0.0; return alive
    def dock_note(self, title):
        API.SysMsg("%s: minimized until the Action Bar opens; then it folds into its tray." % title, Kit.HUE_INFO)
    def dock_add(self, key, hooks):
        self.dock_remove(key); self.docks.append((key, hooks))
        gump = hooks.get("gump")
        if gump is not None: self.layout_add(key, gump, hooks.get("title"), hooks)
    def dock_remove(self, key): self.docks = [d for d in self.docks if d[0] != key]; self.layout_remove(key)
    def layout_add(self, key, get_gump, title=None, hooks=None):
        cur = self.current(); owner = (cur.key, self.cur_part if cur.parts else None) if cur is not None else None
        LAYOUT.add(key, get_gump, title, hooks, owner)
    def layout_remove(self, key): LAYOUT.remove(key)
    def layout_slot(self, key):
        key = str(key)
        if not LAYOUT.holds(key): return None
        rec = LAYOUT.fitted.get(key)
        if rec is not None and rec.get("told") is not None: return rec["told"]
        slot = LAYOUT.placed.get(key); return (slot[2], slot[3]) if slot is not None else None
    def layout_rect(self, key):
        key = str(key)
        if not LAYOUT.holds(key): return None
        slot = LAYOUT.placed.get(key); return tuple(slot) if slot is not None else None
    def layout_holds(self, key): return LAYOUT.holds(key)
    def layout_need(self, key, w=None, h=None): LAYOUT.need(key, w, h)
    def layout_base(self, key): return LAYOUT.zone_base(key)
    def layout_locked(self, key): return LAYOUT.locked(key)
    def layout_arrange(self, on=None): LAYOUT.set_arrange((not LAYOUT.arrange) if on is None else on)
    def layout_arranging(self): return LAYOUT.arrange
    def layout_in_use(self): return bool(LAYOUT.assign)
    def layout_pair(self, top_key, bottom_key): return LAYOUT.pair_below(top_key, bottom_key)
    def layout_refit(self): LAYOUT.dirty = LAYOUT.fresh = True
    @staticmethod
    def suite_alive():
        try: return time.time() - float(API.GetSharedVar(ALIVE_KEY) or 0) < 3.0
        except Exception: return False
    def bar_alive(self):
        if VA_ALONE: return False
        try: alive = float(API.GetSharedVar(ConfigWindow.LINK_ALIVE) or 0)
        except Exception: alive = 0.0
        return time.time() - alive <= ConfigWindow.LINK_STALE
    def dock_tick(self):
        now = time.time()
        if now < self.dock_next and self.dock_next - now <= 0.25: return
        self.dock_next = now + 0.25; Binds.load(); Binds.tick(); want = self._dock_want(); fold, unfold = [], []
        self.zone_up_tick()
        for k, d in self.docks:
            if LAYOUT.holds(k): continue
            try: s = d["state"]()
            except Exception: s = None
            if s == "docked":
                if k not in want: self.dock_want_set(k, True)
                unfold.append(d)
            elif s == "open":
                if k in want: self.dock_want_set(k, False)
            elif s == "minimized" and k in want: fold.append(d)
        if not fold and not unfold: return
        if self.bar_alive():
            for d in fold: safe(d.get("dock"))
        else:
            for d in unfold: safe(d.get("undock"))
    ZONE_WAS_VAR = "Layout_zone_was"
    def _zone_was(self):
        d = self._zone_was_d
        if d is None:
            d = self._zone_was_d = dict(p.split("=", 1) for p in Kit.get_var(self.ZONE_WAS_VAR).split(",") if "=" in p)
        return d
    def _zone_was_save(self):
        Kit.put_var(self.ZONE_WAS_VAR, ",".join("%s=%s" % kv for kv in sorted(self._zone_was_d.items())))
    def zone_up_tick(self):
        if VA_ALONE: return
        held, was = self._zone_held, self._zone_was()
        for k, d in self.docks:
            on = LAYOUT.holds(k); changed = on != (k in held)
            if changed:
                if on: held.add(k)
                else: held.discard(k)
            try: s = d["state"]() if (on or k in was) else None
            except Exception: s = None
            if on and s in ("minimized", "docked"):
                if k not in was: was[k] = "d" if (s == "docked" or self.dock_wanted(k)) else "m"; self._zone_was_save()
                safe(d.get("show")); continue
            if not on and k in was and s is not None:
                v = was.pop(k); self._zone_was_save()
                if v == "d": self.dock_to_bar(k, d.get("title"))
                else: safe(d.get("minimize"))
                continue
            if changed and d.get("redraw") is not None and s != "docked": safe(d.get("redraw"))
    TWICE = "%s: %s loaded twice (module key \"%s\"); skipped the second copy."
    def add(self, key, title, desc, factory, interval, default_on=False, category=None, parts=(), aliases=()):
        s = dict.get(self.by_key, key)
        if s is not None and s.lazy is not None:
            s.lazy = None; s.title, s.desc, s.factory, s.interval = title, desc, factory, interval
            self._note_parts(s, default_on, category, parts, aliases)
        elif s is not None: API.SysMsg(self.TWICE % (APP_NAME, title, key), Kit.HUE_BAD); return s
        else:
            s = ModuleSlot(key, title, desc, factory, interval)
            self._note_parts(s, default_on, category, parts, aliases); self.slots.append(s); self.by_key[key] = s
        try: s.api = factory()
        except Exception as ex:
            s.broken = str(ex) + _error_where(); Kit.say("%s could not be loaded: %s" % (title, s.broken), Kit.HUE_BAD)
        self._arm(s)
        if VA_ALONE and self.alone is None: self.run_alone(s)
        return s
    @staticmethod
    def _arm(s):
        api = s.api; s.on_client = bool(api and api.get("client_tick")); s.iv_fn = api.get("interval") if api else None
        s.has_thread = bool(api) and "thread_tick" in api; s.thread_want = api.get("thread_wanted") if api else None
    def add_lazy(self, key, title, desc, path, interval, default_on=False, category=None, parts=(), aliases=()):
        if dict.__contains__(self.by_key, key): return dict.__getitem__(self.by_key, key)
        s = ModuleSlot(key, title, desc, None, interval); self._note_parts(s, default_on, category, parts, aliases)
        s.lazy = path; self.slots.append(s); self.by_key[key] = s; return s
    def request_load(self, s):
        if s is None or s.lazy is None: return False
        if s not in self.load_jobs: self.load_jobs.append(s)
        self.poke(); return True
    def _run_load_jobs(self):
        if not self.load_jobs or self.stack: return
        s = self.load_jobs.pop(0); ok = self.load(s)
        if ok and s.enabled and not s.running and not s.pending_stop: self.start(s)
        elif not ok and s.enabled: s.enabled = False; self.save_prefs()
        if self.config is not None: self.config.loaded(s.key)
    def load(self, s):
        if s is None: return False
        if s.lazy is not None:
            path = s.lazy
            try:
                code = compile(_read_text(path), path, "exec"); exec(code, globals())
                if s.lazy is not None: raise Exception("the file's HOST.add line didn't run")
            except Exception as ex:
                s.lazy = None; line = getattr(ex, "lineno", None)
                where = (" (%s line %s)" % (os.path.basename(path), line)) if line else _error_where()
                s.api, s.broken = None, "%s%s" % (getattr(ex, "msg", None) or ex, where)
                Kit.say("%s could not be loaded: %s" % (s.title, s.broken), Kit.HUE_BAD)
        return s.api is not None
    def current(self): return self.stack[-1] if self.stack else None
    def stopping(self):
        if self.quitting: return True
        try: return bool(API.StopRequested)
        except Exception: return True
    def aborting(self):
        if self.stopping(): return True
        if self.client_idles > 1 and Client.on_client_thread(): return True
        s = self.current(); return s is not None and (s.pending_stop or not s.enabled)
    def idle(self, seconds):
        if Client.on_client_thread():
            self.client_idles += 1; return self.client_idles <= 1 and not self.aborting()
        end = time.time() + max(0.0, seconds)
        while not API.StopRequested:
            if self.aborting(): return False
            safe(API.ProcessCallbacks); self.run_due()
            if self.aborting(): return False
            rem = end - time.time()
            if rem <= 0 or rem > seconds + 1.0: return True
            API.Pause(min(HOST_TICK, rem))
        return False
    def _enter(self, s): s.busy = True; self.stack.append(s)
    def _leave(self, s):
        stack = self.stack
        if stack and stack[-1] is s: stack.pop()
        elif s in stack: stack.remove(s)
        s.busy = False
    def report(self, s, ex, what=None, part=None):
        msg = str(ex) + _error_where(); s.error_count += 1
        if msg not in s.errors:
            s.errors.add(msg); Kit.say("%s error (still running): %s" % (what or s.title, msg), Kit.HUE_BAD)
        if s.error_count >= 25 and s.enabled:
            Kit.say("%s kept failing and was switched off." % (what or s.title), Kit.HUE_BAD)
            if part is not None and s.parts and s.parts_on.get(part): self.part_set(s.key, part, False)
            else: self.disable(s.key)
            if s.enabled: s.error_count = 0
    def start(self, s):
        if s.running or self.stopping() or not self.load(s): return
        if self.config is not None: self.config.forget_measure(s.key)
        s.errors, s.error_count = set(), 0; s.pending_stop = False; self._enter(s)
        try:
            s.running = True; self._arm(s); self._refresh_active(); self.client_idles = 0; Kit.on_client(s.api["start"])
        except Exception as ex:
            s.running = False; msg = str(ex) + _error_where()
            Kit.say("%s could not start: %s" % (s.title, msg), Kit.HUE_BAD)
            safe(lambda: s.api["stop"]()); s.enabled = False; self.save_prefs()
        finally: self._leave(s); self._refresh_active()
        s.next_due = 0.0
    def _stop(self, s):
        s.pending_stop = False
        if not s.running: return
        if self.config is not None: self.config.forget_measure(s.key)
        olds = [s.key] + [old for p in s.parts for old in p[4]]
        for k in olds + [p[0] for p in s.parts]: Picker.drop(k)
        if self.cursor_claim[0] in olds: self.cursor_claim = (None, 0.0)
        self._enter(s)
        try: s.api["stop"]()
        except Exception: pass
        finally: s.running = False; self._leave(s); self._refresh_active()
    def tick(self, s, hook="tick"):
        s.busy = True; stack = self.stack; stack.append(s); self.client_idles = 0; t0 = time.time()
        try: s.api[hook]()
        except Exception as ex:
            if not self.stopping(): self.report(s, ex)
        finally:
            if stack and stack[-1] is s: stack.pop()
            elif s in stack: stack.remove(s)
            s.busy = False; t1 = time.time(); ms = (t1 - t0) * 1000.0; decayed = s.worst_ms * 0.98
            s.worst_ms = ms if ms > decayed else decayed
        if hook == "tick":
            s.next_due = t1 + Host._ask(s.iv_fn, s.interval)
            s.thread_due = s.has_thread and Host._ask(s.thread_want, True, bool)
        if s.pending_stop: self._stop(s)
    @staticmethod
    def _ask(fn, default, cast=None):
        if fn is None: return default
        try: v = fn(); return cast(v) if cast else (v or default)
        except Exception: return default
    def enable(self, key):
        s, part = self.resolve(key)
        if s is None: return
        if part is not None: self.part_set(s.key, part, True); return
        self._parts_fill(s)
        if s.lazy is not None and Client.on_client_thread():
            s.enabled = True; self.save_prefs(); self.request_load(s); return
        if not self.load(s): return
        s.enabled = True
        if s.running and s.pending_stop: s.pending_stop = False
        self.save_prefs(); self.start(s)
    def show_settings(self, key):
        if self.config is not None: self.config.show_settings(key)
    def refresh_settings(self, key):
        if self.config is not None: s, _part = self.resolve(key); self.config.refresh(s.key if s is not None else key)
    def disable(self, key):
        s, part = self.resolve(key)
        if s is None: return
        if self.shut or self.stopping(): return
        if part is None and s.parts and self.cur_part is not None and self.current() is s \
                and s.parts_on.get(self.cur_part):
            part = self.cur_part
        if part is not None: self.part_set(s.key, part, False); return
        s.enabled = False; self.save_prefs()
        if s.running:
            s.pending_stop = True
            if not s.busy: self._stop(s)
    def run_due(self):
        if self.shut: return
        if self.profile_req is not None and not self.stack:
            req, self.profile_req = self.profile_req, None; self.profile_job(req); return
        if self.load_jobs and not self.stack: self._run_load_jobs()
        poked, self.poked = self.poked, False; self.pass_id += 1
        if poked: self.ui_next = 0.0
        now = time.time()
        if poked or self._client_due(now):
            self.pass_poked = poked
            try: Kit.on_client(self._pass_fn)
            except Exception as ex:
                if not self.stopping(): self._tell("%s: pass error: %s" % (APP_NAME, ex))
            now = time.time()
        if Picker.jobs: Picker.run_blocking()
        for s in self.active:
            if s.pending_stop:
                if s.busy: continue
                self._stop(s)
            elif s.busy or not s.running: continue
            elif not s.on_client and (poked or now >= s.next_due or s.next_due - now > self.CLOCK_BACK): self.tick(s)
            elif s.thread_due: s.thread_due = False; self.tick(s, "thread_tick")
            else: continue
            if self.stopping(): return
            try: API.ProcessCallbacks()
            except Exception: pass
        cfg = self.config
        if cfg is not None and cfg.prof_stale and not self.stack: cfg.refresh_profiles()
    LOOKAHEAD = HOST_TICK + 0.035; CLOCK_BACK = 60.0; EARLY = 0.008
    def _client_due(self, now):
        if now >= self.ui_next or Kit.pending or Picker.jobs: return True
        if self.ui_next - now > 1.0: self.ui_next = now; return True
        soon = now + self.LOOKAHEAD
        for s in self.client_run:
            if soon >= s.next_due: return True
            if s.next_due - now > self.CLOCK_BACK: s.next_due = now; return True
        return False
    def _client_pass(self, poked=None):
        self.in_hop = True
        try:
            if poked is None: poked = self.pass_poked
            self.client_idles = 0
            if Kit._texts_sweep: Kit._prune_texts()
            self.ui_tick()
            if Picker.jobs:
                try: Picker.tick()
                except Exception as ex: self._tell("%s: target cursor error: %s" % (APP_NAME, ex))
            now = time.time()
            for s in self.client_run:
                if s.running and not s.busy and not s.pending_stop and (
                        poked or now + self.EARLY >= s.next_due or s.next_due - now > self.CLOCK_BACK):
                    self.tick(s)
                    if self.stopping(): return
            if ALERTS.pending:
                try: ALERTS.tick(time.time())
                except Exception as ex: self._tell("%s: alert error: %s%s" % (APP_NAME, ex, _error_where()))
        finally: self.in_hop = False
    def claim_cursor(self, key, seconds):
        self._claim_len = max(0.0, seconds); self.cursor_claim = (key, time.time() + self._claim_len)
    def release_cursor(self, key):
        if self.cursor_claim[0] == key: self.cursor_claim = (None, 0.0)
    def cursor_busy(self, key=None):
        if Picker.jobs: return "pick"
        owner, until = self.cursor_claim
        return owner if owner is not None and owner != key and \
            0 < until - time.time() <= self._claim_len + 0.05 else None
    def cursor_ok(self, key, kind="any"):
        if self.cursor_busy(key) is not None: return False
        try: return bool(API.HasTarget(kind))
        except Exception: return False
    def guard_hold(self):
        try: g = GUARD.guarded()
        except Exception: g = None
        return "guard" if g is True else "unknown" if g is None else None
    def foe_near(self):
        now = time.time(); at, name = self.foe_seen
        if 0 <= at - now <= FOE_EVERY: return name
        def look():
            try: me = int(self.me().Serial)
            except Exception: me = 0
            try:
                for m in self.mobiles(FOE_RANGE):
                    try:
                        if int(m.Serial) == me or m.IsRenamable: continue
                        n = int(m.Notoriety)
                        if n in FOE_NOTO or (n in FOE_WAR_NOTO and m.InWarMode): return str(m.Name or "") or "?"
                    except Exception: continue
            except Exception: pass
            return None
        try: name = Kit.on_client(look)
        except Exception: name = None
        self.foe_seen = (now + FOE_EVERY, name); return name
    def fight_hold(self, now=None):
        if now is None: now = time.time()
        dead = war = False
        try: p = self.me(); dead = bool(p.IsDead); war = bool(p.InWarMode); hits = int(p.Hits)
        except Exception: hits = None
        if hits is not None:
            if (self.hurt_hp is not None and hits < self.hurt_hp and 0 <= now - self.hurt_at <= 2.0):
                self.hurt_until = now + HURT_SECS
            self.hurt_hp = hits; self.hurt_at = now
        if dead: return "dead"
        if war: return "war"
        if 0 < self.hurt_until - now <= HURT_SECS: return "hurt"
        if self.foe_near(): return "foe"
        if Kit.held_item(): return "item"
        up = self.services.get("attention.up")
        if up is not None and safe(up): return "alarm"
        return None
    def me(self):
        if self.in_hop and self._me_pid == self.pass_id: return self._me
        try: p = API.Player
        except Exception: p = None
        m = _Memo(p) if p is not None else None
        if self.in_hop: self._me_pid = self.pass_id; self._me = m
        return m
    def _mob_scan(self):
        if self.in_hop and self._mob_pid == self.pass_id: return self._mob_list
        out = []; byser = None
        if self.in_hop:
            if self._one_pid != self.pass_id: self._one = {}; self._one_pid = self.pass_id
            byser = self._one
        try: raw = API.GetAllMobiles() or ()
        except Exception: raw = ()
        for r in raw:
            try:
                d = r.Distance; m = _Memo(r); m.__dict__["Distance"] = d; out.append((d, m))
                if byser is not None: byser[int(r.Serial)] = m
            except Exception: continue
        if self.in_hop: self._mob_pid = self.pass_id; self._mob_list = out
        return out
    def mobiles(self, distance=None):
        lst = self._mob_scan()
        if distance is None: return [e[1] for e in lst]
        return [m for d, m in lst if d <= distance]
    def mobile(self, serial):
        try: k = int(serial)
        except Exception: return None
        if self.in_hop:
            if self._one_pid != self.pass_id: self._one = {}; self._one_pid = self.pass_id
            one = self._one
            if k in one: return one[k]
        try: r = API.FindMobile(k)
        except Exception: r = None
        m = _Memo(r) if r is not None else None
        if self.in_hop: self._one[k] = m
        return m
    def pack_items(self, deep=True, max_age=0.0):
        k = bool(deep); now = time.time(); ent = self._pack.get(k)
        if ent is not None and ((self.in_hop and ent[0] == self.pass_id)
                                or (max_age > 0 and 0 <= now - ent[1] <= max_age)):
            return list(ent[2])
        bp = API.Backpack; lst = list(API.ItemsInContainer(bp, k) or []) if bp else []
        self._pack[k] = (self.pass_id if self.in_hop else -1, now, lst); return list(lst)
    def pack_dirty(self): self._pack.clear()
    def pick_target(self, timeout, on_done, owner=None): Picker.ask(timeout, on_done, owner)
    def ui_tick(self):
        if self.ui_busy or self.config is None: return
        self.ui_busy = True
        try:
            while Kit.pending:
                lst, Kit.pending = Kit.pending, []
                for fn in lst: safe(fn)
            now = time.time()
            if now >= self.ui_next:
                self.ui_next = now + UI_TICK; self.config.poll()
                if not VA_ALONE and now >= self.alive_at:
                    self.alive_at = now + 1.0; API.SetSharedVar(ALIVE_KEY, str(now))
                if self.hub is not None: self.hub.poll()
                self.dock_tick(); SNAP.tick()
                if self.grid is not None: self.grid.tick()
                LAYOUT.poll()
                try: ALERTS.tick(now)
                except Exception as ex: self._tell("%s: alert error: %s%s" % (APP_NAME, ex, _error_where()))
                try: GUARD.tick(now)
                except Exception as ex: self._tell("%s: guard-zone error: %s%s" % (APP_NAME, ex, _error_where()))
                if self.whats_new.g is not None: self.whats_new.poll()
        except Exception as ex:
            msg = "%s: settings window error: %s%s" % (APP_NAME, ex, _error_where())
            if not self.stopping(): self._tell(msg)
        finally: self.ui_busy = False
    def load_prefs(self):
        prefs = self.prefs = Kit.codec_load(Kit.get_var(SETTINGS_KEY))
        on = [k for k in prefs.get("modules", "").split(",") if k]
        seen = set(k for k in prefs.get("seen", "").split(",") if k); was = prefs.get("seen", "")
        changed = self._migrate_parts(prefs, on, seen)
        for s in self.slots:
            if s.default_on and s.key not in seen: on.append(s.key); seen.add(s.key); self._parts_fill(s)
            s.enabled = s.key in on and (s.api is not None or s.lazy is not None)
            if s.enabled: self._parts_fill(s)
        prefs["seen"] = ",".join(sorted(seen))
        if prefs["seen"] != was or changed: self.save_prefs()
    def _migrate_parts(self, prefs, on, seen):
        def by_module(key):
            out = {}
            for item in prefs.get(key, "").split(","):
                if "." in item: mk, pk = item.split(".", 1); out.setdefault(mk, set()).add(pk)
            return out
        saved, saved_off = by_module("parts"), by_module("parts_off")
        fresh = "parts" not in prefs or prefs.get("parts_from", "") != prefs.get("modules", ""); on_set = set(on)
        changed = False
        for s in self.slots:
            if not s.parts: continue
            mine = saved.get(s.key); off = saved_off.get(s.key)
            if mine is None and off is not None and s.key not in on_set \
                    and not any(k in on_set for p in s.parts for k in p[4]):
                for p in s.parts: s.parts_on[p[0]] = p[0] in off
                continue
            if mine is not None and not fresh:
                for p in s.parts:
                    s.parts_on[p[0]] = p[0] in mine
                    if len(p) > 5 and p[5] and p[0] not in mine and p[3]:
                        new_seen = str(Kit.get_var("VirtueAssistant_new_parts", "") or "").split(",")
                        if p[0] not in new_seen:
                            if not VA_ALONE:
                                Kit.put_var("VirtueAssistant_new_parts", ",".join([x for x in new_seen if x] + [p[0]]))
                            s.parts_on[p[0]] = True; changed = True
            else:
                olds = [k for p in s.parts for k in p[4]]
                had_old = any(k in on_set for k in olds) or (s.key in on_set and not olds)
                for p in s.parts:
                    if p[4]: s.parts_on[p[0]] = any(k in on_set for k in p[4])
                    elif mine is not None: s.parts_on[p[0]] = p[0] in mine
                    else: s.parts_on[p[0]] = bool(p[3]) and not had_old and s.key not in on_set
                if s.key in on_set: self._parts_fill(s)
                changed = True
                if any(k in seen for k in olds) and s.key not in seen: seen.add(s.key)
            if s.parts_wanted():
                if s.key not in on_set: on.append(s.key); on_set.add(s.key)
            elif s.key in on_set: on.remove(s.key); on_set.discard(s.key)
        return changed
    def pref_int(self, key, default):
        try: return int(self.prefs.get(key, default))
        except Exception: return default
    def save_prefs(self):
        if self.config is not None: self.config.box_hit = True
        if self.prefs_frozen: return None
        mods, parts, off = [], [], []
        for s in self.slots:
            if not s.enabled:
                for p in s.parts:
                    if s.parts_on.get(p[0]): off.append("%s.%s" % (s.key, p[0]))
                continue
            mods.append(s.key)
            for p in s.parts:
                if s.parts_on.get(p[0]):
                    parts.append("%s.%s" % (s.key, p[0]))
                    for old in p[4]:
                        if old not in mods: mods.append(old)
        self.prefs["modules"] = ",".join(mods); self.prefs["parts"] = ",".join(parts)
        self.prefs["parts_from"] = self.prefs["modules"]
        if off: self.prefs["parts_off"] = ",".join(off)
        else: self.prefs.pop("parts_off", None)
        if self.config is not None: self.config.store_prefs(self.prefs)
        if self.hub is not None: self.hub.store_prefs(self.prefs)
        data = ";".join("%s=%s" % (k, v) for k, v in sorted(self.prefs.items())); Kit.put_var(SETTINGS_KEY, data)
        return data
    def profile_job(self, req):
        kind, name = req
        try: getattr(self, "_profile_" + kind)(name)
        except Exception as ex: Kit.say("profile %s failed: %s%s" % (kind, Tz.why(ex), _error_where()), Kit.HUE_BAD)
        if kind != "load" and self.config is not None and not self.stopping():
            self.config.refresh_profiles()
            if self.config.mode == "full": self.config.prof_redraw = False; self.config.redraw()
    def _profile_save(self, name):
        name = PROFILES.clean(name)
        if not name: raise Exception("type a name for the profile in the box")
        Kit.say('saving profile "%s".' % name, Kit.HUE_INFO); data = self.save_prefs()
        stamp, n, saved, failed = PROFILES.save(name, data); fav = PROFILES.favorite()
        PROFILES.set_state("fav" if name == fav else "pick", name, stamp)
        if name == fav:
            try: PROFILES.set_client_default(name)
            except Exception as ex: failed.append("TazUO default for new characters (%s)" % Tz.why(ex))
        if self.config is not None: self.config.prof_sel = name
        PROFILES.report(name, "saved", n, True, saved, failed)
    def _profile_load(self, name):
        if PROFILES.info(name) is None: raise Exception('there is no profile "%s"' % name)
        Kit.say('loading profile "%s".' % name, Kit.HUE_INFO); self.prefs_frozen = True
        try:
            LAYOUT.close()
            for s in self.slots:
                if s.running: self._stop(s)
            if self.config is not None: safe(self.config.close)
            if self.hub is not None: safe(self.hub.close)
            mode = "fav" if name == PROFILES.favorite() else "pick"; result = PROFILES.apply(name, mode)
            for c in set(Binds.saved.values()): self.hotkey_drop(c, Binds.OWNER)
            Binds.saved.clear(); Binds.loaded = False; self._zone_was_d = None
            ALERTS.loaded = False; GUARD.saved = None; Kit.read_screen(); LAYOUT.load(); Binds.load()
            for s in self.slots:
                if s.api is not None and s.lazy is None and s.factory is not None:
                    try: s.api = s.factory(); s.broken = None
                    except Exception as ex:
                        s.api, s.broken = None, str(ex) + _error_where()
                        Kit.say("%s could not be loaded: %s" % (s.title, s.broken), Kit.HUE_BAD)
            self.load_prefs()
        finally:
            self.prefs_frozen = False; self.config = ConfigWindow(self); self.config.prof_sel = name; self.config.open()
            self.hub = HubWindow(self)
            if self.grid is not None: safe(self.grid.show if self.pref_int("grid_on", 0) == 1 else self.grid.hide)
            for s in self.slots:
                if s.enabled: self.start(s)
            Kit.note_screen()
        PROFILES.report(name, "loaded", *result)
    def _profile_fav(self, name):
        if PROFILES.info(name) is None: raise Exception("save a profile first, then star it")
        if PROFILES.favorite() == name:
            PROFILES.set_favorite(""); safe(lambda: PROFILES.set_client_default(None))
            Kit.say('"%s" is no longer the favourite profile.' % name, Kit.HUE_INFO); return
        PROFILES.set_favorite(name); note = ""
        try: PROFILES.set_client_default(name)
        except Exception as ex: note = " (TazUO's default for new characters wasn't set: %s)" % Tz.why(ex)
        Kit.say('"%s" is the favourite profile: characters that haven\'t loaded another get it at start.%s'
                   % (name, note), Kit.HUE_GOOD)
    def run(self):
        Client.find()
        if Client.mouse is None:
            Kit.say("no client mouse timer; double-clicks use the client's own event.", Kit.HUE_INFO)
        self.load_prefs(); Kit.read_screen(); LAYOUT.load(); SNAP.on_drop(LAYOUT.dropped)
        API.OnStop(self.shutdown); self.grid = Grid(self)
        try: self.config = ConfigWindow(self); self.config.open()
        except Exception as ex:
            self._tell("%s: couldn't build the window: %s%s" % (APP_NAME, ex, _error_where()))
            if self.config is None: self.config = safe(lambda: ConfigWindow(self))
            if self.config is not None: safe(lambda: self.config.build_gear(self.config.gx, self.config.gy))
        try: self.hub = HubWindow(self)
        except Exception as ex:
            self._tell("%s: couldn't make the Ultima Tracker window: %s%s" % (APP_NAME, ex, _error_where()))
        if self.pref_int("grid_on", 0) == 1: safe(self.grid.show)
        names = [s.title for s in self.slots if s.enabled]
        API.SysMsg("%s %s running. %s" % (APP_NAME, APP_VERSION, ("On: " + ", ".join(names)) if names else
                   "Tick a module on the Modules tab."), Kit.HUE_GOOD)
        API.SetSharedVar(ALIVE_KEY, str(time.time())); Binds.load()
        for s in self.slots:
            if s.enabled: self.start(s)
        Kit.note_screen()
        try: self.whats_new.open()
        except Exception as ex: self._tell("%s: couldn't make the What's new window: %s" % (APP_NAME, ex))
        self.loop()
    def run_alone(self, s):
        if self.suite_alive():
            API.SysMsg("%s: %s is running; use %s there." % (s.title, APP_NAME, s.title), Kit.HUE_BAD); return
        self.alone, self.prefs_frozen = s, True; Client.find(); self.load_prefs(); Kit.read_screen()
        API.OnStop(self.shutdown); self.config = AlonePage(s); self.hub = safe(lambda: HubWindow(self))
        on = Kit.get_var(ALONE_PARTS % s.key, "")
        if s.parts and on: s.parts_on = dict((p[0], p[0] in on.split(",")) for p in s.parts)
        API.SysMsg("%s: running alone, without the rest of %s." % (s.title, APP_NAME), Kit.HUE_GOOD)
        Binds.load(); self.enable(s.key); self.loop()
    def loop(self):
        try:
            while not self.stopping() and (self.alone is None or self.alone.enabled):
                try: API.ProcessCallbacks()
                except Exception: pass
                try: self.run_due()
                except Exception as ex:
                    if self.stopping(): break
                    self._tell("%s: main loop error: %s%s" % (APP_NAME, ex, _error_where()))
                API.Pause(HOST_TICK)
        finally: self.shutdown()
    def shutdown(self):
        if self.shut: return
        self.shut = self.quitting = True; safe(Picker.drop)
        if not VA_ALONE:
            safe(lambda: Kit.on_client(LAYOUT.game_view_restore)); safe(lambda: LAYOUT.set_arrange(False, tell=False))
            safe(lambda: Kit.on_client(lambda: [cw.free() for cw in list(ClientWin.found.values()) + [
                LAYOUT.journal_held] if cw is not None]))
        for s in reversed(self.slots):
            if s.running:
                try: self._stop(s)
                except Exception: s.running = False
        self._refresh_active()
        if self.config is not None: safe(self.save_prefs); safe(self.config.close)
        if self.hub is not None: safe(self.hub.close)
        for fn in (ALERTS.close, self.whats_new.close, LAYOUT.close, GUARD.store, Kit.note_screen): safe(fn)
        if self.grid is not None: safe(self.grid.hide)
        safe(lambda: API.SysMsg("%s stopped." % APP_NAME, Kit.HUE_INFO))


class PartSet(object):
    OFF_LINE = "%s is off: tick it under PARTS to see its settings."
    def __init__(self, key, title, parts):
        self.key = key; self.specs = [[sp[0], sp[1], float(sp[2]), sp[3] if len(sp) > 3 else None] for sp in parts]
        self._owner = {sp[0]: sp[3] or ("%s.%s" % (key, sp[0])) for sp in self.specs}
        self._iv = {sp[0]: sp[2] for sp in self.specs}; self._fns = {}; self.api = {}; self.running = []; self.due = {}
        self.thread_due = {}; self.want = self._slot = None; self.busy = 0; self.stopping = False
    def slot(self):
        if self._slot is None: self._slot = dict.get(HOST.by_key, self.key)
        return self._slot
    def owner(self, pk): return self._owner.get(pk, pk)
    def part_api(self, pk):
        api = self.api.get(pk)
        if api is None:
            for sp in self.specs:
                if sp[0] == pk:
                    HOST.cur_part, HOST.cur_owner = pk, self.owner(pk)
                    try: api = sp[1]()
                    except Exception as ex:
                        api = {}; s = self.slot()
                        if s is not None: HOST.report(s, ex, s.part_title(pk), pk)
                    finally: HOST.cur_part = HOST.cur_owner = None
                    self.api[pk] = api
                    self._fns[pk] = ((api.get("interval"), "thread_tick" in api,
                                      api.get("thread_wanted")) if api else (None, False, None))
                    break
        return api
    def _call(self, pk, hook, *args):
        api = self.part_api(pk); fn = api.get(hook) if api else None
        if not fn: return None
        s = self.slot(); was = (HOST.cur_part, HOST.cur_owner); HOST.cur_part, HOST.cur_owner = pk, self.owner(pk)
        self.busy += 1
        try: return fn(*args)
        except Exception as ex:
            if s is not None and not HOST.stopping(): HOST.report(s, ex, s.part_title(pk), pk)
        finally: self.busy -= 1; HOST.cur_part, HOST.cur_owner = was
        return None
    def _sync_slot(self):
        s = self.slot()
        if s is not None: s.parts_running = set(self.running)
    def start_part(self, pk):
        if pk in self.running or self.stopping: return
        api = self.part_api(pk)
        if not api: self.api.pop(pk, None); return
        self.running.append(pk); self._sync_slot()
        if HOST.config is not None: HOST.config.forget_measure(self.key)
        self.due[pk] = 0.0; self.thread_due[pk] = False; s = self.slot()
        if s is not None: s.next_due = 0.0
        self._call(pk, "start")
    def stop_part(self, pk):
        if pk not in self.running: return
        self.running.remove(pk); self._sync_slot()
        if HOST.config is not None: HOST.config.forget_measure(self.key)
        owner = self.owner(pk); Picker.drop(owner); HOST.release_cursor(owner); self._call(pk, "stop")
    def wanted(self): s = self.slot(); return set(s.parts_wanted()) if s is not None else set()
    def reconcile(self, want=None):
        if want is None: want = self.wanted()
        if self.busy: self.want = set(want); return
        self.want = None
        for sp in self.specs:
            pk = sp[0]
            if pk in want and pk not in self.running: self.start_part(pk)
        for pk in list(reversed(self.running)):
            if pk not in want: self.stop_part(pk)
    def _start(self): self.stopping = False; self.reconcile()
    _NOFN = (None, False, None)
    def _tick(self):
        now = time.time(); poked = HOST.pass_poked; running = self.running; due = self.due
        for pk in list(running):
            if pk not in running: continue
            d = due.get(pk, 0.0)
            if poked or now + Host.EARLY >= d or d - now > Host.CLOCK_BACK:
                self._call(pk, "tick"); nxt, has_thread, want = self._fns.get(pk, self._NOFN)
                due[pk] = time.time() + Host._ask(nxt, self._iv.get(pk, 0.1))
                self.thread_due[pk] = has_thread and Host._ask(want, True, bool)
        if self.want is not None and not self.busy: self.reconcile(self.want)
    def _thread_wanted(self):
        if self.want is not None: return True
        td = self.thread_due
        for pk in self.running:
            if td.get(pk): return True
        return False
    def _thread_tick(self):
        for pk in list(self.running):
            if self.thread_due.get(pk) and pk in self.running:
                self.thread_due[pk] = False; self._call(pk, "thread_tick")
        if self.want is not None and not self.busy: self.reconcile(self.want)
    def _interval(self):
        best = None; due = self.due
        for pk in self.running:
            d = due.get(pk, 0.0)
            if best is None or d < best: best = d
        if best is None: return 1.0
        return min(30.0, max(0.002, best - time.time()))
    def _stop(self):
        self.stopping = True; self.want = None
        for pk in list(reversed(self.running)): self.stop_part(pk)
    HEAD_H = 28
    def _config_height(self, w):
        h = 0
        for sp in self.specs:
            pk = sp[0]; h += (Kit.GAP if h else 0) + self.HEAD_H
            if pk in self.running:
                api = self.api.get(pk)
                if api and api.get("config_height"):
                    hh = self._call(pk, "config_height", w); h += Kit.GAP + max(0, int(hh or 0))
        return max(40, h)
    def _build_config(self, g, x, y, w):
        s = self.slot()
        for sp in self.specs:
            pk = sp[0]; title = s.part(pk)[1] if s is not None and s.part(pk) else pk; on = pk in self.running
            api = self.api.get(pk) if on else None
            if y > 0 and sp is not self.specs[0]: y += Kit.GAP
            Kit.add_section(g, x, y, w, self.HEAD_H, title.upper() if on else None)
            if not on: Kit.add_label(g, Kit.fit(self.OFF_LINE % title, w - 24), x + 12, y + 7, Kit.HUE_INFO)
            y += self.HEAD_H
            if on and api and api.get("build_config"):
                y += Kit.GAP; hh = self._call(pk, "config_height", w) if api.get("config_height") else 0
                self._call(pk, "build_config", g, x, y, w); y += max(0, int(hh or 0))
    def _poll_config(self):
        for pk in list(self.running): self._call(pk, "poll_config")
    def _config_closed(self):
        for pk in self.specs:
            api = self.api.get(pk[0])
            if api and api.get("config_closed"): self._call(pk[0], "config_closed")
    def hooks(self):
        return {"start": self._start, "tick": self._tick, "stop": self._stop, "client_tick": True,
                "thread_tick": self._thread_tick, "thread_wanted": self._thread_wanted, "interval": self._interval,
                "parts": self.reconcile, "config_height": self._config_height, "build_config": self._build_config,
                "poll_config": self._poll_config, "config_closed": self._config_closed}


class Tz(object):
    _types = {}; _MISS = object()
    @staticmethod
    def T(name):
        if name not in Tz._types: Tz._types[name] = Client._type(name)
        t = Tz._types[name]
        if t is None: raise Exception("this TazUO build has no %s" % name.split(".")[-1])
        return t
    @staticmethod
    def get(obj, name, t=None):
        v = Typing._get(obj, name, t, Tz._MISS)
        if v is Tz._MISS: raise Exception("can't read %s" % name)
        return v
    @staticmethod
    def _flags(static):
        from System.Reflection import BindingFlags
        return BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.DeclaredOnly | \
            (BindingFlags.Static if static else BindingFlags.Instance)
    _found = {}
    @staticmethod
    def put(obj, name, value, t=None):
        t = t if t is not None else obj.GetType(); ck = ("put", t, name, obj is None); hit = Tz._found.get(ck, Tz._MISS)
        if hit is Tz._MISS:
            hit = None; flags = Tz._flags(obj is None); tt = t
            while tt is not None:
                p = tt.GetProperty(name, flags)
                if p is not None and p.CanWrite: hit = (True, p); break
                f = tt.GetField(name, flags)
                if f is not None: hit = (False, f); break
                tt = tt.BaseType
            Tz._found[ck] = hit
        if hit is None: raise Exception("can't set %s" % name)
        if hit[0]: hit[1].SetValue(obj, value, None)
        else: hit[1].SetValue(obj, value)
    @staticmethod
    def call(obj, name, args=(), t=None):
        import System; t = t if t is not None else obj.GetType(); args = list(args)
        ck = ("call", t, name, len(args), obj is None); m = Tz._found.get(ck, Tz._MISS)
        if m is Tz._MISS:
            m = None; flags = Tz._flags(obj is None); tt = t
            while tt is not None and m is None:
                for mm in tt.GetMethods(flags):
                    if mm.Name == name and not mm.IsGenericMethodDefinition and mm.GetParameters().Length == len(args):
                        m = mm; break
                tt = tt.BaseType
            Tz._found[ck] = m
        if m is None: raise Exception("can't call %s.%s" % (t.Name, name))
        return m.Invoke(obj, System.Array[object](args))
    @staticmethod
    def load_json(path, typeinfo, t):
        import System; cr = Tz.T("ClassicUO.Configuration.ConfigurationResolver")
        for m in cr.GetMethods(Tz._flags(True)):
            if m.Name == "Load" and m.IsGenericMethodDefinition and m.GetParameters().Length == 2:
                g = m.MakeGenericMethod(System.Array[System.Type]([t]))
                return g.Invoke(None, System.Array[object]([path, typeinfo]))
        raise Exception("can't read TazUO settings files")
    @staticmethod
    def copy_props(src, dst, skip=()):
        import System; from System.Reflection import BindingFlags; changed = failed = 0
        for p in dst.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance):
            name = str(p.Name)
            if name in skip or name.endswith("Serial"): continue
            if not p.CanRead or not p.CanWrite or p.GetIndexParameters().Length or p.GetSetMethod(False) is None:
                continue
            attrs = safe(lambda: list(p.GetCustomAttributes(True)), []) or []
            if any(a.GetType().Name == "JsonIgnoreAttribute" for a in attrs): continue
            try:
                v = p.GetValue(src, None)
                if System.Object.Equals(v, p.GetValue(dst, None)): continue
                try: p.SetValue(dst, v, None)
                except Exception:
                    pt = p.PropertyType
                    v = System.Enum.ToObject(pt, v) if pt.IsEnum else System.Convert.ChangeType(v, pt)
                    p.SetValue(dst, v, None)
                changed += 1
            except Exception: failed += 1
        return changed, failed
    @staticmethod
    def windows(type_names):
        gumps = Tz.get(None, "Gumps", Tz.T("ClassicUO.Game.Managers.UIManager"))
        return [g for g in list(gumps) if str(g.GetType().Name) in type_names]
    @staticmethod
    def why(ex):
        e = getattr(ex, "clsException", None) or ex
        while getattr(e, "InnerException", None) is not None: e = e.InnerException
        return str(getattr(e, "Message", None) or e)


class Profiles(object):
    PROFILE_SKIP = ("Username", "ServerName", "CharacterName", "Serial", "LastLoaded", "FollowingTarget")
    BAG_OWN = ("slot.", "trapsel=", "trapextra="); SERIAL_KEY = re.compile(r"_[0-9A-Fa-f]{8}$")
    MISSING = "\x01VA-missing"
    def __init__(self): self.base = os.path.join(Kit.data_dir(), PROFILE_DIR)
    @staticmethod
    def _read(path):
        import System
        try:
            if path and System.IO.File.Exists(path): return str(System.IO.File.ReadAllText(path))
        except Exception: pass
        return None
    @staticmethod
    def _write(path, text): import System; System.IO.File.WriteAllText(path, text, System.Text.UTF8Encoding(False))
    @staticmethod
    def _esc(s): return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\r", "\\r") .replace("\n", "\\n")
    @staticmethod
    def _unesc(s):
        un = {"t": "\t", "r": "\r", "n": "\n"}
        return re.sub(r"\\(.)", lambda m: un.get(m.group(1), m.group(1)), s, flags=re.S)
    RESERVED = frozenset(["CON", "PRN", "AUX", "NUL", "CLOCK$"] + ["COM%d" % i for i in range(1, 10)]
                         + ["LPT%d" % i for i in range(1, 10)])
    @staticmethod
    def clean(name):
        name = re.sub(r'[\\/:*?"<>|\t\r\n]+', "-", str(name or ""))
        name = name.strip(" .-")[:PROFILE_NAME_MAX].strip(" .-")
        if name.lower().endswith((".old", ".saving")):
            dot = name.rfind("."); name = (name[:dot] + "-" + name[dot + 1:])[:PROFILE_NAME_MAX]
        if name.split(".")[0].upper() in Profiles.RESERVED: return ""
        return name
    def folder(self, name): return os.path.join(self.base, name)
    def names(self):
        import System; out = []
        try:
            if System.IO.Directory.Exists(self.base):
                for d in System.IO.Directory.GetDirectories(self.base):
                    n = str(System.IO.Path.GetFileName(d))
                    if n.endswith(".saving") or n.endswith(".old"): continue
                    if System.IO.File.Exists(os.path.join(str(d), "profile.txt")): out.append(n)
        except Exception: pass
        return sorted(out, key=lambda s: s.lower())
    def info(self, name):
        text = self._read(os.path.join(self.folder(name), "profile.txt")) if name else None
        if text is None: return None
        pairs = (line.split("=", 1) for line in text.splitlines() if "=" in line)
        return dict((k.strip(), v.strip()) for k, v in pairs)
    def favorite(self):
        name = (self._read(os.path.join(self.base, "_favorite.txt")) or "").strip()
        return name if name and self.info(name) is not None else ""
    def set_favorite(self, name):
        import System; System.IO.Directory.CreateDirectory(self.base)
        self._write(os.path.join(self.base, "_favorite.txt"), name or "")
    def state(self):
        p = Kit.get_var(PROFILE_STATE_KEY).split("|"); return (p[0], p[1], p[2]) if len(p) >= 3 else ("", "", "")
    def set_state(self, mode, name, stamp): Kit.put_var(PROFILE_STATE_KEY, "%s|%s|%s" % (mode, name, stamp))
    SESSION_VARS = ("Layout_gameview_own", "Layout_gameview_lock", "Layout_zone_was", "VirtueAssistant_reclaim_undo")
    def keep_var(self, key):
        return key != PROFILE_STATE_KEY and not self.SERIAL_KEY.search(key) and (
            key not in self.SESSION_VARS and not key.startswith("Layout_client_locked_"))
    @staticmethod
    def char_vars():
        import System; t = Tz.T("ClassicUO.LegionScripting.PersistentVars")
        for m in t.GetMethods():
            if m.Name == "GetAllVars" and m.GetParameters().Length == 1:
                scope = System.Enum.Parse(m.GetParameters()[0].ParameterType, "Char")
                d = m.Invoke(None, System.Array[object]([scope]))
                return dict((str(kv.Key), "" if kv.Value is None else str(kv.Value)) for kv in d)
        raise Exception("can't list this character's saved settings")
    def read_vars(self, name):
        text = self._read(os.path.join(self.folder(name), "va_vars.txt")) or ""; out = {}
        for line in text.split("\n"):
            if "\t" in line:
                k, v = line.split("\t", 1); k = self._unesc(k)
                if k and self.keep_var(k): out[k] = self._unesc(v.rstrip("\r"))
        return out
    def wait_vars(self, wanted, timeout=5.0):
        left = dict(wanted); end = time.time() + timeout
        while left and not API.StopRequested:
            for k in list(left):
                got = safe(lambda: API.GetPersistentVar(k, self.MISSING, API.PersistentVar.Char))
                if got is not None and str(got) == left[k]: del left[k]
            if not left or time.time() > end: break
            API.Pause(0.05)
        return not left
    @staticmethod
    def bag_path():
        serial = safe(lambda: int(API.Player.Serial), 0)
        if not serial: return None
        return Kit.data_path("_unified_bag_%d.cfg" % serial)
    @staticmethod
    def client_files():
        CFG, MGR = "ClassicUO.Configuration.", "ClassicUO.Game.Managers."; PM = lambda: Tz.T(CFG + "ProfileManager")
        cur = lambda: Tz.get(None, "CurrentProfile", PM()); path = lambda: str(Tz.get(None, "ProfilePath", PM()))
        world = lambda: Tz.get(None, "Instance", Tz.T("ClassicUO.Game.World"))
        static = lambda tn, name, args=(): Tz.call(None, name, args, Tz.T(tn))
        current = lambda tn: Tz.get(None, "Current", Tz.T(tn)); inst = lambda tn: Tz.get(None, "Instance", Tz.T(tn))
        SD = CFG + "FeatureConfigs.ScreenDecorations.ScreenDecorations"
        def autoloot_reload(): a = inst(MGR + "AutoLootManager"); Tz.put(a, "_loaded", False); Tz.call(a, "Load")
        def infobar_reload():
            Tz.call(Tz.get(world(), "InfoBars"), "Load")
            for gump in Tz.windows(("InfoBarGump",)): safe(lambda: Tz.call(gump, "ResetItems"))
        def buysell_flush(): static(MGR + "BuySellAgent", "Unload"); static(MGR + "BuySellAgent", "Load")
        return (("cooldownbars.json", "cooldown bars", lambda: Tz.call(current(CFG + "CooldownBarsConfig"), "Save"),
             lambda: static(CFG + "CooldownBarsConfig", "LoadForProfile", (path(), cur()))),
            ("grid_highlights.json", "grid highlights", lambda: Tz.call(current(CFG + "GridHighlightsConfig"), "Save"),
             lambda: static(CFG + "GridHighlightsConfig", "LoadForProfile", (path(), cur()))),
            ("grid_container_bands.json", "container bands",
             lambda: Tz.call(current(CFG + "GridContainerBandsConfig"), "Save"),
             lambda: static(CFG + "GridContainerBandsConfig", "LoadForProfile", (path(),))),
            ("screen_decorations.json", "screen effects", lambda: Tz.call(current(SD), "Save"),
             lambda: static(SD, "LoadForProfile", (path(),))), ("tooltip_overrides.json", "tooltip overrides",
             lambda: Tz.call(Tz.get(current(CFG + "TooltipOverridesConfig"), "Char"), "Save"),
             lambda: static(CFG + "TooltipOverridesConfig", "Load")), ("nameoverhead.xml", "name plates",
             lambda: static(MGR + "NameOverHeadManager", "Save"), lambda: static(MGR + "NameOverHeadManager", "Load")),
            ("infobar.xml", "info bar", lambda: Tz.call(Tz.get(world(), "InfoBars"), "Save"), infobar_reload), 
            ("AutoLoot.json", "auto loot", lambda: Tz.call(inst(MGR + "AutoLootManager"), "Save"), autoloot_reload),
            ("OrganizerConfig.json", "organizer", lambda: Tz.call(inst(MGR + "OrganizerAgent"), "Save"),
             lambda: static(MGR + "OrganizerAgent", "Load")), ("journal_filters.json", "journal filter",
             lambda: Tz.call(inst(MGR + "JournalFilterManager"), "Save", (False,)),
             lambda: Tz.call(inst(MGR + "JournalFilterManager"), "Load")),
            ("BuyAgentConfig.json", "auto buy", buysell_flush, lambda: static(MGR + "BuySellAgent", "Load")),
            ("SellAgentConfig.json", "auto sell", lambda: None, lambda: static(MGR + "BuySellAgent", "Load")),
            ("macros.xml", "macros", lambda: Tz.call(Tz.get(world(), "Macros"), "Save", (None,)),
             lambda: Tz.call(Tz.get(world(), "Macros"), "Load")), ("hotkeys.json", "hotkeys",
             lambda: static(MGR + "Hotkeys.HotKeys", "Save"), lambda: static(MGR + "Hotkeys.HotKeys", "Load")),)
    @staticmethod
    def _profile_type():
        PM = Tz.T("ClassicUO.Configuration.ProfileManager"); return PM, Tz.get(None, "CurrentProfile", PM)
    def _client_export(self, dest):
        import System; F = System.IO.File; PM, cur = self._profile_type(); src = str(Tz.get(None, "ProfilePath", PM))
        saved, failed, pairs = [], [], []
        try:
            Tz.call(cur, "Save")
            pairs.append((os.path.join(src, "profile.json"), os.path.join(dest, "profile.json"), "options"))
        except Exception as ex: failed.append("options (%s)" % Tz.why(ex))
        for fn, what, flush, reload in self.client_files():
            try:
                flush(); p = os.path.join(src, fn)
                if F.Exists(p): pairs.append((p, os.path.join(dest, fn), what))
            except Exception as ex: failed.append("%s (%s)" % (what, Tz.why(ex)))
        return saved, failed, pairs
    def _apply_options(self, path):
        import System; PM, cur = self._profile_type()
        ctx = Tz.get(None, "DefaultToUse", Tz.T("ClassicUO.Configuration.ProfileJsonContext"))
        src = Tz.load_json(path, Tz.get(ctx, "Profile"), cur.GetType())
        if src is None: raise Exception("its profile.json can't be read")
        changed, failed = Tz.copy_props(src, cur, self.PROFILE_SKIP); Tz.call(cur, "Save")
        safe(lambda: Tz.call(Tz.get(None, "Game", Tz.T("ClassicUO.Client")), "SetVSync", (Tz.get(cur, "EnableVSync"),)))
        safe(lambda: Tz.put(None, "ContainerScale", System.Single(int(Tz.get(cur, "ContainersScale")) / 100.0),
                            Tz.T("ClassicUO.Game.Managers.UIManager")))
        return changed, failed
    def _client_import(self, srcdir):
        import System; F = System.IO.File; done, failed = [], []
        for w in Tz.windows(("OptionsWindow", "AssistantWindow")): safe(lambda: Tz.call(w, "Dispose"))
        PM, cur = self._profile_type(); dest = str(Tz.get(None, "ProfilePath", PM))
        pj = os.path.join(srcdir, "profile.json")
        if F.Exists(pj):
            try:
                changed, bad = self._apply_options(pj); done.append("options (%d changed)" % changed)
                if bad: failed.append(Kit.count(bad, "option"))
            except Exception as ex: failed.append("options (%s)" % Tz.why(ex))
        for fn, what, flush, reload in self.client_files():
            p = os.path.join(srcdir, fn)
            if not F.Exists(p): continue
            target = os.path.join(dest, fn); old = F.ReadAllBytes(target) if F.Exists(target) else None
            try: F.Copy(p, target, True); reload(); done.append(what)
            except Exception as ex:
                failed.append("%s (%s)" % (what, Tz.why(ex)))
                try:
                    if old is not None: F.WriteAllBytes(target, old)
                    elif F.Exists(target): F.Delete(target)
                    reload()
                except Exception: pass
        return done, failed
    def set_client_default(self, name):
        import System; F = System.IO.File
        root = str(Tz.get(None, "RootPath", Tz.T("ClassicUO.Configuration.ProfileManager")))
        for fn, dflt in (("profile.json", "default.json"), ("macros.xml", "macros.xml")):
            target = os.path.join(root, dflt); bak, none = target + ".va-backup", target + ".va-none"
            if name:
                src = os.path.join(self.folder(name), "tazuo", fn)
                if not F.Exists(src): continue
                if not F.Exists(bak) and not F.Exists(none):
                    if F.Exists(target): F.Copy(target, bak, False)
                    else: self._write(none, "")
                F.Copy(src, target, True)
            elif F.Exists(bak): F.Copy(bak, target, True); F.Delete(bak)
            elif F.Exists(none):
                if F.Exists(target): F.Delete(target)
                F.Delete(none)
    @staticmethod
    def _on_client(fn):
        try: res = Kit.on_client(fn, fallback=False)
        except Exception as ex: res = ([], ["TazUO settings (%s)" % Tz.why(ex)])
        return res or ([], ["TazUO settings (couldn't reach the client)"])
    def save(self, name, prefs_data):
        import System; D = System.IO.Directory; final = self.folder(name); tmp, old = final + ".saving", final + ".old"
        if D.Exists(tmp): D.Delete(tmp, True)
        D.CreateDirectory(os.path.join(tmp, "tazuo")); stamp = "%d" % int(time.time())
        va = dict((k, v) for k, v in self.char_vars().items() if self.keep_var(k)); va[SETTINGS_KEY] = prefs_data
        self._write(os.path.join(tmp, "va_vars.txt"),
                    "".join("%s\t%s\n" % (self._esc(k), self._esc(va[k])) for k in sorted(va)))
        bag = self.bag_path(); text = self._read(bag) if bag else None
        if text is not None:
            lay = [l for l in text.splitlines() if l.strip() and not l.startswith(self.BAG_OWN)]
            self._write(os.path.join(tmp, "unified_bag.cfg"), "\n".join(lay))
        res = self._on_client(lambda: self._client_export(os.path.join(tmp, "tazuo")))
        saved, failed = list(res[0]), list(res[1]); F = System.IO.File
        for src, dst, what in (res[2] if len(res) > 2 else ()):
            try: F.Copy(src, dst, True); saved.append(what)
            except Exception as ex: failed.append("%s (%s)" % (what, Tz.why(ex)))
        who = safe(lambda: str(API.Player.Name), "") or ""
        self._write(os.path.join(tmp, "profile.txt"),
                    "name=%s\nsaved=%s\nfrom=%s\nversion=%s\n" % (name, stamp, who, APP_VERSION))
        if D.Exists(old): D.Delete(old, True)
        if D.Exists(final): D.Move(final, old)
        try: D.Move(tmp, final)
        except Exception:
            if D.Exists(old) and not D.Exists(final): safe(lambda: D.Move(old, final))
            raise
        if D.Exists(old): D.Delete(old, True)
        if self.read_vars(name) != va or (self.info(name) or {}).get("saved") != stamp:
            raise Exception("the saved copy doesn't read back the same; try again")
        return stamp, len(va), saved, failed
    def apply(self, name, mode):
        info = self.info(name)
        if info is None: raise Exception('there is no profile "%s"' % name)
        folder = self.folder(name); va = self.read_vars(name)
        for k in sorted(va): Kit.put_var(k, va[k])
        ok = self.wait_vars(va); lay = self._read(os.path.join(folder, "unified_bag.cfg")); bag = self.bag_path()
        if lay is not None and bag:
            own = [l for l in (self._read(bag) or "").splitlines() if l.startswith(self.BAG_OWN)]
            self._write(bag, "\n".join([l for l in lay.splitlines() if l.strip()] + own))
        done, failed = self._on_client(lambda: self._client_import(os.path.join(folder, "tazuo")))
        self.set_state(mode, name, info.get("saved", "")); return len(va), ok, done, failed
    def report(self, name, verb, n, ok, done, failed):
        Kit.say('profile "%s" %s: %d Virtue Assistant settings; TazUO: %s.'
                   % (name, verb, n, ", ".join(done) or "nothing"), Kit.HUE_GOOD)
        if not ok:
            Kit.say("some settings were still saving; restart Virtue Assistant if a module looks unchanged.",
                    Kit.HUE_BAD)
        if failed: Kit.say("not done: %s." % "; ".join(failed), Kit.HUE_BAD)
    def startup(self):
        fav = self.favorite()
        if not fav: return
        stamp = (self.info(fav) or {}).get("saved", ""); mode, name, had = self.state()
        if mode == "pick" and name != fav and self.info(name) is not None: return
        if name == fav and had == stamp: return
        self.report(fav, "(the favourite) put on this character", *self.apply(fav, "fav"))


class ConfigWindow(object):
    W = 640; GEAR = 52; TABS = (("modules", "Modules"), ("settings", "Settings")); DOCK_KEY = "va"
    LINK_CMD = "VirtueAssistant_cmd"; LINK_STATE = "VirtueAssistant_state"; LINK_ALIVE = "ActionBar_alive"
    LINK_STALE = 10.0; LINK_ENABLE = "VirtueAssistant_enable"
    def __init__(self, host):
        self.host = host; self.g = self.mode = self._pp_key = self.shown_page = self.request = self.request_tab = None
        self.snap_cb = self.lag_lbl = self.grid_tb = self.dirty = self.gear_pos = None
        self.link_state = self.prof_sel = self.grid_text = self.prof_cache = self.prof_shown = None
        self.loading = self.stale_page = self.search_tb = self.search_text = None
        self.gear_clicked = self.closing = self.docked = self.prof_stale = self.prof_redraw = False
        self.box_hit = self.redraw_req = self.search_focus = False
        self.gear_look = self.lag_next = self.gear_moved = self.link_next = self.box_next = self.search_at = 0.0
        self.resize_at = 0.0; self.store = ({}, {}); self.seen = {}; self._pp_gate = [0.0]; self._fld_gate = [0.0]
        self._fld_due = True
        self.x, self.y = Kit.adapt(host.pref_int("cfg_x", 140), host.pref_int("cfg_y", 80), self.W, self.MIN_H)
        self.gx, self.gy = Kit.adapt(host.pref_int("gear_x", self.x),
                                     host.pref_int("gear_y", self.y), self.GEAR, self.GEAR)
        self.minimized = host.pref_int("cfg_min", 0) == 1 or host.dock_wanted(self.DOCK_KEY)
        self.tab = host.prefs.get("cfg_tab", "modules")
        if self.tab not in ("modules", "settings"): self.tab = "modules"
        self.page = host.prefs.get("cfg_page", ""); SNAP.enabled = host.pref_int("snap", 1) == 1
        self.reported = set(); self.page_keys = []; self.box_list = []
        self.part_boxes = []; self.fold_keys = []; self.measured = {}; self.mod_search = ""; self._prof_reset()
        sh = Kit.screen()[1]; self.lim_w = max(self.W, host.pref_int("cfg_w", self.W))
        self.lim_h = max(self.MIN_H, host.pref_int("cfg_h", (sh - 60) if sh > 400 else 1000))
        self.scale = max(50, min(200, host.pref_int("cfg_scale", 100))) / 100.0; self.size = (0, 0)
        for var in (self.LINK_CMD, self.LINK_ENABLE): API.RemoveSharedVar(var)
    STAR_RECTS = ((7, 1, 1, 2), (6, 3, 3, 2), (5, 5, 5, 1), (1, 6, 13, 1), (2, 7, 11, 1),
                  (4, 8, 7, 4), (3, 12, 3, 1), (9, 12, 3, 1), (3, 13, 1, 1), (11, 13, 1, 1))
    STAR_ON, STAR_OFF = "#F0C040", "#6A6A6A"; PROF_H = 34; PROF_DD_W = 196
    def _prof_reset(self):
        self.prof_dd = self.prof_dd_args = self.prof_tb = self.prof_seen = None; self.prof_names = []
        self.prof_fav = ""; self.prof_stars = {}; self.prof_star_hit = False
    @staticmethod
    def _cap_w(art, text): return (Kit.pic_size(art[0])[0] or 30) + 5 + Kit.text_w(text)
    def refresh_profiles(self):
        self.prof_stale = False; P = PROFILES
        try: data = ("ok", P.names(), P.favorite(), P.state()[1])
        except Exception as ex: data = ("err", ex)
        self.prof_cache = data
        if self.prof_shown is not None and self._prof_key(data) != self.prof_shown and self.mode == "full":
            self.prof_redraw = True
    @staticmethod
    def _prof_key(data): return ("ok", data[1], data[2]) if data[0] == "ok" else ("err", str(data[1]))
    def _build_profiles(self, g, x, y, w):
        data = self.prof_cache
        if data is None: self.refresh_profiles(); data = self.prof_cache
        self.prof_shown = self._prof_key(data); self.prof_stale = True
        if data[0] != "ok": raise data[1]
        names, fav, cur = data[1], data[2], data[3]; sel = self.prof_sel if self.prof_sel in names else None
        if sel is None: sel = cur if cur in names else (fav if fav in names else (names[0] if names else None))
        self.prof_sel, self.prof_names, self.prof_fav = sel, names, fav; H = self.PROF_H; Kit.add_section(g, x, y, w, H)
        xs = x + 12 + self.PROF_DD_W + 10; ys = y + (H - 16) // 2; self.prof_stars = {"on": [], "off": []}
        for key, color, d in (("shadow", "#000000", 1), ("on", self.STAR_ON, 0), ("off", self.STAR_OFF, 0)):
            for rx, ry, rw, rh in self.STAR_RECTS:
                b = Kit.add_box(g, xs + rx + d, ys + ry + d, rw, rh, 1.0, color)
                if b is not None and key != "shadow": self.prof_stars[key].append(b)
        Kit.catcher(g, xs - 3, ys - 3, 22, 22, self._star_click,
                    "Favourite: characters that haven't loaded another profile get it (click again to clear)")
        xb = xs + 28
        for key, art, cap, gap, tip in (("p_load", Kit.ART_PLAY, "Load", 14, "Load the picked profile here"),
                ("p_save", Kit.ART_OK, "Save", 6, "Save this setup under the typed name, or over the picked profile")):
            Kit.art_button(g, self.store, key, art, xb, y + 6, cap, tip); xb += self._cap_w(art, cap) + gap
        Kit.add_label(g, "as", xb, y + 9, Kit.HUE_INFO); xf = xb + Kit.text_w("as") + 8
        self.prof_tb = Kit.with_tip(Kit.add_textbox(g, "", xf, y + 6, max(60, x + w - 12 - xf), numbers=False),
                                    "New profile name (empty: save over the picked one)")
        items = [n + ("  (favourite)" if n == fav else "") for n in names] or ["(no profiles saved yet)"]
        self.prof_dd_args = (x + 12, y + 7, self.PROF_DD_W, items, names.index(sel) if sel in names else 0)
    def _add_profile_list(self, g):
        if self.prof_dd_args is None: return
        dx, dy, dw, items, idx = self.prof_dd_args; dd = G.CreateDropDown(dw, items, idx); dd.SetPos(dx, dy); g.Add(dd)
        self.prof_dd = Kit.with_tip(dd, "Saved profiles: pick one to load or save over")
        self.prof_seen = idx; self._show_star()
    def _prof_picked(self): return self.prof_sel if self.prof_sel in self.prof_names else None
    def _show_star(self):
        p = self._prof_picked(); on = bool(p) and p == self.prof_fav
        for key, shown in (("on", on), ("off", not on)):
            for b in self.prof_stars.get(key, []): Kit.set(b, "IsVisible", shown)
    def _star_click(self): self.prof_star_hit = True
    def _poll_profiles(self):
        if self.prof_dd is not None and self._fld_due:
            try: i = int(self.prof_dd.GetSelectedIndex())
            except Exception: i = None
            if i is not None and i != self.prof_seen:
                self.prof_seen = i
                if 0 <= i < len(self.prof_names): self.prof_sel = self.prof_names[i]
                self._show_star()
        star, self.prof_star_hit = self.prof_star_hit, False; load = Kit.was_clicked(self.store, "p_load")
        save = Kit.was_clicked(self.store, "p_save")
        if not (star or load or save): return
        if self.host.profile_req is not None: return
        picked = self._prof_picked()
        if save:
            typed = str(safe(lambda: self.prof_tb.Text, "") or "").strip()
            name = PROFILES.clean(typed) if typed else picked
            if not name: Kit.say("type a profile name beside Save.", Kit.HUE_BAD); return
            self.host.profile_req = ("save", name)
        elif not picked: Kit.say("save a profile first (type a name beside Save).", Kit.HUE_BAD)
        elif load: self.host.profile_req = ("load", picked)
        else: self.host.profile_req = ("fav", picked)
    def settings_slots(self):
        return [s for s in self.host.slots if s.lazy is not None or (s.api is not None and s.api.get("build_config"))] \
            + list(self.host.pages)
    def open(self):
        if self.prof_cache is None: self.refresh_profiles()
        if self.minimized: self.build_gear(self.gx, self.gy)
        else: self.build_full(self.x, self.y)
    def build_full(self, x, y): Kit.on_client(lambda: self._build_full(x, y))
    def _replace(self, g, mode, x, y, w, h, head=None):
        old = self.g; x, y = Kit.place(g, x, y, w, h, head)
        if mode == "gear": self.gx, self.gy = x, y
        else: self.x, self.y = x, y
        self.g, self.mode = g, mode; G.AddGump(g); Kit.on_moved(g, self._moved)
        if mode == "gear": g.SetInScreen()
        Kit.dispose(old)
    def _note_pos(self):
        x, y = self.pos()
        if x is None or y is None: return False
        if self.mode == "gear": self.gx, self.gy = x, y
        elif self.mode == "full": self.x, self.y = x, y
        return True
    def _moved(self):
        if self._note_pos(): self.host.save_prefs()
    def _settings_error(self, s, what, ex):
        msg = "%s: %s settings %s error: %s%s" % (APP_NAME, s.title, what, ex, _error_where())
        if msg not in self.reported: self.reported.add(msg); API.SysMsg(msg, Kit.HUE_BAD)
    def _leave_page(self):
        key, self.shown_page = self.shown_page, None; stale, self.stale_page = self.stale_page == key, None
        s = self.host.page_slot(key)
        if s is None or s.api is None: return
        for fn in (("config_closed",) if stale else ("poll_config", "config_closed")):
            if s.api.get(fn):
                try: s.api[fn]()
                except Exception as ex: self._settings_error(s, "save", ex)
    COL_W = W - 2 * Kit.MARGIN; MIN_W = W; MIN_H = 200; SETTLE = 0.35; SCALES = (70, 80, 90, 100, 110, 125, 150)
    ART_LESS = (5401, 5401, 5401); ART_MORE = (5402, 5402, 5402)
    HELP_LINES = ("Tick a module to turn it on; closing its window turns it off. Settings are on the Settings tab.",
                  "Drag a corner to resize; - and + scale the window.")
    SNAP_CAP = "Snap windows together"; BROKEN = "couldn't load: see the journal"
    LAG_SAMPLE = "12 modules on; slowest lately: Ultima Tracker, 999 ms"
    def _context(self):
        host = self.host; pages = self.settings_slots(); page = None
        if self.tab == "settings" and pages:
            page = host.page_slot(self.page)
            if page not in pages: page = pages[0]; self.page = page.key
            if page.lazy is not None and Client.on_client_thread():
                host.request_load(page); self.loading = page; return host.slots, pages, None
            if not host.load(page) or not page.api.get("build_config"):
                pages = self.settings_slots()
                page = pages[0] if pages and host.load(pages[0]) and pages[0].api.get("build_config") else None
                if page is not None: self.page = page.key
        self.loading = None; return host.slots, pages, page
    def _body_y(self): return Kit.MARGIN + 34 + Kit.GAP + self.PROF_H + Kit.GAP
    def _pack(self, units, n, limit):
        GAP = Kit.GAP; out, col, y = [], 0, 0
        for u, unit in enumerate(units):
            rows = unit.get("rows")
            if rows is None:
                size = unit["h"]; top = y + GAP if y else 0
                if y and top + size > limit: col, top = col + 1, 0
                if col >= n or size > limit: return None
                out.append((u, col, top, None, None, size)); y = top + size; continue
            head, tail = unit["head"], unit["tail"]; i = 0
            while i < len(rows):
                top = y + GAP if y else 0
                if y and top + head + rows[i] + tail > limit: col, top = col + 1, 0
                if col >= n or head + rows[i] + tail > limit: return None
                j, h = i, head + tail
                while j < len(rows) and top + h + rows[j] <= limit: h += rows[j]; j += 1
                out.append((u, col, top, i, j, h)); i, y = j, top + h
                if i < len(rows): col, y = col + 1, 0
        return out
    def _fit(self, units, n):
        lo = hi = 0
        for unit in units:
            rows = unit.get("rows")
            if rows is None: lo = max(lo, unit["h"]); hi += unit["h"] + Kit.GAP
            elif rows:
                lo = max(lo, unit["head"] + max(rows) + unit["tail"])
                hi += unit["head"] + sum(rows) + unit["tail"] + Kit.GAP
        hi = max(hi, lo, 1); best = self._pack(units, n, hi)
        while lo < hi:
            mid = (lo + hi) // 2; p = self._pack(units, n, mid)
            if p is not None: hi, best = mid, p
            else: lo = mid + 1
        return best or []
    def _flow(self, units, CW):
        M, GAP = Kit.MARGIN, Kit.GAP; lim_w = self.lim_w; sw = Kit.screen()[0]
        if sw: lim_w = min(lim_w, max(self.MIN_W, int(sw / self.scale) - 10))
        n = max(1, (lim_w - 2 * M + GAP) // (CW + GAP))
        if sw: n = max(1, min(n, (int(sw / self.scale) - 2 * M + GAP) // (CW + GAP)))
        limit = max(40, self.lim_h - self._body_y() - M); placed = self._pack(units, n, limit)
        if placed is None: placed = self._fit(units, n)
        return placed
    @staticmethod
    def _matches(s, q):
        if not q: return True, []
        hit = q in s.title.lower() or q in (s.desc or "").lower() or any(q in a.lower() for a in s.aliases)
        parts = [p[0] for p in s.parts if q in p[1].lower() or q in (p[2] or "").lower()]
        if not parts: parts = [p[0] for p in s.parts if any(q in str(o).lower() for o in p[4])]
        return hit or bool(parts), parts
    def _mod_rows(self, slots, CW):
        q = self.mod_search.strip().lower(); groups, order, found = {}, [], {}
        for s in slots:
            hit, parts = self._matches(s, q)
            if not hit: continue
            found[s.key] = parts; cat = getattr(s, "category", None) or "Other"
            if cat not in groups: groups[cat] = []; order.append(cat)
            groups[cat].append(s)
        cats = [c for c in CATEGORY_ORDER if c in groups] + sorted(c for c in order if c not in CATEGORY_ORDER)
        rows = []
        for cat in cats:
            rows.append(("head", cat))
            for s in groups[cat]:
                broken = s.api is None and s.lazy is None
                rows.append(("mod", s, broken, Kit.wrap(self.BROKEN if broken else s.desc, CW - 212)))
                if s.parts and not broken and (not s.folded or found.get(s.key)):
                    for p in s.parts:
                        rows.append(("part", s, p, Kit.wrap(p[2] or "", CW - 248), p[0] in found.get(s.key, ())))
        if not rows: rows.append(("none", 'No module matches "%s".' % self.mod_search.strip()))
        return rows
    @staticmethod
    def _row_h(r):
        if r[0] in ("mod", "part"): return 26 + 20 * (len(r[3]) - 1)
        return 24
    def _units_modules(self, slots):
        CW = self.COL_W; rows = self._mod_rows(slots, CW)
        lines = [l for para in self.HELP_LINES for l in Kit.wrap(para, CW - 42)]
        split = CW < 30 + Kit.text_w(self.LAG_SAMPLE) + 12 + Kit.text_w("Grid px") + 8 + 48 + 12
        h_opts = 8 + 22 * len(lines) + 48 + (24 if split else 0)
        units = [{"rows": [self._row_h(r) for r in rows], "head": 34, "tail": 4,
                  "draw": lambda g, x, y, h, i, j: self._draw_mods(g, x, y, CW, h, rows[i:j], i == 0)}, {"h": h_opts,
                  "draw": lambda g, x, y, h, i, j: self._draw_opts(g, x, y, CW, h, lines, split)}]
        return units, CW
    PAGE_MAX_W = 1100
    def _measure_page(self, page, x0, y0, CW):
        ck = (page.key, CW)
        if ck in self.measured: return self.measured[ck]
        measure = PageCanvas(None); out = None
        try:
            page.api["build_config"](measure, x0, y0, CW)
            if Kit.flush():
                right = x0 + CW
                for c in measure.ctrls:
                    r = safe(lambda: int(c.GetX()) + int(c.GetWidth()), None)
                    if r is not None and r != x0 + CW: right = max(right, r + 4)
                out = ([tuple(int(v) for v in r) for r in measure.sections], right - x0)
        except Exception: out = None
        finally:
            if page.api.get("config_closed"): safe(page.api["config_closed"])
            for c in measure.ctrls: Kit.dispose(c)
        if len(self.measured) > 64: self.measured.clear()
        if page not in self.host.pages: self.measured[ck] = out
        return out
    def forget_measure(self, key):
        for ck in [ck for ck in self.measured if ck[0] == key]: self.measured.pop(ck, None)
    def loaded(self, key):
        self.forget_measure(key)
        if self.loading is not None and self.loading.key == key: self.redraw_req = True
    def _pick_unit(self, pages, CW, lit):
        slot = 35 + max([Kit.text_w(s.title) for s in pages] or [80]) + 12; per = max(1, 1 + (CW - 30 - slot) // 196)
        self.page_keys = [("page_" + s.key, s.key) for s in pages]
        def draw_pick(g, x, y, h, i, j):
            Kit.add_section(g, x, y, CW, h)
            for k, s in enumerate(pages):
                r = k // per
                if i <= r < j:
                    Kit.art_button(g, self.store, "page_" + s.key, Kit.ART_PAGE, x + 30 + (k % per) * 196,
                                   y + 6 + (r - i) * 28, s.title, "Show %s settings" % s.title,
                                   Kit.HUE_TITLE if lit(s) else Kit.HUE_TEXT)
        return {"rows": [28] * ((len(pages) + per - 1) // per), "head": 6, "tail": 4, "draw": draw_pick}
    def _units_loading(self, pages, title):
        CW = self.COL_W
        def draw_note(g, x, y, h, i, j):
            Kit.add_section(g, x, y, CW, h)
            Kit.add_label(g, "Loading %s settings" % title, x + 12, y + 12, Kit.HUE_INFO)
        return [self._pick_unit(pages, CW, lambda s: s.title == title), {"h": 40, "draw": draw_note}], CW
    def _units_settings(self, pages, page, x0, y0):
        CW = self.COL_W; rects = None; m = self._measure_page(page, x0, y0, CW)
        if m is not None:
            rects, need = m
            if need > CW:
                CW = min(self.PAGE_MAX_W, need); m = self._measure_page(page, x0, y0, CW)
                rects = m[0] if m is not None else None
        units = [self._pick_unit(pages, CW, lambda s: s is page)]
        if page.parts:
            units.append({"h": 34 + 26 * len(page.parts) + 6,
                          "draw": lambda g, x, y, h, i, j: self._draw_parts(g, x, y, CW, h, page)})
        wins = LAYOUT.windows_of(page.key)
        if wins:
            units.append({"h": 34 + 26 * len(wins) + 6, "draw": lambda g, x, y, h, i,
                          j: self._draw_windows(g, x, y, CW, h, wins)})
        try: h_page = max(40, int(page.api["config_height"](CW)))
        except Exception as ex: self._settings_error(page, "layout", ex); h_page = 40
        bands = (self._bands(rects, y0, h_page) if rects else None) or [(0, h_page)]; state = {"at": {}}
        def band_draw(b):
            def draw(g, x, y, h, i, j):
                state["at"][b] = (x, y)
                if b == len(bands) - 1: self._draw_page(g, page, x0, y0, CW, bands, state["at"])
            return draw
        for b, (top, bottom) in enumerate(bands): units.append({"h": bottom - top, "draw": band_draw(b)})
        return units, CW
    @staticmethod
    def _bands(rects, y0, h_page):
        rects = sorted(set(rects), key=lambda r: (r[1], r[0]))
        top_level = [r for r in rects if not any(o != r and o[0] <= r[0] and o[1] <= r[1] and r[0] + r[2] <= o[0] + o[2]
            and r[1] + r[3] <= o[1] + o[3] for o in rects)]
        bands = []
        for x, y, w, h in top_level:
            t, b = y - y0, y - y0 + h
            if bands and t < bands[-1][1]: bands[-1] = (bands[-1][0], max(bands[-1][1], b))
            else: bands.append((t, b))
        return bands
    def _draw_page(self, g, page, x0, y0, CW, bands, at):
        canvas = PageCanvas(g)
        try: page.api["build_config"](canvas, x0, y0, CW)
        except Exception as ex:
            self._settings_error(page, "window", ex); Kit.add_section(g, x0, y0, CW, 40)
            Kit.add_label(g, "Settings unavailable: %s" % ex, x0 + 12, y0 + 12, Kit.HUE_BAD)
        self.shown_page = page.key; moves = []
        for b, (top, bottom) in enumerate(bands):
            px, py = at.get(b, (x0, y0 + top)); moves.append((top, px - x0, py - (y0 + top)))
        if all(dx == 0 and dy == 0 for t, dx, dy in moves): return
        if not Kit.flush(): return
        for c in canvas.ctrls:
            try: cx, cy = int(c.GetX()), int(c.GetY())
            except Exception: continue
            rel = cy - y0; dx, dy = moves[0][1], moves[0][2]
            for top, mx, my in moves:
                if rel >= top: dx, dy = mx, my
            if dx or dy: safe(lambda: c.SetPos(cx + dx, cy + dy))
    SEARCH_W = 150
    def _draw_parts(self, g, x, y, w, h, s):
        Kit.add_section(g, x, y, w, h, "PARTS  (tick a part to turn it on)"); ry = y + 32
        for p in s.parts:
            self._part_box(g, s, p, x + 12, ry)
            Kit.add_label(g, Kit.fit(p[2] or "", w - 236), x + 224, ry + 2, Kit.HUE_INFO); ry += 26
    def _part_box(self, g, s, p, x, ry):
        on = bool(s.parts_on.get(p[0])); cb = Kit.add_check(g, p[1], x, ry, on, "%s: %s" % (s.title, p[2] or p[1]))
        self._hook_box(cb); self.part_boxes.append((s, p[0], cb)); self.seen["%s.%s" % (s.key, p[0])] = on
    ZONE_TIP = "Click: next zone (free: stays where you put it; Settings > Layout lists them all)"
    def _draw_windows(self, g, x, y, w, h, wins):
        Kit.add_section(g, x, y, w, h, "WINDOWS  (the zone each sits in)"); zones = LAYOUT.zone_choices(); ry = y + 32
        for key, title in wins:
            Kit.add_label(g, Kit.fit(title, 200), x + 12, ry + 3); zid = LAYOUT.zone_of(key)
            cap = "Zone: " + (zid if zid else "free"); bkey = "zone_" + key
            Kit.art_button(g, self.store, bkey, Kit.ART_PAGE, x + 224, ry - 2, cap, self.ZONE_TIP)
            self.zone_keys.append((bkey, key, zones)); ry += 26
    FOLD_TIP = "Show its parts"; UNFOLD_TIP = "Hide its parts"; NEW_TAG = "(new)"
    def _draw_mods(self, g, x, y, w, h, rows, first):
        Kit.add_section(g, x, y, w, h, "MODULES  (tick a module to turn it on)" if first else "MODULES  (continued)")
        if first:
            xs = x + w - 12 - self.SEARCH_W
            Kit.add_label(g, "Search", xs - 8 - Kit.text_w("Search"), y + 7, Kit.HUE_INFO)
            self.search_tb = Kit.with_tip(Kit.add_textbox(g, self.mod_search, xs, y + 5, self.SEARCH_W, numbers=False),
                                          "Type part of a name or feature to list matching modules (old names work)")
            self.search_text = None
        ry = y + 32
        for row in rows:
            if row[0] == "part":
                s, p, lines, hit = row[1], row[2], row[3], row[4]; self._part_box(g, s, p, x + 36, ry); xd = x + 236
                for k, line in enumerate(lines): Kit.add_label(g, line, xd, ry + 2 + 20 * k, Kit.HUE_INFO)
                tag = "<- found" if hit else (self.NEW_TAG if not p[4] else "")
                if tag:
                    tw = Kit.text_w(lines[0]) if lines else 0
                    Kit.add_label(g, tag, min(xd + tw + 10, x + w - 12 - Kit.text_w(tag)), ry + 2,
                                  Kit.HUE_TITLE if hit else Kit.HUE_INFO)
            elif row[0] != "mod":
                Kit.add_label(g, row[1].upper() if row[0] == "head" else row[1], x + 12, ry + 3,
                              Kit.HUE_TITLE if row[0] == "head" else Kit.HUE_INFO)
            else:
                s, broken, lines = row[1], row[2], row[3]
                if broken: Kit.add_label(g, s.title, x + 36, ry + 2, Kit.HUE_INFO)
                else:
                    cb = Kit.add_check(g, s.title, x + 12, ry, s.enabled, s.desc); self._hook_box(cb)
                    self.box_list.append((s, None, cb)); self.seen[s.key] = s.enabled
                    if s.parts:
                        arrow = ">" if s.folded else "v"; Kit.add_label(g, arrow, x + 184, ry + 2, Kit.HUE_TITLE)
                        Kit.catcher(g, x + 178, ry, 18, 22, self._fold_click(s.key),
                                    self.FOLD_TIP if s.folded else self.UNFOLD_TIP)
                        self.fold_keys.append(("fold_" + s.key, s.key))
                for k, line in enumerate(lines):
                    Kit.add_label(g, line, x + 200, ry + 2 + 20 * k, Kit.HUE_BAD if broken else Kit.HUE_INFO)
            ry += self._row_h(row)
    def _fold_click(self, key):
        store = self.store
        def hit(): Kit.clicks_seen = True; store[1]["fold_" + key] = True; HOST.poke()
        return hit
    def _draw_opts(self, g, x, y, w, h, lines, split):
        host = self.host; Kit.add_section(g, x, y, w, h); ly = y + 8
        for line in lines: Kit.add_label(g, line, x + 30, ly, Kit.HUE_INFO); ly += 22
        self.snap_cb = Kit.add_check(g, self.SNAP_CAP, x + 30, ly, SNAP.enabled); self._hook_box(self.snap_cb)
        ly += 24; self.lag_lbl = Kit.add_label(g, "", x + 30, ly, Kit.HUE_INFO)
        self.lag_next = 0.0
        if split:
            ly += 24; Kit.add_label(g, "Grid px", x + 30, ly, Kit.HUE_INFO); gx = x + 30 + Kit.text_w("Grid px") + 8
        else: gx = x + w - 12 - 50; Kit.add_label(g, "Grid px", gx - Kit.text_w("Grid px") - 8, ly, Kit.HUE_INFO)
        self.grid_tb = Kit.with_tip(Kit.add_textbox(g, str(host.grid_size()), gx, ly - 2, 44),
                                    "Grid spacing for snapping (8-512; the Action Bar's Grid button shows it)")
    def _on_resized(self, *args):
        first = not self.resize_at; self.resize_at = time.time(); g = self.g
        if first and self.mode == "full" and Kit.is_open(g): g.SetAlpha(0.55)
    def _relayout(self):
        g = self.g
        if self.mode != "full" or not Kit.is_open(g): return
        try: w, h = int(g.GetWidth()), int(g.GetHeight()); x, y = int(g.GetX()), int(g.GetY())
        except Exception: return
        if (w, h) == self.size: return
        self.lim_w = max(self.MIN_W, int(round(w / self.scale)))
        self.lim_h = max(self.MIN_H, int(round(h / self.scale))); self.x, self.y = x, y; self.build_full(x, y)
        self.host.save_prefs()
    def _step_scale(self, d):
        pcts = list(self.SCALES); cur = int(round(self.scale * 100))
        i = min(range(len(pcts)), key=lambda k: abs(pcts[k] - cur))
        i = max(0, min(len(pcts) - 1, i + d)) if d else pcts.index(100)
        if pcts[i] != cur: self.scale = pcts[i] / 100.0; self.redraw()
    def _reset(self):
        self._leave_page(); self.search_tb, self.search_text, self.search_at = None, None, 0.0; self.store = ({}, {})
        self.page_keys, self.box_list, self.zone_keys = [], [], []; self.snap_cb = self.lag_lbl = None
        self._prof_reset()
    def _build_full(self, x, y):
        self._reset(); self.seen, self.grid_tb, self.resize_at, self.grid_text = {}, None, 0.0, None
        self.part_boxes, self.fold_keys = [], []; M, GAP = Kit.MARGIN, Kit.GAP; L = M
        slots, pages, page = self._context(); y_title = M; y_prof = y_title + 34 + GAP; y_body = self._body_y()
        if self.tab == "settings" and page is not None: units, CW = self._units_settings(pages, page, L, y_body)
        elif self.tab == "settings" and self.loading is not None and pages:
            units, CW = self._units_loading(pages, self.loading.title)
        else: units, CW = self._units_modules(slots)
        placed = self._flow(units, CW); n_cols = 1 + max([p[1] for p in placed] or [0])
        W = 2 * M + n_cols * CW + (n_cols - 1) * GAP; H = y_body + max([p[2] + p[5] for p in placed] or [40]) + M
        IW = W - 2 * M; S = self.scale; WS, HS = int(round(W * S)), int(round(H * S))
        g = G.CreateModernGump(x, y, WS, HS, True, int(self.MIN_W * S), int(self.MIN_H * S), self._on_resized)
        g.SetAlpha(0)
        Kit.add_window_frame(g, W, H, mouse=False); Kit.add_section(g, L, y_title, IW, 34)
        Kit.add_label(g, "VIRTUE ASSISTANT", L + 30, y_title + 9, Kit.HUE_TITLE)
        xv = L + 30 + Kit.text_w("VIRTUE ASSISTANT") + 12
        Kit.add_label(g, "v" + APP_VERSION, xv, y_title + 9, Kit.HUE_INFO); xt = xv + Kit.text_w("v" + APP_VERSION) + 16
        Kit.title_catcher(g, L, y_title, xt - 6 - L, 34, lambda: self.store[1].__setitem__("min", True), key="va")
        for key, text in self.TABS:
            on = key == self.tab
            Kit.art_button(g, self.store, "tab_" + key, Kit.ART_PAGE, xt, y_title + 6, text,
                           "Show the %s tab" % text, Kit.HUE_TITLE if on else Kit.HUE_INFO)
            xt += self._cap_w(Kit.ART_PAGE, text) + 16
        pct = "%d%%" % int(round(S * 100)); xp = W - M - 74 - Kit.DOCK_DX - 8 - 16
        Kit.art_button(g, self.store, "scale_up", self.ART_MORE, xp, y_title + 9, None, "Larger window and text")
        xl = xp - 6 - Kit.text_w(pct); Kit.add_label(g, pct, xl, y_title + 9, Kit.HUE_TEXT)
        Kit.catcher(g, xl - 2, y_title + 6, Kit.text_w(pct) + 4, 22,
                    lambda: self.store[1].__setitem__("scale_reset", True), "Scale (click: 100%)")
        Kit.art_button(g, self.store, "scale_down", self.ART_LESS, xl - 6 - 16, y_title + 9,
                       None, "Smaller window and text")
        Kit.dock_button(g, self.store, W - M - 74, y_title + 9)
        Kit.art_button(g, self.store, "min", Kit.ART_MIN, W - M - 74, y_title + 9, None,
                       "Minimize to the gear (or double-click the title)")
        Kit.art_button(g, self.store, "close", Kit.ART_CLOSE, W - M - 54, y_title + 6,
                       None, "Close Virtue Assistant (stops every module)")
        try: self._build_profiles(g, L, y_prof, IW)
        except Exception as ex:
            self.prof_dd_args = None; Kit.add_label(g, "Profiles unavailable: %s" % ex, L + 12, y_prof + 9, Kit.HUE_BAD)
        for u, col, top, i, j, h in sorted(placed, key=lambda p: p[0]):
            units[u]["draw"](g, L + col * (CW + GAP), y_body + top, h, i, j)
        self._add_profile_list(g)
        if not Kit.scale_window(g, S) and S != 1.0:
            self.scale, S, WS, HS = 1.0, 1.0, W, H; Kit.say("can't scale the window; it stays at 100%.", Kit.HUE_BAD)
        self._replace(g, "full", x, y, WS, HS, int(round(y_body * S))); fit = Kit.scroll_info(g)
        self.size = (fit["w2"], fit["hv"]) if fit else (WS, HS); self.minimized = False; self.dirty = None
        if self.search_focus:
            self.search_focus = False; tb = self.search_tb
            if tb is not None:
                cc = Kit.client_control(tb)
                if cc is not None and Kit.flush(): safe(lambda: cc.SetKeyboardFocus())
    def build_gear(self, x, y):
        self._reset(); S = self.GEAR; g = G.CreateGump(True, True); Kit.add_window_frame(g, S, S, corners=False)
        Kit.add_section(g, 7, 7, S - 14, S - 14)
        p = G.CreateGumpItemPic(0x1053, S - 18, S - 18); p.SetPos(9, 9); p.SetAcceptMouseInput(False); g.Add(p)
        Kit.catcher(g, 0, 0, S, S, self._gear_click, "%s: click to open, drag to move" % APP_NAME, movable=True)
        self.gear_clicked, self.gear_pos, self.gear_moved = False, None, 0.0; self._replace(g, "gear", x, y, S, S)
        self.minimized = True; self.docked = self.host.dock_wanted(self.DOCK_KEY) and self.host.bar_alive()
        if self.docked: self._show_gear(False)
    def fold_to_bar(self):
        self.host.dock_want_set(self.DOCK_KEY, True)
        if self.mode == "full": self.fold()
        if not self.host.bar_alive(): self.host.dock_note(APP_NAME)
    def _show_gear(self, shown):
        g = self.g
        if self.mode == "gear" and Kit.is_open(g): g.IsVisible = bool(shown)
    def link_tick(self):
        now = time.time()
        if now < self.link_next and self.link_next - now <= 0.1: return
        self.link_next = now + 0.1; key = self._take_shared(self.LINK_ENABLE)
        if key: self.host.enable(str(key))
        cmd = self._take_shared(self.LINK_CMD)
        if cmd:
            cmd = str(cmd)
            if cmd == "show" and self.mode != "full": self.unfold()
            elif cmd == "dock" and self.mode == "full": self.fold_to_bar()
            elif cmd == "modules": self.request_tab = "modules"
        want = self.host.dock_wanted(self.DOCK_KEY)
        if self.mode == "gear" and (self.docked or want):
            hide = want and self.host.bar_alive()
            if hide != self.docked: self.docked = hide; self._show_gear(not hide)
        state = ("docked" if self.docked else "gear") if self.mode == "gear" else "open"
        if state != self.link_state: self.link_state = state; API.SetSharedVar(self.LINK_STATE, state)
    @staticmethod
    def _take_shared(name):
        try: v = API.GetSharedVar(name)
        except Exception: return None
        if v: API.RemoveSharedVar(name)
        return v
    def _gear_click(self): self.gear_clicked = True
    def pos(self): g = self.g; return safe(lambda: int(g.GetX())), safe(lambda: int(g.GetY()))
    def store_prefs(self, prefs):
        if Client.on_client_thread(): self._note_pos()
        for k, v in (("cfg_x", self.x), ("cfg_y", self.y), ("cfg_w", self.lim_w), ("cfg_h", self.lim_h),
                     ("cfg_scale", int(round(self.scale * 100))), ("gear_x", self.gx), ("gear_y", self.gy)):
            prefs[k] = str(v)
        prefs["cfg_min"] = "1" if self.minimized else "0"
        prefs["cfg_tab"], prefs["cfg_page"] = self.tab, self.page or ""; prefs["snap"] = "1" if SNAP.enabled else "0"
    def fold(self):
        x, y = self.pos()
        if x is not None: self.x, self.y = x, y
        self.gx, self.gy = self.x, self.y; self.build_gear(self.gx, self.gy); self.host.save_prefs()
    def unfold(self):
        x, y = self.pos()
        if x is not None: self.gx, self.gy = x, y
        self.docked = False; self.host.dock_forget(self.DOCK_KEY); self.build_full(self.gx, self.gy)
        self.host.save_prefs()
    def redraw(self):
        if self.mode != "full": self.unfold(); return
        x, y = self.pos()
        if x is not None: self.x, self.y = x, y
        self.build_full(self.x, self.y); self.host.save_prefs()
    def show_settings(self, key): self.request = key
    def refresh(self, key):
        self.forget_measure(key)
        if self.shown_page == key: self.dirty = self.stale_page = key
    def close(self):
        self.closing = True; self._leave_page(); g, self.g = self.g, None; Kit.dispose(g)
        self.docked, self.link_state = False, None; API.SetSharedVar(self.LINK_STATE, "off")
    def poll(self):
        if self.closing: return
        if not Kit.is_open(self.g):
            if self.host.stopping(): return
            self.shown_page = None; self.build_gear(self.gx, self.gy); return
        g = self.g; self.link_tick()
        if self.g is not g and not Kit.is_open(self.g): return
        if self.request is not None:
            key, self.request = self.request, None; self.tab, self.page = "settings", key; self.redraw(); return
        if self.request_tab is not None:
            tab, self.request_tab = self.request_tab, None
            if tab in ("modules", "settings"): self.tab = tab
            self.redraw(); return
        if self.mode == "gear":
            now = time.time()
            if not self.docked and (self.gear_clicked or self.gear_pos is None or now >= self.gear_look
                                    or SNAP.pressed() is not False):
                self.gear_look = now + 0.5; p = self.pos()
                if p != self.gear_pos:
                    if self.gear_pos is not None: self.gear_moved = now
                    self.gear_pos = p
            if self.gear_clicked:
                self.gear_clicked = False
                if now - self.gear_moved > 0.35: self.unfold()
            return
        if self.prof_redraw: self.prof_redraw = False; self.redraw(); return
        if self.redraw_req:
            self.redraw_req = False
            if self.tab == "settings": self.redraw(); return
        if self.resize_at and time.time() - self.resize_at >= self.SETTLE and not SNAP.pressed():
            self.resize_at = 0.0; self._relayout(); return
        if self._poll_buttons(): return
        self._fld_due = self.host.poll_due(self._fld_gate); self._poll_profiles()
        if self.search_tb is not None and self._fld_due and self._poll_search(): return
        if self.lag_lbl is not None and time.time() >= self.lag_next:
            self.lag_next = time.time() + 1.0; running = self.host.active
            if running:
                worst = max(running, key=lambda s: s.worst_ms)
                text = "%d modules on; slowest lately: %s, %d ms" % (len(running), worst.title, worst.worst_ms)
            else: text = "No modules on"
            Kit.set_text(self.lag_lbl, text)
        if self.grid_tb is not None and self._fld_due:
            try: t = self.grid_tb.Text
            except Exception: t = None
            if t != self.grid_text:
                self.grid_text = t
                try: v = int(str(t or "").strip() or 0)
                except Exception: v = 0
                if 8 <= v <= 512 and v != self.host.grid_size():
                    self.host.prefs["grid"] = str(v); self.host.save_prefs()
                    if self.host.grid is not None: self.host.grid.redraw()
        now = time.time()
        if self.box_hit or now >= self.box_next or not Kit.clicks_seen:
            self.box_hit = False; self.box_next = now + self.BOX_EVERY
            if self._poll_boxes(): return
        s = self.host.page_slot(self.shown_page) if self.shown_page is not None else None
        if self.stale_page is not None and self.stale_page == self.shown_page: s = None
        if s is not None and s.api is not None and s.api.get("poll_config"):
            if self._pp_key != self.shown_page: self._pp_key = self.shown_page; self._pp_gate[0] = 0.0
            if self.host.poll_due(self._pp_gate, s.api.get("poll_every")):
                try: s.api["poll_config"]()
                except Exception as ex: self._settings_error(s, "update", ex)
        if self.dirty is not None and self.dirty == self.shown_page: self.redraw()
    def _poll_search(self):
        try: t = str(self.search_tb.Text or "")
        except Exception: return False
        now = time.time()
        if t != self.search_text:
            if self.search_text is not None: self.search_at = now
            self.search_text = t; return False
        if self.search_at and now - self.search_at >= SEARCH_SETTLE:
            self.search_at = 0.0
            if t.strip().lower() != self.mod_search.strip().lower():
                self.mod_search = t.strip(); self.search_focus = True; self.redraw(); return True
        return False
    BOX_EVERY = 1.0
    def _hook_box(self, cb):
        if cb is None: return
        def hit(*args): Kit.clicks_seen = True; self.box_hit = True; HOST.poke()
        G.AddControlOnClick(cb, hit)
    def _poll_boxes(self):
        if self.snap_cb is not None:
            try: v = bool(self.snap_cb.IsChecked)
            except Exception: v = SNAP.enabled
            if v != SNAP.enabled:
                SNAP.enabled = v
                if not v: SNAP.links.clear()
                self.host.save_prefs()
        seen = self.seen
        for s, pk, cb in self.box_list + self.part_boxes:
            sk, cur = (s.key, s.enabled) if pk is None else ("%s.%s" % (s.key, pk), bool(s.parts_on.get(pk)))
            try: v = bool(cb.IsChecked)
            except Exception: v = cur
            if v != seen.get(sk):
                seen[sk] = v
                if pk is not None: self.host.part_set(s.key, pk, v)
                elif v: self.host.enable(s.key)
                else: self.host.disable(s.key)
                if not Kit.is_open(self.g) or self.mode != "full": return True
            elif v != cur: safe(lambda: cb.SetIsChecked(cur)); seen[sk] = cur
        return False
    def _poll_buttons(self):
        store = self.store
        if Kit.clicks_seen and True not in store[1].values(): return False
        if Kit.was_clicked(store, "close"): self.host.save_prefs(); self.host.quitting = True; return True
        if Kit.was_clicked(store, "min"): self.host.dock_forget(self.DOCK_KEY); self.fold(); return True
        if Kit.was_clicked(store, "tobar"): self.fold_to_bar(); return True
        for key, d in (("scale_down", -1), ("scale_up", 1), ("scale_reset", 0)):
            if Kit.was_clicked(store, key): self._step_scale(d); return True
        for key, _ in self.TABS:
            if Kit.was_clicked(store, "tab_" + key) and key != self.tab: self.tab = key; self.redraw(); return True
        for bkey, key in self.page_keys:
            if Kit.was_clicked(store, bkey) and key != self.shown_page: self.page = key; self.redraw(); return True
        for bkey, key in self.fold_keys:
            if Kit.was_clicked(store, bkey):
                s = dict.get(self.host.by_key, key)
                if s is not None: s.folded = not s.folded
                self.redraw(); return True
        for bkey, key, zones in self.zone_keys:
            if Kit.was_clicked(store, bkey):
                cur = LAYOUT.zone_of(key); i = zones.index(cur) if cur in zones else 0
                nxt = zones[(i + 1) % len(zones)] if zones else None; mz = LAYOUT._map_zone()
                if nxt is not None and key != "worldmap" and nxt == mz and len(zones) > 2:
                    nxt = zones[(i + 2) % len(zones)]
                LAYOUT.assign_to(key, nxt); self.redraw(); return True
        return False


class AlonePage(object):
    W = 460; prof_stale = False; mode = "alone"
    def __init__(self, s):
        self.s, self.want, self.dirty, self.parts, self.check_at = s, False, False, None, 0.0
        self.st = {"minimized": False, "shutting": False, "docked": False, "queue": []}
        self.win = {"g": None, "c": {}, "store": ({}, {})}
        self.wnd = Kit.Window(s.key + "_alone", s.title + " settings", self.st, self.win, self.build,
                              "VirtueAssistant_alone_pos", mini=(260, 46), lock=False, owner=False, close_tip="Close")
    def __getattr__(self, name): return lambda *args, **kw: None
    def api(self): return self.s.api if self.s.api and self.s.api.get("build_config") else None
    def show_settings(self, key): self.want, self.st["minimized"] = True, False
    def refresh(self, key=None): self.dirty = True
    def rows(self): return (("PARTS", [("check", p[0], p[1], p[2]) for p in self.s.parts]),) if self.s.parts else ()
    def build(self):
        api, M = self.api(), Kit.MARGIN; w = self.W - 2 * M; top = M + 30 + Kit.GAP; self.parts = None
        ph = Kit.Form.height(self.rows(), w); ph += Kit.GAP if ph else 0
        g, store, c = self.wnd.begin(self.W, top + ph + int(api["config_height"](w) or 0) + M)
        if not self.st["minimized"]:
            self.wnd.frame(g, settings=False); self.parts = Kit.Form(g, M, top, w, dict(self.s.parts_on), self.rows())
            api["build_config"](g, M, top + ph, w)
        self.wnd.end(g)
    def poll_parts(self):
        s = self.s; new = self.parts.read(); changed = [k for k in new if s.parts_on.get(k) != new[k]]
        for k in changed: HOST.part_set(s.key, k, new[k])
        if changed: Kit.put_var(ALONE_PARTS % s.key, ",".join(s.parts_wanted())); self.dirty = True
    def poll(self):
        now = time.time()
        if now >= self.check_at:
            self.check_at = now + 2.0
            if HOST.suite_alive():
                API.SysMsg("%s: %s started, so this copy stops." % (self.s.title, APP_NAME), Kit.HUE_INFO)
                HOST.disable(self.s.key); return
        if self.api() is None: return
        q = self.st["queue"]
        while q:
            action = q.pop(0)
            if action != "to_bar": self.wnd.action(action)
        if self.want or (self.dirty and self.win["g"] is not None): self.want = self.dirty = False; self.build()
        if self.win["g"] is None: return
        if Kit.was_clicked(self.win["store"], "close"): self.close()
        elif not self.st["minimized"]:
            if self.parts is not None: self.poll_parts()
            try: self.s.api["poll_config"]()
            except Exception as ex: HOST._tell("%s: settings error: %s" % (self.s.title, ex))
    def close(self):
        if self.win["g"] is None: return
        if self.api().get("config_closed"): self.s.api["config_closed"]()
        self.wnd.close()


class HubWindow(object):
    W = 372; MINI_W, MINI_H = 240, 46
    def __init__(self, host):
        self.host = host; self.g = None; self.H = 0; self.sections = []; self.stores = {}; self.store = ({}, {})
        self.x, self.y = Kit.adapt(host.pref_int("hub_x", 100), host.pref_int("hub_y", 100), self.W, self.MINI_H)
        self.minimized = host.pref_int("hub_min", 0) == 1 or host.dock_wanted("hub")
        self.docked = self.dirty = self.closing = False; self._gates = {}
        host.dock_add("hub", {"title": "Ultima Tracker", "icon": 0x1057, "always": True,
                              "state": self.state, "show": self.show, "dock": self.dock,
                              "undock": self.undock, "minimize": self.minimize, "on": self.open_modules})
    def add(self, key, title, hooks): self.remove(key); self.sections.append((key, title, hooks)); self.dirty = True
    def remove(self, key):
        keep = [s for s in self.sections if s[0] != key]
        if len(keep) == len(self.sections): return
        self.sections = keep; self.stores.pop(key, None)
        if not keep: self._close_window()
        else: self.dirty = True
    def refresh(self): self.dirty = True
    def title(self): return self.sections[0][1] if len(self.sections) == 1 else "Ultima Tracker"
    def state(self):
        if not self.sections or self.g is None: return None
        return "docked" if self.docked else ("minimized" if self.minimized else "open")
    def show(self): self.docked = self.minimized = False; self.dirty = True
    def dock(self):
        if not self.sections: return
        self.minimized = self.docked = True; self.dirty = True
    def undock(self):
        if self.docked: self.docked = False; self._visible(True)
    def minimize(self):
        if not self.sections: return
        self.minimized, self.docked = True, False; self.dirty = True
    def toggle_min(self):
        self.minimized = not self.minimized; self.docked = False; self.host.dock_forget("hub"); self.dirty = True
    def open_modules(self):
        if self.host.config is not None: self.host.config.request_tab = "modules"
    def _visible(self, on):
        g = self.g
        if Kit.is_open(g): Kit.set(g, "IsVisible", bool(on))
    def _pos(self):
        g = self.g
        if Kit.is_open(g):
            try: self.x, self.y = int(g.GetX()), int(g.GetY())
            except Exception: pass
    def _leave(self):
        for key, title, hooks in self.sections:
            st_ = self.stores.get(key)
            if st_ is not None and hooks.get("poll"): safe(lambda: hooks["poll"](st_))
            if key in self.stores and hooks.get("closed"): safe(hooks["closed"])
        self.stores = {}
    def _close_window(self): self._pos(); self._leave(); g, self.g = self.g, None; Kit.dispose(g); self.docked = False
    def _part_of(self, key):
        m = self.host.old_map.get(key)
        if m is not None and dict.get(self.host.by_key, m[0]) is not None: return m
        return key, None
    def _off(self, key): mk, pk = self._part_of(key); self.host.disable(("%s.%s" % (mk, pk)) if pk is not None else key)
    def _error(self, key, ex):
        mk, pk = self._part_of(key); s = dict.get(self.host.by_key, mk)
        if s is not None: self.host.report(s, ex, None, pk)
    def build(self): Kit.on_client(self._build)
    def _build(self):
        self.dirty = False
        if not self.sections: self._close_window(); return
        self._pos(); self._leave(); old = self.g; M, GAP = Kit.MARGIN, Kit.GAP; store = ({}, {})
        g = G.CreateGump(True, True); title = self.title().upper()
        close_tip = "Close %s (turns %s off; the Modules tab turns %s back on)" % (
            self.title(), "them" if len(self.sections) > 1 else "it", "them" if len(self.sections) > 1 else "it")
        if self.minimized:
            w, h = self.MINI_W, self.MINI_H; Kit.add_window_frame(g, w, h, corners=False)
            Kit.add_section(g, 8, 8, w - 16, h - 16); Kit.add_label(g, title, 18, 15, Kit.HUE_TITLE)
            Kit.title_catcher(g, 8, 8, w - 70, h - 16, self.toggle_min, key="hub:mini")
            Kit.art_button(g, store, "min", Kit.ART_RESTORE, w - 60, 15, None, Kit.RESTORE_TIP)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - 44, 12, None, close_tip)
        else:
            w = self.W; IW = w - 2 * M
            heights = [max(20, int(safe(lambda: hooks["height"](IW), 40) or 40)) for key, t, hooks in self.sections]
            h = M + 30 + GAP + sum(heights) + GAP * (len(heights) - 1) + M; Kit.add_window_frame(g, w, h, corners=False)
            Kit.add_section(g, M, M, IW, 30); Kit.add_label(g, title, M + 10, M + 7, Kit.HUE_TITLE)
            Kit.title_catcher(g, M, M, IW - 70 - Kit.DOCK_DX, 30, self.toggle_min, key="hub")
            Kit.dock_button(g, store, w - M - 66, M + 7)
            Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 66, M + 7, None, Kit.MIN_TIP)
            Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 44, M + 4, None, close_tip); y = M + 30 + GAP
            for (key, t, hooks), sh in zip(self.sections, heights):
                st_ = self.stores[key] = ({}, {})
                try: hooks["build"](g, M, y, IW, st_)
                except Exception as ex:
                    Kit.add_section(g, M, y, IW, sh); Kit.add_label(g, "%s: %s" % (t, ex), M + 10, y + 10, Kit.HUE_BAD)
                    self._error(key, ex)
                y += sh + GAP
        self.H = h; self.x, self.y = Kit.place(g, self.x, self.y, w, h); self.g, self.store = g, store
        G.AddControlOnDisposed(g, lambda *a: self._disposed(g)); G.AddGump(g); g.SetInScreen()
        Kit.on_moved(g, self._moved); Kit.dispose(old)
        if self.docked: self._visible(False)
    def _moved(self): self._pos(); self.host.save_prefs()
    def _disposed(self, g):
        if self.g is g and not self.closing:
            self.g = None; self.stores = {}
            for key, t, hooks in list(self.sections): safe(hooks.get("closed", lambda: None)); self._off(key)
    def store_prefs(self, prefs):
        if Client.on_client_thread(): self._pos()
        prefs["hub_x"], prefs["hub_y"] = str(self.x), str(self.y); prefs["hub_min"] = "1" if self.minimized else "0"
    def close(self): self.closing = True; self._close_window()
    def poll(self):
        if self.closing: return
        if self.dirty:
            self.build()
            if self.sections and self.host.pref_int("hub_min", 0) != int(self.minimized): self.host.save_prefs()
        g = self.g
        if g is None: return
        if not Kit.is_open(g): self.g = None; return
        if Kit.clicks_seen and True not in self.store[1].values(): pass
        elif Kit.was_clicked(self.store, "close"):
            self._pos()
            for key, t, hooks in list(self.sections): self._off(key)
            return
        elif Kit.was_clicked(self.store, "min"): self.toggle_min(); self.build(); self.host.save_prefs(); return
        elif Kit.was_clicked(self.store, "tobar"):
            self.host.dock_to_bar("hub", self.title())
            if self.dirty: self.build()
            self.host.save_prefs(); return
        if self.docked or self.minimized: return
        for key, t, hooks in list(self.sections):
            st_ = self.stores.get(key)
            if st_ is not None and hooks.get("poll"):
                gate = self._gates.get(key)
                if gate is None: gate = self._gates[key] = [0.0]
                if not self.host.poll_due(gate, hooks.get("poll_every")): continue
                try: hooks["poll"](st_)
                except Exception as ex: self._error(key, ex)


SNAP_DIST = 16
SNAP_SETTLE = 0.25
SNAP_EVERY = 0.08
SNAP_PRUNE = 2.0


class Snap(object):
    def __init__(self):
        self.gumps = []; self.members = set(); self.last = None; self.drag = {}; self.links = {}; self.button = None
        self.enabled = True; self.next = 0.0; self.prune_at = 0.0; self.moved_cb = {}; self.moved = set()
        self.attached = {}; self._fmap = None; self.no_snap = set()
        self.keep_at = 0.0; self.screen = None; self.by_code = {}; self.dragged = set(); self.droppers = []
        self.drag_end = {}; self.drag_key = {}; self.drag_rect = {}; self.lost = {}
    def add(self, g):
        if g is not None and g not in self.members: self.members.add(g); self.gumps.append(g)
    def on_moved(self, g, fn):
        if g is None: return
        if g not in self.attached: self.add(g)
        self.moved_cb[g] = fn
    def on_drop(self, fn):
        if fn not in self.droppers: self.droppers.append(fn)
    def _tell_moved(self):
        moved, self.moved = self.moved, set(); dragged, self.dragged = self.dragged, set()
        for g in moved:
            fn = self.moved_cb.get(g)
            if fn is None: continue
            if Kit.is_open(g):
                try: fn()
                except Exception: pass
        now = time.time()
        for g in dragged: self.drag_end[g] = now
        if len(self.drag_end) > 32:
            for g in [g for g, t in self.drag_end.items() if now - t > 5.0]: del self.drag_end[g]
        keys, rects = self.drag_key, self.drag_rect; self.drag_key, self.drag_rect = {}, {}
        lost, self.lost = self.lost, {}
        for g in dragged:
            if g in moved and Kit.is_open(g):
                for fn in self.droppers:
                    try: fn(g)
                    except Exception: pass
                continue
            if keys.get(g) is not None and rects.get(g) is not None: lost[g] = (keys[g], rects[g])
        done = set()
        for g, (key, r) in lost.items():
            if key in done: continue
            done.add(key)
            for fn in self.droppers:
                try: fn(None, key=key, rect=r)
                except Exception: pass
    def moved_by_code(self, g):
        if g is None: return
        p = self.pos(g)
        if self.last is not None and p is not None: self.last[g] = p
        self.drag.pop(g, None); self.moved.discard(g); self.by_code[g] = time.time()
    def skip_gump(self, g, keep_fresh=False):
        if not keep_fresh: LAYOUT.fresh_adds.discard(g)
        if g in self.members: self.members.discard(g); self.gumps.remove(g)
    def exempt(self, g):
        if g is None: return
        self.add(g); self.no_snap.add(g); self.links.pop(g, None)
        for f, l in list(self.links.items()):
            if l is g: self.links.pop(f, None)
    def attach(self, follower, leader):
        if follower is None or leader is None or follower is leader: return
        self.skip_gump(follower, keep_fresh=True); self.attached[follower] = leader; self._fmap = None; self.add(leader)
    def detach(self, follower):
        self._fmap = None
        if self.attached.pop(follower, None) is not None and Kit.is_open(follower): self.add(follower)
    def followers(self, g):
        fm = self._fmap
        if fm is not None: lst = fm.get(g); return list(lst) if lst else []
        out = []
        for f, l in list(self.attached.items()):
            if not Kit.is_open(f): self._forget(f)
            elif l is g: out.append(f)
        return out
    def _forget(self, g):
        if g in self.dragged:
            k, r = self.drag_key.get(g), self.drag_rect.get(g)
            if k is not None and r is not None: self.lost[g] = (k, r)
        for d in (self.drag_key, self.drag_rect, self.drag, self.by_code, self.links, self.moved_cb): d.pop(g, None)
        for s in (self.members, Kit._pinned, self.moved, self.dragged, self.no_snap): s.discard(g)
        self._fmap = None; self.attached.pop(g, None)
        for f, l in list(self.attached.items()):
            if l is g: self.attached.pop(f, None)
        if self.last is not None: self.last.pop(g, None)
    def _prune(self):
        live = []
        for g in self.gumps:
            if Kit.is_open(g): live.append(g)
            else: self._forget(g)
        self.gumps = live; return live
    def pressed(self):
        if self.button is None:
            self.button = False
            try:
                m = Client._member(Client._type("ClassicUO.Input.Mouse"), "LButtonPressed"); bool(m[0]())
                self.button = m[0]
            except Exception: pass
        if not self.button: return None
        try: v = self.button()
        except Exception: return None
        return None if v is None else bool(v)
    @staticmethod
    def rect(g): r = Kit.rect(g); return r if r is not None and r[2] > 0 and r[3] > 0 else None
    @staticmethod
    def pos(g): return Kit.pos(g)
    @staticmethod
    def visible(g): return bool(g.IsVisible)
    @staticmethod
    def move(g, x, y): g.SetPos(int(x), int(y)); Kit.note_rect(g, x, y)
    def tick(self, now=None):
        now = time.time() if now is None else now
        if now < self.next and self.next - now <= SNAP_EVERY: return
        self.next = now + SNAP_EVERY
        if LAYOUT.arrange and not self.drag and API.IsKeyPressed("ESCAPE"): LAYOUT.set_arrange(False)
        pressed = self.pressed()
        if pressed is not True:
            if now >= self.keep_at: self.keep_at = now + KEEP_EVERY; self.keep()
            elif (LAYOUT.fresh or LAYOUT.fresh_adds) and LAYOUT.assign:
                self.keep(light=bool(LAYOUT.fresh_adds) and not LAYOUT.fresh)
        if pressed is False and not self.drag:
            self.last = None
            if now >= self.prune_at: self.prune_at = now + SNAP_PRUNE; self._prune()
            return
        if pressed is not True or now >= self.prune_at: self.prune_at = now + SNAP_PRUNE; live = self._prune()
        else: live = self.gumps
        last = self.last
        if last is None:
            last = self.last = {}
            for g in live:
                p = self.pos(g)
                if p is not None: last[g] = p
            return
        drag = self.drag; by_code = self.by_code
        if by_code:
            for g in [g for g, t in by_code.items() if now - t > 1.0]: del by_code[g]
        for g in live:
            p = self.pos(g)
            if p is None: continue
            prev = last.get(g)
            if prev is None: last[g] = p; continue
            if p != prev:
                dx, dy = p[0] - prev[0], p[1] - prev[1]; last[g] = p
                if by_code and g in by_code: del by_code[g]; continue
                if pressed is False: continue
                drag[g] = now; self.moved.add(g); self.dragged.add(g); r = None
                if LAYOUT.loaded:
                    if g not in self.drag_key: self.drag_key[g] = LAYOUT._key_of(g)
                    r = self.rect(g)
                    if r is not None: self.drag_rect[g] = r
                if LAYOUT.arrange: LAYOUT.arrange_hover(g, r)
                if self.enabled and g not in self.no_snap and g not in LAYOUT.held: self.follow(g, dx, dy, set([g]))
            elif g in drag:
                if pressed is False or (pressed is None and now - drag[g] >= SNAP_SETTLE):
                    del drag[g]
                    if self.enabled and g not in self.no_snap and not LAYOUT.takes(g): self.snap(g, live)
        if (self.moved or self.lost) and not drag: self._tell_moved()
    def follow(self, leader, dx, dy, seen):
        links = self.links
        if not links: return
        held = LAYOUT.held
        for g in self.gumps:
            if g in seen or links.get(g) is not leader: continue
            if g in held: links.pop(g, None); continue
            p = self.pos(g)
            if p is None: continue
            seen.add(g); self.move(g, p[0] + dx, p[1] + dy)
            if self.last is not None: self.last[g] = (p[0] + dx, p[1] + dy)
            self.moved.add(g); self.follow(g, dx, dy, seen)
    def snap(self, g, live):
        if self._fmap is not None: return self._snap(g, live)
        self._build_fmap()
        try: return self._snap(g, live)
        finally: self._fmap = None
    def _snap(self, g, live):
        r = self.rect(g)
        if r is None: return
        x, y, w, h = r; corner = None; ex = ey = None; links = self.links; targets = []
        for o in live:
            if o is g or links.get(o) is g or not self.visible(o) or o in self.no_snap: continue
            targets.append((o, o))
            for f in self.followers(o):
                if f is not g and self.visible(f): targets.append((f, o))
        for o, lead in targets:
            ro = self.rect(o)
            if ro is None: continue
            ox, oy, ow, oh = ro
            for tx, ty in ((ox + ow, oy), (ox + ow, oy + oh - h), (ox - w, oy),
                           (ox - w, oy + oh - h), (ox, oy + oh), (ox + ow - w, oy + oh),
                           (ox, oy - h), (ox + ow - w, oy - h)):
                d = max(abs(x - tx), abs(y - ty))
                if d <= SNAP_DIST and (corner is None or d < corner[0]): corner = (d, tx, ty, lead)
            if y < oy + oh + SNAP_DIST and oy < y + h + SNAP_DIST:
                for tx in (ox + ow, ox - w, ox, ox + ow - w):
                    d = abs(x - tx)
                    if d <= SNAP_DIST and (ex is None or d < ex[0]): ex = (d, tx, lead)
            if x < ox + ow + SNAP_DIST and ox < x + w + SNAP_DIST:
                for ty in (oy + oh, oy - h, oy, oy + oh - h):
                    d = abs(y - ty)
                    if d <= SNAP_DIST and (ey is None or d < ey[0]): ey = (d, ty, lead)
        if corner is not None: nx, ny, leader = corner[1], corner[2], corner[3]
        else: nx = ex[1] if ex else x; ny = ey[1] if ey else y; leader = (ex or ey or (None, None, None))[2]
        if leader is None: links.pop(g, None); nx, ny = self.snap_screen(x, y, w, h)
        else: links[g] = leader
        nx, ny = Kit.clamp(nx, ny, w, h)
        if (nx, ny) != (x, y):
            self.move(g, nx, ny)
            if self.last is not None: self.last[g] = (nx, ny)
            self.follow(g, nx - x, ny - y, set([g]))
    def keep(self, light=False):
        W, H = Kit.screen()
        if W <= 0 or H <= 0: return
        live = self._prune(); Kit.prune_pending()
        try: self._keep_body(W, H, live, light)
        finally: self._fmap = None
    def _build_fmap(self):
        fm = {}
        for f, l in list(self.attached.items()):
            if not Kit.is_open(f): self._forget(f)
            else:
                lst = fm.get(l)
                if lst is None: fm[l] = [f]
                else: lst.append(f)
        self._fmap = fm
    def _keep_body(self, W, H, live, light=False):
        self._build_fmap(); new = None
        if light:
            new = set(LAYOUT.fresh_adds); att = self.attached
            for g in list(new):
                l = att.get(g)
                if l is not None: new.add(l)
        try: Kit.scroll_sweep()
        except Exception: pass
        old = self.screen
        if old != (W, H):
            new = None; self.screen = (W, H)
            if old is not None:
                for g in live:
                    if g in self.drag: continue
                    r = self.rect(g)
                    if r is None: continue
                    x, y, w, h = r; nx = Kit.remap_axis(x, w, old[0], W); ny = Kit.remap_axis(y, h, old[1], H)
                    if (nx, ny) != (x, y): self._shift(g, nx - x, ny - y)
            Kit.note_screen((W, H))
        held = LAYOUT.held
        for g in live:
            if new is not None and g not in new: continue
            if g not in self.drag and g not in held: self.keep_one(g)
        try: LAYOUT.keep(W, H)
        except Exception as ex: HOST._tell("%s: layout error: %s%s" % (APP_NAME, ex, _error_where()))
        if (self.moved or self.lost) and not self.drag: self._tell_moved()
    def keep_one(self, g):
        r = self.rect(g)
        if r is None: return False
        x0, y0, x1, y1 = r[0], r[1], r[0] + r[2], r[1] + r[3]
        for f in self.followers(g):
            rf = self.rect(f)
            if rf is not None and self.visible(f):
                x0, y0 = min(x0, rf[0]), min(y0, rf[1]); x1, y1 = max(x1, rf[0] + rf[2]), max(y1, rf[1] + rf[3])
        nx, ny = Kit.clamp(x0, y0, x1 - x0, y1 - y0)
        if (nx, ny) == (x0, y0): return False
        self._shift(g, nx - x0, ny - y0); return True
    def _shift(self, g, dx, dy):
        for w in [g] + self.followers(g):
            p = self.pos(w)
            if p is None: continue
            self.move(w, p[0] + dx, p[1] + dy)
            if self.last is not None: self.last[w] = (p[0] + dx, p[1] + dy)
        self.moved.add(g)
    @staticmethod
    def near_anchor(x, y, w, h):
        found = [(max(abs(ax - x), abs(ay - y)), ax, ay) for ax, ay in Kit.anchor_targets(w, h)]
        best = min(found, key=_first) if found else None
        return best if best is not None and best[0] <= SNAP_ANCHOR else None
    def snap_screen(self, x, y, w, h):
        W, H = Kit.screen()
        if W <= 0 or H <= 0: return x, y
        best = Snap.near_anchor(x, y, w, h)
        if best is not None: return best[1], best[2]
        nx, ny = x, y
        for tx in (0, max(0, W - w)):
            if abs(tx - x) <= SNAP_DIST: nx = tx
        for ty in (0, max(0, H - h)):
            if abs(ty - y) <= SNAP_DIST: ny = ty
        if HOST.grid_shown():
            step = HOST.grid_size()
            def on_line(lo, size, cur):
                cands = []
                for edge, back in ((lo, 0), (lo + size, size)):
                    line = int(round(float(edge) / step)) * step
                    if abs(line - edge) <= SNAP_DIST: cands.append((abs(line - edge), line - back))
                return min(cands)[1] if cands and cur == lo else cur
            nx, ny = on_line(x, w, nx), on_line(y, h, ny)
        return nx, ny


class Grid(object):
    MINOR, MAJOR = 0.16, 0.34; CROSS, MARK = 0.55, 0.75; MARK_W = 10
    def __init__(self, host): self.host = host; self.g = None; self.shown = False; self.drawn = None
    @staticmethod
    def show_overlay(g, x, y, w, h, under=False):
        g.SetRect(x, y, w, h); g.SetAcceptMouseInput(False); g.CanMove = False
        if under:
            try: import System; g.LayerOrder = System.Enum.Parse(g.LayerOrder.GetType(), "Under")
            except Exception: pass
        G.AddGump(g); SNAP.skip_gump(g)
    def toggle(self): self.hide() if self.shown else self.show()
    def show(self): self.shown = True; Kit.on_client(self.build)
    def hide(self): self.shown = False; g, self.g = self.g, None; Kit.dispose(g)
    def redraw(self):
        if self.shown: Kit.on_client(self.build)
    def tick(self):
        if self.shown and self.drawn is not None:
            W, H = Kit.screen()
            if (W, H, self.host.grid_size()) != self.drawn: self.redraw()
    def build(self):
        W, H = Kit.screen(); step = self.host.grid_size(); old, self.g = self.g, None
        if W <= 0 or H <= 0: Kit.dispose(old); return
        g = G.CreateGump(False, False)
        for n, x in enumerate(range(step, W, step), 1):
            Kit.add_box(g, x, 0, 1, H, self.MAJOR if n % 4 == 0 else self.MINOR)
        for n, y in enumerate(range(step, H, step), 1):
            Kit.add_box(g, 0, y, W, 1, self.MAJOR if n % 4 == 0 else self.MINOR)
        Kit.add_box(g, W // 2, 0, 1, H, self.CROSS, "#FFD700"); Kit.add_box(g, 0, H // 2, W, 1, self.CROSS, "#FFD700")
        m = self.MARK_W
        for ax, ay in Kit.anchor_targets(m, m): Kit.add_box(g, ax, ay, m, m, self.MARK, "#FFD700")
        Kit.add_label(g, "GRID %d px: windows snap to its lines, the screen's corners, edges and centre  (the Action "
                      "Bar's Grid button hides it)" % step, m + 8, m + 4, Kit.HUE_TITLE)
        self.g = g; self.drawn = (W, H, step); Grid.show_overlay(g, 0, 0, W, H, True); Kit.dispose(old)


LAYOUT_VAR = "VirtueAssistant_layout"
LAYOUT_ACTIVE = "VirtueAssistant_layout_active"
LAYOUT_LIST = "VirtueAssistant_layout_list"
LAYOUT_NAMED = "VirtueAssistant_layout_%s"
FRAMES_ACTIVE = "VirtueAssistant_frames_active"
FRAMES_LIST = "VirtueAssistant_frames_list"
FRAMES_NAMED = "VirtueAssistant_frames_%s"
LAYOUT_OPTS = "VirtueAssistant_layout_opts"
LAYOUT_EDITOR_POS = "VirtueAssistant_layout_editor_pos"
LAYOUT_DEFAULT = "Default"
LAYOUT_MIRRORED = "Mirrored"
LAYOUT_MINE = "Default (mine)"
LAYOUT_GONE = frozenset(("spelltimers", "bandage", "swing"))
WINDOWS_DEFAULT = ("L1=character;L2=bag;C1=unitframes.player;C2=unitframes.target;C4=actionbar;"
                   "R1=worldmap;R2=ultima.friend,ultima.neutral,ultima.foe;R3=meters")
WINDOWS_MIRRORED = ("L1=worldmap;L2=ultima.friend,ultima.neutral,ultima.foe,meters;"
                    "C1=unitframes.player;C2=unitframes.target;C4=actionbar;R1=character;R2=bag")
SIDE_MIN, SIDE_MAX, SIDE_SHARE = 240, 440, 0.22
SPILL_MIN, SPILL_MAX, SPILL_SHARE = 240, 360, 0.12
CENTRE_MIN_SHARE = 0.40
TOP_MIN, TOP_MAX, BOT_MIN, BOT_MAX, STRIP_SHARE = 110, 180, 100, 160, 0.14
LEFT_SLOTS = (("L1", 0.32, 260, "w", 2), ("L2", 0.38, 180, "w", 1), ("L3", 0.30, 160, "r", 0))
RIGHT_SLOTS = (("R1", 0.32, 200, "w", 2), ("R2", 0.40, 240, "w", 3), ("R3", 0.28, 120, "w", 1))
MINI_BAR = 46
ZONE_MIN_W, ZONE_MIN_H = 96, 64
ZONE_COLORS = {"w": "#3A78C8", "k": "#3AA060", "r": "#C88A3A"}
ZONE_KINDS = (("w", "window"), ("k", "keep clear"), ("r", "reserved"))
ZONE_STACKS = (("d", "down"), ("u", "up"), ("r", "right"), ("l", "left"))
SHRINK_MAX = 6


def ratio_class(W, H):
    if W <= 0 or H <= 0: return "wide"
    r = float(W) / float(H); return "narrow" if r < 1.5 else "wide" if r < 2.0 else "ultrawide"


def _clampv(v, lo, hi): return max(lo, min(hi, v))


def _ordinal(n):
    n = int(n)
    if n <= 0: return "never"
    if n % 100 in (11, 12, 13): return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


class Zone(object):
    __slots__ = ("id", "kind", "rect", "pins", "min", "stack", "prio", "px", "squeezed", "fit",
                 "hug", "arch", "overlap", "lock")
    def __init__(self, id, kind="w", rect=(0, 0, 200, 200), pins="", mins=(0, 0), stack="d",
                 prio=0, fit="w", hug=False, arch=False, overlap=False, lock=False):
        self.id = str(id); self.kind = kind if kind in ("w", "k", "r") else "w"; self.rect = tuple(int(v) for v in rect)
        self.pins = "".join(c for c in str(pins or "").upper() if c in "LTRBXY")
        self.min = (int(mins[0]), int(mins[1])); self.stack = stack if stack in ("d", "u", "r", "l") else "d"
        self.prio = max(0, min(SHRINK_MAX, int(prio))); self.fit = fit if fit in ("w", "s", "n") else "w"
        self.hug = bool(hug) and self.kind == "w"; self.arch = bool(arch) and self.kind == "k"
        self.overlap = bool(overlap); self.lock = bool(lock); self.px = None; self.squeezed = False
    def kind_name(self): return dict(ZONE_KINDS)[self.kind]
    def stack_name(self): return dict(ZONE_STACKS)[self.stack]
    def copy(self):
        z = Zone(self.id, self.kind, self.rect, self.pins, self.min, self.stack, self.prio,
                 self.fit, self.hug, self.arch, self.overlap, self.lock)
        z.px = tuple(self.px) if self.px else None; return z
    def set_px(self, x, y, w, h, W, H):
        w, h = max(1, int(w)), max(1, int(h))
        if W > 0: w = min(w, W); x = _clampv(int(x), 0, W - w)
        if H > 0: h = min(h, H); y = _clampv(int(y), 0, H - h)
        self.px = (int(x), int(y), w, h)
        if W > 0 and H > 0:
            self.rect = (int(round(1000.0 * x / W)), int(round(1000.0 * y / H)),
                         int(round(1000.0 * w / W)), int(round(1000.0 * h / H)))
    def note_pins(self, W, H):
        if not self.px or W <= 0 or H <= 0: return
        x, y, w, h = self.px
        self.pins = "".join(c for c, d in (("L", x), ("T", y), ("R", W - (x + w)), ("B", H - (y + h)),
                                           ("X", abs((x + w / 2.0) - W / 2.0)), ("Y", abs((y + h / 2.0) - H / 2.0)))
                            if d <= SNAP_DIST)
    def save_text(self):
        n = 4 if self.overlap or self.lock else (2 if self.hug or self.arch else 0)
        extra = "".join(":%d" % v for v in (self.hug, self.arch, self.overlap, self.lock)[:n])
        return "%s:%s:%d,%d,%d,%d:%s:%d,%d:%s:%d:%s%s" % (
            self.id.replace(":", " ").replace(";", " "), self.kind, self.rect[0], self.rect[1],
            self.rect[2], self.rect[3], self.pins, self.min[0], self.min[1], self.stack, self.prio, self.fit, extra)
    @staticmethod
    def parse(text):
        try:
            f = text.split(":")
            if len(f) < 7 or not f[0].strip(): return None
            rect = [int(v) for v in f[2].split(",")]; mn = [int(v) for v in f[4].split(",")]
            if len(rect) != 4 or len(mn) != 2 or rect[2] <= 0 or rect[3] <= 0: return None
            fit = f[7].strip() if len(f) > 7 else "w"
            hug, arch, overlap, lock = [len(f) > i and f[i].strip() == "1" for i in (8, 9, 10, 11)]
            return Zone(f[0].strip(), f[1].strip(), rect, f[3], mn, f[5].strip(), int(f[6]), fit,
                        hug, arch, overlap, lock)
        except Exception: return None


class ZoneSet(object):
    def __init__(self, name, zones=None, grid=GRID_DEFAULT, screen=(0, 0), generated=False):
        self.name = str(name); self.zones = list(zones or []); self.grid = int(grid or GRID_DEFAULT)
        self.screen = (int(screen[0]), int(screen[1])); self.generated = generated; self.skipped = []; self.ver = 2
        self.needs = {}
    def by_id(self, zid):
        for z in self.zones:
            if z.id == zid: return z
        return None
    def ids(self): return [z.id for z in self.zones]
    def copy(self, name=None):
        out = ZoneSet(name or self.name, [z.copy() for z in self.zones], self.grid, self.screen, self.generated)
        out.ver = self.ver; return out
    def save_text(self):
        return "grid=%d,screen=%dx%d,v=%d;" % (self.grid, self.screen[0], self.screen[1], self.ver) + \
            ";".join(z.save_text() for z in self.zones)
    @staticmethod
    def parse(name, text):
        text = str(text or "").strip()
        if not text: return None
        parts = text.split(";"); grid, screen, ver = GRID_DEFAULT, (0, 0), 1; head = parts[0]
        if head.startswith("grid="):
            parts = parts[1:]
            for item in head.split(","):
                try:
                    k, v = item.split("=", 1)
                    if k == "grid": grid = int(v)
                    elif k == "screen": w, h = v.lower().split("x"); screen = (int(w), int(h))
                    elif k == "v": ver = int(v)
                except Exception: pass
        zs = ZoneSet(name, [], grid, screen); zs.ver = ver
        for p in parts:
            if not p.strip(): continue
            z = Zone.parse(p)
            if z is None: zs.skipped.append(p.split(":")[0].strip() or "?")
            elif zs.by_id(z.id) is None: zs.zones.append(z)
        return zs
    @staticmethod
    def default(W, H, occupied=(), game_grows=True):
        zs = ZoneSet(LAYOUT_DEFAULT, [], GRID_DEFAULT, (W, H), generated=True)
        if W <= 0 or H <= 0: return zs
        occupied = set(occupied); cls = ratio_class(W, H)
        if cls == "narrow": side, spill = SIDE_MIN, 0
        else:
            side = int(_clampv(SIDE_SHARE * W, SIDE_MIN, SIDE_MAX))
            spill = (int(_clampv(SPILL_SHARE * W, SPILL_MIN, SPILL_MAX)) if cls == "ultrawide" else 0)
        if W - 2 * side - 2 * spill < CENTRE_MIN_SHARE * W:
            spill = 0
            if W - 2 * side < CENTRE_MIN_SHARE * W: side = max(SIDE_MIN, int((W - CENTRE_MIN_SHARE * W) / 2))
        lx, rx = spill, W - spill - side; cx, cw = spill + side, W - 2 * (spill + side)
        top_h = int(_clampv(STRIP_SHARE * H, TOP_MIN, TOP_MAX)); bot_h = int(_clampv(STRIP_SHARE * H, BOT_MIN, BOT_MAX))
        def add(z, x, y, w, h): z.set_px(x, y, w, h, W, H); z.note_pins(W, H); zs.zones.append(z); return z
        def band(x, slots):
            heights = ZoneSet._band_heights(H, slots, occupied); y = 0
            for (zid, share, mn, kind, prio), (h, squeezed) in zip(slots, heights):
                add(Zone(zid, kind, (0, 0, 1, 1), "", (SIDE_MIN, mn), "d", prio), x, y, side, h).squeezed = squeezed
                y += h
        band(lx, LEFT_SLOTS); half = cw // 2
        for zid, x, w, p in (("C1", cx, half, 3), ("C2", cx + half, cw - half, 2)):
            add(Zone(zid, "w", (0, 0, 1, 1), "T", (300, TOP_MIN), "d", p), x, 0, w, top_h)
        gx, gw = cx, cw
        if game_grows:
            if not any(s[0] in occupied for s in LEFT_SLOTS if s[3] == "w"): gx, gw = 0, gw + cx
            if not any(s[0] in occupied for s in RIGHT_SLOTS if s[3] == "w"): gw = W - gx
        add(Zone("C3", "k", (0, 0, 1, 1), "XY", (0, 0), "d", 0), gx, top_h, gw, H - top_h - bot_h)
        add(Zone("C4", "w", (0, 0, 1, 1), "B", (600, BOT_MIN), "r", 1), cx, H - bot_h, cw, bot_h); band(rx, RIGHT_SLOTS)
        if spill:
            for zid, x in (("L0", 0), ("R0", W - spill)):
                add(Zone(zid, "w", (0, 0, 1, 1), "", (SPILL_MIN, 120), "d", 1), x, 0, spill, H)
        return zs
    @staticmethod
    def _band_heights(H, slots, occupied):
        n = len(slots); room = H; any_win = any(zid in occupied for zid, sh, mn, kind, prio in slots if kind == "w")
        share, mins = [], []
        for zid, sh, mn, kind, prio in slots:
            empty = kind == "w" and zid not in occupied and any_win; share.append(0.0 if empty else float(sh))
            mins.append(46 if empty else int(mn))
        squeezed = [False] * n
        order = sorted([i for i in range(n) if slots[i][4] > 0 and slots[i][3] == "w"], key=lambda i: slots[i][4])
        while sum(mins) > room and order:
            i = order.pop(0)
            if mins[i] > MINI_BAR: mins[i] = MINI_BAR; squeezed[i] = True; share[i] = 0.0
        total = sum(share) or 1.0; h = [room * sh / total for sh in share]
        for _ in range(n):
            short = [(i, mins[i] - h[i]) for i in range(n) if h[i] < mins[i]]
            if not short: break
            need = sum(d for i, d in short); fixed = set(i for i, d in short)
            for i, d in short: h[i] = mins[i]
            donors = [i for i in range(n) if i not in fixed and h[i] > mins[i]]
            pool = sum(h[i] - mins[i] for i in donors)
            if pool <= 0: break
            take = min(need, pool)
            for i in donors: h[i] -= take * (h[i] - mins[i]) / pool
        for i in range(n):
            if slots[i][3] == "r" and h[i] > slots[i][1] * room:
                extra, h[i] = h[i] - slots[i][1] * room, slots[i][1] * room
                takers = [j for j in range(n) if slots[j][3] == "w" and not squeezed[j] and share[j] > 0]
                if takers:
                    pool = sum(share[j] for j in takers) or 1.0
                    for j in takers: h[j] += extra * share[j] / pool
                else:
                    takers = [j for j in range(n) if slots[j][3] == "w" and not squeezed[j]]
                    pool = sum(slots[j][1] for j in takers) or 1.0
                    for j in takers: h[j] += extra * slots[j][1] / pool
        out = [int(round(v)) for v in h]; extra = room - sum(out)
        if out and extra: out[out.index(max(out))] += extra
        return [(max(1, out[i]), squeezed[i]) for i in range(n)]
    def reflow(self, W, H, step):
        if W <= 0 or H <= 0: return
        step = max(8, int(step or GRID_DEFAULT))
        if self.needs:
            drawn = [(z, z.rect) for z in self.zones]; self.needs, needs = {}, self.needs; self.reflow(W, H, step)
            self.needs = needs; self._apply_needs(W, H); self._keep_clear(W, H)
            for z, r in drawn: z.rect = r
            return
        oldW, oldH = self.screen if self.screen[0] > 0 and self.screen[1] > 0 else (W, H)
        flush = self._flush_pairs(oldW, oldH)
        def on_grid(v, limit): v = int(round(float(v) / step)) * step; return _clampv(v, 0, limit)
        for z in self.zones:
            l, t, w, h = z.rect; x0, y0 = on_grid(W * l / 1000.0, W), on_grid(H * t / 1000.0, H)
            x1, y1 = on_grid(W * (l + w) / 1000.0, W), on_grid(H * (t + h) / 1000.0, H)
            if "L" in z.pins: x0 = 0
            if "T" in z.pins: y0 = 0
            if "R" in z.pins: x1 = W
            if "B" in z.pins: y1 = H
            if "X" in z.pins and "L" not in z.pins and "R" not in z.pins:
                half = (x1 - x0) // 2; x0, x1 = W // 2 - half, W // 2 - half + (x1 - x0)
            if "Y" in z.pins and "T" not in z.pins and "B" not in z.pins:
                half = (y1 - y0) // 2; y0, y1 = H // 2 - half, H // 2 - half + (y1 - y0)
            z.px = (x0, y0, max(1, x1 - x0), max(1, y1 - y0))
        for a, b, side in flush:
            za, zb = self.by_id(a), self.by_id(b)
            if za is None or zb is None or za.px is None or zb.px is None: continue
            ax, ay, aw, ah = za.px; bx, by, bw, bh = zb.px
            if side == "h":
                nx = ax + aw; right = W if "R" in zb.pins else bx + bw
                if right - nx >= ZONE_MIN_W: zb.px = (nx, by, right - nx, bh)
            else:
                ny = ay + ah; bottom = H if "B" in zb.pins else by + bh
                if bottom - ny >= ZONE_MIN_H: zb.px = (bx, ny, bw, bottom - ny)
        for z in self.zones:
            if z.kind == "k": continue
            x, y, w, h = z.px
            if w < z.min[0]: w = min(z.min[0], max(w, self._free(z, 0, W) - x))
            if h < z.min[1]: h = min(z.min[1], max(h, self._free(z, 1, H) - y))
            z.set_px(x, y, w, h, W, H); z.squeezed = z.prio > 0 and z.px[3] < z.min[1]
        for z in self.zones:
            if z.kind != "k" and not z.overlap and self.overlaps(z): self.push_clear(z, W, H)
        for z in self.zones:
            if z.kind == "k" and not z.overlap: z.set_px(*(ZoneSet.cut_clear(z, self.zones) + (W, H)))
        for z in self.zones: z.set_px(z.px[0], z.px[1], z.px[2], z.px[3], W, H)
        self.screen = (W, H)
    @staticmethod
    def cut_clear(z, zones):
        x, y, w, h = z.px
        for o in zones:
            if o is z or o.kind != "w" or o.px is None: continue
            ox, oy, ow, oh = o.px
            if ox < x + w and x < ox + ow and oy < y + h and y < oy + oh:
                cut, side = min([(x + w - ox, "R"), ((ox + ow) - x, "L"), (y + h - oy, "B"), ((oy + oh) - y, "T")])
                if side == "R": w -= cut
                elif side == "L": x, w = x + cut, w - cut
                elif side == "B": h -= cut
                else: y, h = y + cut, h - cut
                if w < ZONE_MIN_W or h < ZONE_MIN_H: x, y, w, h = z.px; break
        return x, y, max(1, w), max(1, h)
    def _flush_pairs(self, W, H):
        out = []; px = {}
        for z in self.zones:
            l, t, w, h = z.rect; px[z.id] = (W * l / 1000.0, H * t / 1000.0, W * w / 1000.0, H * h / 1000.0)
        for a in self.zones:
            ax, ay, aw, ah = px[a.id]
            for b in self.zones:
                if a is b: continue
                bx, by, bw, bh = px[b.id]
                if abs(bx - (ax + aw)) <= SNAP_DIST and by < ay + ah and ay < by + bh: out.append((a.id, b.id, "h"))
                if abs(by - (ay + ah)) <= SNAP_DIST and bx < ax + aw and ax < bx + bw: out.append((a.id, b.id, "v"))
        def rank(zid): z = self.by_id(zid); return -len(z.pins) if z else 0
        out.sort(key=lambda p: (rank(p[0]), rank(p[1]))); return out
    def _free(self, z, i, lim):
        r, j = z.px, 1 - i
        for o in self.zones:
            if o is z or o.kind == "k" or o.px is None: continue
            p = o.px
            if p[i] >= r[i] + r[i + 2] and p[j] < r[j] + r[j + 2] and r[j] < p[j] + p[j + 2]: lim = min(lim, p[i])
        return lim
    def overlaps(self, z, px=None):
        x, y, w, h = px or z.px; out = []
        if z.overlap: return out
        for o in self.zones:
            if o is z or o.px is None or o.overlap: continue
            if (z.kind == "r" and o.kind == "k") or (z.kind == "k" and o.kind == "r"): continue
            ox, oy, ow, oh = o.px
            if ox < x + w and x < ox + ow and oy < y + h and y < oy + oh: out.append(o)
        return out
    def push_clear(self, z, W, H, step=None):
        for _ in range(12):
            hits = self.overlaps(z)
            if not hits: return True
            x, y, w, h = z.px; cands = []
            for o in hits:
                ox, oy, ow, oh = o.px
                for nx, ny in (((ox - w), y), ((ox + ow), y), (x, (oy - h)), (x, (oy + oh))):
                    if not (0 <= nx <= W - w and 0 <= ny <= H - h): continue
                    clear = not self.overlaps(z, (nx, ny, w, h))
                    if clear and step:
                        gx, gy = (int(round(float(nx) / step)) * step, int(round(float(ny) / step)) * step)
                        if (0 <= gx <= W - w and 0 <= gy <= H - h and not self.overlaps(z, (gx, gy, w, h))):
                            nx, ny = gx, gy
                    cands.append((0 if clear else 1, abs(nx - x) + abs(ny - y), nx, ny))
            if not cands: return False
            cands.sort(); z.set_px(cands[0][2], cands[0][3], w, h, W, H)
            if cands[0][0] == 0: return True
        return not self.overlaps(z)
    def _keep_clear(self, W, H):
        for z in self.zones:
            if z.kind != "k" or z.overlap or z.px is None: continue
            x, y, w, h = z.px
            for o in self.zones:
                if o is z or o.kind != "w" or o.px is None: continue
                ox, oy, ow, oh = o.px
                if ox >= x + w or x >= ox + ow or oy >= y + h or y >= oy + oh: continue
                if oy + oh >= y + h and oy > y: h = oy - y
                elif oy <= y and oy + oh < y + h: h, y = h - (oy + oh - y), oy + oh
                elif ox + ow >= x + w and ox > x: w = ox - x
                elif ox <= x and ox + ow < x + w: w, x = w - (ox + ow - x), ox + ow
            z.px = (x, y, max(1, w), max(1, h))
    def _apply_needs(self, W, H):
        for z in self.zones:
            need = self.needs.get(z.id)
            if need is None or z.px is None or z.kind == "k": continue
            r = list(z.px)
            for i, pin, S in ((1, "B", H), (0, "R", W)):
                n, a, s, j = need[i], r[i], r[i + 2], 1 - i
                if not n or n <= s: continue
                grow = min(n - s, S - s)
                others = [o for o in self.zones if o is not z and o.kind == "w" and not o.overlap and o.px is not None
                          and o.px[j] < r[j] + r[j + 2] and r[j] < o.px[j] + o.px[j + 2]]
                if pin in z.pins or a + s / 2.0 >= S / 2.0:
                    na = max(0, a - grow)
                    for o in others:
                        p = list(o.px)
                        if p[i] < a and p[i] + p[i + 2] > na:
                            cut = max(p[i] + max(o.min[i], 1), na); p[i + 2] = cut - p[i]; o.px = tuple(p)
                            na = max(na, cut)
                    r[i], r[i + 2] = na, s + (a - na)
                else:
                    ne = min(S, a + s + grow)
                    for o in others:
                        p = list(o.px)
                        if p[i] >= a + s and p[i] < ne:
                            top = min(p[i] + p[i + 2] - max(o.min[i], 1), ne)
                            p[i], p[i + 2] = top, p[i] + p[i + 2] - top; o.px = tuple(p); ne = min(ne, top)
                    r[i + 2] = ne - a
            z.px = tuple(r)
    def fill_gaps(self, W, H, step):
        step = max(8, int(step or GRID_DEFAULT))
        order = sorted(self.zones, key=lambda z: {"w": 0, "r": 1, "k": 2}[z.kind])
        for z in order:
            if z.overlap or z.lock: continue
            r = list(z.px)
            for i, lo, hi, S in ((0, "L", "R", W), (1, "T", "B", H)):
                lim = max([0] + [o.px[i] + o.px[i + 2] for o in self.overlaps_side(z, lo)])
                n = 0 if lim == 0 else ((lim + step - 1) // step) * step
                if n < r[i]: r[i], r[i + 2] = n, r[i + 2] + (r[i] - n)
                lim = min([S] + [o.px[i] for o in self.overlaps_side(z, hi)])
                e = S if lim == S else (lim // step) * step
                if e > r[i] + r[i + 2]: r[i + 2] = e - r[i]
            z.set_px(r[0], r[1], r[2], r[3], W, H)
    def overlaps_side(self, z, side):
        i = 0 if side in ("L", "R") else 1; j, r = 1 - i, z.px
        return [o for o in self.zones if o is not z and o.px is not None and set((z.kind, o.kind)) != set(("r", "k"))
                and o.px[j] < r[j] + r[j + 2] and r[j] < o.px[j] + o.px[j + 2]
                and (o.px[i] + o.px[i + 2] <= r[i] if side in ("L", "T") else o.px[i] >= r[i] + r[i + 2])]
    def even_out(self, z, W, H, step):
        step = max(8, int(step or GRID_DEFAULT)); D = SNAP_DIST
        def run(horizontal):
            same = [o for o in self.zones if o.kind == "w" and o.px is not None and (
                (abs(o.px[1] - z.px[1]) <= D and abs(o.px[3] - z.px[3]) <= D) if horizontal else
                (abs(o.px[0] - z.px[0]) <= D and abs(o.px[2] - z.px[2]) <= D))]
            i = 0 if horizontal else 1; same.sort(key=lambda o: o.px[i]); chain = [z]
            for direction in (1, -1):
                cur = z
                while True:
                    nxt = None
                    for o in same:
                        if o in chain: continue
                        if direction == 1 and abs(o.px[i] - (cur.px[i] + cur.px[i + 2])) <= D: nxt = o
                        elif direction == -1 and abs(o.px[i] + o.px[i + 2] - cur.px[i]) <= D: nxt = o
                    if nxt is None: break
                    chain.append(nxt); cur = nxt
            chain.sort(key=lambda o: o.px[i]); return chain, i
        chain, i = run(True)
        if len(chain) < 2: chain, i = run(False)
        if len(chain) < 2: return len(chain)
        lo = chain[0].px[i]; hi = chain[-1].px[i] + chain[-1].px[i + 2]; n = len(chain); edges = [lo]
        for k in range(1, n):
            e = lo + (hi - lo) * k / float(n); g = int(round(e / step)) * step
            edges.append(g if abs(g - e) <= step / 2.0 and edges[-1] < g < hi else int(round(e)))
        edges.append(hi)
        for k, o in enumerate(chain):
            x, y, w, h = o.px
            if i == 0: o.set_px(edges[k], y, edges[k + 1] - edges[k], h, W, H)
            else: o.set_px(x, edges[k], w, edges[k + 1] - edges[k], W, H)
        return n
    def new_id(self):
        n = len(self.zones) + 1
        while self.by_id("Zone %d" % n) is not None: n += 1
        return "Zone %d" % n


class ClientWin(object):
    KINDS = {"worldmap": ("WorldMapGump",), "journal": ("ResizableJournal",)}
    TITLES = {"worldmap": "TazUO's World Map", "journal": "TazUO's journal"}; INSET = {"worldmap": 4}
    DROPS = ("worldmap",); LOOK_EVERY = 1.0; LOCK_VAR = "Layout_client_locked_%s"; found = {}; looked = {}; errors = {}
    _pt = [None]; _bf = [None]
    @staticmethod
    def point(x, y):
        import System; t = ClientWin._pt[0]
        if t is None:
            t = ClientWin._pt[0] = Tz.T("ClassicUO.Game.UI.Controls.Control").GetProperty("Location").PropertyType
        return System.Activator.CreateInstance(t, System.Array[object]([int(x), int(y)]))
    @staticmethod
    def bounds(raw):
        f = ClientWin._bf[0]
        if f is None:
            f = ClientWin._bf[0] = Tz.T("ClassicUO.Game.UI.Controls.Control").GetField("_bounds",
                                                                                     Client.flags(public=False))
        return f.GetValue(raw)
    def __init__(self, kind, raw):
        self.kind, self.raw = kind, raw; self.own = None; self.tries = 0; self.fail = {}; self.warned = False
        self.mins = None; self._rc = None
    @staticmethod
    def of(kind):
        cw = ClientWin.found.get(kind)
        if cw is not None and cw.IsDisposed: cw = ClientWin.found[kind] = None
        if cw is not None: return cw
        now = time.time()
        if now - ClientWin.looked.get(kind, 0.0) < ClientWin.LOOK_EVERY: return None
        ClientWin.looked[kind] = now
        try: wins = Tz.windows(ClientWin.KINDS[kind]); ClientWin.errors.pop(kind, None)
        except Exception as ex: wins = []; ClientWin.errors[kind] = Tz.why(ex)
        for raw in wins:
            try:
                if not raw.IsDisposed: cw = ClientWin(kind, raw); break
            except Exception: pass
        ClientWin.found[kind] = cw; return cw
    @property
    def IsDisposed(self):
        try: return bool(self.raw.IsDisposed)
        except Exception: return True
    @property
    def IsVisible(self):
        try: return bool(self.raw.IsVisible)
        except Exception: return False
    def rect(self):
        hop = HOST.in_hop
        if hop:
            c = self._rc
            if c is not None and c[0] == HOST.pass_id: return c[1]
        b = ClientWin.bounds(self.raw); r = (int(b.X), int(b.Y), int(b.Width), int(b.Height))
        self._rc = (HOST.pass_id, r) if hop else None; return r
    def GetX(self): return self.rect()[0]
    def GetY(self): return self.rect()[1]
    def GetWidth(self): return self.rect()[2]
    def GetHeight(self): return self.rect()[3]
    def _put_bounds(self, x, y, w, h):
        import System; self.rect(); f = ClientWin._bf[0]; self._rc = None
        f.SetValue(self.raw, System.Activator.CreateInstance(
            f.FieldType, System.Array[object]([int(x), int(y), int(w), int(h)])))
    def SetPos(self, x, y):
        x, y = int(x), int(y); why = None; self._rc = None
        try: self.raw.Location = ClientWin.point(x, y)
        except Exception as ex: why = Tz.why(ex)
        try:
            r = self.rect()
            if r[:2] != (x, y): self._put_bounds(x, y, r[2], r[3]); r = self.rect()
            if r[:2] == (x, y): self.fail.pop("place", None); return True
        except Exception as ex: why = why or Tz.why(ex)
        self.fail["place"] = "it couldn't be moved (%s)" % (why or "the client put it back"); return False
    def _locked(self):
        try: return bool(self.raw.IsLocked)
        except Exception: return None
    def _lock(self, on):
        raw = self.raw; on = bool(on)
        with Kit.quiet:
            if bool(raw.IsLocked) != on: Tz.call(raw, "SetLockStatus", (on,))
        with Kit.quiet:
            if on and raw.CanMove: raw.CanMove = False
            elif not on and not raw.CanMove and self.own is not None and self.own[4]: raw.CanMove = True
    def _min_size(self):
        if self.mins is None:
            self.mins = (int(Typing._get(self.raw, "_minW", None, 0) or 0),
                         int(Typing._get(self.raw, "_minH", None, 0) or 0))
        return self.mins
    def fit(self, w, h, lock=True):
        raw = self.raw
        if self.own is None:
            try:
                lk = self._locked()
                if lk and Kit.get_var(ClientWin.LOCK_VAR % self.kind, "") == "1": lk = False
                self.own = self.rect() + (bool(raw.CanMove), lk)
            except Exception: self.own = None
            Kit.put_var(ClientWin.LOCK_VAR % self.kind, "1")
        self._lock(lock); mw, mh = self._min_size(); w, h = max(int(w), mw, 1), max(int(h), mh, 1)
        try: r = self.rect()
        except Exception as ex: self.fail["size"] = "its size couldn't be read (%s)" % Tz.why(ex); return
        if (r[2], r[3]) == (w, h): self.tries = 0; self.fail.pop("size", None); return
        self.tries += 1
        if self.tries > 4: self.fail["size"] = "it stays %d x %d, not %d x %d" % (r[2], r[3], w, h)
        with Kit.quiet: Tz.put(raw, "_isFullscreen", False)
        p = ClientWin.point(w, h); self._rc = None
        try: Tz.call(raw, "ResizeWindow", (p,))
        except Exception as ex: self.fail["size"] = "it couldn't be resized (%s)" % Tz.why(ex)
    def free(self):
        own, self.own, self.tries = self.own, None, 0; self._rc = None; Kit.put_var(ClientWin.LOCK_VAR % self.kind, "")
        if own is None or self.IsDisposed: return
        try:
            self._lock(bool(own[5]))
            if not own[5]: self.raw.CanMove = own[4]
            Tz.call(self.raw, "ResizeWindow", (ClientWin.point(own[2], own[3]),)); self.SetPos(own[0], own[1])
        except Exception: pass
        self.fail = {}
    def report(self):
        if self.fail and not self.warned:
            self.warned = True
            Kit.say("%s couldn't be held in its zone: %s." % (ClientWin.TITLES.get(self.kind, self.kind),
                "; ".join(self.fail[k] for k in ("place", "size") if k in self.fail)), Kit.HUE_BAD)


class Tex(object):
    ok = None; parts = {}; names = set()
    @staticmethod
    def find():
        if Tex.ok is not None: return Tex.ok
        try:
            import clr; import System; static = Client.flags(True); inst = Client.flags(); p = Tex.parts
            lt = Client._type("ClassicUO.Assets.ExternalImageLoader")
            loader = lt.GetProperty("Instance", static).GetValue(None, None)
            p["table"] = lt.GetField("_zipNamedTextures", inst).GetValue(loader)
            p["device"] = lt.GetProperty("GraphicsDevice", inst).GetValue(loader, None)
            p["tex_t"] = Client._type("Microsoft.Xna.Framework.Graphics.Texture2D")
            p["format"] = System.Enum.Parse(Client._type("Microsoft.Xna.Framework.Graphics.SurfaceFormat"), "Color")
            p["set_data"] = [m for m in p["tex_t"].GetMethods() if m.Name == "SetData" and m.IsGenericMethodDefinition
                             and len(m.GetParameters()) == 1][0].MakeGenericMethod(clr.GetClrType(System.UInt32))
            game = Client._type("ClassicUO.Client").GetProperty("Game", static).GetValue(None, None)
            gumps = Tz.get(Tz.get(game, "UO"), "Gumps"); p["gumps"] = gumps
            p["hued"] = gumps.GetType().GetMethod("GetHuedGumpPixels")
            Tex.ok = all(p.get(k) is not None for k in ("table", "device", "tex_t", "set_data", "gumps", "hued"))
        except Exception: Tex.ok = False
        return Tex.ok
    @staticmethod
    def gump_pixels(gid):
        import System; args = System.Array[System.Object]([System.UInt32(gid), System.UInt16(0), False, None])
        px = Tex.parts["hued"].Invoke(Tex.parts["gumps"], args); b = args[3]
        if px is None or not len(px) or int(b.Width) <= 0 or int(b.Height) <= 0: return None
        return list(px), int(b.Width), int(b.Height)
    @staticmethod
    def put(name, w, h, pixels):
        import System; p = Tex.parts
        tex = System.Activator.CreateInstance(p["tex_t"], System.Array[System.Object](
            [p["device"], int(w), int(h), False, p["format"]]))
        p["set_data"].Invoke(tex, System.Array[System.Object]([System.Array[System.UInt32](pixels)]))
        table = p["table"]; old = table[name] if table.ContainsKey(name) else None; table[name] = tex
        Tex.names.add(name)
        if old is not None: safe(old.Dispose)
    @staticmethod
    def drop(names=None):
        if not Tex.ok: return
        table = Tex.parts["table"]
        for name in list(Tex.names if names is None else names):
            Tex.names.discard(name)
            try:
                if table.ContainsKey(name): tex = table[name]; table.Remove(name); tex.Dispose()
            except Exception: pass
    @staticmethod
    def control(g, name, x, y, w, h):
        t = G.LegionTextureControl(name, int(w), int(h)); t.SetRect(int(x), int(y), int(w), int(h))
        safe(lambda: t.SetAcceptMouseInput(False)); g.Add(t); return t


class Layout(object):
    def __init__(self):
        self.wins = {}; self.assign = {}; self.frames = None; self.frames_name = LAYOUT_DEFAULT; self.layout_name = ""
        self.game_grows = True; self.fit_view = True; self.screen = None; self.dirty = True
        self.occ = None; self.gump_key = {}
        self.placed = {}; self.squeezed_told = set(); self.editor = None; self.loaded = False; self.page_refresh = False
        self.hooks = {}; self.owner = {}; self.fitted = {}; self.base = {}; self.fresh = False; self.fresh_adds = set()
        self.client_seen = {}; self.journal_held = None; self.pair_tried = None; self.client_settle = {}
        self.misfit = {}; self.fallback = {}; self.client_told = set(); self.chat_seen = (0.0, None); self.held = {}
        self.arrange = False; self.arrange_last = 0.0; self.arrange_g = None; self.arrange_lit = {}
        self.arrange_hot = None; self.client_target = {}; self.repair_at = 0.0; self.repair_told = set()
        self.freed = None; self.page_preview = ""; self.homes = None; self.back_told = False; self._arrange_sig = None
    def _client_getter(self, kind, key):
        def get():
            cw = ClientWin.of(kind)
            if cw is not self.client_seen.get(kind):
                self.client_seen[kind] = cw; self.fitted.pop(key, None); self.placed.pop(key, None)
            if cw is None and kind not in self.client_told and ClientWin.errors.get(kind) \
                    and self.zone_of(key) is not None:
                self.client_told.add(kind)
                Kit.say("%s can't be found for its zone: %s." % (
                    ClientWin.TITLES.get(kind, kind), ClientWin.errors[kind]), Kit.HUE_BAD)
            return cw
        return get
    def _client_fit(self, kind):
        def fit(w, h, mode):
            cw = ClientWin.of(kind)
            if cw is None: return
            if w is None or h is None: cw.free()
            else: cw.fit(int(w), int(h), lock=not self.arrange); cw.report()
        return fit
    def _client_drops(self):
        if not self.arrange: self.client_settle.clear(); return
        for key in ClientWin.DROPS:
            if key not in self.wins: self.client_settle.pop(key, None); continue
            cw = ClientWin.of(key)
            if cw is None: self.client_settle.pop(key, None); continue
            try: r = cw.rect()
            except Exception: continue
            if self.zone_of(key) is not None:
                self.client_settle.pop(key, None); at = self.client_target.get(key)
                if at is not None and max(abs(r[0] - at[0]), abs(r[1] - at[1])) > SNAP_DIST \
                        and SNAP.pressed() is not True:
                    self.client_target.pop(key, None); self.dropped(cw)
                continue
            st = self.client_settle.get(key)
            if st is None or st[0] is not cw: self.client_settle[key] = (cw, r, r); continue
            settled, last = st[1], st[2]
            if r != last: self.client_settle[key] = (cw, settled, r); continue
            if r == settled or SNAP.pressed() is True: continue
            self.client_settle[key] = (cw, r, r)
            if (r[2], r[3]) != (settled[2], settled[3]): continue
            self.dropped(cw)
    CHAT_ROOM = 18
    def _chat_line(self):
        now = time.time(); at, rect = self.chat_seen
        if now - at < 0.5: return rect
        rect = None
        try:
            Typing._find(); sc = Typing._get(None, "SystemChat", Typing.uim) if Typing.uim is not None else None
            if sc is not None and not bool(Typing._get(sc, "IsDisposed", default=True)):
                b = ClientWin.bounds(sc); sx = int(Typing._get(sc, "ParentX", default=0) or 0) + int(b.X)
                sy = int(Typing._get(sc, "ParentY", default=0) or 0) + int(b.Y)
                top = sy + int(b.Height) - Layout.CHAT_ROOM; tb = Typing._get(sc, "TextBoxControl")
                if tb is not None:
                    tby = int(ClientWin.bounds(tb).Y)
                    if 0 <= tby < int(b.Height): top = min(top, sy + tby)
                if int(b.Width) > 0 and int(b.Height) > 0: rect = (sx, top, int(b.Width))
        except Exception: rect = None
        self.chat_seen = (now, rect); return rect
    def _clear_of_chat(self, x, y, w, h, H):
        line = self._chat_line()
        if line is None: cut = Layout.CHAT_ROOM if H and y + h >= H - 2 else 0; bottom = y + h - cut
        else:
            lx, top, lw = line
            if x >= lx + lw or lx >= x + w or not (y < top < y + h): return h
            bottom = top
        return max(min(h, 60), bottom - y)
    def _hold_journal(self, zs, H=0):
        z = (next((zz for zz in zs.zones if zz.kind == "r" and zz.px is not None), None)
             if self.layout_name or self.assign else None)
        cw = ClientWin.of("journal") if z is not None else None; held = self.journal_held
        if held is not None and held is not cw: held.free(); self.journal_held = None
        if cw is None: return
        x, y, w, h = z.px; h = self._clear_of_chat(x, y, w, h, H); cw.fit(w, h)
        try:
            if (cw.GetX(), cw.GetY()) != (x, y): cw.SetPos(x, y)
        except Exception: pass
        cw.report(); self.journal_held = cw
    def load(self):
        self.freed = None; self.homes = None; self.repair_told = set(); self.back_told = False; self.loaded = True
        if "worldmap" not in self.wins:
            self.add("worldmap", self._client_getter("worldmap", "worldmap"), "TazUO's World Map",
                     {"fit": self._client_fit("worldmap"), "exact": True, "client": True,
                      "inset": ClientWin.INSET.get("worldmap", 0)})
        self.frames_name = Kit.get_var(FRAMES_ACTIVE, LAYOUT_DEFAULT) or LAYOUT_DEFAULT
        if self.frames_name != LAYOUT_DEFAULT and self.frames_name not in self.frame_names():
            self.frames_name = LAYOUT_DEFAULT
        self.layout_name = Kit.get_var(LAYOUT_ACTIVE, ""); opts = Kit.get_var(LAYOUT_OPTS, "game=1")
        self.game_grows = "game=0" not in opts; self.fit_view = "fit=0" not in opts; raw = Kit.get_var(LAYOUT_VAR, "")
        self.assign = self.parse_windows(raw)[1]
        if raw and raw != self.windows_text() and any(k.strip() in LAYOUT_GONE for part in str(raw).split(";")
                if "=" in part and part.split("=", 1)[0].strip() != "frames" for k in part.split("=", 1)[1].split(",")):
            self.save_assign()
        self.frames = None; self.dirty = True
    def save_assign(self): Kit.put_var(LAYOUT_VAR, self.windows_text()); self._note_homes()
    RECLAIM_VAR = "VirtueAssistant_reclaim_undo"; RECLAIM_FIXED = "VirtueAssistant_reclaim_fixed"
    def _undo_load(self):
        if getattr(self, "reclaim_undo", None) is None and not getattr(self, "_undo_read", False):
            self._undo_read = True; p = str(Kit.get_var(self.RECLAIM_VAR, "") or "").split("|", 2)
            if len(p) == 3 and p[0]: self.reclaim_undo = (p[0], p[2], None, p[1] == "1")
        return getattr(self, "reclaim_undo", None)
    def _undo_set(self, undo):
        self.reclaim_undo = undo; self._undo_read = True
        Kit.put_var(self.RECLAIM_VAR, "" if undo is None else "%s|%d|%s" % (undo[0], 1 if undo[3] else 0, undo[1]))
    @staticmethod
    def _reclaim_edges(z, blockers, W, H):
        r = list(z.px)
        for side in "LTRB":
            i = 0 if side in "LR" else 1; j = 1 - i
            ps = [o.px for o in blockers if o is not z and o.px is not None
                  and o.px[j] < r[j] + r[j + 2] and r[j] < o.px[j] + o.px[j + 2]]
            if side in "LT":
                lim = max([0] + [p[i] + p[i + 2] for p in ps if p[i] + p[i + 2] <= r[i]])
                if lim < r[i]: r[i], r[i + 2] = lim, r[i + 2] + (r[i] - lim)
            else:
                lim = min([(W, H)[i]] + [p[i] for p in ps if p[i] >= r[i] + r[i + 2]])
                if lim > r[i] + r[i + 2]: r[i + 2] = lim - r[i]
        return tuple(r)
    def reclaim_zones(self, zs, W, H):
        fixed = [o for o in zs.zones if o.px is not None and not o.hug and (o.kind != "k" and not o.overlap)]
        others = [o for o in zs.zones if o.px is not None and o.kind != "r"]; changed = []
        for kind, blockers in (("k", fixed), ("w", others)):
            for z in zs.zones:
                if z.kind != kind or z.lock or z.px is None or (kind == "w" and (z.hug or z.overlap)): continue
                r = self._reclaim_edges(z, blockers, W, H)
                if r != tuple(z.px): z.set_px(r[0], r[1], r[2], r[3], W, H); changed.append(z.id)
        return changed
    @staticmethod
    def _game_px(zs):
        best = None
        for z in zs.zones:
            if z.kind == "k" and z.px is not None and z.px[2] > 2 and z.px[3] > 2 and (
                    best is None or z.px[2] * z.px[3] > best[2] * best[3]): best = tuple(z.px)
        return best
    def reclaim_space(self):
        W, H = Kit.screen(); zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None
        if zs is None or not zs.zones: Kit.say("no frame layout in use.", Kit.HUE_INFO); return
        was = (self._game_px(zs) or (0, 0, 0, 0))[2:]; default = self.frames_name == LAYOUT_DEFAULT
        undo = (zs.name, zs.save_text(), was, default); moved = self.reclaim_zones(zs, W, H)
        now = (self._game_px(zs) or (0, 0, 0, 0))[2:]
        if not moved or now[0] * now[1] < was[0] * was[1]:
            self.frames, self.dirty = None, True
            Kit.say("Reclaim space: every zone is already tight.", Kit.HUE_INFO); return
        self._undo_set(undo); target = zs.name if not default else "Reclaimed"; zs.generated = False
        self.save_frames(zs, target, W, H); self.use_frames(target, False); self.refit_all()
        Kit.say("Reclaim space: %d zone%s tightened; game area %d x %d (was %d x %d). Undo puts it back." % (
            len(moved), "" if len(moved) == 1 else "s", now[0], now[1], was[0], was[1]), Kit.HUE_GOOD)
    def reclaim_back(self):
        undo = self._undo_load()
        if undo is None: return
        self._undo_set(None); W, H = Kit.screen()
        if undo[3]: self.use_frames(LAYOUT_DEFAULT, False)
        else:
            zs = ZoneSet.parse(undo[0], undo[1])
            if zs is None: return
            zs.reflow(W, H, HOST.grid_size()); self.save_frames(zs, undo[0], W, H); self.use_frames(undo[0], False)
        self.refit_all(); Kit.say("Reclaim space undone.", Kit.HUE_INFO)
    def _repair_stretched(self, zs, W, H):
        if Kit.get_var(self.RECLAIM_FIXED, "") == "1": return
        Kit.put_var(self.RECLAIM_FIXED, "1")
        tall = [z for z in zs.zones if z.hug and z.px is not None and z.rect[3] >= 450]
        if not tall: return
        self._undo_set((zs.name, zs.save_text(), None, False)); top = int(_clampv(STRIP_SHARE * H, TOP_MIN, TOP_MAX))
        for z in tall: z.set_px(z.px[0], z.px[1], z.px[2], top, W, H)
        self.save_frames(zs, zs.name, W, H)
        Kit.say("%d frame zone%s Reclaim space stretched in layout \"%s\" put right; Settings > Layout's "
                   "Undo puts it back." % (len(tall), "" if len(tall) == 1 else "s", zs.name), Kit.HUE_GOOD)
    def refit_all(self): self.dirty = self.fresh = self.page_refresh = True
    def save_opts(self): Kit.put_var(LAYOUT_OPTS, "game=%d;fit=%d;art=plain" % (self.game_grows, self.fit_view))
    @staticmethod
    def parse_windows(text):
        frames, out = LAYOUT_DEFAULT, {}
        for part in str(text or "").split(";"):
            if "=" not in part: continue
            k, v = part.split("=", 1); k = k.strip()
            if k == "frames": frames = v.strip() or LAYOUT_DEFAULT; continue
            keys = [s.strip() for s in v.split(",") if s.strip() and s.strip() not in LAYOUT_GONE]
            if k and keys: out[k] = keys
        return frames, out
    def windows_text(self, frames=None):
        return ";".join(["frames=%s" % (frames or self.frames_name)] + [
            "%s=%s" % (zid, ",".join(self.assign[zid])) for zid in sorted(self.assign) if self.assign[zid]])
    @staticmethod
    def _names(var): return [n for n in Kit.get_var(var, "").split(",") if n.strip()]
    def frame_names(self): return self._names(FRAMES_LIST)
    def layout_names(self): return self._names(LAYOUT_LIST)
    @staticmethod
    def clean_name(name, fallback):
        name = re.sub(r"[^A-Za-z0-9 ()'_-]", "", str(name or "")).strip()[:24]; return name or fallback
    def add(self, key, getter, title=None, hooks=None, owner=None):
        key = str(key)
        if key in LAYOUT_GONE: return
        self.wins[key] = (getter, str(title or key)); self.hooks[key] = hooks if hasattr(hooks, "get") else {}
        if owner is not None: self.owner[key] = owner
        self.fitted.pop(key, None); self.dirty = True
    def remove(self, key):
        key = str(key)
        for d in (self.wins, self.placed, self.hooks, self.owner, self.fitted, self.base): d.pop(key, None)
        self.dirty = True
    def owner_of(self, key):
        o = self.owner.get(key)
        if o is not None: return o
        k = str(key)
        while k:
            s, part = HOST.resolve(k)
            if s is not None: return s.key, part
            if "." not in k: break
            k = k.rsplit(".", 1)[0]
        return None, None
    def windows_of(self, module_key):
        return sorted([(key, self.title_of(key)) for key in self.wins if self.owner_of(key)[0] == module_key],
                      key=lambda kt: kt[1].lower())
    def all_windows(self):
        out = []
        for key in self.wins:
            mk = self.owner_of(key)[0]; s = dict.get(HOST.by_key, mk) if mk else None; t = self.title_of(key)
            if s is not None and s.title != t: t = "%s: %s" % (s.title, t)
            out.append((key, t))
        out.sort(key=lambda kt: kt[1].lower()); return out
    def zone_choices(self):
        W, H = Kit.screen(); zs = self.frames_in_use(W, H) if W > 0 and H > 0 else self.frames; out = [None]
        if zs is not None: out.extend(z.id for z in zs.zones if z.kind == "w")
        return out
    def assign_to(self, key, zid, tell=True):
        key = str(key); old = self.zone_of(key)
        if old == zid: return
        if tell and zid and ((key != "worldmap" and zid == self._map_zone())
                             or (key == "worldmap" and self.assign.get(zid))):
            Kit.say("TazUO's World Map keeps its zone to itself; pick another zone for %s."
                       % (self.title_of(key) if key != "worldmap" else "it"), Kit.HUE_BAD)
            self.page_refresh = True; return
        if old is not None:
            self.assign[old] = [k for k in self.assign[old] if k != key]
            if not self.assign[old]: del self.assign[old]
        if zid: self.assign.setdefault(zid, []).append(key); self.unfree(key)
        elif tell: self.free_by_you([key])
        self.save_assign()
        if not zid: self.free_scrolled()
        self.placed.pop(key, None); self.dirty = True; self.squeezed_told.discard(key); self.page_refresh = True
        if tell:
            API.SysMsg(('%s: %s is in zone "%s".' % (APP_NAME, self.title_of(key), zid)) if zid else
                       ("%s: %s is free (it stays where you put it)." % (APP_NAME, self.title_of(key))), Kit.HUE_GOOD)
        HOST.poke()
    def zone_of(self, key):
        for zid, keys in self.assign.items():
            if key in keys: return zid
        return None
    def need(self, key, w, h):
        zid = self.zone_of(str(key)); zs = self.frames
        if zid is None or zs is None: return
        want = (w, h) if (w or h) else None
        if zs.needs.get(zid) != want:
            if want is None: zs.needs.pop(zid, None)
            else: zs.needs[zid] = want
            self.need_due = True
    def zone_base(self, key):
        zid = self.zone_of(str(key)); zs = self.frames
        z = zs.by_id(zid) if (zid is not None and zs is not None) else None
        if z is None: return None
        W, H = zs.screen
        if W <= 0 or H <= 0: W, H = Kit.screen()
        return (max(1, int(W * z.rect[2] / 1000.0)), max(1, int(H * z.rect[3] / 1000.0)))
    def holds(self, key):
        zid = self.zone_of(str(key))
        if zid is None: return False
        zs = self.frames; return zs is None or zs.by_id(zid) is not None
    def locked(self, key): return not self.arrange and self.holds(key)
    def _hold(self, g, key):
        if isinstance(g, ClientWin): return
        if g not in self.held:
            self.held[g] = (key, bool(g.CanMove))
            for f, l in list(SNAP.links.items()):
                if f is g or l is g: SNAP.links.pop(f, None)
        if bool(g.CanMove) != bool(self.arrange): g.CanMove = bool(self.arrange)
    def _release(self, keep):
        for g in [g for g in self.held if g not in keep]:
            key, own = self.held.pop(g)
            if g in SNAP.drag or not Kit.is_open(g): continue
            if not own and not self.holds(key):
                rd = (self.hooks.get(key) or {}).get("redraw")
                if callable(rd): safe(rd); continue
                own = True
            if bool(g.CanMove) != own: g.CanMove = own
    def set_arrange(self, on, tell=True):
        on = bool(on)
        if on == self.arrange: return
        self.arrange = on; self.arrange_last = time.time(); self.arrange_hot = None
        if not on: old, self.arrange_g = self.arrange_g, None; self.arrange_lit = {}; Kit.dispose(old)
        self.dirty = True; self.page_refresh = True
        if tell:
            API.SysMsg(("%s: Arrange mode on; drag windows on to zones, then click Done." if on else
                        "%s: windows locked in their zones.") % APP_NAME, Kit.HUE_GOOD)
        HOST.poke()
    def _arrange_tick(self, zs, W, H):
        if not self.arrange: return
        now = time.time()
        if SNAP.drag: self.arrange_last = now
        elif now - self.arrange_last > 60.0: self.set_arrange(False); return
        sig = (W, H, tuple((z.id, z.kind, tuple(z.px)) for z in zs.zones if z.px is not None))
        if self.arrange_g is not None and Kit.is_open(self.arrange_g) and self._arrange_sig == sig: return
        self._arrange_sig = sig; old, self.arrange_g = self.arrange_g, None; self.arrange_lit = {}; Kit.dispose(old)
        g = G.CreateGump(False, False)
        for z in zs.zones:
            if z.px is None or z.kind != "w": continue
            x, y, w, h = z.px; col = ZONE_COLORS.get(z.kind, "#3A78C8"); lit = Kit.add_box(g, x, y, w, h, 0.30, col)
            lit.IsVisible = False; self.arrange_lit[z.id] = lit
            for bx, by, bw_, bh in ((x, y, w, 2), (x, y + h - 2, w, 2), (x, y, 2, h), (x + w - 2, y, 2, h)):
                Kit.add_box(g, bx, by, bw_, bh, 0.9, col)
            name = Kit.fit(z.id, max(20, w - 28)); pw = Kit.text_w(name) + 12
            Kit.add_box(g, x + 6, y + h - 6 - 22, pw, 22, 0.85, "#000000")
            Kit.add_label(g, name, x + 12, y + h - 6 - 20, Kit.HUE_TITLE)
        Grid.show_overlay(g, 0, 0, W, H); self.arrange_g = g; self.arrange_hot = None
    def arrange_hover(self, g, r=None):
        if not self.arrange or not self.arrange_lit or self.frames is None: return
        if r is None: r = Snap.rect(g)
        z = self._drop_zone(r) if r is not None else None; zid = z.id if z is not None else None
        if zid == self.arrange_hot: return
        for k in (self.arrange_hot, zid):
            box = self.arrange_lit.get(k) if k is not None else None
            if box is not None: box.IsVisible = k == zid
        self.arrange_hot = zid
    def _min_of(self, key, g=None):
        hooks = self.hooks.get(key) or {}; mn = hooks.get("min")
        if callable(mn): mn = safe(mn)
        if mn:
            try: return int(mn[0]), int(mn[1])
            except Exception: pass
        g = g if g is not None else self.gump_of(key)
        if isinstance(g, ClientWin):
            m = g._min_size()
            if m[0] > 0 or m[1] > 0: return m
        return None
    def _too_small(self, key, z, g=None):
        mn = self._min_of(key, g)
        if mn is None or z is None or z.px is None: return False
        if z.px[2] >= mn[0] and z.px[3] >= mn[1]: return False
        Kit.say("%s needs a zone at least %d x %d." % (self.title_of(key), mn[0], mn[1]), Kit.HUE_BAD); return True
    def title_of(self, key):
        w = self.wins.get(key)
        if w is not None: return w[1]
        s = HOST.page_slot(key); return s.title if s is not None else key
    PAIR_MIN_H = 120
    def _flush_below(self, top, z):
        if top is None or z is None or top is z or top.px is None or z.px is None: return False
        tx, ty, tw, th = top.px; zx, zy, zw, zh = z.px
        if abs(zy - (ty + th)) > SNAP_DIST: return False
        ov = min(tx + tw, zx + zw) - max(tx, zx); return ov * 2 > min(tw, zw)
    def _free_under(self, zs, top, H):
        tx, ty, tw, th = top.px; lim = H
        for o in zs.zones:
            if o is top or o.px is None: continue
            ox, oy, ow, oh = o.px
            if oy + oh > ty + th and ox < tx + tw and tx < ox + ow: lim = min(lim, max(oy, ty + th))
        return lim
    def pair_below(self, top_key, bottom_key):
        if not self.loaded: return None
        W, H = Kit.screen()
        if W <= 0 or H <= 0: return None
        zs = self.frames_in_use(W, H); top_key, bottom_key = str(top_key), str(bottom_key)
        tzid, bzid = self.zone_of(top_key), self.zone_of(bottom_key); tz = zs.by_id(tzid) if tzid else None
        bz = zs.by_id(bzid) if bzid else None
        if tz is None or tz.kind != "w" or tz.px is None:
            if bzid is not None: self.assign_to(bottom_key, None, tell=False)
            return None
        if bz is not None and self._flush_below(tz, bz): return tz.px, bz.px
        moved = bz is not None; best = None
        for z in zs.zones:
            if z.kind == "w" and self._flush_below(tz, z):
                tx, ty, tw, th = tz.px; ov = min(tx + tw, z.px[0] + z.px[2]) - max(tx, z.px[0])
                if best is None or ov > best[0]: best = (ov, z)
        if best is not None:
            self.assign_to(bottom_key, best[1].id, tell=False)
            if moved:
                Kit.say('%s rides in the %s window, so it takes the zone under it ("%s").'
                           % (self.title_of(bottom_key), self.title_of(top_key), best[1].id), Kit.HUE_INFO)
            return tz.px, best[1].px
        mark = (zs.name, tz.id, tuple(tz.px))
        if self.pair_tried == mark: return tz.px, None
        self.pair_tried = mark; name = zs.name
        if zs.generated or name == LAYOUT_DEFAULT:
            zs = ZoneSet.default(W, H, (), False)
            zs.name, zs.generated = LAYOUT_MINE, False; name = LAYOUT_MINE; tz = zs.by_id(tz.id)
            if tz is None or tz.px is None: return None
        else: zs = zs.copy(); tz = zs.by_id(tz.id)
        tx, ty, tw, th = tz.px; room = self._free_under(zs, tz, H) - (ty + th); split = False
        if room >= max(ZONE_MIN_H, self.PAIR_MIN_H): nx, ny, nw, nh = tx, ty + th, tw, room
        elif th >= 2 * ZONE_MIN_H:
            split = True; ht = max(ZONE_MIN_H, min(th - ZONE_MIN_H, int(round(th * 0.46))))
            nx, ny, nw, nh = tx, ty + ht, tw, th - ht
        else: return tz.px, None
        nid = "%s bags" % tz.id
        if zs.by_id(nid) is not None: nid = zs.new_id()
        nz = Zone(nid, "w", (0, 0, 1, 1), "", (tz.min[0], self.PAIR_MIN_H), "d", tz.prio, tz.fit)
        if split: tz.set_px(tx, ty, tw, ht, W, H)
        nz.set_px(nx, ny, nw, nh, W, H); nz.note_pins(W, H); tz.note_pins(W, H); zs.zones.append(nz)
        self.save_frames(zs, name, W, H)
        if self.frames_name != name: self.use_frames(name, tell=False)
        else: self.frames, self.dirty = None, True
        self.assign_to(bottom_key, nid, tell=False)
        Kit.say('zone "%s" made under "%s" for the bags%s; frame layout "%s" saved.' % (
            nid, tz.id, " (split in two)" if split else "", name), Kit.HUE_GOOD)
        zs2 = self.frames_in_use(W, H); t2, b2 = zs2.by_id(tz.id), zs2.by_id(nid)
        if t2 is None or b2 is None or t2.px is None or b2.px is None: return tz.px, nz.px
        return t2.px, b2.px
    def gump_of(self, key):
        w = self.wins.get(key)
        if w is None: return None
        try: g = w[0]()
        except Exception: return None
        return g if Kit.is_open(g) else None
    def occupied(self):
        return set(zid for zid, keys in self.assign.items() if any(self.gump_of(key) is not None for key in keys))
    def frames_in_use(self, W, H):
        if self.frames is not None and not self.dirty and self.screen == (W, H): return self.frames
        zs = self.load_frames(self.frames_name, W, H) if self.frames_name != LAYOUT_DEFAULT else None
        if zs is not None: self._repair_stretched(zs, W, H)
        elif self.frames_name != LAYOUT_DEFAULT:
            self.frames_name = LAYOUT_DEFAULT; Kit.put_var(FRAMES_ACTIVE, LAYOUT_DEFAULT)
        if zs is None: zs = ZoneSet.default(W, H, self.occupied(), self.game_grows)
        self._overlap_shape(zs); self.frames, self.screen, self.dirty = zs, (W, H), False; return zs
    @staticmethod
    def _overlap_shape(zs):
        for k in zs.zones:
            if k.kind == "k" and k.overlap and k.px is not None: k.arch = False; k.px = ZoneSet.cut_clear(k, zs.zones)
    GV_VAR = "Layout_gameview_own"; GV_LOCK_VAR = "Layout_gameview_lock"; GV_MIN = (640, 480)
    def _viewport(self): t = Tz.T("ClassicUO.Game.UI.Gumps.WorldViewportGump"); return t, Tz.get(None, "Instance", t)
    def _vp_border(self): return 0 if self._vp_full() else 5
    def _vp_set(self, x, y, w, h):
        t, vp = self._viewport(); b = self._vp_border(); Tz.call(vp, "ResizeGameWindow", (ClientWin.point(w, h),), t)
        Tz.call(vp, "SetGameWindowPosition", (ClientWin.point(x - b, y - b),), t)
    def _vp_get(self):
        r = ClientWin.bounds(self._viewport()[1]); b = self._vp_border()
        return int(r.X) + b, int(r.Y) + b, int(r.Width) - 2 * b, int(r.Height) - 2 * b
    @staticmethod
    def _profile():
        Typing._find(); return Typing._get(None, "CurrentProfile", Typing.prof) if Typing.prof is not None else None
    def _vp_full(self):
        cur = self._profile()
        return bool(Typing._get(cur, "GameWindowFullSize", default=False)) if cur is not None else False
    def _vp_chrome(self, on):
        t, vp = self._viewport(); fs = getattr(self, "_vp_fields", None)
        if fs is None:
            fs = self._vp_fields = [t.GetField(n, Client.flags(public=False)) for n in ("_borderControl", "_button")]
        for f in fs:
            ctl = f.GetValue(vp) if f is not None else None
            if ctl is not None and bool(ctl.IsVisible) != bool(on): ctl.IsVisible = bool(on)
    def _vp_lock(self, locked):
        cur = self._profile()
        if cur is not None: Tz.put(cur, "GameWindowLock", bool(locked))
        t, vp = self._viewport(); vp.CanMove = not locked
    def _game_view(self, zs):
        want = self._game_px(zs) if self.fit_view and self.assign and not self._vp_full() else None
        if want is not None and (want[2] < self.GV_MIN[0] or want[3] < self.GV_MIN[1]):
            if not getattr(self, "gv_small_told", False):
                self.gv_small_told = True
                Kit.say("the game view would be %d x %d, under the client's smallest (%d x %d); left as you "
                           "set it." % (want[2], want[3], self.GV_MIN[0], self.GV_MIN[1]), Kit.HUE_INFO)
            want = None
        if not getattr(self, "gv_checked", False):
            self.gv_checked = True
            if want is None and Kit.get_var(self.GV_VAR, ""): self.game_view_restore(); return
        if want == getattr(self, "gv_applied", None):
            if want is not None: self._vp_chrome(False)
            return
        if want is None: self.game_view_restore(); return
        if not Kit.get_var(self.GV_VAR, ""):
            Kit.put_var(self.GV_VAR, "%d,%d,%d,%d" % self._vp_get()); cur = self._profile()
            lk = bool(Typing._get(cur, "GameWindowLock", default=False)) if cur is not None else False
            Kit.put_var(self.GV_LOCK_VAR, "1" if lk else "0")
        self._vp_set(*want); self._vp_chrome(False); self._vp_lock(True); self.gv_applied = want
    def game_view_restore(self):
        self.gv_applied = None; raw = Kit.get_var(self.GV_VAR, "")
        if not raw: return
        try:
            x, y, w, h = [int(v) for v in raw.split(",")]; self._vp_set(x, y, w, h)
            if not self._vp_full(): self._vp_chrome(True)
            lk = Kit.get_var(self.GV_LOCK_VAR, "")
            if lk: self._vp_lock(lk == "1")
        except Exception: return
        Kit.put_var(self.GV_VAR, ""); Kit.put_var(self.GV_LOCK_VAR, "")
    def load_frames(self, name, W, H):
        cls = ratio_class(W, H); var = FRAMES_NAMED % name; zs = ZoneSet.parse(name, Kit.get_var(var + "@" + cls, ""))
        fresh = False
        if zs is None: zs = ZoneSet.parse(name, Kit.get_var(var, "")); fresh = True
        if zs is None: return None
        for zid in zs.skipped:
            HOST._tell('%s: zone "%s" in frame layout "%s" couldn\'t be read; skipped.' % (APP_NAME, zid, name))
        zs.reflow(W, H, HOST.grid_size())
        if fresh and zs.zones: Kit.put_var(var + "@" + cls, zs.save_text())
        return zs
    def save_frames(self, zs, name, W, H):
        zs.name = name; zs.screen = (W, H); zs.grid = HOST.grid_size()
        for z in zs.zones: z.note_pins(W, H)
        text = zs.save_text(); Kit.put_var(FRAMES_NAMED % name, text); cls = ratio_class(W, H)
        for k in ("narrow", "wide", "ultrawide"): Kit.put_var((FRAMES_NAMED % name) + "@" + k, text if k == cls else "")
        names = self.frame_names()
        if name not in names: names.append(name); Kit.put_var(FRAMES_LIST, ",".join(names))
        self.page_refresh = True
    def use_frames(self, name, tell=True):
        if name != LAYOUT_DEFAULT and name not in self.frame_names(): name = LAYOUT_DEFAULT
        self.frames_name = name; Kit.put_var(FRAMES_ACTIVE, name); self.frames, self.dirty = None, True
        W, H = Kit.screen(); zs = self.frames_in_use(W, H) if W > 0 else None
        if tell:
            free = 0
            if zs is not None:
                ids = set(zs.ids()); free = sum(len(k) for zid, k in self.assign.items() if zid not in ids)
            Kit.say('frame layout "%s" in use%s.' % (name, ("; %s had no zone and are free" % Kit.count(free, "window"))
                if free else ""), Kit.HUE_GOOD)
        self.page_refresh = True
    def remove_frames(self, name):
        if name == LAYOUT_DEFAULT: return False
        names = [n for n in self.frame_names() if n != name]; Kit.put_var(FRAMES_LIST, ",".join(names))
        for cls in ("", "@narrow", "@wide", "@ultrawide"): Kit.put_var((FRAMES_NAMED % name) + cls, "")
        if self.frames_name == name: self.use_frames(LAYOUT_DEFAULT, tell=False)
        Kit.say('frame layout "%s" deleted.' % name, Kit.HUE_GOOD); self.page_refresh = True
        return True
    def window_layout_text(self, name):
        if name == LAYOUT_DEFAULT: return "frames=%s;%s" % (LAYOUT_DEFAULT, WINDOWS_DEFAULT)
        if name == LAYOUT_MIRRORED: return "frames=%s;%s" % (LAYOUT_DEFAULT, WINDOWS_MIRRORED)
        return Kit.get_var(LAYOUT_NAMED % name, "")
    def use_windows(self, name, tell=True):
        if (name and name not in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) and name not in self.layout_names()): name = ""
        frames, assign = (self.parse_windows(self.window_layout_text(name)) if name else (self.frames_name, {}))
        if name: self.unfree(None)
        else: self.free_by_you(list(self.wins) + [k for ks in self.assign.values() for k in ks])
        self.layout_name = name; Kit.put_var(LAYOUT_ACTIVE, name); self.assign = assign; self.save_assign()
        self.free_scrolled(); self.placed = {}; self.squeezed_told = set()
        if name and name not in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) and frames != self.frames_name:
            self.use_frames(frames, tell=False)
        else: self.dirty = True
        if tell:
            API.SysMsg(('%s: window layout "%s" in use.' % (APP_NAME, name)) if name else
                       ("%s: every window is free; drop one on a zone to slot it." % APP_NAME), Kit.HUE_GOOD)
        self.page_refresh = True
    def save_windows(self, name=None):
        name = name or self.layout_name or LAYOUT_MINE
        if name in (LAYOUT_DEFAULT, LAYOUT_MIRRORED): name = name + " (mine)"
        name = self.clean_name(name, LAYOUT_MINE); Kit.put_var(LAYOUT_NAMED % name, self.windows_text())
        names = self.layout_names()
        if name not in names: names.append(name); Kit.put_var(LAYOUT_LIST, ",".join(names))
        self.layout_name = name; Kit.put_var(LAYOUT_ACTIVE, name)
        Kit.say('window layout "%s" saved.' % name, Kit.HUE_GOOD); self.page_refresh = True
    def free_scrolled(self):
        for key in [k for k in self.fitted if self.zone_of(k) is None]: self._unfit(key)
        for key, rect in list(self.placed.items()):
            if self.zone_of(key) is None:
                g = self.gump_of(key); info = Kit.scroll_info(g) if g is not None else None
                if info is not None:
                    try:
                        Kit.place(g, int(g.GetX()), int(g.GetY()), info["w"], info["h"], info["head"])
                        Kit.moved_by_code(g)
                    except Exception: pass
                self.placed.pop(key, None)
    def keep(self, W, H):
        if not self.loaded or W <= 0 or H <= 0: return
        occ = self.occupied()
        if occ != self.occ:
            self.occ = occ
            if self.frames_name == LAYOUT_DEFAULT: self.dirty = True
        zs = self.frames_in_use(W, H)
        if self.editor is not None: self.editor.keep(W, H)
        self.fresh = False; self.fresh_adds.clear(); Fill.prune()
        for key in [k for k in self.fitted if self.zone_of(k) is None]: self._unfit(key)
        now = time.time()
        jobs = [(self._hold_journal, (zs, H)), (self._client_drops, ()), (self._arrange_tick, (zs, W, H))]
        if now >= self.repair_at and not SNAP.drag: self.repair_at = now + 2.0; jobs.append((self._repair, (zs,)))
        for fn, args in jobs:
            try: fn(*args)
            except Exception: pass
        drag = SNAP.drag; told = []; seen = set(); self.gump_key = {}
        for z in (zs.zones if self.assign else ()):
            keys = self.assign.get(z.id)
            if not keys or z.kind != "w" or z.px is None: continue
            items = []
            for key in keys:
                g = self.gump_of(key)
                if g is None: continue
                self.gump_key[g] = key
                if g in seen or g in SNAP.attached or not Snap.visible(g): continue
                riding = (self.hooks.get(key) or {}).get("riding")
                if riding is not None:
                    try:
                        if riding(): continue
                    except Exception: pass
                seen.add(g); self._hold(g, key)
                if z.squeezed and key not in self.squeezed_told: self.squeezed_told.add(key); self._minimize(key)
                r = Snap.rect(g)
                if r is None:
                    if isinstance(g, ClientWin):
                        try: g.rect(); why = "it has no size"
                        except Exception as ex: why = Tz.why(ex)
                        g.fail["size"] = "its place and size couldn't be read (%s)" % why; g.report()
                    continue
                hooks = self.hooks.get(key) or {}; fol = [f for f in SNAP.followers(g) if Snap.visible(f)]; ext = r
                for f in fol:
                    rf = Snap.rect(f)
                    if rf is not None:
                        x0, y0 = min(ext[0], rf[0]), min(ext[1], rf[1]); x1 = max(ext[0] + ext[2], rf[0] + rf[2])
                        y1 = max(ext[1] + ext[3], rf[1] + rf[3]); ext = (x0, y0, x1 - x0, y1 - y0)
                mini = False; state = hooks.get("state")
                if state is not None:
                    try: mini = state() == "minimized"
                    except Exception: pass
                items.append((key, g, r, ext, fol, hooks, mini, self._base(key, g, ext, mini)))
            if not items: continue
            for it, slot in zip(items, self._slots(z, items)):
                if it[1] in drag: continue
                try:
                    if self._fit_slot(it, slot, z): told.append(it[1])
                except Exception: self.placed[it[0]] = slot
        self._release(seen)
        try: self._game_view(zs)
        except Exception: pass
        if self.assign and getattr(self, "need_due", False): self.need_due = False; zs.reflow(W, H, HOST.grid_size())
        if told:
            Kit.flush()
            for g in told:
                fn = SNAP.moved_cb.get(g)
                if fn is not None:
                    try: fn()
                    except Exception: pass
    def _base(self, key, g, ext, mini):
        if mini: return ext[2], ext[3]
        b = self.base.get(key)
        if b is None:
            rec = Fill.recs.get(g); b = rec["nat"] if rec is not None else (ext[2], ext[3]); self.base[key] = b
        return b
    def _slots(self, z, items):
        zx, zy, zw, zh = z.px; down = z.stack in ("d", "u"); along = zh if down else zw; n = len(items)
        all_mini = all(it[6] for it in items); fixed = []; weights = []
        for it in items:
            size = it[7][1] if down else it[7][0]
            if it[6] and not all_mini: fixed.append(max(1, min(int(size), along))); weights.append(0)
            else: fixed.append(None); weights.append(max(1, int(size)))
        free = along - sum(f for f in fixed if f is not None); total = sum(weights)
        if free < n or total <= 0:
            fixed = [None] * n; weights = [max(1, int(it[7][1] if down else it[7][0])) for it in items]
            free, total = along, sum(weights)
        lens = []; left, left_w = free, total
        for f, wt in zip(fixed, weights):
            if f is not None: lens.append(f)
            else:
                share = int(round(left * float(wt) / left_w)) if left_w > 0 else left; lens.append(max(1, share))
                left -= share; left_w -= wt
        out = []; pos = (zy if z.stack == "d" else zy + zh if z.stack == "u" else zx if z.stack == "r" else zx + zw)
        back = z.stack in ("u", "l")
        for ln in lens:
            if back: pos -= ln
            out.append((zx, pos, zw, ln) if down else (pos, zy, ln, zh))
            if not back: pos += ln
        return out
    def _fit_slot(self, it, slot, z=None):
        key, g, r, ext, fol, hooks, mini, base = it; ins = int(hooks.get("inset") or 0)
        slot = (slot[0] - ins, slot[1] - ins, slot[2] + 2 * ins, slot[3] + 2 * ins); self.placed[key] = slot
        sx, sy, sw, sh = slot; fit_fn = hooks.get("fit"); rec = self.fitted.get(key)
        if fit_fn is not None:
            tw, th = sw, sh
            if fol and not hooks.get("pieces_out"): tw, th = sw - (ext[2] - r[2]), sh - (ext[3] - r[3])
            told = rec.get("told") if rec is not None else None
            if told is None or abs(told[0] - tw) > 4 or abs(told[1] - th) > 4 \
                    or (told != (tw, th) and (tw, th) == (sw, sh)) or hooks.get("client"):
                self.fitted[key] = rec = {"kind": "fit", "told": (tw, th)}
                try: fit_fn(tw, th, "w")
                except Exception: pass
        elif rec is None: self.fitted[key] = {"kind": "fill"}
        if hooks.get("exact"):
            gx, gy = sx + (r[0] - ext[0]), sy + (r[1] - ext[1])
            if hooks.get("pieces_out"): gx, gy = sx, sy
            if isinstance(g, ClientWin):
                gx, gy = self._client_overflow(key, g, z, gx, gy, sw, sh, ins); self.client_target[key] = (gx, gy)
            if fit_fn is not None and hooks.get("verify"):
                self._verify(key, g, r, rec, fit_fn, mini); fb = self.fallback.get(key)
                if fb is not None and not mini and not fol:
                    if fb != (sw, sh): self.fallback.pop(key, None)
                    else:
                        done = Fill.fit(g, sx, sy, sw, sh, hooks.get("fill") or "anchor")
                        if done is not None:
                            if done: Kit.moved_by_code(g)
                            return bool(done)
            return self._move_all(g, fol, r, gx, gy)
        if fol:
            if hooks.get("pieces_out"): lx, ly, lw, lh = sx, sy, sw, sh
            else:
                lx, ly = sx + (r[0] - ext[0]), sy + (r[1] - ext[1]); lw, lh = sw - (ext[2] - r[2]), sh - (ext[3] - r[3])
            if lw < 40 or lh < 20: return self._move_all(g, fol, r, sx + (r[0] - ext[0]), sy + (r[1] - ext[1]))
            done = Fill.fit(g, lx, ly, lw, lh, hooks.get("fill") or "anchor")
            if done is None: return self._move_all(g, fol, r, lx, ly)
            nr = Snap.rect(g) or (lx, ly, lw, lh)
            for f in fol:
                rf = Snap.rect(f)
                if rf is None: continue
                fx, fy = Fill.beside(rf, r, nr)
                if (rf[0], rf[1]) != (fx, fy): Snap.move(f, fx, fy); Kit.moved_by_code(f); done = True
            if done: Kit.moved_by_code(g)
            return bool(done)
        done = Fill.fit(g, sx, sy, sw, sh, hooks.get("fill") or "anchor")
        if done is None:
            Fill.unfit(g); info = Kit.scroll_info(g)
            fw, fh = (info["w"], info["h"]) if info is not None else (r[2], r[3])
            if (r[0], r[1]) == (sx, sy) and r[3] == min(fh, sh): return False
            Kit._place_raw(g, sx, sy, fw, fh, None, sh if fh > sh else None); done = True
        if done: Kit.moved_by_code(g)
        return bool(done)
    @staticmethod
    def _move_all(g, fol, r, x, y):
        if (r[0], r[1]) == (x, y): return False
        Snap.move(g, x, y); Kit.moved_by_code(g)
        for f in fol:
            pf = Snap.pos(f)
            if pf is not None: Snap.move(f, pf[0] + x - r[0], pf[1] + y - r[1]); Kit.moved_by_code(f)
        return True
    def _client_overflow(self, key, g, z, gx, gy, sw, sh, ins):
        try: mw, mh = g._min_size()
        except Exception: return gx, gy
        rw, rh = max(sw, mw), max(sh, mh)
        if rw <= sw and rh <= sh: return gx, gy
        zs = self.frames; W, H = Kit.screen()
        if (z is not None and z.px is not None and (key, z.id, z.px) != getattr(self, "small_said", None)):
            self.small_said = (key, z.id, z.px)
            Kit.say('%s needs zone "%s" to be at least %d x %d; it is %d x %d.' % (
                self.title_of(key), z.id, max(z.px[2], mw - 2 * ins), max(z.px[3], mh - 2 * ins), z.px[2],
                z.px[3]), Kit.HUE_BAD)
        ox, oy = rw - sw, rh - sh
        def cost(x, y):
            c = 0
            for o in (zs.zones if zs is not None else []):
                if o is z or o.px is None or o.kind == "r": continue
                a = max(0, min(x + rw, o.px[0] + o.px[2]) - max(x, o.px[0])) * \
                    max(0, min(y + rh, o.px[1] + o.px[3]) - max(y, o.px[1]))
                c += a * (100 if o.kind == "w" else 10)
            on = max(0, min(x + rw, W) - max(x, 0)) * max(0, min(y + rh, H) - max(y, 0)); return c + (rw * rh - on)
        best = None
        for fx in sorted(set((0, ox // 2, ox))):
            for fy in sorted(set((0, oy // 2, oy))):
                c = cost(gx - fx, gy - fy)
                if best is None or c < best[0]: best = (c, gx - fx, gy - fy)
        return best[1], best[2]
    MISFIT_SLACK = 2
    def _verify(self, key, g, r, rec, fit_fn, it_mini=False):
        told = rec.get("told") if rec is not None else None
        if told is None or SNAP.drag: return
        if it_mini or not (abs(r[2] - told[0]) > self.MISFIT_SLACK or abs(r[3] - told[1]) > self.MISFIT_SLACK):
            self.misfit.pop(key, None); return
        n = self.misfit.get(key, 0) + 1; self.misfit[key] = n
        if n == 8 and key not in self.fallback: self.fallback[key] = (int(told[0]), int(told[1]))
        if n >= 2 and n & (n - 1) == 0:
            try: fit_fn(told[0], told[1], "again")
            except Exception: pass
    def _unfit(self, key):
        rec = self.fitted.pop(key, None)
        for d in (self.base, self.misfit, self.fallback, self.client_settle): d.pop(key, None)
        if rec is None: return
        hooks = self.hooks.get(key) or {}
        if rec.get("kind") == "fit":
            fn = hooks.get("fit")
            if fn is not None and rec.get("told") is not None:
                try: fn(None, None, None)
                except Exception: pass
        g = self.gump_of(key)
        if g is not None: Fill.unfit(g)
    def _minimize(self, key):
        fn = (dict(HOST.docks).get(key) or {}).get("minimize")
        if fn is not None: safe(fn)
    def report_fit(self):
        W, H = Kit.screen(); zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None; n = bad = 0; ridden = []
        for z in (zs.zones if zs is not None else []):
            keys = self.assign.get(z.id, [])
            rides = [safe((self.hooks.get(k) or {}).get("riding") or (lambda: False), False) for k in keys]
            if keys and all(rides) and z.px is not None: ridden.append(z.px)
        for z in (zs.zones if zs is not None else []):
            for key in self.assign.get(z.id, []):
                g = self.gump_of(key); slot = self.placed.get(key)
                if g is None or slot is None: continue
                r = Snap.rect(g)
                if r is None: continue
                n += 1; want = tuple(slot); ok = all(abs(a - b) <= self.MISFIT_SLACK for a, b in zip(r, want))
                for p in ridden:
                    x0, y0 = min(want[0], p[0]), min(want[1], p[1])
                    u = (x0, y0, max(want[0] + want[2], p[0] + p[2]) - x0, max(want[1] + want[3], p[1] + p[3]) - y0)
                    if all(abs(a - b) <= self.MISFIT_SLACK for a, b in zip(r, u)): ok = True
                if not ok: bad += 1
                Kit.say('%s in "%s": %d x %d at %d, %d%s.' % (self.title_of(key), z.id, r[2], r[3], r[0], r[1],
                    "; fills it" if ok else "; its zone is %d x %d at %d, %d" % (want[2], want[3], want[0], want[1])),
                    Kit.HUE_GOOD if ok else Kit.HUE_BAD)
                k, full = self.drawn_at(key, g)
                if k < 0.995 and full is not None:
                    Kit.say('%s is drawn at %d%% in zone "%s"; %d x %d shows it at 100%%.'
                               % (self.title_of(key), int(round(k * 100)), z.id, full[0], full[1]), Kit.HUE_INFO)
        if not n: Kit.say("no window sits in a zone.", Kit.HUE_INFO)
        else:
            Kit.say("%d of %d windows fill their zone; screen %d x %d (UI scale %.2f)." % (
                n - bad, n, W, H, Kit.render_scale()), Kit.HUE_INFO)
    def drawn_at(self, key, g):
        hooks = self.hooks.get(key) or {}; fn = hooks.get("drawn_at")
        if fn is not None:
            got = safe(fn, None)
            if got: return got
        rec = Fill.recs.get(g)
        if rec is None or rec.get("k", 1.0) >= 0.995: return 1.0, None
        nw, nh = rec["nat"]; return rec["k"], (int(nw), int(nh))
    def _map_zone(self): return self.zone_of("worldmap")
    FREED_VAR = "VirtueAssistant_layout_freed"; HOMES_VAR = "VirtueAssistant_layout_homes"
    def _freed(self):
        if self.freed is None: self.freed = set(k for k in Kit.get_var(self.FREED_VAR, "").split(",") if k.strip())
        return self.freed
    def free_by_you(self, keys):
        f = self._freed(); n = len(f); f.update(str(k) for k in keys)
        if len(f) != n: Kit.put_var(self.FREED_VAR, ",".join(sorted(f)))
    def unfree(self, key=None):
        f = self._freed()
        if not f: return
        if key is None: f.clear()
        elif key in f: f.discard(key)
        else: return
        Kit.put_var(self.FREED_VAR, ",".join(sorted(f)))
    def _homes(self):
        if self.homes is None:
            self.homes = {}; raw = Kit.get_var(self.HOMES_VAR, ""); self.migrating = not raw
            for part in raw.split(";"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    if k.strip() and v.strip(): self.homes[k.strip()] = v.strip()
        return self.homes
    def _note_homes(self):
        h = self._homes(); changed = False
        for zid, keys in self.assign.items():
            for k in keys:
                if h.get(k) != zid: h[k] = zid; changed = True
        if changed:
            if len(h) > 64:
                for k in [k for k in h if self.zone_of(k) is None][:len(h) - 64]: del h[k]
            Kit.put_var(self.HOMES_VAR, ";".join("%s=%s" % kv for kv in sorted(h.items())))
    def _repair(self, zs):
        if not self.assign: return
        homes = self._homes()
        if not homes: self._note_homes()
        mz = self._map_zone(); squat = [k for k in (self.assign.get(mz, []) if mz else []) if k != "worldmap"]
        freed = self._freed(); todo = list(squat); listed = None
        for key in ("ultima.friend", "ultima.neutral", "ultima.foe", "ultima.combat", "meters", "worldmap"):
            if (key not in self.wins or key in freed or key in squat or self.zone_of(key) is not None): continue
            if listed is None:
                listed = set()
                if self.layout_name:
                    for ks in self.parse_windows(self.window_layout_text(self.layout_name))[1].values():
                        listed.update(ks)
            mod = key.split(".")[0]; kin = any(k.split(".")[0] == mod for ks in self.assign.values() for k in ks)
            if key in homes or key in listed or (kin and key != "worldmap") \
                    or (getattr(self, "migrating", False) and key != "worldmap"):
                todo.append(key)
        changed = []
        for key in todo:
            if self.gump_of(key) is None: continue
            cur = self.zone_of(key); home = self._home_for(key, zs, mz)
            if home is None:
                if key not in self.repair_told and key != "worldmap":
                    self.repair_told.add(key)
                    Kit.say("%s has no zone to go back to; drop it on one in Arrange mode."
                               % self.title_of(key), Kit.HUE_INFO)
                if cur is None: continue
            if cur is not None:
                self.assign[cur] = [k for k in self.assign[cur] if k != key]
                if not self.assign[cur]: del self.assign[cur]
            if home is not None: self.assign.setdefault(home, []).append(key)
            self._refit(key); changed.append((key, home))
        if changed:
            self.save_assign(); self.dirty = self.fresh = True; self.page_refresh = True
            for key, home in changed:
                if home is not None: Kit.say('%s put back in zone "%s".' % (self.title_of(key), home), Kit.HUE_GOOD)
            self.free_scrolled(); HOST.poke()
    def _home_for(self, key, zs, mz):
        wz = [z for z in zs.zones if z.kind == "w" and z.px is not None and z.id != mz]
        if key == "worldmap":
            wz = [z for z in zs.zones if z.kind == "w" and z.px is not None and not self.assign.get(z.id)]
        ids = set(z.id for z in wz); mod = key.split(".")[0]
        def kin_only(zid): return all(k.split(".")[0] == mod for k in self.assign.get(zid, []) if k != key)
        last = self._homes().get(key)
        if last in ids and kin_only(last): return last
        if key == "worldmap": return None
        zid = next((zid for zid, keys in self.parse_windows(WINDOWS_DEFAULT)[1].items() if key in keys), None)
        if zid in ids and kin_only(zid): return zid
        empty = [z for z in wz if not self.assign.get(z.id)]
        kin = [z for z in wz if z.id in self.assign
               and any(k != key and k.split(".")[0] == mod for k in self.assign[z.id])]
        if kin:
            for kz in kin:
                kx, ky, kw, kh = kz.px
                for z in empty:
                    x, y, w, h = z.px; ov = min(y + h, ky + kh) - max(y, ky)
                    side = abs(x - (kx + kw)) <= SNAP_DIST or abs((x + w) - kx) <= SNAP_DIST
                    if side and ov * 2 > min(h, kh): return z.id
            return kin[0].id
        if empty:
            r = Snap.rect(self.gump_of(key)) if self.gump_of(key) is not None else None
            cx, cy = (r[0] + r[2] / 2.0, r[1] + r[3] / 2.0) if r else (0.0, 0.0)
            empty.sort(key=lambda z: (z.px[0] + z.px[2] / 2.0 - cx) ** 2 + (z.px[1] + z.px[3] / 2.0 - cy) ** 2)
            return empty[0].id
        return None
    def _refit(self, key):
        self.placed.pop(key, None); rec = self.fitted.get(key)
        if rec is not None and rec.get("kind") == "fit": rec.pop("told", None)
    def _key_of(self, g):
        key = self.gump_key.get(g)
        if key is None:
            for k in self.wins:
                if self.gump_of(k) is g: return k
        return key
    def _drop_zone(self, r):
        cx, cy = r[0] + r[2] // 2, r[1] + r[3] // 2; hit = None; covered = None
        for z in self.frames.zones:
            if z.kind != "w" or z.px is None: continue
            x, y, w, h = z.px
            if hit is None and x <= cx < x + w and y <= cy < y + h: hit = z
            ow = min(x + w, r[0] + r[2]) - max(x, r[0]); oh = min(y + h, r[1] + r[3]) - max(y, r[1])
            if (ow > 0 and oh > 0 and ow * oh * 2 > w * h and (covered is None or ow * oh > covered[0])):
                covered = (ow * oh, z)
        if covered is not None: hit = covered[1]
        return hit
    def takes(self, g):
        if not self.loaded or self.frames is None or not self.arrange: return False
        if self._key_of(g) is None or safe(Follow.alt_held, False): return False
        r = Snap.rect(g); return r is not None and self._drop_zone(r) is not None
    def _back(self): self.dirty = True; HOST.poke()
    def dropped(self, g, key=None, rect=None):
        if not self.loaded or self.frames is None: return
        if key is None: key = self._key_of(g)
        else:
            g = self.gump_of(key)
            if g is None: return
        if key is None: return
        if not self.arrange:
            if self.zone_of(key) is not None: self.fresh = self.dirty = True; HOST.poke()
            return
        self.arrange_last = time.time()
        if safe(Follow.alt_held, False): return
        r = rect if rect is not None else Snap.rect(g)
        if r is None: return
        cx, cy = r[0] + r[2] // 2, r[1] + r[3] // 2; hit = self._drop_zone(r); self.fresh = True
        if self.arrange_hot is not None:
            box = self.arrange_lit.get(self.arrange_hot)
            if box is not None: box.IsVisible = False
            self.arrange_hot = None
        for f, l in list(SNAP.links.items()):
            if f is g or l is g: SNAP.links.pop(f, None)
        old = self.zone_of(key)
        if hit is None:
            if old is None: return
            self._back()
            if not self.back_told:
                self.back_told = True
                Kit.say("%s stays in its zone; drop it on another zone to move it (Settings > Layout frees "
                           "windows)." % self.title_of(key), Kit.HUE_INFO)
            return
        if old == hit.id and len(self.assign.get(old, [])) <= 1: self._back(); return
        mz = self._map_zone(); others_there = [k for k in self.assign.get(hit.id, []) if k != key]
        lone = len(others_there) == 1 and self.gump_of(others_there[0]) is not None
        if (key != "worldmap" and hit.id == mz and hit.id != old and (old is None or not lone)) \
                or (key == "worldmap" and others_there and (old is None or not lone)):
            self._back()
            Kit.say("TazUO's World Map keeps its zone to itself; drop %s on another zone."
                       % (self.title_of(key) if key != "worldmap" else "it"), Kit.HUE_BAD)
            return
        if old != hit.id and self._too_small(key, hit, g): self._back(); return
        swap = None; slots_was = dict((k, self.placed.get(k)) for k in self.assign.get(hit.id, []))
        if old is not None:
            others = [k for k in self.assign.get(hit.id, []) if k != key] if old != hit.id else []
            if len(others) == 1 and self.gump_of(others[0]) is not None:
                swap = others[0]
                if self._too_small(swap, self.frames.by_id(old)): self._back(); return
            for k in list(self.assign.get(old, [])) + list(self.assign.get(hit.id, [])): self._refit(k)
            at = self.assign[old].index(key) if key in self.assign[old] else 0
            self.assign[old] = [k for k in self.assign[old] if k != key]
            if swap is not None:
                self.assign[old].insert(min(at, len(self.assign[old])), swap)
                self.assign[hit.id] = [k for k in self.assign[hit.id] if k != swap]; self.placed.pop(swap, None)
                self.squeezed_told.discard(swap)
            if not self.assign[old]: del self.assign[old]
        keys = self.assign.setdefault(hit.id, []); pos = len(keys)
        for i, k in enumerate(keys):
            p = slots_was.get(k) or self.placed.get(k)
            if p is None: continue
            if hit.stack in ("d", "u"): mid = p[1] + p[3] // 2; before = cy < mid if hit.stack == "d" else cy > mid
            else: mid = p[0] + p[2] // 2; before = cx < mid if hit.stack == "r" else cx > mid
            if before: pos = i; break
        keys.insert(pos, key); self.unfree(key); self.save_assign(); self.dirty = True; self.squeezed_told.discard(key)
        HOST.poke()
    def _size_of(self, key):
        base = self.base.get(key)
        if base is None:
            g = self.gump_of(key); r = Snap.rect(g) if g is not None and not isinstance(g, ClientWin) else None
            base = (r[2], r[3]) if r else None
        return base
    def slots_for(self, z, keys):
        if not keys or z is None or z.px is None: return []
        return list(zip(keys, self._slots(z, [(k, None, None, None, None, None, False, self._size_of(k) or (100, 100))
                                              for k in keys])))
    def preview_text(self, key, z, keys=None):
        if key is None or z is None or z.px is None: return ""
        t = self.title_of(key)
        if z.kind != "w": return "!%s can only go in a window zone." % t
        mz = self._map_zone()
        if (key != "worldmap" and z.id == mz and z.id != self.zone_of(key)) or \
                (key == "worldmap" and [k for k in self.assign.get(z.id, []) if k != key]):
            return "!TazUO's World Map keeps its zone to itself."
        mn = self._min_of(key)
        if mn and (z.px[2] < mn[0] or z.px[3] < mn[1]):
            return ("!%s needs %d x %d at least; this zone is %d x %d." % (t, mn[0], mn[1], z.px[2], z.px[3]))
        keys = ([k for k in (keys if keys is not None else self.assign.get(z.id, [])) if k != key] + [key]); slot = None
        for k, sl in self.slots_for(z, keys):
            if k == key: slot = sl
        if slot is None: slot = z.px
        w, h = max(1, slot[2]), max(1, slot[3]); base = self._size_of(key); shown = ""
        if base and base[0] > 0 and base[1] > 0:
            sc = min(1.0, float(w) / base[0], float(h) / base[1])
            if sc < 0.995: shown = " (shown at %d%%)" % int(round(sc * 100))
        return "%s: %d x %d here%s." % (t, w, h, shown)
    def edit(self, fresh=False):
        if self.editor is not None: return
        W, H = Kit.screen()
        if W <= 0 or H <= 0: return
        if fresh:
            names = self.frame_names(); n, name = 2, "Mine"
            while name in names or name == LAYOUT_DEFAULT: name = "Mine %d" % n; n += 1
            zs = ZoneSet(name, [], HOST.grid_size(), (W, H)); z = Zone("Zone 1", "w", (0, 0, 1, 1), "", (0, 0), "d", 0)
            z.set_px((W - 320) // 2, (H - 240) // 2, 320, 240, W, H); zs.zones.append(z)
        elif self.frames_name == LAYOUT_DEFAULT:
            zs = ZoneSet.default(W, H, self.occupied(), False); zs.generated = False
        else: zs = self.load_frames(self.frames_name, W, H) or self.frames_in_use(W, H).copy()
        self.editor = LayoutEditor(self, zs); self.editor.open()
    def poll(self):
        if self.editor is not None: self.editor.poll()
    def status_text(self):
        W, H = Kit.screen(); step = HOST.grid_size()
        if W <= 0 or H <= 0: return "Screen: not known yet"
        return "Screen: %d x %d, %s; grid %d px, %d x %d squares" % (
            W, H, ratio_class(W, H), step, (W + step - 1) // step, (H + step - 1) // step)
    def close(self):
        if self.editor is not None: self.editor.close(keep=False, quiet=True)


class LayoutEditor(object):
    BAR_W = 720; SETTLE = 0.3; FIELD_W = 52; ROW = 28
    KEYS = {"up": ("UP",), "down": ("DOWN",), "left": ("LEFT",), "right": ("RIGHT",),
            "delete": ("DELETE",), "z": ("Z",), "y": ("Y",), "enter": ("RETURN", "KP_ENTER"), "esc": ("ESCAPE",)}
    FIELDS = ("col", "row", "w", "h")
    def __init__(self, layout, zs):
        self.layout = layout; self.zs = zs; self.frames = {}; self.bar = None; self.store = ({}, {}); self.c = {}
        self.renames = {}; self.sel = zs.zones[0].id if zs.zones else None; self.multi = set(); self.grid_was = None
        self.fields = None; self.saveas_text = ""; self.bar_pos = None; self.rebuild = False; self.closed = False
        self.W, self.H = Kit.screen(); self.px_mode = False; self.undo, self.redo = [], []; self.keys_was = {}
        self.focus_was = None; self.raws = {}; self.said = None; self.del_armed = None; self.marks = None
        self.marks_sig = None; self.counts = (0, 0); self.handles = []; self.handles_sig = None; self.edge = None
        self.edge_g = None; self.edge_at = 0.0; self.pressed_was = False; self.pick = 0; self.pick_keys = []
        self.preview = ""; self.raws_ok = False
    def open(self):
        self.grid_was = HOST.grid_shown()
        if not self.grid_was: safe(HOST.grid_toggle)
        for z in self.zs.zones: self.build_zone(z)
        self.build_bar(); self.draw_marks()
    def close(self, keep, quiet=False):
        if self.closed: return
        self.closed = True
        for zid, fr in list(self.frames.items()): Kit.dispose(fr.get("g"))
        self.frames = {}; self._drop_handles()
        for a in ("bar", "marks", "edge_g"): Kit.dispose(getattr(self, a)); setattr(self, a, None)
        if self.grid_was is not None and HOST.grid_shown() != self.grid_was: safe(HOST.grid_toggle)
        self.layout.editor = None; self.layout.dirty = True; self.layout.page_refresh = True
        if not keep and not quiet: Kit.say("the saved zones are back.", Kit.HUE_INFO)
    def _snap(self): return ([z.copy() for z in self.zs.zones], self.sel, dict(self.renames))
    def push(self):
        self.undo.append(self._snap())
        if len(self.undo) > 50: del self.undo[0]
        self.redo = []
    def _restore(self, snap):
        zones, sel, renames = snap
        for zid in list(self.frames): Kit.dispose(self.frames[zid].get("g"))
        self.frames = {}; self.zs.zones = [z.copy() for z in zones]; self.renames = dict(renames)
        self.sel = (sel if self.zs.by_id(sel) is not None else (self.zs.zones[0].id if self.zs.zones else None))
        self.multi = set()
        for z in self.zs.zones: self.build_zone(z)
        self.rebuild = True
    def _hist(self, a, b, word):
        if not a: self.say("nothing to %s." % word, Kit.HUE_INFO); return
        b.append(self._snap()); self._restore(a.pop())
    def do_undo(self): self._hist(self.undo, self.redo, "undo")
    def do_redo(self): self._hist(self.redo, self.undo, "redo")
    def say(self, text, hue=None):
        if text == self.said: return
        self.said = text; Kit.say(text, Kit.HUE_BAD if hue is None else hue)
    def _windows_in(self, z):
        L = self.layout; zid = self.orig_id(z.id); return [L.title_of(k) for k in L.assign.get(zid, [])]
    def orig_id(self, zid):
        for was, now in self.renames.items():
            if now == zid: return was
        return zid
    def build_zone(self, z):
        old = self.frames.get(z.id, {}).get("g"); x, y, w, h = z.px; M = Kit.MARGIN
        fr = {"g": None, "resize_at": 0.0, "size": (w, h)}
        g = G.CreateModernGump(x, y, w, h, not z.lock, ZONE_MIN_W, ZONE_MIN_H, self._resized(z.id)); g.SetAlpha(0)
        if z.lock: g.CanMove = False
        Kit.add_window_frame(g, w, h, corners=False, mouse=False)
        Kit.add_box(g, M, M, w - 2 * M, h - 2 * M, 0.25, ZONE_COLORS.get(z.kind, "#FFFFFF")); self._draw_overlaps(g, z)
        if z.kind == "k": self._draw_game(g, z)
        if z.id == self.sel and self.pick: self._draw_preview(g, z)
        Kit.add_section(g, M, M, w - 2 * M, 30); sel = z.id == self.sel or z.id in self.multi
        fr["lbl"] = Kit.add_label(g, Kit.fit(z.id + ("  (locked)" if z.lock else ""), w - 2 * M - 24),
                                  M + 12, M + 7, Kit.HUE_TITLE if sel else Kit.HUE_TEXT)
        wins = self._windows_in(z) if z.kind == "w" else []
        fr["wins"] = Kit.add_label(g, Kit.fit(", ".join(wins), w - 2 * M - 24) if wins else "",
                                   M + 12, M + 30 + 6, Kit.HUE_TEXT)
        fr["sum"] = Kit.add_label(g, "", M + 12, M + 30 + 6 + (20 if wins else 0), Kit.HUE_INFO)
        Kit.catcher(g, M, M, w - 2 * M, 30, self._select(z.id), "Select the zone (Shift+click: pick more)" + (
            "; locked" if z.lock else "; drag to move it on the grid"), movable=not z.lock)
        Kit.place(g, x, y, w, h); G.AddGump(g); Kit.no_snap(g); Kit.on_moved(g, self._moved(z.id))
        fr["g"] = g; self.frames[z.id] = fr; self.update_zone(z); Kit.dispose(old)
    def _draw_overlaps(self, g, z):
        x, y, w, h = z.px
        for o in self.zs.zones:
            if o is z or o.px is None or not (z.overlap or o.overlap): continue
            ox, oy, ow, oh = o.px; ax, ay = max(x, ox), max(y, oy); bx, by = min(x + w, ox + ow), min(y + h, oy + oh)
            if bx - ax < 4 or by - ay < 4: continue
            for sx in range(ax, bx, 12): Kit.add_box(g, sx - x, ay - y, min(4, bx - sx), by - ay, 0.45, "#E8C15A")
    def _draw_game(self, g, z):
        zs = self.zs.copy(); Layout._overlap_shape(zs); kx, ky, kw, kh = zs.by_id(z.id).px; kx -= z.px[0]; ky -= z.px[1]
        for r in ((kx, ky + kh - 2, kw, 2), (kx, ky, 2, kh), (kx + kw - 2, ky, 2, kh), (kx, ky, kw, 2)):
            Kit.add_box(g, r[0], r[1], r[2], r[3], 0.9, "#E8C15A")
    def _draw_preview(self, g, z):
        key = self.pick_keys[self.pick] if 0 < self.pick < len(self.pick_keys) else None
        if key is None or z.kind != "w": return
        L = self.layout; keys = [k for k in L.assign.get(self.orig_id(z.id), []) if k != key] + [key]
        x, y = z.px[0], z.px[1]
        for k, (sx, sy, sw, sh) in L.slots_for(z, keys):
            Kit.add_box(g, sx - x, sy - y, max(1, sw), max(1, sh), 0.55, "#E8C15A" if k == key else "#202020")
            Kit.add_label(g, Kit.fit(L.title_of(k), max(20, sw - 16)), sx - x + 8, sy - y + sh - 26, Kit.HUE_TEXT)
    def update_zone(self, z):
        fr = self.frames.get(z.id)
        if fr is None: return
        step = HOST.grid_size(); x, y, w, h = z.px
        text = "%s, %d x %d squares" % (z.kind_name(), max(1, int(round(float(w) / step))),
                                        max(1, int(round(float(h) / step))))
        if z.overlap: text += ", overlaps"
        Kit.set_text(fr["sum"], Kit.fit(text, w - 2 * Kit.MARGIN - 24))
        Kit.set_text(fr["lbl"], Kit.fit(z.id + ("  (locked)" if z.lock else ""), w - 2 * Kit.MARGIN - 24),
                     Kit.HUE_TITLE if (z.id == self.sel or z.id in self.multi) else Kit.HUE_TEXT)
    def _select(self, zid):
        def hit():
            shift = bool(Client.key_held("shift"))
            if shift and self.sel is not None and zid != self.sel:
                if zid in self.multi: self.multi.discard(zid)
                else: self.multi.add(zid); self.multi.add(self.sel)
                self.rebuild = True; HOST.poke(); return
            if zid != self.sel or self.multi:
                self.multi = set(); self.sel = zid; self.pick = 0; self.rebuild = True; HOST.poke()
        return hit
    def _resized(self, zid):
        def hit(*args):
            fr = self.frames.get(zid)
            if fr is not None: fr["resize_at"] = time.time()
        return hit
    def _moved(self, zid):
        def hit():
            z = self.zs.by_id(zid); fr = self.frames.get(zid)
            if z is None or fr is None or not Kit.is_open(fr["g"]): return
            r = Snap.rect(fr["g"])
            if r is None: return
            if (r[0], r[1]) == (z.px[0], z.px[1]): return
            if z.lock:
                self.place_zone(z); self.say('zone "%s" is locked; click Lock to move it.' % z.id, Kit.HUE_INFO); return
            self.landed(z, r[0], r[1], z.px[2], z.px[3], resized=False)
        return hit
    def _blocker(self, z): hits = self.zs.overlaps(z); return hits[0] if hits else None
    def landed(self, z, x, y, w, h, resized=True):
        W, H = self.W, self.H; step = HOST.grid_size()
        if resized:
            w = max(ZONE_MIN_W, int(round(float(w) / step)) * step)
            h = max(ZONE_MIN_H, int(round(float(h) / step)) * step)
        w, h = min(w, W), min(h, H); best = Snap.near_anchor(x, y, w, h)
        if best is not None: nx, ny = best[1], best[2]
        else:
            nx = ny = None
            for tx in (0, max(0, W - w)):
                if abs(tx - x) <= SNAP_DIST: nx = tx
            for ty in (0, max(0, H - h)):
                if abs(ty - y) <= SNAP_DIST: ny = ty
            for o in self.zs.zones:
                if o is z or o.px is None: continue
                ox, oy, ow, oh = o.px
                if nx is None and oy < y + h + SNAP_DIST and y < oy + oh + SNAP_DIST:
                    for tx in (ox + ow, ox - w, ox, ox + ow - w):
                        if abs(tx - x) <= SNAP_DIST: nx = tx
                if ny is None and ox < x + w + SNAP_DIST and x < ox + ow + SNAP_DIST:
                    for ty in (oy + oh, oy - h, oy, oy + oh - h):
                        if abs(ty - y) <= SNAP_DIST: ny = ty
            if nx is None: nx = int(round(float(x) / step)) * step
            if ny is None: ny = int(round(float(y) / step)) * step
        was = z.px; self.push(); z.set_px(nx, ny, w, h, W, H)
        if not self.zs.push_clear(z, W, H, step):
            z.set_px(was[0], was[1], was[2], was[3], W, H); self.undo.pop(); o = self._blocker(z)
            self.say('no room for zone "%s" there%s; it stays where it was.' % (
                z.id, (' (it would cover "%s")' % o.id) if o is not None else ""))
        z.note_pins(W, H); self.place_zone(z); self.changed()
    def _refields(self): self.fields = None; self.show_fields()
    def changed(self): self._refields(); self.draw_marks()
    def place_zone(self, z):
        fr = self.frames.get(z.id)
        if fr is None: return
        x, y, w, h = z.px
        if ((w, h) != fr["size"] or z.overlap or z.kind == "k" or any(o.overlap for o in self.zs.zones)):
            self.build_zone(z); return
        try: Kit.place(fr["g"], x, y, w, h); Kit.moved_by_code(fr["g"])
        except Exception: pass
        self.update_zone(z)
    def keep(self, W, H):
        if (W, H) != (self.W, self.H):
            self.W, self.H = W, H; self.zs.reflow(W, H, HOST.grid_size())
            for z in self.zs.zones: self.place_zone(z)
            self.draw_marks()
    def gaps(self):
        W, H = self.W, self.H; zs = [z.px for z in self.zs.zones if z.px is not None]
        xs = [v for v in sorted(set([0, W] + [p[0] for p in zs] + [p[0] + p[2] for p in zs])) if 0 <= v <= W]
        ys = [v for v in sorted(set([0, H] + [p[1] for p in zs] + [p[1] + p[3] for p in zs])) if 0 <= v <= H]
        nx, ny = len(xs) - 1, len(ys) - 1; free = {}
        for j in range(ny):
            cy = (ys[j] + ys[j + 1]) / 2.0
            for i in range(nx):
                cx = (xs[i] + xs[i + 1]) / 2.0
                if not any(p[0] <= cx < p[0] + p[2] and p[1] <= cy < p[1] + p[3] for p in zs): free[(i, j)] = True
        seen, n = set(), 0
        for cell in free:
            if cell in seen: continue
            n += 1; stack = [cell]; seen.add(cell)
            while stack:
                i, j = stack.pop()
                for nb in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                    if nb in free and nb not in seen: seen.add(nb); stack.append(nb)
        rects = []
        for j in range(ny):
            i = 0
            while i < nx:
                if (i, j) in free:
                    i0 = i
                    while i < nx and (i, j) in free: i += 1
                    rects.append((xs[i0], ys[j], xs[i] - xs[i0], ys[j + 1] - ys[j]))
                else: i += 1
        merged = []
        for r in rects:
            for k, m in enumerate(merged):
                if m[0] == r[0] and m[2] == r[2] and m[1] + m[3] == r[1]:
                    merged[k] = (m[0], m[1], m[2], m[3] + r[3]); break
            else: merged.append(r)
        return merged, n
    def bad_overlaps(self):
        out = []; zones = self.zs.zones
        for i, a in enumerate(zones):
            for b in zones[i + 1:]:
                if a.px is None or b.px is None or b not in self.zs.overlaps(a): continue
                if a in self.zs.overlaps(b) or not b.overlap:
                    x0, y0 = max(a.px[0], b.px[0]), max(a.px[1], b.px[1])
                    x1 = min(a.px[0] + a.px[2], b.px[0] + b.px[2]); y1 = min(a.px[1] + a.px[3], b.px[1] + b.px[3])
                    if x1 > x0 and y1 > y0: out.append((a, b, (x0, y0, x1 - x0, y1 - y0)))
        return out
    def draw_marks(self):
        sig = (self.W, self.H, tuple((z.id, z.kind, z.overlap, tuple(z.px or ())) for z in self.zs.zones))
        if sig == self.marks_sig and Kit.is_open(self.marks): return
        self.marks_sig = sig; gaps, n = self.gaps(); bad = self.bad_overlaps(); counts = (n, len(bad))
        old, self.marks = self.marks, None; Kit.dispose(old)
        if gaps or bad:
            g = G.CreateGump(False, False)
            for (x, y, w, h) in gaps: Kit.add_box(g, x, y, w, h, 0.45, "#C83030")
            for a, b, (x, y, w, h) in bad: Kit.add_box(g, x, y, w, h, 0.55, "#C83030")
            Grid.show_overlay(g, 0, 0, self.W, self.H); self.marks = g
        if counts != self.counts: self.counts = counts; self.rebuild = True
    def _drop_handles(self):
        for g, side, r in self.handles: Kit.dispose(g)
        self.handles = []; self.handles_sig = None
    def _sync_handles(self):
        z = self.zs.by_id(self.sel) if self.sel else None; fr = self.frames.get(z.id) if z is not None else None
        sig = (z.id, tuple(z.px), z.lock, fr.get("g") if fr else None) if z is not None and z.px is not None else None
        if sig == self.handles_sig: return
        self._drop_handles(); self.handles_sig = sig
        if z is None or z.lock: return
        x, y, w, h = z.px; T = 10; L_ = max(24, min(80, w // 3)); V_ = max(24, min(80, h // 3))
        for side, r in (("l", (x, y + (h - V_) // 2, T, V_)), ("r", (x + w - T, y + (h - V_) // 2, T, V_)),
                        ("t", (x + (w - L_) // 2, y + Kit.MARGIN + 30, L_, T)),
                        ("b", (x + (w - L_) // 2, y + h - T, L_, T))):
            g = G.CreateGump(True, False); Kit.add_box(g, 0, 0, r[2], r[3], 0.9, "#E8C15A")
            Kit.catcher(g, 0, 0, r[2], r[3], lambda: None, "Drag to move this edge on the grid")
            g.SetRect(r[0], r[1], r[2], r[3]); G.AddGump(g); SNAP.skip_gump(g); self.handles.append((g, side, r))
    def _edge_tick(self, pressed):
        now = time.time()
        if self.edge is None:
            if pressed and not self.pressed_was and self.handles:
                m = Kit.mouse_pos()
                if m is not None:
                    for g, side, r in self.handles:
                        if r[0] <= m[0] < r[0] + r[2] and r[1] <= m[1] < r[1] + r[3]:
                            z = self.zs.by_id(self.sel)
                            if z is not None: self.edge = (z.id, side, m, tuple(z.px))
                            break
            return
        zid, side, m0, p0 = self.edge; z = self.zs.by_id(zid); m = Kit.mouse_pos()
        if z is None or m is None: self.edge = None; Kit.dispose(self.edge_g); self.edge_g = None; return
        x, y, w, h = p0; dx, dy = m[0] - m0[0], m[1] - m0[1]
        if side == "l": nx = min(x + w - ZONE_MIN_W, max(0, x + dx)); x, w = nx, w + (x - nx)
        elif side == "r": w = max(ZONE_MIN_W, min(self.W - x, w + dx))
        elif side == "t": ny = min(y + h - ZONE_MIN_H, max(0, y + dy)); y, h = ny, h + (y - ny)
        else: h = max(ZONE_MIN_H, min(self.H - y, h + dy))
        if pressed:
            if now - self.edge_at >= 0.05:
                self.edge_at = now; step = HOST.grid_size(); old, self.edge_g = self.edge_g, None; Kit.dispose(old)
                g = G.CreateGump(False, False)
                for bx, by, bw_, bh in ((0, 0, w, 2), (0, h - 2, w, 2), (0, 0, 2, h), (w - 2, 0, 2, h)):
                    Kit.add_box(g, bx, by, bw_, bh, 0.95, "#E8C15A")
                t = "%d x %d squares (%d x %d)" % (max(1, int(round(float(w) / step))),
                                                    max(1, int(round(float(h) / step))), w, h)
                Kit.add_box(g, 6, 6, Kit.text_w(t) + 12, 22, 0.85, "#000000"); Kit.add_label(g, t, 12, 8, Kit.HUE_TITLE)
                Grid.show_overlay(g, x, y, w, h); self.edge_g = g
            return
        self.edge = None; Kit.dispose(self.edge_g); self.edge_g = None
        if (x, y, w, h) != p0: self.landed_rect(z, x, y, w, h)
    def landed_rect(self, z, x, y, w, h):
        step = HOST.grid_size(); x0, y0, x1, y1 = [int(round(float(v) / step)) * step for v in (x, y, x + w, y + h)]
        x1, y1 = min(x1, self.W), min(y1, self.H)
        if x + w >= self.W - SNAP_DIST: x1 = self.W
        if y + h >= self.H - SNAP_DIST: y1 = self.H
        self.apply_rect(z, x0, y0, max(ZONE_MIN_W, x1 - x0), max(ZONE_MIN_H, y1 - y0))
    def apply_rect(self, z, x, y, w, h, typed=None):
        W, H = self.W, self.H
        if w > W or h > H or x < 0 or y < 0 or x + w > W or y + h > H:
            self.say('zone "%s" can\'t be %s there: it would run off the screen; make it '
                     'smaller or move it.' % (z.id, typed or "that size"))
            return False
        was = z.px; z.set_px(x, y, w, h, W, H); o = self._blocker(z)
        if o is not None:
            z.set_px(was[0], was[1], was[2], was[3], W, H)
            self.say('zone "%s" can\'t be %s there: it would cover "%s"; make it %s or move ' 'it.' % (
                z.id, typed or "that size", o.id,
                "shorter" if (h > was[3] and w <= was[2]) else "narrower" if w > was[2] else "smaller"))
            return False
        nw = z.px; z.set_px(was[0], was[1], was[2], was[3], W, H); self.push()
        z.set_px(nw[0], nw[1], nw[2], nw[3], W, H); z.note_pins(W, H); self.said = None; self.place_zone(z)
        self.changed(); return True
    @staticmethod
    def _cap_w(cap): return 35 + Kit.text_w(cap)
    def _flow(self, g, store, items, x0, y, x_max):
        x = x0
        for key, art, cap, tip in items:
            cw = self._cap_w(cap)
            if x > x0 and x + cw > x_max: x = x0; y += self.ROW
            if g is not None: Kit.art_button(g, store, key, art, x, y - 2, cap, tip)
            x += cw + 16
        return y
    def build_bar(self):
        old = self.bar; W = self.BAR_W; M, GAP = Kit.MARGIN, Kit.GAP; store = ({}, {}); c = {}
        g = G.CreateGump(True, True); IW = W - 2 * M; x_max = M + IW - 12
        z = self.zs.by_id(self.sel) if self.sel else None; L = self.layout; step = HOST.grid_size(); ops = []
        y1 = M + 30 + GAP; ry = y1 + 32; body = []
        if z is None:
            body.append(("label", "Click Add zone, then drag it into place.", M + 12, ry + 3, Kit.HUE_INFO))
            ry += self.ROW
        else:
            nx = M + 12 + Kit.text_w("Name:") + 8; body.append(("label", "Name:", M + 12, ry + 3, None))
            body.append(("box", "name", z.id, nx, ry, 130, False,
                         "Zone name, unique in this frame layout; Enter uses it"))
            items = [("kind", Kit.ART_PAGE, "Kind: " + z.kind_name(), "Switch kind: window, keep clear, reserved"),
                     ("stack", Kit.ART_PAGE, "Stack: " + z.stack_name(), "Switch the way windows stack in this zone"),
                     ("prio", Kit.ART_PAGE, "Shrinks: " + _ordinal(z.prio),
                      "Change when this zone shrinks to minimized bars on a small screen"),
                     ("overlap", Kit.ART_PAGE, "Overlap: " + ("on" if z.overlap else "off"),
                      "Let this zone lie over others (on) or keep clear of them (off)"),
                     ("lock", Kit.ART_PAGE, "Lock: " + ("on" if z.lock else "off"),
                      "Lock the zone against moving and resizing, or unlock it"),
                     ("dup", Kit.ART_OK, "Duplicate", "Add a copy of this zone beside it"),
                     ("remove", Kit.ART_CLOSE, "Remove", "Remove this zone (or Delete twice); its windows become free")]
            ops.append(("flow", items, nx + 130 + 16, ry))
            ry = self._flow(None, None, items, nx + 130 + 16, ry, x_max) + self.ROW; fx = M + 12
            unit = "px" if self.px_mode else "squares"
            for key, label, tip in (("col", "X:" if self.px_mode else "Col:", "Left edge in %s from the screen's left"),
                                    ("row", "Y:" if self.px_mode else "Row:", "Top edge in %s from the screen's top"),
                                    ("w", "W:", "Width in %s"), ("h", "H:", "Height in %s")):
                hi = (self.W if key in ("col", "w") else self.H)
                if not self.px_mode: hi = (hi + step - 1) // step
                body.append(("label", label, fx, ry + 3, None)); fx += Kit.text_w(label) + 6
                body.append(("box", key, "", fx, ry, self.FIELD_W, True,
                             (tip % unit) + " (%d-%d); Enter or Apply uses it, "
                             "Esc puts it back" % (0 if key in ("col", "row") else 1, hi)))
                fx += self.FIELD_W + 14
            items = [("apply", Kit.ART_OK, "Apply", "Use the typed values (Enter does too)"),
                     ("units", Kit.ART_PAGE, "Units: " + unit, "Switch between grid squares and pixels")]
            ops.append(("flow", items, fx + 4, ry)); ry = self._flow(None, None, items, fx + 4, ry, x_max) + self.ROW
            c["px_y"] = ry + 3; body.append(("px", M + 12, ry + 3)); ry += 20
            pins = ", ".join(n for p, n in (("L", "left"), ("T", "top"), ("R", "right"), ("B", "bottom"),
                                            ("X", "centre"), ("Y", "middle")) if p in z.pins)
            body.append(("pins", "Pinned: " + (pins or "none"), M + 12, ry + 3)); ry += 28
            items = [("even", Kit.ART_PLAY, "Even out", "Give this zone and those flush beside it in its row (or "
                      "column) equal sizes")]
            if len(self.multi) >= 2:
                items += [("al_" + e[0], Kit.ART_PLAY, "Align " + e,
                           "Line the picked zones' %s edges up with this zone's" % e)
                          for e in ("left", "top", "right", "bottom")]
                items.append(("same", Kit.ART_PLAY, "Same size", "Make the picked zones this zone's size"))
            ops.append(("flow", items, M + 12, ry)); ry = self._flow(None, None, items, M + 12, ry, x_max) + self.ROW
            if len(self.multi) >= 2:
                body.append(("label", Kit.fit("%d zones picked (Shift+click picks more or fewer)."
                                              % len(self.multi), IW - 24), M + 12, ry + 3, Kit.HUE_INFO))
                ry += 20
        ZH = ry - y1 + 6; y2 = y1 + ZH + GAP; wins_rows = []; WH = 0
        if z is not None and z.kind == "w":
            wins_rows = list(L.assign.get(self.orig_id(z.id), []))
            WH = 30 + 28 + 26 * len(wins_rows) + (20 if self.preview else 0) + 14
            if not wins_rows: WH += 20
        y3 = y2 + (WH + GAP if WH else 0); cls = ratio_class(self.W, self.H)
        others = [k for k in ("narrow", "wide", "ultrawide") if k != cls]
        presets = [("undo", Kit.ART_PAGE, "Undo", "Undo the last change (Ctrl+Z)"),
                   ("redo", Kit.ART_PAGE, "Redo", "Redo the last undo (Ctrl+Y)"),
                   ("from_default", Kit.ART_PLAY, "New from Default", "Start again from the Default layout"),
                   ("mirror", Kit.ART_PLAY, "Mirror", "Swap the zones left and right"),
                   ("copyto", Kit.ART_OK, "Copy to others",
                    "Use these zones on %s and %s screens too (save them first)" % tuple(others))]
        saved_other = [k for k in others if Kit.get_var((FRAMES_NAMED % self.zs.name) + "@" + k, "")]
        if saved_other:
            presets.append(("reflow", Kit.ART_PLAY, "Reflow from: " + saved_other[0],
                            "Rebuild from this layout's %s-screen version" % saved_other[0]))
            c["reflow_from"] = saved_other[0]
        prow = self._flow(None, None, presets, M + 12, 0, x_max); FH = 30 + 28 * 2 + prow + 20 * 3 + 10; H = y3 + FH + M
        Kit.add_window_frame(g, W, H); Kit.add_section(g, M, M, IW, 30)
        Kit.add_label(g, "ZONES", M + 30, M + 7, Kit.HUE_TITLE)
        Kit.add_label(g, Kit.fit('frame layout "%s"' % self.zs.name, IW - 250),
                      M + 30 + Kit.text_w("ZONES") + 12, M + 7, Kit.HUE_INFO)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None,
                       "Close the editor and bring back the saved zones")
        Kit.add_section(g, M, y1, IW, ZH, "ZONE  (selected)"); boxes = []
        for item in body:
            if item[0] == "label": Kit.add_label(g, item[1], item[2], item[3], item[4])
            elif item[0] == "box":
                key, text, bx, by, bw_, num, tip = item[1:]
                c[key] = Kit.with_tip(Kit.add_textbox(g, text, bx, by, bw_, numbers=num), tip); boxes.append(key)
            elif item[0] == "px": c["px"] = Kit.add_label(g, "", item[1], item[2], Kit.HUE_INFO); c["px_x"] = item[1]
            elif item[0] == "pins":
                Kit.with_tip(Kit.add_label(g, item[1], item[2], item[3], Kit.HUE_INFO),
                             "Edges kept on the screen's edge (or centre line) on other screen sizes")
        for op in ops: self._flow(g, store, op[1], op[2], op[3], x_max)
        if WH:
            Kit.add_section(g, M, y2, IW, WH, "WINDOWS  (in this zone, top to bottom)"); ry = y2 + 32
            Kit.add_label(g, "Window:", M + 12, ry + 3); dd_x = M + 12 + Kit.text_w("Window:") + 8; dd_w = 300
            bx = dd_x + dd_w + 16
            Kit.art_button(g, store, "w_add", Kit.ART_OK, bx, ry - 2, "Put it here",
                           "Put the picked window in this zone (no Arrange mode needed)")
            ry += 28
            if not wins_rows:
                Kit.add_label(g, "Pick a window above, then click Put it here.", M + 12, ry + 3, Kit.HUE_INFO); ry += 20
            for i, k in enumerate(wins_rows):
                Kit.add_label(g, Kit.fit(L.title_of(k), 300), M + 12, ry + 3)
                self._flow(g, store, [("w_%s_%d" % (w_, i), art, cap, tip % L.title_of(k)) for w_, art, cap, tip in (
                    ("up", Kit.ART_PAGE, "Up", "Move %s up the zone's stack"),
                    ("down", Kit.ART_PAGE, "Down", "Move %s down the zone's stack"),
                    ("out", Kit.ART_CLOSE, "Take out", "Free %s from the zone (it stays where it is)"))],
                    M + 12 + 310, ry, 1 << 30)
                ry += 26
            c["wins_rows"] = wins_rows
            if self.preview:
                Kit.add_label(g, Kit.fit(self.preview.lstrip("!"), IW - 24), M + 12, ry + 3,
                              Kit.HUE_BAD if self.preview.startswith("!") else Kit.HUE_INFO)
        Kit.add_section(g, M, y3, IW, FH, "FRAME LAYOUT"); ry = y3 + 32; x = M + 12
        for key, art, cap, tip in (("add", Kit.ART_OK, "Add zone", "Add a zone mid-screen to drag into place"),
                                   ("fill", Kit.ART_PLAY, "Fill the gaps", "Grow every zone into empty room beside it"),
                                   ("save", Kit.ART_OK, "Save",
                                    "Save as the frame layout in use (Default saves as Default (mine))"),
                                   ("saveas", Kit.ART_OK, "Save as", "Save under the name in the box")):
            Kit.art_button(g, store, key, art, x, ry - 2, cap, tip); x += self._cap_w(cap) + 16
        c["saveas"] = Kit.with_tip(Kit.add_textbox(g, self.saveas_text, x, ry, max(
            60, W - M - 12 - self._cap_w("Discard") - 16 - x), numbers=False),
            "A name for Save as (letters, digits, spaces)")
        cap = "Discard"
        Kit.art_button(g, store, "discard", Kit.ART_CLOSE, W - M - 12 - self._cap_w(cap), ry - 2,
                       cap, "Close the editor and bring back the saved zones")
        ry += 28; ry = self._flow(g, store, presets, M + 12, ry, x_max) + 28; n = len(self.zs.zones)
        nk = sum(1 for zz in self.zs.zones if zz.kind == "k"); nr = sum(1 for zz in self.zs.zones if zz.kind == "r")
        gaps, over = self.counts
        status = "%s, %d keep clear, %d reserved; %s, %s; %d x %d, %s" % (
            Kit.count(n, "zone"), nk, nr, Kit.count(gaps, "gap"), Kit.count(over, "overlap"), self.W, self.H, cls)
        Kit.add_label(g, Kit.fit(status, IW - 24), M + 12, ry + 3, Kit.HUE_BAD if (gaps or over) else Kit.HUE_INFO)
        ry += 20; lx = M + 12
        for col, name in ((ZONE_COLORS["w"], "window"), (ZONE_COLORS["k"], "keep clear"),
                          (ZONE_COLORS["r"], "reserved"), ("#C83030", "gap or overlap"),
                          ("#E8C15A", "overlap allowed")):
            Kit.add_box(g, lx, ry + 6, 12, 12, 0.9, col); Kit.add_label(g, name, lx + 16, ry + 3, Kit.HUE_INFO)
            lx += 16 + Kit.text_w(name) + 14
        ry += 20
        Kit.add_label(g, Kit.fit("Arrows nudge the zone a square; Shift+arrows resize it; Delete "
                                 "twice removes it.", IW - 24), M + 12, ry + 3, Kit.HUE_INFO)
        if WH:
            wl = L.all_windows(); names = ["(pick a window)"]; self.pick_keys = [None]
            for k, t in wl:
                zid = L.zone_of(k); names.append(Kit.fit(t + (' (in "%s")' % zid if zid else ""), 290))
                self.pick_keys.append(k)
            if self.pick >= len(names): self.pick = 0
            dd = G.CreateDropDown(dd_w, names, self.pick); dd.SetPos(dd_x, y2 + 32); g.Add(dd)
            c["w_pick"] = Kit.with_tip(dd, "A window for this zone; the zone shows where it would sit")
        ax, ay = Kit.anchor_pos("B", W, H)
        x, y = self.bar_pos or Kit.load_pos(LAYOUT_EDITOR_POS, (ax or 200, ay or 200), (W, H))
        if Kit.is_open(old): x, y = old.GetX(), old.GetY()
        Kit.place(g, x, y, W, H); G.AddGump(g); Kit.on_moved(g, self._bar_moved)
        self.bar, self.store, self.c = g, store, c; self.raws = {}
        for key in boxes + ["saveas"]:
            raw = Kit.client_control(c[key]) if key in c else None
            if raw is not None: self.raws[key] = raw
        self.fields = None; self.focus_was = None; self.show_fields(); Kit.dispose(old)
    def _bar_moved(self): Kit.save_pos(LAYOUT_EDITOR_POS, self.bar); self.bar_pos = Snap.pos(self.bar)
    def _values(self, z):
        x, y, w, h = z.px
        if self.px_mode: return tuple(str(v) for v in (x, y, w, h))
        step = HOST.grid_size()
        return tuple(str(v) for v in (int(round(float(x) / step)), int(round(float(y) / step)),
                                      max(1, int(round(float(w) / step))), max(1, int(round(float(h) / step)))))
    def show_fields(self):
        c = self.c; z = self.zs.by_id(self.sel) if self.sel else None
        if z is None or "col" not in c: return
        texts = self._values(z)
        if texts != self.fields:
            self.fields = texts
            for key, t in zip(self.FIELDS, texts): c[key].SetText(t)
        x, y, w, h = z.px
        if self.px_mode:
            step = HOST.grid_size()
            text = "%d x %d squares at square %d, %d" % (
                max(1, int(round(float(w) / step))), max(1, int(round(float(h) / step))),
                int(round(float(x) / step)), int(round(float(y) / step)))
        else: text = "%d x %d px at %d, %d" % (w, h, x, y)
        Kit.set_text(c["px"], Kit.fit(text, self.BAR_W - Kit.MARGIN - 12 - c["px_x"]))
    def _key(self, name):
        down = False
        for k in self.KEYS[name]:
            if API.IsKeyPressed(k): down = True; break
        was = self.keys_was.get(name, False); self.keys_was[name] = down; return down and not was
    def _focus(self):
        if not self.raws: return None
        try:
            Typing._find()
            f = (Typing._get(None, "KeyboardFocusControl", Typing.uim) if Typing.uim is not None else None)
        except Exception: f = None
        self.raws_ok = Typing.uim is not None; n = 0
        while f is not None and n < 4:
            for key, raw in self.raws.items():
                if Typing._same(f, raw): return key
            f = Typing._get(f, "Parent"); n += 1
        return None
    def _box_texts(self):
        c = self.c
        try: return tuple(str(c[k].Text or "").strip() for k in self.FIELDS)
        except Exception: return None
    def poll(self):
        if self.closed: return
        if not Kit.is_open(self.bar): self.close(keep=False); return
        now = time.time()
        for zid, fr in list(self.frames.items()):
            z = self.zs.by_id(zid); g = fr.get("g")
            if z is None or not Kit.is_open(g): continue
            if fr["resize_at"]:
                r = Snap.rect(g)
                if r is not None and (r[2], r[3]) != fr["size"]:
                    step = HOST.grid_size()
                    Kit.set_text(fr["sum"], Kit.fit("%d x %d squares" % (max(1, int(round(float(r[2]) / step))),
                        max(1, int(round(float(r[3]) / step)))), max(40, r[2] - 2 * Kit.MARGIN - 24)), Kit.HUE_TITLE)
                if now - fr["resize_at"] >= self.SETTLE:
                    fr["resize_at"] = 0.0
                    if r is not None and (r[2], r[3]) != fr["size"]:
                        if z.lock: self.build_zone(z)
                        else: self.landed(z, r[0], r[1], r[2], r[3], resized=True)
        pressed = SNAP.pressed() is True; self._sync_handles(); self._edge_tick(pressed); self.pressed_was = pressed
        store, c = self.store, self.c; z = self.zs.by_id(self.sel) if self.sel else None
        if Kit.was_clicked(store, "close") or Kit.was_clicked(store, "discard"): self.close(keep=False); return
        focus = self._focus(); typing = Client.typing(); enter = self._key("enter")
        esc = self._key("esc")
        if not typing and not self.edge:
            ctrl = bool(Client.key_held("ctrl")); shift = bool(Client.key_held("shift"))
            if self._key("z") and ctrl: self.do_undo()
            elif self._key("y") and ctrl: self.do_redo()
            elif z is not None:
                for name, d in (("left", (-1, 0)), ("right", (1, 0)), ("up", (0, -1)), ("down", (0, 1))):
                    if self._key(name): self.nudge(z, d, shift)
                if self._key("delete"): self.delete_pressed(z)
        if Kit.was_clicked(store, "add"):
            self.push(); zid = self.zs.new_id(); nz = Zone(zid, "w", (0, 0, 1, 1), "", (0, 0), "d", 0)
            nz.set_px((self.W - 320) // 2, (self.H - 240) // 2, 320, 240, self.W, self.H); self.zs.zones.append(nz)
            if not self.zs.push_clear(nz, self.W, self.H, HOST.grid_size()):
                self.zs.zones.remove(nz); self.undo.pop()
                self.say("no room for another zone; remove one or make one smaller."); return
            nz.note_pins(self.W, self.H); self.sel, self.multi = zid, set(); self.build_zone(nz); self.changed()
            self.rebuild = True
        elif Kit.was_clicked(store, "undo"): self.do_undo()
        elif Kit.was_clicked(store, "redo"): self.do_redo()
        elif Kit.was_clicked(store, "even") and z is not None:
            self.push(); n = self.zs.even_out(z, self.W, self.H, HOST.grid_size())
            if n < 2: self.undo.pop(); self.say("no zone sits flush beside this one in its row or column.")
            else: self._all_moved()
        elif Kit.was_clicked(store, "fill"):
            self.push(); self.zs.fill_gaps(self.W, self.H, HOST.grid_size()); self._all_moved()
        elif Kit.was_clicked(store, "save"):
            self.save(self.zs.name if self.zs.name != LAYOUT_DEFAULT else LAYOUT_MINE); return
        elif Kit.was_clicked(store, "saveas"):
            name = Layout.clean_name(safe(lambda: c["saveas"].Text, ""), "")
            if not name: self.say("type a name in the box, then click Save as.")
            else: self.save(name if name != LAYOUT_DEFAULT else LAYOUT_MINE); return
        elif Kit.was_clicked(store, "reflow") and c.get("reflow_from"):
            other = ZoneSet.parse(self.zs.name, Kit.get_var((FRAMES_NAMED % self.zs.name) + "@" + c["reflow_from"], ""))
            if other is not None:
                other.reflow(self.W, self.H, HOST.grid_size()); self.push()
                self._restore(([zz.copy() for zz in other.zones], self.sel, {})); self.changed()
        elif Kit.was_clicked(store, "from_default"):
            self.push(); d = ZoneSet.default(self.W, self.H, (), False)
            self._restore(([zz.copy() for zz in d.zones], self.sel, {})); self.changed()
        elif Kit.was_clicked(store, "mirror"):
            self.push()
            for zz in self.zs.zones:
                x, y, w, h = zz.px; zz.set_px(self.W - x - w, y, w, h, self.W, self.H)
            self._all_moved()
        elif Kit.was_clicked(store, "copyto"): self.copy_to()
        elif Kit.was_clicked(store, "units"):
            self.commit_rect(z, quiet=True) if z is not None else None; self.px_mode = not self.px_mode
            self.rebuild = True
        if z is not None and not self.rebuild: self.poll_zone(z, store)
        if z is not None and z.kind == "w" and not self.rebuild: self.poll_windows(z, store, c)
        if not self.rebuild: self.poll_fields(z, focus, enter, esc, Kit.was_clicked(store, "apply"))
        self.focus_was = focus; self.draw_marks()
        if self.rebuild:
            self.rebuild = False; self.saveas_text = str(safe(lambda: c["saveas"].Text, self.saveas_text) or "")
            for zz in self.zs.zones: self.update_zone(zz)
            self.build_bar()
    def _all_moved(self):
        for zz in self.zs.zones: zz.note_pins(self.W, self.H); self.place_zone(zz)
        self.changed()
    def poll_zone(self, z, store):
        if Kit.was_clicked(store, "kind"):
            self.push(); kinds = [k for k, n in ZONE_KINDS]; z.kind = kinds[(kinds.index(z.kind) + 1) % len(kinds)]
            z.hug = z.hug and z.kind == "w"; self.build_zone(z); self.changed()
            self.rebuild = True
        elif Kit.was_clicked(store, "stack"):
            self.push(); stacks = [k for k, n in ZONE_STACKS]
            z.stack = stacks[(stacks.index(z.stack) + 1) % len(stacks)]; self.rebuild = True
        elif Kit.was_clicked(store, "prio"): self.push(); z.prio = (z.prio + 1) % (SHRINK_MAX + 1); self.rebuild = True
        elif Kit.was_clicked(store, "overlap"):
            self.push(); z.overlap = not z.overlap
            if not z.overlap:
                if not self.zs.push_clear(z, self.W, self.H, HOST.grid_size()):
                    o = self._blocker(z)
                    self.say('zone "%s" still lies over "%s"; move it or make it smaller.'
                             % (z.id, o.id if o is not None else "a zone"), Kit.HUE_INFO)
                z.note_pins(self.W, self.H)
            for zz in self.zs.zones: self.build_zone(zz)
            self.changed(); self.rebuild = True
        elif Kit.was_clicked(store, "lock"): self.push(); z.lock = not z.lock; self.build_zone(z); self.rebuild = True
        elif Kit.was_clicked(store, "dup"): self.duplicate(z)
        elif Kit.was_clicked(store, "remove"): self.remove(z)
        else:
            for key, edge in (("al_l", "l"), ("al_t", "t"), ("al_r", "r"), ("al_b", "b"), ("same", "s")):
                if Kit.was_clicked(store, key): self.align(z, edge); break
    def poll_windows(self, z, store, c):
        L = self.layout; dd = c.get("w_pick"); now = time.time(); add = Kit.was_clicked(store, "w_add")
        if dd is not None and (now >= getattr(self, "_pick_next", 0.0) or now - HOST.input_at <= HOST.INPUT_FAST):
            self._pick_next = now + 0.2; i = LayoutPage._pick(dd, self.pick)
            if i != self.pick:
                self.pick = i; key = self.pick_keys[i] if 0 < i < len(self.pick_keys) else None
                self.preview = self.preview_text(key, z) if key else ""; self.build_zone(z); self.rebuild = True
                if not add: return
        zid = self.orig_id(z.id)
        if add:
            key = self.pick_keys[self.pick] if 0 < self.pick < len(self.pick_keys) else None
            if key is None: self.say("pick a window in the list first, then click Put it here.", Kit.HUE_INFO); return
            if L.frames is None or L.frames.by_id(zid) is None:
                self.say('zone "%s" isn\'t saved yet; click Save, then put the window in it.' % z.id); return
            if L.zone_of(key) == zid: self.say("%s already sits in this zone." % L.title_of(key), Kit.HUE_INFO); return
            mz = L._map_zone()
            if (key != "worldmap" and zid == mz) or (key == "worldmap" and L.assign.get(zid)):
                self.say("TazUO's World Map keeps its zone to itself; pick another zone for %s."
                         % (L.title_of(key) if key != "worldmap" else "it"))
                return
            if L._too_small(key, L.frames.by_id(zid)): return
            L.assign_to(key, zid); self.pick, self.preview = 0, ""; self.build_zone(z); self.rebuild = True; return
        rows = c.get("wins_rows") or []
        for i, k in enumerate(rows):
            for what in ("up", "down", "out"):
                if not Kit.was_clicked(store, "w_%s_%d" % (what, i)): continue
                keys = L.assign.get(zid, [])
                if k not in keys: break
                if what == "out": L.assign_to(k, None)
                else:
                    j = keys.index(k); t = j - 1 if what == "up" else j + 1
                    if 0 <= t < len(keys):
                        keys[j], keys[t] = keys[t], keys[j]
                        for kk in keys: L._refit(kk)
                        L.save_assign(); L.dirty = L.fresh = True; HOST.poke()
                self.build_zone(z); self.rebuild = True; return
    def preview_text(self, key, z):
        return self.layout.preview_text(key, z, self.layout.assign.get(self.orig_id(z.id), []))
    def poll_fields(self, z, focus, enter, esc, apply):
        c = self.c
        if z is None or "name" not in c: return
        left = self.focus_was if (self.focus_was is not None and focus != self.focus_was) else None
        if esc and (focus is not None or self._edited(z)): self._refields(); c["name"].SetText(z.id); return
        if (enter and focus == "name") or left == "name" or apply:
            name = str(safe(lambda: c["name"].Text, z.id) or "").strip()
            if name != z.id: self.rename(z, name); return
        if focus is None and left is None and enter and not self.raws_ok:
            name = str(safe(lambda: c["name"].Text, z.id) or "").strip()
            if name != z.id: self.rename(z, name); return
            self.commit_rect(z); return
        if ((enter and focus in self.FIELDS) or (left in self.FIELDS and focus not in self.FIELDS) or apply):
            self.commit_rect(z)
    def _edited(self, z):
        texts = self._box_texts(); name = str(safe(lambda: self.c["name"].Text, z.id) or "").strip()
        return (texts is not None and texts != self._values(z)) or name != z.id
    def commit_rect(self, z, quiet=False):
        texts = self._box_texts()
        if texts is None or texts == self._values(z): return
        try: col, row, w, h = [int(t) for t in texts]
        except Exception:
            if not quiet: self.say("type whole numbers in Col, Row, W and H.")
            self._refields(); return
        step = 1 if self.px_mode else HOST.grid_size(); x, y = max(0, col) * step, max(0, row) * step
        w, h = max(1, w) * step, max(1, h) * step
        typed = "%d x %d %s" % (max(1, int(texts[2])), max(1, int(texts[3])), "px" if self.px_mode else "squares")
        if w < ZONE_MIN_W or h < ZONE_MIN_H:
            if not quiet:
                self.say('zone "%s" can\'t be %s: the smallest zone is %d x %d px.' % (
                    z.id, typed, ZONE_MIN_W, ZONE_MIN_H))
            self._refields(); return
        if z.lock:
            self.say('zone "%s" is locked; click Lock to change it.' % z.id, Kit.HUE_INFO); self._refields(); return
        if not self.apply_rect(z, x, y, w, h, typed): self._refields()
    def rename(self, z, name):
        name = Layout.clean_name(name, "")
        if not name or name.lower() == "frames" or self.zs.by_id(name) is not None:
            self.say('zone "%s" can\'t be called "%s": %s.' % (
                z.id, name, "a name needs letters or digits" if not name else
                "the name is taken" if self.zs.by_id(name) is not None else "that name is kept"))
            self.c["name"].SetText(z.id); return
        self.push(); old = z.id; z.id = name
        for k, v in self.renames.items():
            if v == old: self.renames[k] = name; break
        else: self.renames[old] = name
        fr = self.frames.pop(old, None)
        if fr is not None: self.frames[name] = fr
        self.sel = name; self.multi = set(name if m == old else m for m in self.multi); self.said = None
        self.build_zone(z); self.rebuild = True
    def nudge(self, z, d, resize):
        if z.lock: self.say('zone "%s" is locked; click Lock to change it.' % z.id, Kit.HUE_INFO); return
        step = HOST.grid_size(); x, y, w, h = z.px
        if resize: self.apply_rect(z, x, y, max(ZONE_MIN_W, w + d[0] * step), max(ZONE_MIN_H, h + d[1] * step))
        else: self.apply_rect(z, x + d[0] * step, y + d[1] * step, w, h)
    def delete_pressed(self, z):
        now = time.time()
        if (self.del_armed is not None and self.del_armed[0] == z.id and now - self.del_armed[1] <= 3.0):
            self.del_armed = None; self.remove(z); return
        self.del_armed = (z.id, now); Kit.say('press Delete again to remove zone "%s".' % z.id, Kit.HUE_INFO)
    def remove(self, z):
        if z.lock: self.say('zone "%s" is locked; click Lock to remove it.' % z.id, Kit.HUE_INFO); return
        self.push(); self.zs.zones = [zz for zz in self.zs.zones if zz is not z]; fr = self.frames.pop(z.id, None)
        if fr is not None: Kit.dispose(fr.get("g"))
        self.multi.discard(z.id); self.sel = self.zs.zones[0].id if self.zs.zones else None; self.changed()
        self.rebuild = True
    def duplicate(self, z):
        self.push(); nz = z.copy(); nz.id = self.zs.new_id(); nz.lock = False; step = HOST.grid_size()
        x, y, w, h = z.px; nz.set_px(x + step, y + step, w, h, self.W, self.H); self.zs.zones.append(nz)
        if not nz.overlap and not self.zs.push_clear(nz, self.W, self.H, step):
            self.zs.zones.remove(nz); self.undo.pop()
            self.say("no room for a copy of zone \"%s\"; make room first." % z.id); return
        nz.note_pins(self.W, self.H); self.sel, self.multi = nz.id, set(); self.build_zone(nz); self.changed()
        self.rebuild = True
    def align(self, z, edge):
        picked = [p for p in [self.zs.by_id(i) for i in self.multi if i != z.id] if p is not None and not p.lock]
        if not picked: return
        self.push(); x, y, w, h = z.px; refused = []
        for p in picked:
            px, py, pw, ph = p.px
            r = {"l": (x, py, pw, ph), "t": (px, y, pw, ph), "r": (x + w - pw, py, pw, ph),
                 "b": (px, y + h - ph, pw, ph)}.get(edge, (px, py, w, h))
            was = p.px; p.set_px(r[0], r[1], r[2], r[3], self.W, self.H)
            if self._blocker(p) is not None:
                p.set_px(was[0], was[1], was[2], was[3], self.W, self.H); refused.append(p.id)
            p.note_pins(self.W, self.H)
        if refused:
            self.say("%s would cover another zone, so %s stayed where %s %s." % (
                ", ".join('"%s"' % r for r in refused), "it" if len(refused) == 1 else "they",
                "it" if len(refused) == 1 else "they", "was" if len(refused) == 1 else "were"), Kit.HUE_INFO)
        self._all_moved()
    def copy_to(self):
        name = self.zs.name
        if self.zs.generated or name == LAYOUT_DEFAULT or name not in self.layout.frame_names():
            self.say("save these zones first (Save or Save as), then click Copy to.", Kit.HUE_INFO); return
        cls = ratio_class(self.W, self.H); zs = self.zs.copy(name); zs.screen = (self.W, self.H)
        zs.grid = HOST.grid_size()
        for zz in zs.zones: zz.note_pins(self.W, self.H)
        text = zs.save_text(); others = [k for k in ("narrow", "wide", "ultrawide") if k != cls]
        for k in others: Kit.put_var((FRAMES_NAMED % name) + "@" + k, text)
        Kit.say('frame layout "%s" copied to %s screens.' % (name, " and ".join(others)), Kit.HUE_GOOD)
    def warnings(self):
        out = []; L = self.layout
        for z in self.zs.zones:
            if z.kind != "w" or z.px is None: continue
            for k in L.assign.get(self.orig_id(z.id), []):
                mn = L._min_of(k)
                if mn and (z.px[2] < mn[0] or z.px[3] < mn[1]):
                    out.append('zone "%s" is %d x %d, smaller than %s can be (%d x %d)' % (
                        z.id, z.px[2], z.px[3], L.title_of(k), mn[0], mn[1]))
        gaps, over = self.counts
        if gaps: out.append("the zones leave %s (Fill the gaps closes them)" % Kit.count(gaps, "gap"))
        if over: out.append("%s of zones without Overlap on" % Kit.count(over, "overlap"))
        if not any(z.kind == "k" for z in self.zs.zones): out.append("no keep-clear zone: nothing marks the game view")
        return out
    def save(self, name):
        for w in self.warnings(): Kit.say("note: %s." % w, Kit.HUE_INFO)
        zs = self.zs.copy(name); zs.generated = False; zs.ver = 2; self.layout.save_frames(zs, name, self.W, self.H)
        L, moved = self.layout, False
        for was, now in self.renames.items():
            if was != now and was in L.assign and now not in L.assign: L.assign[now] = L.assign.pop(was); moved = True
        if moved: L.save_assign()
        Kit.say('frame layout "%s" saved.' % name, Kit.HUE_GOOD); self.close(keep=True)
        self.layout.use_frames(name, tell=False)


class LayoutPage(_Page):
    H, DD_W = 200, 170
    def page(self, w):
        L = LAYOUT; lbl = {"hue": Kit.HUE_TEXT, "ndy": 3}; wins = L.all_windows()
        out = (("LAYOUT  (where each window sits)", (("note", "Zones:", dict(lbl, stay=True)),
            ("buttons", (("edit", Kit.ART_PAGE, "Edit zones", "Drag, resize, add or remove zones on the screen grid"),
                         ("new", Kit.ART_OK, "New zones", "Start a new frame layout with one zone"),
                         ("remove", Kit.ART_CLOSE, "Remove zones", "Delete the frame layout in use (not Default)")),
             {"dx": 278}), ("note", "Windows:", dict(lbl, stay=True)), ("buttons", (("save", Kit.ART_OK, "Save windows",
                          "Save where every window sits as the window layout in use"),
                         ("reset", Kit.ART_CLOSE, "Reset", "Go back to the Default window layout"),
                         ("free", Kit.ART_CLOSE, "Free all", "Take every window out of its zone")), {"dx": 278}),
            ("check", "game", "Give an empty zone's room to the game area",
             "Widens the game area beside an empty zone"),
            ("check", "fit_view", "Fit the game view to the keep-clear zone",
             "Borderless, sized and locked to that zone; "
             "unticked or stopped, your own view comes back", {"stay": True}),
            ("buttons", (("check", Kit.ART_PLAY, "Check fit", "Print where each window in a zone sits and whether it "
                          "fills it"),), {"dx": w - 47 - Kit.text_w("Check fit"), "h": 26}),
            ("buttons", (("arrange", Kit.ART_OK if L.arrange else Kit.ART_PLAY,
                          "Done" if L.arrange else "Arrange windows", "Lock every window in its zone" if L.arrange else
                          "Unlock windows to move them between zones (Esc or Done locks them)"),), {"stay": True}),
            ("buttons", (("reclaim", Kit.ART_PLAY, "Reclaim space", "Give the game area every gap beside it; windows "
                          "keep their size"),) +
             ((("reclaim_undo", Kit.ART_CLOSE, "Undo", "Put the zones back as before Reclaim space"),)
              if L._undo_load() is not None else ()), {"dx": 278}),
            ("note", Kit.fit(L.status_text(), w - 24)), ("custom", 0, self._drops)), {"top": 32, "pad": 12}),)
        if not wins: return out
        pv = L.page_preview; rows = [("note", Kit.fit(t, 270), dict(lbl, h=26)) for k, t in wins]
        if pv: rows.append(("note", Kit.fit(pv.lstrip("!"), w - 24),
                            {"ndy": 3, "hue": Kit.HUE_BAD if pv.startswith("!") else Kit.HUE_INFO}))
        rows.append(("custom", 0, lambda f, x, y: self._zone_drops(f, x, wins)))
        return out + (("WINDOWS  (the zone each sits in)", rows, {"top": 32, "pad": 8}),)
    def height(self, w): return Kit.Form.height(self.page(w), w, bgap=16)
    def build(self, g, x, y, w):
        f = Kit.Form(g, x, y, w, {"game": LAYOUT.game_grows, "fit_view": LAYOUT.fit_view}, self.page(w), bgap=16)
        self.store, self.c = f.store, f.c
    def _drop(self, g, names, i, x, y, tip):
        dd = G.CreateDropDown(self.DD_W, names, i); dd.SetPos(x, y); g.Add(dd); return Kit.with_tip(dd, tip)
    def _drops(self, f, x, y):
        L, c, y = LAYOUT, f.c, f.top + 32; self.frame_names = [LAYOUT_DEFAULT] + L.frame_names()
        fi = self.frame_names.index(L.frames_name) if L.frames_name in self.frame_names else 0
        c["zones"] = (self._drop(f.g, self.frame_names, fi, x + 92, y, "The frame layout in use (its zones)"), fi)
        self.layout_names = ["(none)", LAYOUT_DEFAULT, LAYOUT_MIRRORED] + L.layout_names()
        cur = L.layout_name or "(none)"; li = self.layout_names.index(cur) if cur in self.layout_names else 0
        c["windows"] = (self._drop(f.g, self.layout_names, li, x + 92, y + 28,
                                   "The window layout in use; pick one to place every window"), li)
        c["zone_dd"] = []
    def _zone_drops(self, f, x, wins):
        L, ry = LAYOUT, f.top + self.H + Kit.GAP + 32; zones = ["free"] + [z for z in L.zone_choices() if z]
        for key, title in wins:
            zid = L.zone_of(key); ids, labels = zones, zones
            if zid is not None and zid not in zones:
                ids, labels = zones + [zid], zones + [Kit.fit("%s (missing)" % zid, self.DD_W - 30)]
            zi = ids.index(zid) if zid in ids else 0
            f.c["zone_dd"].append((key, self._drop(f.g, labels, zi, x + 302, ry,
                                                   "The zone %s sits in (free: stays where you put it)" % title),
                                        zi, ids))
            ry += 26
    @staticmethod
    def _pick(dd, was):
        try: return int(dd.GetSelectedIndex())
        except Exception: return was
    def poll(self):
        c = self.c
        if c is None: return
        L = LAYOUT
        if L.page_refresh: L.page_refresh = False; HOST.refresh_settings(LAYOUT_PAGE); return
        for n, (key, dd3, zi, ids) in enumerate(c["zone_dd"]):
            i = self._pick(dd3, zi)
            if i != zi and 0 <= i < len(ids):
                c["zone_dd"][n] = (key, dd3, i, ids); zid = None if i == 0 else ids[i]; L.page_preview = ""
                if zid:
                    W, H = Kit.screen(); zs = L.frames_in_use(W, H) if W > 0 and H > 0 else None
                    z = zs.by_id(zid) if zs is not None else None; L.page_preview = L.preview_text(key, z)
                L.assign_to(key, zid); L.page_refresh = True; return
        dd, fi = c["zones"]; i = self._pick(dd, fi)
        if i != fi and 0 <= i < len(self.frame_names): c["zones"] = (dd, i); L.use_frames(self.frame_names[i]); return
        dd2, li = c["windows"]; i = self._pick(dd2, li)
        if i != li and 0 <= i < len(self.layout_names):
            c["windows"] = (dd2, i); L.use_windows("" if i == 0 else self.layout_names[i]); return
        for k, attr in (("game", "game_grows"), ("fit_view", "fit_view")):
            v = bool(c[k].IsChecked)
            if v != getattr(L, attr):
                setattr(L, attr, v); L.save_opts(); L.dirty = True
                if k != "game": L.fresh = True
        if Kit.was_clicked(self.store, "reclaim"): L.reclaim_space(); return
        if Kit.was_clicked(self.store, "reclaim_undo"): L.reclaim_back(); return
        if Kit.was_clicked(self.store, "check"): L.report_fit()
        if Kit.was_clicked(self.store, "arrange"): L.set_arrange(not L.arrange); return
        if Kit.was_clicked(self.store, "edit"): L.edit(fresh=False)
        elif Kit.was_clicked(self.store, "new"): L.edit(fresh=True)
        elif Kit.was_clicked(self.store, "remove"):
            if not L.remove_frames(L.frames_name):
                Kit.say("Default can't be deleted; pick another frame layout first.", Kit.HUE_BAD)
        elif Kit.was_clicked(self.store, "save"): L.save_windows()
        elif Kit.was_clicked(self.store, "reset"): L.use_windows(LAYOUT_DEFAULT)
        elif Kit.was_clicked(self.store, "free"): L.use_windows("")


LAYOUT_PAGE = "va.layout"
SNAP = Snap()
ALERTS = Alerts()
GUARD = Guard()
LAYOUT = Layout()
HOST = Host()
MODULE_FILES = (("actionbar", "Action Bar", "ActionBarModule.py"), ("hud", "Character HUD", "CharacterHudModule.py"),
    ("inventory", "Inventory", "InventoryModule.py"), ("grimoire", "Grimoire", "GrimoireModule.py"),
    ("worldmap", "World Map", "WorldMapModule.py"), ("ultima", "Ultima Tracker", "UltimaTrackerModule.py"),
    ("social", "Social", "SocialModule.py"), ("skills", "Skills", "SkillsModule.py"),
    ("butler", "Property Butler", "PropertyButlerModule.py"), ("meters", "Meters", "MetersModule.py"),
    ("mongotchi", "Mongotchi", "MongotchiModule.py"),)
RETIRED_KEYS = ("autodoors",)


def module_folders():
    places = []; base = str(API.ScriptPath or "").rstrip("/\\")
    if base:
        if os.path.isfile(base): base = os.path.dirname(base)
        places += [base, os.path.dirname(base)]
    try:
        import System; root = str(System.AppDomain.CurrentDomain.BaseDirectory).rstrip("/\\")
        places += [os.path.join(root, "LegionScripts"), root]
    except Exception: pass
    found = {}
    for p in places:
        if not p: continue
        for n in (safe(lambda: os.listdir(p), []) or []):
            if n in found or not (n.startswith("VirtueAssistant") and n.endswith("Modules")): continue
            d = os.path.join(p, n)
            if os.path.isdir(d): found[n] = d
    names = ([MODULE_DIR] if MODULE_DIR in found else []) + sorted(n for n in found if n != MODULE_DIR)
    return [found[n] for n in names]


def _read_text(path):
    try:
        with open(path, "r") as f: return f.read()
    except Exception: import System; return str(System.IO.File.ReadAllText(path))


class _Reg(object):
    ok = False
    def take(self, key, title, desc, factory=None, interval=None, default_on=False,
             category=None, parts=(), aliases=()):
        self.key, self.title, self.desc = str(key), str(title), str(desc)
        self.interval = interval if isinstance(interval, (int, float)) else None; self.default_on = bool(default_on)
        self.category = category; self.parts = tuple(tuple(p) for p in (parts or ()))
        self.aliases = tuple(aliases or ()); self.ok = True


def _balanced(text, start):
    depth, i, n = 0, start, len(text); quote = None
    while i < n:
        ch = text[i]
        if quote:
            if ch == "\\": i += 2; continue
            if ch == quote: quote = None
        elif ch in "\"'": quote = ch
        elif ch == "#": j = text.find("\n", i); i = n if j < 0 else j; continue
        elif ch == "(": depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0: return text[start + 1:i]
        i += 1
    return None


def read_registration(text):
    at = text.rfind("HOST.add(")
    if at < 0: return None
    args = _balanced(text, at + len("HOST.add"))
    if args is None: return None
    ns = {}
    for name in set(re.findall(r"[A-Za-z_]\w*", args)):
        v = globals().get(name); ns[name] = v if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    reg = _Reg(); ns["_reg"] = reg.take
    try: eval("_reg(" + args + ")", {"__builtins__": {}}, ns)
    except Exception: return None
    return reg if reg.ok else None


def load_modules():
    folders = module_folders()
    if not folders: Kit.say("no %s folder beside this script, so no modules loaded." % MODULE_DIR, Kit.HUE_BAD); return
    order = dict((f, i) for i, (_, _, f) in enumerate(MODULE_FILES)); entries, taken = [], set()
    for d in folders:
        for n in sorted(n for n in safe(lambda: os.listdir(d), []) or [] if n.endswith("Module.py")):
            if n not in taken: taken.add(n); entries.append((d, n))
    entries.sort(key=lambda e: order.get(e[1], len(order)))
    titles = dict((f, (k, t)) for k, t, f in MODULE_FILES); prefs = Kit.codec_load(Kit.get_var(SETTINGS_KEY))
    on = set(k for k in prefs.get("modules", "").split(",") if k)
    for where, name in entries:
        path = os.path.join(where, name)
        if not os.path.isfile(path): continue
        m = None
        try:
            text = _read_text(path); m = read_registration(text)
            if m is not None and m.key in RETIRED_KEYS:
                Kit.say("skipped %s (retired; the file can be deleted)." % name, Kit.HUE_INFO); continue
            if m is not None and m.key in HOST.old_map and HOST.old_map[m.key][0] != m.key:
                mk, pk = HOST.old_map[m.key]; home = dict.get(HOST.by_key, mk)
                Kit.say("skipped %s (now part of %s; the file can be deleted)." % (
                    name, home.title if home else mk), Kit.HUE_INFO)
                continue
            if m is not None and dict.__contains__(HOST.by_key, m.key):
                API.SysMsg(HOST.TWICE % (APP_NAME, m.title, m.key), Kit.HUE_BAD); continue
            wanted = m is not None and (m.key in on or any(
                old in on for p in m.parts for old in (p[4] if len(p) > 4 else ())))
            if m is not None and m.interval is not None and not wanted:
                HOST.add_lazy(m.key, m.title, m.desc, path, m.interval, m.default_on, m.category, m.parts, m.aliases)
                continue
            exec(compile(text, path, "exec"), globals())
        except Exception as ex:
            line = getattr(ex, "lineno", None)
            if line: msg = "%s (%s line %s)" % (getattr(ex, "msg", None) or ex, name, line)
            else: msg = "%s%s" % (ex, _error_where())
            Kit.say("%s could not be loaded: %s" % (name, msg), Kit.HUE_BAD)
            kt = (m.key, m.title) if m is not None else titles.get(name)
            if kt is not None and not dict.__contains__(HOST.by_key, kt[0]):
                key, title = kt; s = HOST.add(key, title, "", lambda: None, 0.1); s.api, s.broken = None, msg


Kit.data_setup()
PROFILES = Profiles()
if not VA_ALONE:
    try: PROFILES.startup()
    except Exception as _ex:
        Kit.say("the favourite profile could not be put on this character: %s%s"
                   % (Tz.why(_ex), _error_where()), Kit.HUE_BAD)


def _module_sysstats():
    KEY = "sysstats"; TITLE = "System Stats"
    POS_KEY, MIN_KEY, BTN_KEY, OPEN_KEY = ("SystemStats_pos", "SystemStats_min", "SystemStats_btn", "SystemStats_open")
    W, MINI_W, MINI_H = 240, 240, 46; EVERY = 0.3; TRAY_ICON = 0x1F2D
    ROWS = ("Ping", "FPS", "Frame", "Memory", "In", "Out", "Packets")
    st = {"shutting": False, "minimized": False, "docked": False, "open": False, "queue": [],
          "next": 0.0, "vals": {}, "tip": None}
    win = {"g": None, "c": {}, "store": ({}, {})}; btn = {"g": None, "b": None, "store": ({}, {})}
    queue = Kit.queuer(st)
    def read():
        v = {}
        try:
            fps = int(Tz.get(None, "CurrentRefreshRate", Tz.T("ClassicUO.CUOEnviroment"))); v["FPS"] = str(fps)
            v["Frame"] = "%.1f ms" % (1000.0 / fps) if fps > 0 else "-"
        except Exception: pass
        try:
            sock = Tz.get(None, "Socket", Tz.T("ClassicUO.Network.AsyncNetClient")); stats = Tz.get(sock, "Statistics")
            src = str(Typing._get(stats, "CurrentPingSource", default="") or "")
            v["Ping"] = "off" if src.endswith("Disabled") else "%d ms" % int(Tz.get(stats, "Ping"))
            v["In"] = "%.1f KB/s" % (int(Tz.get(stats, "DeltaBytesReceived")) / 1024.0)
            v["Out"] = "%.1f KB/s" % (int(Tz.get(stats, "DeltaBytesSent")) / 1024.0)
            v["Packets"] = "%d in, %d out" % (int(Tz.get(stats, "TotalPacketsReceived")),
                                              int(Tz.get(stats, "TotalPacketsSent")))
        except Exception: pass
        try: import System; v["Memory"] = "%d MB" % (int(System.GC.GetTotalMemory(False)) // (1024 * 1024))
        except Exception: pass
        return v
    def build_button():
        x, y = Kit.load_pos(BTN_KEY, (8, 200), (46, 46)); store = ({}, {}); g = G.CreateGump(True, True)
        Kit.add_window_frame(g, 46, 46, corners=False); st["tip"] = None
        b = Kit.art_button(g, store, "stats", Kit.ART_CIRCLE, 12, 12, None, "System stats", on_click=queue("toggle"))
        Kit.show_window(g, x, y, 46, 46, None, False, None, lambda: Kit.save_pos(BTN_KEY, g), btn,
                        {"g": g, "b": b, "store": store})
    def build_window():
        M = Kit.MARGIN; h = M + 30 + Kit.GAP + len(ROWS) * 20 + M - 12; g, store, c = wnd.begin(W, h)
        if not st["minimized"]:
            wnd.frame(g, settings=False); yb = M + 30 + Kit.GAP; Kit.add_section(g, M, yb, W - 2 * M, h - yb - M)
            for i, name in enumerate(ROWS):
                Kit.add_label(g, name + ":", M + 10, yb + 6 + i * 20, Kit.HUE_INFO)
                c[name] = Kit.add_label(g, "", M + 90, yb + 6 + i * 20, Kit.HUE_TEXT)
        wnd.end(g); refresh()
    wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, default=(70, 200), mini=(MINI_W, MINI_H),
                     icon=TRAY_ICON, close_tip="Close")
    def refresh():
        v = st["vals"]; c = win["c"]
        if st["minimized"]:
            lbl = c.get("status")
            if lbl is not None: Kit.set_text(lbl, "%s: %s, %s FPS" % (TITLE, v.get("Ping", "-"), v.get("FPS", "-")))
            return
        for name in ROWS:
            lbl = c.get(name)
            if lbl is not None: Kit.set_text(lbl, v.get(name, "-"))
    def open_window():
        st["open"] = True; build_window(); wnd.dock()
    def close_window(): st["open"] = False; HOST.dock_remove(KEY); wnd.close(); Kit.put_var(OPEN_KEY, "0")
    def _start():
        st.update({"shutting": False, "docked": False, "queue": [], "next": 0.0, "minimized": Kit.load_min(MIN_KEY)
                   or HOST.dock_wanted(KEY), "open": Kit.get_var(OPEN_KEY, "0") == "1"})
        build_button()
        if st["open"] or HOST.layout_holds(KEY): open_window()
    def _tick():
        now = time.time()
        while st["queue"]:
            action = st["queue"].pop(0)
            if action == "toggle":
                if st["open"] and not HOST.layout_holds(KEY): close_window()
                elif not st["open"]: Kit.put_var(OPEN_KEY, "1"); st["minimized"] = st["docked"] = False; open_window()
            elif action == "redraw":
                if st["open"]: build_window()
            else: Kit.win_action(action, st, KEY, TITLE, build_window, MIN_KEY)
        if st["open"] and Kit.was_clicked(win["store"], "close"): close_window()
        if not 0 <= st["next"] - now <= EVERY:
            st["next"] = now + EVERY; v = st["vals"] = read()
            tip = "Ping %s, %s FPS, memory %s; click to open or close the window" % (
                v.get("Ping", "-"), v.get("FPS", "-"), v.get("Memory", "-"))
            if tip != st["tip"] and btn["b"] is not None: st["tip"] = tip; Kit.with_tip(btn["b"], tip)
            if st["open"] and win["g"] is not None and not (st["minimized"] and st["docked"]): refresh()
    def _stop():
        st["shutting"] = True; HOST.dock_remove(KEY); Kit.save_min(MIN_KEY, st["minimized"])
        Kit.put_var(OPEN_KEY, "1" if st["open"] else "0"); wnd.close(); b, btn["g"] = btn["g"], None
        Kit.save_pos(BTN_KEY, b); Kit.dispose(b)
    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True}


if not VA_ALONE:
    load_modules()
    HOST.add("sysstats", "System Stats", "Ping, FPS and memory button", _module_sysstats, 0.1, category="On screen")
    HOST.run()
