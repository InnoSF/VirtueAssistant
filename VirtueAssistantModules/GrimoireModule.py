def _module_grimoire():
	bZ=HOST.bar_alive;bt=HOST.claim_cursor;aL=HOST.dock_want_set;bu=HOST.dock_wanted;N=HOST.idle;a_=HOST.release_cursor;r="grimoire";aM="Grimoire";bv=[3834];dn={"charge":0,"recall":3,"gate":4,"sacred":5,};ay="recall";b_=("recall","gate","charge","recall_scroll","gate_scroll","sacred");do={"recall":"Recall","gate":"Gate Travel","sacred":"Sacred Journey"};b0=3;a0=40;bw=a0;b1=.15;b2=.5;b3,b4="#F0C040","#6A6A6A";bx=1;aN=8012;aO=8032;b5=12;b6=5;b7=("fizzles","not yet recovered","more reagents","insufficient mana","concentration is disturbed");b8=.4;b9=5.;dp=frozenset("Reactive Armor|Protection|Magic Reflection|Incognito|Create Food|Earthquake|Summon Creature|Air Elemental|Earth Elemental|Fire Elemental|Water Elemental|Summon Daemon".split("|"));ca=1.5;cb=4.;cc,cd=920,950;aP,aQ=700,220;an=160;ag,a1=60,150;by=54;bz="Grimoire_cmd";ce="Grimoire_state";bA=95;a2=66;a3=Kit.WINDOW_BG;cf=Kit.ART_PLAY[0];dq=Kit.ART_PLAY[1];cg=2225;T="#E8C84A";J="#ECECEC";I="#9C9C9C";ao="#6E6E6E";P="#E04848";ap="#C8B070";a4=.05;ah={J:Kit.HUE_TEXT,T:Kit.HUE_TITLE,I:Kit.HUE_INFO,ao:Kit.HUE_INFO,P:Kit.HUE_BAD};dr=("Lowers the target's Dexterity for a time.|Conjures a random piece of food into your pack.|Lowers the target's Intelligence for a time.|Restores a small amount of the target's health.|Strikes the target with a minor bolt of magic.|Lets the target see clearly in darkness.|Wards you with armor that soaks up melee damage.|Lowers the target's Strength for a time.|Raises the target's Dexterity for a time.|Raises the target's Intelligence for a time.|Attempts to neutralize poison in the target.|Damages the target; strongest at close range.|Traps a container to explode when opened.|Disarms a magical trap on a container.|Temporarily raises your armor rating.|Raises the target's Strength for a time.|Raises the target's Strength, Dexterity and Intelligence.|Hurls a ball of fire at the target.|Magically seals a container shut.|Poisons the target.|Uses or opens an object from a distance.|Instantly moves you to a visible location.|Opens a magically locked container.|Raises a temporary wall of stone.|Cures poison in the target and those nearby.|Raises the armor rating of everyone around you.|Lowers the target's Strength, Dexterity and Intelligence.|Creates a wall of flame that burns those who cross it.|Restores a large amount of the target's health.|Calls a bolt of lightning down on the target.|Drains mana from the target.|Teleports you to the location marked on a rune.|Summons whirling blades that attack nearby creatures.|Destroys a magical field.|Disguises your appearance and name for a time.|Turns harmful spells back upon their caster.|Damages the target based on your superior intellect.|Freezes the target in place for a time.|Creates a wall of poisonous gas.|Summons a random creature to fight for you.|Banishes a summoned creature.|Strikes the target with a powerful bolt of energy.|Engulfs the target in a fiery explosion.|Makes the target invisible for a time.|Marks a recall rune with your current location.|Curses everyone in an area.|Creates a wall that paralyzes those who touch it.|Reveals hidden creatures and players nearby.|Lightning strikes everyone around the target.|Creates an impassable wall of energy.|Engulfs the target in a column of fire.|Opens a moongate to a rune's location that others can use.|Steals the target's mana and gives it to you.|Banishes all summoned creatures in an area.|Rains fire on everyone around the target.|Transforms you into another creature.|Shakes the ground, damaging everyone around you.|Summons a vortex of energy that attacks your foes.|Brings a ghost back to life.|Summons an air elemental to serve you.|Summons a daemon to serve you.|Summons an earth elemental to serve you.|Summons a fire elemental to serve you.|Summons a water elemental to serve you.").split("|");ds={"Feeblemind":"NS GI","Cunning":"NS MR","Resurrection":"BM GI GA"};a5=[(e9+" Circle",[(fa,dr[e8*8+fb],ds.get(fa,fc))for fb,(fa,fc)in enumerate(Kit.MAGERY[e8*8:e8*8+8])])for e8,e9 in enumerate(("First","Second","Third","Fourth","Fifth","Sixth","Seventh","Eighth"))];az=dict(Kit.REAGENTS,SS=("Spider's Silk",3981));dt=["BP","BM","GA","GI","MR","NS","SA","SS"];a6=16;ch=24;du=[("charge","Charge","Recall using one of the book's charges"),("recall","Recall","Cast Recall on this rune"),("gate","Gate","Cast Gate Travel to this rune"),("recall_scroll","Recall scroll","Read a Recall scroll on this rune"),("gate_scroll","Gate scroll","Read a Gate Travel scroll on this rune")];aA=86;a7=60;aR={"opacity":bA,"scale":100,"loaded":False};e4=dict(aR);b={"minimized":False,"shutting":False,"docked":False,"queue":[]};c={"g":None,"c":{},"store":({},{}),"w":cc,"h":cd,"opacity":bA};a8,O,k=Kit.basics(b,aM)
	def e5():pass
	def e6():pass
	U=0;aB=None;z=[];D={};K={};A=[];L={"hold":0.,"reading":False};V=0x554B87F3;B={"ver":0,"dest_ver":-1,"dests":[]};j={"list":[],"keys":set(),"last":None,"owner":None,"save":False,"save_last":False};Z={};aS={};aC=[]
	def ci(hidden=False):return{"ctrls":[],"tops":[],"counts":[],"spells":[],"stars":{},"hidden":hidden}
	aa=ci();t={};u=aa;ab={};a9={};ba={};Q={"key":None,"t":0.,"selected":None}
	def cj(s):s=re.sub(r"[^a-z]","",(s or "").lower());return s.replace("summon","")if "elemental"in s else s
	def aD(fresh=False):return HOST.pack_items(deep=True,max_age=0. if fresh else.5)
	def bb():
		b=[API.FindLayer("OneHanded"),API.FindLayer("TwoHanded")];b+=list(API.ItemsInContainer(API.Player.Serial)or());c,d,e=set(),[],API.Backpack
		for a in b:
			if a and a.Serial not in c and a.Serial!=e:c.add(a.Serial);d.append(a)
		return d
	def ck():
		a=set()
		for b in Kit.get_var("Grimoire_RunebookTypes").split(","):
			try:g,h=b.split(":");a.add((int(g,16),int(h,16)))
			except ValueError:pass
		return a
	aE=ck();bB=set()
	def cl(it):return bC(it.Graphic,it.Hue,it.Name)
	def bC(g,h,name):
		if(g,h)in aE:return True
		name=(name or "").lower()
		if "rune"in name and "book"in name:return True
		if "spellbook"in name:return False
		if g in bv and h==1121:return True
		return g==8901
	def cm(it):return it.Graphic in bv and not cl(it)
	def dv():
		a=[d for d in bb()+aD()if cm(d)]
		for b in a:
			if list(API.GetSpellsInSpellbook(b.Serial)or()):return b.Serial
		return a[0].Serial if a else 0
	def dw(serial):
		a=False
		with Kit.quiet:
			for g in list(Tz.get(None,"Gumps",Tz.T("ClassicUO.Game.Managers.UIManager"))):
				with Kit.quiet:
					if(g.LocalSerial==serial and "Spellbook"in g.GetType().Name and not g.IsDisposed):g.Dispose();a=True
		return a
	def cn():return "spells_%08X"%int(API.Player.Serial)
	def dx(force=False):
		if not U:return
		a=list(API.GetSpellsInSpellbook(U)or[])
		if not a and not force:
			c=set(f for f in bh(cn()).split(",")if f)
			if c:return c
		if not a:
			API.UseObject(U);b=time.time()+2.
			while time.time()<b and N(.05):
				a=list(API.GetSpellsInSpellbook(U)or[])
				if a:break
			b=time.time()+1.
			while time.time()<b and not HOST.aborting():
				if Kit.on_client(lambda:dw(U)):break
				N(.05)
		if not a:return
		d=set(cj(g)for g in a);bf(cn(),",".join(sorted(d)));return d
	dy=set([fd for fe,fd in az.values()]+[aN,aO])
	def bc():
		c=aD();a=None
		if HOST.in_hop:
			a=(HOST.pass_id,len(c))
			if bD["key"]==a:return dict(bD["totals"])
		b=dict((f,0)for f in dy)
		for d in c:
			g=d.Graphic
			if g in b:b[g]+=max(1,d.Amount or 0)
		if a is not None:bD.update({"key":a,"totals":dict(b)})
		return b
	bD={"key":None,"totals":None}
	def bd(n):return "{:,}".format(n)
	def co(graphic,lbl,n,owned=True):return[graphic,lbl,bd(n),ah[J if owned else ao],ah[P if owned else ao]]
	def cp(totals):return(totals.get(aN,0)>0,totals.get(aO,0)>0)
	def dz():
		if not aa["counts"]and not any(q["counts"]for q in t.values()):return
		c=bc();f=c!=m["totals"];m["totals"]=c;j=(aa["counts"]+[v for s in t.values()for v in s["counts"]])if f else[]
		for a in j:
			k,g,h=a[0],a[1],a[2];n=c.get(k,0);d=bd(n)
			if d==h:continue
			if(n==0)!=(h=="0"):g.Hue=a[3]if n else a[4]
			d0(g,d);a[2]=d
		if f:db()
		l=cp(c);o=aK(b["tab"])
		for e,i in list(t.items()):
			if i.get("scrolls")is not None and i["scrolls"]!=l and not b["dirty"]:
				if e==o:aZ(e,False)
				else:aU(t.pop(e)["ctrls"])
	cq=set([3834,8901,4079,4080,4081,4082,4083,4084,4029,4030,7185,7187,8786,8787,9100,9120,11600])
	def dA():
		b=[d for d in bb()+aD()if d.Graphic in cq or "book"in(d.Name or "").lower()]
		if not b:k("no books in your pack or hands.",Kit.HUE_BAD);return
		k("books you carry (graphic / hue / name / kind):",Kit.HUE_INFO)
		for a in b:c="runebook"if cl(a)else("spellbook"if cm(a)else "?");k("0x%04X / 0x%04X / %s (%s)."%(a.Graphic,a.Hue,a.Name or "no name",c),Kit.HUE_INFO)
	def dB():
		k("target one of your runebooks.",Kit.HUE_INFO);a=object();b["pick"]=a
		def c(serial):
			if b["pick"]is not a:return
			b["pick"]=None;O.add(("registered",serial),dup=True,front=True)
		HOST.pick_target(15,c)
	def dC(serial):
		if not serial:k("cancelled.",Kit.HUE_INFO);return False
		a=API.FindItem(serial)
		if not a:k("that isn't an item.",Kit.HUE_BAD);return False
		aE.add((a.Graphic,a.Hue));Kit.put_var("Grimoire_RunebookTypes",",".join("%X:%X"%d for d in sorted(aE)));k("runebooks are graphic 0x%04X, hue 0x%04X; saved."%(a.Graphic,a.Hue),Kit.HUE_GOOD);return True
	def cr(items):
		b=[]
		for a in items:
			try:g,h,n=a.Graphic,a.Hue,a.Name
			except Exception:continue
			b.append((a.Serial,g,h,n,bC(g,h,n)))
		return b
	def dD():
		c,b=[],{};d=cr(aD(fresh=True));bB.update((l,q)for x,l,q,v,w in d if w and v);e=set()
		for s,g,h,n,f in cr(bb())+d:
			i=f or(not n and(g,h)in bB)
			if not i or int(s)in e:continue
			e.add(int(s));a=(n or "").strip()or "Runebook";a=a[:1].upper()+a[1:];b[a]=b.get(a,0)+1
			if b[a]>1:a="%s %d"%(a,b[a])
			c.append({"serial":int(s),"title":a})
		return c
	def cs(raw):return str(raw or "").replace("\r","").replace("\x00","").split("\n")
	def dE():
		a={}
		try:a["is_cmd"]=Kit.gump_is_cmd("croppedtext 305 60 115 17 81 17");a["text_is_text"]=not Kit.gump_is_cmd("Page 2 Boss");b,c=Kit.gump_parse("Shame Bankpage 0");a["split_merged"]=(b,c);a["lines"]=len(Kit.gump_parse("a\nb\nc\npage 0")[0])
		except Exception as d:a["error"]=str(d)
		return a
	dF=re.compile(r"^(empty|\(indescript\)|charges?:?|max charges:?|rename( book)?|drop rune|set default|"r"recall.*|gate travel.*|sacred journey.*|use charge.*|next|prev(ious)?|okay|cancel|"r"felucca|trammel|ilshenar|malas|tokuno)$",re.I);dG=re.compile(r"\d+\s*[o\u00b0]\s*\d+'?\s*[NSEW]",re.I);aF={"croppedtext":(7,6),"text":(5,4),"htmlgump":(6,5)}
	def ct(raw):
		b,e=Kit.gump_parse(raw);a,c,d=0,[],[]
		for t in e:
			try:
				k=t[0].lower()
				if k=="page":a=int(t[1])
				elif k=="button"and len(t)>=8:
					if int(t[5])==1:c.append((a,int(t[1]),int(t[2]),int(t[7])))
				elif k in aF and len(t)>=aF[k][0]:d.append((a,int(t[1]),int(t[2]),Kit.strip_html(b[int(t[aF[k][1]])])))
			except(ValueError,IndexError):continue
		return b,c,d
	def dH(text):
		t=text.strip()
		if not t or dF.match(t)or dG.search(t):return False
		return not re.match(r"^[\d\s/:.,-]+$",t)
	ac={}
	def cu(raw):
		j,h=Kit.gump_parse(raw);ac.clear();ac.update({"text_lines":len(j),"commands":len(h)})
		if h:ac["last_command"]=" ".join(h[-1])
		else:k=cs(raw);ac["last_line_repr"]=repr(k[-2]if len(k)>1 else k[-1])
		i,c={},None
		for t in h:
			try:
				m=t[0].lower()
				if m=="button"and len(t)>=8 and t[5]=="1":a=int(t[7]);c=a if a>=2 and(a-2)%6==0 else None
				elif m in("croppedtext","text")and c is not None:
					e=Kit.strip_html(j[int(t[-1])]);f=(c-2)//6
					if f not in i:i[f]=(e,c)
					c=None
				else:c=None
			except Exception as p:ac["error"]=str(p);c=None
		ac["sequential_pairs"]=len(i);b=[{"name":w,"slot":x,"button":y}for x,(w,y)in i.items()if w and w.lower()!="empty"]
		if b:return sorted(b,key=lambda d:d["name"].lower())
		j,l,n=ct(raw);ac.update({"buttons":len(l),"labels":len(n)})
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
				if a and dH(a[1]):c[f]=(a[1],a[2])
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
	dI=re.compile(r"^(max(imum)?\s*)?charges?\s*:?\s*(\d+)?\s*(/\s*(\d+))?$",re.I)
	def cv(raw):
		j,l=Kit.gump_parse(raw);a,b,d={},None,[];e=0
		for t in l:
			try:
				k=t[0].lower()
				if k=="page":e=int(t[1]);continue
				if k in("xmfhtmlgump","xmfhtmlgumpcolor","xmfhtmltok")and len(t)>=6:
					f=int(t[5])
					if f==1011296:b="cur"
					elif f==1011297:b="max"
					continue
				if k not in aF or len(t)<aF[k][0]:continue
				x,y,c=int(t[1]),int(t[2]),j[int(t[aF[k][1]])]
			except(ValueError,IndexError):continue
			c=Kit.strip_html(c)
			if Kit.gump_is_int(c):
				if b and b not in a:a[b]=int(c);b=None
				else:d.append((e,x,y,int(c)))
				continue
			m=dI.match(c)
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
	def bE(s):return(str(s).replace("%","%25").replace("|","%7C").replace(";","%3B").replace("\t","%09").replace("\n","%0A").replace("\r",""))
	def bF(s):return(s.replace("%0A","\n").replace("%09","\t").replace("%3B",";").replace("%7C","|").replace("%25","%"))
	def dJ(s):return "".join(["%04X"%ord(a)for a in s])
	def dK(h):
		try:return "".join([chr(int(h[a:a+4],16))for a in range(0,len(h)-3,4)])
		except ValueError:return ""
	def aG(s):return int(s)if Kit.gump_is_int(s)else None
	def dL(path,text):Kit.write_safe(path,text)
	cw="Grimoire_saved.txt";F={"data":None,"warned":False,"dirty":set(),"retry_at":0.}
	def be():
		if F["data"]is None:
			F["data"]={};b=Kit.read_merge(Kit.data_path(cw))
			for a in cs(b):
				if "\t"in a:k,v=a.split("\t",1);F["data"][k]=v
		return F["data"]
	def bf(key,value):
		a=be()
		if a.get(key)==value:return
		a[key]=value;F["dirty"].add(key)
	def cx(force=False):
		if not F["dirty"]or(not force and time.time()<F["retry_at"]):return
		a,F["dirty"]=F["dirty"],set();b=be();d=Kit.data_path(cw)
		try:c=Kit.merge_save(d,dict((n,n+"\t"+b[n])for n in a),lambda l:l.split("\t",1)[0]if "\t"in l else None);e="couldn't read it first"
		except Exception as i:c,e=None,i
		if c is not None:
			for f in c:
				if "\t"in f:
					g,v=f.split("\t",1)
					if g not in F["dirty"]:b[g]=v
			return
		F["dirty"]|=a;F["retry_at"]=time.time()+30.
		if not F["warned"]:k("couldn't save to %s (%s)."%(d,e),Kit.HUE_BAD);F["warned"]=True
		for h in sorted(a):
			try:Kit.put_var("Grimoire_H_"+h,dJ(b[h]),True)
			except Exception:
				if not F["warned"]:k("couldn't save the runebook lists; they are read again next time.",Kit.HUE_BAD);F["warned"]=True
	def bh(key):
		v=be().get(key)
		if v:return v
		h=Kit.get_var("Grimoire_H_"+key);return dK(h)if h else ""
	def cy(serial):return "book_%08X"%int(serial)
	def bi(v):return ""if v is None else str(v)
	def dM(serial):
		a=D.get(serial)
		if a is None:return
		c,d=K.get(serial,(None,None));b=["v1",bi(c),bi(d)];b+=["|".join([bE(f["name"]),bi(f["slot"]),bi(f["button"]),str(f.get("rune")or "")])for f in a];bf(cy(serial),";".join(b))
	def dN(serial):
		a=bh(cy(serial)).split(";")
		if len(a)<3 or a[0]!="v1":return False
		b=[]
		for p in a[3:]:
			f=p.split("|")
			if len(f)!=4:continue
			d={"name":bF(f[0]),"slot":aG(f[1]),"button":aG(f[2])}
			if aG(f[3]):d["rune"]=aG(f[3])
			b.append(d)
		D[serial]=b;K[serial]=(aG(a[1]),aG(a[2]));return True
	def cz(serial,dests,charges):
		b=(D.get(serial,"none"),K.get(serial))
		if D.get(serial)and(dests is None or(not dests and serial in aq)):return False
		D[serial]=dests
		if charges is not None:K[serial]=charges;aC.append(serial)
		if dests is not None:dM(serial)
		a=b!=(D.get(serial),K.get(serial))
		if a:cA(serial);B["ver"]+=1
		return a
	def ai(serial,index,name=None,taken=None):
		a=D.get(serial)
		if not a:return
		n=len(a)
		if 0<=index<n and(name is None or a[index]["name"]==name)and(taken is None or index not in taken):return index
		if name is None:return
		b=[(abs(d-index),d)for d in range(n)if a[d]["name"]==name and(taken is None or d not in taken)];return min(b)[1]if b else None
	def bG():
		b,c,a=set(),set(),[]
		for f in j["list"]:
			k=(f[0],f[1])if f[1]>=0 else(f[0],-1,f[2])
			if k in c:continue
			c.add(k);a.append(f)
			if f[1]>=0:b.add(k)
		if len(a)!=len(j["list"]):j["list"]=a;j["save"]=True
		j["keys"]=b
	def cA(serial):
		c=False;d=set();e=sorted([g for g in j["list"]if g[0]==serial],key=lambda f:(f[1]<0,f[1]))
		for b in e:
			i=ai(serial,b[1],b[2],d)
			if i is None:
				if b[1]!=-1:b[1]=-1;c=True
				continue
			d.add(i)
			if i!=b[1]:b[1]=i;c=True
		if c:bG();j["save"]=True
		a=j["last"]
		if a is not None and a[0]==serial:
			i=ai(serial,a[1],a[2])
			if i is not None and i!=a[1]:j["last"]=(serial,i,a[2],a[3]);j["save_last"]=True
	def dO():
		b="%08X"%int(API.Player.Serial)
		if b==j["owner"]:return
		if j["save"]or j["save_last"]:bj()
		d=[];a=bh("favs_"+b).split(";")
		if a and a[0]=="v1":
			for p in a[1:]:
				f=p.split("|")
				if len(f)!=3:continue
				try:d.append([int(f[0],16),int(f[1]),bF(f[2])])
				except ValueError:continue
		c=None;a=bh("last_"+b).split(";")
		if len(a)==2 and a[0]=="v1":
			f=a[1].split("|")
			try:
				if len(f)==4 and f[3]in b_:c=(int(f[0],16),int(f[1]),bF(f[2]),f[3])
			except ValueError:c=None
		j.update({"list":d[:bw],"last":c,"owner":b,"save":False,"save_last":False});bG();B["ver"]+=1
	def bj():
		b=j["owner"]
		if b is None:j["save"]=j["save_last"]=False;return
		if j["save"]:j["save"]=False;bf("favs_"+b,";".join(["v1"]+["%08X|%d|%s"%(d[0],d[1],bE(d[2]))for d in list(j["list"])]))
		if j["save_last"]:
			j["save_last"]=False;a=j["last"]
			if a is not None:bf("last_"+b,"v1;%08X|%d|%s|%s"%(a[0],a[1],bE(a[2]),a[3]))
	def dP(serial,index,name):
		a=(serial,index)
		if a in j["keys"]:j["list"]=[d for d in j["list"]if(d[0],d[1])!=a];b=False
		else:
			if len(j["list"])>=bw:k("Favourites is full (%d); take a star off first."%bw,Kit.HUE_BAD);return
			j["list"].append([serial,index,name]);b=True
		bG();j["save"]=True;B["ver"]+=1;return b
	def dQ(serial,dest,method):
		a=next((f for f,g in enumerate(D.get(serial)or[])if g is dest),None)
		if a is None:a=ai(serial,0,dest.get("name"))
		if a is None:return
		j["last"]=(serial,a,dest.get("name")or "",method);j["save_last"]=True;B["ver"]+=1
	aq={};R={"books":set()}
	def bk():return not R["written"]or R["armed"]
	def bH(text):
		if not bk():return
		R["written"],R["armed"]=True,False;a=Kit.data_path("Grimoire_runebook_dump.txt")
		try:dL(a,text)
		except Exception as b:k("couldn't save the runebook details (%s)."%b,Kit.HUE_BAD);return
		k("saved the runebook details to %s."%a,Kit.HUE_INFO);return a
	def bI(serial,path):
		if path:
			b,R["books"]=R["books"],set([serial])
			for a in b:
				if a!=serial:Kit.on_client(lambda s=a:bX(s)if s in t else None)
	def cB(container):return Kit.on_client(lambda:["  0x%08X  graphic 0x%04X  hue 0x%04X  amount %d  name '%s'"%(a.Serial,a.Graphic,a.Hue,a.Amount or 0,a.Name or "")for a in list(API.ItemsInContainer(container)or[])])
	def cC(serial,read=False):
		nonlocal V
		if V and API.HasGump(V):API.CloseGump(V);N(.1)
		b=HOST.services.get("gump.expect")
		if b is not None and V:b(V,4.)
		if read and(o["claim"]or time.time()<L["hold"]):return("busy",None)
		d=API.HasGump();API.ConfigNextGump(serial=V,isVisible=False);API.UseObject(serial)
		def e():
			a=API.HasGump()
			if a and(a==V or a!=d):return("gump",a)
			b=API.FindItem(serial);return("container",None)if b and b.GetContainerGump()else None
		a=(None,"double-clicking the book opened nothing within 3 seconds");f=time.time()+3.
		try:
			while time.time()<f and N(.05):
				if read and o["claim"]:return("busy",None)
				c=Kit.on_client(e)
				if c is not None:a=c;break
		finally:API.ConfigNextGump()
		if(a[0]is None and Kit.on_client(lambda:len(list(API.ItemsInContainer(serial)or[])))):a=("container",None)
		if a[0]=="gump":V=a[1]
		return a
	def dR(f):
		def i():a=API.FindItem(f);return((a.Name if a else "")or "").strip()
		a=Kit.on_client(i)
		if not a or a.lower()in("recall rune","a recall rune","rune"):
			with Kit.quiet:
				j=bN();k=time.time();API.ClickObject(f);l=k+1.;m=a.lower();b,g=None,0.
				while time.time()<l and not o["claim"]and N(.1):
					d=None
					for e in j.new():
						h=(e.name or "").lower();c=(e.text or "").strip()
						if not c or(h and h!=m)or cK(c):continue
						if "rune"in e.low:d=c;break
						if b is None:b,g=c,time.time()+.3
					if d is not None:a=d;break
					if b is not None and time.time()>=g:a=b;break
				else:
					if b is not None:a=b
		return re.sub(r"^(a |an )?(marked )?recall rune( for| to)?\s*","",a,flags=re.I).strip()
	def dS(serial):
		a=[];e=Kit.on_client(lambda:[d.Serial for d in list(API.ItemsInContainer(serial)or[])])
		for c in e or[]:
			b=dR(c)
			if o["claim"]:a=None;break
			if not b or "unmarked"in b.lower():continue
			a.append({"name":b,"slot":None,"button":None,"rune":c})
		def f():
			a=API.FindItem(serial);g=a.GetContainerGump()if a else None
			if g:g.Dispose()
		Kit.on_client(f);return "busy"if a is None else sorted(a,key=lambda d:d["name"].lower())
	def bJ(gid):
		def a():g=API.GetGump(gid);return(g.PacketGumpText or "")if g else ""
		return Kit.on_client(a)
	def dT(serial):
		d,b=cC(serial,True)
		if d=="busy":return d,None
		aq.pop(serial,None)
		if d=="container":
			c=dS(serial)
			if not c:
				aq[serial]="The book opened like a bag, but no named runes were inside."
				if bk():bI(serial,bH("Runebook 0x%08X opened as a CONTAINER\n\n"%serial+"\n".join(cB(serial))))
			return c,None
		if d is None:
			aq[serial]="Couldn't open it: "+b+"."
			if bk():bI(serial,bH("Runebook 0x%08X: %s\nLast server gump: 0x%08X\nItems inside:\n%s"%(serial,b,API.HasGump(),"\n".join(cB(serial))or "  (none known)")))
			return None,None
		a=bJ(b)
		if not a:N(.1);a=bJ(b)
		API.CloseGump(b);c=cu(a)if a else[]
		if not c:
			aq.setdefault(serial,"The book's window didn't match any known layout.")
			if bk():e,f,g=ct(a)if a else([],[],[]);ac["selftest"]=dE();bI(serial,bH("Runebook 0x%08X  gump 0x%08X  (%d texts, %d buttons)\nparser: %r\n\n%s"%(serial,b,len(e),len(f),ac,a or "(empty PacketGumpText)")))
			return c,None
		return c,cv(a)
	def dU(book_serial,gid):
		a=bJ(gid)
		if not a:return
		b=cu(a)
		if b and cz(book_serial,b,cv(a)):Kit.on_client(lambda:bX(book_serial))
	def cD(serial,dest):
		a=[f for f in(D.get(serial)or())if f.get("name")==dest.get("name")and f.get("slot")is not None]
		for d in a:
			if d["slot"]==dest["slot"]:return d
		return a[0]if a else None
	def cE(book_serial):
		b,a=cC(book_serial)
		if b!="gump":k("the runebook did not open.",Kit.HUE_BAD);return
		dU(book_serial,a);N(.1);return a
	def cF(gid):API.CloseGump(gid);k("that rune isn't in the book any more; nothing was used.",Kit.HUE_BAD)
	dV=b7+("already casting","not allowed to travel","recall from this","gate from this","travel from this","location is blocked","too encumbered","heat of battle","doth not appear to work","is not marked","not yet marked")
	def bK(it):return max(1,int(it.Amount or 0))
	def dW(a):
		def b():n=sum(bK(d)for d in map(API.FindItem,a)if d);return bool(API.HasTarget("any")),n,(int(API.Player.X),int(API.Player.Y))
		return Kit.on_client(b)
	def bL():
		if API.HasTarget("any"):k("a target cursor is up; finish it or press Esc first.",Kit.HUE_INFO);return True
		return False
	def dX(book_serial,dest,method):
		e=aO if method=="gate_scroll"else aN;f="Gate Travel"if method=="gate_scroll"else "Recall";g=bN();h=bM();c=Kit.on_client(lambda:next(((n.Serial,bK(n))for n in aD()if n.Graphic==e),None))
		if not c:k("you have no %s scrolls."%f,Kit.HUE_BAD);return
		d,i=c;b=dest.get("rune")
		if not b:
			if dest["slot"]is None:k("scrolls need a standard runebook layout.",Kit.HUE_BAD);return
			a=cE(book_serial)
			if a is None:return
			dest=cD(book_serial,dest)
			if dest is None:return cF(a)
			API.ConfigNextGump(serial=a,isVisible=False);API.ReplyGump(2+dest["slot"]*6+2,a);j=time.time()+2.
			while time.time()<j and N(.1):
				if API.HasGump(a):break
			API.ConfigNextGump();API.CloseGump(a)
			if not N(.3):return
			b=book_serial
		if not cH():return
		if bL():return
		bt(r,b5+1.)
		try:
			l=cI();API.CancelPreTarget();API.PreTarget(b,"neutral");API.UseObject(d)
			if cG((d,),i,g,h,l,b5)and API.HasTarget("any")and not ar():API.Target(b)
		finally:API.CancelPreTarget();a_(r)
	def cG(a,before,since,me,start,timeout):
		b=time.time()+timeout
		while time.time()<b and N(.1):
			c,d,e=dW(a)
			if c:N(.15);return True
			if(before and d<before)or dZ(since,me)or dY(start,e):return False
		return False
	def ar():return HOST.cursor_busy(r)is not None
	def cH():
		a=time.time()+3.
		while ar()and time.time()<a:
			if not N(.1):return False
		return True
	def cI():return Kit.on_client(lambda:(int(API.Player.X),int(API.Player.Y)))
	def bM():return Kit.on_client(lambda:API.Player.Name)or ""
	def dY(start,now):return start is not None and now is not None and max(abs(now[0]-start[0]),abs(now[1]-start[1]))>30
	def bN():Journal.update(True);return Journal.Reader()
	cJ={"titles":None}
	def cK(text):
		i=text.find(": ")
		if i<=0 or i>60:return False
		a=cJ["titles"]
		if a is None:
			a=set(["Virtue Assistant","Grimoire"])
			for b in HOST.slots:
				a.add(b.title)
				for p in b.parts:a.add(p[1]);a.add("%s > %s"%(b.title,p[1]))
			cJ["titles"]=a
		return text[:i]in a
	def cL(lines,texts,me):
		for a in lines:
			b=a.name or ""
			if b and b!="System"and b!=me:continue
			c=a.low
			for f in texts:
				if f in c:
					if not cK(a.text or ""):return True
					break
		return False
	def dZ(rd,me=""):return cL(rd.new(),dV,me)
	def d_(book_serial,dest,method):
		if bL():return
		if method in("recall_scroll","gate_scroll"):dX(book_serial,dest,method);return
		if dest.get("rune"):
			b=do.get(method,"Recall")
			if not cH():return
			if bL():return
			bt(r,b6)
			try:d,e,f=bN(),cI(),bM();g=az["BP"][1];c=Kit.on_client(lambda:[(l.Serial,bK(l))for l in aD(True)if l.Graphic==g])if b in("Recall","Gate Travel")else None;h=tuple(q for q,v in c or());i=sum(s for w,s in c or());API.CancelPreTarget();API.PreTarget(dest["rune"],"neutral");API.CastSpell(b);cG(h,i,d,f,e,b6)
			finally:API.CancelPreTarget();a_(r)
			return
		a=cE(book_serial)
		if a is None:return
		if dest["slot"]is not None:
			dest=cD(book_serial,dest)
			if dest is None:return cF(a)
			API.ReplyGump(2+dest["slot"]*6+dn[method],a)
		else:API.ReplyGump(dest["button"],a)
		if(method=="charge"or dest["slot"]is None)and book_serial not in A:A.append(book_serial)
	C={"scale":1.}
	def e(v):return int(round(v*C["scale"]))
	def cM(parent,ctrl):
		if parent is c["g"]:
			u["tops"].append(ctrl)
			if u["hidden"]:ctrl.IsVisible=False
	def cN(layer,shown):
		for a in layer["tops"]:a.IsVisible=shown
		layer["hidden"]=not shown
	def aj(parent,ctrl,a):cM(parent,ctrl);parent.Add(ctrl);a.append(ctrl);return ctrl
	def S(parent,x,y,w,h,color,alpha,a):b=G.CreateGumpColorBox(alpha,color);b.SetRect(e(x),e(y),max(1,e(w)),max(1,e(h)));return aj(parent,b,a)
	def p(parent,text,x,y,size,color,a,width=0,align="left",smooth=False):
		b=ah.get(color)
		if b is not None and not smooth and not(width and align=="left"):l=G.CreateGumpLabel(text,b);l.SetAcceptMouseInput(False);cO(l,x,y,size,width,align);return aj(parent,l,a)
		size=max(6,Kit.tsize(e(size)))
		if width:l=G.CreateGumpTTFLabel(text,size,color,aligned=align,maxWidth=e(width))
		else:l=G.CreateGumpTTFLabel(text,size,color)
		l.SetPos(e(x),e(y));l.SetAcceptMouseInput(False);return aj(parent,l,a)
	at={}
	def cO(l,x,y,size,width,align):
		a=int(l.GetWidth())or 7*len(l.Text or "");b=int(l.GetHeight())or 16;X=e(x)
		if width and align=="center":X+=max(0,(e(width)-a)//2)
		elif width and align=="right":X+=max(0,e(width)-a)
		Y=e(y)+max(0,(int(e(size)*1.3)-b)//2);l.SetPos(X,Y)
		if width and align!="left":
			if len(at)>3000:
				for k in[d for d in at if d.IsDisposed]:del at[k]
			at[l]=(x,y,size,width,align)
	def d0(l,text):
		l.Text=text;m=at.get(l)
		if m is not None:cO(l,m[0],m[1],m[2],m[3],m[4])
	def cP(parent,graphic,x,y,size,a):p=G.CreateGumpItemPic(graphic,e(size),e(size));p.SetPos(e(x),e(y));p.SetAcceptMouseInput(False);return aj(parent,p,a)
	def cQ(parent,x,y,on,c):
		d=b3 if on else b4;a=[]
		for e,f,g,h in((6,0,2,4),(0,4,14,2),(3,6,8,3),(2,9,3,3),(9,9,3,3)):b=S(parent,x+e,y+f,g,h,d,1.,c);b.SetAcceptMouseInput(False);a.append(b)
		return a
	d1=dict((ff,tuple(int(fg[fh:fh+2],16)for fh in(1,3,5)))for ff,fg in((True,b3),(False,b4)))
	def cR(parts,on):
		r,a,b=d1[bool(on)]
		for p in parts:p.SetBaseColor(r,a,b,255)
	def ad(ctrl,fn):G.AddControlOnClick(ctrl,fn)
	aT={"ok":None}
	def cS(a,fn):
		if aT["ok"]is False:return False
		aT["ok"]=Kit.hook_double(a,fn,queue=False)
		if not aT["ok"]:k("double-clicks can't be caught on this client; click a row, then click it again to use it.",Kit.HUE_BAD)
		return aT["ok"]
	def cT(key,action):
		def a():
			b=time.time();a=Q["selected"]
			if a is not None and a!=key and a in ab:ab[a].SetAlpha(a4)
			if key in ab:ab[key].SetAlpha(.2)
			Q["selected"]=key
			if aT["ok"]is False and Q["key"]==key and b-Q["t"]<=3.:Q["key"],Q["t"]=None,0.;cX(bl(action,b))
			else:Q["key"],Q["t"]=key,b
		return a
	def bl(action,now=None):
		if action[0]=="cast":return action+(now or time.time(),)
		if action[0]in("travel","favgo"):return("pressed",now or time.time(),action)
		return action
	def cU(bg,key,action):ad(bg,cT(key,action));cS(bg,cW(action))
	def cV(i):
		if i!=b["circle"]or b["tab"]!="spells":di("spells",lambda:b.update({"circle":i}))
	def cW(action):
		def a():cX(bl(action))
		return a
	def cX(act):
		if act[0]=="cast"and L["reading"]and not b["shutting"]and o["wait"]is None and not o["claim"]and not ar()and not API.HasTarget("any"):bY(act[1],Client.on_client_thread());return
		O.add(act,dup=True)
	def ak(action):
		def a():
			if action not in b["ui_queue"]:b["ui_queue"].append(action)
		return a
	def ae(name,default):
		try:return int(Kit.get_var("Grimoire_"+name,str(default)))
		except Exception:return default
	def al(name,value):Kit.put_var("Grimoire_"+name,str(int(value)))
	au={"value":None,"t":0.}
	def cY():C["scale"]=min(a1,max(ag,ae("Scale",100)))/100.;c["w"]=max(e(aP),ae("W",e(cc)));c["h"]=max(e(aQ),ae("H",e(cd)));c["opacity"]=min(100,max(0,ae("Opacity",bA)));bm()
	def bm():
		if E["own"]is not None:return
		W,H=Kit.screen()
		if H>0:c["h"]=max(aQ*ag//100,min(c["h"],H))
		if W>0:c["w"]=max(aP*ag//100,min(c["w"],W))
	def LW():return max(aP,int(c["w"]/C["scale"]))
	def LH():return max(aQ,int(c["h"]/C["scale"]))
	af={"parts":[]}
	def d2():
		if b["minimized"]:return
		c["w"],c["h"]=c["g"].GetWidth(),c["g"].GetHeight();m["size_dirty"]=True;b["dirty"]=True;m["settle"]=time.time()+.3
	def cZ():
		m["size_dirty"]=False
		if E["own"]is not None:return
		for k,v in(("W",c["w"]),("H",c["h"])):al(k,v)
	def d3():
		bm();a,b=ae("X",-1),ae("Y",-1)
		if a>=0:a,b=Kit.adapt(a,max(0,b),c["w"],c["h"]);a,b=Kit.clamp(a,b,c["w"],c["h"]);a,b=max(0,a),max(0,b)
		c["g"]=g=G.CreateModernGump(a if a>=0 else 100,b if b>=0 else 60,c["w"],c["h"],True,aP*ag//100,aQ*ag//100,d2);g.SetAlpha(0)
		if a<0:g.CenterXInViewPort();g.CenterYInViewPort()
	e7=None
	def aU(a):
		for c in a:at.pop(c,None);c.Dispose()
		del a[:]
	bO={}
	def av(graphic):
		if graphic not in bO:p=G.CreateGumpPic(graphic,0,0,0);bO[graphic]=(int(p.GetWidth()),int(p.GetHeight()));p.Dispose()
		return bO[graphic]
	def aH(parent,graphic,X,Y,W,H,a,mouse=False,hue=0):
		p=G.CreateGumpPic(graphic,X,Y,Kit.look_hue(graphic,hue));p.SetWidth(max(1,W));p.SetHeight(max(1,H))
		if not mouse:p.SetAcceptMouseInput(False)
		return aj(parent,p,a)
	def bP(parent,graphic,X,Y,W,H,a):t=G.CreateTiledGumpPic(graphic,max(1,W),max(1,H),Kit.look_hue(graphic));t.SetRect(X,Y,max(1,W),max(1,H));t.SetAcceptMouseInput(False);return aj(parent,t,a)
	def d4(parent,x,y,w,h,q,alpha=1.):
		a,b,c,d=e(x),e(y),e(x+w),e(y+h);m,n=av(a3);o,p=av(a3+8);m,o=min(m,(c-a)//2),min(o,(c-a)//2);n,p=min(n,(d-b)//2),min(p,(d-b)//2);f=[a,a+m,c-o,c];g=[b,b+n,d-p,d];j=[]
		for i in[4,0,1,2,3,5,6,7,8]:
			k,l=i%3,i//3;W,H=f[k+1]-f[k],g[l+1]-g[l]
			if W<=0 or H<=0:continue
			if i in(0,2,6,8):j.append(aH(parent,a3+i,f[k],g[l],W,H,q))
			else:j.append(bP(parent,a3+i,f[k],g[l],W,H,q))
		for r in j:r.SetAlpha(alpha)
		return[(s,1.)for s in j]
	def aV(parent,x,y,w,h,a,alpha=1.):p=bP(parent,Kit.SECTION_TILE,e(x),e(y),e(w),e(h),a);p.SetAlpha(alpha*Kit.SECTION_ALPHA);return[(p,Kit.SECTION_ALPHA)]
	def d5(w,h,d):a,b=av(Kit.CORNER_ART);W,H=e(w),e(h);return[aH(c["g"],Kit.CORNER_ART,f,g,a,b,d)for f,g in((0,0),(W-a,0),(0,H-b),(W-a,H-b))]
	aW={}
	def bQ(text):return int(round(Kit.text_px(text)/C["scale"]))
	def aI(text,room,size=None):
		if size is None:return Kit.fit(text,e(room))
		if bR(text,size)<=room:return text
		a,b=2,len(text)-1
		while a<b:
			c=(a+b+1)//2
			if bR(text[:c]+"..",size)<=room:a=c
			else:b=c-1
		return text[:a].rstrip()+".."
	def bR(text,size):
		a=(text,size,C["scale"],Kit.tscale)
		if a not in aW:
			if len(aW)>=4000:aW.clear()
			l=G.CreateGumpTTFLabel(text,max(6,Kit.tsize(e(size))),J);b=int(l.GetWidth()or 0);l.Dispose();aW[a]=b or int(.55*size*len(text))
		return int(round(aW[a]/C["scale"]))
	def c_(art):return int(round(av(art[0])[0]/C["scale"]))
	def am(x,y,w,h,text,tooltip,fn,size=14,parent=None,art=Kit.ART_PLAY):
		parent=parent or c["g"];a=u["ctrls"];g,i=av(art[0]);b=G.CreateGumpButton("",0,art[0],art[1],art[2]);b.SetPos(e(x),e(y)+max(0,(e(h)-i)//2));aj(parent,b,a);ad(b,fn);Kit.with_tip(b,tooltip)
		if text:d=x+int(round(g/C["scale"]))+4;p(parent,text,d,y+(h-size)//2-1,size,J,a);f=S(parent,d,y,max(4,x+w-d),h,ap,0.,a);ad(f,fn);Kit.with_tip(f,tooltip)
		return b
	def d6():
		if Kit.zone_up(r)and not b["minimized"]:return
		aL(r,False);aJ()
	def bS():
		if Kit.zone_up(r):return
		aL(r,True)
		if not b["minimized"]:aJ()
		if bZ():aw(True)
		else:HOST.dock_note(aM)
	def aJ(save=True):
		b["minimized"]=not b["minimized"]
		if b["minimized"]:c["g"].SetResizable(False);c["g"].SetHeight(e(by))
		else:c["g"].SetHeight(c["h"]);c["g"].SetResizable(E["own"]is None)
		aw(False);b["dirty"]=True
		if save:al("Min",1 if b["minimized"]else 0)
	def d7():
		a=Kit.zone_up(r)
		if not a:aL(r,False)
		if b["minimized"]:aJ(not a)
		aw(False)
	def d8():
		if not b["minimized"]:aJ()
	def d9():aw(False)
	def c0():
		if Kit.zone_up(r):return
		x,y=int(c["g"].GetX()),int(c["g"].GetY());m["last_pos"]=(x,y)
		for k,v in(("X",x),("Y",y)):al(k,v)
	def aw(on):
		on=bool(on)
		if on==b["docked"]:return
		b["docked"]=on;c["g"].IsVisible=not on;Kit.stir()
	def c1():
		a=time.time()
		if a<b.get("link_next",0.):return
		b["link_next"]=a+.1
		if b.pop("to_bar",False):bS()
		c=API.GetSharedVar(bz)
		if c:
			API.RemoveSharedVar(bz);c=str(c)
			if c=="show"and(b["minimized"]or b["docked"]):
				aL(r,False)
				if b["minimized"]:aJ()
				aw(False)
			elif c=="dock"and not b["docked"]:bS()
		if b["docked"]:
			if not HOST.bar_soon():aw(False)
		elif b["minimized"]and a>=b.get("wish_next",0.):
			b["wish_next"]=a+.25
			if bu(r)and bZ():aw(True)
		elif not b["minimized"]and a>=b.get("wish_next",0.):
			b["wish_next"]=a+1.
			if bu(r)and not Kit.zone_up(r):aL(r,False)
		d="docked"if b["docked"]else("minimized"if b["minimized"]else "open")
		if d!=b["link_state"]:b["link_state"]=d;API.SetSharedVar(ce,d)
	def ea(value):
		c["opacity"]=int(value)
		for p,a in af["parts"]:p.SetAlpha(c["opacity"]/100.*a)
		al("Opacity",c["opacity"])
	def eb(value):au["value"]=int(value);au["t"]=time.time()
	def bT():c["g"].SetWidth(c["w"]);c["g"].SetHeight(e(by)if b["minimized"]else c["h"]);b["dirty"]=True
	def c2(new,w,h):
		for k,v in(("Scale",int(round(new*100))),("W",w),("H",h)):al(k,v)
	def c3(new,save):
		if abs(new-C["scale"])<.001:return
		a=new/C["scale"];C["scale"]=new;c["w"],c["h"]=int(round(c["w"]*a)),int(round(c["h"]*a));b,d=c["w"],c["h"];bm();bT()
		if save:c2(new,b,d)
	def c4():
		e=au["value"];au["value"]=None;a=min(a1,max(ag,e))/100.
		if E["own"]is None:c3(a,True);return
		if abs(a-E["own"][0])<.001:return
		c=int(round(E["own"][1]*a/E["own"][0]));d=int(round(E["own"][2]*a/E["own"][0]));c3(a,False);E["own"]=(a,c,d);c2(a,c,d)
		if E["told"]is not None:b["ui_queue"].append(("fit",)+E["told"])
	E={"own":None,"told":None}
	def ec(w,h,mode):E["told"]=(w,h)if w else None;b["ui_queue"].append(("fit",w,h))
	def ed(w,h):
		if not w:
			a,E["own"]=E["own"],None
			if a is not None:C["scale"]=a[0];c["w"],c["h"]=a[1],a[2];bm();bT();c["g"].SetResizable(not b["minimized"])
			return
		if E["own"]is None:E["own"]=(C["scale"],c["w"],c["h"]);c["g"].SetResizable(False);b["dirty"]=True
		w,h=int(w),int(h)
		if b["minimized"]:h=c["h"]
		if(c["w"],c["h"])!=(w,h):c["w"],c["h"]=w,h;bT()
	aX=48
	def ee():
		w=LW();h=by if b["minimized"]else LH();a=u["ctrls"];e=c["opacity"]/100.;af["parts"]=d4(c["g"],0,0,w,h,a,e);g=[i for i,l in af["parts"]];d=Kit.zone_up(r);f=C["scale"]
		if d:C["scale"]=1.;w=c["w"]
		try:af["parts"]+=aV(c["g"],12,12,w-24,30,a,e)
		finally:C["scale"]=f
		if not b["minimized"]:g+=d5(LW(),h,a);af["parts"]+=aV(c["g"],12,h-40,LW()-24,28,a,e)
		Kit._frame_parts[c["g"]]=g
		if d:C["scale"]=1.
		try:ef(w,d)
		finally:C["scale"]=f
		return max(50,int(-(-50//f)))if d else 50
	def ef(w,a):
		d=u["ctrls"];p(c["g"],"GRIMOIRE",42,18,14,T,d);f=w-12-44-20-(0 if b["minimized"]else Kit.DOCK_DX+106+98);d.append(Kit.title_catcher(c["g"],e(12),e(12),e(f-16),e(30),ak(("min_click",)),key="grimoire:mini"if b["minimized"]else "grimoire"));x=w-12-44
		if not a:am(x,15,30,24,"",Kit.CLOSE_TIP%aM,ak(("close",)),art=Kit.ART_CLOSE);x-=20;am(x,15,16,24,"",Kit.RESTORE_TIP if b["minimized"]else Kit.MIN_TIP,ak(("min_click",)),art=Kit.ART_RESTORE if b["minimized"]else Kit.ART_MIN)
		if not b["minimized"]:
			if not a:x-=Kit.DOCK_DX;am(x,15,16,24,"",Kit.DOCK_TIP,lambda:b.__setitem__("to_bar",True),art=Kit.ART_DOCK)
			x-=106;am(x,15,100,24,"Settings",Kit.SETTINGS_TIP%aM,ak(("settings",)),art=Kit.ART_PAGE);x-=98;am(x,15,92,24,"Refresh","Find your spellbook and runebooks again and reread every runebook",O(("refresh",)),art=Kit.ART_OK)
	def bn():return LW()-an-20
	def bU(key):return key not in("spells","favs","+add")and not isinstance(key,tuple)
	def aY(serial):a=K.get(serial,(None,None))[0];return a is not None and a<b0
	def c5(key,title,short):
		a=title if short!=title else None
		if bU(key)and aY(key):b=K[key][0];a="%s: %s left (low)"%(title,Kit.count(b,"charge"))
		return a
	def c6(key,x,y,w,h,text,tooltip,title=None):
		d=u["ctrls"];n=b["tab"]==key;j=P if bU(key)and aY(key)else J;f,g=av(cf);k,l=e(x),e(y)+max(0,(e(h)-g)//2);aH(c["g"],cf,k,l,f,g,d);a=aH(c["g"],dq,k,l,f,g,d);a.SetAlpha(1. if n else 0.);o=p(c["g"],text,x+int(round(f/C["scale"]))+4,y+(h-14)//2-1,14,j,d);i=S(c["g"],x,y,w,h,ap,0.,d);m=eh(key);ad(i,m);ad(a,m)
		if tooltip:i.SetTooltip(tooltip);a.SetTooltip(tooltip)
		a9[key]=a
		if bU(key):ba[key]=(o,i,a,title or text,text,j==P)
	def eg(serial):
		a=ba.get(serial);b=aY(serial)
		if a is None or a[5]==b:return
		d,e,f,c,g,i=a;d.Hue=ah[P if b else J];ba[serial]=(d,e,f,c,g,b);h=c5(serial,c,g)or c;e.SetTooltip(h);f.SetTooltip(h)
	def eh(key):
		def a():b["switch"]=key
		return a
	def ei(top):
		m=[("spells","Spellbook")]+([("favs","Favourites")]if z else[])+[(n["serial"],n["title"])for n in z];f=bn();g=28;h,x,y=[],20,top+4;i=c_(Kit.ART_OK)
		for d,a in m:
			e=a if len(a)<18 else a[:16]+"..";w=max(90,i+4+bQ(e)+14)
			if x+w>f-4:x,y=20,y+g
			h.append((d,a,e,x,y,w));x+=w+6
		if b["scanned"]:
			a="Add runebook...";w=max(90,i+4+bQ(a)+14);j=f-4-w
			if x>j:y+=g
			h.append(("+add",a,a,j,y,w))
		k=y+g+2;l=c["opacity"]/100.;af["parts"]+=aV(c["g"],12,top,f-12,k-top,u["ctrls"],l)
		for d,a,e,x,y,w in h:
			if d=="+add":am(x,y,w,24,e,"Target an unlisted runebook; books of its kind are found from then on",O(("register",)),art=Kit.ART_OK)
			elif d=="favs":c6(d,x,y,w,24,e,"Starred destinations, last trip and a search of every runebook")
			else:c6(d,x,y,w,24,e,c5(d,a,e),a)
		top=k+Kit.GAP;af["parts"]+=aV(c["g"],12,top,f-12,LH()-aX-top,u["ctrls"],l);b["content_top"]=top+4;return top+4
	def bo(x,y,w,h):a=G.CreateGumpScrollArea(e(x),e(y),e(w),e(max(40,h)));u["ctrls"].append(a);return a
	def bp(ctrl):cM(c["g"],ctrl);c["g"].Add(ctrl)
	def ej(top):
		a=u["ctrls"];f=LW()-an-12;h=LH()-aX;af["parts"]+=aV(c["g"],f,top,an,h-top,a,c["opacity"]/100.);p(c["g"],"Supplies",f,top+8,15,T,a,width=an,align="center");i=[az[v]for v in dt];i+=[None,("Recall scroll",aN),("Gate scroll",aO)];j,l=40,34;o=sum(10 if w is None else j for w in i);g=top+32
		if g+o<=h:d,e,m,b=c["g"],f,g,None
		else:b=bo(f+2,g,an-2,h-g-4);d,e,m=b,0,0
		q=bc();y=m
		for r in i:
			if r is None:S(d,e+10,y+4,an-20-(16 if b else 0),1,I,.6,a);y+=10;continue
			s,k=r;cP(d,k,e+8,y+(j-l)//2,l,a);n=q.get(k,0);t=p(d,bd(n),e+48,y+3,15,J if n else P,a);u["counts"].append(co(k,t,n));p(d,aI(s,an-52-(16 if b else 0)),e+48,y+21,12,J,a);y+=j
		if b is not None:bp(b)
	def ek(top,circle):
		b=u["ctrls"];s=bn();x=22;D,E=av(cg);w=max(1,D*30//E)
		for i in range(8):
			k=aH(c["g"],cg+i,e(x),e(top+2),e(w),e(30),b,mouse=True)
			if circle!=i:k.SetAlpha(.45)
			ad(k,ak(("circle",i)));k.SetTooltip(a5[i][0]);x+=w+6
		F,G=a5[circle];p(c["g"],F,x+10,top+6,18,T,b);top+=38
		if not U:p(c["g"],"No spellbook in your pack or hands. Carry one, then click Refresh.",22,top+4,14,I,b);return
		d=bo(16,top,s-20,LH()-top-aX-4);l=100;t=bc();H=circle*8;n=s-34;o=a2+18;K=n-4*aA-6;L=m["mana"]
		for i,(g,v,z)in enumerate(G):
			y=i*l;a=aB is None or cj(g)in aB;A=("spell",g);h=S(d,0,y,n,l-4,ap,a4,b);ab[A]=h;f=[g,[az[W][1]for W in z.split()],c8[circle],None,None,h,None]
			if a:f[6]=c9(f,t,L)
			B=a and f[6][0];M=f[4]=aH(d,2240+H+i,e(8),e(y+(l-4-a2)//2),e(a2),e(a2),b,hue=0 if a else 946)
			if B:M.SetAlpha(c7)
			f[3]=p(d,g,o,y+14,17,(I if B else J)if a else ao,b);p(d,v if a else v+"  (not in your book)",o,y+38,13,I if a else ao,b,width=max(120,K-o-8));C=z.split();j=n-len(C)*aA-6
			for N in C:
				O,q=az[N];Q=cP(d,q,j+(aA-a7)//2,y+2,a7,b)
				if not a:Q.SetAlpha(.4)
				r=t.get(q,0);R=p(d,bd(r),j,y+a7+3,13,(J if r else P)if a else ao,b,width=aA,align="center");u["counts"].append(co(q,R,r,a));p(d,O,j,y+a7+20,11,I if a else ao,b,width=aA,align="center");j+=aA
			if a:cU(h,A,("cast",g));h.SetTooltip(da(f));u["spells"].append(f)
		bp(d)
	c7=.45;el=dict((fj,fi)for fi,fj in az.values());c8=Kit.SPELL_MANA
	def c9(a,totals,mana):
		for b in a[1]:
			if totals.get(b,0)<=0:return(True,"Out of "+el.get(b,"a reagent"))
		if mana is not None and mana<a[2]:return(True,"Not enough mana (needs %d)"%a[2])
		return(False,"")
	def da(a):
		b="Double-click to cast "+a[0]
		if a[6]is not None and a[6][0]:b+="\n"+a[6][1]
		return b
	def db():
		b=m["totals"]
		if b is None:return
		d=m["mana"]
		for f in list(t.values()):
			for e in f["spells"]:
				a=c9(e,b,d)
				if a==e[6]:continue
				e[6]=a;c=a[0];e[3].Hue=ah[I if c else J];e[4].SetAlpha(c7 if c else 1.);e[5].SetTooltip(da(e))
	def em(now):
		if(now<m["next_mana"]and m["next_mana"]-now<=b2)or b["tab"]!="spells"or b["minimized"]or b["docked"]:return
		m["next_mana"]=now+b2;a=int(API.Player.Mana);c=sum(1 for d in c8 if d<=a);m["mana"]=a
		if c!=m["tier"]:m["tier"]=c;db()
	def en(serial):
		a,b=K.get(serial,(None,None))
		if a is None:return None,1
		if b is None:return "Charges: %d"%a,a
		return "Charges: %d / %d"%(a,b),a
	def eo(top,serial):
		a=u["ctrls"];h=bn();N=next((bg for bg in z if bg["serial"]==serial),None)
		if N is None:
			if serial==b["tab"]:b["switch"]="spells"
			return
		p(c["g"],N["title"],22,top+2,ch,T,a,smooth=True);am(h-104,top+4,96,26,"Re-read","Read this runebook again",ak(("reread",serial)),size=15,art=Kit.ART_PAGE)
		if serial not in D:
			p(c["g"],"Reading this runebook",22,top+36,14,I,a)
			if serial in A:A.remove(serial)
			O.add(("read",serial));return
		Q,U=en(serial)
		if Q:p(c["g"],Q,h-340,top+6,20,T if U and not aY(serial)else P,a,width=226,align="right",smooth=True)
		e=D[serial]
		if e is None or(not e and serial in aq):ag=aq.get(serial,"Couldn't read this runebook.");p(c["g"],ag,22,top+36,14,P,a,width=h-26);p(c["g"],"Details saved to Grimoire_runebook_dump.txt in the VirtueAssistantSettings folder; send that file, then click Refresh."if serial in R["books"]else "Click Re-read to save this book's details to Grimoire_runebook_dump.txt in the VirtueAssistantSettings folder.",22,top+62,12,I,a,width=h-26);return
		if not e:p(c["g"],"No runes in this runebook. Add some, then click Re-read.",22,top+36,14,I,a);return
		x=bc();u["scrolls"]=cp(x);V={"recall_scroll":x.get(aN,0),"gate_scroll":x.get(aO,0),"charge":U};ah=K.get(serial,(None,None))[0]is not None;B=len(e);W=any(e8["slot"]is not None for e8 in e);ai=W or any(e9.get("rune")for e9 in e);p(c["g"],"%s; double-click a name to %s there"%(Kit.count(B,"destination"),ay),22,top+36,a6,I,a,smooth=True);C=c_(Kit.ART_PLAY);q=[]
		if ai:
			for m,n,r in du:
				if m=="charge"and not W:continue
				q.append((m,n,r,max(C+12,bR(n,a6)+12)))
		X=sum(fa[3]for fa in q);s=top+62;Y=s+26;E=h-34;aj=200+X+16;t=max(1,min(B,E//aj));i=E//t;F=i-X-20;Z=(B+t-1)//t;aa=LH()-Y-aX-4;f=max(36,min(54,aa//max(1,Z)));o=max(16,int((f-4)*.72));al=int(o*1.3)
		for v in range(t):
			hx=16+v*i+F+16;p(c["g"],"Destination",16+v*i+30,s,a6,T,a,smooth=True)
			for m,n,r,k in q:an=T if V.get(m,1)else P;p(c["g"],n,hx,s,a6,an,a,width=k,align="center",smooth=True);hx+=k
		S(c["g"],18,s+23,E-4,1,I,.5,a);g=bo(16,Y,h-20,aa);ao=u["stars"]
		for w,d in enumerate(e):
			v,ar=divmod(w,Z);l,y=v*i,ar*f;ac=("rune",serial,d["button"],d["name"]);G=S(g,l,y,i-6,f-4,ap,a4,a);ab[ac]=G;ae=d["slot"]is not None;at=bool(d.get("rune"));cU(G,ac,("travel",serial,d,bV(d)));G.SetTooltip("Double-click to %s to %s"%(ay,d["name"]));ao[w]=cQ(g,l+8,y+max(0,(f-4-14)//2),(serial,w)in j["keys"],a);af=S(g,l+2,y,26,f-4,ap,0.,a);ad(af,ak(("star",serial,w,d["name"])));af.SetTooltip(dc);ty=y+max(0,(f-4-al)//2)
			if not(ae or at):p(g,aI(d["name"],i-46,o),l+30,ty,o,J,a,smooth=True);continue
			p(g,aI(d["name"],F-24,o),l+30,ty,o,J,a,smooth=True);H=l+F+16
			for m,n,r,k in q:
				if m=="charge"and not ae:H+=k;continue
				L=V.get(m,1);M=r
				if m in("recall_scroll","gate_scroll"):M+=" (%d carried)"%L
				elif m=="charge"and ah:M+=" (%d left)"%L
				au=am(H+(k-C)//2,y+2,C,f-8,"",M,cW(("travel",serial,d,m)),parent=g)
				if not L:au.SetAlpha(.35)
				H+=k
		bp(g)
	def bV(dest):return ay if dest["slot"]is not None or dest.get("rune")else "charge"
	dc="Add to Favourites (click again to remove)";dd={"recall":"recall","gate":"gate","charge":"recall (a charge)","recall_scroll":"recall (a scroll)","gate_scroll":"gate (a scroll)","sacred":"travel (Sacred Journey)"}
	def ep(top):a=u["ctrls"];b=bn();p(c["g"],"Favourites",22,top+2,ch,T,a,smooth=True);f=220;g=b-8-f;h="Search:";p(c["g"],h,g-10-bQ(h),top+8,14,J,a);bP(c["g"],Kit.FIELD_TILE,e(g)-2,e(top+4)-1,e(f)+4,24,a);d=G.CreateGumpTextBox(Z["text"],e(f),22,False,16);d.SetPos(e(g),e(top+4));Kit.with_tip(d,"Search every runebook you carry by rune or book name (empty: your Favourites)");aj(c["g"],d,a);l=p(c["g"],"",22,top+38,14,I,a);i=top+62;j=b-34;k=bo(16,i,b-20,LH()-i-aX-4);Z.update({"layer":u,"tb":d,"info":l,"sa":k,"pool":[],"seen":None,"ver":-1,"row_w":j,"name_w":max(120,int(j*.55)),"info_w":b-30});df(building=True);bp(k)
	def eq():
		d=dict((v["serial"],v["title"])for v in z);k=[w["serial"]for w in z]
		if not k:return[],"No runebooks in your pack or hands."
		q=Z["text"].strip().lower();a=[]
		if q:
			a,l=de(q.split(),a0)
			if l:return a,"More than %d found; type more letters."%a0
			if a:return a,"%s found; double-click one to %s there"%(Kit.count(len(a),"destination"),ay)
			return a,"No rune or runebook name has '%s' in it."%Z["text"].strip()
		b=j["last"]
		if b is not None and b[0]in d:
			i=ai(b[0],b[1],b[2])
			if i is not None:a.append((b[0],i,b[2],d[b[0]],b[3],True))
		e={}
		for c in j["list"]:e.setdefault(c[0],[]).append(c)
		g=0
		for s in list(e):
			if s not in d:g+=len(e.pop(s))
		n=0
		for s in k:
			for c in sorted(e.get(s,()),key=lambda f:f[1]):
				i=ai(s,c[1],c[2])
				if i is None:g+=1;continue
				a.append((s,i,c[2],d[s],None,False));n+=1
		if n:h="%s; double-click one to %s there, or type above to search"%(Kit.count(n,"favourite"),ay)
		else:h="Click a destination's star on a runebook page to list it here."
		if g:h+="  (%d not in the books you carry)"%g
		return a[:a0+1],h
	def de(words,cap):
		a=[]
		for b in z:
			s,d=b["serial"],b["title"].lower();c=D.get(s)or()
			for i in range(len(c)):
				if all(f in c[i]["name"].lower()+"  "+d for f in words):
					if len(a)>=cap:return a,True
					a.append((s,i,c[i]["name"],b["title"],None,False))
		return a,False
	def df(building=False):
		a=Z;d=a["layer"]
		if d is None or(t.get("favs")is not d and not building):a["layer"]=None;return
		c,e=eq();a["ver"],a["seen"]=B["ver"],a["text"];Kit.set_text(a["info"],aI(e,a["info_w"]),ah[I]);b=a["pool"]
		for i in range(len(c)):
			if i>=len(b):b.append(er(i,c[i]))
			dh(b[i],c[i])
		for i in range(len(c),len(b)):dh(b[i],None)
	def er(i,row):f=Z;d,e,c=f["sa"],f["layer"]["ctrls"],30;y=i*c;b={"i":i,"a":None,"prev":None,"at":0.,"tip":None,"shown":True};b["bg"]=S(d,0,y,f["row_w"],c-4,ap,a4,e);ab[("fav",i)]=b["bg"];b["on"]=(row[0],row[1])in j["keys"];b["star"]=cQ(d,8,y+(c-4-14)//2,b["on"],e);b["hit"]=S(d,2,y,26,c-4,ap,0.,e);b["hit"].SetTooltip(dc);b["name"]=p(d,"",32,y+(c-4-14)//2-2,14,J,e);b["book"]=p(d,"",32+f["name_w"]+10,y+(c-4-14)//2-2,14,I,e);ad(b["hit"],bW(b,lambda a:ak(("star",a[0],a[1],a[2]))()));ad(b["bg"],bW(b,lambda a:cT(("fav",b["i"]),("favgo",)+a)()));cS(b["bg"],bW(b,lambda a:O.add(bl(("favgo",)+a),dup=True)));return b
	def dg(slot,shown):
		slot["shown"]=shown
		for a in[slot["bg"],slot["hit"],slot["name"],slot["book"]]+slot["star"]:a.IsVisible=shown
	def dh(slot,row):
		if row is None:
			if slot["a"]is not None:slot["prev"],slot["at"],slot["a"]=slot["a"],time.time(),None
			if slot["shown"]:dg(slot,False)
			return
		d=(row[0],row[1],row[2],row[4],row[5])
		if slot["a"]!=d:slot["prev"],slot["at"],slot["a"]=slot["a"],time.time(),d
		if not slot["shown"]:dg(slot,True)
		a=Z;Kit.set_text(slot["name"],aI(("Last: "if row[5]else "")+row[2],a["name_w"]-4),ah[J]);f=row[3]+((", "+dd.get(row[4],row[4]))if row[4]else "");Kit.set_text(slot["book"],aI(f,a["row_w"]-a["name_w"]-46),ah[I]);b=(row[0],row[1])in j["keys"]
		if b!=slot["on"]:cR(slot["star"],b);slot["on"]=b
		e=D.get(row[0])or();m=row[4]or(bV(e[row[1]])if row[1]<len(e)else ay);c="Double-click to %s to %s (%s)"%(dd.get(m,m),row[2],row[3])
		if c!=slot["tip"]:slot["tip"]=c;Kit.with_tip(slot["bg"],c)
	def bW(slot,go):
		def a():
			a=slot["prev"]if slot["prev"]is not None and time.time()-slot["at"]<.15 else slot["a"]
			if a is not None:go(a)
		return a
	def es(now):
		a=Z
		if a["layer"]is None:return
		if t.get("favs")is not a["layer"]:a["layer"]=None;return
		if b["tab"]!="favs"or b["minimized"]or b["docked"]:return
		if now>=a["next"]or a["next"]-now>b1:a["next"]=now+b1;a["text"]=str(a["tb"].Text or "")
		if a["text"]!=a["seen"]or a["ver"]!=B["ver"]:df()
	def et(act):
		a,d,b,e=act[1],act[2],act[3],act[4];i=ai(a,d,b)
		if i is None:k("%s isn't in that runebook any more."%b,Kit.HUE_BAD);return
		c=D[a][i];return("travel",a,c,e or bV(c))
	def aK(tab):return("spells",b["circle"])if tab=="spells"else tab
	def aZ(key,hidden):
		nonlocal u;a=t.pop(key,None);c=u=ci(hidden)
		try:
			if isinstance(key,tuple):ek(b["content_top"],key[1])
			elif key=="favs":ep(b["content_top"])
			else:eo(b["content_top"],key)
		finally:u=aa
		t[key]=c
		if a is not None:aU(a["ctrls"])
		return c
	def bX(key):
		if b["minimized"]or b["dirty"]:
			if key in t:aU(t.pop(key)["ctrls"])
			return
		aZ(key,key!=aK(b["tab"]))
	def eu():
		a=[("spells",d)for d in range(len(a5))]
		if z:a.append("favs")
		a+=[f["serial"]for f in z if f["serial"]in D];return a
	def di(tab,change=None):
		c=aK(b["tab"])
		if change:change()
		b["tab"]=tab;al("Tab",0 if tab=="spells"else(bx if tab=="favs"else tab));al("Circle",b["circle"])
		if tab=="spells":m["next_mana"]=0.
		a=aK(tab)
		if a==c and a in t and not t[a]["hidden"]:return
		Q["selected"]=None
		if c in t:cN(t[c],False)
		if a in t:cN(t[a],True)
		else:aZ(a,False)
	def ev(key):
		for k,a in a9.items():a.SetAlpha(1. if k==key else 0.)
		di(key)
	def ew():
		if b["minimized"]:return False
		a=[d for d in eu()if d not in t]
		if a:aZ(a[0],a[0]!=aK(b["tab"]))
		m["next_prebuild"]=time.time()+b8;return bool(a)
	def dj():
		d=aa["ctrls"][:]
		for k in("ctrls","tops","counts"):del aa[k][:]
		e=list(t.values())
		for f in(t,ab,a9):f.clear()
		Q["selected"]=None;b["dirty"]=False;a=ee()
		if not b["minimized"]:ej(a);ei(a);p(c["g"],b["status"],30,LH()-35,12,I,aa["ctrls"]);aZ(aK(b["tab"]),False);m["next_prebuild"]=time.time()+b8
		aU(d)
		for g in e:aU(g["ctrls"])
	def ex(full=False,bags=True):nonlocal U,aB;be();dO();U=Kit.on_client(dv);aB=dx(force=full);Kit.on_client(lambda:ey(full,bags))
	def ey(full,bags):
		nonlocal z;z=dD();del A[:]
		for d in z:
			s=d["serial"];c=s in D or dN(s)
			if full or not c:A.append(s)
			if c and s not in aS:aS[s]=K.get(s,(None,None))[0]
			if c and D.get(s):cA(s)
		B["ver"]+=1;a=b.pop("want_tab",None)
		if a and(any(f["serial"]==a for f in z)or(a==bx and z)):b["tab"]="favs"if a==bx else a
		if b["tab"]in A:A.remove(b["tab"]);A.insert(0,b["tab"])
		if(b["tab"]=="favs"and not z)or(b["tab"]not in("favs","spells")and not any(g["serial"]==b["tab"]for g in z)):b["tab"]="spells"
		e=("All spells shown"if aB is None else "%d spells known"%len(aB));b["status"]="%s, %s"%(e if U else "No spellbook",Kit.count(len(z),"runebook"))
		if not z and bags and(full or not b["reported"]):dA();b["reported"]=True
		b["scanned"]=True;b["dirty"]=True
	def ez(serial):
		a,b=dT(serial)
		if a=="busy":
			if serial not in A:A.insert(0,serial)
			return
		if cz(serial,a,b):Kit.on_client(lambda:bX(serial))
	def eA():b["closed"]=True
	def eB(act,now):
		if 0<=now-act[1]<=3.:dk[act[2][0]](act[2],now)
		else:k("trip not made; Grimoire was busy with a runebook. Press it again.",Kit.HUE_INFO)
	def eC(act,now):
		if len(act)>2 and now-act[2]>ca:k("%s was not cast; Grimoire was busy with a runebook."%act[1],Kit.HUE_INFO)
		elif o["wait"]is not None:pass
		elif ar():o["wait"]=(act[1],now+ca);k("target cursor in use; %s is cast once it is free."%act[1],Kit.HUE_INFO)
		else:bY(act[1])
	def eD(act,now):
		if act[1]in A:A.remove(act[1])
		if now<L["hold"]or b["pick"]is not None or o["claim"]or o["wait"]is not None or ar()or API.HasTarget("any"):A.insert(0,act[1])
		else:M.append(act)
	def bq(act,now):
		if act[0]=="refresh":R["armed"]=True
		M.append(act)
	def eE(act,now):
		a=et(act)
		if a is not None:M.append(a)
	def eF(act,now):
		if dC(act[1]):O.add(("scan",),dup=True,front=True)
	dk={"pressed":eB,"cast":eC,"read":eD,"travel":bq,"scan":bq,"rescan":bq,"refresh":bq,"favgo":eE,"register":lambda act,now:dB(),"registered":eF}
	def eG(w):return(("WINDOW",(("slider","opacity","Background opacity:","How solid the stone and black backdrop are (0-100, 0 = see-through)",0,100),("slider","scale","Scale:","Size of everything in the window (%d-%d%%, applied when the slider stops)"%(ag,a1),ag,a1),("note","Drag a window corner to resize.",{"ndy":2})),{"sh":124}),)
	eH={"top":34,"fh":30,"ldy":0,"sdy":4,"lw":178,"sw":200,"ugap":12,"vfmt":"%d%%"}
	def eI(old,new):
		if new["opacity"]!=old["opacity"]:ea(new["opacity"])
		if new["scale"]!=old["scale"]:
			eb(new["scale"])
			if not Kit.is_open(c["g"]):c4()
	br=Kit.Page(aR,eG,None,eI,eH)
	def eJ(g,x,y,w):
		if not aR["loaded"]and not Kit.is_open(c["g"]):aR["loaded"]=True;cY()
		aR.update({"opacity":c["opacity"],"scale":int(round(C["scale"]*100))});br.build(g,x,y,w)
	m={};ax={};M=[];o={"rd":None,"me":""}
	def eK():
		nonlocal u;b.update({"tab":"spells","circle":0,"dirty":True,"closed":False,"queue":[],"ui_queue":[],"status":"Reading your books","minimized":False,"switch":None,"content_top":0,"shutting":False,"scanned":False,"reported":False,"docked":False,"link_state":None,"pick":None})
		for k in("ctrls","tops","counts"):del aa[k][:]
		for d in(t,ab,a9,ba,at,aS,bB):d.clear()
		for a in(M,A,aC):del a[:]
		u=aa;af["parts"]=[];m.update({"next_count":0.,"next_prebuild":0.,"last_pos":(None,None),"held":None,"totals":None,"settle":0.,"size_dirty":False,"mana":None,"tier":None,"next_mana":0.});ax["busy"],ax["at"]=False,0.;Z.update({"layer":None,"tb":None,"info":None,"sa":None,"pool":[],"text":"","seen":None,"ver":-1,"next":0.});B["ver"]+=1;B["dest_ver"]=-1;o.update({"wait":None,"claim":0.,"seen":False,"next":0.});R.update({"written":False,"armed":False});aE.clear();aE.update(ck())
	def eL():
		if b["closed"]or b["shutting"]or not Kit.is_open(c["g"]):return
		return "docked"if b["docked"]else("minimized"if b["minimized"]else "open")
	def eM():
		eK();O.add(("scan",),dup=True);E["own"]=None;cY();b["circle"]=max(0,min(len(a5)-1,ae("Circle",0)));b["want_tab"]=ae("Tab",0)or None;d3();G.AddControlOnDisposed(c["g"],eA)
		if ae("Min",0)==1 or bu(r):aJ()
		b["docked"]=bool(b["minimized"]and HOST.dock_soon(r));Kit.add_front(c["g"],b["docked"]);Kit.on_moved(c["g"],c0);HOST.dock_add(r,{"title":aM,"icon":bv[0],"state":eL,"show":d7,"minimize":d8,"dock":bS,"undock":d9,"gump":lambda:c["g"],"fit":ec,"exact":True,"verify":True,"min":lambda:(e(aP),e(aQ))});a8.add(HOST.dock_remove,r);E["own"],E["told"]=None,None;a8.service("look.grimoire",lambda:b.update(dirty=True));API.RemoveSharedVar(bz);c1();HOST.alert_kind("grimoire.charges","Runebook low on charges",490)
		for a,d in eX.items():a8.service(a,d)
	def eN(act):
		a=act[0]
		if a=="min_click":d6()
		elif a=="circle":
			i=act[1]
			if("spells",i)in t and not b["dirty"]:cV(i)
			else:b["switch"]=("spells",i)
		elif a=="settings":HOST.show_settings(r)
		elif a=="fit":ed(act[1],act[2])
		elif a=="close":Kit.dispose(c["g"])
		elif a=="reread":R["armed"]=True;O.add(("read",act[1]),dup=True)
		elif a=="star":
			d,i=act[1],act[2];e=dP(d,i,act[3])
			if e is None:return
			f=t.get(d);g=f["stars"].get(i)if f is not None else None
			if g is not None:cR(g,e)
	def bY(name,b=False):
		a=time.time()
		if name in dp:API.CastSpell(name);L["hold"]=a+cb;return
		bt(r,b9);o.update({"claim":a+b9,"seen":False,"next":a+.1,"rd":Journal.Reader()if b else Journal.reader(),"me":bM()});API.CastSpell(name);L["hold"]=a+cb
	def dl():o["claim"],o["rd"]=0.,None;a_(r)
	def eO(now):
		if now>=o["claim"]:dl();return
		if now<o["next"]:return
		o["next"]=now+.1
		if API.HasTarget():o["seen"]=True
		elif o["seen"]or cL(o["rd"].new(),b7,o["me"]):dl()
	def eP(now):
		if API.HasTarget("any"):L["cursor_next"]=now+.25;return True
		return False
	def eQ():
		if b["closed"]:
			if not b["shutting"]:HOST.disable(r)
			return
		a=time.time()
		if au["value"]is not None and a-au["t"]>=.4:c4()
		c1()
		while b["ui_queue"]:
			eN(b["ui_queue"].pop(0))
			if b["closed"]:return
		if a>=m["settle"]:
			if m["size_dirty"]:cZ()
			if b["dirty"]:dj()
		if b["switch"]is not None:
			c,b["switch"]=b["switch"],None
			if isinstance(c,tuple):cV(c[1])
			else:ev(c)
			if b["dirty"]:dj()
		if aC:eR()
		if o["claim"]:eO(a)
		if o["wait"]is not None:
			d,f=o["wait"]
			if not ar():o["wait"]=None;bY(d)
			elif a>=f:o["wait"]=None;k("%s was not cast; the target cursor stayed in use."%d,Kit.HUE_BAD)
		if M:pass
		elif b["queue"]:e=b["queue"].pop(0);dk[e[0]](e,a)
		elif A and a>=L["hold"]and b["pick"]is None and o["claim"]==0. and o["wait"]is None and not ar()and a>=L.get("cursor_next",0.)and not eP(a):M.append(("read",A.pop(0)))
		if not M and not b["dirty"]and b["switch"]is None and a>=m["next_prebuild"]:ew()
		if b["closed"]:return
		if a>=m["next_count"]:dz();e2();m["next_count"]=time.time()+1.5
		em(a);es(a)
	def eR():
		while aC:
			a=aC.pop(0);b=K.get(a,(None,None))[0];c=aS.get(a);aS[a]=b;d=aY(a);e=c is not None and c<b0
			if d and not e:f=next((h["title"]for h in z if h["serial"]==a),"A runebook");g="%s left"%Kit.count(b,"charge");HOST.alert("grimoire.charges","%s: %s"%(f,g),who=a)
			eg(a)
	def dm():return(ax["busy"]or time.time()-ax["at"]<2. or any(d[0]=="travel"for d in M)or any(f[0]in("travel","favgo")or(f[0]=="pressed"and f[2][0]in("travel","favgo"))for f in b["queue"]))
	def eS(book_serial,e,method,name=None):
		if b["shutting"]or b["closed"]:return False
		if method not in b_:k("no way to travel called '%s'."%method,Kit.HUE_BAD);return False
		try:c,f=int(book_serial),int(e)
		except(TypeError,ValueError):return False
		if not b["scanned"]:k("still finding your runebooks; try again shortly.",Kit.HUE_INFO);return False
		d=next((g["title"]for g in z if g["serial"]==c),None)
		if d is None:k("that runebook isn't in your pack or hands.",Kit.HUE_BAD);return False
		try:a=D[c][ai(c,f,name)]
		except(KeyError,IndexError,TypeError):a=None
		if a is None:k("%s isn't in %s any more."%(name or "that rune",d),Kit.HUE_BAD);return False
		if method=="charge"and a.get("rune"):k("%s has no charges to use; pick Recall instead."%d,Kit.HUE_BAD);return False
		if method in("gate","sacred")and a.get("slot")is None and not a.get("rune"):k("%s has its own layout; only its rune's own button works there, not %s."%(d,"Gate Travel"if method=="gate"else "Sacred Journey"),Kit.HUE_BAD);return False
		if dm():k("a trip is already on its way.",Kit.HUE_INFO);return False
		O.add(("travel",c,a,method),dup=True);return True
	def eT(q,n=8):
		a=str(q or "").lower().split()
		if not a or b["shutting"]or b["closed"]:return[]
		return[("%s  (%s)"%(d[2],d[3]),(d[0],d[1],d[2]))for d in de(a,max(0,int(n or 0)))[0]]
	def eU(a):
		if b["shutting"]or b["closed"]:k("trip not made; Grimoire is closing.",Kit.HUE_INFO);return False
		try:c,e,d=int(a[0]),int(a[1]),str(a[2])
		except Exception:return False
		if not any(f["serial"]==c for f in z)or ai(c,e,d)is None:k("%s isn't in the runebooks you carry any more."%d,Kit.HUE_BAD);return False
		if dm():k("a trip is already on its way.",Kit.HUE_INFO);return False
		O.add(bl(("favgo",c,e,d,None,False)),dup=True);HOST.poke(r);return True
	def eV():
		if B["dest_ver"]!=B["ver"]:B["dests"]=[{"book":a["serial"],"book_name":a["title"],"index":f,"name":g["name"],"charges":K.get(a["serial"],(None,None))[0]}for a in z for f,g in enumerate(D.get(a["serial"])or())];B["dest_ver"]=B["ver"]
		return list(B["dests"])
	def eW():
		if B.get("chg_ver")!=B["ver"]:B["charges"]=dict((a["serial"],K.get(a["serial"],(None,None))[0])for a in z if D.get(a["serial"]));B["chg_ver"]=B["ver"]
		return B["charges"]
	eX={"grimoire.travel":eS,"grimoire.destinations":eV,"grimoire.book_charges":eW,"grimoire.find":eT,"grimoire.go":eU}
	def eY():
		try:e0()
		finally:cx()
	def eZ():a=(b["ui_queue"]or b["queue"]or M or A or aC or o["claim"]or b["dirty"]or o["wait"]is not None or b["switch"]is not None or au["value"]is not None or m["size_dirty"]);return.05 if a else.15
	def e_():return bool(M or j["save"]or j["save_last"]or(F["dirty"]and time.time()>=F["retry_at"]))
	def e0():
		if b["closed"]:return
		if j["save"]or j["save_last"]:bj()
		if not M:return
		a=M[0];c=a[0]
		if c=="travel":ax["busy"],ax["at"]=True,time.time()
		M.pop(0)
		if c=="travel":
			try:dQ(a[1],a[2],a[3]);bj();d_(a[1],a[2],a[3])
			finally:ax["busy"]=False
			L["hold"]=time.time()+6.
		elif c=="read":
			if API.HasTarget("any"):
				if a[1]in A:A.remove(a[1])
				A.insert(0,a[1]);return
			L["reading"]=True
			try:ez(a[1])
			finally:L["reading"]=False
			L["hold"]=max(L["hold"],time.time()+.55)
		else:ex(full=c=="refresh",bags=c!="rescan")
	bs={}
	def e1(it,c):
		g=it.Graphic
		if g in cq:return True
		h=it.Hue
		if(g,h)in aE:return True
		b=(it.Serial,g,h);a=None if c else bs.get(b)
		if a is None:
			n=it.Name;a=bC(g,h,n)
			if n:
				if len(bs)>200:bs.clear()
				bs[b]=a
		return a
	def e2():
		m["hand_looks"]=n=m.get("hand_looks",0)+1;b=n%10==0;a=sorted(d.Serial for d in bb()if e1(d,b))
		if m["held"]is not None and a!=m["held"]:O.add(("rescan",))
		m["held"]=a
	def e3():
		b["shutting"]=True;a8.close();bj();cx(True);b["docked"],b["link_state"]=False,None;API.SetSharedVar(ce,"off");a_(r);o.update({"wait":None,"claim":0.,"seen":False,"rd":None})
		def a():
			if Kit.is_open(c["g"]):c0();return True
			return False
		d=Kit.on_client(a)
		if not d and m["last_pos"][0]is not None:
			for k,v in zip(("X","Y"),m["last_pos"]):al(k,v)
		if m["size_dirty"]:cZ()
		if Kit.is_open(c["g"]):Kit.dispose(c["g"])
	return{"start":eM,"tick":eQ,"stop":e3,"client_tick":True,"config_height":br.height,"build_config":eJ,"poll_config":br.poll,"config_closed":br.closed,"thread_tick":eY,"thread_wanted":e_,"interval":eZ}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("grimoire","Grimoire","Spellbook, runebooks and reagents",_module_grimoire,.05,category="Your things")
