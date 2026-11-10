def _module_meters():
	bc=Follow.alt_held;bd=HOST.dock_forget;be=HOST.refresh_settings;Z=Kit.ART_CLOSE;bf=Kit.ART_OK;aa=Kit.ART_PAGE;B=Kit.GAP;ak=Kit.HUE_BAD;au=Kit.HUE_GOOD;q=Kit.HUE_INFO;P=Kit.HUE_TEXT;al=Kit.HUE_TITLE;ab=Kit.MARGIN;e=Kit.add_label;S=Kit.add_section;bg=Kit.add_textbox;bh=Kit.add_window_frame;O=Kit.art_button;bi=Kit.attach;ac=Kit.catcher;T=Kit.dispose;u=Kit.fit;bj=Kit.get_var;z=Kit.is_open;bk=Kit.put_var;bl=Kit.screen;J=Kit.set_text;bm=Kit.show_window;p=Kit.text_w;ad=Kit.was_clicked;bn=Kit.with_tip;Q="meters";ae="Meters";bo="Meters_settings";bp="Meters_windows";W=360;av=240;b4=1200;b5=.35;b6=.5;bq,b7=320,46;V=360;aw=300;K=20;br=146;am=6;b8=3823;b9=(4014,4016,4015);ca="#17171a";bs=1.;cb=.25;cc=3.;cd=2.;bt=30.;ce=30.;bu=18;cf=12;cg=0x80000000;ch=3821;ci=8.;bv=2.;cj=2.5;ck=8.;bw=1.5;cl=4.;bx=25;aK=5;aL="VirtueMeters.DamageHook";cm=4000;aM=220;cn=bt/2;co=40;cp=600;cq=800;by="Meters_spots";aN=20;bz=24;bA=20;ax=(1,300);cr=1.;bB="Elsewhere";bC=60.;ay=60;aO=40;af=4;aP=18+aO+4;aQ="Meters_%08X.txt";cs=50;an=10.;ct=12;aR=40;az=360;cu="Meters_recap_pos";cv=("Who: spell words heard before the hit,","else whom you fought (marked ?).");bD=200;bE=300;cw=20;bF=4.;cx=.5;cy=frozenset(("Magic Arrow","Harm","Fireball","Lightning","Mind Blast","Energy Bolt","Explosion","Flamestrike","Chain Lightning","Meteor Swarm","Earthquake","Poison","Poison Field","Fire Field","Holy Light","Pain Spike","Poison Strike","Strangle","Wither"));cz="you begin applying the bandages";cA=("you finish applying the bandages","you heal what little damage","you apply the bandages, but they barely help");cB="you have cured the target of all poisons";cC="the spell fizzles";cD="your concentration is disturbed";cE="insufficient mana";cF=re.compile(r"your skill in (.+?) has (increased|decreased) by "r"([0-9]+(?:\.[0-9]+)?)",re.I);cG=re.compile(r"your (strength|dexterity|intelligence) has (increased|decreased) by "r"([0-9]+)",re.I);cH=re.compile(r"you have (gained|lost) .*?\b(fame|karma)\b",re.I);bG=Kit.SPELL_WORDS;cI={3852:("Heal","heal"),3847:("Cure","cure"),3851:("Refresh",None),3849:("Strength",None),3848:("Agility",None),3853:("Explosion",None),3846:("Night Sight",None),3850:("Poison",None)};aA={3962:"Black Pearl",3963:"Blood Moss",3972:"Garlic",3973:"Ginseng",3974:"Mandrake Root",3976:"Nightshade",3981:"Spiders' Silk",3980:"Sulfurous Ash",3960:"Bat Wing",3983:"Grave Dust",3965:"Daemon Blood",3982:"Nox Crystal",3978:"Pig Iron",3903:"Arrows",7163:"Bolts"};F={"dmg_done":("Damage done","s","n","#c4562a",True),"dmg_taken":("Damage taken","s","n","#b02a2a",True),"dmg_nearby":("All damage nearby","s","n","#9a5a3a",True),"big":("Biggest hits","","n","#d07a2a",True),"kills":("Kills","h","n","#8a6ab0",False),"deaths":("Deaths","h","n","#6a6a78",True),"heal_done":("Healing done","s","n","#2f9a3c",True),"heal_taken":("Healing received","s","n","#3fae5a",True),"heal_by":("Healing by method","s","n","#4aa070",False),"cures":("Cures","m","n","#2a9a8a",True),"poisoned":("Poisonings","m","n","#5a9a2a",True),"spells":("Spells cast","m","n","#2f62cc",False),"mana":("Mana spent","m","n","#3a72d8",False),"consum":("Consumables","h","n","#a08a2a",False),"buffs":("Buffs & debuffs","h","n","#8a5ab0",False),"gold":("Gold","h","n","#cfae2a",False),"gold_place":("Gold by place","h","n","#d8b84a",False),"loot":("Items gained","h","n","#a8925a",False),"skills":("Skill gains","h","d1","#5a8acc",False),"stats":("Stat gains","h","n","#cc7a5a",False),"fame":("Fame & karma","h","n","#b0a050",False),"travel":("Travel","h","n","#6a9aaa",False),"session":("Session summary","","","#4a4a58",False)};aS=(("COMBAT",("dmg_done","dmg_taken","dmg_nearby","big","kills","deaths")),("HEALING",("heal_done","heal_taken","heal_by","cures","poisoned")),("MAGIC & ITEMS",("spells","mana","consum","buffs")),("ECONOMY & PROGRESS",("gold","gold_place","loot","skills","stats","fame","travel","session")));ag=[d2 for d3,d1 in aS for d2 in d1];aT="dmg_done";bH={"s":"per sec","m":"per min","h":"per hour"};m={"idle":6,"engage":12,"history":10,"min_heal":3,"rows":8,"rank":True,"pct":True,"scan":True,"travel":True,"party":True,"recap":True};cJ=dict(m);aU={"idle":(2,60),"engage":(3,120),"history":(1,30),"min_heal":(1,50),"rows":(3,20)};cK=5000;cL=4000;aV="(others)";cM=ae.lower()+":";a={"minimized":False,"shutting":False,"docked":False,"queue":[],"active":False,"hooked":False,"jr":None,"engaged":{},"watch":{},"friendly":{},"mobs":{},"dead_seen":{},"pack_sig":None,"pend":[],"orph":[],"last_spell":None,"cast_t":0.,"prev_lt":0,"to_write":[],"changed":False};d_={"g":None,"c":{},"store":({},{})};aW,h,H=Kit.basics(a,ae);o=[];C={"min":None,"b":None,"hist":{},"ver":0,"vb":{}};bI={"g":None,"c":{},"store":({},{}),"rows":[]};b={};j=[];aX={};L={"q":None,"handler":None,"event":None,"kind":"not hooked"};R={"tried":False,"tm":None,"la":None};ah=[];bJ=[0];import heapq;cN=re.compile(r"^[0-9,]+\s+");cO=60;cP=1.;ao=HOST.mobile
	def cQ():
		a=HOST.services.get("pets.list")
		if a is not None:
			try:
				b=a(distance=bu)
				if b is not None:return[int(d)for d in b]
			except Exception:pass
		c=[]
		for m in HOST.mobiles(bu):
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
	def ai(v,f="n"):s=l(v,f);return s if v<0 else "+"+s
	def D(a):a=int(max(0,a));h,m,s=a//3600,(a//60)%60,a%60;return "%d:%02d:%02d"%(h,m,s)if h else "%d:%02d"%(m,s)
	def ap(ser):return 0<int(ser or 0)<0x40000000
	def aY(name):return name.endswith(" (%)")
	def bK():Kit.kv_load(bo,"|",m,aU)
	def bL():Kit.kv_save(bo,"|",m,sorted(cJ),aU)
	def aZ(a,metric=aT,x=200,y=200,minimized=False):return{"id":a,"metric":metric if metric in F else aT,"seg":"current","x":x,"y":y,"minimized":minimized,"docked":False,"shutting":False,"g":None,"c":{},"store":({},{}),"slots":[],"picker":None,"segpick":None,"detail":None,"dc":{},"detail_row":None,"detail_metric":None,"graph":False,"gcols":[],"gkey":None,"fit":None,"size":None,"drawn":None,"resize_at":0.,"preview":False}
	def bM():
		a=[]
		for f in bj(bp).split(";"):
			p=f.split(",")
			if len(p)<6:continue
			try:c,x,y=int(p[0]),int(p[3]),int(p[4])
			except ValueError:continue
			if any(g["id"]==c for g in a):continue
			x,y=Kit.adapt(x,y,W,0);b=aZ(c,p[1],x,y,p[5]=="1");b["seg"]="overall"if p[2]=="overall"else "current";b["graph"]=len(p)>6 and p[6]=="1"
			if len(p)>8:
				try:
					d,e=int(p[7]),int(p[8])
					if d>0 and e>0:b["size"]=bN(d,e)
				except ValueError:pass
			a.append(b)
		a.sort(key=lambda w:w["id"])
		if not a or a[0]["id"]!=0:a.insert(0,aZ(0))
		del j[:];j.extend(a[:am])
	def bN(sw,sh):return max(av,min(b4,sw)),max(60,sh)
	def bO():
		if not j:bM()
		for w in j:w["size"]=None
		E()
	def E():
		a=[]
		for w in j:
			g=w["g"]
			if z(g):w["x"],w["y"]=g.GetX(),g.GetY()
			b=w.get("size")or(0,0);a.append("%d,%s,%s,%d,%d,%s,%s,%d,%d"%(w["id"],w["metric"],"overall"if w["seg"]=="overall"else "current",int(w["x"]),int(w["y"]),"1"if w["minimized"]else "0","1"if w.get("graph")else "0",int(b[0]),int(b[1])))
		bk(bp,";".join(a))
	def bP():
		del o[:];b,c=ax
		for d in bj(by).split(";"):
			p=d.split(",")
			if len(p)<5 or not p[0].strip():continue
			try:a=[p[0].strip(),int(p[1]),int(p[2]),int(p[3]),max(b,min(c,int(p[4])))]
			except ValueError:continue
			if all(f[0]!=a[0]for f in o)and len(o)<aN:o.append(a)
	def bQ():bk(by,";".join("%s,%d,%d,%d,%d"%tuple(d)for d in o))
	def cR(text):
		for a in ";,|":text=text.replace(a," ")
		return " ".join(text.split())[:bz]
	def bR(kind,n=0):a=time.time();bJ[0]+=1;return{"kind":kind,"n":n,"name":"Fight %d"%n if n else "Overall","start":a,"end":None,"combat":0.,"d":{},"serial":{},"big":[],"fights":0,"uid":bJ[0],"ver":0,"tot":{},"place_t":{}}
	def a_():b.clear();b.update({"overall":bR("overall"),"cur":None,"hist":[],"n":0,"last_combat":0.,"c_at":None});a["watch"].clear();a["engaged"].clear();a["pend"],a["orph"]=[],[];C.update({"min":None,"b":None,"ver":C["ver"]+1});C["hist"].clear();C["vb"].clear()
	def a0():a=b["cur"];return(b["overall"],a)if a is not None else(b["overall"],)
	def bS(now):
		m=int(now//60)
		if m!=C["min"]:
			a=C["hist"]
			for k in[d for d in a if d<=m-ay]:del a[k]
			C["min"]=m;C["b"]=a.setdefault(m,{})
		return C["b"]
	def c(b,row,c,ser=None):
		f=time.time();g=row.endswith(" (%)")
		if not g and(b!="gold"or row=="Gained"):h=bS(f);h[b]=h.get(b,0.)+c;i=C["vb"];i[b]=i.get(b,0)+1
		for d in a0():
			e=d["d"].get(b)
			if e is None:e=d["d"][b]={}
			r=e.get(row)
			if r is None:
				if len(e)>=cK:cS(d,b,e)
				r=e[row]=[0.,0,c,c,f,f]
			r[0]+=c;r[1]+=1
			if c>r[2]:r[2]=c
			if c<r[3]:r[3]=c
			r[5]=f
			if ser:d["serial"][(b,row)]=ser
			if not g:k=d["tot"];k[b]=k.get(b,0.)+c
			d["ver"]+=1
		if c and any(n["metric"]in(b,"session")and not n["docked"]for n in j):a["changed"]=True
	def cS(seg,a,d):
		b=sorted((abs(g[0]),f)for f,g in d.items()if f!=aV and not f.endswith(" (%)"));o=d.get(aV);c=seg["serial"]
		for e,k in b[:max(0,len(d)-cL)]:
			r=d.pop(k);c.pop((a,k),None)
			if o is None:o=d[aV]=list(r)
			else:o[0]+=r[0];o[1]+=r[1];o[2],o[3]=max(o[2],r[2]),min(o[3],r[3]);o[4],o[5]=min(o[4],r[4]),max(o[5],r[5])
	def cT(b,name,ser):
		c=bS(time.time())
		if b>c.get("big",0.):c["big"]=b;d=C["vb"];d["big"]=d.get("big",0)+1
		for e in a0():
			a=e["big"]
			if len(a)>=bx and b<=a[-1][0]:continue
			i=len(a)
			while i>0 and a[i-1][0]<b:i-=1
			a.insert(i,(b,name,ser));del a[bx:]
	def N(seg,a):return seg["tot"].get(a,0)
	def bT():
		a=time.time()
		if b["cur"]is None:b["n"]+=1;b["cur"]=bR("fight",b["n"]);b["overall"]["fights"]+=1
		b["last_combat"]=a;b["c_at"]=(b["cur"]["combat"],b["overall"]["combat"])
	def cU(now):
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
	def aB(seg):return max(1.,seg["combat"])
	def aC(seg):return max(1.,(seg["end"]or time.time())-seg["start"])
	def aj(seg,a,value):
		if a=="s":return value/aB(seg)
		if a=="m":return value/(aC(seg)/60.)
		return value/(max(60.,aC(seg))/3600.)
	def aD(w):
		s=w["seg"]
		if s=="overall":return b["overall"]
		if s!="current":
			for h in b["hist"]:
				if h["n"]==s:return h
			w["seg"]="current"
		return b["cur"]or(b["hist"][0]if b["hist"]else None)
	cV={"overall":"Overall","current":"Current"}
	def aE(w):return cV.get(w["seg"])or "Fight %d"%w["seg"]
	def cW(seg):
		if seg is None:return ""
		if seg["kind"]=="overall":return D(time.time()-seg["start"])
		return D(aB(seg))
	def bU(a):return abs(a[1][0])
	def X(seg,v,r,head=l):return "%s (%s/%s)"%(head(v),U(aj(seg,r,v)),r)
	def a1(a,seg,e=None):
		r,b,f,r,r=F[a]
		if seg is None:return(["No fight yet."],[])
		i=cW(seg)
		if a=="session":return cZ(seg)
		if a=="big":t=seg["big"]if e is None else seg["big"][:e];g=[(G,y,l(y),d1,None)for y,G,d1 in t];c=(["Biggest %s on %s"%(l(seg["big"][0][0]),seg["big"][0][1])]if seg["big"]else["No hits yet."]);return(c+[i],g)
		d=seg["d"].get(a,{})
		if a=="gold":n=d.get("Gained",[0.])[0];o=d.get("Spent / banked",[0.])[0];j=n-o;g=[("Gained",n,X(seg,n,"h"),None,d.get("Gained")),("Spent / banked",o,l(o),None,d.get("Spent / banked")),("Net",abs(j),X(seg,j,"h",ai),None,None)];return(["Net %s"%ai(j),"%s per hour"%U(aj(seg,"h",j)),i],g)
		if a=="gold_place":return cY(seg,d,e,i)
		h=N(seg,a)
		if e is None:p=sorted(d.items(),key=bU,reverse=True)
		elif e<=0:p=[]
		else:p=heapq.nlargest(e,d.items(),key=bU)
		g=[]
		for q,s in p:
			v=s[0];k=[]
			if b:k.append(U(aj(seg,b,v),f)+(""if b=="s"else "/"+b))
			if m["pct"]and h and not aY(q)and v>0:k.append("%d%%"%int(round(100.*v/h)))
			u=(ai(v,f)if a in("skills","stats")else l(v,f));w=u+(" (%s)"%", ".join(k)if k else "");g.append((q,abs(v),w,seg["serial"].get((a,q)),s))
		if a in("skills","stats"):c=["Total %s"%ai(h,f)]
		elif a=="cures":x=N(seg,"cures_mine");c=["Cures %s"%l(h),"by you %s"%l(x)]
		else:c=["Total %s"%l(h,f)]
		if b:c.append("%s %s"%(U(aj(seg,b,h),f),bH[b]))
		c.append("in combat "+D(seg["combat"])if b=="s"else i);return(c,g)
	def bV(seg,name,gold):a=seg["place_t"].get(name,0.);return gold/(max(bC,a)/3600.),a
	def cX(row):return row[1]
	def cY(seg,d,g,dur):
		j=seg["place_t"];c=list(d)
		for k,n in j.items():
			if n>=bC and k not in d:c.append(k)
		e=sum(s[0]for s in d.values());a=[]
		for f in c:
			r=d.get(f);b=r[0]if r is not None else 0.;h,p=bV(seg,f,b);i=[l(b)]
			if m["pct"]and e and b>0:i.append("%d%%"%int(round(100.*b/e)))
			a.append((f,h,"%s/h (%s)"%(U(h),", ".join(i)),None,r))
		a.sort(key=cX,reverse=True)
		if g is not None:del a[max(0,g):]
		o=len(c);return(["Gained %s"%l(e),Kit.count(o,"place"),dur],a)
	def cZ(seg):
		a=aC(seg);c=seg["combat"];f,g,h=N(seg,"dmg_done"),N(seg,"dmg_taken"),N(seg,"heal_done");i,j=N(seg,"kills"),N(seg,"deaths");d=seg["d"].get("gold",{});k=d.get("Gained",[0.])[0]-d.get("Spent / banked",[0.])[0];e=N(seg,"skills");b=[("Time",D(a)),("In combat","%s (%d%%)"%(D(c),int(100*c/a)))]
		if seg["kind"]=="overall":b.append(("Fights","%d"%seg["fights"]))
		b+=[("Damage done",X(seg,f,"s")),("Damage taken",X(seg,g,"s")),("Healing done",X(seg,h,"s")),("Kills",X(seg,i,"h")),("Deaths",l(j)),("Gold",X(seg,k,"h",ai)),("Skill gain","%s (%s/h)"%(ai(e,"d1"),U(aj(seg,"h",e),"d1"))),("Items gained",l(N(seg,"loot"))),("Spells cast",l(sum(s[1]for n,s in seg["d"].get("spells",{}).items()if n not in("Fizzled","Interrupted","Out of mana"))))];m=[(r,0.,t,None,None)for r,t in b];return([seg["name"]if seg["kind"]=="fight"else "Session",D(a)],m)
	def c_():
		try:
			import clr;clr.AddReference("System.Collections.Concurrent");clr.AddReference("System.Linq.Expressions");from System import Array,Int32,UInt32,Object,EventHandler,Tuple,Type,AppDomain;from System.Reflection import BindingFlags;from System.Collections.Concurrent import ConcurrentQueue;from System.Linq.Expressions import Expression,ParameterExpression;m=BindingFlags.Public|BindingFlags.NonPublic|BindingFlags.Static;e=API.GetType().Assembly;n=e.GetType("ClassicUO.Game.Managers.EventSink");f=e.GetType("ClassicUO.Game.GameObjects.Entity");a=n.GetEvent("OnEntityDamage",m);o,b,g=(clr.GetClrType(Object),clr.GetClrType(Int32),clr.GetClrType(UInt32));h=Tuple[UInt32,Int32];q=ConcurrentQueue[h]();c=Expression.Parameter(o,"sender");i=Expression.Parameter(b,"amount");j=Expression.Constant(q);p=Expression.Convert(Expression.PropertyOrField(Expression.Convert(c,f),"Serial"),g);r=clr.GetClrType(h).GetConstructor(Array[Type]([g,b]));s=Expression.Call(j,q.GetType().GetMethod("Enqueue"),Array[Expression]([Expression.New(r,Array[Expression]([p,i]))]));t=Expression.LessThan(Expression.Property(j,"Count"),Expression.Constant(cm,b));u=Expression.IfThen(Expression.AndAlso(Expression.TypeIs(c,f),t),s);d=Expression.Lambda[EventHandler[Int32]](u,Array[ParameterExpression]([c,i])).Compile();k=AppDomain.CurrentDomain;l=k.GetData(aL)
			if l is not None:safe(lambda:a.GetRemoveMethod(True).Invoke(None,Array[Object]([l])))
			a.GetAddMethod(True).Invoke(None,Array[Object]([d]));k.SetData(aL,d);L.update({"q":q,"handler":d,"event":a,"kind":"exact (per mobile)"});return True
		except Exception as v:L.update({"q":None,"handler":None,"event":None});L["kind"]="amounts only (%s)"%(str(v)[:50]or "no hook");return False
	def c0():
		h,a=L.get("handler"),L.get("event")
		if h is None or a is None:return
		with Kit.quiet:from System import Array,Object,AppDomain;a.GetRemoveMethod(True).Invoke(None,Array[Object]([h]));AppDomain.CurrentDomain.SetData(aL,None)
		L.update({"q":None,"handler":None,"event":None,"kind":"not hooked"})
	def c1(*b):
		if not a["active"]:return
		if not a["poked"]:a["poked"]=True;HOST.poke(Q,False)
		if L.get("q")is not None:return
		for c in b:
			try:a["amtq"].append(int(c))
			except Exception:continue
			del a["amtq"][:-200];return
	def c2():
		if not R["tried"]:
			R["tried"]=True
			try:from System.Reflection import BindingFlags;a=BindingFlags.Instance|BindingFlags.Public|BindingFlags.NonPublic;b=API.GetType().GetField("World",a).GetValue(API);c=b.GetType().GetProperty("TargetManager",a).GetValue(b,None);R["tm"],R["la"]=c,c.GetType().GetProperty("LastAttack",a)
			except Exception:R["tm"]=R["la"]=None
		if R["la"]is None:return 0
		return int(R["la"].GetValue(R["tm"],None)or 0)
	def c3(*b):
		if not a["active"]:return
		for c in b:
			try:a["used"].append(int(c));del a["used"][:-30];return
			except Exception:continue
	def c4(*b):
		if not a["active"]:return
		a["died"]=True
		if not a["poked"]:a["poked"]=True;HOST.poke(Q,False)
	def c5(*b):
		if not a["active"]:return
		for c in b:
			t=safe(lambda:c.Title)
			if t:a["buffq"].append(str(t));del a["buffq"][:-50];return
	def c6():
		e=time.time();c={"me":None,"dmg":[],"info":{},"fhp":{},"wst":{},"used":[],"pack":None,"friends":None};p=HOST.me()
		if p is None:return c
		b=int(p.Serial)
		if b!=a["my_ser"]or e>=a["next_name"]:a["my_name"]=str(p.Name or "");a["my_ser"],a["next_name"]=b,e+cP
		g={"ser":b,"name":a["my_name"],"hits":int(p.Hits),"hmax":int(p.HitsMax),"mana":int(p.Mana),"x":int(p.X),"y":int(p.Y),"gold":int(p.Gold or 0),"dead":bool(p.IsDead),"war":bool(p.InWarMode),"poison":bool(p.IsPoisoned),"map":int(API.GetMap())};c["me"]=g;q=L["q"]
		if q is not None:
			for w in range(cp):
				x,o=q.TryDequeue()
				if not x:break
				c["dmg"].append((int(o.Item1),int(o.Item2)))
		j=a["mobs"];h=c["info"]
		for b,w in c["dmg"]:
			if b not in j and b not in h and b!=g["ser"]:d=ao(b);h[b]=str(d.Name or "")if d is not None else ""
		c["lt"]=int(API.LastTargetSerial or 0);c["la"]=c2()
		for k in(a["engaged"],(c["lt"],c["la"])):
			for b in k:
				if ap(b)and b not in j and b not in h and b!=g["ser"]:
					d=ao(b)
					if d is not None:h[b]=str(d.Name or "")
		if e>=a["next_friends"]:
			a["next_friends"]=e+cc;r=[int(G)for G in API.GetPartyMemberSerials()or[]];s=cQ();t=[int(d1)for d1 in API.GetAllFriends()or[]];c["friends"]=(r,s,t);i,u=[],set()
			for k in(t,s,r):
				for f in k:
					if f!=g["ser"]and f not in u:
						u.add(f)
						if ao(f)is not None:i.append(f)
		else:i=None
		y=c["friends"]is not None;z=c["fhp"]
		for b in a["present"]:
			d=ao(b)
			if d is not None:A=None if y else j.get(b);z[b]=(int(d.Hits),int(d.HitsMax),bool(d.IsPoisoned),bool(d.IsDead),A or str(d.Name or ""))
		if i is not None:a["present"]=i
		l=c["wst"]
		for b,B in a["watch"].items():
			if e-B["t"]>cn:continue
			if ao(b)is not None:l[b]="alive"
			elif API.FindMobile(b|cg)is not None:l[b]="dying"
			else:l[b]="gone"
		if a["used"]:
			C,a["used"]=a["used"],[]
			for b in C:
				n=API.FindItem(b)
				if n is not None:c["used"].append((int(n.Graphic),str(n.Name or "")))
		if not m["scan"]:a["pscan"]=None
		elif a["pscan"]is None and e>=a["next_scan"]:
			a["next_scan"]=e+cd
			if API.Backpack:a["pscan"]=[HOST.pack_items(True),0,[],0,0,e]
		v=a["pscan"]
		if v is not None:c["pack"]=c7(v,e)
		return c
	def c7(e,now):
		m,i,g,h,j,n=e;o=len(m);p=min(o,i+cO)
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
	def a2(ser):b=a["me"];return(b is not None and ser==b["ser"])or ser in a["friendly"]
	def aF(ser):
		b=a["me"]
		if b is not None and ser==b["ser"]:return b["name"]or "You"
		return a["mobs"].get(ser)or "Unknown"
	def bW(ser,now):t=a["engaged"].get(ser);return t is not None and now-t<=m["engage"]
	def aq(now,kind,method,secs):
		b=kind=="cure+";kind="cure"if b else kind
		for o in list(a["orph"]):
			if o[1]==kind and now-o[0]<=bw:
				a["orph"].remove(o);bX(kind,method,o[2],o[3],o[4])
				if not b:return
		a["pend"].append([now+secs,kind,method,b])
	def bX(kind,method,ser,name,a):
		if kind=="heal":
			c("heal_done",name,a,ser)
			if not aY(name):c("heal_by",method,a)
		else:c("cures_mine",method,1)
	def bY(kind,now,ser,name,b):
		for p in a["pend"]:
			if p[1]==kind and now<=p[0]:
				if not p[3]:a["pend"].remove(p)
				bX(kind,p[2],ser,name,b);return
		a["orph"].append((now,kind,ser,name,b))
	def c8(s,now):
		d=s["me"]
		if d is None:return
		f,a["me"]=a["me"],d;q=a["mobs"]
		if len(q)>cq:q.clear()
		for b,e in s["info"].items():
			if e:q[b]=e
		if a["pend"]:a["pend"]=[d1 for d1 in a["pend"]if d1[0]>=now]
		if a["orph"]:a["orph"]=[d2 for d2 in a["orph"]if now-d2[0]<=bw]
		if s["friends"]is not None:
			K,L,M=s["friends"];A={}
			for N,O in(("friend",M),("pet",L),("party",K)):
				for b in O:A[b]=N
			A.pop(d["ser"],None);a["friendly"]=A
		j,r=s.get("lt",0),s.get("la",0)
		if r and d["war"]and ap(r)and not a2(r):a["engaged"][r]=now
		if(ap(j)and not a2(j)and(j!=a["prev_lt"]or now-a["cast_t"]<=2.)):a["engaged"][j]=now
		a["prev_lt"]=j
		if a["engaged"]:
			for b in[d3 for d3,d4 in a["engaged"].items()if now-d4>m["engage"]]:a["engaged"].pop(b,None)
		B=0
		if f is not None and d["hits"]<f["hits"]:B=f["hits"]-d["hits"]
		for b,P in s["dmg"]:a3(b,P,now)
		if a["amtq"]:
			t=None
			for g in a["amtq"]:
				if B>=g:B-=g;a3(d["ser"],g,now)
				else:
					if t is None:t=max(a["engaged"].items(),key=lambda a:a[1])[0]if a["engaged"]else 0
					a3(t,g,now)if t else c("dmg_nearby","Unknown",g)
			a["amtq"]=[]
		u=s["fhp"];u[d["ser"]]=(d["hits"],d["hmax"],d["poison"],d["dead"],d["name"]or "You")
		for b,(I,v,C,D,e)in u.items():
			if e:q[b]=e
			e=aF(b);h=a["prev"].get(b);a["prev"][b]=(I,v,C,D)
			if h is None:continue
			if D and not h[3]:
				if now-a["dead_seen"].get(b,0)>10:
					c("deaths",e,1,b);a["dead_seen"][b]=now
					if b==d["ser"]and m["recap"]:b_(now)
				continue
			if D or h[3]:continue
			E=b==d["ser"]or a["friendly"].get(b)=="party"or v not in(25,100);F=I-h[0]
			if F>=(m["min_heal"]if E else 1)and v==h[1]:x=e if E else e+" (%)";g=F if E else F*100./max(1,v);c("heal_taken",x,g,b);bY("heal",now,b,x,g)
			if C and not h[2]:c("poisoned",e,1,b)
			elif h[2]and not C:c("cures",e,1,b);bY("cure",now,b,e,1)
		if len(a["prev"])!=len(u):
			for b in[d5 for d5 in a["prev"]if d5 not in u]:a["prev"].pop(b,None)
		for b,Q in s["wst"].items():
			w=a["watch"].get(b)
			if w is None:continue
			if Q=="dying":
				a["watch"].pop(b,None)
				if w["friend"]:
					if now-a["dead_seen"].get(b,0)>10:c("deaths",w["name"],1,b);a["dead_seen"][b]=now
				elif w["mine"]and now-w["mine"]<=ce:c("kills",w["name"],1)
		if a["watch"]:
			for b in[d6 for d6,d7 in a["watch"].items()if now-d7["t"]>bt]:a["watch"].pop(b,None)
		if a["dead_seen"]:
			for b in[d8 for d8,d9 in a["dead_seen"].items()if now-d9>30]:a["dead_seen"].pop(b,None)
		i=a["hp_log"]
		if not i or i[-1][1]!=d["hits"]or i[-1][2]!=d["hmax"]:
			i.append((now,d["hits"],d["hmax"]))
			if len(i)>bE:del i[:len(i)-bE]
		if f is not None and d["mana"]<f["mana"]and not d["dead"]:G=a["last_spell"];x=G[1]if G is not None and now-G[0]<=cl else "Other";c("mana",x,f["mana"]-d["mana"])
		if f is not None and f["ser"]==d["ser"]:
			l=d["gold"]-f["gold"]
			if l>0:c("gold","Gained",l);c("gold_place",a["place"]or bB,l)
			elif l<0:c("gold","Spent / banked",-l)
		R=(d["x"],d["y"],d["map"])
		if m["travel"]and a["pos"]is not None and(d["x"]or d["y"]):
			S,T,U=a["pos"];H=max(abs(d["x"]-S),abs(d["y"]-T))
			if U!=d["map"]or H>cf:c("travel","Recalls, gates & teleports",1)
			elif H>0:c("travel","Tiles walked",H)
		a["pos"]=R
		for V,e in s["used"]:
			n=cI.get(V)
			if n is None:continue
			W=n[0]+" potion";c("consum",W,1)
			if n[1]:aq(now,n[1],n[0]+" potion",cj)
		o=s["pack"]
		if o is not None:
			p=a["pack"];X=p is not None and len(p)==0 and len(o)>0
			if p is not None and not X:
				for k,J in o.items():
					y=p.get(k);z=J[0]-(y[0]if y else 0)
					if z>0 and k[0]!=ch:Y=cN.sub("",(J[1]or "").strip())or "Item 0x%04X"%k[0];c("loot",Y.title(),z)
					elif z<0 and k[0]in aA:c("consum",aA[k[0]],-z)
				for k,y in p.items():
					if k not in o and k[0]in aA:c("consum",aA[k[0]],y[0])
			a["pack"]=o
		if a["buffq"]:
			for Z in a["buffq"]:c("buffs",Z,1)
			a["buffq"]=[]
	def a3(ser,dmg,now):
		d=a["me"];b=aF(ser);c("dmg_nearby",b,dmg,ser);w=a["watch"].get(ser)
		if w is None:
			if len(a["watch"])>=co:e=min(a["watch"].items(),key=lambda a:a[1]["t"])[0];a["watch"].pop(e,None)
			w=a["watch"][ser]={"name":b,"t":now,"mine":0.,"friend":False}
		w["t"],w["name"]=now,b
		if a2(ser):
			w["friend"]=ser!=d["ser"];c("dmg_taken",b,dmg,ser);bT()
			if ser==d["ser"]:dg(dmg,now)
		elif bW(ser,now):a["engaged"][ser]=now;w["mine"]=now;c("dmg_done",b,dmg,ser);cT(dmg,b,ser);bT()
	def c9(now):
		g=a["me"];e=g["name"]if g else None
		for h in a["jr"].new():
			f=h.name;b=h.low.strip()
			if e and f==e:
				d=bG.get(b)
				if d is not None:
					c("spells",d[0],1);a["last_spell"]=(now,d[0]);a["cast_t"]=now
					if d[1]=="heal":aq(now,"heal",d[0],ci)
					elif d[1]in("cure","cure+"):aq(now,d[1],d[0],ck)
				continue
			if b.startswith(cM):continue
			if b.startswith(cC):c("spells","Fizzled",1)
			elif b.startswith(cD):c("spells","Interrupted",1)
			elif b.startswith(cE):c("spells","Out of mana",1)
			elif b.startswith(cz):c("consum","Bandages",1)
			elif b.startswith(cB):aq(now,"cure","Bandage",bv)
			elif b.startswith(cA):aq(now,"heal","Bandage",bv)
			else:
				if f and e:
					d=bG.get(b)
					if d is not None:
						if d[0]in cy:de(now,f,d[0])
						continue
				if "your skill in"in b:
					m=cF.search(b)
					if m:v=float(m.group(3));c("skills",m.group(1).strip().title(),v if m.group(2).lower()=="increased"else-v);continue
				if "your "in b and " has "in b:
					m=cG.search(b)
					if m:v=int(m.group(3));c("stats",m.group(1).title(),v if m.group(2).lower()=="increased"else-v);continue
				if "you have "in b and("fame"in b or "karma"in b):
					m=cH.search(b)
					if m:c("fame","%s %s"%(m.group(2).title(),m.group(1).lower()),1)
	def da(me):
		c=HOST.guard_area()
		if c:return str(c)
		a=None;x,y,m=me["x"],me["y"],me["map"]
		for b in o:
			if b[3]==m:
				d=max(abs(x-b[1]),abs(y-b[2]))
				if d<=b[4]and(a is None or d<a[0]):a=(d,b[0])
		return a[1]if a is not None else bB
	def db(now,e):
		b=a["me"]
		if b is None:return
		if a["place"]is None or now>=a["next_place"]:a["next_place"]=now+cr;a["place"]=da(b)
		c=a["place"]
		for f in a0():d=f["place_t"];d[c]=d.get(c,0.)+e
	def dc(name,radius):
		b=a["me"]
		if b is None or not(b["x"]or b["y"]):H("position unknown; try again.",ak);return
		name=cR(name)or "Spot %d"%(len(o)+1);d,e=ax;radius=max(d,min(e,int(radius)));c=[g for g in o if g[0].lower()==name.lower()]
		if not c and len(o)>=aN:H("%d spots at most; remove one first."%aN,ak);return
		for f in c:o.remove(f)
		o.append([name,b["x"],b["y"],b["map"],radius]);bQ();a["place"]=None;H("spot \"%s\" named here (%d, %d), %d tiles round."%(name,b["x"],b["y"],radius),au);be(Q)
	def bZ(name):
		n=len(o);o[:]=[d for d in o if d[0]!=name]
		if len(o)!=n:bQ();a["place"]=None;be(Q)
	def dd(now):
		b=a["fnames"]
		if b is not None and b[0]==now:return b[1]
		c=a["mobs"];d=set(c.get(f)for f in a["friendly"]if c.get(f));a["fnames"]=(now,d);return d
	def de(now,name,spell):
		if name in dd(now):return
		c=Kit.spell_info(spell);d=float(c[3])if c else 0.;b=a["casts"];b.append([now,name,spell,False,d])
		while b and(len(b)>cw or now-b[0][0]>b[0][4]+bF):b.pop(0)
	def df(now):
		for c in a["casts"]:
			f=now-c[0]
			if not c[3]and c[4]-cx<=f<=c[4]+bF:c[3]=True;return "%s: %s"%(c[1],c[2]),c[1],0
		b=None
		for g,t in a["engaged"].items():
			if b is None or t>b[1]:b=(g,t)
		if b is not None and bW(b[0],now):d=aF(b[0]);return d+"?",d,b[0]
		e=a["me"]
		if e is not None and e["poison"]:return "Poison",None,0
		return "Unknown",None,0
	def dg(dmg,now):
		c=a["me"];d,e,f=df(now);b=a["taken"];b.append((now,dmg,d,e,f,c["hits"],c["hmax"]))
		if len(b)>bD:del b[:len(b)-bD]
	def b_(now):
		e=now-an;f=[n for n in a["taken"]if n[0]>=e];c,d=[],None
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
	def dh(now):
		b=a["me"]
		if b is None or now-a["dead_seen"].get(b["ser"],0)<=10:return
		c("deaths",aF(b["ser"]),1,b["ser"]);a["dead_seen"][b["ser"]]=now
		if m["recap"]:b_(now)
	def di(w):
		c=aD(w);e=aE(w)
		if c is None:c,e=b["overall"],"Overall"
		f=a["me"];j=f["ser"]if f else int(safe(lambda:API.Player.Serial,0)or 0);k=Kit.data_path(aQ%j);g=c["name"]if e!=c["name"]else "";d=["Meters export: %s%s, %s"%(e," (%s)"%g if g else "",time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))),("Session time %s, in combat %s"%(D(aC(c)),D(c["combat"]))if c["kind"]=="overall"else "Fight time %s"%D(aB(c))),""]
		for h in ag:
			l,i=a1(h,c,cs);d.append("== %s =="%F[h][0]);d.append("   "+"   ".join(n for n in l if n))
			for m,r in enumerate(i):d.append("   %2d. %-30s %s"%(m+1,r[0],r[2]))
			if not i:d.append("   (nothing)")
			d.append("")
		a["to_write"].append((k,"\n".join(d)+"\n",e))
	def dj():
		while a["to_write"]and not a["shutting"]:
			b,c,d=a["to_write"].pop(0)
			try:
				with open(b,"w")as e:e.write(c)
				H("%s exported to %s."%(d,b),au)
			except Exception as f:H("couldn't write %s (%s)."%(b,f),ak)
	M=ab
	def I(w):return Q if w["id"]==0 else "%s_%d"%(Q,w["id"])
	def Y(w):return ae if w["id"]==0 else "%s %d"%(ae,w["id"]+1)
	def dk(w,g):
		def b(*b):
			if w["g"]is g and not a["shutting"]:
				w["g"]=None
				if w["id"]==0:HOST.disable(Q)
				else:h.add(("closed",w["id"]),dup=True)
		return b
	def dl(w,slot,g):
		def a(*a):
			if w.get(slot)is g:w[slot]=None
		return a
	def dm(w,i):
		def a(*c):
			a=w["slots"]
			if i>=len(a):return
			b=a[i].get("ser")
			if bc():
				if b:h(("follow",b))()
				return
			h(("detail",w["id"],i))()
		return a
	def b0(w):n=8+35+p("New")+14+35+p("Report")+8;return n+14+35+p("Reset")if w["id"]==0 else n
	def A(w):
		x,y=w["x"],w["y"];C=w["g"]
		if z(C):x,y=C.GetX(),C.GetY()
		w["g"]=None;f,i,ad,ae=({},{}),{},[],[];ag=w["metric"];ah=("Close "+Y(w)+(" (this window only)"if w["id"]else " (turns it off; the Modules tab turns it back on)"));w["resize_at"],w["preview"]=0.,False
		if w["minimized"]:g=G.CreateGump(True,True);a,b=bq,b7;i["status"]=Kit.mini_bar(g,f,a,b,Y(w),I(w),h(("toggle_min",w["id"])),close_tip=ah)
		else:
			j=m["rows"];n=M+30+B;d=n+30+B;o=56+(aP if w.get("graph")else 0);aq=b0(w);D=w["fit"];t=D if D is not None else w["size"];ar=(max(120,t[0])if t else W)-2*M;ai=aq>ar
			if ai:o+=26
			k=o+j*K;a,b=W,d+k+M
			if t is not None:
				a,b=max(120,t[0]),t[1];j=max(1,(b-d-M-o)//K);k=max(o+j*K,b-d-M)
				if D is not None:k=max(30,min(k,b-d-M));j=max(0,(k-o)//K)
				b=d+k+M
			c=a-2*M
			if D is None:x,y=Kit.clamp(x,y,a,b);at=d+o+K+M;g=G.CreateModernGump(x,y,a,b,True,min(av,a),min(at,b),dn(w));g.SetAlpha(0)
			else:g=G.CreateGump(True,True)
			bh(g,a,b,mouse=False);au=0 if Kit.zone_up(I(w))else 84+Kit.DOCK_DX;aw=(ab+30+p(Y(w).upper())+16+au+35+p("Settings")+ab);Kit.title_bar(g,f,a,Y(w),I(w),h(("toggle_min",w["id"])),h(("to_bar",w["id"])),h(("settings",))if a>=aw else None,close_tip=ah);S(g,M,n,c,30);N=M+8;O(g,f,"prev",b9,N,n+4,None,"Show previous display",on_click=h(("step",w["id"],-1)));O(g,f,"next",Kit.ART_PLAY,N+32,n+4,None,"Show next display",on_click=h(("step",w["id"],1)));H,ax,ax,aj,ak=F[ag];Q=N+68;R=H if Q+35+p(H)+10+35+40<=M+c-6 else None;O(g,f,"pick",aa,Q,n+4,R,"Pick what this window shows"+(""if R else " (now: %s)"%H),on_click=h(("picker",w["id"])));J=Q+(35+p(H)if R else 30)+10;i["seg_room"],i["iw"]=max(20,M+c-6-J-35),c;az=u(aE(w),i["seg_room"]);i["seg"]=O(g,f,"segs",aa,J,n+4,az,"Pick a segment: current fight, Overall or an earlier fight",on_click=h(("segpick",w["id"])));S(g,M,d,c,k);i["head"]=e(g,"",M+8,d+5,q);al="Alt+click: auto-follow (again to stop)"
			if ag in("session","big","gold"):an=al if ak else None
			else:an="Show this row's details"+(". "+al if ak else "")
			U=min(br,int(c*.45));aA=c-12-U-10
			for l in range(j):v=d+26+l*K;L=G.CreateGumpSimpleProgressBar(c-12,K-2,ca,aj,0,100);L.SetPos(M+6,v);L.SetAcceptMouseInput(False);g.Add(L);ln=e(g,"",M+10,v+1,P);lv=e(g,"",M+c-6-U,v+1,P);ad.append({"bar":L,"name":ln,"val":lv,"ser":None,"key":None,"prog":None,"nw":aA,"vw":U})
			for l in range(j):v=d+26+l*K;ac(g,M+6,v,c-12,K-2,dm(w,l),an)
			r=d+26+j*K+4
			if w.get("graph"):
				gy=r-2;i["gcap"]=e(g,"",M+10,gy,q);ao=gy+18+aO;ap=max(1,min(ay,(c-12)//(af+1)));gx=M+6+(c-12-ap*(af+1))//2
				for l in range(ap):A=G.CreateGumpColorBox(.9,aj);A.SetRect(gx+l*(af+1),ao-1,af,1);A.IsVisible=False;A.SetAcceptMouseInput(False);g.Add(A);ae.append({"box":A,"x":gx+l*(af+1),"h":0})
				i["gbase"]=ao;r+=aP
			O(g,f,"new",aa,M+8,r,"New","Open another window (up to %d)"%am,on_click=h(("new",)));rx=M+8+35+p("New")+14;O(g,f,"report",aa,rx,r,"Report","Post the top %d rows to party chat (if set and in a party), else the journal"%aK,on_click=h(("report",w["id"])))
			if w["id"]==0:aB=r+26 if ai else r;O(g,f,"reset",Z,a-M-8-35-p("Reset"),aB,"Reset","Clear all meters; new session",on_click=h(("reset",)))
		w["x"],w["y"]=bm(g,x,y,a,b,I(w),w["minimized"]and w["docked"],dk(w,g),E,w,{"g":g,"c":i,"store":f,"slots":ad,"vkey":None,"gcols":ae,"gkey":None,"drawn":(a,b)})
		for aC in("picker","segpick","detail"):
			s=w.get(aC)
			if z(s)and not w["minimized"]:
				X=Kit.scroll_info(s)
				if X is not None:sw,sh=int(X["w"]),int(X["h"])
				else:sw,sh=int(s.GetWidth()or V),int(s.GetHeight()or 200)
				J,sy=a4(w,sw);Kit.place(s,J,sy,sw,sh);bi(s,g)
		ba(w);T(C)
	def dn(w):
		def a(*a):
			w["resize_at"]=time.time();g=w["g"]
			if w["preview"]or w["fit"]is not None or w["minimized"]or not z(g):return
			if(int(g.GetWidth()),int(g.GetHeight()))!=w["drawn"]:w["preview"]=True;g.SetAlpha(.55)
		return a
	def do(w):
		g=w["g"];w["preview"]=False
		if not z(g)or w["minimized"]:return
		b,a=int(g.GetWidth()),int(g.GetHeight())
		if w["fit"]is not None:
			g.SetAlpha(0)
			if(b,a)!=w["drawn"]:A(w)
			return
		c=w["drawn"]or(0,0)
		if abs(b-c[0])<=2 and abs(a-c[1])<=2:g.SetAlpha(0);return
		d=bl()[1]
		if d>0:a=min(a,d)
		w["size"]=bN(b,a);A(w);E()
	def a4(w,width):
		g=w["g"];r=Kit.rect(g)if z(g)else None;x,y=(r[0],r[1])if r is not None else(w["x"],w["y"]);b=bl()[0];a=x+((w.get("drawn")or(W,0))[0])+4
		if b and a+width>b:a=max(0,x-width-4)
		return a,y
	def aG(width,a,title,store,b,action,g=None):
		if g is None:g=G.CreateGump(True,True)
		bh(g,width,a);S(g,M,M,width-2*M,30);e(g,title,M+30,M+7,al);O(g,store,b,Z,width-M-54,M+4,None,"Close this window",on_click=h(action));return g
	def a5(w,slot):T(w[slot]);w[slot]=None
	def a6(w,slot,g,width,a):b,c=a4(w,width);bm(g,b,c,width,a,None,False,dl(w,slot,g),None,w,{slot:g});bi(g,w["g"])
	def a7(w):
		a5(w,"picker");a=V-2*M;c=(a-24)//2;f=[28+((len(v)+1)//2)*22+6 for x,v in aS];i=28+2*22+6;j=M+30+sum(G+B for G in f)+i+B+M;g=aG(V,j,"DISPLAYS",({},{}),"pclose",("close_sub",w["id"],"picker"));y=M+30+B
		for(r,s),k in zip(aS,f):
			S(g,M,y,a,k,r)
			for l,b in enumerate(s):m=M+12+(l%2)*(c+12);n=y+28+(l//2)*22;t=al if b==w["metric"]else P;e(g,u(F[b][0],c-4),m,n,t);ac(g,m-2,n-2,c,20,h(("metric",w["id"],b)),"Show %s in this window"%F[b][0])
			y+=k+B
		S(g,M,y,a,i,"THIS WINDOW");o=bool(w.get("graph"));d="on"if o else "off";e(g,u("Last-hour graph",a-36-p(d)),M+12,y+28);e(g,d,M+a-12-p(d),y+28,au if o else q);ac(g,M+8,y+26,a-16,20,h(("graph",w["id"])),"Show or hide the last hour under the rows, one bar per minute");e(g,u("Export this segment",a-24),M+12,y+50);ac(g,M+8,y+48,a-16,20,h(("export",w["id"])),"Write every display to %s in the VirtueAssistantSettings folder"%(aQ.replace("%08X","<serial>")));a6(w,"picker",g,V,j)
	def dp(w):
		a5(w,"segpick");c=V-2*M;d=[("current","Current fight"+(" (going on)"if b["cur"]else " (or the last)"),""),("overall","Overall (session)",D(time.time()-b["overall"]["start"]))]
		for a in b["hist"]:d.append((a["n"],"#%d  %s"%(a["n"],a["name"]),"%s  %s"%(D(aB(a)),l(N(a,"dmg_done")))))
		i=28+len(d)*22+6;j=M+30+B+i+M;g=aG(V,j,"SEGMENTS",({},{}),"sclose",("close_sub",w["id"],"segpick"));y=M+30+B;S(g,M,y,c,i,"WHAT TO SHOW  (fight time, damage done)");k=110
		for o,(m,p,n)in enumerate(d):
			f=y+28+o*22;r=al if m==w["seg"]else P;e(g,u(p,c-24-k-6),M+12,f,r)
			if n:e(g,n,M+c-12-k,f,q)
			ac(g,M+8,f-2,c-16,20,h(("seg",w["id"],m)),"Show this segment")
		a6(w,"segpick",g,V,j)
	ar=("Total","Share","Rate","Times","Average","Biggest","Smallest","First","Last")
	def dq(w):
		a5(w,"detail");a=aw-2*M;b=30+len(ar)*20+6;d=M+30+B+b+M;g=aG(aw,d,"DETAILS",({},{}),"dclose",("close_sub",w["id"],"detail"));c={};y=M+30+B;S(g,M,y,a,b);c["name"]=e(g,"",M+10,y+6,al);f=max(p(k)for k in ar)+14
		for i,t in enumerate(ar):h=y+30+i*20;e(g,t,M+10,h,q);c[t]=e(g,"",M+10+f,h,P)
		c["vw"]=a-20-f;w["dc"]=c;a6(w,"detail",g,aw,d);aH(w)
	def dr(w):
		a=w["metric"];m=int(time.time()//60);f=(a,m,C["ver"],C["vb"].get(a,0))
		if f==w["gkey"]:return
		w["gkey"]=f;k=C["hist"];d=[];b=0.
		if a!="session":
			n=m-ay+1
			for i in range(ay):
				g=k.get(n+i);v=g.get(a,0.)if g is not None else 0.
				if v>b:b=v
				d.append(v)
		o=w["c"]["gbase"];p=len(d)-len(w["gcols"])
		for i,c in enumerate(w["gcols"]):
			v=d[i+p]if d else 0.;h=int(round(aO*v/b))if b>0 and v>0 else 0
			if v>0 and h<1:h=1
			if h!=c["h"]:
				j=c["box"]
				if h:Kit.ui_rect(j,c["x"],o-h,af,h)
				if(h>0)!=(c["h"]>0):j.IsVisible=h>0
				c["h"]=h
		if a=="session":e="No graph for the summary"
		elif b<=0:e="Last hour, per minute: nothing yet"
		else:e="Last hour, %s per minute: peak %s"%("biggest hit"if a=="big"else "gained"if a in("gold","gold_place")else "total",l(b,F[a][2]or "n"))
		J(w["c"]["gcap"],u(e,w["c"].get("iw",W-2*ab)-20))
	def at(a,k,text,width):
		f=a.get(k)
		if f is not None and f[0]==text and f[1]==width:return f[2]
		b=u(text,width);a[k]=(text,width,b);return b
	def ds(i):
		def a(*b):
			a=bI["rows"]
			if i<len(a)and a[i]and bc():h(("follow",a[i]))()
		return a
	def dt(hp,t):
		a=hp[0]if hp else(t,0,0)
		for h in hp:
			if h[0]>t:break
			a=h
		return a[1],a[2]
	def a8():
		b=a["recap"]
		if b is None:return
		c=az-2*M;k=b["rows"][-ct:];d=30;m=30+20+d+8+max(1,len(k))*20+2*18+6;v=M+30+B+m+M;g,F,Q=a9.begin(az,v,a4(j[0],az)if j else None);aG(az,v,"DEATH RECAP",F,"close",("recap_close",),g);h=M+30+B;S(g,M,h,c,m,"LAST %d SECONDS  (damage you took)"%int(an));H=len(b["rows"]);I="Died %s: %s damage in %s"%(time.strftime("%H:%M:%S",time.localtime(b["t"])),l(b["total"]),Kit.count(H,"hit"));e(g,u(I,c-20),M+10,h+26,P);n=h+26+20;e(g,"HP",M+10,n+(d-16)//2,q);w=M+10+p("HP")+8;x=max(2,(M+c-10-w)//aR);J=b["t"]-an
		for i in range(aR):
			o,r=dt(b["hp"],J+(i+1)*an/aR);s=int(round(d*max(0,o)/float(r)))if r>0 else 0
			if s>0:y=G.CreateGumpColorBox(.9,"#c22d2d");y.SetRect(w+i*x,n+d-s,max(1,x-1),s);g.Add(y)
		z=n+d+8;t=[]
		if not k:e(g,"No damage seen.",M+10,z,q)
		A,C=M+60,c-166
		for i,(K,L,N,D,o,r)in enumerate(k):
			f=z+i*20;e(g,"-%.1fs"%max(0.,b["t"]-K),M+10,f,q);e(g,u(N,C),A,f,P);E="-%s"%l(L);e(g,E,M+c-64-p(E),f,ak);e(g,"HP %d"%o,M+c-58,f,q);t.append(D if ap(D)else 0)
			if t[-1]:ac(g,A-2,f-2,C+4,20,ds(i),"Alt+click: auto-follow (again to stop)")
		for i,O in enumerate(cv):e(g,u(O,c-20),M+10,h+m-40+i*18,q)
		a9.end(g,{"rows":t})
	a9=Kit.Window(Q,ae,None,bI,a8,cu,cleanup=aW,names=None,lock=False,owner=False,clear={"rows":[]});d0=None
	def ba(w):
		q=w["g"]
		if not z(q):return
		e=w["metric"]
		if w.get("gcols")and not w["minimized"]:dr(w)
		c=aD(w);l=a["me"];h=l["name"]if l else None;f=None
		if c is not None:
			if c["end"]is not None:f=(e,w["seg"],c["uid"],c["ver"],w["minimized"],m["rank"],m["pct"],h)
			elif F[e][1]=="s":f=(e,w["seg"],c["uid"],c["ver"],c["combat"],w["minimized"],m["rank"],m["pct"],h)
			if f is not None and f==w.get("vkey"):aH(w);return
		w["vkey"]=f;n,j=a1(e,c,0 if w["minimized"]else len(w["slots"]));d=w["c"]
		if w["minimized"]:
			o=d.get("status")
			if o is not None:J(o,at(d,"_fst","%s: %s  %s"%(Y(w),F[e][0],"  ".join(n[:2])),bq-90))
			return
		J(d["head"],at(d,"_fhd","   ".join(y for y in n if y),d.get("iw",W-2*ab)-16));J(d["seg"],at(d,"_fsg",aE(w),d.get("seg_room",400)));r=max([G[1]for G in j]+[0.])
		for k,b in enumerate(w["slots"]):
			if k<len(j):i,s,t,p,x=j[k];u=("%d. %s"%(k+1,i))if m["rank"]else i;v=al if(h and i==h)else P;J(b["name"],at(b,"_fn",u,b["nw"]),v);J(b["val"],at(b,"_fv",t,b.get("vw",br)));g=(float(s),float(r or 1.));b["ser"],b["key"]=(p if ap(p)else None),i
			else:J(b["name"],"");J(b["val"],"");g=(0.,1.);b["ser"],b["key"]=None,None
			if g!=b["prog"]:b["prog"]=g;b["bar"].SetProgress(g[0],g[1])
		aH(w)
	def aH(w):
		if not z(w["detail"]):return
		d=w["dc"];a,b=w["detail_metric"],w["detail_row"];c=aD(w);r=c["d"].get(a,{}).get(b)if(c is not None and a)else None;J(d["name"],u("%s (%s)"%(b or "",F.get(a,("",))[0]),aw-2*ab-20));e=dict((s,"")for s in ar)
		if r is not None:
			j,g,f,j,j=F[a];k=time.time();h=N(c,a)
			if a=="gold_place":m,n=bV(c,b,r[0]);i="%s/h (%s there)"%(U(m),D(n))
			elif g:i="%s %s"%(U(aj(c,g,r[0]),f),bH[g])
			else:i="-"
			e.update({"Total":l(r[0],f),"Share":("%d%% of %s"%(int(round(100.*r[0]/h)),l(h,f))if h and not aY(b)else "-"),"Rate":i,"Times":"%d"%r[1],"Average":l(r[0]/max(1,r[1]),f),"Biggest":l(r[2],f),"Smallest":l(r[3],f),"First":"%s ago"%D(k-r[4]),"Last":"%s ago"%D(k-r[5])})
		elif b:e["Total"]="nothing in this segment"
		for t in ar:J(d[t],u(e[t],d["vw"]))
	def aI():return bool(SNAP.drag)or SNAP.pressed()is True
	def du(w):
		def a(fw,fh,mode):
			a=(int(fw),int(fh))if(fw is not None and fh is not None)else None
			if a!=w.get("fit")or(mode=="again"and a is not None):w["fit"]=a;h(("redraw",w["id"]))()
		return a
	def dv(w):
		def a():a=56+(aP if w.get("graph")else 0)+(26 if b0(w)>av-2*M else 0);return av,M+30+B+30+B+a+K+M
		return a
	def dw():
		if aI():return
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
	def bb(w):a=Kit.dock_hooks(Y(w),b8,w,w,h(("redraw",w["id"])),fit=du(w));a.update({"exact":True,"verify":True,"pieces_out":True,"min":dv(w)});HOST.dock_add(I(w),a)
	def b1(w,remove):
		w["shutting"]=True;HOST.dock_remove(I(w))
		if remove:bd(I(w))
		for k in("picker","segpick","detail","g"):g,w[k]=w[k],None;T(g)
		if remove and w in j:j.remove(w)
	def dx(w):
		d=w["metric"];h=aD(w);b,i=a1(d,h,aK);c="%s (%s)"%(F[d][0],aE(w));e=["%d. %s %s"%(n+1,k[0],k[2])for n,k in enumerate(i[:aK])]
		if m["party"]and API.GetPartyMemberSerials():
			f="; ".join(e)or "nothing yet";g="%s: %s; %s"%(c,"  ".join(b[:2]),f);j=[g]if len(g)<=aM else["%s: %s"%(c,"  ".join(b[:2])),f]
			for a in j:
				if len(a)>aM:a=a[:aM-2]+".."
				API.PartyMsg(a)
		else:
			H("%s: %s."%(c,"  ".join(b)),q)
			for p in e or["nothing yet"]:H("   %s."%p,P)
	def dy(action,w):
		if len(j)>=am:H("%d windows at most."%am,q);return
		a=j[-1];g=a["g"];c,d=(g.GetX(),g.GetY())if z(g)else(a["x"],a["y"]);e=max(i["id"]for i in j)+1;f=set(k["metric"]for k in j);h=next((n for n in ag if n not in f),aT);b=aZ(e,h,c+30,d+30);j.append(b);A(b);bb(b);E()
	def dz(action,w):
		for a in j:
			b=a["size"]is not None;a["size"]=None
			if b and a["fit"]is None and z(a["g"]):A(a)
		E()
	def dA(action,w):a_();a["next_ui"]=0.;H("all meters cleared; new session.",au)
	def dB(action,w):
		if a["recap"]is None:H("no death this session.",q)
		else:a8()
	def dC(action,w):
		w["graph"]=not w.get("graph");A(w);bb(w)
		if z(w["picker"]):a7(w)
		E()
	def dD(action,w):a["redraw_wait"].discard(w["id"]);b1(w,True);E()
	def dE(action,w):w["minimized"],w["docked"]=not w["minimized"],False;bd(I(w));A(w);E()
	def dF(action,w):
		if aI():a["redraw_wait"].add(w["id"]);return
		a["redraw_wait"].discard(w["id"]);A(w);E()
	def dG(action,w):
		i=ag.index(w["metric"])if w["metric"]in ag else 0;w["metric"]=ag[(i+action[2])%len(ag)];A(w)
		if z(w["picker"]):a7(w)
		E()
	def b2(action,w):
		a=action[0]
		if z(w[a]):T(w[a])
		else:(a7 if a=="picker"else dp)(w)
	def dH(action,w):w["metric"]=action[2];T(w["picker"]);A(w);E()
	def dI(action,w):w["seg"]=action[2];T(w["segpick"]);ba(w);E()
	def dJ(action,w):
		a=w["slots"];i=action[2];b=a[i].get("key")if i<len(a)else None
		if b is None or w["metric"]in("session","big","gold"):return
		w["detail_row"],w["detail_metric"]=b,w["metric"]
		if z(w["detail"]):aH(w)
		else:dq(w)
	dK={"settings":lambda action,w:HOST.show_settings(Q),"follow":lambda action,w:Follow.toggle(action[1],ae),"new":dy,"own_size":dz,"reset":dA,"spot_add":lambda action,w:dc(action[1],action[2]),"spot_rm":lambda action,w:bZ(action[1]),"recap":dB,"recap_close":lambda action,w:a9.close(),"graph":dC,"export":lambda action,w:di(w),"closed":dD,"toggle_min":dE,"to_bar":lambda action,w:HOST.dock_to_bar(I(w),Y(w)),"redraw":dF,"step":dG,"picker":b2,"segpick":b2,"metric":dH,"seg":dI,"close_sub":lambda action,w:T(w.get(action[2])),"detail":dJ,"report":lambda action,w:dx(w)};dL=("settings","follow","new","own_size","reset","spot_add","spot_rm","recap","recap_close");dM=(("idle","A fight ends after quiet of:","No damage for this long ends the fight","s"),("engage","Your targets count for:","Damage on what you attacked or targeted this recently is yours","s"),("history","Earlier fights kept:","Finished fights in the segment list","fights"),("min_heal","Ignore HP rises under:","Smaller rises count as regeneration","HP"),("rows","Rows per window:","For windows at their own size; undoes corner drags","rows"));dN=(("rank","Number the rows","A rank before each name"),("pct","Show each row's share (%)","Percentage of the total after the value"),("party","Report to party chat in a party","Unticked, Report goes to your journal"),("scan","Watch the backpack (loot, reagents, ammo)","Open your backpack once after login so the client knows its contents"),("travel","Count tiles walked and recalls / gates","Fills the Travel display"),("recap","Show a death recap when you die","The last %d s of damage taken: who, how much, your HP"%int(an)));dO="Pets' and strangers' healing is a \"(%)\" row outside the total.";b3=24
	def dP(w):return(("COUNTING  (fights, healing, rows)",[("num",)+d+aU[d[0]]for d in dM],{"align":True,"pad":4}),("SHOW AND TRACK",[("check",)+f for f in dN]+[("note",u(dO,w-28),{"ndy":2,"h":18})],{"pad":4}),("GOLD BY PLACE  (per character)",(("custom",28+max(1,len(o))*b3,dQ),),{"pad":4}),("TOOLS",(("buttons",(("new",aa,"New meter window","Open one more (up to %d)"%am),("recap",aa,"Last death recap","Show it again"),("own_size",Z,"Reset sizes","Give windows outside zones their own size (Rows above, %d px wide)"%W))),("buttons",(("export",bf,"Export","Write the first window's segment to %s in the VirtueAssistantSettings folder"%aQ.replace("%08X","<serial>")),("reset",Z,"Reset all meters","Clear everything; new session"))),("note",u("Damage numbers: "+L["kind"],w-28),{"key":"feed","h":26})),{"pad":4}))
	def dQ(f,x,y):
		g,c,w,i=f.g,f.c,f.w,f.store;e(g,"Name:",x+12,y+3);j=x+12+p("Name:")+8;c["spot_name"]=bn(bg(g,"",j,y,140,numbers=False),"Spot name (up to %d letters)"%bz);a=j+140+12;e(g,"Radius:",a,y+3);a+=p("Radius:")+8;c["spot_radius"]=bn(bg(g,str(aX.get("radius",bA)),a,y,44),"Tiles round you (%d-%d)"%ax);a+=44+10;e(g,"tiles",a,y+3,q);O(g,i,"spot_add",bf,a+p("tiles")+12,y-2,"Name this spot","Gold gained within the radius counts here (a guarded town comes first)")
		if not o:e(g,u("No spots yet: stand where you farm, type a name, click Name this spot.",w-28),x+12,y+28+3,q)
		d=Kit.pic_size(Z[0])[0]or 30;c["spot_rm"]=[("spot_rm%d"%n,r[0])for n,r in enumerate(o)]
		for k,b in enumerate(o):h=y+28+k*b3;l="facet %d at %d, %d, %d tiles round"%(b[3],b[1],b[2],b[4]);m=p(l);e(g,u(b[0],w-24-d-18-m-12),x+12,h+3);e(g,l,x+w-12-d-12-m,h+3,q);O(g,i,"spot_rm%d"%k,Z,x+w-12-d,h,None,"Remove "+b[0])
	dR=.2
	def dS(f):
		c,b=f.c,f.store
		for k in("reset","new"):
			if ad(b,k):h((k,))()
		if ad(b,"own_size"):
			if a["active"]:h(("own_size",))()
			else:bO()
		d=[r for n,r in(("export",("export",0)),("recap",("recap",)))if ad(b,n)]
		if ad(b,"spot_add"):aX["radius"]=Kit.read_int(c["spot_radius"],bA,*ax);d.append(("spot_add",str(c["spot_name"].Text or ""),aX["radius"]))
		for g in d:
			if a["active"]:h(g)()
			else:H("turn Meters on first.",q)
		for i,e in c["spot_rm"]:
			if ad(b,i):
				if a["active"]:h(("spot_rm",e))()
				else:bZ(e)
	def dT(f,new):J(f.c["feed"],u("Damage numbers: "+L["kind"],f.w-28))
	def dU(c,new):
		del b["hist"][new["history"]:]
		if new["rows"]!=c["rows"]:
			if a["active"]:
				for w in j:w["size"]=None;h(("redraw",w["id"]))()
			else:bO()
		a["next_ui"]=0.
	aJ=Kit.Page(m,dP,bL,dU,adjust=dT,clicks=dS,every=dR);bK();bP();a_()
	def dV():
		a.update({"shutting":False,"active":True,"queue":[],"last_tick":time.time(),"next_ui":0.,"next_friends":0.,"next_scan":0.,"me":None,"pos":None,"pack":None,"prev":{},"used":[],"buffq":[],"amtq":[],"poked":False,"place":None,"next_place":0.,"taken":[],"hp_log":[],"casts":[],"recap":None,"recap_show":False,"to_write":[],"redraw_wait":set(),"present":[],"pscan":None,"pack_cand":None,"my_ser":None,"my_name":"","next_name":0.,"fnames":None,"died":False});a["jr"]=Journal.reader();bK();a_();bM();bP();aW.add(c0)
		for w in j:
			w["shutting"]=w["docked"]=False
			if HOST.dock_wanted(I(w)):w["minimized"]=True
		Kit.hook_once(a,"hooked",("ObjectUsed",c3),("OnBuffAdded",c5),("OnEntityDamage",c1),("OnPlayerDeath",c4))
		if L["handler"]is None:del ah[:];ah.append(c_)
		for w in j:A(w);bb(w)
	def dW():
		a["poked"]=False
		if not j or j[0]["g"]is None:return
		c=time.time();e=max(0.,min(1.,c-a["last_tick"]));a["last_tick"]=c
		for w in list(j):
			if ad(w["store"],"close"):
				if w["id"]==0:T(w["g"]);return
				h.add(("closed",w["id"]),dup=True)
		while a["queue"]:
			d=a["queue"].pop(0);f=d[0];w=(next((n for n in j if n["id"]==d[1]),None)if len(d)>1 and isinstance(d[1],int)and f!="follow"else None)
			if w is not None or f in dL:dK[f](d,w)
		if a["redraw_wait"]and not aI():
			i,a["redraw_wait"]=a["redraw_wait"],set()
			for w in list(j):
				if w["id"]in i:A(w)
			E()
		for w in j:
			if w["resize_at"]and c-w["resize_at"]>=b5 and not aI():w["resize_at"]=0.;do(w)
		if c>=a.get("next_zone",0.):a["next_zone"]=c+b6;dw()
		try:s=c6()
		except Exception as k:
			s=None;g=str(k)[:120]
			if g!=a.get("err"):a["err"]=g;H("couldn't read the client (%s)."%g,ak)
		c9(c)
		if s:c8(s,c)
		if a["died"]:a["died"]=False;dh(c)
		db(c,e)
		if a["recap_show"]:a["recap_show"]=False;a8()
		if b["cur"]is not None:
			b["cur"]["combat"]+=e;b["overall"]["combat"]+=e
			if not 0.<=c-b["last_combat"]<=m["idle"]:cU(c);a["next_ui"]=0.
		if c>=a["next_ui"]or(a["changed"]and a["next_ui"]-c<=bs-cb):
			a["next_ui"]=c+bs;a["changed"]=False
			for w in j:
				if not w["docked"]:ba(w)
	def dX():
		while ah and not a["shutting"]:ah.pop(0)()
		if a["to_write"]:dj()
	def dY():return bool(ah)or bool(a["to_write"])
	def dZ():
		a["shutting"],a["active"],a["jr"]=True,False,None;del ah[:];E();bL();aW.close()
		for w in list(j):b1(w,False)
	return{"start":dV,"tick":dW,"stop":dZ,"client_tick":True,"config_height":aJ.height,"build_config":aJ.build,"poll_config":aJ.poll,"config_closed":aJ.closed,"thread_tick":dX,"thread_wanted":dY}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("meters","Meters","Damage, healing, loot and gold meters",_module_meters,.25,category="Extras")
