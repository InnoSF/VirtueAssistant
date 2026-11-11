def _module_grimoire():
	bC=HOST.bar_alive;bD=HOST.claim_cursor;aQ=HOST.dock_want_set;bE=HOST.dock_wanted;Q=HOST.idle;a6=HOST.release_cursor;bF=Kit.ART_OK;ce=Kit.ART_PAGE;a7=Kit.ART_PLAY;cf=Kit.CORNER_ART;D=Kit.HUE_BAD;M=Kit.HUE_INFO;aB=Kit.count;bG=Kit.data_path;cg=Kit.dispose;bH=Kit.get_var;ch=Kit.gump_is_cmd;ci=Kit.gump_is_int;aR=Kit.gump_parse;aS=Kit.is_open;cj=Kit.look_hue;I=Kit.on_client;bI=Kit.put_var;bJ=Kit.set_text;bK=Kit.strip_html;a8=Kit.with_tip;aC=Kit.zone_up;r="grimoire";aT="Grimoire";bL=[3834];dI={"charge":0,"recall":3,"gate":4,"sacred":5,};aD="recall";ck=("recall","gate","charge","recall_scroll","gate_scroll","sacred");dJ={"recall":"Recall","gate":"Gate Travel","sacred":"Sacred Journey"};cl=3;a9=40;bM=a9;cm=.15;cn=.5;co,cp="#F0C040","#6A6A6A";bN=1;aU=8012;aV=8032;cq=12;cr=5;cs=("fizzles","not yet recovered","more reagents","insufficient mana","concentration is disturbed");ct=.4;cu=5.;dK=frozenset("Reactive Armor|Protection|Magic Reflection|Incognito|Create Food|Earthquake|Summon Creature|Air Elemental|Earth Elemental|Fire Elemental|Water Elemental|Summon Daemon".split("|"));cv=1.5;cw=4.;cx,cy=920,950;aW,aX=700,220;aq=160;aj,ba=60,150;bO=54;bP="Grimoire_cmd";cz="Grimoire_state";bQ=95;bb=66;bc=Kit.WINDOW_BG;cA=a7[0];dL=a7[1];cB=2225;Z="#E8C84A";L="#ECECEC";K="#9C9C9C";ar="#6E6E6E";S="#E04848";at="#C8B070";bd=.05;ak={L:Kit.HUE_TEXT,Z:Kit.HUE_TITLE,K:M,ar:M,S:D};dM=("Lowers the target's Dexterity for a time.|Conjures a random piece of food into your pack.|Lowers the target's Intelligence for a time.|Restores a small amount of the target's health.|Strikes the target with a minor bolt of magic.|Lets the target see clearly in darkness.|Wards you with armor that soaks up melee damage.|Lowers the target's Strength for a time.|Raises the target's Dexterity for a time.|Raises the target's Intelligence for a time.|Attempts to neutralize poison in the target.|Damages the target; strongest at close range.|Traps a container to explode when opened.|Disarms a magical trap on a container.|Temporarily raises your armor rating.|Raises the target's Strength for a time.|Raises the target's Strength, Dexterity and Intelligence.|Hurls a ball of fire at the target.|Magically seals a container shut.|Poisons the target.|Uses or opens an object from a distance.|Instantly moves you to a visible location.|Opens a magically locked container.|Raises a temporary wall of stone.|Cures poison in the target and those nearby.|Raises the armor rating of everyone around you.|Lowers the target's Strength, Dexterity and Intelligence.|Creates a wall of flame that burns those who cross it.|Restores a large amount of the target's health.|Calls a bolt of lightning down on the target.|Drains mana from the target.|Teleports you to the location marked on a rune.|Summons whirling blades that attack nearby creatures.|Destroys a magical field.|Disguises your appearance and name for a time.|Turns harmful spells back upon their caster.|Damages the target based on your superior intellect.|Freezes the target in place for a time.|Creates a wall of poisonous gas.|Summons a random creature to fight for you.|Banishes a summoned creature.|Strikes the target with a powerful bolt of energy.|Engulfs the target in a fiery explosion.|Makes the target invisible for a time.|Marks a recall rune with your current location.|Curses everyone in an area.|Creates a wall that paralyzes those who touch it.|Reveals hidden creatures and players nearby.|Lightning strikes everyone around the target.|Creates an impassable wall of energy.|Engulfs the target in a column of fire.|Opens a moongate to a rune's location that others can use.|Steals the target's mana and gives it to you.|Banishes all summoned creatures in an area.|Rains fire on everyone around the target.|Transforms you into another creature.|Shakes the ground, damaging everyone around you.|Summons a vortex of energy that attacks your foes.|Brings a ghost back to life.|Summons an air elemental to serve you.|Summons a daemon to serve you.|Summons an earth elemental to serve you.|Summons a fire elemental to serve you.|Summons a water elemental to serve you.").split("|");dN={"Feeblemind":"NS GI","Cunning":"NS MR","Resurrection":"BM GI GA"};be=[(fv+" Circle",[(fw,dM[fu*8+fx],dN.get(fw,fy))for fx,(fw,fy)in enumerate(Kit.MAGERY[fu*8:fu*8+8])])for fu,fv in enumerate(("First","Second","Third","Fourth","Fifth","Sixth","Seventh","Eighth"))];aE=dict(Kit.REAGENTS,SS=("Spider's Silk",3981));dO=["BP","BM","GA","GI","MR","NS","SA","SS"];bf=16;cC=24;dP=[("charge","Charge","Recall using one of the book's charges"),("recall","Recall","Cast Recall on this rune"),("gate","Gate","Cast Gate Travel to this rune"),("recall_scroll","Recall scroll","Read a Recall scroll on this rune"),("gate_scroll","Gate scroll","Read a Gate Travel scroll on this rune")];aF=86;bh=60;aY={"opacity":bQ,"scale":100,"loaded":False};fq=dict(aY);b={"minimized":False,"shutting":False,"docked":False,"queue":[]};c={"g":None,"c":{},"store":({},{}),"w":cx,"h":cy,"opacity":bQ};bi,R,k=Kit.basics(b,aT)
	def fr():pass
	def fs():pass
	aa=0;aG=None;z=[];E={};N={};A=[];O={"hold":0.,"reading":False};ab=0x554B87F3;B={"ver":0,"dest_ver":-1,"dests":[]};j={"list":[],"keys":set(),"last":None,"owner":None,"save":False,"save_last":False};ac={};aZ={};aH=[]
	def cD(hidden=False):return{"ctrls":[],"tops":[],"counts":[],"spells":[],"stars":{},"hidden":hidden}
	ad=cD();t={};u=ad;ae={};bj={};bk={};T={"key":None,"t":0.,"selected":None}
	def cE(s):s=re.sub(r"[^a-z]","",(s or "").lower());return s.replace("summon","")if "elemental"in s else s
	def aI(fresh=False):return HOST.pack_items(deep=True,max_age=0. if fresh else.5)
	def bl():
		b=[API.FindLayer("OneHanded"),API.FindLayer("TwoHanded")];b+=list(API.ItemsInContainer(API.Player.Serial)or());c,d,e=set(),[],API.Backpack
		for a in b:
			if a and a.Serial not in c and a.Serial!=e:c.add(a.Serial);d.append(a)
		return d
	def cF():
		a=set()
		for b in bH("Grimoire_RunebookTypes").split(","):
			try:g,h=b.split(":");a.add((int(g,16),int(h,16)))
			except ValueError:pass
		return a
	aJ=cF();bR=set()
	def cG(it):return bS(it.Graphic,it.Hue,it.Name)
	def bS(g,h,name):
		if(g,h)in aJ:return True
		name=(name or "").lower()
		if "rune"in name and "book"in name:return True
		if "spellbook"in name:return False
		if g in bL and h==1121:return True
		return g==8901
	def cH(it):return it.Graphic in bL and not cG(it)
	def dQ():
		a=[d for d in bl()+aI()if cH(d)]
		for b in a:
			if list(API.GetSpellsInSpellbook(b.Serial)or()):return b.Serial
		return a[0].Serial if a else 0
	def dR(serial):
		a=False
		with Kit.quiet:
			for g in list(Tz.get(None,"Gumps",Tz.T("ClassicUO.Game.Managers.UIManager"))):
				with Kit.quiet:
					if(g.LocalSerial==serial and "Spellbook"in g.GetType().Name and not g.IsDisposed):g.Dispose();a=True
		return a
	def cI():return "spells_%08X"%int(API.Player.Serial)
	def dS(force=False):
		if not aa:return
		a=list(API.GetSpellsInSpellbook(aa)or[])
		if not a and not force:
			c=set(f for f in bq(cI()).split(",")if f)
			if c:return c
		if not a:
			API.UseObject(aa);b=time.time()+2.
			while time.time()<b and Q(.05):
				a=list(API.GetSpellsInSpellbook(aa)or[])
				if a:break
			b=time.time()+1.
			while time.time()<b and not HOST.aborting():
				if I(lambda:dR(aa)):break
				Q(.05)
		if not a:return
		d=set(cE(g)for g in a);bp(cI(),",".join(sorted(d)));return d
	dT=set([fz for fA,fz in aE.values()]+[aU,aV])
	def bm():
		c=aI();a=None
		if HOST.in_hop:
			a=(HOST.pass_id,len(c))
			if bT["key"]==a:return dict(bT["totals"])
		b=dict((f,0)for f in dT)
		for d in c:
			g=d.Graphic
			if g in b:b[g]+=max(1,d.Amount or 0)
		if a is not None:bT.update({"key":a,"totals":dict(b)})
		return b
	bT={"key":None,"totals":None}
	def bn(n):return "{:,}".format(n)
	def cJ(graphic,lbl,n,owned=True):return[graphic,lbl,bn(n),ak[L if owned else ar],ak[S if owned else ar]]
	def cK(totals):return(totals.get(aU,0)>0,totals.get(aV,0)>0)
	def dU():
		if not ad["counts"]and not any(q["counts"]for q in t.values()):return
		c=bm();f=c!=m["totals"];m["totals"]=c;j=(ad["counts"]+[v for s in t.values()for v in s["counts"]])if f else[]
		for a in j:
			k,g,h=a[0],a[1],a[2];n=c.get(k,0);d=bn(n)
			if d==h:continue
			if(n==0)!=(h=="0"):g.Hue=a[3]if n else a[4]
			el(g,d);a[2]=d
		if f:dw()
		l=cK(c);o=aP(b["tab"])
		for e,i in list(t.items()):
			if i.get("scrolls")is not None and i["scrolls"]!=l and not b["dirty"]:
				if e==o:a5(e,False)
				else:a0(t.pop(e)["ctrls"])
	cL=set([3834,8901,4079,4080,4081,4082,4083,4084,4029,4030,7185,7187,8786,8787,9100,9120,11600])
	def dV():
		b=[d for d in bl()+aI()if d.Graphic in cL or "book"in(d.Name or "").lower()]
		if not b:k("no books in your pack or hands.",D);return
		k("books you carry (graphic / hue / name / kind):",M)
		for a in b:c="runebook"if cG(a)else("spellbook"if cH(a)else "?");k("0x%04X / 0x%04X / %s (%s)."%(a.Graphic,a.Hue,a.Name or "no name",c),M)
	def dW():
		k("target one of your runebooks.",M);a=object();b["pick"]=a
		def c(serial):
			if b["pick"]is not a:return
			b["pick"]=None;R.add(("registered",serial),dup=True,front=True)
		HOST.pick_target(15,c)
	def dX(serial):
		if not serial:k("cancelled.",M);return False
		a=API.FindItem(serial)
		if not a:k("that isn't an item.",D);return False
		aJ.add((a.Graphic,a.Hue));bI("Grimoire_RunebookTypes",",".join("%X:%X"%d for d in sorted(aJ)));k("runebooks are graphic 0x%04X, hue 0x%04X; saved."%(a.Graphic,a.Hue),Kit.HUE_GOOD);return True
	def cM(items):
		b=[]
		for a in items:
			try:g,h,n=a.Graphic,a.Hue,a.Name
			except Exception:continue
			b.append((a.Serial,g,h,n,bS(g,h,n)))
		return b
	def dY():
		c,b=[],{};d=cM(aI(fresh=True));bR.update((l,q)for x,l,q,v,w in d if w and v);e=set()
		for s,g,h,n,f in cM(bl())+d:
			i=f or(not n and(g,h)in bR)
			if not i or int(s)in e:continue
			e.add(int(s));a=(n or "").strip()or "Runebook";a=a[:1].upper()+a[1:];b[a]=b.get(a,0)+1
			if b[a]>1:a="%s %d"%(a,b[a])
			c.append({"serial":int(s),"title":a})
		return c
	def cN(raw):return str(raw or "").replace("\r","").replace("\x00","").split("\n")
	def dZ():
		a={}
		try:a["is_cmd"]=ch("croppedtext 305 60 115 17 81 17");a["text_is_text"]=not ch("Page 2 Boss");b,c=aR("Shame Bankpage 0");a["split_merged"]=(b,c);a["lines"]=len(aR("a\nb\nc\npage 0")[0])
		except Exception as d:a["error"]=str(d)
		return a
	d_=re.compile(r"^(empty|\(indescript\)|charges?:?|max charges:?|rename( book)?|drop rune|set default|"r"recall.*|gate travel.*|sacred journey.*|use charge.*|next|prev(ious)?|okay|cancel|"r"felucca|trammel|ilshenar|malas|tokuno)$",re.I);d0=re.compile(r"\d+\s*[o\u00b0]\s*\d+'?\s*[NSEW]",re.I);aK={"croppedtext":(7,6),"text":(5,4),"htmlgump":(6,5)}
	def cO(raw):
		b,e=aR(raw);a,c,d=0,[],[]
		for t in e:
			try:
				k=t[0].lower()
				if k=="page":a=int(t[1])
				elif k=="button"and len(t)>=8:
					if int(t[5])==1:c.append((a,int(t[1]),int(t[2]),int(t[7])))
				elif k in aK and len(t)>=aK[k][0]:d.append((a,int(t[1]),int(t[2]),bK(b[int(t[aK[k][1]])])))
			except(ValueError,IndexError):continue
		return b,c,d
	def d1(text):
		t=text.strip()
		if not t or d_.match(t)or d0.search(t):return False
		return not re.match(r"^[\d\s/:.,-]+$",t)
	af={}
	def cP(raw):
		j,h=aR(raw);af.clear();af.update({"text_lines":len(j),"commands":len(h)})
		if h:af["last_command"]=" ".join(h[-1])
		else:k=cN(raw);af["last_line_repr"]=repr(k[-2]if len(k)>1 else k[-1])
		i,c={},None
		for t in h:
			try:
				m=t[0].lower()
				if m=="button"and len(t)>=8 and t[5]=="1":a=int(t[7]);c=a if a>=2 and(a-2)%6==0 else None
				elif m in("croppedtext","text")and c is not None:
					e=bK(j[int(t[-1])]);f=(c-2)//6
					if f not in i:i[f]=(e,c)
					c=None
				else:c=None
			except Exception as p:af["error"]=str(p);c=None
		af["sequential_pairs"]=len(i);b=[{"name":w,"slot":x,"button":y}for x,(w,y)in i.items()if w and w.lower()!="empty"]
		if b:return sorted(b,key=lambda d:d["name"].lower())
		j,l,n=cO(raw);af.update({"buttons":len(l),"labels":len(n)})
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
				if a and d1(a[1]):c[f]=(a[1],a[2])
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
	d2=re.compile(r"^(max(imum)?\s*)?charges?\s*:?\s*(\d+)?\s*(/\s*(\d+))?$",re.I)
	def cQ(raw):
		j,l=aR(raw);a,b,d={},None,[];e=0
		for t in l:
			try:
				k=t[0].lower()
				if k=="page":e=int(t[1]);continue
				if k in("xmfhtmlgump","xmfhtmlgumpcolor","xmfhtmltok")and len(t)>=6:
					f=int(t[5])
					if f==1011296:b="cur"
					elif f==1011297:b="max"
					continue
				if k not in aK or len(t)<aK[k][0]:continue
				x,y,c=int(t[1]),int(t[2]),j[int(t[aK[k][1]])]
			except(ValueError,IndexError):continue
			c=bK(c)
			if ci(c):
				if b and b not in a:a[b]=int(c);b=None
				else:d.append((e,x,y,int(c)))
				continue
			m=d2.match(c)
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
	def bU(s):return(str(s).replace("%","%25").replace("|","%7C").replace(";","%3B").replace("\t","%09").replace("\n","%0A").replace("\r",""))
	def bV(s):return(s.replace("%0A","\n").replace("%09","\t").replace("%3B",";").replace("%7C","|").replace("%25","%"))
	def d3(s):return "".join(["%04X"%ord(a)for a in s])
	def d4(h):
		try:return "".join([chr(int(h[a:a+4],16))for a in range(0,len(h)-3,4)])
		except ValueError:return ""
	def aL(s):return int(s)if ci(s)else None
	def d5(path,text):Kit.write_safe(path,text)
	cR="Grimoire_saved.txt";J={"data":None,"warned":False,"dirty":set(),"retry_at":0.}
	def bo():
		if J["data"]is None:
			J["data"]={};b=Kit.read_merge(bG(cR))
			for a in cN(b):
				if "\t"in a:k,v=a.split("\t",1);J["data"][k]=v
		return J["data"]
	def bp(key,value):
		a=bo()
		if a.get(key)==value:return
		a[key]=value;J["dirty"].add(key)
	def cS(force=False):
		if not J["dirty"]or(not force and time.time()<J["retry_at"]):return
		a,J["dirty"]=J["dirty"],set();b=bo();d=bG(cR)
		try:c=Kit.merge_save(d,dict((n,n+"\t"+b[n])for n in a),lambda l:l.split("\t",1)[0]if "\t"in l else None);e="couldn't read it first"
		except Exception as i:c,e=None,i
		if c is not None:
			for f in c:
				if "\t"in f:
					g,v=f.split("\t",1)
					if g not in J["dirty"]:b[g]=v
			return
		J["dirty"]|=a;J["retry_at"]=time.time()+30.
		if not J["warned"]:k("couldn't save to %s (%s)."%(d,e),D);J["warned"]=True
		for h in sorted(a):
			try:bI("Grimoire_H_"+h,d3(b[h]),True)
			except Exception:
				if not J["warned"]:k("couldn't save the runebook lists; they are read again next time.",D);J["warned"]=True
	def bq(key):
		v=bo().get(key)
		if v:return v
		h=bH("Grimoire_H_"+key);return d4(h)if h else ""
	def cT(serial):return "book_%08X"%int(serial)
	def br(v):return ""if v is None else str(v)
	def d6(serial):
		a=E.get(serial)
		if a is None:return
		c,d=N.get(serial,(None,None));b=["v1",br(c),br(d)];b+=["|".join([bU(f["name"]),br(f["slot"]),br(f["button"]),str(f.get("rune")or "")])for f in a];bp(cT(serial),";".join(b))
	def d7(serial):
		a=bq(cT(serial)).split(";")
		if len(a)<3 or a[0]!="v1":return False
		b=[]
		for p in a[3:]:
			f=p.split("|")
			if len(f)!=4:continue
			d={"name":bV(f[0]),"slot":aL(f[1]),"button":aL(f[2])}
			if aL(f[3]):d["rune"]=aL(f[3])
			b.append(d)
		E[serial]=b;N[serial]=(aL(a[1]),aL(a[2]));return True
	def cU(serial,dests,charges):
		b=(E.get(serial,"none"),N.get(serial))
		if E.get(serial)and(dests is None or(not dests and serial in au)):return False
		E[serial]=dests
		if charges is not None:N[serial]=charges;aH.append(serial)
		if dests is not None:d6(serial)
		a=b!=(E.get(serial),N.get(serial))
		if a:cV(serial);B["ver"]+=1
		return a
	def al(serial,index,name=None,taken=None):
		a=E.get(serial)
		if not a:return
		n=len(a)
		if 0<=index<n and(name is None or a[index]["name"]==name)and(taken is None or index not in taken):return index
		if name is None:return
		b=[(abs(d-index),d)for d in range(n)if a[d]["name"]==name and(taken is None or d not in taken)];return min(b)[1]if b else None
	def bW():
		b,c,a=set(),set(),[]
		for f in j["list"]:
			k=(f[0],f[1])if f[1]>=0 else(f[0],-1,f[2])
			if k in c:continue
			c.add(k);a.append(f)
			if f[1]>=0:b.add(k)
		if len(a)!=len(j["list"]):j["list"]=a;j["save"]=True
		j["keys"]=b
	def cV(serial):
		c=False;d=set();e=sorted([g for g in j["list"]if g[0]==serial],key=lambda f:(f[1]<0,f[1]))
		for b in e:
			i=al(serial,b[1],b[2],d)
			if i is None:
				if b[1]!=-1:b[1]=-1;c=True
				continue
			d.add(i)
			if i!=b[1]:b[1]=i;c=True
		if c:bW();j["save"]=True
		a=j["last"]
		if a is not None and a[0]==serial:
			i=al(serial,a[1],a[2])
			if i is not None and i!=a[1]:j["last"]=(serial,i,a[2],a[3]);j["save_last"]=True
	def d8():
		b="%08X"%int(API.Player.Serial)
		if b==j["owner"]:return
		if j["save"]or j["save_last"]:bs()
		d=[];a=bq("favs_"+b).split(";")
		if a and a[0]=="v1":
			for p in a[1:]:
				f=p.split("|")
				if len(f)!=3:continue
				try:d.append([int(f[0],16),int(f[1]),bV(f[2])])
				except ValueError:continue
		c=None;a=bq("last_"+b).split(";")
		if len(a)==2 and a[0]=="v1":
			f=a[1].split("|")
			try:
				if len(f)==4 and f[3]in ck:c=(int(f[0],16),int(f[1]),bV(f[2]),f[3])
			except ValueError:c=None
		j.update({"list":d[:bM],"last":c,"owner":b,"save":False,"save_last":False});bW();B["ver"]+=1
	def bs():
		b=j["owner"]
		if b is None:j["save"]=j["save_last"]=False;return
		if j["save"]:j["save"]=False;bp("favs_"+b,";".join(["v1"]+["%08X|%d|%s"%(d[0],d[1],bU(d[2]))for d in list(j["list"])]))
		if j["save_last"]:
			j["save_last"]=False;a=j["last"]
			if a is not None:bp("last_"+b,"v1;%08X|%d|%s|%s"%(a[0],a[1],bU(a[2]),a[3]))
	def d9(serial,index,name):
		a=(serial,index)
		if a in j["keys"]:j["list"]=[d for d in j["list"]if(d[0],d[1])!=a];b=False
		else:
			if len(j["list"])>=bM:k("Favourites is full (%d); take a star off first."%bM,D);return
			j["list"].append([serial,index,name]);b=True
		bW();j["save"]=True;B["ver"]+=1;return b
	def ea(serial,dest,method):
		a=next((f for f,g in enumerate(E.get(serial)or[])if g is dest),None)
		if a is None:a=al(serial,0,dest.get("name"))
		if a is None:return
		j["last"]=(serial,a,dest.get("name")or "",method);j["save_last"]=True;B["ver"]+=1
	au={};U={"books":set()}
	def bt():return not U["written"]or U["armed"]
	def bX(text):
		if not bt():return
		U["written"],U["armed"]=True,False;a=bG("Grimoire_runebook_dump.txt")
		try:d5(a,text)
		except Exception as b:k("couldn't save the runebook details (%s)."%b,D);return
		k("saved the runebook details to %s."%a,M);return a
	def bY(serial,path):
		if path:
			b,U["books"]=U["books"],set([serial])
			for a in b:
				if a!=serial:I(lambda s=a:cc(s)if s in t else None)
	def cW(container):return I(lambda:["  0x%08X  graphic 0x%04X  hue 0x%04X  amount %d  name '%s'"%(a.Serial,a.Graphic,a.Hue,a.Amount or 0,a.Name or "")for a in list(API.ItemsInContainer(container)or[])])
	def cX(serial,read=False):
		nonlocal ab
		if ab and API.HasGump(ab):API.CloseGump(ab);Q(.1)
		b=HOST.services.get("gump.expect")
		if b is not None and ab:b(ab,4.)
		if read and(o["claim"]or time.time()<O["hold"]):return("busy",None)
		d=API.HasGump();API.ConfigNextGump(serial=ab,isVisible=False);API.UseObject(serial)
		def e():
			a=API.HasGump()
			if a and(a==ab or a!=d):return("gump",a)
			b=API.FindItem(serial);return("container",None)if b and b.GetContainerGump()else None
		a=(None,"double-clicking the book opened nothing within 3 seconds");f=time.time()+3.
		try:
			while time.time()<f and Q(.05):
				if read and o["claim"]:return("busy",None)
				c=I(e)
				if c is not None:a=c;break
		finally:API.ConfigNextGump()
		if(a[0]is None and I(lambda:len(list(API.ItemsInContainer(serial)or[])))):a=("container",None)
		if a[0]=="gump":ab=a[1]
		return a
	def eb(f):
		def i():a=API.FindItem(f);return((a.Name if a else "")or "").strip()
		a=I(i)
		if not a or a.lower()in("recall rune","a recall rune","rune"):
			with Kit.quiet:
				j=b2();k=time.time();API.ClickObject(f);l=k+1.;m=a.lower();b,g=None,0.
				while time.time()<l and not o["claim"]and Q(.1):
					d=None
					for e in j.new():
						h=(e.name or "").lower();c=(e.text or "").strip()
						if not c or(h and h!=m)or c4(c):continue
						if "rune"in e.low:d=c;break
						if b is None:b,g=c,time.time()+.3
					if d is not None:a=d;break
					if b is not None and time.time()>=g:a=b;break
				else:
					if b is not None:a=b
		return re.sub(r"^(a |an )?(marked )?recall rune( for| to)?\s*","",a,flags=re.I).strip()
	def ec(serial):
		a=[];e=I(lambda:[d.Serial for d in list(API.ItemsInContainer(serial)or[])])
		for c in e or[]:
			b=eb(c)
			if o["claim"]:a=None;break
			if not b or "unmarked"in b.lower():continue
			a.append({"name":b,"slot":None,"button":None,"rune":c})
		def f():
			a=API.FindItem(serial);g=a.GetContainerGump()if a else None
			if g:g.Dispose()
		I(f);return "busy"if a is None else sorted(a,key=lambda d:d["name"].lower())
	def bZ(gid):
		def a():g=API.GetGump(gid);return(g.PacketGumpText or "")if g else ""
		return I(a)
	def ed(serial):
		d,b=cX(serial,True)
		if d=="busy":return d,None
		au.pop(serial,None)
		if d=="container":
			c=ec(serial)
			if not c:
				au[serial]="The book opened like a bag, but no named runes were inside."
				if bt():bY(serial,bX("Runebook 0x%08X opened as a CONTAINER\n\n"%serial+"\n".join(cW(serial))))
			return c,None
		if d is None:
			au[serial]="Couldn't open it: "+b+"."
			if bt():bY(serial,bX("Runebook 0x%08X: %s\nLast server gump: 0x%08X\nItems inside:\n%s"%(serial,b,API.HasGump(),"\n".join(cW(serial))or "  (none known)")))
			return None,None
		a=bZ(b)
		if not a:Q(.1);a=bZ(b)
		API.CloseGump(b);c=cP(a)if a else[]
		if not c:
			au.setdefault(serial,"The book's window didn't match any known layout.")
			if bt():e,f,g=cO(a)if a else([],[],[]);af["selftest"]=dZ();bY(serial,bX("Runebook 0x%08X  gump 0x%08X  (%d texts, %d buttons)\nparser: %r\n\n%s"%(serial,b,len(e),len(f),af,a or "(empty PacketGumpText)")))
			return c,None
		return c,cQ(a)
	def ee(b,gid):
		a=bZ(gid)
		if not a:return
		c=cP(a)
		if c and cU(b,c,cQ(a)):I(lambda:cc(b))
	def cY(serial,dest):
		a=[f for f in(E.get(serial)or())if f.get("name")==dest.get("name")and f.get("slot")is not None]
		for d in a:
			if d["slot"]==dest["slot"]:return d
		return a[0]if a else None
	def cZ(a):
		c,b=cX(a)
		if c!="gump":k("the runebook did not open.",D);return
		ee(a,b);Q(.1);return b
	def c_(gid):API.CloseGump(gid);k("that rune isn't in the book any more; nothing was used.",D)
	ef=cs+("already casting","not allowed to travel","recall from this","gate from this","travel from this","location is blocked","too encumbered","heat of battle","doth not appear to work","is not marked","not yet marked")
	def b_(it):return max(1,int(it.Amount or 0))
	def eg(a):
		def b():n=sum(b_(d)for d in map(API.FindItem,a)if d);return bool(API.HasTarget("any")),n,(int(API.Player.X),int(API.Player.Y))
		return I(b)
	def b0():
		if API.HasTarget("any"):k("a target cursor is up; finish it or press Esc first.",M);return True
		return False
	def eh(c,dest,method):
		f=aV if method=="gate_scroll"else aU;g="Gate Travel"if method=="gate_scroll"else "Recall";h=b2();i=b1();d=I(lambda:next(((n.Serial,b_(n))for n in aI()if n.Graphic==f),None))
		if not d:k("you have no %s scrolls."%g,D);return
		e,j=d;b=dest.get("rune")
		if not b:
			if dest["slot"]is None:k("scrolls need a standard runebook layout.",D);return
			a=cZ(c)
			if a is None:return
			dest=cY(c,dest)
			if dest is None:return c_(a)
			API.ConfigNextGump(serial=a,isVisible=False);API.ReplyGump(2+dest["slot"]*6+2,a);l=time.time()+2.
			while time.time()<l and Q(.1):
				if API.HasGump(a):break
			API.ConfigNextGump();API.CloseGump(a)
			if not Q(.3):return
			b=c
		if not c1():return
		if b0():return
		bD(r,cq+1.)
		try:
			m=c2();API.CancelPreTarget();API.PreTarget(b,"neutral");API.UseObject(e)
			if c0((e,),j,h,i,m,cq)and API.HasTarget("any")and not av():API.Target(b)
		finally:API.CancelPreTarget();a6(r)
	def c0(a,before,since,me,start,timeout):
		b=time.time()+timeout
		while time.time()<b and Q(.1):
			c,d,e=eg(a)
			if c:Q(.15);return True
			if(before and d<before)or ej(since,me)or ei(start,e):return False
		return False
	def av():return HOST.cursor_busy(r)is not None
	def c1():
		a=time.time()+3.
		while av()and time.time()<a:
			if not Q(.1):return False
		return True
	def c2():return I(lambda:(int(API.Player.X),int(API.Player.Y)))
	def b1():return I(lambda:API.Player.Name)or ""
	def ei(start,now):return start is not None and now is not None and max(abs(now[0]-start[0]),abs(now[1]-start[1]))>30
	def b2():Journal.update(True);return Journal.Reader()
	c3={"titles":None}
	def c4(text):
		i=text.find(": ")
		if i<=0 or i>60:return False
		a=c3["titles"]
		if a is None:
			a=set(["Virtue Assistant","Grimoire"])
			for b in HOST.slots:
				a.add(b.title)
				for p in b.parts:a.add(p[1]);a.add("%s > %s"%(b.title,p[1]))
			c3["titles"]=a
		return text[:i]in a
	def c5(lines,texts,me):
		for a in lines:
			b=a.name or ""
			if b and b!="System"and b!=me:continue
			c=a.low
			for f in texts:
				if f in c:
					if not c4(a.text or ""):return True
					break
		return False
	def ej(rd,me=""):return c5(rd.new(),ef,me)
	def ek(a,dest,method):
		if b0():return
		if method in("recall_scroll","gate_scroll"):eh(a,dest,method);return
		if dest.get("rune"):
			c=dJ.get(method,"Recall")
			if not c1():return
			if b0():return
			bD(r,cr)
			try:e,f,g=b2(),c2(),b1();h=aE["BP"][1];d=I(lambda:[(l.Serial,b_(l))for l in aI(True)if l.Graphic==h])if c in("Recall","Gate Travel")else None;i=tuple(q for q,v in d or());j=sum(s for w,s in d or());API.CancelPreTarget();API.PreTarget(dest["rune"],"neutral");API.CastSpell(c);c0(i,j,e,g,f,cr)
			finally:API.CancelPreTarget();a6(r)
			return
		b=cZ(a)
		if b is None:return
		if dest["slot"]is not None:
			dest=cY(a,dest)
			if dest is None:return c_(b)
			API.ReplyGump(2+dest["slot"]*6+dI[method],b)
		else:API.ReplyGump(dest["button"],b)
		if(method=="charge"or dest["slot"]is None)and a not in A:A.append(a)
	C={"scale":1.}
	def e(v):return int(round(v*C["scale"]))
	def c6(parent,ctrl):
		if parent is c["g"]:
			u["tops"].append(ctrl)
			if u["hidden"]:ctrl.IsVisible=False
	def c7(layer,shown):
		for a in layer["tops"]:a.IsVisible=shown
		layer["hidden"]=not shown
	def am(parent,ctrl,a):c6(parent,ctrl);parent.Add(ctrl);a.append(ctrl);return ctrl
	def V(parent,x,y,w,h,color,alpha,a):b=G.CreateGumpColorBox(alpha,color);b.SetRect(e(x),e(y),max(1,e(w)),max(1,e(h)));return am(parent,b,a)
	def p(parent,text,x,y,size,color,a,width=0,align="left",smooth=False):
		b=ak.get(color)
		if b is not None and not smooth and not(width and align=="left"):l=G.CreateGumpLabel(text,b);l.SetAcceptMouseInput(False);c8(l,x,y,size,width,align);return am(parent,l,a)
		size=max(6,Kit.tsize(e(size)))
		if width:l=G.CreateGumpTTFLabel(text,size,color,aligned=align,maxWidth=e(width))
		else:l=G.CreateGumpTTFLabel(text,size,color)
		l.SetPos(e(x),e(y));l.SetAcceptMouseInput(False);return am(parent,l,a)
	aw={}
	def c8(l,x,y,size,width,align):
		a=int(l.GetWidth())or 7*len(l.Text or "");b=int(l.GetHeight())or 16;X=e(x)
		if width and align=="center":X+=max(0,(e(width)-a)//2)
		elif width and align=="right":X+=max(0,e(width)-a)
		Y=e(y)+max(0,(int(e(size)*1.3)-b)//2);l.SetPos(X,Y)
		if width and align!="left":
			if len(aw)>3000:
				for k in[d for d in aw if d.IsDisposed]:del aw[k]
			aw[l]=(x,y,size,width,align)
	def el(l,text):
		l.Text=text;m=aw.get(l)
		if m is not None:c8(l,m[0],m[1],m[2],m[3],m[4])
	def c9(parent,graphic,x,y,size,a):p=G.CreateGumpItemPic(graphic,e(size),e(size));p.SetPos(e(x),e(y));p.SetAcceptMouseInput(False);return am(parent,p,a)
	def da(parent,x,y,on,c):
		d=co if on else cp;a=[]
		for e,f,g,h in((6,0,2,4),(0,4,14,2),(3,6,8,3),(2,9,3,3),(9,9,3,3)):b=V(parent,x+e,y+f,g,h,d,1.,c);b.SetAcceptMouseInput(False);a.append(b)
		return a
	em=dict((fB,tuple(int(fC[fD:fD+2],16)for fD in(1,3,5)))for fB,fC in((True,co),(False,cp)))
	def db(parts,on):
		r,a,b=em[bool(on)]
		for p in parts:p.SetBaseColor(r,a,b,255)
	def ag(ctrl,fn):G.AddControlOnClick(ctrl,fn)
	a_={"ok":None}
	def dc(a,fn):
		if a_["ok"]is False:return False
		a_["ok"]=Kit.hook_double(a,fn,queue=False)
		if not a_["ok"]:k("double-clicks can't be caught on this client; click a row, then click it again to use it.",D)
		return a_["ok"]
	def dd(key,action):
		def a():
			b=time.time();a=T["selected"]
			if a is not None and a!=key and a in ae:ae[a].SetAlpha(bd)
			if key in ae:ae[key].SetAlpha(.2)
			T["selected"]=key
			if a_["ok"]is False and T["key"]==key and b-T["t"]<=3.:T["key"],T["t"]=None,0.;dh(bu(action,b))
			else:T["key"],T["t"]=key,b
		return a
	def bu(action,now=None):
		if action[0]=="cast":return action+(now or time.time(),)
		if action[0]in("travel","favgo"):return("pressed",now or time.time(),action)
		return action
	def de(bg,key,action):ag(bg,dd(key,action));dc(bg,dg(action))
	def df(i):
		if i!=b["circle"]or b["tab"]!="spells":dD("spells",lambda:b.update({"circle":i}))
	def dg(action):
		def a():dh(bu(action))
		return a
	def dh(act):
		if act[0]=="cast"and O["reading"]and not b["shutting"]and o["wait"]is None and not o["claim"]and not av()and not API.HasTarget("any"):cd(act[1],Client.on_client_thread());return
		R.add(act,dup=True)
	def an(action):
		def a():
			if action not in b["ui_queue"]:b["ui_queue"].append(action)
		return a
	def ah(name,default):
		try:return int(bH("Grimoire_"+name,str(default)))
		except Exception:return default
	def ao(name,value):bI("Grimoire_"+name,str(int(value)))
	ax={"value":None,"t":0.}
	def di():C["scale"]=min(ba,max(aj,ah("Scale",100)))/100.;c["w"]=max(e(aW),ah("W",e(cx)));c["h"]=max(e(aX),ah("H",e(cy)));c["opacity"]=min(100,max(0,ah("Opacity",bQ)));bv()
	def bv():
		if F["own"]is not None:return
		W,H=Kit.screen()
		if H>0:c["h"]=max(aX*aj//100,min(c["h"],H))
		if W>0:c["w"]=max(aW*aj//100,min(c["w"],W))
	def LW():return max(aW,int(c["w"]/C["scale"]))
	def LH():return max(aX,int(c["h"]/C["scale"]))
	ai={"parts":[]}
	def en():
		if b["minimized"]:return
		c["w"],c["h"]=c["g"].GetWidth(),c["g"].GetHeight();m["size_dirty"]=True;b["dirty"]=True;m["settle"]=time.time()+.3
	def dj():
		m["size_dirty"]=False
		if F["own"]is not None:return
		for k,v in(("W",c["w"]),("H",c["h"])):ao(k,v)
	def eo():
		bv();a,b=ah("X",-1),ah("Y",-1)
		if a>=0:a,b=Kit.adapt(a,max(0,b),c["w"],c["h"]);a,b=Kit.clamp(a,b,c["w"],c["h"]);a,b=max(0,a),max(0,b)
		c["g"]=g=G.CreateModernGump(a if a>=0 else 100,b if b>=0 else 60,c["w"],c["h"],True,aW*aj//100,aX*aj//100,en);g.SetAlpha(0)
		if a<0:g.CenterXInViewPort();g.CenterYInViewPort()
	ft=None
	def a0(a):
		for c in a:aw.pop(c,None);c.Dispose()
		del a[:]
	b3={}
	def ay(graphic):
		if graphic not in b3:p=G.CreateGumpPic(graphic,0,0,0);b3[graphic]=(int(p.GetWidth()),int(p.GetHeight()));p.Dispose()
		return b3[graphic]
	def aM(parent,graphic,X,Y,W,H,a,mouse=False,hue=0):
		p=G.CreateGumpPic(graphic,X,Y,cj(graphic,hue));p.SetWidth(max(1,W));p.SetHeight(max(1,H))
		if not mouse:p.SetAcceptMouseInput(False)
		return am(parent,p,a)
	def b4(parent,graphic,X,Y,W,H,a):t=G.CreateTiledGumpPic(graphic,max(1,W),max(1,H),cj(graphic));t.SetRect(X,Y,max(1,W),max(1,H));t.SetAcceptMouseInput(False);return am(parent,t,a)
	def ep(parent,x,y,w,h,q,alpha=1.):
		a,b,c,d=e(x),e(y),e(x+w),e(y+h);m,n=ay(bc);o,p=ay(bc+8);m,o=min(m,(c-a)//2),min(o,(c-a)//2);n,p=min(n,(d-b)//2),min(p,(d-b)//2);f=[a,a+m,c-o,c];g=[b,b+n,d-p,d];j=[]
		for i in[4,0,1,2,3,5,6,7,8]:
			k,l=i%3,i//3;W,H=f[k+1]-f[k],g[l+1]-g[l]
			if W<=0 or H<=0:continue
			if i in(0,2,6,8):j.append(aM(parent,bc+i,f[k],g[l],W,H,q))
			else:j.append(b4(parent,bc+i,f[k],g[l],W,H,q))
		for r in j:r.SetAlpha(alpha)
		return[(s,1.)for s in j]
	def a1(parent,x,y,w,h,a,alpha=1.):p=b4(parent,Kit.SECTION_TILE,e(x),e(y),e(w),e(h),a);p.SetAlpha(alpha*Kit.SECTION_ALPHA);return[(p,Kit.SECTION_ALPHA)]
	def eq(w,h,d):a,b=ay(cf);W,H=e(w),e(h);return[aM(c["g"],cf,f,g,a,b,d)for f,g in((0,0),(W-a,0),(0,H-b),(W-a,H-b))]
	a2={}
	def b5(text):return int(round(Kit.text_px(text)/C["scale"]))
	def aN(text,room,size=None):
		if size is None:return Kit.fit(text,e(room))
		if b6(text,size)<=room:return text
		a,b=2,len(text)-1
		while a<b:
			c=(a+b+1)//2
			if b6(text[:c]+"..",size)<=room:a=c
			else:b=c-1
		return text[:a].rstrip()+".."
	def b6(text,size):
		a=(text,size,C["scale"],Kit.tscale)
		if a not in a2:
			if len(a2)>=4000:a2.clear()
			l=G.CreateGumpTTFLabel(text,max(6,Kit.tsize(e(size))),L);b=int(l.GetWidth()or 0);l.Dispose();a2[a]=b or int(.55*size*len(text))
		return int(round(a2[a]/C["scale"]))
	def dk(art):return int(round(ay(art[0])[0]/C["scale"]))
	def ap(x,y,w,h,text,tooltip,fn,size=14,parent=None,art=a7):
		parent=parent or c["g"];a=u["ctrls"];g,i=ay(art[0]);b=G.CreateGumpButton("",0,art[0],art[1],art[2]);b.SetPos(e(x),e(y)+max(0,(e(h)-i)//2));am(parent,b,a);ag(b,fn);a8(b,tooltip)
		if text:d=x+int(round(g/C["scale"]))+4;p(parent,text,d,y+(h-size)//2-1,size,L,a);f=V(parent,d,y,max(4,x+w-d),h,at,0.,a);ag(f,fn);a8(f,tooltip)
		return b
	def er():
		if aC(r)and not b["minimized"]:return
		aQ(r,False);aO()
	def b7():
		if aC(r):return
		aQ(r,True)
		if not b["minimized"]:aO()
		if bC():az(True)
		else:HOST.dock_note(aT)
	def aO(save=True):
		b["minimized"]=not b["minimized"]
		if b["minimized"]:c["g"].SetResizable(False);c["g"].SetHeight(e(bO))
		else:c["g"].SetHeight(c["h"]);c["g"].SetResizable(F["own"]is None)
		az(False);b["dirty"]=True
		if save:ao("Min",1 if b["minimized"]else 0)
	def es():
		a=aC(r)
		if not a:aQ(r,False)
		if b["minimized"]:aO(not a)
		az(False)
	def et():
		if not b["minimized"]:aO()
	def eu():az(False)
	def dl():
		if aC(r):return
		x,y=int(c["g"].GetX()),int(c["g"].GetY());m["last_pos"]=(x,y)
		for k,v in(("X",x),("Y",y)):ao(k,v)
	def az(on):
		on=bool(on)
		if on==b["docked"]:return
		b["docked"]=on;c["g"].IsVisible=not on
	def dm():
		a=time.time()
		if a<b.get("link_next",0.):return
		b["link_next"]=a+.1
		if b.pop("to_bar",False):b7()
		c=API.GetSharedVar(bP)
		if c:
			API.RemoveSharedVar(bP);c=str(c)
			if c=="show"and(b["minimized"]or b["docked"]):
				aQ(r,False)
				if b["minimized"]:aO()
				az(False)
			elif c=="dock"and not b["docked"]:b7()
		if b["docked"]:
			if not bC():az(False)
		elif b["minimized"]and a>=b.get("wish_next",0.):
			b["wish_next"]=a+.25
			if bE(r)and bC():az(True)
		elif not b["minimized"]and a>=b.get("wish_next",0.):
			b["wish_next"]=a+1.
			if bE(r)and not aC(r):aQ(r,False)
		d="docked"if b["docked"]else("minimized"if b["minimized"]else "open")
		if d!=b["link_state"]:b["link_state"]=d;API.SetSharedVar(cz,d)
	def ev(value):
		c["opacity"]=int(value)
		for p,a in ai["parts"]:p.SetAlpha(c["opacity"]/100.*a)
		ao("Opacity",c["opacity"])
	def ew(value):ax["value"]=int(value);ax["t"]=time.time()
	def b8():c["g"].SetWidth(c["w"]);c["g"].SetHeight(e(bO)if b["minimized"]else c["h"]);b["dirty"]=True
	def dn(new,w,h):
		for k,v in(("Scale",int(round(new*100))),("W",w),("H",h)):ao(k,v)
	def do(new,save):
		if abs(new-C["scale"])<.001:return
		a=new/C["scale"];C["scale"]=new;c["w"],c["h"]=int(round(c["w"]*a)),int(round(c["h"]*a));b,d=c["w"],c["h"];bv();b8()
		if save:dn(new,b,d)
	def dp():
		e=ax["value"];ax["value"]=None;a=min(ba,max(aj,e))/100.
		if F["own"]is None:do(a,True);return
		if abs(a-F["own"][0])<.001:return
		c=int(round(F["own"][1]*a/F["own"][0]));d=int(round(F["own"][2]*a/F["own"][0]));do(a,False);F["own"]=(a,c,d);dn(a,c,d)
		if F["told"]is not None:b["ui_queue"].append(("fit",)+F["told"])
	F={"own":None,"told":None}
	def ex(w,h,mode):F["told"]=(w,h)if w else None;b["ui_queue"].append(("fit",w,h))
	def ey(w,h):
		if not w:
			a,F["own"]=F["own"],None
			if a is not None:C["scale"]=a[0];c["w"],c["h"]=a[1],a[2];bv();b8();c["g"].SetResizable(not b["minimized"])
			return
		if F["own"]is None:F["own"]=(C["scale"],c["w"],c["h"]);c["g"].SetResizable(False);b["dirty"]=True
		w,h=int(w),int(h)
		if b["minimized"]:h=c["h"]
		if(c["w"],c["h"])!=(w,h):c["w"],c["h"]=w,h;b8()
	a3=48
	def ez():
		w=LW();h=bO if b["minimized"]else LH();a=u["ctrls"];e=c["opacity"]/100.;ai["parts"]=ep(c["g"],0,0,w,h,a,e);g=[i for i,l in ai["parts"]];d=aC(r);f=C["scale"]
		if d:C["scale"]=1.;w=c["w"]
		try:ai["parts"]+=a1(c["g"],12,12,w-24,30,a,e)
		finally:C["scale"]=f
		if not b["minimized"]:g+=eq(LW(),h,a);ai["parts"]+=a1(c["g"],12,h-40,LW()-24,28,a,e)
		Kit._frame_parts[c["g"]]=g
		if d:C["scale"]=1.
		try:eA(w,d)
		finally:C["scale"]=f
		return max(50,int(-(-50//f)))if d else 50
	def eA(w,a):
		d=u["ctrls"];p(c["g"],"GRIMOIRE",42,18,14,Z,d);f=w-12-44-20-(0 if b["minimized"]else Kit.DOCK_DX+106+98);d.append(Kit.title_catcher(c["g"],e(12),e(12),e(f-16),e(30),an(("min_click",)),key="grimoire:mini"if b["minimized"]else "grimoire"));x=w-12-44
		if not a:ap(x,15,30,24,"",Kit.CLOSE_TIP%aT,an(("close",)),art=Kit.ART_CLOSE);x-=20;ap(x,15,16,24,"",Kit.RESTORE_TIP if b["minimized"]else Kit.MIN_TIP,an(("min_click",)),art=Kit.ART_RESTORE if b["minimized"]else Kit.ART_MIN)
		if not b["minimized"]:
			if not a:x-=Kit.DOCK_DX;ap(x,15,16,24,"",Kit.DOCK_TIP,lambda:b.__setitem__("to_bar",True),art=Kit.ART_DOCK)
			x-=106;ap(x,15,100,24,"Settings",Kit.SETTINGS_TIP%aT,an(("settings",)),art=ce);x-=98;ap(x,15,92,24,"Refresh","Find your spellbook and runebooks again and reread every runebook",R(("refresh",)),art=bF)
	def bw():return LW()-aq-20
	def b9(key):return key not in("spells","favs","+add")and not isinstance(key,tuple)
	def a4(serial):a=N.get(serial,(None,None))[0];return a is not None and a<cl
	def dq(key,title,short):
		a=title if short!=title else None
		if b9(key)and a4(key):b=N[key][0];a="%s: %s left (low)"%(title,aB(b,"charge"))
		return a
	def dr(key,x,y,w,h,text,tooltip,title=None):
		d=u["ctrls"];n=b["tab"]==key;j=S if b9(key)and a4(key)else L;f,g=ay(cA);k,l=e(x),e(y)+max(0,(e(h)-g)//2);aM(c["g"],cA,k,l,f,g,d);a=aM(c["g"],dL,k,l,f,g,d);a.SetAlpha(1. if n else 0.);o=p(c["g"],text,x+int(round(f/C["scale"]))+4,y+(h-14)//2-1,14,j,d);i=V(c["g"],x,y,w,h,at,0.,d);m=eC(key);ag(i,m);ag(a,m)
		if tooltip:i.SetTooltip(tooltip);a.SetTooltip(tooltip)
		bj[key]=a
		if b9(key):bk[key]=(o,i,a,title or text,text,j==S)
	def eB(serial):
		a=bk.get(serial);b=a4(serial)
		if a is None or a[5]==b:return
		d,e,f,c,g,i=a;d.Hue=ak[S if b else L];bk[serial]=(d,e,f,c,g,b);h=dq(serial,c,g)or c;e.SetTooltip(h);f.SetTooltip(h)
	def eC(key):
		def a():b["switch"]=key
		return a
	def eD(top):
		m=[("spells","Spellbook")]+([("favs","Favourites")]if z else[])+[(n["serial"],n["title"])for n in z];f=bw();g=28;h,x,y=[],20,top+4;i=dk(bF)
		for d,a in m:
			e=a if len(a)<18 else a[:16]+"..";w=max(90,i+4+b5(e)+14)
			if x+w>f-4:x,y=20,y+g
			h.append((d,a,e,x,y,w));x+=w+6
		if b["scanned"]:
			a="Add runebook...";w=max(90,i+4+b5(a)+14);j=f-4-w
			if x>j:y+=g
			h.append(("+add",a,a,j,y,w))
		k=y+g+2;l=c["opacity"]/100.;ai["parts"]+=a1(c["g"],12,top,f-12,k-top,u["ctrls"],l)
		for d,a,e,x,y,w in h:
			if d=="+add":ap(x,y,w,24,e,"Target an unlisted runebook; books of its kind are found from then on",R(("register",)),art=bF)
			elif d=="favs":dr(d,x,y,w,24,e,"Starred destinations, last trip and a search of every runebook")
			else:dr(d,x,y,w,24,e,dq(d,a,e),a)
		top=k+Kit.GAP;ai["parts"]+=a1(c["g"],12,top,f-12,LH()-a3-top,u["ctrls"],l);b["content_top"]=top+4;return top+4
	def bx(x,y,w,h):a=G.CreateGumpScrollArea(e(x),e(y),e(w),e(max(40,h)));u["ctrls"].append(a);return a
	def by(ctrl):c6(c["g"],ctrl);c["g"].Add(ctrl)
	def eE(top):
		a=u["ctrls"];f=LW()-aq-12;h=LH()-a3;ai["parts"]+=a1(c["g"],f,top,aq,h-top,a,c["opacity"]/100.);p(c["g"],"Supplies",f,top+8,15,Z,a,width=aq,align="center");i=[aE[v]for v in dO];i+=[None,("Recall scroll",aU),("Gate scroll",aV)];j,l=40,34;o=sum(10 if w is None else j for w in i);g=top+32
		if g+o<=h:d,e,m,b=c["g"],f,g,None
		else:b=bx(f+2,g,aq-2,h-g-4);d,e,m=b,0,0
		q=bm();y=m
		for r in i:
			if r is None:V(d,e+10,y+4,aq-20-(16 if b else 0),1,K,.6,a);y+=10;continue
			s,k=r;c9(d,k,e+8,y+(j-l)//2,l,a);n=q.get(k,0);t=p(d,bn(n),e+48,y+3,15,L if n else S,a);u["counts"].append(cJ(k,t,n));p(d,aN(s,aq-52-(16 if b else 0)),e+48,y+21,12,L,a);y+=j
		if b is not None:by(b)
	def eF(top,circle):
		b=u["ctrls"];s=bw();x=22;D,E=ay(cB);w=max(1,D*30//E)
		for i in range(8):
			k=aM(c["g"],cB+i,e(x),e(top+2),e(w),e(30),b,mouse=True)
			if circle!=i:k.SetAlpha(.45)
			ag(k,an(("circle",i)));k.SetTooltip(be[i][0]);x+=w+6
		F,G=be[circle];p(c["g"],F,x+10,top+6,18,Z,b);top+=38
		if not aa:p(c["g"],"No spellbook in your pack or hands. Carry one, then click Refresh.",22,top+4,14,K,b);return
		d=bx(16,top,s-20,LH()-top-a3-4);l=100;t=bm();H=circle*8;n=s-34;o=bb+18;I=n-4*aF-6;J=m["mana"]
		for i,(g,v,z)in enumerate(G):
			y=i*l;a=aG is None or cE(g)in aG;A=("spell",g);h=V(d,0,y,n,l-4,at,bd,b);ae[A]=h;f=[g,[aE[W][1]for W in z.split()],dt[circle],None,None,h,None]
			if a:f[6]=du(f,t,J)
			B=a and f[6][0];M=f[4]=aM(d,2240+H+i,e(8),e(y+(l-4-bb)//2),e(bb),e(bb),b,hue=0 if a else 946)
			if B:M.SetAlpha(ds)
			f[3]=p(d,g,o,y+14,17,(K if B else L)if a else ar,b);p(d,v if a else v+"  (not in your book)",o,y+38,13,K if a else ar,b,width=max(120,I-o-8));C=z.split();j=n-len(C)*aF-6
			for N in C:
				O,q=aE[N];P=c9(d,q,j+(aF-bh)//2,y+2,bh,b)
				if not a:P.SetAlpha(.4)
				r=t.get(q,0);Q=p(d,bn(r),j,y+bh+3,13,(L if r else S)if a else ar,b,width=aF,align="center");u["counts"].append(cJ(q,Q,r,a));p(d,O,j,y+bh+20,11,K if a else ar,b,width=aF,align="center");j+=aF
			if a:de(h,A,("cast",g));h.SetTooltip(dv(f));u["spells"].append(f)
		by(d)
	ds=.45;eG=dict((fF,fE)for fE,fF in aE.values());dt=Kit.SPELL_MANA
	def du(a,totals,mana):
		for b in a[1]:
			if totals.get(b,0)<=0:return(True,"Out of "+eG.get(b,"a reagent"))
		if mana is not None and mana<a[2]:return(True,"Not enough mana (needs %d)"%a[2])
		return(False,"")
	def dv(a):
		b="Double-click to cast "+a[0]
		if a[6]is not None and a[6][0]:b+="\n"+a[6][1]
		return b
	def dw():
		b=m["totals"]
		if b is None:return
		d=m["mana"]
		for f in list(t.values()):
			for e in f["spells"]:
				a=du(e,b,d)
				if a==e[6]:continue
				e[6]=a;c=a[0];e[3].Hue=ak[K if c else L];e[4].SetAlpha(ds if c else 1.);e[5].SetTooltip(dv(e))
	def eH(now):
		if(now<m["next_mana"]and m["next_mana"]-now<=cn)or b["tab"]!="spells"or b["minimized"]or b["docked"]:return
		m["next_mana"]=now+cn;a=int(API.Player.Mana);c=sum(1 for d in dt if d<=a);m["mana"]=a
		if c!=m["tier"]:m["tier"]=c;dw()
	def eI(serial):
		a,b=N.get(serial,(None,None))
		if a is None:return None,1
		if b is None:return "Charges: %d"%a,a
		return "Charges: %d / %d"%(a,b),a
	def eJ(top,serial):
		a=u["ctrls"];h=bw();M=next((bg for bg in z if bg["serial"]==serial),None)
		if M is None:
			if serial==b["tab"]:b["switch"]="spells"
			return
		p(c["g"],M["title"],22,top+2,cC,Z,a,smooth=True);ap(h-104,top+4,96,26,"Re-read","Read this runebook again",an(("reread",serial)),size=15,art=ce)
		if serial not in E:
			p(c["g"],"Reading this runebook",22,top+36,14,K,a)
			if serial in A:A.remove(serial)
			R.add(("read",serial));return
		O,P=eI(serial)
		if O:p(c["g"],O,h-340,top+6,20,Z if P and not a4(serial)else S,a,width=226,align="right",smooth=True)
		e=E[serial]
		if e is None or(not e and serial in au):af=au.get(serial,"Couldn't read this runebook.");p(c["g"],af,22,top+36,14,S,a,width=h-26);p(c["g"],"Details saved to Grimoire_runebook_dump.txt in the VirtueAssistantSettings folder; send that file, then click Refresh."if serial in U["books"]else "Click Re-read to save this book's details to Grimoire_runebook_dump.txt in the VirtueAssistantSettings folder.",22,top+62,12,K,a,width=h-26);return
		if not e:p(c["g"],"No runes in this runebook. Add some, then click Re-read.",22,top+36,14,K,a);return
		x=bm();u["scrolls"]=cK(x);Q={"recall_scroll":x.get(aU,0),"gate_scroll":x.get(aV,0),"charge":P};ah=N.get(serial,(None,None))[0]is not None;B=len(e);T=any(fn["slot"]is not None for fn in e);ai=T or any(fu.get("rune")for fu in e);p(c["g"],"%s; double-click a name to %s there"%(aB(B,"destination"),aD),22,top+36,bf,K,a,smooth=True);C=dk(a7);q=[]
		if ai:
			for m,n,r in dP:
				if m=="charge"and not T:continue
				q.append((m,n,r,max(C+12,b6(n,bf)+12)))
		W=sum(fv[3]for fv in q);s=top+62;X=s+26;D=h-34;aj=200+W+16;t=max(1,min(B,D//aj));i=D//t;F=i-W-20;Y=(B+t-1)//t;aa=LH()-X-a3-4;f=max(36,min(54,aa//max(1,Y)));o=max(16,int((f-4)*.72));ak=int(o*1.3)
		for v in range(t):
			hx=16+v*i+F+16;p(c["g"],"Destination",16+v*i+30,s,bf,Z,a,smooth=True)
			for m,n,r,k in q:al=Z if Q.get(m,1)else S;p(c["g"],n,hx,s,bf,al,a,width=k,align="center",smooth=True);hx+=k
		V(c["g"],18,s+23,D-4,1,K,.5,a);g=bx(16,X,h-20,aa);am=u["stars"]
		for w,d in enumerate(e):
			v,ao=divmod(w,Y);l,y=v*i,ao*f;ab=("rune",serial,d["button"],d["name"]);G=V(g,l,y,i-6,f-4,at,bd,a);ae[ab]=G;ac=d["slot"]is not None;aq=bool(d.get("rune"));de(G,ab,("travel",serial,d,ca(d)));G.SetTooltip("Double-click to %s to %s"%(aD,d["name"]));am[w]=da(g,l+8,y+max(0,(f-4-14)//2),(serial,w)in j["keys"],a);ad=V(g,l+2,y,26,f-4,at,0.,a);ag(ad,an(("star",serial,w,d["name"])));ad.SetTooltip(dx);ty=y+max(0,(f-4-ak)//2)
			if not(ac or aq):p(g,aN(d["name"],i-46,o),l+30,ty,o,L,a,smooth=True);continue
			p(g,aN(d["name"],F-24,o),l+30,ty,o,L,a,smooth=True);H=l+F+16
			for m,n,r,k in q:
				if m=="charge"and not ac:H+=k;continue
				I=Q.get(m,1);J=r
				if m in("recall_scroll","gate_scroll"):J+=" (%d carried)"%I
				elif m=="charge"and ah:J+=" (%d left)"%I
				ar=ap(H+(k-C)//2,y+2,C,f-8,"",J,dg(("travel",serial,d,m)),parent=g)
				if not I:ar.SetAlpha(.35)
				H+=k
		by(g)
	def ca(dest):return aD if dest["slot"]is not None or dest.get("rune")else "charge"
	dx="Add to Favourites (click again to remove)";dy={"recall":"recall","gate":"gate","charge":"recall (a charge)","recall_scroll":"recall (a scroll)","gate_scroll":"gate (a scroll)","sacred":"travel (Sacred Journey)"}
	def eK(top):a=u["ctrls"];b=bw();p(c["g"],"Favourites",22,top+2,cC,Z,a,smooth=True);f=220;g=b-8-f;h="Search:";p(c["g"],h,g-10-b5(h),top+8,14,L,a);b4(c["g"],Kit.FIELD_TILE,e(g)-2,e(top+4)-1,e(f)+4,24,a);d=G.CreateGumpTextBox(ac["text"],e(f),22,False,16);d.SetPos(e(g),e(top+4));a8(d,"Search every runebook you carry by rune or book name (empty: your Favourites)");am(c["g"],d,a);l=p(c["g"],"",22,top+38,14,K,a);i=top+62;j=b-34;k=bx(16,i,b-20,LH()-i-a3-4);ac.update({"layer":u,"tb":d,"info":l,"sa":k,"pool":[],"seen":None,"ver":-1,"row_w":j,"name_w":max(120,int(j*.55)),"info_w":b-30});dA(building=True);by(k)
	def eL():
		d=dict((v["serial"],v["title"])for v in z);k=[w["serial"]for w in z]
		if not k:return[],"No runebooks in your pack or hands."
		q=ac["text"].strip().lower();a=[]
		if q:
			a,l=dz(q.split(),a9)
			if l:return a,"More than %d found; type more letters."%a9
			if a:return a,"%s found; double-click one to %s there"%(aB(len(a),"destination"),aD)
			return a,"No rune or runebook name has '%s' in it."%ac["text"].strip()
		b=j["last"]
		if b is not None and b[0]in d:
			i=al(b[0],b[1],b[2])
			if i is not None:a.append((b[0],i,b[2],d[b[0]],b[3],True))
		e={}
		for c in j["list"]:e.setdefault(c[0],[]).append(c)
		g=0
		for s in list(e):
			if s not in d:g+=len(e.pop(s))
		n=0
		for s in k:
			for c in sorted(e.get(s,()),key=lambda f:f[1]):
				i=al(s,c[1],c[2])
				if i is None:g+=1;continue
				a.append((s,i,c[2],d[s],None,False));n+=1
		if n:h="%s; double-click one to %s there, or type above to search"%(aB(n,"favourite"),aD)
		else:h="Click a destination's star on a runebook page to list it here."
		if g:h+="  (%d not in the books you carry)"%g
		return a[:a9+1],h
	def dz(words,cap):
		a=[]
		for b in z:
			s,d=b["serial"],b["title"].lower();c=E.get(s)or()
			for i in range(len(c)):
				if all(f in c[i]["name"].lower()+"  "+d for f in words):
					if len(a)>=cap:return a,True
					a.append((s,i,c[i]["name"],b["title"],None,False))
		return a,False
	def dA(building=False):
		a=ac;d=a["layer"]
		if d is None or(t.get("favs")is not d and not building):a["layer"]=None;return
		c,e=eL();a["ver"],a["seen"]=B["ver"],a["text"];bJ(a["info"],aN(e,a["info_w"]),ak[K]);b=a["pool"]
		for i in range(len(c)):
			if i>=len(b):b.append(eM(i,c[i]))
			dC(b[i],c[i])
		for i in range(len(c),len(b)):dC(b[i],None)
	def eM(i,row):f=ac;d,e,c=f["sa"],f["layer"]["ctrls"],30;y=i*c;b={"i":i,"a":None,"prev":None,"at":0.,"tip":None,"shown":True};b["bg"]=V(d,0,y,f["row_w"],c-4,at,bd,e);ae[("fav",i)]=b["bg"];b["on"]=(row[0],row[1])in j["keys"];b["star"]=da(d,8,y+(c-4-14)//2,b["on"],e);b["hit"]=V(d,2,y,26,c-4,at,0.,e);b["hit"].SetTooltip(dx);b["name"]=p(d,"",32,y+(c-4-14)//2-2,14,L,e);b["book"]=p(d,"",32+f["name_w"]+10,y+(c-4-14)//2-2,14,K,e);ag(b["hit"],cb(b,lambda a:an(("star",a[0],a[1],a[2]))()));ag(b["bg"],cb(b,lambda a:dd(("fav",b["i"]),("favgo",)+a)()));dc(b["bg"],cb(b,lambda a:R.add(bu(("favgo",)+a),dup=True)));return b
	def dB(slot,shown):
		slot["shown"]=shown
		for a in[slot["bg"],slot["hit"],slot["name"],slot["book"]]+slot["star"]:a.IsVisible=shown
	def dC(slot,row):
		if row is None:
			if slot["a"]is not None:slot["prev"],slot["at"],slot["a"]=slot["a"],time.time(),None
			if slot["shown"]:dB(slot,False)
			return
		d=(row[0],row[1],row[2],row[4],row[5])
		if slot["a"]!=d:slot["prev"],slot["at"],slot["a"]=slot["a"],time.time(),d
		if not slot["shown"]:dB(slot,True)
		a=ac;bJ(slot["name"],aN(("Last: "if row[5]else "")+row[2],a["name_w"]-4),ak[L]);f=row[3]+((", "+dy.get(row[4],row[4]))if row[4]else "");bJ(slot["book"],aN(f,a["row_w"]-a["name_w"]-46),ak[K]);b=(row[0],row[1])in j["keys"]
		if b!=slot["on"]:db(slot["star"],b);slot["on"]=b
		e=E.get(row[0])or();m=row[4]or(ca(e[row[1]])if row[1]<len(e)else aD);c="Double-click to %s to %s (%s)"%(dy.get(m,m),row[2],row[3])
		if c!=slot["tip"]:slot["tip"]=c;a8(slot["bg"],c)
	def cb(slot,go):
		def a():
			a=slot["prev"]if slot["prev"]is not None and time.time()-slot["at"]<.15 else slot["a"]
			if a is not None:go(a)
		return a
	def eN(now):
		a=ac
		if a["layer"]is None:return
		if t.get("favs")is not a["layer"]:a["layer"]=None;return
		if b["tab"]!="favs"or b["minimized"]or b["docked"]:return
		if now>=a["next"]or a["next"]-now>cm:a["next"]=now+cm;a["text"]=str(a["tb"].Text or "")
		if a["text"]!=a["seen"]or a["ver"]!=B["ver"]:dA()
	def eO(act):
		a,d,b,e=act[1],act[2],act[3],act[4];i=al(a,d,b)
		if i is None:k("%s isn't in that runebook any more."%b,D);return
		c=E[a][i];return("travel",a,c,e or ca(c))
	def aP(tab):return("spells",b["circle"])if tab=="spells"else tab
	def a5(key,hidden):
		nonlocal u;a=t.pop(key,None);c=u=cD(hidden)
		try:
			if isinstance(key,tuple):eF(b["content_top"],key[1])
			elif key=="favs":eK(b["content_top"])
			else:eJ(b["content_top"],key)
		finally:u=ad
		t[key]=c
		if a is not None:a0(a["ctrls"])
		return c
	def cc(key):
		if b["minimized"]or b["dirty"]:
			if key in t:a0(t.pop(key)["ctrls"])
			return
		a5(key,key!=aP(b["tab"]))
	def eP():
		a=[("spells",d)for d in range(len(be))]
		if z:a.append("favs")
		a+=[f["serial"]for f in z if f["serial"]in E];return a
	def dD(tab,d=None):
		c=aP(b["tab"])
		if d:d()
		b["tab"]=tab;ao("Tab",0 if tab=="spells"else(bN if tab=="favs"else tab));ao("Circle",b["circle"])
		if tab=="spells":m["next_mana"]=0.
		a=aP(tab)
		if a==c and a in t and not t[a]["hidden"]:return
		T["selected"]=None
		if c in t:c7(t[c],False)
		if a in t:c7(t[a],True)
		else:a5(a,False)
	def eQ(key):
		for k,a in bj.items():a.SetAlpha(1. if k==key else 0.)
		dD(key)
	def eR():
		if b["minimized"]:return False
		a=[d for d in eP()if d not in t]
		if a:a5(a[0],a[0]!=aP(b["tab"]))
		m["next_prebuild"]=time.time()+ct;return bool(a)
	def dE():
		d=ad["ctrls"][:]
		for k in("ctrls","tops","counts"):del ad[k][:]
		e=list(t.values())
		for f in(t,ae,bj):f.clear()
		T["selected"]=None;b["dirty"]=False;a=ez()
		if not b["minimized"]:eE(a);eD(a);p(c["g"],b["status"],30,LH()-35,12,K,ad["ctrls"]);a5(aP(b["tab"]),False);m["next_prebuild"]=time.time()+ct
		a0(d)
		for g in e:a0(g["ctrls"])
	def eS(full=False,bags=True):nonlocal aa,aG;bo();d8();aa=I(dQ);aG=dS(force=full);I(lambda:eT(full,bags))
	def eT(full,bags):
		nonlocal z;z=dY();del A[:]
		for d in z:
			s=d["serial"];c=s in E or d7(s)
			if full or not c:A.append(s)
			if c and s not in aZ:aZ[s]=N.get(s,(None,None))[0]
			if c and E.get(s):cV(s)
		B["ver"]+=1;a=b.pop("want_tab",None)
		if a and(any(f["serial"]==a for f in z)or(a==bN and z)):b["tab"]="favs"if a==bN else a
		if b["tab"]in A:A.remove(b["tab"]);A.insert(0,b["tab"])
		if(b["tab"]=="favs"and not z)or(b["tab"]not in("favs","spells")and not any(g["serial"]==b["tab"]for g in z)):b["tab"]="spells"
		e=("All spells shown"if aG is None else "%d spells known"%len(aG));b["status"]="%s, %s"%(e if aa else "No spellbook",aB(len(z),"runebook"))
		if not z and bags and(full or not b["reported"]):dV();b["reported"]=True
		b["scanned"]=True;b["dirty"]=True
	def eU(serial):
		a,b=ed(serial)
		if a=="busy":
			if serial not in A:A.insert(0,serial)
			return
		if cU(serial,a,b):I(lambda:cc(serial))
	def eV():b["closed"]=True
	def eW(act,now):
		if 0<=now-act[1]<=3.:dF[act[2][0]](act[2],now)
		else:k("trip not made; Grimoire was busy with a runebook. Press it again.",M)
	def eX(act,now):
		if len(act)>2 and now-act[2]>cv:k("%s was not cast; Grimoire was busy with a runebook."%act[1],M)
		elif o["wait"]is not None:pass
		elif av():o["wait"]=(act[1],now+cv);k("target cursor in use; %s is cast once it is free."%act[1],M)
		else:cd(act[1])
	def eY(act,now):
		if act[1]in A:A.remove(act[1])
		if now<O["hold"]or b["pick"]is not None or o["claim"]or o["wait"]is not None or av()or API.HasTarget("any"):A.insert(0,act[1])
		else:P.append(act)
	def bz(act,now):
		if act[0]=="refresh":U["armed"]=True
		P.append(act)
	def eZ(act,now):
		a=eO(act)
		if a is not None:P.append(a)
	def e_(act,now):
		if dX(act[1]):R.add(("scan",),dup=True,front=True)
	dF={"pressed":eW,"cast":eX,"read":eY,"travel":bz,"scan":bz,"rescan":bz,"refresh":bz,"favgo":eZ,"register":lambda act,now:dW(),"registered":e_}
	def e0(w):return(("WINDOW",(("slider","opacity","Background opacity:","How solid the stone and black backdrop are (0-100, 0 = see-through)",0,100),("slider","scale","Scale:","Size of everything in the window (%d-%d%%, applied when the slider stops)"%(aj,ba),aj,ba),("note","Drag a window corner to resize.",{"ndy":2})),{"sh":124}),)
	e1={"top":34,"fh":30,"ldy":0,"sdy":4,"lw":178,"sw":200,"ugap":12,"vfmt":"%d%%"}
	def e2(a,new):
		if new["opacity"]!=a["opacity"]:ev(new["opacity"])
		if new["scale"]!=a["scale"]:
			ew(new["scale"])
			if not aS(c["g"]):dp()
	bA=Kit.Page(aY,e0,None,e2,e1)
	def e3(g,x,y,w):
		if not aY["loaded"]and not aS(c["g"]):aY["loaded"]=True;di()
		aY.update({"opacity":c["opacity"],"scale":int(round(C["scale"]*100))});bA.build(g,x,y,w)
	m={};aA={};P=[];o={"rd":None,"me":""}
	def e4():
		nonlocal u;b.update({"tab":"spells","circle":0,"dirty":True,"closed":False,"queue":[],"ui_queue":[],"status":"Reading your books","minimized":False,"switch":None,"content_top":0,"shutting":False,"scanned":False,"reported":False,"docked":False,"link_state":None,"pick":None})
		for k in("ctrls","tops","counts"):del ad[k][:]
		for d in(t,ae,bj,bk,aw,aZ,bR):d.clear()
		for a in(P,A,aH):del a[:]
		u=ad;ai["parts"]=[];m.update({"next_count":0.,"next_prebuild":0.,"last_pos":(None,None),"held":None,"totals":None,"settle":0.,"size_dirty":False,"mana":None,"tier":None,"next_mana":0.});aA["busy"],aA["at"]=False,0.;ac.update({"layer":None,"tb":None,"info":None,"sa":None,"pool":[],"text":"","seen":None,"ver":-1,"next":0.});B["ver"]+=1;B["dest_ver"]=-1;o.update({"wait":None,"claim":0.,"seen":False,"next":0.});U.update({"written":False,"armed":False});aJ.clear();aJ.update(cF())
	def e5():
		if b["closed"]or b["shutting"]or not aS(c["g"]):return
		return "docked"if b["docked"]else("minimized"if b["minimized"]else "open")
	def e6():
		e4();R.add(("scan",),dup=True);F["own"]=None;di();b["circle"]=max(0,min(len(be)-1,ah("Circle",0)));b["want_tab"]=ah("Tab",0)or None;eo();G.AddControlOnDisposed(c["g"],eV);G.AddGump(c["g"]);Kit.on_moved(c["g"],dl);HOST.dock_add(r,{"title":aT,"icon":bL[0],"state":e5,"show":es,"minimize":et,"dock":b7,"undock":eu,"gump":lambda:c["g"],"fit":ex,"exact":True,"verify":True,"min":lambda:(e(aW),e(aX))});bi.add(HOST.dock_remove,r);F["own"],F["told"]=None,None;bi.service("look.grimoire",lambda:b.update(dirty=True))
		if ah("Min",0)==1 or bE(r):aO()
		API.RemoveSharedVar(bP);dm();HOST.alert_kind("grimoire.charges","Runebook low on charges",490)
		for a,d in fh.items():bi.service(a,d)
	def e7(act):
		a=act[0]
		if a=="min_click":er()
		elif a=="circle":
			i=act[1]
			if("spells",i)in t and not b["dirty"]:df(i)
			else:b["switch"]=("spells",i)
		elif a=="settings":HOST.show_settings(r)
		elif a=="fit":ey(act[1],act[2])
		elif a=="close":cg(c["g"])
		elif a=="reread":U["armed"]=True;R.add(("read",act[1]),dup=True)
		elif a=="star":
			d,i=act[1],act[2];e=d9(d,i,act[3])
			if e is None:return
			f=t.get(d);g=f["stars"].get(i)if f is not None else None
			if g is not None:db(g,e)
	def cd(name,b=False):
		a=time.time()
		if name in dK:API.CastSpell(name);O["hold"]=a+cw;return
		bD(r,cu);o.update({"claim":a+cu,"seen":False,"next":a+.1,"rd":Journal.Reader()if b else Journal.reader(),"me":b1()});API.CastSpell(name);O["hold"]=a+cw
	def dG():o["claim"],o["rd"]=0.,None;a6(r)
	def e8(now):
		if now>=o["claim"]:dG();return
		if now<o["next"]:return
		o["next"]=now+.1
		if API.HasTarget():o["seen"]=True
		elif o["seen"]or c5(o["rd"].new(),cs,o["me"]):dG()
	def e9(now):
		if API.HasTarget("any"):O["cursor_next"]=now+.25;return True
		return False
	def fa():
		if b["closed"]:
			if not b["shutting"]:HOST.disable(r)
			return
		a=time.time()
		if ax["value"]is not None and a-ax["t"]>=.4:dp()
		dm()
		while b["ui_queue"]:
			e7(b["ui_queue"].pop(0))
			if b["closed"]:return
		if a>=m["settle"]:
			if m["size_dirty"]:dj()
			if b["dirty"]:dE()
		if b["switch"]is not None:
			c,b["switch"]=b["switch"],None
			if isinstance(c,tuple):df(c[1])
			else:eQ(c)
			if b["dirty"]:dE()
		if aH:fb()
		if o["claim"]:e8(a)
		if o["wait"]is not None:
			d,f=o["wait"]
			if not av():o["wait"]=None;cd(d)
			elif a>=f:o["wait"]=None;k("%s was not cast; the target cursor stayed in use."%d,D)
		if P:pass
		elif b["queue"]:e=b["queue"].pop(0);dF[e[0]](e,a)
		elif A and a>=O["hold"]and b["pick"]is None and o["claim"]==0. and o["wait"]is None and not av()and a>=O.get("cursor_next",0.)and not e9(a):P.append(("read",A.pop(0)))
		if not P and not b["dirty"]and b["switch"]is None and a>=m["next_prebuild"]:eR()
		if b["closed"]:return
		if a>=m["next_count"]:dU();fo();m["next_count"]=time.time()+1.5
		eH(a);eN(a)
	def fb():
		while aH:
			a=aH.pop(0);b=N.get(a,(None,None))[0];c=aZ.get(a);aZ[a]=b;d=a4(a);e=c is not None and c<cl
			if d and not e:f=next((h["title"]for h in z if h["serial"]==a),"A runebook");g="%s left"%aB(b,"charge");HOST.alert("grimoire.charges","%s: %s"%(f,g),who=a)
			eB(a)
	def dH():return(aA["busy"]or time.time()-aA["at"]<2. or any(d[0]=="travel"for d in P)or any(f[0]in("travel","favgo")or(f[0]=="pressed"and f[2][0]in("travel","favgo"))for f in b["queue"]))
	def fc(e,f,method,name=None):
		if b["shutting"]or b["closed"]:return False
		if method not in ck:k("no way to travel called '%s'."%method,D);return False
		try:c,g=int(e),int(f)
		except(TypeError,ValueError):return False
		if not b["scanned"]:k("still finding your runebooks; try again shortly.",M);return False
		d=next((h["title"]for h in z if h["serial"]==c),None)
		if d is None:k("that runebook isn't in your pack or hands.",D);return False
		try:a=E[c][al(c,g,name)]
		except(KeyError,IndexError,TypeError):a=None
		if a is None:k("%s isn't in %s any more."%(name or "that rune",d),D);return False
		if method=="charge"and a.get("rune"):k("%s has no charges to use; pick Recall instead."%d,D);return False
		if method in("gate","sacred")and a.get("slot")is None and not a.get("rune"):k("%s has its own layout; only its rune's own button works there, not %s."%(d,"Gate Travel"if method=="gate"else "Sacred Journey"),D);return False
		if dH():k("a trip is already on its way.",M);return False
		R.add(("travel",c,a,method),dup=True);return True
	def fd(q,n=8):
		a=str(q or "").lower().split()
		if not a or b["shutting"]or b["closed"]:return[]
		return[("%s  (%s)"%(d[2],d[3]),(d[0],d[1],d[2]))for d in dz(a,max(0,int(n or 0)))[0]]
	def fe(a):
		if b["shutting"]or b["closed"]:k("trip not made; Grimoire is closing.",M);return False
		try:c,e,d=int(a[0]),int(a[1]),str(a[2])
		except Exception:return False
		if not any(f["serial"]==c for f in z)or al(c,e,d)is None:k("%s isn't in the runebooks you carry any more."%d,D);return False
		if dH():k("a trip is already on its way.",M);return False
		R.add(bu(("favgo",c,e,d,None,False)),dup=True);HOST.poke(r);return True
	def ff():
		if B["dest_ver"]!=B["ver"]:B["dests"]=[{"book":a["serial"],"book_name":a["title"],"index":f,"name":g["name"],"charges":N.get(a["serial"],(None,None))[0]}for a in z for f,g in enumerate(E.get(a["serial"])or())];B["dest_ver"]=B["ver"]
		return list(B["dests"])
	def fg():
		if B.get("chg_ver")!=B["ver"]:B["charges"]=dict((a["serial"],N.get(a["serial"],(None,None))[0])for a in z if E.get(a["serial"]));B["chg_ver"]=B["ver"]
		return B["charges"]
	fh={"grimoire.travel":fc,"grimoire.destinations":ff,"grimoire.book_charges":fg,"grimoire.find":fd,"grimoire.go":fe}
	def fi():
		try:fl()
		finally:cS()
	def fj():a=(b["ui_queue"]or b["queue"]or P or A or aH or o["claim"]or b["dirty"]or o["wait"]is not None or b["switch"]is not None or ax["value"]is not None or m["size_dirty"]);return.05 if a else.15
	def fk():return bool(P or j["save"]or j["save_last"]or(J["dirty"]and time.time()>=J["retry_at"]))
	def fl():
		if b["closed"]:return
		if j["save"]or j["save_last"]:bs()
		if not P:return
		a=P[0];c=a[0]
		if c=="travel":aA["busy"],aA["at"]=True,time.time()
		P.pop(0)
		if c=="travel":
			try:ea(a[1],a[2],a[3]);bs();ek(a[1],a[2],a[3])
			finally:aA["busy"]=False
			O["hold"]=time.time()+6.
		elif c=="read":
			if API.HasTarget("any"):
				if a[1]in A:A.remove(a[1])
				A.insert(0,a[1]);return
			O["reading"]=True
			try:eU(a[1])
			finally:O["reading"]=False
			O["hold"]=max(O["hold"],time.time()+.55)
		else:eS(full=c=="refresh",bags=c!="rescan")
	bB={}
	def fm(it,c):
		g=it.Graphic
		if g in cL:return True
		h=it.Hue
		if(g,h)in aJ:return True
		b=(it.Serial,g,h);a=None if c else bB.get(b)
		if a is None:
			n=it.Name;a=bS(g,h,n)
			if n:
				if len(bB)>200:bB.clear()
				bB[b]=a
		return a
	def fo():
		m["hand_looks"]=n=m.get("hand_looks",0)+1;b=n%10==0;a=sorted(d.Serial for d in bl()if fm(d,b))
		if m["held"]is not None and a!=m["held"]:R.add(("rescan",))
		m["held"]=a
	def fp():
		b["shutting"]=True;bi.close();bs();cS(True);b["docked"],b["link_state"]=False,None;API.SetSharedVar(cz,"off");a6(r);o.update({"wait":None,"claim":0.,"seen":False,"rd":None})
		def a():
			if aS(c["g"]):dl();return True
			return False
		d=I(a)
		if not d and m["last_pos"][0]is not None:
			for k,v in zip(("X","Y"),m["last_pos"]):ao(k,v)
		if m["size_dirty"]:dj()
		if aS(c["g"]):cg(c["g"])
	return{"start":e6,"tick":fa,"stop":fp,"client_tick":True,"config_height":bA.height,"build_config":e3,"poll_config":bA.poll,"config_closed":bA.closed,"thread_tick":fi,"thread_wanted":fk,"interval":fj}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("grimoire","Grimoire","Spellbook, runebooks and reagents",_module_grimoire,.05,category="Your things")
