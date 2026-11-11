def _module_worldmap():
	af=HOST.alert;ag=HOST.alert_kind;U=HOST.dock_forget;au=HOST.dock_wanted;av=HOST.layout_holds;ah=HOST.release_cursor;aw=HOST.show_settings;ax=Journal.reader;O=Kit.ART_CLOSE;az=Kit.ART_MIN;P=Kit.ART_PLAY;aA=Kit.ART_RESTORE;ai=Kit.FACETS;C=Kit.GAP;A=Kit.HUE_BAD;D=Kit.HUE_GOOD;b=Kit.HUE_INFO;B=Kit.HUE_TEXT;i=Kit.HUE_TITLE;F=Kit.MARGIN;aB=Kit.add_check;c=Kit.add_label;I=Kit.add_section;aj=Kit.add_textbox;k=Kit.art_button;R=Kit.basics;ak=Kit.catcher;V=Kit.closed;W=Kit.codec_load;z=Kit.count;X=Kit.drop_arrow;E=Kit.facet_name;o=Kit.fit;J=Kit.get_var;al=Kit.hook_once;am=Kit.kv_load;an=Kit.kv_save;aC=Kit.on_client;H=Kit.put_var;S=Kit.row_clicker;Q=Kit.row_set;Y=Kit.save_min;ao=Kit.set;h=Kit.set_text;u=Kit.text_w;aD=Kit.was_clicked;K=Kit.where_text;L=Kit.with_tip;aL="worldmap";aE="World Map";ap="VA ";aq="WorldMap_atlas_placed";aF="WorldMap_atlas";aG=(("corpse","your corpse"),("maps","your dig spots"),("dry","the spots that ran dry"),("traps","the traps you have seen"));aM=1.;aH=2.5;aN=.5;Z=2.;aI=3;aO=60;aP={"at":-1.,"ok":False,"map":False,"arrow":False}
	def aJ(fresh=False):
		a=aP;b=time.time()
		if not fresh and 0.<=b-a["at"]<aN:return a
		a["at"]=b;c=d=False
		try:e=[str(f.GetType().Name)for f in Tz.windows(("WorldMapGump","QuestArrowGump"))];c,d="WorldMapGump"in e,"QuestArrowGump"in e;a["ok"]=True
		except Exception:a["ok"]=False
		a["map"],a["arrow"]=c,d;return a
	class Atlas(object):
		def __init__(self):self.items,self.on,self.placed,self.want,self.loose={},{},{},{},set();self.synced=True;self.open_since=self.saved=None;self.next_check=0.;self.loaded=self.strip_pending=False;self.chg={}
		def load(self):
			if self.loaded:return
			self.loaded=True
			for k,v in W(J(aF)).items():self.on[k]=v!="0"
			a=str(API.GetPersistentVar(aq,"",API.PersistentVar.Global)or "")
			for b in a.split("\n"):
				p=b.split("|")
				if len(p)==5 and p[0].startswith(ap):
					try:self.placed[p[0]]=(int(p[1]),int(p[2]),int(p[3]),p[4])
					except ValueError:pass
			self.saved=a;self.strip_pending=bool(self.placed)and not self.map_open(True);self._rebuild()
		def is_on(self,owner):self.load();return self.on.get(owner,True)
		def set_on(self,owner,on):
			self.load()
			if self.on.get(owner,True)!=bool(on):self.on[owner]=bool(on);H(aF,";".join("%s=%d"%(a,1 if self.on.get(a,True)else 0)for a,d in aG));self._rebuild()
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
						if len(a)>=aO:break
						a[d]=v
			self.want=a;self.synced=a==self.placed
		def map_open(self,fresh=False):f=aJ(fresh);return f["ok"]and f["map"]
		def tick(self):
			if self.synced or self.strip_pending:return
			a=time.time()
			if a<self.next_check and self.next_check-a<=Z+aM:return
			if not self.map_open():self.open_since=None;self.next_check=a+aH;return
			if self.open_since is None or self.open_since>a:self.open_since=a
			if a-self.open_since<Z:self.next_check=self.open_since+Z;return
			if not self.map_open(True):self.open_since=None;self.next_check=a+aH;return
			self.next_check=a+.25;c=0
			for b in list(self.placed):
				if c>=aI:break
				if self.want.get(b)!=self.placed[b]:API.RemoveMapMarker(b);self._drop(b);c+=1
			for b,v in self.want.items():
				if c>=aI:break
				if b not in self.placed:API.AddMapMarker(b,v[0],v[1],v[2],v[3]);self._put(b,v);c+=1
			self.synced=self.want==self.placed;self._save()
		def thread_work(self):
			if not self.strip_pending and not self.loose:return
			a=aC(lambda:self.map_open(True))
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
			try:b=str(API.GetPersistentVar(aq,"",API.PersistentVar.Global)or "")
			except Exception:return
			a=Kit.merge_text(b,self.chg,lambda l:l.split("|",1)[0])[0];self.chg={};self.saved=a;safe(lambda:API.SavePersistentVar(aq,a,API.PersistentVar.Global))
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
	q=Atlas()
	def aa(text):return ap+str(text).replace(","," ")
	def ar(fresh=False):f=aJ(fresh);return f["arrow"]if f["ok"]else True
	ab={}
	def ac(owner):
		def a(f,x,y):ab[owner]=aB(f.g,"Show %s on TazUO's World Map"%dict(aG).get(owner,owner),x+12,y,q.is_on(owner),"Markers named \"%s...\" while the map is open; removed when unticked or the part stops"%ap)
		return "TAZUO'S WORLD MAP  (while open)",(("custom",26,a),),{"sh":66}
	def ad(api,owner):
		b,c,d=api["poll_config"],api["config_closed"],api["stop"]
		def e():
			b();a=ab.get(owner)
			if a is not None:
				try:c=bool(a.IsChecked)
				except Exception:return
				if c!=q.is_on(owner):q.set_on(owner,c)
		def f():c();ab.pop(owner,None)
		def g():
			try:d()
			finally:ab.pop(owner,None);q.clear(owner)
		a=dict(api);a.update({"poll_config":e,"config_closed":f,"stop":g});return a
	aK={"said":False}
	def aQ():
		try:q.tick()
		except Exception as a:
			if not aK["said"]:aK["said"]=True;API.SysMsg("%s: couldn't update TazUO's World Map (%s)."%(aE,a),A)
	def aR():
		try:q.thread_work()
		except Exception:q.strip_pending=False
	aS={"tick":aQ,"stop":q.shutdown,"thread_tick":aR,"thread_wanted":lambda:q.strip_pending or q.loose};aT=("TazUO","World Map","Map Pings","Enhanced Map","Virtue Assistant","Settings","Inventory","Need help","Look here","Go here","Danger!")
	def ae(text):
		text=str(text or "")
		if not text or text[0]in "[(\"'"or text.startswith(aT):return text
		return text[0].lower()+text[1:]
	def M(x,y,fmt="%d, %d"):return Kit.veil("xy",fmt%(x,y))
	def N(rows,row_h):return 2*F+30+2*C+36+30+rows*row_h+8
	def T(a,st,b,c):
		z=a.slot
		if z is None or st["minimized"]or not av(a.key)or z[0]<b or z[1]<c:return
		return z
	def aU():
		bB="pings";an="Map Pings";aH=8887;E={"look":"CTRL+1","danger":"CTRL+2","go":"CTRL+3","help":"CTRL+4",};aO=("look","danger","go","help");aI=60;aP=.75;aQ=5;a6=(490,775,508,514);aR=200;aJ=10
		try:import socket;import select;aS=True
		except Exception:aS=False
		import collections;V="EMPings.";aT=V+"options";ac,ag,GO,ap=0,1,2,3;aq=[("auto","TazUO's map if on, else my login"),("tazuo","Only TazUO's Enhanced Map"),("own","Only my own login")];aK=[bJ[0]for bJ in aq];ad={"ping_secs":(2,60),"drag":(5,200)};j={"sounds":True,"share":True,"gesture":True,"connection":"auto","ping_secs":8,"drag":25};bC=dict(j);l={"minimized":False,"shutting":False,"docked":False,"queue":[],"app":None};bD={"g":None,"c":{},"store":({},{})};aU,bE,s=R(l,an)
		def a7():
			for k,v in W(J(aT)).items():
				if k in("sounds","share","gesture"):j[k]=v=="1"
				elif k=="connection"and v in aK:j[k]=v
				elif k in ad:
					try:a,b=ad[k];j[k]=max(a,min(b,int(v)))
					except ValueError:pass
				elif k.startswith("hk_")and k[3:]in E:E[k[3:]]=_norm_key(v)
		def ar():a="sounds=%d;share=%d;gesture=%d;connection=%s"%(j["sounds"],j["share"],j["gesture"],j["connection"]);a+="".join(";hk_%s=%s"%(d,E[d].replace(";",""))for d in aO);a+=";ping_secs=%d;drag=%d"%(int(j["ping_secs"]),int(j["drag"]));H(aT,a)
		def bF():pass
		bG=None
		def bH():pass
		bI={};aL={"look":ac,"danger":ag,"go":GO,"help":ap};aV={"up":ac,"right":ag,"down":GO,"left":ap};aa={ac:("Look here",53,14138,"yellow"),ag:("Danger!",33,14089,"red"),GO:("Go here",68,14186,"green"),ap:("Need help",88,14170,"blue"),};ax=0x50494E47
		def v(t):return aa[t][0]
		def al(m):return ai[m]if 0<=m<len(ai)else "map %d"%m
		def af(a,payload=b""):return struct.pack("<BH",a,3+len(payload))+payload
		def a8(user,a):u,p=user.encode("latin-1","replace"),a.encode("latin-1","replace");return af(31,struct.pack("<BB",len(u),len(p))+u+p)
		def aW(x,y):return af(39,struct.pack("<HH",x&65535,y&65535))
		aB=32768
		def a9(a,ay):
			if not(a&aB and ay&aB):return
			return a&8191,ay&4095,(ay>>12)&7,(a>>13)&3
		def ba(x,y,m,t):
			if 0<=x<8192 and 0<=y<4096 and 0<=m<8 and 0<=t<4:return aW(aB|(t<<13)|x,aB|(m<<12)|y)
		def bb(pos,stats,flag,color):return af(37,struct.pack("<HHB6HBBBIB",pos[0]&65535,pos[1]&65535,pos[2]&255,*([max(0,min(d,65535))for d in stats]+[flag,0,0,color&0xFFFFFFFF,5]))+b"Arial"+struct.pack("<fB",12.,1))
		class Reader(object):
			def __init__(self,data,offset=3):self.d,self.p=data,offset
			def take(self,n):
				if self.p+n>len(self.d):raise ValueError("short packet")
				self.p+=n;return self.d[self.p-n:self.p]
			def u8(self):return bytearray(self.take(1))[0]
			def u16(self):return struct.unpack("<H",self.take(2))[0]
			def ascii(self,n):return bytes(self.take(n)).decode("latin-1")
		class PySocketTransport(object):
			def __init__(self,host,port,timeout):self.s=socket.create_connection((host,port),timeout);self.s.settimeout(aQ)
			def send(self,data):self.s.sendall(data)
			def recv(self):
				r,b,b=select.select([self.s],[],[],0)
				if not r:return b""
				a=self.s.recv(8192)
				if not a:raise EOFError()
				return a
			def close(self):safe(lambda:self.s.close())
		class DotNetTransport(object):
			def __init__(self,host,port,timeout):
				import clr;from System.Net.Sockets import TcpClient,SelectMode;self._select_read=SelectMode.SelectRead;from System import Array,Byte;self._Array,self._Byte=Array,Byte;self.c=TcpClient();a=self.c.ConnectAsync(host,port)
				if not a.Wait(int(timeout*1000))or not self.c.Connected:self.c.Close();raise IOError("timed out")
				self.st=self.c.GetStream();self.st.WriteTimeout=int(aQ*1000)
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
		def bc(host,port,timeout=5):
			if aS:
				try:return PySocketTransport(host,port,timeout)
				except(socket.timeout,socket.gaierror,ConnectionError,OSError):raise
				except Exception:pass
			return DotNetTransport(host,port,timeout)
		class Sender(object):
			def __init__(self,b):
				self.t=b;self.error=self.cond=None;self.stopped=False;self.q=collections.deque()
				try:import threading;self.cond=threading.Condition();a=threading.Thread(target=self._run);a.daemon=True;a.start()
				except Exception:self.cond=None
			def send(self,data):
				if self.error is not None or self.stopped:raise self.error or IOError("sender stopped")
				if self.cond is None:self.t.send(data);return
				with self.cond:self.q.append(data);self.cond.notify()
			def _run(self):
				while not self.stopped:
					with self.cond:
						while not self.q and not self.stopped:self.cond.wait(.5)
						if self.stopped:return
						a=self.q.popleft()
					try:self.t.send(a)
					except Exception as b:self.error=b;return
			def stop(self):
				self.stopped=True
				if self.cond is not None:
					with self.cond:self.q.clear();self.cond.notify()
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
						import threading;b=self.connecting={"done":False,"t":None,"err":None,"abandon":False,"lock":threading.Lock()}
						def h(p=b,host=self.host,port=self.port):
							try:p["t"]=bc(host,port)
							except Exception as a:p["err"]=a
							with p["lock"]:p["done"]=True;b=p["abandon"]
							if b and p["t"]is not None:p["t"].close()
						try:i=threading.Thread(target=h);i.daemon=True;i.start()
						except Exception:h()
					if not b["done"]:return a
					self.connecting=None;d=time.time()
					try:
						if b["err"]is not None:raise b["err"]
						if b["t"]is None:raise IOError("no connection")
						self.t=b["t"]
					except Exception as e:self.backoff=min(self.backoff*2,60);a.append(("status","Can't reach the map server at %s:%d (%s). Retrying in %d s."%(self.host,self.port,am(e),self.backoff),not self.unreachable_reported));self.unreachable_reported=True;self.next_try=d+self.backoff;return a
					self.state=self.HANDSHAKE;self.state_since=d;self.buf=bytearray();self.sender=Sender(self.t);self.send(af(43,b"\x00"));a.append(("status","Connecting",False))
				c=None;g=self.sender
				if g is not None and g.error is not None:e=g.error;c=("error","%s: %s"%(e.__class__.__name__,am(e)))
				try:
					j=self.t.recv()if self.t else b""
					if j:
						self.buf.extend(j)
						if len(self.buf)>1<<20:raise IOError("too much data")
				except EOFError:c=("eof","")
				except Exception as e:c=("error","%s: %s"%(e.__class__.__name__,am(e)))
				while len(self.buf)>=3 and self.t is not None:
					k=self.buf[0];f=self.buf[1]|(self.buf[2]<<8)
					if f<3:self._drop(a,"garbled","bad packet size",10);return a
					if len(self.buf)<f:break
					l=bytes(self.buf[:f]);del self.buf[:f]
					try:self._handle(k,l,a)
					except ValueError:pass
				if c and self.t is not None:self._drop(a,c[0],c[1],30 if self.state==self.LOGIN else 10);return a
				if(self.t is not None and self.state in(self.HANDSHAKE,self.LOGIN)and d-self.state_since>15):self._drop(a,"timeout","no reply in 15 s",15)
				return a
			def _handle(self,a,data,events):
				r=Reader(data)
				if a==43 and self.state==self.HANDSHAKE:self.state=self.LOGIN;self.state_since=time.time();self.send(a8(self.user,self.password))
				elif a==31 and self.state==self.LOGIN:
					if r.u8()==1:r.u8();self.name=r.ascii(r.u8())or self.user;self.state=self.READY;self.ready_since=time.time();self.login_failures=0;self.backoff=3;self.unreachable_reported=False;events.append(("status","Connected as %s."%self.name,True))
					else:self._drop(events,"eof","login rejected",30)
				elif a in(51,39)and self.state==self.READY:events.append(aX(a,r))
				elif a==47 and self.state==self.READY:events.append(("message",r.ascii(r.u16())))
		def aX(a,r):
			if a==51:x,y,m,t=r.u16(),r.u16(),r.u8(),r.u8();return("ping",r.ascii(r.u8()),x,y,m,t if t in aa else ac)
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
				b,c=aZ(a.GetType())
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
					if b:a.append(("status","Using TazUO's Enhanced Map login (%s)."%(self.name or "connected"),True))
					elif self.was_connected:
						c=time.time();self.drops=[f for f in self.drops if c-f<self.DROP_WINDOW]+[c]
						if len(self.drops)>=self.DROP_LIMIT and not self.unhooked_for_drops:safe(self.bridge.unhook);self.unhooked_for_drops=True;a.append(("status","TazUO's Enhanced Map keeps dropping, so Map Pings stopped listening on it (your pings still go out; others' don't show). If it still drops, the cause is elsewhere. Click Reconnect to listen again.",True))
						else:a.append(("status","TazUO's Enhanced Map connection dropped; TazUO will reconnect.",True))
					else:a.append(("status","Waiting for TazUO's Enhanced Map to connect",False))
					self.was_connected=b
				for d,e in self.bridge.frames():
					if d==51:self.server_relays_ping=True
					try:a.append(aX(d,Reader(e,0)))
					except ValueError:pass
				return a
			def send(self,data):safe(lambda:self.bridge.send(data))
			def reset(self):
				self.drops=[]
				if self.unhooked_for_drops:self.unhooked_for_drops=False;safe(self.bridge.hook)
				safe(self.bridge.reconnect)
			def close(self):safe(self.bridge.unhook)
		def am(e):s=str(e)or e.__class__.__name__;return s if len(s)<60 else s[:59]
		aY={}
		def aZ(t):
			a=aY.get(t)
			if a is None:a=aY[t]=(t.GetField("X"),t.GetField("Y"))
			return a
		def bd(obj):
			if obj is None:return
			with Kit.quiet:return int(obj.X),int(obj.Y)
			with Kit.quiet:
				t=obj.GetType();a,b=aZ(t)
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
				c,d,l,k=aa[t];b,e,f,g=self.player();h=K(x-b,y-e,"on you")if f==m and b>0 else "on %s"%al(m);who=(who or "You")if local else sender;s("%s pinged %s %s (%d, %d, %s)."%("you"if who=="You"else who,c,h,x,y,al(m)),d);self.hist_seq+=1;p.entry=HistEntry(self.hist_seq,a,t,str(who),x,y,m,bool(local));self.history.append(p.entry)
				if len(self.history)>aR:del self.history[:len(self.history)-aR]
				self.hist_ver+=1
				if not local and g:API.HeadMsg("%s: %s %s"%(sender,c,h),g,d)
				if f==m:
					i=(x,y,m);self.marked[i]=self.marked.get(i,0)+1;p.marked=True;API.MarkTile(x,y,d,m)
					if(not auto and b>0 and x>0 and y>0 and max(abs(x-b),abs(y-e))>2):API.TrackingArrow(x,y,ax);self.arrow_for=p
				j=("%s: %s %s"%(who,c,time.strftime("%H:%M:%S"))).replace(","," ")
				if q.map_open(True):
					API.AddMapMarker(j,x,y,m,k);self.markers.append((a+60,j))
					if len(self.markers)>aI:q.loose.update([w for G,w in self.markers[:-aI]]);del self.markers[:-aI]
				self._play_sound(t,a)
			def _play_sound(self,t,now):
				if not j["sounds"]or now-self.last_sound<.3:return
				self.last_sound=now;API.PlaySound(a6[t])
			def update(self):
				if not self.pings and not self.markers:return
				a=time.time();b=None;c=j["ping_secs"]
				for p in list(self.pings):
					if a-p.created>=c:self._expire(p);continue
					if a<p.next_pulse:continue
					if b is None:b=self.player()[2]
					if p.map==b:p.next_pulse=a+self.PULSE;d,e,f,d=aa[p.type];API.CreateEffect(f,type=API.EffectType.FixedXYZ,hue=e,sourceX=p.x,sourceY=p.y,duration=self.PULSE)
				if self.markers and a>=self.markers[0][0]and self._map_ready(a)and q.map_open(True):
					while self.markers and a>=self.markers[0][0]:API.RemoveMapMarker(self.markers.pop(0)[1])
			def _map_ready(self,now):
				if now>=self.map_at or self.map_at-now>2.:
					self.map_at=now+1.
					if q.map_open():
						if self.map_since is None or self.map_since>now:self.map_since=now
					else:self.map_since=None
				return self.map_since is not None and now-self.map_since>=Z
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
			def arrow_to(self,e):API.TrackingArrow(e.x,e.y,ax);self.arrow_for=e
			def arrow_off(self):
				if self.arrow_for is not None:API.TrackingArrow(-1,-1,ax);self.arrow_for=None
			def clear(self):
				for p in list(self.pings):self._expire(p)
				if self.markers:
					a=[d for e,d in self.markers]
					if q.map_open(True):
						for b in a:API.RemoveMapMarker(b)
					else:q.loose.update(a)
				self.markers=[];API.TrackingArrow(-1,-1,ax)
		class Settings(object):
			def __init__(self):
				a=API.PersistentVar.Server;self.host=API.GetPersistentVar(V+"host","",a).strip()
				try:self.port=int(API.GetPersistentVar(V+"port",str(aH),a))
				except ValueError:self.port=aH
				self.user=API.GetPersistentVar(V+"user","",a).strip();self.password=API.GetPersistentVar(V+"pass","",a)
			@property
			def complete(self):return bool(self.host and self.user and self.password and 0<self.port<65536)
			def save(self):
				a=API.PersistentVar.Server
				for k,v in(("host",self.host),("port",str(self.port)),("user",self.user),("pass",self.password)):API.SavePersistentVar(V+k,v,a)
		aE="Ping History";X="pings_history";be=V+"history_pos";aF=V+"history_min";aM=V+"history_open";a_,bf=320,46;ab=24;bg=(("When",70),("Ping",80),("From",140));a0="Put the tracking arrow on this spot (click again to take it down)";bh=". Alt+click: auto-follow (again to stop)";bi="No pings yet. Send one with a ping button, a hotkey or the wheel drag."
		class HistoryWindow(object):
			def __init__(self,app):self.app=app;self.page,self.next_draw=0,0.;self.drawn=self.drawn_pos=None;self.st={"g":None,"shutting":False,"minimized":False,"docked":False,"queue":[],"c":{},"store":({},{}),"rows":[]};self.wnd=Kit.Window(X,aE,self.st,self.st,self.build,be,default=(260,160),mini=(a_,bf),icon=5355,lock=True,owner=False,close_tip="Close Ping History",clear={"c":{},"rows":[]});self.queue=self.wnd.queue
			def start(self):
				a=self.st;a["shutting"]=False;a["minimized"]=Kit.load_min(aF)or au(X);self.wnd.dock(fit=True,min=(560,N(1,ab)),show=self.zone_show)
				if J(aM,"0")=="1":self.build()
			def zone_show(self):self.st["minimized"]=self.st["docked"]=False;self.queue.add("open")
			def toggle_open(self):
				a=self.st
				if a["g"]is not None and not(a["minimized"]or a["docked"]):
					if not av(X):self.close()
					return
				a["minimized"]=a["docked"]=False;U(X);Y(aF,False);H(aM,"1");self.build()
			def close(self):
				a=self.st
				if a["g"]is None:return
				self.wnd.close();a["docked"]=False;U(X);H(aM,"0")
			def shutdown(self):
				a=self.st;a["shutting"]=True;HOST.dock_remove(X)
				if a["g"]is not None:Y(aF,a["minimized"]and not a["docked"]);self.wnd.close()
			def build(self):
				o=self.st;z=T(self.wnd,o,560,N(1,ab));w,p=z if z else(560,N(aJ,ab));v=self.wnd.rows(ab,N(0,ab),aJ)if z else aJ;g,h,q=self.wnd.begin(w,p);s=[]
				if not o["minimized"]:
					self.wnd.frame(g);M=F;e=w-2*M;a=M+30+C;I(g,M,a,e,36);j=M+12;k(g,h,"clear",O,j,a+7,"Clear","Empty the history (pings on screen stay)",on_click=self.queue("clear"));j+=35+u("Clear")+16;k(g,h,"arrow_off",O,j,a+7,"Arrow off","Take the tracking arrow down",on_click=self.queue("arrow_off"));l=M+e-8;q["pg"]=c(g,"",l-100,a+10,b);k(g,h,"pg_up",aA,l-56,a+8,None,"Previous page (newer pings)",on_click=self.queue(("page",-1)));k(g,h,"pg_dn",az,l-34,a+8,None,"Next page (older pings)",on_click=self.queue(("page",1)));f=a+36+C;I(g,M,f,e,p-f-M);d=M+12;m=[]
					for x,t in bg:c(g,x,d,f+6,i);m.append((d,t));d+=t+8
					c(g,"Where",d,f+6,i);q["where_w"]=M+e-12-d
					for y in range(v):n=f+30+y*ab;r={"val":None,"prev":None,"changed":0.,"tip":None,"vis":True,"sig":None,"labels":[c(g,"",G,n+3,B)for G,at in m],"where":c(g,"",d,n+3,b),"widths":[ay for bJ,ay in m]};r["catch"]=ak(g,M+6,n,e-12,ab,S(r,self.queue,"arrow"),a0);s.append(r)
				self.wnd.end(g,{"rows":s});self.drawn=None;self.refresh()
			def tick(self):
				a=self.st
				if a["g"]is not None and aD(a["store"],"close"):self.close();return
				q=a["queue"]
				while q:
					c=q.pop(0);b=c[0]if isinstance(c,tuple)else c
					if b=="toggle_min":a["minimized"]=not a["minimized"];a["docked"]=False;U(X);Y(aF,a["minimized"])
					elif b=="to_bar":HOST.dock_to_bar(X,aE)
					elif b=="settings":aw("pings")
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
				if b!=e.map:s("that ping is on %s; you are on %s."%(al(e.map),al(b)));return
				a.arrow_to(e);s("tracking arrow on %s's %s (%d, %d)."%(e.who,v(e.type),e.x,e.y))
			def follow(self,seq):
				e=self.entry(seq)
				if e is None:return
				if e.local:s("that ping is your own.");return
				a=self.mobile_named(e.who)
				if not a:s("%s isn't in range."%e.who);return
				Follow.toggle(a,an)
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
				a=M(e.x,e.y,"(%d, %d)")
				if b!=e.map or px<=0:return "%s %s"%(al(e.map),a)
				return "%s  %s"%(K(e.x-px,e.y-py,"here"),a)
			def refresh(self):
				g=self.st;a=self.app.display;c=a.history;d=g["c"]
				if g["minimized"]:
					if self.drawn==a.hist_ver:return
					self.drawn=a.hist_ver
					if c:e=c[-1];t="%s: %s, last %s %s"%(aE,z(len(c),"ping"),v(e.type),self.sender(e))
					else:t="%s: no pings yet"%aE
					if d.get("status")is not None:h(d["status"],o(t,a_-90))
					return
				f=time.time();u=a.arrow_entry();k=(a.hist_ver,self.page,u)
				if k==self.drawn and f<self.next_draw:return
				l=a.player()[:3]if c else(0,0,-1)
				if k==self.drawn and l==self.drawn_pos:self.next_draw=f+1.;return
				self.drawn,self.next_draw,self.drawn_pos=k,f+1.,l;n=len(c);m=max(1,len(g["rows"]));p=max(1,(n+m-1)//m);self.page=max(0,min(p-1,self.page))
				if d.get("pg")is not None:h(d["pg"],("%d/%d"%(self.page+1,p))if p>1 else "")
				C,D,E=l;F=n-1-self.page*m;G=d.get("where_w",200)
				for w,r in enumerate(g["rows"]):
					x=F-w
					if x<0:
						Q(r,None,f);r["sig"]=None
						if w==0 and n==0:h(r["labels"][0],bi,b);self._show(r,True,only_first=True)
						else:self._show(r,False)
						continue
					e=c[x];Q(r,(e.seq,),f);H=aa[e.type][1];j=u is e;y=self.where_text(e,C,D,E);A=(e.seq,y,j)
					if A!=r["sig"]:
						r["sig"]=A;I=(time.strftime("%H:%M:%S",time.localtime(e.at)),v(e.type),self.sender(e));J=(b,H,B if not e.local else b)
						for q,K in enumerate(r["labels"]):h(K,o(I[q],r["widths"][q]),J[q])
						h(r["where"],o(("> "if j else "")+y,G),i if j else b);s=("Take the tracking arrow down"if j else a0)+(""if e.local else bh)
						if s!=r["tip"]:r["tip"]=s;L(r["catch"],s)
					self._show(r,True)
			def sender(self,e):
				if e.who=="You"or not Kit.streamer:return e.who
				return Kit.veil("name",e.who,Kit.checksum(e.who.lower().encode("utf-8")))
			def _show(self,r,on,only_first=False):
				a=("first"if only_first else on)
				if r["vis"]==a:return
				r["vis"]=a;b=r["labels"]+[r["where"],r["catch"]]
				for j,c in enumerate(b):ao(c,"IsVisible",on and(not only_first or j==0))
		class PingApp(object):
			def __init__(self):self.mouse=self.gesture=self.guide=self.bridge=self.bridge_error=self.conn=None;self.aim=self.status_label=self.last_pos=None;self.guide_labels,self.recent_pings={},{};self.bridge_tried=self._shut=False;self.next_link_check=self.last_pos_sent=self.next_pos_read=0;self.last_ping_sent=self.last_auto_sent=0;self.recent_order=collections.deque();self.settings=Settings();self.display=PingDisplay();self.pending,self.jobs,self.outbox,self.inbox,self.hooked=[],[],[],[],[];self.status_text,self.status_w="",300;self.history=HistoryWindow(self)
			def set_status(self,text,also_journal=True):
				self.status_text=text
				if self.status_label is not None:h(self.status_label,o(text,self.status_w))
				if also_journal:s(ae(text))
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
					except Exception as e:self.bridge=None;self.bridge_error=am(e)
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
				if a-self.last_ping_sent<aP:return
				self.last_ping_sent=a;self._send(x,y,m,t)
			def send_auto(self,x,y,m,t,who=None):
				a=time.time()
				if a-self.last_auto_sent<aP:return False
				self.last_auto_sent=a;self._send(x,y,m,t,who=who,auto=True);return True
			def _send(self,x,y,m,t,who=None,auto=False):
				self.display.show("You",x,y,m,t,local=True,who=who,auto=auto)
				if self.conn and self.conn.ready:
					if self.conn.server_relays_ping:self.outbox.append(af(51,struct.pack("<HHBB",x&65535,y&65535,m&255,t&255)))
					a=ba(x,y,m,t)
					if a:self.outbox.append(a)
					self.outbox.append(aW(x,y))
				else:b="Not connected: only you can see that ping.";self.set_status(b,also_journal=not auto or self.status_text!=b)
			AIM_SECONDS=10
			def target_ping(self,t):
				s("target a spot for %s (yourself: where you stand)."%v(t));self.aim=None;b=Picker._tm()
				if b is not None:
					a={"t":t,"fired":False,"spot":None,"d":None,"tm":b,"until":time.time()+self.AIM_SECONDS}
					def c(obj,aim=a):aim["spot"]=bd(obj);aim["fired"]=True
					with Kit.quiet:from System import Action;a["d"]=Action[object](c);b.SetTargeting(a["d"],Picker.CURSOR_TARGET,Picker.neutral);self.aim=a;HOST.claim_cursor("pings",self.AIM_SECONDS);return
				self.jobs.append(("aim",t))
			def poll_aim(self):
				a=self.aim
				if a is None:return
				if not a["fired"]:
					b=bool(a["tm"].IsCurrentTargetingAction(a["d"]))
					if b and time.time()<a["until"]:return
					self.aim=None;ah("pings")
					if b:a["tm"].CancelTarget()
					return
				self.aim=None;ah("pings");self.aimed(a["t"],a["spot"])
			def aimed(self,t,spot):
				if spot is None:return
				x,y=spot
				if x<=0 or y<=0:return
				self.send_ping(x,y,int(API.GetMap()),t)
			def drop_aim(self):
				a,self.aim=self.aim,None;ah("pings")
				if a is None or a["fired"]:return
				b=a["tm"]
				def c():
					if b.IsCurrentTargetingAction(a["d"]):b.CancelTarget()
				safe(lambda:aC(c,fallback=False))
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
					if a-self.conn.last_sent>20:self.outbox.append(af(254))
					return
				if((b!=self.last_pos and a-self.last_pos_sent>=1.)or a-self.last_pos_sent>=10):c=(4 if p.IsDead else 1 if p.IsPoisoned else 2 if p.IsYellowHits else 3 if p.IsParalyzed else 5 if p.IsHidden else 0);d=(int(p.Hits),int(p.Stamina),int(p.Mana),int(p.HitsMax),int(p.StaminaMax),int(p.ManaMax));self.outbox.append(bb(b,d,c,0xFFFFD700));self.last_pos,self.last_pos_sent=b,a
			def handle(self,ev):
				a=ev[0]
				if a=="status":self.set_status(ev[1],also_journal=ev[2])
				elif a=="ping":self.show_once(*ev[1:])
				elif a=="alert":
					d,b,x,y=ev;c=a9(x,y)
					if c:self.show_once(b,*c)
					elif not self.seen_recently(b,x,y):self.show_once(b,x,y,int(API.GetMap()),ac)
				elif a=="message":s("map server: "+ev[1])
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
					if b[0]=="open_setup":aw("pings")
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
				except Exception as e:self.mouse=None;s("mouse-wheel pings unavailable (%s): use the ping buttons or hotkeys."%am(e))
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
					g,self.gesture=self.gesture,None;self.close_guide();t=aV.get(g["dir"])
					if g["tile"]is not None and t is not None:self.send_ping(g["tile"][0],g["tile"][1],g["map"],t)
			def show_guide(self,center):
				self.close_guide();w,h=180,104;a=G.CreateGump(False,False);d=Kit.render_scale()or 1.;g,j=int(round(center[0]/d)),int(round(center[1]/d));Kit.place(a,g-w//2,j-h//2,w,h);Kit.add_window_frame(a,w,h,corners=False);I(a,6,6,w-12,h-12)
				for e,(k,l)in(("up",(58,9)),("right",(110,43)),("down",(58,77)),("left",(11,43))):t=aV[e];c=G.CreateGumpLabel(v(t),b);c.SetRect(k,l,70,18);a.Add(c);self.guide_labels[e]=(c,t)
				f=G.CreateGumpLabel("+",i);f.SetRect(w//2-3,h//2-9,10,18);a.Add(f);G.AddGump(a);SNAP.skip_gump(a);self.guide=a
			def update_guide(self,a):
				for d,(b,t)in self.guide_labels.items():b.Text="["+v(t)+"]"if d==a else v(t);b.Hue=aa[t][1]if d==a else 946
			def close_guide(self):Kit.dispose(self.guide);self.guide,self.guide_labels=None,{}
			def register_hotkeys(self):
				self.unregister_hotkeys()
				for c,a in E.items():
					if a:
						t=aL[c];d="%s ping"%v(t);b=HOST.hotkey_on(a,an,self._queue_ping(t),d)
						if b is False:s("couldn't set the %s hotkey (%s isn't a key)."%(v(t),a),A)
						if b is not False:self.hooked.append(a)
			def unregister_hotkeys(self):
				for a in self.hooked:HOST.hotkey_off(a,an)
				self.hooked=[]
			def shutdown(self):
				if self._shut:return
				self._shut=True;self.unregister_hotkeys();self.drop_aim();self.close_guide();safe(self.history.shutdown);safe(self.display.clear)
				if self.conn:self.conn.close()
			def start(self):self.init_mouse();self.register_hotkeys();self.history.start();s("on; ping buttons are on the World Map settings page.",D);self.choose_link();self.next_link_check=time.time()+5
		def aG(action):
			if l["app"]is not None:l["app"].pending.append(action)
		a={"f":None};a1,a2,bj=116,160,70;bk="Send a %s ping on the spot, item or person you target";bl="Key for a %s ping, like CTRL+1, F9 or SHIFT+F2 (blank = none)";bm={"host":"Map server address (host name or IP)","port":"Map server port (default %d)"%aH,"user":"Your map server login name","pass":"Map server password; saved in plain text on this PC, like Enhanced Map's"}
		def aN(action):
			def a(*a):aG(action)
			return a
		def bn(f,x,y):
			g,e,w=f.g,f.store,f.w;j=x+12
			for t in(ac,ag,GO,ap):m,r=aa[t][:2];n=m+"...";k(g,e,"ping%d"%t,P,j,y+28,n,bk%m,hue=r,on_click=aN(("target",t)));j+=35+u(n)+16
			k(g,e,"recon",P,x+12,y+58,"Reconnect","Reconnect to the map server",on_click=aN(("reconnect",)));p=x+12+35+u("Reconnect")+16;k(g,e,"history",Kit.ART_PAGE,p,y+58,"History","Open or close the window of recent pings, yours and others'",on_click=aN(("history",)));q=p+35+u("History")+16;d=l["app"]
			if d is not None:c(g,o("Wheel drag: up Look, right Danger, down Go, left Help",x+w-12-q),q,y+61,b)
			i=c(g,"",x+12,y+90,b);a["status"]=i
			if d is not None:d.status_label,d.status_w=i,w-24;h(i,o(d.status_text or "Starting",w-24))
		def bo(f,x,y):
			g,w=f.g,f.w;d=Settings();h=(w-36)//2;a["fields"]=m={}
			for i,(e,n,p)in enumerate((("host","Server address:",d.host),("port","Port:",str(d.port)),("user","Map username:",d.user),("pass","Map password:",d.password))):j=x+12+(i%2)*(h+12);l=y+30+(i//2)*48;c(g,n,j,l);m[e]=L(aj(g,p,j+2,l+20,h-8,numbers=e=="port"),bm[e])
			k(g,f.store,"save",Kit.ART_OK,x+12,y+128,"Save and connect","Save the four fields on this PC and connect");a["login"]=c(g,o("Saved on this PC in plain text (password shows while typing).",w-236),x+220,y+131,b)
		def bp(f,x,y):
			b=x+12;a["keys"]=e={}
			for k in aO:d=k.capitalize()+":";c(f.g,d,b,y+36);e[k]=L(aj(f.g,E[k],b+u(d)+8,y+33,84,numbers=False),bl%v(aL[k]));b+=u(d)+8+84+16
		a3={"lgap":8,"fw":44,"ugap":6};a4=(("SEND A PING  (or a hotkey or wheel drag)",(("custom",0,bn),),{"sh":a1,"top":0}),("MAP LOGIN  (when TazUO's Enhanced Map is off)",(("custom",0,bo),),{"sh":a2,"top":0}),("OPTIONS",(("check","sounds","Play a sound for each ping","For your pings and others'",{"stay":True}),("check","gesture","Ping with a mouse-wheel drag","Hold the wheel on a spot and drag: up Look here, right Danger!, down Go here, left Need help",{"dx":312}),("check","share","Show me on guildmates' maps","Sends your position (map login only; TazUO's Enhanced Map does its own)",{"stay":True}),("gap",28),("num","ping_secs","Ping stays:","How long a ping's marker and pulse stay","s",ad["ping_secs"][0],ad["ping_secs"][1],dict(a3,stay=True)),("num","drag","Drag distance:","Pixels the wheel drag must move to count","px",ad["drag"][0],ad["drag"][1],dict(a3,dx=312))),{"top":32}),("HOTKEYS  (blank = none)",(("custom",0,bp),),{"sh":bj,"top":0}))
		def bq(w):return a4
		br=Kit.Page(j,bq,ar)
		def bs(g,x,y,w):f=Kit.Form(g,x,y,w,j,a4);d=y+a1+a2+2*C;c(g,"Connection:",x+312,d+60);e=aK.index(j["connection"])if j["connection"]in aK else 0;b=G.CreateDropDown(190,[m[1]for m in aq],e);b.SetPos(x+414,d+56);g.Add(b);L(b,"TazUO's Enhanced Map while it is on, or the login above");a.update({"f":f,"dd":b,"seen_keys":dict(E),"next_read":0.})
		def a5(force=False):
			f=a["f"]
			if f is None:return
			if aD(f.store,"save"):bt()
			c=time.time()
			if not force and c<a["next_read"]:return
			a["next_read"]=c+.2;b=f.read();i=Kit.dd_index(a["dd"],-1)
			if 0<=i<len(aq):b["connection"]=aq[i][0]
			if b!=j:j.update(b);ar();aG(("options",))
			b={}
			for k,d in a["keys"].items():
				try:b[k]=_norm_key(d.Text)
				except Exception:b[k]=_norm_key(E[k])
			if force and b!=a["seen_keys"]:a["typed"]=a["seen_keys"]=b;E.update(b);ar();aG(("rehook",))
			elif b!=a.get("typed"):a["typed"],a["stable"]=b,0
			elif b!=a["seen_keys"]:
				a["stable"]=a.get("stable",0)+1
				if force or a["stable"]>=5:a["seen_keys"]=b;E.update(b);ar();aG(("rehook",))
		def bt():
			f=a["fields"]
			try:d=f["host"].Text.strip();j=f["port"].Text.strip();e=f["user"].Text.strip();g=f["pass"].Text
			except Exception:return
			try:c=int(j)
			except ValueError:c=0
			if not d or not e or not g or not(0<c<65536):h(a["login"],"Fill in all four fields (the port is a number)",A);return
			b=Settings();b.host,b.port,b.user,b.password=d,c,e,g;b.save();h(a["login"],"Saved",D);i=l["app"]
			if i is not None:s=i.settings;s.host,s.port,s.user,s.password=d,c,e,g;i.pending.append(("save_setup",))
		def bu():
			a5(True);b=l["app"]
			if b is not None and b.status_label is a.get("status"):b.status_label=None
			a.update({"f":None,"dd":None,"status":None,"keys":None,"fields":None,"login":None})
		def bv(x,y,m=None,kind="danger",who=None):
			a=l["app"]
			if a is None or a._shut:return False
			if m is None:m=API.GetMap()
			return a.send_auto(int(x),int(y),int(m),aL.get(kind,ag),who)
		a7()
		def bw():l["app"]=PingApp();l["app"].start();aU.service("pings.send",bv)
		def bx():
			if l["app"]is not None:l["app"].step()
		def by():
			if l["app"]is not None:l["app"].thread_step()
		def bz():
			a=l["app"]
			if a is None:return.05
			if a.gesture is not None:return.02
			if a.aim is not None or a.pending or a.inbox or a.jobs or a.outbox:return.05
			return.1
		def bA():
			aU.close();a,l["app"]=l["app"],None
			if a is not None:a.shutdown()
		return{"start":bw,"tick":bx,"stop":bA,"client_tick":True,"config_height":br.height,"build_config":bs,"poll_config":a5,"config_closed":bu,"thread_tick":by,"interval":bz}
	def aV():
		Z="corpserun";t="Corpse";ar="CorpseRun_settings";aQ="CorpseRun_pos";at="CorpseRun_min";ab="CorpseRun_corpse";v=0x434F5250;aR=8198;au,av=3786,3794;aw=15;ax=45;L,N=1,120;ay=60;az=120.;aA="corpserun.decay";aB=20.;aS=(400,401,605,606,666,667);aC=24;aD=1.;ad=2;aT=.25;aU=10.;x=.7;aE=2;aF=250;aV=("must wait to perform another action",);aW,aX=8251,8269;aG=15.;W=420;aH,aY=280,46;aZ=128;ah=F+30+C+aZ+F;e={"arrow":True,"restore":True,"ping":False,"decay":aw,"bones":ax};bv=dict(e);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"body":0,"body_at":0.,"note_until":0.,"name":"","drawn":None,"drawn_c":None,"unnamed":False,"hooked":False,"find_at":0.};y={"g":None,"c":{},"store":({},{})};ai={};aI,aj,l=R(a,t);aJ={"decay":(L,N),"bones":(L,N)}
		def a_():
			am(ar,";",e,aJ)
			if(e["decay"],e["bones"])==(7,7):e["decay"],e["bones"]=aw,ax
		def aK():an(ar,";",e,("arrow","restore","ping","decay","bones"),aJ)
		def a0():
			p=J(ab).split("|")
			if len(p)<8 or p[0]!="1":return
			try:return{"serial":int(p[1]),"x":int(p[2]),"y":int(p[3]),"facet":int(p[4]),"died":float(p[5]),"body":int(p[6]),"spot":p[7]=="1","exact":len(p)<9 or p[8]!="0","name":p[9]if len(p)>9 else ""}
			except ValueError:return
		def r():
			r=a["rec"]
			if r is None:H(ab,"");return
			H(ab,"1|%d|%d|%d|%d|%.0f|%d|%d|%d|%s"%(r["serial"],r["x"],r["y"],r["facet"],r["died"],r["body"],1 if r["spot"]else 0,1 if r["exact"]else 0,r["name"].replace("|","")))
		def g(text,secs=6.,spot=None):a["note"]=text if spot is None else text.replace("%d, %d"%spot,M(*spot));a["note_until"]=time.time()+secs;a["lbl_at"]=0.;l(ae(text))
		def Q(now):
			r=a["rec"]
			if r is None:return 0.
			if r["died"]>now:r["died"]=now
			return 60.*(e["decay"]+e["bones"])-(now-r["died"])
		def S(secs):secs=max(0,int(secs));return "%d:%02d"%(secs//60,secs%60)
		n=Kit.find_item;aL=Kit.held_item
		def aM():return bool(HOST.cursor_busy(Z))or bool(API.HasTarget())
		def a1(it):
			if aW<=int(it.Graphic)<=aX:return True
			d=it.GetItemData();return d is not None and int(d.Layer)in(11,16)
		def a2(it):
			d=it.GetItemData();w=int(d.Weight)if d is not None else 0;a=(0 if w>=255 else w)*max(1,int(it.Amount or 1))
			if it.IsContainer:
				for x in API.ItemsInContainer(int(it.Serial),True)or():
					d=x.GetItemData();b=int(d.Weight)if d is not None else 0
					if b<255:a+=b*max(1,int(x.Amount or 1))
			return a
		def ak():
			z=T(p,a,W,ah);w,j=z if z else(W,ah);g,h,f=p.begin(w,j)
			if not a["minimized"]:p.frame(g);M=F;l=w-2*M;d=M+30+C;I(g,M,d,l,j-d-M,"YOUR CORPSE  (where, how long it lasts)");f["where"]=c(g,"",M+12,d+28,B);f["decay"]=c(g,"",M+12,d+48,b);f["info"]=c(g,"",M+12,d+68,b);i=d+92;e=M+10;f["go"]=k(g,h,"go",P,e,i,"Get my things","Move your things from your corpse to your backpack one by one (stand beside it; click again to stop)",on_click=aj("go"));e+=35+max(u("Get my things"),u("Stop"))+14;k(g,h,"help",P,e,i,"Ping for help","Send your guild a Need help ping on your corpse (needs World Map > Map Pings)",on_click=aj("help"));e+=35+u("Ping for help")+14;k(g,h,"forget",O,e,i,"Forget","Forget this corpse and take its arrow down",on_click=aj("forget"))
			p.end(g);a["lbl_at"]=0.
		p=Kit.Window(Z,t,a,y,ak,aQ,at,(220,220),(aH,aY),3786,aI,lock=True,clear={"c":{}})
		def a3():
			if not a["minimized"]and not a["docked"]:return
			a["minimized"],a["docked"]=False,False;U(Z);Y(at,False);ak()
		def a4(me,now,n):
			r=a["rec"];j=a["job"]
			if r is None:o=bool(a["was_dead"]);c=a["note"]if a["note"]and now<a["note_until"]else("Find a healer or a resurrection."if o else "When you die, this window shows the way back.");return("No corpse to find.",B,"",b,c,t+": none")
			d=Q(now);p,q=int(me.X),int(me.Y)
			if not r["spot"]:g,f="Looking for your corpse round you","looking"
			elif n!=r["facet"]:g="On %s, at %s"%(E(r["facet"]),M(r["x"],r["y"]));f=E(r["facet"])
			else:h=K(r["x"]-p,r["y"]-q);g="%s%s, at %s"%(h[0].upper(),h[1:],M(r["x"],r["y"]));f=h
			m=60.*e["bones"];i=""if r["exact"]else "at most "
			if d>m:k="Bones in %s%s, gone in %s%s"%(i,S(d-m),i,S(d))
			elif d>0:k=("Bones %s; gone in %s%s"%("now"if r["exact"]else "soon",i,S(d)))
			else:k="Should have decayed by now"
			s=A if d<=ay else b
			if a["note"]and now<a["note_until"]:c=a["note"]
			elif j is not None:
				if j["phase"]=="open":c="Opening your corpse"
				else:c="Moving %d / %d"%(min(j["i"],len(j["plan"])),len(j["plan"]))
			else:
				l=(("Died %s ago."%Kit.ago(now-r["died"]))if r["exact"]else "Found as a ghost.")
				if not r["serial"]and a["unnamed"]:c="Waiting for the corpse's name: click it once."
				elif a["was_dead"]:c=l+" Be resurrected, then click Get my things."
				elif r["serial"]and r["spot"]:c=l+" Stand by it and click Get my things."
				else:c=l+" Not seen there yet."
			f="%s  %s"%(f,S(d))if d>0 else f;return g,B,k,s,c,"%s: %s"%(t,f)
		def a5(me,now,p,force=False):
			q=y["g"]
			if q is None or(a["minimized"]and a["docked"]):return
			if not force and now<a["lbl_at"]:return
			a["lbl_at"]=now+.5;e,f,g,j,k,l=a4(me,now,p);c=y["c"]
			if a["minimized"]:m=A if a["rec"]is not None and Q(now)<=ay else b;d=(l,m)
			else:d=(e,f,g,j,k,a["job"]is not None)
			if d==a["drawn"]and c is a["drawn_c"]:return
			a["drawn"],a["drawn_c"]=d,c
			if a["minimized"]:
				n=c.get("status")
				if n is not None:h(n,o(l,aH-90),m)
				return
			for r,s,t in(("where",e,f),("decay",g,j),("info",k,b)):h(c[r],o(s,W-2*F-24),t)
			h(c["go"],"Stop"if a["job"]is not None else "Get my things",i if a["job"]is not None else B)
		def a6(me,c):
			r=a["rec"];b=None
			if e["arrow"]and r is not None and r["spot"]and c==r["facet"]:
				if max(abs(int(me.X)-r["x"]),abs(int(me.Y)-r["y"]))>ad:b=(r["x"],r["y"])
			if b==a["arrow"]:return
			if b is None:X(a,v)
			else:API.TrackingArrow(b[0],b[1],v);a["arrow"]=b
		def ao(me,now,at_start=False):
			if a["job"]is not None:m("you died")
			x,y,b=int(me.X),int(me.Y),int(API.GetMap());a["name"]=str(me.Name or "");a["rec"]={"serial":0,"x":x,"y":y,"facet":b,"died":now,"body":a["body"],"spot":not at_start,"exact":not at_start,"name":a["name"]};a["seek_until"],a["seek_at"]=now+aB,now;a["gone_since"],a["warned"],a["unnamed"]=None,False,False;a["refused"]=set();r()
			if at_start:l("you are a ghost: looking for your corpse round you.")
			else:
				l("you died at %d, %d (%s). Bones in %s, gone %s later."%(x,y,E(b),z(e["decay"],"minute"),z(e["bones"],"minute")),A)
				if e["ping"]:a["ping"]=(x,y,b,now+aG)
			if e["restore"]:a3()
		a7=("a corpse of ","corpse of ","the remains of ","remains of ")
		def ap():r=a["rec"];return((r["name"]if r is not None and r["name"]else a["name"])or "").strip().lower()
		def aN(it,graphic,e):
			r=a["rec"];d=r["body"]if r is not None else 0;b=int(it.Amount or 0)
			if d and b and b!=d:return 0
			f=au<=graphic<=av
			if f and(not b or(not d and b not in aS)):return 0
			n=(str(it.Name or "")or str(it.NameAndProps(False)or "")).strip().lower();c=None
			for p in a7:
				if n.startswith(p):c=n[len(p):].strip();break
			if c is None:
				if not n or n in("corpse","a corpse","bones","remains")or f:return 1
				c=n
			if not e:return 1
			return 2 if c==e else 0
		def aO(items,g,h,lim,c,i):
			for a,j in items:
				s,e,f=int(a.Serial),int(a.X),int(a.Y);d=max(abs(e-g),abs(f-h))
				if d>lim:continue
				m=aN(a,j,i)
				if m==1:c[1]=True
				if m!=2:continue
				k=(d,s,e,f);b=c[0]
				if b is None or d<b[0]or(d==b[0]and s>b[1]):c[0]=k
		def a8(me):
			r=a["rec"];d=ap();e,f,h=(r["x"],r["y"],3)if r["spot"]else(int(me.X),int(me.Y),aC);b=[None,False];i,j=[],[]
			for c in API.GetItemsOnGround(aC)or():
				g=int(c.Graphic)
				if g==aR:i.append((c,g))
				elif au<=g<=av:j.append((c,g))
			aO(i,e,f,h,b,d)
			if b[0]is None:aO(j,e,f,h,b,d)
			return(None if b[0]is None else b[0][1:]),b[1]
		def s(why=None):
			if a["job"]is not None:m(None)
			a["rec"]=a["ping"]=a["gone_since"]=None;a["unnamed"]=False;a["refused"]=set();X(a,v);r()
			if why:l(why)
			a["lbl_at"]=0.
		def a9(me,now,d):
			b=a["rec"];e=Q(now);h=max(abs(int(me.X)-b["x"]),abs(int(me.Y)-b["y"]))
			if not b["serial"]:
				m=b["spot"]and d==b["facet"]and h<=12;o=not b["spot"]and a["unnamed"];i=now<a["seek_until"]
				if(i and now>=a["seek_at"])or(not i and(m or o)and now>=a["look_at"]):
					a["seek_at"]=now+.5;a["look_at"]=now+1.;a["find_at"]=now;j,k=a8(me)
					if j is not None:
						b["serial"],b["x"],b["y"]=j;a["unnamed"]=False
						if not b["name"]:b["name"]=ap()
						if not b["spot"]:b["spot"]=True;l("found your corpse at %d, %d."%(b["x"],b["y"]))
						r();a["lbl_at"]=0.
					elif k!=a["unnamed"]:a["unnamed"]=k;a["lbl_at"]=0.
				if(not b["serial"]and not b["spot"]and now>=a["seek_until"]and not a["unnamed"]):s("your corpse isn't in view (it was left before %s started)."%t);return
			elif now>=a["item_at"]or a["item_at"]-now>aD:
				a["item_at"]=now+aD;c=n(b["serial"])
				if c is not None:
					a["gone_since"]=None;f,g=int(c.X),int(c.Y)
					if(f or g)and(f,g)!=(b["x"],b["y"])and not int(c.Container or 0):b["x"],b["y"]=f,g;r()
				elif d==b["facet"]and a["job"]is None and h<=12:
					if a["gone_since"]is None:a["gone_since"]=now
					elif now-a["gone_since"]>=6.:s("your corpse isn't at %d, %d any more (decayed or looted)."%(b["x"],b["y"]));return
				else:a["gone_since"]=None
			if e<=60 and not a["warned"]and e>0:a["warned"]=True;p=K(b["x"]-int(me.X),b["y"]-int(me.Y))if d==b["facet"]else "on "+E(b["facet"]);af(aA,"Corpse decays in under a minute (%s)"%p,"warn")
			if e<=-az and n(b["serial"])is None:s("your corpse has decayed.")
		def ba(now):
			p=a["ping"]
			if p is None:return
			x,y,m,c=p;b=HOST.services.get("pings.send")
			if b is None or now>c:
				a["ping"]=None
				if b is None:l("World Map > Map Pings is off, so no Need help ping was sent.")
				return
			try:
				if b(x,y,m=m,kind="help"):a["ping"]=None;l("Need help ping sent on your corpse.")
			except Exception:a["ping"]=None
		def bb(me,now):
			r=a["rec"]
			if a["job"]is not None:return
			if r is None:g("No corpse remembered.");return
			if bool(a["was_dead"]):g("You are still a ghost: get resurrected first.");return
			c=(r["x"],r["y"])
			if not r["serial"]:g("Your corpse hasn't been seen yet: go to %d, %d."%c,spot=c);return
			b=n(r["serial"])
			if b is None:g("Your corpse isn't in view yet (%d, %d)."%c,spot=c);return
			d=aN(b,int(b.Graphic),ap())
			if d==1:g("Waiting for the corpse's name: click it once.");return
			if d!=2:g("That corpse isn't yours.");return
			e,f=int(b.X)-int(me.X),int(b.Y)-int(me.Y)
			if max(abs(e),abs(f))>ad:g("Walk up to your corpse first (%s)."%K(e,f));return
			h=int(API.Backpack or 0)
			if not h:g("No backpack to put things in.");return
			if aM():g("A target cursor is up: finish or cancel it first.");return
			if aL():g("You are holding an item: put it down first.");return
			a["job"]={"phase":"open","corpse":r["serial"],"pack":h,"at":now+1.,"until":now+3.,"plan":[],"i":0,"tried":set(),"waits":{},"move":None,"check":None,"sent_at":0.,"last":0,"rechecks":0,"hold":0.,"moved":0,"refused":0,"streak":0,"why":None,"replans":0};API.UseObject(r["serial"]);a["note"]="";a["lbl_at"]=0.
		def aq(j):
			b=[]
			for c in API.ItemsInContainer(j["corpse"],False)or():
				if len(b)>=aF:break
				s=int(c.Serial)
				if s not in j["tried"]and s not in a["refused"]and not a1(c):b.append(s)
			return b
		def bc(me,now):
			j=a["job"]
			if j["why"]:m(j["why"]);return
			if j["move"]is not None:return
			if a["was_dead"]:m("you died");return
			d=n(j["corpse"])
			if d is None:m("your corpse is gone from view");return
			if max(abs(int(d.X)-int(me.X)),abs(int(d.Y)-int(me.Y)))>ad:m("you walked away from your corpse");return
			if j["check"]is not None and(now<j["at"]or not bd(j,now)):return
			if j["phase"]=="open":
				if now<j["at"]:return
				b=aq(j)
				if not b and now<j["until"]:return
				j["plan"],j["i"],j["phase"]=b,0,"move"
				if not b:aP();return
			if now<j["hold"]:return
			if aM():m("a target cursor is up");return
			h=aL()
			if h and h!=j["last"]:m("you picked something up");return
			b=j["plan"]
			while j["i"]<len(b):
				s=b[j["i"]];j["i"]+=1
				if s in j["tried"]:continue
				x=n(s)
				if x is None or int(x.Container or 0)!=j["corpse"]:continue
				c,e=int(me.WeightMax or 0),int(me.Weight or 0)
				if c>0 and(e>=c or e+a2(x)>c):m("the next item would put you over your weight limit (%d / %d stones)"%(e,c));return
				j["tried"].add(s);j["move"]=s;return
			if j["replans"]<2:
				j["replans"]+=1;f=aq(j)
				if f:j["plan"],j["i"]=f,0;return
			aP()
		def bd(j,now):
			s=j["check"];b=n(s);c=int(b.Container or 0)if b is not None else None
			if c is None and j["rechecks"]<aE:j["rechecks"]+=1;j["at"]=now+x*.5;return False
			if c!=j["corpse"]:j["moved"]+=1;j["streak"]=j["rechecks"]=0;j["check"]=None;return True
			if(Journal.find(j["sent_at"],aV)is not None and j["waits"].get(s,0)<2):j["waits"][s]=j["waits"].get(s,0)+1;j["tried"].discard(s);j["i"]=max(0,j["i"]-1);j["check"]=None;j["rechecks"]=0;j["hold"]=now+x;return False
			if j["rechecks"]<aE:j["rechecks"]+=1;j["at"]=now+x*.5;return False
			j["check"]=None;j["rechecks"]=0;j["refused"]+=1;j["streak"]+=1
			if len(a["refused"])<aF:a["refused"].add(s)
			if j["streak"]>=3:m("%d moves in a row were refused"%j["streak"]);return False
			return True
		def be():
			j=a["job"]
			if j is None or j["move"]is None or a["shutting"]:return
			b=j["move"];j["move"]=None
			try:API.MoveItem(b,j["pack"])
			except Exception as c:j["why"]="a move failed (%s)"%c;return
			j["check"]=b;j["last"]=b;j["sent_at"]=time.time();j["at"]=j["sent_at"]+x
		def aP():
			j,a["job"]=a["job"],None
			if j is None:return
			c=[]
			if n(j["corpse"])is not None:c=aq({"corpse":j["corpse"],"tried":set()})
			d=len(a["refused"])
			if j["moved"]==0 and not j["refused"]and not c:s("nothing left in your corpse%s."%((" but %s the server refused (take %s by hand)"%(z(d,"item"),"it"if d==1 else "them"))if d else ""));return
			e="%s back in your backpack"%z(j["moved"],"item")
			if j["refused"]:e+=", %d refused (left in your corpse: take %s by hand)"%(j["refused"],"it"if j["refused"]==1 else "them")
			if c:l("%s; %d still in your corpse (click Get my things again)."%(e,len(c)),A if j["refused"]else b);a["lbl_at"]=0.;return
			s(None);l("%s. Re-dress when you are ready."%e,A if j["refused"]else D)
		def m(why=None,user=False):
			j,a["job"]=a["job"],None
			if j is None:return
			if user:l("stopped (%d moved)."%j["moved"])
			elif why:l("stopped: %s (%d moved)."%(why,j["moved"]),A)
			a["lbl_at"]=0.
		def bf(me,now):
			if a["job"]is not None:m(None,user=True)
			elif me is not None:bb(me,now)
		def bg(me,now):
			r=a["rec"]
			if r is None or not r["spot"]:g("No corpse to ping.")
			elif HOST.services.get("pings.send")is None:g("World Map > Map Pings is off: turn it on to send pings.")
			else:a["ping"]=(r["x"],r["y"],r["facet"],now+aG)
		def bh(me,now):
			if a["rec"]is None:g("No corpse remembered.")
			else:s("forgot your corpse.")
		bi={"go":bf,"help":bg,"forget":bh};bj=("One item every %.1f s; stops on Stop, a target cursor, picking something up, walking away or going over your weight limit."%x)
		def bk(w):a="Corpse to bones:";return(("WHEN YOU DIE",(("check","arrow","Point the tracking arrow at your corpse","Its own arrow (others are left alone); hidden when you stand beside it"),("check","restore","Open the Corpse window when you die, even minimized or folded","It comes back full size"),("check","ping","Send a Need help map ping on your corpse when you die","Your guild sees where you died (needs World Map > Map Pings); off at first, as it shows where you are")),{"pad":4}),("DECAY  (minutes; the shard's times)",(("num","decay",a,"Minutes from death until bones",None,L,N,{"stay":True}),("num","bones","Bones gone after:","Minutes the bones (with your things) last",None,L,N,{"dx":u(a)+86})),{"ldy":4,"fw":40,"pad":8}),("GET MY THINGS  (one item at a time)",[("note",d)for d in Kit.wrap(bj,w-28)]),ac("corpse"))
		def bl(f,new):
			b=time.time()
			for k in("decay","bones"):
				try:a=str(f.c[k].Text or "").strip()
				except Exception:continue
				t=ai.get(k)
				if t is None or t[0]!=a:ai[k]=(a,b)
				if not G.force and(t is None or t[0]!=a or b-t[1]<1.):new[k]=e[k]
		def bm(b,new):
			if(new["decay"],new["bones"])!=(b["decay"],b["bones"]):a["warned"]=False
			a["lbl_at"]=0.
			if not new["arrow"]:X(a,v)
		G=Kit.Page(e,bk,aK,bm,adjust=bl,final=True)
		def bn():G.closed();ai.clear()
		def bo(*c):
			r=a["rec"]
			if r is None or r["serial"]or a["shutting"]:return
			b=a["find_at"]+aT;a["seek_at"]=min(a["seek_at"],b);a["look_at"]=min(a["look_at"],b)
		def bp(*b):
			if a["shutting"]:return
			a["died"]=True;HOST.poke("worldmap.corpse",False)
		def bq(d):
			for k in("body_at","seek_until","seek_at","look_at","item_at","lbl_at","note_until","find_at","died_at"):a[k]=a[k]+d
			if a["gone_since"]is not None:a["gone_since"]+=d
			p=a["ping"]
			if p is not None:a["ping"]=(p[0],p[1],p[2],p[3]+d)
			j=a["job"]
			if j is not None:
				for k in("at","until","sent_at","hold"):j[k]+=d
			b=a["rec"]
			if b is not None:b["died"]+=d;r()
		def br():
			a.update({"shutting":False,"docked":False,"queue":[],"job":None,"arrow":None,"refused":set(),"ping":None,"was_dead":None,"seek_until":0.,"seek_at":0.,"look_at":0.,"gone_since":None,"item_at":0.,"lbl_at":0.,"note":"","last_now":None,"atlas":False,"unnamed":False,"died":False,"died_at":0.,"minimized":p.start_min()});a_();a["rec"]=a0();a["warned"]=False
			if a["rec"]is not None and Q(time.time())<=-az:a["rec"]=None;r()
			if a["rec"]is not None and not a["rec"]["spot"]:a["seek_until"]=time.time()+aB
			ag(aA,"Corpse about to decay",490);ak();p.dock(fit=True,min=(W,ah));al(a,"hooked",("OnCorpseCreated",bo),("OnPlayerDeath",bp))
		def bs():
			if y["g"]is None:return
			if V(y):return
			b=time.time();g,a["last_now"]=a["last_now"],b
			if g is not None and b<g-2.:bq(b-g)
			c=HOST.me()
			while a["queue"]:
				i=a["queue"].pop(0)
				if not p.action(i):bi[i](c,b)
			if c is None:return
			d=bool(c.IsDead);f=a["was_dead"];a["was_dead"]=d;j=a["died"];a["died"]=False
			if j and not f:ao(c,b);a["died_at"]=0. if d else b
			elif f is None:
				if d and a["rec"]is None:ao(c,b,at_start=True)
			elif d and not f:
				if not 0.<=b-a["died_at"]<=aU:ao(c,b)
				a["died_at"]=0.
			elif f and not d and a["rec"]is not None:
				r=a["rec"]
				if r["spot"]:l("you are alive. Your corpse is %s: click Get my things beside it."%K(r["x"]-int(c.X),r["y"]-int(c.Y)),D)
				a["lbl_at"]=0.
			if not d and b>=a["body_at"]:a["body_at"]=b+2.;a["body"]=int(c.Graphic);a["name"]=str(c.Name or "")or a["name"]
			if not a["name"]:a["name"]=str(c.Name or "")
			h=int(API.GetMap())if a["rec"]is not None or a["arrow"]is not None else None
			if a["rec"]is not None:a9(c,b,h)
			if a["job"]is not None:bc(c,b);be()
			if a["ping"]is not None:ba(b)
			if a["rec"]is not None or a["arrow"]is not None:a6(c,h)
			r=a["rec"];e=(r["x"],r["y"],r["facet"])if r is not None and r["spot"]else None
			if e!=a["atlas"]:a["atlas"]=e;q.set("corpse",{}if e is None else{aa("Your corpse"):(e[0],e[1],e[2],"white")})
			a5(c,b,h)
		def bt():return.1 if a["job"]is not None else.25
		def bu():a["shutting"]=True;a["job"]=a["ping"]=None;X(a,v);aK();aI.close()
		return{"start":br,"tick":bs,"stop":bu,"client_tick":True,"config_height":G.height,"build_config":G.build,"poll_config":G.poll,"config_closed":bn,"interval":bt}
	def aW():
		aB="treasure";ad="Treasure Maps";aC="TreasureHunter_settings";a2="TreasureHunter_pos";a3="TreasureHunter_min";aD="TreasureHunter_maps";aE,a4=320,46;ap=8;v=24;aF=0x54524541;aq=(5355,5356);aG=("youthful","plainly","expertly","adeptly","cleverly","deviously","ingeniously");aH=["Youthful"]+[bN.capitalize()+" drawn"for bN in aG[1:]];a5=["somewhere in "+bO.lower()for bO in ai];a6="you successfully decode a treasure map";a7="the treasure is marked by the red pin";a8="this treasure hunt has already been completed";a9=re.compile(r"believe this is somewhere near (\d+) and (\d+)");at=300.;aI=1.;Y=6.;aJ=.25;af=8.;aK=5.;aL=60;aM=6.;aN=.5;Z="Point the tracking arrow at this map's spot (again: back to the nearest map)";ba="Send the tracking arrow back to the nearest map's spot";bb="Point the tracking arrow at this map's spot (again: take it down)";bc="Send a Go here ping on this map's spot (needs World Map > Map Pings)";bd="No treasure maps in your pack: put one in and double-click it once.";aO="This treasure has been dug up";n={"auto":True,"undecoded":True,"done":False};bM=dict(n);d={"minimized":False,"shutting":False,"docked":False,"queue":[],"next_look":0.,"dirty":False,"next_save":0.,"list_ver":0,"me":(0,0,-1),"hooked":False,"tm_at":0.,"tm_serial":0,"hidden":0,"in_pack":frozenset()};j={};ab={};aP=5.;ag=[False];ah=set();A={};G={"g":None,"c":{},"store":({},{}),"rows":[]};JR={"rd":None};aQ,U,l=R(d,ad);W={"at":0.,"items":[]}
		def au(lvl):return aH[lvl]if 0<=lvl<len(aH)else "Treasure map"
		def be():am(aC,";",n)
		def aR():an(aC,";",n,("auto","undecoded","done"))
		def bf():
			j.clear();c=time.time()-60*86400
			for d in J(aD).split(";"):
				b=d.strip().split(",")
				if len(b)<7:continue
				try:s=int(b[0],16);a={"x":int(b[1]),"y":int(b[2]),"f":int(b[3]),"lvl":int(b[4]),"done":b[5]=="1","t":int(b[6]),"approx":len(b)>7 and b[7]=="1"}
				except ValueError:continue
				if s<=0 or a["x"]<=0 or a["y"]<=0 or a["t"]<c:continue
				j[s]=a
			aS()
		def aS():
			if len(j)>aL:
				a=sorted(j,key=lambda s:j[s]["t"])
				for b in a[:len(j)-aL]:del j[b]
		def aT():d["dirty"]=False;H(aD,";".join("%X,%d,%d,%d,%d,%d,%d,%d"%(e,a["x"],a["y"],a["f"],a["lvl"],1 if a["done"]else 0,a["t"],1 if a.get("approx")else 0)for e,a in sorted(j.items())))
		def bg(text):
			b=text.lower();c=b.split("\n",1)[0];a={"tm":"treasure map"in b,"lvl":-1,"dec":None,"f":-1,"done":"completed by"in b}
			for d,e in enumerate(aG):
				if e in c:a["lvl"]=d;break
			if a["tm"]:a["dec"]="tattered"not in c
			for f,t in enumerate(a5):
				if t in b:a["f"]=f;break
			return a
		def aU(serial,it,now=None):
			a=ab.get(serial)
			if now is not None and a is not None and now<a[2]<=now+aP:return a[1]
			if now is None:now=time.time()
			b=str(API.ItemNameAndProps(serial,False)or "");c=now+aP
			if not b.strip():
				c=0.;b=str(it.Name or "")
				if serial not in ah:
					ah.add(serial)
					if len(ah)>500:ah.clear()
					API.RequestOPLData([serial])
			if a is not None and a[0]==b:ab[serial]=(b,a[1],c);return a[1]
			d=bg(b)
			if len(ab)>300:ab.clear()
			ab[serial]=(b,d,c);return d
		def av(est,end,p,size):
			if None in(end,p,size):return est,None
			p,size=float(p),float(size)
			if size<=0 or p<0 or p>size:return est,None
			k=1.-p/at;a=None
			if abs(k)>=.001:
				c=p*end/at;d,e=(est-c)/k,(est+1-c)/k;a=int(math.floor((d+e)/2.))
				if not 0<end-a<=8192:a=None
			b=float(end-a)/size if a is not None and abs(k)>=.25 else None
			if abs(size-at)<.5:return est,b
			if a is None or abs(1.-(p+.5)/size)/abs(k)>2.:return None,b
			return int(a+(p+.5)*(end-a)/size),b
		def aV(est,end,p,size,scale=None):
			a=av(est,end,p,size)[0]
			if a is not None:return a,False
			if scale and None not in(end,p,size):return int(end-(float(size)-float(p)-.5)*scale),False
			return est,True
		def m(obj,name):
			v=Typing._get(obj,name)
			if v is None:return
			try:return int(v)
			except Exception:return
		def bh():
			Typing._find();a=Typing.uim
			if a is None:return
			b=Typing._get(None,"Gumps",a)
			if b is None:return
			n=0
			try:
				for g in b:
					if str(g.GetType().Name)!="MapGump":continue
					r=bi(g)
					if r is None:return
					n+=r
			except Exception:return
			return n
		def bi(g):
			a=m(g,"LocalSerial")
			if not a:return 0
			if Typing._get(g,"IsDisposed",default=False):return 0
			if A.get(a)is g:return 0
			k=Typing._get(g,"foundMapLoc")
			if k is None:return
			if not k:return 0
			f,h=m(g,"mapX"),m(g,"mapY")
			if f is None or h is None:return
			l,n,i=m(g,"mapEndX"),m(g,"mapEndY"),m(g,"mapFacet");b=Typing._get(g,"_hit");o=m(b,"Width")if b is not None else None;p=m(b,"Height")if b is not None else None;c=d=None;j=Typing._get(g,"_container")
			try:
				if j is not None and int(j.Count)>0:
					e=j[0];q,r=m(e,"Width"),m(e,"Height");s,t=m(e,"X"),m(e,"Y")
					if None not in(q,r,s,t):c,d=s-q-5,t-r
			except Exception:c=d=None
			if len(A)>50:A.clear()
			A[a]=g;u=av(f,l,c,o)[1];v=av(h,n,d,p)[1];x,w=aV(f,l,c,o,v);y,z=aV(h,n,d,p,u)
			if x is None or y is None or x<=0 or y<=0:return 0
			aW(a,x,y,i if i is not None and i>0 else-1,w or z);return 1
		def aW(serial,x,y,g,approx=False):
			h=API.FindItem(serial);e=aU(serial,h)if h is not None else{};i=time.time();m=0<=i-d["tm_at"]<=Y and(d["tm_serial"]==serial or(not d["tm_serial"]and i-d["tm_at"]<=1.5))
			if not(e.get("tm")or serial in j or m):return False
			f=g if g>=0 else e.get("f",-1)
			if f<0:f=int(API.GetMap())
			b=j.get(serial);c=e.get("lvl",-1)
			if c<0 and b is not None:c=b["lvl"]
			a={"x":int(x),"y":int(y),"f":int(f),"lvl":c,"done":bool(e.get("done")or(b is not None and b["done"])),"t":int(time.time()),"approx":bool(approx)};n=(b is not None and(b["x"],b["y"],b["f"])==(a["x"],a["y"],a["f"]));j[serial]=a;aS();d["dirty"]=True;d["next_scan"]=0.
			if not n:d["arrow_off"]=False;k,o,p=d["me"];q=(", "+K(a["x"]-k,a["y"]-o,"here"))if p==a["f"]and k>0 else "";l("%s map%s: dig at %s%d, %d in %s%s."%(au(c).lower(),(" (level %d)"%c)if c>=0 else "","about "if a["approx"]else "",a["x"],a["y"],E(a["f"]),q),D)
			return True
		def aw(now):d["look_until"]=now+Y;d["next_look"]=0.
		def bj(*a):
			if not d["active"]:return
			for b in a:
				try:s=int(b)
				except Exception:continue
				if s>0 and len(d["used"])<20:d["used"].append(s)
				return
		def bk():al(d,"hooked",("ObjectUsed",bj))
		def bl(now):
			b,d["used"]=d["used"],[]
			for s in b:
				a=API.FindItem(s)
				if a is not None and int(a.Graphic)in aq:d["last_map"]=(s,now);aw(now)
		def bm(now):
			c=JR["rd"]
			if c is None:return
			g=ad.lower()+":"
			for e in c.new():
				a=e.low
				if "somewhere near"in a:b=1
				elif a7 in a or a6 in a:b=2
				elif a8 in a:b=3
				else:continue
				if a.startswith(g):continue
				f=(e.name or "").strip().lower()
				if f and f!="system":continue
				if b==1:
					m=a9.search(a)
					if m:d["est"]=(int(m.group(1)),int(m.group(2)),now);aw(now)
				elif b==2:s,t=d["last_map"];d["tm_at"]=now;d["tm_serial"]=s if s and 0<=now-t<=af else 0;ag[0]=True;aw(now)
				else:
					s,t=d["last_map"];ag[0]=True
					if s and 0<=now-t<=af and s in j and not j[s]["done"]:j[s]["done"]=True;d["dirty"]=True;d["next_scan"]=0.
		def bn(now):
			if not(now<d["look_until"]<=now+Y+1.):
				if d["look_until"]>now+Y+1.:d["look_until"]=now+Y;return
				if d["est"]is not None:aX()
				if A:A.clear()
				return
			if now<d["next_look"]<=now+aJ:return
			d["next_look"]=now+aJ;n=bh()
			if n is None:
				a,b=d["est"],d["last_map"]
				if a is not None and b[0]and-2.<=a[2]-b[1]<=af:aX()
			elif n>0:d["est"]=None;d["look_until"]=min(d["look_until"],now+1.)
		def aX():
			x,y,a=d["est"];d["est"]=None;s,b=d["last_map"]
			if not s or not(-2.<=a-b<=af)or x<=0 or y<=0:return
			d["last_map"]=(0,0.);aW(s,x,y,-1)
		def aY(now):
			try:p=API.Player;i,k=int(p.X),int(p.Y);l=int(API.GetMap())
			except Exception:return
			d["me"]=(i,k,l)
			if not int(API.Backpack or 0):d["in_pack"]=None;return
			q=[y for y in HOST.pack_items(True,.5)if int(y.Graphic)in aq];r=bo(now);w=set([int(bN.Serial)for bN in r]);q.extend(r);c,f=[],set();g=0;t=int(time.time());x=None if ag[0]else time.time();ag[0]=False
			for u in q:
				s=int(u.Serial)
				if s in f:continue
				f.add(s)
				if len(c)>=100:continue
				b=aU(s,u,x);a=j.get(s)
				if not b["tm"]and a is None:continue
				m=b["lvl"]if b["lvl"]>=0 else(a["lvl"]if a else-1);h=bool(b["done"]or(a is not None and a["done"]))
				if a is not None:
					if b["f"]>=0 and a["f"]!=b["f"]:a["f"]=b["f"];d["dirty"]=True
					if m!=a["lvl"]or h!=a["done"]:a["lvl"],a["done"]=m,h;d["dirty"]=True
					if t-a["t"]>86400:a["t"]=t;d["dirty"]=True
				o=True if a is not None else b["dec"];e={"serial":s,"lvl":m,"dec":o,"done":h,"x":None,"y":None,"f":-1,"dist":None,"group":3,"bank":s in w}
				if a is not None:
					e["x"],e["y"],e["f"]=a["x"],a["y"],a["f"];e["approx"]=a.get("approx",False)
					if e["f"]==l:e["dist"]=max(abs(a["x"]-i),abs(a["y"]-k));e["dir"]=Kit.compass(a["x"]-i,a["y"]-k);e["group"]=0
					else:e["group"]=1
				elif o:e["group"]=2
				if h:
					e["group"]=4
					if not n["done"]:g+=1;continue
				elif not o and not n["undecoded"]:g+=1;continue
				e["where"],e["hue"],e["tip"]=bs(e,l)
				if e["bank"]:e["where"]="in the bank: "+e["where"]
				c.append(e)
			c.sort(key=bq);d["list"]=c;d["in_pack"]=f
			if d["pin"]and d["pin"]not in f:d["pin"]=0
			v=(tuple((bO["serial"],bO["lvl"],bO["dec"],bO["done"],bO["where"])for bO in c)+(g,));d["hidden"]=g
			if v!=d["list_sig"]:d["list_sig"]=v;d["list_ver"]+=1
		def bo(now):
			if now-W["at"]<5. and now>=W["at"]:return W["items"]
			b=int(API.Bank or 0);W["at"]=now;W["items"]=[]
			if b and bp(b):W["items"]=[a for a in list(API.ItemsInContainer(b,True)or[])[:2000]if int(a.Graphic)in aq]
			return W["items"]
		def bp(bank):
			with Kit.quiet:
				for g in Tz.windows(("ContainerGump","GridContainer")):
					if int(g.LocalSerial)==bank:return True
			return False
		def aZ(keep):
			a=set((int(f["x"]),int(f["y"]),int(f["f"]))for f in keep)
			for t in d["dig_tiles"]-a:API.RemoveMarkedTile(t[0],t[1],t[2])
			for t in a-d["dig_tiles"]:API.MarkTile(t[0],t[1],53,t[2])
			d["dig_tiles"]=a
		def bq(e):return(e["group"],e["dist"]if e["dist"]is not None else 0,e["lvl"],e["serial"])
		def br():
			a=[f for f in d["list"]if not(f["x"]is None or f["done"]or f["f"]<0)];b=tuple((g["serial"],g["x"],g["y"],g["f"],g["lvl"])for g in a)
			if b==d["atlas_sig"]:return
			d["atlas_sig"]=b;aZ(a);q.set("maps",{aa(("Dig L%d #%04X"%(p["lvl"],p["serial"]&65535))if p["lvl"]>=0 else("Dig #%04X"%(p["serial"]&65535))):(int(p["x"]),int(p["y"]),int(p["f"]),"yellow")for p in a})
		def bs(e,c):
			if e["x"]is not None:
				a=("about "if e.get("approx")else "")+M(e["x"],e["y"],"(%d, %d)")
				if e["done"]:return "dug up  "+a,b,aO
				if e["f"]==c:
					d=e["dist"]
					if d==0:return "here  "+a,D,Z
					return("%s %s  %s"%(z(d,"tile"),e["dir"],a),B,Z)
				return("in %s  %s"%(E(e["f"]),a),b,"This map's spot is in %s; you are in %s"%(E(e["f"]),E(c)))
			if e["done"]:return "dug up",b,aO
			if e["dec"]:return "open the map once to read its spot",b,"Double-click the map once to read it"
			if e["dec"]is None:return "open the map to read it",b,"Double-click the map to read it"
			return "not decoded yet",b,"Double-click the map to decode it (Cartography)"
		def ay(serial):return next((a for a in d["list"]if a["serial"]==serial),None)
		def bt():
			if d["arrow_off"]:return
			a=d["me"][2]
			if d["pin"]:
				e=ay(d["pin"])
				if e is not None and e["x"]is not None and e["f"]==a and not e["done"]:return(e["x"],e["y"],e["serial"])
			if n["auto"]:
				for e in d["list"]:
					if e["group"]==0:return(e["x"],e["y"],e["serial"])
			return
		def X(force_off=False,force=False):
			a=None if force_off else bt();b=d["arrow"]
			if not force and(a[:2]if a else None)==(b[:2]if b else None):d["arrow"]=a;return
			if a is None:API.TrackingArrow(-1,-1,aF)
			else:API.TrackingArrow(a[0],a[1],aF);d["arrow_at"]=time.time()
			d["arrow"]=a
		def bu(now):
			if d["arrow"]is None:return
			a=now-d.get("arrow_at",0.)
			if a<0:d["arrow_at"]=now;return
			if a<1.5 or ar():return
			d["arrow"],d["arrow_off"],d["pin"]=None,True,0
		def a_():
			z=T(t,d,560,N(1,v));w,s=z if z else(560,N(ap,v));G=t.rows(v,N(0,v),ap)if z else ap;g,f,h=t.begin(w,s);x=[]
			if not d["minimized"]:
				t.frame(g);M=F;l=w-2*M;a=M+30+C;I(g,M,a,l,36);o=M+l-8;k(g,f,"pg_dn",az,o-22,a+8,None,"Next page",on_click=U(("page",1)));k(g,f,"pg_up",aA,o-46,a+8,None,"Previous page",on_click=U(("page",-1)));y=o-52-u("9/9");h["pg"]=c(g,"",y,a+10,b);A=y-12-(35+u("Arrow off"));k(g,f,"arrow_off",O,A,a+7,"Arrow off","Take the tracking arrow down (a row click or Nearest brings it back)",on_click=U("arrow_off"));D=A-12-(35+u("Nearest"));k(g,f,"nearest",P,D,a+7,"Nearest","Point the tracking arrow at the nearest dig spot on your facet",on_click=U("nearest"));h["status"]=c(g,"",M+12,a+10,b);h["status_w"]=D-8-(M+12);e=a+36+C;I(g,M,e,l,s-e-M);m=M+12;p=m+max(34,u("Level"))+8;q=p+150+8;n=M+l-12-22;c(g,"Level",m,e+6,i);c(g,"Map",p,e+6,i);c(g,"Dig spot",q,e+6,i);h["where_w"]=n-8-q;h["empty_w"]=n-8-m
				for E in range(G):j=e+30+E*v;r={"val":None,"prev":None,"changed":0.,"sig":None,"tip":None,"pvis":True,"lvl":c(g,"",m,j+3,i),"name":c(g,"",p,j+3,B),"where":c(g,"",q,j+3,b)};r["catch"]=ak(g,M+6,j,n-4-(M+6),v,S(r,U,"row",follow=False),Z);r["ping"]=k(g,f,"ping%d"%E,P,n,j+1,None,bc,on_click=S(r,U,"ping",follow=False));x.append(r)
			t.end(g,{"rows":x});d["drawn"]=None;a1()
		t=Kit.Window(aB,ad,d,G,a_,a2,a3,(240,180),(aE,a4),5355,aQ,lock=True,clear={"rows":[]},docked_min=True)
		def a0(a,r,key,on):
			if r[key]!=on:r[key]=on;ao(a,"IsVisible",on)
		def a1():
			H=G["g"]
			if H is None or(d["minimized"]and d["docked"]):return
			v=d["arrow"][2]if d["arrow"]else 0;j=(d["list_ver"],d["page"],v,d["pin"],d["minimized"])
			if j==d["drawn"]:return
			d["drawn"]=j;c=G["c"];p=d["list"];q=next((bN for bN in p if bN["group"]==0),None);f=len(p);s=z(f,"map")
			if q is not None:w=q["dist"];x=("here"if w==0 else "%s %s"%(z(w,"tile"),q["dir"]));g="%s, nearest %s"%(s,x);k="%s, %s"%(s,x)
			elif f:g=k="%s, no spot on this facet"%s
			elif d["hidden"]:g="No maps listed (%d hidden on the settings page)"%d["hidden"];k="%d hidden"%d["hidden"]
			else:g="No treasure maps in your pack";k="no maps"
			if d["minimized"]:
				if c.get("status")is not None:h(c["status"],o("%s: %s"%(ad,k),aE-90))
				return
			y=G["rows"];t=max(1,len(y));l=max(1,(f+t-1)//t)
			if not 0<=d["page"]<l:d["page"]=max(0,min(l-1,d["page"]));d["drawn"]=j[:1]+(d["page"],)+j[2:]
			h(c["status"],o(g,c.get("status_w",200)));h(c["pg"],("%d/%d"%(d["page"]+1,l))if l>1 else "");I=d["page"]*t;J=c.get("where_w",200);A=time.time()
			for C,r in enumerate(y):
				D=I+C
				if D>=f:
					Q(r,None,A)
					if C==0 and f==0:m=("empty",bd if not d["hidden"]else(g+"."))
					else:m=("empty","")
					if r["sig"]!=m:r["sig"]=m;h(r["lvl"],o(m[1],c.get("empty_w",400)),b);h(r["name"],"");h(r["where"],"")
					a0(r["ping"],r,"pvis",False);continue
				e=p[D];Q(r,(e["serial"],),A);u=v==e["serial"];E=(e["serial"],e["lvl"],e["dec"],e["done"],e["where"],u,d["pin"]==e["serial"],n["auto"])
				if E!=r["sig"]:
					r["sig"]=E;h(r["lvl"],("L%d"%e["lvl"])if e["lvl"]>=0 else "?",i if not e["done"]else b);h(r["name"],o(au(e["lvl"]),150),B if e["dec"]and not e["done"]else b);h(r["where"],o(("> "if u else "")+e["where"],J),i if u else e["hue"]);a=e["tip"]
					if a==Z:
						F=d["pin"]==e["serial"]
						if n["auto"]:a=ba if F else Z
						else:a="Take the tracking arrow down"if F else bb
					if a!=r["tip"]:r["tip"]=a;L(r["catch"],a)
				a0(r["ping"],r,"pvis",e["x"]is not None and not e["done"])
		def bv(serial):
			e=ay(serial)
			if e is None:return
			if e["x"]is None or e["done"]:l(ae(e["tip"])+".");return
			if e["f"]!=d["me"][2]:l("that map's spot is in %s; you are in %s."%(E(e["f"]),E(d["me"][2])));return
			d["arrow_off"]=False
			if d["pin"]==serial:
				d["pin"]=0
				if n["auto"]:l("tracking arrow back on the nearest map.")
				else:d["arrow_off"]=True;l("tracking arrow down.")
			else:d["pin"]=serial;l("tracking arrow on the %s map's spot (%d, %d)."%(au(e["lvl"]).lower(),e["x"],e["y"]))
			X(force=True)
		def bw(serial,now):
			e=ay(serial)
			if e is None or e["x"]is None:return
			if HOST.services.get("pings.send")is None:l("World Map > Map Pings is off; turn it on to send map pings.");return
			d["ping"]=[e["x"],e["y"],e["f"],now+aM,0.]
		def bx(now):
			p=d["ping"]
			if p is None or(now<p[4]<=now+aN):return
			a=HOST.services.get("pings.send")
			if a is None:d["ping"]=None;l("World Map > Map Pings is off; turn it on to send map pings.");return
			try:b=bool(a(p[0],p[1],m=p[2],kind="go"))
			except Exception:b=True
			if b:d["ping"]=None
			elif not(now<p[3]<=now+aM):d["ping"]=None;l("Map Pings didn't take the ping (too soon after the last one); try again.")
			else:p[4]=now+aN
		def by():
			a=d["in_pack"]
			if a is None:l("your backpack isn't known yet; nothing was forgotten.");return
			b=[e for e in j if e not in a]
			for s in b:del j[s]
			d["dirty"]=True;l("forgot %s of maps not in your pack."%z(len(b),"spot"))
		def bz(f,x,y):c(f.g,"%s remembered"%z(len(j),"spot"),x+12,y+4,b);k(f.g,f.store,"forget",O,x+f.w-12-(35+u("Forget lost maps")),y,"Forget lost maps","Forget the spots of maps not in your backpack",on_click=U("forget"))
		def bA(a,now):d["page"]=max(0,d["page"]+a[1])
		def bB(a,now):
			d["arrow_off"]=False
			if n["auto"]:d["pin"]=0
			else:b=next((f for f in d["list"]if f["group"]==0),None);d["pin"]=b["serial"]if b is not None else 0
			X(force=True)
			if d["arrow"]is None:l("no decoded map with a spot on this facet.")
		def bC(a,now):d["pin"],d["arrow_off"]=0,True;X()
		def bD(a,now):by();HOST.refresh_settings(aB)
		bE={"page":bA,"row":lambda a,now:bv(a[1]),"ping":lambda a,now:bw(a[1],now),"nearest":bB,"arrow_off":bC,"forget":bD};bF=(("WINDOW  (open a decoded map once to read it)",(("check","auto","Point the tracking arrow at the nearest map's spot","With no map picked, the arrow points at the nearest spot on your facet"),("check","undecoded","List maps not decoded yet","Maps still to decode (Cartography)"),("check","done","List maps already dug up","Maps whose treasure is dug up"))),("SAVED SPOTS",(("custom",24,bz),),{"sh":64}),ac("maps"))
		def bG(w):return bF
		def bH(a,new):d["next_scan"]=0.;d["drawn"]=None
		aj=Kit.Page(n,bG,aR,bH)
		def bI():d.update({"shutting":False,"active":True,"docked":False,"queue":[],"used":[],"minimized":t.start_min(),"list":[],"list_sig":None,"next_scan":0.,"arrow":None,"pin":0,"arrow_at":0.,"arrow_off":False,"ping":None,"est":None,"look_until":0.,"last_map":(0,0.),"drawn":None,"page":0,"atlas_ver":None,"atlas_sig":None,"dig_tiles":set()});be();bf();A.clear();JR["rd"]=ax();bk();aY(time.time());a_();t.dock(fit=True,min=(560,N(1,v)));X()
		def bJ():
			if G["g"]is None:return
			if V(G):return
			a=time.time()
			if d["used"]:bl(a)
			bm(a);bn(a);q=d["queue"]
			while q:
				b=q.pop(0);c=b[0]if isinstance(b,tuple)else b
				if not t.action(c):bE[c](b,a)
				if G["g"]is None:return
			if not(a<d["next_scan"]<=a+aI):
				d["next_scan"]=a+aI;aY(a);bu(a);X()
				if d["list_ver"]!=d["atlas_ver"]:d["atlas_ver"]=d["list_ver"];br()
			if d["ping"]is not None:bx(a)
			if d["dirty"]and not(a<d["next_save"]<=a+aK):d["next_save"]=a+aK;aT()
			a1()
		def bK():return.1 if d["look_until"]>time.time()else.2
		def bL():
			d["shutting"]=True;d["active"]=False;X(force_off=True);aR()
			if d["dirty"]:aT()
			JR["rd"]=None;aZ(());d["used"],d["queue"],d["ping"]=[],[],None;aQ.close()
		return{"start":bI,"tick":bJ,"stop":bL,"client_tick":True,"config_height":aj.height,"build_config":aj.build,"poll_config":aj.poll,"config_closed":aj.closed,"interval":bK}
	def aX():
		aV="harvest";ai="Ore Tracker";aw="Harvest_settings";aW="Harvest_pos";aX="Harvest_min";U=("ore","wood","fish","sand");v={"ore":"Ore","wood":"Wood","fish":"Fish","sand":"Sand"};aY={"ore":"mining","wood":"lumberjacking","fish":"fishing","sand":"sand for glassblowing"};aZ={"ore":1153,"wood":68,"fish":88,"sand":53};a_={"there is no metal here to mine.":"ore","there's not enough wood here to harvest.":"wood","the fish don't seem to be biting here.":"fish","there is no sand here to mine.":"sand",};a0={"you loosen some rocks but fail to find any useable ore.":"ore","you hack at the tree for a while, but fail to produce any useable wood.":"wood","you fish a while, but fail to catch anything.":"fish","you dig for a while but fail to find any of sufficient quality for glassblowing.":"sand",};a1=(("you dig some ","ore"),("you put some logs","wood"),("you chop some ","wood"),("you pull out ","fish"),("you carefully dig up sand","sand"),("your backpack can't hold the sand","sand"),);a2=("","system");ay={"ore":(8,8),"wood":(4,3),"fish":(8,8),"sand":(8,8)};aj={"ore":(10,20),"wood":(20,30),"fish":(10,20),"sand":(10,20)};az=3;a3={"ore":3,"wood":3,"fish":5,"sand":3};aA=300;al=8;aB=.85;ab=.95;a4,a5=40,3.5;aC=.5;aD="harvest.weight";aE=1.;aF=1.;ap=0x48525654;aG=6.;aH=5.;aq="Harvest_spots";at=440;aI,a6=340,46;W=24;a7={"north":(0,-1),"northeast":(1,-1),"east":(1,0),"southeast":(1,1),"south":(0,1),"southwest":(-1,1),"west":(-1,0),"northwest":(-1,-1)};aJ="Put the tracking arrow on it (again: take it down)";a8="Send a Look here ping on this spot so others know it is dry (needs World Map > Map Pings)";a9="No dry spots yet: spots the shard says ran out show here.";aK=60.*az*max(bH for bI,bH in aj.values());f={"ore":True,"wood":True,"fish":True,"sand":True,"alert":True,"keep":True};bG=dict(f);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"rd":None,"ver":0,"mini_key":None,"w_key":None,"arrow_at":0.};g={};j={};l={"g":None,"c":{},"store":({},{}),"rows":[]};G=[];aL,ad,X=R(a,ai)
		def ba():am(aw,";",f)
		def aM():an(aw,";",f,U+("alert","keep"))
		def aN():return ";".join("%s,%d,%d,%d,%d,%d,%d"%(d["kind"],d["m"],d["x"],d["y"],int(d["lo"]),int(d["hi"]),1 if d["about"]else 0)for d in g.values())
		def bb():
			g.clear()
			if not f["keep"]:return
			c=time.time()
			for e in J(aq).split(";"):
				b=e.split(",")
				if len(b)<7 or b[0]not in U:continue
				try:m,x,y,h,d=int(b[1]),int(b[2]),int(b[3]),float(b[4]),float(b[5])
				except ValueError:continue
				if d<=c or d-c>aK+60:continue
				aO(b[0],m,x,y,h,d,b[6]=="1",c)
			a["ver"]+=1
		def Y():
			a["ver"]+=1
			if f["keep"]:a["save_due"]=True
		def bc():a["save_due"]=False;a["save_at"]=time.time()+aH;H(aq,aN()if f["keep"]else "")
		def N(kind,m,x,y):a,b=ay[kind];return(kind,m,x//a,y//b)
		def aO(kind,m,x,y,lo,hi,about,now):
			b=N(kind,m,x,y);d=g.get(b);g[b]={"kind":kind,"m":m,"x":x,"y":y,"lo":lo,"hi":hi,"at":now,"about":about,"key":b}
			if a["arrow"]==b and d is not None and(d["x"],d["y"])!=(x,y):API.TrackingArrow(x,y,ap);a["arrow_at"]=now
			if len(g)>60:
				c=None
				for k,e in g.items():
					if k!=b and(c is None or e["hi"]<g[c]["hi"]):c=k
				if c is not None:
					del g[c]
					if a["arrow"]==c:p()
			return b
		def aP():return az if HOST.guarded()is True else 1
		def bd(kind,x,y,m,about,now):
			g=N(kind,m,x,y);b,a=aj[kind];c=aP();b,a=b*c,a*c;f=j.pop(g,None)
			if f is not None and 0<=now-f<a*60.:d,e=f+b*60.,f+a*60.
			else:d,e=now,now+a*60.
			aO(kind,m,x,y,d,e,about,now);Y()
		def be(kind,x,y,m,got,now):
			b=N(kind,m,x,y)
			if g.pop(b,None)is not None:
				if a["arrow"]==b:p()
				Y()
			if got:
				f=j.get(b)
				if f is None or not 0<=now-f<aj[kind][1]*60.*aP():
					if len(j)>=aA:
						for k in[d for d,e in j.items()if not 0<=now-e<aK]:del j[k]
						if len(j)>=aA:j.clear()
					j[b]=now
		def bf(now):
			c=[n for n,m in g.items()if m["hi"]<=now or m["at"]-now>60.]
			for k in c:
				del g[k]
				if a["arrow"]==k:p()
			if c:Y()
			b=a["arrow"]
			if b is not None and 1.5<=now-a["arrow_at"]and not ar():a["arrow"]=None;a["ver"]+=1;b=None
			if b is not None:
				d=Z()
				if d is not None and d[2]!=b[1]:p()
		def bg(d):
			for e in g.values():e["lo"]+=d;e["hi"]+=d;e["at"]+=d
			for k in list(j):j[k]+=d
			for k in("w_at","draw_at","expire_at","save_at","arrow_at"):a[k]=a[k]+d
			p=a["ping"]
			if p is not None:p[3]+=d
			if g:Y()
		def Z():
			p=API.Player
			if p is None:return
			b=(int(p.X),int(p.Y),int(API.GetMap()))
			if b[0]<=0 and b[1]<=0:return
			a["me"]=b;return b
		def bh(kind,me):
			a,b=me[0],me[1];p=API.LastTargetPos;x,y=int(p.X),int(p.Y)
			if 0<x<65535 and 0<y<65535 and max(abs(x-a),abs(y-b))<=a3[kind]:return x,y,False
			c,d=a7.get(str(API.Player.Direction or "").strip().lower(),(0,0));return a+c,b+d,True
		def bi(low):
			k=a_.get(low)
			if k is not None:return "dry",k
			k=a0.get(low)
			if k is not None:return "fail",k
			if low.startswith("you"):
				for a,k in a1:
					if low.startswith(a):return "got",k
			return
		def bj(now):
			e=a["rd"]
			if e is None:return
			for g in e.new():
				h=bi(g.low.strip())
				if h is None or(g.name or "").strip().lower()not in a2:continue
				d,b=h
				if d=="dry"and not f[b]:continue
				c=Z()
				if c is None:continue
				x,y,i=bh(b,c)
				if d=="dry":bd(b,x,y,c[2],i,now)
				else:be(b,x,y,c[2],d=="got",now)
		def bk():s=HOST.by_key.get("character");return s is not None and bool(s.running)
		def bl(now):
			if now<a["w_at"]and a["w_at"]-now<=aC:return
			a["w_at"]=now+aC
			if not f["alert"]and(l["g"]is None or(a["minimized"]and a["docked"])):return
			p=API.Player
			if p is None:return
			d,b=int(p.Weight),int(p.WeightMax);e=int(p.Strength)if b<=0 else 0
			if b<=0 and e>0:b=int(a4+a5*e)
			c=(float(d)/b)if b>0 else-1.;a["weight"]=(d,b,c)
			if c>=ab:
				if a["w_armed"]:
					g=True
					if f["alert"]and not bk():g=af(aD,"Weight %d/%d (%d%%): nearly overloaded"%(d,b,int(c*100)),level="warn",who="weight")is not False
					if g:a["w_armed"]=False
			elif 0<=c<.92:a["w_armed"]=True
		def p():
			if a["arrow"]is None:return
			a["arrow"]=None;a["ver"]+=1;API.TrackingArrow(-1,-1,ap)
		def bm(key):
			e=g.get(key)
			if e is None:return
			if a["arrow"]==key and ar(True):p();return
			b=Z()or a["me"]
			if b is not None and b[2]!=e["m"]:X("that spot is in %s; you are in %s."%(E(e["m"]),E(b[2])));return
			API.TrackingArrow(e["x"],e["y"],ap);a["arrow"],a["arrow_at"]=key,time.time();a["ver"]+=1
		def bn(key):
			e=g.get(key)
			if e is None:return
			if HOST.services.get("pings.send")is None:X("turn World Map > Map Pings on to ping a spot.");return
			a["ping"]=[e["x"],e["y"],e["m"],time.time()+aG,"the dry %s spot (%d, %d)"%(v[e["kind"]].lower(),e["x"],e["y"])]
		def bo(now):
			p=a["ping"]
			if p is None:return
			b=HOST.services.get("pings.send")
			if b is None or now>p[3]or p[3]-now>aG+1.:a["ping"]=None;X("the ping on %s wasn't sent (%s)."%(p[4],"Map Pings is off"if b is None else "Map Pings stayed busy"));return
			try:c=b(p[0],p[1],p[2],"look")
			except Exception:c=None
			if c is False:return
			a["ping"]=None
			if c:X("Look here ping on %s."%p[4],D)
			else:X("couldn't send the ping on %s (Map Pings refused it)."%p[4],A)
		def au(secs):
			secs=max(0,int(secs))
			if secs<60:return "%ds"%secs
			return "%dm"%((secs+59)//60)
		def bp(e,me):
			if me is None:return 0
			if me[2]!=e["m"]:return 1<<30
			if N(e["kind"],me[2],me[0],me[1])==e["key"]:return 0
			return max(abs(e["x"]-me[0]),abs(e["y"]-me[1]))
		def bq(e,me):
			if me is None:return M(e["x"],e["y"],"(%d, %d)")
			if me[2]!=e["m"]:return "in %s"%E(e["m"])
			if N(e["kind"],me[2],me[0],me[1])==e["key"]:return "here"
			return("about "if e["about"]else "")+K(e["x"]-me[0],e["y"]-me[1])
		def aQ(e,now):
			if now<e["lo"]:return "back in %s-%s"%(au(e["lo"]-now),au(e["hi"]-now)),A
			return "back within %s"%au(e["hi"]-now),i
		def br(e,on):
			a,b=ay[e["kind"]];f,g=(e["x"]//a)*a,(e["y"]//b)*b;c=time.strftime("%H:%M",time.localtime(e["hi"]))
			if e["lo"]>e["at"]:d="back between %s and %s"%(time.strftime("%H:%M",time.localtime(e["lo"])),c)
			else:d="back by %s at the latest"%c
			return "%s ran dry at %s%s: the %dx%d block from %s, %s.  %s"%(v[e["kind"]],M(e["x"],e["y"])," (about: the tile in front of you)"if e["about"]else "",a,b,M(f,g),d,"Take the tracking arrow down"if on else aJ)
		def av():return[d for d in g.values()if f[d["kind"]]]
		def bs(t):return(t[0],t[1])
		def bt():q.set("dry",{aa("%s dry %d %d"%(v[d["kind"]],d["x"],d["y"])):(int(d["x"]),int(d["y"]),int(d["m"]),"blue")for d in sorted(av(),key=lambda e:-e["at"])[:15]})
		def ae(n):return 2*F+30+3*C+46+36+74+n*W+22
		def aR():
			M=F;z=T(s,a,at,ae(1));w,v=z if z else(at,ae(al));x=s.rows(W,ae(0),al)if z else al;g,j,d=s.begin(w,v);y=[]
			if not a["minimized"]:
				s.frame(g);e=w-2*M;l=M+30+C;I(g,M,l,e,46,"WEIGHT");d["wtext"]=c(g,"",M+20+u("WEIGHT"),l+6,B);Kit.weight_bar(g,d,M+12,l+28,e-24);m=l+46+C;I(g,M,m,e,36);o=M+12;k(g,j,"clear",O,o,m+7,"Clear","Empty the list of dry spots",on_click=ad("clear"));o+=35+u("Clear")+16;k(g,j,"arrow_off",O,o,m+7,"Arrow off","Take the tracking arrow down",on_click=ad("arrow_off"));n=m+36+C;I(g,M,n,e,v-n-M,"DRY SPOTS  (nearest first)");d["here"]=c(g,"",M+12,n+28,b);E=35+u("Ping");A,D,p=M+12,M+12+52,M+12+52+130;q=M+e-6-E;d["back_w"]=q-8-p;f=n+52;c(g,"What",A,f,i);c(g,"Where",D,f,i);c(g,"When",p,f,i);d["here_w"]=e-24
				for t in range(x):h=f+22+t*W;r={"val":None,"prev":None,"changed":0.,"sig":None,"vis":True,"tip":None,"kind":c(g,"",A,h+3,B),"where":c(g,"",D,h+3,B),"back":c(g,"",p,h+3,b)};r["catch"]=ak(g,M+6,h,q-4-(M+6),W,S(r,ad,"arrow",follow=False),aJ);r["plbl"]=k(g,j,"ping%d"%t,P,q,h,"Ping",a8,on_click=S(r,ad,"ping",follow=False));r["pbtn"]=j[0].get("ping%d"%t);y.append(r)
				d["more"]=c(g,"",M+12,f+22+x*W+2,b)
			s.end(g,{"rows":y});a["drawn"]=a["mini_drawn"]=a["wdrawn"]=None;a["draw_at"]=0.;aT(time.time())
		s=Kit.Window(aV,ai,a,l,aR,aW,aX,(260,220),(aI,a6),3718,aL,lock=True,clear={"rows":[],"c":{}},docked_min=True)
		def aS(r,on):
			if r["vis"]==on:return
			r["vis"]=on
			for n in("where","back","catch","pbtn","plbl"):ao(r.get(n),"IsVisible",on)
			if not on:h(r["kind"],"")
		def aT(now):
			K=l["g"]
			if K is None or(a["minimized"]and a["docked"]):return
			c=l["c"]
			if a["minimized"]:
				d=a["weight"];k=(a["ver"],f["ore"],f["wood"],f["fish"],f["sand"])
				if a["count"][0]!=k:a["count"]=(k,len(av()))
				u=a["count"][1];w=(u,d)
				if a["mini_drawn"]is not None and w==a["mini_key"]:return
				a["mini_key"]=w;s="%s: %s, %s"%(ai,("weight %d%%"%int(d[2]*100))if d and d[2]>=0 else "weight ?",z(u,"dry spot"))
				if s!=a["mini_drawn"]:
					a["mini_drawn"]=s;x=c.get("status")
					if x is not None:
						t=b
						if d and d[2]>=ab:t=A
						elif d and d[2]>=aB:t=i
						h(x,o(s,aI-90),t)
				return
			bu();k=(a["ver"],a["arrow"],f["ore"],f["wood"],f["fish"],f["sand"])
			if k==a["drawn"]and now<a["draw_at"]and a["draw_at"]-now<=aE:return
			a["drawn"],a["draw_at"]=k,now+aE;j=Z()or a["me"];m=[(bp(bH,j),bH["hi"],bH)for bH in av()];m.sort(key=bs);p=None
			if j is not None:
				for y in U:
					if f[y]:
						e=g.get(N(y,j[2],j[0],j[1]))
						if e is not None:p=e;break
			if p is not None:h(c["here"],o("Here: %s is dry, %s"%(v[p["kind"]].lower(),aQ(p,now)[0]),c["here_w"]),A)
			elif m:h(c["here"],"Here: nothing known dry",D)
			else:h(c["here"],o(a9,c["here_w"]),b)
			M=c.get("back_w",160)
			for C,r in enumerate(l["rows"]):
				if C>=len(m):Q(r,None,now);r["sig"]=None;aS(r,False);continue
				e=m[C][2];E=bq(e,j);q=e["key"];Q(r,(q,),now);n=a["arrow"]==q;F,G=aQ(e,now);H=(q,E,F,G,n,e["lo"],e["hi"]);aS(r,True)
				if H==r["sig"]:continue
				r["sig"]=H;h(r["kind"],v[e["kind"]],aZ.get(e["kind"],B));h(r["where"],o(("> "if n else "")+E,124),i if n else B);h(r["back"],o(F,M),G);I=(q,n,e["lo"],e["hi"])
				if I!=r["tip"]:r["tip"]=I;L(r["catch"],br(e,n))
			J=len(m)-len(l["rows"]);h(c["more"],("+%d farther"%J)if J>0 else "",b)
		def bu():
			c=l["c"];b=a["weight"]
			if a["wdrawn"]is not None and b==a["w_key"]:return
			a["w_key"]=b;j=c.get("wfills")
			if b is None or b[2]<0:e,d,f="not known yet",None,0
			else:e="%d / %d stones (%d%%)"%(b[0],b[1],int(b[2]*100));d,f=Kit.weight_level(b[2],c.get("wbar_w",100))
			g=(e,d,f)
			if g==a["wdrawn"]:return
			a["wdrawn"]=g;k={"red":A,"warn":i}.get(d,B)
			if c.get("wtext")is not None:h(c["wtext"],e,k)
			Kit.weight_show(j or{},d,f)
		bv=("Back in: ore and sand 10-20 min, wood 20-30, fish 10-20, from the block's first harvest (3x as long in guarded towns).")
		def bw(action):p();g.clear();Y()
		bx={"clear":bw,"arrow_off":lambda action:p(),"arrow":lambda action:bm(action[1]),"ping":lambda action:bn(action[1])}
		def aU(kind):return "%s (%s)"%(v[kind],aY[kind])
		def by(w):a=max(u(aU(d))for d in U);return 2 if a+30<=(w-24)//2 else 1
		def bz(w):a,b=by(w),(w-24)//2;return(("WHAT TO WATCH",[("check",d,aU(d),"List spots where the %s ran out"%v[d].lower(),{"dx":12+(e%a)*b,"stay":e%a<a-1})for e,d in enumerate(U)]+[("gap",6),("check","keep","Keep the list when Virtue Assistant stops (per character)","Unticked: it starts empty each time"),("gap",2)]+[("note",m)for m in["Unticked kinds are hidden, not forgotten."]+Kit.wrap(bv,w-28)],{"top":32}),("WEIGHT  (yellow at %d%%, red at %d%%)"%(int(aB*100),int(ab*100)),(("check","alert","Alert as you cross the red line","Once each time you pass %d%% of your maximum weight; quiet while Inventory > Paperdoll is on (it has its own)"%int(ab*100)),),{"top":32,"pad":4}),ac("dry"))
		def bA(b,new):
			if new["keep"]!=b["keep"]:a["save_due"]=True
			if new["alert"]and not b["alert"]:a["w_armed"]=True
			a["drawn"]=a["mini_drawn"]=None
		ah=Kit.Page(f,bz,aM,bA)
		def bB():a.update({"shutting":False,"docked":False,"queue":[],"drawn":None,"mini_drawn":None,"wdrawn":None,"arrow":None,"ping":None,"w_armed":True,"weight":None,"w_at":0.,"draw_at":0.,"expire_at":0.,"save_due":False,"save_at":0.,"me":None,"count":(None,0),"last_now":None,"atlas":None,"minimized":s.start_min()});del G[:];j.clear();ba();bb();a["rd"]=ax();ag(aD,"Weight near the limit",74);Z();aR();s.dock(fit=True,min=(at,ae(1)))
		def bC():
			if l["g"]is None:return
			if V(l):return
			b=time.time();d,a["last_now"]=a["last_now"],b
			if d is not None and b<d-2.:bg(b-d)
			q=a["queue"]
			while q:
				c=q.pop(0);g=c[0]if isinstance(c,tuple)else c
				if not s.action(c):bx[g](c)
				if l["g"]is None:return
			bj(b)
			if b>=a["expire_at"]or a["expire_at"]-b>aF:a["expire_at"]=b+aF;bf(b)
			e=(a["ver"],f["ore"],f["wood"],f["fish"],f["sand"])
			if e!=a["atlas"]:a["atlas"]=e;bt()
			bl(b);bo(b);aT(b)
			if a["save_due"]and(b>=a["save_at"]or a["save_at"]-b>aH)and not G:G.append(bc)
		def bD():
			while G and not a["shutting"]:G.pop(0)()
		def bE():return bool(G)
		def bF():a["shutting"]=True;p();a["ping"]=a["rd"]=None;del G[:];aM();H(aq,aN()if f["keep"]else "");a["save_due"]=False;aL.close()
		return{"start":bB,"tick":bC,"stop":bF,"client_tick":True,"config_height":ah.height,"build_config":ah.build,"poll_config":ah.poll,"config_closed":ah.closed,"thread_tick":bD,"thread_wanted":bE}
	def aY():
		X="traphl";v="Traps & Fields";Y="TrapHL_settings";aA="TrapHL_pos";Z="TrapHL_view";B=F+30+C+40+F;ab,aC=320,46;ad=68;ah=33;l=3000;aD=.15;aE=1.;aF=3.;aG=3.;aH=5.;aI=[4355,4374,4524,4529,4512,4520,4536,4412,4423,4341,4348,4389,7025,7026,7027,7028,3696,];ai="TrapHL_fields";aJ=(("fire",14732,14751),("poison",14612,14633),("paralyze",14695,14730),("energy",14662,14692));E=53;G=1153;aK={"fire":("Fire field",i),"poison":("Poison field",i),"energy":("Energy field",i),"paralyze":("Paralyze field!",A)};ak=3;am="traphl.trap";M={bp:bm for bm,bn,bo in aJ for bp in range(bn,bo+1)};aL={};d={"range":14,"cycle":2.,"pulse":True,"green":ad,"red":ah,"by_name":True,"graphics":list(aI),"ping":True,"fields":True,"field_hue":E,"para_hue":G,"field_say":False};bl=dict(d);a={"minimized":False,"shutting":False,"docked":False,"queue":[],"hooked":False,"poke":False};s={"g":None,"c":{},"store":({},{})};j={"f":None,"gfx_typed":None,"gfx_since":0.};an,aM,ao=R(a,v)
		def aN():
			p=J(Y).split("|")
			if len(p)<7:return
			with Kit.quiet:
				d["range"]=max(1,min(30,int(p[0])));d["cycle"]=max(.5,min(10.,float(p[1])));d["pulse"]=p[2]=="1";d["green"]=int(p[3]);d["red"]=int(p[4]);d["by_name"]=p[5]=="1";a=ap(p[6])
				if a or not p[6].strip():d["graphics"]=a
				if len(p)>=8:d["ping"]=p[7]!="0"
		def aO():
			v=W(J(ai));d["fields"]=v.get("on")!="0";d["field_say"]=v.get("say")=="1"
			for k,a,b in(("hue","field_hue",E),("para","para_hue",G)):
				try:d[a]=max(0,min(l,int(v[k])))
				except(KeyError,ValueError):d[a]=b
		def aP():H(ai,"on=%d;hue=%d;para=%d;say=%d"%(int(d["fields"]),d["field_hue"],d["para_hue"],int(d["field_say"])))
		def N():H(Y,"|".join([str(d["range"]),"%.2f"%d["cycle"],"1"if d["pulse"]else "0",str(d["green"]),str(d["red"]),"1"if d["by_name"]else "0",O(),"1"if d["ping"]else "0"]))
		def ap(text):
			b=[]
			for a in str(text).replace(";",",").replace(" ",",").split(","):
				a=a.strip()
				if not a:continue
				try:v=int(a,16)
				except Exception:continue
				if 0<v<65536 and v not in b:b.append(v)
			return b
		def O():return ", ".join("0x%04X"%e for e in d["graphics"])
		def aQ():b=J(Z);v=W(b);a["minimized"]=v.get("min")=="1";a["paused"]=v.get("paused")=="1";a["view_saved"]=b
		def aq():
			b="min=%d;paused=%d"%(int(bool(a["minimized"])),int(bool(a["paused"])))
			if b!=a.get("view_saved"):a["view_saved"]=b;H(Z,b)
		def m(item,hue):item.Hue=int(hue)&65535
		def t(item):return int(item.Hue or 0)
		def P(item):return int(item.X),int(item.Y)
		r={};ar={"gfx":None,"wanted":frozenset(),"by_name":None,"fields":None}
		def aR(it):
			a=str(it.Name or "").lower()
			if not a:return
			return "trap"in a and "scroll"not in a and "kit"not in a
		def aS():
			a=ar;b=d["graphics"]
			if a["gfx"]is not b or a["by_name"]!=d["by_name"]or a["fields"]!=d["fields"]:a["gfx"],a["wanted"]=b,frozenset(b);a["by_name"],a["fields"]=d["by_name"],d["fields"];r.clear()
			return a["wanted"]
		def aT():
			x=int(d["range"]);a["atlas_map"]=None;j={};k={};h=a["last_scan"];l=h>=a["hue_at"];q=M if d["fields"]else aL
			if l:a["hue_at"]=h+aG
			y=aS();z=d["by_name"];A=r;n={}
			for b in API.GetItemsOnGround(x)or():
				c=int(b.Serial);g=int(b.Graphic);v=A.get(c)
				if v is not None and v[0]==g and(not v[2]or h<v[2]):e=v[1];n[c]=v
				else:
					s=0
					if g in y:e=1
					elif z and g not in q:
						u=aR(b)
						if u is None:e,s=0,h+aH
						else:e=1 if u else 0
					else:e=2 if g in q else 0
					n[c]=(g,e,s)
				if e==1:j[c]=b
				elif e==2:k[c]=b
			r.clear();r.update(n);f=a["tracked"];o=[]
			for c,b in j.items():
				i=f.get(c)
				if i is None:
					p=t(b)
					if p in(d["green"],d["red"]):p=0
					f[c]={"item":b,"orig":p,"set":d["green"]};m(b,d["green"]);aU(b)
					if d["ping"]and c not in a["pinged"]:a["ping_wait"].append(c)
					if c not in a["alerted"]:o.append(b)
				else:
					i["item"]=b
					if l and t(b)!=i["set"]:m(b,i["set"])
			w=[bm for bm in f if bm not in j]
			for c in w:Q(c,f.pop(c))
			if w and a["ping_wait"]:a["ping_wait"]=[bn for bn in a["ping_wait"]if bn in f]
			if o:aX(o)
			if k or a["fields"]:aY(k,l)
		def aU(it):
			x,y=P(it)
			if x<=0 or y<=0:return
			if a["atlas_map"]is None:a["atlas_map"]=int(API.GetMap())
			c=(x,y,a["atlas_map"]);b=a["atlas_traps"]
			if c in b:return
			b.append(c)
			if len(b)>20:del b[0]
			a["atlas_ver"]+=1
		def aV():q.set("traps",{aa("Trap %d %d"%(e,f)):(e,f,g,"red")for e,f,g in a["atlas_traps"]})
		aW=("east","south-east","south","south-west","west","north-west","north","north-east")
		def aX(b):
			d=a["alerted"]
			if len(d)+len(b)>5000:d.clear()
			p=API.Player;l,m=int(p.X),int(p.Y);f,e,g,h=None,None,0,0
			for c in b:
				d.add(int(c.Serial));i,j=int(c.X)-l,int(c.Y)-m;k=max(abs(i),abs(j))
				if e is None or k<e:f,e,g,h=c,k,i,j
			w=K(g,h,names=aW);n="A trap %s"%w if len(b)==1 else "%d new traps in range (nearest %s)"%(len(b),w);af(am,n,who=int(f.Serial))
		def at(kind):return d["para_hue"]if kind=="paralyze"else d["field_hue"]
		def aY(k,l):
			h=a["fields"];i=[]
			for f,c in k.items():
				e=h.get(f)
				if e is None:
					j=M.get(int(c.Graphic))
					if j is None:continue
					b=at(j);g=t(c)
					if g and g in(d["field_hue"],d["para_hue"]):g=0
					h[f]=e={"item":c,"orig":g,"set":b,"kind":j}
					if b:m(c,b)
					if d["field_say"]:i.append(e)
					continue
				e["item"]=c;b=at(e["kind"])
				if b!=e["set"]:m(c,b if b else e["orig"]);e["set"]=b
				elif b and l and t(c)!=b:m(c,b)
			for f in[w for w in h if w not in k]:av(f)
			if i:aZ(i)
		def aZ(recs):
			d=time.time();b=[w for w in a["field_said"]if d-w[3]<10.];f=sorted([P(bm["item"])+(bm["kind"],bm["item"])for bm in recs],key=a_)
			for x,y,c,g in f:
				e=False
				for k,h,j,t in b:
					if(k==c and abs(h-x)<=ak and abs(j-y)<=ak):e=True;break
				b.append((c,x,y,d))
				if e:continue
				l,m=aK.get(c,("Field",i));API.HeadMsg(l,int(g.Serial),m)
			a["field_said"]=b[-20:]
		def a_(e):return(e[0],e[1])
		def av(serial):
			b=a["fields"].pop(serial,None)
			if b is not None and b["set"]:Q(serial,b)
		def Q(serial,rec):m(API.FindItem(serial)or rec["item"],rec["orig"])
		def aw():
			for b in list(a["tracked"]):Q(b,a["tracked"].pop(b))
			for b in list(a["fields"]):av(b)
		def a0():
			if not a["tracked"]:return
			e=d["pulse"]and(time.time()%max(.5,d["cycle"])<min(.35,d["cycle"]/2.));b=d["red"]if e else d["green"]
			for c in a["tracked"].values():
				if c["set"]!=b:m(c["item"],b);c["set"]=b
		def u():return HOST.services.get("pings.send")
		def a1():
			b=len(a["ping_wait"])
			if b:
				a2()
				if len(a["ping_wait"])!=b:n()
		def a2():
			b=a["ping_wait"];e=u()
			if e is None:
				if not a["ping_noted"]:a["ping_noted"]=True;ao("turn World Map > Map Pings on to ping traps (they wait until then).")
				return
			if time.time()<a["ping_next"]:return
			g=a["tracked"];m=None
			while b:
				c=b[0];f=g.get(c)
				if f is None or c in a["pinged"]:b.pop(0);continue
				x,y=P(f["item"])
				if x<=0 or y<=0:b.pop(0);continue
				if m is None:m=int(API.GetMap())
				d=(m,x,y)
				if d in a["pinged_spots"]:S(c,None);b.pop(0);continue
				try:h=e(x,y,m,"danger","You (trap)")
				except Exception:S(c,d);b.pop(0);return
				if h:b.pop(0);S(c,d);a["ping_sent"]+=1;a["ping_next"]=time.time()+.75
				return
		def S(serial,spot):
			if len(a["pinged"])>=5000:a["pinged"].clear();a["pinged_spots"].clear()
			a["pinged"].add(serial)
			if spot is not None:a["pinged_spots"].add(spot)
		def a3():
			a["pinged"].clear();a["pinged_spots"].clear();a["ping_sent"]=0;a["ping_wait"]=list(a["tracked"]);c=len(a["ping_wait"])
			if a["paused"]:b="paused: untick Pause highlighting (World Map settings) to ping traps."
			elif c==0:b="no traps in range; each is pinged when next found."
			elif u()is None:b=("%s to ping once World Map > Map Pings is on."%z(c,"trap"))
			else:b="pinging %s."%z(c,"trap")
			ao(b);a["ping_noted"]=False;n()
		def a4():
			n=len(a["ping_wait"])
			if n and a["ping_svc"]is not None:return "sending %d"%n,b
			if not d["ping"]:return "auto-ping off",b
			if a["ping_svc"]is None:return "World Map > Map Pings is off",A
			return "%d sent"%a["ping_sent"],D
		a5="Ping danger on each highlighted trap, and again when next found (needs World Map > Map Pings)";U="Ping traps on screen"
		def ax():
			z=T(p,a,320,B);w,h=z if z else(320,B);g,c,d=p.begin(w,h)
			if not a["minimized"]:p.frame(g);M=F;b=M+30+C;I(g,M,b,w-2*M,h-b-M);k(g,c,"ping",Kit.ART_CIRCLE,M+12,b+12,U,a5,on_click=aM("ping_again"))
			p.end(g);n();aq()
		p=Kit.Window(X,v,a,s,ax,aA,None,(200,200),(ab,aC),4412,an,lock=True)
		def n():
			g=s["c"];n=len(a["tracked"]);e=len(a["fields"])
			if a["paused"]:c,d="Paused",b
			elif n==0 and e==0:c,d="No traps in range",b
			elif e==0:c,d="Highlighting %s"%z(n,"trap"),D
			elif n==0:c,d="Highlighting %s"%z(e,"field"),D
			else:c,d="Highlighting %s, %s"%(z(n,"trap"),z(e,"field")),D
			if g.get("status")is not None:h(g["status"],o("%s: %s"%(v,ae(c)),ab-90),d)
			f=j["f"]
			if f is None:return
			h(f.c["now"],c,d);i,k=a4();h(f.c["now_ping"],"Pings: "+i,k)
			if a["pause_want"]is None and bool(f.c["paused"].IsChecked)!=bool(a["paused"]):f.c["paused"].SetIsChecked(bool(a["paused"]))
		def a6(f,x,y):f.c["now"]=c(f.g,"",x+12,y,D);f.c["now_ping"]=c(f.g,"",x+12+f.w//2,y,b)
		def a7(f,x,y):f.c["paused"]=aB(f.g,"Pause highlighting (the hues are put back)",x+12,y,a["paused"],"Stops the scan and puts every hue back")
		a8={"ping_again":a3}
		def a9(f,x,y):c(f.g,"Pulse cycle:",x+12,y+4);a=int(round(d["cycle"]*10));f.c["cycle"]=L(Kit.add_slider(f.g,x+120,y+2,160,5,100,a),"Seconds between red flashes (0.5-10)");f.c["cycle_v"]=c(f.g,"%.1f s"%d["cycle"],x+290,y+4,b)
		def ba(f,x,y):f.c["graphics"]=L(aj(f.g,O(),x+12,y,f.w-28,numbers=False),"Trap item graphics in hex (0x1103 or 1103), comma separated; applied when you stop typing")
		ay={"lw":98,"fw":60,"stay":True,"clamp":False};az=(("STATUS  (the window has %s)"%U,(("custom",24,a6),("custom",26,a7)),{"pad":4}),("TRAPS  (hues are client hue numbers)",(("slider","range","Scan range:","Tiles round you scanned as you move (1-30)",1,30,{"lw":98,"ldy":4,"sw":160,"ugap":10,"vfmt":"%d tiles"}),("custom",29,a9),("num","green","Green hue:","Hue traps are held at (1-%d; default %d)"%(l,ad),None,1,l,ay),("num","red","Red hue:","Hue of the pulse (1-%d; default %d)"%(l,ah),None,1,l,{"dx":200,"lw":70,"fw":60,"h":29,"clamp":False}),("check","pulse","Pulse red once per cycle (unticked: steady green)","Flashes each highlighted trap red for a beat")),{"top":32,"pad":2}),("TRAP GRAPHICS  (hex ids, comma separated)",(("custom",30,ba),("check","by_name","Also highlight ground items the client names 'trap'","For traps not in the list (the client knows a name only after a tooltip or click)")),{"top":32,"pad":8}),("TRAP PINGS  (needs World Map > Map Pings)",(("check","ping","Send a Danger! map ping on each new trap, once per trap","For you and your guildmates; \"%s\" on the window pings them all again"%U),),{"top":32,"pad":4}),("MAGIC FIELDS  (client hue numbers, 0 = leave as is)",(("check","fields","Highlight magic fields: fire, poison, energy, paralyze","Client-side recolour, like the traps; paralyze fields get their own hue",{"h":29}),("num","field_hue","Field hue:","Hue of fire, poison and energy fields (0-%d, 0 = as is; default %d)"%(l,E),None,0,l,ay),("num","para_hue","Paralyze hue:","Hue of paralyze fields (0-%d, 0 = as is; default %d)"%(l,G),None,0,l,{"dx":200,"lgap":12,"fw":60,"h":29,"clamp":False}),("check","field_say","Show an overhead text when a field appears","Names each new field above it once (\"Fire field\", \"Paralyze field!\")")),{"top":32,"pad":2}),ac("traps"))
		def bb(w):return az
		bc=Kit.Page(d,bb,N)
		def bd(g,x,y,w):j["f"]=Kit.Form(g,x,y,w,d,az);j["gfx_typed"],j["gfx_applied"]=None,O();n()
		def be():
			g=j["f"]
			if g is None:return
			b=g.read();f=g.c;i=time.time()
			try:c=str(f["graphics"].Text or "");e=int(f["cycle"].Value);k=bool(f["paused"].IsChecked)
			except Exception:return
			e=max(5,min(100,e))/10.
			if abs(e-d["cycle"])>.01:b["cycle"]=e;h(f["cycle_v"],"%.1f s"%e)
			if c!=j["gfx_typed"]:j["gfx_typed"],j["gfx_since"]=c,i
			elif i-j["gfx_since"]>=.7 and c!=j["gfx_applied"]:j["gfx_applied"]=c;b["graphics"]=(ap(c)or d["graphics"])if c.strip()else[]
			if k!=(a["paused"]if a["pause_want"]is None else a["pause_want"]):a["pause_want"]=k
			if b["ping"]!=d["ping"]:a["ping_wait"]=[w for w in a["tracked"]if w not in a["pinged"]]if b["ping"]else[]
			if b==d:return
			d.update(b);a["last_scan"]=0.;N();aP();n()
		def bf():j["f"]=None;j["gfx_typed"]=None
		def bg():
			a.update({"shutting":False,"docked":False,"queue":[],"last_scan":0.,"hue_at":0.,"moved":False,"tracked":{},"pinged":set(),"pinged_spots":set(),"ping_wait":[],"ping_sent":0,"ping_noted":False,"ping_svc":u(),"ping_next":0.,"fields":{},"field_said":[],"alerted":set(),"atlas_traps":[],"atlas_ver":0,"atlas_done":-1,"atlas_map":None,"pause_want":None});r.clear();aN();aO();ag(am,"New trap in range",495);aQ();al(a,"hooked",("OnItemCreated",bi),("OnPositionChanged",bj))
			if au(X):a["minimized"]=True
			ax();p.dock(fit=True,min=(320,B))
		def bh():
			if s["g"]is None:return
			if V(s):return
			b=a["pause_want"]
			if b is not None:
				a["pause_want"]=None
				if b!=a["paused"]:
					a["paused"]=b
					if b:aw();a["ping_wait"]=[]
					else:a["last_scan"]=0.
					aq();n()
			while a["queue"]:
				e=a["queue"].pop(0)
				if not p.action(e):a8[e]()
			if a["paused"]:return
			f=time.time();c=f-a["last_scan"]
			if c>=aF or(a["moved"]and c>=aE)or(a["poke"]and c>=aD):
				a["last_scan"]=f;a["poke"]=a["moved"]=False;g=(len(a["tracked"]),len(a["fields"]));aT();d=u()
				if(len(a["tracked"]),len(a["fields"]))!=g or(d is None)!=(a["ping_svc"]is None):
					a["ping_svc"]=d
					if d is not None:a["ping_noted"]=False
					n()
				if a["atlas_ver"]!=a["atlas_done"]:a["atlas_done"]=a["atlas_ver"];aV()
			a1();a0()
		def bi(*b):
			if a["poke"]or a["paused"]or a["shutting"]:return
			for c in b:
				try:g=int(c.Graphic)
				except Exception:continue
				if g in ar["wanted"]or(d["fields"]and g in M):a["poke"]=True
				return
		def bj(*b):a["moved"]=True
		def bk():a["shutting"]=True;aw();N();an.close()
		return{"start":bg,"tick":bh,"stop":bk,"client_tick":True,"config_height":bc.height,"build_config":bd,"poll_config":be,"config_closed":bf}
	aZ=(("pings",aU,.05,"pings"),("corpse",lambda:ad(aV(),"corpse"),.25,"corpserun"),("maps",lambda:ad(aW(),"maps"),.2,"treasure"),("dry",lambda:ad(aX(),"dry"),.2,"harvest"),("traps",lambda:ad(aY(),"traps"),.1,"traphl"),);return PartSet(aL,aE,aZ,shared=aS).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("worldmap","World Map","Pings, corpse, dig and dry spots, traps",_module_worldmap,.05,category="The world",parts=(("pings","Map Pings","Guild pings on your Enhanced Map",False,("pings",)),("corpse","Corpse","Arrow, decay time and Get my things",False,("corpserun",)),("maps","Treasure Maps","Dig spots of your decoded maps",False,("treasure",)),("dry","Ore Tracker","Your weight and spots that ran dry",False,("harvest",)),("traps","Traps & Fields","Traps and magic fields recoloured",False,("traphl",)),),aliases=('Map Pings','Corpse Run','Treasure Hunter','Harvest Helper','Dry spots','Ore Tracker','Trap Highlight','Enhanced Map','tracking arrow','ping','corpse','dig spot','weight bar','TazUO World Map'))
