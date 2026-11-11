def _module_actionbar():
	be=Client._type;aT=Client.on_client_thread;cD=HOST.aborting;cE=HOST.cursor_busy;cF=HOST.dock_forget;cG=HOST.dock_to_bar;bN=HOST.enable;bO=HOST.layout_arranging;cH=HOST.layout_in_use;cI=HOST.layout_locked;cJ=HOST.layout_need;cK=HOST.pack_ver;aU=HOST.poke;an=HOST.refresh_settings;cL=HOST.release_typing;bf=HOST.show_settings;bP=HOST.typing;cM=Kit.ART_CLOSE;aV=Kit.ART_MIN;cN=Kit.ART_OK;aW=Kit.ART_PAGE;bQ=Kit.ART_PLAY;bR=Kit.ART_RESTORE;u=Kit.HUE_BAD;W=Kit.HUE_GOOD;J=Kit.HUE_INFO;X=Kit.HUE_TEXT;ae=Kit.HUE_TITLE;cO=Kit.STONE_TILE;cP=Kit.add_box;I=Kit.add_label;cQ=Kit.add_section;bS=Kit.add_textbox;Y=Kit.add_tiled;bT=Kit.add_window_frame;cR=Kit.anchor_pos;af=Kit.art_button;aF=Kit.catcher;bU=Kit.dd_index;V=Kit.dispose;bV=Kit.find_item;bW=Kit.fit;bg=Kit.get_var;aX=Kit.gold_box;K=Kit.is_open;cS=Kit.load_pos;aY=Kit.mouse_pos;cT=Kit.moved_by_code;cU=Kit.on_client;aG=Kit.pic_size;bX=Kit.place;aH=Kit.pos;bY=Kit.put_var;cV=Kit.save_min;bh=Kit.screen;aI=Kit.set_text;bZ=Kit.spell_info;cW=Kit.text_px;M=Kit.text_w;b_=Kit.ui_pos;bi=Kit.was_clicked;av=Kit.with_tip;bj=Kit.wrap;ag=Kit.zone_up;r="actionbar";aZ="Action Bar";cX="ActionBar_settings";b0="ActionBar_pos";b1="ActionBar_min";z=24;N=12;E=11;O=5;Z=z+N;T=12;ei=22;bk,bl=36,64;ao,aw=50,150;ej=8;ek=44;cY=.65;el=4;em=3;en=30;ap=4;aq=2624;ar=.92;b2=.75;cZ=2.;c_=5;eo=.1;aJ=("r",0);ep=10.;c0=20;eq=70;er=16;es="#E8B830";c1=set(("clumsy|feeblemind|magic arrow|weaken|harm|fireball|poison|curse|lightning|mana drain|mind blast|paralyze|dispel|energy bolt|explosion|mass curse|chain lightning|flamestrike|mana vampire|meteor swarm|earthquake|mass dispel|paralyze field").split("|"));et=[("recall","Recall (spell)"),("gate","Gate Travel (spell)"),("charge","Recall (a book charge)"),("recall_scroll","Recall scroll"),("gate_scroll","Gate Travel scroll"),("sacred","Sacred Journey (spell)")];eu={"recall":"Recall","gate":"Gate","charge":"Recall (charge)","recall_scroll":"Recall scroll","gate_scroll":"Gate scroll","sacred":"Sacred Journey"};bm={"recall_scroll":8012,"gate_scroll":8032};c2={"charge":8901,"recall_scroll":8012,"gate_scroll":8032};c3={"recall":"Recall","gate":"Gate Travel","sacred":"Sacred Journey"};aK="bag";c4="ActionBar_alive";c5="grimoire";ev="Grimoire_cmd";ew="VirtueAssistant_cmd";c6="ActionBar_cells";c7="ActionBar_pages";c8="ActionBar_extra";bn=4;a_=bn*z;c9,da=240,46;b3=[("paperdoll","Paperdoll",7939,"paperdoll"),("status","Status",3852,"ga:OpenStatusBar"),("journal","Journal",4080,"ga:OpenJournal:ResizableJournal"),("skills","Skills",5091,"ga:OpenSkills"),("spellbook","Grimoire",3834,"grimoire"),("worldmap","World map",5355,"ga:OpenWorldMap"),("minimap","Mini map",5365,"ga:OpenMiniMap"),("quests","Quest log",3636,"quests"),("guild","Guild",7030,"ga:OpenGuildGump"),("party","Party",7956,"macro:PartyManifest"),("chat","Chat",3639,"ga:OpenChat"),("options","Options",7864,"ga:OpenSettings"),("help","Help",4079,"help"),("war","War / peace",5119,"war"),("barsettings","Bar settings",4031,"barsettings"),("virtue","Virtue Assistant",4179,"virtue"),("launcher","Launcher",3630,"launcher"),("lock","Lock / unlock bar",4111,"lock"),("minimize","Minimize bar",0,"minimize"),];db=(3834,8787,8786,9100,9120,11600,11677);ex={"paperdoll":"Open your paperdoll","status":"Open the status bar","journal":"Open the journal","skills":"Open the skills window","worldmap":"Open TazUO's World Map","minimap":"Open the mini map","quests":"Open the quest log","guild":"Open the guild window","party":"Open the party window","chat":"Open the chat window","options":"Open the client's options","help":"Open the help menu","war":"Switch war and peace mode","barsettings":"Open the Action Bar settings page","lock":"Lock or unlock the bar","minimize":"Minimize the bar","launcher":"Open the Quick Launcher"};b4="paperdoll status skills spellbook guild chat minimap worldmap options barsettings virtue".split();ey=["paperdoll","status","journal","skills","spellbook","worldmap","minimap","quests","options","barsettings","virtue"];bo=16;Q=2;ez=("Anatomy|Animal Lore|Animal Taming|Arms Lore|Begging|Cartography|Detect Hidden|Discordance|Evaluate Intelligence|Forensic Evaluation|Hiding|Inscription|Item Identification|Meditation|Peacemaking|Poisoning|Provocation|Remove Trap|Spirit Speak|Stealing|Stealth|Taste Identification|Tracking").split("|");eA=["Magery","Necromancy","Chivalry","Bushido","Ninjitsu","Spellweaving","Mysticism"];bp=16;b5=4;bq=20;br=[("","Empty"),("item","Item + counter"),("spell","Spell"),("skill","Skill"),("macro","TazUO macro"),("ability","Weapon ability"),("script","Legion script"),("dress","Dress outfit"),("undress","Undress outfit"),("say","Say text"),("ui","Client window"),("travel","Travel (runebook)")];b6=("rb","ri","rm");dc=[("","None"),("self","Self"),("last","Last target")];bs=["Bags' slots","Bags I pick","Backpack + sub-bags"];de=((2240,"|".join(gv for gv,gy in Kit.MAGERY)),(20480,"Animate Dead|Blood Oath|Corpse Skin|Curse Weapon|Evil Omen|Horrific Beast|Lich Form|Mind Rot|Pain Spike|Poison Strike|Strangle|Summon Familiar|Vampiric Embrace|Vengeful Spirit|Wither|Wraith Form|Exorcism"),(20736,"Cleanse by Fire|Close Wounds|Consecrate Weapon|Dispel Evil|Divine Fury|Enemy of One|Holy Light|Noble Sacrifice|Remove Curse|Sacred Journey"),(21536,"Honorable Execution|Confidence|Evasion|Counter Attack|Lightning Strike|Momentum Strike"),(21280,"Focus Attack|Death Strike|Animal Form|Ki Attack|Surprise Attack|Backstab|Shadowjump|Mirror Image"),(23000,"Arcane Circle|Gift of Renewal|Immolating Weapon|Attune Weapon|Thunderstorm|Nature's Fury|Summon Fey|Summon Fiend|Reaper Form|Wildfire|Essence of Wind|Dryad Allure|Ethereal Voyage|Word of Death|Gift of Life|Arcane Empowerment"),(24000,"Nether Bolt|Healing Stone|Purge Magic|Enchant|Sleep|Eagle Strike|Animated Weapon|Stone Form|Spell Trigger|Mass Sleep|Cleansing Winds|Bombard|Spell Plague|Hail Storm|Nether Cyclone|Rising Colossus"),);eB=["Click a cell to use it; right-click it (Shift+click when right-clicks don't reach the bar) to choose what it holds: an item (counted in your pack), spell, skill, weapon ability, TazUO macro, Legion script, outfit, text to say, window or runebook destination, plus its hotkey and target.","Click an empty cell to target an item for it.","The 12 bottom-left cells have 12 pages, each with its own cells and hotkeys: the tiny arrows and the number switch pages.","Keys (far right) starts keybind mode: hover a cell, window button or bag slot and press a key; Esc ends it, Backspace clears a key. Lock locks the bar (with zones, toggles Arrange mode); Grid shows the snap grid.","Drag the bar by its stone edge; drop it near a corner, edge middle or the centre to anchor it there (upright on the left or right edge).","Bag slots show the bags of Inventory > Bags: click to show the Bags window, again to fold it into the bar; right-click for its settings. With Bags I pick, click an empty slot to target a bag.","The Grimoire and Virtue Assistant buttons show their window (turning Grimoire on); click again to fold it into the bar.","A Module windows button (page 2 of the Client window list) turns that module on and shows its window; click again to fold it into the tray beside the bar. The bar's numbered button hides or shows the tray.","A Travel (runebook) cell goes to a runebook destination by Recall, Gate Travel, a book charge, a scroll or Sacred Journey, through Grimoire (must be on); its counter shows charges or scrolls.","A used skill or spell darkens the cells of that kind while they count down; a spell cell greys out while a reagent it needs is at 0. Red at: when an item's counter turns red.","Radial ring: hold its key to show one page's cells round the mouse, point at one and let go to use it; the middle or outside uses nothing."];b={"slot":44,"top":True,"keys":True,"lock":False,"short":True,"hue":False,"bagmode":0,"bags":"","page":0,"scale":100,"tray_open":True,"bagkeys":"","extra":0,"anchor":"","vertical":False,"radial":"","radial_page":0};gt=dict(b);C={"a":[],"u":[],"x":[],"pages":[]}
	def df():return{"shutting":False,"queue":[],"want_target":None,"next_count":0.,"next_scan":0.,"rebuild_at":0.,"bag_sig":None,"ability_sig":None,"bind":None,"jobs":[],"redraw":set(),"ub_job":False,"cool":{"skill":0.,"spell":0.},"cool_next":0.}
	a={"minimized":False,"shutting":False,"docked":False,"queue":[],"em":False,"ub_pending":False,"cnt":{},"cnt_g":{},"first":{},"first_g":{},"bags":[None]*O,"ub_found":None,"ub_cache":None,"ub_state":None,"grim_state":None,"va_state":None,"pending_on":None,"right_ok":None,"dock_sig":None,"watch_next":0.,"script_check":None,"ub_last":None};a.update(df());e={"g":None,"c":{},"store":({},{}),"cells":{},"bags":{}};ax,A,l=Kit.basics(a,aZ);ac={"g":None,"at":None};j={"g":None,"ref":None,"level":"cats","cat":None,"page":0,"c":{},"bag":None,"items":[],"anchor":None,"moved":None,"placed":None};P={"sel":Z-N,"dds":[]};b7=dict((gC.lower(),gz+gB)for gz,gA in de for gB,gC in enumerate(gA.split("|")))
	def ah(fn):a["jobs"].append(fn)
	def dg(name):
		n=(name or "").strip().lower()
		if not n:return 0
		a=b7.get(n)
		if a is None:a=next((d for c,d in b7.items()if c.startswith(n)),None)
		return a if a and aG(a)[0]>0 else 0
	def eC(f):
		d=[str(g)for g in(API.CurrentAbilityNames()or[])];i=1 if f=="secondary"else 0
		if len(d)<=i:return 0,""
		a=d[i];b=[str(h)for h in(API.KnownAbilityNames()or[])]
		if a not in b:return 0,a
		c=b.index(a)
		if b and b[0].lower()in("none","invalid"):c-=1
		e=20992+c;return(e if c>=0 and aG(e)[0]>0 else 0),a
	def a0(uid):
		if uid.startswith("mod:"):return dh(uid[4:])
		return next((c for c in b3 if c[0]==uid),None)
	def dh(key,a=None):
		s=HOST.by_key.get(key)
		if s is None or key==r:return
		d=(a if a is not None else dict(HOST.docks)).get(key);b=int(d.get("icon")or 0)if d else 0;return("mod:"+key,s.title,b,"mod:"+key)
	def di():
		b=[];c=dict(HOST.docks)
		for a in HOST.slots:
			e=[g[4][0]if len(g)>4 and g[4]else "%s.%s"%(a.key,g[0])for g in a.parts]
			for f in e or[a.key]:
				d=dh(f,c)
				if d is not None:b.append(d)
		return b
	def dj():return b3+di()
	def eD(key):
		s=HOST.by_key.get(key)
		if s is None:return "Module '%s' (not loaded)"%key
		d=dict(HOST.docks).get(key)
		if not s.running:return "Turn %s on"%s.title
		if d is None:return "Turn %s off"%s.title
		if safe(d.get("state"))=="open":return "Fold %s into the bar"%s.title
		return "Show %s"%s.title
	def eE(key):
		s=HOST.by_key.get(key)
		if s is None:l("no module '%s'."%key,u);return False
		d=dict(HOST.docks).get(key)
		if not s.running:
			cF(key)
			def a(k=key,title=s.title):
				bN(k)
				if not HOST.by_key[k].running:l("%s couldn't be turned on."%title,u)
			ah(a);return True
		if d is None:HOST.disable(key);return True
		if safe(d.get("state"))=="open":cG(key,s.title)
		else:safe(d.get("show"));cF(key)
		return True
	def ay(k):k=_norm_key(k);return HOST.hotkeys_owned.get(k)or("the radial ring"if k and k==b8()else None)
	def b8():return _norm_key(b["radial"])
	def dk():return set(_norm_key(d["k"])for f,d in az()if d["k"]and d["t"])|set(c for c in aj()if c)
	def ai(text,width):return bW(str(text),width,".")
	def dl(k):return(k.upper().replace("CTRL+","C").replace("SHIFT+","S").replace("ALT+","A").replace("NUMPAD","N").replace("KP_","N"))
	def dm(n):
		if b["short"]:
			if n>=10000:return "%dk"%(n//1000)
			if n>=1000:return "%.1fk"%(n/1000.)
		return str(n)
	def eF(text):
		t=(text or "").strip()
		if not t:return
		a,b=[c.strip()for c in(t.split(",",1)+[""])[:2]]
		try:return(int(a,16)if a.lower().startswith("0x")else int(a),(int(b,16)if b.lower().startswith("0x")else int(b))if b else 0)
		except Exception:return
	def ad():return{"t":"","v":"","g":0,"h":0,"tg":"","k":"","lo":c_,"n":""}
	def B(ref):
		if ref[0]!="p":return C[ref[0]][ref[1]]
		a,i=divmod(ref[1],N);return C["a"][z+i]if a==b["page"]else C["pages"][a][i]
	def aj():a=[_norm_key(c)for c in b["bagkeys"].split(",")];return(a+[""]*O)[:O]
	def b9(ref,k):
		if ref==aJ:b["radial"]=_norm_key(k);aa();an(r)
		elif ref[0]=="b":a=aj();a[ref[1]]=k;b["bagkeys"]=",".join(a);aa()
		else:B(ref)["k"]=k;a4()
	def S(ref):
		a,i=ref
		if a=="b":return "bag slot %d"%(i+1)
		if a=="r":return "the radial ring"
		if a=="p":return "page %d cell %d"%(i//N+1,i%N+1)
		if a=="u":return "button %d"%(i+1)
		if a=="x":return "row %d cell %d"%(i//z+2,i%z+1)
		if i<z:return "top cell %d"%(i+1)
		return "page %d cell %d"%(b["page"]+1,i-z+1)
	def a1(idx):
		if idx<Z:return("a",idx)
		if idx<Z+E:return("u",idx-Z)
		return("x",idx-Z-E)
	def eG(ref):
		if ref[0]=="a":return ref[1]
		if ref[0]=="u":return Z+ref[1]
		return Z+E+ref[1]
	def eH():return(["Top %d"%(c+1)for c in range(z)]+["Bottom %d"%(d+1)for d in range(N)]+["Button %d"%(f+1)for f in range(E)]+["Row %d-%d"%(g//z+2,g%z+1)for g in range(a_)])
	def bt(ref):
		a,i=ref
		if a=="x":return i<b["extra"]*z
		if a=="a":return b["top"]or i>=z
		return True
	def az():return[((d,f),g)for d in "aux"for f,g in enumerate(C[d])]
	def eI():
		a=[ad()for f in range(Z)];b=[(3617,"Bandages","self"),(3852,"Heal potion",""),(3847,"Cure potion",""),(3851,"Refresh potion","")]
		for i,(c,n,d)in enumerate(b):a[z+i].update({"t":"item","g":c,"n":n,"tg":d})
		u=[ad()for g in range(E)]
		for i,e in enumerate(b4[:E]):u[i].update({"t":"ui","v":e})
		return a,u
	def ak(c):
		t,v=c["t"],c["v"]
		if t=="item":return c["n"]or("0x%04X"%c["g"])
		if t=="ui":d=a0(v);return d[1]if d else v
		if t=="ability":return "Secondary"if v=="secondary"else "Primary"
		if t=="script":return v.replace("\\","/").split("/")[-1].rsplit(".",1)[0]
		return v
	def a2(c):return "%s to %s%s"%(eu.get(c.get("rm"),"Travel"),c["v"]or "?",(" (%s)"%c["n"])if c["n"]else "")
	def a3(ref):
		c=B(ref);t=c["t"]
		if not t:
			if ref[0]in("a","x"):return "Empty: click to target an item; right-click for a spell, skill or more"
			return "Empty: right-click to choose what it does"
		if t=="travel":
			b=a2(c)
			if HOST.services.get("grimoire.travel")is None:b="Grimoire is off: turn it on to use this cell\n"+b
			if c["k"]:b+="  [%s]"%c["k"]
			return b+"\nRight-click to change"
		d=ak(c)
		if t=="ui"and c["v"]=="spellbook":d={"open":"Fold Grimoire into the bar","minimized":"Show Grimoire","docked":"Show Grimoire"}.get(a["grim_state"],"Open Grimoire (turns it on)")
		elif t=="ui"and c["v"]=="virtue":d={"open":"Fold Virtue Assistant into the bar","gear":"Open the Virtue Assistant window","docked":"Open the Virtue Assistant window"}.get(a["va_state"],"Virtue Assistant (not running)")
		elif t=="ui"and c["v"].startswith("mod:"):d=eD(c["v"][4:])
		elif t=="ui":d=ex.get(c["v"],d)
		b={"item":"Use %s","spell":"Cast %s","skill":"Use %s","macro":"Run macro %s","ability":"Use the %s ability","script":"Start or stop script %s","dress":"Dress %s","undress":"Undress %s","say":"Say \"%s\"","ui":"%s"}.get(t,"%s")%d
		if c["tg"]:b+=", then target %s"%("yourself"if c["tg"]=="self"else "last target")
		if c["k"]:b+="  [%s]"%c["k"]
		if t=="spell":
			e=dB(c["v"])
			if e is not None:b+="\nOut of %s"%e[1]
		return b+"\nRight-click to change"
	def eJ(s):return(str(s).replace("%","%25").replace("&","%26").replace("=","%3D").replace(";","%3B").replace("|","%7C"))
	def eK(s):return(s.replace("%7C","|").replace("%3B",";").replace("%3D","=").replace("%26","&").replace("%25","%"))
	def dn(d):return "&".join("%s=%s"%(c,eJ(f))for c,f in d.items())
	def do(s):return dict((c,eK(d))for c,d in(f.split("=",1)for f in s.split("&")if "="in f))
	def dp():
		d=do(bg(cX))
		for k in("top","keys","lock","short","hue","tray_open","vertical"):
			if k in d:b[k]=d[k]=="1"
		for k,c,e in(("slot",bk,bl),("bagmode",0,len(bs)-1),("page",0,T-1),("scale",ao,aw),("extra",0,bn),("radial_page",0,T)):
			with Kit.quiet:b[k]=int(d[k])
			b[k]=max(c,min(e,b[k]))
		a=d.get("anchor","");b["anchor"]=a if a in Kit.ANCHORS else ""
		for k in("bags","bagkeys","radial"):b[k]=d.get(k,b[k])
	def aa():bY(cX,dn(dict((d,("1"if c else "0")if isinstance(c,bool)else c)for d,c in b.items())))
	def eL(d):
		c=ad()
		for k in("t","v","tg","k","n"):c[k]=d.get(k,c[k])
		for k in("g","h","lo"):
			with Kit.quiet:c[k]=int(d.get(k,c[k]))
		if c["t"]=="travel":
			for k in b6:c[k]=d.get(k,"")
		return c
	def bu(raw,n,a=True):b=[eL(do(c))for c in raw.split(";")if c or not a];return(b+[ad()for d in range(n)])[:n]
	def dq():
		ca.clear();a,u=eI();e=bg(c6)
		if "|"in e:
			h,i=e.split("|",1);a=bu(h,Z,False);u=bu(i,E,False);j=set(o["v"]for o in u if o["t"]=="ui");f=[p for p in b4 if p not in j]
			for c in u:
				if c["t"]=="ui"and a0(c["v"])is None and not c["v"].startswith("mod:"):
					c.update(ad())
					if f:c.update({"t":"ui","v":f.pop(0)})
			if[q["v"]if q["t"]=="ui"else None for q in u]==ey[:E]:
				for k,l in enumerate(b4[:E]):u[k].update({"t":"ui","v":l})
		d=[[ad()for t in range(N)]for s in range(T)];g=bg(c7)
		if g:
			for m,n in enumerate(g.split("|")[:T]):d[m]=bu(n,N)
		else:d[0]=a[z:];b["page"]=0
		a[z:]=d[b["page"]];C["x"]=bu(bg(c8),a_);C["a"],C["u"],C["pages"]=a,u,d;cf()
	def dr():
		if C["pages"]:C["pages"][b["page"]]=list(C["a"][z:])
	ca={}
	def a4():
		dr();cf()
		def a(a):return ";".join(dn(d)for d in a)
		for b,c in((c6,a(C["a"])+"|"+a(C["u"])),(c7,"|".join(a(f)for f in C["pages"])),(c8,a(C["x"]))):
			if ca.get(b)!=c:bY(b,c);ca[b]=c
	def eM(p):
		p=p%T
		if p==b["page"]:return
		dr();b["page"]=p;C["a"][z:]=C["pages"][p];cf();aa();aE();a["next_count"]=0.;aR([("a",z+d)for d in range(N)]);fg();an(r);c=j.get("ref")
		if j.get("g")is not None and c and c[0]=="a"and c[1]>=z:aD()
	def ds():
		a=[0]*O
		for i,p in enumerate(b["bags"].split(",")[:O]):
			try:a[i]=int(p,16)if p.strip()else 0
			except Exception:a[i]=0
		return a
	def dt(i,serial):a=ds();a[i]=serial;b["bags"]=",".join(("%X"%c)if c else ""for c in a);aa()
	def a5():
		if ag(r):return
		p=aH(e["g"])if K(e["g"])else None
		if p is not None and p!=a.get("pos_saved"):a["pos_saved"]=p;bY(b0,"%d,%d"%p)
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
			ClientUI.looked=True;a=ClientUI.world=safe(lambda:ClientUI._get(API,"World"));ClientUI.GA=be("ClassicUO.Game.GameActions");ClientUI.UIM=be("ClassicUO.Game.Managers.UIManager")
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
	def du():return Kit.data_path("_unified_bag_%d.cfg"%int(safe(lambda:API.Player.Serial,0)or 0))
	def dv(path):
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
	def eN():
		if not aT():a["ub_last"],a["ub_pending"]=dv(du()),False
		elif not a["ub_job"]:
			a["ub_job"]=True;b=du()
			def c():
				a["ub_job"]=False;c=dv(b)
				if c!=a["ub_last"]or a["ub_pending"]:a["ub_last"],a["ub_pending"]=c,False;a["next_scan"]=0.
			ah(c)
		return None if a["ub_last"]is None else list(a["ub_last"])
	def cb(a,b):s=API.GetSharedVar(a);return str(s)if s is not None and str(s)in b else None
	def aL():return cb("UnifiedBag_state",("open","collapsed","docked"))
	def bv():return cb("Grimoire_state",("open","minimized","docked"))
	def cc():return cb("VirtueAssistant_state",("open","gear","docked"))
	def cd(cmd):API.SetSharedVar("UnifiedBag_cmd",cmd)
	def ce():return list(HOST.docks)
	def bw():return[(f,c)for f,c in ce()if c.get("always")or safe(c.get("state"))=="docked"]
	def dw():return tuple([(c,safe(f.get("state")))for c,f in ce()])
	def dx():return tuple([(f,c.get("icon"),safe(c.get("state"))if c.get("always")else None)for f,c in bw()])
	def al(on=True):
		if on and not a["em"]:API.SetSharedVar(c4,time.time())
		else:API.RemoveSharedVar(c4)
	def eO():
		f=time.time()
		if f<a["watch_next"]:return
		a["watch_next"]=f+.25;c=False
		for k,s,i in(("ub_state",aL(),b["bagmode"]==0),("grim_state",bv(),True),("va_state",cc(),True)):
			if s!=a[k]:a[k]=s;c=c or i
		if c:dN()
		d=dw()
		if d!=a["dock_sig"]:
			j=set(o for o,q in(a["dock_sig"]or()));a["dock_sig"]=d;g=dx()
			if g!=a.get("tray_sig"):a["tray_sig"]=g;dO()
			h=[v for v,t in az()if t["t"]=="ui"and t["v"].startswith("mod:")]
			if h:
				if set(w for w,x in d)!=j:aR(h)
				else:dN()
		e=frozenset(HOST.hotkeys_owned)
		if e!=a.get("owned_sig"):
			m=e^(a.get("owned_sig")or frozenset());a["owned_sig"]=e
			if m&dk():aE()
		p=a["pending_on"]
		if p and time.time()>p[2]:
			a["pending_on"]=None;n=aL()if p[0]==aK else bv()
			if n is None:
				l("%s didn't start; is Virtue Assistant running?"%p[1],u)
				if p[3]is not None:p[3]()
	def bx(key,title,fallback=None):
		if key in HOST.by_key:ah(lambda:bN(key))
		else:API.SetSharedVar("VirtueAssistant_enable",key)
		l("turning %s on."%title);a["pending_on"]=(key,title,time.time()+4.,fallback)
	def eP():
		a=bv();al()
		if a in("minimized","docked","open"):API.SetSharedVar(ev,"dock"if a=="open"else "show")
		else:bx(c5,"Grimoire",fs)
		return True
	def eQ():
		a=cc();al()
		if a not in("open","gear","docked"):l("Virtue Assistant isn't running.",u);return False
		API.SetSharedVar(ew,"dock"if a=="open"else "show");return True
	def dy():
		a=[];b=int(API.Backpack or 0)
		if b:a.append(b)
		for c in(API.ItemsInContainer(b,False)or[]):
			if len(a)>=O:break
			with Kit.quiet:
				if c.IsContainer:a.append(int(c.Serial))
		return a
	def dz():
		h=b["bagmode"]
		if h==0:
			c=eN()
			if c is None and a["ub_pending"]:c=[]
			else:
				a["ub_found"]=c is not None
				if c is None:c=dy()
		elif h==1:c=ds()
		else:c=dy()
		d,g=[],[]
		for s in(list(c)+[0]*O)[:O]:
			if not s:d.append(None);g.append(None);continue
			e=bV(s);g.append(e)
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
			a["bags"],a["bag_sig"]=d,k;aR([("b",n)for n in range(O)])
	def aM(i):return a["bags"][i]if i<len(a["bags"])else None
	aA={"types":None}
	def cf():aA["types"]=None
	def a6():
		if aA["types"]is None:
			b=C["a"]+C["u"]+C["x"];aA["types"]=set(g["t"]for g in b);aA["items"]=set(h["g"]for h in b if h["t"]=="item");d,e=set(),set();a={"skill":[],"spell":[]}
			for f,c in az():
				if c["t"]=="spell":d.update(i[1]for i in dA(c["v"]));a["spell"].append(f)
				elif c["t"]=="skill":a["skill"].append(f)
				elif c["t"]=="travel"and c.get("rm")in bm:e.add(bm[c["rm"]])
			aA["extra"],aA["refs"]=frozenset(d|e),a
		return aA
	def eR():
		if "ability"not in a6()["types"]:return
		b=tuple([str(d)for d in(API.CurrentAbilityNames()or[])])
		if b!=a["ability_sig"]:a["ability_sig"]=b;aR([f for f,g in az()if g["t"]=="ability"])
	def a7(extra=(),max_age=0.):
		o=cK()
		try:p=HOST.pack_items(deep=True,max_age=max_age);q=int(API.Backpack or 0)
		except Exception:return
		k=a6();d=k["items"]
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
	def cg(info,lbl,text,hue):
		if info.get("txt")!=text:
			info["txt"]=text
			try:lbl.Text=text;b_(lbl,info["x"]+info["w"]-cW(text)-3,info["y"]+info["h"]-16)
			except Exception:pass
		if info.get("hue")!=hue:info["hue"]=hue;Kit.set(lbl,"Hue",hue)
	def eS():
		if a["em"]:return
		k=a6()
		if "item"in k["types"]or k["extra"]:a7(max_age=.5)
		else:a["pack_v"]=None
		a9()
	a8=[None]
	def a9():
		l=time.time();r=a["cool"];m=False;i=a8[0]
		if i is None:i=[(x,w,w["count"])for x,w in e["cells"].items()if w.get("count")is not None];a8[0]=i
		for p,g,j in i:
			c=B(p);t,v=c["t"],c["v"];d,f="",X;h=r.get(t)
			if h and l<h:d,f=dC(h-l),ae
			elif t=="item":n=a["cnt"].get((c["g"],c["h"]),0)if b["hue"]else a["cnt_g"].get(c["g"],0);d=dm(n);f=u if n<=max(0,c["lo"])else X
			elif t in("spell","ability","script"):
				try:
					if t=="spell":k=bool(API.IsSpellActive(v))
					elif t=="ability":k=bool(API.SecondaryAbilityActive()if v=="secondary"else API.PrimaryAbilityActive())
					else:k=bJ(v)
				except Exception:k=False
				d,f=("ON"if k else ""),W
			elif t=="travel":
				if m is False:m=eU()
				d,f=eV(c,m)
			if t=="spell":
				o=dB(v);eT(p,g,o is not None)
				if o is not None and not(h and l<h):d,f=o[0],u
			cg(g,j,d,f)
		for s,g in list(e["bags"].items()):
			j=g.get("count");q=aM(s)
			if j is None or not q:continue
			try:n=int(API.Contents(q["s"])or 0)
			except Exception:n=0
			cg(g,j,str(n),X)
	bz={}
	def dA(name):
		a=bz.get(name)
		if a is None:
			c=bZ(name);b=Kit.REAGENTS;a=tuple((d,b[d][1],b[d][0])for d in(c[1]if c else())if d in b)
			if len(bz)>200:bz.clear()
			bz[name]=a
		return a
	def dB(name):
		b,c=a["cnt_g"],a.get("counted")or()
		for d,g,n in dA(name):
			if b.get(g,0)<=0 and g in c:return(d,n)
		return
	def eT(ref,info,grey):
		if info.get("grey",False)==grey:return
		info["grey"]=grey;a=info.get("icon")
		if a is not None:a.SetAlpha(.35 if grey else 1.)
		bE(info,a3(ref))
	def eU():
		a=HOST.services.get("grimoire.book_charges")
		if a is not None:return safe(a)
		a=HOST.services.get("grimoire.destinations")
		if a is None:return
		try:return dict((c["book"],c["charges"])for c in a()or())
		except Exception:return
	def eV(c,charges):
		if charges is None:return "off",J
		m=c.get("rm");b=max(0,c["lo"])
		if m in bm:n=a["cnt_g"].get(bm[m],0);return dm(n),u if n<=b else X
		try:n=charges.get(int(c.get("rb")or "0",16))
		except ValueError:n=None
		if n is None:return "",X
		if m=="charge":return str(n),u if n<=b else X
		return str(n),J
	def eW(c):
		a=HOST.services.get("grimoire.travel")
		if a is None:l("Grimoire is off; turn it on to use Travel cells.",u);return False
		try:b,d=int(c.get("rb")or "",16),int(c.get("ri")or "")
		except ValueError:l("this Travel cell has no destination; right-click it to pick one.",u);return False
		return bool(a(b,d,c.get("rm")or "recall",c["v"]or None))
	def eX(ref,d,method):a=B(ref);b=dict(ad(),t="travel",v=str(d["name"]),n=str(d["book_name"]),k=a["k"],tg="",lo=a["lo"]if a["t"]=="travel"else 2,rb="%X"%int(d["book"]),ri=str(int(d["index"])),rm=method);C[ref[0]][ref[1]]=b;aB(recount=True,refs=[ref]);l("%s set on %s."%(a2(b),S(ref)),W)
	eY={"arms lore":3.,"item identification":3.,"detect hidden":3.}
	def dC(a):return("%d"%int(math.ceil(a)))if a>=3. else("%.1f"%max(0.,a))
	def eZ(t,v):
		if t=="skill":b=eY.get(str(v).strip().lower(),10.)
		else:c=bZ(v);b=c[3]if c else 0.
		if b and b>0:a["cool"][t]=time.time()+b;a["cool_next"]=0.
	def e_(now):
		c=a["cool"]
		if not(c["skill"]or c["spell"])or now<a["cool_next"]:return
		a["cool_next"]=now+.1;k=a6()["refs"];i=False
		for f in("skill","spell"):
			g=c[f]
			if not g:continue
			d=now>=g
			if d:c[f]=0.;i=True
			l=""if d else dC(g-now)
			for m in k[f]:
				b=e["cells"].get(m)
				if b is None:continue
				h=not d
				if b.get("dark",False)!=h:b["dark"]=h;b["catcher"].SetAlpha(.55 if h else.01)
				j=b.get("count")
				if j is not None and not d:cg(b,j,l,ae)
		if i:a9()
	def e0(ref):
		c=B(ref)
		if c["t"]=="travel":return a2(c)
		a=a3(ref).split("\n")[0];return a.replace("  [%s]"%c["k"],"")if c["k"]else a
	def e1():
		a=[(_norm_key(f["k"]),"%s: %s"%(S(d),e0(d)))for d,f in az()if _norm_key(f["k"])and f["t"]and bt(d)];a+=[(c,"bag slot %d"%(g+1))for g,c in enumerate(aj())if c];a=[(h,i+((" (left to %s)"%ay(h))if ay(h)else ""))for h,i in a];b=b8()
		if b:a.append((b,"radial ring"+((" (left to %s)"%HOST.hotkeys_owned[b])if b in HOST.hotkeys_owned else "")))
		return a
	e2=Kit.disposer(r,a,e)
	def au(delay=0.):a["rebuild_at"]=time.time()+delay
	def aB(recount=False,refresh=True,refs=None):
		a4();aE()
		if recount:a["next_count"]=0.
		if refs is None:au()
		else:aR(refs)
		if refresh:an(r)
	def dD(ref):C[ref[0]][ref[1]]=ad();aB(refs=[ref])
	D={"scale":None,"vertical":None,"slot":None,"off":(0,0),"sig":None}
	def bA():
		v=D["scale"]
		if v is not None:return v
		k=Kit.tscale*(.85 if Kit.compact else 1.);s=int(b["scale"]);return s if k==1. else max(ao,min(aw,int(round(s*k))))
	def aN():v=D["vertical"];return bool(b["vertical"])if v is None else v
	def ch():return D["slot"]if D["scale"]is not None else None
	def dE():return(b["slot"],b["top"],b["extra"])
	def ci(b,c):
		f=D["scale"]
		try:
			D["scale"]=100;d=aO();a=max(ao,min(aw,int(min(b*100./max(1.,d["W"]),c*100./max(1.,d["H"])))))
			def e(p):D["scale"]=p;a=aO();return a["W"]<=b and a["H"]<=c
			for g in range(8):
				if a<=ao or e(a):break
				a-=1
			for g in range(8):
				if a>=aw or not e(a+1):break
				a+=1
			return a
		finally:D["scale"]=f
	def dF():
		a=HOST.layout_base(r)
		if not b["extra"]or a is None:cJ(r);return
		c=a[1]>a[0];f,g=(a[1],a[0])if c else a;d,h,i=b["extra"],D["scale"],U.get("vtmp");U["vtmp"]=c
		try:b["extra"]=0;p=ci(int(f),int(g));b["extra"]=d;D["scale"]=p;e=aO()["H"]
		finally:b["extra"]=d;D["scale"]=h;U["vtmp"]=i
		cJ(r,e if c else None,None if c else e)
	def e3(w,h,mode):
		if w is None or h is None or not w or not h:c=(None,None);d=e=None
		else:
			d=(int(w),int(h));b=h>w;f,g=(h,w)if b else(w,h);e=dE();dF();U["vtmp"]=b
			try:c=(ci(int(f),int(g)),b)
			finally:U["vtmp"]=None
		i=(bA(),aN(),D["slot"]);D["scale"],D["vertical"]=c;D["slot"],D["sig"]=d,e
		if(bA(),aN(),D["slot"])!=i and not a["shutting"]:au()
	def e4():
		a=ch();b=dE()
		if a is None or b==D["sig"]:return
		c,d=(a[1],a[0])if D["vertical"]else a;D["scale"]=ci(c,d);D["sig"]=b;dF()
	def e5():
		if e["g"]is None or a["shutting"]:return
		return "minimized"if a["em"]else "open"
	def e6():
		c,d=D["scale"],U["vtmp"];a=[]
		try:
			D["scale"]=ao
			for v in(False,True):U["vtmp"]=v;b=aO();a.append((b["H"],b["W"])if v else(b["W"],b["H"]))
		finally:D["scale"],U["vtmp"]=c,d
		return min(a[0][0],a[1][0]),min(a[0][1],a[1][1])
	e7={"fit":e3,"state":e5,"min":e6,"exact":True,"untitled":True}
	def sc(v,lo=1):k=max(ao,min(aw,bA()))/100.;return max(lo,int(round(v*k)))
	ba={"key":None,"L":None}
	def cj():
		a=ch();c=(b["slot"],bA(),b["top"],b["extra"],a,aN())
		if ba["key"]!=c:
			if a is None:ba["L"]=aO()
			else:d,e=(a[1],a[0])if aN()else a;ba["L"]=fa(aO(),d,e)
			ba["key"]=c
		return ba["L"]
	U={"capw":None,"vtmp":None}
	def dG():
		if U["capw"]is None:U["capw"]=max(M(d)for d in("Keys","Lock","Grid"))+6
		return U["capw"]
	def dH(a):return(4,2,1)if a else(1,2,4)
	def e8(c,b,d):a=(4+c-1)//c;e=(b-2*Q-(c-1)*Q)//c;f=min(24,(d-2*Q-(a-1)*Q)//a);return a,e,f
	def e9(b,a):
		d=dG()
		for c in dH(a):
			e=(4+c-1)//c;f=e*bo+(e-1)*Q+2*Q;g=c*d+(c-1)*Q+2*Q
			if a and g<=b:return f
			if not a and f<=b:return g
		return(4*bo+5*Q)if a else(4*d+5*Q)
	def aO():S=sc(max(bk,min(bl,int(b["slot"]))),18);k,c,a=sc(ej,4),sc(6,3),sc(4,2);m=k;t,l,n=sc(4,2),sc(el,2),sc(em,2);h,g,o=sc(ei,16),sc(ek,34),sc(en,18);f=S+t;e=S+2*a;i=h+z*f+a;p=N*f+a;q=o+2*a;r=i-h-p-2*c-q-c;j=int(r*cY);s=r-j;u=(j-2*a-(E-1)*l)//E;v=(s-2*a-(O-1)*n)//O;d=(2 if b["top"]else 1)+b["extra"];g=max(g,e9(d*e+(d-1)*c,aN()if U["vtmp"]is None else U["vtmp"]));return{"S":S,"pitch":f,"ph":e,"inner":i,"left_w":p,"rows":d,"ui_w":j,"bag_w":s,"bw":u,"bh":e-3*a,"tray_w":q,"tb":o,"bgw":v,"bgh":e-2*a,"m":m,"sg":c,"p4":a,"ug":l,"bg":n,"pw":h,"cw":g,"tm":k,"colx":tuple(a+w*f for w in range(z)),"colw":(S,)*z,"top_w":z*f+a,"sgx":c,"sgc":c,"rowy":tuple(x*(e+c)for x in range(d)),"rowh":(e,)*d,"celly":(a,)*d,"cellh":(S,)*d,"W":m+i+c+g+m,"H":m+d*e+(d-1)*c+m}
	def aP(total,n):
		if n<=0:return[]
		if total<=0:return[0]*n
		return[(total*(c+1))//n-(total*c)//n for c in range(n)]
	def fa(L,P,Q):
		L=dict(L);S,e,d,c=L["S"],L["p4"],L["sg"],L["rows"];o=L["pitch"]-S;n=z;p=max(0,int(S*1.6)-S);a=P-L["W"]
		if a>0:
			h=n*o+d;b=min(a,h);t=float(b)/h if h>0 else 0.;q=min(b,int(round(d*t)));i=[o+at for at in aP(b-q,n)];f=min(a-b,n*p);s=[S+by for by in aP(f,n)];j=a-b-f;u=0
			if j>0:
				if c>1:i=[dd+fn for dd,fn in zip(i,aP(j,n))]
				else:u=j
			k,x=[],e
			for v in range(n):k.append(x);x+=s[v]+i[v]
			w=d+int(round(d*t));A=L["ug"]+int(round(L["ug"]*t));B=L["bg"]+int(round(L["bg"]*t));C,R=L["pw"],L["tray_w"];l=C+x+u;D=k[N];F=l-C-D-3*w-R;m=int(F*cY);G=F-m;L.update({"colx":tuple(k),"colw":tuple(s),"top_w":x,"sgx":w,"sgc":d+q,"ug":A,"bg":B,"inner":l,"left_w":D,"ui_w":m,"bag_w":G,"bw":(m-2*e-(E-1)*A)//E,"bgw":(G-2*e-(O-1)*B)//O});L["W"]=L["m"]+l+L["sgc"]+L["cw"]+L["m"]
		a=Q-L["H"]
		if a>0:
			b=min(a,(c-1)*d);T=[d+gv for gv in aP(b,c-1)];f=min(a-b,c*p);g=[S+gw for gw in aP(f,c)];H=aP(a-b-f,c);I,J,K,y=[],[],[],0
			for r in range(c):I.append(y);M=g[r]+2*e+H[r];J.append(M);K.append(e+H[r]//2);y+=M+(T[r]if r<c-1 else 0)
			L.update({"rowy":tuple(I),"rowh":tuple(J),"celly":tuple(K),"cellh":tuple(g),"bh":g[-1]-e,"bgh":g[-1]});L["H"]=L["m"]+y+L["m"]
		return L
	def aQ():return not aN()
	def bB():
		if a["em"]:return c9,da
		L=cj();return(L["W"],L["H"])if aQ()else(L["H"],L["W"])
	def R(x,y,w,h):a,b=D["off"];return(x+a,y+b,w,h)if aQ()else(y+a,x+b,h,w)
	def bb(g,graphic,hue,x,y,w,h):
		try:p=G.CreateGumpItemPic(int(graphic),int(w),int(h))
		except Exception:return
		if hue:p.Hue=max(0,min(65535,int(hue)))
		p.SetPos(x,y);p.SetAcceptMouseInput(False);g.Add(p);return p
	def dI(text):t=str(text).replace("_"," ");return "".join(" "+c if d and c.isupper()and t[d-1].islower()else c for d,c in enumerate(t))
	def bc(g,text,x,y,w,h,hue=None):
		b=max(1,min(3,(h-2)//14));a=[bW(d,w-4)for d in bj(dI(text),w-4)]
		if len(a)>b:a=a[:b];a[-1]=bW(a[-1]+"..",w-4)if not a[-1].endswith("..")else a[-1]
		c=y+(h-14*len(a))//2-1;return[I(g,f,x+(w-M(f))//2,c+k*14,X if hue is None else hue)for k,f in enumerate(a)]
	def fb(kind,c,b):
		def d():
			if a["right_ok"]is False and Client.key_held("shift"):A.add((c,b),dup=True)
			else:A.add((kind,b),dup=True)
		return Kit.once(d,(r,kind,b),Kit.TWICE)
	def fc(b,fn):
		if b is None or a["right_ok"]is False:return False
		if Kit.hook_mouse(b,fn,event="MouseUp",button="Right"):a["right_ok"]=True;return True
		if a["right_ok"]is None:a["right_ok"]=False;l("no right-click events from this client; Shift+click a cell for its menu instead.")
		return False
	def bC(g,icon,x,y,w,h):
		a=min(w,h)-4;p=Kit.add_pic(g,icon,x+(w-a)//2,y+(h-a)//2)
		if p is not None:p.SetWidth(a);p.SetHeight(a);p.SetAcceptMouseInput(False)
		return p
	def bD(g,a,d,y,h):
		e=Kit.GOLD_V if aQ()else Kit.GOLD_H
		for b,f,w in zip(a,a[1:],d):c=f-b-w;s=min(c,Kit.GOLD_T);Y(g,e,*R(b+w+(c-s)//2,y,s,h))
	def ck(g,ref,x,y,w,h):
		if not B(ref)["t"]:
			Y(g,aq,x,y,w,h,ar*.3)
			for a,b,c,d in((x,y,w,1),(x,y+h-1,w,1),(x,y,1,h),(x+w-1,y,1,h)):Y(g,aq,a,b,c,d,ar)
		else:Y(g,aq,x,y,w,h,ar)
		dJ(g,ref,x,y,w,h)
	def cl(ref,x,y,w,h,pad):
		if w==h or ref[0]=="u":return x+pad,y+pad,w-2*pad,h-2*pad
		a=min(w,h)-2*pad;return x+(w-a)//2,y+(h-a)//2,a,a
	def dJ(g,ref,x,y,w,h):c=B(ref);t=c["t"];a={"x":x,"y":y,"w":w,"h":h,"count":None};d=dK(g,ref,c,a,x,y,w,h,14 if(b["keys"]and c["k"]and t)else 0)[0];e["cells"][ref]=dL(g,a,d,t in("item","spell","ability","script","skill","travel"),c["k"]if b["keys"]and t else "",a3(ref),("click","menu",ref));a8[0]=None
	def dK(g,ref,c,info,x,y,w,h,b):
		t=c["t"];d=[];f=False;p=None
		if t=="item"and c["g"]:p=bb(g,c["g"],c["h"],*cl(ref,x,y,w,h,3))
		elif t=="spell":
			a=dg(c["v"])
			if a:p=info["icon"]=bC(g,a,x,y,w,h)
		elif t=="travel":
			m=c.get("rm")
			if m in c3:
				a=dg(c3[m])
				if a:p=bC(g,a,x,y,w,h)
			elif m in c2:p=bb(g,c2[m],0,*cl(ref,x,y,w,h,3))
			if p is not None:p.SetAlpha(.5)
			e=ai(c["v"]or "?",w-4);d.append(I(g,e,x+(w-M(e))//2,y+b+(h-b-14)//2-1));f=True
		elif t=="ability":
			a,e=eC(c["v"])
			if a:p=bC(g,a,x,y,w,h)
			elif e:d.extend(bc(g,e,x,y+b,w,h-b));f=True
		elif t=="ui":
			i=a0(c["v"])
			if i and i[2]:p=bb(g,i[2],0,*cl(ref,x,y,w,h,2))
		elif t=="script":
			j=dI(ak(c)).strip().lower();a=b7.get(j)if j else None
			if a and aG(a)[0]>0:p=bC(g,a,x,y,w,h)
		if p is not None:f=True;d.append(p)
		if t and not f:d.extend(bc(g,ak(c),x,y+b,w,h-b))
		return d,p
	def dL(g,info,parts,counted,k,tip,click):
		x,y,w,h=info["x"],info["y"],info["w"],info["h"]
		if counted:info["count"]=I(g,"",x+w-6,y+h-16);info["txt"],info["hue"]="",X;parts.append(info["count"])
		if k:a=ai(dl(k),w-4);info["key"]=I(g,a,x+w-2-M(a),y+1,J);parts.append(info["key"])
		info["tip"]=tip;info["catcher"]=aF(g,x,y,w,h,fb(*click),tip);parts.append(info["catcher"]);fc(info["catcher"],A(click[1:]));info["parts"]=parts;return info
	def cm(i):
		c,e=aM(i),b["bagmode"];f=(e==0 and a["ub_state"])and("Show the Bags window"if a["ub_state"]!="open"else "Fold the Bags window into the bar")
		if e==1:d=("Open %s\nRight-click: pick another bag, or clear the slot"%c["n"]if c else "Empty: click, then target a bag for it")
		elif f:d=f+"\n%sRight-click: the Bags settings"%(c["n"]+"   "if c else "")
		else:d="Open %s"%c["n"]if c else "No bag here"
		g=aj()[i]
		if g:d+="  [%s]"%g
		return d
	def fd(g,i,x,y,w,h):Y(g,aq,x,y,w,h,ar);dM(g,i,x,y,w,h)
	def dM(g,i,x,y,w,h):a=aM(i);c={"x":x,"y":y,"w":w,"h":h,"count":None};d=[bb(g,a["g"],a["h"],x+3,y+3,w-6,h-6)]if a and a["g"]else[];e["bags"][i]=dL(g,c,d,a,aj()[i]if b["keys"]else "",cm(i),("bag","bagmenu",i))
	def aR(refs):a["redraw"].update(refs)
	def fe(ref):
		g=e["g"];f=ref[0]=="b";a,k=(e["bags"].get(ref[1]),aj()[ref[1]])if f else(e["cells"].get(ref),B(ref)["k"])
		if a is None or not K(g):return
		d=ai(dl(k),a["w"]-4)if(b["keys"]and k and(f or B(ref)["t"]))else "";c=a.get("key")
		if d and c is None:c=I(g,d,a["x"]+a["w"]-2-M(d),a["y"]+1,J);c.SetAcceptMouseInput(False);a["key"]=c;a.setdefault("parts",[]).append(c)
		elif c is not None:c.Text=d
		bE(a,cm(ref[1])if f else a3(ref))
	def bE(info,tip):
		c=info.get("catcher")
		if c is not None and info.get("tip")!=tip:info["tip"]=tip;av(c,tip)
	def dN():
		if not K(e["g"]):return
		for b,a in list(e["cells"].items()):
			c=B(b)
			if(c["t"]=="ui"and(c["v"]in("spellbook","virtue")or c["v"].startswith("mod:"))or c["t"]=="travel"):bE(a,a3(b))
		for i,a in list(e["bags"].items()):bE(a,cm(i))
	def bF(a,hue,tip):
		for b in a["text"]:b.Hue=hue
		av(a.get("catcher"),tip)
	def cn():
		a=e.get("keybtn")
		if a and K(e["g"]):bF(a,*dP())
	def dO():
		if not K(e["g"]):return
		a=e.get("traybtn")
		if a:
			n=len(bw());c=ae if n else J
			for b in a.get("text",[]):aI(b,str(n),c);b_(b,a["x"]+(a["w"]-cW(str(n)))//2,a["ly"])
			av(a.get("catcher"),dQ(n))
		dX()
	bG=(("up","Next page of the bottom-left cells (page %d of %d showing)"),("dn","Previous page of the bottom-left cells (page %d of %d showing)"),("catcher","Page %d of %d of the bottom-left cells; click for the next page"))
	def ff(g,store,x,d,ph,m):p=b["page"];c,a=aG(bR[0]);c,a=c or 16,a or 16;n=x+(m-c)//2;f,h=R(n,d+1,c,a)[:2];q=af(g,store,"pgup",bR,f,h,None,bG[0][1]%(p+1,T),on_click=A(("page",1)));f,h=R(n,d+ph-a-1,c,a)[:2];r=af(g,store,"pgdn",aV,f,h,None,bG[1][1]%(p+1,T),on_click=A(("page",-1)));o=str(p+1);i,j,k,l=R(x,d+a+1,m,max(1,ph-2*a-2));s=I(g,o,i+(k-M(o))//2,j+(l-14)//2,ae);t=aF(g,i,j,k,l,A(("page",1)),bG[2][1]%(p+1,T));e["pagecol"]={"up":q,"dn":r,"num":s,"catcher":t,"rect":(i,j,k,l),"page":p}
	def fg():
		a=e.get("pagecol");p=b["page"]
		if not a or a["page"]==p or not K(e["g"]):return
		a["page"]=p;c=str(p+1);f,g,h,i=a["rect"];d=a["num"];aI(d,c);b_(d,f+(h-M(c))//2,g+(i-14)//2)
		for k,j in bG:av(a[k],j%(p+1,T))
	def fh(g,key,d,x,y,w,h):
		Y(g,aq,x,y,w,h,ar);a=safe(d.get("state"));b=d.get("title")or key;e=0 if a=="open"else J;c=d.get("icon")or 0;f=c and bb(g,c,e,x+2,y+2,w-4,h-4)is not None
		if not f:bc(g,b[:3].upper(),x,y,w,h,X if a=="open"else J)
		i=("%s is off; click to turn it on"if a is None else "Fold %s into the bar"if a=="open"else "Show %s")%b;aF(g,x,y,w,h,A(("dock",key)),i)
	def fi(g,box,a,fn,hue,tip):x,y,w,h=box;Y(g,aq,x,y,w,h,ar);return{"text":bc(g,a,x,y,w,max(16,h),hue),"catcher":aF(g,x,y,w,h,fn,tip)}
	def dP():
		if a["bind"]is not None:return ae,"Keybind mode on: hover a cell, press a key; Esc or a click here ends it"
		return X,"Start keybind mode: hover a cell and press a key to bind it"
	def dQ(n):return "%s folded into the bar; click to %s the tray"%(Kit.count(n,"window"),"hide"if b["tray_open"]else "show")
	def fj(g,store,L):
		c,h=L["m"],L["cw"];x=c+L["inner"]+L["sgc"];l=L["rowy"][-1]+L["rowh"][-1];d,f=aG(aV[0]);d,f=d or 16,f or 16;m=c+2+f+4;n=c+l-m;j=dG();z=(("Keys",A(("bind",)),dP()),("Lock",A(("lockbar",)),co()),("Grid",A(("grid",)),dR()))
		if aQ()and n>=66 and h-4>=j:p,q=R(x+(h-d)//2,c+2,d,f)[:2];B,s=h-4,min(28,(n-8)//3);t=[R(x+2,m+at*(s+4),B,s)for at in range(3)]
		else:C,D,u,v=R(x,c,h,l);w=[(by,)+e8(by,u,v)for by in dH(not aQ())];i,y,a,b=(next((dd for dd in w if dd[2]>=j and dd[3]>=bo),None)or max(w,key=lambda o:min(o[2]-j,o[3]-bo)));a,b=max(1,a),max(1,b);E=i*a+(i-1)*Q;F=y*b+(y-1)*Q;G=C+max(Q,(u-E)//2);H=D+max(Q,(v-F)//2);k=[(G+(gv%i)*(a+Q),H+(gv//i)*(b+Q),a,b)for gv in range(4)];p,q=k[0][0]+(a-d)//2,k[0][1]+(b-f)//2;t=k[1:]
		if not ag(r):af(g,store,"min",aV,p,q,None,"Minimize the bar",on_click=A(("toggle_min",)))
		e["keybtn"],e["lockbtn"],e["gridbtn"]=[fi(g,gz,gw,gx,*gy)for(gw,gx,gy),gz in zip(z,t)]
	def dR():
		if HOST.grid_shown():return ae,"Hide the screen grid windows snap to"
		return J,"Show the screen grid; windows you let go snap to it, the corners, edge middles and centre"
	def fk():
		b=bool(HOST.grid_toggle());a=e.get("gridbtn")
		if a and K(e["g"]):bF(a,*dR())
		l("screen grid %s."%("shown"if b else "hidden"))
	def co():
		if cH():
			if bO():return ae,"Lock every window in its zone"
			return J,"Unlock the layout to move windows between zones"
		if b["lock"]:return u,"Locked; click to unlock the bar"
		return J,"Lock the bar in place"
	def dS():
		g,a=e["g"],e.get("lockbtn")
		if not a or not K(g):return False
		g.CanMove=not b["lock"]and not cI(r);bF(a,*co());e["arranging"]=bO();return True
	dT=("g","store","cells","bags","keybtn","lockbtn","gridbtn","traybtn","pagecol")
	def dU():
		b=dict((f,e.get(f))for f in dT);a=b["g"];x,y=(a.GetX(),a.GetY())if K(a)else(None,None);e.setdefault("stale",[]).append(a);e.update(dict.fromkeys(dT[4:]),g=None,cells={},bags={});d=({},{});a8[0]=None;c={"g":None}
		try:fl(x,y,d,c)
		except Exception:
			if e["g"]is None:V(c["g"]);e.update(b);a8[0]=None;e["stale"]=[g for g in e.get("stale",[])if g is not a]
			else:
				for s in e.pop("stale",[]):V(s)
			raise
	def fl(x,y,store,built):
		H=cI(r);I=a["em"]=bool(a["minimized"])and not ag(r)
		if I:
			w,h=c9,da
			if x is None:x,y=cS(b0,(200,600),(w,h))
			g=built["g"]=G.CreateGump(True,not H);Kit.mini_bar(g,store,w,h,aZ,r,A(("toggle_min",)),"%s: page %d"%(aZ,b["page"]+1))
		else:
			e4();L=cj();w,h=bB();D["off"]=(0,0);l=ch()
			if l is not None:D["off"]=(max(0,(l[0]-w)//2),max(0,(l[1]-h)//2));w,h=max(w,l[0]),max(h,l[1])
			if x is None:x,y=cS(b0,(200,600),(w,h))
			p,J,m=L["m"],L["pw"],L["p4"];u,v,W=L["ug"],L["bg"],L["tb"];B,q,s=L["sgx"],L["colx"],L["colw"];K,M,P,Q=L["rowy"],L["rowh"],L["celly"],L["cellh"];k=p+J;g=built["g"]=G.CreateGump(True,not b["lock"]and not H);bT(g,w,h,corners=False);d=0
			for X,Z in([("x",at*z)for at in range(b["extra"]-1,-1,-1)]+([("a",0)]if b["top"]else[])):
				c=p+K[d];aX(g,*R(k,c,L["top_w"],M[d]));f,n=c+P[d],Q[d]
				for i in range(z):ck(g,(X,Z+i),*R(k+q[i],f,s[i],n))
				bD(g,[k+by for by in q],s,f,n);d+=1
			c,j=p+K[d],M[d];f,n=c+P[d],Q[d];ff(g,store,p,c,j,J);aX(g,*R(k,c,L["left_w"],j))
			for i in range(N):ck(g,("a",z+i),*R(k+q[i],f,s[i],n))
			bD(g,[k+dd for dd in q[:N]],s,f,n);t=k+L["left_w"]+B;aX(g,*R(t,c,L["ui_w"],j));Y(g,cO,*R(t+m,c+m,L["ui_w"]-2*m,j-2*m),alpha=.55);C=E*L["bw"]+(E-1)*u;o=t+(L["ui_w"]-C)//2
			for i in range(E):ck(g,("u",i),*R(o+i*(L["bw"]+u),c+(j-L["bh"])//2,L["bw"],L["bh"]))
			bD(g,[o+fn*(L["bw"]+u)for fn in range(E)],(L["bw"],)*E,c+(j-L["bh"])//2,L["bh"]);F=t+L["ui_w"]+B;aX(g,*R(F,c,L["bag_w"],j));C=O*L["bgw"]+(O-1)*v;o=F+(L["bag_w"]-C)//2
			for i in range(O):fd(g,i,*R(o+i*(L["bgw"]+v),f,L["bgw"],L["bgh"]))
			bD(g,[o+gv*(L["bgw"]+v)for gv in range(O)],(L["bgw"],)*O,f,L["bgh"]);S=F+L["bag_w"]+B;aX(g,*R(S,c,L["tray_w"],j));fm(g,*R(S+m,f,W,L["bgh"]));fj(g,store,L)
		if b["anchor"]and not ag(r):
			T,ay=cR(b["anchor"],w,h)
			if T is not None:x,y=T,ay
		a["last_pos"]=Kit.show_window(g,x,y,w,h,None,False,e2(g),a5,e,{"g":g,"store":store});a["moved_at"]=None
		for aa in e.pop("stale",[]):V(aa)
		if not I and time.time()-a.get("counted_at",0.)>b2:
			U=a6()
			if "item"in U["types"]or U["extra"]:a7()
		a9();dX()
	def fm(g,x,y,w,h):n=len(bw());Y(g,aq,x,y,w,h,ar);a=bc(g,str(n),x,y,w,h,ae if n else J);e["traybtn"]={"text":a,"x":x,"w":w,"ly":y+(h-14)//2-1,"catcher":aF(g,x,y,w,h,A(("traywin",)),dQ(n))}
	def dV(w,h,at=None,rect=False):
		if rect is False:
			g=e["g"]
			if not K(g):return 300,300
			rect=Kit.rect(g)
			if at is None:at=aH(g)or(0,0)
		a,b=at;d,c=(rect[2],rect[3])if rect is not None and rect[2]>0 else bB();W,H=bh()
		if aQ():
			x,y=a+d+ap,b+c-h
			if W and x+w>W:
				x=a-ap-w
				if x<0:
					x,y=a,b+c+ap
					if H and y+h>H:y=b-ap-h
		else:
			x,y=a,b+c+ap
			if H and y+h>H:
				y=b-ap-h
				if y<0:
					x,y=a+d+ap,b
					if W and x+w>W:x=a-ap-w
		return x,y
	def fo():return e["g"]
	gu=None
	def fp():
		d,a["redraw"]=a["redraw"],set();g=e["g"]
		if not d or a["em"]or not K(g):return
		for c in sorted(d):
			f=c[0]=="b";b=e["bags"].get(c[1])if f else e["cells"].get(c)
			if b is None:continue
			for p in b.get("parts")or():V(p)
			if f:dM(g,c[1],b["x"],b["y"],b["w"],b["h"])
			else:dJ(g,c,b["x"],b["y"],b["w"],b["h"])
		a9()
	def dW():
		g=e["g"]
		if not b["anchor"]or not K(g)or ag(r):return
		w,h=bB();x,y=cR(b["anchor"],w,h)
		if x is None:return
		if(x,y)!=a.get("last_pos"):g.SetPos(x,y);Kit.note_rect(g,x,y);cT(g);a["last_pos"]=(x,y);dY()
	def fq(x,y):
		if a["em"]:return
		if ag(r):return
		w,h=bB();c=Kit.anchor_at(x,y,w,h,SNAP_ANCHOR);d=True if c in("L","R")else False if c in("T","B")else None;e=d is not None and d!=b["vertical"]
		if c!=b["anchor"]or e:
			b["anchor"]=c
			if e:b["vertical"]=d;aa();au();l("standing %s along the %s edge."%("upright"if d else "flat",{"L":"left","R":"right","T":"top","B":"bottom"}[c]));return
			aa()
		dW();a5()
	def fr(now):
		g=e["g"]
		if not K(g):return
		d=Kit.rect(g);c=(d[0],d[1])if d else(0,0)
		if c!=a.get("last_pos"):a["last_pos"],a["moved_at"]=c,now
		elif a.get("moved_at")is not None and now-a["moved_at"]>=.3 and SNAP.pressed()is not True:a["moved_at"]=None;fq(c[0],c[1])
		dY(c,d)
		if b["anchor"]and now>=a.get("screen_next",0.):
			a["screen_next"]=now+2.;f=bh()
			if f!=a.get("screen_wh"):
				a["screen_wh"]=f
				if not ag(r):dW()
	def dX():
		k,ac["g"]=ac["g"],None;d=bw()
		if a["em"]or not b["tray_open"]or not d:V(k);return
		L=cj();f,l,m=L["tb"],L["bg"],max(4,L["tm"]//2);c,i=aG(aV[0]);c,i=c or 16,i or 16;j=L["bgh"];w=m+len(d)*(f+l)+c+m;h=m+j+m;g=G.CreateGump(True,False);bT(g,w,h,corners=False)
		for n,(o,p)in enumerate(d):fh(g,o,p,m+n*(f+l),m,f,j)
		q=({},{});af(g,q,"fold",aV,w-m-c,m+(j-i)//2,None,"Hide the tray (the bar's numbered button brings it back)",on_click=A(("traywin",)));x,y=dV(w,h);bX(g,x,y,w,h);ac.update({"g":g,"at":(x,y),"w":w,"h":h});G.AddGump(g);Kit.attach(g,e["g"]);V(k)
	def dY(at=None,rect=False):
		g=ac["g"]
		if not K(g):return
		w,h=ac.get("w",0),ac.get("h",0);x,y=dV(w,h,at,rect)
		if(x,y)!=ac["at"]:ac["at"]=(x,y);g.SetPos(*Kit.clamp(x,y,w,h));cT(g)
	def fs():
		a7(db);b=(next((c for c in(a["first_g"].get(d)for d in db)if c),None)or API.FindLayer("Spellbook"))
		if b:API.UseObject(b);return True
		l("no spellbook in your pack.",u);return False
	def dZ():
		if cH():HOST.layout_arrange();dS();return
		b["lock"]=not b["lock"];aa()
		if not dS():au()
		if ab.f is not None:ab.f.c["lock"].IsChecked=b["lock"]
		else:an(r)
		l("%s."%("locked"if b["lock"]else "unlocked"),W)
	def ft():
		g=e["g"];b=aY();c=aH(g)if K(g)else None
		if b is None or c is None:return
		d,f=b[0]-c[0],b[1]-c[1]
		for h,a in(list(e["cells"].items())+[(("b",k),m)for k,m in e["bags"].items()]):
			if a["x"]<=d<a["x"]+a["w"]and a["y"]<=f<a["y"]+a["h"]:return h
		return
	def cp(ref=None):cL();a["bind"]={"sel":ref};cn();l("keybind mode on: %s (Esc ends it, Backspace clears a key)."%("click a cell, then press a key"if aY()is None else "hover a cell and press a key"))
	def bH():
		if a["bind"]is None:return
		a["bind"]=None;cn();l("keybind mode off.")
	def fu():cL();a["bind"]={"sel":aJ};cn();l("press the key for the radial ring (Esc ends, Backspace clears it).")
	def cq(ref,k):
		a=ref==aJ;c=HOST.hotkeys_owned.get(_norm_key(k))if a else ay(k)
		if c:l("%s belongs to %s; pick another."%(k,c),u);return
		d=_norm_key(k)
		if a and(d in dk()or any(h["t"]and _norm_key(h["k"])==d for m in C["pages"]for h in m)):l("%s is on a cell; pick another."%k,u);return
		b=[ref]
		for r,e in az():
			if r!=ref and _norm_key(e["k"])==k:e["k"]="";b.append(r);l("%s taken off %s."%(k,S(r)))
		for i,f in enumerate(aj()):
			if("b",i)!=ref and f==k:b9(("b",i),"");b.append(("b",i));l("%s taken off bag slot %d."%(k,i+1))
		b9(ref,k)
		if ref[0]=="b":a4()
		aE();d_(b);g=ref[0]in("a","u","x")and not B(ref)["t"];l("%s bound to %s%s."%(k,S(ref)," (empty; fill it to use it)"if g else ""),W)
		if a:bH()
	def fv(d):
		c=a["bind"]
		if not c:return
		k=d.rsplit("+",1)[-1]
		if k=="ESCAPE":bH();return
		b=c["sel"]if c["sel"]==aJ else ft()or c["sel"]
		if b is None:l("hover a cell on the bar (or click one) first.");return
		c["sel"]=b
		if k in("BACKSPACE","DELETE"):
			b9(b,"");aE();d_([b]);l("%s has no hotkey now."%S(b),W)
			if b==aJ:bH()
			return
		cq(b,d)
	def d_(refs):
		for r in refs:
			if r!=aJ:fe(r)
		a=a1(P["sel"])
		if ab.f is not None and a in refs:ab.f.c["key"].SetText(B(a)["k"])
	d0={"barsettings":lambda:bf(r),"lock":lambda:dZ(),"minimize":lambda:A(("toggle_min",))(),"war":lambda:API.SetWarMode(not bool(API.Player.InWarMode)),"help":lambda:API.OpenHelp(),"quests":lambda:API.OpenQuestLog()}
	def cr(uid):
		d=a0(uid)
		if d is None:l("unknown window button '%s'."%uid,u);return False
		a=d[3];b=True
		if a in d0:d0[a]()
		elif a=="grimoire":return eP()
		elif a=="virtue":return eQ()
		elif a=="launcher":return fw()
		elif a=="paperdoll":
			import System
			if not ClientUI.game_action("OpenPaperdoll",[System.UInt32(int(API.Player.Serial))]):
				if aT():ah(lambda:cr("paperdoll"))
				else:b=safe(lambda:API.ContextMenu(API.Player,"Open Paperdoll",2),None)is not False
		elif a.startswith("mod:"):return eE(a[4:])
		elif a.startswith("ga:"):c=a.split(":");b=ClientUI.game_action(c[1],reuse=c[2]if len(c)>2 else None)
		elif a.startswith("macro:"):b=ClientUI.open_macro(a[6:])
		if not b:l("couldn't open %s (%s)."%(d[1],ClientUI.error or "unknown"),u)
		return b
	def fw():
		a=HOST.services.get("launcher.open")
		if a is None:l("the Quick Launcher needs the full Virtue Assistant.",u);return False
		try:a()
		except Exception as b:l("couldn't open the Quick Launcher (%s)."%b,u);return False
		return True
	aC={"looked":False,"type":None}
	def cs():
		if not aC["looked"]and aT():
			if not aC.get("asked"):aC["asked"]=True;ah(cs)
			return[]
		if not aC["looked"]:aC["looked"]=True;aC["type"]=be("ClassicUO.LegionScripting.LegionScripting")
		t=aC["type"]
		if t is None:return[]
		c=[]
		def a(a,n):return str(safe(lambda:ClientUI._get(a,n),"")or "")
		with Kit.quiet:
			for b in(ClientUI._get(None,"LoadedScripts",t)or[]):
				d,e=a(b,"RelativePath")or a(b,"FileName"),a(b,"FullPath")
				if d or e:c.append((d,e))
		return c
	d1={};ct=set()
	def cu(v):
		v=str(v or "").strip().replace("\\","/");b=d1.get(v)
		if b is not None and time.time()<b[0]:return list(b[1])
		f=v.split("/")[-1];k,l=v.lower(),f.lower();d=[]
		def a(c):
			if c and c not in d:d.append(c)
		m=not aT()
		if not m:
			if v not in ct:
				ct.add(v)
				def n():ct.discard(v);cu(v)
				ah(n)
			if b is not None:return list(b[1])
		if "/"in v:a(v)
		for e,q in cs():
			r=e.replace("\\","/");g=r.lower()
			if g==k or g.endswith("/"+k)or g.split("/")[-1]==l:a(r)
		if not m:a(v);a(f);return list(d)
		h=d8()
		if h:
			with Kit.quiet:
				for o,i,p in os.walk(h):
					e=o.replace("\\","/")[len(h):].strip("/")
					if e.count("/")>=2:i[:]=[]
					i[:]=[s for s in i if not s.startswith(".")and s.lower()not in cx]
					for j in p:
						if j.lower()==l:a((e+"/"+j)if e else j)
		a(v);a(f);d1[v]=(time.time()+60.,d);return list(d)
	bI={}
	def bJ(v):
		b=cu(v);a=bI.get(v)
		if a is not None and a in b:
			try:
				if API.IsScriptRunning(a):return True
			except Exception:pass
		for c in b:
			if c==a:continue
			try:
				if API.IsScriptRunning(c):
					if len(bI)>200:bI.clear()
					bI[v]=c;return True
			except Exception:pass
		return False
	def fx(v):
		e=cu(v);b=bJ(v);f=API.StopScript if b else API.PlayScript;d=False
		for g in e:
			if not safe(lambda c=g:(f(c),True)[1],False):continue
			d=True
			if not HOST.idle(.1)or bJ(v)!=b:break
		a["script_check"]=(v,b,time.time()+.5);return d
	def fy(now):
		b=a.get("script_check")
		if not b or now<b[2]:return
		a["script_check"]=None;v,c,f=b;e=bJ(v);d=v.replace("\\","/").split("/")[-1]
		if c and not e:l("stopped %s."%d)
		elif not c and e:l("started %s."%d,W)
		elif not c:l("%s didn't start; is it in the Legion Script Manager's list (refresh it)?"%d,u)
		a9()
	def fz(c):
		def e():return a["first"].get((c["g"],c["h"]))or(None if b["hue"]else a["first_g"].get(c["g"]))
		f=time.time()-a.get("counted_at",0.)>b2
		if f:a7()
		d=e()
		if not d and not f:a7();d=e()
		if not d:l("no %s left."%ak(c),u);return False
		API.UseObject(d);a["next_count"]=time.time()+.4;HOST.pack_dirty();return True
	d2={"spell":API.CastSpell,"skill":API.UseSkill,"dress":API.Dress,"undress":API.Undress,"say":API.Msg};fA=("stealing","snooping","discordance","provocation")
	def d3(c,t,v):
		if t=="skill":n=v.lower();return bool(n)and any(n in d for d in fA)
		if t=="spell":n=v.lower();return bool(n)and(n in c1 or any(f.startswith(n)for f in c1))
		return t=="item"and int(c.get("g")or 0)==3853
	def fB(a,c,t,v):
		if c["tg"]!="last"or not d3(c,t,v):return False
		return not HOST.harm_ok(int(API.LastTargetSerial or 0),("actionbar",)+a,aZ,True,"press again to confirm",t=="skill")
	def d4(ref):
		c=B(ref);t,v=c["t"],c["v"].strip()
		if not t:l("%s is empty."%S(ref));return
		m=time.time();e=(ref,b["page"])
		if fB(e,c,t,v):return
		h=c["tg"]in("self","last")and t not in("travel","say","ui","dress","undress","ability");w=a["want_target"]
		if w and m>w[1]:w=None
		i=bool(w)and w[2]==e;j=False
		if w and not i:bd();j=h
		d=True;n=bool(API.HasTarget("any"))
		try:
			if t in d2:d2[t](v)
			elif t=="item":d=fz(c)
			elif t=="macro":
				f=ClientUI.run_macro(v);d=bool(f)
				if f is None:l("no TazUO macro named '%s'."%v,u)
				elif not f:l("couldn't run macro '%s' (%s)."%(v,ClientUI.error or "unknown"),u)
			elif t=="ability":API.ToggleAbility(v or "primary")
			elif t=="script":
				def o():
					try:fx(v)
					except Exception as a:l("couldn't use %s (%s)."%(ak(c),a),u)
				ah(o)
			elif t=="ui":d=cr(v)
			elif t=="travel":d=eW(c)
		except Exception as p:l("couldn't use %s (%s)."%(ak(c),p),u);d=False
		if d and t in("skill","spell"):eZ(t,v)
		if d and h and not i:
			if j:l("a target was still pending; target by hand.")
			elif n:l("a target cursor was already up; target by hand.")
			elif cE(r):l("another module is using the target cursor; target by hand.")
			else:
				g=2.5
				if t=="spell":k=bZ(v);g+=k[3]if k else 0.
				HOST.claim_cursor(r,g);a["want_target"]=(c["tg"],time.time()+g,e,d3(c,t,v),int(API.LastTargetSerial or 0))
	def fC(now):
		w=a["want_target"]
		if not w:return
		c,d=w[0],w[1]
		if now>d:bd();return
		if not API.HasTarget("any"):return
		bd()
		if cE(r):return
		if API.HasTarget("beneficial"if w[3]else "harmful"):l("that cursor isn't this cell's; target by hand.");return
		if c=="self":API.TargetSelf()
		else:
			b=w[4]if w[3]else int(API.LastTargetSerial or 0)
			if b:API.Target(b)
			else:l("no last target yet; target by hand.")
	def bd():a["want_target"]=None;HOST.release_cursor(r)
	def d5(action):
		bd()
		def a(serial):A.add(tuple(action)+(int(serial or 0),),dup=True)
		HOST.pick_target(15,a)
	def cv(ref):l("target an item for %s (Esc to cancel)."%S(ref));d5(("picked_item",ref,b["page"]))
	def fD(ref,pg,serial):
		if a["shutting"]or cD():return
		c=bV(serial)
		if c is None:l("no item picked.");return
		e,i=int(c.Graphic or 0),int(c.Hue or 0);f=str(c.Name or "")or("0x%04X"%e);g=S(ref);h=[ref]
		if ref[0]=="a"and ref[1]>=z and pg!=b["page"]and C["pages"]:d=C["pages"][pg][ref[1]-z];g="page %d cell %d"%(pg+1,ref[1]-z+1);h=[]
		else:d=B(ref)
		d.update({"t":"item","v":"","g":e,"h":i,"n":f})
		for k in b6:d.pop(k,None)
		aB(recount=True,refs=h);l("%s set on %s."%(f,g),W)
	def d6(i):l("target a bag for bag slot %d (Esc to cancel)."%(i+1));d5(("picked_bag",i))
	def fE(i,serial):
		if a["shutting"]or cD():return
		b=bV(serial)
		if b is None or not b.IsContainer:l("that isn't a bag.",u);return
		dt(i,serial);a["next_scan"]=0.
	def fF(ref):
		if a["bind"]is not None:a["bind"]["sel"]=ref;l("%s; now press a key or combination for it."%S(ref))
		elif B(ref)["t"]:d4(ref)
		elif ref[0]in("a","x"):cv(ref)
		else:cz(ref)
	def cw(i):
		if a["bind"]is not None:a["bind"]["sel"]=("b",i);l("bag slot %d; now press a key or combination for it."%(i+1));return
		c=aM(i)
		if b["bagmode"]==1 and c is None:d6(i);return
		if b["bagmode"]==0:
			d=aL()
			if d in("collapsed","docked"):cd("show");al()
			elif d=="open":al();cd("dock")
			else:e=c["s"]if c else None;bx(aK,"Bags",(lambda:API.UseObject(e))if e else None)
		elif c is None:l("no bag in that slot (see Bag slots on the Action Bar settings page).")
		else:API.UseObject(c["s"])
	d7=[("item","Item...")]+[(gD,dict(br)[gD])for gD in "spell skill ability ui macro script dress undress say travel".split()];fG=dict(d7+[("hotkey","Hotkey"),("lo","Red at")]);bK={"macro":"TazUO macros","script":"Legion scripts","dress":"Dress outfits","undress":"Dress outfits"}
	def d8():a=Kit.script_dir().replace("\\","/").rstrip("/");b=os.path.dirname(a);return b if b and b!=a else a
	cx=("iplib","lib","libs","library","site-packages","dlls","stubs","__pycache__","api","docs","examples","virtueassistantmodules")
	def fH():
		b=d8();h=b.lower();c=[]
		for i,j in cs():
			p=j.replace("\\","/");a=(p[len(b):].strip("/")if b and p.lower().startswith(h)else(p or i));g=a.lower().split("/")
			if any(m in cx for m in g[:-1])or g[-1].startswith("_"):continue
			if a and a not in c:c.append(a)
		if c or not b:return sorted(c,key=lambda s:s.lower())
		with Kit.quiet:
			for k,d,e in os.walk(b):
				a=k.replace("\\","/")[len(b):].strip("/")
				if a.count("/")>=2 or "__init__.py"in e:
					d[:]=[]
					if "__init__.py"in e:continue
				d[:]=[n for n in d if not n.startswith(".")and n.lower()not in cx]
				for f in e:
					if f.lower().endswith(".py")and not f.startswith("_"):c.append((a+"/"+f)if a else f)
		return sorted(c,key=lambda s:s.lower())
	def d9(cat):
		if cat=="macro":return ClientUI.macro_names()
		if cat=="script":return fH()
		return list(API.GetAvailableDressOutfits()or[])
	cy={"macro":"The name of a macro from TazUO's macro window","script":"The script's file name (heal.py, or Spells/Bless.py)","dress":"An outfit name from TazUO's dress agent","undress":"An outfit name from TazUO's dress agent","say":"The text to say in game","hotkey":"A key or combination (F5, CTRL+Q, SHIFT+F2; blank = none)","lo":"The counter turns red at this many or fewer (0 = only when none)"}
	def fI(info):a=aH(e["g"])if K(e["g"])and info is not None else None;return None if a is None else(a[0]+info["x"],a[1]+info["y"],info["w"],info["h"])
	def fJ(w,h):
		a=j.get("anchor")
		if j.get("moved")is not None:x,y=j["moved"]
		elif a is None:x,y=300,300
		else:c,b,e,d=a;x,y=c,b+d+2
		W,H=bh()
		if W and H:
			if a is not None and j.get("moved")is None and y+h>H:y=b-2-h
			x,y=max(0,min(x,W-w)),max(0,min(y,H-h))
		return int(x),int(y)
	def aD():g,j["g"]=j["g"],None;j["c"]={};V(g)
	def fK(g):
		def a(*a):
			if j["g"]is g:j["g"]=None;j["c"]={}
		return a
	def cz(ref,bag=None):j.update({"ref":ref,"bag":bag,"level":"cats"if ref else "bag","cat":None,"page":0,"moved":None,"placed":None,"anchor":fI(e["cells"].get(ref)if ref else e["bags"].get(bag))});cA()
	def ea(rows):return[rows[c:c+bp*b5]for c in range(0,len(rows),bp*b5)]
	def fL():
		f,d=j["level"],j["cat"]
		if f=="bag":
			i=j["bag"];a=[]
			if b["bagmode"]==1:a+=[("Pick a bag...",("pickbag",i)),("Clear this slot",("clearbag",i))]
			elif b["bagmode"]==0:
				s=aL()
				if s in("collapsed","docked"):a.append(("Show the Bags window",("ub","show")))
				elif s=="open":a.append(("Fold the Bags window into the bar",("ub","dock")))
				else:a.append(("Turn Bags on",("ub","on")))
				if aK in HOST.by_key:a.append(("Bags settings",("ub","settings")))
			else:h=aM(i);a.append(("Open %s"%h["n"]if h else "No bag here",("bag",i)))
			a.append(("Hotkey: %s"%(aj()[i]or "none"),("bagbind",i)));a.append(("Bag slots: "+bs[b["bagmode"]],("bagmode",None)));return a,None
		if f=="cats":
			g=B(j["ref"]);a=[(q,("cat",o))for o,q in d7];l={"self":"self","last":"last target"}.get(g["tg"],"none");a+=[("-",None),("Hotkey: %s"%(g["k"]or "none"),("cat","hotkey")),("Press a key for it",("bindsel",None)),("Then target: %s"%l,("target",None))]
			if g["t"]in("item","travel"):a.append(("Red at: %d or fewer"%max(0,g["lo"]),("cat","lo")))
			a+=[("Clear cell",("clear",None)),("More on the settings page",("settings",None))];return a,None
		if f=="method":return[(v,("tset",t))for t,v in et],None
		if f=="list":
			if d=="spell":c=[[(x,("set",("spell",x)))for x in m.split("|")]for w,m in de];e=eA
			elif d=="skill":c,e=[[(y,("set",("skill",y)))for y in ez]],["Skills"]
			elif d=="ability":c,e=[[("Primary ability",("set",("ability","primary"))),("Secondary ability",("set",("ability","secondary")))]],["Weapon ability"]
			elif d=="travel":
				if HOST.services.get("grimoire.destinations")is None:a=[("Grimoire is off: click to turn it on",("grimon",None))]
				elif not j["items"]:a=[("No runebook read yet: open Grimoire's runebook tabs",("none",None))]
				else:a=[(ai("%s  (%s)"%(G["name"],G["book_name"]),260),("tdest",L))for L,G in enumerate(j["items"])]
				c=ea(a);e=["Runebook destinations"]*len(c)
			elif d in bK:
				a=[(ai(at,220),("set",(d,at)))for at in j["items"]]
				if not a:a=[("Nothing saved in TazUO yet",("none",None))]
				a.append(("Type a name",("typed",d)));c=ea(a);e=[bK[d]]*len(c)
			else:
				c=[[(n[1],("set",("ui",n[0])))for n in b3]];e=["Client windows"];k=[(by[1],("set",("ui",by[0])))for by in di()]
				if k:c.append(k);e.append("Module windows")
			p=max(0,min(len(c)-1,j["page"]));j["page"]=p;return c[p],(e[p],p,len(c))
		return[],None
	def cA():cU(fM)
	def fM():
		o=j["g"];p=aH(o)if K(o)else None
		if p is not None and j.get("placed")is not None and p!=j["placed"]:j["moved"]=p
		j["g"],j["stale"]=None,o;f,q=({},{}),{};a,z=Kit.MARGIN,Kit.GAP;h,r=fL();c,d=j["level"],j["ref"]
		if c=="bag":i="BAG SLOT %d"%(j["bag"]+1)
		elif c=="method":i="TRAVEL TO %s"%str((j.get("dest")or{}).get("name","?")).upper()
		elif c in("list","text"):k=fG.get(j["cat"],"Hotkey");i="%s: %s"%(S(d).upper(),k.replace("...","").upper())
		else:i="SET "+S(d).upper()
		C=M(i)+60
		if c=="text":w=max(C,340);l=92
		else:s=max(1,min(b5,(len(h)+bp-1)//bp));D=(len(h)+s-1)//s if h else 1;m=max([M(at[0])for at in h]+[100])+24;w=max(C,2*a+16+s*m);l=10+D*bq+(34 if r else 10)
		t=w-2*a;u=a+30+z+l+a;g=G.CreateGump(True,True);bT(g,w,u,corners=False);cQ(g,a,a,t,30);I(g,i,a+10,a+7,ae);af(g,f,"close",cM,w-a-34,a+4,None,"Close the menu",on_click=A(("mpick","close",None)))
		if c not in("cats","bag"):af(g,f,"back",bR,w-a-54,a+7,None,"Back to the previous menu",on_click=A(("mpick","back",None)))
		b=a+30+z;cQ(g,a,b,t,l)
		if c=="text":
			n=B(d)
			if j["cat"]=="lo":E=str(max(0,n["lo"]))
			else:E=n["k"]if j["cat"]=="hotkey"else(n["v"]if n["t"]==j["cat"]else "")
			I(g,cy.get(j["cat"],""),a+10,b+8,J);q["text"]=bS(g,E,a+10,b+32,t-20,numbers=False);af(g,f,"ok",cN,a+10,b+62,"Apply","Save this value on the cell",on_click=A(("mpick","text",None)));q["status"]=I(g,"",a+10+35+M("Apply")+12,b+65,J)
		else:
			for H,(k,e)in enumerate(h):
				L,N=divmod(H,D);x=a+8+L*m;y=b+6+N*bq
				if e is None:Y(g,cO,x,y+bq//2,m-16,1);continue
				O=e[0]=="set"and(B(d)["t"],B(d)["v"])==e[1]or e[0]in("tdest","tset")and fN(d,e);I(g,k,x+4,y+2,W if O else X);aF(g,x,y,m-8,bq,A(("mpick",)+tuple(e)),k)
			if r:
				P,Q,F=r;v=b+l-28;I(g,"%s  (%d of %d)"%(P,Q+1,F),a+10,v+4,J)
				if F>1:af(g,f,"next",aW,w-a-44,v,None,"Next page",on_click=A(("mpick","page",1)));af(g,f,"prev",aW,w-a-84,v,None,"Previous page",on_click=A(("mpick","page",-1)))
		x,y=fJ(w,u);x,y=bX(g,x,y,w,u);j.update({"g":g,"c":q,"placed":(x,y)});G.AddControlOnDisposed(g,fK(g));G.AddGump(g);g.SetInScreen();V(j.pop("stale",None))
	def eb(ref,t,v):a=B(ref);b=dict(ad(),t=t,v=v,k=a["k"],tg=a["tg"],lo=a["lo"]);C[ref[0]][ref[1]]=b;aB(recount=True,refs=[ref]);l("%s set on %s."%(ak(b),S(ref)),W)
	def fN(ref,action):
		c=B(ref)
		if c["t"]!="travel":return False
		if action[0]=="tdest":a=j["items"];d=a[action[1]]if 0<=action[1]<len(a)else None
		else:
			d=j.get("dest")
			if c.get("rm")!=action[1]:return False
		if not d:return False
		try:return(int(c.get("rb")or "0",16)==int(d["book"])and c.get("ri")==str(int(d["index"])))
		except(ValueError,TypeError,KeyError):return False
	def am(**a):j.update(a);cA()
	def fO(what,a):
		b=j["ref"]
		if what in("close","bindsel","bagbind","set","settings","pickbag","clearbag","ub","bag","bagmode","tset","grimon")or(what,a)==("cat","item"):aD()
		if what in ec:ec[what](b,a)
	def fP(ref,a):
		if j["level"]=="method":am(level="list",cat="travel")
		else:am(level="cats",cat=None,page=0)
	def fQ(ref,a):
		if a=="travel":b=HOST.services.get("grimoire.destinations");am(items=list(safe(b,[])or[])if b is not None else[],level="list",cat="travel",page=0);return
		if a=="item":cv(ref);return
		if a in bK and aT():
			def c():
				b=d9(a)
				if j["ref"]==ref and j["level"]=="cats"and K(j["g"]):am(items=b,level="list",cat=a,page=0)
			ah(c);return
		if a in("spell","skill","ability","ui","macro","script","dress","undress"):am(items=d9(a)if a in bK else[],level="list",cat=a,page=0);return
		am(level="text",cat=a)
	def fR(ref,a):
		if j["level"]=="list"and j["cat"]=="travel"and 0<=a<len(j["items"]):am(level="method",dest=j["items"][a])
	def fS(ref,a):
		if j.get("dest")and ref is not None:eX(ref,j["dest"],a)
	def fT(ref,c):
		v=str(j["c"]["text"].Text or "").strip()
		if j["cat"]=="hotkey":
			k=_norm_key(v);a=ay(k)
			if a:aI(j["c"]["status"],"%s belongs to %s"%(k,a),u);return
			if k:cq(ref,k)
			else:B(ref)["k"]="";aB(refs=[ref])
			aD();return
		if j["cat"]=="lo":
			try:b=int(v)
			except ValueError:aI(j["c"]["status"],"Type a number",u);return
			B(ref)["lo"]=max(0,b);aB(refs=[ref]);aD();return
		if not v:aI(j["c"]["status"],"Type a value first",u)
		else:aD();eb(ref,j["cat"],v)
	def fU(ref,a):c=B(ref);c["tg"]={"":"self","self":"last","last":""}.get(c["tg"],"");a4();aR([ref]);an(r);cA()
	def fV(ref,a):dD(ref);aD()
	def fW(ref,a):P["sel"]=eG(ref);bf(r);an(r)
	def fX(ref,b):dt(b,0);a["next_scan"]=0.
	def fY(ref,a):
		if a=="settings":
			if aK in HOST.by_key:bf(aK)
		elif a=="on":bx(aK,"Bags")
		else:al();cd(a)
	ec={"bindsel":lambda ref,a:cp(ref),"bagbind":lambda ref,a:cp(("b",a)),"set":lambda ref,a:eb(ref,a[0],a[1]),"pickbag":lambda ref,a:d6(a),"bag":lambda ref,a:cw(a),"bagmode":lambda ref,a:bf(r),"grimon":lambda ref,a:bx(c5,"Grimoire"),"page":lambda ref,a:am(page=j["page"]+a),"back":fP,"cat":fQ,"tdest":fR,"tset":fS,"typed":lambda ref,a:am(level="text",cat=a),"text":fT,"target":fU,"clear":fV,"settings":fW,"clearbag":fX,"ub":fY}
	def ed(ref):
		if ref[0]=="b":cw(ref[1])
		else:d4(ref)
	def fZ(ref):
		try:ed(ref)
		except Exception as a:l("couldn't use %s (%s)."%(S(ref),a),u)
	F={"g":None,"at":(0,0),"cells":[],"until":0.,"hot":None,"box":[],"side":0,"rad":0,"half":0,"start":(0,0)}
	def f_():p=b["radial_page"];a=b["page"]if not p else p-1;return[c for c in[("p",a*N+d)for d in range(N)]if B(c)["t"]]
	def bL():g,F["g"]=F["g"],None;F.update(cells=[],hot=None,box=[]);V(g)
	def f0():
		bL();i=f_()
		if not i:l("the radial ring's page has no filled cells.");return
		W,H=bh();j=aY()or(W//2,H//2);c=sc(b["slot"],20);p=len(i);h=int(max(eq,er*p)*max(1.,c/44.));a=h+c//2+22;g=G.CreateGump(False,False);d=[];q=[]
		for v,k in enumerate(i):
			r=2*math.pi*v/p-math.pi/2;m,s=int(round(h*math.cos(r))),int(round(h*math.sin(r)));x,y=a+m-c//2,a+s-c//2;n=B(k);d.append(Y(g,aq,x,y,c,c,ar));w,z=dK(g,k,n,{},x,y,c,c,0);d.extend(w)
			if z is not None and n["t"]!="travel":t=ai(ak(n),c+28);d.append(I(g,t,a+m-M(t)//2,y+c+1))
			q.append((m,s,k))
		d.append(cP(g,a-3,a-3,6,6,.8,"#909090"));o=[cP(g,0,0,2,2,.95,es)for L in range(4)]
		for u in d+o:
			if u is not None:Kit.inert(u)
		for A in o:A.SetAlpha(0.)
		e,f=j[0]-a,j[1]-a
		if W and H:e,f=max(0,min(e,W-2*a)),max(0,min(f,H-2*a))
		e,f=bX(g,e,f,2*a,2*a);G.AddGump(g);SNAP.skip_gump(g);F.update(g=g,at=(e+a,f+a),cells=q,until=time.time()+ep,hot=None,box=o,side=c,rad=h,half=a,start=j)
	def ee(pos):
		g=F["g"];a=aH(g)if g is not None else None
		if pos is None or a is None or not F["cells"]:return
		d=F["half"];e,f=pos[0]-a[0]-d,pos[1]-a[1]-d;h=math.hypot(e,f)
		if h<c0 or h>F["rad"]+F["side"]//2+12:return
		if math.hypot(pos[0]-F["start"][0],pos[1]-F["start"][1])<c0:return
		i,b=None,None
		for c in F["cells"]:
			j=(c[0]-e)**2+(c[1]-f)**2
			if b is None or j<b:i,b=c,j
		return i
	def f1(now):
		if now>=F["until"]or not K(F["g"]):bL();return
		a=ee(aY());c=a[2]if a else None
		if c==F["hot"]:return
		F["hot"]=c;d=F["box"]
		if a is None:
			for b in d:b.SetAlpha(0.)
			return
		s,e=F["side"],F["half"];x,y=e+a[0]-s//2-2,e+a[1]-s//2-2
		for b,r in zip(d,((x,y,s+4,2),(x,y+s+2,s+4,2),(x,y,2,s+4),(x+s+2,y,2,s+4))):b.SetRect(*r);b.SetAlpha(.95)
	def f2():
		if F["g"]is None:return
		a=ee(aY());bL()
		if a is not None:A.add(("use",a[2]))
	def f3():b["radial_page"]=(b["radial_page"]+1)%(T+1);aa();an(r)
	f4={"a":Z,"u":E,"x":a_,"p":T*N};f5=dict(br)
	def f6(q,n=8):
		d=str(q or "").lower().split();a=[];n=int(n or 0);e=([("a",g)for g in range(z)]+[("x",h)for h in range(a_)]+[("p",k)for k in range(T*N)]+[("u",m)for m in range(E)])
		for r in e:
			if len(a)>=n:break
			c=B(r);t=c["t"]
			if not t or not bt(r)or(t=="ui"and c["v"]=="launcher"):continue
			b=a2(c)if t=="travel"else ak(c)
			if not all(i in("%s %s"%(b,f5.get(t,t))).lower()for i in d):continue
			f={"a":"top row","u":"button %d"%(r[1]+1),"x":"row %d"%(r[1]//z+2),"p":"page %d"%(r[1]//N+1)}[r[0]];a.append(("%s  (%s)"%(b,f),r,"outfit"if t in("dress","undress")else t))
		return a
	def f7(ref):
		try:
			a,i=ref;i=int(i)
			if not 0<=i<f4.get(a,0):return False
		except Exception:return False
		if not bt((a,i))or not B((a,i))["t"]:return False
		b=A.add(("use",(a,i)));aU(r);return b
	H={"ok":None,"held":{},"map":{},"hooks":None,"ring":None,"ring_down":None}
	def ef(k):
		b,a=_norm_key(k).split("+"),None
		for p in b:
			if p and p not in("CTRL","SHIFT","ALT"):a=p if p.startswith("SDLK_")else "SDLK_"+p
		c=[d for d in("CTRL","SHIFT","ALT")if d in b];return "+".join(c+([a]if a else[]))
	def f8(a):return "+".join(c[5:]if c.startswith("SDLK_")else c for c in str(a).upper().split("+"))
	def f9(ref):
		if ref[0]=="b":return(a["bind"]is None and aM(ref[1])is not None and(b["bagmode"]!=0 or a["ub_state"]is not None))
		c=B(ref)
		if c["t"]=="ui":d=a0(c["v"]);e=d[3]if d else "";return(e in("war","help","quests","paperdoll","lock","minimize")or e.startswith(("ga:","macro:")))
		return c["t"]in("item","spell","skill","ability","macro","say","dress","undress","travel")
	def ga(b):
		try:
			if not H["ok"]:return
			b=str(b);f=b.rsplit("+",1)[-1];g,c=time.time(),H["held"];h=c.get(f);c[f]=g
			if h is not None and g-h<cZ:return
			if len(c)>32:
				for k in[i for i,m in c.items()if g-m>=cZ]:del c[k]
			if a["shutting"]or e["g"]is None:return
			if a["bind"]is not None:
				if not bP():A.add(("bindkey",f8(b)),dup=True);aU()
				return
			if b==H["ring"]:
				if not bP():H["ring_down"]=f;A.add(("ring",True),dup=True);aU(r)
				return
			d=H["map"].get(b)
			if d is None or bP():return
			if f9(d):fZ(d)
			else:A.add(("use",d),dup=True);aU()
		except Exception:pass
	def gb(b):
		try:
			a=str(b).rsplit("+",1)[-1];H["held"].pop(a,None)
			if H["ring_down"]==a:H["ring_down"]=None;A.add(("ring",False),dup=True);aU(r)
		except Exception:pass
	def gc():
		if H["ok"]is not None:return
		H["ok"]=False
		try:
			import clr;import System;from System.Reflection import BindingFlags;d=BindingFlags.Static|BindingFlags.Public|BindingFlags.NonPublic;e=be("ClassicUO.Input.Keyboard");a,b=e.GetEvent("KeyDownEvent",d),e.GetEvent("KeyUpEvent",d);c=clr.GetPythonType(a.EventHandlerType)(ga);f=clr.GetPythonType(b.EventHandlerType)(gb);a.GetAddMethod(True).Invoke(None,System.Array[object]([c]))
			try:b.GetAddMethod(True).Invoke(None,System.Array[object]([f]))
			except Exception:a.GetRemoveMethod(True).Invoke(None,System.Array[object]([c]));raise
			H.update({"hooks":(a,c,b,f),"ok":True,"held":{}})
		except Exception as g:l("couldn't read the keyboard, so cell hotkeys are off (%s)."%g,u)
	def gd():
		a,H["hooks"]=H["hooks"],None;H["ok"]=None if a else H["ok"];H.update(map={},ring=None,ring_down=None)
		if not a:return
		import System;b,c,d,e=a;safe(lambda:b.GetRemoveMethod(True).Invoke(None,System.Array[object]([c])));safe(lambda:d.GetRemoveMethod(True).Invoke(None,System.Array[object]([e])))
	cB=set()
	def cC(what,text):
		if what not in cB:cB.add(what);l(text,u)
	def aE():
		c={}
		for r,d in az():
			k=_norm_key(d["k"])
			if not k or not d["t"]or not bt(r):continue
			a=ay(k)
			if a:cC((k,a),"%s belongs to %s; %s has no hotkey."%(k,a,S(r)));continue
			if k in c:cC((k,"two cells"),"%s is on two cells; %s gets it."%(k,S(r)))
			c[k]=r
		for i,k in enumerate(aj()):
			if k and not ay(k):c[k]=("b",i)
		H["map"]=dict((ef(f),g)for f,g in c.items())if H["ok"]else{};b=b8();a=HOST.hotkeys_owned.get(b)if b else None
		if a:cC((b,a),"%s belongs to %s; the radial ring has no key."%(b,a))
		H["ring"]=ef(b)if b and not a and H["ok"]else None
	eg={"click":fF,"use":ed,"bag":cw,"ui":cr,"pick":cv,"menu":cz,"mpick":fO,"picked_item":fD,"picked_bag":fE,"bindkey":fv,"lockbar":dZ,"grid":fk,"bagmenu":lambda i:cz(None,i),"page":lambda step:eM(b["page"]+step),"bind":lambda:cp()if a["bind"]is None else bH(),"ring":lambda down:f0()if down else f2(),"ring_bind":fu,"ring_page":f3}
	def ge(w):a=(w-24)//3;c=bj("Value: a spell, skill, macro or outfit name, primary or secondary, a script file, text to say, or an item graphic (0x0E21, or 0x0E21,1153 with a hue).",w-24)[:3];return(("BAR",(("check","lock","Lock in place","Keep the bar where it is (unlocked: drag its stone edge)",{"stay":True}),("check","top","Show the top row","Show the 24-cell row above the bottom row",{"stay":True,"dx":12+a}),("check","keys","Show hotkeys","Show each cell's hotkey in its corner",{"dx":12+2*a}),("check","short","Short counts","Show 1200 as 1.2k on the counters",{"stay":True}),("check","hue","Count same hue only","Count only items of the cell's hue",{"stay":True,"dx":12+a}),("custom",28,gf),("slider","slot","Cell size:","Cell side in pixels (%d-%d)"%(bk,bl),bk,bl,{"sw":120,"vfmt":"%d px","stay":True}),("custom",26,gg),("custom",26,gh),("slider","scale","Scale:","Size of the whole bar (%d-%d%%); text keeps its size"%(ao,aw),ao,aw,{"sw":160,"vfmt":"%d%%"}),("slider","extra","Extra rows:","Rows of %d cells above the top row (0-%d); hidden rows' hotkeys are off"%(z,bn),0,bn,{"sw":100,"vfmt":"%d","stay":True}),("custom",26,gi)),{"ldy":2,"sdy":6,"lgap":8,"ugap":10,"fh":26,"pad":6}),("RADIAL RING",[("buttons",(("radial",bQ,"Ring key: %s"%(b["radial"]or "none"),"Pick the key to hold for a ring of one page's cells (Backspace clears it)",A(("ring_bind",))),("radial_page",aW,"Ring page: %s"%(b["radial_page"]or "shown"),"Choose the page the ring shows: the shown page or page 1-12",A(("ring_page",)))))]+[("note",d)for d in bj("Hold the key, point at a cell and let go to use it; the middle or outside uses nothing.",w-24)]),("EDIT A CELL",[("custom",128,gj)]+[("note",f)for f in c]),("HOW TO USE",[("note",h)for g in eB for h in bj(g,w-24)]))
	def eh(f,by,a):return Kit.buttons(f.g,f.store,f.x+12,by,a,16)
	def bM(f,lx,a,label,key,b,c,value,tooltip):I(f.g,label,lx,a+2);d=[g[0]for g in c];P["dds"].append((key,lx+M(label)+8,a,b,[h[1]for h in c],d.index(value)if value in d else 0,tooltip));return lx+M(label)+8+b+16
	def gf(f,x,y):b=a["ub_found"];c=aL();e=({"open":"Bags: shown","collapsed":"Bags: folded","docked":"Bags: in the bar"}.get(c)if c else "Bags: off"if b else "Bags: not found"if b is False else "Bags: not in use");b=b or c is not None;d=(f.w-24)//3;I(f.g,ai(e,d-6),x+12+2*d,y+2,W if b else J)
	def gg(f,x,y):bM(f,x+f.w-12-170-8-M("Bag slots:"),y,"Bag slots:","bagmode",170,list(enumerate(bs)),b["bagmode"],"Where the bag slots get bags: Inventory > Bags, bags you target, or your backpack and its bags")
	def gh(f,x,y):a=eh(f,y,(("pgprev",aW,"Prev","Show the previous bottom-left page"),("pgnext",aW,"Next","Show the next bottom-left page"),("bind",bQ,"Keybind mode","Start keybind mode: hover a cell and press a key")));I(f.g,ai("Bar page %d of %d"%(b["page"]+1,T),x+f.w-16-a),a,y+3,J)
	def gi(f,x,y):c=x+12+M("Extra rows:")+8;a=b["anchor"];d={"":"none (drop near a corner or edge middle)","L":"left edge, upright","R":"right edge, upright","T":"top edge","B":"bottom edge","C":"screen centre"}.get(a,{"TL":"top-left","TR":"top-right","BL":"bottom-left","BR":"bottom-right"}.get(a,a)+" corner");I(f.g,ai("Anchor: %s"%d,x+f.w-16-(c+130)),c+130,y+2,J)
	def gj(f,x,y):
		g,e,w=f.g,f.c,f.w;i=P["sel"];a=B(a1(i));b=bM(f,x+12,y,"Cell:","sel",120,list(enumerate(eH())),i,"The cell to edit (right-clicking a cell on the bar does the same)");b=bM(f,b,y,"Does:","does",150,br,a["t"],"What a click or the hotkey does");bM(f,b,y,"Target:","target",100,dc,a["tg"],"Answer the cell's target cursor with yourself or your last target (when no other module holds it)");I(g,"Value:",x+12,y+34)
		if a["t"]=="item":c=("0x%04X"%a["g"])+((",%d"%a["h"])if a["h"]else "")
		elif a["t"]=="ui":c=""
		elif a["t"]=="travel":c=a2(a)
		else:c=a["v"]
		d=x+12+max(M("Value:"),M("Window:"))+8;e["value"]=av(bS(g,c,d,y+32,x+w-16-d,numbers=False),"The cell's value (see below; a Client window cell uses Window)");I(g,"Window:",x+12,y+66);j=dj();k=[s[0]for s in j];P["dds"].append(("window",d,y+64,140,[t[1]for t in j],k.index(a["v"])if a["t"]=="ui"and a["v"]in k else 0,"The client or module window a Client window cell opens"));b=d+140+16
		for m,h,n,l,o,p in(("key","Hotkey:",a["k"],100,False,cy["hotkey"]+"; or use Keybind mode"),("lo","Red at:",str(a["lo"]),40,True,cy["lo"])):I(g,h,b,y+66);e[m]=av(bS(g,n,b+M(h)+8,y+64,l,numbers=o),p);b+=M(h)+8+l+16
		q=eh(f,y+96,(("apply",cN,"Apply","Save this cell"),("pick",bQ,"Pick item...","Target an item for this cell"),("clear",cM,"Clear","Empty this cell")));e["status"]=I(g,"",q,y+99,J)
	def gk(g,x,y,w):
		if not C["a"]:dq()
		P["dds"]=[];f=ab.build(g,x,y,w)
		for c,e,h,i,j,k,l in sorted(P["dds"],key=lambda d:-d[2]):a=G.CreateDropDown(i,j,k);a.SetPos(e,h);g.Add(a);f.c[c]=av(a,l)
		P.update({"seen_sel":P["sel"],"seen_bag":b["bagmode"]})
	def aS(text,hue=None):
		if ab.f is not None:aI(ab.f.c["status"],text,J if hue is None else hue)
	def gl():
		d=ab.f.c;e=a1(P["sel"]);a=B(e)
		def f(a,dd):return a[max(0,min(len(a)-1,bU(dd,0)))][0]
		t=f(br,d["does"]);v=str(d["value"].Text or "").strip();i=f(dc,d["target"]);k=_norm_key(d["key"].Text);g=ay(k)
		if g:aS("%s belongs to %s"%(k,g),u);return
		try:h=int(str(d["lo"].Text or "0"))
		except Exception:h=c_
		b=dict(ad(),t=t,tg=i,k=k,lo=h)
		if t=="item":
			c=eF(v)
			if c is None and a["t"]=="item"and a["g"]:c=(a["g"],a["h"])
			if c is None:aS("Pick an item, or type its graphic",u);return
			b.update({"g":c[0],"h":c[1],"n":a["n"]if(a["g"],a["h"])==c else "0x%04X"%c[0]})
		elif t=="ui":b["v"]=f(dj(),d["window"])
		elif t=="ability":b["v"]="secondary"if v.lower().startswith("s")else "primary"
		elif t=="travel":
			if a["t"]!="travel":aS("Pick its destination: right-click the cell, then Travel (runebook)",u);return
			b["tg"]=""
			for k in("v","n")+b6:b[k]=a.get(k,"")
		elif t:
			if not v:aS("Type a value first",u);return
			b["v"]=v
		C[e[0]][e[1]]=b
		if b["k"]and b["k"]!=_norm_key(a["k"]):cq(e,b["k"])
		aB(recount=True,refresh=False,refs=[e]);aS("Saved %s"%S(e),W)
	def gm(f):
		for a,b in(("pgprev",("page",-1)),("pgnext",("page",1)),("bind",("bind",))):
			if bi(f.store,a):A(b)()
		if bi(f.store,"apply"):gl()
		if bi(f.store,"pick"):A(("pick",a1(P["sel"])))();aS("Target the item")
		if bi(f.store,"clear"):dD(a1(P["sel"]))
	def gn(f,new):
		a=bU(f.c["bagmode"],b["bagmode"])
		if a!=P["seen_bag"]and 0<=a<len(bs):P["seen_bag"]=new["bagmode"]=a
		c=bU(f.c["sel"],P["sel"])
		if c!=P["seen_sel"]and 0<=c<Z+E+a_:P["sel"]=c;an(r)
	def go(b,new):
		if new["bagmode"]!=b["bagmode"]:a["bag_sig"],a["next_scan"]=None,0.
		aE();au(.4)
	ab=Kit.Page(b,ge,aa,go,adjust=gn,clicks=gm,every=.2);dp()
	def gp():a.update(df(),minimized=Kit.load_min(b1),em=False,ub_last=None,ub_pending=True,counted_at=0.);cB.clear();H.update(held={},ring_down=None);D.update(scale=None,vertical=None,slot=None,sig=None);dp();dq();dz();a["ub_state"],a["grim_state"],a["va_state"]=aL(),bv(),cc();al();HOST.layout_add(r,fo,aZ,e7);ax.add(HOST.layout_remove,r);a.update(dock_sig=dw(),tray_sig=dx(),watch_next=0.,owned_sig=frozenset(HOST.hotkeys_owned));dU();a.update(rebuild_at=0.,redraw=set());gc();aE();ax.service("actionbar.hotkeys",e1);ax.service("look.actionbar",au);ax.service("actionbar.find",f6);ax.service("actionbar.use",f7);ax.add(bL)
	def gq():
		if a["shutting"]or e["g"]is None:return
		if Kit.closed(e):return
		c=time.time();fC(c);fy(c);eO()
		if a["minimized"]and a["em"]==ag(r)and not a["rebuild_at"]:au()
		h=bO()
		if h!=e.get("arranging",False):
			e["arranging"]=h
			if e.get("lockbtn"):bF(e["lockbtn"],*co())
		while a["queue"]:
			d=a["queue"].pop(0);f=d[0]
			if f in eg:eg[f](*d[1:])
			elif f=="dock":
				g=dict(ce()).get(d[1])
				if g is not None:
					s=safe(g.get("state"))
					if s is None:
						if g.get("on"):safe(g["on"])
						else:ah(lambda k=d[1]:safe(lambda:bN(k)))
					elif s=="open":cG(d[1])
					else:safe(g.get("show"))
					a["dock_sig"],a["watch_next"]=None,0.
			elif f=="traywin":b["tray_open"]=not b["tray_open"];aa();dO()
			elif f=="toggle_min":
				if ag(r)and not a["minimized"]:continue
				a5();a["minimized"]=not a["minimized"];cV(b1,a["minimized"]);al();au()
			if a["shutting"]or e["g"]is None:return
		c=time.time()
		if F["g"]is not None:f1(c)
		if c>=a["next_scan"]:
			a["next_scan"]=c+2.;dz();eR();al()
			if a.get("last_pos")!=a.get("pos_saved"):a5()
		if a["rebuild_at"]and c>=a["rebuild_at"]:a["rebuild_at"]=0.;a["redraw"]=set();dU()
		elif a["redraw"]:fp()
		if c>=a["next_count"]or(a.get("pack_v")is not None and c-a.get("counted_at",0.)>=eo and cK()!=a["pack_v"]):a["next_count"]=c+b2;eS()
		e_(c)
		if c>=a.get("tray_next",0.):a["tray_next"]=c+.1;fr(c)
	def gr():
		while a["jobs"]and not a["shutting"]:a["jobs"].pop(0)()
	def gs():
		a["shutting"]=True;ax.close();bd();g,ac["g"]=ac["g"],None;V(g);a["bind"]=None;aD();al(False);gd()
		with Kit.quiet:cU(a5)
		cV(b1,a["minimized"]);aa();a4();g,e["g"]=e["g"],None;V(g)
		for s in e.pop("stale",[]):V(s)
	return{"start":gp,"tick":gq,"stop":gs,"client_tick":True,"config_height":ab.height,"build_config":gk,"poll_config":ab.poll,"config_closed":ab.closed,"thread_tick":gr,"thread_wanted":lambda:bool(a["jobs"])}
if "HOST"not in globals():
	import API
	exec(open(API.ScriptPath+"/../VirtueAssistantModules/_Alone.py").read())
HOST.add("actionbar","Action Bar","Cells for items, spells, skills and windows",_module_actionbar,.05,category="On screen")
