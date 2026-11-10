import API
import math
import os
import re
import struct
import time
APP_NAME="Virtue Assistant"
APP_VERSION="2.7.0.25"
MODULE_DIR="VirtueAssistantModules"
SETTINGS_DIR="VirtueAssistantSettings"
SETTINGS_KEY="VirtueAssistant_settings"
VA_ALONE="VA_ALONE"in globals()
ALIVE_KEY="VirtueAssistant_alive"
ALONE_PARTS="VirtueAssistant_alone_parts_%s"
HOST_TICK=.02
UI_TICK=.05
UI_IDLE=.12
UI_IDLE_AFTER=2.
GRID_DEFAULT=32
SNAP_ANCHOR=40
KEEP_EVERY=.5
KEEP_SWEEP=2.
PROFILE_DIR="VirtueAssistantProfiles"
PROFILE_STATE_KEY="VirtueAssistant_profile"
PROFILE_NAME_MAX=32
ALERT_RATE=10.
ALERT_HOLD=8.
ALERT_SOUND_GAP=.4
ALERT_FLASH=.5
ALERT_SOUNDS=(("Silent",0),("Chime",490),("Harp note",976),("Lever",74),("Whistle",821),("Yell",824),("War drum",743),("Trap snap",495),("Boom",775),("Recall",508),("Heal tone",514),("Bird",23),("Smack",946),("Harm",497),("Cure",480))
GUARD_IN_TEXTS=("you are now under the protection of the town guards",)
GUARD_OUT_TEXTS=("you have left the protection of the town guards","beware! you have left the protection of the town guards")
GUARD_AREAS=()
GUARD_SPOT=3
FOE_RANGE=12
FOE_EVERY=1.
FOE_NOTO=(5,6)
FOE_WAR_NOTO=(3,4)
HURT_SECS=10.
MAX_MODULE_ERRORS=25
ERROR_SECS=60.
GUMP_EXPECT_MAX=30.
ATTACK_HUE=34
HARM_SECS=3.
HARM_DOUBLE=.6
HARM_NOTO=("innocent","ally","odd")
HOLD_TEXT={"dead":"you are dead","war":"war mode","hurt":"you took damage","foe":"a hostile is near","item":"you are moving an item","alarm":"an alarm needs you","guard":"guard zone","unknown":"Guard zone not known yet: cross a town's guard line once","attacked":"you are being attacked",}
CATEGORY_ORDER=("On screen","Your things","The world","Skills and home","Extras","Other")
SEARCH_SETTLE=.3
WHATS_NEW_KEY="VirtueAssistant_seen_version"
def whats_new():
	import sys;d=module_folders()
	if not d:return()
	if d[0]not in sys.path:sys.path.insert(0,d[0])
	sys.modules.pop("_WhatsNew",None)
	try:import _WhatsNew;return tuple(_WhatsNew.WHATS_NEW)
	except Exception:return()
class _Gumps(object):
	def __init__(self,inner):self._inner=inner
	def __getattr__(self,name):v=getattr(self._inner,name);self.__dict__[name]=v;return v
	def AddControlOnClick(self,ctrl,fn):
		a=HOST.click_key()
		def b(*b):
			try:fn(*b)
			finally:HOST.poke(a)
		self._inner.AddControlOnClick(ctrl,b)
	def AddGump(self,g):
		Kit.set(g,"CanCloseWithRightClick",False);Kit.set(Kit._raw_gump(g),"CanCloseWithRightClick",False);p=Kit._pend.get(g)
		if(p is not None and p[2]and p[3])or g in Kit._scrolled:Kit.pin_size(g)
		r=self._inner.AddGump(g)
		with Kit.quiet:
			SNAP.add(g)
			if LAYOUT.loaded:LAYOUT.fresh_adds.add(g)
		return r
G=_Gumps(API.Gumps)
def safe(fn,default=None):
	try:return fn()
	except Exception:return default
class Client(object):
	looked=False;mouse=None;keys={};NO_CLICK_TIME=1;_types={};_client_asm=False;TYPE_RETRY=30.
	@staticmethod
	def _type(name):
		a=Client._types.get(name)
		if a is not None:
			if type(a)is not tuple:return a
			if time.time()-a[1]<Client.TYPE_RETRY:return
		t=None
		try:
			if Client._client_asm is False:
				Client._client_asm=None
				try:Client._client_asm=API.GetType().Assembly
				except Exception:pass
			b=Client._client_asm
			if b is not None:
				try:t=b.GetType(name,False)
				except Exception:t=None
			if t is None:
				import System
				for b in System.AppDomain.CurrentDomain.GetAssemblies():
					try:t=b.GetType(name,False)
					except Exception:t=None
					if t is not None:break
		except Exception:t=None
		Client._types[name]=t if t is not None else(None,time.time());return t
	@staticmethod
	def flags(static=False,public=True):from System.Reflection import BindingFlags;return((BindingFlags.Static if static else BindingFlags.Instance)|BindingFlags.NonPublic|(BindingFlags.Public if public else BindingFlags.Default))
	@staticmethod
	def _member(t,name):
		import System;a=Client.flags(True);p=t.GetProperty(name,a)
		if p is not None:return(lambda:p.GetValue(None,None),lambda v:p.SetValue(None,System.Convert.ChangeType(v,p.PropertyType),None))
		f=t.GetField(name,a)
		if f is not None:return(lambda:f.GetValue(None),lambda v:f.SetValue(None,System.Convert.ChangeType(v,f.FieldType)))
		return
	@staticmethod
	def find():
		if Client.looked:return
		Client.looked=True;a=Client._type("ClassicUO.Input.Mouse")
		if a is not None:
			try:m=Client._member(a,"LastLeftButtonClickTime");int(m[0]());Client.mouse=m
			except Exception:Client.mouse=None
		b=Client._type("ClassicUO.Input.Keyboard")
		if b is not None:
			for c,d in(("alt","Alt"),("shift","Shift"),("ctrl","Ctrl")):
				with Kit.quiet:m=Client._member(b,d);bool(m[0]());Client.keys[c]=m[0]
	@staticmethod
	def second_click_swallowed():
		Client.find()
		if Client.mouse is None:return False
		a,b=Client.mouse
		try:c=int(a());b(Client.NO_CLICK_TIME);return c in(0,0xFFFFFFFF)
		except Exception:return False
	@staticmethod
	def typing():return bool(safe(Typing.now,False))
	@staticmethod
	def key_held(b):
		if not Client.looked:Client.find()
		a=Client.keys.get(b)
		if a is None:return
		try:return bool(a())
		except Exception:return False
	MTQ=None;mtq_looked=False;main_call=None
	@staticmethod
	def _find_mtq():
		if Client.mtq_looked:return Client.MTQ
		Client.mtq_looked=True
		try:import clr;clr.AddReference(API.GetType().Assembly);from ClassicUO.Game.Managers import MainThreadQueue;Client.MTQ=MainThreadQueue
		except Exception:Client.MTQ=None
		return Client.MTQ
	@staticmethod
	def on_client_thread():
		a=Client.MTQ if Client.mtq_looked else Client._find_mtq()
		if a is None:return False
		try:return bool(a.IsMainThread)
		except Exception:return False
	@staticmethod
	def _pick_main_call():
		from System import Func;a=Client.MTQ;F=Func[object]
		def d():
			b=a.InvokeOnMainThread[object]
			def c(run):b(F(run))
			return c
		def e():
			def b(run):a.InvokeOnMainThread(F(run))
			return b
		def f():
			from System import Action;from System.Threading import ManualResetEventSlim
			def b(run):
				b=ManualResetEventSlim(False)
				def c():
					try:run()
					finally:b.Set()
				a.EnqueueAction(Action(c))
				if not b.Wait(5000):raise _HopTimeout("the client thread didn't answer in 5 s")
			return b
		for g in(d,e,f):
			b={}
			def h():b["ok"]=True
			try:c=g();c(h)
			except Exception:continue
			if b.get("ok"):return c
		return
	@staticmethod
	def on_main_ex(fn):
		Client.exc=None
		if(Client.MTQ if Client.mtq_looked else Client._find_mtq())is None:return "no",None
		if Client.on_client_thread():
			try:return "ok",fn()
			except Exception as a:Client.error=str(getattr(a,"InnerException",None)or a);Client.exc=a;return "err",Client.error
		c=Client.main_call
		if c is None:
			c=Client.main_call=Client._pick_main_call()
			if c is None:Client.error="can't run on the client thread";return "no",None
		b=_Hop(fn)
		try:c(b.run)
		except _HopTimeout as a:Client.error=str(a);return "err",Client.error
		except Exception as a:Client.error=str(a);return "no",None
		if b.e is not None:Client.error,Client.exc=b.e,b.x;return "err",b.e
		return "ok",b.v
	error="";exc=None
class _HopTimeout(Exception):pass
class _Hop(object):
	__slots__=("fn","v","e","x")
	def __init__(self,fn):self.fn,self.v,self.e,self.x=fn,None,None,None
	def run(self):
		try:self.v=self.fn()
		except Exception as a:self.e=str(getattr(a,"InnerException",None)or a);self.x=a
		except:self.e="unknown error"
class Typing(object):
	looked=False;uim=None;prof=None;_members={};_flags=None;_prof_t=None;_chat_t=None;_now_memo=[-1,False]
	@staticmethod
	def _find():
		if Typing.looked:return
		Typing.looked=True;Typing.uim=Client._type("ClassicUO.Game.Managers.UIManager");Typing.prof=Client._type("ClassicUO.Configuration.ProfileManager")
	@staticmethod
	def _lookup(t,name,static):
		if Typing._flags is None:from System.Reflection import BindingFlags;c=BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.DeclaredOnly;Typing._flags=(c|BindingFlags.Instance,c|BindingFlags.Static)
		d=Typing._flags[1 if static else 0];m,b,a=None,False,t
		while a is not None and m is None:
			try:m=a.GetProperty(name,d)
			except Exception:m=None
			if m is not None:b=True
			else:m=a.GetField(name,d)
			a=a.BaseType
		if m is None and not static:
			for e in t.GetInterfaces():
				m=e.GetProperty(name)
				if m is not None:b=True;break
		return(m,b)if m is not None else None
	@staticmethod
	def _get(obj,name,t=None,default=None):
		try:
			a=obj is None
			if t is None:t=obj.GetType()
			b=(t,name,a);m=Typing._members.get(b,False)
			if m is False:m=Typing._members[b]=Typing._lookup(t,name,a)
			if m is None:return default
			if m[1]:return m[0].GetValue(obj,None)
			return m[0].GetValue(obj)
		except Exception:return default
	@staticmethod
	def _same(a,b):return a is not None and b is not None and bool(Kit._same()(a,b))
	@staticmethod
	def _ptype(cur):
		t=Typing._prof_t
		if t is None:
			try:t=Typing._prof_t=cur.GetType()
			except Exception:t=None
		return t
	@staticmethod
	def hop(b,fn):
		try:h=HOST;a=h.pass_id if h.in_hop else None
		except Exception:a=None
		if a is not None and b[0]==a:return b[1]
		v=fn()
		if a is not None:b[0]=a;b[1]=v
		return v
	@staticmethod
	def now():return Typing.hop(Typing._now_memo,Typing._now)
	@staticmethod
	def _now():
		Typing._find();e=Typing.uim
		if e is None:return False
		a=Typing._get(None,"KeyboardFocusControl",e);b=Typing._get(None,"SystemChat",e);c=None
		if b is not None:
			d=Typing._chat_t
			if d is None:
				try:d=Typing._chat_t=b.GetType()
				except Exception:d=None
			c=Typing._get(b,"TextBoxControl",d)
		if a is not None and not Typing._same(a,c)and not bool(Typing._get(a,"IsDisposed",default=False))and bool(Typing._get(a,"IsVisible",default=True))and bool(Typing._get(a,"AcceptKeyboardInput",default=True)):return True
		if b is None:return False
		g=True
		if Typing.prof is not None:
			f=Typing._get(None,"CurrentProfile",Typing.prof)
			if f is not None:v=Typing._get(f,"ActivateChatAfterEnter",Typing._ptype(f));g=True if v is None else bool(v)
		if g and bool(Typing._get(b,"IsActive",Typing._chat_t,default=False)):return True
		h=Typing._get(c,"Text")if c is not None else None;return h is not None and len(str(h))>0
	@staticmethod
	def release():
		Typing._now_memo[0]=-1
		def a():
			Typing._find();a=Typing.uim
			if a is None:return
			try:
				m=a.GetMethod("RestoreSystemChatFocus",Client.flags(True))
				if m is not None:m.Invoke(None,None);return
			except Exception:pass
			b=Typing._get(None,"SystemChat",a);c=Typing._get(b,"TextBoxControl")if b is not None else None
			if c is not None:safe(lambda:c.SetKeyboardFocus())
		if Client.on_client_thread():safe(a)
		else:Client.on_main_ex(a)
class Follow(object):
	serial=None;readers=None;ALT_NAMES=("ALT","LALT","RALT","LEFTALT","RIGHTALT","MENU","LMENU","RMENU");SDL_ALT=768
	@staticmethod
	def _find():
		if Follow.readers is not None:return
		r=[]
		try:
			import clr
			for b in("ClassicUO","ClassicUO.Client","TazUO","FNA","SDL2-CS","SDL3-CS"):safe(lambda:clr.AddReference(b))
		except Exception:pass
		Client.find()
		if "alt"in Client.keys:r.append(lambda:Client.key_held("alt"))
		try:from ClassicUO.Input import Keyboard;bool(Keyboard.Alt);r.append(lambda:bool(Keyboard.Alt))
		except Exception:pass
		for c in("SDL2","SDL3"):
			try:a=__import__(c).SDL;int(a.SDL_GetModState());r.append(lambda a=a:(int(a.SDL_GetModState())&Follow.SDL_ALT)!=0)
			except Exception:pass
		Follow.readers=r
	@staticmethod
	def alt_held():
		Follow._find()
		for a in Follow.readers:
			if safe(a,False):return True
		if Follow.readers:return False
		for k in Follow.ALT_NAMES:
			if safe(lambda:API.IsKeyPressed(k),False):return True
		return False
	_memo=[-1,None]
	@staticmethod
	def current():return Typing.hop(Follow._memo,Follow._current)
	@staticmethod
	def _current():
		Typing._find();a=Typing._get(None,"CurrentProfile",Typing.prof)if Typing.prof is not None else None
		if a is not None:
			b=Typing._ptype(a);c=Typing._get(a,"FollowingMode",b)
			if c is not None:
				if not bool(c):Follow.serial=None;return
				t=Typing._get(a,"FollowingTarget",b)
				if t is not None:
					try:Follow.serial=int(t)or None
					except Exception:pass
				return Follow.serial
		if Follow.serial is not None and API.FindMobile(Follow.serial)is None:Follow.serial=None
		return Follow.serial
	@staticmethod
	def start(serial,who=APP_NAME):
		serial=int(serial or 0)
		if not serial:return False
		a=int(safe(lambda:API.Player.Serial,0)or 0)
		if serial==a:API.SysMsg("%s: you can't follow yourself."%who,Kit.HUE_INFO);return False
		if API.FindMobile(serial)is None:API.SysMsg("%s: can't follow them, they are out of sight."%who,Kit.HUE_BAD);return False
		try:API.AutoFollow(serial)
		except Exception as b:API.SysMsg("%s: couldn't auto-follow (%s)."%(who,b),Kit.HUE_BAD);return False
		Follow.serial=serial;Follow._memo[0]=-1;API.HeadMsg("* following *",serial,68);return True
	@staticmethod
	def stop(who=APP_NAME):
		s=Follow.serial;Follow._memo[0]=-1;API.CancelAutoFollow();Follow.serial=None
		if s:API.HeadMsg("* stopped following *",s,53)
	@staticmethod
	def toggle(serial,who=APP_NAME):
		serial=int(serial or 0)
		if serial and Follow.current()==serial:Follow.stop(who);return False
		return Follow.start(serial,who)
class Kit(object):
	WINDOW_BG=5054;STONE_TILE=5058;SECTION_TILE=2624;SECTION_ALPHA=.8;FIELD_TILE=2624;CORNER_ART=10460;ART_PLAY=(4005,4007,4006);ART_CLOSE=(4017,4019,4018);DARK_HUE=1899;DARK_CORNER_HUE=2305;DARK_SECTION_ALPHA=.95;LIGHT_SECTION_ALPHA=.8;GOLD_H=2700;GOLD_V=2701;GOLD_T=3;_dark={};_wins={};ART_OK=(4023,4025,4024);ART_PAGE=(4011,4013,4012);ART_MIN=(253,252,253);ART_RESTORE=(251,250,251);ART_DOCK=(5602,5606,5602);ART_CIRCLE=(2117,2118,2118);DOCK_DX,DOCK_DY=20,2;DOCK_TIP="Fold into the Action Bar's tray";MIN_TIP="Minimize (or double-click the title)";RESTORE_TIP="Restore";SETTINGS_TIP="Open %s settings";CLOSE_TIP="Close %s (turns it off)";DOUBLE_TIP="Double-click: minimize or restore";LINE_RED,LINE_BLUE,LINE_POISON=2053,2054,2056;HUE_TITLE=53;HUE_TEXT=1153;HUE_GOOD=68;HUE_BAD=33;HUE_INFO=946;MARGIN=12;GAP=8;_sizes={}
	@staticmethod
	def on_client(fn,fallback=True):
		a,v=Client.on_main_ex(fn)
		if a=="ok":return v
		if a=="err":raise Client.exc if isinstance(Client.exc,Exception)else Exception(Client.error)
		return fn()if fallback else None
	_screen={"wh":(0,0),"at":0.}
	@staticmethod
	def screen():
		b=time.time()
		if b-Kit._screen["at"]>=1.:
			Kit._screen["at"]=b
			try:c=API.GetClientBounds();a=(int(c.Width),int(c.Height))
			except Exception:a=None
			if a and a[0]>0 and a[1]>0:
				s=Kit.render_scale()
				if abs(s-1.)>.001:a=(int(round(a[0]/s)),int(round(a[1]/s)))
				Kit._screen["wh"]=a
		return Kit._screen["wh"]
	_scale={"fn":None,"looked":False}
	@staticmethod
	def render_scale():
		a=Kit._scale
		if not a["looked"]:
			a["looked"]=True
			try:t=Client._type("ClassicUO.Client");b=t.GetProperty("Game",Client.flags(True));c=b.GetValue(None,None);d=c.GetType().GetProperty("RenderScale",Client.flags());float(d.GetValue(c,None));a["fn"]=lambda:float(d.GetValue(b.GetValue(None,None),None))
			except Exception:a["fn"]=None
		e=a["fn"]
		if e is None:return 1.
		try:s=e();return s if.25<=s<=4. else 1.
		except Exception:return 1.
	ANCHORS=("TL","T","TR","L","C","R","BL","B","BR");SCREEN_KEY="VirtueAssistant_screen";_pos_screen=None
	@staticmethod
	def clamp(x,y,w,h):
		W,H=Kit.screen();x,y,w,h=int(x or 0),int(y or 0),int(w or 0),int(h or 0)
		if W>0:x=max(0,min(x,W-w))if w<=W else max(W-w,min(x,0))
		if H>0:y=max(0,min(y,H-h))if h<=H else max(H-h,min(y,0))
		return x,y
	_frame_parts={};_pend={};PEND_FOR=1.
	@staticmethod
	def note_rect(g,x,y,w=None,h=None):
		if g is None:return
		try:
			r=None
			if Kit._pend:r=Kit.rect(g)
			a=Kit._pend.get(g)
			if w is None and a is not None:w,h=a[2],a[3]
			if a is not None:b=a[5]
			elif r is not None:b=r
			else:b=(int(g.GetX()),int(g.GetY()),int(g.GetWidth()or 0),int(g.GetHeight()or 0))
			Kit._pend[g]=(int(x),int(y),None if w is None else int(w),None if h is None else int(h),time.time(),b)
		except Exception:pass
	@staticmethod
	def rect(g):
		try:x,y=int(g.GetX()),int(g.GetY());w,h=int(g.GetWidth()or 0),int(g.GetHeight()or 0)
		except Exception:return
		a=Kit._pend
		if a:
			p=a.get(g)
			if p is not None:
				b=w if p[2]is None else p[2];c=h if p[3]is None else p[3]
				if(x,y,w,h)==(p[0],p[1],b,c)or(x,y,w,h)!=p[5]or time.time()-p[4]>Kit.PEND_FOR:del a[g]
				else:return p[0],p[1],b,c
		return x,y,w,h
	@staticmethod
	def pos(g):
		if Kit._pend and g in Kit._pend:r=Kit.rect(g);return None if r is None else(r[0],r[1])
		try:return int(g.GetX()),int(g.GetY())
		except Exception:return
	@staticmethod
	def prune_pending():
		if len(Kit._pinned)>400:Kit._pinned=set(b for b in Kit._pinned if Kit.is_open(b))
		if not Kit._pend:return
		a=time.time()
		for g in[c for c,d in Kit._pend.items()if a-d[4]>Kit.PEND_FOR]:Kit._pend.pop(g,None)
	@staticmethod
	def place(g,x,y,w,h,head=None,max_h=None):
		a=Fill.recs.get(g)if Fill.recs else None
		if a is not None and a["slot"]is not None:
			a["nat"],a["size"]=(int(w or 0),int(h or 0)),None;b,c,d,e=a["slot"]
			if Kit.on_client(lambda:Fill.fit(g,b,c,d,e,a["mode"]),fallback=False)is not None:return b,c
			Fill.recs.pop(g,None)
		return Kit._place_raw(g,x,y,w,h,head,max_h)
	@staticmethod
	def _place_raw(g,x,y,w,h,head=None,max_h=None):
		w,h=int(w or 0),int(h or 0);H=Kit.screen()[1];a=H if not max_h else min(H,int(max_h))
		if a>0 and(h>a or g in Kit._scrolled):
			b=Kit.scroll_fit(g,w,h,head,int(max_h)if max_h else None)
			if b is not None:w,h=b
		x,y=Kit.clamp(x,y,w,h);g.SetRect(x,y,w,h);Kit.note_rect(g,x,y,w,h)
		if g not in Kit._pinned:Kit.pin_size(g)
		return x,y
	_pinned=set()
	@staticmethod
	def pin_size(g,raw=None):
		try:
			raw=raw if raw is not None else Kit._raw_gump(g)
			if raw is None:return False
			if raw.WantUpdateSize:raw.WantUpdateSize=False
			Kit._pinned.add(g);return True
		except Exception:return False
	SCROLL_BAND=15;_frames={};_scrolled={};scroll_info=_scrolled.get;_rawmode={}
	@staticmethod
	def scroll_fit(g,w,h,head=None,b=None):
		try:
			H=Kit.screen()[1]
			if b:H=min(H,int(b))
			a=Kit._scrolled.get(g)
			if a is not None and a["w"]==w and a["h"]==h and a["H"]==H:return a["w2"],a["hv"]
			if head is None:head=a["head"]if a is not None else Kit.MARGIN+30+Kit.GAP
			c=Kit.on_client(lambda:Kit._scroll_build(g,w,h,int(head),H),fallback=False)
			if c is not None:Kit._scrolled[g]["lim"]=int(b)if b else None
			return c
		except Exception:return
	@staticmethod
	def _raw_rect(c):
		a=Kit._rawmode
		try:b=c.Location;x,y=int(b.X),int(b.Y)
		except Exception:return
		d=a.get("how")
		if d!="reflect":
			try:w,h=int(c.Width),int(c.Height);a["how"]="direct";return x,y,w,h
			except Exception:a["how"]="reflect"
		try:t=c.GetType();e=t.GetProperty("Width");f=t.GetProperty("Height");return x,y,int(e.GetValue(c,None)),int(f.GetValue(c,None))
		except Exception:return
	@staticmethod
	def _raw_gump(g):
		try:
			a=g.Gump
			if a is not None:return a
		except Exception:pass
		return Kit.client_control(g)
	@staticmethod
	def _children(raw):a=raw.Children;return[a[b]for b in range(int(a.Count))]
	@staticmethod
	def _scroll_build(g,w,h,head,H):
		M=Kit.MARGIN
		if not Kit.flush():return
		a=Kit._raw_gump(g)
		if a is None:return
		b=min(h,H);head=max(0,min(head,b-M-40));e=w+Kit.SCROLL_BAND;p=w-M+14;q=b-M;s=Kit._scrolled.get(g)
		if s is not None:return Kit._scroll_refit(g,s,a,w,h,H,b,e,p,q,head)
		d=Kit._frames.get(g);i=d["corners"]if d else True;j=d["mouse"]if d else True;t=list(d["pieces"])if d else[];u,v,k,l=[],[],[],[];y=[C for C in map(Kit.client_control,t)if C is not None];z=Kit._same()
		for c in Kit._children(a):
			try:
				if c.IsDisposed:continue
			except Exception:continue
			if any(z(c,D)for D in y):continue
			r=Kit._raw_rect(c)
			if r is None:return
			u.append(c);x,A=r[1],r[3]
			if x<=0 and A>=h-2:l.append(c)
			elif x<head:k.append(c)
			else:v.append(c)
		Kit._frames.pop(g,None)
		for B in t:Kit.dispose(B)
		m=f=n=None
		try:
			f=G.CreateGumpScrollArea(0,0,p,q);m=Kit._scroll_frame(g,e,b,i,j)
			if not Kit.flush():raise Exception("queue")
			for c in l:c.Parent=a
			g.Add(f)
			if not Kit.flush():raise Exception("queue")
			o=Kit.client_control(f)
			if o is None:raise Exception("no area")
			for c in v:c.Parent=o
			n=Kit._scroll_band(g,w,e,b,head,i,j)
			if not Kit.flush():raise Exception("queue")
			for c in k:c.Parent=a
		except Exception:Kit._scroll_undo(g,a,w,h,i,j,u,m,f,n);return
		Kit._scroll_note(g,a,w,h,H,e,b,head,f,o,m,n,k,l,i,j);return e,b
	@staticmethod
	def _scroll_refit(g,info,raw,w,h,H,hv,w2,m,n,head):
		d=a=e=None;j=False
		try:
			for p in info["frame"]+info["band"]:Kit.dispose(p)
			o,q=info["area"],info["area_raw"];k=[s for s in info["header"]if not s.IsDisposed];l=[t for t in info["fixed"]if not t.IsDisposed];f,i=info["corners"],info["mouse"];d=Kit._scroll_frame(g,w2,hv,f,i)
			if not Kit.flush():raise Exception("queue")
			for c in l:c.Parent=raw
			a=G.CreateGumpScrollArea(0,0,m,n);g.Add(a)
			if not Kit.flush():raise Exception("queue")
			b=Kit.client_control(a)
			if b is None:raise Exception("no area")
			r=Kit._children(q)
			for c in r[1:]:
				try:
					if not c.IsDisposed:c.Parent=b
				except Exception:pass
			Kit.dispose(o);j=True;e=Kit._scroll_band(g,w,w2,hv,head,f,i)
			if not Kit.flush():raise Exception("queue")
			for c in k:c.Parent=raw
		except Exception:
			if j:info.update(area=a,area_raw=b)
			else:Kit.dispose(a)
			info.update(frame=d or[],band=e or[],known=None,skip_raw=None);return
		Kit._scroll_note(g,raw,w,h,H,w2,hv,head,a,b,d,e,k,l,f,i);return w2,hv
	@staticmethod
	def _scroll_frame(g,w2,hv,corners,mouse):return Kit._add_corners(g,Kit._frame_pieces(g,w2,hv,False,mouse),w2,hv,corners,mouse)
	@staticmethod
	def _add_corners(g,out,right,hv,corners,mouse):
		a,b=Kit.pic_size(Kit.CORNER_ART)if corners and Kit.CORNER_ART else(0,0)
		if a and b:
			for c in(0,hv-b):
				p=Kit.add_pic(g,Kit.CORNER_ART,0 if right is None else right-a,c,mouse=mouse)
				if p is not None:out.append(p);Kit._note_frame_part(g,p)
		return out
	@staticmethod
	def _scroll_band(g,w,w2,hv,head,corners,mouse):
		M=Kit.MARGIN;a=[];b=Kit.pic_size(Kit.WINDOW_BG+3)[0]or M;c=Kit.pic_size(Kit.WINDOW_BG+1)[1]or M;t=Kit.add_tiled(g,Kit.STONE_TILE,b,c,w-M-b,head-c)
		if t is not None:t.SetAcceptMouseInput(True);t.CanMove=True;a.append(t)
		return Kit._add_corners(g,a,None,hv,corners,mouse)
	@staticmethod
	def _note_frame_part(g,p):
		a=Kit._frame_parts.get(g)
		if a is not None:a.append(p)
	@staticmethod
	def _scroll_note(g,raw,w,h,H,w2,hv,head,area,area_raw,frame,band,header,fixed,corners,mouse):Kit._scrolled[g]={"w":w,"h":h,"H":H,"w2":w2,"hv":hv,"head":head,"raw":raw,"area":area,"area_raw":area_raw,"frame":frame,"band":band,"header":header,"fixed":fixed,"n":Kit._live_count(raw),"corners":corners,"mouse":mouse};Kit._prune(Kit._scrolled)
	@staticmethod
	def _scroll_undo(g,raw,w,h,corners,mouse,kids,frame,area,band):
		for p in(frame or[])+(band or[]):Kit.dispose(p)
		Kit.dispose(area)
		with Kit.quiet:
			a=Kit._frame_pieces(g,w,h,corners,mouse);Kit._frames[g]={"pieces":a,"corners":corners,"mouse":mouse};Kit.flush()
			for c in kids:c.Parent=raw
	@staticmethod
	def _live_count(raw):
		n=0
		try:
			a=raw.Children
			for i in range(int(a.Count)):
				if not a[i].IsDisposed:n+=1
		except Exception:return-1
		return n
	_same_fn=None
	@staticmethod
	def _same():
		c=Kit._same_fn
		if c is not None:return c
		try:import System;c=System.Object.ReferenceEquals
		except Exception:c=lambda a,b:a is b
		Kit._same_fn=c;return c
	@staticmethod
	def scroll_sweep():
		if not Kit._scrolled:return
		i,j=[],False;H=Kit.screen()[1]
		for g,a in list(Kit._scrolled.items()):
			if not Kit.is_open(g):i.append(g);continue
			b=a["raw"];h=a.get("lim");k=min(H,h)if h else H
			if H>0 and a["H"]!=k:
				try:
					d=Kit._scroll_build(g,a["w"],a["h"],a["head"],k)
					if d is not None:a=Kit._scrolled.get(g)or a;a["lim"]=h;x,y=Kit.clamp(int(g.GetX()),int(g.GetY()),d[0],d[1]);g.SetRect(x,y,d[0],d[1]);Kit.moved_by_code(g)
				except Exception:pass
				continue
			try:e=int(b.Children.Count)
			except Exception:e=-1
			l=time.time()
			if e>=0 and e==a.get("cnt")and 0<=a.get("full_at",0.)-l:continue
			a["cnt"]=e;a["full_at"]=l+Kit.SWEEP_FULL;n=Kit._live_count(b)
			if n<0 or n==a["n"]:continue
			if j or not Kit.flush():a["cnt"],j=None,True;continue
			try:m=Kit._children(b)
			except Exception:a["cnt"]=None;continue
			f=a.get("known")
			if f is None:f=a["known"]=set([a["area_raw"]]+a["header"]+a["fixed"]+[o for o in map(Kit.client_control,a["frame"]+a["band"])if o is not None])
			for c in m:
				try:
					if c.IsDisposed or c in f:continue
				except Exception:continue
				r=Kit._raw_rect(c)
				if r is None:continue
				if r[1]<a["head"]:a["header"].append(c);f.add(c)
				else:
					try:c.Parent=a["area_raw"]
					except Exception:pass
			a["n"]=Kit._live_count(b)
			try:a["cnt"]=int(b.Children.Count)
			except Exception:a["cnt"]=-1
		for g in i:Kit._scrolled.pop(g,None);Kit._frames.pop(g,None)
	@staticmethod
	def attach(a,leader):SNAP.attach(a,leader)
	@staticmethod
	def detach(a):SNAP.detach(a)
	@staticmethod
	def no_snap(g):SNAP.exempt(g)
	@staticmethod
	def anchor_pos(name,w,h):
		W,H=Kit.screen()
		if W<=0 or H<=0 or not name:return None,None
		a="L"if "L"in name else "R"if "R"in name else "C";b="T"if "T"in name else "B"if "B"in name else "C";x=0 if a=="L"else max(0,W-w)if a=="R"else max(0,(W-w)//2);y=0 if b=="T"else max(0,H-h)if b=="B"else max(0,(H-h)//2);return x,y
	@staticmethod
	def anchor_at(x,y,w,h,a=2):
		W,H=Kit.screen()
		if W<=0 or H<=0:return ""
		b="L"if abs(x)<=a else "R"if abs(x+w-W)<=a else "C"if abs(x-(W-w)//2)<=a else None;c="T"if abs(y)<=a else "B"if abs(y+h-H)<=a else "C"if abs(y-(H-h)//2)<=a else None
		if b is None or c is None:return ""
		return(c+b).replace("C","")or "C"
	@staticmethod
	def anchor_targets(w,h):
		W,H=Kit.screen()
		if W<=0 or H<=0:return[]
		return[Kit.anchor_pos(a,w,h)for a in Kit.ANCHORS]
	@staticmethod
	def remap_axis(p,s,S,a):
		p,s,S,a=int(p),int(s or 0),int(S),int(a)
		if S<=0 or a<=0 or S==a:return p
		if p==0:return 0
		if p==S-s:return a-s
		if p==(S-s)//2:return(a-s)//2
		c=p+s/2.
		if c<S/3.:return p
		if c>2*S/3.:return a-(S-p)
		return p+(a-S)//2
	@staticmethod
	def adapt(x,y,w=0,h=0):
		W,H=Kit.screen();a=Kit._pos_screen;x,y=int(x),int(y)
		if a is not None and W>0 and H>0 and(W,H)!=a:x=Kit.remap_axis(x,w,a[0],W);y=Kit.remap_axis(y,h,a[1],H)
		if w and h:x,y=Kit.clamp(x,y,w,h)
		return x,y
	@staticmethod
	def read_screen():
		try:w,h=Kit.get_var(Kit.SCREEN_KEY).split(",");Kit._pos_screen=(int(w),int(h))
		except Exception:Kit._pos_screen=None
	@staticmethod
	def note_screen(wh=None):
		wh=wh or Kit.screen()
		if wh and wh[0]>0 and wh[1]>0 and wh!=Kit._pos_screen:Kit._pos_screen=wh;Kit.put_var(Kit.SCREEN_KEY,"%d,%d"%wh)
	@staticmethod
	def pic_size(graphic):
		a=Kit._sizes.get(graphic)
		if a is None:
			w=h=0
			try:p=G.CreateGumpPic(graphic);w,h=int(p.GetWidth()or 0),int(p.GetHeight()or 0);Kit.dispose(p)
			except Exception:pass
			a=Kit._sizes[graphic]=(w,h)
		return a
	@staticmethod
	def dark():return bool(Kit._dark)
	@staticmethod
	def set_dark(on):a=[(Kit.WINDOW_BG+b,Kit.DARK_HUE)for b in range(9)]+[(Kit.CORNER_ART,Kit.DARK_CORNER_HUE)];Kit._dark=dict(a)if on else{};Kit.SECTION_ALPHA=Kit.DARK_SECTION_ALPHA if on else Kit.LIGHT_SECTION_ALPHA
	@staticmethod
	def look_hue(graphic,hue=0):return hue or Kit._dark.get(graphic,0)
	@staticmethod
	def retint():
		for a in list(Kit._frame_parts.values()):
			for p in a:
				with Kit.quiet:p.Hue=Kit._dark.get(int(p.Graphic),0)
	@staticmethod
	def add_pic(g,graphic,x,y,hue=0,mouse=True):
		try:
			hue=hue or Kit._dark.get(graphic,0);p=G.CreateGumpPic(graphic,x,y,hue)if hue else G.CreateGumpPic(graphic,x,y);p.SetPos(x,y)
			if not mouse:p.SetAcceptMouseInput(False)
			g.Add(p);return p
		except Exception:return
	@staticmethod
	def add_tiled(g,graphic,x,y,w,h,alpha=None,fallback="#101010",hue=0):
		if w<=0 or h<=0:return
		hue=hue or Kit._dark.get(graphic,0)
		try:t=(G.CreateTiledGumpPic(graphic,w,h,hue)if hue else G.CreateTiledGumpPic(graphic,w,h))
		except Exception:t=G.CreateGumpColorBox(alpha if alpha is not None else 1.,fallback)
		t.SetRect(x,y,w,h)
		if alpha is not None:t.SetAlpha(alpha)
		t.SetAcceptMouseInput(False);g.Add(t);return t
	@staticmethod
	def add_box(g,x,y,w,h,alpha=.5,color="#FFFFFF"):
		if w<=0 or h<=0:return
		b=G.CreateGumpColorBox(alpha,color);b.SetRect(x,y,w,h);b.SetAcceptMouseInput(False);g.Add(b);return b
	@staticmethod
	def add_resizepic(g,base,x,y,w,h,mouse=True):
		s=Kit._rp_sizes.get(base)
		if s is None:
			s=[Kit.pic_size(base+j)for j in range(9)]
			if not all(k[0]>0 and k[1]>0 for k in s):return[Kit.add_tiled(g,base+4,x,y,w,h)]
			Kit._rp_sizes[base]=s
		a,t,b,l,i,r,c,e,d=s;f=[Kit.add_tiled(g,base+4,x+l[0],y+t[1],w-l[0]-r[0],h-t[1]-e[1]),Kit.add_tiled(g,base+1,x+a[0],y,w-a[0]-b[0],t[1]),Kit.add_tiled(g,base+7,x+c[0],y+h-e[1],w-c[0]-d[0],e[1]),Kit.add_tiled(g,base+3,x,y+a[1],l[0],h-a[1]-c[1]),Kit.add_tiled(g,base+5,x+w-r[0],y+b[1],r[0],h-b[1]-d[1]),Kit.add_pic(g,base+0,x,y,mouse=mouse),Kit.add_pic(g,base+2,x+w-b[0],y,mouse=mouse),Kit.add_pic(g,base+6,x,y+h-c[1],mouse=mouse),Kit.add_pic(g,base+8,x+w-d[0],y+h-d[1],mouse=mouse)];return[m for m in f if m is not None]
	@staticmethod
	def gold_box(g,x,y,w,h,t=GOLD_T):
		a=[Kit.add_tiled(g,Kit.SECTION_TILE,x+t,y+t,w-2*t,h-2*t)]
		for b,c,d,e,f in((Kit.GOLD_H,x,y,w,t),(Kit.GOLD_H,x,y+h-t,w,t),(Kit.GOLD_V,x,y,t,h),(Kit.GOLD_V,x+w-t,y,t,h)):a.append(Kit.add_tiled(g,b,c,d,e,f))
		return[i for i in a if i is not None]
	@staticmethod
	def _frame_pieces(g,w,h,corners=True,mouse=True):
		a=Kit.add_resizepic(g,Kit.WINDOW_BG,0,0,w,h,mouse)
		if corners and Kit.CORNER_ART:
			b,c=Kit.pic_size(Kit.CORNER_ART)
			if b and c:
				for d,e in((0,0),(w-b,0),(0,h-c),(w-b,h-c)):
					p=Kit.add_pic(g,Kit.CORNER_ART,d,e,mouse=mouse)
					if p is not None:a.append(p)
		if type(g)is not PageCanvas:
			try:Kit._prune(Kit._frame_parts);Kit._frame_parts[g]=[f for f in a if f is not None]
			except TypeError:pass
		return a
	_frame_want={}
	@staticmethod
	def frame_show(g,on):
		Kit._prune(Kit._frame_want,32);Kit._frame_want[g]=bool(on)
		if g in Seam.bare or g in Seam.recs:return
		for p in Kit._frame_parts.get(g)or():Kit.set(p,"IsVisible",bool(on))
	@staticmethod
	def frame_fit(g,w,h):
		a=Kit._frames.get(g);s=Kit._rp_sizes.get(Kit.WINDOW_BG)
		if a is None or s is None or g in Kit._scrolled:return False
		b,t,c,l,n,r,d,f,e=s;i,j=Kit.pic_size(Kit.CORNER_ART)if a["corners"]and Kit.CORNER_ART else(0,0);k=[(l[0],t[1],w-l[0]-r[0],h-t[1]-f[1]),(b[0],0,w-b[0]-c[0],t[1]),(d[0],h-f[1],w-d[0]-e[0],f[1]),(0,b[1],l[0],h-b[1]-d[1]),(w-r[0],c[1],r[0],h-c[1]-e[1]),(0,0),(w-c[0],0),(0,h-d[1]),(w-e[0],h-e[1])]
		if i and j:k+=[(0,0),(w-i,0),(0,h-j),(w-i,h-j)]
		if len(a["pieces"])!=len(k):return False
		for p,m in zip(a["pieces"],k):
			if len(m)==4:p.SetRect(*m)
			else:p.SetPos(*m)
		return True
	@staticmethod
	def add_window_frame(g,w,h,corners=True,mouse=True):
		a=Kit._frame_pieces(g,w,h,corners,mouse)
		if type(g)is not PageCanvas:
			Kit._prune(Kit._frames,32)
			if len(Kit._frames)>48:Kit._frames.clear()
			Kit._frames[g]={"pieces":a,"corners":corners,"mouse":mouse}
	@staticmethod
	def add_section(g,x,y,w,h,title=None,alpha=None):
		if type(g)is PageCanvas:g.sections.append((x,y,w,h))
		t=Kit.add_tiled(g,Kit.SECTION_TILE,x,y,w,h,Kit.SECTION_ALPHA if alpha is None else alpha)
		if title:Kit.add_label(g,title,x+8,y+6,Kit.HUE_TITLE)
		return t
	@staticmethod
	def add_label(g,text,x,y,hue=None):a=G.CreateGumpLabel(text,Kit.HUE_TEXT if hue is None else hue);a.SetPos(x,y);g.Add(a);return a
	@staticmethod
	def add_check(g,text,x,y,checked=False,tooltip=None):a=G.CreateGumpCheckbox(text,Kit.HUE_TEXT,checked);a.SetPos(x,y);Kit.with_tip(a,tooltip);g.Add(a);return a
	@staticmethod
	def add_textbox(g,text,x,y,w=60,numbers=True,font=16):
		Kit.add_tiled(g,Kit.FIELD_TILE,x-2,y-1,w+4,24);a=G.CreateGumpTextBox(text,w,22,False,font);a.SetPos(x,y)
		if numbers:a.NumbersOnly=True
		g.Add(a);return a
	@staticmethod
	def add_slider(g,x,y,w,lo,hi,value):s=G.CreateSlider(w,lo,hi,int(value),x,y,True);g.Add(s);return s
	clicks_seen=False
	@staticmethod
	def on_click(ctrl,fn):
		a=HOST.click_key()
		def b(*c):
			Kit.clicks_seen=True;b=Client.second_click_swallowed()
			try:fn()
			finally:
				try:
					if b:fn()
				finally:HOST.poke(a)
		G.AddControlOnClick(ctrl,b)
	_dbl={};pending=[];_fired={}
	@staticmethod
	def _prune(d,cap=64):
		if len(d)>cap:
			for k in[a for a in d if not Kit.is_open(a)]:d.pop(k,None)
	@staticmethod
	def _forget_old(d,now,age=5.):
		if len(d)>64:
			for k in[b for b,a in d.items()if now-(a[0]if type(a)is tuple else a)>age]:d.pop(k,None)
	TWICE=.15
	@staticmethod
	def once(fn,key,gap=.6):
		def a():
			a=time.time()
			if a-Kit._fired.get(key,0.)<gap:return
			Kit._fired[key]=a;Kit._forget_old(Kit._fired,a);fn()
		return a
	@staticmethod
	def hook_mouse(g,fn,queue=True,event="MouseDoubleClick",button="Left"):
		try:
			import clr;import System;c=Kit.client_control(g);d=c.GetType();f=(str(d.FullName),event);b=Kit._dbl_events.get(f)
			if b is None:
				h=Client.flags();t,a=d,None
				while t is not None and a is None:a=t.GetEvent(event,h);t=t.BaseType
				b=(a,clr.GetPythonType(a.EventHandlerType),a.GetAddMethod(True))
				if len(Kit._dbl_events)>64:Kit._dbl_events.clear()
				Kit._dbl_events[f]=b
			a,i,j=b
			def k(sender,e):
				try:
					if str(e.Button)==button:
						if queue:Kit.pending.append(fn)
						else:fn()
						e.Result=True;HOST.poke()
				except Exception:pass
			j.Invoke(c,System.Array[object]([i(k)]));return True
		except Exception:return False
	hook_double=hook_mouse;_dbl_events={}
	@staticmethod
	def on_moved(g,fn):SNAP.on_moved(g,fn)
	@staticmethod
	def moved_by_code(g):SNAP.moved_by_code(g)
	@staticmethod
	def title_catcher(g,x,y,w,h,fn,key=None):
		key=key or id(g);a=Kit.once(fn,key)
		def fn():
			if Kit.just_dragged(g):Kit._dbl.pop(key,None);return
			a()
		def b():
			b=time.time()
			if Kit.just_dragged(g):Kit._dbl.pop(key,None);return
			c=(g.GetX(),g.GetY());a=Kit._dbl.get(key)
			if a and b-a[0]<=.7 and abs(c[0]-a[1][0])<=3 and abs(c[1]-a[1][1])<=3:Kit._dbl.pop(key,None);fn()
			else:Kit._dbl[key]=(b,c);Kit._forget_old(Kit._dbl,b)
		c=Kit.catcher(g,x,y,w,h,b,Kit.DOUBLE_TIP,movable=True)
		if Client.mouse is None:Kit.hook_double(c,fn)
		return c
	DRAG_QUIET=.4
	@staticmethod
	def just_dragged(g):
		try:
			if g in SNAP.drag or g in SNAP.dragged:return True
			t=SNAP.drag_end.get(g);return t is not None and time.time()-t<Kit.DRAG_QUIET
		except Exception:return False
	@staticmethod
	def catcher(g,x,y,w,h,fn,tooltip=None,movable=False):
		c=G.CreateGumpColorBox(.01,"#000000");c.SetRect(x,y,w,h);Kit.on_click(c,fn);Kit.with_tip(c,tooltip)
		if movable:c.CanMove=True
		g.Add(c);return c
	@staticmethod
	def art_button(g,store,key,art,x,y,label=None,tooltip=None,hue=None,on_click=None):
		h,c=store;b=G.CreateGumpButton("",Kit.HUE_TEXT,art[0],art[1],art[2]);b.SetPos(x,y);g.Add(b);h[key]=b;c[key]=False;d=Binds.note(store,key,on_click,b,tooltip)
		def i(*a):
			c[key]=True
			if on_click is not None:on_click()
		e=Binds.wrap(d,i);Kit.on_click(b,e);f=Binds.saved.get(d)
		if f:tooltip=(tooltip+" "if tooltip else "")+"(hotkey: %s)"%f
		Kit.with_tip(b,tooltip)
		if label:j,k=Kit.pic_size(art[0]);a=Kit.add_label(g,label,x+(j or 30)+5,y+max(((k or 22)-16)//2,0),hue);a.SetAcceptMouseInput(True);Kit.on_click(a,e);return a
		return b
	@staticmethod
	def closed(win,key="g"):
		if not Kit.was_clicked(win["store"],"close"):return False
		Kit.dispose(win[key]);return True
	@staticmethod
	def weight_bar(g,c,b,by,bw,centre=0):
		e,h=Kit.pic_size(Kit.LINE_RED);a=max(4,min(11,Kit.pic_size(Kit.LINE_BLUE)[1]or h or 9))
		if centre:by+=max(0,(centre-a)//2)
		if e>0:Kit.add_tiled(g,Kit.LINE_RED,b,by,bw,a,hue=946)
		else:Kit.add_tiled(g,Kit.SECTION_TILE,b,by,bw,a,1.)
		d={}
		for i,j,k in(("ok",Kit.LINE_POISON,0),("warn",Kit.LINE_BLUE,53),("red",Kit.LINE_RED,0)):
			f=Kit.add_tiled(g,j,b,by,1,a,hue=k)
			if f is not None:f.IsVisible=False;d[i]=f
		c["wfills"]=d;c["wbar_w"]=bw
	@staticmethod
	def weight_level(a,bw):
		if a<0:return None,0
		b="red"if a>=.95 else "warn"if a>=.85 else "ok";return b,max(1,min(bw,int(round(bw*min(1.,a)))))
	@staticmethod
	def weight_show(fills,kind,width):
		for k,f in fills.items():
			try:
				if k==kind:Kit.ui_w(f,width)
				f.IsVisible=k==kind
			except Exception:pass
	_hooks={}
	@staticmethod
	def hook_once(a,key,*d):
		if a[key]:return
		a[key]=True;e=HOST.owner_key()
		for b,c in d:
			try:getattr(API.Events,b)(c)
			except Exception:continue
			Kit._hooks.setdefault(e,[]).append((b,c,a,key))
	@staticmethod
	def unhook(owner):
		a=Kit._hooks.pop(owner,None)
		if not a:return
		def b():
			for c in a:
				b,d,e,f=c
				try:getattr(API.Events,"Unregister"+(b if b.startswith("On")else "On"+b))(d)
				except Exception:Kit._hooks.setdefault(owner,[]).append(c);continue
				e[f]=False
		with Kit.quiet:Kit.on_client(b)
	@staticmethod
	def was_clicked(store,key):
		b=store[1];a=b.get(key,False)
		if a:b[key]=False
		if Kit.clicks_seen:return a
		c=store[0].get(key)
		if c is not None:
			try:a=c.HasBeenClicked()or a
			except Exception:pass
		return a
	_texts={};_texts_cap=3000;_texts_sweep=False;_texts_list=None;_texts_at=0;TEXTS_SLICE=400
	@staticmethod
	def set_text(lbl,text,hue=None):
		try:e=Kit._texts.get(lbl)
		except TypeError:e=[None,None]
		if e is None:
			e=Kit._texts[lbl]=[None,None]
			if len(Kit._texts)>Kit._texts_cap:Kit._prune_texts()
		a=e[0]!=text
		if a:
			e[0]=text
			try:lbl.Text=text
			except Exception:
				try:lbl.SetText(text)
				except Exception:pass
		if hue is not None and e[1]!=hue:
			e[1]=hue
			try:lbl.Hue=hue
			except Exception:pass
		return a
	@staticmethod
	def _prune_texts():
		if not Client.on_client_thread():Kit._texts_cap=len(Kit._texts)+500;Kit._texts_sweep=True;return
		a=Kit._texts_list
		if a is None:a=Kit._texts_list=list(Kit._texts);Kit._texts_at=0;Kit._texts_cap=len(Kit._texts)+500
		Kit._texts_sweep=True;i=Kit._texts_at;d=min(len(a),i+Kit.TEXTS_SLICE);c=Kit._texts
		while i<d:
			b=a[i];i+=1
			try:
				if b.IsDisposed:c.pop(b,None)
			except Exception:c.pop(b,None)
		Kit._texts_at=i
		if i>=len(a):Kit._texts_list=None;Kit._texts_sweep=False;Kit._texts_cap=max(3000,2*len(Kit._texts))
	_widths={};_ctl_prop={};_rp_sizes={};SWEEP_FULL=5.;WIDTHS_MAX=4000
	@staticmethod
	def text_w(text):
		a=Kit._widths.get(text)
		if a is None:
			a=0
			try:l=G.CreateGumpLabel(text,Kit.HUE_TEXT);a=int(l.GetWidth()or 0);Kit.dispose(l)
			except Exception:pass
			a=a or 8*len(text)
			if len(Kit._widths)>=Kit.WIDTHS_MAX:
				b=Kit._widths
				for k in[c for c in b if len(c)>12]:del b[k]
				if len(b)>=Kit.WIDTHS_MAX//2:b.clear()
			Kit._widths[text]=a
		return a
	_wraps={}
	@staticmethod
	def wrap(text,width):
		b=(text,width);a=Kit._wraps.get(b)
		if a is None:
			if len(Kit._wraps)>600:Kit._wraps.clear()
			a=Kit._wraps[b]=tuple(Kit._wrap_raw(text,width))
		return list(a)
	@staticmethod
	def _wrap_raw(text,width):
		a=[];d=text.split()
		if d and Kit._px["ok"]is None:Kit.text_px("")
		if Kit._px["ok"]:
			g,h=Kit._px["pad"],Kit._px_ch;c=h.get(" ")
			if c is None:c=Kit._ch_w(" ")
			e=0
			for b in d:
				f=Kit.text_px(b)-g
				if a and e+c+f<=width:a[-1]+=" "+b;e+=c+f
				else:a.append(b);e=g+f
			return a or[""]
		for b in d:
			if a and Kit.text_w(a[-1]+" "+b)<=width:a[-1]+=" "+b
			else:a.append(b)
		return a or[""]
	_px={"ok":None,"pad":0};_px_ch={};PX_REF="Total 120.0 / 700.0 (+5.2) Session ~1h 05m: Magery, Str"
	@staticmethod
	def _ch_w(ch):w=Kit.text_w("x"+ch+"x")-Kit.text_w("xx");Kit._px_ch[ch]=w;return w
	@staticmethod
	def text_px(text):
		a=Kit._px
		if a["ok"]is None:
			try:a["pad"]=2*Kit.text_w("x")-Kit.text_w("xx");b=Kit.PX_REF;a["ok"]=Kit.text_w(b)==a["pad"]+sum(Kit._ch_w(e)for e in b)
			except Exception:a["ok"]=False
		if not a["ok"]:return Kit.text_w(text)
		w,d=a["pad"],Kit._px_ch
		for c in text:x=d.get(c);w+=Kit._ch_w(c)if x is None else x
		return w
	@staticmethod
	def fit(text,width,tail=".."):
		text=str(text or "")
		if len(text)*9<=width or Kit.text_px(text)<=width:return text
		if Kit._px["ok"]:
			w,d=Kit.text_px(text+tail),Kit._px_ch
			while text and w>width:w-=d.get(text[-1],0);text=text[:-1]
			return text.rstrip()+tail
		a,b=1,len(text)-1
		while a<b:
			c=(a+b+1)//2
			if Kit.text_w(text[:c]+tail)<=width:a=c
			else:b=c-1
		return text[:a].rstrip()+tail
	GUMP_CMDS=("page","button","buttontileart","checkertrans","croppedtext","gumppic","gumppictiled","gumppichued","gumppicphued","htmlgump","xmfhtmlgump","xmfhtmlgumpcolor","xmfhtmltok","noclose","nodispose","nomove","noresize","group","endgroup","radio","checkbox","resizepic","text","textentry","textentrylimited","tilepic","tilepichue","tooltip","itemproperty","mastergump","picinpic","picinpichued","picinpicphued","togglelimitgumpscale","maparea");_gump_cmds=frozenset(GUMP_CMDS);_cliloc_cache={}
	@staticmethod
	def gump_is_int(a):
		a=str(a)
		if a.startswith("-"):a=a[1:]
		return len(a)>0 and a.isdigit()
	@staticmethod
	def _gump_arg_ok(a):
		if Kit.gump_is_int(a):return True
		if a.startswith("#"):return Kit.gump_is_int(a[1:])
		if "="in a:return a.split("=",1)[0].isalnum()
		return a.startswith("@")or a.endswith("@")
	@staticmethod
	def gump_is_cmd(line):
		b=str(line).strip().split()
		if not b or b[0].lower()not in Kit._gump_cmds:return False
		c=False
		for a in b[1:]:
			if c:
				if a.endswith("@"):c=False
				continue
			if a.startswith("@")and not(len(a)>1 and a.endswith("@")):c=True;continue
			if not Kit._gump_arg_ok(a):return False
		return True
	@staticmethod
	def _gump_split_merged(a):
		a=str(a);d=a.lower();n=len(a)
		for p in range(n):
			for c in Kit.GUMP_CMDS:
				b=p+len(c)
				if d[p:b]!=c:continue
				if b<n and a[b]!=" ":continue
				if Kit.gump_is_cmd(a[p:]):return a[:p],a[p:]
		return a,None
	@staticmethod
	def gump_parse(raw):
		raw=str(raw or "").replace("\r","").replace("\x00","");a=raw.split("\n")
		while a and a[-1].strip()=="":a.pop()
		j=len(a)
		while j>0 and Kit.gump_is_cmd(a[j-1]):j-=1
		if j==0:b,c=[],a
		else:
			e,d=Kit._gump_split_merged(a[j-1])
			if d is None:b,c=a[:j]+[""],a[j:]
			else:b,c=a[:j-1]+[e],[d]+a[j:]
		return b,[f.split()for f in c]
	_HTML_RE=re.compile(r"<[^>]*>")
	@staticmethod
	def strip_html(s):return Kit._HTML_RE.sub("",str(s or "")).replace("&nbsp;"," ").strip()
	@staticmethod
	def cliloc_text(n,clilocs=None):
		if clilocs:
			t=clilocs.get(n)
			if t is not None:return t
		t=Kit._cliloc_cache.get(n)
		if t is None:
			t=str(safe(lambda:API.GetClilocString(n),"")or "").strip()or("#%d"%n)
			if len(Kit._cliloc_cache)>500:Kit._cliloc_cache.clear()
			Kit._cliloc_cache[n]=t
		return t
	_CELLS={"htmlgump":(8,5,None,6,1),"xmfhtmlgump":(8,None,5,6,1),"xmfhtmlgumpcolor":(8,None,5,6,1),"xmfhtmltok":(9,None,8,5,1),"text":(5,4,None,None,0),"croppedtext":(7,6,None,None,1)}
	@staticmethod
	def gump_cells(raw,clilocs=None):
		i,j=Kit.gump_parse(raw);b,c=[],[]
		for t in j:
			try:
				k=t[0].lower()
				if k=="button"and len(t)>=8:
					if int(t[5])==1:c.append((int(t[1]),int(t[2]),int(t[7])))
					continue
				r=Kit._CELLS.get(k)
				if r is None or len(t)<r[0]:continue
				d,a,e,f=r[1:];g=""if d is None else i[int(t[d])];h=0 if a is None else int(str(t[a]).replace("#",""));b.append({"x":int(t[1]),"y":int(t[2]),"w":int(t[3])if f else 0,"h":int(t[4])if f else 0,"raw":g,"text":Kit.strip_html(g)if a is None else Kit.cliloc_text(h,clilocs),"cliloc":h,"bg":e is not None and int(t[e])!=0})
			except(ValueError,IndexError):continue
		return b,c
	@staticmethod
	def dispose(ctrl):
		if ctrl is not None:
			try:ctrl.Dispose()
			except Exception:pass
	@staticmethod
	def is_open(g):
		if g is None:return False
		try:return not g.IsDisposed
		except Exception:return False
	_vars={}
	@staticmethod
	def get_var(key,default=""):
		v=Kit._vars.get(key)
		if v is None:
			try:v=str(API.GetPersistentVar(key,"",API.PersistentVar.Char)or "")
			except Exception:return str(default)
			if len(Kit._vars)>3000:Kit._vars.clear()
			Kit._vars[key]=v
		return v or str(default)
	@staticmethod
	def put_var(key,value,a=False):
		v=str(value)
		if Kit._vars.get(key)==v:return
		Kit._vars.pop(key,None)
		if a:API.SavePersistentVar(key,value,API.PersistentVar.Char)
		else:
			with Kit.quiet:API.SavePersistentVar(key,value,API.PersistentVar.Char);Kit._vars[key]=v
			return
		Kit._vars[key]=v
	_data_dir=[None];DATA_MOVE=re.compile(r"^(_ultima_tracker_data\.txt|_lookout_feed\.txt|_unified_bag_\d+\.cfg"r"|_storage_index_[^\\/]+?\.txt|_swing_timer_\d+\.txt"r"|Skills_[0-9A-F]{8}\.txt|SkillBags_[0-9A-F]{8}_rule\d+\.txt"r"|Meters_[0-9A-F]{8}\.txt|Grimoire_saved\.txt"r"|Grimoire_runebook_dump\.txt)"r"(\.\d+)?(\.tmp)?$");DATA_MOVE_ROOT=re.compile(r"^(Grimoire_saved\.txt|Grimoire_runebook_dump\.txt)$")
	@staticmethod
	def script_dir():
		a=str(API.ScriptPath or "").rstrip("/\\")
		if a and os.path.isfile(a):a=os.path.dirname(a)
		if a.endswith("Modules"):a=os.path.dirname(a)
		return a or safe(Kit._legion_root,"")
	@staticmethod
	def _legion_root():import System;return os.path.join(str(System.AppDomain.CurrentDomain.BaseDirectory),"LegionScripts")
	@staticmethod
	def data_dir():
		d=Kit._data_dir[0]
		if d is None:a=Kit.script_dir();d=Kit._data_dir[0]=os.path.join(a,SETTINGS_DIR)if a else SETTINGS_DIR
		return d
	@staticmethod
	def data_path(name):return os.path.join(Kit.data_dir(),name)
	@staticmethod
	def write_safe(path,text,g="utf-8",tail=None):
		try:import threading;a="%s.%d.%d.tmp"%(path,os.getpid(),threading.get_ident())
		except Exception:a="%s.%d.tmp"%(path,id(text))
		import io
		try:
			if isinstance(text,bytes):
				with io.open(a,"wb")as f:f.write(text)
			else:
				with io.open(a,"w",encoding=g,newline="")as f:f.write(text)
			d=tail()if tail is not None else None
			if d:
				with io.open(a,"ab")as f:f.write(d)
		except Exception:safe(lambda:os.remove(a));raise
		e=False
		for h in range(3):
			try:os.replace(a,path);e=True;break
			except Exception:pass
		if not e:
			b=a+".bak";c=os.path.exists(path)
			try:
				if c:os.rename(path,b)
				os.rename(a,path)
			except Exception:
				if c and os.path.exists(b):
					if os.path.exists(path):safe(lambda:os.remove(b))
					else:safe(lambda:os.rename(b,path))
				safe(lambda:os.remove(a));raise
			if c:safe(lambda:os.remove(b))
		if text:Kit._seen.add(os.path.normcase(os.path.abspath(path)))
		return True
	_seen=set();_gone={};MISS_WAIT=5.
	@staticmethod
	def read_merge(path):
		a=os.path.normcase(os.path.abspath(path))
		if not os.path.exists(path):
			if a not in Kit._seen:return ""
			b=time.time();t=Kit._gone.setdefault(a,b)
			if b-t<Kit.MISS_WAIT:return
			Kit._seen.discard(a);Kit._gone.pop(a,None);return ""
		Kit._gone.pop(a,None);c=Kit.read_safe(path)
		if c:Kit._seen.add(a)
		return c
	@staticmethod
	def read_safe(path,missing=""):
		try:
			if not os.path.exists(path):return missing
			import io
			with io.open(path,"r",encoding="utf-8-sig")as f:return f.read()
		except Exception:return
	@staticmethod
	def merge_text(text,entries,d,c="\n"):
		a,b=[],{}
		for e in(text or "").split(c):
			e=e.rstrip("\r")
			if not e.strip():continue
			k=d(e)
			if k is not None and k in b:a[b[k]]=e;continue
			if k is not None:b[k]=len(a)
			a.append(e)
		for k,e in entries.items():
			if k in b:a[b[k]]=e
			elif e is not None:b[k]=len(a);a.append(e)
		a=[f for f in a if f is not None];return c.join(a),a
	@staticmethod
	def merge_save(path,entries,d,a="\n"):
		b=Kit.read_merge(path)
		if b is None:return
		e,c=Kit.merge_text(b,entries,d,a);Kit.write_safe(path,e+a if c else "");return c
	@staticmethod
	def data_setup():
		a,d=Kit.script_dir(),Kit.data_dir()
		try:
			if not os.path.isdir(d):os.makedirs(d)
		except Exception as k:Kit._data_dir[0]=a or "";Kit.say("couldn't make the %s folder (%s); saving beside the script."%(SETTINGS_DIR,k),Kit.HUE_BAD);return
		e,f=0,0;h=[(a,Kit.DATA_MOVE)]if a else[];g=safe(Kit._legion_root,"");i=lambda p:os.path.normcase(os.path.abspath(p))if p else ""
		if g and i(g)!=i(a):h.append((g,Kit.DATA_MOVE_ROOT))
		for j,l in h:
			try:m=os.listdir(j)
			except Exception:continue
			for n in m:
				if not l.match(n):continue
				b,c=os.path.join(j,n),os.path.join(d,n)
				try:
					if not os.path.isfile(b)or os.path.exists(c):continue
					os.rename(b,c);e+=1
				except Exception:f+=1
		if a:
			b,c=os.path.join(a,PROFILE_DIR),os.path.join(d,PROFILE_DIR)
			try:
				if os.path.isdir(b)and not os.path.exists(c):os.rename(b,c);e+=1
			except Exception:f+=1
		if e:Kit.say("moved %s into the %s folder."%(Kit.count(e,"saved file"),SETTINGS_DIR),Kit.HUE_INFO)
		if f:Kit.say("couldn't move %s into the %s folder (open in another client?)."%(Kit.count(f,"saved file"),SETTINGS_DIR),Kit.HUE_BAD)
	@staticmethod
	def load_pos(key,default=(200,200),size=None):
		try:x,y=Kit.get_var(key,"%d,%d"%default).split(",");x,y=int(x),int(y)
		except Exception:x,y=default
		w,h=size if size else(0,0);return Kit.adapt(x,y,w,h)
	@staticmethod
	def load_min(key):return Kit.get_var(key,"0")=="1"
	@staticmethod
	def save_min(key,minimized):Kit.put_var(key,"1"if minimized else "0")
	@staticmethod
	def save_pos(key,g):
		if Kit.is_open(g)and g not in LAYOUT.held:Kit.put_var(key,"%d,%d"%(g.GetX(),g.GetY()))
	@staticmethod
	def queuer(st):
		def a(action,dup=False,front=False,cap=None,key=None):
			q=st["queue"]
			if not dup and action in q or cap is not None and len(q)>=cap:return False
			if front:q.insert(0,action)
			else:q.append(action)
			if key is not None and(HOST.draining or not HOST.in_hop):HOST.poke(key)
			return True
		def b(action,dup=False):
			b=HOST.click_key()
			def c(*c):a(action,dup,key=b)
			return c
		b.add=a;return b
	@staticmethod
	def disposer(key,st,win):
		def a(g):
			def a(*a):
				if win["g"]is g and not st["shutting"]:win["g"]=None;HOST.disable(key)
			return a
		return a
	TITLE_GAP=6;CAP_GAP=10;BARE_GAP=4
	@staticmethod
	def caption_tip(a,tip):
		tip=str(tip or "")
		if not tip:return a
		return "%s: %s%s"%(a,tip[:1].lower(),tip[1:])
	@staticmethod
	def title_plan(w,title,buttons,after=None):
		M=Kit.MARGIN;c=w-M-84-Kit.DOCK_DX;e=M+30;i=[35+Kit.text_w(k[0])for k in buttons]
		def f(a):
			b,x=[],c
			for d in i:x-=d if a else 30;b.append(x);x-=Kit.CAP_GAP if a else Kit.BARE_GAP
			return b
		g=Kit.text_w(title.upper());j=(8+Kit.text_w(after))if after else 0
		for h in(True,False):
			a=f(h);b=a[-1]if a else c
			if e+g+j+Kit.TITLE_GAP<=b:return h,bool(after),title.upper(),a,b
		a=f(False)
		while a and a[-1]<M+4:a.pop()
		b=a[-1]if a else c;d=b-Kit.TITLE_GAP-e;T=title.upper()if g<=d else ""if d<Kit.text_w("W..")else Kit.fit(title.upper(),d);return False,False,T,a,b
	@staticmethod
	def title_bar(g,store,w,title,key,h,p,i=None,close_tip=None,extra=None,after=None):
		M=Kit.MARGIN;Kit.add_section(g,M,M,w-2*M,30);c=[]
		if i is not None:c.append(("Settings","settings",Kit.ART_PAGE,Kit.SETTINGS_TIP%title,i))
		for b in(extra or()):c.append((b[2],b[0],b[1],b[3],b[4]))
		d=Kit.zone_up(key);j=(84+Kit.DOCK_DX-10)if d else 0;k,q,e,f,l=Kit.title_plan(w+j,title,c,after);Kit.add_label(g,e,M+30,M+7,Kit.HUE_TITLE)
		if q:Kit.add_label(g,after,M+30+Kit.text_w(e)+8,M+7,Kit.HUE_INFO)
		if d:m=Kit.catcher(g,M,M,max(20,l-M-Kit.TITLE_GAP),30,lambda*a:None,None,movable=True)
		else:m=Kit.title_catcher(g,M,M,max(20,l-M-Kit.TITLE_GAP),30,h,key=key)
		if e!=title.upper():Kit.with_tip(m,title if d else "%s. %s"%(title,Kit.DOUBLE_TIP))
		for(n,r,s,o,t),x in zip(c,f):Kit.art_button(g,store,r,s,x,M+4,n if k else None,o if k else Kit.caption_tip(n,o),on_click=t)
		if not d:Kit.dock_button(g,store,w-M-74,M+7,on_click=p);Kit.art_button(g,store,"min",Kit.ART_MIN,w-M-74,M+7,None,Kit.MIN_TIP,on_click=h);Kit.art_button(g,store,"close",Kit.ART_CLOSE,w-M-54,M+4,None,close_tip or Kit.CLOSE_TIP%title)
		return f[-1]if f else w-M-84-Kit.DOCK_DX+j
	@staticmethod
	def zone_up(key):return bool(HOST.layout_holds(key))
	_mouse=[None]
	@staticmethod
	def mouse_pos():
		f=Kit._mouse[0]
		if f is None:
			Kit._mouse[0]=False;t=Client._type("ClassicUO.Input.Mouse")
			if t is not None:
				try:m=Client._member(t,"Position");p=m[0]();int(p.X);Kit._mouse[0]=m[0]
				except Exception:pass
			f=Kit._mouse[0]
		if not f:return
		try:p=f();return int(p.X),int(p.Y)
		except Exception:return
	@staticmethod
	def mini_bar(g,store,w,h,title,key,a,text="",hue=None,close_tip=None):Kit.add_window_frame(g,w,h,corners=False);Kit.add_section(g,8,8,w-16,h-16);b=Kit.add_label(g,text,18,15,Kit.HUE_INFO if hue is None else hue);Kit.title_catcher(g,8,8,w-70,h-16,a,key=str(key)+":mini");Kit.art_button(g,store,"restore",Kit.ART_RESTORE,w-60,15,None,Kit.RESTORE_TIP,on_click=a);Kit.art_button(g,store,"close",Kit.ART_CLOSE,w-44,12,None,close_tip or Kit.CLOSE_TIP%title);return b
	@staticmethod
	def dock_button(g,store,a,b,on_click=None,key="tobar"):return Kit.art_button(g,store,key,Kit.ART_DOCK,a-Kit.DOCK_DX,b+Kit.DOCK_DY,None,Kit.DOCK_TIP,on_click=on_click)
	@staticmethod
	def dock_hooks(title,icon,st,win,redraw,fit=None):
		def c():
			if win["g"]is None or st["shutting"]:return
			return "docked"if st["docked"]else("minimized"if st["minimized"]else "open")
		def a(docked,minimized):
			def f():st["docked"],st["minimized"]=docked,minimized;redraw()
			return f
		def d():st["docked"]=False;redraw()
		b={"title":title,"icon":icon,"state":c,"show":a(False,False),"dock":a(True,True),"undock":d,"minimize":a(False,True),"gump":lambda:win["g"],"redraw":redraw}
		if fit is not None:b["fit"]=fit
		return b
	@staticmethod
	def flush():
		a=Client._find_mtq()
		if a is None or not Client.on_client_thread():return False
		try:
			n=0
			while int(a.Count)>0 and n<500:a.ProcessQueue();n+=1
			return int(a.Count)==0
		except Exception:return False
	@staticmethod
	def client_control(c):
		try:
			b=type(c);d=Kit._ctl_prop;a=d.get(b,False)
			if a is False:
				a=None;import clr;e=Client.flags();t=clr.GetClrType(b)
				while t is not None:
					a=t.GetProperty("Control",e)
					if a is not None:break
					t=t.BaseType
				d[b]=a
			if a is not None:return a.GetValue(c,None)
		except Exception:pass
		return
	@staticmethod
	def _scroll_skip(g):
		a=Kit._scrolled.get(g)
		if a is None:return[],None
		b=a.get("skip_raw")
		if b is None:b=[f for f in map(Kit.client_control,a["frame"]+a["band"])if f is not None];a["skip_raw"]=b
		c=list(b);d=a["area_raw"]
		try:
			e=d.Children
			if int(e.Count)>0:c.append(e[0])
		except Exception:pass
		return c,d
	@staticmethod
	def scale_window(g,scale):
		if abs(scale-1.)<.001:return True
		a=Kit.client_control(g)
		if a is None or not Kit.flush():return False
		b,d=Kit._scroll_skip(g);e=Kit._same()
		def f(c):
			if b and any(e(c,j)for j in b):return
			if d is None or not e(c,d):
				if str(c.GetType().Name)=="GumpPicTiled":Kit.set(c,"ScaleTiledTexture",True)
				c.ApplyScale(scale,True,True,False)
			a=c.Children
			for i in range(a.Count):f(a[i])
		try:
			h=a.Children
			for i in range(h.Count):f(h[i])
			return True
		except Exception:return False
	@staticmethod
	def ui_pos(c,x,y):
		if c is None:return
		if not(Fill.recs and Fill.change(c,x=x,y=y)):c.SetPos(int(x),int(y))
	@staticmethod
	def ui_rect(c,x,y,w,h):
		if c is None:return
		if not(Fill.recs and Fill.change(c,x,y,w,h)):c.SetRect(int(x),int(y),int(w),int(h))
	@staticmethod
	def ui_w(c,w):
		if c is None:return
		if not(Fill.recs and Fill.change(c,w=w)):c.SetWidth(int(w))
	@staticmethod
	def ui_size(c,w,h):
		if c is None:return
		if not(Fill.recs and Fill.change(c,w=w,h=h)):c.SetWidth(int(w));c.SetHeight(int(h))
	@staticmethod
	def ui_y(c):a=Fill.own(c)if Fill.recs else None;return a[1]if a is not None else c.GetY()
	SPELL_WORDS,MAGERY,CAST_DELAY_OTHER={},[],{}
	for _r in("uus jux,Clumsy,BM NS,;in mani ylem,Create Food,GA GI MR,;rel wis,Feeblemind,GI NS,;in mani,Heal,GA GI SS,heal;in por ylem,Magic Arrow,SA,;in lor,Night Sight,SS SA,;flam sanct,Reactive Armor,GA SS SA,;des mani,Weaken,GA NS,;ex uus,Agility,BM MR,;uus wis,Cunning,MR NS,;an nox,Cure,GA GI,cure;an mani,Harm,NS SS,;in jux,Magic Trap,GA SS SA,;an jux,Magic Untrap,BM SA,;uus sanct,Protection,GA GI SA,;uus mani,Strength,MR NS,;rel sanct,Bless,GA MR,;vas flam,Fireball,BP,;an por,Magic Lock,BM GA SA,;in nox,Poison,NS,;ort por ylem,Telekinesis,BM MR,;rel por,Teleport,BM MR,;ex por,Unlock,BM SA,;in sanct ylem,Wall of Stone,BM GA,;vas an nox,Arch Cure,GA GI MR,cure+;vas uus sanct,Arch Protection,GA GI MR SA,;des sanct,Curse,GA NS SA,;in flam grav,Fire Field,BP SS SA,;in vas mani,Greater Heal,GA GI MR SS,heal;por ort grav,Lightning,MR SA,;ort rel,Mana Drain,BP MR SS,;kal ort por,Recall,BP BM MR,;in jux hur ylem,Blade Spirits,BP MR NS,;an grav,Dispel Field,BP GA SS SA,;kal in ex,Incognito,BM GA NS,;in jux sanct,Magic Reflection,GA MR SS,;por corp wis,Mind Blast,BP MR NS SA,;an ex por,Paralyze,GA MR SS,;in nox grav,Poison Field,BP NS SS,;kal xen,Summon Creature,BM MR SS,;an ort,Dispel,GA MR SA,;corp por,Energy Bolt,BP NS,;vas ort flam,Explosion,BM MR,;an lor xen,Invisibility,BM NS,;kal por ylem,Mark,BP BM MR,;vas des sanct,Mass Curse,GA MR NS SA,;in ex grav,Paralyze Field,BP GI SS,;wis quas,Reveal,BM SA,;vas ort grav,Chain Lightning,BP BM MR SA,;in sanct grav,Energy Field,BP MR SS SA,;kal vas flam,Flamestrike,SS SA,;vas rel por,Gate Travel,BP MR SA,;ort sanct,Mana Vampire,BP BM MR SS,;vas an ort,Mass Dispel,BP GA MR SA,;flam kal des ylem,Meteor Swarm,BM MR SS SA,;vas ylem rel,Polymorph,BM MR SS,;in vas por,Earthquake,BM GI MR SA,;vas corp por,Energy Vortex,BP BM MR NS,;an corp,Resurrection,BM GA GI,;kal vas xen hur,Air Elemental,BM MR SS,;kal vas xen corp,Summon Daemon,BM MR SS SA,;kal vas xen ylem,Earth Elemental,BM MR SS,;kal vas xen flam,Fire Elemental,BM MR SS SA,;kal vas xen an flam,Water Elemental,BM MR SS,;expor flamus,Cleanse by Fire,1.0,cure;obsu vulni,Close Wounds,1.5,heal;consecrus arma,Consecrate Weapon,0.5,;dispiro malas,Dispel Evil,0.25,;divinum furis,Divine Fury,1.0,;forul solum,Enemy of One,0.5,;augus luminos,Holy Light,1.75,;dium prostra,Noble Sacrifice,1.5,;extermo vomica,Remove Curse,1.5,;sanctum viatas,Sacred Journey,1.5,;uus corp,Animate Dead,1.75,;in jux mani xen,Blood Oath,1.5,;in agle corp ylem,Corpse Skin,1.5,;an sanct gra char,Curse Weapon,1.0,;pas tym an sanct,Evil Omen,1.0,;rel xen vas bal,Horrific Beast,2.0,;rel xen corp ort,Lich Form,2.0,;wis an ben,Mind Rot,1.5,;in sar,Pain Spike,1.25,;in vas nox,Poison Strike,2.0,;in bal nox,Strangle,2.0,;kal xen bal,Summon Familiar,2.0,;rel xen an sanct,Vampiric Embrace,2.0,;kal xen bal beh,Vengeful Spirit,2.0,;kal vas an flam,Wither,1.5,;rel xen um,Wraith Form,2.0,;ort corp grav,Exorcism,2.0,").split(";"):
		_w,_n,_x,_t=_r.split(",");SPELL_WORDS[_w]=(_n,_t or None)
		if _x[0]>"9":MAGERY.append((_n,_x))
		else:CAST_DELAY_OTHER[_n]=float(_x)
	MAGERY=tuple(MAGERY);del _r,_w,_n,_x,_t;REAGENTS={"BP":("Black Pearl",3962),"BM":("Blood Moss",3963),"GA":("Garlic",3972),"GI":("Ginseng",3973),"MR":("Mandrake Root",3974),"NS":("Nightshade",3976),"SS":("Spiders' Silk",3981),"SA":("Sulfurous Ash",3980)};SPELL_MANA=(4,6,9,11,14,20,40,50);CAST_DELAY=(.5,.75,1.,1.25,1.5,1.75,2.,2.25);CAST_EXTRA=.5;_spells={}
	@staticmethod
	def spell_info(name):
		if not Kit._spells:
			for n,a in Kit.CAST_DELAY_OTHER.items():Kit._spells[n.lower()]=(0,(),0,a)
			for i,(n,b)in enumerate(Kit.MAGERY):c=i//8+1;Kit._spells[n.lower()]=(c,tuple(b.split()),Kit.SPELL_MANA[c-1],Kit.CAST_DELAY[c-1]+Kit.CAST_EXTRA)
		return Kit._spells.get(str(name or "").strip().lower())
	COMPASS=("E","SE","S","SW","W","NW","N","NE");FACETS=("Felucca","Trammel","Ilshenar","Malas","Tokuno","Ter Mur")
	@staticmethod
	def compass(dx,dy,names=None):
		if not dx and not dy:return ""
		return(names or Kit.COMPASS)[int(round(math.atan2(dy,dx)/(math.pi/4)))%8]
	@staticmethod
	def held_item():
		a=HOST.pass_id if HOST.in_hop else None
		if a is not None and Kit._held[0]==a:return Kit._held[1]
		try:v=int(API.GetHeldItem()or 0)
		except Exception:v=0
		if a is not None:Kit._held[0],Kit._held[1]=a,v
		return v
	_held=[-1,0]
	@staticmethod
	def find_item(serial):
		if not serial:return
		try:return API.FindItem(serial)
		except Exception:return
	@staticmethod
	def top_of(serial):
		s=int(serial or 0)
		for b in range(10):
			a=Kit.find_item(s)
			if a is None:return s,0
			try:c=int(a.Container or 0)
			except Exception:c=0
			if not c or c==0xFFFFFFFF:return s,0
			if c<0x40000000:return s,c
			s=c
		return s,0
	@staticmethod
	def in_pack(serial):a=int(API.Backpack or 0);return bool(a)and bool(serial)and Kit.top_of(serial)[0]==a
	@staticmethod
	def where_text(dx,dy,here="under you",names=None):
		d=max(abs(int(dx)),abs(int(dy)))
		if d==0:return here
		return "%s %s"%(Kit.count(d,"tile"),Kit.compass(dx,dy,names))
	@staticmethod
	def count(n,word,a=None):return "%d %s"%(n,word if n==1 else a or word+"s")
	@staticmethod
	def facet_name(m):
		try:m=int(m)
		except Exception:return "?"
		return Kit.FACETS[m]if 0<=m<len(Kit.FACETS)else "facet %d"%m
	AGO=((60,1,"%ds"),(3600,60,"%dm"),(0,3600,"%dh %dm"));AGO_SHORT=((60,1,"%ds"),(3600,60,"%dm"),(0,3600,"%dh"));AGO_WORDS=((60,1,"just now"),(3600,60,"%dm ago"),(86400,3600,"%dh ago"),(0,86400,"%dd ago"))
	@staticmethod
	def ago(secs,units=None):
		secs=max(0,int(secs))
		for c,b,a in units or Kit.AGO:
			if not c or secs<c:break
		n=a.count("%")
		if n==0:return a
		return a%(secs//b)if n==1 else a%(secs//b,secs%b//60)
	@staticmethod
	def read_int(ctrl,default,lo=None,hi=None):
		try:v=int(str(ctrl.Text or "").strip())
		except Exception:return default
		if lo is not None and v<lo:v=lo
		if hi is not None and v>hi:v=hi
		return v
	@staticmethod
	def codec_load(text):
		a={}
		for b in str(text or "").split(";"):
			if "="in b:k,v=b.split("=",1);a[k.strip()]=v.strip()
		return a
	@staticmethod
	def kv_load(key,d,b,a=None,e=()):
		a=a or{}
		for c in Kit.get_var(key).split(d):
			if "="not in c:continue
			k,v=c.split("=",1);k,v=k.strip(),v.strip()
			if k in a:
				try:b[k]=max(a[k][0],min(a[k][1],int(v)))
				except ValueError:pass
			elif k in e:b[k]=v
			elif k in b:b[k]=v=="1"
	@staticmethod
	def kv_save(key,b,vals,order,a=None,c=()):a=a or{};Kit.put_var(key,b.join("%s=%s"%(d,vals[d]if d in a or d in c else("1"if vals[d]else "0"))for d in order))
	@staticmethod
	def with_tip(ctrl,text):
		if text:
			try:ctrl.SetTooltip(text)
			except Exception:pass
		return ctrl
	@staticmethod
	def sayer(title,gate=None,key=None):
		def a(text,hue=None):
			if gate is None or gate[key]:API.SysMsg("%s: %s"%(title,text),Kit.HUE_INFO if hue is None else hue)
		return a
	@staticmethod
	def basics(st,title):return Kit.Cleanup(),Kit.queuer(st),Kit.sayer(title)
	@staticmethod
	def dd_index(dd,default):
		try:return int(dd.GetSelectedIndex())
		except Exception:return default
	@staticmethod
	def drop_arrow(st,a):
		if st["arrow"]is not None:st["arrow"]=None;API.TrackingArrow(-1,-1,a)
	@staticmethod
	def say(text,hue=None):API.SysMsg(APP_NAME+": "+str(text),Kit.HUE_INFO if hue is None else hue)
	@staticmethod
	def win_action(action,st,key,title,build,a=None):
		if action=="settings":HOST.show_settings(key)
		elif action=="toggle_min":
			st["minimized"],st["docked"]=not st["minimized"],False;HOST.dock_forget(key)
			if a:Kit.save_min(a,st["minimized"])
			build()
		elif action=="to_bar":HOST.dock_to_bar(key,title)
		elif action=="redraw":build()
		else:return False
		return True
	@staticmethod
	def show_window(g,x,y,w,h,a,hidden,b,moved,c=None,parts=None,max_h=None):
		d=Kit.place(g,x,y,w,h,None,max_h)
		if a is not None and HOST.layout_locked(a):g.CanMove=False
		if c is not None:c.update(parts)
		if b is not None:G.AddControlOnDisposed(g,b)
		G.AddGump(g)
		if moved is not None:Kit.on_moved(g,moved)
		if hidden:g.IsVisible=False
		return d
	@staticmethod
	def row_set(row,val,now):
		a=row.get("val")
		if(a[0]if a else None)!=(val[0]if val else None):row["prev"],row["val"],row["changed"]=a or None,val,now
	@staticmethod
	def row_clicker(row,queue,kind,a=.15,follow=True):
		def b(*b):
			v=row.get("prev")
			if not(v and time.time()-row.get("changed",0.)<a):v=row.get("val")
			if not v or not v[0]:return
			if follow and Follow.alt_held():queue(("follow",v[0]))()
			else:queue((kind,)+tuple(v))()
		return b
	@staticmethod
	def buttons(g,store,x,y,rows,gap=20):
		for b in rows:Kit.art_button(g,store,b[0],b[1],x,y,b[2],b[3],b[5]if len(b)>5 else None,b[4]if len(b)>4 else None);x+=35+Kit.text_w(b[2])+gap
		return x
	class Form(object):
		OPTS={"top":30,"pad":10,"ch":26,"fh":28,"nh":20,"bh":28,"dx":12,"ldy":3,"lgap":10,"ugap":8,"fw":50,"sw":140,"sdy":2,"ndy":0,"bdy":-2,"bgap":20,"fmt":"%d"};STEP={"check":"ch","note":"nh","buttons":"bh","num":"fh","text":"fh","slider":"fh"};FIELDS=("num","text","slider")
		def __init__(self,g,x,y,w,vals,page=(),store=None,**opts):
			self.g,self.x,self.y,self.w,self.vals,self.opts=g,x,y,w,vals,opts;self.top,self.c,self.store,self.specs=y,{},store or({},{}),[]
			for a in page:self.section(*a)
		@property
		def h(self):return max(0,self.y-self.top-Kit.GAP)
		@staticmethod
		def height(page,w=0,**opts):return Kit.Form(None,0,0,w,{},page,**opts).h
		def _o(self,a,r=None):
			o=dict(Kit.Form.OPTS);o.update(self.opts);o.update(a)
			if r and type(r[-1])is dict:o.update(r[-1])
			return o
		@staticmethod
		def _step(r,o):
			if o.get("stay"):return 0
			if r[0]in("gap","custom"):return r[1]
			return o["h"]if "h"in o else o[Kit.Form.STEP[r[0]]]
		def section(self,title,rows,a=None):
			a=a or{};b,c=self._o(a),[self._o(a,i)for i in rows];d=a.get("sh")or b["top"]+sum(Kit.Form._step(j,k)for j,k in zip(rows,c))+b["pad"];x,e,g=self.x,self.y+b["top"],self.g
			if g is not None:Kit.add_section(g,x,self.y,self.w,d,title)
			self.y+=d+Kit.GAP
			if g is None:return
			f=max([Kit.text_w(l[2])for l in rows if l[0]in Kit.Form.FIELDS]or[0])
			for r,o in zip(rows,c):self._row(g,r,o,x,e,o.get("lw",f if o.get("align")else None));e+=Kit.Form._step(r,o)
		def _row(self,g,r,o,sx,y,lw):
			a,c,x=r[0],self.c,sx+o["dx"];k=r[1]if a in Kit.Form.FIELDS or a=="check"else None
			if a=="check":c[k]=Kit.add_check(g,r[2],x,y,self.vals[k],r[3]);self.specs.append((r,o))
			elif a=="note":
				e=Kit.add_label(g,r[1],x,y+o["ndy"],o.get("hue",Kit.HUE_INFO))
				if o.get("key"):c[o["key"]]=e
			elif a=="buttons":Kit.buttons(g,self.store,x,y+o["bdy"],[i[:5]for i in r[1]],o["bgap"])
			elif a=="custom":r[2](self,sx,y)
			elif a in Kit.Form.FIELDS:
				e=Kit.add_label(g,r[2],x,y+o["ldy"]);b=x+(Kit.text_w(r[2])if lw is None else lw)+o["lgap"];d=r[3]
				if a=="num":
					if d and not d.endswith(")"):d+=" (%d-%d)"%(r[5],r[6])
					c[k]=Kit.add_textbox(g,o["fmt"]%self.vals[k],b,y,o["fw"])
					if r[4]:Kit.add_label(g,r[4],b+o["fw"]+o["ugap"],y+o["ldy"],Kit.HUE_INFO)
				elif a=="text":f=o.get("tw")or self.w-(b-sx)-16;c[k]=Kit.add_textbox(g,self.vals[k],b,y,f,numbers=False)
				else:
					c[k]=Kit.add_slider(g,b,y+o["sdy"],o["sw"],r[4],r[5],self.vals[k])
					if o.get("vfmt")or o.get("unit"):c[k+"_lbl"]=Kit.add_label(g,o["vfmt"]%self.vals[k]if o.get("vfmt")else o["unit"],b+o["sw"]+o["ugap"],y+o["ldy"],Kit.HUE_INFO)
				Kit.with_tip(c[k],d)
				if o.get("ltip"):Kit.with_tip(e,d)
				self.specs.append((r,o))
		def read(self,strict=False,empty=None):
			a=dict(self.vals)
			for r,o in self.specs:
				b,k=r[0],r[1]
				try:
					c=self.c[k]
					if b=="check":v=bool(c.IsChecked)
					elif b=="num":v=Kit.read_int(c,a[k],*((r[5],r[6])if o.get("clamp",True)else()));v=o.get("cast",int)(v if r[5]<=v<=r[6]else a[k])
					elif b=="text":v=str(c.Text or "").strip()or(empty or{}).get(k,"")
					else:v=max(r[4],min(r[5],int(c.Value)))
				except Exception:
					if strict:raise
					continue
				a[k]=v
				if b=="slider"and o.get("vfmt"):Kit.set_text(self.c[k+"_lbl"],o["vfmt"]%v)
			return a
	class Page(object):
		def __init__(self,vals,table,save=None,a=None,opts=None,strict=False,empty=None,adjust=None,clicks=None,every=0.,final=False):self.vals,self.table,self.save,self.on_change,self.opts=vals,table,save,a,opts or{};self.strict,self.empty,self.adjust,self.clicks,self.every=strict,empty,adjust,clicks,every;self.f,self.unread,self.at,self.final,self.force=None,False,0.,final,False
		def rows(self,w):return self.table(w)if callable(self.table)else self.table
		def height(self,w):return Kit.Form.height(self.rows(w),w,**self.opts)
		def build(self,g,x,y,w):self.unread,self.at=False,0.;self.f=Kit.Form(g,x,y,w,self.vals,self.rows(w),**self.opts);return self.f
		def poll(self,force=False):
			f=self.f
			if f is None:return
			if self.clicks is not None:
				self.clicks(f)
				if self.f is not f:return
			if self.every:
				b=time.time()
				if not force and b<self.at:self.unread=True;return
				self.at,self.unread=b+self.every,False
			try:a=f.read(self.strict,self.empty)
			except Exception:self.f=None;return
			self.force=force
			if self.adjust is not None:self.adjust(f,a)
			if a==self.vals:return
			c=dict(self.vals);self.vals.update(a)
			if self.save is not None:self.save()
			if self.on_change is not None:self.on_change(c,self.vals)
		def closed(self):
			if(self.unread or self.final)and self.f is not None:self.poll(True)
			self.f,self.unread=None,False
	class Cleanup(object):
		def __init__(self):self.jobs=[]
		def add(self,fn,*a):self.jobs.append((fn,a));return fn
		def service(self,name,fn):HOST.services[name]=fn;self.jobs.append((Kit.Cleanup.drop,(name,fn)));return fn
		@staticmethod
		def drop(name,fn):
			if HOST.services.get(name)is fn:HOST.services.pop(name,None)
		def close(self):
			a=self.jobs
			while a:
				b,c=a.pop()
				with Kit.quiet:b(*c)
	class Window(object):
		def __init__(self,key,title,st,win,build,a,b=None,default=(200,200),mini=None,icon=None,cleanup=None,gkey="g",names=("c","store"),lock=True,owner=True,close_tip=None,clear=None,docked_min=False):self.key,self.title,self.st,self.win,self.build,self.pos_key=key,title,st,win,build,a;self.min_key,self.default,self.mini,self.icon,self.cleanup=b,default,mini,icon,cleanup;self.gkey,self.names,self.lock,self.owner,self.close_tip=gkey,names,lock,owner,close_tip;self.clear,self.docked_min,self.slot,self.held,self.old=clear or{},docked_min,None,False,None;self.queue=Kit.queuer(st)if st is not None else None;self.x=self.y=self.w=self.h=0;self.c,self.store={},({},{})
		def minimized(self):return self.st is not None and bool(self.st["minimized"])
		def start_min(self):return bool(HOST.dock_wanted(self.key)or(self.min_key and Kit.load_min(self.min_key)))
		def begin(self,w,h,default=None):
			if self.queue is not None:Kit._wins[self.key]=self
			if Kit.is_open(self.old)and self.old is not self.win.get(self.gkey):Kit.dispose(self.old)
			a=self.win.get(self.gkey);b=self.minimized()
			if b and self.mini:w,h=self.mini
			self.w,self.h=w,h
			if Kit.is_open(a):self.x,self.y=a.GetX(),a.GetY()
			else:self.x,self.y=Kit.load_pos(self.pos_key,default or self.default,(w,h))
			self.old,self.win[self.gkey]=a,None
			if self.cleanup is not None and not self.held:self.held=True;self.cleanup.add(self.release)
			g=G.CreateGump(True,True);self.c,self.store={},({},{})
			if b:self.c["status"]=Kit.mini_bar(g,self.store,w,h,self.title,self.key,self.queue("toggle_min"),close_tip=self.close_tip)
			return g,self.store,self.c
		def frame(self,g,w=None,h=None,extra=None,after=None,settings=True,mouse=True,corners=True):w=self.w if w is None else w;q=self.queue;Kit.add_window_frame(g,w,self.h if h is None else h,corners,mouse);return Kit.title_bar(g,self.store,w,self.title,self.key,q("toggle_min"),q("to_bar"),q("settings")if settings else None,self.close_tip,extra,after)
		def end(self,g,parts=None,w=None,h=None,max_h=None):
			c,parts=self.st,dict(parts or{});parts[self.gkey]=g
			for d,v in zip(self.names or(),(self.c,self.store)):parts[d]=v
			b=Kit.show_window(g,self.x,self.y,self.w if w is None else w,self.h if h is None else h,self.key if self.lock else None,c is not None and c["minimized"]and c["docked"],self.disposed(g),self.save_pos,self.win,parts,max_h);a=LAYOUT.placed.get(self.key)if LAYOUT.seamless and LAYOUT.holds(self.key)else None
			if a is not None and b is not None and(b[0],b[1])!=(a[0],a[1]):g.SetPos(int(a[0]),int(a[1]));Kit.note_rect(g,a[0],a[1]);Kit.moved_by_code(g);b=(a[0],a[1])
			if a is not None and b is not None:LAYOUT.fit_now(self.key,g)
			e,self.old=self.old,None;Kit.dispose(e);return b
		def disposed(self,g):
			def a(*b):
				a=self.win
				if a.get(self.gkey)is not g or(self.owner and self.st["shutting"]):return
				a[self.gkey]=None;a.update(self.clear)
				if self.owner:HOST.disable(self.key)
			return a
		def save_pos(self):Kit.save_pos(self.pos_key,self.win.get(self.gkey))
		def close(self):
			if Kit.is_open(self.old)and self.old is not self.win.get(self.gkey):Kit.dispose(self.old)
			a=self.st;self.save_pos()
			if self.min_key and a is not None:Kit.save_min(self.min_key,a["minimized"]and not(self.docked_min and a["docked"]))
			g,self.win[self.gkey]=self.win.get(self.gkey),None;self.win.update(self.clear);Kit.dispose(g)
		def release(self):self.held=False;self.close()
		def action(self,action):return Kit.win_action(action,self.st,self.key,self.title,self.build,self.min_key)
		def fit(self,w,h,mode):
			a=(int(w),int(h))if(w is not None and h is not None)else None
			if a!=self.slot or(mode=="again"and a is not None):self.slot=a;self.queue("redraw")()
		def rows(self,row_h,fixed_h,a,b=1):
			if self.slot is None or not HOST.layout_holds(self.key):return a
			return max(b,int(self.slot[1]-fixed_h)//max(1,int(row_h)))
		def dock(self,fit=False,**extra):
			a=Kit.dock_hooks(self.title,self.icon,self.st,self.win,self.queue("redraw"),self.fit if fit is True else(fit or None));a.update(extra);HOST.dock_add(self.key,a)
			if self.cleanup is not None:self.cleanup.add(HOST.dock_remove,self.key)
			return a
	class _Quiet(object):
		def __enter__(self):return self
		def __exit__(self,kind,value,tb):return kind is not None and issubclass(kind,Exception)
	quiet=_Quiet();_notos={}
	@staticmethod
	def noto_name(mob):
		try:v=mob.Notoriety
		except Exception:return "unknown"
		return Kit.noto_of(v)
	@staticmethod
	def noto_of(v):
		try:return Kit._notos[v]
		except KeyError:pass
		except Exception:return str(v).split(".")[-1].lower()
		n=Kit._notos[v]=str(v).split(".")[-1].lower();return n
	@staticmethod
	def set(obj,a,value):
		try:setattr(obj,a,value)
		except Exception:pass
class Fill(object):
	ROW_H=72;MIN_EDGE=20;MIN_BG=40;FILL_MIN_K=.6;FIELD_T="TTFTextInputField";recs={};by_raw={};w2r={};_api_t=[None];broken=False
	@staticmethod
	def _axis(n,N,M,h,mode):
		n,N=float(max(1,n)),float(max(1,N));E=N-n
		if E<.5:return
		d,e=float(M),n-M
		if e-d<8:d,e=0.,n
		a=[]
		for b,c in sorted(h):
			b,c=max(d,float(b)),min(e,float(c))
			if c-b<1:continue
			if a and b<=a[-1][1]:a[-1][1]=max(a[-1][1],c)
			else:a.append([b,c])
		if not a or mode=="grid":a=[[d,e]]
		L=sum(j-i for i,j in a);f=[(0.,0.)];g=0.
		for b,c in a:f.append((b,b+g));g+=E*(c-b)/L;f.append((c,c+g))
		f.append((n,n+g));return f
	@staticmethod
	def _ev(m,v):
		if m is None or v<=m[0][0]:return float(v)
		for i in range(1,len(m)):
			a,c=m[i-1];b,d=m[i]
			if v<=b:
				if b-a<1e-9:return d
				return c+(v-a)*(d-c)/(b-a)
		e,f=m[-1];return f+(v-e)
	@staticmethod
	def _xform(rec,e):
		F,x,y,w,h,c=e[:6];u=e[8]if len(e)>8 else None
		if u=="back":
			q=rec["ent"].get(e[9])
			if q is not None:n=Fill._xform(rec,q);return n[0]-2,n[1]-1,n[2]+4,n[3]+(h-q[4])
		k=rec.get("k",1.);v=h
		if k!=1.:
			x,y,w=x*k,y*k,w*k
			if u=="field":z=e[10]if len(e)>10 else None;A=h if z is None else max(h*k,min(h,(h+2*z)*k));y=y+h*k/2.-A/2.;h=A
			else:h=h*k
			if c is not None:c=(c[0]*k,c[1]*k,c[2]*k,c[3]*k)
			w=max(1,int(round(w)));h=max(1,int(round(h)))
		d,g=rec["fx"],rec["fy"];N,j=rec["size"];a=Fill._ev
		if F=="s":
			o,r=a(d,x),a(d,x+w)
			if v>=Fill.MIN_EDGE and(v>Fill.ROW_H or rec["rows"])and not Fill.title_strip(e[2],e[4]):l,p=a(g,y),a(g,y+h)
			else:B=a(g,y+h/2.);l,p=B-h/2.,B+h/2.
			o=max(0,min(N-1,int(round(o))));l=max(0,min(j-1,int(round(l))));r,p=min(N,int(round(r))),min(j,int(round(p)));return o,l,max(1,r-o),max(1,p-l)
		s=rec["mode"]
		if c is not None:
			f,G,m,H=c
			if s=="frame":C,D=f+m/2.,G+H/2.;b=x+a(d,C)-C;i=y+a(g,D)-D
			else:
				if s=="anchor":
					E=m/3.;t=x+w/2.
					if t<f+E:b=a(d,f)+(x-f)
					elif t>f+m-E:b=a(d,f+m)-(f+m-x)
					else:b=a(d,t)-w/2.
				else:b=a(d,x+w/2.)-w/2.
				i=a(g,y+h/2.)-h/2.
		elif s=="frame"and not e[7]:b=x+(N-rec["nat"][0]*k)/2.;i=y+(j-rec["nat"][1]*k)/2.
		else:b=a(d,x+w/2.)-w/2.;i=a(g,y+h/2.)-h/2.
		b=max(0,min(int(round(b)),N-w))if w<N else 0;i=max(0,min(int(round(i)),j-h))if h<j else 0;return b,i,w,h
	@staticmethod
	def raw_of(c):
		r=Fill.w2r.get(c)
		if r is None:
			r=Kit.client_control(c)
			if r is None:return
			if len(Fill.w2r)>4000:Fill.w2r.clear()
			Fill.w2r[c]=r
		return r
	@staticmethod
	def _set(raw,r,c=False):
		t=Fill._api_t[0]
		if t is None:return False
		try:
			a=Fill._wraps;w=a.get(raw)
			if w is None:
				b=Fill._mk
				if b is None:import System;b=Fill._mk=System.Activator.CreateInstance
				w=b(t,raw)
				if len(a)>=6000:a.clear()
				a[raw]=w
			if c:w.SetPos(int(r[0]),int(r[1]))
			else:w.SetRect(int(r[0]),int(r[1]),int(r[2]),int(r[3]))
			return True
		except Exception:Fill.broken=True;return False
	_wraps={};_mk=None
	@staticmethod
	def _find_api_type(g):
		if Fill._api_t[0]is not None:return True
		with Kit.quiet:
			import clr;t=clr.GetClrType(type(g))
			while t is not None:
				if str(t.Name)=="ApiUiBaseControl":Fill._api_t[0]=t;return True
				t=t.BaseType
		return False
	@staticmethod
	def _scan(rec,kids,skip,f=1.):
		g=rec["ent"];h=Kit._same();d=[]
		for c in kids:
			try:
				if c.IsDisposed or c in g or c in Seam.catchers:continue
			except Exception:continue
			if skip and any(h(c,i)for i in skip):continue
			r=Kit._raw_rect(c)
			if r is None:continue
			a=str(c.GetType().Name);b="s"if a in Fill.STRETCH else "p"
			if a=="GumpPic":
				with Kit.quiet:
					if int(c.Graphic)in(Kit.LINE_RED,Kit.LINE_BLUE,Kit.LINE_POISON):b="s"
			if b=="s"and a=="AlphaBlendControl"and r[2]<Fill.MIN_BG:
				with Kit.quiet:
					if float(c.Alpha)<.05:b="p"
			e=[b,r[0],r[1],r[2],r[3],None,tuple(r),c in rec["frame"],"field"if a==Fill.FIELD_T else None,None,None];g[c]=e;Fill.by_raw[c]=(rec,e);d.append((c,e))
			if a=="ScrollArea":rec["nested"]=True
			if f!=1.:Fill._scale_one(rec,c,f)
		if d:Fill._pair_fields(rec)
		return d
	@staticmethod
	def _pair_fields(rec):
		f=rec["ent"];g=[(o,n)for o,n in f.items()if n[8]=="field"]
		if not g:return
		for h,e in f.items():
			if e[0]!="s"or e[8]is not None or e[7]:continue
			for i,a in g:
				if abs(e[1]-(a[1]-2))<=1 and abs(e[2]-(a[2]-1))<=1 and abs(e[3]-(a[3]+4))<=1 and e[4]<=26:e[8],e[9]="back",i;a[9]=h;break
		for i,a in g:
			c,b,m,j=a[1],a[2],a[3],a[4];d=None
			for h,e in f.items():
				if h is i or e[8]=="back"or e[7]:continue
				x,y,w,k=e[1],e[2],e[3],e[4]
				if x>=c+m or x+w<=c:continue
				if x<=c and y<=b and x+w>=c+m and y+k>=b+j:continue
				if y+k<=b:l=b-(y+k)
				elif y>=b+j:l=y-(b+j)
				else:continue
				d=l if d is None else min(d,l)
			a[10]=d
	@staticmethod
	def _desc(c):
		a=[]
		try:b=list(Kit._children(c))
		except Exception:return a
		while b:
			d=b.pop();a.append(d)
			with Kit.quiet:b.extend(Kit._children(d))
		return a
	@staticmethod
	def _scale_one(rec,c,k):
		try:
			if abs(k-1.)>.001 and str(c.GetType().Name)=="GumpPicTiled":c.ScaleTiledTexture=True
			c.SetInternalScale(k)
		except Exception:pass
		b=rec["desc"]
		for d in Fill._desc(c):
			try:
				a=b.get(d)
				if a is None:
					r=Kit._raw_rect(d)
					if r is None:continue
					a=b[d]=tuple(r)
				if abs(k-1.)>.001 and str(d.GetType().Name)=="GumpPicTiled":d.ScaleTiledTexture=True
				Fill._set(d,(a[0]*k,a[1]*k,max(1,a[2]*k),max(1,a[3]*k)));d.SetInternalScale(k)
			except Exception:pass
	STRETCH=("GumpPicTiled","AlphaBlendControl","ScrollArea","ResizePic","SimpleProgressBar")
	@staticmethod
	def _bgs(rec):
		c,a=rec["nat"];b=[];d=rec["frame"]
		for f,e in rec["ent"].items():
			if e[0]!="s"or f in d or e[8]=="back":continue
			x,y,w,h=e[1],e[2],e[3],e[4]
			if w<Fill.MIN_BG or h<Fill.MIN_EDGE:continue
			if w>=c-8 and h>=a-8:continue
			if y<2 or y+h>a-2:continue
			b.append((x,y,w,h))
		return b
	@staticmethod
	def title_strip(y,h):return y<=Kit.MARGIN+2 and h<=31
	@staticmethod
	def _maps(rec):
		c,d=rec["nat"];N,e=rec["size"];k=rec.get("k",1.);M=Kit.MARGIN*k;a=Fill._bgs(rec);b=[g for g in a if g[3]>Fill.ROW_H];rec["rows"]=not b;rec["fx"]=Fill._axis(c*k,N,M,[(h[0]*k,(h[0]+h[2])*k)for h in a],rec["mode"]);rec["fy"]=Fill._axis(d*k,e,M,[(i[1]*k,(i[1]+i[3])*k)for i in(b or a)if not Fill.title_strip(i[1],i[3])],rec["mode"]);rec["bgs"]=a
		for f in rec["ent"].values():Fill._anchor(f,a)
	@staticmethod
	def _anchor(e,bgs):
		if e[0]=="s":return
		b,c=e[1]+e[3]/2.,e[2]+e[4]/2.;a=None
		for x,y,w,h in bgs:
			if(x<=b<=x+w and y<=c<=y+h and(a is None or w*h<a[2]*a[3])):a=(x,y,w,h)
		e[5]=a
	@staticmethod
	def _apply(rec,a=None):
		for c,e in(list(rec["ent"].items())if a is None else a):
			try:
				if c.IsDisposed:rec["ent"].pop(c,None);Fill.by_raw.pop(c,None);Fill._wraps.pop(c,None);continue
			except Exception:continue
			r=Fill._xform(rec,e)
			if r!=e[6]and Fill._set(c,r,e[0]=="p"and rec.get("k",1.)==1. and(r[2],r[3])==(e[3],e[4])):e[6]=r
	@staticmethod
	def fit(g,x,y,W,H,mode="anchor"):
		if Fill.broken or not Fill._find_api_type(g)or not Kit.flush():return
		c=Kit._raw_gump(g)
		if c is None:return
		a=Fill.recs.get(g);d=Kit.scroll_info(g)
		if a is None:
			r=Snap.rect(g)
			if r is None:return
			w=(d["w"],d["h"])if d is not None else(r[2],r[3]);a={"g":g,"raw":c,"nat":w,"size":None,"slot":None,"mode":mode,"ent":{},"fx":None,"fy":None,"rows":False,"n":-1,"an":-1,"placed":None,"scroll":False,"bgs":[],"frame":set(),"k":1.,"desc":{},"nested":False,"head0":(d["head"]if d is not None else None)or(Kit.MARGIN+30+Kit.GAP)};p=Kit._frames.get(g);a["frame"].update(C for C in map(Kit.client_control,p["pieces"]if p else())if C is not None);Fill.recs[g]=a
		elif a["placed"]is not None and d is None:
			r=Snap.rect(g)
			if r is not None and(r[2],r[3])!=a["placed"][2:]:a["nat"]=(r[2],r[3]);a["size"]=None
		a["mode"]=mode;z,b=Kit._scroll_skip(g)
		try:i=(int(c.Children.Count),int(b.Children.Count)if b is not None else 0)
		except Exception:i=None
		q=time.time()
		if i is not None and i==a.get("cnt")and 0<=a.get("full_at",0.)-q:s,l=a["n"],a.get("an")
		else:a["cnt"]=i;a["full_at"]=q+Kit.SWEEP_FULL;s=Kit._live_count(c);l=Kit._live_count(b)if b is not None else 0
		e=[]
		if s!=a["n"]or l!=a.get("an"):
			m=Kit._children(c)
			if b is not None:m=m+Kit._children(b)
			e=Fill._scan(a,m,z+([b]if b is not None else[]),a["k"]);a["n"],a["an"]=Kit._live_count(c),l
		n,f=a["nat"];t=Kit.SCROLL_BAND;o=g in Kit._scrolled
		if o:u=W-t;k=1. if(u>=n and H>=f)else min(1.,u/float(n),max(Fill.FILL_MIN_K,H/float(f)));h=f*k>H+1
		else:k,h=Fill.scale_for(n,f,W,H,a["nested"])
		j=(W-t,int(round(f*k))if h else H)if h or o else(W,H)
		if abs(k-a["k"])>.0005:
			a["k"]=k
			for v in list(a["ent"]):Fill._scale_one(a,v,k)
			a["size"]=None
		if j!=a["size"]or mode!=a.get("mode_was"):a["size"],a["mode_was"],a["scroll"]=j,mode,h;Fill._maps(a);Fill._apply(a)
		elif e:
			for v,A in e:Fill._anchor(A,a["bgs"])
			Fill._apply(a,e)
		r=Snap.rect(g)
		if r is not None and(r[0],r[1],r[2],r[3])==(x,y,W,H)and not e and a["placed"]is not None:return False
		if h or o:B=int(round(a["head0"]*k));Kit._place_raw(g,x,y,j[0],j[1],B,H)
		else:Kit._place_raw(g,x,y,W,H,None,None)
		r=Snap.rect(g);a["placed"]=(x,y,r[2],r[3])if r is not None else(x,y,W,H);a["slot"]=(x,y,W,H);return True
	@staticmethod
	def scale_for(nw,nh,W,H,nested=False):
		nw,nh=float(max(1,nw)),float(max(1,nh))
		if W>=nw and H>=nh:return 1.,False
		if nested:return min(1.,W/nw,H/nh),False
		k=min(1.,W/nw,max(Fill.FILL_MIN_K,H/nh))
		if nh*k>H+1:k=min(1.,(W-Kit.SCROLL_BAND)/nw,max(Fill.FILL_MIN_K,H/nh));return k,nh*k>H+1
		return k,False
	@staticmethod
	def unfit(g):
		a=Fill.recs.pop(g,None)
		if a is None:return False
		for d,b in list(a.get("desc",{}).items()):
			try:
				if not d.IsDisposed:Fill._set(d,b);d.SetInternalScale(1.)
			except Exception:pass
		for c,e in list(a["ent"].items()):
			Fill.by_raw.pop(c,None)
			try:
				if not c.IsDisposed:
					if a.get("k",1.)!=1.:c.SetInternalScale(1.)
					Fill._set(c,(e[1],e[2],e[3],e[4]),e[0]=="p"and a.get("k",1.)==1.)
			except Exception:pass
			Fill._wraps.pop(c,None)
		if Kit.is_open(g):
			try:f,h=a["nat"];Kit._place_raw(g,int(g.GetX()),int(g.GetY()),f,h,None,None);Kit.moved_by_code(g)
			except Exception:pass
		return True
	@staticmethod
	def beside(a,r,b):
		def c(a,e,b,c,d,f):
			if a>=c:return f+(a-c)
			if e<=b:return d-(b-a)
			return a+(d-b)
		return(c(a[0],a[0]+a[2],r[0],r[0]+r[2],b[0],b[0]+b[2]),c(a[1],a[1]+a[3],r[1],r[1]+r[3],b[1],b[1]+b[3]))
	@staticmethod
	def prune():
		if not Fill.recs:return
		for g in[b for b in Fill.recs if not Kit.is_open(b)]:
			a=Fill.recs.pop(g)
			for c in a["ent"]:Fill.by_raw.pop(c,None);Fill._wraps.pop(c,None)
		if len(Fill.by_raw)>20000:
			Fill.by_raw.clear()
			for a in Fill.recs.values():
				for c,e in a["ent"].items():Fill.by_raw[c]=(a,e)
	@staticmethod
	def entry(c):return Fill.by_raw.get(Fill.raw_of(c))if Fill.recs else None
	@staticmethod
	def change(c,x=None,y=None,w=None,h=None):
		b=Fill.entry(c)
		if b is None:return False
		a,e=b
		for i,v in((1,x),(2,y),(3,w),(4,h)):
			if v is not None:e[i]=int(v)
		if a["size"]is None:return False
		if e[0]=="p"and(x is not None or y is not None):Fill._anchor(e,a["bgs"])
		r=Fill._xform(a,e)
		try:
			if e[0]=="p"and w is None and h is None:c.SetPos(r[0],r[1])
			else:c.SetRect(r[0],r[1],r[2],r[3])
			e[6]=r
		except Exception:return False
		return True
	@staticmethod
	def own(c):a=Fill.entry(c);return None if a is None else tuple(a[1][1:5])
class PageCanvas(object):
	def __init__(self,inner):self._inner=inner;self.ctrls=[];self.sections=[]
	def Add(self,ctrl,*a):
		self.ctrls.append(ctrl)
		if self._inner is not None:return self._inner.Add(ctrl,*a)
		return ctrl
	def __getattr__(self,name):
		if self._inner is None:raise AttributeError(name)
		return getattr(self._inner,name)
class Alerts(object):
	KEY="VirtueAssistant_alerts";POS_KEY="VirtueAssistant_alert_pos";W,H=420,46;LEVELS={"info":Kit.HUE_INFO,"warn":Kit.HUE_TITLE,"alarm":Kit.HUE_BAD};TEST_KEY="va.test"
	def __init__(self):self.kinds={};self.order=[];self.choice={};self.banner_on=True;self.mute=self.loaded=self.busy=self.shown=self.alarm=self.flash_on=self.clicked=False;self.last={};self.pending=[];self.sounds=[];self.pings=[];self.sound_at=self.hide_at=self.flash_at=self.moved_at=0.;self.g=self.pos=None;self.c={};self.count=0;self.hue=Kit.HUE_TITLE;self.line="";self.tw=self.W-36
	def load(self):
		self.loaded=True;self.choice={};self.mute,self.banner_on=False,True
		for k,v in Kit.codec_load(Kit.get_var(self.KEY)).items():
			if k=="mute":self.mute=v=="1"
			elif k=="banner":self.banner_on=v!="0"
			elif k.startswith("kind."):
				a=v.split(",")
				try:b=int(a[1])if len(a)>1 and a[1]!=""else None
				except ValueError:b=None
				self.choice[k[5:]]=[a[0]!="0",b]
	def save(self):
		a=["mute=%d"%(1 if self.mute else 0),"banner=%d"%(1 if self.banner_on else 0)]
		for k in sorted(self.choice):c,b=self.choice[k];a.append("kind.%s=%d,%s"%(k,1 if c else 0,""if b is None else int(b)))
		Kit.put_var(self.KEY,";".join(a))
	def setting(self,key):
		if not self.loaded:self.load()
		k=self.kinds.get(key);a=self.choice.get(key);b=a[0]if a is not None else True;c=a[1]if a is not None and a[1]is not None else(k["sound"]if k else 0);return b,int(c or 0)
	def choose(self,key,on=None,sound=None):
		a=self.setting(key);b=[a[0]if on is None else bool(on),a[1]if sound is None else int(sound)]
		if b!=list(a)or key not in self.choice:self.choice[key]=b;self.save()
	def kind(self,key,label,sound=None,owner=None):
		key=str(key);k=self.kinds.get(key);a={"label":str(label or key),"sound":int(sound or 0),"owner":str(owner or APP_NAME)}
		if k is None:self.order.append(key)
		if a!=k:
			self.kinds[key]=a
			if key!=self.TEST_KEY:HOST.refresh_settings(ALERTS_PAGE)
		return key
	def raise_(self,key,text,level="warn",sound=None,ping=None,who=None,owner=None):
		if not self.loaded:self.load()
		key=str(key);k=self.kinds.get(key)
		if k is None:self.kind(key,key,sound,owner);k=self.kinds[key]
		h,c=self.setting(key)
		if not h:return False
		a=time.time();d=(key,str(who)if who is not None else str(text));t=self.last.get(d)
		if t is not None and 0<=a-t<ALERT_RATE:return False
		if len(self.last)>200:
			i=a-ALERT_RATE
			for j in[m for m,l in self.last.items()if l<i or l>a]:del self.last[j]
		self.last[d]=a;e=k["owner"];text=str(text);f=text if text.startswith(e+":")else "%s: %s"%(e,text);g=self.LEVELS.get(level,Kit.HUE_TITLE);API.SysMsg(f,g);b=(int(sound)if sound else c)if c else 0
		if b and not self.mute and len(self.sounds)<4:
			if not self.sounds and not 0<=a-self.sound_at<ALERT_SOUND_GAP:self._play(b,a)
			else:self.sounds.append(b)
		if self.banner_on:
			self.pending.append((f,g,level=="alarm"))
			if len(self.pending)>50:del self.pending[:-50]
		if ping is not None and len(self.pings)<8:safe(lambda:self.pings.append([int(ping[0]),int(ping[1]),a+10.]))
		self.busy=True;return True
	def _play(self,sid,now):self.sound_at=now;API.PlaySound(int(sid))
	def tick(self,now):
		if not self.busy:return
		if self.sounds and not 0<=now-self.sound_at<ALERT_SOUND_GAP:self._play(self.sounds.pop(0),now)
		if self.pings:
			x,y,c=self.pings[0];b=HOST.services.get("pings.send");a=now>c or b is None
			if not a:
				try:a=bool(b(x,y))
				except Exception:a=True
			if a:self.pings.pop(0)
		if self.pending:d,self.pending=self.pending,[];self._show(d,now)
		if self.shown:self._watch(now)
		self.busy=bool(self.sounds or self.pings or self.pending or self.shown)
	def _show(self,items,now):
		if not self.banner_on:return
		a,b,c=items[-1]
		if self.shown and Kit.is_open(self.g):self.count+=len(items);self.alarm=self.alarm or any(e for d,d,e in items)
		else:self.count=len(items)-1;self.alarm=any(g for f,f,g in items)
		self.line,self.hue=a,b
		if not Kit.is_open(self.g):self._build()
		if self.g is None:return
		self._label()
		if not self.shown:Kit.set(self.g,"IsVisible",True);self.shown=True;self.clicked=False;self.pos=Snap.pos(self.g)
		self.hide_at=now+ALERT_HOLD;self.flash_at=now+ALERT_FLASH;self.flash_on=True
	def _label(self):
		c=self.c;a=("+%d more"%self.count)if self.count>0 else "";b=Kit.text_px(a)if a else 0;d=self.W-36-((b+8)if a else 0);self.tw=d;Kit.set_text(c["text"],Kit.fit(self.line,d),self.hue);Kit.set_text(c["more"],a,Kit.HUE_INFO)
		if a:c["more"].SetPos(self.W-18-b,15)
	def _watch(self,now):
		g=self.g
		if not Kit.is_open(g):self.shown,self.g=False,None;return
		p=Snap.pos(g)
		if p!=self.pos:
			if self.pos is not None:self.moved_at=now
			self.pos=p
		if self.clicked:
			self.clicked=False
			if not 0<=now-self.moved_at<=.35:self.dismiss();return
		if self.alarm:
			if not 0<self.flash_at-now<=ALERT_FLASH:self.flash_at=now+ALERT_FLASH;self.flash_on=not self.flash_on;Kit.set_text(self.c["text"],Kit.fit(self.line,self.tw),Kit.HUE_BAD if self.flash_on else Kit.HUE_TEXT)
		elif not 0<self.hide_at-now<=ALERT_HOLD:self.dismiss()
	def dismiss(self):
		self.shown,self.count,self.alarm=False,0,False;g=self.g
		if Kit.is_open(g):Kit.set(g,"IsVisible",False)
	def _click(self):self.clicked=True;self.busy=True
	def _build(self):W,H=self.W,self.H;a=Kit.screen()[0]or 1024;x,y=Kit.load_pos(self.POS_KEY,(max(0,(a-W)//2),60),(W,H));g=G.CreateGump(True,True);Kit.add_window_frame(g,W,H,corners=False);Kit.add_section(g,8,8,W-16,H-16);c={"text":Kit.add_label(g,"",18,15,Kit.HUE_TITLE),"more":Kit.add_label(g,"",W-60,15,Kit.HUE_INFO)};Kit.catcher(g,0,0,W,H,self._click,"Click to dismiss; drag to move",movable=True);Kit.show_window(g,x,y,W,H,None,False,None,lambda:Kit.save_pos(self.POS_KEY,self.g));self.g,self.c=g,c;self.shown=False
	def close(self):
		g,self.g=self.g,None
		if Kit.is_open(g):Kit.save_pos(self.POS_KEY,g)
		Kit.dispose(g);self.shown=False;self.pending,self.sounds,self.pings=[],[],[];self.busy=False
class Guard(object):
	KEY="VirtueAssistant_guard";EVERY=.25
	def __init__(self):self.state=self.rd=self.saved=None;self.next=0.;self.cache=(0.,None,None)
	def tick(self,now):
		if now<self.next and self.next-now<=self.EVERY:return
		self.next=now+self.EVERY
		if self.rd is None:self.rd=Journal.reader();self.rd.last=0
		for b in self.rd.new():
			c=b.low
			if "protection of the town guards"not in c:continue
			if b.name and b.name.lower()!="system":continue
			a=False if c.startswith(GUARD_OUT_TEXTS)else True if c.startswith(GUARD_IN_TEXTS)else None
			if a is not None and a!=self.state:self.state=a;self.cache=(0.,None,None);self._save(a)
	@staticmethod
	def _where():
		try:p=HOST.me();return int(p.X),int(p.Y),int(API.GetMap())
		except Exception:return
	def _save(self,state):
		w=self._where()
		if w is None or not(w[0]or w[1]):return
		self.saved=(state,w[0],w[1],w[2]);Kit.put_var(self.KEY,"%d,%d,%d,%d"%(1 if state else 0,w[0],w[1],w[2]))
	def store(self):
		if self.state is not None:self._save(self.state)
	def _look(self):
		d=time.time()
		if d<self.cache[0]<=d+1.:return self.cache[1],self.cache[2]
		w=self._where();b,e=None,None
		if w is not None:
			x,y,m=w
			for a in GUARD_AREAS:
				try:
					if a[0]==m and a[1]<=x<=a[3]and a[2]<=y<=a[4]:b,e=True,str(a[5]);break
				except Exception:continue
			if b is None and self.state is None:
				if self.saved is None:
					try:c=[int(f)for f in Kit.get_var(self.KEY).split(",")];self.saved=(c[0]==1,c[1],c[2],c[3])
					except Exception:self.saved=(None,0,0,-1)
				s=self.saved
				if s[0]is not None and s[3]==m and abs(s[1]-x)<=GUARD_SPOT and abs(s[2]-y)<=GUARD_SPOT:b=s[0]
		self.cache=(d+1.,b,e);return b,e
	def guarded(self):
		if self.state is not None:return self.state
		return self._look()[0]
	def area(self):return self._look()[1]
class _Page(object):
	def __init__(self):self.c=None;self.store=({},{})
	def closed(self):self.c=None
	def api(self):return{"config_height":self.height,"build_config":self.build,"poll_config":self.poll,"config_closed":self.closed}
class AlertsPage(_Page):
	def kinds(self):return[a for a in ALERTS.order if a!=Alerts.TEST_KEY]
	def table(self,w):return(("ALERTS  (every module's warnings)",(("check","mute","Mute every alert sound","No alert sounds; banners and journal lines stay",{"stay":True}),("check","banner","Show the banner","Show alerts in a banner (click to dismiss, drag to move)",{"dx":242}),("buttons",(("test",Kit.ART_PLAY,"Test alert","Raise a test alert"),),{"bdy":4,"stay":True}),("note","The same alert repeats at most every %d s."%int(ALERT_RATE),{"dx":172,"ndy":7})),{"top":32,"sh":98}),(Kit.fit("ALERT KINDS  (from modules on this session)",w-16),(("custom",0,self._kinds),),{"sh":40+28*max(1,len(self.kinds()))}))
	def height(self,w):return Kit.Form.height(self.table(w),w)
	def build(self,g,x,y,w):
		if not ALERTS.loaded:ALERTS.load()
		self.store=({},{});self.c=Kit.Form(g,x,y,w,{"mute":ALERTS.mute,"banner":ALERTS.banner_on},self.table(w),self.store).c
	def _kinds(self,f,x,y):
		g,w,i,j=f.g,f.w,f.c,self.kinds();i.update(rows=[],dd=[])
		if not j:Kit.add_label(g,"No alerts yet: turn on a module that has some.",x+12,y+6,Kit.HUE_INFO)
		l=150;m=x+w-12-30-8-l;n=[]
		for o,a in enumerate(j):
			k=ALERTS.kinds[a];q,c=ALERTS.setting(a);d=y+4+28*o;r=Kit.fit(k["label"],196);s=Kit.add_check(g,r,x+12,d,q,"Raise the %s alert"%k["label"]);Kit.add_label(g,Kit.fit(k["owner"],m-8-(x+236)),x+236,d+2,Kit.HUE_INFO);Kit.art_button(g,self.store,"play%d"%o,Kit.ART_PLAY,x+w-12-30,d-2,None,"Play this alert's sound");b=[v for z,v in ALERT_SOUNDS];e=[A for A,B in ALERT_SOUNDS]
			if c not in b:b.append(c);e.append("Sound 0x%X"%c)
			n.append((a,b,e,b.index(c),m,d));i["rows"].append((a,s))
		for a,b,e,p,t,u in n:h=G.CreateDropDown(l,e,p);h.SetPos(t,u);g.Add(h);Kit.with_tip(h,"This alert's sound");i["dd"].append((a,h,b,p))
	def poll(self):
		c=self.c
		if c is None:return
		try:f=bool(c["mute"].IsChecked);e=bool(c["banner"].IsChecked)
		except Exception:f,e=ALERTS.mute,ALERTS.banner_on
		if f!=ALERTS.mute or e!=ALERTS.banner_on:
			ALERTS.mute,ALERTS.banner_on=f,e
			if not e:ALERTS.dismiss()
			ALERTS.save()
		for a,h in c["rows"]:
			try:v=bool(h.IsChecked)
			except Exception:continue
			if v!=ALERTS.setting(a)[0]:ALERTS.choose(a,on=v)
		if Kit.was_clicked(self.store,"test"):ALERTS.kind(Alerts.TEST_KEY,"Test",490,APP_NAME);ALERTS.last.pop((Alerts.TEST_KEY,"test"),None);ALERTS.raise_(Alerts.TEST_KEY,"This is how an alert looks and sounds.","warn",who="test")
		for n,j in enumerate(c["dd"]):
			a,g,b,d=j;i=Kit.dd_index(g,d)
			if i!=d and 0<=i<len(b):d=i;c["dd"][n]=(a,g,b,i);ALERTS.choose(a,sound=b[i])
			if Kit.was_clicked(self.store,"play%d"%n)and b[d]:API.PlaySound(int(b[d]))
def _norm_key(k):a=[c for c in str(k or "").strip().upper().replace(" ","").split("+")if c];b=[d[5:]if d.startswith("SDLK_")else d for d in a if d not in("CTRL","SHIFT","ALT")];return "+".join([e for e in("CTRL","SHIFT","ALT")if e in a]+b[-1:])
class Binds(object):
	VAR="VirtueAssistant_binds";REPEAT=.6;ARM_SECS=20.;REG_CAP=5000;armed_until=0.;reg={};saved={};last={};hooked=set();armed=False;picked=None;answer=None;loaded=False;scope=None;OWNER="Button binds";IDS_VAR="VirtueAssistant_binds_ids"
	@staticmethod
	def scoped(name,fn,*a):
		b=Binds.scope;Binds.scope=name
		try:return fn(*a)
		finally:Binds.scope=b
	@staticmethod
	def note(store,key,on_click,d,tip):
		a=Binds.scope or HOST.cur_owner
		if a is None:b=HOST.current();a=b.key if b is not None else "va"
		c="%s|%s"%(a,key)
		if len(Binds.reg)>=Binds.REG_CAP:Binds.reg.clear()
		Binds.reg[c]=(store,key,on_click);return c
	@staticmethod
	def wrap(a,handler):
		def b(*b):
			if Binds.armed:
				Binds.armed=False
				if time.time()<=Binds.armed_until:Binds.pick(a);return
			handler(*b)
		return b
	@staticmethod
	def load():
		if Binds.loaded or not safe(lambda:API.Player):return
		Binds.loaded=True;d=str(Kit.get_var(Binds.IDS_VAR,"")or "")!="2";b=0
		for e in str(Kit.get_var(Binds.VAR,"")or "").split(";"):
			if "="in e:
				c,a=e.rsplit("=",1)
				if d and c.split("|",1)[0]in("va","interface"):b+=1;continue
				a=_norm_key(a)
				if c and a:Binds.saved[c]=a;Binds.hook(a)
		if d:
			Kit.put_var(Binds.IDS_VAR,"2")
			if b:Binds.save();Kit.say("%s cleared (each window has its own now); bind them again in Settings > Hotkeys."%Kit.count(b,"button key"),Kit.HUE_INFO)
	@staticmethod
	def save():Kit.put_var(Binds.VAR,";".join("%s=%s"%a for a in sorted(Binds.saved.items())))
	@staticmethod
	def hook(a):
		if HOST.hotkey_on(a,Binds.OWNER,lambda:Binds.fire(a),"a button")is not False:Binds.hooked.add(a)
	@staticmethod
	def unhook(a):Binds.hooked.discard(a);HOST.hotkey_off(a,Binds.OWNER)
	@staticmethod
	def fire(a):
		b=time.time();c=Binds.last.get(a);Binds.last[a]=b
		if c is not None and 0<=b-c<Binds.REPEAT:return
		for e,f in Binds.saved.items():
			if f==a:
				r=Binds.reg.get(e)
				if r is None:return
				g,h,d=r;g[1][h]=True;HOST.poke()
				if d is not None:d()
				return
	@staticmethod
	def arm(on=True):
		Binds.armed=bool(on)
		if on:Binds.armed_until=time.time()+Binds.ARM_SECS;Kit.say("click a button to bind within %d s (Esc on the key window cancels)."%int(Binds.ARM_SECS),Kit.HUE_INFO)
	@staticmethod
	def pick(a):
		Binds.armed=False;Binds.picked=a;Binds.answer=None;import System
		def b():
			try:Binds.answer=str(API.RequestHotkey("Press the key for this button",30)or "")
			except Exception:Binds.answer=""
		t=System.Threading.Thread(System.Threading.ThreadStart(b));t.IsBackground=True;t.Start()
	@staticmethod
	def tick():
		if Binds.answer is None:return
		a,Binds.answer=_norm_key(Binds.answer),None;b,Binds.picked=Binds.picked,None
		if b is None or not a:return
		d=next((e[1]for e in KeysPage.rows()if e[0]==a and not(e[1]==Binds.OWNER and Binds.saved.get(b)==a)),None)
		if d is not None:Kit.say("%s is already %s's key; pick another."%(a,d),Kit.HUE_BAD);return
		c=Binds.saved.get(b)
		if c and c!=a:Binds.unhook(c)
		Binds.saved[b]=a;Binds.hook(a);Binds.save();Kit.say("%s bound."%a,Kit.HUE_GOOD);HOST.refresh_settings(KEYS_PAGE)
	@staticmethod
	def clear():
		for a in set(Binds.saved.values())|Binds.hooked:Binds.unhook(a)
		Binds.saved.clear();Binds.save()
class KeysPage(_Page):
	ROW=24
	@staticmethod
	def rows():
		b,e=[],set()
		for a,c,i in list(HOST.hotkey_list):b.append((_norm_key(a),c,i));e.add((_norm_key(a),c))
		for a,c in list(HOST.hotkeys_owned.items()):
			if(_norm_key(a),c)not in e:b.append((_norm_key(a),str(c),""))
		for d,f in list(HOST.services.items()):
			if not d.endswith(".hotkeys")or not callable(f):continue
			s=HOST.by_key.get(d[:-len(".hotkeys")]);c=s.title if s is not None else d[:-len(".hotkeys")]
			try:g=f()or[]
			except Exception:g=[]
			for h in g:
				try:b.append((_norm_key(h[0]),c,str(h[1])))
				except Exception:continue
		n={}
		for a,j,j in b:
			if a:n[a]=n.get(a,0)+1
		b=[(k,l,m,n.get(k,0)>1)for k,l,m in b if k];b.sort(key=lambda r:(r[0],r[1],r[2]));return b
	def height(self,w):return 64+self.ROW*max(1,len(self.rows()))
	def build(self,g,x,y,w):
		self.store=({},{});a=self.rows();k=64+self.ROW*max(1,len(a));Kit.add_section(g,x,y,w,k,"HOTKEYS  (every key Virtue Assistant listens to)");d=x+w+4
		for l,m,e,n,o in(("refresh",Kit.ART_PAGE,"Refresh",4,"Read the hotkeys again"),("bind_clear",Kit.ART_CLOSE,"Clear binds",28,"Unbind every button"),("bind",Kit.ART_PLAY,"Bind a button",28,"Click this, then a button in any window, then a key")):d-=16+35+Kit.text_w(e);Kit.art_button(g,self.store,l,m,d,y+n,e,o)
		b=len(set(t[0]for t in a if t[3]));Kit.add_label(g,("%s bound twice (shown in red)"%Kit.count(b,"key"))if b else "No key is bound twice.",x+12,y+32,Kit.HUE_BAD if b else Kit.HUE_INFO)
		if not a:Kit.add_label(g,"No module that is on has a hotkey.",x+12,y+56,Kit.HUE_INFO)
		p,f=x+12+160,x+12+160+150
		for q,(r,s,h,i)in enumerate(a):
			c=y+56+self.ROW*q;j=Kit.HUE_BAD if i else Kit.HUE_TEXT;Kit.add_label(g,Kit.fit(r,150),x+12,c,j);Kit.add_label(g,Kit.fit(s,140),p,c,j if i else Kit.HUE_TITLE)
			if h:Kit.add_label(g,Kit.fit(h,x+w-16-f),f,c,Kit.HUE_INFO)
		self.c=True
	def poll(self):
		if self.c is not None and Kit.was_clicked(self.store,"refresh"):HOST.refresh_settings(KEYS_PAGE)
		if self.c is not None and Kit.was_clicked(self.store,"bind"):Binds.arm(True)
		if self.c is not None and Kit.was_clicked(self.store,"bind_clear"):Binds.clear();HOST.refresh_settings(KEYS_PAGE)
ALERTS_PAGE,KEYS_PAGE="va.alerts","va.keys"
class WhatsNew(object):
	W=520
	def __init__(self):self.g=None;self.store=({},{});self.text=None
	def due(self):
		if self.text is None:self.text=whats_new()
		if not self.text:return False
		try:a=API.GetPersistentVar(WHATS_NEW_KEY,"",API.PersistentVar.Account)
		except Exception:return False
		return str(a or "")!=APP_VERSION
	def open(self):
		if self.due():Kit.on_client(lambda:Binds.scoped("va.news",self._build))
	def _build(self):
		M,W=Kit.MARGIN,self.W;a=[]
		for d in self.text:a+=Kit.wrap(d,W-2*M-24)or[""]
		b=16+20*len(a);H=M+30+Kit.GAP+b+M;self.store=({},{});g=G.CreateGump(True,True);Kit.add_window_frame(g,W,H);Kit.add_section(g,M,M,W-2*M,30);Kit.add_label(g,"WHAT'S NEW IN %s %s"%(APP_NAME.upper(),APP_VERSION),M+30,M+7,Kit.HUE_TITLE);Kit.art_button(g,self.store,"close",Kit.ART_CLOSE,W-M-54,M+4,None,"Close (shown once per version)");c=M+30+Kit.GAP;Kit.add_section(g,M,c,W-2*M,b)
		for i,e in enumerate(a):Kit.add_label(g,e,M+12,c+8+20*i,Kit.HUE_TEXT)
		f,h=Kit.screen();Kit.place(g,max(0,((f or 1024)-W)//2),max(0,((h or 768)-H)//3),W,H);G.AddGump(g);self.g=g
	def poll(self):
		g=self.g
		if g is None:return
		if not Kit.is_open(g)or Kit.was_clicked(self.store,"close"):self.close(True)
	def close(self,seen=False):
		g,self.g=self.g,None;Kit.dispose(g)
		if seen:API.SavePersistentVar(WHATS_NEW_KEY,APP_VERSION,API.PersistentVar.Account)
class ModuleSlot(object):
	def __init__(self,key,title,desc,a,interval):self.key=key;self.title=title;self.desc=desc;self.factory=a;self.interval=interval;self.api=self.lazy=self.broken=self.iv_fn=self.thread_want=None;self.enabled=self.default_on=self.running=self.busy=self.pending_stop=False;self.thread_due=self.on_client=self.has_thread=False;self.category="Other";self.next_due=self.worst_ms=0.;self.errors=set();self.error_times={};self.start_tok=None;self.page_err_at=0.;self.parts=self.aliases=();self.parts_on={};self.parts_running=set();self.folded=True
	def part(self,key):
		for p in self.parts:
			if p[0]==key:return p
		return
	def parts_wanted(self):return[a[0]for a in self.parts if self.parts_on.get(a[0])]
	def part_title(self,key):p=self.part(key);return "%s > %s"%(self.title,p[1])if p is not None else self.title
class PartView(object):
	def __init__(self,key,slot,part):self.key=key;self.slot=slot;self.part=part;self.title=slot.part_title(part);self.category=slot.category
	@property
	def running(self):return bool(self.slot.running and self.part in self.slot.parts_running)
	@property
	def enabled(self):return bool(self.slot.enabled and self.slot.parts_on.get(self.part))
	@property
	def api(self):return self.slot.api
	@property
	def lazy(self):return self.slot.lazy
	@property
	def broken(self):return self.slot.broken
class _KeyMap(dict):
	def __init__(self,host):dict.__init__(self);self.host=host
	def view(self,key):b,a=self.host.resolve(key);return PartView(key,b,a)if a is not None else None
	def __contains__(self,key):return dict.__contains__(self,key)or self.view(key)is not None
	def get(self,key,default=None):
		if dict.__contains__(self,key):return dict.__getitem__(self,key)
		v=self.view(key);return v if v is not None else default
	def __getitem__(self,key):
		if dict.__contains__(self,key):return dict.__getitem__(self,key)
		v=self.view(key)
		if v is None:raise KeyError(key)
		return v
def _error_where():
	try:
		import sys;a=sys.exc_info()[2]
		while a is not None and a.tb_next is not None:a=a.tb_next
		if a is None:return ""
		b=safe(lambda:os.path.basename(str(a.tb_frame.f_code.co_filename)),"")or ""
		if b.endswith("Module.py"):return " (%s line %d)"%(b,a.tb_lineno)
		return " (line %d)"%a.tb_lineno
	except Exception:return ""
class JLine(object):
	__slots__=("seq","text","low","name","hue","ticks","at","kind")
	def __init__(self,seq,text,name,hue,ticks,at,kind):self.seq,self.text,self.low,self.name=seq,text,text.lower(),name;self.hue,self.ticks,self.at,self.kind=hue,ticks,at,kind
class Journal(object):
	KEEP=60.;MAX_BACK=30.;lines=[];seen={};seq=0;read_at=0.;pass_id=-1;zero_seen=False;ATTACK_RE=re.compile(r"\*?\s*(.+?)\s+is attacking you",re.IGNORECASE)
	class Reader(object):
		__slots__=("last",)
		def __init__(self):self.last=Journal.seq
		def new(self,read=True):
			if read:Journal.update()
			b,self.last=self.last,Journal.seq
			if b>=Journal.seq:return[]
			a=[]
			for c in reversed(Journal.lines):
				if c.seq<=b:break
				a.append(c)
			a.reverse();return a
	@staticmethod
	def reader():Journal.update();return Journal.Reader()
	@staticmethod
	def update(force=False):
		o=HOST.pass_id
		if o==Journal.pass_id and not force:return
		Journal.pass_id=o;f=time.time();p=min(Journal.MAX_BACK,max(1.,f-Journal.read_at+1.))if Journal.read_at else Journal.MAX_BACK;Journal.read_at=f
		try:j=list(API.GetJournalEntries(p)or[])
		except Exception:j=[]
		k,g,h,q,i=Journal.seen,[],[],False,len(j)-1
		while i>=0:
			e=j[i];i-=1;c=i
			try:
				r=str(e.Text or "")
				if not r:continue
				try:l=int(e.Time.Ticks)
				except Exception:l=0
				a=(l,r,str(e.Name or ""))
				if l==0:h.append((a,e,c));Journal.zero_seen=True;continue
				if q or a in k:
					if not Journal.zero_seen:break
					q=True;continue
				g.append((a,e,c))
			except Exception:continue
		if h:
			m={}
			for a,e,c in h:m[a]=m.get(a,0)+1
			n={};y=f-p
			for b in reversed(Journal.lines):
				if b.at<y:break
				if b.ticks==0:s=(0,b.text,b.name);n[s]=n.get(s,0)+1
			u={}
			for a,e,c in h:
				v=u.get(a,0);u[a]=v+1
				if v<m[a]-n.get(a,0):g.append((a,e,c))
			g.sort(key=lambda t:t[2])
		else:g.reverse()
		w={}
		for a,e,c in g:
			if a[0]!=0:
				if a in w:continue
				w[a]=1
			try:Journal.seq+=1;k[a]=Journal.seq;Journal.lines.append(JLine(Journal.seq,a[1],a[2],int(e.Hue or 0),a[0],f,str(e.TextType or "")))
			except Exception:continue
		x=f-Journal.KEEP;d=Journal.lines
		if d and d[0].at<x:
			i=0
			while i<len(d)and d[i].at<x:b=d[i];k.pop((b.ticks,b.text,b.name),None);i+=1
			del d[:i]
	@staticmethod
	def since(t):
		Journal.update();a=[]
		for b in reversed(Journal.lines):
			if b.at<t:break
			a.append(b)
		a.reverse();return a
	@staticmethod
	def recent(secs):return Journal.since(time.time()-secs)
	@staticmethod
	def find(t,texts):
		if isinstance(texts,str):texts=(texts,)
		b=[c.lower()for c in texts]
		for a in Journal.since(t):
			for x in b:
				if x in a.low:return a
		return
class Picker(object):
	jobs=[];cuo=None;neutral=None;looked=False;CURSOR_TARGET=6983686
	@staticmethod
	def _tm():
		if not Picker.looked:
			Picker.looked=True
			try:import clr;clr.AddReference(API.GetType().Assembly);from ClassicUO import Client as CUO;from ClassicUO.Game.Managers import TargetType;Picker.cuo,Picker.neutral=CUO,TargetType.Neutral
			except Exception:Picker.cuo=None
		if Picker.cuo is None:return
		try:return Picker.cuo.Game.UO.World.TargetManager
		except Exception:return
	@staticmethod
	def ask(timeout,fn,owner=None):
		for j in Picker.jobs:j["cancel"]=True
		if owner is None:owner=HOST.owner_key()
		Picker.jobs.append({"t":float(timeout),"fn":fn,"until":0.,"d":None,"got":None,"block":False,"cancel":False,"owner":owner});HOST.poke()
	@staticmethod
	def due():
		for j in Picker.jobs:
			if j["d"]is None or j["got"]is not None:return True
		return False
	@staticmethod
	def _done(j,serial):
		if j in Picker.jobs:Picker.jobs.remove(j)
		try:j["fn"](int(serial or 0))
		except Exception as a:Kit.say("target error: %s%s"%(a,_error_where()),Kit.HUE_BAD)
	@staticmethod
	def tick():
		if not Picker.jobs:return
		b=Picker._tm()
		for a in list(Picker.jobs):
			if a["block"]:continue
			if a["d"]is None:
				if a["cancel"]:Picker._done(a,0);continue
				if b is None:a["block"]=True;continue
				try:
					from System import Action
					def d(obj,j=a):
						try:j["got"]=(int(obj.Serial or 0)if obj is not None else 0)
						except Exception:j["got"]=0
					a["d"]=Action[object](d);b.SetTargeting(a["d"],Picker.CURSOR_TARGET,Picker.neutral);a["until"]=time.time()+a["t"]
				except Exception:a["d"],a["block"]=None,True
				continue
			if a["got"]is not None:Picker._done(a,a["got"]);continue
			try:c=bool(b.IsCurrentTargetingAction(a["d"]))
			except Exception:c=False
			if not c:Picker._done(a,0)
			elif a["cancel"]or time.time()>=a["until"]:
				try:b.CancelTarget()
				except Exception:pass
				Picker._done(a,0)
	@staticmethod
	def drop(owner=None):
		a=[e for e in Picker.jobs if owner is None or e.get("owner")==owner]
		if not a:return
		for j in a:Picker.jobs.remove(j)
		b=Picker._tm();c=[f["d"]for f in a if f["d"]is not None and f["got"]is None]
		if b is not None and c:
			def d():
				for d in c:
					if b.IsCurrentTargetingAction(d):b.CancelTarget()
			safe(lambda:Kit.on_client(d,fallback=False))
		for j in a:Picker._done(j,0)
	@staticmethod
	def run_blocking():
		for j in[b for b in Picker.jobs if b["block"]]:Picker.jobs.remove(j);a=0 if j["cancel"]else int(safe(lambda:API.RequestTarget(j["t"]),0)or 0);Picker._done(j,a)
def _first(e):return e[0]
class _Memo(object):
	def __init__(self,raw):self.__dict__["raw"]=raw
	def __getattr__(self,name):v=getattr(self.__dict__["raw"],name);self.__dict__[name]=v;return v
	def __setattr__(self,name,value):setattr(self.__dict__["raw"],name,value);self.__dict__.pop(name,None)
	def __int__(self):return int(self.__dict__["raw"].Serial)
class Host(object):
	def __init__(self):
		self.slots=[];self.by_key=_KeyMap(self);self.old_map={};self.cur_part=self.cur_owner=self.config=self.hub=self.grid=self.profile_req=self.alone=None;self.hurt_hp=self._me=self._want_raw=self.attack_rd=None;self.stack=[];self.harm_conf=(None,0,0.);self.quitting=self.shut=self.ui_busy=self.poked=self.prefs_frozen=False;self.in_hop=self.pass_poked=self.pass_all=self.poke_user=self.draining=False;self.alive_at=0.;self.poke_keys=set();self.pass_keys=self.NO_KEYS;self.off_q=[];self._stop_fi=None;self.look=self.LOOKAHEAD;import threading;self._drain_lk=threading.Lock();self.ui_next=self.dock_next=self._claim_len=self.hurt_until=self.input_at=0.;self.attacked_until=self.prefs_at=0.;self.hurt_who=0;self.prefs_due=False;self.docks=[];self.services={};self.hotkeys_owned={};self.prefs={};self.cursor_claim=(None,0.);self.hk_fns={};self.hk_wait={};self.gump_exp={};self.services["gump.expect"]=self.gump_expect;self.foe_seen=(0.,None);self.client_idles=self.pass_id=0;self._me_pid=self._mob_pid=self._one_pid=-1;self._mob_list=();self._one={};self._pack={};self._mob_at=0.;self._pack_v=0;self._pack_keys=set();self._pack_hook={"on":False};self._pack_fn=self._pack_event;self.active=[];self.client_run=[];self._pass_fn=self._client_pass;self._want_set=frozenset();self.told,self._zone_held,self._zone_was_d,self._zone_bring=set(),set(),None,{};self.load_jobs=[];self.hotkey_list=[];self.pages=[];self.held_on=set()
		for a,b,c in((ALERTS_PAGE,"Alerts",AlertsPage()),(KEYS_PAGE,"Hotkeys",KeysPage())):s=ModuleSlot(a,b,"",None,1.);s.api=c.api();self.pages.append(s)
		self.whats_new=WhatsNew()
	def _tell(self,msg):
		if msg in self.told:return
		if len(self.told)>50:self.told.clear()
		self.told.add(msg);API.SysMsg(msg,Kit.HUE_BAD)
	def _refresh_active(self):a=[b for b in self.slots if b.running];self.active=a;self.client_run=[c for c in a if c.on_client]
	NO_KEYS=frozenset()
	def poke(self,key=None,user=True):
		if self.draining:
			if key is None:self.pass_all=self.pass_poked=True
			else:self.pass_keys=self.pass_keys|frozenset((key,key.partition(".")[0]))
			if user:self.pass_poked=True;self.input_at=time.time()
			if user or key is None:self.ui_next=0.
			return
		if key is None:self.poked=True
		else:a=self.poke_keys;a.add(key);a.add(key.partition(".")[0])
		if user:self.poke_user=True;self.input_at=time.time()
	def click_key(self):a=self.current();return a.key if a is not None else None
	INPUT_FAST=1.;PAGE_EVERY=.25
	def poll_due(self,gate,every=None):
		a=time.time()
		if every is not None and every<=UI_TICK:return True
		if not Kit.clicks_seen:return True
		b=a-self.input_at<=self.INPUT_FAST or 0<=gate[0]-a>2.
		if not b:
			p=SNAP.pressed()
			if p is not False:
				if p:self.input_at=a
				b=True
			else:b=Client.typing()
		if b or a>=gate[0]:gate[0]=a+(every if every is not None else self.PAGE_EVERY);return True
		return False
	def alert_kind(self,key,label,a=None):s=self.current();return ALERTS.kind(key,label,a,s.title if s is not None else APP_NAME)
	def alert(self,key,text,level="warn",sound=None,ping=None,who=None):s=self.current();return ALERTS.raise_(key,text,level,sound,ping,who,s.title if s is not None else APP_NAME)
	def guarded(self):return GUARD.guarded()
	def guard_area(self):return GUARD.area()
	def hotkey_note(self,a,owner,what=""):
		k=_norm_key(a);self.hotkey_list=[b for b in self.hotkey_list if not(_norm_key(b[0])==k and b[1]==owner)];self.hotkey_list.append((k,str(owner),str(what or "")))
		if k not in self.hotkeys_owned:self.hotkeys_owned[k]=str(owner)
	def hotkey_on(self,e,owner,fn,what=""):
		k,owner=_norm_key(e),str(owner)
		if not k:return False
		b=self.current();c=(owner,fn,b.key if b is not None else None,str(what or ""));a=self.hk_fns.get(k)
		if a is not None and a[0]!=owner:d=[f for f in self.hk_wait.get(k,())if f[0]!=owner];d.append(c);self.hk_wait[k]=d;Kit.say("%s is already %s's key; %s can't use it until that lets it go."%(k,a[0],owner),Kit.HUE_BAD);return
		if a is None:
			try:API.OnHotKey(k,self._hk_fire(k))
			except Exception:return False
		self._hk_take(k,c);return True
	def _hk_take(self,k,ent):self.hk_fns[k]=ent;self.hotkey_note(k,ent[0],ent[3]);self.hotkeys_owned[k]=ent[0]
	def _hk_fire(self,k):
		def a(*b):
			a=self.hk_fns.get(k)
			if a is not None:a[1]()
		return a
	def hotkey_off(self,d,owner):
		k,owner=_norm_key(d),str(owner);b=self.hk_fns.get(k);a=[e for e in self.hk_wait.get(k,())if e[0]!=owner]
		if a:self.hk_wait[k]=a
		else:self.hk_wait.pop(k,None)
		self.hotkey_drop(k,owner)
		if b is None or b[0]!=owner:return
		if a:
			c=a.pop(0)
			if not a:self.hk_wait.pop(k,None)
			self._hk_take(k,c);Kit.say("%s is %s's key now."%(k,c[0]),Kit.HUE_INFO);return
		self.hk_fns.pop(k,None)
		with Kit.quiet:API.OnHotKey(k)
	def hotkey_drop(self,c,owner=None):
		k=_norm_key(c);self.hotkey_list=[d for d in self.hotkey_list if not(_norm_key(d[0])==k and(owner is None or d[1]==owner))];a=[f[1]for f in self.hotkey_list if _norm_key(f[0])==k];b=self.hotkeys_owned.get(k)
		if b is None or owner is None or b==str(owner):
			if a:self.hotkeys_owned[k]=a[0]
			else:self.hotkeys_owned.pop(k,None)
	def page_slot(self,key):
		s=self.resolve(key)[0]
		if s is None:return next((a for a in self.pages if a.key==key),None)
		return s
	def resolve(self,key):
		s=dict.get(self.by_key,key)
		if s is not None:return s,None
		m=self.old_map.get(key)
		if m is None and "."in str(key):m=str(key).split(".",1)
		if m is not None:
			s=dict.get(self.by_key,m[0])
			if s is not None and s.part(m[1])is not None:return s,m[1]
		return None,None
	def _note_parts(self,s,default_on,category,parts,aliases):
		s.default_on=bool(default_on);s.category=str(category or "Other");s.parts=tuple(tuple(b)for b in(parts or()));s.aliases=tuple(str(c)for c in(aliases or()))
		for p in s.parts:
			for a in(p[4]if len(p)>4 else()):self.old_map[str(a)]=(s.key,p[0])
			if p[0]not in s.parts_on:s.parts_on[p[0]]=False
	def part_on(self,part,a=None):
		if a is None:b=self.current();a=b.key if b is not None else None
		s=dict.get(self.by_key,a);return bool(s is not None and s.parts_on.get(part))
	def owner_key(self):
		a=self.current()
		if a is None:return
		if self.cur_owner is not None and a.parts:return self.cur_owner
		return a.key
	def _parts_fill(self,s):
		if s.parts and not s.parts_wanted():
			for p in[a[0]for a in s.parts if a[3]]or[s.parts[0][0]]:s.parts_on[p]=True
	def _part_notify(self,s):
		if not s.running or s.api is None or not s.api.get("parts"):return
		a=s.busy;self._enter(s)
		try:b=set(s.parts_wanted());Kit.on_client(lambda:s.api["parts"](b))
		except Exception as c:self.report(s,c)
		finally:self._leave(s);s.busy=a
	def part_set(self,a,part,on):
		s=dict.get(self.by_key,a)
		if s is None or s.part(part)is None:return
		on=bool(on)
		if s.parts_on.get(part)==on:
			if on and not s.enabled:self.enable(a)
			return
		s.parts_on[part]=on
		if not on:s.error_times.pop(part,None)
		if on and not s.enabled:self.enable(a)
		elif not on and not s.parts_wanted():self.disable(a)
		else:self.save_prefs();self._part_notify(s)
		self.refresh_settings(a)
	def alarm_up(self):return bool(ALERTS.shown and ALERTS.alarm)
	def typing(self):return Client.typing()
	def release_typing(self):Typing.release()
	def grid_size(self):return max(8,min(512,self.pref_int("grid",GRID_DEFAULT)))
	def grid_shown(self):return self.grid is not None and self.grid.shown
	def grid_toggle(self):
		if self.grid is not None:self.grid.toggle();self.prefs["grid_on"]="1"if self.grid_shown()else "0";self.save_prefs()
		return self.grid_shown()
	def set_dark(self,on):
		on=bool(on);self.prefs["dark"]="1"if on else "0";self.save_prefs();Kit.set_dark(on);Kit.retint()
		for k,d in list(self.docks):
			try:s=d["state"]()if d.get("redraw")is not None else None
			except Exception:s=None
			if s in("open","minimized"):safe(d["redraw"])
		for w in list(Kit._wins.values()):
			if Kit.is_open(w.win.get(w.gkey)):w.queue.add("redraw")
		for a,b in list(self.services.items()):
			if a.startswith("look."):safe(b)
		self.refresh_settings(LAYOUT_OWNER);self.poke();Kit.say("Dark mode on."if on else "Dark mode off.",Kit.HUE_GOOD)
	def dock_wanted(self,key):return key in self._dock_want()
	def _dock_want(self):
		a=self.prefs.get("dock_want","")or ""
		if a!=self._want_raw:self._want_raw=a;self._want_set=frozenset(b for b in str(a).split(",")if b)
		return self._want_set
	def dock_want_set(self,key,on):
		a=self._dock_want()
		if bool(on)==(key in a):return
		self.prefs["dock_want"]=",".join(sorted(a|{key}if on else a-{key}));self.save_prefs()
	def dock_forget(self,key):self.dock_want_set(key,False)
	def gump_expect(self,gid,secs=5.):
		gid=int(gid or 0)
		if not gid:return
		a=time.time();b=dict((d,c)for d,c in list(self.gump_exp.items())if 0<c-a<=GUMP_EXPECT_MAX);b[gid]=a+max(0.,min(float(secs),GUMP_EXPECT_MAX));self.gump_exp=b
	def gump_expected(self,gid,now):t=self.gump_exp.get(gid);return t is not None and 0<t-now<=GUMP_EXPECT_MAX
	def dock_to_bar(self,key,title=None):
		if LAYOUT.holds(key):return False
		self.dock_want_set(key,True);d=dict(self.docks).get(key);a=self.bar_alive()
		if d is not None:
			b=d.get("dock")if a else(d.get("minimize")or d.get("dock"))
			if b:safe(b)
			title=title or d.get("title")
		if not a:self.dock_note(title or key)
		self.dock_next=0.;return a
	def dock_note(self,title):API.SysMsg("%s: minimized until the Action Bar opens; then it folds into its tray."%title,Kit.HUE_INFO)
	def dock_add(self,key,hooks):
		self.dock_remove(key);self.docks.append((key,hooks));a=hooks.get("gump")
		if a is not None:self.layout_add(key,a,hooks.get("title"),hooks)
	def dock_remove(self,key):self.docks=[a for a in self.docks if a[0]!=key];self.layout_remove(key)
	def layout_add(self,key,b,title=None,hooks=None):a=self.current();c=(a.key,self.cur_part if a.parts else None)if a is not None else None;LAYOUT.add(key,b,title,hooks,c)
	def layout_remove(self,key):LAYOUT.remove(key)
	def layout_slot(self,key):
		key=str(key)
		if not LAYOUT.holds(key):return
		a=LAYOUT.fitted.get(key)
		if a is not None and a.get("told")is not None:return a["told"]
		b=LAYOUT.placed.get(key);return(b[2],b[3])if b is not None else None
	def layout_rect(self,key):
		key=str(key)
		if not LAYOUT.holds(key):return
		a=LAYOUT.placed.get(key);return tuple(a)if a is not None else None
	def layout_holds(self,key):return LAYOUT.holds(key)
	def layout_need(self,key,w=None,h=None):LAYOUT.need(key,w,h)
	def layout_base(self,key):return LAYOUT.zone_base(key)
	def layout_locked(self,key):return LAYOUT.locked(key)
	def layout_arrange(self,on=None):LAYOUT.set_arrange((not LAYOUT.arrange)if on is None else on)
	def layout_arranging(self):return LAYOUT.arrange
	def layout_in_use(self):return bool(LAYOUT.assign)and LAYOUT.enabled
	def layout_pair(self,a,b):return LAYOUT.pair_below(a,b)
	def layout_refit(self):LAYOUT.dirty=LAYOUT.fresh=True
	@staticmethod
	def suite_alive():
		try:return time.time()-float(API.GetSharedVar(ALIVE_KEY)or 0)<3.
		except Exception:return False
	def bar_alive(self):
		if VA_ALONE:return False
		try:a=float(API.GetSharedVar(ConfigWindow.LINK_ALIVE)or 0)
		except Exception:a=0.
		return time.time()-a<=ConfigWindow.LINK_STALE
	def dock_tick(self):
		a=time.time()
		if a<self.dock_next and self.dock_next-a<=.25:return
		self.dock_next=a+.25;Binds.load();Binds.tick();b=self._dock_want();c,e=[],[];self.zone_up_tick()
		for k,d in self.docks:
			if LAYOUT.holds(k):continue
			try:s=d["state"]()
			except Exception:s=None
			if s=="docked":
				if k not in b:self.dock_want_set(k,True)
				e.append(d)
			elif s=="open":
				if k in b:self.dock_want_set(k,False)
			elif s=="minimized"and k in b:c.append(d)
		if not c and not e:return
		if self.bar_alive():
			for d in c:safe(d.get("dock"))
		else:
			for d in e:safe(d.get("undock"))
	ZONE_WAS_VAR="Layout_zone_was"
	def _zone_was(self):
		d=self._zone_was_d
		if d is None:d=self._zone_was_d=dict(a.split("=",1)for a in Kit.get_var(self.ZONE_WAS_VAR).split(",")if "="in a)
		return d
	def _zone_was_save(self):Kit.put_var(self.ZONE_WAS_VAR,",".join("%s=%s"%a for a in sorted(self._zone_was_d.items())))
	def zone_up_tick(self):
		if VA_ALONE:return
		c,b=self._zone_held,self._zone_was()
		for k,d in self.docks:
			a=LAYOUT.holds(k);e=a!=(k in c)
			if e:
				if a:c.add(k)
				else:c.discard(k)
			try:s=d["state"]()if(a or k in b)else None
			except Exception:s=None
			if a and s in("minimized","docked"):
				if k not in b:b[k]="d"if(s=="docked"or self.dock_wanted(k))else "m";self._zone_was_save()
				safe(d.get("show"));continue
			if not a and k in b and s is not None:
				v=b.pop(k);self._zone_was_save()
				if v=="d":self.dock_to_bar(k,d.get("title"))
				else:safe(d.get("minimize"))
				continue
			if a and s is None and not LAYOUT.arrange and time.time()>=self._zone_bring.get(k,0.):
				f=d.get("show")or d.get("on")
				if f is not None:self._zone_bring[k]=time.time()+2.;safe(f)
			if e and d.get("redraw")is not None and s!="docked":safe(d.get("redraw"))
	TWICE="%s: %s loaded twice (module key \"%s\"); skipped the second copy."
	def add(self,key,title,desc,a,interval,default_on=False,category=None,parts=(),aliases=()):
		s=dict.get(self.by_key,key)
		if s is not None and s.lazy is not None:s.lazy=None;s.title,s.desc,s.factory,s.interval=title,desc,a,interval;self._note_parts(s,default_on,category,parts,aliases)
		elif s is not None:API.SysMsg(self.TWICE%(APP_NAME,title,key),Kit.HUE_BAD);return s
		else:s=ModuleSlot(key,title,desc,a,interval);self._note_parts(s,default_on,category,parts,aliases);self.slots.append(s);self.by_key[key]=s
		try:s.api=a()
		except Exception as b:s.broken=str(b)+_error_where();Kit.say("couldn't load %s (%s)."%(title,s.broken),Kit.HUE_BAD)
		self._arm(s)
		if VA_ALONE and self.alone is None:self.run_alone(s)
		return s
	@staticmethod
	def _arm(s):a=s.api;s.on_client=bool(a and a.get("client_tick"));s.iv_fn=a.get("interval")if a else None;s.has_thread=bool(a)and "thread_tick"in a;s.thread_want=a.get("thread_wanted")if a else None
	def add_lazy(self,key,title,desc,path,interval,default_on=False,category=None,parts=(),aliases=()):
		if dict.__contains__(self.by_key,key):return dict.__getitem__(self.by_key,key)
		s=ModuleSlot(key,title,desc,None,interval);self._note_parts(s,default_on,category,parts,aliases);s.lazy=path;self.slots.append(s);self.by_key[key]=s;return s
	def request_load(self,s):
		if s is None or s.lazy is None:return False
		if s not in self.load_jobs:self.load_jobs.append(s)
		self.poke();return True
	def _run_load_jobs(self):
		if not self.load_jobs or self.stack:return
		s=self.load_jobs.pop(0);a=self.load(s)
		if a and s.enabled and not s.running and not s.pending_stop:self.start(s)
		elif not a and s.enabled:s.enabled=False;self.held_on.add(s.key);self.save_prefs()
		if self.config is not None:self.config.loaded(s.key)
	def load(self,s):
		if s is None:return False
		if s.lazy is not None:
			a=s.lazy
			try:
				d=compile(_read_text(a),a,"exec");exec(d,globals())
				if s.lazy is not None:raise Exception("the file's HOST.add line didn't run")
			except Exception as b:s.lazy=None;c=getattr(b,"lineno",None);e=(" (%s line %s)"%(os.path.basename(a),c))if c else _error_where();s.api,s.broken=None,"%s%s"%(getattr(b,"msg",None)or b,e);Kit.say("couldn't load %s (%s)."%(s.title,s.broken),Kit.HUE_BAD)
		return s.api is not None
	def current(self):return self.stack[-1]if self.stack else None
	def stopping(self):
		if self.quitting:return True
		try:return bool(API.StopRequested)
		except Exception:return True
	def aborting(self):
		if self.stopping():return True
		if self.client_idles>1 and Client.on_client_thread():return True
		s=self.current();return s is not None and(s.pending_stop or not s.enabled)
	def idle(self,b):
		if Client.on_client_thread():self.client_idles+=1;return self.client_idles<=1 and not self.aborting()
		c=time.time()+max(0.,b)
		while not API.StopRequested:
			if self.aborting():return False
			self.drain();self.run_due()
			if self.aborting():return False
			a=c-time.time()
			if a<=0 or a>b+1.:return True
			API.Pause(min(HOST_TICK,a))
		return False
	def _enter(self,s):s.busy=True;self.stack.append(s)
	def _leave(self,s):
		a=self.stack
		if a and a[-1]is s:a.pop()
		elif s in a:a.remove(s)
		s.busy=False
	def report(self,s,b,what=None,part=None):
		a=str(b)+_error_where()
		if a not in s.errors:s.errors.add(a);Kit.say("%s error (still running): %s"%(what or s.title,a),Kit.HUE_BAD)
		self.count_error(s,what,part)
	def count_error(self,s,what=None,part=None,page=False):
		a=time.time()
		if page:
			if 0<=a-s.page_err_at<1.:return
			s.page_err_at=a
		b=[c for c in s.error_times.get(part,())if 0<=a-c<ERROR_SECS];b.append(a);s.error_times[part]=b
		if len(b)<MAX_MODULE_ERRORS or not s.enabled:return
		s.error_times.pop(part,None);Kit.say("%s kept failing and was switched off."%(what or s.title),Kit.HUE_BAD)
		if part is not None and s.parts and s.parts_on.get(part):self.part_set(s.key,part,False)
		else:self.disable(s.key)
	def start(self,s):
		if s.running or self.stopping()or not self.load(s):return
		s.errors,s.error_times=set(),{};s.pending_stop=False;self._enter(s);c=s.start_tok=object();import threading;b=threading.Lock();a={"began":False,"ended":False,"undone":False}
		def d():
			with b:
				if a["undone"]:return
				a["undone"]=True
			safe(lambda:s.api["stop"]());safe(lambda:self._unclaim(s))
		def e():
			with b:
				if s.start_tok is not c or not s.running:return
				a["began"]=True
			try:s.api["start"]()
			finally:
				with b:a["ended"]=True;e=s.start_tok is not c or not s.running
				if e:d()
		try:s.running=True;self._arm(s);self._refresh_active();self.client_idles=0;Kit.on_client(e)
		except Exception as f:
			with b:s.start_tok=None;s.running=False;g=a["began"]and not a["ended"]
			h=str(f)+_error_where();Kit.say("couldn't start %s (%s)."%(s.title,h),Kit.HUE_BAD)
			if not g:d()
			s.enabled=False;self.save_prefs()
		finally:self._leave(s);self._refresh_active()
		s.next_due=0.
	def _stop(self,s):
		s.pending_stop=False
		if not s.running:return
		self._unclaim(s);self._enter(s)
		try:s.api["stop"]()
		except Exception:pass
		finally:s.running=False;self._leave(s);self._refresh_active()
	def _unclaim(self,s):
		a=[s.key]+[g for f in s.parts for g in f[4]]
		for k in a+[h[0]for h in s.parts]:Picker.drop(k)
		if self.cursor_claim[0]in a:self.cursor_claim=(None,0.)
		for k,d in list(self.hk_wait.items()):
			for w in[i for i in d if i[2]==s.key]:self.hotkey_off(k,w[0])
		for k,c in list(self.hk_fns.items()):
			if c[2]==s.key:self.hotkey_off(k,c[0])
		e=s.key+"."
		for b in list(Kit._hooks):
			if b in a or str(b).startswith(e):Kit.unhook(b)
	def tick(self,s,b="tick"):
		s.busy=True;a=self.stack;a.append(s);self.client_idles=0;f=time.time()
		try:s.api[b]()
		except Exception as g:
			if not self.stopping():self.report(s,g)
		finally:
			if a and a[-1]is s:a.pop()
			elif s in a:a.remove(s)
			s.busy=False;c=time.time();d=(c-f)*1000.;e=s.worst_ms*.98;s.worst_ms=d if d>e else e
		if b=="tick":s.next_due=c+Host._ask(s.iv_fn,s.interval);s.thread_due=s.has_thread and Host._ask(s.thread_want,True,bool)
		if s.pending_stop:self._stop(s)
	@staticmethod
	def _ask(fn,default,cast=None):
		if fn is None:return default
		try:v=fn();return cast(v)if cast else(v or default)
		except Exception:return default
	def enable(self,key):
		s,a=self.resolve(key)
		if s is None:return
		if self.off_q:self.off_q=[b for b in self.off_q if b[1:]!=(s.key,a)]
		if a is not None:self.part_set(s.key,a,True);return
		self._parts_fill(s)
		if s.lazy is not None and Client.on_client_thread():s.enabled=True;self.save_prefs();self.request_load(s);return
		if not self.load(s):return
		s.enabled=True
		if s.running and s.pending_stop:s.pending_stop=False
		self.save_prefs();self.start(s)
	def show_settings(self,key):
		if self.config is not None:self.config.show_settings(key)
	def refresh_settings(self,key):
		if self.config is not None:s,a=self.resolve(key);self.config.refresh(s.key if s is not None else key)
	def disable(self,key):
		s,a=self.resolve(key)
		if s is None:return
		if self.shut or self.stopping():return
		if self.draining:self.off_q.append((key,s.key,a));return
		if a is None and s.parts and self.cur_part is not None and self.current()is s and s.parts_on.get(self.cur_part):a=self.cur_part
		if a is not None:self.part_set(s.key,a,False);return
		self.held_on.discard(s.key);s.enabled=False;self.save_prefs()
		if s.running:
			s.pending_stop=True
			if not s.busy:self._stop(s)
	def run_due(self):
		if self.shut:return
		if self.profile_req is not None and not self.stack:f,self.profile_req=self.profile_req,None;self.profile_job(f);return
		a,self.poked=self.poked,False;self.pass_id+=1;b,e=self.poke_keys,self.poke_user
		if b:self.poke_keys=set()
		else:b=self.NO_KEYS
		self.poke_user=False;self.pass_keys=b
		if a or e:self.ui_next=0.
		c=time.time()
		if self.prefs_due:self.prefs_flush()
		if a or b or self._client_due(c):
			self.pass_poked,self.pass_all=a or e,a
			try:Kit.on_client(self._pass_fn)
			except Exception as g:
				if not self.stopping():self._tell("%s: pass error: %s"%(APP_NAME,g))
			a,b=self.pass_all,self.pass_keys
			if self.stopping():return
			if self.off_q:
				q,self.off_q=self.off_q,[]
				for h in q:self.disable(h[0])
			c=time.time()
		if Picker.jobs:Picker.run_blocking()
		for s in self.active:
			if s.pending_stop:
				if s.busy:continue
				self._stop(s)
			elif s.busy or not s.running:continue
			elif not s.on_client and(a or s.key in b or c>=s.next_due or s.next_due-c>self.CLOCK_BACK):self.tick(s)
			elif s.thread_due:s.thread_due=False;self.tick(s,"thread_tick")
			else:continue
			if self.stopping():return
			self.drain()
		if self.load_jobs and not self.stack:self._run_load_jobs()
		d=self.config
		if d is not None and d.prof_stale and not self.stack:d.refresh_profiles()
	LOOKAHEAD=HOST_TICK+.035;CLOCK_BACK=60.;EARLY=.008;MOB_AGE=.1;PACK_CAP=6000;PREFS_EVERY=1.
	def _client_due(self,now):
		if now>=self.ui_next or Picker.jobs or(Kit.pending and self.config is not None):return True
		if self.ui_next-now>UI_TICK and SNAP.pressed():self.ui_next=now;return True
		if self.ui_next-now>1.:self.ui_next=now;return True
		a=now+self.look
		for s in self.client_run:
			if a>=s.next_due:return True
			if s.next_due-now>self.CLOCK_BACK:s.next_due=now;return True
		return False
	def drain(self,hop=False):
		a=self._drain_lk
		if not a.acquire(False):return
		try:
			if hop:self.draining=True
			API.ProcessCallbacks()
		except Exception:pass
		finally:
			if hop:self.draining=False
			a.release()
	FRAME_MIN=1./60;NAP_MIN=.002
	def nap(self,began):
		a=time.time()
		if(self.poked or self.poke_keys or self.poke_user or(Kit.pending and self.config is not None)or Picker.due()or 0<=a-self.input_at<=self.INPUT_FAST):self.look=self.EARLY;return max(self.NAP_MIN,self.FRAME_MIN-max(0.,a-began))
		self.look=self.LOOKAHEAD;return HOST_TICK
	def _stop_free(self):
		f=self._stop_fi
		if f is None:
			try:from System.Reflection import BindingFlags;f=API.GetType().GetField("_onStopScheduled",BindingFlags.NonPublic|BindingFlags.Instance)
			except Exception:f=None
			f=self._stop_fi=f or False
		if f is False:return False
		try:return not f.GetValue(API)
		except Exception:return False
	def _drop_offs(self):
		q,self.off_q=self.off_q,[]
		for e in q:
			s=dict.get(self.by_key,e[1])
			if s is None:continue
			if e[2]is not None:s.parts_on[e[2]]=False
			if e[2]is None or not s.parts_wanted():s.enabled=False;self.held_on.discard(s.key)
	def _client_pass(self,poked=None):
		self.in_hop=True
		try:
			self.client_idles=0
			if self._stop_free():self.drain(True)
			if self.stopping():return
			if poked is None:poked=self.pass_all
			c=self.pass_keys;d=set(f[1]for f in self.off_q if f[2]is None)if self.off_q else()
			if Kit._texts_sweep:Kit._prune_texts()
			self.ui_pending();self.fight_sample(time.time())
			if Picker.jobs:
				try:Picker.tick()
				except Exception as a:self._tell("%s: target cursor error: %s"%(APP_NAME,a))
			b=time.time()
			for s in self.client_run:
				if s.running and not s.busy and not s.pending_stop and s.key not in d and(poked or s.key in c or b+self.EARLY>=s.next_due or s.next_due-b>self.CLOCK_BACK):
					self.tick(s)
					if self.stopping():return
			self.ui_tick()
			if ALERTS.pending:
				try:ALERTS.tick(time.time())
				except Exception as a:self._tell("%s: alert error: %s%s"%(APP_NAME,a,_error_where()))
		finally:self.in_hop=False
	def claim_cursor(self,key,a):self._claim_len=max(0.,a);self.cursor_claim=(key,time.time()+self._claim_len)
	def release_cursor(self,key):
		if self.cursor_claim[0]==key:self.cursor_claim=(None,0.)
	def cursor_busy(self,key=None):
		if Picker.jobs:return "pick"
		a,b=self.cursor_claim;return a if a is not None and a!=key and 0<b-time.time()<=self._claim_len+.05 else None
	def cursor_ok(self,key,kind="any"):
		if self.cursor_busy(key)is not None:return False
		try:return bool(API.HasTarget(kind))
		except Exception:return False
	def harm_ok(self,serial,key,title,harmful=None,again="press again to confirm",odd=False,now=None):
		if harmful is None:
			try:harmful=bool(API.HasTarget("harmful"))
			except Exception:harmful=False
		if not harmful:return True
		a=self.guarded()
		if a is False:return True
		try:m=API.FindMobile(serial)if serial else None
		except Exception:m=None
		b=Kit.noto_name(m)if m is not None else("odd"if odd and serial else "unknown")
		if b not in HARM_NOTO:return True
		now=time.time()if now is None else now;c=self.harm_conf
		if c[0]==key and c[1]==serial:
			d=now-c[2]
			if 0<=d<HARM_DOUBLE:return False
			if 0<=d<=HARM_SECS:self.harm_conf=(None,0,0.);return True
		self.harm_conf=(key,serial,now)
		try:e=str(m.Name or "")if m is not None else ""
		except Exception:e=""
		f="%s is %s"%(e or "they","green"if b=="ally"else "blue")if m is not None else "your target is not a mobile";API.SysMsg("%s: %s and you %s in a guard zone: %s."%(title,f,"are"if a else "may be",again),Kit.HUE_BAD)
		if m is not None:API.HeadMsg("* %s *"%again,serial,34)
		return False
	def guard_hold(self):
		try:g=GUARD.guarded()
		except Exception:g=None
		return "guard"if g is True else "unknown"if g is None else None
	def foe_near(self):
		b=time.time();c,a=self.foe_seen
		if 0<=c-b<=FOE_EVERY:return a
		def d():
			try:a=int(self.me().Serial)
			except Exception:a=0
			try:
				for m in self.mobiles(FOE_RANGE):
					try:
						if int(m.Serial)==a or m.IsRenamable:continue
						n=int(m.Notoriety)
						if n in FOE_NOTO or(n in FOE_WAR_NOTO and m.InWarMode):return str(m.Name or "")or "?"
					except Exception:continue
			except Exception:pass
			return
		try:a=Kit.on_client(d)
		except Exception:a=None
		self.foe_seen=(b+FOE_EVERY,a);return a
	def fight_sample(self,now):
		try:p=self.me();a=int(p.Serial);b=int(p.Hits)
		except Exception:return
		if a!=self.hurt_who:self.hurt_hp=None;self.hurt_who=a
		if self.hurt_hp is not None and b<self.hurt_hp:self.hurt_until=now+HURT_SECS
		self.hurt_hp=b
	def fight_hold(self,now=None):
		if now is None:now=time.time()
		b=c=False
		try:p=self.me();b=bool(p.IsDead);c=bool(p.InWarMode)
		except Exception:pass
		if b:return "dead"
		if c:return "war"
		if self.attack_rd is None:self.attack_rd=Journal.reader()
		else:
			for a in self.attack_rd.new():
				if a.hue==ATTACK_HUE and str(a.kind).upper()!="CLIENT"and Journal.ATTACK_RE.search(a.text):self.attacked_until=max(self.attacked_until,min(a.at,now)+HURT_SECS)
		if 0<self.hurt_until-now<=HURT_SECS:return "hurt"
		if 0<self.attacked_until-now<=HURT_SECS:return "attacked"
		if self.foe_near():return "foe"
		if Kit.held_item():return "item"
		d=self.services.get("attention.up")
		if d is not None and safe(d):return "alarm"
		return
	def me(self):
		if self.in_hop and self._me_pid==self.pass_id:return self._me
		try:p=API.Player
		except Exception:p=None
		m=_Memo(p)if p is not None else None
		if self.in_hop:self._me_pid=self.pass_id;self._me=m
		return m
	def _mob_scan(self):
		if self._mob_pid==self.pass_id and(self.in_hop or time.time()-self._mob_at<=self.MOB_AGE):return self._mob_list
		a=[];b=None
		if self.in_hop:
			if self._one_pid!=self.pass_id:self._one={};self._one_pid=self.pass_id
			b=self._one
		try:c=API.GetAllMobiles()or()
		except Exception:c=()
		for r in c:
			try:
				d=r.Distance;m=_Memo(r);m.__dict__["Distance"]=d;a.append((d,m))
				if b is not None:b[int(r.Serial)]=m
			except Exception:continue
		self._mob_pid,self._mob_list,self._mob_at=self.pass_id,a,time.time();return a
	def mobiles(self,distance=None):
		a=self._mob_scan()
		if distance is None:return[b[1]for b in a]
		return[e for c,e in a if c<=distance]
	def mobile(self,serial):
		try:k=int(serial)
		except Exception:return
		if self.in_hop:
			if self._one_pid!=self.pass_id:self._one={};self._one_pid=self.pass_id
			a=self._one
			if k in a:return a[k]
		try:r=API.FindMobile(k)
		except Exception:r=None
		m=_Memo(r)if r is not None else None
		if self.in_hop:self._one[k]=m
		return m
	def pack_items(self,deep=True,max_age=0.):
		k=bool(deep);e=time.time();c=self._pack.get(k)
		if c is not None and((self.in_hop and c[0]==self.pass_id)or(max_age>0 and 0<=e-c[1]<=max_age)):return list(c[2])
		a=API.Backpack;d=list((API.FindTypeAll(0xFFFFFFFF,a)if k else API.ItemsInContainer(a,False))or[])if a else[]
		if a and self._pack_hook["on"]:
			try:b=set(int(f.Serial)for f in d);b.add(int(a))
			except Exception:b=set()
			if not k and len(self._pack_keys)<=self.PACK_CAP:b|=self._pack_keys
			self._pack_keys=b if len(b)<=self.PACK_CAP else set([int(a)])
		self._pack[k]=(self.pass_id if self.in_hop else-1,e,d);return list(d)
	def pack_dirty(self):self._pack.clear()
	def pack_ver(self):Kit.hook_once(self._pack_hook,"on",("OnItemCreated",self._pack_fn),("OnItemUpdated",self._pack_fn));return self._pack_v
	def _pack_event(self,*c):
		a=self._pack_keys
		for b in c:
			try:s,d=int(b.Serial),int(b.Container)
			except Exception:continue
			if d in a or s in a:self._pack_v+=1;self._pack.clear()
			return
	def pick_target(self,timeout,a,owner=None):Picker.ask(timeout,a,owner)
	def ui_pending(self):
		if self.ui_busy or self.config is None or not Kit.pending:return
		self.ui_busy=True
		try:
			while Kit.pending:
				a,Kit.pending=Kit.pending,[]
				for b in a:safe(b)
		finally:self.ui_busy=False
	def ui_tick(self):
		self.ui_pending()
		if self.ui_busy or self.config is None:return
		self.ui_busy=True
		try:
			a=time.time()
			if a>=self.ui_next:
				self.ui_next=a+UI_TICK;self.config.poll()
				if not VA_ALONE and a>=self.alive_at:self.alive_at=a+1.;API.SetSharedVar(ALIVE_KEY,str(a))
				if self.hub is not None:self.hub.poll()
				self.dock_tick();SNAP.tick()
				if a-self.input_at>UI_IDLE_AFTER and not(SNAP.down or LAYOUT.arrange):self.ui_next=a+UI_IDLE
				if self.grid is not None:self.grid.tick()
				try:ALERTS.tick(a)
				except Exception as b:self._tell("%s: alert error: %s%s"%(APP_NAME,b,_error_where()))
				try:GUARD.tick(a)
				except Exception as b:self._tell("%s: guard-zone error: %s%s"%(APP_NAME,b,_error_where()))
				if self.whats_new.g is not None:self.whats_new.poll()
		except Exception as b:
			c="%s: settings window error: %s%s"%(APP_NAME,b,_error_where())
			if not self.stopping():self._tell(c)
		finally:self.ui_busy=False
	def load_prefs(self):
		a=self.prefs=Kit.codec_load(Kit.get_var(SETTINGS_KEY));b=[g for g in a.get("modules","").split(",")if g];c=set(h for h in a.get("seen","").split(",")if h);d=a.get("seen","");e=self._migrate_parts(a,b,c);f=self.held_on=set()
		for s in self.slots:
			if s.default_on and s.key not in c:b.append(s.key);c.add(s.key);self._parts_fill(s)
			s.enabled=s.key in b and(s.api is not None or s.lazy is not None)
			if s.key in b and not s.enabled:f.add(s.key)
			if s.enabled:self._parts_fill(s)
		a["seen"]=",".join(sorted(c));Kit.set_dark(self.pref_int("dark",0)==1)
		if a["seen"]!=d or e:self.save_prefs()
	def _migrate_parts(self,c,on,seen):
		def f(key):
			a={}
			for b in c.get(key,"").split(","):
				if "."in b:d,e=b.split(".",1);a.setdefault(d,set()).add(e)
			return a
		i,j=f("parts"),f("parts_off");k="parts"not in c or c.get("parts_from","")!=c.get("modules","");a=set(on);d=False
		for s in self.slots:
			if not s.parts:continue
			b=i.get(s.key);g=j.get(s.key)
			if b is None and g is not None and s.key not in a and not any(n in a for m in s.parts for n in m[4]):
				for p in s.parts:s.parts_on[p[0]]=p[0]in g
				continue
			if b is not None and not k:
				for p in s.parts:
					s.parts_on[p[0]]=p[0]in b
					if len(p)>5 and p[5]and p[0]not in b and p[3]:
						h=str(Kit.get_var("VirtueAssistant_new_parts","")or "").split(",")
						if p[0]not in h:
							if not VA_ALONE:Kit.put_var("VirtueAssistant_new_parts",",".join([o for o in h if o]+[p[0]]))
							s.parts_on[p[0]]=True;d=True
			else:
				e=[r for q in s.parts for r in q[4]];l=any(t in a for t in e)or(s.key in a and not e)
				for p in s.parts:
					if p[4]:s.parts_on[p[0]]=any(u in a for u in p[4])
					elif b is not None:s.parts_on[p[0]]=p[0]in b
					else:s.parts_on[p[0]]=bool(p[3])and not l and s.key not in a
				if s.key in a:self._parts_fill(s)
				d=True
				if any(v in seen for v in e)and s.key not in seen:seen.add(s.key)
			if s.parts_wanted():
				if s.key not in a:on.append(s.key);a.add(s.key)
			elif s.key in a:on.remove(s.key);a.discard(s.key)
		return d
	def pref_int(self,key,default):
		try:return int(self.prefs.get(key,default))
		except Exception:return default
	def save_prefs(self,now=False):
		if self.config is not None:self.config.box_hit=True
		if self.prefs_frozen:return
		a,d,b=[],[],[]
		for s in self.slots:
			if not s.enabled and s.key not in self.held_on:
				for p in s.parts:
					if s.parts_on.get(p[0]):b.append("%s.%s"%(s.key,p[0]))
				continue
			a.append(s.key)
			for p in s.parts:
				if s.parts_on.get(p[0]):
					d.append("%s.%s"%(s.key,p[0]))
					for e in p[4]:
						if e not in a:a.append(e)
		self.prefs["modules"]=",".join(a);self.prefs["parts"]=",".join(d);self.prefs["parts_from"]=self.prefs["modules"]
		if b:self.prefs["parts_off"]=",".join(b)
		else:self.prefs.pop("parts_off",None)
		if self.config is not None:self.config.store_prefs(self.prefs)
		if self.hub is not None:self.hub.store_prefs(self.prefs)
		c=";".join("%s=%s"%(f,g)for f,g in sorted(self.prefs.items()));t=time.time()
		if not now and t<self.prefs_at:self.prefs_due=True;return c
		self.prefs_due=False;self.prefs_at=t+self.PREFS_EVERY;Kit.put_var(SETTINGS_KEY,c);return c
	def prefs_flush(self,force=False):
		if self.prefs_due and not self.prefs_frozen and(force or time.time()>=self.prefs_at):self.save_prefs(True)
	def profile_job(self,req):
		a,b=req
		try:getattr(self,"_profile_"+a)(b)
		except Exception as c:d={"fav":"set the favourite profile"}.get(a,a+" the profile");Kit.say("couldn't %s (%s%s)."%(d,Tz.why(c),_error_where()),Kit.HUE_BAD)
		if a!="load"and self.config is not None and not self.stopping():
			self.config.refresh_profiles()
			if self.config.mode=="full":self.config.prof_redraw=False;self.config.redraw()
	def _profile_save(self,name):
		name=PROFILES.clean(name)
		if not name:raise Exception("type a name for the profile in the box")
		Kit.say('saving profile "%s".'%name,Kit.HUE_INFO);c=self.save_prefs(True);d,n,e,a=PROFILES.save(name,c);b=PROFILES.favorite();PROFILES.set_state("fav"if name==b else "pick",name,d)
		if name==b:
			try:PROFILES.set_client_default(name)
			except Exception as f:a.append("TazUO default for new characters (%s)"%Tz.why(f))
		if self.config is not None:self.config.prof_sel=name
		PROFILES.report(name,"saved",n,True,e,a)
	def _profile_load(self,name):
		if PROFILES.info(name)is None:raise Exception('there is no profile "%s"'%name)
		Kit.say('loading profile "%s".'%name,Kit.HUE_INFO);self.prefs_flush(True);self.prefs_frozen=True
		try:
			if self.config is not None:safe(self.config.close)
			for s in self.slots:
				if s.running:self._stop(s)
			if self.hub is not None:safe(self.hub.close)
			Kit._vars.clear();a="fav"if name==PROFILES.favorite()else "pick";b=PROFILES.apply(name,a)
			for c in set(Binds.saved.values())|Binds.hooked:Binds.unhook(c)
			Binds.saved.clear();Binds.loaded=False;self._zone_was_d=None;Kit._vars.clear();ALERTS.loaded=False;GUARD.saved=None;Kit.read_screen();Binds.load()
			for s in self.slots:
				if s.api is not None and s.lazy is None and s.factory is not None:
					try:s.api=s.factory();s.broken=None
					except Exception as d:s.api,s.broken=None,str(d)+_error_where();Kit.say("couldn't load %s (%s)."%(s.title,s.broken),Kit.HUE_BAD)
			self.load_prefs();LAYOUT.load()
		finally:
			self.prefs_frozen=False;self.config=ConfigWindow(self);self.config.prof_sel=name;self.config.open();self.hub=HubWindow(self)
			if self.grid is not None:safe(self.grid.show if self.pref_int("grid_on",0)==1 else self.grid.hide)
			for s in self.slots:
				if s.enabled:self.start(s)
			Kit.note_screen()
		PROFILES.report(name,"loaded",*b)
	def _profile_fav(self,name):
		if PROFILES.info(name)is None:raise Exception("save a profile first, then star it")
		if PROFILES.favorite()==name:PROFILES.set_favorite("");safe(lambda:PROFILES.set_client_default(None));Kit.say('"%s" is no longer the favourite profile.'%name,Kit.HUE_INFO);return
		PROFILES.set_favorite(name);a=""
		try:PROFILES.set_client_default(name)
		except Exception as b:a=" (TazUO's default for new characters wasn't set: %s)"%Tz.why(b)
		Kit.say('"%s" is the favourite profile: characters that haven\'t loaded another get it at start.%s'%(name,a),Kit.HUE_GOOD)
	def run(self):
		Client.find()
		if Client.mouse is None:Kit.say("no client mouse timer; double-clicks use the client's own event.",Kit.HUE_INFO)
		self.load_prefs();Kit.read_screen();LAYOUT.load();SNAP.on_drop(LAYOUT.dropped);API.OnStop(self.shutdown);self.grid=Grid(self)
		try:self.config=ConfigWindow(self);self.config.open()
		except Exception as a:
			self._tell("%s: couldn't build the window: %s%s"%(APP_NAME,a,_error_where()))
			if self.config is None:self.config=safe(lambda:ConfigWindow(self))
			if self.config is not None:safe(lambda:self.config.build_gear(self.config.gx,self.config.gy))
		try:self.hub=HubWindow(self)
		except Exception as a:self._tell("%s: couldn't make the Ultima Tracker window: %s%s"%(APP_NAME,a,_error_where()))
		if self.pref_int("grid_on",0)==1:safe(self.grid.show)
		b=[c.title for c in self.slots if c.enabled];API.SysMsg("%s %s running. %s"%(APP_NAME,APP_VERSION,("On: "+", ".join(b))if b else "Tick a module on the Modules tab."),Kit.HUE_GOOD);API.SetSharedVar(ALIVE_KEY,str(time.time()));Binds.load();self.load_jobs.extend(d for d in self.slots if d.enabled and d not in self.load_jobs);Kit.note_screen()
		try:self.whats_new.open()
		except Exception as a:self._tell("%s: couldn't make the What's new window: %s"%(APP_NAME,a))
		self.loop()
	def run_alone(self,s):
		if self.suite_alive():API.SysMsg("%s: %s is running; use %s there."%(s.title,APP_NAME,s.title),Kit.HUE_BAD);return
		self.alone,self.prefs_frozen=s,True;Client.find();self.load_prefs();Kit.read_screen();API.OnStop(self.shutdown);self.config=AlonePage(s);self.hub=safe(lambda:HubWindow(self));a=Kit.get_var(ALONE_PARTS%s.key,"")
		if s.parts and a:s.parts_on=dict((b[0],b[0]in a.split(","))for b in s.parts)
		API.SysMsg("%s: running alone, without the rest of %s."%(s.title,APP_NAME),Kit.HUE_GOOD);Binds.load();self.enable(s.key);self.loop()
	def loop(self):
		try:
			while not self.stopping()and(self.alone is None or self.alone.enabled):
				a=time.time();self.drain()
				try:self.run_due()
				except Exception as b:
					if self.stopping():break
					self._tell("%s: main loop error: %s%s"%(APP_NAME,b,_error_where()))
				API.Pause(self.nap(a))
		finally:self.shutdown()
	def shutdown(self):
		if self.shut:return
		self.shut=self.quitting=True;safe(Picker.drop)
		if self.off_q:self._drop_offs()
		if not VA_ALONE:safe(lambda:Kit.on_client(LAYOUT.game_view_restore));safe(lambda:LAYOUT.set_arrange(False,tell=False));safe(lambda:Kit.on_client(lambda:[b.free()for b in list(ClientWin.found.values())+[LAYOUT.journal_held]if b is not None]))
		if self.config is not None:safe(lambda:self.save_prefs(True));safe(self.config.close)
		else:safe(lambda:self.prefs_flush(True))
		for s in reversed(self.slots):
			if s.running:
				try:self._stop(s)
				except Exception:s.running=False
		self._refresh_active()
		if self.hub is not None:safe(self.hub.close)
		for a in(ALERTS.close,self.whats_new.close,GUARD.store,Kit.note_screen):safe(a)
		if self.grid is not None:safe(self.grid.hide)
		safe(lambda:API.SysMsg("%s stopped."%APP_NAME,Kit.HUE_INFO))
class PartSet(object):
	OFF_LINE="%s is off: tick it under PARTS to see its settings."
	def __init__(self,key,title,parts,shared=None):self.key=key;self.specs=[[a[0],a[1],float(a[2]),a[3]if len(a)>3 else None]for a in parts];self._owner={b[0]:b[3]or("%s.%s"%(key,b[0]))for b in self.specs};self._iv={c[0]:c[2]for c in self.specs};self._fns={};self.api={};self.running=[];self.due={};self.thread_due={};self.want=self._slot=None;self.busy=0;self.stopping=False;self.shared=shared or{}
	def slot(self):
		if self._slot is None:self._slot=dict.get(HOST.by_key,self.key)
		return self._slot
	def owner(self,a):return self._owner.get(a,a)
	def part_api(self,b):
		a=self.api.get(b)
		if a is None:
			for c in self.specs:
				if c[0]==b:
					HOST.cur_part,HOST.cur_owner=b,self.owner(b)
					try:a=c[1]()
					except Exception as d:
						a={};s=self.slot()
						if s is not None:HOST.report(s,d,s.part_title(b),b)
					finally:HOST.cur_part=HOST.cur_owner=None
					self.api[b]=a;self._fns[b]=((a.get("interval"),"thread_tick"in a,a.get("thread_wanted"))if a else(None,False,None));break
		return a
	def _call(self,a,d,*e):
		b=self.part_api(a);c=b.get(d)if b else None
		if not c:return
		s=self.slot();f=(HOST.cur_part,HOST.cur_owner);HOST.cur_part,HOST.cur_owner=a,self.owner(a);self.busy+=1
		try:return c(*e)
		except Exception as g:
			if s is not None and not HOST.stopping():HOST.report(s,g,s.part_title(a),a)
		finally:self.busy-=1;HOST.cur_part,HOST.cur_owner=f
		return
	def _sync_slot(self):
		s=self.slot()
		if s is not None:s.parts_running=set(self.running)
	def start_part(self,a):
		if a in self.running or self.stopping:return
		b=self.part_api(a)
		if not b:self.api.pop(a,None);return
		self.running.append(a);self._sync_slot();self.due[a]=0.;self.thread_due[a]=False;s=self.slot()
		if s is not None:s.next_due=0.
		self._call(a,"start")
	def stop_part(self,a):
		if a not in self.running:return
		self.running.remove(a);self._sync_slot();b=self.owner(a);Picker.drop(b);HOST.release_cursor(b);self._call(a,"stop");Kit.unhook(b)
	def wanted(self):s=self.slot();return set(s.parts_wanted())if s is not None else set()
	def reconcile(self,want=None):
		if want is None:want=self.wanted()
		if self.busy:self.want=set(want);return
		self.want=None
		for b in self.specs:
			a=b[0]
			if a in want and a not in self.running:self.start_part(a)
		for a in list(reversed(self.running)):
			if a not in want:self.stop_part(a)
	def _start(self):self.stopping=False;self.reconcile()
	_NOFN=(None,False,None)
	def _tick(self):
		b=time.time();g=HOST.pass_poked;c=self.running;d=self.due;e=HOST.pass_keys if self.key in HOST.pass_keys else None
		for a in list(c):
			if a not in c:continue
			f=d.get(a,0.)
			if g or b+Host.EARLY>=f or f-b>Host.CLOCK_BACK or(e is not None and self.key+"."+a in e):self._call(a,"tick");h,i,j=self._fns.get(a,self._NOFN);d[a]=time.time()+Host._ask(h,self._iv.get(a,.1));self.thread_due[a]=i and Host._ask(j,True,bool)
		if self.want is not None and not self.busy:self.reconcile(self.want)
	def _thread_wanted(self):
		if self.want is not None:return True
		a=self.thread_due
		for b in self.running:
			if a.get(b):return True
		return False
	def _thread_tick(self):
		for a in list(self.running):
			if self.thread_due.get(a)and a in self.running:self.thread_due[a]=False;self._call(a,"thread_tick")
		if self.want is not None and not self.busy:self.reconcile(self.want)
	def _interval(self):
		a=None;b=self.due
		for c in self.running:
			d=b.get(c,0.)
			if a is None or d<a:a=d
		if a is None:return 1.
		return min(30.,max(.002,a-time.time()))
	def _stop(self):
		self.stopping=True;self.want=None
		for a in list(reversed(self.running)):self.stop_part(a)
	HEAD_H=28
	def _config_height(self,w):
		h=0
		for c in self.specs:
			a=c[0];h+=(Kit.GAP if h else 0)+self.HEAD_H
			if a in self.running:
				b=self.api.get(a)
				if b and b.get("config_height"):d=self._call(a,"config_height",w);h+=Kit.GAP+max(0,int(d or 0))
		return max(40,h)
	def _build_config(self,g,x,y,w):
		s=self.slot()
		for d in self.specs:
			a=d[0];e=s.part(a)[1]if s is not None and s.part(a)else a;b=a in self.running;c=self.api.get(a)if b else None
			if y>0 and d is not self.specs[0]:y+=Kit.GAP
			Kit.add_section(g,x,y,w,self.HEAD_H,e.upper()if b else None)
			if not b:Kit.add_label(g,Kit.fit(self.OFF_LINE%e,w-24),x+12,y+7,Kit.HUE_INFO)
			y+=self.HEAD_H
			if b and c and c.get("build_config"):y+=Kit.GAP;f=self._call(a,"config_height",w)if c.get("config_height")else 0;self._call(a,"build_config",g,x,y,w);y+=max(0,int(f or 0))
	def _poll_config(self):
		for a in list(self.running):self._call(a,"poll_config")
	def _config_closed(self):
		for a in self.specs:
			b=self.api.get(a[0])
			if b and b.get("config_closed"):self._call(a[0],"config_closed")
	def hooks(self):
		h={"start":self._start,"tick":self._tick,"stop":self._stop,"client_tick":True,"thread_tick":self._thread_tick,"thread_wanted":self._thread_wanted,"interval":self._interval,"parts":self.reconcile,"config_height":self._config_height,"build_config":self._build_config,"poll_config":self._poll_config,"config_closed":self._config_closed};a=self.shared
		if not a:return h
		def b():self._tick();a["tick"]()
		def c():
			try:self._stop()
			finally:a["stop"]()
		def d():self._thread_tick();a["thread_tick"]()
		def e():return bool(a["thread_wanted"]())or self._thread_wanted()
		f={"tick":b,"stop":c,"thread_tick":d,"thread_wanted":e};h.update((g,f[g])for g in a);return h
class Tz(object):
	_types={};_MISS=object()
	@staticmethod
	def T(name):
		if name not in Tz._types:Tz._types[name]=Client._type(name)
		t=Tz._types[name]
		if t is None:raise Exception("this TazUO build has no %s"%name.split(".")[-1])
		return t
	@staticmethod
	def get(obj,name,t=None):
		v=Typing._get(obj,name,t,Tz._MISS)
		if v is Tz._MISS:raise Exception("can't read %s"%name)
		return v
	@staticmethod
	def _flags(static):from System.Reflection import BindingFlags;return BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.DeclaredOnly|(BindingFlags.Static if static else BindingFlags.Instance)
	_found={}
	@staticmethod
	def put(obj,name,value,t=None):
		t=t if t is not None else obj.GetType();c=("put",t,name,obj is None);a=Tz._found.get(c,Tz._MISS)
		if a is Tz._MISS:
			a=None;d=Tz._flags(obj is None);b=t
			while b is not None:
				p=b.GetProperty(name,d)
				if p is not None and p.CanWrite:a=(True,p);break
				f=b.GetField(name,d)
				if f is not None:a=(False,f);break
				b=b.BaseType
			Tz._found[c]=a
		if a is None:raise Exception("can't set %s"%name)
		if a[0]:a[1].SetValue(obj,value,None)
		else:a[1].SetValue(obj,value)
	@staticmethod
	def call(obj,name,b=(),t=None,f=False):
		import System;t=t if t is not None else obj.GetType();b=list(b);n=len(b);g=("call",t,name,n,obj is None,f);a=Tz._found.get(g,Tz._MISS)
		if a is Tz._MISS:
			a=None;h=Tz._flags(obj is None);c=t
			while c is not None and a is None:
				for d in c.GetMethods(h):
					if d.Name!=name or d.IsGenericMethodDefinition:continue
					e=list(d.GetParameters())
					if len(e)==n or f and len(e)>n and all(i.IsOptional for i in e[n:]):a=(d,[j.DefaultValue for j in e[n:]]);break
				c=c.BaseType
			Tz._found[g]=a
		if a is None:raise Exception("can't call %s.%s"%(t.Name,name))
		return a[0].Invoke(obj,System.Array[object](b+a[1]))
	@staticmethod
	def load_json(path,a,t):
		import System;b=Tz.T("ClassicUO.Configuration.ConfigurationResolver")
		for m in b.GetMethods(Tz._flags(True)):
			if m.Name=="Load"and m.IsGenericMethodDefinition and m.GetParameters().Length==2:g=m.MakeGenericMethod(System.Array[System.Type]([t]));return g.Invoke(None,System.Array[object]([path,a]))
		raise Exception("can't read TazUO settings files")
	@staticmethod
	def copy_props(src,dst,skip=()):
		import System;from System.Reflection import BindingFlags;b=c=0
		for p in dst.GetType().GetProperties(BindingFlags.Public|BindingFlags.Instance):
			d=str(p.Name)
			if d in skip or d.endswith("Serial"):continue
			if not p.CanRead or not p.CanWrite or p.GetIndexParameters().Length or p.GetSetMethod(False)is None:continue
			e=safe(lambda:list(p.GetCustomAttributes(True)),[])or[]
			if any(f.GetType().Name=="JsonIgnoreAttribute"for f in e):continue
			try:
				v=p.GetValue(src,None)
				if System.Object.Equals(v,p.GetValue(dst,None)):continue
				try:p.SetValue(dst,v,None)
				except Exception:a=p.PropertyType;v=System.Enum.ToObject(a,v)if a.IsEnum else System.Convert.ChangeType(v,a);p.SetValue(dst,v,None)
				b+=1
			except Exception:c+=1
		return b,c
	@staticmethod
	def windows(a):b=Tz.get(None,"Gumps",Tz.T("ClassicUO.Game.Managers.UIManager"));return[c for c in list(b)if str(c.GetType().Name)in a]
	@staticmethod
	def why(a):
		e=getattr(a,"clsException",None)or a
		while getattr(e,"InnerException",None)is not None:e=e.InnerException
		return str(getattr(e,"Message",None)or e)
class Profiles(object):
	PROFILE_SKIP=("Username","ServerName","CharacterName","Serial","LastLoaded","FollowingTarget");BAG_OWN=("slot.","trapsel=","trapextra=");SERIAL_KEY=re.compile(r"_[0-9A-Fa-f]{8}$");VA_KEYS=("ActionBar_","Attention_","BandageAgent","Character_","CombatBars_","CorpseRun_","EMPings.","Grimoire_","Harvest_","Interface_","Layout_","Lookout_","Meters_","Mongotchi_","Pets_","PropertyButler_","Restock_","SkillBags_","Skills_","Social_","SpellTimers_","StorageIndex_","SwingTimer_","swingtimer_","SystemStats_","TrapHL_","TreasureHunter_","UltimaTracker_","UnifiedBag_","UnitFrames_","VirtueAssistant_","WorldMap_");OWN_VARS=("CorpseRun_corpse","SkillBags_rules","SkillBags_done","UnitFrames_tracked","Social_names","TreasureHunter_maps","Restock_settings","PropertyButler_visits","SpellTimers_active");MISSING="\x01VA-missing"
	def __init__(self):self.base=os.path.join(Kit.data_dir(),PROFILE_DIR)
	@staticmethod
	def _read(path):return Kit.read_safe(path,None)if path else None
	@staticmethod
	def _write(path,text):Kit.write_safe(path,text)
	@staticmethod
	def _esc(s):return s.replace("\\","\\\\").replace("\t","\\t").replace("\r","\\r").replace("\n","\\n")
	@staticmethod
	def _unesc(s):a={"t":"\t","r":"\r","n":"\n"};return re.sub(r"\\(.)",lambda m:a.get(m.group(1),m.group(1)),s,flags=re.S)
	RESERVED=frozenset(["CON","PRN","AUX","NUL","CLOCK$"]+["COM%d"%i for i in range(1,10)]+["LPT%d"%i for i in range(1,10)])
	@staticmethod
	def clean(name):
		name=re.sub(r'[\\/:*?"<>|\t\r\n]+',"-",str(name or ""));name=name.strip(" .-")[:PROFILE_NAME_MAX].strip(" .-")
		if name.lower().endswith((".old",".saving")):a=name.rfind(".");name=(name[:a]+"-"+name[a+1:])[:PROFILE_NAME_MAX]
		if name.split(".")[0].upper()in Profiles.RESERVED:return ""
		return name
	def folder(self,name):return os.path.join(self.base,name)
	def names(self):
		import System;a=[]
		with Kit.quiet:
			if System.IO.Directory.Exists(self.base):
				for d in System.IO.Directory.GetDirectories(self.base):
					n=str(System.IO.Path.GetFileName(d))
					if n.endswith(".saving")or n.endswith(".old"):continue
					if System.IO.File.Exists(os.path.join(str(d),"profile.txt")):a.append(n)
		return sorted(a,key=lambda s:s.lower())
	def info(self,name):
		a=self._read(os.path.join(self.folder(name),"profile.txt"))if name else None
		if a is None:return
		b=(c.split("=",1)for c in a.splitlines()if "="in c);return dict((d.strip(),e.strip())for d,e in b)
	def favorite(self):a=(self._read(os.path.join(self.base,"_favorite.txt"))or "").strip();return a if a and self.info(a)is not None else ""
	def set_favorite(self,name):
		if not os.path.isdir(self.base):os.makedirs(self.base)
		self._write(os.path.join(self.base,"_favorite.txt"),name or "")
	def state(self):p=Kit.get_var(PROFILE_STATE_KEY).split("|");return(p[0],p[1],p[2])if len(p)>=3 else("","","")
	def set_state(self,mode,name,a):Kit.put_var(PROFILE_STATE_KEY,"%s|%s|%s"%(mode,name,a))
	SESSION_VARS=("Layout_gameview_own","Layout_gameview_lock","Layout_zone_was","VirtueAssistant_reclaim_undo")
	def keep_var(self,key,extra=()):
		if key==PROFILE_STATE_KEY or self.SERIAL_KEY.search(key)or key in self.SESSION_VARS:return False
		if key in self.OWN_VARS or key.startswith(("Grimoire_H_","Layout_client_locked_")):return False
		return key.startswith(self.VA_KEYS+tuple(extra))
	def profile_vars(self,a):b=set(d.key for d in HOST.slots);c=tuple(set(e[:-8]for e in a if e.endswith("_settings")and e[:-9].lower()in b));return dict((f,g)for f,g in a.items()if self.keep_var(f,c))
	@staticmethod
	def char_vars():
		import System;t=Tz.T("ClassicUO.LegionScripting.PersistentVars")
		for m in t.GetMethods():
			if m.Name=="GetAllVars"and m.GetParameters().Length==1:a=System.Enum.Parse(m.GetParameters()[0].ParameterType,"Char");d=m.Invoke(None,System.Array[object]([a]));return dict((str(b.Key),""if b.Value is None else str(b.Value))for b in d)
		raise Exception("can't list this character's saved settings")
	def read_vars(self,name):
		c=self._read(os.path.join(self.folder(name),"va_vars.txt"))or "";a={}
		for b in c.split("\n"):
			if "\t"in b:
				k,v=b.split("\t",1);k=self._unesc(k)
				if k:a[k]=self._unesc(v.rstrip("\r"))
		return self.profile_vars(a)
	def wait_vars(self,wanted,timeout=5.):
		a=dict(wanted);c=time.time()+timeout
		while a and not API.StopRequested:
			for k in list(a):
				b=safe(lambda:API.GetPersistentVar(k,self.MISSING,API.PersistentVar.Char))
				if b is not None and str(b)==a[k]:del a[k]
			if not a or time.time()>c:break
			API.Pause(.05)
		return not a
	@staticmethod
	def bag_path():
		a=safe(lambda:int(API.Player.Serial),0)
		if not a:return
		return Kit.data_path("_unified_bag_%d.cfg"%a)
	@staticmethod
	def client_files():
		c,a="ClassicUO.Configuration.","ClassicUO.Game.Managers.";h=lambda:Tz.T(c+"ProfileManager");i=lambda:Tz.get(None,"CurrentProfile",h());f=lambda:str(Tz.get(None,"ProfilePath",h()));g=lambda:Tz.get(None,"Instance",Tz.T("ClassicUO.Game.World"));b=lambda a,name,b=():Tz.call(None,name,b,Tz.T(a));d=lambda a:Tz.get(None,"Current",Tz.T(a));e=lambda a:Tz.get(None,"Instance",Tz.T(a));j=c+"FeatureConfigs.ScreenDecorations.ScreenDecorations"
		def k():b=e(a+"AutoLootManager");Tz.put(b,"_loaded",False);Tz.call(b,"Load")
		def l():
			Tz.call(Tz.get(g(),"InfoBars"),"Load")
			for a in Tz.windows(("InfoBarGump",)):safe(lambda:Tz.call(a,"ResetItems"))
		def m():b(a+"BuySellAgent","Unload");b(a+"BuySellAgent","Load")
		return(("cooldownbars.json","cooldown bars",lambda:Tz.call(d(c+"CooldownBarsConfig"),"Save"),lambda:b(c+"CooldownBarsConfig","LoadForProfile",(f(),i()))),("grid_highlights.json","grid highlights",lambda:Tz.call(d(c+"GridHighlightsConfig"),"Save"),lambda:b(c+"GridHighlightsConfig","LoadForProfile",(f(),i()))),("grid_container_bands.json","container bands",lambda:Tz.call(d(c+"GridContainerBandsConfig"),"Save"),lambda:b(c+"GridContainerBandsConfig","LoadForProfile",(f(),))),("screen_decorations.json","screen effects",lambda:Tz.call(d(j),"Save"),lambda:b(j,"LoadForProfile",(f(),))),("tooltip_overrides.json","tooltip overrides",lambda:Tz.call(Tz.get(d(c+"TooltipOverridesConfig"),"Char"),"Save"),lambda:b(c+"TooltipOverridesConfig","Load")),("nameoverhead.xml","name plates",lambda:b(a+"NameOverHeadManager","Save"),lambda:b(a+"NameOverHeadManager","Load")),("infobar.xml","info bar",lambda:Tz.call(Tz.get(g(),"InfoBars"),"Save"),l),("AutoLoot.json","auto loot",lambda:Tz.call(e(a+"AutoLootManager"),"Save"),k),("OrganizerConfig.json","organizer",lambda:Tz.call(e(a+"OrganizerAgent"),"Save"),lambda:b(a+"OrganizerAgent","Load")),("journal_filters.json","journal filter",lambda:Tz.call(e(a+"JournalFilterManager"),"Save",(False,)),lambda:Tz.call(e(a+"JournalFilterManager"),"Load")),("BuyAgentConfig.json","auto buy",m,lambda:b(a+"BuySellAgent","Load")),("SellAgentConfig.json","auto sell",lambda:None,lambda:b(a+"BuySellAgent","Load")),("macros.xml","macros",lambda:Tz.call(Tz.get(g(),"Macros"),"Save",(None,)),lambda:Tz.call(Tz.get(g(),"Macros"),"Load")),("hotkeys.json","hotkeys",lambda:b(a+"Hotkeys.HotKeys","Save"),lambda:b(a+"Hotkeys.HotKeys","Load")),)
	@staticmethod
	def _profile_type():a=Tz.T("ClassicUO.Configuration.ProfileManager");return a,Tz.get(None,"CurrentProfile",a)
	def _client_export(self,dest):
		import System;F=System.IO.File;g,h=self._profile_type();d=str(Tz.get(None,"ProfilePath",g));i,a,b=[],[],[]
		try:Tz.call(h,"Save");b.append((os.path.join(d,"profile.json"),os.path.join(dest,"profile.json"),"options"))
		except Exception as c:a.append("options (%s)"%Tz.why(c))
		for e,f,j,k in self.client_files():
			try:
				j();p=os.path.join(d,e)
				if F.Exists(p):b.append((p,os.path.join(dest,e),f))
			except Exception as c:a.append("%s (%s)"%(f,Tz.why(c)))
		return i,a,b
	def _apply_options(self,path):
		import System;f,a=self._profile_type();c=Tz.get(None,"DefaultToUse",Tz.T("ClassicUO.Configuration.ProfileJsonContext"));b=Tz.load_json(path,Tz.get(c,"Profile"),a.GetType())
		if b is None:raise Exception("its profile.json can't be read")
		d,e=Tz.copy_props(b,a,self.PROFILE_SKIP);Tz.call(a,"Save");safe(lambda:Tz.call(Tz.get(None,"Game",Tz.T("ClassicUO.Client")),"SetVSync",(Tz.get(a,"EnableVSync"),)));safe(lambda:Tz.put(None,"ContainerScale",System.Single(int(Tz.get(a,"ContainersScale"))/100.),Tz.T("ClassicUO.Game.Managers.UIManager")));return d,e
	def _client_import(self,e):
		import System;F=System.IO.File;c,b=[],[]
		for w in Tz.windows(("OptionsWindow","AssistantWindow")):safe(lambda:Tz.call(w,"Dispose"))
		l,o=self._profile_type();m=str(Tz.get(None,"ProfilePath",l));f=os.path.join(e,"profile.json")
		if F.Exists(f):
			try:
				n,g=self._apply_options(f);c.append("options (%d changed)"%n)
				if g:b.append(Kit.count(g,"option"))
			except Exception as d:b.append("options (%s)"%Tz.why(d))
		for h,i,q,j in self.client_files():
			p=os.path.join(e,h)
			if not F.Exists(p):continue
			a=os.path.join(m,h);k=F.ReadAllBytes(a)if F.Exists(a)else None
			try:F.Copy(p,a,True);j();c.append(i)
			except Exception as d:
				b.append("%s (%s)"%(i,Tz.why(d)))
				with Kit.quiet:
					if k is not None:F.WriteAllBytes(a,k)
					elif F.Exists(a):F.Delete(a)
					j()
		return c,b
	def set_client_default(self,name):
		import System;F=System.IO.File;e=str(Tz.get(None,"RootPath",Tz.T("ClassicUO.Configuration.ProfileManager")))
		for f,g in(("profile.json","default.json"),("macros.xml","macros.xml")):
			a=os.path.join(e,g);b,c=a+".va-backup",a+".va-none"
			if name:
				d=os.path.join(self.folder(name),"tazuo",f)
				if not F.Exists(d):continue
				if not F.Exists(b)and not F.Exists(c):
					if F.Exists(a):F.Copy(a,b,False)
					else:self._write(c,"")
				F.Copy(d,a,True)
			elif F.Exists(b):F.Copy(b,a,True);F.Delete(b)
			elif F.Exists(c):
				if F.Exists(a):F.Delete(a)
				F.Delete(c)
	@staticmethod
	def _on_client(fn):
		try:a=Kit.on_client(fn,fallback=False)
		except Exception as b:a=([],["TazUO settings (%s)"%Tz.why(b)])
		return a or([],["TazUO settings (couldn't reach the client)"])
	def save(self,name,l):
		import System;D=System.IO.Directory;b=self.folder(name);a,c=b+".saving",b+".old"
		if D.Exists(a):D.Delete(a,True)
		D.CreateDirectory(os.path.join(a,"tazuo"));f="%d"%int(time.time());d=self.profile_vars(self.char_vars());d[SETTINGS_KEY]=l;self._write(os.path.join(a,"va_vars.txt"),"".join("%s\t%s\n"%(self._esc(r),self._esc(d[r]))for r in sorted(d)));g=self.bag_path();h=self._read(g)if g else None
		if h is not None:m=[s for s in h.splitlines()if s.strip()and not s.startswith(self.BAG_OWN)];self._write(os.path.join(a,"unified_bag.cfg"),"\n".join(m))
		e=self._on_client(lambda:self._client_export(os.path.join(a,"tazuo")));i,j=list(e[0]),list(e[1]);F=System.IO.File
		for n,o,k in(e[2]if len(e)>2 else()):
			try:F.Copy(n,o,True);i.append(k)
			except Exception as p:j.append("%s (%s)"%(k,Tz.why(p)))
		q=safe(lambda:str(API.Player.Name),"")or "";self._write(os.path.join(a,"profile.txt"),"name=%s\nsaved=%s\nfrom=%s\nversion=%s\n"%(name,f,q,APP_VERSION))
		if D.Exists(c):D.Delete(c,True)
		if D.Exists(b):D.Move(b,c)
		try:D.Move(a,b)
		except Exception:
			if D.Exists(c)and not D.Exists(b):safe(lambda:D.Move(c,b))
			raise
		if D.Exists(c):D.Delete(c,True)
		if self.read_vars(name)!=d or(self.info(name)or{}).get("saved")!=f:raise Exception("the saved copy doesn't read back the same; try again")
		return f,len(d),i,j
	def apply(self,name,mode):
		f=self.info(name)
		if f is None:raise Exception('there is no profile "%s"'%name)
		g=self.folder(name);a=self.read_vars(name)
		for k in sorted(a):Kit.put_var(k,a[k])
		h=self.wait_vars(a);c=self._read(os.path.join(g,"unified_bag.cfg"));b=self.bag_path();d=Kit.read_safe(b)if c is not None and b else None
		if d is not None:i=[m for m in d.splitlines()if m.startswith(self.BAG_OWN)];self._write(b,"\n".join([n for n in c.splitlines()if n.strip()]+i))
		j,e=self._on_client(lambda:self._client_import(os.path.join(g,"tazuo")))
		if c is not None and b and d is None:e=list(e)+["bag layout (couldn't read the bag file)"]
		self.set_state(mode,name,f.get("saved",""));return len(a),h,j,e
	def report(self,name,a,n,ok,done,failed):
		Kit.say('profile "%s" %s: %d Virtue Assistant settings; TazUO: %s.'%(name,a,n,", ".join(done)or "nothing"),Kit.HUE_GOOD)
		if not ok:Kit.say("some settings were still saving; restart Virtue Assistant if a module looks unchanged.",Kit.HUE_BAD)
		if failed:Kit.say("not done: %s."%"; ".join(failed),Kit.HUE_BAD)
	def startup(self):
		a=self.favorite()
		if not a:return
		c=(self.info(a)or{}).get("saved","");d,b,e=self.state()
		if d=="pick"and b!=a and self.info(b)is not None:return
		if b==a and e==c:return
		self.report(a,"(the favourite) put on this character",*self.apply(a,"fav"))
class ConfigWindow(object):
	W=640;GEAR=52;TABS=(("modules","Modules"),("settings","Settings"));DOCK_KEY="va";LINK_CMD="VirtueAssistant_cmd";LINK_STATE="VirtueAssistant_state";LINK_ALIVE="ActionBar_alive";LINK_STALE=10.;LINK_ENABLE="VirtueAssistant_enable"
	def __init__(self,host):
		self.host=host;self.g=self.mode=self._pp_key=self.shown_page=self.request=self.request_tab=None;self.lag_lbl=self.dirty=self.gear_pos=self.body=self.head=None;self.link_state=self.prof_sel=self.prof_cache=self.prof_shown=None;self.loading=self.stale_page=self.search_tb=self.search_text=None;self.gear_clicked=self.closing=self.docked=self.prof_stale=self.prof_redraw=False;self.box_hit=self.redraw_req=self.search_focus=False;self.gear_look=self.lag_next=self.gear_moved=self.link_next=self.box_next=self.search_at=0.;self.resize_at=0.;self.store=({},{});self.seen={};self._pp_gate=[0.];self._fld_gate=[0.];self._fld_due=True;self.x,self.y=Kit.adapt(host.pref_int("cfg_x",140),host.pref_int("cfg_y",80),self.W,self.MIN_H);self.gx,self.gy=Kit.adapt(host.pref_int("gear_x",self.x),host.pref_int("gear_y",self.y),self.GEAR,self.GEAR);self.minimized=host.pref_int("cfg_min",0)==1 or host.dock_wanted(self.DOCK_KEY);self.tab=host.prefs.get("cfg_tab","modules")
		if self.tab not in("modules","settings"):self.tab="modules"
		self.page=host.prefs.get("cfg_page","");SNAP.enabled=host.pref_int("snap",1)==1;self.reported=set();self.page_keys=[];self.box_list=[];self.part_boxes=[];self.fold_keys=[];self.measured={};self.mod_search="";self._prof_reset();a=Kit.screen()[1];self.lim_w=max(self.W,host.pref_int("cfg_w",self.W));self.lim_h=max(self.MIN_H,host.pref_int("cfg_h",(a-60)if a>400 else 1000));self.scale=max(50,min(200,host.pref_int("cfg_scale",100)))/100.;self.size=(0,0)
		for b in(self.LINK_CMD,self.LINK_ENABLE):API.RemoveSharedVar(b)
	STAR_RECTS=((7,1,1,2),(6,3,3,3),(1,6,13,2),(4,8,7,3),(3,11,3,3),(9,11,3,3));STAR_ON,STAR_OFF=(240,192,64),(106,106,106);PROF_H=34;PROF_DD_W=196
	def _prof_reset(self):self.prof_dd=self.prof_dd_args=self.prof_tb=self.prof_seen=None;self.prof_names=[];self.prof_fav="";self.prof_stars=[];self.prof_star_hit=False
	@staticmethod
	def _cap_w(art,text):return(Kit.pic_size(art[0])[0]or 30)+5+Kit.text_w(text)
	def refresh_profiles(self):
		self.prof_stale=False;P=PROFILES
		try:a=("ok",P.names(),P.favorite(),P.state()[1])
		except Exception as b:a=("err",b)
		self.prof_cache=a
		if self.prof_shown is not None and self._prof_key(a)!=self.prof_shown and self.mode=="full":self.prof_redraw=True
	@staticmethod
	def _prof_key(data):return("ok",data[1],data[2])if data[0]=="ok"else("err",str(data[1]))
	def _build_profiles(self,g,x,y,w):
		b=self.prof_cache
		if b is None:self.refresh_profiles();b=self.prof_cache
		self.prof_shown=self._prof_key(b);self.prof_stale=True
		if b[0]!="ok":raise b[1]
		a,d,h=b[1],b[2],b[3];c=self.prof_sel if self.prof_sel in a else None
		if c is None:c=h if h in a else(d if d in a else(a[0]if a else None))
		self.prof_sel,self.prof_names,self.prof_fav=c,a,d;H=self.PROF_H;Kit.add_section(g,x,y,w,H);f=x+12+self.PROF_DD_W+10;i=y+(H-16)//2;m="#%02X%02X%02X"%self.STAR_OFF;n=[Kit.add_box(g,f+s,i+t,u,v,1.,m)for s,t,u,v in self.STAR_RECTS];self.prof_stars=[z for z in n if z is not None];Kit.catcher(g,f-3,i-3,22,22,self._star_click,"Favourite: characters that haven't loaded another profile get it (click again to clear)");e=f+28
		for o,j,k,p,q in(("p_load",Kit.ART_PLAY,"Load",14,"Load the picked profile here"),("p_save",Kit.ART_OK,"Save",6,"Save this setup under the typed name, or over the picked profile")):Kit.art_button(g,self.store,o,j,e,y+6,k,q);e+=self._cap_w(j,k)+p
		Kit.add_label(g,"as",e,y+9,Kit.HUE_INFO);l=e+Kit.text_w("as")+8;self.prof_tb=Kit.with_tip(Kit.add_textbox(g,"",l,y+6,max(60,x+w-12-l),numbers=False),"New profile name (empty: save over the picked one)");r=[A+("  (favourite)"if A==d else "")for A in a]or["(no profiles saved yet)"];self.prof_dd_args=(x+12,y+7,self.PROF_DD_W,r,a.index(c)if c in a else 0)
	def _add_profile_list(self,g):
		if self.prof_dd_args is None:return
		a=self.prof_dd;d,e,f,h,b=self.prof_dd_args
		if a is not None:
			i=Kit.dd_index(a,None);Kit.dispose(a)
			if i is not None and 0<=i<len(self.prof_names):self.prof_sel=self.prof_names[i]
		if self.prof_sel in self.prof_names:b=self.prof_names.index(self.prof_sel)
		c=G.CreateDropDown(f,h,b);c.SetPos(d,e);g.Add(c);self.prof_dd=Kit.with_tip(c,"Saved profiles: pick one to load or save over");self.prof_seen=b;self._show_star()
	def _prof_picked(self):return self.prof_sel if self.prof_sel in self.prof_names else None
	def _show_star(self):
		p=self._prof_picked();r,g,b=self.STAR_ON if bool(p)and p==self.prof_fav else self.STAR_OFF
		for a in self.prof_stars:
			with Kit.quiet:a.SetBaseColor(r,g,b,255)
	def _star_click(self):self.prof_star_hit=True
	def _poll_profiles(self):
		if self.prof_dd is not None and self._fld_due:
			i=Kit.dd_index(self.prof_dd,None)
			if i is not None and i!=self.prof_seen:
				self.prof_seen=i
				if 0<=i<len(self.prof_names):self.prof_sel=self.prof_names[i]
				self._show_star()
		f,self.prof_star_hit=self.prof_star_hit,False;b=Kit.was_clicked(self.store,"p_load");c=Kit.was_clicked(self.store,"p_save")
		if not(f or b or c):return
		if self.host.profile_req is not None:return
		a=self._prof_picked()
		if c:
			d=str(safe(lambda:self.prof_tb.Text,"")or "").strip();e=PROFILES.clean(d)if d else a
			if not e:Kit.say("type a profile name beside Save.",Kit.HUE_BAD);return
			self.host.profile_req=("save",e)
		elif not a:Kit.say("save a profile first (type a name beside Save).",Kit.HUE_BAD)
		elif b:self.host.profile_req=("load",a)
		else:self.host.profile_req=("fav",a)
	def settings_slots(self):return[a for a in self.host.slots if a.lazy is not None or(a.api is not None and a.api.get("build_config"))]+list(self.host.pages)
	def open(self):
		if self.prof_cache is None:self.refresh_profiles()
		if self.minimized:self.build_gear(self.gx,self.gy)
		else:self.build_full(self.x,self.y)
	def build_full(self,x,y):Kit.on_client(lambda:self._build_full(x,y))
	def _replace(self,g,mode,x,y,w,h,head=None):
		a=self.g;x,y=Kit.place(g,x,y,w,h,head)
		if mode=="gear":self.gx,self.gy=x,y
		else:self.x,self.y=x,y
		self.g,self.mode=g,mode;G.AddGump(g);Kit.on_moved(g,self._moved)
		if mode=="gear":g.SetInScreen()
		Kit.dispose(a)
	def _note_pos(self):
		x,y=self.pos()
		if x is None or y is None:return False
		if self.mode=="gear":self.gx,self.gy=x,y
		elif self.mode=="full":self.x,self.y=x,y
		return True
	def _moved(self):
		if self._note_pos():self.host.save_prefs()
	def _settings_error(self,s,what,b):
		a="%s: %s settings %s error: %s%s"%(APP_NAME,s.title,what,b,_error_where())
		if a not in self.reported:self.reported.add(a);API.SysMsg(a,Kit.HUE_BAD)
		self.host.count_error(s,page=True)
	def _leave_page(self):
		a,self.shown_page=self.shown_page,None;c,self.stale_page=self.stale_page==a,None;s=self.host.page_slot(a)
		if s is None or s.api is None:return
		for b in(("config_closed",)if c else("poll_config","config_closed")):
			if s.api.get(b):
				try:s.api[b]()
				except Exception as d:self._settings_error(s,"save",d)
	COL_W=W-2*Kit.MARGIN;MIN_W=W;MIN_H=200;SETTLE=.35;SCALES=(70,80,90,100,110,125,150);ART_LESS=(5401,5401,5401);ART_MORE=(5402,5402,5402);HELP_LINES=("Tick a module to turn it on; closing its window turns it off. Settings are on the Settings tab.","Drag a corner to resize; - and + scale the window.","Zones, layout and snapping: Settings > Interface.");BROKEN="couldn't load: see the journal";LAG_SAMPLE="12 modules on; slowest lately: Ultima Tracker, 999 ms"
	def _context(self):
		c=self.host;b=self.settings_slots();a=None
		if self.tab=="settings"and b:
			a=c.page_slot(self.page)
			if a not in b:a=b[0];self.page=a.key
			if a.lazy is not None and Client.on_client_thread():c.request_load(a);self.loading=a;return c.slots,b,None
			if not c.load(a)or not a.api.get("build_config"):
				b=self.settings_slots();a=b[0]if b and c.load(b[0])and b[0].api.get("build_config")else None
				if a is not None:self.page=a.key
		self.loading=None;return c.slots,b,a
	def _body_y(self):return Kit.MARGIN+34+Kit.GAP+self.PROF_H+Kit.GAP
	def _pack(self,units,n,d):
		m=Kit.GAP;g,a,y=[],0,0
		for u,e in enumerate(units):
			c=e.get("rows")
			if c is None:
				f=e["h"];b=y+m if y else 0
				if y and b+f>d:a,b=a+1,0
				if a>=n or f>d:return
				g.append((u,a,b,None,None,f));y=b+f;continue
			k,l=e["head"],e["tail"];i=0
			while i<len(c):
				b=y+m if y else 0
				if y and b+k+c[i]+l>d:a,b=a+1,0
				if a>=n or k+c[i]+l>d:return
				j,h=i,k+l
				while j<len(c)and b+h+c[j]<=d:h+=c[j];j+=1
				g.append((u,a,b,i,j,h));i,y=j,b+h
				if i<len(c):a,y=a+1,0
		return g
	def _fit(self,units,n):
		a=b=0
		for c in units:
			d=c.get("rows")
			if d is None:a=max(a,c["h"]);b+=c["h"]+Kit.GAP
			elif d:a=max(a,c["head"]+max(d)+c["tail"]);b+=c["head"]+sum(d)+c["tail"]+Kit.GAP
		b=max(b,a,1);f=self._pack(units,n,b)
		while a<b:
			e=(a+b)//2;p=self._pack(units,n,e)
			if p is not None:b,f=e,p
			else:a=e+1
		return f or[]
	def _flow(self,units,e):
		M,a=Kit.MARGIN,Kit.GAP;c=self.lim_w;b=Kit.screen()[0]
		if b:c=min(c,max(self.MIN_W,int(b/self.scale)-10))
		n=max(1,(c-2*M+a)//(e+a))
		if b:n=max(1,min(n,(int(b/self.scale)-2*M+a)//(e+a)))
		f=max(40,self.lim_h-self._body_y()-M);d=self._pack(units,n,f)
		if d is None:d=self._fit(units,n)
		return d
	@staticmethod
	def _matches(s,q):
		if not q:return True,[]
		b=q in s.title.lower()or q in(s.desc or "").lower()or any(q in c.lower()for c in s.aliases);a=[d[0]for d in s.parts if q in d[1].lower()or q in(d[2]or "").lower()]
		if not a:a=[e[0]for e in s.parts if any(q in str(f).lower()for f in e[4])]
		return b or bool(a),a
	def _mod_rows(self,slots,f):
		q=self.mod_search.strip().lower();c,g,d={},[],{}
		for s in slots:
			h,i=self._matches(s,q)
			if not h:continue
			d[s.key]=i;a=s.category or "Other"
			if a not in c:c[a]=[];g.append(a)
			c[a].append(s)
		j=[k for k in CATEGORY_ORDER if k in c]+sorted(l for l in g if l not in CATEGORY_ORDER);b=[]
		for a in j:
			b.append(("head",a))
			for s in c[a]:
				e=s.api is None and s.lazy is None;b.append(("mod",s,e,Kit.wrap(self.BROKEN if e else s.desc,f-212)))
				if s.parts and not e and(not s.folded or d.get(s.key)):
					for p in s.parts:b.append(("part",s,p,Kit.wrap(p[2]or "",f-248),p[0]in d.get(s.key,())))
		if not b:b.append(("none",'No module matches "%s".'%self.mod_search.strip()))
		return b
	@staticmethod
	def _row_h(r):
		if r[0]in("mod","part"):return 26+20*(len(r[3])-1)
		return 24
	def _units_modules(self,slots):a=self.COL_W;b=self._mod_rows(slots,a);c=[k for f in self.HELP_LINES for k in Kit.wrap(f,a-42)];d=8+22*len(c)+24;e=[{"rows":[self._row_h(l)for l in b],"head":34,"tail":4,"draw":lambda g,x,y,h,i,j:self._draw_mods(g,x,y,a,h,b[i:j],i==0)},{"h":d,"draw":lambda g,x,y,h,i,j:self._draw_opts(g,x,y,a,h,c)}];return e,a
	PAGE_MAX_W=1100
	def _measure_page(self,page,b,i,a):
		try:h=int(page.api["config_height"](a))
		except Exception:h=None
		f=(page.key,a,h,bool(page.running),tuple(j[0]for j in page.parts if page.parts_on.get(j[0])))
		if f in self.measured:return self.measured[f]
		c=PageCanvas(None);d=None
		try:
			page.api["build_config"](c,b,i,a)
			if Kit.flush():
				g=b+a
				for e in c.ctrls:
					r=safe(lambda:int(e.GetX())+int(e.GetWidth()),None)
					if r is not None and r!=b+a:g=max(g,r+4)
				d=([tuple(int(l)for l in k)for k in c.sections],g-b)
		except Exception:d=None
		finally:
			if page.api.get("config_closed"):safe(page.api["config_closed"])
			for e in c.ctrls:Kit.dispose(e)
		if len(self.measured)>64:self.measured.clear()
		if page not in self.host.pages:self.measured[f]=d
		return d
	def forget_measure(self,key):
		for a in[b for b in self.measured if b[0]==key]:self.measured.pop(a,None)
	def loaded(self,key):
		self.forget_measure(key)
		if self.loading is not None and self.loading.key==key:self.redraw_req=True
	def _pick_unit(self,pages,b,lit):
		c=35+max([Kit.text_w(e.title)for e in pages]or[80])+12;a=max(1,1+(b-30-c)//196);self.page_keys=[("page_"+f.key,f.key)for f in pages];n=(len(pages)+a-1)//a
		def d(g,x,y,h,i,j):
			Kit.add_section(g,x,y,b,h)
			for k,s in enumerate(pages):
				r=k//a
				if i<=r<j:Kit.art_button(g,self.store,"page_"+s.key,Kit.ART_PAGE,x+30+(k%a)*196,y+6+(r-i)*28,s.title,"Show %s settings"%s.title,Kit.HUE_TITLE if lit(s)else Kit.HUE_TEXT)
		return{"rows":[28]*n,"head":6,"tail":4,"draw":d}
	def _units_loading(self,pages,title):
		a=self.COL_W
		def b(g,x,y,h,i,j):Kit.add_section(g,x,y,a,h);Kit.add_label(g,"Loading %s settings"%title,x+12,y+12,Kit.HUE_INFO)
		return[self._pick_unit(pages,a,lambda s:s.title==title),{"h":40,"draw":b}],a
	def _units_settings(self,pages,page,f,c):
		a=self.COL_W;d=None;m=self._measure_page(page,f,c,a)
		if m is not None:
			d,o=m
			if o>a:a=min(self.PAGE_MAX_W,o);m=self._measure_page(page,f,c,a);d=m[0]if m is not None else None
		e=[self._pick_unit(pages,a,lambda s:s is page)]
		if page.parts:e.append({"h":34+26*len(page.parts)+6,"draw":lambda g,x,y,h,i,j:self._draw_parts(g,x,y,a,h,page)})
		k=LAYOUT.windows_of(page.key)if LAYOUT.enabled else()
		if k:e.append({"h":34+26*len(k)+6,"draw":lambda g,x,y,h,i,j:self._draw_windows(g,x,y,a,h,k)})
		try:l=max(40,int(page.api["config_height"](a)))
		except Exception as q:self._settings_error(page,"layout",q);l=40
		n=(self._bands(d,c,l)if d else None)or[(0,l)];p={"at":{}}
		def r(b):
			def d(g,x,y,h,i,j):
				p["at"][b]=(x,y)
				if b==len(n)-1:self._draw_page(g,page,f,c,a,n,p["at"])
			return d
		for t,(u,v)in enumerate(n):e.append({"h":v-u,"draw":r(t)})
		return e,a
	@staticmethod
	def _bands(b,c,f):
		b=sorted(set(b),key=lambda r:(r[1],r[0]));e=[g for g in b if not any(i!=g and i[0]<=g[0]and i[1]<=g[1]and g[0]+g[2]<=i[0]+i[2]and g[1]+g[3]<=i[1]+i[3]for i in b)];a=[]
		for x,y,w,h in e:
			t,d=y-c,y-c+h
			if a and t<a[-1][1]:a[-1]=(a[-1][0],max(a[-1][1],d))
			else:a.append((t,d))
		return a
	def _draw_page(self,g,page,b,a,i,m,at):
		j=PageCanvas(g)
		try:page.api["build_config"](j,b,a,i)
		except Exception as k:self._settings_error(page,"window",k);Kit.add_section(g,b,a,i,40);Kit.add_label(g,"Settings unavailable: %s"%k,b+12,a+12,Kit.HUE_BAD)
		self.shown_page=page.key;c=[]
		for n,(d,u)in enumerate(m):o,p=at.get(n,(b,a+d));c.append((d,o-b,p-(a+d)))
		if all(v==0 and w==0 for x,v,w in c):return
		if not Kit.flush():return
		for e in j.ctrls:
			try:q,l=int(e.GetX()),int(e.GetY())
			except Exception:continue
			r=l-a;f,h=c[0][1],c[0][2]
			for d,s,t in c:
				if r>=d:f,h=s,t
			if f or h:safe(lambda:e.SetPos(q+f,l+h))
	SEARCH_W=150
	def _draw_parts(self,g,x,y,w,h,s):
		Kit.add_section(g,x,y,w,h,"PARTS  (tick a part to turn it on)");a=y+32
		for p in s.parts:self._part_box(g,s,p,x+12,a);Kit.add_label(g,Kit.fit(p[2]or "",w-236),x+224,a+2,Kit.HUE_INFO);a+=26
	def _part_box(self,g,s,p,x,c):a=bool(s.parts_on.get(p[0]));b=Kit.add_check(g,p[1],x,c,a,"%s: %s"%(s.title,p[2]or p[1]));self._hook_box(b);self.part_boxes.append((s,p[0],b));self.seen["%s.%s"%(s.key,p[0])]=a
	ZONE_TIP="Click: next zone (free: stays where you put it; Settings > Interface lists them all)"
	def _draw_windows(self,g,x,y,w,h,wins):
		Kit.add_section(g,x,y,w,h,"WINDOWS  (the zone each sits in)");e=LAYOUT.zone_choices();a=y+32
		for b,f in wins:Kit.add_label(g,Kit.fit(f,200),x+12,a+3);c=LAYOUT.zone_of(b);i="Zone: "+(c if c else "free");d="zone_"+b;Kit.art_button(g,self.store,d,Kit.ART_PAGE,x+224,a-2,i,self.ZONE_TIP);self.zone_keys.append((d,b,e));a+=26
	FOLD_TIP="Show its parts";UNFOLD_TIP="Hide its parts";NEW_TAG="(new)"
	def _draw_mods(self,g,x,y,w,h,rows,first):
		Kit.add_section(g,x,y,w,h,"MODULES  (tick a module to turn it on)"if first else "MODULES  (continued)")
		if first:f=x+w-12-self.SEARCH_W;Kit.add_label(g,"Search",f-8-Kit.text_w("Search"),y+7,Kit.HUE_INFO);self.search_tb=Kit.with_tip(Kit.add_textbox(g,self.mod_search,f,y+5,self.SEARCH_W,numbers=False),"Type part of a name or feature to list matching modules (old names work)");self.search_text=None
		b=y+32
		for a in rows:
			if a[0]=="part":
				s,p,c,i=a[1],a[2],a[3],a[4];self._part_box(g,s,p,x+36,b);j=x+236
				for k,d in enumerate(c):Kit.add_label(g,d,j,b+2+20*k,Kit.HUE_INFO)
				e="<- found"if i else(self.NEW_TAG if not p[4]else "")
				if e:n=Kit.text_w(c[0])if c else 0;Kit.add_label(g,e,min(j+n+10,x+w-12-Kit.text_w(e)),b+2,Kit.HUE_TITLE if i else Kit.HUE_INFO)
			elif a[0]!="mod":Kit.add_label(g,a[1].upper()if a[0]=="head"else a[1],x+12,b+3,Kit.HUE_TITLE if a[0]=="head"else Kit.HUE_INFO)
			else:
				s,l,c=a[1],a[2],a[3]
				if l:Kit.add_label(g,s.title,x+36,b+2,Kit.HUE_INFO)
				else:
					m=Kit.add_check(g,s.title,x+12,b,s.enabled,s.desc);self._hook_box(m);self.box_list.append((s,None,m));self.seen[s.key]=s.enabled
					if s.parts:o=">"if s.folded else "v";Kit.add_label(g,o,x+184,b+2,Kit.HUE_TITLE);Kit.catcher(g,x+178,b,18,22,self._fold_click(s.key),self.FOLD_TIP if s.folded else self.UNFOLD_TIP);self.fold_keys.append(("fold_"+s.key,s.key))
				for k,d in enumerate(c):Kit.add_label(g,d,x+200,b+2+20*k,Kit.HUE_BAD if l else Kit.HUE_INFO)
			b+=self._row_h(a)
	def _fold_click(self,key):
		a=self.store
		def b():Kit.clicks_seen=True;a[1]["fold_"+key]=True;HOST.poke()
		return b
	def _draw_opts(self,g,x,y,w,h,lines):
		Kit.add_section(g,x,y,w,h);a=y+8
		for b in lines:Kit.add_label(g,b,x+30,a,Kit.HUE_INFO);a+=22
		self.lag_lbl=Kit.add_label(g,"",x+30,a,Kit.HUE_INFO);self.lag_next=0.
	def _on_resized(self,*b):
		a=not self.resize_at;self.resize_at=time.time();g=self.g
		if a and self.mode=="full"and Kit.is_open(g):g.SetAlpha(.55)
	def _relayout(self):
		g=self.g
		if self.mode!="full"or not Kit.is_open(g):return
		try:w,h=int(g.GetWidth()),int(g.GetHeight());x,y=int(g.GetX()),int(g.GetY())
		except Exception:return
		if(w,h)==self.size:return
		self.lim_w=max(self.MIN_W,int(round(w/self.scale)));self.lim_h=max(self.MIN_H,int(round(h/self.scale)));self.x,self.y=x,y;self.build_full(x,y);self.host.save_prefs()
	def _step_scale(self,d):
		a=list(self.SCALES);b=int(round(self.scale*100));i=min(range(len(a)),key=lambda k:abs(a[k]-b));i=max(0,min(len(a)-1,i+d))if d else a.index(100)
		if a[i]!=b:self.scale=a[i]/100.;self.redraw()
	def _reset(self):self._leave_page();self.search_tb,self.search_text,self.search_at=None,None,0.;self.store=({},{});self.page_keys,self.box_list,self.zone_keys=[],[],[];self.lag_lbl=None;self._prof_reset()
	def _plan(self):
		h,c,d=self._context();M,i=Kit.MARGIN,Kit.GAP;f=self._body_y()
		if self.tab=="settings"and d is not None:b,a=self._units_settings(c,d,M,f)
		elif self.tab=="settings"and self.loading is not None and c:b,a=self._units_loading(c,self.loading.title)
		else:b,a=self._units_modules(h)
		e=self._flow(b,a);g=1+max([j[1]for j in e]or[0]);W=2*M+g*a+(g-1)*i;H=f+max([k[2]+k[5]for k in e]or[40])+M;return d,b,a,e,W,H
	def _draw_body(self,g,units,b,placed):
		a=PageCanvas(g);c=self._body_y()
		for u,d,e,i,j,h in sorted(placed,key=lambda p:p[0]):units[u]["draw"](a,Kit.MARGIN+d*(b+Kit.GAP),c+e,h,i,j)
		return a
	def _build_full(self,x,y):
		self._reset();self.seen,self.resize_at={},0.;self.part_boxes,self.fold_keys=[],[];M,q=Kit.MARGIN,Kit.GAP;L=M;B,r,s,t,W,H=self._plan();a=M;j=a+34+q;u=self._body_y();k=W-2*M;S=self.scale;b,c=int(round(W*S)),int(round(H*S));g=G.CreateModernGump(x,y,b,c,True,int(self.MIN_W*S),int(self.MIN_H*S),self._on_resized);g.SetAlpha(0);Kit.add_window_frame(g,W,H,mouse=False);Kit.add_section(g,L,a,k,34);Kit.add_label(g,"VIRTUE ASSISTANT",L+30,a+9,Kit.HUE_TITLE);l=L+30+Kit.text_w("VIRTUE ASSISTANT")+12;Kit.add_label(g,"v"+APP_VERSION,l,a+9,Kit.HUE_INFO);d=l+Kit.text_w("v"+APP_VERSION)+16;Kit.title_catcher(g,L,a,d-6-L,34,lambda:self.store[1].__setitem__("min",True),key="va")
		for m,e in self.TABS:v=m==self.tab;Kit.art_button(g,self.store,"tab_"+m,Kit.ART_PAGE,d,a+6,e,"Show the %s tab"%e,Kit.HUE_TITLE if v else Kit.HUE_INFO);d+=self._cap_w(Kit.ART_PAGE,e)+16
		f="%d%%"%int(round(S*100));n=W-M-74-Kit.DOCK_DX-8-16;Kit.art_button(g,self.store,"scale_up",self.ART_MORE,n,a+9,None,"Larger window and text");h=n-6-Kit.text_w(f);Kit.add_label(g,f,h,a+9,Kit.HUE_TEXT);Kit.catcher(g,h-2,a+6,Kit.text_w(f)+4,22,lambda:self.store[1].__setitem__("scale_reset",True),"Scale (click: 100%)");Kit.art_button(g,self.store,"scale_down",self.ART_LESS,h-6-16,a+9,None,"Smaller window and text");Kit.dock_button(g,self.store,W-M-74,a+9);Kit.art_button(g,self.store,"min",Kit.ART_MIN,W-M-74,a+9,None,"Minimize to the gear (or double-click the title)");Kit.art_button(g,self.store,"close",Kit.ART_CLOSE,W-M-54,a+6,None,"Close Virtue Assistant (stops every module)")
		try:self._build_profiles(g,L,j,k)
		except Exception as w:self.prof_dd_args=None;Kit.add_label(g,"Profiles unavailable: %s"%w,L+12,j+9,Kit.HUE_BAD)
		z=frozenset(self.store[0]);A=self._draw_body(g,r,s,t);self._add_profile_list(g)
		if not Kit.scale_window(g,S)and S!=1.:self.scale,S,b,c=1.,1.,W,H;Kit.say("can't scale the window; it stays at 100%.",Kit.HUE_BAD)
		self._replace(g,"full",x,y,b,c,int(round(u*S)));i=Kit.scroll_info(g);self.size=(i["w2"],i["hv"])if i else(b,c);self.minimized=False;self.dirty=None;self.body,self.head=A,(g,W,self.tab,Kit.dark(),z)
		if self.search_focus:
			self.search_focus=False;o=self.search_tb
			if o is not None:
				p=Kit.client_control(o)
				if p is not None and Kit.flush():safe(lambda:p.SetKeyboardFocus())
	def build_gear(self,x,y):
		self._reset();S=self.GEAR;g=G.CreateGump(True,True);Kit.add_window_frame(g,S,S,corners=False);Kit.add_section(g,7,7,S-14,S-14);p=G.CreateGumpItemPic(4179,S-18,S-18);p.SetPos(9,9);p.SetAcceptMouseInput(False);g.Add(p);Kit.catcher(g,0,0,S,S,self._gear_click,"%s: click to open, drag to move"%APP_NAME,movable=True);self.gear_clicked,self.gear_pos,self.gear_moved=False,None,0.;self._replace(g,"gear",x,y,S,S);self.minimized=True;self.docked=self.host.dock_wanted(self.DOCK_KEY)and self.host.bar_alive()
		if self.docked:self._show_gear(False)
	def fold_to_bar(self):
		self.host.dock_want_set(self.DOCK_KEY,True)
		if self.mode=="full":self.fold()
		if not self.host.bar_alive():self.host.dock_note(APP_NAME)
	def _show_gear(self,shown):
		g=self.g
		if self.mode=="gear"and Kit.is_open(g):g.IsVisible=bool(shown)
	def link_tick(self):
		b=time.time()
		if b<self.link_next and self.link_next-b<=.1:return
		self.link_next=b+.1;e=self._take_shared(self.LINK_ENABLE)
		if e:self.host.enable(str(e))
		a=self._take_shared(self.LINK_CMD)
		if a:
			a=str(a)
			if a=="show"and self.mode!="full":self.unfold()
			elif a=="dock"and self.mode=="full":self.fold_to_bar()
			elif a=="modules":self.request_tab="modules"
		f=self.host.dock_wanted(self.DOCK_KEY)
		if self.mode=="gear"and(self.docked or f):
			c=f and self.host.bar_alive()
			if c!=self.docked:self.docked=c;self._show_gear(not c)
		d=("docked"if self.docked else "gear")if self.mode=="gear"else "open"
		if d!=self.link_state:self.link_state=d;API.SetSharedVar(self.LINK_STATE,d)
	@staticmethod
	def _take_shared(name):
		try:v=API.GetSharedVar(name)
		except Exception:return
		if v:API.RemoveSharedVar(name)
		return v
	def _gear_click(self):self.gear_clicked=True
	def pos(self):g=self.g;return safe(lambda:int(g.GetX())),safe(lambda:int(g.GetY()))
	def store_prefs(self,a):
		if Client.on_client_thread():self._note_pos()
		for k,v in(("cfg_x",self.x),("cfg_y",self.y),("cfg_w",self.lim_w),("cfg_h",self.lim_h),("cfg_scale",int(round(self.scale*100))),("gear_x",self.gx),("gear_y",self.gy)):a[k]=str(v)
		a["cfg_min"]="1"if self.minimized else "0";a["cfg_tab"],a["cfg_page"]=self.tab,self.page or "";a["snap"]="1"if SNAP.enabled else "0"
	def fold(self):
		x,y=self.pos()
		if x is not None:self.x,self.y=x,y
		self.gx,self.gy=self.x,self.y;self.build_gear(self.gx,self.gy);self.host.save_prefs()
	def unfold(self):
		x,y=self.pos()
		if x is not None:self.gx,self.gy=x,y
		self.docked=False;self.host.dock_forget(self.DOCK_KEY);self.build_full(self.gx,self.gy);self.host.save_prefs()
	def redraw(self):
		if self.mode!="full":self.unfold();return
		x,y=self.pos()
		if x is not None:self.x,self.y=x,y
		self.build_full(self.x,self.y);self.host.save_prefs()
	def _switch_page(self,key):
		self.page=key;x,y=self.pos()
		if x is not None:self.x,self.y=x,y
		Kit.on_client(self._swap_body);self.host.save_prefs()
	def _swap_body(self):
		g,a=self.g,self.head;b=False
		if a is not None and a[0]is g and Kit.is_open(g)and self.tab==a[2]=="settings"and a[3]==Kit.dark()and self.scale==1. and g not in Kit._scrolled and g not in Fill.recs and not self.resize_at and self.prof_cache is not None and self._prof_key(self.prof_cache)==self.prof_shown:
			try:b=self._fast_body(g,a[1],a[4])
			except Exception as c:self.host._tell("%s: settings window error: %s%s"%(APP_NAME,c,_error_where()))
		if not b:self._build_full(self.x,self.y)
	def _fast_body(self,g,b,keys):
		self._leave_page();self.page_keys,self.zone_keys,self.part_boxes,self.seen=[],[],[],{};d,e,f,h,W,H=self._plan()
		if d is None or W!=b or H>Kit.screen()[1]>0 or not Kit.frame_fit(g,W,H):return False
		a,i,j=self.store,Kit._texts,Fill.w2r
		for c in self.body.ctrls:Kit.dispose(c);i.pop(c,None);j.pop(c,None)
		for k in[l for l in a[0]if l not in keys]:a[0].pop(k,None);a[1].pop(k,None)
		self.body=self._draw_body(g,e,f,h);self._add_profile_list(g);self.x,self.y=Kit.place(g,self.x,self.y,W,H);Kit.moved_by_code(g);self.size,self.dirty=(W,H),None;return True
	def show_settings(self,key):self.request=key
	def refresh(self,key):
		self.forget_measure(key)
		if self.shown_page==key:self.dirty=self.stale_page=key
	def close(self):self.closing=True;self._leave_page();g,self.g=self.g,None;Kit.dispose(g);self.docked,self.link_state=False,None;API.SetSharedVar(self.LINK_STATE,"off")
	def poll(self):
		if self.closing:return
		if not Kit.is_open(self.g):
			if self.host.stopping():return
			self.shown_page=None;self.build_gear(self.gx,self.gy);return
		g=self.g;self.link_tick()
		if self.g is not g and not Kit.is_open(self.g):return
		if self.request is not None:h,self.request=self.request,None;self.tab,self.page="settings",h;self.redraw();return
		if self.request_tab is not None:
			d,self.request_tab=self.request_tab,None
			if d in("modules","settings"):self.tab=d
			self.redraw();return
		if self.mode=="gear":
			a=time.time()
			if not self.docked and(self.gear_clicked or self.gear_pos is None or a>=self.gear_look or SNAP.pressed()is not False):
				self.gear_look=a+.5;p=self.pos()
				if p!=self.gear_pos:
					if self.gear_pos is not None:self.gear_moved=a
					self.gear_pos=p
			if self.gear_clicked:
				self.gear_clicked=False
				if a-self.gear_moved>.35:self.unfold()
			return
		if self.prof_redraw:self.prof_redraw=False;self.redraw();return
		if self.redraw_req:
			self.redraw_req=False
			if self.tab=="settings":self.redraw();return
		if self.resize_at and time.time()-self.resize_at>=self.SETTLE and not SNAP.pressed():self.resize_at=0.;self._relayout();return
		if self._poll_buttons():return
		self._fld_due=self.host.poll_due(self._fld_gate);self._poll_profiles()
		if self.search_tb is not None and self._fld_due and self._poll_search():return
		if self.lag_lbl is not None and time.time()>=self.lag_next:
			self.lag_next=time.time()+1.;c=self.host.active
			if c:e=max(c,key=lambda s:s.worst_ms);f="%d modules on; slowest lately: %s, %d ms"%(len(c),e.title,e.worst_ms)
			else:f="No modules on"
			Kit.set_text(self.lag_lbl,f)
		a=time.time()
		if self.box_hit or a>=self.box_next or not Kit.clicks_seen:
			self.box_hit=False;self.box_next=a+self.BOX_EVERY
			if self._poll_boxes():return
		b=self.host.page_slot(self.shown_page)if self.shown_page is not None else None
		if self.stale_page is not None and self.stale_page==self.shown_page:b=None
		if b is not None and b.api is not None and b.api.get("poll_config"):
			if self._pp_key!=self.shown_page:self._pp_key=self.shown_page;self._pp_gate[0]=0.
			if self.host.poll_due(self._pp_gate,b.api.get("poll_every")):
				try:b.api["poll_config"]()
				except Exception as i:self._settings_error(b,"update",i)
		if self.dirty is not None and self.dirty==self.shown_page:self.redraw()
	def _poll_search(self):
		try:t=str(self.search_tb.Text or "")
		except Exception:return False
		a=time.time()
		if t!=self.search_text:
			if self.search_text is not None:self.search_at=a
			self.search_text=t;return False
		if self.search_at and a-self.search_at>=SEARCH_SETTLE:
			self.search_at=0.
			if t.strip().lower()!=self.mod_search.strip().lower():self.mod_search=t.strip();self.search_focus=True;self.redraw();return True
		return False
	BOX_EVERY=1.
	def _hook_box(self,a):
		if a is None:return
		def b(*a):Kit.clicks_seen=True;self.box_hit=True;HOST.poke()
		G.AddControlOnClick(a,b)
	def _poll_boxes(self):
		c=self.seen
		for s,a,e in self.box_list+self.part_boxes:
			d,b=(s.key,s.enabled)if a is None else("%s.%s"%(s.key,a),bool(s.parts_on.get(a)))
			try:v=bool(e.IsChecked)
			except Exception:v=b
			if v!=c.get(d):
				c[d]=v
				if a is not None:self.host.part_set(s.key,a,v)
				elif v:self.host.enable(s.key)
				else:self.host.disable(s.key)
				if not Kit.is_open(self.g)or self.mode!="full":return True
			elif v!=b:safe(lambda:e.SetIsChecked(b));c[d]=b
		return False
	def _poll_buttons(self):
		b=self.store
		if Kit.clicks_seen and True not in b[1].values():return False
		if Kit.was_clicked(b,"close"):self.host.save_prefs();self.host.quitting=True;return True
		if Kit.was_clicked(b,"min"):self.host.dock_forget(self.DOCK_KEY);self.fold();return True
		if Kit.was_clicked(b,"tobar"):self.fold_to_bar();return True
		for a,g in(("scale_down",-1),("scale_up",1),("scale_reset",0)):
			if Kit.was_clicked(b,a):self._step_scale(g);return True
		for a,j in self.TABS:
			if Kit.was_clicked(b,"tab_"+a)and a!=self.tab:self.tab=a;self.redraw();return True
		for d,a in self.page_keys:
			if Kit.was_clicked(b,d)and a!=self.shown_page:self._switch_page(a);return True
		for d,a in self.fold_keys:
			if Kit.was_clicked(b,d):
				s=dict.get(self.host.by_key,a)
				if s is not None:s.folded=not s.folded
				self.redraw();return True
		for d,a,c in self.zone_keys:
			if Kit.was_clicked(b,d):
				f=LAYOUT.zone_of(a);i=c.index(f)if f in c else 0;e=c[(i+1)%len(c)]if c else None;h=LAYOUT._map_zone()
				if e is not None and a!="worldmap"and e==h and len(c)>2:e=c[(i+2)%len(c)]
				LAYOUT.assign_to(a,e);self.redraw();return True
		return False
class AlonePage(object):
	W=460;prof_stale=False;mode="alone"
	def __init__(self,s):self.s,self.want,self.dirty,self.parts,self.check_at=s,False,False,None,0.;self.st={"minimized":False,"shutting":False,"docked":False,"queue":[]};self.win={"g":None,"c":{},"store":({},{})};self.wnd=Kit.Window(s.key+"_alone",s.title+" settings",self.st,self.win,self.build,"VirtueAssistant_alone_pos",mini=(260,46),lock=False,owner=False,close_tip="Close these settings")
	def __getattr__(self,name):return lambda*a,**b:None
	def api(self):return self.s.api if self.s.api and self.s.api.get("build_config")else None
	def show_settings(self,key):self.want,self.st["minimized"]=True,False
	def refresh(self,key=None):self.dirty=True
	def rows(self):return(("PARTS",[("check",a[0],a[1],a[2])for a in self.s.parts]),)if self.s.parts else()
	def build(self):
		c,M=self.api(),Kit.MARGIN;w=self.W-2*M;b=M+30+Kit.GAP;self.parts=None;a=Kit.Form.height(self.rows(),w);a+=Kit.GAP if a else 0;g,d,e=self.wnd.begin(self.W,b+a+int(c["config_height"](w)or 0)+M)
		if not self.st["minimized"]:self.wnd.frame(g,settings=False);self.parts=Kit.Form(g,M,b,w,dict(self.s.parts_on),self.rows());c["build_config"](g,M,b+a,w)
		self.wnd.end(g)
	def poll_parts(self):
		s=self.s;a=self.parts.read();b=[c for c in a if s.parts_on.get(c)!=a[c]]
		if b and s.parts and not any(a.get(d[0],s.parts_on.get(d[0]))for d in s.parts):self.dirty=True;API.SysMsg("%s: keep one part ticked; close the window to turn it off."%s.title,Kit.HUE_INFO);return
		for k in b:HOST.part_set(s.key,k,a[k])
		if b:Kit.put_var(ALONE_PARTS%s.key,",".join(s.parts_wanted()));self.dirty=True
	def poll(self):
		a=time.time()
		if a>=self.check_at:
			self.check_at=a+2.
			if HOST.suite_alive():API.SysMsg("%s: %s started, so this copy stops."%(self.s.title,APP_NAME),Kit.HUE_INFO);HOST.disable(self.s.key);return
		if self.api()is None:return
		q=self.st["queue"]
		while q:
			b=q.pop(0)
			if b!="to_bar":self.wnd.action(b)
		if self.want or(self.dirty and self.win["g"]is not None):self.want=self.dirty=False;self.build()
		if self.win["g"]is None:return
		if Kit.was_clicked(self.win["store"],"close"):self.close()
		elif not self.st["minimized"]:
			if self.parts is not None:self.poll_parts()
			try:self.s.api["poll_config"]()
			except Exception as c:HOST._tell("%s: settings error: %s"%(self.s.title,c));HOST.count_error(self.s,page=True)
	def close(self):
		if self.win["g"]is None:return
		if self.api().get("config_closed"):self.s.api["config_closed"]()
		self.wnd.close()
class HubWindow(object):
	W=372;MINI_W,MINI_H=240,46
	def __init__(self,host):self.host=host;self.g=None;self.H=0;self.sections=[];self.stores={};self.store=({},{});self.x,self.y=Kit.adapt(host.pref_int("hub_x",100),host.pref_int("hub_y",100),self.W,self.MINI_H);self.minimized=host.pref_int("hub_min",0)==1 or host.dock_wanted("hub");self.docked=self.dirty=self.closing=False;self._gates={};host.dock_add("hub",{"title":"Ultima Tracker","icon":4183,"always":True,"state":self.state,"show":self.show,"dock":self.dock,"undock":self.undock,"minimize":self.minimize,"on":self.open_modules,"gump":lambda:self.g,"redraw":self.refresh})
	def add(self,key,title,hooks):self.remove(key);self.sections.append((key,title,hooks));self.dirty=True
	def remove(self,key):
		a=[b for b in self.sections if b[0]!=key]
		if len(a)==len(self.sections):return
		self.sections=a;self.stores.pop(key,None)
		if not a:self._close_window()
		else:self.dirty=True
	def refresh(self):self.dirty=True
	def title(self):return self.sections[0][1]if len(self.sections)==1 else "Ultima Tracker"
	def state(self):
		if not self.sections or self.g is None:return
		return "docked"if self.docked else("minimized"if self.minimized else "open")
	def show(self):self.docked=self.minimized=False;self.dirty=True
	def dock(self):
		if not self.sections:return
		self.minimized=self.docked=True;self.dirty=True
	def undock(self):
		if self.docked:self.docked=False;self._visible(True)
	def minimize(self):
		if not self.sections:return
		self.minimized,self.docked=True,False;self.dirty=True
	def toggle_min(self):self.minimized=not self.minimized;self.docked=False;self.host.dock_forget("hub");self.dirty=True
	def open_modules(self):
		if self.host.config is not None:self.host.config.request_tab="modules"
	def _visible(self,on):
		g=self.g
		if Kit.is_open(g):Kit.set(g,"IsVisible",bool(on))
	def _pos(self):
		g=self.g
		if Kit.is_open(g)and not self.host.layout_holds("hub"):
			with Kit.quiet:self.x,self.y=int(g.GetX()),int(g.GetY())
	def _leave(self):
		for b,d,a in self.sections:
			c=self.stores.get(b)
			if c is not None and a.get("poll"):safe(lambda:a["poll"](c))
			if b in self.stores and a.get("closed"):safe(a["closed"])
		self.stores={}
	def _close_window(self):self._pos();self._leave();g,self.g=self.g,None;Kit.dispose(g);self.docked=False
	def _part_of(self,key):
		m=self.host.old_map.get(key)
		if m is not None and dict.get(self.host.by_key,m[0])is not None:return m
		return key,None
	def _off(self,key):b,a=self._part_of(key);self.host.disable(("%s.%s"%(b,a))if a is not None else key)
	def _error(self,key,a):
		b,c=self._part_of(key);s=dict.get(self.host.by_key,b)
		if s is not None:self.host.report(s,a,None,c)
	def build(self):Kit.on_client(lambda:Binds.scoped("va.hub",self._build))
	def _build(self):
		self.dirty=False
		if not self.sections:self._close_window();return
		self._pos();self._leave();o=self.g;M,d=Kit.MARGIN,Kit.GAP;b=({},{});g=G.CreateGump(True,True);j=self.title().upper();e=self.host.layout_holds("hub");k="Close %s (turns %s off; the Modules tab turns %s back on)"%(self.title(),"them"if len(self.sections)>1 else "it","them"if len(self.sections)>1 else "it")
		if self.minimized:w,h=self.MINI_W,self.MINI_H;Kit.add_window_frame(g,w,h,corners=False);Kit.add_section(g,8,8,w-16,h-16);Kit.add_label(g,j,18,15,Kit.HUE_TITLE);Kit.title_catcher(g,8,8,w-70,h-16,self.toggle_min,key="hub:mini");Kit.art_button(g,b,"min",Kit.ART_RESTORE,w-60,15,None,Kit.RESTORE_TIP);Kit.art_button(g,b,"close",Kit.ART_CLOSE,w-44,12,None,k)
		else:
			w=self.W;c=w-2*M;f=[max(20,int(safe(lambda:r["height"](c),40)or 40))for s,u,r in self.sections];h=M+30+d+sum(f)+d*(len(f)-1)+M;Kit.add_window_frame(g,w,h,corners=False)
			if e:Kit.title_bar(g,b,w,self.title(),"hub",None,None)
			else:Kit.add_section(g,M,M,c,30);Kit.add_label(g,j,M+10,M+7,Kit.HUE_TITLE);Kit.title_catcher(g,M,M,c-70-Kit.DOCK_DX,30,self.toggle_min,key="hub");Kit.dock_button(g,b,w-M-66,M+7);Kit.art_button(g,b,"min",Kit.ART_MIN,w-M-66,M+7,None,Kit.MIN_TIP);Kit.art_button(g,b,"close",Kit.ART_CLOSE,w-M-44,M+4,None,k)
			y=M+30+d
			for(i,t,p),l in zip(self.sections,f):
				q=self.stores[i]=({},{})
				try:Binds.scoped(i,p["build"],g,M,y,c,q)
				except Exception as m:Kit.add_section(g,M,y,c,l);Kit.add_label(g,"%s: %s"%(t,m),M+10,y+10,Kit.HUE_BAD);self._error(i,m)
				y+=l+d
		if e:n=LAYOUT.placed.get("hub")or(self.x,self.y);g.SetPos(int(n[0]),int(n[1]))
		else:self.x,self.y=Kit.place(g,self.x,self.y,w,h)
		self.H=h;self.g,self.store=g,b;G.AddControlOnDisposed(g,lambda*a:self._disposed(g));G.AddGump(g)
		if not e:g.SetInScreen()
		Kit.on_moved(g,self._moved);Kit.dispose(o)
		if self.docked:self._visible(False)
	def _moved(self):self._pos();self.host.save_prefs()
	def _disposed(self,g):
		if self.g is g and not self.closing:
			self.g=None;self.stores={}
			for a,t,b in list(self.sections):safe(b.get("closed",lambda:None));self._off(a)
	def store_prefs(self,a):
		if Client.on_client_thread():self._pos()
		a["hub_x"],a["hub_y"]=str(self.x),str(self.y);a["hub_min"]="1"if self.minimized else "0"
	def close(self):self.closing=True;self._close_window()
	def poll(self):
		if self.closing:return
		if self.dirty:
			self.build()
			if self.sections and self.host.pref_int("hub_min",0)!=int(self.minimized):self.host.save_prefs()
		g=self.g
		if g is None:return
		if not Kit.is_open(g):self.g=None;return
		if Kit.clicks_seen and True not in self.store[1].values():pass
		elif Kit.was_clicked(self.store,"close"):
			self._pos()
			for a,t,b in list(self.sections):self._off(a)
			return
		elif Kit.was_clicked(self.store,"min"):self.toggle_min();self.build();self.host.save_prefs();return
		elif Kit.was_clicked(self.store,"tobar"):
			self.host.dock_to_bar("hub",self.title())
			if self.dirty:self.build()
			self.host.save_prefs();return
		if self.docked or self.minimized:return
		for a,t,b in list(self.sections):
			d=self.stores.get(a)
			if d is not None and b.get("poll"):
				c=self._gates.get(a)
				if c is None:c=self._gates[a]=[0.]
				if not self.host.poll_due(c,b.get("poll_every")):continue
				try:b["poll"](d)
				except Exception as e:self._error(a,e)
SNAP_DIST=16
SNAP_SETTLE=.25
SNAP_EVERY=.08
SNAP_PRUNE=2.
class Snap(object):
	def __init__(self):self.gumps=[];self.members=set();self.last=None;self.drag={};self.links={};self.button=None;self.enabled=True;self.next=0.;self.prune_at=0.;self.moved_cb={};self.moved=set();self.attached={};self._fmap=None;self.no_snap=set();self.keep_at=0.;self.screen=None;self.by_code={};self.dragged=set();self.droppers=[];self.drag_end={};self.drag_key={};self.drag_rect={};self.lost={};self.down=True;self.sweep_at=0.;self.keep_sig=None
	def add(self,g):
		if g is not None and g not in self.members:self.members.add(g);self.gumps.append(g)
	def on_moved(self,g,fn):
		if g is None:return
		if g not in self.attached:self.add(g)
		self.moved_cb[g]=fn
	def on_drop(self,fn):
		if fn not in self.droppers:self.droppers.append(fn)
	def _tell_moved(self):
		c,self.moved=self.moved,set();d,self.dragged=self.dragged,set()
		for g in c:
			a=self.moved_cb.get(g)
			if a is None:continue
			if Kit.is_open(g):
				try:a()
				except Exception:pass
		e=time.time()
		for g in d:self.drag_end[g]=e
		if len(self.drag_end)>32:
			for g in[k for k,l in self.drag_end.items()if e-l>5.]:del self.drag_end[g]
		f,h=self.drag_key,self.drag_rect;self.drag_key,self.drag_rect={},{};i,self.lost=self.lost,{}
		for g in d:
			if g in c and Kit.is_open(g):
				for a in self.droppers:
					try:a(g)
					except Exception:pass
				continue
			if f.get(g)is not None and h.get(g)is not None:i[g]=(f[g],h[g])
		j=set()
		for g,(b,r)in i.items():
			if b in j:continue
			j.add(b)
			for a in self.droppers:
				try:a(None,key=b,rect=r)
				except Exception:pass
	def moved_by_code(self,g):
		if g is None:return
		p=self.pos(g)
		if self.last is not None and p is not None:self.last[g]=p
		self.drag.pop(g,None);self.moved.discard(g);self.by_code[g]=time.time()
	def skip_gump(self,g,keep_fresh=False):
		if not keep_fresh:LAYOUT.fresh_adds.discard(g)
		if g in self.members:self.members.discard(g);self.gumps.remove(g)
	def exempt(self,g):
		if g is None:return
		self.add(g);self.no_snap.add(g);self.links.pop(g,None)
		for f,l in list(self.links.items()):
			if l is g:self.links.pop(f,None)
	def attach(self,a,leader):
		if a is None or leader is None or a is leader:return
		self.skip_gump(a,keep_fresh=True);self.attached[a]=leader;self._fmap=None;self.add(leader)
	def detach(self,a):
		self._fmap=None
		if self.attached.pop(a,None)is not None and Kit.is_open(a):self.add(a)
	def followers(self,g):
		a=self._fmap
		if a is not None:b=a.get(g);return list(b)if b else[]
		c=[]
		for f,l in list(self.attached.items()):
			if not Kit.is_open(f):self._forget(f)
			elif l is g:c.append(f)
		return c
	def _forget(self,g):
		if g in self.dragged:
			k,r=self.drag_key.get(g),self.drag_rect.get(g)
			if k is not None and r is not None:self.lost[g]=(k,r)
		for d in(self.drag_key,self.drag_rect,self.drag,self.by_code,self.links,self.moved_cb):d.pop(g,None)
		for s in(self.members,Kit._pinned,self.moved,self.dragged,self.no_snap):s.discard(g)
		self._fmap=None;self.attached.pop(g,None)
		for f,l in list(self.attached.items()):
			if l is g:self.attached.pop(f,None)
		if self.last is not None:self.last.pop(g,None)
	def _prune(self):
		a=[]
		for g in self.gumps:
			if Kit.is_open(g):a.append(g)
			else:self._forget(g)
		self.gumps=a;return a
	def pressed(self):
		if self.button is None:
			self.button=False
			try:m=Client._member(Client._type("ClassicUO.Input.Mouse"),"LButtonPressed");bool(m[0]());self.button=m[0]
			except Exception:pass
		if not self.button:return
		try:v=self.button()
		except Exception:return
		return None if v is None else bool(v)
	@staticmethod
	def rect(g):r=Kit.rect(g);return r if r is not None and r[2]>0 and r[3]>0 else None
	@staticmethod
	def pos(g):return Kit.pos(g)
	@staticmethod
	def visible(g):return bool(g.IsVisible)
	@staticmethod
	def move(g,x,y):g.SetPos(int(x),int(y));Kit.note_rect(g,x,y)
	def tick(self,now=None):
		now=time.time()if now is None else now
		if now<self.next and self.next-now<=SNAP_EVERY:return
		self.next=now+SNAP_EVERY
		if LAYOUT.arrange and not self.drag and API.IsKeyPressed("ESCAPE"):LAYOUT.set_arrange(False)
		a=self.pressed();self.down=a is not False or bool(self.drag)
		if a is not True:
			if now>=self.keep_at:
				self.keep_at=now+KEEP_EVERY
				if now>=self.sweep_at or self._keep_sig()!=self.keep_sig:self.sweep_at=now+KEEP_SWEEP;self.keep();self.keep_sig=self._keep_sig()
			elif LAYOUT.assign and(LAYOUT.fresh or LAYOUT.fresh_adds or LAYOUT.retry_due(now)):self.keep(light=bool(LAYOUT.fresh_adds)and not LAYOUT.fresh)
		if a is False and not self.drag:
			self.last=None
			if now>=self.prune_at:self.prune_at=now+SNAP_PRUNE;self._prune()
			return
		if a is not True or now>=self.prune_at:self.prune_at=now+SNAP_PRUNE;e=self._prune()
		else:e=self.gumps
		b=self.last
		if b is None:
			b=self.last={}
			for g in e:
				p=self.pos(g)
				if p is not None:b[g]=p
			return
		d=self.drag;c=self.by_code
		if c:
			for g in[j for j,k in c.items()if now-k>1.]:del c[g]
		for g in e:
			p=self.pos(g)
			if p is None:continue
			f=b.get(g)
			if f is None:b[g]=p;continue
			if p!=f:
				h,i=p[0]-f[0],p[1]-f[1];b[g]=p
				if c and g in c:del c[g];continue
				if a is False:continue
				d[g]=now;self.moved.add(g);self.dragged.add(g);r=None
				if LAYOUT.loaded:
					if g not in self.drag_key:self.drag_key[g]=LAYOUT._key_of(g)
					r=self.rect(g)
					if r is not None:self.drag_rect[g]=r
				if LAYOUT.arrange:LAYOUT.arrange_hover(g,r)
				if self.enabled and g not in self.no_snap and g not in LAYOUT.held:self.follow(g,h,i,set([g]))
			elif g in d:
				if a is False or(a is None and now-d[g]>=SNAP_SETTLE):
					del d[g]
					if self.enabled and g not in self.no_snap and not LAYOUT.takes(g):self.snap(g,e)
		if(self.moved or self.lost)and not d:self._tell_moved()
	def follow(self,leader,dx,dy,seen):
		a=self.links
		if not a:return
		b=LAYOUT.held
		for g in self.gumps:
			if g in seen or a.get(g)is not leader:continue
			if g in b:a.pop(g,None);continue
			p=self.pos(g)
			if p is None:continue
			seen.add(g);self.move(g,p[0]+dx,p[1]+dy)
			if self.last is not None:self.last[g]=(p[0]+dx,p[1]+dy)
			self.moved.add(g);self.follow(g,dx,dy,seen)
	def snap(self,g,live):
		if self._fmap is not None:return self._snap(g,live)
		self._build_fmap()
		try:return self._snap(g,live)
		finally:self._fmap=None
	def _snap(self,g,live):
		u=self.rect(g)
		if u is None:return
		x,y,w,h=u;f=None;k=l=None;p=self.links;q=[]
		for o in live:
			if o is g or p.get(o)is g or not self.visible(o)or o in self.no_snap:continue
			q.append((o,o))
			for r in self.followers(o):
				if r is not g and self.visible(r):q.append((r,o))
		for o,s in q:
			v=self.rect(o)
			if v is None:continue
			a,b,i,j=v
			for m,n in((a+i,b),(a+i,b+j-h),(a-w,b),(a-w,b+j-h),(a,b+j),(a+i-w,b+j),(a,b-h),(a+i-w,b-h)):
				d=max(abs(x-m),abs(y-n))
				if d<=SNAP_DIST and(f is None or d<f[0]):f=(d,m,n,s)
			if y<b+j+SNAP_DIST and b<y+h+SNAP_DIST:
				for m in(a+i,a-w,a,a+i-w):
					d=abs(x-m)
					if d<=SNAP_DIST and(k is None or d<k[0]):k=(d,m,s)
			if x<a+i+SNAP_DIST and a<x+w+SNAP_DIST:
				for n in(b+j,b-h,b,b+j-h):
					d=abs(y-n)
					if d<=SNAP_DIST and(l is None or d<l[0]):l=(d,n,s)
		if f is not None:c,e,t=f[1],f[2],f[3]
		else:c=k[1]if k else x;e=l[1]if l else y;t=(k or l or(None,None,None))[2]
		if t is None:p.pop(g,None);c,e=self.snap_screen(x,y,w,h)
		else:p[g]=t
		c,e=Kit.clamp(c,e,w,h)
		if(c,e)!=(x,y):
			self.move(g,c,e)
			if self.last is not None:self.last[g]=(c,e)
			self.follow(g,c-x,e-y,set([g]))
	def _keep_sig(self):
		if self.down or Kit._pend or LAYOUT.arrange or LAYOUT.dirty or LAYOUT.fresh or LAYOUT.fresh_adds:return object()
		a=[Kit.screen(),safe(LAYOUT.occupied)]
		for g in self.gumps+list(self.attached)+[b for b in ClientWin.found.values()if b is not None]:
			try:a.append((id(g),Kit.is_open(g),Kit.rect(g),bool(g.IsVisible)))
			except Exception:a.append(id(g))
		return a
	def keep(self,light=False):
		W,H=Kit.screen()
		if W<=0 or H<=0:return
		a=self._prune();Kit.prune_pending()
		try:self._keep_body(W,H,a,light)
		finally:self._fmap=None
	def _build_fmap(self):
		a={}
		for f,l in list(self.attached.items()):
			if not Kit.is_open(f):self._forget(f)
			else:
				b=a.get(l)
				if b is None:a[l]=[f]
				else:b.append(f)
		self._fmap=a
	def _keep_body(self,W,H,live,light=False):
		self._build_fmap();a=None
		if light:
			a=set(LAYOUT.fresh_adds);e=self.attached
			for g in list(a):
				l=e.get(g)
				if l is not None:a.add(l)
		try:Kit.scroll_sweep()
		except Exception:pass
		b=self.screen
		if b!=(W,H):
			a=None;self.screen=(W,H)
			if b is not None:
				for g in live:
					if g in self.drag:continue
					r=self.rect(g)
					if r is None:continue
					x,y,w,h=r;c=Kit.remap_axis(x,w,b[0],W);d=Kit.remap_axis(y,h,b[1],H)
					if(c,d)!=(x,y):self._shift(g,c-x,d-y)
			Kit.note_screen((W,H))
		f=LAYOUT.held
		for g in live:
			if a is not None and g not in a:continue
			if g not in self.drag and g not in f:self.keep_one(g)
		try:LAYOUT.keep(W,H,a)
		except Exception as i:HOST._tell("%s: layout error: %s%s"%(APP_NAME,i,_error_where()))
		if(self.moved or self.lost)and not self.drag:self._tell_moved()
	def keep_one(self,g):
		r=self.rect(g)
		if r is None:return False
		b,c,d,e=r[0],r[1],r[0]+r[2],r[1]+r[3]
		for f in self.followers(g):
			a=self.rect(f)
			if a is not None and self.visible(f):b,c=min(b,a[0]),min(c,a[1]);d,e=max(d,a[0]+a[2]),max(e,a[1]+a[3])
		h,i=Kit.clamp(b,c,d-b,e-c)
		if(h,i)==(b,c):return False
		self._shift(g,h-b,i-c);return True
	def _shift(self,g,dx,dy):
		for w in[g]+self.followers(g):
			p=self.pos(w)
			if p is None:continue
			self.move(w,p[0]+dx,p[1]+dy)
			if self.last is not None:self.last[w]=(p[0]+dx,p[1]+dy)
		self.moved.add(g)
	@staticmethod
	def near_anchor(x,y,w,h):b=[(max(abs(c-x),abs(d-y)),c,d)for c,d in Kit.anchor_targets(w,h)];a=min(b,key=_first)if b else None;return a if a is not None and a[0]<=SNAP_ANCHOR else None
	def snap_screen(self,x,y,w,h):
		W,H=Kit.screen()
		if W<=0 or H<=0:return x,y
		c=Snap.near_anchor(x,y,w,h)
		if c is not None:return c[1],c[2]
		a,b=x,y
		for d in(0,max(0,W-w)):
			if abs(d-x)<=SNAP_DIST:a=d
		for e in(0,max(0,H-h)):
			if abs(e-y)<=SNAP_DIST:b=e
		if HOST.grid_shown():
			f=HOST.grid_size()
			def g(lo,size,cur):
				a=[]
				for b,d in((lo,0),(lo+size,size)):
					c=int(round(float(b)/f))*f
					if abs(c-b)<=SNAP_DIST:a.append((abs(c-b),c-d))
				return min(a)[1]if a and cur==lo else cur
			a,b=g(x,w,a),g(y,h,b)
		return a,b
class Grid(object):
	MINOR,MAJOR=.16,.34;CROSS,MARK=.55,.75;MARK_W=10
	def __init__(self,host):self.host=host;self.g=None;self.shown=False;self.drawn=None
	@staticmethod
	def show_overlay(g,x,y,w,h,a=False):
		g.SetRect(x,y,w,h);g.SetAcceptMouseInput(False);g.CanMove=False
		if a:
			with Kit.quiet:import System;g.LayerOrder=System.Enum.Parse(g.LayerOrder.GetType(),"Under")
		G.AddGump(g);SNAP.skip_gump(g)
	def toggle(self):self.hide()if self.shown else self.show()
	def show(self):self.shown=True;Kit.on_client(self.build)
	def hide(self):self.shown=False;g,self.g=self.g,None;Kit.dispose(g)
	def redraw(self):
		if self.shown:Kit.on_client(self.build)
	def tick(self):
		if self.shown and self.drawn is not None:
			W,H=Kit.screen()
			if(W,H,self.host.grid_size())!=self.drawn:self.redraw()
	def build(self):
		W,H=Kit.screen();a=self.host.grid_size();b,self.g=self.g,None
		if W<=0 or H<=0:Kit.dispose(b);return
		g=G.CreateGump(False,False)
		for n,x in enumerate(range(a,W,a),1):Kit.add_box(g,x,0,1,H,self.MAJOR if n%4==0 else self.MINOR)
		for n,y in enumerate(range(a,H,a),1):Kit.add_box(g,0,y,W,1,self.MAJOR if n%4==0 else self.MINOR)
		Kit.add_box(g,W//2,0,1,H,self.CROSS,"#FFD700");Kit.add_box(g,0,H//2,W,1,self.CROSS,"#FFD700");m=self.MARK_W
		for c,d in Kit.anchor_targets(m,m):Kit.add_box(g,c,d,m,m,self.MARK,"#FFD700")
		Kit.add_label(g,"GRID %d px: windows snap to its lines, the screen's corners, edges and centre  (the Action Bar's Grid button hides it)"%a,m+8,m+4,Kit.HUE_TITLE);self.g=g;self.drawn=(W,H,a);Grid.show_overlay(g,0,0,W,H,True);Kit.dispose(b)
LAYOUT_VAR="VirtueAssistant_layout"
LAYOUT_ACTIVE="VirtueAssistant_layout_active"
LAYOUT_LIST="VirtueAssistant_layout_list"
LAYOUT_NAMED="VirtueAssistant_layout_%s"
FRAMES_ACTIVE="VirtueAssistant_frames_active"
FRAMES_LIST="VirtueAssistant_frames_list"
FRAMES_NAMED="VirtueAssistant_frames_%s"
LAYOUT_OPTS="VirtueAssistant_layout_opts"
LAYOUT_DEFAULT="Default"
LAYOUT_MIRRORED="Mirrored"
LAYOUT_MINE="Default (mine)"
LAYOUT_GONE=frozenset(("spelltimers","bandage","swing"))
WINDOWS_DEFAULT=("L1=character;L2=bag;C1=unitframes.player;C2=unitframes.target;C4=actionbar;R1=worldmap;R2=ultima.friend,ultima.neutral,ultima.foe;R3=meters")
WINDOWS_MIRRORED=("L1=worldmap;L2=ultima.friend,ultima.neutral,ultima.foe,meters;C1=unitframes.player;C2=unitframes.target;C4=actionbar;R1=character;R2=bag")
SIDE_MIN,SIDE_MAX,SIDE_SHARE=240,440,.22
SPILL_MIN,SPILL_MAX,SPILL_SHARE=240,360,.12
CENTRE_MIN_SHARE=.4
TOP_MIN,TOP_MAX,BOT_MIN,BOT_MAX,STRIP_SHARE=110,180,100,160,.14
LEFT_SLOTS=(("L1",.32,260,"w",2),("L2",.38,180,"w",1),("L3",.3,160,"r",0))
RIGHT_SLOTS=(("R1",.32,200,"w",2),("R2",.4,240,"w",3),("R3",.28,120,"w",1))
MINI_BAR=46
ZONE_MIN_W,ZONE_MIN_H=96,64
ZONE_COLORS={"w":"#3A78C8","k":"#3AA060","r":"#C88A3A"}
ZONE_KINDS=(("w","window"),("k","keep clear"),("r","reserved"))
ZONE_STACKS=(("d","down"),("u","up"),("r","right"),("l","left"))
SHRINK_MAX=6
LAYOUT_OWNER="interface"
SEAM_PAD=6
REVEAL_H=14
REVEAL_HOLD=.6
SEAM_WAIT=2.
SEAM_RETRY=.1
def ratio_class(W,H):
	if W<=0 or H<=0:return "wide"
	r=float(W)/float(H);return "narrow"if r<1.5 else "wide"if r<2. else "ultrawide"
def _clampv(v,lo,hi):return max(lo,min(hi,v))
def _ordinal(n):
	n=int(n)
	if n<=0:return "never"
	if n%100 in(11,12,13):return "%dth"%n
	return "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n%10,"th"))
class Zone(object):
	__slots__=("id","kind","rect","pins","min","stack","prio","px","squeezed","fit","hug","arch","overlap","lock","solo","free","exact")
	def __init__(self,id,kind="w",rect=(0,0,200,200),pins="",mins=(0,0),stack="d",prio=0,fit="w",hug=False,arch=False,overlap=False,lock=False,solo=False,free=False):self.id=str(id);self.kind=kind if kind in("w","k","r")else "w";self.rect=tuple(int(a)for a in rect);self.pins="".join(b for b in str(pins or "").upper()if b in "LTRBXY");self.min=(int(mins[0]),int(mins[1]));self.stack=stack if stack in("d","u","r","l")else "d";self.prio=max(0,min(SHRINK_MAX,int(prio)));self.fit=fit if fit in("w","s","n")else "w";self.hug=bool(hug)and self.kind=="w";self.arch=bool(arch)and self.kind=="k";self.overlap=bool(overlap);self.lock=bool(lock);self.solo=bool(solo);self.free=bool(free);self.px=None;self.squeezed=False;self.exact=None
	def kind_name(self):return dict(ZONE_KINDS)[self.kind]
	def stack_name(self):return dict(ZONE_STACKS)[self.stack]
	def copy(self):z=Zone(self.id,self.kind,self.rect,self.pins,self.min,self.stack,self.prio,self.fit,self.hug,self.arch,self.overlap,self.lock,self.solo,self.free);z.px=tuple(self.px)if self.px else None;z.exact=self.exact;return z
	def set_px(self,x,y,w,h,W,H):
		w,h=max(1,int(w)),max(1,int(h))
		if W>0:w=min(w,W);x=_clampv(int(x),0,W-w)
		if H>0:h=min(h,H);y=_clampv(int(y),0,H-h)
		self.px=(int(x),int(y),w,h)
		if W>0 and H>0:self.rect=(int(round(1000.*x/W)),int(round(1000.*y/H)),int(round(1000.*w/W)),int(round(1000.*h/H)));self.exact=self.px+(int(W),int(H))
	def note_pins(self,W,H):
		if not self.px or W<=0 or H<=0:return
		x,y,w,h=self.px;a=.5 if self.free else SNAP_DIST;self.pins="".join(b for b,e in(("L",x),("T",y),("R",W-(x+w)),("B",H-(y+h)),("X",abs((x+w/2.)-W/2.)),("Y",abs((y+h/2.)-H/2.)))if e<=a)
	def save_text(self):
		b=(self.hug,self.arch,self.overlap,self.lock,self.solo,self.free);n=(6 if self.free else 5 if self.solo else 4 if self.overlap or self.lock else 2 if self.hug or self.arch else 0);a="".join(":%d"%c for c in b[:n])
		if self.free and self.exact:a+=":%d,%d,%d,%d,%d,%d"%self.exact
		return "%s:%s:%d,%d,%d,%d:%s:%d,%d:%s:%d:%s%s"%(self.id.replace(":"," ").replace(";"," "),self.kind,self.rect[0],self.rect[1],self.rect[2],self.rect[3],self.pins,self.min[0],self.min[1],self.stack,self.prio,self.fit,a)
	@staticmethod
	def parse(text):
		try:
			f=text.split(":")
			if len(f)<7 or not f[0].strip():return
			a=[int(l)for l in f[2].split(",")];b=[int(m)for m in f[4].split(",")]
			if len(a)!=4 or len(b)!=2 or a[2]<=0 or a[3]<=0:return
			d=f[7].strip()if len(f)>7 else "w";g,h,i,j,k,c=[len(f)>n and f[n].strip()=="1"for n in range(8,14)];z=Zone(f[0].strip(),f[1].strip(),a,f[3],b,f[5].strip(),int(f[6]),d,g,h,i,j,k,c);e=f[14].strip()if c and len(f)>14 else ""
			if re.match(r"^\d+(,\d+){5}$",e):
				e=tuple(int(o)for o in e.split(","))
				if e[2]>0 and e[3]>0 and e[4]>0 and e[5]>0:z.exact=e
			return z
		except Exception:return
class ZoneSet(object):
	def __init__(self,name,zones=None,grid=GRID_DEFAULT,screen=(0,0),generated=False):self.name=str(name);self.zones=list(zones or[]);self.grid=int(grid or GRID_DEFAULT);self.screen=(int(screen[0]),int(screen[1]));self.generated=generated;self.skipped=[];self.ver=2;self.needs={}
	def by_id(self,a):
		for z in self.zones:
			if z.id==a:return z
		return
	def ids(self):return[a.id for a in self.zones]
	def copy(self,name=None):a=ZoneSet(name or self.name,[b.copy()for b in self.zones],self.grid,self.screen,self.generated);a.ver=self.ver;return a
	def save_text(self):return "grid=%d,screen=%dx%d,v=%d;"%(self.grid,self.screen[0],self.screen[1],self.ver)+";".join(a.save_text()for a in self.zones)
	@staticmethod
	def parse(name,text):
		text=str(text or "").strip()
		if not text:return
		b=text.split(";");c,d,e=GRID_DEFAULT,(0,0),1;f=b[0]
		if f.startswith("grid="):
			b=b[1:]
			for g in f.split(","):
				with Kit.quiet:
					k,v=g.split("=",1)
					if k=="grid":c=int(v)
					elif k=="screen":w,h=v.lower().split("x");d=(int(w),int(h))
					elif k=="v":e=int(v)
		a=ZoneSet(name,[],c,d);a.ver=e
		for p in b:
			if not p.strip():continue
			z=Zone.parse(p)
			if z is None:a.skipped.append(p.split(":")[0].strip()or "?")
			elif a.by_id(z.id)is None:a.zones.append(z)
		return a
	@staticmethod
	def default(W,H,c=(),r=True):
		i=ZoneSet(LAYOUT_DEFAULT,[],GRID_DEFAULT,(W,H),generated=True)
		if W<=0 or H<=0:return i
		c=set(c);p=ratio_class(W,H)
		if p=="narrow":b,a=SIDE_MIN,0
		else:b=int(_clampv(SIDE_SHARE*W,SIDE_MIN,SIDE_MAX));a=(int(_clampv(SPILL_SHARE*W,SPILL_MIN,SPILL_MAX))if p=="ultrawide"else 0)
		if W-2*b-2*a<CENTRE_MIN_SHARE*W:
			a=0
			if W-2*b<CENTRE_MIN_SHARE*W:b=max(SIDE_MIN,int((W-CENTRE_MIN_SHARE*W)/2))
		s,t=a,W-a-b;d,f=a+b,W-2*(a+b);j=int(_clampv(STRIP_SHARE*H,TOP_MIN,TOP_MAX));k=int(_clampv(STRIP_SHARE*H,BOT_MIN,BOT_MAX))
		def e(z,x,y,w,h):z.set_px(x,y,w,h,W,H);z.note_pins(W,H);i.zones.append(z);return z
		def q(x,slots):
			a=ZoneSet._band_heights(H,slots,c);y=0
			for(d,k,f,g,i),(h,j)in zip(slots,a):e(Zone(d,g,(0,0,1,1),"",(SIDE_MIN,f),"d",i),x,y,b,h).squeezed=j;y+=h
		q(s,LEFT_SLOTS);l=f//2
		for m,n,u,v in(("C1",d,l,3),("C2",d+l,f-l,2)):e(Zone(m,"w",(0,0,1,1),"T",(300,TOP_MIN),"d",v),n,0,u,j)
		o,g=d,f
		if r:
			if not any(A[0]in c for A in LEFT_SLOTS if A[3]=="w"):o,g=0,g+d
			if not any(B[0]in c for B in RIGHT_SLOTS if B[3]=="w"):g=W-o
		e(Zone("C3","k",(0,0,1,1),"XY",(0,0),"d",0),o,j,g,H-j-k);e(Zone("C4","w",(0,0,1,1),"B",(600,BOT_MIN),"r",1),d,H-k,f,k);q(t,RIGHT_SLOTS)
		if a:
			for m,n in(("L0",0),("R0",W-a)):e(Zone(m,"w",(0,0,1,1),"",(SPILL_MIN,120),"d",1),n,0,a,H)
		return i
	@staticmethod
	def _band_heights(H,slots,o):
		n=len(slots);e=H;s=any(E in o for E,I,J,F,K in slots if F=="w");c,b=[],[]
		for t,u,v,w,B in slots:p=w=="w"and t not in o and s;c.append(0. if p else float(u));b.append(46 if p else int(v))
		l=[False]*n;q=sorted([L for L in range(n)if slots[L][4]>0 and slots[L][3]=="w"],key=lambda i:slots[i][4])
		while sum(b)>e and q:
			a=q.pop(0)
			if b[a]>MINI_BAR:b[a]=MINI_BAR;l[a]=True;c[a]=0.
		x=sum(c)or 1.;h=[e*M/x for M in c]
		for C in range(n):
			m=[(N,b[N]-h[N])for N in range(n)if h[N]<b[N]]
			if not m:break
			y=sum(O for P,O in m);z=set(Q for Q,R in m)
			for a,D in m:h[a]=b[a]
			r=[S for S in range(n)if S not in z and h[S]>b[S]];d=sum(h[T]-b[T]for T in r)
			if d<=0:break
			A=min(y,d)
			for a in r:h[a]-=A*(h[a]-b[a])/d
		for a in range(n):
			if slots[a][3]=="r"and h[a]>slots[a][1]*e:
				j,h[a]=h[a]-slots[a][1]*e,slots[a][1]*e;f=[U for U in range(n)if slots[U][3]=="w"and not l[U]and c[U]>0]
				if f:
					d=sum(c[V]for V in f)or 1.
					for k in f:h[k]+=j*c[k]/d
				else:
					f=[W for W in range(n)if slots[W][3]=="w"and not l[W]];d=sum(slots[X][1]for X in f)or 1.
					for k in f:h[k]+=j*slots[k][1]/d
		g=[int(round(Y))for Y in h];j=e-sum(g)
		if g and j:g[g.index(max(g))]+=j
		return[(max(1,g[Z]),l[Z])for Z in range(n)]
	def reflow(self,W,H,step):
		if W<=0 or H<=0:return
		step=max(8,int(step or GRID_DEFAULT))
		if self.needs:
			D=[(P,P.rect,P.exact)for P in self.zones];self.needs,E={},self.needs;self.reflow(W,H,step);self.needs=E;self._apply_needs(W,H);self._keep_clear(W,H)
			for z,F,e in D:z.rect,z.exact=F,e
			return
		G,I=self.screen if self.screen[0]>0 and self.screen[1]>0 else(W,H);J=self._flush_pairs(G,I)
		def j(v,b,free):a=1 if free else step;return _clampv(int(round(float(v)/a))*a,0,b)
		k=set()
		for z in self.zones:
			o,t,w,h=z.rect;g=z.free;e=z.exact if g and z.exact and z.exact[4:]==(W,H)else None
			if e is not None:k.add(z.id);a,b,c,d=e[0],e[1],e[0]+e[2],e[1]+e[3]
			else:a,b=j(W*o/1000.,W,g),j(H*t/1000.,H,g);c,d=j(W*(o+w)/1000.,W,g),j(H*(t+h)/1000.,H,g)
			if g:z.pins="".join(Q for Q,R in(("L",a<=0),("T",b<=0),("R",c>=W),("B",d>=H))if R)
			if "L"in z.pins:a=0
			if "T"in z.pins:b=0
			if "R"in z.pins:c=W
			if "B"in z.pins:d=H
			if "X"in z.pins and "L"not in z.pins and "R"not in z.pins:i=(c-a)//2;a,c=W//2-i,W//2-i+(c-a)
			if "Y"in z.pins and "T"not in z.pins and "B"not in z.pins:i=(d-b)//2;b,d=H//2-i,H//2-i+(d-b)
			z.px=(a,b,max(1,c-a),max(1,d-b))
		for p,q,K in J:
			l,f=self.by_id(p),self.by_id(q)
			if l is None or f is None or l.px is None or f.px is None or(p in k and q in k):continue
			L,M,N,O=l.px;r,s,u,x=f.px
			if K=="h":
				m=L+N;y=W if "R"in f.pins else r+u
				if y-m>=ZONE_MIN_W:f.px=(m,s,y-m,x)
			else:
				n=M+O;A=H if "B"in f.pins else s+x
				if A-n>=ZONE_MIN_H:f.px=(r,n,u,A-n)
		for z in self.zones:
			if z.kind=="k":continue
			B,C,w,h=z.px
			if w<z.min[0]:w=min(z.min[0],max(w,self._free(z,0,W)-B))
			if h<z.min[1]:h=min(z.min[1],max(h,self._free(z,1,H)-C))
			z.set_px(B,C,w,h,W,H);z.squeezed=z.prio>0 and z.px[3]<z.min[1]
		for z in self.zones:
			if z.kind!="k"and not z.overlap and self.overlaps(z):self.push_clear(z,W,H)
		for z in self.zones:
			if z.kind=="k"and not z.overlap:z.set_px(*(ZoneSet.cut_clear(z,self.zones)+(W,H)))
		for z in self.zones:z.set_px(z.px[0],z.px[1],z.px[2],z.px[3],W,H)
		self.screen=(W,H)
	@staticmethod
	def cut_clear(z,zones):
		x,y,w,h=z.px
		for o in zones:
			if o is z or o.kind!="w"or o.px is None:continue
			b,c,e,f=o.px
			if b<x+w and x<b+e and c<y+h and y<c+f:
				a,d=min([(x+w-b,"R"),((b+e)-x,"L"),(y+h-c,"B"),((c+f)-y,"T")])
				if d=="R":w-=a
				elif d=="L":x,w=x+a,w-a
				elif d=="B":h-=a
				else:y,h=y+a,h-a
				if w<ZONE_MIN_W or h<ZONE_MIN_H:x,y,w,h=z.px;break
		return x,y,max(1,w),max(1,h)
	def _flush_pairs(self,W,H):
		c=[];d={}
		for z in self.zones:l,t,w,m=z.rect;d[z.id]=(W*l/1000.,H*t/1000.,W*w/1000.,H*m/1000.)
		for a in self.zones:
			e,f,i,j=d[a.id]
			for b in self.zones:
				if a is b:continue
				g,h,n,o=d[b.id];q=a.free or b.free;r,s=(1.+W/1000.,1.+H/1000.)if q else(SNAP_DIST,SNAP_DIST)
				if abs(g-(e+i))<=r and h<f+j and f<h+o:c.append((a.id,b.id,"h"))
				if abs(h-(f+j))<=s and g<e+i and e<g+n:c.append((a.id,b.id,"v"))
		def k(a):z=self.by_id(a);return-len(z.pins)if z else 0
		c.sort(key=lambda p:(k(p[0]),k(p[1])));return c
	def _free(self,z,i,lim):
		r,j=z.px,1-i
		for o in self.zones:
			if o is z or o.kind=="k"or o.px is None:continue
			p=o.px
			if p[i]>=r[i]+r[i+2]and p[j]<r[j]+r[j+2]and r[j]<p[j]+p[j+2]:lim=min(lim,p[i])
		return lim
	def overlaps(self,z,px=None):
		x,y,w,h=px or z.px;a=[]
		if z.overlap:return a
		for o in self.zones:
			if o is z or o.px is None or o.overlap:continue
			if(z.kind=="r"and o.kind=="k")or(z.kind=="k"and o.kind=="r"):continue
			b,c,d,e=o.px
			if b<x+w and x<b+d and c<y+h and y<c+e:a.append(o)
		return a
	def push_clear(self,z,W,H,step=None):
		for m in range(12):
			f=self.overlaps(z)
			if not f:return True
			x,y,w,h=z.px;a=[]
			for o in f:
				g,i,k,l=o.px
				for b,c in(((g-w),y),((g+k),y),(x,(i-h)),(x,(i+l))):
					if not(0<=b<=W-w and 0<=c<=H-h):continue
					j=not self.overlaps(z,(b,c,w,h))
					if j and step:
						d,e=(int(round(float(b)/step))*step,int(round(float(c)/step))*step)
						if(0<=d<=W-w and 0<=e<=H-h and not self.overlaps(z,(d,e,w,h))):b,c=d,e
					a.append((0 if j else 1,abs(b-x)+abs(c-y),b,c))
			if not a:return False
			a.sort();z.set_px(a[0][2],a[0][3],w,h,W,H)
			if a[0][0]==0:return True
		return not self.overlaps(z)
	def _keep_clear(self,W,H):
		for z in self.zones:
			if z.kind!="k"or z.overlap or z.px is None:continue
			x,y,w,h=z.px
			for o in self.zones:
				if o is z or o.kind!="w"or o.px is None:continue
				a,b,c,d=o.px
				if a>=x+w or x>=a+c or b>=y+h or y>=b+d:continue
				if b+d>=y+h and b>y:h=b-y
				elif b<=y and b+d<y+h:h,y=h-(b+d-y),b+d
				elif a+c>=x+w and a>x:w=a-x
				elif a<=x and a+c<x+w:w,x=w-(a+c-x),a+c
			z.px=(x,y,max(1,w),max(1,h))
	def _apply_needs(self,W,H):
		for z in self.zones:
			e=self.needs.get(z.id)
			if e is None or z.px is None or z.kind=="k":continue
			r=list(z.px)
			for i,k,S in((1,"B",H),(0,"R",W)):
				n,a,s,j=e[i],r[i],r[i+2],1-i
				if not n or n<=s:continue
				f=min(n-s,S-s);g=[l for l in self.zones if l is not z and l.kind=="w"and not l.overlap and l.px is not None and l.px[j]<r[j]+r[j+2]and r[j]<l.px[j]+l.px[j+2]]
				if k in z.pins or a+s/2.>=S/2.:
					b=max(0,a-f)
					for o in g:
						p=list(o.px)
						if p[i]<a and p[i]+p[i+2]>b:h=max(p[i]+max(o.min[i],1),b);p[i+2]=h-p[i];o.px=tuple(p);b=max(b,h)
					r[i],r[i+2]=b,s+(a-b)
				else:
					c=min(S,a+s+f)
					for o in g:
						p=list(o.px)
						if p[i]>=a+s and p[i]<c:d=min(p[i]+p[i+2]-max(o.min[i],1),c);p[i],p[i+2]=d,p[i]+p[i+2]-d;o.px=tuple(p);c=min(c,d)
					r[i+2]=c-a
			z.px=tuple(r)
	def fill_gaps(self,W,H,step):
		step=max(8,int(step or GRID_DEFAULT));d=sorted(self.zones,key=lambda z:{"w":0,"r":1,"k":2}[z.kind])
		for a in d:
			if a.overlap or a.lock:continue
			r=list(a.px);b=1 if a.free else step
			for i,f,g,S in((0,"L","R",W),(1,"T","B",H)):
				c=max([0]+[h.px[i]+h.px[i+2]for h in self.overlaps_side(a,f)]);n=0 if c==0 else((c+b-1)//b)*b
				if n<r[i]:r[i],r[i+2]=n,r[i+2]+(r[i]-n)
				c=min([S]+[j.px[i]for j in self.overlaps_side(a,g)]);e=S if c==S else(c//b)*b
				if e>r[i]+r[i+2]:r[i+2]=e-r[i]
			a.set_px(r[0],r[1],r[2],r[3],W,H)
	def overlaps_side(self,z,side):i=0 if side in("L","R")else 1;j,r=1-i,z.px;return[a for a in self.zones if a is not z and a.px is not None and set((z.kind,a.kind))!=set(("r","k"))and a.px[j]<r[j]+r[j+2]and r[j]<a.px[j]+a.px[j+2]and(a.px[i]+a.px[i+2]<=r[i]if side in("L","T")else a.px[i]>=r[i]+r[i+2])]
	def even_out(self,z,W,H,step):
		step=max(8,int(step or GRID_DEFAULT));D=SNAP_DIST
		def h(f):
			e=[l for l in self.zones if l.kind=="w"and l.px is not None and((abs(l.px[1]-z.px[1])<=D and abs(l.px[3]-z.px[3])<=D)if f else(abs(l.px[0]-z.px[0])<=D and abs(l.px[2]-z.px[2])<=D))];i=0 if f else 1;e.sort(key=lambda o:o.px[i]);c=[z]
			for g in(1,-1):
				d=z
				for h in range(len(e)):
					b=None
					for a in e:
						if a in c:continue
						if g==1 and abs(a.px[i]-(d.px[i]+d.px[i+2]))<=D:b=a
						elif g==-1 and abs(a.px[i]+a.px[i+2]-d.px[i])<=D:b=a
					if b is None:break
					c.append(b);d=b
			c.sort(key=lambda o:o.px[i]);return c,i
		a,i=h(True)
		if len(a)<2:a,i=h(False)
		if len(a)<2:return len(a)
		c=a[0].px[i];d=a[-1].px[i]+a[-1].px[i+2];n=len(a);b=[c]
		for k in range(1,n):e=c+(d-c)*k/float(n);g=int(round(e/step))*step;b.append(g if abs(g-e)<=step/2. and b[-1]<g<d else int(round(e)))
		b.append(d)
		for k,f in enumerate(a):
			x,y,w,j=f.px
			if i==0:f.set_px(b[k],y,b[k+1]-b[k],j,W,H)
			else:f.set_px(x,b[k],w,b[k+1]-b[k],W,H)
		return n
	def new_id(self):
		n=len(self.zones)+1
		while self.by_id("Zone %d"%n)is not None:n+=1
		return "Zone %d"%n
class ClientWin(object):
	KINDS={"worldmap":("WorldMapGump",),"journal":("ResizableJournal",)};TITLES={"worldmap":"TazUO's World Map","journal":"TazUO's journal"};INSET={"worldmap":4};DROPS=("worldmap",);LOOK_EVERY=1.;LOCK_VAR="Layout_client_locked_%s";found={};looked={};errors={};_pt=[None];_bf=[None]
	@staticmethod
	def point(x,y):
		import System;t=ClientWin._pt[0]
		if t is None:t=ClientWin._pt[0]=Tz.T("ClassicUO.Game.UI.Controls.Control").GetProperty("Location").PropertyType
		return System.Activator.CreateInstance(t,System.Array[object]([int(x),int(y)]))
	@staticmethod
	def bounds(raw):
		f=ClientWin._bf[0]
		if f is None:f=ClientWin._bf[0]=Tz.T("ClassicUO.Game.UI.Controls.Control").GetField("_bounds",Client.flags(public=False))
		return f.GetValue(raw)
	def __init__(self,kind,raw):self.kind,self.raw=kind,raw;self.own=None;self.tries=0;self.fail={};self.warned=False;self.mins=None;self._rc=None
	@staticmethod
	def of(kind):
		a=ClientWin.found.get(kind)
		if a is not None and a.IsDisposed:a=ClientWin.found[kind]=None
		if a is not None:return a
		b=time.time()
		if b-ClientWin.looked.get(kind,0.)<ClientWin.LOOK_EVERY:return
		ClientWin.looked[kind]=b
		try:c=Tz.windows(ClientWin.KINDS[kind]);ClientWin.errors.pop(kind,None)
		except Exception as e:c=[];ClientWin.errors[kind]=Tz.why(e)
		for d in c:
			with Kit.quiet:
				if not d.IsDisposed:a=ClientWin(kind,d);break
		ClientWin.found[kind]=a;return a
	@property
	def IsDisposed(self):
		try:return bool(self.raw.IsDisposed)
		except Exception:return True
	@property
	def IsVisible(self):
		try:return bool(self.raw.IsVisible)
		except Exception:return False
	def rect(self):
		a=HOST.in_hop
		if a:
			c=self._rc
			if c is not None and c[0]==HOST.pass_id:return c[1]
		b=ClientWin.bounds(self.raw);r=(int(b.X),int(b.Y),int(b.Width),int(b.Height));self._rc=(HOST.pass_id,r)if a else None;return r
	def GetX(self):return self.rect()[0]
	def GetY(self):return self.rect()[1]
	def GetWidth(self):return self.rect()[2]
	def GetHeight(self):return self.rect()[3]
	def _put_bounds(self,x,y,w,h):import System;self.rect();f=ClientWin._bf[0];self._rc=None;f.SetValue(self.raw,System.Activator.CreateInstance(f.FieldType,System.Array[object]([int(x),int(y),int(w),int(h)])))
	def SetPos(self,x,y):
		x,y=int(x),int(y);a=None;self._rc=None
		try:self.raw.Location=ClientWin.point(x,y)
		except Exception as b:a=Tz.why(b)
		try:
			r=self.rect()
			if r[:2]!=(x,y):self._put_bounds(x,y,r[2],r[3]);r=self.rect()
			if r[:2]==(x,y):self.fail.pop("place",None);return True
		except Exception as b:a=a or Tz.why(b)
		self.fail["place"]="it couldn't be moved (%s)"%(a or "the client put it back");return False
	def _locked(self):
		try:return bool(self.raw.IsLocked)
		except Exception:return
	def _lock(self,on):
		a=self.raw;on=bool(on)
		with Kit.quiet:
			if bool(a.IsLocked)!=on:Tz.call(a,"SetLockStatus",(on,))
		with Kit.quiet:
			if on and a.CanMove:a.CanMove=False
			elif not on and not a.CanMove and self.own is not None and self.own[4]:a.CanMove=True
	def _min_size(self):
		if self.mins is None:self.mins=(int(Typing._get(self.raw,"_minW",None,0)or 0),int(Typing._get(self.raw,"_minH",None,0)or 0))
		return self.mins
	def fit(self,w,h,lock=True):
		a=self.raw
		if self.own is None:
			try:
				b=self._locked()
				if b and Kit.get_var(ClientWin.LOCK_VAR%self.kind,"")=="1":b=False
				self.own=self.rect()+(bool(a.CanMove),b)
			except Exception:self.own=None
			Kit.put_var(ClientWin.LOCK_VAR%self.kind,"1")
		self._lock(lock);d,e=self._min_size();w,h=max(int(w),d,1),max(int(h),e,1)
		try:r=self.rect()
		except Exception as c:self.fail["size"]="its size couldn't be read (%s)"%Tz.why(c);return
		if(r[2],r[3])==(w,h):self.tries=0;self.fail.pop("size",None);return
		self.tries+=1
		if self.tries>4:self.fail["size"]="it stays %d x %d, not %d x %d"%(r[2],r[3],w,h)
		with Kit.quiet:Tz.put(a,"_isFullscreen",False)
		p=ClientWin.point(w,h);self._rc=None
		try:Tz.call(a,"ResizeWindow",(p,))
		except Exception as c:self.fail["size"]="it couldn't be resized (%s)"%Tz.why(c)
	def free(self):
		a,self.own,self.tries=self.own,None,0;self._rc=None;Kit.put_var(ClientWin.LOCK_VAR%self.kind,"")
		if a is None or self.IsDisposed:return
		with Kit.quiet:
			self._lock(bool(a[5]))
			if not a[5]:self.raw.CanMove=a[4]
			Tz.call(self.raw,"ResizeWindow",(ClientWin.point(a[2],a[3]),));self.SetPos(a[0],a[1])
		self.fail={}
	def report(self):
		if self.fail and not self.warned:self.warned=True;Kit.say("%s couldn't be held in its zone: %s."%(ClientWin.TITLES.get(self.kind,self.kind),"; ".join(self.fail[a]for a in("place","size")if a in self.fail)),Kit.HUE_BAD)
class Tex(object):
	ok=None;parts={};names=set()
	@staticmethod
	def find():
		if Tex.ok is not None:return Tex.ok
		try:import clr;import System;b=Client.flags(True);c=Client.flags();p=Tex.parts;a=Client._type("ClassicUO.Assets.ExternalImageLoader");d=a.GetProperty("Instance",b).GetValue(None,None);p["table"]=a.GetField("_zipNamedTextures",c).GetValue(d);p["device"]=a.GetProperty("GraphicsDevice",c).GetValue(d,None);p["tex_t"]=Client._type("Microsoft.Xna.Framework.Graphics.Texture2D");p["format"]=System.Enum.Parse(Client._type("Microsoft.Xna.Framework.Graphics.SurfaceFormat"),"Color");p["set_data"]=[g for g in p["tex_t"].GetMethods()if g.Name=="SetData"and g.IsGenericMethodDefinition and len(g.GetParameters())==1][0].MakeGenericMethod(clr.GetClrType(System.UInt32));f=Client._type("ClassicUO.Client").GetProperty("Game",b).GetValue(None,None);e=Tz.get(Tz.get(f,"UO"),"Gumps");p["gumps"]=e;p["hued"]=e.GetType().GetMethod("GetHuedGumpPixels");Tex.ok=all(p.get(h)is not None for h in("table","device","tex_t","set_data","gumps","hued"))
		except Exception:Tex.ok=False
		return Tex.ok
	@staticmethod
	def gump_pixels(gid):
		import System;c=System.Array[System.Object]([System.UInt32(gid),System.UInt16(0),False,None]);a=Tex.parts["hued"].Invoke(Tex.parts["gumps"],c);b=c[3]
		if a is None or not len(a)or int(b.Width)<=0 or int(b.Height)<=0:return
		return list(a),int(b.Width),int(b.Height)
	@staticmethod
	def put(name,w,h,d):
		import System;p=Tex.parts;b=System.Activator.CreateInstance(p["tex_t"],System.Array[System.Object]([p["device"],int(w),int(h),False,p["format"]]));p["set_data"].Invoke(b,System.Array[System.Object]([System.Array[System.UInt32](d)]));a=p["table"];c=a[name]if a.ContainsKey(name)else None;a[name]=b;Tex.names.add(name)
		if c is not None:safe(c.Dispose)
	@staticmethod
	def drop(names=None):
		if not Tex.ok:return
		b=Tex.parts["table"]
		for a in list(Tex.names if names is None else names):
			Tex.names.discard(a)
			with Kit.quiet:
				if b.ContainsKey(a):c=b[a];b.Remove(a);c.Dispose()
	@staticmethod
	def control(g,name,x,y,w,h):t=G.LegionTextureControl(name,int(w),int(h));t.SetRect(int(x),int(y),int(w),int(h));safe(lambda:t.SetAcceptMouseInput(False));g.Add(t);return t
class Layout(object):
	def __init__(self):self.wins={};self.assign={};self.frames=None;self.frames_name=LAYOUT_DEFAULT;self.layout_name="";self.game_grows=True;self.fit_view=True;self.screen=None;self.dirty=True;self.occ=None;self.gump_key={};self.placed={};self.titles={};self.min_seen={};self.loaded=False;self.page_refresh=False;self.enabled=True;self.seamless=False;self.gv_off_done=False;self.seam_skip={};self.seam_wait={};self.hooks={};self.owner={};self.fitted={};self.base={};self.fresh=False;self.fresh_adds=set();self.client_seen={};self.journal_held=None;self.pair_tried=None;self.client_settle={};self.misfit={};self.fallback={};self.client_told=set();self.chat_seen=(0.,None);self.held={};self.arrange=False;self.arrange_last=0.;self.arrange_g=None;self.arrange_lit={};self.arrange_hot=None;self.client_target={};self.repair_at=0.;self.repair_told=set();self.freed=None;self.page_preview="";self.homes=None;self.back_told=False;self._arrange_sig=None;self.rev={};self.retry_at=0.;self.slot_was={};self.bags_swept=False;self.reclaim_undo=self._vp_fields=self.gv_applied=self.small_said=None;self._undo_read=self.gv_small_told=self.gv_checked=self.need_due=self.migrating=False
	def _client_getter(self,kind,key):
		def a():
			a=ClientWin.of(kind)
			if a is not self.client_seen.get(kind):self.client_seen[kind]=a;self.fitted.pop(key,None);self.placed.pop(key,None)
			if a is None and kind not in self.client_told and ClientWin.errors.get(kind)and self.zone_of(key)is not None:self.client_told.add(kind);Kit.say("%s can't be found for its zone: %s."%(ClientWin.TITLES.get(kind,kind),ClientWin.errors[kind]),Kit.HUE_BAD)
			return a
		return a
	def _client_fit(self,kind):
		def a(w,h,mode):
			a=ClientWin.of(kind)
			if a is None:return
			if w is None or h is None:a.free()
			else:a.fit(int(w),int(h),lock=not self.arrange);a.report()
		return a
	def _client_drops(self):
		if not self.arrange:self.client_settle.clear();return
		for a in ClientWin.DROPS:
			if a not in self.wins:self.client_settle.pop(a,None);continue
			b=ClientWin.of(a)
			if b is None:self.client_settle.pop(a,None);continue
			try:r=b.rect()
			except Exception:continue
			if self.zone_of(a)is not None:
				self.client_settle.pop(a,None);e=self.client_target.get(a)
				if e is not None and max(abs(r[0]-e[0]),abs(r[1]-e[1]))>SNAP_DIST and SNAP.pressed()is not True:self.client_target.pop(a,None);self.dropped(b)
				continue
			c=self.client_settle.get(a)
			if c is None or c[0]is not b:self.client_settle[a]=(b,r,r);continue
			d,f=c[1],c[2]
			if r!=f:self.client_settle[a]=(b,d,r);continue
			if r==d or SNAP.pressed()is True:continue
			self.client_settle[a]=(b,r,r)
			if(r[2],r[3])!=(d[2],d[3]):continue
			self.dropped(b)
	CHAT_ROOM=18
	def _chat_line(self):
		e=time.time();i,a=self.chat_seen
		if e-i<.5:return a
		a=None
		try:
			Typing._find();c=Typing._get(None,"SystemChat",Typing.uim)if Typing.uim is not None else None
			if c is not None and not bool(Typing._get(c,"IsDisposed",default=True)):
				b=ClientWin.bounds(c);j=int(Typing._get(c,"ParentX",default=0)or 0)+int(b.X);f=int(Typing._get(c,"ParentY",default=0)or 0)+int(b.Y);d=f+int(b.Height)-Layout.CHAT_ROOM;g=Typing._get(c,"TextBoxControl")
				if g is not None:
					h=int(ClientWin.bounds(g).Y)
					if 0<=h<int(b.Height):d=min(d,f+h)
				if int(b.Width)>0 and int(b.Height)>0:a=(j,d,int(b.Width))
		except Exception:a=None
		self.chat_seen=(e,a);return a
	def _clear_of_chat(self,x,y,w,h,H):
		a=self._chat_line()
		if a is None:e=Layout.CHAT_ROOM if H and y+h>=H-2 else 0;b=y+h-e
		else:
			c,d,f=a
			if x>=c+f or c>=x+w or not(y<d<y+h):return h
			b=d
		return max(min(h,60),b-y)
	def _hold_journal(self,zs,H=0):
		z=(next((c for c in zs.zones if c.kind=="r"and c.px is not None),None)if self.layout_name or self.assign else None);a=ClientWin.of("journal")if z is not None else None;b=self.journal_held
		if b is not None and b is not a:b.free();self.journal_held=None
		if a is None:return
		x,y,w,h=z.px;h=self._clear_of_chat(x,y,w,h,H);a.fit(w,h)
		try:
			if(a.GetX(),a.GetY())!=(x,y):a.SetPos(x,y)
		except Exception:pass
		a.report();self.journal_held=a
	def load(self):
		self.freed=None;self.homes=None;self.repair_told=set();self.back_told=False;self.loaded=True;self.bags_swept=False;self.seam_skip={};self.seam_wait={}
		if "worldmap"not in self.wins:self.add("worldmap",self._client_getter("worldmap","worldmap"),"TazUO's World Map",{"fit":self._client_fit("worldmap"),"exact":True,"client":True,"inset":ClientWin.INSET.get("worldmap",0)})
		self.frames_name=Kit.get_var(FRAMES_ACTIVE,LAYOUT_DEFAULT)or LAYOUT_DEFAULT
		if self.frames_name!=LAYOUT_DEFAULT and self.frames_name not in self.frame_names():self.frames_name=LAYOUT_DEFAULT
		self.layout_name=Kit.get_var(LAYOUT_ACTIVE,"");b=Kit.get_var(LAYOUT_OPTS,"game=1");self.game_grows="game=0"not in b;self.fit_view="fit=0"not in b;a=Kit.get_var(LAYOUT_VAR,"");self.seamless="seam=1"in b;c=dict.get(HOST.by_key,LAYOUT_OWNER);self.enabled=bool(c is not None and c.enabled and c.api is not None);self.assign=self.parse_windows(a)[1]
		if a and a!=self.windows_text()and any(e.strip()in LAYOUT_GONE for d in str(a).split(";")if "="in d and d.split("=",1)[0].strip()!="frames"for e in d.split("=",1)[1].split(",")):self.save_assign()
		self.frames=None;self.dirty=True
	def save_assign(self):Kit.put_var(LAYOUT_VAR,self.windows_text());self._note_homes()
	RECLAIM_VAR="VirtueAssistant_reclaim_undo";RECLAIM_FIXED="VirtueAssistant_reclaim_fixed"
	def _undo_load(self):
		if self.reclaim_undo is None and not self._undo_read:
			self._undo_read=True;p=str(Kit.get_var(self.RECLAIM_VAR,"")or "").split("|",2)
			if len(p)==3 and p[0]:self.reclaim_undo=(p[0],p[2],None,p[1]=="1")
		return self.reclaim_undo
	def _undo_set(self,undo):self.reclaim_undo=undo;self._undo_read=True;Kit.put_var(self.RECLAIM_VAR,""if undo is None else "%s|%d|%s"%(undo[0],1 if undo[3]else 0,undo[1]))
	@staticmethod
	def _reclaim_edges(z,d,W,H):
		r=list(z.px)
		for b in "LTRB":
			i=0 if b in "LR"else 1;j=1-i;c=[e.px for e in d if e is not z and e.px is not None and e.px[j]<r[j]+r[j+2]and r[j]<e.px[j]+e.px[j+2]]
			if b in "LT":
				a=max([0]+[f[i]+f[i+2]for f in c if f[i]+f[i+2]<=r[i]])
				if a<r[i]:r[i],r[i+2]=a,r[i+2]+(r[i]-a)
			else:
				a=min([(W,H)[i]]+[g[i]for g in c if g[i]>=r[i]+r[i+2]])
				if a>r[i]+r[i+2]:r[i+2]=a-r[i]
		return tuple(r)
	def reclaim_zones(self,zs,W,H):
		c=[f for f in zs.zones if f.px is not None and not f.hug and(f.kind!="k"and not f.overlap)];d=[g for g in zs.zones if g.px is not None and g.kind!="r"];a=[]
		for b,e in(("k",c),("w",d)):
			for z in zs.zones:
				if z.kind!=b or z.lock or z.px is None or(b=="w"and(z.hug or z.overlap)):continue
				r=self._reclaim_edges(z,e,W,H)
				if r!=tuple(z.px):z.set_px(r[0],r[1],r[2],r[3],W,H);a.append(z.id)
		return a
	@staticmethod
	def _game_px(zs):
		a=None
		for z in zs.zones:
			if z.kind=="k"and z.px is not None and z.px[2]>2 and z.px[3]>2 and(a is None or z.px[2]*z.px[3]>a[2]*a[3]):a=tuple(z.px)
		return a
	def reclaim_space(self):
		W,H=Kit.screen();a=self.frames_in_use(W,H)if W>0 and H>0 else None
		if a is None or not a.zones:Kit.say("no frame layout in use.",Kit.HUE_INFO);return
		b=(self._game_px(a)or(0,0,0,0))[2:];e=self.frames_name==LAYOUT_DEFAULT;g=(a.name,a.save_text(),b,e);d=self.reclaim_zones(a,W,H);c=(self._game_px(a)or(0,0,0,0))[2:]
		if not d or c[0]*c[1]<b[0]*b[1]:self.frames,self.dirty=None,True;Kit.say("Reclaim space: every zone is already tight.",Kit.HUE_INFO);return
		self._undo_set(g);f=a.name if not e else "Reclaimed";a.generated=False;self.save_frames(a,f,W,H);self.use_frames(f,False);self.refit_all();Kit.say("Reclaim space: %d zone%s tightened; game area %d x %d (was %d x %d). Undo puts it back."%(len(d),""if len(d)==1 else "s",c[0],c[1],b[0],b[1]),Kit.HUE_GOOD)
	def reclaim_back(self):
		a=self._undo_load()
		if a is None:return
		self._undo_set(None);W,H=Kit.screen()
		if a[3]:self.use_frames(LAYOUT_DEFAULT,False)
		else:
			b=ZoneSet.parse(a[0],a[1])
			if b is None:return
			b.reflow(W,H,HOST.grid_size());self.save_frames(b,a[0],W,H);self.use_frames(a[0],False)
		self.refit_all();Kit.say("Reclaim space undone.",Kit.HUE_INFO)
	def _repair_stretched(self,zs,W,H):
		if Kit.get_var(self.RECLAIM_FIXED,"")=="1":return
		Kit.put_var(self.RECLAIM_FIXED,"1");a=[c for c in zs.zones if c.hug and c.px is not None and c.rect[3]>=450]
		if not a:return
		self._undo_set((zs.name,zs.save_text(),None,False));b=int(_clampv(STRIP_SHARE*H,TOP_MIN,TOP_MAX))
		for z in a:z.set_px(z.px[0],z.px[1],z.px[2],b,W,H)
		self.save_frames(zs,zs.name,W,H);Kit.say("%d frame zone%s Reclaim space stretched in layout \"%s\" put right; Settings > Interface's Undo puts it back."%(len(a),""if len(a)==1 else "s",zs.name),Kit.HUE_GOOD)
	def refit_all(self):self.dirty=self.fresh=self.page_refresh=True;self.seam_skip={};self.seam_wait={}
	def save_opts(self):Kit.put_var(LAYOUT_OPTS,"game=%d;fit=%d;seam=%d;art=plain"%(self.game_grows,self.fit_view,self.seamless))
	def set_enabled(self,on):
		on=bool(on)
		if on==self.enabled:return
		if not on:self.set_arrange(False,tell=False)
		self.enabled,self.gv_off_done=on,False;self.refit_all();HOST.poke()
	def _off(self):
		Seam.undo_all()
		for b in list(self.fitted):self._unfit(b)
		for b in list(self.placed):
			g=self.gump_of(b);a=Kit.scroll_info(g)if g is not None else None
			if a is not None:
				with Kit.quiet:Kit.place(g,int(g.GetX()),int(g.GetY()),a["w"],a["h"],a["head"]);Kit.moved_by_code(g)
		self.placed={}
		if self.held:self._release(set())
		c,self.journal_held=self.journal_held,None
		if c is not None:c.free()
		if not self.gv_off_done:self.gv_off_done=True;self.game_view_restore()
	@staticmethod
	def parse_windows(text):
		a,b=LAYOUT_DEFAULT,{}
		for c in str(text or "").split(";"):
			if "="not in c:continue
			k,v=c.split("=",1);k=k.strip()
			if k=="frames":a=v.strip()or LAYOUT_DEFAULT;continue
			d=[e.strip()for e in v.split(",")if e.strip()and e.strip()not in LAYOUT_GONE]
			if k and d:b[k]=d
		return a,b
	def windows_text(self,frames=None):return ";".join(["frames=%s"%(frames or self.frames_name)]+["%s=%s"%(a,",".join(self.assign[a]))for a in sorted(self.assign)if self.assign[a]])
	@staticmethod
	def _names(a):return[b for b in Kit.get_var(a,"").split(",")if b.strip()]
	def frame_names(self):return self._names(FRAMES_LIST)
	def layout_names(self):return self._names(LAYOUT_LIST)
	@staticmethod
	def clean_name(name,fallback):name=re.sub(r"[^A-Za-z0-9 ()'_-]","",str(name or "")).strip()[:24];return name or fallback
	def add(self,key,getter,title=None,hooks=None,owner=None):
		key=str(key)
		if key in LAYOUT_GONE:return
		t=self.titles[key]=str(title or key);self.wins[key]=(getter,t);self.hooks[key]=hooks if hooks is not None else{}
		if owner is not None:self.owner[key]=owner
		self.fitted.pop(key,None);self.dirty=True
	def remove(self,key):
		key=str(key)
		for d in(self.wins,self.placed,self.hooks,self.owner,self.fitted,self.base,self.slot_was,self.min_seen):d.pop(key,None)
		self.dirty=True
	def owner_of(self,key):
		o=self.owner.get(key)
		if o is not None:return o
		k=str(key)
		while k:
			s,a=HOST.resolve(k)
			if s is not None:return s.key,a
			if "."not in k:break
			k=k.rsplit(".",1)[0]
		return None,None
	def windows_of(self,a):return sorted([(b,self.title_of(b))for b in self.wins if self.owner_of(b)[0]==a],key=lambda a:a[1].lower())
	def all_windows(self):
		b=[]
		for a in list(self.wins)+sorted(set(d for e in self.assign.values()for d in e if d not in self.wins)):
			c=self.owner_of(a)[0];s=dict.get(HOST.by_key,c)if c else None;t=self.title_of(a)
			if s is not None and s.title!=t:t="%s: %s"%(s.title,t)
			b.append((a,t if a in self.wins else t+" (not open)"))
		b.sort(key=lambda a:a[1].lower());return b
	def zone_choices(self):
		W,H=Kit.screen();a=self.frames_in_use(W,H)if W>0 and H>0 else self.frames;b=[None]
		if a is not None:b.extend(c.id for c in a.zones if c.kind=="w")
		return b
	def assign_to(self,key,a,tell=True):
		key=str(key);b=self.zone_of(key)
		if b==a:return
		if tell and a and((key!="worldmap"and a==self._map_zone())or(key=="worldmap"and self.assign.get(a))):Kit.say("TazUO's World Map keeps its zone to itself; pick another zone for %s."%(self.title_of(key)if key!="worldmap"else "it"),Kit.HUE_BAD);self.page_refresh=True;return
		if b is not None:
			self.assign[b]=[d for d in self.assign[b]if d!=key]
			if not self.assign[b]:del self.assign[b]
		if a:self.assign.setdefault(a,[]).append(key);self.unfree(key)
		elif tell:self.free_by_you([key])
		self.save_assign();W,H=Kit.screen();c=b is not None and not self.assign.get(b)
		if key=="bag"and c and W>0 and H>0 and self.drop_empty_bags(self.frames_in_use(W,H),W,H,(b,)):self.frames,self.dirty=None,True
		if not a:self.free_scrolled()
		self.placed.pop(key,None);self.dirty=True;self.page_refresh=True
		if tell:API.SysMsg(('%s: %s is in zone "%s".'%(APP_NAME,self.title_of(key),a))if a else("%s: %s is free (it stays where you put it)."%(APP_NAME,self.title_of(key))),Kit.HUE_GOOD)
		HOST.poke()
	def zone_of(self,key):
		a=self.rev.get(key)
		if a is not None and key in self.assign.get(a,()):return a
		self.rev=dict((d,b)for b,c in self.assign.items()for d in c);return self.rev.get(key)
	def need(self,key,w,h):
		a=self.zone_of(str(key));b=self.frames
		if a is None or b is None:return
		c=(w,h)if(w or h)else None
		if b.needs.get(a)!=c:
			if c is None:b.needs.pop(a,None)
			else:b.needs[a]=c
			self.need_due=True
	def zone_base(self,key):
		b=self.zone_of(str(key));a=self.frames;z=a.by_id(b)if(b is not None and a is not None)else None
		if z is None:return
		W,H=a.screen
		if W<=0 or H<=0:W,H=Kit.screen()
		return(max(1,int(W*z.rect[2]/1000.)),max(1,int(H*z.rect[3]/1000.)))
	def holds(self,key):
		if not self.enabled:return False
		a=self.zone_of(str(key))
		if a is None:return False
		b=self.frames;return b is None or b.by_id(a)is not None
	def locked(self,key):return not self.arrange and self.holds(key)
	def _hold(self,g,key):
		if isinstance(g,ClientWin):return
		if g not in self.held:
			self.held[g]=(key,bool(g.CanMove))
			for f,l in list(SNAP.links.items()):
				if f is g or l is g:SNAP.links.pop(f,None)
		if bool(g.CanMove)!=bool(self.arrange):g.CanMove=bool(self.arrange)
	def _release(self,keep):
		for g in[d for d in self.held if d not in keep]:
			b,a=self.held.pop(g)
			if g in SNAP.drag or not Kit.is_open(g):continue
			if not a and not self.holds(b):
				c=(self.hooks.get(b)or{}).get("redraw")
				if callable(c):safe(c);continue
				a=True
			if bool(g.CanMove)!=a:g.CanMove=a
	def set_arrange(self,on,tell=True):
		on=bool(on)and self.enabled
		if on==self.arrange:return
		self.arrange=on;self.arrange_last=time.time();self.arrange_hot=None
		if not on:a,self.arrange_g=self.arrange_g,None;self.arrange_lit={};Kit.dispose(a)
		self.dirty=True;self.page_refresh=True
		if tell:API.SysMsg(("%s: Arrange mode on; drag windows on to zones, then click Done."if on else "%s: windows locked in their zones.")%APP_NAME,Kit.HUE_GOOD)
		HOST.poke()
	def _arrange_tick(self,zs,W,H):
		if not self.arrange:return
		b=time.time()
		if SNAP.drag:self.arrange_last=b
		elif b-self.arrange_last>60.:self.set_arrange(False);return
		c=(W,H,tuple((p.id,p.kind,tuple(p.px))for p in zs.zones if p.px is not None))
		if self.arrange_g is not None and Kit.is_open(self.arrange_g)and self._arrange_sig==c:return
		self._arrange_sig=c;j,self.arrange_g=self.arrange_g,None;self.arrange_lit={};Kit.dispose(j);g=G.CreateGump(False,False)
		for z in zs.zones:
			if z.px is None or z.kind!="w":continue
			x,y,w,h=z.px;d=ZONE_COLORS.get(z.kind,"#3A78C8");e=Kit.add_box(g,x,y,w,h,.3,d);e.IsVisible=False;self.arrange_lit[z.id]=e
			for k,l,m,n in((x,y,w,2),(x,y+h-2,w,2),(x,y,2,h),(x+w-2,y,2,h)):Kit.add_box(g,k,l,m,n,.9,d)
			f=Kit.fit(z.id,max(20,w-28));o=Kit.text_w(f)+12;Kit.add_box(g,x+6,y+h-6-22,o,22,.85,"#000000");Kit.add_label(g,f,x+12,y+h-6-20,Kit.HUE_TITLE)
		i="Drag windows onto zones; Esc or Done to finish";a=Kit.text_w(i)+24;Kit.add_box(g,(W-a)//2,6,a,26,.85,"#000000");Kit.add_label(g,i,(W-a)//2+12,10,Kit.HUE_TITLE);Grid.show_overlay(g,0,0,W,H);self.arrange_g=g;self.arrange_hot=None
	def arrange_hover(self,g,r=None):
		if not self.arrange or not self.arrange_lit or self.frames is None:return
		if r is None:r=Snap.rect(g)
		z=self._drop_zone(r)if r is not None else None;a=z.id if z is not None else None
		if a==self.arrange_hot:return
		for k in(self.arrange_hot,a):
			b=self.arrange_lit.get(k)if k is not None else None
			if b is not None:b.IsVisible=k==a
		self.arrange_hot=a
	def _min_of(self,key,g=None):
		b=self.hooks.get(key)or{};a=b.get("min")
		if callable(a):a=safe(a)
		if a:
			with Kit.quiet:return int(a[0]),int(a[1])
		g=g if g is not None else self.gump_of(key)
		if isinstance(g,ClientWin):
			m=g._min_size()
			if m[0]>0 or m[1]>0:return m
		return
	def _too_small(self,key,z,g=None):
		a=self._min_of(key,g)
		if a is None or z is None or z.px is None:return False
		if z.px[2]>=a[0]and z.px[3]>=a[1]:return False
		Kit.say("%s needs a zone at least %d x %d."%(self.title_of(key),a[0],a[1]),Kit.HUE_BAD);return True
	def title_of(self,key):
		t=self.titles.get(key)
		if t is not None:return t
		a,b=self.owner_of(key);s=dict.get(HOST.by_key,a)if a else None
		if s is None:s=HOST.page_slot(key);return s.title if s is not None else key
		p=s.part(b)if b else None;return p[1]if p else s.title
	def drop_empty_bags(self,zs,W,H,b):
		a=[c for c in zs.zones if c.id in b and c.id.endswith(" bags")and c.kind=="w"and not self.assign.get(c.id)]
		if not a or zs.generated or zs.name==LAYOUT_DEFAULT:return False
		zs.zones=[d for d in zs.zones if d not in a]
		for z in a:zs.needs.pop(z.id,None)
		self.save_frames(zs,zs.name,W,H);Kit.say('empty zone%s %s removed; frame layout "%s" saved.'%(""if len(a)==1 else "s",", ".join('"%s"'%e.id for e in a),zs.name),Kit.HUE_INFO);return True
	PAIR_MIN_H=120
	def _flush_below(self,top,z):
		if top is None or z is None or top is z or top.px is None or z.px is None:return False
		a,e,b,f=top.px;c,g,d,i=z.px
		if abs(g-(e+f))>SNAP_DIST:return False
		h=min(a+b,c+d)-max(a,c);return h*2>min(b,d)
	def _free_under(self,zs,top,H):
		b,c,g,d=top.px;a=H
		for o in zs.zones:
			if o is top or o.px is None:continue
			e,f,h,i=o.px
			if f+i>c+d and e<b+g and b<e+h:a=min(a,max(f,c+d))
		return a
	def pair_below(self,k,c):
		if not self.loaded or not self.enabled:return
		W,H=Kit.screen()
		if W<=0 or H<=0:return
		b=self.frames_in_use(W,H);k,c=str(k),str(c);t,o=self.zone_of(k),self.zone_of(c);a=b.by_id(t)if t else None;l=b.by_id(o)if o else None
		if a is None or a.kind!="w"or a.px is None:
			if o is not None:self.assign_to(c,None,tell=False)
			return
		if l is not None and self._flush_below(a,l):return a.px,l.px
		D=l is not None;d=None
		for z in b.zones:
			if z.kind=="w"and self._flush_below(a,z):
				f,i,j,e=a.px;E=min(f+j,z.px[0]+z.px[2])-max(f,z.px[0]);u=(z.id=="%s bags"%a.id,E)
				if d is None or u>d[0]:d=(u,z)
		if d is not None:
			self.assign_to(c,d[1].id,tell=False)
			if D:Kit.say('%s rides in the %s window, so it takes the zone under it ("%s").'%(self.title_of(c),self.title_of(k),d[1].id),Kit.HUE_INFO)
			return a.px,d[1].px
		v=(b.name,a.id,tuple(a.px))
		if self.pair_tried==v:return a.px,None
		self.pair_tried=v;g=b.name
		if b.generated or g==LAYOUT_DEFAULT:
			b=ZoneSet.default(W,H,(),False);b.name,b.generated=LAYOUT_MINE,False;g=LAYOUT_MINE;a=b.by_id(a.id)
			if a is None or a.px is None:return
		else:b=b.copy();a=b.by_id(a.id)
		m=b.by_id("%s bags"%a.id)
		if m is not None and m.kind=="w"and not[F for F in self.assign.get(m.id,[])if F!=c]:b.zones.remove(m)
		f,i,j,e=a.px;w=self._free_under(b,a,H)-(i+e);p=False
		if w>=max(ZONE_MIN_H,self.PAIR_MIN_H):x,y,A,B=f,i+e,j,w
		elif e>=2*ZONE_MIN_H:p=True;q=max(ZONE_MIN_H,min(e-ZONE_MIN_H,int(round(e*.46))));x,y,A,B=f,i+q,j,e-q
		else:return a.px,None
		h="%s bags"%a.id
		if b.by_id(h)is not None:h=b.new_id()
		n=Zone(h,"w",(0,0,1,1),"",(a.min[0],self.PAIR_MIN_H),"d",a.prio,a.fit)
		if p:a.set_px(f,i,j,q,W,H)
		n.set_px(x,y,A,B,W,H);n.note_pins(W,H);a.note_pins(W,H);b.zones.append(n);self.save_frames(b,g,W,H)
		if self.frames_name!=g:self.use_frames(g,tell=False)
		else:self.frames,self.dirty=None,True
		self.assign_to(c,h,tell=False);Kit.say('zone "%s" made under "%s" for the bags%s; frame layout "%s" saved.'%(h,a.id," (split in two)"if p else "",g),Kit.HUE_GOOD);C=self.frames_in_use(W,H);r,s=C.by_id(a.id),C.by_id(h)
		if r is None or s is None or r.px is None or s.px is None:return a.px,n.px
		return r.px,s.px
	def gump_of(self,key):
		w=self.wins.get(key)
		if w is None:return
		try:g=w[0]()
		except Exception:return
		return g if Kit.is_open(g)else None
	def occupied(self):return set(a for a,b in self.assign.items()if any(self.gump_of(c)is not None for c in b))
	def frames_in_use(self,W,H):
		if self.frames is not None and not self.dirty and self.screen==(W,H):return self.frames
		a=self.load_frames(self.frames_name,W,H)if self.frames_name!=LAYOUT_DEFAULT else None
		if a is not None:
			self._repair_stretched(a,W,H)
			if not self.bags_swept:self.bags_swept=True;self.drop_empty_bags(a,W,H,a.ids())
		elif self.frames_name!=LAYOUT_DEFAULT:self.frames_name=LAYOUT_DEFAULT;Kit.put_var(FRAMES_ACTIVE,LAYOUT_DEFAULT)
		if a is None:a=ZoneSet.default(W,H,self.occupied(),self.game_grows)
		self._overlap_shape(a);self.frames,self.screen,self.dirty=a,(W,H),False;return a
	@staticmethod
	def _overlap_shape(zs):
		for k in zs.zones:
			if k.kind=="k"and k.overlap:k.arch=False
	GV_VAR="Layout_gameview_own";GV_LOCK_VAR="Layout_gameview_lock";GV_MIN=(640,480)
	def _viewport(self):t=Tz.T("ClassicUO.Game.UI.Gumps.WorldViewportGump");return t,Tz.get(None,"Instance",t)
	def _vp_border(self):return 0 if self._vp_full()else 5
	def _vp_set(self,x,y,w,h):t,a=self._viewport();b=self._vp_border();Tz.call(a,"ResizeGameWindow",(ClientWin.point(w,h),),t);Tz.call(a,"SetGameWindowPosition",(ClientWin.point(x-b,y-b),),t)
	def _vp_get(self):r=ClientWin.bounds(self._viewport()[1]);b=self._vp_border();return int(r.X)+b,int(r.Y)+b,int(r.Width)-2*b,int(r.Height)-2*b
	@staticmethod
	def _profile():Typing._find();return Typing._get(None,"CurrentProfile",Typing.prof)if Typing.prof is not None else None
	def _vp_full(self):a=self._profile();return bool(Typing._get(a,"GameWindowFullSize",default=False))if a is not None else False
	def _vp_chrome(self,on):
		t,c=self._viewport();a=self._vp_fields
		if a is None:a=self._vp_fields=[t.GetField(d,Client.flags(public=False))for d in("_borderControl","_button")]
		for f in a:
			b=f.GetValue(c)if f is not None else None
			if b is not None and bool(b.IsVisible)!=bool(on):b.IsVisible=bool(on)
	def _vp_lock(self,locked):
		a=self._profile()
		if a is not None:Tz.put(a,"GameWindowLock",bool(locked))
		t,b=self._viewport();b.CanMove=not locked
	def _game_view(self,zs):
		a=self._game_px(zs)if self.fit_view and self.assign and not self._vp_full()else None
		if a is not None and(a[2]<self.GV_MIN[0]or a[3]<self.GV_MIN[1]):
			if not self.gv_small_told:self.gv_small_told=True;Kit.say("the game view would be %d x %d, under the client's smallest (%d x %d); left as you set it."%(a[2],a[3],self.GV_MIN[0],self.GV_MIN[1]),Kit.HUE_INFO)
			a=None
		if not self.gv_checked:
			self.gv_checked=True
			if a is None and Kit.get_var(self.GV_VAR,""):self.game_view_restore();return
		if a==self.gv_applied:
			if a is not None:self._vp_chrome(False)
			return
		if a is None:self.game_view_restore();return
		if not Kit.get_var(self.GV_VAR,""):Kit.put_var(self.GV_VAR,"%d,%d,%d,%d"%self._vp_get());b=self._profile();c=bool(Typing._get(b,"GameWindowLock",default=False))if b is not None else False;Kit.put_var(self.GV_LOCK_VAR,"1"if c else "0")
		self._vp_set(*a);self._vp_chrome(False);self._vp_lock(True);self.gv_applied=a
	def game_view_restore(self):
		self.gv_applied=None;a=Kit.get_var(self.GV_VAR,"")
		if not a:return
		try:
			x,y,w,h=[int(c)for c in a.split(",")];self._vp_set(x,y,w,h)
			if not self._vp_full():self._vp_chrome(True)
			b=Kit.get_var(self.GV_LOCK_VAR,"")
			if b:self._vp_lock(b=="1")
		except Exception:return
		Kit.put_var(self.GV_VAR,"");Kit.put_var(self.GV_LOCK_VAR,"")
	def load_frames(self,name,W,H):
		c=ratio_class(W,H);b=FRAMES_NAMED%name;a=ZoneSet.parse(name,Kit.get_var(b+"@"+c,""));d=False
		if a is None:a=ZoneSet.parse(name,Kit.get_var(b,""));d=True
		if a is None:return
		for e in a.skipped:HOST._tell('%s: zone "%s" in frame layout "%s" couldn\'t be read; skipped.'%(APP_NAME,e,name))
		a.reflow(W,H,HOST.grid_size())
		if d and a.zones:Kit.put_var(b+"@"+c,a.save_text())
		return a
	def save_frames(self,zs,name,W,H):
		zs.name=name;zs.screen=(W,H);zs.grid=HOST.grid_size()
		for z in zs.zones:z.note_pins(W,H)
		b=zs.save_text();Kit.put_var(FRAMES_NAMED%name,b);c=ratio_class(W,H)
		for k in("narrow","wide","ultrawide"):Kit.put_var((FRAMES_NAMED%name)+"@"+k,b if k==c else "")
		a=self.frame_names()
		if name not in a:a.append(name);Kit.put_var(FRAMES_LIST,",".join(a))
		self.page_refresh=True
	def use_frames(self,name,tell=True):
		if name!=LAYOUT_DEFAULT and name not in self.frame_names():name=LAYOUT_DEFAULT
		self.frames_name=name;Kit.put_var(FRAMES_ACTIVE,name);self.frames,self.dirty=None,True;W,H=Kit.screen();b=self.frames_in_use(W,H)if W>0 else None
		if tell:
			a=0
			if b is not None:c=set(b.ids());a=sum(len(e)for d,e in self.assign.items()if d not in c)
			Kit.say('frame layout "%s" in use%s.'%(name,("; %s had no zone and are free"%Kit.count(a,"window"))if a else ""),Kit.HUE_GOOD)
		self.page_refresh=True
	def remove_frames(self,name):
		if name==LAYOUT_DEFAULT:return False
		a=[c for c in self.frame_names()if c!=name];Kit.put_var(FRAMES_LIST,",".join(a))
		for b in("","@narrow","@wide","@ultrawide"):Kit.put_var((FRAMES_NAMED%name)+b,"")
		if self.frames_name==name:self.use_frames(LAYOUT_DEFAULT,tell=False)
		Kit.say('frame layout "%s" deleted.'%name,Kit.HUE_GOOD);self.page_refresh=True;return True
	def window_layout_text(self,name):
		if name==LAYOUT_DEFAULT:return "frames=%s;%s"%(LAYOUT_DEFAULT,WINDOWS_DEFAULT)
		if name==LAYOUT_MIRRORED:return "frames=%s;%s"%(LAYOUT_DEFAULT,WINDOWS_MIRRORED)
		return Kit.get_var(LAYOUT_NAMED%name,"")
	def use_windows(self,name,tell=True):
		if(name and name not in(LAYOUT_DEFAULT,LAYOUT_MIRRORED)and name not in self.layout_names()):name=""
		a,b=(self.parse_windows(self.window_layout_text(name))if name else(self.frames_name,{}))
		if name:self.unfree(None)
		else:self.free_by_you(list(self.wins)+[d for c in self.assign.values()for d in c])
		self.layout_name=name;Kit.put_var(LAYOUT_ACTIVE,name);self.assign=b;self.save_assign();self.free_scrolled();self.placed={}
		if name and name not in(LAYOUT_DEFAULT,LAYOUT_MIRRORED)and a!=self.frames_name:self.use_frames(a,tell=False)
		else:self.dirty=True
		if tell:API.SysMsg(('%s: window layout "%s" in use.'%(APP_NAME,name))if name else("%s: every window is free; drop one on a zone to slot it."%APP_NAME),Kit.HUE_GOOD)
		self.page_refresh=True
	def save_windows(self,name=None):
		name=name or self.layout_name or LAYOUT_MINE
		if name in(LAYOUT_DEFAULT,LAYOUT_MIRRORED):name=name+" (mine)"
		name=self.clean_name(name,LAYOUT_MINE);Kit.put_var(LAYOUT_NAMED%name,self.windows_text());a=self.layout_names()
		if name not in a:a.append(name);Kit.put_var(LAYOUT_LIST,",".join(a))
		self.layout_name=name;Kit.put_var(LAYOUT_ACTIVE,name);Kit.say('window layout "%s" saved.'%name,Kit.HUE_GOOD);self.page_refresh=True
	def free_scrolled(self):
		for a in[d for d in self.fitted if not self.holds(d)]:self._unfit(a)
		for a,c in list(self.placed.items()):
			if not self.holds(a):
				g=self.gump_of(a);b=Kit.scroll_info(g)if g is not None else None
				if b is not None:
					with Kit.quiet:Kit.place(g,int(g.GetX()),int(g.GetY()),b["w"],b["h"],b["head"]);Kit.moved_by_code(g)
				self.placed.pop(a,None)
	def keep(self,W,H,i=None):
		if not self.loaded or W<=0 or H<=0:return
		if not self.enabled:self.fresh_adds.clear();self._off();return
		p=self.occupied()
		if p!=self.occ:
			self.occ=p
			if self.frames_name==LAYOUT_DEFAULT:self.dirty=True
		e=self.frames_in_use(W,H);Kit.flush();self.fresh=False;self.fresh_adds.clear();Fill.prune()
		for b in[L for L in self.fitted if not self.holds(L)]:self._unfit(b)
		q=time.time();f=[(self._hold_journal,(e,H)),(self._client_drops,()),(self._arrange_tick,(e,W,H))]
		if q>=self.repair_at and not SNAP.drag:self.repair_at=q+2.;f.append((self._repair,(e,)))
		for j,C in f:
			try:j(*C)
			except Exception:pass
		D=SNAP.drag;k=[];l=set();f=[]
		if i is None:self.gump_key={}
		for z in(e.zones if self.assign else()):
			n=self.assign.get(z.id)
			if not n or z.kind!="w"or z.px is None:continue
			if i is not None and not any(self.gump_of(M)in i for M in n):continue
			m=[]
			for b in n:
				g=self.gump_of(b)
				if g is None:continue
				self.gump_key[g]=b
				if g in l or g in SNAP.attached or not Snap.visible(g):continue
				s=(self.hooks.get(b)or{}).get("riding")
				if s is not None:
					try:
						if s():continue
					except Exception:pass
				l.add(g);self._hold(g,b);r=Snap.rect(g)
				if r is None:
					if isinstance(g,ClientWin):
						try:g.rect();t="it has no size"
						except Exception as E:t=Tz.why(E)
						g.fail["size"]="its place and size couldn't be read (%s)"%t;g.report()
					continue
				u=self.hooks.get(b)or{};v=[N for N in SNAP.followers(g)if Snap.visible(N)];c=r
				for F in v:
					d=Snap.rect(F)
					if d is not None:w,x=min(c[0],d[0]),min(c[1],d[1]);G=max(c[0]+c[2],d[0]+d[2]);I=max(c[1]+c[3],d[1]+d[3]);c=(w,x,G-w,I-x)
				o=False;y=u.get("state")
				if y is not None:
					try:o=y()=="minimized"
					except Exception:pass
				m.append((b,g,r,c,v,u,o,self._base(b,g,c,o)))
			if m:f.extend((O,P,z)for O,P in zip(m,self._slots(z,m)))
		J,K=(Seam.pad(),)*4,(Kit.MARGIN,)*4;A=set()
		for a,h,z in f:
			if a[1]in D:continue
			if self._small(a[0],z,a[1]):
				A.add(a[1]);self.placed[a[0]]=h
				if a[0]in self.fitted:self._unfit(a[0])
				if self._move_all(a[1],a[4],a[2],h[0],h[1]):k.append(a[1])
				continue
			try:
				if self._fit_slot(a,h,z,(K if z.solo else J)if self.seamless else None):k.append(a[1])
			except Exception:self.placed[a[0]]=h
		if i is None:
			self._release(l)
			for g in[Q for Q in Seam.recs if Q not in l]:Seam.undo(g)
		B=set()
		if self.seamless and self.enabled:
			for a,h,z in[R for R in f if R[0][1]not in A]:
				for g in[a[1]]+list(a[4]):
					try:
						if not isinstance(g,ClientWin)and Seam.strip(g,g is a[1]and a[5].get("untitled")):B.add(g)
					except Exception:pass
		for g in([S for S in Seam.bare if S not in B]if i is None else()):Seam.unstrip(g)
		try:self._game_view(e)
		except Exception:pass
		if self.assign and self.need_due:self.need_due=False;e.reflow(W,H,HOST.grid_size())
		if k:
			Kit.flush()
			for g in k:
				j=SNAP.moved_cb.get(g)
				if j is not None:
					try:j()
					except Exception:pass
	def _base(self,key,g,a,mini):
		if mini:return a[2],a[3]
		b=self.base.get(key)
		if b is None:c=Fill.recs.get(g);b=c["nat"]if c is not None else(a[2],a[3]);self.base[key]=b
		return b
	def _slots(self,z,items):
		f,g,h,i=z.px;c=z.stack in("d","u");j=i if c else h;q=len(items);x=all(y[6]for y in items);b=[];a=[]
		for k in items:
			r=k[7][1]if c else k[7][0]
			if k[6]and not x:b.append(max(1,min(int(r),j)));a.append(0)
			else:b.append(None);a.append(max(1,int(r)))
		l=j-sum(A for A in b if A is not None);m=sum(a)
		if l<q or m<=0:b=[None]*q;a=[max(1,int(B[7][1]if c else B[7][0]))for B in items];l,m=j,sum(a)
		n=[];o,p=l,m
		for s,t in zip(b,a):
			if s is not None:n.append(s)
			else:u=int(round(o*float(t)/p))if p>0 else o;n.append(max(1,u));o-=u;p-=t
		v=[];d=(g if z.stack=="d"else g+i if z.stack=="u"else f if z.stack=="r"else f+h);w=z.stack in("u","l")
		for e in n:
			if w:d-=e
			v.append((f,d,h,e)if c else(d,g,e,i))
			if not w:d+=e
		return v
	def retry_due(self,now):
		if not self.seam_wait or now<self.retry_at:return False
		self.retry_at=now+SEAM_RETRY
		for a,b in list(self.seam_wait.items()):
			g=self.gump_of(a)
			if g is None or not Snap.visible(g)or not self.holds(a)or now-b[1]>2*SEAM_WAIT:self.seam_wait.pop(a,None)
			else:self.fresh_adds.add(g)
		return bool(self.fresh_adds)
	def fit_now(self,key,g):
		c=self.slot_was.get(key)
		if(c is None or not(self.seamless and self.enabled)or self.dirty or self.fresh or g in SNAP.drag or g in SNAP.attached or not Client.on_client_thread()):return
		Kit.flush();a=self.hooks.get(key)or{};r=Snap.rect(g)
		if r is None or a.get("riding")is not None or SNAP.followers(g):return
		try:b=a.get("state")is not None and a["state"]()=="minimized"
		except Exception:b=False
		d,z,e=c;self.gump_key[g]=key
		try:
			self._fit_slot((key,g,r,r,[],a,b,self._base(key,g,r,b)),d,z,e)
			if not isinstance(g,ClientWin):Seam.strip(g,a.get("untitled"))
		except Exception:pass
	def _fit_slot(self,it,slot,z=None,pads=None):
		a,g,r,l,f,h,k,m=it;c=int(h.get("inset")or 0)
		if g in Seam.recs and not Client.on_client_thread():return False
		self.slot_was[a]=(slot,z,pads);slot=(slot[0]-c,slot[1]-c,slot[2]+2*c,slot[3]+2*c);self.placed[a]=slot
		if pads is not None:pads=Seam.clip(slot,pads)
		b=Seam.grow(slot,pads)if pads is not None else None
		if(b is not None and self.seam_skip.get(a)!=slot and Seam.can(g,h,k)and b[3]<=Kit.screen()[1]):
			self.placed[a]=b
			if Seam.holds(g,slot,pads,b,r):return False
			Seam.undo(g);Seam.unstrip(g);self._fit_at(it,b,z,c);d=Snap.rect(g);i=Fill.recs.get(g);S=self.MISFIT_SLACK
			if d is not None and(i is None or i.get("k",1.)>=.995):
				if d[:2]!=b[:2]:self._move_all(g,f,d,b[0],b[1])
				if f or(abs(d[2]-b[2])<=S and abs(d[3]-b[3])<=S):self.seam_wait.pop(a,None);return Seam.trim(g,slot,pads)
				e=self.seam_wait.get(a);j=time.time()
				if e is None or e[0]!=slot:e=self.seam_wait[a]=(slot,j)
				if j-e[1]<SEAM_WAIT:return False
			self.seam_skip[a]=slot;self.placed[a]=slot
		self.seam_wait.pop(a,None)
		if g in Seam.recs:Seam.undo(g)
		return self._fit_at(it,slot,z,c)
	def _fit_at(self,it,slot,z,F):
		i,g,r,c,j,d,B,I=it;e,f,h,b=slot;p=d.get("fit");m=self.fitted.get(i)
		if p is not None:
			k,l=h,b
			if j and not d.get("pieces_out"):k,l=h-(c[2]-r[2]),b-(c[3]-r[3])
			q=m.get("told")if m is not None else None
			if q is None or abs(q[0]-k)>4 or abs(q[1]-l)>4 or(q!=(k,l)and(k,l)==(h,b))or d.get("client"):
				self.fitted[i]=m={"kind":"fit","told":(k,l)}
				try:p(k,l,"w")
				except Exception:pass
		elif m is None:self.fitted[i]={"kind":"fill"}
		if d.get("exact"):
			n,o=e+(r[0]-c[0]),f+(r[1]-c[1])
			if d.get("pieces_out"):n,o=e,f
			if isinstance(g,ClientWin):n,o=self._client_overflow(i,g,z,n,o,h,b,F);self.client_target[i]=(n,o)
			if p is not None and d.get("verify"):
				self._verify(i,g,r,m,p,B);C=self.fallback.get(i)
				if C is not None and not B and not j:
					if C!=(h,b):self.fallback.pop(i,None)
					else:
						a=Fill.fit(g,e,f,h,b,d.get("fill")or "anchor")
						if a is not None:
							if a:Kit.moved_by_code(g)
							return bool(a)
			return self._move_all(g,j,r,n,o)
		if j:
			if d.get("pieces_out"):s,t,u,v=e,f,h,b
			else:s,t=e+(r[0]-c[0]),f+(r[1]-c[1]);u,v=h-(c[2]-r[2]),b-(c[3]-r[3])
			if u<40 or v<20:return self._move_all(g,j,r,e+(r[0]-c[0]),f+(r[1]-c[1]))
			a=Fill.fit(g,s,t,u,v,d.get("fill")or "anchor")
			if a is None:return self._move_all(g,j,r,s,t)
			G=Snap.rect(g)or(s,t,u,v)
			for x in j:
				w=Snap.rect(x)
				if w is None:continue
				D,E=Fill.beside(w,r,G)
				if(w[0],w[1])!=(D,E):Snap.move(x,D,E);Kit.moved_by_code(x);a=True
			if a:Kit.moved_by_code(g)
			return bool(a)
		a=Fill.fit(g,e,f,h,b,d.get("fill")or "anchor")
		if a is None:
			Fill.unfit(g);y=Kit.scroll_info(g);H,A=(y["w"],y["h"])if y is not None else(r[2],r[3])
			if(r[0],r[1])==(e,f)and r[3]==min(A,b):return False
			Kit._place_raw(g,e,f,H,A,None,b if A>b else None);a=True
		if a:Kit.moved_by_code(g)
		return bool(a)
	@staticmethod
	def _move_all(g,b,r,x,y):
		if(r[0],r[1])==(x,y):return False
		Snap.move(g,x,y);Kit.moved_by_code(g)
		for f in b:
			a=Snap.pos(f)
			if a is not None:Snap.move(f,a[0]+x-r[0],a[1]+y-r[1]);Kit.moved_by_code(f)
		return True
	def _client_overflow(self,key,g,z,d,e,sw,sh,f):
		try:h,i=g._min_size()
		except Exception:return d,e
		a,b=max(sw,h),max(sh,i)
		if a<=sw and b<=sh:return d,e
		j=self.frames;W,H=Kit.screen()
		if(z is not None and z.px is not None and(key,z.id,z.px)!=self.small_said):self.small_said=(key,z.id,z.px);Kit.say('%s needs zone "%s" to be at least %d x %d; it is %d x %d.'%(self.title_of(key),z.id,max(z.px[2],h-2*f),max(z.px[3],i-2*f),z.px[2],z.px[3]),Kit.HUE_BAD)
		k,l=a-sw,b-sh
		def p(x,y):
			c=0
			for o in(j.zones if j is not None else[]):
				if o is z or o.px is None or o.kind=="r":continue
				d=max(0,min(x+a,o.px[0]+o.px[2])-max(x,o.px[0]))*max(0,min(y+b,o.px[1]+o.px[3])-max(y,o.px[1]));c+=d*(100 if o.kind=="w"else 10)
			e=max(0,min(x+a,W)-max(x,0))*max(0,min(y+b,H)-max(y,0));return c+(a*b-e)
		c=None
		for m in sorted(set((0,k//2,k))):
			for n in sorted(set((0,l//2,l))):
				o=p(d-m,e-n)
				if c is None or o<c[0]:c=(o,d-m,e-n)
		return c[1],c[2]
	MISFIT_SLACK=2
	def _verify(self,key,g,r,rec,b,c=False):
		a=rec.get("told")if rec is not None else None
		if a is None or SNAP.drag:return
		if c or not(abs(r[2]-a[0])>self.MISFIT_SLACK or abs(r[3]-a[1])>self.MISFIT_SLACK):self.misfit.pop(key,None);return
		n=self.misfit.get(key,0)+1;self.misfit[key]=n
		if n==8 and key not in self.fallback:self.fallback[key]=(int(a[0]),int(a[1]))
		if n>=2 and n&(n-1)==0:
			try:b(a[0],a[1],"again")
			except Exception:pass
	def _unfit(self,key):
		a=self.fitted.pop(key,None)
		for d in(self.base,self.misfit,self.fallback,self.client_settle,self.slot_was):d.pop(key,None)
		if a is None:return
		c=self.hooks.get(key)or{}
		if a.get("kind")=="fit":
			b=c.get("fit")
			if b is not None and a.get("told")is not None:
				try:b(None,None,None)
				except Exception:pass
		g=self.gump_of(key)
		if g is not None and g in Seam.recs:Seam.undo(g)
		if g is not None:Fill.unfit(g)
	def _small(self,key,z,g):
		b=(z.id,tuple(z.px));a=self.min_seen.get(key)
		if a is None or a[0]!=b:a=self.min_seen[key]=(b,self._too_small(key,z,g))
		return a[1]
	def report_fit(self):
		W,H=Kit.screen();d=self.frames_in_use(W,H)if W>0 and H>0 else None;n=i=0;j=[]
		for z in(d.zones if d is not None else[]):
			b=self.assign.get(z.id,[]);q=[safe((self.hooks.get(t)or{}).get("riding")or(lambda:False),False)for t in b]
			if b and all(q)and z.px is not None:j.append(z.px)
		for z in(d.zones if d is not None else[]):
			b=self.assign.get(z.id,[]);f=[v for v in b if self.gump_of(v)is None]
			if z.kind=="w"and not b:Kit.say('zone "%s": empty.'%z.id,Kit.HUE_INFO)
			if f:s=", ".join(self.title_of(w)for w in f);Kit.say('zone "%s": %s.'%(z.id,("empty (%s not open)"if len(f)==len(b)else "%s not open")%s),Kit.HUE_BAD)
			for c in b:
				g=self.gump_of(c);k=self.placed.get(c)
				if g is None or k is None:continue
				r=Snap.rect(g)
				if r is None:continue
				n+=1;a=tuple(k);e=all(abs(x-y)<=self.MISFIT_SLACK for x,y in zip(r,a))
				for p in j:
					l,m=min(a[0],p[0]),min(a[1],p[1]);u=(l,m,max(a[0]+a[2],p[0]+p[2])-l,max(a[1]+a[3],p[1]+p[3])-m)
					if all(abs(A-B)<=self.MISFIT_SLACK for A,B in zip(r,u)):e=True
				if not e:i+=1
				Kit.say('%s in "%s": %d x %d at %d, %d%s.'%(self.title_of(c),z.id,r[2],r[3],r[0],r[1],"; fills it"if e else "; its zone is %d x %d at %d, %d"%(a[2],a[3],a[0],a[1])),Kit.HUE_GOOD if e else Kit.HUE_BAD);o,h=self.drawn_at(c,g)
				if o<.995 and h is not None:Kit.say('%s is drawn at %d%% in zone "%s"; %d x %d shows it at 100%%.'%(self.title_of(c),int(round(o*100)),z.id,h[0],h[1]),Kit.HUE_INFO)
		if self.seamless:Kit.say("One panel: on; %s without a title row, %s with its title hidden in place, %s left as is."%(Kit.count(len(Seam.recs),"window"),Kit.count(sum(1 for C in Seam.bare.values()if C["title"]),"window"),Kit.count(max(0,n-len(Seam.recs)-sum(1 for D in Seam.bare.values()if D["title"])),"window")),Kit.HUE_INFO)
		if not n:Kit.say("no window sits in a zone.",Kit.HUE_INFO)
		else:Kit.say("%d of %d windows fill their zone; screen %d x %d (UI scale %.2f)."%(n-i,n,W,H,Kit.render_scale()),Kit.HUE_INFO)
	def drawn_at(self,key,g):
		d=self.hooks.get(key)or{};b=d.get("drawn_at")
		if b is not None:
			c=safe(b,None)
			if c:return c
		a=Fill.recs.get(g)
		if a is None or a.get("k",1.)>=.995:return 1.,None
		e,f=a["nat"];return a["k"],(int(e),int(f))
	def _map_zone(self):return self.zone_of("worldmap")
	FREED_VAR="VirtueAssistant_layout_freed";HOMES_VAR="VirtueAssistant_layout_homes"
	def _freed(self):
		if self.freed is None:self.freed=set(a for a in Kit.get_var(self.FREED_VAR,"").split(",")if a.strip())
		return self.freed
	def free_by_you(self,keys):
		f=self._freed();n=len(f);f.update(str(a)for a in keys)
		if len(f)!=n:Kit.put_var(self.FREED_VAR,",".join(sorted(f)))
	def unfree(self,key=None):
		f=self._freed()
		if not f:return
		if key is None:f.clear()
		elif key in f:f.discard(key)
		else:return
		Kit.put_var(self.FREED_VAR,",".join(sorted(f)))
	def _homes(self):
		if self.homes is None:
			self.homes={};a=Kit.get_var(self.HOMES_VAR,"");self.migrating=not a
			for b in a.split(";"):
				if "="in b:
					k,v=b.split("=",1)
					if k.strip()and v.strip():self.homes[k.strip()]=v.strip()
		return self.homes
	def _note_homes(self):
		h=self._homes();a=False
		for b,c in self.assign.items():
			for k in c:
				if h.get(k)!=b:h[k]=b;a=True
		if a:
			if len(h)>64:
				for k in[d for d in h if self.zone_of(d)is None][:len(h)-64]:del h[k]
			Kit.put_var(self.HOMES_VAR,";".join("%s=%s"%e for e in sorted(h.items())))
	def _repair(self,zs):
		if not self.assign:return
		g=self._homes()
		if not g:self._note_homes()
		e=self._map_zone();h=[n for n in(self.assign.get(e,[])if e else[])if n!="worldmap"];j=self._freed();i=list(h);d=None
		for a in("ultima.friend","ultima.neutral","ultima.foe","ultima.combat","meters","worldmap"):
			if(a not in self.wins or a in j or a in h or self.holds(a)):continue
			if d is None:
				d=set()
				if self.layout_name:
					for k in self.parse_windows(self.window_layout_text(self.layout_name))[1].values():d.update(k)
			l=a.split(".")[0];m=any(p.split(".")[0]==l for o in self.assign.values()for p in o)
			if a in g or a in d or(m and a!="worldmap")or(self.migrating and a!="worldmap"):i.append(a)
		f=[]
		for a in i:
			if self.gump_of(a)is None:continue
			c=self.zone_of(a);b=self._home_for(a,zs,e)
			if b is None:
				if a not in self.repair_told and a!="worldmap":self.repair_told.add(a);Kit.say("%s has no zone to go back to; drop it on one in Arrange mode."%self.title_of(a),Kit.HUE_INFO)
				if c is None:continue
			if c is not None:
				self.assign[c]=[q for q in self.assign[c]if q!=a]
				if not self.assign[c]:del self.assign[c]
			if b is not None:self.assign.setdefault(b,[]).append(a)
			self._refit(a);f.append((a,b))
		if f:
			self.save_assign();self.dirty=self.fresh=True;self.page_refresh=True
			for a,b in f:
				if b is not None:Kit.say('%s put back in zone "%s".'%(self.title_of(a),b),Kit.HUE_GOOD)
			self.free_scrolled();HOST.poke()
	def _home_for(self,key,zs,n):
		a=[v for v in zs.zones if v.kind=="w"and v.px is not None and v.id!=n]
		if key=="worldmap":a=[A for A in zs.zones if A.kind=="w"and A.px is not None and not self.assign.get(A.id)]
		f=set(B.id for B in a);g=key.split(".")[0]
		def h(a):return all(v.split(".")[0]==g for v in self.assign.get(a,[])if v!=key)
		c=self._homes().get(key)
		if c in f and h(c):return c
		if key=="worldmap":return
		d=next((C for C,D in self.parse_windows(WINDOWS_DEFAULT)[1].items()if key in D),None)
		if d in f and h(d):return d
		b=[E for E in a if not self.assign.get(E.id)];e=[F for F in a if F.id in self.assign and any(H!=key and H.split(".")[0]==g for H in self.assign[F.id])]
		if e:
			for o in e:
				i,j,p,k=o.px
				for l in b:
					x,y,w,m=l.px;q=min(y+m,j+k)-max(y,j);s=abs(x-(i+p))<=SNAP_DIST or abs((x+w)-i)<=SNAP_DIST
					if s and q*2>min(m,k):return l.id
			return e[0].id
		if b:r=Snap.rect(self.gump_of(key))if self.gump_of(key)is not None else None;t,u=(r[0]+r[2]/2.,r[1]+r[3]/2.)if r else(0.,0.);b.sort(key=lambda z:(z.px[0]+z.px[2]/2.-t)**2+(z.px[1]+z.px[3]/2.-u)**2);return b[0].id
		return
	def _refit(self,key):
		self.placed.pop(key,None);self.min_seen.pop(key,None);a=self.fitted.get(key)
		if a is not None and a.get("kind")=="fit":a.pop("told",None)
	def _key_of(self,g):
		a=self.gump_key.get(g)
		if a is None:
			for k in self.wins:
				if self.gump_of(k)is g:return k
		return a
	def _drop_zone(self,r):
		e,f=r[0]+r[2]//2,r[1]+r[3]//2;b=None;a=None
		for z in self.frames.zones:
			if z.kind!="w"or z.px is None:continue
			x,y,w,h=z.px
			if b is None and x<=e<x+w and y<=f<y+h:b=z
			c=min(x+w,r[0]+r[2])-max(x,r[0]);d=min(y+h,r[1]+r[3])-max(y,r[1])
			if(c>0 and d>0 and c*d*2>w*h and(a is None or c*d>a[0])):a=(c*d,z)
		if a is not None:b=a[1]
		return b
	def takes(self,g):
		if not self.loaded or self.frames is None or not self.arrange:return False
		if self._key_of(g)is None or safe(Follow.alt_held,False):return False
		r=Snap.rect(g);return r is not None and self._drop_zone(r)is not None
	def _back(self):self.dirty=True;HOST.poke()
	def dropped(self,g,key=None,rect=None):
		if not self.loaded or self.frames is None:return
		if key is None:key=self._key_of(g)
		else:
			g=self.gump_of(key)
			if g is None:return
		if key is None:return
		if not self.arrange:
			if self.zone_of(key)is not None:self.fresh=self.dirty=True;HOST.poke()
			return
		self.arrange_last=time.time()
		if safe(Follow.alt_held,False):return
		r=rect if rect is not None else Snap.rect(g)
		if r is None:return
		i,j=r[0]+r[2]//2,r[1]+r[3]//2;b=self._drop_zone(r);self.fresh=True
		if self.arrange_hot is not None:
			l=self.arrange_lit.get(self.arrange_hot)
			if l is not None:l.IsVisible=False
			self.arrange_hot=None
		for m,s in list(SNAP.links.items()):
			if m is g or s is g:SNAP.links.pop(m,None)
		a=self.zone_of(key)
		if b is None:
			if a is None:return
			self._back()
			if not self.back_told:self.back_told=True;Kit.say("%s stays in its zone; drop it on another zone to move it (Settings > Interface frees windows)."%self.title_of(key),Kit.HUE_INFO)
			return
		if a==b.id and len(self.assign.get(a,[]))<=1:self._back();return
		t=self._map_zone();e=[x for x in self.assign.get(b.id,[])if x!=key];n=len(e)==1 and self.gump_of(e[0])is not None
		if(key!="worldmap"and b.id==t and b.id!=a and(a is None or not n))or(key=="worldmap"and e and(a is None or not n)):self._back();Kit.say("TazUO's World Map keeps its zone to itself; drop %s on another zone."%(self.title_of(key)if key!="worldmap"else "it"),Kit.HUE_BAD);return
		if a!=b.id and self._too_small(key,b,g):self._back();return
		c=None;u=dict((y,self.placed.get(y))for y in self.assign.get(b.id,[]))
		if a is not None:
			f=[z for z in self.assign.get(b.id,[])if z!=key]if a!=b.id else[]
			if len(f)==1 and self.gump_of(f[0])is not None:
				c=f[0]
				if self._too_small(c,self.frames.by_id(a)):self._back();return
			for k in list(self.assign.get(a,[]))+list(self.assign.get(b.id,[])):self._refit(k)
			v=self.assign[a].index(key)if key in self.assign[a]else 0;self.assign[a]=[A for A in self.assign[a]if A!=key]
			if c is not None:self.assign[a].insert(min(v,len(self.assign[a])),c);self.assign[b.id]=[B for B in self.assign[b.id]if B!=c];self.placed.pop(c,None)
			if not self.assign[a]:del self.assign[a]
		h=self.assign.setdefault(b.id,[]);o=len(h)
		for w,k in enumerate(h):
			p=u.get(k)or self.placed.get(k)
			if p is None:continue
			if b.stack in("d","u"):d=p[1]+p[3]//2;q=j<d if b.stack=="d"else j>d
			else:d=p[0]+p[2]//2;q=i<d if b.stack=="r"else i>d
			if q:o=w;break
		h.insert(o,key);self.unfree(key);self.save_assign();self.dirty=True;HOST.poke()
	def _size_of(self,key):
		a=self.base.get(key)
		if a is None:g=self.gump_of(key);r=Snap.rect(g)if g is not None and not isinstance(g,ClientWin)else None;a=(r[2],r[3])if r else None
		return a
	def slots_for(self,z,keys):
		if not keys or z is None or z.px is None:return[]
		return list(zip(keys,self._slots(z,[(a,None,None,None,None,None,False,self._size_of(a)or(100,100))for a in keys])))
	def preview_text(self,key,z,keys=None):
		if key is None or z is None or z.px is None:return ""
		t=self.title_of(key)
		if z.kind!="w":return "!%s can only go in a window zone."%t
		f=self._map_zone()
		if(key!="worldmap"and z.id==f and z.id!=self.zone_of(key))or(key=="worldmap"and[i for i in self.assign.get(z.id,[])if i!=key]):return "!TazUO's World Map keeps its zone to itself."
		a=self._min_of(key)
		if a and(z.px[2]<a[0]or z.px[3]<a[1]):return("!%s needs %d x %d at least; this zone is %d x %d."%(t,a[0],a[1],z.px[2],z.px[3]))
		keys=([j for j in(keys if keys is not None else self.assign.get(z.id,[]))if j!=key]+[key]);b=None
		for k,g in self.slots_for(z,keys):
			if k==key:b=g
		if b is None:b=z.px
		w,h=max(1,b[2]),max(1,b[3]);c=self._size_of(key);d=""
		if c and c[0]>0 and c[1]>0:
			e=min(1.,float(w)/c[0],float(h)/c[1])
			if e<.995:d=" (shown at %d%%)"%int(round(e*100))
		return "%s: %d x %d here%s."%(t,w,h,d)
	def status_text(self):
		W,H=Kit.screen();a=HOST.grid_size()
		if W<=0 or H<=0:return "Screen: not known yet"
		return "Screen: %d x %d, %s; grid %d px, %d x %d squares"%(W,H,ratio_class(W,H),a,(W+a-1)//a,(H+a-1)//a)
class Seam(object):
	recs={};bare={};titled_n={};edge=[None];catchers={};seen=[None,0.]
	@staticmethod
	def pad():
		if Seam.edge[0]is None:s=[Kit.pic_size(Kit.WINDOW_BG+a)for a in(1,3,5,7)];Seam.edge[0]=min(Kit.MARGIN,max([SEAM_PAD,s[0][1],s[1][0],s[2][0],s[3][1]])+1)
		return Seam.edge[0]
	@staticmethod
	def title_of(raw,w):
		M=Kit.MARGIN;a=[(b,Kit._raw_rect(b))for b in Kit._children(raw)]
		if not any(d is not None and abs(d[0]-M)<=2 and abs(d[1]-M)<=2 and abs(d[3]-30)<=1 and d[2]>=w-2*M-6 for e,d in a):return[]
		return[g for g,f in a if f is not None and M-4<=f[1]<M+34 and f[1]+f[3]<=M+36]
	@staticmethod
	def titled(g):
		if g in Seam.recs:return True
		a=Kit._raw_gump(g);r=Kit.rect(g)
		if a is None or r is None:return False
		n=int(a.Children.Count);b=Seam.titled_n.get(g)
		if b is not None and b[0]==n:return b[1]
		Kit._prune(Seam.titled_n,32);c=bool(Seam.title_of(a,r[2]));Seam.titled_n[g]=(n,c);return c
	@staticmethod
	def strip(g,untitled=False):
		b=Kit._frame_parts.get(g);d=Kit._raw_gump(g)
		if not b or d is None:return False
		a=Seam.bare.get(g);n=int(d.Children.Count)
		if a is not None and a["parts"]is b:
			if a["n"]!=n:
				f=Kit._children(d);i=set(f);M=Kit.MARGIN
				for p in b:Kit.set(p,"IsVisible",False)
				a["title"]=[l for l in a["title"]if l[0]in i]
				for e in[m for m in f if m not in a["kids"]]if a["band"]else():
					r=Kit._raw_rect(e)
					if r is None or not(M-4<=r[1]<M+34 and r[1]+r[3]<=M+36):continue
					v=bool(e.IsVisible);a["title"].append([e,None,None,v]);e.IsVisible=v and a["open"]
				a["kids"],a["n"]=i,len(f)
			Seam.watch(a,False);return True
		h=(a["open"],a["until"])if a is not None else(False,0.)
		if a is not None:Seam.unstrip(g)
		r=Kit.rect(g);j=r is not None and g not in Seam.recs and not untitled;c=Seam.title_of(d,r[2])if j else[];k=set(o for o in map(Kit.client_control,b)if o is not None);c=[[q,None,None,bool(q.IsVisible)]for q in c if q not in k]
		for p in b:Kit.set(p,"IsVisible",False)
		for t in c:t[0].IsVisible=False
		Kit._prune(Seam.bare,32);Seam.bare[g]={"parts":b,"n":n,"title":c,"open":h[0],"until":h[1],"band":bool(c),"kids":set(Kit._children(d))}
		for t in c:t[0].IsVisible=t[3]and h[0]
		return True
	@staticmethod
	def unstrip(g):
		a=Seam.bare.pop(g,None)
		if a is None or not Kit.is_open(g):return
		b=Kit._frame_want.get(g,True)
		for p in a["parts"]:Kit.set(p,"IsVisible",b)
		for t in a["title"]:
			with Kit.quiet:t[0].IsVisible=t[3]
	@staticmethod
	def cut(pads):M=Kit.MARGIN;return M-pads[0],M+30+Kit.GAP-pads[1],M-pads[2],M-pads[3]
	@staticmethod
	def clip(slot,pads):
		W,H=Kit.screen();M=Kit.MARGIN
		if W<=0 or H<=0:return pads
		return(min(M,max(pads[0],M-slot[0])),pads[1],min(M,max(pads[2],M-(W-slot[0]-slot[2]))),min(M,max(pads[3],M-(H-slot[1]-slot[3]))))
	@staticmethod
	def grow(slot,pads):l,t,r,b=Seam.cut(pads);return slot[0]-l,slot[1]-t,slot[2]+l+r,slot[3]+t+b
	@staticmethod
	def can(g,hooks,mini):return not(mini or isinstance(g,ClientWin)or hooks.get("untitled"))and bool(Kit._frame_parts.get(g))and g not in Kit._scrolled and Client.on_client_thread()and Seam.titled(g)
	@staticmethod
	def holds(g,slot,pads,grown,r):
		a=Seam.recs.get(g)
		if a is None or a["slot"]!=tuple(slot)or a["pads"]!=pads or r is None or r[:2]!=grown[:2]:return False
		try:
			c=a["raw"].Children;n=int(c.Count)
			if(n!=a["n"]or(n and c[n-1]is not a["last"]))and not Seam.refresh(g,a):return False
			b=a["catch"]
			if b is not None and bool(b.CanMove)!=bool(LAYOUT.arrange):b.CanMove=bool(LAYOUT.arrange)
		except Exception:return False
		Seam.watch(a,True);return True
	@staticmethod
	def refresh(g,rec):
		a=Kit._children(rec["raw"]);b=set(a)
		if rec["catch"]is not None and rec["catch"]not in b:return False
		d=set(f for f in map(Kit.client_control,Kit._frame_parts.get(g)or())if f is not None);rec["frame"]=[h for h in rec["frame"]if h[0]in b];rec["title"]=[i for i in rec["title"]if i[0]in b];e=[j for j in a if j not in rec["kids"]]
		for c in e:
			if c in d:rec["frame"].append((c,bool(c.IsVisible)));c.IsVisible=False
		Seam.adopt(rec,[k for k in e if k not in d]);rec["kids"],rec["n"],rec["last"]=b,len(a),a[-1]if a else None;return True
	@staticmethod
	def adopt(rec,new):
		M=Kit.MARGIN;a=30+Kit.GAP
		for c in new:
			r=Kit._raw_rect(c)
			if r is None or not(M-4<=r[1]<M+34 and r[1]+r[3]<=M+36):continue
			rec["title"].append([c,r[0],r[1],bool(c.IsVisible)]);c.Location=ClientWin.point(r[0],r[1]+a);c.IsVisible=rec["open"]and rec["title"][-1][3]
	@staticmethod
	def watch(rec,trimmed):
		M=Kit.MARGIN;a=30+Kit.GAP
		for c,v in rec.get("frame",())if trimmed else():
			try:
				if c.IsVisible:c.IsVisible=False
			except Exception:pass
		for t in rec["title"]:
			c=t[0]
			try:
				r=Kit._raw_rect(c)if trimmed else None
				if r is not None and r[1]<M+34:t[1],t[2],t[3]=r[0],r[1],bool(c.IsVisible);c.Location=ClientWin.point(r[0],r[1]+a);c.IsVisible=rec["open"]and t[3]
				elif not rec["open"]and bool(c.IsVisible):t[3]=True;c.IsVisible=False
			except Exception:pass
	@staticmethod
	def trim(g,slot,pads):
		b=Kit._raw_gump(g)
		if b is None:return False
		M=Kit.MARGIN;j=30+Kit.GAP;k=set(p for p in map(Kit.client_control,Kit._frame_parts.get(g)or())if p is not None);f,h=[],[]
		for c in Kit._children(b):
			r=Kit._raw_rect(c)
			if r is None:continue
			i=bool(c.IsVisible)
			if c in k:c.IsVisible=False;f.append((c,i))
			elif M-4<=r[1]<M+34 and r[1]+r[3]<=M+36:c.IsVisible=False;c.Location=ClientWin.point(r[0],r[1]+j);h.append([c,r[0],r[1],i])
		l,t=Seam.cut(pads)[:2];d=G.CreateGumpColorBox(.01,"#000000");d.SetRect(l,t,slot[2],slot[3]);g.Add(d);Kit.flush();a=Kit.client_control(d)
		if a is not None and b.Children.Remove(a):
			b.Children.Insert(0,a);a.AcceptMouseInput=True;a.CanMove=bool(LAYOUT.arrange)
			if len(Seam.catchers)>64:
				for m in[q for q in Seam.catchers if q.IsDisposed]:Seam.catchers.pop(m,None)
			Seam.catchers[a]=g
		o=bool(b.AcceptMouseInput);Kit._prune(Seam.recs,32)
		if a is not None and a in Seam.catchers:b.AcceptMouseInput=False
		e=Kit._children(b);n=len(e);Seam.recs[g]={"slot":tuple(slot),"pads":pads,"raw":b,"n":n,"frame":f,"title":h,"open":False,"until":0.,"box":d,"catch":a,"mouse":o,"last":e[-1]if n else None,"kids":set(e)};return True
	@staticmethod
	def undo(g):
		a=Seam.recs.pop(g,None)
		if a is None or not Kit.is_open(g):return False
		Seam.bare.pop(g,None);b=Kit._frame_want.get(g)
		for c,x,y,d in[(e,None,None,f if b is None else b)for e,f in a["frame"]]+a["title"]:
			with Kit.quiet:
				if x is not None:c.Location=ClientWin.point(x,y)
				c.IsVisible=d
		a["raw"].AcceptMouseInput=a["mouse"];Seam.catchers.pop(a.get("catch"),None);Kit.dispose(a["box"]);return True
	@staticmethod
	def undo_all():
		for g in list(Seam.recs):Seam.undo(g)
		for g in list(Seam.bare):Seam.unstrip(g)
	@staticmethod
	def hover(d=False):
		if not(Seam.recs or Seam.bare):return
		m=Kit.mouse_pos();b=time.time();e=(m,d,len(Seam.recs),len(Seam.bare))
		if e==Seam.seen[0]and b<Seam.seen[1]:return
		Seam.seen[0],Seam.seen[1]=e,b+.25
		for f,h in((Seam.recs,True),(Seam.bare,False)):
			for g,a in list(f.items()):
				if not a["title"]:continue
				if not Kit.is_open(g):f.pop(g,None);continue
				r=a["slot"]if h else Kit.rect(g)
				if r is None:continue
				x,y,w,k=r;i=a["pads"][1]if h else Kit.MARGIN+4;j=30+i if a["open"]else REVEAL_H
				if d or(m is not None and x<=m[0]<x+w and y<=m[1]<y+j):a["until"]=b+REVEAL_HOLD
				c=b<a["until"]
				if c:Seam.seen[1]=min(Seam.seen[1],a["until"])
				if c!=a["open"]:
					a["open"]=c
					for t in a["title"]:
						try:t[0].IsVisible=c and t[3]
						except Exception:pass
SNAP=Snap()
ALERTS=Alerts()
GUARD=Guard()
LAYOUT=Layout()
HOST=Host()
MODULE_FILES=(("actionbar","Action Bar","ActionBarModule.py"),("hud","Character HUD","CharacterHudModule.py"),("interface","Interface","InterfaceModule.py"),("inventory","Inventory","InventoryModule.py"),("grimoire","Grimoire","GrimoireModule.py"),("worldmap","World Map","WorldMapModule.py"),("ultima","Ultima Tracker","UltimaTrackerModule.py"),("social","Social","SocialModule.py"),("skills","Skills","SkillsModule.py"),("butler","Property Butler","PropertyButlerModule.py"),("meters","Meters","MetersModule.py"),("mongotchi","Mongotchi","MongotchiModule.py"),)
RETIRED_KEYS=("autodoors",)
def module_folders():
	c=[];a=str(API.ScriptPath or "").rstrip("/\\")
	if a:
		if os.path.isfile(a):a=os.path.dirname(a)
		c+=[a,os.path.dirname(a)]
	with Kit.quiet:import System;d=str(System.AppDomain.CurrentDomain.BaseDirectory).rstrip("/\\");c+=[os.path.join(d,"LegionScripts"),d]
	b={}
	for p in c:
		if not p:continue
		for n in(safe(lambda:os.listdir(p),[])or[]):
			if n in b or not(n.startswith("VirtueAssistant")and n.endswith("Modules")):continue
			e=os.path.join(p,n)
			if os.path.isdir(e):b[n]=e
	f=([MODULE_DIR]if MODULE_DIR in b else[])+sorted(g for g in b if g!=MODULE_DIR);return[b[h]for h in f]
def _read_text(path):
	try:
		with open(path,"r")as f:return f.read()
	except Exception:import System;return str(System.IO.File.ReadAllText(path))
class _Reg(object):
	ok=False
	def take(self,key,title,desc,a=None,interval=None,default_on=False,category=None,parts=(),aliases=()):self.key,self.title,self.desc=str(key),str(title),str(desc);self.interval=interval if isinstance(interval,(int,float))else None;self.default_on=bool(default_on);self.category=category;self.parts=tuple(tuple(b)for b in(parts or()));self.aliases=tuple(aliases or());self.ok=True
def _balanced(text,start):
	c,i,n=0,start,len(text);b=None
	while i<n:
		a=text[i]
		if b:
			if a=="\\":i+=2;continue
			if a==b:b=None
		elif a in "\"'":b=a
		elif a=="#":j=text.find("\n",i);i=n if j<0 else j;continue
		elif a=="(":c+=1
		elif a==")":
			c-=1
			if c==0:return text[start+1:i]
		i+=1
	return
def read_registration(text):
	d=text.rfind("HOST.add(")
	if d<0:return
	a=_balanced(text,d+len("HOST.add"))
	if a is None:return
	b={}
	for e in set(re.findall(r"[A-Za-z_]\w*",a)):v=globals().get(e);b[e]=v if isinstance(v,(int,float))and not isinstance(v,bool)else None
	c=_Reg();b["_reg"]=c.take
	try:eval("_reg("+a+")",{"__builtins__":{}},b)
	except Exception:return
	return c if c.ok else None
def load_modules():
	h=module_folders()
	if not h:Kit.say("no %s folder beside this script, so no modules loaded."%MODULE_DIR,Kit.HUE_BAD);return
	i=dict((z,x)for x,(y,y,z)in enumerate(MODULE_FILES));d,j=[],set()
	for k in h:
		for n in sorted(A for A in safe(lambda:os.listdir(k),[])or[]if A.endswith("Module.py")):
			if n not in j:j.add(n);d.append((k,n))
	d.sort(key=lambda e:i.get(e[1],len(i)));r=dict((D,(B,C))for B,C,D in MODULE_FILES)
	for t,a in d:
		b=os.path.join(t,a)
		if not os.path.isfile(b):continue
		m=None
		try:
			l=_read_text(b);m=read_registration(l)
			if m is not None and m.key in RETIRED_KEYS:Kit.say("skipped %s (retired; the file can be deleted)."%a,Kit.HUE_INFO);continue
			if m is not None and m.key in HOST.old_map and HOST.old_map[m.key][0]!=m.key:o,w=HOST.old_map[m.key];p=dict.get(HOST.by_key,o);Kit.say("skipped %s (now part of %s; the file can be deleted)."%(a,p.title if p else o),Kit.HUE_INFO);continue
			if m is not None and dict.__contains__(HOST.by_key,m.key):API.SysMsg(HOST.TWICE%(APP_NAME,m.title,m.key),Kit.HUE_BAD);continue
			if m is not None and m.interval is not None:HOST.add_lazy(m.key,m.title,m.desc,b,m.interval,m.default_on,m.category,m.parts,m.aliases);continue
			exec(compile(l,b,"exec"),globals())
		except Exception as c:
			q=getattr(c,"lineno",None)
			if q:f="%s (%s line %s)"%(getattr(c,"msg",None)or c,a,q)
			else:f="%s%s"%(c,_error_where())
			Kit.say("couldn't load %s (%s)."%(a,f),Kit.HUE_BAD);g=(m.key,m.title)if m is not None else r.get(a)
			if g is not None and not dict.__contains__(HOST.by_key,g[0]):u,v=g;s=HOST.add(u,v,"",lambda:None,.1);s.api,s.broken=None,f
Kit.data_setup()
PROFILES=Profiles()
if not VA_ALONE:
	try:PROFILES.startup()
	except Exception as _ex:Kit.say("couldn't put the favourite profile on this character (%s%s)."%(Tz.why(_ex),_error_where()),Kit.HUE_BAD)
def _module_sysstats():
	o=HOST.dock_remove;h=HOST.layout_holds;p=Kit.add_label;i=Kit.put_var;q=Kit.save_pos;r=Kit.set_text;b="sysstats";j="System Stats";v,k,l,e=("SystemStats_pos","SystemStats_min","SystemStats_btn","SystemStats_open");W,w,x=240,240,46;s=.3;y=7981;m=("Ping","FPS","Frame","Memory","In","Out","Packets");a={"shutting":False,"minimized":False,"docked":False,"open":False,"queue":[],"next":0.,"vals":{},"tip":None};f={"g":None,"c":{},"store":({},{})};d={"g":None,"b":None,"store":({},{})};z=Kit.queuer(a)
	def A():
		v={}
		with Kit.quiet:b=int(Tz.get(None,"CurrentRefreshRate",Tz.T("ClassicUO.CUOEnviroment")));v["FPS"]=str(b);v["Frame"]="%.1f ms"%(1000./b)if b>0 else "-"
		with Kit.quiet:c=Tz.get(None,"Socket",Tz.T("ClassicUO.Network.AsyncNetClient"));a=Tz.get(c,"Statistics");d=str(Typing._get(a,"CurrentPingSource",default="")or "");v["Ping"]="off"if d.endswith("Disabled")else "%d ms"%int(Tz.get(a,"Ping"));v["In"]="%.1f KB/s"%(int(Tz.get(a,"DeltaBytesReceived"))/1024.);v["Out"]="%.1f KB/s"%(int(Tz.get(a,"DeltaBytesSent"))/1024.);v["Packets"]="%d in, %d out"%(int(Tz.get(a,"TotalPacketsReceived")),int(Tz.get(a,"TotalPacketsSent")))
		with Kit.quiet:import System;v["Memory"]="%d MB"%(int(System.GC.GetTotalMemory(False))//(1024*1024))
		return v
	def B():x,y=Kit.load_pos(l,(8,200),(46,46));b=({},{});g=G.CreateGump(True,True);Kit.add_window_frame(g,46,46,corners=False);a["tip"]=None;c=Kit.art_button(g,b,"stats",Kit.ART_CIRCLE,12,12,None,"System stats",on_click=z("toggle"));Kit.show_window(g,x,y,46,46,None,False,None,lambda:q(l,g),d,{"g":g,"b":c,"store":b})
	def g():
		M=Kit.MARGIN;h=M+30+Kit.GAP+len(m)*20+M-12;g,f,e=c.begin(W,h)
		if not a["minimized"]:
			c.frame(g,settings=False);b=M+30+Kit.GAP;Kit.add_section(g,M,b,W-2*M,h-b-M)
			for i,d in enumerate(m):p(g,d+":",M+10,b+6+i*20,Kit.HUE_INFO);e[d]=p(g,"",M+90,b+6+i*20,Kit.HUE_TEXT)
		c.end(g);t()
	c=Kit.Window(b,j,a,f,g,v,default=(70,200),mini=(w,x),icon=y)
	def t():
		v=a["vals"];c=f["c"]
		if a["minimized"]:
			b=c.get("status")
			if b is not None:r(b,"%s: %s, %s FPS"%(j,v.get("Ping","-"),v.get("FPS","-")))
			return
		for d in m:
			b=c.get(d)
			if b is not None:r(b,v.get(d,"-"))
	def n():a["open"]=True;g();c.dock()
	def u():a["open"]=False;o(b);c.close();i(e,"0")
	def C():
		a.update({"shutting":False,"docked":False,"queue":[],"next":0.,"minimized":Kit.load_min(k)or HOST.dock_wanted(b),"open":Kit.get_var(e,"0")=="1"});B()
		if a["open"]or h(b):n()
	def D():
		m=time.time()
		while a["queue"]:
			c=a["queue"].pop(0)
			if c=="toggle":
				if a["open"]and not h(b):u()
				elif not a["open"]:i(e,"1");a["minimized"]=a["docked"]=False;n()
			elif c=="redraw":
				if a["open"]:g()
			else:Kit.win_action(c,a,b,j,g,k)
		if a["open"]and Kit.was_clicked(f["store"],"close"):u()
		if not 0<=a["next"]-m<=s:
			if not a["open"]and h(b):n()
			a["next"]=m+s;v=a["vals"]=A();l="Ping %s, %s FPS, memory %s; click to open or close the window"%(v.get("Ping","-"),v.get("FPS","-"),v.get("Memory","-"))
			if l!=a["tip"]and d["b"]is not None:a["tip"]=l;Kit.with_tip(d["b"],l)
			if a["open"]and f["g"]is not None and not(a["minimized"]and a["docked"]):t()
	def E():a["shutting"]=True;o(b);Kit.save_min(k,a["minimized"]);i(e,"1"if a["open"]else "0");c.close();f,d["g"]=d["g"],None;q(l,f);Kit.dispose(f)
	return{"start":C,"tick":D,"stop":E,"client_tick":True}
if not VA_ALONE:load_modules();HOST.add("sysstats","System Stats","Ping, FPS and memory button",_module_sysstats,.1,category="On screen");HOST.run()
