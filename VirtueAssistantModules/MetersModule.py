def _module_meters():
	bf=Follow.alt_held;bg=HOST.dock_forget;bh=HOST.refresh_settings;aa=Kit.ART_CLOSE;bi=Kit.ART_OK;ab=Kit.ART_PAGE;B=Kit.GAP;am=Kit.HUE_BAD;aw=Kit.HUE_GOOD;q=Kit.HUE_INFO;P=Kit.HUE_TEXT;an=Kit.HUE_TITLE;ac=Kit.MARGIN;e=Kit.add_label;S=Kit.add_section;bj=Kit.add_textbox;bk=Kit.add_window_frame;O=Kit.art_button;bl=Kit.attach;ad=Kit.catcher;T=Kit.dispose;u=Kit.fit;bm=Kit.get_var;z=Kit.is_open;bn=Kit.put_var;bo=Kit.screen;J=Kit.set_text;bp=Kit.show_window;p=Kit.text_w;ae=Kit.was_clicked;bq=Kit.with_tip;Q="meters";af="Meters";br="Meters_settings";bs="Meters_windows";W=360;ax=240;b7=1200;b8=.35;b9=.5;bt,ca=320,46;V=360;ay=300;K=20;bu=146;ao=6;cb=3823;cc=(4014,4016,4015);cd="#17171a";bv=1.;ce=.25;cf=3.;cg=2.;bw=30.;ch=30.;bx=18;ci=12;cj=0x80000000;ck=3821;cl=8.;by=2.;cm=2.5;cn=8.;bz=1.5;co=4.;bA=25;aO=5;aP="VirtueMeters.DamageHook";cp=4000;aQ=220;cq=bw/2;cr=40;cs=600;aR=800;bB="Meters_spots";aS=20;bC=24;bD=20;az=(1,300);ct=1.;bE="Elsewhere";bF=60.;aA=60;aT=40;ag=4;aU=18+aT+4;aV="Meters_%08X.txt";cu=50;ap=10.;cv=12;aW=40;aB=360;cw="Meters_recap_pos";cx=("Who: spell words heard before the hit,","else whom you fought (marked ?).");bG=200;bH=300;cy=20;bI=4.;cz=.5;cA=frozenset(("Magic Arrow","Harm","Fireball","Lightning","Mind Blast","Energy Bolt","Explosion","Flamestrike","Chain Lightning","Meteor Swarm","Earthquake","Poison","Poison Field","Fire Field","Holy Light","Pain Spike","Poison Strike","Strangle","Wither"));cB="you begin applying the bandages";cC=("you finish applying the bandages","you heal what little damage","you apply the bandages, but they barely help");cD="you have cured the target of all poisons";cE="the spell fizzles";cF="your concentration is disturbed";cG="insufficient mana";cH=re.compile(r"your skill in (.+?) has (increased|decreased) by "r"([0-9]+(?:\.[0-9]+)?)",re.I);cI=re.compile(r"your (strength|dexterity|intelligence) has (increased|decreased) by "r"([0-9]+)",re.I);cJ=re.compile(r"you have (gained|lost) .*?\b(fame|karma)\b",re.I);bJ=Kit.SPELL_WORDS;cK={3852:("Heal","heal"),3847:("Cure","cure"),3851:("Refresh",None),3849:("Strength",None),3848:("Agility",None),3853:("Explosion",None),3846:("Night Sight",None),3850:("Poison",None)};aC={3962:"Black Pearl",3963:"Blood Moss",3972:"Garlic",3973:"Ginseng",3974:"Mandrake Root",3976:"Nightshade",3981:"Spiders' Silk",3980:"Sulfurous Ash",3960:"Bat Wing",3983:"Grave Dust",3965:"Daemon Blood",3982:"Nox Crystal",3978:"Pig Iron",3903:"Arrows",7163:"Bolts"};F={"dmg_done":("Damage done","s","n","#c4562a",True),"dmg_taken":("Damage taken","s","n","#b02a2a",True),"dmg_nearby":("All damage nearby","s","n","#9a5a3a",True),"big":("Biggest hits","","n","#d07a2a",True),"kills":("Kills","h","n","#8a6ab0",False),"deaths":("Deaths","h","n","#6a6a78",True),"heal_done":("Healing done","s","n","#2f9a3c",True),"heal_taken":("Healing received","s","n","#3fae5a",True),"heal_by":("Healing by method","s","n","#4aa070",False),"cures":("Cures","m","n","#2a9a8a",True),"poisoned":("Poisonings","m","n","#5a9a2a",True),"spells":("Spells cast","m","n","#2f62cc",False),"mana":("Mana spent","m","n","#3a72d8",False),"consum":("Consumables","h","n","#a08a2a",False),"buffs":("Buffs & debuffs","h","n","#8a5ab0",False),"gold":("Gold","h","n","#cfae2a",False),"gold_place":("Gold by place","h","n","#d8b84a",False),"loot":("Items gained","h","n","#a8925a",False),"skills":("Skill gains","h","d1","#5a8acc",False),"stats":("Stat gains","h","n","#cc7a5a",False),"fame":("Fame & karma","h","n","#b0a050",False),"travel":("Travel","h","n","#6a9aaa",False),"session":("Session summary","","","#4a4a58",False)};aX=(("COMBAT",("dmg_done","dmg_taken","dmg_nearby","big","kills","deaths")),("HEALING",("heal_done","heal_taken","heal_by","cures","poisoned")),("MAGIC & ITEMS",("spells","mana","consum","buffs")),("ECONOMY & PROGRESS",("gold","gold_place","loot","skills","stats","fame","travel","session")));ah=[d5 for d6,d4 in aX for d5 in d4];aY="dmg_done";bK={"s":"per sec","m":"per min","h":"per hour"};m={"idle":6,"engage":12,"history":10,"min_heal":3,"rows":8,"rank":True,"pct":True,"scan":True,"travel":True,"party":True,"recap":True};cL=dict(m);aZ={"idle":(2,60),"engage":(3,120),"history":(1,30),"min_heal":(1,50),"rows":(3,20)};cM=5000;cN=4000;a_="(others)";cO=af.lower()+":";a={"minimized":False,"shutting":False,"docked":False,"queue":[],"active":False,"hooked":False,"jr":None,"engaged":{},"watch":{},"friendly":{},"mobs":{},"dead_seen":{},"pack_sig":None,"pend":[],"orph":[],"last_spell":None,"cast_t":0.,"prev_lt":0,"to_write":[],"changed":False};d2={"g":None,"c":{},"store":({},{})};a0,h,H=Kit.basics(a,af);o=[];C={"min":None,"b":None,"hist":{},"ver":0,"vb":{}};bL={"g":None,"c":{},"store":({},{}),"rows":[]};b={};j=[];a1={};X={};L={"q":None,"handler":None,"event":None,"kind":"not hooked"};R={"tried":False,"tm":None,"la":None};ai=[];bM=[0];import heapq;cP=re.compile(r"^[0-9,]+\s+");cQ=60;cR=1.;aq=HOST.mobile
	def cS():
		a=HOST.services.get("pets.list")
		if a is not None:
			try:
				b=a(distance=bx)
				if b is not None:return[int(d)for d in b]
			except Exception:pass
		c=[]
		for m in HOST.mobiles(bx):
			try:
				if m.IsRenamable:c.append(int(m.Serial))
			except Exception:pass
		return c
	def l(v,f="n"):
		if f=="d1":return "%.1f"%v
		a=abs(v)
		if a>=1e6:return "%.2fM"%(v/1e6)
		if a>=1e4:return "%.1fk"%(v/1e3)
		if a>=1000:return "%.2fk"%(v/1e3)
		if abs(v-round(v))<.05:return "%d"%int(round(v))
		return "%.1f"%v
	def U(v,f="n"):
		if f=="d1":return "%.1f"%v if abs(v)<100 else "%d"%int(round(v))
		if abs(v)<10:return "%.1f"%v
		if abs(v)<1000:return "%d"%int(round(v))
		return l(v)
	def aj(v,f="n"):s=l(v,f);return s if v<0 else "+"+s
	def D(a):a=int(max(0,a));h,m,s=a//3600,(a//60)%60,a%60;return "%d:%02d:%02d"%(h,m,s)if h else "%d:%02d"%(m,s)
	def ak(ser):return 0<int(ser or 0)<0x40000000
	def ar(name):return name.endswith(" (%)")
	def bN():Kit.kv_load(br,"|",m,aZ)
	def bO():Kit.kv_save(br,"|",m,sorted(cL),aZ)
	def a2(a,metric=aY,x=200,y=200,minimized=False):return{"id":a,"metric":metric if metric in F else aY,"seg":"current","x":x,"y":y,"minimized":minimized,"docked":False,"shutting":False,"g":None,"c":{},"store":({},{}),"slots":[],"picker":None,"segpick":None,"detail":None,"dc":{},"detail_row":None,"detail_metric":None,"graph":False,"gcols":[],"gkey":None,"fit":None,"size":None,"drawn":None,"resize_at":0.,"preview":False}
	def bP():
		a=[]
		for f in bm(bs).split(";"):
			p=f.split(",")
			if len(p)<6:continue
			try:c,x,y=int(p[0]),int(p[3]),int(p[4])
			except ValueError:continue
			if any(g["id"]==c for g in a):continue
			x,y=Kit.adapt(x,y,W,0);b=a2(c,p[1],x,y,p[5]=="1");b["seg"]="overall"if p[2]=="overall"else "current";b["graph"]=len(p)>6 and p[6]=="1"
			if len(p)>8:
				try:
					d,e=int(p[7]),int(p[8])
					if d>0 and e>0:b["size"]=bQ(d,e)
				except ValueError:pass
			a.append(b)
		a.sort(key=lambda w:w["id"])
		if not a or a[0]["id"]!=0:a.insert(0,a2(0))
		del j[:];j.extend(a[:ao])
	def bQ(sw,sh):return max(ax,min(b7,sw)),max(60,sh)
	def bR():
		if not j:bP()
		for w in j:w["size"]=None
		E()
	def E():
		a=[]
		for w in j:
			g=w["g"]
			if z(g):w["x"],w["y"]=g.GetX(),g.GetY()
			b=w.get("size")or(0,0);a.append("%d,%s,%s,%d,%d,%s,%s,%d,%d"%(w["id"],w["metric"],"overall"if w["seg"]=="overall"else "current",int(w["x"]),int(w["y"]),"1"if w["minimized"]else "0","1"if w.get("graph")else "0",int(b[0]),int(b[1])))
		bn(bs,";".join(a))
	def bS():
		del o[:];b,c=az
		for d in bm(bB).split(";"):
			p=d.split(",")
			if len(p)<5 or not p[0].strip():continue
			try:a=[p[0].strip(),int(p[1]),int(p[2]),int(p[3]),max(b,min(c,int(p[4])))]
			except ValueError:continue
			if all(f[0]!=a[0]for f in o)and len(o)<aS:o.append(a)
	def bT():bn(bB,";".join("%s,%d,%d,%d,%d"%tuple(d)for d in o))
	def cT(text):
		for a in ";,|":text=text.replace(a," ")
		return " ".join(text.split())[:bC]
	def bU(kind,n=0):a=time.time();bM[0]+=1;return{"kind":kind,"n":n,"name":"Fight %d"%n if n else "Overall","start":a,"end":None,"combat":0.,"d":{},"serial":{},"big":[],"fights":0,"uid":bM[0],"ver":0,"tot":{},"place_t":{}}
	def a3():b.clear();b.update({"overall":bU("overall"),"cur":None,"hist":[],"n":0,"last_combat":0.,"c_at":None});a["watch"].clear();a["engaged"].clear();a["pend"],a["orph"]=[],[];C.update({"min":None,"b":None,"ver":C["ver"]+1});C["hist"].clear();C["vb"].clear()
	def aD():a=b["cur"];return(b["overall"],a)if a is not None else(b["overall"],)
	def bV(now):
		m=int(now//60)
		if m!=C["min"]:
			a=C["hist"]
			for k in[d for d in a if d<=m-aA]:del a[k]
			C["min"]=m;C["b"]=a.setdefault(m,{})
		return C["b"]
	def c(b,row,amt,ser=None):
		e=time.time();f=row.endswith(" (%)")
		if not f and(b!="gold"or row=="Gained"):g=bV(e);g[b]=g.get(b,0.)+amt;h=C["vb"];h[b]=h.get(b,0)+1
		for c in aD():
			d=c["d"].get(b)
			if d is None:d=c["d"][b]={}
			r=d.get(row)
			if r is None:
				if len(d)>=cM:cU(c,b,d)
				r=d[row]=[0.,0,amt,amt,e,e]
			r[0]+=amt;r[1]+=1
			if amt>r[2]:r[2]=amt
			if amt<r[3]:r[3]=amt
			r[5]=e
			if ser:c["serial"][(b,row)]=ser
			if not f:i=c["tot"];i[b]=i.get(b,0.)+amt
			c["ver"]+=1
		if amt and any(k["metric"]in(b,"session")and not k["docked"]for k in j):a["changed"]=True
	def cU(seg,a,d):
		b=sorted((abs(g[0]),f)for f,g in d.items()if f!=a_ and not f.endswith(" (%)"));o=d.get(a_);c=seg["serial"]
		for e,k in b[:max(0,len(d)-cN)]:
			r=d.pop(k);c.pop((a,k),None)
			if o is None:o=d[a_]=list(r)
			else:o[0]+=r[0];o[1]+=r[1];o[2],o[3]=max(o[2],r[2]),min(o[3],r[3]);o[4],o[5]=min(o[4],r[4]),max(o[5],r[5])
	def cV(amt,name,ser):
		b=bV(time.time())
		if amt>b.get("big",0.):b["big"]=amt;c=C["vb"];c["big"]=c.get("big",0)+1
		for d in aD():
			a=d["big"]
			if len(a)>=bA and amt<=a[-1][0]:continue
			i=len(a)
			while i>0 and a[i-1][0]<amt:i-=1
			a.insert(i,(amt,name,ser));del a[bA:]
	def N(seg,a):return seg["tot"].get(a,0)
	def bW():
		a=time.time()
		if b["cur"]is None:b["n"]+=1;b["cur"]=bU("fight",b["n"]);b["overall"]["fights"]+=1
		b["last_combat"]=a;b["c_at"]=(b["cur"]["combat"],b["overall"]["combat"])
	def cW(now):
		a=b["cur"]
		if a is None:return
		c=b.get("c_at")
		if c is not None:a["combat"],b["overall"]["combat"]=c
		else:
			f=max(0.,now-b["last_combat"])
			for e in(a,b["overall"]):e["combat"]=max(0.,e["combat"]-f)
		b["c_at"]=None;a["end"]=b["last_combat"];d=a["d"].get("dmg_done",{})
		if d:g=max(d.items(),key=lambda a:a[1][0])[0];a["name"]=g+(" +%d"%(len(d)-1)if len(d)>1 else "")
		b["hist"].insert(0,a);del b["hist"][m["history"]:];b["cur"]=None
	def aE(seg):return max(1.,seg["combat"])
	def aF(seg):return max(1.,(seg["end"]or time.time())-seg["start"])
	def al(seg,a,value):
		if a=="s":return value/aE(seg)
		if a=="m":return value/(aF(seg)/60.)
		return value/(max(60.,aF(seg))/3600.)
	def aG(w):
		s=w["seg"]
		if s=="overall":return b["overall"]
		if s!="current":
			for h in b["hist"]:
				if h["n"]==s:return h
			w["seg"]="current"
		return b["cur"]or(b["hist"][0]if b["hist"]else None)
	cX={"overall":"Overall","current":"Current"}
	def aH(w):return cX.get(w["seg"])or "Fight %d"%w["seg"]
	def cY(seg):
		if seg is None:return ""
		if seg["kind"]=="overall":return D(time.time()-seg["start"])
		return D(aE(seg))
	def bX(a):return abs(a[1][0])
	def Y(seg,v,r,head=l):return "%s (%s/%s)"%(head(v),U(al(seg,r,v)),r)
	def a4(a,seg,e=None):
		r,b,f,r,r=F[a]
		if seg is None:return(["No fight yet."],[])
		i=cY(seg)
		if a=="session":return c0(seg)
		if a=="big":t=seg["big"]if e is None else seg["big"][:e];g=[(G,y,l(y),d4,None)for y,G,d4 in t];c=(["Biggest %s on %s"%(l(seg["big"][0][0]),aJ(seg["big"][0][1],seg["big"][0][2]))]if seg["big"]else["No hits yet."]);return(c+[i],g)
		d=seg["d"].get(a,{})
		if a=="gold":n=d.get("Gained",[0.])[0];o=d.get("Spent / banked",[0.])[0];j=n-o;g=[("Gained",n,Y(seg,n,"h"),None,d.get("Gained")),("Spent / banked",o,l(o),None,d.get("Spent / banked")),("Net",abs(j),Y(seg,j,"h",aj),None,None)];return(["Net %s"%aj(j),"%s per hour"%U(al(seg,"h",j)),i],g)
		if a=="gold_place":return c_(seg,d,e,i)
		h=N(seg,a)
		if e is None:p=sorted(d.items(),key=bX,reverse=True)
		elif e<=0:p=[]
		else:p=heapq.nlargest(e,d.items(),key=bX)
		g=[]
		for q,s in p:
			v=s[0];k=[]
			if b:k.append(U(al(seg,b,v),f)+(""if b=="s"else "/"+b))
			if m["pct"]and h and not ar(q)and v>0:k.append("%d%%"%int(round(100.*v/h)))
			u=(aj(v,f)if a in("skills","stats")else l(v,f));w=u+(" (%s)"%", ".join(k)if k else "");g.append((q,abs(v),w,seg["serial"].get((a,q)),s))
		if a in("skills","stats"):c=["Total %s"%aj(h,f)]
		elif a=="cures":x=N(seg,"cures_mine");c=["Cures %s"%l(h),"by you %s"%l(x)]
		else:c=["Total %s"%l(h,f)]
		if b:c.append("%s %s"%(U(al(seg,b,h),f),bK[b]))
		c.append("in combat "+D(seg["combat"])if b=="s"else i);return(c,g)
	def bY(seg,name,gold):a=seg["place_t"].get(name,0.);return gold/(max(bF,a)/3600.),a
	def cZ(row):return row[1]
	def c_(seg,d,g,dur):
		j=seg["place_t"];c=list(d)
		for k,n in j.items():
			if n>=bF and k not in d:c.append(k)
		e=sum(s[0]for s in d.values());a=[]
		for f in c:
			r=d.get(f);b=r[0]if r is not None else 0.;h,p=bY(seg,f,b);i=[l(b)]
			if m["pct"]and e and b>0:i.append("%d%%"%int(round(100.*b/e)))
			a.append((f,h,"%s/h (%s)"%(U(h),", ".join(i)),None,r))
		a.sort(key=cZ,reverse=True)
		if g is not None:del a[max(0,g):]
		o=len(c);return(["Gained %s"%l(e),Kit.count(o,"place"),dur],a)
	def c0(seg):
		a=aF(seg);c=seg["combat"];f,g,h=N(seg,"dmg_done"),N(seg,"dmg_taken"),N(seg,"heal_done");i,j=N(seg,"kills"),N(seg,"deaths");d=seg["d"].get("gold",{});k=d.get("Gained",[0.])[0]-d.get("Spent / banked",[0.])[0];e=N(seg,"skills");b=[("Time",D(a)),("In combat","%s (%d%%)"%(D(c),int(100*c/a)))]
		if seg["kind"]=="overall":b.append(("Fights","%d"%seg["fights"]))
		b+=[("Damage done",Y(seg,f,"s")),("Damage taken",Y(seg,g,"s")),("Healing done",Y(seg,h,"s")),("Kills",Y(seg,i,"h")),("Deaths",l(j)),("Gold",Y(seg,k,"h",aj)),("Skill gain","%s (%s/h)"%(aj(e,"d1"),U(al(seg,"h",e),"d1"))),("Items gained",l(N(seg,"loot"))),("Spells cast",l(sum(s[1]for n,s in seg["d"].get("spells",{}).items()if n not in("Fizzled","Interrupted","Out of mana"))))];m=[(r,0.,t,None,None)for r,t in b];return([seg["name"]if seg["kind"]=="fight"else "Session",D(a)],m)
	def c1():
		try:
			import clr;clr.AddReference("System.Collections.Concurrent");clr.AddReference("System.Linq.Expressions");from System import Array,Int32,UInt32,Object,EventHandler,Tuple,Type,AppDomain;from System.Reflection import BindingFlags;from System.Collections.Concurrent import ConcurrentQueue;from System.Linq.Expressions import Expression,ParameterExpression;m=BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Static;e=API.GetType().Assembly;n=e.GetType("ClassicUO.Game.Managers.EventSink");f=e.GetType("ClassicUO.Game.GameObjects.Entity");a=n.GetEvent("OnEntityDamage",m);o,b,g=(clr.GetClrType(Object),clr.GetClrType(Int32),clr.GetClrType(UInt32));h=Tuple[UInt32,Int32];q=ConcurrentQueue[h]();c=Expression.Parameter(o,"sender");i=Expression.Parameter(b,"amount");j=Expression.Constant(q);p=Expression.Convert(Expression.PropertyOrField(Expression.Convert(c,f),"Serial"),g);r=clr.GetClrType(h).GetConstructor(Array[Type]([g,b]));s=Expression.Call(j,q.GetType().GetMethod("Enqueue"),Array[Expression]([Expression.New(r,Array[Expression]([p,i]))]));t=Expression.LessThan(Expression.Property(j,"Count"),Expression.Constant(cp,b));u=Expression.IfThen(Expression.AndAlso(Expression.TypeIs(c,f),t),s);d=Expression.Lambda[EventHandler[Int32]](u,Array[ParameterExpression]([c,i])).Compile();k=AppDomain.CurrentDomain;l=k.GetData(aP)
			if l is not None:safe(lambda:a.GetRemoveMethod(True).Invoke(None,Array[Object]([l])))
			a.GetAddMethod(True).Invoke(None,Array[Object]([d]));k.SetData(aP,d);L.update({"q":q,"handler":d,"event":a,"kind":"exact (per mobile)"});return True
		except Exception as v:L.update({"q":None,"handler":None,"event":None});L["kind"]="amounts only (%s)"%(str(v)[:50]or "no hook");return False
	def c2():
		h,a=L.get("handler"),L.get("event")
		if h is None or a is None:return
		with Kit.quiet:from System import Array,Object,AppDomain;a.GetRemoveMethod(True).Invoke(None,Array[Object]([h]));AppDomain.CurrentDomain.SetData(aP,None)
		L.update({"q":None,"handler":None,"event":None,"kind":"not hooked"})
	def c3(*b):
		if not a["active"]:return
		if not a["poked"]:a["poked"]=True;HOST.poke(Q,False)
		if L.get("q")is not None:return
		for c in b:
			try:a["amtq"].append(int(c))
			except Exception:continue
			del a["amtq"][:-200];return
	def c4():
		if not R["tried"]:
			R["tried"]=True
			try:from System.Reflection import BindingFlags;a=BindingFlags.Instance|BindingFlags.Public|BindingFlags.NonPublic;b=API.GetType().GetField("World",a).GetValue(API);c=b.GetType().GetProperty("TargetManager",a).GetValue(b,None);R["tm"],R["la"]=c,c.GetType().GetProperty("LastAttack",a)
			except Exception:R["tm"]=R["la"]=None
		if R["la"]is None:return 0
		return int(R["la"].GetValue(R["tm"],None)or 0)
	def c5(*b):
		if not a["active"]:return
		for c in b:
			try:a["used"].append(int(c));del a["used"][:-30];return
			except Exception:continue
	def c6(*b):
		if not a["active"]:return
		a["died"]=True
		if not a["poked"]:a["poked"]=True;HOST.poke(Q,False)
	def c7(*b):
		if not a["active"]:return
		for c in b:
			t=safe(lambda:c.Title)
			if t:a["buffq"].append(str(t));del a["buffq"][:-50];return
	def c8():
		e=time.time();c={"me":None,"dmg":[],"info":{},"fhp":{},"wst":{},"used":[],"pack":None,"friends":None,"hum":[]};p=HOST.me()
		if p is None:return c
		b=int(p.Serial)
		if b!=a["my_ser"]or e>=a["next_name"]:a["my_name"]=str(p.Name or "");a["my_ser"],a["next_name"]=b,e+cR
		g={"ser":b,"name":a["my_name"],"hits":int(p.Hits),"hmax":int(p.HitsMax),"mana":int(p.Mana),"x":int(p.X),"y":int(p.Y),"gold":int(p.Gold or 0),"dead":bool(p.IsDead),"war":bool(p.InWarMode),"poison":bool(p.IsPoisoned),"map":int(API.GetMap())};c["me"]=g;q=L["q"]
		if q is not None:
			for w in range(cs):
				x,o=q.TryDequeue()
				if not x:break
				c["dmg"].append((int(o.Item1),int(o.Item2)))
		j=a["mobs"];h=c["info"]
		for b,w in c["dmg"]:
			if b not in j and b not in h and b!=g["ser"]:
				d=aq(b);h[b]=str(d.Name or "")if d is not None else ""
				if d is not None and d.IsHuman:c["hum"].append(b)
		c["lt"]=int(API.LastTargetSerial or 0);c["la"]=c4()
		for k in(a["engaged"],(c["lt"],c["la"])):
			for b in k:
				if ak(b)and b not in j and b not in h and b!=g["ser"]:
					d=aq(b)
					if d is not None:
						h[b]=str(d.Name or "")
						if d.IsHuman:c["hum"].append(b)
		if e>=a["next_friends"]:
			a["next_friends"]=e+cf;r=[int(G)for G in API.GetPartyMemberSerials()or[]];s=cS();t=[int(d4)for d4 in API.GetAllFriends()or[]];c["friends"]=(r,s,t);i,u=[],set()
			for k in(t,s,r):
				for f in k:
					if f!=g["ser"]and f not in u:
						u.add(f)
						if aq(f)is not None:i.append(f)
		else:i=None
		y=c["friends"]is not None;z=c["fhp"]
		for b in a["present"]:
			d=aq(b)
			if d is not None:A=None if y else j.get(b);z[b]=(int(d.Hits),int(d.HitsMax),bool(d.IsPoisoned),bool(d.IsDead),A or str(d.Name or ""))
		if i is not None:a["present"]=i
		l=c["wst"]
		for b,B in a["watch"].items():
			if e-B["t"]>cq:continue
			if aq(b)is not None:l[b]="alive"
			elif API.FindMobile(b|cj)is not None:l[b]="dying"
			else:l[b]="gone"
		if a["used"]:
			C,a["used"]=a["used"],[]
			for b in C:
				n=API.FindItem(b)
				if n is not None:c["used"].append((int(n.Graphic),str(n.Name or "")))
		if not m["scan"]:a["pscan"]=None
		elif a["pscan"]is None and e>=a["next_scan"]:
			a["next_scan"]=e+cg
			if API.Backpack:a["pscan"]=[HOST.pack_items(True),0,[],0,0,e]
		v=a["pscan"]
		if v is not None:c["pack"]=c9(v,e)
		return c
	def c9(e,now):
		m,i,g,h,j,n=e;o=len(m);p=min(o,i+cQ)
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
	def a5(ser):b=a["me"];return(b is not None and ser==b["ser"])or ser in a["friendly"]
	def aI(ser):
		b=a["me"]
		if b is not None and ser==b["ser"]:return b["name"]or "You"
		return a["mobs"].get(ser)or "Unknown"
	def aJ(name,ser=None):
		if not Kit.streamer or not name:return name
		b=name[:-4]if ar(name)else name;c=a["me"]
		if c is not None and b==c["name"]:return Kit.veil("me",b)+name[len(b):]
		if b.lower()not in X:return name
		return Kit.veil("name",b,ser if ak(ser)else Kit.checksum(b.lower().encode("utf-8")))+name[len(b):]
	def bZ(ser,now):t=a["engaged"].get(ser);return t is not None and now-t<=m["engage"]
	def at(now,kind,method,secs):
		b=kind=="cure+";kind="cure"if b else kind
		for o in list(a["orph"]):
			if o[1]==kind and now-o[0]<=bz:
				a["orph"].remove(o);b_(kind,method,o[2],o[3],o[4])
				if not b:return
		a["pend"].append([now+secs,kind,method,b])
	def b_(kind,method,ser,name,amt):
		if kind=="heal":
			c("heal_done",name,amt,ser)
			if not ar(name):c("heal_by",method,amt)
		else:c("cures_mine",method,1)
	def b0(kind,now,ser,name,amt):
		for p in a["pend"]:
			if p[1]==kind and now<=p[0]:
				if not p[3]:a["pend"].remove(p)
				b_(kind,p[2],ser,name,amt);return
		a["orph"].append((now,kind,ser,name,amt))
	def da():
		b=set()
		for c in aD():
			for d in c["d"].values():b.update((f[:-4]if ar(f)else f).lower()for f in d)
			b.update(str(g[1]).lower()for g in c["big"])
		if a["recap"]is not None:b.update(str(i[2]).lower()for i in a["recap"]["rows"])
		e=[n for n in X if n in b][-(aR//2):];X.clear();X.update((r,True)for r in e)
	def db(s,now):
		d=s["me"]
		if d is None:return
		f,a["me"]=a["me"],d;g=a["mobs"]
		if len(g)>aR:g.clear()
		if len(X)>aR:g.clear();da()
		for b,e in s["info"].items():
			if e:g[b]=e
		for b in s["hum"]:
			if g.get(b):X[g[b].lower()]=True
		if a["pend"]:a["pend"]=[d4 for d4 in a["pend"]if d4[0]>=now]
		if a["orph"]:a["orph"]=[d5 for d5 in a["orph"]if now-d5[0]<=bz]
		if s["friends"]is not None:
			J,N,K=s["friends"];B={}
			for O,P in(("friend",K),("pet",N),("party",J)):
				for b in P:B[b]=O
			for b in K+J:
				r=s["fhp"][b][4]if b in s["fhp"]else g.get(b)
				if r:X[r.lower()]=True
			B.pop(d["ser"],None);a["friendly"]=B
		l,t=s.get("lt",0),s.get("la",0)
		if t and d["war"]and ak(t)and not a5(t):a["engaged"][t]=now
		if(ak(l)and not a5(l)and(l!=a["prev_lt"]or now-a["cast_t"]<=2.)):a["engaged"][l]=now
		a["prev_lt"]=l
		if a["engaged"]:
			for b in[d6 for d6,d7 in a["engaged"].items()if now-d7>m["engage"]]:a["engaged"].pop(b,None)
		C=0
		if f is not None and d["hits"]<f["hits"]:C=f["hits"]-d["hits"]
		for b,Q in s["dmg"]:a6(b,Q,now)
		if a["amtq"]:
			u=None
			for h in a["amtq"]:
				if C>=h:C-=h;a6(d["ser"],h,now)
				else:
					if u is None:u=max(a["engaged"].items(),key=lambda a:a[1])[0]if a["engaged"]else 0
					a6(u,h,now)if u else c("dmg_nearby","Unknown",h)
			a["amtq"]=[]
		v=s["fhp"];v[d["ser"]]=(d["hits"],d["hmax"],d["poison"],d["dead"],d["name"]or "You")
		for b,(L,x,D,E,e)in v.items():
			if e:g[b]=e
			e=aI(b);i=a["prev"].get(b);a["prev"][b]=(L,x,D,E)
			if i is None:continue
			if E and not i[3]:
				if now-a["dead_seen"].get(b,0)>10:
					c("deaths",e,1,b);a["dead_seen"][b]=now
					if b==d["ser"]and m["recap"]:b2(now)
				continue
			if E or i[3]:continue
			F=b==d["ser"]or a["friendly"].get(b)=="party"or x not in(25,100);G=L-i[0]
			if G>=(m["min_heal"]if F else 1)and x==i[1]:y=e if F else e+" (%)";h=G if F else G*100./max(1,x);c("heal_taken",y,h,b);b0("heal",now,b,y,h)
			if D and not i[2]:c("poisoned",e,1,b)
			elif i[2]and not D:c("cures",e,1,b);b0("cure",now,b,e,1)
		if len(a["prev"])!=len(v):
			for b in[d8 for d8 in a["prev"]if d8 not in v]:a["prev"].pop(b,None)
		for b,R in s["wst"].items():
			w=a["watch"].get(b)
			if w is None:continue
			if R=="dying":
				a["watch"].pop(b,None)
				if w["friend"]:
					if now-a["dead_seen"].get(b,0)>10:c("deaths",w["name"],1,b);a["dead_seen"][b]=now
				elif w["mine"]and now-w["mine"]<=ch:c("kills",w["name"],1)
		if a["watch"]:
			for b in[d9 for d9,ea in a["watch"].items()if now-ea["t"]>bw]:a["watch"].pop(b,None)
		if a["dead_seen"]:
			for b in[eb for eb,ec in a["dead_seen"].items()if now-ec>30]:a["dead_seen"].pop(b,None)
		j=a["hp_log"]
		if not j or j[-1][1]!=d["hits"]or j[-1][2]!=d["hmax"]:
			j.append((now,d["hits"],d["hmax"]))
			if len(j)>bH:del j[:len(j)-bH]
		if f is not None and d["mana"]<f["mana"]and not d["dead"]:H=a["last_spell"];y=H[1]if H is not None and now-H[0]<=co else "Other";c("mana",y,f["mana"]-d["mana"])
		if f is not None and f["ser"]==d["ser"]:
			n=d["gold"]-f["gold"]
			if n>0:c("gold","Gained",n);c("gold_place",a["place"]or bE,n)
			elif n<0:c("gold","Spent / banked",-n)
		S=(d["x"],d["y"],d["map"])
		if m["travel"]and a["pos"]is not None and(d["x"]or d["y"]):
			T,U,V=a["pos"];I=max(abs(d["x"]-T),abs(d["y"]-U))
			if V!=d["map"]or I>ci:c("travel","Recalls, gates & teleports",1)
			elif I>0:c("travel","Tiles walked",I)
		a["pos"]=S
		for W,e in s["used"]:
			o=cK.get(W)
			if o is None:continue
			Y=o[0]+" potion";c("consum",Y,1)
			if o[1]:at(now,o[1],o[0]+" potion",cm)
		p=s["pack"]
		if p is not None:
			q=a["pack"];Z=q is not None and len(q)==0 and len(p)>0
			if q is not None and not Z:
				for k,M in p.items():
					z=q.get(k);A=M[0]-(z[0]if z else 0)
					if A>0 and k[0]!=ck:r=cP.sub("",(M[1]or "").strip())or "Item 0x%04X"%k[0];c("loot",r.title(),A)
					elif A<0 and k[0]in aC:c("consum",aC[k[0]],-A)
				for k,z in q.items():
					if k not in p and k[0]in aC:c("consum",aC[k[0]],z[0])
			a["pack"]=p
		if a["buffq"]:
			for aa in a["buffq"]:c("buffs",aa,1)
			a["buffq"]=[]
	def a6(ser,dmg,now):
		d=a["me"];b=aI(ser);c("dmg_nearby",b,dmg,ser);w=a["watch"].get(ser)
		if w is None:
			if len(a["watch"])>=cr:e=min(a["watch"].items(),key=lambda a:a[1]["t"])[0];a["watch"].pop(e,None)
			w=a["watch"][ser]={"name":b,"t":now,"mine":0.,"friend":False}
		w["t"],w["name"]=now,b
		if a5(ser):
			w["friend"]=ser!=d["ser"];c("dmg_taken",b,dmg,ser);bW()
			if ser==d["ser"]:dj(dmg,now)
		elif bZ(ser,now):a["engaged"][ser]=now;w["mine"]=now;c("dmg_done",b,dmg,ser);cV(dmg,b,ser);bW()
	def dc(now):
		g=a["me"];e=g["name"]if g else None
		for h in a["jr"].new():
			f=h.name;b=h.low.strip()
			if e and f==e:
				d=bJ.get(b)
				if d is not None:
					c("spells",d[0],1);a["last_spell"]=(now,d[0]);a["cast_t"]=now
					if d[1]=="heal":at(now,"heal",d[0],cl)
					elif d[1]in("cure","cure+"):at(now,d[1],d[0],cn)
				continue
			if b.startswith(cO):continue
			if b.startswith(cE):c("spells","Fizzled",1)
			elif b.startswith(cF):c("spells","Interrupted",1)
			elif b.startswith(cG):c("spells","Out of mana",1)
			elif b.startswith(cB):c("consum","Bandages",1)
			elif b.startswith(cD):at(now,"cure","Bandage",by)
			elif b.startswith(cC):at(now,"heal","Bandage",by)
			else:
				if f and e:
					d=bJ.get(b)
					if d is not None:
						if d[0]in cA:dh(now,f,d[0])
						continue
				if "your skill in"in b:
					m=cH.search(b)
					if m:v=float(m.group(3));c("skills",m.group(1).strip().title(),v if m.group(2).lower()=="increased"else-v);continue
				if "your "in b and " has "in b:
					m=cI.search(b)
					if m:v=int(m.group(3));c("stats",m.group(1).title(),v if m.group(2).lower()=="increased"else-v);continue
				if "you have "in b and("fame"in b or "karma"in b):
					m=cJ.search(b)
					if m:c("fame","%s %s"%(m.group(2).title(),m.group(1).lower()),1)
	def dd(me):
		c=HOST.guard_area()
		if c:return str(c)
		a=None;x,y,m=me["x"],me["y"],me["map"]
		for b in o:
			if b[3]==m:
				d=max(abs(x-b[1]),abs(y-b[2]))
				if d<=b[4]and(a is None or d<a[0]):a=(d,b[0])
		return a[1]if a is not None else bE
	def de(now,e):
		b=a["me"]
		if b is None:return
		if a["place"]is None or now>=a["next_place"]:a["next_place"]=now+ct;a["place"]=dd(b)
		c=a["place"]
		for f in aD():d=f["place_t"];d[c]=d.get(c,0.)+e
	def df(name,radius):
		b=a["me"]
		if b is None or not(b["x"]or b["y"]):H("position unknown; try again.",am);return
		name=cT(name)or "Spot %d"%(len(o)+1);d,e=az;radius=max(d,min(e,int(radius)));c=[g for g in o if g[0].lower()==name.lower()]
		if not c and len(o)>=aS:H("%d spots at most; remove one first."%aS,am);return
		for f in c:o.remove(f)
		o.append([name,b["x"],b["y"],b["map"],radius]);bT();a["place"]=None;H("spot \"%s\" named here (%d, %d), %d tiles round."%(name,b["x"],b["y"],radius),aw);bh(Q)
	def b1(name):
		n=len(o);o[:]=[d for d in o if d[0]!=name]
		if len(o)!=n:bT();a["place"]=None;bh(Q)
	def dg(now):
		b=a["fnames"]
		if b is not None and b[0]==now:return b[1]
		c=a["mobs"];d=set(c.get(f)for f in a["friendly"]if c.get(f));a["fnames"]=(now,d);return d
	def dh(now,name,spell):
		if name in dg(now):return
		c=Kit.spell_info(spell);d=float(c[3])if c else 0.;b=a["casts"];b.append([now,name,spell,False,d])
		while b and(len(b)>cy or now-b[0][0]>b[0][4]+bI):b.pop(0)
	def di(now):
		for c in a["casts"]:
			f=now-c[0]
			if not c[3]and c[4]-cz<=f<=c[4]+bI:c[3]=True;return "%s: %s"%(c[1],c[2]),c[1],0
		b=None
		for g,t in a["engaged"].items():
			if b is None or t>b[1]:b=(g,t)
		if b is not None and bZ(b[0],now):d=aI(b[0]);return d+"?",d,b[0]
		e=a["me"]
		if e is not None and e["poison"]:return "Poison",None,0
		return "Unknown",None,0
	def dj(dmg,now):
		c=a["me"];d,e,f=di(now);b=a["taken"];b.append((now,dmg,d,e,f,c["hits"],c["hmax"]))
		if len(b)>bG:del b[:len(b)-bG]
	def b2(now):
		e=now-ap;f=[n for n in a["taken"]if n[0]>=e];c,d=[],None
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
	def dk(now):
		b=a["me"]
		if b is None or now-a["dead_seen"].get(b["ser"],0)<=10:return
		c("deaths",aI(b["ser"]),1,b["ser"]);a["dead_seen"][b["ser"]]=now
		if m["recap"]:b2(now)
	def dl(w):
		c=aG(w);e=aH(w)
		if c is None:c,e=b["overall"],"Overall"
		f=a["me"];j=f["ser"]if f else int(safe(lambda:API.Player.Serial,0)or 0);k=Kit.data_path(aV%j);g=c["name"]if e!=c["name"]else "";d=["Meters export: %s%s, %s"%(e," (%s)"%g if g else "",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),("Session time %s, in combat %s"%(D(aF(c)),D(c["combat"]))if c["kind"]=="overall"else "Fight time %s"%D(aE(c))),""]
		for h in ah:
			l,i=a4(h,c,cu);d.append("== %s =="%F[h][0]);d.append("   "+"   ".join(n for n in l if n))
			for m,r in enumerate(i):d.append("   %2d. %-30s %s"%(m+1,r[0],r[2]))
			if not i:d.append("   (nothing)")
			d.append("")
		a["to_write"].append((k,"\n".join(d)+"\n",e))
	def dm():
		while a["to_write"]and not a["shutting"]:
			b,c,d=a["to_write"].pop(0)
			try:
				with open(b,"w")as e:e.write(c)
				H("%s exported to %s."%(d,b),aw)
			except Exception as f:H("couldn't write %s (%s)."%(b,f),am)
	M=ac
	def I(w):return Q if w["id"]==0 else "%s_%d"%(Q,w["id"])
	def Z(w):return af if w["id"]==0 else "%s %d"%(af,w["id"]+1)
	def dn(w,g):
		def b(*b):
			if w["g"]is g and not a["shutting"]:
				w["g"]=None
				if w["id"]==0:HOST.disable(Q)
				else:h.add(("closed",w["id"]),dup=True)
		return b
	def do(w,slot,g):
		def a(*a):
			if w.get(slot)is g:w[slot]=None
		return a
	def dp(w,i):
		def a(*c):
			a=w["slots"]
			if i>=len(a):return
			b=a[i].get("ser")
			if bf():
				if b:h(("follow",b))()
				return
			h(("detail",w["id"],i))()
		return a
	def b3(w):n=8+35+p("New")+14+35+p("Report")+8;return n+14+35+p("Reset")if w["id"]==0 else n
	def A(w):
		x,y=w["x"],w["y"];C=w["g"]
		if z(C):x,y=C.GetX(),C.GetY()
		w["g"]=None;f,i,ae,af=({},{}),{},[],[];ah=w["metric"];ai=("Close "+Z(w)+(" (this window only)"if w["id"]else " (turns it off; the Modules tab turns it back on)"));w["resize_at"],w["preview"]=0.,False
		if w["minimized"]:g=G.CreateGump(True,True);a,b=bt,ca;i["status"]=Kit.mini_bar(g,f,a,b,Z(w),I(w),h(("toggle_min",w["id"])),close_tip=ai)
		else:
			j=m["rows"];n=M+30+B;d=n+30+B;o=56+(aU if w.get("graph")else 0);ar=b3(w);D=w["fit"];t=D if D is not None else w["size"];at=(max(120,t[0])if t else W)-2*M;aj=ar>at
			if aj:o+=26
			k=o+j*K;a,b=W,d+k+M
			if t is not None:
				a,b=max(120,t[0]),t[1];j=max(1,(b-d-M-o)//K);k=max(o+j*K,b-d-M)
				if D is not None:k=max(30,min(k,b-d-M));j=max(0,(k-o)//K)
				b=d+k+M
			c=a-2*M
			if D is None:x,y=Kit.clamp(x,y,a,b);au=d+o+K+M;g=G.CreateModernGump(x,y,a,b,True,min(ax,a),min(au,b),dq(w));g.SetAlpha(0)
			else:g=G.CreateGump(True,True)
			bk(g,a,b,mouse=False);av=0 if Kit.zone_up(I(w))else 84+Kit.DOCK_DX;aw=(ac+30+p(Z(w).upper())+16+av+35+p("Settings")+ac);Kit.title_bar(g,f,a,Z(w),I(w),h(("toggle_min",w["id"])),h(("to_bar",w["id"])),h(("settings",))if a>=aw else None,close_tip=ai);S(g,M,n,c,30);N=M+8;O(g,f,"prev",cc,N,n+4,None,"Show previous display",on_click=h(("step",w["id"],-1)));O(g,f,"next",Kit.ART_PLAY,N+32,n+4,None,"Show next display",on_click=h(("step",w["id"],1)));H,ay,ay,ak,al=F[ah];Q=N+68;R=H if Q+35+p(H)+10+35+40<=M+c-6 else None;O(g,f,"pick",ab,Q,n+4,R,"Pick what this window shows"+(""if R else " (now: %s)"%H),on_click=h(("picker",w["id"])));J=Q+(35+p(H)if R else 30)+10;i["seg_room"],i["iw"]=max(20,M+c-6-J-35),c;az=u(aH(w),i["seg_room"]);i["seg"]=O(g,f,"segs",ab,J,n+4,az,"Pick a segment: current fight, Overall or an earlier fight",on_click=h(("segpick",w["id"])));S(g,M,d,c,k);i["head"]=e(g,"",M+8,d+5,q);am="Alt+click: auto-follow (again to stop)"
			if ah in("session","big","gold"):an=am if al else None
			else:an="Show this row's details"+(". "+am if al else "")
			U=min(bu,int(c*.45));aB=c-12-U-10
			for l in range(j):v=d+26+l*K;L=G.CreateGumpSimpleProgressBar(c-12,K-2,cd,ak,0,100);L.SetPos(M+6,v);L.SetAcceptMouseInput(False);g.Add(L);ln=e(g,"",M+10,v+1,P);lv=e(g,"",M+c-6-U,v+1,P);ae.append({"bar":L,"name":ln,"val":lv,"ser":None,"key":None,"prog":None,"nw":aB,"vw":U})
			for l in range(j):v=d+26+l*K;ad(g,M+6,v,c-12,K-2,dp(w,l),an)
			r=d+26+j*K+4
			if w.get("graph"):
				gy=r-2;i["gcap"]=e(g,"",M+10,gy,q);ap=gy+18+aT;aq=max(1,min(aA,(c-12)//(ag+1)));gx=M+6+(c-12-aq*(ag+1))//2
				for l in range(aq):A=G.CreateGumpColorBox(.9,ak);A.SetRect(gx+l*(ag+1),ap-1,ag,1);A.IsVisible=False;A.SetAcceptMouseInput(False);g.Add(A);af.append({"box":A,"x":gx+l*(ag+1),"h":0})
				i["gbase"]=ap;r+=aU
			O(g,f,"new",ab,M+8,r,"New","Open another window (up to %d)"%ao,on_click=h(("new",)));rx=M+8+35+p("New")+14;O(g,f,"report",ab,rx,r,"Report","Post the top %d rows to party chat (if set and in a party), else the journal"%aO,on_click=h(("report",w["id"])))
			if w["id"]==0:aC=r+26 if aj else r;O(g,f,"reset",aa,a-M-8-35-p("Reset"),aC,"Reset","Clear all meters; new session",on_click=h(("reset",)))
		w["x"],w["y"]=bp(g,x,y,a,b,I(w),w["minimized"]and w["docked"],dn(w,g),E,w,{"g":g,"c":i,"store":f,"slots":ae,"vkey":None,"gcols":af,"gkey":None,"drawn":(a,b)})
		for aD in("picker","segpick","detail"):
			s=w.get(aD)
			if z(s)and not w["minimized"]:
				X=Kit.scroll_info(s)
				if X is not None:Y,sh=int(X["w"]),int(X["h"])
				else:Y,sh=int(s.GetWidth()or V),int(s.GetHeight()or 200)
				J,sy=a7(w,Y);Kit.place(s,J,sy,Y,sh);bl(s,g)
		bd(w);T(C)
	def dq(w):
		def a(*a):
			w["resize_at"]=time.time();g=w["g"]
			if w["preview"]or w["fit"]is not None or w["minimized"]or not z(g):return
			if(int(g.GetWidth()),int(g.GetHeight()))!=w["drawn"]:w["preview"]=True;g.SetAlpha(.55)
		return a
	def dr(w):
		g=w["g"];w["preview"]=False
		if not z(g)or w["minimized"]:return
		b,a=int(g.GetWidth()),int(g.GetHeight())
		if w["fit"]is not None:
			g.SetAlpha(0)
			if(b,a)!=w["drawn"]:A(w)
			return
		c=w["drawn"]or(0,0)
		if abs(b-c[0])<=2 and abs(a-c[1])<=2:g.SetAlpha(0);return
		d=bo()[1]
		if d>0:a=min(a,d)
		w["size"]=bQ(b,a);A(w);E()
	def a7(w,width):
		g=w["g"];r=Kit.rect(g)if z(g)else None;x,y=(r[0],r[1])if r is not None else(w["x"],w["y"]);b=bo()[0];a=x+((w.get("drawn")or(W,0))[0])+4
		if b and a+width>b:a=max(0,x-width-4)
		return a,y
	def aK(width,a,title,store,b,action,g=None):
		if g is None:g=G.CreateGump(True,True)
		bk(g,width,a);S(g,M,M,width-2*M,30);e(g,title,M+30,M+7,an);O(g,store,b,aa,width-M-54,M+4,None,"Close this window",on_click=h(action));return g
	def a8(w,slot):T(w[slot]);w[slot]=None
	def a9(w,slot,g,width,a):b,c=a7(w,width);bp(g,b,c,width,a,None,False,do(w,slot,g),None,w,{slot:g});bl(g,w["g"])
	def ba(w):
		a8(w,"picker");a=V-2*M;c=(a-24)//2;f=[28+((len(v)+1)//2)*22+6 for x,v in aX];i=28+2*22+6;j=M+30+sum(G+B for G in f)+i+B+M;g=aK(V,j,"DISPLAYS",({},{}),"pclose",("close_sub",w["id"],"picker"));y=M+30+B
		for(r,s),k in zip(aX,f):
			S(g,M,y,a,k,r)
			for l,b in enumerate(s):m=M+12+(l%2)*(c+12);n=y+28+(l//2)*22;t=an if b==w["metric"]else P;e(g,u(F[b][0],c-4),m,n,t);ad(g,m-2,n-2,c,20,h(("metric",w["id"],b)),"Show %s in this window"%F[b][0])
			y+=k+B
		S(g,M,y,a,i,"THIS WINDOW");o=bool(w.get("graph"));d="on"if o else "off";e(g,u("Last-hour graph",a-36-p(d)),M+12,y+28);e(g,d,M+a-12-p(d),y+28,aw if o else q);ad(g,M+8,y+26,a-16,20,h(("graph",w["id"])),"Show or hide the last hour under the rows, one bar per minute");e(g,u("Export this segment",a-24),M+12,y+50);ad(g,M+8,y+48,a-16,20,h(("export",w["id"])),"Write every display to %s in the VirtueAssistantSettings folder"%(aV.replace("%08X","<serial>")));a9(w,"picker",g,V,j)
	def ds(w):
		a8(w,"segpick");c=V-2*M;d=[("current","Current fight"+(" (going on)"if b["cur"]else " (or the last)"),""),("overall","Overall (session)",D(time.time()-b["overall"]["start"]))]
		for a in b["hist"]:d.append((a["n"],"#%d  %s"%(a["n"],a["name"]),"%s  %s"%(D(aE(a)),l(N(a,"dmg_done")))))
		i=28+len(d)*22+6;j=M+30+B+i+M;g=aK(V,j,"SEGMENTS",({},{}),"sclose",("close_sub",w["id"],"segpick"));y=M+30+B;S(g,M,y,c,i,"WHAT TO SHOW  (fight time, damage done)");k=110
		for o,(m,p,n)in enumerate(d):
			f=y+28+o*22;r=an if m==w["seg"]else P;e(g,u(p,c-24-k-6),M+12,f,r)
			if n:e(g,n,M+c-12-k,f,q)
			ad(g,M+8,f-2,c-16,20,h(("seg",w["id"],m)),"Show this segment")
		a9(w,"segpick",g,V,j)
	au=("Total","Share","Rate","Times","Average","Biggest","Smallest","First","Last")
	def dt(w):
		a8(w,"detail");a=ay-2*M;b=30+len(au)*20+6;d=M+30+B+b+M;g=aK(ay,d,"DETAILS",({},{}),"dclose",("close_sub",w["id"],"detail"));c={};y=M+30+B;S(g,M,y,a,b);c["name"]=e(g,"",M+10,y+6,an);f=max(p(k)for k in au)+14
		for i,t in enumerate(au):h=y+30+i*20;e(g,t,M+10,h,q);c[t]=e(g,"",M+10+f,h,P)
		c["vw"]=a-20-f;w["dc"]=c;a9(w,"detail",g,ay,d);aL(w)
	def du(w):
		a=w["metric"];m=int(time.time()//60);f=(a,m,C["ver"],C["vb"].get(a,0))
		if f==w["gkey"]:return
		w["gkey"]=f;k=C["hist"];d=[];b=0.
		if a!="session":
			n=m-aA+1
			for i in range(aA):
				g=k.get(n+i);v=g.get(a,0.)if g is not None else 0.
				if v>b:b=v
				d.append(v)
		o=w["c"]["gbase"];p=len(d)-len(w["gcols"])
		for i,c in enumerate(w["gcols"]):
			v=d[i+p]if d else 0.;h=int(round(aT*v/b))if b>0 and v>0 else 0
			if v>0 and h<1:h=1
			if h!=c["h"]:
				j=c["box"]
				if h:Kit.ui_rect(j,c["x"],o-h,ag,h)
				if(h>0)!=(c["h"]>0):j.IsVisible=h>0
				c["h"]=h
		if a=="session":e="No graph for the summary"
		elif b<=0:e="Last hour, per minute: nothing yet"
		else:e="Last hour, %s per minute: peak %s"%("biggest hit"if a=="big"else "gained"if a in("gold","gold_place")else "total",l(b,F[a][2]or "n"))
		J(w["c"]["gcap"],u(e,w["c"].get("iw",W-2*ac)-20))
	def av(a,k,text,width):
		f=a.get(k)
		if f is not None and f[0]==text and f[1]==width:return f[2]
		b=u(text,width);a[k]=(text,width,b);return b
	def dv(i):
		def a(*b):
			a=bL["rows"]
			if i<len(a)and a[i]and bf():h(("follow",a[i]))()
		return a
	def dw(hp,t):
		a=hp[0]if hp else(t,0,0)
		for h in hp:
			if h[0]>t:break
			a=h
		return a[1],a[2]
	def bb():
		b=a["recap"]
		if b is None:return
		c=aB-2*M;k=b["rows"][-cv:];d=30;m=30+20+d+8+max(1,len(k))*20+2*18+6;w=M+30+B+m+M;g,F,Q=bc.begin(aB,w,a7(j[0],aB)if j else None);aK(aB,w,"DEATH RECAP",F,"close",("recap_close",),g);h=M+30+B;S(g,M,h,c,m,"LAST %d SECONDS  (damage you took)"%int(ap));H=len(b["rows"]);I="Died %s: %s damage in %s"%(time.strftime("%H:%M:%S",time.localtime(b["t"])),l(b["total"]),Kit.count(H,"hit"));e(g,u(I,c-20),M+10,h+26,P);n=h+26+20;e(g,"HP",M+10,n+(d-16)//2,q);x=M+10+p("HP")+8;y=max(2,(M+c-10-x)//aW);J=b["t"]-ap
		for i in range(aW):
			o,r=dw(b["hp"],J+(i+1)*ap/aW);s=int(round(d*max(0,o)/float(r)))if r>0 else 0
			if s>0:z=G.CreateGumpColorBox(.9,"#c22d2d");z.SetRect(x+i*y,n+d-s,max(1,y-1),s);g.Add(z)
		A=n+d+8;t=[]
		if not k:e(g,"No damage seen.",M+10,A,q)
		C,D=M+60,c-166
		for i,(K,L,N,v,o,r)in enumerate(k):
			f=A+i*20;e(g,"-%.1fs"%max(0.,b["t"]-K),M+10,f,q);e(g,u(aJ(N,v),D),C,f,P);E="-%s"%l(L);e(g,E,M+c-64-p(E),f,am);e(g,"HP %d"%o,M+c-58,f,q);t.append(v if ak(v)else 0)
			if t[-1]:ad(g,C-2,f-2,D+4,20,dv(i),"Alt+click: auto-follow (again to stop)")
		for i,O in enumerate(cx):e(g,u(O,c-20),M+10,h+m-40+i*18,q)
		bc.end(g,{"rows":t})
	bc=Kit.Window(Q,af,None,bL,bb,cw,cleanup=a0,names=None,lock=False,owner=False,clear={"rows":[]});d3=None
	def bd(w):
		r=w["g"]
		if not z(r):return
		e=w["metric"]
		if w.get("gcols")and not w["minimized"]:du(w)
		c=aG(w);n=a["me"];h=n["name"]if n else None;f=None
		if c is not None:
			if c["end"]is not None:f=(e,w["seg"],c["uid"],c["ver"],w["minimized"],m["rank"],m["pct"],h)
			elif F[e][1]=="s":f=(e,w["seg"],c["uid"],c["ver"],c["combat"],w["minimized"],m["rank"],m["pct"],h)
			if f is not None and f==w.get("vkey"):aL(w);return
		w["vkey"]=f;o,i=a4(e,c,0 if w["minimized"]else len(w["slots"]));d=w["c"]
		if w["minimized"]:
			p=d.get("status")
			if p is not None:J(p,av(d,"_fst","%s: %s  %s"%(Z(w),F[e][0],"  ".join(o[:2])),bt-90))
			return
		J(d["head"],av(d,"_fhd","   ".join(G for G in o if G),d.get("iw",W-2*ac)-16));J(d["seg"],av(d,"_fsg",aH(w),d.get("seg_room",400)));s=max([d4[1]for d4 in i]+[0.])
		for j,b in enumerate(w["slots"]):
			if j<len(i):k,t,u,l,y=i[j];q=aJ(k,l);v=("%d. %s"%(j+1,q))if m["rank"]else q;x=an if(h and k==h)else P;J(b["name"],av(b,"_fn",v,b["nw"]),x);J(b["val"],av(b,"_fv",u,b.get("vw",bu)));g=(float(t),float(s or 1.));b["ser"],b["key"]=(l if ak(l)else None),k
			else:J(b["name"],"");J(b["val"],"");g=(0.,1.);b["ser"],b["key"]=None,None
			if g!=b["prog"]:b["prog"]=g;b["bar"].SetProgress(g[0],g[1])
		aL(w)
	def aL(w):
		if not z(w["detail"]):return
		d=w["dc"];a,c=w["detail_metric"],w["detail_row"];b=aG(w);r=b["d"].get(a,{}).get(c)if(b is not None and a)else None;m=b["serial"].get((a,c))if b is not None and a else None;J(d["name"],u("%s (%s)"%(aJ(c,m)or "",F.get(a,("",))[0]),ay-2*ac-20));e=dict((s,"")for s in au)
		if r is not None:
			j,g,f,j,j=F[a];k=time.time();h=N(b,a)
			if a=="gold_place":n,o=bY(b,c,r[0]);i="%s/h (%s there)"%(U(n),D(o))
			elif g:i="%s %s"%(U(al(b,g,r[0]),f),bK[g])
			else:i="-"
			e.update({"Total":l(r[0],f),"Share":("%d%% of %s"%(int(round(100.*r[0]/h)),l(h,f))if h and not ar(c)else "-"),"Rate":i,"Times":"%d"%r[1],"Average":l(r[0]/max(1,r[1]),f),"Biggest":l(r[2],f),"Smallest":l(r[3],f),"First":"%s ago"%D(k-r[4]),"Last":"%s ago"%D(k-r[5])})
		elif c:e["Total"]="nothing in this segment"
		for t in au:J(d[t],u(e[t],d["vw"]))
	def aM():return bool(SNAP.drag)or SNAP.pressed()is True
	def dx(w):
		def a(fw,fh,mode):
			a=(int(fw),int(fh))if(fw is not None and fh is not None)else None
			if a!=w.get("fit")or(mode=="again"and a is not None):w["fit"]=a;h(("redraw",w["id"]))()
		return a
	def dy(w):
		def a():a=56+(aU if w.get("graph")else 0)+(26 if b3(w)>ax-2*M else 0);return ax,M+30+B+30+B+a+K+M
		return a
	def dz():
		if aM():return
		for w in j:
			g=w["g"]
			if w["minimized"]or w["docked"]or w["resize_at"]or not z(g):continue
			a=HOST.layout_slot(I(w))
			if a is not None:
				a=(int(a[0]),int(a[1]));b=w["fit"]
				if b is None or abs(b[0]-a[0])>4 or abs(b[1]-a[1])>4:w["fit"]=a;A(w);continue
				if w["drawn"]is None or w["drawn"][0]!=max(120,b[0]):A(w);continue
				c=(int(g.GetWidth()),int(g.GetHeight()))
				if abs(c[0]-w["drawn"][0])>2 or abs(c[1]-w["drawn"][1])>2:
					w["misfit"]=w.get("misfit",0)+1
					if w["misfit"]in(2,6,20):A(w)
				else:w["misfit"]=0
			elif w["fit"]is not None and not HOST.layout_holds(I(w)):w["fit"]=None;A(w)
	def be(w):a=Kit.dock_hooks(Z(w),cb,w,w,h(("redraw",w["id"])),fit=dx(w));a.update({"exact":True,"verify":True,"pieces_out":True,"min":dy(w)});HOST.dock_add(I(w),a)
	def b4(w,remove):
		w["shutting"]=True;HOST.dock_remove(I(w))
		if remove:bg(I(w))
		for k in("picker","segpick","detail","g"):g,w[k]=w[k],None;T(g)
		if remove and w in j:j.remove(w)
	def dA(w):
		d=w["metric"];h=aG(w);b,i=a4(d,h,aO);c="%s (%s)"%(F[d][0],aH(w));e=["%d. %s %s"%(n+1,k[0],k[2])for n,k in enumerate(i[:aO])]
		if m["party"]and API.GetPartyMemberSerials():
			f="; ".join(e)or "nothing yet";g="%s: %s; %s"%(c,"  ".join(b[:2]),f);j=[g]if len(g)<=aQ else["%s: %s"%(c,"  ".join(b[:2])),f]
			for a in j:
				if len(a)>aQ:a=a[:aQ-2]+".."
				API.PartyMsg(a)
		else:
			H("%s: %s."%(c,"  ".join(b)),q)
			for p in e or["nothing yet"]:H("   %s."%p,P)
	def dB(action,w):
		if len(j)>=ao:H("%d windows at most."%ao,q);return
		a=j[-1];g=a["g"];c,d=(g.GetX(),g.GetY())if z(g)else(a["x"],a["y"]);e=max(i["id"]for i in j)+1;f=set(k["metric"]for k in j);h=next((n for n in ah if n not in f),aY);b=a2(e,h,c+30,d+30);j.append(b);A(b);be(b);E()
	def dC(action,w):
		for a in j:
			b=a["size"]is not None;a["size"]=None
			if b and a["fit"]is None and z(a["g"]):A(a)
		E()
	def dD(action,w):a3();a["next_ui"]=0.;H("all meters cleared; new session.",aw)
	def dE(action,w):
		if a["recap"]is None:H("no death this session.",q)
		else:bb()
	def dF(action,w):
		w["graph"]=not w.get("graph");A(w);be(w)
		if z(w["picker"]):ba(w)
		E()
	def dG(action,w):a["redraw_wait"].discard(w["id"]);b4(w,True);E()
	def dH(action,w):w["minimized"],w["docked"]=not w["minimized"],False;bg(I(w));A(w);E()
	def dI(action,w):
		if aM():a["redraw_wait"].add(w["id"]);return
		a["redraw_wait"].discard(w["id"]);A(w);E()
	def dJ(action,w):
		i=ah.index(w["metric"])if w["metric"]in ah else 0;w["metric"]=ah[(i+action[2])%len(ah)];A(w)
		if z(w["picker"]):ba(w)
		E()
	def b5(action,w):
		a=action[0]
		if z(w[a]):T(w[a])
		else:(ba if a=="picker"else ds)(w)
	def dK(action,w):w["metric"]=action[2];T(w["picker"]);A(w);E()
	def dL(action,w):w["seg"]=action[2];T(w["segpick"]);bd(w);E()
	def dM(action,w):
		a=w["slots"];i=action[2];b=a[i].get("key")if i<len(a)else None
		if b is None or w["metric"]in("session","big","gold"):return
		w["detail_row"],w["detail_metric"]=b,w["metric"]
		if z(w["detail"]):aL(w)
		else:dt(w)
	dN={"settings":lambda action,w:HOST.show_settings(Q),"follow":lambda action,w:Follow.toggle(action[1],af),"new":dB,"own_size":dC,"reset":dD,"spot_add":lambda action,w:df(action[1],action[2]),"spot_rm":lambda action,w:b1(action[1]),"recap":dE,"recap_close":lambda action,w:bc.close(),"graph":dF,"export":lambda action,w:dl(w),"closed":dG,"toggle_min":dH,"to_bar":lambda action,w:HOST.dock_to_bar(I(w),Z(w)),"redraw":dI,"step":dJ,"picker":b5,"segpick":b5,"metric":dK,"seg":dL,"close_sub":lambda action,w:T(w.get(action[2])),"detail":dM,"report":lambda action,w:dA(w)};dO=("settings","follow","new","own_size","reset","spot_add","spot_rm","recap","recap_close");dP=(("idle","A fight ends after quiet of:","No damage for this long ends the fight","s"),("engage","Your targets count for:","Damage on what you attacked or targeted this recently is yours","s"),("history","Earlier fights kept:","Finished fights in the segment list","fights"),("min_heal","Ignore HP rises under:","Smaller rises count as regeneration","HP"),("rows","Rows per window:","For windows at their own size; undoes corner drags","rows"));dQ=(("rank","Number the rows","A rank before each name"),("pct","Show each row's share (%)","Percentage of the total after the value"),("party","Report to party chat in a party","Unticked, Report goes to your journal"),("scan","Watch the backpack (loot, reagents, ammo)","Open your backpack once after login so the client knows its contents"),("travel","Count tiles walked and recalls / gates","Fills the Travel display"),("recap","Show a death recap when you die","The last %d s of damage taken: who, how much, your HP"%int(ap)));dR="Pets' and strangers' healing is a \"(%)\" row outside the total.";b6=24
	def dS(w):return(("COUNTING  (fights, healing, rows)",[("num",)+d+aZ[d[0]]for d in dP],{"align":True,"pad":4}),("SHOW AND TRACK",[("check",)+f for f in dQ]+[("note",u(dR,w-28),{"ndy":2,"h":18})],{"pad":4}),("GOLD BY PLACE  (per character)",(("custom",28+max(1,len(o))*b6,dT),),{"pad":4}),("TOOLS",(("buttons",(("new",ab,"New meter window","Open one more (up to %d)"%ao),("recap",ab,"Last death recap","Show it again"),("own_size",aa,"Reset sizes","Give windows outside zones their own size (Rows above, %d px wide)"%W))),("buttons",(("export",bi,"Export","Write the first window's segment to %s in the VirtueAssistantSettings folder"%aV.replace("%08X","<serial>")),("reset",aa,"Reset all meters","Clear everything; new session"))),("note",u("Damage numbers: "+L["kind"],w-28),{"key":"feed","h":26})),{"pad":4}))
	def dT(f,x,y):
		g,c,w,i=f.g,f.c,f.w,f.store;e(g,"Name:",x+12,y+3);j=x+12+p("Name:")+8;c["spot_name"]=bq(bj(g,"",j,y,140,numbers=False),"Spot name (up to %d letters)"%bC);a=j+140+12;e(g,"Radius:",a,y+3);a+=p("Radius:")+8;c["spot_radius"]=bq(bj(g,str(a1.get("radius",bD)),a,y,44),"Tiles round you (%d-%d)"%az);a+=44+10;e(g,"tiles",a,y+3,q);O(g,i,"spot_add",bi,a+p("tiles")+12,y-2,"Name this spot","Gold gained within the radius counts here (a guarded town comes first)")
		if not o:e(g,u("No spots yet: stand where you farm, type a name, click Name this spot.",w-28),x+12,y+28+3,q)
		d=Kit.pic_size(aa[0])[0]or 30;c["spot_rm"]=[("spot_rm%d"%n,r[0])for n,r in enumerate(o)]
		for k,b in enumerate(o):h=y+28+k*b6;l="facet %d at %d, %d, %d tiles round"%(b[3],b[1],b[2],b[4]);m=p(l);e(g,u(b[0],w-24-d-18-m-12),x+12,h+3);e(g,l,x+w-12-d-12-m,h+3,q);O(g,i,"spot_rm%d"%k,aa,x+w-12-d,h,None,"Remove "+b[0])
	dU=.2
	def dV(f):
		c,b=f.c,f.store
		for k in("reset","new"):
			if ae(b,k):h((k,))()
		if ae(b,"own_size"):
			if a["active"]:h(("own_size",))()
			else:bR()
		d=[r for n,r in(("export",("export",0)),("recap",("recap",)))if ae(b,n)]
		if ae(b,"spot_add"):a1["radius"]=Kit.read_int(c["spot_radius"],bD,*az);d.append(("spot_add",str(c["spot_name"].Text or ""),a1["radius"]))
		for g in d:
			if a["active"]:h(g)()
			else:H("turn Meters on first.",q)
		for i,e in c["spot_rm"]:
			if ae(b,i):
				if a["active"]:h(("spot_rm",e))()
				else:b1(e)
	def dW(f,new):J(f.c["feed"],u("Damage numbers: "+L["kind"],f.w-28))
	def dX(c,new):
		del b["hist"][new["history"]:]
		if new["rows"]!=c["rows"]:
			if a["active"]:
				for w in j:w["size"]=None;h(("redraw",w["id"]))()
			else:bR()
		a["next_ui"]=0.
	aN=Kit.Page(m,dS,bO,dX,adjust=dW,clicks=dV,every=dU);bN();bS();a3()
	def dY():
		a.update({"shutting":False,"active":True,"queue":[],"last_tick":time.time(),"next_ui":0.,"next_friends":0.,"next_scan":0.,"me":None,"pos":None,"pack":None,"prev":{},"used":[],"buffq":[],"amtq":[],"poked":False,"place":None,"next_place":0.,"taken":[],"hp_log":[],"casts":[],"recap":None,"recap_show":False,"to_write":[],"redraw_wait":set(),"present":[],"pscan":None,"pack_cand":None,"my_ser":None,"my_name":"","next_name":0.,"fnames":None,"died":False});a["jr"]=Journal.reader();bN();a3();bP();bS();a0.add(c2)
		for w in j:
			w["shutting"]=w["docked"]=False
			if HOST.dock_wanted(I(w)):w["minimized"]=True
		Kit.hook_once(a,"hooked",("ObjectUsed",c5),("OnBuffAdded",c7),("OnEntityDamage",c3),("OnPlayerDeath",c6))
		if L["handler"]is None:del ai[:];ai.append(c1)
		for w in j:A(w);be(w)
	def dZ():
		a["poked"]=False
		if not j or j[0]["g"]is None:return
		c=time.time();e=max(0.,min(1.,c-a["last_tick"]));a["last_tick"]=c
		for w in list(j):
			if ae(w["store"],"close"):
				if w["id"]==0:T(w["g"]);return
				h.add(("closed",w["id"]),dup=True)
		while a["queue"]:
			d=a["queue"].pop(0);f=d[0];w=(next((n for n in j if n["id"]==d[1]),None)if len(d)>1 and isinstance(d[1],int)and f!="follow"else None)
			if w is not None or f in dO:dN[f](d,w)
		if a["redraw_wait"]and not aM():
			i,a["redraw_wait"]=a["redraw_wait"],set()
			for w in list(j):
				if w["id"]in i:A(w)
			E()
		for w in j:
			if w["resize_at"]and c-w["resize_at"]>=b8 and not aM():w["resize_at"]=0.;dr(w)
		if c>=a.get("next_zone",0.):a["next_zone"]=c+b9;dz()
		try:s=c8()
		except Exception as k:
			s=None;g=str(k)[:120]
			if g!=a.get("err"):a["err"]=g;H("couldn't read the client (%s)."%g,am)
		dc(c)
		if s:db(s,c)
		if a["died"]:a["died"]=False;dk(c)
		de(c,e)
		if a["recap_show"]:a["recap_show"]=False;bb()
		if b["cur"]is not None:
			b["cur"]["combat"]+=e;b["overall"]["combat"]+=e
			if not 0.<=c-b["last_combat"]<=m["idle"]:cW(c);a["next_ui"]=0.
		if c>=a["next_ui"]or(a["changed"]and a["next_ui"]-c<=bv-ce):
			a["next_ui"]=c+bv;a["changed"]=False
			for w in j:
				if not w["docked"]:bd(w)
	def d_():
		while ai and not a["shutting"]:ai.pop(0)()
		if a["to_write"]:dm()
	def d0():return bool(ai)or bool(a["to_write"])
	def d1():
		a["shutting"],a["active"],a["jr"]=True,False,None;del ai[:];E();bO();a0.close()
		for w in list(j):b4(w,False)
	return{"start":dY,"tick":dZ,"stop":d1,"client_tick":True,"config_height":aN.height,"build_config":aN.build,"poll_config":aN.poll,"config_closed":aN.closed,"thread_tick":d_,"thread_wanted":d0}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("meters","Meters","Damage, healing, loot and gold meters",_module_meters,.25,category="Extras")
