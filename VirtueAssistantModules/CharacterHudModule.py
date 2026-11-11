def _module_hud():
	aM=Client._member;X=Client._type;ad=Follow.alt_held;Y=Follow.toggle;ao=HOST.alert;ae=HOST.alert_kind;aN=HOST.claim_cursor;Z=HOST.cursor_busy;aO=HOST.cursor_ok;aP=HOST.disable;aQ=HOST.dock_remove;aR=HOST.harm_ok;ap=HOST.me;aA=HOST.mobile;af=HOST.pick_target;ag=HOST.refresh_settings;H=HOST.release_cursor;aa=Journal.reader;aq=Journal.said;aS=Kit.ART_CIRCLE;W=Kit.ART_CLOSE;K=Kit.ART_PLAY;B=Kit.GAP;j=Kit.HUE_BAD;I=Kit.HUE_GOOD;k=Kit.HUE_INFO;C=Kit.HUE_TEXT;O=Kit.HUE_TITLE;F=Kit.MARGIN;aT=Kit.SECTION_TILE;aU=Kit._raw_gump;P=Kit.add_box;l=Kit.add_label;aB=Kit.add_pic;J=Kit.add_section;ar=Kit.add_tiled;ah=Kit.add_window_frame;Q=Kit.art_button;aV=Kit.attach;ai=Kit.basics;D=Kit.catcher;aC=Kit.closed;S=Kit.count;aW=Kit.detach;L=Kit.dispose;M=Kit.fit;aX=Kit.frame_show;T=Kit.get_var;aY=Kit.hook_once;aZ=Kit.hp_mark;aj=Kit.inert;q=Kit.is_open;aD=Kit.kv_load;aE=Kit.kv_save;aF=Kit.moved_by_code;aG=Kit.note_rect;aH=Kit.on_moved;N=Kit.pic_size;a_=Kit.pin_size;ak=Kit.place;U=Kit.put_var;a0=Kit.row_clicker;al=Kit.screen;aI=Kit.set;A=Kit.set_text;aJ=Kit.spell_info;ab=Kit.text_px;z=Kit.text_w;am=Kit.ui_pos;a1=Kit.ui_rect;au=Kit.ui_w;a2=Kit.was_clicked;a8="hud";a9="Character HUD";e={"anchor":{},"piece":{},"tied":{},"span":{},"inner":{},"bg":{},"bare":{},"stack":{},"dirty":True,"full_at":0.,"sig":None,"objs":None,"inside":[]};a3=.5;av=42;aw={500007:"you are no longer frozen",500119:"you must wait to perform another action",500231:"you feel cured of poison",500295:"you are too far away to do that",500641:"your concentration is disturbed",500916:"you apply the bandages, but they do not seem",500951:"you cannot heal that",500954:"that creature may only be healed",500955:"that being is not damaged",500956:"you begin applying the bandages",500957:"you begin applying the bandages",500958:"you begin applying the bandages",500959:"you begin applying the bandages",500960:"you begin applying the bandages",500962:"you were unable to finish your work",500963:"you did not stay close enough to heal",500964:"you did not stay close enough to heal",500965:"you are able to resurrect",500966:"you are unable to resurrect",500967:"you heal what little damage",500968:"you apply the bandages, but they barely help",500969:"you finish applying the bandages",500970:"bandages cannot be used on that",501604:"incognito cannot be cast",501775:"this spell is already in effect",501816:"you are too far away to do that",501857:"this spell won't work on that",502136:"the poison seems to have worn off",502349:"this target already has reactive armor",502381:"you cannot move!",502382:"you can move!",502625:"insufficient mana",502630:"more reagents are needed",502632:"the spell fizzles",503252:"you were unable to finish your work",503253:"you did not stay close enough to heal",503254:"you did not stay close enough to heal",503255:"you are able to resurrect",503258:"you heal what little damage",503259:"you apply the bandages, but they barely help",503260:"you finish applying the bandages",503261:"bandages cannot be used on that",1005382:"the spell will not adhere to you",1005383:"the spell will not adhere to you",1005384:"you currently have a reactive armor spell",1005385:"the spell will not adhere to you",1005416:"you currently have a reflect spell",1005417:"this spell is already in effect",1005545:"the spell will not adhere to you",1005546:"you currently have a reflect spell",1005547:"the spell will not adhere to you",1005548:"you currently have a reactive armor spell",1005549:"the spell will not adhere to you",1005550:"your protection spell has been nullified",1005552:"the spell will not adhere to you",1005553:"you currently have a reflect spell",1005554:"the spell will not adhere to you",1005555:"the spell will not adhere to you",1005556:"your reactive armor spell has been nullified",1005557:"you currently have a reflect spell",1005559:"this spell is already in effect",1005603:"you can move again!",1008072:"you have been cured of all poisons",1010058:"you have cured the target of all poisons",1010059:"you have been cured of all poisons",1010398:"you cannot heal that",1010406:"you cannot heal that",1010445:"you cannot incognito",1010648:"you have cured the target of all poisons",1010649:"you have been cured of all poisons",1042857:"you feel a bit nauseous",1042858:"looks ill",1042859:"you feel disoriented and nauseous",1042860:"looks extremely ill",1042861:"you begin to feel pain throughout your body",1042862:"stumbles around in confusion and pain",1042863:"you feel extremely weak and are in severe pain",1042864:"is wracked with extreme pain",1042865:"you are in extreme pain, and require immediate aid",1042866:"begins to spasm uncontrollably",1042867:"looks extremely ill",1042868:"stumbles around in confusion and pain",1042869:"is wracked with extreme pain",1042870:"begins to spasm uncontrollably",1045157:"you must wait to perform another action",1061091:"you cannot cast that spell in this form",1061654:"you cannot heal that",3000201:"you must wait to perform another action"}
	def ax(a,below):
		s=e["stack"].get(a)
		if s is None or s[0]!=below:return 0
		return max(0,int(s[1]))
	def a4(a,getter,span=None,inner=None):
		e["dirty"]=True
		if getter is None:
			e["anchor"].pop(a,None);e["span"].pop(a,None);e["inner"].pop(a,None)
			for b,(c,d,f)in list(e["piece"].items()):
				if c==a:ay(b)
		else:e["anchor"][a]=getter;e["span"][a],e["inner"][a]=span,inner
	def aK(a,b,order,getter):e["piece"][a]=(b,int(order),getter);e["dirty"]=True
	def aL(a):e["piece"].pop(a,None);e["dirty"]=True;ay(a)
	def ay(a):
		b=e["tied"].pop(a,None);g=None
		if b is not None:aW(b[0]);g=b[0]
		elif a in e["piece"]:g=e["piece"][a][2]()
		c=e["bare"]
		if g is None or not c or not c.pop(g,False)or not q(g):return
		aX(g,True)
		for d in e["bg"].get(g)or():aI(d,"IsVisible",True)
	def V(b):a=e["anchor"].get(b);g=a()if a is not None else None;return g if q(g)and g.IsVisible else None
	def a5(a):p=e["piece"].get(a);return p is not None and V(p[0])is not None
	R={"at":0.,"uim":None,"off":False,"same":None}
	def a6(j):
		if R["off"]:return
		e=time.time()
		if e<R["at"]:return
		R["at"]=e+.25
		try:
			if R["uim"]is None:import System;R["same"]=System.Object.ReferenceEquals;R["uim"]=Tz.T("ClassicUO.Game.Managers.UIManager")
			f,g=R["uim"],R["same"];k=Tz.get(None,"Gumps",f);c=Kit.mouse_pos()
			for l,h in j:
				if c is not None:
					a=ac(h)
					if a is not None and a[0]<=c[0]<a[0]+a[2]and a[1]<=c[1]<a[1]+a[3]:continue
				d,i=aU(l),aU(h)
				if d is None or i is None:continue
				b=k.First
				while b is not None:
					v=b.Value
					if g(v,d):break
					if g(v,i):Tz.call(None,"MakeTopMostGump",[d],f);break
					b=b.Next
		except Exception:R["off"]=True
	def ac(g):r=Kit.rect(g);return r if r is not None and r[2]>0 and r[3]>0 else None
	def ba(sw,sh):
		b=[sw,sh];c=[]
		for j,(a,k,l)in e["piece"].items():b.append((j,a,k));c.append(l())
		for a in e["anchor"]:
			d=V(a);r=f=g=None
			if d is not None:r=ac(d);h,i=e["span"].get(a),e["inner"].get(a);f=h()if h is not None else None;g=i()if i is not None else None
			b.append((a,r,f,g));c.append(d)
		return b,c
	def bb():
		w,z=al();A=time.time();K,p=ba(w,z)
		if not e["dirty"]and A<e["full_at"]and A+2*a3>e["full_at"]and K==e["sig"]:
			C=e["objs"];D=C is not None and len(C)==len(p)
			if D:
				for L in range(len(p)):
					if p[L]is not C[L]:D=False;break
			if D:
				if e["inside"]:a6(e["inside"])
				return
		e["sig"],e["objs"]=K,p;e["dirty"]=False;e["full_at"]=A+a3;M={};k=[];E={}
		for a,(b,N,l)in e["piece"].items():E.setdefault(b,[]).append((N,a,l))
		for b in[at for at in e["stack"]if at not in E]:e["stack"].pop(b,None)
		for b,G in E.items():
			f=V(b)
			if f is None:
				for X,a,_g in G:ay(a)
				e["stack"].pop(b,None);continue
			O=ac(f)
			if O is None:e["dirty"]=True;continue
			m,h,r,H=O;s=z<=0 or(h+H/2.)<z/2.;P,Q=e["span"].get(b),e["inner"].get(b);c=P()if P is not None else None;t=Q()if Q is not None and c is not None else None;R=None;G.sort();y=h+H if s else h
			for X,a,l in G:
				g=l()
				if not q(g):ay(a);continue
				M[a]=g
				if not g.IsVisible:continue
				S=ac(g)
				if S is None:e["dirty"]=True;continue
				Y,Z,d,T=S;u=None
				if t is not None and R is None and d<r:
					i=F;I,iw,ih,aa,ah=t[:5];v=(c[0]-i)if c[2]else(c[1]-d+i);U=(t[5]if len(t)>5 else aa+ah)+B-i;v=max(I-i,min(v,iw-I-d+i))
					if U+i+av<=ih-I+2 and v>=0:u,R=(m+v,h+U),1
				if u is not None:x,n=u;k.append((g,f))
				elif c is not None and d<r:x=m+(c[1]-d if c[2]else c[0]);x=max(m,min(x,m+r-d))
				else:x=m+(r-d)//2
				if u is None:
					if w>0:x=max(0,min(x,w-d))
					if s:n,y=y,y+T
					else:y-=T;n=y
				if(Y,Z)!=(x,n):g.SetPos(x,n);aG(g,x,n);aF(g)
				j=e["tied"].get(a)
				if j is None or j[0]is not g or j[1]is not f:
					if j is not None and j[0]is not g:aW(j[0])
					aV(g,f);e["tied"][a]=(g,f)
			e["stack"][b]=(s,(y-(h+H))if s else(h-y))
		J=e["bare"];ab=set(bj for bj,bk in k)
		for W in(J,e["bg"]):
			for g in[bl for bl in W if not q(bl)]:W.pop(g,None)
		for a,(b,N,l)in e["piece"].items():
			g=M.get(a)
			if g is None:g=l()
			if not q(g):continue
			o=g in ab
			if J.get(g,False)!=o:
				J[g]=o
				if o:a_(g)
				aX(g,not o)
				for ad in e["bg"].get(g)or():aI(ad,"IsVisible",not o)
		e["inside"]=k
		if k:a6(k)
	az={"fn":None};bc=("Ready","Done","Out!","Dead","Paused")
	def a7():return max(z(a)for a in bc)
	def E(name,serial,noto=None,me=False):a=Kit.noto_mark(noto)if noto else "";return(a+" "if a else "")+(Kit.veil("me",name)if me else Kit.veil("name",name,serial))
	def an(name,default=0.):
		try:return float(API.GetSkill(name).Value or 0)
		except Exception:return default
	def bd():
		ae="unitframes";aQ="Frames";b1="UnitFrames_settings";c0="UnitFrames_pos";c1="UnitFrames_min";b2=("hits","mana","stam");b3="#17171a";c2={"hits":"#c22d2d","poison":"#2f9a3c","yellow":"#cfae2a","mana":"#2f62cc","stam":"#d39a1c"};b4={"innocent":(46,104,214),"ally":(40,160,70),"gray":(120,120,126),"criminal":(120,120,126),"enemy":(222,118,30),"murderer":(196,38,38),"invulnerable":(214,178,40)};aL=(226,226,230);c3={1:"innocent",2:"ally",3:"gray",4:"criminal",5:"enemy",6:"murderer",7:"invulnerable"};bn=(0,0,8);b5,b6=50000,60000;c4={400:12,402:12,401:13,403:13,605:14,607:14,606:15,608:15,666:666,694:666,667:665,695:665,1253:51253,987:12};c5=(401,403,606,608,667,695);c6,c7=987,1002;b7=("cloak","shirt","arms","torso","tunic","face","robe","neck","hair","beard","earrings","helmet");c8=("shirt","arms","torso","tunic","face","robe","cloak","neck","hair","beard","earrings","helmet");c9=("shirt","arms","torso","tunic","cloak","face","neck","hair","beard","earrings","helmet","robe");da=(41674,41675);bC=(39301,39302,42002,41675,41674);db=(5136,5143);b8=110;bo=2.;bD=.008;aT="vauf_";bp=12;aB,aK,b9=50,150,70;aU=14;ca=10;ao=100;cb="UnitFrames_tracked";cc="UnitFrames_framepos";cd=350;ce=(4017,4018,4017);cf=3;dc,dd=240,46;bE=.4;cg=.05;aW=SNAP_DIST;aX=24;aY=2;ch=1.5;de=10.;df=.025;dg={"cast":"#cfae2a","done":"#2f9a3c","fail":"#c22d2d"};dh=(("the spell fizzles","fizzled"),("your concentration is disturbed","disturbed"),("insufficient mana","no mana"),("more reagents are needed","no reagents"));di=Kit.SPELL_WORDS;bq=ab;bi,a9=502,194;bj=(96.5,96.5);bF=52.5;ci=((86.,(22,22,24)),(81.5,(226,226,230)),(79.5,"tire"),(64.5,(30,25,10)),(61.5,(226,226,230)),(60.5,"gold"),(53.5,(14,10,2)));br=(78.,83.5);ac=(150.,39.5,491.5,154.5,9.);dj=(153.,42.6,488.,151.,6.5);dk=(178.5,47.5,476.5,146.,8.);dl=(183.5,51.5,472.5,141.5,6.);dm=((77.5,83.5),(109.5,115.5));dn=((483.5,45.8,(188,188,193)),(483.5,148.6,(128,128,133)));do,dp=(20,20,22),(16,16,18);cj=(182,474);dq=((51,79),(83,111),(115,143));ck=.70710678;o={"player":True,"target":True,"hide_empty":False,"numbers":True,"lock":False,"click":True,"party":False,"ignore_self":True,"attack":False,"status":True,"scale":b9,"pdx":0,"pdy":0,"pscale_on":False,"pscale":b9,"pzoom":100,"mirror":False,"sup_open":False,"sup_deep":True,"sup_hide0":False,"sup_follow":True,"sup_low":10,"sup_side":0,"cast":True,"guard":True,"hide_bar":True};cl=dict(o);bs={"scale":(aB,aK),"pscale":(aB,aK),"pdx":(-60,60),"pdy":(-60,60),"pzoom":(50,200),"sup_low":(0,9999),"sup_side":(0,2)}
		def cm():i.update({"shutting":False,"queue":[],"rebuild":False,"docked":False,"target":0,"next_party":0.,"snaps":{},"stale":set(),"snap_queue":[],"art_scales":set(),"snap_px":None,"party":set(),"snap_job":None,"art_jobs":[],"art_failed":set(),"recent":[],"next_prune":0.,"art_dirty":True,"snap_tries":{},"guard":None,"next_guard":0.,"jr":None,"dismissed":set(),"removing":False,"full_at":0.,"mirror_now":False,"pos_save_at":0.})
		i={"minimized":False,"shutting":False,"docked":False,"queue":[],"me":0,"names":{},"pos":{},"next_save":0.,"pos_dirty":False,"crop_changed":0.,"art":None,"textures":set(),"running":False};cm();H=[];ba={"sig":None,"at":None};m={"g":None,"c":{},"spell":None,"start":0.,"secs":1.,"state":None,"until":0.,"pct":0,"word":"","shown":None,"at":None,"leader":None,"s":None,"w":0};t={};bt={"g":None,"c":{},"store":({},{})};a0,ar,V=ai(i,aQ);R={"store":({},{}),"next_preview":0.,"layers":None};cn={};bG,bu=T,U
		def co():aD(b1,",",o,bs)
		def bH():aE(b1,",",o,sorted(cl),bs)
		def dr():
			del H[:]
			for a in bG(cb).split(";"):
				p=a.split(",",2)
				if len(p)<3:continue
				try:H.append({"serial":int(p[0]),"auto":p[1]=="1","name":p[2]})
				except ValueError:pass
		def bc():bu(cb,";".join("%d,%s,%s"%(a["serial"],"1"if a["auto"]else "0",a["name"].replace(";"," ").replace(","," "))for a in H))
		def ds():
			i["pos"]={}
			for a in bG(cc).split(";"):
				try:k,b=a.split(":");x,y=b.split(",");i["pos"][k]=Kit.adapt(int(x),int(y))
				except ValueError:pass
		def bv():
			bI();b=set("m%d"%c["serial"]for c in H);b.update(("player","target"));a=i["pos"]
			for k in[d for d in a if d not in b]:del a[k]
			bu(cc,";".join("%s:%d,%d"%(g,f[0],f[1])for g,f in sorted(a.items())));i["pos_dirty"]=False
		def bw(key,p,at=0):
			if i["pos"].get(key)!=p:
				i["pos"][key]=p;i["pos_dirty"]=True
				if at:i["pos_save_at"]=at
		def bI():
			for a,b in t.items():
				if q(b.get("g")):
					p=a7(b)
					if p is not None and not aP(a):bw(a,p)
		def bJ():return int(safe(lambda:API.Player.Serial,0)or 0)
		def dt(n):
			if n is None:return ""
			try:return c3.get(int(n),"")
			except Exception:return str(n).split(".")[-1].lower()
		def cp(serial):return ap()if serial==i["me"]else aA(serial)
		bx,du,dv,dw,dz,dA,dB,bK,cq,cr,cs,ct=range(12);bk={}
		def cu(serial):
			if not serial:return
			m=cp(serial)
			if m is None:return
			try:
				a=bool(m.IsDead);d=time.time();c=bk.get(serial)
				if c is None or d>=c[5]or a!=c[6]:
					if c is None and len(bk)>=64:bk.clear()
					c=bk[serial]=(str(m.Name or ""),int(m.HitsMax or 0),int(m.ManaMax or 0),int(m.StaminaMax or 0),dt(m.Notoriety),d+.5,a)
				e=(c[0],int(m.Hits or 0),c[1],int(m.Mana or 0)if c[2]else 0,c[2],int(m.Stamina or 0)if c[3]else 0,c[3],c[4],a,bool(m.IsPoisoned),bool(m.IsYellowHits),bool(m.IsParalyzed))
			except Exception:bk.pop(serial,None);return
			b=e[bx]
			if b and i["names"].get(serial)!=b:i["names"][serial]=b
			return e
		an={"get":None,"looked":False,"root":None,"obj":None,"until":0.};cv=2.
		def dC():
			t=X("ClassicUO.Game.World");a=aM(t,"Instance")if t is not None else None
			if a is None:return
			def b():
				c=a[0]()
				if c is None:an["obj"]=None;return 0
				b=an["obj"];d=time.time()
				if b is None or c is not an["root"]or not 0<an["until"]-d<=cv:
					an["obj"]=None;b=Typing._get(c,"TargetManager")
					if b is None:return 0
					an.update({"root":c,"obj":b,"until":d+cv})
				v=Typing._get(b,"LastAttack")
				if v is None:an["obj"]=None
				return int(v or 0)
			b();return b
		def dD():
			if not an["looked"]:an["looked"]=True;an["get"]=safe(dC)
			return int(safe(an["get"],0)or 0)if an["get"]is not None else 0
		def dE():
			s=(dD()if o["attack"]else 0)or int(API.LastTargetSerial or 0)
			if not s:i["target"]=0;return
			if s==i["target"]:return
			if s==i["me"]:
				if not o["ignore_self"]:i["target"]=s
			elif API.FindMobile(s)is not None:i["target"]=s
		def dF():
			a=set(int(d)for d in(API.GetPartyMemberSerials()or[])if int(d)and int(d)!=i["me"]);i["party"]=a;c=False;b=i["dismissed"]
			if b:
				if o["party"]:b&=a
				else:b.clear()
			if o["party"]:
				for s in a:
					if s in b:continue
					if not any(f["serial"]==s for f in H)and len(H)<bp:H.append({"serial":s,"auto":True,"name":i["names"].get(s)or "Party member"});c=True
			for t in list(H):
				if t["auto"]and(t["serial"]not in a or not o["party"]):H.remove(t);c=True
			if c:bc();bg();ag(ae)
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
				import clr;import System;from System.Reflection.Emit import DynamicMethod,OpCodes;p=Bridge.parts;p["uo"]=Tz.get(Tz.get(None,"Game",X("ClassicUO.Client")),"UO");p["anims"]=Typing._get(p["uo"],"Animations");p["hues"]=Typing._get(Typing._get(p["uo"],"FileManager"),"Hues");p["hue_color"]=p["hues"].GetType().GetMethod("GetHueColorRgba8888");d=X("ClassicUO.Game.World");p["world"]=d.GetProperty("Instance").GetValue(None,None);p["get_entity"]=d.GetMethod("Get",System.Array[System.Type]([clr.GetClrType(System.UInt32)]));n=X("ClassicUO.Game.GameObjects.Mobile");p["group_for"]=n.GetMethod("GetGroupForAnimation");p["get_data"]=[s for s in p["tex_t"].GetMethods()if s.Name=="GetData"and s.IsGenericMethodDefinition and len(s.GetParameters())==5][0].MakeGenericMethod(clr.GetClrType(System.UInt32));e=p["anims"].GetType();f=e.GetMethod("GetAnimationFrames");g=X("ClassicUO.Renderer.SpriteInfo");b=f.ReturnType;h,i,j,o=(clr.GetClrType(System.Object),clr.GetClrType(System.UInt16),clr.GetClrType(System.Byte),clr.GetClrType(System.Int32));k=DynamicMethod("vauf_frame",h,System.Array[System.Type]([e,i,j,j,o,clr.GetClrType(System.Array[System.UInt16])]),h.Module,True);a=k.GetILGenerator();c=a.DeclareLocal(b);l=a.DeclareLocal(i);q=a.DeclareLocal(clr.GetClrType(System.Boolean));m=a.DefineLabel()
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
		def au(d,s):v=.5-d*s;return 0. if v<=0 else(1. if v>=1 else v)
		def by(u,v,box):c,d,e,f,r=box;a=abs(u-(c+e)*.5)-((e-c)*.5-r);b=abs(v-(d+f)*.5)-((f-d)*.5-r);g=a if a>0 else 0.;h=b if b>0 else 0.;i=a if a>b else b;return math.sqrt(g*g+h*h)+(i if i<0 else 0.)-r
		def dG(a,b,x):t=(x-a)/(b-a);t=0. if t<0 else(1. if t>1 else t);return t*t*(3-2*t)
		def cw(v):c=132.-62.*min(1.,max(0.,(v-43.)/107.));return(c,c,c+6.)
		def dH(dx,dy,r):b=(dx+dy)/r*ck;f=min(1.,max(0.,(b+.71)/1.42));t=min(1.,max(0.,(r-67.)/11.5));a=44.*(t**1.2)*f;return(128.-a,128.-a,134.-a)
		def dI(dx,dy,r):b=-(dx+dy)/r*ck;t=min(1.,max(0.,(r-56.)/4.));a=t*(-42.+57.*dG(-.3,.75,b));return(min(255.,234.+a),min(255.,203.+a),min(255.,91.+a*.65))
		def a3(b,c,a):
			if a<=0:return
			k=1.-a;b[0]=c[0]*a+b[0]*k;b[1]=c[1]*a+b[1]*k;b[2]=c[2]*a+b[2]*k;b[3]=a+b[3]*k
		def cx(b,a):k=1.-a;b[0]*=k;b[1]*=k;b[2]*=k;b[3]*=k
		def dJ(u,v,s):
			a=[0.,0.,0.,0.]
			if 140<=u and 38<=v<=156:
				a3(a,do,au(by(u,v,ac),s))
				if a[3]>0:
					a3(a,cw(v),au(by(u,v,dj),s));a3(a,dp,au(by(u,v,dk),s));e=au(by(u,v,dl),s)
					if e>0:
						cx(a,e)
						for k,l in dm:
							f=min(v-k,l-v)
							if f>-1.5:a3(a,cw(v),e*au(-f,s))
					for g,h,m in dn:
						if abs(u-g)<4 and abs(v-h)<4:i=math.sqrt((u-g)**2+(v-h)**2);a3(a,(40,40,44),au(i-2.6,s));a3(a,m,au(i-1.6,s))
			c,d=u-bj[0],v-bj[1];r=math.sqrt(c*c+d*d)
			if r<ci[0][0]+2:
				for n,b in ci:
					j=au(r-n,s)
					if j<=0:continue
					if b=="tire":b=dH(c,d,max(r,.01))
					elif b=="gold":b=dI(c,d,max(r,.01))
					a3(a,b,j)
				cx(a,au(r-bF,s))
			return a
		def bL(a):
			b=a[3]
			if b<=.002:return 0
			return(int(a[0]+.5)|(int(a[1]+.5)<<8)|(int(a[2]+.5)<<16)|(int(b*255+.5)<<24))
		def dK(s):
			w,h=int(bi*s),int(a9*s);b=1./s;a=[0]*(w*h)
			for y in range(h):
				v=(y+.5)*b;d=y*w
				for x in range(w):a[d+x]=bL(dJ((x+.5)*b,v,s))
				yield None
			c=[]
			for y in range(h):c.extend(a[y*w:(y+1)*w][::-1])
			yield w,h,a,c
		def cy(s,c):
			f=br[1]+1;a=int(math.ceil(2*f*s));d=a/2.;e=[0]*(a*a)
			for y in range(a):
				if y%4==3:yield None
				for x in range(a):
					r=math.sqrt((x+.5-d)**2+(y+.5-d)**2)/s;b=min(au(r-br[1],s),au(br[0]-r,s))
					if b>0:e[y*a+x]=bL([c[0]*b,c[1]*b,c[2]*b,b])
			yield a,e
		def cz(s):a=int(round(s*100));return{"player":"%sframe_player_%d"%(aT,a),"target":"%sframe_target_%d"%(aT,a),"blank":"%ssnap_blank_%d"%(aT,a)}
		def dL(s):
			c=cz(s);a=None
			for a in dK(s):
				if a is None:yield None
			w,h,e,f=a;b=bP(s);g=[bL([bn[0],bn[1],bn[2],1.])]*(b*b)
			for a in cy(s,aL):
				if a is None:yield None
			d,i=a;j=bN(aL,s)
			def k():Bridge.put_texture(c["player"],w,h,e);Bridge.put_texture(c["target"],w,h,f);Bridge.put_texture(c["blank"],b,b,g);Bridge.put_texture(j,d,d,i)
			yield k
		def dM(s):
			if s in i["art_scales"]:return True
			if s in i["art_failed"]:return False
			if not any(a["kind"]=="art"and a["s"]==s for a in i["art_jobs"]):i["art_jobs"]=i["art_jobs"]+[{"kind":"art","s":s,"gen":dL(s)}]
			return
		def bM():
			a=set([bz(o["scale"])/100.])
			if o["pscale_on"]:a.add(bz(o["pscale"])/100.)
			for v in bd.values():
				if v is not None:a.add(v/100.)
			return a
		def dN():
			c=bM();c.update(f.get("s")for f in t.values()if f.get("art"));a=[g for g in i["art_scales"]if g not in c]
			if not a:return
			d=set(str(int(round(h*100)))for h in a);e=tuple(aT+p for p in("frame_","noto_","snap_blank_"));b=[r for r in i["textures"]if r.startswith(e)and r.rsplit("_",1)[-1]in d]
			for s in a:i["art_scales"].discard(s)
			for n in b:i["textures"].discard(n)
			if b:safe(lambda:Bridge.on_main(lambda:Tex.drop(b)))
		def bN(a,s):return "%snoto_%d_%d_%d_%d"%(aT,a[0],a[1],a[2],int(round(s*100)))
		def dO(c,s,name):
			a=None
			for a in cy(s,c):
				if a is None:yield None
			b,d=a;yield lambda:Bridge.put_texture(name,b,b,d)
		def dP(b,s):
			a=bN(b,s)
			if a in i["textures"]:return a
			if a not in i["art_failed"]and not any(d.get("name")==a for d in i["art_jobs"]):c={"kind":"noto","s":s,"name":a,"gen":dO(b,s,a)};i["art_jobs"]=i["art_jobs"]+[c]
			return
		def bO():return any("out"not in a for a in i["art_jobs"])
		def dQ(budget):
			a=time.time()+budget
			for j in i["art_jobs"]:
				while "out"not in j:
					try:r=next(j["gen"])
					except Exception:r=False
					if r is not None:j["out"]=r
					elif time.time()>=a:return True
				if time.time()>=a:break
			return bO()
		def dR():
			b=i["art_jobs"];c=bM();c.update(g.get("s")for g in t.values());a=[];d=False
			for j in b:
				if j["s"]not in c:continue
				if d or "out"not in j:a.append(j);continue
				r=j["out"];d=True;e=r is not False and bool(safe(lambda:r()or True,False))
				if j["kind"]=="art":(i["art_scales"]if e else i["art_failed"]).add(j["s"]);i["art_dirty"]=True
				elif not e:i["art_failed"].add(j["name"])
				else:
					for f in t.values():f["last"]=None
			if len(a)!=len(b):i["art_jobs"]=a
		def bP(s):return int(math.ceil(2*(bF+2)*s))
		def bQ():return bP(max(bM()))
		def dS(graphic,item):
			b=cn.get(graphic)
			if b is None:
				a=item.GetItemData()
				if a is None:return 0,False,False
				b=cn[graphic]=(int(a.AnimID or 0),bool(a.IsPartialHue),bool(a.IsContainer))
			return b
		def dT(layer,worn):
			a=worn.get("robe",(0,0))[0]
			if layer=="tunic":return worn.get("tunic",(0,0))[0]==568 and a and a not in bC
			if layer=="arms":return bool(a)and a not in bC
			if layer=="torso":
				if a and a not in bC:return True
				b=worn.get("tunic",(0,0))[0];return bool(b)and b not in(5441,5442)and worn.get("torso",(0,0))[0]in(30762,30763)
			if layer in("helmet","hair")and a:
				if a>12659:return a in(19357,30742)
				if a<=9863:return a>=9859 or 8270<=a<=8271
				return a in(12217,12659)
			return False
		def cA(serial):
			m=cp(serial)
			if m is None:return
			e=int(m.Graphic or 0);g=c4.get(e)
			if g is None:return{"body":0,"pieces":()}
			k=c7 if e==c6 else int(m.Hue or 0)&16383;l=e in c5;b,h={},{}
			for a in b7:
				f=API.FindLayer(a,serial)
				if f is None:continue
				try:i=int(f.Graphic or 0);b[a]=(i,int(f.Hue or 0)&16383);h[a]=dS(i,f)
				except Exception:b.pop(a,None)
			d=b7
			if "cloak"in b:
				if b.get("robe",(0,0))[0]in da:d=c9
				elif h["cloak"][2]:d=c8
			if b.get("arms",(0,0))[0]in db:d=tuple({"arms":"torso","torso":"arms"}.get(r,r)for r in d)
			j=[((g,),k,True)]
			for a in d:
				if a not in b or dT(a,b):continue
				c,n,p=h[a]
				if not c:continue
				if c==970 and e in(694,695):c=547
				o=(c+b6,c+b5)if l else(c+b5,c+b6);j.append((tuple(s for s in o if s<=65535),b[a][1],n))
			return{"body":g,"pieces":tuple(j)}
		def cB(doll):
			def a():
				a=[]
				for c,d,e in doll["pieces"]:
					b=Bridge.gump_pixels(c,d,e)
					if b is not None:a.append(b)
				return a
			return Bridge.on_main(a)or[]
		def dU(layers):
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
		def dV(body,layers,bounds):
			if not body and layers:w,h=layers[0][1:];a=max(w,h)*1.08*100./o["pzoom"];return(w-a)/2.+o["pdx"],(h-a)/2.+o["pdy"],a
			a=b8*100./o["pzoom"]
			if bounds is None or bounds[1]is None:d,e=98,70;b,c=d-a/2.,e-a/2.
			else:f,g,i=bounds;b=(f+i+1)/2.-a/2.;c=g-2
			return b+o["pdx"],c+o["pdy"],a
		def bR(f,body,out):
			b=[];E=isinstance(f,list)
			for F,(c,w,h)in enumerate(f):
				if isinstance(c,list):b.append((c,w,h))
				else:
					k=(list(c),w,h);b.append(k)
					if E:f[F]=k
				yield None
			l=None
			if body and b:
				for r in dU(b):
					if r is None:yield None
					else:l=r
			m,n,o=dV(body,b,l);a=int(math.ceil(o))+1;q,s=int(math.floor(m)),int(math.floor(n));G=bn;t=[G]*(a*a)
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
		def cC(serial):
			if serial and(serial not in i["snaps"]or serial in i["stale"])and not any(b[0]==serial for b in i["snap_queue"]):
				a=i["snap_job"]
				if a is not None and a.get("serial")==serial:return
				i["snap_queue"].append((serial,0.))
		def dW(got,job):
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
			for r in bR(job["layers"],0,job["size"]):yield r
		def cD():a=i["snap_job"];return a is not None and "out"not in a
		def dX(now,budget=.008):
			a=i["snap_job"]
			if a is None or "out"in a:return False
			b=now+budget
			while not API.StopRequested:
				try:r=next(a["gen"])
				except StopIteration:a["out"]=False;return False
				except Exception:a["out"]=None;return False
				if r is not None:a["out"]=r;return False
				if time.time()>=b:return True
		def dY(now):
			a=i["snap_job"]
			if a is None or "out"not in a:return
			i["snap_job"]=None;r=a["out"]
			if r is None:
				if not any(f[0]==a["serial"]for f in i["snap_queue"]):i["snap_queue"].append((a["serial"],now+bo))
				return
			if r is False:return
			b,d,c=a["serial"],"%ssnap_%d"%(aT,a["serial"]),a["size"]
			if c!=bQ():
				if not any(g[0]==b for g in i["snap_queue"]):i["snap_queue"].append((b,now))
				return
			if safe(lambda:Bridge.put_texture(d,c,c,r)or True,False):
				i["snaps"][b]={"name":d,"creature":False}
				if b==i["me"]and a8.f is not None:R["layers"]=(a["layers"],a["body"])
				cF(b)
		def cE(now):
			dY(now)
			if i["snap_job"]is not None:return
			for h,(a,j)in enumerate(i["snap_queue"]):
				if j<=now:del i["snap_queue"][h];break
			else:return
			if a in i["snaps"]and a not in i["stale"]:return
			b=cA(a)
			if b is None:i["snap_queue"].append((a,now+bo));return
			i["stale"].discard(a);c=bQ()
			if not b["body"]:
				f=safe(lambda:Bridge.on_main(lambda:Bridge.creature_pixels(a)))if Bridge.creatures else None
				if f is None:
					if Bridge.creatures and i["snap_tries"].get(a,0)<3:i["snap_tries"][a]=i["snap_tries"].get(a,0)+1;i["snap_queue"].append((a,now+bo));return
					i["snaps"][a]={"name":None,"creature":True};cF(a);return
				d={"serial":a,"size":c,"layers":None,"body":0};d["gen"]=dW(f,d);i["snap_job"]=d;return
			e,g=safe(lambda:cB(b),[]),b["body"]
			if not e:i["snap_queue"].append((a,now+bo));return
			i["snap_job"]={"gen":bR(e,g,c),"serial":a,"size":c,"layers":e,"body":g}
		def cF(serial):
			for a,b in t.items():
				if a5(a)==serial:b["last"]=None
		def cG():
			i["stale"]=set(i["snaps"])
			for a in t:cC(a5(a))
		bS=8
		def dZ(serial):
			a=i["recent"]
			if not serial or(a and a[-1]==serial):return
			if serial in a:a.remove(serial)
			a.append(serial)
			if len(a)>4*bS:del a[:-bS]
		def d_():
			a=set(a5(h)for h in t);a.update(n["serial"]for n in H);a.update(i["party"]);a.update(i["recent"][-bS:]);a.add(i["me"]);g=set(p.get("snap")for p in t.values());c=i["snaps"];e=[]
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
		def bT(key):return "target"if key=="target"else "player"
		def a5(key):
			if key=="player":return i["me"]
			if key=="target":return i["target"]
			return int(key[1:])
		bd={"player":None,"target":None};be={"player":None,"target":None};ay=F+2
		def bz(v):k=Kit.tscale*(.85 if Kit.compact else 1.);return v if k==1. else max(aB,min(aK,int(round(v*k))))
		def bU(key):
			a=bd.get(key)
			if a is not None:return a/100.
			if o["pscale_on"]and key[:1]=="m"and key[1:].isdigit()and int(key[1:])in i["party"]:return bz(o["pscale"])/100.
			return bz(o["scale"])/100.
		def d0(key):
			def a(w,h,mode):
				b=None;a=None
				if w and h:
					a=(int(w),int(h));e,d=a[0]-2*ay,a[1]-2*ay;c=int(min(100.*float(e)/bi,100.*float(d)/a9))
					if a6(key):c=min(c,int(100.*(d-B-av)/ac[3]))
					b=max(aB,min(aK,c))
				be[key]=a
				if b!=bd.get(key):bd[key]=b;i["art_dirty"]=True
			return a
		def cH(s):return max(a9*s,ac[3]*s+B+av)
		def d1(key):
			def a(h):
				c=int(h)-2*ay;a=100.*c/a9;b=a6(key)
				if b:a=min(a,100.*(c-B-av)/ac[3])
				s=max(aB,min(aK,int(a)))/100.;f=max(bi*s,ac[0]*s+(161-2*F)+4)if b else bi*s;d=0
				if b:
					e=int(math.ceil(cH(s)))+2*ay+1
					if e>int(h):d=e
				return int(math.ceil(f))+2*ay,d
			return a
		def a6(key):
			for c,(a,b,d)in e["piece"].items():
				if a==key and b==0:return True
			return False
		def d2(key,w,h):
			a=be.get(key)
			if not a:return w,h,0,0,False
			W,H=max(a[0],w+2*ay),max(a[1],h+2*ay);c=ay if bT(key)=="player"else W-ay-w;b=h
			if a6(key):b=max(h,int(math.ceil(cH(float(h)/a9))))
			return W,H,c,max(ay if b>h else 0,(H-b)//2),True
		def d3(key):
			def a():
				a=t.get(key)
				if not a or not a.get("box"):return
				b,e,w,f=a["box"];s=a["s"];c,d=int(round(ac[0]*s)),int(round(ac[2]*s))
				if bT(key)=="player":return b+c,b+d,True
				return b+w-d,b+w-c,False
			return a
		def d4(key):
			def a():
				a=t.get(key)
				if not a or not a.get("slot")or not a.get("box"):return
				c,b,d,h=a["box"];W,H=a["win"];return ay,W,H,b,h,b+int(round(ac[3]*a["s"]))
			return a
		def aN(key):s=bU(key);return s,int(bi*s),int(a9*s)
		def cI(b,w,a,x1):return(a,x1)if b=="player"else(w-x1,w-a)
		def d5(key):
			a,w,h=aN(key)
			if key=="player":return 60,420
			if key=="target":return 60+w+20,420
			i=[b["serial"]for b in H].index(int(key[1:]))if key[1:].isdigit()else 0;return 60+(i//4)*(w+10),40+(i%4)*(h+2)
		def bV(serial,action=None):
			def h(*a):
				if ad():ar(("follow_serial",serial))();return
				if action:ar(action)()
			return h
		def cJ(key):
			def a():
				a=t.get(key);g=a and a.get("g")
				if not g:return
				b=ad();c=not b and not o["click"]and i.get("removing")
				if not b and not o["click"]and not c:return
				p=a7(a)
				if p!=a.get("seen")or time.time()<a.get("drag_until",0.):a["seen"]=p;return
				ar(("follow"if b else("remove_click"if c else "click"),key))()
			return a
		def d6(key,g):
			def a(*b):
				a=t.get(key)
				if a is not None and a.get("g")is g and not i["shutting"]:a["g"]=None;ar.add(("closed",key),dup=True)
			return a
		def bf(g,x,y,w,h,a,alpha=1.):return P(g,x,y,w,h,alpha,"#%02x%02x%02x"%a)
		def cK(g,c,rows):
			for b,(d,e,f,h)in zip(b2,rows):
				for v in(("hits","poison","yellow")if b=="hits"else(b,)):a=G.CreateGumpSimpleProgressBar(f-d,h-e,b3,c2[v],0,100);a.SetPos(d,e);g.Add(aj(a));c["bar_"+v]=a
		def d7(key):
			p=t.get(key,{}).get("g");s,w,n=aN(key);r=bT(key);x,y=i["pos"].get(key)or d5(key)
			if q(p):x,y=p.GetX(),p.GetY()
			if key in t:t[key]["g"]=None
			a=lambda v:int(round(v*s));A=bool(i["art"])and s in i["art_scales"];W,H,d,e,I=d2(key,w,n);B=not o["lock"]and not HOST.layout_locked(ae+"."+key);g=G.CreateGump(True,B)
			if aP(key):x,y=int(x),int(y);g.SetRect(x,y,W,H);aG(g,x,y,W,H);a_(g)
			else:x,y=ak(g,x,y,W,H)
			c={}
			if I:M=F;ah(g,W,H);J(g,M,M,W-2*M,H-2*M)
			f=d+(a(bj[0])if r=="player"else w-a(bj[0]));h=e+a(bj[1]);O,P=cI(r,w,a(cj[0]),a(cj[1]));j=[(d+O,e+a(at),d+P,e+a(dx))for at,dx in dq];b=int(bF*s);C=cz(s)if A else None
			if A:u=bP(s);c["snap"]=Tex.control(g,C["blank"],f-u//2,h-u//2,u,u);cK(g,c,j);Tex.control(g,C[r],d,e,w,n);z=int(math.ceil(2*(br[1]+1)*s));c["noto"]=Tex.control(g,bN(aL,s),f-z//2,h-z//2,z,z)
			else:
				if not I:ah(g,w,n,corners=False)
				k=2*b;J(g,f-b,h-b,k,k,alpha=.95);m=max(2,int(round(3*s)));c["edge"]=[bf(g,f-b,h-b,k,m,aL),bf(g,f-b,h+b-m,k,m,aL),bf(g,f-b,h-b,m,k,aL),bf(g,f+b-m,h-b,m,k,aL)];J(g,j[0][0]-4,j[0][1]-4,j[0][2]-j[0][0]+8,j[-1][3]-j[0][1]+8,alpha=.9);cK(g,c,[(dy,eQ+1,eR,eS-1)for dy,eQ,eR,eS in j])
			c["strip"]=bf(g,f-22,h+int(b*.42),44,aU+4,(0,0,0),.65);c["strip"].IsVisible=False
			if key=="player":K="Click: target yourself"if o["click"]else "Your character's frame"
			else:K=("Click: make them your target. Alt+click: auto-follow (again to stop)"if o["click"]else "Alt+click: auto-follow (again to stop)")
			D(g,d,e,w,n,cJ(key),None,movable=B);N,Q=cI(r,w,a(ac[0]),a(ac[2]));D(g,d+N,e+a(ac[1]),Q-N,a(ac[3])-a(ac[1]),cJ(key),K,movable=B);d9(g,key,d,e)
			for R in("name","hits","mana","stam","status","portrait_text"):c["lbl_"+R]=aj(l(g,"",0,0))
			E=None
			if key=="player":c["guard_bg"]=bf(g,0,0,1,1,(0,0,0),.65);c["guard_bg"].IsVisible=False;c["lbl_guard"]=aj(l(g,"",0,0));E=(d+a(ac[2])-6,e+max(1,a(ac[1])-aU-3))
			t[key]={"g":g,"c":c,"rows":j,"centre":(f,h),"hole":b,"s":s,"art":A,"names":C,"last":None,"seen":(x,y),"noto":None,"variant":None,"snap":None,"code_move":False,"shown":{},"bars":{},"serial":None,"box":(d,e,w,n),"win":(W,H),"slot":be.get(key),"rides":a6(key)}
			if E is not None:t[key]["guard_at"]=E
			i["art_dirty"]=True;G.AddControlOnDisposed(g,d6(key,g));G.AddGump(g);Kit.no_snap(g);aH(g,d8(key));L(p)
		def d8(key):
			def a():
				a=t.get(key)
				if a is None or not q(a.get("g")):return
				p=a7(a)
				if p is not None and p!=a.get("seen"):
					a["seen"]=p;a["code_move"]=True
					if not aP(key):bw(key,p)
				bv()
			return a
		def d9(g,key,ox,oy):
			if key in("player","target"):return
			a=ce if N(ce[0])[0]>0 else W;x,y,c=ox+cf,oy+cf,bV(int(key[1:]),("xclose",key));d="Close this frame. Alt+click: auto-follow (again to stop)"
			if N(a[0])[0]>0:b=G.CreateGumpButton("",C,a[0],a[1],a[2]);b.SetPos(x,y);g.Add(b);Kit.on_click(b,c);b.SetTooltip(d);return
			l(g,"x",x+2,y,O);D(g,x,y,max(14,z("x")+4),16,c,d)
		def bl(key):
			a=t.pop(key,None)
			if a:
				i["art_dirty"]=True;g=a.get("g")
				if q(g):
					p=a7(a)
					if p is not None and not aP(key):bw(key,p)
				a["g"]=None;L(g)
		def ea(w,h,side,p=None):
			d=t.get("player")
			if d is None or not q(d.get("g")):return
			if p is None:p=a7(d)
			if p is None:return
			c,b=p;g,i=d.get("win")or aN("player")[1:];W,H=al()
			if side==1:
				a=(c-w-2,b)
				if a[0]<0:a=(c+g+2,b)
			elif side==2:
				a=(c+g+2,b)
				if W>0 and a[0]+w>W:a=(c-w-2,b)
			else:
				j,k=cN(b,i);e=b+i+2+j+ax("player",True);a=(c,e)
				if H>0 and e+h>H:
					f=b-h-2-k-ax("player",False)
					if f>=0 or f+h>H-e:a=(c,f)
			x,y=a
			if W>0:x=max(0,min(x,W-w))
			if H>0:y=max(0,min(y,H-h))
			return(x,y)
		bW="UnitFrames_hbar_held";cL=1.;aO={"at":0.,"held":None}
		def eb():
			try:return Tz.get(None,"CurrentProfile",Tz.T("ClassicUO.Configuration.ProfileManager"))
			except Exception:return
		def cM(want):
			a=eb()
			if a is None:return
			if aO["held"]is None:aO["held"]=bG(bW)=="1"
			b=aO["held"]
			if want:
				if not b and not bool(Tz.get(a,"OpenHealthBarForLastAttack")):return
				if not b:Tz.put(a,"OpenHealthBarForLastAttack",False);bu(bW,"1");aO["held"]=True
				try:
					t=Tz.T("ClassicUO.Game.UI.Gumps.BaseHealthBarGump");c=Tz.get(None,"LastAttackBar",t)
					if c is not None and not c.IsDisposed:c.Dispose()
				except Exception:pass
			elif b:Tz.put(a,"OpenHealthBarForLastAttack",True);bu(bW,"");aO["held"]=False
		def ec(now):
			if 0<=aO["at"]-now<=cL:return
			aO["at"]=now+cL
			try:cM(bool(o["hide_bar"]and o["target"]))
			except Exception:pass
		def ed(w,h,side):
			a=t.get("player")
			if a is None or not q(a.get("g")):return
			p=a.get("seen");b=None
			if p is not None:b=(p,a.get("win")or aN("player")[1:],side,o["cast"],e["stack"].get("player"),al(),w,h)
			if b is None or b!=ba["sig"]or ba["at"]is None:ba["at"]=ea(w,h,side,p);ba["sig"]=b if ba["at"]is not None else None
			c=ba["at"];return None if c is None else(a["g"],c)
		def cN(fy,fh):
			if not o["cast"]:return 0,0
			H=al()[1]
			if H>0 and fy+fh+aY+aX>H:return 0,aX+aY
			return aX+aY,0
		def cO(fr):
			p=fr.get("seen")
			if p is None:return
			g,d,h,c=fr.get("box")or(0,0,0,aN("player")[2]);b=p[1]+d;e,i=cN(b,c);x=p[0]+fr["rows"][0][0]-6;f=(fr.get("win")or aN("player")[1:])[1]
			if e:
				a=ax("player",True);y=b+c+aY
				if a:y=max(y,p[1]+f+a+aY)
				return x,y
			a=ax("player",False);y=b-aX-aY
			if a:y=min(y,p[1]-a-aX-aY)
			return x,y
		def bX():g,m["g"]=m["g"],None;m["leader"]=None;m["shown"]=None;L(g)
		def ee(fr):
			bX();d=fr["rows"];w,h=d[0][2]-d[0][0]+12,aX;g=G.CreateGump(False,False);ah(g,w,h,corners=False,mouse=False);c={}
			for k in("cast","done","fail"):a=G.CreateGumpSimpleProgressBar(w-12,h-10,b3,dg[k],0,100);a.SetPos(6,5);g.Add(aj(a));c[k]=a
			c["lbl"]=aj(l(g,"",6,4));b=cO(fr)or(0,0);ak(g,b[0],b[1],w,h);G.AddGump(g);g.IsVisible=False;aV(g,fr["g"]);m.update({"g":g,"c":c,"shown":None,"at":b,"leader":fr["g"],"s":fr["s"],"w":w})
		def cP(now):
			a=t.get("player")
			if not o["cast"]or a is None or not q(a.get("g")):
				m["state"]=None;i["jr"]=None
				if m["g"]is not None:bX()
				return
			c=None
			if i["jr"]is None:i["jr"]=aa()
			else:c=i["jr"].new()
			if c:
				g=i["names"].get(i["me"])or ""
				for b in c:
					d=b.name or ""
					if g and d==g:
						e=di.get(b.low.strip())
						if e is not None:f=aJ(e[0]);l=f[3]if f and f[3]else 1.;m.update({"spell":e[0],"start":min(now,b.at or now),"secs":max(.1,float(l)),"state":"cast","pct":0,"word":""});continue
					elif d and d!="System":continue
					if m["spell"]is None or now-m["start"]>m["secs"]+de:continue
					n=aq(b,aw)
					for p,r in dh:
						if n.startswith(p):
							if m["state"]!="cast":m["pct"]=100
							m.update({"state":"fail","word":r,"until":now+ch});break
			h=m["state"]
			if h=="cast":
				j=now-m["start"]
				if j>=m["secs"]:m.update({"state":"done","until":now+ch,"pct":100})
				else:m["pct"]=max(0,int(100*j/m["secs"]))
			elif h is not None and now>=m["until"]:m["state"]=None
			k=a["last"][5]if a.get("last")else None
			if k is not None and k[cq]:m["state"]=None
			ef(a)
		def ef(fr):
			b=m["state"];g=m["g"]
			if b is None:
				if g is not None and m["shown"]is not None:m["shown"]=None;aI(g,"IsVisible",False)
				return
			if g is None or not q(g)or m["s"]!=fr["s"]or m["leader"]is not fr["g"]:ee(fr);g=m["g"]
			c=cO(fr)
			if c is not None and c!=m["at"]:m["at"]=c;g.SetRect(c[0],c[1],m["w"],aX);aF(g)
			f=m["spell"]if b!="fail"else "%s: %s"%(m["spell"],m["word"]);d=(b,m["pct"],f);a=m["shown"]
			if d==a:return
			m["shown"]=d;e=m["c"]
			if a is None or a[0]!=b:
				for k in("cast","done","fail"):e[k].IsVisible=k==b
			if a is None or a[0]!=b or a[1]!=d[1]:e[b].SetProgress(float(d[1]),100.)
			if a is None or a[2]!=f:h=M(f,m["w"]-16);A(e["lbl"],h,C);e["lbl"].SetPos(max(6,(m["w"]-bq(h))//2),4)
			if a is None:g.IsVisible=True
		def eg(now):
			if not o["guard"]:i["guard"]=False
			elif now>=i["next_guard"]:i["next_guard"]=now+.5;i["guard"]=HOST.guarded()
			a=t.get("player")
			if a is None or "guard_at"not in a or not q(a.get("g")):return
			d=i["guard"]
			if d is None:b,c="?",k
			elif d:b,c="GUARDED",I
			else:b,c="",C
			e,y=a["guard_at"];bm(a,"guard",b,e,y,c,"right")
			if a["shown"].get("guard_bg")!=b:
				a["shown"]["guard_bg"]=b;f=a["c"]["guard_bg"]
				if b:g=z(b)+8;a1(f,e-g+4,y-1,g,aU+4)
				f.IsVisible=bool(b)
		def bm(fr,name,text,x,y,hue,align="left"):
			if align=="right":x-=bq(text)if text else 0
			elif align=="center":x-=(bq(text)if text else 0)//2
			a=(text,hue,int(x),int(y));c=fr["shown"];b=c.get(name)
			if b==a:return
			c[name]=a;d=fr["c"]["lbl_"+name];A(d,text,hue)
			if b is None or b[2]!=a[2]or b[3]!=a[3]:am(d,a[2],a[3])
		def bY(fr,variant,cur,mx):
			a=(float(max(0,cur)),float(max(1,mx)))
			if fr["bars"].get(variant)==a:return
			b=fr["c"].get("bar_"+variant)
			if b is not None:b.SetProgress(a[0],a[1]);fr["bars"][variant]=a
		def eh(fr,want):
			if fr["variant"]==want:return
			fr["variant"]=want
			for v in("hits","poison","yellow"):
				a=fr["c"].get("bar_"+v)
				if a is not None:
					a.IsVisible=v==want
					if v!=want:a.SetProgress(0.,1.);fr["bars"][v]=(0.,1.)
		def ei(fr,a):
			if fr["noto"]==a:return
			c=fr["c"]
			if fr["art"]:
				b=dP(a,fr["s"])
				if b is None:return
				c["noto"].TextureName=b
			else:
				for d in c["edge"]:d.SetBaseColor(a[0],a[1],a[2],255)
			fr["noto"]=a
		def ej(fr,serial):
			if not fr["art"]:return{}
			a=not serial
			if fr["shown"].get("snap_hidden")!=a:fr["shown"]["snap_hidden"]=a;fr["c"]["snap"].IsVisible=not a
			if a:return{}
			cC(serial);c=i["snaps"].get(serial)or{};b=c.get("name")or fr["names"]["blank"]
			if fr["snap"]!=b:fr["snap"]=b;fr["c"]["snap"].TextureName=b
			return c
		def ek(cur,mx):return int(round(100.*cur/mx))if mx>0 else 0
		def el(key):
			a=t.get(key)
			if a is None or not q(a.get("g")):return
			b=a5(key)
			if b!=a["serial"]:a["serial"]=b;dZ(b)
			d=cu(b);r=b==i["me"];B=key!="target"and b and b==i["target"];D=ej(a,b);F=a["c"];G=(b,B,o["numbers"],a["snap"],bool(D.get("creature")),d)
			if G==a["last"]:return
			a["last"]=G;H=O if B else C;e,n="",""
			if not b or d is None:
				I,H,f,s=aL,k,((0,1),)*3,"hits"
				if not b:g,c="",("","","");n="No target"
				else:g=E(i["names"].get(b)or "Unknown",b,None,r);c=("Out of range","","")
			else:
				p=d[cq];J=aZ(d[cr],d[ct],d[cs]);g=E(d[bx]or i["names"].get(b)or "Unknown",b,None if p else d[bK],r)+("  "+J if J else "");s="poison"if d[cr]else("yellow"if d[cs]else "hits");f=((d[du],d[dv]),(d[dw],d[dz]),(d[dA],d[dB]));I=aL if p else Kit.cb_rgb(d[bK],b4.get(d[bK],b4["gray"]));e="DEAD"if p else("PARA"if d[ct]else "")
				if D.get("creature"):n="No picture"
				c=[]
				for h,(K,u)in enumerate(f):
					if u<=0:c.append(""if h else "--")
					elif r or h:c.append("%d/%d"%(K,u))
					else:c.append("%d%%"%ek(K,u))
				if p:c[0]="Dead"
				c=tuple(c)
			if not o["numbers"]and c and c[0]!="Out of range":c=("","","")
			eh(a,s);bY(a,s,f[0][0],f[0][1]);bY(a,"mana",f[1][0],f[1][1]);bY(a,"stam",f[2][0],f[2][1]);ei(a,I);L=a["rows"]
			for h,S in enumerate(b2):v,l,w,x=L[h];bm(a,S,c[h],w-8,l+(x-l-aU)//2-1,C,"right")
			v,l,w,x=L[0];y=max(20,w-v-16-(bq(c[0])+10 if c[0]else 0));m=a["shown"].get("fit")
			if m is None or m[0]!=g or m[1]!=y:m=a["shown"]["fit"]=(g,y,M(g,y))
			bm(a,"name",m[2],v+8,l+(x-l-aU)//2-1,H);A,N=a["centre"];P=a["hole"];Q=N+int(P*.42);bm(a,"status",e,A,Q+2,j if e=="DEAD"else O,"center")
			if a["shown"].get("strip")!=e:
				a["shown"]["strip"]=e
				if e:R=z(e)+10;a1(F["strip"],A-R//2,Q,R,aU+4)
				F["strip"].IsVisible=bool(e)
			bm(a,"portrait_text",M(n,2*P-6)if n else "",A,N-aU//2-1,k,"center")
		def em():
			a=[]
			if o["player"]:a.append("player")
			if o["target"]and(i["target"]or not o["hide_empty"]):a.append("target")
			a.extend("m%d"%b["serial"]for b in H);return a
		def en():
			c=em()
			for a in list(t):
				if a not in c:bl(a)
			for a in c:
				b=t.get(a)
				if(b is None or not q(b.get("g"))or b.get("s")!=bU(a)or b.get("redo")or b.get("slot")!=be.get(a)or(b.get("slot")and b.get("rides")!=a6(a)))and(not i["art"]or dM(bU(a))is not None):d7(a)
				el(a)
		def cQ(key):
			def a():a=t.get(key);return a.get("g")if a else None
			return a
		def aP(key):return Kit.zone_up(ae+"."+key)
		def a7(fr):r=Kit.rect(fr.get("g"));return None if r is None else(r[0],r[1])
		def eo(now):
			for b,a in t.items():
				if not q(a.get("g")):continue
				p=a7(a)
				if p is None:continue
				if p!=a.get("seen"):
					a["seen"]=p
					if a.get("code_move"):a["code_move"]=False
					else:
						a["drag_until"]=now+bE
						if not aP(b):a["moved"]=a["dropped"]=True
					if not aP(b):bw(b,p,now+bE)
				else:
					a["code_move"]=False
					if a.get("dropped")and now>=a.get("drag_until",0.)and SNAP.pressed()is not True:a["dropped"]=False;ep(b)
			if i["pos_dirty"]and now>=i["pos_save_at"]:bv()
		def cR(key):
			a=t.get(key)
			if a is None or not q(a.get("g")):return
			p=a.get("seen")or a7(a)
			if p is None:return
			w,h=a.get("win")or aN(key)[1:];return p[0],p[1],w,h
		def ep(key):
			r=cR(key)
			if r is None:return
			x,y,w,h=r;f=None;g=i=None
			for n in t:
				if n==key:continue
				o=cR(n)
				if o is None:continue
				a,b,c,e=o
				for j,k in((a+c,b),(a+c,b+e-h),(a-w,b),(a-w,b+e-h),(a,b+e),(a+c-w,b+e),(a,b-h),(a+c-w,b-h)):
					d=max(abs(x-j),abs(y-k))
					if d<=aW and(f is None or d<f[0]):f=(d,j,k)
				if y<b+e+aW and b<y+h+aW:
					for j in(a+c,a-w,a,a+c-w):
						d=abs(x-j)
						if d<=aW and(g is None or d<g[0]):g=(d,j)
				if x<a+c+aW and a<x+w+aW:
					for k in(b+e,b-h,b,b+e-h):
						d=abs(y-k)
						if d<=aW and(i is None or d<i[0]):i=(d,k)
			if f is not None:l,m=f[1],f[2]
			else:l=g[1]if g else x;m=i[1]if i else y
			if(l,m)!=(x,y):bZ(key,l,m);t[key]["moved"]=True
		def bZ(key,x,y):
			a=t.get(key)
			if a is None or not q(a.get("g")):return
			w,h=a.get("win")or aN(key)[1:];g=a["g"];x,y=Kit.clamp(x,y,w,h);g.SetRect(int(x),int(y),w,h);aG(g,int(x),int(y),w,h);aF(g);a.update({"seen":(int(x),int(y)),"code_move":True,"moved":False});i["pos"][key]=a["seen"];i.update({"pos_dirty":True,"pos_save_at":time.time()+bE})
		def eq(force=False):
			p,b=t.get("player"),t.get("target")
			if(p is None or b is None or not q(p.get("g"))or not q(b.get("g"))):return
			e,g=al();i,w,j=aN("player");c,d=p.get("seen"),b.get("seen")
			if aP("player")or aP("target")or e<=0 or g<=0 or c is None or d is None:return
			f=bool(p.get("moved"));h=bool(b.get("moved"))
			if h and not f and not force:
				a=(e-d[0]-w,d[1])
				if a!=c:bZ("player",*a)
			elif f or force:
				a=(e-c[0]-w,c[1])
				if a!=d:bZ("target",*a)
		def er(key):
			a=a5(key)
			if not a:return
			if API.HasTarget()and Z(ae)in(None,"pick"):
				if aR(a,"hud.frame",aQ):API.Target(a)
			else:
				API.SetLastTarget(serial=a)
				if key!="target"and a!=i["me"]:i["target"]=a
		def bA(serial,auto=False):
			if not serial:V("target someone first, then click Add frame.",j);return
			i["dismissed"].discard(serial)
			if serial==i["me"]:V("that's you; your own frame is the player frame.");return
			for t in H:
				if t["serial"]==serial:t["auto"]=False;V("%s already has a frame."%t["name"]);bc();return
			if len(H)>=bp:V("%d frames is the limit."%bp,j);return
			d=cu(serial)
			if d is None:V("that isn't a mobile you can see.",j);return
			H.append({"serial":serial,"auto":auto,"name":d[bx]or "Unknown"});bc();V("added %s."%(d[bx]or "a frame"),I);bg();ag(ae)
		def b_(serial):
			for t in H:
				if t["serial"]==serial and t["auto"]:i["dismissed"].add(serial)
			H[:]=[a for a in H if a["serial"]!=serial];bl("m%d"%serial);bc();bg();ag(ae)
		def cS(serial):return any(a["serial"]==serial for a in H)
		def cT(kind):
			def a(serial):ar.add((kind,int(serial or 0)),dup=True)
			return a
		es=("Frame your target, or pick someone with a target cursor. Alt+click a frame: auto-follow (again to stop)");et="Click a person or their frame with a target cursor to remove it (each frame has an X too)";cU=40
		def bg():
			if i["shutting"]:return
			M=F;g,b,c=bh.begin(cd,M+30+B+cU+M)
			if not i["minimized"]:bh.frame(g);a=M+30+B;J(g,M,a,cd-2*M,cU);Q(g,b,"add",aS,M+12,a+12,"Add frame",es,on_click=ar("add_frame"));Q(g,b,"remove",aS,M+56+z("Add frame"),a+12,"Remove frame",et,on_click=ar("remove_frame"))
			bh.end(g);eu()
		bh=Kit.Window(ae,aQ,i,bt,bg,c0,c1,mini=(dc,dd),icon=7028,cleanup=a0,lock=True)
		def eu():
			c=bt["c"]
			if "status"in c:A(c["status"],"%s: %s"%(aQ,S(len(H),"frame")))
		cV={"rm":b_,"click":er,"add_ext":bA,"follow_serial":lambda serial:Y(serial,aQ)};cW=(("player","Show your own frame","Your HP, mana and stamina"),("target","Show the target frame","Your current target"),("hide_empty","Hide the target frame with no target","Shown only while you have a target"),("numbers","Show numbers on the bars","HP, mana and stamina as numbers (others' HP as a %)"),("lock","Lock the frames in place","Frames can't be dragged"),("cast","Show a cast bar under your frame","Your spell filling through its cast delay: green when cast, red when it fails"));ev=(("hide_bar","Hide TazUO's own target health bar","Avoids two target bars; untick to get your client's setting back"),("click","Click a frame to target it","Aims a target cursor if one is up, else sets your last target"),("party","Add a frame for each party member","While they are in your party"),("ignore_self","Ignore yourself as last target","Targeting yourself (a bandage, a heal) keeps your target frame"),("attack","Prefer the attack target","Frame who you attack, else your last target"),("mirror","Mirror the player and target frames","Drag either frame and the other mirrors it across the screen"),("guard","Show a GUARDED tag on your frame","GUARDED in guard zones, ? until known (enter or leave one), blank outside"));cX=aT+"snap_preview";ew="Frame size, percent of the art (%d-%d%%)"%(aB,aK);ex="Party members' frame size while ticked (%d-%d%%)"%(aB,aK);bB=(("pdx","Left / right","Move pictures left or right in the circle","%+d"),("pdy","Up / down","Move pictures up or down in the circle","%+d"),("pzoom","Zoom","Zoom pictures in or out (100%% = %d art pixels tall)"%b8,"%d%%"))
		def ey(w):
			a=max(z("All frames:"),24+z("Party members:"))
			def b(f,x,y):b=x+26+a;f.c["pscale"]=Kit.with_tip(Kit.add_slider(f.g,b,y+4,260,aB,aK,o["pscale"]),ex);f.c["pscale_lbl"]=l(f.g,"%d%%"%o["pscale"],b+272,y+2,k)
			c={"top":32,"sh":30+ao+4+10,"dx":12+ao+4+16,"ldy":0,"fh":26,"sw":180,"ugap":12,"lgap":12,"lw":max(z(d[1])for d in bB),"bdy":0,"bgap":18};return(("OTHERS' FRAMES  (%d of %d)"%(len(H),bp),(("custom",0,ez),),{"top":0,"sh":30+28+4+max(1,len(H))*24+6}),("OPTIONS",[("check",)+g for g in cW]+[("gap",-26*len(cW))]+[("check",)+h+({"dx":12+w//2},)for h in ev],{"pad":6}),("FRAME SIZE",(("slider","scale","All frames:",ew,aB,aK,{"lw":a,"lgap":14,"ldy":2,"sdy":4,"sw":260,"ugap":12,"vfmt":"%d%%"}),("check","pscale_on","Party members:","Party members' frames use the slider beside this; unticked, the size above",{"stay":True}),("custom",0,b)),{"top":34,"sh":96}),("PICTURE  (in each frame's circle)",[("custom",0,eA)]+[("slider",n,p+":",r,bs[n][0],bs[n][1],{"vfmt":s})for n,p,r,s in bB]+[("buttons",(("retake",K,"Retake pictures","Take every picture again (after a gear change)"),("reset",W,"Reset","Put the picture sliders back to defaults")))],c))
		def ez(f,x,y):
			g,w,a=f.g,f.w,f.store;d=x+12;Q(g,a,"add",K,d,y+28,"Add target","Frame your current target",on_click=ar("add_target"));Q(g,a,"pick",K,d+49+z("Add target"),y+28,"Pick...","Pick someone to frame",on_click=ar("pick"));Q(g,a,"clear",W,x+w-47-z("Clear all"),y+28,"Clear all","Remove everyone else's frame",on_click=ar("clear"));e=y+30+28+4;h=N(W[0])[0]or 30
			if not H:l(g,"No frames yet. Target someone, then click Add target.",x+12,e+3,k)
			for i,t in enumerate(H):
				b=e+i*24;c="(party)"if t["auto"]else "";j=w-24-h-6-(z(c)+8 if c else 0);m=E(t["name"],t["serial"]);n=M(m,j);l(g,n,x+12,b+3);D(g,x+12,b,j+8,20,bV(t["serial"]),"Alt+click: auto-follow (again to stop)")
				if c:l(g,c,x+12+z(n)+8,b+3,k)
				Q(g,a,"rm%d"%i,W,x+w-12-h,b,None,"Remove %s's frame. Alt+click: auto-follow (again to stop)"%m,on_click=bV(t["serial"],("rm",t["serial"])))
		def eA(f,x,y):
			g=f.g;J(g,x+12,y-2,ao+4,ao+4,alpha=1.)
			if i["art"]and i.get("running"):b0();Tex.control(g,cX,x+14,y,ao,ao)
			else:
				a=("Pictures","unavailable")if i.get("running")else("Turn Frames","on for a","preview");c=y+(ao-len(a)*18)//2
				for d,b in enumerate(a):l(g,b,x+14+(ao-z(b))//2,c+d*18,k)
		def cY():
			a=time.time();i["crop_changed"]=a
			if i["art"]and i.get("running")and a>=R["next_preview"]:R["next_preview"]=a+.3;b0()
		def eB(f):
			if a2(f.store,"retake"):R["layers"]=None;i["crop_changed"]=1.
			if a2(f.store,"reset"):
				for k,a,b,c in bB:f.c[k].SetValue(cl[k])
				cY()
		def eC(f,new):
			try:new["pscale"]=max(aB,min(aK,int(f.c["pscale"].Value)))
			except Exception:return
			A(f.c["pscale_lbl"],"%d%%"%new["pscale"])
		def eD(a,new):
			if(new["lock"],new["click"])!=(a["lock"],a["click"]):i["rebuild"]=True
			if new["party"]!=a["party"]:i["next_party"]=0.
			if new["mirror"]and not a["mirror"]:i["mirror_now"]=True
			i["art_dirty"]=True
			for k,b,c,d in bB:
				if new[k]!=a[k]:cY();break
		a8=Kit.Page(o,ey,bH,eD,adjust=eC,clicks=eB)
		def eE(g,x,y,w):R["store"]=a8.build(g,x,y,w).store
		def eF():a8.closed();R.update({"layers":None,"preview_gen":None})
		def b0():
			if i.get("running")and i["art"]:R["preview_want"]=True
		def eG():
			a=cA(i["me"]or bJ())
			if not a or not a["body"]:return
			b=safe(lambda:cB(a),[]);return(b,a["body"])if b else None
		def eH():
			a=R.get("layers")
			if a is None:
				a=safe(lambda:Kit.on_client(eG))
				if not a:return
				R["layers"]=a
			R["preview_gen"]=bR(a[0],a[1],ao)
		def eI(budget):
			b=time.time()+budget
			while R.get("preview_gen")is not None:
				a=R["preview_gen"]
				try:r=next(a)
				except Exception:
					if R.get("preview_gen")is a:R["preview_gen"]=None
					return
				if r is not None:
					if R.get("preview_gen")is a:R["preview_gen"]=None
					safe(lambda:Bridge.on_main(lambda:Bridge.put_texture(cX,ao,ao,r)));return
				if time.time()>=b:return
		def eJ(now):
			t=i["crop_changed"]
			if not t or now-t<.5:return
			i["crop_changed"]=0.
			if i["art"]:
				if a8.f is not None:b0()
				cG()
		co()
		def eK():
			cm();i.update({"me":bJ(),"running":True});m.update({"spell":None,"state":None,"shown":None});R.update({"preview_want":False,"preview_gen":None});co();dr();ds();a0.service("frames.player_anchor",ed);i["minimized"]=bh.start_min();i["art"]=Bridge.find()
			if not i["art"]:V("no drawn pictures on this client; using stone frames.")
			bg();bh.dock();a0.service("unitframes.add",lambda serial:ar(("add_ext",int(serial)))());a0.service("look.hud",eL);bd["player"]=bd["target"]=None;be["player"]=be["target"]=None
			for a in("player","target"):HOST.layout_add(ae+"."+a,cQ(a),aQ+" ("+a+")",{"fit":d0(a),"fill":"frame","exact":True,"pieces_out":True,"hug":d1(a),"untitled":True});a4(a,cQ(a),d3(a),d4(a));a0.add(HOST.layout_remove,ae+"."+a);a0.add(a4,a,None)
			az["fn"]=lambda:i["target"]
		def eL():
			for a in t.values():a["redo"]=True
		def cZ():return i["target"]or int(API.LastTargetSerial or 0)
		def eM():
			if bt["g"]is None:return
			if aC(bt):return
			a=time.time()
			if a<i["full_at"]and not i["queue"]and not i["rebuild"]and a+1.>i["full_at"]:
				if i["art"]:cE(a)
				if m["state"]=="cast":cP(a)
				return
			i["full_at"]=a+cg-.005;i["me"]=i["me"]or bJ();dE()
			while i["queue"]:
				c=i["queue"].pop(0);b=c[0]if isinstance(c,tuple)else c
				if bh.action(c):continue
				if b=="add_frame":
					d=cZ()
					if d and d!=i["me"]and not cS(d):bA(d);continue
					b="busy"if Z(ae)else "pick"
				elif b=="remove_frame":
					if not H:V("nobody else has a frame (turn off your own and the target frame in settings).")
					elif Z(ae):b="busy"
					else:V("click the person, or their frame, to remove.");i["removing"]=True;af(ca,cT("unpicked"))
				if b=="busy":V("a target cursor is up; try again after it.")
				elif b=="pick":V("choose who gets a frame.");af(ca,cT("picked"))
				elif b=="add_target":bA(cZ())
				elif b=="picked":
					if c[1]:bA(c[1])
					else:V("pick cancelled.")
				elif b=="remove_click":
					d=a5(c[1])
					if d and i.get("removing")and API.HasTarget():API.Target(d)
				elif b=="unpicked":
					i["removing"]=False
					if not c[1]:V("remove cancelled.")
					elif cS(c[1]):h=next((n["name"]for n in H if n["serial"]==c[1]),"");b_(c[1]);V("removed %s."%(h or "the frame"))
					else:V("they have no frame of their own.")
				elif b=="clear":
					for j in H:bl("m%d"%j["serial"])
					del H[:];bc();ag(ae)
					if o["party"]:V("cleared; party members come back while 'Add a frame for each party member' is ticked.")
					bg()
				elif b=="follow":
					d=a5(c[1])
					if d:Y(d,aQ)
				elif b in("closed","xclose"):
					e=c[1]
					if b=="xclose":bl(e)
					t.pop(e,None)
					if e in("player","target"):o[e]=False;bH();ag(ae);V("%s frame hidden; tick it again in settings."%e)
					elif e[1:].isdigit():b_(int(e[1:]))
				elif b in cV:cV[b](c[1])
			if i["rebuild"]:
				i["rebuild"]=False;bI()
				for e in list(t):bl(e)
			if i["art"]:
				f=bQ()
				if i["snap_px"]!=f:
					i["snap_px"]=f
					if i["snaps"]:cG()
			a=time.time()
			if a>=i["next_party"]:i["next_party"]=a+1.;dF()
			if i["art_jobs"]:dR()
			en()
			if i["art"]and i["art_dirty"]:i["art_dirty"]=False;dN()
			if a>=i["next_prune"]:i["next_prune"]=a+5.;d_()
			for k in t.values():k["moved"]=False
			eo(a);g=(a6("player"),a6("target"))
			if g!=i.get("rides"):i["rides"]=g;HOST.layout_refit()
			bb()
			if o["mirror"]:eq(force=i.pop("mirror_now",False))
			cP(a);ec(a);eg(a)
			if i["art"]:cE(a)
			eJ(a)
			if a>=i["next_save"]:
				i["next_save"]=a+10.;bI()
				if i["pos_dirty"]:bv()
		def eN():
			if i["shutting"]:return
			if bO():dQ(bD)
			if cD():dX(time.time(),bD)
			if R.get("preview_want"):
				R["preview_want"]=False
				if a8.f is not None:eH()
			if R.get("preview_gen")is not None:eI(bD)
		def c_():return bool(cD()or bO()or R.get("preview_want")or R.get("preview_gen")is not None)
		def eO():
			if m["state"]=="cast":return df
			return.03 if i["art_jobs"]or i["snap_job"]is not None or c_()else cg
		def eP():
			i.update({"shutting":True,"running":False,"removing":False,"snap_job":None,"art_jobs":[]});R.update({"preview_want":False,"preview_gen":None});az["fn"]=None;bv();bH();bc();safe(lambda:cM(False));aO["held"]=None
			for b in list(t):a=t.pop(b);g,a["g"]=a.get("g"),None;L(g)
			bX();i["jr"]=None
			if i["art"]and i["textures"]:c=list(i["textures"]);safe(lambda:Bridge.on_main(lambda:Tex.drop(c)));i["textures"].clear();i["art_scales"]=set()
			i["art"]=None;a0.close()
		return{"start":eK,"tick":eM,"stop":eP,"client_tick":True,"config_height":a8.height,"build_config":eE,"poll_config":a8.poll,"config_closed":eF,"thread_tick":eN,"interval":eO,"thread_wanted":c_}
	def be():
		W="spelltimers";Q="Buffs & Timers";aT="SpellTimers_settings";bB="SpellTimers_pos";bC="SpellTimers_min";aU="SpellTimers_active";bD=3834;aV,bE=320,46;aW=28;aX,aZ,bF=3,16,8;a_=.1;a0=.25;a1=5.;av=2240;a2=22;aA=2.5;a3=2;a4=1.;a5=4;a6=40;a7="spelltimers.ending";aB=120;a8=360;bG=frozenset(("polymorph",));bH=I;H=dict.fromkeys(("Clumsy","Feeblemind","Weaken","Curse"),("target","debuff",(0,1.2,0,0,0),0,"stat"));H.update(dict.fromkeys(("Agility","Cunning","Strength","Bless"),("target","buff",(0,1.2,0,0,0),0,"stat")));H.update({"Night Sight":("target","buff",(900,0,0,0,0),2340,None),"Invisibility":("target","buff",(0,1.2,0,0,0),0,"hidden"),"Paralyze":("target","debuff",(7,.2,0,0,0),0,"paralyzed"),"Poison":("target","debuff",None,0,"poisoned"),"Protection":("self","buff",(0,2.,0,15,240),0,None),"Reactive Armor":("self","buff",None,0,None),"Magic Reflection":("self","buff",None,0,None),"Incognito":("self","buff",(1,1.2,0,0,144),0,"name"),"Polymorph":("self","buff",(0,2.,0,0,240),0,"body"),});aF={("str",1):"Strength",("str",-1):"Weaken",("dex",1):"Agility",("dex",-1):"Clumsy",("int",1):"Cunning",("int",-1):"Feeblemind"};bI=("the spell fizzles","your concentration is disturbed","insufficient mana","more reagents are needed","target cannot be seen","that is too far away","target is too far away","this spell won't work on that","this spell is already in effect","the spell will not adhere to you","you currently have a re","this target already has reactive armor","incognito cannot be cast","you cannot disguise yourself","you cannot polymorph","you cannot incognito","you cannot cast that spell in this form");bJ=(("your reactive armor spell has been nullified","Reactive Armor"),("your protection spell has been nullified","Protection"));bK=(("you currently have a reflect spell","Magic Reflection"),("you currently have a reactive armor spell","Reactive Armor"));bL=("you can move!","you can move again!","you are no longer frozen");bM=(("you feel a bit nauseous",1),("you feel disoriented and nauseous",2),("you begin to feel pain throughout your body",3),("you feel extremely weak and are in severe pain",4),("you are in extreme pain, and require immediate aid",5));bN=(("looks extremely ill",2),("looks ill",1),("stumbles around in confusion and pain",3),("is wracked with extreme pain",4),("begins to spasm uncontrollably",5));bO=("the poison seems to have worn off","you feel cured of poison","you have been cured of all poisons");bP=("","Lesser","Regular","Greater","Deadly","Lethal");bQ=frozenset(("paralyze","paralyzed","poison","curse","clumsy","feeblemind","weaken","mindrot","strangle","corpseskin","evilomen","bloodoath","masscurse","mortalstrike"));bR={"buff":(47,154,60),"debuff":(194,45,45),"other":(207,174,42),"dim":(90,90,90)};bS=Q.lower()+":"
		def n(name):return str(name or "").lower().replace(" ","").replace("-","")
		aG={n(cs[0]):av+cr for cr,cs in enumerate(Kit.MAGERY)};aG["paralyzed"]=aG.get("paralyze",av);K={n(cu):cu for cu in H};K["paralyzed"]="Paralyzed";a9={"buff":0,"debuff":1};bT=frozenset(n(cv)for cv,cw in H.items()if cw[1]=="buff");h={"me":True,"debuff":True,"others":True,"stats":True,"icons":True,"rows":bF,"warn":0,"bars":False};cp=dict(h)
		def ba():b.update({"shutting":False,"docked":False,"queue":[],"rd":None,"pend":None,"landings":[],"last_land":None,"para":None,"pois":None,"stats":None,"next_sample":0.,"next_others":0.,"events":[],"icons_seen":False,"next_icons":0.,"warned":{},"rebuild":False,"dead":False,"skills":(0.,0.,-1e9)})
		b={"minimized":False,"shutting":False,"docked":False,"queue":[],"me":0,"name":"","prev_name":("",0.),"body":0,"hooked":False,"ct":None,"ct_looked":False,"ver":0,"active":False,"redraw":False};ba();c={};f={"str":[],"dex":[],"int":[]};u={"g":None,"c":{},"store":({},{}),"slots":[],"nrows":0};bb,aH,cq=ai(b,Q);Z=24;N=30;aI=42;R=3;bc=24;bd=.5;v={cz:{"g":None,"cells":[],"per":1,"lines":-1,"w":0}for cz in("player","target")};be={"rows":(aX,aZ),"warn":(0,aB)}
		def bf():aD(aT,";",h,be)
		def bg():aE(aT,";",h,("me","debuff","others","stats","icons","rows","warn","bars"),be)
		def bh():
			p=ap()
			try:return "%d,%d,%d"%(int(p.Strength),int(p.Dexterity),int(p.Intelligence))
			except Exception:return ""
		def bU():
			d=time.time();a=["t=%d"%int(d)];g=bh()
			for b in("str","dex","int"):
				for e in f[b]:a.append("e:%s,%d,%d,%d,%d,%s"%(b,e["d"],int(e["t"]),int(e["end"]or 0),1 if e.get("hide")else 0,g))
			for r in c.values():
				if r["who"]or "cast"not in r["srcs"]or "stat"in r["srcs"]or r["sid"]not in bT:continue
				a.append("r:%s,%s,%d,%d,%d"%(r["sid"],r["kind"],int(r["start"]),int(r["end"]or 0),int(r["most"]or 0)))
			U(aU,";".join(a))
		def bV(now):
			c=T(aU).split(";")
			try:d=float(c[0].split("=",1)[1])if c[0].startswith("t=")else 0.
			except(ValueError,IndexError):d=0.
			if not d or not 0<=now-d<=1800.:return
			e=bh()
			for p in c[1:]:
				try:
					g,j=p.split(":",1);b=j.split(",")
					if g=="e"and b[0]in f and h["stats"]:
						if len(f[b[0]])>=a5:continue
						k,l,a=int(b[1]),float(b[2]),float(b[3])
						if(a and a>now)or(not a and e and len(b)>7 and ",".join(b[5:8])==e):f[b[0]].append({"d":k,"t":l,"end":a or None,"hide":len(b)>4 and b[4]=="1"})
					elif g=="r"and b[0]in K:
						m,a,i=float(b[2]),float(b[3]),float(b[4])
						if a and max(a,i)<=now:continue
						r=z(0,b[0],b[1]if b[1]in a9 else "buff",m);r["end"],r["most"]=a or None,i or None;r["srcs"].add("cast");aN(r,now)
				except Exception:continue
		def z(who,sid,kind,now,name=""):
			a=(who,sid);r=c.get(a)
			if r is None:
				r={"key":a,"who":who,"sid":sid,"kind":kind,"start":now,"end":None,"most":None,"srcs":set(),"watch":None,"seen":False,"confirm":0.,"base":None,"level":0,"delta":0,"name":name,"away":0.,"icon":aG.get(sid,av),"end_src":None,"bar":None};c[a]=r
				if len(c)>a6:bW(a)
			else:
				r["kind"]=kind
				if name:r["name"]=name
			b["ver"]+=1;return r
		def m(key):
			r=c.pop(key,None)
			if r is None:return
			b["ver"]+=1;b["warned"].pop(key,None)
			if r["bar"]:S(r,time.time())
		def aN(r,now):
			if r["bar"]:S(r,now)
			if r["sid"]not in bG or r["who"]or not h["bars"]or r["end"]is None or r["end"]<=now:return
			a=K[r["sid"]];API.CreateCooldownBar(r["end"]-now,a,bH);r["bar"]=(a,r["end"])
		def S(r,now):
			a=r["bar"];r["bar"]=None
			if a is not None and a[1]>now:API.DeleteCooldown(a[0])
		def aO(key,src):
			r=c.get(key)
			if r is None:return
			r["srcs"].discard(src)
			if not r["srcs"]:m(key)
			else:b["ver"]+=1
		def bW(keep):
			b=sorted(c.values(),key=lambda r:(r["who"]==0,r["start"]))
			for a in b:
				if len(c)<=a6:break
				if a["key"]!=keep:S(c.pop(a["key"]),time.time())
		def bi(r):return(r["sid"],r.get("label"),r["delta"],r["level"],r["who"],r["name"],r["end"]is None,"stat"in r["srcs"],Kit.streamer)
		def aP(r):
			b=r["sid"];a=K.get(b)or r.get("label")or b
			if r["delta"]:a="%s %+d"%(a,r["delta"])
			if r["level"]and b=="poison":a="%s (%s)"%(a,bP[max(1,min(5,r["level"]))])
			if r["who"]:a="%s: %s"%(a,E(r["name"],r["who"])if r["name"]else "someone")
			return a
		def bj(now,force=False):
			s=b["skills"]
			if force or not 0<=now-s[2]<15.:s=b["skills"]=(an("Magery",s[0]),an("Evaluating Intelligence",s[1]),now)
			return s
		def bX(spell,now):
			b=H.get(spell)
			if b is None or b[2]is None:return
			e,f,g,c,d=b[2];h,i,j=bj(now);a=e+f*h+g*i
			if c:a=max(c,a)
			if d:a=min(d,a)
			return max(1.,a)
		def bY(spell,at,now):
			a=b["pend"]
			if a is not None:
				c=a["at"]+a["delay"];b["pend"]=None
				if a["side"]=="self"and at>=c-.05:af(a,b["me"],c,now)
				elif a["side"]=="target"and not a["cursor"]and at>=c+.2:
					e=int(API.LastTargetSerial or 0)
					if e:af(a,e,c,now)
			f=H.get(spell)
			if f is None:b["pend"]=None;return
			d=aJ(spell);g=d[3]if d and d[3]else 1.;bj(now,True);b["pend"]={"spell":spell,"sid":n(spell),"at":at,"delay":float(g),"side":f[0],"cursor":False,"body0":b["body"],"name0":b["name"]}
		def bZ(now):
			p=b["pend"]
			if p is None:return
			a=p["at"]+p["delay"]
			if now<a-.05:return
			if p["side"]=="self":
				if now>=a+.6:b["pend"]=None;af(p,b["me"],a,now)
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
			if c:af(p,c,now,now)
		def af(p,who,at,now):
			f,g=p["spell"],p["sid"];c=H[f];i=b["me"];d=not who or who==i;e=bX(f,now)
			if d and c[4]=="stat"and h["stats"]:b["landings"].append({"sid":g,"t":at,"dur":e or 0.});del b["landings"][:-6];bk(now);return
			m=None if d else API.FindMobile(who);j=str(m.Name or "")if m is not None else "";r=z(0 if d else who,g,c[1],at,j);r["start"]=at;r["srcs"].add("cast")
			if r["end_src"]!="icon":r["end"]=(at+e)if e else None;r["most"]=(at+c[3])if c[3]else None;r["end_src"]="cast"
			r["delta"],r["away"]=0,0.;a=c[4]
			if a=="stat"or(a in("body","name","hidden")and not d):a=None
			r["watch"],r["seen"]=a,False;r["confirm"]=now+2.
			if a=="body":r["base"]=p["body0"]
			elif a=="name":r["base"]=p["name0"]
			b["last_land"]=(r["key"],now);b["warned"].pop(r["key"],None);aN(r,now)
		def b_(now,d=False):
			p=b["pend"]
			if p is not None and(d or now>=p["at"]+p["delay"]-.3):b["pend"]=None;return
			a=b["last_land"]
			if a is not None and 0<=now-a[1]<=1.:
				b["last_land"]=None;r=c.get(a[0])
				if r is not None and r["srcs"]==set(("cast",)):m(a[0])
		def bk(now):
			a=[g for g in b["landings"]if 0<=now-g["t"]<=aA+1.];b["landings"]=a
			if not a:return False
			c=False
			for d in("str","dex","int"):
				for e in f[d]:
					if(e["end"]is not None or e["d"]<=0 or not 0<=now-e["t"]<=aA+1.):continue
					for l in reversed(a):
						if l["sid"]in("bless",n(aF[(d,1)]))and abs(e["t"]-l["t"])<=aA and l["dur"]:e["end"],e["cast"]=l["t"]+l["dur"],l["sid"];c=True;break
			if c:ag()
			return c
		def b0(stat,d,now):
			a=f[stat];b=0
			for e in a:b+=e["d"]
			if a and b+d==0:del a[:];return
			for i,e in enumerate(a):
				if e["d"]==-d:del a[i];return
			a.append({"d":d,"t":now,"end":None})
			if len(a)>a5:del a[0]
		def b1(vals,now):
			c=b["stats"];b["stats"]=vals
			if c is None:return
			a=False
			for i,e in enumerate(("str","dex","int")):
				d=vals[i]-c[i]
				if abs(d)>30:del f[e][:];a=True
				elif abs(d)>=a3:b0(e,d,now);a=True
			if a:
				p=b["pend"]
				if p is not None and p["side"]=="target"and H[p["spell"]][4]=="stat"and now>=p["at"]+p["delay"]-.4 and h["stats"]:b["pend"]=None;af(p,b["me"],now,now)
				bk(now);ag()
		def ag():
			k={};h=set();S,D,I=f["str"],f["dex"],f["int"]
			for a in S:
				if a.get("hide"):continue
				for d in D:
					if id(d)in h or d.get("hide")or d["d"]!=a["d"]or abs(d["t"]-a["t"])>a4:continue
					for e in I:
						if id(e)in h or e.get("hide")or e["d"]!=a["d"]or abs(e["t"]-a["t"])>a4:continue
						h.update((id(a),id(d),id(e)));i="bless"if a["d"]>0 else "curse";o=a["end"]or d["end"]or e["end"];bl(k,i,a["d"],min(a["t"],d["t"],e["t"]),o);break
					if id(a)in h:break
			for l in("str","dex","int"):
				for g in f[l]:
					if id(g)in h or g.get("hide"):continue
					i=n(aF[(l,1 if g["d"]>0 else-1)]);bl(k,i,g["d"],g["t"],g["end"])
			for i,j in k.items():
				p="buff"if j[0]>0 else "debuff";r=z(0,i,p,j[1])
				if "stat"not in r["srcs"]:r["start"]=j[1]
				r["srcs"].add("stat");r["delta"]=j[0]
				if r["end_src"]!="icon":r["end"],r["end_src"]=j[2],"stat";r["most"]=None
			for m in[t for t,s in c.items()if not s["who"]and "stat"in s["srcs"]and s["sid"]not in k]:r=c[m];r["delta"]=0;aO(m,"stat")
			b["ver"]+=1
		def bl(groups,sid,d,t,end):
			g=groups.get(sid)
			if g is None:groups[sid]=[d,t,end]
			else:
				g[0]+=d;g[1]=min(g[1],t)
				if end is not None and(g[2]is None or end>g[2]):g[2]=end
		def bm():
			for a in[g for g in c if not g[0]]:m(a)
			for d in f:del f[d][:]
			b.update({"stats":None,"pend":None,"landings":[],"para":None,"pois":None})
		def b2(now):
			p=ap()
			if p is None:return
			g=int(p.Serial);e=str(p.Name or "");l=bool(p.IsDead);n=bool(p.IsParalyzed);o=bool(p.IsPoisoned);q=bool(p.IsHidden);i=int(p.Graphic or 0);d=(int(p.Strength or 0),int(p.Dexterity or 0),int(p.Intelligence or 0))
			if g!=b["me"]:
				if b["me"]:bm()
				b["me"]=g
			if e!=b["name"]:
				if b["name"]:b["prev_name"]=(b["name"],now)
				b["name"]=e
			if l:
				if not b["dead"]:b["dead"]=True;bm()
				return
			if b["dead"]:b["dead"]=False;b["stats"]=None
			b["body"]=i
			for k,j,a in(("para","paralyzed",n),("pois","poison",o)):
				if a!=b[k]:
					b[k]=a
					if a:z(0,j,"debuff",now)["srcs"].add("flag")
					else:m((0,j))
			for r in list(c.values()):
				if r["who"]or r["watch"]is None:continue
				w=r["watch"]
				if w=="hidden":a=q
				elif w=="body":a=i!=r["base"]
				elif w=="name":a=e!=r["base"]
				else:continue
				if a:r["seen"]=True
				elif r["seen"]:m(r["key"])
				elif w=="hidden"and now>r["confirm"]:m(r["key"])
			if h["stats"]:
				if d[0]and d[1]and d[2]:b1(d,now)
			elif b["stats"]is not None or f["str"]or f["dex"]or f["int"]:
				b["stats"]=None
				for s in f:del f[s][:]
				ag()
		def b3(now):
			if not c:return
			e={};g={}
			for r in list(c.values()):
				a=r["who"]
				if not a:continue
				if a not in e:e[a]=API.FindMobile(a)
				d=e[a]
				if d is None:
					if not r["away"]:r["away"]=now;b["ver"]+=1
					if r["watch"]and not r["seen"]and now>r["confirm"]:m(r["key"])
					continue
				if r["away"]:r["away"]=0.;b["ver"]+=1
				try:
					f=g.get(a)
					if f is None:f=g[a]=bool(d.IsDead)
					if f:m(r["key"]);continue
					w=r["watch"]
					if w=="paralyzed":h=bool(d.IsParalyzed)
					elif w=="poisoned":h=bool(d.IsPoisoned)
					else:continue
				except Exception:continue
				if h:
					if not r["seen"]:r["seen"]=True
				elif r["seen"]:m(r["key"])
				elif now>r["confirm"]:m(r["key"])
		def b4(now):
			f=b["rd"]
			if f is None:b["rd"]=aa();return
			g=f.new()
			if not g:return
			h=b["name"];i,k=b["prev_name"]
			for d in g:
				c=aq(d,aw)
				if c.startswith(bS):continue
				a=d.name or "";e=bool(h)and a==h or(i and a==i and 0<=now-k<=5.)
				if e:
					j=Kit.SPELL_WORDS.get(c.strip())
					if j is not None:bY(j[0],min(now,d.at or now),now);continue
				if a and not e and a!="System":b6(c,a);continue
				b5(c,now,not e)
		def b5(low,now,system):
			d=low.strip(" *")
			for t,e in bM:
				if d.startswith(t):
					r=z(0,"poison","debuff",now);r["srcs"].add("line")
					if e!=r["level"]:r["level"]=e;b["ver"]+=1
					return
			if not system:return
			for t in bI:
				if low.startswith(t):
					for f,a in bK:
						if low.startswith(f):
							r=c.get((0,n(a)))
							if r is None:r=z(0,n(a),"buff",now)
							r["srcs"].add("cast")
					p=b["pend"]
					if p is not None and p["sid"]in("reactivearmor","magicreflection")and t=="this spell is already in effect"and(0,p["sid"])not in c:z(0,p["sid"],"buff",now)["srcs"].add("cast")
					b_(now,t=="your concentration is disturbed");return
			for t,a in bJ:
				if low.startswith(t):m((0,n(a)));return
			if low.startswith("you cannot move!"):z(0,"paralyzed","debuff",now)["srcs"].add("line")
			elif low.startswith(bL):m((0,"paralyzed"))
			elif d.startswith(bO):m((0,"poison"))
		def b6(low,name):
			for r in c.values():
				if r["who"]and r["sid"]=="poison":break
			else:return
			for t,a in bN:
				if t in low:
					d=name.lower()
					for r in c.values():
						if r["who"]and r["sid"]=="poison"and r["name"]and r["level"]!=a and(r["name"].lower()==d or r["name"].lower()in low):r["level"]=a;b["ver"]+=1
					return
		def bn(kind,c):
			if not b["active"]:return
			for a in c:
				try:d=(kind,str(a.Title or ""),int(a.Graphic or 0),int(a.Timer or 0))
				except Exception:continue
				if len(b["events"])<60:b["events"].append(d);HOST.poked=True
				return
		def b7():aY(b,"hooked",("OnBuffAdded",lambda*a:bn("add",a)),("OnBuffRemoved",lambda*a:bn("remove",a)))
		def b8():
			if not b["ct_looked"]:
				b["ct_looked"]=True
				try:t=X("ClassicUO.Time");m=aM(t,"Ticks")if t is not None else None;b["ct"]=m[0]if m else None
				except Exception:b["ct"]=None
			a=b["ct"]
			if a is None:return
			try:return int(a())
			except Exception:return
		def bo(title,graphic,a,now):
			b=n(title)
			if not b:return
			e="debuff"if b in bQ else "buff";r=z(0,b,e,now)
			if "icon"not in r["srcs"]:r["start"]=now
			r["srcs"].add("icon");r["label"]=title
			if graphic:r["icon"]=graphic
			c=None
			if 0<a<0xFFFFFFFF:
				d=b8()
				if d is not None and a>d:c=now+(a-d)/1000.
			if c is not None:r["end"],r["end_src"],r["most"]=c,"icon",None
		def b9(now):
			f,b["events"]=b["events"],[]
			if not h["icons"]:return
			for g,a,i,j in f:
				b["icons_seen"]=True
				if g=="add":bo(a,i,j,now)
				else:aO((0,n(a)),"icon")
			if now>=b["next_icons"]:
				b["next_icons"]=now+a1
				if not b["icons_seen"]and b["next_icons"]-a1>b["started"]+1.:return
				e=set()
				for d in API.ActiveBuffs()or[]:
					a=str(d.Title or "")
					if not a:continue
					e.add(n(a));b["icons_seen"]=True;r=c.get((0,n(a)))
					if r is None or "icon"not in r["srcs"]:bo(a,int(d.Graphic or 0),int(d.Timer or 0),now)
				for k in[p for p,s in c.items()if not p[0]and "icon"in s["srcs"]and p[1]not in e]:aO(k,"icon")
		def ca(now):
			if not c:return
			for r in list(c.values()):
				b,a=r["key"],r["srcs"];d=r["end"]
				if r["who"]and r["away"]and now-r["away"]>60. and(d is None or now>d):m(b);continue
				if "icon"in a or "stat"in a or "flag"in a:continue
				if r["watch"]and r["seen"]:continue
				if "line"in a and "cast"not in a:
					if now-r["start"]>60.:m(b)
					continue
				if d is None:
					if not r["watch"]and now-r["start"]>3600.:m(b)
					continue
				if now>max(d,r["most"]or 0)+1.:m(b)
		def cb(now):
			a=h["warn"]
			if not a or not h["me"]:return
			for r in c.values():
				if r["who"]or r["kind"]!="buff"or r["end"]is None:continue
				d=r["end"]-now;e=r["key"]
				if 0<d<=a and b["warned"].get(e)!=r["end"]:b["warned"][e]=r["end"];ao(a7,"%s runs out in %d s"%(K.get(r["sid"],r.get("label")or r["sid"]),int(d+.5)),"info",who=r["sid"])
		def aR():return a8,2*F+30+B+Kit.pitch(aW)+12
		def ah():
			a=o.zone_slot(*aR());e=2*F+30+B+12;w=a[0]if a else a8;f=[];c=Kit.pitch(aW);n=o.rows(c,e,h["rows"])if a else h["rows"];g,p,m=o.begin(w,a[1]if a else e+n*c)
			if not b["minimized"]:
				M=F;i=w-2*M;o.frame(g);d=M+30+B;J(g,M,d,i,(a[1]-M-d)if a else n*c+12);m["empty"]=l(g,"",M+12,d+10,k)
				for j in range(n):f.append(cc(g,j,M,d+6+j*c,i,c))
			o.end(g,{"slots":f,"nrows":n});b["redraw"]=True;by(time.time())
		o=Kit.Window(W,Q,b,u,ah,bB,bC,default=(60,260),mini=(aV,bE),icon=bD,lock=True,clear={"slots":[]})
		def bp(g,x,y,px):a=G.CreateGumpPic(av,x,y);a.SetPos(x,y);a.SetWidth(px);a.SetHeight(px);a.SetAcceptMouseInput(False);g.Add(a);return a
		def bq(s,icon,px):s["icon_g"]=icon;s["pic"].Graphic=icon;s["pic"].SetWidth(px);s["pic"].SetHeight(px)
		def cc(g,i,sx,a,IW,rh):s={"row":None,"prev":(None,0.),"vis":True,"icon_g":None,"tip":None,"tx":None,"fw":-1,"col":None,"x":sx,"y":a,"iw":IW};s["pic"]=bp(g,sx+6,a+2,a2);s["name"]=l(g,"",sx+34,a+1,C);s["time"]=l(g,"",sx+IW-50,a+1,k);b=IW-34-10;s["bw"]=b;s["bg"]=P(g,sx+34,a+rh-9,b,5,.9,"#202020");s["fill"]=P(g,sx+34,a+rh-9,b,5,1.,"#2f9a3c");s["hit"]=D(g,sx,a,IW,rh-2,br(lambda:u["slots"],i),"");aj(s,False);return s
		def br(get,i):
			def a(*e):
				a=get()
				if i>=len(a):return
				c=a[i];r=c["row"];b,d=c["prev"]
				if 0<=time.time()-d<=.15:r=b
				if r is None:return
				if r[0]and ad():aH(("follow",r[0]))();return
				aH(("clear",r))()
			return a
		def aj(s,on):
			if s["vis"]==on:return
			s["vis"]=on
			for k in("pic","name","time","bg","fill","hit"):
				if s.get(k)is not None:s[k].IsVisible=on
		def cd():
			a=[]
			for r in c.values():
				if r["who"]:
					if not h["others"]:continue
				elif r["kind"]=="buff":
					if not h["me"]:continue
				elif not h["debuff"]:continue
				a.append(r)
			a.sort(key=ce);return a
		def ce(r):a=r["end"];return(1 if r["who"]else 0,a9.get(r["kind"],2),a if a is not None else 1e18,r["start"])
		def bs(s):
			s=int(s+.999)
			if s<60:return "%ds"%s
			if s<3600:return "%d:%02d"%(s//60,s%60)
			return "%dh %02d"%(s//3600,(s%3600)//60)
		def aS(r,now):
			a=r["end"]
			if a is None:
				if r["sid"]in("reactivearmor","magicreflection")and not r["who"]:return "on",None,False
				return "+"+bs(max(0.,now-r["start"])),None,False
			b=a-now
			if b>0:c=max(.1,a-r["start"]);return bs(b),max(0.,min(1.,b/c)),False
			if r["most"]and now<r["most"]:return "soon",None,True
			return "due"if("stat"in r["srcs"]or "icon"in r["srcs"])else "0s",0.,True
		def bt(r):
			if r["who"]:return("%s on %s, cast by you. Click: clear this row. Alt+click: auto-follow (again to stop)"%(K.get(r["sid"],r["sid"]),E(r["name"],r["who"])if r["name"]else "them"))
			if "stat"in r["srcs"]and r["end"]is None:return "From a stat step; ends when it steps back. Click: clear this row."
			if r["end"]is None and r["sid"]in("reactivearmor","magicreflection"):return "Up until used up (the shard doesn't say when). Click: clear this row."
			return "Click: clear this row"
		al=("player","target");bu={"player":W,"target":W+".target"}
		def ar():return b.get("row_mode",False)
		def cf(now):
			if 0<=b.get("form_at",0.)-now<=bd:return
			b["form_at"]=now+bd;g=V("player");c=g is not None
			if c!=ar():bv(c)
			elif c:
				for d in al:
					a=v[d];f=V(d);e=a["w"]
					if f is not None:
						r=ac(f)
						if r is None:continue
						e=r[2]
					if a["g"]is None or e!=a["w"]:ax(d,e,max(0,a["lines"]))
		def bv(row):
			b["row_mode"]=row
			if row:
				aQ(W);o.close()
				for a in al:c=V(a);r=ac(c)if c is not None else None;ax(a,r[2]if r is not None else 200,0)
				for a in al:aK(bu[a],a,1,lambda s=a:v[s]["g"])
			else:bw();ah();o.dock(fit=True,min=aR)
			b["redraw"]=True
		def bw():
			for b in al:aL(bu[b]);a=v[b];g,a["g"]=a["g"],None;a["cells"],a["lines"],a["w"]=[],-1,0;L(g)
		def ax(side,fw,lines):
			c=v[side];a,c["g"]=c["g"],None;fw=max(N+2*R,int(fw));b=max(1,(fw-2*R)//N);h=max(1,lines)*aI+2*R;x,y=0,0
			if q(a):x,y=a.GetX(),a.GetY()
			g=G.CreateGump(True,False);J(g,0,0,fw,h,alpha=.6);d=[];n=min(bc,b*max(1,lines));e=R+(fw-2*R-b*N)//2
			for i in range(n):f,j=divmod(i,b);d.append(cg(g,side,i,e+j*N,R+f*aI))
			ak(g,x,y,fw,h);G.AddGump(g);g.IsVisible=lines>0;c.update({"g":g,"cells":d,"per":b,"lines":lines,"w":fw});L(a)
		def cg(g,side,i,a,b):c={"row":None,"prev":(None,0.),"icon_g":None,"tip":None,"vis":True,"x":a,"y":b,"tw":None};c["pic"]=bp(g,a+(N-Z)//2,b,Z);c["time"]=l(g,"",a,b+Z+1,k);c["time"].SetAcceptMouseInput(False);c["hit"]=D(g,a,b,N,aI-2,br(lambda:v[side]["cells"],i),"");return c
		def bx(side,now,mine):
			a=v[side];mine=mine[:bc];f=a["per"];g=(len(mine)+f-1)//f if mine else 0
			if g!=a["lines"]:ax(side,a["w"]or 200,g)
			if a["g"]is None:return
			for i,c in enumerate(a["cells"]):
				r=mine[i]if i<len(mine)else None;h=r["key"]if r is not None else None
				if h!=c["row"]:c["prev"]=(c["row"],now);c["row"]=h
				if r is None:aj(c,False);continue
				aj(c,True);k=r["icon"]
				if k!=c["icon_g"]:bq(c,k,Z)
				b,n,m=aS(r,now)
				if r["end"]is None:b=""
				d=ab(b)if b else 0
				if d!=c["tw"]:c["tw"]=d;am(c["time"],c["x"]+max(0,(N-d)//2),c["y"]+Z+1)
				A(c["time"],b,j if(m or r["kind"]=="debuff")else C);l=bi(r)
				if l!=c.get("tipk"):
					c["tipk"]=l;e="%s. %s"%(aP(r),bt(r))
					if e!=c["tip"]:c["tip"]=e;c["hit"].SetTooltip(e)
		def by(now):
			d=ar()
			if not d and(u["g"]is None or(b["minimized"]and b["docked"])):return
			if not b["redraw"]and b.get("drawn_at",0.)+.25>now>=b.get("drawn_at",0.)and b.get("drawn_ver")==b["ver"]:return
			b["redraw"]=False;b["drawn_at"],b["drawn_ver"]=now,b["ver"];a=cd()
			if d:
				e=az["fn"]()if az["fn"]is not None and V("target")is not None else 0;j=[p for p in a if not p["who"]];l=[w for w in a if e and w["who"]==e]
				if v["player"]["g"]is not None:bx("player",now,j)
				if v["target"]["g"]is not None:bx("target",now,l)
				return
			f=u["c"]
			if b["minimized"]:
				g=f.get("status")
				if g is not None:
					if a:
						t=aS(a[0],now)[0];c="%s: %s %s"%(Q,aP(a[0]),t)
						if len(a)>1:c+="  (+%d)"%(len(a)-1)
						c=M(c,aV-90)
					else:c="%s: no timers"%Q
					A(g,c,k)
				return
			m=u["slots"];A(f["empty"],""if a else "No timers yet; your buffs and casts show here.",k)
			for i,s in enumerate(m):
				r=a[i]if i<len(a)else None;h=r["key"]if r is not None else None
				if h!=s["row"]:s["prev"]=(s["row"],now);s["row"]=h
				if r is None:aj(s,False);continue
				aj(s,True);ch(s,r,now)
		def ch(s,r,now):
			l=r["icon"]
			if l!=s["icon_g"]:bq(s,l,a2)
			if r["who"]:f,a=(k if r["away"]else O),"other"
			elif r["kind"]=="debuff":f,a=j,"debuff"
			else:f,a=C,"buff"
			c,m,n=aS(r,now)
			if r["who"]and r["away"]:c=c+" (away)"
			q=ab(c);d=s["x"]+s["iw"]-8-q
			if d!=s["tx"]:s["tx"]=d;am(s["time"],d,s["y"]+1)
			A(s["time"],c,j if n else k);g=bi(r);o=d-(s["x"]+34)-6;p=(g,o)
			if p!=s.get("namek"):t=aP(r);s["namek"],s["name_txt"]=p,M(t,max(20,o))
			A(s["name"],s["name_txt"],f)
			if m is None:b,a=s["bw"],"dim"
			else:
				b=int(round(s["bw"]*m))
				if n:a="dim"
			e=s["fill"]
			if b!=s["fw"]:
				s["fw"]=b
				if b<=0:e.IsVisible=False
				else:au(e,b);e.IsVisible=True
			if a!=s["col"]:s["col"]=a;h=bR[a];e.SetBaseColor(h[0],h[1],h[2],255)
			if g!=s.get("tipk"):
				s["tipk"]=g;i=bt(r)
				if i!=s["tip"]:s["tip"]=i;s["hit"].SetTooltip(i)
		def ci(key):
			r=c.get(key)
			if r is None:return
			if "stat"in r["srcs"]:
				for a in("str","dex","int"):
					for e in f[a]:
						b=n(aF[(a,1 if e["d"]>0 else-1)])
						if b==key[1]or(key[1]in("bless","curse")and(e["d"]>0)==(key[1]=="bless")):e["hide"]=True
			m(key)
			if "stat"in r["srcs"]:ag()
		bz={"follow":lambda serial:Y(serial,Q),"clear":ci}
		def cj(w):return(("WINDOW  (what it lists)",(("check","me","Show the buffs on you","Bless, Strength, Protection, Reactive Armor, Magic Reflection, Night Sight and more"),("check","debuff","Show what is done to you (paralyze, poison, curses)","Paralyzed, Poison (with its level), Curse, Clumsy, Feeblemind and Weaken on you"),("check","others","Show your spells on others","What you cast on someone else. Alt+click such a row: auto-follow (again to stop)"),("num","rows","Rows shown:","Rows the window has room for",None,aX,aZ,{"clamp":False})),{"sh":140}),("TIMER SOURCES  (your casts always count)",(("check","stats","Watch your stats for Bless, Curse and their kin","A Str, Dex or Int step of %d or more is a spell on you (all three: Bless / Curse); potions show too"%a3),("check","icons","Use the shard's buff icons when it sends them","Exact names and times when the shard sends icons (a classic shard sends none)")),{"sh":90}),("TAZUO'S COOLDOWN BARS",(("check","bars","Also show Polymorph as a TazUO cooldown bar","Same time as its row here; goes when the timer ends or this is unticked"),),{"sh":64}),("ALERTS  (sound: Settings > Alerts)",(("num","warn","Warn before a buff on you runs out:","One alert this many seconds before it ends (0-%d, 0 = never)"%aB,"s",0,aB,{"clamp":False}),),{"sh":64}))
		def ck(a,new):
			b["redraw"]=True
			if new["icons"]and not a["icons"]:b["next_icons"]=0.
			if new["rows"]!=a["rows"]:b["rebuild"]=True
			if new["warn"]!=a["warn"]:b["warned"]={}
			if new["bars"]!=a["bars"]:
				d=time.time()
				for r in list(c.values()):(aN if new["bars"]else S)(r,d)
		ay=Kit.Page(h,cj,bg,ck,{"ldy":4,"lgap":12,"fw":40})
		def bA(serial=None):
			f=time.time();g=b["me"];d=[]
			for r in c.values():
				e=r["who"]or g
				if serial is not None and e!=serial:continue
				a=r["end"];d.append({"spell":K.get(r["sid"],r.get("label")or r["sid"]),"serial":e,"you":not r["who"],"kind":r["kind"],"end":a,"left":(a-f)if a is not None else None,"icon":r["icon"],"level":r["level"],"delta":r["delta"]})
			return d
		bf()
		def cl():
			a=time.time();ba();b.update({"active":True,"redraw":True,"started":a,"minimized":o.start_min()})
			for r in c.values():S(r,a)
			c.clear()
			for d in f:del f[d][:]
			bf();bV(a);ag();b7();ae(a7,"Buff about to run out",490);b["row_mode"],b["form_at"]=False,0.
			if V("player")is not None:bv(True)
			else:ah();o.dock(fit=True,min=aR)
			HOST.services["spelltimers.list"]=bA;bb.service("look.hud.timers",lambda:aH.add("redraw"))
		def cm():
			a=time.time();cf(a)
			if u["g"]is None and not ar():return
			if u["g"]is not None and aC(u):return
			while b["queue"]:
				c=b["queue"].pop(0);f=c[0]if isinstance(c,tuple)else c
				if c=="redraw":
					if not ar():ah()
					else:
						for g in al:
							d=v[g]
							if d["g"]is not None:ax(g,d["w"]or 200,max(0,d["lines"]))
						b["redraw"]=True;e["dirty"]=True
				elif o.action(c):pass
				elif f in bz:bz[f](c[1])
			if b["rebuild"]:
				b["rebuild"]=False
				if not ar()and not b["minimized"]and h["rows"]!=u["nrows"]:ah()
			b9(a)
			if not 0<=b["next_sample"]-a<=a_:b["next_sample"]=a+a_;b2(a)
			b4(a);bZ(a)
			if cn()and not 0<=b["next_others"]-a<=a0:b["next_others"]=a+a0;b3(a)
			ca(a);cb(a);by(a)
		def cn():
			for k in c:
				if k[0]:return True
			return False
		def co():
			b["shutting"]=True;b["active"]=False;aQ(W)
			if HOST.services.get("spelltimers.list")is bA:HOST.services.pop("spelltimers.list",None)
			a=time.time()
			for r in c.values():S(r,a)
			bw();o.close();bg();bU();bb.close()
		return{"start":cl,"tick":cm,"stop":co,"client_tick":True,"config_height":ay.height,"build_config":ay.build,"poll_config":ay.poll,"config_closed":ay.closed}
	def bf():
		aw="swing";M="Swing Bar"
		try:from System import DateTime
		except Exception:DateTime=None
		bt=[(0,4,-10,"Starving"),(5,9,-5,"Hungry"),(10,14,0,"Fed"),(15,19,0,"Full"),(20,20,0,"Stuffed"),];a_=300;a0=20;bu=[("lich lord",90),("lich",70),("dragon",90),("daemon",90),("troll",60),("ogre lord",85),("ogre",65),("orc captain",80),("orc",55),("ettin",55),("skeleton",50),("zombie",35),("rat",25),("headless",30),("mongbat",10),];ax=60;ac,ag=0,120;W="CTRL+SHIFT+T";ay="CTRL+SHIFT+R";az="CTRL+SHIFT+UP";aA="CTRL+SHIFT+DOWN";a1="CTRL+SHIFT+RIGHT";a2="CTRL+SHIFT+LEFT";bv,bw=300,300;bx,by=53,"#b8913a";bz,bA=63,"#3fa34d";bB,bC=946,"#6b6b6b";aC=10;a3=250;a4="SwingTimer_history";bD=("you have been disarmed","your weapon has been disarmed");bE=("you have been knocked off","you fall off of your mount","you fall off your mount");bF=("system","");a6="swing.notice";a8=30.;a9,aD,aj,aE=68,53,33,946;X=C;m,Q,r,WR="Swordsmanship","Fencing","Mace Fighting","Wrestling";AR="Archery";_W=[("Broadsword",45,m,(3934,3935)),("Cutlass",45,m,(5185,5184)),("Katana",58,m,(5119,5118)),("Longsword",35,m,(3937,3936)),("Scimitar",30,m,(5046,5045)),("Viking Sword",30,m,(5049,5050)),("Thin Longsword",35,m,(5048,5047)),("Butcher Knife",40,m,(5110,5111)),("Cleaver",40,m,(3779,3778)),("Skinning Knife",40,m,(3780,3781)),("Axe",37,m,(3913,3914)),("Battle Axe",31,m,(3911,3912)),("Double Axe",37,m,(3915,3916)),("Executioner's Axe",37,m,(3909,3910)),("Large Battle Axe",29,m,(5115,5114)),("Two Handed Axe",31,m,(5187,5186)),("Pickaxe",35,m,(3718,3717)),("Hatchet",41,m,(3907,3908)),("Bardiche",26,m,(3917,3918)),("Halberd",25,m,(5182,5183)),("Dagger",55,Q,(3922,3921)),("Kryss",53,Q,(5121,5120)),("Short Spear",50,Q,(5123,5122)),("Spear",46,Q,(3938,3939)),("War Fork",45,Q,(5125,5124)),("Pitchfork",45,Q,(3719,3720)),("Club",40,r,(5044,5043)),("Hammer Pick",30,r,(5181,5180)),("Mace",30,r,(3932,3933)),("Maul",30,r,(5179,5178)),("War Axe",40,r,(5040,5039)),("War Hammer",31,r,(5177,5176)),("War Mace",26,r,(5127,5126)),("Quarter Staff",48,r,(3721,3722)),("Gnarled Staff",33,r,(5112,5113)),("Black Staff",35,r,(3568,3569)),("Shepherd's Crook",30,r,(3713,3714)),("Bow",20,AR,(5042,5041)),("Crossbow",18,AR,(3920,3919)),("Heavy Crossbow",10,AR,(5117,5116)),];aF={}
		for bG,bH,bI,bJ in _W:
			for _g in bJ:aF[_g]=(bG,bH,bI)
		bK=("Fists",30,WR);bL={562,563,564,567,568,569,570,571,572};bM=[("supremely accurate",10),("exceedingly accurate",8),("eminently accurate",6),("surpassingly accurate",4),("accurate",2)]
		def al(a,b):
			v=(a+100)*b
			if v<=0:v=1
			return 15000./v*1000.
		def aG(hunger):
			h=int(round(max(0,min(20,hunger))))
			for a,b,c,d in bt:
				if a<=h<=b:return c,d
			return 0,"?"
		def bN(b,c,d,hunger):e,f=aG(hunger);a=(max(b,-49.9)+50.)/((max(c,-49.9)+50.)*2.);a*=1.+d/100.;return max(0.,min(1.,a*(1.+e/100.)))
		def o():return time.time()*1000.
		def aI():
			for b in("OneHanded","TwoHanded"):
				a=API.FindLayer(b)
				if a and int(a.Graphic)in aF:c,d,e=aF[int(a.Graphic)];return c,d,e,bO(a)
			return bK+(0,)
		aq={}
		def bO(item):
			a=int(item.Serial);c=aq.get(a)if a else None
			if c is not None and time.time()<c[1]:return c[0]
			d=(item.Name or "").lower()
			if "accurate"not in d:d=(API.ItemNameAndProps(a,False)or "").lower()
			b=0
			for e,p in bM:
				if e in d:b=p;break
			if a:
				if len(aq)>50:aq.clear()
				aq[a]=(b,time.time()+(1e9 if b else 2.))
			return b
		def aJ(mob,a,name=None):
			if a is not None:return a
			if mob is None:return B["enemy_default"]
			name=(mob.Name or ""if name is None else name).lower()
			for b,c in bu:
				if b in name:return c
			return 100 if mob.IsHuman else B["enemy_default"]
		def F(key,default):
			try:return float(T(key,str(default)))
			except Exception:return float(default)
		def u(key,value):U(key,str(value))
		def bP(v):
			try:return int(max(ac,min(ag,int(round(float(v))))))
			except Exception:return ax
		B={"enemy_default":ax};cv=dict(B);st={"minimized":False,"shutting":False,"docked":False,"queue":[]};d={"g":None,"c":{},"store":({},{}),"bar_w":109,"x1":0,"row1":0,"food_w":[0]*21,"fill_w":-1,"fill_state":None,"shown":{},"tips":{},"active":False,"closing":False};ba,cw,at=ai(st,M)
		def bQ():B["enemy_default"]=bP(F("swingtimer_enemy_default",ax))
		def bR():u("swingtimer_enemy_default",B["enemy_default"])
		bQ()
		class State:last_swing=None;cycle_ms=None;gaps=[];gaps_weapon=None;history={};slow=[];dirty=False;paused_at=None;target_serial=0;enemy_override=None;hunger=a0;hunger_clock=o();seen_sounds=set();sounds=[];keys=[];notice=None
		c=State()
		def bb():
			if not c.gaps:return
			return sum(c.gaps)/float(len(c.gaps))
		def bc(name):return name.replace("|","/").replace(";","/")
		def bd(weapon):
			a=(weapon[0],int(weapon[1]))
			if c.gaps_weapon==a:return False
			b=(bc(a[0]),a[1])
			if a not in c.history and b in c.history:c.history[a]=c.history.pop(b)
			c.gaps_weapon=a;c.gaps=c.history.setdefault(a,[]);c.slow=[];return True
		n={"saved_at":0.,"save":False,"import":False}
		def be(text,c):
			b={}
			for d in text.split(c):
				p=d.strip().split("|")
				if len(p)!=3 or not p[0]:continue
				try:e=int(p[1]);a=[float(h)for h in p[2].split(",")if h.strip()]
				except Exception:continue
				a=[t for t in a if t>=a3][-aC:]
				if a:b[(p[0],e)]=a
			return b
		def bS():
			c.history={};c.gaps,c.gaps_weapon,c.dirty,c.slow=[],None,False,[];a=T(a4)
			if a:c.history=be(a,";")
			n["import"]=not c.history
		def bT():
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
			h=be(g,"\n");b=0
			for e,i in h.items():
				if not c.history.get(e):c.history[e]=i;b+=1
			if not b:return
			c.gaps_weapon=None;c.dirty=True;aM();at("brought over learned swings of %s from the old data file."%S(b,"weapon"),I)
		def aM():n["save"]=False;a=["%s|%d|%s"%(bc(h),p,",".join("%.0f"%t for t in b))for(h,p),b in sorted(c.history.items())if b];U(a4,";".join(a));c.dirty=False;n["saved_at"]=o()
		def bU(gap,formula):
			a=bb()
			if gap<a3 or gap>(a or formula)+3000:c.slow=[];return
			if a is not None and gap>a*1.15:
				c.slow.append(gap)
				if len(c.slow)<3:return
				c.gaps[:]=c.slow;c.slow=[];bf("Slow: low stamina",aD)
			else:c.slow=[];c.gaps.append(gap)
			if len(c.gaps)>aC:del c.gaps[:-aC]
			c.dirty=True
		def aN(a):
			if c.paused_at is not None:
				if c.last_swing is not None:c.last_swing+=max(0.,a-c.paused_at)
				c.paused_at=a
			b=aI();d=al(int(API.Player.Stamina),b[1]);e=bd(b)
			if c.last_swing is not None and not e:bU(a-c.last_swing,d)
			c.last_swing=a;c.cycle_ms=bb()or d
		def bV(a):
			try:return max(0.,(DateTime.Now-a.Time).TotalMilliseconds)
			except Exception:return 0.
		def bW(a):
			b=int(a.Index)
			if b not in bL:return
			return(b,int(a.X),int(a.Y),str(a.Time),o()-bV(a))
		def bX(snd,p):
			e,a,b,f,g=snd
			if a!=int(p.X)or b!=int(p.Y):return
			d=(e,a,b,f)
			if d in c.seen_sounds:return
			c.seen_sounds.add(d)
			if len(c.seen_sounds)>200:c.seen_sounds.clear()
			aN(g)
		def bY(*e):
			if not d.get("active"):return
			for g in e:
				try:a=bW(g)
				except Exception:continue
				if a is not None and len(c.sounds)<50:
					c.sounds.append(a)
					if not f.get("fast"):
						b=f.get("xy")
						if b is None or(a[1],a[2])==b:HOST.poke("hud.swing",False)
				return
		bZ=[False]
		def bf(text,hue):c.notice=(text,hue,o()+4000.)
		R={"rd":None,"clock":0.,"own":(M.lower(),)}
		def b_():
			a=set([M.lower()])
			for t in[APP_NAME]+[b.title for b in HOST.slots]:
				t=str(t or "").strip().lower()
				if t:a.add(t)
			return tuple(a)
		def b0():
			d=R["own"]
			for a in R["rd"].new(time.time()-Journal.read_at>=.5):
				b=a.low
				if b.startswith(d)or str(a.name or "").lower()not in bF:continue
				for e,c in((bD,("Disarmed!","You were disarmed")),(bE,("Dismounted!","You were dismounted"))):
					if any(g in b for g in e):bf(c[0],aj);ao(a6,c[1]);break
		b1=[("simply too full to eat any more",20,20),("but you are stuffed",20,20),("but are still extremely hungry",0,4),("begin to feel more satiated",5,9),("you feel much less hungry",10,14),("feel quite full after consuming",15,19),];bg={"rd":None}
		def b2():
			e=bg["rd"]
			if e is None:bg["rd"]=aa();a=Journal.recent(a8)
			else:a=e.new()
			if not a:return
			try:f=float(DateTime.Now.Ticks)
			except Exception:f=time.time()*1e7
			for b in a:
				if b.ticks>1e12 and(f-b.ticks)/1e7>a8:continue
				h=b.low
				for i,g,d in b1:
					if i in h:aO(max(g,min(d,c.hunger+3 if g!=d else d)));break
		def aO(value):aX[0]=True;c.hunger=float(max(0,min(20,value)));c.hunger_clock=o();u("swingtimer_hunger",c.hunger)
		def b3():
			b=o()-c.hunger_clock;a=a_*1000.
			if b>=a:d=int(b//a);c.hunger=max(0.,c.hunger-d);c.hunger_clock+=d*a;u("swingtimer_hunger",c.hunger)
		aQ=" Alt+click: auto-follow (again to stop)"
		def H(what,value):
			if len(c.keys)<50:c.keys.append((what,value));HOST.poke()
		def b4(serial):
			if serial:c.target_serial=int(serial);c.enemy_override=None
		def b5():
			while c.keys:
				a,v=c.keys.pop(0)
				if a=="target":at("target the mobile you are fighting.");af(10,b4)
				elif a=="resync":aN(v)
				elif a=="hunger":aO(round(c.hunger)+v)
				elif a=="enemy":b=bi();d=aJ(b,c.enemy_override);c.enemy_override=max(ac,min(ag,d+v))
				elif a=="follow":
					b=f.get("mob")
					if b is not None:Y(int(b.Serial),M)
					else:at("no target to follow.")
		b6=((W,lambda:H("target",None),"pick the mobile you fight"),(ay,lambda:H("resync",o()),"restart the bar (I just swung)"),(az,lambda:H("hunger",1),"satiety estimate +1"),(aA,lambda:H("hunger",-1),"satiety estimate -1"),(a1,lambda:H("enemy",5),"enemy skill +5"),(a2,lambda:H("enemy",-5),"enemy skill -5"))
		def b7(fn):
			def a(*a):
				if not HOST.typing():fn()
			return a
		def bh(on):
			for a,b,c in b6:
				if on:HOST.hotkey_on(a,M,b7(b),c)
				else:HOST.hotkey_off(a,M)
		def bi():
			for a in(c.target_serial,API.LastTargetSerial):
				if a:
					m=API.FindMobile(a)
					if m and not m.IsDead:return m
			N=API.Notoriety;return API.NearestMobile([N.Gray,N.Criminal,N.Enemy,N.Murderer],2)
		K=A;b8={(False,False):400.,(False,True):200.,(True,False):200.,(True,True):100.};b9,ca=50.,800.;aR="swingtimer_kite";cb={"close":"#E8C25A","turn":"#3CD070","far":"#E04040","idle":"#C8C8C8"};cc={"close":O,"turn":I,"far":j,"idle":k};i={"on":bool(int(F(aR,1)or 0)),"steps":{},"xy":None,"at":0.,"stat0":None,"swing0":None,"px":None,"state":None,"tiles":None};s,Z=16,34;bj=3;V=max(0.,min(100.,F("swingtimer_bg_opacity",85)));aS={"f":None}
		def bk():return q(d["c"].get("gump"))
		def aU(hue,color,h):
			if N(Kit.LINE_BLUE)[0]>0:
				t=ar(d["c"]["gump"],Kit.LINE_BLUE,d["x1"],s,1,h,hue=hue)
				if t is not None:return t
			return P(d["c"]["gump"],d["x1"]+1,s+1,1,h,1.,color)
		def cd():d["row1"]=d["bar_w"]+5+max(z("15.0s"),a7());return d["row1"]+2*bj+16,58
		def bl(x=None,y=None):
			k=x is None
			if k:x=int(F("swingtimer_x",bv));y=int(F("swingtimer_y",bw))
			c=d["c"];o=c.get("gump");c.clear();m=N(Kit.LINE_RED)[0];g=N(Kit.LINE_BLUE)[1]or 8;d["bar_w"]=m or 109;w,h=cd();d["x1"]=f=8+bj
			if k:x,y=Kit.adapt(x,y,w,h)
			b=G.CreateGump(True,True);ak(b,x,y,w,h);c["gump"]=b;ah(b,w,h,corners=False);c["section"]=J(b,8,8,w-16,h-16);e["bg"][b]=[c["section"]];bp()
			if m>0:aB(b,Kit.LINE_RED,f,s)
			else:ar(b,aT,f,s,109,9,1.)
			c["fills"]={"fill":aU(bx,by,g),"ready":aU(bz,bA,g),"paused":aU(bB,bC,g)}
			for p in c["fills"].values():p.IsVisible=False
			c["kite"]={}
			for q,r in cb.items():c["kite"][q]=t=P(b,f,s-1,2,g+2,1.,r);t.IsVisible=False
			c["kite_lbl"]=l(b,"",f,s-2,X);c["kite_lbl"].SetAcceptMouseInput(False);i.update({"px":None,"state":None,"tiles":None});c["swing"]=l(b,"",f+d["bar_w"]+5,s-2,X);c["notice"]=n=l(b,"",f+4,s-2,aj);n.SetAcceptMouseInput(False);n.IsVisible=False;c["hit"]=l(b,"",f,Z,aE);c["food"]=l(b,"",f+d["row1"]-z("Food 20/20"),Z,X);d["food_w"]=[ab("Food %d/20"%v)for v in range(21)];j=d["row1"]//2;c["tip_bar"]=D(b,f-2,s-4,d["row1"]+4,18,bm,bn(None),movable=True);c["tip_hit"]=D(b,f-2,Z-2,j,18,bm,aV(None),movable=True);c["tip_food"]=D(b,f+j,Z-2,d["row1"]-j+2,18,lambda*a:None,bo(),movable=True);d["fill_w"],d["fill_state"],d["shown"],d["tips"]=-1,None,{},{};d["notice_shown"]=None;G.AddControlOnDisposed(b,ck(b));G.AddGump(b);aH(b,aW);L(o)
		cx=None
		def av(key,text):
			c=d["c"].get(key)
			if c is None or d["tips"].get(key)==text:return
			d["tips"][key]=text;c.SetTooltip(text)
		def bm(*a):
			if ad():H("follow",None)
		def bn(info):
			a="Time to your next swing. Green: ready; grey: paused (no war mode or target)."
			if info is not None:b,c,d,n=info;a+=" %s, speed %d, swing %.1f s (%s)."%(b,c,d/1000.,"learned from %s"%S(n,"swing")if n else "formula")
			return a+aQ
		def aV(info):
			if info is None:return "Chance to hit your target; set it with %s.%s"%(W,aQ)
			a,b,c,d,e,f=info;return("Chance to hit %s: your %s %.1f vs their assumed %d, accuracy +%d%%, satiety %+d%%; set the target with %s.%s"%(a[:20],b,c,d,e,f,W,aQ))
		def bo(label="",mod=0):return("Satiety estimate%s, %+d%% to hit: drops 1 every %d min, rises when you eat%s. Adjust: %s / %s."%((": "+label.lower())if label else "",mod,a_//60,""if aX[0]else " (none seen yet, so grey)",az,aA))
		def bp():d["c"]["section"].SetAlpha(V/100.*Kit.SECTION_ALPHA)
		def ce(i,state):
			a=int(d["bar_w"]*max(0,min(1000,i))/1000);c,e=d["fill_w"],d["fill_state"]
			if a==c and state==e:return
			d["fill_w"],d["fill_state"]=a,state;f=d["c"]["fills"];g=e if c>0 else None;b=state if a>0 else None
			if b is not None:au(f[b],a)
			if g!=b:
				for h,j in((g,False),(b,True)):
					if h is not None:f[h].IsVisible=j
		def cf(p,t):
			a=(int(p.X),int(p.Y));b,h=i["xy"],i["at"]
			if a==b:return
			i["xy"],i["at"]=a,t
			if b is None:return
			c=max(abs(a[0]-b[0]),abs(a[1]-b[1]));e=t-h
			if not(0<c<=4 and 0<e<=700.*c):return
			f=max(b9,min(ca,e/float(c)));g=bq(p);d=i["steps"].get(g);i["steps"][g]=f if d is None else d+(f-d)*.15
		def bq(p):return(bool(p.IsMounted),bool(p.IsRunning))
		def cg(p):a=bq(p);v=i["steps"].get(a);return v if v is not None else b8[a]
		def ch(a,step):return int(1+(a/2.)/max(1.,step))
		def ci(dist,a):
			if dist is None:return "idle"
			return "close"if dist<a else("turn"if dist==a else "far")
		def cj(p,mob,cycle,stat,k):
			a=d["c"].get("kite")
			if not a:return
			h=d["c"].get("kite_lbl")
			if not i["on"]or c.notice is not None:
				if i["state"]is not None:a[i["state"]].IsVisible=False;i["state"]=None;i["tiles"]=None;A(h,"")
				return
			e=float(cycle)
			if i["swing0"]!=c.last_swing or i["stat0"]is None:i["swing0"],i["stat0"]=c.last_swing,stat
			elif stat!=i["stat0"]:
				l=al(i["stat0"],k)
				if l>0:e=e*al(stat,k)/float(l)
			m=max(.02,min(.98,(e/2.)/max(1.,float(cycle))));f=d["x1"]+int(d["bar_w"]*m);g=ch(e,cg(p));j=None
			if mob is not None:
				try:j=int(mob.Distance)
				except Exception:j=None
			b=ci(j,g)
			if b!=i["state"]:
				if i["state"]is not None:a[i["state"]].IsVisible=False
				a[b].IsVisible=True;i["state"]=b;i["px"]=None;i["tiles"]=None
			if f!=i["px"]:i["px"]=f;a[b].SetPos(f,s-1);h.SetPos(f+4,s-2)
			if g!=i["tiles"]:i["tiles"]=g;A(h,str(g),cc[b])
		def ck(g):
			def a(*a):
				if d["closing"]or d["c"].get("gump")is not g:return
				aW();d["c"].clear();aP("swing")
			return a
		def aW():
			g=d["c"].get("gump")
			if q(g)and not a5(aw)and g.GetX()>TAB_X//2:u("swingtimer_x",g.GetX());u("swingtimer_y",g.GetY())
		aX=[False]
		def br():return "{:.0f}/20 {}".format(c.hunger,aG(c.hunger)[1])
		def aZ(a,b):return "%s / %s"%(a,b.rsplit("+",1)[1])
		cy={}
		def bs(w):a=((aZ(W,ay),"pick the target / restart the bar"),(aZ(az,aA),"satiety estimate +1 / -1"),(aZ(a1,a2),"enemy skill +5 / -5"));return(("WINDOW",(("gap",32),("check","kite","Show the kite marker on the bar","Turn-back point and tiles to kite out; colour: too close, turn now, too far",{"h":-32}),("slider","opacity","Background opacity:","How solid the window's black inside is (0-100)",0,100,{"lgap":12,"sdy":8,"sw":160})),{"sh":96,"ldy":4}),("HIT CHANCE",(("num","enemy","Enemy skill:","Skill assumed for an unknown monster; players count as GM (%d-%d)"%(ac,ag),None,ac,ag,{"lgap":8,"fw":44,"stay":True}),("slider","satiety","Satiety estimate:","How well fed you are, 0 (starving) to 20 (stuffed); low lowers the hit chance",0,20,{"dx":220,"lw":150,"sdy":8,"sw":120,"unit":br()})),{"sh":68,"ldy":4}),("HOTKEYS",[h for b,g in a for h in(("note",b,{"stay":True}),("note",g,{"dx":330}))],{"sh":100}))
		cl=Kit.Page(B,bs)
		def cm(g,x,y,w):aS["f"]=Kit.Form(g,x,y,w,{"kite":i["on"],"opacity":int(round(V)),"enemy":B["enemy_default"],"satiety":int(round(c.hunger))},bs(w))
		def cn():aS["f"]=None
		def co():
			nonlocal V;b=aS["f"]
			if b is None:return
			a,c=b.read(),b.vals;b.vals=a
			if a["opacity"]!=c["opacity"]:
				V=float(a["opacity"]);u("swingtimer_bg_opacity",V)
				if bk():bp()
			if a["enemy"]!=c["enemy"]:B["enemy_default"]=a["enemy"];bR();f["slow_clock"]=0.
			if a["satiety"]!=c["satiety"]:aO(a["satiety"])
			A(b.c["satiety_lbl"],br())
			if a["kite"]!=i["on"]:i["on"]=a["kite"];u(aR,1 if a["kite"]else 0)
		f={}
		def cp():d["closing"],d["active"]=False,True;n.update({"saved_at":o(),"save":False});bS();del c.sounds[:],c.keys[:];c.last_swing=c.cycle_ms=c.notice=None;R.update({"rd":aa(),"clock":0.,"own":b_()});ae(a6,"Disarmed or dismounted",946);c.hunger=max(0.,min(20.,F("swingtimer_hunger",a0)));c.hunger_clock=o();i["on"]=bool(int(F(aR,1)or 0));i["steps"].clear();i["xy"],i["stat0"],i["swing0"]=None,None,None;bl();ba.service("look.hud.swing",lambda:d.update({"redo":True}));aK(aw,"target",0,lambda:d["c"].get("gump"));bh(True);aY(bZ,0,("SoundPlayed",bY));f.update({"slow_clock":0.,"eat_clock":0.,"weapon":aI(),"mob":None,"my_skill":0.,"mob_skill":aJ(None,None),"mob_name":"","skill_of":None,"skill_clock":0.,"timer_clock":0.,"timer_mode":None,"fast":False,"react":None});at("on (%s picks the target, %s restarts the bar)."%(W,ay),I)
		def cq():
			if not bk():f["fast"]=False;return
			if d.pop("redo",False):y=d["c"]["gump"];bl(y.GetX(),y.GetY());e["dirty"]=True
			t=o();p=ap()
			if p is None:return
			while c.sounds:bX(c.sounds.pop(0),p)
			if c.keys:b5()
			if t-R["clock"]>=100:R["clock"]=t;b0()
			z=(c.target_serial,API.LastTargetSerial,bool(p.InWarMode))
			if z!=f["react"]:f["react"]=z;f["slow_clock"]=t-250
			if t-f["slow_clock"]>=250:
				f["slow_clock"]=t;f["xy"]=(int(p.X),int(p.Y));f["weapon"]=aI();M=c.gaps_weapon
				if bd(f["weapon"]):
					c.cycle_ms=None
					if M is not None and f["weapon"][2]==AR:c.last_swing=None;aN(t)
				if c.dirty and t-n["saved_at"]>=5000:n["save"]=True
				a=f["mob"]=bi();r=(a.Name or "")if a is not None else "";f["mob_skill"]=aJ(a,None,r);f["mob_name"]=(E(r,a.Serial)if r else "target")if a is not None else ""
				if f["weapon"][2]!=f.get("skill_of")or t-f.get("skill_clock",0.)>=1000:f["skill_of"],f["skill_clock"]=f["weapon"][2],t;f["my_skill"]=an(f["weapon"][2])
				b3()
				if t-f["eat_clock"]>=1000:f["eat_clock"]=t;b2()
			A,m,B,s=f["weapon"];C=int(p.Stamina);h=c.gaps;N=sum(h)/float(len(h))if h else None;q=N or al(C,m);a=f["mob"];i=bool(p.InWarMode)and a is not None
			if not i:
				if c.paused_at is None:c.paused_at=t
				D=c.paused_at
			else:
				if c.paused_at is not None:
					if c.last_swing is not None:c.last_swing+=t-c.paused_at
					c.paused_at=None
				D=t
			b=c.notice
			if b is not None and t>=b[2]:c.notice=b=None
			if c.last_swing is None:g,F,j=1000,0.,q
			else:j=c.cycle_ms or q;u=D-c.last_swing;F=j-u;g=1000 if u>=j else int(u/j*1000)
			ce(g,"paused"if not i else("ready"if g>=1000 else "fill"));cf(p,t);cj(p,a,j,C,m);f["fast"]=i and g<1000
			if b is not d["notice_shown"]:
				d["notice_shown"]=b;G=d["c"]["notice"]
				if b is not None:K(G,b[0],b[1])
				G.IsVisible=b is not None
			H=(i,g>=1000,a is None)
			if H!=f["timer_mode"]or t-f["timer_clock"]>=100:
				f["timer_mode"],f["timer_clock"]=H,t
				if not i:K(d["c"]["swing"],"Paused"if a is not None else "Ready",aE)
				elif g>=1000:K(d["c"]["swing"],"Ready",a9)
				else:K(d["c"]["swing"],"%.1fs"%(max(0.,F)/1000.),X)
			l=(A,m,"%.1f"%(q/1000.),len(h))
			if d["shown"].get("bar_tip")!=l:d["shown"]["bar_tip"]=l;av("tip_bar",bn((A,m,q,len(h))))
			I=d["shown"];v=f["my_skill"];w=c.enemy_override if c.enemy_override is not None else f["mob_skill"];l=(a is not None,f["mob_name"],w,v,B,s,c.hunger)
			if I.get("rows")!=l:
				I["rows"]=l;x=bN(v,w,s,c.hunger);J,O=aG(c.hunger)
				if a is not None:K(d["c"]["hit"],"Hit %d%%"%int(round(x*100)),a9 if x>=.6 else(aD if x>=.4 else aj));av("tip_hit",aV((f["mob_name"],B,v,w,s,J)))
				else:K(d["c"]["hit"],"Hit --%",aE);av("tip_hit",aV(None))
				L=max(0,min(20,int(round(c.hunger))))
				if K(d["c"]["food"],"Food %d/20"%L,k if not aX[0]else(aj if c.hunger<5 else(aD if c.hunger<10 else X))):am(d["c"]["food"],d["x1"]+d["row1"]-d["food_w"][L],Z)
				av("tip_food",bo(O,J))
		def cr():
			if n["import"]and not d["closing"]:
				bT()
				if not n["import"]:f["slow_clock"]=0.
			if n["save"]and c.dirty:aM()
			n["save"]=False
		def cs():return.025 if f.get("fast")else.1
		def ct():return bool(n["save"]or n["import"])
		def cu():
			d["closing"],d["active"]=True,False;bh(False);R["rd"]=None
			if c.dirty:aM()
			aW();aL(aw);u("swingtimer_bg_opacity",V);g=d["c"].get("gump");d["c"].clear();L(g);ba.close()
		return{"start":cp,"tick":cq,"stop":cu,"client_tick":True,"config_height":cl.height,"build_config":cm,"poll_config":co,"config_closed":cn,"thread_tick":cr,"thread_wanted":ct,"interval":cs}
	def bg():
		h="bandage";Q="Bandages";ax="BandageAgent_pos";W=3617;ay=15.;az=7.5;aA=.5;F,K=1.,60.;X,ab=0.,5.;aC=3.;r=1;aD=("you did not stay close enough to heal","you were unable to finish your work");bl=("that being is not damaged","you are too far away to do that","bandages can not be used on that","you cannot heal that","bandages cannot be used on that","that is too far away","that creature may only be healed")+aD;bm=("you finish applying the bandages","you apply the bandages, but they barely help","you apply the bandages, but they do not seem","you heal what little damage","you are able to resurrect","you are unable to resurrect","you have cured the target of all poisons");ac=50;aE,aF=0,99;bn,bo=400,300;aG=60.;aI=60.;aJ=.6;aM=10;ag,aj=0,999;aQ="bandage.low";aR="bandage.hp";aS="bandage.poison";aU="bandage.ready";aV=10;aW="BandageAgentStartPct";aX="BandageAgent_timing";aY="BandageAgent_extra";aZ="BandageAgent_other";a_="#E8C25A";R=62;s,bp=16,35;f=18;t=8;a0,a1,a2=120,118,104;bq=a0+B+a1+B+a2;d={"cure":True,"low":aM,"others":False,"other_pct":80,"party":True,"pets":True};bV=dict(d)
		def a3():b.update({"phase":"idle","shutting":False,"queue":[],"rebuild":False,"skills":(0.,0.,-1e9),"count":None,"count_at":0.,"low_armed":True,"hp_armed":True,"poison_armed":True,"target":None,"last":None,"pick":False,"begun":False,"by_buff":False,"buff":False,"lt":(0,0.)})
		b={"minimized":False,"shutting":False,"docked":False,"queue":[],"start_pct":ac,"band_time":ay,"other_time":az,"buffer":aA,"t0":0.,"deadline":0.,"rd":None};a3();c={"g":None,"c":{"fill":None,"fill_box":None,"label":None,"count":None},"store":({},{}),"bar_w":109,"fill_w":-1,"text":None,"count_text":None,"wide":False};a4,M,i=ai(b,Q);n={"f":None,"typed":None,"applied":None,"since":0.}
		def a6():bs();bt();bu()
		def br():a8();a9()
		def bs():
			try:b["start_pct"]=max(aE,min(aF,int(T(aW,str(ac)))))
			except Exception:b["start_pct"]=ac
		def a8():U(aW,str(b["start_pct"]))
		def bt():
			p=T(aX).split("|")
			try:
				if p[0]:b["band_time"]=max(F,min(K,float(p[0])))
				if len(p)>=2 and p[1]:b["buffer"]=max(X,min(ab,float(p[1])))
			except ValueError:b["band_time"],b["buffer"]=ay,aA
			try:
				v=T(aZ)
				if v:b["other_time"]=max(F,min(K,float(v)))
			except ValueError:b["other_time"]=az
		def a9():U(aX,"%.2f|%.2f"%(b["band_time"],b["buffer"]));U(aZ,"%.2f"%b["other_time"])
		def bu():v=dict(a.split("=",1)for a in T(aY).split(";")if "="in a);d["cure"]=v.get("cure","1")!="0";d["others"]=v.get("others","0")=="1";d["party"]=v.get("party")!="0";d["pets"]=v.get("pets")!="0";d["low"]=ba(v.get("low"),ag,aj,aM);d["other_pct"]=ba(v.get("opct"),1,99,80)
		def ba(text,lo,hi,default):
			try:return max(lo,min(hi,int(text)))
			except(TypeError,ValueError):return default
		def bv():U(aY,"cure=%d;low=%d;others=%d;opct=%d;party=%d;pets=%d"%(int(d["cure"]),d["low"],int(d["others"]),d["other_pct"],int(d["party"]),int(d["pets"])))
		def al():
			if not a5(h):Kit.save_pos(ax,c["g"])
		def bw():a=N(Kit.LINE_RED)[0];i=N(Kit.LINE_BLUE)[0];b=a if a>0 and i>0 else 109;j=(max(z("15.0s"),a7())+(90 if d["others"]else 0));c=z("x999");e=b+5+j;g=f+t+c+t+f+t+f;h=max(e,g)+6;return{"bar_w":b,"count_w":c,"row1":e,"row2":g,"sec_w":h,"W":h+16}
		def bb():
			b=bw();n=b["W"];z=N(Kit.LINE_RED)[0];A,B=N(Kit.LINE_BLUE);C=d["others"];x,y=Kit.load_pos(ax,(bn,bo),(n,R));m=c["g"]
			if q(m):x,y=m.GetX(),m.GetY()
			g=G.CreateGump(True,True);ak(g,x,y,n,R);ah(g,n,R,corners=False);e["bg"][g]=[J(g,8,8,b["sec_w"],R-16)];g.SetTooltip("%s: one press, one bandage (x = bandages left)"%Q);j=8+(b["sec_w"]-b["row1"])//2;i=c["c"];i["fill"]=i["fill_box"]=None;c["bar_w"]=b["bar_w"]
			if z>0 and A>0:aB(g,Kit.LINE_RED,j,s);i["fill"]=ar(g,Kit.LINE_BLUE,j,s,1,B);i["fill"].SetWidth(0)
			else:ar(g,aT,j,s,109,9,1.);i["fill_box"]=P(g,j+1,s+1,1,7,1.,"#3A63A8")
			E=j+b["bar_w"]+5;i["label"]=l(g,"Ready",E,s-2,k);D(g,j-2,s-4,b["row1"]+4,18,bA,"Bandage in progress and its patient. Alt+click: auto-follow (again to stop)",movable=True);o=8+(b["sec_w"]-b["row2"])//2;h=bp;p=G.CreateGumpItemPic(W,f,f);p.SetPos(o,h);p.SetAcceptMouseInput(False);g.Add(p);D(g,o,h,f,f,M("me"),"Use one bandage on yourself");u=o+f+t;i["count"]=l(g,"",u,h+1,k);D(g,u,h,b["count_w"],f,lambda*a:None,"Bandages left in your backpack",movable=True);v=u+b["count_w"]+t;by(g,v,h);D(g,v,h,f,f,bz,"Target someone within %d tile%s for one bandage. Alt+click: auto-follow (again to stop)"%(r,""if r==1 else "s"));w=v+f+t;bx(g,w,h);D(g,w,h,f,f,bB,"One more bandage on your last patient. Alt+click: auto-follow (again to stop)");c.update({"fill_w":-1,"text":None,"count_text":None,"wide":C,"g":g});G.AddControlOnDisposed(g,bC(g));G.AddGump(g);aH(g,al);L(m);bd()
		bW=None
		def bc(g,x,y,art,ch):
			p=aB(g,art,x,y,hue=53,mouse=False)
			if p is None:l(g,ch,x+5,y+1,C);return False
			p.SetWidth(f);p.SetHeight(f);return True
		def bx(g,x,y):
			if not bc(g,x,y,8012,"@"):return
			P(g,x+8,y,10,7,1.,"#101010")
			for r in range(7):P(g,x+9,y+r,(3-abs(r-3))*2+1,1,1.,a_)
		def by(g,x,y):
			if not bc(g,x,y,8012,"+"):return
			c=f//2
			for a,b,d,e in((c-1,0,2,5),(c-1,f-5,2,5),(0,c-1,5,2),(f-5,c-1,5,2),(c-1,c-1,2,2)):P(g,x+a,y+b,d,e,1.,a_)
		def am(o):
			a=ad()
			if a and o is not None:M(("follow",o["serial"]))()
			return a
		def bz(*a):
			if not am(b["last"]):M("other")()
		def bA(*a):am(b["target"]or b["last"])
		def bB(*a):
			if not am(b["last"]):M("again")()
		def bC(g):
			def a(*a):
				if c["g"]is g and not b["shutting"]:al();c["g"]=None;aP(h)
			return a
		def bd():
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
					au(d,w)
					if(w>0)!=(b>0)or b<0:d.IsVisible=w>0
				elif c["c"]["fill_box"]is not None:au(c["c"]["fill_box"],max(1,w-2))
			e=c["c"]["label"]
			if e is not None and(text,hue)!=c["text"]:c["text"]=(text,hue);A(e,text,k if hue is None else hue)
		def V(kind,text,level="warn"):ao(kind,text,level)
		def bD():
			a,c,e=b["skills"];d=time.time()
			if d-e>=5.:a,c=an("Healing"),an("Anatomy");b["skills"]=(a,c,d)
			return a>=aG and c>=aI
		def bE(p,hits,hmax):
			a=b["start_pct"]
			if a>0 and hmax>0:
				if hits*100./hmax<=a:
					if b["hp_armed"]:b["hp_armed"]=False;V(aR,"Your HP is at %d%%: bandage?"%int(hits*100./hmax))
				else:b["hp_armed"]=True
			if d["cure"]:
				if p.IsPoisoned:
					if b["poison_armed"]and bD():b["poison_armed"]=False;V(aS,"Poisoned: a bandage can cure it")
				else:b["poison_armed"]=True
		def bF(now):
			if now<b["count_at"]:return
			b["count_at"]=now+2.;n=0
			for c in API.FindTypeAll(W,API.Backpack)or():n+=int(c.Amount or 1)
			e,b["count"]=b["count"],n;a=d["low"]
			if a>0 and n<a:
				if b["low_armed"]and(n>0 or(e or 0)>0):b["low_armed"]=False;V(aQ,"No bandages left"if n<=0 else "Only %s left"%S(n,"bandage"))
			else:b["low_armed"]=True
			bd()
		def ap(m,px,py,reach):return max(abs(int(m.X)-px),abs(int(m.Y)-py))<=reach
		def be(m):return bf(str(m.Name or "")or "them",int(m.Serial))
		def bf(name,serial):a=E(name,serial);b=a if len(a)<=aV else a[:aV-1]+".";return{"serial":serial,"name":name,"short":b,"veil":Kit.streamer}
		def av(p,now,target):
			if b["phase"]!="idle":i("a bandage is already running.");return
			if API.HasTarget("any")or Z(h):i("a target cursor is up (aim it or press Esc first).");return
			if p.IsDead:return
			a=API.FindType(W,API.Backpack)
			if not a:u(0.,"Out!",j);i("out of bandages!",j);return
			b["rd"].new();API.UseObject(a.Serial);b["count_at"]=min(b["count_at"],now+aJ);aN(h,aC);b["target"]=target;b["begun"],b["by_buff"]=False,False;b["phase"],b["deadline"]="cursor",now+aC
		def bG(serial):
			b["pick"]=False
			if serial:M(("on",int(serial)))()
		def bg(p,now,serial):
			m=API.FindMobile(serial)
			if m is None:i("couldn't bandage them (out of sight).",j);return
			if int(p.Serial)==int(m.Serial):av(p,now,None);return
			if m.IsDead:i("they are dead.",j);return
			if not ap(m,int(p.X),int(p.Y),r):i("too far away (%s at most)."%S(r,"tile"),j);return
			av(p,now,be(m))
		def bH(now):
			a=int(API.LastTargetSerial)
			if a!=b["lt"][0]:b["lt"]=(a,now)
		def bI(p,now):
			a,c=b["lt"]
			if not a:return
			with Kit.quiet:
				if a==int(p.Serial):return
				m=API.FindMobile(a)
				if m is None or not ap(m,int(p.X),int(p.Y),r+1):return
				if now-c<=4. or(p.Hits>=p.HitsMax and not p.IsPoisoned):return be(m)
			return
		def bh(p,now,at,buff=False):
			a=b["phase"]=="heal"and not b["begun"]and not b["by_buff"]
			if b["phase"]=="cursor":H(h)
			if buff and b["phase"]=="heal":return
			if not a:b["target"]=bI(p,now)
			b["t0"]=min(now,at);b["phase"],b["begun"],b["by_buff"]="heal",not buff,buff;b["count_at"]=min(b["count_at"],now+aJ)
		def bJ(p,now):
			a=bool(API.BuffExists("Healing"));c,b["buff"]=b["buff"],a
			if a and not c:bh(p,now,now,True)
			elif c and not a and b["phase"]=="heal"and b["by_buff"]:return "done"
			return
		def bK(p,now):
			d=b["rd"].new()
			if not d:return
			f=Q.lower()+":"
			for a in d:
				e=a.low.strip()
				if e.startswith(f):continue
				if a.name and str(a.name).lower()!="system":continue
				c=aq(a,aw).strip()
				if c.startswith("you begin applying the bandages"):bh(p,now,a.at);continue
				if b["phase"]=="idle":continue
				g=b["phase"]=="cursor"or(not b["begun"]and now-b["t0"]<=2.)
				for x in bl:
					if c.startswith(x)and(g or x in aD):return e.rstrip(".!")
				if b["phase"]=="heal"and c.startswith(bm):return "done"
			return
		def bL(p,o):
			try:m=API.FindMobile(o["serial"]);a=m is not None and not m.IsDead and ap(m,int(p.X),int(p.Y),r)
			except Exception:a=False
			if not a:API.CancelTarget();i("%s is out of reach; cursor put down."%o["name"],j);return False
			API.Target(o["serial"]);b["last"]=o;i("bandaging %s."%o["name"]);return True
		def bM(action,p,now):
			if not b["pick"]and b["phase"]=="idle":b["pick"]=True;af(15.,bG,h)
		def bN(action,p,now):
			if b["last"]is None:i("nobody bandaged yet; use the target icon first.")
			else:bg(p,now,b["last"]["serial"])
		def O(v):return("%.2f"%v).rstrip("0").rstrip(".")
		bi={"follow":lambda action,p,now:Y(action[1],Q),"me":lambda action,p,now:av(p,now,None),"other":bM,"again":bN,"on":lambda action,p,now:bg(p,now,action[1])}
		def bj(w):a=("On yourself:","On someone else:","Latency buffer:");b={"stay":True,"tw":50};c=("note","s",{"dx":82+max(z(g)for g in a),"ndy":4,"h":28});e=("Bandage: one on you. Target icon: one on whoever you click (within %d tile%s). Arrow: one more on the last one."%(r,""if r==1 else "s"));d=(int(F),int(K));return(("BANDAGE TIMES",(("text","time",a[0],"Seconds one on yourself takes; applied when you stop typing (%d-%d)"%d,b),c,("text","other",a[1],"Seconds one on someone else takes, much faster on this shard (%d-%d)"%d,b),c,("text","buffer",a[2],"Seconds added for latency before the bar says Done (%d-%d)"%(int(X),int(ab)),b),c),{"sh":a0,"align":True}),("ALERTS  (sound: Settings > Alerts)",(("num","box","Alert when your HP is at or under:","One alert per fall to this % or below (0-99, 0 = never)","%",aE,aF,{"clamp":False}),("check","cure","Alert when poisoned and a bandage can cure it","Once per poisoning, with Healing %d and Anatomy %d or more"%(int(aG),int(aI))),("num","low","Alert when bandages drop under:","One alert when your bandages drop under this (%d-%d, 0 = never)"%(ag,aj),None,ag,aj,{"clamp":False})),{"sh":a1}),("WINDOW",[("check","others","Show who the bandage is on (a wider bar)","The bar names your patient. Alt+click the name: auto-follow (again to stop)")]+[("note",m,{"ndy":2})for m in Kit.wrap(e,w-24)[:2]],{"sh":a2}))
		bX=Kit.Page(d,bj)
		def bO(g,x,y,w):a=bj(w);c=dict(d,time=O(b["band_time"]),other=O(b["other_time"]),buffer=O(b["buffer"]),box=b["start_pct"]);n.update({"f":Kit.Form(g,x,y,w,c,a,ldy=4,lgap=12,fw=40),"typed":None,"applied":None})
		def bk():n.update({"f":None,"typed":None,"applied":None})
		def bP(text,lo,hi):
			try:v=float(str(text).strip().replace(",","."))
			except(ValueError,TypeError):return
			return v if lo<=v<=hi else None
		def bQ():
			f=n["f"]
			if f is None:return
			try:a=f.read(True)
			except Exception:bk();return
			f.vals=a
			if a["box"]!=b["start_pct"]:b["start_pct"]=a["box"];b["hp_armed"]=True;a8()
			if a["low"]!=d["low"]:b["count_at"]=0.
			c=False
			for k,h in(("cure","poison_armed"),("others","rebuild"),("low","low_armed")):
				if a[k]!=d[k]:d[k]=a[k];b[h]=True;c=True
			if c:bv()
			g=time.time();e=(a["time"],a["other"],a["buffer"])
			if e!=n["typed"]:n["typed"],n["since"]=e,g;return
			if n["applied"]==e or g-n["since"]<.7:return
			n["applied"]=e;c=False
			for i,(k,j,l)in enumerate((("band_time",F,K),("other_time",F,K),("buffer",X,ab))):
				v=bP(e[i],j,l)
				if v is not None and abs(v-b[k])>.001:b[k],c=v,True
			if c:a9()
		a6()
		def bR():
			a3();b["rd"]=aa();a6()
			for k,a,d in((aQ,"Bandages running low",490),(aR,"HP low: bandage?",497),(aS,"Poisoned (a bandage cures)",480),(aU,"Bandage done",514)):ae(k,a,d)
			bb();aK(h,"player",0,lambda:c["g"]);a4.service("look.hud.bandage",lambda:b.update({"rebuild":True,"redo":True}));i("on (%s s on you, %s s on others)."%(O(b["band_time"]),O(b["other_time"])),I)
		def bS():
			p=API.Player
			if p is None:return
			a=time.time()
			if b["queue"]or b["rebuild"]:
				if b["rebuild"]:
					b["rebuild"]=False;r=b.pop("redo",False)
					if c["g"]is not None and(r or c["wide"]!=d["others"]):bb()
				while b["queue"]:
					f=b["queue"].pop(0);m=f[0]if isinstance(f,tuple)else f
					if m in bi:bi[m](f,p,a)
				if c["g"]is None:return
			if p.IsDead:
				if b["phase"]!="idle":H(h)
				b["phase"],b["target"]="idle",None;u(0.,"Dead",j);return
			bF(a);s,n=p.Hits,p.HitsMax
			if n>0:bE(p,s,n)
			bH(a);e=bK(p,a);v=bJ(p,a)
			if e is None:e=v
			if e is not None and e!="done"and b["phase"]!="idle":
				if b["phase"]=="cursor":H(h)
				b["phase"],b["target"]="idle",None;u(0.,"Ready");i("the bandage failed (%s)."%e,j);return
			if b["phase"]=="heal":
				o=b["target"];g=b["other_time"]if o is not None else b["band_time"];k=a-b["t0"]
				if k>=g+b["buffer"]or e=="done":b["phase"],b["target"]="idle",None;u(1.,"Done",I);V(aU,"Bandage done","info")
				else:
					l="%.1fs"%max(0.,g-k)
					if o is not None and c["wide"]:
						if o["veil"]!=Kit.streamer:o.update(bf(o["name"],o["serial"]))
						l="%s %s"%(o["short"],l)
					u(k/g,l,C)
				return
			if b["phase"]=="cursor":
				if aO(h,"beneficial"):
					o=b["target"]
					if o is None:API.TargetSelf();q=True
					else:q=bL(p,o)
					H(h)
					if q:b["phase"],b["t0"]="heal",a
					else:b["phase"],b["target"]="idle",None
				elif a>b["deadline"]:
					if API.HasTarget("beneficial"):i("a bandage cursor is up: press Esc or aim it.")
					else:i("no bandage cursor appeared.",j)
					H(h);b["phase"],b["target"]="idle",None
				return
			t=c["text"]
			if t is None or t[0]not in("Ready","Done","Out!")or(t[0]=="Out!"and(b["count"]or 0)>0):u(0.,"Ready")
		def bT():
			if b["phase"]=="cursor":return.01
			if b["phase"]!="heal":return.1
			a=b["other_time"]if b["target"]is not None else b["band_time"];return min(.1,max(.01,b["t0"]+a+b["buffer"]-time.time()))
		def bU():b["shutting"]=True;H(h);al();aL(h);br();g,c["g"]=c["g"],None;c["c"]["label"]=c["c"]["count"]=None;L(g);a4.close()
		return{"start":bR,"tick":bS,"stop":bU,"client_tick":True,"config_height":lambda w:bq,"build_config":bO,"poll_config":bQ,"config_closed":bk,"interval":bT}
	def bh():
		h="pets";i="Pets";au="Pets_settings";a8="Pets_pos";a9="Pets_min";L=440;av,ba=280,46;ax=.25;ay=1.;t={};az=1.;bb,aB,aF=18,2,24;X=6;N=50;aG=130;aH=110;s=20;ac=1;ad=10;ag=3.;bc=("the spell fizzles","your concentration is disturbed","insufficient mana","more reagents are needed","you must wait to perform another action");aI=3.;aK=(("follow","Follow me","all follow me"),("guard","Guard me","all guard me"),("stay","Stay","all stay"),("come","Come","all come"));ah="all kill";bd=dict((bJ,bK)for bJ,bL,bK in aK);aL=(("pet_follow","Follow","%s follow me"),("pet_guard","Guard","%s guard"),("pet_stay","Stay","%s stay"));P=dict([(bM,bN)for bM,bO,bN in aL]+[("pet_kill","%s kill")]);R=(("","Bandage"),("Heal","Heal (spell)"),("Greater Heal","Greater Heal (spell)"));aM,aP="pets.low","pets.dead";be="#17171a";bf,bg,bh="#c22d2d","#2f9a3c","#d39a1c";aQ="then pick the enemy with the shard's cursor (only on a click)";e={"range":bb,"low":30,"heal":0,"kill":False,"hidden":True};bH=dict(e)
		def aS():a.update({"shutting":False,"docked":False,"queue":[],"heal":None,"confirm":None,"scan_at":0.,"look_at":0.,"note":"","full_at":0.,"note_until":0.,"order":[]})
		a={"minimized":False,"shutting":False,"docked":False,"queue":[],"followers":0,"fmax":0,"me":0,"note_hue":k,"cmd_at":{},"seq":0};aS();d={"g":None,"c":{},"store":({},{}),"rows":[],"n_rows":-1,"room":X,"w":L};aj,q,bI=ai(a,i);b={};aT={"range":(aB,aF),"low":(0,99),"heal":(0,len(R)-1)}
		def aU():aD(au,";",e,aT)
		def aV():aE(au,";",e,("range","low","heal","kill","hidden"),aT)
		def c(text,hue=None,secs=4.):a["note"],a["note_hue"]=text,k if hue is None else hue;a["note_until"]=time.time()+secs;U()
		def ak(now):return bool(a["note"])and 0<=a["note_until"]-now<=10.
		def aW():return R[e["heal"]]
		def al(n):return S(n,"tile")
		def aX(serial,name,manual=False):a["seq"]+=1;r={"serial":serial,"name":name,"seq":a["seq"],"seen":0.,"where":"gone","pct":None,"stam":None,"dist":0,"dir":"","dead":False,"poison":False,"low":False,"manual":manual,"alive":False,"noto":None};b[serial]=r;a["order"]=[];return r
		def u(serial):
			if b.pop(serial,None)is not None:a["order"]=[]
		def T(r,m,px,py,now,near):
			if r["manual"]and r.get("own"):r["own"]=bool(m.IsRenamable)
			d=str(m.Name or "");r["noto"]=Kit.noto_name(m)if Kit.cblind else None
			if d:r["name"]=d
			j,f,k,g=int(m.Hits or 0),int(m.HitsMax or 0),int(m.Stamina or 0),int(m.StaminaMax or 0);r["pct"]=max(0,min(100,int(j*100//f)))if f>0 else None;r["stam"]=max(0,min(100,int(k*100//g)))if g>0 else None;c=bool(m.IsDead);r["poison"]=bool(m.IsPoisoned);h,i=int(m.X),int(m.Y);r["dist"]=max(abs(h-px),abs(i-py));r["dir"]=Kit.compass(h-px,i-py)or "here";r["where"]="near"if near else "far";r["seen"]=now
			if c and not r["dead"]and r["alive"]:aY(aP,"%s died"%(E(r["name"],r["serial"])if r["name"]else "A pet"),r["serial"],r["name"])
			r["dead"]=c
			if c:r["low"]=True;return
			r["alive"]=True;a=e["low"];b=r["pct"]
			if b is not None:
				if a>0 and b<=a and not r["low"]:r["low"]=True;aY(aM,"%s at %d%% HP (%s)"%(E(r["name"],r["serial"])if r["name"]else "A pet",b,"here"if r["dist"]==0 else "%s %s"%(al(r["dist"]),r["dir"])),r["serial"],r["name"])
				elif r["low"]and(a<=0 or b>=a+10):r["low"]=False
		def aY(key,text,serial,name=""):ao(key,text,"warn",who=serial,name=name)
		def bi(p,now):
			i=int(p.Serial);g,h=int(p.X),int(p.Y);a["me"]=i;w=a["followers"];a["followers"],a["fmax"]=int(p.Followers or 0),int(p.FollowersMax or 0);f=set();j=False;l=e["range"];d=now>=a["full_at"]or a["full_at"]-now>ay or a["followers"]!=w
			if not d:
				n=[x for x,y in b.items()if y["where"]=="near"]
				if len(n)<a["followers"]:d=True
			if not d:
				o=[]
				for k in n:
					try:
						m=aA(k)
						if m is None or int(m.Distance)>l:d=True;break
					except Exception:d=True;break
					o.append((k,m))
				if not d:
					for k,m in o:
						try:
							r=b.get(k)
							if r is None:continue
							if not r["manual"]and not m.IsRenamable:u(k);continue
							f.add(k);T(r,m,g,h,now,True)
						except Exception:continue
					q=()
			if d:
				a["full_at"]=now+ay;q=HOST.mobiles(l)or[]
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
						r=aX(c,"")
					elif not r["manual"]and not m.IsRenamable:u(c);continue
					f.add(c);T(r,m,g,h,now,True)
				except Exception:continue
			for c,r in b.items():
				if c not in f and r["where"]=="near":j=True;r["where"]="far"
			if j or now>=a["look_at"]or a["look_at"]-now>az:
				a["look_at"]=now+az
				for c in[G for G in b if G not in f]:
					r=b[c];m=aA(c)
					if m is None:r["where"]="gone";continue
					try:
						if not r["manual"]and not m.IsRenamable:u(c);continue
						T(r,m,g,h,now,False)
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
		def bj():
			if not a["order"]or len(a["order"])!=len(b):a["order"]=sorted(b.values(),key=lambda r:r["seq"])
			return a["order"]
		def ap(g,store,items,a,e,f):
			x,y,b=a,e,1
			for h,i,c,j,k,l in items:
				d=35+z(c)
				if x>a and x+d>f:x,y,b=a,y+26,b+1
				if g is not None:Q(g,store,h,i,x,y,c,j,hue=l,on_click=k)
				x+=d+12
			return b
		def a_():
			a=[("all_"+f,W if f=="stay"else K,g,"Say \"%s\" (all your pets in earshot)"%m,q(("all",f)),None)for f,g,m in aK]
			if e["kill"]:a.append(("all_kill",K,"Kill","Say \"%s\", %s"%(ah,aQ),q(("all","kill")),j))
			return a
		def bk(w):M=F;return 30+ap(None,None,a_(),M+10,0,w-M-10)*26+22
		def a1():return L,2*F+30+2*B+bk(L)+30+N+2
		def ar():
			M=F;f=o.zone_slot(*a1());w=f[0]if f else L;d=w-2*M;E=a_();H=ap(None,None,E,M+10,0,M+d-10);s=30+H*26+22;t=2*M+30+2*B+s;I=o.rows(N,t+32,X)if f else X;p=min(I,len(b));O=f[1]-t if f else 30+max(1,p)*N+2;g,u,h=o.begin(w,t+O);R=[]
			if not a["minimized"]:
				o.frame(g);r=M+30+B;J(g,M,r,d,s,"ALL PETS  (said out loud)");ap(g,u,E,M+10,r+26,M+d-10);h["note"]=l(g,"",M+12,r+30+H*26-2,k);i=r+s+B;S="YOUR PETS  (click to target)";J(g,M,i,d,O,S);h["title_end"]=M+8+z(S);v=M+d-10-35-z("Add...");Q(g,u,"add",K,v,i+3,"Add...","List a pet of yours that isn't shown (this session)",on_click=q("add"));h["count"]=l(g,"",v-60,i+6,k);h["count_right"]=v-10;T=M+12+aG+8;aa=T+aH+10;U=aW();x=[(bJ,bL,bK,"Say \"%s\""%(P[bJ]%"<name>"))for(bJ,bK,bM),bL in zip(aL,(K,K,W))];x.append(("heal",K,"Heal","Use one bandage on this pet (within %s)"%al(ac)if not U[0]else "Cast %s on this pet (within %d tiles)"%(U[0],ad)))
				if e["kill"]:x.append(("pet_kill",K,"Kill","Say \"<name> kill\", "+aQ))
				for V in range(p):
					m=i+30+V*N;c={"val":None,"prev":None,"changed":0.,"vis_hits":False,"vis_poison":False,"stam_on":False};c["name_lbl"]=l(g,"",M+12,m+3,C);y={}
					for ab,ae,af,by in(("hits",bf,9,6),("poison",bg,9,6),("stam",bh,3,16)):n=G.CreateGumpSimpleProgressBar(aH,af,be,ae,0,100);n.SetPos(T,m+by);n.SetAcceptMouseInput(False);g.Add(n);n.IsVisible=False;y[ab]=n
					c["bars"],c["stam_bar"]=y,y.pop("stam");c["info"]=l(g,"",aa,m+3,k);D(g,M+10,m,d-20,22,a0(c,q,"target"),"Click: aim your cursor at this pet, or make it your last target. Alt+click: auto-follow (again to stop)");Y=M+10
					for A,ag,Z,ah in x:Q(g,u,"%s%d"%(A,V),ag,Y,m+24,Z,ah+". Alt+click: auto-follow (again to stop)",hue=j if A=="pet_kill"else None,on_click=a0(c,q,A));Y+=35+z(Z)+12
					R.append(c)
				h["empty"]=(l(g,"",M+12,i+33,k)if not p else None)
			o.end(g,{"rows":R,"n_rows":p,"count_w":None,"room":I,"w":w});a4(time.time())
		o=Kit.Window(h,i,a,d,ar,a8,a9,mini=(av,ba),icon=3713,cleanup=aj,lock=True,clear={"rows":[],"c":{},"n_rows":-1})
		def a2(row,key,ctrl,on):
			if row.get(key)!=on:row[key]=on;ctrl.IsVisible=on
		def a3(row,key,ctrl,v):
			if row.get(key)!=v:row[key]=v;ctrl.SetProgress(float(v),100.)
		def bl():
			if ak(time.time()):return a["note"],a["note_hue"]
			d=[g for g in b.values()if g["low"]and not g["dead"]and g["where"]!="gone"and g["pct"]is not None]
			if d:c=min(d,key=lambda r:r["pct"]);e=E(c["name"],c["serial"])if c["name"]else "pet";return "%s: %s %d%% HP"%(i,M(e,80),c["pct"]),j
			f=len([m for m in b.values()if m["where"]!="gone"])
			if not b:return "%s: none in view"%i,k
			return "%s: %s, %d in view"%(i,S(len(b),"pet"),f),k
		def U():
			c=d["c"]
			if d["g"]is None or a["docked"]:return
			if a["minimized"]:
				b=c.get("status")
				if b is not None:t,e=bl();A(b,M(t,av-90),e)
				return
			b=c.get("note")
			if b is not None:f=ak(time.time());A(b,M(a["note"],d["w"]-2*F-24)if f else "",a["note_hue"])
		def a4(now):
			if d["g"]is None or a["shutting"]or a["docked"]:return
			if a["minimized"]:U();return
			h=bj()
			if min(d["room"],len(h))!=d["n_rows"]:ar();return
			g=d["c"]
			for c,r in zip(d["rows"],h):
				Kit.row_set(c,(r["serial"],),now);i,l=r["where"],r["pct"]
				if r["dead"]or i=="gone":m=k
				elif r["low"]:m=j
				elif r["poison"]:m=I
				else:m=C
				t=aZ(r["poison"]);w=E(r["name"],r["serial"],r["noto"])if r["name"]else "(no name yet)";A(c["name_lbl"],M(w+("  "+t if t else ""),aG),m);e=None
				if i=="near"and not r["dead"]:e="poison"if r["poison"]else "hits";n="%s, %s"%("%d%%"%l if l is not None else "?%","here"if r["dist"]==0 else "%d %s"%(r["dist"],r["dir"]))
				elif r["dead"]and i!="gone":n="dead, %d %s"%(r["dist"],r["dir"])
				elif i=="far":n="far: %d %s"%(r["dist"],r["dir"])
				else:n=("out of range (%s)"%Kit.ago(now-r["seen"],Kit.AGO_SHORT)if r["seen"]else "out of range")
				A(c["info"],n,C if e else k)
				for v,x in c["bars"].items():a2(c,"vis_"+v,x,v==e)
				if e:a3(c,"p_"+e,c["bars"][e],l if l is not None else 0)
				p=r["stam"]if e else None;a2(c,"stam_on",c["stam_bar"],p is not None)
				if p is not None:a3(c,"p_stam",c["stam_bar"],p)
			o=g.get("count")
			if o is not None:
				if a["fmax"]>0:f="%d / %d slots"%(a["followers"],a["fmax"])
				else:f="%d known"%len(b)if b else ""
				if len(h)>d["room"]:
					u=("%d more, %s"%(len(h)-d["room"],f)).rstrip(", ")
					if g["count_right"]-ab(u)>=g["title_end"]+8:f=u
				A(o,f);q=ab(f)if f else 0
				if d["count_w"]!=q:d["count_w"]=q;am(o,g["count_right"]-q,Kit.ui_y(o))
			s=g.get("empty")
			if s is not None:
				if a["followers"]>0:A(s,"%s used, none in view. Add... lists one."%S(a["followers"],"slot"))
				else:A(s,"No pets in view. Click Add... to list one.")
			U()
		def a5(action,p,now):
			if not e["hidden"]:return True
			if not p.IsHidden:a["confirm"]=None;return True
			b=a["confirm"]
			if b is not None and b[0]==action and b[1]<=now<=b[2]:a["confirm"]=None;return True
			a["confirm"]=(action,now+.3,now+aI);c("That reveals you: click again to do it.",O,aI);return False
		def bm(text,now,shown):
			b=a["cmd_at"].get(text)
			if b is not None and 0<=now-b<.6:return
			if len(a["cmd_at"])>50:a["cmd_at"].clear()
			a["cmd_at"][text]=now;API.Msg(text);c("Said \"%s\"."%shown)
		def bn(serial):
			r=b.get(serial)
			if r is None or not r["name"]:c("That pet has no name yet.",j);return
			return r["name"]
		def bo(serial):
			if API.HasTarget("any")and not Z(h):
				if not aR(serial,"hud.pets",i):return
				API.Target(serial)
				if a["heal"]is not None:a["heal"]=None;H(h)
				return
			API.SetLastTarget(serial=serial);API.HeadMsg("* last target *",serial,53)
		def a6(m,p):return max(abs(int(m.X)-int(p.X)),abs(int(m.Y)-int(p.Y)))
		def bp(serial,p,now):
			r=b.get(serial);e=(r and r["name"]and E(r["name"],serial))or "that pet"
			if a["heal"]is not None:c("A heal is already on its way.",O);return
			if p.IsDead:c("You are dead.",j);return
			if API.HasTarget("any")or Z(h):c("A target cursor is up: aim it or press Esc first.",O);return
			d,n=aW();f=ad if d else ac;m=API.FindMobile(serial)
			if m is None:c("%s is out of range."%e,j);return
			k=a6(m,p)
			if k>f:c("%s is %d tiles away (%s reaches %d)."%(e,k,n.lower(),f),j);return
			if not a5(("heal",serial),p,now):return
			if d:API.CastSpell(d);g=aJ(d)[3]+ag
			else:
				l=API.FindType(3617,API.Backpack)
				if not l:c("Out of bandages.",j);API.SysMsg("%s: out of bandages!"%i,j);return
				API.UseObject(l.Serial);g=ag
			aN(h,g);a["heal"]={"serial":serial,"name":e,"until":now+g,"reach":f,"what":d or "a bandage","t0":now,"rd":aa()};c("%s for %s..."%(d or "Bandage",e))
		def bq(p,now):
			b=a["heal"];d=False;e=b["what"][0].upper()+b["what"][1:]
			for f in b["rd"].new():
				g=aq(f,aw)
				for x in bc:
					if x in g:d=True;break
				if d:break
			if d:a["heal"]=None;H(h);c("%s for %s failed."%(e,b["name"]),j);return
			if HOST.cursor_claim[0]==h and aO(h,"beneficial"):
				m=API.FindMobile(b["serial"]);a["heal"]=None;H(h)
				if m is not None and a6(m,p)<=b["reach"]:API.Target(b["serial"]);c("%s on %s."%(e,b["name"]),I)
				else:API.CancelTarget();c("%s moved out of reach."%b["name"],j)
				return
			if not 0<=b["until"]-now<=ag+10.:
				a["heal"]=None;H(h)
				if API.HasTarget("any"):c("A target cursor is up: aim it or press Esc.",O)
				else:c("No target cursor came for %s."%b["name"],j)
		def br(serial):q.add(("added",int(serial or 0)),dup=True)
		def bs(serial,p,now):
			if not serial:return
			if serial==a["me"]or serial==int(p.Serial):c("That's you.",j);return
			m=API.FindMobile(serial)
			if m is None:c("That isn't a creature in view.",j);return
			r=b.get(serial)
			if r is None:
				if len(b)>=s:an(now,room=1)
				if len(b)>=s:c("The list is full (%d)."%s,j);return
				r=aX(serial,"",manual=True)
			r["manual"]=True;r["own"]=bool(m.IsRenamable);T(r,m,int(p.X),int(p.Y),now,True)
			if r["dist"]>e["range"]:r["where"]="far"
			c("%s is listed for this session."%(E(r["name"],serial)if r["name"]else "It"),I)
		def bt(action,p,now):af(10.,br);c("Target the pet to list.")
		def a7(action,p,now):
			a=action[0]
			if(action[1]=="kill"if a=="all"else a=="pet_kill")and not e["kill"]:return
			if a=="all":c=d=ah if action[1]=="kill"else bd.get(action[1])
			else:b=bn(action[1]);c=b and P[a]%b;d=b and P[a]%E(b,action[1])
			if c and not bu(p)and a5(action,p,now):bm(c,now,d)
		def bu(p):
			if p.IsDead:c("You are dead: your pets can't hear you.",j);return True
			return False
		bv=("add","follow");at={"add":bt,"follow":lambda action,p,now:Y(action[1],i),"added":lambda action,p,now:bs(action[1],p,now),"target":lambda action,p,now:bo(action[1]),"heal":lambda action,p,now:bp(action[1],p,now),"all":a7};at.update((bP,a7)for bP in P);bw=("One heal per click, aimed at the pet when its cursor comes (bandage within %s, spell within %d)."%(al(ac),ad));bx="Said only on a click; the shard's cursor then picks the enemy."
		def by(w):a,b=([("note",g)for g in Kit.wrap(f,w-28)]for f in(bw,bx));return(("WINDOW",(("num","range","List pets within:","How far a pet is listed with its bars","tiles",aB,aF),("check","hidden","While hidden, a command or a heal needs a second click","Speaking and healing reveal you; the first click only asks"))),("HEAL BUTTON  (on each pet's row)",[("note","Heal with:",{"ndy":4,"h":28,"hue":C})]+a),("COMBAT COMMANDS",[("check","kill","Show Kill buttons (\"%s\" and \"<name> kill\")"%ah,"One for all pets and one per pet row",{"h":28})]+b),("ALERTS  (sound: Settings > Alerts)",(("num","low","Alert when a pet's HP falls to:","One alert per fall to this % or below (0-99, 0 = never)","%",0,99),)))
		def bz(f,new):
			i=Kit.dd_index(f.c["heal"],-1)
			if 0<=i<len(R):new["heal"]=i
		def bA(b,new):
			if new["hidden"]!=b["hidden"]:a["confirm"]=None
			if(new["kill"],new["heal"])!=(b["kill"],b["heal"])and d["g"]is not None:q("redraw")()
		V=Kit.Page(e,by,aV,bA,{"ldy":4,"lgap":12,"fw":44,"pad":6},strict=True,adjust=bz)
		def bB(g,x,y,w):f=V.build(g,x,y,w);a=G.CreateDropDown(200,[m for n,m in R],e["heal"]);a.SetPos(x+22+z("Heal with:"),y+90+B+30);g.Add(a);f.c["heal"]=a;a.SetTooltip("What each row's Heal button uses")
		aU()
		def bC():
			aS();a["minimized"]=o.start_min();aU()
			for r in b.values():r["where"]="gone"if r["where"]=="gone"else "far"
			ae(aM,"Pet HP low",821);ae(aP,"Pet died",497);ar();o.dock(fit=True,min=a1);aj.service("pets.list",bD)
		def bD(distance=None):
			if a["shutting"]:return
			c=e["range"]
			if distance is None:distance=c
			if distance>c:return
			return[g for g,f in b.items()if f["where"]=="near"and(not f["manual"]or f.get("own"))and f["dist"]<=distance]
		def bE():
			if d["g"]is None:return
			if aC(d):return
			b=time.time();p=API.Player
			while a["queue"]:
				c=a["queue"].pop(0);e=c[0]if isinstance(c,tuple)else c
				if not(o.action(c)or p is None and e not in bv)and e in at:at[e](c,p,b)
				if d["g"]is None:return
			if p is None:return
			if a["heal"]is not None:bq(p,b)
			if b>=a["scan_at"]or a["scan_at"]-b>ax:a["scan_at"]=b+ax;bi(p,b);a4(b)
			elif a["note"]and not ak(b):a["note"]="";U()
		def bF():return.02 if a["heal"]is not None else.1
		def bG():a["shutting"]=True;a["heal"]=None;H(h);aV();aj.close()
		return{"start":bC,"tick":bE,"stop":bG,"client_tick":True,"config_height":V.height,"build_config":bB,"poll_config":V.poll,"config_closed":V.closed,"interval":bF}
	bi=(("frames",bd,.1,"unitframes"),("timers",be,.1,"spelltimers"),("swing",bf,.025,"swing"),("bandage",bg,.1,"bandage"),("pets",bh,.1,"pets"),);return PartSet(a8,a9,bi).hooks()
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("hud","Character HUD","Frames, timers and bars for you and pets",_module_hud,.025,category="On screen",parts=(("frames","Frames","Health frames: you, target, party",True,("unitframes",)),("timers","Buffs & Timers","Timed buffs, debuffs and your spells",True,("spelltimers",)),("swing","Swing Bar","When your next melee swing lands",False,("swing",)),("bandage","Bandages","One-press bandage, timer and alerts",False,("bandage",)),("pets","Pets","Pets' health, distance and commands",False,("pets",)),),aliases=('Unit Frames','Spell Timers','Swing Timer','Bandage Agent','Pets','cast bar','buffs','debuffs','party frames','hit chance'))
