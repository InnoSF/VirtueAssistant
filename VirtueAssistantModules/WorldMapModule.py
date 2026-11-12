def _module_worldmap():
	C=HOST.alert;D=HOST.alert_kind;k=HOST.dock_forget;J=HOST.dock_wanted;K=HOST.layout_holds;E=HOST.release_cursor;L=HOST.show_settings;M=Journal.reader;U="worldmap";N="World Map";F="VA ";H="WorldMap_atlas_placed";O="WorldMap_atlas";P=(("corpse","your corpse"),("maps","your dig spots"),("dry","the spots that ran dry"),("traps","the traps you have seen"));V=1.;Q=2.5;W=.5;o=2.;R=3;X=60;Y={"at":-1.,"ok":False,"map":False,"arrow":False}
	def S(fresh=False):
		a=Y;b=time.time()
		if not fresh and 0.<=b-a["at"]<W:return a
		a["at"]=b;c=d=False
		try:e=[str(f.GetType().Name)for f in Tz.windows(("WorldMapGump","QuestArrowGump"))];c,d="WorldMapGump"in e,"QuestArrowGump"in e;a["ok"]=True
		except Exception:a["ok"]=False
		a["map"],a["arrow"]=c,d;return a
	class Atlas(object):
		def __init__(self):self.items,self.on,self.placed,self.want,self.loose={},{},{},{},set();self.synced=True;self.open_since=self.saved=None;self.next_check=0.;self.loaded=self.strip_pending=False;self.chg={}
		def load(self):
			if self.loaded:return
			self.loaded=True
			for k,v in Kit.codec_load(Kit.get_var(O)).items():self.on[k]=v!="0"
			a=str(API.GetPersistentVar(H,"",API.PersistentVar.Global)or "")
			for b in a.split("\n"):
				p=b.split("|")
				if len(p)==5 and p[0].startswith(F):
					try:self.placed[p[0]]=(int(p[1]),int(p[2]),int(p[3]),p[4])
					except ValueError:pass
			self.saved=a;self.strip_pending=bool(self.placed)and not self.map_open(True);self._rebuild()
		def is_on(self,owner):self.load();return self.on.get(owner,True)
		def set_on(self,owner,on):
			self.load()
			if self.on.get(owner,True)!=bool(on):self.on[owner]=bool(on);Kit.put_var(O,";".join("%s=%d"%(a,1 if self.on.get(a,True)else 0)for a,d in P));self._rebuild()
		def set(self,owner,items):
			self.load()
			if self.items.get(owner)!=items:self.items[owner]=dict(items);self._rebuild()
		def clear(self,owner):
			if self.items.pop(owner,None):self._rebuild()
		def _rebuild(self):
			a={}
			for b,c in self.items.items():
				if self.on.get(b,True):
					for d,v in c.items():
						if len(a)>=X:break
						a[d]=v
			self.want=a;self.synced=a==self.placed
		def map_open(self,fresh=False):f=S(fresh);return f["ok"]and f["map"]
		def tick(self):
			if self.synced or self.strip_pending:return
			a=time.time()
			if a<self.next_check and self.next_check-a<=o+V:return
			if not self.map_open():self.open_since=None;self.next_check=a+Q;return
			if self.open_since is None or self.open_since>a:self.open_since=a
			if a-self.open_since<o:self.next_check=self.open_since+o;return
			if not self.map_open(True):self.open_since=None;self.next_check=a+Q;return
			self.next_check=a+.25;c=0
			for b in list(self.placed):
				if c>=R:break
				if self.want.get(b)!=self.placed[b]:API.RemoveMapMarker(b);self._drop(b);c+=1
			for b,v in self.want.items():
				if c>=R:break
				if b not in self.placed:API.AddMapMarker(b,v[0],v[1],v[2],v[3]);self._put(b,v);c+=1
			self.synced=self.want==self.placed;self._save()
		def thread_work(self):
			if not self.strip_pending and not self.loose:return
			a=Kit.on_client(lambda:self.map_open(True))
			if self.strip_pending:
				if not a and self._strip_file():self._drop_all();self._save()
				self.strip_pending=False;self.synced=self.want==self.placed
			if self.loose:
				if a:
					for b in list(self.loose):API.RemoveMapMarker(b)
				else:self._strip_file()
				self.loose.clear()
		def _put(self,name,v):self.placed[name]=v;self.chg[name]="%s|%d|%d|%d|%s"%(name,v[0],v[1],v[2],v[3])
		def _drop(self,name):self.placed.pop(name,None);self.chg[name]=None
		def _drop_all(self):
			for a in list(self.placed):self._drop(a)
		def _save(self):
			if not self.chg:return
			try:b=str(API.GetPersistentVar(H,"",API.PersistentVar.Global)or "")
			except Exception:return
			a=Kit.merge_text(b,self.chg,lambda l:l.split("|",1)[0])[0];self.chg={};self.saved=a;safe(lambda:API.SavePersistentVar(H,a,API.PersistentVar.Global))
		def shutdown(self):
			self.items.clear();self.want={};self.strip_pending=False
			if not self.placed and not self.loose:self.synced=True;return
			if self.map_open(True):
				for a in list(self.placed)+list(self.loose):API.RemoveMapMarker(a)
				self._drop_all()
			elif self._strip_file():self._drop_all()
			self.loose.clear();self.synced=not self.placed;self._save()
		def _strip_file(self):
			try:
				e=str(Tz.get(None,"ExecutablePath",Tz.T("ClassicUO.CUOEnviroment")));b=os.path.join(e,"Data","Client")
				if not os.path.isdir(b):return False
				a=os.path.join(b,"userMarkers.usr")
				if not os.path.exists(a):return True
				import io
				with io.open(a,"r",encoding="utf-8-sig")as f:c=f.read().splitlines()
				g=set(self.placed)|self.loose;d=[j for j in c if len(j.split(","))<4 or j.split(",")[3]not in g]
				if len(d)!=len(c):Kit.write_safe(a,u"".join(m+u"\n"for m in d))
				return True
			except Exception:return False
	b=Atlas()
	def q(text):return F+str(text).replace(","," ")
	def I(fresh=False):f=S(fresh);return f["arrow"]if f["ok"]else True
	u={}
	def z(owner):
		def a(f,x,y):u[owner]=Kit.add_check(f.g,"Show %s on TazUO's World Map"%dict(P).get(owner,owner),x+12,y,b.is_on(owner),"Markers named \"%s...\" while the map is open; removed when unticked or the part stops"%F)
		return "TAZUO'S WORLD MAP  (while open)",(("custom",26,a),),{"sh":66}
	def A(api,owner):
		c,d,e=api["poll_config"],api["config_closed"],api["stop"]
		def f():
			c();a=u.get(owner)
			if a is not None:
				try:d=bool(a.IsChecked)
				except Exception:return
				if d!=b.is_on(owner):b.set_on(owner,d)
		def g():d();u.pop(owner,None)
		def h():
			try:e()
			finally:u.pop(owner,None);b.clear(owner)
		a=dict(api);a.update({"poll_config":f,"config_closed":g,"stop":h});return a
	T={"said":False}
	def Z():
		try:b.tick()
		except Exception as a:
			if not T["said"]:T["said"]=True;API.SysMsg("%s: couldn't update TazUO's World Map (%s)."%(N,a),Kit.HUE_BAD)
	def aa():
		try:b.thread_work()
		except Exception:b.strip_pending=False
	ab={"tick":Z,"stop":b.shutdown,"thread_tick":aa,"thread_wanted":lambda:b.strip_pending or b.loose};ac=("TazUO","World Map","Map Pings","Enhanced Map","Virtue Assistant","Settings","Inventory","Need help","Look here","Go here","Danger!")
	def B(text):
		text=str(text or "")
		if not text or text[0]in "[(\"'"or text.startswith(ac):return text
		return text[0].lower()+text[1:]
	def c(x,y,fmt="%d, %d"):return Kit.veil("xy",fmt%(x,y))
	def h(rows,row_h):return 2*Kit.MARGIN+30+2*Kit.GAP+36+30+rows*row_h+8
	def i(a,st,b,c):
		z=a.slot
		if z is None or st["minimized"]or not K(a.key)or z[0]<b or z[1]<c:return
		return z
	def ad():
		a8="pings";Q="Map Pings";aa=8887;u={"look":"CTRL+1","danger":"CTRL+2","go":"CTRL+3","help":"CTRL+4",};ai=("look","danger","go","help");ab=60;aj=.75;ak=5;aE=(490,775,508,514);al=200;ac=10;A=ad=M=None
		def am():
			nonlocal A,ad,M
			if M is None:
				try:import _socket as so;import select as se;A,ad,M=so,se,True
				except Exception:M=False
			return M
		import collections;v="EMPings.";an=v+"options";F,N,R,S=0,1,2,3;T=[("auto","TazUO's map if on, else my login"),("tazuo","Only TazUO's Enhanced Map"),("own","Only my own login")];ae=[bg[0]for bg in T];H={"ping_secs":(2,60),"drag":(5,200)};j={"sounds":True,"share":True,"gesture":True,"connection":"auto","ping_secs":8,"drag":25};a9=dict(j);l={"minimized":False,"shutting":False,"docked":False,"queue":[],"app":None};ba={"g":None,"c":{},"store":({},{})};ao,bb,q=Kit.basics(l,Q)
		def aF():
			for k,v in Kit.codec_load(Kit.get_var(an)).items():
				if k in("sounds","share","gesture"):j[k]=v=="1"
				elif k=="connection"and v in ae:j[k]=v
				elif k in H:
					try:a,b=H[k];j[k]=max(a,min(b,int(v)))
					except ValueError:pass
				elif k.startswith("hk_")and k[3:]in u:u[k[3:]]=_norm_key(v)
		def U():a="sounds=%d;share=%d;gesture=%d;connection=%s"%(j["sounds"],j["share"],j["gesture"],j["connection"]);a+="".join(";hk_%s=%s"%(d,u[d].replace(";",""))for d in ai);a+=";ping_secs=%d;drag=%d"%(int(j["ping_secs"]),int(j["drag"]));Kit.put_var(an,a)
		def bc():pass
		bd=None
		def be():pass
		bf={};af={"look":F,"danger":N,"go":R,"help":S};ap={"up":F,"right":N,"down":R,"left":S};C={F:("Look here",53,14138,"yellow"),N:("Danger!",33,14089,"red"),R:("Go here",68,14186,"green"),S:("Need help",88,14170,"blue"),};V=0x50494E47
		def s(t):return C[t][0]
		def O(m):return Kit.FACETS[m]if 0<=m<len(Kit.FACETS)else "map %d"%m
		def I(a,payload=b""):return struct.pack("<BH",a,3+len(payload))+payload
		def aG(user,a):u,p=user.encode("latin-1","replace"),a.encode("latin-1","replace");return I(31,struct.pack("<BB",len(u),len(p))+u+p)
		def aq(x,y):return I(39,struct.pack("<HH",x&65535,y&65535))
		W=32768
		def aH(a,ay):
			if not(a&W and ay&W):return
			return a&8191,ay&4095,(ay>>12)&7,(a>>13)&3
		def aI(x,y,m,t):
			if 0<=x<8192 and 0<=y<4096 and 0<=m<8 and 0<=t<4:return aq(W|(t<<13)|x,W|(m<<12)|y)
		def aJ(pos,stats,flag,color):return I(37,struct.pack("<HHB6HBBBIB",pos[0]&65535,pos[1]&65535,pos[2]&255,*([max(0,min(d,65535))for d in stats]+[flag,0,0,color&0xFFFFFFFF,5]))+b"Arial"+struct.pack("<fB",12.,1))
		class Reader(object):
			def __init__(self,data,offset=3):self.d,self.p=data,offset
			def take(self,n):
				if self.p+n>len(self.d):raise ValueError("short packet")
				self.p+=n;return self.d[self.p-n:self.p]
			def u8(self):return bytearray(self.take(1))[0]
			def u16(self):return struct.unpack("<H",self.take(2))[0]
			def ascii(self,n):return bytes(self.take(n)).decode("latin-1")
		class PySocketTransport(object):
			def __init__(self,host,port,timeout):
				a=None
				for b,c,d,g,e in A.getaddrinfo(host,port,0,A.SOCK_STREAM):
					s=None
					try:s=A.socket(b,c,d);s.settimeout(timeout);s.connect(e);break
					except OSError as f:
						a=f
						if s is not None:s.close()
				else:raise a if a is not None else OSError("getaddrinfo returns an empty list")
				self.s=s;s.settimeout(ak)
			def send(self,data):self.s.sendall(data)
			def recv(self):
				r,b,b=ad.select([self.s],[],[],0)
				if not r:return b""
				a=self.s.recv(8192)
				if not a:raise EOFError()
				return a
			def close(self):safe(lambda:self.s.close())
		class DotNetTransport(object):
			def __init__(self,host,port,timeout):
				import clr;from System.Net.Sockets import TcpClient,SelectMode;self._select_read=SelectMode.SelectRead;from System import Array,Byte;self._Array,self._Byte=Array,Byte;self.c=TcpClient();a=self.c.ConnectAsync(host,port)
				if not a.Wait(int(timeout*1000))or not self.c.Connected:self.c.Close();raise IOError("timed out")
				self.st=self.c.GetStream();self.st.WriteTimeout=int(ak*1000)
			def send(self,data):a=self._Array[self._Byte](bytearray(data));self.st.Write(a,0,len(a))
			def recv(self):
				if not self.c.Connected:raise EOFError()
				n=self.c.Available
				if n<=0:
					if self.c.Client.Poll(0,self._select_read):raise EOFError()
					return b""
				a=self._Array.CreateInstance(self._Byte,n);b=self.st.Read(a,0,n)
				if b<=0:raise EOFError()
				return bytes(bytearray(a)[:b])
			def close(self):safe(lambda:self.c.Close())
		def aK(host,port,timeout=5):
			if am():
				try:return PySocketTransport(host,port,timeout)
				except(A.timeout,A.gaierror,ConnectionError,OSError):raise
				except Exception:pass
			return DotNetTransport(host,port,timeout)
		class Sender(object):
			def __init__(self,a):
				self.t=a;self.error=self.wake=None;self.stopped=False;self.q=collections.deque()
				try:import _thread;self.wake=_thread.allocate_lock();self.wake.acquire();_thread.start_new_thread(self._run,())
				except Exception:self.wake=None
			def send(self,data):
				if self.error is not None or self.stopped:raise self.error or IOError("sender stopped")
				if self.wake is None:self.t.send(data);return
				self.q.append(data);self.poke()
			def poke(self):
				with Kit.quiet:self.wake.release()
			def _run(self):
				while not self.stopped:
					if not self.q:self.wake.acquire(True,.5);continue
					try:a=self.q.popleft()
					except IndexError:continue
					try:self.t.send(a)
					except Exception as b:self.error=b;return
			def stop(self):
				self.stopped=True
				if self.wake is not None:self.q.clear();self.poke()
		class MapConnection(object):
			kind="own";owns_position=True;server_relays_ping=True;OFF,HANDSHAKE,LOGIN,READY=range(4)
			def __init__(self,host,port,user,a):self.host,self.port,self.user,self.password=host,port,user,a;self.t=self.gave_up=self.connecting=self.sender=None;self.state=self.OFF;self.buf=bytearray();self.next_try=self.login_failures=self.last_sent=self.state_since=self.ready_since=0;self.backoff=3;self.kicks=[];self.name=user;self.unreachable_reported=False
			def close(self):
				if self.connecting is not None:
					a,self.connecting=self.connecting,None
					with a["lock"]:a["abandon"]=True;b=a["done"]
					if b and a["t"]is not None:a["t"].close()
				if self.sender is not None:self.sender.stop();self.sender=None
				if self.t:self.t.close()
				self.t=None;self.state=self.OFF;self.buf=bytearray()
			def _drop(self,events,kind,detail,a):
				c=self.state;self.close();b=time.time()
				if c==self.LOGIN and kind=="eof":
					self.login_failures+=1
					if self.login_failures>=3:self.gave_up="Login refused 3 times. Check the map username and password.";events.append(("status",self.gave_up,True));return
					events.append(("status","Login refused (wrong username or password?). Retrying in %d s."%a,True))
				elif c==self.LOGIN:events.append(("status","Login problem (%s). Retrying in %d s."%(detail,a),True))
				elif c==self.READY:
					if kind=="eof"and b-self.ready_since<6:d="Dropped right after login. Is this map account logged in elsewhere (Enhanced Map)?"
					elif kind=="eof":d="Lost the map server."
					else:d="Connection problem (%s)."%detail
					self.kicks=[f for f in self.kicks if b-f<300]+[b]
					if len(self.kicks)>=4:self.gave_up=("Kept getting dropped. Is this map account logged in elsewhere (Enhanced Map)? Use a separate account, then click Reconnect.");events.append(("status",self.gave_up,True));return
					events.append(("status","%s Reconnecting in %d s."%(d,a),True))
				else:e={"eof":"Server closed the connection","timeout":"Server didn't answer"}.get(kind,"Connection problem");events.append(("status","%s (%s). Retrying in %d s."%(e,detail or "handshake",a),False))
				self.next_try=b+a
			def reset(self):self.close();self.gave_up=None;self.login_failures=self.next_try=0;self.kicks=[];self.backoff=3
			@property
			def ready(self):return self.state==self.READY
			def send(self,data):
				if not self.t:return
				try:
					if self.sender is not None:self.sender.send(data)
					else:self.t.send(data)
					self.last_sent=time.time()
				except Exception:self.close();self.next_try=time.time()+3
			def poll(self):
				a=[];d=time.time()
				if self.gave_up:return a
				if self.t is None:
					if d<self.next_try:return a
					b=self.connecting
					if b is None:
						import _thread;am();b=self.connecting={"done":False,"t":None,"err":None,"abandon":False,"lock":_thread.allocate_lock()}
						def h(p=b,host=self.host,port=self.port):
							try:p["t"]=aK(host,port)
							except Exception as a:p["err"]=a
							with p["lock"]:p["done"]=True;b=p["abandon"]
							if b and p["t"]is not None:p["t"].close()
						try:_thread.start_new_thread(h,())
						except Exception:h()
					if not b["done"]:return a
					self.connecting=None;d=time.time()
					try:
						if b["err"]is not None:raise b["err"]
						if b["t"]is None:raise IOError("no connection")
						self.t=b["t"]
					except Exception as e:self.backoff=min(self.backoff*2,60);a.append(("status","Can't reach the map server at %s:%d (%s). Retrying in %d s."%(self.host,self.port,P(e),self.backoff),not self.unreachable_reported));self.unreachable_reported=True;self.next_try=d+self.backoff;return a
					self.state=self.HANDSHAKE;self.state_since=d;self.buf=bytearray();self.sender=Sender(self.t);self.send(I(43,b"\x00"));a.append(("status","Connecting",False))
				c=None;g=self.sender
				if g is not None and g.error is not None:e=g.error;c=("error","%s: %s"%(e.__class__.__name__,P(e)))
				try:
					i=self.t.recv()if self.t else b""
					if i:
						self.buf.extend(i)
						if len(self.buf)>1<<20:raise IOError("too much data")
				except EOFError:c=("eof","")
				except Exception as e:c=("error","%s: %s"%(e.__class__.__name__,P(e)))
				while len(self.buf)>=3 and self.t is not None:
					j=self.buf[0];f=self.buf[1]|(self.buf[2]<<8)
					if f<3:self._drop(a,"garbled","bad packet size",10);return a
					if len(self.buf)<f:break
					k=bytes(self.buf[:f]);del self.buf[:f]
					try:self._handle(j,k,a)
					except ValueError:pass
				if c and self.t is not None:self._drop(a,c[0],c[1],30 if self.state==self.LOGIN else 10);return a
				if(self.t is not None and self.state in(self.HANDSHAKE,self.LOGIN)and d-self.state_since>15):self._drop(a,"timeout","no reply in 15 s",15)
				return a
			def _handle(self,a,data,events):
				r=Reader(data)
				if a==43 and self.state==self.HANDSHAKE:self.state=self.LOGIN;self.state_since=time.time();self.send(aG(self.user,self.password))
				elif a==31 and self.state==self.LOGIN:
					if r.u8()==1:b=bool(self.login_failures or self.kicks or self.unreachable_reported);r.u8();self.name=r.ascii(r.u8())or self.user;self.state=self.READY;self.ready_since=time.time();self.login_failures=0;self.backoff=3;self.unreachable_reported=False;events.append(("status","Connected as %s."%self.name,b))
					else:self._drop(events,"eof","login rejected",30)
				elif a in(51,39)and self.state==self.READY:events.append(ar(a,r))
				elif a==47 and self.state==self.READY:events.append(("message",r.ascii(r.u16())))
		def ar(a,r):
			if a==51:x,y,m,t=r.u16(),r.u16(),r.u8(),r.u8();return("ping",r.ascii(r.u8()),x,y,m,t if t in C else F)
			x,y=r.u16(),r.u16();return("alert",r.ascii(r.u8()),x,y)
		class TazUOBridge(object):
			HOOK_KEY="EMPings.OnFrameHook"
			def __init__(self):
				import clr;clr.AddReference("System.Collections.Concurrent");from System import Array,Byte,Action,Delegate,AppDomain;from System.Reflection import BindingFlags;from System.Collections.Concurrent import ConcurrentQueue;self._Array,self._Byte,self._Delegate,self._AppDomain=(Array,Byte,Delegate,AppDomain);a=BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Instance;d=BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Static;b=API.GetType().Assembly.GetType("ClassicUO.Game.Managers.EnhancedMap.EnhancedMapManager");f=b.GetProperty("Instance",d);self._p_connected=b.GetProperty("IsConnected",a);self._p_config=b.GetProperty("Config",d);self._m_reconnect=b.GetMethod("Reconnect",a);g=b.GetField("_client",a);self._asm=API.GetType().Assembly;self._manager=f.GetValue(None);self._client=g.GetValue(self._manager);c=self._client.GetType();self._f_connection=c.GetField("_connection",a);self._m_send=c.GetMethod("SendRaw",a);self._f_onframe=c.GetField("OnFrame",a)
				try:self._handler,self._queue=self._make_handler()
				except Exception:
					self._queue=ConcurrentQueue[object]();e=self._queue
					def h(a,payload):
						try:
							if a in(51,39)and e.Count<200:e.Enqueue((int(a),payload))
						except Exception:pass
					self._handler=Action[Byte,Array[Byte]](h)
				self._hooked=False
			@staticmethod
			def _make_handler():import clr;clr.AddReference("System.Collections.Concurrent");clr.AddReference("System.Linq.Expressions");from System import Array,Byte,Int32,Action,Tuple,Type;from System.Collections.Concurrent import ConcurrentQueue;from System.Linq.Expressions import Expression,ParameterExpression;d,e,a=(clr.GetClrType(Byte),clr.GetClrType(Array[Byte]),clr.GetClrType(Int32));f=Tuple[Byte,Array[Byte]];b=ConcurrentQueue[f]();c=Expression.Parameter(d,"id");g=Expression.Parameter(e,"payload");q=Expression.Constant(b);h=Expression.Convert(c,a);i=Expression.OrElse(Expression.Equal(h,Expression.Constant(51,a)),Expression.Equal(h,Expression.Constant(39,a)));j=Expression.LessThan(Expression.Property(q,"Count"),Expression.Constant(200,a));k=clr.GetClrType(f).GetConstructor(Array[Type]([d,e]));l=Expression.Call(q,b.GetType().GetMethod("Enqueue"),Array[Expression]([Expression.New(k,Array[Expression]([c,g]))]));m=Expression.IfThen(Expression.AndAlso(i,j),l);n=Expression.Lambda[Action[Byte,Array[Byte]]](m,Array[ParameterExpression]([c,g]));return n.Compile(),b
			def hook(self):
				if self._hooked:return
				b=self._AppDomain.CurrentDomain;a=self._f_onframe.GetValue(self._client);c=b.GetData(self.HOOK_KEY)
				if c is not None:a=self._Delegate.Remove(a,c)
				a=self._own_handlers_only(a);self._f_onframe.SetValue(self._client,self._Delegate.Combine(a,self._handler));b.SetData(self.HOOK_KEY,self._handler);self._hooked=True
			def _own_handlers_only(self,current):
				if current is None:return
				try:
					a=None
					for d in current.GetInvocationList():
						if((d.Target is not None and d.Target.Equals(self._manager))or self._tazuo_code(d)):a=self._Delegate.Combine(a,d)
					return a
				except Exception:return current
			def _tazuo_code(self,d):
				try:return bool(d.Method.Module.Assembly.Equals(self._asm))
				except Exception:return False
			def unhook(self):
				if not self._hooked:return
				try:a=self._f_onframe.GetValue(self._client);self._f_onframe.SetValue(self._client,self._Delegate.Remove(a,self._handler));self._AppDomain.CurrentDomain.SetData(self.HOOK_KEY,None)
				finally:self._hooked=False
			def config(self):
				c=self._p_config.GetValue(None)
				if c is None:return
				return{"enabled":bool(c.Enabled),"configured":bool(c.IsConfigured),"user":str(c.Username or ""),"address":str(c.Address or ""),"port":int(c.Port),"send_location":bool(c.SendLocation)}
			def is_connected(self):return bool(self._p_connected.GetValue(self._manager))
			def send(self,data):
				a=self._f_connection.GetValue(self._client)
				if a is None:return
				b=self._Array[self._Byte]([int(d)for d in bytearray(data)]);self._m_send.Invoke(self._client,self._Array[object]([a,b]))
			def reconnect(self):self._m_reconnect.Invoke(self._manager,None)
			def frames(self):
				b=[]
				for f in range(200):
					e,a=self._queue.TryDequeue()
					if not e:break
					if isinstance(a,tuple):c,d=a
					else:c,d=a.Item1,a.Item2
					b.append((int(c),bytes(bytearray([int(g)for g in d]))))
				return b
		class TazUOMouse(object):
			def __init__(self):import clr;from System.Reflection import BindingFlags;a=BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Static;b=API.GetType().Assembly;c=b.GetType("ClassicUO.Input.Mouse");d=b.GetType("ClassicUO.Game.SelectedObject");e=b.GetType("ClassicUO.Game.Managers.UIManager");self._pos=c.GetField("Position",a);self._mclick=c.GetField("MClickPosition",a);self._mdown=c.GetProperty("MButtonPressed",a);self._mdown_get=None;self._over_world=e.GetProperty("IsMouseOverWorld",a);self._object=d.GetField("Object",a)
			def middle_down(self):
				a=self._mdown_get
				if a is None:a=self._mdown_get=self._mdown.GetValue
				return bool(a(None))
			def position(self,f=None):p=(self._pos if f is None else f).GetValue(None);return int(p.X),int(p.Y)
			def tile_under_mouse(self):
				if not bool(self._over_world.GetValue(None)):return
				a=self._object.GetValue(None)
				if a is None:return
				b,c=av(a.GetType())
				if b is None or c is None:return
				x,y=int(b.GetValue(a)),int(c.GetValue(a));return(x,y)if x>0 and y>0 else None
		class TazUOLink(object):
			kind="tazuo";owns_position=False;DROP_WINDOW=120;DROP_LIMIT=3
			def __init__(self,a):self.bridge=a;self.bridge.hook();self.was_connected=None;self.drops=[];self.unhooked_for_drops=self.server_relays_ping=False
			@property
			def ready(self):return self.bridge.is_connected()
			@property
			def name(self):return(self.bridge.config()or{}).get("user","")
			def poll(self):
				a=[];b=self.ready
				if b!=self.was_connected:
					if b:a.append(("status","Using TazUO's Enhanced Map login (%s)."%(self.name or "connected"),False))
					elif self.was_connected:
						c=time.time();self.drops=[f for f in self.drops if c-f<self.DROP_WINDOW]+[c]
						if len(self.drops)>=self.DROP_LIMIT and not self.unhooked_for_drops:safe(self.bridge.unhook);self.unhooked_for_drops=True;a.append(("status","TazUO's Enhanced Map keeps dropping, so Map Pings stopped listening on it (your pings still go out; others' don't show). If it still drops, the cause is elsewhere. Click Reconnect to listen again.",True))
						else:a.append(("status","TazUO's Enhanced Map connection dropped; TazUO will reconnect.",True))
					else:a.append(("status","Waiting for TazUO's Enhanced Map to connect",False))
					self.was_connected=b
				for d,e in self.bridge.frames():
					if d==51:self.server_relays_ping=True
					try:a.append(ar(d,Reader(e,0)))
					except ValueError:pass
				return a
			def send(self,data):safe(lambda:self.bridge.send(data))
			def reset(self):
				self.drops=[]
				if self.unhooked_for_drops:self.unhooked_for_drops=False;safe(self.bridge.hook)
				safe(self.bridge.reconnect)
			def close(self):safe(self.bridge.unhook)
		def P(e):s=str(e)or e.__class__.__name__;return s if len(s)<60 else s[:59]
		au={}
		def av(t):
			a=au.get(t)
			if a is None:a=au[t]=(t.GetField("X"),t.GetField("Y"))
			return a
		def aL(obj):
			if obj is None:return
			with Kit.quiet:return int(obj.X),int(obj.Y)
			with Kit.quiet:
				t=obj.GetType();a,b=av(t)
				if a is not None and b is not None:return int(a.GetValue(obj)),int(b.GetValue(obj))
				c,d=t.GetProperty("X"),t.GetProperty("Y")
				if c is not None and d is not None:return int(c.GetValue(obj,None)),int(d.GetValue(obj,None))
			return
		class Ping(object):
			def __init__(self,x,y,m,t,now,auto=False):self.x,self.y,self.map,self.type,self.auto=x,y,m,t,auto;self.created=self.next_pulse=now;self.marked,self.entry=False,None
		class HistEntry(object):
			def __init__(self,seq,at,t,who,x,y,m,local):self.seq,self.at,self.type,self.who=seq,at,t,who;self.x,self.y,self.map,self.local=x,y,m,local
		class PingDisplay(object):
			PULSE=1.4
			def __init__(self):self.pings,self.markers,self.history,self.marked=[],[],[],{};self.map_at,self.last_sound=0.,-1.;self.map_since=self.arrow_for=None;self.hist_ver=self.hist_seq=0
			def player(self):
				p=API.Player
				try:return int(p.X),int(p.Y),int(API.GetMap()),int(p.Serial)
				except Exception:return 0,0,-1,0
			def show(self,sender,x,y,m,t,local=False,who=None,auto=False):
				a=time.time();p=Ping(x,y,m,t,a,auto);self.pings.append(p)
				if len(self.pings)>12:self._expire(next((r for r in self.pings[:-1]if r.auto),self.pings[0]))
				d,e,n,l=C[t];c,f,g,h=self.player();i=Kit.where_text(x-c,y-f,"on you")if g==m and c>0 else "on %s"%O(m);who=(who or "You")if local else sender;q("%s pinged %s %s (%d, %d, %s)."%("you"if who=="You"else who,d,i,x,y,O(m)),e);self.hist_seq+=1;p.entry=HistEntry(self.hist_seq,a,t,str(who),x,y,m,bool(local));self.history.append(p.entry)
				if len(self.history)>al:del self.history[:len(self.history)-al]
				self.hist_ver+=1
				if not local and h:API.HeadMsg("%s: %s %s"%(sender,d,i),h,e)
				if g==m:
					j=(x,y,m);self.marked[j]=self.marked.get(j,0)+1;p.marked=True;API.MarkTile(x,y,e,m)
					if(not auto and c>0 and x>0 and y>0 and max(abs(x-c),abs(y-f))>2):API.TrackingArrow(x,y,V);self.arrow_for=p
				k=("%s: %s %s"%(who,d,time.strftime("%H:%M:%S"))).replace(","," ")
				if b.map_open(True):
					API.AddMapMarker(k,x,y,m,l);self.markers.append((a+60,k))
					if len(self.markers)>ab:b.loose.update([w for G,w in self.markers[:-ab]]);del self.markers[:-ab]
				self._play_sound(t,a)
			def _play_sound(self,t,now):
				if not j["sounds"]or now-self.last_sound<.3:return
				self.last_sound=now;API.PlaySound(aE[t])
			def update(self):
				if not self.pings and not self.markers:return
				a=time.time();c=None;d=j["ping_secs"]
				for p in list(self.pings):
					if a-p.created>=d:self._expire(p);continue
					if a<p.next_pulse:continue
					if c is None:c=self.player()[2]
					if p.map==c:p.next_pulse=a+self.PULSE;e,f,g,e=C[p.type];API.CreateEffect(g,type=API.EffectType.FixedXYZ,hue=f,sourceX=p.x,sourceY=p.y,duration=self.PULSE)
				if self.markers and a>=self.markers[0][0]and self._map_ready(a)and b.map_open(True):
					while self.markers and a>=self.markers[0][0]:API.RemoveMapMarker(self.markers.pop(0)[1])
			def _map_ready(self,now):
				if now>=self.map_at or self.map_at-now>2.:
					self.map_at=now+1.
					if b.map_open():
						if self.map_since is None or self.map_since>now:self.map_since=now
					else:self.map_since=None
				return self.map_since is not None and now-self.map_since>=o
			def _expire(self,p):
				if p in self.pings:self.pings.remove(p)
				if p.marked:
					a=(p.x,p.y,p.map);b=self.marked.get(a,1)-1
					if b<=0:self.marked.pop(a,None);API.RemoveMarkedTile(p.x,p.y,p.map)
					else:self.marked[a]=b
					p.marked=False
				if self.arrow_for is p:self.arrow_off()
			def arrow_entry(self):
				a=self.arrow_for
				if a is None or isinstance(a,HistEntry):return a
				return a.entry
			def arrow_to(self,e):API.TrackingArrow(e.x,e.y,V);self.arrow_for=e
			def arrow_off(self):
				if self.arrow_for is not None:API.TrackingArrow(-1,-1,V);self.arrow_for=None
			def clear(self):
				for p in list(self.pings):self._expire(p)
				if self.markers:
					a=[d for e,d in self.markers]
					if b.map_open(True):
						for c in a:API.RemoveMapMarker(c)
					else:b.loose.update(a)
				self.markers=[];API.TrackingArrow(-1,-1,V)
		class Settings(object):
			def __init__(self):
				a=API.PersistentVar.Server;self.host=API.GetPersistentVar(v+"host","",a).strip()
				try:self.port=int(API.GetPersistentVar(v+"port",str(aa),a))
				except ValueError:self.port=aa
				self.user=API.GetPersistentVar(v+"user","",a).strip();self.password=API.GetPersistentVar(v+"pass","",a)
			@property
			def complete(self):return bool(self.host and self.user and self.password and 0<self.port<65536)
			def save(self):
				a=API.PersistentVar.Server
				for k,b in(("host",self.host),("port",str(self.port)),("user",self.user),("pass",self.password)):API.SavePersistentVar(v+k,b,a)
		X="Ping History";z="pings_history";aM=v+"history_pos";Y=v+"history_min";ag=v+"history_open";aw,aN=320,46;D=24;aO=(("When",70),("Ping",80),("From",140));ax="Put the tracking arrow on this spot (click again to take it down)";aP=". Alt+click: auto-follow (again to stop)";aQ="No pings yet. Send one with a ping button, a hotkey or the wheel drag."
		class HistoryWindow(object):
			def __init__(self,app):self.app=app;self.page,self.next_draw=0,0.;self.drawn=self.drawn_pos=None;self.st={"g":None,"shutting":False,"minimized":False,"docked":False,"queue":[],"c":{},"store":({},{}),"rows":[]};self.wnd=Kit.Window(z,X,self.st,self.st,self.build,aM,default=(260,160),mini=(aw,aN),icon=5355,lock=True,owner=False,close_tip="Close Ping History",clear={"c":{},"rows":[]});self.queue=self.wnd.queue
			def start(self):
				a=self.st;a["shutting"]=False;a["minimized"]=Kit.load_min(Y)or J(z);self.wnd.dock(fit=True,min=(560,h(1,D)),show=self.zone_show)
				if Kit.get_var(ag,"0")=="1":self.build()
			def zone_show(self):self.st["minimized"]=self.st["docked"]=False;self.queue.add("open")
			def toggle_open(self):
				a=self.st
				if a["g"]is not None and not(a["minimized"]or a["docked"]):
					if not K(z):self.close()
					return
				a["minimized"]=a["docked"]=False;k(z);Kit.save_min(Y,False);Kit.put_var(ag,"1");self.build()
			def close(self):
				a=self.st
				if a["g"]is None:return
				self.wnd.close();a["docked"]=False;k(z);Kit.put_var(ag,"0")
			def shutdown(self):
				a=self.st;a["shutting"]=True;HOST.dock_remove(z)
				if a["g"]is not None:Kit.save_min(Y,a["minimized"]and not a["docked"]);self.wnd.close()
			def build(self):
				m=self.st;z=i(self.wnd,m,560,h(1,D));w,n=z if z else(560,h(ac,D));s=self.wnd.rows(D,h(0,D),ac)if z else ac;g,e,o=self.wnd.begin(w,n);p=[]
				if not m["minimized"]:
					self.wnd.frame(g);M=Kit.MARGIN;c=w-2*M;a=M+30+Kit.GAP;Kit.add_section(g,M,a,c,36);f=M+12;Kit.art_button(g,e,"clear",Kit.ART_CLOSE,f,a+7,"Clear","Empty the history (pings on screen stay)",on_click=self.queue("clear"));f+=35+Kit.text_w("Clear")+16;Kit.art_button(g,e,"arrow_off",Kit.ART_CLOSE,f,a+7,"Arrow off","Take the tracking arrow down",on_click=self.queue("arrow_off"));j=M+c-8;o["pg"]=Kit.add_label(g,"",j-100,a+10,Kit.HUE_INFO);Kit.art_button(g,e,"pg_up",Kit.ART_RESTORE,j-56,a+8,None,"Previous page (newer pings)",on_click=self.queue(("page",-1)));Kit.art_button(g,e,"pg_dn",Kit.ART_MIN,j-34,a+8,None,"Next page (older pings)",on_click=self.queue(("page",1)));d=a+36+Kit.GAP;Kit.add_section(g,M,d,c,n-d-M);b=M+12;k=[]
					for t,q in aO:Kit.add_label(g,t,b,d+6,Kit.HUE_TITLE);k.append((b,q));b+=q+8
					Kit.add_label(g,"Where",b,d+6,Kit.HUE_TITLE);o["where_w"]=M+c-12-b
					for u in range(s):l=d+30+u*D;r={"val":None,"prev":None,"changed":0.,"tip":None,"vis":True,"sig":None,"labels":[Kit.add_label(g,"",x,l+3,Kit.HUE_TEXT)for x,y in k],"where":Kit.add_label(g,"",b,l+3,Kit.HUE_INFO),"widths":[G for at,G in k]};r["catch"]=Kit.catcher(g,M+6,l,c-12,D,Kit.row_clicker(r,self.queue,"arrow"),ax);p.append(r)
				self.wnd.end(g,{"rows":p});self.drawn=None;self.refresh()
			def tick(self):
				a=self.st
				if a["g"]is not None and Kit.was_clicked(a["store"],"close"):self.close();return
				q=a["queue"]
				while q:
					c=q.pop(0);b=c[0]if isinstance(c,tuple)else c
					if b=="toggle_min":a["minimized"]=not a["minimized"];a["docked"]=False;k(z);Kit.save_min(Y,a["minimized"])
					elif b=="to_bar":HOST.dock_to_bar(z,X)
					elif b=="settings":L("pings")
					elif b=="page":self.page=max(0,self.page+c[1]);self.next_draw=0.
					elif b=="clear":d=self.app.display;del d.history[:];d.hist_ver+=1;self.page=0
					elif b=="arrow_off":self.app.display.arrow_off()
					elif b=="arrow":self.arrow(c[1])
					elif b=="follow":self.follow(c[1])
					if b=="open"or b in("toggle_min","redraw")and a["g"]is not None:self.build()
				if a["g"]is None or(a["minimized"]and a["docked"]):return
				self.refresh()
			def entry(self,seq):return next((d for d in self.app.display.history if d.seq==seq),None)
			def arrow(self,seq):
				a=self.app.display;e=self.entry(seq)
				if e is None:return
				if a.arrow_entry()is e:a.arrow_off();return
				b=a.player()[2]
				if b!=e.map:q("that ping is on %s; you are on %s."%(O(e.map),O(b)));return
				a.arrow_to(e);q("tracking arrow on %s's %s (%d, %d)."%(e.who,s(e.type),e.x,e.y))
			def follow(self,seq):
				e=self.entry(seq)
				if e is None:return
				if e.local:q("that ping is your own.");return
				a=self.mobile_named(e.who)
				if not a:q("%s isn't in range."%e.who);return
				Follow.toggle(a,Q)
			def mobile_named(self,name):
				b=str(name or "").strip().lower()
				if not b:return 0
				c,a=0,None
				for m in API.GetAllMobiles()or():
					if str(m.Name or "").strip().lower()!=b:continue
					d=int(m.Distance)
					if a is None or d<a:c,a=int(m.Serial),d
				return c
			def where_text(self,e,px,py,b):
				a=c(e.x,e.y,"(%d, %d)")
				if b!=e.map or px<=0:return "%s %s"%(O(e.map),a)
				return "%s  %s"%(Kit.where_text(e.x-px,e.y-py,"here"),a)
			def refresh(self):
				f=self.st;a=self.app.display;b=a.history;c=f["c"]
				if f["minimized"]:
					if self.drawn==a.hist_ver:return
					self.drawn=a.hist_ver
					if b:e=b[-1];o="%s: %s, last %s %s"%(X,Kit.count(len(b),"ping"),s(e.type),self.sender(e))
					else:o="%s: no pings yet"%X
					if c.get("status")is not None:Kit.set_text(c["status"],Kit.fit(o,aw-90))
					return
				d=time.time();p=a.arrow_entry();h=(a.hist_ver,self.page,p)
				if h==self.drawn and d<self.next_draw:return
				i=a.player()[:3]if b else(0,0,-1)
				if h==self.drawn and i==self.drawn_pos:self.next_draw=d+1.;return
				self.drawn,self.next_draw,self.drawn_pos=h,d+1.,i;n=len(b);j=max(1,len(f["rows"]));k=max(1,(n+j-1)//j);self.page=max(0,min(k-1,self.page))
				if c.get("pg")is not None:Kit.set_text(c["pg"],("%d/%d"%(self.page+1,k))if k>1 else "")
				w,x,y=i;z=n-1-self.page*j;A=c.get("where_w",200)
				for q,r in enumerate(f["rows"]):
					t=z-q
					if t<0:
						Kit.row_set(r,None,d);r["sig"]=None
						if q==0 and n==0:Kit.set_text(r["labels"][0],aQ,Kit.HUE_INFO);self._show(r,True,only_first=True)
						else:self._show(r,False)
						continue
					e=b[t];Kit.row_set(r,(e.seq,),d);B=C[e.type][1];g=p is e;u=self.where_text(e,w,x,y);v=(e.seq,u,g)
					if v!=r["sig"]:
						r["sig"]=v;D=(time.strftime("%H:%M:%S",time.localtime(e.at)),s(e.type),self.sender(e));E=(Kit.HUE_INFO,B,Kit.HUE_TEXT if not e.local else Kit.HUE_INFO)
						for l,F in enumerate(r["labels"]):Kit.set_text(F,Kit.fit(D[l],r["widths"][l]),E[l])
						Kit.set_text(r["where"],Kit.fit(("> "if g else "")+u,A),Kit.HUE_TITLE if g else Kit.HUE_INFO);m=("Take the tracking arrow down"if g else ax)+(""if e.local else aP)
						if m!=r["tip"]:r["tip"]=m;Kit.with_tip(r["catch"],m)
					self._show(r,True)
			def sender(self,e):
				if e.who=="You"or not Kit.streamer:return e.who
				return Kit.veil("name",e.who,Kit.checksum(e.who.lower().encode("utf-8")))
			def _show(self,r,on,only_first=False):
				a=("first"if only_first else on)
				if r["vis"]==a:return
				r["vis"]=a;b=r["labels"]+[r["where"],r["catch"]]
				for j,c in enumerate(b):Kit.set(c,"IsVisible",on and(not only_first or j==0))
		class PingApp(object):
			def __init__(self):self.mouse=self.gesture=self.guide=self.bridge=self.bridge_error=self.conn=None;self.aim=self.status_label=self.last_pos=None;self.guide_labels,self.recent_pings={},{};self.bridge_tried=self._shut=False;self.next_link_check=self.last_pos_sent=self.next_pos_read=0;self.last_ping_sent=self.last_auto_sent=0;self.recent_order=collections.deque();self.settings=Settings();self.display=PingDisplay();self.pending,self.jobs,self.outbox,self.inbox,self.hooked=[],[],[],[],[];self.status_text,self.status_w="",300;self.history=HistoryWindow(self)
			def set_status(self,text,also_journal=True):
				self.status_text=text
				if self.status_label is not None:Kit.set_text(self.status_label,Kit.fit(text,self.status_w))
				if also_journal:q(B(text))
			def _queue_ping(self,t):
				def a(*a):
					if HOST.typing():return
					self.pending.append(("target",t));HOST.poke()
				return a
			def save_setup(self):
				if self.conn and self.conn.kind=="tazuo":self.set_status("Saved; TazUO's Enhanced Map login is on, so that stays in use.");return
				if self.conn:self.conn.close();self.conn=None
				self.choose_link()
			def apply_options(self):
				if j["gesture"]and self.mouse is None:self.init_mouse()
				elif not j["gesture"]:self.mouse=self.gesture=None;self.close_guide()
				self.jobs.append(("link",))
			def connect(self):
				if self.conn:self.conn.close()
				s=self.settings;self.conn=MapConnection(s.host,s.port,s.user,s.password);self.set_status("Connecting to %s:%d"%(s.host,s.port),also_journal=False)
			def get_bridge(self):
				if not self.bridge_tried:
					self.bridge_tried=True
					try:self.bridge=TazUOBridge()
					except Exception as e:self.bridge=None;self.bridge_error=P(e)
				return self.bridge
			def tazuo_available(self):b=self.get_bridge();return b is not None and bool((b.config()or{}).get("configured"))
			def choose_link(self,announce=True):
				b=(j["connection"]or "auto").lower();a=self.conn.kind if self.conn else None
				if b in("auto","tazuo")and self.tazuo_available():
					if a!="tazuo":
						if self.conn:self.conn.close()
						self.conn=TazUOLink(self.bridge)
					return
				if b=="tazuo":
					if a=="tazuo":return
					if a=="own":self.conn.close();self.conn=None;announce=True
					if announce:
						if self.get_bridge()is None:self.set_status("Can't use TazUO's Enhanced Map connection (%s)."%self.bridge_error)
						else:self.set_status("Turn on Enhanced Map in TazUO's Options (server, port, login).")
					return
				if a=="tazuo":self.conn.close();self.conn=None;a=None
				if a=="own":return
				if self.settings.complete:self.connect()
				elif announce:
					if b=="auto"and self.get_bridge()is not None:self.set_status("Turn on Enhanced Map in TazUO, or enter a map login (World Map settings).")
					else:self.set_status("Enter your map server details to start.");self.inbox.append(("open_setup",))
			def send_ping(self,x,y,m,t):
				a=time.time()
				if a-self.last_ping_sent<aj:return
				self.last_ping_sent=a;self._send(x,y,m,t)
			def send_auto(self,x,y,m,t,who=None):
				a=time.time()
				if a-self.last_auto_sent<aj:return False
				self.last_auto_sent=a;self._send(x,y,m,t,who=who,auto=True);return True
			def _send(self,x,y,m,t,who=None,auto=False):
				self.display.show("You",x,y,m,t,local=True,who=who,auto=auto)
				if self.conn and self.conn.ready:
					if self.conn.server_relays_ping:self.outbox.append(I(51,struct.pack("<HHBB",x&65535,y&65535,m&255,t&255)))
					a=aI(x,y,m,t)
					if a:self.outbox.append(a)
					self.outbox.append(aq(x,y))
				else:b="Not connected: only you can see that ping.";self.set_status(b,also_journal=not auto or self.status_text!=b)
			AIM_SECONDS=10
			def target_ping(self,t):
				q("target a spot for %s (yourself: where you stand)."%s(t));self.aim=None;b=Picker._tm()
				if b is not None:
					a={"t":t,"fired":False,"spot":None,"d":None,"tm":b,"until":time.time()+self.AIM_SECONDS}
					def c(obj,aim=a):aim["spot"]=aL(obj);aim["fired"]=True
					with Kit.quiet:from System import Action;a["d"]=Action[object](c);b.SetTargeting(a["d"],Picker.CURSOR_TARGET,Picker.neutral);self.aim=a;HOST.claim_cursor("pings",self.AIM_SECONDS);return
				self.jobs.append(("aim",t))
			def poll_aim(self):
				a=self.aim
				if a is None:return
				if not a["fired"]:
					b=bool(a["tm"].IsCurrentTargetingAction(a["d"]))
					if b and time.time()<a["until"]:return
					self.aim=None;E("pings")
					if b:a["tm"].CancelTarget()
					return
				self.aim=None;E("pings");self.aimed(a["t"],a["spot"])
			def aimed(self,t,spot):
				if spot is None:return
				x,y=spot
				if x<=0 or y<=0:return
				self.send_ping(x,y,int(API.GetMap()),t)
			def drop_aim(self):
				a,self.aim=self.aim,None;E("pings")
				if a is None or a["fired"]:return
				b=a["tm"]
				def c():
					if b.IsCurrentTargetingAction(a["d"]):b.CancelTarget()
				safe(lambda:Kit.on_client(c,fallback=False))
			def target_ping_blocking(self,t):
				a=API.RequestAnyTarget(10)
				if a is None:return
				try:x,y=int(a.X),int(a.Y)
				except Exception:return
				self.inbox.append(("aimed",t,(x,y)))
			def share_position(self):
				if not self.conn or not self.conn.ready or not self.conn.owns_position:return
				a=time.time()
				if a<self.next_pos_read:return
				self.next_pos_read=a+.5;b=None
				if j["share"]:
					p=API.Player
					try:b=(int(p.X),int(p.Y),int(API.GetMap()))
					except Exception:pass
				if b is None or b[0]<=0:
					if a-self.conn.last_sent>20:self.outbox.append(I(254))
					return
				if((b!=self.last_pos and a-self.last_pos_sent>=1.)or a-self.last_pos_sent>=10):c=(4 if p.IsDead else 1 if p.IsPoisoned else 2 if p.IsYellowHits else 3 if p.IsParalyzed else 5 if p.IsHidden else 0);d=(int(p.Hits),int(p.Stamina),int(p.Mana),int(p.HitsMax),int(p.StaminaMax),int(p.ManaMax));self.outbox.append(aJ(b,d,c,0xFFFFD700));self.last_pos,self.last_pos_sent=b,a
			def handle(self,ev):
				a=ev[0]
				if a=="status":self.set_status(ev[1],also_journal=ev[2])
				elif a=="ping":self.show_once(*ev[1:])
				elif a=="alert":
					d,b,x,y=ev;c=aH(x,y)
					if c:self.show_once(b,*c)
					elif not self.seen_recently(b,x,y):self.show_once(b,x,y,int(API.GetMap()),F)
				elif a=="message":q("map server: "+ev[1])
			DEDUPE_SECONDS=3
			def seen_recently(self,name,x,y,t=None):
				d=time.time();b,a=self.recent_order,self.recent_pings
				while b and d-b[0][0]>self.DEDUPE_SECONDS:
					e,c=b.popleft()
					if a.get(c)==e:del a[c]
				if t is not None:return(name,x,y,t)in a
				for k in a:
					if k[0]==name and k[1]==x and k[2]==y:return True
				return False
			def show_once(self,name,x,y,m,t):
				if self.seen_recently(name,x,y,t):return
				a=time.time();b=(name,x,y,t);self.recent_pings[b]=a;self.recent_order.append((a,b));self.display.show(name,x,y,m,t)
			def step(self):
				while self.pending:
					a=self.pending.pop(0)
					if a[0]=="target":self.target_ping(a[1])
					elif a[0]=="options":self.apply_options()
					elif a[0]=="rehook":self.register_hotkeys()
					elif a[0]=="history":self.history.toggle_open()
					else:self.jobs.append(a)
				c=self.inbox
				if c:self.inbox=[]
				for b in c:
					if b[0]=="open_setup":L("pings")
					elif b[0]=="aimed":self.aimed(b[1],b[2])
					else:self.handle(b)
				self.poll_aim()
				if self.conn:self.share_position()
				self.poll_gesture();self.display.update();self.history.tick()
			def thread_step(self):
				while self.jobs:
					a=self.jobs.pop(0)
					if a[0]=="save_setup":self.save_setup()
					elif a[0]=="link":self.choose_link(announce=False)
					elif a[0]=="aim":self.target_ping_blocking(a[1])
					elif a[0]=="reconnect":
						if self.conn and self.conn.kind=="tazuo":self.conn.reset();self.set_status("Asked TazUO's Enhanced Map to reconnect.")
						elif self.settings.complete and(j["connection"]or "auto").lower()!="tazuo":self.connect();self.conn.reset()
						else:self.choose_link()
				if time.time()>=self.next_link_check:self.next_link_check=time.time()+5;self.choose_link(announce=False)
				b=self.outbox
				if b:self.outbox=[]
				if self.conn:
					for c in b:self.conn.send(c)
					self.inbox.extend(self.conn.poll())
			def init_mouse(self):
				if not j["gesture"]:self.mouse=None;return
				try:self.mouse=TazUOMouse()
				except Exception as e:self.mouse=None;q("mouse-wheel pings unavailable (%s): use the ping buttons or hotkeys."%P(e))
			@staticmethod
			def drag_direction(dx,dy):
				if max(abs(dx),abs(dy))<j["drag"]:return
				if abs(dx)>abs(dy):return "right"if dx>0 else "left"
				return "down"if dy>0 else "up"
			def poll_gesture(self):
				m=self.mouse
				if m is None:return
				a=m.middle_down()
				if a and self.gesture is None:
					b=m.tile_under_mouse();c=m.position(m._mclick);self.gesture={"tile":b,"start":c,"dir":None,"map":int(API.GetMap())}
					if b is not None:self.show_guide(c)
				elif a and self.gesture is not None:
					if self.gesture["tile"]is None:return
					x,y=m.position();d=self.drag_direction(x-self.gesture["start"][0],y-self.gesture["start"][1])
					if d!=self.gesture["dir"]:self.gesture["dir"]=d;self.update_guide(d)
				elif not a and self.gesture is not None:
					g,self.gesture=self.gesture,None;self.close_guide();t=ap.get(g["dir"])
					if g["tile"]is not None and t is not None:self.send_ping(g["tile"][0],g["tile"][1],g["map"],t)
			def show_guide(self,center):
				self.close_guide();w,h=180,104;a=G.CreateGump(False,False);c=Kit.render_scale()or 1.;f,g=int(round(center[0]/c)),int(round(center[1]/c));Kit.place(a,f-w//2,g-h//2,w,h);Kit.add_window_frame(a,w,h,corners=False);Kit.add_section(a,6,6,w-12,h-12)
				for d,(i,j)in(("up",(58,9)),("right",(110,43)),("down",(58,77)),("left",(11,43))):t=ap[d];b=G.CreateGumpLabel(s(t),Kit.HUE_INFO);b.SetRect(i,j,70,18);a.Add(b);self.guide_labels[d]=(b,t)
				e=G.CreateGumpLabel("+",Kit.HUE_TITLE);e.SetRect(w//2-3,h//2-9,10,18);a.Add(e);Kit.add_front(a);SNAP.skip_gump(a);self.guide=a
			def update_guide(self,a):
				for d,(b,t)in self.guide_labels.items():b.Text="["+s(t)+"]"if d==a else s(t);b.Hue=C[t][1]if d==a else 946
			def close_guide(self):Kit.dispose(self.guide);self.guide,self.guide_labels=None,{}
			def register_hotkeys(self):
				self.unregister_hotkeys()
				for c,a in u.items():
					if a:
						t=af[c];d="%s ping"%s(t);b=HOST.hotkey_on(a,Q,self._queue_ping(t),d)
						if b is False:q("couldn't set the %s hotkey (%s isn't a key)."%(s(t),a),Kit.HUE_BAD)
						if b is not False:self.hooked.append(a)
			def unregister_hotkeys(self):
				for a in self.hooked:HOST.hotkey_off(a,Q)
				self.hooked=[]
			def shutdown(self):
				if self._shut:return
				self._shut=True;self.unregister_hotkeys();self.drop_aim();self.close_guide();safe(self.history.shutdown);safe(self.display.clear)
				if self.conn:self.conn.close()
			def start(self):self.init_mouse();self.register_hotkeys();self.history.start();self.choose_link();self.next_link_check=time.time()+5
		def Z(action):
			if l["app"]is not None:l["app"].pending.append(action)
		a={"f":None};az,aA,aR=116,160,70;aS="Send a %s ping on the spot, item or person you target";aT="Key for a %s ping, like CTRL+1, F9 or SHIFT+F2 (blank = none)";aU={"host":"Map server address (host name or IP)","port":"Map server port (default %d)"%aa,"user":"Your map server login name","pass":"Map server password; saved in plain text on this PC, like Enhanced Map's"}
		def ah(action):
			def a(*a):Z(action)
			return a
		def aV(f,x,y):
			g,c,w=f.g,f.store,f.w;e=x+12
			for t in(F,N,R,S):h,m=C[t][:2];i=h+"...";Kit.art_button(g,c,"ping%d"%t,Kit.ART_PLAY,e,y+28,i,aS%h,hue=m,on_click=ah(("target",t)));e+=35+Kit.text_w(i)+16
			Kit.art_button(g,c,"recon",Kit.ART_PLAY,x+12,y+58,"Reconnect","Reconnect to the map server",on_click=ah(("reconnect",)));j=x+12+35+Kit.text_w("Reconnect")+16;Kit.art_button(g,c,"history",Kit.ART_PAGE,j,y+58,"History","Open or close the window of recent pings, yours and others'",on_click=ah(("history",)));k=j+35+Kit.text_w("History")+16;b=l["app"]
			if b is not None:Kit.add_label(g,Kit.fit("Wheel drag: up Look, right Danger, down Go, left Help",x+w-12-k),k,y+61,Kit.HUE_INFO)
			d=Kit.add_label(g,"",x+12,y+90,Kit.HUE_INFO);a["status"]=d
			if b is not None:b.status_label,b.status_w=d,w-24;Kit.set_text(d,Kit.fit(b.status_text or "Starting",w-24))
		def aW(f,x,y):
			g,w=f.g,f.w;b=Settings();d=(w-36)//2;a["fields"]=j={}
			for i,(c,k,l)in enumerate((("host","Server address:",b.host),("port","Port:",str(b.port)),("user","Map username:",b.user),("pass","Map password:",b.password))):e=x+12+(i%2)*(d+12);h=y+30+(i//2)*48;Kit.add_label(g,k,e,h);j[c]=Kit.with_tip(Kit.add_textbox(g,l,e+2,h+20,d-8,numbers=c=="port"),aU[c])
			Kit.art_button(g,f.store,"save",Kit.ART_OK,x+12,y+128,"Save and connect","Save the four fields on this PC and connect");a["login"]=Kit.add_label(g,Kit.fit("Saved on this PC in plain text (password shows while typing).",w-236),x+220,y+131,Kit.HUE_INFO)
		def aX(f,x,y):
			b=x+12;a["keys"]=d={}
			for k in ai:c=k.capitalize()+":";Kit.add_label(f.g,c,b,y+36);d[k]=Kit.with_tip(Kit.add_textbox(f.g,u[k],b+Kit.text_w(c)+8,y+33,84,numbers=False),aT%s(af[k]));b+=Kit.text_w(c)+8+84+16
		aB={"lgap":8,"fw":44,"ugap":6};aC=(("SEND A PING  (or a hotkey or wheel drag)",(("custom",0,aV),),{"sh":az,"top":0}),("MAP LOGIN  (when TazUO's Enhanced Map is off)",(("custom",0,aW),),{"sh":aA,"top":0}),("OPTIONS",(("check","sounds","Play a sound for each ping","For your pings and others'",{"stay":True}),("check","gesture","Ping with a mouse-wheel drag","Hold the wheel on a spot and drag: up Look here, right Danger!, down Go here, left Need help",{"dx":312}),("check","share","Show me on guildmates' maps","Sends your position (map login only; TazUO's Enhanced Map does its own)",{"stay":True}),("gap",28),("num","ping_secs","Ping stays:","How long a ping's marker and pulse stay","s",H["ping_secs"][0],H["ping_secs"][1],dict(aB,stay=True)),("num","drag","Drag distance:","Pixels the wheel drag must move to count","px",H["drag"][0],H["drag"][1],dict(aB,dx=312))),{"top":32}),("HOTKEYS  (blank = none)",(("custom",0,aX),),{"sh":aR,"top":0}))
		def aY(w):return aC
		aZ=Kit.Page(j,aY,U)
		def a_(g,x,y,w):f=Kit.Form(g,x,y,w,j,aC);c=y+az+aA+2*Kit.GAP;Kit.add_label(g,"Connection:",x+312,c+60);d=ae.index(j["connection"])if j["connection"]in ae else 0;b=G.CreateDropDown(190,[e[1]for e in T],d);b.SetPos(x+414,c+56);g.Add(b);Kit.with_tip(b,"TazUO's Enhanced Map while it is on, or the login above");a.update({"f":f,"dd":b,"seen_keys":dict(u),"next_read":0.})
		def aD(force=False):
			f=a["f"]
			if f is None:return
			if Kit.was_clicked(f.store,"save"):a0()
			c=time.time()
			if not force and c<a["next_read"]:return
			a["next_read"]=c+.2;b=f.read();i=Kit.dd_index(a["dd"],-1)
			if 0<=i<len(T):b["connection"]=T[i][0]
			if b!=j:j.update(b);U();Z(("options",))
			b={}
			for k,d in a["keys"].items():
				try:b[k]=_norm_key(d.Text)
				except Exception:b[k]=_norm_key(u[k])
			if force and b!=a["seen_keys"]:a["typed"]=a["seen_keys"]=b;u.update(b);U();Z(("rehook",))
			elif b!=a.get("typed"):a["typed"],a["stable"]=b,0
			elif b!=a["seen_keys"]:
				a["stable"]=a.get("stable",0)+1
				if force or a["stable"]>=5:a["seen_keys"]=b;u.update(b);U();Z(("rehook",))
		def a0():
			f=a["fields"]
			try:d=f["host"].Text.strip();i=f["port"].Text.strip();e=f["user"].Text.strip();g=f["pass"].Text
			except Exception:return
			try:c=int(i)
			except ValueError:c=0
			if not d or not e or not g or not(0<c<65536):Kit.set_text(a["login"],"Fill in all four fields (the port is a number)",Kit.HUE_BAD);return
			b=Settings();b.host,b.port,b.user,b.password=d,c,e,g;b.save();Kit.set_text(a["login"],"Saved",Kit.HUE_GOOD);h=l["app"]
			if h is not None:s=h.settings;s.host,s.port,s.user,s.password=d,c,e,g;h.pending.append(("save_setup",))
		def a1():
			aD(True);b=l["app"]
			if b is not None and b.status_label is a.get("status"):b.status_label=None
			a.update({"f":None,"dd":None,"status":None,"keys":None,"fields":None,"login":None})
		def a2(x,y,m=None,kind="danger",who=None):
			a=l["app"]
			if a is None or a._shut:return False
			if m is None:m=API.GetMap()
			return a.send_auto(int(x),int(y),int(m),af.get(kind,N),who)
		aF()
		def a3():l["app"]=PingApp();l["app"].start();ao.service("pings.send",a2)
		def a4():
			if l["app"]is not None:l["app"].step()
		def a5():
			if l["app"]is not None:l["app"].thread_step()
		def a6():
			a=l["app"]
			if a is None:return.05
			if a.gesture is not None:return.02
			if a.aim is not None or a.pending or a.inbox or a.jobs or a.outbox:return.05
			return.1
		def a7():
			ao.close();a,l["app"]=l["app"],None
			if a is not None:a.shutdown()
		return{"start":a3,"tick":a4,"stop":a7,"client_tick":True,"config_height":aZ.height,"build_config":a_,"poll_config":aD,"config_closed":a1,"thread_tick":a5,"interval":a6}
	def ae():
		F="corpserun";r="Corpse";P="CorpseRun_settings";ao="CorpseRun_pos";Q="CorpseRun_min";G="CorpseRun_corpse";s=0x434F5250;ap=8198;R,S=3786,3794;T=15;U=45;x,y=1,120;V=60;X=120.;Y="corpserun.decay";Z=20.;aq=(400,401,605,606,666,667);aa=24;ab=1.;H=2;ar=.25;at=10.;t=.7;ac=2;ad=250;au=("must wait to perform another action",);av,aw=8251,8269;ae=15.;W=420;af,ax=280,46;ay=128;I=Kit.MARGIN+30+Kit.GAP+ay+Kit.MARGIN;e={"arrow":True,"restore":True,"ping":False,"decay":T,"bones":U};a4=dict(e);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"body":0,"body_at":0.,"note_until":0.,"name":"","drawn":None,"drawn_c":None,"unnamed":False,"hooked":False,"find_at":0.};u={"g":None,"c":{},"store":({},{})};J={};ag,K,h=Kit.basics(a,r);ah={"decay":(x,y),"bones":(x,y)}
		def az():
			Kit.kv_load(P,";",e,ah)
			if(e["decay"],e["bones"])==(7,7):e["decay"],e["bones"]=T,U
		def ai():Kit.kv_save(P,";",e,("arrow","restore","ping","decay","bones"),ah)
		def aA():
			p=Kit.get_var(G).split("|")
			if len(p)<8 or p[0]!="1":return
			try:return{"serial":int(p[1]),"x":int(p[2]),"y":int(p[3]),"facet":int(p[4]),"died":float(p[5]),"body":int(p[6]),"spot":p[7]=="1","exact":len(p)<9 or p[8]!="0","name":p[9]if len(p)>9 else ""}
			except ValueError:return
		def o():
			r=a["rec"]
			if r is None:Kit.put_var(G,"");return
			Kit.put_var(G,"1|%d|%d|%d|%d|%.0f|%d|%d|%d|%s"%(r["serial"],r["x"],r["y"],r["facet"],r["died"],r["body"],1 if r["spot"]else 0,1 if r["exact"]else 0,r["name"].replace("|","")))
		def g(text,secs=6.,spot=None):a["note"]=text if spot is None else text.replace("%d, %d"%spot,c(*spot));a["note_until"]=time.time()+secs;a["lbl_at"]=0.;h(B(text))
		def A(now):
			r=a["rec"]
			if r is None:return 0.
			if r["died"]>now:r["died"]=now
			return 60.*(e["decay"]+e["bones"])-(now-r["died"])
		def E(secs):secs=max(0,int(secs));return "%d:%02d"%(secs//60,secs%60)
		m=Kit.find_item;aj=Kit.held_item
		def ak():return bool(HOST.cursor_busy(F))or bool(API.HasTarget())
		def aB(it):
			if av<=int(it.Graphic)<=aw:return True
			d=it.GetItemData();return d is not None and int(d.Layer)in(11,16)
		def aC(it):
			d=it.GetItemData();w=int(d.Weight)if d is not None else 0;a=(0 if w>=255 else w)*max(1,int(it.Amount or 1))
			if it.IsContainer:
				for x in API.ItemsInContainer(int(it.Serial),True)or():
					d=x.GetItemData();b=int(d.Weight)if d is not None else 0
					if b<255:a+=b*max(1,int(x.Amount or 1))
			return a
		def L():
			z=i(n,a,W,I);w,h=z if z else(W,I);g,e,d=n.begin(w,h)
			if not a["minimized"]:n.frame(g);M=Kit.MARGIN;j=w-2*M;b=M+30+Kit.GAP;Kit.add_section(g,M,b,j,h-b-M,"YOUR CORPSE  (where, how long it lasts)");d["where"]=Kit.add_label(g,"",M+12,b+28,Kit.HUE_TEXT);d["decay"]=Kit.add_label(g,"",M+12,b+48,Kit.HUE_INFO);d["info"]=Kit.add_label(g,"",M+12,b+68,Kit.HUE_INFO);f=b+92;c=M+10;d["go"]=Kit.art_button(g,e,"go",Kit.ART_PLAY,c,f,"Get my things","Move your things from your corpse to your backpack one by one (stand beside it; click again to stop)",on_click=K("go"));c+=35+max(Kit.text_w("Get my things"),Kit.text_w("Stop"))+14;Kit.art_button(g,e,"help",Kit.ART_PLAY,c,f,"Ping for help","Send your guild a Need help ping on your corpse (needs World Map > Map Pings)",on_click=K("help"));c+=35+Kit.text_w("Ping for help")+14;Kit.art_button(g,e,"forget",Kit.ART_CLOSE,c,f,"Forget","Forget this corpse and take its arrow down",on_click=K("forget"))
			n.end(g);a["lbl_at"]=0.
		n=Kit.Window(F,r,a,u,L,ao,Q,(220,220),(af,ax),3786,ag,lock=True,clear={"c":{}})
		def aD():
			if not a["minimized"]and not a["docked"]:return
			a["minimized"],a["docked"]=False,False;k(F);Kit.save_min(Q,False);L()
		def aE(me,now,o):
			b=a["rec"];j=a["job"]
			if b is None:p=bool(a["was_dead"]);d=a["note"]if a["note"]and now<a["note_until"]else("Find a healer or a resurrection."if p else "When you die, this window shows the way back.");return("No corpse to find.",Kit.HUE_TEXT,"",Kit.HUE_INFO,d,r+": none")
			f=A(now);q,s=int(me.X),int(me.Y)
			if not b["spot"]:h,g="Looking for your corpse round you","looking"
			elif o!=b["facet"]:h="On %s, at %s"%(Kit.facet_name(b["facet"]),c(b["x"],b["y"]));g=Kit.facet_name(b["facet"])
			else:i=Kit.where_text(b["x"]-q,b["y"]-s);h="%s%s, at %s"%(i[0].upper(),i[1:],c(b["x"],b["y"]));g=i
			n=60.*e["bones"];k=""if b["exact"]else "at most "
			if f>n:l="Bones in %s%s, gone in %s%s"%(k,E(f-n),k,E(f))
			elif f>0:l=("Bones %s; gone in %s%s"%("now"if b["exact"]else "soon",k,E(f)))
			else:l="Should have decayed by now"
			t=Kit.HUE_BAD if f<=V else Kit.HUE_INFO
			if a["note"]and now<a["note_until"]:d=a["note"]
			elif j is not None:
				if j["phase"]=="open":d="Opening your corpse"
				else:d="Moving %d / %d"%(min(j["i"],len(j["plan"])),len(j["plan"]))
			else:
				m=(("Died %s ago."%Kit.ago(now-b["died"]))if b["exact"]else "Found as a ghost.")
				if not b["serial"]and a["unnamed"]:d="Waiting for the corpse's name: click it once."
				elif a["was_dead"]:d=m+" Be resurrected, then click Get my things."
				elif b["serial"]and b["spot"]:d=m+" Stand by it and click Get my things."
				else:d=m+" Not seen there yet."
			g="%s  %s"%(g,E(f))if f>0 else g;return h,Kit.HUE_TEXT,l,t,d,"%s: %s"%(r,g)
		def aF(me,now,l,force=False):
			m=u["g"]
			if m is None or(a["minimized"]and a["docked"]):return
			if not force and now<a["lbl_at"]:return
			a["lbl_at"]=now+.5;d,e,f,g,h,i=aE(me,now,l);c=u["c"]
			if a["minimized"]:j=Kit.HUE_BAD if a["rec"]is not None and A(now)<=V else Kit.HUE_INFO;b=(i,j)
			else:b=(d,e,f,g,h,a["job"]is not None)
			if b==a["drawn"]and c is a["drawn_c"]:return
			a["drawn"],a["drawn_c"]=b,c
			if a["minimized"]:
				k=c.get("status")
				if k is not None:Kit.set_text(k,Kit.fit(i,af-90),j)
				return
			for n,o,p in(("where",d,e),("decay",f,g),("info",h,Kit.HUE_INFO)):Kit.set_text(c[n],Kit.fit(o,W-2*Kit.MARGIN-24),p)
			Kit.set_text(c["go"],"Stop"if a["job"]is not None else "Get my things",Kit.HUE_TITLE if a["job"]is not None else Kit.HUE_TEXT)
		def aG(me,c):
			r=a["rec"];b=None
			if e["arrow"]and r is not None and r["spot"]and c==r["facet"]:
				if max(abs(int(me.X)-r["x"]),abs(int(me.Y)-r["y"]))>H:b=(r["x"],r["y"])
			if b==a["arrow"]:return
			if b is None:Kit.drop_arrow(a,s)
			else:API.TrackingArrow(b[0],b[1],s);a["arrow"]=b
		def M(me,now,at_start=False):
			if a["job"]is not None:l("you died")
			x,y,m=int(me.X),int(me.Y),int(API.GetMap());a["name"]=str(me.Name or "");a["rec"]={"serial":0,"x":x,"y":y,"facet":m,"died":now,"body":a["body"],"spot":not at_start,"exact":not at_start,"name":a["name"]};a["seek_until"],a["seek_at"]=now+Z,now;a["gone_since"],a["warned"],a["unnamed"]=None,False,False;a["refused"]=set();o()
			if at_start:h("you are a ghost: looking for your corpse round you.")
			else:
				h("you died at %d, %d (%s). Bones in %s, gone %s later."%(x,y,Kit.facet_name(m),Kit.count(e["decay"],"minute"),Kit.count(e["bones"],"minute")),Kit.HUE_BAD)
				if e["ping"]:a["ping"]=(x,y,m,now+ae)
			if e["restore"]:aD()
		aH=("a corpse of ","corpse of ","the remains of ","remains of ")
		def N():r=a["rec"];return((r["name"]if r is not None and r["name"]else a["name"])or "").strip().lower()
		def al(it,graphic,e):
			r=a["rec"];d=r["body"]if r is not None else 0;b=int(it.Amount or 0)
			if d and b and b!=d:return 0
			f=R<=graphic<=S
			if f and(not b or(not d and b not in aq)):return 0
			n=(str(it.Name or "")or str(it.NameAndProps(False)or "")).strip().lower();c=None
			for p in aH:
				if n.startswith(p):c=n[len(p):].strip();break
			if c is None:
				if not n or n in("corpse","a corpse","bones","remains")or f:return 1
				c=n
			if not e:return 1
			return 2 if c==e else 0
		def am(items,g,h,lim,c,i):
			for a,j in items:
				s,e,f=int(a.Serial),int(a.X),int(a.Y);d=max(abs(e-g),abs(f-h))
				if d>lim:continue
				m=al(a,j,i)
				if m==1:c[1]=True
				if m!=2:continue
				k=(d,s,e,f);b=c[0]
				if b is None or d<b[0]or(d==b[0]and s>b[1]):c[0]=k
		def aI(me):
			r=a["rec"];d=N();e,f,h=(r["x"],r["y"],3)if r["spot"]else(int(me.X),int(me.Y),aa);b=[None,False];i,j=[],[]
			for c in API.GetItemsOnGround(aa)or():
				g=int(c.Graphic)
				if g==ap:i.append((c,g))
				elif R<=g<=S:j.append((c,g))
			am(i,e,f,h,b,d)
			if b[0]is None:am(j,e,f,h,b,d)
			return(None if b[0]is None else b[0][1:]),b[1]
		def p(why=None):
			if a["job"]is not None:l(None)
			a["rec"]=a["ping"]=a["gone_since"]=None;a["unnamed"]=False;a["refused"]=set();Kit.drop_arrow(a,s);o()
			if why:h(why)
			a["lbl_at"]=0.
		def aJ(me,now,d):
			b=a["rec"];e=A(now);i=max(abs(int(me.X)-b["x"]),abs(int(me.Y)-b["y"]))
			if not b["serial"]:
				n=b["spot"]and d==b["facet"]and i<=12;q=not b["spot"]and a["unnamed"];j=now<a["seek_until"]
				if(j and now>=a["seek_at"])or(not j and(n or q)and now>=a["look_at"]):
					a["seek_at"]=now+.5;a["look_at"]=now+1.;a["find_at"]=now;k,l=aI(me)
					if k is not None:
						b["serial"],b["x"],b["y"]=k;a["unnamed"]=False
						if not b["name"]:b["name"]=N()
						if not b["spot"]:b["spot"]=True;h("found your corpse at %d, %d."%(b["x"],b["y"]))
						o();a["lbl_at"]=0.
					elif l!=a["unnamed"]:a["unnamed"]=l;a["lbl_at"]=0.
				if(not b["serial"]and not b["spot"]and now>=a["seek_until"]and not a["unnamed"]):p("your corpse isn't in view (it was left before %s started)."%r);return
			elif now>=a["item_at"]or a["item_at"]-now>ab:
				a["item_at"]=now+ab;c=m(b["serial"])
				if c is not None:
					a["gone_since"]=None;f,g=int(c.X),int(c.Y)
					if(f or g)and(f,g)!=(b["x"],b["y"])and not int(c.Container or 0):b["x"],b["y"]=f,g;o()
				elif d==b["facet"]and a["job"]is None and i<=12:
					if a["gone_since"]is None:a["gone_since"]=now
					elif now-a["gone_since"]>=6.:p("your corpse isn't at %d, %d any more (decayed or looted)."%(b["x"],b["y"]));return
				else:a["gone_since"]=None
			if e<=60 and not a["warned"]and e>0:a["warned"]=True;s=Kit.where_text(b["x"]-int(me.X),b["y"]-int(me.Y))if d==b["facet"]else "on "+Kit.facet_name(b["facet"]);C(Y,"Corpse decays in under a minute (%s)"%s,"warn")
			if e<=-X and m(b["serial"])is None:p("your corpse has decayed.")
		def aK(now):
			p=a["ping"]
			if p is None:return
			x,y,m,c=p;b=HOST.services.get("pings.send")
			if b is None or now>c:
				a["ping"]=None
				if b is None:h("World Map > Map Pings is off, so no Need help ping was sent.")
				return
			try:
				if b(x,y,m=m,kind="help"):a["ping"]=None;h("Need help ping sent on your corpse.")
			except Exception:a["ping"]=None
		def aL(me,now):
			r=a["rec"]
			if a["job"]is not None:return
			if r is None:g("No corpse remembered.");return
			if bool(a["was_dead"]):g("You are still a ghost: get resurrected first.");return
			c=(r["x"],r["y"])
			if not r["serial"]:g("Your corpse hasn't been seen yet: go to %d, %d."%c,spot=c);return
			b=m(r["serial"])
			if b is None:g("Your corpse isn't in view yet (%d, %d)."%c,spot=c);return
			d=al(b,int(b.Graphic),N())
			if d==1:g("Waiting for the corpse's name: click it once.");return
			if d!=2:g("That corpse isn't yours.");return
			e,f=int(b.X)-int(me.X),int(b.Y)-int(me.Y)
			if max(abs(e),abs(f))>H:g("Walk up to your corpse first (%s)."%Kit.where_text(e,f));return
			h=int(API.Backpack or 0)
			if not h:g("No backpack to put things in.");return
			if ak():g("A target cursor is up: finish or cancel it first.");return
			if aj():g("You are holding an item: put it down first.");return
			a["job"]={"phase":"open","corpse":r["serial"],"pack":h,"at":now+1.,"until":now+3.,"plan":[],"i":0,"tried":set(),"waits":{},"move":None,"check":None,"sent_at":0.,"last":0,"rechecks":0,"hold":0.,"moved":0,"refused":0,"streak":0,"why":None,"replans":0};API.UseObject(r["serial"]);a["note"]="";a["lbl_at"]=0.
		def O(j):
			b=[]
			for c in API.ItemsInContainer(j["corpse"],False)or():
				if len(b)>=ad:break
				s=int(c.Serial)
				if s not in j["tried"]and s not in a["refused"]and not aB(c):b.append(s)
			return b
		def aM(me,now):
			j=a["job"]
			if j["why"]:l(j["why"]);return
			if j["move"]is not None:return
			if a["was_dead"]:l("you died");return
			d=m(j["corpse"])
			if d is None:l("your corpse is gone from view");return
			if max(abs(int(d.X)-int(me.X)),abs(int(d.Y)-int(me.Y)))>H:l("you walked away from your corpse");return
			if j["check"]is not None and(now<j["at"]or not aN(j,now)):return
			if j["phase"]=="open":
				if now<j["at"]:return
				b=O(j)
				if not b and now<j["until"]:return
				j["plan"],j["i"],j["phase"]=b,0,"move"
				if not b:an();return
			if now<j["hold"]:return
			if ak():l("a target cursor is up");return
			h=aj()
			if h and h!=j["last"]:l("you picked something up");return
			b=j["plan"]
			while j["i"]<len(b):
				s=b[j["i"]];j["i"]+=1
				if s in j["tried"]:continue
				x=m(s)
				if x is None or int(x.Container or 0)!=j["corpse"]:continue
				c,e=int(me.WeightMax or 0),int(me.Weight or 0)
				if c>0 and(e>=c or e+aC(x)>c):l("the next item would put you over your weight limit (%d / %d stones)"%(e,c));return
				j["tried"].add(s);j["move"]=s;return
			if j["replans"]<2:
				j["replans"]+=1;f=O(j)
				if f:j["plan"],j["i"]=f,0;return
			an()
		def aN(j,now):
			s=j["check"];b=m(s);c=int(b.Container or 0)if b is not None else None
			if c is None and j["rechecks"]<ac:j["rechecks"]+=1;j["at"]=now+t*.5;return False
			if c!=j["corpse"]:j["moved"]+=1;j["streak"]=j["rechecks"]=0;j["check"]=None;return True
			if(Journal.find(j["sent_at"],au)is not None and j["waits"].get(s,0)<2):j["waits"][s]=j["waits"].get(s,0)+1;j["tried"].discard(s);j["i"]=max(0,j["i"]-1);j["check"]=None;j["rechecks"]=0;j["hold"]=now+t;return False
			if j["rechecks"]<ac:j["rechecks"]+=1;j["at"]=now+t*.5;return False
			j["check"]=None;j["rechecks"]=0;j["refused"]+=1;j["streak"]+=1
			if len(a["refused"])<ad:a["refused"].add(s)
			if j["streak"]>=3:l("%d moves in a row were refused"%j["streak"]);return False
			return True
		def aO():
			j=a["job"]
			if j is None or j["move"]is None or a["shutting"]:return
			b=j["move"];j["move"]=None
			try:API.MoveItem(b,j["pack"])
			except Exception as c:j["why"]="a move failed (%s)"%c;return
			j["check"]=b;j["last"]=b;j["sent_at"]=time.time();j["at"]=j["sent_at"]+t
		def an():
			j,a["job"]=a["job"],None
			if j is None:return
			b=[]
			if m(j["corpse"])is not None:b=O({"corpse":j["corpse"],"tried":set()})
			c=len(a["refused"])
			if j["moved"]==0 and not j["refused"]and not b:p("nothing left in your corpse%s."%((" but %s the server refused (take %s by hand)"%(Kit.count(c,"item"),"it"if c==1 else "them"))if c else ""));return
			d="%s back in your backpack"%Kit.count(j["moved"],"item")
			if j["refused"]:d+=", %d refused (left in your corpse: take %s by hand)"%(j["refused"],"it"if j["refused"]==1 else "them")
			if b:h("%s; %d still in your corpse (click Get my things again)."%(d,len(b)),Kit.HUE_BAD if j["refused"]else Kit.HUE_INFO);a["lbl_at"]=0.;return
			p(None);h("%s. Re-dress when you are ready."%d,Kit.HUE_BAD if j["refused"]else Kit.HUE_GOOD)
		def l(why=None,user=False):
			j,a["job"]=a["job"],None
			if j is None:return
			if user:h("stopped (%d moved)."%j["moved"])
			elif why:h("stopped: %s (%d moved)."%(why,j["moved"]),Kit.HUE_BAD)
			a["lbl_at"]=0.
		def aP(me,now):
			if a["job"]is not None:l(None,user=True)
			elif me is not None:aL(me,now)
		def aQ(me,now):
			r=a["rec"]
			if r is None or not r["spot"]:g("No corpse to ping.")
			elif HOST.services.get("pings.send")is None:g("World Map > Map Pings is off: turn it on to send pings.")
			else:a["ping"]=(r["x"],r["y"],r["facet"],now+ae)
		def aR(me,now):
			if a["rec"]is None:g("No corpse remembered.")
			else:p("forgot your corpse.")
		aS={"go":aP,"help":aQ,"forget":aR};aT=("One item every %.1f s; stops on Stop, a target cursor, picking something up, walking away or going over your weight limit."%t)
		def aU(w):a="Corpse to bones:";return(("WHEN YOU DIE",(("check","arrow","Point the tracking arrow at your corpse","Its own arrow (others are left alone); hidden when you stand beside it"),("check","restore","Open the Corpse window when you die, even minimized or folded","It comes back full size"),("check","ping","Send a Need help map ping on your corpse when you die","Your guild sees where you died (needs World Map > Map Pings); off at first, as it shows where you are")),{"pad":4}),("DECAY  (minutes; the shard's times)",(("num","decay",a,"Minutes from death until bones",None,x,y,{"stay":True}),("num","bones","Bones gone after:","Minutes the bones (with your things) last",None,x,y,{"dx":Kit.text_w(a)+86})),{"ldy":4,"fw":40,"pad":8}),("GET MY THINGS  (one item at a time)",[("note",d)for d in Kit.wrap(aT,w-28)]),z("corpse"))
		def aV(f,new):
			b=time.time()
			for k in("decay","bones"):
				try:a=str(f.c[k].Text or "").strip()
				except Exception:continue
				t=J.get(k)
				if t is None or t[0]!=a:J[k]=(a,b)
				if not v.force and(t is None or t[0]!=a or b-t[1]<1.):new[k]=e[k]
		def aW(old,new):
			if(new["decay"],new["bones"])!=(old["decay"],old["bones"]):a["warned"]=False
			a["lbl_at"]=0.
			if not new["arrow"]:Kit.drop_arrow(a,s)
		v=Kit.Page(e,aU,ai,aW,adjust=aV,final=True)
		def aX():v.closed();J.clear()
		def aY(*c):
			r=a["rec"]
			if r is None or r["serial"]or a["shutting"]:return
			b=a["find_at"]+ar;a["seek_at"]=min(a["seek_at"],b);a["look_at"]=min(a["look_at"],b)
		def aZ(*b):
			if a["shutting"]:return
			a["died"]=True;HOST.poke("worldmap.corpse",False)
		def a_(d):
			for k in("body_at","seek_until","seek_at","look_at","item_at","lbl_at","note_until","find_at","died_at"):a[k]=a[k]+d
			if a["gone_since"]is not None:a["gone_since"]+=d
			p=a["ping"]
			if p is not None:a["ping"]=(p[0],p[1],p[2],p[3]+d)
			j=a["job"]
			if j is not None:
				for k in("at","until","sent_at","hold"):j[k]+=d
			r=a["rec"]
			if r is not None:r["died"]+=d;o()
		def a0():
			a.update({"shutting":False,"docked":False,"queue":[],"job":None,"arrow":None,"refused":set(),"ping":None,"was_dead":None,"seek_until":0.,"seek_at":0.,"look_at":0.,"gone_since":None,"item_at":0.,"lbl_at":0.,"note":"","last_now":None,"atlas":False,"unnamed":False,"died":False,"died_at":0.,"minimized":n.start_min()});az();a["rec"]=aA();a["warned"]=False
			if a["rec"]is not None and A(time.time())<=-X:a["rec"]=None;o()
			if a["rec"]is not None and not a["rec"]["spot"]:a["seek_until"]=time.time()+Z
			D(Y,"Corpse about to decay",490);L();n.dock(fit=True,min=(W,I));Kit.hook_once(a,"hooked",("OnCorpseCreated",aY),("OnPlayerDeath",aZ))
		def a1():
			if u["g"]is None:return
			if Kit.closed(u):return
			c=time.time();i,a["last_now"]=a["last_now"],c
			if i is not None and c<i-2.:a_(c-i)
			d=HOST.me()
			while a["queue"]:
				k=a["queue"].pop(0)
				if not n.action(k):aS[k](d,c)
			if d is None:return
			e=bool(d.IsDead);g=a["was_dead"];a["was_dead"]=e;l=a["died"];a["died"]=False
			if l and not g:M(d,c);a["died_at"]=0. if e else c
			elif g is None:
				if e and a["rec"]is None:M(d,c,at_start=True)
			elif e and not g:
				if not 0.<=c-a["died_at"]<=at:M(d,c)
				a["died_at"]=0.
			elif g and not e and a["rec"]is not None:
				r=a["rec"]
				if r["spot"]:h("you are alive. Your corpse is %s: click Get my things beside it."%Kit.where_text(r["x"]-int(d.X),r["y"]-int(d.Y)),Kit.HUE_GOOD)
				a["lbl_at"]=0.
			if not e and c>=a["body_at"]:a["body_at"]=c+2.;a["body"]=int(d.Graphic);a["name"]=str(d.Name or "")or a["name"]
			if not a["name"]:a["name"]=str(d.Name or "")
			j=int(API.GetMap())if a["rec"]is not None or a["arrow"]is not None else None
			if a["rec"]is not None:aJ(d,c,j)
			if a["job"]is not None:aM(d,c);aO()
			if a["ping"]is not None:aK(c)
			if a["rec"]is not None or a["arrow"]is not None:aG(d,j)
			r=a["rec"];f=(r["x"],r["y"],r["facet"])if r is not None and r["spot"]else None
			if f!=a["atlas"]:a["atlas"]=f;b.set("corpse",{}if f is None else{q("Your corpse"):(f[0],f[1],f[2],"white")})
			aF(d,c,j)
		def a2():return.1 if a["job"]is not None else.25
		def a3():a["shutting"]=True;a["job"]=a["ping"]=None;Kit.drop_arrow(a,s);ai();ag.close()
		return{"start":a0,"tick":a1,"stop":a3,"client_tick":True,"config_height":v.height,"build_config":v.build,"poll_config":v.poll,"config_closed":aX,"interval":a2}
	def af():
		V="treasure";G="Treasure Maps";W="TreasureHunter_settings";ay="TreasureHunter_pos";az="TreasureHunter_min";X="TreasureHunter_maps";Y,aA=320,46;N=8;o=24;Z=0x54524541;O=(5355,5356);aa=("youthful","plainly","expertly","adeptly","cleverly","deviously","ingeniously");ab=["Youthful"]+[bi.capitalize()+" drawn"for bi in aa[1:]];aB=["somewhere in "+bj.lower()for bj in Kit.FACETS];aC="you successfully decode a treasure map";aD="the treasure is marked by the red pin";aE="this treasure hunt has already been completed";aF=re.compile(r"believe this is somewhere near (\d+) and (\d+)");P=300.;ac=1.;D=6.;ad=.25;H=8.;ae=5.;af=60;ag=6.;ah=.5;E="Point the tracking arrow at this map's spot (again: back to the nearest map)";aG="Send the tracking arrow back to the nearest map's spot";aH="Point the tracking arrow at this map's spot (again: take it down)";aI="Send a Go here ping on this map's spot (needs World Map > Map Pings)";aJ="No treasure maps in your pack: put one in and double-click it once.";ai="This treasure has been dug up";m={"auto":True,"undecoded":True,"done":False};bh=dict(m);d={"minimized":False,"shutting":False,"docked":False,"queue":[],"next_look":0.,"dirty":False,"next_save":0.,"list_ver":0,"me":(0,0,-1),"hooked":False,"tm_at":0.,"tm_serial":0,"hidden":0,"in_pack":frozenset()};j={};F={};aj=5.;J=[False];K=set();t={};u={"g":None,"c":{},"store":({},{}),"rows":[]};Q={"rd":None};ak,v,k=Kit.basics(d,G);A={"at":0.,"items":[]}
		def R(lvl):return ab[lvl]if 0<=lvl<len(ab)else "Treasure map"
		def aK():Kit.kv_load(W,";",m)
		def al():Kit.kv_save(W,";",m,("auto","undecoded","done"))
		def aL():
			j.clear();c=time.time()-60*86400
			for d in Kit.get_var(X).split(";"):
				b=d.strip().split(",")
				if len(b)<7:continue
				try:s=int(b[0],16);a={"x":int(b[1]),"y":int(b[2]),"f":int(b[3]),"lvl":int(b[4]),"done":b[5]=="1","t":int(b[6]),"approx":len(b)>7 and b[7]=="1"}
				except ValueError:continue
				if s<=0 or a["x"]<=0 or a["y"]<=0 or a["t"]<c:continue
				j[s]=a
			am()
		def am():
			if len(j)>af:
				a=sorted(j,key=lambda s:j[s]["t"])
				for b in a[:len(j)-af]:del j[b]
		def an():d["dirty"]=False;Kit.put_var(X,";".join("%X,%d,%d,%d,%d,%d,%d,%d"%(e,a["x"],a["y"],a["f"],a["lvl"],1 if a["done"]else 0,a["t"],1 if a.get("approx")else 0)for e,a in sorted(j.items())))
		def aM(text):
			b=text.lower();c=b.split("\n",1)[0];a={"tm":"treasure map"in b,"lvl":-1,"dec":None,"f":-1,"done":"completed by"in b}
			for d,e in enumerate(aa):
				if e in c:a["lvl"]=d;break
			if a["tm"]:a["dec"]="tattered"not in c
			for f,t in enumerate(aB):
				if t in b:a["f"]=f;break
			return a
		def ao(serial,it,now=None):
			a=F.get(serial)
			if now is not None and a is not None and now<a[2]<=now+aj:return a[1]
			if now is None:now=time.time()
			b=str(API.ItemNameAndProps(serial,False)or "");c=now+aj
			if not b.strip():
				c=0.;b=str(it.Name or "")
				if serial not in K:
					K.add(serial)
					if len(K)>500:K.clear()
					API.RequestOPLData([serial])
			if a is not None and a[0]==b:F[serial]=(b,a[1],c);return a[1]
			d=aM(b)
			if len(F)>300:F.clear()
			F[serial]=(b,d,c);return d
		def S(est,end,p,size):
			if None in(end,p,size):return est,None
			p,size=float(p),float(size)
			if size<=0 or p<0 or p>size:return est,None
			k=1.-p/P;a=None
			if abs(k)>=.001:
				c=p*end/P;d,e=(est-c)/k,(est+1-c)/k;a=int(math.floor((d+e)/2.))
				if not 0<end-a<=8192:a=None
			b=float(end-a)/size if a is not None and abs(k)>=.25 else None
			if abs(size-P)<.5:return est,b
			if a is None or abs(1.-(p+.5)/size)/abs(k)>2.:return None,b
			return int(a+(p+.5)*(end-a)/size),b
		def ap(est,end,p,size,scale=None):
			a=S(est,end,p,size)[0]
			if a is not None:return a,False
			if scale and None not in(end,p,size):return int(end-(float(size)-float(p)-.5)*scale),False
			return est,True
		def l(obj,name):
			v=Typing._get(obj,name)
			if v is None:return
			try:return int(v)
			except Exception:return
		def aN():
			Typing._find();a=Typing.uim
			if a is None:return
			b=Typing._get(None,"Gumps",a)
			if b is None:return
			n=0
			try:
				for g in b:
					if str(g.GetType().Name)!="MapGump":continue
					r=aO(g)
					if r is None:return
					n+=r
			except Exception:return
			return n
		def aO(g):
			a=l(g,"LocalSerial")
			if not a:return 0
			if Typing._get(g,"IsDisposed",default=False):return 0
			if t.get(a)is g:return 0
			k=Typing._get(g,"foundMapLoc")
			if k is None:return
			if not k:return 0
			f,h=l(g,"mapX"),l(g,"mapY")
			if f is None or h is None:return
			m,n,i=l(g,"mapEndX"),l(g,"mapEndY"),l(g,"mapFacet");b=Typing._get(g,"_hit");o=l(b,"Width")if b is not None else None;p=l(b,"Height")if b is not None else None;c=d=None;j=Typing._get(g,"_container")
			try:
				if j is not None and int(j.Count)>0:
					e=j[0];q,r=l(e,"Width"),l(e,"Height");s,u=l(e,"X"),l(e,"Y")
					if None not in(q,r,s,u):c,d=s-q-5,u-r
			except Exception:c=d=None
			if len(t)>50:t.clear()
			t[a]=g;v=S(f,m,c,o)[1];w=S(h,n,d,p)[1];x,z=ap(f,m,c,o,w);y,A=ap(h,n,d,p,v)
			if x is None or y is None or x<=0 or y<=0:return 0
			aq(a,x,y,i if i is not None and i>0 else-1,z or A);return 1
		def aq(serial,x,y,g,approx=False):
			h=API.FindItem(serial);e=ao(serial,h)if h is not None else{};i=time.time();m=0<=i-d["tm_at"]<=D and(d["tm_serial"]==serial or(not d["tm_serial"]and i-d["tm_at"]<=1.5))
			if not(e.get("tm")or serial in j or m):return False
			f=g if g>=0 else e.get("f",-1)
			if f<0:f=int(API.GetMap())
			b=j.get(serial);c=e.get("lvl",-1)
			if c<0 and b is not None:c=b["lvl"]
			a={"x":int(x),"y":int(y),"f":int(f),"lvl":c,"done":bool(e.get("done")or(b is not None and b["done"])),"t":int(time.time()),"approx":bool(approx)};n=(b is not None and(b["x"],b["y"],b["f"])==(a["x"],a["y"],a["f"]));j[serial]=a;am();d["dirty"]=True;d["next_scan"]=0.
			if not n:d["arrow_off"]=False;l,o,p=d["me"];q=(", "+Kit.where_text(a["x"]-l,a["y"]-o,"here"))if p==a["f"]and l>0 else "";k("%s map%s: dig at %s%d, %d in %s%s."%(R(c).lower(),(" (level %d)"%c)if c>=0 else "","about "if a["approx"]else "",a["x"],a["y"],Kit.facet_name(a["f"]),q),Kit.HUE_GOOD)
			return True
		def T(now):d["look_until"]=now+D;d["next_look"]=0.
		def aP(*a):
			if not d["active"]:return
			for b in a:
				try:s=int(b)
				except Exception:continue
				if s>0 and len(d["used"])<20:d["used"].append(s)
				return
		def aQ():Kit.hook_once(d,"hooked",("ObjectUsed",aP))
		def aR(now):
			b,d["used"]=d["used"],[]
			for s in b:
				a=API.FindItem(s)
				if a is not None and int(a.Graphic)in O:d["last_map"]=(s,now);T(now)
		def aS(now):
			c=Q["rd"]
			if c is None:return
			g=G.lower()+":"
			for e in c.new():
				a=e.low
				if "somewhere near"in a:b=1
				elif aD in a or aC in a:b=2
				elif aE in a:b=3
				else:continue
				if a.startswith(g):continue
				f=(e.name or "").strip().lower()
				if f and f!="system":continue
				if b==1:
					m=aF.search(a)
					if m:d["est"]=(int(m.group(1)),int(m.group(2)),now);T(now)
				elif b==2:s,t=d["last_map"];d["tm_at"]=now;d["tm_serial"]=s if s and 0<=now-t<=H else 0;J[0]=True;T(now)
				else:
					s,t=d["last_map"];J[0]=True
					if s and 0<=now-t<=H and s in j and not j[s]["done"]:j[s]["done"]=True;d["dirty"]=True;d["next_scan"]=0.
		def aT(now):
			if not(now<d["look_until"]<=now+D+1.):
				if d["look_until"]>now+D+1.:d["look_until"]=now+D;return
				if d["est"]is not None:ar()
				if t:t.clear()
				return
			if now<d["next_look"]<=now+ad:return
			d["next_look"]=now+ad;n=aN()
			if n is None:
				a,b=d["est"],d["last_map"]
				if a is not None and b[0]and-2.<=a[2]-b[1]<=H:ar()
			elif n>0:d["est"]=None;d["look_until"]=min(d["look_until"],now+1.)
		def ar():
			x,y,a=d["est"];d["est"]=None;s,b=d["last_map"]
			if not s or not(-2.<=a-b<=H)or x<=0 or y<=0:return
			d["last_map"]=(0,0.);aq(s,x,y,-1)
		def at(now):
			try:p=API.Player;i,k=int(p.X),int(p.Y);l=int(API.GetMap())
			except Exception:return
			d["me"]=(i,k,l)
			if not int(API.Backpack or 0):d["in_pack"]=None;return
			q=[y for y in HOST.pack_items(True,.5)if int(y.Graphic)in O];r=aU(now);w=set([int(bi.Serial)for bi in r]);q.extend(r);c,f=[],set();g=0;t=int(time.time());x=None if J[0]else time.time();J[0]=False
			for u in q:
				s=int(u.Serial)
				if s in f:continue
				f.add(s)
				if len(c)>=100:continue
				b=ao(s,u,x);a=j.get(s)
				if not b["tm"]and a is None:continue
				n=b["lvl"]if b["lvl"]>=0 else(a["lvl"]if a else-1);h=bool(b["done"]or(a is not None and a["done"]))
				if a is not None:
					if b["f"]>=0 and a["f"]!=b["f"]:a["f"]=b["f"];d["dirty"]=True
					if n!=a["lvl"]or h!=a["done"]:a["lvl"],a["done"]=n,h;d["dirty"]=True
					if t-a["t"]>86400:a["t"]=t;d["dirty"]=True
				o=True if a is not None else b["dec"];e={"serial":s,"lvl":n,"dec":o,"done":h,"x":None,"y":None,"f":-1,"dist":None,"group":3,"bank":s in w}
				if a is not None:
					e["x"],e["y"],e["f"]=a["x"],a["y"],a["f"];e["approx"]=a.get("approx",False)
					if e["f"]==l:e["dist"]=max(abs(a["x"]-i),abs(a["y"]-k));e["dir"]=Kit.compass(a["x"]-i,a["y"]-k);e["group"]=0
					else:e["group"]=1
				elif o:e["group"]=2
				if h:
					e["group"]=4
					if not m["done"]:g+=1;continue
				elif not o and not m["undecoded"]:g+=1;continue
				e["where"],e["hue"],e["tip"]=aY(e,l)
				if e["bank"]:e["where"]="in the bank: "+e["where"]
				c.append(e)
			c.sort(key=aW);d["list"]=c;d["in_pack"]=f
			if d["pin"]and d["pin"]not in f:d["pin"]=0
			v=(tuple((bj["serial"],bj["lvl"],bj["dec"],bj["done"],bj["where"])for bj in c)+(g,));d["hidden"]=g
			if v!=d["list_sig"]:d["list_sig"]=v;d["list_ver"]+=1
		def aU(now):
			if now-A["at"]<5. and now>=A["at"]:return A["items"]
			b=int(API.Bank or 0);A["at"]=now;A["items"]=[]
			if b and aV(b):A["items"]=[a for a in list(API.ItemsInContainer(b,True)or[])[:2000]if int(a.Graphic)in O]
			return A["items"]
		def aV(bank):
			with Kit.quiet:
				for g in Tz.windows(("ContainerGump","GridContainer")):
					if int(g.LocalSerial)==bank:return True
			return False
		def au(keep):
			a=set((int(f["x"]),int(f["y"]),int(f["f"]))for f in keep)
			for t in d["dig_tiles"]-a:API.RemoveMarkedTile(t[0],t[1],t[2])
			for t in a-d["dig_tiles"]:API.MarkTile(t[0],t[1],53,t[2])
			d["dig_tiles"]=a
		def aW(e):return(e["group"],e["dist"]if e["dist"]is not None else 0,e["lvl"],e["serial"])
		def aX():
			a=[f for f in d["list"]if not(f["x"]is None or f["done"]or f["f"]<0)];c=tuple((g["serial"],g["x"],g["y"],g["f"],g["lvl"])for g in a)
			if c==d["atlas_sig"]:return
			d["atlas_sig"]=c;au(a);b.set("maps",{q(("Dig L%d #%04X"%(p["lvl"],p["serial"]&65535))if p["lvl"]>=0 else("Dig #%04X"%(p["serial"]&65535))):(int(p["x"]),int(p["y"]),int(p["f"]),"yellow")for p in a})
		def aY(e,b):
			if e["x"]is not None:
				a=("about "if e.get("approx")else "")+c(e["x"],e["y"],"(%d, %d)")
				if e["done"]:return "dug up  "+a,Kit.HUE_INFO,ai
				if e["f"]==b:
					d=e["dist"]
					if d==0:return "here  "+a,Kit.HUE_GOOD,E
					return("%s %s  %s"%(Kit.count(d,"tile"),e["dir"],a),Kit.HUE_TEXT,E)
				return("in %s  %s"%(Kit.facet_name(e["f"]),a),Kit.HUE_INFO,"This map's spot is in %s; you are in %s"%(Kit.facet_name(e["f"]),Kit.facet_name(b)))
			if e["done"]:return "dug up",Kit.HUE_INFO,ai
			if e["dec"]:return "open the map once to read its spot",Kit.HUE_INFO,"Double-click the map once to read it"
			if e["dec"]is None:return "open the map to read it",Kit.HUE_INFO,"Double-click the map to read it"
			return "not decoded yet",Kit.HUE_INFO,"Double-click the map to decode it (Cartography)"
		def U(serial):return next((a for a in d["list"]if a["serial"]==serial),None)
		def aZ():
			if d["arrow_off"]:return
			a=d["me"][2]
			if d["pin"]:
				e=U(d["pin"])
				if e is not None and e["x"]is not None and e["f"]==a and not e["done"]:return(e["x"],e["y"],e["serial"])
			if m["auto"]:
				for e in d["list"]:
					if e["group"]==0:return(e["x"],e["y"],e["serial"])
			return
		def C(force_off=False,force=False):
			a=None if force_off else aZ();b=d["arrow"]
			if not force and(a[:2]if a else None)==(b[:2]if b else None):d["arrow"]=a;return
			if a is None:API.TrackingArrow(-1,-1,Z)
			else:API.TrackingArrow(a[0],a[1],Z);d["arrow_at"]=time.time()
			d["arrow"]=a
		def a_(now):
			if d["arrow"]is None:return
			a=now-d.get("arrow_at",0.)
			if a<0:d["arrow_at"]=now;return
			if a<1.5 or I():return
			d["arrow"],d["arrow_off"],d["pin"]=None,True,0
		def av():
			z=i(n,d,560,h(1,o));w,s=z if z else(560,h(N,o));B=n.rows(o,h(0,o),N)if z else N;g,c,e=n.begin(w,s);t=[]
			if not d["minimized"]:
				n.frame(g);M=Kit.MARGIN;j=w-2*M;a=M+30+Kit.GAP;Kit.add_section(g,M,a,j,36);m=M+j-8;Kit.art_button(g,c,"pg_dn",Kit.ART_MIN,m-22,a+8,None,"Next page",on_click=v(("page",1)));Kit.art_button(g,c,"pg_up",Kit.ART_RESTORE,m-46,a+8,None,"Previous page",on_click=v(("page",-1)));u=m-52-Kit.text_w("9/9");e["pg"]=Kit.add_label(g,"",u,a+10,Kit.HUE_INFO);x=u-12-(35+Kit.text_w("Arrow off"));Kit.art_button(g,c,"arrow_off",Kit.ART_CLOSE,x,a+7,"Arrow off","Take the tracking arrow down (a row click or Nearest brings it back)",on_click=v("arrow_off"));y=x-12-(35+Kit.text_w("Nearest"));Kit.art_button(g,c,"nearest",Kit.ART_PLAY,y,a+7,"Nearest","Point the tracking arrow at the nearest dig spot on your facet",on_click=v("nearest"));e["status"]=Kit.add_label(g,"",M+12,a+10,Kit.HUE_INFO);e["status_w"]=y-8-(M+12);b=a+36+Kit.GAP;Kit.add_section(g,M,b,j,s-b-M);k=M+12;p=k+max(34,Kit.text_w("Level"))+8;q=p+150+8;l=M+j-12-22;Kit.add_label(g,"Level",k,b+6,Kit.HUE_TITLE);Kit.add_label(g,"Map",p,b+6,Kit.HUE_TITLE);Kit.add_label(g,"Dig spot",q,b+6,Kit.HUE_TITLE);e["where_w"]=l-8-q;e["empty_w"]=l-8-k
				for A in range(B):f=b+30+A*o;r={"val":None,"prev":None,"changed":0.,"sig":None,"tip":None,"pvis":True,"lvl":Kit.add_label(g,"",k,f+3,Kit.HUE_TITLE),"name":Kit.add_label(g,"",p,f+3,Kit.HUE_TEXT),"where":Kit.add_label(g,"",q,f+3,Kit.HUE_INFO)};r["catch"]=Kit.catcher(g,M+6,f,l-4-(M+6),o,Kit.row_clicker(r,v,"row",follow=False),E);r["ping"]=Kit.art_button(g,c,"ping%d"%A,Kit.ART_PLAY,l,f+1,None,aI,on_click=Kit.row_clicker(r,v,"ping",follow=False));t.append(r)
			n.end(g,{"rows":t});d["drawn"]=None;ax()
		n=Kit.Window(V,G,d,u,av,ay,az,(240,180),(Y,aA),5355,ak,lock=True,clear={"rows":[]},docked_min=True)
		def aw(ctl,r,key,on):
			if r[key]!=on:r[key]=on;Kit.set(ctl,"IsVisible",on)
		def ax():
			B=u["g"]
			if B is None or(d["minimized"]and d["docked"]):return
			q=d["arrow"][2]if d["arrow"]else 0;f=(d["list_ver"],d["page"],q,d["pin"],d["minimized"])
			if f==d["drawn"]:return
			d["drawn"]=f;c=u["c"];j=d["list"];k=next((bi for bi in j if bi["group"]==0),None);n=len(j);l=Kit.count(n,"map")
			if k is not None:s=k["dist"];t=("here"if s==0 else "%s %s"%(Kit.count(s,"tile"),k["dir"]));b="%s, nearest %s"%(l,t);g="%s, %s"%(l,t)
			elif n:b=g="%s, no spot on this facet"%l
			elif d["hidden"]:b="No maps listed (%d hidden on the settings page)"%d["hidden"];g="%d hidden"%d["hidden"]
			else:b="No treasure maps in your pack";g="no maps"
			if d["minimized"]:
				if c.get("status")is not None:Kit.set_text(c["status"],Kit.fit("%s: %s"%(G,g),Y-90))
				return
			v=u["rows"];o=max(1,len(v));h=max(1,(n+o-1)//o)
			if not 0<=d["page"]<h:d["page"]=max(0,min(h-1,d["page"]));d["drawn"]=f[:1]+(d["page"],)+f[2:]
			Kit.set_text(c["status"],Kit.fit(b,c.get("status_w",200)));Kit.set_text(c["pg"],("%d/%d"%(d["page"]+1,h))if h>1 else "");C=d["page"]*o;D=c.get("where_w",200);w=time.time()
			for x,r in enumerate(v):
				y=C+x
				if y>=n:
					Kit.row_set(r,None,w)
					if x==0 and n==0:i=("empty",aJ if not d["hidden"]else(b+"."))
					else:i=("empty","")
					if r["sig"]!=i:r["sig"]=i;Kit.set_text(r["lvl"],Kit.fit(i[1],c.get("empty_w",400)),Kit.HUE_INFO);Kit.set_text(r["name"],"");Kit.set_text(r["where"],"")
					aw(r["ping"],r,"pvis",False);continue
				e=j[y];Kit.row_set(r,(e["serial"],),w);p=q==e["serial"];z=(e["serial"],e["lvl"],e["dec"],e["done"],e["where"],p,d["pin"]==e["serial"],m["auto"])
				if z!=r["sig"]:
					r["sig"]=z;Kit.set_text(r["lvl"],("L%d"%e["lvl"])if e["lvl"]>=0 else "?",Kit.HUE_TITLE if not e["done"]else Kit.HUE_INFO);Kit.set_text(r["name"],Kit.fit(R(e["lvl"]),150),Kit.HUE_TEXT if e["dec"]and not e["done"]else Kit.HUE_INFO);Kit.set_text(r["where"],Kit.fit(("> "if p else "")+e["where"],D),Kit.HUE_TITLE if p else e["hue"]);a=e["tip"]
					if a==E:
						A=d["pin"]==e["serial"]
						if m["auto"]:a=aG if A else E
						else:a="Take the tracking arrow down"if A else aH
					if a!=r["tip"]:r["tip"]=a;Kit.with_tip(r["catch"],a)
				aw(r["ping"],r,"pvis",e["x"]is not None and not e["done"])
		def a0(serial):
			e=U(serial)
			if e is None:return
			if e["x"]is None or e["done"]:k(B(e["tip"])+".");return
			if e["f"]!=d["me"][2]:k("that map's spot is in %s; you are in %s."%(Kit.facet_name(e["f"]),Kit.facet_name(d["me"][2])));return
			d["arrow_off"]=False
			if d["pin"]==serial:
				d["pin"]=0
				if m["auto"]:k("tracking arrow back on the nearest map.")
				else:d["arrow_off"]=True;k("tracking arrow down.")
			else:d["pin"]=serial;k("tracking arrow on the %s map's spot (%d, %d)."%(R(e["lvl"]).lower(),e["x"],e["y"]))
			C(force=True)
		def a1(serial,now):
			e=U(serial)
			if e is None or e["x"]is None:return
			if HOST.services.get("pings.send")is None:k("World Map > Map Pings is off; turn it on to send map pings.");return
			d["ping"]=[e["x"],e["y"],e["f"],now+ag,0.]
		def a2(now):
			p=d["ping"]
			if p is None or(now<p[4]<=now+ah):return
			a=HOST.services.get("pings.send")
			if a is None:d["ping"]=None;k("World Map > Map Pings is off; turn it on to send map pings.");return
			try:b=bool(a(p[0],p[1],m=p[2],kind="go"))
			except Exception:b=True
			if b:d["ping"]=None
			elif not(now<p[3]<=now+ag):d["ping"]=None;k("Map Pings didn't take the ping (too soon after the last one); try again.")
			else:p[4]=now+ah
		def a3():
			a=d["in_pack"]
			if a is None:k("your backpack isn't known yet; nothing was forgotten.");return
			b=[e for e in j if e not in a]
			for s in b:del j[s]
			d["dirty"]=True;k("forgot %s of maps not in your pack."%Kit.count(len(b),"spot"))
		def a4(f,x,y):Kit.add_label(f.g,"%s remembered"%Kit.count(len(j),"spot"),x+12,y+4,Kit.HUE_INFO);Kit.art_button(f.g,f.store,"forget",Kit.ART_CLOSE,x+f.w-12-(35+Kit.text_w("Forget lost maps")),y,"Forget lost maps","Forget the spots of maps not in your backpack",on_click=v("forget"))
		def a5(a,now):d["page"]=max(0,d["page"]+a[1])
		def a6(a,now):
			d["arrow_off"]=False
			if m["auto"]:d["pin"]=0
			else:b=next((f for f in d["list"]if f["group"]==0),None);d["pin"]=b["serial"]if b is not None else 0
			C(force=True)
			if d["arrow"]is None:k("no decoded map with a spot on this facet.")
		def a7(a,now):d["pin"],d["arrow_off"]=0,True;C()
		def a8(a,now):a3();HOST.refresh_settings(V)
		a9={"page":a5,"row":lambda a,now:a0(a[1]),"ping":lambda a,now:a1(a[1],now),"nearest":a6,"arrow_off":a7,"forget":a8};ba=(("WINDOW  (open a decoded map once to read it)",(("check","auto","Point the tracking arrow at the nearest map's spot","With no map picked, the arrow points at the nearest spot on your facet"),("check","undecoded","List maps not decoded yet","Maps still to decode (Cartography)"),("check","done","List maps already dug up","Maps whose treasure is dug up"))),("SAVED SPOTS",(("custom",24,a4),),{"sh":64}),z("maps"))
		def bb(w):return ba
		def bc(old,new):d["next_scan"]=0.;d["drawn"]=None
		L=Kit.Page(m,bb,al,bc)
		def bd():d.update({"shutting":False,"active":True,"docked":False,"queue":[],"used":[],"minimized":n.start_min(),"list":[],"list_sig":None,"next_scan":0.,"arrow":None,"pin":0,"arrow_at":0.,"arrow_off":False,"ping":None,"est":None,"look_until":0.,"last_map":(0,0.),"drawn":None,"page":0,"atlas_ver":None,"atlas_sig":None,"dig_tiles":set()});aK();aL();t.clear();Q["rd"]=M();aQ();at(time.time());av();n.dock(fit=True,min=(560,h(1,o)));C()
		def be():
			if u["g"]is None:return
			if Kit.closed(u):return
			a=time.time()
			if d["used"]:aR(a)
			aS(a);aT(a);q=d["queue"]
			while q:
				b=q.pop(0);c=b[0]if isinstance(b,tuple)else b
				if not n.action(c):a9[c](b,a)
				if u["g"]is None:return
			if not(a<d["next_scan"]<=a+ac):
				d["next_scan"]=a+ac;at(a);a_(a);C()
				if d["list_ver"]!=d["atlas_ver"]:d["atlas_ver"]=d["list_ver"];aX()
			if d["ping"]is not None:a2(a)
			if d["dirty"]and not(a<d["next_save"]<=a+ae):d["next_save"]=a+ae;an()
			ax()
		def bf():return.1 if d["look_until"]>time.time()else.2
		def bg():
			d["shutting"]=True;d["active"]=False;C(force_off=True);al()
			if d["dirty"]:an()
			Q["rd"]=None;au(());d["used"],d["queue"],d["ping"]=[],[],None;ak.close()
		return{"start":bd,"tick":be,"stop":bg,"client_tick":True,"config_height":L.height,"build_config":L.build,"poll_config":L.poll,"config_closed":L.closed,"interval":bf}
	def ag():
		ar="harvest";K="Ore Tracker";S="Harvest_settings";at="Harvest_pos";au="Harvest_min";u=("ore","wood","fish","sand");o={"ore":"Ore","wood":"Wood","fish":"Fish","sand":"Sand"};av={"ore":"mining","wood":"lumberjacking","fish":"fishing","sand":"sand for glassblowing"};aw={"ore":1153,"wood":68,"fish":88,"sand":53};ax={"there is no metal here to mine.":"ore","there's not enough wood here to harvest.":"wood","the fish don't seem to be biting here.":"fish","there is no sand here to mine.":"sand",};ay={"you loosen some rocks but fail to find any useable ore.":"ore","you hack at the tree for a while, but fail to produce any useable wood.":"wood","you fish a while, but fail to catch anything.":"fish","you dig for a while but fail to find any of sufficient quality for glassblowing.":"sand",};az=(("you dig some ","ore"),("you put some logs","wood"),("you chop some ","wood"),("you pull out ","fish"),("you carefully dig up sand","sand"),("your backpack can't hold the sand","sand"),);aA=("","system");T={"ore":(8,8),"wood":(4,3),"fish":(8,8),"sand":(8,8)};L={"ore":(10,20),"wood":(20,30),"fish":(10,20),"sand":(10,20)};U=3;aB={"ore":3,"wood":3,"fish":5,"sand":3};V=300;N=8;X=.85;F=.95;aC,aD=40,3.5;Y=.5;Z="harvest.weight";aa=1.;ab=1.;O=0x48525654;ac=6.;ad=5.;P="Harvest_spots";W=440;ae,aE=340,46;v=24;aF={"north":(0,-1),"northeast":(1,-1),"east":(1,0),"southeast":(1,1),"south":(0,1),"southwest":(-1,1),"west":(-1,0),"northwest":(-1,-1)};af="Put the tracking arrow on it (again: take it down)";aG="Send a Look here ping on this spot so others know it is dry (needs World Map > Map Pings)";aH="No dry spots yet: spots the shard says ran out show here.";ag=60.*U*max(be for bf,be in L.values());f={"ore":True,"wood":True,"fish":True,"sand":True,"alert":True,"keep":True};bd=dict(f);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"rd":None,"ver":0,"mini_key":None,"w_key":None,"arrow_at":0.};g={};h={};j={"g":None,"c":{},"store":({},{}),"rows":[]};p=[];ah,G,A=Kit.basics(a,K)
		def aI():Kit.kv_load(S,";",f)
		def ai():Kit.kv_save(S,";",f,u+("alert","keep"))
		def aj():return ";".join("%s,%d,%d,%d,%d,%d,%d"%(d["kind"],d["m"],d["x"],d["y"],int(d["lo"]),int(d["hi"]),1 if d["about"]else 0)for d in g.values())
		def aJ():
			g.clear()
			if not f["keep"]:return
			c=time.time()
			for e in Kit.get_var(P).split(";"):
				b=e.split(",")
				if len(b)<7 or b[0]not in u:continue
				try:m,x,y,h,d=int(b[1]),int(b[2]),int(b[3]),float(b[4]),float(b[5])
				except ValueError:continue
				if d<=c or d-c>ag+60:continue
				ak(b[0],m,x,y,h,d,b[6]=="1",c)
			a["ver"]+=1
		def B():
			a["ver"]+=1
			if f["keep"]:a["save_due"]=True
		def aK():a["save_due"]=False;a["save_at"]=time.time()+ad;Kit.put_var(P,aj()if f["keep"]else "")
		def s(kind,m,x,y):a,b=T[kind];return(kind,m,x//a,y//b)
		def ak(kind,m,x,y,lo,hi,about,now):
			b=s(kind,m,x,y);d=g.get(b);g[b]={"kind":kind,"m":m,"x":x,"y":y,"lo":lo,"hi":hi,"at":now,"about":about,"key":b}
			if a["arrow"]==b and d is not None and(d["x"],d["y"])!=(x,y):API.TrackingArrow(x,y,O);a["arrow_at"]=now
			if len(g)>60:
				c=None
				for e,f in g.items():
					if e!=b and(c is None or f["hi"]<g[c]["hi"]):c=e
				if c is not None:
					del g[c]
					if a["arrow"]==c:k()
			return b
		def al():return U if HOST.guarded()is True else 1
		def aL(kind,x,y,m,about,now):
			g=s(kind,m,x,y);b,a=L[kind];c=al();b,a=b*c,a*c;f=h.pop(g,None)
			if f is not None and 0<=now-f<a*60.:d,e=f+b*60.,f+a*60.
			else:d,e=now,now+a*60.
			ak(kind,m,x,y,d,e,about,now);B()
		def aM(kind,x,y,m,got,now):
			b=s(kind,m,x,y)
			if g.pop(b,None)is not None:
				if a["arrow"]==b:k()
				B()
			if got:
				f=h.get(b)
				if f is None or not 0<=now-f<L[kind][1]*60.*al():
					if len(h)>=V:
						for c in[d for d,e in h.items()if not 0<=now-e<ag]:del h[c]
						if len(h)>=V:h.clear()
					h[b]=now
		def aN(now):
			c=[n for n,m in g.items()if m["hi"]<=now or m["at"]-now>60.]
			for d in c:
				del g[d]
				if a["arrow"]==d:k()
			if c:B()
			b=a["arrow"]
			if b is not None and 1.5<=now-a["arrow_at"]and not I():a["arrow"]=None;a["ver"]+=1;b=None
			if b is not None:
				e=E()
				if e is not None and e[2]!=b[1]:k()
		def aO(d):
			for e in g.values():e["lo"]+=d;e["hi"]+=d;e["at"]+=d
			for k in list(h):h[k]+=d
			for k in("w_at","draw_at","expire_at","save_at","arrow_at"):a[k]=a[k]+d
			p=a["ping"]
			if p is not None:p[3]+=d
			if g:B()
		def E():
			p=API.Player
			if p is None:return
			b=(int(p.X),int(p.Y),int(API.GetMap()))
			if b[0]<=0 and b[1]<=0:return
			a["me"]=b;return b
		def aP(kind,me):
			a,b=me[0],me[1];p=API.LastTargetPos;x,y=int(p.X),int(p.Y)
			if 0<x<65535 and 0<y<65535 and max(abs(x-a),abs(y-b))<=aB[kind]:return x,y,False
			c,d=aF.get(str(API.Player.Direction or "").strip().lower(),(0,0));return a+c,b+d,True
		def aQ(low):
			k=ax.get(low)
			if k is not None:return "dry",k
			k=ay.get(low)
			if k is not None:return "fail",k
			if low.startswith("you"):
				for a,k in az:
					if low.startswith(a):return "got",k
			return
		def aR(now):
			e=a["rd"]
			if e is None:return
			for g in e.new():
				h=aQ(g.low.strip())
				if h is None or(g.name or "").strip().lower()not in aA:continue
				d,b=h
				if d=="dry"and not f[b]:continue
				c=E()
				if c is None:continue
				x,y,i=aP(b,c)
				if d=="dry":aL(b,x,y,c[2],i,now)
				else:aM(b,x,y,c[2],d=="got",now)
		def aS():s=HOST.by_key.get("character");return s is not None and bool(s.running)
		def aT(now):
			if now<a["w_at"]and a["w_at"]-now<=Y:return
			a["w_at"]=now+Y
			if not f["alert"]and(j["g"]is None or(a["minimized"]and a["docked"])):return
			p=API.Player
			if p is None:return
			d,b=int(p.Weight),int(p.WeightMax);e=int(p.Strength)if b<=0 else 0
			if b<=0 and e>0:b=int(aC+aD*e)
			c=(float(d)/b)if b>0 else-1.;a["weight"]=(d,b,c)
			if c>=F:
				if a["w_armed"]:
					g=True
					if f["alert"]and not aS():g=C(Z,"Weight %d/%d (%d%%): nearly overloaded"%(d,b,int(c*100)),level="warn",who="weight")is not False
					if g:a["w_armed"]=False
			elif 0<=c<.92:a["w_armed"]=True
		def k():
			if a["arrow"]is None:return
			a["arrow"]=None;a["ver"]+=1;API.TrackingArrow(-1,-1,O)
		def aU(key):
			e=g.get(key)
			if e is None:return
			if a["arrow"]==key and I(True):k();return
			b=E()or a["me"]
			if b is not None and b[2]!=e["m"]:A("that spot is in %s; you are in %s."%(Kit.facet_name(e["m"]),Kit.facet_name(b[2])));return
			API.TrackingArrow(e["x"],e["y"],O);a["arrow"],a["arrow_at"]=key,time.time();a["ver"]+=1
		def aV(key):
			e=g.get(key)
			if e is None:return
			if HOST.services.get("pings.send")is None:A("turn World Map > Map Pings on to ping a spot.");return
			a["ping"]=[e["x"],e["y"],e["m"],time.time()+ac,"the dry %s spot (%d, %d)"%(o[e["kind"]].lower(),e["x"],e["y"])]
		def aW(now):
			p=a["ping"]
			if p is None:return
			b=HOST.services.get("pings.send")
			if b is None or now>p[3]or p[3]-now>ac+1.:a["ping"]=None;A("the ping on %s wasn't sent (%s)."%(p[4],"Map Pings is off"if b is None else "Map Pings stayed busy"));return
			try:c=b(p[0],p[1],p[2],"look")
			except Exception:c=None
			if c is False:return
			a["ping"]=None
			if c:A("Look here ping on %s."%p[4],Kit.HUE_GOOD)
			else:A("couldn't send the ping on %s (Map Pings refused it)."%p[4],Kit.HUE_BAD)
		def Q(secs):
			secs=max(0,int(secs))
			if secs<60:return "%ds"%secs
			return "%dm"%((secs+59)//60)
		def aX(e,me):
			if me is None:return 0
			if me[2]!=e["m"]:return 1<<30
			if s(e["kind"],me[2],me[0],me[1])==e["key"]:return 0
			return max(abs(e["x"]-me[0]),abs(e["y"]-me[1]))
		def aY(e,me):
			if me is None:return c(e["x"],e["y"],"(%d, %d)")
			if me[2]!=e["m"]:return "in %s"%Kit.facet_name(e["m"])
			if s(e["kind"],me[2],me[0],me[1])==e["key"]:return "here"
			return("about "if e["about"]else "")+Kit.where_text(e["x"]-me[0],e["y"]-me[1])
		def am(e,now):
			if now<e["lo"]:return "back in %s-%s"%(Q(e["lo"]-now),Q(e["hi"]-now)),Kit.HUE_BAD
			return "back within %s"%Q(e["hi"]-now),Kit.HUE_TITLE
		def aZ(e,on):
			a,b=T[e["kind"]];g,h=(e["x"]//a)*a,(e["y"]//b)*b;d=time.strftime("%H:%M",time.localtime(e["hi"]))
			if e["lo"]>e["at"]:f="back between %s and %s"%(time.strftime("%H:%M",time.localtime(e["lo"])),d)
			else:f="back by %s at the latest"%d
			return "%s ran dry at %s%s: the %dx%d block from %s, %s.  %s"%(o[e["kind"]],c(e["x"],e["y"])," (about: the tile in front of you)"if e["about"]else "",a,b,c(g,h),f,"Take the tracking arrow down"if on else af)
		def R():return[d for d in g.values()if f[d["kind"]]]
		def a_(t):return(t[0],t[1])
		def a0():b.set("dry",{q("%s dry %d %d"%(o[d["kind"]],d["x"],d["y"])):(int(d["x"]),int(d["y"]),int(d["m"]),"blue")for d in sorted(R(),key=lambda e:-e["at"])[:15]})
		def H(n):return 2*Kit.MARGIN+30+3*Kit.GAP+46+36+74+n*v+22
		def an():
			M=Kit.MARGIN;z=i(l,a,W,H(1));w,q=z if z else(W,H(N));s=l.rows(v,H(0),N)if z else N;g,f,c=l.begin(w,q);t=[]
			if not a["minimized"]:
				l.frame(g);b=w-2*M;h=M+30+Kit.GAP;Kit.add_section(g,M,h,b,46,"WEIGHT");c["wtext"]=Kit.add_label(g,"",M+20+Kit.text_w("WEIGHT"),h+6,Kit.HUE_TEXT);Kit.weight_bar(g,c,M+12,h+28,b-24);j=h+46+Kit.GAP;Kit.add_section(g,M,j,b,36);m=M+12;Kit.art_button(g,f,"clear",Kit.ART_CLOSE,m,j+7,"Clear","Empty the list of dry spots",on_click=G("clear"));m+=35+Kit.text_w("Clear")+16;Kit.art_button(g,f,"arrow_off",Kit.ART_CLOSE,m,j+7,"Arrow off","Take the tracking arrow down",on_click=G("arrow_off"));k=j+36+Kit.GAP;Kit.add_section(g,M,k,b,q-k-M,"DRY SPOTS  (nearest first)");c["here"]=Kit.add_label(g,"",M+12,k+28,Kit.HUE_INFO);y=35+Kit.text_w("Ping");u,x,n=M+12,M+12+52,M+12+52+130;o=M+b-6-y;c["back_w"]=o-8-n;d=k+52;Kit.add_label(g,"What",u,d,Kit.HUE_TITLE);Kit.add_label(g,"Where",x,d,Kit.HUE_TITLE);Kit.add_label(g,"When",n,d,Kit.HUE_TITLE);c["here_w"]=b-24
				for p in range(s):e=d+22+p*v;r={"val":None,"prev":None,"changed":0.,"sig":None,"vis":True,"tip":None,"kind":Kit.add_label(g,"",u,e+3,Kit.HUE_TEXT),"where":Kit.add_label(g,"",x,e+3,Kit.HUE_TEXT),"back":Kit.add_label(g,"",n,e+3,Kit.HUE_INFO)};r["catch"]=Kit.catcher(g,M+6,e,o-4-(M+6),v,Kit.row_clicker(r,G,"arrow",follow=False),af);r["plbl"]=Kit.art_button(g,f,"ping%d"%p,Kit.ART_PLAY,o,e,"Ping",aG,on_click=Kit.row_clicker(r,G,"ping",follow=False));r["pbtn"]=f[0].get("ping%d"%p);t.append(r)
				c["more"]=Kit.add_label(g,"",M+12,d+22+s*v+2,Kit.HUE_INFO)
			l.end(g,{"rows":t});a["drawn"]=a["mini_drawn"]=a["wdrawn"]=None;a["draw_at"]=0.;ap(time.time())
		l=Kit.Window(ar,K,a,j,an,at,au,(260,220),(ae,aE),3718,ah,lock=True,clear={"rows":[],"c":{}},docked_min=True)
		def ao(r,on):
			if r["vis"]==on:return
			r["vis"]=on
			for n in("where","back","catch","pbtn","plbl"):Kit.set(r.get(n),"IsVisible",on)
			if not on:Kit.set_text(r["kind"],"")
		def ap(now):
			G=j["g"]
			if G is None or(a["minimized"]and a["docked"]):return
			c=j["c"]
			if a["minimized"]:
				b=a["weight"];h=(a["ver"],f["ore"],f["wood"],f["fish"],f["sand"])
				if a["count"][0]!=h:a["count"]=(h,len(R()))
				q=a["count"][1];t=(q,b)
				if a["mini_drawn"]is not None and t==a["mini_key"]:return
				a["mini_key"]=t;n="%s: %s, %s"%(K,("weight %d%%"%int(b[2]*100))if b and b[2]>=0 else "weight ?",Kit.count(q,"dry spot"))
				if n!=a["mini_drawn"]:
					a["mini_drawn"]=n;v=c.get("status")
					if v is not None:
						p=Kit.HUE_INFO
						if b and b[2]>=F:p=Kit.HUE_BAD
						elif b and b[2]>=X:p=Kit.HUE_TITLE
						Kit.set_text(v,Kit.fit(n,ae-90),p)
				return
			a1();h=(a["ver"],a["arrow"],f["ore"],f["wood"],f["fish"],f["sand"])
			if h==a["drawn"]and now<a["draw_at"]and a["draw_at"]-now<=aa:return
			a["drawn"],a["draw_at"]=h,now+aa;d=E()or a["me"];i=[(aX(be,d),be["hi"],be)for be in R()];i.sort(key=a_);l=None
			if d is not None:
				for w in u:
					if f[w]:
						e=g.get(s(w,d[2],d[0],d[1]))
						if e is not None:l=e;break
			if l is not None:Kit.set_text(c["here"],Kit.fit("Here: %s is dry, %s"%(o[l["kind"]].lower(),am(l,now)[0]),c["here_w"]),Kit.HUE_BAD)
			elif i:Kit.set_text(c["here"],"Here: nothing known dry",Kit.HUE_GOOD)
			else:Kit.set_text(c["here"],Kit.fit(aH,c["here_w"]),Kit.HUE_INFO)
			H=c.get("back_w",160)
			for x,r in enumerate(j["rows"]):
				if x>=len(i):Kit.row_set(r,None,now);r["sig"]=None;ao(r,False);continue
				e=i[x][2];y=aY(e,d);m=e["key"];Kit.row_set(r,(m,),now);k=a["arrow"]==m;z,A=am(e,now);B=(m,y,z,A,k,e["lo"],e["hi"]);ao(r,True)
				if B==r["sig"]:continue
				r["sig"]=B;Kit.set_text(r["kind"],o[e["kind"]],aw.get(e["kind"],Kit.HUE_TEXT));Kit.set_text(r["where"],Kit.fit(("> "if k else "")+y,124),Kit.HUE_TITLE if k else Kit.HUE_TEXT);Kit.set_text(r["back"],Kit.fit(z,H),A);C=(m,k,e["lo"],e["hi"])
				if C!=r["tip"]:r["tip"]=C;Kit.with_tip(r["catch"],aZ(e,k))
			D=len(i)-len(j["rows"]);Kit.set_text(c["more"],("+%d farther"%D)if D>0 else "",Kit.HUE_INFO)
		def a1():
			c=j["c"];b=a["weight"]
			if a["wdrawn"]is not None and b==a["w_key"]:return
			a["w_key"]=b;h=c.get("wfills")
			if b is None or b[2]<0:e,d,f="not known yet",None,0
			else:e="%d / %d stones (%d%%)"%(b[0],b[1],int(b[2]*100));d,f=Kit.weight_level(b[2],c.get("wbar_w",100))
			g=(e,d,f)
			if g==a["wdrawn"]:return
			a["wdrawn"]=g;i={"red":Kit.HUE_BAD,"warn":Kit.HUE_TITLE}.get(d,Kit.HUE_TEXT)
			if c.get("wtext")is not None:Kit.set_text(c["wtext"],e,i)
			Kit.weight_show(h or{},d,f)
		a2=("Back in: ore and sand 10-20 min, wood 20-30, fish 10-20, from the block's first harvest (3x as long in guarded towns).")
		def a3(action):k();g.clear();B()
		a4={"clear":a3,"arrow_off":lambda action:k(),"arrow":lambda action:aU(action[1]),"ping":lambda action:aV(action[1])}
		def aq(kind):return "%s (%s)"%(o[kind],av[kind])
		def a5(w):a=max(Kit.text_w(aq(d))for d in u);return 2 if a+30<=(w-24)//2 else 1
		def a6(w):a,b=a5(w),(w-24)//2;return(("WHAT TO WATCH",[("check",d,aq(d),"List spots where the %s ran out"%o[d].lower(),{"dx":12+(e%a)*b,"stay":e%a<a-1})for e,d in enumerate(u)]+[("gap",6),("check","keep","Keep the list when Virtue Assistant stops (per character)","Unticked: it starts empty each time"),("gap",2)]+[("note",m)for m in["Unticked kinds are hidden, not forgotten."]+Kit.wrap(a2,w-28)],{"top":32}),("WEIGHT  (yellow at %d%%, red at %d%%)"%(int(X*100),int(F*100)),(("check","alert","Alert as you cross the red line","Once each time you pass %d%% of your maximum weight; quiet while Inventory > Paperdoll is on (it has its own)"%int(F*100)),),{"top":32,"pad":4}),z("dry"))
		def a7(old,new):
			if new["keep"]!=old["keep"]:a["save_due"]=True
			if new["alert"]and not old["alert"]:a["w_armed"]=True
			a["drawn"]=a["mini_drawn"]=None
		J=Kit.Page(f,a6,ai,a7)
		def a8():a.update({"shutting":False,"docked":False,"queue":[],"drawn":None,"mini_drawn":None,"wdrawn":None,"arrow":None,"ping":None,"w_armed":True,"weight":None,"w_at":0.,"draw_at":0.,"expire_at":0.,"save_due":False,"save_at":0.,"me":None,"count":(None,0),"last_now":None,"atlas":None,"minimized":l.start_min()});del p[:];h.clear();aI();aJ();a["rd"]=M();D(Z,"Weight near the limit",74);E();an();l.dock(fit=True,min=(W,H(1)))
		def a9():
			if j["g"]is None:return
			if Kit.closed(j):return
			b=time.time();d,a["last_now"]=a["last_now"],b
			if d is not None and b<d-2.:aO(b-d)
			q=a["queue"]
			while q:
				c=q.pop(0);g=c[0]if isinstance(c,tuple)else c
				if not l.action(c):a4[g](c)
				if j["g"]is None:return
			aR(b)
			if b>=a["expire_at"]or a["expire_at"]-b>ab:a["expire_at"]=b+ab;aN(b)
			e=(a["ver"],f["ore"],f["wood"],f["fish"],f["sand"])
			if e!=a["atlas"]:a["atlas"]=e;a0()
			aT(b);aW(b);ap(b)
			if a["save_due"]and(b>=a["save_at"]or a["save_at"]-b>ad)and not p:p.append(aK)
		def ba():
			while p and not a["shutting"]:p.pop(0)()
		def bb():return bool(p)
		def bc():a["shutting"]=True;k();a["ping"]=a["rd"]=None;del p[:];ai();Kit.put_var(P,aj()if f["keep"]else "");a["save_due"]=False;ah.close()
		return{"start":a8,"tick":a9,"stop":bc,"client_tick":True,"config_height":J.height,"build_config":J.build,"poll_config":J.poll,"config_closed":J.closed,"thread_tick":ba,"thread_wanted":bb}
	def ah():
		r="traphl";s="Traps & Fields";L="TrapHL_settings";ae="TrapHL_pos";M="TrapHL_view";H=Kit.MARGIN+30+Kit.GAP+40+Kit.MARGIN;N,af=320,46;O=68;P=33;h=3000;ag=.15;ah=1.;ai=3.;aj=3.;ak=5.;al=[4355,4374,4524,4529,4512,4520,4536,4412,4423,4341,4348,4389,7025,7026,7027,7028,3696,];Q="TrapHL_fields";am=(("fire",14732,14751),("poison",14612,14633),("paralyze",14695,14730),("energy",14662,14692));t=53;u=1153;an={"fire":("Fire field",Kit.HUE_TITLE),"poison":("Poison field",Kit.HUE_TITLE),"energy":("Energy field",Kit.HUE_TITLE),"paralyze":("Paralyze field!",Kit.HUE_BAD)};R=3;S="traphl.trap";v={a3:a0 for a0,a1,a2 in am for a3 in range(a1,a2+1)};ao={};c={"range":14,"cycle":2.,"pulse":True,"green":O,"red":P,"by_name":True,"graphics":list(al),"ping":True,"fields":True,"field_hue":t,"para_hue":u,"field_say":False};a_=dict(c);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"hooked":False,"poke":False};n={"g":None,"c":{},"store":({},{})};d={"f":None,"gfx_typed":None,"gfx_since":0.};T,ap,U=Kit.basics(a,s)
		def aq():
			p=Kit.get_var(L).split("|")
			if len(p)<7:return
			with Kit.quiet:
				c["range"]=max(1,min(30,int(p[0])));c["cycle"]=max(.5,min(10.,float(p[1])));c["pulse"]=p[2]=="1";c["green"]=int(p[3]);c["red"]=int(p[4]);c["by_name"]=p[5]=="1";a=V(p[6])
				if a or not p[6].strip():c["graphics"]=a
				if len(p)>=8:c["ping"]=p[7]!="0"
		def ar():
			v=Kit.codec_load(Kit.get_var(Q));c["fields"]=v.get("on")!="0";c["field_say"]=v.get("say")=="1"
			for k,a,b in(("hue","field_hue",t),("para","para_hue",u)):
				try:c[a]=max(0,min(h,int(v[k])))
				except(KeyError,ValueError):c[a]=b
		def at():Kit.put_var(Q,"on=%d;hue=%d;para=%d;say=%d"%(int(c["fields"]),c["field_hue"],c["para_hue"],int(c["field_say"])))
		def A():Kit.put_var(L,"|".join([str(c["range"]),"%.2f"%c["cycle"],"1"if c["pulse"]else "0",str(c["green"]),str(c["red"]),"1"if c["by_name"]else "0",E(),"1"if c["ping"]else "0"]))
		def V(text):
			b=[]
			for a in str(text).replace(";",",").replace(" ",",").split(","):
				a=a.strip()
				if not a:continue
				try:v=int(a,16)
				except Exception:continue
				if 0<v<65536 and v not in b:b.append(v)
			return b
		def E():return ", ".join("0x%04X"%e for e in c["graphics"])
		def au():b=Kit.get_var(M);v=Kit.codec_load(b);a["minimized"]=v.get("min")=="1";a["paused"]=v.get("paused")=="1";a["view_saved"]=b
		def W():
			b="min=%d;paused=%d"%(int(bool(a["minimized"])),int(bool(a["paused"])))
			if b!=a.get("view_saved"):a["view_saved"]=b;Kit.put_var(M,b)
		def j(item,hue):item.Hue=int(hue)&65535
		def o(item):return int(item.Hue or 0)
		def F(item):return int(item.X),int(item.Y)
		m={};X={"gfx":None,"wanted":frozenset(),"by_name":None,"fields":None}
		def av(it):
			a=str(it.Name or "").lower()
			if not a:return
			return "trap"in a and "scroll"not in a and "kit"not in a
		def aw():
			a=X;b=c["graphics"]
			if a["gfx"]is not b or a["by_name"]!=c["by_name"]or a["fields"]!=c["fields"]:a["gfx"],a["wanted"]=b,frozenset(b);a["by_name"],a["fields"]=c["by_name"],c["fields"];m.clear()
			return a["wanted"]
		def ax():
			y=int(c["range"]);a["atlas_map"]=None;l={};n={};i=a["last_scan"];p=i>=a["hue_at"];t=v if c["fields"]else ao
			if p:a["hue_at"]=i+aj
			z=aw();A=c["by_name"];B=m;q={}
			for b in API.GetItemsOnGround(y)or():
				d=int(b.Serial);g=int(b.Graphic);f=B.get(d)
				if f is not None and f[0]==g and(not f[2]or i<f[2]):e=f[1];q[d]=f
				else:
					u=0
					if g in z:e=1
					elif A and g not in t:
						w=av(b)
						if w is None:e,u=0,i+ak
						else:e=1 if w else 0
					else:e=2 if g in t else 0
					q[d]=(g,e,u)
				if e==1:l[d]=b
				elif e==2:n[d]=b
			m.clear();m.update(q);h=a["tracked"];r=[]
			for d,b in l.items():
				k=h.get(d)
				if k is None:
					s=o(b)
					if s in(c["green"],c["red"]):s=0
					h[d]={"item":b,"orig":s,"set":c["green"]};j(b,c["green"]);ay(b)
					if c["ping"]and d not in a["pinged"]:a["ping_wait"].append(d)
					if d not in a["alerted"]:r.append(b)
				else:
					k["item"]=b
					if p and o(b)!=k["set"]:j(b,k["set"])
			x=[a0 for a0 in h if a0 not in l]
			for d in x:G(d,h.pop(d))
			if x and a["ping_wait"]:a["ping_wait"]=[a1 for a1 in a["ping_wait"]if a1 in h]
			if r:aB(r)
			if n or a["fields"]:aC(n,p)
		def ay(it):
			x,y=F(it)
			if x<=0 or y<=0:return
			if a["atlas_map"]is None:a["atlas_map"]=int(API.GetMap())
			c=(x,y,a["atlas_map"]);b=a["atlas_traps"]
			if c in b:return
			b.append(c)
			if len(b)>20:del b[0]
			a["atlas_ver"]+=1
		def az():b.set("traps",{q("Trap %d %d"%(e,f)):(e,f,g,"red")for e,f,g in a["atlas_traps"]})
		aA=("east","south-east","south","south-west","west","north-west","north","north-east")
		def aB(b):
			d=a["alerted"]
			if len(d)+len(b)>5000:d.clear()
			p=API.Player;l,m=int(p.X),int(p.Y);f,e,g,h=None,None,0,0
			for c in b:
				d.add(int(c.Serial));i,j=int(c.X)-l,int(c.Y)-m;k=max(abs(i),abs(j))
				if e is None or k<e:f,e,g,h=c,k,i,j
			w=Kit.where_text(g,h,names=aA);n="A trap %s"%w if len(b)==1 else "%d new traps in range (nearest %s)"%(len(b),w);C(S,n,who=int(f.Serial))
		def Y(kind):return c["para_hue"]if kind=="paralyze"else c["field_hue"]
		def aC(l,m):
			h=a["fields"];i=[]
			for f,d in l.items():
				e=h.get(f)
				if e is None:
					k=v.get(int(d.Graphic))
					if k is None:continue
					b=Y(k);g=o(d)
					if g and g in(c["field_hue"],c["para_hue"]):g=0
					h[f]=e={"item":d,"orig":g,"set":b,"kind":k}
					if b:j(d,b)
					if c["field_say"]:i.append(e)
					continue
				e["item"]=d;b=Y(e["kind"])
				if b!=e["set"]:j(d,b if b else e["orig"]);e["set"]=b
				elif b and m and o(d)!=b:j(d,b)
			for f in[w for w in h if w not in l]:Z(f)
			if i:aD(i)
		def aD(recs):
			d=time.time();b=[w for w in a["field_said"]if d-w[3]<10.];f=sorted([F(a0["item"])+(a0["kind"],a0["item"])for a0 in recs],key=aE)
			for x,y,c,g in f:
				e=False
				for k,h,i,t in b:
					if(k==c and abs(h-x)<=R and abs(i-y)<=R):e=True;break
				b.append((c,x,y,d))
				if e:continue
				j,l=an.get(c,("Field",Kit.HUE_TITLE));API.HeadMsg(j,int(g.Serial),l)
			a["field_said"]=b[-20:]
		def aE(e):return(e[0],e[1])
		def Z(serial):
			b=a["fields"].pop(serial,None)
			if b is not None and b["set"]:G(serial,b)
		def G(serial,rec):j(API.FindItem(serial)or rec["item"],rec["orig"])
		def aa():
			for b in list(a["tracked"]):G(b,a["tracked"].pop(b))
			for b in list(a["fields"]):Z(b)
		def aF():
			if not a["tracked"]:return
			e=c["pulse"]and(time.time()%max(.5,c["cycle"])<min(.35,c["cycle"]/2.));b=c["red"]if e else c["green"]
			for d in a["tracked"].values():
				if d["set"]!=b:j(d["item"],b);d["set"]=b
		def p():return HOST.services.get("pings.send")
		def aG():
			b=len(a["ping_wait"])
			if b:
				aH()
				if len(a["ping_wait"])!=b:k()
		def aH():
			b=a["ping_wait"];e=p()
			if e is None:
				if not a["ping_noted"]:a["ping_noted"]=True;U("turn World Map > Map Pings on to ping traps (they wait until then).")
				return
			if time.time()<a["ping_next"]:return
			g=a["tracked"];m=None
			while b:
				c=b[0];f=g.get(c)
				if f is None or c in a["pinged"]:b.pop(0);continue
				x,y=F(f["item"])
				if x<=0 or y<=0:b.pop(0);continue
				if m is None:m=int(API.GetMap())
				d=(m,x,y)
				if d in a["pinged_spots"]:I(c,None);b.pop(0);continue
				try:h=e(x,y,m,"danger","You (trap)")
				except Exception:I(c,d);b.pop(0);return
				if h:b.pop(0);I(c,d);a["ping_sent"]+=1;a["ping_next"]=time.time()+.75
				return
		def I(serial,spot):
			if len(a["pinged"])>=5000:a["pinged"].clear();a["pinged_spots"].clear()
			a["pinged"].add(serial)
			if spot is not None:a["pinged_spots"].add(spot)
		def aI():
			a["pinged"].clear();a["pinged_spots"].clear();a["ping_sent"]=0;a["ping_wait"]=list(a["tracked"]);n=len(a["ping_wait"])
			if a["paused"]:b="paused: untick Pause highlighting (World Map settings) to ping traps."
			elif n==0:b="no traps in range; each is pinged when next found."
			elif p()is None:b=("%s to ping once World Map > Map Pings is on."%Kit.count(n,"trap"))
			else:b="pinging %s."%Kit.count(n,"trap")
			U(b);a["ping_noted"]=False;k()
		def aJ():
			n=len(a["ping_wait"])
			if n and a["ping_svc"]is not None:return "sending %d"%n,Kit.HUE_INFO
			if not c["ping"]:return "auto-ping off",Kit.HUE_INFO
			if a["ping_svc"]is None:return "World Map > Map Pings is off",Kit.HUE_BAD
			return "%d sent"%a["ping_sent"],Kit.HUE_GOOD
		aK="Ping danger on each highlighted trap, and again when next found (needs World Map > Map Pings)";K="Ping traps on screen"
		def ab():
			z=i(l,a,320,H);w,h=z if z else(320,H);g,c,d=l.begin(w,h)
			if not a["minimized"]:l.frame(g);M=Kit.MARGIN;b=M+30+Kit.GAP;Kit.add_section(g,M,b,w-2*M,h-b-M);Kit.art_button(g,c,"ping",Kit.ART_CIRCLE,M+12,b+12,K,aK,on_click=ap("ping_again"))
			l.end(g);k();W()
		l=Kit.Window(r,s,a,n,ab,ae,None,(200,200),(N,af),4412,T,lock=True)
		def k():
			h=n["c"];e=len(a["tracked"]);g=len(a["fields"])
			if a["paused"]:b,c="Paused",Kit.HUE_INFO
			elif e==0 and g==0:b,c="No traps in range",Kit.HUE_INFO
			elif g==0:b,c="Highlighting %s"%Kit.count(e,"trap"),Kit.HUE_GOOD
			elif e==0:b,c="Highlighting %s"%Kit.count(g,"field"),Kit.HUE_GOOD
			else:b,c="Highlighting %s, %s"%(Kit.count(e,"trap"),Kit.count(g,"field")),Kit.HUE_GOOD
			if h.get("status")is not None:Kit.set_text(h["status"],Kit.fit("%s: %s"%(s,B(b)),N-90),c)
			f=d["f"]
			if f is None:return
			Kit.set_text(f.c["now"],b,c);i,j=aJ();Kit.set_text(f.c["now_ping"],"Pings: "+i,j)
			if a["pause_want"]is None and bool(f.c["paused"].IsChecked)!=bool(a["paused"]):f.c["paused"].SetIsChecked(bool(a["paused"]))
		def aL(f,x,y):f.c["now"]=Kit.add_label(f.g,"",x+12,y,Kit.HUE_GOOD);f.c["now_ping"]=Kit.add_label(f.g,"",x+12+f.w//2,y,Kit.HUE_INFO)
		def aM(f,x,y):f.c["paused"]=Kit.add_check(f.g,"Pause highlighting (the hues are put back)",x+12,y,a["paused"],"Stops the scan and puts every hue back")
		aN={"ping_again":aI}
		def aO(f,x,y):Kit.add_label(f.g,"Pulse cycle:",x+12,y+4);a=int(round(c["cycle"]*10));f.c["cycle"]=Kit.with_tip(Kit.add_slider(f.g,x+120,y+2,160,5,100,a),"Seconds between red flashes (0.5-10)");f.c["cycle_v"]=Kit.add_label(f.g,"%.1f s"%c["cycle"],x+290,y+4,Kit.HUE_INFO)
		def aP(f,x,y):f.c["graphics"]=Kit.with_tip(Kit.add_textbox(f.g,E(),x+12,y,f.w-28,numbers=False),"Trap item graphics in hex (0x1103 or 1103), comma separated; applied when you stop typing")
		ac={"lw":98,"fw":60,"stay":True,"clamp":False};ad=(("STATUS  (the window has %s)"%K,(("custom",24,aL),("custom",26,aM)),{"pad":4}),("TRAPS  (hues are client hue numbers)",(("slider","range","Scan range:","Tiles round you scanned as you move (1-30)",1,30,{"lw":98,"ldy":4,"sw":160,"ugap":10,"vfmt":"%d tiles"}),("custom",29,aO),("num","green","Green hue:","Hue traps are held at (1-%d; default %d)"%(h,O),None,1,h,ac),("num","red","Red hue:","Hue of the pulse (1-%d; default %d)"%(h,P),None,1,h,{"dx":200,"lw":70,"fw":60,"h":29,"clamp":False}),("check","pulse","Pulse red once per cycle (unticked: steady green)","Flashes each highlighted trap red for a beat")),{"top":32,"pad":2}),("TRAP GRAPHICS  (hex ids, comma separated)",(("custom",30,aP),("check","by_name","Also highlight ground items the client names 'trap'","For traps not in the list (the client knows a name only after a tooltip or click)")),{"top":32,"pad":8}),("TRAP PINGS  (needs World Map > Map Pings)",(("check","ping","Send a Danger! map ping on each new trap, once per trap","For you and your guildmates; \"%s\" on the window pings them all again"%K),),{"top":32,"pad":4}),("MAGIC FIELDS  (client hue numbers, 0 = leave as is)",(("check","fields","Highlight magic fields: fire, poison, energy, paralyze","Client-side recolour, like the traps; paralyze fields get their own hue",{"h":29}),("num","field_hue","Field hue:","Hue of fire, poison and energy fields (0-%d, 0 = as is; default %d)"%(h,t),None,0,h,ac),("num","para_hue","Paralyze hue:","Hue of paralyze fields (0-%d, 0 = as is; default %d)"%(h,u),None,0,h,{"dx":200,"lgap":12,"fw":60,"h":29,"clamp":False}),("check","field_say","Show an overhead text when a field appears","Names each new field above it once (\"Fire field\", \"Paralyze field!\")")),{"top":32,"pad":2}),z("traps"))
		def aQ(w):return ad
		aR=Kit.Page(c,aQ,A)
		def aS(g,x,y,w):d["f"]=Kit.Form(g,x,y,w,c,ad);d["gfx_typed"],d["gfx_applied"]=None,E();k()
		def aT():
			h=d["f"]
			if h is None:return
			b=h.read();g=h.c;i=time.time()
			try:e=str(g["graphics"].Text or "");f=int(g["cycle"].Value);j=bool(g["paused"].IsChecked)
			except Exception:return
			f=max(5,min(100,f))/10.
			if abs(f-c["cycle"])>.01:b["cycle"]=f;Kit.set_text(g["cycle_v"],"%.1f s"%f)
			if e!=d["gfx_typed"]:d["gfx_typed"],d["gfx_since"]=e,i
			elif i-d["gfx_since"]>=.7 and e!=d["gfx_applied"]:d["gfx_applied"]=e;b["graphics"]=(V(e)or c["graphics"])if e.strip()else[]
			if j!=(a["paused"]if a["pause_want"]is None else a["pause_want"]):a["pause_want"]=j
			if b["ping"]!=c["ping"]:a["ping_wait"]=[w for w in a["tracked"]if w not in a["pinged"]]if b["ping"]else[]
			if b==c:return
			c.update(b);a["last_scan"]=0.;A();at();k()
		def aU():d["f"]=None;d["gfx_typed"]=None
		def aV():
			a.update({"shutting":False,"docked":HOST.dock_soon(r),"queue":[],"last_scan":0.,"hue_at":0.,"moved":False,"tracked":{},"pinged":set(),"pinged_spots":set(),"ping_wait":[],"ping_sent":0,"ping_noted":False,"ping_svc":p(),"ping_next":0.,"fields":{},"field_said":[],"alerted":set(),"atlas_traps":[],"atlas_ver":0,"atlas_done":-1,"atlas_map":None,"pause_want":None});m.clear();aq();ar();D(S,"New trap in range",495);au();Kit.hook_once(a,"hooked",("OnItemCreated",aX),("OnPositionChanged",aY))
			if J(r):a["minimized"]=True
			ab();l.dock(fit=True,min=(320,H))
		def aW():
			if n["g"]is None:return
			if Kit.closed(n):return
			b=a["pause_want"]
			if b is not None:
				a["pause_want"]=None
				if b!=a["paused"]:
					a["paused"]=b
					if b:aa();a["ping_wait"]=[]
					else:a["last_scan"]=0.
					W();k()
			while a["queue"]:
				e=a["queue"].pop(0)
				if not l.action(e):aN[e]()
			if a["paused"]:return
			f=time.time();c=f-a["last_scan"]
			if c>=ai or(a["moved"]and c>=ah)or(a["poke"]and c>=ag):
				a["last_scan"]=f;a["poke"]=a["moved"]=False;g=(len(a["tracked"]),len(a["fields"]));ax();d=p()
				if(len(a["tracked"]),len(a["fields"]))!=g or(d is None)!=(a["ping_svc"]is None):
					a["ping_svc"]=d
					if d is not None:a["ping_noted"]=False
					k()
				if a["atlas_ver"]!=a["atlas_done"]:a["atlas_done"]=a["atlas_ver"];az()
			aG();aF()
		def aX(*b):
			if a["poke"]or a["paused"]or a["shutting"]:return
			for d in b:
				try:g=int(d.Graphic)
				except Exception:continue
				if g in X["wanted"]or(c["fields"]and g in v):a["poke"]=True
				return
		def aY(*b):a["moved"]=True
		def aZ():a["shutting"]=True;aa();A();T.close()
		return{"start":aV,"tick":aW,"stop":aZ,"client_tick":True,"config_height":aR.height,"build_config":aS,"poll_config":aT,"config_closed":aU}
	ai=(("pings",ad,.05,"pings"),("corpse",lambda:A(ae(),"corpse"),.25,"corpserun"),("maps",lambda:A(af(),"maps"),.2,"treasure"),("dry",lambda:A(ag(),"dry"),.2,"harvest"),("traps",lambda:A(ah(),"traps"),.1,"traphl"),);return PartSet(U,N,ai,shared=ab).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("worldmap","World Map","Pings, corpse, dig and dry spots, traps",_module_worldmap,.05,category="The world",parts=(("pings","Map Pings","Guild pings on your Enhanced Map",False,("pings",)),("corpse","Corpse","Arrow, decay time and Get my things",False,("corpserun",)),("maps","Treasure Maps","Dig spots of your decoded maps",False,("treasure",)),("dry","Ore Tracker","Your weight and spots that ran dry",False,("harvest",)),("traps","Traps & Fields","Traps and magic fields recoloured",False,("traphl",)),),aliases=('Map Pings','Corpse Run','Treasure Hunter','Harvest Helper','Dry spots','Ore Tracker','Trap Highlight','Enhanced Map','tracking arrow','ping','corpse','dig spot','weight bar','TazUO World Map'))
