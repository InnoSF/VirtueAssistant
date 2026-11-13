import API
import math
import os
import re
import struct
import time
APP_NAME = "Virtue Assistant"
APP_VERSION = "2.7.0.39"
MODULE_DIR = "VirtueAssistantModules"
SETTINGS_DIR = "VirtueAssistantSettings"
SETTINGS_KEY = "VirtueAssistant_settings"
VA_ALONE = "VA_ALONE" in globals() and "_VA_INNER" not in globals()
START_AT = (globals().get("_VA_INNER") or [time.time()])[0]
ALIVE_KEY = "VirtueAssistant_alive"
START_KEY = "VirtueAssistant_starting"
ALONE_PARTS = "VirtueAssistant_alone_parts_%s"
HOST_TICK = 0.02
UI_TICK = 0.05
UI_IDLE = 0.12
UI_IDLE_AFTER = 2.0
GRID_DEFAULT = 32
SNAP_ANCHOR = 40
KEEP_EVERY = 0.5
KEEP_SWEEP = 2.0
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
MAX_MODULE_ERRORS = 25
ERROR_SECS = 60.0
GUMP_EXPECT_MAX = 30.0
ATTACK_HUE = 0x22
HARM_SECS = 3.0
HARM_DOUBLE = 0.6
HARM_NOTO = ("innocent", "ally", "odd")
HOLD_TEXT = {"dead": "you are dead", "war": "war mode", "hurt": "you took damage", "foe": "a hostile is near",
    "item": "you are moving an item", "alarm": "an alarm needs you", "guard": "guard zone",
    "unknown": "Guard zone not known yet: cross a town's guard line once", "attacked": "you are being attacked",}
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
    def __init__(self, inner): self._inner = inner; self.made = 0
    def __getattr__(self, name):
        v = getattr(self._inner, name)
        if self.made is not None and name.startswith("Create"): v = self._counted(v)
        self.__dict__[name] = v; return v
    def _counted(self, fn):
        def run(*args, **kw):
            if self.made is not None: self.made += 1
            return fn(*args, **kw)
        return run
    def AddControlOnClick(self, ctrl, fn):
        key = HOST.click_key()
        def run(*args):
            HOST.pressed_at = time.time()
            try: fn(*args)
            finally: HOST.poke(key)
        self._inner.AddControlOnClick(ctrl, run)
    def AddGump(self, g):
        Kit.set(g, "CanCloseWithRightClick", False); Kit.set(Kit._raw_gump(g), "CanCloseWithRightClick", False)
        p = Kit._pend.get(g)
        if (p is not None and p[2] and p[3]) or g in Kit._scrolled: Kit.pin_size(g)
        r = self._inner.AddGump(g); Kit.stir()
        with Kit.quiet:
            SNAP.add(g)
            if LAYOUT.loaded: LAYOUT.fresh_adds.add(g)
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
                try: Client._client_asm = Kit._measure["asm"] = API.GetType().Assembly
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
                with Kit.quiet: m = Client._member(kb, name); bool(m[0]()); Client.keys[key] = m[0]
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
    MTQ = None; mtq_looked = False; main_call = None; main_cached = False
    @staticmethod
    def _find_mtq():
        if Client.mtq_looked: return Client.MTQ
        Client.mtq_looked = True
        try:
            import clr; clr.AddReference(API.GetType().Assembly); from ClassicUO.Game.Managers import MainThreadQueue
            Client.MTQ = Kit._measure["mtq"] = MainThreadQueue
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
        makes = (generic_of, inferred_of, with_event_of); at = Kit._measure.get("main_call"); Client.main_cached = False
        if at in (0, 1, 2):
            try: candidate = makes[at](); Client.main_cached = True; return candidate
            except Exception: Kit._measure.pop("main_call", None)
        for at, make in enumerate(makes):
            probe = {}
            def run_probe(): probe["ok"] = True
            try: candidate = make(); candidate(run_probe)
            except Exception: continue
            if probe.get("ok"): Kit._measure["main_call"] = at; return candidate
        return None
    @staticmethod
    def post(fn):
        from System import Action; Client.MTQ.EnqueueAction(Action(fn))
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
        except Exception as ex:
            Client.error = str(ex)
            if Client.main_cached:
                Client.main_call = None; Client.main_cached = False; Kit._measure.pop("main_call", None)
            return "no", None
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
    _now_memo = [-1, False]
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
    def hop(memo, fn):
        try: h = HOST; pid = h.pass_id if h.in_hop else None
        except Exception: pid = None
        if pid is not None and memo[0] == pid: return memo[1]
        v = fn()
        if pid is not None: memo[0] = pid; memo[1] = v
        return v
    @staticmethod
    def now(): return Typing.hop(Typing._now_memo, Typing._now)
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
        Typing._now_memo[0] = -1
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
    _memo = [-1, None]
    @staticmethod
    def current(): return Typing.hop(Follow._memo, Follow._current)
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
        Follow.serial = serial; Follow._memo[0] = -1; API.HeadMsg("* following *", serial, 0x44); return True
    @staticmethod
    def stop(who=APP_NAME):
        s = Follow.serial; Follow._memo[0] = -1; API.CancelAutoFollow(); Follow.serial = None
        if s: API.HeadMsg("* stopped following *", s, 0x35)
    @staticmethod
    def toggle(serial, who=APP_NAME):
        serial = int(serial or 0)
        if serial and Follow.current() == serial: Follow.stop(who); return False
        return Follow.start(serial, who)


class Kit(object):
    WINDOW_BG     = 5054; STONE_TILE    = 5058; SECTION_TILE  = 2624; SECTION_ALPHA = 0.8; FIELD_TILE    = 2624
    CORNER_ART    = 10460; ART_PLAY    = (4005, 4007, 4006); ART_CLOSE   = (4017, 4019, 4018)
    DARK_HUE = 1899; DARK_CORNER_HUE = 2305; DARK_SECTION_ALPHA = 0.95; LIGHT_SECTION_ALPHA = 0.8
    PARCH_HUE = 2960; PARCH_CORNER_HUE = 1260; PARCH_SECTION_HUE = 1845; PARCH_SECTION_ALPHA = 0.9
    CONTRAST_HUE = 1175; CONTRAST_SECTION_ALPHA = 1.0
    LOOKS = {"classic": (0, 0, 0, LIGHT_SECTION_ALPHA), "dark": (DARK_HUE, DARK_CORNER_HUE, 0, DARK_SECTION_ALPHA),
             "parchment": (PARCH_HUE, PARCH_CORNER_HUE, PARCH_SECTION_HUE, PARCH_SECTION_ALPHA),
             "contrast": (CONTRAST_HUE, CONTRAST_HUE, 0, CONTRAST_SECTION_ALPHA)}
    LOOK_ORDER = ("classic", "dark", "parchment", "contrast")
    LOOK_NAMES = {"classic": "Classic", "dark": "Dark", "parchment": "Parchment", "contrast": "High contrast"}
    TEXT_SIZES = (100, 115, 130, 150); SECTION_HUE = 0; tscale = 1.0; compact = cblind = streamer = False
    GOLD_H = 2700; GOLD_V = 2701; GOLD_T = 3
    _hues = {}; _look = "classic"; _wins = {}; _behind = set()
    ART_OK      = (4023, 4025, 4024); ART_PAGE    = (4011, 4013, 4012); ART_MIN     = (253, 252, 253)
    ART_RESTORE = (251, 250, 251); ART_DOCK    = (5602, 5606, 5602); ART_CIRCLE  = (2117, 2118, 2118)
    DOCK_DX, DOCK_DY = 20, 2; DOCK_TIP = "Fold into the Action Bar's tray"
    MIN_TIP = "Minimize (or double-click the title)"; RESTORE_TIP = "Restore"
    SETTINGS_TIP = "Open %s settings"; CLOSE_TIP = "Close %s (turns it off)"
    DOUBLE_TIP = "Double-click: minimize or restore"; LINE_RED, LINE_BLUE, LINE_POISON = 0x0805, 0x0806, 0x0808
    HUE_TITLE = 53; HUE_TEXT  = 1153; HUE_GOOD  = 68; HUE_BAD   = 33; HUE_INFO  = 946; MARGIN = 12; GAP    = 8
    _sizes = {}; _measure = {}; MEASURE_CAP = 6000
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
                gp, rp = Kit._measure.get("scale") or (None, None)
                if rp is None:
                    t = Client._type("ClassicUO.Client"); gp = t.GetProperty("Game", Client.flags(True))
                    game = gp.GetValue(None, None); rp = game.GetType().GetProperty("RenderScale", Client.flags())
                    float(rp.GetValue(game, None)); Kit._measure["scale"] = (gp, rp)
                st["fn"] = lambda: float(rp.GetValue(gp.GetValue(None, None), None))
            except Exception: st["fn"] = None
        fn = st["fn"]
        if fn is None: return 1.0
        try: s = fn(); return s if 0.25 <= s <= 4.0 else 1.0
        except Exception: Kit._measure.pop("scale", None); return 1.0
    ANCHORS = ("TL", "T", "TR", "L", "C", "R", "BL", "B", "BR"); SCREEN_KEY = "VirtueAssistant_screen"
    _pos_screen = None
    @staticmethod
    def clamp(x, y, w, h):
        W, H = Kit.screen(); x, y, w, h = int(x or 0), int(y or 0), int(w or 0), int(h or 0)
        if W > 0: x = max(0, min(x, W - w)) if w <= W else max(W - w, min(x, 0))
        if H > 0: y = max(0, min(y, H - h)) if h <= H else max(H - h, min(y, 0))
        return x, y
    _frame_parts = {}; _pend = {}; PEND_FOR = 1.0; churn = 0; churn_at = 0.0
    @staticmethod
    def stir(): Kit.churn += 1; Kit.churn_at = time.time()
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
            n = (int(x), int(y), None if w is None else int(w), None if h is None else int(h)); b = old or was
            if b[0:2] != n[0:2] or (n[2] is not None and (b[2], b[3]) != n[2:4]): Kit.stir()
            Kit._pend[g] = n + (time.time(), was)
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
        off = g in Kit._behind or int(x or 0) <= TAB_X // 2; x, y = Kit.clamp(x, y, w, h)
        if off: x = TAB_X
        g.SetRect(x, y, w, h); Kit.note_rect(g, x, y, w, h)
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
                        x, y = Kit.clamp(int(g.GetX()), int(g.GetY()), fit[0], fit[1])
                        if g in Kit._behind: x = TAB_X
                        g.SetRect(x, y, fit[0], fit[1]); Kit.moved_by_code(g)
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
            except Exception: Kit._measure["bad"] = True
            wh = Kit._sizes[graphic] = (w, h)
        return wh
    @staticmethod
    def dark(): return Kit._look in ("dark", "contrast")
    @staticmethod
    def look(): return Kit._look
    @staticmethod
    def set_look(name):
        name = name if name in Kit.LOOKS else "classic"; fh, kh, sh, sa = Kit.LOOKS[name]
        art = [(Kit.WINDOW_BG + i, fh) for i in range(9)] + [(Kit.CORNER_ART, kh), (Kit.SECTION_TILE, sh)]
        Kit._hues = dict(p for p in art if p[1]); Kit._look, Kit.SECTION_HUE, Kit.SECTION_ALPHA = name, sh, sa
    @staticmethod
    def tsize(px): return int(round(px * Kit.tscale))
    @staticmethod
    def pitch(h): return max(20, h - 4) if Kit.compact and h > 20 else h
    @staticmethod
    def look_hue(graphic, hue=0): return hue or Kit._hues.get(graphic, 0)
    @staticmethod
    def retint():
        for parts in list(Kit._frame_parts.values()):
            for p in parts:
                with Kit.quiet: p.Hue = Kit._hues.get(int(p.Graphic), 0)
    @staticmethod
    def add_pic(g, graphic, x, y, hue=0, mouse=True):
        try:
            hue = hue or Kit._hues.get(graphic, 0)
            p = G.CreateGumpPic(graphic, x, y, hue) if hue else G.CreateGumpPic(graphic, x, y); p.SetPos(x, y)
            if not mouse: p.SetAcceptMouseInput(False)
            g.Add(p); return p
        except Exception: return None
    @staticmethod
    def add_tiled(g, graphic, x, y, w, h, alpha=None, fallback="#101010", hue=0):
        if w <= 0 or h <= 0: return None
        hue = hue or Kit._hues.get(graphic, 0)
        try: t = (G.CreateTiledGumpPic(graphic, w, h, hue) if hue else G.CreateTiledGumpPic(graphic, w, h))
        except Exception: t = G.CreateGumpColorBox(alpha if alpha is not None else 1.0, fallback)
        t.SetRect(x, y, w, h)
        if alpha is not None: t.SetAlpha(alpha)
        t.SetAcceptMouseInput(False); g.Add(t); return t
    @staticmethod
    def inert(ctrl): ctrl.SetAcceptMouseInput(False); return ctrl
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
    def gold_box(g, x, y, w, h, t=GOLD_T):
        out = [Kit.add_tiled(g, Kit.SECTION_TILE, x + t, y + t, w - 2 * t, h - 2 * t)]
        for art, bx, by, bw, bh in ((Kit.GOLD_H, x, y, w, t), (Kit.GOLD_H, x, y + h - t, w, t),
                                    (Kit.GOLD_V, x, y, t, h), (Kit.GOLD_V, x + w - t, y, t, h)):
            out.append(Kit.add_tiled(g, art, bx, by, bw, bh))
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
    _frame_want = {}
    @staticmethod
    def frame_show(g, on):
        Kit._prune(Kit._frame_want, 32); Kit._frame_want[g] = bool(on)
        if g in Seam.bare or g in Seam.recs: return
        for p in Kit._frame_parts.get(g) or (): Kit.set(p, "IsVisible", bool(on))
    @staticmethod
    def frame_fit(g, w, h):
        fr = Kit._frames.get(g); s = Kit._rp_sizes.get(Kit.WINDOW_BG)
        if fr is None or s is None or g in Kit._scrolled: return False
        tl, t, tr, l, _, r, bl, b, br = s
        cw, ch = Kit.pic_size(Kit.CORNER_ART) if fr["corners"] and Kit.CORNER_ART else (0, 0)
        rects = [(l[0], t[1], w - l[0] - r[0], h - t[1] - b[1]), (tl[0], 0, w - tl[0] - tr[0], t[1]),
                 (bl[0], h - b[1], w - bl[0] - br[0], b[1]), (0, tl[1], l[0], h - tl[1] - bl[1]),
                 (w - r[0], tr[1], r[0], h - tr[1] - br[1]), (0, 0), (w - tr[0], 0), (0, h - bl[1]),
                 (w - br[0], h - br[1])]
        if cw and ch: rects += [(0, 0), (w - cw, 0), (0, h - ch), (w - cw, h - ch)]
        if len(fr["pieces"]) != len(rects): return False
        for p, rect in zip(fr["pieces"], rects):
            if len(rect) == 4: p.SetRect(*rect)
            else: p.SetPos(*rect)
        return True
    @staticmethod
    def add_window_frame(g, w, h, corners=True, mouse=True):
        pieces = Kit._frame_pieces(g, w, h, corners, mouse)
        if type(g) is not PageCanvas:
            Kit._prune(Kit._frames, 32)
            if len(Kit._frames) > 256: Kit._frames.clear()
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
        key = HOST.click_key(); swallow = type(ctrl).__name__ != "ApiUiButton"
        def handler(*args):
            Kit.clicks_seen = True; twice = swallow and Client.second_click_swallowed()
            try: fn()
            finally:
                try:
                    if twice: fn()
                finally: HOST.poke(key)
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
    TWICE = 0.15
    @staticmethod
    def once(fn, key, gap=0.6):
        def run():
            now = time.time()
            if now - Kit._fired.get(key, 0.0) < gap: return
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
                        if event == "MouseDoubleClick": e.Result = True
                        HOST.pressed_at = time.time(); HOST.poke()
                except Exception: pass
            add.Invoke(ctrl, System.Array[object]([delegate_type(handler)])); return True
        except Exception: return False
    hook_double = hook_mouse; _dbl_events = {}
    @staticmethod
    def on_moved(g, fn): SNAP.on_moved(g, fn)
    @staticmethod
    def moved_by_code(g): SNAP.moved_by_code(g); Kit.stir()
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
        click = Binds.wrap(bid, clicked); Kit.on_click(b, click); combo = Binds.saved.get(bid); va = "va|%s" % (key,)
        if not combo and Binds.last_va.get(key) == bid and Binds.old(va): combo = Binds.saved.get(va)
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
    _hooks = {}
    @staticmethod
    def hook_once(holder, key, *pairs, owner=False):
        if holder[key]: return
        holder[key] = True; owner = HOST.owner_key() if owner is False else owner
        for event, fn in pairs:
            try: getattr(API.Events, event if event.startswith("On") else "On" + event)(fn)
            except Exception: continue
            Kit._hooks.setdefault(owner, []).append((event, fn, holder, key))
    @staticmethod
    def unhook(owner):
        recs = Kit._hooks.pop(owner, None)
        if not recs: return
        def run():
            for rec in recs:
                event, fn, holder, key = rec
                try: getattr(API.Events, "Unregister" + (event if event.startswith("On") else "On" + event))(fn)
                except Exception: Kit._hooks.setdefault(owner, []).append(rec); continue
                holder[key] = False
        with Kit.quiet: Kit.on_client(run)
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
        if not Client.on_client_thread() and (Client.MTQ if Client.mtq_looked else Client._find_mtq()) is not None:
            Kit._texts_cap = len(Kit._texts) + 500; Kit._texts_sweep = True; return
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
            except Exception: Kit._measure["bad"] = True
            px = px or 8 * len(text)
            if len(Kit._widths) >= Kit.WIDTHS_MAX:
                wd = Kit._widths
                for k in [k for k in wd if len(k) > 12]: del wd[k]
                if len(wd) >= Kit.WIDTHS_MAX // 2: wd.clear()
            Kit._widths[text] = px
        return px
    _wraps = {}
    @staticmethod
    def wrap(text, width):
        ck = (text, width); got = Kit._wraps.get(ck)
        if got is None:
            if len(Kit._wraps) > 600: Kit._wraps.clear()
            got = Kit._wraps[ck] = tuple(Kit._wrap_raw(text, width))
        return list(got)
    @staticmethod
    def _wrap_raw(text, width):
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
            except Exception: px["ok"] = False; Kit._measure["bad"] = True
        if not px["ok"]: return Kit.text_w(text)
        w, cw = px["pad"], Kit._px_ch
        for ch in text: x = cw.get(ch); w += Kit._ch_w(ch) if x is None else x
        return w
    @staticmethod
    def measure_bind():
        import sys; key = (APP_VERSION, os.getpid()); st = sys.__dict__.get("_VA_MEASURE")
        e = st.get(key) if type(st) is dict else None
        if type(e) is not dict or e.get("bad") is not False: e = {"bad": False}; sys._VA_MEASURE = {key: e}
        for cls, name in ((Kit, "_widths"), (Kit, "_px_ch"), (Kit, "_px"), (Kit, "_sizes"), (Kit, "_rp_sizes"),
                          (Kit, "_ctl_prop"), (Client, "_types"), (Typing, "_members"), (Tz, "_types"), (Tz, "_found"),
                          (Tex, "parts")):
            k = cls.__name__ + "." + name; d = e.get(k)
            if type(d) is not dict or len(d) > Kit.MEASURE_CAP: d = e[k] = cls.__dict__[name]
            setattr(cls, name, d)
        if e.get("asm") is not None: Client._client_asm = e["asm"]
        if e.get("mtq") is not None: Client.MTQ, Client.mtq_looked = e["mtq"], True
        Tex.ok = True if Tex.parts.get("ok") is True else None; Kit._measure = e
    @staticmethod
    def fit(text, width, tail=".."):
        text = str(text or "")
        if not text or (len(text) * 12 <= width and max(text) <= "\u024f") or Kit.text_px(text) <= width: return text
        if Kit._px["ok"]:
            w, cw = Kit.text_px(text + tail), Kit._px_ch
            while text and w > width: w -= cw.get(text[-1], 0); text = text[:-1]
        else:
            lo, hi = 1, len(text) - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if Kit.text_w(text[:mid] + tail) <= width: lo = mid
                else: hi = mid - 1
            text = text[:lo]
        if text and "\ud800" <= text[-1] <= "\udbff": text = text[:-1]
        return text.rstrip() + tail
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
            if ctrl in SNAP.members: Kit.stir()
            try: ctrl.Dispose()
            except Exception: pass
    @staticmethod
    def is_open(g):
        if g is None: return False
        try: return not g.IsDisposed
        except Exception: return False
    _vars = {}
    @staticmethod
    def get_var(key, default=""):
        v = Kit._vars.get(key)
        if v is None:
            try: v = str(API.GetPersistentVar(key, "", API.PersistentVar.Char) or "")
            except Exception: return str(default)
            if len(Kit._vars) > 3000: Kit._vars.clear()
            Kit._vars[key] = v
        return v or str(default)
    @staticmethod
    def put_var(key, value, loud=False):
        v = str(value)
        if Kit._vars.get(key) == v: return
        Kit._vars.pop(key, None)
        if loud: API.SavePersistentVar(key, value, API.PersistentVar.Char)
        else:
            with Kit.quiet: API.SavePersistentVar(key, value, API.PersistentVar.Char); Kit._vars[key] = v
            return
        Kit._vars[key] = v
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
    def write_safe(path, text, enc="utf-8", tail=None):
        try: import _thread; tmp = "%s.%d.%d.tmp" % (path, os.getpid(), _thread.get_ident())
        except Exception: tmp = "%s.%d.tmp" % (path, id(text))
        import io
        try:
            if isinstance(text, bytes):
                with io.open(tmp, "wb") as f: f.write(text)
            else:
                with io.open(tmp, "w", encoding=enc, newline="", errors="replace") as f: f.write(text)
            more = tail() if tail is not None else None
            if more:
                with io.open(tmp, "ab") as f: f.write(more)
        except Exception:
            safe(lambda: os.remove(tmp)); raise
        done = False
        for _ in range(3):
            try: os.replace(tmp, path); done = True; break
            except Exception: pass
        if not done:
            bak = tmp + ".bak"; had = os.path.exists(path)
            try:
                if had: os.rename(path, bak)
                os.rename(tmp, path)
            except Exception:
                if had and os.path.exists(bak):
                    if os.path.exists(path): safe(lambda: os.remove(bak))
                    else: safe(lambda: os.rename(bak, path))
                safe(lambda: os.remove(tmp)); raise
            if had: safe(lambda: os.remove(bak))
        if text: Kit._seen.add(os.path.normcase(os.path.abspath(path)))
        return True
    _seen = set(); _gone = {}; MISS_WAIT = 5.0
    @staticmethod
    def read_merge(path):
        key = os.path.normcase(os.path.abspath(path))
        if not os.path.exists(path):
            d, pre = os.path.split(key); baks = []
            try:
                baks = [n for n in os.listdir(d) if os.path.normcase(n).startswith(pre + ".")
                        and os.path.normcase(n).endswith(".tmp.bak")]
            except Exception: pass
            if not os.path.exists(path):
                if key not in Kit._seen and not baks: Kit._gone.pop(key, None); return ""
                now = time.time(); t = Kit._gone.setdefault(key, now)
                if now - t < Kit.MISS_WAIT: return None
                if baks:
                    try:
                        bak = os.path.join(d, max(baks, key=lambda n: os.path.getmtime(os.path.join(d, n))))
                        os.rename(bak[:-4] if os.path.exists(bak[:-4]) else bak, path)
                    except Exception: pass
                    if os.path.exists(path):
                        for x in [os.path.join(d, n)[:cut] for n in baks for cut in (None, -4)]:
                            if os.path.exists(x):
                                with Kit.quiet: os.remove(x)
                if not os.path.exists(path): Kit._seen.discard(key); return ""
        Kit._gone.pop(key, None); text = Kit.read_safe(path)
        if text: Kit._seen.add(key)
        return text
    @staticmethod
    def read_safe(path, missing=""):
        try:
            if not os.path.exists(path): return missing
            import io
            with io.open(path, "rb") as f: raw = f.read()
            if raw[:2] in (b"\xff\xfe", b"\xfe\xff"): text = raw.decode("utf-16")
            else:
                try: text = raw.decode("utf-8-sig")
                except UnicodeError:
                    out = []
                    for ln in (raw[3:] if raw[:3] == b"\xef\xbb\xbf" else raw).split(b"\n"):
                        try: out.append(ln.decode("utf-8"))
                        except UnicodeError:
                            try: out.append(ln.decode("mbcs"))
                            except (UnicodeError, LookupError): out.append(ln.decode("latin-1"))
                    text = "\n".join(out)
            return text.replace("\r\n", "\n").replace("\r", "\n")
        except Exception: return None
    @staticmethod
    def merge_text(text, entries, key_of, sep="\n"):
        out, at = [], {}
        for e in (text or "").split(sep):
            e = e.rstrip("\r")
            if not e.strip(): continue
            k = key_of(e)
            if k is not None and k in at: out[at[k]] = e; continue
            if k is not None: at[k] = len(out)
            out.append(e)
        for k, e in entries.items():
            if k in at: out[at[k]] = e
            elif e is not None: at[k] = len(out); out.append(e)
        out = [e for e in out if e is not None]; return sep.join(out), out
    @staticmethod
    def merge_save(path, entries, key_of, sep="\n"):
        text = Kit.read_merge(path)
        if text is None: return None
        merged, out = Kit.merge_text(text, entries, key_of, sep)
        Kit.write_safe(path, merged + sep if out else ""); return out
    @staticmethod
    def data_setup():
        safe(Kit.measure_bind); base, d = Kit.script_dir(), Kit.data_dir()
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
        if Kit.is_open(g) and g not in LAYOUT.held and g.GetX() > TAB_X // 2:
            Kit.put_var(key, "%d,%d" % (g.GetX(), g.GetY()))
    @staticmethod
    def queuer(st):
        def add(action, dup=False, front=False, cap=None, key=None):
            q = st["queue"]
            if not dup and action in q or cap is not None and len(q) >= cap: return False
            if front: q.insert(0, action)
            else: q.append(action)
            if key is not None and (HOST.draining or not HOST.in_hop): HOST.poke(key)
            return True
        def queue(action, dup=False):
            key = HOST.click_key()
            def handler(*args): add(action, dup, key=key)
            return handler
        queue.add = add; return queue
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
    def dock_hooks(title, icon, st, win, redraw, fit=None):
        def state():
            if win["g"] is None or st["shutting"]: return None
            return "docked" if st["docked"] else ("minimized" if st["minimized"] else "open")
        def to(docked, minimized):
            def f(): st["docked"], st["minimized"] = docked, minimized; redraw()
            return f
        def undock(): st["docked"] = False; redraw()
        hooks = {"title": title, "icon": icon, "state": state, "show": to(False, False), "dock": to(True, True),
                 "undock": undock, "minimize": to(False, True), "gump": lambda: win["g"], "redraw": redraw}
        if fit is not None: hooks["fit"] = fit
        return hooks
    @staticmethod
    def add_front(g, hidden=False):
        Kit.flush()
        if hidden: g.IsVisible = False
        return G.AddGump(g)
    _stack = {"off": False}
    @staticmethod
    def replace_gump(old, g, hidden=False):
        r = Kit.add_front(g, hidden); st = Kit._stack
        if Kit.is_open(old): SNAP.swap(old, g)
        if st["off"] or Host.ORDER_OFF in HOST.tz_off or not Kit.is_open(old) or not Client.on_client_thread(): return r
        try:
            ro, rn = Kit._raw_gump(old), Kit._raw_gump(g)
            if ro is None or rn is None: return r
            uim = Tz.T("ClassicUO.Game.Managers.UIManager"); gumps = Tz.get(None, "Gumps", uim); same = Kit._same()
        except Exception: st["off"] = True; return r
        try:
            node, new, at, n = gumps.First, None, None, 0
            while node is not None and n < 2000 and (new is None or at is None):
                v = node.Value
                if new is None and same(v, rn): new = node
                elif at is None and same(v, ro): at = node
                node = node.Next; n += 1
            if new is None or at is None or (new.Next is not None and same(new.Next.Value, ro)): return r
            gumps.Remove(new)
            try: gumps.AddBefore(at, new)
            except Exception: gumps.AddFirst(new)
            Tz.put(None, "_gumpsStructureVersion", int(Tz.get(None, "_gumpsStructureVersion", uim)) + 1, uim)
            Tz.put(None, "TopMostControl", gumps.First.Value, uim)
        except Exception: pass
        return r
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
    def walk(g, fn, root=None):
        root = Kit.client_control(g) if root is None else root
        if root is None: return False
        def tree(c):
            if fn(c) is False: return
            kids = c.Children
            for i in range(kids.Count): tree(kids[i])
        try:
            kids = root.Children
            for i in range(kids.Count): tree(kids[i])
            return True
        except Exception: return False
    @staticmethod
    def scale_window(g, scale):
        if abs(scale - 1.0) < 0.001: return True
        root = Kit.client_control(g)
        if root is None or not Kit.flush(): return False
        skip, area = Kit._scroll_skip(g); same = Kit._same()
        def one(c):
            if skip and any(same(c, k) for k in skip): return False
            if area is None or not same(c, area):
                if str(c.GetType().Name) == "GumpPicTiled": Kit.set(c, "ScaleTiledTexture", True)
                c.ApplyScale(scale, True, True, False)
        return Kit.walk(g, one, root)
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
    def top_of(serial):
        s = int(serial or 0)
        for _ in range(10):
            it = Kit.find_item(s)
            if it is None: return s, 0
            try: c = int(it.Container or 0)
            except Exception: c = 0
            if not c or c == 0xFFFFFFFF: return s, 0
            if c < 0x40000000: return s, c
            s = c
        return s, 0
    @staticmethod
    def in_pack(serial):
        pack = int(API.Backpack or 0); return bool(pack) and bool(serial) and Kit.top_of(serial)[0] == pack
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
    B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    B64_REV = dict((ch, i) for i, ch in enumerate(B64))
    @staticmethod
    def b64(data):
        out = []; B64 = Kit.B64
        for i in range(0, len(data), 3):
            n = (data[i] << 16) | (data[i + 1] << 8) | data[i + 2]
            out += [B64[(n >> 18) & 63], B64[(n >> 12) & 63], B64[(n >> 6) & 63], B64[n & 63]]
        return "".join(out)
    @staticmethod
    def unb64(s):
        data = []; B64_REV = Kit.B64_REV
        for i in range(0, len(s), 4):
            n = 0
            for ch in s[i:i + 4]: n = (n << 6) | B64_REV[ch]
            data += [(n >> 16) & 255, (n >> 8) & 255, n & 255]
        return data
    @staticmethod
    def checksum(data):
        s = 7
        for i, b in enumerate(data): s = (s * 31 + b + i) & 0xFFFF
        return s
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
    def basics(st, title): return Kit.Cleanup(), Kit.queuer(st), Kit.sayer(title)
    @staticmethod
    def dd_index(dd, default):
        try: return int(dd.GetSelectedIndex())
        except Exception: return default
    @staticmethod
    def drop_arrow(st, arrow_id):
        if st["arrow"] is not None: st["arrow"] = None; API.TrackingArrow(-1, -1, arrow_id)
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
    def show_window(g, x, y, w, h, lock_key, hidden, on_disposed, moved, into=None, parts=None, max_h=None, old=None):
        xy = Kit.place(g, x, y, w, h, None, max_h)
        if lock_key is not None: HOST.built(lock_key)
        if lock_key is not None and HOST.layout_locked(lock_key): g.CanMove = False
        if into is not None: into.update(parts)
        if on_disposed is not None: G.AddControlOnDisposed(g, on_disposed)
        Kit.replace_gump(old, g, hidden)
        if moved is not None: Kit.on_moved(g, moved)
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
        COMPACT = {"ch": 22, "fh": 24, "bh": 26, "top": 28, "pad": 6}
        FIELDS = ("num", "text", "slider"); sink = mark = fresh = page = None; BOX_W = 20; FOUND = "<- found"
        NEW = "new"
        def __init__(self, g, x, y, w, vals, page=(), store=None, **opts):
            self.g, self.x, self.y, self.w, self.vals, self.opts = g, x, y, w, vals, opts
            self.top, self.c, self.store, self.specs = y, {}, store or ({}, {}), []
            for sec in page: self.section(*sec)
        @property
        def h(self): return max(0, self.y - self.top - Kit.GAP)
        @staticmethod
        def height(page, w=0, **opts): return Kit.Form(None, 0, 0, w, {}, page, **opts).h
        def _o(self, sec, r=None):
            o = dict(Kit.Form.OPTS)
            if Kit.compact: o.update(Kit.Form.COMPACT)
            o.update(self.opts); o.update(sec)
            if r and type(r[-1]) is dict: o.update(r[-1])
            return o
        @staticmethod
        def _step(r, o):
            if o.get("stay"): return 0
            if r[0] in ("gap", "custom"): return r[1]
            return o["h"] if "h" in o else o[Kit.Form.STEP[r[0]]]
        def section(self, title, rows, sec=None):
            if Kit.Form.sink is not None: Kit.Form.sink.append((HOST.cur_part, title, rows))
            sec = sec or {}; so, opts = self._o(sec), [self._o(sec, r) for r in rows]
            sh = sec.get("sh") or so["top"] + sum(Kit.Form._step(r, o) for r, o in zip(rows, opts)) + so["pad"]
            x, ry, g = self.x, self.y + so["top"], self.g
            if g is not None: Kit.add_section(g, x, self.y, self.w, sh, title)
            self.y += sh + Kit.GAP
            if g is None: return
            lw = max([Kit.text_w(r[2]) for r in rows if r[0] in Kit.Form.FIELDS] or [0])
            for r, o in zip(rows, opts):
                self._row(g, r, o, x, ry, o.get("lw", lw if o.get("align") else None)); ry += Kit.Form._step(r, o)
        @staticmethod
        def _tag(r):
            F = Kit.Form
            if F.page is None or r[0] in ("gap", "custom"): return None
            pk = HOST.cur_part; keys = [b[0] for b in r[1]] if r[0] == "buttons" else [r[1]]
            if F.mark is not None and F.mark[0] == pk and F.mark[1] in keys: return F.FOUND
            pre = F.page + "." + (pk + "." if pk else "")
            if r[0] != "note" and F.fresh and any(pre + str(k) in F.fresh for k in keys): return F.NEW
            return None
        def _row(self, g, r, o, sx, y, lw):
            kind, c, x = r[0], self.c, sx + o["dx"]; k = r[1] if kind in Kit.Form.FIELDS or kind == "check" else None
            tag = Kit.Form._tag(r); end = None
            if kind == "check":
                c[k] = Kit.add_check(g, r[2], x, y, self.vals[k], r[3]); self.specs.append((r, o))
                end = x + Kit.Form.BOX_W + (Kit.text_w(r[2]) if tag else 0)
            elif kind == "note":
                lbl = Kit.add_label(g, r[1], x, y + o["ndy"], o.get("hue", Kit.HUE_INFO))
                if o.get("key"): c[o["key"]] = lbl
                end = x + (Kit.text_w(r[1]) if tag else 0)
            elif kind == "buttons":
                end = Kit.buttons(g, self.store, x, y + o["bdy"], [b[:5] for b in r[1]], o["bgap"]) - o["bgap"]
            elif kind == "custom": r[2](self, sx, y)
            elif kind in Kit.Form.FIELDS:
                lbl = Kit.add_label(g, r[2], x, y + o["ldy"])
                fx = x + (Kit.text_w(r[2]) if lw is None else lw) + o["lgap"]; tip = r[3]
                if kind == "num":
                    if tip and not tip.endswith(")"): tip += " (%d-%d)" % (r[5], r[6])
                    c[k] = Kit.add_textbox(g, o["fmt"] % self.vals[k], fx, y, o["fw"]); end = fx + o["fw"]
                    if r[4]:
                        Kit.add_label(g, r[4], fx + o["fw"] + o["ugap"], y + o["ldy"], Kit.HUE_INFO)
                        end += o["ugap"] + (Kit.text_w(r[4]) if tag else 0)
                elif kind == "text":
                    tw = (o.get("tw") or self.w - (fx - sx) - 16) - (Kit.text_w(tag) + 6 if tag else 0)
                    c[k] = Kit.add_textbox(g, self.vals[k], fx, y, tw, numbers=False); end = fx + tw
                else:
                    c[k] = Kit.add_slider(g, fx, y + o["sdy"], o["sw"], r[4], r[5], self.vals[k]); end = fx + o["sw"]
                    if o.get("vfmt") or o.get("unit"):
                        f = o.get("vfmt"); v = self.vals[k]
                        lt = (f(v) if callable(f) else f % v) if f else o["unit"]
                        c[k + "_lbl"] = Kit.add_label(g, lt, fx + o["sw"] + o["ugap"], y + o["ldy"], Kit.HUE_INFO)
                        end += o["ugap"] + (Kit.text_w(lt) if tag else 0)
                Kit.with_tip(c[k], tip)
                if o.get("ltip"): Kit.with_tip(lbl, tip)
                self.specs.append((r, o))
            if tag and end is not None:
                dy = {"check": 2, "note": o["ndy"], "buttons": o["bdy"] + 3}.get(kind, o["ldy"])
                Kit.add_label(g, tag, min(end + 6, sx + self.w - 4 - Kit.text_w(tag)), y + dy, Kit.HUE_TITLE)
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
                out[k] = v; f = o.get("vfmt") if kind == "slider" else None
                if f: Kit.set_text(self.c[k + "_lbl"], f(v) if callable(f) else f % v)
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
        @staticmethod
        def drop(name, fn):
            if HOST.services.get(name) is fn: HOST.services.pop(name, None)
        def close(self):
            jobs = self.jobs
            while jobs:
                fn, args = jobs.pop()
                with Kit.quiet: fn(*args)
    class Window(object):
        def __init__(self, key, title, st, win, build, pos_key, min_key=None, default=(200, 200), mini=None,
                     icon=None, cleanup=None, gkey="g", names=("c", "store"), lock=True, owner=True, close_tip=None,
                     clear=None, docked_min=False):
            self.key, self.title, self.st, self.win, self.build, self.pos_key = key, title, st, win, build, pos_key
            self.min_key, self.default, self.mini, self.icon, self.cleanup = min_key, default, mini, icon, cleanup
            self.gkey, self.names, self.lock, self.owner, self.close_tip = gkey, names, lock, owner, close_tip
            self.clear, self.docked_min, self.slot, self.held, self.old = clear or {}, docked_min, None, False, None
            self.queue = Kit.queuer(st) if st is not None else None; self.x = self.y = self.w = self.h = 0
            self.c, self.store, self.fade = {}, ({}, {}), True
        def minimized(self): return self.st is not None and bool(self.st["minimized"])
        def start_min(self): return bool(HOST.dock_wanted(self.key) or (self.min_key and Kit.load_min(self.min_key)))
        def begin(self, w, h, default=None, resize=None):
            if self.queue is not None: Kit._wins[self.key] = self
            if Kit.is_open(self.old) and self.old is not self.win.get(self.gkey): Kit.dispose(self.old)
            old = self.win.get(self.gkey); mini = self.minimized()
            if mini and self.mini: w, h = self.mini
            self.w, self.h = w, h
            p = None if Kit.is_open(old) or mini or not self.lock or not LAYOUT.planned else LAYOUT.plan_at(self.key)
            if Kit.is_open(old): self.x, self.y = old.GetX(), old.GetY()
            elif p is not None: self.x, self.y = int(p[0]), int(p[1])
            else: self.x, self.y = Kit.load_pos(self.pos_key, default or self.default, (w, h))
            self.old, self.win[self.gkey] = old, None
            if self.cleanup is not None and not self.held: self.held = True; self.cleanup.add(self.release)
            if resize is not None and not mini:
                self.x, self.y = Kit.clamp(self.x, self.y, w, h)
                g = G.CreateModernGump(self.x, self.y, w, h, True, resize[0], resize[1], resize[2]); g.SetAlpha(0)
            else: g = G.CreateGump(True, True)
            self.c, self.store = {}, ({}, {})
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
            if not self.lock: HOST.built(self.key)
            if st is not None and st.get("minimized") and st.get("docked") is False and HOST.dock_soon(self.key):
                st["docked"] = True
            for name, v in zip(self.names or (), (self.c, self.store)): parts[name] = v
            xy = Kit.show_window(g, self.x, self.y, self.w if w is None else w, self.h if h is None else h,
                                 self.key if self.lock else None, st is not None and st["minimized"] and st["docked"],
                                 self.disposed(g), self.save_pos, self.win, parts, max_h, self.old)
            slot = LAYOUT.spot(self.key) if self.lock and LAYOUT.seamless and LAYOUT.holds(self.key) else None
            if slot is not None and xy is not None and (xy[0], xy[1]) != (slot[0], slot[1]):
                g.SetPos(int(slot[0]), int(slot[1])); Kit.note_rect(g, slot[0], slot[1]); Kit.moved_by_code(g)
                xy = (slot[0], slot[1])
            if slot is not None and xy is not None: LAYOUT._hold(g, self.key); LAYOUT.fit_now(self.key, g)
            if FADE.on: FADE.wake(self.key)
            old, self.old = self.old, None; Kit.dispose(old); return xy
        def disposed(self, g):
            def handler(*args):
                win = self.win
                if win.get(self.gkey) is not g or (self.owner and self.st["shutting"]): return
                win[self.gkey] = None; win.update(self.clear)
                if self.owner: HOST.disable(self.key)
            return handler
        def save_pos(self):
            if not (self.lock and HOST.layout_holds(self.key)): Kit.save_pos(self.pos_key, self.win.get(self.gkey))
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
            if new != self._slot or (mode == "again" and new is not None): self.slot = new; self.queue("redraw")()
        @property
        def slot(self):
            s = self._slot
            if s is None and LAYOUT.planned and not self.told and self.st is not None and not self.st["minimized"]:
                p = LAYOUT.plan_at(self.key)
                if p is not None: s = self._slot = (int(p[2]), int(p[3])); self.told = True
            return s
        @slot.setter
        def slot(self, v): self._slot = v; self.told = v is not None or self.__dict__.get("told", False)
        def zone_slot(self, mw, mh):
            z = self.slot if Kit.zone_up(self.key) and not self.st["minimized"] else None
            return z if z is not None and z[0] >= mw and z[1] >= mh else None
        def rows(self, row_h, fixed_h, own_n, min_n=1):
            if self.slot is None or not HOST.layout_holds(self.key): return own_n
            return max(min_n, int(self.slot[1] - fixed_h) // max(1, int(row_h)))
        def dock(self, fit=False, **extra):
            hooks = Kit.dock_hooks(self.title, self.icon, self.st, self.win, self.queue("redraw"),
                                   self.fit if fit is True else (fit or None))
            hooks.update(extra); HOST.dock_add(self.key, hooks)
            if self.cleanup is not None: self.cleanup.add(HOST.dock_remove, self.key)
            return hooks
    class _Quiet(object):
        def __enter__(self): return self
        def __exit__(self, kind, value, tb): return kind is not None and issubclass(kind, Exception)
    quiet = _Quiet(); _notos = {}
    NOTO_ORDER = ("unknown", "innocent", "ally", "gray", "criminal", "enemy", "murderer", "invulnerable")
    CB_RGB = {"innocent": (0, 114, 178), "ally": (86, 180, 233), "gray": (153, 153, 153), "criminal": (153, 153, 153),
              "enemy": (230, 159, 0), "murderer": (213, 94, 0), "invulnerable": (240, 228, 66)}
    CB_HUE = {"innocent": 1266, "ally": 1060, "gray": 2958, "criminal": 2958, "enemy": 1174, "murderer": 1100,
              "invulnerable": 1568}
    NOTO_MARKS = {"murderer": "R", "criminal": "C", "gray": "C", "enemy": "O", "ally": "A", "invulnerable": "I"}
    VEILS = {"me": "You", "guild": "(hidden)", "xy": "(hidden)", "place": "(hidden)"}
    B36 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
    def _noto_key(noto):
        if type(noto) is int: return Kit.NOTO_ORDER[noto] if 0 <= noto < len(Kit.NOTO_ORDER) else "unknown"
        return noto if isinstance(noto, str) else Kit.noto_of(noto)
    @staticmethod
    def cb_rgb(noto, default=None): return Kit.CB_RGB.get(Kit._noto_key(noto), default) if Kit.cblind else default
    @staticmethod
    def cb_hex(noto, default=None):
        c = Kit.cb_rgb(noto); return default if c is None else "#%02X%02X%02X" % c
    @staticmethod
    def cb_hue(noto, default=0): return Kit.CB_HUE.get(Kit._noto_key(noto), default) if Kit.cblind else default
    @staticmethod
    def noto_mark(noto): return Kit.NOTO_MARKS.get(Kit._noto_key(noto), "") if Kit.cblind else ""
    @staticmethod
    def hp_mark(poisoned=False, paralysed=False, mortal=False):
        if not Kit.cblind: return ""
        return ("P" if poisoned else "") + ("Z" if paralysed else "") + ("M" if mortal else "")
    @staticmethod
    def veil(kind, text, serial=0):
        if not Kit.streamer: return text
        if kind != "name": return Kit.VEILS.get(kind, "(hidden)")
        try: s = int(serial or 0)
        except (TypeError, ValueError): s = 0
        if s <= 0: return "Player"
        d = ""
        for _ in range(3):
            d = Kit.B36[s % 36] + d; s //= 36
            if not s: break
        return "Player " + d
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
            if h0 >= Fill.MIN_EDGE and (h0 > Fill.ROW_H or rec["rows"]) and not Fill.title_strip(e[2], e[4]):
                y0, y1 = ev(fy, y), ev(fy, y + h)
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
        with Kit.quiet:
            import clr; t = clr.GetClrType(type(g))
            while t is not None:
                if str(t.Name) == "ApiUiBaseControl": Fill._api_t[0] = t; return True
                t = t.BaseType
        return False
    @staticmethod
    def _scan(rec, kids, skip, k_now=1.0):
        ents = rec["ent"]; same = Kit._same(); new = []
        for c in kids:
            try:
                if c.IsDisposed or c in ents or c in Seam.catchers: continue
            except Exception: continue
            if skip and any(same(c, s) for s in skip): continue
            r = Kit._raw_rect(c)
            if r is None: continue
            tn = str(c.GetType().Name); kind = "s" if tn in Fill.STRETCH else "p"
            if tn == "GumpPic":
                with Kit.quiet:
                    if int(c.Graphic) in (Kit.LINE_RED, Kit.LINE_BLUE, Kit.LINE_POISON): kind = "s"
            if kind == "s" and tn == "AlphaBlendControl" and r[2] < Fill.MIN_BG:
                with Kit.quiet:
                    if float(c.Alpha) < 0.05: kind = "p"
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
            with Kit.quiet: stack.extend(Kit._children(d))
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
    def title_strip(y, h): return y <= Kit.MARGIN + 2 and h <= 31
    @staticmethod
    def _maps(rec):
        nw, nh = rec["nat"]; N, Hn = rec["size"]; k = rec.get("k", 1.0); M = Kit.MARGIN * k; bgs = Fill._bgs(rec)
        tall = [b for b in bgs if b[3] > Fill.ROW_H]; rec["rows"] = not tall
        rec["fx"] = Fill._axis(nw * k, N, M, [(b[0] * k, (b[0] + b[2]) * k) for b in bgs], rec["mode"])
        rec["fy"] = Fill._axis(nh * k, Hn, M, [(b[1] * k, (b[1] + b[3]) * k) for b in (tall or bgs)
                                               if not Fill.title_strip(b[1], b[3])], rec["mode"])
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
        if r is not None and (r[0], r[1], r[2], r[3]) == (TAB_X if g in Kit._behind else x, y, W, H) and not new \
                and rec["placed"] is not None:
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
    LOG_KEY = "VirtueAssistant_alert_log"; LOG_CAP = 50; LOG_EVERY = 60.0; LOG_CUT = 160; QUIET_MAX = 1440
    QUIET_ALARM = 30.0
    def __init__(self):
        self.kinds = {}; self.order = []; self.choice = {}; self.banner_on = True
        self.mute = self.loaded = self.busy = self.shown = self.alarm = self.flash_on = self.clicked = False
        self.last = {}; self.pending = []; self.sounds = []; self.pings = []
        self.sound_at = self.hide_at = self.flash_at = self.moved_at = 0.0; self.g = self.pos = None; self.c = {}
        self.count = 0; self.hue = Kit.HUE_TITLE; self.line = ""; self.tw = self.W - 36; self.scale = 1.0
        self.log = []; self.log_ver = 0; self.log_due = False; self.log_at = 0.0; self.quiet_until = 0
        self.bw = 30; self.store = ({}, {}); self.alarm_until = 0.0; self.line_who = ("", 0); self.items = []
        self.hold = {}
    def load(self):
        self.loaded = True; self.choice = {}; self.mute, self.banner_on = False, True; self.quiet_until = 0
        for k, v in Kit.codec_load(Kit.get_var(self.KEY)).items():
            if k == "mute": self.mute = v == "1"
            elif k == "banner": self.banner_on = v != "0"
            elif k == "quiet":
                try: self.quiet_until = int(v)
                except ValueError: self.quiet_until = 0
            elif k.startswith("kind."):
                bits = v.split(",")
                try: snd = int(bits[1]) if len(bits) > 1 and bits[1] != "" else None
                except ValueError: snd = None
                self.choice[k[5:]] = [bits[0] != "0", snd]
        log = []
        for ln in Kit.get_var(self.LOG_KEY).split("\n"):
            b = ln.split("~", 5)
            if len(b) < 4: continue
            try: t, ser = float(b[0]), int(b[5]) if len(b) > 5 and b[5] else 0
            except ValueError: continue
            log.append((t, b[1], b[3], "", b[2] == "q", b[4] if len(b) > 4 else "", ser))
        self.log = log[-self.LOG_CAP:]; self.log_ver += 1; self.log_due = False
    def save(self):
        parts = ["mute=%d" % (1 if self.mute else 0), "banner=%d" % (1 if self.banner_on else 0)]
        for k in sorted(self.choice):
            on, snd = self.choice[k]
            parts.append("kind.%s=%d,%s" % (k, 1 if on else 0, "" if snd is None else int(snd)))
        parts.append("quiet=%d" % int(self.quiet_until)); Kit.put_var(self.KEY, ";".join(parts))
    @staticmethod
    def _clip(s, n): return re.sub(r"[~\r\n]", " ", str(s))[:n]
    @staticmethod
    def veiled(line, name, serial=0):
        if not Kit.streamer or not name or name not in line: return line
        v = Kit.veil("name", name, serial); return re.sub(r"(?<!\w)%s(?!\w)" % re.escape(name), lambda m: v, line)
    @staticmethod
    def with_quiet(text, mine):
        keep = [p for p in str(text or "").split(";") if p.strip() and not p.strip().startswith("quiet=")]
        return ";".join(keep + [p for p in str(mine or "").split(";") if p.strip().startswith("quiet=")][-1:])
    def shown_line(self): return Alerts.veiled(self.line, *self.line_who)
    def save_log(self, now):
        self.log_due = False; self.log_at = now + self.LOG_EVERY; c = Alerts._clip
        rows = ("%d~%s~%s~%s~%s~%d" % (int(t), c(lv, 8), "q" if q else "", c(line, self.LOG_CUT), c(who, 40), ser)
                for t, lv, line, _k, q, who, ser in list(self.log))
        Kit.put_var(self.LOG_KEY, "\n".join(rows))
    def quiet_on(self, now=None):
        if not self.loaded: self.load()
        left = self.quiet_until - (time.time() if now is None else now); return 0 < left <= 60 * self.QUIET_MAX
    def quiet(self, minutes=30):
        if not self.loaded: self.load()
        m = max(1, min(self.QUIET_MAX, int(minutes))); self.quiet_until = int(time.time() + 60 * m)
        self.sounds, self.pending = [], []; self.save(); HOST.refresh_settings(ALERTS_PAGE)
        API.SysMsg("Alerts: quiet until %s." % time.strftime("%H:%M", time.localtime(self.quiet_until)), Kit.HUE_INFO)
    def resume(self):
        if not self.loaded: self.load()
        self.quiet_until = 0; self.save(); HOST.refresh_settings(ALERTS_PAGE)
        API.SysMsg("Alerts: back on.", Kit.HUE_INFO)
    def quiet_alarm(self, now=None):
        left = self.alarm_until - (time.time() if now is None else now); return 0 < left <= self.QUIET_ALARM
    def toggle_quiet(self):
        if self.quiet_on(): self.resume()
        else: self.quiet(30)
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
    def raise_(self, key, text, level="warn", sound=None, ping=None, who=None, owner=None, name=None, serial=None):
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
        nm = str(name) if name is not None else who if isinstance(who, str) and len(who) > 1 else ""
        try: ser = int((0 if isinstance(who, str) else who) if serial is None else serial) or 0
        except (TypeError, ValueError): ser = 0
        hue = self.LEVELS.get(level, Kit.HUE_TITLE); API.SysMsg(Alerts.veiled(line, nm, ser), hue)
        quiet = self.quiet_on(now); self.log.append((now, str(level), line, key, quiet, nm, ser))
        if len(self.log) > self.LOG_CAP: del self.log[:-self.LOG_CAP]
        self.log_ver += 1; self.log_due = True
        if level == "alarm" and (quiet or not self.banner_on):
            self.alarm_until = self.hold[rk[1]] = now + self.QUIET_ALARM
            if len(self.hold) > 50: self.hold = dict((w, u) for w, u in self.hold.items() if u > now)
        sid = (int(sound) if sound else snd) if snd else 0
        if sid and not self.mute and not quiet and len(self.sounds) < 4:
            if not self.sounds and not 0 <= now - self.sound_at < ALERT_SOUND_GAP: self._play(sid, now)
            else: self.sounds.append(sid)
        if self.banner_on and not quiet:
            self.pending.append((line, hue, level == "alarm", nm, ser, rk[1]))
            if len(self.pending) > 50: del self.pending[:-50]
        if ping is not None and len(self.pings) < 8:
            safe(lambda: self.pings.append([int(ping[0]), int(ping[1]), now + 10.0]))
        self.busy = True; return True
    def _play(self, sid, now): self.sound_at = now; API.PlaySound(int(sid))
    def tick(self, now):
        if self.log_due and not 0 <= self.log_at - now <= self.LOG_EVERY: self.save_log(now)
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
        line, hue, alarm, nm, ser = items[-1][:5]
        if self.shown and Kit.is_open(self.g):
            self.count += len(items); self.alarm = self.alarm or any(it[2] for it in items); self.items += items
        else: self.count = len(items) - 1; self.alarm = any(it[2] for it in items); self.items = list(items)
        if len(self.items) > 50:
            cut = len(self.items) - 50; keep = []
            for it in self.items:
                if cut and not it[2]: cut -= 1
                else: keep.append(it)
            self.items = keep[-50:]
        self.line, self.hue, self.line_who = line, hue, (nm, ser)
        if not Kit.is_open(self.g): self._build()
        if self.g is None: return
        self._label()
        if not self.shown:
            Kit.set(self.g, "IsVisible", True); self.shown = True; self.clicked = False
            self.pos = Snap.pos(self.g)
        self.hide_at = now + ALERT_HOLD; self.flash_at = now + ALERT_FLASH; self.flash_on = True
    def _label(self):
        c = self.c; more = ("+%d more" % self.count) if self.count > 0 else ""; mw = Kit.text_px(more) if more else 0
        bw = self.bw + 6; tw = self.W - 36 - bw - ((mw + 8) if more else 0); self.tw = tw
        Kit.set_text(c["text"], Kit.fit(self.shown_line(), tw), self.hue); Kit.set_text(c["more"], more, Kit.HUE_INFO)
        if more: s = self.scale; c["more"].SetPos(int(round((self.W - 18 - bw - mw) * s)), int(round(15 * s)))
    def _watch(self, now):
        g = self.g
        if not Kit.is_open(g): self.shown, self.g, self.items = False, None, []; return
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
                Kit.set_text(self.c["text"], Kit.fit(self.shown_line(), self.tw), Kit.HUE_BAD
                             if self.flash_on else Kit.HUE_TEXT)
        elif not 0 < self.hide_at - now <= ALERT_HOLD: self.dismiss()
    def drop(self, whos):
        whos = set([str(whos)] if isinstance(whos, str) else [str(w) for w in whos])
        now = time.time(); n = len(self.pending) + len(self.hold)
        self.pending = [it for it in self.pending if it[5] not in whos]
        self.hold = dict((w, u) for w, u in self.hold.items() if w not in whos)
        self.alarm_until = max(list(self.hold.values()) + [0.0])
        if not self.shown: self.items = []
        keep = [it for it in self.items if it[5] not in whos]; gone = len(self.items) - len(keep)
        if not gone: return n != len(self.pending) + len(self.hold)
        if not keep: self.dismiss(); return True
        self.items, self.count, self.alarm = keep, max(0, self.count - gone), any(it[2] for it in keep)
        self.line, self.hue, self.line_who = keep[-1][0], keep[-1][1], (keep[-1][3], keep[-1][4])
        if Kit.is_open(self.g): self._label(); self.hide_at = now + ALERT_HOLD
        return True
    def dismiss(self, hold=False):
        if hold:
            now = time.time()
            for it in (self.items if self.shown else []) + self.pending:
                if it[2]: self.alarm_until = self.hold[it[5]] = now + self.QUIET_ALARM
        self.shown, self.count, self.alarm = False, 0, False; g = self.g; self.items = []
        if Kit.is_open(g): Kit.set(g, "IsVisible", False)
    def _click(self): self.clicked = True; self.busy = True
    def _build(self):
        W, H, s = self.W, self.H, Kit.tscale; WS, HS = int(round(W * s)), int(round(H * s))
        sw = Kit.screen()[0] or 1024
        x, y = Kit.load_pos(self.POS_KEY, (max(0, (sw - WS) // 2), 60), (WS, HS)); g = G.CreateGump(True, True)
        Kit.add_window_frame(g, W, H, corners=False); Kit.add_section(g, 8, 8, W - 16, H - 16)
        c = {"text": Kit.add_label(g, "", 18, 15, Kit.HUE_TITLE),
             "more": Kit.add_label(g, "", W - 60, 15, Kit.HUE_INFO)}
        Kit.catcher(g, 0, 0, W, H, self._click, "Click to dismiss; drag to move", movable=True)
        bw, bh = Kit.pic_size(Kit.ART_PAGE[0]); self.bw, bh = bw or 30, bh or 22; self.store = ({}, {})
        Binds.scoped("va.banner", Kit.art_button, g, self.store, "history", Kit.ART_PAGE, W - 12 - self.bw,
                     (H - bh) // 2, None, "Show the last 50 alerts", None, lambda: HOST.alert_log.open())
        self.scale = s if Kit.scale_window(g, s) else 1.0
        if self.scale == 1.0: WS, HS = W, H
        Kit.show_window(g, x, y, WS, HS, None, False, None, lambda: Kit.save_pos(self.POS_KEY, self.g))
        self.g, self.c = g, c; self.shown = False
    def rebuild(self):
        g = self.g; up = self.shown and Kit.is_open(g)
        if g is None: return
        if Kit.is_open(g): Kit.save_pos(self.POS_KEY, g)
        self.g = None; Kit.dispose(g); self.shown = False
        if not up: return
        self._build()
        if self.g is None: return
        self._label(); Kit.set(self.g, "IsVisible", True); self.shown = True; self.pos = Snap.pos(self.g)
    def close(self):
        if self.log_due: self.save_log(time.time())
        g, self.g = self.g, None
        if Kit.is_open(g): Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g); self.shown = False; self.pending, self.sounds, self.pings = [], [], []; self.busy = False


class AlertLog(object):
    W = 600; ROW = 20; POS_KEY = "VirtueAssistant_alert_log_pos"; EVERY = 1.0; TITLE = "ALERT HISTORY"
    def __init__(self): self.g = None; self.store = ({}, {}); self.ver = -1; self.next = 0.0; self.want = 0.0
    def open(self):
        now = time.time()
        if 0 <= now - self.want < 2.0: return
        self.want = now; Kit.pending.append(self._open); HOST.poke()
    def _open(self):
        self.want = 0.0
        if not ALERTS.loaded: ALERTS.load()
        if Kit.is_open(self.g): self.rebuild()
        else: Binds.scoped("va.alertlog", self._build)
    def rows(self):
        out = []; tw = self.W - 2 * Kit.MARGIN - 24
        for t, level, line, _key, quiet, who, ser in reversed(list(ALERTS.log)):
            line = Alerts.veiled(line, who, ser)
            head = time.strftime("%H:%M", time.localtime(t)) + "  "; tail = "  (quiet)" if quiet else ""
            text = head + Kit.fit(line, tw - Kit.text_w(head) - Kit.text_w(tail)) + tail
            out.append((text, Kit.HUE_INFO if quiet else Alerts.LEVELS.get(level, Kit.HUE_TITLE)))
        return out
    def _build(self):
        M, W, s = Kit.MARGIN, self.W, Kit.tscale; rows = self.rows(); self.store = ({}, {})
        self.ver = ALERTS.log_ver; self.next = time.time() + self.EVERY
        h_body = 16 + self.ROW * max(1, len(rows)); H = M + 30 + Kit.GAP + h_body + M
        g = G.CreateGump(True, True); Kit.add_window_frame(g, W, H); Kit.add_section(g, M, M, W - 2 * M, 30)
        Kit.add_label(g, self.TITLE, M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, self.store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None, "Close")
        yb = M + 30 + Kit.GAP; Kit.add_section(g, M, yb, W - 2 * M, h_body)
        if not rows: Kit.add_label(g, "No alerts yet.", M + 12, yb + 8, Kit.HUE_INFO)
        for i, (text, hue) in enumerate(rows): Kit.add_label(g, text, M + 12, yb + 8 + self.ROW * i, hue)
        sc = s if Kit.scale_window(g, s) else 1.0; WS, HS = int(round(W * sc)), int(round(H * sc))
        sw = Kit.screen()[0] or 1024; x, y = Kit.load_pos(self.POS_KEY, (max(0, (sw - WS) // 2), 80), (WS, HS))
        Kit.place(g, x, y, WS, HS, int(round((M + 30 + Kit.GAP) * sc))); Kit.add_front(g)
        Kit.on_moved(g, lambda: Kit.save_pos(self.POS_KEY, self.g)); self.g = g
    def rebuild(self):
        g, self.g = self.g, None
        if Kit.is_open(g): Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g); Binds.scoped("va.alertlog", self._build)
    def poll(self, now):
        g = self.g
        if g is None: return
        if not Kit.is_open(g) or Kit.was_clicked(self.store, "close"): self.close(); return
        if self.ver != ALERTS.log_ver and not 0 <= self.next - now <= self.EVERY: self.rebuild()
    def close(self):
        g, self.g = self.g, None
        if Kit.is_open(g): Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g)


class Guard(object):
    KEY = "VirtueAssistant_guard"; EVERY = 0.25
    NUMS = {500112: GUARD_IN_TEXTS[0], 500114: GUARD_IN_TEXTS[0], 500113: GUARD_OUT_TEXTS[0],
            500115: GUARD_OUT_TEXTS[1]}
    def __init__(self): self.state = self.rd = self.saved = None; self.next = 0.0; self.cache = (0.0, None, None)
    def tick(self, now):
        if now < self.next and self.next - now <= self.EVERY: return
        self.next = now + self.EVERY
        if self.rd is None: self.rd = Journal.reader(); self.rd.last = 0
        for ln in self.rd.new():
            low = Journal.said(ln, self.NUMS)
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
    QUIET_CAPS = ("Quiet 30 min", "Resume")
    def table(self, w):
        q = ALERTS.quiet_on(); qx = 12 + 35 + max(Kit.text_w(c) for c in self.QUIET_CAPS) + 20 + 35
        qx += Kit.text_w("History") + 20
        note = ("Quiet until %s" % time.strftime("%H:%M", time.localtime(ALERTS.quiet_until))) if q else ""
        quiet = (("quiet", Kit.ART_PLAY, self.QUIET_CAPS[1], "Turn alert sounds and banners back on") if q else
                 ("quiet", Kit.ART_PLAY, self.QUIET_CAPS[0], "No alert sounds or banners for 30 minutes; journal "
                  "lines and the history stay"))
        return (("ALERTS  (every module's warnings)", (("check", "mute", "Mute every alert sound",
                     "No alert sounds; banners and journal lines stay", {"stay": True}),
                    ("check", "banner", "Show the banner", "Show alerts in a banner (click to dismiss, drag to move)",
                     {"dx": 242}), ("buttons", (("test", Kit.ART_PLAY, "Test alert",
                                  "Raise a test alert"),), {"bdy": 4, "stay": True}),
                    ("note", "The same alert repeats at most every %d s." % int(ALERT_RATE), {"dx": 172, "ndy": 7}),
                    ("buttons", (quiet, ("history", Kit.ART_PAGE, "History", "Show the last 50 alerts")),
                     {"bdy": 4, "stay": True}), ("note", note, {"dx": qx, "ndy": 7})),
                 {"top": 32, "sh": 118}), (Kit.fit("ALERT KINDS  (from modules on this session)", w - 16),
                 (("custom", 0, self._kinds),), {"sh": 40 + 28 * max(1, len(self.kinds()))}))
    def height(self, w): return Kit.Form.height(self.table(w), w)
    def build(self, g, x, y, w):
        if not ALERTS.loaded: ALERTS.load()
        self.store = ({}, {}); self.quiet_drawn = ALERTS.quiet_on()
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
            if not banner: ALERTS.dismiss(True)
            ALERTS.save()
        for key, cb in c["rows"]:
            try: v = bool(cb.IsChecked)
            except Exception: continue
            if v != ALERTS.setting(key)[0]: ALERTS.choose(key, on=v)
        if Kit.was_clicked(self.store, "test"):
            ALERTS.kind(Alerts.TEST_KEY, "Test", 0x1EA, APP_NAME); ALERTS.last.pop((Alerts.TEST_KEY, "test"), None)
            ALERTS.raise_(Alerts.TEST_KEY, "This is how an alert looks and sounds.", "warn", who="test")
        if Kit.was_clicked(self.store, "quiet"): ALERTS.toggle_quiet()
        if Kit.was_clicked(self.store, "history"): HOST.alert_log.open()
        q = ALERTS.quiet_on()
        if q != self.quiet_drawn: self.quiet_drawn = q; HOST.refresh_settings(ALERTS_PAGE)
        for n, row in enumerate(c["dd"]):
            key, dd, ids, idx = row; i = Kit.dd_index(dd, idx)
            if i != idx and 0 <= i < len(ids): idx = i; c["dd"][n] = (key, dd, ids, i); ALERTS.choose(key, sound=ids[i])
            if Kit.was_clicked(self.store, "play%d" % n) and ids[idx]: API.PlaySound(int(ids[idx]))


class BackupPage(_Page):
    KEEP = 10; ARM = 3.0; DIR = "Backups"; VER_KEY = "VirtueAssistant_backup_ver"; AUTO = "before %s"
    SKIP = ("VirtueAssistant_starting", "VirtueAssistant_backup_ver")
    def __init__(self):
        _Page.__init__(self); self.items = None; self.sel = 0; self.armed = (None, 0.0); self.pick = None
    def table(self, w):
        return (("BACKUPS  (this character)", (
            ("buttons", (("backup_now", Kit.ART_OK, "Back up now", "Save every Virtue Assistant setting of this "
                          "character now (the 10 newest are kept)"),
                         ("restore", Kit.ART_PLAY, "Restore", "Put the picked backup back (press twice; the "
                          "settings of now are backed up first)"))),
            ("custom", 30, self._list), ("note", "In the VirtueAssistantSettings folder, Backups")), {}),)
    def height(self, w): return Kit.Form.height(self.table(w), w)
    def build(self, g, x, y, w):
        self.store = ({}, {}); self.c = Kit.Form(g, x, y, w, {}, self.table(w), self.store).c
    def _list(self, f, x, y):
        items = self.items or []; names = [lbl for _, lbl in items]
        if not names: names = ["Reading the backups" if self.items is None else "No backups yet"]
        at = [i for i, it in enumerate(items) if it[0] == self.pick]
        self.sel = at[0] if at else max(0, min(self.sel, len(names) - 1))
        dd = G.CreateDropDown(min(380, f.w - 24), names, self.sel); dd.SetPos(x + 12, y + 2); f.g.Add(dd)
        Kit.with_tip(dd, "The backup that Restore puts back"); f.c["dd"] = dd
    def poll(self):
        c = self.c
        if c is None: return
        dd = c.get("dd"); items = self.items or []
        if dd is not None: self.sel = Kit.dd_index(dd, self.sel)
        if 0 <= self.sel < len(items): self.pick = items[self.sel][0]
        if Kit.was_clicked(self.store, "backup_now"): self.ask(("backup", "by hand"))
        if not Kit.was_clicked(self.store, "restore"): return
        if not items: API.SysMsg("Backups: there is no backup to restore yet.", Kit.HUE_BAD); return
        name = items[max(0, min(self.sel, len(items) - 1))][0]; now = time.time(); a = self.armed
        if a[0] == name and 0 <= a[1] - now <= self.ARM: self.armed = (None, 0.0); self.ask(("restore", name)); return
        self.armed = (name, now + self.ARM); API.SysMsg("Backups: press Restore again to confirm.", Kit.HUE_INFO)
    @staticmethod
    def ask(req):
        if HOST.profile_req is not None: API.SysMsg("Backups: busy saving; try again.", Kit.HUE_BAD); return
        HOST.profile_req = req; HOST.poke()
    @staticmethod
    def base():
        serial = safe(lambda: int(API.Player.Serial), 0)
        if not serial: raise Exception("the character isn't in the world yet")
        return os.path.join(Kit.data_path(BackupPage.DIR), "%08X" % serial)
    @staticmethod
    def names():
        base = BackupPage.base()
        if not os.path.isdir(base): return []
        return sorted(n for n in os.listdir(base) if not n.endswith(".saving")
                      and os.path.isfile(os.path.join(base, n, "info.txt")))
    @staticmethod
    def info(name):
        text = Kit.read_safe(os.path.join(BackupPage.base(), name, "info.txt"), None) or ""
        return dict((k.strip(), v.strip()) for k, v in (ln.split("=", 1) for ln in text.splitlines() if "=" in ln))
    @staticmethod
    def label(name): return "%s %s%s" % (name[:10], name[11:19].replace("-", ":"), name[19:].replace("-", " #"))
    def scan(self):
        out = []
        for n in reversed(self.names()):
            why = self.info(n).get("why", ""); out.append((n, self.label(n) + ("  (%s)" % why if why else "")))
        self.items = out
    @staticmethod
    def snapshot(prefs):
        found = Profiles.char_vars(); extra = Profiles.extra_keys(found)
        skip = set(Profiles.SESSION_VARS + BackupPage.SKIP + (PROFILE_STATE_KEY,))
        va = dict((k, v) for k, v in found.items() if k not in skip and k.startswith(Profiles.VA_KEYS + extra))
        va[SETTINGS_KEY] = prefs; return va
    @staticmethod
    def _drop(path):
        for n in os.listdir(path): os.remove(os.path.join(path, n))
        os.rmdir(path)
    @staticmethod
    def read_vars(path): return Profiles.parse_vars(Kit.read_safe(os.path.join(path, "va_vars.txt"), None) or "")
    @staticmethod
    def early():
        if Kit.get_var(BackupPage.VER_KEY) == APP_VERSION: return None
        bag = safe(Profiles.bag_path)
        return safe(lambda: (BackupPage.snapshot(Kit.get_var(SETTINGS_KEY)), Kit.read_safe(bag, None) if bag else None))
    def make(self, why, prefs, keep=None, early=None):
        base = self.base(); t = time.time(); stem = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(t))
        if not os.path.isdir(base): os.makedirs(base)
        top = -1
        for n in os.listdir(base):
            if n.endswith(".saving"): safe(lambda: self._drop(os.path.join(base, n))); continue
            rest = n[len(stem):] if n.startswith(stem) else None
            if rest == "": top = max(top, 0)
            elif rest and rest[0] == "-" and rest[1:].isdigit(): top = max(top, int(rest[1:]))
        name = stem if top < 0 else "%s-%02d" % (stem, top + 1)
        final = os.path.join(base, name); tmp = final + ".saving"; os.makedirs(tmp)
        va = early[0] if early else self.snapshot(prefs)
        Profiles._write(os.path.join(tmp, "va_vars.txt"),
                        "".join("%s\t%s\n" % (Profiles._esc(k), Profiles._esc(va[k])) for k in sorted(va)))
        bag = Profiles.bag_path(); text = early[1] if early else Kit.read_safe(bag, None) if bag else None
        if text is not None: Profiles._write(os.path.join(tmp, "unified_bag.cfg"), text)
        Profiles._write(os.path.join(tmp, "info.txt"), "saved=%d\nversion=%s\nwhy=%s\ncount=%d\n"
                        % (int(t), APP_VERSION, why, len(va)))
        if self.read_vars(tmp) != va:
            safe(lambda: self._drop(tmp)); raise Exception("the backup doesn't read back the same; try again")
        os.rename(tmp, final); names = self.names(); extra = len(names) - self.KEEP
        for n in names:
            if extra <= 0: break
            if n != keep and n != name: safe(lambda: self._drop(os.path.join(base, n))); extra -= 1
        return name, len(va)
    def read(self, name):
        path = os.path.join(self.base(), name)
        if not os.path.isfile(os.path.join(path, "info.txt")): raise Exception("that backup is gone")
        va = self.read_vars(path); n = self.info(name).get("count", "")
        if n.isdigit() and int(n) != len(va): raise Exception("that backup is damaged")
        return va, Kit.read_safe(os.path.join(path, "unified_bag.cfg"), None)
    @staticmethod
    def apply(va, lay, gone=()):
        for k in sorted(va): Kit.put_var(k, va[k])
        for k in sorted(set(gone) - set(va)): Kit.put_var(k, "")
        ok = PROFILES.wait_vars(va); bag = Profiles.bag_path(); own = Profiles.BAG_OWN
        cur = Kit.read_safe(bag) if lay is not None and bag else None
        if cur is not None:
            keep = [l for l in lay.splitlines() if l.strip() and not l.startswith(own)]
            Profiles._write(bag, "\n".join(keep + [l for l in cur.splitlines() if l.startswith(own)]))
        return ok


def _norm_key(k):
    parts = [p for p in str(k or "").strip().upper().replace(" ", "").split("+") if p]
    keys = [p[5:] if p.startswith("SDLK_") else p for p in parts if p not in ("CTRL", "SHIFT", "ALT")]
    return "+".join([m for m in ("CTRL", "SHIFT", "ALT") if m in parts] + keys[-1:])


class Binds(object):
    VAR = "VirtueAssistant_binds"; REPEAT = 0.6; ARM_SECS = 20.0; REG_CAP = 5000; armed_until = 0.0; reg = {}
    saved = {}; last = {}; hooked = set(); armed = False; picked = None; answer = None; loaded = False; scope = None
    OWNER = "Button binds"; IDS_VAR = "VirtueAssistant_binds_ids"; NEW_VAR = "VirtueAssistant_binds_new"; made = set()
    last_va = {}
    @staticmethod
    def old(bid): return bid.startswith("va|") and bid not in Binds.made
    @staticmethod
    def scoped(name, fn, *args):
        was = Binds.scope; Binds.scope = name
        try: return fn(*args)
        finally: Binds.scope = was
    @staticmethod
    def note(store, key, on_click, ctl, tip):
        owner = Binds.scope or HOST.cur_owner
        if len(Binds.reg) >= Binds.REG_CAP: Binds.reg.clear(); Binds.last_va.clear()
        if owner is None:
            cur = HOST.current(); pg = Kit.Form.page
            if cur is not None: owner = cur.key
            else:
                owner = pg + ".page" if dict.__contains__(HOST.by_key, pg) else "va"
                Binds.last_va[key] = "%s|%s" % (owner, key)
        bid = "%s|%s" % (owner, key)
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
        Binds.loaded = True; fresh = str(Kit.get_var(Binds.IDS_VAR, "") or "") != "2"; dropped = 0
        for part in str(Kit.get_var(Binds.VAR, "") or "").split(";"):
            if "=" in part:
                bid, combo = part.rsplit("=", 1)
                if fresh and bid.split("|", 1)[0] in ("va", "interface"): dropped += 1; continue
                combo = _norm_key(combo)
                if bid and combo: Binds.saved[bid] = combo; Binds.hook(combo)
        new = [(b, _norm_key(c)) for b, c in (x.rsplit("=", 1) for x in
                                               str(Kit.get_var(Binds.NEW_VAR, "") or "").split(";") if "=" in x)]
        for b, c in new:
            if Binds.page(b) and c and b not in Binds.saved and c not in Binds.saved.values():
                Binds.saved[b] = c; Binds.hook(c)
        Binds.made = set(b for b, c in new if Binds.saved.get(b) == c and not Binds.page(b))
        if fresh:
            Kit.put_var(Binds.IDS_VAR, "2")
            if dropped:
                Binds.save()
                Kit.say("%s cleared (each window has its own now); bind them again in Settings > Hotkeys."
                        % Kit.count(dropped, "button key"), Kit.HUE_INFO)
    @staticmethod
    def page(bid): return bid.split("|", 1)[0].endswith(".page")
    @staticmethod
    def save():
        Kit.put_var(Binds.VAR, ";".join("%s=%s" % kv for kv in sorted(Binds.saved.items()) if not Binds.page(kv[0])))
        Binds.made &= set(Binds.saved)
        Kit.put_var(Binds.NEW_VAR, ";".join("%s=%s" % (b, c) for b, c in sorted(Binds.saved.items())
                                            if b in Binds.made or Binds.page(b)))
    @staticmethod
    def hook(combo):
        if HOST.hotkey_on(combo, Binds.OWNER, lambda: Binds.fire(combo), "a button") is not False:
            Binds.hooked.add(combo)
    @staticmethod
    def unhook(combo): Binds.hooked.discard(combo); HOST.hotkey_off(combo, Binds.OWNER)
    @staticmethod
    def fire(combo):
        now = time.time(); was = Binds.last.get(combo); Binds.last[combo] = now
        if was is not None and 0 <= now - was < Binds.REPEAT: return
        for bid, c in Binds.saved.items():
            if c == combo:
                if Binds.old(bid): bid = Binds.last_va.get(bid[3:], bid)
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
        gone = [b for b, c in Binds.saved.items() if c == combo and b != bid and Binds.old(b)]
        taken = next((row[1] for row in KeysPage.rows() if row[0] == combo
                      and not (row[1] == Binds.OWNER and (gone or Binds.saved.get(bid) == combo))), None)
        if taken is not None:
            Kit.say("%s is already %s's key; pick another." % (combo, taken), Kit.HUE_BAD); return
        for b in gone: Binds.saved.pop(b, None)
        old = Binds.saved.get(bid)
        if bid.startswith("va|"): Binds.made.add(bid)
        if old and old != combo: Binds.unhook(old)
        Binds.saved[bid] = combo; Binds.hook(combo); Binds.save()
        Kit.say("%s bound." % combo, Kit.HUE_GOOD); HOST.refresh_settings(KEYS_PAGE)
    @staticmethod
    def clear():
        for combo in set(Binds.saved.values()) | Binds.hooked: Binds.unhook(combo)
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


ALERTS_PAGE, KEYS_PAGE, BACKUP_PAGE = "va.alerts", "va.keys", "va.backups"


class WhatsNew(object):
    W = 520; SEEN_KEY = "VirtueAssistant_new_seen"; seen_keys = None
    NEW_KEYS = ("prices.pick_book", "prices.book_open", "prices.book_head", "prices.keep_SS", "prices.keep_NS",
                "prices.keep_BP", "prices.keep_GA", "prices.keep_SA", "prices.keep_BM", "prices.keep_GI",
                "prices.keep_MR", "prices.say", "prices.skip_old", "prices.dist", "prices.old", "prices.hk")
    def __init__(self): self.g = None; self.store = ({}, {}); self.text = None
    @staticmethod
    def seen():
        if WhatsNew.seen_keys is None:
            ver, _, keys = Kit.get_var(WhatsNew.SEEN_KEY, "").partition(":")
            WhatsNew.seen_keys = set(k for k in keys.split(",") if k) if ver == APP_VERSION else set()
        return WhatsNew.seen_keys
    @staticmethod
    def unseen(page=None):
        seen = WhatsNew.seen(); pre = None if page is None else page + "."
        return set(k for k in WhatsNew.NEW_KEYS if k not in seen and (pre is None or k.startswith(pre)))
    @staticmethod
    def see(keys):
        seen = WhatsNew.seen(); new = set(keys) - seen
        if new: seen.update(new); Kit.put_var(WhatsNew.SEEN_KEY, "%s:%s" % (APP_VERSION, ",".join(sorted(seen))))
    def due(self):
        if self.text is None: self.text = whats_new()
        if not self.text: return False
        try: seen = API.GetPersistentVar(WHATS_NEW_KEY, "", API.PersistentVar.Account)
        except Exception: return False
        return str(seen or "") != APP_VERSION
    def open(self):
        if self.due(): Kit.on_client(lambda: Binds.scoped("va.news", self._build))
    def show(self):
        if self.text is None: self.text = whats_new()
        if not self.text: return False
        if not Kit.is_open(self.g): Kit.on_client(lambda: Binds.scoped("va.news", self._build))
        return True
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
        Kit.add_front(g); self.g = g
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
        self.category = "Other"; self.next_due = 0.0; self.errors = set(); self.error_times = {}
        self.load = [0.0, 0.0, 0.0]; self.part_load = {}
        self.start_tok = None; self.page_err_at = 0.0; self.shipped = False
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
    __slots__ = ("seq", "text", "low", "name", "hue", "ticks", "at", "kind", "num", "mtype")
    def __init__(self, seq, text, name, hue, ticks, at, kind, mtype=""):
        self.seq, self.text, self.low, self.name = seq, text, text.lower(), name
        self.hue, self.ticks, self.at, self.kind, self.num, self.mtype = hue, ticks, at, kind, 0, mtype


class Journal(object):
    KEEP = 60.0; MAX_BACK = 30.0; lines = []; seen = {}; seq = 0; read_at = 0.0; pass_id = -1; zero_seen = False
    clis = []; CLI_CAP = 64; CLI_AGE = 5.0; hook = {"on": False}; AHEAD = 50000000
    ATTACK_RE = re.compile(r"\*?\s*(.+?)\s+is attacking you", re.IGNORECASE)
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
        Journal.pass_id = pid; now = time.time(); lines = Journal.lines
        if not Journal.hook["on"]:
            Kit.hook_once(Journal.hook, "on", ("OnClilocMessageReceived", Journal.on_cliloc), owner=None)
        if lines and lines[-1].at > now + 1.0:
            d = lines[-1].at - now
            for ln in lines: ln.at -= d
        back = min(Journal.MAX_BACK, max(1.0, now - Journal.read_at + 1.0)) if Journal.read_at else Journal.MAX_BACK
        Journal.read_at = now
        try: entries = list(API.GetJournalEntries(back) or [])
        except Exception: entries = []
        nt = base = ub = None
        if entries:
            try:
                import System; d = System.DateTime; nt = int(d.Now.Ticks); t = time.time(); base = t - nt / 1e7
                ub = t - int(d.UtcNow.Ticks) / 1e7
            except Exception: nt = base = ub = None
        seen, fresh, zero, stopped, i = Journal.seen, [], [], False, len(entries) - 1
        while i >= 0:
            e = entries[i]; i -= 1; pos = i
            try:
                text = str(e.Text or "")
                if not text: continue
                try: ticks = int(e.Time.Ticks)
                except Exception: ticks = 0
                if nt is not None and ticks > nt + Journal.AHEAD: continue
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
                at = now
                if key[0] and base is not None:
                    try: at = int(e.Time.ToUniversalTime().Ticks) / 1e7 + ub
                    except Exception: at = key[0] / 1e7 + base
                    if at < now - back - 1.0: continue
                    at = min(now, at)
                try: mt = e.MessageType; mt = "" if mt is None else str(mt)
                except Exception: mt = ""
                Journal.seq += 1; seen[key] = Journal.seq; kind = e.TextType
                Journal.lines.append(JLine(Journal.seq, key[1], key[2], int(e.Hue or 0), key[0], at,
                                           "" if kind is None else str(kind), mt))
            except Exception: continue
        if Journal.clis: Journal.pair(now)
        cut = now - Journal.KEEP
        if lines and lines[0].at < cut:
            i = 0
            while i < len(lines) and lines[i].at < cut:
                ln = lines[i]; seen.pop((ln.ticks, ln.text, ln.name), None); i += 1
            del lines[:i]
    @staticmethod
    def on_cliloc(e):
        try: Journal.clis.append((int(e.Cliloc), str(e.Text or ""), time.time()))
        except Exception: return
        if len(Journal.clis) > Journal.CLI_CAP: del Journal.clis[:-Journal.CLI_CAP]
    @staticmethod
    def pair(now):
        recs, Journal.clis = Journal.clis, []; keep = []
        for rec in recs:
            num, text, t = rec; hit = False
            for ln in reversed(Journal.lines):
                if ln.at < t - Journal.CLI_AGE: break
                if not ln.num and ln.text == text: ln.num = num; hit = True; break
            if not hit and now - t < Journal.CLI_AGE: keep.append(rec)
        if keep: Journal.clis[:0] = keep[-Journal.CLI_CAP:]
    @staticmethod
    def said(ln, nums): t = nums.get(ln.num) if ln.num else None; return ln.low if t is None or t in ln.low else t
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
    def due():
        for j in Picker.jobs:
            if j["d"] is None or j["got"] is not None: return True
        return False
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
                        try: j["got"] = (int(obj.Serial or 0) if obj is not None else 0)
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
        self.boot = [("code", time.time() - START_AT)]; self.boot_at = time.time(); self.boot_load = 0.0
        self.cur_part = self.cur_owner = self.config = self.hub = self.grid = self.profile_req = self.alone = None
        self.hurt_hp = self._me = self._want_raw = self.attack_rd = None; self.stack = []
        self.harm_conf = (None, 0, 0.0)
        self.quitting = self.shut = self.ui_busy = self.poked = self.prefs_frozen = False
        self.prefs_busy = self.prefs_told = False; self.gump_hold = (None, 0.0)
        self.in_hop = self.pass_poked = self.pass_all = self.poke_user = self.draining = False; self.alive_at = 0.0
        self.poke_keys = set(); self.pass_keys = self.NO_KEYS; self.off_q = []; self._stop_fi = None
        self.look = self.LOOKAHEAD
        import _thread; self._drain_lk = _thread.allocate_lock(); self._gump_lk = _thread.allocate_lock()
        self.ui_next = self.dock_next = self._claim_len = self.hurt_until = self.input_at = 0.0
        self.attacked_until = self.prefs_at = self.pressed_at = 0.0; self.hurt_who = 0; self.prefs_due = False
        self.docks = []; self.services = {}; self.hotkeys_owned = {}; self.prefs = {}; self.cursor_claim = (None, 0.0)
        self.hk_fns = {}; self.hk_wait = {}; self.gump_exp = {}; self.services["gump.expect"] = self.gump_expect
        self.foe_seen = (0.0, None); self.client_idles = self.pass_id = 0
        self._me_pid = self._mob_pid = self._one_pid = -1; self._mob_list = (); self._one = {}; self._pack = {}
        self._mob_at = 0.0; self._pack_v = 0; self._pack_keys = set(); self._pack_hook = {"on": False}
        self._pack_fn = self._pack_event
        self.active = []; self.client_run = []; self._pass_fn = self._client_pass; self._want_set = frozenset()
        self.told, self._zone_held, self._zone_was_d, self._zone_bring = set(), set(), None, {}
        self.load_jobs = []; self.hotkey_list = []; self.pages = []; self.held_on = set(); self.held_parts = set()
        self.marked = False; self.ask_g = None; self.ask_store = ({}, {})
        self.settled_at = self.boot_line = None; self.settle_seen = 0.0; self.settle_capped = False; self.builds = {}
        self.settle_from = None; self.settle_holds = []; self.split = {}; self.compile_hit = False
        self.bar_dead = self.ahead_off = False; self.texts = {}; self.ahead_ms = {}
        self.tz_at = 0.0; self.tz_off = set(); self.tz_told = set()
        self.backups = BackupPage(); self.alert_log = AlertLog(); self.launcher = None; self.early_backup = None
        for key, title, page in ((ALERTS_PAGE, "Alerts", AlertsPage()), (KEYS_PAGE, "Hotkeys", KeysPage()),
                                 (BACKUP_PAGE, "Backups", self.backups)):
            s = ModuleSlot(key, title, "", None, 1.0); s.api = page.api(); self.pages.append(s)
        self.whats_new = WhatsNew()
        self.services["alerts.history"] = self.alert_log.open; self.services["alerts.quiet"] = ALERTS.toggle_quiet
    def _tell(self, msg):
        if msg in self.told: return
        if len(self.told) > 50: self.told.clear()
        self.told.add(msg); API.SysMsg(msg, Kit.HUE_BAD)
    def _refresh_active(self):
        act = [s for s in self.slots if s.running]; self.active = act; self.client_run = [s for s in act if s.on_client]
    NO_KEYS = frozenset()
    def poke(self, key=None, user=True):
        if self.draining:
            if key is None: self.pass_all = self.pass_poked = True
            else: self.pass_keys = self.pass_keys | frozenset((key, key.partition(".")[0]))
            if user: self.pass_poked = True; self.input_at = time.time()
            if user or key is None: self.ui_next = 0.0
            return
        if key is None: self.poked = True
        else: ks = self.poke_keys; ks.add(key); ks.add(key.partition(".")[0])
        if user: self.poke_user = True; self.input_at = time.time()
    def click_key(self): cur = self.current(); return cur.key if cur is not None else None
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
    def alert(self, key, text, level="warn", sound=None, ping=None, who=None, name=None, serial=None):
        s = self.current()
        if FADE.on and s is not None: FADE.wake(s.key)
        return ALERTS.raise_(key, text, level, sound, ping, who, s.title if s is not None else APP_NAME, name, serial)
    def guarded(self): return GUARD.guarded()
    def guard_area(self): return GUARD.area()
    def hotkey_note(self, combo, owner, what=""):
        k = _norm_key(combo)
        self.hotkey_list = [e for e in self.hotkey_list if not (_norm_key(e[0]) == k and e[1] == owner)]
        self.hotkey_list.append((k, str(owner), str(what or "")))
        if k not in self.hotkeys_owned: self.hotkeys_owned[k] = str(owner)
    def hotkey_on(self, combo, owner, fn, what=""):
        k, owner = _norm_key(combo), str(owner)
        if not k: return False
        cur = self.current(); ent = (owner, fn, cur.key if cur is not None else None, str(what or ""))
        held = self.hk_fns.get(k)
        if held is not None and held[0] != owner:
            wait = [w for w in self.hk_wait.get(k, ()) if w[0] != owner]; wait.append(ent); self.hk_wait[k] = wait
            Kit.say("%s is already %s's key; %s can't use it until that lets it go." % (k, held[0], owner), Kit.HUE_BAD)
            return None
        if held is None:
            try: API.OnHotKey(k, self._hk_fire(k))
            except Exception: return False
        self._hk_take(k, ent); return True
    def _hk_take(self, k, ent):
        self.hk_fns[k] = ent; self.hotkey_note(k, ent[0], ent[3]); self.hotkeys_owned[k] = ent[0]
    def _hk_fire(self, k):
        def fired(*args):
            self.pressed_at = time.time(); ent = self.hk_fns.get(k)
            if ent is not None: ent[1]()
        return fired
    def hotkey_off(self, combo, owner):
        k, owner = _norm_key(combo), str(owner); held = self.hk_fns.get(k)
        wait = [w for w in self.hk_wait.get(k, ()) if w[0] != owner]
        if wait: self.hk_wait[k] = wait
        else: self.hk_wait.pop(k, None)
        self.hotkey_drop(k, owner)
        if held is None or held[0] != owner: return
        if wait:
            nxt = wait.pop(0)
            if not wait: self.hk_wait.pop(k, None)
            self._hk_take(k, nxt); Kit.say("%s is %s's key now." % (k, nxt[0]), Kit.HUE_INFO); return
        self.hk_fns.pop(k, None)
        with Kit.quiet: API.OnHotKey(k)
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
            for p in [p[0] for p in s.parts if p[3] and (s.key, p[0]) not in self.held_parts] or [s.parts[0][0]]:
                s.parts_on[p] = True
    def _part_notify(self, s):
        if not s.running or s.api is None or not s.api.get("parts"): return
        was = s.busy; self._enter(s)
        try: want = set(s.parts_wanted()); Kit.on_client(lambda: s.api["parts"](want))
        except Exception as ex: self.report(s, ex)
        finally: self._leave(s); s.busy = was
    def part_set(self, module, part, on):
        s = dict.get(self.by_key, module)
        if s is None or s.part(part) is None: return
        on = bool(on); self.held_parts.discard((s.key, part))
        if s.parts_on.get(part) == on:
            if on and not s.enabled: self.enable(module)
            return
        s.parts_on[part] = on
        if not on: s.error_times.pop(part, None)
        if on and not s.enabled: self.enable(module)
        elif not on and not s.parts_wanted(): self.disable(module)
        else: self.save_prefs(); self._part_notify(s)
        self.refresh_settings(module)
    def alarm_up(self): return bool(ALERTS.shown and ALERTS.alarm) or ALERTS.quiet_alarm()
    def typing(self): return Client.typing()
    def release_typing(self): Typing.release()
    def grid_size(self): return max(8, min(512, self.pref_int("grid", GRID_DEFAULT)))
    def grid_shown(self): return self.grid is not None and self.grid.shown
    def grid_toggle(self):
        if self.grid is not None:
            self.grid.toggle(); self.prefs["grid_on"] = "1" if self.grid_shown() else "0"; self.save_prefs()
        return self.grid_shown()
    def set_look(self, name):
        name = name if name in Kit.LOOKS else "classic"; self.prefs["look"] = name
        self.prefs["dark"] = "1" if name in ("dark", "contrast") else "0"; self.save_prefs(); Kit.set_look(name)
        self.restyle("Look: %s." % Kit.LOOK_NAMES[name])
    SWITCHES = {"compact": "Compact rows", "cblind": "Colour-blind marks", "streamer": "Streamer mode"}
    def set_switch(self, key, value):
        if key == "tsize":
            v = int(value) if int(value) in Kit.TEXT_SIZES else 100; self.prefs[key] = str(v); Kit.tscale = v / 100.0
            note = "Text size: %d%%." % v
        elif key in self.SWITCHES:
            on = bool(value); self.prefs[key] = "1" if on else "0"
            note = "%s %s." % (self.SWITCHES[key], "on" if on else "off")
            if key == "compact": Kit.compact = on
            elif key == "cblind": Kit.cblind = on
            else: Kit.streamer = on
        else: return
        self.save_prefs(); self.restyle(note)
    def _apply_style(self):
        look, dark = self.prefs.get("look", ""), self.pref_int("dark", 0) == 1
        if look not in Kit.LOOKS or dark != (look in ("dark", "contrast")): look = "dark" if dark else "classic"
        Kit.set_look(look); ts = self.pref_int("tsize", 100); Kit.tscale = (ts if ts in Kit.TEXT_SIZES else 100) / 100.0
        Kit.compact, Kit.cblind = self.pref_int("compact", 0) == 1, self.pref_int("cblind", 0) == 1
        Kit.streamer = self.pref_int("streamer", 0) == 1; FADE.load(self)
    def restyle(self, note=None):
        FADE.reset(); Kit.retint()
        for k, d in list(self.docks):
            try: s = d["state"]() if d.get("redraw") is not None else None
            except Exception: s = None
            if s in ("open", "minimized"): safe(d["redraw"])
        for w in list(Kit._wins.values()):
            if Kit.is_open(w.win.get(w.gkey)): w.queue.add("redraw")
        for name, fn in list(self.services.items()):
            if name.startswith("look."): safe(fn)
        self.refresh_settings(LAYOUT_OWNER); c = self.config
        if c is not None and c.mode == "alone": c.refresh()
        elif c is not None:
            c.measured.clear()
            if c.mode == "full": c.prof_redraw = True
        safe(ALERTS.rebuild); self.poke()
        if self.alert_log.g is not None: self.alert_log.open()
        if Kit.is_open(self.whats_new.g): self.whats_new.close(); self.whats_new.show()
        if self.launcher is not None and self.launcher.g is not None: Kit.pending.append(self.launcher.rebuild)
        if note: Kit.say(note, Kit.HUE_GOOD)
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
    def gump_expect(self, gid, secs=5.0):
        gid = int(gid or 0)
        if not gid: return
        now = time.time(); exp = dict((k, t) for k, t in list(self.gump_exp.items()) if 0 < t - now <= GUMP_EXPECT_MAX)
        exp[gid] = now + max(0.0, min(float(secs), GUMP_EXPECT_MAX)); self.gump_exp = exp
    def gump_expected(self, gid, now):
        t = self.gump_exp.get(gid); return t is not None and 0 < t - now <= GUMP_EXPECT_MAX
    def gump_claim(self, owner, secs=10.0):
        with self._gump_lk:
            if self.gump_busy(owner) is not None: return False
            self.gump_hold = (owner, time.time() + max(0.0, min(float(secs), GUMP_EXPECT_MAX))); return True
    def gump_release(self, owner):
        with self._gump_lk:
            if self.gump_hold[0] == owner: self.gump_hold = (None, 0.0)
    def gump_busy(self, owner=None):
        o, t = self.gump_hold; due = 0 < t - time.time() <= GUMP_EXPECT_MAX
        return o if o is not None and o != owner and due else None
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
        if self.booting() and LAYOUT.holds(key): self._zone_held.add(key)
        gump = hooks.get("gump")
        if gump is not None: self.layout_add(key, gump, hooks.get("title"), hooks)
    def dock_remove(self, key): self.docks = [d for d in self.docks if d[0] != key]; self.layout_remove(key)
    def layout_add(self, key, get_gump, title=None, hooks=None):
        cur = self.current(); owner = (cur.key, self.cur_part if cur.parts else None) if cur is not None else None
        LAYOUT.add(key, get_gump, title, hooks, owner); LAYOUT.fit_added(key)
    def layout_remove(self, key): LAYOUT.remove(key)
    def layout_slot(self, key):
        key = str(key)
        if not LAYOUT.holds(key): return None
        rec = LAYOUT.fitted.get(key)
        if rec is not None and rec.get("told") is not None: return rec["told"]
        slot = LAYOUT.placed.get(key) or LAYOUT.plan_at(key); return (slot[2], slot[3]) if slot is not None else None
    def layout_rect(self, key):
        key = str(key)
        if not LAYOUT.holds(key): return None
        slot = LAYOUT.spot(key); return tuple(slot) if slot is not None else None
    def layout_holds(self, key): return LAYOUT.holds(key)
    def layout_need(self, key, w=None, h=None): LAYOUT.need(key, w, h)
    def layout_base(self, key): return LAYOUT.zone_base(key)
    def layout_locked(self, key): return LAYOUT.locked(key)
    def layout_arrange(self, on=None): LAYOUT.set_arrange((not LAYOUT.arrange) if on is None else on)
    def layout_arranging(self): return LAYOUT.arrange
    def layout_in_use(self): return bool(LAYOUT.assign) and LAYOUT.enabled
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
    def bar_on(self):
        s = dict.get(self.by_key, "actionbar")
        return not VA_ALONE and s is not None and bool(s.enabled) and not s.broken and not self.bar_dead
    def bar_soon(self): return self.bar_alive() or (self.booting() and self.bar_on())
    def dock_soon(self, key):
        return key in self._dock_want() and not LAYOUT.holds(key) and self.bar_on() and (
            self.booting() or self.bar_alive())
    def dock_tick(self):
        now = time.time()
        if now < self.dock_next and self.dock_next - now <= 0.25 and self.settled_at is not None: return
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
        elif not (self.booting() and self.bar_on()):
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
            if on and s is None and not LAYOUT.arrange and time.time() >= self._zone_bring.get(k, 0.0):
                fn = d.get("show") or d.get("on")
                if fn is not None: self._zone_bring[k] = time.time() + 2.0; safe(fn)
            if changed and d.get("redraw") is not None and s != "docked": safe(d.get("redraw"))
    TWICE = "%s: %s loaded twice (module key \"%s\"); skipped the second copy."; COMPILE_CAP = 64
    def compiled(self, text, path):
        c = None; self.compile_hit = False
        try:
            import sys; c = sys.__dict__.get("_COMPILED")
            if not isinstance(c, dict): c = {}; sys._COMPILED = c
            e = c.get(path)
            if type(e) is tuple and len(e) == 3 and e[0] == len(text) and type(e[1]) is str and e[1] == text:
                if type(e[2]) is type(self.compiled.__func__.__code__): self.compile_hit = True; return e[2]
        except Exception: c = c if type(c) is dict else None
        code = compile(text, path, "exec")
        try:
            if c is not None:
                if path not in c:
                    root = os.path.normcase(os.path.dirname(os.path.dirname(path)))
                    for k in [k for k in c if os.path.normcase(os.path.dirname(os.path.dirname(str(k)))) != root]:
                        c.pop(k, None)
                    if len(c) >= self.COMPILE_CAP: c.clear()
                c[path] = (len(text), text, code)
        except Exception: pass
        return code
    SELF_KEY = "_VA_INNER"
    def self_run(self, g):
        box = g.get(self.SELF_KEY)
        if box is not None:
            box[1] = True
            for k, ms in box[2]: self.split_add(k, ms)
            return False
        import sys; keep = None
        try:
            path = str(g.get("__file__") or os.path.join(str(API.ScriptPath), str(API.ScriptName)))
            t0 = time.time(); text = _read_text(path); t1 = time.time(); e = sys.__dict__.get("_VA_SELF")
            same = type(e) is tuple and len(e) == 4 and e[0] == path and e[1] == len(text) and type(e[2]) is str \
                and e[2] == text
            if same and e[3] is None: return False
            if same and type(e[3]) is type(self.compiled.__func__.__code__): code, kind = e[3], "hit"
            elif safe(self.no_cache, False): return False
            else:
                sys._VA_SELF = None; kind = "compile"
                code = compile(re.sub(r"(?m)^import API$", "", text.replace("\r\n", "\n")), path, "exec")
                sys._VA_SELF = (path, len(text), text, code)
            keep = dict(g); ms = (time.time() - t1) * 1000.0
            box = [START_AT, False, [("read:mother", (t1 - t0) * 1000.0), (kind + ":mother", ms)]]
            g[self.SELF_KEY] = box; exec(code, g)
        except Exception:
            if box is not None and box[1]: raise
        finally: g.pop(self.SELF_KEY, None)
        if box is not None and box[1]: return True
        stop = bool(safe(lambda: API.StopRequested, False))
        if keep is not None:
            g.clear(); g.update(keep)
            if not stop: sys._VA_SELF = (path, len(text), text, None)
        return stop
    @staticmethod
    def no_cache():
        t = Tz.T("ClassicUO.LegionScripting.LegionScripting")
        return bool(Tz.get(None, "LScriptSettings", t).DisableModuleCache)
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
            s.broken = str(ex) + _error_where()
            if not self.stopping(): Kit.say("couldn't load %s (%s)." % (title, s.broken), Kit.HUE_BAD)
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
        jobs, self.load_jobs, todo = self.load_jobs, [], []; jobs, owed, rank = self.compile_ahead(jobs)
        for s in jobs:
            if self.stopping(): break
            if self._load_job(s): todo.append(s)
        todo.sort(key=lambda s: rank[s.key] if s.key in rank else self._start_rank(s)); self.start_all(todo)
        if owed and not todo: safe(lambda: Kit.on_client(self._starts_done))
    def _load_job(self, s):
        ok = self.load(s)
        if not ok and s.enabled and not self.stopping(): s.enabled = False; self.held_on.add(s.key); self.save_prefs()
        if self.config is not None: self.config.loaded(s.key)
        return ok and s.enabled and not s.running and not s.pending_stop
    AHEAD_WAIT = 5.0
    def compile_ahead(self, jobs):
        done, box = [], {"owed": False, "rank": {}}
        try: self._ahead(jobs, done, box)
        except Exception: self.ahead_off = True
        return [s for s in jobs if s not in done], box["owed"], box["rank"]
    def _ahead(self, jobs, done, box):
        if self.settled_at is not None or len(jobs) < 2 or self._poster() is None: return
        import sys; c = sys.__dict__.get("_COMPILED"); c = c if type(c) is dict else {}; texts = self.texts
        def warm(path):
            e = c.get(path); return type(e) is tuple and len(e) == 3 and e[0] == len(texts.get(path) or "")
        rank = dict((s.key, self._start_rank(s)) for s in jobs); order = sorted(jobs, key=lambda s: rank[s.key])
        cold = [s for s in order if s.lazy is not None and not warm(s.lazy)]
        if not cold: return
        box["rank"] = rank
        self.ahead_off = False; left = lambda: [x for x in cold if x.lazy is not None and x.lazy not in self.ahead_ms]
        def ahead(busy):
            while busy() and not self.ahead_off:
                todo = left()
                if not todo: break
                path = todo[0].lazy
                try:
                    text = texts.get(path)
                    if text is None: text = _read_text(path); texts[path] = text
                    t0 = time.time(); self.compiled(text, path); self.ahead_ms[path] = time.time() - t0
                except Exception: self.ahead_off = True
        tail = []
        for s in order:
            if self.stopping() or self.ahead_off: return
            bar = self.bar_on(); go = self._load_job(s)
            if self.bar_on() != bar:
                self.ahead_off = True; box["rank"] = dict((k, 2 if r == 3 else r) for k, r in rank.items())
                if not go: done.append(s)
                return
            if go and (tail or not left()): tail.append(s); continue
            if go: box["owed"] = True; self.start_all((s,), ahead, False)
            done.append(s)
        if tail: box["owed"] = False; self.start_all(tail); done.extend(tail)
    def _poster(self):
        if (Client.MTQ if Client.mtq_looked else Client._find_mtq()) is None or Client.on_client_thread(): return None
        return Client.post
    def _hop(self, fn, ahead):
        post = None if ahead is None or self.ahead_off else self._poster()
        if post is None: return Kit.on_client(fn)
        import _thread; lk, began, done = _thread.allocate_lock(), _thread.allocate_lock(), _thread.allocate_lock()
        began.acquire(); done.acquire(); hop = _Hop(fn); box = {"go": None}; t0 = time.time()
        def run():
            with lk:
                if box["go"] is not None: return
                box["go"] = True
            began.release()
            try: hop.run()
            finally: done.release()
        try: post(run)
        except Exception: self.ahead_off = True; return Kit.on_client(fn)
        try: ahead(lambda: done.locked() and (box["go"] is not None or time.time() - t0 < self.AHEAD_WAIT))
        except Exception: self.ahead_off = True
        if not began.acquire(True, max(0.0, self.AHEAD_WAIT - (time.time() - t0))):
            with lk: late = box["go"] is None; box["go"] = box["go"] or False
            if late: self.ahead_off = True; return Kit.on_client(fn)
        done.acquire()
        if hop.e is not None: raise hop.x if isinstance(hop.x, Exception) else Exception(hop.e)
        return hop.v
    def _start_rank(self, s):
        if s.key == LAYOUT_OWNER: return 0
        if s.key == "actionbar": return 1
        return 3 if self.dock_soon(s.key) else 2
    def load(self, s):
        if s is None: return False
        if s.lazy is not None:
            path = s.lazy; t0 = time.time(); pre = self.ahead_ms.pop(path, None)
            try:
                text = self.texts.pop(path, None) or _read_text(path); t1 = time.time()
                code = self.compiled(text, path); hit, t2 = self.compile_hit, time.time(); exec(code, globals())
                t3 = time.time(); hit = hit and pre is None
                if s.lazy is not None: raise Exception("the file's HOST.add line didn't run")
                for n, a, b in (("read", t0, t1), ("hit" if hit else "compile", t1, t2 if pre is None else t1 + pre),
                                ("exec", t2, t3)):
                    self.split_add(n + ":" + s.key, (b - a) * 1000.0)
            except Exception as ex:
                s.lazy = None; line = getattr(ex, "lineno", None)
                where = (" (%s line %s)" % (os.path.basename(path), line)) if line else _error_where()
                s.api, s.broken = None, "%s%s" % (getattr(ex, "msg", None) or ex, where)
                if not self.stopping(): Kit.say("couldn't load %s (%s)." % (s.title, s.broken), Kit.HUE_BAD)
            if self.boot is not None: d = time.time() - t0; self.boot.append((s.title, d)); self.boot_load += d
        return s.api is not None
    def boot_mark(self, name):
        if self.boot is not None: t = time.time(); self.boot.append((name, t - self.boot_at)); self.boot_at = t
    def boot_done(self):
        boot, self.boot = self.boot, None; t = time.time()
        if self.alone is None: self.backup_start()
        if self.alone is None and self.pref_int("startup", 0) == 1:
            boot.append(("first build", max(0.0, t - self.boot_at - self.boot_load)))
            self.boot_line = "start-up took %.1f s (%s)" % (t - START_AT, ", ".join("%s %d ms" % (n, d * 1000)
                                                                                  for n, d in boot))
        if self.settled_at is not None: self.settle_report()
    def built(self, key):
        b = self.builds
        if self.settled_at is None and (key in b or len(b) < 200): b[key] = b.get(key, 0) + 1
    def settle_tick(self, now):
        if self.alone is not None: self.settled_at = now; self.split_end(); return
        cfg, hub, lay = self.config, self.hub, LAYOUT
        if (self.boot is not None or self.load_jobs or (lay.enabled and lay.loaded and (
                lay.dirty or lay.fresh or lay.fresh_adds or lay.seam_wait)) or (hub is not None and hub.dirty)
                or (cfg is not None and (cfg.request is not None or cfg.request_tab is not None or (
                    cfg.mode == "full" and (cfg.redraw_req or cfg.prof_redraw))))
                or any(safe(fn, False) for fn in self.settle_holds)):
            self.settle_seen = now
        capped = self.ask_g is None and now - (self.settle_from or START_AT) >= self.SETTLE_CAP
        quiet = self.SETTLE_QUIET_HOLD if self.settle_holds else self.SETTLE_QUIET
        if not capped and now - max(self.settle_seen, Kit.churn_at) < quiet: return
        if not capped and safe(lay.plan_prune, False): self.settle_seen = now; return
        self.settled_at, self.settle_capped = now, capped; del self.settle_holds[:]; self.texts.clear()
        self.ahead_ms.clear()
        self.settle_report(); safe(lambda: Kit.on_client(self.front_script_manager))
    def booting(self): return self.settled_at is None
    def settle_hold(self, fn):
        if self.settled_at is None and len(self.settle_holds) < 32: self.settle_holds.append(fn)
    def split_add(self, key, ms):
        sp = self.split
        if sp is not None and (key in sp or len(sp) < self.SPLIT_CAP): sp[key] = ms
    def split_at(self, name):
        s = self.current(); self.split_add("at:" + (name if s is None else s.title), (time.time() - START_AT) * 1000.0)
    def split_end(self):
        self.split = None; G.made = None
        for k in [k for k in G.__dict__ if k.startswith("Create")]: G.__dict__.pop(k, None)
    def split_line(self, sp):
        tot = dict((n, 0.0) for n in ("read", "compile", "hit", "exec")); marks = []
        for k, v in sp.items():
            n = k.split(":", 1)
            if len(n) == 2 and n[0] in tot: tot[n[0]] += v
            elif len(n) == 2 and n[0] == "at": marks.append((v, n[1]))
        hops = int(sp.get("hops", 0)); top = max([(sp.get("hop %d" % i, 0.0), i) for i in range(1, hops + 1)]
                                                 or [(0.0, 0)])
        text = "Splits: read %d ms, compiled %d ms (%d cached), set up %d ms; started in %s (longest %d ms, %s)" % (
            tot["read"], tot["compile"] + tot["hit"], len([k for k in sp if k.startswith("hit:")]), tot["exec"],
            Kit.count(hops, "step"), top[0], Kit.count(int(sp.get("hop %d controls" % top[1], 0)), "control"))
        return text + "".join("; %s ready at %.1f s" % (n, v / 1000.0) for v, n in sorted(marks)) + "."
    @staticmethod
    def front_script_manager():
        if Host.ORDER_OFF in HOST.tz_off: return
        uim = Tz.T("ClassicUO.Game.Managers.UIManager"); node = Tz.get(None, "Gumps", uim).First; n = 0
        while node is not None and n < 2000:
            v = node.Value
            if str(v.GetType().Name) == "ScriptManagerWindow" and not v.IsDisposed:
                Tz.call(None, "MakeTopMostGump", [v], uim); return
            node = node.Next; n += 1
    def settle_report(self):
        line, self.boot_line, sp = self.boot_line, None, self.split
        if self.boot is None: self.split_end()
        if line is None or self.alone is not None: return
        end = ("not settled after %d s" % self.SETTLE_CAP) if self.settle_capped else \
            ("settled at %.1f s" % (self.settled_at - START_AT))
        Kit.say("%s; %s." % (line, end), Kit.HUE_INFO)
        names = sorted((-n, APP_NAME if k == ConfigWindow.DOCK_KEY else safe(lambda: LAYOUT.title_of(k), k))
                       for k, n in self.builds.items() if n > 1)
        text = "Settling: " + Kit.count(sum(self.builds.values()), "window build")
        if names: text += " (%s)" % ", ".join("%s %d" % (t, -n) for n, t in names[:6])
        log = self.config.why_log if self.config is not None else []
        if log: text += ", main window built at " + ", ".join("%.1f s (%s)" % (t - START_AT, self.why_text(w))
                                                              for t, w in log[-3:])
        stale = self.config.stale_log if self.config is not None else []
        if stale: text += ", ignored before any input: " + ", ".join("%s at %.1f s" % (
            self.why_text(w), t - START_AT) for t, w in stale[-3:])
        Kit.say(text + ".", Kit.HUE_INFO)
        if sp: Kit.say(self.split_line(sp), Kit.HUE_INFO)
    WHY_WORDS = {"link": "Settings link", "gear": "gear click", "redraw": "refresh"}
    def why_text(self, why):
        kind, _, arg = str(why).partition(":"); s = dict.get(self.by_key, arg) if arg else None
        if kind == "request": return "%s settings" % (s.title if s is not None else arg)
        if kind == "tab": return "%s tab" % arg.capitalize()
        return self.WHY_WORDS.get(kind, kind)
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
            self.drain(); self.run_due()
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
        msg = str(ex) + _error_where()
        if msg not in s.errors:
            if len(s.errors) >= 50: s.errors.clear()
            s.errors.add(msg); Kit.say("%s error (still running): %s" % (what or s.title, msg), Kit.HUE_BAD)
        self.count_error(s, what, part)
    def count_error(self, s, what=None, part=None, page=False):
        now = time.time()
        if page:
            if 0 <= now - s.page_err_at < 1.0: return
            s.page_err_at = now
        seen = [t for t in s.error_times.get(part, ()) if 0 <= now - t < ERROR_SECS]
        seen.append(now); s.error_times[part] = seen
        if len(seen) < MAX_MODULE_ERRORS or not s.enabled: return
        s.error_times.pop(part, None); Kit.say("%s kept failing and was switched off." % (what or s.title), Kit.HUE_BAD)
        if part is not None and s.parts and s.parts_on.get(part): self.part_set(s.key, part, False)
        else: self.disable(s.key)
    def start(self, s): self.start_all((s,))
    def start_all(self, slots, ahead=None, last=True):
        runs = [r for r in (self._start_prep(s) for s in slots) if r is not None]; n = len(runs); pos = {"i": 0}
        while pos["i"] < n and not self.stopping():
            i = pos["i"]
            try: self._hop(lambda: self._start_hop(runs, pos, n, last), ahead)
            except Exception as ex:
                msg = str(ex) + _error_where(); pos["gone"] = True; hit = False
                for r in runs[i:]:
                    with r["lk"]: began, ended = r["began"], r["ended"]
                    if ended or r["err"] is not None: continue
                    if began or not hit: r["err"] = msg; hit = True
                    else: r["again"] = True
                pos["i"] = n
        for j, r in enumerate(runs):
            if r["again"] or j >= pos["i"]:
                with r["lk"]: r["s"].start_tok = None; r["s"].running = False
        for r in runs: self._start_end(r)
        again = [r["s"] for r in runs if r["again"] and r["s"] not in self.load_jobs]
        if again and not self.stopping(): self.load_jobs[:0] = again
    def _start_prep(self, s):
        if s.running or self.stopping() or not self.load(s): return None
        s.errors, s.error_times = set(), {}; s.pending_stop = False
        import _thread; lk = _thread.allocate_lock()
        run = tok = s.start_tok = {"s": s, "lk": lk, "began": False, "ended": False, "undone": False, "err": None,
                                   "again": False}
        def undo():
            with lk:
                if run["undone"]: return
                run["undone"] = True; began = run["began"]
            if began: safe(lambda: s.api["stop"]())
            safe(lambda: self._unclaim(s))
        def go():
            with lk:
                if s.start_tok is not tok or not s.running or run["began"]: return
                run["began"] = True
            try: s.api["start"]()
            finally:
                with lk: run["ended"] = True; late = s.start_tok is not tok or not s.running
                if late: undo()
        run["undo"], run["go"] = undo, go
        if s.key == "actionbar": self.bar_dead = False
        try: s.running = True; self._arm(s); self._refresh_active()
        except Exception as ex: run["err"] = str(ex) + _error_where()
        return run
    def _start_hop(self, runs, pos, n, last=True):
        t0, m0 = time.time(), G.made
        while pos["i"] < n and not pos.get("gone"):
            r = runs[pos["i"]]; pos["i"] += 1; self._start_go(r)
            if time.time() - t0 >= self.START_HOP: break
        if pos["i"] >= n and not pos.get("gone") and last: self._starts_done()
        sp = self.split
        if sp is not None and m0 is not None:
            h = sp["hops"] = sp.get("hops", 0) + 1; self.split_add("hop %d" % h, (time.time() - t0) * 1000.0)
            self.split_add("hop %d controls" % h, (G.made or m0) - m0)
    def _start_go(self, r):
        s = r["s"]
        if r["err"] is None:
            self._enter(s); self.client_idles = 0
            try: r["go"]()
            except Exception as ex: r["err"] = str(getattr(ex, "InnerException", None) or ex) + _error_where()
            finally: self._leave(s)
        if s.key == "actionbar" and (r["err"] is not None or not self.bar_alive()): self.bar_dead = True
    def _starts_done(self):
        cfg = self.config
        if self.bar_dead and self.alone is None and cfg is not None:
            safe(cfg.dock_sync); safe(self.dock_tick)
    def _start_end(self, r):
        s = r["s"]
        if r["err"] is not None:
            with r["lk"]: s.start_tok = None; s.running = False; began = r["began"]; busy = began and not r["ended"]
            stop = self.stopping()
            if not stop: Kit.say("couldn't start %s (%s)." % (s.title, r["err"]), Kit.HUE_BAD)
            if not busy: r["undo"]()
            if not stop: s.enabled = False; self.save_prefs()
        self._refresh_active(); s.next_due = 0.0; self._page_redraw(s.key)
    def _stop(self, s):
        s.pending_stop = False
        if not s.running: return
        r = s.start_tok; cold = False
        if r is not None:
            with r["lk"]: cold = not r["began"]; s.running = not cold
        self._unclaim(s); self._enter(s)
        try:
            if not cold: s.api["stop"]()
        except Exception: pass
        finally: s.running = False; self._leave(s); self._refresh_active(); self._page_redraw(s.key)
    def _page_redraw(self, key):
        c = self.config
        if c is not None and self.alone is None and c.shown_page == key: c.dirty = key
    def _unclaim(self, s):
        olds = [s.key] + [old for p in s.parts for old in p[4]]
        for k in olds + [p[0] for p in s.parts]: Picker.drop(k)
        if self.cursor_claim[0] in olds: self.cursor_claim = (None, 0.0)
        for k, wait in list(self.hk_wait.items()):
            for w in [w for w in wait if w[2] == s.key]: self.hotkey_off(k, w[0])
        for k, ent in list(self.hk_fns.items()):
            if ent[2] == s.key: self.hotkey_off(k, ent[0])
        pre = s.key + "."; o = self.gump_hold[0]
        if o in olds or str(o).startswith(pre): self.gump_release(o)
        for owner in list(Kit._hooks):
            if owner in olds or str(owner).startswith(pre): Kit.unhook(owner)
    def tick(self, s, hook="tick"):
        s.busy = True; stack = self.stack; stack.append(s); self.client_idles = 0; t0 = time.time()
        try: s.api[hook]()
        except Exception as ex:
            if not self.stopping(): self.report(s, ex)
        finally:
            if stack and stack[-1] is s: stack.pop()
            elif s in stack: stack.remove(s)
            s.busy = False; t1 = time.time(); Host.busy_add(s.load, (t1 - t0) * 1000.0, t1)
        if hook == "tick":
            s.next_due = t1 + Host._ask(s.iv_fn, s.interval)
            s.thread_due = s.has_thread and Host._ask(s.thread_want, True, bool)
        if s.pending_stop: self._stop(s)
    BUSY_T = 10.0
    @staticmethod
    def busy_add(ld, ms, t1):
        d = ld[1] - t1; ld[0] = (ld[0] * math.exp(d / Host.BUSY_T) if d < 0.0 else ld[0]) + ms; ld[1] = t1
        w = ld[2] * 0.98; ld[2] = ms if ms > w else w
    @staticmethod
    def busy_share(ld, now):
        d = ld[1] - now; return (ld[0] * math.exp(d / Host.BUSY_T) if d < 0.0 else ld[0]) / Host.BUSY_T
    @staticmethod
    def _ask(fn, default, cast=None):
        if fn is None: return default
        try: v = fn(); return cast(v) if cast else (v or default)
        except Exception: return default
    def enable(self, key):
        s, part = self.resolve(key)
        if s is None: return
        if self.off_q: self.off_q = [e for e in self.off_q if e[1:] != (s.key, part)]
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
        if self.draining: self.off_q.append((key, s.key, part)); return
        if part is None and s.parts and self.cur_part is not None and self.current() is s \
                and s.parts_on.get(self.cur_part):
            part = self.cur_part
        if part is not None: self.part_set(s.key, part, False); return
        self.held_on.discard(s.key); s.enabled = False; self.save_prefs()
        if s.running:
            s.pending_stop = True
            if not s.busy: self._stop(s)
    def run_due(self):
        if self.shut: return
        if self.profile_req is not None and not self.stack:
            req, self.profile_req = self.profile_req, None; self.profile_job(req); return
        poked, self.poked = self.poked, False; self.pass_id += 1; keys, user = self.poke_keys, self.poke_user
        if keys: self.poke_keys = set()
        else: keys = self.NO_KEYS
        self.poke_user = False; self.pass_keys = keys
        if poked or user: self.ui_next = 0.0
        now = time.time()
        if self.prefs_due: self.prefs_flush()
        if now >= self.tz_at: self.tz_warn()
        if poked or keys or self._client_due(now):
            self.pass_poked, self.pass_all = poked or user, poked
            try: Kit.on_client(self._pass_fn)
            except Exception as ex:
                if not self.stopping(): self._tell("%s: pass error: %s" % (APP_NAME, ex))
            poked, keys = self.pass_all, self.pass_keys
            if self.stopping(): return
            if self.off_q:
                q, self.off_q = self.off_q, []
                for e in q: self.disable(e[0])
            now = time.time()
        if Picker.jobs: Picker.run_blocking()
        for s in self.active:
            if s.pending_stop:
                if s.busy: continue
                self._stop(s)
            elif s.busy or not s.running: continue
            elif not s.on_client and (poked or s.key in keys or now >= s.next_due
                                      or s.next_due - now > self.CLOCK_BACK): self.tick(s)
            elif s.thread_due: s.thread_due = False; self.tick(s, "thread_tick")
            else: continue
            if self.stopping(): return
            self.drain()
        if self.load_jobs and not self.stack: self._run_load_jobs()
        elif self.boot is not None and not self.load_jobs and self.ask_g is None: self.boot_done()
        elif self.marked and self.ask_g is None and not self.load_jobs and all(s.next_due > 0.0 for s in self.active):
            self.unmark()
        cfg = self.config
        if cfg is not None and cfg.prof_stale and not self.stack: cfg.refresh_profiles()
    LOOKAHEAD = HOST_TICK + 0.035; CLOCK_BACK = 60.0; EARLY = 0.008; MOB_AGE = 0.1; PACK_CAP = 6000; PREFS_EVERY = 1.0
    SETTLE_QUIET = 0.25; SETTLE_QUIET_HOLD = 0.5; SETTLE_CAP = 30.0; START_HOP = 0.05; SPLIT_CAP = 300
    ORDER_OFF = "start-up_order"
    def _client_due(self, now):
        if now >= self.ui_next or Picker.jobs or (Kit.pending and self.config is not None): return True
        if self.ui_next - now > UI_TICK and SNAP.pressed(): self.ui_next = now; return True
        if self.ui_next - now > 1.0: self.ui_next = now; return True
        soon = now + self.look
        for s in self.client_run:
            if soon >= s.next_due: return True
            if s.next_due - now > self.CLOCK_BACK: s.next_due = now; return True
        return False
    def drain(self, hop=False):
        lk = self._drain_lk
        if not lk.acquire(False): return
        try:
            if hop: self.draining = True
            API.ProcessCallbacks()
        except Exception: pass
        finally:
            if hop: self.draining = False
            lk.release()
    FRAME_MIN = 1.0 / 60; NAP_MIN = 0.002
    def nap(self, began):
        now = time.time()
        if (self.poked or self.poke_keys or self.poke_user or (Kit.pending and self.config is not None)
                or Picker.due() or 0 <= now - self.input_at <= self.INPUT_FAST):
            self.look = self.EARLY; return max(self.NAP_MIN, self.FRAME_MIN - max(0.0, now - began))
        self.look = self.LOOKAHEAD; return HOST_TICK
    def _stop_free(self):
        f = self._stop_fi
        if f is None:
            try:
                from System.Reflection import BindingFlags
                f = API.GetType().GetField("_onStopScheduled", BindingFlags.NonPublic | BindingFlags.Instance)
            except Exception: f = None
            f = self._stop_fi = f or False
        if f is False: return False
        try: return not f.GetValue(API)
        except Exception: return False
    def _drop_offs(self):
        q, self.off_q = self.off_q, []
        for e in q:
            s = dict.get(self.by_key, e[1])
            if s is None: continue
            if e[2] is not None: s.parts_on[e[2]] = False
            if e[2] is None or not s.parts_wanted(): s.enabled = False; self.held_on.discard(s.key)
    def _client_pass(self, poked=None):
        self.in_hop = True
        try:
            self.client_idles = 0
            if self._stop_free(): self.drain(True)
            if self.stopping(): return
            if poked is None: poked = self.pass_all
            keys = self.pass_keys; offs = set(e[1] for e in self.off_q if e[2] is None) if self.off_q else ()
            if Kit._texts_sweep: Kit._prune_texts()
            self.ui_pending(); self.fight_sample(time.time())
            if Picker.jobs:
                try: Picker.tick()
                except Exception as ex: self._tell("%s: target cursor error: %s" % (APP_NAME, ex))
            now = time.time()
            for s in self.client_run:
                if s.running and not s.busy and not s.pending_stop and s.key not in offs and (poked or s.key in keys
                        or now + self.EARLY >= s.next_due or s.next_due - now > self.CLOCK_BACK):
                    self.tick(s)
                    if self.stopping(): return
            self.ui_tick()
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
    def harm_ok(self, serial, key, title, harmful=None, again="press again to confirm", odd=False, now=None):
        if harmful is None:
            try: harmful = bool(API.HasTarget("harmful"))
            except Exception: harmful = False
        if not harmful: return True
        gz = self.guarded()
        if gz is False: return True
        try: m = API.FindMobile(serial) if serial else None
        except Exception: m = None
        noto = Kit.noto_name(m) if m is not None else ("odd" if odd and serial else "unknown")
        if noto not in HARM_NOTO: return True
        now = time.time() if now is None else now; c = self.harm_conf
        if c[0] == key and c[1] == serial:
            age = now - c[2]
            if 0 <= age < Kit.TWICE: self.harm_conf = (key, serial, now); return False
            if HARM_DOUBLE <= age <= HARM_SECS: self.harm_conf = (None, 0, 0.0); return True
        self.harm_conf = (key, serial, now)
        try: name = str(m.Name or "") if m is not None else ""
        except Exception: name = ""
        who = "%s is %s" % (name or "they", "green" if noto == "ally" else "blue") if m is not None else \
            "your target is not a mobile"
        API.SysMsg("%s: %s and you %s in a guard zone: %s." % (title, who, "are" if gz else "may be", again),
                   Kit.HUE_BAD)
        if m is not None: API.HeadMsg("* %s *" % again, serial, 0x22)
        return False
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
    def fight_sample(self, now):
        try: p = self.me(); who = int(p.Serial); hits = int(p.Hits)
        except Exception: return
        if who != self.hurt_who: self.hurt_hp = None; self.hurt_who = who
        if self.hurt_hp is not None and hits < self.hurt_hp: self.hurt_until = now + HURT_SECS
        self.hurt_hp = hits
    def fight_hold(self, now=None):
        if now is None: now = time.time()
        dead = war = False; p = None
        try: p = self.me(); dead = bool(p.IsDead); war = bool(p.InWarMode)
        except Exception: pass
        if dead: return "dead"
        if war: return "war"
        if self.attack_rd is None: self.attack_rd = Journal.reader()
        else:
            mine = None
            for ln in self.attack_rd.new():
                if ln.hue != ATTACK_HUE or str(ln.kind).upper() == "CLIENT": continue
                m = Journal.ATTACK_RE.search(ln.text)
                if m is None: continue
                if mine is None:
                    try: mine = str(p.Name or "").strip().lower() or None
                    except Exception: mine = None
                sp = str(ln.name or "").strip().lower()
                if sp in ("", "system", m.group(1).strip("* ").lower()) or (mine is not None and sp == mine):
                    self.attacked_until = max(self.attacked_until, min(ln.at, now) + HURT_SECS)
        if 0 < self.hurt_until - now <= HURT_SECS: return "hurt"
        if 0 < self.attacked_until - now <= HURT_SECS: return "attacked"
        if self.foe_near(): return "foe"
        if Kit.held_item(): return "item"
        up = self.services.get("attention.up")
        if safe(up) if up is not None else self.alarm_up(): return "alarm"
        return None
    def me(self):
        if self.in_hop and self._me_pid == self.pass_id: return self._me
        try: p = API.Player
        except Exception: p = None
        m = _Memo(p) if p is not None else None
        if self.in_hop: self._me_pid = self.pass_id; self._me = m
        return m
    def _mob_scan(self):
        if self._mob_pid == self.pass_id and (self.in_hop or time.time() - self._mob_at <= self.MOB_AGE):
            return self._mob_list
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
        self._mob_pid, self._mob_list, self._mob_at = self.pass_id, out, time.time(); return out
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
        bp = API.Backpack
        lst = list((API.FindTypeAll(0xFFFFFFFF, bp) if k else API.ItemsInContainer(bp, False)) or []) if bp else []
        if bp and self._pack_hook["on"]:
            try: ks = set(int(i.Serial) for i in lst); ks.add(int(bp))
            except Exception: ks = set()
            if not k and len(self._pack_keys) <= self.PACK_CAP: ks |= self._pack_keys
            self._pack_keys = ks if len(ks) <= self.PACK_CAP else set([int(bp)])
        self._pack[k] = (self.pass_id if self.in_hop else -1, now, lst); return list(lst)
    def pack_dirty(self): self._pack.clear()
    def pack_ver(self):
        Kit.hook_once(self._pack_hook, "on", ("OnItemCreated", self._pack_fn), ("OnItemUpdated", self._pack_fn),
                      owner=None)
        return self._pack_v
    def _pack_event(self, *args):
        keys = self._pack_keys
        for a in args:
            try: s, c = int(a.Serial), int(a.Container)
            except Exception: continue
            if c in keys or s in keys: self._pack_v += 1; self._pack.clear()
            return
    def pick_target(self, timeout, on_done, owner=None): Picker.ask(timeout, on_done, owner)
    def ui_pending(self):
        if self.ui_busy or not Kit.pending: return
        self.ui_busy = True
        try:
            while Kit.pending:
                lst, Kit.pending = Kit.pending, []
                for fn in lst: safe(fn)
        finally: self.ui_busy = False
    def ui_tick(self):
        self.ui_pending()
        if self.ui_busy: return
        self.ui_busy = True
        try:
            now = time.time()
            if now >= self.ui_next:
                boot = self.settled_at is None; self.ui_next = now + (0.0 if boot else UI_TICK)
                if not VA_ALONE and now >= self.alive_at:
                    self.alive_at = now + 1.0; API.SetSharedVar(ALIVE_KEY, str(now))
                try: ALERTS.tick(now)
                except Exception as ex: self._tell("%s: alert error: %s%s" % (APP_NAME, ex, _error_where()))
                try: GUARD.tick(now)
                except Exception as ex: self._tell("%s: guard-zone error: %s%s" % (APP_NAME, ex, _error_where()))
                if self.config is not None: self.config.poll()
                if self.hub is not None: self.hub.poll()
                self.dock_tick(); SNAP.tick()
                if FADE.on:
                    try: FADE.tick(now)
                    except Exception as ex: self._tell("%s: fade error: %s%s" % (APP_NAME, ex, _error_where()))
                if now - self.input_at > UI_IDLE_AFTER and not (boot or SNAP.down or LAYOUT.arrange):
                    self.ui_next = now + UI_IDLE
                if self.grid is not None: self.grid.tick()
                if self.whats_new.g is not None: self.whats_new.poll()
                if self.alert_log.g is not None: self.alert_log.poll(now)
                if self.launcher is not None and self.launcher.g is not None: self.launcher.poll(now)
                if self.ask_g is not None: self.ask_poll()
        except Exception as ex:
            msg = "%s: settings window error: %s%s" % (APP_NAME, ex, _error_where())
            if not self.stopping(): self._tell(msg)
        finally: self.ui_busy = False
    def load_prefs(self):
        prefs = self.prefs = Kit.codec_load(Kit.get_var(SETTINGS_KEY))
        on = [k for k in prefs.get("modules", "").split(",") if k]
        seen = set(k for k in prefs.get("seen", "").split(",") if k); was = prefs.get("seen", "")
        changed = self._migrate_parts(prefs, on, seen); held = self.held_on = set(); self.held_parts = set()
        for s in self.slots:
            if s.default_on and s.key not in seen: on.append(s.key); seen.add(s.key); self._parts_fill(s)
            s.enabled = s.key in on and (s.api is not None or s.lazy is not None)
            if s.key in on and not s.enabled: held.add(s.key)
            if s.enabled: self._parts_fill(s)
        prefs["seen"] = ",".join(sorted(seen)); self._apply_style()
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
                for p in s.parts:
                    if p[4]: s.parts_on[p[0]] = any(k in on_set for k in p[4])
                    else: s.parts_on[p[0]] = mine is not None and p[0] in mine
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
    def save_prefs(self, now=False):
        if self.config is not None: self.config.box_hit = True
        if self.prefs_busy or self.alone is not None: return None
        mods, parts, off = [], [], []
        for s in self.slots:
            if not s.enabled and s.key not in self.held_on:
                for p in s.parts:
                    if s.parts_on.get(p[0]) or (s.key, p[0]) in self.held_parts: off.append("%s.%s" % (s.key, p[0]))
                continue
            mods.append(s.key)
            for p in s.parts:
                if s.parts_on.get(p[0]) or (s.key, p[0]) in self.held_parts:
                    parts.append("%s.%s" % (s.key, p[0]))
                    for old in p[4]:
                        if old not in mods: mods.append(old)
        for name, have in (("modules", mods), ("parts", parts), ("parts_off", off)):
            for k in str(self.prefs.get(name, "") or "").split(","):
                mk = k.partition(".")[0]; s = dict.get(self.by_key, mk)
                if not k or mk in RETIRED_KEYS: continue
                out = have if s is None else parts if mk in mods else off
                keep = s.broken is not None and not s.parts and name != "modules" if s else mk not in self.old_map
                if keep and k not in out: out.append(k)
        self.prefs["modules"] = ",".join(mods); self.prefs["parts"] = ",".join(parts)
        self.prefs["parts_from"] = self.prefs["modules"]
        if off: self.prefs["parts_off"] = ",".join(off)
        else: self.prefs.pop("parts_off", None)
        if self.config is not None: self.config.store_prefs(self.prefs)
        if self.hub is not None: self.hub.store_prefs(self.prefs)
        data = ";".join("%s=%s" % (k, v) for k, v in sorted(self.prefs.items())); t = time.time()
        if self.prefs_frozen:
            if not self.prefs_told:
                self.prefs_told = True
                Kit.say("couldn't save settings this session (a modules folder couldn't be read); the saved ones "
                        "are kept.", Kit.HUE_BAD)
            return data
        if not now and 0 < self.prefs_at - t <= self.PREFS_EVERY: self.prefs_due = True; return data
        self.prefs_due = False; self.prefs_at = t + self.PREFS_EVERY; Kit.put_var(SETTINGS_KEY, data)
        return data
    def prefs_flush(self, force=False):
        if self.prefs_due and not (self.prefs_frozen or self.prefs_busy) and (
                force or not 0 < self.prefs_at - time.time() <= self.PREFS_EVERY):
            self.save_prefs(True)
    def profile_job(self, req):
        kind, name = req
        try: getattr(self, "_profile_" + kind)(name)
        except Exception as ex:
            what = {"fav": "set the favourite profile", "backup": "save the backup",
                    "restore": "restore the backup"}.get(kind, kind + " the profile")
            Kit.say("couldn't %s (%s%s)." % (what, Tz.why(ex), _error_where()), Kit.HUE_BAD)
        if kind not in ("load", "restore", "backup") and self.config is not None and not self.stopping():
            self.config.refresh_profiles()
            if self.config.mode == "full": self.config.prof_redraw = False; self.config.redraw()
    def _profile_save(self, name):
        name = PROFILES.clean(name)
        if not name: raise Exception("type a name for the profile in the box")
        Kit.say('saving profile "%s".' % name, Kit.HUE_INFO); data = self.save_prefs(True)
        stamp, n, saved, failed = PROFILES.save(name, data); fav = PROFILES.favorite()
        PROFILES.set_state("fav" if name == fav else "pick", name, stamp)
        if name == fav:
            try: PROFILES.set_client_default(name)
            except Exception as ex: failed.append("TazUO default for new characters (%s)" % Tz.why(ex))
        if self.config is not None: self.config.prof_sel = name
        PROFILES.report(name, "saved", n, True, saved, failed)
    def _profile_load(self, name):
        if PROFILES.info(name) is None: raise Exception('there is no profile "%s"' % name)
        Kit.say('loading profile "%s".' % name, Kit.HUE_INFO)
        result = self._reload(lambda: PROFILES.apply(name, "fav" if name == PROFILES.favorite() else "pick"), name)
        PROFILES.report(name, "loaded", *result)
    def _reload(self, apply, sel=None):
        self.prefs_flush(True); self.prefs_busy = True
        if ALERTS.log_due: ALERTS.save_log(time.time())
        try:
            if self.config is not None: safe(self.config.close)
            for s in self.slots:
                if s.running: self._stop(s)
            if self.hub is not None: safe(self.hub.close)
            Kit._vars.clear(); result = apply()
            for c in set(Binds.saved.values()) | Binds.hooked: Binds.unhook(c)
            Binds.saved.clear(); Binds.loaded = False; self._zone_was_d = None; Kit._vars.clear()
            ALERTS.load(); WhatsNew.seen_keys = None; GUARD.saved = None; Kit.read_screen(); Binds.load()
            for s in self.slots:
                if s.api is not None and s.lazy is None and s.factory is not None:
                    try: s.api = s.factory(); s.broken = None
                    except Exception as ex:
                        s.api, s.broken = None, str(ex) + _error_where()
                        Kit.say("couldn't load %s (%s)." % (s.title, s.broken), Kit.HUE_BAD)
            self.load_prefs(); self.tz_check(); LAYOUT.load()
        finally:
            self.prefs_busy = False
            try:
                self.config = ConfigWindow(self)
                if sel is not None: self.config.prof_sel = sel
                self.config.open()
            except Exception as ex:
                self._tell("%s: couldn't build the window: %s%s" % (APP_NAME, ex, _error_where()))
                if self.config is None or self.config.closing: self.config = safe(lambda: ConfigWindow(self))
                if self.config is not None: safe(lambda: self.config.build_gear(self.config.gx, self.config.gy))
            self.hub = safe(lambda: HubWindow(self))
            if self.grid is not None: safe(self.grid.show if self.pref_int("grid_on", 0) == 1 else self.grid.hide)
            self.start_all(sorted([s for s in self.slots if s.enabled], key=self._start_rank)); Kit.note_screen()
        return result
    def backup_start(self):
        try: self.backups.scan()
        except Exception: self.backups.items = []
        self.refresh_settings(BACKUP_PAGE)
        if Kit.get_var(BackupPage.VER_KEY) != APP_VERSION and self.profile_req is None:
            self.profile_req = ("backup", BackupPage.AUTO % APP_VERSION)
    def _profile_backup(self, why, keep=None):
        if ALERTS.log_due: ALERTS.save_log(time.time())
        auto = why == BackupPage.AUTO % APP_VERSION
        name, n = self.backups.make(why, self.save_prefs(True), keep, self.early_backup if auto else None)
        if auto: Kit.put_var(BackupPage.VER_KEY, APP_VERSION); self.early_backup = None
        self.backups.scan(); self.refresh_settings(BACKUP_PAGE)
        API.SysMsg("Backups: saved %s (%s)." % (Kit.count(n, "setting"), BackupPage.label(name)), Kit.HUE_GOOD)
    def _profile_restore(self, name):
        va, lay = self.backups.read(name)
        if not va: raise Exception("that backup is empty")
        self._profile_backup("before restore", name); gone = list(BackupPage.snapshot(""))
        API.SysMsg("Backups: restoring %s." % BackupPage.label(name), Kit.HUE_INFO)
        ok = self._reload(lambda: BackupPage.apply(va, lay, gone)); self.backups.scan()
        self.refresh_settings(BACKUP_PAGE)
        API.SysMsg("Backups: restored %s from %s." % (Kit.count(len(va), "setting"), BackupPage.label(name)),
                   Kit.HUE_GOOD)
        if not ok:
            API.SysMsg("Backups: some settings were still saving; restart Virtue Assistant if a module looks "
                       "unchanged.", Kit.HUE_BAD)
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
    def hold(self, s, part=None):
        if part is not None:
            if not s.parts_on.get(part): return
            s.parts_on[part] = False; self.held_parts.add((s.key, part))
            if s.parts_wanted(): return
        if s.enabled: s.enabled = False; self.held_on.add(s.key); s.pending_stop = s.running
    TZ_GONE = "TazUO changed %s; %s %s off until the next Virtue Assistant."
    def tz_check(self):
        self.tz_at = 0.0; self.tz_off = set()
        for name, keys in safe(Tz.missing, ()):
            titles = []
            for key in keys:
                s, part = self.resolve(key)
                if s is None and "_" not in key: continue
                t = key.replace("_", " ") if s is None else s.part_title(part)
                if t not in titles: titles.append(t)
                if s is not None: self.hold(s, part)
                else: self.tz_off.add(key)
            if titles:
                Kit.say(self.TZ_GONE % (name, ", ".join(titles), "are" if len(titles) > 1 else "is"), Kit.HUE_BAD)
    TZ_KEY = "TazUO_settings_check"; TZ_EVERY = 60.0; TZ_LINE = "TazUO's \"%s\" is on; %s. Switch it off in %s."
    TZ_RULE = "it %s by itself, which this shard's rules don't allow"; TZ_AL = "Legion Assistant > Agents > Auto Loot"
    TZ_SOON = 5.0
    TZ_SETS = (("EnableAutoLoot", "Enable Auto Loot", TZ_RULE % "loots", TZ_AL),
               ("AutoLootHumanCorpses", "Auto Loot Human Corpses",
                "it loots players' corpses by itself, which can flag you criminal", TZ_AL),
               ("EnableScavenger", "Enable Scavenger", TZ_RULE % "picks up items",
                "Legion Assistant > Agents > Scavenger"))
    def tz_warn(self):
        self.tz_at = time.time() + self.TZ_EVERY
        if self.alone is not None or self.TZ_KEY in self.tz_off or self.pref_int("tz_quiet", 0) == 1: return
        on = safe(self.tz_on, ())
        if on is None: self.tz_at = time.time() + self.TZ_SOON; return
        for name, label, why, where in self.TZ_SETS:
            if name in on and name not in self.tz_told:
                self.tz_told.add(name); Kit.say(self.TZ_LINE % (label, why, where), Kit.HUE_BAD)
    def tz_on(self):
        cur = Tz.get(None, "CurrentProfile", Tz.T("ClassicUO.Configuration.ProfileManager"))
        if cur is None: return None
        on = set(sp[0] for sp in self.TZ_SETS if bool(Tz.get(cur, sp[0])))
        if "EnableAutoLoot" not in on: on.discard("AutoLootHumanCorpses")
        if "EnableScavenger" in on:
            on.discard("EnableScavenger")
            with Kit.quiet:
                sm = Tz.get(None, "Instance", Tz.T("ClassicUO.Game.Managers.ScavengerManager"))
                if bool(Tz.get(sm, "IsLoaded")) and int(Tz.get(sm, "ScavengerEntries").Count) > 0:
                    on.add("EnableScavenger")
        return on
    def mark_start(self):
        was = Kit.get_var(START_KEY) == "1"; Kit.put_var(START_KEY, "1"); self.marked = True; return was
    def unmark(self, stop=False):
        if self.marked and self.ask_g is None and (not stop or safe(lambda: bool(API.StopRequested), False)):
            self.marked = False; Kit.put_var(START_KEY, "")
    def start_on(self):
        if self.settled_at is None: self.settle_from = self.settle_from or time.time(); safe(LAYOUT.plan)
        self.load_jobs.extend(sorted((s for s in self.slots if s.enabled and s not in self.load_jobs),
                                     key=lambda s: s.key != LAYOUT_OWNER))
    SAFE_ASK = "Virtue Assistant didn't finish starting last time. Start with every module off?"
    SAFE_DONE = "every module is off for now; tick them on one at a time on the Modules tab (%s)."
    SAFE_BUTTONS = (("normal", Kit.ART_PLAY, "Start normally", "Turn on the modules you had on"),
                    ("safe", Kit.ART_PLAY, "Start safely", "Keep every module off for now"))
    def ask_open(self):
        if self.config is None: return False
        with Kit.quiet: Kit.on_client(lambda: Binds.scoped("va.safe", self._ask_build))
        return self.ask_g is not None
    def _ask_build(self):
        M, W = Kit.MARGIN, 420; lines = Kit.wrap(self.SAFE_ASK, W - 2 * M - 24); n = len(lines)
        h = 48 + 20 * n; yb = M + 30 + Kit.GAP; H = yb + h + M; self.ask_store = ({}, {})
        g = G.CreateGump(True, True); Kit.add_window_frame(g, W, H); Kit.add_section(g, M, M, W - 2 * M, 30)
        Kit.add_label(g, "SAFE START", M + 30, M + 7, Kit.HUE_TITLE); Kit.add_section(g, M, yb, W - 2 * M, h)
        for i, line in enumerate(lines): Kit.add_label(g, line, M + 12, yb + 8 + 20 * i, Kit.HUE_TEXT)
        Kit.buttons(g, self.ask_store, M + 12, yb + 14 + 20 * n, self.SAFE_BUTTONS)
        sw, sh = Kit.screen(); Kit.place(g, max(0, ((sw or 1024) - W) // 2), max(0, ((sh or 768) - H) // 3), W, H)
        Kit.add_front(g); self.ask_g = g
    def ask_poll(self):
        st = self.ask_store; safe_on = Kit.was_clicked(st, "safe")
        if not (safe_on or Kit.was_clicked(st, "normal") or not Kit.is_open(self.ask_g)): return
        g, self.ask_g = self.ask_g, None; Kit.dispose(g)
        if safe_on:
            names = [s.title for s in self.slots if s.enabled]
            for s in self.slots: self.hold(s)
            Kit.say(self.SAFE_DONE % (", ".join(names) or "none"), Kit.HUE_INFO)
        self.start_on(); self.poke()
    def run(self):
        ask = self.mark_start(); Client.find()
        if Client.mouse is None:
            Kit.say("no client mouse timer; double-clicks use the client's own event.", Kit.HUE_INFO)
        self.early_backup = BackupPage.early(); self.load_prefs(); ALERTS.load(); self.tz_check()
        Kit.read_screen(); LAYOUT.load(); SNAP.on_drop(LAYOUT.dropped)
        API.OnStop(self.shutdown); self.grid = Grid(self)
        self.launcher = Launcher(self); self.services["launcher.open"] = self.launcher.toggle; why = None
        try: self.config = ConfigWindow(self); self.config.refresh_profiles()
        except Exception as ex: why = ex
        safe(self.whats_new.due); self._front_hop(ask, why); self.boot_mark("main window"); self.loop()
    def _front_hop(self, ask, why):
        how, v = Client.on_main_ex(lambda: self._front(ask, why))
        if how == "no": self._front(ask, why)
        elif how == "err" and Client.exc is not None: raise Client.exc
    def _front(self, ask, why):
        try:
            if why is not None: raise why
            self.config.open(True)
        except Exception as ex:
            self._tell("%s: couldn't build the window: %s%s" % (APP_NAME, ex, _error_where()))
            if self.config is None: self.config = safe(lambda: ConfigWindow(self))
            if self.config is not None: safe(lambda: self.config.build_gear(self.config.gx, self.config.gy))
        try: self.hub = HubWindow(self)
        except Exception as ex:
            self._tell("%s: couldn't make the Ultima Tracker window: %s%s" % (APP_NAME, ex, _error_where()))
        if self.pref_int("grid_on", 0) == 1: safe(self.grid.show)
        names = [s.title for s in self.slots if s.enabled]
        API.SysMsg("%s %s running. %s" % (APP_NAME, APP_VERSION, ("On: " + ", ".join(names) + ".") if names else
                   "Tick a module on the Modules tab."), Kit.HUE_GOOD)
        API.SetSharedVar(ALIVE_KEY, str(time.time())); Binds.load()
        if not ask or not self.ask_open(): self.start_on()
        Kit.note_screen()
        try: self.whats_new.open()
        except Exception as ex: self._tell("%s: couldn't make the What's new window: %s" % (APP_NAME, ex))
    def run_alone(self, s):
        if self.suite_alive():
            API.SysMsg("%s: %s is running; use %s there." % (s.title, APP_NAME, s.title), Kit.HUE_BAD); return
        self.alone, self.prefs_frozen = s, True; Client.find(); self.load_prefs(); Kit.read_screen()
        API.OnStop(self.shutdown); self.config = AlonePage(s); self.hub = safe(lambda: HubWindow(self))
        on = set(k for k in Kit.get_var(ALONE_PARTS % s.key, "").split(",") if k)
        if s.parts and on:
            met = any(k[:1] == "!" for k in on); seen = Kit.get_var("VirtueAssistant_new_parts", "").split(",")
            s.parts_on = dict((p[0], p[0] in on or ("!" + p[0] not in on and bool(p[3]) and (
                met or len(p) > 5 and bool(p[5]) and p[0] not in seen))) for p in s.parts)
        API.SysMsg("%s: running alone, without the rest of %s." % (s.title, APP_NAME), Kit.HUE_GOOD)
        Binds.load(); self.enable(s.key); self.loop()
    def loop(self):
        try:
            while not self.stopping() and (self.alone is None or self.alone.enabled):
                began = time.time(); self.drain()
                try:
                    self.run_due()
                    if self.settled_at is None: self.settle_tick(time.time())
                except Exception as ex:
                    if self.stopping(): break
                    self._tell("%s: main loop error: %s%s" % (APP_NAME, ex, _error_where()))
                API.Pause(self.nap(began))
        finally: self.shutdown()
    def shutdown(self):
        if self.shut: return
        self.shut = self.quitting = True; safe(Picker.drop); self.unmark(True)
        if self.off_q: self._drop_offs()
        if not VA_ALONE:
            safe(lambda: API.RemoveSharedVar(ALIVE_KEY))
            safe(lambda: Kit.on_client(LAYOUT.game_view_restore)); safe(lambda: LAYOUT.set_arrange(False, tell=False))
            safe(lambda: Kit.on_client(LAYOUT._tabs_off)); safe(LAYOUT.situ_park)
            safe(lambda: Kit.on_client(lambda: [cw.free() for cw in list(ClientWin.found.values()) + [
                LAYOUT.journal_held] if cw is not None]))
        if self.config is not None: safe(lambda: self.save_prefs(True)); safe(self.config.close)
        else: safe(lambda: self.prefs_flush(True))
        for s in reversed(self.slots):
            if s.running:
                try: self._stop(s)
                except Exception: s.running = False
        self._refresh_active()
        if self.hub is not None: safe(self.hub.close)
        if self.launcher is not None: safe(self.launcher.close)
        for fn in (self.alert_log.close, ALERTS.close, self.whats_new.close, GUARD.store, Kit.note_screen,
                   lambda: Kit.dispose(self.ask_g), lambda: Kit.unhook(None)):
            safe(fn)
        if self.grid is not None: safe(self.grid.hide)
        safe(lambda: API.SysMsg("%s stopped." % APP_NAME, Kit.HUE_INFO))


class PartSet(object):
    OFF_LINE = "%s is off: tick it under PARTS to see its settings."
    def __init__(self, key, title, parts, shared=None):
        self.key = key; self.specs = [[sp[0], sp[1], float(sp[2]), sp[3] if len(sp) > 3 else None] for sp in parts]
        self._owner = {sp[0]: sp[3] or ("%s.%s" % (key, sp[0])) for sp in self.specs}
        self._iv = {sp[0]: sp[2] for sp in self.specs}; self._fns = {}; self.api = {}; self.running = []; self.due = {}
        self.thread_due = {}; self.want = self._slot = None; self.busy = 0; self.stopping = False; self.load = {}
        self.shared = shared or {}
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
        if pk not in self.load: self.load[pk] = [0.0, 0.0, 0.0]
        self.running.append(pk); self._sync_slot()
        self.due[pk] = 0.0; self.thread_due[pk] = False; s = self.slot()
        if s is not None: s.next_due = 0.0; s.part_load = self.load
        fn = api.get("start"); err = None
        if not fn: return
        was = (HOST.cur_part, HOST.cur_owner); HOST.cur_part, HOST.cur_owner = pk, self.owner(pk); self.busy += 1
        try: fn()
        except Exception as ex: err = str(ex) + _error_where()
        finally: self.busy -= 1; HOST.cur_part, HOST.cur_owner = was
        if err is None or s is None or HOST.stopping(): return
        Kit.say("couldn't start %s (%s)." % (s.part_title(pk), err), Kit.HUE_BAD); self.stop_part(pk)
        HOST.part_set(self.key, pk, False)
    def stop_part(self, pk):
        if pk not in self.running: return
        self.running.remove(pk); self._sync_slot()
        owner = self.owner(pk); Picker.drop(owner); HOST.release_cursor(owner); self._call(pk, "stop")
        Kit.unhook(owner)
    def wanted(self): s = self.slot(); return set(s.parts_wanted()) if s is not None else set()
    def reconcile(self, want=None):
        if want is None: want = self.wanted()
        if self.busy: self.want = set(want); return
        self.want = None; s = self.slot()
        for sp in self.specs:
            pk = sp[0]
            if pk in want and pk not in self.running and (s is None or s.parts_on.get(pk)): self.start_part(pk)
        for pk in list(reversed(self.running)):
            if pk not in want: self.stop_part(pk)
    def _start(self): self.stopping = False; self.reconcile()
    _NOFN = (None, False, None)
    def _tick(self):
        now = time.time(); poked = HOST.pass_poked; running = self.running; due = self.due; load = self.load
        keys = HOST.pass_keys if self.key in HOST.pass_keys else None
        for pk in list(running):
            if pk not in running: continue
            d = due.get(pk, 0.0)
            if poked or now + Host.EARLY >= d or d - now > Host.CLOCK_BACK or (
                    keys is not None and self.key + "." + pk in keys):
                t0 = time.time(); self._call(pk, "tick"); t1 = time.time()
                Host.busy_add(load[pk], (t1 - t0) * 1000.0, t1); nxt, has_thread, want = self._fns.get(pk, self._NOFN)
                due[pk] = t1 + Host._ask(nxt, self._iv.get(pk, 0.1))
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
                self.thread_due[pk] = False; t0 = time.time(); self._call(pk, "thread_tick"); t1 = time.time()
                Host.busy_add(self.load[pk], (t1 - t0) * 1000.0, t1)
        if self.want is not None and not self.busy: Kit.on_client(self.reconcile)
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
            elif s is not None and s.part(pk) and len(s.part(pk)) > 2 and s.part(pk)[2]:
                tx = x + 8 + Kit.text_w(title.upper()) + 14
                Kit.add_label(g, Kit.fit(s.part(pk)[2], max(20, x + w - 12 - tx)), tx, y + 6, Kit.HUE_INFO)
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
        h = {"start": self._start, "tick": self._tick, "stop": self._stop, "client_tick": True,
             "thread_tick": self._thread_tick, "thread_wanted": self._thread_wanted, "interval": self._interval,
             "parts": self.reconcile, "config_height": self._config_height, "build_config": self._build_config,
             "poll_config": self._poll_config, "config_closed": self._config_closed}
        sh = self.shared
        if not sh: return h
        def tick(): self._tick(); sh["tick"]()
        def stop():
            try: self._stop()
            finally: sh["stop"]()
        def thread_tick(): self._thread_tick(); sh["thread_tick"]()
        def thread_wanted(): return bool(sh["thread_wanted"]()) or self._thread_wanted()
        wrap = {"tick": tick, "stop": stop, "thread_tick": thread_tick, "thread_wanted": thread_wanted}
        h.update((k, wrap[k]) for k in sh); return h


class Tz(object):
    _types = {}; _MISS = object()
    NEED = (("LegionScripting.LegionAPI", "_onStopScheduled", "early_event_handling"),
        ("LegionScripting.LegionAPI", "World", "actionbar meters social"),
        ("Game.GameActions", "", "actionbar social skills.window"), ("Game.GameActions", "DropItem", "inventory.bags"),
        ("Game.GameActions", "Equip QueueEquipSwap", "inventory.paperdoll"),
        ("Game.Managers.UIManager", "Gumps", "actionbar grimoire interface hud inventory.bags skills.window social"),
        ("Game.Managers.UIManager", "ContainerScale", "inventory.bags"),
        ("Game.Managers.UIManager", "KeyboardFocusControl _gumpsStructureVersion SystemChat", "interface"),
        ("Game.Managers.UIManager", "MakeTopMostGump", "hud skills.window"),
        ("Game.Managers.UIManager", "Gumps MakeTopMostGump _gumpsStructureVersion TopMostControl", "start-up_order"),
        ("Game.Managers.UIManager", "Add", "skills.window"),
        ("Game.Managers.UIManager", "IsMouseOverWorld", "worldmap.pings"),
        ("Game.Managers.MacroManager", "GetAllMacros SetMacroToExecute Update FindMacro", "actionbar"),
        ("Game.Managers.MacroObject", "Items", "actionbar"),
        ("LegionScripting.LegionScripting", "LoadedScripts", "actionbar"),
        ("Input.Keyboard", "KeyDownEvent KeyUpEvent", "actionbar"),
        ("Input.Mouse", "CancelDoubleClick", "inventory.bags"),
        ("Input.Mouse", "Position MClickPosition MButtonPressed", "worldmap.pings"),
        ("Game.World", "Macros", "actionbar"), ("Game.World", "Instance Get TargetManager", "hud.frames"),
        ("Game.World", "TargetManager", "meters"),
        ("Game.World", "Instance Player SkillsGroupManager", "skills.window"), ("Game.World", "Party Player", "social"),
        ("Game.Managers.TargetManager", "LastAttack", "hud.frames meters"),
        ("Client", "Game", "hud.frames inventory.bags inventory.paperdoll social"),
        ("GameController", "UO", "hud.frames inventory.bags inventory.paperdoll social"),
        ("UltimaOnline", "Animations FileManager", "hud.frames"),
        ("UltimaOnline", "GameCursor", "inventory.bags inventory.paperdoll"), ("UltimaOnline", "World", "social"),
        ("Game.GameCursor", "ItemHold", "inventory.bags"),
        ("Game.ItemHold", "Enabled IsFixedPosition Serial Graphic Hue Container MouseOffset DisplayedGraphic",
         "inventory.bags"), ("Configuration.ProfileManager", "CurrentProfile",
         "hud.frames inventory.bags inventory.storage TazUO_settings_check"),
        ("Configuration.Profile", "EnableAutoLoot AutoLootHumanCorpses EnableScavenger", "TazUO_settings_check"),
        ("Game.Managers.ScavengerManager", "Instance IsLoaded ScavengerEntries", "TazUO_settings_check"),
        ("Configuration.Profile", "OpenHealthBarForLastAttack", "hud.frames"),
        ("Configuration.Profile", "Username ServerName", "inventory.storage"),
        ("Game.UI.Gumps.BaseHealthBarGump", "LastAttackBar", "hud.frames"),
        ("Game.GameObjects.Mobile", "GetGroupForAnimation", "hud.frames"),
        ("Game.GameObjects.Mobile", "IsCovered", "inventory.paperdoll"), ("Renderer.SpriteInfo", "", "hud.frames"),
        ("Time", "Ticks", "hud.timers"),
        ("Game.UI.Controls.Control", "SetHitTestOffset _bounds Location", "inventory.bags"),
        ("Game.UI.Controls.Control", "_bounds Location", "interface inventory.paperdoll"),
        ("Game.UI.Gumps.ContainerGump", "_data _gumpPicContainer _hitBox", "inventory.bags"),
        ("Assets.TileDataLoader", "_staticData", "inventory.bags"), ("Game.Data.Layer", "", "inventory.paperdoll"),
        ("Game.UI.Controls.PaperDollInteractable", "GetAnimID", "inventory.paperdoll"),
        ("Game.Managers.EventSink", "OnEntityDamage", "meters"), ("Game.GameObjects.Entity", "", "meters"),
        ("Game.Data.Lock", "", "skills.window"), ("Game.Data.Skill", "Lock", "skills.window"),
        ("Game.GameObjects.PlayerMobile", "Skills", "skills.window"),
        ("Game.GameObjects.PlayerMobile", "Serial", "social"),
        ("Game.Managers.SkillsGroupManager", "Groups", "skills.window"),
        ("Game.Managers.SkillsGroup", "", "skills.window"),
        ("Game.UI.Gumps.SkillButtonGump", "SkillID", "skills.window"),
        ("Game.Managers.FriendsListManager", "Instance", "social"),
        ("Game.Managers.PartyManager", "Leader Inviter CanLoot Members", "social"),
        ("Game.UI.Gumps.IgnoreManagerGump", "", "social"), ("Network.AsyncNetClient", "Socket", "social sysstats"),
        ("Network.AsyncNetClient", "Statistics", "sysstats"), ("Network.NetClientExt", "Send_PartyDecline", "social"),
        ("CUOEnviroment", "CurrentRefreshRate", "sysstats"), ("CUOEnviroment", "ExecutablePath", "worldmap"),
        ("Game.Managers.EnhancedMap.EnhancedMapManager", "Instance IsConnected Config Reconnect _client",
         "worldmap.pings"), ("Game.SelectedObject", "Object", "worldmap.pings"),
        ("Game.UI.Gumps.WorldViewportGump", "Instance ResizeGameWindow SetGameWindowPosition", "interface"),
        ("Game.UI.Gumps.SystemChatControl", "IsDisposed ParentX ParentY TextBoxControl", "interface"),
        ("Game.UI.Controls.TTFTextInputField", "EnterPressed", "launcher_Enter_key"),)
    @staticmethod
    def missing():
        got = Kit._measure.get("tz_missing")
        if got is None:
            if Client._type("ClassicUO.Client") is None: return ()
            fl = Tz._flags(True) | Tz._flags(False); out = {}
            for tn, names, keys in Tz.NEED:
                t = Client._type("ClassicUO." + tn); short = tn.split(".")[-1]
                for gone in [short] if t is None else [short + "." + n for n in names.split() if not Tz.has(t, n, fl)]:
                    out.setdefault(gone, []).extend(keys.split())
            got = Kit._measure["tz_missing"] = tuple((k, tuple(v)) for k, v in sorted(out.items()))
        return [(k, list(v)) for k, v in got]
    @staticmethod
    def has(t, name, fl):
        while t is not None:
            if t.GetMember(name, fl).Length: return True
            t = t.BaseType
        return False
    @staticmethod
    def T(name):
        t = Tz._types.get(name)
        if t is None:
            t = Client._type(name)
            if t is None: raise Exception("this TazUO build has no %s" % name.split(".")[-1])
            Tz._types[name] = t
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
    def call(obj, name, args=(), t=None, opt=False):
        import System; t = t if t is not None else obj.GetType(); args = list(args); n = len(args)
        ck = ("call", t, name, n, obj is None, opt); hit = Tz._found.get(ck, Tz._MISS)
        if hit is Tz._MISS:
            hit = None; flags = Tz._flags(obj is None); tt = t
            while tt is not None and hit is None:
                for mm in tt.GetMethods(flags):
                    if mm.Name != name or mm.IsGenericMethodDefinition: continue
                    ps = list(mm.GetParameters())
                    if len(ps) == n or opt and len(ps) > n and all(p.IsOptional for p in ps[n:]):
                        hit = (mm, [p.DefaultValue for p in ps[n:]]); break
                tt = tt.BaseType
            Tz._found[ck] = hit
        if hit is None: raise Exception("can't call %s.%s" % (t.Name, name))
        return hit[0].Invoke(obj, System.Array[object](args + hit[1]))
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
    VA_KEYS = ("ActionBar_", "Attention_", "BandageAgent", "Character_", "CombatBars_", "CorpseRun_", "EMPings.",
               "Grimoire_", "Harvest_", "Interface_", "Layout_", "Lookout_", "Meters_", "Mongotchi_", "Pets_",
               "PropertyButler_", "Restock_", "SkillBags_", "Skills_", "Social_", "SpellTimers_", "StorageIndex_",
               "SwingTimer_", "swingtimer_", "SystemStats_", "TrapHL_", "TreasureHunter_", "UltimaTracker_",
               "UnifiedBag_", "UnitFrames_", "VirtueAssistant_", "WorldMap_", "ReagentPrices_")
    OWN_VARS = ("CorpseRun_corpse", "SkillBags_rules", "SkillBags_done", "UnitFrames_tracked", "Social_names",
                "TreasureHunter_maps", "Restock_settings", "PropertyButler_visits", "SpellTimers_active",
                "VirtueAssistant_starting", "VirtueAssistant_new_seen", "VirtueAssistant_alert_log",
                "VirtueAssistant_backup_ver", "ReagentPrices_book", "Skills_session", "Social_guild", "Social_roster",
                "PropertyButler_log", "PropertyButler_houses", "Mongotchi_state", "Mongotchi_shop", "Mongotchi_guests",
                "Mongotchi_quests", "Mongotchi_seasonal", "Mongotchi_achievements")
    MISSING = "\x01VA-missing"
    def __init__(self): self.base = os.path.join(Kit.data_dir(), PROFILE_DIR)
    @staticmethod
    def _read(path): return Kit.read_safe(path, None) if path else None
    @staticmethod
    def _write(path, text): Kit.write_safe(path, text)
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
        if name and "\ud800" <= name[-1] <= "\udbff": name = name[:-1]
        if name.split(".")[0].upper() in Profiles.RESERVED or name.lower() == "_favorite.txt": return ""
        return name
    def folder(self, name): return os.path.join(self.base, name)
    def names(self):
        import System; out = []
        with Kit.quiet:
            if System.IO.Directory.Exists(self.base):
                for d in System.IO.Directory.GetDirectories(self.base):
                    n = str(System.IO.Path.GetFileName(d))
                    if n.endswith(".saving") or n.endswith(".old"): continue
                    if System.IO.File.Exists(os.path.join(str(d), "profile.txt")): out.append(n)
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
        if not os.path.isdir(self.base): os.makedirs(self.base)
        self._write(os.path.join(self.base, "_favorite.txt"), name or "")
    def state(self):
        p = Kit.get_var(PROFILE_STATE_KEY).split("|"); return (p[0], p[1], p[2]) if len(p) >= 3 else ("", "", "")
    def set_state(self, mode, name, stamp): Kit.put_var(PROFILE_STATE_KEY, "%s|%s|%s" % (mode, name, stamp))
    SESSION_VARS = ("Layout_gameview_own", "Layout_gameview_lock", "Layout_zone_was", "VirtueAssistant_reclaim_undo")
    def keep_var(self, key, extra=()):
        if key == PROFILE_STATE_KEY or self.SERIAL_KEY.search(key) or key in self.SESSION_VARS: return False
        if key in self.OWN_VARS or key.startswith(("Grimoire_H_", "Layout_client_locked_")): return False
        return key.startswith(self.VA_KEYS + tuple(extra))
    @staticmethod
    def extra_keys(found):
        mods = set(n for s in HOST.slots for n in (s.key.lower(), s.title.replace(" ", "").lower()))
        return tuple(set(k[:-8] for k in found if k.endswith("_settings") and k[:-9].lower() in mods))
    def profile_vars(self, found):
        extra = self.extra_keys(found); va = dict((k, v) for k, v in found.items() if self.keep_var(k, extra))
        if Alerts.KEY in va: va[Alerts.KEY] = Alerts.with_quiet(va[Alerts.KEY], "")
        return va
    @staticmethod
    def char_vars():
        import System; t = Tz.T("ClassicUO.LegionScripting.PersistentVars")
        for m in t.GetMethods():
            if m.Name == "GetAllVars" and m.GetParameters().Length == 1:
                scope = System.Enum.Parse(m.GetParameters()[0].ParameterType, "Char")
                d = m.Invoke(None, System.Array[object]([scope]))
                return dict((str(kv.Key), "" if kv.Value is None else str(kv.Value)) for kv in d)
        raise Exception("can't list this character's saved settings")
    @staticmethod
    def parse_vars(text):
        out = {}
        for line in text.split("\n"):
            if "\t" in line:
                k, v = line.split("\t", 1); k = Profiles._unesc(k)
                if k: out[k] = Profiles._unesc(v.rstrip("\r"))
        return out
    def read_vars(self, name):
        return self.profile_vars(self.parse_vars(self._read(os.path.join(self.folder(name), "va_vars.txt")) or ""))
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
                with Kit.quiet:
                    if old is not None: F.WriteAllBytes(target, old)
                    elif F.Exists(target): F.Delete(target)
                    reload()
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
        va = self.profile_vars(self.char_vars()); va[SETTINGS_KEY] = prefs_data
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
        folder = self.folder(name); text = Kit.read_safe(os.path.join(folder, "va_vars.txt"))
        if text is None: raise Exception("its saved settings can't be read")
        va = self.profile_vars(self.parse_vars(text))
        if Alerts.KEY in va: va[Alerts.KEY] = Alerts.with_quiet(va[Alerts.KEY], Kit.get_var(Alerts.KEY))
        for k in sorted(va): Kit.put_var(k, va[k])
        ok = self.wait_vars(va); lay = self._read(os.path.join(folder, "unified_bag.cfg")); bag = self.bag_path()
        cur = Kit.read_safe(bag) if lay is not None and bag else None
        if cur is not None:
            own = [l for l in cur.splitlines() if l.startswith(self.BAG_OWN)]
            self._write(bag, "\n".join([l for l in lay.splitlines() if l.strip()] + own))
        done, failed = self._on_client(lambda: self._client_import(os.path.join(folder, "tazuo")))
        if lay is not None and bag and cur is None: failed = list(failed) + ["bag layout (couldn't read the bag file)"]
        self.set_state(mode, name, info.get("saved", "")); return len(va), ok, done, failed
    def report(self, name, verb, n, ok, done, failed):
        Kit.say('profile "%s" %s: %s; TazUO: %s.'
                   % (name, verb, Kit.count(n, "Virtue Assistant setting"), ", ".join(done) or "nothing"), Kit.HUE_GOOD)
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
        self.lag_lbl = self.dirty = self.gear_pos = self.body = self.head = None
        self.link_state = self.prof_sel = self.prof_cache = self.prof_shown = None
        self.loading = self.stale_page = self.search_tb = self.search_text = None
        self.gear_clicked = self.closing = self.docked = self.prof_stale = self.prof_redraw = False
        self.box_hit = self.redraw_req = self.search_focus = self.find_prof = False
        self.gear_look = self.lag_next = self.gear_moved = self.link_next = self.box_next = self.search_at = 0.0
        self.resize_at = 0.0; self.store = ({}, {}); self.seen = {}; self._pp_gate = [0.0]; self._fld_gate = [0.0]
        self._fld_due = True; self.opt_search = ""; self.opt_index = {}; self.opt_ver = 0; self.opt_open = False
        self.opt_wait = self.opt_mark = self.opt_lbl = self.opt_drawn = self.fresh_view = None
        self.opt_hits = (None, None); self.hit_keys = []; self.why, self.why_log, self.stale_log = None, [], []
        self.from_xy = None
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
    STAR_RECTS = ((7, 1, 1, 2), (6, 3, 3, 3), (1, 6, 13, 2), (4, 8, 7, 3), (3, 11, 3, 3), (9, 11, 3, 3))
    STAR_ON, STAR_OFF = (240, 192, 64), (106, 106, 106); PROF_H = 34; PROF_DD_W = 196
    def _prof_reset(self):
        self.prof_dd = self.prof_dd_args = self.prof_tb = self.prof_seen = None; self.prof_names = []
        self.prof_fav = ""; self.prof_stars = []; self.prof_star_hit = False
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
        xs = x + 12 + self.PROF_DD_W + 10; ys = y + (H - 16) // 2; off = "#%02X%02X%02X" % self.STAR_OFF
        boxes = [Kit.add_box(g, xs + rx, ys + ry, rw, rh, 1.0, off) for rx, ry, rw, rh in self.STAR_RECTS]
        self.prof_stars = [b for b in boxes if b is not None]
        Kit.catcher(g, xs - 3, ys - 3, 22, 22, self._star_click,
                    "Favourite: characters that haven't loaded another profile get it (click again to clear)")
        xb = xs + 28
        for key, art, cap, gap, tip in (("p_load", Kit.ART_PLAY, "Load", 14, "Load the picked profile here"),
                ("p_save", Kit.ART_OK, "Save", 6, "Save this setup under the typed name, or over the picked profile")):
            Kit.art_button(g, self.store, key, art, xb, y + 6, cap, tip); xb += self._cap_w(art, cap) + gap
        Kit.add_label(g, "as", xb, y + 9, Kit.HUE_INFO); xf = xb + Kit.text_w("as") + 8
        fw = (Kit.pic_size(Kit.ART_PAGE[0])[0] or 30) + 8 if self.find_prof else 0
        self.prof_tb = Kit.with_tip(Kit.add_textbox(g, "", xf, y + 6, max(60, x + w - 12 - xf - fw), numbers=False),
                                    "New profile name (empty: save over the picked one)")
        items = [n + ("  (favourite)" if n == fav else "") for n in names] or ["(no profiles saved yet)"]
        self.prof_dd_args = (x + 12, y + 7, self.PROF_DD_W, items, names.index(sel) if sel in names else 0)
    def _add_profile_list(self, g):
        if self.prof_dd_args is None: return
        old = self.prof_dd; dx, dy, dw, items, idx = self.prof_dd_args
        if old is not None:
            i = Kit.dd_index(old, None); Kit.dispose(old)
            if i is not None and 0 <= i < len(self.prof_names): self.prof_sel = self.prof_names[i]
        if self.prof_sel in self.prof_names: idx = self.prof_names.index(self.prof_sel)
        dd = G.CreateDropDown(dw, items, idx); dd.SetPos(dx, dy); g.Add(dd)
        self.prof_dd = Kit.with_tip(dd, "Saved profiles: pick one to load or save over")
        self.prof_seen = idx; self._show_star()
    def _prof_picked(self): return self.prof_sel if self.prof_sel in self.prof_names else None
    def _show_star(self):
        p = self._prof_picked(); r, g, b = self.STAR_ON if bool(p) and p == self.prof_fav else self.STAR_OFF
        for box in self.prof_stars:
            with Kit.quiet: box.SetBaseColor(r, g, b, 255)
    def _star_click(self): self.prof_star_hit = True
    def _poll_profiles(self):
        if self.prof_dd is not None and self._fld_due:
            i = Kit.dd_index(self.prof_dd, None)
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
            if not name:
                Kit.say("that name can't be used for a profile; pick another." if typed else
                        "type a profile name beside Save.", Kit.HUE_BAD); return
            self.host.profile_req = ("save", name)
        elif not picked: Kit.say("save a profile first (type a name beside Save).", Kit.HUE_BAD)
        elif load: self.host.profile_req = ("load", picked)
        else: self.host.profile_req = ("fav", picked)
    def settings_slots(self):
        return [s for s in self.host.slots if s.lazy is not None or (s.api is not None and s.api.get("build_config"))] \
            + list(self.host.pages)
    def open(self, launch=False):
        if self.prof_cache is None: self.refresh_profiles()
        if launch and self.host.bar_on(): self.host.dock_want_set(self.DOCK_KEY, True)
        if self.minimized or launch: self.build_gear(self.gx, self.gy)
        else: self.build_full(self.x, self.y, "start")
    def build_full(self, x, y, why="redraw"): self.why = why; Kit.on_client(lambda: self._build_full(x, y))
    def _replace(self, g, mode, x, y, w, h, head=None, hidden=False):
        old, same = self.g, self.mode == mode; x, y = Kit.place(g, x, y, w, h, head)
        if mode == "gear": self.gx, self.gy = x, y
        else: self.x, self.y = x, y
        self.g, self.mode = g, mode; Kit.replace_gump(old if same else None, g, hidden); Kit.on_moved(g, self._moved)
        self.host.built(self.DOCK_KEY)
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
        self.host.count_error(s, page=True)
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
                  "Drag a corner to resize; - and + scale the window.",
                  "Zones, layout and snapping: Settings > Interface.")
    BROKEN = "couldn't load: see the journal"; LAG_SAMPLE = "12 modules on; slowest lately: Ultima Tracker, 999 ms"
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
        lim_h = self.lim_h; sh = Kit.screen()[1]
        if sh: lim_h = min(lim_h, max(self.MIN_H, int(sh / self.scale)))
        limit = max(40, lim_h - self._body_y() - M); placed = self._pack(units, n, limit)
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
            found[s.key] = parts; cat = s.category or "Other"
            if cat not in groups: groups[cat] = []; order.append(cat)
            groups[cat].append(s)
        cats = [c for c in CATEGORY_ORDER if c in groups] + sorted(c for c in order if c not in CATEGORY_ORDER)
        rows = []; news = WhatsNew.unseen()
        for cat in cats:
            rows.append(("head", cat))
            for s in groups[cat]:
                broken = s.api is None and s.lazy is None
                rows.append(("mod", s, broken, Kit.wrap(self.BROKEN if broken else s.desc, CW - 212)))
                if s.parts and not broken and (not s.folded or found.get(s.key)):
                    for p in s.parts:
                        hit = p[0] in found.get(s.key, ())
                        tag = Kit.Form.FOUND if hit else (Kit.Form.NEW if "%s.%s" % (s.key, p[0]) in news else "")
                        tw = Kit.text_w(tag) + 10 if tag else 0
                        rows.append(("part", s, p, Kit.wrap(p[2] or "", CW - 248 - tw), hit))
        if not rows: rows.append(("none", 'No module matches "%s".' % self.mod_search.strip()))
        return rows
    @staticmethod
    def _row_h(r):
        if r[0] in ("mod", "part"): return Kit.pitch(26) + 20 * (len(r[3]) - 1)
        return Kit.pitch(24)
    def _units_modules(self, slots):
        CW = self.COL_W; rows = self._mod_rows(slots, CW)
        lines = [l for para in self.HELP_LINES for l in Kit.wrap(para, CW - 42)]; h_opts = 8 + 22 * len(lines) + 24
        units = [{"rows": [self._row_h(r) for r in rows], "head": 34, "tail": 4,
                  "draw": lambda g, x, y, h, i, j: self._draw_mods(g, x, y, CW, h, rows[i:j], i == 0)}, {"h": h_opts,
                  "draw": lambda g, x, y, h, i, j: self._draw_opts(g, x, y, CW, h, lines)}]
        return units, CW
    PAGE_MAX_W = 1100
    def _measure_page(self, page, x0, y0, CW):
        try: hp = int(page.api["config_height"](CW))
        except Exception: hp = None
        ck = (page.key, CW, hp, bool(page.running), tuple(p[0] for p in page.parts if page.parts_on.get(p[0])))
        if ck in self.measured: return self.measured[ck]
        measure = PageCanvas(None); out = None; was = Kit.Form.page
        try:
            Kit.Form.page = page.key; page.api["build_config"](measure, x0, y0, CW)
            if Kit.flush():
                right = x0 + CW
                for c in measure.ctrls:
                    r = safe(lambda: int(c.GetX()) + int(c.GetWidth()), None)
                    if r is not None and r != x0 + CW: right = max(right, r + 4)
                out = ([tuple(int(v) for v in r) for r in measure.sections], right - x0)
        except Exception: out = None
        finally:
            Kit.Form.page = was
            if page.api.get("config_closed"): safe(page.api["config_closed"])
            for c in measure.ctrls: Kit.dispose(c)
        if len(self.measured) > 64: self.measured.clear()
        if page not in self.host.pages: self.measured[ck] = out
        return out
    def forget_measure(self, key):
        for ck in [ck for ck in self.measured if ck[0] == key]: self.measured.pop(ck, None)
    def loaded(self, key):
        self.forget_measure(key); self._forget_index(key)
        if self.opt_wait is not None and self.opt_wait.key == key: self.opt_wait = None
        if self.loading is not None and self.loading.key == key: self.redraw_req = True
    OPT_TIP = "Type words to find an option on any settings page"; OPT_CAP = 4000; OPT_MAX = 30
    READING = "Reading settings: %d of %d pages"
    def _pick_unit(self, pages, CW, lit):
        slot = 35 + max([Kit.text_w(s.title) for s in pages] or [80]) + 12; per = max(1, 1 + (CW - 30 - slot) // 196)
        self.page_keys = [("page_" + s.key, s.key) for s in pages]; n = (len(pages) + per - 1) // per
        news = set(s.key for s in pages if WhatsNew.unseen(s.key))
        def draw_pick(g, x, y, h, i, j):
            Kit.add_section(g, x, y, CW, h, "SETTINGS  (pick a page)" if i == 0 else "SETTINGS  (continued)")
            if i == 0: self._search_box(g, x + CW - 12 - self.SEARCH_W, y, self.opt_search, self.OPT_TIP)
            ly = max(((Kit.pic_size(Kit.ART_PAGE[0])[1] or 22) - 16) // 2, 0)
            for k, s in enumerate(pages):
                r = k // per; bx, by = x + 30 + (k % per) * 196, y + 32 + (r - i) * 28
                if not i <= r < j: continue
                Kit.art_button(g, self.store, "page_" + s.key, Kit.ART_PAGE, bx, by, s.title,
                               "Show %s settings" % s.title, Kit.HUE_TITLE if lit(s) else Kit.HUE_TEXT)
                if s.key in news:
                    Kit.add_label(g, Kit.Form.NEW, bx + self._cap_w(Kit.ART_PAGE, s.title) + 6, by + ly, Kit.HUE_INFO)
        return {"rows": [28] * n, "head": 34, "tail": 4, "draw": draw_pick}
    def _search_box(self, g, xs, y, text, tip):
        Kit.add_label(g, "Search", xs - 8 - Kit.text_w("Search"), y + 7, Kit.HUE_INFO)
        self.search_tb = Kit.with_tip(Kit.add_textbox(g, text, xs, y + 5, self.SEARCH_W, numbers=False), tip)
        self.search_text = None
    def _forget_index(self, key):
        if self.opt_index.pop(key, None) is not None: self.opt_ver += 1
    def _index_page(self, s):
        out = [(s.key, None, "", "page", s.title, s.desc or "", None)]
        out += [(s.key, p[0], "", "part", p[1], p[2] or "", None) for p in s.parts]; sink = Kit.Form.sink = []
        try: s.api["config_height"](self.COL_W)
        except Exception: pass
        finally: Kit.Form.sink = None
        for pk, title, rows in sink:
            sec = str(title or "").split("  ")[0]
            for r in rows:
                if r[0] == "buttons":
                    out += [(s.key, pk, sec, "button", str(b[2] or ""), str(b[3] or ""), b[0]) for b in r[1]]
                elif r[0] == "note": out.append((s.key, pk, sec, "note", str(r[1]), "", r[1]))
                elif r[0] == "check" or r[0] in Kit.Form.FIELDS:
                    out.append((s.key, pk, sec, r[0], str(r[2]), str(r[3] or ""), r[1]))
        keep, seen = [], set()
        for e in out:
            if e not in seen and (e[3] in ("page", "part") or e[4].strip()): seen.add(e); keep.append(e)
        return keep
    def _index_tick(self):
        idx = self.opt_index; todo = [s for s in self.settings_slots() if s.key not in idx]
        if not todo: return False
        s = next((p for p in todo if p.lazy is None), None)
        if s is None:
            if self.opt_wait is not todo[0]: self.opt_wait = todo[0]; self.host.request_load(todo[0])
            return False
        n = sum(len(v) for v in idx.values()); idx[s.key] = self._index_page(s)[:max(0, self.OPT_CAP - n)]
        self.opt_ver += 1; return True
    def _opt_hits(self):
        ck = (self.opt_search.lower(), self.opt_ver)
        if self.opt_hits[0] == ck: return self.opt_hits[1]
        words = ck[0].split(); found = []
        for pi, s in enumerate(self.settings_slots()):
            for n, e in enumerate(self.opt_index.get(s.key, ())):
                p = s.part(e[1]) if e[1] else None; cap, tip = e[4].lower(), e[5].lower()
                head = " ".join((e[2], s.title, p[1] if p else "")).lower(); score = 0
                for w in words:
                    pts = 3 if w in cap else 2 if w in head else 1 if w in tip else 0
                    if not pts: score = 0; break
                    score += pts
                if score: found.append((-score, pi, n, e))
        found.sort(key=lambda f: f[:3]); hits = [f[3] for f in found[:self.OPT_MAX]]
        self.opt_hits = (ck, hits); return hits
    def _poll_index(self):
        changed = self._index_tick(); pages = self.settings_slots()
        done = sum(1 for s in pages if s.key in self.opt_index)
        if not pages: return False
        if done < len(pages):
            if changed and self.opt_lbl is not None: Kit.set_text(self.opt_lbl, self.READING % (done, len(pages)))
            return False
        if self.search_at or self._opt_hits() == self.opt_drawn: return False
        self.search_focus = True; self.redraw(); return True
    def _hit_text(self, e):
        s = self.host.page_slot(e[0]); title = s.title if s is not None else e[0]; cap = e[4].rstrip(":")
        if e[3] == "page": return title
        if e[3] == "part" or not e[2]: return "%s > %s" % (title, cap)
        return "%s > %s: %s" % (title, e[2], cap)
    def _found_unit(self, pages, CW):
        done = sum(1 for s in pages if s.key in self.opt_index); hits = self._opt_hits() if done == len(pages) else None
        self.opt_drawn = hits; rows = hits or [None]
        note = self.READING % (done, len(pages)) if hits is None else 'No option matches "%s".' % self.opt_search
        def draw_found(g, x, y, h, i, j):
            Kit.add_section(g, x, y, CW, h, "FOUND  (click one to open it)" if i == 0 else "FOUND  (continued)")
            for r in range(i, j):
                e, ry = rows[r], y + 32 + (r - i) * 28
                if e is None:
                    self.opt_lbl = Kit.add_label(g, Kit.fit(note, CW - 24), x + 12, ry + 3, Kit.HUE_INFO); continue
                bkey, text = "hit_%d" % r, self._hit_text(e); self.hit_keys.append((bkey, e))
                Kit.art_button(g, self.store, bkey, Kit.ART_PAGE, x + 30, ry, Kit.fit(text, CW - 77),
                               e[5] or "Open %s" % text)
        return {"rows": [28] * len(rows), "head": 34, "tail": 4, "draw": draw_found}
    def _fresh(self, key):
        fv = self.fresh_view
        if fv is None or fv[0] != key: fv = self.fresh_view = (key, WhatsNew.unseen(key))
        return fv[1]
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
        wins = LAYOUT.windows_of(page.key) if LAYOUT.enabled else ()
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
        if len(bands) == 1 and 0 in at: x0, y0 = at[0][0], at[0][1] - bands[0][0]
        canvas = PageCanvas(g); F = Kit.Form; m = self.opt_mark; F.page, F.fresh = page.key, self._fresh(page.key)
        F.mark = (m[1], m[2]) if m is not None and m[0] == page.key and m[3] != "part" else None
        try: page.api["build_config"](canvas, x0, y0, CW)
        except Exception as ex:
            self._settings_error(page, "window", ex); Kit.add_section(g, x0, y0, CW, 40)
            Kit.add_label(g, "Settings unavailable: %s" % ex, x0 + 12, y0 + 12, Kit.HUE_BAD)
        finally: F.page = F.fresh = F.mark = None
        WhatsNew.see(self._fresh(page.key)); self.shown_page = page.key; moves = []
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
        Kit.add_section(g, x, y, w, h, "PARTS  (tick a part to turn it on)"); ry = y + 32; m = self.opt_mark
        fresh = self._fresh(s.key)
        for p in s.parts:
            self._part_box(g, s, p, x + 12, ry); hit = m is not None and m[3] == "part" and m[:2] == (s.key, p[0])
            tag = Kit.Form.FOUND if hit else Kit.Form.NEW if "%s.%s" % (s.key, p[0]) in fresh else None
            d = Kit.fit(p[2] or "", w - 236 - (Kit.text_w(tag) + 6 if tag else 0))
            Kit.add_label(g, d, x + 224, ry + 2, Kit.HUE_INFO)
            if tag: Kit.add_label(g, tag, x + 224 + Kit.text_w(d) + 6, ry + 2, Kit.HUE_TITLE)
            ry += 26
    def _part_box(self, g, s, p, x, ry):
        on = bool(s.parts_on.get(p[0])); cb = Kit.add_check(g, p[1], x, ry, on, "%s: %s" % (s.title, p[2] or p[1]))
        self._hook_box(cb); self.part_boxes.append((s, p[0], cb)); self.seen["%s.%s" % (s.key, p[0])] = on
    ZONE_TIP = "Click: next zone (free: stays where you put it; Settings > Interface lists them all)"
    def _draw_windows(self, g, x, y, w, h, wins):
        Kit.add_section(g, x, y, w, h, "WINDOWS  (the zone each sits in)"); zones = LAYOUT.zone_choices(); ry = y + 32
        for key, title in wins:
            Kit.add_label(g, Kit.fit(title, 200), x + 12, ry + 3); zid = LAYOUT.zone_of(key)
            cap = "Zone: " + ((zid[5:] if zid.startswith("Zone ") else zid) if zid else "free"); bkey = "zone_" + key
            Kit.art_button(g, self.store, bkey, Kit.ART_PAGE, x + 224, ry - 2, cap, self.ZONE_TIP)
            self.zone_keys.append((bkey, key, zones)); ry += 26
    FOLD_TIP = "Show its parts"; UNFOLD_TIP = "Hide its parts"
    MOD_TIP = "Type part of a name or feature to list matching modules (old names work)"
    def _draw_mods(self, g, x, y, w, h, rows, first):
        Kit.add_section(g, x, y, w, h, "MODULES  (tick a module to turn it on)" if first else "MODULES  (continued)")
        if first: self._search_box(g, x + w - 12 - self.SEARCH_W, y, self.mod_search, self.MOD_TIP)
        ry = y + 32; news = WhatsNew.unseen()
        for row in rows:
            if row[0] == "part":
                s, p, lines, hit = row[1], row[2], row[3], row[4]; self._part_box(g, s, p, x + 36, ry); xd = x + 236
                for k, line in enumerate(lines): Kit.add_label(g, line, xd, ry + 2 + 20 * k, Kit.HUE_INFO)
                tag = Kit.Form.FOUND if hit else (Kit.Form.NEW if "%s.%s" % (s.key, p[0]) in news else "")
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
    def _draw_opts(self, g, x, y, w, h, lines):
        Kit.add_section(g, x, y, w, h); ly = y + 8
        for line in lines: Kit.add_label(g, line, x + 30, ly, Kit.HUE_INFO); ly += 22
        self.lag_lbl = Kit.add_label(g, "", x + 30, ly, Kit.HUE_INFO); self.lag_next = 0.0
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
        self.page_keys, self.box_list, self.zone_keys, self.hit_keys = [], [], [], []
        self.lag_lbl = self.opt_lbl = None; self._prof_reset()
    def _plan(self):
        slots, pages, page = self._context(); M, GAP = Kit.MARGIN, Kit.GAP; y_body = self._body_y()
        if self.tab == "settings" and pages and self.opt_search and not self.opt_open:
            CW, page, self.fresh_view = self.COL_W, None, None
            units = [self._pick_unit(pages, CW, lambda s: False), self._found_unit(pages, CW)]
        elif self.tab == "settings" and page is not None: units, CW = self._units_settings(pages, page, M, y_body)
        elif self.tab == "settings" and self.loading is not None and pages:
            units, CW = self._units_loading(pages, self.loading.title)
        else: units, CW = self._units_modules(slots); self.fresh_view = None
        placed = self._flow(units, CW); n_cols = 1 + max([p[1] for p in placed] or [0])
        W = 2 * M + n_cols * CW + (n_cols - 1) * GAP; H = y_body + max([p[2] + p[5] for p in placed] or [40]) + M
        return page, units, CW, placed, W, H
    def _draw_body(self, g, units, CW, placed):
        body = PageCanvas(g); y_body = self._body_y()
        for u, col, top, i, j, h in sorted(placed, key=lambda p: p[0]):
            units[u]["draw"](body, Kit.MARGIN + col * (CW + Kit.GAP), y_body + top, h, i, j)
        return body
    def _build_full(self, x, y):
        if self.host.settled_at is None and len(self.why_log) < 10: self.why_log.append((time.time(), self.why))
        self._reset(); self.seen, self.resize_at = {}, 0.0
        self.part_boxes, self.fold_keys = [], []; M, GAP = Kit.MARGIN, Kit.GAP; L = M
        page, units, CW, placed, W, H = self._plan(); y_title = M; y_prof = y_title + 34 + GAP; y_body = self._body_y()
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
        self.find_prof = False; lt = self.host.launcher; lim = xl - 6 - 16 - 8
        fw, aw = self._cap_w(Kit.ART_PAGE, "Find"), Kit.pic_size(Kit.ART_PAGE[0])[0] or 30
        if lt is not None and xt + fw <= lim:
            Kit.art_button(g, self.store, "find", Kit.ART_PAGE, lim - fw, y_title + 6, "Find", Launcher.TIP,
                           Kit.HUE_INFO, lt.toggle)
        elif lt is not None and xt + aw <= lim:
            Kit.art_button(g, self.store, "find", Kit.ART_PAGE, lim - aw, y_title + 6, None,
                           Kit.caption_tip("Find", Launcher.TIP), None, lt.toggle)
        else: self.find_prof = lt is not None
        try: self._build_profiles(g, L, y_prof, IW)
        except Exception as ex:
            self.prof_dd_args = None; Kit.add_label(g, "Profiles unavailable: %s" % ex, L + 12, y_prof + 9, Kit.HUE_BAD)
        if self.find_prof:
            Kit.art_button(g, self.store, "find", Kit.ART_PAGE, L + IW - 12 - aw, y_prof + 6, None,
                           Kit.caption_tip("Find", Launcher.TIP), None, lt.toggle)
        keys = frozenset(self.store[0]); body = self._draw_body(g, units, CW, placed); self._add_profile_list(g)
        if not Kit.scale_window(g, S) and S != 1.0:
            self.scale, S, WS, HS = 1.0, 1.0, W, H; Kit.say("can't scale the window; it stays at 100%.", Kit.HUE_BAD)
        if self.mode != "full": jx = LAYOUT.beside_journal(x, y, WS, HS); self.from_xy = (x, y, jx); x = jx
        self._replace(g, "full", x, y, WS, HS, int(round(y_body * S))); fit = Kit.scroll_info(g)
        self.size = (fit["w2"], fit["hv"]) if fit else (WS, HS); self.minimized = False; self.dirty = None
        self.body, self.head = body, (g, W, self.tab, (Kit.look(), Kit.compact), keys)
        if self.search_focus:
            self.search_focus = False; tb = self.search_tb
            if tb is not None:
                cc = Kit.client_control(tb)
                if cc is not None and Kit.flush(): safe(lambda: cc.SetKeyboardFocus())
    def build_gear(self, x, y):
        self._reset(); self.fresh_view = None; S = self.GEAR; g = G.CreateGump(True, True)
        Kit.add_window_frame(g, S, S, corners=False); Kit.add_section(g, 7, 7, S - 14, S - 14)
        p = G.CreateGumpItemPic(0x1053, S - 18, S - 18); p.SetPos(9, 9); p.SetAcceptMouseInput(False); g.Add(p)
        Kit.catcher(g, 0, 0, S, S, self._gear_click, "%s: click to open, drag to move" % APP_NAME, movable=True)
        self.gear_clicked, self.gear_pos, self.gear_moved = False, None, 0.0
        self.docked = self.host.dock_wanted(self.DOCK_KEY) and self.host.bar_soon()
        self._replace(g, "gear", x, y, S, S, hidden=self.docked); self.minimized = True
    def fold_to_bar(self):
        self.host.dock_want_set(self.DOCK_KEY, True)
        if self.mode == "full": self.fold()
        if not self.host.bar_alive(): self.host.dock_note(APP_NAME)
    def _show_gear(self, shown):
        g = self.g
        if self.mode == "gear" and Kit.is_open(g): g.IsVisible = bool(shown); Kit.stir()
    def link_tick(self):
        now = time.time()
        if now < self.link_next and self.link_next - now <= 0.1: return
        self.link_next = now + 0.1; key = self._take_shared(self.LINK_ENABLE)
        if key: self.host.enable(str(key))
        cmd = self._take_shared(self.LINK_CMD)
        if cmd:
            cmd = str(cmd)
            if cmd == "show" and self.mode != "full":
                if not self._stale("link"): self.unfold("link")
            elif cmd == "dock" and self.mode == "full": self.fold_to_bar()
            elif cmd == "modules": self.request_tab = "modules"
        self.dock_sync(); state = ("docked" if self.docked else "gear") if self.mode == "gear" else "open"
        if state != self.link_state: self.link_state = state; API.SetSharedVar(self.LINK_STATE, state)
    def dock_sync(self):
        want = self.host.dock_wanted(self.DOCK_KEY)
        if self.mode == "gear" and (self.docked or want):
            hide = want and self.host.bar_soon()
            if hide != self.docked: self.docked = hide; self._show_gear(not hide)
    @staticmethod
    def _take_shared(name):
        try: v = API.GetSharedVar(name)
        except Exception: return None
        if v: API.RemoveSharedVar(name)
        return v
    def _gear_click(self): self.gear_clicked = True
    def _unpressed(self): return self.host.booting() and self.host.pressed_at <= 0
    def _stale(self, why):
        h = self.host
        if not h.booting() or h.pressed_at > 0: return False
        if len(self.stale_log) < 10: self.stale_log.append((time.time(), why))
        return True
    def pos(self): g = self.g; return safe(lambda: int(g.GetX())), safe(lambda: int(g.GetY()))
    def store_prefs(self, prefs):
        if Client.on_client_thread(): self._note_pos()
        for k, v in (("cfg_x", self.x), ("cfg_y", self.y), ("cfg_w", self.lim_w), ("cfg_h", self.lim_h),
                     ("cfg_scale", int(round(self.scale * 100))), ("gear_x", self.gx), ("gear_y", self.gy)):
            prefs[k] = str(v)
        prefs["cfg_min"] = "1" if self.minimized else "0"
        prefs["cfg_tab"], prefs["cfg_page"] = self.tab, self.page or ""; prefs["snap"] = "1" if SNAP.enabled else "0"
    def fold(self):
        x, y = self.pos(); f, self.from_xy = self.from_xy, None
        if x is not None: self.x, self.y = x, y
        self.gx, self.gy = (f[0], f[1]) if f is not None and f[0] != f[2] == self.x else (self.x, self.y)
        self.build_gear(self.gx, self.gy); self.host.save_prefs()
    def unfold(self, why="redraw"):
        x, y = self.pos()
        if x is not None: self.gx, self.gy = x, y
        self.docked = False; self.host.dock_forget(self.DOCK_KEY); self.build_full(self.gx, self.gy, why)
        self.host.save_prefs()
    def redraw(self, why="redraw"):
        if self.mode != "full": self.unfold(why); return
        x, y = self.pos()
        if x is not None: self.x, self.y = x, y
        self.build_full(self.x, self.y, why); self.host.save_prefs()
    def _switch_page(self, key):
        self.page = key; x, y = self.pos()
        if x is not None: self.x, self.y = x, y
        Kit.on_client(self._swap_body); self.host.save_prefs()
    def _swap_body(self):
        g, head = self.g, self.head; done = False
        if head is not None and head[0] is g and Kit.is_open(g) and self.tab == head[2] == "settings" \
                and head[3] == (Kit.look(), Kit.compact) and self.scale == 1.0 and g not in Kit._scrolled \
                and g not in Fill.recs and not self.resize_at and self.prof_cache is not None \
                and self._prof_key(self.prof_cache) == self.prof_shown:
            try: done = self._fast_body(g, head[1], head[4])
            except Exception as ex: self.host._tell("%s: settings window error: %s%s" % (APP_NAME, ex, _error_where()))
        if not done: self.why = "redraw"; self._build_full(self.x, self.y)
    def _fast_body(self, g, W0, keys):
        self._leave_page(); self.page_keys, self.zone_keys, self.part_boxes, self.seen = [], [], [], {}
        page, units, CW, placed, W, H = self._plan()
        if page is None or W != W0 or H > Kit.screen()[1] > 0 or not Kit.frame_fit(g, W, H): return False
        store, texts, w2r = self.store, Kit._texts, Fill.w2r
        for c in self.body.ctrls: Kit.dispose(c); texts.pop(c, None); w2r.pop(c, None)
        for k in [k for k in store[0] if k not in keys]: store[0].pop(k, None); store[1].pop(k, None)
        self.body = self._draw_body(g, units, CW, placed); self._add_profile_list(g)
        self.x, self.y = Kit.place(g, self.x, self.y, W, H)
        Kit.moved_by_code(g); self.size, self.dirty = (W, H), None; return True
    def show_settings(self, key): self.request = key
    def refresh(self, key):
        self.forget_measure(key); self._forget_index(key)
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
            key, self.request = self.request, None; self.tab, self.page = "settings", key
            self.opt_open = self.opt_open or bool(self.opt_search)
            if self.opt_mark is not None and self.opt_mark[0] != key: self.opt_mark = None
            if self.mode == "full" or not self._unpressed(): self.redraw("request:%s" % key)
            return
        if self.request_tab is not None:
            tab, self.request_tab = self.request_tab, None
            if tab in ("modules", "settings"): self.tab = tab
            if self.mode == "full" or not self._unpressed(): self.redraw("tab:%s" % tab)
            return
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
                if now - self.gear_moved > 0.35 and not Kit.just_dragged(self.g) and not self._stale("gear"):
                    self.unfold("gear")
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
        if self.tab == "settings" and self.opt_search and not self.opt_open and self._fld_due:
            if self._poll_index(): return
        if self.lag_lbl is not None and time.time() >= self.lag_next:
            self.lag_next = time.time() + 1.0; running = self.host.active
            if running:
                worst = max(running, key=lambda s: s.load[2])
                text = "%s on; slowest lately: %s, %d ms" % (Kit.count(len(running), "module"), worst.title,
                                                              worst.load[2])
            else: text = "No modules on"
            Kit.set_text(self.lag_lbl, text)
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
            self.search_at = 0.0; q = t.strip(); opt = self.tab == "settings"
            if q.lower() != (self.opt_search if opt else self.mod_search).strip().lower():
                if not opt: self.mod_search = q
                else: self.opt_search, self.opt_open = q, False
                if opt and not q: self.opt_mark = None
                self.search_focus = True; self.redraw(); return True
        return False
    BOX_EVERY = 1.0
    def _hook_box(self, cb):
        if cb is None: return
        def hit(*args): Kit.clicks_seen = True; self.box_hit = True; HOST.poke()
        G.AddControlOnClick(cb, hit)
    def _poll_boxes(self):
        seen = self.seen
        for s, pk, cb in self.box_list + self.part_boxes:
            sk, cur = (s.key, s.enabled) if pk is None else ("%s.%s" % (s.key, pk), bool(s.parts_on.get(pk)))
            try: v = bool(cb.IsChecked)
            except Exception: v = cur
            if v != seen.get(sk):
                seen[sk] = v
                if pk is not None:
                    self.host.part_set(s.key, pk, v)
                    if v: WhatsNew.see((sk,))
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
        Kit.was_clicked(store, "find")
        for key, d in (("scale_down", -1), ("scale_up", 1), ("scale_reset", 0)):
            if Kit.was_clicked(store, key): self._step_scale(d); return True
        for key, _ in self.TABS:
            if Kit.was_clicked(store, "tab_" + key) and key != self.tab: self.tab = key; self.redraw(); return True
        for bkey, key in self.page_keys:
            if Kit.was_clicked(store, bkey) and key != self.shown_page:
                self.opt_open, self.opt_mark = bool(self.opt_search), None; self._switch_page(key); return True
        for bkey, e in self.hit_keys:
            if Kit.was_clicked(store, bkey):
                self.opt_open, self.opt_mark = True, (e[0], e[1], e[6] if e[6] is not None else e[4], e[3])
                self._switch_page(e[0]); return True
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
    W = ConfigWindow.W; prof_stale = False; mode = "alone"
    def __init__(self, s):
        self.s, self.want, self.dirty, self.parts, self.check_at = s, False, False, None, 0.0
        self.st = {"minimized": False, "shutting": False, "docked": False, "queue": []}
        self.win = {"g": None, "c": {}, "store": ({}, {})}
        self.wnd = Kit.Window(s.key + "_alone", s.title + " settings", self.st, self.win, self.build,
                              "VirtueAssistant_alone_pos", mini=(260, 46), lock=False, owner=False,
                              close_tip="Close these settings")
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
            was = Kit.Form.page; Kit.Form.page = self.s.key
            try: api["build_config"](g, M, top + ph, w)
            finally: Kit.Form.page = was
        self.wnd.end(g)
    def poll_parts(self):
        s = self.s; new = self.parts.read(); changed = [k for k in new if s.parts_on.get(k) != new[k]]
        if changed and s.parts and not any(new.get(p[0], s.parts_on.get(p[0])) for p in s.parts):
            self.dirty = True
            API.SysMsg("%s: keep one part ticked; close the window to turn it off." % s.title, Kit.HUE_INFO); return
        for k in changed: HOST.part_set(s.key, k, new[k])
        if changed:
            off = ["!" + p[0] for p in s.parts if not s.parts_on.get(p[0])]
            Kit.put_var(ALONE_PARTS % s.key, ",".join(s.parts_wanted() + off)); self.dirty = True
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
            except Exception as ex:
                HOST._tell("%s: settings error: %s" % (self.s.title, ex)); HOST.count_error(self.s, page=True)
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
        self.docked = self.minimized and host.dock_soon("hub")
        host.dock_add("hub", {"title": "Ultima Tracker", "icon": 0x1057, "always": True,
                              "state": self.state, "show": self.show, "dock": self.dock,
                              "undock": self.undock, "minimize": self.minimize, "on": self.open_modules,
                              "gump": lambda: self.g, "redraw": self.refresh})
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
        if Kit.is_open(g) and not self.host.layout_holds("hub"):
            with Kit.quiet: self.x, self.y = int(g.GetX()), int(g.GetY())
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
    def build(self): Kit.on_client(lambda: Binds.scoped("va.hub", self._build))
    def _build(self):
        self.dirty = False
        if not self.sections: self._close_window(); return
        self._pos(); self._leave(); old = self.g; M, GAP = Kit.MARGIN, Kit.GAP; store = ({}, {})
        g = G.CreateGump(True, True); title = self.title().upper(); held = self.host.layout_holds("hub")
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
            if held: Kit.title_bar(g, store, w, self.title(), "hub", None, None)
            else:
                Kit.add_section(g, M, M, IW, 30); Kit.add_label(g, title, M + 10, M + 7, Kit.HUE_TITLE)
                Kit.title_catcher(g, M, M, IW - 84 - Kit.DOCK_DX - Kit.TITLE_GAP, 30, self.toggle_min, key="hub")
                Kit.dock_button(g, store, w - M - 74, M + 7)
                Kit.art_button(g, store, "min", Kit.ART_MIN, w - M - 74, M + 7, None, Kit.MIN_TIP)
                Kit.art_button(g, store, "close", Kit.ART_CLOSE, w - M - 54, M + 4, None, close_tip)
            y = M + 30 + GAP
            for (key, t, hooks), sh in zip(self.sections, heights):
                st_ = self.stores[key] = ({}, {})
                try: Binds.scoped(key, hooks["build"], g, M, y, IW, st_)
                except Exception as ex:
                    Kit.add_section(g, M, y, IW, sh); Kit.add_label(g, "%s: %s" % (t, ex), M + 10, y + 10, Kit.HUE_BAD)
                    self._error(key, ex)
                y += sh + GAP
        if held: xy = LAYOUT.spot("hub") or (self.x, self.y); g.SetPos(int(xy[0]), int(xy[1]))
        else: self.x, self.y = Kit.place(g, self.x, self.y, w, h)
        self.H = h; self.g, self.store = g, store; G.AddControlOnDisposed(g, lambda *a: self._disposed(g))
        Kit.replace_gump(old, g, self.docked)
        if not held: g.SetInScreen()
        Kit.on_moved(g, self._moved); Kit.dispose(old)
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


class Launcher(object):
    W = 560; ROWS = 8; ROW = 28; SETTLE = 0.15; RECENT = 5; POS_KEY = "VirtueAssistant_launcher_pos"
    ONCE = "va.launcher.run"; GAP = 0.6; SOON = "too soon after the last run; press again."
    TITLE = "QUICK LAUNCHER"; TIP = "Quick launcher: find a rune, cell, window or option"; NAME = "Quick Launcher"
    ENTER_OFF = "launcher_Enter_key"; ORDER = ("rune", "cell", "window", "layout", "option", "command")
    FIELD_TIP = "Type words to find something; Enter runs the top row"
    HINT = "Type to find a rune, cell, window, layout, option or command"
    RUN = "Enter runs the top row; click a row to run it"; CLICK = "Click a row to run it"
    def __init__(self, host):
        self.host = host; self.g = self.tb = self.ver = self.pick = None; self.store = ({}, {})
        self.rows = []; self.recent = []; self.text = self.shown = self.status = ""; self.typed_at = 0.0
        self.enter = self.hooked = False; self.toggle = Kit.once(self._toggle_req, "va.launcher", 0.4)
        self.go = Kit.once(self._go, self.ONCE, self.GAP)
    def _toggle_req(self): Kit.pending.append(self._toggle); self.host.poke()
    def _toggle(self):
        if Kit.is_open(self.g): self.close(); return
        self.text = self.shown = ""; self.typed_at = 0.0; self.enter = False; self.ver = None
        self.rows, self.status = self.find(""); Binds.scoped("va.launcher", self._build)
    @staticmethod
    def score(words, text, extra=""):
        low = text.lower(); starts = low.replace("(", " ").replace(">", " ").split()
        more = extra.lower(); total = 0
        for w in words:
            pts = 3 if any(s.startswith(w) for s in starts) else 2 if w in low else 1 if w in more else 0
            if not pts: return 0
            total += pts
        return total
    def zones_on(self): s = dict.get(self.host.by_key, LAYOUT_OWNER); return s is not None and s.running
    def windows(self):
        out = []; slots = [s for s in self.host.slots if s.api is not None or s.lazy is not None]
        mine = [p[0] for s in slots for p in s.parts]
        for s in slots:
            if not s.parts: out.append(((s.key, (s.key,)), s.title)); continue
            for p in s.parts:
                key = "%s.%s" % (s.key, p[0]); docks = tuple(p[4][:1]) if len(p) > 4 else ()
                docks += (key,) + ((p[0],) if mine.count(p[0]) == 1 and p[0] not in self.host.by_key else ())
                out.append(((key, docks), s.part_title(p[0])))
        return out
    def commands(self):
        return (("history", "Alert history"),
                ("quiet", "Resume alerts" if ALERTS.quiet_on() else "Quiet alerts for 30 minutes"),
                ("backup", "Back up settings now"), ("settings", "Settings"), ("news", "What's new"))
    def options(self, words):
        c = self.host.config
        if c is None or c.mode == "alone": return [], True
        pages = c.settings_slots(); out = []
        for s in pages:
            for e in c.opt_index.get(s.key, ()):
                hay = " ".join((s.title, e[2], e[4], e[5], "option")).lower()
                if e[3] != "note" and all(w in hay for w in words): out.append((e, c._hit_text(e)))
        return out, all(s.key in c.opt_index for s in pages)
    def ask(self, name, q, n=None):
        fn = self.host.services.get(name)
        return (safe(lambda: fn(q, n or self.ROWS), None) or ()) if fn is not None else ()
    def find(self, q):
        words = str(q or "").lower().split()
        if not words:
            if self.recent: return [self._fresh(r) for r in self.recent], "Your last runs this session"
            return [], self.HINT
        found = []
        def add(label, kind, data, tip, extra="", pre=False):
            sc = self.score(words, label, extra) or (len(words) if pre else 0)
            if sc: found.append((-sc, self.ORDER.index(kind), len(found), (label, kind, data, tip)))
        for label, tok in self.ask("grimoire.find", q):
            add("Rune: " + label, "rune", tok, "Travel to %s" % label, "rune", True)
        for label, ref, kind in self.ask("actionbar.find", q):
            head = "Outfit" if kind == "outfit" else "Cell"
            add("%s: %s" % (head, label), "cell", (ref, label), "Use %s" % label, "cell " + kind, True)
        for key, title in self.windows():
            s = self.host.by_key.get(key[0]); on = s is not None and s.running
            add("Window: " + title, "window", key, ("Show %s" if on else "Turn %s on") % title, "window")
        if self.zones_on():
            for name in [LAYOUT_DEFAULT, LAYOUT_MIRRORED] + list(LAYOUT.layout_names()):
                add("Layout: " + name, "layout", name, 'Use the window layout "%s"' % name, "layout")
        opts, done = self.options(words)
        for e, text in opts: add("Option: " + text, "option", e, e[5] or "Open %s" % text, e[5] + " option")
        for key, cap in self.commands(): add(cap, "command", key, cap, "command")
        found.sort(key=lambda f: f[:3]); rows = [f[3] for f in found[:self.ROWS]]
        if not done: return rows, "Still reading settings pages; options appear as they are read"
        if not rows: return rows, 'Nothing matches "%s"' % str(q).strip()
        return rows, self.RUN
    def _fresh(self, row):
        label, kind, data = row[:3]
        if kind == "command": cap = dict(self.commands()).get(data, label); return (cap, kind, data, cap)
        if kind != "window": return row
        s = self.host.by_key.get(data[0]); title = label[len("Window: "):]
        return (label, kind, data, ("Show %s" if s is not None and s.running else "Turn %s on") % title)
    def _build(self):
        M, W, GAP = Kit.MARGIN, self.W, Kit.GAP; s = Kit.tscale; RH = Kit.pitch(self.ROW); rows = self.rows
        old = self.g; store = ({}, {}); yb = M + 30 + GAP; yr = yb + 44; caret = self._caret()
        h_body = 44 + RH * len(rows) + 28; H = yb + h_body + M
        g = G.CreateGump(True, True); Kit.add_window_frame(g, W, H); Kit.add_section(g, M, M, W - 2 * M, 30)
        Kit.add_label(g, self.TITLE, M + 30, M + 7, Kit.HUE_TITLE)
        Kit.art_button(g, store, "close", Kit.ART_CLOSE, W - M - 54, M + 4, None, "Close")
        Kit.add_section(g, M, yb, W - 2 * M, h_body)
        tb = Kit.add_textbox(g, self.text, M + 12, yb + 10, W - 2 * M - 24, numbers=False)
        self.hooked = self._hook(tb); Kit.with_tip(tb, self.FIELD_TIP if self.hooked else self.FIELD_TIP.split(";")[0])
        for i, r in enumerate(rows):
            Kit.art_button(g, store, "run%d" % i, Kit.ART_PLAY, M + 12, yr + RH * i, Kit.fit(r[0], W - 2 * M - 70),
                           r[3])
        text = self.status if self.hooked or self.status != self.RUN else self.CLICK
        Kit.add_label(g, Kit.fit(text, W - 2 * M - 24), M + 12, yr + RH * len(rows) + 4, Kit.HUE_INFO)
        sc = s if Kit.scale_window(g, s) else 1.0; WS, HS = int(round(W * sc)), int(round(H * sc))
        if Kit.is_open(old): x, y = int(old.GetX()), int(old.GetY())
        else:
            sw = Kit.screen()[0] or 1024; x, y = Kit.load_pos(self.POS_KEY, (max(0, (sw - WS) // 2), 120), (WS, HS))
        Kit.place(g, x, y, WS, HS, int(round(yb * sc))); Kit.add_front(g)
        Kit.on_moved(g, lambda: Kit.save_pos(self.POS_KEY, self.g)); self.g, self.tb, self.store = g, tb, store
        Kit.dispose(old); safe(tb.SetFocus); self._put_caret(tb, caret)
    def _caret(self):
        with Kit.quiet:
            n = int(self.tb.CaretIndex)
            if 0 <= n < len(self.text): return n
        return None
    @staticmethod
    def _put_caret(tb, n):
        if n is None: return
        with Kit.quiet: Kit.client_control(tb).TextBox.CaretIndex = n
    def _hook(self, tb):
        if self.ENTER_OFF in self.host.tz_off: return False
        try:
            import clr; import System; c = Kit.client_control(tb); ev = c.GetType().GetEvent("EnterPressed")
            h = clr.GetPythonType(ev.EventHandlerType)(self._enter_hit)
            ev.GetAddMethod(True).Invoke(c, System.Array[object]([h])); return True
        except Exception: return False
    def _enter_hit(self, sender=None, e=None): self.enter = True; self.host.poke()
    def rebuild(self):
        if Kit.is_open(self.g): Kit.save_pos(self.POS_KEY, self.g); Binds.scoped("va.launcher", self._build)
    def poll(self, now):
        if not Kit.is_open(self.g) or Kit.was_clicked(self.store, "close"): self.close(); return
        try: t = str(self.tb.Text or "")
        except Exception: t = self.text
        if t != self.text: self.text, self.typed_at = t, now
        if self.enter:
            self.enter = False; self.rows, self.status = self.find(self.text); self.shown = self.text
            if self.rows: self.run(0, True)
            else: self.rebuild()
            return
        for i in range(len(self.rows)):
            if Kit.was_clicked(self.store, "run%d" % i): self.run(i); return
        c = self.host.config; words = self.text.split()
        if words and c is not None and c.mode != "alone": safe(c._index_tick)
        ver = c.opt_ver if c is not None and c.mode != "alone" else 0
        if (self.text != self.shown and now - self.typed_at >= self.SETTLE) or (words and ver != self.ver):
            rows, status = self.find(self.text); self.shown, self.ver = self.text, ver
            if rows != self.rows or status != self.status: self.rows, self.status = rows, status; self.rebuild()
    def run(self, i, enter=False):
        if not 0 <= i < len(self.rows): return
        if 0.0 <= time.time() - Kit._fired.get(self.ONCE, 0.0) < self.GAP: self.say(self.SOON); return
        self.pick = (self.rows[i], enter); self.close(); self.go()
    def _go(self):
        row, enter = self.pick; label, kind, data = row[0], row[1], row[2]; sv = self.host.services; ok = False
        if kind == "rune":
            fn = sv.get("grimoire.go"); ok = fn is not None and bool(fn(data))
            if fn is None: self.say("Grimoire is off.")
        elif kind == "cell":
            fn = sv.get("actionbar.use"); ref, cap = data; name = cap.rsplit("  (", 1)[0]
            if fn is None: self.say("the Action Bar is off.")
            elif (cap, ref) not in [r[:2] for r in self.ask("actionbar.find", name, 200)]:
                self.say("%s is no longer on the Action Bar." % name)
            else:
                if enter: self.host.harm_conf = (None, 0, 0.0)
                ok = bool(fn(ref))
        elif kind == "window": ok = self._window(data)
        elif kind == "layout":
            ok = self.zones_on() and (data in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) or data in LAYOUT.layout_names())
            if ok: LAYOUT.use_windows(data)
            elif self.zones_on(): self.say('the window layout "%s" is gone.' % data)
            else: self.say("window layouts need the Interface module on.")
        elif kind == "option": ok = self._option(data)
        else: ok = self._command(data)
        if ok:
            self.recent = [row] + [r for r in self.recent if r[1:3] != row[1:3]]; del self.recent[self.RECENT:]
        return ok
    def say(self, text): API.SysMsg("%s: %s" % (self.NAME, text), Kit.HUE_BAD)
    def _window(self, key):
        part, keys = key; s = self.host.by_key.get(part); docks = dict(self.host.docks)
        if s is None: self.say("that window is no longer loaded."); return False
        dk = next((k for k in keys if k in docks), keys[0])
        if not s.running: self.host.dock_forget(dk); self.host.enable(part); return True
        d = docks.get(dk)
        if d is not None and safe(d.get("state")) != "open": safe(d.get("show")); self.host.dock_forget(dk)
        zid = LAYOUT.behind.get(dk)
        if zid is not None: LAYOUT.tab_pick(zid, dk)
        return True
    def _option(self, e):
        c = self.host.config
        if c is None or c.mode == "alone" or self.host.page_slot(e[0]) is None: return False
        c.opt_open, c.opt_mark = True, (e[0], e[1], e[6] if e[6] is not None else e[4], e[3])
        c.show_settings(e[0]); return True
    def _command(self, key):
        h = self.host
        if key == "history": h.alert_log.open()
        elif key == "quiet": ALERTS.toggle_quiet()
        elif key == "backup": BackupPage.ask(("backup", "by hand"))
        elif key == "settings":
            if h.config is None: return False
            h.config.request_tab = "settings"
        elif key == "news": return h.whats_new.show()
        return True
    def close(self):
        g, self.g, self.tb = self.g, None, None; self.enter = False
        if Kit.is_open(g): Kit.save_pos(self.POS_KEY, g)
        Kit.dispose(g); self.store = ({}, {})


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
        self.down = True; self.sweep_at = 0.0; self.keep_sig = None
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
        if self.last is not None and p is not None and g in self.members: self.last[g] = p
        self.drag.pop(g, None); self.moved.discard(g); self.by_code[g] = time.time()
    def skip_gump(self, g, keep_fresh=False):
        if not keep_fresh: LAYOUT.fresh_adds.discard(g)
        if g in self.members: self.members.discard(g); self.gumps.remove(g)
        if self.last is not None: self.last.pop(g, None)
    def exempt(self, g):
        if g is None: return
        self.add(g); self.no_snap.add(g); self.links.pop(g, None)
        for f, l in list(self.links.items()):
            if l is g: self.links.pop(f, None)
    def attach(self, follower, leader):
        if follower is None or leader is None or follower is leader: return
        self.skip_gump(follower, keep_fresh=True); self.attached[follower] = leader; self._fmap = None; self.add(leader)
    def detach(self, follower):
        self._fmap = None; was = self.attached.pop(follower, None) is not None
        if not Kit.is_open(follower): self._forget(follower)
        elif was: self.add(follower)
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
        for f, l in list(self.links.items()):
            if l is g: self.links.pop(f, None)
        for f, l in list(self.attached.items()):
            if l is not g: continue
            self.attached.pop(f, None)
            if Kit.is_open(f): self.add(f)
        if self.last is not None: self.last.pop(g, None)
    def swap(self, old, new):
        if old is None or new is None or old is new: return
        for d in (self.links, self.attached):
            for f, l in list(d.items()):
                if l is old: d[f] = new
        for d in (self.links, self.attached, self.drag, self.drag_key, self.drag_rect, self.drag_end, self.by_code,
                  self.moved_cb):
            if old in d: v = d.pop(old); d.setdefault(new, v)
        for s in (self.moved, self.dragged, self.no_snap):
            if old in s: s.discard(old); s.add(new)
        if self.last is not None and old in self.last:
            p, q = self.pos(new), self.last.pop(old)
            if new not in self.last: self.last[new] = q if p is None else p
        was = old in self.members; Kit._pinned.discard(old)
        if was:
            self.members.discard(old); self.members.add(new)
            self.gumps = [new if x is old else x for x in self.gumps if x is not new]
        if new in self.attached or not was: self.skip_gump(new, keep_fresh=new in self.attached)
        self._fmap = None
    def _prune(self):
        live = []
        for g in self.gumps:
            if Kit.is_open(g): live.append(g)
            else: self._forget(g)
        for g in [g for d in (self.moved_cb, self.by_code, self.attached) for g in d if g not in self.members]:
            if not Kit.is_open(g): self._forget(g)
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
        now = time.time() if now is None else now; boot = HOST.booting()
        if now < self.next and self.next - now <= SNAP_EVERY and not boot: return
        self.next = now + SNAP_EVERY
        if LAYOUT.arrange and not self.drag and API.IsKeyPressed("ESCAPE"): LAYOUT.set_arrange(False)
        pressed = self.pressed(); self.down = pressed is not False or bool(self.drag)
        if pressed is not True:
            if now >= self.keep_at:
                self.keep_at = now + (0.0 if boot else KEEP_EVERY)
                if now >= self.sweep_at or self._keep_sig() != self.keep_sig:
                    self.sweep_at = now + KEEP_SWEEP; self.keep(); self.keep_sig = self._keep_sig()
                elif boot and LAYOUT.assign and LAYOUT.retry_due(now):
                    self.keep(light=bool(LAYOUT.fresh_adds) and not LAYOUT.fresh)
            elif LAYOUT.assign and (LAYOUT.fresh or LAYOUT.fresh_adds or LAYOUT.retry_due(now)):
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
                if pressed is False and g not in drag: continue
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
    def chain(self, g):
        down = set([g]); n = 0
        while len(down) != n: n = len(down); down.update([o for o, l in self.links.items() if l in down])
        return down
    def snap(self, g, live):
        if self._fmap is not None: return self._snap(g, live)
        self._build_fmap()
        try: return self._snap(g, live)
        finally: self._fmap = None
    def _snap(self, g, live):
        r = self.rect(g)
        if r is None: return
        x, y, w, h = r; corner = None; ex = ey = None; links = self.links; targets = []; down = self.chain(g)
        for o in live:
            if o in down or not self.visible(o) or o in self.no_snap: continue
            targets.append((o, o))
            for f in self.followers(o):
                if f not in down and self.visible(f): targets.append((f, o))
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
    def _keep_sig(self):
        if self.down or Kit._pend or LAYOUT.arrange or LAYOUT.dirty or LAYOUT.fresh or LAYOUT.fresh_adds:
            return object()
        out = [Kit.screen(), safe(LAYOUT.occupied)]
        for g in self.gumps + list(self.attached) + [cw for cw in ClientWin.found.values() if cw is not None]:
            try: out.append((id(g), Kit.is_open(g), Kit.rect(g), bool(g.IsVisible)))
            except Exception: out.append(id(g))
        return out
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
            elif self.attached.get(f) is l:
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
                    if g in self.drag or self.links.get(g) in self.members: continue
                    r = self.rect(g)
                    if r is None: continue
                    x, y, w, h = r; nx = Kit.remap_axis(x, w, old[0], W); ny = Kit.remap_axis(y, h, old[1], H)
                    grp = [f for f in self.chain(g) if f in self.members and f not in self.drag]
                    if (nx, ny) != (x, y):
                        for f in grp: self._shift(f, nx - x, ny - y)
                    if len(grp) > 1 and g not in LAYOUT.held: self.keep_one(g, [f for f in grp if f not in LAYOUT.held])
            Kit.note_screen((W, H))
        held = LAYOUT.held
        for g in live:
            if new is not None and g not in new: continue
            if g not in self.drag and g not in held: self.keep_one(g)
        try: LAYOUT.keep(W, H, new)
        except Exception as ex: HOST._tell("%s: layout error: %s%s" % (APP_NAME, ex, _error_where()))
        if (self.moved or self.lost) and not self.drag: self._tell_moved()
    def keep_one(self, g, grp=None):
        r = self.rect(g)
        if r is None or (Kit._behind and self.attached.get(g) in Kit._behind): return False
        x0, y0, x1, y1 = r[0], r[1], r[0] + r[2], r[1] + r[3]; grp = grp or [g]
        for f in [m for m in grp if m is not g] + [f for m in grp for f in self.followers(m)]:
            rf = self.rect(f)
            if rf is not None and self.visible(f):
                x0, y0 = min(x0, rf[0]), min(y0, rf[1]); x1, y1 = max(x1, rf[0] + rf[2]), max(y1, rf[1] + rf[3])
        nx, ny = Kit.clamp(x0, y0, x1 - x0, y1 - y0)
        if (nx, ny) == (x0, y0): return False
        for m in grp: self._shift(m, nx - x0, ny - y0)
        return True
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
            with Kit.quiet: import System; g.LayerOrder = System.Enum.Parse(g.LayerOrder.GetType(), "Under")
        Kit.add_front(g); SNAP.skip_gump(g)
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
        Kit.add_label(g, "GRID %d px: windows snap to its lines, the screen's corners, edges and centre  (Settings > "
                      "Interface or the Action Bar's Grid button hides it)" % step, m + 8, m + 4, Kit.HUE_TITLE)
        self.g = g; self.drawn = (W, H, step); Grid.show_overlay(g, 0, 0, W, H, True); Kit.dispose(old)


LAYOUT_VAR = "VirtueAssistant_layout"
LAYOUT_ACTIVE = "VirtueAssistant_layout_active"
LAYOUT_LIST = "VirtueAssistant_layout_list"
LAYOUT_NAMED = "VirtueAssistant_layout_%s"
FRAMES_ACTIVE = "VirtueAssistant_frames_active"
FRAMES_LIST = "VirtueAssistant_frames_list"
FRAMES_NAMED = "VirtueAssistant_frames_%s"
LAYOUT_OPTS = "VirtueAssistant_layout_opts"
LAYOUT_DEFAULT = "Default"
LAYOUT_MIRRORED = "Mirrored"
LAYOUT_MINE = "Default (mine)"
LAYOUT_GONE = frozenset(("spelltimers", "bandage", "swing"))
DUNGEON_AREAS = ((0, 5120, 0, 6143, 2303), (0, 5404, 3099, 5480, 3166))
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
ZONE_MIN_W, ZONE_MIN_H, ZONE_CAP = 96, 64, 64
ZONE_COLORS = {"w": "#3A78C8", "k": "#3AA060", "r": "#C88A3A"}
ZONE_KINDS = (("w", "window"), ("k", "keep clear"), ("r", "reserved"))
ZONE_STACKS = (("d", "down"), ("u", "up"), ("r", "right"), ("l", "left"), ("t", "tabs"))
TAB_H = 26
TAB_X = -20000
SHRINK_MAX = 6
LAYOUT_OWNER = "interface"
SEAM_PAD = 6
REVEAL_H = 14
REVEAL_HOLD = 0.6
SEAM_WAIT = 2.0
SEAM_RETRY = 0.1


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
                 "hug", "arch", "overlap", "lock", "solo", "free", "exact")
    def __init__(self, id, kind="w", rect=(0, 0, 200, 200), pins="", mins=(0, 0), stack="d",
                 prio=0, fit="w", hug=False, arch=False, overlap=False, lock=False, solo=False, free=False):
        self.id = str(id); self.kind = kind if kind in ("w", "k", "r") else "w"; self.rect = tuple(int(v) for v in rect)
        self.pins = "".join(c for c in str(pins or "").upper() if c in "LTRBXY")
        self.min = (int(mins[0]), int(mins[1])); self.stack = stack if stack in ("d", "u", "r", "l", "t") else "d"
        self.prio = max(0, min(SHRINK_MAX, int(prio))); self.fit = fit if fit in ("w", "s", "n") else "w"
        self.hug = bool(hug) and self.kind == "w"; self.arch = bool(arch) and self.kind == "k"
        self.overlap = bool(overlap); self.lock = bool(lock); self.solo = bool(solo); self.free = bool(free)
        self.px = None; self.squeezed = False; self.exact = None
    def kind_name(self): return dict(ZONE_KINDS)[self.kind]
    def stack_name(self): return dict(ZONE_STACKS)[self.stack]
    def copy(self):
        z = Zone(self.id, self.kind, self.rect, self.pins, self.min, self.stack, self.prio,
                 self.fit, self.hug, self.arch, self.overlap, self.lock, self.solo, self.free)
        z.px = tuple(self.px) if self.px else None; z.exact = self.exact; return z
    def set_px(self, x, y, w, h, W, H):
        w, h = max(1, int(w)), max(1, int(h))
        if W > 0: w = min(w, W); x = _clampv(int(x), 0, W - w)
        if H > 0: h = min(h, H); y = _clampv(int(y), 0, H - h)
        self.px = (int(x), int(y), w, h)
        if W > 0 and H > 0:
            self.rect = (int(round(1000.0 * x / W)), int(round(1000.0 * y / H)),
                         int(round(1000.0 * w / W)), int(round(1000.0 * h / H)))
            self.exact = self.px + (int(W), int(H))
    def note_pins(self, W, H):
        if not self.px or W <= 0 or H <= 0: return
        x, y, w, h = self.px; lim = 0.5 if self.free else SNAP_DIST
        self.pins = "".join(c for c, d in (("L", x), ("T", y), ("R", W - (x + w)), ("B", H - (y + h)),
                                           ("X", abs((x + w / 2.0) - W / 2.0)), ("Y", abs((y + h / 2.0) - H / 2.0)))
                            if d <= lim)
    def save_text(self):
        flags = (self.hug, self.arch, self.overlap, self.lock, self.solo, self.free)
        n = (6 if self.free else 5 if self.solo else 4 if self.overlap or self.lock else
             2 if self.hug or self.arch else 0)
        extra = "".join(":%d" % v for v in flags[:n])
        if self.free and self.exact: extra += ":%d,%d,%d,%d,%d,%d" % self.exact
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
            hug, arch, overlap, lock, solo, free = [len(f) > i and f[i].strip() == "1" for i in range(8, 14)]
            z = Zone(f[0].strip(), f[1].strip(), rect, f[3], mn, f[5].strip(), int(f[6]), fit,
                     hug, arch, overlap, lock, solo, free)
            e = f[14].strip() if free and len(f) > 14 else ""
            if re.match(r"^\d+(,\d+){5}$", e):
                e = tuple(int(v) for v in e.split(","))
                if e[2] > 0 and e[3] > 0 and e[4] > 0 and e[5] > 0: z.exact = e
            return z
        except Exception: return None


class ZoneSet(object):
    def __init__(self, name, zones=None, grid=GRID_DEFAULT, screen=(0, 0), generated=False):
        self.name = str(name); self.zones = list(zones or []); self.grid = int(grid or GRID_DEFAULT)
        self.screen = (int(screen[0]), int(screen[1])); self.generated = generated; self.skipped = []; self.ver = 2
        self.needs = {}; self.dups = 0
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
                with Kit.quiet:
                    k, v = item.split("=", 1)
                    if k == "grid": grid = int(v)
                    elif k == "screen": w, h = v.lower().split("x"); screen = (int(w), int(h))
                    elif k == "v": ver = int(v)
        zs = ZoneSet(name, [], grid, screen); zs.ver = ver; seen = set()
        for p in parts:
            if not p.strip(): continue
            z = Zone.parse(p) if len(zs.zones) < ZONE_CAP else None
            if z is None:
                if len(zs.skipped) < ZONE_CAP: zs.skipped.append(p.split(":")[0].strip() or "?")
            elif z.id in seen: zs.dups += 1
            else: seen.add(z.id); zs.zones.append(z)
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
            if not any(s[0] in occupied for s in LEFT_SLOTS if s[3] == "w"):
                lo = spill if spill and "L0" in occupied else 0; gx, gw = lo, gw + cx - lo
            if not any(s[0] in occupied for s in RIGHT_SLOTS if s[3] == "w"):
                gw = (W - spill if spill and "R0" in occupied else W) - gx
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
            drawn = [(z, z.rect, z.exact) for z in self.zones]; self.needs, needs = {}, self.needs
            self.reflow(W, H, step); self.needs = needs; self._apply_needs(W, H); self._keep_clear(W, H)
            for z, r, e in drawn: z.rect, z.exact = r, e
            return
        oldW, oldH = self.screen if self.screen[0] > 0 and self.screen[1] > 0 else (W, H)
        flush = self._flush_pairs(oldW, oldH); led = set((b, side) for a, b, side in flush)
        def on_grid(v, limit, free):
            st = 1 if free else step; return _clampv(int(round(float(v) / st)) * st, 0, limit)
        exact = set()
        for z in self.zones:
            l, t, w, h = z.rect; f = z.free; e = z.exact if f and z.exact and z.exact[4:] == (W, H) else None
            if e is not None: exact.add(z.id); x0, y0, x1, y1 = e[0], e[1], e[0] + e[2], e[1] + e[3]
            else:
                x0, y0 = on_grid(W * l / 1000.0, W, f), on_grid(H * t / 1000.0, H, f)
                x1, y1 = on_grid(W * (l + w) / 1000.0, W, f), on_grid(H * (t + h) / 1000.0, H, f)
            if f: z.pins = "".join(c for c, on in (("L", x0 <= 0), ("T", y0 <= 0), ("R", x1 >= W), ("B", y1 >= H))
                                   if on)
            if "L" in z.pins: x0 = 0
            if "T" in z.pins: y0 = 0
            if "R" in z.pins: x1 = W
            if "B" in z.pins: y1 = H
            if "X" in z.pins and "L" not in z.pins and "R" not in z.pins and (z.id, "h") not in led:
                half = (x1 - x0) // 2; x0, x1 = W // 2 - half, W // 2 - half + (x1 - x0)
            if "Y" in z.pins and "T" not in z.pins and "B" not in z.pins and (z.id, "v") not in led:
                half = (y1 - y0) // 2; y0, y1 = H // 2 - half, H // 2 - half + (y1 - y0)
            z.px = (x0, y0, max(1, x1 - x0), max(1, y1 - y0))
        edge = {}
        for a, b, side in flush:
            za, zb = self.by_id(a), self.by_id(b)
            if za is None or zb is None or za.px is None or zb.px is None or (a in exact and b in exact): continue
            ax, ay, aw, ah = za.px; bx, by, bw, bh = zb.px
            if side == "h":
                nx = max(ax + aw, edge.get((b, side), 0)); right = W if "R" in zb.pins else bx + bw
                if right - nx >= ZONE_MIN_W: zb.px = (nx, by, right - nx, bh); edge[(b, side)] = nx
            else:
                ny = max(ay + ah, edge.get((b, side), 0)); bottom = H if "B" in zb.pins else by + bh
                if bottom - ny >= ZONE_MIN_H: zb.px = (bx, ny, bw, bottom - ny); edge[(b, side)] = ny
        for z in self.zones:
            if z.kind == "k": continue
            x, y, w, h = z.px
            if w < z.min[0]: w = min(z.min[0], max(w, self._free(z, 0, W) - x))
            if h < z.min[1]: h = min(z.min[1], max(h, self._free(z, 1, H) - y))
            z.set_px(x, y, w, h, W, H); z.squeezed = z.prio > 0 and z.px[3] < z.min[1]
        for z in self.zones:
            if z.kind != "k" and not z.overlap and self.overlaps(z, keep=False):
                p = z.px
                if not self.push_clear(z, W, H, keep=False): z.px = p
        for z in self.zones:
            if z.kind == "k" and not z.overlap: z.set_px(*(ZoneSet.cut_clear(z, self.zones) + (W, H)))
        for z in self.zones: z.set_px(z.px[0], z.px[1], z.px[2], z.px[3], W, H)
        self.screen = (W, H)
    @staticmethod
    def cut_clear(z, zones):
        ws = [o.px for o in zones if o is not z and o.kind == "w" and o.px is not None]
        def hit(r, o): return o[0] < r[0] + r[2] and r[0] < o[0] + o[2] and o[1] < r[1] + r[3] and r[1] < o[1] + o[3]
        def cuts(r, o):
            x, y, w, h = r; ox, oy, ow, oh = o
            return [c for c in ((x, y, ox - x, h), (ox + ow, y, x + w - ox - ow, h), (x, y, w, oy - y),
                                (x, oy + oh, w, y + h - oy - oh)) if c[2] >= ZONE_MIN_W and c[3] >= ZONE_MIN_H]
        def left(r, rest):
            for o in rest:
                c = cuts(r, o) if hit(r, o) else None
                if c: r = max(c, key=lambda q: q[2] * q[3])
            return r[2] * r[3]
        r = tuple(z.px)
        for k, o in enumerate(ws):
            c = cuts(r, o) if hit(r, o) else None
            if c: r = max(c, key=lambda q: left(q, ws[k + 1:]))
        return r[0], r[1], max(1, r[2]), max(1, r[3])
    def _flush_pairs(self, W, H):
        out = []; px = {}
        for z in self.zones:
            l, t, w, h = z.rect; px[z.id] = (W * l / 1000.0, H * t / 1000.0, W * w / 1000.0, H * h / 1000.0)
        for a in self.zones:
            ax, ay, aw, ah = px[a.id]
            for b in self.zones:
                if a is b: continue
                bx, by, bw, bh = px[b.id]; f = a.free or b.free
                tw, th = (1.0 + W / 1000.0, 1.0 + H / 1000.0) if f else (SNAP_DIST, SNAP_DIST)
                if abs(bx - (ax + aw)) <= tw and min(ay + ah, by + bh) - max(ay, by) > th: out.append((a.id, b.id, "h"))
                if abs(by - (ay + ah)) <= th and min(ax + aw, bx + bw) - max(ax, bx) > tw: out.append((a.id, b.id, "v"))
        def rank(zid): z = self.by_id(zid); return -len(z.pins) if z else 0
        out.sort(key=lambda p: (rank(p[0]), rank(p[1]))); return out
    def _free(self, z, i, lim):
        r, j = z.px, 1 - i
        for o in self.zones:
            if o is z or o.kind == "k" or o.px is None: continue
            p = o.px
            if p[i] >= r[i] + r[i + 2] and p[j] < r[j] + r[j + 2] and r[j] < p[j] + p[j + 2]: lim = min(lim, p[i])
        return lim
    def overlaps(self, z, px=None, keep=True):
        x, y, w, h = px or z.px; out = []
        if z.overlap: return out
        for o in self.zones:
            if o is z or o.px is None or o.overlap or (not keep and o.kind == "k"): continue
            if (z.kind == "r" and o.kind == "k") or (z.kind == "k" and o.kind == "r"): continue
            ox, oy, ow, oh = o.px
            if ox < x + w and x < ox + ow and oy < y + h and y < oy + oh: out.append(o)
        return out
    def push_clear(self, z, W, H, step=None, keep=True):
        for _ in range(12):
            hits = self.overlaps(z, keep=keep)
            if not hits: return True
            x, y, w, h = z.px; cands = []
            for o in hits:
                ox, oy, ow, oh = o.px
                for nx, ny in (((ox - w), y), ((ox + ow), y), (x, (oy - h)), (x, (oy + oh))):
                    if not (0 <= nx <= W - w and 0 <= ny <= H - h): continue
                    clear = not self.overlaps(z, (nx, ny, w, h), keep)
                    if clear and step:
                        gx, gy = (int(round(float(nx) / step)) * step, int(round(float(ny) / step)) * step)
                        if (0 <= gx <= W - w and 0 <= gy <= H - h and not self.overlaps(z, (gx, gy, w, h), keep)):
                            nx, ny = gx, gy
                    cands.append((0 if clear else 1, abs(nx - x) + abs(ny - y), nx, ny))
            if not cands: return False
            cands.sort(); z.set_px(cands[0][2], cands[0][3], w, h, W, H)
            if cands[0][0] == 0: return True
        return not self.overlaps(z, keep=keep)
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
                others = sorted([o for o in self.zones if o is not z and o.kind != "k" and not o.overlap
                                 and o.px is not None and o.px[j] < r[j] + r[j + 2] and r[j] < o.px[j] + o.px[j + 2]],
                                key=lambda o: o.kind != "r")
                if pin in z.pins or a + s / 2.0 >= S / 2.0:
                    na = max(0, a - grow)
                    for o in others:
                        p = list(o.px)
                        if p[i] < a and p[i] + p[i + 2] > na:
                            if o.kind == "r": na = max(na, min(a, p[i] + p[i + 2])); continue
                            cut = min(a, max(p[i] + max(o.min[i], (ZONE_MIN_W, ZONE_MIN_H)[i]), na))
                            p[i + 2] = cut - p[i]; o.px = tuple(p)
                            na = max(na, cut)
                    r[i], r[i + 2] = na, s + (a - na)
                else:
                    ne = min(S, a + s + grow)
                    for o in others:
                        p = list(o.px)
                        if p[i] >= a + s and p[i] < ne:
                            if o.kind == "r": ne = p[i]; continue
                            top = max(a + s, min(p[i] + p[i + 2] - max(o.min[i], (ZONE_MIN_W, ZONE_MIN_H)[i]), ne))
                            p[i], p[i + 2] = top, p[i] + p[i + 2] - top; o.px = tuple(p); ne = min(ne, top)
                    r[i + 2] = ne - a
            z.px = tuple(r)
    def fill_gaps(self, W, H, step):
        step = max(8, int(step or GRID_DEFAULT))
        order = sorted(self.zones, key=lambda z: {"w": 0, "r": 1, "k": 2}[z.kind])
        for z in order:
            if z.overlap or z.lock: continue
            r = list(z.px); st = 1 if z.free else step
            for i, lo, hi, S in ((0, "L", "R", W), (1, "T", "B", H)):
                lim = max([0] + [o.px[i] + o.px[i + 2] for o in self.overlaps_side(z, lo)])
                n = 0 if lim == 0 else ((lim + st - 1) // st) * st
                if n < r[i]: r[i], r[i + 2] = n, r[i + 2] + (r[i] - n)
                lim = min([S] + [o.px[i] for o in self.overlaps_side(z, hi)]); e = S if lim == S else (lim // st) * st
                if e > r[i] + r[i + 2]: r[i + 2] = e - r[i]
                z.px = tuple(r)
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
                for _ in range(len(same)):
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
            with Kit.quiet:
                if not raw.IsDisposed: cw = ClientWin(kind, raw); break
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
        own, self.own, self.tries = self.own, None, 0; self._rc = None; self.warned = False; self.fail = {}
        Kit.put_var(ClientWin.LOCK_VAR % self.kind, "")
        if own is None or self.IsDisposed: return
        with Kit.quiet:
            self._lock(bool(own[5]))
            if not own[5]: self.raw.CanMove = own[4]
            Tz.call(self.raw, "ResizeWindow", (ClientWin.point(own[2], own[3]),)); self.SetPos(own[0], own[1])
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
        Tex.parts["ok"] = Tex.ok; return Tex.ok
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
            with Kit.quiet:
                if table.ContainsKey(name): tex = table[name]; table.Remove(name); tex.Dispose()
    @staticmethod
    def has(name):
        if not Tex.ok: return False
        table = Tex.parts["table"]
        with Kit.quiet: return bool(table.ContainsKey(name)) and not table[name].IsDisposed
        return False
    @staticmethod
    def control(g, name, x, y, w, h):
        t = G.LegionTextureControl(name, int(w), int(h)); t.SetRect(int(x), int(y), int(w), int(h))
        safe(lambda: t.SetAcceptMouseInput(False)); g.Add(t); return t


class Layout(object):
    def __init__(self):
        self.wins = {}; self.assign = {}; self.frames = None; self.frames_name = LAYOUT_DEFAULT; self.layout_name = ""
        self.game_grows = True; self.fit_view = True; self.screen = None; self.dirty = True
        self.occ = None; self.gump_key = {}
        self.placed = {}; self.titles = {}; self.min_seen = {}; self.loaded = False; self.page_refresh = False
        self.enabled = True; self.seamless = False; self.gv_off_done = False; self.seam_skip = {}; self.seam_wait = {}
        self.hooks = {}; self.owner = {}; self.fitted = {}; self.base = {}; self.fresh = False; self.fresh_adds = set()
        self.client_seen = {}; self.journal_held = self.journal_px = None; self.pair_tried = None
        self.client_settle = {}
        self.misfit = {}; self.fallback = {}; self.client_told = set(); self.chat_seen = (0.0, None); self.held = {}
        self.arrange = False; self.arrange_last = 0.0; self.arrange_g = None; self.arrange_lit = {}
        self.arrange_hot = None; self.client_target = {}; self.repair_at = 0.0; self.repair_told = set()
        self.freed = None; self.page_preview = ""; self.homes = None; self.back_told = False; self._arrange_sig = None
        self.rev = {}; self.retry_at = 0.0; self.slot_was = {}; self.bags_swept = False
        self.reclaim_undo = self._vp_fields = self.gv_applied = self.small_said = None
        self._undo_read = self.gv_small_told = self.gv_checked = self.need_due = self.migrating = False
        self.situ = {"on": False, "base": ""}; self.situ_now = self.situ_pend = self.situ_last = self.situ_back = None
        self.situ_at = 0.0; self.situ_busy = False; self.situ_bank = (-1e9, 0, 0, -1)
        self.tabs = {}; self.behind = {}; self.strips = {}; self.planned = {}; self.plan_occ = self.plan_sig = None
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
        if cw is None: self.journal_px = None; return
        x, y, w, h = z.px; h = self._clear_of_chat(x, y, w, h, H); cw.fit(w, h); self.journal_px = (x, y, w, h)
        try:
            if (cw.GetX(), cw.GetY()) != (x, y): cw.SetPos(x, y)
        except Exception: pass
        cw.report(); self.journal_held = cw
    def beside_journal(self, x, y, w, h):
        r = self.journal_px
        if r is None or not (r[0] <= x < r[0] + r[2] and y < r[1] + r[3] and r[1] < y + h): return x
        W = Kit.screen()[0]; return r[0] + r[2] if not W or r[0] + r[2] + w <= W else max(0, r[0] - w)
    def load(self):
        self.freed = None; self.homes = None; self.repair_told = set(); self.back_told = False; self.loaded = True
        self.bags_swept = False; self.planned, self.plan_occ, self.plan_sig = {}, None, None
        self.seam_skip = {}; self.seam_wait = {}
        if "worldmap" not in self.wins:
            self.add("worldmap", self._client_getter("worldmap", "worldmap"), "TazUO's World Map",
                     {"fit": self._client_fit("worldmap"), "exact": True, "client": True,
                      "inset": ClientWin.INSET.get("worldmap", 0)})
        self.frames_name = Kit.get_var(FRAMES_ACTIVE, LAYOUT_DEFAULT) or LAYOUT_DEFAULT
        if self.frames_name != LAYOUT_DEFAULT and self.frames_name not in self.frame_names():
            self.frames_name = LAYOUT_DEFAULT
        self.layout_name = Kit.get_var(LAYOUT_ACTIVE, ""); opts = Kit.get_var(LAYOUT_OPTS, "game=1")
        self.game_grows = "game=0" not in opts; self.fit_view = "fit=0" not in opts; raw = Kit.get_var(LAYOUT_VAR, "")
        self.seamless = "seam=1" in opts; owner = dict.get(HOST.by_key, LAYOUT_OWNER)
        self.enabled = bool(owner is not None and owner.enabled and owner.api is not None)
        self.assign = self.parse_windows(raw)[1]
        if raw and raw != self.windows_text() and any(k.strip() in LAYOUT_GONE for part in str(raw).split(";")
                if "=" in part and part.split("=", 1)[0].strip() != "frames" for k in part.split("=", 1)[1].split(",")):
            self.save_assign()
        self.frames = None; self.dirty = True; self.situ_load()
        self.tabs = self._tabs_parse(Kit.get_var(self.TABS_VAR, ""))
    def save_assign(self):
        Kit.put_var(LAYOUT_VAR, self.windows_text())
        if not self.situ_busy: self._note_homes()
    RECLAIM_VAR = "VirtueAssistant_reclaim_undo"; RECLAIM_FIXED = "VirtueAssistant_reclaim_fixed"
    def _undo_load(self):
        if self.reclaim_undo is None and not self._undo_read:
            self._undo_read = True; p = str(Kit.get_var(self.RECLAIM_VAR, "") or "").split("|", 2)
            if len(p) == 3 and p[0]: self.reclaim_undo = (p[0], p[2], None, p[1] == "1")
        return self.reclaim_undo
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
        others = [o for o in zs.zones if o.px is not None]; changed = []
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
        if not moved or now[0] * now[1] <= was[0] * was[1]:
            self.dirty = True
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
        Kit.say("%d frame zone%s Reclaim space stretched in layout \"%s\" put right; Settings > Interface's "
                   "Undo puts it back." % (len(tall), "" if len(tall) == 1 else "s", zs.name), Kit.HUE_GOOD)
    def refit_all(self): self.dirty = self.fresh = self.page_refresh = True; self.seam_skip = {}; self.seam_wait = {}
    def save_opts(self):
        Kit.put_var(LAYOUT_OPTS, "game=%d;fit=%d;seam=%d;art=plain" % (self.game_grows, self.fit_view, self.seamless))
    def set_enabled(self, on):
        on = bool(on)
        if on == self.enabled: return
        if not on: self.set_arrange(False, tell=False)
        self.enabled, self.gv_off_done = on, False; self.refit_all(); HOST.poke()
    def _off(self):
        if self.behind or self.strips or Kit._behind: self._tabs_off()
        Seam.undo_all()
        for key in list(self.fitted): self._unfit(key)
        for key in list(self.placed):
            g = self.gump_of(key); info = Kit.scroll_info(g) if g is not None else None
            if info is not None:
                with Kit.quiet:
                    Kit.place(g, int(g.GetX()), int(g.GetY()), info["w"], info["h"], info["head"]); Kit.moved_by_code(g)
        self.placed = {}
        if self.held: self._release(set())
        held, self.journal_held, self.journal_px = self.journal_held, None, None
        if held is not None: held.free()
        if not self.gv_off_done: self.gv_off_done = True; self.game_view_restore()
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
    def windows_text(self, frames=None, assign=None):
        a = self.assign if assign is None else assign
        return ";".join(["frames=%s" % (frames or self.frames_name)] + [
            "%s=%s" % (zid, ",".join(a[zid])) for zid in sorted(a) if a[zid]])
    RESERVED = ("list", "active", "opts", "situations", "tabs", "freed", "homes", "editor_pos")
    @staticmethod
    def _names(var): return [n for n in Kit.get_var(var, "").split(",") if n.strip()]
    def frame_names(self): return self._names(FRAMES_LIST)
    def layout_names(self): return self._names(LAYOUT_LIST)
    @staticmethod
    def clean_name(name, fallback):
        name = re.sub(r"[^\w ()'-]", "", str(name or "")).strip()[:24]
        if name in Layout.RESERVED: name += " 2"
        return name or fallback
    def add(self, key, getter, title=None, hooks=None, owner=None):
        key = str(key)
        if key in LAYOUT_GONE: return
        t = self.titles[key] = str(title or key); self.wins[key] = (getter, t)
        self.hooks[key] = hooks if hooks is not None else {}
        if owner is not None: self.owner[key] = owner
        self.fitted.pop(key, None); self.dirty = True
    def remove(self, key):
        key = str(key)
        for d in (self.wins, self.placed, self.hooks, self.owner, self.fitted, self.base, self.slot_was, self.min_seen):
            d.pop(key, None)
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
        for key in list(self.wins) + sorted(set(k for ks in self.assign.values() for k in ks if k not in self.wins)):
            mk = self.owner_of(key)[0]; s = dict.get(HOST.by_key, mk) if mk else None; t = self.title_of(key)
            if s is not None and s.title != t: t = "%s: %s" % (s.title, t)
            out.append((key, t if key in self.wins else t + " (not open)"))
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
        self.save_assign(); W, H = Kit.screen(); empty = old is not None and not self.assign.get(old)
        if key == "bag" and empty and W > 0 and H > 0 and self.drop_empty_bags(self.frames_in_use(W, H), W, H, (old,)):
            self.frames, self.dirty = None, True
        if not zid: self.free_scrolled()
        self.placed.pop(key, None); self.dirty = True; self.page_refresh = True
        if tell:
            API.SysMsg(('%s: %s is in zone "%s".' % (APP_NAME, self.title_of(key), zid)) if zid else
                       ("%s: %s is free (it stays where you put it)." % (APP_NAME, self.title_of(key))), Kit.HUE_GOOD)
        HOST.poke()
    def zone_of(self, key):
        zid = self.rev.get(key)
        if zid is not None and key in self.assign.get(zid, ()): return zid
        self.rev = dict((k, z) for z, keys in self.assign.items() for k in keys); return self.rev.get(key)
    def need(self, key, w, h):
        zid = self.zone_of(str(key)); zs = self.frames
        if zid is None or zs is None: return
        z = zs.by_id(zid); want = (w, h + TAB_H if h and z is not None and z.stack == "t" else h) if (w or h) else None
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
        tab = TAB_H if z.stack == "t" else 0
        return (max(1, int(W * z.rect[2] / 1000.0)), max(1, int(H * z.rect[3] / 1000.0) - tab))
    def holds(self, key):
        if not self.enabled: return False
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
        on = bool(on) and self.enabled
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
        tip = "Drag windows onto zones; Esc or Done to finish"; tw = Kit.text_w(tip) + 24
        Kit.add_box(g, (W - tw) // 2, 6, tw, 26, 0.85, "#000000")
        Kit.add_label(g, tip, (W - tw) // 2 + 12, 10, Kit.HUE_TITLE)
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
            with Kit.quiet: return int(mn[0]), int(mn[1])
        g = g if g is not None else self.gump_of(key)
        if isinstance(g, ClientWin):
            m = g._min_size()
            if m[0] > 0 or m[1] > 0: return m
        return None
    def _min_at(self, key, w, h, g=None):
        fn = (self.hooks.get(key) or {}).get("min_for")
        if callable(fn):
            with Kit.quiet: mn = fn(w, h); return int(mn[0]), int(mn[1])
        return self._min_of(key, g)
    def _too_small(self, key, z, g=None, slot=None, say=True):
        if z is None or z.px is None: return False
        b = slot if slot is not None else self._body(z); mn = self._min_at(key, b[2], b[3], g)
        if mn is None or (b[2] >= mn[0] and b[3] >= mn[1]): return False
        if say: Kit.say("%s needs a zone at least %d x %d." % (self.title_of(key), mn[0], mn[1]), Kit.HUE_BAD)
        return True
    def title_of(self, key):
        t = self.titles.get(key)
        if t is not None: return t
        mk, part = self.owner_of(key); s = dict.get(HOST.by_key, mk) if mk else None
        if s is None: s = HOST.page_slot(key); return s.title if s is not None else key
        p = s.part(part) if part else None; return p[1] if p else s.title
    def drop_empty_bags(self, zs, W, H, ids):
        gone = [z for z in zs.zones if z.id in ids and z.id.endswith(" bags") and z.kind == "w"
                and not self.assign.get(z.id)]
        if not gone or zs.generated or zs.name == LAYOUT_DEFAULT: return False
        for n in [n for n in self.layout_names() if n != self.layout_name]:
            f, a = self.parse_windows(Kit.get_var(LAYOUT_NAMED % n, ""))
            if f == zs.name: gone = [z for z in gone if not a.get(z.id)]
        if not gone: return False
        zs.zones = [z for z in zs.zones if z not in gone]
        for z in gone: zs.needs.pop(z.id, None)
        self.save_frames(zs, zs.name, W, H)
        Kit.say('empty zone%s %s removed; frame layout "%s" saved.' % ("" if len(gone) == 1 else "s", ", ".join(
            '"%s"' % z.id for z in gone), zs.name), Kit.HUE_INFO)
        return True
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
        if not self.loaded or not self.enabled: return None
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
                rank = (z.id == "%s bags" % tz.id, ov)
                if best is None or rank > best[0]: best = (rank, z)
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
            zs = ZoneSet.default(W, H, self.occupied(), False)
            zs.name, zs.generated = LAYOUT_MINE, False; name = LAYOUT_MINE; tz = zs.by_id(tz.id)
            if tz is None or tz.px is None: return None
        else: zs = zs.copy(); tz = zs.by_id(tz.id)
        old = zs.by_id("%s bags" % tz.id)
        if old is not None and old.kind == "w" and not [k for k in self.assign.get(old.id, []) if k != bottom_key]:
            zs.zones.remove(old)
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
        else: self.dirty = True
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
        live = set(zid for zid, keys in self.assign.items() if any(self.gump_of(key) is not None for key in keys))
        return live | self.plan_occ if self.plan_occ is not None else live
    def frames_in_use(self, W, H):
        if self.frames is not None and not self.dirty and self.screen == (W, H): return self.frames
        zs = self.load_frames(self.frames_name, W, H) if self.frames_name != LAYOUT_DEFAULT else None
        if zs is not None:
            self._repair_stretched(zs, W, H)
            if not self.bags_swept: self.bags_swept = True; self.drop_empty_bags(zs, W, H, zs.ids())
        elif self.frames_name != LAYOUT_DEFAULT:
            self.frames_name = LAYOUT_DEFAULT; Kit.put_var(FRAMES_ACTIVE, LAYOUT_DEFAULT)
        if zs is None: zs = ZoneSet.default(W, H, self.occupied(), self.game_grows)
        old = self.frames
        if old is not None and old.needs and old.name == zs.name:
            zs.needs = dict((k, v) for k, v in old.needs.items() if zs.by_id(k) is not None
                            and any(key in self.wins for key in self.assign.get(k, ())))
            if zs.needs: zs.reflow(W, H, HOST.grid_size())
        self._overlap_shape(zs); self.frames, self.screen, self.dirty = zs, (W, H), False; return zs
    @staticmethod
    def _overlap_shape(zs):
        for k in zs.zones:
            if k.kind == "k" and k.overlap: k.arch = False
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
        t, vp = self._viewport(); fs = self._vp_fields
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
            if not self.gv_small_told:
                self.gv_small_told = True
                Kit.say("the game view would be %d x %d, under the client's smallest (%d x %d); left as you "
                           "set it." % (want[2], want[3], self.GV_MIN[0], self.GV_MIN[1]), Kit.HUE_INFO)
            want = None
        if not self.gv_checked:
            self.gv_checked = True
            if want is None and Kit.get_var(self.GV_VAR, ""): self.game_view_restore(); return
        if want == self.gv_applied:
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
            Kit.say('frame layout "%s" in use%s.' % (name, ("; %s had no zone and %s free" % (
                Kit.count(free, "window"), "is" if free == 1 else "are")) if free else ""), Kit.HUE_GOOD)
        self.page_refresh = True; self.fresh = True
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
        if self.situ["on"] and not self.situ_busy:
            self.situ["base"] = name; self.situ_now = self.situ_last; self.situ_pend = self.situ_back = None
            self.situ_save()
        frames, assign = (self.parse_windows(self.window_layout_text(name)) if name else (self.frames_name, {}))
        if name and not self.situ_busy: self.unfree(None)
        elif not self.situ_busy: self.free_by_you(list(self.wins) + [k for ks in self.assign.values() for k in ks])
        self.layout_name = name; Kit.put_var(LAYOUT_ACTIVE, name); self.assign = assign; self.save_assign()
        self.free_scrolled(); self.placed = {}; keep = name in (LAYOUT_DEFAULT, LAYOUT_MIRRORED)
        if keep and frames != self.frames_name:
            W, H = Kit.screen(); zs = self.frames_in_use(W, H) if W > 0 and H > 0 else self.frames
            keep = zs is None or any(zs.by_id(zid) is not None for zid in assign)
        if name and not keep and frames != self.frames_name: self.use_frames(frames, tell=False)
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
    CODE_HEAD, CODE_TAG, CODE_VER, CODE_FILE, CODE_MAX = "VA-", "VAL1", 1, "layout-code.txt", 8000; CODE_RAW = 65536
    CODE_BAD = "Interface: that isn't a Virtue Assistant layout code."
    def _shipped(self, key):
        if key == "worldmap": return True
        s = dict.get(HOST.by_key, self.owner_of(key)[0] or ""); return s is not None and s.shipped
    def share_code(self):
        import zlib
        W, H = Kit.screen(); zs = self.frames_in_use(W, H) if W > 0 and H > 0 else self.frames
        if zs is None or not zs.zones: return ""
        if self.frames_name != LAYOUT_DEFAULT and W > 0 and H > 0:
            var = FRAMES_NAMED % self.frames_name; text = Kit.get_var(var + "@" + ratio_class(W, H), "")
            raw = ZoneSet.parse(self.frames_name, text or Kit.get_var(var, ""))
            if raw is not None and raw.zones: zs = raw
        keep = {}
        for zid, keys in self.assign.items():
            ks = [k for k in keys if self._shipped(k)]
            if ks: keep[zid] = ks
        text = "\n".join((self.CODE_TAG, self.frames_name, zs.save_text(), self.windows_text(self.frames_name, keep)))
        data = [self.CODE_VER] + list(bytearray(zlib.compress(text.encode("utf-8"), 9)))
        c = Kit.checksum(data); data += [(c >> 8) & 255, c & 255]; n = len(data)
        return self.CODE_HEAD + Kit.b64(data + [0] * (-n % 3))[:(n * 4 + 2) // 3]
    def _code_read(self, t):
        import zlib
        try:
            if len(t) % 4 == 1 or len(t) > self.CODE_MAX: return None
            if any(ch not in Kit.B64_REV for ch in t): return None
            full = Kit.unb64(t + "A" * (-len(t) % 4)); n = len(t) * 3 // 4; data = full[:n]
            if n < 4 or any(full[n:]) or data[0] != self.CODE_VER: return None
            if Kit.checksum(data[:-2]) != (data[-2] << 8 | data[-1]): return None
            d = zlib.decompressobj(); raw = d.decompress(bytes(bytearray(data[1:-2])), self.CODE_RAW)
            if d.unconsumed_tail or len(raw) >= self.CODE_RAW: return None
            lines = raw.decode("utf-8").split("\n")
            if len(lines) != 4 or lines[0] != self.CODE_TAG: return None
            zs = ZoneSet.parse(lines[1], lines[2])
            if zs is None or not zs.zones or zs.skipped or zs.dups: return None
            return lines[1], zs, self.parse_windows(lines[3])[1]
        except Exception: return None
    def load_code(self, text):
        t = re.sub(r"\s+", "", str(text or ""))
        got = self._code_read(t[len(self.CODE_HEAD):]) if t.startswith(self.CODE_HEAD) else None
        if got is None: API.SysMsg(self.CODE_BAD, Kit.HUE_BAD); return False
        name, zs, assign = got; name = name[:-9] if name.endswith(" (shared)") else name; ren = {}
        for z in zs.zones:
            zid = self.clean_name(z.id, "")
            if zid and zid != "frames" and zid not in ren.values(): ren[z.id] = zid
        n = 1
        for z in zs.zones:
            while z.id not in ren and "Zone %d" % n in ren.values(): n += 1
            ren.setdefault(z.id, "Zone %d" % n)
        assign = dict((ren[k], v) for k, v in assign.items() if k in ren)
        for z in zs.zones: z.id = ren[z.id]
        nm = self.clean_name(name, "Shared")[:15].strip() + " (shared)"; W, H = Kit.screen()
        if W <= 0 or H <= 0: W, H = zs.screen
        if (W, H) != zs.screen: zs.reflow(W, H, HOST.grid_size())
        self.save_frames(zs, nm, W, H)
        Kit.put_var(LAYOUT_NAMED % nm, self.windows_text(nm, assign)); names = self.layout_names()
        if nm not in names: names.append(nm); Kit.put_var(LAYOUT_LIST, ",".join(names))
        self.use_windows(nm); return True
    SITU_VAR = "VirtueAssistant_layout_situations"; SITU_KINDS = ("war", "bank", "dungeon", "town")
    SITU_SAY = {"war": "war mode", "bank": "bank", "dungeon": "dungeon", "town": "town"}
    SITU_EVERY, SITU_HOLD, SITU_WAR_HOLD, SITU_BANK_FOR, SITU_BANK_NEAR = 1.0, 2.0, 0.5, 300.0, 8
    def situ_load(self):
        s = {"on": False, "base": ""}
        for k in self.SITU_KINDS: s[k] = ""
        for k, v in Kit.codec_load(Kit.get_var(self.SITU_VAR, "")).items():
            if k == "on": s["on"] = v == "1"
            elif k in s: s[k] = self.clean_name(v, "")
        self.situ = s; self.situ_now = self.situ_pend = self.situ_last = self.situ_back = None; self.situ_at = 0.0
    def situ_park(self):
        b, self.situ_back = self.situ_back, None
        if b is None or not self.situ_now: return
        Kit.put_var(LAYOUT_ACTIVE, b[0]); Kit.put_var(FRAMES_ACTIVE, b[1])
        Kit.put_var(LAYOUT_VAR, self.windows_text(b[1], b[2])); self.homes = dict(b[3]); self._homes_put()
    def situ_save(self):
        s = self.situ
        Kit.put_var(self.SITU_VAR, ";".join(["on=%d" % (1 if s["on"] else 0)] + [
            "%s=%s" % (k, s.get(k, "")) for k in self.SITU_KINDS + ("base",)]))
    def situ_set(self, on):
        on = bool(on)
        if on == self.situ["on"]: return
        if not on and self.situ_now: self._situ_go("", self.situ["base"], self.situ_now)
        self.situ["on"] = on; self.situ_now = self.situ_pend = self.situ_last = self.situ_back = None
        self.situ_at = 0.0
        if on: self.situ["base"] = self.layout_name
        self.situ_save()
    def situ_pick(self, kind, name):
        if kind not in self.SITU_KINDS: return
        self.situ[kind] = self.clean_name(name, ""); self.situ_now = self.situ_pend = None; self.situ_save()
    def _bank_note(self, now, w):
        try:
            b = int(API.Bank or 0); it = API.FindItem(b) if b else None; up = it is not None and bool(it.Opened)
        except Exception: up = False
        if up and w is not None: self.situ_bank = (now, w[0], w[1], w[2])
    def situ_want(self, now):
        s = self.situ; w = None
        if s["bank"]: w = Guard._where(); self._bank_note(now, w)
        for kind in self.SITU_KINDS:
            if not s[kind]: continue
            if kind == "war": me = HOST.me(); hit = me is not None and bool(me.InWarMode)
            elif kind == "bank":
                b = self.situ_bank
                hit = (w is not None and now - b[0] <= self.SITU_BANK_FOR and b[3] == w[2]
                       and max(abs(b[1] - w[0]), abs(b[2] - w[1])) <= self.SITU_BANK_NEAR)
            elif kind == "dungeon":
                if w is None: w = Guard._where()
                hit = False
                for a in DUNGEON_AREAS:
                    if w is not None and a[0] == w[2] and a[1] <= w[0] <= a[3] and a[2] <= w[1] <= a[4]: hit = True
            else: hit = GUARD.guarded() is True
            if hit: return kind, s[kind]
        return "", s["base"]
    def situ_tick(self, now, busy=False):
        if not self.situ["on"] or not self.enabled or now < self.situ_at: return
        self.situ_at = now + self.SITU_EVERY
        if self.situ_now == "" and self.layout_name != self.situ["base"]:
            self.situ["base"] = self.layout_name; self.situ_back = None; self.situ_save()
        try: kind, name = self.situ_want(now)
        except Exception: return
        self.situ_last = kind; was = self.situ_now
        if kind == was: self.situ_pend = None; return
        if was is None and name == self.layout_name: self.situ_now, self.situ_pend = kind, None; return
        hold = self.SITU_WAR_HOLD if kind == "war" else self.SITU_HOLD; p = self.situ_pend
        if p is None or p[0] != kind:
            self.situ_pend = (kind, now); self.situ_at = now + min(hold, self.SITU_EVERY); return
        if now - p[1] < hold: self.situ_at = min(self.situ_at, p[1] + hold); return
        if busy or self.arrange or SNAP.pressed(): return
        self.situ_now, self.situ_pend = kind, None; self._situ_go(kind, name, was)
    def _situ_go(self, kind, name, was):
        if name == self.layout_name and (kind or self.situ_back is None): return
        if name and name not in (LAYOUT_DEFAULT, LAYOUT_MIRRORED) and name not in self.layout_names(): return
        if kind and was in ("", None) and self.situ_back is None:
            self.situ_back = (self.layout_name, self.frames_name, dict((z, list(v)) for z, v in self.assign.items()),
                              dict(self._homes()))
        back = self.situ_back if not kind else None; self.situ_busy = True
        try: self.use_windows(name, tell=False)
        finally: self.situ_busy = False
        if back is not None:
            self.situ_back = None
            if back[0] == name:
                if back[1] != self.frames_name: self.use_frames(back[1], tell=False)
                self.homes = dict(back[3]); self._homes_put(); self.assign = back[2]; self.save_assign()
                self.placed = {}; self.dirty = True
        t = name or "(none)"
        API.SysMsg("Interface: %s layout (%s)." % (t, self.SITU_SAY[kind]) if kind else "Interface: back to %s." % t,
                   Kit.HUE_INFO)
    def free_scrolled(self):
        for key in [k for k in self.fitted if not self.holds(k)]: self._unfit(key)
        for key, rect in list(self.placed.items()):
            if not self.holds(key):
                g = self.gump_of(key); info = Kit.scroll_info(g) if g is not None else None
                if info is not None:
                    with Kit.quiet:
                        Kit.place(g, int(g.GetX()), int(g.GetY()), info["w"], info["h"], info["head"])
                        Kit.moved_by_code(g)
                self.placed.pop(key, None)
    def keep(self, W, H, only=None):
        if not self.loaded or W <= 0 or H <= 0: return
        if not self.enabled: self.fresh_adds.clear(); self._off(); return
        occ = self.occupied()
        if occ != self.occ:
            self.occ = occ
            if self.frames_name == LAYOUT_DEFAULT: self.dirty = True
        zs = self.frames_in_use(W, H); Kit.flush()
        self.fresh = False; self.fresh_adds.clear(); Fill.prune()
        if self.behind: self._tabs_prune(zs)
        for key in [k for k in self.fitted if not self.holds(k)]: self._unfit(key)
        now = time.time()
        jobs = [(self._hold_journal, (zs, H)), (self._client_drops, ()), (self._arrange_tick, (zs, W, H))]
        if now >= self.repair_at and not SNAP.drag: self.repair_at = now + 2.0; jobs.append((self._repair, (zs,)))
        for fn, args in jobs:
            try: fn(*args)
            except Exception: pass
        drag = SNAP.drag; told = []; seen = set(); jobs = []
        if only is None: self.gump_key = {}
        for z in (zs.zones if self.assign else ()):
            keys = self.assign.get(z.id)
            if not keys or z.kind != "w" or z.px is None: continue
            if only is not None and not any(self.gump_of(k) in only for k in keys): continue
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
            if items and z.stack == "t":
                shown = self.tab_shown(z)
                for it in items:
                    if it[0] != shown: self.behind[it[0]] = z.id
            if items: jobs.extend((it, slot, z) for it, slot in zip(items, self._slots(z, items)))
        if self.behind or Kit._behind: Kit._behind = set(g for g in map(self.gump_of, self.behind) if g is not None)
        thin, full = (Seam.pad(),) * 4, (Kit.MARGIN,) * 4; small = set()
        for it, slot, z in jobs:
            if it[1] in drag: continue
            if self._small(it[0], z, it[1], slot):
                small.add(it[1]); self.placed[it[0]] = slot; x, y = Kit.clamp(slot[0], slot[1], it[2][2], it[2][3])
                if it[0] in self.fitted: self._unfit(it[0])
                if self._move_all(it[1], it[4], it[2], x, y): told.append(it[1])
                continue
            try:
                pads = (full if z.solo else thin) if self.seamless and it[0] not in self.behind else None
                if self._fit_slot(it, slot, z, pads): told.append(it[1])
            except Exception: self.placed[it[0]] = slot
        if only is None:
            self._release(seen)
            for g in [g for g in Seam.recs if g not in seen]: Seam.undo(g)
        bare = set()
        if self.seamless and self.enabled:
            for it, slot, z in [j for j in jobs if j[0][1] not in small and j[0][0] not in self.behind]:
                for g in [it[1]] + list(it[4]):
                    try:
                        if not isinstance(g, ClientWin) and Seam.strip(g, g is it[1] and it[5].get("untitled")):
                            bare.add(g)
                    except Exception: pass
        for g in ([g for g in Seam.bare if g not in bare] if only is None else ()): Seam.unstrip(g)
        if only is None and (self.strips or self.behind or any(z.stack == "t" for z in zs.zones)):
            try: self._strips_keep(zs)
            except Exception: pass
        try: self._game_view(zs)
        except Exception: pass
        if self.assign and self.need_due: self.need_due = False; zs.reflow(W, H, HOST.grid_size()); self.fresh = True
        if self.plan_occ is not None and (not HOST.booting() or self._plan_sig(zs) != self.plan_sig): self.plan_drop()
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
        if z.stack == "t": return [self._body(z)] * len(items)
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
    TABS_VAR = "VirtueAssistant_layout_tabs"; TABS_CAP = 64
    @staticmethod
    def _body(z):
        zx, zy, zw, zh = z.px; return (zx, zy + TAB_H, zw, max(1, zh - TAB_H)) if z.stack == "t" else (zx, zy, zw, zh)
    @staticmethod
    def _tabs_parse(text):
        out = {}
        for part in str(text or "").split(";"):
            if "=" not in part: continue
            k, v = part.split("=", 1)
            if k.strip() and v.strip(): out[k.strip()] = v.strip()
        return out
    def _tabs_save(self): Kit.put_var(self.TABS_VAR, ";".join("%s=%s" % kv for kv in sorted(self.tabs.items())))
    def tab_shown(self, z):
        keys = self.assign.get(z.id, [])
        if not keys: return None
        k = self.tabs.get(z.id)
        if k in keys and self._tab_ok(k): return k
        return next((k for k in keys if self._tab_ok(k)), keys[0])
    def _tab_ok(self, key):
        g = self.gump_of(key)
        if g is None or not Snap.visible(g): return False
        riding = (self.hooks.get(key) or {}).get("riding"); return riding is None or not safe(riding, False)
    def tab_pick(self, zid, key):
        zid, key = str(zid), str(key)
        if key not in self.assign.get(zid, ()): return False
        if self.tabs.get(zid) != key:
            self.tabs[zid] = key
            if len(self.tabs) > self.TABS_CAP: self.tabs = dict(kv for kv in self.tabs.items() if kv[0] in self.assign)
            self._tabs_save()
        for k in self.assign.get(zid, ()): self.seam_skip.pop(k, None); self.seam_wait.pop(k, None)
        self.fresh = True; HOST.poke(); return True
    def spot(self, key):
        slot = self.placed.get(key)
        if slot is None: return self.plan_at(key)
        if key not in self.behind: return slot
        return (TAB_X,) + tuple(slot[1:])
    def _unhide(self, key):
        self.behind.pop(key, None); g = self.gump_of(key)
        if g is None: return
        Kit._behind.discard(g); r = Snap.rect(g)
        if r is None or r[0] > TAB_X // 2: return
        slot = self.placed.get(key); x = slot[0] if slot is not None else Kit.clamp(0, r[1], r[2], r[3])[0]
        self._move_all(g, SNAP.followers(g), r, x, r[1])
    def _tabs_prune(self, zs):
        for key, zid in list(self.behind.items()):
            z = zs.by_id(zid) if zs is not None else None
            if (z is None or z.stack != "t" or z.kind != "w" or z.px is None or not self.holds(key)
                    or self.zone_of(key) != zid or self.tab_shown(z) == key):
                self._unhide(key)
    def _tabs_off(self):
        for key in list(self.behind): self._unhide(key)
        Kit._behind = set()
        for s in list(self.strips.values()): Kit.dispose(s["g"])
        self.strips = {}
    def _strips_keep(self, zs):
        want = {}
        for z in (zs.zones if self.assign else ()):
            if z.stack != "t" or z.kind != "w" or z.px is None: continue
            keys = tuple(k for k in self.assign.get(z.id, []) if self.gump_of(k) is not None)
            if keys:
                want[z.id] = (tuple(z.px), keys, self.tab_shown(z), tuple(self.title_of(k) for k in keys), Kit.look(),
                              Kit.SECTION_ALPHA)
        for zid in [k for k in self.strips if k not in want]: Kit.dispose(self.strips.pop(zid)["g"])
        for zid, sig in want.items():
            s = self.strips.get(zid)
            if s is not None and s["sig"] == sig and Kit.is_open(s["g"]): continue
            old = s["g"] if s is not None else None
            self.strips[zid] = {"g": self._strip(zid, sig), "sig": sig}; Kit.dispose(old)
    def _strip(self, zid, sig):
        (x, y, w, h), keys, shown, titles = sig[0], sig[1], sig[2], sig[3]
        g = G.CreateGump(True, False); Kit.add_section(g, 0, 0, w, TAB_H)
        share = max(1, w // len(keys)); bw, bh = Kit.pic_size(Kit.ART_PAGE[0]); bw, bh = bw or 30, bh or 22
        for i, (k, t) in enumerate(zip(keys, titles)):
            bx = i * share + 4; fn = self._tab_click(zid, k); tip = "Show %s in this zone" % t
            b = G.CreateGumpButton("", Kit.HUE_TEXT, Kit.ART_PAGE[0], Kit.ART_PAGE[1], Kit.ART_PAGE[2])
            b.SetPos(bx, max(0, (TAB_H - bh) // 2)); g.Add(b); Kit.on_click(b, fn); Kit.with_tip(b, tip)
            lbl = Kit.add_label(g, Kit.fit(t, max(10, share - bw - 15)), bx + bw + 5, max(0, (TAB_H - 16) // 2),
                                Kit.HUE_TITLE if k == shown else Kit.HUE_TEXT)
            lbl.SetAcceptMouseInput(True); Kit.on_click(lbl, fn); Kit.with_tip(lbl, tip)
        g.SetRect(x, y, w, TAB_H); g.CanMove = False; Kit.add_front(g); SNAP.skip_gump(g); return g
    def _tab_click(self, zid, key):
        def hit(): self.tab_pick(zid, key)
        return hit
    def retry_due(self, now):
        if not self.seam_wait or now < self.retry_at: return False
        self.retry_at = now + SEAM_RETRY
        for key, was in list(self.seam_wait.items()):
            g = self.gump_of(key)
            if g is None or not Snap.visible(g) or not self.holds(key) or now - was[1] > 2 * SEAM_WAIT:
                self.seam_wait.pop(key, None)
            else: self.fresh_adds.add(g)
        return bool(self.fresh_adds)
    PLAN_PART = {"ultima": "tracker"}
    def plan(self):
        self.plan_drop(); W, H = Kit.screen(); o = dict.get(HOST.by_key, LAYOUT_OWNER)
        if not self.loaded or not self.assign or W <= 0 or H <= 0 or o is None or not o.enabled: return False
        on = {}
        for zid, keys in self.assign.items():
            for key in keys:
                mk, part = self.owner_of(key); s = dict.get(HOST.by_key, mk) if mk else None
                if part is None and key not in self.owner: part = self.PLAN_PART.get(mk)
                if self.gump_of(key) is not None or (s is not None and s.enabled
                                                     and (part is None or s.parts_on.get(part))):
                    on.setdefault(zid, []).append(key)
        self.plan_occ = set(on); self.occ = self.occupied()
        if self.frames_name == LAYOUT_DEFAULT: self.dirty = True
        zs = self.frames_in_use(W, H); self.fresh = False; pad = (Seam.pad(),) * 4
        for z in zs.zones:
            keys = on.get(z.id)
            if not keys or z.kind != "w" or z.px is None: continue
            if z.stack == "t":
                k = self.tabs.get(z.id); keys = [k if k in keys else keys[0]]
            elif len(keys) > 1: continue
            pads = ((Kit.MARGIN,) * 4 if z.solo else pad) if self.seamless else None
            self.planned[keys[0]] = (tuple(self._body(z)), z, pads)
        self.plan_sig = self._plan_sig(zs); return bool(self.planned)
    def _plan_sig(self, zs):
        ids = set(p[1].id for p in self.planned.values()); px = [(z.id, z.px) for z in zs.zones if z.id in ids]
        return zs.screen, self.frames_name, self.windows_text(), self.seamless, sorted(px)
    def plan_drop(self): self.planned, self.plan_occ, self.plan_sig = {}, None, None
    def plan_prune(self):
        if not self.plan_occ: return False
        live = set(z for z in self.plan_occ if any(self.gump_of(k) is not None for k in self.assign.get(z, ())))
        if live == self.plan_occ: return False
        self.plan_occ = live; return True
    def plan_at(self, key):
        p = self.planned.get(key) if self.planned else None
        if p is not None and not HOST.booting(): self.plan_drop(); return None
        if p is None or not self.holds(key): return None
        slot, z, pads = p
        if pads is not None and Client.on_client_thread() and not (self.hooks.get(key) or {}).get("untitled"):
            grown = Seam.grow(slot, Seam.clip(slot, pads))
            if grown[3] <= Kit.screen()[1]: return grown
        return slot
    def fit_added(self, key):
        key = str(key); g = self.gump_of(key) if key in self.planned else None
        if g is not None and Snap.visible(g): self.fit_now(key, g)
    def fit_now(self, key, g):
        was = self.slot_was.get(key) or (self.planned.get(key) if self.planned else None)
        if key in self.behind: Kit._behind.add(g)
        if (was is None or not (self.seamless and self.enabled) or key not in self.wins
                or ((self.dirty or self.fresh) and key not in self.planned) or g in SNAP.drag
                or g in SNAP.attached or not Client.on_client_thread()): return
        Kit.flush(); hooks = self.hooks.get(key) or {}; r = Snap.rect(g)
        if r is None or hooks.get("riding") is not None or SNAP.followers(g): return
        try: mini = hooks.get("state") is not None and hooks["state"]() == "minimized"
        except Exception: mini = False
        slot, z, pads = was; self.gump_key[g] = key
        if z is not None and self._small(key, z, g, slot): return
        try:
            self._fit_slot((key, g, r, r, [], hooks, mini, self._base(key, g, r, mini)), slot, z, pads)
            if not isinstance(g, ClientWin) and key not in self.behind: Seam.strip(g, hooks.get("untitled"))
        except Exception: pass
    def _fit_slot(self, it, slot, z=None, pads=None):
        key, g, r, ext, fol, hooks, mini, base = it; ins = int(hooks.get("inset") or 0)
        if g in Seam.recs and not Client.on_client_thread(): return False
        self.slot_was[key] = (slot, z, pads)
        slot = (slot[0] - ins, slot[1] - ins, slot[2] + 2 * ins, slot[3] + 2 * ins); self.placed[key] = slot
        if pads is not None: pads = Seam.clip(slot, pads)
        grown = Seam.grow(slot, pads) if pads is not None else None
        if (grown is not None and self.seam_skip.get(key) != slot and Seam.can(g, hooks, mini)
                and grown[3] <= Kit.screen()[1]):
            self.placed[key] = grown
            if Seam.holds(g, slot, pads, grown, r): return False
            Seam.undo(g); Seam.unstrip(g); self._fit_at(it, grown, z, ins); r2 = Snap.rect(g)
            rec = Fill.recs.get(g); S = self.MISFIT_SLACK
            if r2 is not None and (rec is None or rec.get("k", 1.0) >= 0.995):
                if r2[:2] != grown[:2]: self._move_all(g, fol, r2, grown[0], grown[1])
                if fol or (abs(r2[2] - grown[2]) <= S and abs(r2[3] - grown[3]) <= S):
                    self.seam_wait.pop(key, None); return Seam.trim(g, slot, pads)
                was = self.seam_wait.get(key); now = time.time()
                if was is None or was[0] != slot: was = self.seam_wait[key] = (slot, now)
                if now - was[1] < SEAM_WAIT: return False
            self.seam_skip[key] = slot; self.placed[key] = slot
        self.seam_wait.pop(key, None)
        if g in Seam.recs: Seam.undo(g)
        return self._fit_at(it, slot, z, ins)
    def _fit_at(self, it, slot, z, ins):
        key, g, r, ext, fol, hooks, mini, base = it
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
            if (r[0], r[1]) == (TAB_X if g in Kit._behind else sx, sy) and r[3] == min(fh, sh): return False
            Kit._place_raw(g, sx, sy, fw, fh, None, sh if fh > sh else None); done = True
        if done: Kit.moved_by_code(g)
        return bool(done)
    @staticmethod
    def _move_all(g, fol, r, x, y):
        if g in Kit._behind: x = TAB_X
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
        if (z is not None and z.px is not None and (key, z.id, z.px) != self.small_said):
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
        for d in (self.base, self.misfit, self.fallback, self.client_settle, self.slot_was): d.pop(key, None)
        if rec is None: return
        hooks = self.hooks.get(key) or {}
        if rec.get("kind") == "fit":
            fn = hooks.get("fit")
            if fn is not None and rec.get("told") is not None:
                try: fn(None, None, None)
                except Exception: pass
        g = self.gump_of(key)
        if g is not None and g in Seam.recs: Seam.undo(g)
        if g is not None: Fill.unfit(g)
    def _small(self, key, z, g, slot=None):
        sig = (z.id, tuple(z.px), z.stack, tuple(slot) if slot is not None else None); was = self.min_seen.get(key)
        if was is None or was[0] != sig:
            told = was is not None and was[1] and was[0][0] == z.id
            was = self.min_seen[key] = (sig, self._too_small(key, z, g, slot, not told))
        return was[1]
    def report_fit(self):
        W, H = Kit.screen(); zs = self.frames_in_use(W, H) if W > 0 and H > 0 else None; n = bad = hid = 0; ridden = []
        for z in (zs.zones if zs is not None else []):
            keys = self.assign.get(z.id, [])
            rides = [safe((self.hooks.get(k) or {}).get("riding") or (lambda: False), False) for k in keys]
            if keys and all(rides) and z.px is not None: ridden.append(z.px)
        for z in (zs.zones if zs is not None else []):
            keys = self.assign.get(z.id, []); shut = [k for k in keys if self.gump_of(k) is None]
            if z.kind == "w" and not keys: Kit.say('zone "%s": empty.' % z.id, Kit.HUE_INFO)
            if shut:
                names = ", ".join(self.title_of(k) for k in shut)
                Kit.say('zone "%s": %s.' % (z.id, ("empty (%s not open)" if len(shut) == len(keys) else "%s not open")
                                            % names), Kit.HUE_BAD)
            for key in keys:
                g = self.gump_of(key); slot = self.placed.get(key)
                if g is None or slot is None: continue
                if key in self.behind:
                    n += 1; hid += 1; Kit.say('%s: behind a tab in "%s".' % (self.title_of(key), z.id), Kit.HUE_GOOD)
                    continue
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
        if self.seamless:
            Kit.say("One panel: on; %s without a title row, %s with the title hidden in place, %s left as is." % (
                Kit.count(len(Seam.recs), "window"),
                Kit.count(sum(1 for r in Seam.bare.values() if r["title"]), "window"),
                Kit.count(max(0, n - hid - len(Seam.recs) - sum(1 for r in Seam.bare.values() if r["title"])),
                          "window")), Kit.HUE_INFO)
        if not n: Kit.say("no window sits in a zone.", Kit.HUE_INFO)
        else:
            Kit.say("%d of %s; screen %d x %d (UI scale %.2f)." % (
                n - bad, "%d windows fill their zone" % n if n > 1 else "1 window fills its zone", W, H,
                Kit.render_scale()), Kit.HUE_INFO)
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
            self._homes_put()
    def _homes_put(self): Kit.put_var(self.HOMES_VAR, ";".join("%s=%s" % kv for kv in sorted(self._homes().items())))
    def _repair(self, zs):
        if not self.assign: return
        homes = self._homes()
        if not homes: self._note_homes()
        mz = self._map_zone(); squat = [k for k in (self.assign.get(mz, []) if mz else []) if k != "worldmap"]
        freed = self._freed(); todo = list(squat); listed = None
        for key in ("ultima.friend", "ultima.neutral", "ultima.foe", "ultima.combat", "meters", "worldmap"):
            if (key not in self.wins or key in freed or key in squat or self.holds(key)): continue
            if listed is None:
                listed = set()
                if self.layout_name:
                    for ks in self.parse_windows(self.window_layout_text(self.layout_name))[1].values():
                        listed.update(ks)
            mod = key.split(".")[0]; kin = any(k.split(".")[0] == mod for ks in self.assign.values() for k in ks)
            if key in homes or key in listed or (kin and key != "worldmap") or (self.migrating and key != "worldmap"):
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
        self.placed.pop(key, None); self.min_seen.pop(key, None); rec = self.fitted.get(key)
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
                Kit.say("%s stays in its zone; drop it on another zone to move it (Settings > Interface frees "
                           "windows)." % self.title_of(key), Kit.HUE_INFO)
            return
        if old == hit.id and len(self.assign.get(old, [])) <= 1: self._back(); return
        if old == hit.id and hit.stack == "t": self.tab_pick(hit.id, key); self._back(); return
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
            if len(others) == 1 and self.gump_of(others[0]) is not None and hit.stack != "t":
                swap = others[0]
                if self._too_small(swap, self.frames.by_id(old)): self._back(); return
            for k in list(self.assign.get(old, [])) + list(self.assign.get(hit.id, [])): self._refit(k)
            at = self.assign[old].index(key) if key in self.assign[old] else 0
            self.assign[old] = [k for k in self.assign[old] if k != key]
            if swap is not None:
                self.assign[old].insert(min(at, len(self.assign[old])), swap)
                self.assign[hit.id] = [k for k in self.assign[hit.id] if k != swap]; self.placed.pop(swap, None)
            if not self.assign[old]: del self.assign[old]
        keys = self.assign.setdefault(hit.id, []); pos = len(keys)
        if hit.stack == "t": self.tabs[hit.id] = key; self._tabs_save()
        for i, k in enumerate(keys if hit.stack != "t" else ()):
            p = slots_was.get(k) or self.placed.get(k)
            if p is None: continue
            if hit.stack in ("d", "u"): mid = p[1] + p[3] // 2; before = cy < mid if hit.stack == "d" else cy > mid
            else: mid = p[0] + p[2] // 2; before = cx < mid if hit.stack == "r" else cx > mid
            if before: pos = i; break
        keys.insert(pos, key); self.unfree(key); self.save_assign(); self.dirty = True
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
        b = self._body(z); mn = self._min_at(key, b[2], b[3])
        if mn and (b[2] < mn[0] or b[3] < mn[1]):
            return ("!%s needs %d x %d at least; this zone is %d x %d." % (t, mn[0], mn[1], b[2], b[3]))
        keys = ([k for k in (keys if keys is not None else self.assign.get(z.id, [])) if k != key] + [key]); slot = None
        for k, sl in self.slots_for(z, keys):
            if k == key: slot = sl
        if slot is None: slot = z.px
        w, h = max(1, slot[2]), max(1, slot[3]); base = self._size_of(key); shown = ""
        if base and base[0] > 0 and base[1] > 0:
            sc = min(1.0, float(w) / base[0], float(h) / base[1])
            if sc < 0.995: shown = " (shown at %d%%)" % int(round(sc * 100))
        return "%s: %d x %d here%s." % (t, w, h, shown)
    def status_text(self):
        W, H = Kit.screen(); step = HOST.grid_size()
        if W <= 0 or H <= 0: return "Screen: not known yet"
        return "Screen: %d x %d, %s; grid %d px, %d x %d squares" % (
            W, H, ratio_class(W, H), step, (W + step - 1) // step, (H + step - 1) // step)


class Seam(object):
    recs = {}; bare = {}; titled_n = {}; edge = [None]; catchers = {}; seen = [None, 0.0]
    @staticmethod
    def pad():
        if Seam.edge[0] is None:
            s = [Kit.pic_size(Kit.WINDOW_BG + i) for i in (1, 3, 5, 7)]
            Seam.edge[0] = min(Kit.MARGIN, max([SEAM_PAD, s[0][1], s[1][0], s[2][0], s[3][1]]) + 1)
        return Seam.edge[0]
    @staticmethod
    def title_of(raw, w):
        M = Kit.MARGIN; rects = [(c, Kit._raw_rect(c)) for c in Kit._children(raw)]
        if not any(r is not None and abs(r[0] - M) <= 2 and abs(r[1] - M) <= 2 and abs(r[3] - 30) <= 1
                   and r[2] >= w - 2 * M - 6 for c, r in rects): return []
        return [c for c, r in rects if r is not None and M - 4 <= r[1] < M + 34 and r[1] + r[3] <= M + 36]
    @staticmethod
    def titled(g):
        if g in Seam.recs: return True
        raw = Kit._raw_gump(g); r = Kit.rect(g)
        if raw is None or r is None: return False
        n = int(raw.Children.Count); had = Seam.titled_n.get(g)
        if had is not None and had[0] == n: return had[1]
        Kit._prune(Seam.titled_n, 32); on = bool(Seam.title_of(raw, r[2])); Seam.titled_n[g] = (n, on); return on
    @staticmethod
    def strip(g, untitled=False):
        parts = Kit._frame_parts.get(g); raw = Kit._raw_gump(g)
        if not parts or raw is None: return False
        rec = Seam.bare.get(g); n = int(raw.Children.Count)
        if rec is not None and rec["parts"] is parts:
            if rec["n"] != n:
                cur = Kit._children(raw); have = set(cur); M = Kit.MARGIN
                for p in parts: Kit.set(p, "IsVisible", False)
                rec["title"] = [t for t in rec["title"] if t[0] in have]
                for c in [c for c in cur if c not in rec["kids"]] if rec["band"] else ():
                    r = Kit._raw_rect(c)
                    if r is None or not (M - 4 <= r[1] < M + 34 and r[1] + r[3] <= M + 36): continue
                    v = bool(c.IsVisible); rec["title"].append([c, None, None, v]); c.IsVisible = v and rec["open"]
                rec["kids"], rec["n"] = have, len(cur)
            Seam.watch(rec, False); return True
        keep = (rec["open"], rec["until"]) if rec is not None else (False, 0.0)
        if rec is not None: Seam.unstrip(g)
        r = Kit.rect(g); free = r is not None and g not in Seam.recs and not untitled
        title = Seam.title_of(raw, r[2]) if free else []
        frame = set(c for c in map(Kit.client_control, parts) if c is not None)
        title = [[c, None, None, bool(c.IsVisible)] for c in title if c not in frame]
        for p in parts: Kit.set(p, "IsVisible", False)
        for t in title: t[0].IsVisible = False
        Kit._prune(Seam.bare, 32)
        Seam.bare[g] = {"parts": parts, "n": n, "title": title, "open": keep[0], "until": keep[1], "band": bool(title),
                        "kids": set(Kit._children(raw))}
        for t in title: t[0].IsVisible = t[3] and keep[0]
        return True
    @staticmethod
    def unstrip(g):
        rec = Seam.bare.pop(g, None)
        if rec is None or not Kit.is_open(g): return
        on = Kit._frame_want.get(g, True)
        for p in rec["parts"]: Kit.set(p, "IsVisible", on)
        for t in rec["title"]:
            with Kit.quiet: t[0].IsVisible = t[3]
    @staticmethod
    def cut(pads):
        M = Kit.MARGIN; return M - pads[0], M + 30 + Kit.GAP - pads[1], M - pads[2], M - pads[3]
    @staticmethod
    def clip(slot, pads):
        W, H = Kit.screen(); M = Kit.MARGIN
        if W <= 0 or H <= 0: return pads
        return (min(M, max(pads[0], M - slot[0])), pads[1], min(M, max(pads[2], M - (W - slot[0] - slot[2]))),
                min(M, max(pads[3], M - (H - slot[1] - slot[3]))))
    @staticmethod
    def grow(slot, pads):
        l, t, r, b = Seam.cut(pads); return slot[0] - l, slot[1] - t, slot[2] + l + r, slot[3] + t + b
    @staticmethod
    def can(g, hooks, mini):
        return not (mini or isinstance(g, ClientWin) or hooks.get("untitled")) and bool(Kit._frame_parts.get(g)) \
            and g not in Kit._scrolled and Client.on_client_thread() and Seam.titled(g)
    @staticmethod
    def holds(g, slot, pads, grown, r):
        rec = Seam.recs.get(g)
        if rec is None or rec["slot"] != tuple(slot) or rec["pads"] != pads or r is None or r[:2] != grown[:2]:
            return False
        try:
            kids = rec["raw"].Children; n = int(kids.Count)
            if (n != rec["n"] or (n and kids[n - 1] is not rec["last"])) and not Seam.refresh(g, rec): return False
            rb = rec["catch"]
            if rb is not None and bool(rb.CanMove) != bool(LAYOUT.arrange): rb.CanMove = bool(LAYOUT.arrange)
        except Exception: return False
        Seam.watch(rec, True); return True
    @staticmethod
    def refresh(g, rec):
        cur = Kit._children(rec["raw"]); have = set(cur)
        if rec["catch"] is not None and rec["catch"] not in have: return False
        frame = set(c for c in map(Kit.client_control, Kit._frame_parts.get(g) or ()) if c is not None)
        rec["frame"] = [fv for fv in rec["frame"] if fv[0] in have]
        rec["title"] = [t for t in rec["title"] if t[0] in have]; new = [c for c in cur if c not in rec["kids"]]
        for c in new:
            if c in frame: rec["frame"].append((c, bool(c.IsVisible))); c.IsVisible = False
        Seam.adopt(rec, [c for c in new if c not in frame])
        rec["kids"], rec["n"], rec["last"] = have, len(cur), cur[-1] if cur else None; return True
    @staticmethod
    def adopt(rec, new):
        M = Kit.MARGIN; down = 30 + Kit.GAP
        for c in new:
            r = Kit._raw_rect(c)
            if r is None or not (M - 4 <= r[1] < M + 34 and r[1] + r[3] <= M + 36): continue
            rec["title"].append([c, r[0], r[1], bool(c.IsVisible)]); c.Location = ClientWin.point(r[0], r[1] + down)
            c.IsVisible = rec["open"] and rec["title"][-1][3]
    @staticmethod
    def watch(rec, trimmed):
        M = Kit.MARGIN; down = 30 + Kit.GAP
        for c, v in rec.get("frame", ()) if trimmed else ():
            try:
                if c.IsVisible: c.IsVisible = False
            except Exception: pass
        for t in rec["title"]:
            c = t[0]
            try:
                r = Kit._raw_rect(c) if trimmed else None
                if r is not None and r[1] < M + 34:
                    t[1], t[2], t[3] = r[0], r[1], bool(c.IsVisible); c.Location = ClientWin.point(r[0], r[1] + down)
                    c.IsVisible = rec["open"] and t[3]
                elif not rec["open"] and bool(c.IsVisible): t[3] = True; c.IsVisible = False
            except Exception: pass
    @staticmethod
    def trim(g, slot, pads):
        raw = Kit._raw_gump(g)
        if raw is None: return False
        M = Kit.MARGIN; down = 30 + Kit.GAP
        frame = set(c for c in map(Kit.client_control, Kit._frame_parts.get(g) or ()) if c is not None)
        hid, title = [], []
        for c in Kit._children(raw):
            r = Kit._raw_rect(c)
            if r is None: continue
            vis = bool(c.IsVisible)
            if c in frame: c.IsVisible = False; hid.append((c, vis))
            elif M - 4 <= r[1] < M + 34 and r[1] + r[3] <= M + 36:
                c.IsVisible = False; c.Location = ClientWin.point(r[0], r[1] + down); title.append([c, r[0], r[1], vis])
        l, t = Seam.cut(pads)[:2]; box = G.CreateGumpColorBox(0.01, "#000000"); box.SetRect(l, t, slot[2], slot[3])
        g.Add(box); Kit.flush(); rb = Kit.client_control(box)
        if rb is not None and raw.Children.Remove(rb):
            raw.Children.Insert(0, rb); rb.AcceptMouseInput = True; rb.CanMove = bool(LAYOUT.arrange)
            if len(Seam.catchers) > 64:
                for k in [k for k in Seam.catchers if k.IsDisposed]: Seam.catchers.pop(k, None)
            Seam.catchers[rb] = g
        was = bool(raw.AcceptMouseInput); Kit._prune(Seam.recs, 32)
        if rb is not None and rb in Seam.catchers: raw.AcceptMouseInput = False
        cur = Kit._children(raw); n = len(cur)
        Seam.recs[g] = {"slot": tuple(slot), "pads": pads, "raw": raw, "n": n, "frame": hid, "title": title,
                        "open": False, "until": 0.0, "box": box, "catch": rb, "mouse": was,
                        "last": cur[-1] if n else None, "kids": set(cur)}
        return True
    @staticmethod
    def undo(g):
        rec = Seam.recs.pop(g, None)
        if rec is None or not Kit.is_open(g): return False
        Seam.bare.pop(g, None); on = Kit._frame_want.get(g)
        for c, x, y, vis in [(c, None, None, v if on is None else on) for c, v in rec["frame"]] + rec["title"]:
            with Kit.quiet:
                if x is not None: c.Location = ClientWin.point(x, y)
                c.IsVisible = vis
        rec["raw"].AcceptMouseInput = rec["mouse"]; Seam.catchers.pop(rec.get("catch"), None); Kit.dispose(rec["box"])
        return True
    @staticmethod
    def undo_all():
        for g in list(Seam.recs): Seam.undo(g)
        for g in list(Seam.bare): Seam.unstrip(g)
    @staticmethod
    def hover(all_on=False):
        if not (Seam.recs or Seam.bare): return
        m = Kit.mouse_pos(); now = time.time(); sig = (m, all_on, len(Seam.recs), len(Seam.bare))
        if sig == Seam.seen[0] and now < Seam.seen[1]: return
        Seam.seen[0], Seam.seen[1] = sig, now + 0.25
        for d, trimmed in ((Seam.recs, True), (Seam.bare, False)):
            for g, rec in list(d.items()):
                if not rec["title"]: continue
                if not Kit.is_open(g): d.pop(g, None); continue
                r = rec["slot"] if trimmed else Kit.rect(g)
                if r is None: continue
                x, y, w, h = r; top = rec["pads"][1] if trimmed else Kit.MARGIN + 4
                band = 30 + top if rec["open"] else REVEAL_H
                if all_on or (m is not None and x <= m[0] < x + w and y <= m[1] < y + band):
                    rec["until"] = now + REVEAL_HOLD
                want = now < rec["until"]
                if want: Seam.seen[1] = min(Seam.seen[1], rec["until"])
                if want != rec["open"]:
                    rec["open"] = want
                    for t in rec["title"]:
                        try: t[0].IsVisible = want and t[3]
                        except Exception: pass


class Fade(object):
    EVERY = 0.2; HIT_EVERY = 1.0; PRUNE_EVERY = 2.0; RETRY = 1.0; NEAR = 0.003; CAP = 64
    TO, AFTER = (20, 90), (2, 30); KEYS = ("fade", "fade_to", "fade_after", "fade_all")
    ALL_ONLY = ("actionbar", "unitframes")
    def __init__(self):
        self.on = self.all = False; self.to, self.after = 0.4, 6.0; self.base = {}; self.dim = {}; self.gk = {}
        self.woke = {}; self.under = set(); self.mouse = self.sig = None; self.next = self.hit_at = self.prune_at = 0.0
        self.kids = {}; self.look_at = 0.0
    def load(self, host):
        self.opts(host.pref_int("fade", 0) == 1, host.pref_int("fade_to", 40), host.pref_int("fade_after", 6),
                  host.pref_int("fade_all", 0) == 1)
    def opts(self, on, to, after, all_):
        to = max(self.TO[0], min(self.TO[1], int(to))) / 100.0
        after = float(max(self.AFTER[0], min(self.AFTER[1], int(after)))); on, all_ = bool(on), bool(all_)
        if self.on and (not on or to != self.to or all_ != self.all): self.reset()
        self.on, self.to, self.after, self.all = on, to, after, all_
        if not on: self.base, self.woke = {}, {}
    def set(self, new):
        p = HOST.prefs
        for k in self.KEYS:
            try: p[k] = str(int(new[k]))
            except Exception: pass
        self.load(HOST); p["fade"], p["fade_all"] = ("1" if self.on else "0"), ("1" if self.all else "0")
        p["fade_to"], p["fade_after"] = str(int(round(self.to * 100))), str(int(self.after)); HOST.save_prefs()
    def reset(self):
        for k, gs in list(self.dim.items()):
            for g in gs:
                if Kit.is_open(g): self._walk(g, False)
        self.dim, self.gk, self.under, self.mouse, self.sig, self.kids = {}, {}, set(), None, None, {}
    def wake(self, key):
        now = time.time(); key = str(key); self.woke[key] = now; pre = key + "."
        for k in list(LAYOUT.wins) + list(Kit._wins):
            if k.startswith(pre) or LAYOUT.owner.get(k, (None,))[0] == key: self.woke[k] = now
    def _may(self, k, g, skip):
        if g in skip or g in Kit._behind or k in LAYOUT.behind or k.endswith("_alone"): return False
        if (LAYOUT.hooks.get(k) or {}).get("fade") is False: return False
        return self.all or not any(k == p or k.startswith(p + ".") for p in self.ALL_ONLY)
    def _units(self):
        c = HOST.config; own = (c.g if c is not None else None, ALERTS.g, HOST.alert_log.g)
        skip = set(g for g in own if g is not None)
        out = {}; seen = set(); no = set()
        for k, w in list(Kit._wins.items()):
            g = w.win.get(w.gkey)
            if not w.fade: no.add(k)
            elif Kit.is_open(g) and self._may(k, g, skip): out[k] = [g]; seen.add(g)
        for k in list(LAYOUT.wins):
            if k in out or k in no: continue
            g = LAYOUT.gump_of(k)
            if g is not None and g not in seen and not isinstance(g, ClientWin) and self._may(k, g, skip):
                out[k] = [g]; seen.add(g)
        for zid, rec in list(LAYOUT.strips.items()):
            sg = rec.get("g")
            if not Kit.is_open(sg): continue
            for k in LAYOUT.assign.get(zid) or ():
                if k in out and k not in LAYOUT.behind: out[k].append(sg); break
        return out
    @staticmethod
    def _kids(g):
        try:
            kids = Kit.client_control(g).Children; n = 0
            for i in range(int(kids.Count)): n += 1 + int(kids[i].Children.Count)
            return n
        except Exception: return -1
    @staticmethod
    def _over(g, m):
        r = Kit.rect(g); return r is not None and r[0] <= m[0] < r[0] + r[2] and r[1] <= m[1] < r[1] + r[3]
    def tick(self, now):
        if now < self.next or VA_ALONE: return
        self.next = now + self.EVERY; L = LAYOUT
        sig = (L.frames_name, L.layout_name, L.arrange, L.enabled, L.seamless, frozenset(L.behind), Kit.look())
        if sig != self.sig:
            if self.sig is not None: self.reset()
            self.sig = sig
        if L.arrange: return
        m = Kit.mouse_pos(); units = self._units(); woke = self.woke
        for k, gs in units.items():
            if self.gk.get(k) is not gs[0]: self.gk[k] = gs[0]; woke[k] = max(woke.get(k, 0.0), now)
        if m != self.mouse or now >= self.hit_at:
            self.mouse, self.hit_at = m, now + self.HIT_EVERY
            self.under = set(k for k, gs in units.items() if m is not None and any(self._over(g, m) for g in gs))
        for k in self.under:
            if k in units: woke[k] = now
        want = set(k for k in units if now - woke.get(k, now) >= self.after)
        for k, gs in list(self.dim.items()):
            if k not in want or units.get(k) != gs:
                self.dim.pop(k, None)
                for g in gs:
                    if Kit.is_open(g): self._walk(g, False)
        if now >= self.look_at:
            self.look_at = now + self.RETRY
            for k, gs in list(self.dim.items()):
                for g in gs:
                    if not Kit.is_open(g): continue
                    n = self._kids(g)
                    if n != self.kids.get(g, n): self.kids[g] = n; self._walk(g, True)
        for k in want:
            if k not in self.dim:
                if all([self._walk(g, True) for g in units[k]]):
                    self.dim[k] = list(units[k])
                    for g in units[k]: self.kids[g] = self._kids(g)
                else: woke[k] = now - self.after + self.RETRY
        if now >= self.prune_at: self.prune_at = now + self.PRUNE_EVERY; self._prune(units, now)
    def _prune(self, units, now):
        self.base = dict((g, r) for g, r in self.base.items() if Kit.is_open(g))
        self.kids = dict((g, n) for g, n in self.kids.items() if g in self.base)
        self.gk = dict((k, g) for k, g in self.gk.items() if k in units)
        self.woke = dict((k, t) for k, t in self.woke.items() if k in units or now - t < self.after)
    def _walk(self, g, on):
        old = self.base.get(g)
        if old is None:
            if not on: return False
            if len(self.base) >= self.CAP:
                self.base = dict((b, r) for b, r in self.base.items() if Kit.is_open(b))
                if len(self.base) >= self.CAP: return False
            old = {}
        new = {}; f = self.to; near = self.NEAR
        def one(c):
            try:
                a = float(c.Alpha); r = old.get(c)
                if on: b = r[0] if r is not None and abs(a - r[1]) <= near else a; v = b * f
                elif r is None: return
                elif abs(a - r[1]) > near: new[c] = (a, a); return
                else: b = v = r[0]
                c.Alpha = v; new[c] = (b, v)
            except Exception: pass
        ok = Kit.walk(g, one); self.base[g] = new; return ok


SNAP = Snap()
ALERTS = Alerts()
GUARD = Guard()
LAYOUT = Layout()
FADE = Fade()
HOST = Host()
MODULE_FILES = (("actionbar", "Action Bar", "ActionBarModule.py"), ("hud", "Character HUD", "CharacterHudModule.py"),
    ("interface", "Interface", "InterfaceModule.py"), ("inventory", "Inventory", "InventoryModule.py"),
    ("grimoire", "Grimoire", "GrimoireModule.py"), ("worldmap", "World Map", "WorldMapModule.py"),
    ("ultima", "Ultima Tracker", "UltimaTrackerModule.py"),
    ("social", "Social", "SocialModule.py"), ("prices", "Reagent Prices", "ReagentPricesModule.py"),
    ("skills", "Skills", "SkillsModule.py"),
    ("butler", "Property Butler", "PropertyButlerModule.py"), ("meters", "Meters", "MetersModule.py"),
    ("mongotchi", "Mongotchi", "MongotchiModule.py"),)
RETIRED_KEYS = ("autodoors",)


def module_folders():
    places = []; base = str(API.ScriptPath or "").rstrip("/\\")
    if base:
        if os.path.isfile(base): base = os.path.dirname(base)
        places += [base, os.path.dirname(base)]
    with Kit.quiet:
        import System; root = str(System.AppDomain.CurrentDomain.BaseDirectory).rstrip("/\\")
        places += [os.path.join(root, "LegionScripts"), root]
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
        import System; raw = System.IO.File.ReadAllBytes(path); text = System.Text.Encoding.UTF8.GetString(raw)
        if len(text) != raw.Length or "\ufffd" in text: raise ValueError(path)
    except Exception:
        try:
            with open(path, "r") as f: text = f.read()
        except Exception: import System; text = str(System.IO.File.ReadAllText(path))
        text = text.lstrip("\ufeff\xef\xbb\xbf")
    return text.replace("\r\n", "\n").replace("\r", "\n") if "\r" in text else text


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
    if not folders:
        Kit.say("no %s folder beside this script, so no modules loaded." % MODULE_DIR, Kit.HUE_BAD)
        HOST.prefs_frozen = True; return
    order = dict((f, i) for i, (_, _, f) in enumerate(MODULE_FILES)); entries, taken = [], set()
    for d in folders:
        try: names = os.listdir(d)
        except Exception as ex:
            names = []; Kit.say("couldn't read the %s folder (%s)." % (os.path.basename(d), ex), Kit.HUE_BAD)
            HOST.prefs_frozen = True
        for n in sorted(n for n in names if n.endswith("Module.py")):
            if n not in taken: taken.add(n); entries.append((d, n))
    if not entries or MODULE_DIR not in [os.path.basename(d) for d in folders]: HOST.prefs_frozen = True
    entries.sort(key=lambda e: order.get(e[1], len(order))); titles = dict((f, (k, t)) for k, t, f in MODULE_FILES)
    for where, name in entries:
        path = os.path.join(where, name); ship = os.path.basename(where) == MODULE_DIR; n0 = len(HOST.slots)
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
            if m is not None and m.interval is not None:
                HOST.add_lazy(m.key, m.title, m.desc, path, m.interval, m.default_on, m.category, m.parts, m.aliases)
                if len(HOST.texts) < 64: HOST.texts[path] = text
                continue
            exec(HOST.compiled(text, path), globals())
            if len(HOST.slots) == n0 and "HOST.add(" not in text:
                msg = "the file is empty or cut short"; Kit.say("couldn't load %s (%s)." % (name, msg), Kit.HUE_BAD)
                kt = titles.get(name)
                if kt is not None and not dict.__contains__(HOST.by_key, kt[0]):
                    s = HOST.add(kt[0], kt[1], "", lambda: None, 0.1); s.api, s.broken = None, msg
        except Exception as ex:
            line = getattr(ex, "lineno", None)
            if line: msg = "%s (%s line %s)" % (getattr(ex, "msg", None) or ex, name, line)
            else: msg = "%s%s" % (ex, _error_where())
            Kit.say("couldn't load %s (%s)." % (name, msg), Kit.HUE_BAD)
            kt = (m.key, m.title) if m is not None else titles.get(name)
            if kt is not None and not dict.__contains__(HOST.by_key, kt[0]):
                key, title = kt; s = HOST.add(key, title, "", lambda: None, 0.1); s.api, s.broken = None, msg
        finally:
            for s in HOST.slots[n0:]: s.shipped = ship


def _module_sysstats():
    KEY = "sysstats"; TITLE = "System Stats"
    POS_KEY, MIN_KEY, BTN_KEY, OPEN_KEY = ("SystemStats_pos", "SystemStats_min", "SystemStats_btn", "SystemStats_open")
    SIZE_KEY = "SystemStats_size"; W, W_MAX, MINI_W, MINI_H = 300, 600, 240, 46; TRAY_ICON = 0x1F2D
    EVERY, CLOSED_EVERY, RESIZE_SETTLE, SOCK_EVERY, BTN = 0.3, 2.0, 0.35, 1.0, 46
    ROWS = ("Ping", "FPS", "Frame", "Memory", "In", "Out", "Packets")
    TOP_MIN, TOP_MAX, TOP_EVERY, TOP_TITLE = 5, 12, 1.0, "BUSIEST PARTS  (share, ms)"
    VAL_W, VAL_WORST = 110, "100.0%, 99999 ms"
    TOP_KEYS = tuple(("top_name%d" % i, "top_val%d" % i) for i in range(TOP_MAX))
    M = Kit.MARGIN; YB = M + 30 + Kit.GAP; HB = len(ROWS) * 20 + 4; Y2 = YB + HB + Kit.GAP; FIXED_H = Y2 + 26 + M
    settings = {"startup": False, "tz_quiet": False}
    st = {"shutting": False, "minimized": False, "docked": False, "open": False, "queue": [],
          "next": 0.0, "vals": {}, "tip": None, "top_next": 0.0, "top": (), "size": None, "drawn": None,
          "resize_at": 0.0, "preview": False, "rows": TOP_MIN, "name_w": 100, "sock": (0.0, None), "gc": None,
          "ping": None}
    win = {"g": None, "c": {}, "store": ({}, {})}; btn = {"g": None, "b": None, "lbl": None, "store": ({}, {})}
    queue = Kit.queuer(st)
    def load_settings(): settings.update([(k, HOST.pref_int(k, 0) == 1) for k in list(settings)])
    def save_settings(): HOST.prefs.update([(k, "1" if v else "0") for k, v in settings.items()]); HOST.save_prefs()
    def own_size(w, h):
        n = max(TOP_MIN, min(TOP_MAX, (int(h) - FIXED_H + 10) // 20))
        return max(W, min(W_MAX, int(w))), FIXED_H + n * 20
    def load_size():
        try: w, h = [int(p) for p in Kit.get_var(SIZE_KEY, "").split(",")[:2]]
        except ValueError: return own_size(W, 0)
        return own_size(w, h)
    def busiest(now):
        rows = []
        for s in HOST.slots:
            if not s.running: continue
            if s.parts:
                pl = s.part_load
                rows.extend((Host.busy_share(pl[p[0]], now), pl[p[0]][2], p[1]) for p in s.parts
                            if p[0] in s.parts_running and p[0] in pl)
            else: rows.append((Host.busy_share(s.load, now), s.load[2], s.title))
        rows.sort(key=lambda r: -r[0]); nw = st["name_w"]
        return tuple((Kit.fit(t, nw), "%.1f%%, %d ms" % (b / 10.0, min(w, 99999))) for b, w, t in rows[:st["rows"]])
    def net_stats(now):
        at, stats = st["sock"]
        if stats is None or not 0 <= now - at <= SOCK_EVERY:
            stats = Tz.get(Tz.get(None, "Socket", Tz.T("ClassicUO.Network.AsyncNetClient")), "Statistics")
            st["sock"] = (now, stats)
        return stats
    def read(now):
        v = {}
        with Kit.quiet:
            fps = int(Tz.get(None, "CurrentRefreshRate", Tz.T("ClassicUO.CUOEnviroment"))); v["FPS"] = str(fps)
            v["Frame"] = "%.1f ms" % (1000.0 / fps) if fps > 0 else "-"
        with Kit.quiet:
            stats = net_stats(now); src = str(Typing._get(stats, "CurrentPingSource", default="") or "")
            v["Ping"] = "off" if src.endswith("Disabled") else "%d ms" % int(Tz.get(stats, "Ping"))
            v["In"] = "%.1f KB/s" % (int(Tz.get(stats, "DeltaBytesReceived")) / 1024.0)
            v["Out"] = "%.1f KB/s" % (int(Tz.get(stats, "DeltaBytesSent")) / 1024.0)
            v["Packets"] = "%d in, %d out" % (int(Tz.get(stats, "TotalPacketsReceived")),
                                              int(Tz.get(stats, "TotalPacketsSent")))
        with Kit.quiet:
            if st["gc"] is None: import System; st["gc"] = System.GC.GetTotalMemory
            v["Memory"] = "%d MB" % (int(st["gc"](False)) // (1024 * 1024))
        return v
    def show_ping(text):
        lbl = btn["lbl"]
        if lbl is None or text == st["ping"]: return
        st["ping"] = text
        if Kit.text_w(text) > BTN - 6: text = Kit.fit(text.replace(" ms", ""), BTN - 6)
        Kit.set_text(lbl, text); lbl.SetPos(max(3, (BTN - Kit.text_w(text)) // 2), (BTN - 16) // 2)
    def build_button():
        x, y = Kit.load_pos(BTN_KEY, (8, 200), (BTN, BTN)); store = ({}, {}); g = G.CreateGump(True, True)
        Kit.add_window_frame(g, BTN, BTN, corners=False); st["tip"] = st["ping"] = None
        lbl = Kit.inert(Kit.add_label(g, "", 3, (BTN - 16) // 2, Kit.HUE_TEXT))
        b = Kit.catcher(g, 0, 0, BTN, BTN, queue("toggle"), "Click to open or close System Stats; drag to move",
                        movable=True)
        Kit.show_window(g, x, y, BTN, BTN, None, False, None, lambda: Kit.save_pos(BTN_KEY, g), btn,
                        {"g": g, "b": b, "lbl": lbl, "store": store})
        show_ping(st["vals"].get("Ping", "-"))
    def build_window():
        held = HOST.layout_holds(KEY); st["resize_at"], st["preview"] = 0.0, False
        if st["size"] is None: st["size"] = load_size()
        ww, h = st["size"]; n = (h - FIXED_H) // 20; vw = max(VAL_W, Kit.text_w(VAL_WORST) + 4)
        st["rows"], st["name_w"] = n, ww - 2 * M - vw - 28
        rs = None if held else (W, FIXED_H + TOP_MIN * 20, on_resized); g, store, c = wnd.begin(ww, h, resize=rs)
        if not st["minimized"]:
            wnd.frame(g, mouse=rs is None); Kit.add_section(g, M, YB, ww - 2 * M, HB)
            st["top_next"] = time.time() + TOP_EVERY; st["top"] = busiest(time.time())
            for i, name in enumerate(ROWS):
                Kit.add_label(g, name + ":", M + 10, YB + 6 + i * 20, Kit.HUE_INFO)
                c[name] = Kit.add_label(g, "", M + 90, YB + 6 + i * 20, Kit.HUE_TEXT)
            Kit.add_section(g, M, Y2, ww - 2 * M, h - Y2 - M, Kit.fit(TOP_TITLE, ww - 2 * M - 16))
            for i, (kn, kv) in enumerate(TOP_KEYS[:n]):
                c[kn] = Kit.add_label(g, "", M + 10, Y2 + 26 + i * 20, Kit.HUE_INFO)
                c[kv] = Kit.add_label(g, "", ww - M - 10 - vw, Y2 + 26 + i * 20, Kit.HUE_TEXT)
        wnd.end(g); st["drawn"] = None if st["minimized"] else (ww, h); refresh()
    wnd = Kit.Window(KEY, TITLE, st, win, build_window, POS_KEY, default=(70, 200), mini=(MINI_W, MINI_H),
                     icon=TRAY_ICON)
    def refresh():
        v = st["vals"]; c = win["c"]
        if "status" in c:
            Kit.set_text(c["status"], "%s: %s, %s FPS" % (TITLE, v.get("Ping", "-"), v.get("FPS", "-"))); return
        for name in ROWS:
            lbl = c.get(name)
            if lbl is not None: Kit.set_text(lbl, v.get(name, "-"))
        top = st["top"]
        for i, (kn, kv) in enumerate(TOP_KEYS):
            if kn not in c: break
            row = top[i] if i < len(top) else ("", ""); Kit.set_text(c[kn], row[0]); Kit.set_text(c[kv], row[1])
    def on_resized(*args):
        st["resize_at"] = time.time(); g = win["g"]
        if st["preview"] or st["minimized"] or not Kit.is_open(g): return
        if (int(g.GetWidth()), int(g.GetHeight())) != st["drawn"]: st["preview"] = True; g.SetAlpha(0.55)
    def apply_resize():
        g = win["g"]; st["preview"] = False
        if not Kit.is_open(g) or st["minimized"]: return
        if HOST.layout_holds(KEY): g.SetAlpha(0); return
        gw, gh = int(g.GetWidth()), int(g.GetHeight()); drawn = st["drawn"] or (0, 0)
        if abs(gw - drawn[0]) <= 2 and abs(gh - drawn[1]) <= 2: g.SetAlpha(0); return
        sh = Kit.screen()[1]; size = own_size(gw, min(gh, sh) if sh > 0 else gh)
        st["size"] = size; Kit.put_var(SIZE_KEY, "%d,%d" % size); build_window()
    def page_table(w):
        load_settings()
        return (("START-UP", (("check", "startup", "Show start-up times",
                               "After loading, list in the journal how long each step took"),)),
                ("SHARD RULES", (("check", "tz_quiet", "Don't warn me about TazUO settings",
                                  "No journal line when a TazUO setting breaks this shard's rules"),)))
    cfg = Kit.Page(settings, page_table, save_settings)
    def open_window():
        st["open"] = True; st["next"] = 0.0; build_window(); wnd.dock()
    def close_window():
        st["open"] = False; st["top"] = (); HOST.dock_remove(KEY); wnd.close(); Kit.put_var(OPEN_KEY, "0")
    def _start():
        load_settings()
        st.update({"shutting": False, "docked": False, "queue": [], "next": 0.0, "top_next": 0.0, "size": None,
                   "resize_at": 0.0, "preview": False, "sock": (0.0, None), "minimized": Kit.load_min(MIN_KEY)
                   or HOST.dock_wanted(KEY), "open": Kit.get_var(OPEN_KEY, "0") == "1"})
        build_button()
        if st["open"] or HOST.layout_holds(KEY): open_window()
    def _tick():
        now = time.time()
        while st["queue"]:
            action = st["queue"].pop(0)
            if action == "toggle":
                if Kit.just_dragged(btn["g"]): continue
                if st["open"] and not HOST.layout_holds(KEY): close_window()
                elif not st["open"]: Kit.put_var(OPEN_KEY, "1"); st["minimized"] = st["docked"] = False; open_window()
            elif action == "redraw":
                if st["open"]: build_window()
            else: Kit.win_action(action, st, KEY, TITLE, build_window, MIN_KEY)
        if st["open"] and Kit.was_clicked(win["store"], "close"): close_window()
        if st["resize_at"] and now - st["resize_at"] >= RESIZE_SETTLE and not (SNAP.drag or SNAP.pressed() is True):
            st["resize_at"] = 0.0; apply_resize()
        if not st["open"] and HOST.layout_holds(KEY): open_window()
        if not 0 <= st["next"] - now <= CLOSED_EVERY:
            st["next"] = now + (EVERY if st["open"] else CLOSED_EVERY); v = st["vals"] = read(now)
            show_ping(v.get("Ping", "-"))
            tip = "Ping %s, %s FPS, memory %s; click to open or close, drag to move" % (
                v.get("Ping", "-"), v.get("FPS", "-"), v.get("Memory", "-"))
            if tip != st["tip"] and btn["b"] is not None: st["tip"] = tip; Kit.with_tip(btn["b"], tip)
            if st["open"] and not st["minimized"] and not 0 <= st["top_next"] - now <= TOP_EVERY:
                st["top_next"] = now + TOP_EVERY; st["top"] = busiest(now)
            if st["open"] and win["g"] is not None and not (st["minimized"] and st["docked"]): refresh()
    def _stop():
        st["shutting"] = True; HOST.dock_remove(KEY); Kit.save_min(MIN_KEY, st["minimized"])
        Kit.put_var(OPEN_KEY, "1" if st["open"] else "0"); wnd.close(); b, btn["g"] = btn["g"], None
        btn["b"] = btn["lbl"] = None; Kit.save_pos(BTN_KEY, b); Kit.dispose(b)
    return {"start": _start, "tick": _tick, "stop": _stop, "client_tick": True, "config_height": cfg.height,
            "build_config": cfg.build, "poll_config": cfg.poll, "config_closed": cfg.closed}


if not VA_ALONE:
    if not HOST.self_run(globals()):
        Kit.data_setup(); PROFILES = Profiles(); HOST.boot_mark("data setup")
        load_modules(); HOST.boot_mark("module files")
        try: PROFILES.startup()
        except Exception as _ex:
            Kit.say("couldn't put the favourite profile on this character (%s%s)."
                    % (Tz.why(_ex), _error_where()), Kit.HUE_BAD)
        HOST.boot_mark("profiles")
        HOST.add("sysstats", "System Stats", "Ping, FPS and memory button", _module_sysstats, 0.1,
                 category="On screen").shipped = True
        HOST.run()
else: Kit.data_setup(); PROFILES = Profiles()
