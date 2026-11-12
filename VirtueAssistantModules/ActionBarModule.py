def _module_actionbar():
	aW=Client._type;aF=Client.on_client_thread;ca=HOST.aborting;cb=HOST.cursor_busy;cc=HOST.dock_forget;cd=HOST.dock_to_bar;br=HOST.enable;bs=HOST.layout_arranging;ce=HOST.layout_in_use;cf=HOST.layout_locked;cg=HOST.layout_need;ch=HOST.pack_ver;aG=HOST.poke;ab=HOST.refresh_settings;ci=HOST.release_typing;aX=HOST.show_settings;bt=HOST.typing;r="actionbar";aH="Action Bar";cj="ActionBar_settings";bu="ActionBar_pos";bv="ActionBar_min";u=24;H=12;D=11;I=5;P=u+H;N=12;dI=22;aY,aZ=36,64;ac,ai=50,150;dJ=8;dK=44;ck=.65;dL=4;dM=3;dN=30;ad=4;ae=2624;af=.92;bw=.75;cl=2.;cm=5;dO=.1;au=("r",0);dP=10.;cn=20;dQ=70;dR=16;dS="#E8B830";dT=14;av=9;co=11;dU="#ECECEC";dV="#FFFFFF";dW=.88;dX=.58;dY=300;dZ=((" ijlI.,:;'!|",.26),("frt()[]-/",.36),("mwMW",.9),("ABCDEFGHJKLNOPQRSTUVXYZ&%@",.72));cp=set(("clumsy|feeblemind|magic arrow|weaken|harm|fireball|poison|curse|lightning|mana drain|mind blast|paralyze|dispel|energy bolt|explosion|mass curse|chain lightning|flamestrike|mana vampire|meteor swarm|earthquake|mass dispel|paralyze field").split("|"));d_=[("recall","Recall (spell)"),("gate","Gate Travel (spell)"),("charge","Recall (a book charge)"),("recall_scroll","Recall scroll"),("gate_scroll","Gate Travel scroll"),("sacred","Sacred Journey (spell)")];d0={"recall":"Recall","gate":"Gate","charge":"Recall (charge)","recall_scroll":"Recall scroll","gate_scroll":"Gate scroll","sacred":"Sacred Journey"};a_={"recall_scroll":8012,"gate_scroll":8032};cq={"charge":8901,"recall_scroll":8012,"gate_scroll":8032};cr={"recall":"Recall","gate":"Gate Travel","sacred":"Sacred Journey"};aw="bag";cs="ActionBar_alive";ct="grimoire";d1="Grimoire_cmd";d2="VirtueAssistant_cmd";cu="ActionBar_cells";cv="ActionBar_pages";cw="ActionBar_extra";a0=4;aI=a0*u;cx,cy=240,46;bx=[("paperdoll","Paperdoll",7939,"paperdoll"),("status","Status",3852,"ga:OpenStatusBar"),("journal","Journal",4080,"ga:OpenJournal:ResizableJournal"),("skills","Skills",5091,"ga:OpenSkills"),("spellbook","Grimoire",3834,"grimoire"),("worldmap","World map",5355,"ga:OpenWorldMap"),("minimap","Mini map",5365,"ga:OpenMiniMap"),("quests","Quest log",3636,"quests"),("guild","Guild",7030,"ga:OpenGuildGump"),("party","Party",7956,"macro:PartyManifest"),("chat","Chat",3639,"ga:OpenChat"),("options","Options",7864,"ga:OpenSettings"),("help","Help",4079,"help"),("war","War / peace",5119,"war"),("barsettings","Bar settings",4031,"barsettings"),("virtue","Virtue Assistant",4179,"virtue"),("launcher","Launcher",3630,"launcher"),("lock","Lock / unlock bar",4111,"lock"),("minimize","Minimize bar",0,"minimize"),];cz=(3834,8787,8786,9100,9120,11600,11677);d3={"paperdoll":"Open your paperdoll","status":"Open the status bar","journal":"Open the journal","skills":"Open the skills window","worldmap":"Open TazUO's World Map","minimap":"Open the mini map","quests":"Open the quest log","guild":"Open the guild window","party":"Open the party window","chat":"Open the chat window","options":"Open the client's options","help":"Open the help menu","war":"Switch war and peace mode","barsettings":"Open the Action Bar settings page","lock":"Lock or unlock the bar","minimize":"Minimize the bar","launcher":"Open the Quick Launcher"};bz="paperdoll status skills spellbook guild chat minimap worldmap options barsettings virtue".split();d4=["paperdoll","status","journal","skills","spellbook","worldmap","minimap","quests","options","barsettings","virtue"];a1=16;K=2;d5=("Anatomy|Animal Lore|Animal Taming|Arms Lore|Begging|Cartography|Detect Hidden|Discordance|Evaluate Intelligence|Forensic Evaluation|Hiding|Inscription|Item Identification|Meditation|Peacemaking|Poisoning|Provocation|Remove Trap|Spirit Speak|Stealing|Stealth|Taste Identification|Tracking").split("|");d6=["Magery","Necromancy","Chivalry","Bushido","Ninjitsu","Spellweaving","Mysticism"];a2=16;bA=4;a3=20;a4=[("","Empty"),("item","Item + counter"),("spell","Spell"),("skill","Skill"),("macro","TazUO macro"),("ability","Weapon ability"),("script","Legion script"),("dress","Dress outfit"),("undress","Undress outfit"),("say","Say text"),("ui","Client window"),("travel","Travel (runebook)")];bB=("rb","ri","rm");cA=[("","None"),("self","Self"),("last","Last target")];a5=["Bags' slots","Bags I pick","Backpack + sub-bags"];cB=((2240,"|".join(f6 for f6,f7 in Kit.MAGERY)),(20480,"Animate Dead|Blood Oath|Corpse Skin|Curse Weapon|Evil Omen|Horrific Beast|Lich Form|Mind Rot|Pain Spike|Poison Strike|Strangle|Summon Familiar|Vampiric Embrace|Vengeful Spirit|Wither|Wraith Form|Exorcism"),(20736,"Cleanse by Fire|Close Wounds|Consecrate Weapon|Dispel Evil|Divine Fury|Enemy of One|Holy Light|Noble Sacrifice|Remove Curse|Sacred Journey"),(21536,"Honorable Execution|Confidence|Evasion|Counter Attack|Lightning Strike|Momentum Strike"),(21280,"Focus Attack|Death Strike|Animal Form|Ki Attack|Surprise Attack|Backstab|Shadowjump|Mirror Image"),(23000,"Arcane Circle|Gift of Renewal|Immolating Weapon|Attune Weapon|Thunderstorm|Nature's Fury|Summon Fey|Summon Fiend|Reaper Form|Wildfire|Essence of Wind|Dryad Allure|Ethereal Voyage|Word of Death|Gift of Life|Arcane Empowerment"),(24000,"Nether Bolt|Healing Stone|Purge Magic|Enchant|Sleep|Eagle Strike|Animated Weapon|Stone Form|Spell Trigger|Mass Sleep|Cleansing Winds|Bombard|Spell Plague|Hail Storm|Nether Cyclone|Rising Colossus"),);d7=["Click a cell to use it; right-click it (Shift+click when right-clicks don't reach the bar) to choose what it holds: an item (counted in your pack), spell, skill, weapon ability, TazUO macro, Legion script, outfit, text to say, window or runebook destination, plus its hotkey and target.","Click an empty cell to target an item for it.","The 12 bottom-left cells have 12 pages, each with its own cells and hotkeys: the tiny arrows and the number switch pages.","Keys (far right) starts keybind mode: hover a cell, window button or bag slot and press a key; Esc ends it, Backspace clears a key. Lock locks the bar (with zones, toggles Arrange mode); Grid shows the snap grid.","Drag the bar by its stone edge; drop it near a corner, edge middle or the centre to anchor it there (upright on the left or right edge).","Bag slots show the bags of Inventory > Bags: click to show the Bags window, again to fold it into the bar; right-click for its settings. With Bags I pick, click an empty slot to target a bag.","The Grimoire and Virtue Assistant buttons show their window (turning Grimoire on); click again to fold it into the bar.","A Module windows button (page 2 of the Client window list) turns that module on and shows its window; click again to fold it into the tray beside the bar. The bar's numbered button hides or shows the tray.","A Travel (runebook) cell goes to a runebook destination by Recall, Gate Travel, a book charge, a scroll or Sacred Journey, through Grimoire (must be on); its counter shows charges or scrolls.","A used skill or spell darkens the cells of that kind while they count down; a spell cell greys out while a reagent it needs is at 0. Red at: when an item's counter turns red.","Radial ring: hold its key to show one page's cells round the mouse, point at one and let go to use it; the middle or outside uses nothing."];b={"slot":44,"top":True,"keys":True,"lock":False,"short":True,"hue":False,"bagmode":0,"bags":"","page":0,"scale":100,"tray_open":True,"bagkeys":"","extra":0,"anchor":"","vertical":False,"radial":"","radial_page":0};f4=dict(b);B={"a":[],"u":[],"x":[],"pages":[]}
	def cC():return{"shutting":False,"queue":[],"want_target":None,"next_count":0.,"next_scan":0.,"rebuild_at":0.,"bag_sig":None,"ability_sig":None,"bind":None,"jobs":[],"redraw":set(),"ub_job":False,"cool":{"skill":0.,"spell":0.},"cool_next":0.}
	a={"minimized":False,"shutting":False,"docked":False,"queue":[],"em":False,"ub_pending":False,"cnt":{},"cnt_g":{},"first":{},"first_g":{},"bags":[None]*I,"ub_found":None,"ub_cache":None,"ub_state":None,"grim_state":None,"va_state":None,"pending_on":None,"right_ok":None,"dock_sig":None,"watch_next":0.,"script_check":None,"ub_last":None};a.update(cC());e={"g":None,"c":{},"store":({},{}),"cells":{},"bags":{}};aj,z,l=Kit.basics(a,aH);U={"g":None,"at":None};j={"g":None,"ref":None,"level":"cats","cat":None,"page":0,"c":{},"bag":None,"items":[],"anchor":None,"moved":None,"placed":None};J={"sel":P-H,"dds":[]};bC=dict((gb.lower(),f8+ga)for f8,f9 in cB for ga,gb in enumerate(f9.split("|")))
	def W(fn):a["jobs"].append(fn)
	def cD(name):
		n=(name or "").strip().lower()
		if not n:return 0
		a=bC.get(n)
		if a is None:a=next((d for c,d in bC.items()if c.startswith(n)),None)
		return a if a and Kit.pic_size(a)[0]>0 else 0
	def d8(f):
		d=[str(g)for g in(API.CurrentAbilityNames()or[])];i=1 if f=="secondary"else 0
		if len(d)<=i:return 0,""
		a=d[i];b=[str(h)for h in(API.KnownAbilityNames()or[])]
		if a not in b:return 0,a
		c=b.index(a)
		if b and b[0].lower()in("none","invalid"):c-=1
		e=20992+c;return(e if c>=0 and Kit.pic_size(e)[0]>0 else 0),a
	def aJ(uid):
		if uid.startswith("mod:"):return cE(uid[4:])
		return next((c for c in bx if c[0]==uid),None)
	def cE(key,a=None):
		s=HOST.by_key.get(key)
		if s is None or key==r:return
		d=(a if a is not None else dict(HOST.docks)).get(key);b=int(d.get("icon")or 0)if d else 0;return("mod:"+key,s.title,b,"mod:"+key)
	def cF():
		b=[];c=dict(HOST.docks)
		for a in HOST.slots:
			e=[g[4][0]if len(g)>4 and g[4]else "%s.%s"%(a.key,g[0])for g in a.parts]
			for f in e or[a.key]:
				d=cE(f,c)
				if d is not None:b.append(d)
		return b
	def cG():return bx+cF()
	def d9(key):
		s=HOST.by_key.get(key)
		if s is None:return "Module '%s' (not loaded)"%key
		d=dict(HOST.docks).get(key)
		if not s.running:return "Turn %s on"%s.title
		if d is None:return "Turn %s off"%s.title
		if safe(d.get("state"))=="open":return "Fold %s into the bar"%s.title
		return "Show %s"%s.title
	def ea(key):
		s=HOST.by_key.get(key)
		if s is None:l("no module '%s'."%key,Kit.HUE_BAD);return False
		d=dict(HOST.docks).get(key)
		if not s.running:
			cc(key)
			def a(k=key,title=s.title):
				br(k)
				if not HOST.by_key[k].running:l("%s couldn't be turned on."%title,Kit.HUE_BAD)
			W(a);return True
		if d is None:HOST.disable(key);return True
		if safe(d.get("state"))=="open":cd(key,s.title)
		else:safe(d.get("show"));cc(key)
		return True
	def ak(k):k=_norm_key(k);return HOST.hotkeys_owned.get(k)or("the radial ring"if k and k==bD()else None)
	def bD():return _norm_key(b["radial"])
	def cH():return set(_norm_key(d["k"])for f,d in al()if d["k"]and d["t"])|set(c for c in X()if c)
	def ax(text,width):return Kit.fit(str(text),width,".")
	def eb(k):return(k.upper().replace("CTRL+","C").replace("SHIFT+","S").replace("ALT+","A").replace("NUMPAD","N").replace("KP_","N").replace("MINUS","-").replace("EQUALS","="))
	def cI(n):
		if b["short"]:
			if n>=10000:return "%dk"%(n//1000)
			if n>=1000:return "%.1fk"%(n/1000.)
		return str(n)
	def ec(text):
		t=(text or "").strip()
		if not t:return
		a,b=[c.strip()for c in(t.split(",",1)+[""])[:2]]
		try:return(int(a,16)if a.lower().startswith("0x")else int(a),(int(b,16)if b.lower().startswith("0x")else int(b))if b else 0)
		except Exception:return
	def V():return{"t":"","v":"","g":0,"h":0,"tg":"","k":"","lo":cm,"n":""}
	def A(ref):
		if ref[0]!="p":return B[ref[0]][ref[1]]
		a,i=divmod(ref[1],H);return B["a"][u+i]if a==b["page"]else B["pages"][a][i]
	def X():a=[_norm_key(c)for c in b["bagkeys"].split(",")];return(a+[""]*I)[:I]
	def bE(ref,k):
		if ref==au:b["radial"]=_norm_key(k);Q();ab(r)
		elif ref[0]=="b":a=X();a[ref[1]]=k;b["bagkeys"]=",".join(a);Q()
		else:A(ref)["k"]=k;aN()
	def M(ref):
		a,i=ref
		if a=="b":return "bag slot %d"%(i+1)
		if a=="r":return "the radial ring"
		if a=="p":return "page %d cell %d"%(i//H+1,i%H+1)
		if a=="u":return "button %d"%(i+1)
		if a=="x":return "row %d cell %d"%(i//u+2,i%u+1)
		if i<u:return "top cell %d"%(i+1)
		return "page %d cell %d"%(b["page"]+1,i-u+1)
	def aK(idx):
		if idx<P:return("a",idx)
		if idx<P+D:return("u",idx-P)
		return("x",idx-P-D)
	def ed(ref):
		if ref[0]=="a":return ref[1]
		if ref[0]=="u":return P+ref[1]
		return P+D+ref[1]
	def ee():return(["Top %d"%(c+1)for c in range(u)]+["Bottom %d"%(d+1)for d in range(H)]+["Button %d"%(f+1)for f in range(D)]+["Row %d-%d"%(g//u+2,g%u+1)for g in range(aI)])
	def a6(ref):
		a,i=ref
		if a=="x":return i<b["extra"]*u
		if a=="a":return b["top"]or i>=u
		return True
	def al():return[((d,f),g)for d in "aux"for f,g in enumerate(B[d])]
	def ef():
		a=[V()for g in range(P)];c=[(3617,"Bandages","self"),(3852,"Heal potion",""),(3847,"Cure potion",""),(3851,"Refresh potion","")]
		for i,(d,n,e)in enumerate(c):a[u+i].update({"t":"item","g":d,"n":n,"tg":e})
		b=[V()for h in range(D)]
		for i,f in enumerate(bz[:D]):b[i].update({"t":"ui","v":f})
		return a,b
	def Y(c):
		t,v=c["t"],c["v"]
		if t=="item":return c["n"]or("0x%04X"%c["g"])
		if t=="ui":d=aJ(v);return d[1]if d else v
		if t=="ability":return "Secondary"if v=="secondary"else "Primary"
		if t=="script":return v.replace("\\","/").split("/")[-1].rsplit(".",1)[0]
		return v
	def aL(c):return "%s to %s%s"%(d0.get(c.get("rm"),"Travel"),c["v"]or "?",(" (%s)"%c["n"])if c["n"]else "")
	def aM(ref):
		c=A(ref);t=c["t"]
		if not t:
			if ref[0]in("a","x"):return "Empty: click to target an item; right-click for a spell, skill or more"
			return "Empty: right-click to choose what it does"
		if t=="travel":
			b=aL(c)
			if HOST.services.get("grimoire.travel")is None:b="Grimoire is off: turn it on to use this cell\n"+b
			if c["k"]:b+="  [%s]"%c["k"]
			return b+"\nRight-click to change"
		d=Y(c)
		if t=="ui"and c["v"]=="spellbook":d={"open":"Fold Grimoire into the bar","minimized":"Show Grimoire","docked":"Show Grimoire"}.get(a["grim_state"],"Open Grimoire (turns it on)")
		elif t=="ui"and c["v"]=="virtue":d={"open":"Fold Virtue Assistant into the bar","gear":"Open the Virtue Assistant window","docked":"Open the Virtue Assistant window"}.get(a["va_state"],"Virtue Assistant (not running)")
		elif t=="script":d=c["v"].replace("\\","/").split("/")[-1]or "?"
		elif t=="ui"and c["v"].startswith("mod:"):d=d9(c["v"][4:])
		elif t=="ui":d=d3.get(c["v"],d)
		b={"item":"Use %s","spell":"Cast %s","skill":"Use %s","macro":"Run macro %s","ability":"Use the %s ability","script":"%s: start or stop","dress":"Dress %s","undress":"Undress %s","say":"Say \"%s\"","ui":"%s"}.get(t,"%s")%d
		if c["tg"]:b+=", then target %s"%("yourself"if c["tg"]=="self"else "last target")
		if c["k"]:b+="  [%s]"%c["k"]
		if t=="spell":
			e=cX(c["v"])
			if e is not None:b+="\nOut of %s"%e[1]
		return b+"\nRight-click to change"
	def eg(s):return(str(s).replace("%","%25").replace("&","%26").replace("=","%3D").replace(";","%3B").replace("|","%7C"))
	def eh(s):return(s.replace("%7C","|").replace("%3B",";").replace("%3D","=").replace("%26","&").replace("%25","%"))
	def cJ(d):return "&".join("%s=%s"%(c,eg(f))for c,f in d.items())
	def cK(s):return dict((c,eh(d))for c,d in(f.split("=",1)for f in s.split("&")if "="in f))
	def cL():
		d=cK(Kit.get_var(cj))
		for k in("top","keys","lock","short","hue","tray_open","vertical"):
			if k in d:b[k]=d[k]=="1"
		for k,c,e in(("slot",aY,aZ),("bagmode",0,len(a5)-1),("page",0,N-1),("scale",ac,ai),("extra",0,a0),("radial_page",0,N)):
			with Kit.quiet:b[k]=int(d[k])
			b[k]=max(c,min(e,b[k]))
		a=d.get("anchor","");b["anchor"]=a if a in Kit.ANCHORS else ""
		for k in("bags","bagkeys","radial"):b[k]=d.get(k,b[k])
	def Q():Kit.put_var(cj,cJ(dict((d,("1"if c else "0")if isinstance(c,bool)else c)for d,c in b.items())))
	def ei(d):
		c=V()
		for k in("t","v","tg","k","n"):c[k]=d.get(k,c[k])
		for k in("g","h","lo"):
			with Kit.quiet:c[k]=int(d.get(k,c[k]))
		if c["t"]=="travel":
			for k in bB:c[k]=d.get(k,"")
		return c
	def a7(raw,n,a=True):b=[ei(cK(c))for c in raw.split(";")if c or not a];return(b+[V()for d in range(n)])[:n]
	def cM():
		bF.clear();d,a=ef();f=Kit.get_var(cu)
		if "|"in f:
			i,j=f.split("|",1);d=a7(i,P,False);a=a7(j,D,False);k=set(p["v"]for p in a if p["t"]=="ui");g=[q for q in bz if q not in k]
			for c in a:
				if c["t"]=="ui"and aJ(c["v"])is None and not c["v"].startswith("mod:"):
					c.update(V())
					if g:c.update({"t":"ui","v":g.pop(0)})
			if[s["v"]if s["t"]=="ui"else None for s in a]==d4[:D]:
				for l,m in enumerate(bz[:D]):a[l].update({"t":"ui","v":m})
		e=[[V()for v in range(H)]for t in range(N)];h=Kit.get_var(cv)
		if h:
			for n,o in enumerate(h.split("|")[:N]):e[n]=a7(o,H)
		else:e[0]=d[u:];b["page"]=0
		d[u:]=e[b["page"]];B["x"]=a7(Kit.get_var(cw),aI);B["a"],B["u"],B["pages"]=d,a,e;bK()
	def cN():
		if B["pages"]:B["pages"][b["page"]]=list(B["a"][u:])
	bF={}
	def aN():
		cN();bK()
		def a(a):return ";".join(cJ(d)for d in a)
		for b,c in((cu,a(B["a"])+"|"+a(B["u"])),(cv,"|".join(a(f)for f in B["pages"])),(cw,a(B["x"]))):
			if bF.get(b)!=c:Kit.put_var(b,c);bF[b]=c
	def ej(p):
		p=p%N
		if p==b["page"]:return
		cN();b["page"]=p;B["a"][u:]=B["pages"][p];bK();Q();ar();a["next_count"]=0.;ao([("a",u+d)for d in range(H)]);eS();ab(r);c=j.get("ref")
		if j.get("g")is not None and c and c[0]=="a"and c[1]>=u:aq()
	def cO():
		a=[0]*I
		for i,p in enumerate(b["bags"].split(",")[:I]):
			try:a[i]=int(p,16)if p.strip()else 0
			except Exception:a[i]=0
		return a
	def cP(i,serial):a=cO();a[i]=serial;b["bags"]=",".join(("%X"%c)if c else ""for c in a);Q()
	def aO():
		if Kit.zone_up(r):return
		p=Kit.pos(e["g"])if Kit.is_open(e["g"])else None
		if p is not None and p!=a.get("pos_saved"):a["pos_saved"]=p;Kit.put_var(bu,"%d,%d"%p)
	class ClientUI(object):
		looked=False;error="";world=None;GA=None;UIM=None;_methods={};_get=staticmethod(Typing._get)
		@staticmethod
		def _method(t,name,b,static):
			a=(t,name,tuple(b),static)
			if a not in ClientUI._methods:ClientUI._methods[a]=ClientUI._find_method(t,name,b,static)
			return ClientUI._methods[a]
		@staticmethod
		def _find_method(t,name,a,static):
			for m in t.GetMethods(Client.flags(static)):
				if m.Name!=name or m.IsGenericMethodDefinition:continue
				b=m.GetParameters()
				if len(b)<len(a):continue
				if any(c is not None and b[d].ParameterType.Name!=c for d,c in enumerate(a)):continue
				if all(f.IsOptional for f in b[len(a):]):return m
			return
		@staticmethod
		def _invoke(m,target,a):import System;b=m.GetParameters();c=list(a)+[d.DefaultValue for d in b[len(a):]];return m.Invoke(target,System.Array[object](c))
		@staticmethod
		def find():
			if ClientUI.looked:return
			ClientUI.looked=True;a=ClientUI.world=safe(lambda:ClientUI._get(API,"World"));ClientUI.GA=aW("ClassicUO.Game.GameActions");ClientUI.UIM=aW("ClassicUO.Game.Managers.UIManager")
			if a is None:ClientUI.error="client World not found"
			elif ClientUI.GA is None:ClientUI.error="GameActions not found"
		@staticmethod
		def on_main(fn):
			a,d=Client.on_main_ex(fn)
			if a=="ok":return d
			if a=="err":b=Client.exc;c=getattr(b,"InnerException",None)or getattr(getattr(b,"clsException",None),"InnerException",None);ClientUI.error=str(c)if c else Client.error
			else:ClientUI.error=Client.error or "can't run on the client thread"
			return
		@staticmethod
		def _bring_to_front(c):
			b=(ClientUI._get(None,"Gumps",ClientUI.UIM)if ClientUI.UIM is not None else None);a=b.First if b is not None else None
			while a is not None:
				g=a.Value
				if g is not None and g.GetType().Name==c and not g.IsDisposed:
					m=ClientUI._method(g.GetType(),"BringOnTop",[],False)
					if m is not None:m.Invoke(g,None)
					return True
				a=a.Next
			return False
		@staticmethod
		def game_action(name,extra=(),reuse=None):
			ClientUI.find()
			if ClientUI.world is None or ClientUI.GA is None:return False
			a=ClientUI.world
			def b():
				if reuse and ClientUI._bring_to_front(reuse):return True
				m=ClientUI._method(ClientUI.GA,name,["World"]+[None]*len(extra),True)
				if m is None:raise Exception("GameActions.%s not found"%name)
				ClientUI._invoke(m,None,[a]+list(extra));return True
			return bool(ClientUI.on_main(b))
		@staticmethod
		def open_macro(b):
			ClientUI.find();a=ClientUI.world
			if a is None:return False
			def c():import System;c=ClientUI._get(a,"Macros");d,e,f=[c.GetType().Assembly.GetType("ClassicUO."+h)for h in("Game.Managers.MacroObject","Common.Enums.MacroType","Common.Enums.MacroSubType")];g=System.Activator.CreateInstance(d,System.Array[object]([System.Enum.Parse(e,"Open",True),System.Enum.Parse(f,b,True)]));ClientUI._run_macro_object(c,g);return True
			return bool(ClientUI.on_main(c))
		@staticmethod
		def macro_names():
			ClientUI.find();a=ClientUI.world
			if a is None:return[]
			def b():b=ClientUI._get(a,"Macros");m=ClientUI._method(b.GetType(),"GetAllMacros",[],False);c=[str(ClientUI._get(d,"Name")or "")for d in(m.Invoke(b,None)or[])];return[f for f in c if f]
			return list(ClientUI.on_main(b)or[])
		@staticmethod
		def _run_macro_object(mgr,mo):t=mgr.GetType();ClientUI._invoke(ClientUI._method(t,"SetMacroToExecute",["MacroObject"],False),mgr,[mo]);ClientUI._invoke(ClientUI._method(t,"Update",[],False),mgr,[])
		@staticmethod
		def run_macro(name):
			ClientUI.find();a=ClientUI.world
			if a is None:return False
			def b():
				b=ClientUI._get(a,"Macros");e=ClientUI._method(b.GetType(),"FindMacro",["String"],False);c=e.Invoke(b,__import__("System").Array[object]([name]))
				if c is None:return "missing"
				d=ClientUI._get(c,"Items")
				if d is None:return "empty"
				ClientUI._run_macro_object(b,d);return "ok"
			r=ClientUI.on_main(b)
			if r=="missing":return
			return r=="ok"
	def cQ():return Kit.data_path("_unified_bag_%d.cfg"%int(safe(lambda:API.Player.Serial,0)or 0))
	def cR(path):
		try:
			e=os.path.getmtime(path);b=a["ub_cache"]
			if b and b[0]==path and b[1]==e:return list(b[2])
			with open(path,"r")as h:i=h.read().splitlines()
		except Exception:return
		d,c=0,{}
		for f in i:
			if "="not in f:continue
			k,v=f.split("=",1);k,v=k.strip(),v.strip()
			with Kit.quiet:
				if k=="slots":d=int(v)
				elif k.startswith("slot."):c[int(k[5:])]=int(v)
		g=[c[m]for m in sorted(c)if(d<=0 or m<d)and c[m]>0];a["ub_cache"]=(path,e,g);return list(g)
	def ek():
		if not aF():a["ub_last"],a["ub_pending"]=cR(cQ()),False
		elif not a["ub_job"]:
			a["ub_job"]=True;b=cQ()
			def c():
				a["ub_job"]=False;c=cR(b)
				if c!=a["ub_last"]or a["ub_pending"]:a["ub_last"],a["ub_pending"]=c,False;a["next_scan"]=0.
			W(c)
		return None if a["ub_last"]is None else list(a["ub_last"])
	def bG(a,b):s=API.GetSharedVar(a);return str(s)if s is not None and str(s)in b else None
	def ay():return bG("UnifiedBag_state",("open","collapsed","docked"))
	def a8():return bG("Grimoire_state",("open","minimized","docked"))
	def bH():return bG("VirtueAssistant_state",("open","gear","docked"))
	def bI(cmd):API.SetSharedVar("UnifiedBag_cmd",cmd)
	def bJ():return list(HOST.docks)
	def a9():return[(f,c)for f,c in bJ()if c.get("always")or safe(c.get("state"))=="docked"]
	def cS():return tuple([(c,safe(f.get("state")))for c,f in bJ()])
	def cT():return tuple([(f,c.get("icon"),safe(c.get("state"))if c.get("always")else None)for f,c in a9()])
	def Z(on=True):
		if on and not a["em"]:API.SetSharedVar(cs,time.time())
		else:API.RemoveSharedVar(cs)
	def el():
		f=time.time()
		if f<a["watch_next"]:return
		a["watch_next"]=f+.25;c=False
		for k,s,i in(("ub_state",ay(),b["bagmode"]==0),("grim_state",a8(),True),("va_state",bH(),True)):
			if s!=a[k]:a[k]=s;c=c or i
		if c:db()
		d=cS()
		if d!=a["dock_sig"]:
			j=set(o for o,q in(a["dock_sig"]or()));a["dock_sig"]=d;g=cT()
			if g!=a.get("tray_sig"):a["tray_sig"]=g;dc()
			h=[v for v,t in al()if t["t"]=="ui"and t["v"].startswith("mod:")]
			if h:
				if set(w for w,x in d)!=j:ao(h)
				else:db()
		e=frozenset(HOST.hotkeys_owned)
		if e!=a.get("owned_sig"):
			m=e^(a.get("owned_sig")or frozenset());a["owned_sig"]=e
			if m&cH():ar()
		p=a["pending_on"]
		if p and time.time()>p[2]:
			a["pending_on"]=None;n=ay()if p[0]==aw else a8()
			if n is None:
				l("%s didn't start; is Virtue Assistant running?"%p[1],Kit.HUE_BAD)
				if p[3]is not None:p[3]()
	def ba(key,title,fallback=None):
		if key in HOST.by_key:W(lambda:br(key))
		else:API.SetSharedVar("VirtueAssistant_enable",key)
		l("turning %s on."%title);a["pending_on"]=(key,title,time.time()+4.,fallback)
	def em():
		a=a8();Z()
		if a in("minimized","docked","open"):API.SetSharedVar(d1,"dock"if a=="open"else "show")
		else:ba(ct,"Grimoire",e2)
		return True
	def en():
		a=bH();Z()
		if a not in("open","gear","docked"):l("Virtue Assistant isn't running.",Kit.HUE_BAD);return False
		HOST.pressed_at=time.time();API.SetSharedVar(d2,"dock"if a=="open"else "show");return True
	def cU():
		a=[];b=int(API.Backpack or 0)
		if b:a.append(b)
		for c in(API.ItemsInContainer(b,False)or[]):
			if len(a)>=I:break
			with Kit.quiet:
				if c.IsContainer:a.append(int(c.Serial))
		return a
	def cV():
		h=b["bagmode"]
		if h==0:
			c=ek()
			if c is None and a["ub_pending"]:c=[]
			else:
				a["ub_found"]=c is not None
				if c is None:c=cU()
		elif h==1:c=cO()
		else:c=cU()
		d,g=[],[]
		for s in(list(c)+[0]*I)[:I]:
			if not s:d.append(None);g.append(None);continue
			e=Kit.find_item(s);g.append(e)
			if e is None:d.append({"s":s,"g":0,"h":0,"n":"Bag (not loaded yet)"});continue
			try:i,j=int(e.Graphic or 0),int(e.Hue or 0)
			except Exception:i=j=0
			d.append({"s":s,"g":i,"h":j,"n":None})
		k=tuple((m["s"],m["g"],m["h"])if m else None for m in d)
		if k!=a["bag_sig"]:
			for f,e in zip(d,g):
				if f is not None and f["n"]is None:
					try:f["n"]=str(e.Name or "")or "Bag"
					except Exception:f["n"]="Bag"
			a["bags"],a["bag_sig"]=d,k;ao([("b",n)for n in range(I)])
	def az(i):return a["bags"][i]if i<len(a["bags"])else None
	am={"types":None}
	def bK():am["types"]=None
	def aP():
		if am["types"]is None:
			b=B["a"]+B["u"]+B["x"];am["types"]=set(g["t"]for g in b);am["items"]=set(h["g"]for h in b if h["t"]=="item");d,e=set(),set();a={"skill":[],"spell":[]}
			for f,c in al():
				if c["t"]=="spell":d.update(i[1]for i in cW(c["v"]));a["spell"].append(f)
				elif c["t"]=="skill":a["skill"].append(f)
				elif c["t"]=="travel"and c.get("rm")in a_:e.add(a_[c["rm"]])
			am["extra"],am["refs"]=frozenset(d|e),a
		return am
	def eo():
		if "ability"not in aP()["types"]:return
		b=tuple([str(d)for d in(API.CurrentAbilityNames()or[])])
		if b!=a["ability_sig"]:a["ability_sig"]=b;ao([f for f,g in al()if g["t"]=="ability"])
	def aQ(extra=(),max_age=0.):
		o=ch()
		try:p=HOST.pack_items(deep=True,max_age=max_age);q=int(API.Backpack or 0)
		except Exception:return
		k=aP();d=k["items"]
		if extra or k["extra"]:d=d|k["extra"]|set(extra)
		e,f,g,h,j,l={},{},{},{},{},{};r,s=e.get,f.get
		for b in p:
			try:
				c=int(b.Graphic)
				if c not in d:continue
				t,m=int(b.Hue),int(b.Serial);n=max(1,int(b.Amount or 0));u,v=(j,l)if int(b.Container)==q else(g,h)
			except Exception:continue
			i=(c,t);e[i]=r(i,0)+n;f[c]=s(c,0)+n;u.setdefault(i,m);v.setdefault(c,m)
		g.update(j);h.update(l);a.update({"cnt":e,"cnt_g":f,"first":g,"first_g":h,"counted":d,"counted_at":time.time(),"pack_v":o})
	def bL(info,lbl,text,hue):
		if info.get("txt")!=text:
			info["txt"]=text
			try:lbl.Text=text;Kit.ui_pos(lbl,info["x"]+info["w"]-Kit.text_px(text)-3,info["y"]+info["h"]-16)
			except Exception:pass
		if info.get("hue")!=hue:info["hue"]=hue;Kit.set(lbl,"Hue",hue)
	def ep():
		if a["em"]:return
		k=aP()
		if "item"in k["types"]or k["extra"]:aQ(max_age=.5)
		else:a["pack_v"]=None
		aS()
	aR=[None]
	def aS():
		l=time.time();r=a["cool"];m=False;i=aR[0]
		if i is None:i=[(x,w,w["count"])for x,w in e["cells"].items()if w.get("count")is not None];aR[0]=i
		for p,g,j in i:
			c=A(p);t,v=c["t"],c["v"];d,f="",Kit.HUE_TEXT;h=r.get(t)
			if h and l<h:d,f=cY(h-l),Kit.HUE_TITLE
			elif t=="item":n=a["cnt"].get((c["g"],c["h"]),0)if b["hue"]else a["cnt_g"].get(c["g"],0);d=cI(n);f=Kit.HUE_BAD if n<=max(0,c["lo"])else Kit.HUE_TEXT
			elif t in("spell","ability","script"):
				try:
					if t=="spell":k=bool(API.IsSpellActive(v))
					elif t=="ability":k=bool(API.SecondaryAbilityActive()if v=="secondary"else API.PrimaryAbilityActive())
					else:k=bn(v)
				except Exception:k=False
				d,f=("ON"if k else ""),Kit.HUE_GOOD
			elif t=="travel":
				if m is False:m=er()
				d,f=es(c,m)
			if t=="spell":
				o=cX(v);eq(p,g,o is not None)
				if o is not None and not(h and l<h):d,f=o[0],Kit.HUE_BAD
			bL(g,j,d,f)
		for s,g in list(e["bags"].items()):
			j=g.get("count");q=az(s)
			if j is None or not q:continue
			try:n=int(API.Contents(q["s"])or 0)
			except Exception:n=0
			bL(g,j,str(n),Kit.HUE_TEXT)
	bb={}
	def cW(name):
		a=bb.get(name)
		if a is None:
			c=Kit.spell_info(name);b=Kit.REAGENTS;a=tuple((d,b[d][1],b[d][0])for d in(c[1]if c else())if d in b)
			if len(bb)>200:bb.clear()
			bb[name]=a
		return a
	def cX(name):
		b,c=a["cnt_g"],a.get("counted")or()
		for d,g,n in cW(name):
			if b.get(g,0)<=0 and g in c:return(d,n)
		return
	def eq(ref,info,grey):
		if info.get("grey",False)==grey:return
		info["grey"]=grey;a=info.get("icon")
		if a is not None:a.SetAlpha(.35 if grey else 1.)
		bi(info,aM(ref))
	def er():
		a=HOST.services.get("grimoire.book_charges")
		if a is not None:return safe(a)
		a=HOST.services.get("grimoire.destinations")
		if a is None:return
		try:return dict((c["book"],c["charges"])for c in a()or())
		except Exception:return
	def es(c,charges):
		if charges is None:return "off",Kit.HUE_INFO
		m=c.get("rm");b=max(0,c["lo"])
		if m in a_:n=a["cnt_g"].get(a_[m],0);return cI(n),Kit.HUE_BAD if n<=b else Kit.HUE_TEXT
		try:n=charges.get(int(c.get("rb")or "0",16))
		except ValueError:n=None
		if n is None:return "",Kit.HUE_TEXT
		if m=="charge":return str(n),Kit.HUE_BAD if n<=b else Kit.HUE_TEXT
		return str(n),Kit.HUE_INFO
	def et(c):
		a=HOST.services.get("grimoire.travel")
		if a is None:l("Grimoire is off; turn it on to use Travel cells.",Kit.HUE_BAD);return False
		try:b,d=int(c.get("rb")or "",16),int(c.get("ri")or "")
		except ValueError:l("this Travel cell has no destination; right-click it to pick one.",Kit.HUE_BAD);return False
		return bool(a(b,d,c.get("rm")or "recall",c["v"]or None))
	def eu(ref,d,method):a=A(ref);b=dict(V(),t="travel",v=str(d["name"]),n=str(d["book_name"]),k=a["k"],tg="",lo=a["lo"]if a["t"]=="travel"else 2,rb="%X"%int(d["book"]),ri=str(int(d["index"])),rm=method);B[ref[0]][ref[1]]=b;an(recount=True,refs=[ref]);l("%s set on %s."%(aL(b),M(ref)),Kit.HUE_GOOD)
	ev={"arms lore":3.,"item identification":3.,"detect hidden":3.}
	def cY(a):return("%d"%int(math.ceil(a)))if a>=3. else("%.1f"%max(0.,a))
	def ew(t,v):
		if t=="skill":b=ev.get(str(v).strip().lower(),10.)
		else:c=Kit.spell_info(v);b=c[3]if c else 0.
		if b and b>0:a["cool"][t]=time.time()+b;a["cool_next"]=0.
	def ex(now):
		c=a["cool"]
		if not(c["skill"]or c["spell"])or now<a["cool_next"]:return
		a["cool_next"]=now+.1;k=aP()["refs"];i=False
		for f in("skill","spell"):
			g=c[f]
			if not g:continue
			d=now>=g
			if d:c[f]=0.;i=True
			l=""if d else cY(g-now)
			for m in k[f]:
				b=e["cells"].get(m)
				if b is None:continue
				h=not d
				if b.get("dark",False)!=h:b["dark"]=h;b["catcher"].SetAlpha(.55 if h else.01)
				j=b.get("count")
				if j is not None and not d:bL(b,j,l,Kit.HUE_TITLE)
		if i:aS()
	def ey(ref):
		c=A(ref)
		if c["t"]=="travel":return aL(c)
		a=aM(ref).split("\n")[0];return a.replace("  [%s]"%c["k"],"")if c["k"]else a
	def ez():
		a=[(_norm_key(f["k"]),"%s: %s"%(M(d),ey(d)))for d,f in al()if _norm_key(f["k"])and f["t"]and a6(d)];a+=[(c,"bag slot %d"%(g+1))for g,c in enumerate(X())if c];a=[(h,i+((" (left to %s)"%ak(h))if ak(h)else ""))for h,i in a];b=bD()
		if b:a.append((b,"radial ring"+((" (left to %s)"%HOST.hotkeys_owned[b])if b in HOST.hotkeys_owned else "")))
		return a
	eA=Kit.disposer(r,a,e)
	def ag(delay=0.):a["rebuild_at"]=time.time()+delay
	def an(recount=False,refresh=True,refs=None):
		aN();ar()
		if recount:a["next_count"]=0.
		if refs is None:ag()
		else:ao(refs)
		if refresh:ab(r)
	def cZ(ref):B[ref[0]][ref[1]]=V();an(refs=[ref])
	C={"scale":None,"vertical":None,"slot":None,"off":(0,0),"sig":None}
	def bc():
		v=C["scale"]
		if v is not None:return v
		k=Kit.tscale*(.85 if Kit.compact else 1.);s=int(b["scale"]);return s if k==1. else max(ac,min(ai,int(round(s*k))))
	def aA():v=C["vertical"];return bool(b["vertical"])if v is None else v
	def bM():return C["slot"]if C["scale"]is not None else None
	def c_():return(b["slot"],b["top"],b["extra"])
	def bN(b,c):
		f=C["scale"]
		try:
			C["scale"]=100;d=aB();a=max(ac,min(ai,int(min(b*100./max(1.,d["W"]),c*100./max(1.,d["H"])))))
			def e(p):C["scale"]=p;a=aB();return a["W"]<=b and a["H"]<=c
			for g in range(8):
				if a<=ac or e(a):break
				a-=1
			for g in range(8):
				if a>=ai or not e(a+1):break
				a+=1
			return a
		finally:C["scale"]=f
	def c0():
		a=HOST.layout_base(r)
		if not b["extra"]or a is None:cg(r);return
		c=a[1]>a[0];f,g=(a[1],a[0])if c else a;d,h,i=b["extra"],C["scale"],O.get("vtmp");O["vtmp"]=c
		try:b["extra"]=0;p=bN(int(f),int(g));b["extra"]=d;C["scale"]=p;e=aB()["H"]
		finally:b["extra"]=d;C["scale"]=h;O["vtmp"]=i
		cg(r,e if c else None,None if c else e)
	def c1(w,h,mode):
		if w is None or h is None or not w or not h:c=(None,None);d=e=None
		else:
			d=(int(w),int(h));b=h>w;f,g=(h,w)if b else(w,h);e=c_();c0();O["vtmp"]=b
			try:c=(bN(int(f),int(g)),b)
			finally:O["vtmp"]=None
		i=(bc(),aA(),C["slot"]);C["scale"],C["vertical"]=c;C["slot"],C["sig"]=d,e
		if(bc(),aA(),C["slot"])!=i and not a["shutting"]:ag()
	def eB():
		a=bM();b=c_()
		if a is None or b==C["sig"]:return
		c,d=(a[1],a[0])if C["vertical"]else a;C["scale"]=bN(c,d);C["sig"]=b;c0()
	def eC():
		if e["g"]is None or a["shutting"]:return
		return "minimized"if a["em"]else "open"
	def eD():
		c,d=C["scale"],O["vtmp"];a=[]
		try:
			C["scale"]=ac
			for v in(False,True):O["vtmp"]=v;b=aB();a.append((b["H"],b["W"])if v else(b["W"],b["H"]))
		finally:C["scale"],O["vtmp"]=c,d
		return min(a[0][0],a[1][0]),min(a[0][1],a[1][1])
	eE={"fit":c1,"state":eC,"min":eD,"exact":True,"untitled":True}
	def S(v,lo=1):k=max(ac,min(ai,bc()))/100.;return max(lo,int(round(v*k)))
	aT={"key":None,"L":None}
	def bO():
		a=bM();c=(b["slot"],bc(),b["top"],b["extra"],a,aA())
		if aT["key"]!=c:
			if a is None:aT["L"]=aB()
			else:d,e=(a[1],a[0])if aA()else a;aT["L"]=eH(aB(),d,e)
			aT["key"]=c
		return aT["L"]
	O={"capw":None,"vtmp":None}
	def c2():
		if O["capw"]is None:O["capw"]=max(Kit.text_px(d)for d in("Keys","Lock","Grid"))+6
		return O["capw"]
	def c3(a):return(4,2,1)if a else(1,2,4)
	def eF(c,b,d):a=(4+c-1)//c;e=(b-2*K-(c-1)*K)//c;f=min(24,(d-2*K-(a-1)*K)//a);return a,e,f
	def eG(b,a):
		d=c2()
		for c in c3(a):
			e=(4+c-1)//c;f=e*a1+(e-1)*K+2*K;g=c*d+(c-1)*K+2*K
			if a and g<=b:return f
			if not a and f<=b:return g
		return(4*a1+5*K)if a else(4*d+5*K)
	def aB():f=S(max(aY,min(aZ,int(b["slot"]))),18);l,c,a=S(dJ,4),S(6,3),S(4,2);m=l;v,n,o=S(4,2),S(dL,2),S(dM,2);i,h,p=S(dI,16),S(dK,34),S(dN,18);g=f+v;e=f+2*a;j=i+u*g+a;q=H*g+a;r=p+2*a;s=j-i-q-2*c-r-c;k=int(s*ck);t=s-k;w=(k-2*a-(D-1)*n)//D;x=(t-2*a-(I-1)*o)//I;d=(2 if b["top"]else 1)+b["extra"];h=max(h,eG(d*e+(d-1)*c,aA()if O["vtmp"]is None else O["vtmp"]));return{"S":f,"pitch":g,"ph":e,"inner":j,"left_w":q,"rows":d,"ui_w":k,"bag_w":t,"bw":w,"bh":e-3*a,"tray_w":r,"tb":p,"bgw":x,"bgh":e-2*a,"m":m,"sg":c,"p4":a,"ug":n,"bg":o,"pw":i,"cw":h,"tm":l,"colx":tuple(a+y*g for y in range(u)),"colw":(f,)*u,"top_w":u*g+a,"sgx":c,"sgc":c,"rowy":tuple(G*(e+c)for G in range(d)),"rowh":(e,)*d,"celly":(a,)*d,"cellh":(f,)*d,"W":m+j+c+h+m,"H":m+d*e+(d-1)*c+m}
	def aC(total,n):
		if n<=0:return[]
		if total<=0:return[0]*n
		return[(total*(c+1))//n-(total*c)//n for c in range(n)]
	def eH(L,P,Q):
		L=dict(L);S,e,d,c=L["S"],L["p4"],L["sg"],L["rows"];o=L["pitch"]-S;n=u;p=max(0,int(S*1.6)-S);a=P-L["W"]
		if a>0:
			h=n*o+d;b=min(a,h);t=float(b)/h if h>0 else 0.;q=min(b,int(round(d*t)));i=[o+at for at in aC(b-q,n)];f=min(a-b,n*p);s=[S+by for by in aC(f,n)];j=a-b-f;v=0
			if j>0:
				if c>1:i=[dd+fn for dd,fn in zip(i,aC(j,n))]
				else:v=j
			k,x=[],e
			for w in range(n):k.append(x);x+=s[w]+i[w]
			z=d+int(round(d*t));A=L["ug"]+int(round(L["ug"]*t));B=L["bg"]+int(round(L["bg"]*t));C,R=L["pw"],L["tray_w"];l=C+x+v;E=k[H];F=l-C-E-3*z-R;m=int(F*ck);G=F-m;L.update({"colx":tuple(k),"colw":tuple(s),"top_w":x,"sgx":z,"sgc":d+q,"ug":A,"bg":B,"inner":l,"left_w":E,"ui_w":m,"bag_w":G,"bw":(m-2*e-(D-1)*A)//D,"bgw":(G-2*e-(I-1)*B)//I});L["W"]=L["m"]+l+L["sgc"]+L["cw"]+L["m"]
		a=Q-L["H"]
		if a>0:
			b=min(a,(c-1)*d);T=[d+f6 for f6 in aC(b,c-1)];f=min(a-b,c*p);g=[S+f7 for f7 in aC(f,c)];J=aC(a-b-f,c);K,M,N,y=[],[],[],0
			for r in range(c):K.append(y);O=g[r]+2*e+J[r];M.append(O);N.append(e+J[r]//2);y+=O+(T[r]if r<c-1 else 0)
			L.update({"rowy":tuple(K),"rowh":tuple(M),"celly":tuple(N),"cellh":tuple(g),"bh":g[-1]-e,"bgh":g[-1]});L["H"]=L["m"]+y+L["m"]
		return L
	def aD():return not aA()
	def bd():
		if a["em"]:return cx,cy
		L=bO();return(L["W"],L["H"])if aD()else(L["H"],L["W"])
	def R(x,y,w,h):a,b=C["off"];return(x+a,y+b,w,h)if aD()else(y+a,x+b,h,w)
	def aU(g,graphic,hue,x,y,w,h):
		try:p=G.CreateGumpItemPic(int(graphic),int(w),int(h))
		except Exception:return
		if hue:p.Hue=max(0,min(65535,int(hue)))
		p.SetPos(x,y);p.SetAcceptMouseInput(False);g.Add(p);return p
	def bP(text):t=str(text).replace("_"," ");return "".join(" "+c if d and c.isupper()and t[d-1].islower()else c for d,c in enumerate(t))
	def bQ(g,text,x,y,w,h,hue=None):
		b=max(1,min(3,(h-2)//14));a=[Kit.fit(d,w-4)for d in Kit.wrap(bP(text),w-4)]
		if len(a)>b:a=a[:b];a[-1]=Kit.fit(a[-1]+"..",w-4)if not a[-1].endswith("..")else a[-1]
		c=y+(h-14*len(a))//2-1;return[Kit.add_label(g,f,x+(w-Kit.text_w(f))//2,c+k*14,Kit.HUE_TEXT if hue is None else hue)for k,f in enumerate(a)]
	eI=dict((ge,gd)for gc,gd in dZ for ge in gc);be={}
	def ah(text,px):return int(math.ceil(sum(eI.get(c,dX)for c in text)*px*dW))
	def bf(words,px,room,most):
		b=[ah(g,px)for g in words];c=ah(" ",px);n=len(b);a={}
		def d(i,k):
			if i==n:return(0,())
			if k==0:return
			if(i,k)in a:return a[(i,k)]
			e=None;f=-c
			for j in range(i,n):
				f+=c+b[j]
				if f>room:break
				g=d(j+1,k-1)
				if g is not None and(e is None or max(f,g[0])<e[0]):e=(max(f,g[0]),(" ".join(words[i:j+1]),)+g[1])
			a[(i,k)]=e;return e
		for f in range(1,most+1):
			e=d(0,f)
			if e is not None:return list(e[1])
		return
	def eJ(word):a=[c for c in range(1,len(word))if word[c].isupper()and(word[c-1].islower()or(c+1<len(word)and word[c+1].islower()))];return[word[d:f]for d,f in zip([0]+a,a+[len(word)])]
	def c4(text,px,room,tail):
		while text and ah(text+tail,px)>room:text=text[:-1]
		return text.rstrip()+tail
	def eK(word,px,room):
		a=[""]
		for b in word:
			if a[-1]and ah(a[-1]+b,px)>room:a.append(b)
			else:a[-1]+=b
		return a
	def eL(text,w,h):
		g=max(av,Kit.tsize(dT));i=(text,w,h,g);d=be.get(i)
		if d is not None:return d
		b=bP(text).split();e=max(1,w-4)
		for c in range(g,av-1,-1):
			f=max(1,h//(c+1));a=bf(b,c,e,f)
			if a is not None:d=(c,a);break
		if d is None:
			c=av;b=[m for k in b for m in eJ(k)];a=bf(b,c,e,f)
			if a is None:
				b=[o for n in b for o in eK(n,c,e)];a=bf(b,c,e,f)
				if a is None:
					a=bf(b,c,e,len(b))or b
					if len(a)>f:a=a[:f-1]+[c4(a[f-1],c,e,"..")]
			d=(c,a)
		if len(be)>=dY:be.clear()
		be[i]=d;return d
	def c5(g,text,px,color,x,y,b=False):a=Kit.inert(G.CreateGumpTTFLabel(text,px,color,applyStroke=b));a.SetPos(x,y);g.Add(a);return a
	def bR(g,text,x,y,w,h):a,b=eL(text,w,h);c=a+1;d=y+(h-c*len(b))//2;return[c5(g,f,a,dU,x+(w-ah(f,a))//2,d+k*c)for k,f in enumerate(b)]
	def eM():return max(av,Kit.tsize(co))+3
	def c6(g,k,x,y,w):
		b=eb(k);a=max(av,Kit.tsize(co))
		while a>av and ah(b,a)>w-4:a-=1
		if ah(b,a)>w-4:b=c4(b,a,w-4,".")
		return c5(g,b,a,dV,max(x+2,x+w-2-ah(b,a)),y+1,True)
	def eN(kind,c,b):
		def d():
			if a["right_ok"]is False and Client.key_held("shift"):z.add((c,b),dup=True)
			else:z.add((kind,b),dup=True)
		return Kit.once(d,(r,kind,b),Kit.TWICE)
	def eO(b,fn):
		if b is None or a["right_ok"]is False:return False
		if Kit.hook_mouse(b,fn,event="MouseUp",button="Right"):a["right_ok"]=True;return True
		if a["right_ok"]is None:a["right_ok"]=False;l("no right-click events from this client; Shift+click a cell for its menu instead.")
		return False
	def bg(g,icon,x,y,w,h):
		a=min(w,h)-4;p=Kit.add_pic(g,icon,x+(w-a)//2,y+(h-a)//2)
		if p is not None:p.SetWidth(a);p.SetHeight(a);p.SetAcceptMouseInput(False)
		return p
	def bh(g,a,d,y,h):
		e=Kit.GOLD_V if aD()else Kit.GOLD_H
		for b,f,w in zip(a,a[1:],d):c=f-b-w;s=min(c,Kit.GOLD_T);Kit.add_tiled(g,e,*R(b+w+(c-s)//2,y,s,h))
	def bS(g,ref,x,y,w,h):
		if not A(ref)["t"]:
			Kit.add_tiled(g,ae,x,y,w,h,af*.3)
			for a,b,c,d in((x,y,w,1),(x,y+h-1,w,1),(x,y,1,h),(x+w-1,y,1,h)):Kit.add_tiled(g,ae,a,b,c,d,af)
		else:Kit.add_tiled(g,ae,x,y,w,h,af)
		c7(g,ref,x,y,w,h)
	def bT(ref,x,y,w,h,pad):
		if w==h or ref[0]=="u":return x+pad,y+pad,w-2*pad,h-2*pad
		a=min(w,h)-2*pad;return x+(w-a)//2,y+(h-a)//2,a,a
	def c7(g,ref,x,y,w,h):c=A(ref);t=c["t"];a={"x":x,"y":y,"w":w,"h":h,"count":None};d=c8(g,ref,c,a,x,y,w,h,eM()if(b["keys"]and c["k"]and t)else 0)[0];e["cells"][ref]=c9(g,a,d,t in("item","spell","ability","script","skill","travel"),c["k"]if b["keys"]and t else "",aM(ref),("click","menu",ref));aR[0]=None
	def c8(g,ref,c,info,x,y,w,h,b):
		t=c["t"];d=[];e=False;p=None
		if t=="item"and c["g"]:p=aU(g,c["g"],c["h"],*bT(ref,x,y,w,h,3))
		elif t=="spell":
			a=cD(c["v"])
			if a:p=info["icon"]=bg(g,a,x,y,w,h)
		elif t=="travel":
			m=c.get("rm")
			if m in cr:
				a=cD(cr[m])
				if a:p=bg(g,a,x,y,w,h)
			elif m in cq:p=aU(g,cq[m],0,*bT(ref,x,y,w,h,3))
			if p is not None:p.SetAlpha(.5)
			d.extend(bR(g,c["v"]or "?",x,y+b,w,h-b));e=True
		elif t=="ability":
			a,i=d8(c["v"])
			if a:p=bg(g,a,x,y,w,h)
			elif i:d.extend(bR(g,i,x,y+b,w,h-b));e=True
		elif t=="ui":
			f=aJ(c["v"])
			if f and f[2]:p=aU(g,f[2],0,*bT(ref,x,y,w,h,2))
		elif t=="script":
			j=bP(Y(c)).strip().lower();a=bC.get(j)if j else None
			if a and Kit.pic_size(a)[0]>0:p=bg(g,a,x,y,w,h)
		if p is not None:e=True;d.append(p)
		if t and not e:d.extend(bR(g,Y(c),x,y+b,w,h-b))
		return d,p
	def c9(g,info,parts,counted,k,tip,click):
		x,y,w,h=info["x"],info["y"],info["w"],info["h"]
		if counted:info["count"]=Kit.add_label(g,"",x+w-6,y+h-16);info["txt"],info["hue"]="",Kit.HUE_TEXT;parts.append(info["count"])
		if k:info["key"]=c6(g,k,x,y,w);parts.append(info["key"])
		info["tip"]=tip;info["catcher"]=Kit.catcher(g,x,y,w,h,eN(*click),tip);parts.append(info["catcher"]);eO(info["catcher"],z(click[1:]));info["parts"]=parts;return info
	def bU(i):
		c,e=az(i),b["bagmode"];f=(e==0 and a["ub_state"])and("Show the Bags window"if a["ub_state"]!="open"else "Fold the Bags window into the bar")
		if e==1:d=("Open %s\nRight-click: pick another bag, or clear the slot"%c["n"]if c else "Empty: click, then target a bag for it")
		elif f:d=f+"\n%sRight-click: the Bags settings"%(c["n"]+"   "if c else "")
		else:d="Open %s"%c["n"]if c else "No bag here"
		g=X()[i]
		if g:d+="  [%s]"%g
		return d
	def eP(g,i,x,y,w,h):Kit.add_tiled(g,ae,x,y,w,h,af);da(g,i,x,y,w,h)
	def da(g,i,x,y,w,h):a=az(i);c={"x":x,"y":y,"w":w,"h":h,"count":None};d=[aU(g,a["g"],a["h"],x+3,y+3,w-6,h-6)]if a and a["g"]else[];e["bags"][i]=c9(g,c,d,a,X()[i]if b["keys"]else "",bU(i),("bag","bagmenu",i))
	def ao(refs):a["redraw"].update(refs)
	def eQ(ref):
		g=e["g"];d=ref[0]=="b";a,k=(e["bags"].get(ref[1]),X()[ref[1]])if d else(e["cells"].get(ref),A(ref)["k"])
		if a is None or not Kit.is_open(g):return
		c=a.pop("key",None);f=a.setdefault("parts",[]);h=b["keys"]and k
		if not d and bool(h and A(ref)["t"])!=(c is not None):
			if c is not None:a["key"]=c
			ao([ref]);return
		if c is not None:
			Kit.dispose(c)
			if c in f:f.remove(c)
		if b["keys"]and k and(d or A(ref)["t"]):a["key"]=c6(g,k,a["x"],a["y"],a["w"]);f.append(a["key"])
		bi(a,bU(ref[1])if d else aM(ref))
	def bi(info,tip):
		c=info.get("catcher")
		if c is not None and info.get("tip")!=tip:info["tip"]=tip;Kit.with_tip(c,tip)
	def db():
		if not Kit.is_open(e["g"]):return
		for b,a in list(e["cells"].items()):
			c=A(b)
			if(c["t"]=="ui"and(c["v"]in("spellbook","virtue")or c["v"].startswith("mod:"))or c["t"]=="travel"):bi(a,aM(b))
		for i,a in list(e["bags"].items()):bi(a,bU(i))
	def bj(a,hue,tip):
		for b in a["text"]:b.Hue=hue
		Kit.with_tip(a.get("catcher"),tip)
	def bV():
		a=e.get("keybtn")
		if a and Kit.is_open(e["g"]):bj(a,*de())
	def dc():
		if not Kit.is_open(e["g"]):return
		a=e.get("traybtn")
		if a:
			n=len(a9());c=Kit.HUE_TITLE if n else Kit.HUE_INFO
			for b in a.get("text",[]):Kit.set_text(b,str(n),c);Kit.ui_pos(b,a["x"]+(a["w"]-Kit.text_px(str(n)))//2,a["ly"])
			Kit.with_tip(a.get("catcher"),df(n))
		dm()
	bk=(("up","Next page of the bottom-left cells (page %d of %d showing)"),("dn","Previous page of the bottom-left cells (page %d of %d showing)"),("catcher","Page %d of %d of the bottom-left cells; click for the next page"))
	def eR(g,store,x,d,ph,m):p=b["page"];c,a=Kit.pic_size(Kit.ART_RESTORE[0]);c,a=c or 16,a or 16;n=x+(m-c)//2;f,h=R(n,d+1,c,a)[:2];q=Kit.art_button(g,store,"pgup",Kit.ART_RESTORE,f,h,None,bk[0][1]%(p+1,N),on_click=z(("page",1)));f,h=R(n,d+ph-a-1,c,a)[:2];r=Kit.art_button(g,store,"pgdn",Kit.ART_MIN,f,h,None,bk[1][1]%(p+1,N),on_click=z(("page",-1)));o=str(p+1);i,j,k,l=R(x,d+a+1,m,max(1,ph-2*a-2));s=Kit.add_label(g,o,i+(k-Kit.text_w(o))//2,j+(l-14)//2,Kit.HUE_TITLE);t=Kit.catcher(g,i,j,k,l,z(("page",1)),bk[2][1]%(p+1,N));e["pagecol"]={"up":q,"dn":r,"num":s,"catcher":t,"rect":(i,j,k,l),"page":p}
	def eS():
		a=e.get("pagecol");p=b["page"]
		if not a or a["page"]==p or not Kit.is_open(e["g"]):return
		a["page"]=p;c=str(p+1);f,g,h,i=a["rect"];d=a["num"];Kit.set_text(d,c);Kit.ui_pos(d,f+(h-Kit.text_w(c))//2,g+(i-14)//2)
		for k,j in bk:Kit.with_tip(a[k],j%(p+1,N))
	def eT(g,key,d,x,y,w,h):
		Kit.add_tiled(g,ae,x,y,w,h,af);a=safe(d.get("state"));b=d.get("title")or key;e=0 if a=="open"else Kit.HUE_INFO;c=d.get("icon")or 0;f=c and aU(g,c,e,x+2,y+2,w-4,h-4)is not None
		if not f:bQ(g,b[:3].upper(),x,y,w,h,Kit.HUE_TEXT if a=="open"else Kit.HUE_INFO)
		i=("%s is off; click to turn it on"if a is None else "Fold %s into the bar"if a=="open"else "Show %s")%b;Kit.catcher(g,x,y,w,h,z(("dock",key)),i)
	def eU(g,box,a,fn,hue,tip):x,y,w,h=box;Kit.add_tiled(g,ae,x,y,w,h,af);return{"text":bQ(g,a,x,y,w,max(16,h),hue),"catcher":Kit.catcher(g,x,y,w,h,fn,tip)}
	def de():
		if a["bind"]is not None:return Kit.HUE_TITLE,"Keybind mode on: hover a cell, press a key; Esc or a click here ends it"
		return Kit.HUE_TEXT,"Start keybind mode: hover a cell and press a key to bind it"
	def df(n):return "%s folded into the bar; click to %s the tray"%(Kit.count(n,"window"),"hide"if b["tray_open"]else "show")
	def eV(g,store,L):
		c,h=L["m"],L["cw"];x=c+L["inner"]+L["sgc"];l=L["rowy"][-1]+L["rowh"][-1];d,f=Kit.pic_size(Kit.ART_MIN[0]);d,f=d or 16,f or 16;m=c+2+f+4;n=c+l-m;j=c2();A=(("Keys",z(("bind",)),de()),("Lock",z(("lockbar",)),bW()),("Grid",z(("grid",)),dg()))
		if aD()and n>=66 and h-4>=j:p,q=R(x+(h-d)//2,c+2,d,f)[:2];B,s=h-4,min(28,(n-8)//3);t=[R(x+2,m+at*(s+4),B,s)for at in range(3)]
		else:C,D,u,v=R(x,c,h,l);w=[(by,)+eF(by,u,v)for by in c3(not aD())];i,y,a,b=(next((dd for dd in w if dd[2]>=j and dd[3]>=a1),None)or max(w,key=lambda o:min(o[2]-j,o[3]-a1)));a,b=max(1,a),max(1,b);E=i*a+(i-1)*K;F=y*b+(y-1)*K;G=C+max(K,(u-E)//2);H=D+max(K,(v-F)//2);k=[(G+(f6%i)*(a+K),H+(f6//i)*(b+K),a,b)for f6 in range(4)];p,q=k[0][0]+(a-d)//2,k[0][1]+(b-f)//2;t=k[1:]
		if not Kit.zone_up(r):Kit.art_button(g,store,"min",Kit.ART_MIN,p,q,None,"Minimize the bar",on_click=z(("toggle_min",)))
		e["keybtn"],e["lockbtn"],e["gridbtn"]=[eU(g,ga,f7,f8,*f9)for(f7,f8,f9),ga in zip(A,t)]
	def dg():
		if HOST.grid_shown():return Kit.HUE_TITLE,"Hide the screen grid windows snap to"
		return Kit.HUE_INFO,"Show the screen grid; windows you let go snap to it, the corners, edge middles and centre"
	def eW():
		b=bool(HOST.grid_toggle());a=e.get("gridbtn")
		if a and Kit.is_open(e["g"]):bj(a,*dg())
		l("screen grid %s."%("shown"if b else "hidden"))
	def bW():
		if ce():
			if bs():return Kit.HUE_TITLE,"Lock every window in its zone"
			return Kit.HUE_INFO,"Unlock the layout to move windows between zones"
		if b["lock"]:return Kit.HUE_BAD,"Locked; click to unlock the bar"
		return Kit.HUE_INFO,"Lock the bar in place"
	def dh():
		g,a=e["g"],e.get("lockbtn")
		if not a or not Kit.is_open(g):return False
		g.CanMove=not b["lock"]and not cf(r);bj(a,*bW());e["arranging"]=bs();return True
	di=("g","store","cells","bags","keybtn","lockbtn","gridbtn","traybtn","pagecol")
	def dj():
		b=dict((f,e.get(f))for f in di);a=b["g"];x,y=(a.GetX(),a.GetY())if Kit.is_open(a)else(None,None);e.setdefault("stale",[]).append(a);e.update(dict.fromkeys(di[4:]),g=None,cells={},bags={});d=({},{});aR[0]=None;c={"g":None}
		try:eX(x,y,d,c)
		except Exception:
			if e["g"]is None:Kit.dispose(c["g"]);e.update(b);aR[0]=None;e["stale"]=[g for g in e.get("stale",[])if g is not a]
			else:
				for s in e.pop("stale",[]):Kit.dispose(s)
			raise
	def eX(x,y,store,built):
		J=cf(r);K=a["em"]=bool(a["minimized"])and not Kit.zone_up(r)
		if K:
			w,h=cx,cy
			if x is None:x,y=Kit.load_pos(bu,(200,600),(w,h))
			g=built["g"]=G.CreateGump(True,not J);Kit.mini_bar(g,store,w,h,aH,r,z(("toggle_min",)),"%s: page %d"%(aH,b["page"]+1))
		else:
			eB();L=bO();w,h=bd();C["off"]=(0,0);l=bM()
			if l is not None:C["off"]=(max(0,(l[0]-w)//2),max(0,(l[1]-h)//2));w,h=max(w,l[0]),max(h,l[1])
			if x is None:x,y=Kit.load_pos(bu,(200,600),(w,h))
			p,M,m=L["m"],L["pw"],L["p4"];v,A,V=L["ug"],L["bg"],L["tb"];B,q,s=L["sgx"],L["colx"],L["colw"];N,O,P,Q=L["rowy"],L["rowh"],L["celly"],L["cellh"];k=p+M;g=built["g"]=G.CreateGump(True,not b["lock"]and not J);Kit.add_window_frame(g,w,h,corners=False);d=0
			for W,X in([("x",at*u)for at in range(b["extra"]-1,-1,-1)]+([("a",0)]if b["top"]else[])):
				c=p+N[d];Kit.gold_box(g,*R(k,c,L["top_w"],O[d]));f,n=c+P[d],Q[d]
				for i in range(u):bS(g,(W,X+i),*R(k+q[i],f,s[i],n))
				bh(g,[k+by for by in q],s,f,n);d+=1
			c,j=p+N[d],O[d];f,n=c+P[d],Q[d];eR(g,store,p,c,j,M);Kit.gold_box(g,*R(k,c,L["left_w"],j))
			for i in range(H):bS(g,("a",u+i),*R(k+q[i],f,s[i],n))
			bh(g,[k+dd for dd in q[:H]],s,f,n);t=k+L["left_w"]+B;Kit.gold_box(g,*R(t,c,L["ui_w"],j));Kit.add_tiled(g,Kit.STONE_TILE,*R(t+m,c+m,L["ui_w"]-2*m,j-2*m),alpha=.55);E=D*L["bw"]+(D-1)*v;o=t+(L["ui_w"]-E)//2
			for i in range(D):bS(g,("u",i),*R(o+i*(L["bw"]+v),c+(j-L["bh"])//2,L["bw"],L["bh"]))
			bh(g,[o+fn*(L["bw"]+v)for fn in range(D)],(L["bw"],)*D,c+(j-L["bh"])//2,L["bh"]);F=t+L["ui_w"]+B;Kit.gold_box(g,*R(F,c,L["bag_w"],j));E=I*L["bgw"]+(I-1)*A;o=F+(L["bag_w"]-E)//2
			for i in range(I):eP(g,i,*R(o+i*(L["bgw"]+A),f,L["bgw"],L["bgh"]))
			bh(g,[o+f6*(L["bgw"]+A)for f6 in range(I)],(L["bgw"],)*I,f,L["bgh"]);S=F+L["bag_w"]+B;Kit.gold_box(g,*R(S,c,L["tray_w"],j));eY(g,*R(S+m,f,V,L["bgh"]));eV(g,store,L)
		if b["anchor"]and not Kit.zone_up(r):
			T,Y=Kit.anchor_pos(b["anchor"],w,h)
			if T is not None:x,y=T,Y
		a["last_pos"]=Kit.show_window(g,x,y,w,h,None,False,eA(g),aO,e,{"g":g,"store":store});a["moved_at"]=None
		for Z in e.pop("stale",[]):Kit.dispose(Z)
		if not K and time.time()-a.get("counted_at",0.)>bw:
			U=aP()
			if "item"in U["types"]or U["extra"]:aQ()
		aS();dm()
	def eY(g,x,y,w,h):n=len(a9());Kit.add_tiled(g,ae,x,y,w,h,af);a=bQ(g,str(n),x,y,w,h,Kit.HUE_TITLE if n else Kit.HUE_INFO);e["traybtn"]={"text":a,"x":x,"w":w,"ly":y+(h-14)//2-1,"catcher":Kit.catcher(g,x,y,w,h,z(("traywin",)),df(n))}
	def dk(w,h,at=None,rect=False):
		if rect is False:
			g=e["g"]
			if not Kit.is_open(g):return 300,300
			rect=Kit.rect(g)
			if at is None:at=Kit.pos(g)or(0,0)
		a,b=at;d,c=(rect[2],rect[3])if rect is not None and rect[2]>0 else bd();W,H=Kit.screen()
		if aD():
			x,y=a+d+ad,b+c-h
			if W and x+w>W:
				x=a-ad-w
				if x<0:
					x,y=a,b+c+ad
					if H and y+h>H:y=b-ad-h
		else:
			x,y=a,b+c+ad
			if H and y+h>H:
				y=b-ad-h
				if y<0:
					x,y=a+d+ad,b
					if W and x+w>W:x=a-ad-w
		return x,y
	def eZ():return e["g"]
	f5=None
	def e_():
		d,a["redraw"]=a["redraw"],set();g=e["g"]
		if not d or a["em"]or not Kit.is_open(g):return
		for c in sorted(d):
			f=c[0]=="b";b=e["bags"].get(c[1])if f else e["cells"].get(c)
			if b is None:continue
			for p in b.get("parts")or():Kit.dispose(p)
			if f:da(g,c[1],b["x"],b["y"],b["w"],b["h"])
			else:c7(g,c,b["x"],b["y"],b["w"],b["h"])
		aS()
	def dl():
		g=e["g"]
		if not b["anchor"]or not Kit.is_open(g)or Kit.zone_up(r):return
		w,h=bd();x,y=Kit.anchor_pos(b["anchor"],w,h)
		if x is None:return
		if(x,y)!=a.get("last_pos"):g.SetPos(x,y);Kit.note_rect(g,x,y);Kit.moved_by_code(g);a["last_pos"]=(x,y);dn()
	def e0(x,y):
		if a["em"]:return
		if Kit.zone_up(r):return
		w,h=bd();c=Kit.anchor_at(x,y,w,h,SNAP_ANCHOR);d=True if c in("L","R")else False if c in("T","B")else None;e=d is not None and d!=b["vertical"]
		if c!=b["anchor"]or e:
			b["anchor"]=c
			if e:b["vertical"]=d;Q();ag();l("standing %s along the %s edge."%("upright"if d else "flat",{"L":"left","R":"right","T":"top","B":"bottom"}[c]));return
			Q()
		dl();aO()
	def e1(now):
		g=e["g"]
		if not Kit.is_open(g):return
		d=Kit.rect(g);c=(d[0],d[1])if d else(0,0)
		if c!=a.get("last_pos"):a["last_pos"],a["moved_at"]=c,now
		elif a.get("moved_at")is not None and now-a["moved_at"]>=.3 and SNAP.pressed()is not True:a["moved_at"]=None;e0(c[0],c[1])
		dn(c,d)
		if b["anchor"]and now>=a.get("screen_next",0.):
			a["screen_next"]=now+2.;f=Kit.screen()
			if f!=a.get("screen_wh"):
				a["screen_wh"]=f
				if not Kit.zone_up(r):dl()
	def dm():
		k,U["g"]=U["g"],None;d=a9()
		if a["em"]or not b["tray_open"]or not d:Kit.dispose(k);return
		L=bO();f,l,m=L["tb"],L["bg"],max(4,L["tm"]//2);c,i=Kit.pic_size(Kit.ART_MIN[0]);c,i=c or 16,i or 16;j=L["bgh"];w=m+len(d)*(f+l)+c+m;h=m+j+m;g=G.CreateGump(True,False);Kit.add_window_frame(g,w,h,corners=False)
		for n,(o,p)in enumerate(d):eT(g,o,p,m+n*(f+l),m,f,j)
		q=({},{});Kit.art_button(g,q,"fold",Kit.ART_MIN,w-m-c,m+(j-i)//2,None,"Hide the tray (the bar's numbered button brings it back)",on_click=z(("traywin",)));x,y=dk(w,h);Kit.place(g,x,y,w,h);U.update({"g":g,"at":(x,y),"w":w,"h":h});Kit.add_front(g);Kit.attach(g,e["g"]);Kit.dispose(k)
	def dn(at=None,rect=False):
		g=U["g"]
		if not Kit.is_open(g):return
		w,h=U.get("w",0),U.get("h",0);x,y=dk(w,h,at,rect)
		if(x,y)!=U["at"]:U["at"]=(x,y);g.SetPos(*Kit.clamp(x,y,w,h));Kit.moved_by_code(g)
	def e2():
		aQ(cz);b=(next((c for c in(a["first_g"].get(d)for d in cz)if c),None)or API.FindLayer("Spellbook"))
		if b:API.UseObject(b);return True
		l("no spellbook in your pack.",Kit.HUE_BAD);return False
	def do():
		if ce():HOST.layout_arrange();dh();return
		b["lock"]=not b["lock"];Q()
		if not dh():ag()
		if T.f is not None:T.f.c["lock"].IsChecked=b["lock"]
		else:ab(r)
		l("%s."%("locked"if b["lock"]else "unlocked"),Kit.HUE_GOOD)
	def e3():
		g=e["g"];b=Kit.mouse_pos();c=Kit.pos(g)if Kit.is_open(g)else None
		if b is None or c is None:return
		d,f=b[0]-c[0],b[1]-c[1]
		for h,a in(list(e["cells"].items())+[(("b",k),m)for k,m in e["bags"].items()]):
			if a["x"]<=d<a["x"]+a["w"]and a["y"]<=f<a["y"]+a["h"]:return h
		return
	def bX(ref=None):ci();a["bind"]={"sel":ref};bV();l("keybind mode on: %s (Esc ends it, Backspace clears a key)."%("click a cell, then press a key"if Kit.mouse_pos()is None else "hover a cell and press a key"))
	def bl():
		if a["bind"]is None:return
		a["bind"]=None;bV();l("keybind mode off.")
	def e4():ci();a["bind"]={"sel":au};bV();l("press the key for the radial ring (Esc ends, Backspace clears it).")
	def bY(ref,k):
		a=ref==au;c=HOST.hotkeys_owned.get(_norm_key(k))if a else ak(k)
		if c:l("%s belongs to %s; pick another."%(k,c),Kit.HUE_BAD);return
		d=_norm_key(k)
		if a and(d in cH()or any(h["t"]and _norm_key(h["k"])==d for m in B["pages"]for h in m)):l("%s is on a cell; pick another."%k,Kit.HUE_BAD);return
		b=[ref]
		for r,e in al():
			if r!=ref and _norm_key(e["k"])==k:e["k"]="";b.append(r);l("%s taken off %s."%(k,M(r)))
		for i,f in enumerate(X()):
			if("b",i)!=ref and f==k:bE(("b",i),"");b.append(("b",i));l("%s taken off bag slot %d."%(k,i+1))
		bE(ref,k)
		if ref[0]=="b":aN()
		ar();dp(b);g=ref[0]in("a","u","x")and not A(ref)["t"];l("%s bound to %s%s."%(k,M(ref)," (empty; fill it to use it)"if g else ""),Kit.HUE_GOOD)
		if a:bl()
	def e5(d):
		c=a["bind"]
		if not c:return
		k=d.rsplit("+",1)[-1]
		if k=="ESCAPE":bl();return
		b=c["sel"]if c["sel"]==au else e3()or c["sel"]
		if b is None:l("hover a cell on the bar (or click one) first.");return
		c["sel"]=b
		if k in("BACKSPACE","DELETE"):
			bE(b,"");ar();dp([b]);l("%s has no hotkey now."%M(b),Kit.HUE_GOOD)
			if b==au:bl()
			return
		bY(b,d)
	def dp(refs):
		for r in refs:
			if r!=au:eQ(r)
		a=aK(J["sel"])
		if T.f is not None and a in refs:T.f.c["key"].SetText(A(a)["k"])
	dq={"barsettings":lambda:aX(r),"lock":lambda:do(),"minimize":lambda:z(("toggle_min",))(),"war":lambda:API.SetWarMode(not bool(API.Player.InWarMode)),"help":lambda:API.OpenHelp(),"quests":lambda:API.OpenQuestLog()}
	def bZ(uid):
		d=aJ(uid)
		if d is None:l("unknown window button '%s'."%uid,Kit.HUE_BAD);return False
		a=d[3];b=True
		if a in dq:dq[a]()
		elif a=="grimoire":return em()
		elif a=="virtue":return en()
		elif a=="launcher":return e6()
		elif a=="paperdoll":
			import System
			if not ClientUI.game_action("OpenPaperdoll",[System.UInt32(int(API.Player.Serial))]):
				if aF():W(lambda:bZ("paperdoll"))
				else:b=safe(lambda:API.ContextMenu(API.Player,"Open Paperdoll",2),None)is not False
		elif a.startswith("mod:"):return ea(a[4:])
		elif a.startswith("ga:"):c=a.split(":");b=ClientUI.game_action(c[1],reuse=c[2]if len(c)>2 else None)
		elif a.startswith("macro:"):b=ClientUI.open_macro(a[6:])
		if not b:l("couldn't open %s (%s)."%(d[1],ClientUI.error or "unknown"),Kit.HUE_BAD)
		return b
	def e6():
		a=HOST.services.get("launcher.open")
		if a is None:l("the Quick Launcher needs the full Virtue Assistant.",Kit.HUE_BAD);return False
		try:a()
		except Exception as b:l("couldn't open the Quick Launcher (%s)."%b,Kit.HUE_BAD);return False
		return True
	ap={"looked":False,"type":None}
	def b_():
		if not ap["looked"]and aF():
			if not ap.get("asked"):ap["asked"]=True;W(b_)
			return[]
		if not ap["looked"]:ap["looked"]=True;ap["type"]=aW("ClassicUO.LegionScripting.LegionScripting")
		t=ap["type"]
		if t is None:return[]
		c=[]
		def a(a,n):return str(safe(lambda:ClientUI._get(a,n),"")or "")
		with Kit.quiet:
			for b in(ClientUI._get(None,"LoadedScripts",t)or[]):
				d,e=a(b,"RelativePath")or a(b,"FileName"),a(b,"FullPath")
				if d or e:c.append((d,e))
		return c
	dr={};b0=set()
	def b1(v):
		v=str(v or "").strip().replace("\\","/");b=dr.get(v)
		if b is not None and time.time()<b[0]:return list(b[1])
		f=v.split("/")[-1];k,l=v.lower(),f.lower();d=[]
		def a(c):
			if c and c not in d:d.append(c)
		m=not aF()
		if not m:
			if v not in b0:
				b0.add(v)
				def n():b0.discard(v);b1(v)
				W(n)
			if b is not None:return list(b[1])
		if "/"in v:a(v)
		for e,q in b_():
			r=e.replace("\\","/");g=r.lower()
			if g==k or g.endswith("/"+k)or g.split("/")[-1]==l:a(r)
		if not m:a(v);a(f);return list(d)
		h=dy()
		if h:
			with Kit.quiet:
				for o,i,p in os.walk(h):
					e=o.replace("\\","/")[len(h):].strip("/")
					if e.count("/")>=2:i[:]=[]
					i[:]=[s for s in i if not s.startswith(".")and s.lower()not in b4]
					for j in p:
						if j.lower()==l:a((e+"/"+j)if e else j)
		a(v);a(f);dr[v]=(time.time()+60.,d);return list(d)
	bm={}
	def bn(v):
		b=b1(v);a=bm.get(v)
		if a is not None and a in b:
			try:
				if API.IsScriptRunning(a):return True
			except Exception:pass
		for c in b:
			if c==a:continue
			try:
				if API.IsScriptRunning(c):
					if len(bm)>200:bm.clear()
					bm[v]=c;return True
			except Exception:pass
		return False
	def e7(v):
		e=b1(v);b=bn(v);f=API.StopScript if b else API.PlayScript;d=False
		for g in e:
			if not safe(lambda c=g:(f(c),True)[1],False):continue
			d=True
			if not HOST.idle(.1)or bn(v)!=b:break
		a["script_check"]=(v,b,time.time()+.5);return d
	def e8(now):
		b=a.get("script_check")
		if not b or now<b[2]:return
		a["script_check"]=None;v,c,f=b;e=bn(v);d=v.replace("\\","/").split("/")[-1]
		if c and not e:l("stopped %s."%d)
		elif not c and e:l("started %s."%d,Kit.HUE_GOOD)
		elif not c:l("%s didn't start; is it in the Legion Script Manager's list (refresh it)?"%d,Kit.HUE_BAD)
		aS()
	def e9(c):
		def e():return a["first"].get((c["g"],c["h"]))or(None if b["hue"]else a["first_g"].get(c["g"]))
		f=time.time()-a.get("counted_at",0.)>bw
		if f:aQ()
		d=e()
		if not d and not f:aQ();d=e()
		if not d:l("no %s left."%Y(c),Kit.HUE_BAD);return False
		API.UseObject(d);a["next_count"]=time.time()+.4;HOST.pack_dirty();return True
	ds={"spell":API.CastSpell,"skill":API.UseSkill,"dress":API.Dress,"undress":API.Undress,"say":API.Msg};fa=("stealing","snooping","discordance","provocation")
	def dt(c,t,v):
		if t=="skill":n=v.lower();return bool(n)and any(n in d for d in fa)
		if t=="spell":n=v.lower();return bool(n)and(n in cp or any(f.startswith(n)for f in cp))
		return t=="item"and int(c.get("g")or 0)==3853
	def fb(a,c,t,v):
		if c["tg"]!="last"or not dt(c,t,v):return False
		return not HOST.harm_ok(int(API.LastTargetSerial or 0),("actionbar",)+a,aH,True,"press again to confirm",t=="skill")
	def du(ref):
		c=A(ref);t,v=c["t"],c["v"].strip()
		if not t:l("%s is empty."%M(ref));return
		m=time.time();e=(ref,b["page"])
		if fb(e,c,t,v):return
		h=c["tg"]in("self","last")and t not in("travel","say","ui","dress","undress","ability");w=a["want_target"]
		if w and m>w[1]:w=None
		i=bool(w)and w[2]==e;j=False
		if w and not i:aV();j=h
		d=True;n=bool(API.HasTarget("any"))
		try:
			if t in ds:ds[t](v)
			elif t=="item":d=e9(c)
			elif t=="macro":
				f=ClientUI.run_macro(v);d=bool(f)
				if f is None:l("no TazUO macro named '%s'."%v,Kit.HUE_BAD)
				elif not f:l("couldn't run macro '%s' (%s)."%(v,ClientUI.error or "unknown"),Kit.HUE_BAD)
			elif t=="ability":API.ToggleAbility(v or "primary")
			elif t=="script":
				def o():
					try:e7(v)
					except Exception as a:l("couldn't use %s (%s)."%(Y(c),a),Kit.HUE_BAD)
				W(o)
			elif t=="ui":d=bZ(v)
			elif t=="travel":d=et(c)
		except Exception as p:l("couldn't use %s (%s)."%(Y(c),p),Kit.HUE_BAD);d=False
		if d and t in("skill","spell"):ew(t,v)
		if d and h and not i:
			if j:l("a target was still pending; target by hand.")
			elif n:l("a target cursor was already up; target by hand.")
			elif cb(r):l("another module is using the target cursor; target by hand.")
			else:
				g=2.5
				if t=="spell":k=Kit.spell_info(v);g+=k[3]if k else 0.
				HOST.claim_cursor(r,g);a["want_target"]=(c["tg"],time.time()+g,e,dt(c,t,v),int(API.LastTargetSerial or 0))
	def fc(now):
		w=a["want_target"]
		if not w:return
		c,d=w[0],w[1]
		if now>d:aV();return
		if not API.HasTarget("any"):return
		aV()
		if cb(r):return
		if API.HasTarget("beneficial"if w[3]else "harmful"):l("that cursor isn't this cell's; target by hand.");return
		if c=="self":API.TargetSelf()
		else:
			b=w[4]if w[3]else int(API.LastTargetSerial or 0)
			if b:API.Target(b)
			else:l("no last target yet; target by hand.")
	def aV():a["want_target"]=None;HOST.release_cursor(r)
	def dv(action):
		aV()
		def a(serial):z.add(tuple(action)+(int(serial or 0),),dup=True)
		HOST.pick_target(15,a)
	def b2(ref):l("target an item for %s (Esc to cancel)."%M(ref));dv(("picked_item",ref,b["page"]))
	def fd(ref,pg,serial):
		if a["shutting"]or ca():return
		c=Kit.find_item(serial)
		if c is None:l("no item picked.");return
		e,i=int(c.Graphic or 0),int(c.Hue or 0);f=str(c.Name or "")or("0x%04X"%e);g=M(ref);h=[ref]
		if ref[0]=="a"and ref[1]>=u and pg!=b["page"]and B["pages"]:d=B["pages"][pg][ref[1]-u];g="page %d cell %d"%(pg+1,ref[1]-u+1);h=[]
		else:d=A(ref)
		d.update({"t":"item","v":"","g":e,"h":i,"n":f})
		for k in bB:d.pop(k,None)
		an(recount=True,refs=h);l("%s set on %s."%(f,g),Kit.HUE_GOOD)
	def dw(i):l("target a bag for bag slot %d (Esc to cancel)."%(i+1));dv(("picked_bag",i))
	def fe(i,serial):
		if a["shutting"]or ca():return
		b=Kit.find_item(serial)
		if b is None or not b.IsContainer:l("that isn't a bag.",Kit.HUE_BAD);return
		cP(i,serial);a["next_scan"]=0.
	def ff(ref):
		if a["bind"]is not None:a["bind"]["sel"]=ref;l("%s; now press a key or combination for it."%M(ref))
		elif A(ref)["t"]:du(ref)
		elif ref[0]in("a","x"):b2(ref)
		else:b6(ref)
	def b3(i):
		if a["bind"]is not None:a["bind"]["sel"]=("b",i);l("bag slot %d; now press a key or combination for it."%(i+1));return
		c=az(i)
		if b["bagmode"]==1 and c is None:dw(i);return
		if b["bagmode"]==0:
			d=ay()
			if d in("collapsed","docked"):bI("show");Z()
			elif d=="open":Z();bI("dock")
			else:e=c["s"]if c else None;ba(aw,"Bags",(lambda:API.UseObject(e))if e else None)
		elif c is None:l("no bag in that slot (see Bag slots on the Action Bar settings page).")
		else:API.UseObject(c["s"])
	dx=[("item","Item...")]+[(gf,dict(a4)[gf])for gf in "spell skill ability ui macro script dress undress say travel".split()];fg=dict(dx+[("hotkey","Hotkey"),("lo","Red at")]);bo={"macro":"TazUO macros","script":"Legion scripts","dress":"Dress outfits","undress":"Dress outfits"}
	def dy():a=Kit.script_dir().replace("\\","/").rstrip("/");b=os.path.dirname(a);return b if b and b!=a else a
	b4=("iplib","lib","libs","library","site-packages","dlls","stubs","__pycache__","api","docs","examples","virtueassistantmodules")
	def fh():
		b=dy();h=b.lower();c=[]
		for i,j in b_():
			p=j.replace("\\","/");a=(p[len(b):].strip("/")if b and p.lower().startswith(h)else(p or i));g=a.lower().split("/")
			if any(m in b4 for m in g[:-1])or g[-1].startswith("_"):continue
			if a and a not in c:c.append(a)
		if c or not b:return sorted(c,key=lambda s:s.lower())
		with Kit.quiet:
			for k,d,e in os.walk(b):
				a=k.replace("\\","/")[len(b):].strip("/")
				if a.count("/")>=2 or "__init__.py"in e:
					d[:]=[]
					if "__init__.py"in e:continue
				d[:]=[n for n in d if not n.startswith(".")and n.lower()not in b4]
				for f in e:
					if f.lower().endswith(".py")and not f.startswith("_"):c.append((a+"/"+f)if a else f)
		return sorted(c,key=lambda s:s.lower())
	def dz(cat):
		if cat=="macro":return ClientUI.macro_names()
		if cat=="script":return fh()
		return list(API.GetAvailableDressOutfits()or[])
	b5={"macro":"The name of a macro from TazUO's macro window","script":"The script's file name (heal.py, or Spells/Bless.py)","dress":"An outfit name from TazUO's dress agent","undress":"An outfit name from TazUO's dress agent","say":"The text to say in game","hotkey":"A key or combination (F5, CTRL+Q, SHIFT+F2; blank = none)","lo":"The counter turns red at this many or fewer (0 = only when none)"}
	def fi(info):a=Kit.pos(e["g"])if Kit.is_open(e["g"])and info is not None else None;return None if a is None else(a[0]+info["x"],a[1]+info["y"],info["w"],info["h"])
	def fj(w,h):
		a=j.get("anchor")
		if j.get("moved")is not None:x,y=j["moved"]
		elif a is None:x,y=300,300
		else:c,b,e,d=a;x,y=c,b+d+2
		W,H=Kit.screen()
		if W and H:
			if a is not None and j.get("moved")is None and y+h>H:y=b-2-h
			x,y=max(0,min(x,W-w)),max(0,min(y,H-h))
		return int(x),int(y)
	def aq():g,j["g"]=j["g"],None;j["c"]={};Kit.dispose(g)
	def fk(g):
		def a(*a):
			if j["g"]is g:j["g"]=None;j["c"]={}
		return a
	def b6(ref,bag=None):j.update({"ref":ref,"bag":bag,"level":"cats"if ref else "bag","cat":None,"page":0,"moved":None,"placed":None,"anchor":fi(e["cells"].get(ref)if ref else e["bags"].get(bag))});b7()
	def dA(rows):return[rows[c:c+a2*bA]for c in range(0,len(rows),a2*bA)]
	def fl():
		f,d=j["level"],j["cat"]
		if f=="bag":
			i=j["bag"];a=[]
			if b["bagmode"]==1:a+=[("Pick a bag...",("pickbag",i)),("Clear this slot",("clearbag",i))]
			elif b["bagmode"]==0:
				s=ay()
				if s in("collapsed","docked"):a.append(("Show the Bags window",("ub","show")))
				elif s=="open":a.append(("Fold the Bags window into the bar",("ub","dock")))
				else:a.append(("Turn Bags on",("ub","on")))
				if aw in HOST.by_key:a.append(("Bags settings",("ub","settings")))
			else:h=az(i);a.append(("Open %s"%h["n"]if h else "No bag here",("bag",i)))
			a.append(("Hotkey: %s"%(X()[i]or "none"),("bagbind",i)));a.append(("Bag slots: "+a5[b["bagmode"]],("bagmode",None)));return a,None
		if f=="cats":
			g=A(j["ref"]);a=[(q,("cat",o))for o,q in dx];l={"self":"self","last":"last target"}.get(g["tg"],"none");a+=[("-",None),("Hotkey: %s"%(g["k"]or "none"),("cat","hotkey")),("Press a key for it",("bindsel",None)),("Then target: %s"%l,("target",None))]
			if g["t"]in("item","travel"):a.append(("Red at: %d or fewer"%max(0,g["lo"]),("cat","lo")))
			a+=[("Clear cell",("clear",None)),("More on the settings page",("settings",None))];return a,None
		if f=="method":return[(v,("tset",t))for t,v in d_],None
		if f=="list":
			if d=="spell":c=[[(x,("set",("spell",x)))for x in m.split("|")]for w,m in cB];e=d6
			elif d=="skill":c,e=[[(y,("set",("skill",y)))for y in d5]],["Skills"]
			elif d=="ability":c,e=[[("Primary ability",("set",("ability","primary"))),("Secondary ability",("set",("ability","secondary")))]],["Weapon ability"]
			elif d=="travel":
				if HOST.services.get("grimoire.destinations")is None:a=[("Grimoire is off: click to turn it on",("grimon",None))]
				elif not j["items"]:a=[("No runebook read yet: open Grimoire's runebook tabs",("none",None))]
				else:a=[(ax("%s  (%s)"%(G["name"],G["book_name"]),260),("tdest",L))for L,G in enumerate(j["items"])]
				c=dA(a);e=["Runebook destinations"]*len(c)
			elif d in bo:
				a=[(ax(at,220),("set",(d,at)))for at in j["items"]]
				if not a:a=[("Nothing saved in TazUO yet",("none",None))]
				a.append(("Type a name",("typed",d)));c=dA(a);e=[bo[d]]*len(c)
			else:
				c=[[(n[1],("set",("ui",n[0])))for n in bx]];e=["Client windows"];k=[(by[1],("set",("ui",by[0])))for by in cF()]
				if k:c.append(k);e.append("Module windows")
			p=max(0,min(len(c)-1,j["page"]));j["page"]=p;return c[p],(e[p],p,len(c))
		return[],None
	def b7():Kit.on_client(fm)
	def fm():
		o=j["g"];p=Kit.pos(o)if Kit.is_open(o)else None
		if p is not None and j.get("placed")is not None and p!=j["placed"]:j["moved"]=p
		j["g"],j["stale"]=None,o;f,q=({},{}),{};a,B=Kit.MARGIN,Kit.GAP;h,r=fl();c,d=j["level"],j["ref"]
		if c=="bag":i="BAG SLOT %d"%(j["bag"]+1)
		elif c=="method":i="TRAVEL TO %s"%str((j.get("dest")or{}).get("name","?")).upper()
		elif c in("list","text"):k=fg.get(j["cat"],"Hotkey");i="%s: %s"%(M(d).upper(),k.replace("...","").upper())
		else:i="SET "+M(d).upper()
		C=Kit.text_w(i)+60
		if c=="text":w=max(C,340);l=92
		else:s=max(1,min(bA,(len(h)+a2-1)//a2));D=(len(h)+s-1)//s if h else 1;m=max([Kit.text_w(at[0])for at in h]+[100])+24;w=max(C,2*a+16+s*m);l=10+D*a3+(34 if r else 10)
		t=w-2*a;u=a+30+B+l+a;g=G.CreateGump(True,True);Kit.add_window_frame(g,w,u,corners=False);Kit.add_section(g,a,a,t,30);Kit.add_label(g,i,a+10,a+7,Kit.HUE_TITLE);Kit.art_button(g,f,"close",Kit.ART_CLOSE,w-a-34,a+4,None,"Close the menu",on_click=z(("mpick","close",None)))
		if c not in("cats","bag"):Kit.art_button(g,f,"back",Kit.ART_RESTORE,w-a-54,a+7,None,"Back to the previous menu",on_click=z(("mpick","back",None)))
		b=a+30+B;Kit.add_section(g,a,b,t,l)
		if c=="text":
			n=A(d)
			if j["cat"]=="lo":E=str(max(0,n["lo"]))
			else:E=n["k"]if j["cat"]=="hotkey"else(n["v"]if n["t"]==j["cat"]else "")
			Kit.add_label(g,b5.get(j["cat"],""),a+10,b+8,Kit.HUE_INFO);q["text"]=Kit.add_textbox(g,E,a+10,b+32,t-20,numbers=False);Kit.art_button(g,f,"ok",Kit.ART_OK,a+10,b+62,"Apply","Save this value on the cell",on_click=z(("mpick","text",None)));q["status"]=Kit.add_label(g,"",a+10+35+Kit.text_w("Apply")+12,b+65,Kit.HUE_INFO)
		else:
			for H,(k,e)in enumerate(h):
				I,J=divmod(H,D);x=a+8+I*m;y=b+6+J*a3
				if e is None:Kit.add_tiled(g,Kit.STONE_TILE,x,y+a3//2,m-16,1);continue
				K=e[0]=="set"and(A(d)["t"],A(d)["v"])==e[1]or e[0]in("tdest","tset")and fo(d,e);Kit.add_label(g,k,x+4,y+2,Kit.HUE_GOOD if K else Kit.HUE_TEXT);Kit.catcher(g,x,y,m-8,a3,z(("mpick",)+tuple(e)),k)
			if r:
				L,N,F=r;v=b+l-28;Kit.add_label(g,"%s  (%d of %d)"%(L,N+1,F),a+10,v+4,Kit.HUE_INFO)
				if F>1:Kit.art_button(g,f,"next",Kit.ART_PAGE,w-a-44,v,None,"Next page",on_click=z(("mpick","page",1)));Kit.art_button(g,f,"prev",Kit.ART_PAGE,w-a-84,v,None,"Previous page",on_click=z(("mpick","page",-1)))
		x,y=fj(w,u);x,y=Kit.place(g,x,y,w,u);j.update({"g":g,"c":q,"placed":(x,y)});G.AddControlOnDisposed(g,fk(g));Kit.add_front(g);g.SetInScreen();Kit.dispose(j.pop("stale",None))
	def dB(ref,t,v):a=A(ref);b=dict(V(),t=t,v=v,k=a["k"],tg=a["tg"],lo=a["lo"]);B[ref[0]][ref[1]]=b;an(recount=True,refs=[ref]);l("%s set on %s."%(Y(b),M(ref)),Kit.HUE_GOOD)
	def fo(ref,action):
		c=A(ref)
		if c["t"]!="travel":return False
		if action[0]=="tdest":a=j["items"];d=a[action[1]]if 0<=action[1]<len(a)else None
		else:
			d=j.get("dest")
			if c.get("rm")!=action[1]:return False
		if not d:return False
		try:return(int(c.get("rb")or "0",16)==int(d["book"])and c.get("ri")==str(int(d["index"])))
		except(ValueError,TypeError,KeyError):return False
	def aa(**a):j.update(a);b7()
	def fp(what,a):
		b=j["ref"]
		if what in("close","bindsel","bagbind","set","settings","pickbag","clearbag","ub","bag","bagmode","tset","grimon")or(what,a)==("cat","item"):aq()
		if what in dC:dC[what](b,a)
	def fq(ref,a):
		if j["level"]=="method":aa(level="list",cat="travel")
		else:aa(level="cats",cat=None,page=0)
	def fr(ref,a):
		if a=="travel":b=HOST.services.get("grimoire.destinations");aa(items=list(safe(b,[])or[])if b is not None else[],level="list",cat="travel",page=0);return
		if a=="item":b2(ref);return
		if a in bo and aF():
			def c():
				b=dz(a)
				if j["ref"]==ref and j["level"]=="cats"and Kit.is_open(j["g"]):aa(items=b,level="list",cat=a,page=0)
			W(c);return
		if a in("spell","skill","ability","ui","macro","script","dress","undress"):aa(items=dz(a)if a in bo else[],level="list",cat=a,page=0);return
		aa(level="text",cat=a)
	def fs(ref,a):
		if j["level"]=="list"and j["cat"]=="travel"and 0<=a<len(j["items"]):aa(level="method",dest=j["items"][a])
	def ft(ref,a):
		if j.get("dest")and ref is not None:eu(ref,j["dest"],a)
	def fu(ref,c):
		v=str(j["c"]["text"].Text or "").strip()
		if j["cat"]=="hotkey":
			k=_norm_key(v);a=ak(k)
			if a:Kit.set_text(j["c"]["status"],"%s belongs to %s"%(k,a),Kit.HUE_BAD);return
			if k:bY(ref,k)
			else:A(ref)["k"]="";an(refs=[ref])
			aq();return
		if j["cat"]=="lo":
			try:b=int(v)
			except ValueError:Kit.set_text(j["c"]["status"],"Type a number",Kit.HUE_BAD);return
			A(ref)["lo"]=max(0,b);an(refs=[ref]);aq();return
		if not v:Kit.set_text(j["c"]["status"],"Type a value first",Kit.HUE_BAD)
		else:aq();dB(ref,j["cat"],v)
	def fv(ref,a):c=A(ref);c["tg"]={"":"self","self":"last","last":""}.get(c["tg"],"");aN();ao([ref]);ab(r);b7()
	def fw(ref,a):cZ(ref);aq()
	def fx(ref,a):J["sel"]=ed(ref);aX(r);ab(r)
	def fy(ref,b):cP(b,0);a["next_scan"]=0.
	def fz(ref,a):
		if a=="settings":
			if aw in HOST.by_key:aX(aw)
		elif a=="on":ba(aw,"Bags")
		else:Z();bI(a)
	dC={"bindsel":lambda ref,a:bX(ref),"bagbind":lambda ref,a:bX(("b",a)),"set":lambda ref,a:dB(ref,a[0],a[1]),"pickbag":lambda ref,a:dw(a),"bag":lambda ref,a:b3(a),"bagmode":lambda ref,a:aX(r),"grimon":lambda ref,a:ba(ct,"Grimoire"),"page":lambda ref,a:aa(page=j["page"]+a),"back":fq,"cat":fr,"tdest":fs,"tset":ft,"typed":lambda ref,a:aa(level="text",cat=a),"text":fu,"target":fv,"clear":fw,"settings":fx,"clearbag":fy,"ub":fz}
	def dD(ref):
		if ref[0]=="b":b3(ref[1])
		else:du(ref)
	def fA(ref):
		try:dD(ref)
		except Exception as a:l("couldn't use %s (%s)."%(M(ref),a),Kit.HUE_BAD)
	E={"g":None,"at":(0,0),"cells":[],"until":0.,"hot":None,"box":[],"side":0,"rad":0,"half":0,"start":(0,0)}
	def fB():p=b["radial_page"];a=b["page"]if not p else p-1;return[c for c in[("p",a*H+d)for d in range(H)]if A(c)["t"]]
	def bp():g,E["g"]=E["g"],None;E.update(cells=[],hot=None,box=[]);Kit.dispose(g)
	def fC():
		bp();i=fB()
		if not i:l("the radial ring's page has no filled cells.");return
		W,H=Kit.screen();j=Kit.mouse_pos()or(W//2,H//2);c=S(b["slot"],20);p=len(i);h=int(max(dQ,dR*p)*max(1.,c/44.));a=h+c//2+22;g=G.CreateGump(False,False);d=[];q=[]
		for v,k in enumerate(i):
			r=2*math.pi*v/p-math.pi/2;m,s=int(round(h*math.cos(r))),int(round(h*math.sin(r)));x,y=a+m-c//2,a+s-c//2;n=A(k);d.append(Kit.add_tiled(g,ae,x,y,c,c,af));w,z=c8(g,k,n,{},x,y,c,c,0);d.extend(w)
			if z is not None and n["t"]!="travel":t=ax(Y(n),c+28);d.append(Kit.add_label(g,t,a+m-Kit.text_w(t)//2,y+c+1))
			q.append((m,s,k))
		d.append(Kit.add_box(g,a-3,a-3,6,6,.8,"#909090"));o=[Kit.add_box(g,0,0,2,2,.95,dS)for L in range(4)]
		for u in d+o:
			if u is not None:Kit.inert(u)
		for B in o:B.SetAlpha(0.)
		e,f=j[0]-a,j[1]-a
		if W and H:e,f=max(0,min(e,W-2*a)),max(0,min(f,H-2*a))
		e,f=Kit.place(g,e,f,2*a,2*a);Kit.add_front(g);SNAP.skip_gump(g);E.update(g=g,at=(e+a,f+a),cells=q,until=time.time()+dP,hot=None,box=o,side=c,rad=h,half=a,start=j)
	def dE(pos):
		g=E["g"];a=Kit.pos(g)if g is not None else None
		if pos is None or a is None or not E["cells"]:return
		d=E["half"];e,f=pos[0]-a[0]-d,pos[1]-a[1]-d;h=math.hypot(e,f)
		if h<cn or h>E["rad"]+E["side"]//2+12:return
		if math.hypot(pos[0]-E["start"][0],pos[1]-E["start"][1])<cn:return
		i,b=None,None
		for c in E["cells"]:
			j=(c[0]-e)**2+(c[1]-f)**2
			if b is None or j<b:i,b=c,j
		return i
	def fD(now):
		if now>=E["until"]or not Kit.is_open(E["g"]):bp();return
		a=dE(Kit.mouse_pos());c=a[2]if a else None
		if c==E["hot"]:return
		E["hot"]=c;d=E["box"]
		if a is None:
			for b in d:b.SetAlpha(0.)
			return
		s,e=E["side"],E["half"];x,y=e+a[0]-s//2-2,e+a[1]-s//2-2
		for b,r in zip(d,((x,y,s+4,2),(x,y+s+2,s+4,2),(x,y,2,s+4),(x+s+2,y,2,s+4))):b.SetRect(*r);b.SetAlpha(.95)
	def fE():
		if E["g"]is None:return
		a=dE(Kit.mouse_pos());bp()
		if a is not None:z.add(("use",a[2]))
	def fF():b["radial_page"]=(b["radial_page"]+1)%(N+1);Q();ab(r)
	fG={"a":P,"u":D,"x":aI,"p":N*H};fH=dict(a4)
	def fI(q,n=8):
		d=str(q or "").lower().split();a=[];n=int(n or 0);e=([("a",g)for g in range(u)]+[("x",h)for h in range(aI)]+[("p",k)for k in range(N*H)]+[("u",m)for m in range(D)])
		for r in e:
			if len(a)>=n:break
			c=A(r);t=c["t"]
			if not t or not a6(r)or(t=="ui"and c["v"]=="launcher"):continue
			b=aL(c)if t=="travel"else Y(c)
			if not all(i in("%s %s"%(b,fH.get(t,t))).lower()for i in d):continue
			f={"a":"top row","u":"button %d"%(r[1]+1),"x":"row %d"%(r[1]//u+2),"p":"page %d"%(r[1]//H+1)}[r[0]];a.append(("%s  (%s)"%(b,f),r,"outfit"if t in("dress","undress")else t))
		return a
	def fJ(ref):
		try:
			a,i=ref;i=int(i)
			if not 0<=i<fG.get(a,0):return False
		except Exception:return False
		if not a6((a,i))or not A((a,i))["t"]:return False
		b=z.add(("use",(a,i)));aG(r);return b
	F={"ok":None,"held":{},"map":{},"hooks":None,"ring":None,"ring_down":None}
	def dF(k):
		b,a=_norm_key(k).split("+"),None
		for p in b:
			if p and p not in("CTRL","SHIFT","ALT"):a=p if p.startswith("SDLK_")else "SDLK_"+p
		c=[d for d in("CTRL","SHIFT","ALT")if d in b];return "+".join(c+([a]if a else[]))
	def fK(a):return "+".join(c[5:]if c.startswith("SDLK_")else c for c in str(a).upper().split("+"))
	def fL(ref):
		if ref[0]=="b":return(a["bind"]is None and az(ref[1])is not None and(b["bagmode"]!=0 or a["ub_state"]is not None))
		c=A(ref)
		if c["t"]=="ui":d=aJ(c["v"]);e=d[3]if d else "";return(e in("war","help","quests","paperdoll","lock","minimize")or e.startswith(("ga:","macro:")))
		return c["t"]in("item","spell","skill","ability","macro","say","dress","undress","travel")
	def fM(b):
		try:
			if not F["ok"]:return
			b=str(b);f=b.rsplit("+",1)[-1];g,c=time.time(),F["held"];h=c.get(f);c[f]=g
			if h is not None and g-h<cl:return
			if len(c)>32:
				for k in[i for i,m in c.items()if g-m>=cl]:del c[k]
			if a["shutting"]or e["g"]is None:return
			if a["bind"]is not None:
				if not bt():z.add(("bindkey",fK(b)),dup=True);aG()
				return
			if b==F["ring"]:
				if not bt():F["ring_down"]=f;z.add(("ring",True),dup=True);aG(r)
				return
			d=F["map"].get(b)
			if d is None or bt():return
			if fL(d):fA(d)
			else:z.add(("use",d),dup=True);aG()
		except Exception:pass
	def fN(b):
		try:
			a=str(b).rsplit("+",1)[-1];F["held"].pop(a,None)
			if F["ring_down"]==a:F["ring_down"]=None;z.add(("ring",False),dup=True);aG(r)
		except Exception:pass
	def fO():
		if F["ok"]is not None:return
		F["ok"]=False
		try:
			import clr;import System;from System.Reflection import BindingFlags;d=BindingFlags.Static|BindingFlags.Public|BindingFlags.NonPublic;e=aW("ClassicUO.Input.Keyboard");a,b=e.GetEvent("KeyDownEvent",d),e.GetEvent("KeyUpEvent",d);c=clr.GetPythonType(a.EventHandlerType)(fM);f=clr.GetPythonType(b.EventHandlerType)(fN);a.GetAddMethod(True).Invoke(None,System.Array[object]([c]))
			try:b.GetAddMethod(True).Invoke(None,System.Array[object]([f]))
			except Exception:a.GetRemoveMethod(True).Invoke(None,System.Array[object]([c]));raise
			F.update({"hooks":(a,c,b,f),"ok":True,"held":{}})
		except Exception as g:l("couldn't read the keyboard, so cell hotkeys are off (%s)."%g,Kit.HUE_BAD)
	def fP():
		a,F["hooks"]=F["hooks"],None;F["ok"]=None if a else F["ok"];F.update(map={},ring=None,ring_down=None)
		if not a:return
		import System;b,c,d,e=a;safe(lambda:b.GetRemoveMethod(True).Invoke(None,System.Array[object]([c])));safe(lambda:d.GetRemoveMethod(True).Invoke(None,System.Array[object]([e])))
	b8=set()
	def b9(what,text):
		if what not in b8:b8.add(what);l(text,Kit.HUE_BAD)
	def ar():
		c={}
		for r,d in al():
			k=_norm_key(d["k"])
			if not k or not d["t"]or not a6(r):continue
			a=ak(k)
			if a:b9((k,a),"%s belongs to %s; %s has no hotkey."%(k,a,M(r)));continue
			if k in c:b9((k,"two cells"),"%s is on two cells; %s gets it."%(k,M(r)))
			c[k]=r
		for i,k in enumerate(X()):
			if k and not ak(k):c[k]=("b",i)
		F["map"]=dict((dF(f),g)for f,g in c.items())if F["ok"]else{};b=bD();a=HOST.hotkeys_owned.get(b)if b else None
		if a:b9((b,a),"%s belongs to %s; the radial ring has no key."%(b,a))
		F["ring"]=dF(b)if b and not a and F["ok"]else None
	dG={"click":ff,"use":dD,"bag":b3,"ui":bZ,"pick":b2,"menu":b6,"mpick":fp,"picked_item":fd,"picked_bag":fe,"bindkey":e5,"lockbar":do,"grid":eW,"bagmenu":lambda i:b6(None,i),"page":lambda step:ej(b["page"]+step),"bind":lambda:bX()if a["bind"]is None else bl(),"ring":lambda down:fC()if down else fE(),"ring_bind":e4,"ring_page":fF}
	def fQ(w):a=(w-24)//3;c=Kit.wrap("Value: a spell, skill, macro or outfit name, primary or secondary, a script file, text to say, or an item graphic (0x0E21, or 0x0E21,1153 with a hue).",w-24)[:3];return(("BAR",(("check","lock","Lock in place","Keep the bar where it is (unlocked: drag its stone edge)",{"stay":True}),("check","top","Show the top row","Show the 24-cell row above the bottom row",{"stay":True,"dx":12+a}),("check","keys","Show hotkeys","Show each cell's hotkey in its corner",{"dx":12+2*a}),("check","short","Short counts","Show 1200 as 1.2k on the counters",{"stay":True}),("check","hue","Count same hue only","Count only items of the cell's hue",{"stay":True,"dx":12+a}),("custom",28,fR),("slider","slot","Cell size:","Cell side in pixels (%d-%d)"%(aY,aZ),aY,aZ,{"sw":120,"vfmt":"%d px","stay":True}),("custom",26,fS),("custom",26,fT),("slider","scale","Scale:","Size of the whole bar (%d-%d%%); text keeps its size"%(ac,ai),ac,ai,{"sw":160,"vfmt":"%d%%"}),("slider","extra","Extra rows:","Rows of %d cells above the top row (0-%d); hidden rows' hotkeys are off"%(u,a0),0,a0,{"sw":100,"vfmt":"%d","stay":True}),("custom",26,fU)),{"ldy":2,"sdy":6,"lgap":8,"ugap":10,"fh":26,"pad":6}),("RADIAL RING",[("buttons",(("radial",Kit.ART_PLAY,"Ring key: %s"%(b["radial"]or "none"),"Pick the key to hold for a ring of one page's cells (Backspace clears it)",z(("ring_bind",))),("radial_page",Kit.ART_PAGE,"Ring page: %s"%(b["radial_page"]or "shown"),"Choose the page the ring shows: the shown page or page 1-12",z(("ring_page",)))))]+[("note",d)for d in Kit.wrap("Hold the key, point at a cell and let go to use it; the middle or outside uses nothing.",w-24)]),("EDIT A CELL",[("custom",128,fV)]+[("note",f)for f in c]),("HOW TO USE",[("note",h)for g in d7 for h in Kit.wrap(g,w-24)]))
	def dH(f,by,a):return Kit.buttons(f.g,f.store,f.x+12,by,a,16)
	def bq(f,lx,a,label,key,b,c,value,tooltip):Kit.add_label(f.g,label,lx,a+2);d=[g[0]for g in c];J["dds"].append((key,lx+Kit.text_w(label)+8,a,b,[h[1]for h in c],d.index(value)if value in d else 0,tooltip));return lx+Kit.text_w(label)+8+b+16
	def fR(f,x,y):b=a["ub_found"];c=ay();e=({"open":"Bags: shown","collapsed":"Bags: folded","docked":"Bags: in the bar"}.get(c)if c else "Bags: off"if b else "Bags: not found"if b is False else "Bags: not in use");b=b or c is not None;d=(f.w-24)//3;Kit.add_label(f.g,ax(e,d-6),x+12+2*d,y+2,Kit.HUE_GOOD if b else Kit.HUE_INFO)
	def fS(f,x,y):bq(f,x+f.w-12-170-8-Kit.text_w("Bag slots:"),y,"Bag slots:","bagmode",170,list(enumerate(a5)),b["bagmode"],"Where the bag slots get bags: Inventory > Bags, bags you target, or your backpack and its bags")
	def fT(f,x,y):a=dH(f,y,(("pgprev",Kit.ART_PAGE,"Prev","Show the previous bottom-left page"),("pgnext",Kit.ART_PAGE,"Next","Show the next bottom-left page"),("bind",Kit.ART_PLAY,"Keybind mode","Start keybind mode: hover a cell and press a key")));Kit.add_label(f.g,ax("Bar page %d of %d"%(b["page"]+1,N),x+f.w-16-a),a,y+3,Kit.HUE_INFO)
	def fU(f,x,y):c=x+12+Kit.text_w("Extra rows:")+8;a=b["anchor"];d={"":"none (drop near a corner or edge middle)","L":"left edge, upright","R":"right edge, upright","T":"top edge","B":"bottom edge","C":"screen centre"}.get(a,{"TL":"top-left","TR":"top-right","BL":"bottom-left","BR":"bottom-right"}.get(a,a)+" corner");Kit.add_label(f.g,ax("Anchor: %s"%d,x+f.w-16-(c+130)),c+130,y+2,Kit.HUE_INFO)
	def fV(f,x,y):
		g,e,w=f.g,f.c,f.w;i=J["sel"];a=A(aK(i));b=bq(f,x+12,y,"Cell:","sel",120,list(enumerate(ee())),i,"The cell to edit (right-clicking a cell on the bar does the same)");b=bq(f,b,y,"Does:","does",150,a4,a["t"],"What a click or the hotkey does");bq(f,b,y,"Target:","target",100,cA,a["tg"],"Answer the cell's target cursor with yourself or your last target (when no other module holds it)");Kit.add_label(g,"Value:",x+12,y+34)
		if a["t"]=="item":c=("0x%04X"%a["g"])+((",%d"%a["h"])if a["h"]else "")
		elif a["t"]=="ui":c=""
		elif a["t"]=="travel":c=aL(a)
		else:c=a["v"]
		d=x+12+max(Kit.text_w("Value:"),Kit.text_w("Window:"))+8;e["value"]=Kit.with_tip(Kit.add_textbox(g,c,d,y+32,x+w-16-d,numbers=False),"The cell's value (see below; a Client window cell uses Window)");Kit.add_label(g,"Window:",x+12,y+66);j=cG();k=[s[0]for s in j];J["dds"].append(("window",d,y+64,140,[t[1]for t in j],k.index(a["v"])if a["t"]=="ui"and a["v"]in k else 0,"The client or module window a Client window cell opens"));b=d+140+16
		for m,h,n,l,o,p in(("key","Hotkey:",a["k"],100,False,b5["hotkey"]+"; or use Keybind mode"),("lo","Red at:",str(a["lo"]),40,True,b5["lo"])):Kit.add_label(g,h,b,y+66);e[m]=Kit.with_tip(Kit.add_textbox(g,n,b+Kit.text_w(h)+8,y+64,l,numbers=o),p);b+=Kit.text_w(h)+8+l+16
		q=dH(f,y+96,(("apply",Kit.ART_OK,"Apply","Save this cell"),("pick",Kit.ART_PLAY,"Pick item...","Target an item for this cell"),("clear",Kit.ART_CLOSE,"Clear","Empty this cell")));e["status"]=Kit.add_label(g,"",q,y+99,Kit.HUE_INFO)
	def fW(g,x,y,w):
		if not B["a"]:cM()
		J["dds"]=[];f=T.build(g,x,y,w)
		for c,e,h,i,j,k,l in sorted(J["dds"],key=lambda d:-d[2]):a=G.CreateDropDown(i,j,k);a.SetPos(e,h);g.Add(a);f.c[c]=Kit.with_tip(a,l)
		J.update({"seen_sel":J["sel"],"seen_bag":b["bagmode"]})
	def aE(text,hue=None):
		if T.f is not None:Kit.set_text(T.f.c["status"],text,Kit.HUE_INFO if hue is None else hue)
	def fX():
		d=T.f.c;e=aK(J["sel"]);a=A(e)
		def f(a,dd):return a[max(0,min(len(a)-1,Kit.dd_index(dd,0)))][0]
		t=f(a4,d["does"]);v=str(d["value"].Text or "").strip();i=f(cA,d["target"]);k=_norm_key(d["key"].Text);g=ak(k)
		if g:aE("%s belongs to %s"%(k,g),Kit.HUE_BAD);return
		try:h=int(str(d["lo"].Text or "0"))
		except Exception:h=cm
		b=dict(V(),t=t,tg=i,k=k,lo=h)
		if t=="item":
			c=ec(v)
			if c is None and a["t"]=="item"and a["g"]:c=(a["g"],a["h"])
			if c is None:aE("Pick an item, or type its graphic",Kit.HUE_BAD);return
			b.update({"g":c[0],"h":c[1],"n":a["n"]if(a["g"],a["h"])==c else "0x%04X"%c[0]})
		elif t=="ui":b["v"]=f(cG(),d["window"])
		elif t=="ability":b["v"]="secondary"if v.lower().startswith("s")else "primary"
		elif t=="travel":
			if a["t"]!="travel":aE("Pick its destination: right-click the cell, then Travel (runebook)",Kit.HUE_BAD);return
			b["tg"]=""
			for k in("v","n")+bB:b[k]=a.get(k,"")
		elif t:
			if not v:aE("Type a value first",Kit.HUE_BAD);return
			b["v"]=v
		B[e[0]][e[1]]=b
		if b["k"]and b["k"]!=_norm_key(a["k"]):bY(e,b["k"])
		an(recount=True,refresh=False,refs=[e]);aE("Saved %s"%M(e),Kit.HUE_GOOD)
	def fY(f):
		for a,b in(("pgprev",("page",-1)),("pgnext",("page",1)),("bind",("bind",))):
			if Kit.was_clicked(f.store,a):z(b)()
		if Kit.was_clicked(f.store,"apply"):fX()
		if Kit.was_clicked(f.store,"pick"):z(("pick",aK(J["sel"])))();aE("Target the item")
		if Kit.was_clicked(f.store,"clear"):cZ(aK(J["sel"]))
	def fZ(f,new):
		a=Kit.dd_index(f.c["bagmode"],b["bagmode"])
		if a!=J["seen_bag"]and 0<=a<len(a5):J["seen_bag"]=new["bagmode"]=a
		c=Kit.dd_index(f.c["sel"],J["sel"])
		if c!=J["seen_sel"]and 0<=c<P+D+aI:J["sel"]=c;ab(r)
	def f_(old,new):
		if new["bagmode"]!=old["bagmode"]:a["bag_sig"],a["next_scan"]=None,0.
		ar();ag(.4)
	T=Kit.Page(b,fQ,Q,f_,adjust=fZ,clicks=fY,every=.2);cL()
	def f0():
		a.update(cC(),minimized=Kit.load_min(bv),em=False,ub_last=None,ub_pending=True,counted_at=0.);b8.clear();F.update(held={},ring_down=None);C.update(scale=None,vertical=None,slot=None,sig=None);cL();cM();cV();a["ub_state"],a["grim_state"],a["va_state"]=ay(),a8(),bH();HOST.layout_add(r,eZ,aH,eE);aj.add(HOST.layout_remove,r);b=HOST.layout_slot(r)if HOST.booting()else None
		if b and b[0]and b[1]:c1(b[0],b[1],None)
		a.update(dock_sig=cS(),tray_sig=cT(),watch_next=0.,owned_sig=frozenset(HOST.hotkeys_owned));dj();Z();a.update(rebuild_at=0.,redraw=set());fO();ar();aj.service("actionbar.hotkeys",ez);aj.service("look.actionbar",ag);aj.service("actionbar.find",fI);aj.service("actionbar.use",fJ);aj.add(bp)
	def f1():
		if a["shutting"]or e["g"]is None:return
		if Kit.closed(e):return
		c=time.time();fc(c);e8(c);el()
		if a["minimized"]and a["em"]==Kit.zone_up(r)and not a["rebuild_at"]:ag()
		h=bs()
		if h!=e.get("arranging",False):
			e["arranging"]=h
			if e.get("lockbtn"):bj(e["lockbtn"],*bW())
		while a["queue"]:
			d=a["queue"].pop(0);f=d[0]
			if f in dG:dG[f](*d[1:])
			elif f=="dock":
				g=dict(bJ()).get(d[1])
				if g is not None:
					s=safe(g.get("state"))
					if s is None:
						if g.get("on"):safe(g["on"])
						else:W(lambda k=d[1]:safe(lambda:br(k)))
					elif s=="open":cd(d[1])
					else:safe(g.get("show"))
					a["dock_sig"],a["watch_next"]=None,0.
			elif f=="traywin":b["tray_open"]=not b["tray_open"];Q();dc()
			elif f=="toggle_min":
				if Kit.zone_up(r)and not a["minimized"]:continue
				aO();a["minimized"]=not a["minimized"];Kit.save_min(bv,a["minimized"]);Z();ag()
			if a["shutting"]or e["g"]is None:return
		c=time.time()
		if E["g"]is not None:fD(c)
		if c>=a["next_scan"]:
			a["next_scan"]=c+2.;cV();eo();Z()
			if a.get("last_pos")!=a.get("pos_saved"):aO()
		if a["rebuild_at"]and c>=a["rebuild_at"]:a["rebuild_at"]=0.;a["redraw"]=set();dj()
		elif a["redraw"]:e_()
		if c>=a["next_count"]or(a.get("pack_v")is not None and c-a.get("counted_at",0.)>=dO and ch()!=a["pack_v"]):a["next_count"]=c+bw;ep()
		ex(c)
		if c>=a.get("tray_next",0.):a["tray_next"]=c+.1;e1(c)
	def f2():
		while a["jobs"]and not a["shutting"]:a["jobs"].pop(0)()
	def f3():
		a["shutting"]=True;aj.close();aV();g,U["g"]=U["g"],None;Kit.dispose(g);a["bind"]=None;aq();Z(False);fP()
		with Kit.quiet:Kit.on_client(aO)
		Kit.save_min(bv,a["minimized"]);Q();aN();g,e["g"]=e["g"],None;Kit.dispose(g)
		for s in e.pop("stale",[]):Kit.dispose(s)
	return{"start":f0,"tick":f1,"stop":f3,"client_tick":True,"config_height":T.height,"build_config":fW,"poll_config":T.poll,"config_closed":T.closed,"thread_tick":f2,"thread_wanted":lambda:bool(a["jobs"])}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("actionbar","Action Bar","Cells for items, spells, skills and windows",_module_actionbar,.05,category="On screen")
