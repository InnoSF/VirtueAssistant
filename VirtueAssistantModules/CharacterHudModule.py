def _module_hud():
	aJ=Client._member;W=Client._type;ac=Follow.alt_held;X=Follow.toggle;am=HOST.alert;ad=HOST.alert_kind;aK=HOST.claim_cursor;Y=HOST.cursor_busy;aL=HOST.cursor_ok;aM=HOST.disable;aN=HOST.dock_remove;aO=HOST.harm_ok;an=HOST.me;aw=HOST.mobile;ae=HOST.pick_target;af=HOST.refresh_settings;F=HOST.release_cursor;Z=Journal.reader;aP=Kit.ART_CIRCLE;V=Kit.ART_CLOSE;I=Kit.ART_PLAY;B=Kit.GAP;j=Kit.HUE_BAD;J=Kit.HUE_GOOD;k=Kit.HUE_INFO;C=Kit.HUE_TEXT;N=Kit.HUE_TITLE;E=Kit.MARGIN;aQ=Kit.SECTION_TILE;aR=Kit._raw_gump;O=Kit.add_box;l=Kit.add_label;ax=Kit.add_pic;H=Kit.add_section;ao=Kit.add_tiled;ag=Kit.add_window_frame;P=Kit.art_button;aS=Kit.attach;ah=Kit.basics;D=Kit.catcher;ay=Kit.closed;R=Kit.count;aT=Kit.detach;K=Kit.dispose;L=Kit.fit;aU=Kit.frame_show;S=Kit.get_var;aV=Kit.hook_once;q=Kit.is_open;az=Kit.kv_load;aA=Kit.kv_save;aB=Kit.moved_by_code;aC=Kit.note_rect;aD=Kit.on_moved;M=Kit.pic_size;aW=Kit.pin_size;ai=Kit.place;T=Kit.put_var;aX=Kit.row_clicker;aj=Kit.screen;aE=Kit.set;A=Kit.set_text;aF=Kit.spell_info;aa=Kit.text_px;z=Kit.text_w;ak=Kit.ui_pos;aY=Kit.ui_rect;ap=Kit.ui_w;aZ=Kit.was_clicked;aG=Kit.zone_up;a4="hud";a5="Character HUD";e={"anchor":{},"piece":{},"tied":{},"span":{},"inner":{},"bg":{},"bare":{},"stack":{},"dirty":True,"full_at":0.,"sig":None,"objs":None,"inside":[]};a_=.5;aq=42
	def ar(a,below):
		s=e["stack"].get(a)
		if s is None or s[0]!=below:return 0
		return max(0,int(s[1]))
	def a0(a,getter,span=None,inner=None):
		e["dirty"]=True
		if getter is None:
			e["anchor"].pop(a,None);e["span"].pop(a,None);e["inner"].pop(a,None)
			for b,(c,d,f)in list(e["piece"].items()):
				if c==a:au(b)
		else:e["anchor"][a]=getter;e["span"][a],e["inner"][a]=span,inner
	def aH(a,b,order,getter):e["piece"][a]=(b,int(order),getter);e["dirty"]=True
	def aI(a):e["piece"].pop(a,None);e["dirty"]=True;au(a)
	def au(a):
		b=e["tied"].pop(a,None);g=None
		if b is not None:aT(b[0]);g=b[0]
		elif a in e["piece"]:g=e["piece"][a][2]()
		c=e["bare"]
		if g is None or not c or not c.pop(g,False)or not q(g):return
		aU(g,True)
		for d in e["bg"].get(g)or():aE(d,"IsVisible",True)
	def U(b):a=e["anchor"].get(b);g=a()if a is not None else None;return g if q(g)and g.IsVisible else None
	def a1(a):p=e["piece"].get(a);return p is not None and U(p[0])is not None
	Q={"at":0.,"uim":None,"off":False,"same":None}
	def a2(j):
		if Q["off"]:return
		e=time.time()
		if e<Q["at"]:return
		Q["at"]=e+.25
		try:
			if Q["uim"]is None:import System;Q["same"]=System.Object.ReferenceEquals;Q["uim"]=Tz.T("ClassicUO.Game.Managers.UIManager")
			f,g=Q["uim"],Q["same"];k=Tz.get(None,"Gumps",f);c=Kit.mouse_pos()
			for l,h in j:
				if c is not None:
					a=ab(h)
					if a is not None and a[0]<=c[0]<a[0]+a[2]and a[1]<=c[1]<a[1]+a[3]:continue
				d,i=aR(l),aR(h)
				if d is None or i is None:continue
				b=k.First
				while b is not None:
					v=b.Value
					if g(v,d):break
					if g(v,i):Tz.call(None,"MakeTopMostGump",[d],f);break
					b=b.Next
		except Exception:Q["off"]=True
	def ab(g):r=Kit.rect(g);return r if r is not None and r[2]>0 and r[3]>0 else None
	def a6(sw,sh):
		b=[sw,sh];c=[]
		for j,(a,k,l)in e["piece"].items():b.append((j,a,k));c.append(l())
		for a in e["anchor"]:
			d=U(a);r=f=g=None
			if d is not None:r=ab(d);h,i=e["span"].get(a),e["inner"].get(a);f=h()if h is not None else None;g=i()if i is not None else None
			b.append((a,r,f,g));c.append(d)
		return b,c
	def a7():
		w,z=aj();A=time.time();K,p=a6(w,z)
		if not e["dirty"]and A<e["full_at"]and A+2*a_>e["full_at"]and K==e["sig"]:
			C=e["objs"];D=C is not None and len(C)==len(p)
			if D:
				for L in range(len(p)):
					if p[L]is not C[L]:D=False;break
			if D:
				if e["inside"]:a2(e["inside"])
				return
		e["sig"],e["objs"]=K,p;e["dirty"]=False;e["full_at"]=A+a_;M={};k=[];F={}
		for a,(b,N,l)in e["piece"].items():F.setdefault(b,[]).append((N,a,l))
		for b in[at for at in e["stack"]if at not in F]:e["stack"].pop(b,None)
		for b,G in F.items():
			f=U(b)
			if f is None:
				for X,a,_g in G:au(a)
				e["stack"].pop(b,None);continue
			O=ab(f)
			if O is None:e["dirty"]=True;continue
			m,h,r,H=O;s=z<=0 or(h+H/2.)<z/2.;P,Q=e["span"].get(b),e["inner"].get(b);c=P()if P is not None else None;t=Q()if Q is not None and c is not None else None;R=None;G.sort();y=h+H if s else h
			for X,a,l in G:
				g=l()
				if not q(g):au(a);continue
				M[a]=g
				if not g.IsVisible:continue
				S=ab(g)
				if S is None:e["dirty"]=True;continue
				Y,Z,d,T=S;u=None
				if t is not None and R is None and d<r:
					i=E;I,iw,ih,ay,ah=t[:5];v=(c[0]-i)if c[2]else(c[1]-d+i);V=(t[5]if len(t)>5 else ay+ah)+B-i;v=max(I-i,min(v,iw-I-d+i))
					if V+i+aq<=ih-I+2 and v>=0:u,R=(m+v,h+V),1
				if u is not None:x,n=u;k.append((g,f))
				elif c is not None and d<r:x=m+(c[1]-d if c[2]else c[0]);x=max(m,min(x,m+r-d))
				else:x=m+(r-d)//2
				if u is None:
					if w>0:x=max(0,min(x,w-d))
					if s:n,y=y,y+T
					else:y-=T;n=y
				if(Y,Z)!=(x,n):g.SetPos(x,n);aC(g,x,n);aB(g)
				j=e["tied"].get(a)
				if j is None or j[0]is not g or j[1]is not f:
					if j is not None and j[0]is not g:aT(j[0])
					aS(g,f);e["tied"][a]=(g,f)
			e["stack"][b]=(s,(y-(h+H))if s else(h-y))
		J=e["bare"];aa=set(bf for bf,bg in k)
		for W in(J,e["bg"]):
			for g in[bh for bh in W if not q(bh)]:W.pop(g,None)
		for a,(b,N,l)in e["piece"].items():
			g=M.get(a)
			if g is None:g=l()
			if not q(g):continue
			o=g in aa
			if J.get(g,False)!=o:
				J[g]=o
				if o:aW(g)
				aU(g,not o)
				for ac in e["bg"].get(g)or():aE(ac,"IsVisible",not o)
		e["inside"]=k
		if k:a2(k)
	av={"fn":None};a8=("Ready","Done","Out!","Dead","Paused")
	def a3():return max(z(a)for a in a8)
	def al(name,default=0.):
		try:return float(API.GetSkill(name).Value or 0)
		except Exception:return default
	def a9():
		ad="unitframes";aN="Frames";bX="UnitFrames_settings";cT="UnitFrames_pos";cU="UnitFrames_min";bY=("hits","mana","stam");bZ="#17171a";cV={"hits":"#c22d2d","poison":"#2f9a3c","yellow":"#cfae2a","mana":"#2f62cc","stam":"#d39a1c"};b_={"innocent":(46,104,214),"ally":(40,160,70),"gray":(120,120,126),"criminal":(120,120,126),"enemy":(222,118,30),"murderer":(196,38,38),"invulnerable":(214,178,40)};ax=(226,226,230);cW={1:"innocent",2:"ally",3:"gray",4:"criminal",5:"enemy",6:"murderer",7:"invulnerable"};bk=(0,0,8);b0,b1=50000,60000;cX={400:12,402:12,401:13,403:13,605:14,607:14,606:15,608:15,666:666,694:666,667:665,695:665,1253:51253,987:12};cY=(401,403,606,608,667,695);cZ,c_=987,1002;b2=("cloak","shirt","arms","torso","tunic","face","robe","neck","hair","beard","earrings","helmet");c0=("shirt","arms","torso","tunic","face","robe","cloak","neck","hair","beard","earrings","helmet");c1=("shirt","arms","torso","tunic","cloak","face","neck","hair","beard","earrings","helmet","robe");c2=(41674,41675);by=(39301,39302,42002,41675,41674);c3=(5136,5143);b3=110;bl=2.;bz=.008;aQ="vauf_";bm=12;aH,aI,b4=50,150,70;aR=14;b5=10;am=100;b6="UnitFrames_tracked";b7="UnitFrames_framepos";b8=350;b9=(4017,4018,4017);ca=3;c4,c5=240,46;bA=.4;cb=.05;aT=SNAP_DIST;aU=24;aV=2;cc=1.5;c6=10.;c7=.025;c8={"cast":"#cfae2a","done":"#2f9a3c","fail":"#c22d2d"};c9=(("the spell fizzles","fizzled"),("your concentration is disturbed","disturbed"),("insufficient mana","no mana"),("more reagents are needed","no reagents"));da=Kit.SPELL_WORDS;bn=aa;be,a4=502,194;bf=(96.5,96.5);bB=52.5;cd=((86.,(22,22,24)),(81.5,(226,226,230)),(79.5,"tire"),(64.5,(30,25,10)),(61.5,(226,226,230)),(60.5,"gold"),(53.5,(14,10,2)));bo=(78.,83.5);ab=(150.,39.5,491.5,154.5,9.);db=(153.,42.6,488.,151.,6.5);dc=(178.5,47.5,476.5,146.,8.);dd=(183.5,51.5,472.5,141.5,6.);de=((77.5,83.5),(109.5,115.5));df=((483.5,45.8,(188,188,193)),(483.5,148.6,(128,128,133)));dg,dh=(20,20,22),(16,16,18);ce=(182,474);di=((51,79),(83,111),(115,143));cf=.70710678;o={"player":True,"target":True,"hide_empty":False,"numbers":True,"lock":False,"click":True,"party":False,"ignore_self":True,"attack":False,"status":True,"scale":b4,"pdx":0,"pdy":0,"pscale_on":False,"pscale":b4,"pzoom":100,"mirror":False,"sup_open":False,"sup_deep":True,"sup_hide0":False,"sup_follow":True,"sup_low":10,"sup_side":0,"cast":True,"guard":True,"hide_bar":True};cg=dict(o);bp={"scale":(aH,aI),"pscale":(aH,aI),"pdx":(-60,60),"pdy":(-60,60),"pzoom":(50,200),"sup_low":(0,9999),"sup_side":(0,2)}
		def ch():i.update({"shutting":False,"queue":[],"rebuild":False,"docked":False,"target":0,"next_party":0.,"snaps":{},"stale":set(),"snap_queue":[],"art_scales":set(),"snap_px":None,"party":set(),"snap_job":None,"art_jobs":[],"art_failed":set(),"recent":[],"next_prune":0.,"art_dirty":True,"snap_tries":{},"guard":None,"next_guard":0.,"jr":None,"dismissed":set(),"removing":False,"full_at":0.,"mirror_now":False,"pos_save_at":0.})
		i={"minimized":False,"shutting":False,"docked":False,"queue":[],"me":0,"names":{},"pos":{},"next_save":0.,"pos_dirty":False,"crop_changed":0.,"art":None,"textures":set(),"running":False};ch();F=[];a5={"sig":None,"at":None};m={"g":None,"c":{},"spell":None,"start":0.,"secs":1.,"state":None,"until":0.,"pct":0,"word":"","shown":None,"at":None,"leader":None,"s":None,"w":0};t={};bq={"g":None,"c":{},"store":({},{})};a6,ao,U=ah(i,aN);Q={"store":({},{}),"next_preview":0.,"layers":None};ci={};bC,br=S,T
		def cj():az(bX,",",o,bp)
		def bD():aA(bX,",",o,sorted(cg),bp)
		def dj():
			del F[:]
			for a in bC(b6).split(";"):
				p=a.split(",",2)
				if len(p)<3:continue
				try:F.append({"serial":int(p[0]),"auto":p[1]=="1","name":p[2]})
				except ValueError:pass
		def a8():br(b6,";".join("%d,%s,%s"%(a["serial"],"1"if a["auto"]else "0",a["name"].replace(";"," ").replace(","," "))for a in F))
		def dk():
			i["pos"]={}
			for a in bC(b7).split(";"):
				try:k,b=a.split(":");x,y=b.split(",");i["pos"][k]=Kit.adapt(int(x),int(y))
				except ValueError:pass
		def bs():
			bE();b=set("m%d"%c["serial"]for c in F);b.update(("player","target"));a=i["pos"]
			for k in[d for d in a if d not in b]:del a[k]
			br(b7,";".join("%s:%d,%d"%(g,f[0],f[1])for g,f in sorted(a.items())));i["pos_dirty"]=False
		def bt(key,p,at=0):
			if i["pos"].get(key)!=p:
				i["pos"][key]=p;i["pos_dirty"]=True
				if at:i["pos_save_at"]=at
		def bE():
			for a,b in t.items():
				if q(b.get("g")):
					p=a2(b)
					if p is not None and not aM(a):bt(a,p)
		def bF():return int(safe(lambda:API.Player.Serial,0)or 0)
		def dl(n):
			if n is None:return ""
			try:return cW.get(int(n),"")
			except Exception:return str(n).split(".")[-1].lower()
		def ck(serial):return an()if serial==i["me"]else aw(serial)
		bu,dm,dn,do,dp,dq,dr,ds,cl,dt,du,dv=range(12);bg={}
		def cm(serial):
			if not serial:return
			m=ck(serial)
			if m is None:return
			try:
				a=bool(m.IsDead);d=time.time();c=bg.get(serial)
				if c is None or d>=c[5]or a!=c[6]:
					if c is None and len(bg)>=64:bg.clear()
					c=bg[serial]=(str(m.Name or ""),int(m.HitsMax or 0),int(m.ManaMax or 0),int(m.StaminaMax or 0),dl(m.Notoriety),d+.5,a)
				e=(c[0],int(m.Hits or 0),c[1],int(m.Mana or 0)if c[2]else 0,c[2],int(m.Stamina or 0)if c[3]else 0,c[3],c[4],a,bool(m.IsPoisoned),bool(m.IsYellowHits),bool(m.IsParalyzed))
			except Exception:bg.pop(serial,None);return
			b=e[bu]
			if b and i["names"].get(serial)!=b:i["names"][serial]=b
			return e
		al={"get":None,"looked":False,"root":None,"obj":None,"until":0.};cn=2.
		def dw():
			t=W("ClassicUO.Game.World");a=aJ(t,"Instance")if t is not None else None
			if a is None:return
			def b():
				c=a[0]()
				if c is None:al["obj"]=None;return 0
				b=al["obj"];d=time.time()
				if b is None or c is not al["root"]or not 0<al["until"]-d<=cn:
					al["obj"]=None;b=Typing._get(c,"TargetManager")
					if b is None:return 0
					al.update({"root":c,"obj":b,"until":d+cn})
				v=Typing._get(b,"LastAttack")
				if v is None:al["obj"]=None
				return int(v or 0)
			b();return b
		def dz():
			if not al["looked"]:al["looked"]=True;al["get"]=safe(dw)
			return int(safe(al["get"],0)or 0)if al["get"]is not None else 0
		def dA():
			s=(dz()if o["attack"]else 0)or int(API.LastTargetSerial or 0)
			if not s:i["target"]=0;return
			if s==i["target"]:return
			if s==i["me"]:
				if not o["ignore_self"]:i["target"]=s
			elif API.FindMobile(s)is not None:i["target"]=s
		def dB():
			a=set(int(d)for d in(API.GetPartyMemberSerials()or[])if int(d)and int(d)!=i["me"]);i["party"]=a;c=False;b=i["dismissed"]
			if b:
				if o["party"]:b&=a
				else:b.clear()
			if o["party"]:
				for s in a:
					if s in b:continue
					if not any(f["serial"]==s for f in F)and len(F)<bm:F.append({"serial":s,"auto":True,"name":i["names"].get(s)or "Party member"});c=True
			for t in list(F):
				if t["auto"]and(t["serial"]not in a or not o["party"]):F.remove(t);c=True
			if c:a8();bc();af(ad)
		class Bridge(object):
			ok=None;parts=Tex.parts;creatures=False
			@staticmethod
			def find():
				if Bridge.ok is None:
					Bridge.ok=Tex.find()
					if Bridge.ok:Bridge.creatures=bool(safe(Bridge.find_creatures,False))
				return Bridge.ok
			@staticmethod
			def find_creatures():
				import clr;import System;from System.Reflection.Emit import DynamicMethod,OpCodes;p=Bridge.parts;p["uo"]=Tz.get(Tz.get(None,"Game",W("ClassicUO.Client")),"UO");p["anims"]=Typing._get(p["uo"],"Animations");p["hues"]=Typing._get(Typing._get(p["uo"],"FileManager"),"Hues");p["hue_color"]=p["hues"].GetType().GetMethod("GetHueColorRgba8888");d=W("ClassicUO.Game.World");p["world"]=d.GetProperty("Instance").GetValue(None,None);p["get_entity"]=d.GetMethod("Get",System.Array[System.Type]([clr.GetClrType(System.UInt32)]));n=W("ClassicUO.Game.GameObjects.Mobile");p["group_for"]=n.GetMethod("GetGroupForAnimation");p["get_data"]=[s for s in p["tex_t"].GetMethods()if s.Name=="GetData"and s.IsGenericMethodDefinition and len(s.GetParameters())==5][0].MakeGenericMethod(clr.GetClrType(System.UInt32));e=p["anims"].GetType();f=e.GetMethod("GetAnimationFrames");g=W("ClassicUO.Renderer.SpriteInfo");b=f.ReturnType;h,i,j,o=(clr.GetClrType(System.Object),clr.GetClrType(System.UInt16),clr.GetClrType(System.Byte),clr.GetClrType(System.Int32));k=DynamicMethod("vauf_frame",h,System.Array[System.Type]([e,i,j,j,o,clr.GetClrType(System.Array[System.UInt16])]),h.Module,True);a=k.GetILGenerator();c=a.DeclareLocal(b);l=a.DeclareLocal(i);q=a.DeclareLocal(clr.GetClrType(System.Boolean));m=a.DefineLabel()
				for r in(OpCodes.Ldarg_0,OpCodes.Ldarg_1,OpCodes.Ldarg_2,OpCodes.Ldarg_3):a.Emit(r)
				a.Emit(OpCodes.Ldloca_S,l);a.Emit(OpCodes.Ldloca_S,q);a.Emit(OpCodes.Ldc_I4_0);a.Emit(OpCodes.Ldc_I4_0);a.Emit(OpCodes.Callvirt,f);a.Emit(OpCodes.Stloc,c);a.Emit(OpCodes.Ldloca_S,c);a.Emit(OpCodes.Call,b.GetProperty("Length").GetGetMethod());a.Emit(OpCodes.Ldarg_S,System.Byte(4));a.Emit(OpCodes.Ble,m);a.Emit(OpCodes.Ldarg_S,System.Byte(5));a.Emit(OpCodes.Ldc_I4_0);a.Emit(OpCodes.Ldloc,l);a.Emit(OpCodes.Stelem_I2);a.Emit(OpCodes.Ldloca_S,c);a.Emit(OpCodes.Ldarg_S,System.Byte(4));a.Emit(OpCodes.Call,b.GetMethod("get_Item"));a.Emit(OpCodes.Ldobj,g);a.Emit(OpCodes.Box,g);a.Emit(OpCodes.Ret);a.MarkLabel(m);a.Emit(OpCodes.Ldnull);a.Emit(OpCodes.Ret);p["frame"]=k;return all(p[u]is not None for u in("anims","hues","hue_color","world","get_entity","group_for","get_data"))
			@staticmethod
			def creature_pixels(serial):
				import System;p=Bridge.parts;b=p["get_entity"].Invoke(p["world"],System.Array[System.Object]([System.UInt32(serial)]))
				if b is None:return
				j=int(b.GetGraphicForAnimation());k=int(p["group_for"].Invoke(None,System.Array[System.Object]([b,System.UInt16(0),True])));l=int(b.GetDirectionForAnimation())&127;e=System.Array[System.UInt16]([System.UInt16(0)]);c=p["frame"].Invoke(None,System.Array[System.Object]([p["anims"],System.UInt16(j),System.Byte(k),System.Byte(l),0,e]))
				if c is None or c.Texture is None:return
				d=c.UV;w,h=int(d.Width),int(d.Height)
				if w<=0 or h<=0:return
				f=System.Array[System.UInt32](w*h);p["get_data"].Invoke(c.Texture,System.Array[System.Object]([0,d,f,0,w*h]));a=int(b.Hue);g=(a&32768)!=0;a&=32767
				if a==0:a=int(e[0]);g=False
				i=None
				if a:i=[int(p["hue_color"].Invoke(p["hues"],System.Array[System.Object]([System.UInt16(n),System.UInt16(a)])))&0xFFFFFF for n in range(32)]
				return f,w,h,i,g
			@staticmethod
			def on_main(fn):
				a,b=Client.on_main_ex(fn)
				if a=="ok":return b
				if a=="err"and isinstance(Client.exc,Exception):raise Client.exc
				raise Exception(Client.error or "can't reach the game thread")
			@staticmethod
			def gump_pixels(d,hue,e):
				import System
				for f in d:
					c=System.Array[System.Object]([System.UInt32(f),System.UInt16(hue&65535),bool(e),None]);a=Bridge.parts["hued"].Invoke(Bridge.parts["gumps"],c);b=c[3]
					if a is not None and len(a)and int(b.Width)>0:return a,int(b.Width),int(b.Height)
				return
			@staticmethod
			def put_texture(name,w,h,a):Tex.put(name,w,h,a);i["textures"].add(name)
		def bh(ctrl):ctrl.SetAcceptMouseInput(False);return ctrl
		def ap(d,s):v=.5-d*s;return 0. if v<=0 else(1. if v>=1 else v)
		def bv(u,v,box):c,d,e,f,r=box;a=abs(u-(c+e)*.5)-((e-c)*.5-r);b=abs(v-(d+f)*.5)-((f-d)*.5-r);g=a if a>0 else 0.;h=b if b>0 else 0.;i=a if a>b else b;return math.sqrt(g*g+h*h)+(i if i<0 else 0.)-r
		def dC(a,b,x):t=(x-a)/(b-a);t=0. if t<0 else(1. if t>1 else t);return t*t*(3-2*t)
		def co(v):c=132.-62.*min(1.,max(0.,(v-43.)/107.));return(c,c,c+6.)
		def dD(dx,dy,r):b=(dx+dy)/r*cf;f=min(1.,max(0.,(b+.71)/1.42));t=min(1.,max(0.,(r-67.)/11.5));a=44.*(t**1.2)*f;return(128.-a,128.-a,134.-a)
		def dE(dx,dy,r):b=-(dx+dy)/r*cf;t=min(1.,max(0.,(r-56.)/4.));a=t*(-42.+57.*dC(-.3,.75,b));return(min(255.,234.+a),min(255.,203.+a),min(255.,91.+a*.65))
		def aX(b,c,a):
			if a<=0:return
			k=1.-a;b[0]=c[0]*a+b[0]*k;b[1]=c[1]*a+b[1]*k;b[2]=c[2]*a+b[2]*k;b[3]=a+b[3]*k
		def cp(b,a):k=1.-a;b[0]*=k;b[1]*=k;b[2]*=k;b[3]*=k
		def dF(u,v,s):
			a=[0.,0.,0.,0.]
			if 140<=u and 38<=v<=156:
				aX(a,dg,ap(bv(u,v,ab),s))
				if a[3]>0:
					aX(a,co(v),ap(bv(u,v,db),s));aX(a,dh,ap(bv(u,v,dc),s));e=ap(bv(u,v,dd),s)
					if e>0:
						cp(a,e)
						for k,l in de:
							f=min(v-k,l-v)
							if f>-1.5:aX(a,co(v),e*ap(-f,s))
					for g,h,m in df:
						if abs(u-g)<4 and abs(v-h)<4:i=math.sqrt((u-g)**2+(v-h)**2);aX(a,(40,40,44),ap(i-2.6,s));aX(a,m,ap(i-1.6,s))
			c,d=u-bf[0],v-bf[1];r=math.sqrt(c*c+d*d)
			if r<cd[0][0]+2:
				for n,b in cd:
					j=ap(r-n,s)
					if j<=0:continue
					if b=="tire":b=dD(c,d,max(r,.01))
					elif b=="gold":b=dE(c,d,max(r,.01))
					aX(a,b,j)
				cp(a,ap(r-bB,s))
			return a
		def bG(a):
			b=a[3]
			if b<=.002:return 0
			return(int(a[0]+.5)|(int(a[1]+.5)<<8)|(int(a[2]+.5)<<16)|(int(b*255+.5)<<24))
		def dG(s):
			w,h=int(be*s),int(a4*s);b=1./s;a=[0]*(w*h)
			for y in range(h):
				v=(y+.5)*b;d=y*w
				for x in range(w):a[d+x]=bG(dF((x+.5)*b,v,s))
				yield None
			c=[]
			for y in range(h):c.extend(a[y*w:(y+1)*w][::-1])
			yield w,h,a,c
		def cq(s,c):
			f=bo[1]+1;a=int(math.ceil(2*f*s));d=a/2.;e=[0]*(a*a)
			for y in range(a):
				if y%4==3:yield None
				for x in range(a):
					r=math.sqrt((x+.5-d)**2+(y+.5-d)**2)/s;b=min(ap(r-bo[1],s),ap(bo[0]-r,s))
					if b>0:e[y*a+x]=bG([c[0]*b,c[1]*b,c[2]*b,b])
			yield a,e
		def cr(s):a=int(round(s*100));return{"player":"%sframe_player_%d"%(aQ,a),"target":"%sframe_target_%d"%(aQ,a),"blank":"%ssnap_blank_%d"%(aQ,a)}
		def dH(s):
			c=cr(s);a=None
			for a in dG(s):
				if a is None:yield None
			w,h,e,f=a;b=bK(s);g=[bG([bk[0],bk[1],bk[2],1.])]*(b*b)
			for a in cq(s,ax):
				if a is None:yield None
			d,i=a;j=bI(ax,s)
			def k():Bridge.put_texture(c["player"],w,h,e);Bridge.put_texture(c["target"],w,h,f);Bridge.put_texture(c["blank"],b,b,g);Bridge.put_texture(j,d,d,i)
			yield k
		def dI(s):
			if s in i["art_scales"]:return True
			if s in i["art_failed"]:return False
			if not any(a["kind"]=="art"and a["s"]==s for a in i["art_jobs"]):i["art_jobs"]=i["art_jobs"]+[{"kind":"art","s":s,"gen":dH(s)}]
			return
		def bH():
			a=set([o["scale"]/100.])
			if o["pscale_on"]:a.add(o["pscale"]/100.)
			for v in a9.values():
				if v is not None:a.add(v/100.)
			return a
		def dJ():
			c=bH();c.update(f.get("s")for f in t.values()if f.get("art"));a=[g for g in i["art_scales"]if g not in c]
			if not a:return
			d=set(str(int(round(h*100)))for h in a);e=tuple(aQ+p for p in("frame_","noto_","snap_blank_"));b=[r for r in i["textures"]if r.startswith(e)and r.rsplit("_",1)[-1]in d]
			for s in a:i["art_scales"].discard(s)
			for n in b:i["textures"].discard(n)
			if b:safe(lambda:Bridge.on_main(lambda:Tex.drop(b)))
		def bI(a,s):return "%snoto_%d_%d_%d_%d"%(aQ,a[0],a[1],a[2],int(round(s*100)))
		def dK(c,s,name):
			a=None
			for a in cq(s,c):
				if a is None:yield None
			b,d=a;yield lambda:Bridge.put_texture(name,b,b,d)
		def dL(b,s):
			a=bI(b,s)
			if a in i["textures"]:return a
			if a not in i["art_failed"]and not any(d.get("name")==a for d in i["art_jobs"]):c={"kind":"noto","s":s,"name":a,"gen":dK(b,s,a)};i["art_jobs"]=i["art_jobs"]+[c]
			return
		def bJ():return any("out"not in a for a in i["art_jobs"])
		def dM(budget):
			a=time.time()+budget
			for j in i["art_jobs"]:
				while "out"not in j:
					try:r=next(j["gen"])
					except Exception:r=False
					if r is not None:j["out"]=r
					elif time.time()>=a:return True
				if time.time()>=a:break
			return bJ()
		def dN():
			b=i["art_jobs"];c=bH();c.update(g.get("s")for g in t.values());a=[];d=False
			for j in b:
				if j["s"]not in c:continue
				if d or "out"not in j:a.append(j);continue
				r=j["out"];d=True;e=r is not False and bool(safe(lambda:r()or True,False))
				if j["kind"]=="art":(i["art_scales"]if e else i["art_failed"]).add(j["s"]);i["art_dirty"]=True
				elif not e:i["art_failed"].add(j["name"])
				else:
					for f in t.values():f["last"]=None
			if len(a)!=len(b):i["art_jobs"]=a
		def bK(s):return int(math.ceil(2*(bB+2)*s))
		def bL():return bK(max(bH()))
		def dO(graphic,item):
			b=ci.get(graphic)
			if b is None:
				a=item.GetItemData()
				if a is None:return 0,False,False
				b=ci[graphic]=(int(a.AnimID or 0),bool(a.IsPartialHue),bool(a.IsContainer))
			return b
		def dP(layer,worn):
			a=worn.get("robe",(0,0))[0]
			if layer=="tunic":return worn.get("tunic",(0,0))[0]==568 and a and a not in by
			if layer=="arms":return bool(a)and a not in by
			if layer=="torso":
				if a and a not in by:return True
				b=worn.get("tunic",(0,0))[0];return bool(b)and b not in(5441,5442)and worn.get("torso",(0,0))[0]in(30762,30763)
			if layer in("helmet","hair")and a:
				if a>12659:return a in(19357,30742)
				if a<=9863:return a>=9859 or 8270<=a<=8271
				return a in(12217,12659)
			return False
		def cs(serial):
			m=ck(serial)
			if m is None:return
			e=int(m.Graphic or 0);g=cX.get(e)
			if g is None:return{"body":0,"pieces":()}
			k=c_ if e==cZ else int(m.Hue or 0)&16383;l=e in cY;b,h={},{}
			for a in b2:
				f=API.FindLayer(a,serial)
				if f is None:continue
				try:i=int(f.Graphic or 0);b[a]=(i,int(f.Hue or 0)&16383);h[a]=dO(i,f)
				except Exception:b.pop(a,None)
			d=b2
			if "cloak"in b:
				if b.get("robe",(0,0))[0]in c2:d=c1
				elif h["cloak"][2]:d=c0
			if b.get("arms",(0,0))[0]in c3:d=tuple({"arms":"torso","torso":"arms"}.get(r,r)for r in d)
			j=[((g,),k,True)]
			for a in d:
				if a not in b or dP(a,b):continue
				c,n,p=h[a]
				if not c:continue
				if c==970 and e in(694,695):c=547
				o=(c+b1,c+b0)if l else(c+b0,c+b1);j.append((tuple(s for s in o if s<=65535),b[a][1],n))
			return{"body":g,"pieces":tuple(j)}
		def ct(doll):
			def a():
				a=[]
				for c,d,e in doll["pieces"]:
					b=Bridge.gump_pixels(c,d,e)
					if b is not None:a.append(b)
				return a
			return Bridge.on_main(a)or[]
		def dQ(layers):
			a,c,d=None,None,None
			for f,w,h in layers:
				for y in range(h):
					if y%24==23:yield None
					if a is not None and y>a+120:break
					g=y*w;b=-1
					for x in range(w):
						if(f[g+x]>>24)&255>127:b=x;break
					if b<0:continue
					e=b
					for x in range(w-1,b,-1):
						if(f[g+x]>>24)&255>127:e=x;break
					if a is None or y<a:a=y
					c=b if c is None else min(c,b);d=e if d is None else max(d,e)
			yield(c,a,d)
		def dR(body,layers,bounds):
			if not body and layers:w,h=layers[0][1:];a=max(w,h)*1.08*100./o["pzoom"];return(w-a)/2.+o["pdx"],(h-a)/2.+o["pdy"],a
			a=b3*100./o["pzoom"]
			if bounds is None or bounds[1]is None:d,e=98,70;b,c=d-a/2.,e-a/2.
			else:f,g,i=bounds;b=(f+i+1)/2.-a/2.;c=g-2
			return b+o["pdx"],c+o["pdy"],a
		def bM(f,body,out):
			b=[];E=isinstance(f,list)
			for F,(c,w,h)in enumerate(f):
				if isinstance(c,list):b.append((c,w,h))
				else:
					k=(list(c),w,h);b.append(k)
					if E:f[F]=k
				yield None
			l=None
			if body and b:
				for r in dQ(b):
					if r is None:yield None
					else:l=r
			m,n,o=dR(body,b,l);a=int(math.ceil(o))+1;q,s=int(math.floor(m)),int(math.floor(n));G=bk;t=[G]*(a*a)
			for c,w,h in b:
				for y in range(a):
					if y%16==15:yield None
					g=s+y
					if g<0 or g>=h:continue
					H=g*w;I=y*a
					for x in range(a):
						u=q+x
						if 0<=u<w:
							p=c[H+u]
							if(p>>24)&255>127:t[I+x]=(p&255,(p>>8)&255,(p>>16)&255)
			v=o/float(out);z=(.25,.75);A=[0]*(out*out)
			for i in range(out):
				if i%8==7:yield None
				for B in range(out):
					r=C=D=0
					for J in z:
						d=int(n+(i+J)*v)-s;d=0 if d<0 else(a-1 if d>=a else d)
						for K in z:e=int(m+(B+K)*v)-q;e=0 if e<0 else(a-1 if e>=a else e);j=t[d*a+e];r+=j[0];C+=j[1];D+=j[2]
					A[i*out+B]=((r>>2)|((C>>2)<<8)|((D>>2)<<16)|(255<<24))
			yield A
		def cu(serial):
			if serial and(serial not in i["snaps"]or serial in i["stale"])and not any(b[0]==serial for b in i["snap_queue"]):
				a=i["snap_job"]
				if a is not None and a.get("serial")==serial:return
				i["snap_queue"].append((serial,0.))
		def dS(got,job):
			e,w,h,c,f=got;b=list(e);yield None
			if c:
				for i,a in enumerate(b):
					if i%4096==4095:yield None
					d=a&0xFF000000
					if not d:continue
					r,g,j=a&255,(a>>8)&255,(a>>16)&255
					if f and(r!=g or r!=j):continue
					b[i]=c[r>>3]|d
			job["layers"]=[(b,w,h)]
			for r in bM(job["layers"],0,job["size"]):yield r
		def cv():a=i["snap_job"];return a is not None and "out"not in a
		def dT(now,budget=.008):
			a=i["snap_job"]
			if a is None or "out"in a:return False
			b=now+budget
			while not API.StopRequested:
				try:r=next(a["gen"])
				except StopIteration:a["out"]=False;return False
				except Exception:a["out"]=None;return False
				if r is not None:a["out"]=r;return False
				if time.time()>=b:return True
		def dU(now):
			a=i["snap_job"]
			if a is None or "out"not in a:return
			i["snap_job"]=None;r=a["out"]
			if r is None:
				if not any(f[0]==a["serial"]for f in i["snap_queue"]):i["snap_queue"].append((a["serial"],now+bl))
				return
			if r is False:return
			b,d,c=a["serial"],"%ssnap_%d"%(aQ,a["serial"]),a["size"]
			if c!=bL():
				if not any(g[0]==b for g in i["snap_queue"]):i["snap_queue"].append((b,now))
				return
			if safe(lambda:Bridge.put_texture(d,c,c,r)or True,False):
				i["snaps"][b]={"name":d,"creature":False}
				if b==i["me"]and a3.f is not None:Q["layers"]=(a["layers"],a["body"])
				cx(b)
		def cw(now):
			dU(now)
			if i["snap_job"]is not None:return
			for h,(a,j)in enumerate(i["snap_queue"]):
				if j<=now:del i["snap_queue"][h];break
			else:return
			if a in i["snaps"]and a not in i["stale"]:return
			b=cs(a)
			if b is None:i["snap_queue"].append((a,now+bl));return
			i["stale"].discard(a);c=bL()
			if not b["body"]:
				f=safe(lambda:Bridge.on_main(lambda:Bridge.creature_pixels(a)))if Bridge.creatures else None
				if f is None:
					if Bridge.creatures and i["snap_tries"].get(a,0)<3:i["snap_tries"][a]=i["snap_tries"].get(a,0)+1;i["snap_queue"].append((a,now+bl));return
					i["snaps"][a]={"name":None,"creature":True};cx(a);return
				d={"serial":a,"size":c,"layers":None,"body":0};d["gen"]=dS(f,d);i["snap_job"]=d;return
			e,g=safe(lambda:ct(b),[]),b["body"]
			if not e:i["snap_queue"].append((a,now+bl));return
			i["snap_job"]={"gen":bM(e,g,c),"serial":a,"size":c,"layers":e,"body":g}
		def cx(serial):
			for a,b in t.items():
				if a_(a)==serial:b["last"]=None
		def cy():
			i["stale"]=set(i["snaps"])
			for a in t:cu(a_(a))
		bN=8
		def dV(serial):
			a=i["recent"]
			if not serial or(a and a[-1]==serial):return
			if serial in a:a.remove(serial)
			a.append(serial)
			if len(a)>4*bN:del a[:-bN]
		def dW():
			a=set(a_(h)for h in t);a.update(n["serial"]for n in F);a.update(i["party"]);a.update(i["recent"][-bN:]);a.add(i["me"]);g=set(p.get("snap")for p in t.values());c=i["snaps"];e=[]
			for d in[r for r in c if r not in a]:
				b=c[d].get("name")
				if b and b in g:continue
				del c[d]
				if b:e.append(b);i["textures"].discard(b)
			for f in(i["names"],i["snap_tries"]):
				for d in[u for u in f if u not in a]:del f[d]
			i["stale"]=set(v for v in i["stale"]if v in c);q=i["snap_queue"]
			if any(s[0]not in a for s in q):q[:]=[w for w in q if w[0]in a]
			if e and i["art"]:safe(lambda:Bridge.on_main(lambda:Tex.drop(e)))
		def bO(key):return "target"if key=="target"else "player"
		def a_(key):
			if key=="player":return i["me"]
			if key=="target":return i["target"]
			return int(key[1:])
		a9={"player":None,"target":None};ba={"player":None,"target":None};au=E+2
		def bP(key):
			a=a9.get(key)
			if a is not None:return a/100.
			if o["pscale_on"]and key[:1]=="m"and key[1:].isdigit()and int(key[1:])in i["party"]:return o["pscale"]/100.
			return o["scale"]/100.
		def dX(key):
			def a(w,h,mode):
				b=None;a=None
				if w and h:
					a=(int(w),int(h));e,d=a[0]-2*au,a[1]-2*au;c=int(min(100.*float(e)/be,100.*float(d)/a4))
					if a1(key):c=min(c,int(100.*(d-B-aq)/ab[3]))
					b=max(aH,min(aI,c))
				ba[key]=a
				if b!=a9.get(key):a9[key]=b;i["art_dirty"]=True
			return a
		def cz(s):return max(a4*s,ab[3]*s+B+aq)
		def dY(key):
			def a(h):
				c=int(h)-2*au;a=100.*c/a4;b=a1(key)
				if b:a=min(a,100.*(c-B-aq)/ab[3])
				s=max(aH,min(aI,int(a)))/100.;f=max(be*s,ab[0]*s+(161-2*E)+4)if b else be*s;d=0
				if b:
					e=int(math.ceil(cz(s)))+2*au+1
					if e>int(h):d=e
				return int(math.ceil(f))+2*au,d
			return a
		def a1(key):
			for c,(a,b,d)in e["piece"].items():
				if a==key and b==0:return True
			return False
		def dZ(key,w,h):
			a=ba.get(key)
			if not a:return w,h,0,0,False
			W,H=max(a[0],w+2*au),max(a[1],h+2*au);c=au if bO(key)=="player"else W-au-w;b=h
			if a1(key):b=max(h,int(math.ceil(cz(float(h)/a4))))
			return W,H,c,max(au if b>h else 0,(H-b)//2),True
		def d_(key):
			def a():
				a=t.get(key)
				if not a or not a.get("box"):return
				b,e,w,f=a["box"];s=a["s"];c,d=int(round(ab[0]*s)),int(round(ab[2]*s))
				if bO(key)=="player":return b+c,b+d,True
				return b+w-d,b+w-c,False
			return a
		def d0(key):
			def a():
				a=t.get(key)
				if not a or not a.get("slot")or not a.get("box"):return
				c,b,d,h=a["box"];W,H=a["win"];return au,W,H,b,h,b+int(round(ab[3]*a["s"]))
			return a
		def aK(key):s=bP(key);return s,int(be*s),int(a4*s)
		def cA(b,w,a,x1):return(a,x1)if b=="player"else(w-x1,w-a)
		def d1(key):
			a,w,h=aK(key)
			if key=="player":return 60,420
			if key=="target":return 60+w+20,420
			i=[b["serial"]for b in F].index(int(key[1:]))if key[1:].isdigit()else 0;return 60+(i//4)*(w+10),40+(i%4)*(h+2)
		def bQ(serial,action=None):
			def h(*a):
				if ac():ao(("follow_serial",serial))();return
				if action:ao(action)()
			return h
		def cB(key):
			def a():
				a=t.get(key);g=a and a.get("g")
				if not g:return
				b=ac();c=not b and not o["click"]and i.get("removing")
				if not b and not o["click"]and not c:return
				p=a2(a)
				if p!=a.get("seen")or time.time()<a.get("drag_until",0.):a["seen"]=p;return
				ao(("follow"if b else("remove_click"if c else "click"),key))()
			return a
		def d2(key,g):
			def a(*b):
				a=t.get(key)
				if a is not None and a.get("g")is g and not i["shutting"]:a["g"]=None;ao.add(("closed",key),dup=True)
			return a
		def bb(g,x,y,w,h,a,alpha=1.):return O(g,x,y,w,h,alpha,"#%02x%02x%02x"%a)
		def cC(g,c,rows):
			for b,(d,e,f,h)in zip(bY,rows):
				for v in(("hits","poison","yellow")if b=="hits"else(b,)):a=G.CreateGumpSimpleProgressBar(f-d,h-e,bZ,cV[v],0,100);a.SetPos(d,e);g.Add(bh(a));c["bar_"+v]=a
		def d3(key):
			r=t.get(key,{}).get("g");s,w,p=aK(key);u=bO(key);x,y=i["pos"].get(key)or d1(key)
			if q(r):x,y=r.GetX(),r.GetY()
			if key in t:t[key]["g"]=None
			a=lambda v:int(round(v*s));B=bool(i["art"])and s in i["art_scales"];W,k,d,e,J=dZ(key,w,p);C=not o["lock"]and not HOST.layout_locked(ad+"."+key);g=G.CreateGump(True,C)
			if aM(key):x,y=int(x),int(y);g.SetRect(x,y,W,k);aC(g,x,y,W,k);aW(g)
			else:x,y=ai(g,x,y,W,k)
			c={}
			if J:M=E;ag(g,W,k);H(g,M,M,W-2*M,k-2*M)
			f=d+(a(bf[0])if u=="player"else w-a(bf[0]));h=e+a(bf[1]);O,P=cA(u,w,a(ce[0]),a(ce[1]));j=[(d+O,e+a(at),d+P,e+a(dx))for at,dx in di];b=int(bB*s);F=cr(s)if B else None
			if B:z=bK(s);c["snap"]=Tex.control(g,F["blank"],f-z//2,h-z//2,z,z);cC(g,c,j);Tex.control(g,F[u],d,e,w,p);A=int(math.ceil(2*(bo[1]+1)*s));c["noto"]=Tex.control(g,bI(ax,s),f-A//2,h-A//2,A,A)
			else:
				if not J:ag(g,w,p,corners=False)
				m=2*b;H(g,f-b,h-b,m,m,alpha=.95);n=max(2,int(round(3*s)));c["edge"]=[bb(g,f-b,h-b,m,n,ax),bb(g,f-b,h+b-n,m,n,ax),bb(g,f-b,h-b,n,m,ax),bb(g,f+b-n,h-b,n,m,ax)];H(g,j[0][0]-4,j[0][1]-4,j[0][2]-j[0][0]+8,j[-1][3]-j[0][1]+8,alpha=.9);cC(g,c,[(dy,eL+1,eM,eN-1)for dy,eL,eM,eN in j])
			c["strip"]=bb(g,f-22,h+int(b*.42),44,aR+4,(0,0,0),.65);c["strip"].IsVisible=False
			if key=="player":L="Click: target yourself"if o["click"]else "Your character's frame"
			else:L=("Click: make them your target. Alt+click: auto-follow (again to stop)"if o["click"]else "Alt+click: auto-follow (again to stop)")
			D(g,d,e,w,p,cB(key),None,movable=C);N,Q=cA(u,w,a(ab[0]),a(ab[2]));D(g,d+N,e+a(ab[1]),Q-N,a(ab[3])-a(ab[1]),cB(key),L,movable=C);d5(g,key,d,e)
			for R in("name","hits","mana","stam","status","portrait_text"):c["lbl_"+R]=bh(l(g,"",0,0))
			I=None
			if key=="player":c["guard_bg"]=bb(g,0,0,1,1,(0,0,0),.65);c["guard_bg"].IsVisible=False;c["lbl_guard"]=bh(l(g,"",0,0));I=(d+a(ab[2])-6,e+max(1,a(ab[1])-aR-3))
			t[key]={"g":g,"c":c,"rows":j,"centre":(f,h),"hole":b,"s":s,"art":B,"names":F,"last":None,"seen":(x,y),"noto":None,"variant":None,"snap":None,"code_move":False,"shown":{},"bars":{},"serial":None,"box":(d,e,w,p),"win":(W,k),"slot":ba.get(key),"rides":a1(key)}
			if I is not None:t[key]["guard_at"]=I
			i["art_dirty"]=True;G.AddControlOnDisposed(g,d2(key,g));G.AddGump(g);Kit.no_snap(g);aD(g,d4(key));K(r)
		def d4(key):
			def a():
				a=t.get(key)
				if a is None or not q(a.get("g")):return
				p=a2(a)
				if p is not None and p!=a.get("seen"):
					a["seen"]=p;a["code_move"]=True
					if not aM(key):bt(key,p)
				bs()
			return a
		def d5(g,key,ox,oy):
			if key in("player","target"):return
			a=b9 if M(b9[0])[0]>0 else V;x,y,c=ox+ca,oy+ca,bQ(int(key[1:]),("xclose",key));d="Close this frame. Alt+click: auto-follow (again to stop)"
			if M(a[0])[0]>0:b=G.CreateGumpButton("",C,a[0],a[1],a[2]);b.SetPos(x,y);g.Add(b);Kit.on_click(b,c);b.SetTooltip(d);return
			l(g,"x",x+2,y,N);D(g,x,y,max(14,z("x")+4),16,c,d)
		def bi(key):
			a=t.pop(key,None)
			if a:
				i["art_dirty"]=True;g=a.get("g")
				if q(g):
					p=a2(a)
					if p is not None and not aM(key):bt(key,p)
				a["g"]=None;K(g)
		def d6(w,h,side,p=None):
			d=t.get("player")
			if d is None or not q(d.get("g")):return
			if p is None:p=a2(d)
			if p is None:return
			c,b=p;g,i=d.get("win")or aK("player")[1:];W,H=aj()
			if side==1:
				a=(c-w-2,b)
				if a[0]<0:a=(c+g+2,b)
			elif side==2:
				a=(c+g+2,b)
				if W>0 and a[0]+w>W:a=(c-w-2,b)
			else:
				j,k=cF(b,i);e=b+i+2+j+ar("player",True);a=(c,e)
				if H>0 and e+h>H:
					f=b-h-2-k-ar("player",False)
					if f>=0 or f+h>H-e:a=(c,f)
			x,y=a
			if W>0:x=max(0,min(x,W-w))
			if H>0:y=max(0,min(y,H-h))
			return(x,y)
		bR="UnitFrames_hbar_held";cD=1.;aL={"at":0.,"held":None}
		def d7():
			try:return Tz.get(None,"CurrentProfile",Tz.T("ClassicUO.Configuration.ProfileManager"))
			except Exception:return
		def cE(want):
			a=d7()
			if a is None:return
			if aL["held"]is None:aL["held"]=bC(bR)=="1"
			b=aL["held"]
			if want:
				if not b and not bool(Tz.get(a,"OpenHealthBarForLastAttack")):return
				if not b:Tz.put(a,"OpenHealthBarForLastAttack",False);br(bR,"1");aL["held"]=True
				try:
					t=Tz.T("ClassicUO.Game.UI.Gumps.BaseHealthBarGump");c=Tz.get(None,"LastAttackBar",t)
					if c is not None and not c.IsDisposed:c.Dispose()
				except Exception:pass
			elif b:Tz.put(a,"OpenHealthBarForLastAttack",True);br(bR,"");aL["held"]=False
		def d8(now):
			if 0<=aL["at"]-now<=cD:return
			aL["at"]=now+cD
			try:cE(bool(o["hide_bar"]and o["target"]))
			except Exception:pass
		def d9(w,h,side):
			a=t.get("player")
			if a is None or not q(a.get("g")):return
			p=a.get("seen");b=None
			if p is not None:b=(p,a.get("win")or aK("player")[1:],side,o["cast"],e["stack"].get("player"),aj(),w,h)
			if b is None or b!=a5["sig"]or a5["at"]is None:a5["at"]=d6(w,h,side,p);a5["sig"]=b if a5["at"]is not None else None
			c=a5["at"];return None if c is None else(a["g"],c)
		def cF(fy,fh):
			if not o["cast"]:return 0,0
			H=aj()[1]
			if H>0 and fy+fh+aV+aU>H:return 0,aU+aV
			return aU+aV,0
		def cG(fr):
			p=fr.get("seen")
			if p is None:return
			g,d,h,c=fr.get("box")or(0,0,0,aK("player")[2]);b=p[1]+d;e,i=cF(b,c);x=p[0]+fr["rows"][0][0]-6;f=(fr.get("win")or aK("player")[1:])[1]
			if e:
				a=ar("player",True);y=b+c+aV
				if a:y=max(y,p[1]+f+a+aV)
				return x,y
			a=ar("player",False);y=b-aU-aV
			if a:y=min(y,p[1]-a-aU-aV)
			return x,y
		def bS():g,m["g"]=m["g"],None;m["leader"]=None;m["shown"]=None;K(g)
		def ea(fr):
			bS();d=fr["rows"];w,h=d[0][2]-d[0][0]+12,aU;g=G.CreateGump(False,False);ag(g,w,h,corners=False,mouse=False);c={}
			for k in("cast","done","fail"):a=G.CreateGumpSimpleProgressBar(w-12,h-10,bZ,c8[k],0,100);a.SetPos(6,5);g.Add(bh(a));c[k]=a
			c["lbl"]=bh(l(g,"",6,4));b=cG(fr)or(0,0);ai(g,b[0],b[1],w,h);G.AddGump(g);g.IsVisible=False;aS(g,fr["g"]);m.update({"g":g,"c":c,"shown":None,"at":b,"leader":fr["g"],"s":fr["s"],"w":w})
		def cH(now):
			a=t.get("player")
			if not o["cast"]or a is None or not q(a.get("g")):
				m["state"]=None;i["jr"]=None
				if m["g"]is not None:bS()
				return
			c=None
			if i["jr"]is None:i["jr"]=Z()
			else:c=i["jr"].new()
			if c:
				g=i["names"].get(i["me"])or ""
				for b in c:
					d=b.name or ""
					if g and d==g:
						e=da.get(b.low.strip())
						if e is not None:f=aF(e[0]);l=f[3]if f and f[3]else 1.;m.update({"spell":e[0],"start":min(now,b.at or now),"secs":max(.1,float(l)),"state":"cast","pct":0,"word":""});continue
					elif d and d!="System":continue
					if m["spell"]is None or now-m["start"]>m["secs"]+c6:continue
					n=b.low
					for p,r in c9:
						if n.startswith(p):
							if m["state"]!="cast":m["pct"]=100
							m.update({"state":"fail","word":r,"until":now+cc});break
			h=m["state"]
			if h=="cast":
				j=now-m["start"]
				if j>=m["secs"]:m.update({"state":"done","until":now+cc,"pct":100})
				else:m["pct"]=max(0,int(100*j/m["secs"]))
			elif h is not None and now>=m["until"]:m["state"]=None
			k=a["last"][5]if a.get("last")else None
			if k is not None and k[cl]:m["state"]=None
			eb(a)
		def eb(fr):
			b=m["state"];g=m["g"]
			if b is None:
				if g is not None and m["shown"]is not None:m["shown"]=None;aE(g,"IsVisible",False)
				return
			if g is None or not q(g)or m["s"]!=fr["s"]or m["leader"]is not fr["g"]:ea(fr);g=m["g"]
			c=cG(fr)
			if c is not None and c!=m["at"]:m["at"]=c;g.SetRect(c[0],c[1],m["w"],aU);aB(g)
			f=m["spell"]if b!="fail"else "%s: %s"%(m["spell"],m["word"]);d=(b,m["pct"],f);a=m["shown"]
			if d==a:return
			m["shown"]=d;e=m["c"]
			if a is None or a[0]!=b:
				for k in("cast","done","fail"):e[k].IsVisible=k==b
			if a is None or a[0]!=b or a[1]!=d[1]:e[b].SetProgress(float(d[1]),100.)
			if a is None or a[2]!=f:h=L(f,m["w"]-16);A(e["lbl"],h,C);e["lbl"].SetPos(max(6,(m["w"]-bn(h))//2),4)
			if a is None:g.IsVisible=True
		def ec(now):
			if not o["guard"]:i["guard"]=False
			elif now>=i["next_guard"]:i["next_guard"]=now+.5;i["guard"]=HOST.guarded()
			a=t.get("player")
			if a is None or "guard_at"not in a or not q(a.get("g")):return
			d=i["guard"]
			if d is None:b,c="?",k
			elif d:b,c="GUARDED",J
			else:b,c="",C
			e,y=a["guard_at"];bj(a,"guard",b,e,y,c,"right")
			if a["shown"].get("guard_bg")!=b:
				a["shown"]["guard_bg"]=b;f=a["c"]["guard_bg"]
				if b:g=z(b)+8;aY(f,e-g+4,y-1,g,aR+4)
				f.IsVisible=bool(b)
		def bj(fr,name,text,x,y,hue,align="left"):
			if align=="right":x-=bn(text)if text else 0
			elif align=="center":x-=(bn(text)if text else 0)//2
			a=(text,hue,int(x),int(y));c=fr["shown"];b=c.get(name)
			if b==a:return
			c[name]=a;d=fr["c"]["lbl_"+name];A(d,text,hue)
			if b is None or b[2]!=a[2]or b[3]!=a[3]:ak(d,a[2],a[3])
		def bT(fr,variant,cur,mx):
			a=(float(max(0,cur)),float(max(1,mx)))
			if fr["bars"].get(variant)==a:return
			b=fr["c"].get("bar_"+variant)
			if b is not None:b.SetProgress(a[0],a[1]);fr["bars"][variant]=a
		def ed(fr,want):
			if fr["variant"]==want:return
			fr["variant"]=want
			for v in("hits","poison","yellow"):
				a=fr["c"].get("bar_"+v)
				if a is not None:
					a.IsVisible=v==want
					if v!=want:a.SetProgress(0.,1.);fr["bars"][v]=(0.,1.)
		def ee(fr,a):
			if fr["noto"]==a:return
			c=fr["c"]
			if fr["art"]:
				b=dL(a,fr["s"])
				if b is None:return
				c["noto"].TextureName=b
			else:
				for d in c["edge"]:d.SetBaseColor(a[0],a[1],a[2],255)
			fr["noto"]=a
		def ef(fr,serial):
			if not fr["art"]:return{}
			a=not serial
			if fr["shown"].get("snap_hidden")!=a:fr["shown"]["snap_hidden"]=a;fr["c"]["snap"].IsVisible=not a
			if a:return{}
			cu(serial);c=i["snaps"].get(serial)or{};b=c.get("name")or fr["names"]["blank"]
			if fr["snap"]!=b:fr["snap"]=b;fr["c"]["snap"].TextureName=b
			return c
		def eg(cur,mx):return int(round(100.*cur/mx))if mx>0 else 0
		def eh(key):
			a=t.get(key)
			if a is None or not q(a.get("g")):return
			c=a_(key)
			if c!=a["serial"]:a["serial"]=c;dV(c)
			d=cm(c);P=c==i["me"];A=key!="target"and c and c==i["target"];B=ef(a,c);D=a["c"];E=(c,A,o["numbers"],a["snap"],bool(B.get("creature")),d)
			if E==a["last"]:return
			a["last"]=E;F=N if A else C;e,n="",""
			if not c or d is None:
				G,F,f,p=ax,k,((0,1),)*3,"hits"
				if not c:g,b="",("","","");n="No target"
				else:g,b=i["names"].get(c)or "Unknown",("Out of range","","")
			else:
				r=d[cl];g=d[bu]or i["names"].get(c)or "Unknown";p="poison"if d[dt]else("yellow"if d[du]else "hits");f=((d[dm],d[dn]),(d[do],d[dp]),(d[dq],d[dr]));G=ax if r else b_.get(d[ds],b_["gray"]);e="DEAD"if r else("PARA"if d[dv]else "")
				if B.get("creature"):n="No picture"
				b=[]
				for h,(H,s)in enumerate(f):
					if s<=0:b.append(""if h else "--")
					elif P or h:b.append("%d/%d"%(H,s))
					else:b.append("%d%%"%eg(H,s))
				if r:b[0]="Dead"
				b=tuple(b)
			if not o["numbers"]and b and b[0]!="Out of range":b=("","","")
			ed(a,p);bT(a,p,f[0][0],f[0][1]);bT(a,"mana",f[1][0],f[1][1]);bT(a,"stam",f[2][0],f[2][1]);ee(a,G);I=a["rows"]
			for h,Q in enumerate(bY):u,l,v,w=I[h];bj(a,Q,b[h],v-8,l+(w-l-aR)//2-1,C,"right")
			u,l,v,w=I[0];x=max(20,v-u-16-(bn(b[0])+10 if b[0]else 0));m=a["shown"].get("fit")
			if m is None or m[0]!=g or m[1]!=x:m=a["shown"]["fit"]=(g,x,L(g,x))
			bj(a,"name",m[2],u+8,l+(w-l-aR)//2-1,F);y,J=a["centre"];K=a["hole"];M=J+int(K*.42);bj(a,"status",e,y,M+2,j if e=="DEAD"else N,"center")
			if a["shown"].get("strip")!=e:
				a["shown"]["strip"]=e
				if e:O=z(e)+10;aY(D["strip"],y-O//2,M,O,aR+4)
				D["strip"].IsVisible=bool(e)
			bj(a,"portrait_text",L(n,2*K-6)if n else "",y,J-aR//2-1,k,"center")
		def ei():
			a=[]
			if o["player"]:a.append("player")
			if o["target"]and(i["target"]or not o["hide_empty"]):a.append("target")
			a.extend("m%d"%b["serial"]for b in F);return a
		def ej():
			c=ei()
			for a in list(t):
				if a not in c:bi(a)
			for a in c:
				b=t.get(a)
				if(b is None or not q(b.get("g"))or b.get("s")!=bP(a)or b.get("slot")!=ba.get(a)or(b.get("slot")and b.get("rides")!=a1(a)))and(not i["art"]or dI(bP(a))is not None):d3(a)
				eh(a)
		def cI(key):
			def a():a=t.get(key);return a.get("g")if a else None
			return a
		def aM(key):return aG(ad+"."+key)
		def a2(fr):r=Kit.rect(fr.get("g"));return None if r is None else(r[0],r[1])
		def ek(now):
			for b,a in t.items():
				if not q(a.get("g")):continue
				p=a2(a)
				if p is None:continue
				if p!=a.get("seen"):
					a["seen"]=p
					if a.get("code_move"):a["code_move"]=False
					else:
						a["drag_until"]=now+bA
						if not aM(b):a["moved"]=a["dropped"]=True
					if not aM(b):bt(b,p,now+bA)
				else:
					a["code_move"]=False
					if a.get("dropped")and now>=a.get("drag_until",0.)and SNAP.pressed()is not True:a["dropped"]=False;el(b)
			if i["pos_dirty"]and now>=i["pos_save_at"]:bs()
		def cJ(key):
			a=t.get(key)
			if a is None or not q(a.get("g")):return
			p=a.get("seen")or a2(a)
			if p is None:return
			w,h=a.get("win")or aK(key)[1:];return p[0],p[1],w,h
		def el(key):
			r=cJ(key)
			if r is None:return
			x,y,w,h=r;f=None;g=i=None
			for n in t:
				if n==key:continue
				o=cJ(n)
				if o is None:continue
				a,b,c,e=o
				for j,k in((a+c,b),(a+c,b+e-h),(a-w,b),(a-w,b+e-h),(a,b+e),(a+c-w,b+e),(a,b-h),(a+c-w,b-h)):
					d=max(abs(x-j),abs(y-k))
					if d<=aT and(f is None or d<f[0]):f=(d,j,k)
				if y<b+e+aT and b<y+h+aT:
					for j in(a+c,a-w,a,a+c-w):
						d=abs(x-j)
						if d<=aT and(g is None or d<g[0]):g=(d,j)
				if x<a+c+aT and a<x+w+aT:
					for k in(b+e,b-h,b,b+e-h):
						d=abs(y-k)
						if d<=aT and(i is None or d<i[0]):i=(d,k)
			if f is not None:l,m=f[1],f[2]
			else:l=g[1]if g else x;m=i[1]if i else y
			if(l,m)!=(x,y):bU(key,l,m);t[key]["moved"]=True
		def bU(key,x,y):
			a=t.get(key)
			if a is None or not q(a.get("g")):return
			w,h=a.get("win")or aK(key)[1:];g=a["g"];x,y=Kit.clamp(x,y,w,h);g.SetRect(int(x),int(y),w,h);aC(g,int(x),int(y),w,h);aB(g);a.update({"seen":(int(x),int(y)),"code_move":True,"moved":False});i["pos"][key]=a["seen"];i.update({"pos_dirty":True,"pos_save_at":time.time()+bA})
		def em(force=False):
			p,b=t.get("player"),t.get("target")
			if(p is None or b is None or not q(p.get("g"))or not q(b.get("g"))):return
			e,g=aj();i,w,j=aK("player");c,d=p.get("seen"),b.get("seen")
			if aM("player")or aM("target")or e<=0 or g<=0 or c is None or d is None:return
			f=bool(p.get("moved"));h=bool(b.get("moved"))
			if h and not f and not force:
				a=(e-d[0]-w,d[1])
				if a!=c:bU("player",*a)
			elif f or force:
				a=(e-c[0]-w,c[1])
				if a!=d:bU("target",*a)
		def en(key):
			a=a_(key)
			if not a:return
			if API.HasTarget()and Y(ad)in(None,"pick"):
				if aO(a,"hud.frame",aN):API.Target(a)
			else:
				API.SetLastTarget(serial=a)
				if key!="target"and a!=i["me"]:i["target"]=a
		def bw(serial,auto=False):
			if not serial:U("target someone first, then click Add frame.",j);return
			i["dismissed"].discard(serial)
			if serial==i["me"]:U("that's you; your own frame is the player frame.");return
			for t in F:
				if t["serial"]==serial:t["auto"]=False;U("%s already has a frame."%t["name"]);a8();return
			if len(F)>=bm:U("%d frames is the limit."%bm,j);return
			d=cm(serial)
			if d is None:U("that isn't a mobile you can see.",j);return
			F.append({"serial":serial,"auto":auto,"name":d[bu]or "Unknown"});a8();U("added %s."%(d[bu]or "a frame"),J);bc();af(ad)
		def bV(serial):
			for t in F:
				if t["serial"]==serial and t["auto"]:i["dismissed"].add(serial)
			F[:]=[a for a in F if a["serial"]!=serial];bi("m%d"%serial);a8();bc();af(ad)
		def cK(serial):return any(a["serial"]==serial for a in F)
		def cL(kind):
			def a(serial):ao.add((kind,int(serial or 0)),dup=True)
			return a
		eo=("Frame your target, or pick someone with a target cursor. Alt+click a frame: auto-follow (again to stop)");ep="Click a person or their frame with a target cursor to remove it (each frame has an X too)";cM=40
		def bc():
			if i["shutting"]:return
			M=E;g,b,c=bd.begin(b8,M+30+B+cM+M)
			if not i["minimized"]:bd.frame(g);a=M+30+B;H(g,M,a,b8-2*M,cM);P(g,b,"add",aP,M+12,a+12,"Add frame",eo,on_click=ao("add_frame"));P(g,b,"remove",aP,M+56+z("Add frame"),a+12,"Remove frame",ep,on_click=ao("remove_frame"))
			bd.end(g);eq()
		bd=Kit.Window(ad,aN,i,bq,bc,cT,cU,mini=(c4,c5),icon=7028,cleanup=a6,lock=True)
		def eq():
			c=bq["c"]
			if "status"in c:A(c["status"],"%s: %s"%(aN,R(len(F),"frame")))
		cN={"rm":bV,"click":en,"add_ext":bw,"follow_serial":lambda serial:X(serial,aN)};cO=(("player","Show your own frame","Your HP, mana and stamina"),("target","Show the target frame","Your current target"),("hide_empty","Hide the target frame with no target","Shown only while you have a target"),("numbers","Show numbers on the bars","HP, mana and stamina as numbers (others' HP as a %)"),("lock","Lock the frames in place","Frames can't be dragged"),("cast","Show a cast bar under your frame","Your spell filling through its cast delay: green when cast, red when it fails"));er=(("hide_bar","Hide TazUO's own target health bar","Avoids two target bars; untick to get your client's setting back"),("click","Click a frame to target it","Aims a target cursor if one is up, else sets your last target"),("party","Add a frame for each party member","While they are in your party"),("ignore_self","Ignore yourself as last target","Targeting yourself (a bandage, a heal) keeps your target frame"),("attack","Prefer the attack target","Frame who you attack, else your last target"),("mirror","Mirror the player and target frames","Drag either frame and the other mirrors it across the screen"),("guard","Show a GUARDED tag on your frame","GUARDED in guard zones, ? until known (enter or leave one), blank outside"));cP=aQ+"snap_preview";es="Frame size, percent of the art (%d-%d%%)"%(aH,aI);et="Party members' frame size while ticked (%d-%d%%)"%(aH,aI);bx=(("pdx","Left / right","Move pictures left or right in the circle","%+d"),("pdy","Up / down","Move pictures up or down in the circle","%+d"),("pzoom","Zoom","Zoom pictures in or out (100%% = %d art pixels tall)"%b3,"%d%%"))
		def eu(w):
			a=max(z("All frames:"),24+z("Party members:"))
			def b(f,x,y):b=x+26+a;f.c["pscale"]=Kit.with_tip(Kit.add_slider(f.g,b,y+4,260,aH,aI,o["pscale"]),et);f.c["pscale_lbl"]=l(f.g,"%d%%"%o["pscale"],b+272,y+2,k)
			c={"top":32,"sh":30+am+4+10,"dx":12+am+4+16,"ldy":0,"fh":26,"sw":180,"ugap":12,"lgap":12,"lw":max(z(d[1])for d in bx),"bdy":0,"bgap":18};return(("OTHERS' FRAMES  (%d of %d)"%(len(F),bm),(("custom",0,ev),),{"top":0,"sh":30+28+4+max(1,len(F))*24+6}),("OPTIONS",[("check",)+g for g in cO]+[("gap",-26*len(cO))]+[("check",)+h+({"dx":12+w//2},)for h in er],{"pad":6}),("FRAME SIZE",(("slider","scale","All frames:",es,aH,aI,{"lw":a,"lgap":14,"ldy":2,"sdy":4,"sw":260,"ugap":12,"vfmt":"%d%%"}),("check","pscale_on","Party members:","Party members' frames use the slider beside this; unticked, the size above",{"stay":True}),("custom",0,b)),{"top":34,"sh":96}),("PICTURE  (in each frame's circle)",[("custom",0,ew)]+[("slider",n,p+":",r,bp[n][0],bp[n][1],{"vfmt":s})for n,p,r,s in bx]+[("buttons",(("retake",I,"Retake pictures","Take every picture again (after a gear change)"),("reset",V,"Reset","Put the picture sliders back to defaults")))],c))
		def ev(f,x,y):
			g,w,a=f.g,f.w,f.store;d=x+12;P(g,a,"add",I,d,y+28,"Add target","Frame your current target",on_click=ao("add_target"));P(g,a,"pick",I,d+49+z("Add target"),y+28,"Pick...","Pick someone to frame",on_click=ao("pick"));P(g,a,"clear",V,x+w-47-z("Clear all"),y+28,"Clear all","Remove everyone else's frame",on_click=ao("clear"));e=y+30+28+4;h=M(V[0])[0]or 30
			if not F:l(g,"No frames yet. Target someone, then click Add target.",x+12,e+3,k)
			for i,t in enumerate(F):
				b=e+i*24;c="(party)"if t["auto"]else "";j=w-24-h-6-(z(c)+8 if c else 0);m=L(t["name"],j);l(g,m,x+12,b+3);D(g,x+12,b,j+8,20,bQ(t["serial"]),"Alt+click: auto-follow (again to stop)")
				if c:l(g,c,x+12+z(m)+8,b+3,k)
				P(g,a,"rm%d"%i,V,x+w-12-h,b,None,"Remove %s's frame. Alt+click: auto-follow (again to stop)"%t["name"],on_click=bQ(t["serial"],("rm",t["serial"])))
		def ew(f,x,y):
			g=f.g;H(g,x+12,y-2,am+4,am+4,alpha=1.)
			if i["art"]and i.get("running"):bW();Tex.control(g,cP,x+14,y,am,am)
			else:
				a=("Pictures","unavailable")if i.get("running")else("Turn Frames","on for a","preview");c=y+(am-len(a)*18)//2
				for d,b in enumerate(a):l(g,b,x+14+(am-z(b))//2,c+d*18,k)
		def cQ():
			a=time.time();i["crop_changed"]=a
			if i["art"]and i.get("running")and a>=Q["next_preview"]:Q["next_preview"]=a+.3;bW()
		def ex(f):
			if aZ(f.store,"retake"):Q["layers"]=None;i["crop_changed"]=1.
			if aZ(f.store,"reset"):
				for k,a,b,c in bx:f.c[k].SetValue(cg[k])
				cQ()
		def ey(f,new):
			try:new["pscale"]=max(aH,min(aI,int(f.c["pscale"].Value)))
			except Exception:return
			A(f.c["pscale_lbl"],"%d%%"%new["pscale"])
		def ez(a,new):
			if(new["lock"],new["click"])!=(a["lock"],a["click"]):i["rebuild"]=True
			if new["party"]!=a["party"]:i["next_party"]=0.
			if new["mirror"]and not a["mirror"]:i["mirror_now"]=True
			i["art_dirty"]=True
			for k,b,c,d in bx:
				if new[k]!=a[k]:cQ();break
		a3=Kit.Page(o,eu,bD,ez,adjust=ey,clicks=ex)
		def eA(g,x,y,w):Q["store"]=a3.build(g,x,y,w).store
		def eB():a3.closed();Q.update({"layers":None,"preview_gen":None})
		def bW():
			if i.get("running")and i["art"]:Q["preview_want"]=True
		def eC():
			a=cs(i["me"]or bF())
			if not a or not a["body"]:return
			b=safe(lambda:ct(a),[]);return(b,a["body"])if b else None
		def eD():
			a=Q.get("layers")
			if a is None:
				a=safe(lambda:Kit.on_client(eC))
				if not a:return
				Q["layers"]=a
			Q["preview_gen"]=bM(a[0],a[1],am)
		def eE(budget):
			b=time.time()+budget
			while Q.get("preview_gen")is not None:
				a=Q["preview_gen"]
				try:r=next(a)
				except Exception:
					if Q.get("preview_gen")is a:Q["preview_gen"]=None
					return
				if r is not None:
					if Q.get("preview_gen")is a:Q["preview_gen"]=None
					safe(lambda:Bridge.on_main(lambda:Bridge.put_texture(cP,am,am,r)));return
				if time.time()>=b:return
		def eF(now):
			t=i["crop_changed"]
			if not t or now-t<.5:return
			i["crop_changed"]=0.
			if i["art"]:
				if a3.f is not None:bW()
				cy()
		cj()
		def eG():
			ch();i.update({"me":bF(),"running":True});m.update({"spell":None,"state":None,"shown":None});Q.update({"preview_want":False,"preview_gen":None});cj();dj();dk();a6.service("frames.player_anchor",d9);i["minimized"]=bd.start_min();i["art"]=Bridge.find()
			if not i["art"]:U("no drawn pictures on this client; using stone frames.")
			bc();bd.dock();a6.service("unitframes.add",lambda serial:ao(("add_ext",int(serial)))());a9["player"]=a9["target"]=None;ba["player"]=ba["target"]=None
			for a in("player","target"):HOST.layout_add(ad+"."+a,cI(a),aN+" ("+a+")",{"fit":dX(a),"fill":"frame","exact":True,"pieces_out":True,"hug":dY(a),"untitled":True});a0(a,cI(a),d_(a),d0(a));a6.add(HOST.layout_remove,ad+"."+a);a6.add(a0,a,None)
			av["fn"]=lambda:i["target"]
		def cR():return i["target"]or int(API.LastTargetSerial or 0)
		def eH():
			if bq["g"]is None:return
			if ay(bq):return
			a=time.time()
			if a<i["full_at"]and not i["queue"]and not i["rebuild"]and a+1.>i["full_at"]:
				if i["art"]:cw(a)
				if m["state"]=="cast":cH(a)
				return
			i["full_at"]=a+cb-.005;i["me"]=i["me"]or bF();dA()
			while i["queue"]:
				c=i["queue"].pop(0);b=c[0]if isinstance(c,tuple)else c
				if bd.action(c):continue
				if b=="add_frame":
					d=cR()
					if d and d!=i["me"]and not cK(d):bw(d);continue
					b="busy"if Y(ad)else "pick"
				elif b=="remove_frame":
					if not F:U("nobody else has a frame (turn off your own and the target frame in settings).")
					elif Y(ad):b="busy"
					else:U("click the person, or their frame, to remove.");i["removing"]=True;ae(b5,cL("unpicked"))
				if b=="busy":U("a target cursor is up; try again after it.")
				elif b=="pick":U("choose who gets a frame.");ae(b5,cL("picked"))
				elif b=="add_target":bw(cR())
				elif b=="picked":
					if c[1]:bw(c[1])
					else:U("pick cancelled.")
				elif b=="remove_click":
					d=a_(c[1])
					if d and i.get("removing")and API.HasTarget():API.Target(d)
				elif b=="unpicked":
					i["removing"]=False
					if not c[1]:U("remove cancelled.")
					elif cK(c[1]):h=next((n["name"]for n in F if n["serial"]==c[1]),"");bV(c[1]);U("removed %s."%(h or "the frame"))
					else:U("they have no frame of their own.")
				elif b=="clear":
					for j in F:bi("m%d"%j["serial"])
					del F[:];a8();af(ad)
					if o["party"]:U("cleared; party members come back while 'Add a frame for each party member' is ticked.")
					bc()
				elif b=="follow":
					d=a_(c[1])
					if d:X(d,aN)
				elif b in("closed","xclose"):
					e=c[1]
					if b=="xclose":bi(e)
					t.pop(e,None)
					if e in("player","target"):o[e]=False;bD();af(ad);U("%s frame hidden; tick it again in settings."%e)
					elif e[1:].isdigit():bV(int(e[1:]))
				elif b in cN:cN[b](c[1])
			if i["rebuild"]:
				i["rebuild"]=False;bE()
				for e in list(t):bi(e)
			if i["art"]:
				f=bL()
				if i["snap_px"]!=f:
					i["snap_px"]=f
					if i["snaps"]:cy()
			a=time.time()
			if a>=i["next_party"]:i["next_party"]=a+1.;dB()
			if i["art_jobs"]:dN()
			ej()
			if i["art"]and i["art_dirty"]:i["art_dirty"]=False;dJ()
			if a>=i["next_prune"]:i["next_prune"]=a+5.;dW()
			for k in t.values():k["moved"]=False
			ek(a);g=(a1("player"),a1("target"))
			if g!=i.get("rides"):i["rides"]=g;HOST.layout_refit()
			a7()
			if o["mirror"]:em(force=i.pop("mirror_now",False))
			cH(a);d8(a);ec(a)
			if i["art"]:cw(a)
			eF(a)
			if a>=i["next_save"]:
				i["next_save"]=a+10.;bE()
				if i["pos_dirty"]:bs()
		def eI():
			if i["shutting"]:return
			if bJ():dM(bz)
			if cv():dT(time.time(),bz)
			if Q.get("preview_want"):
				Q["preview_want"]=False
				if a3.f is not None:eD()
			if Q.get("preview_gen")is not None:eE(bz)
		def cS():return bool(cv()or bJ()or Q.get("preview_want")or Q.get("preview_gen")is not None)
		def eJ():
			if m["state"]=="cast":return c7
			return.03 if i["art_jobs"]or i["snap_job"]is not None or cS()else cb
		def eK():
			i.update({"shutting":True,"running":False,"removing":False,"snap_job":None,"art_jobs":[]});Q.update({"preview_want":False,"preview_gen":None});av["fn"]=None;bs();bD();a8();safe(lambda:cE(False));aL["held"]=None
			for b in list(t):a=t.pop(b);g,a["g"]=a.get("g"),None;K(g)
			bS();i["jr"]=None
			if i["art"]and i["textures"]:c=list(i["textures"]);safe(lambda:Bridge.on_main(lambda:Tex.drop(c)));i["textures"].clear();i["art_scales"]=set()
			i["art"]=None;a6.close()
		return{"start":eG,"tick":eH,"stop":eK,"client_tick":True,"config_height":a3.height,"build_config":eA,"poll_config":a3.poll,"config_closed":eB,"thread_tick":eI,"interval":eJ,"thread_wanted":cS}
	def ba():
		I="spelltimers";J="Buffs & Timers";aM="SpellTimers_settings";bu="SpellTimers_pos";bv="SpellTimers_min";aO="SpellTimers_active";bw=3834;aP,bx=320,46;M=28;aQ,aR,by=3,16,8;aS=.1;aT=.25;aU=5.;aj=2240;aW=22;ar=2.5;aX=2;aY=1.;aZ=4;a_=40;a0="spelltimers.ending";au=120;a1=360;v=dict.fromkeys(("Clumsy","Feeblemind","Weaken","Curse"),("target","debuff",(0,1.2,0,0,0),0,"stat"));v.update(dict.fromkeys(("Agility","Cunning","Strength","Bless"),("target","buff",(0,1.2,0,0,0),0,"stat")));v.update({"Night Sight":("target","buff",(900,0,0,0,0),2340,None),"Invisibility":("target","buff",(0,1.2,0,0,0),0,"hidden"),"Paralyze":("target","debuff",(7,.2,0,0,0),0,"paralyzed"),"Poison":("target","debuff",None,0,"poisoned"),"Protection":("self","buff",(0,2.,0,15,240),0,None),"Reactive Armor":("self","buff",None,0,None),"Magic Reflection":("self","buff",None,0,None),"Incognito":("self","buff",(1,1.2,0,0,144),0,"name"),"Polymorph":("self","buff",(0,2.,0,0,240),0,"body"),});aw={("str",1):"Strength",("str",-1):"Weaken",("dex",1):"Agility",("dex",-1):"Clumsy",("int",1):"Cunning",("int",-1):"Feeblemind"};bz=("the spell fizzles","your concentration is disturbed","insufficient mana","more reagents are needed","target cannot be seen","that is too far away","target is too far away","this spell won't work on that","this spell is already in effect","the spell will not adhere to you","you currently have a re","this target already has reactive armor","incognito cannot be cast","you cannot disguise yourself","you cannot polymorph","you cannot incognito","you cannot cast that spell in this form");bA=(("your reactive armor spell has been nullified","Reactive Armor"),("your protection spell has been nullified","Protection"));bB=(("you currently have a reflect spell","Magic Reflection"),("you currently have a reactive armor spell","Reactive Armor"));bC=("you can move!","you can move again!","you are no longer frozen");bD=(("you feel a bit nauseous",1),("you feel disoriented and nauseous",2),("you begin to feel pain throughout your body",3),("you feel extremely weak and are in severe pain",4),("you are in extreme pain, and require immediate aid",5));bE=(("looks extremely ill",2),("looks ill",1),("stumbles around in confusion and pain",3),("is wracked with extreme pain",4),("begins to spasm uncontrollably",5));bF=("the poison seems to have worn off","you feel cured of poison","you have been cured of all poisons");bG=("","Lesser","Regular","Greater","Deadly","Lethal");bH=frozenset(("paralyze","paralyzed","poison","curse","clumsy","feeblemind","weaken","mindrot","strangle","corpseskin","evilomen","bloodoath","masscurse","mortalstrike"));bI={"buff":(47,154,60),"debuff":(194,45,45),"other":(207,174,42),"dim":(90,90,90)};bJ=J.lower()+":"
		def m(name):return str(name or "").lower().replace(" ","").replace("-","")
		ax={m(cl[0]):aj+ck for ck,cl in enumerate(Kit.MAGERY)};ax["paralyzed"]=ax.get("paralyze",aj);P={m(cm):cm for cm in v};P["paralyzed"]="Paralyzed";a2={"buff":0,"debuff":1};bK=frozenset(m(cn)for cn,co in v.items()if co[1]=="buff");h={"me":True,"debuff":True,"others":True,"stats":True,"icons":True,"rows":by,"warn":0};ch=dict(h)
		def a3():b.update({"shutting":False,"docked":False,"queue":[],"rd":None,"pend":None,"landings":[],"last_land":None,"para":None,"pois":None,"stats":None,"next_sample":0.,"next_others":0.,"events":[],"icons_seen":False,"next_icons":0.,"warned":{},"rebuild":False,"dead":False,"skills":(0.,0.,-1e9)})
		b={"minimized":False,"shutting":False,"docked":False,"queue":[],"me":0,"name":"","prev_name":("",0.),"body":0,"hooked":False,"ct":None,"ct_looked":False,"ver":0,"active":False,"redraw":False};a3();c={};e={"str":[],"dex":[],"int":[]};o={"g":None,"c":{},"store":({},{}),"slots":[],"nrows":0};ci,a4,cj=ah(b,J);R=24;F=30;aB=42;Q=3;a5=24;a6=.5;z={cp:{"g":None,"cells":[],"per":1,"lines":-1,"w":0}for cp in("player","target")};a7={"rows":(aQ,aR),"warn":(0,au)}
		def a8():az(aM,";",h,a7)
		def a9():aA(aM,";",h,("me","debuff","others","stats","icons","rows","warn"),a7)
		def ba():
			p=an()
			try:return "%d,%d,%d"%(int(p.Strength),int(p.Dexterity),int(p.Intelligence))
			except Exception:return ""
		def bL():
			f=time.time();b=["t=%d"%int(f)];g=ba()
			for d in("str","dex","int"):
				for a in e[d]:b.append("e:%s,%d,%d,%d,%d,%s"%(d,a["d"],int(a["t"]),int(a["end"]or 0),1 if a.get("hide")else 0,g))
			for r in c.values():
				if r["who"]or "cast"not in r["srcs"]or "stat"in r["srcs"]or r["sid"]not in bK:continue
				b.append("r:%s,%s,%d,%d,%d"%(r["sid"],r["kind"],int(r["start"]),int(r["end"]or 0),int(r["most"]or 0)))
			T(aO,";".join(b))
		def bM(now):
			c=S(aO).split(";")
			try:d=float(c[0].split("=",1)[1])if c[0].startswith("t=")else 0.
			except(ValueError,IndexError):d=0.
			if not d or not 0<=now-d<=1800.:return
			f=ba()
			for p in c[1:]:
				try:
					g,j=p.split(":",1);b=j.split(",")
					if g=="e"and b[0]in e and h["stats"]:
						if len(e[b[0]])>=aZ:continue
						k,l,a=int(b[1]),float(b[2]),float(b[3])
						if(a and a>now)or(not a and f and len(b)>7 and ",".join(b[5:8])==f):e[b[0]].append({"d":k,"t":l,"end":a or None,"hide":len(b)>4 and b[4]=="1"})
					elif g=="r"and b[0]in P:
						m,a,i=float(b[2]),float(b[3]),float(b[4])
						if a and max(a,i)<=now:continue
						r=u(0,b[0],b[1]if b[1]in a2 else "buff",m);r["end"],r["most"]=a or None,i or None;r["srcs"].add("cast")
				except Exception:continue
		def u(who,sid,kind,now,name=""):
			a=(who,sid);r=c.get(a)
			if r is None:
				r={"key":a,"who":who,"sid":sid,"kind":kind,"start":now,"end":None,"most":None,"srcs":set(),"watch":None,"seen":False,"confirm":0.,"base":None,"level":0,"delta":0,"name":name,"away":0.,"icon":ax.get(sid,aj),"end_src":None};c[a]=r
				if len(c)>a_:bN(a)
			else:
				r["kind"]=kind
				if name:r["name"]=name
			b["ver"]+=1;return r
		def f(key):
			if c.pop(key,None)is not None:b["ver"]+=1;b["warned"].pop(key,None)
		def aC(key,src):
			r=c.get(key)
			if r is None:return
			r["srcs"].discard(src)
			if not r["srcs"]:f(key)
			else:b["ver"]+=1
		def bN(keep):
			b=sorted(c.values(),key=lambda r:(r["who"]==0,r["start"]))
			for a in b:
				if len(c)<=a_:break
				if a["key"]!=keep:c.pop(a["key"],None)
		def bb(r):return(r["sid"],r.get("label"),r["delta"],r["level"],r["who"],r["name"],r["end"]is None,"stat"in r["srcs"])
		def aD(r):
			b=r["sid"];a=P.get(b)or r.get("label")or b
			if r["delta"]:a="%s %+d"%(a,r["delta"])
			if r["level"]and b=="poison":a="%s (%s)"%(a,bG[max(1,min(5,r["level"]))])
			if r["who"]:a="%s: %s"%(a,r["name"]or "someone")
			return a
		def bc(now,force=False):
			s=b["skills"]
			if force or not 0<=now-s[2]<15.:s=b["skills"]=(al("Magery",s[0]),al("Evaluating Intelligence",s[1]),now)
			return s
		def bO(spell,now):
			b=v.get(spell)
			if b is None or b[2]is None:return
			e,f,g,c,d=b[2];h,i,j=bc(now);a=e+f*h+g*i
			if c:a=max(c,a)
			if d:a=min(d,a)
			return max(1.,a)
		def bP(spell,at,now):
			a=b["pend"]
			if a is not None:
				c=a["at"]+a["delay"];b["pend"]=None
				if a["side"]=="self"and at>=c-.05:V(a,b["me"],c,now)
				elif a["side"]=="target"and not a["cursor"]and at>=c+.2:
					e=int(API.LastTargetSerial or 0)
					if e:V(a,e,c,now)
			f=v.get(spell)
			if f is None:b["pend"]=None;return
			d=aF(spell);g=d[3]if d and d[3]else 1.;bc(now,True);b["pend"]={"spell":spell,"sid":m(spell),"at":at,"delay":float(g),"side":f[0],"cursor":False,"body0":b["body"],"name0":b["name"]}
		def bQ(now):
			p=b["pend"]
			if p is None:return
			a=p["at"]+p["delay"]
			if now<a-.05:return
			if p["side"]=="self":
				if now>=a+.6:b["pend"]=None;V(p,b["me"],a,now)
				return
			if API.HasTarget():
				if not p["cursor"]:p["cursor"]=True;p["lt0"]=int(API.LastTargetSerial or 0)
				p["mana0"]=int(API.Player.Mana);p["gone"]=None
				if now>a+30.:b["pend"]=None
				return
			if not p["cursor"]and now<a+1.2:return
			c=int(API.LastTargetSerial or 0)
			if p["cursor"]:
				if p.get("gone")is None:p["gone"]=now
				if int(API.Player.Mana)>=p["mana0"]and c==p.get("lt0",0):
					if 0<=now-p["gone"]<1.5:return
					b["pend"]=None;return
			b["pend"]=None
			if c:V(p,c,now,now)
		def V(p,who,at,now):
			f,g=p["spell"],p["sid"];c=v[f];i=b["me"];d=not who or who==i;e=bO(f,now)
			if d and c[4]=="stat"and h["stats"]:b["landings"].append({"sid":g,"t":at,"dur":e or 0.});del b["landings"][:-6];bd(now);return
			m=None if d else API.FindMobile(who);j=str(m.Name or "")if m is not None else "";r=u(0 if d else who,g,c[1],at,j);r["start"]=at;r["srcs"].add("cast")
			if r["end_src"]!="icon":r["end"]=(at+e)if e else None;r["most"]=(at+c[3])if c[3]else None;r["end_src"]="cast"
			r["delta"],r["away"]=0,0.;a=c[4]
			if a=="stat"or(a in("body","name","hidden")and not d):a=None
			r["watch"],r["seen"]=a,False;r["confirm"]=now+2.
			if a=="body":r["base"]=p["body0"]
			elif a=="name":r["base"]=p["name0"]
			b["last_land"]=(r["key"],now);b["warned"].pop(r["key"],None)
		def bR(now,d=False):
			p=b["pend"]
			if p is not None and(d or now>=p["at"]+p["delay"]-.3):b["pend"]=None;return
			a=b["last_land"]
			if a is not None and 0<=now-a[1]<=1.:
				b["last_land"]=None;r=c.get(a[0])
				if r is not None and r["srcs"]==set(("cast",)):f(a[0])
		def bd(now):
			c=[g for g in b["landings"]if 0<=now-g["t"]<=ar+1.];b["landings"]=c
			if not c:return False
			d=False
			for f in("str","dex","int"):
				for a in e[f]:
					if(a["end"]is not None or a["d"]<=0 or not 0<=now-a["t"]<=ar+1.):continue
					for l in reversed(c):
						if l["sid"]in("bless",m(aw[(f,1)]))and abs(a["t"]-l["t"])<=ar and l["dur"]:a["end"],a["cast"]=l["t"]+l["dur"],l["sid"];d=True;break
			if d:Y()
			return d
		def bS(stat,d,now):
			a=e[stat];c=0
			for b in a:c+=b["d"]
			if a and c+d==0:del a[:];return
			for i,b in enumerate(a):
				if b["d"]==-d:del a[i];return
			a.append({"d":d,"t":now,"end":None})
			if len(a)>aZ:del a[0]
		def bT(vals,now):
			c=b["stats"];b["stats"]=vals
			if c is None:return
			a=False
			for i,f in enumerate(("str","dex","int")):
				d=vals[i]-c[i]
				if abs(d)>30:del e[f][:];a=True
				elif abs(d)>=aX:bS(f,d,now);a=True
			if a:
				p=b["pend"]
				if p is not None and p["side"]=="target"and v[p["spell"]][4]=="stat"and now>=p["at"]+p["delay"]-.4 and h["stats"]:b["pend"]=None;V(p,b["me"],now,now)
				bd(now);Y()
		def Y():
			k={};h=set();S,D,I=e["str"],e["dex"],e["int"]
			for a in S:
				if a.get("hide"):continue
				for d in D:
					if id(d)in h or d.get("hide")or d["d"]!=a["d"]or abs(d["t"]-a["t"])>aY:continue
					for f in I:
						if id(f)in h or f.get("hide")or f["d"]!=a["d"]or abs(f["t"]-a["t"])>aY:continue
						h.update((id(a),id(d),id(f)));i="bless"if a["d"]>0 else "curse";o=a["end"]or d["end"]or f["end"];be(k,i,a["d"],min(a["t"],d["t"],f["t"]),o);break
					if id(a)in h:break
			for l in("str","dex","int"):
				for g in e[l]:
					if id(g)in h or g.get("hide"):continue
					i=m(aw[(l,1 if g["d"]>0 else-1)]);be(k,i,g["d"],g["t"],g["end"])
			for i,j in k.items():
				p="buff"if j[0]>0 else "debuff";r=u(0,i,p,j[1])
				if "stat"not in r["srcs"]:r["start"]=j[1]
				r["srcs"].add("stat");r["delta"]=j[0]
				if r["end_src"]!="icon":r["end"],r["end_src"]=j[2],"stat";r["most"]=None
			for n in[t for t,s in c.items()if not s["who"]and "stat"in s["srcs"]and s["sid"]not in k]:r=c[n];r["delta"]=0;aC(n,"stat")
			b["ver"]+=1
		def be(groups,sid,d,t,end):
			g=groups.get(sid)
			if g is None:groups[sid]=[d,t,end]
			else:
				g[0]+=d;g[1]=min(g[1],t)
				if end is not None and(g[2]is None or end>g[2]):g[2]=end
		def bf():
			for a in[g for g in c if not g[0]]:f(a)
			for d in e:del e[d][:]
			b.update({"stats":None,"pend":None,"landings":[],"para":None,"pois":None})
		def bU(now):
			p=an()
			if p is None:return
			i=int(p.Serial);g=str(p.Name or "");m=bool(p.IsDead);n=bool(p.IsParalyzed);o=bool(p.IsPoisoned);q=bool(p.IsHidden);j=int(p.Graphic or 0);d=(int(p.Strength or 0),int(p.Dexterity or 0),int(p.Intelligence or 0))
			if i!=b["me"]:
				if b["me"]:bf()
				b["me"]=i
			if g!=b["name"]:
				if b["name"]:b["prev_name"]=(b["name"],now)
				b["name"]=g
			if m:
				if not b["dead"]:b["dead"]=True;bf()
				return
			if b["dead"]:b["dead"]=False;b["stats"]=None
			b["body"]=j
			for k,l,a in(("para","paralyzed",n),("pois","poison",o)):
				if a!=b[k]:
					b[k]=a
					if a:u(0,l,"debuff",now)["srcs"].add("flag")
					else:f((0,l))
			for r in list(c.values()):
				if r["who"]or r["watch"]is None:continue
				w=r["watch"]
				if w=="hidden":a=q
				elif w=="body":a=j!=r["base"]
				elif w=="name":a=g!=r["base"]
				else:continue
				if a:r["seen"]=True
				elif r["seen"]:f(r["key"])
				elif w=="hidden"and now>r["confirm"]:f(r["key"])
			if h["stats"]:
				if d[0]and d[1]and d[2]:bT(d,now)
			elif b["stats"]is not None or e["str"]or e["dex"]or e["int"]:
				b["stats"]=None
				for s in e:del e[s][:]
				Y()
		def bV(now):
			if not c:return
			d={};g={}
			for r in list(c.values()):
				a=r["who"]
				if not a:continue
				if a not in d:d[a]=API.FindMobile(a)
				m=d[a]
				if m is None:
					if not r["away"]:r["away"]=now;b["ver"]+=1
					if r["watch"]and not r["seen"]and now>r["confirm"]:f(r["key"])
					continue
				if r["away"]:r["away"]=0.;b["ver"]+=1
				try:
					e=g.get(a)
					if e is None:e=g[a]=bool(m.IsDead)
					if e:f(r["key"]);continue
					w=r["watch"]
					if w=="paralyzed":h=bool(m.IsParalyzed)
					elif w=="poisoned":h=bool(m.IsPoisoned)
					else:continue
				except Exception:continue
				if h:
					if not r["seen"]:r["seen"]=True
				elif r["seen"]:f(r["key"])
				elif now>r["confirm"]:f(r["key"])
		def bW(now):
			f=b["rd"]
			if f is None:b["rd"]=Z();return
			g=f.new()
			if not g:return
			h=b["name"];i,k=b["prev_name"]
			for d in g:
				c=d.low
				if c.startswith(bJ):continue
				a=d.name or "";e=bool(h)and a==h or(i and a==i and 0<=now-k<=5.)
				if e:
					j=Kit.SPELL_WORDS.get(c.strip())
					if j is not None:bP(j[0],min(now,d.at or now),now);continue
				if a and not e and a!="System":bY(c,a);continue
				bX(c,now,not e)
		def bX(low,now,system):
			d=low.strip(" *")
			for t,e in bD:
				if d.startswith(t):
					r=u(0,"poison","debuff",now);r["srcs"].add("line")
					if e!=r["level"]:r["level"]=e;b["ver"]+=1
					return
			if not system:return
			for t in bz:
				if low.startswith(t):
					for g,a in bB:
						if low.startswith(g):
							r=c.get((0,m(a)))
							if r is None:r=u(0,m(a),"buff",now)
							r["srcs"].add("cast")
					p=b["pend"]
					if p is not None and p["sid"]in("reactivearmor","magicreflection")and t=="this spell is already in effect"and(0,p["sid"])not in c:u(0,p["sid"],"buff",now)["srcs"].add("cast")
					bR(now,t=="your concentration is disturbed");return
			for t,a in bA:
				if low.startswith(t):f((0,m(a)));return
			if low.startswith("you cannot move!"):u(0,"paralyzed","debuff",now)["srcs"].add("line")
			elif low.startswith(bC):f((0,"paralyzed"))
			elif d.startswith(bF):f((0,"poison"))
		def bY(low,name):
			for r in c.values():
				if r["who"]and r["sid"]=="poison":break
			else:return
			for t,a in bE:
				if t in low:
					d=name.lower()
					for r in c.values():
						if r["who"]and r["sid"]=="poison"and r["name"]and r["level"]!=a and(r["name"].lower()==d or r["name"].lower()in low):r["level"]=a;b["ver"]+=1
					return
		def bg(kind,c):
			if not b["active"]:return
			for a in c:
				try:d=(kind,str(a.Title or ""),int(a.Graphic or 0),int(a.Timer or 0))
				except Exception:continue
				if len(b["events"])<60:b["events"].append(d);HOST.poked=True
				return
		def bZ():aV(b,"hooked",("OnBuffAdded",lambda*a:bg("add",a)),("OnBuffRemoved",lambda*a:bg("remove",a)))
		def b_():
			if not b["ct_looked"]:
				b["ct_looked"]=True
				try:t=W("ClassicUO.Time");m=aJ(t,"Ticks")if t is not None else None;b["ct"]=m[0]if m else None
				except Exception:b["ct"]=None
			a=b["ct"]
			if a is None:return
			try:return int(a())
			except Exception:return
		def bh(title,graphic,a,now):
			b=m(title)
			if not b:return
			e="debuff"if b in bH else "buff";r=u(0,b,e,now)
			if "icon"not in r["srcs"]:r["start"]=now
			r["srcs"].add("icon");r["label"]=title
			if graphic:r["icon"]=graphic
			c=None
			if 0<a<0xFFFFFFFF:
				d=b_()
				if d is not None and a>d:c=now+(a-d)/1000.
			if c is not None:r["end"],r["end_src"],r["most"]=c,"icon",None
		def b0(now):
			f,b["events"]=b["events"],[]
			if not h["icons"]:return
			for g,a,i,j in f:
				b["icons_seen"]=True
				if g=="add":bh(a,i,j,now)
				else:aC((0,m(a)),"icon")
			if now>=b["next_icons"]:
				b["next_icons"]=now+aU
				if not b["icons_seen"]and b["next_icons"]-aU>b["started"]+1.:return
				e=set()
				for d in API.ActiveBuffs()or[]:
					a=str(d.Title or "")
					if not a:continue
					e.add(m(a));b["icons_seen"]=True;r=c.get((0,m(a)))
					if r is None or "icon"not in r["srcs"]:bh(a,int(d.Graphic or 0),int(d.Timer or 0),now)
				for k in[p for p,s in c.items()if not p[0]and "icon"in s["srcs"]and p[1]not in e]:aC(k,"icon")
		def b1(now):
			if not c:return
			for r in list(c.values()):
				b,a=r["key"],r["srcs"];d=r["end"]
				if r["who"]and r["away"]and now-r["away"]>60. and(d is None or now>d):f(b);continue
				if "icon"in a or "stat"in a or "flag"in a:continue
				if r["watch"]and r["seen"]:continue
				if "line"in a and "cast"not in a:
					if now-r["start"]>60.:f(b)
					continue
				if d is None:
					if not r["watch"]and now-r["start"]>3600.:f(b)
					continue
				if now>max(d,r["most"]or 0)+1.:f(b)
		def b2(now):
			a=h["warn"]
			if not a or not h["me"]:return
			for r in c.values():
				if r["who"]or r["kind"]!="buff"or r["end"]is None:continue
				d=r["end"]-now;e=r["key"]
				if 0<d<=a and b["warned"].get(e)!=r["end"]:b["warned"][e]=r["end"];am(a0,"%s runs out in %d s"%(P.get(r["sid"],r.get("label")or r["sid"]),int(d+.5)),"info",who=r["sid"])
		def aE():return a1,2*E+30+B+M+12
		def b3():z=n.slot if aG(I)and not b["minimized"]else None;a,c=aE();return z if z is not None and z[0]>=a and z[1]>=c else None
		def ae():
			a=b3();f=2*E+30+B+12;w=a[0]if a else a1;i=[];d=n.rows(M,f,h["rows"])if a else h["rows"];g,p,o=n.begin(w,a[1]if a else f+d*M)
			if not b["minimized"]:
				c=E;j=w-2*c;n.frame(g);e=c+30+B;H(g,c,e,j,(a[1]-c-e)if a else d*M+12);o["empty"]=l(g,"",c+12,e+10,k)
				for m in range(d):i.append(b4(g,m,c,e+6+m*M,j))
			n.end(g,{"slots":i,"nrows":d});b["redraw"]=True;br(time.time())
		n=Kit.Window(I,J,b,o,ae,bu,bv,default=(60,260),mini=(aP,bx),icon=bw,lock=True,clear={"slots":[]})
		def bi(g,x,y,px):a=G.CreateGumpPic(aj,x,y);a.SetPos(x,y);a.SetWidth(px);a.SetHeight(px);a.SetAcceptMouseInput(False);g.Add(a);return a
		def bj(s,icon,px):s["icon_g"]=icon;s["pic"].Graphic=icon;s["pic"].SetWidth(px);s["pic"].SetHeight(px)
		def b4(g,i,sx,a,IW):s={"row":None,"prev":(None,0.),"vis":True,"icon_g":None,"tip":None,"tx":None,"fw":-1,"col":None,"x":sx,"y":a,"iw":IW};s["pic"]=bi(g,sx+6,a+2,aW);s["name"]=l(g,"",sx+34,a+1,C);s["time"]=l(g,"",sx+IW-50,a+1,k);b=IW-34-10;s["bw"]=b;s["bg"]=O(g,sx+34,a+19,b,5,.9,"#202020");s["fill"]=O(g,sx+34,a+19,b,5,1.,"#2f9a3c");s["hit"]=D(g,sx,a,IW,M-2,bk(lambda:o["slots"],i),"");af(s,False);return s
		def bk(get,i):
			def a(*e):
				a=get()
				if i>=len(a):return
				c=a[i];r=c["row"];b,d=c["prev"]
				if 0<=time.time()-d<=.15:r=b
				if r is None:return
				if r[0]and ac():a4(("follow",r[0]))();return
				a4(("clear",r))()
			return a
		def af(s,on):
			if s["vis"]==on:return
			s["vis"]=on
			for k in("pic","name","time","bg","fill","hit"):
				if s.get(k)is not None:s[k].IsVisible=on
		def b5():
			a=[]
			for r in c.values():
				if r["who"]:
					if not h["others"]:continue
				elif r["kind"]=="buff":
					if not h["me"]:continue
				elif not h["debuff"]:continue
				a.append(r)
			a.sort(key=b6);return a
		def b6(r):a=r["end"];return(1 if r["who"]else 0,a2.get(r["kind"],2),a if a is not None else 1e18,r["start"])
		def bl(s):
			s=int(s+.999)
			if s<60:return "%ds"%s
			if s<3600:return "%d:%02d"%(s//60,s%60)
			return "%dh %02d"%(s//3600,(s%3600)//60)
		def aK(r,now):
			a=r["end"]
			if a is None:
				if r["sid"]in("reactivearmor","magicreflection")and not r["who"]:return "on",None,False
				return "+"+bl(max(0.,now-r["start"])),None,False
			b=a-now
			if b>0:c=max(.1,a-r["start"]);return bl(b),max(0.,min(1.,b/c)),False
			if r["most"]and now<r["most"]:return "soon",None,True
			return "due"if("stat"in r["srcs"]or "icon"in r["srcs"])else "0s",0.,True
		def bm(r):
			if r["who"]:return("%s on %s, cast by you. Click: clear this row. Alt+click: auto-follow (again to stop)"%(P.get(r["sid"],r["sid"]),r["name"]or "them"))
			if "stat"in r["srcs"]and r["end"]is None:return "From a stat step; ends when it steps back. Click: clear this row."
			if r["end"]is None and r["sid"]in("reactivearmor","magicreflection"):return "Up until used up (the shard doesn't say when). Click: clear this row."
			return "Click: clear this row"
		ao=("player","target");bn={"player":I,"target":I+".target"}
		def ag():return b.get("row_mode",False)
		def b7(now):
			if 0<=b.get("form_at",0.)-now<=a6:return
			b["form_at"]=now+a6;g=U("player");c=g is not None
			if c!=ag():bo(c)
			elif c:
				for d in ao:
					a=z[d];f=U(d);e=a["w"]
					if f is not None:
						r=ab(f)
						if r is None:continue
						e=r[2]
					if a["g"]is None or e!=a["w"]:aL(d,e,max(0,a["lines"]))
		def bo(row):
			b["row_mode"]=row
			if row:
				aN(I);n.close()
				for a in ao:c=U(a);r=ab(c)if c is not None else None;aL(a,r[2]if r is not None else 200,0)
				for a in ao:aH(bn[a],a,1,lambda s=a:z[s]["g"])
			else:bp();ae();n.dock(fit=True,min=aE)
			b["redraw"]=True
		def bp():
			for b in ao:aI(bn[b]);a=z[b];g,a["g"]=a["g"],None;a["cells"],a["lines"],a["w"]=[],-1,0;K(g)
		def aL(side,fw,lines):
			c=z[side];a,c["g"]=c["g"],None;fw=max(F+2*Q,int(fw));b=max(1,(fw-2*Q)//F);h=max(1,lines)*aB+2*Q;x,y=0,0
			if q(a):x,y=a.GetX(),a.GetY()
			g=G.CreateGump(True,False);H(g,0,0,fw,h,alpha=.6);d=[];n=min(a5,b*max(1,lines));e=Q+(fw-2*Q-b*F)//2
			for i in range(n):f,j=divmod(i,b);d.append(b8(g,side,i,e+j*F,Q+f*aB))
			ai(g,x,y,fw,h);G.AddGump(g);g.IsVisible=lines>0;c.update({"g":g,"cells":d,"per":b,"lines":lines,"w":fw});K(a)
		def b8(g,side,i,a,b):c={"row":None,"prev":(None,0.),"icon_g":None,"tip":None,"vis":True,"x":a,"y":b,"tw":None};c["pic"]=bi(g,a+(F-R)//2,b,R);c["time"]=l(g,"",a,b+R+1,k);c["time"].SetAcceptMouseInput(False);c["hit"]=D(g,a,b,F,aB-2,bk(lambda:z[side]["cells"],i),"");return c
		def bq(side,now,mine):
			a=z[side];mine=mine[:a5];f=a["per"];g=(len(mine)+f-1)//f if mine else 0
			if g!=a["lines"]:aL(side,a["w"]or 200,g)
			if a["g"]is None:return
			for i,c in enumerate(a["cells"]):
				r=mine[i]if i<len(mine)else None;h=r["key"]if r is not None else None
				if h!=c["row"]:c["prev"]=(c["row"],now);c["row"]=h
				if r is None:af(c,False);continue
				af(c,True);k=r["icon"]
				if k!=c["icon_g"]:bj(c,k,R)
				b,n,m=aK(r,now)
				if r["end"]is None:b=""
				d=aa(b)if b else 0
				if d!=c["tw"]:c["tw"]=d;ak(c["time"],c["x"]+max(0,(F-d)//2),c["y"]+R+1)
				A(c["time"],b,j if(m or r["kind"]=="debuff")else C);l=bb(r)
				if l!=c.get("tipk"):
					c["tipk"]=l;e="%s. %s"%(aD(r),bm(r))
					if e!=c["tip"]:c["tip"]=e;c["hit"].SetTooltip(e)
		def br(now):
			d=ag()
			if not d and(o["g"]is None or(b["minimized"]and b["docked"])):return
			if not b["redraw"]and b.get("drawn_at",0.)+.25>now>=b.get("drawn_at",0.)and b.get("drawn_ver")==b["ver"]:return
			b["redraw"]=False;b["drawn_at"],b["drawn_ver"]=now,b["ver"];a=b5()
			if d:
				e=av["fn"]()if av["fn"]is not None and U("target")is not None else 0;j=[p for p in a if not p["who"]];l=[w for w in a if e and w["who"]==e]
				if z["player"]["g"]is not None:bq("player",now,j)
				if z["target"]["g"]is not None:bq("target",now,l)
				return
			f=o["c"]
			if b["minimized"]:
				g=f.get("status")
				if g is not None:
					if a:
						t=aK(a[0],now)[0];c="%s: %s %s"%(J,aD(a[0]),t)
						if len(a)>1:c+="  (+%d)"%(len(a)-1)
						c=L(c,aP-90)
					else:c="%s: no timers"%J
					A(g,c,k)
				return
			m=o["slots"];A(f["empty"],""if a else "No timers yet; your buffs and casts show here.",k)
			for i,s in enumerate(m):
				r=a[i]if i<len(a)else None;h=r["key"]if r is not None else None
				if h!=s["row"]:s["prev"]=(s["row"],now);s["row"]=h
				if r is None:af(s,False);continue
				af(s,True);b9(s,r,now)
		def b9(s,r,now):
			l=r["icon"]
			if l!=s["icon_g"]:bj(s,l,aW)
			if r["who"]:f,a=(k if r["away"]else N),"other"
			elif r["kind"]=="debuff":f,a=j,"debuff"
			else:f,a=C,"buff"
			c,m,n=aK(r,now)
			if r["who"]and r["away"]:c=c+" (away)"
			q=aa(c);d=s["x"]+s["iw"]-8-q
			if d!=s["tx"]:s["tx"]=d;ak(s["time"],d,s["y"]+1)
			A(s["time"],c,j if n else k);g=bb(r);o=d-(s["x"]+34)-6;p=(g,o)
			if p!=s.get("namek"):t=aD(r);s["namek"],s["name_txt"]=p,L(t,max(20,o))
			A(s["name"],s["name_txt"],f)
			if m is None:b,a=s["bw"],"dim"
			else:
				b=int(round(s["bw"]*m))
				if n:a="dim"
			e=s["fill"]
			if b!=s["fw"]:
				s["fw"]=b
				if b<=0:e.IsVisible=False
				else:ap(e,b);e.IsVisible=True
			if a!=s["col"]:s["col"]=a;h=bI[a];e.SetBaseColor(h[0],h[1],h[2],255)
			if g!=s.get("tipk"):
				s["tipk"]=g;i=bm(r)
				if i!=s["tip"]:s["tip"]=i;s["hit"].SetTooltip(i)
		def ca(key):
			r=c.get(key)
			if r is None:return
			if "stat"in r["srcs"]:
				for b in("str","dex","int"):
					for a in e[b]:
						d=m(aw[(b,1 if a["d"]>0 else-1)])
						if d==key[1]or(key[1]in("bless","curse")and(a["d"]>0)==(key[1]=="bless")):a["hide"]=True
			f(key)
			if "stat"in r["srcs"]:Y()
		bs={"follow":lambda serial:X(serial,J),"clear":ca}
		def cb(w):return(("WINDOW  (what it lists)",(("check","me","Show the buffs on you","Bless, Strength, Protection, Reactive Armor, Magic Reflection, Night Sight and more"),("check","debuff","Show what is done to you (paralyze, poison, curses)","Paralyzed, Poison (with its level), Curse, Clumsy, Feeblemind and Weaken on you"),("check","others","Show your spells on others","What you cast on someone else. Alt+click such a row: auto-follow (again to stop)"),("num","rows","Rows shown:","Rows the window has room for",None,aQ,aR,{"clamp":False})),{"sh":140}),("TIMER SOURCES  (your casts always count)",(("check","stats","Watch your stats for Bless, Curse and their kin","A Str, Dex or Int step of %d or more is a spell on you (all three: Bless / Curse); potions show too"%aX),("check","icons","Use the shard's buff icons when it sends them","Exact names and times when the shard sends icons (a classic shard sends none)")),{"sh":90}),("ALERTS  (sound: Settings > Alerts)",(("num","warn","Warn before a buff on you runs out:","One alert this many seconds before it ends (0-%d, 0 = never)"%au,"s",0,au,{"clamp":False}),),{"sh":64}))
		def cc(a,new):
			b["redraw"]=True
			if new["icons"]and not a["icons"]:b["next_icons"]=0.
			if new["rows"]!=a["rows"]:b["rebuild"]=True
			if new["warn"]!=a["warn"]:b["warned"]={}
		aq=Kit.Page(h,cb,a9,cc,{"ldy":4,"lgap":12,"fw":40})
		def bt(serial=None):
			f=time.time();g=b["me"];d=[]
			for r in c.values():
				e=r["who"]or g
				if serial is not None and e!=serial:continue
				a=r["end"];d.append({"spell":P.get(r["sid"],r.get("label")or r["sid"]),"serial":e,"you":not r["who"],"kind":r["kind"],"end":a,"left":(a-f)if a is not None else None,"icon":r["icon"],"level":r["level"],"delta":r["delta"]})
			return d
		a8()
		def cd():
			a=time.time();a3();b.update({"active":True,"redraw":True,"started":a,"minimized":n.start_min()});c.clear()
			for d in e:del e[d][:]
			a8();bM(a);Y();bZ();ad(a0,"Buff about to run out",490);b["row_mode"],b["form_at"]=False,0.
			if U("player")is not None:bo(True)
			else:ae();n.dock(fit=True,min=aE)
			HOST.services["spelltimers.list"]=bt
		def ce():
			a=time.time();b7(a)
			if o["g"]is None and not ag():return
			if o["g"]is not None and ay(o):return
			while b["queue"]:
				c=b["queue"].pop(0);d=c[0]if isinstance(c,tuple)else c
				if c=="redraw":
					if not ag():ae()
				elif n.action(c):pass
				elif d in bs:bs[d](c[1])
			if b["rebuild"]:
				b["rebuild"]=False
				if not ag()and not b["minimized"]and h["rows"]!=o["nrows"]:ae()
			b0(a)
			if not 0<=b["next_sample"]-a<=aS:b["next_sample"]=a+aS;bU(a)
			bW(a);bQ(a)
			if cf()and not 0<=b["next_others"]-a<=aT:b["next_others"]=a+aT;bV(a)
			b1(a);b2(a);br(a)
		def cf():
			for k in c:
				if k[0]:return True
			return False
		def cg():
			b["shutting"]=True;b["active"]=False;aN(I)
			if HOST.services.get("spelltimers.list")is bt:HOST.services.pop("spelltimers.list",None)
			bp();n.close();a9();bL()
		return{"start":cd,"tick":ce,"stop":cg,"client_tick":True,"config_height":aq.height,"build_config":aq.build,"poll_config":aq.poll,"config_closed":aq.closed}
	def bb():
		av="swing";L="Swing Bar"
		try:from System import DateTime
		except Exception:DateTime=None
		bq=[(0,4,-10,"Starving"),(5,9,-5,"Hungry"),(10,14,0,"Fed"),(15,19,0,"Full"),(20,20,0,"Stuffed"),];a_=300;a0=20;br=[("lich lord",90),("lich",70),("dragon",90),("daemon",90),("troll",60),("ogre lord",85),("ogre",65),("orc captain",80),("orc",55),("ettin",55),("skeleton",50),("zombie",35),("rat",25),("headless",30),("mongbat",10),];aw=60;ab,af=0,120;V="CTRL+SHIFT+T";ay="CTRL+SHIFT+R";az="CTRL+SHIFT+UP";aA="CTRL+SHIFT+DOWN";a2="CTRL+SHIFT+RIGHT";a4="CTRL+SHIFT+LEFT";bs,bt=300,300;bu,bv=53,"#b8913a";bw,bx=63,"#3fa34d";by,bz=946,"#6b6b6b";aB=10;a5=250;a6="SwingTimer_history";bA=("you have been disarmed","your weapon has been disarmed");bB=("you have been knocked off","you fall off of your mount","you fall off your mount");bC=("system","");a7="swing.notice";a8=30.;a9,aC,aj,aE=68,53,33,946;W=C;m,P,r,WR="Swordsmanship","Fencing","Mace Fighting","Wrestling";AR="Archery";_W=[("Broadsword",45,m,(3934,3935)),("Cutlass",45,m,(5185,5184)),("Katana",58,m,(5119,5118)),("Longsword",35,m,(3937,3936)),("Scimitar",30,m,(5046,5045)),("Viking Sword",30,m,(5049,5050)),("Thin Longsword",35,m,(5048,5047)),("Butcher Knife",40,m,(5110,5111)),("Cleaver",40,m,(3779,3778)),("Skinning Knife",40,m,(3780,3781)),("Axe",37,m,(3913,3914)),("Battle Axe",31,m,(3911,3912)),("Double Axe",37,m,(3915,3916)),("Executioner's Axe",37,m,(3909,3910)),("Large Battle Axe",29,m,(5115,5114)),("Two Handed Axe",31,m,(5187,5186)),("Pickaxe",35,m,(3718,3717)),("Hatchet",41,m,(3907,3908)),("Bardiche",26,m,(3917,3918)),("Halberd",25,m,(5182,5183)),("Dagger",55,P,(3922,3921)),("Kryss",53,P,(5121,5120)),("Short Spear",50,P,(5123,5122)),("Spear",46,P,(3938,3939)),("War Fork",45,P,(5125,5124)),("Pitchfork",45,P,(3719,3720)),("Club",40,r,(5044,5043)),("Hammer Pick",30,r,(5181,5180)),("Mace",30,r,(3932,3933)),("Maul",30,r,(5179,5178)),("War Axe",40,r,(5040,5039)),("War Hammer",31,r,(5177,5176)),("War Mace",26,r,(5127,5126)),("Quarter Staff",48,r,(3721,3722)),("Gnarled Staff",33,r,(5112,5113)),("Black Staff",35,r,(3568,3569)),("Shepherd's Crook",30,r,(3713,3714)),("Bow",20,AR,(5042,5041)),("Crossbow",18,AR,(3920,3919)),("Heavy Crossbow",10,AR,(5117,5116)),];aF={}
		for bD,bE,bF,bG in _W:
			for _g in bG:aF[_g]=(bD,bE,bF)
		bH=("Fists",30,WR);bI={562,563,564,567,568,569,570,571,572};bJ=[("supremely accurate",10),("exceedingly accurate",8),("eminently accurate",6),("surpassingly accurate",4),("accurate",2)]
		def aq(a,b):
			v=(a+100)*b
			if v<=0:v=1
			return 15000./v*1000.
		def aG(hunger):
			h=int(round(max(0,min(20,hunger))))
			for a,b,c,d in bq:
				if a<=h<=b:return c,d
			return 0,"?"
		def bK(b,c,d,hunger):e,f=aG(hunger);a=(max(b,-49.9)+50.)/((max(c,-49.9)+50.)*2.);a*=1.+d/100.;return max(0.,min(1.,a*(1.+e/100.)))
		def o():return time.time()*1000.
		def aJ():
			for b in("OneHanded","TwoHanded"):
				a=API.FindLayer(b)
				if a and int(a.Graphic)in aF:c,d,e=aF[int(a.Graphic)];return c,d,e,bL(a)
			return bH+(0,)
		ar={}
		def bL(item):
			a=int(item.Serial);c=ar.get(a)if a else None
			if c is not None and time.time()<c[1]:return c[0]
			d=(item.Name or "").lower()
			if "accurate"not in d:d=(API.ItemNameAndProps(a,False)or "").lower()
			b=0
			for e,p in bJ:
				if e in d:b=p;break
			if a:
				if len(ar)>50:ar.clear()
				ar[a]=(b,time.time()+(1e9 if b else 2.))
			return b
		def aK(mob,a,name=None):
			if a is not None:return a
			if mob is None:return B["enemy_default"]
			name=(mob.Name or ""if name is None else name).lower()
			for b,c in br:
				if b in name:return c
			return 100 if mob.IsHuman else B["enemy_default"]
		def E(key,default):
			try:return float(S(key,str(default)))
			except Exception:return float(default)
		def u(key,value):T(key,str(value))
		def bM(v):
			try:return int(max(ab,min(af,int(round(float(v))))))
			except Exception:return aw
		B={"enemy_default":aw};ct=dict(B);st={"minimized":False,"shutting":False,"docked":False,"queue":[]};d={"g":None,"c":{},"store":({},{}),"bar_w":109,"x1":0,"row1":0,"food_w":[0]*21,"fill_w":-1,"fill_state":None,"shown":{},"tips":{},"active":False,"closing":False};cu,cv,at=ah(st,L)
		def bN():B["enemy_default"]=bM(E("swingtimer_enemy_default",aw))
		def bO():u("swingtimer_enemy_default",B["enemy_default"])
		bN()
		class State:last_swing=None;cycle_ms=None;gaps=[];gaps_weapon=None;history={};slow=[];dirty=False;paused_at=None;target_serial=0;enemy_override=None;hunger=a0;hunger_clock=o();seen_sounds=set();sounds=[];keys=[];notice=None
		c=State()
		def ba():
			if not c.gaps:return
			return sum(c.gaps)/float(len(c.gaps))
		def bb(name):return name.replace("|","/").replace(";","/")
		def bc(weapon):
			a=(weapon[0],int(weapon[1]))
			if c.gaps_weapon==a:return False
			b=(bb(a[0]),a[1])
			if a not in c.history and b in c.history:c.history[a]=c.history.pop(b)
			c.gaps_weapon=a;c.gaps=c.history.setdefault(a,[]);c.slow=[];return True
		n={"saved_at":0.,"save":False,"import":False}
		def bd(text,c):
			b={}
			for d in text.split(c):
				p=d.strip().split("|")
				if len(p)!=3 or not p[0]:continue
				try:e=int(p[1]);a=[float(h)for h in p[2].split(",")if h.strip()]
				except Exception:continue
				a=[t for t in a if t>=a5][-aB:]
				if a:b[(p[0],e)]=a
			return b
		def bP():
			c.history={};c.gaps,c.gaps_weapon,c.dirty,c.slow=[],None,False,[];a=S(a6)
			if a:c.history=bd(a,";")
			n["import"]=not c.history
		def bQ():
			if o()<n.get("import_next",0.):return
			n["import_next"]=o()+1000.
			try:a=int(API.Player.Serial)
			except Exception:a=0
			if not a:return
			n["import"]=False
			try:
				d=Kit.data_path("_swing_timer_{}.txt".format(a))
				if not os.path.exists(d):return
				with open(d,"r")as f:g=f.read()
			except Exception:return
			h=bd(g,"\n");b=0
			for e,i in h.items():
				if not c.history.get(e):c.history[e]=i;b+=1
			if not b:return
			c.gaps_weapon=None;c.dirty=True;aL();at("brought over learned swings of %s from the old data file."%R(b,"weapon"),J)
		def aL():n["save"]=False;a=["%s|%d|%s"%(bb(h),p,",".join("%.0f"%t for t in b))for(h,p),b in sorted(c.history.items())if b];T(a6,";".join(a));c.dirty=False;n["saved_at"]=o()
		def bR(gap,formula):
			a=ba()
			if gap<a5 or gap>(a or formula)+3000:c.slow=[];return
			if a is not None and gap>a*1.15:
				c.slow.append(gap)
				if len(c.slow)<3:return
				c.gaps[:]=c.slow;c.slow=[];be("Slow: low stamina",aC)
			else:c.slow=[];c.gaps.append(gap)
			if len(c.gaps)>aB:del c.gaps[:-aB]
			c.dirty=True
		def aN(a):
			if c.paused_at is not None:
				if c.last_swing is not None:c.last_swing+=max(0.,a-c.paused_at)
				c.paused_at=a
			b=aJ();d=aq(int(API.Player.Stamina),b[1]);e=bc(b)
			if c.last_swing is not None and not e:bR(a-c.last_swing,d)
			c.last_swing=a;c.cycle_ms=ba()or d
		def bS(a):
			try:return max(0.,(DateTime.Now-a.Time).TotalMilliseconds)
			except Exception:return 0.
		def bT(a):
			b=int(a.ID)
			if b not in bI:return
			return(b,int(a.X),int(a.Y),str(a.Time),o()-bS(a))
		def bU(snd,p):
			e,a,b,f,g=snd
			if a!=int(p.X)or b!=int(p.Y):return
			d=(e,a,b,f)
			if d in c.seen_sounds:return
			c.seen_sounds.add(d)
			if len(c.seen_sounds)>200:c.seen_sounds.clear()
			aN(g)
		def bV(*e):
			if not d.get("active"):return
			for g in e:
				try:a=bT(g)
				except Exception:continue
				if a is not None and len(c.sounds)<50:
					c.sounds.append(a)
					if not f.get("fast"):
						b=f.get("xy")
						if b is None or(a[1],a[2])==b:HOST.poke()
				return
		bW=[False]
		def be(text,hue):c.notice=(text,hue,o()+4000.)
		Q={"rd":None,"clock":0.,"own":(L.lower(),)}
		def bX():
			a=set([L.lower()])
			for t in[APP_NAME]+[b.title for b in HOST.slots]:
				t=str(t or "").strip().lower()
				if t:a.add(t)
			return tuple(a)
		def bY():
			d=Q["own"]
			for a in Q["rd"].new(time.time()-Journal.read_at>=.5):
				b=a.low
				if b.startswith(d)or str(a.name or "").lower()not in bC:continue
				for e,c in((bA,("Disarmed!","You were disarmed")),(bB,("Dismounted!","You were dismounted"))):
					if any(g in b for g in e):be(c[0],aj);am(a7,c[1]);break
		bZ=[("simply too full to eat any more",20,20),("but you are stuffed",20,20),("but are still extremely hungry",0,4),("begin to feel more satiated",5,9),("you feel much less hungry",10,14),("feel quite full after consuming",15,19),];bf={"rd":None}
		def b_():
			e=bf["rd"]
			if e is None:bf["rd"]=Z();a=Journal.recent(a8)
			else:a=e.new()
			if not a:return
			try:f=float(DateTime.Now.Ticks)
			except Exception:f=time.time()*1e7
			for b in a:
				if b.ticks>1e12 and(f-b.ticks)/1e7>a8:continue
				h=b.low
				for i,g,d in bZ:
					if i in h:aO(max(g,min(d,c.hunger+3 if g!=d else d)));break
		def aO(value):aX[0]=True;c.hunger=float(max(0,min(20,value)));c.hunger_clock=o();u("swingtimer_hunger",c.hunger)
		def b0():
			b=o()-c.hunger_clock;a=a_*1000.
			if b>=a:d=int(b//a);c.hunger=max(0.,c.hunger-d);c.hunger_clock+=d*a;u("swingtimer_hunger",c.hunger)
		aP=" Alt+click: auto-follow (again to stop)"
		def F(what,value):
			if len(c.keys)<50:c.keys.append((what,value));HOST.poke()
		def b1(serial):
			if serial:c.target_serial=int(serial);c.enemy_override=None
		def b2():
			while c.keys:
				a,v=c.keys.pop(0)
				if a=="target":at("target the mobile you are fighting.");ae(10,b1)
				elif a=="resync":aN(v)
				elif a=="hunger":aO(round(c.hunger)+v)
				elif a=="enemy":b=bh();d=aK(b,c.enemy_override);c.enemy_override=max(ab,min(af,d+v))
				elif a=="follow":
					b=f.get("mob")
					if b is not None:X(int(b.Serial),L)
					else:at("no target to follow.")
		b3=((V,lambda:F("target",None),"pick the mobile you fight"),(ay,lambda:F("resync",o()),"restart the bar (I just swung)"),(az,lambda:F("hunger",1),"satiety estimate +1"),(aA,lambda:F("hunger",-1),"satiety estimate -1"),(a2,lambda:F("enemy",5),"enemy skill +5"),(a4,lambda:F("enemy",-5),"enemy skill -5"))
		def b4(fn):
			def a(*a):
				if not HOST.typing():fn()
			return a
		def bg(on):
			for a,b,c in b3:
				if on:HOST.hotkey_on(a,L,b4(b),c)
				else:HOST.hotkey_off(a,L)
		def bh():
			for a in(c.target_serial,API.LastTargetSerial):
				if a:
					m=API.FindMobile(a)
					if m and not m.IsDead:return m
			N=API.Notoriety;return API.NearestMobile([N.Gray,N.Criminal,N.Enemy,N.Murderer],2)
		I=A;b5={(False,False):400.,(False,True):200.,(True,False):200.,(True,True):100.};b6,b7=50.,800.;aR="swingtimer_kite";b8={"close":"#E8C25A","turn":"#3CD070","far":"#E04040","idle":"#C8C8C8"};b9={"close":N,"turn":J,"far":j,"idle":k};i={"on":bool(int(E(aR,1)or 0)),"steps":{},"xy":None,"at":0.,"stat0":None,"swing0":None,"px":None,"state":None,"tiles":None};s,Y=16,34;bi=3;U=max(0.,min(100.,E("swingtimer_bg_opacity",85)));aS={"f":None}
		def bj():return q(d["c"].get("gump"))
		def aT(hue,color,h):
			if M(Kit.LINE_BLUE)[0]>0:
				t=ao(d["c"]["gump"],Kit.LINE_BLUE,d["x1"],s,1,h,hue=hue)
				if t is not None:return t
			return O(d["c"]["gump"],d["x1"]+1,s+1,1,h,1.,color)
		def ca():d["row1"]=d["bar_w"]+5+max(z("15.0s"),a3());return d["row1"]+2*bi+16,58
		def cb(x=None,y=None):
			k=x is None
			if k:x=int(E("swingtimer_x",bs));y=int(E("swingtimer_y",bt))
			c=d["c"];o=c.get("gump");c.clear();m=M(Kit.LINE_RED)[0];g=M(Kit.LINE_BLUE)[1]or 8;d["bar_w"]=m or 109;w,h=ca();d["x1"]=f=8+bi
			if k:x,y=Kit.adapt(x,y,w,h)
			b=G.CreateGump(True,True);ai(b,x,y,w,h);c["gump"]=b;ag(b,w,h,corners=False);c["section"]=H(b,8,8,w-16,h-16);e["bg"][b]=[c["section"]];bn()
			if m>0:ax(b,Kit.LINE_RED,f,s)
			else:ao(b,aQ,f,s,109,9,1.)
			c["fills"]={"fill":aT(bu,bv,g),"ready":aT(bw,bx,g),"paused":aT(by,bz,g)}
			for p in c["fills"].values():p.IsVisible=False
			c["kite"]={}
			for q,r in b8.items():c["kite"][q]=t=O(b,f,s-1,2,g+2,1.,r);t.IsVisible=False
			c["kite_lbl"]=l(b,"",f,s-2,W);c["kite_lbl"].SetAcceptMouseInput(False);i.update({"px":None,"state":None,"tiles":None});c["swing"]=l(b,"",f+d["bar_w"]+5,s-2,W);c["notice"]=n=l(b,"",f+4,s-2,aj);n.SetAcceptMouseInput(False);n.IsVisible=False;c["hit"]=l(b,"",f,Y,aE);c["food"]=l(b,"",f+d["row1"]-z("Food 20/20"),Y,W);d["food_w"]=[aa("Food %d/20"%v)for v in range(21)];j=d["row1"]//2;c["tip_bar"]=D(b,f-2,s-4,d["row1"]+4,18,bk,bl(None),movable=True);c["tip_hit"]=D(b,f-2,Y-2,j,18,bk,aU(None),movable=True);c["tip_food"]=D(b,f+j,Y-2,d["row1"]-j+2,18,lambda*a:None,bm(),movable=True);d["fill_w"],d["fill_state"],d["shown"],d["tips"]=-1,None,{},{};d["notice_shown"]=None;G.AddControlOnDisposed(b,ci(b));G.AddGump(b);aD(b,aW);K(o)
		cw=None
		def au(key,text):
			c=d["c"].get(key)
			if c is None or d["tips"].get(key)==text:return
			d["tips"][key]=text;c.SetTooltip(text)
		def bk(*a):
			if ac():F("follow",None)
		def bl(info):
			a="Time to your next swing. Green: ready; grey: paused (no war mode or target)."
			if info is not None:b,c,d,n=info;a+=" %s, speed %d, swing %.1f s (%s)."%(b,c,d/1000.,"learned from %s"%R(n,"swing")if n else "formula")
			return a+aP
		def aU(info):
			if info is None:return "Chance to hit your target; set it with %s.%s"%(V,aP)
			a,b,c,d,e,f=info;return("Chance to hit %s: your %s %.1f vs their assumed %d, accuracy +%d%%, satiety %+d%%; set the target with %s.%s"%(a[:20],b,c,d,e,f,V,aP))
		def bm(label="",mod=0):return("Satiety estimate%s, %+d%% to hit: drops 1 every %d min, rises when you eat%s. Adjust: %s / %s."%((": "+label.lower())if label else "",mod,a_//60,""if aX[0]else " (none seen yet, so grey)",az,aA))
		def bn():d["c"]["section"].SetAlpha(U/100.*Kit.SECTION_ALPHA)
		def cc(i,state):
			a=int(d["bar_w"]*max(0,min(1000,i))/1000);c,e=d["fill_w"],d["fill_state"]
			if a==c and state==e:return
			d["fill_w"],d["fill_state"]=a,state;f=d["c"]["fills"];g=e if c>0 else None;b=state if a>0 else None
			if b is not None:ap(f[b],a)
			if g!=b:
				for h,j in((g,False),(b,True)):
					if h is not None:f[h].IsVisible=j
		def cd(p,t):
			a=(int(p.X),int(p.Y));b,h=i["xy"],i["at"]
			if a==b:return
			i["xy"],i["at"]=a,t
			if b is None:return
			c=max(abs(a[0]-b[0]),abs(a[1]-b[1]));e=t-h
			if not(0<c<=4 and 0<e<=700.*c):return
			f=max(b6,min(b7,e/float(c)));g=bo(p);d=i["steps"].get(g);i["steps"][g]=f if d is None else d+(f-d)*.15
		def bo(p):return(bool(p.IsMounted),bool(p.IsRunning))
		def ce(p):a=bo(p);v=i["steps"].get(a);return v if v is not None else b5[a]
		def cf(a,step):return int(1+(a/2.)/max(1.,step))
		def cg(dist,a):
			if dist is None:return "idle"
			return "close"if dist<a else("turn"if dist==a else "far")
		def ch(p,mob,cycle,stat,k):
			a=d["c"].get("kite")
			if not a:return
			h=d["c"].get("kite_lbl")
			if not i["on"]or c.notice is not None:
				if i["state"]is not None:a[i["state"]].IsVisible=False;i["state"]=None;i["tiles"]=None;A(h,"")
				return
			e=float(cycle)
			if i["swing0"]!=c.last_swing or i["stat0"]is None:i["swing0"],i["stat0"]=c.last_swing,stat
			elif stat!=i["stat0"]:
				l=aq(i["stat0"],k)
				if l>0:e=e*aq(stat,k)/float(l)
			m=max(.02,min(.98,(e/2.)/max(1.,float(cycle))));f=d["x1"]+int(d["bar_w"]*m);g=cf(e,ce(p));j=None
			if mob is not None:
				try:j=int(mob.Distance)
				except Exception:j=None
			b=cg(j,g)
			if b!=i["state"]:
				if i["state"]is not None:a[i["state"]].IsVisible=False
				a[b].IsVisible=True;i["state"]=b;i["px"]=None;i["tiles"]=None
			if f!=i["px"]:i["px"]=f;a[b].SetPos(f,s-1);h.SetPos(f+4,s-2)
			if g!=i["tiles"]:i["tiles"]=g;A(h,str(g),b9[b])
		def ci(g):
			def a(*a):
				if d["closing"]or d["c"].get("gump")is not g:return
				aW();d["c"].clear();aM("swing")
			return a
		def aW():
			g=d["c"].get("gump")
			if q(g)and not a1(av):u("swingtimer_x",g.GetX());u("swingtimer_y",g.GetY())
		aX=[False]
		def bp():return "{:.0f}/20 {}".format(c.hunger,aG(c.hunger)[1])
		def aY(a,b):return "%s / %s"%(a,b.rsplit("+",1)[1])
		cx={}
		def aZ(w):a=((aY(V,ay),"pick the target / restart the bar"),(aY(az,aA),"satiety estimate +1 / -1"),(aY(a2,a4),"enemy skill +5 / -5"));return(("WINDOW",(("gap",32),("check","kite","Show the kite marker on the bar","Turn-back point and tiles to kite out; colour: too close, turn now, too far",{"h":-32}),("slider","opacity","Background opacity:","How solid the window's black inside is (0-100)",0,100,{"lgap":12,"sdy":8,"sw":160})),{"sh":96,"ldy":4}),("HIT CHANCE",(("num","enemy","Enemy skill:","Skill assumed for an unknown monster; players count as GM (%d-%d)"%(ab,af),None,ab,af,{"lgap":8,"fw":44,"stay":True}),("slider","satiety","Satiety estimate:","How well fed you are, 0 (starving) to 20 (stuffed); low lowers the hit chance",0,20,{"dx":220,"lw":150,"sdy":8,"sw":120,"unit":bp()})),{"sh":68,"ldy":4}),("HOTKEYS",[h for b,g in a for h in(("note",b,{"stay":True}),("note",g,{"dx":330}))],{"sh":100}))
		cy=Kit.Page(B,aZ)
		def cj(w):return Kit.Form.height(aZ(w),w)
		def ck(g,x,y,w):aS["f"]=Kit.Form(g,x,y,w,{"kite":i["on"],"opacity":int(round(U)),"enemy":B["enemy_default"],"satiety":int(round(c.hunger))},aZ(w))
		def cl():aS["f"]=None
		def cm():
			nonlocal U;b=aS["f"]
			if b is None:return
			a,c=b.read(),b.vals;b.vals=a
			if a["opacity"]!=c["opacity"]:
				U=float(a["opacity"]);u("swingtimer_bg_opacity",U)
				if bj():bn()
			if a["enemy"]!=c["enemy"]:B["enemy_default"]=a["enemy"];bO();f["slow_clock"]=0.
			if a["satiety"]!=c["satiety"]:aO(a["satiety"])
			A(b.c["satiety_lbl"],bp())
			if a["kite"]!=i["on"]:i["on"]=a["kite"];u(aR,1 if a["kite"]else 0)
		f={}
		def cn():d["closing"],d["active"]=False,True;n.update({"saved_at":o(),"save":False});bP();del c.sounds[:],c.keys[:];c.last_swing=c.cycle_ms=c.notice=None;Q.update({"rd":Z(),"clock":0.,"own":bX()});ad(a7,"Disarmed or dismounted",946);c.hunger=max(0.,min(20.,E("swingtimer_hunger",a0)));c.hunger_clock=o();i["on"]=bool(int(E(aR,1)or 0));i["steps"].clear();i["xy"],i["stat0"],i["swing0"]=None,None,None;cb();aH(av,"target",0,lambda:d["c"].get("gump"));bg(True);aV(bW,0,("SoundPlayed",bV));f.update({"slow_clock":0.,"eat_clock":0.,"weapon":aJ(),"mob":None,"my_skill":0.,"mob_skill":aK(None,None),"mob_name":"","skill_of":None,"skill_clock":0.,"timer_clock":0.,"timer_mode":None,"fast":False,"react":None});at("on (%s picks the target, %s restarts the bar)."%(V,ay),J)
		def co():
			if not bj():f["fast"]=False;return
			t=o();p=an()
			if p is None:return
			while c.sounds:bU(c.sounds.pop(0),p)
			if c.keys:b2()
			if t-Q["clock"]>=100:Q["clock"]=t;bY()
			w=(c.target_serial,API.LastTargetSerial,bool(p.InWarMode))
			if w!=f["react"]:f["react"]=w;f["slow_clock"]=t-250
			if t-f["slow_clock"]>=250:
				f["slow_clock"]=t;f["xy"]=(int(p.X),int(p.Y));f["weapon"]=aJ();J=c.gaps_weapon
				if bc(f["weapon"]):
					c.cycle_ms=None
					if J is not None and f["weapon"][2]==AR:c.last_swing=None;aN(t)
				if c.dirty and t-n["saved_at"]>=5000:n["save"]=True
				a=f["mob"]=bh();x=(a.Name or "")if a is not None else "";f["mob_skill"]=aK(a,None,x);f["mob_name"]=(x or "target")if a is not None else ""
				if f["weapon"][2]!=f.get("skill_of")or t-f.get("skill_clock",0.)>=1000:f["skill_of"],f["skill_clock"]=f["weapon"][2],t;f["my_skill"]=al(f["weapon"][2])
				b0()
				if t-f["eat_clock"]>=1000:f["eat_clock"]=t;b_()
			y,l,z,q=f["weapon"];A=int(p.Stamina);g=c.gaps;K=sum(g)/float(len(g))if g else None;m=K or aq(A,l);a=f["mob"];h=bool(p.InWarMode)and a is not None
			if not h:
				if c.paused_at is None:c.paused_at=t
				B=c.paused_at
			else:
				if c.paused_at is not None:
					if c.last_swing is not None:c.last_swing+=t-c.paused_at
					c.paused_at=None
				B=t
			b=c.notice
			if b is not None and t>=b[2]:c.notice=b=None
			if c.last_swing is None:e,C,i=1000,0.,m
			else:i=c.cycle_ms or m;r=B-c.last_swing;C=i-r;e=1000 if r>=i else int(r/i*1000)
			cc(e,"paused"if not h else("ready"if e>=1000 else "fill"));cd(p,t);ch(p,a,i,A,l);f["fast"]=h and e<1000
			if b is not d["notice_shown"]:
				d["notice_shown"]=b;D=d["c"]["notice"]
				if b is not None:I(D,b[0],b[1])
				D.IsVisible=b is not None
			E=(h,e>=1000,a is None)
			if E!=f["timer_mode"]or t-f["timer_clock"]>=100:
				f["timer_mode"],f["timer_clock"]=E,t
				if not h:I(d["c"]["swing"],"Paused"if a is not None else "Ready",aE)
				elif e>=1000:I(d["c"]["swing"],"Ready",a9)
				else:I(d["c"]["swing"],"%.1fs"%(max(0.,C)/1000.),W)
			j=(y,l,"%.1f"%(m/1000.),len(g))
			if d["shown"].get("bar_tip")!=j:d["shown"]["bar_tip"]=j;au("tip_bar",bl((y,l,m,len(g))))
			F=d["shown"];s=f["my_skill"];u=c.enemy_override if c.enemy_override is not None else f["mob_skill"];j=(a is not None,f["mob_name"],u,s,z,q,c.hunger)
			if F.get("rows")!=j:
				F["rows"]=j;v=bK(s,u,q,c.hunger);G,L=aG(c.hunger)
				if a is not None:I(d["c"]["hit"],"Hit %d%%"%int(round(v*100)),a9 if v>=.6 else(aC if v>=.4 else aj));au("tip_hit",aU((f["mob_name"],z,s,u,q,G)))
				else:I(d["c"]["hit"],"Hit --%",aE);au("tip_hit",aU(None))
				H=max(0,min(20,int(round(c.hunger))))
				if I(d["c"]["food"],"Food %d/20"%H,k if not aX[0]else(aj if c.hunger<5 else(aC if c.hunger<10 else W))):ak(d["c"]["food"],d["x1"]+d["row1"]-d["food_w"][H],Y)
				au("tip_food",bm(L,G))
		def cp():
			if n["import"]and not d["closing"]:
				bQ()
				if not n["import"]:f["slow_clock"]=0.
			if n["save"]and c.dirty:aL()
			n["save"]=False
		def cq():return.025 if f.get("fast")else.1
		def cr():return bool(n["save"]or n["import"])
		def cs():
			d["closing"],d["active"]=True,False;bg(False);Q["rd"]=None
			if c.dirty:aL()
			aW();aI(av);u("swingtimer_bg_opacity",U);g=d["c"].get("gump");d["c"].clear();K(g)
		return{"start":cn,"tick":co,"stop":cs,"client_tick":True,"config_height":cj,"build_config":ck,"poll_config":cm,"config_closed":cl,"thread_tick":cp,"thread_wanted":cr,"interval":cq}
	def bc():
		h="bandage";P="Bandages";au="BandageAgent_pos";V=3617;av=15.;aw=7.5;ay=.5;E,I=1.,60.;W,aa=0.,5.;az=3.;r=1;aA=("you did not stay close enough to heal","you were unable to finish your work");bg=("that being is not damaged","you are too far away to do that","bandages can not be used on that","you cannot heal that","bandages cannot be used on that","that is too far away","that creature may only be healed")+aA;bh=("you finish applying the bandages","you apply the bandages, but they barely help","you apply the bandages, but they do not seem","you heal what little damage","you are able to resurrect","you are unable to resurrect","you have cured the target of all poisons");ab=50;aB,aC=0,99;bi,bj=400,300;aE=60.;aF=60.;aG=.6;aJ=10;af,aj=0,999;aN="bandage.low";aO="bandage.hp";aP="bandage.poison";aR="bandage.ready";aS=10;aT="BandageAgentStartPct";aU="BandageAgent_timing";aV="BandageAgent_extra";aW="BandageAgent_other";aX="#E8C25A";Q=62;s,bk=16,35;f=18;t=8;aY,aZ,a_=120,118,104;bl=aY+B+aZ+B+a_;d={"cure":True,"low":aJ,"others":False,"other_pct":80,"party":True,"pets":True};bQ=dict(d)
		def a0():b.update({"phase":"idle","shutting":False,"queue":[],"rebuild":False,"skills":(0.,0.,-1e9),"count":None,"count_at":0.,"low_armed":True,"hp_armed":True,"poison_armed":True,"target":None,"last":None,"pick":False,"begun":False,"by_buff":False,"buff":False,"lt":(0,0.)})
		b={"minimized":False,"shutting":False,"docked":False,"queue":[],"start_pct":ab,"band_time":av,"other_time":aw,"buffer":ay,"t0":0.,"deadline":0.,"rd":None};a0();c={"g":None,"c":{"fill":None,"fill_box":None,"label":None,"count":None},"store":({},{}),"bar_w":109,"fill_w":-1,"text":None,"count_text":None,"wide":False};bR,L,i=ah(b,P);n={"f":None,"typed":None,"applied":None,"since":0.}
		def a2():bn();bo();bp()
		def bm():a4();a5()
		def bn():
			try:b["start_pct"]=max(aB,min(aC,int(S(aT,str(ab)))))
			except Exception:b["start_pct"]=ab
		def a4():T(aT,str(b["start_pct"]))
		def bo():
			p=S(aU).split("|")
			try:
				if p[0]:b["band_time"]=max(E,min(I,float(p[0])))
				if len(p)>=2 and p[1]:b["buffer"]=max(W,min(aa,float(p[1])))
			except ValueError:b["band_time"],b["buffer"]=av,ay
			try:
				v=S(aW)
				if v:b["other_time"]=max(E,min(I,float(v)))
			except ValueError:b["other_time"]=aw
		def a5():T(aU,"%.2f|%.2f"%(b["band_time"],b["buffer"]));T(aW,"%.2f"%b["other_time"])
		def bp():v=dict(a.split("=",1)for a in S(aV).split(";")if "="in a);d["cure"]=v.get("cure","1")!="0";d["others"]=v.get("others","0")=="1";d["party"]=v.get("party")!="0";d["pets"]=v.get("pets")!="0";d["low"]=a6(v.get("low"),af,aj,aJ);d["other_pct"]=a6(v.get("opct"),1,99,80)
		def a6(text,lo,hi,default):
			try:return max(lo,min(hi,int(text)))
			except(TypeError,ValueError):return default
		def bq():T(aV,"cure=%d;low=%d;others=%d;opct=%d;party=%d;pets=%d"%(int(d["cure"]),d["low"],int(d["others"]),d["other_pct"],int(d["party"]),int(d["pets"])))
		def ak():
			if not a1(h):Kit.save_pos(au,c["g"])
		def br():a=M(Kit.LINE_RED)[0];i=M(Kit.LINE_BLUE)[0];b=a if a>0 and i>0 else 109;j=(max(z("15.0s"),a3())+(90 if d["others"]else 0));c=z("x999");e=b+5+j;g=f+t+c+t+f+t+f;h=max(e,g)+6;return{"bar_w":b,"count_w":c,"row1":e,"row2":g,"sec_w":h,"W":h+16}
		def a7():
			b=br();n=b["W"];z=M(Kit.LINE_RED)[0];A,B=M(Kit.LINE_BLUE);C=d["others"];x,y=Kit.load_pos(au,(bi,bj),(n,Q));m=c["g"]
			if q(m):x,y=m.GetX(),m.GetY()
			g=G.CreateGump(True,True);ai(g,x,y,n,Q);ag(g,n,Q,corners=False);e["bg"][g]=[H(g,8,8,b["sec_w"],Q-16)];g.SetTooltip("%s: one press, one bandage (x = bandages left)"%P);j=8+(b["sec_w"]-b["row1"])//2;i=c["c"];i["fill"]=i["fill_box"]=None;c["bar_w"]=b["bar_w"]
			if z>0 and A>0:ax(g,Kit.LINE_RED,j,s);i["fill"]=ao(g,Kit.LINE_BLUE,j,s,1,B);i["fill"].SetWidth(0)
			else:ao(g,aQ,j,s,109,9,1.);i["fill_box"]=O(g,j+1,s+1,1,7,1.,"#3A63A8")
			E=j+b["bar_w"]+5;i["label"]=l(g,"Ready",E,s-2,k);D(g,j-2,s-4,b["row1"]+4,18,bv,"Bandage in progress and its patient. Alt+click: auto-follow (again to stop)",movable=True);o=8+(b["sec_w"]-b["row2"])//2;h=bk;p=G.CreateGumpItemPic(V,f,f);p.SetPos(o,h);p.SetAcceptMouseInput(False);g.Add(p);D(g,o,h,f,f,L("me"),"Use one bandage on yourself");u=o+f+t;i["count"]=l(g,"",u,h+1,k);D(g,u,h,b["count_w"],f,lambda*a:None,"Bandages left in your backpack",movable=True);v=u+b["count_w"]+t;bt(g,v,h);D(g,v,h,f,f,bu,"Target someone within %d tile%s for one bandage. Alt+click: auto-follow (again to stop)"%(r,""if r==1 else "s"));w=v+f+t;bs(g,w,h);D(g,w,h,f,f,bw,"One more bandage on your last patient. Alt+click: auto-follow (again to stop)");c.update({"fill_w":-1,"text":None,"count_text":None,"wide":C,"g":g});G.AddControlOnDisposed(g,bx(g));G.AddGump(g);aD(g,ak);K(m);a9()
		bS=None
		def a8(g,x,y,art,ch):
			p=ax(g,art,x,y,hue=53,mouse=False)
			if p is None:l(g,ch,x+5,y+1,C);return False
			p.SetWidth(f);p.SetHeight(f);return True
		def bs(g,x,y):
			if not a8(g,x,y,8012,"@"):return
			O(g,x+8,y,10,7,1.,"#101010")
			for r in range(7):O(g,x+9,y+r,(3-abs(r-3))*2+1,1,1.,aX)
		def bt(g,x,y):
			if not a8(g,x,y,8012,"+"):return
			c=f//2
			for a,b,d,e in((c-1,0,2,5),(c-1,f-5,2,5),(0,c-1,5,2),(f-5,c-1,5,2),(c-1,c-1,2,2)):O(g,x+a,y+b,d,e,1.,aX)
		def an(o):
			a=ac()
			if a and o is not None:L(("follow",o["serial"]))()
			return a
		def bu(*a):
			if not an(b["last"]):L("other")()
		def bv(*a):an(b["target"]or b["last"])
		def bw(*a):
			if not an(b["last"]):L("again")()
		def bx(g):
			def a(*a):
				if c["g"]is g and not b["shutting"]:ak();c["g"]=None;aM(h)
			return a
		def a9():
			e=c["c"]["count"];n=b["count"]
			if e is None:return
			if n is None:a=("",k)
			else:f=d["low"];a=("x%d"%n,j if f>0 and n<f else k)
			if a!=c["count_text"]:c["count_text"]=a;A(e,a[0],a[1])
		def u(a,text,hue=None):
			a=max(0.,min(1.,a));w=int(c["bar_w"]*a);b=c["fill_w"]
			if w!=b:
				c["fill_w"]=w;d=c["c"]["fill"]
				if d is not None:
					ap(d,w)
					if(w>0)!=(b>0)or b<0:d.IsVisible=w>0
				elif c["c"]["fill_box"]is not None:ap(c["c"]["fill_box"],max(1,w-2))
			e=c["c"]["label"]
			if e is not None and(text,hue)!=c["text"]:c["text"]=(text,hue);A(e,text,k if hue is None else hue)
		def U(kind,text,level="warn"):am(kind,text,level)
		def by():
			a,c,e=b["skills"];d=time.time()
			if d-e>=5.:a,c=al("Healing"),al("Anatomy");b["skills"]=(a,c,d)
			return a>=aE and c>=aF
		def bz(p,hits,hmax):
			a=b["start_pct"]
			if a>0 and hmax>0:
				if hits*100./hmax<=a:
					if b["hp_armed"]:b["hp_armed"]=False;U(aO,"Your HP is at %d%%: bandage?"%int(hits*100./hmax))
				else:b["hp_armed"]=True
			if d["cure"]:
				if p.IsPoisoned:
					if b["poison_armed"]and by():b["poison_armed"]=False;U(aP,"Poisoned: a bandage can cure it")
				else:b["poison_armed"]=True
		def bA(now):
			if now<b["count_at"]:return
			b["count_at"]=now+2.;n=0
			for c in API.FindTypeAll(V,API.Backpack)or():n+=int(c.Amount or 1)
			e,b["count"]=b["count"],n;a=d["low"]
			if a>0 and n<a:
				if b["low_armed"]and(n>0 or(e or 0)>0):b["low_armed"]=False;U(aN,"No bandages left"if n<=0 else "Only %s left"%R(n,"bandage"))
			else:b["low_armed"]=True
			a9()
		def aq(m,px,py,reach):return max(abs(int(m.X)-px),abs(int(m.Y)-py))<=reach
		def ba(m):a=str(m.Name or "")or "them";b=a if len(a)<=aS else a[:aS-1]+".";return{"serial":int(m.Serial),"name":a,"short":b}
		def ar(p,now,target):
			if b["phase"]!="idle":i("a bandage is already running.");return
			if API.HasTarget("any")or Y(h):i("a target cursor is up (aim it or press Esc first).");return
			if p.IsDead:return
			a=API.FindType(V,API.Backpack)
			if not a:u(0.,"Out!",j);i("out of bandages!",j);return
			b["rd"].new();API.UseObject(a.Serial);b["count_at"]=min(b["count_at"],now+aG);aK(h,az);b["target"]=target;b["begun"],b["by_buff"]=False,False;b["phase"],b["deadline"]="cursor",now+az
		def bB(serial):
			b["pick"]=False
			if serial:L(("on",int(serial)))()
		def bb(p,now,serial):
			m=API.FindMobile(serial)
			if m is None:i("couldn't bandage them (out of sight).",j);return
			if int(p.Serial)==int(m.Serial):ar(p,now,None);return
			if m.IsDead:i("they are dead.",j);return
			if not aq(m,int(p.X),int(p.Y),r):i("too far away (%s at most)."%R(r,"tile"),j);return
			ar(p,now,ba(m))
		def bC(now):
			a=int(API.LastTargetSerial)
			if a!=b["lt"][0]:b["lt"]=(a,now)
		def bD(p,now):
			a,c=b["lt"]
			if not a:return
			with Kit.quiet:
				if a==int(p.Serial):return
				m=API.FindMobile(a)
				if m is None or not aq(m,int(p.X),int(p.Y),r+1):return
				if now-c<=4. or(p.Hits>=p.HitsMax and not p.IsPoisoned):return ba(m)
			return
		def bc(p,now,at,buff=False):
			a=b["phase"]=="heal"and not b["begun"]and not b["by_buff"]
			if b["phase"]=="cursor":F(h)
			if buff and b["phase"]=="heal":return
			if not a:b["target"]=bD(p,now)
			b["t0"]=min(now,at);b["phase"],b["begun"],b["by_buff"]="heal",not buff,buff;b["count_at"]=min(b["count_at"],now+aG)
		def bE(p,now):
			a=bool(API.BuffExists("Healing"));c,b["buff"]=b["buff"],a
			if a and not c:bc(p,now,now,True)
			elif c and not a and b["phase"]=="heal"and b["by_buff"]:return "done"
			return
		def bF(p,now):
			d=b["rd"].new()
			if not d:return
			e=P.lower()+":"
			for c in d:
				a=c.low.strip()
				if a.startswith(e):continue
				if c.name and str(c.name).lower()!="system":continue
				if a.startswith("you begin applying the bandages"):bc(p,now,c.at);continue
				if b["phase"]=="idle":continue
				f=b["phase"]=="cursor"or(not b["begun"]and now-b["t0"]<=2.)
				for x in bg:
					if a.startswith(x)and(f or x in aA):return a.rstrip(".!")
				if b["phase"]=="heal"and a.startswith(bh):return "done"
			return
		def bG(p,o):
			try:m=API.FindMobile(o["serial"]);a=m is not None and not m.IsDead and aq(m,int(p.X),int(p.Y),r)
			except Exception:a=False
			if not a:API.CancelTarget();i("%s is out of reach; cursor put down."%o["name"],j);return False
			API.Target(o["serial"]);b["last"]=o;i("bandaging %s."%o["name"]);return True
		def bH(action,p,now):
			if not b["pick"]and b["phase"]=="idle":b["pick"]=True;ae(15.,bB,h)
		def bI(action,p,now):
			if b["last"]is None:i("nobody bandaged yet; use the target icon first.")
			else:bb(p,now,b["last"]["serial"])
		def N(v):return("%.2f"%v).rstrip("0").rstrip(".")
		bd={"follow":lambda action,p,now:X(action[1],P),"me":lambda action,p,now:ar(p,now,None),"other":bH,"again":bI,"on":lambda action,p,now:bb(p,now,action[1])}
		def be(w):a=("On yourself:","On someone else:","Latency buffer:");b={"stay":True,"tw":50};c=("note","s",{"dx":82+max(z(g)for g in a),"ndy":4,"h":28});e=("Bandage: one on you. Target icon: one on whoever you click (within %d tile%s). Arrow: one more on the last one."%(r,""if r==1 else "s"));d=(int(E),int(I));return(("BANDAGE TIMES",(("text","time",a[0],"Seconds one on yourself takes; applied when you stop typing (%d-%d)"%d,b),c,("text","other",a[1],"Seconds one on someone else takes, much faster on this shard (%d-%d)"%d,b),c,("text","buffer",a[2],"Seconds added for latency before the bar says Done (%d-%d)"%(int(W),int(aa)),b),c),{"sh":aY,"align":True}),("ALERTS  (sound: Settings > Alerts)",(("num","box","Alert when your HP is at or under:","One alert per fall to this % or below (0-99, 0 = never)","%",aB,aC,{"clamp":False}),("check","cure","Alert when poisoned and a bandage can cure it","Once per poisoning, with Healing %d and Anatomy %d or more"%(int(aE),int(aF))),("num","low","Alert when bandages drop under:","One alert when your bandages drop under this (%d-%d, 0 = never)"%(af,aj),None,af,aj,{"clamp":False})),{"sh":aZ}),("WINDOW",[("check","others","Show who the bandage is on (a wider bar)","The bar names your patient. Alt+click the name: auto-follow (again to stop)")]+[("note",m,{"ndy":2})for m in Kit.wrap(e,w-24)[:2]],{"sh":a_}))
		bT=Kit.Page(d,be)
		def bJ(g,x,y,w):a=be(w);c=dict(d,time=N(b["band_time"]),other=N(b["other_time"]),buffer=N(b["buffer"]),box=b["start_pct"]);n.update({"f":Kit.Form(g,x,y,w,c,a,ldy=4,lgap=12,fw=40),"typed":None,"applied":None})
		def bf():n.update({"f":None,"typed":None,"applied":None})
		def bK(text,lo,hi):
			try:v=float(str(text).strip().replace(",","."))
			except(ValueError,TypeError):return
			return v if lo<=v<=hi else None
		def bL():
			f=n["f"]
			if f is None:return
			try:a=f.read(True)
			except Exception:bf();return
			f.vals=a
			if a["box"]!=b["start_pct"]:b["start_pct"]=a["box"];b["hp_armed"]=True;a4()
			if a["low"]!=d["low"]:b["count_at"]=0.
			c=False
			for k,h in(("cure","poison_armed"),("others","rebuild"),("low","low_armed")):
				if a[k]!=d[k]:d[k]=a[k];b[h]=True;c=True
			if c:bq()
			g=time.time();e=(a["time"],a["other"],a["buffer"])
			if e!=n["typed"]:n["typed"],n["since"]=e,g;return
			if n["applied"]==e or g-n["since"]<.7:return
			n["applied"]=e;c=False
			for i,(k,j,l)in enumerate((("band_time",E,I),("other_time",E,I),("buffer",W,aa))):
				v=bK(e[i],j,l)
				if v is not None and abs(v-b[k])>.001:b[k],c=v,True
			if c:a5()
		a2()
		def bM():
			a0();b["rd"]=Z();a2()
			for k,a,d in((aN,"Bandages running low",490),(aO,"HP low: bandage?",497),(aP,"Poisoned (a bandage cures)",480),(aR,"Bandage done",514)):ad(k,a,d)
			a7();aH(h,"player",0,lambda:c["g"]);i("on (%s s on you, %s s on others)."%(N(b["band_time"]),N(b["other_time"])),J)
		def bN():
			p=API.Player
			if p is None:return
			a=time.time()
			if b["queue"]or b["rebuild"]:
				if b["rebuild"]:
					b["rebuild"]=False
					if c["g"]is not None and c["wide"]!=d["others"]:a7()
				while b["queue"]:
					f=b["queue"].pop(0);m=f[0]if isinstance(f,tuple)else f
					if m in bd:bd[m](f,p,a)
				if c["g"]is None:return
			if p.IsDead:
				if b["phase"]!="idle":F(h)
				b["phase"],b["target"]="idle",None;u(0.,"Dead",j);return
			bA(a);r,n=p.Hits,p.HitsMax
			if n>0:bz(p,r,n)
			bC(a);e=bF(p,a);s=bE(p,a)
			if e is None:e=s
			if e is not None and e!="done"and b["phase"]!="idle":
				if b["phase"]=="cursor":F(h)
				b["phase"],b["target"]="idle",None;u(0.,"Ready");i("the bandage failed (%s)."%e,j);return
			if b["phase"]=="heal":
				o=b["target"];g=b["other_time"]if o is not None else b["band_time"];k=a-b["t0"]
				if k>=g+b["buffer"]or e=="done":b["phase"],b["target"]="idle",None;u(1.,"Done",J);U(aR,"Bandage done","info")
				else:
					l="%.1fs"%max(0.,g-k)
					if o is not None and c["wide"]:l="%s %s"%(o["short"],l)
					u(k/g,l,C)
				return
			if b["phase"]=="cursor":
				if aL(h,"beneficial"):
					o=b["target"]
					if o is None:API.TargetSelf();q=True
					else:q=bG(p,o)
					F(h)
					if q:b["phase"],b["t0"]="heal",a
					else:b["phase"],b["target"]="idle",None
				elif a>b["deadline"]:
					if API.HasTarget("beneficial"):i("a bandage cursor is up: press Esc or aim it.")
					else:i("no bandage cursor appeared.",j)
					F(h);b["phase"],b["target"]="idle",None
				return
			t=c["text"]
			if t is None or t[0]not in("Ready","Done","Out!")or(t[0]=="Out!"and(b["count"]or 0)>0):u(0.,"Ready")
		def bO():
			if b["phase"]=="cursor":return.01
			if b["phase"]!="heal":return.1
			a=b["other_time"]if b["target"]is not None else b["band_time"];return min(.1,max(.01,b["t0"]+a+b["buffer"]-time.time()))
		def bP():b["shutting"]=True;F(h);ak();aI(h);bm();g,c["g"]=c["g"],None;c["c"]["label"]=c["c"]["count"]=None;K(g)
		return{"start":bM,"tick":bN,"stop":bP,"client_tick":True,"config_height":lambda w:bl,"build_config":bJ,"poll_config":bL,"config_closed":bf,"interval":bO}
	def bd():
		h="pets";i="Pets";ar="Pets_settings";a5="Pets_pos";a6="Pets_min";W=440;at,a7=280,46;au=.25;av=1.;t={};ax=1.;a8,aB,aC=18,2,24;T=6;K=50;aD=130;aE=110;s=20;U=1;ab=10;ac=3.;a9=("the spell fizzles","your concentration is disturbed","insufficient mana","more reagents are needed","you must wait to perform another action");aH=3.;aI=(("follow","Follow me","all follow me"),("guard","Guard me","all guard me"),("stay","Stay","all stay"),("come","Come","all come"));af="all kill";ba=dict((bH,bI)for bH,bJ,bI in aI);aJ=(("pet_follow","Follow","%s follow me"),("pet_guard","Guard","%s guard"),("pet_stay","Stay","%s stay"));ag=dict([(bK,bL)for bK,bM,bL in aJ]+[("pet_kill","%s kill")]);M=(("","Bandage"),("Heal","Heal (spell)"),("Greater Heal","Greater Heal (spell)"));aM,aN="pets.low","pets.dead";bb="#17171a";bc,bd,be="#c22d2d","#2f9a3c","#d39a1c";aP="then pick the enemy with the shard's cursor (only on a click)";e={"range":a8,"low":30,"heal":0,"kill":False,"hidden":True};bF=dict(e)
		def aQ():a.update({"shutting":False,"docked":False,"queue":[],"heal":None,"confirm":None,"scan_at":0.,"look_at":0.,"note":"","full_at":0.,"note_until":0.,"order":[]})
		a={"minimized":False,"shutting":False,"docked":False,"queue":[],"followers":0,"fmax":0,"me":0,"note_hue":k,"cmd_at":{},"seq":0};aQ();d={"g":None,"c":{},"store":({},{}),"rows":[],"n_rows":-1,"room":T,"w":W};ai,q,bG=ah(a,i);b={};aR={"range":(aB,aC),"low":(0,99),"heal":(0,len(M)-1)}
		def aS():az(ar,";",e,aR)
		def aT():aA(ar,";",e,("range","low","heal","kill","hidden"),aR)
		def c(text,hue=None,secs=4.):a["note"],a["note_hue"]=text,k if hue is None else hue;a["note_until"]=time.time()+secs;Q()
		def aj(now):return bool(a["note"])and 0<=a["note_until"]-now<=10.
		def aU():return M[e["heal"]]
		def al(n):return R(n,"tile")
		def aV(serial,name,manual=False):a["seq"]+=1;r={"serial":serial,"name":name,"seq":a["seq"],"seen":0.,"where":"gone","pct":None,"stam":None,"dist":0,"dir":"","dead":False,"poison":False,"low":False,"manual":manual,"alive":False};b[serial]=r;a["order"]=[];return r
		def u(serial):
			if b.pop(serial,None)is not None:a["order"]=[]
		def O(r,m,px,py,now,near):
			if r["manual"]and r.get("own"):r["own"]=bool(m.IsRenamable)
			d=str(m.Name or "")
			if d:r["name"]=d
			j,f,k,g=int(m.Hits or 0),int(m.HitsMax or 0),int(m.Stamina or 0),int(m.StaminaMax or 0);r["pct"]=max(0,min(100,int(j*100//f)))if f>0 else None;r["stam"]=max(0,min(100,int(k*100//g)))if g>0 else None;c=bool(m.IsDead);r["poison"]=bool(m.IsPoisoned);h,i=int(m.X),int(m.Y);r["dist"]=max(abs(h-px),abs(i-py));r["dir"]=Kit.compass(h-px,i-py)or "here";r["where"]="near"if near else "far";r["seen"]=now
			if c and not r["dead"]and r["alive"]:aW(aN,"%s died"%(r["name"]or "A pet"),r["serial"])
			r["dead"]=c
			if c:r["low"]=True;return
			r["alive"]=True;a=e["low"];b=r["pct"]
			if b is not None:
				if a>0 and b<=a and not r["low"]:r["low"]=True;aW(aM,"%s at %d%% HP (%s)"%(r["name"]or "A pet",b,"here"if r["dist"]==0 else "%s %s"%(al(r["dist"]),r["dir"])),r["serial"])
				elif r["low"]and(a<=0 or b>=a+10):r["low"]=False
		def aW(key,text,serial):am(key,text,"warn",who=serial)
		def bf(p,now):
			i=int(p.Serial);g,h=int(p.X),int(p.Y);a["me"]=i;w=a["followers"];a["followers"],a["fmax"]=int(p.Followers or 0),int(p.FollowersMax or 0);f=set();j=False;l=e["range"];d=now>=a["full_at"]or a["full_at"]-now>av or a["followers"]!=w
			if not d:
				n=[x for x,y in b.items()if y["where"]=="near"]
				if len(n)<a["followers"]:d=True
			if not d:
				o=[]
				for k in n:
					try:
						m=aw(k)
						if m is None or int(m.Distance)>l:d=True;break
					except Exception:d=True;break
					o.append((k,m))
				if not d:
					for k,m in o:
						try:
							r=b.get(k)
							if r is None:continue
							if not r["manual"]and not m.IsRenamable:u(k);continue
							f.add(k);O(r,m,g,h,now,True)
						except Exception:continue
					q=()
			if d:
				a["full_at"]=now+av;q=HOST.mobiles(l)or[]
				if len(t)>400:t.clear()
			for m in q:
				try:
					if m is None:continue
					c=int(m.Serial)
					if c==i:continue
					r=b.get(c)
					if r is None:
						v=t.get(c)
						if v is not None and now<v:continue
						if not m.IsRenamable:t[c]=now+2.5;continue
						t.pop(c,None)
						if len(b)>=s:
							an(now,room=1)
							if len(b)>=s:continue
						r=aV(c,"")
					elif not r["manual"]and not m.IsRenamable:u(c);continue
					f.add(c);O(r,m,g,h,now,True)
				except Exception:continue
			for c,r in b.items():
				if c not in f and r["where"]=="near":j=True;r["where"]="far"
			if j or now>=a["look_at"]or a["look_at"]-now>ax:
				a["look_at"]=now+ax
				for c in[G for G in b if G not in f]:
					r=b[c];m=aw(c)
					if m is None:r["where"]="gone";continue
					try:
						if not r["manual"]and not m.IsRenamable:u(c);continue
						O(r,m,g,h,now,False)
					except Exception:continue
			an(now)
		def an(now,room=0):
			c=[g for g in b.values()if g["where"]=="gone"]
			if not c:return
			for e in c:
				if now-e["seen"]>1800.:u(e["serial"])
			d=s-room
			if a["fmax"]>0:f=len(b)-len([m for m in b.values()if m["where"]=="gone"]);d=min(d,max(a["followers"],f))
			if len(b)>d:
				c=sorted([n for n in b.values()if n["where"]=="gone"],key=lambda r:r["seen"])
				while c and len(b)>d:u(c.pop(0)["serial"])
		def bg():
			if not a["order"]or len(a["order"])!=len(b):a["order"]=sorted(b.values(),key=lambda r:r["seq"])
			return a["order"]
		def ao(g,store,items,a,e,f):
			x,y,b=a,e,1
			for h,i,c,j,k,l in items:
				d=35+z(c)
				if x>a and x+d>f:x,y,b=a,y+26,b+1
				if g is not None:P(g,store,h,i,x,y,c,j,hue=l,on_click=k)
				x+=d+12
			return b
		def aY():
			a=[("all_"+f,V if f=="stay"else I,g,"Say \"%s\" (all your pets in earshot)"%m,q(("all",f)),None)for f,g,m in aI]
			if e["kill"]:a.append(("all_kill",I,"Kill","Say \"%s\", %s"%(af,aP),q(("all","kill")),j))
			return a
		def bh(w):M=E;return 30+ao(None,None,aY(),M+10,0,w-M-10)*26+22
		def aZ():return W,2*E+30+2*B+bh(W)+30+K+2
		def bi():z=o.slot if aG(h)and not a["minimized"]else None;b,c=aZ();return z if z is not None and z[0]>=b and z[1]>=c else None
		def ap():
			M=E;f=bi();w=f[0]if f else W;d=w-2*M;F=aY();J=ao(None,None,F,M+10,0,M+d-10);s=30+J*26+22;t=2*M+30+2*B+s;L=o.rows(K,t+32,T)if f else T;p=min(L,len(b));N=f[1]-t if f else 30+max(1,p)*K+2;g,u,h=o.begin(w,t+N);O=[]
			if not a["minimized"]:
				o.frame(g);r=M+30+B;H(g,M,r,d,s,"ALL PETS  (said out loud)");ao(g,u,F,M+10,r+26,M+d-10);h["note"]=l(g,"",M+12,r+30+J*26-2,k);i=r+s+B;Q="YOUR PETS  (click to target)";H(g,M,i,d,N,Q);h["title_end"]=M+8+z(Q);v=M+d-10-35-z("Add...");P(g,u,"add",I,v,i+3,"Add...","List a pet of yours that isn't shown (this session)",on_click=q("add"));h["count"]=l(g,"",v-60,i+6,k);h["count_right"]=v-10;R=M+12+aD+8;aa=R+aE+10;S=aU();x=[(bH,bJ,bI,"Say \"%s\""%(ag[bH]%"<name>"))for(bH,bI,bK),bJ in zip(aJ,(I,I,V))];x.append(("heal",I,"Heal","Use one bandage on this pet (within %s)"%al(U)if not S[0]else "Cast %s on this pet (within %d tiles)"%(S[0],ab)))
				if e["kill"]:x.append(("pet_kill",I,"Kill","Say \"<name> kill\", "+aP))
				for X in range(p):
					m=i+30+X*K;c={"val":None,"prev":None,"changed":0.,"vis_hits":False,"vis_poison":False,"stam_on":False};c["name_lbl"]=l(g,"",M+12,m+3,C);y={}
					for ac,ad,bh,by in(("hits",bc,9,6),("poison",bd,9,6),("stam",be,3,16)):n=G.CreateGumpSimpleProgressBar(aE,bh,bb,ad,0,100);n.SetPos(R,m+by);n.SetAcceptMouseInput(False);g.Add(n);n.IsVisible=False;y[ac]=n
					c["bars"],c["stam_bar"]=y,y.pop("stam");c["info"]=l(g,"",aa,m+3,k);D(g,M+10,m,d-20,22,aX(c,q,"target"),"Click: aim your cursor at this pet, or make it your last target. Alt+click: auto-follow (again to stop)");Y=M+10
					for A,ae,Z,af in x:P(g,u,"%s%d"%(A,X),ae,Y,m+24,Z,af+". Alt+click: auto-follow (again to stop)",hue=j if A=="pet_kill"else None,on_click=aX(c,q,A));Y+=35+z(Z)+12
					O.append(c)
				h["empty"]=(l(g,"",M+12,i+33,k)if not p else None)
			o.end(g,{"rows":O,"n_rows":p,"count_w":None,"room":L,"w":w});a1(time.time())
		o=Kit.Window(h,i,a,d,ap,a5,a6,mini=(at,a7),icon=3713,cleanup=ai,lock=True,clear={"rows":[],"c":{},"n_rows":-1})
		def a_(row,key,ctrl,on):
			if row.get(key)!=on:row[key]=on;ctrl.IsVisible=on
		def a0(row,key,ctrl,v):
			if row.get(key)!=v:row[key]=v;ctrl.SetProgress(float(v),100.)
		def bj():
			if aj(time.time()):return a["note"],a["note_hue"]
			c=[f for f in b.values()if f["low"]and not f["dead"]and f["where"]!="gone"and f["pct"]is not None]
			if c:d=min(c,key=lambda r:r["pct"]);return "%s: %s %d%% HP"%(i,L(d["name"]or "pet",80),d["pct"]),j
			e=len([g for g in b.values()if g["where"]!="gone"])
			if not b:return "%s: none in view"%i,k
			return "%s: %s, %d in view"%(i,R(len(b),"pet"),e),k
		def Q():
			c=d["c"]
			if d["g"]is None or a["docked"]:return
			if a["minimized"]:
				b=c.get("status")
				if b is not None:t,e=bj();A(b,L(t,at-90),e)
				return
			b=c.get("note")
			if b is not None:f=aj(time.time());A(b,L(a["note"],d["w"]-2*E-24)if f else "",a["note_hue"])
		def a1(now):
			if d["g"]is None or a["shutting"]or a["docked"]:return
			if a["minimized"]:Q();return
			h=bg()
			if min(d["room"],len(h))!=d["n_rows"]:ap();return
			g=d["c"]
			for c,r in zip(d["rows"],h):
				Kit.row_set(c,(r["serial"],),now);i,l=r["where"],r["pct"]
				if r["dead"]or i=="gone":m=k
				elif r["low"]:m=j
				elif r["poison"]:m=J
				else:m=C
				A(c["name_lbl"],L(r["name"]or "(no name yet)",aD),m);e=None
				if i=="near"and not r["dead"]:e="poison"if r["poison"]else "hits";n="%s, %s"%("%d%%"%l if l is not None else "?%","here"if r["dist"]==0 else "%d %s"%(r["dist"],r["dir"]))
				elif r["dead"]and i!="gone":n="dead, %d %s"%(r["dist"],r["dir"])
				elif i=="far":n="far: %d %s"%(r["dist"],r["dir"])
				else:n=("out of range (%s)"%Kit.ago(now-r["seen"],Kit.AGO_SHORT)if r["seen"]else "out of range")
				A(c["info"],n,C if e else k)
				for v,u in c["bars"].items():a_(c,"vis_"+v,u,v==e)
				if e:a0(c,"p_"+e,c["bars"][e],l if l is not None else 0)
				p=r["stam"]if e else None;a_(c,"stam_on",c["stam_bar"],p is not None)
				if p is not None:a0(c,"p_stam",c["stam_bar"],p)
			o=g.get("count")
			if o is not None:
				if a["fmax"]>0:f="%d / %d slots"%(a["followers"],a["fmax"])
				else:f="%d known"%len(b)if b else ""
				if len(h)>d["room"]:
					t=("%d more, %s"%(len(h)-d["room"],f)).rstrip(", ")
					if g["count_right"]-aa(t)>=g["title_end"]+8:f=t
				A(o,f);q=aa(f)if f else 0
				if d["count_w"]!=q:d["count_w"]=q;ak(o,g["count_right"]-q,Kit.ui_y(o))
			s=g.get("empty")
			if s is not None:
				if a["followers"]>0:A(s,"%s used, none in view. Add... lists one."%R(a["followers"],"slot"))
				else:A(s,"No pets in view. Click Add... to list one.")
			Q()
		def a2(action,p,now):
			if not e["hidden"]:return True
			if not p.IsHidden:a["confirm"]=None;return True
			b=a["confirm"]
			if b is not None and b[0]==action and b[1]<=now<=b[2]:a["confirm"]=None;return True
			a["confirm"]=(action,now+.3,now+aH);c("That reveals you: click again to do it.",N,aH);return False
		def bk(text,now):
			b=a["cmd_at"].get(text)
			if b is not None and 0<=now-b<.6:return
			if len(a["cmd_at"])>50:a["cmd_at"].clear()
			a["cmd_at"][text]=now;API.Msg(text);c("Said \"%s\"."%text)
		def bl(serial):
			r=b.get(serial)
			if r is None or not r["name"]:c("That pet has no name yet.",j);return
			return r["name"]
		def bm(serial):
			if API.HasTarget("any")and not Y(h):
				if not aO(serial,"hud.pets",i):return
				API.Target(serial)
				if a["heal"]is not None:a["heal"]=None;F(h)
				return
			API.SetLastTarget(serial=serial);API.HeadMsg("* last target *",serial,53)
		def a3(m,p):return max(abs(int(m.X)-int(p.X)),abs(int(m.Y)-int(p.Y)))
		def bn(serial,p,now):
			r=b.get(serial);e=(r and r["name"])or "that pet"
			if a["heal"]is not None:c("A heal is already on its way.",N);return
			if p.IsDead:c("You are dead.",j);return
			if API.HasTarget("any")or Y(h):c("A target cursor is up: aim it or press Esc first.",N);return
			d,n=aU();f=ab if d else U;m=API.FindMobile(serial)
			if m is None:c("%s is out of range."%e,j);return
			k=a3(m,p)
			if k>f:c("%s is %d tiles away (%s reaches %d)."%(e,k,n.lower(),f),j);return
			if not a2(("heal",serial),p,now):return
			if d:API.CastSpell(d);g=aF(d)[3]+ac
			else:
				l=API.FindType(3617,API.Backpack)
				if not l:c("Out of bandages.",j);API.SysMsg("%s: out of bandages!"%i,j);return
				API.UseObject(l.Serial);g=ac
			aK(h,g);a["heal"]={"serial":serial,"name":e,"until":now+g,"reach":f,"what":d or "a bandage","t0":now,"rd":Z()};c("%s for %s..."%(d or "Bandage",e))
		def bo(p,now):
			b=a["heal"];d=False;e=b["what"][0].upper()+b["what"][1:]
			for f in b["rd"].new():
				for x in a9:
					if x in f.low:d=True;break
				if d:break
			if d:a["heal"]=None;F(h);c("%s for %s failed."%(e,b["name"]),j);return
			if HOST.cursor_claim[0]==h and aL(h,"beneficial"):
				m=API.FindMobile(b["serial"]);a["heal"]=None;F(h)
				if m is not None and a3(m,p)<=b["reach"]:API.Target(b["serial"]);c("%s on %s."%(e,b["name"]),J)
				else:API.CancelTarget();c("%s moved out of reach."%b["name"],j)
				return
			if not 0<=b["until"]-now<=ac+10.:
				a["heal"]=None;F(h)
				if API.HasTarget("any"):c("A target cursor is up: aim it or press Esc.",N)
				else:c("No target cursor came for %s."%b["name"],j)
		def bp(serial):q.add(("added",int(serial or 0)),dup=True)
		def bq(serial,p,now):
			if not serial:return
			if serial==a["me"]or serial==int(p.Serial):c("That's you.",j);return
			m=API.FindMobile(serial)
			if m is None:c("That isn't a creature in view.",j);return
			r=b.get(serial)
			if r is None:
				if len(b)>=s:an(now,room=1)
				if len(b)>=s:c("The list is full (%d)."%s,j);return
				r=aV(serial,"",manual=True)
			r["manual"]=True;r["own"]=bool(m.IsRenamable);O(r,m,int(p.X),int(p.Y),now,True)
			if r["dist"]>e["range"]:r["where"]="far"
			c("%s is listed for this session."%(r["name"]or "It"),J)
		def br(action,p,now):ae(10.,bp);c("Target the pet to list.")
		def a4(action,p,now):
			b=action[0]
			if(action[1]=="kill"if b=="all"else b=="pet_kill")and not e["kill"]:return
			if b=="all":a=af if action[1]=="kill"else ba.get(action[1])
			else:a=bl(action[1]);a=a and ag[b]%a
			if a and not bs(p)and a2(action,p,now):bk(a,now)
		def bs(p):
			if p.IsDead:c("You are dead: your pets can't hear you.",j);return True
			return False
		bt=("add","follow");aq={"add":br,"follow":lambda action,p,now:X(action[1],i),"added":lambda action,p,now:bq(action[1],p,now),"target":lambda action,p,now:bm(action[1]),"heal":lambda action,p,now:bn(action[1],p,now),"all":a4};aq.update((bN,a4)for bN in ag);bu=("One heal per click, aimed at the pet when its cursor comes (bandage within %s, spell within %d)."%(al(U),ab));bv="Said only on a click; the shard's cursor then picks the enemy."
		def bw(w):a,b=([("note",g)for g in Kit.wrap(f,w-28)]for f in(bu,bv));return(("WINDOW",(("num","range","List pets within:","How far a pet is listed with its bars","tiles",aB,aC),("check","hidden","While hidden, a command or a heal needs a second click","Speaking and healing reveal you; the first click only asks"))),("HEAL BUTTON  (on each pet's row)",[("note","Heal with:",{"ndy":4,"h":28,"hue":C})]+a),("COMBAT COMMANDS",[("check","kill","Show Kill buttons (\"%s\" and \"<name> kill\")"%af,"One for all pets and one per pet row",{"h":28})]+b),("ALERTS  (sound: Settings > Alerts)",(("num","low","Alert when a pet's HP falls to:","One alert per fall to this % or below (0-99, 0 = never)","%",0,99),)))
		def bx(f,new):
			i=Kit.dd_index(f.c["heal"],-1)
			if 0<=i<len(M):new["heal"]=i
		def by(b,new):
			if new["hidden"]!=b["hidden"]:a["confirm"]=None
			if(new["kill"],new["heal"])!=(b["kill"],b["heal"])and d["g"]is not None:q("redraw")()
		S=Kit.Page(e,bw,aT,by,{"ldy":4,"lgap":12,"fw":44,"pad":6},strict=True,adjust=bx)
		def bz(g,x,y,w):f=S.build(g,x,y,w);a=G.CreateDropDown(200,[m for n,m in M],e["heal"]);a.SetPos(x+22+z("Heal with:"),y+90+B+30);g.Add(a);f.c["heal"]=a;a.SetTooltip("What each row's Heal button uses")
		aS()
		def bA():
			aQ();a["minimized"]=o.start_min();aS()
			for r in b.values():r["where"]="gone"if r["where"]=="gone"else "far"
			ad(aM,"Pet HP low",821);ad(aN,"Pet died",497);ap();o.dock(fit=True,min=aZ);ai.service("pets.list",bB)
		def bB(distance=None):
			if a["shutting"]:return
			c=e["range"]
			if distance is None:distance=c
			if distance>c:return
			return[g for g,f in b.items()if f["where"]=="near"and(not f["manual"]or f.get("own"))and f["dist"]<=distance]
		def bC():
			if d["g"]is None:return
			if ay(d):return
			b=time.time();p=API.Player
			while a["queue"]:
				c=a["queue"].pop(0);e=c[0]if isinstance(c,tuple)else c
				if not(o.action(c)or p is None and e not in bt)and e in aq:aq[e](c,p,b)
				if d["g"]is None:return
			if p is None:return
			if a["heal"]is not None:bo(p,b)
			if b>=a["scan_at"]or a["scan_at"]-b>au:a["scan_at"]=b+au;bf(p,b);a1(b)
			elif a["note"]and not aj(b):a["note"]="";Q()
		def bD():return.02 if a["heal"]is not None else.1
		def bE():a["shutting"]=True;a["heal"]=None;F(h);aT();ai.close()
		return{"start":bA,"tick":bC,"stop":bE,"client_tick":True,"config_height":S.height,"build_config":bz,"poll_config":S.poll,"config_closed":S.closed,"interval":bD}
	be=(("frames",a9,.1,"unitframes"),("timers",ba,.1,"spelltimers"),("swing",bb,.025,"swing"),("bandage",bc,.1,"bandage"),("pets",bd,.1,"pets"),);return PartSet(a4,a5,be).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("hud","Character HUD","Frames, timers and bars for you and pets",_module_hud,.025,category="On screen",parts=(("frames","Frames","Health frames: you, target, party",True,("unitframes",)),("timers","Buffs & Timers","Timed buffs, debuffs and your spells",True,("spelltimers",)),("swing","Swing Bar","When your next melee swing lands",False,("swing",)),("bandage","Bandages","One-press bandage, timer and alerts",False,("bandage",)),("pets","Pets","Pets' health, distance and commands",False,("pets",)),),aliases=('Unit Frames','Spell Timers','Swing Timer','Bandage Agent','Pets','cast bar','buffs','debuffs','party frames','hit chance'))
