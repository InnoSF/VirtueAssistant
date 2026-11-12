def _module_hud():
	Y=Client._member;A=Client._type;F=Follow.alt_held;B=Follow.toggle;M=HOST.alert;H=HOST.alert_kind;I=HOST.booting;Z=HOST.claim_cursor;C=HOST.cursor_busy;aa=HOST.cursor_ok;ab=HOST.disable;ac=HOST.dock_remove;ad=HOST.harm_ok;N=HOST.me;U=HOST.mobile;J=HOST.pick_target;K=HOST.refresh_settings;l=HOST.release_cursor;ae=HOST.settle_hold;D=Journal.reader;O=Journal.said;al="hud";am="Character HUD";e={"anchor":{},"piece":{},"tied":{},"span":{},"inner":{},"bg":{},"bare":{},"stack":{},"dirty":True,"full_at":0.,"sig":None,"objs":None,"inside":[],"want":{}};af=.5;P=42;Q={500007:"you are no longer frozen",500119:"you must wait to perform another action",500231:"you feel cured of poison",500295:"you are too far away to do that",500641:"your concentration is disturbed",500916:"you apply the bandages, but they do not seem",500951:"you cannot heal that",500954:"that creature may only be healed",500955:"that being is not damaged",500956:"you begin applying the bandages",500957:"you begin applying the bandages",500958:"you begin applying the bandages",500959:"you begin applying the bandages",500960:"you begin applying the bandages",500962:"you were unable to finish your work",500963:"you did not stay close enough to heal",500964:"you did not stay close enough to heal",500965:"you are able to resurrect",500966:"you are unable to resurrect",500967:"you heal what little damage",500968:"you apply the bandages, but they barely help",500969:"you finish applying the bandages",500970:"bandages cannot be used on that",501604:"incognito cannot be cast",501775:"this spell is already in effect",501816:"you are too far away to do that",501857:"this spell won't work on that",502136:"the poison seems to have worn off",502349:"this target already has reactive armor",502381:"you cannot move!",502382:"you can move!",502625:"insufficient mana",502630:"more reagents are needed",502632:"the spell fizzles",503252:"you were unable to finish your work",503253:"you did not stay close enough to heal",503254:"you did not stay close enough to heal",503255:"you are able to resurrect",503258:"you heal what little damage",503259:"you apply the bandages, but they barely help",503260:"you finish applying the bandages",503261:"bandages cannot be used on that",1005382:"the spell will not adhere to you",1005383:"the spell will not adhere to you",1005384:"you currently have a reactive armor spell",1005385:"the spell will not adhere to you",1005416:"you currently have a reflect spell",1005417:"this spell is already in effect",1005545:"the spell will not adhere to you",1005546:"you currently have a reflect spell",1005547:"the spell will not adhere to you",1005548:"you currently have a reactive armor spell",1005549:"the spell will not adhere to you",1005550:"your protection spell has been nullified",1005552:"the spell will not adhere to you",1005553:"you currently have a reflect spell",1005554:"the spell will not adhere to you",1005555:"the spell will not adhere to you",1005556:"your reactive armor spell has been nullified",1005557:"you currently have a reflect spell",1005559:"this spell is already in effect",1005603:"you can move again!",1008072:"you have been cured of all poisons",1010058:"you have cured the target of all poisons",1010059:"you have been cured of all poisons",1010398:"you cannot heal that",1010406:"you cannot heal that",1010445:"you cannot incognito",1010648:"you have cured the target of all poisons",1010649:"you have been cured of all poisons",1042857:"you feel a bit nauseous",1042858:"looks ill",1042859:"you feel disoriented and nauseous",1042860:"looks extremely ill",1042861:"you begin to feel pain throughout your body",1042862:"stumbles around in confusion and pain",1042863:"you feel extremely weak and are in severe pain",1042864:"is wracked with extreme pain",1042865:"you are in extreme pain, and require immediate aid",1042866:"begins to spasm uncontrollably",1042867:"looks extremely ill",1042868:"stumbles around in confusion and pain",1042869:"is wracked with extreme pain",1042870:"begins to spasm uncontrollably",1045157:"you must wait to perform another action",1061091:"you cannot cast that spell in this form",1061654:"you cannot heal that",3000201:"you must wait to perform another action"}
	def R(a,below):
		s=e["stack"].get(a)
		if s is None or s[0]!=below:return 0
		return max(0,int(s[1]))
	def ag(a,getter,span=None,inner=None):
		e["dirty"]=True
		if getter is None:
			e["anchor"].pop(a,None);e["span"].pop(a,None);e["inner"].pop(a,None);e["want"].pop(a,None)
			for b,(c,d,f)in list(e["piece"].items()):
				if c==a:S(b)
		else:e["anchor"][a]=getter;e["span"][a],e["inner"][a]=span,inner
	def V(a,b,order,getter):e["piece"][a]=(b,int(order),getter);e["dirty"]=True
	def W(a):e["piece"].pop(a,None);e["dirty"]=True;S(a)
	def S(a):
		b=e["tied"].pop(a,None);g=None
		if b is not None:Kit.detach(b[0]);g=b[0]
		elif a in e["piece"]:g=e["piece"][a][2]()
		c=e["bare"]
		if g is None or not c or not c.pop(g,False)or not Kit.is_open(g):return
		Kit.frame_show(g,True)
		for d in e["bg"].get(g)or():Kit.set(d,"IsVisible",True)
	def q(b):a=e["anchor"].get(b);g=a()if a is not None else None;return g if Kit.is_open(g)and g.IsVisible else None
	def ah(a,since,cap):b=e["want"].get(a);return(b is not None and q(a)is None and I()and time.time()-since<cap and b())
	def ai(a):p=e["piece"].get(a);return p is not None and q(p[0])is not None
	z={"at":0.,"uim":None,"off":False,"same":None}
	def aj(j):
		if z["off"]:return
		e=time.time()
		if e<z["at"]:return
		z["at"]=e+.25
		try:
			if z["uim"]is None:import System;z["same"]=System.Object.ReferenceEquals;z["uim"]=Tz.T("ClassicUO.Game.Managers.UIManager")
			f,g=z["uim"],z["same"];k=Tz.get(None,"Gumps",f);c=Kit.mouse_pos()
			for l,h in j:
				if c is not None:
					a=E(h)
					if a is not None and a[0]<=c[0]<a[0]+a[2]and a[1]<=c[1]<a[1]+a[3]:continue
				d,i=Kit._raw_gump(l),Kit._raw_gump(h)
				if d is None or i is None:continue
				b=k.First
				while b is not None:
					v=b.Value
					if g(v,d):break
					if g(v,i):Tz.call(None,"MakeTopMostGump",[d],f);break
					b=b.Next
		except Exception:z["off"]=True
	def E(g):r=Kit.rect(g);return r if r is not None and r[2]>0 and r[3]>0 else None
	def an(sw,sh):
		b=[sw,sh];c=[]
		for j,(a,k,l)in e["piece"].items():b.append((j,a,k));c.append(l())
		for a in e["anchor"]:
			d=q(a);r=f=g=None
			if d is not None:r=E(d);h,i=e["span"].get(a),e["inner"].get(a);f=h()if h is not None else None;g=i()if i is not None else None
			b.append((a,r,f,g));c.append(d)
		return b,c
	def X():
		w,z=Kit.screen();A=time.time();J,p=an(w,z)
		if not e["dirty"]and A<e["full_at"]and A+2*af>e["full_at"]and J==e["sig"]:
			B=e["objs"];C=B is not None and len(B)==len(p)
			if C:
				for K in range(len(p)):
					if p[K]is not B[K]:C=False;break
			if C:
				if e["inside"]:aj(e["inside"])
				return
		e["sig"],e["objs"]=J,p;e["dirty"]=False;e["full_at"]=A+af;L={};k=[];D={}
		for a,(b,M,l)in e["piece"].items():D.setdefault(b,[]).append((M,a,l))
		for b in[at for at in e["stack"]if at not in D]:e["stack"].pop(b,None)
		for b,F in D.items():
			f=q(b)
			if f is None:
				for X,a,_g in F:S(a)
				e["stack"].pop(b,None);continue
			N=E(f)
			if N is None:e["dirty"]=True;continue
			m,h,r,G=N;s=z<=0 or(h+G/2.)<z/2.;O,Q=e["span"].get(b),e["inner"].get(b);c=O()if O is not None else None;t=Q()if Q is not None and c is not None else None;R=None;F.sort();y=h+G if s else h
			for X,a,l in F:
				g=l()
				if not Kit.is_open(g):S(a);continue
				L[a]=g
				if not g.IsVisible:continue
				T=E(g)
				if T is None:e["dirty"]=True;continue
				Y,Z,d,U=T;u=None
				if t is not None and R is None and d<r:
					i=Kit.MARGIN;H,iw,ih,ay,ah=t[:5];v=(c[0]-i)if c[2]else(c[1]-d+i);V=(t[5]if len(t)>5 else ay+ah)+Kit.GAP-i;v=max(H-i,min(v,iw-H-d+i))
					if V+i+P<=ih-H+2 and v>=0:u,R=(m+v,h+V),1
				if u is not None:x,n=u;k.append((g,f))
				elif c is not None and d<r:x=m+(c[1]-d if c[2]else c[0]);x=max(m,min(x,m+r-d))
				else:x=m+(r-d)//2
				if u is None:
					if w>0:x=max(0,min(x,w-d))
					if s:n,y=y,y+U
					else:y-=U;n=y
				if(Y,Z)!=(x,n):g.SetPos(x,n);Kit.note_rect(g,x,n);Kit.moved_by_code(g)
				j=e["tied"].get(a)
				if j is None or j[0]is not g or j[1]is not f:
					if j is not None and j[0]is not g:Kit.detach(j[0])
					Kit.attach(g,f);e["tied"][a]=(g,f)
			e["stack"][b]=(s,(y-(h+G))if s else(h-y))
		I=e["bare"];aa=set(ax for ax,az in k)
		for W in(I,e["bg"]):
			for g in[aA for aA in W if not Kit.is_open(aA)]:W.pop(g,None)
		for a,(b,M,l)in e["piece"].items():
			g=L.get(a)
			if g is None:g=l()
			if not Kit.is_open(g):continue
			o=g in aa
			if I.get(g,False)!=o:
				I[g]=o
				if o:Kit.pin_size(g)
				Kit.frame_show(g,not o)
				for ab in e["bg"].get(g)or():Kit.set(ab,"IsVisible",not o)
		e["inside"]=k
		if k:aj(k)
	T={"fn":None};ao=("Ready","Done","Out!","Dead","Paused")
	def ak():return max(Kit.text_w(a)for a in ao)
	def j(name,serial,noto=None,me=False):a=Kit.noto_mark(noto)if noto else "";return(a+" "if a else "")+(Kit.veil("me",name)if me else Kit.veil("name",name,serial))
	def L(name,default=0.):
		try:return float(API.GetSkill(name).Value or 0)
		except Exception:return default
	def ap():
		H="unitframes";ak="Frames";bu="UnitFrames_settings";cD="UnitFrames_pos";cE="UnitFrames_min";bv=("hits","mana","stam");bw="#17171a";cF={"hits":"#c22d2d","poison":"#2f9a3c","yellow":"#cfae2a","mana":"#2f62cc","stam":"#d39a1c"};a0={"innocent":(46,104,214),"ally":(40,160,70),"gray":(120,120,126),"criminal":(120,120,126),"enemy":(222,118,30),"murderer":(196,38,38),"invulnerable":(214,178,40)};M=(226,226,230);cG={1:"innocent",2:"ally",3:"gray",4:"criminal",5:"enemy",6:"murderer",7:"invulnerable"};aG=(0,0,8);bx,by=50000,60000;cH={400:12,402:12,401:13,403:13,605:14,607:14,606:15,608:15,666:666,694:666,667:665,695:665,1253:51253,987:12};cI=(401,403,606,608,667,695);cJ,cK=987,1002;bz=("cloak","shirt","arms","torso","tunic","face","robe","neck","hair","beard","earrings","helmet");cL=("shirt","arms","torso","tunic","face","robe","cloak","neck","hair","beard","earrings","helmet");cM=("shirt","arms","torso","tunic","cloak","face","neck","hair","beard","earrings","helmet","robe");cN=(41674,41675);a1=(39301,39302,42002,41675,41674);cO=(5136,5143);bA=110;aM=2.;bB=.008;L="vauf_";cP=3.;cQ=.04;cR=64;cS=4;aN=12;ab,ac,bC=50,150,70;al=14;bD=10;V=100;bE="UnitFrames_tracked";bF="UnitFrames_framepos";bG=350;bH=(4017,4018,4017);bI=3;cT,cU=240,46;a2=.4;bJ=.05;am=SNAP_DIST;an=24;ao=2;bK=1.5;cV=10.;cW=.025;cX={"cast":"#cfae2a","done":"#2f9a3c","fail":"#c22d2d"};cY=(("the spell fizzles","fizzled"),("your concentration is disturbed","disturbed"),("insufficient mana","no mana"),("more reagents are needed","no reagents"));cZ=Kit.SPELL_WORDS;aO=Kit.text_px;ay,ap=502,194;az=(96.5,96.5);aP=52.5;a3=((86.,(22,22,24)),(81.5,(226,226,230)),(79.5,"tire"),(64.5,(30,25,10)),(61.5,(226,226,230)),(60.5,"gold"),(53.5,(14,10,2)));aH=(78.,83.5);E=(150.,39.5,491.5,154.5,9.);bL=(153.,42.6,488.,151.,6.5);bM=(178.5,47.5,476.5,146.,8.);bN=(183.5,51.5,472.5,141.5,6.);bO=((77.5,83.5),(109.5,115.5));bP=((483.5,45.8,(188,188,193)),(483.5,148.6,(128,128,133)));bQ,bR=(20,20,22),(16,16,18);bS=(182,474);c_=((51,79),(83,111),(115,143));bT=.70710678;a4=(APP_VERSION,ay,ap,az,aP,a3,aH,E,bL,bM,bN,bO,bP,bQ,bR,aG);l={"player":True,"target":True,"hide_empty":False,"numbers":True,"lock":False,"click":True,"party":False,"ignore_self":True,"attack":False,"status":True,"scale":bC,"pdx":0,"pdy":0,"pscale_on":False,"pscale":bC,"pzoom":100,"mirror":False,"sup_open":False,"sup_deep":True,"sup_hide0":False,"sup_follow":True,"sup_low":10,"sup_side":0,"cast":True,"guard":True,"hide_bar":True};bU=dict(l);aQ={"scale":(ab,ac),"pscale":(ab,ac),"pdx":(-60,60),"pdy":(-60,60),"pzoom":(50,200),"sup_low":(0,9999),"sup_side":(0,2)}
		def bV():i.update({"shutting":False,"queue":[],"rebuild":False,"docked":False,"target":0,"next_party":0.,"snaps":{},"stale":set(),"snap_queue":[],"art_scales":set(),"snap_px":None,"party":set(),"snap_job":None,"art_jobs":[],"art_failed":set(),"recent":[],"next_prune":0.,"art_dirty":True,"snap_tries":{},"guard":None,"next_guard":0.,"jr":None,"dismissed":set(),"removing":False,"full_at":0.,"mirror_now":False,"pos_save_at":0.,"snap_keys":{},"art_wait":False})
		i={"minimized":False,"shutting":False,"docked":False,"queue":[],"me":0,"names":{},"pos":{},"next_save":0.,"pos_dirty":False,"crop_changed":0.,"art":None,"textures":set(),"running":False};bV();q=[];aA={"sig":None,"at":None};m={"g":None,"c":{},"spell":None,"start":0.,"secs":1.,"state":None,"until":0.,"pct":0,"word":"","shown":None,"at":None,"leader":None,"s":None,"w":0};o={};aR={"g":None,"c":{},"store":({},{})};aq,W,z=Kit.basics(i,ak);t={"store":({},{}),"next_preview":0.,"layers":None};bW={};a5,aS=Kit.get_var,Kit.put_var
		def bX():Kit.kv_load(bu,",",l,aQ)
		def a6():Kit.kv_save(bu,",",l,sorted(bU),aQ)
		def c0():
			del q[:]
			for a in a5(bE).split(";"):
				p=a.split(",",2)
				if len(p)<3:continue
				try:q.append({"serial":int(p[0]),"auto":p[1]=="1","name":p[2]})
				except ValueError:pass
		def aB():aS(bE,";".join("%d,%s,%s"%(a["serial"],"1"if a["auto"]else "0",a["name"].replace(";"," ").replace(","," "))for a in q))
		def c1():
			i["pos"]={}
			for a in a5(bF).split(";"):
				try:k,b=a.split(":");x,y=b.split(",");i["pos"][k]=Kit.adapt(int(x),int(y))
				except ValueError:pass
		def aT():
			a7();b=set("m%d"%c["serial"]for c in q);b.update(("player","target"));a=i["pos"]
			for k in[d for d in a if d not in b]:del a[k]
			aS(bF,";".join("%s:%d,%d"%(g,f[0],f[1])for g,f in sorted(a.items())));i["pos_dirty"]=False
		def aU(key,p,at=0):
			if i["pos"].get(key)!=p:
				i["pos"][key]=p;i["pos_dirty"]=True
				if at:i["pos_save_at"]=at
		def a7():
			for a,b in o.items():
				if Kit.is_open(b.get("g")):
					p=aw(b)
					if p is not None and not aj(a):aU(a,p)
		def a8():return int(safe(lambda:API.Player.Serial,0)or 0)
		def c2(n):
			if n is None:return ""
			try:return cG.get(int(n),"")
			except Exception:return str(n).split(".")[-1].lower()
		def a9(serial):return N()if serial==i["me"]else U(serial)
		aV,c3,c4,c5,c6,c7,c8,ba,bY,bZ,b_,b0=range(12);aI={}
		def b1(serial):
			if not serial:return
			m=a9(serial)
			if m is None:return
			try:
				a=bool(m.IsDead);d=time.time();c=aI.get(serial)
				if c is None or d>=c[5]or a!=c[6]:
					if c is None and len(aI)>=64:aI.clear()
					c=aI[serial]=(str(m.Name or ""),int(m.HitsMax or 0),int(m.ManaMax or 0),int(m.StaminaMax or 0),c2(m.Notoriety),d+.5,a)
				e=(c[0],int(m.Hits or 0),c[1],int(m.Mana or 0)if c[2]else 0,c[2],int(m.Stamina or 0)if c[3]else 0,c[3],c[4],a,bool(m.IsPoisoned),bool(m.IsYellowHits),bool(m.IsParalyzed))
			except Exception:aI.pop(serial,None);return
			b=e[aV]
			if b and i["names"].get(serial)!=b:i["names"][serial]=b
			return e
		S={"get":None,"looked":False,"root":None,"obj":None,"until":0.};b2=2.
		def c9():
			t=A("ClassicUO.Game.World");a=Y(t,"Instance")if t is not None else None
			if a is None:return
			def b():
				c=a[0]()
				if c is None:S["obj"]=None;return 0
				b=S["obj"];d=time.time()
				if b is None or c is not S["root"]or not 0<S["until"]-d<=b2:
					S["obj"]=None;b=Typing._get(c,"TargetManager")
					if b is None:return 0
					S.update({"root":c,"obj":b,"until":d+b2})
				v=Typing._get(b,"LastAttack")
				if v is None:S["obj"]=None
				return int(v or 0)
			b();return b
		def da():
			if not S["looked"]:S["looked"]=True;S["get"]=safe(c9)
			return int(safe(S["get"],0)or 0)if S["get"]is not None else 0
		def b3():
			s=(da()if l["attack"]else 0)or int(API.LastTargetSerial or 0)
			if not s:i["target"]=0;return
			if s==i["target"]:return
			if s==i["me"]:
				if not l["ignore_self"]:i["target"]=s
			elif API.FindMobile(s)is not None:i["target"]=s
		def db():
			a=set(int(d)for d in(API.GetPartyMemberSerials()or[])if int(d)and int(d)!=i["me"]);i["party"]=a;c=False;b=i["dismissed"]
			if b:
				if l["party"]:b&=a
				else:b.clear()
			if l["party"]:
				for s in a:
					if s in b:continue
					if not any(f["serial"]==s for f in q)and len(q)<aN:q.append({"serial":s,"auto":True,"name":i["names"].get(s)or "Party member"});c=True
			for t in list(q):
				if t["auto"]and(t["serial"]not in a or not l["party"]):q.remove(t);c=True
			if c:aB();aE();K(H)
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
				import clr;import System;from System.Reflection.Emit import DynamicMethod,OpCodes;p=Bridge.parts;p["uo"]=Tz.get(Tz.get(None,"Game",A("ClassicUO.Client")),"UO");p["anims"]=Typing._get(p["uo"],"Animations");p["hues"]=Typing._get(Typing._get(p["uo"],"FileManager"),"Hues");p["hue_color"]=p["hues"].GetType().GetMethod("GetHueColorRgba8888");d=A("ClassicUO.Game.World");p["world"]=d.GetProperty("Instance").GetValue(None,None);p["get_entity"]=d.GetMethod("Get",System.Array[System.Type]([clr.GetClrType(System.UInt32)]));n=A("ClassicUO.Game.GameObjects.Mobile");p["group_for"]=n.GetMethod("GetGroupForAnimation");p["get_data"]=[s for s in p["tex_t"].GetMethods()if s.Name=="GetData"and s.IsGenericMethodDefinition and len(s.GetParameters())==5][0].MakeGenericMethod(clr.GetClrType(System.UInt32));e=p["anims"].GetType();f=e.GetMethod("GetAnimationFrames");g=A("ClassicUO.Renderer.SpriteInfo");b=f.ReturnType;h,i,j,o=(clr.GetClrType(System.Object),clr.GetClrType(System.UInt16),clr.GetClrType(System.Byte),clr.GetClrType(System.Int32));k=DynamicMethod("vauf_frame",h,System.Array[System.Type]([e,i,j,j,o,clr.GetClrType(System.Array[System.UInt16])]),h.Module,True);a=k.GetILGenerator();c=a.DeclareLocal(b);l=a.DeclareLocal(i);q=a.DeclareLocal(clr.GetClrType(System.Boolean));m=a.DefineLabel()
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
		def Z(d,s):v=.5-d*s;return 0. if v<=0 else(1. if v>=1 else v)
		def aW(u,v,box):c,d,e,f,r=box;a=abs(u-(c+e)*.5)-((e-c)*.5-r);b=abs(v-(d+f)*.5)-((f-d)*.5-r);g=a if a>0 else 0.;h=b if b>0 else 0.;i=a if a>b else b;return math.sqrt(g*g+h*h)+(i if i<0 else 0.)-r
		def dc(a,b,x):t=(x-a)/(b-a);t=0. if t<0 else(1. if t>1 else t);return t*t*(3-2*t)
		def b4(v):c=132.-62.*min(1.,max(0.,(v-43.)/107.));return(c,c,c+6.)
		def dd(dx,dy,r):b=(dx+dy)/r*bT;f=min(1.,max(0.,(b+.71)/1.42));t=min(1.,max(0.,(r-67.)/11.5));a=44.*(t**1.2)*f;return(128.-a,128.-a,134.-a)
		def de(dx,dy,r):b=-(dx+dy)/r*bT;t=min(1.,max(0.,(r-56.)/4.));a=t*(-42.+57.*dc(-.3,.75,b));return(min(255.,234.+a),min(255.,203.+a),min(255.,91.+a*.65))
		def ar(b,c,a):
			if a<=0:return
			k=1.-a;b[0]=c[0]*a+b[0]*k;b[1]=c[1]*a+b[1]*k;b[2]=c[2]*a+b[2]*k;b[3]=a+b[3]*k
		def b5(b,a):k=1.-a;b[0]*=k;b[1]*=k;b[2]*=k;b[3]*=k
		def df(u,v,s):
			a=[0.,0.,0.,0.]
			if 140<=u and 38<=v<=156:
				ar(a,bQ,Z(aW(u,v,E),s))
				if a[3]>0:
					ar(a,b4(v),Z(aW(u,v,bL),s));ar(a,bR,Z(aW(u,v,bM),s));e=Z(aW(u,v,bN),s)
					if e>0:
						b5(a,e)
						for k,l in bO:
							f=min(v-k,l-v)
							if f>-1.5:ar(a,b4(v),e*Z(-f,s))
					for g,h,m in bP:
						if abs(u-g)<4 and abs(v-h)<4:i=math.sqrt((u-g)**2+(v-h)**2);ar(a,(40,40,44),Z(i-2.6,s));ar(a,m,Z(i-1.6,s))
			c,d=u-az[0],v-az[1];r=math.sqrt(c*c+d*d)
			if r<a3[0][0]+2:
				for n,b in a3:
					j=Z(r-n,s)
					if j<=0:continue
					if b=="tire":b=dd(c,d,max(r,.01))
					elif b=="gold":b=de(c,d,max(r,.01))
					ar(a,b,j)
				b5(a,Z(r-aP,s))
			return a
		def bb(a):
			b=a[3]
			if b<=.002:return 0
			return(int(a[0]+.5)|(int(a[1]+.5)<<8)|(int(a[2]+.5)<<16)|(int(b*255+.5)<<24))
		def dg(s):
			w,h=int(ay*s),int(ap*s);b=1./s;a=[0]*(w*h)
			for y in range(h):
				v=(y+.5)*b;d=y*w
				for x in range(w):a[d+x]=bb(df((x+.5)*b,v,s))
				yield None
			c=[]
			for y in range(h):c.extend(a[y*w:(y+1)*w][::-1])
			yield w,h,a,c
		def b6(s,c):
			f=aH[1]+1;a=int(math.ceil(2*f*s));d=a/2.;e=[0]*(a*a)
			for y in range(a):
				if y%4==3:yield None
				for x in range(a):
					r=math.sqrt((x+.5-d)**2+(y+.5-d)**2)/s;b=min(Z(r-aH[1],s),Z(aH[0]-r,s))
					if b>0:e[y*a+x]=bb([c[0]*b,c[1]*b,c[2]*b,b])
			yield a,e
		def bc(s):a=int(round(s*100));return{"player":"%sframe_player_%d"%(L,a),"target":"%sframe_target_%d"%(L,a),"blank":"%ssnap_blank_%d"%(L,a)}
		def dh(s):
			c=bc(s);a=None
			for a in dg(s):
				if a is None:yield None
			w,h,e,f=a;b=bf(s);g=[bb([aG[0],aG[1],aG[2],1.])]*(b*b)
			for a in b6(s,M):
				if a is None:yield None
			d,i=a;j=aX(M,s)
			def k():Bridge.put_texture(c["player"],w,h,e);Bridge.put_texture(c["target"],w,h,f);Bridge.put_texture(c["blank"],b,b,g);Bridge.put_texture(j,d,d,i)
			yield k
		def b7(s):
			if s in i["art_scales"]:return True
			if s in i["art_failed"]:return False
			if not any(a["kind"]=="art"and a["s"]==s for a in i["art_jobs"]):i["art_jobs"]=i["art_jobs"]+[{"kind":"art","s":s,"gen":dh(s)}]
			return
		def bd():
			a=set([aY(l["scale"])/100.])
			if l["pscale_on"]:a.add(aY(l["pscale"])/100.)
			for v in aC.values():
				if v is not None:a.add(v/100.)
			return a
		def di():
			c=bd();c.update(f.get("s")for f in o.values()if f.get("art"));a=[g for g in i["art_scales"]if g not in c]
			if not a:return
			d=set(str(int(round(h*100)))for h in a);e=tuple(L+p for p in("frame_","noto_","snap_blank_"));b=[k for k in i["textures"]if k.startswith(e)and k.rsplit("_",1)[-1]in d]
			for s in a:i["art_scales"].discard(s)
			for n in b:i["textures"].discard(n)
			if b:safe(lambda:Bridge.on_main(lambda:Tex.drop(b)))
		def aJ():
			import sys;a=sys.__dict__.get("_VA_ART")
			if not isinstance(a,dict):a={};sys._VA_ART=a
			return a
		def dj():
			b=aJ();c=b.pop("tex",None)or{};d=b.pop("scales",None)or();e=Tex.parts.get("table");f=[p for p in c if Tex.has(p)]
			if b.get("sig")!=a4 or b.get("table")is not e:b.clear();b.update({"sig":a4,"table":e});f=[]
			h=set(str(int(round(r*100)))for r in d);j=set("%d_%d_%d"%tuple(u)for u in[Kit.cb_rgb(w,x)for w,x in a0.items()]+[M])
			for n in f:
				v,a=c[n],n[len(L):].split("_")
				if a[0]=="snap"and len(a)==2 and a[1].isdigit()and type(v)is tuple:g=int(a[1]);i["snaps"][g]={"name":n,"creature":False};i["snap_keys"][n]=v;i["stale"].add(g)
				elif a[-1]not in h or(a[0]=="noto"and "_".join(a[1:4])not in j):continue
				i["textures"].add(n)
			for s in d:
				if all(k in i["textures"]for k in list(bc(s).values())+[aX(M,s)]):i["art_scales"].add(s)
		def dk():a=i["textures"];Tex.drop([b for b in list(Tex.parts["table"].Keys)if str(b).startswith(L)and b not in a])
		def dl():
			d,e,c=i["snap_keys"],[],[]
			for a in i["textures"]:
				if a in d:c.append(a)
				elif not a.startswith(L+"snap_")or a.startswith(L+"snap_blank_"):e.append(a)
			f="%ssnap_%d"%(L,i["me"]);c.sort(key=lambda n:n!=f);b=(e+c)[:cR];aJ().update({"sig":a4,"table":Tex.parts.get("table"),"scales":list(i["art_scales"]),"tex":dict((g,d.get(g,True))for g in b)});b=set(b);return[h for h in i["textures"]if h not in b]
		def dm(key,b):a=aJ();c=[d for d in a.get("px")or()if d[0]!=key];a["px"]=c[-(cS-1):]+[(key,b)]
		def dn(key):return next((b for a,b in aJ().get("px")or()if a==key),None)
		def aX(a,s):return "%snoto_%d_%d_%d_%d"%(L,a[0],a[1],a[2],int(round(s*100)))
		def do(c,s,name):
			a=None
			for a in b6(s,c):
				if a is None:yield None
			b,d=a;yield lambda:Bridge.put_texture(name,b,b,d)
		def dp(b,s):
			a=aX(b,s)
			if a in i["textures"]:return a
			if b==M and b7(s)is None:return
			if a not in i["art_failed"]and not any(d.get("name")==a for d in i["art_jobs"]):c={"kind":"noto","s":s,"name":a,"gen":do(b,s,a)};i["art_jobs"]=i["art_jobs"]+[c]
			return
		def be():return any("out"not in a for a in i["art_jobs"])
		def dq(budget):
			a=time.time()+budget
			for j in i["art_jobs"]:
				while "out"not in j:
					try:r=next(j["gen"])
					except Exception:r=False
					if r is not None:j["out"]=r
					elif time.time()>=a:return True
				if time.time()>=a:break
			return be()
		def dr():
			b=i["art_jobs"];c=bd();c.update(g.get("s")for g in o.values());a=[];d=False
			for j in b:
				if j["s"]not in c:continue
				if d or "out"not in j:a.append(j);continue
				r=j["out"];d=True;e=r is not False and bool(safe(lambda:r()or True,False))
				if j["kind"]=="art":(i["art_scales"]if e else i["art_failed"]).add(j["s"]);i["art_dirty"]=True
				elif not e:i["art_failed"].add(j["name"])
				else:
					for f in o.values():f["last"]=None
			if len(a)!=len(b):i["art_jobs"]=a
		def bf(s):return int(math.ceil(2*(aP+2)*s))
		def bg():return bf(max(bd()))
		def ds(graphic,item):
			b=bW.get(graphic)
			if b is None:
				a=item.GetItemData()
				if a is None:return 0,False,False
				b=bW[graphic]=(int(a.AnimID or 0),bool(a.IsPartialHue),bool(a.IsContainer))
			return b
		def dt(layer,worn):
			a=worn.get("robe",(0,0))[0]
			if layer=="tunic":return worn.get("tunic",(0,0))[0]==568 and a and a not in a1
			if layer=="arms":return bool(a)and a not in a1
			if layer=="torso":
				if a and a not in a1:return True
				b=worn.get("tunic",(0,0))[0];return bool(b)and b not in(5441,5442)and worn.get("torso",(0,0))[0]in(30762,30763)
			if layer in("helmet","hair")and a:
				if a>12659:return a in(19357,30742)
				if a<=9863:return a>=9859 or 8270<=a<=8271
				return a in(12217,12659)
			return False
		def b8(serial):
			m=a9(serial)
			if m is None:return
			e=int(m.Graphic or 0);g=cH.get(e)
			if g is None:return{"body":0,"pieces":()}
			k=cK if e==cJ else int(m.Hue or 0)&16383;l=e in cI;b,h={},{}
			for a in bz:
				f=API.FindLayer(a,serial)
				if f is None:continue
				try:i=int(f.Graphic or 0);b[a]=(i,int(f.Hue or 0)&16383);h[a]=ds(i,f)
				except Exception:b.pop(a,None)
			d=bz
			if "cloak"in b:
				if b.get("robe",(0,0))[0]in cN:d=cM
				elif h["cloak"][2]:d=cL
			if b.get("arms",(0,0))[0]in cO:d=tuple({"arms":"torso","torso":"arms"}.get(r,r)for r in d)
			j=[((g,),k,True)]
			for a in d:
				if a not in b or dt(a,b):continue
				c,n,p=h[a]
				if not c:continue
				if c==970 and e in(694,695):c=547
				o=(c+by,c+bx)if l else(c+bx,c+by);j.append((tuple(s for s in o if s<=65535),b[a][1],n))
			return{"body":g,"pieces":tuple(j)}
		def b9(doll):
			def a():
				a=[]
				for c,d,e in doll["pieces"]:
					b=Bridge.gump_pixels(c,d,e)
					if b is not None:a.append(b)
				return a
			return Bridge.on_main(a)or[]
		def du(layers):
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
		def dv(body,layers,bounds):
			if not body and layers:w,h=layers[0][1:];a=max(w,h)*1.08*100./l["pzoom"];return(w-a)/2.+l["pdx"],(h-a)/2.+l["pdy"],a
			a=bA*100./l["pzoom"]
			if bounds is None or bounds[1]is None:d,e=98,70;b,c=d-a/2.,e-a/2.
			else:f,g,i=bounds;b=(f+i+1)/2.-a/2.;c=g-2
			return b+l["pdx"],c+l["pdy"],a
		def bh(f,body,out):
			b=[];E=isinstance(f,list)
			for F,(c,w,h)in enumerate(f):
				if isinstance(c,list):b.append((c,w,h))
				else:
					k=(list(c),w,h);b.append(k)
					if E:f[F]=k
				yield None
			l=None
			if body and b:
				for r in du(b):
					if r is None:yield None
					else:l=r
			m,n,o=dv(body,b,l);a=int(math.ceil(o))+1;q,s=int(math.floor(m)),int(math.floor(n));G=aG;t=[G]*(a*a)
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
		def ca(serial):
			if serial and(serial not in i["snaps"]or serial in i["stale"])and not any(b[0]==serial for b in i["snap_queue"]):
				a=i["snap_job"]
				if a is not None and a.get("serial")==serial:return
				i["snap_queue"].append((serial,0.))
		def dw(got,job):
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
			for r in bh(job["layers"],0,job["size"]):yield r
		def cb():a=i["snap_job"];return a is not None and "out"not in a
		def dz(now,budget=.008):
			a=i["snap_job"]
			if a is None or "out"in a:return False
			b=now+budget
			while not API.StopRequested:
				try:r=next(a["gen"])
				except StopIteration:a["out"]=False;return False
				except Exception:a["out"]=None;return False
				if r is not None:a["out"]=r;return False
				if time.time()>=b:return True
		def dA(now):
			a=i["snap_job"]
			if a is None or "out"not in a:return
			i["snap_job"]=None;r=a["out"]
			if r is None:
				if not any(d[0]==a["serial"]for d in i["snap_queue"]):i["snap_queue"].append((a["serial"],now+aM))
				return
			if r is False:return
			b,c=a["serial"],a["size"]
			if c!=bg():
				if not any(f[0]==b for f in i["snap_queue"]):i["snap_queue"].append((b,now))
				return
			if cc(b,c,r,a.get("key"))and b==i["me"]and ax.f is not None:t["layers"]=(a["layers"],a["body"])
		def cc(serial,size,b,key):
			a="%ssnap_%d"%(L,serial)
			if not safe(lambda:Bridge.put_texture(a,size,size,b)or True,False):return False
			i["snaps"][serial]={"name":a,"creature":False};i["snap_keys"].pop(a,None)
			if key is not None:i["snap_keys"][a]=key;dm(key,b)
			cd(serial);bq();return True
		def bi(now):
			dA(now)
			if i["snap_job"]is not None:return
			for m,(a,n)in enumerate(i["snap_queue"]):
				if n<=now:del i["snap_queue"][m];break
			else:return
			if a in i["snaps"]and a not in i["stale"]:return
			b=b8(a)
			if b is None:i["snap_queue"].append((a,now+aM));return
			i["stale"].discard(a);c=bg()
			if not b["body"]:
				j=safe(lambda:Bridge.on_main(lambda:Bridge.creature_pixels(a)))if Bridge.creatures else None
				if j is None:
					if Bridge.creatures and i["snap_tries"].get(a,0)<3:i["snap_tries"][a]=i["snap_tries"].get(a,0)+1;i["snap_queue"].append((a,now+aM));return
					i["snaps"][a]={"name":None,"creature":True};cd(a);return
				f={"serial":a,"size":c,"layers":None,"body":0};f["gen"]=dw(j,f);i["snap_job"]=f;return
			d=(a,c,b["body"],b["pieces"],l["pzoom"],l["pdx"],l["pdy"]);g="%ssnap_%d"%(L,a)
			if i["snap_keys"].get(g)==d and g in i["textures"]and(i["snaps"].get(a)or{}).get("name")==g:return
			h=safe(lambda:dn(d))
			if h is not None and len(h)==c*c and cc(a,c,h,d):return
			e,k=safe(lambda:b9(b),[]),b["body"]
			if not e:i["snap_queue"].append((a,now+aM));return
			if len(e)!=len(b["pieces"]):d=None
			i["snap_job"]={"gen":bh(e,k,c),"serial":a,"size":c,"layers":e,"body":k,"key":d}
		def cd(serial):
			for a,b in o.items():
				if au(a)==serial:b["last"]=None
		def ce():
			i["stale"]=set(i["snaps"])
			for a in o:ca(au(a))
		bj=8
		def dB(serial):
			a=i["recent"]
			if not serial or(a and a[-1]==serial):return
			if serial in a:a.remove(serial)
			a.append(serial)
			if len(a)>4*bj:del a[:-bj]
		def dC():
			a=set(au(n)for n in o);a.update(k["serial"]for k in q);a.update(i["party"]);a.update(i["recent"][-bj:]);a.add(i["me"]);h=set(p.get("snap")for p in o.values());c=i["snaps"];e=[]
			for d in[r for r in c if r not in a]:
				b=c[d].get("name")
				if b and b in h:continue
				del c[d]
				if b:e.append(b);i["textures"].discard(b);i["snap_keys"].pop(b,None)
			for g in(i["names"],i["snap_tries"]):
				for d in[u for u in g if u not in a]:del g[d]
			i["stale"]=set(v for v in i["stale"]if v in c);f=i["snap_queue"]
			if any(s[0]not in a for s in f):f[:]=[w for w in f if w[0]in a]
			if e and i["art"]:safe(lambda:Bridge.on_main(lambda:Tex.drop(e)))
		def bk(key):return "target"if key=="target"else "player"
		def au(key):
			if key=="player":return i["me"]
			if key=="target":return i["target"]
			return int(key[1:])
		aC={"player":None,"target":None};ah={"player":None,"target":None};aa=Kit.MARGIN+2
		def aY(v):k=Kit.tscale*(.85 if Kit.compact else 1.);return v if k==1. else max(ab,min(ac,int(round(v*k))))
		def cf(key):
			a=aC.get(key)
			if a is not None:return a/100.
			if l["pscale_on"]and key[:1]=="m"and key[1:].isdigit()and int(key[1:])in i["party"]:return aY(l["pscale"])/100.
			return aY(l["scale"])/100.
		def cg(key):
			def a(w,h,mode):
				b=None;a=None
				if w and h:
					a=(int(w),int(h));e,d=a[0]-2*aa,a[1]-2*aa;c=int(min(100.*float(e)/ay,100.*float(d)/ap))
					if av(key):c=min(c,int(100.*(d-Kit.GAP-P)/E[3]))
					b=max(ab,min(ac,c))
				ah[key]=a
				if b!=aC.get(key):aC[key]=b;i["art_dirty"]=True
			return a
		def ch(s):return max(ap*s,E[3]*s+Kit.GAP+P)
		def dD(key):
			def a(h):
				c=int(h)-2*aa;a=100.*c/ap;b=av(key)
				if b:a=min(a,100.*(c-Kit.GAP-P)/E[3])
				s=max(ab,min(ac,int(a)))/100.;f=max(ay*s,E[0]*s+(161-2*Kit.MARGIN)+4)if b else ay*s;d=0
				if b:
					e=int(math.ceil(ch(s)))+2*aa+1
					if e>int(h):d=e
				return int(math.ceil(f))+2*aa,d
			return a
		def av(key):
			for c,(a,b,d)in e["piece"].items():
				if a==key and b==0:return True
			return False
		def dE(key,w,h):
			a=ah.get(key)
			if not a:return w,h,0,0,False
			W,H=max(a[0],w+2*aa),max(a[1],h+2*aa);c=aa if bk(key)=="player"else W-aa-w;b=h
			if av(key):b=max(h,int(math.ceil(ch(float(h)/ap))))
			return W,H,c,max(aa if b>h else 0,(H-b)//2),True
		def dF(key):
			def a():
				a=o.get(key)
				if not a or not a.get("box"):return
				b,e,w,f=a["box"];s=a["s"];c,d=int(round(E[0]*s)),int(round(E[2]*s))
				if bk(key)=="player":return b+c,b+d,True
				return b+w-d,b+w-c,False
			return a
		def dG(key):
			def a():
				a=o.get(key)
				if not a or not a.get("slot")or not a.get("box"):return
				c,b,d,h=a["box"];W,H=a["win"];return aa,W,H,b,h,b+int(round(E[3]*a["s"]))
			return a
		def af(key):s=cf(key);return s,int(ay*s),int(ap*s)
		def ci(b,w,a,x1):return(a,x1)if b=="player"else(w-x1,w-a)
		def dH(key):
			a,w,h=af(key)
			if key=="player":return 60,420
			if key=="target":return 60+w+20,420
			i=[b["serial"]for b in q].index(int(key[1:]))if key[1:].isdigit()else 0;return 60+(i//4)*(w+10),40+(i%4)*(h+2)
		def bl(serial,action=None):
			def h(*a):
				if F():W(("follow_serial",serial))();return
				if action:W(action)()
			return h
		def cj(key):
			def a():
				a=o.get(key);g=a and a.get("g")
				if not g:return
				b=F();c=not b and not l["click"]and i.get("removing")
				if not b and not l["click"]and not c:return
				p=aw(a)
				if p!=a.get("seen")or time.time()<a.get("drag_until",0.):a["seen"]=p;return
				W(("follow"if b else("remove_click"if c else "click"),key))()
			return a
		def dI(key,g):
			def a(*b):
				a=o.get(key)
				if a is not None and a.get("g")is g and not i["shutting"]:a["g"]=None;W.add(("closed",key),dup=True)
			return a
		def aD(g,x,y,w,h,a,alpha=1.):return Kit.add_box(g,x,y,w,h,alpha,"#%02x%02x%02x"%a)
		def ck(g,c,rows):
			for b,(d,e,f,h)in zip(bv,rows):
				for v in(("hits","poison","yellow")if b=="hits"else(b,)):a=G.CreateGumpSimpleProgressBar(f-d,h-e,bw,cF[v],0,100);a.SetPos(d,e);g.Add(Kit.inert(a));c["bar_"+v]=a
		def dJ(key):
			r=o.get(key,{}).get("g");s,w,k=af(key);t=bk(key);x,y=i["pos"].get(key)or dH(key)
			if Kit.is_open(r):x,y=r.GetX(),r.GetY()
			if key in o:o[key]["g"]=None
			c=lambda v:int(round(v*s));u=bool(i["art"])and s in i["art_scales"];q=bool(i["art"])and not u and s not in i["art_failed"];W,m,e,f,D=dE(key,w,k);F=not l["lock"]and not HOST.layout_locked(H+"."+key);g=G.CreateGump(True,F)
			if aj(key):x,y=int(x),int(y);g.SetRect(x,y,W,m);Kit.note_rect(g,x,y,W,m);Kit.pin_size(g)
			else:x,y=Kit.place(g,x,y,W,m)
			d={}
			if D:z=Kit.MARGIN;Kit.add_window_frame(g,W,m);Kit.add_section(g,z,z,W-2*z,m-2*z)
			h=e+(c(az[0])if t=="player"else w-c(az[0]));j=f+c(az[1]);N,O=ci(t,w,c(bS[0]),c(bS[1]));b=[(e+N,f+c(at),e+O,f+c(dx))for at,dx in c_];a=int(aP*s);I=bc(s)if u or q else None;A=[]
			if u or q:
				if q:
					if not D:A=Kit.add_resizepic(g,Kit.WINDOW_BG,e,f,w,k,mouse=False)
					A=A+[Kit.add_section(g,h-a,j-a,2*a,2*a,alpha=.95),Kit.add_section(g,b[0][0]-4,b[0][1]-4,b[0][2]-b[0][0]+8,b[-1][3]-b[0][1]+8,alpha=.9)]
				B=bf(s);d["snap"]=Tex.control(g,I["blank"],h-B//2,j-B//2,B,B);ck(g,d,b);Tex.control(g,I[t],e,f,w,k);C=int(math.ceil(2*(aH[1]+1)*s));d["noto"]=Tex.control(g,aX(M,s),h-C//2,j-C//2,C,C)
			else:
				if not D:Kit.add_window_frame(g,w,k,corners=False)
				n=2*a;Kit.add_section(g,h-a,j-a,n,n,alpha=.95);p=max(2,int(round(3*s)));d["edge"]=[aD(g,h-a,j-a,n,p,M),aD(g,h-a,j+a-p,n,p,M),aD(g,h-a,j-a,p,n,M),aD(g,h+a-p,j-a,p,n,M)];Kit.add_section(g,b[0][0]-4,b[0][1]-4,b[0][2]-b[0][0]+8,b[-1][3]-b[0][1]+8,alpha=.9);ck(g,d,[(dy,es+1,et,eu-1)for dy,es,et,eu in b])
			d["strip"]=aD(g,h-22,j+int(a*.42),44,al+4,(0,0,0),.65);d["strip"].IsVisible=False
			if key=="player":K="Click: target yourself"if l["click"]else "Your character's frame"
			else:K=("Click: make them your target. Alt+click: auto-follow (again to stop)"if l["click"]else "Alt+click: auto-follow (again to stop)")
			Kit.catcher(g,e,f,w,k,cj(key),None,movable=F);L,P=ci(t,w,c(E[0]),c(E[2]));Kit.catcher(g,e+L,f+c(E[1]),P-L,c(E[3])-c(E[1]),cj(key),K,movable=F);dL(g,key,e,f)
			for Q in("name","hits","mana","stam","status","portrait_text"):d["lbl_"+Q]=Kit.inert(Kit.add_label(g,"",0,0))
			J=None
			if key=="player":d["guard_bg"]=aD(g,0,0,1,1,(0,0,0),.65);d["guard_bg"].IsVisible=False;d["lbl_guard"]=Kit.inert(Kit.add_label(g,"",0,0));J=(e+c(E[2])-6,f+max(1,c(E[1])-al-3))
			o[key]={"g":g,"c":d,"rows":b,"centre":(h,j),"hole":a,"s":s,"art":u or q,"plain":q,"stand":A,"names":I,"last":None,"seen":(x,y),"noto":None,"variant":None,"snap":None,"code_move":False,"shown":{},"bars":{},"serial":None,"box":(e,f,w,k),"win":(W,m),"slot":ah.get(key),"rides":av(key)}
			if J is not None:o[key]["guard_at"]=J
			i["art_dirty"]=True;G.AddControlOnDisposed(g,dI(key,g));Kit.add_front(g);Kit.no_snap(g);Kit.on_moved(g,dK(key));Kit.dispose(r)
		def dK(key):
			def a():
				a=o.get(key)
				if a is None or not Kit.is_open(a.get("g")):return
				p=aw(a)
				if p is not None and p!=a.get("seen"):
					a["seen"]=p;a["code_move"]=True
					if not aj(key):aU(key,p)
				aT()
			return a
		def dL(g,key,ox,oy):
			if key in("player","target"):return
			a=bH if Kit.pic_size(bH[0])[0]>0 else Kit.ART_CLOSE;x,y,c=ox+bI,oy+bI,bl(int(key[1:]),("xclose",key));d="Close this frame. Alt+click: auto-follow (again to stop)"
			if Kit.pic_size(a[0])[0]>0:b=G.CreateGumpButton("",Kit.HUE_TEXT,a[0],a[1],a[2]);b.SetPos(x,y);g.Add(b);Kit.on_click(b,c);b.SetTooltip(d);return
			Kit.add_label(g,"x",x+2,y,Kit.HUE_TITLE);Kit.catcher(g,x,y,max(14,Kit.text_w("x")+4),16,c,d)
		def aK(key):
			a=o.pop(key,None)
			if a:
				i["art_dirty"]=True;g=a.get("g")
				if Kit.is_open(g):
					p=aw(a)
					if p is not None and not aj(key):aU(key,p)
				a["g"]=None;Kit.dispose(g)
		def dM(w,h,side,p=None):
			d=o.get("player")
			if d is None or not Kit.is_open(d.get("g")):return
			if p is None:p=aw(d)
			if p is None:return
			c,b=p;g,i=d.get("win")or af("player")[1:];W,H=Kit.screen()
			if side==1:
				a=(c-w-2,b)
				if a[0]<0:a=(c+g+2,b)
			elif side==2:
				a=(c+g+2,b)
				if W>0 and a[0]+w>W:a=(c-w-2,b)
			else:
				j,k=cn(b,i);e=b+i+2+j+R("player",True);a=(c,e)
				if H>0 and e+h>H:
					f=b-h-2-k-R("player",False)
					if f>=0 or f+h>H-e:a=(c,f)
			x,y=a
			if W>0:x=max(0,min(x,W-w))
			if H>0:y=max(0,min(y,H-h))
			return(x,y)
		bm="UnitFrames_hbar_held";cl=1.;ai={"at":0.,"held":None}
		def dN():
			try:return Tz.get(None,"CurrentProfile",Tz.T("ClassicUO.Configuration.ProfileManager"))
			except Exception:return
		def cm(want):
			a=dN()
			if a is None:return
			if ai["held"]is None:ai["held"]=a5(bm)=="1"
			b=ai["held"]
			if want:
				if not b and not bool(Tz.get(a,"OpenHealthBarForLastAttack")):return
				if not b:Tz.put(a,"OpenHealthBarForLastAttack",False);aS(bm,"1");ai["held"]=True
				try:
					t=Tz.T("ClassicUO.Game.UI.Gumps.BaseHealthBarGump");c=Tz.get(None,"LastAttackBar",t)
					if c is not None and not c.IsDisposed:c.Dispose()
				except Exception:pass
			elif b:Tz.put(a,"OpenHealthBarForLastAttack",True);aS(bm,"");ai["held"]=False
		def dO(now):
			if 0<=ai["at"]-now<=cl:return
			ai["at"]=now+cl
			try:cm(bool(l["hide_bar"]and l["target"]))
			except Exception:pass
		def dP(w,h,side):
			a=o.get("player")
			if a is None or not Kit.is_open(a.get("g")):return
			p=a.get("seen");b=None
			if p is not None:b=(p,a.get("win")or af("player")[1:],side,l["cast"],e["stack"].get("player"),Kit.screen(),w,h)
			if b is None or b!=aA["sig"]or aA["at"]is None:aA["at"]=dM(w,h,side,p);aA["sig"]=b if aA["at"]is not None else None
			c=aA["at"];return None if c is None else(a["g"],c)
		def cn(fy,fh):
			if not l["cast"]:return 0,0
			H=Kit.screen()[1]
			if H>0 and fy+fh+ao+an>H:return 0,an+ao
			return an+ao,0
		def co(fr):
			p=fr.get("seen")
			if p is None:return
			g,d,h,c=fr.get("box")or(0,0,0,af("player")[2]);b=p[1]+d;e,i=cn(b,c);x=p[0]+fr["rows"][0][0]-6;f=(fr.get("win")or af("player")[1:])[1]
			if e:
				a=R("player",True);y=b+c+ao
				if a:y=max(y,p[1]+f+a+ao)
				return x,y
			a=R("player",False);y=b-an-ao
			if a:y=min(y,p[1]-a-an-ao)
			return x,y
		def bn():g,m["g"]=m["g"],None;m["leader"]=None;m["shown"]=None;Kit.dispose(g)
		def dQ(fr):
			bn();d=fr["rows"];w,h=d[0][2]-d[0][0]+12,an;g=G.CreateGump(False,False);Kit.add_window_frame(g,w,h,corners=False,mouse=False);c={}
			for k in("cast","done","fail"):a=G.CreateGumpSimpleProgressBar(w-12,h-10,bw,cX[k],0,100);a.SetPos(6,5);g.Add(Kit.inert(a));c[k]=a
			c["lbl"]=Kit.inert(Kit.add_label(g,"",6,4));b=co(fr)or(0,0);Kit.place(g,b[0],b[1],w,h);Kit.add_front(g,True);Kit.attach(g,fr["g"]);m.update({"g":g,"c":c,"shown":None,"at":b,"leader":fr["g"],"s":fr["s"],"w":w})
		def cp(now):
			a=o.get("player")
			if not l["cast"]or a is None or not Kit.is_open(a.get("g")):
				m["state"]=None;i["jr"]=None
				if m["g"]is not None:bn()
				return
			c=None
			if i["jr"]is None:i["jr"]=D()
			else:c=i["jr"].new()
			if c:
				g=i["names"].get(i["me"])or ""
				for b in c:
					d=b.name or ""
					if g and d==g:
						e=cZ.get(b.low.strip())
						if e is not None:f=Kit.spell_info(e[0]);n=f[3]if f and f[3]else 1.;m.update({"spell":e[0],"start":min(now,b.at or now),"secs":max(.1,float(n)),"state":"cast","pct":0,"word":""});continue
					elif d and d!="System":continue
					if m["spell"]is None or now-m["start"]>m["secs"]+cV:continue
					p=O(b,Q)
					for q,r in cY:
						if p.startswith(q):
							if m["state"]!="cast":m["pct"]=100
							m.update({"state":"fail","word":r,"until":now+bK});break
			h=m["state"]
			if h=="cast":
				j=now-m["start"]
				if j>=m["secs"]:m.update({"state":"done","until":now+bK,"pct":100})
				else:m["pct"]=max(0,int(100*j/m["secs"]))
			elif h is not None and now>=m["until"]:m["state"]=None
			k=a["last"][5]if a.get("last")else None
			if k is not None and k[bY]:m["state"]=None
			dR(a)
		def dR(fr):
			b=m["state"];g=m["g"]
			if b is None:
				if g is not None and m["shown"]is not None:m["shown"]=None;Kit.set(g,"IsVisible",False)
				return
			if g is None or not Kit.is_open(g)or m["s"]!=fr["s"]or m["leader"]is not fr["g"]:dQ(fr);g=m["g"]
			c=co(fr)
			if c is not None and c!=m["at"]:m["at"]=c;g.SetRect(c[0],c[1],m["w"],an);Kit.moved_by_code(g)
			f=m["spell"]if b!="fail"else "%s: %s"%(m["spell"],m["word"]);d=(b,m["pct"],f);a=m["shown"]
			if d==a:return
			m["shown"]=d;e=m["c"]
			if a is None or a[0]!=b:
				for k in("cast","done","fail"):e[k].IsVisible=k==b
			if a is None or a[0]!=b or a[1]!=d[1]:e[b].SetProgress(float(d[1]),100.)
			if a is None or a[2]!=f:h=Kit.fit(f,m["w"]-16);Kit.set_text(e["lbl"],h,Kit.HUE_TEXT);e["lbl"].SetPos(max(6,(m["w"]-aO(h))//2),4)
			if a is None:g.IsVisible=True;Kit.stir()
		def dS(now):
			if not l["guard"]:i["guard"]=False
			elif now>=i["next_guard"]:i["next_guard"]=now+.5;i["guard"]=HOST.guarded()
			a=o.get("player")
			if a is None or "guard_at"not in a or not Kit.is_open(a.get("g")):return
			d=i["guard"]
			if d is None:b,c="?",Kit.HUE_INFO
			elif d:b,c="GUARDED",Kit.HUE_GOOD
			else:b,c="",Kit.HUE_TEXT
			e,y=a["guard_at"];aL(a,"guard",b,e,y,c,"right")
			if a["shown"].get("guard_bg")!=b:
				a["shown"]["guard_bg"]=b;f=a["c"]["guard_bg"]
				if b:g=Kit.text_w(b)+8;Kit.ui_rect(f,e-g+4,y-1,g,al+4)
				f.IsVisible=bool(b)
		def aL(fr,name,text,x,y,hue,align="left"):
			if align=="right":x-=aO(text)if text else 0
			elif align=="center":x-=(aO(text)if text else 0)//2
			a=(text,hue,int(x),int(y));c=fr["shown"];b=c.get(name)
			if b==a:return
			c[name]=a;d=fr["c"]["lbl_"+name];Kit.set_text(d,text,hue)
			if b is None or b[2]!=a[2]or b[3]!=a[3]:Kit.ui_pos(d,a[2],a[3])
		def bo(fr,variant,cur,mx):
			a=(float(max(0,cur)),float(max(1,mx)))
			if fr["bars"].get(variant)==a:return
			b=fr["c"].get("bar_"+variant)
			if b is not None:b.SetProgress(a[0],a[1]);fr["bars"][variant]=a
		def dT(fr,want):
			if fr["variant"]==want:return
			fr["variant"]=want
			for v in("hits","poison","yellow"):
				a=fr["c"].get("bar_"+v)
				if a is not None:
					a.IsVisible=v==want
					if v!=want:a.SetProgress(0.,1.);fr["bars"][v]=(0.,1.)
		def dU(fr,a):
			if fr["noto"]==a:return
			c=fr["c"]
			if fr["art"]:
				b=dp(a,fr["s"])
				if b is None:return
				c["noto"].TextureName=b
			else:
				for d in c["edge"]:d.SetBaseColor(a[0],a[1],a[2],255)
			fr["noto"]=a
		def dV(fr,serial):
			if not fr["art"]:return{}
			a=not serial
			if fr["shown"].get("snap_hidden")!=a:fr["shown"]["snap_hidden"]=a;fr["c"]["snap"].IsVisible=not a
			if a:return{}
			ca(serial);b=i["snaps"].get(serial)or{};dW(fr,b.get("name")or fr["names"]["blank"]);return b
		def dW(fr,tex):
			if fr["snap"]!=tex:fr["snap"]=tex;fr["c"]["snap"].TextureName=tex
		def dX(cur,mx):return int(round(100.*cur/mx))if mx>0 else 0
		def dY(key):
			a=o.get(key)
			if a is None or not Kit.is_open(a.get("g")):return
			b=au(key)
			if b!=a["serial"]:a["serial"]=b;dB(b)
			d=b1(b);q=b==i["me"];z=key!="target"and b and b==i["target"];A=dV(a,b);B=a["c"];C=(b,z,l["numbers"],a["snap"],bool(A.get("creature")),d)
			if C==a["last"]:return
			a["last"]=C;D=Kit.HUE_TITLE if z else Kit.HUE_TEXT;e,g="",""
			if not b or d is None:
				E,D,f,r=M,Kit.HUE_INFO,((0,1),)*3,"hits"
				if not b:h,c="",("","","");g="No target"
				else:h=j(i["names"].get(b)or "Unknown",b,None,q);c=("Out of range","","")
			else:
				p=d[bY];F=Kit.hp_mark(d[bZ],d[b0],d[b_]);h=j(d[aV]or i["names"].get(b)or "Unknown",b,None if p else d[ba],q)+("  "+F if F else "");r="poison"if d[bZ]else("yellow"if d[b_]else "hits");f=((d[c3],d[c4]),(d[c5],d[c6]),(d[c7],d[c8]));E=M if p else Kit.cb_rgb(d[ba],a0.get(d[ba],a0["gray"]));e="DEAD"if p else("PARA"if d[b0]else "")
				if A.get("creature"):g="No picture"
				c=[]
				for k,(G,s)in enumerate(f):
					if s<=0:c.append(""if k else "--")
					elif q or k:c.append("%d/%d"%(G,s))
					else:c.append("%d%%"%dX(G,s))
				if p:c[0]="Dead"
				c=tuple(c)
			if not l["numbers"]and c and c[0]!="Out of range":c=("","","")
			dT(a,r);bo(a,r,f[0][0],f[0][1]);bo(a,"mana",f[1][0],f[1][1]);bo(a,"stam",f[2][0],f[2][1]);dU(a,E);H=a["rows"]
			for k,L in enumerate(bv):t,m,u,v=H[k];aL(a,L,c[k],u-8,m+(v-m-al)//2-1,Kit.HUE_TEXT,"right")
			t,m,u,v=H[0];w=max(20,u-t-16-(aO(c[0])+10 if c[0]else 0));n=a["shown"].get("fit")
			if n is None or n[0]!=h or n[1]!=w:n=a["shown"]["fit"]=(h,w,Kit.fit(h,w))
			aL(a,"name",n[2],t+8,m+(v-m-al)//2-1,D);x,I=a["centre"];y=a["hole"];J=I+int(y*.42);aL(a,"status",e,x,J+2,Kit.HUE_BAD if e=="DEAD"else Kit.HUE_TITLE,"center")
			if a["shown"].get("strip")!=e:
				a["shown"]["strip"]=e
				if e:K=Kit.text_w(e)+10;Kit.ui_rect(B["strip"],x-K//2,J,K,al+4)
				B["strip"].IsVisible=bool(e)
			if g=="No target"and Kit.text_w(g)>2*y-6:g="None"
			aL(a,"portrait_text",Kit.fit(g,2*y-6)if g else "",x,I-al//2-1,Kit.HUE_INFO,"center")
		def bp():
			a=[]
			if l["player"]:a.append("player")
			if l["target"]and(i["target"]or not l["hide_empty"]):a.append("target")
			a.extend("m%d"%b["serial"]for b in q);return a
		def cq():
			d=bp()
			for b in list(o):
				if b not in d:aK(b)
			for b in d:
				a=o.get(b)
				if a is None:d_(b)
				s=cf(b);c=b7(s)if i["art"]else False
				if a is not None and a.get("plain")and c is not None and a.get("s")==s:
					if c:dZ(a)
					else:a["redo"]=True
				if(a is None or not Kit.is_open(a.get("g"))or a.get("s")!=s or a.get("redo")or a.get("slot")!=ah.get(b)or(a.get("slot")and a.get("rides")!=av(b)))and(c is not None or a is None or a.get("plain")or not Kit.is_open(a.get("g"))):
					dJ(b)
					if not o[b]["plain"]:bq()
				dY(b)
		def dZ(fr):
			for p in fr["stand"]:Kit.set(p,"IsVisible",False)
			fr.update({"plain":False,"stand":[],"last":None});bq()
		def bq():
			if i["art"]and I()and time.time()<i.get("first_by",0.):HOST.split_at("HUD art")
		def d_(key):
			if ah.get(key)is not None or key not in ah or not I():return
			a=HOST.layout_slot(H+"."+key)
			if a and a[0]and a[1]:cg(key)(a[0],a[1],None)
		def cr():
			if not i["art"]or not I():return False
			if i["art_jobs"]or i["snap_job"]is not None or any(o.get(a)is None for a in bp())or any(b.get("plain")for b in o.values()):return True
			return any(a9(c[0])is not None for c in i["snap_queue"])
		def cs(key):
			def a():a=o.get(key);return a.get("g")if a else None
			return a
		def aj(key):return Kit.zone_up(H+"."+key)
		def aw(fr):r=Kit.rect(fr.get("g"));return None if r is None else(r[0],r[1])
		def d0(now):
			for b,a in o.items():
				if not Kit.is_open(a.get("g")):continue
				p=aw(a)
				if p is None:continue
				if p!=a.get("seen"):
					a["seen"]=p
					if a.get("code_move"):a["code_move"]=False
					else:
						a["drag_until"]=now+a2
						if not aj(b):a["moved"]=a["dropped"]=True
					if not aj(b):aU(b,p,now+a2)
				else:
					a["code_move"]=False
					if a.get("dropped")and now>=a.get("drag_until",0.)and SNAP.pressed()is not True:a["dropped"]=False;d1(b)
			if i["pos_dirty"]and now>=i["pos_save_at"]:aT()
		def ct(key):
			a=o.get(key)
			if a is None or not Kit.is_open(a.get("g")):return
			p=a.get("seen")or aw(a)
			if p is None:return
			w,h=a.get("win")or af(key)[1:];return p[0],p[1],w,h
		def d1(key):
			r=ct(key)
			if r is None:return
			x,y,w,h=r;f=None;g=i=None
			for n in o:
				if n==key:continue
				p=ct(n)
				if p is None:continue
				a,b,c,e=p
				for j,k in((a+c,b),(a+c,b+e-h),(a-w,b),(a-w,b+e-h),(a,b+e),(a+c-w,b+e),(a,b-h),(a+c-w,b-h)):
					d=max(abs(x-j),abs(y-k))
					if d<=am and(f is None or d<f[0]):f=(d,j,k)
				if y<b+e+am and b<y+h+am:
					for j in(a+c,a-w,a,a+c-w):
						d=abs(x-j)
						if d<=am and(g is None or d<g[0]):g=(d,j)
				if x<a+c+am and a<x+w+am:
					for k in(b+e,b-h,b,b+e-h):
						d=abs(y-k)
						if d<=am and(i is None or d<i[0]):i=(d,k)
			if f is not None:l,m=f[1],f[2]
			else:l=g[1]if g else x;m=i[1]if i else y
			if(l,m)!=(x,y):br(key,l,m);o[key]["moved"]=True
		def br(key,x,y):
			a=o.get(key)
			if a is None or not Kit.is_open(a.get("g")):return
			w,h=a.get("win")or af(key)[1:];g=a["g"];x,y=Kit.clamp(x,y,w,h);g.SetRect(int(x),int(y),w,h);Kit.note_rect(g,int(x),int(y),w,h);Kit.moved_by_code(g);a.update({"seen":(int(x),int(y)),"code_move":True,"moved":False});i["pos"][key]=a["seen"];i.update({"pos_dirty":True,"pos_save_at":time.time()+a2})
		def d2(force=False):
			p,t=o.get("player"),o.get("target")
			if(p is None or t is None or not Kit.is_open(p.get("g"))or not Kit.is_open(t.get("g"))):return
			d,f=Kit.screen();h,w,i=af("player");b,c=p.get("seen"),t.get("seen")
			if aj("player")or aj("target")or d<=0 or f<=0 or b is None or c is None:return
			e=bool(p.get("moved"));g=bool(t.get("moved"))
			if g and not e and not force:
				a=(d-c[0]-w,c[1])
				if a!=b:br("player",*a)
			elif e or force:
				a=(d-b[0]-w,b[1])
				if a!=c:br("target",*a)
		def d3(key):
			a=au(key)
			if not a:return
			if API.HasTarget()and C(H)in(None,"pick"):
				if ad(a,"hud.frame",ak):API.Target(a)
			else:
				API.SetLastTarget(serial=a)
				if key!="target"and a!=i["me"]:i["target"]=a
		def aZ(serial,auto=False):
			if not serial:z("target someone first, then click Add frame.",Kit.HUE_BAD);return
			i["dismissed"].discard(serial)
			if serial==i["me"]:z("that's you; your own frame is the player frame.");return
			for t in q:
				if t["serial"]==serial:t["auto"]=False;z("%s already has a frame."%t["name"]);aB();return
			if len(q)>=aN:z("%d frames is the limit."%aN,Kit.HUE_BAD);return
			d=b1(serial)
			if d is None:z("that isn't a mobile you can see.",Kit.HUE_BAD);return
			q.append({"serial":serial,"auto":auto,"name":d[aV]or "Unknown"});aB();z("added %s."%(d[aV]or "a frame"),Kit.HUE_GOOD);aE();K(H)
		def bs(serial):
			for t in q:
				if t["serial"]==serial and t["auto"]:i["dismissed"].add(serial)
			q[:]=[a for a in q if a["serial"]!=serial];aK("m%d"%serial);aB();aE();K(H)
		def cu(serial):return any(a["serial"]==serial for a in q)
		def cv(kind):
			def a(serial):W.add((kind,int(serial or 0)),dup=True)
			return a
		d4=("Frame your target, or pick someone with a target cursor. Alt+click a frame: auto-follow (again to stop)");d5="Click a person or their frame with a target cursor to remove it (each frame has an X too)";cw=40
		def aE():
			if i["shutting"]:return
			M=Kit.MARGIN;g,b,c=aF.begin(bG,M+30+Kit.GAP+cw+M)
			if not i["minimized"]:aF.frame(g);a=M+30+Kit.GAP;Kit.add_section(g,M,a,bG-2*M,cw);Kit.art_button(g,b,"add",Kit.ART_CIRCLE,M+12,a+12,"Add frame",d4,on_click=W("add_frame"));Kit.art_button(g,b,"remove",Kit.ART_CIRCLE,M+56+Kit.text_w("Add frame"),a+12,"Remove frame",d5,on_click=W("remove_frame"))
			aF.end(g);d6()
		aF=Kit.Window(H,ak,i,aR,aE,cD,cE,mini=(cT,cU),icon=7028,cleanup=aq,lock=True)
		def d6():
			c=aR["c"]
			if "status"in c:Kit.set_text(c["status"],"%s: %s"%(ak,Kit.count(len(q),"frame")))
		cx={"rm":bs,"click":d3,"add_ext":aZ,"follow_serial":lambda serial:B(serial,ak)};cy=(("player","Show your own frame","Your HP, mana and stamina"),("target","Show the target frame","Your current target"),("hide_empty","Hide the target frame with no target","Shown only while you have a target"),("numbers","Show numbers on the bars","HP, mana and stamina as numbers (others' HP as a %)"),("lock","Lock the frames in place","Frames can't be dragged"),("cast","Show a cast bar under your frame","Your spell filling through its cast delay: green when cast, red when it fails"));d7=(("hide_bar","Hide TazUO's own target health bar","Avoids two target bars; untick to get your client's setting back"),("click","Click a frame to target it","Aims a target cursor if one is up, else sets your last target"),("party","Add a frame for each party member","While they are in your party"),("ignore_self","Ignore yourself as last target","Targeting yourself (a bandage, a heal) keeps your target frame"),("attack","Prefer the attack target","Frame who you attack, else your last target"),("mirror","Mirror the player and target frames","Drag either frame and the other mirrors it across the screen"),("guard","GUARDED tag on your frame","GUARDED in guard zones, ? until known (enter or leave one), blank outside"));cz=L+"snap_preview";d8="Frame size, percent of the art (%d-%d%%)"%(ab,ac);d9="Party members' frame size while ticked (%d-%d%%)"%(ab,ac);a_=(("pdx","Left / right","Move pictures left or right in the circle","%+d"),("pdy","Up / down","Move pictures up or down in the circle","%+d"),("pzoom","Zoom","Zoom pictures in or out (100%% = %d art pixels tall)"%bA,"%d%%"))
		def ea(w):
			a=max(Kit.text_w("All frames:"),24+Kit.text_w("Party members:"))
			def b(f,x,y):b=x+26+a;f.c["pscale"]=Kit.with_tip(Kit.add_slider(f.g,b,y+4,260,ab,ac,l["pscale"]),d9);f.c["pscale_lbl"]=Kit.add_label(f.g,"%d%%"%l["pscale"],b+272,y+2,Kit.HUE_INFO)
			c={"top":32,"sh":30+V+4+10,"dx":12+V+4+16,"ldy":0,"fh":26,"sw":180,"ugap":12,"lgap":12,"lw":max(Kit.text_w(d[1])for d in a_),"bdy":0,"bgap":18};return(("OTHERS' FRAMES  (%d of %d)"%(len(q),aN),(("custom",0,eb),),{"top":0,"sh":30+28+4+max(1,len(q))*24+6}),("OPTIONS",[("check",)+g for g in cy]+[("gap",-26*len(cy))]+[("check",)+h+({"dx":12+w//2},)for h in d7],{"pad":6}),("FRAME SIZE",(("slider","scale","All frames:",d8,ab,ac,{"lw":a,"lgap":14,"ldy":2,"sdy":4,"sw":260,"ugap":12,"vfmt":"%d%%"}),("check","pscale_on","Party members:","Party members' frames use the slider beside this; unticked, the size above",{"stay":True}),("custom",0,b)),{"top":34,"sh":96}),("PICTURE  (in each frame's circle)",[("custom",0,ec)]+[("slider",n,p+":",r,aQ[n][0],aQ[n][1],{"vfmt":s})for n,p,r,s in a_]+[("buttons",(("retake",Kit.ART_PLAY,"Retake pictures","Take every picture again (after a gear change)"),("reset",Kit.ART_CLOSE,"Reset","Put the picture sliders back to defaults")))],c))
		def eb(f,x,y):
			g,w,a=f.g,f.w,f.store;d=x+12;Kit.art_button(g,a,"add",Kit.ART_PLAY,d,y+28,"Add target","Frame your current target",on_click=W("add_target"));Kit.art_button(g,a,"pick",Kit.ART_PLAY,d+49+Kit.text_w("Add target"),y+28,"Pick...","Pick someone to frame",on_click=W("pick"));Kit.art_button(g,a,"clear",Kit.ART_CLOSE,x+w-47-Kit.text_w("Clear all"),y+28,"Clear all","Remove everyone else's frame",on_click=W("clear"));e=y+30+28+4;h=Kit.pic_size(Kit.ART_CLOSE[0])[0]or 30
			if not q:Kit.add_label(g,"No frames yet. Target someone, then click Add target.",x+12,e+3,Kit.HUE_INFO)
			for i,t in enumerate(q):
				b=e+i*24;c="(party)"if t["auto"]else "";k=w-24-h-6-(Kit.text_w(c)+8 if c else 0);l=j(t["name"],t["serial"]);m=Kit.fit(l,k);Kit.add_label(g,m,x+12,b+3);Kit.catcher(g,x+12,b,k+8,20,bl(t["serial"]),"Alt+click: auto-follow (again to stop)")
				if c:Kit.add_label(g,c,x+12+Kit.text_w(m)+8,b+3,Kit.HUE_INFO)
				Kit.art_button(g,a,"rm%d"%i,Kit.ART_CLOSE,x+w-12-h,b,None,"Remove %s's frame. Alt+click: auto-follow (again to stop)"%l,on_click=bl(t["serial"],("rm",t["serial"])))
		def ec(f,x,y):
			g=f.g;Kit.add_section(g,x+12,y-2,V+4,V+4,alpha=1.)
			if i["art"]and i.get("running"):bt();Tex.control(g,cz,x+14,y,V,V)
			else:
				a=("Pictures","unavailable")if i.get("running")else("Turn Frames","on for a","preview");c=y+(V-len(a)*18)//2
				for d,b in enumerate(a):Kit.add_label(g,b,x+14+(V-Kit.text_w(b))//2,c+d*18,Kit.HUE_INFO)
		def cA():
			a=time.time();i["crop_changed"]=a
			if i["art"]and i.get("running")and a>=t["next_preview"]:t["next_preview"]=a+.3;bt()
		def ed(f):
			if Kit.was_clicked(f.store,"retake"):t["layers"]=None;i["crop_changed"]=1.
			if Kit.was_clicked(f.store,"reset"):
				for k,a,b,c in a_:f.c[k].SetValue(bU[k])
				cA()
		def ee(f,new):
			try:new["pscale"]=max(ab,min(ac,int(f.c["pscale"].Value)))
			except Exception:return
			Kit.set_text(f.c["pscale_lbl"],"%d%%"%new["pscale"])
		def ef(old,new):
			if(new["lock"],new["click"])!=(old["lock"],old["click"]):i["rebuild"]=True
			if new["party"]!=old["party"]:i["next_party"]=0.
			if new["mirror"]and not old["mirror"]:i["mirror_now"]=True
			i["art_dirty"]=True
			for k,a,b,c in a_:
				if new[k]!=old[k]:cA();break
		ax=Kit.Page(l,ea,a6,ef,adjust=ee,clicks=ed)
		def eg(g,x,y,w):t["store"]=ax.build(g,x,y,w).store
		def eh():ax.closed();t.update({"layers":None,"preview_gen":None})
		def bt():
			if i.get("running")and i["art"]:t["preview_want"]=True
		def ei():
			a=b8(i["me"]or a8())
			if not a or not a["body"]:return
			b=safe(lambda:b9(a),[]);return(b,a["body"])if b else None
		def ej():
			a=t.get("layers")
			if a is None:
				a=safe(lambda:Kit.on_client(ei))
				if not a:return
				t["layers"]=a
			t["preview_gen"]=bh(a[0],a[1],V)
		def ek(budget):
			b=time.time()+budget
			while t.get("preview_gen")is not None:
				a=t["preview_gen"]
				try:r=next(a)
				except Exception:
					if t.get("preview_gen")is a:t["preview_gen"]=None
					return
				if r is not None:
					if t.get("preview_gen")is a:t["preview_gen"]=None
					safe(lambda:Bridge.on_main(lambda:Bridge.put_texture(cz,V,V,r)));return
				if time.time()>=b:return
		def el(now):
			t=i["crop_changed"]
			if not t or now-t<.5:return
			i["crop_changed"]=0.
			if i["art"]:
				if ax.f is not None:bt()
				ce()
		bX()
		def em():
			bV();i.update({"me":a8(),"running":True});m.update({"spell":None,"state":None,"shown":None});t.update({"preview_want":False,"preview_gen":None});bX();c0();c1();aq.service("frames.player_anchor",dP);i["minimized"]=aF.start_min();i["first_by"]=time.time()+cP;i["art"]=Bridge.find()
			if i["art"]:safe(dj);safe(lambda:Bridge.on_main(dk))
			else:z("no drawn pictures on this client; using stone frames.")
			aE();aF.dock();aq.service("unitframes.add",lambda serial:W(("add_ext",int(serial)))());aq.service("look.hud",en);aC["player"]=aC["target"]=None;ah["player"]=ah["target"]=None
			for a in("player","target"):HOST.layout_add(H+"."+a,cs(a),ak+" ("+a+")",{"fit":cg(a),"fill":"frame","exact":True,"pieces_out":True,"hug":dD(a),"untitled":True});ag(a,cs(a),dF(a),dG(a));e["want"][a]=lambda k=a:k not in o and k in bp();aq.add(HOST.layout_remove,H+"."+a);aq.add(ag,a,None)
			T["fn"]=lambda:i["target"];b3();cq();b=time.time()
			for c in range(len(i["snap_queue"])):
				if not i["art"]or i["snap_job"]is not None:break
				bi(b)
			i["art_wait"]=cr()
			if i["art_wait"]:ae(lambda:i["running"]and i["art_wait"]and time.time()<i.get("first_by",0.))
		def en():
			for a in o.values():a["redo"]=True
		def cB():return i["target"]or int(API.LastTargetSerial or 0)
		def eo():
			if aR["g"]is None:return
			if Kit.closed(aR):return
			a=time.time()
			if a<i["full_at"]and not i["queue"]and not i["rebuild"]and a+1.>i["full_at"]:
				if i["art"]:bi(a)
				if m["state"]=="cast":cp(a)
				return
			i["full_at"]=a+bJ-.005;i["me"]=i["me"]or a8();b3()
			while i["queue"]:
				c=i["queue"].pop(0);b=c[0]if isinstance(c,tuple)else c
				if aF.action(c):continue
				if b=="add_frame":
					d=cB()
					if d and d!=i["me"]and not cu(d):aZ(d);continue
					b="busy"if C(H)else "pick"
				elif b=="remove_frame":
					if not q:z("nobody else has a frame (turn off your own and the target frame in settings).")
					elif C(H):b="busy"
					else:z("click the person, or their frame, to remove.");i["removing"]=True;J(bD,cv("unpicked"))
				if b=="busy":z("a target cursor is up; try again after it.")
				elif b=="pick":z("choose who gets a frame.");J(bD,cv("picked"))
				elif b=="add_target":aZ(cB())
				elif b=="picked":
					if c[1]:aZ(c[1])
					else:z("pick cancelled.")
				elif b=="remove_click":
					d=au(c[1])
					if d and i.get("removing")and API.HasTarget():API.Target(d)
				elif b=="unpicked":
					i["removing"]=False
					if not c[1]:z("remove cancelled.")
					elif cu(c[1]):h=next((k["name"]for k in q if k["serial"]==c[1]),"");bs(c[1]);z("removed %s."%(h or "the frame"))
					else:z("they have no frame of their own.")
				elif b=="clear":
					for t in q:aK("m%d"%t["serial"])
					del q[:];aB();K(H)
					if l["party"]:z("cleared; party members come back while 'Add a frame for each party member' is ticked.")
					aE()
				elif b=="follow":
					d=au(c[1])
					if d:B(d,ak)
				elif b in("closed","xclose"):
					e=c[1]
					if b=="xclose":aK(e)
					o.pop(e,None)
					if e in("player","target"):l[e]=False;a6();K(H);z("%s frame hidden; tick it again in settings."%e)
					elif e[1:].isdigit():bs(int(e[1:]))
				elif b in cx:cx[b](c[1])
			if i["rebuild"]:
				i["rebuild"]=False;a7()
				for e in list(o):aK(e)
			if i["art"]:
				f=bg()
				if i["snap_px"]!=f:
					i["snap_px"]=f
					if i["snaps"]:ce()
			a=time.time()
			if a>=i["next_party"]:i["next_party"]=a+1.;db()
			if i["art_jobs"]:dr()
			cq()
			if i["art"]and i["art_dirty"]:i["art_dirty"]=False;di()
			if a>=i["next_prune"]:i["next_prune"]=a+5.;dC()
			for j in o.values():j["moved"]=False
			d0(a);g=(av("player"),av("target"))
			if g!=i.get("rides"):i["rides"]=g;HOST.layout_refit()
			X()
			if l["mirror"]:d2(force=i.pop("mirror_now",False))
			cp(a);dO(a);dS(a)
			if i["art"]:bi(a)
			if i["art_wait"]:i["art_wait"]=cr()
			el(a)
			if a>=i["next_save"]:
				i["next_save"]=a+10.;a7()
				if i["pos_dirty"]:aT()
		def ep():
			if i["shutting"]:return
			a=cQ if I()and not HOST.load_jobs else bB;b=time.time()+a
			if be():dq(a)
			if cb():dz(time.time(),max(.002,b-time.time()))
			if t.get("preview_want"):
				t["preview_want"]=False
				if ax.f is not None:ej()
			if t.get("preview_gen")is not None:ek(bB)
		def cC():return bool(cb()or be()or t.get("preview_want")or t.get("preview_gen")is not None)
		def eq():
			if m["state"]=="cast":return cW
			return.03 if i["art_jobs"]or i["snap_job"]is not None or cC()else bJ
		def er():
			i.update({"shutting":True,"running":False,"removing":False,"snap_job":None,"art_jobs":[]});t.update({"preview_want":False,"preview_gen":None});T["fn"]=None;aT();a6();aB();safe(lambda:cm(False));ai["held"]=None
			for c in list(o):b=o.pop(c);g,b["g"]=b.get("g"),None;Kit.dispose(g)
			bn();i["jr"]=None
			if i["art"]and i["textures"]:
				a=safe(dl)if HOST.stopping()and not safe(HOST.no_cache,False)else None
				if a is None:a=list(i["textures"]);aJ().pop("tex",None)
				if a:safe(lambda:Bridge.on_main(lambda:Tex.drop(a)))
				i["textures"].clear();i["art_scales"]=set()
			i["art"]=None;aq.close()
		return{"start":em,"tick":eo,"stop":er,"client_tick":True,"config_height":ax.height,"build_config":eg,"poll_config":ax.poll,"config_closed":eh,"thread_tick":ep,"interval":eq,"thread_wanted":cC}
	def aq():
		P="spelltimers";I="Buffs & Timers";ar="SpellTimers_settings";ba="SpellTimers_pos";bb="SpellTimers_min";au="SpellTimers_active";bc=3834;av,bd=320,46;aw=28;ax,ay,be=3,16,8;az=.1;aA=.25;aB=5.;ad=2240;aC=22;ag=2.5;aD=2;aE=1.;aF=4;aG=40;aH="spelltimers.ending";ah=120;aI=360;bf=frozenset(("polymorph",));bg=Kit.HUE_GOOD;v=dict.fromkeys(("Clumsy","Feeblemind","Weaken","Curse"),("target","debuff",(0,1.2,0,0,0),0,"stat"));v.update(dict.fromkeys(("Agility","Cunning","Strength","Bless"),("target","buff",(0,1.2,0,0,0),0,"stat")));v.update({"Night Sight":("target","buff",(900,0,0,0,0),2340,None),"Invisibility":("target","buff",(0,1.2,0,0,0),0,"hidden"),"Paralyze":("target","debuff",(7,.2,0,0,0),0,"paralyzed"),"Poison":("target","debuff",None,0,"poisoned"),"Protection":("self","buff",(0,2.,0,15,240),0,None),"Reactive Armor":("self","buff",None,0,None),"Magic Reflection":("self","buff",None,0,None),"Incognito":("self","buff",(1,1.2,0,0,144),0,"name"),"Polymorph":("self","buff",(0,2.,0,0,240),0,"body"),});ai={("str",1):"Strength",("str",-1):"Weaken",("dex",1):"Agility",("dex",-1):"Clumsy",("int",1):"Cunning",("int",-1):"Feeblemind"};bh=("the spell fizzles","your concentration is disturbed","insufficient mana","more reagents are needed","target cannot be seen","that is too far away","target is too far away","this spell won't work on that","this spell is already in effect","the spell will not adhere to you","you currently have a re","this target already has reactive armor","incognito cannot be cast","you cannot disguise yourself","you cannot polymorph","you cannot incognito","you cannot cast that spell in this form");bi=(("your reactive armor spell has been nullified","Reactive Armor"),("your protection spell has been nullified","Protection"));bj=(("you currently have a reflect spell","Magic Reflection"),("you currently have a reactive armor spell","Reactive Armor"));bk=("you can move!","you can move again!","you are no longer frozen");bl=(("you feel a bit nauseous",1),("you feel disoriented and nauseous",2),("you begin to feel pain throughout your body",3),("you feel extremely weak and are in severe pain",4),("you are in extreme pain, and require immediate aid",5));bm=(("looks extremely ill",2),("looks ill",1),("stumbles around in confusion and pain",3),("is wracked with extreme pain",4),("begins to spasm uncontrollably",5));bn=("the poison seems to have worn off","you feel cured of poison","you have been cured of all poisons");bo=("","Lesser","Regular","Greater","Deadly","Lethal");bp=frozenset(("paralyze","paralyzed","poison","curse","clumsy","feeblemind","weaken","mindrot","strangle","corpseskin","evilomen","bloodoath","masscurse","mortalstrike"));bq={"buff":(47,154,60),"debuff":(194,45,45),"other":(207,174,42),"dim":(90,90,90)};br=I.lower()+":"
		def l(name):return str(name or "").lower().replace(" ","").replace("-","")
		aj={l(b1[0]):ad+b0 for b0,b1 in enumerate(Kit.MAGERY)};aj["paralyzed"]=aj.get("paralyze",ad);z={l(b2):b2 for b2 in v};z["paralyzed"]="Paralyzed";aJ={"buff":0,"debuff":1};bs=frozenset(l(b3)for b3,b4 in v.items()if b4[1]=="buff");h={"me":True,"debuff":True,"others":True,"stats":True,"icons":True,"rows":be,"warn":0,"bars":False};bZ=dict(h)
		def aK():b.update({"shutting":False,"docked":False,"queue":[],"rd":None,"pend":None,"landings":[],"last_land":None,"para":None,"pois":None,"stats":None,"next_sample":0.,"next_others":0.,"events":[],"icons_seen":False,"next_icons":0.,"warned":{},"rebuild":False,"dead":False,"skills":(0.,0.,-1e9)})
		b={"minimized":False,"shutting":False,"docked":False,"queue":[],"me":0,"name":"","prev_name":("",0.),"body":0,"hooked":False,"ct":None,"ct_looked":False,"ver":0,"active":False,"redraw":False};aK();c={};f={"str":[],"dex":[],"int":[]};n={"g":None,"c":{},"store":({},{}),"slots":[],"nrows":0};aL,ak,b_=Kit.basics(b,I);R=24;C=30;al=42;J=3;aM=24;aN=.5;o={b5:{"g":None,"cells":[],"per":1,"lines":-1,"w":0}for b5 in("player","target")};aO={"rows":(ax,ay),"warn":(0,ah)}
		def aP():Kit.kv_load(ar,";",h,aO)
		def aQ():Kit.kv_save(ar,";",h,("me","debuff","others","stats","icons","rows","warn","bars"),aO)
		def aR():
			p=N()
			try:return "%d,%d,%d"%(int(p.Strength),int(p.Dexterity),int(p.Intelligence))
			except Exception:return ""
		def bt():
			d=time.time();a=["t=%d"%int(d)];g=aR()
			for b in("str","dex","int"):
				for e in f[b]:a.append("e:%s,%d,%d,%d,%d,%s"%(b,e["d"],int(e["t"]),int(e["end"]or 0),1 if e.get("hide")else 0,g))
			for r in c.values():
				if r["who"]or "cast"not in r["srcs"]or "stat"in r["srcs"]or r["sid"]not in bs:continue
				a.append("r:%s,%s,%d,%d,%d"%(r["sid"],r["kind"],int(r["start"]),int(r["end"]or 0),int(r["most"]or 0)))
			Kit.put_var(au,";".join(a))
		def bu(now):
			c=Kit.get_var(au).split(";")
			try:d=float(c[0].split("=",1)[1])if c[0].startswith("t=")else 0.
			except(ValueError,IndexError):d=0.
			if not d or not 0<=now-d<=1800.:return
			e=aR()
			for p in c[1:]:
				try:
					g,j=p.split(":",1);b=j.split(",")
					if g=="e"and b[0]in f and h["stats"]:
						if len(f[b[0]])>=aF:continue
						k,l,a=int(b[1]),float(b[2]),float(b[3])
						if(a and a>now)or(not a and e and len(b)>7 and ",".join(b[5:8])==e):f[b[0]].append({"d":k,"t":l,"end":a or None,"hide":len(b)>4 and b[4]=="1"})
					elif g=="r"and b[0]in z:
						m,a,i=float(b[2]),float(b[3]),float(b[4])
						if a and max(a,i)<=now:continue
						r=u(0,b[0],b[1]if b[1]in aJ else "buff",m);r["end"],r["most"]=a or None,i or None;r["srcs"].add("cast");am(r,now)
				except Exception:continue
		def u(who,sid,kind,now,name=""):
			a=(who,sid);r=c.get(a)
			if r is None:
				r={"key":a,"who":who,"sid":sid,"kind":kind,"start":now,"end":None,"most":None,"srcs":set(),"watch":None,"seen":False,"confirm":0.,"base":None,"level":0,"delta":0,"name":name,"away":0.,"icon":aj.get(sid,ad),"end_src":None,"bar":None};c[a]=r
				if len(c)>aG:bv(a)
			else:
				r["kind"]=kind
				if name:r["name"]=name
			b["ver"]+=1;return r
		def k(key):
			r=c.pop(key,None)
			if r is None:return
			b["ver"]+=1;b["warned"].pop(key,None)
			if r["bar"]:K(r,time.time())
		def am(r,now):
			if r["bar"]:K(r,now)
			if r["sid"]not in bf or r["who"]or not h["bars"]or r["end"]is None or r["end"]<=now:return
			a=z[r["sid"]];API.CreateCooldownBar(r["end"]-now,a,bg);r["bar"]=(a,r["end"])
		def K(r,now):
			a=r["bar"];r["bar"]=None
			if a is not None and a[1]>now:API.DeleteCooldown(a[0])
		def an(key,src):
			r=c.get(key)
			if r is None:return
			r["srcs"].discard(src)
			if not r["srcs"]:k(key)
			else:b["ver"]+=1
		def bv(keep):
			b=sorted(c.values(),key=lambda r:(r["who"]==0,r["start"]))
			for a in b:
				if len(c)<=aG:break
				if a["key"]!=keep:K(c.pop(a["key"]),time.time())
		def aS(r):return(r["sid"],r.get("label"),r["delta"],r["level"],r["who"],r["name"],r["end"]is None,"stat"in r["srcs"],Kit.streamer)
		def ao(r):
			b=r["sid"];a=z.get(b)or r.get("label")or b
			if r["delta"]:a="%s %+d"%(a,r["delta"])
			if r["level"]and b=="poison":a="%s (%s)"%(a,bo[max(1,min(5,r["level"]))])
			if r["who"]:a="%s: %s"%(a,j(r["name"],r["who"])if r["name"]else "someone")
			return a
		def aT(now,force=False):
			s=b["skills"]
			if force or not 0<=now-s[2]<15.:s=b["skills"]=(L("Magery",s[0]),L("Evaluating Intelligence",s[1]),now)
			return s
		def bw(spell,now):
			b=v.get(spell)
			if b is None or b[2]is None:return
			e,f,g,c,d=b[2];h,i,j=aT(now);a=e+f*h+g*i
			if c:a=max(c,a)
			if d:a=min(d,a)
			return max(1.,a)
		def bx(spell,at,now):
			a=b["pend"]
			if a is not None:
				c=a["at"]+a["delay"];b["pend"]=None
				if a["side"]=="self"and at>=c-.05:S(a,b["me"],c,now)
				elif a["side"]=="target"and not a["cursor"]and at>=c+.2:
					e=int(API.LastTargetSerial or 0)
					if e:S(a,e,c,now)
			f=v.get(spell)
			if f is None:b["pend"]=None;return
			d=Kit.spell_info(spell);g=d[3]if d and d[3]else 1.;aT(now,True);b["pend"]={"spell":spell,"sid":l(spell),"at":at,"delay":float(g),"side":f[0],"cursor":False,"body0":b["body"],"name0":b["name"]}
		def by(now):
			p=b["pend"]
			if p is None:return
			a=p["at"]+p["delay"]
			if now<a-.05:return
			if p["side"]=="self":
				if now>=a+.6:b["pend"]=None;S(p,b["me"],a,now)
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
			if c:S(p,c,now,now)
		def S(p,who,at,now):
			f,g=p["spell"],p["sid"];c=v[f];i=b["me"];d=not who or who==i;e=bw(f,now)
			if d and c[4]=="stat"and h["stats"]:b["landings"].append({"sid":g,"t":at,"dur":e or 0.});del b["landings"][:-6];aU(now);return
			m=None if d else API.FindMobile(who);j=str(m.Name or "")if m is not None else "";r=u(0 if d else who,g,c[1],at,j);r["start"]=at;r["srcs"].add("cast")
			if r["end_src"]!="icon":r["end"]=(at+e)if e else None;r["most"]=(at+c[3])if c[3]else None;r["end_src"]="cast"
			r["delta"],r["away"]=0,0.;a=c[4]
			if a=="stat"or(a in("body","name","hidden")and not d):a=None
			r["watch"],r["seen"]=a,False;r["confirm"]=now+2.
			if a=="body":r["base"]=p["body0"]
			elif a=="name":r["base"]=p["name0"]
			b["last_land"]=(r["key"],now);b["warned"].pop(r["key"],None);am(r,now)
		def bz(now,d=False):
			p=b["pend"]
			if p is not None and(d or now>=p["at"]+p["delay"]-.3):b["pend"]=None;return
			a=b["last_land"]
			if a is not None and 0<=now-a[1]<=1.:
				b["last_land"]=None;r=c.get(a[0])
				if r is not None and r["srcs"]==set(("cast",)):k(a[0])
		def aU(now):
			c=[i for i in b["landings"]if 0<=now-i["t"]<=ag+1.];b["landings"]=c
			if not c:return False
			d=False
			for g in("str","dex","int"):
				for e in f[g]:
					if(e["end"]is not None or e["d"]<=0 or not 0<=now-e["t"]<=ag+1.):continue
					for a in reversed(c):
						if a["sid"]in("bless",l(ai[(g,1)]))and abs(e["t"]-a["t"])<=ag and a["dur"]:e["end"],e["cast"]=a["t"]+a["dur"],a["sid"];d=True;break
			if d:U()
			return d
		def bA(stat,d,now):
			a=f[stat];b=0
			for e in a:b+=e["d"]
			if a and b+d==0:del a[:];return
			for i,e in enumerate(a):
				if e["d"]==-d:del a[i];return
			a.append({"d":d,"t":now,"end":None})
			if len(a)>aF:del a[0]
		def bB(vals,now):
			c=b["stats"];b["stats"]=vals
			if c is None:return
			a=False
			for i,e in enumerate(("str","dex","int")):
				d=vals[i]-c[i]
				if abs(d)>30:del f[e][:];a=True
				elif abs(d)>=aD:bA(e,d,now);a=True
			if a:
				p=b["pend"]
				if p is not None and p["side"]=="target"and v[p["spell"]][4]=="stat"and now>=p["at"]+p["delay"]-.4 and h["stats"]:b["pend"]=None;S(p,b["me"],now,now)
				aU(now);U()
		def U():
			k={};h=set();S,D,I=f["str"],f["dex"],f["int"]
			for a in S:
				if a.get("hide"):continue
				for d in D:
					if id(d)in h or d.get("hide")or d["d"]!=a["d"]or abs(d["t"]-a["t"])>aE:continue
					for e in I:
						if id(e)in h or e.get("hide")or e["d"]!=a["d"]or abs(e["t"]-a["t"])>aE:continue
						h.update((id(a),id(d),id(e)));i="bless"if a["d"]>0 else "curse";o=a["end"]or d["end"]or e["end"];aV(k,i,a["d"],min(a["t"],d["t"],e["t"]),o);break
					if id(a)in h:break
			for m in("str","dex","int"):
				for g in f[m]:
					if id(g)in h or g.get("hide"):continue
					i=l(ai[(m,1 if g["d"]>0 else-1)]);aV(k,i,g["d"],g["t"],g["end"])
			for i,j in k.items():
				p="buff"if j[0]>0 else "debuff";r=u(0,i,p,j[1])
				if "stat"not in r["srcs"]:r["start"]=j[1]
				r["srcs"].add("stat");r["delta"]=j[0]
				if r["end_src"]!="icon":r["end"],r["end_src"]=j[2],"stat";r["most"]=None
			for n in[t for t,s in c.items()if not s["who"]and "stat"in s["srcs"]and s["sid"]not in k]:r=c[n];r["delta"]=0;an(n,"stat")
			b["ver"]+=1
		def aV(groups,sid,d,t,end):
			g=groups.get(sid)
			if g is None:groups[sid]=[d,t,end]
			else:
				g[0]+=d;g[1]=min(g[1],t)
				if end is not None and(g[2]is None or end>g[2]):g[2]=end
		def aW():
			for a in[g for g in c if not g[0]]:k(a)
			for d in f:del f[d][:]
			b.update({"stats":None,"pend":None,"landings":[],"para":None,"pois":None})
		def bC(now):
			p=N()
			if p is None:return
			g=int(p.Serial);e=str(p.Name or "");m=bool(p.IsDead);n=bool(p.IsParalyzed);o=bool(p.IsPoisoned);q=bool(p.IsHidden);i=int(p.Graphic or 0);d=(int(p.Strength or 0),int(p.Dexterity or 0),int(p.Intelligence or 0))
			if g!=b["me"]:
				if b["me"]:aW()
				b["me"]=g
			if e!=b["name"]:
				if b["name"]:b["prev_name"]=(b["name"],now)
				b["name"]=e
			if m:
				if not b["dead"]:b["dead"]=True;aW()
				return
			if b["dead"]:b["dead"]=False;b["stats"]=None
			b["body"]=i
			for j,l,a in(("para","paralyzed",n),("pois","poison",o)):
				if a!=b[j]:
					b[j]=a
					if a:u(0,l,"debuff",now)["srcs"].add("flag")
					else:k((0,l))
			for r in list(c.values()):
				if r["who"]or r["watch"]is None:continue
				w=r["watch"]
				if w=="hidden":a=q
				elif w=="body":a=i!=r["base"]
				elif w=="name":a=e!=r["base"]
				else:continue
				if a:r["seen"]=True
				elif r["seen"]:k(r["key"])
				elif w=="hidden"and now>r["confirm"]:k(r["key"])
			if h["stats"]:
				if d[0]and d[1]and d[2]:bB(d,now)
			elif b["stats"]is not None or f["str"]or f["dex"]or f["int"]:
				b["stats"]=None
				for s in f:del f[s][:]
				U()
		def bD(now):
			if not c:return
			d={};f={}
			for r in list(c.values()):
				a=r["who"]
				if not a:continue
				if a not in d:d[a]=API.FindMobile(a)
				m=d[a]
				if m is None:
					if not r["away"]:r["away"]=now;b["ver"]+=1
					if r["watch"]and not r["seen"]and now>r["confirm"]:k(r["key"])
					continue
				if r["away"]:r["away"]=0.;b["ver"]+=1
				try:
					e=f.get(a)
					if e is None:e=f[a]=bool(m.IsDead)
					if e:k(r["key"]);continue
					w=r["watch"]
					if w=="paralyzed":g=bool(m.IsParalyzed)
					elif w=="poisoned":g=bool(m.IsPoisoned)
					else:continue
				except Exception:continue
				if g:
					if not r["seen"]:r["seen"]=True
				elif r["seen"]:k(r["key"])
				elif now>r["confirm"]:k(r["key"])
		def bE(now):
			f=b["rd"]
			if f is None:b["rd"]=D();return
			g=f.new()
			if not g:return
			h=b["name"];i,k=b["prev_name"]
			for d in g:
				c=O(d,Q)
				if c.startswith(br):continue
				a=d.name or "";e=bool(h)and a==h or(i and a==i and 0<=now-k<=5.)
				if e:
					j=Kit.SPELL_WORDS.get(c.strip())
					if j is not None:bx(j[0],min(now,d.at or now),now);continue
				if a and not e and a!="System":bG(c,a);continue
				bF(c,now,not e)
		def bF(low,now,system):
			d=low.strip(" *")
			for t,e in bl:
				if d.startswith(t):
					r=u(0,"poison","debuff",now);r["srcs"].add("line")
					if e!=r["level"]:r["level"]=e;b["ver"]+=1
					return
			if not system:return
			for t in bh:
				if low.startswith(t):
					for f,a in bj:
						if low.startswith(f):
							r=c.get((0,l(a)))
							if r is None:r=u(0,l(a),"buff",now)
							r["srcs"].add("cast")
					p=b["pend"]
					if p is not None and p["sid"]in("reactivearmor","magicreflection")and t=="this spell is already in effect"and(0,p["sid"])not in c:u(0,p["sid"],"buff",now)["srcs"].add("cast")
					bz(now,t=="your concentration is disturbed");return
			for t,a in bi:
				if low.startswith(t):k((0,l(a)));return
			if low.startswith("you cannot move!"):u(0,"paralyzed","debuff",now)["srcs"].add("line")
			elif low.startswith(bk):k((0,"paralyzed"))
			elif d.startswith(bn):k((0,"poison"))
		def bG(low,name):
			for r in c.values():
				if r["who"]and r["sid"]=="poison":break
			else:return
			for t,a in bm:
				if t in low:
					d=name.lower()
					for r in c.values():
						if r["who"]and r["sid"]=="poison"and r["name"]and r["level"]!=a and(r["name"].lower()==d or r["name"].lower()in low):r["level"]=a;b["ver"]+=1
					return
		def aX(kind,c):
			if not b["active"]:return
			for a in c:
				try:d=(kind,str(a.Title or ""),int(a.Graphic or 0),int(a.Timer or 0))
				except Exception:continue
				if len(b["events"])<60:b["events"].append(d);HOST.poked=True
				return
		def bH():Kit.hook_once(b,"hooked",("OnBuffAdded",lambda*a:aX("add",a)),("OnBuffRemoved",lambda*a:aX("remove",a)))
		def bI():
			if not b["ct_looked"]:
				b["ct_looked"]=True
				try:t=A("ClassicUO.Time");m=Y(t,"Ticks")if t is not None else None;b["ct"]=m[0]if m else None
				except Exception:b["ct"]=None
			a=b["ct"]
			if a is None:return
			try:return int(a())
			except Exception:return
		def aY(title,graphic,a,now):
			b=l(title)
			if not b:return
			e="debuff"if b in bp else "buff";r=u(0,b,e,now)
			if "icon"not in r["srcs"]:r["start"]=now
			r["srcs"].add("icon");r["label"]=title
			if graphic:r["icon"]=graphic
			c=None
			if 0<a<0xFFFFFFFF:
				d=bI()
				if d is not None and a>d:c=now+(a-d)/1000.
			if c is not None:r["end"],r["end_src"],r["most"]=c,"icon",None
		def bJ(now):
			f,b["events"]=b["events"],[]
			if not h["icons"]:return
			for g,a,i,j in f:
				b["icons_seen"]=True
				if g=="add":aY(a,i,j,now)
				else:an((0,l(a)),"icon")
			if now>=b["next_icons"]:
				b["next_icons"]=now+aB
				if not b["icons_seen"]and b["next_icons"]-aB>b["started"]+1.:return
				e=set()
				for d in API.ActiveBuffs()or[]:
					a=str(d.Title or "")
					if not a:continue
					e.add(l(a));b["icons_seen"]=True;r=c.get((0,l(a)))
					if r is None or "icon"not in r["srcs"]:aY(a,int(d.Graphic or 0),int(d.Timer or 0),now)
				for k in[p for p,s in c.items()if not p[0]and "icon"in s["srcs"]and p[1]not in e]:an(k,"icon")
		def bK(now):
			if not c:return
			for r in list(c.values()):
				b,a=r["key"],r["srcs"];d=r["end"]
				if r["who"]and r["away"]and now-r["away"]>60. and(d is None or now>d):k(b);continue
				if "icon"in a or "stat"in a or "flag"in a:continue
				if r["watch"]and r["seen"]:continue
				if "line"in a and "cast"not in a:
					if now-r["start"]>60.:k(b)
					continue
				if d is None:
					if not r["watch"]and now-r["start"]>3600.:k(b)
					continue
				if now>max(d,r["most"]or 0)+1.:k(b)
		def bL(now):
			a=h["warn"]
			if not a or not h["me"]:return
			for r in c.values():
				if r["who"]or r["kind"]!="buff"or r["end"]is None:continue
				d=r["end"]-now;e=r["key"]
				if 0<d<=a and b["warned"].get(e)!=r["end"]:b["warned"][e]=r["end"];M(aH,"%s runs out in %d s"%(z.get(r["sid"],r.get("label")or r["sid"]),int(d+.5)),"info",who=r["sid"])
		def ap():return aI,2*Kit.MARGIN+30+Kit.GAP+Kit.pitch(aw)+12
		def X():
			a=m.zone_slot(*ap());e=2*Kit.MARGIN+30+Kit.GAP+12;w=a[0]if a else aI;f=[];c=Kit.pitch(aw);n=m.rows(c,e,h["rows"])if a else h["rows"];g,l,k=m.begin(w,a[1]if a else e+n*c)
			if not b["minimized"]:
				M=Kit.MARGIN;i=w-2*M;m.frame(g);d=M+30+Kit.GAP;Kit.add_section(g,M,d,i,(a[1]-M-d)if a else n*c+12);k["empty"]=Kit.add_label(g,"",M+12,d+10,Kit.HUE_INFO)
				for j in range(n):f.append(bM(g,j,M,d+6+j*c,i,c))
			m.end(g,{"slots":f,"nrows":n});b["redraw"]=True;a7(time.time())
		m=Kit.Window(P,I,b,n,X,ba,bb,default=(60,260),mini=(av,bd),icon=bc,lock=True,clear={"slots":[]})
		def aZ(g,x,y,px):a=G.CreateGumpPic(ad,x,y);a.SetPos(x,y);a.SetWidth(px);a.SetHeight(px);a.SetAcceptMouseInput(False);g.Add(a);return a
		def a_(s,icon,px):s["icon_g"]=icon;s["pic"].Graphic=icon;s["pic"].SetWidth(px);s["pic"].SetHeight(px)
		def bM(g,i,sx,a,IW,rh):s={"row":None,"prev":(None,0.),"vis":True,"icon_g":None,"tip":None,"tx":None,"fw":-1,"col":None,"x":sx,"y":a,"iw":IW};s["pic"]=aZ(g,sx+6,a+2,aC);s["name"]=Kit.add_label(g,"",sx+34,a+1,Kit.HUE_TEXT);s["time"]=Kit.add_label(g,"",sx+IW-50,a+1,Kit.HUE_INFO);b=IW-34-10;s["bw"]=b;s["bg"]=Kit.add_box(g,sx+34,a+rh-9,b,5,.9,"#202020");s["fill"]=Kit.add_box(g,sx+34,a+rh-9,b,5,1.,"#2f9a3c");s["hit"]=Kit.catcher(g,sx,a,IW,rh-2,a0(lambda:n["slots"],i),"");Z(s,False);return s
		def a0(get,i):
			def a(*e):
				a=get()
				if i>=len(a):return
				c=a[i];r=c["row"];b,d=c["prev"]
				if 0<=time.time()-d<=.15:r=b
				if r is None:return
				if r[0]and F():ak(("follow",r[0]))();return
				ak(("clear",r))()
			return a
		def Z(s,on):
			if s["vis"]==on:return
			s["vis"]=on
			for k in("pic","name","time","bg","fill","hit"):
				if s.get(k)is not None:s[k].IsVisible=on
		def bN():
			a=[]
			for r in c.values():
				if r["who"]:
					if not h["others"]:continue
				elif r["kind"]=="buff":
					if not h["me"]:continue
				elif not h["debuff"]:continue
				a.append(r)
			a.sort(key=bO);return a
		def bO(r):a=r["end"];return(1 if r["who"]else 0,aJ.get(r["kind"],2),a if a is not None else 1e18,r["start"])
		def a1(s):
			s=int(s+.999)
			if s<60:return "%ds"%s
			if s<3600:return "%d:%02d"%(s//60,s%60)
			return "%dh %02d"%(s//3600,(s%3600)//60)
		def aq(r,now):
			a=r["end"]
			if a is None:
				if r["sid"]in("reactivearmor","magicreflection")and not r["who"]:return "on",None,False
				return "+"+a1(max(0.,now-r["start"])),None,False
			b=a-now
			if b>0:c=max(.1,a-r["start"]);return a1(b),max(0.,min(1.,b/c)),False
			if r["most"]and now<r["most"]:return "soon",None,True
			return "due"if("stat"in r["srcs"]or "icon"in r["srcs"])else "0s",0.,True
		def a2(r):
			if r["who"]:return("%s on %s, cast by you. Click: clear this row. Alt+click: auto-follow (again to stop)"%(z.get(r["sid"],r["sid"]),j(r["name"],r["who"])if r["name"]else "them"))
			if "stat"in r["srcs"]and r["end"]is None:return "From a stat step; ends when it steps back. Click: clear this row."
			if r["end"]is None and r["sid"]in("reactivearmor","magicreflection"):return "Up until used up (the shard doesn't say when). Click: clear this row."
			return "Click: clear this row"
		aa=("player","target");a3={"player":P,"target":P+".target"}
		def ab():return b.get("row_mode",False)
		def bP(now):
			if 0<=b.get("form_at",0.)-now<=aN:return
			b["form_at"]=now+aN;g=q("player");c=g is not None
			if c!=ab():a4(c)
			elif c:
				for d in aa:
					a=o[d];f=q(d);e=a["w"]
					if f is not None:
						r=E(f)
						if r is None:continue
						e=r[2]
					if a["g"]is None or e!=a["w"]:ae(d,e,max(0,a["lines"]))
		def a4(row):
			b["row_mode"]=row
			if row:
				ac(P);m.close()
				for a in aa:c=q(a);r=E(c)if c is not None else None;ae(a,r[2]if r is not None else 200,0)
				for a in aa:V(a3[a],a,1,lambda s=a:o[s]["g"])
			else:a5();X();m.dock(fit=True,min=ap)
			b["redraw"]=True
		def a5():
			for b in aa:W(a3[b]);a=o[b];g,a["g"]=a["g"],None;a["cells"],a["lines"],a["w"]=[],-1,0;Kit.dispose(g)
		def ae(side,fw,lines):
			c=o[side];a,c["g"]=c["g"],None;fw=max(C+2*J,int(fw));b=max(1,(fw-2*J)//C);h=max(1,lines)*al+2*J;x,y=0,0
			if Kit.is_open(a):x,y=a.GetX(),a.GetY()
			g=G.CreateGump(True,False);Kit.add_section(g,0,0,fw,h,alpha=.6);d=[];n=min(aM,b*max(1,lines));e=J+(fw-2*J-b*C)//2
			for i in range(n):f,j=divmod(i,b);d.append(bQ(g,side,i,e+j*C,J+f*al))
			Kit.place(g,x,y,fw,h);Kit.add_front(g,lines<=0);c.update({"g":g,"cells":d,"per":b,"lines":lines,"w":fw});Kit.dispose(a)
		def bQ(g,side,i,a,b):c={"row":None,"prev":(None,0.),"icon_g":None,"tip":None,"vis":True,"x":a,"y":b,"tw":None};c["pic"]=aZ(g,a+(C-R)//2,b,R);c["time"]=Kit.add_label(g,"",a,b+R+1,Kit.HUE_INFO);c["time"].SetAcceptMouseInput(False);c["hit"]=Kit.catcher(g,a,b,C,al-2,a0(lambda:o[side]["cells"],i),"");return c
		def a6(side,now,mine):
			a=o[side];mine=mine[:aM];f=a["per"];g=(len(mine)+f-1)//f if mine else 0
			if g!=a["lines"]:ae(side,a["w"]or 200,g)
			if a["g"]is None:return
			for i,c in enumerate(a["cells"]):
				r=mine[i]if i<len(mine)else None;h=r["key"]if r is not None else None
				if h!=c["row"]:c["prev"]=(c["row"],now);c["row"]=h
				if r is None:Z(c,False);continue
				Z(c,True);j=r["icon"]
				if j!=c["icon_g"]:a_(c,j,R)
				b,m,l=aq(r,now)
				if r["end"]is None:b=""
				d=Kit.text_px(b)if b else 0
				if d!=c["tw"]:c["tw"]=d;Kit.ui_pos(c["time"],c["x"]+max(0,(C-d)//2),c["y"]+R+1)
				Kit.set_text(c["time"],b,Kit.HUE_BAD if(l or r["kind"]=="debuff")else Kit.HUE_TEXT);k=aS(r)
				if k!=c.get("tipk"):
					c["tipk"]=k;e="%s. %s"%(ao(r),a2(r))
					if e!=c["tip"]:c["tip"]=e;c["hit"].SetTooltip(e)
		def a7(now):
			d=ab()
			if not d and(n["g"]is None or(b["minimized"]and b["docked"])):return
			if not b["redraw"]and b.get("drawn_at",0.)+.25>now>=b.get("drawn_at",0.)and b.get("drawn_ver")==b["ver"]:return
			b["redraw"]=False;b["drawn_at"],b["drawn_ver"]=now,b["ver"];a=bN()
			if d:
				e=T["fn"]()if T["fn"]is not None and q("target")is not None else 0;j=[p for p in a if not p["who"]];k=[w for w in a if e and w["who"]==e]
				if o["player"]["g"]is not None:a6("player",now,j)
				if o["target"]["g"]is not None:a6("target",now,k)
				return
			f=n["c"]
			if b["minimized"]:
				g=f.get("status")
				if g is not None:
					if a:
						t=aq(a[0],now)[0];c="%s: %s %s"%(I,ao(a[0]),t)
						if len(a)>1:c+="  (+%d)"%(len(a)-1)
						c=Kit.fit(c,av-90)
					else:c="%s: no timers"%I
					Kit.set_text(g,c,Kit.HUE_INFO)
				return
			l=n["slots"];Kit.set_text(f["empty"],""if a else "No timers yet; your buffs and casts show here.",Kit.HUE_INFO)
			for i,s in enumerate(l):
				r=a[i]if i<len(a)else None;h=r["key"]if r is not None else None
				if h!=s["row"]:s["prev"]=(s["row"],now);s["row"]=h
				if r is None:Z(s,False);continue
				Z(s,True);bR(s,r,now)
		def bR(s,r,now):
			j=r["icon"]
			if j!=s["icon_g"]:a_(s,j,aC)
			if r["who"]:f,a=(Kit.HUE_INFO if r["away"]else Kit.HUE_TITLE),"other"
			elif r["kind"]=="debuff":f,a=Kit.HUE_BAD,"debuff"
			else:f,a=Kit.HUE_TEXT,"buff"
			c,k,l=aq(r,now)
			if r["who"]and r["away"]:c=c+" (away)"
			o=Kit.text_px(c);d=s["x"]+s["iw"]-8-o
			if d!=s["tx"]:s["tx"]=d;Kit.ui_pos(s["time"],d,s["y"]+1)
			Kit.set_text(s["time"],c,Kit.HUE_BAD if l else Kit.HUE_INFO);g=aS(r);m=d-(s["x"]+34)-6;n=(g,m)
			if n!=s.get("namek"):p=ao(r);s["namek"],s["name_txt"]=n,Kit.fit(p,max(20,m))
			Kit.set_text(s["name"],s["name_txt"],f)
			if k is None:b,a=s["bw"],"dim"
			else:
				b=int(round(s["bw"]*k))
				if l:a="dim"
			e=s["fill"]
			if b!=s["fw"]:
				s["fw"]=b
				if b<=0:e.IsVisible=False
				else:Kit.ui_w(e,b);e.IsVisible=True
			if a!=s["col"]:s["col"]=a;h=bq[a];e.SetBaseColor(h[0],h[1],h[2],255)
			if g!=s.get("tipk"):
				s["tipk"]=g;i=a2(r)
				if i!=s["tip"]:s["tip"]=i;s["hit"].SetTooltip(i)
		def bS(key):
			r=c.get(key)
			if r is None:return
			if "stat"in r["srcs"]:
				for a in("str","dex","int"):
					for e in f[a]:
						b=l(ai[(a,1 if e["d"]>0 else-1)])
						if b==key[1]or(key[1]in("bless","curse")and(e["d"]>0)==(key[1]=="bless")):e["hide"]=True
			k(key)
			if "stat"in r["srcs"]:U()
		a8={"follow":lambda serial:B(serial,I),"clear":bS}
		def bT(w):return(("WINDOW  (what it lists)",(("check","me","Show the buffs on you","Bless, Strength, Protection, Reactive Armor, Magic Reflection, Night Sight and more"),("check","debuff","Show what is done to you (paralyze, poison, curses)","Paralyzed, Poison (with its level), Curse, Clumsy, Feeblemind and Weaken on you"),("check","others","Show your spells on others","What you cast on someone else. Alt+click such a row: auto-follow (again to stop)"),("num","rows","Rows shown:","Rows the window has room for",None,ax,ay,{"clamp":False})),{"sh":140}),("TIMER SOURCES  (your casts always count)",(("check","stats","Watch your stats for Bless, Curse and their kin","A Str, Dex or Int step of %d or more is a spell on you (all three: Bless / Curse); potions show too"%aD),("check","icons","Use the shard's buff icons when it sends them","Exact names and times when the shard sends icons (a classic shard sends none)")),{"sh":90}),("TAZUO'S COOLDOWN BARS",(("check","bars","Also show Polymorph as a TazUO cooldown bar","Same time as its row here; goes when the timer ends or this is unticked"),),{"sh":64}),("ALERTS  (sound: Settings > Alerts)",(("num","warn","Warn before a buff on you runs out:","One alert this many seconds before it ends (0-%d, 0 = never)"%ah,"s",0,ah,{"clamp":False}),),{"sh":64}))
		def bU(old,new):
			b["redraw"]=True
			if new["icons"]and not old["icons"]:b["next_icons"]=0.
			if new["rows"]!=old["rows"]:b["rebuild"]=True
			if new["warn"]!=old["warn"]:b["warned"]={}
			if new["bars"]!=old["bars"]:
				a=time.time()
				for r in list(c.values()):(am if new["bars"]else K)(r,a)
		af=Kit.Page(h,bT,aQ,bU,{"ldy":4,"lgap":12,"fw":40})
		def a9(serial=None):
			f=time.time();g=b["me"];d=[]
			for r in c.values():
				e=r["who"]or g
				if serial is not None and e!=serial:continue
				a=r["end"];d.append({"spell":z.get(r["sid"],r.get("label")or r["sid"]),"serial":e,"you":not r["who"],"kind":r["kind"],"end":a,"left":(a-f)if a is not None else None,"icon":r["icon"],"level":r["level"],"delta":r["delta"]})
			return d
		aP()
		def bV():
			a=time.time();aK();b.update({"active":True,"redraw":True,"started":a,"minimized":m.start_min()})
			for r in c.values():K(r,a)
			c.clear()
			for d in f:del f[d][:]
			aP();bu(a);U();bH();H(aH,"Buff about to run out",490);b["row_mode"],b["form_at"]=False,0.
			if q("player")is not None:a4(True)
			else:X();m.dock(fit=True,min=ap)
			HOST.services["spelltimers.list"]=a9;aL.service("look.hud.timers",lambda:ak.add("redraw"))
		def bW():
			a=time.time();bP(a)
			if n["g"]is None and not ab():return
			if n["g"]is not None and Kit.closed(n):return
			while b["queue"]:
				c=b["queue"].pop(0);f=c[0]if isinstance(c,tuple)else c
				if c=="redraw":
					if not ab():X()
					else:
						for g in aa:
							d=o[g]
							if d["g"]is not None:ae(g,d["w"]or 200,max(0,d["lines"]))
						b["redraw"]=True;e["dirty"]=True
				elif m.action(c):pass
				elif f in a8:a8[f](c[1])
			if b["rebuild"]:
				b["rebuild"]=False
				if not ab()and not b["minimized"]and h["rows"]!=n["nrows"]:X()
			bJ(a)
			if not 0<=b["next_sample"]-a<=az:b["next_sample"]=a+az;bC(a)
			bE(a);by(a)
			if bX()and not 0<=b["next_others"]-a<=aA:b["next_others"]=a+aA;bD(a)
			bK(a);bL(a);a7(a)
		def bX():
			for k in c:
				if k[0]:return True
			return False
		def bY():
			b["shutting"]=True;b["active"]=False;ac(P)
			if HOST.services.get("spelltimers.list")is a9:HOST.services.pop("spelltimers.list",None)
			a=time.time()
			for r in c.values():K(r,a)
			a5();m.close();aQ();bt();aL.close()
		return{"start":bV,"tick":bW,"stop":bY,"client_tick":True,"config_height":af.height,"build_config":af.build,"poll_config":af.poll,"config_closed":af.closed}
	def ar():
		aa="swing";z="Swing Bar"
		try:from System import DateTime
		except Exception:DateTime=None
		a6=[(0,4,-10,"Starving"),(5,9,-5,"Hungry"),(10,14,0,"Fed"),(15,19,0,"Full"),(20,20,0,"Stuffed"),];aE=300;aF=20;a7=[("lich lord",90),("lich",70),("dragon",90),("daemon",90),("troll",60),("ogre lord",85),("ogre",65),("orc captain",80),("orc",55),("ettin",55),("skeleton",50),("zombie",35),("rat",25),("headless",30),("mongbat",10),];ac=60;O,P=0,120;Q="CTRL+SHIFT+T";aG="CTRL+SHIFT+R";ad="CTRL+SHIFT+UP";af="CTRL+SHIFT+DOWN";aH="CTRL+SHIFT+RIGHT";aI="CTRL+SHIFT+LEFT";a8,a9=300,300;ba,bb=53,"#b8913a";bc,bd=63,"#3fa34d";be,bf=946,"#6b6b6b";ag=10;aJ=250;aK=5.;aL="SwingTimer_history";bg=("you have been disarmed","your weapon has been disarmed");bh=("you have been knocked off","you fall off of your mount","you fall off your mount");bi=("system","");aM="swing.notice";aN=30.;aO,aj,R,al=68,53,33,946;I=Kit.HUE_TEXT;i,A,m,WR="Swordsmanship","Fencing","Mace Fighting","Wrestling";T="Archery";_W=[("Broadsword",45,i,(3934,3935)),("Cutlass",45,i,(5185,5184)),("Katana",58,i,(5119,5118)),("Longsword",35,i,(3937,3936)),("Scimitar",30,i,(5046,5045)),("Viking Sword",30,i,(5049,5050)),("Thin Longsword",35,i,(5048,5047)),("Butcher Knife",40,i,(5110,5111)),("Cleaver",40,i,(3779,3778)),("Skinning Knife",40,i,(3780,3781)),("Axe",37,i,(3913,3914)),("Battle Axe",31,i,(3911,3912)),("Double Axe",37,i,(3915,3916)),("Executioner's Axe",37,i,(3909,3910)),("Large Battle Axe",29,i,(5115,5114)),("Two Handed Axe",31,i,(5187,5186)),("Pickaxe",35,i,(3718,3717)),("Hatchet",41,i,(3907,3908)),("Bardiche",26,i,(3917,3918)),("Halberd",25,i,(5182,5183)),("Dagger",55,A,(3922,3921)),("Kryss",53,A,(5121,5120)),("Short Spear",50,A,(5123,5122)),("Spear",46,A,(3938,3939)),("War Fork",45,A,(5125,5124)),("Pitchfork",45,A,(3719,3720)),("Club",40,m,(5044,5043)),("Hammer Pick",30,m,(5181,5180)),("Mace",30,m,(3932,3933)),("Maul",30,m,(5179,5178)),("War Axe",40,m,(5040,5039)),("War Hammer",31,m,(5177,5176)),("War Mace",26,m,(5127,5126)),("Quarter Staff",48,m,(3721,3722)),("Gnarled Staff",33,m,(5112,5113)),("Black Staff",35,m,(3568,3569)),("Shepherd's Crook",30,m,(3713,3714)),("Bow",20,T,(5042,5041)),("Crossbow",18,T,(3920,3919)),("Heavy Crossbow",10,T,(5117,5116)),];am={}
		for bj,bk,bl,bm in _W:
			for _g in bm:am[_g]=(bj,bk,bl)
		bn=("Fists",30,WR);bo={562,563,564,567,568,569,570,571,572};bp=[("supremely accurate",10),("exceedingly accurate",8),("eminently accurate",6),("surpassingly accurate",4),("accurate",2)]
		def U(a,b):
			v=(a+100)*b
			if v<=0:v=1
			return 15000./v*1000.
		def an(hunger):
			h=int(round(max(0,min(20,hunger))))
			for a,b,c,d in a6:
				if a<=h<=b:return c,d
			return 0,"?"
		def bq(b,c,d,hunger):e,f=an(hunger);a=(max(b,-49.9)+50.)/((max(c,-49.9)+50.)*2.);a*=1.+d/100.;return max(0.,min(1.,a*(1.+e/100.)))
		def l():return time.time()*1000.
		def ao():
			for b in("OneHanded","TwoHanded"):
				a=API.FindLayer(b)
				if a and int(a.Graphic)in am:c,d,e=am[int(a.Graphic)];return c,d,e,br(a)
			return bn+(0,)
		Y={}
		def br(item):
			a=int(item.Serial);c=Y.get(a)if a else None
			if c is not None and time.time()<c[1]:return c[0]
			d=(item.Name or "").lower()
			if "accurate"not in d:d=(API.ItemNameAndProps(a,False)or "").lower()
			b=0
			for e,p in bp:
				if e in d:b=p;break
			if a:
				if len(Y)>50:Y.clear()
				Y[a]=(b,time.time()+(1e9 if b else 2.))
			return b
		def ap(mob,a,name=None):
			if a is not None:return a
			if mob is None:return q["enemy_default"]
			name=(mob.Name or ""if name is None else name).lower()
			for b,c in a7:
				if b in name:return c
			return 100 if mob.IsHuman else q["enemy_default"]
		def r(key,default):
			try:return float(Kit.get_var(key,str(default)))
			except Exception:return float(default)
		def o(key,value):Kit.put_var(key,str(value))
		def bs(v):
			try:return int(max(O,min(P,int(round(float(v))))))
			except Exception:return ac
		q={"enemy_default":ac};b8=dict(q);st={"minimized":False,"shutting":False,"docked":False,"queue":[]};c={"g":None,"c":{},"store":({},{}),"bar_w":109,"x1":0,"row1":0,"food_w":[0]*21,"fill_w":-1,"fill_state":None,"shown":{},"tips":{},"active":False,"closing":False,"wait":None};aP,b9,aq=Kit.basics(st,z)
		def bt():q["enemy_default"]=bs(r("swingtimer_enemy_default",ac))
		def bu():o("swingtimer_enemy_default",q["enemy_default"])
		bt()
		class State:last_swing=None;cycle_ms=None;gaps=[];gaps_weapon=None;history={};slow=[];dirty=False;paused_at=None;target_serial=0;enemy_override=None;hunger=aF;hunger_clock=l();seen_sounds=set();sounds=[];keys=[];notice=None
		S=State()
		def aQ():
			if not S.gaps:return
			return sum(S.gaps)/float(len(S.gaps))
		def aR(name):return name.replace("|","/").replace(";","/")
		def aS(weapon):
			a=(weapon[0],int(weapon[1]))
			if S.gaps_weapon==a:return False
			b=(aR(a[0]),a[1])
			if a not in S.history and b in S.history:S.history[a]=S.history.pop(b)
			S.gaps_weapon=a;S.gaps=S.history.setdefault(a,[]);S.slow=[];return True
		k={"saved_at":0.,"save":False,"import":False}
		def aT(text,c):
			b={}
			for d in text.split(c):
				p=d.strip().split("|")
				if len(p)!=3 or not p[0]:continue
				try:e=int(p[1]);a=[float(h)for h in p[2].split(",")if h.strip()]
				except Exception:continue
				a=[t for t in a if t>=aJ][-ag:]
				if a:b[(p[0],e)]=a
			return b
		def bv():
			S.history={};S.gaps,S.gaps_weapon,S.dirty,S.slow=[],None,False,[];a=Kit.get_var(aL)
			if a:S.history=aT(a,";")
			k["import"]=not S.history
		def bw():
			if l()<k.get("import_next",0.):return
			k["import_next"]=l()+1000.
			try:a=int(API.Player.Serial)
			except Exception:a=0
			if not a:return
			k["import"]=False
			try:
				b=Kit.data_path("_swing_timer_{}.txt".format(a))
				if not os.path.exists(b):return
				with open(b,"r")as f:d=f.read()
			except Exception:return
			e=aT(d,"\n");n=0
			for c,g in e.items():
				if not S.history.get(c):S.history[c]=g;n+=1
			if not n:return
			S.gaps_weapon=None;S.dirty=True;ar();aq("brought over learned swings of %s from the old data file."%Kit.count(n,"weapon"),Kit.HUE_GOOD)
		def ar():k["save"]=False;a=["%s|%d|%s"%(aR(h),p,",".join("%.0f"%t for t in b))for(h,p),b in sorted(S.history.items())if b];Kit.put_var(aL,";".join(a));S.dirty=False;k["saved_at"]=l()
		def bx(gap,formula):
			a=aQ()
			if gap<aJ or gap>(a or formula)+3000:S.slow=[];return
			if a is not None and gap>a*1.15:
				S.slow.append(gap)
				if len(S.slow)<3:return
				S.gaps[:]=S.slow;S.slow=[];aU("Slow: low stamina",aj)
			else:S.slow=[];S.gaps.append(gap)
			if len(S.gaps)>ag:del S.gaps[:-ag]
			S.dirty=True
		def at(a):
			if S.paused_at is not None:
				if S.last_swing is not None:S.last_swing+=max(0.,a-S.paused_at)
				S.paused_at=a
			b=ao();c=U(int(API.Player.Stamina),b[1]);d=aS(b)
			if S.last_swing is not None and not d:bx(a-S.last_swing,c)
			S.last_swing=a;S.cycle_ms=aQ()or c
		def by(a):
			try:return max(0.,(DateTime.Now-a.Time).TotalMilliseconds)
			except Exception:return 0.
		def bz(a):
			b=int(a.Index)
			if b not in bo:return
			return(b,int(a.X),int(a.Y),str(a.Time),l()-by(a))
		def bA(snd,p):
			d,a,b,e,f=snd
			if a!=int(p.X)or b!=int(p.Y):return
			c=(d,a,b,e)
			if c in S.seen_sounds:return
			S.seen_sounds.add(c)
			if len(S.seen_sounds)>200:S.seen_sounds.clear()
			at(f)
		def bB(*e):
			if not c.get("active"):return
			for f in e:
				try:a=bz(f)
				except Exception:continue
				if a is not None and len(S.sounds)<50:
					S.sounds.append(a)
					if not d.get("fast"):
						b=d.get("xy")
						if b is None or(a[1],a[2])==b:HOST.poke("hud.swing",False)
				return
		bC=[False]
		def aU(text,hue):S.notice=(text,hue,l()+4000.)
		C={"rd":None,"clock":0.,"own":(z.lower(),)}
		def bD():
			a=set([z.lower()])
			for t in[APP_NAME]+[b.title for b in HOST.slots]:
				t=str(t or "").strip().lower()
				if t:a.add(t)
			return tuple(a)
		def bE():
			d=C["own"]
			for a in C["rd"].new(time.time()-Journal.read_at>=.5):
				b=a.low
				if b.startswith(d)or str(a.name or "").lower()not in bi:continue
				for e,c in((bg,("Disarmed!","You were disarmed")),(bh,("Dismounted!","You were dismounted"))):
					if any(g in b for g in e):aU(c[0],R);M(aM,c[1]);break
		bF=[("simply too full to eat any more",20,20),("but you are stuffed",20,20),("but are still extremely hungry",0,4),("begin to feel more satiated",5,9),("you feel much less hungry",10,14),("feel quite full after consuming",15,19),];aV={"rd":None}
		def bG():
			d=aV["rd"]
			if d is None:aV["rd"]=D();a=Journal.recent(aN)
			else:a=d.new()
			if not a:return
			try:e=float(DateTime.Now.Ticks)
			except Exception:e=time.time()*1e7
			for b in a:
				if b.ticks>1e12 and(e-b.ticks)/1e7>aN:continue
				g=b.low
				for h,f,c in bF:
					if h in g:au(max(f,min(c,S.hunger+3 if f!=c else c)));break
		def au(value):aC[0]=True;S.hunger=float(max(0,min(20,value)));S.hunger_clock=l();o("swingtimer_hunger",S.hunger)
		def bH():
			b=l()-S.hunger_clock;a=aE*1000.
			if b>=a:c=int(b//a);S.hunger=max(0.,S.hunger-c);S.hunger_clock+=c*a;o("swingtimer_hunger",S.hunger)
		av=" Alt+click: auto-follow (again to stop)"
		def s(what,value):
			if len(S.keys)<50:S.keys.append((what,value));HOST.poke()
		def bI(serial):
			if serial:S.target_serial=int(serial);S.enemy_override=None
		def bJ():
			while S.keys:
				a,v=S.keys.pop(0)
				if a=="target":aq("target the mobile you are fighting.");J(10,bI)
				elif a=="resync":at(v)
				elif a=="hunger":au(round(S.hunger)+v)
				elif a=="enemy":b=aX();c=ap(b,S.enemy_override);S.enemy_override=max(O,min(P,c+v))
				elif a=="follow":
					b=d.get("mob")
					if b is not None:B(int(b.Serial),z)
					else:aq("no target to follow.")
		bK=((Q,lambda:s("target",None),"pick the mobile you fight"),(aG,lambda:s("resync",l()),"restart the bar (I just swung)"),(ad,lambda:s("hunger",1),"satiety estimate +1"),(af,lambda:s("hunger",-1),"satiety estimate -1"),(aH,lambda:s("enemy",5),"enemy skill +5"),(aI,lambda:s("enemy",-5),"enemy skill -5"))
		def bL(fn):
			def a(*a):
				if not HOST.typing():fn()
			return a
		def aW(on):
			for a,b,c in bK:
				if on:HOST.hotkey_on(a,z,bL(b),c)
				else:HOST.hotkey_off(a,z)
		def aX():
			for a in(S.target_serial,API.LastTargetSerial):
				if a:
					m=API.FindMobile(a)
					if m and not m.IsDead:return m
			N=API.Notoriety;return API.NearestMobile([N.Gray,N.Criminal,N.Enemy,N.Murderer],2)
		u=Kit.set_text;bM={(False,False):400.,(False,True):200.,(True,False):200.,(True,True):100.};bN,bO=50.,800.;aw="swingtimer_kite";bP={"close":"#E8C25A","turn":"#3CD070","far":"#E04040","idle":"#C8C8C8"};bQ={"close":Kit.HUE_TITLE,"turn":Kit.HUE_GOOD,"far":Kit.HUE_BAD,"idle":Kit.HUE_INFO};f={"on":bool(int(r(aw,1)or 0)),"steps":{},"xy":None,"at":0.,"stat0":None,"swing0":None,"px":None,"state":None,"tiles":None};n,K=16,34;aY=3;E=max(0.,min(100.,r("swingtimer_bg_opacity",85)));ax={"f":None}
		def aZ():return Kit.is_open(c["c"].get("gump"))
		def ay(hue,color,h):
			if Kit.pic_size(Kit.LINE_BLUE)[0]>0:
				t=Kit.add_tiled(c["c"]["gump"],Kit.LINE_BLUE,c["x1"],n,1,h,hue=hue)
				if t is not None:return t
			return Kit.add_box(c["c"]["gump"],c["x1"]+1,n+1,1,h,1.,color)
		def bR():c["row1"]=c["bar_w"]+5+max(Kit.text_w("15.0s"),ak());return c["row1"]+2*aY+16,58
		def az(x=None,y=None):
			k=x is None
			if k:x=int(r("swingtimer_x",a8));y=int(r("swingtimer_y",a9))
			d=c["c"];o=d.get("gump");d.clear();l=Kit.pic_size(Kit.LINE_RED)[0];h=Kit.pic_size(Kit.LINE_BLUE)[1]or 8;c["bar_w"]=l or 109;w,i=bR();c["x1"]=g=8+aY
			if k:x,y=Kit.adapt(x,y,w,i)
			b=G.CreateGump(True,True);Kit.place(b,x,y,w,i);d["gump"]=b;Kit.add_window_frame(b,w,i,corners=False);d["section"]=Kit.add_section(b,8,8,w-16,i-16);e["bg"][b]=[d["section"]];a2()
			if l>0:Kit.add_pic(b,Kit.LINE_RED,g,n)
			else:Kit.add_tiled(b,Kit.SECTION_TILE,g,n,109,9,1.)
			d["fills"]={"fill":ay(ba,bb,h),"ready":ay(bc,bd,h),"paused":ay(be,bf,h)}
			for p in d["fills"].values():p.IsVisible=False
			d["kite"]={}
			for q,s in bP.items():d["kite"][q]=t=Kit.add_box(b,g,n-1,2,h+2,1.,s);t.IsVisible=False
			d["kite_lbl"]=Kit.add_label(b,"",g,n-2,I);d["kite_lbl"].SetAcceptMouseInput(False);f.update({"px":None,"state":None,"tiles":None});d["swing"]=Kit.add_label(b,"",g+c["bar_w"]+5,n-2,I);d["notice"]=m=Kit.add_label(b,"",g+4,n-2,R);m.SetAcceptMouseInput(False);m.IsVisible=False;d["hit"]=Kit.add_label(b,"",g,K,al);d["food"]=Kit.add_label(b,"",g+c["row1"]-Kit.text_w("Food 20/20"),K,I);c["food_w"]=[Kit.text_px("Food %d/20"%v)for v in range(21)];j=c["row1"]//2;d["tip_bar"]=Kit.catcher(b,g-2,n-4,c["row1"]+4,18,a_,a0(None),movable=True);d["tip_hit"]=Kit.catcher(b,g-2,K-2,j,18,a_,aA(None),movable=True);d["tip_food"]=Kit.catcher(b,g+j,K-2,c["row1"]-j+2,18,lambda*a:None,a1(),movable=True);c["fill_w"],c["fill_state"],c["shown"],c["tips"]=-1,None,{},{};c["notice_shown"]=None;G.AddControlOnDisposed(b,bY(b));Kit.add_front(b);Kit.on_moved(b,aB);Kit.dispose(o)
		ca=None
		def Z(key,text):
			a=c["c"].get(key)
			if a is None or c["tips"].get(key)==text:return
			c["tips"][key]=text;a.SetTooltip(text)
		def a_(*a):
			if F():s("follow",None)
		def a0(info):
			a="Time to your next swing. Green: ready; grey: paused (no war mode or target)."
			if info is not None:b,c,d,n=info;a+=" %s, speed %d, swing %.1f s (%s)."%(b,c,d/1000.,"learned from %s"%Kit.count(n,"swing")if n else "formula")
			return a+av
		def aA(info):
			if info is None:return "Chance to hit your target; set it with %s.%s"%(Q,av)
			a,b,c,d,e,f=info;return("Chance to hit %s: your %s %.1f vs their assumed %d, accuracy +%d%%, satiety %+d%%; set the target with %s.%s"%(a[:20],b,c,d,e,f,Q,av))
		def a1(label="",mod=0):return("Satiety estimate%s, %+d%% to hit: drops 1 every %d min, rises when you eat%s. Adjust: %s / %s."%((": "+label.lower())if label else "",mod,aE//60,""if aC[0]else " (none seen yet, so grey)",ad,af))
		def a2():c["c"]["section"].SetAlpha(E/100.*Kit.SECTION_ALPHA)
		def bS(i,state):
			a=int(c["bar_w"]*max(0,min(1000,i))/1000);d,e=c["fill_w"],c["fill_state"]
			if a==d and state==e:return
			c["fill_w"],c["fill_state"]=a,state;f=c["c"]["fills"];g=e if d>0 else None;b=state if a>0 else None
			if b is not None:Kit.ui_w(f[b],a)
			if g!=b:
				for h,j in((g,False),(b,True)):
					if h is not None:f[h].IsVisible=j
		def bT(p,t):
			a=(int(p.X),int(p.Y));b,i=f["xy"],f["at"]
			if a==b:return
			f["xy"],f["at"]=a,t
			if b is None:return
			c=max(abs(a[0]-b[0]),abs(a[1]-b[1]));e=t-i
			if not(0<c<=4 and 0<e<=700.*c):return
			g=max(bN,min(bO,e/float(c)));h=a3(p);d=f["steps"].get(h);f["steps"][h]=g if d is None else d+(g-d)*.15
		def a3(p):return(bool(p.IsMounted),bool(p.IsRunning))
		def bU(p):a=a3(p);v=f["steps"].get(a);return v if v is not None else bM[a]
		def bV(a,step):return int(1+(a/2.)/max(1.,step))
		def bW(dist,a):
			if dist is None:return "idle"
			return "close"if dist<a else("turn"if dist==a else "far")
		def bX(p,mob,cycle,stat,j):
			a=c["c"].get("kite")
			if not a:return
			h=c["c"].get("kite_lbl")
			if not f["on"]or S.notice is not None:
				if f["state"]is not None:a[f["state"]].IsVisible=False;f["state"]=None;f["tiles"]=None;Kit.set_text(h,"")
				return
			d=float(cycle)
			if f["swing0"]!=S.last_swing or f["stat0"]is None:f["swing0"],f["stat0"]=S.last_swing,stat
			elif stat!=f["stat0"]:
				k=U(f["stat0"],j)
				if k>0:d=d*U(stat,j)/float(k)
			l=max(.02,min(.98,(d/2.)/max(1.,float(cycle))));e=c["x1"]+int(c["bar_w"]*l);g=bV(d,bU(p));i=None
			if mob is not None:
				try:i=int(mob.Distance)
				except Exception:i=None
			b=bW(i,g)
			if b!=f["state"]:
				if f["state"]is not None:a[f["state"]].IsVisible=False
				a[b].IsVisible=True;f["state"]=b;f["px"]=None;f["tiles"]=None
			if e!=f["px"]:f["px"]=e;a[b].SetPos(e,n-1);h.SetPos(e+4,n-2)
			if g!=f["tiles"]:f["tiles"]=g;Kit.set_text(h,str(g),bQ[b])
		def bY(g):
			def a(*a):
				if c["closing"]or c["c"].get("gump")is not g:return
				aB();c["c"].clear();ab("swing")
			return a
		def aB():
			g=c["c"].get("gump")
			if Kit.is_open(g)and not ai(aa)and g.GetX()>TAB_X//2:o("swingtimer_x",g.GetX());o("swingtimer_y",g.GetY())
		aC=[False]
		def a4():return "{:.0f}/20 {}".format(S.hunger,an(S.hunger)[1])
		def aD(a,b):return "%s / %s"%(a,b.rsplit("+",1)[1])
		cb={}
		def a5(w):a=((aD(Q,aG),"pick the target / restart the bar"),(aD(ad,af),"satiety estimate +1 / -1"),(aD(aH,aI),"enemy skill +5 / -5"));return(("WINDOW",(("gap",32),("check","kite","Show the kite marker on the bar","Turn-back point and tiles to kite out; colour: too close, turn now, too far",{"h":-32}),("slider","opacity","Background opacity:","How solid the window's black inside is (0-100)",0,100,{"lgap":12,"sdy":8,"sw":160})),{"sh":96,"ldy":4}),("HIT CHANCE",(("num","enemy","Enemy skill:","Skill assumed for an unknown monster; players count as GM (%d-%d)"%(O,P),None,O,P,{"lgap":8,"fw":44,"stay":True}),("slider","satiety","Satiety estimate:","How well fed you are, 0 (starving) to 20 (stuffed); low lowers the hit chance",0,20,{"dx":220,"lw":150,"sdy":8,"sw":120,"unit":a4()})),{"sh":68,"ldy":4}),("HOTKEYS",[h for b,g in a for h in(("note",b,{"stay":True}),("note",g,{"dx":330}))],{"sh":100}))
		bZ=Kit.Page(q,a5)
		def b_(g,x,y,w):ax["f"]=Kit.Form(g,x,y,w,{"kite":f["on"],"opacity":int(round(E)),"enemy":q["enemy_default"],"satiety":int(round(S.hunger))},a5(w))
		def b0():ax["f"]=None
		def b1():
			nonlocal E;b=ax["f"]
			if b is None:return
			a,c=b.read(),b.vals;b.vals=a
			if a["opacity"]!=c["opacity"]:
				E=float(a["opacity"]);o("swingtimer_bg_opacity",E)
				if aZ():a2()
			if a["enemy"]!=c["enemy"]:q["enemy_default"]=a["enemy"];bu();d["slow_clock"]=0.
			if a["satiety"]!=c["satiety"]:au(a["satiety"])
			Kit.set_text(b.c["satiety_lbl"],a4())
			if a["kite"]!=f["on"]:f["on"]=a["kite"];o(aw,1 if a["kite"]else 0)
		d={}
		def b2():
			c["closing"],c["active"]=False,True;k.update({"saved_at":l(),"save":False});bv();del S.sounds[:],S.keys[:];S.last_swing=S.cycle_ms=S.notice=None;C.update({"rd":D(),"clock":0.,"own":bD()});H(aM,"Disarmed or dismounted",946);S.hunger=max(0.,min(20.,r("swingtimer_hunger",aF)));S.hunger_clock=l();f["on"]=bool(int(r(aw,1)or 0));f["steps"].clear();f["xy"],f["stat0"],f["swing0"]=None,None,None;V(aa,"target",0,lambda:c["c"].get("gump"));c["wait"]=time.time()
			if not ah("target",c["wait"],aK):c["wait"]=None;az();X()
			else:ae(lambda:c["active"]and c["wait"]is not None)
			aP.service("look.hud.swing",lambda:c.update({"redo":True}));aW(True);Kit.hook_once(bC,0,("SoundPlayed",bB));d.update({"slow_clock":0.,"eat_clock":0.,"weapon":ao(),"mob":None,"my_skill":0.,"mob_skill":ap(None,None),"mob_name":"","skill_of":None,"skill_clock":0.,"timer_clock":0.,"timer_mode":None,"fast":False,"react":None})
		def b3():
			if c["wait"]is not None:
				if ah("target",c["wait"],aK):return
				c["wait"]=None;az();X()
			if not aZ():d["fast"]=False;return
			if c.pop("redo",False):y=c["c"]["gump"];az(y.GetX(),y.GetY());e["dirty"]=True
			t=l();p=N()
			if p is None:return
			while S.sounds:bA(S.sounds.pop(0),p)
			if S.keys:bJ()
			if t-C["clock"]>=100:C["clock"]=t;bE()
			z=(S.target_serial,API.LastTargetSerial,bool(p.InWarMode))
			if z!=d["react"]:d["react"]=z;d["slow_clock"]=t-250
			if t-d["slow_clock"]>=250:
				d["slow_clock"]=t;d["xy"]=(int(p.X),int(p.Y));d["weapon"]=ao();P=S.gaps_weapon
				if aS(d["weapon"]):
					S.cycle_ms=None
					if P is not None and d["weapon"][2]==T:S.last_swing=None;at(t)
				if S.dirty and t-k["saved_at"]>=5000:k["save"]=True
				a=d["mob"]=aX();q=(a.Name or "")if a is not None else "";d["mob_skill"]=ap(a,None,q);d["mob_name"]=(j(q,a.Serial)if q else "target")if a is not None else ""
				if d["weapon"][2]!=d.get("skill_of")or t-d.get("skill_clock",0.)>=1000:d["skill_of"],d["skill_clock"]=d["weapon"][2],t;d["my_skill"]=L(d["weapon"][2])
				bH()
				if t-d["eat_clock"]>=1000:d["eat_clock"]=t;bG()
			A,n,B,r=d["weapon"];D=int(p.Stamina);g=S.gaps;Q=sum(g)/float(len(g))if g else None;o=Q or U(D,n);a=d["mob"];h=bool(p.InWarMode)and a is not None
			if not h:
				if S.paused_at is None:S.paused_at=t
				E=S.paused_at
			else:
				if S.paused_at is not None:
					if S.last_swing is not None:S.last_swing+=t-S.paused_at
					S.paused_at=None
				E=t
			b=S.notice
			if b is not None and t>=b[2]:S.notice=b=None
			if S.last_swing is None:f,F,i=1000,0.,o
			else:i=S.cycle_ms or o;s=E-S.last_swing;F=i-s;f=1000 if s>=i else int(s/i*1000)
			bS(f,"paused"if not h else("ready"if f>=1000 else "fill"));bT(p,t);bX(p,a,i,D,n);d["fast"]=h and f<1000
			if b is not c["notice_shown"]:
				c["notice_shown"]=b;G=c["c"]["notice"]
				if b is not None:u(G,b[0],b[1])
				G.IsVisible=b is not None
			H=(h,f>=1000,a is None)
			if H!=d["timer_mode"]or t-d["timer_clock"]>=100:
				d["timer_mode"],d["timer_clock"]=H,t
				if not h:u(c["c"]["swing"],"Paused"if a is not None else "Ready",al)
				elif f>=1000:u(c["c"]["swing"],"Ready",aO)
				else:u(c["c"]["swing"],"%.1fs"%(max(0.,F)/1000.),I)
			m=(A,n,"%.1f"%(o/1000.),len(g))
			if c["shown"].get("bar_tip")!=m:c["shown"]["bar_tip"]=m;Z("tip_bar",a0((A,n,o,len(g))))
			J=c["shown"];v=d["my_skill"];w=S.enemy_override if S.enemy_override is not None else d["mob_skill"];m=(a is not None,d["mob_name"],w,v,B,r,S.hunger)
			if J.get("rows")!=m:
				J["rows"]=m;x=bq(v,w,r,S.hunger);M,V=an(S.hunger)
				if a is not None:u(c["c"]["hit"],"Hit %d%%"%int(round(x*100)),aO if x>=.6 else(aj if x>=.4 else R));Z("tip_hit",aA((d["mob_name"],B,v,w,r,M)))
				else:u(c["c"]["hit"],"Hit --%",al);Z("tip_hit",aA(None))
				O=max(0,min(20,int(round(S.hunger))))
				if u(c["c"]["food"],"Food %d/20"%O,Kit.HUE_INFO if not aC[0]else(R if S.hunger<5 else(aj if S.hunger<10 else I))):Kit.ui_pos(c["c"]["food"],c["x1"]+c["row1"]-c["food_w"][O],K)
				Z("tip_food",a1(V,M))
		def b4():
			if k["import"]and not c["closing"]:
				bw()
				if not k["import"]:d["slow_clock"]=0.
			if k["save"]and S.dirty:ar()
			k["save"]=False
		def b5():return.025 if d.get("fast")else.1
		def b6():return bool(k["save"]or k["import"])
		def b7():
			c["closing"],c["active"]=True,False;aW(False);C["rd"]=None
			if S.dirty:ar()
			aB();W(aa);o("swingtimer_bg_opacity",E);g=c["c"].get("gump");c["c"].clear();Kit.dispose(g);aP.close()
		return{"start":b2,"tick":b3,"stop":b7,"client_tick":True,"config_height":bZ.height,"build_config":b_,"poll_config":b1,"config_closed":b0,"thread_tick":b4,"thread_wanted":b6,"interval":b5}
	def au():
		h="bandage";A="Bandages";ae="BandageAgent_pos";K=3617;af=15.;ag=7.5;ah=.5;t,u=1.,60.;N,P=0.,5.;aj=3.;n=1;al=("you did not stay close enough to heal","you were unable to finish your work");aX=("that being is not damaged","you are too far away to do that","bandages can not be used on that","you cannot heal that","bandages cannot be used on that","that is too far away","that creature may only be healed")+al;aY=("you finish applying the bandages","you apply the bandages, but they barely help","you apply the bandages, but they do not seem","you heal what little damage","you are able to resurrect","you are unable to resurrect","you have cured the target of all poisons");R=50;am,an=0,99;aZ,a_=400,300;ao=60.;ap=60.;aq=.6;ar=10;S,T=0,999;au="bandage.low";av="bandage.hp";aw="bandage.poison";ax="bandage.ready";ay=10;az="BandageAgentStartPct";aA="BandageAgent_timing";aB="BandageAgent_extra";aC="BandageAgent_other";aD="#E8C25A";E=62;q,a0=16,35;f=18;r=8;aE,aF,aG=120,118,104;a1=aE+Kit.GAP+aF+Kit.GAP+aG;d={"cure":True,"low":ar,"others":False,"other_pct":80,"party":True,"pets":True};bw=dict(d)
		def aH():b.update({"phase":"idle","shutting":False,"queue":[],"rebuild":False,"skills":(0.,0.,-1e9),"count":None,"count_at":0.,"low_armed":True,"hp_armed":True,"poison_armed":True,"target":None,"last":None,"pick":False,"begun":False,"by_buff":False,"buff":False,"lt":(0,0.)})
		b={"minimized":False,"shutting":False,"docked":False,"queue":[],"start_pct":R,"band_time":af,"other_time":ag,"buffer":ah,"t0":0.,"deadline":0.,"rd":None};aH();c={"g":None,"c":{"fill":None,"fill_box":None,"label":None,"count":None},"store":({},{}),"bar_w":109,"fill_w":-1,"text":None,"count_text":None,"wide":False};aI,z,i=Kit.basics(b,A);k={"f":None,"typed":None,"applied":None,"since":0.}
		def aJ():a3();a4();a5()
		def a2():aK();aL()
		def a3():
			try:b["start_pct"]=max(am,min(an,int(Kit.get_var(az,str(R)))))
			except Exception:b["start_pct"]=R
		def aK():Kit.put_var(az,str(b["start_pct"]))
		def a4():
			p=Kit.get_var(aA).split("|")
			try:
				if p[0]:b["band_time"]=max(t,min(u,float(p[0])))
				if len(p)>=2 and p[1]:b["buffer"]=max(N,min(P,float(p[1])))
			except ValueError:b["band_time"],b["buffer"]=af,ah
			try:
				v=Kit.get_var(aC)
				if v:b["other_time"]=max(t,min(u,float(v)))
			except ValueError:b["other_time"]=ag
		def aL():Kit.put_var(aA,"%.2f|%.2f"%(b["band_time"],b["buffer"]));Kit.put_var(aC,"%.2f"%b["other_time"])
		def a5():v=dict(a.split("=",1)for a in Kit.get_var(aB).split(";")if "="in a);d["cure"]=v.get("cure","1")!="0";d["others"]=v.get("others","0")=="1";d["party"]=v.get("party")!="0";d["pets"]=v.get("pets")!="0";d["low"]=aM(v.get("low"),S,T,ar);d["other_pct"]=aM(v.get("opct"),1,99,80)
		def aM(text,lo,hi,default):
			try:return max(lo,min(hi,int(text)))
			except(TypeError,ValueError):return default
		def a6():Kit.put_var(aB,"cure=%d;low=%d;others=%d;opct=%d;party=%d;pets=%d"%(int(d["cure"]),d["low"],int(d["others"]),d["other_pct"],int(d["party"]),int(d["pets"])))
		def U():
			if not ai(h):Kit.save_pos(ae,c["g"])
		def a7():a=Kit.pic_size(Kit.LINE_RED)[0];i=Kit.pic_size(Kit.LINE_BLUE)[0];b=a if a>0 and i>0 else 109;j=(max(Kit.text_w("15.0s"),ak())+(90 if d["others"]else 0));c=Kit.text_w("x999");e=b+5+j;g=f+r+c+r+f+r+f;h=max(e,g)+6;return{"bar_w":b,"count_w":c,"row1":e,"row2":g,"sec_w":h,"W":h+16}
		def aN():
			L=a7();k=L["W"];t=Kit.pic_size(Kit.LINE_RED)[0];u,v=Kit.pic_size(Kit.LINE_BLUE);w=d["others"];x,y=Kit.load_pos(ae,(aZ,a_),(k,E));j=c["g"]
			if Kit.is_open(j):x,y=j.GetX(),j.GetY()
			g=G.CreateGump(True,True);Kit.place(g,x,y,k,E);Kit.add_window_frame(g,k,E,corners=False);e["bg"][g]=[Kit.add_section(g,8,8,L["sec_w"],E-16)];g.SetTooltip("%s: one press, one bandage (x = bandages left)"%A);i=8+(L["sec_w"]-L["row1"])//2;h=c["c"];h["fill"]=h["fill_box"]=None;c["bar_w"]=L["bar_w"]
			if t>0 and u>0:Kit.add_pic(g,Kit.LINE_RED,i,q);h["fill"]=Kit.add_tiled(g,Kit.LINE_BLUE,i,q,1,v);h["fill"].SetWidth(0)
			else:Kit.add_tiled(g,Kit.SECTION_TILE,i,q,109,9,1.);h["fill_box"]=Kit.add_box(g,i+1,q+1,1,7,1.,"#3A63A8")
			B=i+L["bar_w"]+5;h["label"]=Kit.add_label(g,"Ready",B,q-2,Kit.HUE_INFO);Kit.catcher(g,i-2,q-4,L["row1"]+4,18,bb,"Bandage in progress and its patient. Alt+click: auto-follow (again to stop)",movable=True);l=8+(L["sec_w"]-L["row2"])//2;b=a0;m=G.CreateGumpItemPic(K,f,f);m.SetPos(l,b);m.SetAcceptMouseInput(False);g.Add(m);Kit.catcher(g,l,b,f,f,z("me"),"Use one bandage on yourself");o=l+f+r;h["count"]=Kit.add_label(g,"",o,b+1,Kit.HUE_INFO);Kit.catcher(g,o,b,L["count_w"],f,lambda*a:None,"Bandages left in your backpack",movable=True);p=o+L["count_w"]+r;a9(g,p,b);Kit.catcher(g,p,b,f,f,ba,"Target someone within %d tile%s for one bandage. Alt+click: auto-follow (again to stop)"%(n,""if n==1 else "s"));s=p+f+r;a8(g,s,b);Kit.catcher(g,s,b,f,f,bc,"One more bandage on your last patient. Alt+click: auto-follow (again to stop)");c.update({"fill_w":-1,"text":None,"count_text":None,"wide":w,"g":g});G.AddControlOnDisposed(g,bd(g));Kit.add_front(g);Kit.on_moved(g,U);Kit.dispose(j);aP()
		bx=None
		def aO(g,x,y,art,ch):
			p=Kit.add_pic(g,art,x,y,hue=53,mouse=False)
			if p is None:Kit.add_label(g,ch,x+5,y+1,Kit.HUE_TEXT);return False
			p.SetWidth(f);p.SetHeight(f);return True
		def a8(g,x,y):
			if not aO(g,x,y,8012,"@"):return
			Kit.add_box(g,x+8,y,10,7,1.,"#101010")
			for r in range(7):Kit.add_box(g,x+9,y+r,(3-abs(r-3))*2+1,1,1.,aD)
		def a9(g,x,y):
			if not aO(g,x,y,8012,"+"):return
			c=f//2
			for a,b,d,e in((c-1,0,2,5),(c-1,f-5,2,5),(0,c-1,5,2),(f-5,c-1,5,2),(c-1,c-1,2,2)):Kit.add_box(g,x+a,y+b,d,e,1.,aD)
		def X(o):
			a=F()
			if a and o is not None:z(("follow",o["serial"]))()
			return a
		def ba(*a):
			if not X(b["last"]):z("other")()
		def bb(*a):X(b["target"]or b["last"])
		def bc(*a):
			if not X(b["last"]):z("again")()
		def bd(g):
			def a(*a):
				if c["g"]is g and not b["shutting"]:U();c["g"]=None;ab(h)
			return a
		def aP():
			e=c["c"]["count"];n=b["count"]
			if e is None:return
			if n is None:a=("",Kit.HUE_INFO)
			else:f=d["low"];a=("x%d"%n,Kit.HUE_BAD if f>0 and n<f else Kit.HUE_INFO)
			if a!=c["count_text"]:c["count_text"]=a;Kit.set_text(e,a[0],a[1])
		def s(a,text,hue=None):
			a=max(0.,min(1.,a));w=int(c["bar_w"]*a);b=c["fill_w"]
			if w!=b:
				c["fill_w"]=w;d=c["c"]["fill"]
				if d is not None:
					Kit.ui_w(d,w)
					if(w>0)!=(b>0)or b<0:d.IsVisible=w>0
				elif c["c"]["fill_box"]is not None:Kit.ui_w(c["c"]["fill_box"],max(1,w-2))
			e=c["c"]["label"]
			if e is not None and(text,hue)!=c["text"]:c["text"]=(text,hue);Kit.set_text(e,text,Kit.HUE_INFO if hue is None else hue)
		def I(kind,text,level="warn"):M(kind,text,level)
		def be():
			a,c,e=b["skills"];d=time.time()
			if d-e>=5.:a,c=L("Healing"),L("Anatomy");b["skills"]=(a,c,d)
			return a>=ao and c>=ap
		def bf(p,hits,hmax):
			a=b["start_pct"]
			if a>0 and hmax>0:
				if hits*100./hmax<=a:
					if b["hp_armed"]:b["hp_armed"]=False;I(av,"Your HP is at %d%%: bandage?"%int(hits*100./hmax))
				else:b["hp_armed"]=True
			if d["cure"]:
				if p.IsPoisoned:
					if b["poison_armed"]and be():b["poison_armed"]=False;I(aw,"Poisoned: a bandage can cure it")
				else:b["poison_armed"]=True
		def bg(now):
			if now<b["count_at"]:return
			b["count_at"]=now+2.;n=0
			for c in API.FindTypeAll(K,API.Backpack)or():n+=int(c.Amount or 1)
			e,b["count"]=b["count"],n;a=d["low"]
			if a>0 and n<a:
				if b["low_armed"]and(n>0 or(e or 0)>0):b["low_armed"]=False;I(au,"No bandages left"if n<=0 else "Only %s left"%Kit.count(n,"bandage"))
			else:b["low_armed"]=True
			aP()
		def Y(m,px,py,reach):return max(abs(int(m.X)-px),abs(int(m.Y)-py))<=reach
		def aQ(m):return aR(str(m.Name or "")or "them",int(m.Serial))
		def aR(name,serial):a=j(name,serial);b=a if len(a)<=ay else a[:ay-1]+".";return{"serial":serial,"name":name,"short":b,"veil":Kit.streamer}
		def ac(p,now,target):
			if b["phase"]!="idle":i("a bandage is already running.");return
			if API.HasTarget("any")or C(h):i("a target cursor is up (aim it or press Esc first).");return
			if p.IsDead:return
			a=API.FindType(K,API.Backpack)
			if not a:s(0.,"Out!",Kit.HUE_BAD);i("out of bandages!",Kit.HUE_BAD);return
			b["rd"].new();API.UseObject(a.Serial);b["count_at"]=min(b["count_at"],now+aq);Z(h,aj);b["target"]=target;b["begun"],b["by_buff"]=False,False;b["phase"],b["deadline"]="cursor",now+aj
		def bh(serial):
			b["pick"]=False
			if serial:z(("on",int(serial)))()
		def aS(p,now,serial):
			m=API.FindMobile(serial)
			if m is None:i("couldn't bandage them (out of sight).",Kit.HUE_BAD);return
			if int(p.Serial)==int(m.Serial):ac(p,now,None);return
			if m.IsDead:i("they are dead.",Kit.HUE_BAD);return
			if not Y(m,int(p.X),int(p.Y),n):i("too far away (%s at most)."%Kit.count(n,"tile"),Kit.HUE_BAD);return
			ac(p,now,aQ(m))
		def bi(now):
			a=int(API.LastTargetSerial)
			if a!=b["lt"][0]:b["lt"]=(a,now)
		def bj(p,now):
			a,c=b["lt"]
			if not a:return
			with Kit.quiet:
				if a==int(p.Serial):return
				m=API.FindMobile(a)
				if m is None or not Y(m,int(p.X),int(p.Y),n+1):return
				if now-c<=4. or(p.Hits>=p.HitsMax and not p.IsPoisoned):return aQ(m)
			return
		def aT(p,now,at,buff=False):
			a=b["phase"]=="heal"and not b["begun"]and not b["by_buff"]
			if b["phase"]=="cursor":l(h)
			if buff and b["phase"]=="heal":return
			if not a:b["target"]=bj(p,now)
			b["t0"]=min(now,at);b["phase"],b["begun"],b["by_buff"]="heal",not buff,buff;b["count_at"]=min(b["count_at"],now+aq)
		def bk(p,now):
			a=bool(API.BuffExists("Healing"));c,b["buff"]=b["buff"],a
			if a and not c:aT(p,now,now,True)
			elif c and not a and b["phase"]=="heal"and b["by_buff"]:return "done"
			return
		def bl(p,now):
			d=b["rd"].new()
			if not d:return
			f=A.lower()+":"
			for a in d:
				e=a.low.strip()
				if e.startswith(f):continue
				if a.name and str(a.name).lower()!="system":continue
				c=O(a,Q).strip()
				if c.startswith("you begin applying the bandages"):aT(p,now,a.at);continue
				if b["phase"]=="idle":continue
				g=b["phase"]=="cursor"or(not b["begun"]and now-b["t0"]<=2.)
				for x in aX:
					if c.startswith(x)and(g or x in al):return e.rstrip(".!")
				if b["phase"]=="heal"and c.startswith(aY):return "done"
			return
		def bm(p,o):
			try:m=API.FindMobile(o["serial"]);a=m is not None and not m.IsDead and Y(m,int(p.X),int(p.Y),n)
			except Exception:a=False
			if not a:API.CancelTarget();i("%s is out of reach; cursor put down."%o["name"],Kit.HUE_BAD);return False
			API.Target(o["serial"]);b["last"]=o;i("bandaging %s."%o["name"]);return True
		def bn(action,p,now):
			if not b["pick"]and b["phase"]=="idle":b["pick"]=True;J(15.,bh,h)
		def bo(action,p,now):
			if b["last"]is None:i("nobody bandaged yet; use the target icon first.")
			else:aS(p,now,b["last"]["serial"])
		def ad(v):return("%.2f"%v).rstrip("0").rstrip(".")
		aU={"follow":lambda action,p,now:B(action[1],A),"me":lambda action,p,now:ac(p,now,None),"other":bn,"again":bo,"on":lambda action,p,now:aS(p,now,action[1])}
		def aV(w):a=("On yourself:","On someone else:","Latency buffer:");b={"stay":True,"tw":50};c=("note","s",{"dx":82+max(Kit.text_w(g)for g in a),"ndy":4,"h":28});e=("Bandage: one on you. Target icon: one on whoever you click (within %d tile%s). Arrow: one more on the last one."%(n,""if n==1 else "s"));d=(int(t),int(u));return(("BANDAGE TIMES",(("text","time",a[0],"Seconds one on yourself takes; applied when you stop typing (%d-%d)"%d,b),c,("text","other",a[1],"Seconds one on someone else takes, much faster on this shard (%d-%d)"%d,b),c,("text","buffer",a[2],"Seconds added for latency before the bar says Done (%d-%d)"%(int(N),int(P)),b),c),{"sh":aE,"align":True}),("ALERTS  (sound: Settings > Alerts)",(("num","box","Alert when your HP is at or under:","One alert per fall to this % or below (0-99, 0 = never)","%",am,an,{"clamp":False}),("check","cure","Alert when poisoned and a bandage can cure it","Once per poisoning, with Healing %d and Anatomy %d or more"%(int(ao),int(ap))),("num","low","Alert when bandages drop under:","One alert when your bandages drop under this (%d-%d, 0 = never)"%(S,T),None,S,T,{"clamp":False})),{"sh":aF}),("WINDOW",[("check","others","Show who the bandage is on (a wider bar)","The bar names your patient. Alt+click the name: auto-follow (again to stop)")]+[("note",m,{"ndy":2})for m in Kit.wrap(e,w-24)[:2]],{"sh":aG}))
		by=Kit.Page(d,aV)
		def bp(g,x,y,w):a=aV(w);c=dict(d,time=ad(b["band_time"]),other=ad(b["other_time"]),buffer=ad(b["buffer"]),box=b["start_pct"]);k.update({"f":Kit.Form(g,x,y,w,c,a,ldy=4,lgap=12,fw=40),"typed":None,"applied":None})
		def aW():k.update({"f":None,"typed":None,"applied":None})
		def bq(text,lo,hi):
			try:v=float(str(text).strip().replace(",","."))
			except(ValueError,TypeError):return
			return v if lo<=v<=hi else None
		def br():
			g=k["f"]
			if g is None:return
			try:a=g.read(True)
			except Exception:aW();return
			g.vals=a
			if a["box"]!=b["start_pct"]:b["start_pct"]=a["box"];b["hp_armed"]=True;aK()
			if a["low"]!=d["low"]:b["count_at"]=0.
			e=False
			for c,i in(("cure","poison_armed"),("others","rebuild"),("low","low_armed")):
				if a[c]!=d[c]:d[c]=a[c];b[i]=True;e=True
			if e:a6()
			h=time.time();f=(a["time"],a["other"],a["buffer"])
			if f!=k["typed"]:k["typed"],k["since"]=f,h;return
			if k["applied"]==f or h-k["since"]<.7:return
			k["applied"]=f;e=False
			for j,(c,l,m)in enumerate((("band_time",t,u),("other_time",t,u),("buffer",N,P))):
				v=bq(f[j],l,m)
				if v is not None and abs(v-b[c])>.001:b[c],e=v,True
			if e:aL()
		aJ()
		def bs():
			aH();b["rd"]=D();aJ()
			for k,a,d in((au,"Bandages running low",490),(av,"HP low: bandage?",497),(aw,"Poisoned (a bandage cures)",480),(ax,"Bandage done",514)):H(k,a,d)
			aN();V(h,"player",0,lambda:c["g"]);aI.service("look.hud.bandage",lambda:b.update({"rebuild":True,"redo":True}))
		def bt():
			p=API.Player
			if p is None:return
			a=time.time()
			if b["queue"]or b["rebuild"]:
				if b["rebuild"]:
					b["rebuild"]=False;r=b.pop("redo",False)
					if c["g"]is not None and(r or c["wide"]!=d["others"]):aN()
				while b["queue"]:
					f=b["queue"].pop(0);m=f[0]if isinstance(f,tuple)else f
					if m in aU:aU[m](f,p,a)
				if c["g"]is None:return
			if p.IsDead:
				if b["phase"]!="idle":l(h)
				b["phase"],b["target"]="idle",None;s(0.,"Dead",Kit.HUE_BAD);return
			bg(a);u,n=p.Hits,p.HitsMax
			if n>0:bf(p,u,n)
			bi(a);e=bl(p,a);v=bk(p,a)
			if e is None:e=v
			if e is not None and e!="done"and b["phase"]!="idle":
				if b["phase"]=="cursor":l(h)
				b["phase"],b["target"]="idle",None;s(0.,"Ready");i("the bandage failed (%s)."%e,Kit.HUE_BAD);return
			if b["phase"]=="heal":
				o=b["target"];g=b["other_time"]if o is not None else b["band_time"];j=a-b["t0"]
				if j>=g+b["buffer"]or e=="done":b["phase"],b["target"]="idle",None;s(1.,"Done",Kit.HUE_GOOD);I(ax,"Bandage done","info")
				else:
					k="%.1fs"%max(0.,g-j)
					if o is not None and c["wide"]:
						if o["veil"]!=Kit.streamer:o.update(aR(o["name"],o["serial"]))
						k="%s %s"%(o["short"],k)
					s(j/g,k,Kit.HUE_TEXT)
				return
			if b["phase"]=="cursor":
				if aa(h,"beneficial"):
					o=b["target"]
					if o is None:API.TargetSelf();q=True
					else:q=bm(p,o)
					l(h)
					if q:b["phase"],b["t0"]="heal",a
					else:b["phase"],b["target"]="idle",None
				elif a>b["deadline"]:
					if API.HasTarget("beneficial"):i("a bandage cursor is up: press Esc or aim it.")
					else:i("no bandage cursor appeared.",Kit.HUE_BAD)
					l(h);b["phase"],b["target"]="idle",None
				return
			t=c["text"]
			if t is None or t[0]not in("Ready","Done","Out!")or(t[0]=="Out!"and(b["count"]or 0)>0):s(0.,"Ready")
		def bu():
			if b["phase"]=="cursor":return.01
			if b["phase"]!="heal":return.1
			a=b["other_time"]if b["target"]is not None else b["band_time"];return min(.1,max(.01,b["t0"]+a+b["buffer"]-time.time()))
		def bv():b["shutting"]=True;l(h);U();W(h);a2();g,c["g"]=c["g"],None;c["c"]["label"]=c["c"]["count"]=None;Kit.dispose(g);aI.close()
		return{"start":bs,"tick":bt,"stop":bv,"client_tick":True,"config_height":lambda w:a1,"build_config":bp,"poll_config":br,"config_closed":aW,"interval":bu}
	def av():
		h="pets";i="Pets";ae="Pets_settings";aJ="Pets_pos";aK="Pets_min";W=440;af,aL=280,46;ag=.25;ah=1.;s={};ai=1.;aM,aj,ak=18,2,24;K=6;u=50;al=130;am=110;q=20;L=1;N=10;P=3.;aN=("the spell fizzles","your concentration is disturbed","insufficient mana","more reagents are needed","you must wait to perform another action");an=3.;ao=(("follow","Follow me","all follow me"),("guard","Guard me","all guard me"),("stay","Stay","all stay"),("come","Come","all come"));R="all kill";aO=dict((bj,bk)for bj,bl,bk in ao);ap=(("pet_follow","Follow","%s follow me"),("pet_guard","Guard","%s guard"),("pet_stay","Stay","%s stay"));z=dict([(bm,bn)for bm,bo,bn in ap]+[("pet_kill","%s kill")]);A=(("","Bandage"),("Heal","Heal (spell)"),("Greater Heal","Greater Heal (spell)"));aq,ar="pets.low","pets.dead";aP="#17171a";aQ,aR,aS="#c22d2d","#2f9a3c","#d39a1c";at="then pick the enemy with the shard's cursor (only on a click)";e={"range":aM,"low":30,"heal":0,"kill":False,"hidden":True};bh=dict(e)
		def au():a.update({"shutting":False,"docked":False,"queue":[],"heal":None,"confirm":None,"scan_at":0.,"look_at":0.,"note":"","full_at":0.,"note_until":0.,"order":[]})
		a={"minimized":False,"shutting":False,"docked":False,"queue":[],"followers":0,"fmax":0,"me":0,"note_hue":Kit.HUE_INFO,"cmd_at":{},"seq":0};au();d={"g":None,"c":{},"store":({},{}),"rows":[],"n_rows":-1,"room":K,"w":W};S,o,bi=Kit.basics(a,i);b={};av={"range":(aj,ak),"low":(0,99),"heal":(0,len(A)-1)}
		def aw():Kit.kv_load(ae,";",e,av)
		def ax():Kit.kv_save(ae,";",e,("range","low","heal","kill","hidden"),av)
		def c(text,hue=None,secs=4.):a["note"],a["note_hue"]=text,Kit.HUE_INFO if hue is None else hue;a["note_until"]=time.time()+secs;F()
		def T(now):return bool(a["note"])and 0<=a["note_until"]-now<=10.
		def ay():return A[e["heal"]]
		def V(n):return Kit.count(n,"tile")
		def az(serial,name,manual=False):a["seq"]+=1;r={"serial":serial,"name":name,"seq":a["seq"],"seen":0.,"where":"gone","pct":None,"stam":None,"dist":0,"dir":"","dead":False,"poison":False,"low":False,"manual":manual,"alive":False,"noto":None};b[serial]=r;a["order"]=[];return r
		def t(serial):
			if b.pop(serial,None)is not None:a["order"]=[]
		def E(r,m,px,py,now,near):
			if r["manual"]and r.get("own"):r["own"]=bool(m.IsRenamable)
			d=str(m.Name or "");r["noto"]=Kit.noto_name(m)if Kit.cblind else None
			if d:r["name"]=d
			k,f,l,g=int(m.Hits or 0),int(m.HitsMax or 0),int(m.Stamina or 0),int(m.StaminaMax or 0);r["pct"]=max(0,min(100,int(k*100//f)))if f>0 else None;r["stam"]=max(0,min(100,int(l*100//g)))if g>0 else None;c=bool(m.IsDead);r["poison"]=bool(m.IsPoisoned);h,i=int(m.X),int(m.Y);r["dist"]=max(abs(h-px),abs(i-py));r["dir"]=Kit.compass(h-px,i-py)or "here";r["where"]="near"if near else "far";r["seen"]=now
			if c and not r["dead"]and r["alive"]:aA(ar,"%s died"%(j(r["name"],r["serial"])if r["name"]else "A pet"),r["serial"],r["name"])
			r["dead"]=c
			if c:r["low"]=True;return
			r["alive"]=True;a=e["low"];b=r["pct"]
			if b is not None:
				if a>0 and b<=a and not r["low"]:r["low"]=True;aA(aq,"%s at %d%% HP (%s)"%(j(r["name"],r["serial"])if r["name"]else "A pet",b,"here"if r["dist"]==0 else "%s %s"%(V(r["dist"]),r["dir"])),r["serial"],r["name"])
				elif r["low"]and(a<=0 or b>=a+10):r["low"]=False
		def aA(key,text,serial,name=""):M(key,text,"warn",who=serial,name=name)
		def aT(p,now):
			i=int(p.Serial);g,h=int(p.X),int(p.Y);a["me"]=i;w=a["followers"];a["followers"],a["fmax"]=int(p.Followers or 0),int(p.FollowersMax or 0);f=set();j=False;l=e["range"];d=now>=a["full_at"]or a["full_at"]-now>ah or a["followers"]!=w
			if not d:
				n=[x for x,y in b.items()if y["where"]=="near"]
				if len(n)<a["followers"]:d=True
			if not d:
				o=[]
				for k in n:
					try:
						m=U(k)
						if m is None or int(m.Distance)>l:d=True;break
					except Exception:d=True;break
					o.append((k,m))
				if not d:
					for k,m in o:
						try:
							r=b.get(k)
							if r is None:continue
							if not r["manual"]and not m.IsRenamable:t(k);continue
							f.add(k);E(r,m,g,h,now,True)
						except Exception:continue
					u=()
			if d:
				a["full_at"]=now+ah;u=HOST.mobiles(l)or[]
				if len(s)>400:s.clear()
			for m in u:
				try:
					if m is None:continue
					c=int(m.Serial)
					if c==i:continue
					r=b.get(c)
					if r is None:
						v=s.get(c)
						if v is not None and now<v:continue
						if not m.IsRenamable:s[c]=now+2.5;continue
						s.pop(c,None)
						if len(b)>=q:
							X(now,room=1)
							if len(b)>=q:continue
						r=az(c,"")
					elif not r["manual"]and not m.IsRenamable:t(c);continue
					f.add(c);E(r,m,g,h,now,True)
				except Exception:continue
			for c,r in b.items():
				if c not in f and r["where"]=="near":j=True;r["where"]="far"
			if j or now>=a["look_at"]or a["look_at"]-now>ai:
				a["look_at"]=now+ai
				for c in[G for G in b if G not in f]:
					r=b[c];m=U(c)
					if m is None:r["where"]="gone";continue
					try:
						if not r["manual"]and not m.IsRenamable:t(c);continue
						E(r,m,g,h,now,False)
					except Exception:continue
			X(now)
		def X(now,room=0):
			c=[g for g in b.values()if g["where"]=="gone"]
			if not c:return
			for e in c:
				if now-e["seen"]>1800.:t(e["serial"])
			d=q-room
			if a["fmax"]>0:f=len(b)-len([m for m in b.values()if m["where"]=="gone"]);d=min(d,max(a["followers"],f))
			if len(b)>d:
				c=sorted([n for n in b.values()if n["where"]=="gone"],key=lambda r:r["seen"])
				while c and len(b)>d:t(c.pop(0)["serial"])
		def aU():
			if not a["order"]or len(a["order"])!=len(b):a["order"]=sorted(b.values(),key=lambda r:r["seq"])
			return a["order"]
		def Y(g,store,items,a,e,f):
			x,y,b=a,e,1
			for h,i,c,j,k,l in items:
				d=35+Kit.text_w(c)
				if x>a and x+d>f:x,y,b=a,y+26,b+1
				if g is not None:Kit.art_button(g,store,h,i,x,y,c,j,hue=l,on_click=k)
				x+=d+12
			return b
		def aB():
			a=[("all_"+f,Kit.ART_CLOSE if f=="stay"else Kit.ART_PLAY,g,"Say \"%s\" (all your pets in earshot)"%m,o(("all",f)),None)for f,g,m in ao]
			if e["kill"]:a.append(("all_kill",Kit.ART_PLAY,"Kill","Say \"%s\", %s"%(R,at),o(("all","kill")),Kit.HUE_BAD))
			return a
		def aV(w):M=Kit.MARGIN;return 30+Y(None,None,aB(),M+10,0,w-M-10)*26+22
		def aC():return W,2*Kit.MARGIN+30+2*Kit.GAP+aV(W)+30+u+2
		def ab():
			M=Kit.MARGIN;i=k.zone_slot(*aC());w=i[0]if i else W;d=w-2*M;y=aB();A=Y(None,None,y,M+10,0,M+d-10);p=30+A*26+22;q=2*M+30+2*Kit.GAP+p;B=k.rows(u,q+32,K)if i else K;m=min(B,len(b));C=i[1]-q if i else 30+max(1,m)*u+2;g,r,f=k.begin(w,q+C);D=[]
			if not a["minimized"]:
				k.frame(g);n=M+30+Kit.GAP;Kit.add_section(g,M,n,d,p,"ALL PETS  (said out loud)");Y(g,r,y,M+10,n+26,M+d-10);f["note"]=Kit.add_label(g,"",M+12,n+30+A*26-2,Kit.HUE_INFO);h=n+p+Kit.GAP;E="YOUR PETS  (click to target)";Kit.add_section(g,M,h,d,C,E);f["title_end"]=M+8+Kit.text_w(E);s=M+d-10-35-Kit.text_w("Add...");Kit.art_button(g,r,"add",Kit.ART_PLAY,s,h+3,"Add...","List a pet of yours that isn't shown (this session)",on_click=o("add"));f["count"]=Kit.add_label(g,"",s-60,h+6,Kit.HUE_INFO);f["count_right"]=s-10;f["count_y"]=h+6;F=M+12+al+8;P=F+am+10;H=ay();t=[(bj,bl,bk,"Say \"%s\""%(z[bj]%"<name>"))for(bj,bk,bm),bl in zip(ap,(Kit.ART_PLAY,Kit.ART_PLAY,Kit.ART_CLOSE))];t.append(("heal",Kit.ART_PLAY,"Heal","Use one bandage on this pet (within %s)"%V(L)if not H[0]else "Cast %s on this pet (within %d tiles)"%(H[0],N)))
				if e["kill"]:t.append(("pet_kill",Kit.ART_PLAY,"Kill","Say \"<name> kill\", "+at))
				for I in range(m):
					j=h+30+I*u;c={"val":None,"prev":None,"changed":0.,"vis_hits":False,"vis_poison":False,"stam_on":False};c["name_lbl"]=Kit.add_label(g,"",M+12,j+3,Kit.HUE_TEXT);v={}
					for Q,R,S,T in(("hits",aQ,9,6),("poison",aR,9,6),("stam",aS,3,16)):l=G.CreateGumpSimpleProgressBar(am,S,aP,R,0,100);l.SetPos(F,j+T);l.SetAcceptMouseInput(False);g.Add(l);l.IsVisible=False;v[Q]=l
					c["bars"],c["stam_bar"]=v,v.pop("stam");c["info"]=Kit.add_label(g,"",P,j+3,Kit.HUE_INFO);Kit.catcher(g,M+10,j,d-20,22,Kit.row_clicker(c,o,"target"),"Click: aim your cursor at this pet, or make it your last target. Alt+click: auto-follow (again to stop)");J=M+10
					for x,U,O,X in t:Kit.art_button(g,r,"%s%d"%(x,I),U,J,j+24,O,X+". Alt+click: auto-follow (again to stop)",hue=Kit.HUE_BAD if x=="pet_kill"else None,on_click=Kit.row_clicker(c,o,x));J+=35+Kit.text_w(O)+12
					D.append(c)
				f["empty"]=(Kit.add_label(g,"",M+12,h+33,Kit.HUE_INFO)if not m else None)
			k.end(g,{"rows":D,"n_rows":m,"count_w":None,"room":B,"w":w});aF(time.time())
		k=Kit.Window(h,i,a,d,ab,aJ,aK,mini=(af,aL),icon=3713,cleanup=S,lock=True,clear={"rows":[],"c":{},"n_rows":-1})
		def aD(row,key,ctrl,on):
			if row.get(key)!=on:row[key]=on;ctrl.IsVisible=on
		def aE(row,key,ctrl,v):
			if row.get(key)!=v:row[key]=v;ctrl.SetProgress(float(v),100.)
		def aW():
			if T(time.time()):return a["note"],a["note_hue"]
			d=[g for g in b.values()if g["low"]and not g["dead"]and g["where"]!="gone"and g["pct"]is not None]
			if d:c=min(d,key=lambda r:r["pct"]);e=j(c["name"],c["serial"])if c["name"]else "pet";return "%s: %s %d%% HP"%(i,Kit.fit(e,80),c["pct"]),Kit.HUE_BAD
			f=len([m for m in b.values()if m["where"]!="gone"])
			if not b:return "%s: none in view"%i,Kit.HUE_INFO
			return "%s: %s, %d in view"%(i,Kit.count(len(b),"pet"),f),Kit.HUE_INFO
		def F():
			c=d["c"]
			if d["g"]is None or a["docked"]:return
			if a["minimized"]:
				b=c.get("status")
				if b is not None:t,e=aW();Kit.set_text(b,Kit.fit(t,af-90),e)
				return
			b=c.get("note")
			if b is not None:f=T(time.time());Kit.set_text(b,Kit.fit(a["note"],d["w"]-2*Kit.MARGIN-24)if f else "",a["note_hue"])
		def aF(now):
			if d["g"]is None or a["shutting"]or a["docked"]:return
			if a["minimized"]:F();return
			h=aU()
			if min(d["room"],len(h))!=d["n_rows"]:ab();return
			f=d["c"]
			for c,r in zip(d["rows"],h):
				Kit.row_set(c,(r["serial"],),now);i,k=r["where"],r["pct"]
				if r["dead"]or i=="gone":l=Kit.HUE_INFO
				elif r["low"]:l=Kit.HUE_BAD
				elif r["poison"]:l=Kit.HUE_GOOD
				else:l=Kit.HUE_TEXT
				s=Kit.hp_mark(r["poison"]);u=j(r["name"],r["serial"],r["noto"])if r["name"]else "(no name yet)";Kit.set_text(c["name_lbl"],Kit.fit(u+("  "+s if s else ""),al),l);e=None
				if i=="near"and not r["dead"]:e="poison"if r["poison"]else "hits";m="%s, %s"%("%d%%"%k if k is not None else "?%","here"if r["dist"]==0 else "%d %s"%(r["dist"],r["dir"]))
				elif r["dead"]and i!="gone":m="dead, %d %s"%(r["dist"],r["dir"])
				elif i=="far":m="far: %d %s"%(r["dist"],r["dir"])
				else:m=("out of range (%s)"%Kit.ago(now-r["seen"],Kit.AGO_SHORT)if r["seen"]else "out of range")
				Kit.set_text(c["info"],m,Kit.HUE_TEXT if e else Kit.HUE_INFO)
				for v,w in c["bars"].items():aD(c,"vis_"+v,w,v==e)
				if e:aE(c,"p_"+e,c["bars"][e],k if k is not None else 0)
				n=r["stam"]if e else None;aD(c,"stam_on",c["stam_bar"],n is not None)
				if n is not None:aE(c,"p_stam",c["stam_bar"],n)
			o=f.get("count")
			if o is not None:
				if a["fmax"]>0:g="%d / %d slots"%(a["followers"],a["fmax"])
				else:g="%d known"%len(b)if b else ""
				if len(h)>d["room"]:
					t=("%d more, %s"%(len(h)-d["room"],g)).rstrip(", ")
					if f["count_right"]-Kit.text_px(t)>=f["title_end"]+8:g=t
				Kit.set_text(o,g);p=Kit.text_px(g)if g else 0
				if d["count_w"]!=p:d["count_w"]=p;Kit.ui_pos(o,f["count_right"]-p,f["count_y"])
			q=f.get("empty")
			if q is not None:
				if a["followers"]>0:Kit.set_text(q,"%s used, none in view. Add... lists one."%Kit.count(a["followers"],"slot"))
				else:Kit.set_text(q,"No pets in view. Click Add... to list one.")
			F()
		def aG(action,p,now):
			if not e["hidden"]:return True
			if not p.IsHidden:a["confirm"]=None;return True
			b=a["confirm"]
			if b is not None and b[0]==action and b[1]<=now<=b[2]:a["confirm"]=None;return True
			a["confirm"]=(action,now+.3,now+an);c("That reveals you: click again to do it.",Kit.HUE_TITLE,an);return False
		def aX(text,now,shown):
			b=a["cmd_at"].get(text)
			if b is not None and 0<=now-b<.6:return
			if len(a["cmd_at"])>50:a["cmd_at"].clear()
			a["cmd_at"][text]=now;API.Msg(text);c("Said \"%s\"."%shown)
		def aY(serial):
			r=b.get(serial)
			if r is None or not r["name"]:c("That pet has no name yet.",Kit.HUE_BAD);return
			return r["name"]
		def aZ(serial):
			if API.HasTarget("any")and not C(h):
				if not ad(serial,"hud.pets",i):return
				API.Target(serial)
				if a["heal"]is not None:a["heal"]=None;l(h)
				return
			API.SetLastTarget(serial=serial);API.HeadMsg("* last target *",serial,53)
		def aH(m,p):return max(abs(int(m.X)-int(p.X)),abs(int(m.Y)-int(p.Y)))
		def a_(serial,p,now):
			r=b.get(serial);e=(r and r["name"]and j(r["name"],serial))or "that pet"
			if a["heal"]is not None:c("A heal is already on its way.",Kit.HUE_TITLE);return
			if p.IsDead:c("You are dead.",Kit.HUE_BAD);return
			if API.HasTarget("any")or C(h):c("A target cursor is up: aim it or press Esc first.",Kit.HUE_TITLE);return
			d,n=ay();f=N if d else L;m=API.FindMobile(serial)
			if m is None:c("%s is out of range."%e,Kit.HUE_BAD);return
			k=aH(m,p)
			if k>f:c("%s is %d tiles away (%s reaches %d)."%(e,k,n.lower(),f),Kit.HUE_BAD);return
			if not aG(("heal",serial),p,now):return
			if d:API.CastSpell(d);g=Kit.spell_info(d)[3]+P
			else:
				l=API.FindType(3617,API.Backpack)
				if not l:c("Out of bandages.",Kit.HUE_BAD);API.SysMsg("%s: out of bandages!"%i,Kit.HUE_BAD);return
				API.UseObject(l.Serial);g=P
			Z(h,g);a["heal"]={"serial":serial,"name":e,"until":now+g,"reach":f,"what":d or "a bandage","t0":now,"rd":D()};c("%s for %s..."%(d or "Bandage",e))
		def a0(p,now):
			j=a["heal"];b=False;d=j["what"][0].upper()+j["what"][1:]
			for e in j["rd"].new():
				f=O(e,Q)
				for x in aN:
					if x in f:b=True;break
				if b:break
			if b:a["heal"]=None;l(h);c("%s for %s failed."%(d,j["name"]),Kit.HUE_BAD);return
			if HOST.cursor_claim[0]==h and aa(h,"beneficial"):
				m=API.FindMobile(j["serial"]);a["heal"]=None;l(h)
				if m is not None and aH(m,p)<=j["reach"]:API.Target(j["serial"]);c("%s on %s."%(d,j["name"]),Kit.HUE_GOOD)
				else:API.CancelTarget();c("%s moved out of reach."%j["name"],Kit.HUE_BAD)
				return
			if not 0<=j["until"]-now<=P+10.:
				a["heal"]=None;l(h)
				if API.HasTarget("any"):c("A target cursor is up: aim it or press Esc.",Kit.HUE_TITLE)
				else:c("No target cursor came for %s."%j["name"],Kit.HUE_BAD)
		def a1(serial):o.add(("added",int(serial or 0)),dup=True)
		def a2(serial,p,now):
			if not serial:return
			if serial==a["me"]or serial==int(p.Serial):c("That's you.",Kit.HUE_BAD);return
			m=API.FindMobile(serial)
			if m is None:c("That isn't a creature in view.",Kit.HUE_BAD);return
			r=b.get(serial)
			if r is None:
				if len(b)>=q:X(now,room=1)
				if len(b)>=q:c("The list is full (%d)."%q,Kit.HUE_BAD);return
				r=az(serial,"",manual=True)
			r["manual"]=True;r["own"]=bool(m.IsRenamable);E(r,m,int(p.X),int(p.Y),now,True)
			if r["dist"]>e["range"]:r["where"]="far"
			c("%s is listed for this session."%(j(r["name"],serial)if r["name"]else "It"),Kit.HUE_GOOD)
		def a3(action,p,now):J(10.,a1);c("Target the pet to list.")
		def aI(action,p,now):
			a=action[0]
			if(action[1]=="kill"if a=="all"else a=="pet_kill")and not e["kill"]:return
			if a=="all":c=d=R if action[1]=="kill"else aO.get(action[1])
			else:b=aY(action[1]);c=b and z[a]%b;d=b and z[a]%j(b,action[1])
			if c and not a4(p)and aG(action,p,now):aX(c,now,d)
		def a4(p):
			if p.IsDead:c("You are dead: your pets can't hear you.",Kit.HUE_BAD);return True
			return False
		a5=("add","follow");ac={"add":a3,"follow":lambda action,p,now:B(action[1],i),"added":lambda action,p,now:a2(action[1],p,now),"target":lambda action,p,now:aZ(action[1]),"heal":lambda action,p,now:a_(action[1],p,now),"all":aI};ac.update((bp,aI)for bp in z);a6=("One heal per click, aimed at the pet when its cursor comes (bandage within %s, spell within %d)."%(V(L),N));a7="Said only on a click; the shard's cursor then picks the enemy."
		def a8(w):a,b=([("note",g)for g in Kit.wrap(f,w-28)]for f in(a6,a7));return(("WINDOW",(("num","range","List pets within:","How far a pet is listed with its bars","tiles",aj,ak),("check","hidden","While hidden, a command or a heal needs a second click","Speaking and healing reveal you; the first click only asks"))),("HEAL BUTTON  (on each pet's row)",[("note","Heal with:",{"ndy":4,"h":28,"hue":Kit.HUE_TEXT})]+a),("COMBAT COMMANDS",[("check","kill","Show Kill buttons (\"%s\" and \"<name> kill\")"%R,"One for all pets and one per pet row",{"h":28})]+b),("ALERTS  (sound: Settings > Alerts)",(("num","low","Alert when a pet's HP falls to:","One alert per fall to this % or below (0-99, 0 = never)","%",0,99),)))
		def a9(f,new):
			i=Kit.dd_index(f.c["heal"],-1)
			if 0<=i<len(A):new["heal"]=i
		def ba(old,new):
			if new["hidden"]!=old["hidden"]:a["confirm"]=None
			if(new["kill"],new["heal"])!=(old["kill"],old["heal"])and d["g"]is not None:o("redraw")()
		I=Kit.Page(e,a8,ax,ba,{"ldy":4,"lgap":12,"fw":44,"pad":6},strict=True,adjust=a9)
		def bb(g,x,y,w):f=I.build(g,x,y,w);a=G.CreateDropDown(200,[m for n,m in A],e["heal"]);a.SetPos(x+22+Kit.text_w("Heal with:"),y+90+Kit.GAP+30);g.Add(a);f.c["heal"]=a;a.SetTooltip("What each row's Heal button uses")
		aw()
		def bc():
			au();a["minimized"]=k.start_min();aw()
			for r in b.values():r["where"]="gone"if r["where"]=="gone"else "far"
			H(aq,"Pet HP low",821);H(ar,"Pet died",497);ab();k.dock(fit=True,min=aC);S.service("pets.list",bd)
		def bd(distance=None):
			if a["shutting"]:return
			c=e["range"]
			if distance is None:distance=c
			if distance>c:return
			return[g for g,f in b.items()if f["where"]=="near"and(not f["manual"]or f.get("own"))and f["dist"]<=distance]
		def be():
			if d["g"]is None:return
			if Kit.closed(d):return
			b=time.time();p=API.Player
			while a["queue"]:
				c=a["queue"].pop(0);e=c[0]if isinstance(c,tuple)else c
				if not(k.action(c)or p is None and e not in a5)and e in ac:ac[e](c,p,b)
				if d["g"]is None:return
			if p is None:return
			if a["heal"]is not None:a0(p,b)
			if b>=a["scan_at"]or a["scan_at"]-b>ag:a["scan_at"]=b+ag;aT(p,b);aF(b)
			elif a["note"]and not T(b):a["note"]="";F()
		def bf():return.02 if a["heal"]is not None else.1
		def bg():a["shutting"]=True;a["heal"]=None;l(h);ax();S.close()
		return{"start":bc,"tick":be,"stop":bg,"client_tick":True,"config_height":I.height,"build_config":bb,"poll_config":I.poll,"config_closed":I.closed,"interval":bf}
	aw=(("frames",ap,.1,"unitframes"),("timers",aq,.1,"spelltimers"),("swing",ar,.025,"swing"),("bandage",au,.1,"bandage"),("pets",av,.1,"pets"),);return PartSet(al,am,aw).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("hud","Character HUD","Frames, timers and bars for you and pets",_module_hud,.025,category="On screen",parts=(("frames","Frames","Health frames: you, target, party",True,("unitframes",)),("timers","Buffs & Timers","Timed buffs, debuffs and your spells",True,("spelltimers",)),("swing","Swing Bar","When your next melee swing lands",False,("swing",)),("bandage","Bandages","One-press bandage, timer and alerts",False,("bandage",)),("pets","Pets","Pets' health, distance and commands",False,("pets",)),),aliases=('Unit Frames','Spell Timers','Swing Timer','Bandage Agent','Pets','cast bar','buffs','debuffs','party frames','hit chance'))
