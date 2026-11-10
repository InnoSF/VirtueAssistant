def _module_ultima():
	av=Client.key_held;ad=Follow.alt_held;P=Follow.current;aw=Follow.toggle;ae=HOST.alert;af=HOST.alert_kind;ax=HOST.dock_add;M=HOST.dock_forget;ay=HOST.dock_remove;az=HOST.dock_to_bar;ag=HOST.harm_ok;C=HOST.layout_holds;Q=HOST.me;aA=HOST.mobile;ah=HOST.mobiles;aB=HOST.refresh_settings;ai=HOST.show_settings;V=HOST.stopping;X=Journal.reader;aC=Kit.AGO_SHORT;N=Kit.ART_CLOSE;aj=Kit.ART_MIN;ak=Kit.ART_OK;H=Kit.ART_PAGE;al=Kit.ART_PLAY;aD=Kit.ART_RESTORE;aE=Kit.CORNER_ART;aF=Kit.DOUBLE_TIP;I=Kit.GAP;f=Kit.HUE_BAD;l=Kit.HUE_GOOD;o=Kit.HUE_INFO;K=Kit.HUE_TEXT;am=Kit.HUE_TITLE;p=Kit.MARGIN;an=Kit.MIN_TIP;Y=Kit.SECTION_TILE;aG=Kit.SETTINGS_TIP;ao=Kit.STONE_TILE;aH=Kit.WINDOW_BG;A=Kit.add_label;J=Kit.add_section;aI=Kit.add_window_frame;ap=Kit.ago;E=Kit.art_button;aJ=Kit.basics;Z=Kit.catcher;aq=Kit.clamp;L=Kit.count;aK=Kit.data_path;D=Kit.dispose;aL=Kit.dock_hooks;aM=Kit.drop_arrow;ar=Kit.facet_name;u=Kit.fit;z=Kit.is_open;aN=Kit.load_min;aO=Kit.load_pos;aP=Kit.look_hue;aQ=Kit.mini_bar;aR=Kit.moved_by_code;R=Kit.noto_name;at=Kit.on_moved;S=Kit.pic_size;au=Kit.put_var;aa=Kit.save_min;ab=Kit.save_pos;B=Kit.set;j=Kit.set_text;aS=Kit.show_window;O=Kit.text_w;T=Kit.was_clicked;aT=Kit.where_text;F=Kit.with_tip;aU=Kit.write_safe;ac=Kit.zone_up;aX="ultima";aY="Ultima Tracker";aV=re.compile(r"\bthe\s+[a-z]",re.IGNORECASE);U={"murderer":"red","criminal":"grey","gray":"grey","enemy":"orange","innocent":"blue","ally":"green","invulnerable":"yellow"};aW={"murderer":34,"criminal":946,"gray":946,"enemy":144,"innocent":89,"ally":63,"invulnerable":53}
	def aZ():
		fH="ultima";bj="Ultima Tracker";fI=bj+":";ca=.25;fJ=.15;fK=.05;fL=.45;dW=3.;bB=85;c7,c8=50,200;c9,da=1,24;fM=32;db=210;dc=90;fN=200;fO=18;fP=12;dX=14;fQ=8;dY=220;fR=16;fS=11;bK=170;ct=600;cu=1;dd=10;de=5.;df=12;dZ=18;fT=20.;fU=12;fV=2;fW=("invulnerable",);fX=("innocent","ally");fY=[API.Notoriety.Gray,API.Notoriety.Criminal,API.Notoriety.Enemy,API.Notoriety.Murderer];d_="ultima.foe";fZ=743;dg,dh=1,60;cv=2000;f_=200;di=60.;d0=30.;cw=12;d1=30.;f0=5365;dj=60.;f1=60.;f2=6;f3=40;d2=30.;d3=160;f4={0:"Fel",1:"Tram",2:"Ilsh",3:"Malas",4:"Tok",5:"TerM"};dk=(("All players",None),("Red only",("murderer",)),("Grey only",("gray","criminal")),("Orange only",("enemy",)),("Blue only",("innocent",)),("Foe list","foe"));dl=(("Last hour",3600.),("Today","today"),("All time",None));dm="UltimaTracker_sight_pos";cx="UltimaTracker_sight_min";cy="UltimaTracker_sight_open";dn="UltimaTracker_killer_pos";do="UltimaTracker_killer_min";f5=.5;cz=6;cA=("friend","foe","neutral","combat","panel");f6=4;f7=10;dp=2000;dq=5000;f8=4000;d4=4000;f9=1.;a0=6;ga=24;d5=13;gb=20;cb="#3A3A3A";cB="#5E4E24";d6="#DDDDDD";gc="#F0C850";gd="#A8A8A8";cC="#DDDDDD";cD="#999999";ge="#7D6E52";d7={"friend":"Friends","foe":"Foes","neutral":"Neutral","combat":"Combat"};d8={"friend":"#5CE65C","foe":"#FF5050","neutral":"#9EC8FF","combat":"#FFB050","panel":"#FFD966"};cc={"friend":"#3AA0D4","foe":"#D93030","neutral":"#B8B8B8","combat":"#B32D2D"};cE="#2E9E3A";d9="#FF2020";gf=50;gg=1.2;ea,gh=.1,.55;eb=32;gi=.1;ec="#B8902A";ed="#2A8C9E";ee="#D8CCB0";ef=3617;gj=1;gk=3.;gl=3.5;cF="#3A6FD8";eg="#21A39A";dr="#555555";cG={"innocent":"#4FA3FF","ally":"#40E040","gray":"#B0B0B0","criminal":"#B0B0B0","enemy":"#FF9A2E","murderer":"#FF4040","invulnerable":"#FFE14D","unknown":"#DDDDDD",};gm,gn=10,18;go=aH;gp=Y;gq=Y;cd=3;gr=ao;eh=2092;gs=.6;gt=(aj[0],aD[0]);gu=(2103,2104);ds=1153;gv={cb:0,cB:53,ec:53,ed:89,ee:0,cE:63,cF:1152};gw=[((235,235,235),1153),((150,150,150),946),((225,55,55),34),((70,220,70),63),((90,150,255),89),((255,155,45),144),((255,220,80),53),((25,25,25),0)];bv=aK("_ultima_tracker_data.txt");ei=os.path.join(Kit.script_dir(),"_player_tracker_data.txt");bk=["friend","foe","neutral"];ej={"scale":(c7,c8),"opacity":(0,100),"range":(c9,da),"alert_minutes":(dg,dh)};ek=("scale","opacity","range","alert_minutes");el=("sync","magery","combat_shown","combat_only","healing","borders","alert_red","alert_foes","alert_orange","alert_gray","sightings","killer");dt={"friend":[40,140,240,220,False,False,bB],"foe":[290,140,240,220,False,False,bB],"neutral":[540,140,240,220,False,False,bB],"combat":[300,200,dY,0,False,False,bB],"panel":[40,380,0,0,False,False,bB],};aY={};bs={};aC={ie:list(ig)for ie,ig in dt.items()};ar={"scale":100,"opacity":bB,"range":18,"sync":False,"magery":False,"combat_shown":True,"combat_only":True,"healing":False,"borders":True,"alert_red":True,"alert_foes":True,"alert_orange":False,"alert_gray":False,"alert_minutes":5,"sightings":True,"killer":True};em=dict(ar);gx={"dirty_save":False,"foe_ver":0,"combat_loaded":False,"shutting":False,"started":False,"loaded":False};aM={"minimized":False,"shutting":False,"docked":False,"queue":[],"dirty_save":False,"foe_ver":0,"combat_loaded":False,"started":False,"loaded":False,"party":set()};h9={"g":None,"c":{},"store":({},{})};bT,ia,aX=aJ(aM,bj);a8={};ce=[];du=[];cH=p+30+I;en=2*p+30
		def gy(*a):du.append(True)
		bC={};ba={};bl=[];bb={};a1={};a3={"ver":0,"seen_ver":0,"dirty":False,"save_at":0.};bU={};cf={};cg={};cI=set();bc={};bD=[None]
		def sc(v,scale=None):s=ar["scale"]if scale is None else scale;return max(1,int(round(v*s/100.)))
		gz=13;dv=20
		def cJ(s):return s if s>1. else 1.
		def cK(v):return sc(v)if ar["scale"]>100 else int(v)
		def eo(text,width):width=max(20,int(width));return[u(a,width)for a in Kit.wrap(text,width)]
		def ep(parent,lines,x,y):a=cN(cD);return[bL(A(parent,c,x,y+b*dv,a))for b,c in enumerate(lines)]
		a_={"req":False,"size":{},"own_size":{},"force":set(),"made":{}};gA=3
		def eq():
			for k,v in dt.items():aC[k]=list(v)
		def er():a6.clear();ar.update(em);a_["req"]=False;a5["serial"]=None;eq()
		def bx(v,lo,hi):return max(lo,min(hi,v))
		def ch():return API.StopRequested
		es=("lord ","lady ")
		def a2(name):
			n=(name or "").strip().lower()
			for p in es:
				if n.startswith(p):n=n[len(p):]
			return n
		def dw(text,n):return text if len(text)<=n else text[:max(1,n-2)]+".."
		def bL(c):c.SetAcceptMouseInput(False);return c
		def ci(text,size,color,**a):return bL(API.Gumps.CreateGumpTTFLabel(text,size,color,**a))
		def bM(opacity,color):return bL(API.Gumps.CreateGumpColorBox(opacity,color))
		def bE(b,a):
			try:b.SetAlpha(a)
			except Exception:pass
		def bt(c):bm.pop(id(c),None);D(c)
		cL=[];gB=.15;bV={}
		class RowClick(object):
			__slots__=("row","make")
			def __init__(self,row,make):self.row,self.make=row,make
			def bind(self):
				r=self.row;b,c=r.serial,r.name;a=r.prev
				if a is not None and time.time()-a[2]<gB:b,c=a[0],a[1]
				if b is None:return
				return self.make(b,c)
		def gC():return{"alt":ad(),"shift":bool(av("shift"))}
		def a9(fn):
			def a(*a):
				f=fn.bind()if type(fn)is RowClick else fn
				if f is not None:cL.append((f,gC()))
			return a
		def et(c,fn):Kit.on_click(c,a9(fn))
		def gD():
			while cL:
				a,b=cL.pop(0);bV.clear();bV.update(b)
				try:a()
				except Exception as c:
					if V():return
					bW(c)
				finally:bV.clear()
		def bW(b):
			a=str(b)
			if a not in bi["errors"]:bi["errors"].add(a);aX("error (still running): "+a,f)
		bX=[False];cj=[];bY=[]
		def eu(q):
			while q:
				a=q.pop(0)
				try:a()
				except Exception as b:
					if V():return True
					bW(b)
		def bz(x,y,w,h,fn,tip=None):c=API.Gumps.CreateGumpColorBox(.01,"#000000");c.SetRect(x,y,w,h);et(c,fn);return F(c,tip)
		def cM(graphic,x=0,y=0,hue=0):return bL(API.Gumps.CreateGumpPic(graphic,x,y,aP(graphic,hue)))
		def bq(graphic,w,h,hue=0):return bL(API.Gumps.CreateTiledGumpPic(graphic,max(0,w),max(0,h),aP(graphic,hue)))
		def gE():
			ba.clear();e=ba["icons"]={}
			for f,b in(("lock",(eh,eh)),("min",gt),("opacity",gu)):
				c=[S(i)for i in b]
				if all(g and k for g,k in c):e[f]=list(zip(b,c))
			d="Name the 75% PSN 12y Foes (3)";a=API.Gumps.CreateGumpLabel(d,ds);w,h=int(a.GetWidth()),int(a.GetHeight());a.Dispose()
			if w>0 and h>0:ba["char_w"]=w/float(len(d));ba["font_h"]=h
		dz={}
		def cN(color):
			h=dz.get(color)
			if h is not None:return h
			c=color.lstrip("#");r,g,e=int(c[0:2],16),int(c[2:4],16),int(c[4:6],16);a,b=ds,None
			for(f,i,j),k in gw:
				d=(f-r)**2+(i-g)**2+(j-e)**2
				if b is None or d<b:a,b=k,d
			if len(dz)<256:dz[color]=a
			return a
		ev={}
		def gF(color):
			v=ev.get(color)
			if v is None:c=color.lstrip("#");v=ev[color]=(int(c[0:2],16),int(c[2:4],16),int(c[4:6],16))
			return v
		def cO(size):return "char_w"in ba and gm<=size<=gn
		def gG(size):return ba["char_w"]if cO(size)else size*.58
		bm={};ew=[d4]
		def bn(text,size,color,aligned="left",maxWidth=0,applyStroke=False):
			if applyStroke or not cO(size):a=ci(text,size,color,aligned=aligned,maxWidth=maxWidth,applyStroke=applyStroke);bm.pop(id(a),None);return a
			if len(bm)>ew[0]:
				for k,v in list(bm.items()):
					if v[0].IsDisposed:del bm[k]
				ew[0]=max(d4,2*len(bm))
			text=ex(text,maxWidth);a=bL(API.Gumps.CreateGumpLabel(text,cN(color)));bm[id(a)]=[a,aligned,maxWidth,size,0,0,text];return a
		def dA(a):m=bm.get(id(a));return m if m is not None and m[0]is a else None
		def ex(text,a):
			if a and len(text)*ba.get("char_w",7)>a:return dw(text,max(2,int(a/ba.get("char_w",7))))
			return text
		def bd(b,x,y,text=None):
			m=dA(b)
			if m is None:b.SetPos(x,y);return
			m[4],m[5]=x,y;d,a,f=m[1],m[2],m[3]
			if text is None:text=m[6]
			e=int(len(text)*ba["char_w"]);c=0
			if a and d=="right":c=max(0,a-e)
			elif a and d=="center":c=max(0,(a-e)//2)
			g=int(round((f*1.35-ba["font_h"])/2.));b.SetPos(int(x+c),int(y+g))
		def bA(a,text):
			m=dA(a)
			if m is None:a.SetText(text);return
			text=ex(text,m[2])
			if text==m[6]:return
			m[6]=text;a.Text=text
			if m[1]!="left"and m[2]:bd(a,m[4],m[5],text)
		def ey(a,color):
			if dA(a)is None:return False
			a.Hue=cN(color);return True
		def ez():return bool(bV.get("shift")or av("shift"))
		def bu():return bV.get("alt")or ad()
		def gH():return[a for a in bk+["combat","panel"]if C("hub"if a=="panel"else "ultima."+a)]
		def cP():return bool(SNAP.drag)or SNAP.pressed()is True
		cQ={};gI=2000
		def cR(text,px,size,smooth=False):
			if size>gz and(smooth or not cO(size)):b=size*.6 if smooth else gG(size);return dw(text,max(4,int(px/b)))
			k=(text,px);a=cQ.get(k)
			if a is None:
				if len(cQ)>gI:cQ.clear()
				a=cQ[k]=u(text,max(10,int(px)))
			return a
		def bZ(top,h,font):return top+max(0,int((h-font*1.35)/2))
		def bN(parent,x,y,w,h,text,fn,tip=None,face=cb,color=cC,font=12,store=None):
			f=bq(gr,w,h,gv.get(face,cN(face)));f.SetPos(x,y);color="#141414";parent.Add(f);a=bn(text,font,color,aligned="center",maxWidth=w);bd(a,x,bZ(y,h,font));parent.Add(a);c=bz(x,y,w,h,fn,tip);parent.Add(c)
			if store is not None:store.extend([f,a,c])
			return a
		def cS():return(2 if ar["magery"]else 0)+(1 if ar["healing"]else 0)
		bF="Alt+click: auto-follow (again to stop)";gJ=("Cast Heal on %s (Shift+click: Greater Heal). Alt+click: auto-follow (again to stop)");gK=("Cast Cure on %s (Shift+click: Arch Cure). Alt+click: auto-follow (again to stop)");gL="Bandage %s when adjacent; farther away, follow them (again to stop). "+bF
		def eA(parent,x,y,w,h,serial,name,store=None,row=None):
			j=max(7,int(h*.7/min(1.,ar["scale"]/100.)));e,b,f=[],[],[]if store is None else store
			if ar["magery"]:
				for c,g,i,a,d in(("H","Heal","Greater Heal",gJ,ec),("C","Cure","Arch Cure",gK,ed)):b.append((c,fs(serial,g,i)if row is None else RowClick(row,(lambda a,st:lambda s,n:fs(s,a,st))(g,i)),a,d,"#FFFFFF"))
			if ar["healing"]:b.append(("B",eD(serial,name)if row is None else RowClick(row,eD),gL,ee,"#202020"))
			for c,k,a,d,l in b:bN(parent,x,y,w,h,c,k,a%name,face=d,color=l,font=j,store=f);e.append((f[-1],a));x+=w+2
			return e
		def eB(s):return max(16,int(round(ga*s)))
		def eC(s):return max(16,int(round(gb*s)))
		def gM(serial):
			if safe(P)==serial:return True
			return Follow.start(serial,bj)
		def b_(serial):aw(serial,bj)
		def ck(serial,fn):
			def a(*a):
				if bu():b_(serial)
				else:fn()
			return a
		a5={"serial":None,"name":"","state":None,"until":0.,"follow":None}
		def cl(serial):
			if serial is None or a5["follow"]!=serial:return
			a5["follow"]=None
			if safe(P)==serial:Follow.stop(bj)
		def eD(serial,name):
			def a(*g):
				if a5["serial"]==serial:a5["serial"]=None;bG("bandage");cl(serial);aX("stopped bandaging %s; cursor released."%name,l);return
				try:
					a=API.FindMobile(serial)
					if a is None or bool(a.IsDead):a=None
					else:b=API.Player;d=max(abs(int(a.X)-int(b.X)),abs(int(a.Y)-int(b.Y)))
				except Exception:a=None
				if a is None:aX("can't bandage %s (out of sight or dead)."%name,f);return
				if d>gj:
					if a5["follow"]==serial and safe(P)==serial:cl(serial);aX("stopped following %s."%name,l);return
					e=safe(P)!=serial
					if not gM(serial):return
					if e:a5["follow"]=serial
					aX("following %s; press B again when adjacent."%name,o);return
				c=API.FindType(ef,API.Backpack)or API.FindType(ef)
				if not c:aX("no bandages in your backpack.",f);return
				if a5["serial"]is not None or cU()is not None or API.HasTarget("any"):aX("a target cursor is up; clear it, then press B.",f);return
				API.UseObject(c);a5.update(serial=serial,name=name,state="cursor",until=time.time()+gk);eE("bandage",gl)
			return Kit.once(ck(serial,a),("ultima.bandage",serial),Kit.TWICE)
		cT="ultima";bO={"bandage":False,"spell":False}
		def eE(what,a):bO[what]=True;HOST.claim_cursor(cT,a)
		def bG(what):
			if not bO.get(what):return
			bO[what]=False
			if not any(bO.values()):HOST.release_cursor(cT)
		def cU():return HOST.cursor_busy(cT)
		def eF():
			a=cU()
			if a is not None and a!="pick":return False
			return bool(API.HasTarget("any"))
		def gN():
			s=a5["serial"]
			if s is None:bG("bandage");return
			c=a5["name"]
			try:b=API.FindMobile(s);a=b is None or bool(b.IsDead)
			except Exception:a=True
			if a or time.time()>a5["until"]:a5["serial"]=None;cl(s);aX(("can't bandage %s (out of sight or dead)."if a else "no target cursor for bandaging %s.")%c,f);return
			if a5["state"]=="cursor"and bO["bandage"]and HOST.cursor_ok(cT,"beneficial"):API.Target(s);a5["serial"]=None;bG("bandage");cl(s)
		def gO():
			safe(P);s=Follow.serial
			if s is not None and aA(s)is None:Follow.serial=None
			if a5["follow"]is not None and Follow.serial!=a5["follow"]:a5["follow"]=None
		eG=((3,4,3,8,"#FFFFFF"),(6,4,3,8,"#A0A0A0"),(9,4,3,8,"#5A5A5A"));gP={("lock",True):((3,8,10,6,None),(7,10,2,2,cB),(4,2,8,2,None),(4,2,2,6,None),(10,2,2,6,None)),("lock",False):((3,8,10,6,None),(7,10,2,2,cb),(4,0,8,2,None),(4,0,2,8,None),(10,0,2,3,None)),("min",True):((4,4,8,2,None),(4,4,1,8,None),(11,4,1,8,None),(4,11,8,1,None)),("min",False):((4,10,8,2,None),),("opacity",True):eG,("opacity",False):eG}
		def gQ(add,d,x,y,a,kind,on):
			u=a/16.
			def R(v):return int(round(v*u))
			def S(v):return max(1,int(round(v*u)))
			e=(gc if on else gd)if kind=="lock"else d6
			for f,g,h,i,j in gP.get((kind,bool(on)),()):add(x+R(f),y+R(g),S(h),S(i),j or e)
			if kind=="close":b=max(8,int(a*.8));c=ci("x",b,d6,aligned="center",maxWidth=a);c.SetPos(x,y+max(0,int((a-b*1.35)/2)));d(c)
		cm={};bH=[]
		def eH():
			for c in list(bH):
				if c.gump.IsDisposed:bH.remove(c)
				else:c.frame.apply_borders()
		class Frame(object):
			def __init__(self,gump):
				self.size=(0,0);self.center=bq(gp,1,1);gump.Add(self.center);self.edges=[bq(go+(1 if a in(0,1)else 3),1,1)for a in range(4)]
				for b in self.edges:gump.Add(b)
			def layout(self,w,h):
				self.size=(w,h);a=[(0,0,w,a0),(0,h-a0,w,a0),(0,0,a0,h),(w-a0,0,a0,h)]
				for b,r in zip(self.edges,a):b.SetRect(*r)
				self.apply_borders()
			def apply_borders(self):
				a=ar["borders"]
				for p in self.edges:bE(p,1. if a else 0.)
				w,h=self.size
				if a:self.center.SetRect(a0,a0,max(0,w-2*a0),max(0,h-2*a0))
				else:self.center.SetRect(0,0,w,h)
			def set_alpha(self,a):bE(self.center,a)
		class KitFrame(object):
			def __init__(self,gump,key=None):
				self.gump,self.key=gump,key;self.top=0;a=aH;self.s=[S(a+b)for b in range(9)];self.kw,self.kh=S(aE);self.fill=bq(a+4,1,1);self.center=bq(Y,1,1);self.edges=[bq(a+d,1,1)for d in(1,7,3,5)];self.corners=[cM(a+e,0,0)for e in(0,2,6,8)];self.knots=[cM(aE,0,0)for g in range(4)];self.parts=[self.fill]+self.edges+self.corners+self.knots
				for c in[self.fill,self.center]+self.parts[1:]:gump.Add(c)
				Kit._frame_parts[gump]=self.parts
			def layout(self,w,h,top=None):
				if top is not None:self.top=top
				M=p;a,t,b,l,n,r,c,f,d=self.s;self.fill.SetRect(l[0],t[1],max(0,w-l[0]-r[0]),max(0,h-t[1]-f[1]))
				for j,e in zip(self.edges,((a[0],0,w-a[0]-b[0],t[1]),(c[0],h-f[1],w-c[0]-d[0],f[1]),(0,a[1],l[0],h-a[1]-c[1]),(w-r[0],b[1],r[0],h-b[1]-d[1]))):j.SetRect(e[0],e[1],max(0,e[2]),max(0,e[3]))
				for k,g in zip(self.corners,((0,0),(w-b[0],0),(0,h-c[1]),(w-d[0],h-d[1]))):k.SetPos(*g)
				for m,g in zip(self.knots,((0,0),(w-self.kw,0),(0,h-self.kh),(w-self.kw,h-self.kh))):m.SetPos(*g)
				i=h-self.top-M;self.center.SetRect(M,self.top,max(0,w-2*M),max(0,i));B(self.center,"IsVisible",i>4)
			def apply_borders(self):pass
			def set_alpha(self,a):bE(self.center,a)
			def drop_all(self):
				for c in[self.center]+self.parts:bt(c)
				if Kit._frame_parts.get(self.gump)is self.parts:Kit._frame_parts.pop(self.gump,None)
		class Chrome(object):
			def __init__(self,gump,kit=False,key=None):self.gump=gump;self.kit,self.key=kit,key;self.frame=KitFrame(gump,key)if kit else Frame(gump);bH[:]=[a for a in bH if a.gump is not gump and not a.gump.IsDisposed];bH.append(self);self.strip=[];self.title_bg=self.title_lbl=self.slider=self.pct_lbl=None;self.title_text=self.title_color=self.title_raw=self.status_x=None;self.status_lbl=self.status_text=None;self.title_max,self.title_pos,self.font=40,(0,0),d5;self.opacity,self.content_top=bB,a0;self.on_title_alt,self.alt_key=None,None
			def _add(self,ctrl):self.gump.Add(ctrl);self.strip.append(ctrl);return ctrl
			def _clear_strip(self):
				for c in self.strip:bt(c)
				self.strip=[];self.title_bg=self.title_lbl=self.slider=self.pct_lbl=None;self.status_lbl,self.status_text=None,None
			def dispose(self):
				self._clear_strip();self.frame.drop_all()
				if self in bH:bH.remove(self)
			def layout(self,w,h,s,opacity,title,color,buttons,l,m,o,p):
				self.opacity=opacity;g=opacity/100.;self.frame.layout(w,h);self.frame.set_alpha(g);self._clear_strip();a=eB(s);self.title_bg=self._add(bq(gq,w-2*a0,a));self.title_bg.SetPos(a0,a0);bE(self.title_bg,g);q=self._add(bq(ao,w-2*a0,cd));q.SetPos(a0,a0+a-cd);b=max(12,a-6-cd);i=max(2,int(round(2*s)));n=len(buttons);e=w-a0-4-n*b-max(0,n-1)*i;j=e;self.on_title_dbl=m;self.on_title_alt,self.alt_key=o,p;self._title_catch(a0,max(10,j-a0-2),a,aF+". "+bF);r=a0+(a-cd-b)//2
				for t,u,v,x in buttons:self._button(e,r,b,t,u,v,x);e+=b+i
				self.font=max(9,int(round(d5*cJ(s))));self.title_max=max(20,j-a0-10);self.title_pos=(a0+5,bZ(a0,a-cd,self.font));self.title_color=color;self.title_text=None;self.set_title(title);y=a0+a
				if l:c=eC(s);d=max(8,int(round(11*cJ(s))));z=self._add(bn("Opacity",d,cD));bd(z,a0+5,bZ(y,c,d));f=int(round(34*s));k=a0+int(round(54*s));A=max(40,w-a0-8-f-k);self.slider=API.Gumps.CreateSlider(A,0,100,opacity,k,y+max(2,(c-10)//2),True);self._add(self.slider);self.pct_lbl=self._add(bn("%d%%"%opacity,d,cC,aligned="right",maxWidth=f));bd(self.pct_lbl,w-a0-4-f,bZ(y,c,d));y+=c
				self.content_top=y
			def _title_catch(self,xy,w,h,tip):
				a=bz(xy,xy,w,h,self._title_clicked,tip);B(a,"CanMove",True)
				if Client.mouse is None:Kit.hook_double(a,self._dbl_once())
				self._add(a)
			def _dbl_once(self):return Kit.once(lambda:self.on_title_dbl(),("utitle",id(self)))
			def layout_kit(self,w,h,opacity,title,color,mini,d,i):
				M=p;self._clear_strip();self.content_top=cH;self.frame.layout(w,h,cH);self.frame.set_alpha(opacity/100.);e=self._add(bq(Y,w-2*M,30));e.SetPos(M,M);bE(e,Kit.SECTION_ALPHA)
				if not mini:self._add(bM(1.,color)).SetRect(M,M+30,w-2*M,3)
				a=w-M-54
				if not ac(self.key):
					self._art((aD if mini else aj)[0],a,M+7,d,Kit.RESTORE_TIP if mini else an);a-=Kit.DOCK_DX
					if not mini:self._art(Kit.ART_DOCK[0],a,M+7+Kit.DOCK_DY,i,Kit.DOCK_TIP);a-=10
				b=a
				if not mini:
					f="Settings";c=a-35-O(f)
					if c>M+30+O("COMBAT")+40:self._art(H[0],c,M+4,gy,aG%bj,f);b=c
				g=ac(self.key);self.on_title_dbl=(lambda:None)if g else d;self._title_catch(M,max(10,b-M-6),30,None if g else aF);self.title_max=max(20,b-M-30-10);self.title_pos=(M+30,M+7);self.title_color=color;self.title_text=None;self.set_title(title)
			def _art(self,graphic,x,y,fn,tip,cap=None):
				p=self._add(cM(graphic,x,y));a,b=S(graphic);a,b=a or 20,b or 20
				if cap:c=A(self.gump,cap,x+a+5,y+3,K);self.strip.append(c);a+=5+O(cap)
				self._add(bz(x,y,a,b,fn,tip));return p
			def set_status(self,text):
				if not self.kit or self.title_lbl is None:return
				text=text or ""
				if text==self.status_text:return
				self.status_text=text;x=self.title_pos[0]+O(self.title_text or "")+12;b=self.title_pos[0]+self.title_max-x;c=u(text,b)if b>20 else "";a=(x,self.title_pos[1])
				if self.status_lbl is None:self.status_lbl=A(self.gump,c,x,self.title_pos[1],o);self.strip.append(self.status_lbl);self.status_x=a
				else:
					if a!=self.status_x:self.status_x=a;self.status_lbl.SetPos(x,self.title_pos[1])
					j(self.status_lbl,c)
			def _title_clicked(self,*h):
				f=time.time();d=id(self.gump);a=(self.gump.GetX(),self.gump.GetY())
				if self.on_title_alt is not None and bu():
					b=self.alt_key;e=a6.pos.get(b)if b is not None else None;g=(b is not None and a6.moving==b)or SNAP.drag or(e is not None and(abs(a[0]-e[0])>cz or abs(a[1]-e[1])>cz))
					if not g:self.on_title_alt()
					return
				c=cm.get(d)
				if c and f-c[0]<=f5 and abs(a[0]-c[1][0])<=cz and abs(a[1]-c[1][1])<=cz:cm.pop(d,None);self._dbl_once()()
				else:
					if len(cm)>dp:cm.clear()
					cm[d]=(f,a)
			def _button(self,x,y,a,kind,on,fn,tip):
				b=ba.get("icons",{}).get(kind)
				if b:
					e,(c,d)=b[1 if on else 0]
					if c<=a+6 and d<=a+6:
						f=34 if kind=="lock"and on else 0;p=self._add(cM(e,x+(a-c)//2,y+(a-d)//2,f))
						if kind=="lock"and not on:bE(p,gs)
						self._add(bz(x,y,a,a,fn,tip));return
				if kind=="close"and "char_w"in ba:g=bL(self._add(API.Gumps.CreateGumpLabel("x",ds)));g.SetPos(x+max(0,(a-int(ba["char_w"]))//2),y+(a-ba["font_h"])//2);self._add(bz(x,y,a,a,fn,tip));return
				h=on and kind in("lock","opacity");i=self._add(bM(1.,cB if h else cb));i.SetRect(x,y,a,a)
				def j(a,by,bw,bh,col):p=self._add(bM(1.,col));p.SetRect(a,by,bw,bh)
				gQ(j,self._add,x,y,a,kind,on);self._add(bz(x,y,a,a,fn,tip))
			def set_title(self,text,color=None):
				if self.kit:
					b=(text,self.title_max)
					if self.title_lbl is not None and b==self.title_raw:return
					self.title_raw=b;text=u(str(text).upper(),self.title_max)
					if self.title_lbl is None:self.title_lbl=A(self.gump,text,self.title_pos[0],self.title_pos[1],am);self.strip.append(self.title_lbl);self.title_text=text
					elif text!=self.title_text:
						self.title_text=text;j(self.title_lbl,text)
						if self.status_text is not None:c,self.status_text=self.status_text,None;self.set_status(c)
					return
				if color is not None and color!=self.title_color:
					self.title_color=color;a=self.title_lbl
					if a is not None and not ey(a,color):
						self.title_text=None
						if a in self.strip:self.strip.remove(a)
						bt(a);self.title_lbl=None
				text=cR(text,self.title_max,self.font)
				if self.title_lbl is None:self.title_lbl=self._add(bn(text,self.font,self.title_color or cC));bd(self.title_lbl,*self.title_pos);self.title_text=text
				elif text!=self.title_text:self.title_text=text;bA(self.title_lbl,text)
			def set_opacity(self,v):
				self.opacity=v;a=v/100.;self.frame.set_alpha(a)
				if self.kit:return
				if self.title_bg is not None:bE(self.title_bg,a)
				if self.pct_lbl is not None:bA(self.pct_lbl,"%d%%"%v)
			def poll(self):
				if self.slider is None:return
				v=bx(int(self.slider.Value),0,100)
				if v!=self.opacity:self.set_opacity(v);return v
				return
		class Anchors(object):
			def __init__(self):self.gid,self.next_gid,self.pos,self.dims={},1,{},{};self.moving,self.still,self.linger,self.saved=None,0,0,[];self.pending=self.alt_used=self.touched=False
			def placed(self,key,x=None,y=None,w=None,h=None):
				if x is None:self.pos.pop(key,None)
				else:self.pos[key]=(int(x),int(y))
				if w is None:self.dims.pop(key,None)
				else:self.dims[key]=(int(w),int(h))
				self.pending=True
			def sized(self,key,w,h):self.dims[key]=(int(w),int(h))
			@staticmethod
			def host_follows(g):
				a=set()
				if not SNAP.enabled or g in SNAP.no_snap:return a
				c,d=SNAP.links,SNAP.members;b=[g]
				while b:
					e=b.pop()
					for f,l in list(c.items()):
						if l is e and f is not g and f not in a and f in d:a.add(f);b.append(f)
				return a
			def add_group(self,keys):
				g=self.next_gid;self.next_gid+=1
				for k in keys:self.gid[k]=g
			def members(self,key):
				g=self.gid.get(key)
				if g is None:return[key]
				return[a for a,b in self.gid.items()if b==g]
			def join(self,a,b):
				c,d=self.gid.get(a),self.gid.get(b)
				if c is None and d is None:self.add_group([a,b])
				elif c is None:self.gid[a]=d
				elif d is None:self.gid[b]=c
				elif c!=d:
					for k,v in list(self.gid.items()):
						if v==d:self.gid[k]=c
				self.touched=True
			def detach(self,key):
				g=self.gid.pop(key,None)
				if g is not None:
					self.touched=True;a=[b for b,c in self.gid.items()if c==g]
					if len(a)==1:self.gid.pop(a[0],None)
			def clear(self):self.gid={};self.touched=True
			def saved_groups(self):
				a={}
				for k,g in self.gid.items():
					if k in cA:a.setdefault(g,[]).append(k)
				return[sorted(b)for b in a.values()if len(b)>1]
			def groups_changed(self):
				if not self.touched:return False
				self.touched=False;a=self.saved_groups()
				if a==self.saved:return False
				self.saved=a;return True
			@staticmethod
			def shift(m,dx,dy,a,wins):x,y,w,h=a[m];g=wins[m][0];b,c=Kit.place(g,x+dx,y+dy,w,h);aR(g);a[m]=(b,c,w,h)
			def tick(self,g):
				if self.moving is None and not self.pending and self.linger<=0 and not SNAP.drag:
					for k in list(self.gid):
						if k not in cA and not gR(k):self.detach(k)
					return
				self.pending=False
				if self.linger>0:self.linger-=1
				c=g()
				for k in list(self.gid):
					if k not in c and k not in cA:self.detach(k)
				a={s:(int(n.GetX()),int(n.GetY()),int(n.GetWidth())or q[0],int(n.GetHeight())or q[1])for s,(n,q)in c.items()if z(n)};d=gH();e=HOST.layout_arranging();b=[t for t,v in a.items()if t in self.pos and(v[0],v[1])!=self.pos[t]and t not in d]
				if b:
					k=self.moving if self.moving in b else None
					if k is None:
						for m in b:
							if c[m][0]in SNAP.drag:k=m;break
					if k is None:k=b[0]
					h=a[k][0]-self.pos[k][0];i=a[k][1]-self.pos[k][1];f=self.dims.get(k,a[k][2:])!=a[k][2:]
					if f:b=[]
					elif k in self.gid and bu():
						self.detach(k)
						if not self.alt_used:self.alt_used=True;aX("window unanchored.",l)
					j=self.host_follows(c[k][0])if b and not e else()
					for m in(self.members(k)if b and not e else[]):
						if m!=k and m not in b and m in a and m not in d and c[m][0]not in j:self.shift(m,h,i,a,c)
					if not f:self.moving=k;self.still=0
				elif self.moving is not None:
					if not SNAP.drag:self.still+=1
					if self.still>=f6:
						k,self.moving=self.moving,None
						if k in a and k not in d and not e:self.snap(k,a,c,d)
						self.linger=f7
				self.pos={w:x[:2]for w,x in a.items()};self.dims={y:G[2:]for y,G in a.items()}
			def snap(self,k,h,wins,held):
				a,b,i,j=h[k];l=set(self.members(k))
				if any(t in held for t in l):return
				e=None
				for o,(c,d,m,n)in h.items():
					if o in l or o in held:continue
					p=[]
					if b<d+n and d<b+j:p+=[(abs(a-(c+m)),c+m-a,0),(abs(a+i-c),c-i-a,0)]
					if a<c+m and c<a+i:p+=[(abs(b-(d+n)),0,d+n-b),(abs(b+j-d),0,d-j-b)]
					for q,f,g in p:
						if q<=SNAP_DIST and(e is None or q<e[0]):
							if f and abs(b-d)<=SNAP_DIST:g=d-b
							if g and abs(a-c)<=SNAP_DIST:f=c-a
							e=(q,f,g,o)
				if e is None:return
				s,f,g,o=e
				for r in l:
					if r in h:self.shift(r,f,g,h,wins)
				self.join(k,o)
		a6=Anchors()
		def gR(k):return k.startswith("pop:")and int(k[4:])in a8
		import threading;dB=threading.Lock();cn=[0];cV=[None];cW=[False];bP={};bQ=[None];dC=[0.];co=[0];b0=[0.]
		def eI(fn):t=threading.Thread(target=fn);t.daemon=True;t.start()
		def eJ():
			a=bv if os.path.exists(bv)else gU()or ei
			if not os.path.exists(a):return None,[]
			with dB:
				with open(a,"r")as f:b=f.readlines()
				if a==bv:bQ[0]=dD()
			return a,b
		def gS():
			try:a,b=eJ()
			except Exception as c:aX("couldn't read the save file (%s); saving is off this session."%c,f);return
			eK(a,b)
		def bo():
			if aZ["windows"]is not None and not aM.get("shutting"):bX[0]=True
			else:cY(background=True)
		def eK(path,lines):
			if path is None:cW[0]=True;return
			c=None;l=[]
			try:
				for o in lines:
					try:
						a=o.strip()
						if not a or a.startswith("#"):continue
						if a.startswith("[")and a.endswith("]"):c=a[1:-1].strip().lower();continue
						if c=="foes":aY[a2(a)]=a
						elif c=="ignore":bs[a.lower()]=a
						elif c=="players":be[a.lower()]=a;cq[0]+=1
						elif c=="settings"and "="in a:
							b,h=[r.strip().lower()for r in a.split("=",1)]
							if b in ej:ar[b]=bx(int(h),*ej[b])
							elif b in el:ar[b]=h=="true"
						elif c=="anchors"and "="in a:
							i=[s.strip().lower()for s in a.split("=",1)[1].split(",")];i=[t for t in i if t in cA]
							if len(i)>1:a6.add_group(i)
						elif c=="layout"and "="in a:
							b,h=a.split("=",1);b=b.strip().lower();d=[v.strip()for v in h.split(",")]
							if b in aC and len(d)>=5:
								aC[b]=[int(d[0]),int(d[1]),int(d[2]),int(d[3]),d[4].lower()=="true",len(d)>5 and d[5].lower()=="true",bx(int(d[6]),0,100)if len(d)>6 else ar["opacity"]]
								if b=="combat":aM["combat_loaded"]=True
						elif c=="sightings":
							j=g0(a)
							if j is not None:bl.append(j);dG(j)
						elif c=="links"and "|"in a:e,g=a.split("|",1);l.append((a2(e),a2(g)))
						elif c=="foe_seen"and "|"in a:
							p=a.split("|",5);m=(float(p[0]),int(p[1]),int(p[2]),int(p[3]),{"1":True,"0":False}.get(p[4]));k=a2(p[5]);n=bb.get(k)
							if k and(n is None or n[0]<m[0]):bb[k]=m
					except Exception:continue
				eT();eZ()
				for e,g in l:
					if e!=g and e in aY and g in aY:a1[e]=g
				eW()
				for b in aC:L=aC[b];L[0],L[1]=Kit.adapt(L[0],L[1],L[2],L[3])
				cW[0]=True
			except Exception as q:aX("couldn't read the save file (%s); saving is off this session."%q,f)
			if path==ei:
				for k in("friend","foe","neutral"):aC[k][6]=ar["opacity"]
		def gT():
			if aM["combat_loaded"]:return
			def a(key,default):
				try:return int(API.GetPersistentVar(key,str(default),API.PersistentVar.Char))
				except Exception:return default
			L=aC["combat"];L[0],L[1]=a("CombatBars_X",L[0]),a("CombatBars_Y",L[1]);L[2]=bx(a("CombatBars_W",L[2]),bK,ct);L[6]=bx(a("CombatBars_Opacity",L[6]),0,100);L[4]=a("CombatBars_Locked",0)==1;L[5]=a("CombatBars_Minimized",0)==1;ar["magery"]=a("CombatBars_Magery",0)==1;aM["dirty_save"]=True
		def gU():
			try:d=os.path.dirname(bv)or ".";c=os.path.basename(bv)+".";e=[os.path.join(d,g)for g in os.listdir(d)if g.startswith(c)and g.endswith(".tmp")]
			except Exception:return
			b,a=None,None
			for t in e:
				try:m=os.path.getmtime(t)
				except Exception:continue
				if a is None or m>a:b,a=t,m
			return b
		def gV(text):aU(bv,text,None)
		def dD():return safe(lambda:(os.path.getmtime(bv),os.path.getsize(bv)))
		def gW():
			b=dD();c=time.time()
			if b is None:
				if bQ[0]is None:return True
				if not b0[0]:b0[0]=c
				if c-b0[0]<5.:return False
				bQ[0]=None;b0[0]=0.;return True
			b0[0]=0.
			if b==bQ[0]:return True
			e=Client.on_client_thread()
			if(co[0]and not e)or c<dC[0]:return False
			try:
				with dB:
					with open(bv,"r")as h:i=h.readlines()
			except Exception as j:dC[0]=c+30.;aX("couldn't read the save file to merge it (%s); saving waits."%j,f);return False
			g,d=None,[]
			for k in i:
				a=k.strip()
				if a.startswith("[")and a.endswith("]"):g=a[1:-1].strip().lower()
				elif g=="foes"and a and not a.startswith("#"):d.append(a)
			if e:eL(d,b,0);return True
			l=co[0]=id(d);bY.append(lambda:eL(d,b,l));return False
		def eL(got,c,a):
			if a and a!=co[0]:return
			co[0]=0;d=Kit.merge_text("\n".join(got),dict(bP),a2)[1];b=dict((a2(e),e)for e in d)
			for k in[g for g in aY if g not in b]:del aY[k]
			aY.update(b);bQ[0]=c;aM["foe_ver"]+=1
			if a:bo()
		def cX():
			a,cV[0]=cV[0],None
			if a:aX("couldn't save (%s)."%a,f)
		def eM():
			if not cW[0]or not gW():return
			def c(b):return "true"if b else "false"
			try:
				a=["# UltimaTracker save file - one name per line"]
				for e,g in(("foes",aY),("ignore",bs)):a+=["[%s]"%e]+sorted(g.values(),key=lambda s:s.lower())+[""]
				d=cq[0]
				if cr[0]!=d or cr[1]is None:cr[1]=sorted(be.values(),key=lambda s:s.lower());cr[0]=d
				a+=["[players]"]+cr[1]+[""];a+=["[settings]"]+["%s=%d"%(i,ar[i])for i in ek];a+=["%s=%s"%(n,c(ar[n]))for n in el]+["","[anchors]"];a+=["group=%s"%",".join(q)for q in a6.saved_groups()];a+=["","[layout]"]+["%s=%d,%d,%d,%d,%s,%s,%d"%(t,r[0],r[1],r[2],r[3],c(r[4]),c(r[5]),r[6])for t,r in aC.items()];a+=["","[links]"]+["%s|%s"%(aY[v],aY[w])for v,w in sorted(a1.items())if v in aY and w in aY and "|"not in aY[v]+aY[w]];a+=["","[foe_seen]"]+[g1(m)for m in sorted(aY)if m in bb];a+=["","[sightings]"]+[k[gY]for k in bl];return "\n".join(a)+"\n"
			except Exception as h:aX("couldn't save (%s)."%h,f);return
		def eN(text,seq=None):
			with dB:
				if seq is not None and seq!=cn[0]:return
				try:gV(text);bQ[0]=dD();return True
				except Exception as a:cV[0]=str(a)
		def cY(background=False):
			a=eM()
			if a is None:return
			aM["dirty_save"]=False;a3["dirty"]=False;cn[0]+=1;c=cn[0];d=dict(bP)
			def b():
				if eN(a,c):
					for k,v in d.items():
						if bP.get(k,0)==v:bP.pop(k,None)
			if background:eI(b)
			else:b();cX()
		def gX():
			b={d:CategoryGump(d)for d in bk};a=CombatWindow();aZ.update({"windows":b,"combat":a})
			if ar["combat_shown"]:a.show()
			aZ["panel"]=ControlPanel(b,a);h1(b,a);aM["foe_ver"]+=1;n=len(aY);aX("on, %s."%L(n,"saved foe"),l);bi.update({"last_layout":fB(),"tick":0,"next_scan":0.,"next_combat":0.,"next_glow":0.})
			if Kit.get_var(cy)=="1":bS.show()
		ib=None;aZ={"windows":None,"combat":None,"panel":None};b1,eO,dE,eP,eQ,eR,dF,cZ,b2,gY=range(10);eS={True:"1",False:"0",None:"-"};gZ={"1":True,"0":False}
		def g_(t,serial,noto,facet,x,y,guard,name):return "%d|%d|%s|%d|%d|%d|%s|%s"%(int(t),int(serial),noto,int(facet),int(x),int(y),eS.get(guard,"-"),name)
		def g0(line):
			p=line.split("|",7)
			if len(p)<8 or not p[7]:return
			return[float(p[0]),int(p[1]),p[2]or "unknown",int(p[3]),int(p[4]),int(p[5]),gZ.get(p[6]),p[7],a2(p[7]),line]
		def dG(e):
			k=e[b2];a=bb.get(k)
			if a is not None and a[0]>e[b1]:return False
			bb[k]=(e[b1],e[eP],e[eQ],e[eR],e[dF]);return k in aY
		def g1(k):t,a,x,y,b=bb[k];return "%d|%d|%d|%d|%s|%s"%(int(t),a,x,y,eS.get(b,"-"),aY[k])
		def eT():
			n=len(bl)
			if n>cv+f_:del bl[:n-cv]
			if len(bb)>2*cv:
				a=dict((b,c)for b,c in bb.items()if b in aY);bb.clear();bb.update(a)
				for e in bl:dG(e)
		def g2(t,serial,name,noto,facet,x,y,guard):
			a=g_(t,serial,noto,facet,x,y,guard,name);e=[float(int(t)),serial,noto,facet,x,y,guard,name,a2(name),a];bl.append(e);eT()
			if dG(e):a3["seen_ver"]+=1
			a3["ver"]+=1
			if not a3["dirty"]:a3["dirty"]=True;a3["save_at"]=t+d0
		def eU(noto):return U.get(noto,noto or "unknown")
		def eV(facet,x,y):
			f=f4.get(facet)
			if f is None:f="map %d"%facet if facet>=0 else "?"
			return "%s %d,%d"%(f,x,y)
		def dH(now):a=time.localtime(now);return now-(a.tm_hour*3600+a.tm_min*60+a.tm_sec)
		def dI(t,a):
			try:return time.strftime("%H:%M"if t>=a else "%m/%d %H:%M",time.localtime(t))
			except Exception:return "?"
		def g3(k,now):
			s=bb.get(k)
			if s is None:return "not seen yet"
			t,a,x,y,b=s;return "seen %s, %s%s"%(ap(now-t,Kit.AGO_WORDS),eV(a,x,y)," (guarded)"if b else "")
		def eW():
			for a in list(a1):
				m,n=a1.get(a),0
				while m in a1 and n<10:m,n=a1[m],n+1
				if m is None or m==a or m in a1:a1.pop(a,None)
				else:a1[a]=m
		def eX(main):return sorted(b for b,c in a1.items()if c==main)
		def dJ(k):
			m=a1.get(k)
			if m is not None:return "alt of "+aY.get(m,m)
			a=eX(k)
			if a:return "alts: "+", ".join(aY.get(b,b)for b in a)
			return ""
		def g4(a,b):
			c=a1.get(a,a)
			if b==c or a1.get(b)==c:return "%s and %s are already linked."%(aY.get(a,a),aY.get(b,b))
			d=a1.get(b,b)
			for k in list(a1):
				if a1[k]==d:a1[k]=c
			if d!=c:a1[d]=c
			a1[b]=c;a1.pop(c,None);eW();return "linked %s as an alt of %s."%(aY.get(b,b),aY.get(c,c))
		def eY(k):
			if k in a1:del a1[k];return True
			a=eX(k)
			if not a:return False
			b=a[0];del a1[b]
			for c in a[1:]:a1[c]=b
			return True
		cp={};g5=10.
		def g6(name):
			b=HOST.services.get("social.note")
			if b is None or not name:return ""
			c=time.time();a=cp.get(name)
			if a is not None and 0.<=c-a[0]<g5:return a[1]
			try:n=str(b(name)or "").strip()
			except Exception:return ""
			n=n if len(n)<=d3 else n[:d3-2]+".."
			if len(cp)>500:cp.clear()
			cp[name]=(c,n);return n
		def bI(tip,name,extra=""):
			a=[tip]
			if extra:a.insert(0,extra)
			b=dJ(a2(name))if name else ""
			if b:a.insert(0,b[0].upper()+b[1:])
			n=g6(name)
			if n:a.append("Note: "+n)
			return "\n".join(a)
		def dK(name):aY[a2(name)]=bP[a2(name)]=name;aM["foe_ver"]+=1;bo()
		def g7(key):bP[key]=None;aM["foe_ver"]+=1;bo();return aY.pop(key)
		def g8(serial=None,name=None):
			if name:
				k=a2(str(name))
				if k and k in aY:return True
			if serial is None:return False
			try:s=int(serial)
			except Exception:return False
			k=cg.get(s)
			if k is not None and k in aY:return True
			if not name:
				try:m=API.FindMobile(s);k=a2(str(m.Name or ""))if m is not None else ""
				except Exception:k=""
				return bool(k)and k in aY
			return False
		b3={};c_=set();be={};cq=[0];cr=[None,None];c0=set();dL={};g9=re.compile(r"^\s*\[[^\]]+\]\s*$")
		def eZ(c=None):
			if len(be)<=(dq if c is None else c):return
			b=len(be)-f8;d=[]
			for a,e in list(be.items()):
				if b<=0:break
				if a in bs or a2(e)in aY:d.append(a);continue
				del be[a];b-=1
			for a in d:
				if b<=0:break
				del be[a];b-=1
			cq[0]+=1;b3.clear();aM["dirty_save"]=True
		def b4(cache):
			if len(cache)>dp:cache.clear()
		e_=[0.];br={"learn":None,"attack":None,"killer":None}
		def ha():
			e=time.time()
			if e<e_[0]:return
			e_[0]=e+1.;d=br["learn"]
			if d is None:d=br["learn"]=X()
			for f in d.new():
				b=f.name.strip();a=f.text.strip()
				if not b and ": "in a:b,a=[g.strip()for g in a.split(": ",1)]
				if not b or not a:continue
				c=b.lower()
				if g9.match(a):
					if c not in be:
						if len(be)>=dq:eZ(dq-1)
						be[c]=b;cq[0]+=1;aM["dirty_save"]=True;b3.clear()
				elif a.lower().startswith(c+" the "):b4(c0);c0.add(c)
		b5={};e0=1.;e1=[0.]
		def cs(serial):
			v=b5.get(serial)
			if v is None:
				v=bool(API.IsFriend(serial))
				if len(b5)>500:b5.clear()
				b5[serial]=v
			return v
		def a7(m,a):
			try:return bool(getattr(m,a))
			except Exception:return False
		def hb(mob,serial,name,low):
			if low.startswith(es)or a2(name)in aY or low in be or serial in aM["party"]:return True
			if a7(mob,"IsRunning")or a7(mob,"IsMounted")or a7(mob,"InWarMode"):return True
			return cs(serial)
		def hc(mob,serial,name):
			if serial in c_:return False
			b=name.strip().lower()
			if hb(mob,serial,name,b):b4(c_);c_.add(serial);b3.pop(serial,None);return False
			if b in hS()or b in c0:return True
			c=time.time();a=b3.get(serial)
			if a is not None and(a[0]or c-a[1]<dW):return a[0]
			e=e2(mob);d=bool(aV.search(e.split("\n")[0]+" "+name));b4(b3);b3[serial]=(d,c);return d
		def e2(mob):
			try:return str(mob.NameAndProps(False)or "")
			except Exception:return ""
		def hd(mob,serial,name):
			if serial in c_:return False
			b=name.strip().lower()
			if not b:return False
			a=b in c0
			if not a:
				d=time.time();c=dL.get(serial)
				if c is not None and(c[0]or d-c[1]<dW):a=c[0]
				else:e=e2(mob).split("\n")[0].strip().lower();a=e.startswith(b+" the ");b4(dL);dL[serial]=(a,d)
			if not a:return False
			if b in be or a2(name)in aY or serial in aM["party"]or cs(serial):return False
			return True
		def e3(mob,serial):
			a=a7(mob,"IsDead")
			if not a and not(a7(mob,"IsHuman")or a7(mob,"IsGargoyle")):return
			if a7(mob,"IsRenamable"):return
			b=R(mob)
			if b=="invulnerable":return
			try:c=str(mob.Name or "")
			except Exception:return
			if b=="innocent":
				if hc(mob,serial,c):return
			elif not a and hd(mob,serial,c):return
			return(b,a,c)
		def dM(serial,name,noto,party):
			a=a2(name)
			if a and a in aY:return "foe","L"
			if serial in party:return "friend","P"
			if cs(serial):return "friend","F"
			if noto=="ally":return "friend","G"
			if noto=="murderer":return "foe",""
			if noto=="enemy":return "foe","W"
			return "neutral",""
		def he(mob,party):
			try:
				b=mob.Serial;c=e3(mob,b)
				if c is None:return
				d,e,a=c
				if a and a.lower()in bs:return
				return dM(b,a,d,party)+(d,e)
			except Exception:return
		def dN():return ah(max(ar["range"],dZ))
		def e4(m,a):
			try:return getattr(m,a)or 0
			except Exception:return 0
		def hf(e):return e["name"].lower()
		c1={};dO=[None]
		def hg(serial):
			if dO[0]is None or not HOST.in_hop or HOST.pass_id!=dO[0]:return
			return c1.get(serial)
		def hh():
			k={W:[]for W in bk};c1.clear();dO[0]=HOST.pass_id if HOST.in_hop else None;c=time.time()
			if not 0.<e1[0]-c<=e0:b5.clear();e1[0]=c+e0
			e=Q();bf["me"]=e
			if e is None:return k
			E=ar["range"];F=dN();x=set(API.GetPartyMemberSerials()or[]);aM["party"]=x;ha();G=e.Serial;y,z=int(e.X),int(e.Y);H=(ar["alert_red"]or ar["alert_foes"]or ar["alert_orange"]or ar["alert_gray"]);f=g=h=i=None;I=ar["sightings"];J=aZ["windows"]or{};A={}
			for j in bk:B=J.get(j);A[j]=B is None or not(B.minimized and aC[j][5])
			for m in F:
				try:
					if m is None:continue
					a=m.Serial
					if a==G:continue
					l,n=int(m.X),int(m.Y);o=max(abs(l-y),abs(n-z))
					if o>E:continue
					C=e3(m,a)
					if C is None:continue
					d,r,b=C
					if b and b.lower()in bs:continue
					p,q=dM(a,b,d,x)
					if p!="friend"and b:
						if q=="L":
							s=a2(b)
							if cg.get(a)!=s:b4(cg);cg[a]=s
							if i is None:i=[]
							i.append((s,l,n))
						if I:
							D=bU.get(a)
							if D is None or c-D>di:
								if h is None:h=[]
								h.append((a,b,d,l,n))
							bU[a]=c
						if H and not r and hj(q,d)is not None:
							if f is None:f=set()
							f.add(a)
							if a not in cI:
								if g is None:g=[]
								g.append((a,b,d,q,o,l-y,n-z))
					if A[p]:
						t,u=m.Hits or 0,m.HitsMax or 0;v,w=bool(m.IsPoisoned),bool(m.IsParalyzed)
						if len(c1)<dp:c1[a]=(b,d,p,r,v,w,t,u,o)
					else:t=u=0;v=w=False
					k[p].append({"serial":a,"name":b or "(unknown)","tag":q,"noto":d,"hits":t,"hmax":u,"dist":o,"poisoned":v,"paralyzed":w,"dead":r,"mob":m.raw})
				except Exception:continue
			for j in bk:k[j].sort(key=hf)
			cI.clear()
			if f is not None:cI.update(f)
			try:
				if i:hn(i,c)
				if g:hk(g,c)
				if h:hm(h,c)
			except Exception as K:bW(K)
			return k
		def hj(tag,noto):
			if tag=="L"and ar["alert_foes"]:return "foe"
			if noto=="murderer"and ar["alert_red"]:return "red"
			if noto=="enemy"and ar["alert_orange"]:return "orange"
			if(noto=="gray"or noto=="criminal")and ar["alert_gray"]:return "gray"
			return
		def hk(fresh,now):
			b=ar["alert_minutes"]*60.
			for a,c,d,e,f,g,h in fresh:
				t=cf.get(a)
				if t is not None and now-t<b:continue
				cf[a]=now;ae(d_,hl(c,d,e,f,g,h),level="warn",who=a)
		def hl(name,noto,tag,dist,dx,dy):a=dJ(a2(name))if tag=="L"else "";b="%s (%s)"%(name,a)if a else name;c=eU(noto)+(", on your Foe list"if tag=="L"else "");return "%s: %s, %s"%(b,c,aT(dx,dy,"right here"))
		def e5():return int(API.GetMap())
		def e6():return safe(HOST.guarded)
		def dP(key,serial,again,now=None):return not ag(serial,key,bj,True,again,now=now)
		def hm(a,now):
			b,c=e5(),e6()
			for d,e,f,x,y in a:g2(now,d,e,f,b,x,y,c)
		e7=[-10.,-1,None]
		def hn(here,now):
			b=c=None
			for k,x,y in here:
				d=bb.get(k)
				if b is None:
					a=e7;f=e5()
					if f!=a[1]or not 0.<=now-a[0]<1.:a[0],a[1],a[2]=now,f,e6()
					b,c=a[1],a[2]
				bb[k]=(now,b,x,y,c)
				if d is None or now-d[0]>di:
					a3["seen_ver"]+=1
					if not a3["dirty"]:a3["dirty"]=True;a3["save_at"]=now+d0
		bf={"dead":None,"prune_at":0.,"me":None,"att_at":0.,"died_at":0.}
		def ho(now):
			if now>=bf["prune_at"]:bf["prune_at"]=now+10.;hs(now)
			c=bf["me"];a=a7(c,"IsDead")if c is not None else bf["dead"];b,bf["dead"]=bf["dead"],a
			if ar["killer"]and(now>=bf["att_at"]or(a and b is False)):bf["att_at"]=now+1.;hp(now)
			if b is None or a is None or a==b:return
			if a:hr(now)
			else:b8.end()
		def hp(now):
			f=br["killer"]
			if f is None:br["killer"]=X();return
			g,c=[],set()
			for b in f.new():
				if b.text.startswith(fI)or "is attacking you"not in b.low:continue
				h=fk.search(b.text);a=h.group(1).strip().strip("*").strip()if h is not None else ""
				if a:g.append((b,a));c.add(a.lower())
			i=e8(c)if c else None
			for b,a in g:
				j,k=e9(a,i)
				if k is not False:fa(a,b.at,j)
			for s,e in bp.items():
				m=c4.get(s)
				if m is None:continue
				d=e.get("player")
				if d is None:d=e["player"]=not a7(m,"IsRenamable")and(a7(m,"IsHuman")or a7(m,"IsGargoyle"))
				if d:
					try:a=str(m.Name or "")
					except Exception:a=""
					if a:fa(a,e["last"],s)
		def e8(c):
			a={}
			for m in dN():
				try:
					n=m.Name
					if not n:continue
					b=n.strip().lower()
					if b not in c or b in a:continue
					if a7(m,"IsRenamable"):a[b]=(m.Serial,False)
					else:a[b]=(m.Serial,a7(m,"IsHuman")or a7(m,"IsGargoyle"))
					if len(a)>=len(c):break
				except Exception:continue
			return a
		def e9(name,b=None):
			a=name.lower()
			if b is None:b=e8((a,))
			c=b.get(a)
			if c is not None:return c
			if a.startswith("a ")or a.startswith("an "):return None,False
			return None,None
		def fa(name,t,serial):
			if t<=bf["died_at"]:return False
			if serial is not None and(serial in aM["party"]or cs(serial)):return False
			c=name.lower();a=bc.get(c)
			if a is None:
				if len(bc)>=f3:
					b=None
					for k,v in bc.items():
						if b is None or v[1]<bc[b][1]:b=k
					bc.pop(b,None)
				bc[c]=[name,t,serial];return True
			if t>a[1]:a[1]=t
			if serial is not None:a[2]=serial
			return False
		def hq(a):return-a[1]
		def hr(now):
			bf["died_at"]=now
			if not ar["killer"]:bc.clear();return
			b=now-dj;a=sorted([c for c in bc.values()if c[1]>=b],key=hq);bc.clear()
			if a:b8.open(a[:f2],now,len(a))
		def hs(now):
			a=now-di
			for s in[b for b,c in bU.items()if c<a]:del bU[s]
			if cf:
				a=now-ar["alert_minutes"]*60.
				for s in[d for d,e in cf.items()if e<a]:del cf[s]
			if bc:
				a=now-dj
				for k in[g for g,h in bc.items()if h[1]<a]:del bc[k]
		def fb(serial,name,a=None):
			def b(*e):
				b=time.time();d=bC.get(serial,0);b4(bC);bC[serial]=b
				if bu():bC[serial]=0;b_(serial);return
				if eF():
					bC[serial]=0
					if ag(serial,"ultima.aim",bj):API.Target(serial)
					return
				if a is not None and ez():dR(serial,name,a);bC[serial]=0;return
				c=b-d<=fL
				if c:bC[serial]=0
				API.SetLastTarget(serial=serial)
				if c:
					if dP("ultima.attack",serial,"double-click again to attack"):return
					API.Attack(serial);API.HeadMsg("* attacking *",serial,34)
				else:API.HeadMsg("* last target *",serial,53)
			return b
		def c2(cat,poisoned,dead,paralyzed=False):
			if dead:return dr
			if cat in("friend","combat"):
				if poisoned and paralyzed:return eg
				if paralyzed:return cF
			if poisoned:return cE
			return cc[cat]
		def fc(dead,hits,hmax):return not dead and hmax>0 and hits*100./hmax<=gf
		def fd():a=ea+(gh-ea)*(.5+.5*math.sin(2*math.pi*time.time()/gg));return int(a*eb+.5)/float(eb)
		c3={}
		def dQ(b,low,a=None):
			if b is None:return
			if not low:a=0.
			elif a is None:a=fd()
			k=id(b)
			if c3.get(k)==a:return
			if len(c3)>400:c3.clear()
			c3[k]=a;bE(b,a)
		def fe(dead,hits,hmax,poisoned,paralyzed,dist):
			if dead:return "DEAD  %dy"%dist,0,1
			if hmax>0:a=(" PSN"if poisoned else "")+(" PAR"if paralyzed else "");return "%d%%%s  %dy"%(int(round(100.*hits/hmax)),a,dist),hits,hmax
			return "--  %dy"%dist,0,1
		ht={cc["friend"]:("#3A86BF","#13283A"),cc["neutral"]:("#7E868F","#26292C"),cc["foe"]:("#B23C3C","#3A1616"),cc["combat"]:("#B23C3C","#3A1616"),cE:("#4A9A55","#16301A"),cF:("#5A7FCC","#1A2640"),eg:("#2E9A90","#0F302D"),dr:("#4C4C4C","#1C1C1C")};hu=.85;hv=.9;hw=.95;hx=.16;hy=.3
		def ff(color):return ht.get(color,(color,"#202020"))
		class HealthBar(object):
			def __init__(self,parent,x,y,w,h,color,cur=0,mx=1):
				self.fw=None;self.parts=[];self.color=color;c,d=ff(color);a=1 if h>=5 and w>=8 else 0;self.ix,self.iy=x+a,y+a;self.iw,self.ih=max(1,w-2*a),max(1,h-2*a)
				if a:self._add(parent,hu,"#000000",x,y,w,h)
				self.track=self._add(parent,hv,d,self.ix,self.iy,self.iw,self.ih);self.fill=self._add(parent,hw,c,self.ix,self.iy,0,self.ih);self.sheen=self.shade=None
				if self.ih>=6:self.sheen=self._add(parent,hx,"#FFFFFF",self.ix,self.iy,0,max(1,self.ih*2//5));b=max(1,self.ih//5);self.shade=self._add(parent,hy,"#000000",self.ix,self.iy+self.ih-b,0,b)
				self.SetProgress(cur,mx)
			def _add(self,parent,alpha,color,x,y,w,h):b=bM(alpha,color);b.SetRect(x,y,w,h);parent.Add(b);self.parts.append(b);return b
			def SetProgress(self,cur,mx):
				a=int(round(self.iw*bx(float(cur)/mx,0.,1.)))if mx>0 else 0
				if a==self.fw:return
				self.fw=a
				for b in(self.fill,self.sheen,self.shade):
					if b is not None:b.SetWidth(a)
			def set_color(self,color):
				if color==self.color:return
				a,b=ff(color)
				for c,d in((self.fill,a),(self.track,b)):r,g,e=gF(d);c.SetBaseColor(r,g,e,255)
				self.color=color
			def set_visible(self,on):
				for c in self.parts:B(c,"IsVisible",on)
			def Dispose(self):
				for c in self.parts:bt(c)
				self.parts=[]
		class PopBar(object):
			def __init__(self,serial,name,x,y):self.serial,self.name,self.x,self.y=serial,name,x,y;self.gump=None;self.locked=self.minimized=self.opacity_open=False;self.opacity,self.name_color=ar["opacity"],cC;self.create()
			def create(self):
				s=ar["scale"]/100.;w=sc(fN);self.row_h=max(10,sc(16));self.pad=max(2,sc(5));h=2*a0+eB(s)
				if self.opacity_open:h+=eC(s)
				if not self.minimized:h+=self.row_h+2*self.pad
				self.size=(w,h);self.x,self.y=aq(self.x,self.y,w,h);g=API.Gumps.CreateModernGump(self.x,self.y,w,h,False,w,h);self.gump=g;g.SetAlpha(0.);self.chrome=Chrome(g);self.bar=self.info=self.hit=self.glow=None;self.low,self.spell_ctrls,self.bar_key,self.last=False,[],None,None;self.layout_chrome();G.AddGump(g);at(g,self.moved);a6.placed(self.anchor_key);B(g,"CanMove",not self.locked)
			@property
			def anchor_key(self):return "pop:%d"%self.serial
			def moved(self):a6.pending=True
			def layout_chrome(self):
				w,h=self.size;a,b=self.minimized,self.opacity_open;c=[("lock",self.locked,self.toggle_lock,"Unlock (move and resize again)"if self.locked else "Lock in place (no moving or resizing)"),("min",a,self.toggle_minimize,"Restore"if a else an)]
				if not a:c.append(("opacity",b,self.toggle_opacity,"Hide the opacity slider"if b else "Show the opacity slider (frame and bars stay solid)"))
				c.append(("close",False,self.close,"Close this bar"));self.chrome.layout(w,h,ar["scale"]/100.,self.opacity,self.name,self.name_color,c,b and not a,self.toggle_minimize,lambda:b_(self.serial),self.anchor_key)
			def destroy(self):g,self.gump=self.gump,None;D(g)
			def close(self,*a):a8.pop(self.serial,None);self.destroy()
			def snapshot(self):
				if z(self.gump):self.x,self.y=self.gump.GetX(),self.gump.GetY()
			def rebuild(self):self.snapshot();self.destroy();self.create()
			def set_locked(self,locked):
				self.locked=locked
				if self.gump is not None:B(self.gump,"CanMove",not locked);self.layout_chrome()
			def toggle_lock(self,*a):self.set_locked(not self.locked)
			def toggle_minimize(self,*a):self.minimized=not self.minimized;self.opacity_open=False;self.rebuild()
			def toggle_opacity(self,*a):self.opacity_open=not self.opacity_open;self.rebuild()
			def apply_opacity(self,v):
				self.opacity=v
				if self.gump is not None:self.chrome.set_opacity(v)
			def update(self):
				if not z(self.gump):a8.pop(self.serial,None);return
				try:
					v=self.chrome.poll()
					if v is not None:self.opacity=v
					self._refresh()
				except Exception as a:aX("closed the health bar for %s (%s)."%(self.name,a),f);self.close()
			def _draw_row(self,key):
				f,h,c=key
				if self.bar is not None:self.bar.Dispose()
				for g in[self.info,self.hit,self.glow]+self.spell_ctrls:bt(g)
				self.spell_ctrls=[];w=self.size[0];s=ar["scale"]/100.;y=self.chrome.content_top+self.pad;a=w-2*a0-2*self.pad;x=a0+self.pad
				if c and cS():d=self.row_h;a-=cS()*(d+2);eA(self.gump,x+a+2,y,d,self.row_h,self.serial,self.name,self.spell_ctrls)
				self.glow=None
				if c:b=max(2,self.pad-1);self.glow=bM(0.,d9);self.glow.SetRect(x-b,y-b,a+2*b,self.row_h+2*b);self.gump.Add(self.glow)
				self.bar=HealthBar(self.gump,x,y,a,self.row_h,f);e=max(8,int(round(12*cJ(s))));self.info=ci("",e,"#FFFFFF",aligned="right",maxWidth=a-6,applyStroke=True);self.info.SetPos(x+3,bZ(y,self.row_h,e));self.gump.Add(self.info);self.hit=bz(x,y,a,self.row_h,fb(self.serial,self.name),bI(dS,self.name));self.gump.Add(self.hit);self.bar_key=key;self.last=None
			def pulse(self,a=None):
				if self.gump is not None and not self.minimized:dQ(self.glow,self.low,a)
			def _refresh(self):
				e=Q();d=hg(self.serial)if e is not None else None
				if d is not None and d[0]:a=True
				else:d=None;a=aA(self.serial)
				if a is None or e is None:b,f,g,c,h=("out of range",0,1,(dr,False,False),"#888888");self.low=False
				else:
					if d is not None:k,l,i,j,m,n,o,p,q=d
					else:
						try:k=a.Name or self.name
						except Exception:k=self.name
						l=R(a);i,s=dM(self.serial,k,l,aM["party"]);j,m=a7(a,"IsDead"),a7(a,"IsPoisoned");n,o,p=a7(a,"IsParalyzed"),e4(a,"Hits"),e4(a,"HitsMax")
						try:q=max(abs(int(a.X)-int(e.X)),abs(int(a.Y)-int(e.Y)))
						except Exception:q=0
					c=(c2(i,m,j,n),(ar["magery"],ar["healing"]),i=="friend");self.low=i=="friend"and fc(j,o,p);h=cG.get(l,"#DDDDDD");b,f,g=fe(j,o,p,m,n,q)
				if Follow.serial==self.serial:b="FOL "+b
				self.name_color=h
				if self.minimized:self.chrome.set_title("%s  %s"%(self.name,b.split("  ")[0]),h);return
				self.chrome.set_title(self.name,h)
				if c!=self.bar_key:
					r=self.bar_key
					if r is not None and r[1:]==c[1:]and self.bar is not None:self.bar.set_color(c[0]);self.bar_key=c
					else:self._draw_row(c)
				if self.last!=(b,f,g):self.last=(b,f,g);bA(self.info,b);self.bar.SetProgress(float(f),float(g))
		def hz(serial,name):
			def a(*b):
				if not name or name=="(unknown)":aX("no name yet; try again in a moment.",f);return
				bs[name.lower()]=name;bo();a=a8.get(serial)
				if a is not None:a.close()
				aX("%s marked as an NPC and hidden; Unignore the name to undo."%name,l)
			return ck(serial,a)
		def hA(serial,name,a):return ck(serial,lambda:dR(serial,name,a))
		def hB(serial,name,a):HOST.enable("unitframes");bY.append(lambda:dR(serial,name,a,False))
		def dR(serial,name,a,d=True):
			b=HOST.services.get("unitframes.add")
			if b is None and d and "unitframes"in HOST.by_key:cj.append(lambda:hB(serial,name,a));return
			if b is not None:b(serial);aX("%s gets a frame in Character HUD > Frames."%name,l);return
			c=a8.get(serial)
			if c is not None and z(c.gump):aX("a health bar for %s is already open."%name,f);return
			e=safe(lambda:a.gump.GetX(),300);g=safe(lambda:a.gump.GetY(),300);x=e+a.size[0]+6;y=g+len(a8)*(sc(52)+4);h=a8[serial]=PopBar(serial,name,x,y);h.update();aX("popped out a health bar for %s."%name,l)
		dS=("Click: target; double-click: attack (blue or green in guards: twice). Alt+click: auto-follow (again to stop)");hC="Click: put the name in the box. Alt+click: auto-follow (again to stop)";fg=("Click: show only this player (again for everyone). Alt+click: auto-follow (again to stop)")
		class PoolRow(object):
			glow=None;e=None;prev=None
			def parts(self):return self.ctrls
			def set_shown(self,on):
				for c in self.parts():B(c,"IsVisible",on)
				self.bar.set_visible(on);self.shown=on
			def hide(self):
				if self.serial is not None:self.prev=(self.serial,self.name,time.time())
				self.serial,self.name=None,"";self.low=False;self.last=None
				if self.glow is not None:dQ(self.glow,False)
				self.set_shown(False)
		class TrackerRow(PoolRow):
			def __init__(self,view,i,geo,e):
				self.win=view;self.serial,self.name=e["serial"],e["name"];self.y=y=i*geo["row_h"];self.shown,self.low,self.ctrls=True,False,[];self.last=self.raw=self.name_raw=None;a,b=view.sa,geo["rw"];c=API.Gumps.CreateGumpColorBox(.35,"#000000");c.SetRect(0,y,b,geo["row_h"]-2);et(c,RowClick(self,lambda s,n:fb(s,n,view)));F(c,bI(dS,self.name));self.bg=c;self.glow=None
				if view.cat=="friend":self.glow=bM(0.,d9);self.glow.SetRect(0,y,b,geo["row_h"]-2)
				h,j=fh(e,geo);self.name_lbl=bn(h,geo["name_fs"],j);bd(self.name_lbl,4,y+geo["name_dy"]);self.name_key=(h,j);d,f=geo["pbw"],geo["nbw"];self.info=bn("",geo["info_fs"],"#DDDDDD",aligned="right",maxWidth=b-16-d-f);bd(self.info,4,y+geo["info_dy"])
				for g in(c,self.glow,self.name_lbl,self.info):
					if g is not None:a.Add(g);self.ctrls.append(g)
				bN(a,b-8-d-f,y+geo["npc_dy"],f,f,"N",RowClick(self,hz),"Mark as an NPC and hide (Unignore the name to undo). "+bF,font=geo["npc_fs"],store=self.ctrls);bN(a,b-4-d,y+geo["pop_dy"],d,geo["pop_h"],">",RowClick(self,lambda s,n:hA(s,n,view)),"Pop out a health bar (or Shift+click the row). "+bF,font=geo["pop_fs"],store=self.ctrls);self.tips=[]
				if geo["fbtn"]:self.tips=eA(a,4+geo["bar_w"]+2,y+geo["fbtn_dy"],geo["sb"],geo["sb"],self.serial,self.name,store=self.ctrls,row=self)
				self.bar=HealthBar(a,4,y+geo["bar_dy"],geo["bar_w"],geo["bar_h"],fi(view.cat,e))
			def assign(self,e,geo):
				b,a=e["serial"],e["name"]
				if b!=self.serial or a!=self.name:
					if b!=self.serial:self.prev=(self.serial,self.name,time.time())
					self.serial,self.name=b,a;self.last=None
					for g,h in self.tips:F(g,h%a)
					F(self.bg,bI(dS,a))
				if not self.shown:self.set_shown(True)
				c=(e["name"],e["tag"],e["noto"],geo["name_px"],geo["name_fs"])
				if c!=self.name_raw:
					d,f=fh(e,geo)
					if(d,f)!=self.name_key:self.set_name(d,f,geo)
					self.name_raw=c
				self.bar.set_color(fi(self.win.cat,e))
			def set_name(self,text,color,geo):
				a=self.name_lbl
				if color==self.name_key[1]or ey(a,color):bA(a,text)
				else:b=self.ctrls.index(a);bt(a);a=bn(text,geo["name_fs"],color);bd(a,4,self.y+geo["name_dy"]);self.win.sa.Add(a);self.ctrls[b]=a;self.name_lbl=a
				self.name_key=(text,color)
			def values(self,e):
				self.e=e;d=Follow.serial==e["serial"];f=(e["dead"],e["hits"],e["hmax"],e["poisoned"],e["paralyzed"],e["dist"],d)
				if self.last is not None and f==self.raw:return
				self.raw=f;a,b,c=fe(e["dead"],e["hits"],e["hmax"],e["poisoned"],e["paralyzed"],e["dist"])
				if d:a="FOL "+a
				self.low=fc(e["dead"],e["hits"],e["hmax"])
				if self.last!=(a,b,c):self.last=(a,b,c);bA(self.info,a);self.bar.SetProgress(float(b),float(c))
			def forget(self):
				for c in self.ctrls:bm.pop(id(c),None)
				self.ctrls=[];self.serial=None
		def fh(e,geo):
			a=cR(e["name"],geo["name_px"],geo["name_fs"])
			if e["tag"]:a+="  ["+e["tag"]+"]"
			return a,cG.get(e["noto"],"#DDDDDD")
		def fi(cat,e):return c2(cat,e["poisoned"],e["dead"],e["paralyzed"])
		class PoolWin(object):
			def show_empty(self,on):
				if on and self.empty is None:self.empty=self.make_empty();self.empty_shown=True
				elif self.empty is not None and on!=self.empty_shown:
					for a in self.empty:B(a,"IsVisible",on)
					self.empty_shown=on
			def fill(self,data):
				a,b,n=self.rows,self.geo,len(data)
				for i,e in enumerate(data):
					if i<len(a):a[i].assign(e,b)
					else:a.append(self.Row(self,i,b,e))
				for r in a[n:]:
					if r.shown:r.hide()
				self.show_empty(n==0)
				for r,e in zip(a,data):r.values(e)
			def destroy(self):g,self.gump=self.gump,None;D(g)
			def moved(self):a6.pending=True;self.snapshot();bo()
			@property
			def dock_key(self):return "ultima."+self.cat
			def user_minimize(self,*a):M(self.dock_key);self.toggle_minimize()
			def apply_opacity(self,v):
				aC[self.cat][6]=v
				if z(self.gump)and self.chrome is not None:self.chrome.set_opacity(v)
		class CategoryGump(PoolWin):
			Row=TrackerRow
			def __init__(self,cat):self.cat,self.rows=cat,[];self.gump=self.chrome=self.sa=self.made_min=None;self.locked=self.minimized=self.docked=False;self.create()
			def create(self):
				x,y,w,h,i,e,k=aC[self.cat];self.minimized=e;b,c=sc(db),sc(dc);a=a_["size"].get(self.cat);j=C(self.dock_key)
				if a is not None:
					b=min(b,a[0]);c=min(c,a[1]);w=a[0]
					if not e:h=a[1]
				w=max(w,b)
				if e:d=en;f,g=d,False
				else:d=max(h,c);f,g=c,a is None
				self.made_min=(b,c);self.resized_flag=self.user_resize_pending=False;self.sync_target,self.user_resize_ticks=None,0
				if not j:x,y=aq(x,y,w,d);aC[self.cat][0],aC[self.cat][1]=x,y
				self.gump=API.Gumps.CreateModernGump(x,y,w,d,g,b,f,self._on_resized);self.gump.SetAlpha(0.);self.chrome=Chrome(self.gump,kit=True,key=self.dock_key);self._forget_body();self.size=(w,d);self.count_n=0;self.locked=i;self.layout_chrome();G.AddGump(self.gump);at(self.gump,self.moved);a6.placed(self.cat);self._apply_lock()
				if self.docked and e:B(self.gump,"IsVisible",False)
			def layout_fit(self,w,h,mode):
				a=self.cat
				if w is None or h is None:
					if a in a_["size"]:a_["size"][a]=None
					a_["force"].discard(a)
				else:
					a_["size"][a]=(int(w),int(h))
					if mode=="again":a_["force"].add(a)
				a_["req"]=True
			def _forget_body(self):
				for r in self.rows:r.forget()
				self.rows=[];self.sa=self.empty=self.geo=self.body_key=None
			def layout_chrome(self):w,h=self.size;c=self.cat;self.chrome.layout_kit(w,h,aC[c][6],d7[c],d8[c],self.minimized,self.user_minimize,lambda*a:ce.append(self.dock_key));self.chrome.set_status(str(max(0,self.count_n)))
			def zone_chrome(self):
				if z(self.gump)and self.chrome is not None:self.layout_chrome()
			def _on_resized(self,*a):self.resized_flag=True
			def set_count(self,n):
				if n==self.count_n:return
				self.count_n=n;self.chrome.set_status(str(max(0,n)))
			def _apply_lock(self):
				a=self.locked;b=a_["size"].get(self.cat)is not None;c=C(self.dock_key)
				if not c:B(self.gump,"CanMove",not a)
				self.gump.SetResizable(not a and not self.minimized and not b);aC[self.cat][4]=a;aM["dirty_save"]=True
			def set_locked(self,locked):self.locked=locked;self._apply_lock()
			def toggle_minimize(self,*a):
				self.snapshot();aC[self.cat][5]=not self.minimized
				if not aC[self.cat][5]:self.docked=False
				self.destroy();self.create();aM["dirty_save"]=True
			def geometry(self):
				w,h=self.size;a=p+4;c=max(40,w-2*a);b=max(60,c-dX);e=cK(13);g={"sa":(a,self.chrome.content_top+sc(4),c,max(20,h-self.chrome.content_top-sc(4)-a)),"rw":b,"row_h":sc(fM),"name_fs":e,"info_fs":cK(12),"name_px":max(30,int(b/1.2)),"name_dy":sc(1),"info_dy":sc(2),"pbw":sc(fO),"nbw":sc(fP),"npc_dy":sc(3),"npc_fs":cK(10),"pop_dy":sc(1),"pop_h":sc(16),"pop_fs":cK(12),"fbtn":self.cat=="friend"and cS()>0,"sb":sc(13),"fbtn_dy":sc(16)};d=b-8
				if g["fbtn"]:d-=cS()*(g["sb"]+2)
				g["bar_w"],g["bar_dy"],g["bar_h"]=d,sc(18),max(3,sc(10));return g
			def build_body(self):D(self.sa);self._forget_body();self.geo=a=self.geometry();x,y,w,h=a["sa"];self.sa=API.Gumps.CreateGumpScrollArea(x,y,w,h);self.gump.Add(self.sa)
			def make_empty(self):a=eo("No players in range.",self.geo["rw"]-8);return ep(self.sa,a,4,4)
			def update(self,entries):
				if not z(self.gump):self.create()
				if not self.minimized:
					w,h=int(self.gump.GetWidth()),int(self.gump.GetHeight())
					if(w<=0 or h<=0)and self.size:w,h=self.size
					if(w,h)!=self.size or self.resized_flag:
						self.resized_flag=False;self.size=(w,h);a6.placed(self.cat,self.gump.GetX(),self.gump.GetY(),w,h);self.layout_chrome();self.body_key=None
						if self.sync_target==(w,h)or a_["size"].get(self.cat)is not None:self.sync_target=None
						else:self.user_resize_pending=True;self.user_resize_ticks=0
					elif self.user_resize_pending:self.user_resize_ticks+=1
					a=a_["size"].get(self.cat)
					if a is not None and(w,h)!=a:a_["req"]=True
				self.set_count(len(entries))
				if self.minimized:return
				b=(self.size,self.chrome.content_top,ar["scale"],ar["magery"],ar["healing"])
				if b!=self.body_key:self.build_body();self.body_key=b
				self.fill(entries)
			def pulse(self,a=None):
				if self.cat!="friend"or self.minimized:return
				for b in self.rows:
					if b.shown:dQ(b.glow,b.low,a)
			def resize_to(self,w,h):
				if not self.minimized:
					if self.size==(w,h):return
					self.sync_target=(w,h);self.gump.SetWidth(w);self.gump.SetHeight(h)
					if(self.gump.GetWidth(),self.gump.GetHeight())==(w,h):return
				self.snapshot();aC[self.cat][2],aC[self.cat][3]=w,h;self.destroy();self.create()
			def snapshot(self):
				if not z(self.gump):return
				L=aC[self.cat];L[0],L[1],L[2]=self.gump.GetX(),self.gump.GetY(),self.size[0]
				if not self.minimized:L[3]=self.size[1]
		def dT(windows):
			for w in windows.values():w.destroy()
			for w in windows.values():w.create()
			for p in list(a8.values()):p.rebuild()
		def hD():
			if aZ["windows"]is not None:
				for w in aZ["windows"].values():w.snapshot()
				dT(aZ["windows"])
			if aZ["combat"]is not None:aZ["combat"].relayout=True
		def fj(windows,source):
			if source.minimized:w,h=aC[source.cat][2],aC[source.cat][3]
			else:w,h=source.size
			for t in windows.values():
				if t is source or t.locked or a_["size"].get(t.cat)is not None:continue
				t.resize_to(w,h)
			aM["dirty_save"]=True
		def hE(windows):
			for w in windows.values():
				if not ar["sync"]:w.user_resize_pending=False
				elif w.user_resize_pending and w.user_resize_ticks>=2:
					if cP():return
					w.user_resize_pending=False;fj(windows,w);return
		def hF(a,windows):
			b=ar["scale"]
			if a==b:return
			c=float(a)/b
			for w in windows.values():w.snapshot();L=aC[w.cat];L[2]=max(sc(db,a),int(round(L[2]*c)));L[3]=max(sc(dc,a),int(round(L[3]*c)))
			ar["scale"]=a;dT(windows);aM["dirty_save"]=True
		def hG(windows):
			if not a_["req"]:return
			a_["req"]=False;e=cP()
			for a,i in list(a_["size"].items()):
				b=windows.get(a)
				if b is None or b.gump is None:continue
				if i is None:
					if e:a_["req"]=True;continue
					a_["size"].pop(a,None);c=a_["own_size"].pop(a,None)
					if b.made_min is not None and b.made_min!=(sc(db),sc(dc)):
						b.snapshot()
						if c is not None:aC[a][2],aC[a][3]=c
						b.destroy();b.create()
					elif c is not None and c!=(aC[a][2],aC[a][3]):b.resize_to(c[0],c[1])
					a_["made"].pop(a,None)
					if b.gump is not None:b._apply_lock()
					continue
				if a not in a_["own_size"]:a_["own_size"][a]=(aC[a][2],aC[a][3])
				w,h=i;j=a in a_["force"]
				if b.minimized:
					if aC[a][2]!=w or(b.size and b.size[0]!=w):
						if e:a_["req"]=True;continue
						b.resize_to(w,aC[a][3])
					a_["force"].discard(a);continue
				d=(int(b.gump.GetWidth()),int(b.gump.GetHeight()))
				if d[0]<=0 or d[1]<=0:a_["force"].discard(a);continue
				f=a_["made"].get(a);g=f[1]if f is not None and f[0]==(w,h)else 0
				if d==(w,h)and b.size==(w,h):g=0;a_["made"].pop(a,None)
				if(j or b.size!=(w,h)or d!=(w,h)or b.made_min[0]>w or b.made_min[1]>h)and(j or g<gA):
					if e:a_["req"]=True;continue
					a_["force"].discard(a);a_["made"][a]=((w,h),g+1);b.snapshot();aC[a][2],aC[a][3]=w,h;b.destroy();b.create()
				else:a_["force"].discard(a)
		fk=Journal.ATTACK_RE;fl=[int(ih)for ih in fY];bp={};fm=[0];b6=[];c4={};bR=[];bg={"serial":None,"until":0.,"harmful":True,"stale":False}
		def fo(m):
			try:return m is not None and not m.IsDead
			except Exception:return False
		def dU(m):
			try:return int(m.Distance)
			except Exception:return 0
		def dV(m,attacked_me=False):
			if a7(m,"IsRenamable"):return False
			a=R(m);return a not in fW and(attacked_me or a not in fX)
		def b7(serial,t=None):
			e=bp.get(serial)
			if not e:
				a=Q()
				if a is None or serial==a.Serial:return
			if serial in aM["party"]or cs(serial):return
			t=t or time.time()
			if e:e["last"]=t
			elif len(bp)<fU:fm[0]+=1;bp[serial]={"last":t,"hits":None,"order":fm[0]}
		hH=5.
		def hI():
			d=br["attack"]
			if d is None:br["attack"]=X();return
			g,b=time.time()-hH,set()
			for c in d.new():
				if c.at>=g and "is attacking you"in c.low:
					m=fk.search(c.text)
					if m:b.add(m.group(1).strip().lower())
			if not b:return
			e={}
			for m in dN():
				try:
					n=m.Name
					if n:
						f=n.strip().lower()
						if f in b and dV(m,attacked_me=True):e.setdefault(f,[]).append(m)
				except Exception:pass
			for a in e.values():
				if len(a)==1:b7(a[0].Serial);continue
				h=[i for i in a if dV(i)or a7(i,"InWarMode")]or[min(a,key=dU)]
				for m in h:b7(m.Serial)
		fp=.5;fq={"serial":None,"until":0.}
		def hJ():
			s=API.LastTargetSerial;b=Q()
			if not s or b is None or s==b.Serial or s in bp:return
			if ar["combat_only"]and not b.InWarMode:return
			c=time.time();a=fq
			if a["serial"]==s and 0.<=a["until"]-c<=fp:return
			m=API.FindMobile(s)
			if fo(m)and dU(m)<=df and dV(m):a["serial"]=None;b7(s)
			else:a["serial"],a["until"]=s,c+fp
		def hK():
			a=fV if ar["combat_only"]else df
			for m in ah(a):
				try:
					if int(m.Notoriety)in fl and m.InWarMode and not m.IsDead and not a7(m,"IsRenamable"):b7(m.Serial)
				except Exception:pass
		def fr():
			t=time.time();c4.clear();a=[]
			for s in list(bp.keys()):
				e=bp[s];m=API.FindMobile(s)
				if not fo(m):del bp[s];continue
				d=dU(m)
				if d>dZ:del bp[s];continue
				try:h=m.Hits
				except Exception:del bp[s];continue
				if e["hits"]is not None and h<e["hits"]:e["last"]=t
				e["hits"]=h;n=None
				try:
					if d<=df and m.InWarMode:
						n=m.Notoriety
						if int(n)in fl:e["last"]=t
				except Exception:pass
				if t-e["last"]>fT:del bp[s];continue
				c4[s]=m
				try:b,c=m.Name or "???",m.HitsMax;f,g=bool(m.IsPoisoned),bool(m.IsParalyzed);a.append((e["order"],s,b,R(m)if n is None else Kit.noto_of(n),h,c,f,g))
				except Exception:continue
			a.sort();return[i[1:]for i in a]
		def hL(serial):
			def a(*a):b6.append((serial,bu(),time.time()))
			return a
		def hM():
			while b6:
				s,b,a=b6.pop(0);m=API.FindMobile(s)
				if not m:continue
				if b:b_(s);continue
				if eF():
					if not ag(s,"ultima.aim",bj,now=a):continue
					API.Target(s)
				else:
					if dP("ultima.attack",s,"click the bar again to attack",a):continue
					API.Attack(s)
				b7(s)
		def hN(spell,serial):
			def a(*a):
				if bu():b6.append((serial,True,time.time()));return
				bR.append((spell,serial,True,time.time()))
			return a
		def fs(serial,spell,a):return ck(serial,lambda:bR.append((a if ez()else spell,serial,False,time.time())))
		def hO():
			if bR:
				c,s,a,d=bR[-1]
				if cU()is not None:
					if time.time()-d>de:del bR[:];aX("target cursor busy; %s not cast."%c,f)
				else:
					del bR[:];m=API.FindMobile(s)
					if m and a and dP("ultima.cast",s,"click the button again to cast",d):m=None
					if m:
						b=bool(API.HasTarget("any"))
						if b and bg["serial"]is not None and not bg["stale"]and API.HasTarget("harmful"if bg["harmful"]else "beneficial"):API.CancelTarget();b=False
						API.CastSpell(c);bg.update(serial=s,harmful=a,stale=b,until=time.time()+de);eE("spell",de)
						if a:b7(s)
			if bg["serial"]is None:bG("spell");return
			if time.time()>bg["until"]:bg["serial"]=None;bG("spell");return
			if bg["stale"]:
				if not API.HasTarget("any"):bg["stale"]=False
				return
			if cU()is not None:return
			if API.HasTarget("harmful"if bg["harmful"]else "beneficial"):
				s=bg["serial"];bg["serial"]=None;bG("spell")
				if API.FindMobile(s):API.Target(s)
				else:API.CancelTarget()
		def ft(serial,hits,a,c,d):
			e="?"if not a or a<=1 else str(int(round(hits*100./a)))+"%";b="FOL "if Follow.serial==serial else ""
			if c:b+="PSN "
			if d:b+="PAR "
			return b+e
		fu="Attack or aim at %s (blue or green in guards: twice). "+bF;hP=(("Poison","P",cE,"Cast Poison on %s. Alt+click: auto-follow (again to stop)"),("Paralyze","Z",cF,"Cast Paralyze on %s. Alt+click: auto-follow (again to stop)"));bJ=p+4
		class CombatSlot(PoolRow):
			def __init__(self,view,i,geo,d):
				self.win=view;g=view.gump;k,a,t,l,f,m,o=d;self.serial,self.name=k,a;self.y=b=geo["y"]+i*(geo["rh"]+cu);self.shown,self.ctrls,self.tips=True,[],[];self.bar=HealthBar(g,bJ,b,geo["bar_w"],geo["rh"],c2("combat",m,False,o),l,f if f else 1);self.name_lbl=self.info=self.name_key=self.info_text=self.name_raw=self.info_raw=None;self._texts(d,geo);c=bz(bJ,b,geo["bar_w"],geo["rh"],RowClick(self,lambda s,n:hL(s)),bI(fu%a,a));g.Add(c);self.ctrls.append(c);self.tips.append((c,fu))
				if ar["magery"]:
					h=bJ+geo["bar_w"]+1
					for p,q,r,j in hP:e=[];bN(g,h,b,geo["spell_w"],geo["rh"],q,RowClick(self,(lambda a:lambda s,n:hN(a,s))(p)),j%a,face=r,color="#FFFFFF",font=max(7.,geo["font"]-1),store=e);self.ctrls.extend(e);self.tips.append((e[-1],j));h+=geo["spell_w"]+1
			def _texts(self,d,geo):
				g=self.win.gump;l,f,h,m,i,n,o=d;a=geo["font"];j=bZ(self.y,geo["rh"],a)
				if self.name_lbl is None:b=cR(f,geo["name_w"],a,True);k=cG.get(h,"#FFFFFF");c=ci(b,a,k,applyStroke=True);c.SetPos(bJ+3,j);g.Add(c);self.name_lbl,self.name_key=c,(b,k);self.name_raw=(f,h,geo["name_w"],a)
				if self.info is None:b=ft(l,m,i if i else 1,n,o);e=ci(b,a,"#FFFFFF",aligned="right",maxWidth=geo["info_w"],applyStroke=True);e.SetPos(bJ+geo["bar_w"]-geo["info_w"]-3,j);g.Add(e);self.info,self.info_text=e,b
			def assign(self,d,geo):
				c,a,e,m,n,i,j=d
				if c!=self.serial or a!=self.name:
					if c!=self.serial:self.prev=(self.serial,self.name,time.time())
					self.serial,self.name=c,a
					for k,(l,f)in enumerate(self.tips):F(l,bI(f%a,a)if k==0 else f%a)
				if not self.shown:self.set_shown(True)
				self.bar.set_color(c2("combat",i,False,j));g=geo["font"];h=(a,e,geo["name_w"],g)
				if self.name_lbl is not None and h!=self.name_raw:
					b=(cR(a,geo["name_w"],g,True),cG.get(e,"#FFFFFF"))
					if b!=self.name_key:
						if b[1]==self.name_key[1]:bA(self.name_lbl,b[0]);self.name_key=b
						else:bt(self.name_lbl);self.name_lbl=None
					self.name_raw=h
				self._texts(d,geo)
			def values(self,d):
				self.e=d;a,j,k,b,f,g,h=d;c=f if f else 1;self.bar.SetProgress(b,c);i=(a,b,c,g,h,Follow.serial==a)
				if i!=self.info_raw:
					self.info_raw=i;e=ft(a,b,c,g,h)
					if e!=self.info_text:self.info_text=e;bA(self.info,e)
			def parts(self):return[self.name_lbl,self.info]+self.ctrls
			def dispose(self):
				for c in self.parts():bt(c)
				self.bar.Dispose()
		class CombatWindow(PoolWin):
			Row=CombatSlot
			def __init__(self):self.gump=self.chrome=self.slot=None;self.relayout=self.zone_redraw=self.docked=False;self.made_min=bK;self.cat="combat";self._forget()
			def layout_fit(self,w,h,mode):
				a=(int(w),int(h))if w and h else None
				if a!=self.slot or mode=="again":self.slot=a;self.relayout=self.zone_redraw=True
			def width(self):return self.slot[0]if self.slot is not None else aC["combat"][2]
			def zone_chrome(self):self.relayout=True
			def _forget(self):self.rows,self.grip,self.empty_lines=[],[],[];self.empty=self.frame_key=self.geo=self.fit_n=None;self.empty_shown=False
			@property
			def minimized(self):return bool(aC["combat"][5])
			def is_open(self):return z(self.gump)
			def show(self):
				if self.is_open():return
				L=aC["combat"];L[2]=bx(L[2],bK,ct);a=C(self.dock_key)
				if not a:L[0],L[1]=aq(L[0],L[1],self.width(),self.height(0))
				self.made_min=min(bK,self.width());g=API.Gumps.CreateModernGump(L[0],L[1],self.width(),self.height(0),True,self.made_min,16,self._on_resized);g.SetAlpha(0.);self.gump=g;self._forget();G.AddGump(g);at(g,self.moved);a6.placed("combat")
				if not a:ar["combat_shown"]=True;aM["dirty_save"]=True
				self.apply_lock();self.draw(fr())
			def hide(self):
				self.snapshot();D(self.gump);self.gump=None;self._drop_notes();ar["combat_shown"]=False;aM["dirty_save"]=True
				if self.docked:self.docked=False;M(self.dock_key)
			def _drop_notes(self):
				for a in self.rows:bm.pop(id(a.name_lbl),None);bm.pop(id(a.info),None)
				self._forget()
			def snapshot(self):
				if self.is_open():L=aC["combat"];L[0],L[1]=self.gump.GetX(),self.gump.GetY()
			def reset(self):
				aC["combat"]=list(dt["combat"])
				if self.is_open():L=aC["combat"];g=self.gump;g.SetPos(L[0],L[1]);aR(g);a6.placed("combat");self.apply_lock();self.relayout=True
				else:self.show()
			def metrics(self):s=bx(self.width(),bK,ct)/float(dY);return s,max(10,int(round(fR*s))),fS*cJ(s)
			def height(self,n):
				if self.slot is not None and not aC["combat"][5]:return self.slot[1]
				b,a,b=self.metrics()
				if aC["combat"][5]:return en
				h=cH+p
				if n<=0 and self.empty_lines:return h+max(a+cu,2+dv*len(self.empty_lines))+dd
				return h+max(n,1)*(a+cu)+dd
			def _empty_text(self,W):
				c=max(20,W-2*bJ-4);a=eo("No one is fighting you.",c)
				if self.slot is not None:
					b=max(1,(self.slot[1]-p-cH-2)//dv)
					if len(a)>b:a=a[:b-1]+[u(" ".join(a[b-1:]),c)]
				return a
			def _on_resized(self,*a):
				if not self.is_open()or self.slot is not None:return
				w=bx(int(self.gump.GetWidth()),bK,ct)
				if w==aC["combat"][2]:return
				aC["combat"][2]=w;self.relayout=True
			def apply_lock(self):
				if not self.is_open():return
				g,a=self.gump,aC["combat"][4];b=C(self.dock_key)
				if not b:B(g,"CanMove",not a)
				g.SetResizable(not a and not b)
			def set_locked(self,locked):
				if aC["combat"][4]!=locked:aC["combat"][4]=locked;self.apply_lock();self.relayout=True;aM["dirty_save"]=True
			def toggle_minimize(self,*a):
				aC["combat"][5]=not aC["combat"][5]
				if not aC["combat"][5]:self.docked=False
				self.relayout=True;aM["dirty_save"]=True
			def status_text(self,data):
				n=len(data)
				if not aC["combat"][5]or n==0:return "%d"%n
				a,c,d=None,0,0
				for j,k,l,h,e,g,i in data:
					c+=g;d+=i
					if e:f=int(round(h*100./e));a=f if a is None else min(a,f)
				b=["%d"%n]
				if a is not None:b.append("low %d%%"%a)
				if c:b.append("PSN %d"%c)
				if d:b.append("PAR %d"%d)
				return "  ".join(b)
			def build_frame(self,data):
				g=self.gump
				if self.chrome is not None and self.chrome.gump is g:self.chrome.dispose()
				for j in self.rows:j.dispose()
				for c in self.grip:bt(c)
				for c in self.empty or():bt(c)
				g.Clear();self._forget();L=aC["combat"];b=L[5];s,e,k=self.metrics();W=self.width();n=len(data)
				if not b:self.empty_lines=self._empty_text(W)
				H=self.height(n);g.SetWidth(W);g.SetHeight(H);self.fit_n=n;a6.sized("combat",W,H);self.chrome=Chrome(g,kit=True,key="ultima.combat");self.chrome.layout_kit(W,H,L[6],"Combat",d8["combat"],b,self.user_minimize,lambda*a:ce.append("ultima.combat"));self.chrome.set_status(self.status_text(data))
				if b:return
				l=W-2*bJ;f=int(round(80*s));h=max(14,e)if ar["magery"]else 0;i=l-(2*(h+1)if ar["magery"]else 0);self.geo={"y":self.chrome.content_top,"rh":e,"font":k,"info_w":f,"spell_w":h,"bar_w":i,"name_w":i-f-6,"W":W}
				if L[4]:return
				m,o=W-p-9,H-p-9
				for q,r in fv:d=bM(1.,ge);d.SetRect(m+q,o+r,2,2);g.Add(d);self.grip.append(d)
			def fit(self,n):
				n=max(n,0)
				if n==self.fit_n:return
				self.fit_n=n;W,H=self.geo["W"],self.height(n);self.gump.SetHeight(H);a6.sized("combat",W,H);self.chrome.frame.layout(W,H);a,b=W-p-9,H-p-9
				for(c,d),e in zip(fv,self.grip):e.SetRect(a+c,b+d,2,2)
			def make_empty(self):return ep(self.gump,self.empty_lines or[""],bJ+4,self.geo["y"]+2)
			def fill(self,data):
				if self.slot is not None:
					a=self.geo;c=self.slot[1]-a["y"]-p-dd;b=max(1,c//max(1,a["rh"]+cu))
					if len(data)>b:data=data[:b]
				self.fit(len(data));PoolWin.fill(self,data)
			def draw(self,data):
				L=aC["combat"];a=(L[2],L[5],L[4],ar["magery"],self.slot)
				if self.zone_redraw and self.frame_key is not None and cP():
					if self.chrome is not None:self.chrome.set_status(self.status_text(data))
					if a==self.frame_key and not L[5]and self.geo is not None:self.fill(data)
					return
				if self.relayout or a!=self.frame_key:self.relayout=self.zone_redraw=False;self.build_frame(data);self.frame_key=a
				elif self.chrome is not None:self.chrome.set_title("Combat");self.chrome.set_status(self.status_text(data))
				if not L[5]:self.fill(data)
			def tick(self):
				g=self.gump
				if g is None:del b6[:];return
				if ch():return
				if not z(g):
					self.gump=None;self._drop_notes()
					if C(self.dock_key):return
					ar["combat_shown"]=False;aM["dirty_save"]=True;aX("combat bars hidden; Show combat in the %s window brings them back."%bj,o);return
				if((self.made_min>self.slot[0])if self.slot is not None else(self.made_min<bK))and not cP():
					self.snapshot();self.gump=None;self._drop_notes();D(g);self.show()
					if self.docked:B(self.gump,"IsVisible",False)
					return
				hM();hI();hJ();hK();self.draw(fr())
		fv=((6,6),(6,3),(3,6),(6,0),(0,6),(3,3))
		class ControlPanel(object):
			BODY_H=420;FOE_ROW_H=32
			def __init__(self,windows,combat):
				self.windows,self.combat=windows,combat;self.g=self.list_sa=self.input=self.lock_all_lbl=self.combat_lbl=self.foe_title=None;self.store,self.x0,self.w=({},{}),0,0;self.foe_ver=self.seen_ver=-1;self.foe_rows,self.seen_at=[],0.;self.list_top=self.list_h=0;self.list_lbls=();a=HOST.hub
				if a is not None:a.add("ultima",bj,{"height":self.height,"build":self.build_section,"closed":self.section_closed})
				else:aX("couldn't show the Foe list panel (no shared window).",f)
			@property
			def gump(self):return self.g if z(self.g)else None
			@property
			def size(self):a=HOST.hub;return(a.W,a.H)if a is not None else(0,0)
			def height(self,w):return self.BODY_H+16
			def build_section(self,g,x,y,w,store):self.g,self.store=g,store;self.x0,self.w=x+8,w-16;self.list_sa,self.foe_ver=None,-1;J(g,x,y,w,self.height(w));self.build_body(y+8);a6.pending=True
			def section_closed(self):self.g=self.list_sa=self.input=None;self.foe_rows=[]
			def _heading(self,text,y):a=bn(text,13,"#FFD966");bd(a,self.x0+2,y);self.g.Add(a);return a
			def _divider(self,y):d=bq(ao,self.w,4);d.SetPos(self.x0,y);self.g.Add(d)
			def build_body(self,b):g,X,W=self.g,self.x0,self.w;c=int(W/3);self._heading("FOES & IGNORE LIST",b);f=bq(Kit.FIELD_TILE,W,24);f.SetPos(X,b+21);g.Add(f);self.input=API.Gumps.CreateGumpTextBox("",W-4,22,False,16);self.input.SetPos(X+2,b+22);self.input.SetPlaceholder("Player name");F(self.input,"Player name for the buttons below");g.Add(self.input);j="Hide combat"if self.combat.is_open()else "Show combat";k=(("Add foe",0,52,self.add_foe,ak,"Put the typed name on your Foe list"),("Remove foe",1,52,self.remove_foe,N,"Take the typed name off your Foe list"),("Target...",2,52,self.target_foe,al,"Target a player to put them on your Foe list"),("Ignore",0,80,self.ignore_name,N,"Hide the typed name from the trackers (an NPC)"),("Unignore",1,80,self.unignore_name,ak,"Show the typed name in the trackers again"),("Lock all",2,80,self.lock_all,al,"Lock or unlock every tracker, the combat bars and pop-outs"),(j,0,144,self.toggle_combat,al,"Show or hide the combat bars"),("Settings",1,144,lambda*a:ai("ultima"),H,aG%bj),("Sightings",2,144,lambda*a:bS.toggle(),H,"Open or close the Sightings window"));d=[self._button(m,X+n*c,b+q,c,r,s,v)for m,n,q,r,s,v in k];self.lock_all_lbl,self.combat_lbl=d[5],d[6];self._divider(b+110);self._heading("WINDOWS",b+120);self._divider(b+176);self.foe_title=self._heading("SAVED FOES (0)",b+186);self.list_top=b+210;e=b+self.BODY_H;h=max(16,ba.get("font_h",0)if cO(11)else 0);self.list_h=e-h-14-self.list_top;i=bn("Alt+click any bar: auto-follow (again to stop).",11,cD);bd(i,X+2,e-h-6);g.Add(i);self.foe_ver=aM["foe_ver"];self.rebuild_foe_list()
			def _button(self,text,x,y,w,fn,art,tip=None):a=S(art[0])[0]or 30;b="ut:"+text.lower().replace(" ","_").rstrip(".");return E(self.g,self.store,b,art,x,y,u(text,max(10,w-a-6)),tip,on_click=a9(fn))
			def _typed(self):return(safe(lambda:self.input.Text,"")or "").strip()
			def _clear_input(self):safe(lambda:self.input.SetText(""))
			def add_foe(self,*a):
				n=self._typed()
				if not n:aX("type a name first.",f);return
				dK(n);self._clear_input();aX("added %s to the Foe list."%n,l)
			def remove_foe(self,*a):
				n=self._typed()
				if n:self._remove(a2(n));self._clear_input()
			def _remove(self,key):
				if key in aY:
					eY(key)
					if bD[0]==key:bD[0]=None
					a=g7(key);aX("removed %s from the Foe list."%a,l)
				else:aX("%s isn't on the Foe list."%key,f)
			def target_foe(self,*a):aX("target a player for your Foe list.",o);HOST.pick_target(10,self._foe_targeted)
			def _foe_targeted(self,serial):
				a=API.FindMobile(serial)if serial else None
				if not a or not a.Name:aX("no player targeted.",f);return
				dK(a.Name);aX("added %s to the Foe list."%a.Name,l)
			def ignore_name(self,*a):
				n=self._typed()
				if n:bs[n.lower()]=n;bo();self._clear_input();aX("ignoring %s from now on."%n,l)
			def unignore_name(self,*a):
				n=self._typed()
				if n and n.lower()in bs:bs.pop(n.lower());bo();self._clear_input();aX("no longer ignoring %s."%n,l)
			def _all_locked(self):
				a=[b.locked for b in self.windows.values()]
				if self.combat.is_open():a.append(aC["combat"][4])
				a.extend(c.locked for c in a8.values());return all(a)
			def lock_all(self,*b):
				a=not self._all_locked()
				for w in self.windows.values():w.set_locked(a)
				self.combat.set_locked(a)
				for p in list(a8.values()):p.set_locked(a)
				self.refresh_labels()
			def toggle_combat(self,*b):
				a=self.combat
				if a.is_open()and C(a.dock_key):return
				(a.hide if a.is_open()else a.show)();self.refresh_labels()
			def refresh_labels(self):
				if self.gump is None or self.lock_all_lbl is None:return
				j(self.lock_all_lbl,"Unlock all"if self._all_locked()else "Lock all");j(self.combat_lbl,"Hide combat"if self.combat.is_open()else "Show combat")
			def reset_defaults(self,*b):
				er()
				for p in a8.values():p.opacity,p.locked=bB,False
				for w in self.windows.values():
					if w.docked:w.docked=False;M(w.dock_key)
				a=self.combat.docked
				if a:self.combat.docked=False;M(self.combat.dock_key)
				dT(self.windows);self.combat.reset()
				if a and self.combat.is_open():B(self.combat.gump,"IsVisible",True)
				if HOST.hub is not None:HOST.hub.refresh()
				eH();bo();aX("settings and windows reset to the defaults.",l)
			def set_all_opacity(self,v):
				ar["opacity"]=v
				for w in self.windows.values():w.apply_opacity(v)
				for a in a8.values():a.apply_opacity(v)
				self.combat.apply_opacity(v);aC["panel"][6]=v;aM["dirty_save"]=True
			def rebuild_foe_list(self):
				if self.gump is None:return
				D(self.list_sa)
				for b in self.list_lbls:bm.pop(id(b),None)
				self.list_lbls=h=[];self.list_sa=API.Gumps.CreateGumpScrollArea(self.x0,self.list_top,self.w,self.list_h);self.g.Add(self.list_sa);self.foe_rows=[];i=sorted(aY.items(),key=lambda a:a[1].lower());bA(self.foe_title,"SAVED FOES (%d)"%len(i))
				if not i:b=bn("No foes yet. Type a name and press Add foe.",12,"#888888");h.append(b);bd(b,2,2);self.list_sa.Add(b);return
				l=time.time();m=self.w-dX;o=set(a1.values());e=self.list_sa
				for p,(c,d)in enumerate(i):
					y=p*self.FOE_ROW_H;b=bn(dw(d,24),13,"#FF9090");h.append(b);bd(b,2,y+2);e.Add(b);f=m-22;bN(e,f,y,18,18,"x",self._foe_btn(c,d,self._remove),"Take %s off your Foe list. %s"%(d,bF));f-=22;j=bD[0]==c;bN(e,f,y,18,18,"L*"if j else "L",self._foe_btn(c,d,self.link_click),("Press L on the other entry (L here again: cancel). "if j else "Link as one person: L here, then L on the other entry. ")+bF,face=cB if j else cb)
					if c in a1 or c in o:f-=22;bN(e,f,y,18,18,"U",self._foe_btn(c,d,self.unlink_click),"Unlink from its group. "+bF)
					e.Add(bz(0,y,max(20,f-6),18,(lambda k,n:(lambda*a:self.foe_name_click(k,n)))(c,d),bI(hC,d)));g=bn(self.foe_info(c,l),11,cD,maxWidth=m-6);h.append(g);bd(g,2,y+17);e.Add(g);self.foe_rows.append((c,g))
				self.seen_ver=a3["seen_ver"];self.seen_at=l+d2
			def _foe_btn(self,k,n,fn):return lambda*a:self.foe_name_click(k,n)if bu()else fn(k)
			@staticmethod
			def foe_info(key,now):a=dJ(key);b=g3(key,now);return a+"; "+b if a else b
			def link_click(self,key):
				if key not in aY:return
				a=bD[0]
				if a is None or a not in aY:bD[0]=key;aX("press L on the entry to link with %s."%aY[key],o)
				elif a==key:bD[0]=None;aX("linking cancelled.",o)
				else:bD[0]=None;aX(g4(a,key),l);bo()
				aM["foe_ver"]+=1
			def unlink_click(self,key):
				if key in aY and eY(key):aX("%s is no longer linked."%aY[key],l);bo();aM["foe_ver"]+=1
			def foe_name_click(self,key,name):
				if bu():
					a,b=None,-1.
					for s,k in cg.items():
						if k==key and API.FindMobile(s)is not None:
							t=bU.get(s,0.)
							if t>b:a,b=s,t
					if a is not None:b_(a)
					else:aX("%s isn't in range."%name,f)
					return
				safe(lambda:self.input.SetText(name))
			def update(self):
				if self.gump is None:return
				if self.foe_ver!=aM["foe_ver"]:self.foe_ver=aM["foe_ver"];self.rebuild_foe_list()
				elif self.foe_rows:
					a=time.time()
					if self.seen_ver!=a3["seen_ver"]or a>=self.seen_at:
						self.seen_ver=a3["seen_ver"];self.seen_at=a+d2
						for b,c in self.foe_rows:bA(c,self.foe_info(b,a))
				self.refresh_labels()
		class SightRow(object):
			__slots__=("serial","name","prev","e","c","nm","here")
			def __init__(self):self.serial,self.name,self.prev,self.e=None,"",None,None;self.c,self.nm,self.here={},"",None
		def hQ(serial,name):return ck(serial,lambda:bS.filter_name(name))
		fw=26+cw*22+6;c5=2*p+30+36+fw+36+3*I;fx=c5-(cw-1)*22
		def fy(obj,w,h,mode):
			a=(int(w),int(h))if(w is not None and h is not None)else None
			if a!=obj.slot or(mode=="again"and a is not None):obj.slot=a;obj.redraw=True
		def fz(obj,a,b):
			z=obj.slot
			if z is None or obj.st["minimized"]or not C(obj.KEY)or z[0]<a or z[1]<b:return
			return z
		class SightingsWindow(object):
			KEY="ultima.sightings";TITLE="Sightings";W=480;MINI_W,MINI_H=300,46;COLS=(8,92,230,278,404)
			def __init__(self):self.st={"minimized":False,"docked":False,"shutting":True};self.win={"g":None};self.slot,self.want,self.n,self.w=None,False,cw,self.W;self.hooks=aL(self.TITLE,f0,self.st,self.win,self.ask_redraw,self.fit);self.hooks.update(show=self.zone_show,min=(self.W,fx));self.flt={"text":"","noto":0,"time":0};self.forget()
			def fit(self,w,h,mode):fy(self,w,h,mode)
			def zone_show(self):self.want=True
			def forget(self):self.c,self.store,self.rows={},({},{}),[];self.page,self.matches,self.counts=0,[],{};self.ver,self.ver_at,self.dirty,self.redraw=None,0.,True,False;self.full_at=self.here_at=self.poll_at=0.
			def is_open(self):return self.win["g"]is not None
			def ask_redraw(self):self.redraw=True
			def toggle(self):
				if not self.is_open():self.show()
				elif self.st["minimized"]or self.st["docked"]:self.bring()
				elif not C(self.KEY):self.close()
			def bring(self):
				if not self.is_open():self.show()
				if self.st["minimized"]or self.st["docked"]:M(self.KEY);self.st["minimized"]=self.st["docked"]=False;aa(cx,False);self.build()
			def show(self):
				if self.is_open():return
				a=C(self.KEY);self.st.update(shutting=False,docked=False,minimized=not a and bool(aN(cx)or HOST.dock_wanted(self.KEY)));self.build();au(cy,"1")
			def save_pos(self):
				if not C(self.KEY):ab(dm,self.win["g"])
			def close(self,stopping=False):
				g=self.win["g"]
				if g is None:return
				self.st["shutting"]=True
				if not stopping:M(self.KEY);au(cy,"0")
				if not C(self.KEY):ab(dm,g);aa(cx,self.st["minimized"])
				self.win["g"]=None;self.forget();D(g)
			def lost(self):self.win["g"]=None;self.st["shutting"]=True;au(cy,"0");self.forget()
			def build(self):
				self.redraw=False;d=self.win["g"];x,y=aO(dm,(320,160),(self.W,c5))
				if z(d):x,y=d.GetX(),d.GetY()
				self.win["g"]=None;self.forget();a,c,q=self.store,self.c,self.rows;M,j=p,I;g=G.CreateGump(True,True);self.n,self.w=cw,self.W
				if self.st["minimized"]:w,h=self.MINI_W,self.MINI_H;c["status"]=aQ(g,a,w,h,self.TITLE,self.KEY,a9(self.toggle_min),close_tip="Close Sightings")
				else:
					m=fz(self,self.W,fx);w,h=m if m else(self.W,c5);k=h-c5+fw;self.n=max(1,(k-32)//22);self.w=w;e=w-2*M;aI(g,w,h);Kit.title_bar(g,a,w,self.TITLE,self.KEY,a9(self.toggle_min),a9(lambda:az(self.KEY,self.TITLE)),a9(lambda:ai("ultima")),close_tip="Close Sightings");b=M+30+j;J(g,M,b,e,36);A(g,"Find:",M+10,b+9);c["find"]=F(Kit.add_textbox(g,self.flt["text"],M+52,b+7,128,numbers=False),"Part of a name: list only that player");c["noto"]=E(g,a,"noto",H,M+196,b+7,dk[self.flt["noto"]][0],"Which players to list (click to cycle)",on_click=a9(lambda:self.cycle("noto",dk)));c["time"]=E(g,a,"time",H,M+326,b+7,dl[self.flt["time"]][0],"How far back to list (click to cycle)",on_click=a9(lambda:self.cycle("time",dl)));f=b+36+j;J(g,M,f,e,k)
					for l,s in zip(self.COLS,("Time","Player","Colour","Where","Count")):A(g,s,M+l,f+6,am)
					for t in range(self.n):
						n=f+26+t*22;r=SightRow()
						for u,l,v in(("t",0,o),("n",1,K),("o",2,K),("p",3,o),("k",4,o)):r.c[u]=A(g,"",M+self.COLS[l],n+2,v)
						r.c["hit"]=Z(g,M+4,n,e-8,22,a9(RowClick(r,hQ)),fg);q.append(r)
					i=f+k+j;J(g,M,i,e,36);E(g,a,"newer",H,M+10,i+7,"Prev","Newer sightings",on_click=a9(self.newer));E(g,a,"older",H,M+120,i+7,"Next","Older sightings",on_click=a9(self.older));c["status"]=A(g,"",M+230,i+10,o)
				aS(g,x,y,w,h,self.KEY,self.st["minimized"]and self.st["docked"],None,self.save_pos,self.win,{"g":g});D(d);self.refresh(time.time(),True)
			def toggle_min(self,*a):Kit.win_action("toggle_min",self.st,self.KEY,self.TITLE,self.build,cx)
			def cycle(self,k,table):
				self.flt[k]=(self.flt[k]+1)%len(table)
				if k in self.c:j(self.c[k],table[self.flt[k]][0])
				self.page,self.dirty=0,True
			def newer(self,*a):
				if self.page>0:self.page-=1;self.dirty=True
			def older(self,*a):
				if(self.page+1)*self.n<len(self.matches):self.page+=1;self.dirty=True
			def filter_name(self,name):
				a=""if self.flt["text"].lower()==name.lower()else name;b=self.c.get("find")
				if b is not None:safe(lambda:b.SetText(a))
				self.flt["text"]=a;self.page,self.dirty=0,True
			def tick(self,now):
				if self.want:
					self.want=False
					if C(self.KEY):
						if not self.is_open():self.show()
						elif self.st["minimized"]or self.st["docked"]:self.st["minimized"]=self.st["docked"]=False;self.build()
				if self.win["g"]is None:return
				if T(self.store,"close"):self.close();return
				if self.redraw:self.build();return
				if now<self.poll_at<=now+ca:return
				self.poll_at=now+ca
				if not z(self.win["g"]):self.lost();return
				if self.st["minimized"]and self.st["docked"]:return
				self.refresh(now)
			def refresh(self,now,force=False):
				c=self.c
				if self.st["minimized"]:
					if force or a3["ver"]!=self.ver or now>=self.full_at:
						self.ver,self.full_at=a3["ver"],now+d1;n=len(bl);a="%s: %d"%(self.TITLE,n)
						if n:e=bl[-1];a+=", last %s %s"%(e[cZ],dI(e[b1],dH(now)))
						else:a="%s: none yet"%self.TITLE
						j(c["status"],u(a,self.MINI_W-90))
					return
				b=c.get("find")
				if b is not None:
					d=str(b.Text or "").strip()
					if d!=self.flt["text"]:self.flt["text"]=d;self.page,self.dirty=0,True
				if force or self.dirty or now>=self.full_at or(a3["ver"]!=self.ver and not 0.<=self.ver_at-now<=1.):self.ver_at=now+1.;self.work_out(now);self.fill(now)
				elif now>=self.here_at:self.mark_here(now)
			def work_out(self,now):
				self.dirty=False;self.ver,self.full_at=a3["ver"],now+d1;a=dl[self.flt["time"]][1];f=None if a is None else(dH(now)if a=="today"else now-a);b=dk[self.flt["noto"]][1];g=a2(self.flt["text"]);c,d=[],{}
				for i in range(len(bl)-1,-1,-1):
					e=bl[i]
					if f is not None and e[b1]<f:break
					if g and g not in e[b2]:continue
					if b is not None and(e[b2]not in aY if b=="foe"else e[dE]not in b):continue
					c.append(e);d[e[b2]]=d.get(e[b2],0)+1
				self.matches,self.counts=c,d;h=max(0,(len(c)-1)//self.n)
				if self.page>h:self.page=h
			def fill(self,now):
				d=dH(now);a=self.page*self.n;m=self.matches
				for i,r in enumerate(self.rows):c=a+i;self.assign(r,m[c]if c<len(m)else None,d)
				self.mark_here(now);n=len(m)
				if n:b="%d-%d of %d, %s"%(a+1,min(n,a+self.n),n,L(len(self.counts),"name"))
				elif bl:b="No sightings match the filters"
				else:b="No sightings yet"if ar["sightings"]else "Logging is off (settings page)"
				j(self.c["status"],u(b,self.w-2*p-236))
			def assign(self,r,e,a):
				c=r.c
				if e is None:
					if r.e is not None:
						r.prev=(r.serial,r.name,time.time());r.e,r.serial,r.name,r.nm,r.here=None,None,"","",None
						for k in("t","n","o","p","k"):j(c[k],"")
					return
				if e is not r.e:
					if r.serial is not None and r.serial!=e[eO]:r.prev=(r.serial,r.name,time.time())
					r.e,r.serial,r.name=e,e[eO],e[cZ];r.nm,r.here=u(e[cZ],124),None;j(c["o"],eU(e[dE]),aW.get(e[dE],K));b=eV(e[eP],e[eQ],e[eR]);j(c["p"],u(b+(" G"if e[dF]else ""),118));g=e[dF];d="Seen %s at %s%s"%(dI(e[b1],a),b,", in a guard zone (G)"if g else(", outside the guards"if g is False else ""));F(c["hit"],bI(fg,e[cZ],d))
				j(c["t"],dI(e[b1],a));j(c["k"],"x%d"%self.counts.get(e[b2],1))
			def mark_here(self,now):
				self.here_at=now+1.
				for r in self.rows:
					if r.e is None:continue
					t=bU.get(r.serial);a=t is not None and now-t<=2*ca+.05
					if a!=r.here:r.here=a;j(r.c["n"],r.nm,l if a else K)
		class KillerWindow(object):
			KEY="ultima.killer";TITLE="Add my killer";W=340;MINI_W,MINI_H=260,46;ROW_H=26
			def __init__(self):self.st={"minimized":False,"docked":False,"shutting":True};self.win={"g":None};self.store,self.c,self.cands=({},{}),{},[];self.until,self.slot=0.,None;self.redraw=self.want=False;self.hooks=aL(self.TITLE,0,self.st,self.win,self.ask_redraw,self.fit);self.hooks.update(show=self.zone_show,min=(self.W,self.height(1)))
			def ask_redraw(self):self.redraw=True
			def zone_show(self):self.want=True
			def fit(self,w,h,mode):fy(self,w,h,mode)
			def held(self):return C(self.KEY)
			def height(self,n):return 2*p+30+I+8+n*self.ROW_H+26
			def open(self,got,now,total=None):self.cands=[{"name":b[0],"serial":b[2]}for b in got];self.until=now+f1;self.st.update(shutting=False,docked=False,minimized=not self.held()and aN(do));self.build();n=len(got)if total is None else total;aX("you died; %s attacked you (see %s)."%(L(n,"player"),self.TITLE),f)
			def save_pos(self):
				if not self.held():ab(dn,self.win["g"])
			def close(self):
				g=self.win["g"]
				if g is None:return
				if not self.held():ab(dn,g);aa(do,self.st["minimized"])
				self.st["shutting"]=True;self.win["g"],self.c,self.cands=None,{},[];D(g)
			def end(self):
				if not self.held():self.close()
				elif self.cands:self.cands=[];self.build()
			def build(self):
				c=self.win["g"];q=self.st["minimized"];j=fz(self,self.W,self.height(1));W,H=j if j else(self.W,self.height(max(1,len(self.cands))));s,t=Kit.screen();k=self.cands[:max(1,(H-self.height(0))//self.ROW_H)]if j else self.cands;x,y=aO(dn,(max(0,((s or 1024)-W)//2),max(0,((t or 768)-H)//3)),(W,H))
				if z(c):x,y=c.GetX(),c.GetY()
				self.win["g"]=None;b,l=({},{}),{};M=p;g=G.CreateGump(True,True)
				if q:W,H=self.MINI_W,self.MINI_H;v=len(self.cands);l["status"]=aQ(g,b,W,H,self.TITLE,self.KEY,a9(self.toggle_min),"%s: %s"%(self.TITLE,L(v,"attacker")),close_tip="Close the attacker list")
				else:
					d=W-2*M;aI(g,W,H);J(g,M,M,d,30);A(g,self.TITLE.upper(),M+30,M+7,am)
					if ac(self.KEY):Z(g,M,M,d,30,lambda*a:None,None,movable=True)
					else:Kit.title_catcher(g,M,M,W-M-80-M,30,a9(self.toggle_min),key=self.KEY);E(g,b,"min",aj,W-M-74,M+7,None,an,on_click=a9(self.toggle_min));E(g,b,"close",N,W-M-54,M+4,None,"Close the attacker list")
					e=M+30+I;J(g,M,e,d,H-e-M);r="Add to foes";m=W-M-10-(35+O(r))
					for i,h in enumerate(k):n=e+8+i*self.ROW_H;w=a2(h["name"])in aY;A(g,u(h["name"],m-M-30),M+10,n+3,f);Z(g,M+6,n,m-M-14,22,a9(self.make_follow(i)),bI("Alt+click: auto-follow (again to stop)",h["name"]));l["add%d"%i]=E(g,b,"add%d"%i,ak,m,n,"On Foe list"if w else r,"Put %s on your Foe list. Alt+click: auto-follow (again to stop)"%h["name"],on_click=a9(self.make_add(i)))
					B="Closes on resurrection."if k else u("Lists your attackers when you die."if ar["killer"]else "Off (settings page)",d-20);A(g,B,M+10,e+8+len(k)*self.ROW_H+2,o)
				aS(g,x,y,W,H,self.KEY,q and self.st["docked"],None,self.save_pos);self.win["g"],self.store,self.c=g,b,l;self.redraw=False;D(c)
			def make_add(self,i):
				def a(*c):
					if i>=len(self.cands):return
					if bu():self.make_follow(i)();return
					a=self.cands[i]
					if a2(a["name"])in aY:aX("%s is already on the Foe list."%a["name"],o)
					else:dK(a["name"]);aX("added %s to the Foe list."%a["name"],l)
					b=self.c.get("add%d"%i)
					if b is not None:j(b,"On Foe list")
				return a
			def make_follow(self,i):
				def a(*b):
					if i>=len(self.cands)or not bu():return
					a=self.cands[i];s=a["serial"]
					if s is None:s,c=e9(a["name"])
					if s is None:aX("%s isn't in sight."%a["name"],f)
					else:b_(s)
				return a
			def toggle_min(self,*b):a=self.st;a["minimized"]=not a["minimized"];aa(do,a["minimized"]);self.build()
			def tick(self,now):
				if self.want:
					self.want=False;a=self.st
					if self.held()and(self.win["g"]is None or a["minimized"]or a["docked"]):a.update(shutting=False,minimized=False,docked=False);self.build()
				g=self.win["g"]
				if g is None:return
				if T(self.store,"close"):self.close()
				elif not z(g):self.win["g"],self.c,self.cands=None,{},[];self.st["shutting"]=True
				elif not self.cands and not self.held():self.close()
				elif self.redraw:self.build()
				elif self.cands and now>=self.until:self.end()
		bS=SightingsWindow();b8=KillerWindow();hR=("0aaron2sin1ba2bott3y2del3iel2el4la3y2igail3jah3na3ona3ra2ner2ra4h5am4n2sinthe1cacia3nit4tha2calia2e3lin2hen3illes2kerley1da3ir3lia3m3ra2di4son2eben3laide4e4ia5ne4le3m3na3res3sina2ie3mina3ran3va2lai3er4y2mon2olph3n4cia4ia5s3ra2rian4el5nne1elina2neas1fina2ra3ika2ton1gate4ha2nes2ustin1hara3ve2earn2imsa2mik2ren1ida4n2ella2ken3o2la3een3sa2mee4ry2n3a3hoa3sley3tzane2rlia2sling6n2tan3hne2yana1jara3y4i2inora1kako3la3ndo4ke3sma2baar2ela4lo2il4ah4i5na3na2shay1laina3ke3la3manada3n4a4d4i4na4o3qua3ric3stair3vda3zne2ben4rt6a3inka2cander3ina3ott2dea4n4r5cy3rick2ec3k4a4sy3nne3ron3ser4ia4sa3thea3x4a5nder7ra8ia9na4is2fred2ger2i3a3ce4ia3da3ke3m4a3na3son4tair3ta3x3z4a2laard4n4rd3ele4n3igra4nora4son3yn2ma2odie3nzo3ysia2phonse7o2ston2tair3hea3on2ula3mit2vin5a4ta2ysa4sa6nd2zena1ma3bel3deo4i5ka5s4o3ia3la4ia3nda5ine3ra5nde6te4is3ta2bar3er3ika4s3rose2eerah3lia5na3thyst2ie4l5la3na4ta3ssa3ta4y2mon2oke3s2sden2y1nanda3stasia2celin2ders3i3ra5ianna5s4e5a5us5w5y4ies4omeda2eida3lla3mone3zka2gela5ica6ne6que5o4ni3us2i3ca3eli3sa3ta2ke4r2n3a4bel7le4marie3e4tte3ikka3ora2oki3rah3ush2sel5me3ley3on3reana2teia3hea4ony3je3oinette4nia6o2war1olani1para2irka2olline5oina3ni2ril5le1qua3ene1ra3bella7e3celi3minta3xie2cadia3her4ibald2dath3elia4n3is4th3on2eiela3lla3n3s3tha4ina2gus2i3adne4na3cia5n3el4ne3on3sta5o6tle2kin2len5e4y3in5da3o2man3en3ina5da3on3strong2ne3old4n2on2piar2sen5io2temisia3hur2una2ziki1saria2enka2h3a3by3er3ford3lan4eigh5y4in3on3ur2ia3sa2linda2pasia2ta3er5a3ra4ea4id1talanta3ra2enne3ri2halia4n3ena4ron3la2ifa2man2ta1ubrey2da3ny3rey4ianna5c3un2gustin8a6us2ra3e4k4lia3ilia4na3kene3ora2stin2tumn1va3na3sa2ella3na3rill4y2ie3s3va1xel4la1ya3luna3me3na3sha2dee2ela2iana3la3sha3ta2la2nora2una1zaleah4ia3rael2era2ha2ilea3na3ze2ora2ura0babette2cia2e2iley3ngana2ka4ri5ne2layna3bo3der4win3e4a4ndin3i4a4n5t2mbi2nan3croft3dele3e4lla3ning2ra4n3bara3clay3den4o5n3ika3nabas6y4ett5y3on3rett4y3se3t4h5olomew4on2sha3ia4l4mah3tiaan2takah3hsheba3ya2ul2vol2xter2y3ana5i4rd3lor3o3ta2zyli1ea3can3gan3man3trice6x3u4ina4mont4regard2cca3k4y2delia2l3ana3don3en3ina5da4ta3lanca4e3ora2m3an2n3edict4n3jamin3nett3son3t4e4ley4on2radine3enger3gren3illa4t3k4eley3nadette5rd4ice3sh3t4hold4on4ram3yl2ss4ine2ta3h4ana6y3ony3ty2ulah2val4n3erly3in1ialy3n4ca2lal3lie2na3dy3ti2rdie3kita2shop2talo2xenta1jorn1lade3ine4r4se3ke3nche4da3z2enda2iss2orn2y3the1o2den2gart2hdan6a2lton2namy3d3ita3nie4y2oker3ne2rden3gny3is2tan2wie3man2yce3d4en1rad4en4ford4ney4y3ina3m3n4d5eis5i5on5y4t3xton3y3z4il2en4cis4da6n5on4na6n4t5an3t4t5a3wster2iac4n5d3ce3dget3e4g4r4tta3git6te3na4ley3ona5y3shen3tes4ta6ny2ock3derick4ny4y3nson4t4wyn3oke2uce3no3tus2yan5t3ce3nn3son1ucia3k2d3o2rgess3han3ian3ke3l3r3ton1yran3on0cadence4o3or2edmon2ilan3mile3n4e3tlin4rin2la4ndia6ra3der4well3eb4ndonia4y3ida4sta3la5n4ia5dora5e3tha3vin3ypso2m3den3elia4ron3ilia5le2nace3dace5n4ida6e4ra3tara4on3ute2oimhe2pri5ce2ra4doc3den3esse4y3i4na5e4ssa4ta3l4a4een5n4in6g4o5s5ta4ton4y3ma4el6ina5n3na4elian3ol5ina7e5yn4n3r4ick5e4ocio5ll3son3ter3ver3yn2sey3ilda3per3sandra4ia5dy5us3ta5lia4el2talina4va3erina3herine4leen4y3o4n3riona2van2yla1eara3sar2cania3il5ia2dric2landine3este3ia4na3lia2mal2relia1had4wick3im4tra3l4e4mers3nah4da5er5i5ler5ra4e5l5y4na5ing4tal3pin4man3ris6sa5ty4les5otte5ton4maine3se4tity3tha3uncy3va4iva3y4a4ton2elsea3n4ey4oa3rica6e5e4yl3sna4ter3t3valier2iara3ka4e3lali3mlis3n3po2loe4ris2o2rista7ble6ian7na8e6oph9er7s6y2uck2you1ia3nnait3r2cely4ron2ndy2ro1laire3ra4ence4inda5ssa4k3ude6tte5ia6ne3y4ton2ement7ina9e3veland2iantha3fford4ton3nt5on3ve2orinda3ver2yde1ochiti2dy2lby3e4ene4man4tte3in3lin3on3ton2man2ndon3nie4or3rad3stance7za4uela3way2ra4lie4zon3bett5y4in3coran3deali5ll3etta4y3i4nna4s3liss3nelius3rine3t4ney2ty2urtland1raig3ndall2eighton3scent4sida2ispin2osby2ystal1ullen4in3ver2rran3tis1ybele3il2nric3thia2prien2rano3ene3il5la3us2theria0dabria2cey3ia4e4o2e2g3an3mar3na2i3ly3sel4y2karai3ota2le3ila5ia3lin3ton3y2mara3ek4n3ian4en4on4tri3on2na3e4tt3ia4el6la4or3nik3te3yelle2phene4ne5ie2r3a4lis3by3en3ia4en4o3la4ene3nell3rel6l5n3yl2sha2vene3id4n5e4s4ta2wn2ya3na1eacon3n4a4dra2b3ra2cker2de2e3dee2ianira3ene3rdre2lana5ey5o3bert4in3ia4cia4lia3la5n3more3phina3sin2man3be3i4tria3psey5ter2na3by3ice3nis4ys3ton3ver2r3ek3rick4y2va4ki4l3erell3i4n3lin3net3on2wey1iamanta3ne4the2ederik4re3go3lla3ter2llian4on4y3ys2mitri2nah2onne2rk2sa2ta3i2xie1obry2die2lores2minic7k6que2na4ld4ta5ien5o3ielle3nelley7y5r3ovan2oriya2phina2ra3een3inda4s4thy3on3y2ugie4las7s2v2yle1rake2ew2ina2ucilla1uane2gan3las2lcie5nea2ncan3stan2rand3riken2san3tin4y2tch1wayne2ight1yami3n4i3stro2lan2mas3phna2na0eamon2rl4e3tha2ster2ton1bony1cho1dan4a2gan4r2ie3son3th2lyn2mund2na2olie2ria4n2ward3in5a1fia1gan1ileen2nar2rene1lad3ine3na2den3roth2ek3ora2i3anor4s3jah3na3sa4e4ka4sa3ta3za5beeth2kan3e2la3e4n4ry3iot6t4s3sworth3y2mer3o2odie3ise2sa3ie3ton2ton2wood2ynor3se4ia1ma3jane3lia3nuel2ber2elie4yne2il4io4y2ma3ett2o1ndora2gracia2id2och3la2rico4que2ye1phraim1rasma2ek2ianthe3c4a3k3n2lina2nest2ol2rol2skine2wand3in2yx1skarne2merelda2peranza2sien2ta3eban4lle3her3u1tain5a3nthe2han2ta1udocia2gene5ia2lalia2stacia1va3csa3dine4ne3n4der4geline4the2e3lyn3rett2ita2onne2zen1yota1zekial2ra0fabienne4o2ifuza3nche3rfax3th3zah2llon2ntine2rha3ima3ley3rah4ell2tin2wne2xon2y3e3ina3me1elcia3icite7y4x2mi2nn3ton2rgus3idwyn3n3onia3ran4is1ielding2lbert3inda3more2na3lay4ey3n4igan3ola2ona3renza2sk2tzgerald1lavia2eta4cher2indo4t2ora4ence3yd2ynn1orbes3rest3sythe2ster1rances7ca5ine6s7ca4ek4k5lin3sier3zer4ier2ed4a4erica8k3mont3ya2ida3eda3tz1uller3ton2scienne0gabe3riel7la8e2ge2ia3l2latea3en5o3i4na3vin3ya2mble2na3esa3non2reth3field3gan3ner3rett4ick5dan5son5tt3th3vin3y2spar3ton2uri2vin3rie2ye3le4ord3nor1elasia2mma2nevieve2off5rey6y3gia3rge6anne6tta8e5iana2radline4ldine4rd3da3ik3main3ri4y3trude2va1hislaine1iacinta3nina2deon2gi2lana3berto3da3en4s3lian2n3a3ger3ton2selle2tana3ha2von2zane1leda3n4n5a5o5ys1odfrey2lda4ie2rdon4y3man2tzone1race4ie3dy3ham3inne3m3nger4t4ville3yson3zia2ear3g4er4or6y3sham3ta4chen4te2iffen5ith1uilhem2nnar3ther2s3tave2thrie2y1wen4dolyn4eth2ynne1ytha0hackett2dara4ssa3den3i4ya3ley3rian2gan2idee3ley3mi2l3den4is3e4y3i4an4ma3le4ie3sey2milton3lin2na4n3k3nah4e3s2rden4y3ith3lan3man4oni3old3per3riet5son4y3t4ley3vey2sna3san3tin6gs2va2ya3den3es3lee3nes2zel1ea3th5er2ctor2i3di2laku3degarde3en5a5e3ki2nka3ning3rietta4y2rbert3man3schel2sper3ter1ilary3da3liard3ton2nda2roshi2sa1obart2gan2lden3ly3t2mes2pe2race3ton2shi2uston2ward3rence2yt1ugh3o2mphrey2nter4ley1yacinth2e2man2patia0iain1da2ola3nia1lene2ias2ona1man2ogene1ndia4ra3ra2es3z2ga3mar3ram4id1olana5the2na1ra3tze2ena4e2is2ma2vin5g2win1saac3beau5l6la3dora3iah3ura2is2leta2obel3ke2rael2tas1tzak1van4a3r2ory2y0jabari3ir2celyn3inda5the3k3ob5e3ques3son3y2da2el3n2far2gger2imie3one2ke3inda2l3a3eel2mal3es3ie4la6h4son2n3a3e4lle4t3ice4s3na4elle2rdena3ed4k3man3on3rod3via5nia5s2smine3on3per2van3ier2y3a3ne1ean4ette4ine2bidiah2d3idiah3rek2ff4rey2lani3ena2na4y3dayi4yose3ica3nettia4ifer3sine2remiah5y3olin4me5y3rilyn3zy2sse5e4ica2thro2wel2zebel1ibril2han2llian2n3a3ny3x2ro2vin1oakima3n4ne2bey3ihna2casa3elyn2di3y2el4le5iane2hann6a3n2ia2lan5ta3ene3ie4ne3on2nah4than6on3ina2ra3dan6e4on3gen3vin2seph6ine3hua3ie2tha2y3ce3e1uanita2dd3e3ith6a2lia5n6a6e4e5tta4nka4us2ma3oke2n3e3g2stin6e0kaatje2chine3lyn2din2ede3the2i3a3e3kara3li3mi3ros3ya2kra2la4din4ma4nit4re3b3e4a3i4ka4l5a4nda3kin3le4i3man3onice3yca2ma4l5a5i4ria3bo3eko3ilah5ia2nda3e4ne3iel4ka3tha3ya2pera2ra4n4yan3dal3el4n3ida4mah4sa3ka3l4a4enne4i4yn3mina3ol3sten3ylin4n2sa3ch3en3ia4nda3par3sia2te4b3herine4leen3ja3oka3rien5na2ula2veri3indra2y3a3e3in3la3sa2zia1eane3ra4ney2dar2efe3lan4in4y3nan2fira2gan2hinde2i3ko3r3sha3th2lby3da3eman3ia3l4en5y4i5e4y3sey3vin2n3an3dall4ra5ick3elm3ley3nard4edy5th4is3t4on3yangi4on2ona2pa2r3ani3by3ensa3n3ry3s4en4tan3win2sare3i4a3sie3ter2turah3zia2vin1halida5l2oury1ichi2efer3le3ran4nan2llian2m3berly3mie4y2n3eta3nel3sey3tan2ona2p2ra4n3by3ima3k3sten3ti2sa3ka3met3sa2ta2yoshi1liftin2og1ohana2lina2mor2ntar2ren4ssa1rischan4ten6r1urt1yle4r3y2na3thia2oko0lacey3ie2ethan2ila4ie3rd2keisha2la4sa2mar3ont2n3a3ce3der4on4ra3e3g3i2ra4ine4lee3i4ssa3k3ry3s2tika3onia2ura5na4el4ie5nda4yn2veda4rn6e3inia2wler3rence2zarus1ea3h3la3ndra3r2ba2dah2e2if3gh5ton3ko3la5na2land2n3a3e3non5r5x3or5a5e3sar2o3n4a5rd3ra2ron4y2slie3ter2tha3itia2v3ana3i2wis2xine1i2a3dan3m3n4a4e2bby2en2ke2la3ith3lian5e3y2mber2na3coln3da4say5ey3ette3nae4ea2onel2sa3ette2tsa2v2za1lewellyn2oyd1ogan2is2kelani2la2ni2ra3e4lei5le4n5zo4tta3i3ne3raine2tus2uis5e2well1ucas3ian4lle4ne3retia3y2dia2ela2is4a2ke4ne3ina3yan2lu2na3t2ther1ydia2le2nda4on3elle3n4da4ette2ris2sander3el3nadra0mabel2c3aria3er3hi3k4enzie2ddy3elaine5ina7e5on5yn3y2e2gan4ra3dalen8a6ine3ena5ta3gie3nus2hala5ia2i3a3da3sie3tane3zah2j2laya3colm3ik4la4na5da3ka3lory3u2mie2nco3da5ra4ek5r4isa4y3fred3gena3ning3on3si4ur3uel3ya2ra3c4ella4ia4os4us4y3den3ek4n3garet6ita4o5t4uirte3ia5h5m6a5n6a6na7e4bel4e5l5tta4ly6n4na4o4s5a5ha5sa3jani4eta4orie3k4ham4os3lene4in4o5n3mara3nie5na3sha6l7l4ten3ta4ha4i5n6a6go3vin3y4ann4beth4lou3zia2son2tai4na3eo3hea5r3ilda3rika3thew5ias2ud3ra4een4ice5ta2vis2x3ine3well2y3a3nard3on1ead3ra2da3ea2g3an4ra3han2i3ra2ka2la4nie5tha3ba3ia5n4na5da4senda5sa3linio3odie5y4sa3va2rcedes5r3edith4le3ill3le3rick5k2sha2ta2yer1ia3koda2cael3hael7a4ele6le2dori2gina3non3on3uel2ka3e3kel3os2les3licent5e3o3ton2n3a3da4el4y3er5va3ka3na4ie2ra4nda3em5ba4ya3iam4elle2ssy3ty2tchell3ena4xi3zi1oira2llie4y2na3ique3roe3te2on2rena3gan6a6ce3ia5h3ley3ris3timer4on3ven3z2tega1ukasa2rdoch6k3iel3phy1yles2ra3on0nada3ia4ne3ya2eem2ia3lah3mah2lini3ren2mazzi3i2n3a3cy3ette3tale5n2omi2pea2ra3da3mada2siche3tassia2talie4ne4sha3esa3han6iel2ysa2zirqah1eal4a4e2ci2diva2ely2il2kane2lek3l3son2ola3ma3na2ria4ne4ssa3on2stor2tti2va4da4n3ille4n2ysa1icanor3holas3ia3ola5e6tte2gel2ka3ki3olos2ls2mah2na2obe3la2ra3velli2ssa2ta4ra2xie1oah2din2e3l4ani4la2lan3ita2na2ra4h3bert3een3i4ko3ma5n3ris3ton1uri1ydia2le2rna2ssa0oakes3ley1belia1chen2tavia6us1delia4l3ra3ssa3tta5e2ile3n3on2on1gden1hanna1kelani1laf3the3yinka2esia2ga2iana3n4da3ver5tte4ia1mar1na2ida1pal2helia1ralie3ne2dano2en4da2iana5na3el3ole4n2lantha2man5d2nidaa2rin2son2ville1scar2good2mond1tis2to1wen0paco2ige2kuna2lmer4iera3oma2mela2ndita4ora3thea4zike3ya4in2olo2ris3ker3nell2scal6e2tamon3ia4ence3ricia6k3sy3terson4on2ul4a4ette4in6e2vel3la2xton2yton2zia1earce4l2der2g3gy2lagia2mba4roke2nda3elope3inna3n4y3thea2ony2rcival3dita3ouze3ry3sis2ter3ra2yton1haedra2earcy3dra2ilip4lip7pe4omena2oebe4nix2ylis4lis1ia2er4ce4re4son2la4n2per1laton1olly3oma2rche3ter4ia1rentice3scot7t4ton2iscilla2udence4y1yrena2thia0qamra1ueena3lla3nby4tin5on2illan3ncy4lan4n4tina3terie0rachel2d3cliffe3ella3inka3man2e2fael3ferty2gnar2i3don3zel2leigh3ph2miro3la3on5a3say4ey3ya2nard3ce3dall4ie4olph3e4e4n3ger3i3kin2oul2phael2quel2shida3ine2tri2ul2ven3i4d2wnie2y3mond3na4ell4or2ziya1eade2ba3ecca2dford3mond2ed3se3ve2gan3ina6ld4s2idun2mington3y2na4ldo4ta3dor3e4e3fry3ny2uben2x2yhan1hea3tt2iamon4nne6on2oda5nthe3nda4na2ys4sa1ia3ne2ca4rdo3hard4ter3o2der3gley2gby2hana2kki2ley2mon2ngo2o3dan3rdan2sa2ta2va1oanna3rke2bert6a6o3i4n3yn2chelle3kwell2d3erick3man3ney3rigo2ger2hanna2i2land3dan3f2na4ld4n2oney2rie3y2sa4lind8a8e7e4nne3coe3e4anne4marie7y3s2th2wan3ena3land2xana5ne2y3ce1uben3y2dd3i3yard2fus2mer2nako2skin3s4ell3ty2th4ann4erford3ledge1yan4n5e2ba2der2lan2ssa0saba3ina5y4rah3ra4ina2cha4i2de3ira2ffi3iya2gara2hale3en2idah2kari3inah3ti3ura2lihah4m5ah4na3ly3oman5e2m3antha4ra3ien4rah3mon3son3uel2ncia3ders4ia4on5r4ra5ine4ya3ford2ra4h4i5d3ee4na3gent3i4sha3ngin3ojin2sha4enka2tinka2ul3nders2vanna2wyer2xon1chuyler2otia4t1ean3rlait3son2basten6ian7en2ema2if2la3by3ena3ina3ma2mele2non3ta2rafina3gio3ilda2sha2th2ung2verin3ilin2ward2ymour1haine3kira4o3mmara3na5ta4dra5y4e4i4ley4na5on4tay5ha3rman4on4ri3shi3wn3yndel2ea3ba3ena3ffield3ila3la4by4don4ley5y3n3ridan4man4ri4win5ood2ika3n4a4g3ra4ley2obi3shana2unnar1ibley3ongile3yl2dney3onia3ra2egfried3rra2gourney2ham2las3eas3va4ia2mba3on5e2ne4ad2obhan2ran3ena3oun2tara3embile2v3an3e1kip2yler1lade2evin1mith1ofi2lana5ge3edad3ita3omon2ndra3ia3ja3ya2phia5e4ronia2rgan2terios1palding2encer4ser2ica1tacey4ia4y3ndford4ley4ton3sio2efan6ia3lla3phan7i8e5en3r4ling3sha3van4e5n3wart2ockard3ke3rm3yan2rom2uart1ubrey2katai3i2laiman3lican2mi3mer3ner2n2san5na2therland3ton2zanne1ven3tlana1ybil2delle3ney2eira2lvester4ia2na3ia0tab3ari3itha2ci4ta2d3i2ffy2hirah2i3ma3nn3pa3te2jo2ka4ra3iyah3oda2lasi3bart4ot3e3ia4tha3lulah3man3os2m3a4ra5y3ma4y2naka3ek3i3ner3o3sy3ya2o2ra3o2te3yana2urin2wnie4y2yce3lor1eague2hya2kla2m3ina2rence5tia4se3rence4ill6yn4y3tia3yn2sia3s4a1haddeus4ea3i4s3lassa4ia3man3n4a4e4os3ra2ea3kla3lma3obald4dore6sia4ne3ra4on2ierry3rza2omas3ra4pe2urston2yra1ia3ra2balt2enette3rnan5ey4ra2ffany2lda2mandra3othy2na2ponya2rza2tus2vona1obey3ias3y2d3d2la2mas2ng2r3a3i4n3rance3y2sia2ve2wnsend1racey4y3vers4is2easa3main7e3nt3sa3va4or3y2ianon3cia3lby3na4d3sh5a4tan2oy2udy2yne3on3phena1ucker2lly1yee2ler2mon2ne2rone0ula3ni2tima1ma1na2dine1pton1rania2iah4n5a2sula1ta0vala3entina4ria6e4ska3onia4ra2n3ce3da3essa3ora3ya2shti2ughn1eda2lika3ma2nesssa2ra3ena3ity3n4on3onica2sta2vila1ictor6ia2donia2ncent3son2olet6ta2rgil5nia3idis2to2veka3ian1lad4imir1okes2leta3f1rinda0wade2gner2kanda2lden4o3ker3lace4y3ter2nda3eta2rd3ner3ren2tson2ylan6d4on3ne1ebb3ster2ndell4y2sley3ton2ylin1hilhelmina3taker4ney1ijdan2lfen3l4ard4em4iam4ow3ma3ona3son2nda3ema3ifred3na3ona3ston3throp1lby1oody1yatt2nee3n3ona0xanthe2veria3ier6a1ena3ia3os2rxes1imen5a1ylia3ona0yachne2kecan2le2ncey3ice2rdley3in3milla2smeen4in1elinda2nene2rik3o3vant2smina2tta2va1okiko2landa3ie2nina2rk2vela1usuf1vella3s3tte2onne0zachariah6y3kery2da2hara3irah3ra2id4e2kia2lea3ika3tana2ndra3e3iel3n2ra4h3ed4k2za1ehava2ke2lda3enka3ia3la2na4ide3ia3on2rlinda2va3ida1ia3zan2gana2la2na3nia2on2ta2ven1oe2la2na2ra4h3da3n2sia1uleika4ma2za4nny");fA=[None]
		def hS():
			a=fA[0]
			if a is None:
				a,b=set(),""
				for d,c in re.findall(r"(\d)([a-z]*)",hR):b=b[:int(d)]+c;a.add(b)
				fA[0]=a
			return a
		def fB():return tuple(tuple(a)for b,a in sorted(aC.items()))
		a4={"f":None,"seen":None,"stable":0,"loaded":False,"lines":None,"save_at":0.}
		def hT():
			if aM["started"]or a4["loaded"]:return
			fG();a4["loaded"]=True
			def a():
				try:a4["lines"]=eJ()
				except Exception as a:cV[0]="could not read the save file: "+str(a);a4["lines"]=()
			eI(a)
		def hU():
			a=a4["lines"]
			if a is None:return False
			a4["lines"]=None
			if aM["started"]or not a:return False
			eK(a[0],a[1]);return True
		def b9():
			if aM["started"]:aM["dirty_save"]=True
			else:a4["save_at"]=time.time()+f9
		def fC(background):
			if a4["save_at"]:a4["save_at"]=0.;cY(background=background)
		def hV():return all(bool(aC[a][4])for a in bk+["combat"])
		ic={};fD={"top":32,"pad":6,"ldy":0,"sdy":4,"fh":26,"lw":110,"ugap":6}
		def fE(w):a={"dx":320,"bdy":0,"h":26};return(("WINDOWS",(("slider","scale","Scale:","Size of the trackers and pop-out bars (%d-%d)"%(c7,c8),c7,c8,{"unit":"%"}),("slider","opacity","Opacity:","Background opacity of every window (0-100)",0,100,{"unit":"%"}),("slider","range","Range:","Tracker range in tiles (%d-%d)"%(c9,da),c9,da,{"unit":"tiles"}),("gap",-78),("check","sync","Sync tracker sizes","Resizing one tracker resizes the others",a),("buttons",(("unanchor",N,"Unanchor all","Undo every anchor between windows"),),a),("buttons",(("reset",N,"Reset to defaults","Reset scale, opacity, range, options and window places"),),a),("check","lock","Lock the windows in place","Free windows can't be moved or resized (zoned windows stay put anyway)"))),("OPTIONS",(("check","combat_only","Combat bars: only once fighting","Only add a mobile once it attacks you, you attack it in war mode, or it fights you up close",{"stay":True}),("check","borders","Show a border on the pop-out bars","Stone border round the pop-out bars (the other windows always have one)",{"dx":320,"h":28}),("check","magery","Magery buttons","P (Poison) and Z (Paralyze) on the combat bars; H (Heal) and C (Cure) on friends, Shift+click for the greater spell",{"stay":True}),("check","healing","Bandage button","B on friends' bars: bandage when adjacent, else follow them",{"dx":320}))),("SIGHTINGS AND DEATHS",(("check","sightings","Log players who come into range","Each non-friend player goes in the Sightings log once per visit (last %d kept)"%cv,{"stay":True}),("buttons",(("sightings",H,"Open Sightings","Open the Sightings window"),),{"dx":320}),("check","killer","On death: list your attackers","A window lists players who attacked you in the last %d s, each with Add to foes"%int(dj)))),("FOE ALERT  (sound: Settings > Alerts)",(("check","alert_red","Red","Alert on a red (murderer) in range",{"stay":True}),("check","alert_foes","Foe list","Alert on a Foe list player in range (linked alts too)",{"stay":True,"dx":110}),("check","alert_orange","Orange","Alert on an orange (enemy) in range",{"stay":True,"dx":230}),("check","alert_gray","Grey","Alert on a grey (criminal) in range",{"dx":340,"h":28}),("slider","alert_minutes","Same player again after:","Minutes before the same player alerts again (%d-%d)"%(dg,dh),dg,dh,{"lw":178,"sw":150,"ugap":12,"unit":"%d min"%ar["alert_minutes"]}))))
		hW=Kit.Page(ar,fE,opts=fD)
		def hX(g,x,y,w):hT();a4.update({"f":Kit.Form(g,x,y,w,dict(ar,lock=hV()),fE(w),**fD),"stable":0,"seen":{a:ar[a]for a in ek}})
		def hY():
			f=a4["f"]
			if f is None:return
			if hU():a4["f"]=None;aB("ultima");return
			cX();n=time.time()
			if a4["save_at"]and n>=a4["save_at"]:fC(True)
			i,a=f.store,a4["seen"];b=aZ["windows"]
			if T(i,"unanchor"):a6.clear();b9();aX("every window unanchored.",l)
			if T(i,"reset"):
				if aZ["panel"]is not None:aZ["panel"].reset_defaults()
				else:er();b9();aX("settings and windows reset to the defaults.",l)
				aB("ultima");return
			f.vals=dict(ar,**a);c=f.read();g=c["scale"]
			if g!=a["scale"]:a["scale"]=g;a4["stable"]=0
			elif g!=ar["scale"]:
				a4["stable"]+=1
				if a4["stable"]>=2:
					if b is not None:hF(g,b)
					else:ar["scale"]=g;b9()
			h=c["opacity"]
			if h!=a["opacity"]:
				a["opacity"]=h
				if aZ["panel"]is not None:aZ["panel"].set_all_opacity(h)
				else:ar["opacity"]=h;b9()
			for k in("range","alert_minutes"):
				if c[k]==a[k]:continue
				a[k]=ar[k]=c[k];b9()
				if k=="alert_minutes":j(f.c["alert_minutes_lbl"],"%d min"%c[k])
			if T(i,"sightings"):
				if aZ["windows"]is not None:bi["sight_req"]=True
				else:aX("the trackers aren't up yet; try again in a moment.",o)
			d=bool(c.get("lock"))
			if a.get("lock")is None:a["lock"]=d
			elif d!=a["lock"]:
				a["lock"]=d
				if b is not None:
					for k in bk:b[k].set_locked(d)
				if aZ["panel"]is not None:aZ["panel"].combat.set_locked(d)
				else:
					for k in bk+["combat"]:aC[k][4]=d
				bo()
			for e in("borders","healing","magery","combat_only","sync","alert_red","alert_foes","alert_orange","alert_gray","sightings","killer"):
				v=c[e]
				if v==ar[e]:continue
				ar[e]=v;b9()
				if e=="borders":eH()
				elif e=="healing"and not v:a5["serial"]=None
				elif e=="sync"and v and b is not None:m=[b[q]for q in bk if not b[q].minimized];fj(b,m[0]if m else b[bk[0]]);aX("tracker sizes synced.",l)
		def hZ():a4["f"]=None;fC(True)
		bi={"last_layout":None,"tick":0,"errors":set(),"next_scan":0.,"next_combat":0.,"next_glow":0.,"sight_req":False,"next_hp":0.}
		def c6(key,step,now):
			t=bi[key]
			if now<t<=now+step:return False
			bi[key]=t+step if 0<=now-t<step else now+step;return True
		def h_():
			c,d,b=aZ["windows"],aZ["combat"],aZ["panel"];a={g:(c[g].gump,c[g].size)for g in bk}
			if d.is_open():a["combat"]=(d.gump,(aC["combat"][2],0))
			if b.gump is not None:a["panel"]=(b.gump,b.size)
			for s,e in a8.items():a["pop:%d"%s]=(e.gump,e.size)
			return a
		def fF():
			for w in(aZ["windows"]or{}).values():w.snapshot()
			if aZ["combat"]is not None:aZ["combat"].snapshot()
		def h0(view,title,fit):
			def c():
				if view.gump is None or aM.get("shutting"):return
				return "docked"if view.docked else("minimized"if view.minimized else "open")
			def b(on):B(view.gump,"IsVisible",on)
			def a(docked,mini):
				def f():
					if view.minimized!=mini:view.toggle_minimize()
					view.docked=docked;b(not docked)
				return f
			def d():view.docked=False;b(True)
			def e():
				if view.gump is None and view is aZ["combat"]:bY.append(view.show)
				else:a(False,False)()
			return{"title":title,"icon":0,"state":c,"show":e,"dock":a(True,True),"undock":d,"minimize":a(False,True),"gump":lambda:view.gump,"fit":fit,"exact":True,"verify":True,"redraw":view.zone_chrome}
		def h1(windows,combat):
			for c,w in list(windows.items())+[("combat",combat)]:ax("ultima."+c,h0(w,d7[c],w.layout_fit));bT.add(ay,"ultima."+c)
			for a,b in(("ultima.sightings",bS.hooks),(b8.KEY,b8.hooks)):ax(a,b);bT.add(ay,a)
		def fG():
			for d in(aY,bs,be,a8,bC,bp,bV,b5,cp,bb,a1,cI,bc,bP):d.clear()
			bQ[0]=None;dC[0]=b0[0]=0.;co[0]=0
			for q in(ce,b6,bR,bH,cL,cj,bY,bl):del q[:]
			cq[0]+=1;eq();ar.update(em);a_.update(req=False,size={},own_size={},force=set(),made={});aM.update(gx,party=set());a5.update(serial=None,follow=None);a6.__init__();bg.update(serial=None,stale=False);bX[0]=cW[0]=False;a4.update({"loaded":False,"lines":None,"save_at":0.});br["learn"]=br["attack"]=br["killer"]=None;fq.update(serial=None,until=0.);e7[0]=-10.
			for a in list(bO):bG(a)
			a3.update(dirty=False,save_at=0.);a3["ver"]+=1;a3["seen_ver"]+=1;bD[0]=None;bf["dead"]=bf["me"]=None
		def h2():
			a=None
			if a4["save_at"]:a4["save_at"]=0.;a=eM()
			fG();aM["started"]=True
			for k in br:br[k]=X()
			gE();bi["errors"]=set();af(d_,"Foe in range",fZ);bT.service("ultima.is_foe",g8);bT.service("ultima.classify",he);bT.service("look.ultima",lambda:bY.append(hD));cj.append(lambda:h3(a))
		def h3(a=None):
			if aM["shutting"]:return
			if a is not None:cn[0]+=1;eN(a,cn[0]);cX()
			gS();a6.saved=a6.saved_groups();gT();aM["loaded"]=True
		def h4():
			if aZ["windows"]is None:
				if aM["loaded"]and not aM["shutting"]:gX()
				return
			cX();gD();eu(bY)
			while ce:az(ce.pop(0))
			if du:del du[:];ai(fH)
			b,d,i=aZ["windows"],aZ["combat"],aZ["panel"]
			if b is None:return
			hG(b);a=time.time()
			try:
				try:
					if bi["sight_req"]:bi["sight_req"]=False;bS.bring()
					bS.tick(a);b8.tick(a)
				except Exception as c:
					if V():return
					bW(c)
				hO();gN();a6.tick(h_)
				if a6.groups_changed():aM["dirty_save"]=True
				if c6("next_glow",gi,a):
					f=fd();b["friend"].pulse(f)
					for e in list(a8.values()):e.pulse(f)
				if c6("next_scan",ca,a):
					j=hh()
					try:ho(a)
					except Exception as c:bW(c)
					if ch():return
					for g in bk:b[g].update(j[g])
					for e in list(a8.values()):e.update()
					if ch():return
					hE(b);i.update();gO();bi["tick"]+=1
					if bi["tick"]%fQ==0:
						fF();h=fB()
						if h!=bi["last_layout"]or aM["dirty_save"]or(a3["dirty"]and a>=a3["save_at"]):bi["last_layout"]=h;bo()
				if c6("next_combat",ca if d.docked else fJ,a)and not ch():d.tick()
				if c6("next_hp",fK,a)and not ch():h5(b,d)
			except Exception as c:
				if V():return
				bW(c)
		def h5(windows,combat):
			for w in windows.values():
				if w.minimized or w.docked or not z(w.gump):continue
				for r in w.rows:
					e=r.e
					if not r.shown or not e or not e["hmax"]or e.get("mob")is None:continue
					try:c,b=e["mob"].Hits or 0,e["mob"].HitsMax or 0
					except Exception:continue
					if b>0:e["hits"],e["hmax"]=c,b;r.values(e)
			if combat is None or combat.docked or combat.minimized or not z(combat.gump):return
			for r in combat.rows:
				d=r.e
				if not r.shown or d is None:continue
				m=c4.get(d[0])
				if m is None:continue
				try:a=(m.Hits or 0,m.HitsMax or 0)
				except Exception:continue
				if a[1]>0 and a!=d[3:5]:r.values(d[:3]+a+d[5:])
		def h6():
			if eu(cj):return
			if bX[0]:bX[0]=False;cY(background=True)
		def h7():return bool(cj)or bool(bX[0])
		def h8():
			aM["shutting"]=True;aM["started"]=False;bS.close(stopping=True);b8.close();bT.close()
			for c in list(bO):bG(c)
			if aZ["windows"]is None:return
			safe(lambda:Kit.on_client(fF));bX[0]=False;cY();a=[]
			for w in aZ["windows"].values():a.append(w.gump);w.gump=None
			if aZ["combat"]is not None:a.append(aZ["combat"].gump);aZ["combat"].gump=None
			if HOST.hub is not None:HOST.hub.remove("ultima")
			for b in list(a8.values()):a.append(b.gump);b.gump=None
			a8.clear()
			for g in a:D(g)
			cl(a5["follow"]);aZ.update({"windows":None,"combat":None,"panel":None})
		return{"start":h2,"tick":h4,"stop":h8,"client_tick":True,"config_height":hW.height,"build_config":hX,"poll_config":hY,"config_closed":hZ,"thread_tick":h6,"thread_wanted":h7}
	def a_():
		aa="lookout";s="Lookout";ab="Lookout_settings";aS="Lookout_pos";aX="Lookout_min";aY="_lookout_feed.txt";W=370;ag,aZ=280,46;a_=2597;H=5;a0=30;t=22;M,P=3,24;a1=.25;ai=30.;aj=5.;v=20.;a2=.1;ak=15.;al=32768;am=60;e=65536;a3=30.;a4=120.;an=10.;ao=200;S=1.;T=400;a5=1000;aq=8;at=10.;au=.25;av="lookout.alarm";a6=824;ax="lookout.lost";a7=74;ay=60.;z=0x4C4F4F4B;a8=("Click: tracking arrow to where they were seen (again to clear). Alt+click: auto-follow (again to stop)");b={"watch":False,"listen":True,"range":18,"ping":True,"lost":True};bz=dict(b)
		def az():return{"shutting":False,"minimized":False,"docked":False,"queue":[],"me":0,"path":None,"facet":-1,"next_scan":0.,"present":{},"in_range":0,"hb_next":0.,"outbox":[],"write_next":0.,"pings":[],"ping_next":0.,"listeners":{},"listeners_next":0.,"offset":0,"listen_next":0.,"announce_next":0.,"seen":{},"inbox":[],"watchers":{},"file":"none","recent":[],"arrow":None,"own_alarm":None,"dirty":True,"refresh_at":0.}
		a={"minimized":False,"shutting":False,"docked":False,"queue":[]};a.update(az());c={"g":None,"c":{},"store":({},{}),"rows":[]};aA,V,aB=aJ(a,s);aD,a9={"range":(M,P)},("watch","listen","range","ping","lost")
		def aE():Kit.kv_load(ab,";",b,aD)
		def aF():Kit.kv_save(ab,";",b,a9,aD)
		def C():
			p=a["path"]
			if p is None:p=a["path"]=aK(aY)
			return p
		def g(now,key,step):
			t=a[key]
			if now>=t or t-now>step:a[key]=now+step;return True
			return False
		def aG(text):return str(text or "").replace("|","/").replace("\n"," ").replace("\r"," ").strip()
		def aH(ev,short=False):
			c,d=ev["lx"],ev["ly"]
			if not(c or d):return "at %d,%d"%(ev["x"],ev["y"])
			a,b=ev["x"]-c,ev["y"]-d;e=max(abs(a),abs(b))
			if e==0:return "at the lookout"
			if short:return "%d %s"%(e,Kit.compass(a,b))
			return aT(a,b)+" of the lookout"
		def h(serial,name,noto,x,y,facet,count,lx,ly,pinged=False):s="%.2f|%d|%s|%s|%d|%d|%d|%d|%d|%d|%d|%d\n"%(time.time(),serial,aG(name),aG(noto),x,y,facet,count,lx,ly,a["me"],1 if pinged else 0);return s.encode("utf-8")
		def q(data):
			b=a["outbox"];b.append(data)
			if len(b)>ao:del b[:-ao]
		def X(raw):
			try:
				s=raw.decode("utf-8","replace").strip()
				if not s:return
				p=s.split("|")
				if len(p)<8:return
				a={"t":float(p[0]),"key":p[0],"serial":int(p[1]),"name":p[2],"noto":p[3],"x":int(p[4]),"y":int(p[5]),"facet":int(p[6]),"count":int(p[7]),"lx":int(p[8])if len(p)>8 else 0,"ly":int(p[9])if len(p)>9 else 0,"from":int(p[10])if len(p)>10 else 0,"pinged":len(p)>11 and p[11]=="1"}
				if not 0.<a["t"]<1e11:return
				return a
			except Exception:return
		def aI():
			c=a["outbox"];n=len(c);d=C()
			try:
				with open(d,"ab")as f:f.write(b"".join(c[:n]))
			except Exception:a["write_next"]=time.time()+S;return
			del c[:n]
			try:e=os.path.getsize(d)
			except Exception:return
			if e>(al if b["watch"]else 4*al):ba(d)
		def ba(path):
			with Kit.quiet:
				with open(path,"rb")as h:a=h.read()
				f=a.rfind(b"\n")+1;a=a[:f];g=[k for k in a.split(b"\n")if k.strip()];b=g[-am:];c=set()
				for d in reversed(g[:-am]):
					if b"|listen|"in d and len(c)<aq:
						e=X(d)
						if e is not None and e["from"]not in c:c.add(e["from"]);b.insert(0,d)
				def i():
					with open(path,"rb")as a:a.seek(f);return a.read()
				aU(path,b"\n".join(b)+(b"\n"if b else b""),tail=i)
		def bb(path):
			try:c=os.path.getsize(path)
			except Exception:a["file"]="none";return
			b=a["offset"]
			if c<b:b=0
			if c-b>e:b=c-e;h=True
			else:h=b>0 and b!=a["offset"]
			if c==b:a["offset"]=b;a["file"]="ok";return
			try:
				with open(path,"rb")as i:i.seek(b);d=i.read(min(c-b,e))
			except Exception:a["file"]="busy";return
			a["file"]="ok";g=d.rfind(b"\n")
			if g<0:a["offset"]=b+len(d)if len(d)>=e else b;return
			a["offset"]=b+g+1;f=d[:g].split(b"\n")
			if h and f:f=f[1:]
			return f
		def bc(now):
			e=bb(C())
			if not e:return
			g=a["me"];c=a["seen"];d=a["inbox"]
			for h in e:
				b=X(h)
				if b is None or b["from"]==g or b["noto"]=="listen":continue
				k=(b["key"],b["serial"],b["from"])
				if k in c:continue
				f=now-b["t"]
				if f<-5. or(b["serial"]and f>ak):continue
				c[k]=b["t"];d.append(b)
			if len(c)>T:
				i=now-4*ak
				for k in[m for m,n in c.items()if n<i]:del c[k]
				if len(c)>T:j=sorted(c.items(),key=lambda a:a[1])[-(T//2):];c.clear();c.update(j)
			if len(d)>100:del d[:-100]
		def bd(now):
			c=C()
			try:
				d=os.path.getsize(c)
				with open(c,"rb")as f:
					if d>e:f.seek(d-e)
					i=f.read(e)
			except Exception:return
			g={}
			for h in i.split(b"\n"):
				if b"|listen|"not in h:continue
				b=X(h)
				if b is not None and b["noto"]=="listen"and b["from"]and-5.<=now-b["t"]<=a4:g[b["from"]]=b["t"]
			a["listeners"]=g
		def be(m,serial):
			if m.IsRenamable:return
			a=R(m)
			if a in("invulnerable","ally"):return
			if not(m.IsHuman or m.IsGargoyle):return
			if API.IsFriend(serial):return
			if aV.search(str(m.Name or "")):return
			return a
		def bf(now):
			p=Q()
			if p is None:return
			t=int(p.Serial);j,k=int(p.X),int(p.Y);f=int(API.GetMap());a["me"],a["facet"]=t,f;A=ah(b["range"]);u=set(int(bA)for bA in(API.GetPartyMemberSerials()or()));v=HOST.services.get("ultima.classify");B=a["listeners"];l=[]
			for m in A:
				try:
					if m is None:continue
					c=int(m.Serial)
					if c==t or c in u or c in B:continue
					if v is not None:
						r=v(m,u)
						if r is None or r[0]=="friend"or r[3]:continue
						d=r[2]
					else:
						if m.IsDead:continue
						d=be(m,c)
						if d is None:continue
					if API.OnIgnoreList(c):continue
					l.append((c,m,d))
				except Exception:continue
			e=a["present"];s=[]
			for c,m,d in l:
				w=e.get(c)
				if w is None or now-w>ai:s.append((c,m,d))
				e[c]=now
			if len(e)>len(l):
				for C in[bB for bB,bC in e.items()if not 0<=now-bC<=ai]:del e[C]
				if len(e)>a5:e.clear()
			n=len(l)
			if n!=a["in_range"]:a["in_range"]=n;a["dirty"]=True
			D=b["ping"]and HOST.services.get("pings.send")is not None;i=[]
			for c,m,d in s:
				try:o,x,y=str(m.Name or "")or "(unknown)",int(m.X),int(m.Y)
				except Exception:continue
				z=D and len(a["pings"])<8;q(h(c,o,d,x,y,f,n,j,k,z))
				if z:a["pings"].append([x,y,f,"Lookout: "+o,now+at])
				E={"t":now,"serial":c,"name":o,"noto":d,"x":x,"y":y,"facet":f,"count":n,"lx":j,"ly":k,"src":"here"};aL(E);i.append("%s (%s)"%(o,U.get(d,d)))
			if i:aB("spotted %s, %s in range."%(", ".join(i[:4])+(" and %d more"%(len(i)-4)if len(i)>4 else ""),L(n,"player")))
			if s or g(now,"hb_next",aj):a["hb_next"]=now+aj;q(h(0,"","watch",j,k,f,n,j,k))
		def bg(now):
			c=a["pings"]
			if not c or(now<a["ping_next"]and a["ping_next"]-now<=au):return
			d=HOST.services.get("pings.send")
			if d is None or not b["ping"]:del c[:];return
			x,y,m,f,g=c[0]
			if not 0<=g-now<=at:c.pop(0);return
			try:e=d(x,y,m,"danger",f)
			except Exception:e=True
			if e:c.pop(0)
			else:a["ping_next"]=now+au
		def bh():
			a["present"].clear();a["in_range"]=0;del a["pings"][:]
			if a["me"]:q(h(0,"","off",0,0,a["facet"],0,0,0))
			a["dirty"]=True
		def aL(ev):b=a["recent"];b.insert(0,ev);del b[a0:];a["dirty"]=True
		def bi(ev,now):
			b=a["watchers"];w=b.get(ev["from"])
			if w is None:
				if len(b)>=aq:del b[min(b,key=lambda k:b[k]["t"])]
				w=b[ev["from"]]={"t":0.,"told":False}
			if ev["t"]<w["t"]:return
			w.update({"t":ev["t"],"state":ev["noto"],"x":ev["x"],"y":ev["y"],"facet":ev["facet"],"count":ev["count"]});w["told"]=ev["noto"]!="watch"or not-5.<=now-ev["t"]<=v;a["dirty"]=True
		def bj(ev):
			d=ev["noto"];c="%s (%s)%s, %s"%(ev["name"],U.get(d,d),(", %d players"%ev["count"])if ev["count"]>1 else "",aH(ev))
			if ev["facet"]!=a["facet"]and a["facet"]>=0:c+=" in "+ar(ev["facet"])
			e=None
			if b["ping"]and not ev["pinged"]and ev["facet"]==a["facet"]and HOST.services.get("pings.send")is not None:e=(ev["x"],ev["y"])
			ae(av,c,level="alarm",ping=e,who=ev["serial"]);a["own_alarm"]=(c,time.time());ev["src"]="lookout";aL(ev)
		def bk(now):
			d=a["inbox"]
			if d:
				f,a["inbox"]=d,[]
				for c in f:
					if c["serial"]:bj(c)
					else:bi(c,now)
			if not b["lost"]:return
			for g,w in a["watchers"].items():
				if w["told"]or w.get("state")!="watch":continue
				e=now-w["t"]
				if e>v:w["told"]=True;a["dirty"]=True;ae(ax,"Lookout quiet for %d s"%int(e),level="warn",who=g)
		def bl(i):
			def a():
				b=c["rows"]
				if i>=len(b):return
				r=b[i];a=r["ev"]
				if r["prev"]is not None and time.time()-r["at"]<=.15:a=r["prev"]
				if a is None:return
				if ad():V(("follow",a["serial"]))();return
				V(("arrow",a["x"],a["y"],a["facet"]))()
			return a
		def aN():return p+30+I
		Y=58
		def D(n=H):return aN()+Y+I+30+n*t+6+p
		def aO():
			z=d.slot if ac(aa)and not a["minimized"]else None
			if z is not None and(z[0]<W or z[1]<D(1)):z=None
			w,i=z if z else(W,D());n=d.rows(t,D(0),H)if z else H;g,m,e=d.begin(w,i);M=p;j=[]
			if not a["minimized"]:
				b=w-2*M;d.frame(g);e["info_w"]=b-196;c=aN();J(g,M,c,b,Y);k=w-M-12-35-O("Clear");E(g,m,"clear",N,k,c+28,"Clear","Clear the list, alarm line and tracking arrow",on_click=V("clear"));e["watch"]=A(g,"",M+12,c+9,o);e["listen"]=A(g,"",M+12,c+32,o);e["tw"]=(b-24,k-8-(M+12));f=c+Y+I;J(g,M,f,b,i-f-M,"SPOTTED  (newest first)")
				for l in range(n):h=f+28+l*t;r={"name":A(g,"",M+12,h+2,K),"info":A(g,"",M+12+180,h+2,o),"ev":None,"prev":None,"at":0.,"tip":None,"shown":True};r["hit"]=Z(g,M+6,h,b-12,t,bl(l),"");j.append(r)
			d.end(g,{"rows":j});a["dirty"]=True;aR(time.time())
		d=Kit.Window(aa,s,a,c,aO,aS,aX,(220,220),(ag,aZ),a_,aA,lock=True,clear={"rows":[]})
		def aP():
			if not b["watch"]:return "off",o
			n=a["in_range"]
			if n:return "%d tiles, %s in range"%(b["range"],L(n,"player")),f
			return "%d tiles, all clear"%b["range"],l
		def aQ(now):
			if not b["listen"]:return "off",o
			c=None
			for w in a["watchers"].values():
				if c is None or w["t"]>c["t"]:c=w
			if c is None:
				if a["file"]=="busy":return "the feed is busy, trying again",o
				return "no lookout heard yet",o
			d=ap(now-c["t"],aC)
			if c.get("state")=="off":return "the lookout stopped %s ago"%d,o
			if not-5.<=now-c["t"]<=v:return "the lookout has been quiet for %s"%d,f
			n=c.get("count",0);e="%d,%d"%(c.get("x",0),c.get("y",0))
			if n:return "the lookout at %s sees %s"%(e,L(n,"player")),f
			return "the lookout at %s, all clear"%e,l
		def bm(now):
			c=a["own_alarm"]
			if c is not None and 0<=now-c[1]<=ay:d,e=c[0],f
			elif b["listen"]:d,e=aQ(now)
			else:d,e=aP()
			return "%s: %s"%(s,d),e
		def bn(r,ev,now):
			if ev is not r["ev"]:r["prev"],r["ev"],r["at"]=r["ev"],ev,now
			if ev is None:
				if r["shown"]:j(r["name"],"");j(r["info"],"");B(r["hit"],"IsVisible",False);r["shown"]=False
				return
			if not r["shown"]:B(r["hit"],"IsVisible",True);r["shown"]=True
			b=ev["noto"];j(r["name"],u("%s (%s)"%(ev["name"],U.get(b,b)),172),aW.get(b,K));d="lookout"if ev.get("src")=="lookout"else "here";f=aH(ev,True)if d=="lookout"else "%d,%d"%(ev["x"],ev["y"]);j(r["info"],u("%s, %s ago (%s)"%(f,ap(now-ev["t"],aC),d),c["c"]["info_w"]));e="%s (%s), seen %s at %d,%d%s. %s"%(ev["name"],U.get(b,b),"by the lookout"if d=="lookout"else "here",ev["x"],ev["y"],""if ev["facet"]==a["facet"]else " in "+ar(ev["facet"]),a8)
			if e!=r["tip"]:r["tip"]=e;F(r["hit"],e)
		def aR(now):
			m=c["g"]
			if m is None or(a["minimized"]and a["docked"]):return
			e=c["c"]
			if a["minimized"]:b,d=bm(now);j(e["status"],u(b,ag-90),d);return
			k=e["tw"];b,d=aP();j(e["watch"],u("Watch: "+b,k[0]),d);b,d=aQ(now);g=a["own_alarm"]
			if g is not None and 0<=now-g[1]<=ay:b,d=g[0],f
			else:b="Listen: "+b
			j(e["listen"],u(b,k[1]),d);h=a["recent"];i=c["rows"]
			for l,r in enumerate(i):bn(r,h[l]if l<len(h)else None,now)
			if not h and i:j(i[0]["name"],"No one spotted yet.",o)
		def bo(x,y,m):
			b=a["facet"];c=a["arrow"];API.TrackingArrow(-1,-1,z);a["arrow"]=None
			if c==(x,y,m):return
			if b>=0 and m!=b:aB("that spot is in %s."%ar(m));return
			API.TrackingArrow(x,y,z);a["arrow"]=(x,y,m)
		def bp(action):a["recent"]=[];a["own_alarm"]=None;aM(a,z);a["dirty"]=True
		bq={"clear":bp,"follow":lambda action:aw(action[1],s),"arrow":lambda action:bo(action[1],action[2],action[3])}
		def br(w):return(("WATCH AND LISTEN  (two clients, one TazUO folder)",(("check","watch","Watch: this client is the lookout","Park it hidden and still; it reports every player in range to the other client (not party, friends or guild)"),("check","listen","Listen: this client gets the alarms","Alarm for each player a lookout reports (sound: Settings > Alerts)"),("slider","range","Watch range:","Watch range in tiles (%d-%d)"%(M,P),M,P,{"ldy":6,"sdy":4,"lw":98,"sw":160,"ugap":10,"vfmt":"%d tiles","h":32}),("check","ping","Danger ping on the map where a player is spotted","Needs World Map > Map Pings; guildmates see it too"),("check","lost","Warn when the lookout is quiet for %d s"%int(v),"Its client closed, crashed or lost the connection")),{"top":32,"pad":4}),)
		def bs(b,new):
			for k in("watch","listen","ping","lost"):
				if new[k]!=b[k]:bt(k,new[k])
			a["dirty"]=True
		def bt(k,on):
			if k=="watch":
				if on:a["next_scan"]=a["hb_next"]=a["listeners_next"]=0.
				else:bh()
			elif k=="listen":
				if on:a["listen_next"]=a["announce_next"]=0.
				else:a["inbox"]=[]
			elif k=="ping"and not on:del a["pings"][:]
			a["refresh_at"]=time.time()
		G=Kit.Page(b,br,aF,bs);aE()
		def bu():a.update(az(),minimized=d.start_min());aE();p=API.Player;a["me"]=int(p.Serial)if p is not None else 0;a["facet"]=int(API.GetMap());C();af(av,"Lookout spotted a player",a6);af(ax,"Lookout went quiet",a7);aO();d.dock(fit=True,min=(W,D(1)))
		def bv():
			if c["g"]is None:return
			if Kit.closed(c):return
			while a["queue"]:
				f=a["queue"].pop(0)
				if d.action(f):continue
				h=bq.get(f[0]if isinstance(f,tuple)else f)
				if h is not None:h(f)
			e=time.time()
			if b["watch"]:
				if g(e,"next_scan",a1):bf(e)
				bg(e)
			elif b["listen"]and g(e,"next_scan",1.):
				p=API.Player
				if p is not None:a["me"]=int(p.Serial);a["facet"]=int(API.GetMap())
			if b["listen"]:bk(e)
			if a["dirty"]or g(e,"refresh_at",1.):a["dirty"]=False;aR(e)
		def bw():
			if a["shutting"]:return
			c=time.time()
			if b["listen"]and a["me"]and g(c,"announce_next",a3):q(h(0,"","listen",0,0,a["facet"],0,0,0))
			if a["outbox"]and(c>=a["write_next"]or a["write_next"]-c>S):aI()
			if b["watch"]and g(c,"listeners_next",an):bd(c)
			if b["listen"]and a["me"]and g(c,"listen_next",a2):bc(c)
		def bx():
			if a["shutting"]:return False
			c=time.time()
			if b["listen"]and a["me"]:return True
			if a["outbox"]and not 0<a["write_next"]-c<=S:return True
			return bool(b["watch"])and not 0<a["listeners_next"]-c<=an
		def by():
			a["shutting"]=True
			if b["watch"]and a["me"]:q(h(0,"","off",0,0,a["facet"],0,0,0));aI()
			aM(a,z);aF();aA.close()
		return{"start":bu,"tick":bv,"stop":by,"client_tick":True,"config_height":G.height,"build_config":G.build,"poll_config":G.poll,"config_closed":G.closed,"thread_tick":bw,"thread_wanted":bx}
	a0=(("tracker",aZ,.05,"ultima"),("lookout",a_,.1,"lookout"),);return PartSet(aX,aY,a0).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("ultima","Ultima Tracker","Friends, foes and neutrals near you",_module_ultima,.05,category="The world",parts=(("tracker","Tracker","Trackers and combat bars",True,("ultima",)),("lookout","Lookout","A second client keeps watch",False,("lookout",)),),aliases=('Combat Bars','Lookout','foe','sightings','trackers','second client'))
