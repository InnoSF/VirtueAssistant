def _module_meters():
	aX=Follow.alt_held;aY=HOST.dock_forget;aZ=HOST.layout_slot;a_=HOST.refresh_settings;F="meters";O="Meters";a0="Meters_settings";a1="Meters_windows";W=360;ad=240;bH=1200;bI=.35;bJ=.5;a2,bK=320,46;J=360;ae=300;C=20;a3=146;V=6;bL=3823;bM=(4014,4016,4015);bN="#17171a";a4=1.;bO=.25;bP=3.;bQ=2.;a5=30.;bR=30.;a6=18;bS=12;bT=0x80000000;bU=3821;bV=8.;a7=2.;bW=2.5;bX=8.;a8=1.5;bY=4.;a9=25;av=5;aw="VirtueMeters.DamageHook";bZ=4000;ax=220;b_=a5/2;b0=40;b1=600;ay=800;ba="Meters_spots";az=20;bb=24;bc=20;af=(1,300);b2=1.;bd="Elsewhere";be=60.;ag=60;aA=40;P=4;aB=18+aA+4;aC="Meters_%08X.txt";b3=50;X=10.;b4=12;aD=40;ah=360;b5="Meters_recap_pos";b6=("Who: spell words heard before the hit,","else whom you fought (marked ?).");bf=200;bg=300;b7=20;bh=4.;b8=.5;b9=frozenset(("Magic Arrow","Harm","Fireball","Lightning","Mind Blast","Energy Bolt","Explosion","Flamestrike","Chain Lightning","Meteor Swarm","Earthquake","Poison","Poison Field","Fire Field","Holy Light","Pain Spike","Poison Strike","Strangle","Wither"));ca="you begin applying the bandages";cb=("you finish applying the bandages","you heal what little damage","you apply the bandages, but they barely help");cc="you have cured the target of all poisons";cd="the spell fizzles";ce="your concentration is disturbed";cf="insufficient mana";cg=re.compile(r"your skill in (.+?) has (increased|decreased) by "r"([0-9]+(?:\.[0-9]+)?)",re.I);ch=re.compile(r"your (strength|dexterity|intelligence) has (increased|decreased) by "r"([0-9]+)",re.I);ci=re.compile(r"you have (gained|lost) .*?\b(fame|karma)\b",re.I);bi=Kit.SPELL_WORDS;cj={3852:("Heal","heal"),3847:("Cure","cure"),3851:("Refresh",None),3849:("Strength",None),3848:("Agility",None),3853:("Explosion",None),3846:("Night Sight",None),3850:("Poison",None)};ai={3962:"Black Pearl",3963:"Blood Moss",3972:"Garlic",3973:"Ginseng",3974:"Mandrake Root",3976:"Nightshade",3981:"Spiders' Silk",3980:"Sulfurous Ash",3960:"Bat Wing",3983:"Grave Dust",3965:"Daemon Blood",3982:"Nox Crystal",3978:"Pig Iron",3903:"Arrows",7163:"Bolts"};A={"dmg_done":("Damage done","s","n","#c4562a",True),"dmg_taken":("Damage taken","s","n","#b02a2a",True),"dmg_nearby":("All damage nearby","s","n","#9a5a3a",True),"big":("Biggest hits","","n","#d07a2a",True),"kills":("Kills","h","n","#8a6ab0",False),"deaths":("Deaths","h","n","#6a6a78",True),"heal_done":("Healing done","s","n","#2f9a3c",True),"heal_taken":("Healing received","s","n","#3fae5a",True),"heal_by":("Healing by method","s","n","#4aa070",False),"cures":("Cures","m","n","#2a9a8a",True),"poisoned":("Poisonings","m","n","#5a9a2a",True),"spells":("Spells cast","m","n","#2f62cc",False),"mana":("Mana spent","m","n","#3a72d8",False),"consum":("Consumables","h","n","#a08a2a",False),"buffs":("Buffs & debuffs","h","n","#8a5ab0",False),"gold":("Gold","h","n","#cfae2a",False),"gold_place":("Gold by place","h","n","#d8b84a",False),"loot":("Items gained","h","n","#a8925a",False),"skills":("Skill gains","h","d1","#5a8acc",False),"stats":("Stat gains","h","n","#cc7a5a",False),"fame":("Fame & karma","h","n","#b0a050",False),"travel":("Travel","h","n","#6a9aaa",False),"session":("Session summary","","","#4a4a58",False)};aE=(("COMBAT",("dmg_done","dmg_taken","dmg_nearby","big","kills","deaths")),("HEALING",("heal_done","heal_taken","heal_by","cures","poisoned")),("MAGIC & ITEMS",("spells","mana","consum","buffs")),("ECONOMY & PROGRESS",("gold","gold_place","loot","skills","stats","fame","travel","session")));Q=[dF for dG,dE in aE for dF in dE];aF="dmg_done";bj={"s":"per sec","m":"per min","h":"per hour"};l={"idle":6,"engage":12,"history":10,"min_heal":3,"rows":8,"rank":True,"pct":True,"scan":True,"travel":True,"party":True,"recap":True};ck=dict(l);aG={"idle":(2,60),"engage":(3,120),"history":(1,30),"min_heal":(1,50),"rows":(3,20)};cl=5000;cm=4000;aH="(others)";cn=O.lower()+":";a={"minimized":False,"shutting":False,"docked":False,"queue":[],"active":False,"hooked":False,"jr":None,"engaged":{},"watch":{},"friendly":{},"mobs":{},"dead_seen":{},"pack_sig":None,"pend":[],"orph":[],"last_spell":None,"cast_t":0.,"prev_lt":0,"to_write":[],"changed":False};dC={"g":None,"c":{},"store":({},{})};aI,e,B=Kit.basics(a,O);m=[];p={"min":None,"b":None,"hist":{},"ver":0,"vb":{}};bk={"g":None,"c":{},"store":({},{}),"rows":[]};b={};h=[];aJ={};K={};D={"q":None,"handler":None,"event":None,"kind":"not hooked"};H={"tried":False,"tm":None,"la":None};R=[];bl=[0];import heapq;co=re.compile(r"^[0-9,]+\s+");cp=60;cq=1.;Y=HOST.mobile
	def cr():
		a=HOST.services.get("pets.list")
		if a is not None:
			try:
				b=a(distance=a6)
				if b is not None:return[int(d)for d in b]
			except Exception:pass
		c=[]
		for m in HOST.mobiles(a6):
			try:
				if m.IsRenamable:c.append(int(m.Serial))
			except Exception:pass
		return c
	def j(v,f="n"):
		if f=="d1":return "%.1f"%v
		a=abs(v)
		if a>=1e6:return "%.2fM"%(v/1e6)
		if a>=1e4:return "%.1fk"%(v/1e3)
		if a>=1000:return "%.2fk"%(v/1e3)
		if abs(v-round(v))<.05:return "%d"%int(round(v))
		return "%.1f"%v
	def I(v,f="n"):
		if f=="d1":return "%.1f"%v if abs(v)<100 else "%d"%int(round(v))
		if abs(v)<10:return "%.1f"%v
		if abs(v)<1000:return "%d"%int(round(v))
		return j(v)
	def S(v,f="n"):s=j(v,f);return s if v<0 else "+"+s
	def q(a):a=int(max(0,a));h,m,s=a//3600,(a//60)%60,a%60;return "%d:%02d:%02d"%(h,m,s)if h else "%d:%02d"%(m,s)
	def T(ser):return 0<int(ser or 0)<0x40000000
	def Z(name):return name.endswith(" (%)")
	def bm():Kit.kv_load(a0,"|",l,aG)
	def bn():Kit.kv_save(a0,"|",l,sorted(ck),aG)
	def aK(a,metric=aF,x=200,y=200,minimized=False):return{"id":a,"metric":metric if metric in A else aF,"seg":"current","x":x,"y":y,"minimized":minimized,"docked":False,"shutting":False,"g":None,"c":{},"store":({},{}),"slots":[],"picker":None,"segpick":None,"detail":None,"dc":{},"detail_row":None,"detail_metric":None,"graph":False,"gcols":[],"gkey":None,"fit":None,"size":None,"drawn":None,"resize_at":0.,"preview":False}
	def bo():
		a=[]
		for f in Kit.get_var(a1).split(";"):
			p=f.split(",")
			if len(p)<6:continue
			try:c,x,y=int(p[0]),int(p[3]),int(p[4])
			except ValueError:continue
			if any(g["id"]==c for g in a):continue
			x,y=Kit.adapt(x,y,W,0);b=aK(c,p[1],x,y,p[5]=="1");b["seg"]="overall"if p[2]=="overall"else "current";b["graph"]=len(p)>6 and p[6]=="1"
			if len(p)>8:
				try:
					d,e=int(p[7]),int(p[8])
					if d>0 and e>0:b["size"]=bp(d,e)
				except ValueError:pass
			a.append(b)
		a.sort(key=lambda w:w["id"])
		if not a or a[0]["id"]!=0:a.insert(0,aK(0))
		del h[:];h.extend(a[:V])
	def bp(sw,sh):return max(ad,min(bH,sw)),max(60,sh)
	def bq():
		if not h:bo()
		for w in h:w["size"]=None
		u()
	def u():
		a=[]
		for w in h:
			g=w["g"]
			if Kit.is_open(g):w["x"],w["y"]=g.GetX(),g.GetY()
			b=w.get("size")or(0,0);a.append("%d,%s,%s,%d,%d,%s,%s,%d,%d"%(w["id"],w["metric"],"overall"if w["seg"]=="overall"else "current",int(w["x"]),int(w["y"]),"1"if w["minimized"]else "0","1"if w.get("graph")else "0",int(b[0]),int(b[1])))
		Kit.put_var(a1,";".join(a))
	def br():
		del m[:];b,c=af
		for d in Kit.get_var(ba).split(";"):
			p=d.split(",")
			if len(p)<5 or not p[0].strip():continue
			try:a=[p[0].strip(),int(p[1]),int(p[2]),int(p[3]),max(b,min(c,int(p[4])))]
			except ValueError:continue
			if all(f[0]!=a[0]for f in m)and len(m)<az:m.append(a)
	def bs():Kit.put_var(ba,";".join("%s,%d,%d,%d,%d"%tuple(d)for d in m))
	def cs(text):
		for a in ";,|":text=text.replace(a," ")
		return " ".join(text.split())[:bb]
	def bt(kind,n=0):a=time.time();bl[0]+=1;return{"kind":kind,"n":n,"name":"Fight %d"%n if n else "Overall","start":a,"end":None,"combat":0.,"d":{},"serial":{},"big":[],"fights":0,"uid":bl[0],"ver":0,"tot":{},"place_t":{}}
	def aL():b.clear();b.update({"overall":bt("overall"),"cur":None,"hist":[],"n":0,"last_combat":0.,"c_at":None});a["watch"].clear();a["engaged"].clear();a["pend"],a["orph"]=[],[];p.update({"min":None,"b":None,"ver":p["ver"]+1});p["hist"].clear();p["vb"].clear()
	def aj():a=b["cur"];return(b["overall"],a)if a is not None else(b["overall"],)
	def bu(now):
		m=int(now//60)
		if m!=p["min"]:
			a=p["hist"]
			for k in[d for d in a if d<=m-ag]:del a[k]
			p["min"]=m;p["b"]=a.setdefault(m,{})
		return p["b"]
	def c(b,row,amt,ser=None):
		e=time.time();f=row.endswith(" (%)")
		if not f and(b!="gold"or row=="Gained"):g=bu(e);g[b]=g.get(b,0.)+amt;i=p["vb"];i[b]=i.get(b,0)+1
		for c in aj():
			d=c["d"].get(b)
			if d is None:d=c["d"][b]={}
			r=d.get(row)
			if r is None:
				if len(d)>=cl:ct(c,b,d)
				r=d[row]=[0.,0,amt,amt,e,e]
			r[0]+=amt;r[1]+=1
			if amt>r[2]:r[2]=amt
			if amt<r[3]:r[3]=amt
			r[5]=e
			if ser:c["serial"][(b,row)]=ser
			if not f:j=c["tot"];j[b]=j.get(b,0.)+amt
			c["ver"]+=1
		if amt and any(k["metric"]in(b,"session")and not k["docked"]for k in h):a["changed"]=True
	def ct(seg,a,d):
		b=sorted((abs(g[0]),f)for f,g in d.items()if f!=aH and not f.endswith(" (%)"));o=d.get(aH);c=seg["serial"]
		for e,k in b[:max(0,len(d)-cm)]:
			r=d.pop(k);c.pop((a,k),None)
			if o is None:o=d[aH]=list(r)
			else:o[0]+=r[0];o[1]+=r[1];o[2],o[3]=max(o[2],r[2]),min(o[3],r[3]);o[4],o[5]=min(o[4],r[4]),max(o[5],r[5])
	def cu(amt,name,ser):
		b=bu(time.time())
		if amt>b.get("big",0.):b["big"]=amt;c=p["vb"];c["big"]=c.get("big",0)+1
		for d in aj():
			a=d["big"]
			if len(a)>=a9 and amt<=a[-1][0]:continue
			i=len(a)
			while i>0 and a[i-1][0]<amt:i-=1
			a.insert(i,(amt,name,ser));del a[a9:]
	def E(seg,a):return seg["tot"].get(a,0)
	def bv():
		a=time.time()
		if b["cur"]is None:b["n"]+=1;b["cur"]=bt("fight",b["n"]);b["overall"]["fights"]+=1
		b["last_combat"]=a;b["c_at"]=(b["cur"]["combat"],b["overall"]["combat"])
	def cv(now):
		a=b["cur"]
		if a is None:return
		c=b.get("c_at")
		if c is not None:a["combat"],b["overall"]["combat"]=c
		else:
			f=max(0.,now-b["last_combat"])
			for e in(a,b["overall"]):e["combat"]=max(0.,e["combat"]-f)
		b["c_at"]=None;a["end"]=b["last_combat"];d=a["d"].get("dmg_done",{})
		if d:g=max(d.items(),key=lambda a:a[1][0])[0];a["name"]=g+(" +%d"%(len(d)-1)if len(d)>1 else "")
		b["hist"].insert(0,a);del b["hist"][l["history"]:];b["cur"]=None
	def ak(seg):return max(1.,seg["combat"])
	def al(seg):return max(1.,(seg["end"]or time.time())-seg["start"])
	def U(seg,a,value):
		if a=="s":return value/ak(seg)
		if a=="m":return value/(al(seg)/60.)
		return value/(max(60.,al(seg))/3600.)
	def am(w):
		s=w["seg"]
		if s=="overall":return b["overall"]
		if s!="current":
			for h in b["hist"]:
				if h["n"]==s:return h
			w["seg"]="current"
		return b["cur"]or(b["hist"][0]if b["hist"]else None)
	cw={"overall":"Overall","current":"Current"}
	def an(w):return cw.get(w["seg"])or "Fight %d"%w["seg"]
	def cx(seg):
		if seg is None:return ""
		if seg["kind"]=="overall":return q(time.time()-seg["start"])
		return q(ak(seg))
	def bw(a):return abs(a[1][0])
	def L(seg,v,r,head=j):return "%s (%s/%s)"%(head(v),I(U(seg,r,v)),r)
	def aM(a,seg,e=None):
		s,b,f,s,s=A[a]
		if seg is None:return(["No fight yet."],[])
		i=cx(seg)
		if a=="session":return cA(seg)
		if a=="big":u=seg["big"]if e is None else seg["big"][:e];g=[(dE,G,j(G),dF,None)for G,dE,dF in u];c=(["Biggest %s on %s"%(j(seg["big"][0][0]),ap(seg["big"][0][1],seg["big"][0][2]))]if seg["big"]else["No hits yet."]);return(c+[i],g)
		d=seg["d"].get(a,{})
		if a=="gold":n=d.get("Gained",[0.])[0];o=d.get("Spent / banked",[0.])[0];k=n-o;g=[("Gained",n,L(seg,n,"h"),None,d.get("Gained")),("Spent / banked",o,j(o),None,d.get("Spent / banked")),("Net",abs(k),L(seg,k,"h",S),None,None)];return(["Net %s"%S(k),"%s per hour"%I(U(seg,"h",k)),i],g)
		if a=="gold_place":return cz(seg,d,e,i)
		h=E(seg,a)
		if e is None:p=sorted(d.items(),key=bw,reverse=True)
		elif e<=0:p=[]
		else:p=heapq.nlargest(e,d.items(),key=bw)
		g=[]
		for r,t in p:
			v=t[0];m=[]
			if b:m.append(I(U(seg,b,v),f)+(""if b=="s"else "/"+b))
			if l["pct"]and h and not Z(r)and v>0:m.append("%d%%"%int(round(100.*v/h)))
			w=(S(v,f)if a in("skills","stats")else j(v,f));x=w+(" (%s)"%", ".join(m)if m else "");g.append((r,abs(v),x,seg["serial"].get((a,r)),t))
		if a in("skills","stats"):c=["Total %s"%S(h,f)]
		elif a=="cures":y=E(seg,"cures_mine");c=["Cures %s"%j(h),"by you %s"%j(y)]
		else:c=["Total %s"%j(h,f)]
		if b:c.append("%s %s"%(I(U(seg,b,h),f),bj[b]))
		c.append("in combat "+q(seg["combat"])if b=="s"else i);return(c,g)
	def bx(seg,name,gold):a=seg["place_t"].get(name,0.);return gold/(max(be,a)/3600.),a
	def cy(row):return row[1]
	def cz(seg,d,g,dur):
		m=seg["place_t"];c=list(d)
		for k,n in m.items():
			if n>=be and k not in d:c.append(k)
		e=sum(s[0]for s in d.values());a=[]
		for f in c:
			r=d.get(f);b=r[0]if r is not None else 0.;h,p=bx(seg,f,b);i=[j(b)]
			if l["pct"]and e and b>0:i.append("%d%%"%int(round(100.*b/e)))
			a.append((f,h,"%s/h (%s)"%(I(h),", ".join(i)),None,r))
		a.sort(key=cy,reverse=True)
		if g is not None:del a[max(0,g):]
		o=len(c);return(["Gained %s"%j(e),Kit.count(o,"place"),dur],a)
	def cA(seg):
		a=al(seg);c=seg["combat"];f,g,h=E(seg,"dmg_done"),E(seg,"dmg_taken"),E(seg,"heal_done");i,k=E(seg,"kills"),E(seg,"deaths");d=seg["d"].get("gold",{});l=d.get("Gained",[0.])[0]-d.get("Spent / banked",[0.])[0];e=E(seg,"skills");b=[("Time",q(a)),("In combat","%s (%d%%)"%(q(c),int(100*c/a)))]
		if seg["kind"]=="overall":b.append(("Fights","%d"%seg["fights"]))
		b+=[("Damage done",L(seg,f,"s")),("Damage taken",L(seg,g,"s")),("Healing done",L(seg,h,"s")),("Kills",L(seg,i,"h")),("Deaths",j(k)),("Gold",L(seg,l,"h",S)),("Skill gain","%s (%s/h)"%(S(e,"d1"),I(U(seg,"h",e),"d1"))),("Items gained",j(E(seg,"loot"))),("Spells cast",j(sum(s[1]for n,s in seg["d"].get("spells",{}).items()if n not in("Fizzled","Interrupted","Out of mana"))))];m=[(r,0.,t,None,None)for r,t in b];return([seg["name"]if seg["kind"]=="fight"else "Session",q(a)],m)
	def cB():
		try:
			import clr;clr.AddReference("System.Collections.Concurrent");clr.AddReference("System.Linq.Expressions");from System import Array,Int32,UInt32,Object,EventHandler,Tuple,Type,AppDomain;from System.Reflection import BindingFlags;from System.Collections.Concurrent import ConcurrentQueue;from System.Linq.Expressions import Expression,ParameterExpression;m=BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Static;e=API.GetType().Assembly;n=e.GetType("ClassicUO.Game.Managers.EventSink");f=e.GetType("ClassicUO.Game.GameObjects.Entity");a=n.GetEvent("OnEntityDamage",m);o,b,g=(clr.GetClrType(Object),clr.GetClrType(Int32),clr.GetClrType(UInt32));h=Tuple[UInt32,Int32];q=ConcurrentQueue[h]();c=Expression.Parameter(o,"sender");i=Expression.Parameter(b,"amount");j=Expression.Constant(q);p=Expression.Convert(Expression.PropertyOrField(Expression.Convert(c,f),"Serial"),g);r=clr.GetClrType(h).GetConstructor(Array[Type]([g,b]));s=Expression.Call(j,q.GetType().GetMethod("Enqueue"),Array[Expression]([Expression.New(r,Array[Expression]([p,i]))]));t=Expression.LessThan(Expression.Property(j,"Count"),Expression.Constant(bZ,b));u=Expression.IfThen(Expression.AndAlso(Expression.TypeIs(c,f),t),s);d=Expression.Lambda[EventHandler[Int32]](u,Array[ParameterExpression]([c,i])).Compile();k=AppDomain.CurrentDomain;l=k.GetData(aw)
			if l is not None:safe(lambda:a.GetRemoveMethod(True).Invoke(None,Array[Object]([l])))
			a.GetAddMethod(True).Invoke(None,Array[Object]([d]));k.SetData(aw,d);D.update({"q":q,"handler":d,"event":a,"kind":"exact (per mobile)"});return True
		except Exception as v:D.update({"q":None,"handler":None,"event":None});D["kind"]="amounts only (%s)"%(str(v)[:50]or "no hook");return False
	def cC():
		h,a=D.get("handler"),D.get("event")
		if h is None or a is None:return
		with Kit.quiet:from System import Array,Object,AppDomain;a.GetRemoveMethod(True).Invoke(None,Array[Object]([h]));AppDomain.CurrentDomain.SetData(aw,None)
		D.update({"q":None,"handler":None,"event":None,"kind":"not hooked"})
	def cD(*b):
		if not a["active"]:return
		if not a["poked"]:a["poked"]=True;HOST.poke(F,False)
		if D.get("q")is not None:return
		for c in b:
			try:a["amtq"].append(int(c))
			except Exception:continue
			del a["amtq"][:-200];return
	def cE():
		if not H["tried"]:
			H["tried"]=True
			try:from System.Reflection import BindingFlags;a=BindingFlags.Instance|BindingFlags.Public|BindingFlags.NonPublic;b=API.GetType().GetField("World",a).GetValue(API);c=b.GetType().GetProperty("TargetManager",a).GetValue(b,None);H["tm"],H["la"]=c,c.GetType().GetProperty("LastAttack",a)
			except Exception:H["tm"]=H["la"]=None
		if H["la"]is None:return 0
		return int(H["la"].GetValue(H["tm"],None)or 0)
	def cF(*b):
		if not a["active"]:return
		for c in b:
			try:a["used"].append(int(c));del a["used"][:-30];return
			except Exception:continue
	def cG(*b):
		if not a["active"]:return
		a["died"]=True
		if not a["poked"]:a["poked"]=True;HOST.poke(F,False)
	def cH(*b):
		if not a["active"]:return
		for c in b:
			t=safe(lambda:c.Title)
			if t:a["buffq"].append(str(t));del a["buffq"][:-50];return
	def cI():
		d=time.time();c={"me":None,"dmg":[],"info":{},"fhp":{},"wst":{},"used":[],"pack":None,"friends":None,"hum":[]};p=HOST.me()
		if p is None:return c
		b=int(p.Serial)
		if b!=a["my_ser"]or d>=a["next_name"]:a["my_name"]=str(p.Name or "");a["my_ser"],a["next_name"]=b,d+cq
		f={"ser":b,"name":a["my_name"],"hits":int(p.Hits),"hmax":int(p.HitsMax),"mana":int(p.Mana),"x":int(p.X),"y":int(p.Y),"gold":int(p.Gold or 0),"dead":bool(p.IsDead),"war":bool(p.InWarMode),"poison":bool(p.IsPoisoned),"map":int(API.GetMap())};c["me"]=f;q=D["q"]
		if q is not None:
			for w in range(b1):
				x,o=q.TryDequeue()
				if not x:break
				c["dmg"].append((int(o.Item1),int(o.Item2)))
		i=a["mobs"];g=c["info"]
		for b,w in c["dmg"]:
			if b not in i and b not in g and b!=f["ser"]:
				m=Y(b);g[b]=str(m.Name or "")if m is not None else ""
				if m is not None and m.IsHuman:c["hum"].append(b)
		c["lt"]=int(API.LastTargetSerial or 0);c["la"]=cE()
		for j in(a["engaged"],(c["lt"],c["la"])):
			for b in j:
				if T(b)and b not in i and b not in g and b!=f["ser"]:
					m=Y(b)
					if m is not None:
						g[b]=str(m.Name or "")
						if m.IsHuman:c["hum"].append(b)
		if d>=a["next_friends"]:
			a["next_friends"]=d+bP;r=[int(G)for G in API.GetPartyMemberSerials()or[]];s=cr();t=[int(dE)for dE in API.GetAllFriends()or[]];c["friends"]=(r,s,t);h,u=[],set()
			for j in(t,s,r):
				for e in j:
					if e!=f["ser"]and e not in u:
						u.add(e)
						if Y(e)is not None:h.append(e)
		else:h=None
		y=c["friends"]is not None;z=c["fhp"]
		for b in a["present"]:
			m=Y(b)
			if m is not None:A=None if y else i.get(b);z[b]=(int(m.Hits),int(m.HitsMax),bool(m.IsPoisoned),bool(m.IsDead),A or str(m.Name or ""))
		if h is not None:a["present"]=h
		k=c["wst"]
		for b,B in a["watch"].items():
			if d-B["t"]>b_:continue
			if Y(b)is not None:k[b]="alive"
			elif API.FindMobile(b|bT)is not None:k[b]="dying"
			else:k[b]="gone"
		if a["used"]:
			C,a["used"]=a["used"],[]
			for b in C:
				n=API.FindItem(b)
				if n is not None:c["used"].append((int(n.Graphic),str(n.Name or "")))
		if not l["scan"]:a["pscan"]=None
		elif a["pscan"]is None and d>=a["next_scan"]:
			a["next_scan"]=d+bQ
			if API.Backpack:a["pscan"]=[HOST.pack_items(True),0,[],0,0,d]
		v=a["pscan"]
		if v is not None:c["pack"]=cJ(v,d)
		return c
	def cJ(e,now):
		m,i,g,h,j,n=e;o=len(m);p=min(o,i+cp)
		try:
			while i<p:b=m[i];c=int(b.Amount or 1)or 1;h+=int(b.Serial or 0);j+=c;g.append((b,c));i+=1
		except Exception:
			a["pscan"]=None
			if n==now:raise
			a["next_scan"]=0.;return
		if i<o:e[1],e[3],e[4]=i,h,j;return
		a["pscan"]=None;f=(len(g),h,j)
		if f==a["pack_sig"]and a["pack"]is not None:a["pack_cand"]=None;return
		if n!=now and a.get("pack_cand")!=f:a["pack_cand"]=f;a["next_scan"]=0.;return
		a["pack_cand"]=None;a["pack_sig"]=f;d={}
		for b,c in g:
			k=(int(b.Graphic),int(b.Hue))
			if k in d:d[k][0]+=c
			else:d[k]=[c,None,b]
		q=a["pack"]or{}
		for k,v in d.items():
			l=q.get(k)
			if l is None or v[0]>l[0]:
				try:v[1]=str(v[2].Name or "")
				except Exception:v[1]=""
			else:v[1]=l[1]
			v[2]=None
		return d
	def aN(ser):b=a["me"];return(b is not None and ser==b["ser"])or ser in a["friendly"]
	def ao(ser):
		b=a["me"]
		if b is not None and ser==b["ser"]:return b["name"]or "You"
		return a["mobs"].get(ser)or "Unknown"
	def ap(name,ser=None):
		if not Kit.streamer or not name:return name
		b=name[:-4]if Z(name)else name;c=a["me"]
		if c is not None and b==c["name"]:return Kit.veil("me",b)+name[len(b):]
		if b.lower()not in K:return name
		return Kit.veil("name",b,ser if T(ser)else Kit.checksum(b.lower().encode("utf-8")))+name[len(b):]
	def by(ser,now):t=a["engaged"].get(ser);return t is not None and now-t<=l["engage"]
	def aa(now,kind,method,secs):
		b=kind=="cure+";kind="cure"if b else kind
		for o in list(a["orph"]):
			if o[1]==kind and now-o[0]<=a8:
				a["orph"].remove(o);bz(kind,method,o[2],o[3],o[4])
				if not b:return
		a["pend"].append([now+secs,kind,method,b])
	def bz(kind,method,ser,name,amt):
		if kind=="heal":
			c("heal_done",name,amt,ser)
			if not Z(name):c("heal_by",method,amt)
		else:c("cures_mine",method,1)
	def bA(kind,now,ser,name,amt):
		for p in a["pend"]:
			if p[1]==kind and now<=p[0]:
				if not p[3]:a["pend"].remove(p)
				bz(kind,p[2],ser,name,amt);return
		a["orph"].append((now,kind,ser,name,amt))
	def cK():
		b=set()
		for c in aj():
			for d in c["d"].values():b.update((f[:-4]if Z(f)else f).lower()for f in d)
			b.update(str(g[1]).lower()for g in c["big"])
		if a["recap"]is not None:b.update(str(i[2]).lower()for i in a["recap"]["rows"])
		e=[n for n in K if n in b][-(ay//2):];K.clear();K.update((r,True)for r in e)
	def cL(s,now):
		d=s["me"]
		if d is None:return
		f,a["me"]=a["me"],d;g=a["mobs"]
		if len(g)>ay:g.clear()
		if len(K)>ay:g.clear();cK()
		for b,e in s["info"].items():
			if e:g[b]=e
		for b in s["hum"]:
			if g.get(b):K[g[b].lower()]=True
		if a["pend"]:a["pend"]=[dE for dE in a["pend"]if dE[0]>=now]
		if a["orph"]:a["orph"]=[dF for dF in a["orph"]if now-dF[0]<=a8]
		if s["friends"]is not None:
			J,O,L=s["friends"];B={}
			for P,Q in(("friend",L),("pet",O),("party",J)):
				for b in Q:B[b]=P
			for b in L+J:
				r=s["fhp"][b][4]if b in s["fhp"]else g.get(b)
				if r:K[r.lower()]=True
			B.pop(d["ser"],None);a["friendly"]=B
		m,t=s.get("lt",0),s.get("la",0)
		if t and d["war"]and T(t)and not aN(t):a["engaged"][t]=now
		if(T(m)and not aN(m)and(m!=a["prev_lt"]or now-a["cast_t"]<=2.)):a["engaged"][m]=now
		a["prev_lt"]=m
		if a["engaged"]:
			for b in[dG for dG,dH in a["engaged"].items()if now-dH>l["engage"]]:a["engaged"].pop(b,None)
		C=0
		if f is not None and d["hits"]<f["hits"]:C=f["hits"]-d["hits"]
		for b,R in s["dmg"]:aO(b,R,now)
		if a["amtq"]:
			u=None
			for h in a["amtq"]:
				if C>=h:C-=h;aO(d["ser"],h,now)
				else:
					if u is None:u=max(a["engaged"].items(),key=lambda a:a[1])[0]if a["engaged"]else 0
					aO(u,h,now)if u else c("dmg_nearby","Unknown",h)
			a["amtq"]=[]
		v=s["fhp"];v[d["ser"]]=(d["hits"],d["hmax"],d["poison"],d["dead"],d["name"]or "You")
		for b,(M,x,D,E,e)in v.items():
			if e:g[b]=e
			e=ao(b);i=a["prev"].get(b);a["prev"][b]=(M,x,D,E)
			if i is None:continue
			if E and not i[3]:
				if now-a["dead_seen"].get(b,0)>10:
					c("deaths",e,1,b);a["dead_seen"][b]=now
					if b==d["ser"]and l["recap"]:bC(now)
				continue
			if E or i[3]:continue
			F=b==d["ser"]or a["friendly"].get(b)=="party"or x not in(25,100);G=M-i[0]
			if G>=(l["min_heal"]if F else 1)and x==i[1]:y=e if F else e+" (%)";h=G if F else G*100./max(1,x);c("heal_taken",y,h,b);bA("heal",now,b,y,h)
			if D and not i[2]:c("poisoned",e,1,b)
			elif i[2]and not D:c("cures",e,1,b);bA("cure",now,b,e,1)
		if len(a["prev"])!=len(v):
			for b in[dI for dI in a["prev"]if dI not in v]:a["prev"].pop(b,None)
		for b,S in s["wst"].items():
			w=a["watch"].get(b)
			if w is None:continue
			if S=="dying":
				a["watch"].pop(b,None)
				if w["friend"]:
					if now-a["dead_seen"].get(b,0)>10:c("deaths",w["name"],1,b);a["dead_seen"][b]=now
				elif w["mine"]and now-w["mine"]<=bR:c("kills",w["name"],1)
		if a["watch"]:
			for b in[dJ for dJ,dK in a["watch"].items()if now-dK["t"]>a5]:a["watch"].pop(b,None)
		if a["dead_seen"]:
			for b in[dL for dL,dM in a["dead_seen"].items()if now-dM>30]:a["dead_seen"].pop(b,None)
		j=a["hp_log"]
		if not j or j[-1][1]!=d["hits"]or j[-1][2]!=d["hmax"]:
			j.append((now,d["hits"],d["hmax"]))
			if len(j)>bg:del j[:len(j)-bg]
		if f is not None and d["mana"]<f["mana"]and not d["dead"]:H=a["last_spell"];y=H[1]if H is not None and now-H[0]<=bY else "Other";c("mana",y,f["mana"]-d["mana"])
		if f is not None and f["ser"]==d["ser"]:
			n=d["gold"]-f["gold"]
			if n>0:c("gold","Gained",n);c("gold_place",a["place"]or bd,n)
			elif n<0:c("gold","Spent / banked",-n)
		U=(d["x"],d["y"],d["map"])
		if l["travel"]and a["pos"]is not None and(d["x"]or d["y"]):
			V,W,X=a["pos"];I=max(abs(d["x"]-V),abs(d["y"]-W))
			if X!=d["map"]or I>bS:c("travel","Recalls, gates & teleports",1)
			elif I>0:c("travel","Tiles walked",I)
		a["pos"]=U
		for Y,e in s["used"]:
			o=cj.get(Y)
			if o is None:continue
			Z=o[0]+" potion";c("consum",Z,1)
			if o[1]:aa(now,o[1],o[0]+" potion",bW)
		p=s["pack"]
		if p is not None:
			q=a["pack"];ab=q is not None and len(q)==0 and len(p)>0
			if q is not None and not ab:
				for k,N in p.items():
					z=q.get(k);A=N[0]-(z[0]if z else 0)
					if A>0 and k[0]!=bU:r=co.sub("",(N[1]or "").strip())or "Item 0x%04X"%k[0];c("loot",r.title(),A)
					elif A<0 and k[0]in ai:c("consum",ai[k[0]],-A)
				for k,z in q.items():
					if k not in p and k[0]in ai:c("consum",ai[k[0]],z[0])
			a["pack"]=p
		if a["buffq"]:
			for ac in a["buffq"]:c("buffs",ac,1)
			a["buffq"]=[]
	def aO(ser,dmg,now):
		d=a["me"];b=ao(ser);c("dmg_nearby",b,dmg,ser);w=a["watch"].get(ser)
		if w is None:
			if len(a["watch"])>=b0:e=min(a["watch"].items(),key=lambda a:a[1]["t"])[0];a["watch"].pop(e,None)
			w=a["watch"][ser]={"name":b,"t":now,"mine":0.,"friend":False}
		w["t"],w["name"]=now,b
		if aN(ser):
			w["friend"]=ser!=d["ser"];c("dmg_taken",b,dmg,ser);bv()
			if ser==d["ser"]:cT(dmg,now)
		elif by(ser,now):a["engaged"][ser]=now;w["mine"]=now;c("dmg_done",b,dmg,ser);cu(dmg,b,ser);bv()
	def cM(now):
		g=a["me"];e=g["name"]if g else None
		for h in a["jr"].new():
			f=h.name;b=h.low.strip()
			if e and f==e:
				d=bi.get(b)
				if d is not None:
					c("spells",d[0],1);a["last_spell"]=(now,d[0]);a["cast_t"]=now
					if d[1]=="heal":aa(now,"heal",d[0],bV)
					elif d[1]in("cure","cure+"):aa(now,d[1],d[0],bX)
				continue
			if b.startswith(cn):continue
			if b.startswith(cd):c("spells","Fizzled",1)
			elif b.startswith(ce):c("spells","Interrupted",1)
			elif b.startswith(cf):c("spells","Out of mana",1)
			elif b.startswith(ca):c("consum","Bandages",1)
			elif b.startswith(cc):aa(now,"cure","Bandage",a7)
			elif b.startswith(cb):aa(now,"heal","Bandage",a7)
			else:
				if f and e:
					d=bi.get(b)
					if d is not None:
						if d[0]in b9:cR(now,f,d[0])
						continue
				if "your skill in"in b:
					m=cg.search(b)
					if m:v=float(m.group(3));c("skills",m.group(1).strip().title(),v if m.group(2).lower()=="increased"else-v);continue
				if "your "in b and " has "in b:
					m=ch.search(b)
					if m:v=int(m.group(3));c("stats",m.group(1).title(),v if m.group(2).lower()=="increased"else-v);continue
				if "you have "in b and("fame"in b or "karma"in b):
					m=ci.search(b)
					if m:c("fame","%s %s"%(m.group(2).title(),m.group(1).lower()),1)
	def cN(me):
		c=HOST.guard_area()
		if c:return str(c)
		a=None;x,y,e=me["x"],me["y"],me["map"]
		for b in m:
			if b[3]==e:
				d=max(abs(x-b[1]),abs(y-b[2]))
				if d<=b[4]and(a is None or d<a[0]):a=(d,b[0])
		return a[1]if a is not None else bd
	def cO(now,e):
		b=a["me"]
		if b is None:return
		if a["place"]is None or now>=a["next_place"]:a["next_place"]=now+b2;a["place"]=cN(b)
		c=a["place"]
		for f in aj():d=f["place_t"];d[c]=d.get(c,0.)+e
	def cP(name,radius):
		b=a["me"]
		if b is None or not(b["x"]or b["y"]):B("position unknown; try again.",Kit.HUE_BAD);return
		name=cs(name)or "Spot %d"%(len(m)+1);d,e=af;radius=max(d,min(e,int(radius)));c=[g for g in m if g[0].lower()==name.lower()]
		if not c and len(m)>=az:B("%d spots at most; remove one first."%az,Kit.HUE_BAD);return
		for f in c:m.remove(f)
		m.append([name,b["x"],b["y"],b["map"],radius]);bs();a["place"]=None;B("spot \"%s\" named here (%d, %d), %d tiles round."%(name,b["x"],b["y"],radius),Kit.HUE_GOOD);a_(F)
	def bB(name):
		n=len(m);m[:]=[d for d in m if d[0]!=name]
		if len(m)!=n:bs();a["place"]=None;a_(F)
	def cQ(now):
		b=a["fnames"]
		if b is not None and b[0]==now:return b[1]
		c=a["mobs"];d=set(c.get(f)for f in a["friendly"]if c.get(f));a["fnames"]=(now,d);return d
	def cR(now,name,spell):
		if name in cQ(now):return
		c=Kit.spell_info(spell);d=float(c[3])if c else 0.;b=a["casts"];b.append([now,name,spell,False,d])
		while b and(len(b)>b7 or now-b[0][0]>b[0][4]+bh):b.pop(0)
	def cS(now):
		for c in a["casts"]:
			f=now-c[0]
			if not c[3]and c[4]-b8<=f<=c[4]+bh:c[3]=True;return "%s: %s"%(c[1],c[2]),c[1],0
		b=None
		for g,t in a["engaged"].items():
			if b is None or t>b[1]:b=(g,t)
		if b is not None and by(b[0],now):d=ao(b[0]);return d+"?",d,b[0]
		e=a["me"]
		if e is not None and e["poison"]:return "Poison",None,0
		return "Unknown",None,0
	def cT(dmg,now):
		c=a["me"];d,e,f=cS(now);b=a["taken"];b.append((now,dmg,d,e,f,c["hits"],c["hmax"]))
		if len(b)>bf:del b[:len(b)-bf]
	def bC(now):
		e=now-X;f=[n for n in a["taken"]if n[0]>=e];c,d=[],None
		for h in a["hp_log"]:
			if h[0]<e:d=h
			else:c.append(h)
		if d is not None:c.insert(0,(e,d[1],d[2]))
		j=a["me"]
		if j is not None:c.append((now,0,j["hmax"]))
		g=set(r[3]for r in f if r[3]and not r[4]);i={}
		if g:
			for k,b in a["mobs"].items():
				if b in g:i[b]=k
			for m in API.GetAllMobiles()or[]:
				try:
					b=str(m.Name or "")
					if b in g:i[b]=int(m.Serial)
				except Exception:continue
		l=[(s[0],s[1],s[2],s[4]or i.get(s[3],0),s[5],s[6])for s in f];a["recap"]={"t":now,"rows":l,"hp":c,"total":sum(t[1]for t in f)};a["recap_show"]=True
	def cU(now):
		b=a["me"]
		if b is None or now-a["dead_seen"].get(b["ser"],0)<=10:return
		c("deaths",ao(b["ser"]),1,b["ser"]);a["dead_seen"][b["ser"]]=now
		if l["recap"]:bC(now)
	def cV(w):
		c=am(w);e=an(w)
		if c is None:c,e=b["overall"],"Overall"
		f=a["me"];j=f["ser"]if f else int(safe(lambda:API.Player.Serial,0)or 0);k=Kit.data_path(aC%j);g=c["name"]if e!=c["name"]else "";d=["Meters export: %s%s, %s"%(e," (%s)"%g if g else "",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),("Session time %s, in combat %s"%(q(al(c)),q(c["combat"]))if c["kind"]=="overall"else "Fight time %s"%q(ak(c))),""]
		for h in Q:
			l,i=aM(h,c,b3);d.append("== %s =="%A[h][0]);d.append("   "+"   ".join(n for n in l if n))
			for m,r in enumerate(i):d.append("   %2d. %-30s %s"%(m+1,r[0],r[2]))
			if not i:d.append("   (nothing)")
			d.append("")
		a["to_write"].append((k,"\n".join(d)+"\n",e))
	def cW():
		while a["to_write"]and not a["shutting"]:
			b,c,d=a["to_write"].pop(0)
			try:
				with open(b,"w")as e:e.write(c)
				B("%s exported to %s."%(d,b),Kit.HUE_GOOD)
			except Exception as f:B("couldn't write %s (%s)."%(b,f),Kit.HUE_BAD)
	M=Kit.MARGIN
	def z(w):return F if w["id"]==0 else "%s_%d"%(F,w["id"])
	def N(w):return O if w["id"]==0 else "%s %d"%(O,w["id"]+1)
	def cX(w,g):
		def b(*b):
			if w["g"]is g and not a["shutting"]:
				w["g"]=None
				if w["id"]==0:HOST.disable(F)
				else:e.add(("closed",w["id"]),dup=True)
		return b
	def cY(w,slot,g):
		def a(*a):
			if w.get(slot)is g:w[slot]=None
		return a
	def cZ(w,i):
		def a(*c):
			a=w["slots"]
			if i>=len(a):return
			b=a[i].get("ser")
			if aX():
				if b:e(("follow",b))()
				return
			e(("detail",w["id"],i))()
		return a
	def bD(w):n=8+35+Kit.text_w("New")+14+35+Kit.text_w("Report")+8;return n+14+35+Kit.text_w("Reset")if w["id"]==0 else n
	def o(w):
		x,y=w["x"],w["y"];v=w["g"]
		if Kit.is_open(v):x,y=v.GetX(),v.GetY()
		w["g"]=None;f,h,R,S=({},{}),{},[],[];T=w["metric"];U=("Close "+N(w)+(" (this window only)"if w["id"]else " (turns it off; the Modules tab turns it back on)"));w["resize_at"],w["preview"]=0.,False
		if w["minimized"]:g=G.CreateGump(True,True);a,b=a2,bK;h["status"]=Kit.mini_bar(g,f,a,b,N(w),z(w),e(("toggle_min",w["id"])),close_tip=U)
		else:
			i=l["rows"];m=M+30+Kit.GAP;d=m+30+Kit.GAP;n=56+(aB if w.get("graph")else 0);af=bD(w);B=w["fit"];q=B if B is not None else w["size"];ah=(max(120,q[0])if q else W)-2*M;X=af>ah
			if X:n+=26
			j=n+i*C;a,b=W,d+j+M
			if q is not None:
				a,b=max(120,q[0]),q[1];i=max(1,(b-d-M-n)//C);j=max(n+i*C,b-d-M)
				if B is not None:j=max(30,min(j,b-d-M));i=max(0,(j-n)//C)
				b=d+j+M
			c=a-2*M
			if B is None:x,y=Kit.clamp(x,y,a,b);ai=d+n+C+M;g=G.CreateModernGump(x,y,a,b,True,min(ad,a),min(ai,b),c_(w));g.SetAlpha(0)
			else:g=G.CreateGump(True,True)
			Kit.add_window_frame(g,a,b,mouse=False);aj=0 if Kit.zone_up(z(w))else 84+Kit.DOCK_DX;ak=(Kit.MARGIN+30+Kit.text_w(N(w).upper())+16+aj+35+Kit.text_w("Settings")+Kit.MARGIN);Kit.title_bar(g,f,a,N(w),z(w),e(("toggle_min",w["id"])),e(("to_bar",w["id"])),e(("settings",))if a>=ak else None,close_tip=U);Kit.add_section(g,M,m,c,30);H=M+8;Kit.art_button(g,f,"prev",bM,H,m+4,None,"Show previous display",on_click=e(("step",w["id"],-1)));Kit.art_button(g,f,"next",Kit.ART_PLAY,H+32,m+4,None,"Show next display",on_click=e(("step",w["id"],1)));r,al,al,Y,Z=A[T];I=H+68;K=M+c-6-I-35-10-35-40;D=r if K>=Kit.text_w(r)else(Kit.fit(r,K)if K>=40 else None);Kit.art_button(g,f,"pick",Kit.ART_PAGE,I,m+4,D,"Pick what this window shows"+(""if D==r else " (now: %s)"%r),on_click=e(("picker",w["id"])));E=I+(35+Kit.text_w(D)if D else 30)+10;h["seg_room"],h["iw"]=max(20,M+c-6-E-35),c;am=Kit.fit(an(w),h["seg_room"]);h["seg"]=Kit.art_button(g,f,"segs",Kit.ART_PAGE,E,m+4,am,"Pick a segment: current fight, Overall or an earlier fight",on_click=e(("segpick",w["id"])));Kit.add_section(g,M,d,c,j);h["head"]=Kit.add_label(g,"",M+8,d+5,Kit.HUE_INFO);aa="Alt+click: auto-follow (again to stop)"
			if T in("session","big","gold"):ab=aa if Z else None
			else:ab="Show this row's details"+(". "+aa if Z else "")
			L=min(a3,int(c*.45));ao=c-12-L-10
			for k in range(i):s=d+26+k*C;F=G.CreateGumpSimpleProgressBar(c-12,C-2,bN,Y,0,100);F.SetPos(M+6,s);F.SetAcceptMouseInput(False);g.Add(F);ln=Kit.add_label(g,"",M+10,s+1,Kit.HUE_TEXT);lv=Kit.add_label(g,"",M+c-6-L,s+1,Kit.HUE_TEXT);R.append({"bar":F,"name":ln,"val":lv,"ser":None,"key":None,"prog":None,"nw":ao,"vw":L})
			for k in range(i):s=d+26+k*C;Kit.catcher(g,M+6,s,c-12,C-2,cZ(w,k),ab)
			o=d+26+i*C+4
			if w.get("graph"):
				gy=o-2;h["gcap"]=Kit.add_label(g,"",M+10,gy,Kit.HUE_INFO);ac=gy+18+aA;ae=max(1,min(ag,(c-12)//(P+1)));gx=M+6+(c-12-ae*(P+1))//2
				for k in range(ae):t=G.CreateGumpColorBox(.9,Y);t.SetRect(gx+k*(P+1),ac-1,P,1);t.IsVisible=False;t.SetAcceptMouseInput(False);g.Add(t);S.append({"box":t,"x":gx+k*(P+1),"h":0})
				h["gbase"]=ac;o+=aB
			Kit.art_button(g,f,"new",Kit.ART_PAGE,M+8,o,"New","Open another window (up to %d)"%V,on_click=e(("new",)));rx=M+8+35+Kit.text_w("New")+14;Kit.art_button(g,f,"report",Kit.ART_PAGE,rx,o,"Report","Post the top %d rows to party chat (if set and in a party), else the journal"%av,on_click=e(("report",w["id"])))
			if w["id"]==0:ap=o+26 if X else o;Kit.art_button(g,f,"reset",Kit.ART_CLOSE,a-M-8-35-Kit.text_w("Reset"),ap,"Reset","Clear all meters; new session",on_click=e(("reset",)))
		w["x"],w["y"]=Kit.show_window(g,x,y,a,b,z(w),w["minimized"]and w["docked"],cX(w,g),u,w,{"g":g,"c":h,"store":f,"slots":R,"vkey":None,"gcols":S,"gkey":None,"drawn":(a,b)})
		for aq in("picker","segpick","detail"):
			p=w.get(aq)
			if Kit.is_open(p)and not w["minimized"]:
				O=Kit.scroll_info(p)
				if O is not None:Q,sh=int(O["w"]),int(O["h"])
				else:Q,sh=int(p.GetWidth()or J),int(p.GetHeight()or 200)
				E,sy=aP(w,Q);Kit.place(p,E,sy,Q,sh);Kit.attach(p,g)
		aV(w);Kit.dispose(v)
	def c_(w):
		def a(*a):
			w["resize_at"]=time.time();g=w["g"]
			if w["preview"]or w["fit"]is not None or w["minimized"]or not Kit.is_open(g):return
			if(int(g.GetWidth()),int(g.GetHeight()))!=w["drawn"]:w["preview"]=True;g.SetAlpha(.55)
		return a
	def c0(w):
		g=w["g"];w["preview"]=False
		if not Kit.is_open(g)or w["minimized"]:return
		b,a=int(g.GetWidth()),int(g.GetHeight())
		if w["fit"]is not None:
			g.SetAlpha(0)
			if(b,a)!=w["drawn"]:o(w)
			return
		c=w["drawn"]or(0,0)
		if abs(b-c[0])<=2 and abs(a-c[1])<=2:g.SetAlpha(0);return
		d=Kit.screen()[1]
		if d>0:a=min(a,d)
		w["size"]=bp(b,a);o(w);u()
	def aP(w,width):
		g=w["g"];r=Kit.rect(g)if Kit.is_open(g)else None;x,y=(r[0],r[1])if r is not None else(w["x"],w["y"]);b=Kit.screen()[0];a=x+((w.get("drawn")or(W,0))[0])+4
		if b and a+width>b:a=max(0,x-width-4)
		return a,y
	def aq(width,a,title,store,b,action,g=None):
		if g is None:g=G.CreateGump(True,True)
		Kit.add_window_frame(g,width,a);Kit.add_section(g,M,M,width-2*M,30);Kit.add_label(g,title,M+30,M+7,Kit.HUE_TITLE);Kit.art_button(g,store,b,Kit.ART_CLOSE,width-M-54,M+4,None,"Close this window",on_click=e(action));return g
	def aQ(w,slot):Kit.dispose(w[slot]);w[slot]=None
	def aR(w,slot,g,width,a):b,c=aP(w,width);Kit.show_window(g,b,c,width,a,None,False,cY(w,slot,g),None,w,{slot:g});Kit.attach(g,w["g"])
	def aS(w):
		aQ(w,"picker");a=J-2*M;c=(a-24)//2;f=[28+((len(r)+1)//2)*22+6 for s,r in aE];h=28+2*22+6;i=M+30+sum(t+Kit.GAP for t in f)+h+Kit.GAP+M;g=aq(J,i,"DISPLAYS",({},{}),"pclose",("close_sub",w["id"],"picker"));y=M+30+Kit.GAP
		for(o,p),j in zip(aE,f):
			Kit.add_section(g,M,y,a,j,o)
			for k,b in enumerate(p):l=M+12+(k%2)*(c+12);m=y+28+(k//2)*22;q=Kit.HUE_TITLE if b==w["metric"]else Kit.HUE_TEXT;Kit.add_label(g,Kit.fit(A[b][0],c-4),l,m,q);Kit.catcher(g,l-2,m-2,c,20,e(("metric",w["id"],b)),"Show %s in this window"%A[b][0])
			y+=j+Kit.GAP
		Kit.add_section(g,M,y,a,h,"THIS WINDOW");n=bool(w.get("graph"));d="on"if n else "off";Kit.add_label(g,Kit.fit("Last-hour graph",a-36-Kit.text_w(d)),M+12,y+28);Kit.add_label(g,d,M+a-12-Kit.text_w(d),y+28,Kit.HUE_GOOD if n else Kit.HUE_INFO);Kit.catcher(g,M+8,y+26,a-16,20,e(("graph",w["id"])),"Show or hide the last hour under the rows, one bar per minute");Kit.add_label(g,Kit.fit("Export this segment",a-24),M+12,y+50);Kit.catcher(g,M+8,y+48,a-16,20,e(("export",w["id"])),"Write every display to %s in the VirtueAssistantSettings folder"%(aC.replace("%08X","<serial>")));aR(w,"picker",g,J,i)
	def c1(w):
		aQ(w,"segpick");a=J-2*M;c=[("current","Current fight"+(" (going on)"if b["cur"]else " (or the last)"),""),("overall","Overall (session)",q(time.time()-b["overall"]["start"]))]
		for h in b["hist"]:c.append((h["n"],"#%d  %s"%(h["n"],h["name"]),"%s  %s"%(q(ak(h)),j(E(h,"dmg_done")))))
		f=28+len(c)*22+6;i=M+30+Kit.GAP+f+M;g=aq(J,i,"SEGMENTS",({},{}),"sclose",("close_sub",w["id"],"segpick"));y=M+30+Kit.GAP;Kit.add_section(g,M,y,a,f,"WHAT TO SHOW  (fight time, damage done)");k=110
		for n,(l,o,m)in enumerate(c):
			d=y+28+n*22;p=Kit.HUE_TITLE if l==w["seg"]else Kit.HUE_TEXT;Kit.add_label(g,Kit.fit(o,a-24-k-6),M+12,d,p)
			if m:Kit.add_label(g,m,M+a-12-k,d,Kit.HUE_INFO)
			Kit.catcher(g,M+8,d-2,a-16,20,e(("seg",w["id"],l)),"Show this segment")
		aR(w,"segpick",g,J,i)
	ab=("Total","Share","Rate","Times","Average","Biggest","Smallest","First","Last")
	def c2(w):
		aQ(w,"detail");a=ae-2*M;b=30+len(ab)*20+6;d=M+30+Kit.GAP+b+M;g=aq(ae,d,"DETAILS",({},{}),"dclose",("close_sub",w["id"],"detail"));c={};y=M+30+Kit.GAP;Kit.add_section(g,M,y,a,b);c["name"]=Kit.add_label(g,"",M+10,y+6,Kit.HUE_TITLE);e=max(Kit.text_w(k)for k in ab)+14
		for i,t in enumerate(ab):f=y+30+i*20;Kit.add_label(g,t,M+10,f,Kit.HUE_INFO);c[t]=Kit.add_label(g,"",M+10+e,f,Kit.HUE_TEXT)
		c["vw"]=a-20-e;w["dc"]=c;aR(w,"detail",g,ae,d);ar(w)
	def c3(w):
		a=w["metric"];m=int(time.time()//60);f=(a,m,p["ver"],p["vb"].get(a,0))
		if f==w["gkey"]:return
		w["gkey"]=f;l=p["hist"];d=[];b=0.
		if a!="session":
			n=m-ag+1
			for i in range(ag):
				g=l.get(n+i);v=g.get(a,0.)if g is not None else 0.
				if v>b:b=v
				d.append(v)
		o=w["c"]["gbase"];q=len(d)-len(w["gcols"])
		for i,c in enumerate(w["gcols"]):
			v=d[i+q]if d else 0.;h=int(round(aA*v/b))if b>0 and v>0 else 0
			if v>0 and h<1:h=1
			if h!=c["h"]:
				k=c["box"]
				if h:Kit.ui_rect(k,c["x"],o-h,P,h)
				if(h>0)!=(c["h"]>0):k.IsVisible=h>0
				c["h"]=h
		if a=="session":e="No graph for the summary"
		elif b<=0:e="Last hour, per minute: nothing yet"
		else:e="Last hour, %s per minute: peak %s"%("biggest hit"if a=="big"else "gained"if a in("gold","gold_place")else "total",j(b,A[a][2]or "n"))
		Kit.set_text(w["c"]["gcap"],Kit.fit(e,w["c"].get("iw",W-2*Kit.MARGIN)-20))
	def ac(a,k,text,width):
		f=a.get(k)
		if f is not None and f[0]==text and f[1]==width:return f[2]
		b=Kit.fit(text,width);a[k]=(text,width,b);return b
	def c4(i):
		def a(*b):
			a=bk["rows"]
			if i<len(a)and a[i]and aX():e(("follow",a[i]))()
		return a
	def c5(hp,t):
		a=hp[0]if hp else(t,0,0)
		for h in hp:
			if h[0]>t:break
			a=h
		return a[1],a[2]
	def aT():
		b=a["recap"]
		if b is None:return
		c=ah-2*M;k=b["rows"][-b4:];d=30;l=30+20+d+8+max(1,len(k))*20+2*18+6;s=M+30+Kit.GAP+l+M;g,A,J=aU.begin(ah,s,aP(h[0],ah)if h else None);aq(ah,s,"DEATH RECAP",A,"close",("recap_close",),g);f=M+30+Kit.GAP;Kit.add_section(g,M,f,c,l,"LAST %d SECONDS  (damage you took)"%int(X));B=len(b["rows"]);C="Died %s: %s damage in %s"%(time.strftime("%H:%M:%S",time.localtime(b["t"])),j(b["total"]),Kit.count(B,"hit"));Kit.add_label(g,Kit.fit(C,c-20),M+10,f+26,Kit.HUE_TEXT);m=f+26+20;Kit.add_label(g,"HP",M+10,m+(d-16)//2,Kit.HUE_INFO);t=M+10+Kit.text_w("HP")+8;u=max(2,(M+c-10-t)//aD);D=b["t"]-X
		for i in range(aD):
			n,o=c5(b["hp"],D+(i+1)*X/aD);p=int(round(d*max(0,n)/float(o)))if o>0 else 0
			if p>0:v=G.CreateGumpColorBox(.9,"#c22d2d");v.SetRect(t+i*u,m+d-p,max(1,u-1),p);g.Add(v)
		w=m+d+8;q=[]
		if not k:Kit.add_label(g,"No damage seen.",M+10,w,Kit.HUE_INFO)
		x,y=M+60,c-166
		for i,(E,F,H,r,n,o)in enumerate(k):
			e=w+i*20;Kit.add_label(g,"-%.1fs"%max(0.,b["t"]-E),M+10,e,Kit.HUE_INFO);Kit.add_label(g,Kit.fit(ap(H,r),y),x,e,Kit.HUE_TEXT);z="-%s"%j(F);Kit.add_label(g,z,M+c-64-Kit.text_w(z),e,Kit.HUE_BAD);Kit.add_label(g,"HP %d"%n,M+c-58,e,Kit.HUE_INFO);q.append(r if T(r)else 0)
			if q[-1]:Kit.catcher(g,x-2,e-2,y+4,20,c4(i),"Alt+click: auto-follow (again to stop)")
		for i,I in enumerate(b6):Kit.add_label(g,Kit.fit(I,c-20),M+10,f+l-40+i*18,Kit.HUE_INFO)
		aU.end(g,{"rows":q})
	aU=Kit.Window(F,O,None,bk,aT,b5,cleanup=aI,names=None,lock=False,owner=False,clear={"rows":[]});dD=None
	def aV(w):
		r=w["g"]
		if not Kit.is_open(r):return
		e=w["metric"]
		if w.get("gcols")and not w["minimized"]:c3(w)
		c=am(w);n=a["me"];h=n["name"]if n else None;f=None
		if c is not None:
			if c["end"]is not None:f=(e,w["seg"],c["uid"],c["ver"],w["minimized"],l["rank"],l["pct"],h)
			elif A[e][1]=="s":f=(e,w["seg"],c["uid"],c["ver"],c["combat"],w["minimized"],l["rank"],l["pct"],h)
			if f is not None and f==w.get("vkey"):ar(w);return
		w["vkey"]=f;o,i=aM(e,c,0 if w["minimized"]else len(w["slots"]));d=w["c"]
		if w["minimized"]:
			p=d.get("status")
			if p is not None:Kit.set_text(p,ac(d,"_fst","%s: %s  %s"%(N(w),A[e][0],"  ".join(o[:2])),a2-90))
			return
		Kit.set_text(d["head"],ac(d,"_fhd","   ".join(G for G in o if G),d.get("iw",W-2*Kit.MARGIN)-16));Kit.set_text(d["seg"],ac(d,"_fsg",an(w),d.get("seg_room",400)));s=max([dE[1]for dE in i]+[0.])
		for j,b in enumerate(w["slots"]):
			if j<len(i):k,t,u,m,y=i[j];q=ap(k,m);v=("%d. %s"%(j+1,q))if l["rank"]else q;x=Kit.HUE_TITLE if(h and k==h)else Kit.HUE_TEXT;Kit.set_text(b["name"],ac(b,"_fn",v,b["nw"]),x);Kit.set_text(b["val"],ac(b,"_fv",u,b.get("vw",a3)));g=(float(t),float(s or 1.));b["ser"],b["key"]=(m if T(m)else None),k
			else:Kit.set_text(b["name"],"");Kit.set_text(b["val"],"");g=(0.,1.);b["ser"],b["key"]=None,None
			if g!=b["prog"]:b["prog"]=g;b["bar"].SetProgress(g[0],g[1])
		ar(w)
	def ar(w):
		if not Kit.is_open(w["detail"]):return
		d=w["dc"];a,c=w["detail_metric"],w["detail_row"];b=am(w);r=b["d"].get(a,{}).get(c)if(b is not None and a)else None;m=b["serial"].get((a,c))if b is not None and a else None;Kit.set_text(d["name"],Kit.fit("%s (%s)"%(ap(c,m)or "",A.get(a,("",))[0]),ae-2*Kit.MARGIN-20));e=dict((s,"")for s in ab)
		if r is not None:
			k,g,f,k,k=A[a];l=time.time();h=E(b,a)
			if a=="gold_place":n,o=bx(b,c,r[0]);i="%s/h (%s there)"%(I(n),q(o))
			elif g:i="%s %s"%(I(U(b,g,r[0]),f),bj[g])
			else:i="-"
			e.update({"Total":j(r[0],f),"Share":("%d%% of %s"%(int(round(100.*r[0]/h)),j(h,f))if h and not Z(c)else "-"),"Rate":i,"Times":"%d"%r[1],"Average":j(r[0]/max(1,r[1]),f),"Biggest":j(r[2],f),"Smallest":j(r[3],f),"First":"%s ago"%q(l-r[4]),"Last":"%s ago"%q(l-r[5])})
		elif c:e["Total"]="nothing in this segment"
		for t in ab:Kit.set_text(d[t],Kit.fit(e[t],d["vw"]))
	def at():return bool(SNAP.drag)or SNAP.pressed()is True
	def c6(w):
		def a(fw,fh,mode):
			a=(int(fw),int(fh))if(fw is not None and fh is not None)else None
			if a!=w.get("fit")or(mode=="again"and a is not None):w["fit"]=a;e(("redraw",w["id"]))()
		return a
	def c7(w):
		def a():a=56+(aB if w.get("graph")else 0)+(26 if bD(w)>ad-2*M else 0);return ad,M+30+Kit.GAP+30+Kit.GAP+a+C+M
		return a
	def c8():
		if at():return
		for w in h:
			g=w["g"]
			if w["minimized"]or w["docked"]or w["resize_at"]or not Kit.is_open(g):continue
			a=aZ(z(w))
			if a is not None:
				a=(int(a[0]),int(a[1]));b=w["fit"]
				if b is None or abs(b[0]-a[0])>4 or abs(b[1]-a[1])>4:w["fit"]=a;o(w);continue
				if w["drawn"]is None or w["drawn"][0]!=max(120,b[0]):o(w);continue
				c=(int(g.GetWidth()),int(g.GetHeight()))
				if abs(c[0]-w["drawn"][0])>2 or abs(c[1]-w["drawn"][1])>2:
					w["misfit"]=w.get("misfit",0)+1
					if w["misfit"]in(2,6,20):o(w)
				else:w["misfit"]=0
			elif w["fit"]is not None and not HOST.layout_holds(z(w)):w["fit"]=None;o(w)
	def aW(w):a=Kit.dock_hooks(N(w),bL,w,w,e(("redraw",w["id"])),fit=c6(w));a.update({"exact":True,"verify":True,"pieces_out":True,"min":c7(w)});HOST.dock_add(z(w),a)
	def bE(w,remove):
		w["shutting"]=True;HOST.dock_remove(z(w))
		if remove:aY(z(w))
		for k in("picker","segpick","detail","g"):g,w[k]=w[k],None;Kit.dispose(g)
		if remove and w in h:h.remove(w)
	def c9(w):
		d=w["metric"];h=am(w);b,i=aM(d,h,av);c="%s (%s)"%(A[d][0],an(w));e=["%d. %s %s"%(n+1,k[0],k[2])for n,k in enumerate(i[:av])]
		if l["party"]and API.GetPartyMemberSerials():
			f="; ".join(e)or "nothing yet";g="%s: %s; %s"%(c,"  ".join(b[:2]),f);j=[g]if len(g)<=ax else["%s: %s"%(c,"  ".join(b[:2])),f]
			for a in j:
				if len(a)>ax:a=a[:ax-2]+".."
				API.PartyMsg(a)
		else:
			B("%s: %s."%(c,"  ".join(b)),Kit.HUE_INFO)
			for p in e or["nothing yet"]:B("   %s."%p,Kit.HUE_TEXT)
	def da(action,w):
		if len(h)>=V:B("%d windows at most."%V,Kit.HUE_INFO);return
		a=h[-1];g=a["g"];c,d=(g.GetX(),g.GetY())if Kit.is_open(g)else(a["x"],a["y"]);e=max(k["id"]for k in h)+1;f=set(n["metric"]for n in h);i=next((r for r in Q if r not in f),aF);b=aK(e,i,c+30,d+30);h.append(b);o(b);aW(b);u()
	def db(action,w):
		for a in h:
			b=a["size"]is not None;a["size"]=None
			if b and a["fit"]is None and Kit.is_open(a["g"]):o(a)
		u()
	def dc(action,w):aL();a["next_ui"]=0.;B("all meters cleared; new session.",Kit.HUE_GOOD)
	def dd(action,w):
		if a["recap"]is None:B("no death this session.",Kit.HUE_INFO)
		else:aT()
	def de(action,w):
		w["graph"]=not w.get("graph");o(w);aW(w)
		if Kit.is_open(w["picker"]):aS(w)
		u()
	def df(action,w):a["redraw_wait"].discard(w["id"]);bE(w,True);u()
	def dg(action,w):w["minimized"],w["docked"]=not w["minimized"],False;aY(z(w));o(w);u()
	def dh(action,w):
		if at():a["redraw_wait"].add(w["id"]);return
		a["redraw_wait"].discard(w["id"]);o(w);u()
	def di(action,w):
		i=Q.index(w["metric"])if w["metric"]in Q else 0;w["metric"]=Q[(i+action[2])%len(Q)];o(w)
		if Kit.is_open(w["picker"]):aS(w)
		u()
	def bF(action,w):
		a=action[0]
		if Kit.is_open(w[a]):Kit.dispose(w[a])
		else:(aS if a=="picker"else c1)(w)
	def dj(action,w):w["metric"]=action[2];Kit.dispose(w["picker"]);o(w);u()
	def dk(action,w):w["seg"]=action[2];Kit.dispose(w["segpick"]);aV(w);u()
	def dl(action,w):
		a=w["slots"];i=action[2];b=a[i].get("key")if i<len(a)else None
		if b is None or w["metric"]in("session","big","gold"):return
		w["detail_row"],w["detail_metric"]=b,w["metric"]
		if Kit.is_open(w["detail"]):ar(w)
		else:c2(w)
	dm={"settings":lambda action,w:HOST.show_settings(F),"follow":lambda action,w:Follow.toggle(action[1],O),"new":da,"own_size":db,"reset":dc,"spot_add":lambda action,w:cP(action[1],action[2]),"spot_rm":lambda action,w:bB(action[1]),"recap":dd,"recap_close":lambda action,w:aU.close(),"graph":de,"export":lambda action,w:cV(w),"closed":df,"toggle_min":dg,"to_bar":lambda action,w:HOST.dock_to_bar(z(w),N(w)),"redraw":dh,"step":di,"picker":bF,"segpick":bF,"metric":dj,"seg":dk,"close_sub":lambda action,w:Kit.dispose(w.get(action[2])),"detail":dl,"report":lambda action,w:c9(w)};dn=("settings","follow","new","own_size","reset","spot_add","spot_rm","recap","recap_close");do=(("idle","A fight ends after quiet of:","No damage for this long ends the fight","s"),("engage","Your targets count for:","Damage on what you attacked or targeted this recently is yours","s"),("history","Earlier fights kept:","Finished fights in the segment list","fights"),("min_heal","Ignore HP rises under:","Smaller rises count as regeneration","HP"),("rows","Rows per window:","For windows at their own size; undoes corner drags","rows"));dp=(("rank","Number the rows","A rank before each name"),("pct","Show each row's share (%)","Percentage of the total after the value"),("party","Report to party chat in a party","Unticked, Report goes to your journal"),("scan","Watch the backpack (loot, reagents, ammo)","Open your backpack once after login so the client knows its contents"),("travel","Count tiles walked and recalls / gates","Fills the Travel display"),("recap","Show a death recap when you die","The last %d s of damage taken: who, how much, your HP"%int(X)));dq="Pets' and strangers' healing is a \"(%)\" row outside the total.";bG=24
	def dr(w):return(("COUNTING  (fights, healing, rows)",[("num",)+d+aG[d[0]]for d in do],{"align":True,"pad":4}),("SHOW AND TRACK",[("check",)+f for f in dp]+[("note",Kit.fit(dq,w-28),{"ndy":2,"h":18})],{"pad":4}),("GOLD BY PLACE  (per character)",(("custom",28+max(1,len(m))*bG,ds),),{"pad":4}),("TOOLS",(("buttons",(("new",Kit.ART_PAGE,"New meter window","Open one more (up to %d)"%V),("recap",Kit.ART_PAGE,"Last death recap","Show it again"),("own_size",Kit.ART_CLOSE,"Reset sizes","Give windows outside zones their own size (Rows above, %d px wide)"%W))),("buttons",(("export",Kit.ART_OK,"Export","Write the first window's segment to %s in the VirtueAssistantSettings folder"%aC.replace("%08X","<serial>")),("reset",Kit.ART_CLOSE,"Reset all meters","Clear everything; new session"))),("note",Kit.fit("Damage numbers: "+D["kind"],w-28),{"key":"feed","h":26})),{"pad":4}))
	def ds(f,x,y):
		g,c,w,h=f.g,f.c,f.w,f.store;Kit.add_label(g,"Name:",x+12,y+3);i=x+12+Kit.text_w("Name:")+8;c["spot_name"]=Kit.with_tip(Kit.add_textbox(g,"",i,y,140,numbers=False),"Spot name (up to %d letters)"%bb);a=i+140+12;Kit.add_label(g,"Radius:",a,y+3);a+=Kit.text_w("Radius:")+8;c["spot_radius"]=Kit.with_tip(Kit.add_textbox(g,str(aJ.get("radius",bc)),a,y,44),"Tiles round you (%d-%d)"%af);a+=44+10;Kit.add_label(g,"tiles",a,y+3,Kit.HUE_INFO);Kit.art_button(g,h,"spot_add",Kit.ART_OK,a+Kit.text_w("tiles")+12,y-2,"Name this spot","Gold gained within the radius counts here (a guarded town comes first)")
		if not m:Kit.add_label(g,Kit.fit("No spots yet: stand where you farm, type a name, click Name this spot.",w-28),x+12,y+28+3,Kit.HUE_INFO)
		d=Kit.pic_size(Kit.ART_CLOSE[0])[0]or 30;c["spot_rm"]=[("spot_rm%d"%n,r[0])for n,r in enumerate(m)]
		for j,b in enumerate(m):e=y+28+j*bG;k="facet %d at %d, %d, %d tiles round"%(b[3],b[1],b[2],b[4]);l=Kit.text_w(k);Kit.add_label(g,Kit.fit(b[0],w-24-d-18-l-12),x+12,e+3);Kit.add_label(g,k,x+w-12-d-12-l,e+3,Kit.HUE_INFO);Kit.art_button(g,h,"spot_rm%d"%j,Kit.ART_CLOSE,x+w-12-d,e,None,"Remove "+b[0])
	dt=.2
	def du(f):
		c,b=f.c,f.store
		for k in("reset","new"):
			if Kit.was_clicked(b,k):e((k,))()
		if Kit.was_clicked(b,"own_size"):
			if a["active"]:e(("own_size",))()
			else:bq()
		d=[r for n,r in(("export",("export",0)),("recap",("recap",)))if Kit.was_clicked(b,n)]
		if Kit.was_clicked(b,"spot_add"):aJ["radius"]=Kit.read_int(c["spot_radius"],bc,*af);d.append(("spot_add",str(c["spot_name"].Text or ""),aJ["radius"]))
		for h in d:
			if a["active"]:e(h)()
			else:B("turn Meters on first.",Kit.HUE_INFO)
		for i,g in c["spot_rm"]:
			if Kit.was_clicked(b,i):
				if a["active"]:e(("spot_rm",g))()
				else:bB(g)
	def dv(f,new):Kit.set_text(f.c["feed"],Kit.fit("Damage numbers: "+D["kind"],f.w-28))
	def dw(old,new):
		del b["hist"][new["history"]:]
		if new["rows"]!=old["rows"]:
			if a["active"]:
				for w in h:w["size"]=None;e(("redraw",w["id"]))()
			else:bq()
		a["next_ui"]=0.
	au=Kit.Page(l,dr,bn,dw,adjust=dv,clicks=du,every=dt);bm();br();aL()
	def dx():
		a.update({"shutting":False,"active":True,"queue":[],"last_tick":time.time(),"next_ui":0.,"next_friends":0.,"next_scan":0.,"me":None,"pos":None,"pack":None,"prev":{},"used":[],"buffq":[],"amtq":[],"poked":False,"place":None,"next_place":0.,"taken":[],"hp_log":[],"casts":[],"recap":None,"recap_show":False,"to_write":[],"redraw_wait":set(),"present":[],"pscan":None,"pack_cand":None,"my_ser":None,"my_name":"","next_name":0.,"fnames":None,"died":False});a["jr"]=Journal.reader();bm();aL();bo();br();aI.add(cC)
		for w in h:
			w["shutting"]=w["docked"]=False
			if HOST.dock_wanted(z(w)):w["minimized"]=True;w["docked"]=HOST.dock_soon(z(w))
		Kit.hook_once(a,"hooked",("ObjectUsed",cF),("OnBuffAdded",cH),("OnEntityDamage",cD),("OnPlayerDeath",cG))
		if D["handler"]is None:del R[:];R.append(cB)
		for w in h:
			b=aZ(z(w))if HOST.booting()and w["fit"]is None else None
			if b and b[0]and b[1]:w["fit"]=(int(b[0]),int(b[1]))
			o(w);aW(w)
	def dy():
		a["poked"]=False
		if not h or h[0]["g"]is None:return
		c=time.time();f=max(0.,min(1.,c-a["last_tick"]));a["last_tick"]=c
		for w in list(h):
			if Kit.was_clicked(w["store"],"close"):
				if w["id"]==0:Kit.dispose(w["g"]);return
				e.add(("closed",w["id"]),dup=True)
		while a["queue"]:
			d=a["queue"].pop(0);g=d[0];w=(next((n for n in h if n["id"]==d[1]),None)if len(d)>1 and isinstance(d[1],int)and g!="follow"else None)
			if w is not None or g in dn:dm[g](d,w)
		if a["redraw_wait"]and not at():
			j,a["redraw_wait"]=a["redraw_wait"],set()
			for w in list(h):
				if w["id"]in j:o(w)
			u()
		for w in h:
			if w["resize_at"]and c-w["resize_at"]>=bI and not at():w["resize_at"]=0.;c0(w)
		if c>=a.get("next_zone",0.):a["next_zone"]=c+bJ;c8()
		try:s=cI()
		except Exception as k:
			s=None;i=str(k)[:120]
			if i!=a.get("err"):a["err"]=i;B("couldn't read the client (%s)."%i,Kit.HUE_BAD)
		cM(c)
		if s:cL(s,c)
		if a["died"]:a["died"]=False;cU(c)
		cO(c,f)
		if a["recap_show"]:a["recap_show"]=False;aT()
		if b["cur"]is not None:
			b["cur"]["combat"]+=f;b["overall"]["combat"]+=f
			if not 0.<=c-b["last_combat"]<=l["idle"]:cv(c);a["next_ui"]=0.
		if c>=a["next_ui"]or(a["changed"]and a["next_ui"]-c<=a4-bO):
			a["next_ui"]=c+a4;a["changed"]=False
			for w in h:
				if not w["docked"]:aV(w)
	def dz():
		while R and not a["shutting"]:R.pop(0)()
		if a["to_write"]:cW()
	def dA():return bool(R)or bool(a["to_write"])
	def dB():
		a["shutting"],a["active"],a["jr"]=True,False,None;del R[:];u();bn();aI.close()
		for w in list(h):bE(w,False)
	return{"start":dx,"tick":dy,"stop":dB,"client_tick":True,"config_height":au.height,"build_config":au.build,"poll_config":au.poll,"config_closed":au.closed,"thread_tick":dz,"thread_wanted":dA}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("meters","Meters","Damage, healing, loot and gold meters",_module_meters,.25,category="Extras")
