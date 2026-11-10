def _module_grimoire():
	bA=HOST.bar_alive;bB=HOST.claim_cursor;aP=HOST.dock_want_set;bC=HOST.dock_wanted;P=HOST.idle;a5=HOST.release_cursor;bD=Kit.ART_OK;cd=Kit.ART_PAGE;a6=Kit.ART_PLAY;ce=Kit.CORNER_ART;E=Kit.HUE_BAD;L=Kit.HUE_INFO;aA=Kit.count;bE=Kit.data_path;cf=Kit.dispose;bF=Kit.get_var;cg=Kit.gump_is_cmd;ch=Kit.gump_is_int;aQ=Kit.gump_parse;aR=Kit.is_open;ci=Kit.look_hue;F=Kit.on_client;bG=Kit.put_var;bH=Kit.set_text;bI=Kit.strip_html;a7=Kit.with_tip;aB=Kit.zone_up;q="grimoire";aS="Grimoire";bJ=[3834];dF={"charge":0,"recall":3,"gate":4,"sacred":5,};aC="recall";cj=("recall","gate","charge","recall_scroll","gate_scroll","sacred");dG={"recall":"Recall","gate":"Gate Travel","sacred":"Sacred Journey"};ck=3;a8=40;bK=a8;cl=.15;cm=.5;cn,co="#F0C040","#6A6A6A";bL=1;aT=8012;aU=8032;cp=12;cq=5;cr=("fizzles","not yet recovered","more reagents","insufficient mana","concentration is disturbed");cs=.4;ct=5.;dH=frozenset("Reactive Armor|Protection|Magic Reflection|Incognito|Create Food|Earthquake|Summon Creature|Air Elemental|Earth Elemental|Fire Elemental|Water Elemental|Summon Daemon".split("|"));cu=1.5;cv=4.;cw,cx=920,950;aV,aW=700,220;ao=160;ai,a9=60,150;bM=54;bN="Grimoire_cmd";cy="Grimoire_state";bO=95;ba=66;bb=Kit.WINDOW_BG;cz=a6[0];dI=a6[1];cA=2225;V="#E8C84A";K="#ECECEC";J="#9C9C9C";ap="#6E6E6E";R="#E04848";aq="#C8B070";bc=.05;aj={K:Kit.HUE_TEXT,V:Kit.HUE_TITLE,J:L,ap:L,R:E};dJ=("Lowers the target's Dexterity for a time.|Conjures a random piece of food into your pack.|Lowers the target's Intelligence for a time.|Restores a small amount of the target's health.|Strikes the target with a minor bolt of magic.|Lets the target see clearly in darkness.|Wards you with armor that soaks up melee damage.|Lowers the target's Strength for a time.|Raises the target's Dexterity for a time.|Raises the target's Intelligence for a time.|Attempts to neutralize poison in the target.|Damages the target; strongest at close range.|Traps a container to explode when opened.|Disarms a magical trap on a container.|Temporarily raises your armor rating.|Raises the target's Strength for a time.|Raises the target's Strength, Dexterity and Intelligence.|Hurls a ball of fire at the target.|Magically seals a container shut.|Poisons the target.|Uses or opens an object from a distance.|Instantly moves you to a visible location.|Opens a magically locked container.|Raises a temporary wall of stone.|Cures poison in the target and those nearby.|Raises the armor rating of everyone around you.|Lowers the target's Strength, Dexterity and Intelligence.|Creates a wall of flame that burns those who cross it.|Restores a large amount of the target's health.|Calls a bolt of lightning down on the target.|Drains mana from the target.|Teleports you to the location marked on a rune.|Summons whirling blades that attack nearby creatures.|Destroys a magical field.|Disguises your appearance and name for a time.|Turns harmful spells back upon their caster.|Damages the target based on your superior intellect.|Freezes the target in place for a time.|Creates a wall of poisonous gas.|Summons a random creature to fight for you.|Banishes a summoned creature.|Strikes the target with a powerful bolt of energy.|Engulfs the target in a fiery explosion.|Makes the target invisible for a time.|Marks a recall rune with your current location.|Curses everyone in an area.|Creates a wall that paralyzes those who touch it.|Reveals hidden creatures and players nearby.|Lightning strikes everyone around the target.|Creates an impassable wall of energy.|Engulfs the target in a column of fire.|Opens a moongate to a rune's location that others can use.|Steals the target's mana and gives it to you.|Banishes all summoned creatures in an area.|Rains fire on everyone around the target.|Transforms you into another creature.|Shakes the ground, damaging everyone around you.|Summons a vortex of energy that attacks your foes.|Brings a ghost back to life.|Summons an air elemental to serve you.|Summons a daemon to serve you.|Summons an earth elemental to serve you.|Summons a fire elemental to serve you.|Summons a water elemental to serve you.").split("|");dK={"Feeblemind":"NS GI","Cunning":"NS MR","Resurrection":"BM GI GA"};bd=[(fr+" Circle",[(fs,dJ[fq*8+ft],dK.get(fs,fu))for ft,(fs,fu)in enumerate(Kit.MAGERY[fq*8:fq*8+8])])for fq,fr in enumerate(("First","Second","Third","Fourth","Fifth","Sixth","Seventh","Eighth"))];aD=dict(Kit.REAGENTS,SS=("Spider's Silk",3981));dL=["BP","BM","GA","GI","MR","NS","SA","SS"];be=16;cB=24;dM=[("charge","Charge","Recall using one of the book's charges"),("recall","Recall","Cast Recall on this rune"),("gate","Gate","Cast Gate Travel to this rune"),("recall_scroll","Recall scroll","Read a Recall scroll on this rune"),("gate_scroll","Gate scroll","Read a Gate Travel scroll on this rune")];aE=86;bf=60;aX={"opacity":bO,"scale":100,"loaded":False};fl=dict(aX);b={"minimized":False,"shutting":False,"docked":False,"queue":[]};c={"g":None,"c":{},"store":({},{}),"w":cw,"h":cx,"opacity":bO};bh,Q,o=Kit.basics(b,aS)
	def fm():pass
	def fo():pass
	Z=0;aF=None;B=[];C={};M={};u=[];N={"hold":0.,"reading":False};aa=0x554B87F3;z={"ver":0,"dest_ver":-1,"dests":[]};j={"list":[],"keys":set(),"last":None,"owner":None,"save":False,"save_last":False};ab={};aY={};aG=[]
	def cC(hidden=False):return{"ctrls":[],"tops":[],"counts":[],"spells":[],"stars":{},"hidden":hidden}
	ac=cC();r={};t=ac;ad={};bi={};bj={};S={"key":None,"t":0.,"selected":None}
	def cD(s):s=re.sub(r"[^a-z]","",(s or "").lower());return s.replace("summon","")if "elemental"in s else s
	def aH(fresh=False):return HOST.pack_items(deep=True,max_age=0. if fresh else.5)
	def bk():
		b=[API.FindLayer("OneHanded"),API.FindLayer("TwoHanded")];b+=list(API.ItemsInContainer(API.Player.Serial)or());c,d,e=set(),[],API.Backpack
		for a in b:
			if a and a.Serial not in c and a.Serial!=e:c.add(a.Serial);d.append(a)
		return d
	def cE():
		a=set()
		for b in bF("Grimoire_RunebookTypes").split(","):
			try:g,h=b.split(":");a.add((int(g,16),int(h,16)))
			except ValueError:pass
		return a
	aI=cE();bP=set()
	def cF(it):return bQ(it.Graphic,it.Hue,it.Name)
	def bQ(g,h,name):
		if(g,h)in aI:return True
		name=(name or "").lower()
		if "rune"in name and "book"in name:return True
		if "spellbook"in name:return False
		if g in bJ and h==1121:return True
		return g==8901
	def cG(it):return it.Graphic in bJ and not cF(it)
	def dN():
		a=[d for d in bk()+aH()if cG(d)]
		for b in a:
			if list(API.GetSpellsInSpellbook(b.Serial)or()):return b.Serial
		return a[0].Serial if a else 0
	def dO(serial):
		a=False
		with Kit.quiet:
			for g in list(Tz.get(None,"Gumps",Tz.T("ClassicUO.Game.Managers.UIManager"))):
				with Kit.quiet:
					if(g.LocalSerial==serial and "Spellbook"in g.GetType().Name and not g.IsDisposed):g.Dispose();a=True
		return a
	def cH():return "spells_%08X"%int(API.Player.Serial)
	def dP(force=False):
		if not Z:return
		a=list(API.GetSpellsInSpellbook(Z)or[])
		if not a and not force:
			c=set(f for f in bp(cH()).split(",")if f)
			if c:return c
		if not a:
			API.UseObject(Z);b=time.time()+2.
			while time.time()<b and P(.05):
				a=list(API.GetSpellsInSpellbook(Z)or[])
				if a:break
			b=time.time()+1.
			while time.time()<b and not HOST.aborting():
				if F(lambda:dO(Z)):break
				P(.05)
		if not a:return
		d=set(cD(g)for g in a);bo(cH(),",".join(sorted(d)));return d
	dQ=set([fv for fw,fv in aD.values()]+[aT,aU])
	def bl():
		c=aH();a=None
		if HOST.in_hop:
			a=(HOST.pass_id,len(c))
			if bR["key"]==a:return dict(bR["totals"])
		b=dict((f,0)for f in dQ)
		for d in c:
			g=d.Graphic
			if g in b:b[g]+=max(1,d.Amount or 0)
		if a is not None:bR.update({"key":a,"totals":dict(b)})
		return b
	bR={"key":None,"totals":None}
	def bm(n):return "{:,}".format(n)
	def cI(graphic,lbl,n,owned=True):return[graphic,lbl,bm(n),aj[K if owned else ap],aj[R if owned else ap]]
	def cJ(totals):return(totals.get(aT,0)>0,totals.get(aU,0)>0)
	def dR():
		if not ac["counts"]and not any(s["counts"]for s in r.values()):return
		c=bl();f=c!=k["totals"];k["totals"]=c;j=(ac["counts"]+[w for v in r.values()for w in v["counts"]])if f else[]
		for a in j:
			l,g,h=a[0],a[1],a[2];n=c.get(l,0);d=bm(n)
			if d==h:continue
			if(n==0)!=(h=="0"):g.Hue=a[3]if n else a[4]
			ei(g,d);a[2]=d
		if f:dv()
		m=cJ(c);o=aO(b["tab"])
		for e,i in list(r.items()):
			if i.get("scrolls")is not None and i["scrolls"]!=m and not b["dirty"]:
				if e==o:a4(e,False)
				else:a_(r.pop(e)["ctrls"])
	cK=set([3834,8901,4079,4080,4081,4082,4083,4084,4029,4030,7185,7187,8786,8787,9100,9120,11600])
	def dS():
		b=[d for d in bk()+aH()if d.Graphic in cK or "book"in(d.Name or "").lower()]
		if not b:o("no books in your pack or hands.",E);return
		o("books you carry (graphic / hue / name / kind):",L)
		for a in b:c="runebook"if cF(a)else("spellbook"if cG(a)else "?");o("0x%04X / 0x%04X / %s (%s)."%(a.Graphic,a.Hue,a.Name or "no name",c),L)
	def dT():
		o("target one of your runebooks.",L);a=object();b["pick"]=a
		def c(serial):
			if b["pick"]is not a:return
			b["pick"]=None;Q.add(("registered",serial),dup=True,front=True)
		HOST.pick_target(15,c)
	def dU(serial):
		if not serial:o("cancelled.",L);return False
		a=API.FindItem(serial)
		if not a:o("that isn't an item.",E);return False
		aI.add((a.Graphic,a.Hue));bG("Grimoire_RunebookTypes",",".join("%X:%X"%d for d in sorted(aI)));o("runebooks are graphic 0x%04X, hue 0x%04X; saved."%(a.Graphic,a.Hue),Kit.HUE_GOOD);return True
	def cL(items):
		b=[]
		for a in items:
			try:g,h,n=a.Graphic,a.Hue,a.Name
			except Exception:continue
			b.append((a.Serial,g,h,n,bQ(g,h,n)))
		return b
	def dV():
		c,b=[],{};d=cL(aH(fresh=True));bP.update((l,v)for y,l,v,w,x in d if x and w);e=set()
		for s,g,h,n,f in cL(bk())+d:
			i=f or(not n and(g,h)in bP)
			if not i or int(s)in e:continue
			e.add(int(s));a=(n or "").strip()or "Runebook";a=a[:1].upper()+a[1:];b[a]=b.get(a,0)+1
			if b[a]>1:a="%s %d"%(a,b[a])
			c.append({"serial":int(s),"title":a})
		return c
	def cM(raw):return str(raw or "").replace("\r","").replace("\x00","").split("\n")
	def dW():
		a={}
		try:a["is_cmd"]=cg("croppedtext 305 60 115 17 81 17");a["text_is_text"]=not cg("Page 2 Boss");b,c=aQ("Shame Bankpage 0");a["split_merged"]=(b,c);a["lines"]=len(aQ("a\nb\nc\npage 0")[0])
		except Exception as d:a["error"]=str(d)
		return a
	dX=re.compile(r"^(empty|\(indescript\)|charges?:?|max charges:?|rename( book)?|drop rune|set default|"r"recall.*|gate travel.*|sacred journey.*|use charge.*|next|prev(ious)?|okay|cancel|"r"felucca|trammel|ilshenar|malas|tokuno)$",re.I);dY=re.compile(r"\d+\s*[o\u00b0]\s*\d+'?\s*[NSEW]",re.I);aJ={"croppedtext":(7,6),"text":(5,4),"htmlgump":(6,5)}
	def cN(raw):
		b,e=aQ(raw);a,c,d=0,[],[]
		for t in e:
			try:
				k=t[0].lower()
				if k=="page":a=int(t[1])
				elif k=="button"and len(t)>=8:
					if int(t[5])==1:c.append((a,int(t[1]),int(t[2]),int(t[7])))
				elif k in aJ and len(t)>=aJ[k][0]:d.append((a,int(t[1]),int(t[2]),bI(b[int(t[aJ[k][1]])])))
			except(ValueError,IndexError):continue
		return b,c,d
	def dZ(text):
		t=text.strip()
		if not t or dX.match(t)or dY.search(t):return False
		return not re.match(r"^[\d\s/:.,-]+$",t)
	ae={}
	def cO(raw):
		j,h=aQ(raw);ae.clear();ae.update({"text_lines":len(j),"commands":len(h)})
		if h:ae["last_command"]=" ".join(h[-1])
		else:k=cM(raw);ae["last_line_repr"]=repr(k[-2]if len(k)>1 else k[-1])
		i,c={},None
		for t in h:
			try:
				m=t[0].lower()
				if m=="button"and len(t)>=8 and t[5]=="1":a=int(t[7]);c=a if a>=2 and(a-2)%6==0 else None
				elif m in("croppedtext","text")and c is not None:
					e=bI(j[int(t[-1])]);f=(c-2)//6
					if f not in i:i[f]=(e,c)
					c=None
				else:c=None
			except Exception as p:ae["error"]=str(p);c=None
		ae["sequential_pairs"]=len(i);b=[{"name":w,"slot":x,"button":y}for x,(w,y)in i.items()if w and w.lower()!="empty"]
		if b:return sorted(b,key=lambda d:d["name"].lower())
		j,l,n=cN(raw);ae.update({"buttons":len(l),"labels":len(n)})
		def o(btns):
			c={}
			for(e,g,h,f)in sorted(btns):
				if f in c:continue
				a=None
				for(i,j,k,l)in n:
					b,m=j-g,abs(k-h)
					if i!=e or m>12 or b==0:continue
					if 0<b<=60:d=b
					elif-150<=b<0:d=100-b
					else:continue
					if a is None or d<a[0]:a=(d,l,e)
				if a and dZ(a[1]):c[f]=(a[1],a[2])
			return c
		q=o([G for G in l if G[3]>=2 and(G[3]-2)%6==0]);b=[]
		for a,(e,v)in q.items():
			f=(a-2)//6
			if not any(H["slot"]==f for H in b):b.append({"name":e,"slot":f,"button":a})
		if not b:
			r=o(l);g={}
			for a,(e,s)in r.items():g.setdefault(s,[]).append((e,a))
			if g:
				u=max(sorted(g),key=lambda pg:len(g[pg]))
				for e,a in g[u]:b.append({"name":e,"slot":None,"button":a})
		return sorted(b,key=lambda d:d["name"].lower())
	d_=re.compile(r"^(max(imum)?\s*)?charges?\s*:?\s*(\d+)?\s*(/\s*(\d+))?$",re.I)
	def cP(raw):
		j,l=aQ(raw);a,b,d={},None,[];e=0
		for t in l:
			try:
				k=t[0].lower()
				if k=="page":e=int(t[1]);continue
				if k in("xmfhtmlgump","xmfhtmlgumpcolor","xmfhtmltok")and len(t)>=6:
					f=int(t[5])
					if f==1011296:b="cur"
					elif f==1011297:b="max"
					continue
				if k not in aJ or len(t)<aJ[k][0]:continue
				x,y,c=int(t[1]),int(t[2]),j[int(t[aJ[k][1]])]
			except(ValueError,IndexError):continue
			c=bI(c)
			if ch(c):
				if b and b not in a:a[b]=int(c);b=None
				else:d.append((e,x,y,int(c)))
				continue
			m=d_.match(c)
			if m:
				g="max"if m.group(1)else "cur"
				if m.group(3):
					a.setdefault(g,int(m.group(3)))
					if m.group(5):a.setdefault("max",int(m.group(5)))
				else:b=g
		if not a and len(d)>=2:
			(n,o,p,h),(q,r,s,i)=d[0],d[1]
			if n==q and abs(p-s)<=4 and r>o and h<=i:a={"cur":h,"max":i}
		return a.get("cur"),a.get("max")
	def bS(s):return(str(s).replace("%","%25").replace("|","%7C").replace(";","%3B").replace("\t","%09").replace("\n","%0A").replace("\r",""))
	def bT(s):return(s.replace("%0A","\n").replace("%09","\t").replace("%3B",";").replace("%7C","|").replace("%25","%"))
	def d0(s):return "".join(["%04X"%ord(a)for a in s])
	def d1(h):
		try:return "".join([chr(int(h[a:a+4],16))for a in range(0,len(h)-3,4)])
		except ValueError:return ""
	def aK(s):return int(s)if ch(s)else None
	def d2(path,text):Kit.write_safe(path,text)
	cQ="Grimoire_saved.txt";I={"data":None,"warned":False,"dirty":set(),"retry_at":0.}
	def bn():
		if I["data"]is None:
			I["data"]={};b=Kit.read_merge(bE(cQ))
			for a in cM(b):
				if "\t"in a:k,v=a.split("\t",1);I["data"][k]=v
		return I["data"]
	def bo(key,value):
		a=bn()
		if a.get(key)==value:return
		a[key]=value;I["dirty"].add(key)
	def cR(force=False):
		if not I["dirty"]or(not force and time.time()<I["retry_at"]):return
		a,I["dirty"]=I["dirty"],set();b=bn();d=bE(cQ)
		try:c=Kit.merge_save(d,dict((i,i+"\t"+b[i])for i in a),lambda l:l.split("\t",1)[0]if "\t"in l else None);e="couldn't read it first"
		except Exception as h:c,e=None,h
		if c is not None:
			for f in c:
				if "\t"in f:
					k,v=f.split("\t",1)
					if k not in I["dirty"]:b[k]=v
			return
		I["dirty"]|=a;I["retry_at"]=time.time()+30.
		if not I["warned"]:o("couldn't save to %s (%s)."%(d,e),E);I["warned"]=True
		for g in sorted(a):
			try:bG("Grimoire_H_"+g,d0(b[g]),True)
			except Exception:
				if not I["warned"]:o("couldn't save the runebook lists; they are read again next time.",E);I["warned"]=True
	def bp(key):
		v=bn().get(key)
		if v:return v
		h=bF("Grimoire_H_"+key);return d1(h)if h else ""
	def cS(serial):return "book_%08X"%int(serial)
	def bq(v):return ""if v is None else str(v)
	def d3(serial):
		a=C.get(serial)
		if a is None:return
		c,d=M.get(serial,(None,None));b=["v1",bq(c),bq(d)];b+=["|".join([bS(f["name"]),bq(f["slot"]),bq(f["button"]),str(f.get("rune")or "")])for f in a];bo(cS(serial),";".join(b))
	def d4(serial):
		a=bp(cS(serial)).split(";")
		if len(a)<3 or a[0]!="v1":return False
		b=[]
		for p in a[3:]:
			f=p.split("|")
			if len(f)!=4:continue
			d={"name":bT(f[0]),"slot":aK(f[1]),"button":aK(f[2])}
			if aK(f[3]):d["rune"]=aK(f[3])
			b.append(d)
		C[serial]=b;M[serial]=(aK(a[1]),aK(a[2]));return True
	def cT(serial,dests,charges):
		b=(C.get(serial,"none"),M.get(serial))
		if C.get(serial)and(dests is None or(not dests and serial in at)):return False
		C[serial]=dests
		if charges is not None:M[serial]=charges;aG.append(serial)
		if dests is not None:d3(serial)
		a=b!=(C.get(serial),M.get(serial))
		if a:cU(serial);z["ver"]+=1
		return a
	def ar(serial,index,name=None,taken=None):
		a=C.get(serial)
		if not a:return
		n=len(a)
		if 0<=index<n and(name is None or a[index]["name"]==name)and(taken is None or index not in taken):return index
		if name is None:return
		b=[(abs(d-index),d)for d in range(n)if a[d]["name"]==name and(taken is None or d not in taken)];return min(b)[1]if b else None
	def bU():
		b,c,a=set(),set(),[]
		for f in j["list"]:
			k=(f[0],f[1])if f[1]>=0 else(f[0],-1,f[2])
			if k in c:continue
			c.add(k);a.append(f)
			if f[1]>=0:b.add(k)
		if len(a)!=len(j["list"]):j["list"]=a;j["save"]=True
		j["keys"]=b
	def cU(serial):
		c=False;d=set();e=sorted([g for g in j["list"]if g[0]==serial],key=lambda f:(f[1]<0,f[1]))
		for b in e:
			i=ar(serial,b[1],b[2],d)
			if i is None:
				if b[1]!=-1:b[1]=-1;c=True
				continue
			d.add(i)
			if i!=b[1]:b[1]=i;c=True
		if c:bU();j["save"]=True
		a=j["last"]
		if a is not None and a[0]==serial:
			i=ar(serial,a[1],a[2])
			if i is not None and i!=a[1]:j["last"]=(serial,i,a[2],a[3]);j["save_last"]=True
	def d5():
		b="%08X"%int(API.Player.Serial)
		if b==j["owner"]:return
		if j["save"]or j["save_last"]:br()
		d=[];a=bp("favs_"+b).split(";")
		if a and a[0]=="v1":
			for p in a[1:]:
				f=p.split("|")
				if len(f)!=3:continue
				try:d.append([int(f[0],16),int(f[1]),bT(f[2])])
				except ValueError:continue
		c=None;a=bp("last_"+b).split(";")
		if len(a)==2 and a[0]=="v1":
			f=a[1].split("|")
			try:
				if len(f)==4 and f[3]in cj:c=(int(f[0],16),int(f[1]),bT(f[2]),f[3])
			except ValueError:c=None
		j.update({"list":d[:bK],"last":c,"owner":b,"save":False,"save_last":False});bU();z["ver"]+=1
	def br():
		b=j["owner"]
		if b is None:j["save"]=j["save_last"]=False;return
		if j["save"]:j["save"]=False;bo("favs_"+b,";".join(["v1"]+["%08X|%d|%s"%(d[0],d[1],bS(d[2]))for d in list(j["list"])]))
		if j["save_last"]:
			j["save_last"]=False;a=j["last"]
			if a is not None:bo("last_"+b,"v1;%08X|%d|%s|%s"%(a[0],a[1],bS(a[2]),a[3]))
	def d6(serial,index,name):
		a=(serial,index)
		if a in j["keys"]:j["list"]=[d for d in j["list"]if(d[0],d[1])!=a];b=False
		else:
			if len(j["list"])>=bK:o("Favourites is full (%d); take a star off first."%bK,E);return
			j["list"].append([serial,index,name]);b=True
		bU();j["save"]=True;z["ver"]+=1;return b
	def d7(serial,dest,method):
		a=next((f for f,g in enumerate(C.get(serial)or[])if g is dest),None)
		if a is None:a=ar(serial,0,dest.get("name"))
		if a is None:return
		j["last"]=(serial,a,dest.get("name")or "",method);j["save_last"]=True;z["ver"]+=1
	at={};T={"books":set()}
	def bs():return not T["written"]or T["armed"]
	def bV(text):
		if not bs():return
		T["written"],T["armed"]=True,False;a=bE("Grimoire_runebook_dump.txt")
		try:d2(a,text)
		except Exception as b:o("couldn't save the runebook details (%s)."%b,E);return
		o("saved the runebook details to %s."%a,L);return a
	def bW(serial,path):
		if path:
			b,T["books"]=T["books"],set([serial])
			for a in b:
				if a!=serial:F(lambda s=a:cb(s)if s in r else None)
	def cV(container):return F(lambda:["  0x%08X  graphic 0x%04X  hue 0x%04X  amount %d  name '%s'"%(a.Serial,a.Graphic,a.Hue,a.Amount or 0,a.Name or "")for a in list(API.ItemsInContainer(container)or[])])
	def cW(serial,read=False):
		nonlocal aa
		if aa and API.HasGump(aa):API.CloseGump(aa);P(.1)
		b=HOST.services.get("gump.expect")
		if b is not None and aa:b(aa,4.)
		if read and(m["claim"]or time.time()<N["hold"]):return("busy",None)
		d=API.HasGump();API.ConfigNextGump(serial=aa,isVisible=False);API.UseObject(serial)
		def e():
			a=API.HasGump()
			if a and(a==aa or a!=d):return("gump",a)
			b=API.FindItem(serial);return("container",None)if b and b.GetContainerGump()else None
		a=(None,"double-clicking the book opened nothing within 3 seconds");f=time.time()+3.
		try:
			while time.time()<f and P(.05):
				if read and m["claim"]:return("busy",None)
				c=F(e)
				if c is not None:a=c;break
		finally:API.ConfigNextGump()
		if(a[0]is None and F(lambda:len(list(API.ItemsInContainer(serial)or[])))):a=("container",None)
		if a[0]=="gump":aa=a[1]
		return a
	def d8(f):
		def i():a=API.FindItem(f);return((a.Name if a else "")or "").strip()
		a=F(i)
		if not a or a.lower()in("recall rune","a recall rune","rune"):
			with Kit.quiet:
				j=b0();k=time.time();API.ClickObject(f);l=k+1.;n=a.lower();b,g=None,0.
				while time.time()<l and not m["claim"]and P(.1):
					d=None
					for e in j.new():
						h=(e.name or "").lower();c=(e.text or "").strip()
						if not c or(h and h!=n)or c3(c):continue
						if "rune"in e.low:d=c;break
						if b is None:b,g=c,time.time()+.3
					if d is not None:a=d;break
					if b is not None and time.time()>=g:a=b;break
				else:
					if b is not None:a=b
		return re.sub(r"^(a |an )?(marked )?recall rune( for| to)?\s*","",a,flags=re.I).strip()
	def d9(serial):
		a=[];e=F(lambda:[d.Serial for d in list(API.ItemsInContainer(serial)or[])])
		for c in e or[]:
			b=d8(c)
			if m["claim"]:a=None;break
			if not b or "unmarked"in b.lower():continue
			a.append({"name":b,"slot":None,"button":None,"rune":c})
		def f():
			a=API.FindItem(serial);g=a.GetContainerGump()if a else None
			if g:g.Dispose()
		F(f);return "busy"if a is None else sorted(a,key=lambda d:d["name"].lower())
	def bX(gid):
		def a():g=API.GetGump(gid);return(g.PacketGumpText or "")if g else ""
		return F(a)
	def ea(serial):
		d,b=cW(serial,True)
		if d=="busy":return d,None
		at.pop(serial,None)
		if d=="container":
			c=d9(serial)
			if not c:
				at[serial]="The book opened like a bag, but no named runes were inside."
				if bs():bW(serial,bV("Runebook 0x%08X opened as a CONTAINER\n\n"%serial+"\n".join(cV(serial))))
			return c,None
		if d is None:
			at[serial]="Couldn't open it: "+b+"."
			if bs():bW(serial,bV("Runebook 0x%08X: %s\nLast server gump: 0x%08X\nItems inside:\n%s"%(serial,b,API.HasGump(),"\n".join(cV(serial))or "  (none known)")))
			return None,None
		a=bX(b)
		if not a:P(.1);a=bX(b)
		API.CloseGump(b);c=cO(a)if a else[]
		if not c:
			at.setdefault(serial,"The book's window didn't match any known layout.")
			if bs():e,f,g=cN(a)if a else([],[],[]);ae["selftest"]=dW();bW(serial,bV("Runebook 0x%08X  gump 0x%08X  (%d texts, %d buttons)\nparser: %r\n\n%s"%(serial,b,len(e),len(f),ae,a or "(empty PacketGumpText)")))
			return c,None
		return c,cP(a)
	def eb(b,gid):
		a=bX(gid)
		if not a:return
		c=cO(a)
		if c and cT(b,c,cP(a)):F(lambda:cb(b))
	def cX(serial,dest):
		a=[f for f in(C.get(serial)or())if f.get("name")==dest.get("name")and f.get("slot")is not None]
		for d in a:
			if d["slot"]==dest["slot"]:return d
		return a[0]if a else None
	def cY(a):
		c,b=cW(a)
		if c!="gump":o("the runebook did not open.",E);return
		eb(a,b);P(.1);return b
	def cZ(gid):API.CloseGump(gid);o("that rune isn't in the book any more; nothing was used.",E)
	ec=cr+("already casting","not allowed to travel","recall from this","gate from this","travel from this","location is blocked","too encumbered","heat of battle","doth not appear to work","is not marked","not yet marked")
	def bY(it):return max(1,int(it.Amount or 0))
	def ed(a):
		def b():n=sum(bY(d)for d in map(API.FindItem,a)if d);return bool(API.HasTarget("any")),n,(int(API.Player.X),int(API.Player.Y))
		return F(b)
	def bZ():
		if API.HasTarget("any"):o("a target cursor is up; finish it or press Esc first.",L);return True
		return False
	def ee(c,dest,method):
		f=aU if method=="gate_scroll"else aT;g="Gate Travel"if method=="gate_scroll"else "Recall";h=b0();i=b_();d=F(lambda:next(((n.Serial,bY(n))for n in aH()if n.Graphic==f),None))
		if not d:o("you have no %s scrolls."%g,E);return
		e,j=d;b=dest.get("rune")
		if not b:
			if dest["slot"]is None:o("scrolls need a standard runebook layout.",E);return
			a=cY(c)
			if a is None:return
			dest=cX(c,dest)
			if dest is None:return cZ(a)
			API.ConfigNextGump(serial=a,isVisible=False);API.ReplyGump(2+dest["slot"]*6+2,a);k=time.time()+2.
			while time.time()<k and P(.1):
				if API.HasGump(a):break
			API.ConfigNextGump();API.CloseGump(a)
			if not P(.3):return
			b=c
		if not c0():return
		if bZ():return
		bB(q,cp+1.)
		try:
			l=c1();API.CancelPreTarget();API.PreTarget(b,"neutral");API.UseObject(e)
			if c_((e,),j,h,i,l,cp)and API.HasTarget("any")and not au():API.Target(b)
		finally:API.CancelPreTarget();a5(q)
	def c_(a,before,since,me,start,timeout):
		b=time.time()+timeout
		while time.time()<b and P(.1):
			c,d,e=ed(a)
			if c:P(.15);return True
			if(before and d<before)or eg(since,me)or ef(start,e):return False
		return False
	def au():return HOST.cursor_busy(q)is not None
	def c0():
		a=time.time()+3.
		while au()and time.time()<a:
			if not P(.1):return False
		return True
	def c1():return F(lambda:(int(API.Player.X),int(API.Player.Y)))
	def b_():return F(lambda:API.Player.Name)or ""
	def ef(start,now):return start is not None and now is not None and max(abs(now[0]-start[0]),abs(now[1]-start[1]))>30
	def b0():Journal.update(True);return Journal.Reader()
	c2={"titles":None}
	def c3(text):
		i=text.find(": ")
		if i<=0 or i>60:return False
		a=c2["titles"]
		if a is None:
			a=set(["Virtue Assistant","Grimoire"])
			for b in HOST.slots:
				a.add(b.title)
				for p in b.parts:a.add(p[1]);a.add("%s > %s"%(b.title,p[1]))
			c2["titles"]=a
		return text[:i]in a
	def c4(lines,texts,me):
		for a in lines:
			b=a.name or ""
			if b and b!="System"and b!=me:continue
			c=a.low
			for f in texts:
				if f in c:
					if not c3(a.text or ""):return True
					break
		return False
	def eg(rd,me=""):return c4(rd.new(),ec,me)
	def eh(a,dest,method):
		if bZ():return
		if method in("recall_scroll","gate_scroll"):ee(a,dest,method);return
		if dest.get("rune"):
			c=dG.get(method,"Recall")
			if not c0():return
			if bZ():return
			bB(q,cq)
			try:e,f,g=b0(),c1(),b_();h=aD["BP"][1];d=F(lambda:[(l.Serial,bY(l))for l in aH(True)if l.Graphic==h])if c in("Recall","Gate Travel")else None;i=tuple(v for v,w in d or());j=sum(s for x,s in d or());API.CancelPreTarget();API.PreTarget(dest["rune"],"neutral");API.CastSpell(c);c_(i,j,e,g,f,cq)
			finally:API.CancelPreTarget();a5(q)
			return
		b=cY(a)
		if b is None:return
		if dest["slot"]is not None:
			dest=cX(a,dest)
			if dest is None:return cZ(b)
			API.ReplyGump(2+dest["slot"]*6+dF[method],b)
		else:API.ReplyGump(dest["button"],b)
		if(method=="charge"or dest["slot"]is None)and a not in u:u.append(a)
	A={"scale":1.}
	def e(v):return int(round(v*A["scale"]))
	def c5(parent,ctrl):
		if parent is c["g"]:
			t["tops"].append(ctrl)
			if t["hidden"]:ctrl.IsVisible=False
	def c6(layer,shown):
		for a in layer["tops"]:a.IsVisible=shown
		layer["hidden"]=not shown
	def ak(parent,ctrl,a):c5(parent,ctrl);parent.Add(ctrl);a.append(ctrl);return ctrl
	def U(parent,x,y,w,h,color,alpha,a):b=G.CreateGumpColorBox(alpha,color);b.SetRect(e(x),e(y),max(1,e(w)),max(1,e(h)));return ak(parent,b,a)
	def p(parent,text,x,y,size,color,a,width=0,align="left",smooth=False):
		b=aj.get(color)
		if b is not None and not smooth and not(width and align=="left"):l=G.CreateGumpLabel(text,b);l.SetAcceptMouseInput(False);c7(l,x,y,size,width,align);return ak(parent,l,a)
		size=max(6,e(size))
		if width:l=G.CreateGumpTTFLabel(text,size,color,aligned=align,maxWidth=e(width))
		else:l=G.CreateGumpTTFLabel(text,size,color)
		l.SetPos(e(x),e(y));l.SetAcceptMouseInput(False);return ak(parent,l,a)
	av={}
	def c7(l,x,y,size,width,align):
		a=int(l.GetWidth())or 7*len(l.Text or "");b=int(l.GetHeight())or 16;X=e(x)
		if width and align=="center":X+=max(0,(e(width)-a)//2)
		elif width and align=="right":X+=max(0,e(width)-a)
		Y=e(y)+max(0,(int(e(size)*1.3)-b)//2);l.SetPos(X,Y)
		if width and align!="left":
			if len(av)>3000:
				for k in[d for d in av if d.IsDisposed]:del av[k]
			av[l]=(x,y,size,width,align)
	def ei(l,text):
		l.Text=text;m=av.get(l)
		if m is not None:c7(l,m[0],m[1],m[2],m[3],m[4])
	def c8(parent,graphic,x,y,size,a):p=G.CreateGumpItemPic(graphic,e(size),e(size));p.SetPos(e(x),e(y));p.SetAcceptMouseInput(False);return ak(parent,p,a)
	def c9(parent,x,y,on,c):
		d=cn if on else co;a=[]
		for e,f,g,h in((6,0,2,4),(0,4,14,2),(3,6,8,3),(2,9,3,3),(9,9,3,3)):b=U(parent,x+e,y+f,g,h,d,1.,c);b.SetAcceptMouseInput(False);a.append(b)
		return a
	ej=dict((fx,tuple(int(fy[fz:fz+2],16)for fz in(1,3,5)))for fx,fy in((True,cn),(False,co)))
	def da(parts,on):
		r,a,b=ej[bool(on)]
		for p in parts:p.SetBaseColor(r,a,b,255)
	def af(ctrl,fn):G.AddControlOnClick(ctrl,fn)
	aZ={"ok":None}
	def db(a,fn):
		if aZ["ok"]is False:return False
		aZ["ok"]=Kit.hook_double(a,fn,queue=False)
		if not aZ["ok"]:o("double-clicks can't be caught on this client; click a row, then click it again to use it.",E)
		return aZ["ok"]
	def dc(key,action):
		def a():
			b=time.time();a=S["selected"]
			if a is not None and a!=key and a in ad:ad[a].SetAlpha(bc)
			if key in ad:ad[key].SetAlpha(.2)
			S["selected"]=key
			if aZ["ok"]is False and S["key"]==key and b-S["t"]<=3.:S["key"],S["t"]=None,0.;dg(b1(action,b))
			else:S["key"],S["t"]=key,b
		return a
	def b1(action,now=None):
		if action[0]=="cast":return action+(now or time.time(),)
		if action[0]in("travel","favgo"):return("pressed",now or time.time(),action)
		return action
	def dd(bg,key,action):af(bg,dc(key,action));db(bg,df(action))
	def de(i):
		if i!=b["circle"]or b["tab"]!="spells":dB("spells",lambda:b.update({"circle":i}))
	def df(action):
		def a():dg(b1(action))
		return a
	def dg(act):
		if act[0]=="cast"and N["reading"]and not b["shutting"]and m["wait"]is None and not m["claim"]and not au()and not API.HasTarget("any"):cc(act[1],Client.on_client_thread());return
		Q.add(act,dup=True)
	def al(action):
		def a():
			if action not in b["ui_queue"]:b["ui_queue"].append(action)
		return a
	def ag(name,default):
		try:return int(bF("Grimoire_"+name,str(default)))
		except Exception:return default
	def am(name,value):bG("Grimoire_"+name,str(int(value)))
	aw={"value":None,"t":0.}
	def dh():A["scale"]=min(a9,max(ai,ag("Scale",100)))/100.;c["w"]=max(e(aV),ag("W",e(cw)));c["h"]=max(e(aW),ag("H",e(cx)));c["opacity"]=min(100,max(0,ag("Opacity",bO)));bt()
	def bt():
		if D["own"]is not None:return
		W,H=Kit.screen()
		if H>0:c["h"]=max(aW*ai//100,min(c["h"],H))
		if W>0:c["w"]=max(aV*ai//100,min(c["w"],W))
	def LW():return max(aV,int(c["w"]/A["scale"]))
	def LH():return max(aW,int(c["h"]/A["scale"]))
	ah={"parts":[]}
	def ek():
		if b["minimized"]:return
		c["w"],c["h"]=c["g"].GetWidth(),c["g"].GetHeight();k["size_dirty"]=True;b["dirty"]=True;k["settle"]=time.time()+.3
	def di():
		k["size_dirty"]=False
		if D["own"]is not None:return
		for a,v in(("W",c["w"]),("H",c["h"])):am(a,v)
	def el():
		bt();a,b=ag("X",-1),ag("Y",-1)
		if a>=0:a,b=Kit.adapt(a,max(0,b),c["w"],c["h"]);a,b=Kit.clamp(a,b,c["w"],c["h"]);a,b=max(0,a),max(0,b)
		c["g"]=g=G.CreateModernGump(a if a>=0 else 100,b if b>=0 else 60,c["w"],c["h"],True,aV*ai//100,aW*ai//100,ek);g.SetAlpha(0)
		if a<0:g.CenterXInViewPort();g.CenterYInViewPort()
	fp=None
	def a_(a):
		for c in a:av.pop(c,None);c.Dispose()
		del a[:]
	b2={}
	def ax(graphic):
		if graphic not in b2:p=G.CreateGumpPic(graphic,0,0,0);b2[graphic]=(int(p.GetWidth()),int(p.GetHeight()));p.Dispose()
		return b2[graphic]
	def aL(parent,graphic,X,Y,W,H,a,mouse=False,hue=0):
		p=G.CreateGumpPic(graphic,X,Y,ci(graphic,hue));p.SetWidth(max(1,W));p.SetHeight(max(1,H))
		if not mouse:p.SetAcceptMouseInput(False)
		return ak(parent,p,a)
	def b3(parent,graphic,X,Y,W,H,a):t=G.CreateTiledGumpPic(graphic,max(1,W),max(1,H),ci(graphic));t.SetRect(X,Y,max(1,W),max(1,H));t.SetAcceptMouseInput(False);return ak(parent,t,a)
	def em(parent,x,y,w,h,q,alpha=1.):
		a,b,c,d=e(x),e(y),e(x+w),e(y+h);m,n=ax(bb);o,p=ax(bb+8);m,o=min(m,(c-a)//2),min(o,(c-a)//2);n,p=min(n,(d-b)//2),min(p,(d-b)//2);f=[a,a+m,c-o,c];g=[b,b+n,d-p,d];j=[]
		for i in[4,0,1,2,3,5,6,7,8]:
			k,l=i%3,i//3;W,H=f[k+1]-f[k],g[l+1]-g[l]
			if W<=0 or H<=0:continue
			if i in(0,2,6,8):j.append(aL(parent,bb+i,f[k],g[l],W,H,q))
			else:j.append(b3(parent,bb+i,f[k],g[l],W,H,q))
		for r in j:r.SetAlpha(alpha)
		return[(s,1.)for s in j]
	def a0(parent,x,y,w,h,a,alpha=1.):p=b3(parent,Kit.SECTION_TILE,e(x),e(y),e(w),e(h),a);p.SetAlpha(alpha*Kit.SECTION_ALPHA);return[(p,Kit.SECTION_ALPHA)]
	def en(w,h,d):a,b=ax(ce);W,H=e(w),e(h);return[aL(c["g"],ce,f,g,a,b,d)for f,g in((0,0),(W-a,0),(0,H-b),(W-a,H-b))]
	a1={}
	def b4(text):return int(round(Kit.text_px(text)/A["scale"]))
	def aM(text,room,size=None):
		if size is None:return Kit.fit(text,e(room))
		if b5(text,size)<=room:return text
		a,b=2,len(text)-1
		while a<b:
			c=(a+b+1)//2
			if b5(text[:c]+"..",size)<=room:a=c
			else:b=c-1
		return text[:a].rstrip()+".."
	def b5(text,size):
		a=(text,size,A["scale"])
		if a not in a1:
			if len(a1)>=4000:a1.clear()
			l=G.CreateGumpTTFLabel(text,max(6,e(size)),K);b=int(l.GetWidth()or 0);l.Dispose();a1[a]=b or int(.55*size*len(text))
		return int(round(a1[a]/A["scale"]))
	def dj(art):return int(round(ax(art[0])[0]/A["scale"]))
	def an(x,y,w,h,text,tooltip,fn,size=14,parent=None,art=a6):
		parent=parent or c["g"];a=t["ctrls"];g,i=ax(art[0]);b=G.CreateGumpButton("",0,art[0],art[1],art[2]);b.SetPos(e(x),e(y)+max(0,(e(h)-i)//2));ak(parent,b,a);af(b,fn);a7(b,tooltip)
		if text:d=x+int(round(g/A["scale"]))+4;p(parent,text,d,y+(h-size)//2-1,size,K,a);f=U(parent,d,y,max(4,x+w-d),h,aq,0.,a);af(f,fn);a7(f,tooltip)
		return b
	def eo():
		if aB(q)and not b["minimized"]:return
		aP(q,False);aN()
	def b6():
		if aB(q):return
		aP(q,True)
		if not b["minimized"]:aN()
		if bA():ay(True)
		else:HOST.dock_note(aS)
	def aN(save=True):
		b["minimized"]=not b["minimized"]
		if b["minimized"]:c["g"].SetResizable(False);c["g"].SetHeight(e(bM))
		else:c["g"].SetHeight(c["h"]);c["g"].SetResizable(D["own"]is None)
		ay(False);b["dirty"]=True
		if save:am("Min",1 if b["minimized"]else 0)
	def ep():
		a=aB(q)
		if not a:aP(q,False)
		if b["minimized"]:aN(not a)
		ay(False)
	def eq():
		if not b["minimized"]:aN()
	def er():ay(False)
	def dk():
		if aB(q):return
		x,y=int(c["g"].GetX()),int(c["g"].GetY());k["last_pos"]=(x,y)
		for a,v in(("X",x),("Y",y)):am(a,v)
	def ay(on):
		on=bool(on)
		if on==b["docked"]:return
		b["docked"]=on;c["g"].IsVisible=not on
	def dl():
		a=time.time()
		if a<b.get("link_next",0.):return
		b["link_next"]=a+.1
		if b.pop("to_bar",False):b6()
		c=API.GetSharedVar(bN)
		if c:
			API.RemoveSharedVar(bN);c=str(c)
			if c=="show"and(b["minimized"]or b["docked"]):
				aP(q,False)
				if b["minimized"]:aN()
				ay(False)
			elif c=="dock"and not b["docked"]:b6()
		if b["docked"]:
			if not bA():ay(False)
		elif b["minimized"]and a>=b.get("wish_next",0.):
			b["wish_next"]=a+.25
			if bC(q)and bA():ay(True)
		elif not b["minimized"]and a>=b.get("wish_next",0.):
			b["wish_next"]=a+1.
			if bC(q)and not aB(q):aP(q,False)
		d="docked"if b["docked"]else("minimized"if b["minimized"]else "open")
		if d!=b["link_state"]:b["link_state"]=d;API.SetSharedVar(cy,d)
	def es(value):
		c["opacity"]=int(value)
		for p,a in ah["parts"]:p.SetAlpha(c["opacity"]/100.*a)
		am("Opacity",c["opacity"])
	def et(value):aw["value"]=int(value);aw["t"]=time.time()
	def b7():c["g"].SetWidth(c["w"]);c["g"].SetHeight(e(bM)if b["minimized"]else c["h"]);b["dirty"]=True
	def dm(new,w,h):
		for k,v in(("Scale",int(round(new*100))),("W",w),("H",h)):am(k,v)
	def dn(new,save):
		if abs(new-A["scale"])<.001:return
		a=new/A["scale"];A["scale"]=new;c["w"],c["h"]=int(round(c["w"]*a)),int(round(c["h"]*a));b,d=c["w"],c["h"];bt();b7()
		if save:dm(new,b,d)
	def do():
		e=aw["value"];aw["value"]=None;a=min(a9,max(ai,e))/100.
		if D["own"]is None:dn(a,True);return
		if abs(a-D["own"][0])<.001:return
		c=int(round(D["own"][1]*a/D["own"][0]));d=int(round(D["own"][2]*a/D["own"][0]));dn(a,False);D["own"]=(a,c,d);dm(a,c,d)
		if D["told"]is not None:b["ui_queue"].append(("fit",)+D["told"])
	D={"own":None,"told":None}
	def eu(w,h,mode):D["told"]=(w,h)if w else None;b["ui_queue"].append(("fit",w,h))
	def ev(w,h):
		if not w:
			a,D["own"]=D["own"],None
			if a is not None:A["scale"]=a[0];c["w"],c["h"]=a[1],a[2];bt();b7();c["g"].SetResizable(not b["minimized"])
			return
		if D["own"]is None:D["own"]=(A["scale"],c["w"],c["h"]);c["g"].SetResizable(False);b["dirty"]=True
		w,h=int(w),int(h)
		if b["minimized"]:h=c["h"]
		if(c["w"],c["h"])!=(w,h):c["w"],c["h"]=w,h;b7()
	a2=48
	def ew():
		w=LW();h=bM if b["minimized"]else LH();a=t["ctrls"];e=c["opacity"]/100.;ah["parts"]=em(c["g"],0,0,w,h,a,e);g=[i for i,l in ah["parts"]];d=aB(q);f=A["scale"]
		if d:A["scale"]=1.;w=c["w"]
		try:ah["parts"]+=a0(c["g"],12,12,w-24,30,a,e)
		finally:A["scale"]=f
		if not b["minimized"]:g+=en(LW(),h,a);ah["parts"]+=a0(c["g"],12,h-40,LW()-24,28,a,e)
		Kit._frame_parts[c["g"]]=g
		if d:A["scale"]=1.
		try:ex(w,d)
		finally:A["scale"]=f
		return max(50,int(-(-50//f)))if d else 50
	def ex(w,a):
		d=t["ctrls"];p(c["g"],"GRIMOIRE",42,18,14,V,d);f=w-12-44-20-(0 if b["minimized"]else Kit.DOCK_DX+106+98);d.append(Kit.title_catcher(c["g"],e(12),e(12),e(f-16),e(30),al(("min_click",)),key="grimoire:mini"if b["minimized"]else "grimoire"));x=w-12-44
		if not a:an(x,15,30,24,"",Kit.CLOSE_TIP%aS,al(("close",)),art=Kit.ART_CLOSE);x-=20;an(x,15,16,24,"",Kit.RESTORE_TIP if b["minimized"]else Kit.MIN_TIP,al(("min_click",)),art=Kit.ART_RESTORE if b["minimized"]else Kit.ART_MIN)
		if not b["minimized"]:
			if not a:x-=Kit.DOCK_DX;an(x,15,16,24,"",Kit.DOCK_TIP,lambda:b.__setitem__("to_bar",True),art=Kit.ART_DOCK)
			x-=106;an(x,15,100,24,"Settings",Kit.SETTINGS_TIP%aS,al(("settings",)),art=cd);x-=98;an(x,15,92,24,"Refresh","Find your spellbook and runebooks again and reread every runebook",Q(("refresh",)),art=bD)
	def bu():return LW()-ao-20
	def b8(key):return key not in("spells","favs","+add")and not isinstance(key,tuple)
	def a3(serial):a=M.get(serial,(None,None))[0];return a is not None and a<ck
	def dp(key,title,short):
		a=title if short!=title else None
		if b8(key)and a3(key):b=M[key][0];a="%s: %s left (low)"%(title,aA(b,"charge"))
		return a
	def dq(key,x,y,w,h,text,tooltip,title=None):
		d=t["ctrls"];n=b["tab"]==key;j=R if b8(key)and a3(key)else K;f,g=ax(cz);k,l=e(x),e(y)+max(0,(e(h)-g)//2);aL(c["g"],cz,k,l,f,g,d);a=aL(c["g"],dI,k,l,f,g,d);a.SetAlpha(1. if n else 0.);o=p(c["g"],text,x+int(round(f/A["scale"]))+4,y+(h-14)//2-1,14,j,d);i=U(c["g"],x,y,w,h,aq,0.,d);m=ez(key);af(i,m);af(a,m)
		if tooltip:i.SetTooltip(tooltip);a.SetTooltip(tooltip)
		bi[key]=a
		if b8(key):bj[key]=(o,i,a,title or text,text,j==R)
	def ey(serial):
		a=bj.get(serial);b=a3(serial)
		if a is None or a[5]==b:return
		d,e,f,c,g,i=a;d.Hue=aj[R if b else K];bj[serial]=(d,e,f,c,g,b);h=dp(serial,c,g)or c;e.SetTooltip(h);f.SetTooltip(h)
	def ez(key):
		def a():b["switch"]=key
		return a
	def eA(top):
		m=[("spells","Spellbook")]+([("favs","Favourites")]if B else[])+[(n["serial"],n["title"])for n in B];f=bu();g=28;h,x,y=[],20,top+4;i=dj(bD)
		for d,a in m:
			e=a if len(a)<18 else a[:16]+"..";w=max(90,i+4+b4(e)+14)
			if x+w>f-4:x,y=20,y+g
			h.append((d,a,e,x,y,w));x+=w+6
		if b["scanned"]:
			a="Add runebook...";w=max(90,i+4+b4(a)+14);j=f-4-w
			if x>j:y+=g
			h.append(("+add",a,a,j,y,w))
		k=y+g+2;l=c["opacity"]/100.;ah["parts"]+=a0(c["g"],12,top,f-12,k-top,t["ctrls"],l)
		for d,a,e,x,y,w in h:
			if d=="+add":an(x,y,w,24,e,"Target an unlisted runebook; books of its kind are found from then on",Q(("register",)),art=bD)
			elif d=="favs":dq(d,x,y,w,24,e,"Starred destinations, last trip and a search of every runebook")
			else:dq(d,x,y,w,24,e,dp(d,a,e),a)
		top=k+Kit.GAP;ah["parts"]+=a0(c["g"],12,top,f-12,LH()-a2-top,t["ctrls"],l);b["content_top"]=top+4;return top+4
	def bv(x,y,w,h):a=G.CreateGumpScrollArea(e(x),e(y),e(w),e(max(40,h)));t["ctrls"].append(a);return a
	def bw(ctrl):c5(c["g"],ctrl);c["g"].Add(ctrl)
	def eB(top):
		a=t["ctrls"];f=LW()-ao-12;h=LH()-a2;ah["parts"]+=a0(c["g"],f,top,ao,h-top,a,c["opacity"]/100.);p(c["g"],"Supplies",f,top+8,15,V,a,width=ao,align="center");i=[aD[v]for v in dL];i+=[None,("Recall scroll",aT),("Gate scroll",aU)];j,l=40,34;o=sum(10 if w is None else j for w in i);g=top+32
		if g+o<=h:d,e,m,b=c["g"],f,g,None
		else:b=bv(f+2,g,ao-2,h-g-4);d,e,m=b,0,0
		q=bl();y=m
		for r in i:
			if r is None:U(d,e+10,y+4,ao-20-(16 if b else 0),1,J,.6,a);y+=10;continue
			s,k=r;c8(d,k,e+8,y+(j-l)//2,l,a);n=q.get(k,0);u=p(d,bm(n),e+48,y+3,15,K if n else R,a);t["counts"].append(cI(k,u,n));p(d,aM(s,ao-52-(16 if b else 0)),e+48,y+21,12,K,a);y+=j
		if b is not None:bw(b)
	def eC(top,circle):
		b=t["ctrls"];s=bu();x=22;D,E=ax(cA);w=max(1,D*30//E)
		for i in range(8):
			l=aL(c["g"],cA+i,e(x),e(top+2),e(w),e(30),b,mouse=True)
			if circle!=i:l.SetAlpha(.45)
			af(l,al(("circle",i)));l.SetTooltip(bd[i][0]);x+=w+6
		F,G=bd[circle];p(c["g"],F,x+10,top+6,18,V,b);top+=38
		if not Z:p(c["g"],"No spellbook in your pack or hands. Carry one, then click Refresh.",22,top+4,14,J,b);return
		d=bv(16,top,s-20,LH()-top-a2-4);m=100;u=bl();H=circle*8;n=s-34;o=ba+18;I=n-4*aE-6;L=k["mana"]
		for i,(g,v,z)in enumerate(G):
			y=i*m;a=aF is None or cD(g)in aF;A=("spell",g);h=U(d,0,y,n,m-4,aq,bc,b);ad[A]=h;f=[g,[aD[W][1]for W in z.split()],ds[circle],None,None,h,None]
			if a:f[6]=dt(f,u,L)
			B=a and f[6][0];M=f[4]=aL(d,2240+H+i,e(8),e(y+(m-4-ba)//2),e(ba),e(ba),b,hue=0 if a else 946)
			if B:M.SetAlpha(dr)
			f[3]=p(d,g,o,y+14,17,(J if B else K)if a else ap,b);p(d,v if a else v+"  (not in your book)",o,y+38,13,J if a else ap,b,width=max(120,I-o-8));C=z.split();j=n-len(C)*aE-6
			for N in C:
				O,q=aD[N];P=c8(d,q,j+(aE-bf)//2,y+2,bf,b)
				if not a:P.SetAlpha(.4)
				r=u.get(q,0);Q=p(d,bm(r),j,y+bf+3,13,(K if r else R)if a else ap,b,width=aE,align="center");t["counts"].append(cI(q,Q,r,a));p(d,O,j,y+bf+20,11,J if a else ap,b,width=aE,align="center");j+=aE
			if a:dd(h,A,("cast",g));h.SetTooltip(du(f));t["spells"].append(f)
		bw(d)
	dr=.45;eD=dict((fB,fA)for fA,fB in aD.values());ds=Kit.SPELL_MANA
	def dt(a,totals,mana):
		for b in a[1]:
			if totals.get(b,0)<=0:return(True,"Out of "+eD.get(b,"a reagent"))
		if mana is not None and mana<a[2]:return(True,"Not enough mana (needs %d)"%a[2])
		return(False,"")
	def du(a):
		b="Double-click to cast "+a[0]
		if a[6]is not None and a[6][0]:b+="\n"+a[6][1]
		return b
	def dv():
		b=k["totals"]
		if b is None:return
		d=k["mana"]
		for f in list(r.values()):
			for e in f["spells"]:
				a=dt(e,b,d)
				if a==e[6]:continue
				e[6]=a;c=a[0];e[3].Hue=aj[J if c else K];e[4].SetAlpha(dr if c else 1.);e[5].SetTooltip(du(e))
	def eE(now):
		if(now<k["next_mana"]and k["next_mana"]-now<=cm)or b["tab"]!="spells"or b["minimized"]or b["docked"]:return
		k["next_mana"]=now+cm;a=int(API.Player.Mana);c=sum(1 for d in ds if d<=a);k["mana"]=a
		if c!=k["tier"]:k["tier"]=c;dv()
	def eF(serial):
		a,b=M.get(serial,(None,None))
		if a is None:return None,1
		if b is None:return "Charges: %d"%a,a
		return "Charges: %d / %d"%(a,b),a
	def eG(top,serial):
		a=t["ctrls"];h=bu();N=next((bg for bg in B if bg["serial"]==serial),None)
		if N is None:
			if serial==b["tab"]:b["switch"]="spells"
			return
		p(c["g"],N["title"],22,top+2,cB,V,a,smooth=True);an(h-104,top+4,96,26,"Re-read","Read this runebook again",al(("reread",serial)),size=15,art=cd)
		if serial not in C:
			p(c["g"],"Reading this runebook",22,top+36,14,J,a)
			if serial in u:u.remove(serial)
			Q.add(("read",serial));return
		O,P=eF(serial)
		if O:p(c["g"],O,h-340,top+6,20,V if P and not a3(serial)else R,a,width=226,align="right",smooth=True)
		e=C[serial]
		if e is None or(not e and serial in at):ag=at.get(serial,"Couldn't read this runebook.");p(c["g"],ag,22,top+36,14,R,a,width=h-26);p(c["g"],"Details saved to Grimoire_runebook_dump.txt in the VirtueAssistantSettings folder; send that file, then click Refresh."if serial in T["books"]else "Click Re-read to save this book's details to Grimoire_runebook_dump.txt in the VirtueAssistantSettings folder.",22,top+62,12,J,a,width=h-26);return
		if not e:p(c["g"],"No runes in this runebook. Add some, then click Re-read.",22,top+36,14,J,a);return
		z=bl();t["scrolls"]=cJ(z);S={"recall_scroll":z.get(aT,0),"gate_scroll":z.get(aU,0),"charge":P};ah=M.get(serial,(None,None))[0]is not None;A=len(e);W=any(fn["slot"]is not None for fn in e);ai=W or any(fq.get("rune")for fq in e);p(c["g"],"%s; double-click a name to %s there"%(aA(A,"destination"),aC),22,top+36,be,J,a,smooth=True);D=dj(a6);q=[]
		if ai:
			for m,n,r in dM:
				if m=="charge"and not W:continue
				q.append((m,n,r,max(D+12,b5(n,be)+12)))
		X=sum(fr[3]for fr in q);s=top+62;Y=s+26;E=h-34;aj=200+X+16;v=max(1,min(A,E//aj));i=E//v;F=i-X-20;Z=(A+v-1)//v;aa=LH()-Y-a2-4;f=max(36,min(54,aa//max(1,Z)));o=max(16,int((f-4)*.72));ak=int(o*1.3)
		for w in range(v):
			hx=16+w*i+F+16;p(c["g"],"Destination",16+w*i+30,s,be,V,a,smooth=True)
			for m,n,r,k in q:am=V if S.get(m,1)else R;p(c["g"],n,hx,s,be,am,a,width=k,align="center",smooth=True);hx+=k
		U(c["g"],18,s+23,E-4,1,J,.5,a);g=bv(16,Y,h-20,aa);ao=t["stars"]
		for x,d in enumerate(e):
			w,ap=divmod(x,Z);l,y=w*i,ap*f;ab=("rune",serial,d["button"],d["name"]);G=U(g,l,y,i-6,f-4,aq,bc,a);ad[ab]=G;ac=d["slot"]is not None;ar=bool(d.get("rune"));dd(G,ab,("travel",serial,d,b9(d)));G.SetTooltip("Double-click to %s to %s"%(aC,d["name"]));ao[x]=c9(g,l+8,y+max(0,(f-4-14)//2),(serial,x)in j["keys"],a);ae=U(g,l+2,y,26,f-4,aq,0.,a);af(ae,al(("star",serial,x,d["name"])));ae.SetTooltip(dw);ty=y+max(0,(f-4-ak)//2)
			if not(ac or ar):p(g,aM(d["name"],i-46,o),l+30,ty,o,K,a,smooth=True);continue
			p(g,aM(d["name"],F-24,o),l+30,ty,o,K,a,smooth=True);H=l+F+16
			for m,n,r,k in q:
				if m=="charge"and not ac:H+=k;continue
				I=S.get(m,1);L=r
				if m in("recall_scroll","gate_scroll"):L+=" (%d carried)"%I
				elif m=="charge"and ah:L+=" (%d left)"%I
				au=an(H+(k-D)//2,y+2,D,f-8,"",L,df(("travel",serial,d,m)),parent=g)
				if not I:au.SetAlpha(.35)
				H+=k
		bw(g)
	def b9(dest):return aC if dest["slot"]is not None or dest.get("rune")else "charge"
	dw="Add to Favourites (click again to remove)";dx={"recall":"recall","gate":"gate","charge":"recall (a charge)","recall_scroll":"recall (a scroll)","gate_scroll":"gate (a scroll)","sacred":"travel (Sacred Journey)"}
	def eH(top):a=t["ctrls"];b=bu();p(c["g"],"Favourites",22,top+2,cB,V,a,smooth=True);f=220;g=b-8-f;h="Search:";p(c["g"],h,g-10-b4(h),top+8,14,K,a);b3(c["g"],Kit.FIELD_TILE,e(g)-2,e(top+4)-1,e(f)+4,24,a);d=G.CreateGumpTextBox(ab["text"],e(f),22,False,16);d.SetPos(e(g),e(top+4));a7(d,"Search every runebook you carry by rune or book name (empty: your Favourites)");ak(c["g"],d,a);l=p(c["g"],"",22,top+38,14,J,a);i=top+62;j=b-34;k=bv(16,i,b-20,LH()-i-a2-4);ab.update({"layer":t,"tb":d,"info":l,"sa":k,"pool":[],"seen":None,"ver":-1,"row_w":j,"name_w":max(120,int(j*.55)),"info_w":b-30});dy(building=True);bw(k)
	def eI():
		c=dict((v["serial"],v["title"])for v in B);h=[w["serial"]for w in B]
		if not h:return[],"No runebooks in your pack or hands."
		q=ab["text"].strip().lower();a=[]
		if q:
			o=q.split();k=False
			for s in h:
				l=C.get(s)or();p=c[s].lower()
				for i in range(len(l)):
					r=l[i]["name"].lower()+"  "+p
					if all(x in r for x in o):
						if len(a)>=a8:k=True;break
						a.append((s,i,l[i]["name"],c[s],None,False))
				if k:break
			if k:return a,"More than %d found; type more letters."%a8
			if a:return a,"%s found; double-click one to %s there"%(aA(len(a),"destination"),aC)
			return a,"No rune or runebook name has '%s' in it."%ab["text"].strip()
		b=j["last"]
		if b is not None and b[0]in c:
			i=ar(b[0],b[1],b[2])
			if i is not None:a.append((b[0],i,b[2],c[b[0]],b[3],True))
		e={}
		for d in j["list"]:e.setdefault(d[0],[]).append(d)
		g=0
		for s in list(e):
			if s not in c:g+=len(e.pop(s))
		n=0
		for s in h:
			for d in sorted(e.get(s,()),key=lambda f:f[1]):
				i=ar(s,d[1],d[2])
				if i is None:g+=1;continue
				a.append((s,i,d[2],c[s],None,False));n+=1
		if n:m="%s; double-click one to %s there, or type above to search"%(aA(n,"favourite"),aC)
		else:m="Click a destination's star on a runebook page to list it here."
		if g:m+="  (%d not in the books you carry)"%g
		return a[:a8+1],m
	def dy(building=False):
		a=ab;d=a["layer"]
		if d is None or(r.get("favs")is not d and not building):a["layer"]=None;return
		c,e=eI();a["ver"],a["seen"]=z["ver"],a["text"];bH(a["info"],aM(e,a["info_w"]),aj[J]);b=a["pool"]
		for i in range(len(c)):
			if i>=len(b):b.append(eJ(i,c[i]))
			dA(b[i],c[i])
		for i in range(len(c),len(b)):dA(b[i],None)
	def eJ(i,row):f=ab;d,e,c=f["sa"],f["layer"]["ctrls"],30;y=i*c;b={"i":i,"a":None,"prev":None,"at":0.,"tip":None,"shown":True};b["bg"]=U(d,0,y,f["row_w"],c-4,aq,bc,e);ad[("fav",i)]=b["bg"];b["on"]=(row[0],row[1])in j["keys"];b["star"]=c9(d,8,y+(c-4-14)//2,b["on"],e);b["hit"]=U(d,2,y,26,c-4,aq,0.,e);b["hit"].SetTooltip(dw);b["name"]=p(d,"",32,y+(c-4-14)//2-2,14,K,e);b["book"]=p(d,"",32+f["name_w"]+10,y+(c-4-14)//2-2,14,J,e);af(b["hit"],ca(b,lambda a:al(("star",a[0],a[1],a[2]))()));af(b["bg"],ca(b,lambda a:dc(("fav",b["i"]),("favgo",)+a)()));db(b["bg"],ca(b,lambda a:Q.add(b1(("favgo",)+a),dup=True)));return b
	def dz(slot,shown):
		slot["shown"]=shown
		for a in[slot["bg"],slot["hit"],slot["name"],slot["book"]]+slot["star"]:a.IsVisible=shown
	def dA(slot,row):
		if row is None:
			if slot["a"]is not None:slot["prev"],slot["at"],slot["a"]=slot["a"],time.time(),None
			if slot["shown"]:dz(slot,False)
			return
		d=(row[0],row[1],row[2],row[4],row[5])
		if slot["a"]!=d:slot["prev"],slot["at"],slot["a"]=slot["a"],time.time(),d
		if not slot["shown"]:dz(slot,True)
		a=ab;bH(slot["name"],aM(("Last: "if row[5]else "")+row[2],a["name_w"]-4),aj[K]);f=row[3]+((", "+dx.get(row[4],row[4]))if row[4]else "");bH(slot["book"],aM(f,a["row_w"]-a["name_w"]-46),aj[J]);b=(row[0],row[1])in j["keys"]
		if b!=slot["on"]:da(slot["star"],b);slot["on"]=b
		e=C.get(row[0])or();m=row[4]or(b9(e[row[1]])if row[1]<len(e)else aC);c="Double-click to %s to %s (%s)"%(dx.get(m,m),row[2],row[3])
		if c!=slot["tip"]:slot["tip"]=c;a7(slot["bg"],c)
	def ca(slot,go):
		def a():
			a=slot["prev"]if slot["prev"]is not None and time.time()-slot["at"]<.15 else slot["a"]
			if a is not None:go(a)
		return a
	def eK(now):
		a=ab
		if a["layer"]is None:return
		if r.get("favs")is not a["layer"]:a["layer"]=None;return
		if b["tab"]!="favs"or b["minimized"]or b["docked"]:return
		if now>=a["next"]or a["next"]-now>cl:a["next"]=now+cl;a["text"]=str(a["tb"].Text or "")
		if a["text"]!=a["seen"]or a["ver"]!=z["ver"]:dy()
	def eL(act):
		a,d,b,e=act[1],act[2],act[3],act[4];i=ar(a,d,b)
		if i is None:o("%s isn't in that runebook any more."%b,E);return
		c=C[a][i];return("travel",a,c,e or b9(c))
	def aO(tab):return("spells",b["circle"])if tab=="spells"else tab
	def a4(key,hidden):
		nonlocal t;a=r.pop(key,None);c=t=cC(hidden)
		try:
			if isinstance(key,tuple):eC(b["content_top"],key[1])
			elif key=="favs":eH(b["content_top"])
			else:eG(b["content_top"],key)
		finally:t=ac
		r[key]=c
		if a is not None:a_(a["ctrls"])
		return c
	def cb(key):
		if b["minimized"]or b["dirty"]:
			if key in r:a_(r.pop(key)["ctrls"])
			return
		a4(key,key!=aO(b["tab"]))
	def eM():
		a=[("spells",d)for d in range(len(bd))]
		if B:a.append("favs")
		a+=[f["serial"]for f in B if f["serial"]in C];return a
	def dB(tab,d=None):
		c=aO(b["tab"])
		if d:d()
		b["tab"]=tab;am("Tab",0 if tab=="spells"else(bL if tab=="favs"else tab));am("Circle",b["circle"])
		if tab=="spells":k["next_mana"]=0.
		a=aO(tab)
		if a==c and a in r and not r[a]["hidden"]:return
		S["selected"]=None
		if c in r:c6(r[c],False)
		if a in r:c6(r[a],True)
		else:a4(a,False)
	def eN(key):
		for k,a in bi.items():a.SetAlpha(1. if k==key else 0.)
		dB(key)
	def eO():
		if b["minimized"]:return False
		a=[d for d in eM()if d not in r]
		if a:a4(a[0],a[0]!=aO(b["tab"]))
		k["next_prebuild"]=time.time()+cs;return bool(a)
	def dC():
		d=ac["ctrls"][:]
		for e in("ctrls","tops","counts"):del ac[e][:]
		f=list(r.values())
		for g in(r,ad,bi):g.clear()
		S["selected"]=None;b["dirty"]=False;a=ew()
		if not b["minimized"]:eB(a);eA(a);p(c["g"],b["status"],30,LH()-35,12,J,ac["ctrls"]);a4(aO(b["tab"]),False);k["next_prebuild"]=time.time()+cs
		a_(d)
		for h in f:a_(h["ctrls"])
	def eP(full=False,bags=True):nonlocal Z,aF;bn();d5();Z=F(dN);aF=dP(force=full);F(lambda:eQ(full,bags))
	def eQ(full,bags):
		nonlocal B;B=dV();del u[:]
		for d in B:
			s=d["serial"];c=s in C or d4(s)
			if full or not c:u.append(s)
			if c and s not in aY:aY[s]=M.get(s,(None,None))[0]
			if c and C.get(s):cU(s)
		z["ver"]+=1;a=b.pop("want_tab",None)
		if a and(any(f["serial"]==a for f in B)or(a==bL and B)):b["tab"]="favs"if a==bL else a
		if b["tab"]in u:u.remove(b["tab"]);u.insert(0,b["tab"])
		if(b["tab"]=="favs"and not B)or(b["tab"]not in("favs","spells")and not any(g["serial"]==b["tab"]for g in B)):b["tab"]="spells"
		e=("All spells shown"if aF is None else "%d spells known"%len(aF));b["status"]="%s, %s"%(e if Z else "No spellbook",aA(len(B),"runebook"))
		if not B and bags and(full or not b["reported"]):dS();b["reported"]=True
		b["scanned"]=True;b["dirty"]=True
	def eR(serial):
		a,b=ea(serial)
		if a=="busy":
			if serial not in u:u.insert(0,serial)
			return
		if cT(serial,a,b):F(lambda:cb(serial))
	def eS():b["closed"]=True
	def eT(act,now):
		if 0<=now-act[1]<=3.:dD[act[2][0]](act[2],now)
		else:o("trip not made; Grimoire was busy with a runebook. Press it again.",L)
	def eU(act,now):
		if len(act)>2 and now-act[2]>cu:o("%s was not cast; Grimoire was busy with a runebook."%act[1],L)
		elif m["wait"]is not None:pass
		elif au():m["wait"]=(act[1],now+cu);o("target cursor in use; %s is cast once it is free."%act[1],L)
		else:cc(act[1])
	def eV(act,now):
		if act[1]in u:u.remove(act[1])
		if now<N["hold"]or b["pick"]is not None or m["claim"]or m["wait"]is not None or au()or API.HasTarget("any"):u.insert(0,act[1])
		else:O.append(act)
	def bx(act,now):
		if act[0]=="refresh":T["armed"]=True
		O.append(act)
	def eW(act,now):
		a=eL(act)
		if a is not None:O.append(a)
	def eX(act,now):
		if dU(act[1]):Q.add(("scan",),dup=True,front=True)
	dD={"pressed":eT,"cast":eU,"read":eV,"travel":bx,"scan":bx,"rescan":bx,"refresh":bx,"favgo":eW,"register":lambda act,now:dT(),"registered":eX}
	def eY(w):return(("WINDOW",(("slider","opacity","Background opacity:","How solid the stone and black backdrop are (0-100, 0 = see-through)",0,100),("slider","scale","Scale:","Size of everything in the window (%d-%d%%, applied when the slider stops)"%(ai,a9),ai,a9),("note","Drag a window corner to resize.",{"ndy":2})),{"sh":124}),)
	eZ={"top":34,"fh":30,"ldy":0,"sdy":4,"lw":178,"sw":200,"ugap":12,"vfmt":"%d%%"}
	def e_(a,new):
		if new["opacity"]!=a["opacity"]:es(new["opacity"])
		if new["scale"]!=a["scale"]:
			et(new["scale"])
			if not aR(c["g"]):do()
	by=Kit.Page(aX,eY,None,e_,eZ)
	def e0(g,x,y,w):
		if not aX["loaded"]and not aR(c["g"]):aX["loaded"]=True;dh()
		aX.update({"opacity":c["opacity"],"scale":int(round(A["scale"]*100))});by.build(g,x,y,w)
	k={};az={};O=[];m={"rd":None,"me":""}
	def e1():
		nonlocal t;b.update({"tab":"spells","circle":0,"dirty":True,"closed":False,"queue":[],"ui_queue":[],"status":"Reading your books","minimized":False,"switch":None,"content_top":0,"shutting":False,"scanned":False,"reported":False,"docked":False,"link_state":None,"pick":None})
		for a in("ctrls","tops","counts"):del ac[a][:]
		for d in(r,ad,bi,bj,av,aY,bP):d.clear()
		for c in(O,u,aG):del c[:]
		t=ac;ah["parts"]=[];k.update({"next_count":0.,"next_prebuild":0.,"last_pos":(None,None),"held":None,"totals":None,"settle":0.,"size_dirty":False,"mana":None,"tier":None,"next_mana":0.});az["busy"],az["at"]=False,0.;ab.update({"layer":None,"tb":None,"info":None,"sa":None,"pool":[],"text":"","seen":None,"ver":-1,"next":0.});z["ver"]+=1;z["dest_ver"]=-1;m.update({"wait":None,"claim":0.,"seen":False,"next":0.});T.update({"written":False,"armed":False});aI.clear();aI.update(cE())
	def e2():
		if b["closed"]or b["shutting"]or not aR(c["g"]):return
		return "docked"if b["docked"]else("minimized"if b["minimized"]else "open")
	def e3():
		e1();Q.add(("scan",),dup=True);D["own"]=None;dh();b["circle"]=max(0,min(len(bd)-1,ag("Circle",0)));b["want_tab"]=ag("Tab",0)or None;el();G.AddControlOnDisposed(c["g"],eS);G.AddGump(c["g"]);Kit.on_moved(c["g"],dk);HOST.dock_add(q,{"title":aS,"icon":bJ[0],"state":e2,"show":ep,"minimize":eq,"dock":b6,"undock":er,"gump":lambda:c["g"],"fit":eu,"exact":True,"verify":True,"min":lambda:(e(aV),e(aW))});bh.add(HOST.dock_remove,q);D["own"],D["told"]=None,None;bh.service("look.grimoire",lambda:b.update(dirty=True))
		if ag("Min",0)==1 or bC(q):aN()
		API.RemoveSharedVar(bN);dl();HOST.alert_kind("grimoire.charges","Runebook low on charges",490)
		for a,d in fd.items():bh.service(a,d)
	def e4(act):
		a=act[0]
		if a=="min_click":eo()
		elif a=="circle":
			i=act[1]
			if("spells",i)in r and not b["dirty"]:de(i)
			else:b["switch"]=("spells",i)
		elif a=="settings":HOST.show_settings(q)
		elif a=="fit":ev(act[1],act[2])
		elif a=="close":cf(c["g"])
		elif a=="reread":T["armed"]=True;Q.add(("read",act[1]),dup=True)
		elif a=="star":
			d,i=act[1],act[2];e=d6(d,i,act[3])
			if e is None:return
			f=r.get(d);g=f["stars"].get(i)if f is not None else None
			if g is not None:da(g,e)
	def cc(name,b=False):
		a=time.time()
		if name in dH:API.CastSpell(name);N["hold"]=a+cv;return
		bB(q,ct);m.update({"claim":a+ct,"seen":False,"next":a+.1,"rd":Journal.Reader()if b else Journal.reader(),"me":b_()});API.CastSpell(name);N["hold"]=a+cv
	def dE():m["claim"],m["rd"]=0.,None;a5(q)
	def e5(now):
		if now>=m["claim"]:dE();return
		if now<m["next"]:return
		m["next"]=now+.1
		if API.HasTarget():m["seen"]=True
		elif m["seen"]or c4(m["rd"].new(),cr,m["me"]):dE()
	def e6(now):
		if API.HasTarget("any"):N["cursor_next"]=now+.25;return True
		return False
	def e7():
		if b["closed"]:
			if not b["shutting"]:HOST.disable(q)
			return
		a=time.time()
		if aw["value"]is not None and a-aw["t"]>=.4:do()
		dl()
		while b["ui_queue"]:
			e4(b["ui_queue"].pop(0))
			if b["closed"]:return
		if a>=k["settle"]:
			if k["size_dirty"]:di()
			if b["dirty"]:dC()
		if b["switch"]is not None:
			c,b["switch"]=b["switch"],None
			if isinstance(c,tuple):de(c[1])
			else:eN(c)
			if b["dirty"]:dC()
		if aG:e8()
		if m["claim"]:e5(a)
		if m["wait"]is not None:
			d,f=m["wait"]
			if not au():m["wait"]=None;cc(d)
			elif a>=f:m["wait"]=None;o("%s was not cast; the target cursor stayed in use."%d,E)
		if O:pass
		elif b["queue"]:e=b["queue"].pop(0);dD[e[0]](e,a)
		elif u and a>=N["hold"]and b["pick"]is None and m["claim"]==0. and m["wait"]is None and not au()and a>=N.get("cursor_next",0.)and not e6(a):O.append(("read",u.pop(0)))
		if not O and not b["dirty"]and b["switch"]is None and a>=k["next_prebuild"]:eO()
		if b["closed"]:return
		if a>=k["next_count"]:dR();fj();k["next_count"]=time.time()+1.5
		eE(a);eK(a)
	def e8():
		while aG:
			a=aG.pop(0);b=M.get(a,(None,None))[0];c=aY.get(a);aY[a]=b;d=a3(a);e=c is not None and c<ck
			if d and not e:f=next((h["title"]for h in B if h["serial"]==a),"A runebook");g="%s left"%aA(b,"charge");HOST.alert("grimoire.charges","%s: %s"%(f,g),who=a)
			ey(a)
	def e9():return(az["busy"]or time.time()-az["at"]<2. or any(d[0]=="travel"for d in O)or any(f[0]in("travel","favgo")or(f[0]=="pressed"and f[2][0]in("travel","favgo"))for f in b["queue"]))
	def fa(e,f,method,name=None):
		if b["shutting"]or b["closed"]:return False
		if method not in cj:o("no way to travel called '%s'."%method,E);return False
		try:c,g=int(e),int(f)
		except(TypeError,ValueError):return False
		if not b["scanned"]:o("still finding your runebooks; try again shortly.",L);return False
		d=next((h["title"]for h in B if h["serial"]==c),None)
		if d is None:o("that runebook isn't in your pack or hands.",E);return False
		try:a=C[c][ar(c,g,name)]
		except(KeyError,IndexError,TypeError):a=None
		if a is None:o("%s isn't in %s any more."%(name or "that rune",d),E);return False
		if method=="charge"and a.get("rune"):o("%s has no charges to use; pick Recall instead."%d,E);return False
		if method in("gate","sacred")and a.get("slot")is None and not a.get("rune"):o("%s has its own layout; only its rune's own button works there, not %s."%(d,"Gate Travel"if method=="gate"else "Sacred Journey"),E);return False
		if e9():o("a trip is already on its way.",L);return False
		Q.add(("travel",c,a,method),dup=True);return True
	def fb():
		if z["dest_ver"]!=z["ver"]:z["dests"]=[{"book":a["serial"],"book_name":a["title"],"index":f,"name":g["name"],"charges":M.get(a["serial"],(None,None))[0]}for a in B for f,g in enumerate(C.get(a["serial"])or())];z["dest_ver"]=z["ver"]
		return list(z["dests"])
	def fc():
		if z.get("chg_ver")!=z["ver"]:z["charges"]=dict((a["serial"],M.get(a["serial"],(None,None))[0])for a in B if C.get(a["serial"]));z["chg_ver"]=z["ver"]
		return z["charges"]
	fd={"grimoire.travel":fa,"grimoire.destinations":fb,"grimoire.book_charges":fc}
	def fe():
		try:fh()
		finally:cR()
	def ff():a=(b["ui_queue"]or b["queue"]or O or u or aG or m["claim"]or b["dirty"]or m["wait"]is not None or b["switch"]is not None or aw["value"]is not None or k["size_dirty"]);return.05 if a else.15
	def fg():return bool(O or j["save"]or j["save_last"]or(I["dirty"]and time.time()>=I["retry_at"]))
	def fh():
		if b["closed"]:return
		if j["save"]or j["save_last"]:br()
		if not O:return
		a=O[0];c=a[0]
		if c=="travel":az["busy"],az["at"]=True,time.time()
		O.pop(0)
		if c=="travel":
			try:d7(a[1],a[2],a[3]);br();eh(a[1],a[2],a[3])
			finally:az["busy"]=False
			N["hold"]=time.time()+6.
		elif c=="read":
			if API.HasTarget("any"):
				if a[1]in u:u.remove(a[1])
				u.insert(0,a[1]);return
			N["reading"]=True
			try:eR(a[1])
			finally:N["reading"]=False
			N["hold"]=max(N["hold"],time.time()+.55)
		else:eP(full=c=="refresh",bags=c!="rescan")
	bz={}
	def fi(it,c):
		g=it.Graphic
		if g in cK:return True
		h=it.Hue
		if(g,h)in aI:return True
		b=(it.Serial,g,h);a=None if c else bz.get(b)
		if a is None:
			n=it.Name;a=bQ(g,h,n)
			if n:
				if len(bz)>200:bz.clear()
				bz[b]=a
		return a
	def fj():
		k["hand_looks"]=n=k.get("hand_looks",0)+1;b=n%10==0;a=sorted(d.Serial for d in bk()if fi(d,b))
		if k["held"]is not None and a!=k["held"]:Q.add(("rescan",))
		k["held"]=a
	def fk():
		b["shutting"]=True;bh.close();br();cR(True);b["docked"],b["link_state"]=False,None;API.SetSharedVar(cy,"off");a5(q);m.update({"wait":None,"claim":0.,"seen":False,"rd":None})
		def a():
			if aR(c["g"]):dk();return True
			return False
		d=F(a)
		if not d and k["last_pos"][0]is not None:
			for e,v in zip(("X","Y"),k["last_pos"]):am(e,v)
		if k["size_dirty"]:di()
		if aR(c["g"]):cf(c["g"])
	return{"start":e3,"tick":e7,"stop":fk,"client_tick":True,"config_height":by.height,"build_config":e0,"poll_config":by.poll,"config_closed":by.closed,"thread_tick":fe,"thread_wanted":fg,"interval":ff}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("grimoire","Grimoire","Spellbook, runebooks and reagents",_module_grimoire,.05,category="Your things")
